#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/cap_i4_source_bridge_20261005"
OUT="$ROOT/.lake/cap-i4-evidence"
mkdir -p "$OUT"
cd "$ROOT"
printf 'commit=%s\nrun_id=%s\nrun_attempt=%s\n' "$(git rev-parse HEAD)" "${GITHUB_RUN_ID:-local}" "${GITHUB_RUN_ATTEMPT:-local}" > "$OUT/execution-context.txt"
python3 "$SIDE/gate.py" self-test 2>&1 | tee "$OUT/self-tests.log"
python3 -O "$SIDE/gate.py" self-test 2>&1 | tee "$OUT/self-tests-optimized.log"
python3 "$SIDE/gate.py" source | tee "$OUT/source.json"
python3 -m unittest discover -s formal/tests -v 2>&1 | tee "$OUT/core-tests.log"
python3 -O -m unittest discover -s formal/tests -v 2>&1 | tee "$OUT/core-tests-optimized.log"
python3 formal/gate.py 2>&1 | tee "$OUT/core-source.log"
(cd formal && lake exe cache get)
python3 formal/gate.py --execute 2>&1 | tee "$OUT/core-execute.log"
python3 "$SIDE/gate.py" emit "$OUT"
export CAP_I4_SIDE="$SIDE" CAP_I4_OUT="$OUT"
cd "$ROOT/formal"
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$CAP_I4_SIDE:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$CAP_I4_SIDE:${LEAN_SRC_PATH:-}"
lean --version | tee "$CAP_I4_OUT/toolchain.log"
lean -DwarningAsError=true --root="$CAP_I4_SIDE" -o "$CAP_I4_SIDE/CapI4.olean" "$CAP_I4_SIDE/CapI4.lean" 2>&1 | tee "$CAP_I4_OUT/build.log"
lean -DwarningAsError=true --root="$CAP_I4_OUT" "$CAP_I4_OUT/Positive.lean" 2>&1 | tee "$CAP_I4_OUT/positive.log"
lean -DwarningAsError=true --root="$CAP_I4_OUT" "$CAP_I4_OUT/Audit.lean" 2>&1 | tee "$CAP_I4_OUT/axioms.log"
python3 "$CAP_I4_SIDE/gate.py" audit "$CAP_I4_OUT/axioms.log" | tee "$CAP_I4_OUT/axiom-audit.json"
lean -DwarningAsError=true --root="$CAP_I4_OUT" "$CAP_I4_OUT/Types.lean" 2>&1 | tee "$CAP_I4_OUT/elaborated-types.log"
python3 "$CAP_I4_SIDE/gate.py" types "$CAP_I4_OUT/elaborated-types.log" | tee "$CAP_I4_OUT/type-inventory.json"
leanchecker --fresh CapI4 2>&1 | tee "$CAP_I4_OUT/leanchecker.log"
for control in RejectDroppedSoft RejectDroppedFar; do
  status=0
  lean -DwarningAsError=true --root="$CAP_I4_OUT" "$CAP_I4_OUT/$control.lean" >"$CAP_I4_OUT/$control.log" 2>&1 || status=$?
  python3 "$CAP_I4_SIDE/gate.py" negative "$CAP_I4_OUT/$control.log" --control "$control" --status "$status"
done | tee "$CAP_I4_OUT/negative-controls.log"
INNER
cd "$ROOT"
python3 "$SIDE/gate.py" source | tee "$OUT/final-source.json"
(cd "$OUT" && sha256sum -- *.log *.json *.lean execution-context.txt > SHA256SUMS)
echo 'PASS: Cap I4 companion replay; matrix transport remains OPEN; scientific effect NONE.'
