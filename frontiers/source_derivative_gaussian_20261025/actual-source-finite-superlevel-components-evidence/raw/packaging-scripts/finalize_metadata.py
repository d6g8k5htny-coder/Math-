#!/usr/bin/env python3
"""Prepared63 metadata worker. Execute only after explicit final root GO."""
from pathlib import Path
import copy,json,tomllib
import custody as f
import archive_prepare as archive
R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
REL=Path('frontiers/source_derivative_gaussian_20261025');O=R/'overlay'/REL
M='SourceActualFiniteSuperlevelComponents'
TARGET='I4SourceActualFiniteSuperlevelComponents.actualSource_finite_closedSuperlevel_components'
CNAME='ACTUAL_FINITE_SUPERLEVEL_COMPONENTS_EVIDENCE_CATALOG.json'
META=['README.md','SCOPE.md','lakefile.toml','SOURCE_MANIFEST.json','SOURCE_SHA256SUMS']
BASE_MANIFEST='699faad58606c9eb7b0a5d2eb4c875449114c700d4c096d2c967fb2a42c3235b'
BASE_SUMS='8d171a818cc01dd4e53a6bdb5442401819a2ca5e4e4d6e7a79d8c2d014174145'
SCOPE='Finite actual closed-superlevel path components on the SAME product AddCircle torus: positive L, original SmoothSample, genuine literal IsMorseDistinct of the physical actualField imply FOR EVERY real a, Finite (ZerothHomotopy (superlevel_set actualTorusField (-a))). Derive private/local CompactSpace and LocallyPathConnectedSpace of each literal CLOSED subtype using actual compact torus/field continuity and qualified61 PUBLIC every-open-neighborhood basis; consume the existing Mathlib finite path-components instance directly. No supplied geometry/count/census/finite-cover certificate, public Fintype/enumeration/count, duplicate finite-subcover engine, source61 private input or source62 dependency.'
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
    f.require(not (R/'ASSEMBLY_RESULT.json').exists(),'Completed63 metadata is reusable; never restart')
    c=f.read(R/'FINAL_INPUTS.json');archive.gate(c);raw=archive.prepare(c);cut=c['source_cut']
    bm=f.read(B/'SOURCE_MANIFEST.json');snap=R/'published62-metadata'
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
    publication={'status':'QUALIFIED63_SCRATCH_PROPOSAL_ROOT_APPLY_ONLY','source_cut':cut,'source_cut_parent':c['source_cut_parent'],'qualified_baseline62':f.BASE,'root_reading_verbatim':reading,'root_reading_summary':c['root_reading_summary'],'reviewer_reading_summary':c['reviewer_reading_summary'],'packager_is_63_proof_author':False,'packager_proof_role':'63 metadata preparation only; prior62A authorship does not become63 proof authorship','packager_independent_review_credit':0,'no_inherited62_review_credit':True,'historical_pending_records_preserved':True,'remote62publication_claimed':False,'hosted62CI_claimed':False,'scientific_effect':'NONE','same_family_credit':0}
    catalog={'module':M,'namespace':'I4SourceActualFiniteSuperlevelComponents','public_Prop_targets':[TARGET],'public_data':0,'scope':SCOPE,'source_cut':cut,'source_identity':c['source_identity'],'eligible_object_identity':c['eligible_object_identity'],'object_action':'SKIP_ROOT_COPIED_ONCE','actual_owned_constants':owned,'inventory_summary':inv,'full_inventory_archive_path':c['inventory_archive_path'],'qualification_records':c['qualification'],'sole_negative':c['negative_binding'],'production_helper_integrations':raw['production_helpers'],'ordinary_controls_custody':raw['ordinary_controls_custody'],'kernel_coverage':'Owned production including one private LP adapter and private actual extreme-level compact/local-topology/Finite consumers. Private3singleton/4empty/-4whole positives do NOT exercise the full global-hm-to61-public-to-subtype route. Separate ordinary Controls derives actual global hm ONCE and invokes the new ALL-LEVEL public endpoint; ordinary counterproof/soleFalse have separate qualification and no production-kernel coverage.','actual_run_count':raw['actual_run_count'],'actual_split_stream_files':raw['actual_split_stream_files'],'actual_split_stream_bytes':raw['actual_split_stream_bytes'],'record_schema':'receipt.json/before/after/snapshots[{immutable_path,existing_identity}]/runner_version/runner_history/started_utc/ended_utc plus stdout.log/stderr.log; all actual runner/context versions retained. Actual timeout124 is resource failure, never intended mathematical False.','all_attempts_preserved':True,'raw_catalog':'RAW_EVIDENCE_CATALOG.json','publication':publication,'verification_reuse':'All applicable completed source/math/identity/strict/inventory/ONEkernel/Controls/soleFalse evidence reused. Only new metadata associations checked.','canonical_authority':f.AUTHORITY,'link_delivery_not_reading':True,'scientific_effect':'NONE','same_family_credit':0}
    for name,value in [('RAW_EVIDENCE_CATALOG.json',raw),('PUBLICATION_CONTEXT.json',publication),(CNAME,catalog)]:records[E+'/'+name]=f.write(O/E/name,value)
    for name in c['curated_producer_files']:records[E+'/'+name]=f.copied(O/E/'raw/producer'/name,O/E/name,records[E+'/raw/producer/'+name])
    rp=c['review_report_archive_path'];records[E+'/AUTHOR_SIDE_REVIEW.md']=f.copied(O/E/rp,O/E/'AUTHOR_SIDE_REVIEW.md',records[E+'/'+rp])
    cp={'status':'SKIP_ALL_OWN_OLD_CONTROLS_HELPER_OBJECT_COPIES','root_copy_record':c['root_object_copy_record'],'eligible_own_object_identity':c['eligible_object_identity'],'copies':[],'further_copy_actions':[],'ordinary_control_objects_ineligible':True,'helper_inventory_old_objects_ineligible':True,'ilean_refreshes':0}
    records[E+'/COPY_PLAN.json']=f.write(O/E/'COPY_PLAN.json',cp);f.write(R/'COPY_PLAN.json',cp)
    body=f'''[{M}.lean]({M}.lean) appends exactly one actual-source ALL-LEVEL finiteness proposition and no public data. Positive L, the SAME original smooth sample/physical actualField/product-AddCircle descended field and genuine IsMorseDistinct imply, for EVERY real a, Finite of the actual closed-superlevel ZerothHomotopy at time -a. No supplied compactness/local-PC/finite cover/component census certificate, Fintype/enumeration/count object or public instance replaces that Prop.

Private/local compactness follows from the actual compact torus and continuous descended field. Qualified61's PUBLIC every-open-neighborhood closed-superlevel basis supplies the actual subtype LocallyPathConnectedSpace adapter. The existing Mathlib Finite path-components instance is consumed directly; no duplicate finite-subcover proof engine or61-private implementation/fixture/control binary is copied. Source62 is not a dependency. No uniform cardinal bound or exact component count is asserted.

The SAME primary original period2 field is cos(pi*x)+2*cos(pi*y). Private production positives at3(singleton),4(empty) and-4(WHOLE NONEMPTY torus) exercise actual compactness/local-topology/Finite use; they do NOT exercise the complete global-hm-to61-to-subtype route. Separate ordinary Controls derives genuine global fixture MorseDistinct ONCE, then invokes the new ALL-LEVEL endpoint. The sole mutation swaps only the quotient torus for FULL physical cover at unchanged CLOSED level3, SAME source/period/genuine hm. Its passed independent counterproof uses actual Nat maxima (2n,0), injects their physical component classes by odd-x IVT, and proves NOT Finite before ONE importing False. No level, amplitude, strictness, premise or sample mutation is introduced.

Qualified62 `{f.BASE}` appends to63 modules/1133 written=1124Prop+9data/32 inputs. All {owned} actual owned constants/private/generated/foreign-generated/std3 classifications and all {raw['actual_run_count']} actual calls/{raw['actual_split_stream_files']} full original split streams/{raw['actual_split_stream_bytes']}B are retained. Every source/harness/runner/context version/personal ACK/freeze/complete original/FULL actual amendment/failure remains archived. Counts derive from final records. Exactly one complete PRIVATE production LP TEXT original and one separately complete ordinary Controls TEXT original freeze before ONE integration each; helper executions/hashes/objects are zero, producer owns actual amendments/executions. Production kernel does NOT cover ordinary Controls. Five installed bindings and ALL object/cache actions SKIP after root's single final eligible own copy.

Root reading: {c['root_reading_summary']}. Final reviewer reading: {c['reviewer_reading_summary']}. Packager supplied63 metadata only, has NO63 proof authorship and earns no independent review credit; prior62A proof authorship is disclosed separately and transfers no63 role/credit. No prior62 review transfers to63. Root alone applies/publishes; no remote63 publication or hosted63 CI is claimed. Historical process, actual path/context races and resource failures remain verbatim. ScientificNONE/same-family0; applicable verification remains reusable and provider-distinct process separate. No critical-event geometry, exhaustive H0/elder labels, once-counting, Borel/Rice/Campbell, PairLaw or Parent conclusion follows from this finiteness leaf.
'''
    for name,title in [('README.md','# Finite actual closed-superlevel path components'),('SCOPE.md','# Proposed63 modules/1133 written/32 inputs')]:records[name]=text(O/name,title+'\n\n'+body+'\n---\n\n# Historical qualified62 context preserved verbatim\n\n'+(snap/name).read_text())
    lake=(snap/'lakefile.toml').read_text();marker='"SourceActualTorusRegularSlab"]';f.require(lake.count(marker)==1,'Unique inherited62 last target')
    lake=lake.replace(marker,'"SourceActualTorusRegularSlab", "'+M+'"]')+'\n[[lean_lib]]\nname = "'+M+'"\n';records['lakefile.toml']=text(O/'lakefile.toml',lake)
    manifest=copy.deepcopy(bm);manifest['source_modules'].append(M+'.lean');manifest['targets'].append(TARGET)
    manifest['qualification_role']='Root proposal63/1133written=1124Prop+9data/32 against qualified62 '+f.BASE
    manifest['verification_reuse']='Completed applicable proof/object/identity checks reusable; no old replay for sourcecut/session/provider/process. Actual root/reviewer reading scopes retained separately.'
    manifest['catalogs'].append({'path':E+'/'+CNAME,'source_cut':cut,'scope':SCOPE,'sha256':records[E+'/'+CNAME]['sha256']})
    manifest['new_actual_finite_superlevel_components_scope']={'module':M,'source_cut':cut,'public_propositions':[TARGET],'public_data':0,'actual_owned_constants':owned,'inventory_summary':inv,'catalog':E+'/'+CNAME,'scope':SCOPE,'publication':publication}
    for name in ['README.md','SCOPE.md','lakefile.toml']:manifest['files'][name]=records[name]['sha256']
    newpaths=sorted(p for p in records if p not in bm['files'])
    for path in newpaths:manifest['files'][path]=records[path]['sha256']
    mid=f.write(O/'SOURCE_MANIFEST.json',manifest);sid=text(O/'SOURCE_SHA256SUMS',''.join(manifest['files'][p]+'  '+p+'\n' for p in oldrows+newpaths))
    bs={x['path'] for x in raw['bindings']};allrecords={**records,'SOURCE_MANIFEST.json':mid,'SOURCE_SHA256SUMS':sid}
    plan={'status':'ROOT_ONLY_EXACT63_APPLY_AFTER_METADATA_PASS','expected_HEAD':cut,'qualified_baseline':f.BASE,'overlay_root':str(R/'overlay'),'destination_root':'/workspace/Math-curvature-20261026','apply':[],'skip':[],'cache_object_actions':[]}
    for path,value in sorted(allrecords.items()):plan['skip' if path in bs else 'apply'].append({'path':str(REL/path),'bytes':value['bytes'],'sha256':value['sha256']})
    pid=f.write(R/'APPLY_PLAN.json',plan)
    def registry():
        f.require(manifest['source_modules']==bm['source_modules']+[M+'.lean'] and manifest['targets']==bm['targets']+[TARGET],'One63 module/Prop append')
        f.require((len(manifest['source_modules']),len(manifest['targets']),manifest['inherited_input_count'])==(63,1133,32),'63/1133/32')
        return '1124Prop+9data/32; no public data'
    check('exact63_registration',registry)
    def prefixes():
        f.require(len(oldkeys)==6491 and list(manifest['files'])[:6491]==oldkeys,'6491 inherited manifest KEY prefix')
        f.require({p for p in oldkeys if bm['files'][p]!=manifest['files'][p]}=={'README.md','SCOPE.md','lakefile.toml'},'Only three inherited digest changes')
        rows=[line.split('  ',1) for line in (O/'SOURCE_SHA256SUMS').read_text().splitlines()]
        f.require([p for h,p in rows[:len(oldrows)]]==oldrows,'Independent checksum ROW prefix')
        f.require([p for h,p in rows[len(oldrows):]]==newpaths and {p:h for h,p in rows}==manifest['files'],'Append-only checksum association')
        f.require(not {'SOURCE_MANIFEST.json','SOURCE_SHA256SUMS'}&set(manifest['files']),'No self entries')
        return 'Separate inherited6491 key and independent row order; zero old hashes'
    check('separate_manifest_key_and_checksum_row_prefixes',prefixes)
    def lakecheck():
        old=tomllib.loads((snap/'lakefile.toml').read_text());new=tomllib.loads(lake)
        f.require(new['defaultTargets']==old['defaultTargets']+[M] and new['lean_lib']==old['lean_lib']+[{'name':M}],'One library/default target append')
        f.require(all(new[k]==old[k] for k in old if k not in ['defaultTargets','lean_lib']),'All other Lake fields unchanged')
        return 'One library/default target; no build'
    check('Lake63_append_only',lakecheck)
    def evidence():
        f.require(sum(inv['counts'].values())==owned and inv['standard_three_guard'].startswith('PASS'),'Actual exhaustive owned inventory/std3 association')
        f.require(len(inv['foreign_generated_names'])==inv['foreign_generated_count'],'Foreign generated constants retained')
        rr={x['record_path']:x['record'] for x in raw['runs']}
        for key in ['strict','inventory','kernel','positive_controls']:f.require(rr[str(archive.record_path(c['qualification'][key]))]['exit_code']==0,'Stored '+key+' PASS')
        f.require(rr[str(archive.record_path(c['qualification']['negative']))]['exit_code']==1,'Actual sole negative rejection')
        f.require(len([x for x in raw['runs'] if 'leanchecker' in str(x['record']['command'])])==1,'Exactly one owned kernel')
        f.require(raw['actual_split_stream_files']==2*raw['actual_run_count'],'All original split streams')
        helpers=raw['production_helpers'];f.require(len(helpers)==c['expected_production_helper_count']<=1,'Actual contracted helper count')
        f.require(all(x['integration_count']==1 and x['helper_executions']==0 for x in helpers),'Each production original once/zero helper executions')
        ordinary=raw['ordinary_controls_custody'];f.require(not ordinary['producer_authored'] and ordinary['text_helper_authored'] and ordinary['integration_count']==1 and ordinary['helper_executions']==0,'One separate ordinary Controls TEXT original, once/zero helper execution')
        f.require(c['negative_binding']['exactly_one_intendedFalse'] and c['negative_binding']['counterproof_in_passed_controls'],'Counterproof-qualified sole mutation')
        return 'Dynamic actual63 receipt schema/qualified source-controls-negative associations; no mathematical replay'
    check('retained63_evidence_and_helper_scope',evidence)
    def overlay():
        paths={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()}
        f.require(paths==set(allrecords) and len(plan['skip'])==5 and len(plan['apply'])==len(paths)-5,'Exact overlay/five installed bindings SKIP')
        f.require(not any(archive.artifact(Path(p)) for p in paths),'No actual binaries')
        f.require(not cp['copies'] and not cp['further_copy_actions'] and not plan['cache_object_actions'],'All object actions SKIP')
        return {'overlay_files':len(paths),'apply_files':len(plan['apply']),'binding_SKIP':5}
    check('exact_overlay_ALL_objects_SKIP',overlay)
    def provenance():
        f.require(c['root_reading_summary'] and c['reviewer_reading_summary'] and c['final_review_pass'],'Actual final reading scopes')
        f.require(publication['root_reading_verbatim']==reading and publication['packager_independent_review_credit']==0 and not publication['packager_is_63_proof_author'],'Honest actual reading/credit')
        f.require(publication['historical_pending_records_preserved'] and publication['same_family_credit']==0,'Historical records/process retained')
        return 'Packager63 proof-authorship FALSE/prior62A disclosed; no independent/inherited review credit; actual root/reviewer scopes distinct'
    check('honest_author_review_and_process_scopes',provenance)
    def parse():
        paths=[O/'SOURCE_MANIFEST.json',R/'APPLY_PLAN.json',R/'COPY_PLAN.json']+[O/E/n for n in ['RAW_EVIDENCE_CATALOG.json','PUBLICATION_CONTEXT.json','COPY_PLAN.json',CNAME]]
        for path in paths:f.read(path)
        return {'new_metadata_JSONs':len(paths),'old_raw_JSON_rechecks':0}
    check('new_metadata_JSON_parse',parse)
    counts={'modules':63,'written':1133,'Prop':1124,'data':9,'inputs':32,'manifest_entries':len(manifest['files']),'new_manifest_entries':len(newpaths),'overlay_files':len(allrecords),'apply_files':len(plan['apply']),'binding_SKIP':5,'actual_owned_constants':owned,'actual_runs':raw['actual_run_count'],'split_stream_files':raw['actual_split_stream_files'],'split_stream_bytes':raw['actual_split_stream_bytes'],'excluded_artifacts':len(raw['excluded_artifacts'])}
    result={'status':'NEW63_METADATA_ASSEMBLY_AND_BOUNDED_ASSOCIATIONS_PASS','source_cut':cut,'qualified_baseline':f.BASE,'counts':counts,'owned_constants':owned,'manifest_identity':mid,'sums_identity':sid,'catalog_identity':records[E+'/'+CNAME],'apply_plan_identity':pid,'object_action':'SKIP_ROOT_COPIED_ONCE','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ASSEMBLY_RESULT.json',result);print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':assemble()
