from pathlib import Path
import json,hashlib,datetime,collections
p=Path('/workspace/scratch/gap-conditional-morse-distinct-construct');known={}
def add(path,identity,origin):
 if identity and identity.get('sha256'):
  known[str(path)]={'bytes':identity['bytes'],'sha256':identity['sha256'],'identity_origin':origin}
for q in (p/'runs').glob('*/receipt.json'):
 r=json.loads(q.read_text());add(q.parent/'SourceGapConditionalMorseDistinct.lean',r['before']['source'],'Reused exact recorded source ID bound to the source snapshot copied before this actual run.')
 for n in ['stdout','stderr']:
  add(q.parent/(n+'.log'),r[n],'Reused first recorded original split-stream ID from this run receipt.')
 for h in r.get('harness_snapshots',[]):add(Path(h['snapshot']),h['original_identity'],'Reused exact original harness ID bound to the copy captured for this run.')
for v in json.loads((p/'RECORDED_IDENTITY_CACHE.json').read_text()).values():add(Path(v['identity']['path']),v['identity'],'Reused memoized own-artifact first identity; no new hash of frozen source/object/harness.')
for q in [p/'CONTROL_CONTRACT.md',*(p/'runs').glob('*/CONTROL_CONTRACT.md')]:add(q,{'bytes':12298,'sha256':'aa42af6f306361343b0536bbd1cece548d0094a705bbadd56f76bb7d637564a9'},'Reused authoritative published pre-code control identity from ROOT_GO/CONTROL_FREEZE_ADOPTION; unchanged copied contract.')
for row in json.loads((p/'HELPER_D_ORIGINAL_IDENTITIES.json').read_text())['originals']:
 add(p/'helper-global-cover-frozen'/row['name'],row,'Reused first original helperD ID recorded before one integration.')
for d,n in [('finite-frame','FROZEN_HELPER.json'),('incidence','FROZEN_HELPER.json'),('lifetime-geometry','FROZEN_IDENTITIES.json'),('actual-controls','FROZEN_HELPER.json')]:
 for row in json.loads((p/('helper-'+d+'-frozen')/n).read_text())['files']:
  add(p/('helper-'+d+'-frozen')/Path(row['path']).name,row,'Reused original helper identity frozen before one integration; immutable owned copy.')
for row in json.loads((p/'NUMERIC_HELPER_FIRST_IDENTITIES.json').read_text())['files']:
 add(Path(row['copied_to']),row,'Reused first new numeric helper identity captured before one integration.')
add(p/'helper-amendments/numeric-positive-companion-actual-section.lean.txt',known[str(p/'helper-numeric-controls-frozen/SECTION.lean.txt')],'Exact unchanged numeric helper evidence copy; original first identity reused.')
files=[];counter=collections.Counter()
for f in sorted(p.rglob('*')):
 if not f.is_file() or 'build' in f.relative_to(p).parts or f.name=='CUSTODY.json':continue
 k=known.get(str(f))
 if k:
  assert f.stat().st_size==k['bytes'],(str(f),'size changed from recorded binding')
  row={'path':str(f),'relative_path':str(f.relative_to(p)),**k};counter['reused_recorded_ids']+=1
 else:
  b=f.read_bytes();row={'path':str(f),'relative_path':str(f.relative_to(p)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'identity_origin':'First custody ID of NEW previously unrecorded producer evidence/metadata/snapshot only; no old dependency payload hash.'};counter['first_new_payload_ids']+=1
 files.append(row)
s=json.loads((p/'SOURCE_OBJECT_IDENTITIES.json').read_text())
j={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'FINAL_NEW59_PRODUCER_CUSTODY_FROZEN_ALL19_ACTUAL_RUNS','raw_producer_payload_count':len(files),'identity_counts':dict(counter),'policy':'Known exact IDs reused for frozen production source/object, Controls003, numeric companion, run source/harness copies, original split streams, frozen helpers and precode contract. First hashes only for NEW previously unrecorded evidence/metadata copies. No old source/object/evidence/mathlib payload hashes or proof checks.','files':files,'source':s['source'],'eligible_own_object':s['object'],'ineligible_controls_objects':[s['controls_object'],s['numeric_controls_object']],'raw_payload_exclusions':'build/ objects are bound above as original scratch artifacts, not raw text payloads. Only the named production ownobject is eligible for root cache, alreadycopiedONCE. BothControls objects are ineligible. No furthercopy/ilean refresh.','self_identity':'This manifest has no self SHA claim; root archive may record its first outer identity.','source_cut_separate_root_process_record':s['root_source_cut_process_record'],'root_own_object_copy_once':s['root_copy_once_record'],'historical_pending_frozen_records':'FROZEN_SOURCE/FROZEN_CONTROLS and originalpre-numericreport snapshots preserved unchanged.','immutable_after_final_delivery':True,'no_pending_mathematical_verification':True,'independent_final_review_and_publication':'Separate root/reviewer process; no implication that delivery equals reading or provider-distinct scientific credit.','same_family_credit':0,'scientific_effect':'NONE'}
(p/'CUSTODY.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({'files':len(files),'counts':dict(counter),'report':next(x for x in files if x['relative_path']=='REPORT.md'),'handoff':next(x for x in files if x['relative_path']=='HANDOFF.json')},indent=2))
