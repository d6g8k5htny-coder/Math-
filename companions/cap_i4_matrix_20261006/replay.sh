#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/cap_i4_matrix_20261006"
PARENT="$ROOT/companions/cap_i4_polar_20261006"
OUT="$ROOT/.lake/cap-i4-matrix"
test ! -e "$OUT" && test ! -L "$OUT"
mkdir -p "$OUT/build"
cd "$ROOT"
export MATRIX_ROOT="$ROOT" MATRIX_SIDE="$SIDE" MATRIX_PARENT="$PARENT" MATRIX_OUT="$OUT"
record() {
python3 -B -S - <<'PY'
import hashlib,json,os,subprocess
from pathlib import Path
root=Path(os.environ['MATRIX_ROOT'])
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
if head != os.environ['GITHUB_SHA']: raise ValueError('tested-head mismatch')
scopes=['companions/cap_i4_matrix_20261006','companions/cap_i4_polar_20261006','formal/lean-toolchain','formal/lakefile.toml','formal/lake-manifest.json','.github/workflows/cap-i4-matrix.yml']
names=subprocess.check_output(['git','ls-files','--',*scopes],text=True).splitlines()
rows={}
for name in names:
 p=root/name
 if p.is_symlink(): raise ValueError('symlink '+name)
 data=p.read_bytes()
 if data!=subprocess.check_output(['git','show',head+':'+name]): raise ValueError('dirty source '+name)
 rows[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
for folder in scopes[:2]:
 actual={str(p.relative_to(root)) for p in (root/folder).rglob('*') if p.is_file() or p.is_symlink()}
 if actual!={p for p in names if p.startswith(folder+'/')}: raise ValueError('untracked source membership')
if rows['companions/cap_i4_polar_20261006/CapI4Polar.lean']['blob']!='9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4': raise ValueError('parent changed')
if (root/'formal/lean-toolchain').read_text().strip()!='leanprover/lean4:v4.34.1': raise ValueError('toolchain changed')
print(json.dumps({'head':head,'run':os.environ['GITHUB_RUN_ID'],'attempt':os.environ['GITHUB_RUN_ATTEMPT'],'files':rows},sort_keys=True))
PY
}
record | tee "$OUT/source-before.json"
python3 -B -S "$PARENT/check_evidence.py" source > "$OUT/parent-source.json"
cp "$PARENT/CapI4Polar.lean" "$OUT/build/CapI4Polar.lean"
if [[ -f "$SIDE/CapI4Matrix.lean" ]]; then cp "$SIDE/CapI4Matrix.lean" "$OUT/build/CapI4Matrix.lean"; fi
cp "$SIDE/Contract.lean" "$OUT/Contract.lean"
cp "$SIDE/targets.json" "$OUT/targets.json"
python3 -B -S - <<'PY'
import json,os
from pathlib import Path
out=Path(os.environ['MATRIX_OUT'])
names=json.loads((out/'targets.json').read_text())
(out/'Audit.lean').write_text('import CapI4Matrix\n'+''.join('#print axioms '+n+'\n' for n in names))
(out/'Types.lean').write_text('import CapI4Matrix\n'+''.join('#check @'+n+'\n' for n in names))
(out/'RejectBoundary.lean').write_text('import CapI4Matrix\nexample : (CapI4Matrix.entryMatrix (0, (0, 1))).PosDef := by\n  rw [CapI4Matrix.entryMatrix_posDef_iff]\n  norm_num\n')
(out/'RejectDetOnly.lean').write_text('import CapI4Matrix\nexample : 0 < (CapI4Matrix.entryMatrix (-1, (0, -1))).det → (CapI4Matrix.entryMatrix (-1, (0, -1))).PosDef := by\n  norm_num [CapI4Matrix.entryMatrix_det, CapI4Matrix.entryMatrix_posDef_iff]\n')
PY
cd "$ROOT/formal"
python3 -B -S - <<'PY' | tee "$OUT/dependencies.log"
import json,subprocess
from pathlib import Path
packages=json.loads(Path('lake-manifest.json').read_text())['packages']
for p in packages:
 actual=subprocess.check_output(['git','-C',str(Path('.lake/packages')/p['name']),'rev-parse','HEAD'],text=True).strip()
 if actual!=p['rev']: raise ValueError('dependency mismatch '+p['name'])
 if p['name']=='mathlib' and actual!='d13f23b723b8a846827a245b89c10fc7d3f11612': raise ValueError('mathlib pin')
 print(p['name'],actual)
PY
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$MATRIX_OUT/build:${LEAN_PATH:-}" LEAN_SRC_PATH="$MATRIX_OUT/build:${LEAN_SRC_PATH:-}"
run_logged() {
 local tag="$1"; shift
 local status=0
 "$@" > "$MATRIX_OUT/$tag.log" 2>&1 || status=$?
 printf '%s\n' "$status" > "$MATRIX_OUT/$tag.status"
 cat "$MATRIX_OUT/$tag.log"
 test "$status" -eq 0
}
run_logged toolchain lean --version
run_logged parent-build lean -DwarningAsError=true --root="$MATRIX_OUT/build" -o "$MATRIX_OUT/build/CapI4Polar.olean" "$MATRIX_OUT/build/CapI4Polar.lean"
if [[ -f "$MATRIX_OUT/build/CapI4Matrix.lean" ]]; then
 run_logged child-build lean -DwarningAsError=true --root="$MATRIX_OUT/build" -o "$MATRIX_OUT/build/CapI4Matrix.olean" "$MATRIX_OUT/build/CapI4Matrix.lean"
fi
for item in Contract Audit Types; do
 run_logged "$item" lean -DwarningAsError=true --root="$MATRIX_OUT" "$MATRIX_OUT/$item.lean"
done
run_logged leanchecker leanchecker --fresh CapI4Matrix
for item in RejectBoundary RejectDetOnly; do
 status=0
 lean -DwarningAsError=true --root="$MATRIX_OUT" "$MATRIX_OUT/$item.lean" > "$MATRIX_OUT/$item.log" 2>&1 || status=$?
 printf '%s\n' "$status" > "$MATRIX_OUT/$item.status"
 test "$status" -eq 1
done
INNER
cd "$ROOT"
python3 -B -S - <<'PY' | tee "$OUT/parser-check.log"
import importlib.util,json,os,re
from pathlib import Path
parent=Path(os.environ['MATRIX_PARENT']);out=Path(os.environ['MATRIX_OUT'])
spec=importlib.util.spec_from_file_location('parent_checks',parent/'check_evidence.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
names=json.loads((out/'targets.json').read_text())
m.audit_axioms((out/'Audit.log').read_text(),names)
text=(out/'Types.log').read_text()
if re.findall(r'^@?(CapI4Matrix\.\w+)\s*:',text,re.M)!=names or re.search(r'\b(error|warning):',text): raise ValueError('type inventory or diagnostics')
for item in ['toolchain','parent-build','child-build','Contract','Audit','Types','leanchecker']:
 if (out/(item+'.status')).read_text()!='0\n': raise ValueError('nonzero required command '+item)
for item in ['RejectBoundary','RejectDetOnly']:
 m.audit_negative((out/(item+'.log')).read_text(),int((out/(item+'.status')).read_text()))
print('PASS: 12 declaration inventories; two exact cone-boundary rejections')
PY
python3 -B -S "$SIDE/test_matrix.py" -v > "$OUT/tests-normal.log" 2>&1
cat "$OUT/tests-normal.log"
python3 -B -S -O "$SIDE/test_matrix.py" -v > "$OUT/tests-optimized.log" 2>&1
cat "$OUT/tests-optimized.log"
record | tee "$OUT/source-after.json"
cmp "$OUT/source-before.json" "$OUT/source-after.json"
(cd "$OUT" && sha256sum -- *.json *.log *.lean *.status build/*.lean build/*.olean > SHA256SUMS)
echo 'PASS: matrix-cone identification only; matrix-volume and concrete Gaussian inputs remain separate'
