#!/usr/bin/env python3
"""Package existing receipts plus the one uncovered negative-control receipt.
No Lean invocation and no mathematical verification replay occurs here.
"""
from pathlib import Path
from collections import Counter
import datetime, hashlib, json, re

base=Path('/workspace/scratch/actual-fold-torus-construct')
packet=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
source=packet/'SourceActualFoldTorus.lean'
ns='SourceActualFoldTorus.'
def write(name, value):
    (base/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
def ident(p):
    data=p.read_bytes()
    return {'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
receipts=[json.loads(p.read_text()) for p in sorted((base/'runs').glob('*/receipt.json'))]
bylabel={r['label']:r for r in receipts}
text=source.read_text()
public=[ns+n for n in re.findall(r'^(?:@\[simp\] )?theorem ([\w.]+)',text,re.M)]
definitions=[ns+n for n in re.findall(r'^def (\w+)',text,re.M)]
props=[ns+n for n in re.findall(r'^structure (\w+)',text,re.M)]
projections={ns+'TorusTrapData.'+n for n in [
 'death_lt_birth','maximum_height','older_height','domain_closed','maximum_inside',
 'older_outside','height_ceiling','frontier_bound','strict_trace','closed_path']}
log=(base/'runs/inventory-001/output.log').read_text()
axioms={n:[a.strip() for a in axs.split(',') if a.strip()]
        for n,axs in re.findall(r'^AXIOMS\|([^|]+)\|\[([^\]]*)\]',log,re.M)}
rows=[]
for kind,name in re.findall(r'^INVENTORY\|([^|]+)\|([^\n]+)$',log,re.M):
    if name in public:
        classification='named public theorem'; role='public_theorem_target'
    elif name.startswith('_private.'):
        classification='handwritten private theorem'; role='private_support_theorem'
    elif name in definitions:
        classification='named public definition'; role='definition'
    elif name in props:
        classification='named public Prop bundle'; role='prop_bundle'
    else:
        classification='generated '+kind; role='generated'
    subtype=('Prop-bundle field projection' if name in projections else
             'Prop-bundle eliminator/constructor support' if name.startswith(ns+'TorusTrapData.') and role=='generated' else
             'compiler theorem auxiliary' if role=='generated' else None)
    rows.append({'name':name,'kernel_kind':kind,'classification':classification,
                 'role':role,'generated_subtype':subtype,'private':name.startswith('_private.'),
                 'public_theorem_target':name in public,'transitive_axioms':axioms[name]})
rows.sort(key=lambda x:x['name'])
counts=dict(Counter(r['role'] for r in rows))
kindcounts=dict(Counter(r['kernel_kind'] for r in rows))
assert len(rows)==50 and len(public)==19 and len(definitions)==4 and len(props)==1
assert counts=={'generated':25,'prop_bundle':1,'private_support_theorem':1,'public_theorem_target':19,'definition':4}
assert all(set(r['transitive_axioms'])<= {'propext','Classical.choice','Quot.sound'} for r in rows)
write('INVENTORY.json',{'module':'SourceActualFoldTorus','total':len(rows),
  'evidence_basis':'Existing exhaustive actual-owning-module-index inventory-001; parsed only, not rerun.',
  'receipt':'runs/inventory-001/receipt.json','raw_log':'runs/inventory-001/output.log',
  'role_counts':counts,'kernel_kind_counts':kindcounts,
  'standard_axioms_only':True,'rows':rows})
write('TARGET_CLASSIFICATION.json',{'module':'SourceActualFoldTorus','total_kernel_constants':50,
  'named_public_theorems':19,'named_public_definitions':4,'named_prop_bundles':1,
  'handwritten_private_theorems':1,'generated_constants':25,
  'generated_theorems':20,'generated_definitions':3,'generated_constructors':1,'generated_recursors':1,
  'public_theorem_targets':public,'definitions':definitions,'prop_bundles':props,
  'prop_bundle_fields':sorted(projections),
  'private_support_theorems':[r['name'] for r in rows if r['private']],
  'generated_constants_names':[r['name'] for r in rows if r['role']=='generated'],
  'classification_policy':'Only explicitly named handwritten public theorem declarations are public theorem targets. The four definitions, one Prop-valued structure, its ten generated field projections, all other generated declarations, and the private support theorem are separate. No generated declaration or Prop-bundle field earns additional research-result credit.',
  'h0_interface':'TorusTrapData is the explicit geometric Prop bundle defined here. It is not the old TorusFiltration.ElderTrap type from the H0/ElderInterval lane, and no typed conversion to that structure is claimed.',
  'rows':'INVENTORY.json','evidence_receipt':'runs/inventory-001/receipt.json'})

neg=bylabel['false-control-001']; neglog=(base/'runs/false-control-001/output.log').read_text()
expected='/workspace/scratch/actual-fold-torus-construct/FalseMutation.lean:9:72: error: unsolved goals\n⊢ False\n'
assert neg['exit_code']==1 and neglog==expected
prodid=bylabel['strict-003']['after']['source']; objid=bylabel['strict-003']['after']['object']
assert prodid==neg['before']['source']==neg['after']['source']
assert objid==neg['before']['object']==neg['after']['object']
write('CONTROL_RECEIPT.json',{
 'contract':ident(base/'CONTROL_CONTRACT.md'),
 'positive_source':ident(base/'ActualTorusControls.lean'),
 'positive_object':ident(base/'build/ActualTorusControls.olean'),
 'positive_receipt':'runs/controls-002/receipt.json','positive_exit':0,
 'positive_theorems':10,'positive_definitions':0,
 'negative_scope':'NEGATIVE_CONTROL_SCOPE.md','false_source':ident(base/'FalseMutation.lean'),
 'false_receipt':'runs/false-control-001/receipt.json','false_exit':1,
 'false_target_count':1,'false_residual_goal_count':1,
 'intended_diagnostic':'exactly one unsolved goal, solely False, with no other diagnostic',
 'actual_diagnostic':neglog.strip(),'satisfied_sole_residual_False_contract':True,
 'false_log':neg['log'],'production_source':prodid,'production_object':objid,
 'proved_counterexample_reuse':['ActualTorusControls.negative_period_lifts_same',
   'ActualTorusControls.negative_period_collapsed_lifts_counterexample',
   'ActualTorusControls.negative_period_projection_not_injective'],
 'reused_unchanged_verification':['strict-003','kernel-001','inventory-001','controls-002'],
 'recovery_scope':'Only one new Lean invocation, for this previously unexecuted scratch mutation; no production change, no old or positive verification replay.'})
write('EXECUTION_RECORD_INDEX.json',{
 'runner':'run_stage.py','record_count':len(receipts),
 'records':[{'label':r['label'],'receipt':'runs/'+r['label']+'/receipt.json',
   'log':'runs/'+r['label']+'/output.log','exit_code':r['exit_code'],
   'elapsed_seconds':r['elapsed_seconds'],'started_utc':r['started_utc'],
   'ended_utc':r['ended_utc'],'command':r['command'],'cwd':r['cwd']} for r in receipts],
 'new_recovery_execution_only':['false-control-001'],
 'one_own_module_kernel':['kernel-001'],
 'all_attempts_preserved':True})

frozen=base/'FROZEN_DESCENT_SECTION.lean.txt'
assert frozen.read_bytes() in source.read_bytes()
write('AUTHOR_HELPER_LINEAGE.json',{
 'binding_precode':'5f49444d13b9c322f5214e11bc3936b2271b615f',
 'producer':{'lane':'/root/actual_fold_torus_construct','provider_family':'OpenAI',
    'model':'Exact original producer model not authenticated in this recovery; no new identity claim.',
    'ownership':'SourceActualFoldTorus.lean plus its scratch construction directory'},
 'descent_helper':{'report':'/workspace/scratch/actual-torus-descent/REPORT.md',
    'frozen_helper_source_sha256':'924a21801e7fcd9da5b09a15532ecd1ef130d3185fa2821f5fe4a3d5def8d0ef',
    'actual_model':'gpt-6-sol','actual_reasoning_effort':'high','provider_family':'OpenAI',
    'pickup_basis':'Parent recovery handoff explicitly records actual gpt-6-sol/high following a gpt-6.1-sol capacity failure.',
    'prior_requested_model':'gpt-6.1-sol','prior_pickup_result':'capacity failure; not an active or completed helper',
    'producer_frozen_section':ident(frozen),'frozen_section_occurs_literally_in_production':True,
    'verification_reuse':'helper strict-004 successful source elaboration is existing evidence; integrated new-module strict/kernel/inventory already cover its declarations, without another helper kernel/audit/control campaign.',
    'new_research_target_credit':0},
 'compact_frontier_helper':{'report':'/workspace/scratch/reused-compact-frontier/REPORT.md',
    'declaration':'CapFirstExit.frontier_image_subset',
    'origin_commit':'5f49444d13b9c322f5214e11bc3936b2271b615f',
    'origin_path':'frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean',
    'origin_git_blob_sha1':'01744e2cf571049d7d1557b9ed54646881d341cf',
    'accepted_statement_proof_sha256':'0a9af73f1cefe45a94ea1a99b18a2a336b150a5d6ca5f9dcca65f7996b03fdf0',
    'successor_source_sha256':'29d77453ef7c3cd216521a8ac84639aa30daf5a1d4061785a826b2c2d42d23db',
    'qualified_olean_sha256':'e9e4a4051fbaae8f62b27dc5d83f343d58aa4d45b5e683c61bdbe899be2e666b',
    'qualified_ilean_sha256':'da1c18e2413cda4aefd042ba62e6402692d67f918bf7f2a4eab774c59d74bd81',
    'identity_basis':'Copied exact custody from completed helper report; old Cap mathematical/hash verification not replayed.',
    'verification_reuse':'sole necessary narrow-import successor compile; no old Cap campaign repeated',
    'new_research_target_credit':0},
 'reused_actual_death':{'report':str(packet/'actual-fold-death-evidence/raw/producer/REPORT.md'),
    'source_sha256':'ee84ce7a775ae8163ec9309a0841757ce2990576adfd7186d4ad5bc8ac4de0d0',
    'qualified_olean_sha256':'3b545a10235a769892796a13c0b11194516bd11c1dc5b97aee8c0ef2275ac654',
    'qualified_controls_olean_sha256':'2a8e216590ec2a06b11a73c2bcbb286f2f46eddb83418b4dddb6134710d342d4',
    'basis':'Copied completed death source-object identities and report; old physical polynomial proof/control/kernel campaigns reused.'},
 'recovery':{'lane':'/root/torus_evidence_recovery','provider_family':'OpenAI',
   'scope':'Report/custody/classification plus sole previously unexecuted scratch negative control.',
   'fresh_model_review_or_provider_distinct_credit':False,'subagents_dispatched':0,
   'production_source_edits':False,'process_registration_or_publication':False},
 'provider_distinct_review':{'credited':False,'status':'Separate root-owned process obligation; same OpenAI family does not qualify.'},
 'standing_owner_links':[
  'https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md',
  'https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md']})
# Current own-artifact identity observations establish custody, not a rebuild.
paths=[source,base/'build/SourceActualFoldTorus.olean',base/'build/SourceActualFoldTorus.ilean',
 base/'ActualTorusControls.lean',base/'build/ActualTorusControls.olean',base/'FalseMutation.lean',
 base/'Inventory.lean',base/'CONTROL_CONTRACT.md',frozen,base/'Generic.lean',base/'Transport.lean',
 base/'ActualBody.lean.txt',base/'run_stage.py']
ids=[ident(p) for p in paths]
assert ids[0]==prodid and ids[1]==objid
write('IDENTITIES.json',{'module':'SourceActualFoldTorus','final_identities':ids,
 'source_frozen_before_kernel':True,'binding_strict_receipt':'runs/strict-003/receipt.json',
 'sole_kernel_receipt':'runs/kernel-001/receipt.json',
 'source_object_bindings_reused_in':['kernel-001','inventory-001','controls-002','false-control-001'],
 'copy_to_packet_only':['build/SourceActualFoldTorus.olean','build/SourceActualFoldTorus.ilean'],
 'never_copy_to_production_cache':['build/ActualTorusControls.olean','FalseMutation.lean','Inventory.lean','Generic.lean','Transport.lean'],
 'custody_observation_scope':'Own final artifacts only; reused helper/upstream identities are copied in AUTHOR_HELPER_LINEAGE.json, not freshly recomputed.',
 'no_source_or_production_object_mutation_in_recovery':True})
# Keep legacy death-style identity filename as an exact convenience copy.
(base/'SOURCE_OBJECT_IDENTITIES.json').write_text((base/'IDENTITIES.json').read_text())
write('STATIC_SCOPE.json',{'module':'SourceActualFoldTorus','source_sha256':prodid['sha256'],
 'direct_imports':['SourceActualFoldDeath','ReusedCompactFrontier'],
 'source_has_no_admissions_custom_axioms_native_decide_implemented_by_or_full_Mathlib_umbrella':True,
 'basis':'Read-only recovery inspection of the frozen source; inventory-001 supplies exhaustive transitive axiom evidence.',
 'h0_or_typed_ElderTrap_claim':False,'scientific_effect':'NONE'})
print(json.dumps({'written_reports':['INVENTORY.json','TARGET_CLASSIFICATION.json','CONTROL_RECEIPT.json','EXECUTION_RECORD_INDEX.json','AUTHOR_HELPER_LINEAGE.json','IDENTITIES.json','SOURCE_OBJECT_IDENTITIES.json','STATIC_SCOPE.json'], 'module_constants':len(rows),'roles':counts,'kernel_kinds':kindcounts,'sole_False':True,'production_ilean':ids[2]},indent=2))
