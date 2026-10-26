#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import re
from pathlib import Path
import shutil

# --- Configuration ---
TIMEOUT_SECONDS = 300  # 5 minutes timeout for commands
VENDORED_DIRS = {"node_modules", ".venv", "venv", ".git", "build", "target"}

# --- Global State ---
RESULTS = [] # List of {"name": str, "status": "pass"|"fail"|"warn", "details": str}

# --- Helper Functions ---

def run_cmd(cmd, cwd=None, shell=True, timeout=TIMEOUT_SECONDS):
    """Runs a shell command and returns stdout, stderr, and return code."""
    try:
        # If shell is False, cmd should be a list
        if not shell and isinstance(cmd, str):
            cmd = cmd.split()
            
        result = subprocess.run(
            cmd,
            shell=shell,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout} seconds", 124
    except Exception as e:
        return "", str(e), 1

def check_file(filename):
    return os.path.exists(filename)

def record_result(name, status, details=""):
    RESULTS.append({"name": name, "status": status, "details": details})
    if status == "pass":
        print_success(f"{name} passed")
    elif status == "fail":
        print_failure(f"{name} failed", details)
        print_summary()  # Stop on first failure; exits 1
    elif status == "warn":
        print_warning(f"{name}: {details}")

def print_header(title):
    print(f"\n{ '='*len(title)}\n{title}\n{ '='*len(title)}")

def print_step(msg):
    print(f"🔹 {msg}")

def print_success(msg):
    print(f"✅ {msg}")

def print_failure(msg, details=""):
    print(f"❌ {msg}")
    if details:
        # Indent details for cleaner output
        details_indented = "\n".join(["    " + line for line in details.strip().splitlines()][:20]) # Limit lines
        if len(details.strip().splitlines()) > 20:
             details_indented += "\n    ... (output truncated)"
        print(details_indented)

def print_warning(msg):
    print(f"⚠️ {msg}")

def print_summary():
    if not RESULTS:
        return

    print_header("QA Summary")
    print(f"{'Check':<25} | {'Status':<10}")
    print("-" * 40)
    
    all_passed = True
    for res in RESULTS:
        status_icon = "✅ PASS" if res['status'] == 'pass' else "❌ FAIL" if res['status'] == 'fail' else "⚠️ WARN"
        print(f"{res['name']:<25} | {status_icon}")
        if res['status'] == 'fail':
            all_passed = False
            
    print("-" * 40)
    if all_passed:
        print("🎉 All checks passed!")
        sys.exit(0)
    else:
        print("🛑 Some checks failed.")
        sys.exit(1)

# --- Language/Tool Handlers ---

def check_pre_commit():
    if check_file(".pre-commit-config.yaml"):
        print_step("Found .pre-commit-config.yaml")
        out, err, rc = run_cmd("pre-commit run --all-files")
        if rc == 0:
            record_result("pre-commit", "pass")
        elif "command not found" in err or "not recognized" in err:
            record_result("pre-commit", "warn", "Command not found")
        else:
            record_result("pre-commit", "fail", out + err)
        return True
    return False

def check_makefile():
    if check_file("Makefile"):
        with open("Makefile", errors='ignore') as f:
            content = f.read()
        
        # Priority list
        targets = ["lint", "check", "test", "tests", "qa"]
        for t in targets:
            if re.search(rf"^{t}\s*:", content, re.MULTILINE):
                print_step(f"Found Makefile target: '{t}'")
                out, err, rc = run_cmd(f"make {t}")
                if rc == 0:
                    record_result(f"make {t}", "pass")
                else:
                    record_result(f"make {t}", "fail", out + err)
                return True
    return False

def detect_python_environment():
    """Detects the active Python environment manager."""
    # 1. Pixi
    if check_file("pixi.toml") or check_file("pixi.lock"):
        if shutil.which("pixi"):
            print_step("Detected 'pixi' project.")
            return "pixi run "
        else:
            print_warning("Detected 'pixi' files but 'pixi' command not found.")

    # 2. Poetry
    if check_file("poetry.lock"):
        if shutil.which("poetry"):
            print_step("Detected 'poetry' project.")
            return "poetry run "
        else:
            print_warning("Detected 'poetry' lockfile but 'poetry' command not found.")
            
    # 3. Uv
    if check_file("uv.lock"):
        if shutil.which("uv"):
            print_step("Detected 'uv' project.")
            return "uv run "
        else:
             print_warning("Detected 'uv' lockfile but 'uv' command not found.")

    # 4. Conda/Mamba
    conda_prefix = os.environ.get("CONDA_PREFIX")
    if conda_prefix:
        env_name = os.environ.get("CONDA_DEFAULT_ENV", "unknown")
        print_step(f"Detected active Conda/Mamba environment: '{env_name}'")
        return "" 
    
    # 5. Virtualenv
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
         print_step(f"Detected active Virtualenv: '{Path(venv).name}'")
         return "" 

    return ""

