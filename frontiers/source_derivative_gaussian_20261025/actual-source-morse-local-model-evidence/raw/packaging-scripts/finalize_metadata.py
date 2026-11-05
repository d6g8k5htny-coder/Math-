#!/usr/bin/env python3
"""Prepared60 final metadata worker: no execution before explicit root finalGO."""
from pathlib import Path
import copy,json,tomllib
import custody as f
import archive_prepare as archive
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
REL=Path('frontiers/source_derivative_gaussian_20261025');O=R/'overlay'/REL
M='SourceActualMorseLocalModel';TARGET='I4SourceActualMorseLocalModel.actualSource_c1_quadratic_localModel'
CNAME='ACTUAL_MORSE_LOCAL_MODEL_EVIDENCE_CATALOG.json'
META=['README.md','SCOPE.md','lakefile.toml','SOURCE_MANIFEST.json','SOURCE_SHA256SUMS']
BASE_MANIFEST='9242d165f4472623ddae7f014eb7708e09e0a84926b27aba816fd2989174044e'
BASE_SUMS='5ccfb24cb82f6d567bc3687dc2ab8d5614cebf0735d7d9c99cd50b6fb493c80c'
def text(p,s):f.durable(p,s.encode());return f.identity(p)
def check(name,fn):
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_started','name':name})
    try:detail=fn()
    except BaseException as exc:
        f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_failed','name':name,'exception':repr(exc)});raise
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_passed','name':name,'detail':detail});print('PASS '+name,flush=True)

