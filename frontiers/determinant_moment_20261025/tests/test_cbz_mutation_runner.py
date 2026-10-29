"""Exercise the actual outer wrapper with real exact-test subprocesses; no Lean."""
import contextlib
import hashlib
import importlib._bootstrap_external
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / 'tests/run_cbz_mutations.py'
runner = ModuleType('bounded_outer_mutation_runner')
runner.__file__ = str(RUNNER_PATH)
exec(compile(RUNNER_PATH.read_bytes(), str(RUNNER_PATH), 'exec'), runner.__dict__)
SELECTION = ('test_compiled_admission.CompiledAdmissionTests.'
             'test_unused_definition_forbidden_closure_is_rejected')
MODE = 'optimized' if sys.flags.optimize else 'normal'


class OuterMutationRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='outer-mutation-regression-')
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'input/frontiers/fixture'
        (self.root / 'tests').mkdir(parents=True)
        self.core = ('closure = set()\nALLOWED_NAMES = set()\nencode = str\n'
                     'for name in sorted(closure - ALLOWED_NAMES, key=encode):\n    pass\n')
        (self.root / 'compiled_inventory.py').write_text(self.core)
        (self.root / 'gate.py').write_text(
            "CORE_SHA256 = '" + hashlib.sha256(self.core.encode()).hexdigest() + "'\n")
        (self.root / 'manifest.json').write_text(json.dumps({'files': {}}))
        helper = self.root.parents[1] / 'tools/lean_packet_admission.py'
        helper.parent.mkdir(parents=True)
        helper.write_text('# inert shared helper fixture\n')
        workflow = self.root.parents[1] / '.github/workflows/determinant-moment-lean.yml'
        workflow.parent.mkdir(parents=True)
        workflow.write_bytes((ROOT.parents[1] / '.github/workflows/determinant-moment-lean.yml').read_bytes())
        self.serial = 0

    def fixture(self, phase='test', exception='assertion'):
        action = "self.fail('controlled lifecycle assertion')" if exception == 'assertion' else (
            "raise RuntimeError('controlled lifecycle error')")
        condition = 'if mutated():\n            ' + action + '\n'
        body = '    def test_unused_definition_forbidden_closure_is_rejected(self):\n        self.assertTrue(True)\n'
        if phase == 'import':
            prefix = "if mutated():\n    raise RuntimeError('controlled import error')\n"
        else:
            prefix = ''
        if phase == 'test':
            body = '    def test_unused_definition_forbidden_closure_is_rejected(self):\n        ' + condition
        elif phase in ('setup', 'teardown'):
            body = '    def ' + ('setUp' if phase == 'setup' else 'tearDown') + '(self):\n        ' + condition + body
        elif phase == 'cleanup':
            body = ('    def setUp(self):\n        if mutated():\n'
                    '            self.addCleanup(self.adverse_cleanup)\n'
                    '    def adverse_cleanup(self):\n        ' + action + '\n' + body)
        elif phase in ('setup_subtest', 'test_subtest'):
            method = 'setUp' if phase == 'setup_subtest' else 'test_unused_definition_forbidden_closure_is_rejected'
            selected = '' if phase == 'test_subtest' else body
            body = ('    def ' + method + '(self):\n        if mutated():\n'
                    "            with self.subTest(stage='controlled'):\n                " + action + '\n' + selected)
        elif phase == 'skip':
            body = ('    def test_unused_definition_forbidden_closure_is_rejected(self):\n'
                    "        if mutated():\n            self.skipTest('controlled skip')\n")
        source = ('import unittest\nfrom pathlib import Path\n'
                  "def mutated():\n    return 'MUTANT:' in Path('compiled_inventory.py').read_text()\n" +
                  prefix + 'class CompiledAdmissionTests(unittest.TestCase):\n' + body)
        compile(source, 'controlled_fixture', 'exec')
        (self.root / 'tests/test_compiled_admission.py').write_text(source)

    def execute(self, case=None):
        self.serial += 1
        work = self.base / ('work-' + str(self.serial))
        output = self.base / ('evidence-' + str(self.serial))
        work.mkdir(); output.mkdir(); (work / 'test-tmp').mkdir()
        with patch.object(runner, 'ROOT', self.root):
            return runner.execute_case(case or runner.CASES[0], work, output)

    def test_lifecycle_assertions_cannot_masquerade_as_intended_body_kills(self):
        # Omitting phase-aware delegation would count these same-named FAIL lines.
        for phase in ('setup', 'teardown', 'cleanup', 'setup_subtest'):
            with self.subTest(phase=phase, mode=MODE):
                self.fixture(phase)
                record = self.execute()
                self.assertFalse(record['killed_by_intended_assertions'], phase)

    def test_real_body_assertions_and_subtest_assertions_are_intended_kills(self):
        for phase in ('test', 'test_subtest'):
            with self.subTest(phase=phase, mode=MODE):
                self.fixture(phase)
                record = self.execute()
                self.assertTrue(record['killed_by_intended_assertions'], record)

    def test_import_runtime_and_skip_outcomes_never_count_as_kills(self):
        for phase, exception in (('import', 'error'), ('test', 'error'),
                                 ('setup', 'error'), ('teardown', 'error'),
                                 ('cleanup', 'error'), ('skip', 'assertion')):
            with self.subTest(phase=phase, exception=exception):
                self.fixture(phase, exception)
                record = self.execute()
                self.assertFalse(record['killed_by_intended_assertions'], record)
                self.assertIn('selection_results', record, 'outer wrapper must retain the shared structured decision')
                self.assertEqual(record['selection_results'][0]['status'], 'INVALID_MUTANT')

    def test_selection_mode_and_harness_mismatches_reject_actual_wrapper_pairs(self):
        self.assertTrue(hasattr(runner, '_shared'), 'outer wrapper must use the self-tested shared runner')
        self.fixture()
        original = runner._shared.run_selected
        for field, changed in (('selection', SELECTION + '_wrong'),
                               ('mode', 'other'), ('harness_sha256', '0' * 64)):
            def mismatched(*args, **kwargs):
                result = original(*args, **kwargs)
                if result['classification'] == 'ASSERTION_FAILURE':
                    result[field] = changed
                return result
            with self.subTest(field=field), patch.object(runner._shared, 'run_selected', side_effect=mismatched):
                record = self.execute()
                self.assertFalse(record['killed_by_intended_assertions'], record)
                self.assertEqual(record['selection_results'][0]['status'], 'HARNESS_MISMATCH')

    def test_invalid_baseline_cannot_qualify_an_actual_body_failure(self):
        self.assertTrue(hasattr(runner, '_shared'), 'outer wrapper must use the self-tested shared runner')
        self.fixture()
        original = runner._shared.run_selected
        def invalid_baseline(*args, **kwargs):
            result = original(*args, **kwargs)
            if result['classification'] == 'PASS':
                result['classification'] = 'INVALID'
            return result
        with patch.object(runner._shared, 'run_selected', side_effect=invalid_baseline):
            record = self.execute()
        self.assertFalse(record['killed_by_intended_assertions'], record)
        self.assertEqual(record['selection_results'][0]['status'], 'INVALID_BASELINE')

    def test_invalid_return_zero_wrong_and_skipped_reports_are_not_reclassified(self):
        self.assertTrue(hasattr(runner, '_shared'), 'outer wrapper must use the self-tested shared runner')
        self.fixture()
        original = runner._shared.run_selected
        for changes in ({'returncode': 2}, {'returncode': True}, {'tests_run': 0},
                        {'loaded_test_ids': ['other']}, {'skipped_ids': [SELECTION]},
                        {'expected_failure_ids': [SELECTION]}, {'error_ids': [SELECTION]}):
            def invalid_mutant(*args, **kwargs):
                result = original(*args, **kwargs)
                if result['classification'] == 'ASSERTION_FAILURE':
                    result.update(changes)
                    result['classification'] = runner._shared.classify_execution(result)
                return result
            with self.subTest(changes=changes), patch.object(runner._shared, 'run_selected', side_effect=invalid_mutant):
                record = self.execute()
                self.assertFalse(record['killed_by_intended_assertions'], record)
                self.assertEqual(record['selection_results'][0]['status'], 'INVALID_MUTANT')
                if 'returncode' in changes:
                    self.assertEqual(record['exit_code'], changes['returncode'])

    def test_empty_duplicate_and_broad_selections_are_refused(self):
        self.fixture()
        for selections in ((), (SELECTION, SELECTION), ('test_compiled_admission.CompiledAdmissionTests',),
                           ('-k',), ('',)):
            with self.subTest(selections=selections):
                try:
                    self.execute((*runner.CASES[0][:4], selections))
                except Exception as error:
                    self.assertIsInstance(error, ValueError, 'wrong refusal outcome: ' + repr(error))
                else:
                    self.fail('invalid selection was accepted: ' + repr(selections))

    def test_empty_matrix_is_a_failure_instead_of_vacuous_success(self):
        self.assertTrue(callable(getattr(runner, 'mutation_cases', None)), 'outer wrapper must validate the complete matrix')
        with patch.object(runner, 'ROOT', self.root), \
             patch.object(runner, 'mutation_cases', return_value=()), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(runner.main(['--output', str(self.base / 'empty-matrix')]), 1)

    def test_output_children_are_retained_and_source_and_symlink_paths_refuse(self):
        self.assertTrue(callable(getattr(runner, 'create_run_directory', None)), 'outer evidence needs a safe retained destination')
        with patch.object(runner, 'ROOT', self.root):
            first = runner.create_run_directory(self.base / 'reports')
            sentinel = first / 'prior.log'; sentinel.write_text('retained original evidence')
            second = runner.create_run_directory(self.base / 'reports')
            self.assertNotEqual(first, second)
            self.assertEqual(sentinel.read_text(), 'retained original evidence')
            alias = self.base / 'output-alias'; alias.symlink_to(self.base / 'reports', target_is_directory=True)
            for parent in (self.root / 'output', alias, alias / 'child',
                           self.base / 'input/frontiers/fixture/../fixture/output'):
                with self.subTest(parent=str(parent)), self.assertRaises(ValueError):
                    runner.create_run_directory(parent)

    def test_mutant_copy_preserves_every_source_and_external_input_byte(self):
        self.fixture()
        def inventory():
            return {p.relative_to(self.base / 'input').as_posix(): p.read_bytes()
                    for p in (self.base / 'input').rglob('*') if p.is_file()}
        before = inventory()
        record = self.execute()
        self.assertTrue(record['killed_by_intended_assertions'], record)
        self.assertEqual(inventory(), before)
        self.assertEqual((self.root / 'compiled_inventory.py').read_text(), self.core)

    def test_matrix_refuses_a_source_change_even_when_every_mutant_was_killed(self):
        self.assertTrue(callable(getattr(runner, 'mutation_cases', None)), 'outer matrix must check source preservation')
        self.fixture()
        original = runner.execute_case
        def changed_source(*args, **kwargs):
            record = original(*args, **kwargs)
            (self.root / 'unexpected-source-change.txt').write_text('controlled preservation failure')
            return record
        captured = io.StringIO()
        with patch.object(runner, 'ROOT', self.root), \
             patch.object(runner, 'mutation_cases', return_value=(runner.CASES[0],)), \
             patch.object(runner, 'execute_case', side_effect=changed_source), \
             contextlib.redirect_stdout(captured):
            code = runner.main(['--output', str(self.base / 'preservation-evidence')])
        self.assertEqual(code, 1)
        report = json.loads(Path(json.loads(captured.getvalue())['results']).read_text())
        self.assertFalse(report['source_preserved'])
        self.assertFalse(report['all_killed'])
        self.assertTrue(report['mutations'][0]['killed_by_intended_assertions'])

    def test_shared_runner_uses_one_read_and_ignores_timestamp_valid_bytecode(self):
        folder = self.base / 'loader/tests'; folder.mkdir(parents=True)
        shared_path = folder / 'run_git_identity_mutations.py'
        raw = (ROOT / 'tests/run_git_identity_mutations.py').read_bytes()
        shared_path.write_bytes(raw)
        poisoned = raw.decode().replace(
            "    killed = same_harness and baseline_passed and mutant.get('classification') == 'ASSERTION_FAILURE'",
            '    killed = True  # controlled cached classifier bypass', 1)
        self.assertNotEqual(poisoned.encode(), raw, 'controlled cache fixture needs a real bypass')
        cached = Path(importlib.util.cache_from_source(str(shared_path)))
        cached.parent.mkdir()
        cached.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(
            compile(poisoned, str(shared_path), 'exec'), int(shared_path.stat().st_mtime), len(raw)))
        outer_path = folder / 'run_cbz_mutations.py'
        outer = RUNNER_PATH.read_bytes(); outer_path.write_bytes(outer)
        candidate = ModuleType('controlled_cached_outer_runner'); candidate.__file__ = str(outer_path)
        reads = []
        original_read = Path.read_bytes
        def counted_read(path):
            if path == shared_path:
                reads.append(path)
            return original_read(path)
        with patch.object(Path, 'read_bytes', new=counted_read):
            exec(compile(outer, str(outer_path), 'exec'), candidate.__dict__)
        self.assertEqual(reads, [shared_path], 'shared code must execute the sole source read')
        baseline = dict(selection=SELECTION, mode=MODE, harness_sha256='1' * 64, classification='PASS')
        invalid = dict(baseline, classification='INVALID')
        self.assertFalse(candidate._shared.classify_pair(baseline, invalid)['killed'],
                         'timestamp-valid bytecode replaced the shared strict classifier')
        self.assertEqual(candidate.SHARED_RUNNER_SHA256, hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    unittest.main()
