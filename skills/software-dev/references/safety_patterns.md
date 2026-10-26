# Bash Safety & Defensive Coding Patterns

Shell scripting is powerful but inherently fragile. This guide details patterns to prevent catastrophic failures.

## 1. The Safety Preamble (Strict Mode)

Every script MUST start with:
```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'
	'
```

### Breakdown
*   `set -e` (**E**rrexit): The script exits immediately if any command returns a non-zero exit code.
    *   *Exception:* Commands in `if`, `while`, or `||` constructs are allowed to fail.
*   `set -u` (**U**nset): Accessing an uninitialized variable causes an error. Prevents `rm -rf $DIR/` where `$DIR` is empty from becoming `rm -rf /`.
*   `set -o pipefail`: In a pipeline `cmd1 | cmd2 | cmd3`, the exit code is the code of the *last* command to fail (or 0 if all succeed). Default Bash behavior is to return the code of `cmd3`, hiding errors in `cmd1`.
*   `IFS=$'
	'`: Sets the Internal Field Separator to newline and tab. Prevents iterating over spaces in filenames (e.g., "My File.txt" is treated as one item, not two).

## 2. Robust File Handling

### Iterating Files
❌ **BAD:**
```bash
for f in $(ls *.txt); do # Breaks on spaces/newlines
  echo $f
done
```

✅ **GOOD:**
```bash
# Glob expansion is safe
for f in *.txt; do
  [[ -e "$f" ]] || break # Handle case where no files match
  echo "$f"
done
```

### Temporary Files
Never guess filenames (`/tmp/myscript.tmp`). Use `mktemp` and `trap` for cleanup.

```bash
# Create a temp directory
WORK_DIR=$(mktemp -d)

# Function to run on exit (even on error)
cleanup() {
  rm -rf "$WORK_DIR"
}
# Register cleanup
trap cleanup EXIT

# Do work
echo "data" > "$WORK_DIR/data.txt"
```

## 3. Variable Expansion & Safety

### Default Values
If a variable might be optional, use default expansion.

```bash
# Assign "default_value" if NAME is unset or empty
NAME="${1:-default_value}"

# Assign "default_value" if NAME is unset (but allow empty)
NAME="${1-default_value}"

# Error and exit if REQUIRED_VAR is unset
: "${REQUIRED_VAR:?Variable is required}"
```

### Command Substitution
Use `$()` instead of backticks `` ` ` ``. Backticks cannot be nested easily.

```bash
# Nested substitution
DATE_DIR=$(date +%F_$(uname -s))
```

## 4. Logging & Feedback

Standardize output to `stderr` for logs, keeping `stdout` clean for piping.

```bash
log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')] $*" >&2
}

error() {
    log "ERROR: $*"
    exit 1
}

# Usage
log "Starting backup..."
cp src dst || error "Backup failed!"
```

## 5. Input Validation

Always validate arguments.

```bash
usage() {
    echo "Usage: $0 <input_file> <output_dir>"
    exit 1
}

if [[ $# -lt 2 ]]; then
    usage
fi

INPUT_FILE="$1"
OUTPUT_DIR="$2"

if [[ ! -f "$INPUT_FILE" ]]; then
    error "Input file not found: $INPUT_FILE"
fi

if [[ ! -d "$OUTPUT_DIR" ]]; then
    log "Creating directory: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"
fi
```
