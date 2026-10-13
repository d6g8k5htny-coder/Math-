#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/d2_moment_bridge_20261006"
OUT="$ROOT/.lake/d2-moment-evidence"
cd "$ROOT"
test ! -e "$OUT"
mkdir -p "$OUT"
python3 -B -S "$SIDE/check.py" source | tee "$OUT/source.json"
python3 -B -S "$SIDE/test_bridge.py" 2>&1 | tee "$OUT/tests.log"
python3 -B -O -S "$SIDE/test_bridge.py" 2>&1 | tee "$OUT/tests-optimized.log"
python3 -B -S -m unittest discover -s formal/tests -v 2>&1 | tee "$OUT/core-tests.log"
python3 -B -O -S -m unittest discover -s formal/tests -v 2>&1 | tee "$OUT/core-tests-optimized.log"
python3 -B -S formal/gate.py --execute 2>&1 | tee "$OUT/core-execute.log"
python3 -B -S "$SIDE/check.py" emit "$OUT"
export MOMENT_SIDE="$SIDE" MOMENT_OUT="$OUT"
cd "$ROOT/formal"
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$MOMENT_SIDE:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$MOMENT_SIDE:${LEAN_SRC_PATH:-}"
lean --version | tee "$MOMENT_OUT/toolchain.log"
run_lean() {
  local label="$1"; shift
  local code=0
  "$@" >"$MOMENT_OUT/$label.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$MOMENT_OUT/$label.status"
  cat "$MOMENT_OUT/$label.log"
  test "$code" -eq 0
}
run_lean build lean -DwarningAsError=true --root="$MOMENT_SIDE" -o "$MOMENT_SIDE/D2MomentBridge.olean" "$MOMENT_SIDE/D2MomentBridge.lean"
run_lean positive lean -DwarningAsError=true --root="$MOMENT_OUT" "$MOMENT_OUT/Positive.lean"
run_lean axioms lean -DwarningAsError=true --root="$MOMENT_OUT" "$MOMENT_OUT/Audit.lean"
run_lean types lean -DwarningAsError=true --root="$MOMENT_OUT" "$MOMENT_OUT/Types.lean"
run_lean leanchecker leanchecker --fresh D2MomentBridge
for control in RejectZeroAtom RejectSameRadius; do
  code=0
  lean -DwarningAsError=true --root="$MOMENT_OUT" "$MOMENT_OUT/$control.lean" >"$MOMENT_OUT/$control.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$MOMENT_OUT/$control.status"
  python3 -B -S "$MOMENT_SIDE/check.py" negative "$MOMENT_OUT/$control.log" --control "$control" --status "$code"
done
INNER
cd "$ROOT"
python3 -B -S "$SIDE/check.py" finish "$OUT"
echo 'PASS: actual-law D2 companion; concrete periodic law and scientific acceptance remain unproved here.'
