#!/usr/bin/env bash
# Derived from #317 replay.sh, blob 85c0de87; no live tee/hash race.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/d2_square_schur_20261006"
OUT="$ROOT/.lake/d2-square-schur-evidence"
cd "$ROOT"
test ! -e "$OUT"
mkdir -p "$OUT"
python3 -B -S "$SIDE/check.py" source > "$OUT/source.json"
python3 -B -S "$SIDE/test_check.py" 2>&1 | tee "$OUT/tests.log"
python3 -B -O -S "$SIDE/test_check.py" 2>&1 | tee "$OUT/tests-optimized.log"
python3 -B -S -m unittest discover -s tests -v 2>&1 | tee "$OUT/repository-tests.log"
python3 -B -O -S -m unittest discover -s tests -v 2>&1 | tee "$OUT/repository-tests-optimized.log"
python3 -B -S -m unittest discover -s formal/tests -v 2>&1 | tee "$OUT/core-tests.log"
python3 -B -O -S -m unittest discover -s formal/tests -v 2>&1 | tee "$OUT/core-tests-optimized.log"
python3 -B -S formal/gate.py --execute 2>&1 | tee "$OUT/core-execute.log"
python3 -B -S "$SIDE/check.py" emit "$OUT"
export SQUARE_SIDE="$SIDE" SQUARE_OUT="$OUT"
cd "$ROOT/formal"
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$SQUARE_SIDE:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$SQUARE_SIDE:${LEAN_SRC_PATH:-}"
lean --version | tee "$SQUARE_OUT/toolchain.log"
run_lean() {
  local label="$1"; shift
  local code=0
  "$@" >"$SQUARE_OUT/$label.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$SQUARE_OUT/$label.status"
  cat "$SQUARE_OUT/$label.log"
  test "$code" -eq 0
}
run_lean build lean -DwarningAsError=true --root="$SQUARE_SIDE" -o "$SQUARE_SIDE/D2SquareSchur.olean" "$SQUARE_SIDE/D2SquareSchur.lean"
run_lean contract lean -DwarningAsError=true --root="$SQUARE_SIDE" "$SQUARE_SIDE/Contract.lean"
run_lean axioms lean -DwarningAsError=true --root="$SQUARE_OUT" "$SQUARE_OUT/Audit.lean"
run_lean types lean -DwarningAsError=true --root="$SQUARE_OUT" "$SQUARE_OUT/Types.lean"
run_lean leanchecker leanchecker --fresh D2SquareSchur
for control in RejectSignedWeights RejectEndpointMaximum RejectOutsideDirection; do
  code=0
  lean -DwarningAsError=true --root="$SQUARE_OUT" "$SQUARE_OUT/$control.lean" >"$SQUARE_OUT/$control.log" 2>&1 || code=$?
  printf '%s\n' "$code" >"$SQUARE_OUT/$control.status"
  python3 -B -S "$SQUARE_SIDE/check.py" negative "$SQUARE_OUT/$control.log" --control "$control" --status "$code"
done
INNER
cd "$ROOT"
python3 -B -S "$SIDE/check.py" finish "$OUT"
echo 'PASS: four scalar targets only; model/atom-integral/independent-alignment obligations remain.'
