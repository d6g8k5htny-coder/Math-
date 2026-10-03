"""Timeout diagnostics must retain evidence without weakening the replay gate."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'frontiers/downstream_gate_20260925/run_validation.py'
SPEC = importlib.util.spec_from_file_location('downstream_validation', SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class ValidationTimeoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.command = [sys.executable, '-B', '-S', 'test.py']

    def test_partial_binary_streams_survive_timeout_unchanged(self):
        # Without the timeout handler, neither partial stream reaches disk.
        stdout, stderr = b'partial stdout\x00\xe2\x82', b'partial stderr\xff\n'
        timeout = subprocess.TimeoutExpired(self.command, 30, output=stdout, stderr=stderr)
        with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                M.execute(self.command, self.out, self.out, 'tests_normal', mode='normal')
        self.assertIs(caught.exception, timeout)
        self.assertTrue((self.out / 'tests_normal.stdout').is_file(), 'partial stdout was discarded')
        self.assertEqual((self.out / 'tests_normal.stdout').read_bytes(), stdout)
        self.assertEqual((self.out / 'tests_normal.stderr').read_bytes(), stderr)

    def test_timeout_metadata_has_exact_invocation_and_elapsed_time(self):
        command = [sys.executable, '-B', '-O', '-S', '-m', 'unittest']
        timeout = subprocess.TimeoutExpired(command, 30, output=b'out', stderr=b'err')
        with mock.patch.object(M.subprocess, 'run', side_effect=timeout) as run:
            with mock.patch.object(M.time, 'monotonic', side_effect=[100.0, 130.25]):
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    M.execute(command, self.out, self.out, 'mutation_optimized_allow_green_ci',
                              mutant=True, mode='optimized', mutation='allow_green_ci')
        self.assertIs(caught.exception, timeout)
        self.assertEqual(run.call_args.kwargs['timeout'], 30)
        self.assertTrue(run.call_args.kwargs['capture_output'])
        self.assertTrue(run.call_args.kwargs['text'])
        record = json.loads((self.out / 'mutation_optimized_allow_green_ci.timeout.json').read_text())
        self.assertEqual(record, {
            'argv': command, 'cwd': str(self.out),
            'run_name': 'mutation_optimized_allow_green_ci', 'mode': 'optimized',
            'mutation': 'allow_green_ci', 'mutant': True,
            'timeout_seconds': 30, 'elapsed_seconds': 30.25, 'status': 'timed_out',
            'streams': {'stdout': {'present': True, 'bytes': 3},
                        'stderr': {'present': True, 'bytes': 3}},
            'persistence_failures': [],
        })

    def test_none_and_empty_streams_are_distinguished(self):
        for label, payload, present in [('none', None, False), ('empty', b'', True)]:
            with self.subTest(label=label):
                timeout = subprocess.TimeoutExpired(self.command, 30, output=payload, stderr=payload)
                with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
                    with self.assertRaises(subprocess.TimeoutExpired) as caught:
                        M.execute(self.command, self.out, self.out, label, mode='normal')
                self.assertIs(caught.exception, timeout)
                self.assertEqual((self.out / (label + '.stdout')).read_bytes(), b'')
                self.assertEqual((self.out / (label + '.stderr')).read_bytes(), b'')
                record = json.loads((self.out / (label + '.timeout.json')).read_text())
                for stream in ('stdout', 'stderr'):
                    self.assertEqual(record['streams'][stream], {'present': present, 'bytes': 0})
                self.assertIsNone(record['mutation'])
                self.assertFalse(record['mutant'])

    def test_failed_stream_write_preserves_other_stream_and_original_timeout(self):
        (self.out / 'broken.stdout').mkdir()  # A deterministic real filesystem failure.
        timeout = subprocess.TimeoutExpired(self.command, 30, output=b'out', stderr=b'err')
        with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                M.execute(self.command, self.out, self.out, 'broken', mode='normal')
        self.assertIs(caught.exception, timeout)
        self.assertEqual((self.out / 'broken.stderr').read_bytes(), b'err')
        record = json.loads((self.out / 'broken.timeout.json').read_text())
        self.assertEqual(len(record['persistence_failures']), 1)
        self.assertIn('broken.stdout', record['persistence_failures'][0])
        self.assertIn('IsADirectoryError', record['persistence_failures'][0])
        self.assertTrue(any('broken.stdout' in note for note in timeout.__notes__))

    def test_failed_metadata_write_does_not_mask_original_timeout(self):
        (self.out / 'broken.timeout.json').mkdir()
        timeout = subprocess.TimeoutExpired(self.command, 30, output=b'out', stderr=b'err')
        with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                M.execute(self.command, self.out, self.out, 'broken', mode='normal')
        self.assertIs(caught.exception, timeout)
        self.assertEqual((self.out / 'broken.stdout').read_bytes(), b'out')
        self.assertEqual((self.out / 'broken.stderr').read_bytes(), b'err')
        self.assertTrue(any('broken.timeout.json' in note for note in timeout.__notes__))

    def test_other_subprocess_errors_are_not_caught_as_timeouts(self):
        error = FileNotFoundError('missing executable')
        with mock.patch.object(M.subprocess, 'run', side_effect=error):
            with self.assertRaises(FileNotFoundError) as caught:
                M.execute(self.command, self.out, self.out, 'missing', mode='normal')
        self.assertIs(caught.exception, error)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_completed_baseline_behavior_and_outputs_are_unchanged(self):
        completed = subprocess.CompletedProcess(self.command, 0, 'baseline stdout', 'Ran 71 tests\nOK\n')
        with mock.patch.object(M.subprocess, 'run', return_value=completed):
            M.execute(self.command, self.out, self.out, 'baseline', mode='normal')
        self.assertEqual((self.out / 'baseline.stdout').read_text(), completed.stdout)
        self.assertEqual((self.out / 'baseline.stderr').read_text(), completed.stderr)
        self.assertFalse((self.out / 'baseline.timeout.json').exists())

    def test_completed_assertion_rejection_is_still_expected_only_for_mutants(self):
        stderr = 'Ran 71 tests\nAssertionError: changed semantics\nFAILED (failures=1)\n'
        completed = subprocess.CompletedProcess(self.command, 1, '', stderr)
        with mock.patch.object(M.subprocess, 'run', return_value=completed):
            M.execute(self.command, self.out, self.out, 'mutant', mutant=True,
                      mode='normal', mutation='allow_green_ci')
            with self.assertRaisesRegex(RuntimeError, 'baseline failed'):
                M.execute(self.command, self.out, self.out, 'baseline', mode='normal')
        self.assertFalse((self.out / 'mutant.timeout.json').exists())

    def test_completed_bad_coverage_or_program_errors_still_fail(self):
        bad_stderr = [
            'Ran 70 tests\nAssertionError\nFAILED (failures=1)\n',
            'Ran 71 tests\nAssertionError\nFAILED (failures=1, skipped=1)\n',
            'Ran 71 tests\nSyntaxError\nAssertionError\nFAILED (failures=1)\n',
            'Ran 71 tests\nImportError\nAssertionError\nFAILED (failures=1)\n',
            'Ran 71 tests\nERROR: module\nAssertionError\nFAILED (failures=1)\n',
            'Ran 71 tests\nFAILED (errors=1)\n',
            'Ran 71 tests\nOK\n',
        ]
        for stderr in bad_stderr:
            with self.subTest(stderr=stderr):
                completed = subprocess.CompletedProcess(self.command, 1, '', stderr)
                with mock.patch.object(M.subprocess, 'run', return_value=completed):
                    with self.assertRaises(RuntimeError):
                        M.execute(self.command, self.out, self.out, 'bad', mutant=True,
                                  mode='normal', mutation='allow_green_ci')

    def test_main_timeout_keeps_failed_report_and_stops_later_commands(self):
        timeout = subprocess.TimeoutExpired(self.command, 30, output=b'partial', stderr=b'progress')
        for mutant_timeout in (False, True):
            with self.subTest(mutant_timeout=mutant_timeout):
                out = self.out / str(mutant_timeout)
                argv = [str(SCRIPT), '--output', str(out)]
                baseline = subprocess.CompletedProcess(self.command, 0, '', 'Ran 71 tests\nOK\n')
                gate = subprocess.CompletedProcess(self.command, 0, (M.ROOT / 'RESULTS.json').read_bytes(), b'')
                responses = [baseline, gate, timeout] if mutant_timeout else [timeout]
                with mock.patch.object(sys, 'argv', argv):
                    with mock.patch.object(M.subprocess, 'run', side_effect=responses) as run:
                        with self.assertRaises(subprocess.TimeoutExpired) as caught:
                            M.main()
                self.assertIs(caught.exception, timeout)
                self.assertEqual(run.call_count, len(responses))
                report = json.loads((out / 'REPORT.json').read_text())
                self.assertFalse(report['passed'])
                self.assertEqual(report['modes'], [])
                self.assertFalse(report['promotion_permission'])
                self.assertEqual(report['distinct_tests'], 71)
                self.assertEqual(report['distinct_semantic_mutations'], 24)
                self.assertEqual(report['scientific_effect'], 'NONE')
                name = 'mutation_normal_bypass_own_node_eligibility' if mutant_timeout else 'tests_normal'
                self.assertEqual((out / (name + '.stdout')).read_bytes(), b'partial')
                record = json.loads((out / (name + '.timeout.json')).read_text())
                self.assertEqual(record['mutant'], mutant_timeout)
                self.assertEqual(record['mode'], 'normal')
                self.assertEqual(record['mutation'], 'bypass_own_node_eligibility' if mutant_timeout else None)
                self.assertFalse((out / 'tests_optimized.stdout').exists())

    def test_failed_final_report_write_does_not_mask_timeout(self):
        timeout = subprocess.TimeoutExpired(self.command, 30, output=b'out', stderr=b'err')
        out = self.out / 'main'
        real_write = Path.write_text
        def fail_report(path, data, *args, **kwargs):
            if path.name == 'REPORT.json':
                raise OSError('report disk unavailable')
            return real_write(path, data, *args, **kwargs)
        with mock.patch.object(sys, 'argv', [str(SCRIPT), '--output', str(out)]):
            with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
                with mock.patch.object(Path, 'write_text', fail_report):
                    with self.assertRaises(subprocess.TimeoutExpired) as caught:
                        M.main()
        self.assertIs(caught.exception, timeout)
        self.assertTrue(any('REPORT.json' in note for note in timeout.__notes__))
        self.assertTrue((out / 'tests_normal.timeout.json').is_file())
        self.assertFalse((out / 'REPORT.json').exists())

    def test_real_child_partial_bytes_are_retained(self):
        # Only the test wrapper shortens the timeout. Production still supplies 30.
        real_run = subprocess.run
        observed = []
        def short_run(command, **kwargs):
            self.assertEqual(kwargs['timeout'], 30)
            kwargs['timeout'] = 0.5
            try:
                return real_run(command, **kwargs)
            except subprocess.TimeoutExpired as exc:
                observed.append(exc)
                raise
        command = [sys.executable, '-B', '-S', '-c',
                   "import os,time; os.write(1,b'out\\xe2\\x82'); os.write(2,b'err\\xff'); time.sleep(10)"]
        with mock.patch.object(M.subprocess, 'run', side_effect=short_run):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                M.execute(command, self.out, self.out, 'real', mode='normal')
        self.assertIs(caught.exception, observed[0])
        self.assertEqual((self.out / 'real.stdout').read_bytes(), b'out\xe2\x82')
        self.assertEqual((self.out / 'real.stderr').read_bytes(), b'err\xff')
        record = json.loads((self.out / 'real.timeout.json').read_text())
        self.assertEqual(record['timeout_seconds'], 30)
        self.assertGreater(record['elapsed_seconds'], 0)


if __name__ == '__main__':
    unittest.main()
