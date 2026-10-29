import subprocess, pathlib, hashlib, json, time, sys, os, shutil
root=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=pathlib.Path('/workspace/scratch/adaptive-fold-scalar-barrier')
label=sys.argv[1]; command=sys.argv[2:]
run=out/'runs'/label; run.mkdir(parents=True,exist_ok=False)
source=root/'AdaptiveFoldScalarBarrier.lean'
if source.exists(): shutil.copy2(source,run/source.name)
for p in out.glob('*.lean'): shutil.copy2(p,run/p.name)
start=time.time(); result=subprocess.run(command,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(run/'output.log').write_bytes(result.stdout)
record={'command':command,'cwd':str(root),'started_unix':start,'elapsed_seconds':time.time()-start,'exit_code':result.returncode,'snapshots':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in run.glob('*.lean')}}
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record)); print(result.stdout.decode(),end=''); sys.exit(result.returncode)
