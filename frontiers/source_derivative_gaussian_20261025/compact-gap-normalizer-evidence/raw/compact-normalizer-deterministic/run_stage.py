import datetime, hashlib, json, pathlib, shutil, subprocess, sys, time
base=pathlib.Path('/workspace/scratch/compact-normalizer-deterministic')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=base/'Deterministic.lean'; obj=base/'build/Deterministic.olean'
def ident(p):
 return None if not p.exists() else {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
label=sys.argv[1]; run=base/'runs'/label; run.mkdir(parents=True,exist_ok=False)
shutil.copy2(source,run/source.name)
command=['/home/agent/.elan/bin/lake','env','lean','--root='+str(base),'-DwarningAsError=true','-o',str(obj),str(source)]
record={'label':label,'purpose':'new arbitrary-gap deterministic join elaboration only; completed dependencies reused','cwd':str(packet),'command':command,'before':{'source':ident(source)},'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
start=time.time()
with open(run/'output.log','wb') as out: result=subprocess.run(command,cwd=packet,stdout=out,stderr=subprocess.STDOUT)
record.update({'exit_code':result.returncode,'elapsed_seconds':time.time()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after':{'source':ident(source),'object':ident(obj)},'log':ident(run/'output.log')})
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print((run/'output.log').read_text());print(json.dumps(record,indent=2));sys.exit(result.returncode)
