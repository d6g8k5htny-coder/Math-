#!/usr/bin/env python3
"""Compose the explicit final64 metadata input from frozen actual schemas; no hashes/checks."""
from pathlib import Path
from datetime import datetime,timezone
import json
R=Path('/workspace/scratch/actual-source-quotient-saddle-collar-packaging-proposal')
P=Path('/workspace/scratch/actual-source-quotient-saddle-collar-construct')
U=Path('/workspace/scratch/actual-source-quotient-saddle-collar-publication')
V=Path('/workspace/scratch/actual-source-quotient-saddle-collar-source-review')
def read(p):return json.loads(p.read_text())
g=read(U/'ROOT_FINALIZATION_GO.json');c=read(R/'FINAL_INPUTS.schema.json')
for key in ['status','all_math_complete','final_review_pass','source_cut_committed','own_object_copied_once','immutable_payloads_frozen','qualified_baseline','source_cut','source_cut_parent','source_identity','eligible_object_identity','root_object_copy_record','root_reading_record']:
 c[key]=g[key]
c['root_finalization_go']=str(U/'ROOT_FINALIZATION_GO.json')
root=read(U/'ROOT_READING.json');scope=read(V/'scope.json');inv=read(P/'INVENTORY.json');ctl=read(P/'CONTROL_IDS.json');closure=read(P/'FINAL_EXECUTION_COMPLETION.json');art=read(P/'ARTIFACT_IDENTITIES.json')
c['root_reading_summary']='Root FULL specified helper originals, final Controls/soleFalse and named final documents/captures; BOUNDED final production, inventory, execution index/manifest/allowlist and selected receipt fields. Full mathematical source/evidence/inventory coverage belongs to the nonauthor reviewer. Six earlier documentary outer streams/UTC absent; final entry UTC uninstrumented; one known context SHA recomputation disclosed. See verbatim ROOT_READING and separate final acceptance.'
c['reviewer_reading_summary']='Nonauthor final technical/custody PASS with no findings. Full final896-source coverage via previously full core plus complete new fixture tail/deltas; all96/rawaxioms;13 mathematical26 original streams and7 documentary14 worker streams plus final outer2/entry2; all343 artifacts/215 historical+18 active snapshots/375 paths and final closure. Actual duplicate-body reading reuse and six earlier outer/entry UTC limits remain explicit in all staged reports and scope.json; samefamily0/scienceNONE.'
paths=list(dict.fromkeys(read(P/'PACKAGING_ALLOWLIST.json')['textual_paths']+[g['producer_additive_closure']]))
files=[{'source':p,'archive_path':'raw/producer/'+str(Path(p).relative_to(P))} for p in paths]
files += [{'source':p,'archive_path':'raw/root/'+str(Path(p).relative_to(U))} for p in g['immutable_root_files']]
files += [{'source':p,'archive_path':'raw/review/'+str(Path(p).relative_to(V))} for p in g['immutable_review_files']]
files += [{'source':str(p),'archive_path':'raw/packaging-history/'+str(p.relative_to(R/'preparation-history'))} for p in sorted((R/'preparation-history').rglob('*')) if p.is_file()]
c['immutable_files']=files;c['immutable_directories']=[];c['excluded_artifact_directories']=[str(P/'build')]
ids={}
def add(path,x):
 if path and isinstance(x,dict) and 'bytes' in x and 'sha256' in x:
  ids[str(path)]={'source':str(path),'bytes':x['bytes'],'sha256':x['sha256']}
for x in art['artifacts']:add(x['path'],x)
for k in ['immutable_snapshot_bindings','active_final_snapshot_bindings']:
 for x in art[k]:add(x['immutable_path'],x['existing_identity'])
for x in read(P/'FINAL_DOCUMENT_IDS.json')['documents']:add(x['path'],x)
add(g['producer_additive_closure'],read(Path(g['closure_first_ID_record'])))
for x in read(U/'PRECODE64_IDENTITIES.json')['files']:
 add(U/Path(x['path']).name,x)
for side in ['worker','outer']:
 for key in ['stdout','stderr']:
  x=closure[side][key];add(x['path'],x)
for key in ['stdout','stderr']:
 add(closure['driver_entry'][key+'_path'],{'bytes':0,'sha256':'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'})
