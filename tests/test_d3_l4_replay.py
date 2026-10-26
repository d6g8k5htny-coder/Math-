"""Real-process replay-protocol tests; synthetic fixtures are not coefficient evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DRIVER = ROOT / 'tools' / 'd3_l4_replay.py'


class ReplayTests(unittest.TestCase):
    def load(self):
        self.assertTrue(DRIVER.is_file(), 'source-bound d3 L4 replay driver is missing')
        if hasattr(self, '_module'):
            return self._module
        spec = importlib.util.spec_from_file_location('d3_l4_replay', DRIVER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._module = module
        return module

    def fixture(self, module, root):
        packet = root / module.PACKET
        packet.mkdir(parents=True)
        records = []
        for name in module.FILE_NAMES:
            data = ('synthetic protocol fixture: ' + name + '\n').encode()
            (packet / name).write_bytes(data)
            records.append({'path': name, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest(),
                            'git_blob': module.git_blob(data)})
        (root / 'source.txt').write_bytes(b'synthetic upstream\n')
        manifest = {'object': module.OBJECT, 'scientific_effect': 'NONE',
                    'source_commit': module.SOURCE_COMMIT,
                    'source_repository': module.REPOSITORY,
                    'files': records,
                    'upstream_pins': [{'path': 'source.txt',
                                       'git_blob': module.git_blob(b'synthetic upstream\n')}]}
        raw = (json.dumps(manifest, sort_keys=True) + '\n').encode()
        (packet / 'SOURCE_FILES.json').write_bytes(raw)
        return packet, hashlib.sha256(raw).hexdigest()

    def test_00_driver_exists(self):
        self.assertTrue(DRIVER.is_file(), 'source-bound d3 L4 replay driver is missing')

    def test_valid_synthetic_snapshot(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); _, pin = self.fixture(m, root)
            self.assertEqual(len(m.validate_snapshot(root, pin)['files']), 9)

    def test_manifest_pin_required(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); self.fixture(m, root)
            with self.assertRaisesRegex(m.ReplayError, 'manifest_pin'):
                m.validate_snapshot(root, '0' * 64)

    def test_corrupt_missing_extra_and_directory(self):
        m = self.load()
        for mutation in ('corrupt', 'missing', 'extra', 'directory'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as t:
                root = Path(t); p, pin = self.fixture(m, root)
                path = p / 'PROOF.md'
                if mutation == 'corrupt': path.write_text('changed')
                elif mutation == 'missing': path.unlink()
                elif mutation == 'extra': (p / 'unlisted.txt').write_text('extra')
                else: path.unlink(); path.mkdir()
                with self.assertRaises(m.ReplayError): m.validate_snapshot(root, pin)

    def test_symlink_file_and_parent_rejected(self):
        m = self.load()
        for parent in (False, True):
            with self.subTest(parent=parent), tempfile.TemporaryDirectory() as t:
                root = Path(t); p, pin = self.fixture(m, root)
                path = p.parent if parent else p / 'PROOF.md'
                moved = root / 'displaced'
                path.rename(moved); path.symlink_to(moved, target_is_directory=parent)
                with self.assertRaisesRegex(m.ReplayError, 'symlink'):
                    m.validate_snapshot(root, pin)

    def test_upstream_corruption(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); _, pin = self.fixture(m, root)
            (root / 'source.txt').write_text('corrupt')
            with self.assertRaisesRegex(m.ReplayError, 'git_blob'):
                m.validate_snapshot(root, pin)

    def test_paths_reject_escape_absolute_and_aliases(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            for path in ('../x', '/x', './x', 'a/../x', 'a//x', 'a\\x', ''):
                with self.subTest(path=path), self.assertRaises(m.ReplayError):
                    m.safe_file(Path(t), path)

    def test_json_duplicate_and_nonfinite_rejected(self):
        m = self.load()
        for value in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'{"a":1e999}', b'{} trailing'):
            with self.subTest(value=value), self.assertRaises(m.ReplayError): m.strict_json(value)

    def test_exact_result_mismatch_not_accepted(self):
        m = self.load()
        with self.assertRaisesRegex(m.ReplayError, 'stdout_mismatch'):
            m.compare_output(b'{"coefficient":1}\n', b'{"coefficient":2}\n', 'exact')

    def crosscheck(self):
        return {'source_sha256': 'abc', 'rows': [{'D_interval': ['2.3','2.4'],
                 'disk_diagnostic_is_certificate': False,
                 'independent_disk_midpoint_diagnostic': 2.35}], 'reference_checks': {}}

    def test_crosscheck_diagnostic_float_portability_only(self):
        m = self.load(); expected = self.crosscheck(); actual = self.crosscheck()
        actual['rows'][0]['independent_disk_midpoint_diagnostic'] = 2.3500000000000005
        m.compare_output(json.dumps(actual).encode(), json.dumps(expected).encode(), 'crosschecks')
        actual['rows'][0]['D_interval'] = ['2.2','2.4']
        with self.assertRaisesRegex(m.ReplayError, 'crosscheck_exact_fields'):
            m.compare_output(json.dumps(actual).encode(), json.dumps(expected).encode(), 'crosschecks')

    def test_crosscheck_bad_diagnostic_rejected(self):
        m = self.load(); expected = self.crosscheck()
        for diagnostic in (float('nan'), float('inf'), 5, '2.35', True):
            actual = self.crosscheck(); actual['rows'][0]['independent_disk_midpoint_diagnostic'] = diagnostic
            with self.subTest(diagnostic=diagnostic), self.assertRaises(m.ReplayError):
                m.compare_output(json.dumps(actual).encode(), json.dumps(expected).encode(), 'crosschecks')

    def test_unittest_summary_required(self):
        m = self.load()
        for stderr in (b'', b'Ran 0 tests\n\nOK\n', b'Ran 7 tests\n\nFAILED\n'):
            with self.assertRaisesRegex(m.ReplayError, 'test_summary'):
                m.compare_output(b'', None, 'tests', stderr)
        m.compare_output(b'', None, 'tests', b'.......\n----------------------------------------------------------------------\nRan 7 tests in 0.2s\n\nOK\n')

    def run_fixture(self, source, expected=b'ok\n', timeout=5):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); script = root / 'fixture.py'; script.write_text(source)
            logs = root / 'logs'; logs.mkdir()
            return m.run_step([sys.executable, '-B', '-S', str(script)], root, logs,
                              'fixture', expected, 'exact', timeout)

    def test_real_process_success(self):
        self.assertEqual(self.run_fixture("print('ok')")['returncode'], 0)

    def test_real_process_crash_wrong_exit_and_stderr(self):
        m = self.load()
        for source, code in [("raise RuntimeError('not a mathematical rejection')", 'exit'),
                             ("print('ok');raise SystemExit(1)", 'exit'),
                             ("import sys;print('bad',file=sys.stderr);print('ok')", 'stderr')]:
            with self.subTest(source=source), self.assertRaisesRegex(m.ReplayError, code):
                self.run_fixture(source)

    def test_real_process_timeout_fails_closed(self):
        m = self.load()
        with self.assertRaisesRegex(m.ReplayError, 'timeout'):
            self.run_fixture('import time;time.sleep(30)', timeout=0.1)

    def test_cli_invalid_mode_is_refused(self):
        self.load()
        run = subprocess.run([sys.executable, '-B', '-S', str(DRIVER), '--mode', 'pretend-pass'],
                             capture_output=True)
        self.assertEqual(run.returncode, 2)

    def test_execution_identities_reject_dirty_tool(self):
        m = self.load()
        self.assertTrue(hasattr(m, 'execution_identities'), 'execution-source binding is missing')
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            for name in ('tools/d3_l4_replay.py', 'tests/test_d3_l4_replay.py',
                         '.github/workflows/d3-l4-anisotropic.yml'):
                p = root / name; p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('synthetic execution-source fixture\n')
            def git(*args):
                return subprocess.run(['git', *args], cwd=root, check=True, capture_output=True).stdout.decode().strip()
            git('init', '-q'); git('add', '.')
            git('-c', 'user.name=Protocol fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'synthetic fixture')
            head = git('rev-parse', 'HEAD')
            self.assertEqual(len(m.execution_identities(root, head)), 3)
            (root / 'tools/d3_l4_replay.py').write_text('dirty execution source')
            with self.assertRaisesRegex(m.ReplayError, 'execution_source_drift'):
                m.execution_identities(root, head)

    def test_cli_missing_source_retains_failed_receipt(self):
        self.load()
        for mode in ('normal', 'optimized'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as t:
                root = Path(t); output = root / 'evidence'
                run = subprocess.run([sys.executable, '-B', '-S', str(DRIVER),
                                      '--mode', mode, '--root', str(root), '--output', str(output)],
                                     capture_output=True)
                self.assertNotEqual(run.returncode, 0)
                self.assertEqual(run.stdout, b'')
                receipt = json.loads((output / 'receipt.json').read_text())
                self.assertEqual(receipt['status'], 'FAIL')
                self.assertEqual(receipt['mode'], mode)
                self.assertIn('missing_or_nonregular_source', receipt['failure'])

    def test_cli_refuses_reusing_existing_evidence(self):
        self.load()
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); output = root / 'evidence'; output.mkdir()
            old = output / 'receipt.json'; old.write_text('historical receipt')
            run = subprocess.run([sys.executable, '-B', '-S', str(DRIVER), '--mode', 'normal',
                                  '--root', str(root), '--output', str(output)], capture_output=True)
            self.assertNotEqual(run.returncode, 0)
            self.assertIn(b'evidence_directory_already_exists', run.stderr)
            self.assertEqual(old.read_text(), 'historical receipt')

    def test_workflow_fetches_history_for_proof_reachability(self):
        text = (ROOT / '.github/workflows/d3-l4-anisotropic.yml').read_text()
        checkout = text.split('uses: actions/checkout@', 1)[1].split('      - ', 1)[0]
        self.assertIn('fetch-depth: 0', checkout,
                      'proof-reachability tests consume historical Git objects')

    def test_workflow_covers_packet_dependencies_and_both_modes(self):
        self.load(); wf = ROOT / '.github/workflows/d3-l4-anisotropic.yml'
        self.assertTrue(wf.is_file())
        text = wf.read_text()
        for target in ('coefficients/d3_l4_anisotropic_20261005/**',
                       'coefficients/side24_v1/PROOF.md', 'coefficients/side24_v1/ENCLOSURE.json',
                       'imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md',
                       'reviews/iba1_periodic_jet_claude_20261005/periodic_jet_check.py',
                       'tests/test_d3_l4_replay.py', 'tools/d3_l4_replay.py',
                       "mode: [normal, optimized]", 'contents: read',
                       'persist-credentials: false', 'if: always()', '--mode "${{ matrix.mode }}"'):
            self.assertIn(target, text)
        self.assertNotIn('pull_request_target:', text)


class TimeoutEvidenceTests(unittest.TestCase):
    """Timeout telemetry only; mocked source gates below are orchestration fixtures."""
    def setUp(self):
        from unittest import mock
        self.mock = mock
        spec = importlib.util.spec_from_file_location('timeout_subject', DRIVER)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def invoke_timeout(self, logs, *, out=b'partial\xff\x00', err=b'error\xfe', cwd='relative-cwd'):
        m = self.m
        argv = [sys.executable, '-B', '-O', '-S', 'synthetic-child.py']
        expiry = subprocess.TimeoutExpired(argv, 7, output=out, stderr=err)
        with self.mock.patch.object(m.subprocess, 'run', side_effect=expiry):
            with self.assertRaisesRegex(m.ReplayError, '^probe: timeout$') as caught:
                m.run_step(argv, cwd, logs, 'probe', b'', 'exact', timeout=7)
        self.assertIs(caught.exception.__cause__, expiry)
        return caught.exception, argv

    def read_record(self, logs):
        path = logs / 'probe.process.json'
        self.assertTrue(path.is_file(), 'timeout must retain per-step process metadata')
        return json.loads(path.read_text())

    def test_real_child_timeout_has_partial_bytes_and_process_record(self):
        m = self.m
        with tempfile.TemporaryDirectory() as t:
            logs = Path(t)
            argv = [sys.executable, '-B', '-S', '-c',
                    'import os,time; os.write(1,b"out\\xff\\x00"); '
                    'os.write(2,b"err\\xfe"); time.sleep(5)']
            with self.assertRaisesRegex(m.ReplayError, '^probe: timeout$') as caught:
                m.run_step(argv, logs, logs, 'probe', b'', 'exact', timeout=1)
            self.assertIsInstance(caught.exception.__cause__, subprocess.TimeoutExpired)
            record = self.read_record(logs)
            self.assertEqual((logs/'probe.stdout').read_bytes(), b'out\xff\x00')
            self.assertEqual((logs/'probe.stderr').read_bytes(), b'err\xfe')
            self.assertEqual(record['command'], argv)
            self.assertEqual(record['cwd'], str(logs))
            self.assertEqual(record['timeout_seconds'], 1)
            self.assertEqual(record['status'], 'TIMEOUT')
            self.assertIsNone(record['returncode'])
            self.assertGreaterEqual(record['elapsed_seconds'], 0)
            self.assertEqual(record['evidence_errors'], {})

    def test_partial_binary_hashes_and_exact_relative_cwd(self):
        with tempfile.TemporaryDirectory() as t:
            logs = Path(t); failure, argv = self.invoke_timeout(logs)
            record = self.read_record(logs)
            self.assertEqual(record['command'], argv)
            self.assertEqual(record['cwd'], 'relative-cwd')
            self.assertEqual(record['name'], 'probe')
            self.assertEqual(record['stdout_sha256'], hashlib.sha256(b'partial\xff\x00').hexdigest())
            self.assertEqual(record['stderr_sha256'], hashlib.sha256(b'error\xfe').hexdigest())
            self.assertIs(record['stdout_available'], True)
            self.assertIs(record['stdout_saved'], True)
            self.assertEqual(failure.timeout_record, record)

    def test_unavailable_and_empty_streams_are_distinct(self):
        for out, err in ((None, b''), (b'', None), (None, None)):
            with self.subTest(out=out, err=err), tempfile.TemporaryDirectory() as t:
                logs = Path(t); self.invoke_timeout(logs, out=out, err=err)
                record = self.read_record(logs)
                for key, value in (('stdout', out), ('stderr', err)):
                    self.assertEqual((logs/('probe.'+key)).read_bytes(), b'')
                    self.assertIs(record[key+'_available'], value is not None)
                    self.assertEqual(record[key+'_sha256'], None if value is None
                                     else hashlib.sha256(value).hexdigest())
                    self.assertEqual(record[key+'_bytes'], None if value is None else len(value))

    def test_each_stream_write_failure_keeps_other_stream_and_timeout(self):
        original = Path.write_bytes
        for stream in ('stdout', 'stderr'):
            with self.subTest(stream=stream), tempfile.TemporaryDirectory() as t:
                logs = Path(t)
                def writer(path, data):
                    if path.name == 'probe.'+stream: raise OSError('synthetic stream failure')
                    return original(path, data)
                with self.mock.patch.object(Path, 'write_bytes', writer):
                    self.invoke_timeout(logs)
                record = self.read_record(logs)
                self.assertIs(record[stream+'_saved'], False)
                self.assertIn(stream, record['evidence_errors'])
                other = 'stderr' if stream == 'stdout' else 'stdout'
                self.assertTrue((logs/('probe.'+other)).is_file())
                self.assertIs(record[other+'_saved'], True)

    def test_process_record_write_failure_does_not_mask_timeout(self):
        original = Path.write_text
        with tempfile.TemporaryDirectory() as t:
            logs = Path(t)
            def writer(path, data, *args, **kwargs):
                if path.name == 'probe.process.json': raise OSError('synthetic metadata failure')
                return original(path, data, *args, **kwargs)
            with self.mock.patch.object(Path, 'write_text', writer):
                failure, _ = self.invoke_timeout(logs)
            self.assertIn('process_metadata', failure.timeout_record['evidence_errors'])
            self.assertFalse((logs/'probe.process.json').exists())
            self.assertTrue((logs/'probe.stdout').exists())
            self.assertTrue((logs/'probe.stderr').exists())

    def test_all_evidence_writes_failing_still_preserves_timeout(self):
        with tempfile.TemporaryDirectory() as t:
            with self.mock.patch.object(Path, 'write_bytes', side_effect=OSError('disk')), \
                 self.mock.patch.object(Path, 'write_text', side_effect=OSError('disk')):
                failure, _ = self.invoke_timeout(Path(t))
            self.assertEqual(set(failure.timeout_record['evidence_errors']),
                             {'stdout', 'stderr', 'process_metadata'})

    def test_timeout_elapsed_clock_failure_is_secondary(self):
        for finish in (RuntimeError('clock'), float('nan'), float('inf'), 5.0):
            with self.subTest(finish=finish), tempfile.TemporaryDirectory() as t:
                logs = Path(t)
                with self.mock.patch.object(self.m.time, 'monotonic', side_effect=[10.0, finish]):
                    self.invoke_timeout(logs)
                record = self.read_record(logs)
                self.assertIsNone(record['elapsed_seconds'])
                self.assertIn('elapsed_seconds', record['evidence_errors'])

    def test_completed_success_record_shape_is_unchanged(self):
        with tempfile.TemporaryDirectory() as t:
            logs = Path(t); argv = [sys.executable, '-B', '-S', '-c', 'print("ok")']
            record = self.m.run_step(argv, logs, logs, 'complete', b'ok\n', 'exact')
            self.assertEqual(set(record), {'command', 'returncode', 'elapsed_seconds',
                                          'stdout_sha256', 'stderr_sha256'})
            self.assertEqual(record['returncode'], 0)
            self.assertEqual(record, json.loads((logs/'complete.process.json').read_text()))

    def test_completed_failure_is_not_timeout(self):
        for script, code in (('raise SystemExit(1)', 'unexpected_exit'),
                             ('print("wrong")', 'stdout_mismatch')):
            with self.subTest(code=code), tempfile.TemporaryDirectory() as t:
                logs = Path(t)
                with self.assertRaisesRegex(self.m.ReplayError, code) as caught:
                    self.m.run_step([sys.executable, '-B', '-S', '-c', script],
                                    logs, logs, 'complete', b'ok\n', 'exact')
                self.assertFalse(hasattr(caught.exception, 'timeout_record'))
                self.assertNotIn('status', json.loads((logs/'complete.process.json').read_text()))

    def test_non_timeout_oserror_propagates_without_timeout_artifact(self):
        failure = FileNotFoundError('synthetic missing executable')
        with tempfile.TemporaryDirectory() as t:
            logs = Path(t)
            with self.mock.patch.object(self.m.subprocess, 'run', side_effect=failure):
                with self.assertRaises(FileNotFoundError) as caught:
                    self.m.run_step(['missing'], logs, logs, 'probe', b'', 'exact')
            self.assertIs(caught.exception, failure)
            self.assertFalse((logs/'probe.process.json').exists())

    def drive_main(self, root, *, fail_receipt=False, fail_step_metadata=False, timeout=True):
        """Synthetic source/HEAD setup isolates orchestration, not scientific validation."""
        from contextlib import ExitStack
        m = self.m; logs = root/'evidence'; packet = root/m.PACKET
        packet.mkdir(parents=True)
        for name in ('RESULTS.json', 'REFERENCE.json', 'CROSSCHECKS.json'):
            (packet/name).write_bytes(b'{}')
        events = []
        def process(argv, **kwargs):
            events.append(argv)
            if argv == ['git', 'rev-parse', 'HEAD']:
                return subprocess.CompletedProcess(argv, 0, 'a'*40+'\n', '')
            raise subprocess.TimeoutExpired(argv, 900, output=b'partial', stderr=b'')
        original = Path.write_text
        def writer(path, data, *args, **kwargs):
            if fail_receipt and path.name == 'receipt.json': raise OSError('receipt unavailable')
            if fail_step_metadata and path.name.endswith('.process.json'): raise OSError('step unavailable')
            return original(path, data, *args, **kwargs)
        with ExitStack() as stack:
            stack.enter_context(self.mock.patch.object(m.sys, 'argv', ['replay', '--mode', 'normal',
                         '--root', str(root), '--output', str(logs)]))
            stack.enter_context(self.mock.patch.object(m, '__file__', str(root/'tools/d3_l4_replay.py')))
            stack.enter_context(self.mock.patch.object(m, 'validate_snapshot', return_value={}))
            stack.enter_context(self.mock.patch.object(m, 'execution_identities', return_value={}))
            stack.enter_context(self.mock.patch.dict(m.os.environ, {'GITHUB_ACTIONS': 'false'}))
            stack.enter_context(self.mock.patch.object(m.subprocess, 'run', side_effect=process))
            stack.enter_context(self.mock.patch.object(Path, 'write_text', writer))
            if not timeout: stack.enter_context(self.mock.patch.object(m, 'run_step', return_value={}))
            if timeout:
                with self.assertRaisesRegex(m.ReplayError, '^tests: timeout$') as caught:
                    m.main()
                self.assertIsInstance(caught.exception.__cause__, subprocess.TimeoutExpired)
                return logs, events, caught.exception
            with self.assertRaisesRegex(OSError, 'receipt unavailable'):
                m.main()
            return logs, events, None

    def test_main_timeout_receipt_and_no_later_step(self):
        with tempfile.TemporaryDirectory() as t:
            logs, events, failure = self.drive_main(Path(t))
            receipt = json.loads((logs/'receipt.json').read_text())
            self.assertEqual(receipt['status'], 'FAIL')
            self.assertEqual(receipt['steps'], {})
            self.assertEqual(receipt['failed_step'], failure.timeout_record)
            self.assertIs(receipt['scientific_acceptance'], False)
            self.assertEqual(len(events), 2)
            self.assertIn('unittest', events[1])

    def test_main_receipt_retains_timeout_when_process_record_missing(self):
        with tempfile.TemporaryDirectory() as t:
            logs, _, failure = self.drive_main(Path(t), fail_step_metadata=True)
            receipt = json.loads((logs/'receipt.json').read_text())
            self.assertEqual(receipt['failed_step'], failure.timeout_record)
            self.assertIn('process_metadata', receipt['failed_step']['evidence_errors'])
            self.assertFalse((logs/'tests.process.json').exists())

    def test_main_receipt_write_failure_is_secondary_to_timeout(self):
        with tempfile.TemporaryDirectory() as t:
            logs, _, failure = self.drive_main(Path(t), fail_receipt=True)
            self.assertFalse((logs/'receipt.json').exists())
            self.assertTrue((logs/'tests.process.json').exists())
            self.assertTrue(any('receipt' in note for note in failure.__notes__))

    def test_success_without_receipt_is_still_failure(self):
        with tempfile.TemporaryDirectory() as t:
            self.drive_main(Path(t), fail_receipt=True, timeout=False)


if __name__ == '__main__': unittest.main()
