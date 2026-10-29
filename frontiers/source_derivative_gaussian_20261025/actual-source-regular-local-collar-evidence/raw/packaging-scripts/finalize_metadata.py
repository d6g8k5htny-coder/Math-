#!/usr/bin/env python3
"""Prepared stage66 metadata worker. Execute only after explicit final66 GO."""
from pathlib import Path
import copy,json,tomllib
import custody as f
import archive_prepare as archive

R,P,U,B,A,E=f.R,f.P,f.U,f.B,f.A,f.E
REL=Path('frontiers/source_derivative_gaussian_20261025')
O=R/'overlay'/REL
M='SourceActualRegularLocalCollar'
TARGET='I4SourceActualRegularLocalCollar.actualSource_quotient_regular_local_collar'
CNAME='ACTUAL_REGULAR_LOCAL_COLLAR_EVIDENCE_CATALOG.json'
META=['README.md','SCOPE.md','lakefile.toml','SOURCE_MANIFEST.json','SOURCE_SHA256SUMS']
SCOPE='Actual nonzero-fderiv quotient regular collar: positive original period/sample and actual fderiv nonzero, no global hm. For EVERY prescribed open O obtain ONE rho/phi, centered at the actual quotient point, source contained in O, exact finite-Pi2 target ball, and ordered actual field identity F=c+coordinate1. The SAME phi/rho serves ALL |epsilon|<rho, with NONEMPTY path-connected CLOSED uppercuts AND level slices. Derive the physical triangular continuous-linear equivalence/actual IFT and public quotient descent; no64/65 mathematical dependency, supplied desired chart/certificate, torus C1 atlas or norm-isometry premise. Sole public Prop/no public data.'

