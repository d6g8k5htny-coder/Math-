"""Read actual C291 source-mutation evidence; never rerun Lean or infer a proof."""
from pathlib import Path
import hashlib
import json
import re


# Independent reviewed identities, not values supplied by the acceptance index.
GENERATION = '0b581f8569781d82'
MANIFEST_SHA = 'f511a499d1804a3033728cc576e9c6bba0f8954039f811b9ec1fe71cc73df279'
INVENTORY_SHA = '82f685a5d71671d9e682ca3df87485e97e8321e16f89c094965a49c2f8a100fe'
PROBE_MANIFEST_SHA = '7dd3aa5e64d78e63ebd8f23153c81feb3a20b6c47c698c8c7a4ba9d33fb6b6bc'
PROBE_SOURCE_SHA = 'db9ae52ad5c324d5949af011ca32ff1691ecaaeddf3bfe36fccfba485f82ef62'
BASELINE_RECEIPT = 'negative-runs/20261017T231301Z-NegativeFixtureBaseline-482f2ff2/RECEIPT.json'
BASELINE_RECEIPT_SHA = '1d278de59b1c3d56da4d40f12d12dc77f43c96108a684ec6446644027d1c7272'
PROBE_RECEIPT = 'negative-runs/20261017T232142Z-NegativeFixtureBindingProbe-b26210bd/RECEIPT.json'
PROBE_RECEIPT_SHA = '6eb94d244bfaa3005821d020f4b591fad865b393d4199a7f679fd6fe6282f437'
LEAN_SHA = '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
BASELINE_RUNNER_SHA = '9b666ae4a8834299c154a7642542050be0ee6fcf8d69f76c6161f9b39a0a7b19'
PROBE_RUNNER_SHA = 'e1931aeb581065c2c6e2fbd25bf6e123a43c1bfd6f9ddf0a3df256ee3d735409'
PROBE_IMPORTED_RUNNER_SHA = '407e16658429c752074acb30c6ced60b26796e89173740334e13863950cd45e1'
LATER_RUNNER_SHA = '57d43dda2d54d4a4acb5c24cec966a3c469cdedfa05c489f13a2e8c327a802df'
SUFFIXES = ['covQuadForm_nonneg', 'actualField_linearCombination_map',
            'actualField_raw_second_moment']
