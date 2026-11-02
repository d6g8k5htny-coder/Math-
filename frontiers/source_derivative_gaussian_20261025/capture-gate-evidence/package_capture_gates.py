from pathlib import Path
import json,re,shutil,datetime
root=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
out=Path('/workspace/scratch/capture-gate-evidence-packaging')
prod=Path('/workspace/scratch/quartic-capture-production')
prior=Path('/workspace/scratch/quartic-capture-algebra')
receipt=json.loads((prod/'qualification_receipt.json').read_text())
control=json.loads((prod/'CONTROL_HANDOFF.json').read_text())
inv=json.loads((prod/'PUBLIC_TARGETS.json').read_text())
raw=[]
def copy(src,rel,role):
    dst=out/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    raw.append({'original_path':str(src),'packaged_path':str(rel),'role':role,'bytes_copied':dst.stat().st_size,'packaging_computed_hash':False})
def write(name,data):
    (out/name).write_text(json.dumps(data,indent=2)+'\n')
copy(root/'SourceQuarticCaptureAlgebra.lean',Path('sources/SourceQuarticCaptureAlgebra.lean'),'final qualified source; SHA reused from completed receipt')
copy(root/'SOURCE_QUARTIC_CAPTURE_ALGEBRA.md',Path('contracts/SOURCE_QUARTIC_CAPTURE_ALGEBRA.md'),'frozen production contract; byte copy only')
for f in sorted(prod.iterdir()):
    if f.is_file(): copy(f,Path('raw/production')/f.name,'existing new-production compile/kernel/audit/control and failure history; no execution')
for f in sorted(prior.iterdir()):
    if f.is_file() and '.olean' not in f.name and f.suffix!='.ilean':
        copy(f,Path('raw/reused-scratch21')/f.name,'previously completed scratch21 proof evidence and controls, reused without execution')
copy(prod/'qualification_receipt.json',Path('qualification_receipt.json'),'completed production qualification aggregate unchanged')
text=(out/'sources/SourceQuarticCaptureAlgebra.lean').read_text()
all_decl=[]
for n,line in enumerate(text.splitlines(),1):
    m=re.match(r'(?:(private) )?(theorem|lemma|def|abbrev|instance)\s+(\w+)',line)
    if m: all_decl.append({'name':'I4QuarticCaptureAlgebra.'+m[3],'source_spelling':m[3],'kind':m[2],'private':bool(m[1]),'source_line':n})
proofs=[d for d in all_decl if not d['private'] and d['kind'] in ('theorem','lemma','instance')]
defs=[d for d in all_decl if not d['private'] and d['kind'] in ('def','abbrev')]
private=[d for d in all_decl if d['private']]
# Static inventory projection only; completed reports are not rerun.
for d in proofs:d.update({'direct_print_axioms_report':'raw/production/audit01.log','axioms_from_completed_audit':['propext','Classical.choice','Quot.sound'],'registration_proof_target':True})
for d in defs:d.update({'registration_proof_target':False,'direct_proof_audit_claimed':False,'kernel_covered_as_new_module_declaration':True})
write('CAPTURE_GATES_PUBLIC_INVENTORY.json',{'scope_id':'SOURCE_QUARTIC_CAPTURE_ALGEBRA_ONLY_20261026','module':'SourceQuarticCaptureAlgebra','public_proof_count':28,'public_definition_count':6,'named_instance_count':0,'public_declaration_total':34,'public_proofs':proofs,'definitions':defs,'count_rule':'28 public theorem proof targets; six defs recorded separately, including two Prop-valued definitions. No type/def inflation.'})
write('PUBLIC_PROOF_NAMES_APPEND.json',{'module':'SourceQuarticCaptureAlgebra','proof_target_count':28,'names':inv['public_proofs'],'root_owns_append':True})
(out/'PUBLIC_PROOF_NAMES_APPEND.txt').write_text('\n'.join(inv['public_proofs'])+'\n')
write('DEFINITIONS_SEPARATE.json',{'count':6,'definitions':defs,'not_added_to_public_proof_count':True})
write('PRIVATE_DECLARATIONS_KERNEL_ONLY.json',{'count':len(private),'source_spelling_names_only':True,'private_kernel_covered_not_public_audit_targets':private,'not_added_to_public_proof_count':True})
base={'qualified_modules':24,'public_proof_instance_declaration_targets':615,'exact_inputs':23,'reference_only':True,'copied_hashed_or_rechecked':False,'reference':'../topology-evidence/TOPOLOGY_MEMBERSHIP.json and root current baseline instruction'}
rawref={'module':'SourceRawPinConditioning','root_label':'newRaw7','source_sha256':'77e521c7fc3fc3da1c922a4ef547b065be58b232b321480948c8fe50d76c2aa5','artifact_sha256':'757a9326500ed5ed1205eaccde2d0480aefafeceb66a3122852223c57cb2e090','qualification_receipt_reference':'/workspace/scratch/raw-pin-conditioning/QUALIFICATION_RECEIPT.json','reference_only':True,'direct_dependency_of_this_module':False,'registration_owned_by_root':True}
member={'scope_id':'SOURCE_QUARTIC_CAPTURE_ALGEBRA_ONLY_20261026','modules':[{'module':'SourceQuarticCaptureAlgebra','source_sha256':receipt['source_sha256'],'olean_sha256':receipt['artifact_sha256'],'public_proof_targets':28,'public_definitions':6,'named_instances':0,'private_kernel_only_declarations':len(private),'public_declarations_total':34}],'new_modules':1,'new_public_proof_targets':28,'new_definitions_separate':6,'baseline_by_reference':base,'raw_successor_by_reference':rawref,'registration_aggregation_owned_by_root':True,'no_cumulative_target_total_fabricated':True,'combined_build_or_baseline_gate_claimed':False}
write('CAPTURE_GATES_MEMBERSHIP.json',member)
record_index=[]
for item in raw:
    if not item['packaged_path'].endswith('.json'):continue
    try:data=json.loads((out/item['packaged_path']).read_text())
    except (ValueError,UnicodeDecodeError):continue
    if any(k in data for k in ('command','command_argv','exit','exit_code','exit_code_observed')):
        record_index.append({'packaged_path':item['packaged_path'],'original_path':item['original_path'],'scope':'REUSED_SCRATCH21' if '/reused-scratch21/' in item['packaged_path'] else 'NEW_PRODUCTION','actual_record_unchanged':data})
