from pathlib import Path
from collections import Counter
import json,hashlib,shutil,re,datetime
raw=Path('/workspace/scratch/lifetime-pair-finiteness')
out=Path('/workspace/scratch/lifetime-pair-evidence-packaging');out.mkdir(exist_ok=True)
dest=out/'raw-production';dest.mkdir(exist_ok=True)
source_commit='c039243e449fcab837127ff2bc0b12edb1dc05e9'
provenance=json.loads((raw/'provenance.json').read_text())
before=json.loads((raw/'before.json').read_text())
inventory=json.loads((raw/'public-source-inventory.json').read_text())
module='SourceLifetimePairFiniteness'
public=inventory[module+'.lean'];names=[x['name'] for x in public]
assert len(names)==9 and all(x['kind']=='theorem' for x in public)
kernel=json.loads((raw/(module+'-kernel.json')).read_text())
audit=json.loads((raw/'AxiomAudit-01.json').read_text())
controls=json.loads((raw/'Controls-02.json').read_text())
# These are source identities already captured during qualification; no production
# source or object is rehashed while packaging this completed evidence.
identities={Path(x['path']).name:x for x in kernel['before']}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
compile_records=[]
for name,src,code in [
 ('Lifetime-compile-01','Lifetime.lean.frozen',0),
 ('SourceLifetimeGeometry-compile-01','SourceLifetimeGeometry.lean.frozen',0),
 (module+'-compile-01',module+'.failed01.lean',1),
 (module+'-compile-02',module+'.failed02.lean',1),
 (module+'-compile-03',module+'.lean.frozen',0),
 ('Controls-01','Controls.failed01.lean',1)]:
 if name.startswith('Lifetime-compile'):leanargs=['-o','.lake/build/lib/lean/Lifetime.olean','inputs/Lifetime.lean']
 elif name.startswith('SourceLifetimeGeometry-compile'):leanargs=['-o','.lake/build/lib/lean/SourceLifetimeGeometry.olean','inputs/SourceLifetimeGeometry.lean']
 elif name.startswith(module+'-compile'):leanargs=['-o','.lake/build/lib/lean/'+module+'.olean',module+'.lean']
 else:leanargs=[str(raw/'Controls.lean')]
 compile_records.append({'record_kind':'author_tool_history_transcription','command_argv':['/home/agent/.elan/bin/lake','env','lean','-DwarningAsError=true']+leanargs,'cwd':kernel['cwd'],'observed_exit_code':code,'raw_output':name+'.log','source_snapshot':src,'source_snapshot_sha256':sha(raw/src),'raw_log_sha256':sha(raw/(name+'.log')),'association':'Source snapshot/exit association witnessed in producer tool history; initial runs predate the structured recorder. No machine-captured before/after receipt is invented for them.'})
(raw/'initial-command-history.json').write_text(json.dumps(compile_records,indent=2)+'\n')
# Full raw records, including failed sources/logs, are preserved; these are new
# evidence custody hashes, distinct from old production identities reused above.
for p in sorted(raw.iterdir()):
 if p.is_file():shutil.copyfile(p,dest/p.name)
