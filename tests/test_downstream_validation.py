"""Timeout diagnostics must retain evidence without weakening the replay gate."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
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
PACKET = SCRIPT.parent
sys.path.insert(0, str(PACKET))  # git_transition_audit imports hard_gate from its packet
try:
    AUDIT_SPEC = importlib.util.spec_from_file_location('transition_audit', PACKET / 'git_transition_audit.py')
    AUDIT = importlib.util.module_from_spec(AUDIT_SPEC)
    AUDIT_SPEC.loader.exec_module(AUDIT)
finally:
    sys.path.remove(str(PACKET))


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
            'persistence_failures': [], 'diagnostic_failures': [],
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

    def test_clock_failures_preserve_timeout_streams_and_available_metadata(self):
        clocks = [
            ('initial', [OSError('clock start unavailable')]),
            ('elapsed', [100.0, OSError('clock end unavailable')]),
            ('nan', [100.0, float('nan')]),
            ('infinity', [100.0, float('inf')]),
            ('negative', [100.0, 99.0]),
        ]
        for label, readings in clocks:
            with self.subTest(label=label):
                timeout = subprocess.TimeoutExpired(self.command, 30, output=b'out', stderr=b'err')
                with mock.patch.object(M.time, 'monotonic', side_effect=readings):
                    with mock.patch.object(M.subprocess, 'run', side_effect=timeout) as run:
                        with self.assertRaises(subprocess.TimeoutExpired) as caught:
                            M.execute(self.command, self.out, self.out, label, mode='normal')
                self.assertIs(caught.exception, timeout)
                self.assertEqual(run.call_count, 1)
                self.assertEqual((self.out / (label + '.stdout')).read_bytes(), b'out')
                self.assertEqual((self.out / (label + '.stderr')).read_bytes(), b'err')
                def reject_non_json(value):
                    raise ValueError(value)
                record = json.loads((self.out / (label + '.timeout.json')).read_text(),
                                    parse_constant=reject_non_json)
                self.assertIsNone(record['elapsed_seconds'])
                self.assertEqual(len(record['diagnostic_failures']), 1)
                self.assertTrue(any('clock' in note or 'elapsed' in note for note in timeout.__notes__))

    def test_timeout_cwd_is_the_supplied_path_without_filesystem_resolution(self):
        timeout = subprocess.TimeoutExpired(self.command, 30, output=b'out', stderr=b'err')
        with mock.patch.object(Path, 'resolve', side_effect=OSError('cwd unavailable')):
            with mock.patch.object(M.subprocess, 'run', side_effect=timeout):
                with self.assertRaises(subprocess.TimeoutExpired) as caught:
                    M.execute(self.command, Path('relative-cwd'), self.out, 'cwd', mode='normal')
        self.assertIs(caught.exception, timeout)
        self.assertEqual((self.out / 'cwd.stdout').read_bytes(), b'out')
        record = json.loads((self.out / 'cwd.timeout.json').read_text())
        self.assertEqual(record['cwd'], 'relative-cwd')

    def test_initial_clock_failure_does_not_change_completed_baseline(self):
        completed = subprocess.CompletedProcess(self.command, 0, 'out', 'Ran 71 tests\nOK\n')
        with mock.patch.object(M.time, 'monotonic', side_effect=OSError('clock unavailable')):
            with mock.patch.object(M.subprocess, 'run', return_value=completed):
                M.execute(self.command, self.out, self.out, 'baseline', mode='normal')
        self.assertEqual((self.out / 'baseline.stdout').read_text(), 'out')
        self.assertEqual((self.out / 'baseline.stderr').read_text(), completed.stderr)
        self.assertFalse((self.out / 'baseline.timeout.json').exists())

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


class ReplayGateRefusalControls(unittest.TestCase):
    """Mutation-gap controls: refusal paths of execute()/main() that the tests above leave unpinned."""
    BASELINE = 'Ran 71 tests\nOK\n'
    DETECTED = 'Ran 71 tests\nAssertionError: changed semantics\nFAILED (failures=1)\n'

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name)
        self.command = [sys.executable, '-B', '-S', 'test.py']
        self.two = dict(list(M.MUTANTS.items())[:2])

    def completed(self, code, stderr, stdout=''):
        return subprocess.CompletedProcess(self.command, code, stdout, stderr)

    def gate(self, code=0, stdout=None):
        return self.completed(code, b'', (M.ROOT / 'RESULTS.json').read_bytes() if stdout is None else stdout)

    def assert_refused(self, code, stderr, mutant):
        with mock.patch.object(M.subprocess, 'run', return_value=self.completed(code, stderr)):
            with self.assertRaises(RuntimeError):
                M.execute(self.command, self.out, self.out, 'run', mutant=mutant, mode='normal',
                          mutation='allow_green_ci' if mutant else None)

    def main(self, out, responses, mutants):
        with mock.patch.object(sys, 'argv', [str(SCRIPT), '--output', str(out)]):
            with mock.patch.object(M, 'MUTANTS', mutants):
                with mock.patch.object(M.subprocess, 'run', side_effect=responses) as self.run:
                    with mock.patch.object(M, 'print', create=True):  # keep the success JSON out of test logs
                        M.main()

    def test_test_count_must_match_exactly(self):
        self.assert_refused(0, 'Ran 710 tests\nOK\n', False)
        self.assert_refused(1, 'Ran 711 tests\nAssertionError\nFAILED (failures=1)\n', True)

    def test_mutant_requires_every_detection_signal(self):
        for code, stderr in [(0, self.DETECTED), (2, self.DETECTED), (-9, self.DETECTED),
                             (1, 'Ran 71 tests\nFAILED (failures=1)\n'),
                             (1, 'Ran 71 tests\nAssertionError\nFAILED (errors=1)\n')]:
            with self.subTest(code=code, stderr=stderr):
                self.assert_refused(code, stderr, True)

    def test_signal_killed_baseline_refused(self):
        self.assert_refused(-9, self.BASELINE, False)

    def test_success_replays_both_modes_and_every_mutant(self):
        # A first-two-only production loop must not satisfy this full-map control.
        # Child responses are synthetic; main() still creates real copies and logs.
        out = (self.out / 'ok').resolve()
        mutants = dict(M.MUTANTS)
        self.assertEqual(len(mutants), 24)
        source_files = {p.relative_to(M.ROOT).as_posix(): p.read_bytes()
                        for p in M.ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        source_identities = {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                             for name, data in source_files.items()}
        responses, streams = {}, {}
        for mode, flags in (('normal', []), ('optimized', ['-O'])):
            prefix = [sys.executable, '-E', '-B', *flags, '-S']
            tests = prefix + ['-m', 'unittest', 'discover', '-p', 'test_*.py', '-v']
            baseline_stdout = 'baseline ' + mode + '\n'
            responses[(tuple(tests), str(M.ROOT))] = self.completed(0, self.BASELINE, baseline_stdout)
            responses[(tuple(prefix + ['hard_gate.py']), str(M.ROOT))] = self.gate()
            streams['tests_' + mode] = (baseline_stdout, self.BASELINE)
            for name in mutants:
                stdout = mode + ':' + name + ':stdout\n'
                stderr = mode + ':' + name + ':stderr\n' + self.DETECTED
                scratch = out / 'mutants' / mode / name
                responses[(tuple(tests), str(scratch))] = self.completed(1, stderr, stdout)
                streams['mutation_' + mode + '_' + name] = (stdout, stderr)
        def replay(command, *, cwd, **kwargs):
            return responses[(tuple(command), str(cwd))]
        self.main(out, replay, mutants)
        self.assertEqual(self.run.call_count, 52)
        for offset, mode, flags in ((0, 'normal', []), (26, 'optimized', ['-O'])):
            prefix = [sys.executable, '-E', '-B', *flags, '-S']
            tests = prefix + ['-m', 'unittest', 'discover', '-p', 'test_*.py', '-v']
            baseline, gate = self.run.call_args_list[offset:offset + 2]
            self.assertEqual(baseline.args[0], tests)
            self.assertEqual(baseline.kwargs['cwd'], M.ROOT)
            self.assertEqual(gate.args[0], prefix + ['hard_gate.py'])
            self.assertEqual(gate.kwargs['cwd'], M.ROOT)
            self.assertEqual((out / ('output_' + mode + '.json')).read_bytes(), source_files['RESULTS.json'])
            self.assertEqual({p.name for p in (out / 'mutants' / mode).iterdir()}, set(mutants))
            for index, (name, (old, new)) in enumerate(mutants.items(), 2):
                scratch = out / 'mutants' / mode / name
                call = self.run.call_args_list[offset + index]
                self.assertEqual(call.args[0], tests)
                self.assertEqual(call.kwargs['cwd'], scratch)
                copied = {p.relative_to(scratch).as_posix(): p.read_bytes()
                          for p in scratch.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
                expected = dict(source_files)
                expected['hard_gate.py'] = source_files['hard_gate.py'].replace(old.encode(), new.encode())
                self.assertEqual(copied, expected, mode + ':' + name)
        report = json.loads((out / 'REPORT.json').read_text())
        self.assertTrue(report['passed'])
        self.assertEqual(report['modes'], ['normal', 'optimized'])
        self.assertEqual(report['distinct_semantic_mutations'], 24)
        self.assertTrue(report['sources_unchanged'])
        self.assertEqual(report['source_files'], source_identities)
        self.assertEqual({p.relative_to(M.ROOT).as_posix(): p.read_bytes()
                          for p in M.ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}, source_files)
        for name, (stdout, stderr) in streams.items():
            self.assertEqual((out / (name + '.stdout')).read_bytes(), stdout.encode('utf-8'))
            self.assertEqual((out / (name + '.stderr')).read_bytes(), stderr.encode('utf-8'))
        mutation_logs = {name for name in streams if name.startswith('mutation_')}
        self.assertEqual(len(mutation_logs), 48)
        for stream in ('stdout', 'stderr'):
            self.assertEqual({p.stem for p in out.glob('mutation_*.' + stream)}, mutation_logs)

    def test_actual_child_modes_ignore_ambient_optimization(self):
        # Capture both production constructors; replace only their payloads.
        # These real diagnostic children do not run the 71-test packet.
        out = self.out / 'mode-commands'
        responses = [self.completed(0, self.BASELINE), self.gate(), self.completed(1, self.DETECTED)] * 2
        self.main(out, responses, dict(list(self.two.items())[:1]))
        calls = self.run.call_args_list
        for offset, expected in ((0, 0), (3, 1)):
            tests = calls[offset].args[0]
            gate = calls[offset + 1].args[0]
            prefixes = {'tests_and_mutants': tests[:tests.index('-m')], 'hard_gate': gate[:-1]}
            for constructor, prefix in prefixes.items():
                for ambient in (None, '0', '1', '2'):
                    with self.subTest(expected=expected, constructor=constructor, ambient=ambient):
                        env = {key: value for key, value in os.environ.items()
                               if key not in ('PYTHONOPTIMIZE', 'PYTHONHOME', 'PYTHONPATH')}
                        if ambient is not None:
                            env['PYTHONOPTIMIZE'] = ambient
                        child = subprocess.run(prefix + ['-c', 'import sys; print(sys.flags.optimize)'],
                                               env=env, capture_output=True, text=True, timeout=10)
                        self.assertEqual(child.returncode, 0, child.stderr)
                        self.assertEqual(child.stderr, '')
                        self.assertEqual(child.stdout, str(expected) + '\n')

    def test_real_child_exit_status_distinguishes_assertions_from_abnormal_termination(self):
        # All mutant children emit identical synthetic unittest-shaped text.
        # Their actual exit status, not that text, distinguishes termination.
        real_run = subprocess.run
        cases = [('zero', 0, True), ('assertion', 1, True), ('abnormal', 2, True),
                 ('signal', -signal.SIGKILL, True), ('baseline_signal', -signal.SIGKILL, False)]
        for label, code, mutant in cases:
            with self.subTest(label=label):
                end = ('os.kill(os.getpid(), signal.SIGKILL)' if code < 0 else 'sys.exit(' + str(code) + ')')
                payload = 'import os, signal, sys; sys.stderr.write(' + repr(self.DETECTED) + '); sys.stderr.flush(); ' + end
                command = [sys.executable, '-E', '-B', '-S', '-c', payload]
                observed = []
                def run(*args, **kwargs):
                    child = real_run(*args, **kwargs)
                    observed.append(child)
                    return child
                accepted = True
                with mock.patch.object(M.subprocess, 'run', side_effect=run):
                    try:
                        M.execute(command, self.out, self.out, label, mutant=mutant,
                                  mode='normal', mutation='controlled_stderr' if mutant else None)
                    except RuntimeError:
                        accepted = False
                self.assertEqual(len(observed), 1)
                self.assertEqual(observed[0].returncode, code)
                self.assertEqual(observed[0].stderr, self.DETECTED)
                self.assertEqual((self.out / (label + '.stderr')).read_text(), self.DETECTED)
                self.assertEqual(accepted, mutant and code == 1)

    def test_source_change_during_replay_refused(self):
        out = self.out / 'drift'
        packet = self.out / 'packet'
        shutil.copytree(M.ROOT, packet, ignore=shutil.ignore_patterns('__pycache__'))
        original_identities = M.identities
        commands = 0
        snapshots = []
        def identities():
            snapshot = original_identities()
            snapshots.append((commands, snapshot))
            return snapshot
        with mock.patch.object(M, 'ROOT', packet):
            responses = [self.completed(0, self.BASELINE), self.gate(), self.completed(1, self.DETECTED)] * 2
            def replay(*args, **kwargs):
                nonlocal commands
                commands += 1
                if commands == 1:
                    source = packet / 'README.md'
                    source.write_bytes(source.read_bytes() + b'\nPhysical mid-replay drift fixture.\n')
                return responses[commands - 1]
            with mock.patch.object(M, 'identities', side_effect=identities):
                with self.assertRaisesRegex(RuntimeError, 'source files changed'):
                    self.main(out, replay, dict(list(self.two.items())[:1]))
        self.assertEqual(commands, 6)
        self.assertEqual([count for count, _ in snapshots], [0, 6])
        self.assertNotEqual(snapshots[0][1]['README.md'], snapshots[1][1]['README.md'])
        report = json.loads((out / 'REPORT.json').read_text())
        self.assertFalse(report['passed'])
        self.assertNotIn('sources_unchanged', report)
        self.assertNotIn('source_files', report)
        self.assertFalse(report['promotion_permission'])
        self.assertEqual(report['scientific_effect'], 'NONE')

    def test_output_must_be_new_and_outside_source_before_any_command(self):
        base, link = self.out / 'base', self.out / 'link'
        (base / 'packet').mkdir(parents=True)
        (base / 'existing').mkdir()
        link.symlink_to(base, target_is_directory=True)
        for where in (base, link):  # canonical and symlinked spellings of one directory
            # Production ROOT is resolved (Path(__file__).resolve()); keep that invariant in the mock.
            packet = (where / 'packet').resolve()
            for out in (where / 'packet' / 'out', where / 'existing'):
                with self.subTest(where=where.name, out=out.name):
                    with mock.patch.object(M, 'ROOT', packet):
                        with self.assertRaisesRegex(RuntimeError, 'new output outside source'):
                            self.main(out, AssertionError('no command may run'), self.two)
                    self.assertEqual(self.run.call_count, 0)

    def test_gate_entry_must_exit_zero_with_exact_results(self):
        for gate in (self.gate(stdout=b'{}'), self.gate(code=1)):
            with self.subTest(code=gate.returncode):
                out = self.out / ('gate' + str(gate.returncode))
                with self.assertRaisesRegex(RuntimeError, 'entry/result mismatch'):
                    self.main(out, [self.completed(0, self.BASELINE), gate], self.two)
                self.assertFalse(json.loads((out / 'REPORT.json').read_text())['passed'])

    def test_absent_mutation_anchor_refused(self):
        # Replacing the uniqueness check with count > 0 must fail the duplicate case.
        # Supply a complete synthetic success stream so acceptance cannot hide
        # behind exhausted responses. The packet fixture and report are real files.
        for label in ('absent', 'duplicate'):
            with self.subTest(anchor=label):
                packet = (self.out / ('packet-' + label)).resolve()
                shutil.copytree(M.ROOT, packet, ignore=shutil.ignore_patterns('__pycache__'))
                mutants = {'absent': ('no such anchor text', 'x')}
                name = 'absent'
                if label == 'duplicate':
                    mutants = dict(M.MUTANTS)
                    name, (old, new) = next(iter(mutants.items()))
                    source = (packet / 'hard_gate.py').read_text()
                    self.assertEqual(source.count(old), 1)
                    source += '\n# Duplicate anchor fixture: ' + old + '\n'
                    self.assertEqual(source.count(old), 2)
                    compile(source, '<duplicate anchor fixture>', 'exec')
                    compile(source.replace(old, new), '<duplicate anchor replacement>', 'exec')
                    (packet / 'hard_gate.py').write_text(source)
                before = {p.relative_to(packet).as_posix(): p.read_bytes()
                          for p in packet.rglob('*') if p.is_file()}
                out = self.out / ('anchor-' + label)
                with mock.patch.object(M, 'ROOT', packet):
                    responses = ([self.completed(0, self.BASELINE), self.gate()] +
                                 [self.completed(1, self.DETECTED) for _ in mutants]) * 2
                    with self.assertRaisesRegex(RuntimeError, 'nonunique mutation: ' + name):
                        self.main(out, responses, mutants)
                self.assertEqual(self.run.call_count, 2)
                self.assertFalse((out / 'mutants').exists())
                self.assertEqual({p.relative_to(packet).as_posix(): p.read_bytes()
                                  for p in packet.rglob('*') if p.is_file()}, before)
                report = json.loads((out / 'REPORT.json').read_text())
                self.assertFalse(report['passed'])
                self.assertEqual(report['modes'], [])
                self.assertFalse(report['promotion_permission'])
                self.assertEqual(report['scientific_effect'], 'NONE')

    def test_uncompilable_mutation_refused_before_replay(self):
        old = next(iter(M.MUTANTS.values()))[0]
        with self.assertRaises(SyntaxError):
            self.main(self.out / 'syntax', [self.completed(0, self.BASELINE), self.gate()], {'broken': (old, 'if (:')})
        self.assertEqual(self.run.call_count, 2)
        self.assertFalse((self.out / 'syntax' / 'mutants').exists())

    def test_successful_replay_without_report_fails(self):
        real_write = Path.write_text
        def fail_report(path, data, *args, **kwargs):
            if path.name == 'REPORT.json':
                raise OSError('report disk unavailable')
            return real_write(path, data, *args, **kwargs)
        responses = [self.completed(0, self.BASELINE), self.gate(), self.completed(1, self.DETECTED)] * 2
        with mock.patch.object(Path, 'write_text', fail_report):
            with self.assertRaises(OSError):
                self.main(self.out / 'noreport', responses, dict(list(self.two.items())[:1]))

    def test_identities_cover_every_packet_file(self):
        packet = self.out / 'packet'
        for name in ('a.py', 'DATA.json', 'sub/b.md', '__pycache__/c.pyc'):
            (packet / name).parent.mkdir(parents=True, exist_ok=True)
            (packet / name).write_text(name)
        with mock.patch.object(M, 'ROOT', packet):
            self.assertEqual(set(M.identities()), {'a.py', 'DATA.json', 'sub/b.md'})


def isolated_git_env(environ):
    """Fixture Git environment: no ambient GIT_* (GIT_DIR, GIT_CONFIG_PARAMETERS, ...), no global/system config."""
    env = {k: v for k, v in environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
    return env


class TransitionAuditRefusalControls(unittest.TestCase):
    """Mutation-gap controls for git_transition_audit.py, which the lane runs once on a passing transition."""
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        # The fixture, the in-process audit (AUDIT.git) and the child CLI all inherit this isolated environment.
        environ = mock.patch.dict(os.environ)
        environ.start()
        self.addCleanup(environ.stop)
        self.isolate_environ()
        self.repo = self.init_repo(Path(self.temp.name) / 'repo')

    @staticmethod
    def isolate_environ():
        isolated = isolated_git_env(os.environ)
        os.environ.clear()
        os.environ.update(isolated)

    def init_repo(self, repo):
        repo.mkdir()
        run = lambda *a: subprocess.run(['git', '-C', str(repo), *a], check=True, capture_output=True)
        run('init', '-q', '--template=')  # no template hooks
        for key, value in (('user.name', 'local test'), ('user.email', 'test@example.invalid'),
                           ('commit.gpgSign', 'false'), ('tag.gpgSign', 'false'), ('core.hooksPath', os.devnull)):
            run('config', key, value)
        return repo

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], check=True, capture_output=True, text=True).stdout.strip()

    def commit(self, graph, *files):
        (self.repo / 'GRAPH.json').write_text(json.dumps(graph))
        for name in ('lemma.md', *files):
            (self.repo / name).write_text('bytes of ' + name + '\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'fixture')
        return self.git('rev-parse', 'HEAD')

    @staticmethod
    def graph(**extra):
        nodes = {'L': {'classification': 'PROVED_REVIEWED', 'controlling': False, 'source': 'lemma.md'}, **extra}
        return {'schema_version': 1, 'nodes': nodes, 'edges': []}

    def cli(self, base, head, out):
        # -E plus the outer optimization level: ambient PYTHON* cannot change the child's mode or imports.
        return subprocess.run([sys.executable, '-E', '-B', *(['-O'] * sys.flags.optimize), '-S',
                               str(PACKET / 'git_transition_audit.py'), '--repo', str(self.repo),
                               '--base', base, '--head', head, '--graph', 'GRAPH.json', '--output', str(out)],
                              env=dict(os.environ), capture_output=True, text=True, timeout=120)

    def test_fixture_and_audit_ignore_hostile_ambient_git_config(self):
        tmp = Path(self.temp.name)
        hooks = tmp / 'hostile-hooks'
        hooks.mkdir()
        (hooks / 'pre-commit').write_text('#!/bin/sh\nexit 1\n')
        (hooks / 'pre-commit').chmod(0o755)
        hostile = tmp / 'hostile.gitconfig'
        hostile.write_text('[commit]\n\tgpgSign = true\n[tag]\n\tgpgSign = true\n'
                           '[gpg]\n\tprogram = %s\n[core]\n\thooksPath = %s\n' % (tmp / 'no-such-gpg', hooks))
        probe = tmp / 'probe'
        probe.mkdir()
        bare = lambda *a: subprocess.run(['git', '-C', str(probe), *a], capture_output=True,
                                         env={**os.environ, 'GIT_CONFIG_GLOBAL': str(hostile)})
        for args in (('init', '-q'), ('config', 'user.name', 'p'), ('config', 'user.email', 'p@example.invalid')):
            self.assertEqual(bare(*args).returncode, 0)
        self.assertNotEqual(bare('commit', '-q', '--allow-empty', '-m', 'x').returncode, 0)  # the hostile context bites
        os.environ.update(GIT_CONFIG_GLOBAL=str(hostile), GIT_DIR=str(tmp / 'elsewhere.git'),
                          GIT_INDEX_FILE=str(tmp / 'elsewhere.index'))
        self.isolate_environ()
        self.repo = self.init_repo(tmp / 'isolated')
        graph = self.graph()
        base, head = self.commit(graph), self.commit(graph, 'unrelated.md')
        self.assertTrue(AUDIT.audit(self.repo, base, head, 'GRAPH.json')['check_passed'])
        run = self.cli(base, head, tmp / 'hostile-audit.json')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertFalse((tmp / 'elsewhere.git').exists() or (tmp / 'elsewhere.index').exists())

    def test_revision_must_be_full_lowercase_commit(self):
        rev = self.commit(self.graph())
        for bad in (rev[:12], rev.upper(), 'HEAD'):
            with self.subTest(revision=bad), self.assertRaisesRegex(ValueError, 'immutable commit ID'):
                AUDIT.read_snapshot(self.repo, bad, 'GRAPH.json')
        with self.assertRaisesRegex(ValueError, 'not a commit'):
            AUDIT.read_snapshot(self.repo, self.git('rev-parse', rev + '^{tree}'), 'GRAPH.json')

    def test_each_snapshot_graph_is_validated(self):
        graph = self.graph()
        graph['nodes']['L']['classification'] = 'NOT_A_CLASSIFICATION'
        with self.assertRaises(ValueError):
            AUDIT.read_snapshot(self.repo, self.commit(graph), 'GRAPH.json')

    def test_blank_source_reference_refused(self):
        rev = self.commit(self.graph(W={'classification': 'PROVED_REVIEWED', 'controlling': False, 'source': '   '}))
        with self.assertRaisesRegex(ValueError, 'nonempty string'):
            AUDIT.read_snapshot(self.repo, rev, 'GRAPH.json')

    def test_non_blob_tree_source_object_refused(self):
        rev, real = self.commit(self.graph()), AUDIT.git
        def fake(repo, *args, missing=False):
            if args[:2] == ('cat-file', '-t') and args[2].endswith(':lemma.md'):
                return b'commit\n'
            return real(repo, *args, missing=missing)
        with mock.patch.object(AUDIT, 'git', side_effect=fake):
            with self.assertRaisesRegex(ValueError, 'blob or directory tree'):
                AUDIT.read_snapshot(self.repo, rev, 'GRAPH.json')

    def test_unresolved_controlling_source_fails(self):
        for source in ('absent.md', 'external:paper'):
            with self.subTest(source=source):
                graph = self.graph(C={'classification': 'PROVED_REVIEWED', 'controlling': True, 'source': source})
                base, head = self.commit(graph), self.commit(graph, 'unrelated-' + source.replace(':', '_'))
                r = AUDIT.audit(self.repo, base, head, 'GRAPH.json')
                self.assertEqual((r['controlling_impacted'], r['illegal_controlling']), ([], []))
                self.assertEqual(r['unresolved_controlling_sources'], ['C'])
                self.assertFalse(r['check_passed'])

    def test_unchanged_illegal_controlling_fails_and_cli_exits_2(self):
        graph = self.graph(X={'classification': 'OPEN_ACTIVE', 'controlling': True, 'source': 'lemma.md'})
        base, head = self.commit(graph), self.commit(graph, 'unrelated.md')
        r = AUDIT.audit(self.repo, base, head, 'GRAPH.json')
        self.assertEqual((r['controlling_impacted'], r['unresolved_controlling_sources']), ([], []))
        self.assertEqual(len(r['illegal_controlling']), 1)
        self.assertFalse(r['check_passed'])
        out = Path(self.temp.name) / 'audit.json'
        run = self.cli(base, head, out)
        self.assertEqual(run.returncode, 2, run.stderr)
        self.assertFalse(json.loads(out.read_text())['check_passed'])

    def test_cli_refusals_exit_2_without_output(self):
        base, head = self.commit(self.graph()), self.commit(self.graph(), 'unrelated.md')
        good = Path(self.temp.name) / 'good.json'
        self.assertEqual(self.cli(base, head, good).returncode, 0)
        existing = Path(self.temp.name) / 'existing.json'
        existing.write_text('keep')
        for label, b, out in (('mutable', 'main', Path(self.temp.name) / 'x.json'), ('inside', base, self.repo / 'audit.json'),
                              ('existing', base, existing)):
            with self.subTest(label=label):
                run = self.cli(b, head, out)
                self.assertEqual(run.returncode, 2, run.stderr)
                self.assertIn('TRANSITION_CHECK_REFUSED', run.stderr)
                self.assertEqual(out.read_text() if out.exists() else None, 'keep' if label == 'existing' else None)

if __name__ == '__main__':
    unittest.main()
