#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/cap_i4_entry_volume_20261006"
OUT="$ROOT/.lake/cap-i4-entry-volume"
test ! -e "$OUT" && test ! -L "$OUT"
mkdir -p "$OUT/build"
cd "$ROOT"
export ENTRY_SIDE="$SIDE" ENTRY_OUT="$OUT"
source_record() {
python3 -B -S - <<'PY'
import hashlib,json,os,subprocess
from pathlib import Path
root=Path.cwd()
side=Path('companions/cap_i4_entry_volume_20261006')
def git(*args): return subprocess.check_output(['git',*args],text=True).strip()
pins={
 'companions/cap_i4_polar_20261006/CapI4Polar.lean':'9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4',
 'companions/cap_i4_linear_20261006/CapI4Linear.lean':'3c571603f2aabae49144cdba4bc52cd94a6f4d82',
 'companions/cap_i4_linear_20261006/replay.py':'01ccc2ef0c0af691a89d5836346a8d87535e4b2d',
 'formal/lean-toolchain':'ba8ebf2dbaf6a668cd2a0e086186d6d569b69ff5',
 'formal/lakefile.toml':'8117eae1b2897b7d95f5b2c42e8cf15222a1c5e8',
 'formal/lake-manifest.json':'d482b5f1e038b90397e239d2c0af82792cb0bd09',
 'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md':'dfed3b8d318a3ab1950957f393307733a4bef3f2',
 'imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md':'213594d6ca6a86fb938110f4d166d9ce275a02d0'}
for p,b in pins.items():
 if Path(p).is_symlink() or git('hash-object',p)!=b: raise ValueError('pinned source: '+p)
tracked=git('ls-files',str(side),'.github/workflows/cap-i4-entry-volume.yml',*pins).splitlines()
allowed={'Contract.lean','README.md','replay.sh','CapI4EntryVolume.lean'}
if not {p.name for p in side.iterdir()}<=allowed: raise ValueError('unexpected child member')
if git('diff','--name-only','HEAD','--',*tracked): raise ValueError('dirty source')
for row in json.loads(Path('formal/lake-manifest.json').read_text())['packages']:
 if git('-C',str(root/'formal/.lake/packages'/row['name']),'rev-parse','HEAD')!=row['rev']:
  raise ValueError('dependency head: '+row['name'])
head=git('rev-parse','HEAD')
if head!=os.environ.get('GITHUB_SHA',head): raise ValueError('tested SHA mismatch')
files={}
for p in tracked:
 q=Path(p)
 if not q.is_file() or q.is_symlink(): raise ValueError('nonregular source')
 files[p]=hashlib.sha256(q.read_bytes()).hexdigest()
print(json.dumps({'head':head,'run':os.environ.get('GITHUB_RUN_ID','local'),
 'attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local'),'files':files},sort_keys=True))
PY
}
source_record | tee "$OUT/before.json"
cp companions/cap_i4_polar_20261006/CapI4Polar.lean "$OUT/build/"
cp companions/cap_i4_linear_20261006/CapI4Linear.lean "$OUT/build/"
cp "$SIDE/Contract.lean" "$OUT/"
if [[ -f "$SIDE/CapI4EntryVolume.lean" ]]; then cp "$SIDE/CapI4EntryVolume.lean" "$OUT/build/"; fi
cd "$ROOT/formal"
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$ENTRY_OUT/build:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$ENTRY_OUT/build:${LEAN_SRC_PATH:-}"
run_step() {
  local name="$1"; shift
  local status=0
  timeout 1200 "$@" > "$ENTRY_OUT/$name.log" 2>&1 || status=$?
  printf '%s\n' "$status" > "$ENTRY_OUT/$name.status"
  cat "$ENTRY_OUT/$name.log"
  test "$status" -eq 0
}
run_step toolchain lean --version
for module in CapI4Polar CapI4Linear CapI4EntryVolume; do
 if [[ -f "$ENTRY_OUT/build/$module.lean" ]]; then
  run_step "$module" lean -DwarningAsError=true --root="$ENTRY_OUT/build" -o "$ENTRY_OUT/build/$module.olean" "$ENTRY_OUT/build/$module.lean"
 fi
done
run_step contract lean -DwarningAsError=true --root="$ENTRY_OUT" "$ENTRY_OUT/Contract.lean"
python3 -B -S - <<'PY'
import os
from pathlib import Path
out=Path(os.environ['ENTRY_OUT'])
names=['measurable_traceCoordinates','entry_reorder_lintegral','traceCoordinates_lintegral']
(out/'Audit.lean').write_text('import CapI4EntryVolume\n'+''.join('#print axioms CapI4EntryVolume.'+n+'\n' for n in names))
(out/'Types.lean').write_text('import CapI4EntryVolume\n'+''.join('#check @CapI4EntryVolume.'+n+'\n' for n in names))
(out/'Reject.lean').write_text('import CapI4EntryVolume\nexample : (CapI4Polar.traceCoordinates (0, (1, 0))).2.2 = 0 := by\n  norm_num [CapI4Polar.traceCoordinates]\n')
PY
run_step axioms lean -DwarningAsError=true --root="$ENTRY_OUT" "$ENTRY_OUT/Audit.lean"
run_step types lean -DwarningAsError=true --root="$ENTRY_OUT" "$ENTRY_OUT/Types.lean"
run_step leanchecker leanchecker --fresh CapI4EntryVolume
status=0
lean -DwarningAsError=true --root="$ENTRY_OUT" "$ENTRY_OUT/Reject.lean" > "$ENTRY_OUT/reject.log" 2>&1 || status=$?
printf '%s\n' "$status" > "$ENTRY_OUT/reject.status"
INNER
cd "$ROOT"
python3 -B -S - <<'PY'
import importlib.util,json,os,re
from pathlib import Path
out=Path(os.environ['ENTRY_OUT'])
path=Path('companions/cap_i4_linear_20261006/replay.py')
spec=importlib.util.spec_from_file_location('parent_replay',path)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
names=['CapI4EntryVolume.'+n for n in ['measurable_traceCoordinates','entry_reorder_lintegral','traceCoordinates_lintegral']]
m.axioms((out/'axioms.log').read_text(),names)
types=(out/'types.log').read_text()
if re.findall(r'^@?(CapI4EntryVolume\.\w+)\s*:',types,re.M)!=names or re.search(r'\b(error|warning):',types):
 raise ValueError('elaborated type inventory/diagnostic mismatch')
m.negative((out/'reject.log').read_text(),int((out/'reject.status').read_text()))
for label in ['toolchain','CapI4Polar','CapI4Linear','CapI4EntryVolume','contract','axioms','types','leanchecker']:
 if (out/(label+'.status')).read_text()!='0\n': raise ValueError('nonzero or absent status: '+label)
print(json.dumps({'checked_theorems':3,'scope':'entry-volume lift; Gaussian realization OPEN'},sort_keys=True))
PY
source_record | tee "$OUT/after.json"
cmp "$OUT/before.json" "$OUT/after.json"
(cd "$OUT" && sha256sum -- *.log *.json *.status *.lean > SHA256SUMS)
echo 'PASS: source-bound three-entry volume lift only'
