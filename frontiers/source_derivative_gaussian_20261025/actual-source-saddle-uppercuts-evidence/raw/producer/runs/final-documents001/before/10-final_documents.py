import collections,datetime,hashlib,json,pathlib

BASE=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
PUB=pathlib.Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
PROJECT=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
ACTIVE='final-documents001'
cache=json.loads((BASE/'FIRST_ID_CACHE.json').read_text())
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
    p=pathlib.Path(p); st=p.stat(); marker=[st.st_size,st.st_mtime_ns]
    old=cache.get(str(p))
    if old and old.get('marker')==marker: return old
    row={'path':str(p),'bytes':st.st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'marker':marker,'first_observed_utc':utc(),'origin':'FIRST new actual documentary payload/version identity, calculated once'}
    cache[str(p)]=row
    return row
def known_copy(dst,row,source):
    st=dst.stat(); out={**row,'path':str(dst),'marker':[st.st_size,st.st_mtime_ns],
      'origin':'known exact byte-copy identity reused','copied_from':str(source)}
    cache[str(dst)]=out
    return out
def put(name,data):
    p=BASE/name; assert not p.exists(), 'Never regenerate frozen final output '+str(p)
    p.write_text(data if isinstance(data,str) else json.dumps(data,indent=2)+'\n')
    return identity(p)

# Known root-owned complete controls copy: reuse the proper FIRST identity.
cp=BASE/'CONTROL_CONTRACT.md'; st=cp.stat()
cache[str(cp)]={'path':str(cp),'bytes':13258,'sha256':'7672542a7bb8bfeb2344770dbc0ce6e7c12c96cbe1b380fec700535419b9c6c8',
 'marker':[st.st_size,st.st_mtime_ns],'origin':'Root proper65 complete controls FIRST identity reused; exact preGO copy',
 'binding_reference':str(PUB/'ROOT_CONTROL_CONTRACT_COPY.json')}
# Reuse the actual historical runner002 row for its retained exact copy.
historical=json.loads((BASE/'runs/runner-amend001/receipt.json').read_text())
rp=BASE/'runner/record_run.py'; copy=BASE/'context/record_run.002.py'
known_copy(copy,historical['after'][str(rp)],rp)

receipts=[]
for p in sorted((BASE/'runs').glob('*/receipt.json')):
    receipts.append((p,json.loads(p.read_text())))
counts=dict(collections.Counter(r['scope_kind'] for _,r in receipts))
math=[r for _,r in receipts if r['scope_kind']=='math']
assert len(math)==15
kernel=[r for r in math if r['label']=='kernel001']; assert len(kernel)==1 and kernel[0]['exit_code']==0
negative=next(r for r in math if r['label']=='false-control001')
out=(BASE/'runs/false-control001/stdout.log').read_bytes()
err=(BASE/'runs/false-control001/stderr.log').read_bytes()
assert negative['exit_code']==1 and out.decode().count('⊢ False')==1 and len(err)==0
prod=json.loads((BASE/'FINAL_SOURCE_PRE_KERNEL_IDS.json').read_text())
precontrol=json.loads((BASE/'CONTROL_IDS_PRE_NEGATIVE.json').read_text())
pinv=json.loads((BASE/'INVENTORY_CLASSIFIED.json').read_text())
oinv=json.loads((BASE/'CONTROLS_INVENTORY_CLASSIFIED.json').read_text())
root_actions={}
for name in ['ROOT_SOURCE_CUT.json','ROOT_OWN_OBJECT_COPY.json']:
    p=PUB/name
    root_actions[name]={'path':str(p),'state':'ACTUAL RECORD PRESENT' if p.exists() else 'PENDING ROOT ONLY',
      'record':json.loads(p.read_text()) if p.exists() else None}
