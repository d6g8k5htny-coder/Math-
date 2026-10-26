import datetime,hashlib,json,pathlib,subprocess,time
root=pathlib.Path('/workspace/scratch/remote-jet-arithmetic'); cwd=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
n=len(list((root/'runs').glob('run-*')))+1; run=root/'runs'/f'run-{n:03d}';run.mkdir()
source=root/'Arithmetic.lean'; snap=run/'Arithmetic.lean';snap.write_bytes(source.read_bytes());(run/'compile.py').write_bytes(pathlib.Path(__file__).read_bytes())
argv=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true',str(snap)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();timer=time.monotonic();p=subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE);elapsed=time.monotonic()-timer
(run/'stdout.log').write_bytes(p.stdout);(run/'stderr.log').write_bytes(p.stderr)
r=dict(argv=argv,cwd=str(cwd),utc_start=start,utc_end=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=elapsed,exit_code=p.returncode,source_sha256=hashlib.sha256(snap.read_bytes()).hexdigest(),source_after_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),runner_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
(run/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));print(p.stdout.decode());print(p.stderr.decode())