c['existing_file_identities']=list(ids.values())
c['run_records']=read(P/'EXECUTION_RECORD_INDEX.json')['receipt_paths']+[closure['worker']['receipt']]
c['curated_producer_files']=['REPORT.md','HANDOFF.md','PRODUCTION_QUALIFICATION.json','CONTROL_IDS.json','CONTROL_RECEIPT.json','INVENTORY.json','READ_SCOPE.md','READY.json','STREAM_COUNTS.json','FINAL_EXECUTION_COMPLETION.json','IDENTITY_CUSTODY_CLARIFICATION_001.json','OUTER_CAPTURE_SCOPE_001.json']
c['inventory_archive_path']='raw/producer/INVENTORY.json'
foreign=[x['name'] for x in inv['declarations'] if x['classification']=='foreign-namespace generated declaration']
c['inventory_summary']={'all_module_index_owned_constants':inv['total'],'authored_public_Prop':1,'authored_public_data':0,'counts':inv['counts'],'foreign_generated_names':foreign,'foreign_generated_count':len(foreign),'standard_three_guard':'PASS actual completed exhaustive inventory96; allowed propext/Classical.choice/Quot.sound; evidence reused','allowed_axioms':inv['allowed_axioms'],'coverage':inv['coverage']}
c['production_helper_integrations']=[]
for key in ['A','B']:
 h=read(P/'originals'/f'{key}_CUSTODY.json')
 c['production_helper_integrations'].append({'key':key+'-'+('chart' if key=='A' else 'geometry'),'record_path':f'raw/producer/originals/{key}_CUSTODY.json','integration_count':h['integrations'],'helper_executions':h['helper_executions'],'helper_hashes':h['helper_hashes'],'originals':h['originals'],'actual_full_patches':'ALL producer amendments retained in exact explicit allowlist; original custody preserved'})
c['ordinary_controls_custody']={'producer_authored':True,'text_helper_authored':False,'extra_ordinary_text_helper_count':0,'producer_controls_original_snapshot':'raw/producer/ORDINARY_INITIAL_BINDING.json and the exact initial source snapshot it binds','record_path':'raw/producer/CONTROL_IDS.json','actual_full_patch':'raw/producer/'+ctl['actual_full_patch'],'source_identity':ctl['source'],'ordinary_object_identity':ctl['ordinary_object'],'production_kernel_coverage':False}
c['review_report_archive_path']='raw/review/FINAL_CUSTODY.md'
c['qualification']=g['qualification']
c['negative_binding'].update({'counterproof_in_passed_controls':True,'exactly_one_intendedFalse':True,'ordinary_controls_object_identity':ctl['ordinary_object'],'negative_harness_identity':ctl['negative_harness'],'stdout_bytes':ctl['negative_stdout']['bytes'],'stderr_bytes':ctl['negative_stderr']['bytes'],'negative_stdout_identity':ctl['negative_stdout'],'negative_attempt_count':ctl['negative_attempt_count'],'counterproof':ctl['counterproof'],'actual_mutation':ctl['sole_mutation'],'production_kernel_does_not_cover_ordinary_controls':True})
c['packaging_scripts'] += ['prepare_final_inputs.py','prepare_inputs_capture.py','input-preparation-captures/started.json','input-preparation-captures/stdout.log','input-preparation-captures/stderr.log','input-preparation-captures/receipt.json']
c['documentary_capture_records']=[{'kind':'earlier_six_outer_limit','record_path':'raw/producer/OUTER_CAPTURE_SCOPE_001.json','worker_scope':'Six workers full original separate target streams/command/cwd/start/end/exit','outer_scope':'Only actual combined tool results; separate original outer files and external UTC absent. No fabrication/replay.'},{'kind':'actual_final_documentary_closure','record_path':'raw/producer/FINAL_EXECUTION_COMPLETION.json','counts':closure['final_worker_scope_counts'],'entry_external_UTC':'Uninstrumented; not conflated with child command UTC'},{'kind':'metadata_attempt_prospective','worker':'metadata-attempts/attempt-001/{started.json,stdout.log,stderr.log,execution_receipt.json}','outer':'launcher-captures/metadata-attempt-001/{started.json,stdout.log,stderr.log,receipt.json}','capture':'Prepared before execution; full original separate streams/commands/cwd/observed UTC/exit retained by frozen scripts.'}]
c['historical_identity_recalculation_disclosure']='ONE known A-context002 SHA recomputation by producer; original/helper custody unchanged and helper hashes0. No blanket zero historical identity-recalculation claim.'
c['root_immutable_snapshot_rule']='EXACT86 explicit root files and7 staged review files supplied by actual FINAL_GO. No later root application/publication tail or future65 document inclusion.'
out=R/'FINAL_INPUTS.json'
with out.open('x') as f:json.dump(c,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps({'status':'ACTUAL_FINAL64_INPUTS_COMPOSED_NO_HASH_OR_VALIDATION','producer_textual_paths':len(paths),'root_files':len(g['immutable_root_files']),'review_files':len(g['immutable_review_files']),'existing_identity_rows':len(ids),'actual_worker_receipts':len(c['run_records'])},sort_keys=True))