control=put('CONTROL_IDS.json',{'status':'PASS ordinary strict plus separate ALL-owned/std3, then sole expected negative',
 'pre_negative_immutable_record':str(BASE/'CONTROL_IDS_PRE_NEGATIVE.json'),
 'ordinary_source':precontrol['ordinary_source'],'ordinary_object':precontrol['ordinary_object'],
 'ordinary_final_snapshot':precontrol['ordinary_final_snapshot'],'ordinary_owned_constants':oinv['owned_constants'],
 'ordinary_classification_counts':oinv['classification_counts'],
 'ordinary_strict_receipt':str(BASE/'runs/controls003/receipt.json'),
 'ordinary_inventory_receipt':str(BASE/'runs/ordinary-inventory001/receipt.json'),
 'ordinary_named_kernels':0,'sole_negative_harness':precontrol['sole_harness'],
 'sole_negative_harness_snapshot':precontrol['sole_harness_snapshot'],
 'negative_receipt':str(BASE/'runs/false-control001/receipt.json'),
 'negative_exit':1,'negative_stdout_bytes':len(out),'negative_stderr_bytes':0,'unsolved_False_count':1,
 'negative_worker_times':{k:negative[k] for k in ['start_utc','end_utc','elapsed_seconds']},
 'mutation':'ONLY eps>0 to eps>=0. Same chosen rho/phi/source/field/CLOSED cut and upper bound. Closed assertion has no mutation premise/axiom/parameter.',
 'counterproof':'Actual full inverse vertical target path, every-time target/source/closed-zero-cut membership, actual q midpoint and negative endpoint coordinate product. Structural fields only; no production upperbranch or inherited lowerPC shortcut.'})
finalids=put('FINAL_IDS.json',{'status':'ALL MATHEMATICAL OBLIGATIONS PASS; final documentary/root publication process separate',
 'source':prod['source'],'source_snapshot':prod['source_snapshot'],'own_object':prod['own_object'],
 'source_lines':prod['source_lines'],'sole_public_Prop':prod['public_theorem'],'public_data_global_instances':0,
 'public64_calls':1,'production_owned_constants':pinv['owned_constants'],
 'production_classification_counts':pinv['classification_counts'],
 'production_strict_receipt':prod['strict_pass_receipt'],'production_inventory_receipt':str(BASE/'runs/inventory001/receipt.json'),
 'production_named_kernel_count':1,'production_kernel_receipt':str(BASE/'runs/kernel001/receipt.json'),
 'historical_pre_kernel_zero_record_preserved':str(BASE/'FINAL_SOURCE_PRE_KERNEL_IDS.json'),
 'ordinary_control_ids':control,'root_only_sourcecut_and_copy':root_actions,
 'producer_canonical_copies':0,'all_further_old_copies':'SKIP','science':'NONE','same_family_credit':0})

index=[]
for receipt_path,r in receipts:
    layers={}
    layers['worker']={k:r[k] for k in ['start_utc','end_utc','elapsed_seconds','exit_code']}
    layers['worker']['receipt']=identity(receipt_path)
    layers['worker']['streams']=[identity(receipt_path.parent/'stdout.log'),identity(receipt_path.parent/'stderr.log')]
    for layer in ['outer','entry']:
        p=BASE/'outer'/r['label']/(layer+'.receipt.json'); v=json.loads(p.read_text())
        layers[layer]={k:v[k] for k in ['start_utc','end_utc','elapsed_seconds','exit_code']}
        layers[layer]['receipt']=identity(p)
        layers[layer]['streams']=[identity(pathlib.Path(v['stdout'])),identity(pathlib.Path(v['stderr']))]
    relevant={}
    for key in [str(PROJECT/'SourceActualSaddleUppercuts.lean'),str(BASE/'build/SourceActualSaddleUppercuts.olean'),
                str(BASE/'SaddleUppercutsControls.lean'),str(BASE/'build/SaddleUppercutsControls.olean'),str(BASE/'CONTEXT.md')]:
        relevant[key]={'before':r['before'].get(key),'after':r['after'].get(key),
          'actual_before_snapshot':r['before_snapshots'].get(key)}
    index.append({'label':r['label'],'scope_kind':r['scope_kind'],'command_argv':r['command_argv'],'cwd':r['cwd'],
      'layers':layers,'source_object_context_bindings':relevant,
      'complete_custody_receipt':str(receipt_path),'all_other_input_versions_and_full_actual_snapshots':'See unchanged complete original receipt and immutable before directory'})
