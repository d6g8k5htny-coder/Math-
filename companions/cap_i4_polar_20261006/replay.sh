#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/cap_i4_polar_20261006"
OUT="$ROOT/.lake/cap-i4-polar"
test ! -e "$OUT" && test ! -L "$OUT"
mkdir -p "$OUT/build"
cd "$ROOT"
test "$(git rev-parse HEAD)" = "${GITHUB_SHA:-$(git rev-parse HEAD)}"
printf 'commit=%s\nrun=%s\nattempt=%s\n' "$(git rev-parse HEAD)" "${GITHUB_RUN_ID:-local}" "${GITHUB_RUN_ATTEMPT:-local}" > "$OUT/context.txt"
python3 -B -S "$SIDE/check_evidence.py" source | tee "$OUT/source-before.json"
for opt in normal optimized; do
  flags=(-B -S); if [[ "$opt" = optimized ]]; then flags+=(-O); fi
  python3 "${flags[@]}" "$SIDE/test_polar.py" > "$OUT/source-tests-$opt.log" 2>&1
  python3 "${flags[@]}" "$SIDE/test_evidence.py" > "$OUT/evidence-tests-$opt.log" 2>&1
done
python3 -B -S "$SIDE/check_evidence.py" emit "$OUT"
cp "$SIDE/CapI4Polar.lean" "$OUT/build/CapI4Polar.lean"
export CAP_POLAR_SIDE="$SIDE" CAP_POLAR_OUT="$OUT"
cd "$ROOT/formal"
python3 -B -S - <<'PY'
import json, subprocess
from pathlib import Path
for package in json.loads(Path('lake-manifest.json').read_text())['packages']:
    directory=Path('.lake/packages')/package['name']
    actual=subprocess.check_output(['git','-C',str(directory),'rev-parse','HEAD'],text=True).strip()
    if actual!=package['rev']: raise ValueError('dependency revision: '+package['name'])
print('All pinned dependency heads match')
PY
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$CAP_POLAR_OUT/build:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$CAP_POLAR_OUT/build:${LEAN_SRC_PATH:-}"
lean --version | tee "$CAP_POLAR_OUT/toolchain.log"
lean -DwarningAsError=true --root="$CAP_POLAR_OUT/build" -o "$CAP_POLAR_OUT/build/CapI4Polar.olean" "$CAP_POLAR_OUT/build/CapI4Polar.lean" 2>&1 | tee "$CAP_POLAR_OUT/build.log"
for pair in 'Positive positive' 'Audit axioms' 'Types types'; do
  read -r name log <<< "$pair"
  lean -DwarningAsError=true --root="$CAP_POLAR_OUT" "$CAP_POLAR_OUT/$name.lean" > "$CAP_POLAR_OUT/$log.log" 2>&1
done
leanchecker --fresh CapI4Polar 2>&1 | tee "$CAP_POLAR_OUT/leanchecker.log"
for control in RejectOrder RejectOffDiagonal; do
  status=0
  lean -DwarningAsError=true --root="$CAP_POLAR_OUT" "$CAP_POLAR_OUT/$control.lean" > "$CAP_POLAR_OUT/$control.log" 2>&1 || status=$?
  printf '%s\n' "$status" > "$CAP_POLAR_OUT/$control.status"
done
INNER
cd "$ROOT"
python3 -B -S "$SIDE/check_evidence.py" check "$OUT" | tee "$OUT/verdict.json"
python3 -B -S "$SIDE/check_evidence.py" source | tee "$OUT/source-after.json"
cmp "$OUT/source-before.json" "$OUT/source-after.json"
git diff --exit-code HEAD -- companions/cap_i4_polar_20261006 formal .github/workflows/cap-i4-polar.yml
(cd "$OUT" && sha256sum -- *.log *.json *.status *.lean context.txt > SHA256SUMS)
echo 'PASS: isolated polar sub-interface; entry-volume and concrete Gaussian model remain OPEN'
