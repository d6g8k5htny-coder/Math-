"""Adverse controls for the bounded downstream-origin self-mutation runner."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tests/run_downstream_origin_mutations.py'


class _ContinuedPastGuard(Exception):
    """The disabled guard let a child start."""


SPEC = importlib.util.spec_from_file_location('downstream_origin_mutations', SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class SelfMutationControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)

    def test_process_record_omission_is_in_mutation_inventory(self):
        self.assertIn('process_record_omission', {case[0] for case in M.CASES})

    def test_actual_suite_origin_bypass_is_in_mutation_inventory(self):
        self.assertIn('actual_origin_bypass', {case[0] for case in M.CASES})

    def test_existing_or_in_tree_output_is_refused(self):
        for path in (self.out, ROOT / 'frontiers/downstream_gate_20260925/unwanted-output'):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError, 'new output outside source'):
                    M.run(path)

    def test_modified_helper_is_refused(self):
        path = self.out / 'changed.py'
        path.write_text('# not the source helper\n')
        with mock.patch.object(M, 'HELPER', path):
            with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                M.verified_helper()

    def test_missing_mutation_anchor_is_refused_and_reported(self):
        output = self.out / 'results'
        first = M.CASES[0]
        missing = ((first[0], 'not an anchor', 'new', first[3]), *M.CASES[1:])
        with mock.patch.object(M, 'CASES', missing):
            with self.assertRaisesRegex(ValueError, 'anchor'):
                M.run(output)
        self.assertEqual(json.loads((output / 'results.json').read_text()), [])

    def test_duplicate_cases_are_refused_before_children(self):
        output = self.out / 'duplicate'
        origin = mock.Mock()
        origin.classify.return_value = {'control_pass': True, 'killed': True, 'collected': 1}
        def children_started(*args, **kwargs):
            raise _ContinuedPastGuard()
        with mock.patch.object(M, 'CASES', (M.CASES[0],) * 4):
            with mock.patch.object(M, 'verified_helper', return_value=origin):
                with mock.patch.object(M.subprocess, 'run', side_effect=children_started) as run:
                    continued = False
                    try:
                        M.run(output)
                    except ValueError as exc:
                        self.assertRegex(str(exc), 'case inventory')
                    except _ContinuedPastGuard:
                        continued = True
                    else:
                        continued = True
                    if continued:
                        self.fail('duplicate case inventory was accepted')
                    run.assert_not_called()
        self.assertEqual(json.loads((output / 'results.json').read_text()), [])

    def test_failed_classification_is_refused_and_reported(self):
        output = self.out / 'failed'
        calls = {'n': 0}
        def run_child(*args, **kwargs):
            calls['n'] += 1
            if calls['n'] > 1:
                raise _ContinuedPastGuard()
            return subprocess.CompletedProcess(['synthetic'], 0, '', '')
        origin = mock.Mock()
        origin.classify.return_value = {'control_pass': False, 'killed': False, 'collected': 0}
        with mock.patch.object(M, 'verified_helper', return_value=origin):
            with mock.patch.object(M.subprocess, 'run', side_effect=run_child):
                continued = False
                try:
                    M.run(output)
                except RuntimeError as exc:
                    self.assertIn('self-mutation failed', str(exc))
                except _ContinuedPastGuard:
                    continued = True
                else:
                    continued = True
                if continued:
                    self.fail('failed classification was accepted')
        rows = json.loads((output / 'results.json').read_text())
        self.assertEqual(len(rows), 1)
        self.assertIs(rows[0]['accepted'], False)

    def test_timeout_evidence_write_failures_do_not_mask_original(self):
        output = self.out / 'timeout'
        timeout = subprocess.TimeoutExpired(['synthetic'], 60, output=b'out\xff', stderr=b'err\xfe')
        write_bytes, write_text = Path.write_bytes, Path.write_text
        def bytes_with_failure(path, data):
            if path.name == 'origin_bypass_normal_baseline.stdout':
                raise OSError('stdout unavailable')
            return write_bytes(path, data)
        def text_with_failure(path, data, *args, **kwargs):
            if path.name == 'results.json':
                raise OSError('results unavailable')
            return write_text(path, data, *args, **kwargs)
        with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
            with mock.patch.object(Path, 'write_bytes', bytes_with_failure):
                with mock.patch.object(Path, 'write_text', text_with_failure):
                    try:
                        M.run(output)
                    except Exception as exc:
                        self.assertIs(exc, timeout)
                    else:
                        self.fail('timeout was not raised')
        self.assertEqual((output / 'origin_bypass_normal_baseline.stderr').read_bytes(), b'err\xfe')
        self.assertTrue(any('stdout unavailable' in note for note in timeout.__notes__))
        self.assertTrue(any('results unavailable' in note for note in timeout.__notes__))

    def test_disabled_self_checks_keep_their_anchors(self):
        source = Path(M.__file__).read_text()
        for name in ('self_verdict_bypass', 'self_inventory_bypass'):
            old, new = next((case[1], case[2]) for case in M.SELF_CASES if case[0] == name)
            prefix = 'if False:' + old[old.index('\n'):]
            rest = new[len(prefix) + 1:]
            anchor_at = rest.index(" = '''")
            with self.subTest(name=name):
                self.assertEqual(source.count(old), 1)
                self.assertTrue(new.startswith(prefix + '\n'))
                self.assertEqual(rest[anchor_at + len(" = '''"):], old + "'''")
                self.assertTrue(rest[:anchor_at].strip().isidentifier())
                mutant = source.replace(old, new, 1)
                self.assertEqual(mutant.count(old), 1)
                at = mutant.index(old)
                self.assertEqual(mutant[at - 3:at], "'''")
                indent = source[source.rfind('\n', 0, source.index(old)) + 1:source.index(old)]
                self.assertNotIn('\n' + indent + old, mutant)
                self.assertIn('\n' + indent + 'if False:' + old[old.index('\n'):], mutant)
                compile(mutant, '<self-mutant:' + name + '>', 'exec')

    def test_self_mutant_binding_rejects_unrelated_assertion(self):
        runner_source = Path(M.__file__).read_text()
        for name, (method, message) in M.INTENDED_SELF_FAILURES.items():
            with self.subTest(name=name):
                self.assertEqual(runner_source.count("self.fail(%r)" % message), 0)
                self.assertEqual(Path(__file__).read_text().count("self.fail(%r)" % message), 1)
                self.assertTrue(M.intended_self_failure(self.failure_stderr(method, message), method, message))
                self.assertFalse(M.intended_self_failure(
                    self.failure_stderr(method, 'self-runner mutation anchor must occur exactly once'), method, message))
                self.assertFalse(M.intended_self_failure(self.failure_stderr('test_other', message), method, message))

    def failure_stderr(self, method, message):
        ident = 'test_downstream_origin_mutations.SelfMutationControls.' + method
        phase = {'tests': [{'id': ident, 'body_entered': True}],
                 'events': [{'id': ident, 'phase': 'body', 'kind': 'failure', 'origin_authorized': True,
                             'origin_frames': [{'function': method}]}]}
        return ('FAIL: ' + method + ' (' + ident + ')\n'
                'AssertionError: ' + message + '\n'
                'Ran 1 test in 0.001s\nFAILED (failures=1)\n'
                'SOURCE_MUTATION_PHASES|' + json.dumps(phase) + '\n')


if __name__ == '__main__':
    unittest.main()