write('EXECUTION_RECORD_INDEX.json',{'role':'Projection of genuine existing subprocess records; no subprocess or proof checker executed by packaging','records':record_index})
write('AUTHOR_HELPER_LINEAGE.json',receipt['author_lineage'])
write('CONTROL_AND_HELPER_HISTORY.json',{'production_records':receipt['records'],'production_failed_history':receipt['failed_history'],'new_control_handoff':control,'prior_scratch21_evidence':'raw/reused-scratch21/EVIDENCE.json','source_integrity_binding':{'final_source_sha256':receipt['source_sha256'],'final_object_sha256':receipt['artifact_sha256'],'origin':'Existing completed production and control records; not recomputed during packaging'},'all_helpers_same_family':'OpenAI/Codex; no new scientific review credit','unknown_values':'Historical scratch attempt source hashes were not captured; original receipts explicitly retain UNKNOWN/not captured instead of invention.'})
write('REVIEW_SCOPE.json',{'scientific_effect':'NONE','paper_certificate':'Already closed conditional LM001 Q2/Q3 analytic certificate, inherited separately','new_code_alignment_review':'Provider-distinct scientific review remains separate; none claimed by authors or packaging','qualified_mathematics':'New source-only polynomial and actual drift transfer as completed receipt','not_claimed':['ODE existence','selected unstable branch','complete trajectory/capture','event measurability','geometric Palm identity','elder/counting','P0.2 closure']})
catalog={'schema_version':1,'scope_id':'SOURCE_QUARTIC_CAPTURE_ALGEBRA_ONLY_20261026','role':'Delivery packaging only; byte-copy/read-only projections of completed evidence','packaged_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scientific_effect':'NONE','goal_status':'FULL_ORIGINAL_RESEARCH_GOAL_ACTIVE','mathematical_qualification':'COMPLETE_REUSED_FROM_EXISTING_PRODUCTION_RECEIPT','membership_file':'CAPTURE_GATES_MEMBERSHIP.json','scope_file':'CAPTURE_GATES_SCOPE.md','public_inventory':'CAPTURE_GATES_PUBLIC_INVENTORY.json','public_proof_names_append':'PUBLIC_PROOF_NAMES_APPEND.txt','modules':[{'module':'SourceQuarticCaptureAlgebra','source_path':str(root/'SourceQuarticCaptureAlgebra.lean'),'frozen_source_copy':'sources/SourceQuarticCaptureAlgebra.lean','source_sha256':receipt['source_sha256'],'olean_sha256':receipt['artifact_sha256'],'hash_origin':'Completed receipts; no packaging hash computation','source_integration_commit':None,'integration_cut_owned_by_root':True,'contract_freeze_commit':receipt['contract_freeze_commit'],'public_proof_targets':28,'public_definitions_separate':6,'public_declarations_total':34,'private_kernel_only_declarations':len(private),'compile':'raw/production/compile03.json','kernel':'raw/production/kernel01.json','axioms':'raw/production/audit01.json','positive_new_controls':'raw/production/transfer-controls-02.json','negative_new_controls':['raw/production/rejected-unchanged-drift-01.json','raw/production/rejected-reversed-upper-01.json'],'prior_scratch21_evidence_reused':'raw/reused-scratch21/EVIDENCE.json','qualification_receipt':'qualification_receipt.json'}],'current_norm_field_C1_dependency':{'module':'SourcePinPreservingQuartic','source_sha256':'8e23717ef98518b6d701db921d1f17958c3dee2c893745cafa7aa6172f1621d9','reference_only':True,'copied_hashed_or_rechecked':False},'baseline_by_reference':base,'raw_successor_by_reference':rawref,'packaging_actions_excluded':['Lean/build/kernel/test/stress rerun','hash recomputation','production source edits','shared metadata edits','commits','posts'],'separate_scientific_review_required':True,'combined_build_or_baseline_gate_claimed':False}
write('CAPTURE_GATES_EVIDENCE_CATALOG.json',catalog)
write('RAW_EVIDENCE_INDEX.json',{'role':'Byte-copy index of existing new-module and reused scratch21 records; no checking or hashing during packaging','copied_file_count':len(raw),'files':raw})
(out/'README.md').write_text('''# Capture-gate evidence package

This package projects completed SourceQuarticCaptureAlgebra verification only.
No checks, hashes, source edits, commits or posts were performed by packaging.

* CAPTURE_GATES_EVIDENCE_CATALOG.json: source/object binding and exact scope.
* CAPTURE_GATES_MEMBERSHIP.json: one new module, 28 proof targets, six separate definitions.
* PUBLIC_PROOF_NAMES_APPEND.txt: exactly 28 proof names for root registration.
* CAPTURE_GATES_PUBLIC_INVENTORY.json: public declarations and audit coverage.
* PRIVATE_DECLARATIONS_KERNEL_ONLY.json: eight private proofs, not public targets.
* CONTROL_AND_HELPER_HISTORY.json: genuine failures and author/helper lineage.
* RAW_EVIDENCE_INDEX.json / EXECUTION_RECORD_INDEX.json: copied files and prior commands.
* raw/reused-scratch21: earlier 21-proof scratch evidence, explicitly reused.
* raw/production: final compile03/kernel01/audit01 and new transfer controls.

Root owns code cut, metadata registration and publication. Baseline24, raw-pin
successor and23inputs are referenced only. No ODE or capture closure is claimed.
''')
(out/'CAPTURE_GATES_SCOPE.md').write_text('''# SourceQuarticCaptureAlgebra only

Source SHA ba338bba6fdd6fae70f5379c8ff58a424237baf090672a7e3303691ff2f0209a.
Object SHA abf21676803f57205d8bfeef996e277f69dd64eedba432bc896f7300b3832046.

The exact LM001 quartic has upper/lower horizontal strip gates <=-1 and >=1.
Those polynomial gates do not require REG. Central quartic drift <=-3RW<0
uses REG and does not require the transverse threshold. All adaptive geometry
and coefficient bounds are derived from the exact U-radius.

The new actual-source join projects the qualified MAX-C1 value bound into
Euclidean coordinates. Adaptive-strip points lie in ball2. On physical pins
and the original source regularity/negative-curvature cutoffs, actual upper
transverse drift is negative and lower transverse drift positive. Central
actual drift <=-11RW/4<0 needs only physical pins and regularity cutoff.
The hL,b-only eventual base/weighted AE wrappers derive current pin support
using the existing source theorem; desired gates and ODE capture are not premises.

There are28 audited public proof targets, six separately inventoried definitions,
no named instances and eight private kernel-covered proofs. Definitions returning
Prop are still definitions, not extra proof targets. Earlier21 scratch proofs
are reused and not added again to the28 production targets.

Compile03, named kernel01, audit01 and new transfer controls are completed
mathematical evidence. All public proof reports use only propext,
Classical.choice and Quot.sound. The old Q2/Q3 counterexample controls, baseline24,
raw-pin successor and23inputs are reused by reference and were not rerun.

Geometry helper /root/uniform_jet_moment_sources, new control helper
/root/palm_measure_transfer and owner /root/regression_kernel are all
OpenAI/Codex author lineage. No new provider-distinct scientific review is claimed.
No ODE existence, selected branch, complete transit/capture, measurable capture
event, geometric Palm identity, elder/counting or P0.2 closure follows here.
Root supplies the integration cut and handles registration/publication.
''')
print('packaged',len(raw),'existing files;',len(proofs),'public proofs;',len(defs),'definitions;',len(private),'private proofs')
