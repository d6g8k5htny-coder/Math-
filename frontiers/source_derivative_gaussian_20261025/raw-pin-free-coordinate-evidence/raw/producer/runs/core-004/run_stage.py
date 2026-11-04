#!/usr/bin/env python3
import datetime,hashlib,json,pathlib,shutil,subprocess,sys,time
base=pathlib.Path('/workspace/scratch/raw-pin-free-coordinate-construct')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceRawPinFreeCoordinates.lean'; obj=base/'build/SourceRawPinFreeCoordinates.olean'
def ident(p):
    if not p.exists():return None
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
label=sys.argv[1];command=sys.argv[2:];run=base/'runs'/label;run.mkdir(parents=True,exist_ok=False)
for p in [source,*base.glob('*.lean'),base/'CONTROL_CONTRACT.md',base/'run_stage.py']:
    if p.exists():shutil.copy2(p,run/p.name)
record={'label':label,'cwd':str(packet),'command':command,'before':{'source':ident(source),'object':ident(obj)},'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
start=time.time()
with open(run/'output.log','wb') as out:
    result=subprocess.run(command,cwd=packet,stdout=out,stderr=subprocess.STDOUT)
record.update({'exit_code':result.returncode,'elapsed_seconds':time.time()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after':{'source':ident(source),'object':ident(obj)},'log':ident(run/'output.log')})
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print((run/'output.log').read_text());print(json.dumps(record,indent=2));sys.exit(result.returncode)
