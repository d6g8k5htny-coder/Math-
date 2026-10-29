"""Root documentary freeze and authorization; no mathematical verification/hashing."""
import json
from datetime import datetime, timezone
from pathlib import Path

U = Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
V = Path('/workspace/scratch/actual-source-saddle-uppercuts-source-review')

def write(path, value):
    assert not path.exists(), str(path)
    path.write_text(json.dumps(value, indent=2) + '\n')

now = datetime.now(timezone.utc).isoformat()
acceptance = {
    'status': 'ROOT_ACCEPTS_FINAL65_TECHNICAL_AND_CUSTODY_PASS',
    'observed_utc': now,
    'review_report': str(V/'technical/FINAL_CUSTODY.md'),
    'review_scope': str(V/'technical-scope.json'),
    'root_personal_reading': str(U/'ROOT_READING.json'),
    'root_additional_full_reading': [
        'Final technical FINAL_CUSTODY.md and technical-scope.json, complete 5127-token exposure already completed before this handoff.',
        'Complete actual label amendment patch and prepublication text-assets code/identity rows, 2615-token exposure already completed before this handoff.'
    ],
    'reading_limits': 'ROOT_READING.json limits preserved. Reviewer broader actual-source/delta/inventory/original-capture coverage is separately attributable. Aggregate manifests/index are bounded/structured, not a claim of literal full repeated JSON reading.',
    'prepublication_text_assets': 'Metadata-only raw candidate .txt aliases and exact three transport-utility copies; first identities already recorded in ROOT_METADATA_TEXT_ASSET_IDS.json. Not attributed to the prior nine-family reviewer scope.',
    'all_math_complete': True,
    'source_cut': 'b2d4c91162d98a1daefb5377bf3e65ef8615dd57',
    'own_object_copy_count': 1,
    'all_further_object_actions': 'SKIP',
    'reuse': 'Completed applicable mathematical and custody evidence is reused. No additional Lean, kernel, source/object SHA, ordinary, mutation, old CI or inventory execution.',
    'process': 'OpenDraft; no Ready/merge; same-family independent credit0; scienceNONE; provider-distinct process separate; 014K403 restriction retained.',
    'global_goal': 'ACTIVE_UNMET; continue authorized research after65 publication.'
}
write(U/'ROOT_REVIEW_ACCEPTANCE.json', acceptance)
bad = {'.olean','.ilean','.c','.o','.so','.a','.pyc','.bin','.pkl','.pickle','.index'}
def frozen(base, prefix):
    rows=[]
    for p in sorted(base.rglob('*')):
        if not p.is_file() or p.suffix in bad or {'.lake','__pycache__','objects','build'} & set(p.relative_to(base).parts):
            continue
        rows.append({'source':str(p),'archive_path':prefix+'/'+str(p.relative_to(base))})
    return rows
rootrows=frozen(U,'raw/root')
# These exact paths close immediately after this target exits. They are explicit,
# not a live tail glob. Packager may act only after root observes wrapper closure.
extra=[U/'ROOT_FROZEN_FILES.json',U/'ROOT_FINALIZATION_GO.json']
for layer in ['entry','outer','worker']:
    b=U/'root-final-go001'/layer
    extra += [b/n for n in ['STARTED.json','RESULT.json','EVENTS.jsonl']]
    extra += [b/('01-'+layer)/n for n in ['INTENT.json','RECEIPT.json','stdout.log','stderr.log']]
seen={x['source'] for x in rootrows}
for p in extra:
    if str(p) not in seen:
        rootrows.append({'source':str(p),'archive_path':'raw/root/'+str(p.relative_to(U))})
rootrows.sort(key=lambda x:x['archive_path'])
reviewrows=frozen(V,'raw/review')
write(U/'ROOT_FROZEN_REVIEW_FILES.json',{'status':'EXPLICIT_FROZEN_FINAL65_REVIEW_FILES','observed_utc':now,'files':reviewrows})
rootrows.append({'source':str(U/'ROOT_FROZEN_REVIEW_FILES.json'),'archive_path':'raw/root/ROOT_FROZEN_REVIEW_FILES.json'})
write(U/'ROOT_FROZEN_FILES.json',{'status':'EXPLICIT_FROZEN_FINAL65_ROOT_TEXT_FILES','observed_utc':now,'files':rootrows,'excluded':'All binaries/cache/build/index; future publication tail excluded. Exact failed raw .bin candidates retained through already-IDed .txt aliases.'})
go={
    'status':'ROOT_GO_FINAL65_ASSEMBLY_AND_ONE_METADATA_ATTEMPT',
    'observed_utc':now,
    'root_review_acceptance':str(U/'ROOT_REVIEW_ACCEPTANCE.json'),
    'root_frozen_files':str(U/'ROOT_FROZEN_FILES.json'),
    'review_frozen_files':str(U/'ROOT_FROZEN_REVIEW_FILES.json'),
    'producer_frozen_allowlist':'/workspace/scratch/actual-source-saddle-uppercuts-construct/PUBLICATION_ALLOWLIST_FINAL.json',
    'producer_allowlist_first_identity':'209389B606631324d3b90f80d7fd2aca1a06d209a39cd59bec7dfc53b7f3cf6eda01f29',
    'qualified_baseline':'ee5b141d5ff41a0a9040256a8025690ec22d7266',
    'source_cut':'b2d4c91162d98a1daefb5377bf3e65ef8615dd57',
    'all_math_complete':True,'final_review_pass':True,'source_cut_committed':True,'own_object_copied_once':True,'immutable_payloads_frozen':True,
    'authority':'Packager may build exact FINAL_INPUTS and perform EXACTLY ONE seven-association metadata attempt AFTER root observes this capture closure and sends GO. No shared apply/Git/external/cache/object-copy authority.',
    'required_reuse':'Reuse ALL existing first IDs at exact immutable paths, producer current cache/snapshots/final documents/self/deferred closure, root runtime/snapshot/assets copies, amended SPEC+proper mirrors, B originals/copies. First hash only previously unrecorded immutable metadata after this GO.',
    'immutable_directories':[],
    'future66':'Four proper root EXTRA documents EXCLUDED65 archive/manifest/registry. No66 source/claim/GO/timer.',
    'hard_terminal':'2026-10-28T23:30:00Z or invocation end; no automatic extension',
    'next_checkpoint':'2026-10-28T23:00:00Z'
}
write(U/'ROOT_FINALIZATION_GO.json',go)
print(json.dumps({'status':go['status'],'root_explicit_files':len(rootrows),'review_explicit_files':len(reviewrows),'observed_utc':now}))
