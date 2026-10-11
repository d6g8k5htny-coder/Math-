"""Offline Q1/Q6 controls, not execution of the forty proposed experiments."""
import ast
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import stat
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/c183_qualification_ledger.py'
SPEC = importlib.util.spec_from_file_location('c183_ledger', SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)
FIXTURE = json.loads((ROOT / 'tests/fixtures/c183_qualification_ledger_cases.json').read_text())
API = ('planned_cases', 'parse_outcomes', 'original_predicate', 'verify_sources',
       'historical_ledger', 'build_ledger', 'stop_after_child', 'strict_json', 'read_zip_members', 'main')


def originals():
    return {name: text.encode('utf-8') for name, text in FIXTURE['members'].items()}


def sources():
    return {name: text.encode('utf-8') for name, text in FIXTURE['source_files'].items()}


def transcript(statuses=('ok', 'ok', 'ok'), footer='OK', extra=''):
    rows = [f'{name} ... {status}' for name, status in zip(FIXTURE['synthetic']['ids'], statuses)]
    return ('\n'.join(rows) + '\n' + extra + '\nRan 3 tests in 0.001s\n\n' + footer + '\n').encode()


def small_zip(entries):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w') as z:
        for name, raw, mode in entries:
            info = zipfile.ZipInfo(name)
            info.create_system = 3
            info.external_attr = mode << 16
            z.writestr(info, raw)
    return out.getvalue()


