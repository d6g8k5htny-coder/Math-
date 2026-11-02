#!/usr/bin/env python3
"""Prepared62 metadata worker. Execute only after explicit final root GO."""
from pathlib import Path
import copy,json,tomllib
import custody as f
import archive_prepare as archive
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
REL=Path('frontiers/source_derivative_gaussian_20261025');O=R/'overlay'/REL
M='SourceActualTorusRegularSlab'
TARGET='I4SourceActualTorusRegularSlab.actualSource_closedSlab_componentInclusion_bijective'
CNAME='ACTUAL_TORUS_REGULAR_SLAB_EVIDENCE_CATALOG.json'
META=['README.md','SCOPE.md','lakefile.toml','SOURCE_MANIFEST.json','SOURCE_SHA256SUMS']
BASE_MANIFEST='2170f54dd552587df0c29876583d29cc7d61b20f6fa7ed367efa344f5afbd80c'
BASE_SUMS='a309f02486dc3ffc992baabbd21ea0b827b7ea7c9d9da35c44d10eb61fe11e46'
SCOPE='Actual-source regular CLOSED-slab component inclusion on the SAME product AddCircle torus: positive L, original SmoothSample, a<=b and actual fderiv nonzero at EVERY cover point with a<=g<=b imply bijectivity of the EXISTING inclusion-induced ZerothHomotopy map, s=-b,t=-a. Derive the physical Fourier bounds, closed-cell squared-gradient floor, clipped periodic bounded Lipschitz velocity, ANY finite-horizon joint Picard family, global barriers BEFORE residence, variable hitting map, restricted OPEN quotient descent and actual component-map injectivity/surjectivity internally. No supplied floor/flow/retract/component certificate, MorseDistinct, probability/local-PC61, global Flow/group law, atlas or component census.'
def text(path,value):f.durable(path,value.encode());return f.identity(path)
def check(name,fn):
    journal=R/'VALIDATION_PROGRESS.jsonl'
    prior=[x for x in map(json.loads,journal.read_text().splitlines()) if x['event']=='check_passed' and x['name']==name] if journal.exists() else []
    if prior:return prior[-1]['detail']
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_started','name':name})
    try:detail=fn()
    except BaseException as exc:
        f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_failed','name':name,'exception':repr(exc)});raise
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_passed','name':name,'detail':detail});print('PASS '+name,flush=True)
def assemble():
    f.require(not (R/'ASSEMBLY_RESULT.json').exists(),'Completed62 metadata is reusable; never restart')
    c=f.read(R/'FINAL_INPUTS.json');archive.gate(c);raw=archive.prepare(c);cut=c['source_cut']
    bm=f.read(B/'SOURCE_MANIFEST.json');snap=R/'published61-metadata'
    for name in META:
        h=BASE_MANIFEST if name=='SOURCE_MANIFEST.json' else BASE_SUMS if name=='SOURCE_SHA256SUMS' else bm['files'][name]
        f.copied(B/name,snap/name,{'bytes':(B/name).stat().st_size,'sha256':h})
    oldkeys=list(bm['files']);oldrows=[line.split('  ',1)[1] for line in (snap/'SOURCE_SHA256SUMS').read_text().splitlines()]
    f.write(R/'BASELINE_BINDING.json',{'publication':f.BASE,'manifest_identity_reused':BASE_MANIFEST,'sums_identity_reused':BASE_SUMS,'manifest_key_sequence':oldkeys,'independent_checksum_row_sequence':oldrows,'old_hashes':0})
    records={}
    for path,rec in list(f.identities().items()):
        src=Path(path)
        if A not in src.parents:continue
        rel=src.relative_to(A);dst=O/(rel.name if rel.parts[0]=='bindings' else rel)
        records[str(dst.relative_to(O))]=f.copied(src,dst,rec)
    inv=c['inventory_summary'];owned=inv['all_module_index_owned_constants'];reading=f.read(Path(c['root_reading_record']))
    publication={'status':'QUALIFIED62_SCRATCH_PROPOSAL_ROOT_APPLY_ONLY','source_cut':cut,'source_cut_parent':c['source_cut_parent'],'qualified_baseline61':f.BASE,'root_reading_verbatim':reading,'root_reading_summary':c['root_reading_summary'],'reviewer_reading_summary':c['reviewer_reading_summary'],'packager_is_62_proof_author':True,'packager_proof_role':'A actual normalized-field section original; source/helper authorship disclosed','packager_independent_review_credit':0,'no_inherited61_review_credit':True,'historical_pending_records_preserved':True,'remote62publication_claimed':False,'hosted62CI_claimed':False,'scientific_effect':'NONE','same_family_credit':0}
    catalog={'module':M,'namespace':'I4SourceActualTorusRegularSlab','public_Prop_targets':[TARGET],'public_data':0,'scope':SCOPE,'source_cut':cut,'source_identity':c['source_identity'],'eligible_object_identity':c['eligible_object_identity'],'object_action':'SKIP_ROOT_COPIED_ONCE','actual_owned_constants':owned,'inventory_summary':inv,'full_inventory_archive_path':c['inventory_archive_path'],'qualification_records':c['qualification'],'sole_negative':c['negative_binding'],'production_helper_integrations':raw['production_helpers'],'ordinary_controls_custody':raw['ordinary_controls_custody'],'kernel_coverage':'Owned production including all3 private production sections, actual source fixtures and branch consumers only. Producer-authored ordinary Controls and independently passed actual component-collision counterproof/sole importing False have separate object binding; production kernel covers no ordinary Controls.','actual_run_count':raw['actual_run_count'],'actual_split_stream_files':raw['actual_split_stream_files'],'actual_split_stream_bytes':raw['actual_split_stream_bytes'],'record_schema':'receipt.json/before/after/snapshots[{immutable_path,existing_identity}]/runner_version/runner_history/started_utc/ended_utc plus stdout.log/stderr.log; all actual runner/context versions retained. Actual timeout124 is resource failure, never intended mathematical False.','all_attempts_preserved':True,'raw_catalog':'RAW_EVIDENCE_CATALOG.json','publication':publication,'verification_reuse':'All applicable completed source/math/identity/strict/inventory/ONEkernel/Controls/soleFalse evidence reused. Only new metadata associations checked.','canonical_authority':f.AUTHORITY,'link_delivery_not_reading':True,'scientific_effect':'NONE','same_family_credit':0}
    for name,value in [('RAW_EVIDENCE_CATALOG.json',raw),('PUBLICATION_CONTEXT.json',publication),(CNAME,catalog)]:records[E+'/'+name]=f.write(O/E/name,value)
    for name in c['curated_producer_files']:records[E+'/'+name]=f.copied(O/E/'raw/producer'/name,O/E/name,records[E+'/raw/producer/'+name])
    rp=c['review_report_archive_path'];records[E+'/AUTHOR_SIDE_REVIEW.md']=f.copied(O/E/rp,O/E/'AUTHOR_SIDE_REVIEW.md',records[E+'/'+rp])
    cp={'status':'SKIP_ALL_OWN_OLD_CONTROLS_HELPER_OBJECT_COPIES','root_copy_record':c['root_object_copy_record'],'eligible_own_object_identity':c['eligible_object_identity'],'copies':[],'further_copy_actions':[],'ordinary_control_objects_ineligible':True,'helper_inventory_old_objects_ineligible':True,'ilean_refreshes':0}
    records[E+'/COPY_PLAN.json']=f.write(O/E/'COPY_PLAN.json',cp);f.write(R/'COPY_PLAN.json',cp)
    body=f'''[{M}.lean]({M}.lean) appends exactly one actual regular CLOSED-slab component proposition and no public data. Positive L, the SAME original smooth sample/physical actualField/descended product-AddCircle field, a<=b and actual nonzero fderiv on EVERY point of the CLOSED band imply bijectivity of the existing inclusion-induced component map with s=-b,t=-a. No supplied gradient floor, vector-field/flow/retract/component certificate, global Morse/distinct-values or finite critical-set premise is inserted.

The actual old Fourier majorants pass through explicit physical coordinate operator-norm factors; a compact CLOSED physical fundamental-cell band yields a positive SQUARED-gradient floor. The clipped normalized velocity is globally bounded, Lipschitz and periodic, with scalar speed[0,1] globally and1 on band. The ANY fixed finite-horizon Picard family is patched by uniqueness; global height barriers precede band residence and exact arrival. Variable-time hitting maps descend through the restricted saturated OPEN quotient and prove bijectivity of THIS literal inclusion map. No global Flow, group law, continuous representative or component census is assumed.

The exact original primary fixture at period2 is cos(2*pi*x)+(1/2)*cos(pi*y). Private production and separate ordinary positives exercise the nonempty regular[0,1/4] band, zero-width[0,0] identity and empty[-3,-2] band with BOTH superlevels the WHOLE NONEMPTY torus. The sole mutation changes ONLY the actual no-critical premise from CLOSED Icc[-1/2,0] to OPEN Ioo, preserving primary source/levels/CLOSED superlevels/literal component map. The passed independent counterproof uses the auxiliary actual cosine-x observable to separate two upper components while the actual lower horizontal path joins their inclusion images. This is a genuine nonempty collision, without an exact component count. No auxiliary y sample or second mutation is introduced.

Qualified61 `{f.BASE}` appends to62 modules/1132 written=1123Prop+9data/32 inputs. All {owned} actual owned constants and full standard-three classifications remain retained, including private/generated/foreign-generated declarations. All {raw['actual_run_count']} actual calls/{raw['actual_split_stream_files']} full original split streams/{raw['actual_split_stream_bytes']}B, source/harness/runner/context snapshots, personal ACKs/versions/freezes/all3 complete production originals and FULL actual amendments/failures are retained. Counts derive from actual final records. Ordinary Controls is producer-authored, not a fourth text helper; it has distinct qualification and the production kernel does not cover it. Five installed bindings and ALL object/cache actions SKIP after root's single eligible final own-object copy.

Root reading: {c['root_reading_summary']}. Final reviewer reading: {c['reviewer_reading_summary']}. The packager authored helper A normalized-field text and has NO independent review credit; all3 complete original sections had zero standalone helper executions. No prior61 review transfers to62. Root owns shared application/publication; this proposal claims no remote62 publication or hosted62 CI. Historical process and actual timeout/signal facts stay verbatim. ScientificNONE/same-family0; completed applicable verification and accepted mathematics remain reusable, with provider-distinct process separate. No exhaustive critical-event/elder/once-counting, Borel/Rice/Campbell, actual PairLaw or Parent result is inferred.
'''
    for name,title in [('README.md','# Actual torus regular closed-slab component inclusion'),('SCOPE.md','# Proposed62 modules/1132 written/32 inputs')]:records[name]=text(O/name,title+'\n\n'+body+'\n---\n\n# Historical qualified61 context preserved verbatim\n\n'+(snap/name).read_text())
    lake=(snap/'lakefile.toml').read_text();marker='"SourceActualTorusSuperlevelLocalBasis"]';f.require(lake.count(marker)==1,'Unique inherited61 last target')
    lake=lake.replace(marker,'"SourceActualTorusSuperlevelLocalBasis", "'+M+'"]')+'\n[[lean_lib]]\nname = "'+M+'"\n';records['lakefile.toml']=text(O/'lakefile.toml',lake)
    manifest=copy.deepcopy(bm);manifest['source_modules'].append(M+'.lean');manifest['targets'].append(TARGET)
    manifest['qualification_role']='Root proposal62/1132written=1123Prop+9data/32 against qualified61 '+f.BASE
    manifest['verification_reuse']='Completed applicable proof/object/identity checks reusable; no old replay for sourcecut/session/provider/process. Actual root/reviewer reading scopes retained separately.'
    manifest['catalogs'].append({'path':E+'/'+CNAME,'source_cut':cut,'scope':SCOPE,'sha256':records[E+'/'+CNAME]['sha256']})
    manifest['new_actual_torus_regular_slab_scope']={'module':M,'source_cut':cut,'public_propositions':[TARGET],'public_data':0,'actual_owned_constants':owned,'inventory_summary':inv,'catalog':E+'/'+CNAME,'scope':SCOPE,'publication':publication}
    for name in ['README.md','SCOPE.md','lakefile.toml']:manifest['files'][name]=records[name]['sha256']
    newpaths=sorted(p for p in records if p not in bm['files'])
    for path in newpaths:manifest['files'][path]=records[path]['sha256']
    mid=f.write(O/'SOURCE_MANIFEST.json',manifest);sid=text(O/'SOURCE_SHA256SUMS',''.join(manifest['files'][p]+'  '+p+'\n' for p in oldrows+newpaths))
    bs={x['path'] for x in raw['bindings']};allrecords={**records,'SOURCE_MANIFEST.json':mid,'SOURCE_SHA256SUMS':sid}
    plan={'status':'ROOT_ONLY_EXACT62_APPLY_AFTER_METADATA_PASS','expected_HEAD':cut,'qualified_baseline':f.BASE,'overlay_root':str(R/'overlay'),'destination_root':'/workspace/Math-curvature-20261026','apply':[],'skip':[],'cache_object_actions':[]}
    for path,value in sorted(allrecords.items()):plan['skip' if path in bs else 'apply'].append({'path':str(REL/path),'bytes':value['bytes'],'sha256':value['sha256']})
    pid=f.write(R/'APPLY_PLAN.json',plan)
    def registry():
        f.require(manifest['source_modules']==bm['source_modules']+[M+'.lean'] and manifest['targets']==bm['targets']+[TARGET],'One62 module/Prop append')
        f.require((len(manifest['source_modules']),len(manifest['targets']),manifest['inherited_input_count'])==(62,1132,32),'62/1132/32')
        return '1123Prop+9data/32; no public data'
    check('exact62_registration',registry)
    def prefixes():
        f.require(len(oldkeys)==6045 and list(manifest['files'])[:6045]==oldkeys,'6045 inherited manifest KEY prefix')
        f.require({p for p in oldkeys if bm['files'][p]!=manifest['files'][p]}=={'README.md','SCOPE.md','lakefile.toml'},'Only three inherited digest changes')
        rows=[line.split('  ',1) for line in (O/'SOURCE_SHA256SUMS').read_text().splitlines()]
        f.require([p for h,p in rows[:len(oldrows)]]==oldrows,'Independent checksum ROW prefix')
        f.require([p for h,p in rows[len(oldrows):]]==newpaths and {p:h for h,p in rows}==manifest['files'],'Append-only checksum association')
        f.require(not {'SOURCE_MANIFEST.json','SOURCE_SHA256SUMS'}&set(manifest['files']),'No self entries')
        return 'Separate inherited6045 key and independent row order; zero old hashes'
    check('separate_manifest_key_and_checksum_row_prefixes',prefixes)
    def lakecheck():
        old=tomllib.loads((snap/'lakefile.toml').read_text());new=tomllib.loads(lake)
        f.require(new['defaultTargets']==old['defaultTargets']+[M] and new['lean_lib']==old['lean_lib']+[{'name':M}],'One library/default target append')
        f.require(all(new[k]==old[k] for k in old if k not in ['defaultTargets','lean_lib']),'All other Lake fields unchanged')
        return 'One library/default target; no build'
    check('Lake62_append_only',lakecheck)
    def evidence():
        f.require(sum(inv['counts'].values())==owned and inv['standard_three_guard'].startswith('PASS'),'Actual exhaustive owned inventory/std3 association')
        f.require(len(inv['foreign_generated_names'])==inv['foreign_generated_count'],'Foreign generated constants retained')
        rr={x['record_path']:x['record'] for x in raw['runs']}
        for key in ['strict','inventory','kernel','positive_controls']:f.require(rr[str(archive.record_path(c['qualification'][key]))]['exit_code']==0,'Stored '+key+' PASS')
        f.require(rr[str(archive.record_path(c['qualification']['negative']))]['exit_code']==1,'Actual sole negative rejection')
        f.require(len([x for x in raw['runs'] if 'leanchecker' in str(x['record']['command'])])==1,'Exactly one owned kernel')
        f.require(raw['actual_split_stream_files']==2*raw['actual_run_count'],'All original split streams')
        helpers=raw['production_helpers'];f.require(len(helpers)==c['expected_production_helper_count']<=3,'Actual contracted helper count')
        f.require(all(x['integration_count']==1 and x['helper_executions']==0 for x in helpers),'Each production original once/zero helper executions')
        ordinary=raw['ordinary_controls_custody'];f.require(ordinary['producer_authored'] and not ordinary['text_helper_authored'],'Ordinary Controls is producer-owned, no fourth text helper')
        f.require(c['negative_binding']['exactly_one_intendedFalse'] and c['negative_binding']['counterproof_in_passed_controls'],'Counterproof-qualified sole mutation')
        return 'Dynamic actual62 receipt schema/qualified source-controls-negative associations; no mathematical replay'
    check('retained62_evidence_and_helper_scope',evidence)
    def overlay():
        paths={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()}
        f.require(paths==set(allrecords) and len(plan['skip'])==5 and len(plan['apply'])==len(paths)-5,'Exact overlay/five installed bindings SKIP')
        f.require(not any(archive.artifact(Path(p)) for p in paths),'No actual binaries')
        f.require(not cp['copies'] and not cp['further_copy_actions'] and not plan['cache_object_actions'],'All object actions SKIP')
        return {'overlay_files':len(paths),'apply_files':len(plan['apply']),'binding_SKIP':5}
    check('exact_overlay_ALL_objects_SKIP',overlay)
    def provenance():
        f.require(c['root_reading_summary'] and c['reviewer_reading_summary'] and c['final_review_pass'],'Actual final reading scopes')
        f.require(publication['root_reading_verbatim']==reading and publication['packager_independent_review_credit']==0 and publication['packager_is_62_proof_author'],'Honest actual reading/credit')
        f.require(publication['historical_pending_records_preserved'] and publication['same_family_credit']==0,'Historical records/process retained')
        return 'Packager A proof authorship disclosed; no independent/inherited review credit; actual root/reviewer scopes distinct'
    check('honest_author_review_and_process_scopes',provenance)
    def parse():
        paths=[O/'SOURCE_MANIFEST.json',R/'APPLY_PLAN.json',R/'COPY_PLAN.json']+[O/E/n for n in ['RAW_EVIDENCE_CATALOG.json','PUBLICATION_CONTEXT.json','COPY_PLAN.json',CNAME]]
        for path in paths:f.read(path)
        return {'new_metadata_JSONs':len(paths),'old_raw_JSON_rechecks':0}
    check('new_metadata_JSON_parse',parse)
    counts={'modules':62,'written':1132,'Prop':1123,'data':9,'inputs':32,'manifest_entries':len(manifest['files']),'new_manifest_entries':len(newpaths),'overlay_files':len(allrecords),'apply_files':len(plan['apply']),'binding_SKIP':5,'actual_owned_constants':owned,'actual_runs':raw['actual_run_count'],'split_stream_files':raw['actual_split_stream_files'],'split_stream_bytes':raw['actual_split_stream_bytes'],'excluded_artifacts':len(raw['excluded_artifacts'])}
    result={'status':'NEW62_METADATA_ASSEMBLY_AND_BOUNDED_ASSOCIATIONS_PASS','source_cut':cut,'qualified_baseline':f.BASE,'counts':counts,'owned_constants':owned,'manifest_identity':mid,'sums_identity':sid,'catalog_identity':records[E+'/'+CNAME],'apply_plan_identity':pid,'object_action':'SKIP_ROOT_COPIED_ONCE','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ASSEMBLY_RESULT.json',result);print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':assemble()
