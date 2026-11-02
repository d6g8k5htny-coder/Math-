from pathlib import Path
import datetime, hashlib, json, subprocess, time
root = Path('/workspace/scratch/fold-two-pin-bounds')
ns = sorted((root/'runs').glob('run-*'))
n = len(ns)+1
out = root/'runs'/f'run-{n:02d}'
out.mkdir()
src = root/'TwoPin.lean'
(out/'TwoPin.lean').write_bytes(src.read_bytes())
cmd = ['lake','env','lean','-DwarningAsError=true', str(out/'TwoPin.lean')]
start = time.monotonic()
r = subprocess.run(cmd,cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(out/'output.log').write_text(r.stdout)
meta = dict(command=cmd,cwd='/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025',exit=r.returncode,elapsed_seconds=time.monotonic()-start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
(out/'meta.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta))
print(r.stdout)
