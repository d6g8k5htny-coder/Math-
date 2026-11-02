#!/usr/bin/env python3
"""Bind frozen final65 metadata inputs; no digest/proof/Git/shared action."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, json, os

R=Path('/workspace/scratch/actual-source-saddle-uppercuts-packaging')
P=Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
U=Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
V=Path('/workspace/scratch/actual-source-saddle-uppercuts-source-review')
B=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')

def read(p): return json.loads(Path(p).read_text())
def put(p,d):
    with Path(p).open('x') as f:
        json.dump(d,f,indent=2,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())
def frozen_rows(p,base,prefix):
    d=read(p)
    rows=d if isinstance(d,list) else d.get('files',d.get('paths',d.get('immutable_files')))
    if not isinstance(rows,list): raise RuntimeError('Explicit frozen file list schema '+str(p))
    result=[]
    for x in rows:
        source=Path(x if isinstance(x,str) else x.get('source',x.get('path')))
        if not source.is_absolute(): source=base/source
        rel=(x.get('archive_path') if isinstance(x,dict) else None) or prefix+'/'+str(source.relative_to(base))
        result.append({'source':str(source),'archive_path':rel})
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root-list',required=True);ap.add_argument('--review-list',required=True)
    a=ap.parse_args()
    go_path=U/'ROOT_FINALIZATION_GO.json';go=read(go_path)
    if go['status']!='ROOT_GO_FINAL65_ASSEMBLY_AND_ONE_METADATA_ATTEMPT': raise RuntimeError('No actual root GO')
    allow=read(P/'PUBLICATION_ALLOWLIST_FINAL.json')['paths']
    if len(allow)!=1786: raise RuntimeError('Frozen producer path count changed')
    c=read(R/'FINAL_INPUTS.schema.json')
    for k in ['required_status_after_GO','existing_identity_entry_shape','production_helper_entry_shape']:c.pop(k,None)
    c.update(status=go['status'],root_finalization_go=str(go_path),all_math_complete=True,
             final_review_pass=True,source_cut_committed=True,own_object_copied_once=True,immutable_payloads_frozen=True,
             source_cut='b2d4c91162d98a1daefb5377bf3e65ef8615dd57',source_cut_parent=c['qualified_baseline'],
             immutable_directories=[],excluded_artifact_directories=[])
    fi=read(P/'FINAL_IDS.json');ci=read(P/'CONTROL_IDS.json');review=read(V/'technical-scope.json')
    c['source_identity']={k:fi['source'][k] for k in ['bytes','sha256']}
    c['eligible_object_identity']={k:fi['own_object'][k] for k in ['bytes','sha256']}
    c['root_object_copy_record']=str(U/'ROOT_OWN_OBJECT_COPY.json')
    c['root_reading_record']=str(U/'ROOT_READING.json')
    c['root_reading_summary']='ROOT_READING.json plus ROOT_REVIEW_ACCEPTANCE.json retain exact personal FULL/BOUNDED limits. Root FULL contract/context changes/B five originals/final ordinary and closedFalse/all named final docs/final review+scope/root metadata code and selected actual captures; NOT whole769 production/ALL119 raw/std3/all15 full mathematical receipt fields/large aggregate manifests/all69 grouped paths/all1786 allowlist. Broader source/inventory/receipt/path coverage belongs to nonauthor technical reviewer; completed applicable evidence reused. New prepublication text assets and exact native transfer utilities read by root; metadata-only and after final technical review.'
    c['reviewer_reading_summary']='Final technical FINAL_CUSTODY.md and technical-scope.json PASS/no findings. FULL actual production via full initial source plus actual deltas, ALL119 classified/std3 raw, final ordinary via initial+actual deltas/ALL123 raw, sole closedFalse, all40 actual worker/outer/entry receipts and240 streams, all69 distinct historical version/path groups, all1786 grouped allowlist paths; large aggregate execution index/artifact manifests STRUCTURED/BOUNDED, not literal complete11MB history or all1773 markers. Root first9 native families/21 internalGit/96 streams FULL; tenth prepublication text-assets family is root-owned later metadata scope. No independent scientific/provider-distinct credit.'
    files=[]
    for value in allow:
        src=Path(value)
        if src==B/'SourceActualSaddleUppercuts.lean':rel='raw/producer/SourceActualSaddleUppercuts.lean'
        elif P in src.parents:rel='raw/producer/'+str(src.relative_to(P))
        else:rel='raw/helper-original/'+src.name
        files.append({'source':str(src),'archive_path':rel})
    files.extend(frozen_rows(a.root_list,U,'raw/root'))
    files.extend(frozen_rows(a.review_list,V,'raw/review'))
    c['immutable_files']=files
    paths={x['source'] for x in files}
    runs=sorted(x for x in allow if Path(x).name=='receipt.json' and Path(x).parent.parent==P/'runs')
    if len(runs)!=40:raise RuntimeError('Expected actual frozen40 producer receipts')
    c['run_records']=runs
    c['qualification']={'strict':fi['production_strict_receipt'],'inventory':fi['production_inventory_receipt'],
        'kernel':fi['production_kernel_receipt'],'positive_controls':ci['ordinary_strict_receipt'],
        'ordinary_inventory':ci['ordinary_inventory_receipt'],'negative':ci['negative_receipt']}
    c['inventory_archive_path']='raw/producer/INVENTORY_CLASSIFIED.json'
    c['inventory_summary']={'all_module_index_owned_constants':fi['production_owned_constants'],'authored_public_Prop':1,
        'authored_public_data':0,'counts':fi['production_classification_counts'],
        'foreign_generated_names':['Lifetime.IsCriticalPoint.eq_1'],'foreign_generated_count':1,
        'standard_three_guard':'PASS actual final ALL119 module-index-owned standard-three inventory; completed evidence reused'}
    c['ordinary_inventory_summary']={'all_module_index_owned_constants':ci['ordinary_owned_constants'],
        'counts':ci['ordinary_classification_counts'],'foreign_generated_names':[],
        'standard_three_guard':'PASS actual separately qualified ALL123 ordinary module-index-owned standard-three inventory; no ordinary named kernel'}
    c['production_helper_integrations']=[{'key':'ONE complete private finite-Pi2 closed-uppercut geometry TEXT original',
        'record_path':'raw/producer/B_ORIGINAL_CUSTODY.json','integration_count':1,'helper_executions':0,
        'original_bytes':10572,'original_sha256':'ce44f946a930b55a27a424c55b126a0e8a2262bdc25ab2844b9e7b3dc1a02f6f',
        'context':'Effective004 accepted/released before text; helper five original files retained, ONE integration/FULL actual producer amendments retained'}]
    c['ordinary_controls_custody'].update(producer_controls_original_snapshot='raw/producer/frozen/Controls.INITIAL.lean',
        record_path='raw/producer/CONTROL_IDS.json; actual initial immutable snapshot and FULL amendments in explicit allowlist')
    c['review_report_archive_path']='raw/review/technical/FINAL_CUSTODY.md'
    c['negative_binding'].update(imports='Already passed SaddleUppercutsControls object ONLY plus accepted public dependencies',
        counterproof_in_passed_controls=True,exactly_one_intendedFalse=True,
        ordinary_controls_object_identity={k:ci['ordinary_object'][k] for k in ['bytes','sha256']},
        negative_harness_identity={k:ci['sole_negative_harness'][k] for k in ['bytes','sha256']},
        stdout_bytes=ci['negative_stdout_bytes'],stderr_bytes=ci['negative_stderr_bytes'])
    c['curated_producer_files']=['REPORT.md','HANDOFF.md','FINAL_IDS.json','CONTROL_IDS.json','FINAL_READY.json','FINAL_DOCUMENT_IDS.json']
    c['root_cut_transport']='ROOT_SOURCE_CUT.json actual native b2d4c91162d98a1daefb5377bf3e65ef8615dd57, parent qualified ee5, local branch CAS/source index sync and ONLY own copy complete. Raw exact PUBLIC unauthenticated fetch retained native -0500 headers. Both failed JSON-serialization candidates preserved before any movement. No remote ref publication claimed before root final metadata native normal-FF.'
    # Existing first IDs, bound only to their actual current immutable version.
    seeds={}
    def seed(path,rec,marker_check=False):
        p=Path(path)
        if not p.is_file() or 'bytes' not in rec or 'sha256' not in rec:return
        st=p.stat()
        if marker_check and rec.get('marker') and list(rec['marker'])!=[st.st_size,st.st_mtime_ns]:return
        if st.st_size!=rec['bytes']:raise RuntimeError('Known identity size mismatch '+str(p))
        row={'source':str(p),'bytes':rec['bytes'],'sha256':rec['sha256']}
        old=seeds.get(str(p))
        if old and old!=row:raise RuntimeError('Contradictory current identity '+str(p))
        seeds[str(p)]=row
    cache=read(P/'FIRST_ID_CACHE.json')
    for path,rec in cache.items():seed(path,rec,True)
    for name,key in [('ARTIFACT_IDENTITIES.json','artifacts'),('ARTIFACT_IDENTITIES_ADDENDUM.json','actual_new_rows'),('FINAL_DOCUMENT_IDS.json','first_or_reused_final_document_ids')]:
        for rec in read(P/name)[key]:seed(rec['path'],rec,True)
    adoption=read(U/'ROOT_PRODUCER_CLOSURE_ADOPTION.json')
    for rec in adoption['rows']+[adoption['FINAL_DOCUMENT_IDS_self_reused'],adoption['cut_copy_addendum']]:seed(rec['path'],rec)
    for value in runs:
        d=read(value)
        for canonical,snapshot in d['before_snapshots'].items():seed(snapshot,d['before'][canonical])
        for rec in d['streams'].values():seed(rec['path'],rec)
    for name in ['ROOT_NATIVE_RUNTIME_FIRST_IDS.json','ROOT_NATIVE_MESSAGE_AMENDMENT_FIRST_IDS.json']:
        for rec in read(U/name)['rows']:
            seed(rec['path'],rec);seed(rec['immutable_exact_copy'],rec)
    for name in ['public-native-source-cut001','producer-closure-adoption001','prepublication-text-assets001']:
        rec=read(U/name/'action/SCRIPT_FIRST_ID.json');seed(rec['path'],rec);seed(rec['immutable_exact_copy'],rec)
    for rec in read(U/'ROOT_METADATA_TEXT_ASSET_IDS.json')['rows']:
        seed(rec['source'],rec);seed(rec['destination'],rec)
    for rec in read(U/'GO65_RUNTIME_FIRST_IDS.json'):seed(rec['path'],rec)
    for rec in read(U/'PRECODE65_GENERATION_001.json')['generator_config_first_IDs']:seed(rec['path'],rec)
    rec=read(U/'PRECODE65_GENERATION_002.json')['newscriptfirstID'];seed(rec['path'],rec)
    pre=read(U/'PRECODE65_IDENTITIES.json')['proper_documents'];amend=read(U/'PRECODE65_CITATION_AMENDMENT_001.json')
    for rec in pre:
        current=amend['new_SPEC'] if Path(rec['path']).name=='SOURCE_ACTUAL_SADDLE_UPPERCUTS.md' else rec
        seed(current['path'],current);seed(current['scratch_copy'],current)
        if current is not rec:seed(amend['prior_payload'],rec)
    controls=read(U/'ROOT_CONTROL_CONTRACT_COPY.json')
    seed(controls['destination'],{'bytes':controls['bytes'],'sha256':controls['sha256_reused']})
    for pair in read(P/'B_ORIGINAL_CUSTODY.json')['originals']:
        for rec in pair.values():seed(rec['path'],rec)
    # Optional root-frozen known identity seeds are data, never live-directory discovery.
    for name in ['existing_file_identities','known_identity_rows']:
        for rec in go.get(name,[]):seed(rec.get('source',rec.get('path')),rec)
    c['existing_file_identities']=[rec for path,rec in sorted(seeds.items()) if path in paths or Path(path).parent==B]
    extra=['prepare_final_inputs.py','INPUT_GENERATION_RECORD.json',
           'preparation-history/root-label-fixes-001/AMENDMENT.md',
           'preparation-history/root-label-fixes-001/FINAL_INPUTS.schema.json.ORIGINAL',
           'preparation-history/root-label-fixes-001/finalize_metadata.py.ORIGINAL',
           'preparation-history/root-label-fixes-001/root-label-fixes-001.patch',
           'preparation-history/root-label-fixes-002/run_finalization.py.ORIGINAL',
           'preparation-history/root-label-fixes-002/root-label-fixes-002.patch',
           'preparation-history/root-label-fixes-002/AMENDMENT.md']
    for layer in ['entry','outer','worker']:
        for rel in ['STARTED.json','EVENTS.jsonl','RESULT.json',f'01-{layer}/INTENT.json',f'01-{layer}/RECEIPT.json',f'01-{layer}/stdout.log',f'01-{layer}/stderr.log']:
            extra.append('input-generation001/'+layer+'/'+rel)
    c['packaging_scripts'].extend(extra)
    c['documentary_capture_records']=[{'scope':'Producer40actual workers=15math25documentary, each original worker/outer/entry receipts and240split streams in frozen allowlist','record':'raw/producer/EXECUTION_RECORD_INDEX.json + EXECUTION_RECORD_INDEX_ADDENDUM.json'},
        {'scope':'Root actual metadata capture families and internal Git actions; exact files frozen by root, review coverage explicitly limited to first9; later prepublication text asset family root-read metadata only','record':'raw/root/ROOT_REVIEW_ACCEPTANCE.json'},
        {'scope':'Actual final-input documentary preparation, all three prospective original capture boundaries close BEFORE metadata attempt','record':'raw/packaging-scripts/input-generation001/{entry,outer,worker}/'}]
    put(R/'FINAL_INPUTS.json',c)
    record={'status':'FROZEN_FINAL65_INPUT_BINDING_PREPARED_NO_METADATA_ATTEMPT_YET','observed_utc':datetime.now(timezone.utc).isoformat(),
        'root_go':str(go_path),'root_file_list':a.root_list,'review_file_list':a.review_list,'producer_frozen_paths':len(allow),
        'immutable_files':len(files),'producer_run_records':len(runs),'reused_identity_seed_paths':len(c['existing_file_identities']),
        'digest_computations':0,'proof_replays':0,'Git_actions':0,'shared_mutations':0,
        'capture_policy':'Root generic capture utility reused unchanged as documentary utility, no source/object execution. All three current captures close before metadata entry starts.'}
    put(R/'INPUT_GENERATION_RECORD.json',record);print(json.dumps(record,sort_keys=True))

if __name__=='__main__':main()
