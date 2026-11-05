#!/usr/bin/env python3
# Documentary FIRST IDs only. Completed mathematical and identity evidence is reused.
from pathlib import Path
import json, hashlib, datetime
B=Path('/workspace/scratch/actual-source-torus-regular-slab-construct')
S=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualTorusRegularSlab.lean')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,value):
 p=B/name
 assert not p.exists(),str(p)
 p.write_text(json.dumps(value,indent=2)+'\n' if not isinstance(value,str) else value)
 return p
def first(p):
 data=p.read_bytes()
 return {'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'identity_origin':'FIRST documentary identity; no previous hash/check replay'}
receipts=sorted([json.loads(p.read_text()) for p in (B/'runs').glob('*/receipt.json')],key=lambda d:d['started_utc'])
by={d['label']:d for d in receipts}
strict,inv,kernel,controls,negative=[by[k] for k in ['compile-final','inventory-001','kernel-001','controls-002','false-control-001']]
source=str(S); obj=str(B/'build/SourceActualTorusRegularSlab.olean'); csrc=str(B/'TorusRegularSlabControls.lean'); cobj=str(B/'build/TorusRegularSlabControls.olean'); nsrc=str(B/'FalseMutation.lean')
known={}
snapshots=[]
for d in receipts:
 for side in ['before','after']:
  for p,v in d[side].items():
   if v: known[p]=v
 for side in ['stdout','stderr']: known[d[side]['path']]=d[side]
 for row in d['snapshots']:
  v=dict(row['existing_identity'],path=row['immutable_path'],identity_origin='Existing per-run pre-execution source identity reused for immutable snapshot')
  known[row['immutable_path']]=v
  snapshots.append({'run':d['label'],**row})
for tag in ['A','B','C']:
 for row in json.loads((B/f'originals/{tag}_CUSTODY.json').read_text())['originals']:
  known[row['immutable_retained']]={'path':row['immutable_retained'],'bytes':row['bytes'],'sha256':row['sha256'],'identity_origin':row['origin'],'original_path':row['original']}
for tag in ['001','002']:
 d=json.loads((B/f'context/FIRST_ID_{tag}.json').read_text()); known[d['path']]={k:d[k] for k in ['path','bytes','sha256']}|{'identity_origin':'Existing context FIRST identity reused'}
d=json.loads((B/'history/INITIAL_RUNNER_CUSTODY.json').read_text())
known[d['immutable_initial_runner']]={'path':d['immutable_initial_runner'],'bytes':d['bytes'],'sha256':d['sha256'],'identity_origin':'Existing initial runner FIRST identity reused'}
known[str(B/'history/CONTEXT.INITIAL.md')]=dict(known[str(B/'context/CONTEXT.001.md')],path=str(B/'history/CONTEXT.INITIAL.md'),identity_origin='Existing context001 identity reused for initial retained exact snapshot')
counts=json.loads((B/'INVENTORY.json').read_text())['counts']
qual={'recorded_utc':now,'status':'PASS','source':strict['after'][source],'own_object':strict['after'][obj],'strict_receipt':str(B/'runs/compile-final/receipt.json'),'inventory_receipt':str(B/'runs/inventory-001/receipt.json'),'kernel_receipt':str(B/'runs/kernel-001/receipt.json'),'declaration_count':73,'classifications':counts,'allowed_axioms':['propext','Classical.choice','Quot.sound'],'own_kernel_count':1,'strict_end':strict['ended_utc'],'inventory_end':inv['ended_utc'],'kernel_end':kernel['ended_utc'],'historical_pre_kernel_file':'FINAL_SOURCE_OBJECT_IDS.PRE_KERNEL.json is immutable and truthfully records kernel_count_at_this_source_freeze=0','source_cut':'f99b2e1b4efb7e0d9d3d83420ba7859a611a2016','parent':'c18ad0b8f62060cb78670f5f806af25f1307614b','git_blob':'362b629da2b1895e259decf052f40343e5ce6e24','root_own_copy_count':1,'root_own_copy_utc':'2026-10-28T18:14:34.683861Z','all_further_copies':'SKIP','verification_reuse':'All unchanged applicable evidence reused; no old checks for session/head/process.'}
write('PRODUCTION_QUALIFICATION.json',qual)
controlids={'recorded_utc':now,'status':'PASS','source':controls['after'][csrc],'ordinary_object':controls['after'][cobj],'receipt':str(B/'runs/controls-002/receipt.json'),'completed_utc':controls['ended_utc'],'complete_original_first_run':str(B/'runs/controls-001/TorusRegularSlabControls.lean'),'original_first_identity':by['controls-001']['before'][csrc],'full_actual_patch':str(B/'amendments/controls-002.patch'),'negative_harness':negative['after'][nsrc],'negative_receipt':str(B/'runs/false-control-001/receipt.json'),'negative_exit':negative['exit_code'],'negative_stdout':negative['stdout'],'negative_stderr':negative['stderr'],'negative_completed_utc':negative['ended_utc'],'negative_attempt_count':1,'mutation':'ONLY closed band Icc hypothesis replaced by open Ioo; original actual field/sample/period/endpoints/closed superlevels/literal component map retained','positive_controls':['closedRegular_public [0,1/4]','zeroWidth_public [0,0]','emptyBand_public [-3,-2]','emptyBand_whole_nonempty'],'counterproof':'Actual nonempty component collision for cos(2*pi*x)+(1/2)*cos(pi*y), levels -1/2 to 0. H=cos(pi*x) separates upper components; actual lower closed path joins their images. Open-band no-critical hypothesis independently proved.','control_author':'producer only, no ordinary Controls helper, no production private API/source concatenation'}
write('CONTROL_IDS.json',controlids)
write('CONTROL_RECEIPT.json',{'ordinary':{k:controls[k] for k in ['label','command','cwd','started_utc','ended_utc','elapsed_seconds','exit_code','stdout','stderr']},'sole_negative':{k:negative[k] for k in ['label','command','cwd','started_utc','ended_utc','elapsed_seconds','exit_code','stdout','stderr']},'expected_negative':'one unsolved False goal, no other failure','strict_production_separate':True})
# Lossless full receipts with repeated identity records dictionary-rendered for compact custody.
dictionary=[]; intern={}
def encode(x):
 if isinstance(x,dict):
  if 'path' in x and 'bytes' in x and 'sha256' in x:
   key=json.dumps(x,sort_keys=True)
   if key not in intern:intern[key]=len(dictionary);dictionary.append(x)
   return {'$identity':intern[key]}
  return {k:encode(v) for k,v in x.items()}
 if isinstance(x,list):return [encode(v) for v in x]
 return x
encoded=[encode(d) for d in receipts]
write('EXECUTION_RECORD_INDEX.json',{'created_utc':now,'format':'Lossless full actual receipts; replace each singleton $identity object by identity_dictionary[index]. Original authoritative receipt.json and full separate streams remain retained.','identity_dictionary':dictionary,'receipts':encoded,'receipt_paths':[str(B/'runs'/d['label']/'receipt.json') for d in receipts],'run_count':len(receipts),'split_stream_count':2*len(receipts),'runner_versions':['001'],'checks_replayed':0})
write('STREAM_COUNTS.json',{'runs':len(receipts),'stdout_streams':len(receipts),'stderr_streams':len(receipts),'total_streams':len(receipts)*2,'stdout_bytes':sum(d['stdout']['bytes'] for d in receipts),'stderr_bytes':sum(d['stderr']['bytes'] for d in receipts),'streams':[{'label':d['label'],'exit_code':d['exit_code'],'started_utc':d['started_utc'],'ended_utc':d['ended_utc'],'elapsed_seconds':d['elapsed_seconds'],'stdout':d['stdout'],'stderr':d['stderr']} for d in receipts]})
runrows='\n'.join(f"| {d['label']} | {d['exit_code']} | {d['elapsed_seconds']:.6f} | {d['stdout']['bytes']} / {d['stderr']['bytes']} | {d['ended_utc'][11:26]} |" for d in receipts)
report=f'''# Stage62 producer report

The exact actual-source closed-slab theorem is qualified. The sole public Prop is `I4SourceActualTorusRegularSlab.actualSource_closedSlab_componentInclusion_bijective`; there is no public data. It takes positive period, the original smooth sample, ordered levels, and nonvanishing actual physical derivative throughout the CLOSED band, and proves bijectivity of the literal existing superlevel component inclusion map. There is no desired flow, gradient-floor, retract, or component certificate premise.

The proof derives physical coordinate bounds from existing Fourier majorants, a compact CLOSED-cell squared-gradient floor, a globally bounded Lipschitz periodic normalized field, a direct arbitrary finite symmetric Picard family with uniqueness-patched joint continuity, global height barriers before residence/unit height, continuous variable hitting, restricted OPEN quotient descent, actual lower paths, and the literal component-map bijection. Zero width and empty bands are handled. Existing qualified dependencies and their completed checks are reused. No source61 private body/helper/fixture is consumed.

Production source: 1141 lines, {strict['after'][source]['bytes']} bytes, SHA256 `{strict['after'][source]['sha256']}`. Own object: {strict['after'][obj]['bytes']} bytes, SHA256 `{strict['after'][obj]['sha256']}`. Strict final PASS {strict['ended_utc']}; all73 inventoried declarations use only propext/Classical.choice/Quot.sound, PASS {inv['ended_utc']}; exactly ONE named own-module kernel PASS {kernel['ended_utc']}. Full declarations and separate generated/foreign-generated/definition/Prop-bundle classifications are in INVENTORY.json; raw axioms are runs/inventory-001/stdout.log. PRE_KERNEL metadata remains unchanged as a truthful earlier freeze; PRODUCTION_QUALIFICATION.json records the actual final kernel count1.

Ordinary Controls: {controls['after'][csrc]['bytes']} bytes, SHA256 `{controls['after'][csrc]['sha256']}`; object {controls['after'][cobj]['bytes']} bytes, SHA256 `{controls['after'][cobj]['sha256']}`. Strict Controls002 PASS {controls['ended_utc']}. Same actual period2 finite sample has field cos(2πx)+(1/2)cos(πy). Public positive consumers cover [0,1/4], zero width0, and empty[-3,-2], with both empty-band superlevels the whole NONEMPTY torus. An independent actual endpoint component collision at a=-1/2,b=0 refutes the sole Icc→Ioo hypothesis mutation: cos(πx) separates two upper components, while an actual lower CLOSED path joins their images. The TRUE open-band no-critical hypothesis is proved. No toy map, empty-domain shortcut, private API, source concatenation, or second mutation is used.

The sole importing negative, FalseMutation.lean, ran exactly once AFTER Controls PASS: exit1 at {negative['ended_utc']}, stdout119B contains one unsolved `False`, stderr0B. The counterproof is already a theorem in ordinary Controls; the negative confirms the mutated proposition cannot be filled by that route. CONTROL_IDS.json binds original complete Controls001, the full actual Controls002 patch, passed source/object, negative harness and both raw streams.

There are {len(receipts)} actual producer runs and {len(receipts)*2} full separate original streams. All failures are preserved below, including lexical scope/elaboration/lint/coercion corrections. Every run has its exact command/cwd/start/end/duration/exit, before/after identities and immutable pre-run source/harness/context/runner snapshots. EXECUTION_RECORD_INDEX.json is a lossless dictionary-rendered aggregation, not replacement for originals. No old mathematical verification was repeated for a new agent/session/head/process. Historical overwritten milestone object identities are in receipts; historical objects were not copied. Retained literal source snapshots are mapped in ARTIFACT_IDENTITIES.json.

| Actual run | Exit | Seconds | Stdout / stderr bytes | UTC end |
|---|---:|---:|---:|---|
{runrows}

The COMPLETE context001 and initial runner001 were frozen before helper text/first execution. Root personally read the full5105-token context and accepted it; exact root event UTC was not instrumented, so ROOT_CONTEXT_ACCEPTANCE.json records only actual observation/order. Helper FULL ACKs are A17:25:19, B17:25:20, C17:25:45 UTC. Each complete original froze before exactly ONE integration; all helpers have ZERO executions/probes/checks/hashes/objects. Their immutable originals/provenance/freeze and producer FIRST IDs are in originals/*_CUSTODY.json. A authored normalized field, B finite horizon, C height/hitting. Producer owns all actual amendments and all executions. Scope-only context002 adds localized NNReal notation after an actual failure; original001 and full patch remain retained. There were no new dependent helper texts after their originals froze; A additionally ACKed the correction. Twelve actual source patches, one Controls patch and one context patch are retained. Root's static endpoint-rfl suggestion is disclosed primary-author assistance, not an independent review; root made no source edit or Lean execution.

Root alone made source-only cut f99b2e1b4efb7e0d9d3d83420ba7859a611a2016, parent c18ad0b8f62060cb78670f5f806af25f1307614b, blob362b629da2b1895e259decf052f40343e5ce6e24. Exactly ONE eligible canonical own-object copy occurred18:14:34.683861UTC. All further object copies are SKIP. Root publication records are reused, not rehashed. No helper/Controls/ilean/old binary copy was performed.

Technical reviewer actual_fold_chart_source_review reports complete production PASS: full1141 source lines, all73 classifications/std3, three complete originals/provenance/first-ID custody, twelve source patches, eighteen production receipts/36fullstreams. Reviewer then full-read complete Controls001 and actual002 patch/receipts/streams, and sole negative: PASS/no finding. Final documentary custody reading remains the reviewer’s separate final step. Root’s production reading is BOUNDED with disclosed static support; root FULLREAD final328-line ordinary Controls at18:23:47 and reported no finding. Neither root nor reviewer’s exposure is exaggerated. Same-family independent science credit0; science NONE; provider-distinct/process review remains separately tracked by root.

Ready for final custody review and root-only metadata/publication. No further mathematical check or binary copy is needed. Native pickup6475693627, GO17:19:28.323257, hard terminal19:00UTC28Oct remain the binding stage62 interval. Stage61/source63 are outside this producer action. The active /workspace owner guidance requires reuse of completed applicable verification and is carried into HANDOFF.md.
'''
write('REPORT.md',report)
write('HANDOFF.md',f'''# Stage62 final producer handoff

Production and ordinary Controls are complete; the sole negative behaved as expected. Reuse all completed applicable verification. A new agent/session/handoff/head or pending process requirement does not justify rerunning unchanged material. Mathematical evidence and provider/process requirements are separate.

Read REPORT.md, PRODUCTION_QUALIFICATION.json, CONTROL_IDS.json, INVENTORY.json, EXECUTION_RECORD_INDEX.json, STREAM_COUNTS.json and ARTIFACT_IDENTITIES.json. The latter maps actual retained historical snapshots to existing first identities. All21receipts42original streams remain in runs/. Initial runner001 and fullcontext001 precede executions/helper proof text; all changed context/source/Controls versions have literal snapshots and actual full patches. All3helpers froze complete originals before one integration each and ran zero executions/hashes. Ordinary Controls is producer-authored.

Final source57423B14c900c4e81be9b9ffc85e56fe9c3f191ae8405670d15d0e151a766751b6a23b; own object1880192B73dcf886a5f3d2614b93b941d15008b9828ee86d93ff15692823e79f3b03afe8. Strict PASS18:07:03; inventory73/std3 PASS18:08:29; exactly ONE named kernel PASS18:11:15. The PRE_KERNEL file truthfully records the earlier count0 and stays immutable; additive final qualification has count1. No further strict/inventory/kernel run.

Final Controls15686Bcd19b811cefd5c0c66d0a8af4bba4ed4f8246e4b91794e3bcb0ce77af19f43ff; ordinary object838856B920f8685fa6821922c2525c0b3f6b538696aaf5706f45883e0bffc48641ed24a; Controls002PASS18:16:36. Sole FalseMutation148B1221ad2b09c34e0650903160c26a0631f63e94004ba52860589aa1a547059af0; false001 expectedexit1/oneFalse119B/emptyerr18:24:31. No further Controls/negative check.

Root sourcecutf99b2e1b4efb7e0d9d3d83420ba7859a611a2016 parentc18ad0b8; blob362b629da2b1895e259decf052f40343e5ce6e24. Root copied only eligible own object ONCE18:14:34.683861UTC. All further copies SKIP. Root alone owns shared metadata/cache/Git/external publication and next final-GO. Producer did not stage/commit/edit shared files. Packaging preparer helperA is a disclosed proof author, not independent reviewer. Await final reviewer custody PASS/root FINAL_GO before one metadata attempt. Source63proper docs are root-owned EXTRA and untouched here.

Reviewer full scopes and root bounded/full Controls exposure are stated exactly in REPORT.md. Hard19:00UTC28Oct, no automatic extension. Pending publication/process work does not erase completed mathematics.
''')
write('READY.json',{'created_utc':now,'status':'ALL_MATHEMATICS_COMPLETE_EXPECTED_NEGATIVE_COMPLETE_READY_FOR_FINAL_DOCUMENTARY_REVIEW','production_qualified':True,'controls_qualified':True,'sole_negative_expected_rejection':True,'actual_runs':len(receipts),'split_streams':2*len(receipts),'own_kernel_count':1,'helper_originals':3,'integrations_each':1,'helper_executions':0,'helper_hashes':0,'ordinary_control_helpers':0,'root_copy_count':1,'further_copy_action':'SKIP','metadata_action':'Root FINAL_GO required; producer does not execute root/shared/Git/publication actions','hard_terminal_utc':'2026-10-28T19:00:00Z'})
# Capture newly documentary receipts/patches/metadata FIRST IDs; reuse all known payload IDs.
exclude={'OWN_ID_CACHE.json','ARTIFACT_IDENTITIES.json','PACKAGING_ALLOWLIST.json','FINAL_DOCUMENT_IDS.json'}
files=[p for p in sorted(B.rglob('*')) if p.is_file() and p.name not in exclude and p.suffix not in ['.olean','.ilean']]
rows=[]
for p in files:
 if str(p) in known:rows.append(known[str(p)])
 else:rows.append(first(p))
write('ARTIFACT_IDENTITIES.json',{'created_utc':now,'policy':'Existing run/context/helper first identities reused. Newly documentary artifacts/receipts/patches receive their FIRST identity only; no completed mathematical/hash checks repeated.','final_source':strict['after'][source],'final_own_object':strict['after'][obj],'final_control_object':controls['after'][cobj],'artifacts':rows,'immutable_snapshot_bindings':snapshots,'historical_object_custody':'Per-run before/after identities preserved; overwritten historical objects not claimed to be physically retained.','root_records_reused':['/workspace/scratch/actual-source-regular-slab-publication/ROOT_SOURCE_CUT.json','/workspace/scratch/actual-source-regular-slab-publication/ROOT_OWN_OBJECT_COPY_INTENT.json','/workspace/scratch/actual-source-regular-slab-publication/ROOT_OWN_OBJECT_COPY.json'],'root_records_hash_replayed':False})
write('PACKAGING_ALLOWLIST.json',{'created_utc':now,'mode':'immutable producer-owned textual artifact allowlist; root sole metadata/Git/cache/external action','source':str(S),'textual_paths':[str(p) for p in files]+[str(B/'ARTIFACT_IDENTITIES.json'),str(B/'PACKAGING_ALLOWLIST.json'),str(B/'FINAL_DOCUMENT_IDS.json')],'exclude_binary_copy':True,'binary_copy_count_already':1,'binary_copy_action':'SKIP','root_only_records':'publication/ROOT_SOURCE_CUT*,ROOT_OWN_OBJECT_COPY* remain under root custody; reuse without hash replay','reviewer_paths':['/workspace/scratch/actual-source-regular-slab-precode-review/FINAL_REPORT.md','/workspace/scratch/actual-source-regular-slab-precode-review/final_scope.json'],'unrelated_stage63':'Root-owned EXTRA; not a source62 input/dependency and untouched by producer'})
finalnames=['REPORT.md','HANDOFF.md','PRODUCTION_QUALIFICATION.json','CONTROL_IDS.json','CONTROL_RECEIPT.json','EXECUTION_RECORD_INDEX.json','STREAM_COUNTS.json','ARTIFACT_IDENTITIES.json','READY.json','PACKAGING_ALLOWLIST.json']
write('FINAL_DOCUMENT_IDS.json',{'created_utc':now,'origin':'FIRST identities of newly frozen final documentary outputs; no old artifact/hash/math replay','documents':[first(B/n) if str(B/n) not in known else known[str(B/n)] for n in finalnames],'self_identity':'Not self-hashed; root may take first custody identity when adopting.'})
print(json.dumps({'status':'FROZEN','utc':now,'runs':len(receipts),'streams':2*len(receipts),'files':len(files),'report':str(B/'REPORT.md'),'handoff':str(B/'HANDOFF.md'),'identities':str(B/'ARTIFACT_IDENTITIES.json'),'final_document_ids':str(B/'FINAL_DOCUMENT_IDS.json')},indent=2))