execution=put('EXECUTION_RECORD_INDEX.json',{'closed_worker_counts_at_generation':counts,
 'mathematical_runs':15,'mathematical_original_worker_streams':30,
 'all_closed_runs':len(index),'all_closed_original_worker_outer_entry_streams':len(index)*6,
 'active_documentary_run_excluded_until_actual_closure':ACTIVE,
 'planned_additive_closure':'EXECUTION_RECORD_INDEX_ADDENDUM.json and FINAL_READY.json; no generator replay or recursive self-identity',
 'runs':index})

report=f'''# Stage65 producer report

The sole public Prop theorem `{prod['public_theorem']}` is proved for the original positive-period smooth sample and actual physical critical point with full complementary inertia1, without a global Morse premise. A single PUBLIC64 call supplies one unchanged rho/phi for every ambient open O. Its full closed lower-trace family is retained unchanged. The same chart has uniform closed uppercuts for 0<eps<rho²/4, with two nonempty path-connected sign branches, exact disjoint union and the stated JoinedIn sign test.

The production source is {prod['source_lines']} lines/{prod['source']['bytes']} bytes, SHA256 {prod['source']['sha256']}. Own object {prod['own_object']['bytes']} bytes, SHA256 {prod['own_object']['sha256']}. Strict fixtures004 passed. All {pinv['owned_constants']} exact module-owned constants, including private data/Prop bundles/generated and the separately classified foreign-generated declaration, passed recursive standard3 axiom qualification. Exactly ONE final production named-module kernel passed. Historical PRE_KERNEL0 remains an immutable historical observation; FINAL_IDS records the actual count1. No production check is repeated.

Actual finite-source controls use the literal period2 sample cos(pi*x)+2cos(pi*y). Fresh producer derivations prove the actual field/physical derivatives/full complementary Hessian inertia at both saddles and seam, the projected PHYSICAL ball1/8 neighborhood, quotient seam equality, all three new-theorem consumers, and exact cutoff equality eps*=rho²/16 at inverse coordinates ±rho/4. No old64 private geometry/fixture/ordinary body or control binary was copied. One complete B geometry original was frozen, assigned FIRST identities and integrated ONCE; all actual producer amendments are retained.

The separate ordinary source is {precontrol['ordinary_lines']} lines/{precontrol['ordinary_source']['bytes']} bytes, SHA256 {precontrol['ordinary_source']['sha256']}; ordinary object {precontrol['ordinary_object']['bytes']} bytes, SHA256 {precontrol['ordinary_object']['sha256']}. Controls003 passed before the separate {oinv['owned_constants']}-constant ordinary inventory/std3 PASS. No ordinary named kernel ran. The independent structural inverse vertical path stays in the actual CLOSED zero cut at every time, passes through actual q at its midpoint, and joins opposite-sign endpoints. It refutes only eps>0→eps>=0 for the SAME chosen phi/source/rho/field/CLOSED cut/upper bound. The sole closed no-premise assertion harness was frozen before its ONE execution: expected exit1, {len(out)}-byte stdout containing ONE unsolved False, empty stderr. CONTROL_IDS binds the passing ordinary source/object and ordered receipts.

There are 15 mathematical calls: 7 successful qualification calls, 7 retained development failures and the sole intended negative failure. Every original mathematical worker stdout/stderr is preserved, and worker/outer/entry each have their own command/cwd/start/end/elapsed/exit and separate original streams. At this generator's start there were {counts.get('documentary',0)} preceding closed documentary workers; its own actual closure and final closure-worker records are covered additively. EXECUTION_RECORD_INDEX keeps all complete original receipt references and distinguishes all three timing layers. No worker time is replaced by entry-completion time.

All completed applicable64 verification, object identity, canonical copy and hosted results were reused. Existing proper controls were copied before GO; contexts001–004, complete actual patches, authentic helper ACK/release/start/freeze observations and initial runner versions are retained. Every producer important worker from the first context freeze has full prospective worker/outer/entry capture. Static apply_patch writes and read-only public-API/path lookups are actual tool-history operations, without invented OS timestamps or split-stream claims. They are not Lean probes. Known complete copies/snapshots reuse existing IDs; new versions receive FIRST IDs once. Root-owned earlier publication capture disclosures are separate and are not upgraded by producer capture claims.

Root alone owns sourcecut, shared metadata/cache, eligible canonical object copy, Git and external publication. Current root sourcecut/copy record states are recorded honestly in FINAL_IDS; if pending, a later ROOT_CUT_COPY_ADDENDUM may bind the actual records without rerunning mathematics or this generator. Producer canonical copies0. Future66 root-owned EXTRAs are excluded from this source/archive/manifest/registry scope. Provider-distinct process is separate from established math; same-family credit0/scienceNONE. The larger research goal remains active and unmet beyond this local result.

Final custody: FINAL_IDS.json, CONTROL_IDS.json, EXECUTION_RECORD_INDEX.json, ARTIFACT_IDENTITIES.json, HISTORICAL_ID_BINDINGS.json, FINAL_DOCUMENT_IDS.json, publication allowlist and actual additive closure. Root final reading and independent final custody review precede root-only FINAL_GO/metadata/publication.
'''
put('REPORT.md',report)
put('HANDOFF.md',f'''# Stage65 handoff

All mathematical work is complete and reusable. Do not recompile/reinventory/re-kernel/re-control/re-negative/re-hash unchanged material. The specific successful receipts are fixtures004, inventory001, kernel001 (EXACTLY ONE production kernel), controls003, ordinary-inventory001 and the sole intended false-control001. Full helper geometry002 and generic joins002 evidence is retained; no partial/helper/ordinary kernel exists.

Frozen source {prod['source']['bytes']}B/{prod['source']['sha256']}, own object {prod['own_object']['bytes']}B/{prod['own_object']['sha256']}. Exact119 production and123 ordinary declarations are exhaustively classified/std3-qualified. One production public Prop/no public data or global instance. Own source/ordinary body are frozen; mathematical review has no findings.

Root only: make/bind the new source-only cut and copy ONLY the eligible new own object ONCE if not already completed; record actual existing state, then all further copies SKIP. Producer performed no canonical copy/Git/shared/cache/external action. No old/helper/ordinary/ilean promotion. Root records are referenced by FINAL_IDS and may be attached additively after this generator; pending process does not erase math.

Read final REPORT/CONTROL_IDS/FINAL_IDS/index/bindings/allowlist and actual final generator plus post-run closure receipts/streams; create root final-reading record, obtain final nonauthor custody review, then root-only explicit FINAL_GO to the packager. Reuse all existing FIRST IDs via FIRST_ID_CACHE/ARTIFACT_IDENTITIES; final closure's own closed outer/entry files need root first adoption IDs rather than recursive self-hashing. Future66 EXTRAs are outside65 mathematical archive/manifest/registry. No further producer mathematical execution is authorized absent a concrete new finding.

The source derives one PUBLIC64 chart internally, retains all same-chart lower traces unchanged, adds uniform positive CLOSED upper branches. Ordinary counterproof uses only structural fields plus the complete inverse vertical path; no inherited lowerPC or production upperbranch shortcut. The sole mutation is eps>0→eps>=0, closed no-premise assertion, ordinary inventory before negative. Root GO/checkpoint/hard bound remain21:20/historical-next21:45 and23:30UTC28Oct/end, no autoextension; current later native checkpoint state is root-owned. Original downstream research remains ACTIVE_UNMET.
''')

