#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/cap_i4_angular_20261006"
PARENT="$ROOT/companions/cap_i4_polar_20261006"
OUT="$ROOT/.lake/cap-i4-angular"
test ! -e "$OUT" && test ! -L "$OUT"
mkdir -p "$OUT/build"
cd "$ROOT"
export ANGULAR_ROOT="$ROOT" ANGULAR_SIDE="$SIDE" ANGULAR_PARENT="$PARENT" ANGULAR_OUT="$OUT"
record() {
python3 -B -S - <<'PY'
import hashlib,json,os,subprocess
from pathlib import Path
root=Path(os.environ['ANGULAR_ROOT'])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if head != os.environ['GITHUB_SHA']: raise ValueError('tested-head mismatch')
scopes=['companions/cap_i4_angular_20261006','companions/cap_i4_polar_20261006','formal/lean-toolchain','formal/lakefile.toml','formal/lake-manifest.json','.github/workflows/cap-i4-angular.yml']
subprocess.run(['git','diff','--exit-code','HEAD','--',*scopes],check=True)
names=subprocess.check_output(['git','ls-files','--',*scopes],text=True).splitlines()
rows={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in names}
parent='companions/cap_i4_polar_20261006/CapI4Polar.lean'
if subprocess.check_output(['git','hash-object',parent],text=True).strip()!='9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4': raise ValueError('parent changed')
print(json.dumps({'head':head,'run':os.environ['GITHUB_RUN_ID'],'attempt':os.environ['GITHUB_RUN_ATTEMPT'],'files':rows},sort_keys=True))
PY
}
record | tee "$OUT/source-before.json"
cp "$PARENT/CapI4Polar.lean" "$OUT/build/CapI4Polar.lean"
if [[ -f "$SIDE/CapI4Angular.lean" ]]; then cp "$SIDE/CapI4Angular.lean" "$OUT/build/CapI4Angular.lean"; fi
cp "$SIDE/Contract.lean" "$OUT/Contract.lean"
python3 -B -S - <<'PY'
import os
from pathlib import Path
out=Path(os.environ['ANGULAR_OUT'])
names=['CapI4Angular.angle_lintegral','CapI4Angular.polar_spectral_radial','CapI4Angular.density_radial_bound']
(out/'Audit.lean').write_text('import CapI4Angular\n'+''.join('#print axioms '+n+'\n' for n in names))
(out/'Types.lean').write_text('import CapI4Angular\n'+''.join('#check @'+n+'\n' for n in names))
(out/'RejectFactor.lean').write_text('import CapI4Angular\nexample : (2 : ENNReal) = 1 := by norm_num\n')
PY
cd "$ROOT/formal"
python3 -B -S - <<'PY' | tee "$OUT/dependencies.log"
import json,subprocess
from pathlib import Path
for p in json.loads(Path('lake-manifest.json').read_text())['packages']:
 actual=subprocess.check_output(['git','-C',str(Path('.lake/packages')/p['name']),'rev-parse','HEAD'],text=True).strip()
 if actual!=p['rev']: raise ValueError('dependency mismatch '+p['name'])
 print(p['name'],actual)
PY
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$ANGULAR_OUT/build:${LEAN_PATH:-}" LEAN_SRC_PATH="$ANGULAR_OUT/build:${LEAN_SRC_PATH:-}"
lean --version | tee "$ANGULAR_OUT/toolchain.log"
lean -DwarningAsError=true --root="$ANGULAR_OUT/build" -o "$ANGULAR_OUT/build/CapI4Polar.olean" "$ANGULAR_OUT/build/CapI4Polar.lean" 2>&1 | tee "$ANGULAR_OUT/parent-build.log"
if [[ -f "$ANGULAR_OUT/build/CapI4Angular.lean" ]]; then
 lean -DwarningAsError=true --root="$ANGULAR_OUT/build" -o "$ANGULAR_OUT/build/CapI4Angular.olean" "$ANGULAR_OUT/build/CapI4Angular.lean" 2>&1 | tee "$ANGULAR_OUT/child-build.log"
fi
for item in Contract Audit Types; do
 lean -DwarningAsError=true --root="$ANGULAR_OUT" "$ANGULAR_OUT/$item.lean" 2>&1 | tee "$ANGULAR_OUT/$item.log"
done
leanchecker --fresh CapI4Angular 2>&1 | tee "$ANGULAR_OUT/leanchecker.log"
status=0
lean -DwarningAsError=true --root="$ANGULAR_OUT" "$ANGULAR_OUT/RejectFactor.lean" > "$ANGULAR_OUT/RejectFactor.log" 2>&1 || status=$?
printf '%s\n' "$status" > "$ANGULAR_OUT/RejectFactor.status"
INNER
cd "$ROOT"
python3 -B -S - <<'PY' | tee "$OUT/parser-check.log"
import importlib.util,os,re
from pathlib import Path
parent=Path(os.environ['ANGULAR_PARENT']);out=Path(os.environ['ANGULAR_OUT'])
spec=importlib.util.spec_from_file_location('parent_checks',parent/'check_evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
names=['CapI4Angular.angle_lintegral','CapI4Angular.polar_spectral_radial','CapI4Angular.density_radial_bound']
m.audit_axioms((out/'Audit.log').read_text(),names)
text=(out/'Types.log').read_text()
if re.findall(r'^@?(CapI4Angular\.\w+)\s*:',text,re.M)!=names or re.search(r'\b(error|warning):',text): raise ValueError('type inventory or diagnostics')
m.audit_negative((out/'RejectFactor.log').read_text(),int((out/'RejectFactor.status').read_text()))
print('PASS: 3 axiom/type inventories; intended arithmetic negative rejection')
PY
record | tee "$OUT/source-after.json"
cmp "$OUT/source-before.json" "$OUT/source-after.json"
(cd "$OUT" && sha256sum -- *.json *.log *.lean *.status > SHA256SUMS)
echo 'PASS: angular sub-bridge only; entry-volume and actual Gaussian transport remain OPEN'
