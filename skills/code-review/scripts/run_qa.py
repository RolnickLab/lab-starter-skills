#!/usr/bin/env python3
"""Run a repository's QA checks for the code-review skill, stopping on the first failure.

Exit codes: 0 = checks passed, 1 = a check failed, 2 = nothing was verified.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

# --- Configuration ---
TIMEOUT_SECONDS = 300  # 5 minutes timeout for commands
VENDORED_DIRS = {"node_modules", ".venv", "venv", ".git", "build", "target"}
LINT_TARGETS = ("lint", "check", "qa")
TEST_TARGETS = ("test", "tests")
MAX_DETAIL_LINES = 20

Results = list[tuple[str, str]]  # (check name, "pass" | "fail" | "warn")

# --- Helper Functions ---


def run_cmd(cmd: str) -> tuple[str, str, int]:
    """Run a shell command; return stdout, stderr and exit code (124 on timeout)."""
    try:
        result = subprocess.run(
            cmd,
            check=False,
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {TIMEOUT_SECONDS} seconds", 124
    except OSError as e:
        return "", str(e), 1
    return result.stdout, result.stderr, result.returncode


def record_result(results: Results, name: str, status: str, details: str = "") -> None:
    """Record and print a check result; a failure prints the summary and exits."""
    results.append((name, status))
    if status == "pass":
        print(f"✅ {name} passed")
    elif status == "warn":
        print_warning(f"{name}: {details}")
    else:
        print(f"❌ {name} failed")
        lines = details.strip().splitlines()
        for line in lines[:MAX_DETAIL_LINES]:
            print(f"    {line}")
        if len(lines) > MAX_DETAIL_LINES:
            print("    ... (output truncated)")
        print_summary(results)


def print_header(title: str) -> None:
    print(f"\n{'=' * len(title)}\n{title}\n{'=' * len(title)}")


def print_step(msg: str) -> None:
    print(f"🔹 {msg}")


def print_warning(msg: str) -> None:
    print(f"⚠️ {msg}")


def print_summary(results: Results) -> NoReturn:
    """Print the result table and exit with the QA status code."""
    print_header("QA Summary")
    print(f"{'Check':<25} | {'Status':<10}")
    print("-" * 40)
    icons = {"pass": "✅ PASS", "fail": "❌ FAIL", "warn": "⚠️ WARN"}
    for name, status in results:
        print(f"{name:<25} | {icons[status]}")
    print("-" * 40)

    statuses = {status for _, status in results}
    if "fail" in statuses:
        print("🛑 Some checks failed.")
        sys.exit(1)
    if "pass" not in statuses:
        # A warning-only run (tools missing) must not read as a pass.
        print(
            "🛑 Nothing was verified: no check ran successfully. Run the tools manually."
        )
        sys.exit(2)
    print("🎉 All checks passed!")
    sys.exit(0)


# --- Project-declared checks ---


def check_pre_commit(results: Results) -> None:
    if not Path(".pre-commit-config.yaml").exists():
        return
    print_step("Found .pre-commit-config.yaml")
    out, err, rc = run_cmd("pre-commit run --all-files")
    if rc == 127:  # shell: command not found
        record_result(results, "pre-commit", "warn", "Command not found")
    else:
        record_result(results, "pre-commit", "pass" if rc == 0 else "fail", out + err)


def check_makefile(results: Results) -> bool:
    """Run the first lint-like and the first test-like Makefile target; return True if a test target ran."""
    makefile = Path("Makefile")
    if not makefile.exists():
        return False
    content = makefile.read_text(errors="ignore")

    ran_tests = False
    for group in (LINT_TARGETS, TEST_TARGETS):
        target = next(
            (t for t in group if re.search(rf"^{t}\s*:", content, re.MULTILINE)), None
        )
        if target is None:
            continue
        print_step(f"Found Makefile target: '{target}'")
        out, err, rc = run_cmd(f"make {target}")
        record_result(
            results, f"make {target}", "pass" if rc == 0 else "fail", out + err
        )
        ran_tests = ran_tests or group is TEST_TARGETS
    return ran_tests


# --- Language/Tool Handlers ---


def detect_python_prefix() -> str:
    """Return the run prefix of the project's environment manager, or "" to use the active environment."""
    managers = (
        (("pixi.toml", "pixi.lock"), "pixi"),
        (("poetry.lock",), "poetry"),
        (("uv.lock",), "uv"),
    )
    for files, tool in managers:
        if any(Path(f).exists() for f in files):
            if shutil.which(tool):
                print_step(f"Detected '{tool}' project.")
                return f"{tool} run "
            print_warning(f"Detected '{tool}' files but '{tool}' command not found.")
    return ""


