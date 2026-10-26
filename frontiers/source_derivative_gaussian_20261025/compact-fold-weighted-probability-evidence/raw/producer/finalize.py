#!/usr/bin/env python3
import datetime, hashlib, json, pathlib, re

B = pathlib.Path('/workspace/scratch/compact-fold-weighted-probability-construct')
P = pathlib.Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
S = P / 'SourceCompactFoldWeightedProbability.lean'
M = 'SourceCompactFoldWeightedProbability'

def ident(path):
    path = pathlib.Path(path)
    return {'path': str(path), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def load(path):
    return json.loads(pathlib.Path(path).read_text())

def write(name, value):
    (B / name).write_text(json.dumps(value, indent=2) + '\n')

receipts = {p.parent.name: load(p) for p in sorted((B / 'runs').glob('*/receipt.json'))}
strict, positive, inventory, negative, kernel = [receipts[n] for n in
    ['compile-001', 'controls-001', 'inventory-001', 'false-omitted-mark-factor-001', 'kernel-001']]
source = ident(S)
obj = ident(B / 'build' / (M + '.olean'))
assert len(receipts) == 5
assert len([n for n in receipts if n.startswith('kernel-')]) == 1
for r in receipts.values():
    assert r['before']['source'] == r['after']['source'] == source
    assert r['after']['object'] == obj
    if r is not strict:
        assert r['before']['object'] == obj
for r in [strict, positive, inventory, kernel]:
    assert r['exit_code'] == 0
assert negative['exit_code'] == 1
frozen = load(B / 'FROZEN_SOURCE.json')
assert frozen['source'] == source and frozen['object'] == obj
assert frozen['frozen_utc'] < kernel['started_utc']
assert load(B / 'CONTROL_CONTRACT.json')['frozen_utc'] < strict['started_utc']
for h in frozen['controls_frozen']:
    assert ident(h['path']) == h

log = (B / 'runs/inventory-001/output.log').read_text()
names = dict((n, k) for k, n in re.findall(r'^INVENTORY\|([^|\n]+)\|([^\n]+)$', log, re.M))
axioms = {n: [x.strip() for x in a.split(',') if x.strip()]
          for n, a in re.findall(r'^AXIOMS\|([^|\n]+)\|\[([^\]]*)\]', log, re.M)}
assert len(names) == int(re.search(r'COMPLETE_NEW_MODULE_INVENTORY\|' + M + r'\|(\d+)', log).group(1)) == 21
assert set(names) == set(axioms)
roles = {
    'sourceCompactFoldGood': 'Literal measurable varying-mark cutoff event on the original signed-period smooth carrier.',
    'sourceCompactFoldWeightedLaw': 'Literal prwMeasure of sourceGapLaw and actual physical sourceSmoothWeight, retaining r,b,k.',
    'sourceCompactCutoffA': 'Uniform obstruction coefficient 6*k1*1024*(8*max1(1/(6*k0)))^5.',
    'sourceCompactCutoffA_nonneg': 'Nonnegativity of the full obstruction coefficient for nonnegative upper mark.',
    'sourceCompactFoldGood_measurable': 'Measurability of the exact numerical cutoff event for the varying mark.',
    'varying_cutoff_failure_inclusion': 'Pointwise strict-to-closed failure inclusion preserving full scale, signs, r and 6*k1, with nonnegative Gamma.',
    'sourceCompactFoldGood_compl_subset': 'Actual source event complement lies in the old regularity/one-sided-curvature union for positive compact marks.',
    'sourceCompactFoldWeightedLaw_absolutelyContinuous': 'Derived absolute continuity relative to exactly the posterior being physically weighted.',
    'sourceCompactFoldWeightedProbability_bound': 'Closed compact C,delta before r,b,k: probability law and cubic Good-complement bound from derived actual N and c.',
    'sourceCompactFoldWeightedProbability_h0': 'The same uniform interval works for every coefficient field: weighted-AE Good implies actual ordinary H0 summand and complement, exact strict clearance and death.'
}
generated_roles = {
    M + '.sourceCompactFoldWeightedLaw.congr_simp': 'Compiler-generated congruence simplification theorem for the actual varying law.',
    M + '.sourceCompactCutoffA._proof_1': 'Compiler-generated scalar normalization proof in the full coefficient definition.',
    M + '.sourceCompactFoldGood._proof_1': 'Compiler-generated scalar normalization proof in the literal event definition.',
    M + '.sourceCompactFoldGood._proof_2': 'Compiler-generated scalar normalization proof in the literal event definition.'
}
for n in range(3, 10):
    generated_roles[M + '.sourceCompactFoldWeightedProbability_bound._simp_1_' + str(n)] = \
        'Compiler-generated simplification theorem within the closed uniform probability proof.'
rows = []
for name, kind in sorted(names.items()):
    generated = name in generated_roles
    assert generated or name.removeprefix(M + '.') in roles
    assert not name.startswith('_private.')
    assert set(axioms[name]) <= {'propext', 'Classical.choice', 'Quot.sound'}
    rows.append({'name': name, 'kind': kind, 'generated': generated, 'private': False,
        'handwritten': not generated, 'public_research_theorem': kind == 'theorem' and not generated,
        'prop_bundle': False,
        'classification': 'generated-theorem' if generated else 'named-public-' + kind,
        'research_role': generated_roles[name] if generated else roles[name.removeprefix(M + '.')],
        'transitive_axioms': axioms[name]})
assert sum(r['public_research_theorem'] for r in rows) == 7
assert sum(r['kind'] == 'definition' for r in rows) == 3
assert sum(r['generated'] for r in rows) == 11
write('INVENTORY.json', {'module': M, 'source': source, 'object': obj,
    'coverage': 'All constants selected by actual environment module index, with transitive collectAxioms on every constant. No namespace-prefix shortcut.',
    'receipt': ident(B / 'runs/inventory-001/receipt.json'), 'complete_constant_count': 21,
    'all_axioms_standard3_subset': True, 'rows': rows})
write('TARGET_CLASSIFICATION.json', {'module': M, 'total_kernel_constants': 21,
    'named_public_theorems': 7, 'named_public_definitions': 3, 'named_prop_bundles': 0,
    'handwritten_private_theorems': 0, 'generated_constants': 11, 'generated_theorems': 11,
    'generated_definitions': 0,
    'public_theorem_targets': [r['name'] for r in rows if r['public_research_theorem']],
    'definitions': [r['name'] for r in rows if r['kind'] == 'definition'],
    'prop_bundles': [], 'private_support_theorems': [],
    'generated_constants_names': [r['name'] for r in rows if r['generated']],
    'classification_policy': 'All actual module-index constants; generated scalar-proof/congruence/simp constants are not separate research theorem targets.',
    'rows': 'INVENTORY.json'})

negative_log = (B / 'runs/false-omitted-mark-factor-001/output.log').read_text()
assert negative_log.count('error:') == 1 and negative_log.count('⊢ False') == 1
assert 'unsolved goals' in negative_log
assert not any(t in negative_log for t in ['Unknown identifier', 'unexpected token', 'declaration uses', 'warning:'])
control_names = re.findall(r'^theorem (\S+)', (B / 'Controls.lean').read_text(), re.M)
assert len(control_names) == 15
write('CONTROL_RECEIPT.json', {'contract': ident(B / 'CONTROL_CONTRACT.md'),
    'positive_source': ident(B / 'Controls.lean'), 'positive_object': ident(B / 'build/Controls.olean'),
    'positive_receipt': ident(B / 'runs/controls-001/receipt.json'), 'positive_exit': 0,
    'positive_theorems': 15, 'positive_theorem_names': control_names,
    'positive_scope': ['Literal same actual varying law and exact Good event',
        'Original negative signed period L=-1; B=3,k0=1/12,k1=2; full scale16 and A=12884901888',
        'Actual sample T=16*Gamma and Kappa=-q/(12*r) for mark2; event measurability and complement inclusion',
        'One C,delta for actual marks(b=-3,k=1) and(b=3,k=2)',
        'Uniform probability/H0 endpoint with C,delta before marks and every coefficient field',
        'Literal same-law absolute continuity and weighted AE transfer',
        'Positive-radius Bochner normalization power identity r^5/r^2=r^3',
        'Closed obstruction equality witness; no reverse inclusion is claimed'],
    'false_mutation_source': ident(B / 'FalseOmittedMarkFactor.lean'),
    'false_mutation_receipt': ident(B / 'runs/false-omitted-mark-factor-001/receipt.json'),
    'false_mutation_log': ident(B / 'runs/false-omitted-mark-factor-001/output.log'),
    'false_mutation_exit': 1, 'distinct_mutation_count': 1, 'residual_false_count': 1,
    'unrelated_diagnostics': 0,
    'false_mutation_mechanism': 'Omit 6*k1 from the curvature obstruction. At r=1e-9,Gamma=1,q=-5,k=2,lambda=16, the first Good cutoff holds and the second fails; the full coefficient detects it while the reduced coefficient misses it.',
    'counterexample_scope': 'Finite exact scalar arithmetic only; no claim that a posterior sample realizes the specified Gamma and q.',
    'unexpected_development_failures': [], 'all_expected_rejection_sources_and_logs_preserved': True,
    'old_control_campaign_replayed': False, 'production_source_unchanged_for_controls': True,
    'helper_control_objects_production_eligible': False})

frozen.update({'no_own_kernel_yet': False, 'exactly_one_named_own_module_kernel': True,
    'kernel_receipt': ident(B / 'runs/kernel-001/receipt.json'),
    'source_unchanged_since_strict_compile': True, 'all_frozen_before_kernel_start': True})
write('FROZEN_SOURCE.json', frozen)
write('SOURCE_OBJECT_IDENTITIES.json', {'source': source, 'olean': obj,
    'ilean': ident(B / 'build' / (M + '.ilean')),
    'strict_receipt': ident(B / 'runs/compile-001/receipt.json'),
    'kernel_receipt': ident(B / 'runs/kernel-001/receipt.json'),
    'new_numerator_source': frozen['dependency_numerator_source'],
    'new_numerator_object': frozen['dependency_numerator_object'],
    'new_normalizer_source': frozen['dependency_normalizer_source'],
    'new_normalizer_object': frozen['dependency_normalizer_object'],
    'qualified_existing_packet': '43 modules /1044 targets /32 inputs at6efd145; completed applicable old verification reused, no replay.',
    'precode_commit': 'b8114e28d0e440e078a831c8df7fe69411b3a6e5',
    'production_eligible': [M + '.olean'],
    'ineligible': 'Controls.olean and all control/mutation/helper objects. Root alone owns production cache copy.'})
text = S.read_text()
banned = {pattern: bool(re.search(pattern, text, re.M)) for pattern in
    [r'\bsorry\b', r'^\s*axiom\b', r'\bnative_decide\b', r'\bimplemented_by\b', r'^import Mathlib\s*$']}
assert not any(banned.values())
write('STATIC_SCOPE.json', {'source': source, 'imports': re.findall(r'^import (\S+)', text, re.M),
    'forbidden_token_matches': banned,
    'closed_endpoints': ['sourceCompactFoldWeightedProbability_bound', 'sourceCompactFoldWeightedProbability_h0'],
    'final_premises': ['L!=0', 'B>=0', '0<k0', 'k0<=k1'],
    'literal_same_actual_carrier_measure_weight_and_event': True,
    'constants': 'C=N/c; probability delta=min(deltaN,deltac); H0 delta additionally min(deltaH), all before r,b,k,K.',
    'full_obstruction_constants': 'lambda=8*max1(1/(6*k0)); eps=1/(100*lambda^5); A=6*k1*1024*lambda^5',
    'no_final_model_certificate_premises': True,
    'scope': 'Compact fixed-axis normalized cutoff/H0 success probability. No canonical partner/selector, conditional genericity, frame/translation uniformity, actual Campbell/count-density or ParentA/B closure.'})
write('AUTHOR_HELPER_LINEAGE.json', {'author': {'provider': 'OpenAI', 'family': 'GPT-6/Codex',
    'agent': '/root/compact_fold_weighted_probability_construct', 'role': 'sole new-module author and execution'},
    'root': '/root', 'precode_commit': 'b8114e28d0e440e078a831c8df7fe69411b3a6e5',
    'spec_read_before_code': 'SOURCE_COMPACT_FOLD_WEIGHTED_PROBABILITY.md + SOURCE_COMPACT_FOLD_WEIGHTED_PROBABILITY_PLAN.md',
    'worker_agents_spawned_by_author': 0, 'helpers': [],
    'completed_evidence_reused': True, 'old_math_kernel_control_review_replays': 0,
    'same_provider_review_credit': 'Technical only; zero provider-distinct or organizational independence credit.',
    'scientific_effect': 'NONE',
    'canonical_authority': ['https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md',
        'https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md'],
    'verification_reuse_instruction': '/workspace/AGENTS.md owner clarification25October2026: completed applicable unchanged verification is reusable; pending process requirements do not erase mathematics; agent/session/handoff alone does not justify replay.',
    'root_owned_process': 'Registration/cache/publication/current CI and separate source/spec review; no production metadata or old source/config/cache/manifests touched by this author.'})
write('EXECUTION_ENVIRONMENT.json', {'reused_environment_evidence': 'qualified43/1044/32 at6efd145 and existing EXECUTION_ENVIRONMENT evidence; no old environment verification replay.',
    'lean_version': 'Lean4.34.1 x86_64 Linux commit5045d0056413266e57c625dcd7c365b10e377c52',
    'mathlib_head': 'd13f23b723b8a846827a245b89c10fc7d3f11612',
    'commands_and_explicit_lean_paths': 'runs/*/receipt.json',
    'cache_policy': 'New own/control objects only under assigned scratch; no production cache writes; root owns qualification/copy.'})
runs = []
for label, r in receipts.items():
    runs.append({'label': label, 'receipt': ident(B / 'runs' / label / 'receipt.json'),
        'exit_code': r['exit_code'], 'started_utc': r['started_utc'], 'ended_utc': r['ended_utc'],
        'elapsed_seconds': r['elapsed_seconds'], 'command': r['command'], 'log': r['log'],
        'credit': 'expected sole rejection' if label == 'false-omitted-mark-factor-001' else 'successful'})
write('EXECUTION_RECORD_INDEX.json', {'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'all_verification_invocations': runs, 'exactly_one_own_module_kernel': True,
    'old_math_replay_count': 0, 'all_failures_retained': True, 'unexpected_development_failure_count': 0,
    'native_checkpoint_utc': '2026-10-26T11:00:00Z', 'terminal_utc': '2026-10-26T12:00:00Z', 'timers_reset': False})
write('RAW_LEDGER.json', {'own_all_receipts': receipts, 'all_failures_preserved': True,
    'frozen_source': frozen, 'old_verification_replay_count': 0, 'worker_count': 0,
    'sole_expected_failure': 'false-omitted-mark-factor-001',
    'precode_control_freeze': load(B / 'CONTROL_CONTRACT.json')})
write('HANDOFF.json', {'module': M, 'source': source, 'object': obj,
    'status': 'PASS own scoped execution; root source/spec review and provider-distinct process tracked separately.',
    'strict': 'runs/compile-001/receipt.json', 'kernel': 'runs/kernel-001/receipt.json',
    'inventory': 'runs/inventory-001/receipt.json', 'controls': 'runs/controls-001/receipt.json',
    'sole_false': 'runs/false-omitted-mark-factor-001/receipt.json',
    'kernel_constants': 21, 'named_public_theorems': 7, 'definitions': 3, 'generated_theorems': 11,
    'all_axioms_standard3_subset': True, 'scientific_effect': 'NONE', 'provider_distinct_credit': 0,
    'remaining_root_work': 'Source/spec review; registration and qualified own-module cache; source cut/current CI/publication; separate provider-distinct process.',
    'reuse': 'Carry completed applicable verification forward; no unchanged old-math or new-module replay from handoff alone.'})
print(json.dumps({'module': M, 'source': source, 'object': obj, 'kernel_constants': 21,
    'named_public_theorems': 7, 'definitions': 3, 'generated_theorems': 11,
    'strict': 'PASS', 'exactly_one_own_kernel': 'PASS', 'inventory_standard3': 'PASS',
    'positive_controls': 'PASS15', 'sole_false_rejection': 'PASS1'}, indent=2))
