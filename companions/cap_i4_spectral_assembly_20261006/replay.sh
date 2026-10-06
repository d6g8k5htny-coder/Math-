#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SIDE="$ROOT/companions/cap_i4_spectral_assembly_20261006"
OUT="$ROOT/.lake/cap-i4-spectral-assembly"
test ! -e "$OUT" && test ! -L "$OUT"
mkdir -p "$OUT/build"
cd "$ROOT"

source_record() {
python3 -B -S - <<'PY'
import hashlib,json,os,subprocess
from pathlib import Path
root=Path.cwd()
pins={
 'companions/cap_i4_polar_20261006/CapI4Polar.lean':'9d0bdbfb5ad77c159fe623cf2dcad31cc9402ba4',
 'companions/cap_i4_linear_20261006/CapI4Linear.lean':'3c571603f2aabae49144cdba4bc52cd94a6f4d82',
 'companions/cap_i4_angular_20261006/CapI4Angular.lean':'fab5589a93a2b700cabac5e2617360cf99cba688',
 'companions/cap_i4_entry_volume_20261006/CapI4EntryVolume.lean':'46621995dd93120a6d0456b4d0f0f9fa8a849abd',
 'formal/lean-toolchain':'ba8ebf2dbaf6a668cd2a0e086186d6d569b69ff5',
 'formal/lakefile.toml':'8117eae1b2897b7d95f5b2c42e8cf15222a1c5e8',
 'formal/lake-manifest.json':'d482b5f1e038b90397e239d2c0af82792cb0bd09'}
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
for p,b in pins.items():
    if Path(p).is_symlink() or git('hash-object',p)!=b:
        raise ValueError('pinned source mismatch: '+p)
head=git('rev-parse','HEAD')
if head!=os.environ.get('GITHUB_SHA',head): raise ValueError('tested head mismatch')
paths=[*pins,'companions/cap_i4_spectral_assembly_20261006',
       '.github/workflows/cap-i4-spectral-assembly.yml']
tracked=git('ls-files',*paths).splitlines()
if git('diff','--name-only','HEAD','--',*tracked): raise ValueError('dirty source')
for row in json.loads(Path('formal/lake-manifest.json').read_text())['packages']:
    got=git('-C',str(root/'formal/.lake/packages'/row['name']),'rev-parse','HEAD')
    if got!=row['rev']: raise ValueError('dependency head: '+row['name'])
files={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in tracked}
print(json.dumps({'head':head,'run':os.environ.get('GITHUB_RUN_ID','local'),
 'attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local'),'files':files},sort_keys=True))
PY
}

source_record | tee "$OUT/before.json"
for m in cap_i4_polar_20261006/CapI4Polar cap_i4_linear_20261006/CapI4Linear cap_i4_angular_20261006/CapI4Angular cap_i4_entry_volume_20261006/CapI4EntryVolume; do
  cp "companions/$m.lean" "$OUT/build/"
done
cp "$SIDE/Contract.lean" "$OUT/"
if [[ -f "$SIDE/CapI4SpectralAssembly.lean" ]]; then cp "$SIDE/CapI4SpectralAssembly.lean" "$OUT/build/"; fi

cd "$ROOT/formal"
export ASSEMBLY_OUT="$OUT"
lake env bash <<'INNER'
set -euo pipefail
export LEAN_PATH="$ASSEMBLY_OUT/build:${LEAN_PATH:-}"
export LEAN_SRC_PATH="$ASSEMBLY_OUT/build:${LEAN_SRC_PATH:-}"
run() {
  local name="$1"; shift
  local status=0
  timeout 1200 "$@" > "$ASSEMBLY_OUT/$name.log" 2>&1 || status=$?
  printf '%s\n' "$status" > "$ASSEMBLY_OUT/$name.status"
  cat "$ASSEMBLY_OUT/$name.log"
  test "$status" -eq 0
}
run toolchain lean --version
for m in CapI4Polar CapI4Linear CapI4Angular CapI4EntryVolume CapI4SpectralAssembly; do
  if [[ -f "$ASSEMBLY_OUT/build/$m.lean" ]]; then run "$m" lean -DwarningAsError=true --root="$ASSEMBLY_OUT/build" -o "$ASSEMBLY_OUT/build/$m.olean" "$ASSEMBLY_OUT/build/$m.lean"; fi
done
run contract lean -DwarningAsError=true --root="$ASSEMBLY_OUT" "$ASSEMBLY_OUT/Contract.lean"
INNER
cd "$ROOT"
source_record | tee "$OUT/after.json"
cmp "$OUT/before.json" "$OUT/after.json"
