#!/usr/bin/env python3
"""Unexecuted candidate: one new59 scratch archive/metadata association attempt after final rootGO."""
from pathlib import Path
import copy,json,tomllib
import custody as f
import archive_prepare as archive
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
REL=Path('frontiers/source_derivative_gaussian_20261025');O=R/'overlay'/REL
M='SourceGapConditionalMorseDistinct';TARGET='I4SourceGapConditionalMorseDistinct.sourceGapLaw_ae_isMorseDistinct'
CNAME='GAP_CONDITIONAL_MORSE_DISTINCT_EVIDENCE_CATALOG.json'
META=['README.md','SCOPE.md','lakefile.toml','SOURCE_MANIFEST.json','SOURCE_SHA256SUMS']
BASE_MANIFEST='88ef8261743632262c1e54b26a43a3cce37b2dec728c23ed3c43515f397f7d82'
BASE_SUMS='68bdd3edfa635e45571623bef50690e4acba312b03e484d0ced8d8429b6daa2b'
def text(p,s):f.durable(p,s.encode());return f.identity(p)
def check(name,fn):
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_started','name':name})
    try:detail=fn()
    except BaseException as exc:
        f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_failed','name':name,'exception':repr(exc)});raise
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_passed','name':name,'detail':detail});print('PASS '+name,flush=True)