# name, byte offset, old, new, original line, namespace range, intended error range.
CASE_SPECS = [
    ('ZeroField', 2901, '  F := actualField d L\n', '  F := fun _ _ => 0\n',
     69, [17, 102], [66, 80]),
    ('ShiftedField', 2901, '  F := actualField d L\n',
     '  F := fun ω x => actualField d L ω x + 1\n', 69, [102, 187], [151, 165]),
    ('ZeroMeasure', 2828, '  P := smoothLaw d L\n', '  P := 0\n',
     67, [187, 272], [236, 250]),
    ('HiddenPositiveDimension', 2675,
     'def actualGaussianFieldInterface (d : ℕ) (L : ℝ) (hL : 0 < L) :\n',
     'def actualGaussianFieldInterface (d : ℕ) (L : ℝ) (hL : 0 < L) (hd : 0 < d) :\n',
     63, [272, 357], [352, 354]),
    ('DoubledRawCovariance', 965, '      periodicCovariance d L (x - y) := by\n',
     '      2 * periodicCovariance d L (x - y) := by\n', 26, [357, 442], [366, 373]),
    ('WrongCovarianceArgument', 965, '      periodicCovariance d L (x - y) := by\n',
     '      periodicCovariance d L (x + y) := by\n', 26, [442, 527], [451, 458]),
    ('NegativeQuadraticForm', 1897, '    0 ≤ covQuadForm d L x a := by\n',
     '    0 ≤ -covQuadForm d L x a := by\n', 47, [527, 612], [558, 564]),
]
EXTRA_DEVELOPMENT_SOURCES = {
    'ConstructorEndpointRed.lean': '9686926a3bb8fd15384e39900d9241958bdf170ff6c409b0dace2f7e55f63808',
    'SourceSmoothAxiomAudit.lean': '4dfa901029fab71d127c9f4c8cf30c937607f4444e6af64f429890d9d141d591',
    'ThetaProductProbe.lean': 'f694ef7ac460e798d6d39dc1e336e63e7d3e4e14d3c9ef63234d24e32fcf0bff',
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def verify(root):
    root = Path(root).resolve()
    checks = []

    def ck(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        if not condition:
            raise ValueError(name)

    index = read(root / 'NEGATIVE_FINAL_INDEX.json')
    ck('negative_index_terminal', index['status'] == 'PASS')
    ck('exact_generation_directory', index['generation'] == 'negative-project/generations/' + GENERATION)
    generation = root / index['generation']
    mp = generation / 'MANIFEST.json'
    manifest = read(mp)
    ck('negative_manifest_binding', sha(mp.read_bytes()) == index['manifest_sha256'] == MANIFEST_SHA)
    ck('exact_negative_generation', manifest['generation'] == GENERATION and
       manifest['schema'] == 'C291-negative-fixtures-v3-seven-controls-once-census')
    inventory_path = root / 'FINAL_SOURCE_INVENTORY.json'
    ck('reviewed_final_inventory', sha(inventory_path.read_bytes()) == INVENTORY_SHA)
    inventory = read(inventory_path)
    expected_sources = {s['name']: s['sha256'] for s in inventory['sources']}
    ck('exact_nineteen_frozen_sources', len(expected_sources) == len(inventory['sources']) == 19)
    for name, digest in expected_sources.items():
        ck('frozen_source:' + name, sha((root / 'final-project' / name).read_bytes()) == digest)
    # The historical development runner recorded 22 sources, not just the 19
    # frozen formal modules. Preserve and bind those three additional entries.
    expected_development_sources = dict(expected_sources, **EXTRA_DEVELOPMENT_SOURCES)
    for name, digest in EXTRA_DEVELOPMENT_SOURCES.items():
        snapshot = root / 'evidence/development-source-snapshots' / (digest + '.lean.txt')
        ck('development_source_snapshot:' + name, sha(snapshot.read_bytes()) == digest)
    base = (root / 'final-project/SourceLifetimeField.lean').read_bytes()
    audit = (root / 'final-project/SourceLifetimeAxiomAudit.lean').read_bytes()
    ck('negative_baseline_exact_final_source', sha(base) == manifest['baseline_source_sha256'] and
       sha(audit) == manifest['baseline_audit_sha256'] and
       (generation / 'BASE_SOURCE.lean').read_bytes() == base and
       (generation / 'BASE_AUDIT.lean').read_bytes() == audit)
    cases = manifest['constructor_cases']
    ck('seven_exact_semantic_cases', [c['name'] for c in cases] == [s[0] for s in CASE_SPECS])
    for case, spec in zip(cases, CASE_SPECS):
        name, offset, old, new, line, namespace_range, error_range = spec
        ck('reviewed_edit_and_ranges:' + name,
           case['namespace'] == 'C291Negative.' + name and
           case['raw_clone_path'] == 'raw-clones/' + name + '.lean' and
           case['single_edit'] == {'byte_offset': offset, 'old': old, 'new': new, 'original_line': line} and
           case['combined_namespace_range'] == namespace_range and
           case['required_error_line_range'] == error_range)
    ck('exact_helper_suffixes', manifest['positive_binding_required_local_suffixes'] == SUFFIXES)

    def edit(data, change):
        offset = change['byte_offset']
        old, new = change['old'].encode(), change['new'].encode()
        ck('single_edit_original:' + str(offset) + ':' + sha(new)[:8], data[offset:offset + len(old)] == old)
        ck('single_edit_original_line:' + str(offset), data[:offset].count(b'\n') + 1 == change['original_line'])
        return data[:offset] + new + data[offset + len(old):]

    def extract(text):
        prefix, body = text.split('namespace I4LifetimeField\n', 1)
        body, end = body.rsplit('end I4LifetimeField\n', 1)
        ck('source_namespace_tail', end == '')
        return prefix, body

    prefix, body = extract(base.decode())
    positive = prefix + '\nopen I4LifetimeField\n\n'
    negative = positive
    ck('no_import_of_production_constructor', 'import SourceLifetimeField\n' not in prefix)
    for case in cases:
        changed = edit(base, case['single_edit'])
        raw = (generation / case['raw_clone_path']).read_bytes()
        ck('exact_single_source_mutation:' + case['name'], changed == raw and
           sha(raw) == case['raw_clone_sha256'])
        _, mutated_body = extract(changed.decode())
        ns = case['namespace']
        tail = ('\n/-- Consumer of the unrestricted endpoint at zero spatial dimension. -/\n'
                'example : GaussianFieldInterface 0 1 :=\n'
                '  actualGaussianFieldInterface 0 1 (by norm_num)\n\nend ' + ns + '\n\n')
        positive += 'namespace ' + ns + '\n' + body + tail
        negative += 'namespace ' + ns + '\n' + mutated_body + tail
    for case in cases:
        positive += 'set_option pp.fullNames true in\n#print ' + case['namespace'] + '.actualGaussianFieldInterface\n'
    ck('exact_unmodified_positive_clone_wrappers', (generation / 'NegativeFixtureBaseline.lean').read_text() == positive)
    ck('exact_mutated_clone_wrappers', (generation / 'NegativeConstructorMutants.lean').read_text() == negative)
    axiom_raw = edit(base, manifest['unused_axiom']['single_edit'])
    ck('single_unused_private_axiom_edit', (generation / 'raw-clones/UnusedCustomAxiom.lean').read_bytes() == axiom_raw and
       sha(axiom_raw) == manifest['unused_axiom']['raw_clone_sha256'] and
       axiom_raw.count(b'c291UnusedCustomAxiom') == 1)
    _, axiom_body = extract(axiom_raw.decode())
    expected_axiom = prefix + '\nopen I4LifetimeField\n\nnamespace C291Negative.UnusedAxiom\n' + axiom_body + 'end C291Negative.UnusedAxiom\n'
    ck('exact_private_axiom_wrapper', (generation / 'NegativeUnusedAxiom.lean').read_text() == expected_axiom)
    audit_copy = edit(b'import NegativeUnusedAxiom\n' + audit, manifest['unused_axiom']['audit_harness_change'])
    ck('exact_whole_module_audit_extension', (generation / 'NegativeUnusedAxiomAudit.lean').read_bytes() == audit_copy)
    for module, identity in manifest['modules'].items():
        b = (generation / (module + '.lean')).read_bytes()
        ck('fixture_module_identity:' + module, sha(b) == identity['sha256'] and len(b) == identity['bytes'])

    probe_dir = root / ('negative-project/instrumentation/proof-binding-' + GENERATION)
    probe_manifest_path = probe_dir / 'MANIFEST.json'
    probe_manifest = read(probe_manifest_path)
    references = [c['namespace'] + '.' + suffix for c in cases for suffix in SUFFIXES]
    expected_probe = ('import NegativeFixtureBaseline\n\nset_option pp.fullNames true\n'
                      'set_option pp.proofs true\n\n' + ''.join(
                          '#print ' + c['namespace'] + '.actualGaussianFieldInterface\n' for c in cases))
    probe_source = (probe_dir / 'NegativeFixtureBindingProbe.lean').read_bytes()
    ck('exact_probe_source', probe_source == expected_probe.encode() and sha(probe_source) == PROBE_SOURCE_SHA)
    ck('exact_probe_manifest', sha(probe_manifest_path.read_bytes()) == PROBE_MANIFEST_SHA and
       probe_manifest['generation'] == GENERATION and probe_manifest['source_sha256'] == PROBE_SOURCE_SHA and
       probe_manifest['required_references'] == references and
       probe_manifest['original_compile_receipt'] == BASELINE_RECEIPT)
    ck('exact_original_positive_receipts', index['positive_baseline_receipt'] == BASELINE_RECEIPT and
       sha((root / BASELINE_RECEIPT).read_bytes()) == BASELINE_RECEIPT_SHA and
       index['binding_probe_receipt'] == PROBE_RECEIPT and
       sha((root / PROBE_RECEIPT).read_bytes()) == PROBE_RECEIPT_SHA)

    names = ['positive_baseline_receipt', 'binding_probe_receipt', 'mutants_receipt',
             'axiom_carrier_receipt', 'axiom_rejection_receipt']
    ck('five_unique_actual_executions', len(set(index[n] for n in names)) == 5 and
       set(index['receipts']) == {index[n] for n in names})
    modules = ['NegativeFixtureBaseline', 'NegativeFixtureBindingProbe', 'NegativeConstructorMutants',
               'NegativeUnusedAxiom', 'NegativeUnusedAxiomAudit']
    original = read(root / BASELINE_RECEIPT)
    # The independently pinned original receipt binds the historical absolute
    # execution location. The evidence root may instead be an extracted packet.
    executed_generation = Path(original['command'][-1]).parent
    executed_root = executed_generation.parents[2]
    executed_probe = executed_root / ('negative-project/instrumentation/proof-binding-' + GENERATION)
    ck('baseline_execution_directory', executed_generation == executed_root / index['generation'])
    original_objects = original['production_objects_before']
    ck('exact_development_object_names', set(original_objects) ==
       {Path(n).stem + '.olean' for n in expected_sources} | {'ThetaProductProbe.olean'})
    fixture_hashes = {n: v['sha256'] for n, v in manifest['modules'].items()}
    common_start_keys = {'generation', 'module', 'command', 'started_utc', 'production_sources_before',
                        'production_objects_before', 'runner_sha256', 'executable_sha256', 'lean_path',
                        'timeout_seconds', 'scientific_effect', 'scope', 'child_pid'}
    regular_start_keys = common_start_keys | {'manifest_sha256', 'fixture_before', 'own_objects_before',
                                             'baseline_development_receipts', 'dependency_file_metadata_count', 'threads'}
    probe_start_keys = common_start_keys | {'original_compile_receipt', 'original_compile_receipt_sha256',
        'original_compile_returncode', 'original_control_pass', 'original_baseline_source_sha256',
        'original_baseline_objects', 'original_manifest_sha256', 'probe_source_sha256',
        'probe_manifest_sha256', 'imported_runner_sha256'}
    common_post_keys = {'checks', 'control_pass', 'ended_utc', 'returncode', 'seconds',
                        'stderr_sha256', 'stdout_sha256', 'timed_out'}
    common_regular_checks = {'not_timed_out', 'stderr_empty_or_exact_audit_progress',
        'manifest_unchanged', 'production_sources_unchanged', 'production_objects_unchanged',
        'own_imported_objects_unchanged', 'fixtures_unchanged',
        'no_import_or_unknown_identifier_failure', 'dependency_metadata_unchanged'}
    baseline_local_checks = {'local_binding:' + c['name'] + ':' + s for c in cases for s in SUFFIXES}
    expected_check_names = {
        'NegativeFixtureBaseline': common_regular_checks | {'compiler_success', 'no_errors'} | baseline_local_checks,
        'NegativeFixtureBindingProbe': {'compiler_success', 'not_timed_out', 'stderr_empty', 'no_errors',
            'original_receipt_unchanged', 'original_objects_unchanged', 'probe_unchanged',
            'production_sources_unchanged', 'production_objects_unchanged', 'dependency_metadata_unchanged'} |
            {'local_binding:' + ref for ref in references},
        'NegativeConstructorMutants': common_regular_checks | {'compiler_rejected', 'no_errors_outside_mutant_namespaces'} |
            {'intended_range_rejection:' + c['name'] for c in cases},
        'NegativeUnusedAxiom': common_regular_checks | {'compiler_success', 'no_errors', 'axiom_is_private_and_unused'},
        'NegativeUnusedAxiomAudit': common_regular_checks | {'compiler_rejected', 'whole_module_private_axiom_rejection',
                                                           'no_false_success_marker'},
    }
    records = {}
    outputs = {}
    for key, module in zip(names, modules):
        ck(key + ':receipt_path', re.fullmatch(r'negative-runs/\d{8}T\d{6}Z-' + module +
           r'-[0-9a-f]{8}/RECEIPT\.json', index[key]) is not None)
        path = root / index[key]
        r = read(path)
        records[key] = r
        is_probe = key == 'binding_probe_receipt'
        start_keys = probe_start_keys if is_probe else regular_start_keys
        if key not in {'positive_baseline_receipt', 'binding_probe_receipt'}:
            start_keys = start_keys | {'two_part_positive_acceptance'}
        start = read(path.with_name('START.json'))
        ck(key + ':exact_start_schema_and_equality', set(start) == start_keys and
           all(k in r and r[k] == v for k, v in start.items()))
        post_keys = common_post_keys | ({'output_objects'} if is_probe else
            {'errors', 'own_objects_after', 'production_sources_after', 'production_objects_after'})
        ck(key + ':exact_terminal_schema', set(r) == start_keys | post_keys)
        ck(key + ':generation_and_module', r['generation'] == GENERATION and r['module'] == module)
        source_dir = executed_probe if is_probe else executed_generation
        expected_command = [original['command'][0], '-j2', '-M4096']
        if module != 'NegativeConstructorMutants':
            expected_command.append('-DwarningAsError=true')
        expected_command += ['-o', str(source_dir / 'build' / (module + '.olean')),
                             str(source_dir / (module + '.lean'))]
        ck(key + ':exact_command_and_import_path', r['command'] == expected_command and
           r['lean_path'] == original['lean_path'])
        expected_runner = (PROBE_RUNNER_SHA if is_probe else
                           BASELINE_RUNNER_SHA if key == 'positive_baseline_receipt' else LATER_RUNNER_SHA)
        ck(key + ':archived_runner_identity', sha(path.with_name('RUNNER.py').read_bytes()) ==
           r['runner_sha256'] == expected_runner)
        ck(key + ':actual_not_timeout', r['timed_out'] is False and r['child_pid'] > 0 and
           r['executable_sha256'] == LEAN_SHA and r['scientific_effect'] == 'NONE' and
           r['timeout_seconds'] == (420 if module == 'NegativeUnusedAxiomAudit' else 240) and
           0 <= r['seconds'] < r['timeout_seconds'] + 10)
        for stream in ['stdout', 'stderr']:
            b = (path.parent / (stream + '.txt')).read_bytes()
            ck(key + ':' + stream + '_digest', sha(b) == r[stream + '_sha256'])
        ck(key + ':complete_production_source_map', r['production_sources_before'] == expected_development_sources)
        ck(key + ':exact_nineteen_frozen_projection',
           {n: r['production_sources_before'][n] for n in expected_sources} == expected_sources)
        ck(key + ':complete_production_object_map', r['production_objects_before'] == original_objects)
        ck(key + ':exact_control_names', set(r['checks']) == expected_check_names[module] and
           all(type(v) is bool for v in r['checks'].values()))
        if is_probe:
            ck(key + ':archived_imported_runner', sha(path.with_name('IMPORTED_RUNNER.py').read_bytes()) ==
               r['imported_runner_sha256'] == PROBE_IMPORTED_RUNNER_SHA)
            ck(key + ':source_and_object_unchanged_observations',
               r['checks']['production_sources_unchanged'] is True and
               r['checks']['production_objects_unchanged'] is True)
        else:
            ck(key + ':fixture_map_and_manifest', r['fixture_before'] == fixture_hashes and
               r['manifest_sha256'] == MANIFEST_SHA and r['threads'] == 2)
            ck(key + ':source_unchanged', r['production_sources_before'] == r['production_sources_after'])
            ck(key + ':imported_objects_unchanged', r['production_objects_before'] == r['production_objects_after'])
            ck(key + ':local_imported_objects_unchanged', all(r['own_objects_after'].get(n) == h
               for n, h in r['own_objects_before'].items() if not n.startswith(module + '.')))
            ck(key + ':exact_development_receipt_selection',
               r['baseline_development_receipts'] == original['baseline_development_receipts'])
            for name, relative in r['baseline_development_receipts'].items():
                development = read(root / relative)
                ck(key + ':development_binding:' + name, development['source'] == name + '.lean' and
                   development['returncode'] == 0 and development['timed_out'] is False and
                   development['source_unchanged'] is True and
                   development['source_sha256'] == expected_sources[name + '.lean'] and
                   development['output_sha256'] == original_objects[name + '.olean'])
        output = (path.parent / 'stdout.txt').read_text()
        stderr = (path.parent / 'stderr.txt').read_text()
        outputs[key] = output
        ck(key + ':no_import_failure', re.search(r'unknown (?:identifier|constant|module)|object file .+ does not exist|failed to import', output + stderr, re.I) is None)
        ck(key + ':stderr_scope', stderr == '' or (module == 'NegativeUnusedAxiomAudit' and all(
           re.fullmatch(r'LIFETIME_AUDIT_PROGRESS (?:START|[A-Za-z0-9_.]+ COUNT [0-9]+)', line)
           for line in stderr.splitlines())))
        errors = [{'line': int(m.group(2)), 'column': int(m.group(3)), 'message': m.group(4)}
                  for m in re.finditer(r'^(.+\.lean):(\d+):(\d+): error(?:\([^)]*\))?: (.*)$', output, re.M)]
        ck(key + ':error_source_paths', all(Path(m.group(1)).name == module + '.lean' and
           (m.group(1) == module + '.lean' or m.group(1) == str(source_dir / (module + '.lean')))
           for m in re.finditer(r'^(.+\.lean):(\d+):(\d+): error(?:\([^)]*\))?: (.*)$', output, re.M)))
        if not is_probe:
            ck(key + ':actual_error_list', r['errors'] == errors)
        if module in {'NegativeFixtureBaseline', 'NegativeFixtureBindingProbe', 'NegativeUnusedAxiom'}:
            ck(key + ':actual_no_errors', not errors)
        if key != 'positive_baseline_receipt':
            ck(key + ':all_actual_control_checks', r['control_pass'] is True and all(r['checks'].values()))
    baseline = records['positive_baseline_receipt']
    probe = records['binding_probe_receipt']
    ck('original_print_elision_failure_preserved', baseline['returncode'] == 0 and
       baseline['control_pass'] is False and all(v for k, v in baseline['checks'].items() if not k.startswith('local_binding:')) and
       all(baseline['checks'][k] is False for k in baseline_local_checks))
    ck('original_baseline_only_expected_object', baseline['own_objects_before'] == {} and
       set(baseline['own_objects_after']) == {'NegativeFixtureBaseline.olean'})
    ck('probe_original_object_and_source_binding', probe['original_compile_receipt'] == index['positive_baseline_receipt'] and
       probe['original_compile_receipt_sha256'] == BASELINE_RECEIPT_SHA and
       probe['original_baseline_source_sha256'] == manifest['modules']['NegativeFixtureBaseline']['sha256'] and
       probe['original_manifest_sha256'] == MANIFEST_SHA and probe['returncode'] == 0 and
       probe['original_compile_returncode'] == 0 and probe['original_control_pass'] is False and
       probe['original_baseline_objects'] == baseline['own_objects_after'] and
       probe['probe_source_sha256'] == PROBE_SOURCE_SHA and probe['probe_manifest_sha256'] == PROBE_MANIFEST_SHA)
    for name, digest in probe['original_baseline_objects'].items():
        ck('actual_baseline_object:' + name, sha((generation / 'build' / name).read_bytes()) == digest)
    ck('probe_only_expected_object', set(probe['output_objects']) == {'NegativeFixtureBindingProbe.olean'})
    for name, digest in probe['output_objects'].items():
        ck('actual_probe_object:' + name, sha((probe_dir / 'build' / name).read_bytes()) == digest)
    probe_output = outputs['binding_probe_receipt']
    for ref in references:
        ck('actual_local_proof_binding:' + ref, ref in probe_output)
    ck('exact_acceptance_path', index['two_part_acceptance'] ==
       'negative-runs/positive-acceptance-' + GENERATION + '/TWO_PART_ACCEPTANCE.json')
    acceptance = read(root / index['two_part_acceptance'])
    ck('two_part_acceptance_bound_to_actual_runs', acceptance['status'] == 'PASS' and
       acceptance['generation'] == GENERATION and
       acceptance['positive_baseline_receipt'] == BASELINE_RECEIPT and
       acceptance['positive_baseline_receipt_sha256'] == BASELINE_RECEIPT_SHA and
       acceptance['binding_probe_receipt'] == PROBE_RECEIPT and
       acceptance['binding_probe_receipt_sha256'] == PROBE_RECEIPT_SHA and
       acceptance['baseline_source_sha256'] == manifest['modules']['NegativeFixtureBaseline']['sha256'] and
       acceptance['baseline_manifest_sha256'] == MANIFEST_SHA and
       acceptance['baseline_objects'] == probe['original_baseline_objects'] and
       acceptance['original_baseline_control_pass'] is False and acceptance['bindings_verified'] == 21 and
       acceptance['original_baseline_actual_lean_exit'] == acceptance['binding_probe_actual_lean_exit'] == 0 and
       acceptance['scientific_effect'] == 'NONE')
    mutants = records['mutants_receipt']
    ck('mutants_exact_two_part_admission', mutants['two_part_positive_acceptance'] == {
       'path': index['two_part_acceptance'], 'sha256': sha((root / index['two_part_acceptance']).read_bytes())})
    ck('actual_mutants_rejected', mutants['returncode'] == 1 and mutants['manifest_sha256'] == MANIFEST_SHA)
    output = outputs['mutants_receipt']
    errors = [(int(m.group(1)), m.group(2)) for m in re.finditer(r'^.+\.lean:(\d+):\d+: error(?:\([^)]*\))?: (.*)$', output, re.M)]
    for c in cases:
        lo, hi = c['required_error_line_range']
        ck('actual_intended_mutation_refusal:' + c['name'], any(lo <= line <= hi for line, _ in errors))
    ck('actual_errors_only_inside_reviewed_mutants', all(any(
       c['combined_namespace_range'][0] <= line <= c['combined_namespace_range'][1]
       for c in cases) for line, _ in errors))
    carrier = records['axiom_carrier_receipt']
    rejected = records['axiom_rejection_receipt']
    ck('negative_generation_object_chain', mutants['own_objects_before'] == baseline['own_objects_after'] and
       mutants['own_objects_after'] == mutants['own_objects_before'] and
       carrier['own_objects_before'] == mutants['own_objects_after'] and
       set(carrier['own_objects_after']) == {'NegativeFixtureBaseline.olean', 'NegativeUnusedAxiom.olean'} and
       rejected['own_objects_before'] == carrier['own_objects_after'] and
       rejected['own_objects_after'] == rejected['own_objects_before'])
    for name, digest in rejected['own_objects_after'].items():
        ck('actual_final_negative_object:' + name, sha((generation / 'build' / name).read_bytes()) == digest)
    ck('unused_axiom_carrier_compiled', carrier['returncode'] == 0 and carrier['manifest_sha256'] == MANIFEST_SHA)
    output = outputs['axiom_rejection_receipt']
    ck('actual_private_unused_axiom_refusal', rejected['returncode'] == 1 and rejected['manifest_sha256'] == MANIFEST_SHA and
       'LIFETIME_AUDIT_MODULE NegativeUnusedAxiom COUNT' in output and
       re.search(r'error(?:\([^)]*\))?: forbidden transitive axiom _private\.[^\n]*c291UnusedCustomAxiom', output) is not None and
       'LIFETIME_AUDIT_STANDARD_ONLY_PASS' not in output)
    return {'checks': checks, 'constructor_mutations': 7, 'private_unused_axiom_mutations': 1,
            'positive_acceptance': 'two actual parts; original observation failure preserved', 'scientific_effect': 'NONE'}
