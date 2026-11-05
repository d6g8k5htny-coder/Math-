import collections,datetime,hashlib,json,pathlib
BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
PUB=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
PROJECT=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
ACTIVE='final-closure001'
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
    p=pathlib.Path(p); st=p.stat(); marker=[st.st_size,st.st_mtime_ns]
    old=cache.get(str(p))
    if old and old.get('marker')==marker: return old
    row={'path':str(p),'bytes':st.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'marker':marker,'first_observed_utc':utc(),'origin':'FIRST new actual final closure payload/version identity, calculated once'}
    cache[str(p)]=row
    return row
def put(name,data):
    p=BASE/name; assert not p.exists(), 'No frozen closure output regeneration'
    p.write_text(json.dumps(data,indent=2)+'\n'); return identity(p)
gen=BASE/'runs/final-documents001/receipt.json'; gr=json.loads(gen.read_text()); assert gr['exit_code']==0
layers={'worker':{'receipt':identity(gen),'record':gr,
 'streams':[identity(gen.parent/'stdout.log'),identity(gen.parent/'stderr.log')]}}
for layer in ['outer','entry']:
    p=BASE/'outer/final-documents001'/(layer+'.receipt.json'); r=json.loads(p.read_text()); assert r['exit_code']==0
    layers[layer]={'receipt':identity(p),'record':r,'streams':[identity(r['stdout']),identity(r['stderr'])]}
closed=[json.loads(p.read_text()) for p in (BASE/'runs').glob('*/receipt.json')]
counts=dict(collections.Counter(r['scope_kind'] for r in closed)); assert counts=={'documentary':24,'math':15}
root={}
for name in ['ROOT_SOURCE_CUT.json','ROOT_OWN_OBJECT_COPY.json']:
    p=PUB/name; root[name]={'path':str(p),'state':'ACTUAL RECORD PRESENT' if p.exists() else 'PENDING ROOT ONLY',
      'record':json.loads(p.read_text()) if p.exists() else None}
addendum=put('EXECUTION_RECORD_INDEX_ADDENDUM.json',{
 'purpose':'Actual closed final-documents001 worker/outer/entry added AFTER its own generation. No generator rerun or self-recursive ID.',
 'closed_counts_before_this_closure':counts,'closed_runs_before_this_closure':len(closed),
 'closed_original_streams_before_this_closure':6*len(closed),'final_document_generator_layers':layers,
 'this_closure_label':ACTIVE,'this_closure_capture':'Prospective worker/outer/entry, actual files close after this output is written; root adopts their actual closed records/streams after entry exit0',
 'expected_complete_totals_after_this_closure':{'math':15,'documentary':25,'workers':40,'original_split_streams':240},
 'root_sourcecut_copy_observation':root})
initial=json.loads((BASE/'ARTIFACT_IDENTITIES.json').read_text())
oldpaths={r['path'] for r in initial['artifacts']}
def eligible(p):
    if not p.is_file() or p==BASE/'FIRST_ID_CACHE.json': return False
    if p.suffix in {'.olean','.ilean','.pyc'} or '__pycache__' in p.parts: return False
    if p.parent==BASE/'runs'/ACTIVE and p.name in ['receipt.json','stdout.log','stderr.log']: return False
    if p.parent==BASE/'outer'/ACTIVE: return False
    return True
paths=[PROJECT/'SourceActualSaddleUppercuts.lean']+sorted(p for p in BASE.rglob('*') if eligible(p))
newrows=[identity(p) for p in paths if str(p) not in oldpaths]
artifact=put('ARTIFACT_IDENTITIES_ADDENDUM.json',{'actual_new_rows':newrows,
 'root_only_observation':root,'no_old_hash':'Known matching versions/copies reused from actual cached FIRST IDs',
 'this_closure_final_records':'Actual closed current worker/outer/entry identities are adopted by root after entry exit0. No missing original streams and no recursive self-ID.'})
