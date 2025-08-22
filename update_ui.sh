#!/usr/bin/env bash
set -euo pipefail

# === Config ===
WORKSPACE="${WORKSPACE:-$(pwd)}"
SRC_DIR="${SRC_DIR:-"$WORKSPACE/src"}"

# === Compiler detection ===
choose_compiler() {
  if command -v pyuic5 >/dev/null 2>&1; then
    echo "pyuic5"
    return 0
  fi
  if command -v python >/dev/null 2>&1; then
    if python - <<'PYCHK' >/dev/null 2>&1
import importlib, sys
m = importlib.import_module("PyQt5.uic.pyuic")
PYCHK
    then
      echo "python -m PyQt5.uic.pyuic"
      return 0
    fi
  fi
  return 1
}

if ! COMPILER=$(choose_compiler); then
  printf '[ERROR] PyQt5 UI compiler not found: need "pyuic5" or "python -m PyQt5.uic.pyuic"\n' >&2
  exit 127
fi

printf '[INFO] Workspace: %s\n' "$WORKSPACE"
printf '[INFO] Source dir: %s\n' "$SRC_DIR"
printf '[INFO] Compiler : %s\n' "$COMPILER"

if [[ ! -d "$SRC_DIR" ]]; then
  printf '[ERROR] Source directory not found.\n' >&2
  exit 2
fi

# === Counters ===
total=0
compiled=0
skipped=0
failed=0

start_ts=$(date +%s)

# === Walk & build ===
find "$SRC_DIR" -type f -name '*.ui' -print0 | \
while IFS= read -r -d '' ui; do
  total=$((total + 1))
  dir=$(dirname "$ui")
  base=$(basename "$ui" .ui)
  out="$dir/${base}_ui.py"

  # Decide whether to compile
  if [[ ! -f "$out" || "$ui" -nt "$out" ]]; then
    printf '[BUILD] %s → %s ... ' "$ui" "$out"
    if $COMPILER "$ui" -o "$out" >/dev/null 2>&1; then
      printf 'OK\n'
      compiled=$((compiled + 1))
    else
      printf 'FAIL\n' >&2
      failed=$((failed + 1))
    fi
  else
    printf '[SKIP ] %s (up-to-date)\n' "$ui"
    skipped=$((skipped + 1))
  fi
done

end_ts=$(date +%s)
elapsed=$((end_ts - start_ts))

printf '\n[SUMMARY] total=%d compiled=%d skipped=%d failed=%d elapsed=%ss\n' \
  "$total" "$compiled" "$skipped" "$failed" "$elapsed"

# Exit code reflects failure count
if (( failed > 0 )); then
  exit 1
fi
exit 0
