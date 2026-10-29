#!/usr/bin/env python3
# Frozen as history/runner.001.py before the first stage63 execution.
import datetime, hashlib, json, pathlib, shutil, subprocess, sys, time
BASE=pathlib.Path('/workspace/scratch/actual-source-finite-superlevel-components-construct')
PACKET=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
SOURCE=PACKET/'SourceActualFiniteSuperlevelComponents.lean'
CACHE=BASE/'OWN_ID_CACHE.json'
RUNNER_VERSION='001'
cache=json.loads(CACHE.read_text()) if CACHE.exists() else {}
def ident(p):
    if not p.exists():return None
    st=p.stat();key=str(p);stamp=[st.st_size,st.st_mtime_ns]
    old=cache.get(key)
    if old and old['stamp']==stamp:
        return dict(old['identity'],identity_origin='Existing owned FIRST identity reused; unchanged stat')
    row={'path':key,'bytes':st.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'identity_origin':'FIRST identity of newly created or changed owned payload'}
    cache[key]={'stamp':stamp,'identity':row};return row
label=sys.argv[1];command=sys.argv[2:]
run=BASE/'runs'/label;run.mkdir(parents=True,exist_ok=False)
tracked=[SOURCE,BASE/'build/SourceActualFiniteSuperlevelComponents.olean',BASE/'build/FiniteSuperlevelComponentsControls.olean',BASE/'record_run.py',BASE/'CONTEXT.md',*BASE.glob('*.lean'),*BASE.glob('*.lean.txt')]
tracked=list(dict.fromkeys(tracked));before={str(p):ident(p) for p in tracked};snapshots=[]
for p in tracked:
    if p.exists() and p.suffix!='.olean':
        target=run/p.name;shutil.copy2(p,target)
        snapshots.append({'immutable_path':str(target),'existing_identity':before[str(p)]})
record={'label':label,'cwd':str(PACKET),'command':command,'runner_version':RUNNER_VERSION,'runner_history':str(BASE/f'history/runner.{RUNNER_VERSION}.py'),'before':before,'snapshots':snapshots,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
CACHE.write_text(json.dumps(cache,indent=2)+'\n')
start=time.monotonic();deadline=datetime.datetime(2026,10,28,20,45,tzinfo=datetime.timezone.utc)
remaining=max(0,(deadline-datetime.datetime.now(datetime.timezone.utc)).total_seconds())
with open(run/'stdout.log','wb') as out,open(run/'stderr.log','wb') as err:
    if remaining<=0:
        result_code=124;err.write(b'ROOT hard terminal reached before execution; command not run.\n')
    else:
        try:result_code=subprocess.run(command,cwd=PACKET,stdout=out,stderr=err,timeout=min(300,remaining)).returncode
        except subprocess.TimeoutExpired:
            result_code=124;err.write(b'Actual subprocess timeout; no mathematical rejection claimed.\n')
record.update({'exit_code':result_code,'elapsed_seconds':time.monotonic()-start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after':{str(p):ident(p) for p in tracked},'stdout':ident(run/'stdout.log'),'stderr':ident(run/'stderr.log')})
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n');CACHE.write_text(json.dumps(cache,indent=2)+'\n')
print((run/'stdout.log').read_text());print((run/'stderr.log').read_text());print(json.dumps({k:record[k] for k in ['label','exit_code','elapsed_seconds','started_utc','ended_utc']},indent=2));sys.exit(result_code)
