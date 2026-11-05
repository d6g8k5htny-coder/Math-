#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import json,os,shutil,subprocess,time
R=Path('/workspace/scratch/actual-source-finite-superlevel-components-publication');P=Path('/workspace/scratch/actual-source-finite-superlevel-components-construct');REPO=Path('/workspace/Math-curvature-20261026');BASE='139aa244cccb16395b71e244dd5b81bd330e1595'
def now():return datetime.now(timezone.utc).isoformat()
def put(p,d):
 with p.open('w')as f:json.dump(d,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert not(R/'ROOT_SOURCE_CUT.json').exists()and not(R/'ROOT_OWN_OBJECT_COPY_INTENT.json').exists()
z=json.loads((P/'FINAL_SOURCE_OBJECT_IDS.PRE_KERNEL.json').read_text());s=z['source'];o=z['object'];source=Path(s['path']);obj=Path(o['path']);rel=source.relative_to(REPO);dst=source.parent/'.lake/build/lib/lean/SourceActualFiniteSuperlevelComponents.olean'
assert source.stat().st_size==s['bytes']and obj.stat().st_size==o['bytes']and not dst.exists()
paths={'strict':Path(z['receipt']),'inventory':P/'runs/inventory-001/receipt.json','kernel':P/'runs/kernel-001/receipt.json'};records={}
for name,path in paths.items():
 q=json.loads(path.read_text());assert q['exit_code']==0
 for phase in ['before','after']:assert q[phase][str(source)]['sha256']==s['sha256']
 assert q['after'][str(obj)]['sha256']==o['sha256']
 if name!='strict':assert q['before'][str(obj)]['sha256']==o['sha256']
 records[name]={**{k:q[k]for k in ['command','cwd','started_utc','ended_utc','exit_code','stdout','stderr']},'receipt':str(path)}
assert len([x for x in(P/'runs').glob('*/receipt.json')if 'leanchecker' in str(json.loads(x.read_text())['command'])])==1
commands=[]
def run(label,args):
 start=now();tick=time.monotonic();out=R/(label+'.stdout.txt');err=R/(label+'.stderr.txt')
 with out.open('wb')as a,err.open('wb')as b:q=subprocess.run(args,cwd=REPO,stdout=a,stderr=b)
 rec={'command':args,'cwd':str(REPO),'started_utc':start,'ended_utc':now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':q.returncode,'stdout':str(out),'stderr':str(err)};commands.append(rec);put(R/'ROOT_SOURCE_CUT_COMMANDS.json',commands)
 if q.returncode:raise RuntimeError('Actual command failed; preserve original streams and prior completed actions, no automatic retry')
 return out.read_text().strip()
assert run('SOURCE_CUT_01',['git','rev-parse','HEAD'])==BASE
assert not run('SOURCE_CUT_02',['git','diff','--cached','--name-only'])
run('SOURCE_CUT_03',['git','status','--short'])
run('SOURCE_CUT_04',['git','add','--',str(rel)])
assert run('SOURCE_CUT_04B',['git','diff','--cached','--name-only'])==str(rel)
run('SOURCE_CUT_05',['git','commit','-m','Prove finiteness of every actual torus closed-superlevel component set'])
cut=run('SOURCE_CUT_06',['git','rev-parse','HEAD']);blob=run('SOURCE_CUT_07',['git','rev-parse','HEAD:'+str(rel)])
record={'created_utc':now(),'status':'SOURCE_ONLY63_PRODUCTION_QUALIFIED_ORDINARY_CONTROLS_AND_REGISTRATION_PENDING','source_cut':cut,'parent':BASE,'source':s,'own_object':o,'source_git_blob':blob,'qualification_receipts':records,'inventory':{'actual_owned':30,'authored_public_Prop':1,'public_data':0,'counts':'18authoredprivateProps+1publicProp+4privdefs+3proofaux+2eq+2simp; others0','standard3':'ALL30PASS completedinventory001','full_inventory':str(P/'INVENTORY.json')},'kernel_count':1,'historical_source_freeze_record':str(P/'FINAL_SOURCE_OBJECT_IDS.PRE_KERNEL.json'),'root_personal_reading':'FULLpropercontracts/context001+allactual002003deltas; BOUNDEDproduction onlycore/header/compact/LP/Finiteconsumer/publicdeclaration. Notfull267/all30/rawstd3/all8receipts16streams. ReviewerFULLfinalcoverage/core+allactualfixturetail/patches/all30/std3/all8receipts16streams PASS reused.','qualified_registry_remains':{'modules':62,'written':1132,'Prop':1123,'data':9,'inputs':32},'mathematical_replays':0,'payload_hashes_this_action':0,'scientific_effect':'NONE'}
put(R/'ROOT_SOURCE_CUT.json',record)
intent={'created_utc':now(),'source_cut':cut,'source':str(obj),'destination':str(dst),'source_identity':s,'eligible_own_object_identity':o,'qualification_receipts':records,'copy_once':True,'copy_scope':'ONLYnewqualified63own.olean; nohelper/Controls/ilean/oldobject','all_further_copy_actions':'SKIP'};put(R/'ROOT_OWN_OBJECT_COPY_INTENT.json',intent)
dst.parent.mkdir(parents=True,exist_ok=True);assert not dst.exists();shutil.copyfile(obj,dst)
with dst.open('rb')as f:os.fsync(f.fileno())
result={**intent,'completed_utc':now(),'action':'COPIED_ONCE','destination_size_metadata':dst.stat().st_size,'identity_reused_no_rehash':o['sha256'],'old_object_copies':0,'helper_or_controls_copies':0,'ilean_copies':0,'mathematical_checks':0}
put(R/'ROOT_OWN_OBJECT_COPY.json',result);print(json.dumps({'source_cut':cut,'source_git_blob':blob,'copy_completed_utc':result['completed_utc'],'eligibleownbytes':o['bytes'],'kernel_count':1,'all_further_copy_actions':'SKIP','registry_remains':record['qualified_registry_remains']}))
