from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, time
base=Path('/workspace/scratch/compact-normalizer-gaussian')
packet=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
label=sys.argv[1]
run=base/'runs'/label
run.mkdir(exist_ok=False)
source=base/'GaussianLower.lean'
obj=base/'build'/'GaussianLower.olean'
def ident(p):
    if not p.exists(): return None
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
shutil.copy2(source, run/'GaussianLower.lean')
cmd=['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true','-R',str(base),'-o',str(obj),str(source)]
r={'label':label,'cwd':str(packet),'command':cmd,'before':{'source':ident(source),'object':ident(obj)},'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
t=time.monotonic()
p=subprocess.run(cmd,cwd=packet,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(run/'output.log').write_bytes(p.stdout)
r.update(exit_code=p.returncode,elapsed_seconds=time.monotonic()-t,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),after={'source':ident(source),'object':ident(obj)},log=ident(run/'output.log'))
(run/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(p.stdout.decode(),end='')
print(json.dumps({'label':label,'exit_code':p.returncode,'elapsed_seconds':r['elapsed_seconds'],'receipt':str(run/'receipt.json')}))
sys.exit(p.returncode)