append={'module':module,'source_sha256':provenance['new_source']['sha256'],'source_integration_commit':source_commit,'count':9,'proof_target_count':9,'count_meaning':'9 explicit public Prop theorems; zero definitions, private proofs, or data instances in this new module. The two support inputs are separately classified, not registry append names.','proposition_declarations':9,'structural_data_instances':0,'names':names}
(out/'PUBLIC_PROOF_NAMES_APPEND.json').write_text(json.dumps(append,indent=2)+'\n')
(out/'PUBLIC_PROOF_NAMES_APPEND.txt').write_text('\n'.join(names)+'\n')
(out/'LIFETIME_PAIR_PUBLIC_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
(raw/'Lifetime-import-only.patch').read_bytes()
shutil.copyfile(raw/'Lifetime-import-only.patch',out/'LIFETIME_IMPORT_ONLY.patch')
auditlog=(raw/'AxiomAudit-01.log').read_text()
entries=re.findall(r'DECLARATION (\S+) (\S+) (\S+): AXIOMS \[(.*?)\]',auditlog,re.S)
counts={m:Counter(k for mod,k,n,a in entries if mod==m) for m in ['Lifetime','SourceLifetimeGeometry',module]}
assert len([x for x in entries if x[0]==module])==9
assert set(x[2] for x in entries if x[0]==module)==set(names)
allowed={'propext','Classical.choice','Quot.sound'}
for mod,kind,n,axs in entries:
 assert set(re.findall(r'[A-Za-z][A-Za-z.]*',axs))<=allowed,(n,axs)
rejections=[json.loads((raw/(n+'.json')).read_text()) for n in ['RejectedWithoutCriticality-01','RejectedEverySample-01']]
assert kernel['exit_code']==audit['exit_code']==controls['exit_code']==0
assert all(r['exit_code']==1 for r in rejections)
catalog={
 'schema_version':1,'scope_id':'ACTUAL_SOURCE_LIFETIME_PAIR_FINITENESS_20261026',
 'role':'New actual-source application qualification, packaged from completed execution records without rerun',
 'packaged_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scientific_effect':'NONE','source_integration_commit':source_commit,
 'contract_freeze_commit':before['commit'],'contract_sha256':provenance['brief']['sha256'],
 'scope_file':'LIFETIME_PAIR_SCOPE.md','public_inventory':'LIFETIME_PAIR_PUBLIC_INVENTORY.json',
 'public_registry_append':'PUBLIC_PROOF_NAMES_APPEND.json','public_registry_append_count':9,
 'producer':provenance['producer'],
 'module':{'module':module,'source':provenance['new_source'],'source_hash_origin':'Recorded during qualification, reused for packaging','source_snapshot':'raw-production/'+module+'.lean.frozen','olean':identities[module+'.olean'],'artifact_hash_origin':'Structured named-kernel before/after record, reused without object rehash','public_proof_targets':9,'proposition_declarations':9,'structural_data_instances':0,'public_definitions_separate':0,'exhaustive_audit_declarations':9,'compile':compile_records[4],'kernel':{'record':'raw-production/'+module+'-kernel.json','log':'raw-production/'+module+'-kernel.log','exit_code':0},'audit':{'record':'raw-production/AxiomAudit-01.json','log':'raw-production/AxiomAudit-01.log','exit_code':0}},
 'support_inputs':provenance['support_inputs'],
 'support_input_qualification':{
  'reason':'No compatible Lifetime.olean or SourceLifetimeGeometry.olean found anywhere under /workspace. Lifetime umbrella import is replaced only by sufficient narrow imports; SourceLifetimeGeometry is an exact original-body copy. Both were compiled once for this uncovered input ABI.',
  'Lifetime':{'compile':compile_records[0],'source_declarations':dict(Counter(x['kind'] for x in inventory['inputs/Lifetime.lean'])),'explicit_named_declarations':38,'source_proof_theorems':0,'all_module_declarations_audited':103,'olean':identities['Lifetime.olean']},
  'SourceLifetimeGeometry':{'compile':compile_records[1],'source_declarations':dict(Counter(x['kind'] for x in inventory['inputs/SourceLifetimeGeometry.lean'])),'explicit_named_declarations':13,'preexisting_source_proof_theorems':11,'all_module_declarations_audited':16,'olean':identities['SourceLifetimeGeometry.olean']},
  'import_only_delta':'LIFETIME_IMPORT_ONLY.patch','mathematical_definition_bodies_and_names_byte_identical':True,
  'support_proofs_registry_policy':'No duplicate proof-registration append for copied preexisting geometry; only the new nine application theorems append.'},
 'audit':{'method':'Lean.Util.CollectAxioms over every declaration whose originating module is Lifetime, SourceLifetimeGeometry, or SourceLifetimePairFiniteness; exact new public statement prints follow.','module_declaration_counts':{'Lifetime':103,'SourceLifetimeGeometry':16,module:9},'total_declarations':128,'kind_counts_by_module':{k:dict(v) for k,v in counts.items()},'allowed_axioms':['propext','Classical.choice','Quot.sound'],'exit_code':0,'proof_names_exactly_matched_to_inventory':True},
 'controls':{'positive_and_counterexamples':{'source':'raw-production/Controls.lean','record':'raw-production/Controls-02.json','log':'raw-production/Controls-02.log','exit_code':0,'claims':['FundDomain 2 L infinite when 0<L','arbitrary Pair=True actual-source pairSet on univ infinite for every actual sample','actual zeroSample field is identically zero','actual zeroSample critical FundDomain infinite: every-sample strengthening false','concrete actual candidate window a.s. finite at L=1 with no finiteness or Morse premise']},'expected_rejections':[{'record':'raw-production/'+n+'.json','log':'raw-production/'+n+'.log','observed_exit_code':r['exit_code'],'reason':reason} for n,r,reason in zip(['RejectedWithoutCriticality-01','RejectedEverySample-01'],rejections,['Endpoint-criticality witnesses cannot be constructed by reflexivity for arbitrary actual source points.','The almost-sure theorem cannot be used as a pointwise theorem for each actual sample.'])]},
 'failures':{'records':'raw-production/initial-command-history.json','retained':['SourceLifetimePairFiniteness.failed01.lean','SourceLifetimePairFiniteness-compile-01.log','SourceLifetimePairFiniteness.failed02.lean','SourceLifetimePairFiniteness-compile-02.log','Controls.failed01.lean','Controls-01.log'],'explanation':['Main compile01: spatial point argument omitted when projecting DifferentiableAt.hasFDerivAt; corrected.','Main compile02: deprecated ContinuousLinearMap.zero_apply under warningAsError; changed to zero_apply.','Controls01: interval membership simplification and deprecated set constructor alias; corrected without any production change.']},
 'reused_verification':{'policy':'/workspace/AGENTS.md owner clarification 25 October 2026: completed applicable evidence is reusable; no unchanged checks repeated for handoff. Provider review remains separate.','source_morse_source':before['frontiers/source_derivative_gaussian_20261025/SourceMorseIncidence.lean'],'source_morse_olean':before['frontiers/source_derivative_gaussian_20261025/.lake/build/lib/lean/SourceMorseIncidence.olean'],'basis':'Completed SourceMorseIncidence smoothLaw_ae_finite_sourceCriticalCube source/cube theorem qualification and mathematical evidence remain reused, including all219 standard-axiom audit. No Sard, IFT or generic compact-zero proof replay/reproof.','prior_evidence_reference':'frontiers/source_derivative_gaussian_20261025/evidence/SourceMorseIncidence','old_source_and_object_hashes':'Imported from before.json/provenance or earlier records, never recomputed in this packaging step.'},
 'toolchain':{'lean':'leanprover/lean4:v4.34.1','mathlib_rev':'d13f23b723b8a846827a245b89c10fc7d3f11612','toolchain_file_identity':before['frontiers/source_derivative_gaussian_20261025/lean-toolchain'],'lake_manifest_identity':before['frontiers/source_derivative_gaussian_20261025/lake-manifest.json']},
 'identity_preservation':{'original_C291_source_unchanged':True,'completed_SourceMorseIncidence_source_and_olean_unchanged':True,'basis':'Producer preserved and compared before.json identities before source freeze; qualification recorder snapshots the new application and support identities before/after. Packaging does not rerun those comparisons.'},
 'review_boundary':{'mathematical_execution':'Completed applicable producer evidence above; reused without further execution during packaging.','provider_distinct_alignment_review':'Not claimed; a distinct process requirement, not a reason to erase completed mathematics.','full_density_version_or_parent_theorem':'Not claimed.'},
 'ownership':'Producer changed only new application, two new support copies, and scratch evidence. Root exclusively owns lakefile, global manifests, commits, publication, and integration. PR482/485 and existing source/evidence untouched.',
 'raw_records_custody':[{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(dest.iterdir()) if p.is_file()]
}
(out/'LIFETIME_PAIR_EVIDENCE_CATALOG.json').write_text(json.dumps(catalog,indent=2)+'\n')
print(json.dumps({'output':str(out),'raw_records':len(catalog['raw_records_custody']),'public_proofs':9,'audited_declarations':128,'source_sha256':provenance['new_source']['sha256']},indent=2))
