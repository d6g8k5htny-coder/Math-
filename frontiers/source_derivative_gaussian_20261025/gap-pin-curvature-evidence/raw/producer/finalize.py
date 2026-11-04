#!/usr/bin/env python3
import datetime, hashlib, json, pathlib, re
B=pathlib.Path('/workspace/scratch/gap-pin-curvature-construct')
P=pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
S=P/'SourceGapPinCurvature.lean'
def ident(p):
    p=pathlib.Path(p)
    return {'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(name,data): (B/name).write_text(json.dumps(data,indent=2)+'\n')
def load(p):return json.loads(pathlib.Path(p).read_text())
receipts={p.parent.name:load(p) for p in sorted((B/'runs').glob('*/receipt.json'))}
strict=receipts['compile-002']; kernel=receipts['kernel-001']; inv=receipts['inventory-001']; pos=receipts['controls-002']; neg=receipts['false-target-001']
for r in [strict,kernel,inv,pos,neg]:
    assert r['before']['source']==r['after']['source']==strict['after']['source']
for r in [strict,kernel,inv,pos]:assert r['exit_code']==0
assert len([k for k in receipts if k.startswith('kernel-')])==1
assert ident(S)==strict['after']['source']
frozen=load(B/'FROZEN_SOURCE.json'); assert frozen['frozen_utc'] < kernel['started_utc']
assert frozen['source']==ident(S)
contract=load(B/'CONTROL_CONTRACT.json');assert contract['frozen_utc'] < receipts['compile-001']['started_utc']
log=(B/'runs/inventory-001/output.log').read_text(); names={}; axs={}
for kind,name in re.findall(r'^INVENTORY\|([^|\n]+)\|([^\n]+)$',log,re.M):
    assert name not in names;names[name]=kind
for name,aa in re.findall(r'^AXIOMS\|([^|\n]+)\|\[([^\n]*)\]$',log,re.M):axs[name]=[x.strip() for x in aa.split(',') if x.strip()]
assert len(names)==int(re.search(r'COMPLETE_NEW_MODULE_INVENTORY\|SourceGapPinCurvature\|(\d+)',log).group(1))==10
assert set(names)==set(axs)
roles={
'source_normalized_first_four_third_bound':'Direct Peano absolute endpoint bound by actual third-majorant/2; no sixth-pin premise or radius cap.',
'source_normalized_first_four_bound':'Endpoint absolute bound by original Gamma radius; nonzero radius only.',
'source_normalized_transverse_errors':'Both transverse q-errors; no pin premise.',
'source_normalized_determinant_bounds':'Two literal normalized endpoint determinant factors; zero rows 3/4 only.',
'sourceSmoothWeight_curvature_bound':'Exact physical q-sensitive strict-type weight bound; zero rows 3/4 only.',
'source_positive_weight_curvature_upper':'Strict type implies q<r*third-majorant; no pin premise.',
'source_bad_curvature_slab':'Visible real A one-sided obstruction gives symmetric slab; no pin premise.',
'sourceSmoothWeight_radius_bound':'Coarse 10*r^2*Gamma^4 physical weight bound on r<=1.',
'sourceSmoothKernel_curvature_bounds_ae':'Every target with zero rows 3/4: derive actual posterior support and physical estimates.',
'sourceGapLaw_curvature_bounds':'Closed actual-law all-real-b,k endpoint; hL-only delta before r,b,k; derive covariance invertibility and pins.'}
rows=[]
for name,kind in sorted(names.items()):
    short=name.split('.')[-1];generated=short not in roles;private=name.startswith('_private.')
    assert not generated and not private and kind=='theorem'
    assert set(axs[name])<= {'propext','Classical.choice','Quot.sound'}
    rows.append({'name':name,'kind':kind,'generated':generated,'private':private,'handwritten':True,'public_research_theorem':True,'prop_bundle':False,'classification':'named-public-theorem','research_role':roles[short],'transitive_axioms':axs[name]})
write('INVENTORY.json',{'module':'SourceGapPinCurvature','source':ident(S),'object':ident(B/'build/SourceGapPinCurvature.olean'),'coverage':'Every constant selected by actual environment module index SourceGapPinCurvature, not by name prefix. Transitive collectAxioms of every owned constant.','receipt':ident(B/'runs/inventory-001/receipt.json'),'complete_constant_count':len(rows),'all_standard3':True,'rows':rows})
write('TARGET_CLASSIFICATION.json',{'module':'SourceGapPinCurvature','total_kernel_constants':10,'named_public_theorems':10,'named_public_definitions':0,'named_prop_bundles':0,'handwritten_private_theorems':0,'generated_constants':0,'generated_theorems':0,'generated_definitions':0,'public_theorem_targets':[r['name'] for r in rows],'definitions':[],'prop_bundles':[],'private_support_theorems':[],'generated_constants_names':[],'classification_policy':'Every actual module-index constant was classified. All ten constants are named public theorem targets; no generated/private/definition/Prop-bundle declarations were found.','rows':'INVENTORY.json'})
negative=(B/'runs/false-target-001/output.log').read_text()
assert neg['exit_code']==1 and negative.count('error:')==1 and negative.count('⊢ False')==1 and 'unsolved goals' in negative
assert all(t not in negative for t in ['Unknown identifier','unexpected token','declaration uses','warning:'])
write('CONTROL_RECEIPT.json',{'contract':ident(B/'CONTROL_CONTRACT.md'),'positive_receipt':ident(B/'runs/controls-002/receipt.json'),'positive_source':ident(B/'Controls.lean'),'positive_object':ident(B/'build/Controls.olean'),'positive_exit':0,'original_negative_period':-1,'nondefault_height':3,'nondefault_gap':1,'negative_gap':-2,'literal_sixth_target_at_k1':12,'sixth_target_not_two':True,'generic_all_target_control':'GapPinCurvatureControls.generic_all_target','generic_closed_law_control':'GapPinCurvatureControls.generic_closed_gap','closed_negative_period_control':'GapPinCurvatureControls.closed_nondefault_negative_period','positive_scope':['all-target and actual sourceGapLaw generic signatures','original L=-1,b=3,k=1 and k=-2 share hL-only interval','actual sixth pin 12 and -24; nondefault target unequal 2','pin-free transverse/strict/slab exports','first-four Peano bound valid even at radius -3','literal physical strict-type weight 1/64 at r=1/4,q=-1/2 and zero weight at q=0','q-sensitive ceiling increases from 1/32 to 1/16','nonzero negative q=-3/2 saturates slab at A=3,r=1/2,Gamma=1'],'false_mutation_source':ident(B/'FalseTargetNormalization.lean'),'false_mutation_receipt':ident(B/'runs/false-target-001/receipt.json'),'false_mutation_log':ident(B/'runs/false-target-001/output.log'),'false_mutation_exit':1,'distinct_mutation_count':1,'residual_false_count':1,'unrelated_diagnostics':0,'false_mutation_mechanism':'Counterexample-backed deliberate claim sourceGapPins r 3 1 5=2 reduces by norm_num [sourceGapPins] to exactly one residual False, with proved nondefault_slot5 counterexample in context.','historical_failures':['compile-001 finite vector coercion simplification and unnecessary tactic-sequence linter','controls-001 missing ResearchFormalCoreR1 helper namespace open'],'old_control_campaign_replayed':False,'production_source_unchanged_for_all_controls':True,'helper_objects_production_eligible':False})
write('SOURCE_OBJECT_IDENTITIES.json',{'source':ident(S),'olean':ident(B/'build/SourceGapPinCurvature.olean'),'ilean':ident(B/'build/SourceGapPinCurvature.ilean') if (B/'build/SourceGapPinCurvature.ilean').exists() else None,'strict_receipt':ident(B/'runs/compile-002/receipt.json'),'kernel_receipt':ident(B/'runs/kernel-001/receipt.json'),'direct_import_source':ident(P/'SourceCompactTargetMoments.lean'),'direct_import_object':ident(P/'.lake/build/lib/lean/SourceCompactTargetMoments.olean'),'reused_peano_curvature_source':ident(P/'SourcePinCurvatureBounds.lean'),'reused_peano_curvature_object':ident(P/'.lake/build/lib/lean/SourcePinCurvatureBounds.olean'),'qualified_existing_packet':'38 modules / 989 targets / 32 inputs at published source cut 19f7baf; completed applicable verification reused, no old replay. Root owns qualification metadata.','precode_commit':'c47964f89d819dde79019b0ac544dc9b4bfd710c','production_eligible':['SourceGapPinCurvature.olean'],'ineligible':'Controls.olean and all other helper/control/mutation objects; root alone owns production cache copy.'})
frozen.update({'no_own_kernel_yet':False,'exactly_one_named_own_module_kernel':True,'kernel_receipt':ident(B/'runs/kernel-001/receipt.json'),'source_unchanged_since_strict_compile':True,'frozen_before_kernel_start':True})
write('FROZEN_SOURCE.json',frozen)
text=S.read_text();banned={p:bool(re.search(p,text,re.M)) for p in [r'\bsorry\b',r'^\s*axiom\b',r'\bnative_decide\b',r'\bimplemented_by\b',r'^import Mathlib\s*$']};assert not any(banned.values())
write('STATIC_SCOPE.json',{'source':ident(S),'imports':re.findall(r'^import (\S+)',text,re.M),'forbidden_token_matches':banned,'no_pin5_premise':True,'actual_sourceSmoothWeight_retained':True,'literal_sixth_target':'12*k','closed_endpoint_only_input':'hL : L != 0','delta_quantifiers':'exists delta>0,delta<=1 before forall r>0,r<delta,forall b k:Real','scope':'Target-independent physical curvature/slab bounds; no probability, normalizer, residual-moment, frame or Parent closure.'})
write('AUTHOR_HELPER_LINEAGE.json',{'author':{'provider':'OpenAI','family':'GPT-6','agent':'/root/gap_pin_curvature_construct','role':'new-module implementer and author execution'},'root':'/root','precode_commit':'c47964f89d819dde79019b0ac544dc9b4bfd710c','preflight':'/workspace/scratch/actual-fold-cutoff-probability-preflight/REPORT.md item 1','completed_evidence_reused':True,'old_math_kernel_control_review_replays':0,'worker_agents_spawned':0,'same_provider_review_credit':'Technical only; zero provider-distinct/organizational independence credit','scientific_effect':'NONE','canonical_authority':['https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md','https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md'],'verification_reuse_instruction':'/workspace/AGENTS.md owner clarification 25 October 2026: completed applicable unchanged verification is reusable; process requirements tracked separately.'})
write('EXECUTION_ENVIRONMENT.json',{'reused_environment_evidence':'/workspace/scratch/actual-fold-h0-construct/EXECUTION_ENVIRONMENT.json','lean_toolchain':ident(P/'lean-toolchain'),'lean_version':'Lean 4.34.1 x86_64 Linux, commit 5045d0056413266e57c625dcd7c365b10e377c52','mathlib_head':'d13f23b723b8a846827a245b89c10fc7d3f11612','commands_and_explicit_lean_paths':'runs/*/receipt.json','qualification_dependencies':'Existing qualified packet cache reused; only new module and helper objects written under producer scratch build.'})
runs=[]
for label,d in receipts.items():
    runs.append({'label':label,'receipt':ident(B/'runs'/label/'receipt.json'),'exit_code':d['exit_code'],'started_utc':d['started_utc'],'ended_utc':d['ended_utc'],'elapsed_seconds':d['elapsed_seconds'],'command':d['command'],'log':d['log'],'credit':'expected rejection' if label=='false-target-001' else 'successful' if d['exit_code']==0 else 'retained development failure'})
write('EXECUTION_RECORD_INDEX.json',{'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'all_verification_invocations':runs,'exactly_one_own_module_kernel':True,'old_math_replay_count':0,'all_failures_retained':True,'native_checkpoint_utc':'2026-10-26T10:15:00Z','terminal_utc':'2026-10-26T11:15:00Z','timers_reset':False})
print(json.dumps({'constants':len(rows),'all_standard3':True,'positive_controls':'PASS','negative_residual_false_count':1,'source':ident(S),'object':ident(B/'build/SourceGapPinCurvature.olean')},indent=2))