def check_python(cwd):
    is_python = check_file("requirements.txt") or check_file("pyproject.toml") or check_file("setup.py") or any(Path(cwd).glob("*.py"))
    if not is_python:
        return False

    print_header("Python QA")
    cmd_prefix = detect_python_environment()
    
    # 1. Try existing environment tools with prefix
    tools = ["ruff", "flake8", "pylint", "mypy", "pytest"]
    available_tools = []
    
    for tool in tools:
        check_cmd = f"{cmd_prefix}{tool} --version"
        _, _, rc = run_cmd(check_cmd)
        if rc == 0:
            available_tools.append(tool)

    if available_tools:
        print_step(f"Found tools: {', '.join(available_tools)}")
        
        if "ruff" in available_tools:
            out, err, rc = run_cmd(f"{cmd_prefix}ruff check .")
            record_result("ruff", "pass" if rc == 0 else "fail", out)
        
        if "flake8" in available_tools and "ruff" not in available_tools:
            out, err, rc = run_cmd(f"{cmd_prefix}flake8 .")
            record_result("flake8", "pass" if rc == 0 else "fail", out)

        if "mypy" in available_tools:
            out, err, rc = run_cmd(f"{cmd_prefix}mypy .")
            record_result("mypy", "pass" if rc == 0 else "fail", out)

        if "pytest" in available_tools:
            out, err, rc = run_cmd(f"{cmd_prefix}pytest -q")
            if rc == 5:
                record_result("pytest", "warn", "No tests collected")
            else:
                record_result("pytest", "pass" if rc == 0 else "fail", out + err)
        
        return True

    if cmd_prefix.strip():
        print_warning(f"Detected project environment ({cmd_prefix.strip()}) but no QA tools found.")
    else:
        print_warning("No Python QA tools found. Run them manually.")
    return True

def check_node():
    if not check_file("package.json"):
        return False
    
    print_header("Node.js QA")
    try:
        with open("package.json") as f:
            pkg = json.load(f)
        scripts = pkg.get("scripts", {})
        
        pm = "npm"
        if check_file("yarn.lock"): pm = "yarn"
        elif check_file("pnpm-lock.yaml"): pm = "pnpm"
        
        if "lint" in scripts:
            out, err, rc = run_cmd(f"{pm} run lint")
            record_result("npm lint", "pass" if rc == 0 else "fail", out + err)
        elif "check" in scripts:
             out, err, rc = run_cmd(f"{pm} run check")
             record_result("npm check", "pass" if rc == 0 else "fail", out + err)
        else:
            record_result("npm lint", "warn", "No lint/check script found")

        if "test" in scripts:
            out, err, rc = run_cmd(f"{pm} run test")
            record_result("npm test", "pass" if rc == 0 else "fail", out + err)
            
    except Exception as e:
        record_result("package.json", "fail", str(e))
    
    return True

def check_rust():
    if not check_file("Cargo.toml"):
        return False
    
    print_header("Rust QA")
    
    out, err, rc = run_cmd("cargo check")
    record_result("cargo check", "pass" if rc == 0 else "fail", err)

    if shutil.which("cargo-clippy"):
        out, err, rc = run_cmd("cargo clippy -- -D warnings")
        record_result("cargo clippy", "pass" if rc == 0 else "fail", err)

    out, err, rc = run_cmd("cargo test")
    record_result("cargo test", "pass" if rc == 0 else "fail", out + err)
    
    return True

def check_go():
    if not check_file("go.mod"):
        return False
    
    print_header("Go QA")
    
    out, err, rc = run_cmd("go vet ./...")
    record_result("go vet", "pass" if rc == 0 else "fail", err)
    
    out, err, rc = run_cmd("go test ./...")
    record_result("go test", "pass" if rc == 0 else "fail", out + err)
    
    return True

def check_cpp():
    # Skip vendored dirs: native Node/Python deps ship .c files
    is_cpp = any(
        not VENDORED_DIRS.intersection(f.parts)
        for ext in ("*.cpp", "*.c")
        for f in Path.cwd().rglob(ext)
    )
    if not is_cpp:
        return False
        
    print_header("C/C++ QA")
    
    # Check for clang-format
    if shutil.which("clang-format"):
        # Just check one file to see if it works or if config exists?
        # Better: check for .clang-format
        if check_file(".clang-format"):
             print_step("Found .clang-format. Checking format (dry-run)...")
             # dry run is hard with clang-format without checking all files?
             # We can run --dry-run --Werror on all source files?
             # Too complex for generic script.
             record_result("clang-format", "warn", "Found config but full check skipped (complex).")
        else:
             record_result("clang-format", "warn", "Tool found but no .clang-format config.")

    # Check for cppcheck
    if shutil.which("cppcheck"):
        print_step("Running cppcheck...")
        out, err, rc = run_cmd("cppcheck . --error-exitcode=1 --quiet " + " ".join(f"-i {d}" for d in VENDORED_DIRS))
        record_result("cppcheck", "pass" if rc == 0 else "fail", err)
        
    return True

def main():
    cwd = os.getcwd()
    print(f"🕵️  QA Skill analyzing: {cwd}")
    
    # 1. Config based (Pre-commit / Makefile)
    ran_config = False
    if check_pre_commit(): ran_config = True
    if check_makefile(): ran_config = True
    
    if ran_config:
        print_summary()
        return

    # 2. Language Autodetection
    ran_lang = False
    if check_python(cwd): ran_lang = True
    if check_node(): ran_lang = True
    if check_rust(): ran_lang = True
    if check_go(): ran_lang = True
    if check_cpp(): ran_lang = True
    
    if not ran_lang:
        print_warning("No recognized project structure found.")
        
    print_summary()

if __name__ == "__main__":
    main()