def check_python(results: Results) -> bool:
    markers = ("requirements.txt", "pyproject.toml", "setup.py")
    if not (any(Path(m).exists() for m in markers) or any(Path.cwd().glob("*.py"))):
        return False

    print_header("Python QA")
    prefix = detect_python_prefix()
    available = [
        t
        for t in ("ruff", "flake8", "mypy", "pytest")
        if run_cmd(f"{prefix}{t} --version")[2] == 0
    ]
    if not available:
        record_result(
            results,
            "python tools",
            "warn",
            "No Python QA tools found. Run them manually.",
        )
        return True
    print_step(f"Found tools: {', '.join(available)}")

    linter = (
        "ruff check ."
        if "ruff" in available
        else "flake8 ."
        if "flake8" in available
        else None
    )
    if linter:
        out, err, rc = run_cmd(f"{prefix}{linter}")
        record_result(
            results, linter.split()[0], "pass" if rc == 0 else "fail", out + err
        )

    if "mypy" in available:
        out, err, rc = run_cmd(f"{prefix}mypy .")
        record_result(results, "mypy", "pass" if rc == 0 else "fail", out + err)

    if "pytest" in available:
        out, err, rc = run_cmd(f"{prefix}pytest -q")
        if rc == 5:  # pytest: no tests collected
            record_result(results, "pytest", "warn", "No tests collected")
        else:
            record_result(results, "pytest", "pass" if rc == 0 else "fail", out + err)
    return True


def check_node(results: Results) -> bool:
    package = Path("package.json")
    if not package.exists():
        return False

    print_header("Node.js QA")
    try:
        scripts = json.loads(package.read_text()).get("scripts", {})
    except (OSError, json.JSONDecodeError) as e:
        record_result(results, "package.json", "fail", str(e))
        return True

    pm = (
        "yarn"
        if Path("yarn.lock").exists()
        else "pnpm"
        if Path("pnpm-lock.yaml").exists()
        else "npm"
    )
    lint = next((s for s in ("lint", "check") if s in scripts), None)
    if lint:
        out, err, rc = run_cmd(f"{pm} run {lint}")
        record_result(results, f"{pm} {lint}", "pass" if rc == 0 else "fail", out + err)
    else:
        record_result(results, f"{pm} lint", "warn", "No lint/check script found")

    if "test" in scripts:
        out, err, rc = run_cmd(f"{pm} run test")
        record_result(results, f"{pm} test", "pass" if rc == 0 else "fail", out + err)
    return True


def check_rust(results: Results) -> bool:
    if not Path("Cargo.toml").exists():
        return False

    print_header("Rust QA")
    out, err, rc = run_cmd("cargo check")
    record_result(results, "cargo check", "pass" if rc == 0 else "fail", err)

    if shutil.which("cargo-clippy"):
        out, err, rc = run_cmd("cargo clippy -- -D warnings")
        record_result(results, "cargo clippy", "pass" if rc == 0 else "fail", err)

    out, err, rc = run_cmd("cargo test")
    record_result(results, "cargo test", "pass" if rc == 0 else "fail", out + err)
    return True


def check_go(results: Results) -> bool:
    if not Path("go.mod").exists():
        return False

    print_header("Go QA")
    out, err, rc = run_cmd("go vet ./...")
    record_result(results, "go vet", "pass" if rc == 0 else "fail", err)

    out, err, rc = run_cmd("go test ./...")
    record_result(results, "go test", "pass" if rc == 0 else "fail", out + err)
    return True


def check_cpp(results: Results) -> bool:
    # Skip vendored dirs: native Node/Python deps ship .c files
    is_cpp = any(
        not VENDORED_DIRS.intersection(f.parts)
        for ext in ("*.cpp", "*.c")
        for f in Path.cwd().rglob(ext)
    )
    if not is_cpp:
        return False

    print_header("C/C++ QA")
    if shutil.which("cppcheck"):
        print_step("Running cppcheck...")
        excludes = " ".join(f"-i {d}" for d in VENDORED_DIRS)
        _, err, rc = run_cmd(f"cppcheck . --error-exitcode=1 --quiet {excludes}")
        record_result(results, "cppcheck", "pass" if rc == 0 else "fail", err)
    else:
        record_result(results, "cppcheck", "warn", "Command not found")
    return True


def main() -> NoReturn:
    results: Results = []
    print(f"🕵️  QA Skill analyzing: {Path.cwd()}")

    check_pre_commit(results)
    ran_tests = check_makefile(results)

    # Pre-commit and lint targets rarely run tests, so the language chain runs unless a Makefile test target did.
    # ponytail: may re-run linters pre-commit already covered; split each handler into lint/test if that gets slow.
    if not ran_tests:
        handlers = (check_python, check_node, check_rust, check_go, check_cpp)
        detected = [
            handler(results) for handler in handlers
        ]  # a list, not a generator: every handler must run
        if not any(detected):
            print_warning("No recognized project structure found.")

    print_summary(results)


if __name__ == "__main__":
    main()
