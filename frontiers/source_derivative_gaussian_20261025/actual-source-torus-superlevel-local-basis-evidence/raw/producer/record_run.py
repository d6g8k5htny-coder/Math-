#!/usr/bin/env python3
import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, time
base=pathlib.Path('/workspace/scratch/actual-source-torus-superlevel-local-basis-construct')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceActualTorusSuperlevelLocalBasis.lean'
obj=base/'build/SourceActualTorusSuperlevelLocalBasis.olean'
cachepath=base/'OWN_ID_CACHE.json'
cache=json.loads(cachepath.read_text()) if cachepath.exists() else {}
def ident(p):
    if not p.exists(): return None
    stat=p.stat(); key=str(p); stamp=[stat.st_size,stat.st_mtime_ns]
    old=cache.get(key)
    if old and old['stat']==stamp:
        return dict(old['identity'], identity_origin='reused prior own first identity; unchanged size/mtime')
    result={'path':key,'bytes':stat.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'identity_origin':'first identity of newly created/changed OWN payload'}
    cache[key]={'stat':stamp,'identity':result}
    return result
label=sys.argv[1];command=sys.argv[2:]
run=base/'runs'/label;run.mkdir(parents=True,exist_ok=False)
tracked=[source,obj,base/'build/Controls.olean',*base.glob('*.lean'),*base.glob('*.lean.txt')]
before={str(p):ident(p) for p in tracked}
snapshots=[]
for p in tracked:
    if p.exists() and p.is_file() and p.suffix!='.olean':
        q=run/p.name;shutil.copy2(p,q)
        snapshots.append({'path':str(q),'identity_reused_from':before[str(p)]})
context=base/'CONTEXT.md'
if context.exists():shutil.copy2(context,run/'CONTEXT.md')
record={'label':label,'cwd':str(packet),'command':command,'before':before,'source_snapshots':snapshots,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
start=time.monotonic()
with open(run/'stdout.log','wb') as out, open(run/'stderr.log','wb') as err:
    result=subprocess.run(command,cwd=packet,stdout=out,stderr=err)
record.update({'exit_code':result.returncode,'elapsed_seconds':time.monotonic()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after':{str(p):ident(p) for p in tracked},'stdout':ident(run/'stdout.log'),'stderr':ident(run/'stderr.log')})
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
cachepath.write_text(json.dumps(cache,indent=2)+'\n')
print((run/'stdout.log').read_text());print((run/'stderr.log').read_text());print(json.dumps({k:record[k] for k in ['label','exit_code','elapsed_seconds','started_utc','ended_utc']},indent=2));sys.exit(result.returncode)