# Collect only actual owned textual artifacts. No old modules, objects or future66 EXTRAs.
def eligible(p):
    if not p.is_file(): return False
    if p==BASE/'FIRST_ID_CACHE.json': return False
    if p.suffix in {'.olean','.ilean','.pyc'} or '__pycache__' in p.parts: return False
    if '/runs/'+ACTIVE+'/' in str(p) or '/outer/'+ACTIVE+'/' in str(p): return False
    return True
paths=[PROJECT/'SourceActualSaddleUppercuts.lean']+sorted(p for p in BASE.rglob('*') if eligible(p))
artifact_rows=[identity(p) for p in paths]
artifact=put('ARTIFACT_IDENTITIES.json',{'scope':'Only source65 and actual producer-owned textual custody, no binaries/old modules/future66 EXTRAs',
 'generation_utc':utc(),'artifacts':artifact_rows,
 'self_and_final_closure':'Known new final document IDs recorded in FINAL_DOCUMENT_IDS; active final worker captured additively after closure, no recursive self hash'})

available=collections.defaultdict(list)
for path,row in cache.items():
    p=pathlib.Path(path)
    if p.is_file() and row.get('marker')==[p.stat().st_size,p.stat().st_mtime_ns]:
        available[(row['bytes'],row['sha256'])].append(path)
