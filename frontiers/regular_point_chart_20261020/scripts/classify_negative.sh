#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 2 ]]; then
  echo "usage: $0 LOG EXIT_STATUS" >&2
  exit 2
fi

log="$1"
status="$2"

[[ "$status" =~ ^[0-9]+$ ]] || {
  echo "negative classifier: invalid exit status" >&2
  exit 2
}

if [[ "$status" -eq 0 ]]; then
  echo "negative classifier: fixture unexpectedly succeeded" >&2
  exit 1
fi

if [[ "$status" -eq 124 || "$status" -eq 137 || "$status" -eq 143 ]]; then
  echo "negative classifier: rejected timeout/termination exit status" >&2
  exit 1
fi

if grep -Eiq \
  'unknown (module|package|identifier)|invalid import|failed to (resolve|load|fetch|clone|download)|cannot find|no such file|file not found|command not found|fatal: unable to access|could not resolve host|HTTP[^[:alnum:]]*(403|404|5[0-9][0-9])|parser error|syntax error|invalid syntax|unexpected (token|identifier|end)|expected token|timed? ?out|timeout|killed|out of memory|oom|memory exhausted|resource temporarily unavailable|no space left|signal 9|exit code 137' \
  "$log"; then
  echo "negative classifier: rejected setup/syntax/resource failure" >&2
  exit 1
fi

grep -Eq 'WithoutNoncriticality\.lean:[0-9]+:[0-9]+: error: Type mismatch' "$log"
grep -Eq '¬[[:space:]]*IsCriticalPoint' "$log"
grep -Fq '→ OpenPartialHomeomorph' "$log"

echo "negative classifier: intended missing-noncriticality type mismatch"
