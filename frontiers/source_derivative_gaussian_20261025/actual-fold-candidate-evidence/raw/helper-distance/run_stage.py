#!/usr/bin/env python3
import datetime,hashlib,json,pathlib,shutil,subprocess,sys,time
base=pathlib.Path('/workspace/scratch/actual-fold-candidate-distance')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=base/'CandidateDistance.lean'
def ident(p):
    if not p.exists(): return None
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
label=sys.argv[1]; command=sys.argv[2:]; run=base/'runs'/label; run.mkdir(parents=True,exist_ok=False)
for p in base.glob('*.lean'): shutil.copy2(p,run/p.name)
record={'label':label,'cwd':str(packet),'command':command,'source':ident(source),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(run/'START.json').write_text(json.dumps(record,indent=2)+'\n'); start=time.monotonic()
with open(run/'output.log','wb') as out: result=subprocess.run(command,cwd=packet,stdout=out,stderr=subprocess.STDOUT)
record.update({'exit_code':result.returncode,'elapsed_seconds':time.monotonic()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'log':ident(run/'output.log')})
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n'); print((run/'output.log').read_text()); print(json.dumps(record,indent=2));sys.exit(result.returncode)
