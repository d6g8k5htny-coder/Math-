import datetime,difflib,hashlib,json,pathlib,time

B=pathlib.Path('/workspace/scratch/actual-source-regular-local-collar-publication')
D=pathlib.Path('/workspace/scratch/actual-source-regular-local-collar-preflight/precode-drafts')
P=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
start=utc(); tick=time.monotonic()
names=['SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR.md','SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR_PLAN.md','SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR_CONTROLS.md']
extra='SOURCE_ACTUAL_REGULAR_LOCAL_COLLAR_CONTENDERS.json'
for name in names+[extra]:
    assert not (P/name).exists(), 'new proper document already exists: '+name
    assert not (B/name).exists(), 'new scratch mirror already exists: '+name
issued=utc()
prefix='''28 October 2026. **Adopted PRECODE66 contract; implementation inactive.**
Root adopted the complete contracts after the completed full draft/design
readings and independent PASS_DESIGN, plus full actual precision-delta and
independent delta review. Those readings and qualified mathematics are
reused. The accompanying adoption record gives the actual UTC.
This adoption creates documents and documentary identities only: no66
source/helper proof text, harness, Lean execution, object, author seat,
external claim, GO, implementation role or timer is authorized. The draft
author and document reviewers are not66 proof authors by this adoption.
Same-family technical credit0; scientific effect NONE.

Read the companion SPEC, PLAN and CONTROLS. Dated local adoption evidence
is retained at `/workspace/scratch/actual-source-regular-local-collar-preflight/REPORT.md`
and under `/workspace/scratch/actual-source-regular-local-collar-source-review/`
in REPORT.md, PRECODE_REVIEW.md and PRECODE_DELTA_REVIEW.md. Actual draft
history and the full precision patch remain in the preflight/precode-drafts
directory. These are retained local evidence locators, not a claim that
their files are already published. Draft-relative REPORT citations are
corrected in these proper documents BEFORE their first identities.
Qualified/published64 and its all-four-CI evidence are reused;65 is active
separate work. Neither is a mathematical66 dependency. These proper66
documents await later normal publication as explicit extras; they are
excluded from65 source/evidence/registry/manifest qualification.

'''
documents=[]; patches=[]
(B/'adoption-patches').mkdir(exist_ok=False)
(B/'drafts-before-adoption').mkdir(exist_ok=False)
for name in names:
    original=(D/name).read_text()
    title=original.splitlines()[0].replace('DRAFT66','SPEC66' if name==names[0] else ('PLAN66' if name==names[1] else 'CONTROLS66'))
    if name==names[0]: title='# SPEC66 — actual regular-point quotient collar'
    if name==names[1]: title='# PLAN66 — actual regular-point quotient collar'
    if name==names[2]: title='# CONTROLS66 — actual regular collar and one omitted-derivative mutation'
    body=original[original.index('\n## '):].lstrip('\n')
    body=body.replace('`../REPORT.md`','`/workspace/scratch/actual-source-regular-local-collar-preflight/REPORT.md`')
    proper=title+'\n\n'+prefix+body
    payload=proper.encode()
    sha=hashlib.sha256(payload).hexdigest()
    (B/'drafts-before-adoption'/name).write_text(original)
    patch=''.join(difflib.unified_diff(original.splitlines(True),proper.splitlines(True),fromfile='draft/'+name,tofile='proper/'+name))
    patchpath=B/'adoption-patches'/(name+'.patch');patchpath.write_text(patch)
    (P/name).write_bytes(payload);(B/name).write_bytes(payload)
    documents.append({'path':str(P/name),'mirror':str(B/name),'bytes':len(payload),'sha256':sha,'identity_origin':'NEW proper documentary payload FIRST identity calculated ONCE; mirror is exact byte-copy, ID reused','source_draft':str(D/name),'full_patch':str(patchpath)})
    patches.append(str(patchpath))
contenders={'status':'ADOPTED_LOCAL_PRECODE66_ONLY_PENDING_NORMAL_PUBLICATION','adopted_utc':issued,'module':'SourceActualRegularLocalCollar','namespace':'I4SourceActualRegularLocalCollar','sole_public_Prop':'actualSource_quotient_regular_local_collar','public_data_global_instances':0,'implementation_authority':False,'source_role_claim_GO_timer':False,'active_other_unit':{'stage':65,'creator':6480523901,'next_checkpoint':'2026-10-28T21:45:00Z','hard_terminal':'2026-10-28T23:30:00Z or invocationend/noautoextension'},'qualified_current_head_reused':'ee5b141d5ff41a0a9040256a8025690ec22d7266','qualified64_CI':'All4SUCCESS firstpersonallyobserved20:59:36.597639; no oldpoll/replay','future66_dependency':'Only old qualified public actual-field/IFT/AddCircle interfaces, no64/65 mathematical dependency','future_source_claim':'Fresh scope reconciliation/personal onboarding/publishedpropercontracts/fullcontrols/context/ACK/rootGO required later; no seat by adoption','publication':'Explicit root-only extra with later65 publication, excluded65manifest/archive/registry','review':'Completed full3draftdesignPASS+fullactualprecisiondeltaPASS reused; samefamily0/scienceNONE','owner_guidance':'Completed applicable verification reused acrossagents/sessions/heads/handoffs; new checks onlyactualchange/defect/uncoveredobligation/affectedscope. Provider process separate.'}
payload=(json.dumps(contenders,indent=2)+'\n').encode();sha=hashlib.sha256(payload).hexdigest()
(P/extra).write_bytes(payload);(B/extra).write_bytes(payload)
documents.append({'path':str(P/extra),'mirror':str(B/extra),'bytes':len(payload),'sha256':sha,'identity_origin':'NEW proper documentary payload FIRST identity calculated ONCE; exact mirror ID reused'})
record={'status':'ROOT_ADOPTED_PROPER66_DOCUMENTS_ONLY_IMPLEMENTATION_INACTIVE','adopted_utc':issued,'generation_started_utc':start,'generation_ended_utc':utc(),'elapsed_seconds':time.monotonic()-tick,'documents':documents,'full_adoption_patches':patches,'root_reading':'Completed FULLpreflight5216+indep2678; FULL3draftcoverage via initialaggregate8492+indep2107 and onlytruncatedPLANtail/CONTROLSheader recovery921 at20:37:47; ENTIREactualprecisionpatch+report4594 and FULLindependentdelta review1278. Reused oldmathematics, no repeatverification.','review_paths':['/workspace/scratch/actual-source-regular-local-collar-source-review/REPORT.md','/workspace/scratch/actual-source-regular-local-collar-source-review/PRECODE_REVIEW.md','/workspace/scratch/actual-source-regular-local-collar-source-review/PRECODE_DELTA_REVIEW.md'],'citation_correction_before_FIRST_ids':True,'source_helper_harness_Lean_object_claim_GO_role_timer_authorized':False,'publication_pending':True,'excluded65_manifest_archive_registry':True,'checks_or_old_hashes_replayed':0,'script_IDs':'New runtime script FIRST identities and immutable pre-worker copies recorded by record_worker66.py, never recomputed here.','identity_record_self':'Not self-hashed/recursive; any later necessary first identity must be calculated once and cached.'}
(B/'PRECODE66_IDENTITIES.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':record['status'],'adopted_utc':issued,'documents':documents,'record':str(B/'PRECODE66_IDENTITIES.json')}))