class C183LedgerControls(unittest.TestCase):
    def setUp(self):
        for name in API:
            self.assertTrue(callable(getattr(M, name, None)), 'required offline API absent: ' + name)

    def parsed(self, raw=None, **kw):
        return M.parse_outcomes(transcript() if raw is None else raw, FIXTURE['synthetic']['ids'], **kw)

    def test_original_baseline_and_mutant_populations_are_separate(self):
        ledger = M.historical_ledger(originals())
        self.assertEqual(ledger['baseline']['counts'], {'ok': 71, 'FAIL': 0, 'ERROR': 0})
        self.assertEqual(ledger['numeric_mutant']['counts'], {'ok': 68, 'FAIL': 2, 'ERROR': 1})
        self.assertEqual(ledger['numeric_mutant']['wrapper_decision'], 'REFUSED')
        self.assertEqual(ledger['baseline']['wrapper_decision'], 'UNKNOWN')
        self.assertIsNone(ledger['baseline']['returncode'])
        self.assertIsNone(ledger['numeric_mutant']['returncode'])
        self.assertEqual(ledger['cause'], 'UNKNOWN')

    def test_original_method_identities_and_error_are_retained(self):
        ledger = M.historical_ledger(originals())
        rows = ledger['numeric_mutant']['outcomes']
        self.assertEqual(len(rows), 71)
        self.assertEqual({x['method'].split(' ')[0] for x in rows if x['status'] == 'FAIL'},
                         {'test_required_flag_must_be_exact_boolean', 'test_promotion_boundary_checks_required_boolean'})
        self.assertEqual([x['method'].split(' ')[0] for x in rows if x['status'] == 'ERROR'],
                         ['test_git_d1_component_change_revalidates_d1_d2_d3'])

    def test_original_report_keeps_incomplete_mode_scope_and_exact_runtime_literal(self):
        record = M.historical_ledger(originals())['original_report']
        self.assertFalse(record['passed'])
        self.assertEqual(record['modes'], [])
        self.assertIn('Oct  1 2026', record['python'])
        self.assertFalse(record['promotion_permission'])

    def test_one_byte_changed_historical_member_is_refused(self):
        for name in originals():
            with self.subTest(name=name):
                data = originals(); data[name] += b'\n'
                with self.assertRaises(ValueError): M.historical_ledger(data)

    def test_missing_or_extra_historical_member_is_refused(self):
        data = originals(); data.pop('tests_normal.stdout')
        with self.assertRaises(ValueError): M.historical_ledger(data)
        data = originals(); data['invented.txt'] = b''
        with self.assertRaises(ValueError): M.historical_ledger(data)

    def test_forty_not_run_cases_have_exact_groups_and_suite_populations(self):
        cases = M.planned_cases()
        self.assertEqual(len(cases), 40)
        self.assertEqual(len({x['id'] for x in cases}), 40)
        self.assertEqual(sum(x['group'] == 'matrix' for x in cases), 28)
        self.assertEqual(sum(x['full_suite'] for x in cases), 30)
        self.assertEqual({x['cell'] for x in cases if x['group'] == 'matrix'}, set('UIMDHTQ'))
        for case in cases:
            self.assertEqual(case['execution'], 'NOT_RUN')
            self.assertIsNone(case['outcomes'])
        cases[0]['execution'] = 'invented'
        self.assertEqual(M.planned_cases()[0]['execution'], 'NOT_RUN')

    def test_three_terminal_outcomes_are_complete(self):
        record = self.parsed()
        self.assertTrue(record['complete'])
        self.assertEqual(record['observed_count'], 3)
        self.assertEqual(record['counts'], {'ok': 3, 'FAIL': 0, 'ERROR': 0})

    def test_summary_without_methods_is_not_execution(self):
        record = self.parsed(b'\nRan 3 tests in 0.001s\n\nOK\n')
        self.assertFalse(record['complete'])
        self.assertEqual(record['observed_count'], 0)

    def test_truncated_summary_remains_partial(self):
        record = self.parsed(transcript()[:-4])
        self.assertFalse(record['complete'])
        self.assertEqual(record['observed_count'], 3)

    def test_duplicate_unknown_or_skipped_method_is_refused(self):
        first = (FIXTURE['synthetic']['ids'][0] + ' ... ok\n').encode()
        for raw in (first + transcript(), transcript().replace(b'test_a', b'test_z'),
                    transcript().replace(b'... ok', b"... skipped 'why'", 1)):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError): self.parsed(raw)

    def test_summary_and_outcome_totals_must_agree(self):
        for raw in (transcript().replace(b'Ran 3', b'Ran 4'),
                    transcript(('ok', 'FAIL', 'FAIL'), 'FAILED (failures=1)', 'AssertionError\n')):
            with self.assertRaises(ValueError): self.parsed(raw)

    def test_invalid_expected_method_population_refused(self):
        ids = FIXTURE['synthetic']['ids']
        for population in ([], ids + [ids[0]], ['unknown'], 'not-a-list'):
            with self.assertRaises(ValueError): M.parse_outcomes(transcript(), population)

    def test_timeout_and_interruption_do_not_complete_discovered_methods(self):
        raw = (FIXTURE['synthetic']['ids'][0] + ' ... ok\n').encode()
        for termination in ('timed_out', 'interrupted'):
            record = self.parsed(raw, termination=termination)
            self.assertEqual(record['expected_count'], 3)
            self.assertEqual(record['observed_count'], 1)
            self.assertFalse(record['complete'])
            self.assertEqual(record['termination'], termination)
        self.assertFalse(self.parsed(transcript(), termination='timed_out')['complete'])

    def test_invalid_utf8_preserves_identity_and_incomplete_scope(self):
        raw = transcript() + b'\xe2\x82'
        record = self.parsed(raw, termination='timed_out')
        self.assertEqual(record['stderr'], {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'present': True})
        self.assertFalse(record['complete'])
        self.assertIn('invalid_utf8', record['limitations'])

    def test_absent_and_empty_streams_are_distinct(self):
        absent = M.parse_outcomes(None, FIXTURE['synthetic']['ids'], termination='timed_out')
        empty = self.parsed(b'', termination='timed_out')
        self.assertFalse(absent['stderr']['present'])
        self.assertTrue(empty['stderr']['present'])
        self.assertFalse(absent['complete'])

    def test_original_predicate_accepts_baseline_and_assertion_only_mutant(self):
        self.assertEqual(M.original_predicate(transcript(), 0, False, 3), 'ACCEPTED')
        raw = transcript(('ok', 'FAIL', 'FAIL'), 'FAILED (failures=2)', 'AssertionError\n')
        self.assertEqual(M.original_predicate(raw, 1, True, 3), 'ACCEPTED')
        self.assertEqual(M.original_predicate(raw, 0, True, 3), 'REFUSED')
        self.assertEqual(M.original_predicate(raw, None, True, 3), 'UNKNOWN')

    def test_original_predicate_refuses_program_errors_missing_signals_and_skips(self):
        raw = transcript(('ok', 'FAIL', 'FAIL'), 'FAILED (failures=2)', 'AssertionError\n')
        for bad in (raw+b'\nERROR: actual\n', raw+b'SyntaxError', raw+b'ImportError',
                    raw.replace(b'AssertionError', b'other'), raw+b'skipped=1'):
            with self.subTest(bad=bad):
                self.assertEqual(M.original_predicate(bad, 1, True, 3), 'REFUSED')
        self.assertEqual(M.original_predicate(raw+b'\nERROR: actual\n', None, True, 3), 'REFUSED')

    def test_original_source_pins_and_numeric_mutation_are_distinct(self):
        result = M.verify_sources(sources())
        self.assertEqual(len(result['pristine']), 13)
        self.assertEqual(len(result['method_ids']), 71)
        self.assertEqual(len(result['mutation_anchors']), 24)
        self.assertEqual(result['numeric_mutant']['bytes'], 28246)
        self.assertNotEqual(result['numeric_mutant']['sha256'], result['pristine']['hard_gate.py']['sha256'])
        self.assertEqual(result['wrapper_blob'], 'fcf6480529d6b521628e2635e7c1e271ecfa39a4')

    def test_changed_missing_extra_or_unpinned_source_is_refused(self):
        for name in sources():
            data = sources(); data[name] += b'\n'
            with self.subTest(name=name):
                with self.assertRaises(ValueError): M.verify_sources(data)
        data = sources(); data.pop('GRAPH.json')
        with self.assertRaises(ValueError): M.verify_sources(data)
        data = sources(); data['observer.py'] = b'# not pristine\n'
        with self.assertRaises(ValueError): M.verify_sources(data)

    def test_mutated_assertion_or_current_wrapper_is_not_historical_source(self):
        for name, old, new in [('test_hard_gate.py', b'self.assert', b'self.ignore'),
                               ('run_validation.py', b"'-B'", b"'-E', '-B'")]:
            data = sources(); data[name] = data[name].replace(old, new, 1)
            with self.assertRaises(ValueError): M.verify_sources(data)

    def test_strict_json_rejects_duplicates_nonfinite_and_non_object(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'[]', b'null'):
            with self.assertRaises(ValueError): M.strict_json(raw)
        self.assertEqual(M.strict_json(b'{"a":1}'), {'a': 1})

    def test_stop_semantics_are_after_exit_not_process_control(self):
        self.assertFalse(M.stop_after_child('exited', False))
        self.assertTrue(M.stop_after_child('exited', True))
        self.assertTrue(M.stop_after_child('timed_out', False))
        self.assertTrue(M.stop_after_child('interrupted', False))
        self.assertFalse(M.stop_after_child('exited', True, expected_error_control=True, wrapper_refused=True))
        with self.assertRaises(ValueError): M.stop_after_child('running', True)
        with self.assertRaises(ValueError): M.stop_after_child('exited', True, expected_error_control=True, wrapper_refused=False)
        with self.assertRaises(ValueError): M.stop_after_child('exited', 1)

    def test_zip_reader_uses_bounded_fixed_members_and_no_extraction(self):
        raw = small_zip([('one.txt', b'one', stat.S_IFREG | 0o600)])
        result = M.read_zip_members(raw, ['one.txt'], expected_sha256=hashlib.sha256(raw).hexdigest(), expected_bytes=len(raw))
        self.assertEqual(result, {'one.txt': b'one'})
        with self.assertRaises(ValueError): M.read_zip_members(raw, ['one.txt'], expected_sha256='0'*64, expected_bytes=len(raw))
        with self.assertRaises(ValueError): M.read_zip_members(raw, ['one.txt'], expected_sha256=hashlib.sha256(raw).hexdigest(), expected_bytes=len(raw)+1)

    def test_zip_unsafe_duplicate_missing_and_nonregular_members_refused(self):
        cases = [[('../bad', b'x', stat.S_IFREG)], [('/bad', b'x', stat.S_IFREG)],
                 [('a\\b', b'x', stat.S_IFREG)], [('link', b'target', stat.S_IFLNK)],
                 [('same', b'1', stat.S_IFREG), ('same', b'2', stat.S_IFREG)]]
        for entries in cases:
            with self.subTest(entries=entries):
                raw = small_zip(entries)
                with self.assertRaises(ValueError): M.read_zip_members(raw, [entries[0][0]], expected_sha256=hashlib.sha256(raw).hexdigest(), expected_bytes=len(raw))
        raw = small_zip([('x', b'x', stat.S_IFREG)])
        with self.assertRaises(ValueError): M.read_zip_members(raw, ['absent'], expected_sha256=hashlib.sha256(raw).hexdigest(), expected_bytes=len(raw))

    def test_zip_size_bound_refused_before_payload_use(self):
        raw = small_zip([('x', b'x'*(1024*1024+1), stat.S_IFREG)])
        with self.assertRaises(ValueError): M.read_zip_members(raw, ['x'], expected_sha256=hashlib.sha256(raw).hexdigest(), expected_bytes=len(raw))

    def test_unprovided_gates_are_not_run_and_not_fabricated(self):
        result = M.build_ledger()
        self.assertEqual(result['gates'], {'historical_members': 'NOT_RUN', 'archive_identity': 'NOT_RUN', 'source_identity': 'NOT_RUN'})
        self.assertIsNone(result['historical'])
        self.assertIsNone(result['observer_identity'])
        self.assertEqual(result['cause'], 'UNKNOWN')
        self.assertFalse(result['promotion_permission'])
        self.assertEqual(result['scientific_effect'], 'NONE')

    def test_verified_members_do_not_imply_archive_or_runtime_verification(self):
        result = M.build_ledger(members=originals(), source_files=sources())
        self.assertEqual(result['gates'], {'historical_members': 'VERIFIED', 'archive_identity': 'NOT_RUN', 'source_identity': 'VERIFIED'})
        self.assertEqual(result['runtime_provenance'], 'INCOMPLETE_HISTORICAL')
        self.assertTrue(all(x['execution'] == 'NOT_RUN' for x in result['planned_cases']))

    def test_ledger_is_deterministic_and_inputs_unchanged(self):
        members, source = originals(), sources()
        before = copy.deepcopy((members, source))
        a = M.build_ledger(members=members, source_files=source)
        b = M.build_ledger(members=members, source_files=source)
        self.assertEqual(a, b)
        self.assertEqual((members, source), before)

    def test_cli_without_inputs_is_valid_not_run_json(self):
        out = io.StringIO()
        self.assertEqual(M.main([], output=out), 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result, M.build_ledger())

    def test_helper_has_no_execution_network_or_source_import_capability(self):
        tree = ast.parse(SCRIPT.read_text())
        imports = {n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.Import)}
        imports |= {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module}
        self.assertTrue(imports <= {'argparse','ast','hashlib','io','json','pathlib','re','stat','sys','zipfile'})
        calls = {n.func.id for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
        self.assertFalse(calls & {'eval','exec','compile','__import__'})
        attrs = {n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        self.assertFalse(attrs & {'extract','extractall','write_bytes','write_text','unlink','rmdir','chmod'})


if __name__ == '__main__':
    unittest.main()
