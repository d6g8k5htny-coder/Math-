import datetime, hashlib, json, os, pathlib, subprocess, time
root=pathlib.Path('/workspace/scratch/actual-fold-candidate-inertia')
cwd=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
n=len(list((root/'logs').glob('run-*')))+1
run=root/'logs'/f'run-{n:03d}'
run.mkdir()
src=root/'Inertia.lean'
snap=run/'Inertia.lean'
snap.write_bytes(src.read_bytes())
argv=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true',str(snap)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat(); timer=time.monotonic()
p=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
elapsed=time.monotonic()-timer; end=datetime.datetime.now(datetime.timezone.utc).isoformat()
(run/'stdout.log').write_bytes(p.stdout); (run/'stderr.log').write_bytes(p.stderr)
receipt={'argv':argv,'cwd':str(cwd),'utc_start':start,'utc_end':end,'elapsed_seconds':elapsed,'exit_code':p.returncode,'source_sha256':hashlib.sha256(snap.read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}
(run/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt)); print(p.stdout.decode()); print(p.stderr.decode())