def assemble():
    f.require(not(R/'ASSEMBLY_RESULT.json').exists(),'Completed metadata associations reusable; never restart.')
    c=f.read(R/'FINAL_INPUTS.json')
    f.require(Path(c['root_finalization_go']).is_file(),'Actual final rootGO record required')
    raw=archive.prepare(c);cut=c['source_cut'];bm=f.read(B/'SOURCE_MANIFEST.json');snap=R/'published58-metadata'
    for n in META:
        h=BASE_MANIFEST if n=='SOURCE_MANIFEST.json'else BASE_SUMS if n=='SOURCE_SHA256SUMS'else bm['files'][n]
        f.copied(B/n,snap/n,{'bytes':(B/n).stat().st_size,'sha256':h})
    oldkeys=list(bm['files']);oldrows=[p for h,p in [line.split('  ',1)for line in(snap/'SOURCE_SHA256SUMS').read_text().splitlines()]]
    f.write(R/'BASELINE_BINDING.json',{'publication':f.BASE,'manifest_identity_reused':BASE_MANIFEST,'sums_identity_reused':BASE_SUMS,'manifest_key_sequence':oldkeys,'independent_checksum_row_sequence':oldrows,'old_hashes':0})
    records={}
    for path,rec in list(f.identities().items()):
        src=Path(path)
        if A not in src.parents:continue
        rel=src.relative_to(A);dst=O/(rel.name if rel.parts[0]=='bindings'else rel)
        records[str(dst.relative_to(O))]=f.copied(src,dst,rec)
    tc=f.read(P/'TARGET_CLASSIFICATION.json');inv=f.read(P/'INVENTORY.json');helpers=f.read(P/'AUTHOR_HELPER_LINEAGE.json')
    reading=f.read(Path(c['root_reading_record']))
    scope='Actual defined sourceGapLaw at positive gap: for each L>0 derive delta>0 with delta<=1,L/2 before r,b,k; for each0<r<delta andb,0<k, a.e. literal actualField has Lifetime.IsMorseDistinct. Actual2/3/5 source frames, whole-vector57law/reconstruction, fullDBtheta/dummySard, compactcountable quotient-aware assembly and52pin nullity/fiber; genuine inertia. No common uncountable parameter event, Parent/canonical elder/Rice/counting/localModel60 claim.'
    publication={'status':'QUALIFIED59_SCRATCH_PROPOSAL_ROOT_APPLY_ONLY','source_cut':cut,'source_cut_parent':c['source_cut_parent'],'qualified_baseline58':f.BASE,'root_reading_verbatim':reading,'root_reading_summary':c['root_reading_summary'],'final_reviewer_summary':c['reviewer_reading_summary'],'old58_review_not59_credit':True,'historical_pending_records_preserved':True,'remote59publication_claimed':False,'hosted59CI_claimed':False,'same_family_credit':0,'scientific_effect':'NONE'}
    catalog={'module':M,'public_Prop_targets':[TARGET],'public_data':0,'scope':scope,'source_cut':cut,'source_bytes':99430,'source_sha256':f.SRC_SHA,'eligible_object_bytes':4189248,'eligible_object_sha256':f.OBJ_SHA,'object_action':'SKIP_ROOT_COPIED_ONCE','actual_owned_constants':167,'classification':tc,'all_axioms_allowed':inv['axioms_allowed'],'strict_receipt':'raw/producer/'+c['qualification']['strict'],'strict_reused_after_freeze':True,'inventory_receipt':'raw/producer/'+c['qualification']['inventory'],'ONE_kernel_receipt':'raw/producer/'+c['qualification']['kernel'],'ordinary_control_receipts':c['qualification']['positive_controls'],'sole_negative_receipt':c['qualification']['negative'],'negative_binding':c['negative_binding'],'extra_positive_companion':c['positive_companion_binding'],'kernel_coverage':'Production plus four production-private helpers/source-local positives only; fifth helper and ordinary Controls/companion qualified separately. Negative imports immutable Controls003, not the later companion.','actual_run_count':raw['actual_run_count'],'actual_split_stream_files':raw['actual_split_stream_files'],'actual_split_stream_bytes':raw['actual_split_stream_bytes'],'all_attempts_original_split_streams_retained':True,'helpers':helpers,'raw_membership':'RAW_EVIDENCE_CATALOG.json','publication':publication,'owner_reuse':'Completed applicable proofs/objects/identities/strict/inventory/ONEkernel/Controls/negative reused unchanged; no old hashes or math checks.','canonical_authority':f.AUTHORITY,'link_delivery_not_reading':True,'scientific_effect':'NONE','same_family_credit':0}
    for name,value in [('RAW_EVIDENCE_CATALOG.json',raw),('PUBLICATION_CONTEXT.json',publication),(CNAME,catalog)]:records[E+'/'+name]=f.write(O/E/name,value)
    for n in c['curated_producer_files']:
        src=O/E/'raw/producer'/n
        records[E+'/'+n]=f.copied(src,O/E/n,records[E+'/raw/producer/'+n])
    revpath=c['review_report_archive_path'];records[E+'/AUTHOR_SIDE_REVIEW.md']=f.copied(O/E/revpath,O/E/'AUTHOR_SIDE_REVIEW.md',records[E+'/'+revpath])
    cp={'status':'SKIP_ALL_OWN_OLD_AUXILIARY_OBJECT_COPIES','root_copy_record':c['root_object_copy_record'],'eligible_object_bytes':4189248,'eligible_object_sha256':f.OBJ_SHA,'copies':[],'further_copy_actions':[],'Controls003_object_ineligible':c['negative_binding']['controls_object'],'positive_companion_object_ineligible':True,'helper_or_inventory_object_ineligible':True,'old_cache_or_ilean_refreshes':0}
    records[E+'/COPY_PLAN.json']=f.write(O/E/'COPY_PLAN.json',cp);f.write(R/'COPY_PLAN.json',cp)
    body=f'''[SourceGapConditionalMorseDistinct.lean](SourceGapConditionalMorseDistinct.lean) proves the actual positive-gap conditional Morse/distinct-value endpoint. For eachL>0 one positive delta is chosen before radius and marks, with delta<=1 andL/2; for each0<r<delta,b andk>0, the literal sourceGapLaw-almost-everywhere actual field has Lifetime.IsMorseDistinct. There is no common event over all uncountably many parameters or desired rank/law/Morse premise. Genuine inertia and quotient-distinct critical values use the original source.

Exactly one written public proposition and no public data append:59modules/1129written=1120Prop+9data/32inputs against qualified58 `{f.BASE}`. The actual167constant inventory retains133authored private(115Prop/18data),1publicProp,31privategenerated and2foreigngenerated declarations under the standard3 axioms. FullDBtheta, actual2/3/5finiteframes, whole57vector law, compact/countable quotient-aware assembly, positive-gap endpoints and literal Lifetime bridge are private new joins.

All applicable old mathematical evidence is reused; final strict012, inventory, EXACTLYONEownkernel, ordinary Controls003/sole120BFalse and later separate positive-only numeric/remoteness companion retain their actual independent bindings. Four original production helper sections were each integrated once with zero standalone executions; the fifth Controls-only section and full actual patches have separate ordinary-Controls coverage, not production-kernel coverage. All{raw['actual_run_count']}actual attempts/{raw['actual_split_stream_files']}original split streams/{raw['actual_split_stream_bytes']}B and source/harness/helper snapshots are retained, including every failure. Historical pending sourcecut/reading/timer labels remain verbatim; actual root cut/copy/finalreading are separate records.

Root reading scope is recorded verbatim in the evidence. Root summary: {c['root_reading_summary']}. Final same-family reviewer summary: {c['reviewer_reading_summary']}. No inherited58-native-review coverage of59, independent-provider credit, scientific acceptance, Parent/elder/canonical counting/Rice/PairLaw or60local-model claim is inferred. Scientific effectNONE/same-family0; process separate from mathematics. Root alone applies/publishes; five source/PRECODE bindings and ALL objects are SKIP.
'''
    for n,title in [('README.md','# Positive-gap conditional Morse distinctness'),('SCOPE.md','# Qualified proposal:59 modules,1129 written targets,32 inputs')]:records[n]=text(O/n,title+'\n\n'+body+'\n---\n\n# Historical published58 context, preserved verbatim\n\n'+(snap/n).read_text())
    lake=(snap/'lakefile.toml').read_text();marker='"SourceFramedConfluentCovariance"]';f.require(lake.count(marker)==1,'Unique inherited library marker')
    lake=lake.replace(marker,'"SourceFramedConfluentCovariance", "'+M+'"]')+'\n[[lean_lib]]\nname = "'+M+'"\n';records['lakefile.toml']=text(O/'lakefile.toml',lake)
    manifest=copy.deepcopy(bm);manifest['source_modules'].append(M+'.lean');manifest['targets'].append(TARGET)
    manifest['qualification_role']='Root proposal59/1129written=1120Prop+9data/32 against actual qualified58 '+f.BASE
    manifest['verification_reuse']='Completed applicable mathematical/identity evidence reused. New59 only; sourcecut/Git/provider process is not a replay reason. Root/reviewer reading limits are in the actual records; no inherited58review or root-all-raw claim.'
    manifest['catalogs'].append({'path':E+'/'+CNAME,'source_cut':cut,'scope':scope,'sha256':records[E+'/'+CNAME]['sha256']})
    manifest['new_gap_conditional_morse_distinct_scope']={'module':M,'source_cut':cut,'public_propositions':[TARGET],'public_data':0,'actual_owned_constants':167,'classification_counts':tc['classification_counts'],'foreign_generated':tc['foreign_generated'],'catalog':E+'/'+CNAME,'scope':scope,'publication':publication}
    for n in ['README.md','SCOPE.md','lakefile.toml']:manifest['files'][n]=records[n]['sha256']
    newpaths=sorted(p for p in records if p not in bm['files'])
    for p in newpaths:manifest['files'][p]=records[p]['sha256']
    mid=f.write(O/'SOURCE_MANIFEST.json',manifest)
    sid=text(O/'SOURCE_SHA256SUMS',''.join(manifest['files'][p]+'  '+p+'\n'for p in oldrows+newpaths))
    bset={x['path']for x in raw['bindings']};plan={'status':'ROOT_ONLY_EXACT59_APPLY_AFTER_METADATA_PASS','expected_HEAD':cut,'qualified_baseline':f.BASE,'overlay_root':str(R/'overlay'),'destination_root':'/workspace/Math-curvature-20261026','apply':[],'skip':[],'cache_object_actions':[],'stage60':'Untracked source/private/helpers untouched; no60inspection/registration.'}
    allrecords={**records,'SOURCE_MANIFEST.json':mid,'SOURCE_SHA256SUMS':sid}
    for p,rec in sorted(allrecords.items()):
        x={'path':str(REL/p),'bytes':rec['bytes'],'sha256':rec['sha256']}
        plan['skip'if p in bset else 'apply'].append(x)
    pid=f.write(R/'APPLY_PLAN.json',plan)
    def registration():
        f.require(manifest['source_modules']==bm['source_modules']+[M+'.lean']and manifest['targets']==bm['targets']+[TARGET],'Exactly one module/oneProp append')
        f.require((len(manifest['source_modules']),len(manifest['targets']),manifest['inherited_input_count'])==(59,1129,32),'59/1129/32')
        return '1120Prop+9data; no new public data'
    check('exact59_registry_append',registration)
    def prefix():
        f.require(len(oldkeys)==5141 and list(manifest['files'])[:5141]==oldkeys,'Independent inherited manifest key prefix')
        f.require({p for p in oldkeys if bm['files'][p]!=manifest['files'][p]}=={'README.md','SCOPE.md','lakefile.toml'},'Only three inherited digest changes')
        rows=[line.split('  ',1)for line in(O/'SOURCE_SHA256SUMS').read_text().splitlines()]
        f.require([p for h,p in rows[:len(oldrows)]]==oldrows,'Independent checksum-row prefix preserved')
        f.require([p for h,p in rows[len(oldrows):]]==newpaths and{p:h for h,p in rows}==manifest['files'],'New paths appended/associations exact')
        f.require(not{'SOURCE_MANIFEST.json','SOURCE_SHA256SUMS'}&set(manifest['files']),'No SELF entries')
        return '5141 key prefix and separately inherited checksum row prefix; no old payload hashes'
    check('separate_manifest_and_checksum_prefixes',prefix)
    def lakecheck():
        old=tomllib.loads((snap/'lakefile.toml').read_text());new=tomllib.loads(lake)
        f.require(new['defaultTargets']==old['defaultTargets']+[M]and new['lean_lib']==old['lean_lib']+[{'name':M}],'One exact library/default target append')
        f.require(all(new[k]==old[k]for k in old if k not in ['defaultTargets','lean_lib']),'Other lake configuration unchanged')
        return 'One default target/library append, no build performed'
    check('exact_Lake59_append',lakecheck)
    def association():
        f.require(inv['status']=='PASS'and inv['total_actual_module_constants']==167 and sum(tc['classification_counts'].values())==167,'Retained actual167 classification')
        f.require(len(tc['foreign_generated'])==2 and tc['authored_public_data']==0 and tc['authored_public_propositions']==[TARGET],'OneProp/noData/twoForeignGenerated')
        rr={str(Path(x['receipt']).relative_to(P)):x['record']for x in raw['runs']}
        for name in ['strict','inventory','kernel']:f.require(rr[c['qualification'][name]]['exit_code']==0,'Retained '+name+'PASS')
        for name in c['qualification']['positive_controls']:f.require(rr[name]['exit_code']==0,'Retained ordinary positivePASS')
        f.require(rr[c['qualification']['negative']]['exit_code']==1,'Retained sole intendedFalse receipt')
        f.require(len([x for x in raw['runs']if 'leanchecker'in str(x['record']['command'])])==1,'Exactly one own kernel retained')
        f.require(raw['actual_split_stream_files']==2*raw['actual_run_count'],'All actual separate original streams')
        f.require(all(x['integration_count']==1 and x['helper_executions']==0 for x in helpers['records']),'All helpers once/no independent campaign')
        return 'Stored evidence association only; production/Controls/companion/negative scopes separate, no math rerun'
    check('retained_qualification_and_helper_scope_association',association)
    def overlay():
        paths={str(p.relative_to(O))for p in O.rglob('*')if p.is_file()}
        f.require(paths==set(allrecords),'Exact overlay membership')
        f.require(len(plan['skip'])==5 and len(plan['apply'])==len(paths)-5,'Five installed binding SKIPs')
        f.require(not any(archive.artifact(Path(p))for p in paths),'No actual artifact in archive/overlay')
        f.require(not plan['cache_object_actions']and not cp['copies']and not cp['further_copy_actions'],'All object actions SKIP')
        return {'overlay_files':len(paths),'apply_files':len(plan['apply']),'binding_SKIP':5}
    check('exact_overlay_and_ALL_object_SKIP',overlay)
    def provenance():
        f.require(c['final_review_pass'] and c['immutable_payloads_frozen'],'Actual final review/freeze flags')
        f.require(bool(c['root_reading_summary']) and bool(c['reviewer_reading_summary']),'Actual reading summaries required')
        f.require(publication['root_reading_verbatim']==reading and publication['old58_review_not59_credit'],'Root actual limits/58-only review remain honest')
        f.require(publication['historical_pending_records_preserved'] and publication['same_family_credit']==0 and publication['scientific_effect']=='NONE','Process/scope preserved')
        f.require(c['negative_binding']['controls_object']['sha256']=='90e8eac00890fc1240be834cf7802eae9c64dcee456c259782259bd2c057e305','Negative keeps immutable Controls003 object binding')
        return 'Actual root/reviewer scope verbatim; no inherited58review/companion-negative/kernel coverage transfer'
    check('honest_reading_and_negative_companion_boundaries',provenance)
    def new_json_parse():
        paths=[O/'SOURCE_MANIFEST.json',R/'APPLY_PLAN.json',R/'COPY_PLAN.json']+[O/E/n for n in ['RAW_EVIDENCE_CATALOG.json','PUBLICATION_CONTEXT.json','COPY_PLAN.json',CNAME]]
        for p in paths:f.read(p)
        return {'new_metadata_JSONs':len(paths),'old_raw_JSON_revalidation':0}
    check('new_metadata_JSON_parse',new_json_parse)
    counts={'modules':59,'written':1129,'Prop':1120,'data':9,'inputs':32,'manifest_entries':len(manifest['files']),'new_manifest_entries':len(newpaths),'overlay_files':len(allrecords),'apply_files':len(plan['apply']),'binding_SKIP':5,'actual_runs':raw['actual_run_count'],'split_stream_files':raw['actual_split_stream_files'],'split_stream_bytes':raw['actual_split_stream_bytes'],'excluded_artifacts':len(raw['excluded_artifacts'])}
    result={'status':'NEW59_METADATA_ASSEMBLY_AND_BOUNDED_ASSOCIATIONS_PASS','source_cut':cut,'qualified_baseline':f.BASE,'counts':counts,'manifest_identity':mid,'sums_identity':sid,'catalog_identity':records[E+'/'+CNAME],'apply_plan_identity':pid,'object_action':'SKIP_ROOT_ALREADY_COPIED_ONCE','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ASSEMBLY_RESULT.json',result);print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':assemble()