def check(name,action):
    path=R/'VALIDATION_PROGRESS.jsonl'
    rows=[json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    done=[row for row in rows if row['event']=='check_passed' and row['name']==name]
    if done:return done[-1]['detail']
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_started','name':name})
    try:detail=action()
    except BaseException as exc:
        f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_failed','name':name,'exception':repr(exc)});raise
    f.append('VALIDATION_PROGRESS.jsonl',{'event':'check_passed','name':name,'detail':detail})
    print('PASS '+name,flush=True)

def assemble():
    f.require(not (R/'ASSEMBLY_RESULT.json').exists(),'Completed66 metadata reusable; no restart')
    c=f.read(R/'FINAL_INPUTS.json');archive.gate(c);raw=archive.prepare(c);cut=c['source_cut']
    bm=f.read(B/'SOURCE_MANIFEST.json');snap=R/'published65-metadata'
    for name in META:
        record=c['baseline_metadata_identities'][name]
        f.copied(B/name,snap/name,record)
    oldkeys=list(bm['files'])
    oldrows=[line.split('  ',1)[1] for line in (snap/'SOURCE_SHA256SUMS').read_text().splitlines()]
    f.write(R/'BASELINE_BINDING.json',{'publication':f.BASE,'baseline_metadata_identities_reused':c['baseline_metadata_identities'],
        'manifest_key_sequence':oldkeys,'independent_checksum_row_sequence':oldrows,'old_hashes':0})
    records={}
    for path,record in list(f.identities().items()):
        source=Path(path)
        if A not in source.parents:continue
        relative=source.relative_to(A)
        dest=O/(relative.name if relative.parts[0]=='bindings' else relative)
        records[str(dest.relative_to(O))]=f.copied(source,dest,record)
    inv=c['inventory_summary'];reading=f.read(Path(c['root_reading_record']))
    publication={'status':'QUALIFIED66_SCRATCH_PROPOSAL_ROOT_APPLY_ONLY','source_cut':cut,'source_cut_parent':c['source_cut_parent'],
        'qualified_baseline65':f.BASE,'root_reading_verbatim':reading,'root_reading_summary':c['root_reading_summary'],
        'reviewer_reading_summary':c['reviewer_reading_summary'],'packager_is_66_proof_author':False,
        'packager_role':'66 metadata preparation only; historical65 script derivation does not assign proof authorship or review credit',
        'packager_independent_review_credit':0,'no_inherited65_review_credit':True,'historical_pending_records_preserved':True,
        'remote66publication_claimed':False,'hosted66CI_claimed':False,'scientific_effect':'NONE','same_family_credit':0}
    catalog={'module':M,'namespace':'I4SourceActualRegularLocalCollar','public_Prop_targets':[TARGET],'public_data':0,
        'scope':SCOPE,'source_cut':cut,'source_identity':c['source_identity'],'eligible_object_identity':c['eligible_object_identity'],
        'object_action':'SKIP_ROOT_COPIED_ONCE','actual_owned_constants':inv['all_module_index_owned_constants'],
        'inventory_summary':inv,'ordinary_inventory_summary':c['ordinary_inventory_summary'],
        'full_inventory_archive_path':c['inventory_archive_path'],'qualification_records':c['qualification'],
        'sole_negative':c['negative_binding'],'production_helper_integrations':raw['production_helpers'],
        'ordinary_controls_custody':raw['ordinary_controls_custody'],
        'kernel_coverage':'Exactly one final production named kernel; ordinary Controls/counterproof/sole importingFalse and complete ordinary inventory qualify separately, never covered by production kernel.',
        'actual_run_count':raw['actual_run_count'],'verification_run_count':raw['verification_run_count'],
        'documentary_run_count':raw['documentary_run_count'],'unlabeled_run_count':raw['unlabeled_run_count'],
        'actual_worker_split_stream_files':raw['actual_worker_split_stream_files'],
        'actual_worker_split_stream_bytes':raw['actual_worker_split_stream_bytes'],
        'documentary_capture_records':raw['documentary_capture_records'],
        'record_schema':'Actual66 dedicated receipts: scope_kind math/documentary, command_argv/cwd/start_utc/end_utc, before/after, before_snapshots dictionary with IDs from SAME receipt.before, streams dictionary, separate outer_capture_dir and entry_capture_dir. Dedicated wrappers record child_exit_code/ended_utc. INITIAL_EXTERNAL_FREEZE is a distinct earlier root65-labelled ORIGINAL triple-capture family; preserve its real labels/times, never count it as a dedicated mathematical worker.',
        'all_attempts_preserved':True,'initial_empty_metadata_issue_and_forward_fix_preserved':True,
        'raw_catalog':'RAW_EVIDENCE_CATALOG.json','publication':publication,
        'verification_reuse':'Reuse applicable completed source/math/strict/inventory/ONEkernel/ordinary/soleFalse/identity evidence; check only new metadata associations.',
        'canonical_authority':f.AUTHORITY,'link_delivery_not_reading':True,'scientific_effect':'NONE','same_family_credit':0}
    for name,value in [('RAW_EVIDENCE_CATALOG.json',raw),('PUBLICATION_CONTEXT.json',publication),(CNAME,catalog)]:
        records[E+'/'+name]=f.write(O/E/name,value)
    for name in c['curated_producer_files']:
        records[E+'/'+name]=f.copied(O/E/'raw/producer'/name,O/E/name,records[E+'/raw/producer/'+name])
    review=c['review_report_archive_path']
    records[E+'/AUTHOR_SIDE_REVIEW.md']=f.copied(O/E/review,O/E/'AUTHOR_SIDE_REVIEW.md',records[E+'/'+review])
    copyplan={'status':'SKIP_ALL_OWN_OLD_CONTROLS_HELPER_OBJECT_COPIES','root_copy_record':c['root_object_copy_record'],
        'eligible_own_object_identity':c['eligible_object_identity'],'copies':[],'further_copy_actions':[],
        'ordinary_control_objects_ineligible':True,'helper_inventory_old_objects_ineligible':True,'ilean_refreshes':0}
    records[E+'/COPY_PLAN.json']=f.write(O/E/'COPY_PLAN.json',copyplan);f.write(R/'COPY_PLAN.json',copyplan)
    body=f'''[{M}.lean]({M}.lean) appends exactly one actual quotient regular-local-collar proposition and no public data. {SCOPE}

Actual original period2 cos(pi*x)+2cos(pi*y), BOTH nonzero physical partial alternatives at (1/2,0) and (0,1/2), seam lift(-3/2,0), and prescribed physical E2 ambient O of radius1/8 exercise the public theorem. The SAME actual chart/radius serves zero and +/-rho/2 levels; exact inverse points give actual equality and distinctness, and CLOSED uppercut/level-slice membership. No norm isometry or64/65 mathematical result is used.

At most ONE complete PRIVATE physical-adapter TEXT original is first-frozen before one integration, with zero helper executions/hashes/objects. Producer owns quotient/geometry joins, all actual positives, all ordinary Controls/counterproof and actual amendments/executions. The sole mutation removes ONLY the actual nonzero-fderiv premise, retaining the SAME actual function/sample/carrier/center/target/source/field identity and all conclusions. At the SAME actual maximum0/c3, the inverse target point(0,rho/2) forces actual F>3 while the independently passed ordinary global bound gives F<=3. The public CLOSED ordinary mutation and its independently passed negation precede ONE importingFalse. There is no ordinary named kernel.

Qualified65 `{f.BASE}` appends to66modules/1136written=1127Prop+9data/32inputs. Production owned count {inv['all_module_index_owned_constants']} and separate ordinary inventory remain dynamic stored final evidence. Actual dedicated producer workers {raw['actual_run_count']} = {raw['verification_run_count']} mathematical + {raw['documentary_run_count']} documentary + {raw['unlabeled_run_count']} unlabeled; {raw['actual_worker_split_stream_files']} original worker streams/{raw['actual_worker_split_stream_bytes']}B. Initial external freeze/root65-labelled original wrappers and later dedicated66 wrapper families remain separately attributed. Every actual source/harness/context/runner version, initial originals, full actual patches, ACK/freeze/integration, development failure and capture limit is retained. Initial avoidable EMPTY metadata hash is disclosed; forward fix uses known EMPTY identity without replaying bootstrap.

Root reading: {c['root_reading_summary']}. Nonauthor technical review: {c['reviewer_reading_summary']}. Literal FULL source/evidence reading and structured/bounded aggregate reading remain distinct; links/paths/receipt delivery do not claim reading. Current packager66 proof-authorFALSE/independentcredit0/scienceNONE/samefamily0; historical baseline-script provenance does not assign current proof/review roles. Root ONLY sourcecut, one eligible own-object copy, shared metadata application/Git/external normal publication. Five installed bindings and ALL objects SKIP after root copy once. Qualified65 CI is not66 CI. Four future67 root EXTRA docs are excluded66archive/manifest/registry; no future seat. OpenDraft/noReady/noMerge. Global lowerseparation/finiteadjacency/criticalevents/elder/count/Borel/Rice/PairLaw/Parent remain OPEN.
'''
    for name,title in [('README.md','# Actual quotient regular local collar'),('SCOPE.md','# Proposed66 modules/1136 written/32 inputs')]:
        records[name]=f.text(O/name,title+'\n\n'+body+'\n---\n\n# Historical qualified65 context preserved verbatim\n\n'+(snap/name).read_text())
    lake=(snap/'lakefile.toml').read_text();marker='"SourceActualSaddleUppercuts"]'
    f.require(lake.count(marker)==1,'Unique inherited65 final default target')
    lake=lake.replace(marker,'"SourceActualSaddleUppercuts", "'+M+'"]')+'\n[[lean_lib]]\nname = "'+M+'"\n'
    records['lakefile.toml']=f.text(O/'lakefile.toml',lake)
    manifest=copy.deepcopy(bm);manifest['source_modules'].append(M+'.lean');manifest['targets'].append(TARGET)
    manifest['qualification_role']='Root proposal66/1136written=1127Prop+9data/32 against qualified65 '+f.BASE
    manifest['verification_reuse']='Completed applicable verification reusable across agents/sessions/heads; provider-distinct process tracked separately.'
    manifest['catalogs'].append({'path':E+'/'+CNAME,'source_cut':cut,'scope':SCOPE,'sha256':records[E+'/'+CNAME]['sha256']})
    manifest['new_actual_regular_local_collar_scope']={'module':M,'source_cut':cut,'public_propositions':[TARGET],'public_data':0,
        'inventory_summary':inv,'ordinary_inventory_summary':c['ordinary_inventory_summary'],'catalog':E+'/'+CNAME,'scope':SCOPE,'publication':publication}
    for name in ['README.md','SCOPE.md','lakefile.toml']:manifest['files'][name]=records[name]['sha256']
    newpaths=sorted(path for path in records if path not in bm['files'])
    for path in newpaths:manifest['files'][path]=records[path]['sha256']
    mid=f.write(O/'SOURCE_MANIFEST.json',manifest)
    sid=f.text(O/'SOURCE_SHA256SUMS',''.join(manifest['files'][path]+'  '+path+'\n' for path in oldrows+newpaths))
    installed={row['path'] for row in raw['bindings']}
    allrecords={**records,'SOURCE_MANIFEST.json':mid,'SOURCE_SHA256SUMS':sid}
    plan={'status':'ROOT_ONLY_EXACT66_APPLY_AFTER_METADATA_PASS','expected_HEAD':cut,'qualified_baseline':f.BASE,
        'overlay_root':str(R/'overlay'),'destination_root':'/workspace/Math-curvature-20261026','apply':[],'skip':[],'cache_object_actions':[]}
    for path,row in sorted(allrecords.items()):
        plan['skip' if path in installed else 'apply'].append({'path':str(REL/path),'bytes':row['bytes'],'sha256':row['sha256']})
    pid=f.write(R/'APPLY_PLAN.json',plan)
    def registry():
        f.require(manifest['source_modules']==bm['source_modules']+[M+'.lean'] and manifest['targets']==bm['targets']+[TARGET],'One66 module/Prop append')
        f.require((len(manifest['source_modules']),len(manifest['targets']),manifest['inherited_input_count'])==(66,1136,32),'66/1136/32')
        return '1127Prop+9data/32; sole public Prop/no data'
    check('exact66_registration',registry)
    def prefixes():
        f.require(len(oldkeys)==9685 and list(manifest['files'])[:9685]==oldkeys,'Inherited9685 manifest KEY prefix')
        f.require({path for path in oldkeys if bm['files'][path]!=manifest['files'][path]}=={'README.md','SCOPE.md','lakefile.toml'},'Only three inherited digest changes')
        rows=[line.split('  ',1) for line in (O/'SOURCE_SHA256SUMS').read_text().splitlines()]
        f.require([path for digest,path in rows[:len(oldrows)]]==oldrows,'Independent checksum ROW prefix')
        f.require([path for digest,path in rows[len(oldrows):]]==newpaths and dict((path,digest) for digest,path in rows)==manifest['files'],'Append-only checksum association')
        f.require(not {'SOURCE_MANIFEST.json','SOURCE_SHA256SUMS'}&set(manifest['files']),'No self entries')
        return 'Separate inherited9685 KEY and independent ROW prefixes; no old hashes'
    check('separate_manifest_key_and_checksum_row_prefixes',prefixes)
    def lakecheck():
        old=tomllib.loads((snap/'lakefile.toml').read_text());new=tomllib.loads(lake)
        f.require(new['defaultTargets']==old['defaultTargets']+[M] and new['lean_lib']==old['lean_lib']+[{'name':M}],'One library/default target append')
        f.require(all(new[key]==old[key] for key in old if key not in ['defaultTargets','lean_lib']),'All other Lake fields retained')
        return 'One library/default target; no build'
    check('Lake66_append_only',lakecheck)
    def evidence():
        f.require(sum(inv['counts'].values())==inv['all_module_index_owned_constants'] and inv['standard_three_guard'].startswith('PASS'),'Dynamic full production inventory/std3')
        f.require(len(inv['foreign_generated_names'])==inv['foreign_generated_count'],'Foreign-generated classifications retained')
        receipts={row['record_path']:row['record'] for row in raw['runs']}
        for key in ['strict','inventory','kernel','positive_controls','ordinary_inventory']:
            selected=receipts[str(archive.record_path(c['qualification'][key]))]
            f.require(selected['exit_code']==0 and selected['spawn_or_worker_exception'] is None,'Stored '+key+' PASS without spawn exception')
        selected=receipts[str(archive.record_path(c['qualification']['negative']))]
        f.require(selected['exit_code']==1 and selected['spawn_or_worker_exception'] is None,'Stored sole negative expected exit1 without spawn exception')
        f.require(sum('leanchecker' in str(row['record']['command_argv']) for row in raw['runs'])==1,'Exactly one final production named kernel')
        f.require(raw['actual_worker_split_stream_files']==2*raw['actual_run_count'],'All actual dedicated worker split streams')
        helpers=raw['production_helpers']
        f.require(len(helpers)==c['expected_production_helper_count']<=1,'At most one contracted production helper')
        f.require(all(row['integration_count']==1 and row['helper_executions']==0 for row in helpers),'Original once integrated, zero helper execution')
        ordinary=raw['ordinary_controls_custody'];oi=c['ordinary_inventory_summary'];negative=c['negative_binding']
        f.require(ordinary['producer_authored'] and not ordinary['text_helper_authored'] and ordinary['extra_ordinary_text_helper_count']==0,'Producer-only ordinary Controls')
        f.require(not ordinary['production_kernel_coverage'] and oi['named_kernel_count']==0,'Ordinary qualification distinct from production kernel')
        f.require(sum(oi['counts'].values())==oi['all_module_index_owned_constants'] and oi['standard_three_guard'].startswith('PASS'),'Separate complete ordinary inventory/std3')
        f.require(negative['counterproof_in_passed_controls'] and negative['exactly_one_intendedFalse'] and negative['unsolved_False_count']==1,'Passed counterproof before sole importingFalse')
        f.require(negative['actual_mutation']=='Remove ONLY actual nonzero-fderiv premise; SAME actual function/sample/carrier/center/source/target/field identity and conclusions','Exact66 sole mutation')
        return 'Stored actual66 strict/inventory/ONEkernel/ordinary/soleFalse/helper associations; no mathematics replay'
    check('retained66_evidence_and_helper_scope',evidence)
    def overlay():
        paths={str(path.relative_to(O)) for path in O.rglob('*') if path.is_file()}
        f.require(paths==set(allrecords) and len(plan['skip'])==5 and len(plan['apply'])==len(paths)-5,'Exact overlay/five installed bindings SKIP')
        f.require(not any(archive.artifact(path) for path in paths),'No actual binary/cache/index payload')
        f.require(not copyplan['copies'] and not copyplan['further_copy_actions'] and not plan['cache_object_actions'],'ALL objects SKIP')
        return {'overlay_files':len(paths),'apply_files':len(plan['apply']),'binding_SKIP':5}
    check('exact_overlay_ALL_objects_SKIP',overlay)
    def provenance():
        f.require(c['root_reading_summary'] and c['reviewer_reading_summary'] and c['final_review_pass'],'Actual final root/nonauthor reading scopes')
        f.require(publication['root_reading_verbatim']==reading and not publication['packager_is_66_proof_author'] and publication['packager_independent_review_credit']==0,'Correct current roles/credit')
        f.require(publication['historical_pending_records_preserved'] and publication['same_family_credit']==0,'Historical records/provider process retained')
        return 'Actual separate FULL/structured/bounded reading; current packager no proof/review credit; historical script provenance separate'
    check('honest_author_review_and_process_scopes',provenance)
    def parse():
        paths=[O/'SOURCE_MANIFEST.json',R/'APPLY_PLAN.json',R/'COPY_PLAN.json']+[O/E/name for name in ['RAW_EVIDENCE_CATALOG.json','PUBLICATION_CONTEXT.json','COPY_PLAN.json',CNAME]]
        for path in paths:f.read(path)
        return {'new_metadata_JSONs':len(paths),'old_raw_JSON_rechecks':0}
    check('new_metadata_JSON_parse',parse)
    counts={'modules':66,'written':1136,'Prop':1127,'data':9,'inputs':32,'manifest_entries':len(manifest['files']),
        'new_manifest_entries':len(newpaths),'overlay_files':len(allrecords),'apply_files':len(plan['apply']),'binding_SKIP':5,
        'actual_owned_constants':inv['all_module_index_owned_constants'],'actual_runs':raw['actual_run_count'],
        'verification_runs':raw['verification_run_count'],'documentary_runs':raw['documentary_run_count'],
        'unlabeled_runs':raw['unlabeled_run_count'],'worker_split_stream_files':raw['actual_worker_split_stream_files'],
        'worker_split_stream_bytes':raw['actual_worker_split_stream_bytes'],'excluded_artifacts':len(raw['excluded_artifacts'])}
    result={'status':'NEW66_METADATA_ASSEMBLY_AND_BOUNDED_ASSOCIATIONS_PASS','source_cut':cut,'qualified_baseline':f.BASE,
        'counts':counts,'manifest_identity':mid,'sums_identity':sid,'catalog_identity':records[E+'/'+CNAME],
        'apply_plan_identity':pid,'object_action':'SKIP_ROOT_COPIED_ONCE','old_payload_hashes':0,'proof_replays':0}
    f.write(R/'ASSEMBLY_RESULT.json',result);print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':assemble()
