#!/usr/bin/env python3
import datetime,hashlib,json,pathlib,shutil,subprocess,sys,time
base=pathlib.Path('/workspace/scratch/gap-conditional-morse-distinct-construct')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceGapConditionalMorseDistinct.lean'
obj=base/'build/SourceGapConditionalMorseDistinct.olean'
controls=base/'build/GapMorseDistinctControls.olean'
numeric_controls=base/'build/GapMorseDistinctNumericControls.olean'
cache_path=base/'RECORDED_IDENTITY_CACHE.json'
identity_cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
def ident(p):
    if not p.exists():return None
    st=p.stat();stamp=[st.st_ino,st.st_size,st.st_mtime_ns]
    known=identity_cache.get(str(p))
    if known and known['stat_stamp']==stamp:
        return dict(known['identity'])
    value={'path':str(p),'bytes':st.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    identity_cache[str(p)]={'stat_stamp':stamp,'identity':value}
    cache_path.write_text(json.dumps(identity_cache,indent=2)+'\n')
    return value
def lineage():return {'source':ident(source),'object':ident(obj),'controls_object':ident(controls),'numeric_controls_object':ident(numeric_controls)}
label=sys.argv[1];command=sys.argv[2:];run=base/'runs'/label
run.mkdir(parents=True,exist_ok=False)
for p in [source,*base.glob('*.lean'),base/'CONTROL_CONTRACT.md',base/'run_stage.py',base/'SHARED_CONTEXT59_V1.md']:
    if p.exists():shutil.copy2(p,run/p.name)
record={'label':label,'cwd':str(packet),'command':command,'before':lineage(),
        'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'capture':'Original stdout and stderr captured separately without reconstruction/interleaving claims',
        'harness_snapshots':[{'snapshot':str(run/q.name),'original_identity':ident(q)} for q in base.glob('*.lean')]}
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
start=time.time()
with open(run/'stdout.log','wb') as out,open(run/'stderr.log','wb') as err:
    result=subprocess.run(command,cwd=packet,stdout=out,stderr=err)
record.update({'exit_code':result.returncode,'elapsed_seconds':time.time()-start,
    'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after':lineage(),
    'stdout':ident(run/'stdout.log'),'stderr':ident(run/'stderr.log')})
(run/'receipt.json').write_text(json.dumps(record,indent=2)+'\n')
for name in ['stdout.log','stderr.log']:
    content=(run/name).read_text()
    if content: print(content,end='')
print(json.dumps(record,indent=2));sys.exit(result.returncode)
