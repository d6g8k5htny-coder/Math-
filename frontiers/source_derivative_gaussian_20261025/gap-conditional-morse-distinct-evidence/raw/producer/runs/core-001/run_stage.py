#!/usr/bin/env python3
import datetime,hashlib,json,pathlib,shutil,subprocess,sys,time
base=pathlib.Path('/workspace/scratch/gap-conditional-morse-distinct-construct')
packet=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceGapConditionalMorseDistinct.lean'
obj=base/'build/SourceGapConditionalMorseDistinct.olean'
controls=base/'build/GapMorseDistinctControls.olean'
def ident(p):
    if not p.exists():return None
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def lineage():return {'source':ident(source),'object':ident(obj),'controls_object':ident(controls)}
label=sys.argv[1];command=sys.argv[2:];run=base/'runs'/label
run.mkdir(parents=True,exist_ok=False)
for p in [source,*base.glob('*.lean'),base/'CONTROL_CONTRACT.md',base/'run_stage.py',base/'SHARED_CONTEXT59_V1.md']:
    if p.exists():shutil.copy2(p,run/p.name)
record={'label':label,'cwd':str(packet),'command':command,'before':lineage(),
        'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'capture':'Original stdout and stderr captured separately without reconstruction/interleaving claims'}
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