def assemble():
    f.require(not(R/'ASSEMBLY_RESULT.json').exists(),'Completed60 metadata reusable; never restart.')
    c=f.read(R/'FINAL_INPUTS.json');f.require(Path(c['root_finalization_go']).is_file(),'Actual final rootGO required')
    raw=archive.prepare(c);cut=c['source_cut'];bm=f.read(B/'SOURCE_MANIFEST.json');snap=R/'published59-metadata'
    for n in META:
        h=BASE_MANIFEST if n=='SOURCE_MANIFEST.json'else BASE_SUMS if n=='SOURCE_SHA256SUMS'else bm['files'][n]
        f.copied(B/n,snap/n,{'bytes':(B/n).stat().st_size,'sha256':h})
    oldkeys=list(bm['files']);oldrows=[line.split('  ',1)[1]for line in(snap/'SOURCE_SHA256SUMS').read_text().splitlines()]
    f.write(R/'BASELINE_BINDING.json',{'publication':f.BASE,'manifest_identity_reused':BASE_MANIFEST,'sums_identity_reused':BASE_SUMS,'manifest_key_sequence':oldkeys,'independent_checksum_row_sequence':oldrows,'old_hashes':0})
    records={}
    for path,rec in list(f.identities().items()):
        src=Path(path)
        if A not in src.parents:continue
        rel=src.relative_to(A);dst=O/(rel.name if rel.parts[0]=='bindings'else rel)
        records[str(dst.relative_to(O))]=f.copied(src,dst,rec)
    inv=f.read(P/'INVENTORY_CLASSIFICATION.json');owned=inv['all_module_index_owned_constants']
    reading=f.read(Path(c['root_reading_record']))
    scope='Actual source C1 ordered quadratic coordinates from literal criticality and genuine Hessian inertia: derive j<=2, one centered OpenPartialHomeomorph with C1 inverse and exact signed quadratic identity throughout source, plus arbitrarily small critical-superlevel path-connected neighborhoods using that SAME chart. Actual min/max/diagonal/zero-diagonal saddle fixtures; explicit P. No Cinf chart, probability/globalMorse/quotient regular-slab/elder/counting/Rice/Parent claim.'
    publication={'status':'QUALIFIED60_SCRATCH_PROPOSAL_ROOT_APPLY_ONLY','source_cut':cut,'source_cut_parent':c['source_cut_parent'],'qualified_baseline59':f.BASE,'root_reading_verbatim':reading,'root_reading_summary':c['root_reading_summary'],'reviewer_reading_summary':c['reviewer_reading_summary'],'packager_is_branch_A_proof_author':True,'packager_independent_review_credit':0,'no_inherited59_review_credit':True,'historical_pending_records_preserved':True,'remote60publication_claimed':False,'hosted60CI_claimed':False,'scientific_effect':'NONE','same_family_credit':0}
    catalog={'module':M,'namespace':'I4SourceActualMorseLocalModel','public_Prop_targets':[TARGET],'public_data':0,'scope':scope,'source_cut':cut,'source_bytes':65754,'source_sha256':f.SRC_SHA,'eligible_object_bytes':3409752,'eligible_object_sha256':f.OBJ_SHA,'object_action':'SKIP_ROOT_COPIED_ONCE','actual_owned_constants':owned,'classification_counts':inv['counts'],'foreign_generated_names':inv['foreign_generated_names'],'standard_three_guard':inv['standard_three_guard'],'qualification_records':c['qualification'],'sole_negative':c['negative_binding'],'production_helper_integrations':raw['production_helpers'],'ordinary_controls_integration':raw['ordinary_controls_integration'],'kernel_coverage':'Owned production and source-local PRIVATE direct actual four-fixture positives only. Separate ordinary Controls/counterproof/negative retain their own qualified object binding; no helper or Controls kernel credit.','actual_run_count':raw['actual_run_count'],'actual_split_stream_files':raw['actual_split_stream_files'],'actual_split_stream_bytes':raw['actual_split_stream_bytes'],'record_schema':'RECORD.json/start_utc/end_utc/source_identity + stdout.txt/stderr.txt; original streams never reconstructed or interleaved.','all_attempts_preserved':True,'raw_catalog':'RAW_EVIDENCE_CATALOG.json','publication':publication,'verification_reuse':'All applicable completed source/math/identity/strict/inventory/ONEkernel/positiveControls/soleFalse evidence reused unchanged; only new metadata associations checked.','canonical_authority':f.AUTHORITY,'link_delivery_not_reading':True,'scientific_effect':'NONE','same_family_credit':0}
    for n,x in [('RAW_EVIDENCE_CATALOG.json',raw),('PUBLICATION_CONTEXT.json',publication),(CNAME,catalog)]:records[E+'/'+n]=f.write(O/E/n,x)
    for n in c['curated_producer_files']:records[E+'/'+n]=f.copied(O/E/'raw/producer'/n,O/E/n,records[E+'/raw/producer/'+n])
    rp=c['review_report_archive_path'];records[E+'/AUTHOR_SIDE_REVIEW.md']=f.copied(O/E/rp,O/E/'AUTHOR_SIDE_REVIEW.md',records[E+'/'+rp])
    cp={'status':'SKIP_ALL_OWN_OLD_CONTROLS_HELPER_OBJECT_COPIES','root_copy_record':c['root_object_copy_record'],'eligible_own_object_bytes':3409752,'eligible_own_object_sha256':f.OBJ_SHA,'copies':[],'further_copy_actions':[],'ordinary_control_objects_ineligible':True,'helper_inventory_old_objects_ineligible':True,'ilean_refreshes':0}
    records[E+'/COPY_PLAN.json']=f.write(O/E/'COPY_PLAN.json',cp);f.write(R/'COPY_PLAN.json',cp)
    body=f'''[SourceActualMorseLocalModel.lean](SourceActualMorseLocalModel.lean) proves one actual-source C1 local-model proposition. Literal criticality and genuine complementary-subspace Hessian inertia at X yield j<=2 and a centered OpenPartialHomeomorph from the physical source to real2, with C1 forward/inverse maps and the exact ordered signed quadratic identity on its entire source. The SAME chart supplies arbitrarily small open critical-superlevel path-connected neighborhoods. No supplied chart/pivot/normal-form certificate or finite/global critical-set premise is used; Cinf coordinates are not claimed.

Actual smooth source derivatives supply the weighted Taylor matrix, whose center is J. The private finite2 rational sqrt branch is C1 on an actual neighborhood, with R(J)=I and R^T J R=M for symmetric M; J*M is J-self-adjoint, not assumed ordinarily symmetric. Actual source min/max/diagonal/zero-diagonal saddle fixtures use their explicit P and call the actual Taylor/branch/IFT/cone adapters. The sole ordinary negative omits only(1-t) in the SAME actual normalized minimum scalar entry; the separately passed counterproof gives correct1/unweighted2. Mutant2I remains invertible; no old cubic/rank-collapse/Gaussian-point-mass claim is made.

One public proposition/no public data append to qualified59 `{f.BASE}`:60modules/1130written=1121Prop+9data/32inputs. All{owned}actual module-owned constants are retained and classified, including foreign-generated names; standard-three axioms only. The three production helper originals were integrated once each with zero standalone execution; ordinary Controls original/actual amendments are separate from production-kernel coverage. All{raw['actual_run_count']}actual calls/{raw['actual_split_stream_files']}full original split streams/{raw['actual_split_stream_bytes']}B and source/harness/helper snapshots/complete actual patches are archived verbatim, including every failure. Root's eligible own object was copied once; ALL further object/cache actions and five installed bindings are SKIP.

Root reading scope: {c['root_reading_summary']}. Final nonproof-author reviewer scope: {c['reviewer_reading_summary']}. Packager authored branchA and earns no independent review credit. No inherited59/58 different-family review covers60. Historical pending cut/reading/timer records remain verbatim with actual root records separate. ScientificNONE/same-family0; process requirements are separate from mathematical evidence. No quotient chart/regular-boundary/slab transport/globalMorse/probability/H0component/elder/counting/Rice/Parent result follows from this local leaf. Root alone applies and publishes; no current-source hostedCI or remote publication is claimed here.
'''
    for n,title in [('README.md','# Actual-source C1 quadratic local coordinates'),('SCOPE.md','# Proposed60 modules/1130written/32inputs')]:records[n]=text(O/n,title+'\n\n'+body+'\n---\n\n# Historical qualified59 context, preserved verbatim\n\n'+(snap/n).read_text())
    lake=(snap/'lakefile.toml').read_text();marker='"SourceGapConditionalMorseDistinct"]';f.require(lake.count(marker)==1,'Unique inherited59 target marker')
    lake=lake.replace(marker,'"SourceGapConditionalMorseDistinct", "'+M+'"]')+'\n[[lean_lib]]\nname = "'+M+'"\n';records['lakefile.toml']=text(O/'lakefile.toml',lake)
    manifest=copy.deepcopy(bm);manifest['source_modules'].append(M+'.lean');manifest['targets'].append(TARGET)
    manifest['qualification_role']='Root proposal60/1130written=1121Prop+9data/32 against qualified59 '+f.BASE
    manifest['verification_reuse']='Completed applicable source/math/identity evidence reusable; no proof/kernel/control/hash replay for process/sourcecut/provider labels. Actual root/nonproof-author reviewer reading scopes distinct from branch-author packager.'
    manifest['catalogs'].append({'path':E+'/'+CNAME,'source_cut':cut,'scope':scope,'sha256':records[E+'/'+CNAME]['sha256']})
    manifest['new_actual_morse_local_model_scope']={'module':M,'source_cut':cut,'public_propositions':[TARGET],'public_data':0,'actual_owned_constants':owned,'classification_counts':inv['counts'],'foreign_generated_names':inv['foreign_generated_names'],'catalog':E+'/'+CNAME,'scope':scope,'publication':publication}
    for n in ['README.md','SCOPE.md','lakefile.toml']:manifest['files'][n]=records[n]['sha256']
    newpaths=sorted(p for p in records if p not in bm['files'])
    for p in newpaths:manifest['files'][p]=records[p]['sha256']
    mid=f.write(O/'SOURCE_MANIFEST.json',manifest);sid=text(O/'SOURCE_SHA256SUMS',''.join(manifest['files'][p]+'  '+p+'\n'for p in oldrows+newpaths))
    bs={x['path']for x in raw['bindings']};allrecords={**records,'SOURCE_MANIFEST.json':mid,'SOURCE_SHA256SUMS':sid}
    plan={'status':'ROOT_ONLY_EXACT60_APPLY_AFTER_METADATA_PASS','expected_HEAD':cut,'qualified_baseline':f.BASE,'overlay_root':str(R/'overlay'),'destination_root':'/workspace/Math-curvature-20261026','apply':[],'skip':[],'cache_object_actions':[]}
    for p,x in sorted(allrecords.items()):plan['skip'if p in bs else'apply'].append({'path':str(REL/p),'bytes':x['bytes'],'sha256':x['sha256']})
    pid=f.write(R/'APPLY_PLAN.json',plan)
    def registry():
        f.require(manifest['source_modules']==bm['source_modules']+[M+'.lean'] and manifest['targets']==bm['targets']+[TARGET],'One module/oneProp append')
        f.require((len(manifest['source_modules']),len(manifest['targets']),manifest['inherited_input_count'])==(60,1130,32),'60/1130/32')
        f.require(inv['authored_public_Prop']==1 and inv['authored_public_data']==0,'One authored publicProp/noData')
        return '1121Prop+9data/32'
    check('exact60_registration',registry)
    def prefixes():
        f.require(len(oldkeys)==5458 and list(manifest['files'])[:5458]==oldkeys,'5458 inherited KEY prefix')
        f.require({p for p in oldkeys if bm['files'][p]!=manifest['files'][p]}=={'README.md','SCOPE.md','lakefile.toml'},'Only three old digest changes')
        rows=[line.split('  ',1)for line in(O/'SOURCE_SHA256SUMS').read_text().splitlines()]
        f.require([p for h,p in rows[:len(oldrows)]]==oldrows,'Independent inherited ROW prefix')
        f.require([p for h,p in rows[len(oldrows):]]==newpaths and {p:h for h,p in rows}==manifest['files'],'Append-only new checksum rows and associations')
        f.require(not{'SOURCE_MANIFEST.json','SOURCE_SHA256SUMS'}&set(manifest['files']),'No SELF entries')
        return 'Separate5458key and independent checksum-row sequences retained; no old payload hashes'
    check('separate_manifest_key_and_checksum_row_prefixes',prefixes)
    def lakecheck():
        old=tomllib.loads((snap/'lakefile.toml').read_text());new=tomllib.loads(lake)
        f.require(new['defaultTargets']==old['defaultTargets']+[M] and new['lean_lib']==old['lean_lib']+[{'name':M}],'One library/default target append')
        f.require(all(new[k]==old[k]for k in old if k not in ['defaultTargets','lean_lib']),'All other lake fields unchanged')
        return 'Exact one-library append; no build'
    check('Lake60_append_only',lakecheck)
    def evidence():
        f.require(sum(inv['counts'].values())==owned and inv['standard_three_guard'].startswith('PASS'),'Stored full-owned/std3 inventory')
        f.require(len(inv['foreign_generated_names'])==inv['counts']['owned_foreign_generated'],'Foreign-generated declarations retained')
        rr={str(Path(x['record_path']).relative_to(P)):x['record']for x in raw['runs']}
        for k in ['strict','inventory','kernel','positive_controls']:f.require(rr[c['qualification'][k]]['exit_code']==0,'Retained '+k+' PASS')
        f.require(rr[c['qualification']['negative']]['exit_code']==1,'Retained sole intendedFalse')
        f.require(len([x for x in raw['runs']if'leanchecker'in str(x['record']['command'])])==1,'Exactly one own kernel')
        f.require(raw['actual_split_stream_files']==2*raw['actual_run_count'],'All actual original .txt split streams')
        f.require(len(raw['production_helpers']['integrations'])==3 and all(x['integration_count']==1 and x['helper_executions']==0 for x in raw['production_helpers']['integrations']),'A/B/C once/no standalone executions')
        f.require(raw['ordinary_controls_integration']['integration_count']==1 and raw['ordinary_controls_integration']['helper_executions']==0,'Separate Controls original once/no helper execution')
        return 'Actual60schema and qualification scopes preserved, no proof replays'
    check('retained60_evidence_and_helper_scope',evidence)
    def overlay():
        paths={str(p.relative_to(O))for p in O.rglob('*')if p.is_file()}
        f.require(paths==set(allrecords) and len(plan['skip'])==5 and len(plan['apply'])==len(paths)-5,'Exact overlay/five bindings SKIP')
        f.require(not any(archive.artifact(Path(p))for p in paths),'No artifact binary')
        f.require(not cp['copies'] and not cp['further_copy_actions'] and not plan['cache_object_actions'],'ALL object actions SKIP')
        return {'overlay_files':len(paths),'apply_files':len(plan['apply']),'binding_SKIP':5}
    check('exact_overlay_ALL_objects_SKIP',overlay)
    def provenance():
        f.require(bool(c['root_reading_summary']) and bool(c['reviewer_reading_summary']) and c['final_review_pass'],'Actual final reading scopes required')
        f.require(publication['root_reading_verbatim']==reading and publication['packager_is_branch_A_proof_author'] and publication['packager_independent_review_credit']==0,'Honest branch authorship and actual root/reviewer limits')
        f.require(publication['historical_pending_records_preserved'] and publication['same_family_credit']==0,'Historical process kept separate')
        return 'Nonauthor reviewer distinct from branch-author packager; no review coverage transfer'
    check('honest_author_review_and_process_scopes',provenance)
    def parse():
        paths=[O/'SOURCE_MANIFEST.json',R/'APPLY_PLAN.json',R/'COPY_PLAN.json']+[O/E/n for n in ['RAW_EVIDENCE_CATALOG.json','PUBLICATION_CONTEXT.json','COPY_PLAN.json',CNAME]]
        for p in paths:f.read(p)
        return {'new_metadata_JSONs':len(paths),'old_raw_JSON_rechecks':0}
    check('new_metadata_JSON_parse',parse)
    counts={'modules':60,'written':1130,'Prop':1121,'data':9,'inputs':32,'manifest_entries':len(manifest['files']),'new_manifest_entries':len(newpaths),'overlay_files':len(allrecords),'apply_files':len(plan['apply']),'binding_SKIP':5,'actual_owned_constants':owned,'actual_runs':raw['actual_run_count'],'split_stream_files':raw['actual_split_stream_files'],'split_stream_bytes':raw['actual_split_stream_bytes'],'excluded_artifacts':len(raw['excluded_artifacts'])}
    result={'status':'NEW60_METADATA_ASSEMBLY_AND_BOUNDED_ASSOCIATIONS_PASS','source_cut':cut,'qualified_baseline':f.BASE,'counts':counts,'owned_constants':owned,'manifest_identity':mid,'sums_identity':sid,'catalog_identity':records[E+'/'+CNAME],'apply_plan_identity':pid,'object_action':'SKIP_ROOT_COPIED_ONCE','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ASSEMBLY_RESULT.json',result);print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':assemble()