deferred=[BASE/'runs'/ACTIVE/n for n in ['receipt.json','stdout.log','stderr.log']]
deferred += [BASE/'outer'/ACTIVE/(layer+suffix) for layer in ['outer','entry'] for suffix in ['.receipt.json','.stdout.log','.stderr.log']]
newnames=['EXECUTION_RECORD_INDEX_ADDENDUM.json','ARTIFACT_IDENTITIES_ADDENDUM.json','PUBLICATION_ALLOWLIST_FINAL.json','FINAL_READY.json','FINAL_DOCUMENT_IDS.json']
allowpaths=sorted(set(str(p) for p in paths)|{str(p) for p in deferred}|{str(BASE/n) for n in newnames})
allow=put('PUBLICATION_ALLOWLIST_FINAL.json',{'status':'FROZEN producer text-only65 allowlist; adopt only after actual final-closure001 entry exit0',
 'paths':allowpaths,'path_count':len(allowpaths),'source_only':str(PROJECT/'SourceActualSaddleUppercuts.lean'),
 'excluded':'All binaries, mutable FIRST_ID_CACHE, old modules/evidence, root-owned future66 EXTRAs, shared metadata/config and external files',
 'root_appendix':'Root may separately append its actual sourcecut/copy/context/release/reading and technical-review records under root metadata scope; no producer canonical copying/Git action',
 'closure_final_deferred_actual_paths':[str(p) for p in deferred],
 'closure_identity_policy':'Worker streams become known in recorder cache after child. Remaining newly closed receipt/outer/entry identities need root FIRST adoption, not a producer rerun/self hash.'})
final=json.loads((BASE/'FINAL_IDS.json').read_text()); control=json.loads((BASE/'CONTROL_IDS.json').read_text())
ready=put('FINAL_READY.json',{'status':'ALL MATH PASS; final producer custody outputs written. Root adopts READY after actual enclosing final-closure001 entry exit0.',
 'observed_write_utc':utc(),'mathematical_runs':15,'production_named_kernels':1,'ordinary_named_kernels':0,
 'production_owned_constants':119,'ordinary_owned_constants':123,
 'source':final['source'],'own_object':final['own_object'],'ordinary_source':control['ordinary_source'],
 'ordinary_object':control['ordinary_object'],'sole_negative_harness':control['sole_negative_harness'],
 'expected_negative_exit':1,'sole_unsolved_False':1,'negative_stdout_bytes':control['negative_stdout_bytes'],'negative_stderr_bytes':0,
 'sourcecut_copy':root,'producer_canonical_copies':0,'all_further_old_copies':'SKIP',
 'mathematical_review':'PASS/no findings, technical/FINAL_MATH.md; final custody review/root reading remains separately authorized',
 'next':'Root FULL final documents/bindings, root final-reading record, technical final custody PASS, then root-only FINAL_GO/metadata/cut/copy/publication as applicable. No unchanged math/hash replay.',
 'larger_goal':'ACTIVE_UNMET beyond local65, no stop_goal inference','future66':'Root EXTRAs only, excluded and not a65 source dependency'})
names=['REPORT.md','HANDOFF.md','CONTROL_IDS.json','FINAL_IDS.json','EXECUTION_RECORD_INDEX.json',
 'ARTIFACT_IDENTITIES.json','HISTORICAL_ID_BINDINGS.json','FINAL_DOCUMENT_IDS_INITIAL.json','PUBLICATION_ALLOWLIST_INITIAL.json',*newnames[:-1]]
docids=put('FINAL_DOCUMENT_IDS.json',{'first_or_reused_final_document_ids':[identity(BASE/n) for n in names],
 'known_source_control_object_ids':'FINAL_IDS/CONTROL_IDS, all original cached FIRST IDs reused',
 'active_cache_for_root_reuse':str(BASE/'FIRST_ID_CACHE.json'),
 'final_closed_capture_paths_for_root_FIRST_adoption':[str(p) for p in deferred],
 'self_identity':'Recorded once in actual closure stdout/recorder cache after this file write; not recursively embedded in its own content'})
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'status':'FINAL PRODUCER CUSTODY WRITTEN; require actual enclosing entry exit0 for adoption',
 'ready':ready,'final_document_ids':docids,'allowlist':allow,'artifact_addendum_rows':len(newrows),
 'allowlist_paths':len(allowpaths),'complete_expected_counts':{'math':15,'documentary':25,'all_runs':40,'original_split_streams':240},
 'deferred_new_closed_capture_IDs':[str(p) for p in deferred],
 'sourcecut_copy_states':{k:v['state'] for k,v in root.items()}}))