bindings=[]
for receipt_path,r in receipts:
    for phase in ['before','after']:
        for original,row in r[phase].items():
            if not row: continue
            candidates=available[(row['bytes'],row['sha256'])]
            immutable=[p for p in candidates if any(t in p for t in ['/before/','/frozen/','/helper-originals/','/context/'])]
            bindings.append({'receipt':str(receipt_path),'phase':phase,'logical_original_path':original,
              'bytes':row['bytes'],'sha256':row['sha256'],
              'actual_pre_run_snapshot':r['before_snapshots'].get(original) if phase=='before' else None,
              'available_immutable_snapshot_paths':immutable,
              'available_active_paths':[p for p in candidates if p not in immutable],
              'preserved_bytes_available':bool(candidates),
              'binary_archive_scope':'Object bytes may be preserved in actual local before snapshots; no binary promotion/archive claim. Text source/ID bindings are archived.'})
binding=put('HISTORICAL_ID_BINDINGS.json',{'scope':'Every actual receipt before/after source/object/context/runner/draft identity bound to actual retained snapshot or active bytes; no invented historical bytes',
 'bindings':bindings,'binary_promotion':'NONE by producer; root only eligible new final own object ONCE'})
main_ids=[identity(BASE/n) for n in ['REPORT.md','HANDOFF.md','CONTROL_IDS.json','FINAL_IDS.json','EXECUTION_RECORD_INDEX.json','ARTIFACT_IDENTITIES.json','HISTORICAL_ID_BINDINGS.json']]
put('FINAL_DOCUMENT_IDS_INITIAL.json',{'first_new_document_ids':main_ids,'known_ids_reused':True,
 'current_generator_closed_receipt':'pending until actual outer+entry close; additive closure next',
 'no_repeated_calculation':'Existing matching path/version cache reused; complete known copies reuse source IDs. No unchanged math/object hashes recomputed.'})
allow=sorted(set(str(p) for p in paths)|{str(BASE/n) for n in ['ARTIFACT_IDENTITIES.json','HISTORICAL_ID_BINDINGS.json','FINAL_DOCUMENT_IDS_INITIAL.json','PUBLICATION_ALLOWLIST_INITIAL.json']})
put('PUBLICATION_ALLOWLIST_INITIAL.json',{'paths':allow,'scope':'Frozen text65 only; no shared config/old/future66/binaries/mutable cache',
 'closure_required':'Actual final-documents001 receipt/streams plus final closure outputs are added after this worker closes'})
(BASE/'FIRST_ID_CACHE.json').write_text(json.dumps(cache,indent=2)+'\n')
print(json.dumps({'status':'FINAL DOCUMENTS WRITTEN; actual post-run closure next','artifact_rows':len(artifact_rows),
 'historical_binding_rows':len(bindings),'allowlist_paths':len(allow),'closed_runs':counts,'math_runs':15,
 'root_sourcecut_copy':{k:v['state'] for k,v in root_actions.items()}}))
