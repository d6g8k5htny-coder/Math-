"""Optional raw-process evidence; synthetic children are not mathematical evidence."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'frontiers/ts_small_kappa_20261006'
ENV = 'QS_REPLAY_EVIDENCE_DIR'


class RawEvidenceTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('qs_raw_subject', PACKET / 'replay.py')
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        scripts = self.root / 'scripts'
        scripts.mkdir()
        self.script = scripts / 'fixture.py'
        self.evidence = self.root / 'evidence'
        self.env = patch.dict(os.environ, {ENV: str(self.evidence)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def child(self, text):
        self.script.write_text(text, encoding='utf-8')
        return self.script

    def record(self):
        records = list(self.evidence.glob('invocation-*/process.json'))
        self.assertEqual(len(records), 1, 'one independently retained child process record required')
        return records[0].parent, json.loads(records[0].read_bytes())

    def verify_stream(self, folder, rec, name, value):
        stream = rec['streams'][name]
        self.assertEqual(stream['available'], value is not None)
        self.assertEqual(stream['bytes'], len(value) if value is not None else None)
        self.assertEqual(stream['sha256'], hashlib.sha256(value).hexdigest() if value is not None else None)
        self.assertTrue(stream['saved'])
        self.assertEqual((folder / (name + '.bin')).read_bytes(), value if value is not None else b'')

    def test_no_capture_preserves_original_three_value_result(self):
        os.environ.pop(ENV)
        s = self.child("import os,sys\nos.write(1,b'\\xffok');os.write(2,b'\\x00err');sys.exit(7)\n")
        self.assertEqual(self.m.run(s), (7, b'\xffok', b'\x00err'))
        self.assertFalse(self.evidence.exists())

    def test_real_crash_retains_full_binary_streams_and_invocation(self):
        s = self.child("import os\nos.write(1,b'\\x00\\xffpartial')\nraise RuntimeError('synthetic crash')\n")
        result = self.m.run(s, '--diagnostic')
        self.assertEqual(result[0], 1)
        self.assertIn(b'RuntimeError: synthetic crash', result[2])
        folder, rec = self.record()
        self.assertEqual(rec['command'], [sys.executable, *self.m.interpreter_flags(), str(s), '--diagnostic'])
        self.assertEqual(rec['cwd'], str(s.parent))
        self.assertEqual(rec['timeout_seconds'], 1800)
        self.assertEqual(rec['status'], 'completed')
        self.assertEqual(rec['returncode'], 1)
        self.assertNotIn('passed', rec)
        self.assertEqual(rec['evidence_errors'], [])
        self.verify_stream(folder, rec, 'stdout', result[1])
        self.verify_stream(folder, rec, 'stderr', result[2])

    def test_success_and_intended_failure_outputs_are_not_reinterpreted(self):
        s = self.child("import os,sys\nos.write(1,b'answer\\n');os.write(2,b'diagnostic\\n');sys.exit(int(sys.argv[1]))\n")
        for code in (0, 1, 2):
            with self.subTest(code=code):
                result = self.m.run(s, str(code))
                self.assertEqual(result, (code, b'answer\n', b'diagnostic\n'))
        records = [json.loads(p.read_bytes()) for p in self.evidence.glob('invocation-*/process.json')]
        self.assertEqual(sorted(r['returncode'] for r in records), [0, 1, 2])
        self.assertTrue(all('passed' not in r for r in records))

    def test_repeated_invocations_never_overwrite(self):
        s = self.child("print('first')\n")
        self.m.run(s)
        before = {p: p.read_bytes() for p in self.evidence.glob('invocation-*/*')}
        self.assertEqual(len(before), 3)
        self.m.run(s)
        self.assertEqual(len(list(self.evidence.glob('invocation-*'))), 2)
        for p, data in before.items():
            self.assertEqual(p.read_bytes(), data)

    def test_real_timeout_keeps_partial_bytes_and_timeout_exception(self):
        self.assertTrue(hasattr(self.m, 'PROCESS_TIMEOUT_SECONDS'), 'explicit unchanged production timeout required')
        s = self.child("import os,time\nos.write(1,b'\\xffout');os.write(2,b'\\x00err');time.sleep(10)\n")
        with patch.object(self.m, 'PROCESS_TIMEOUT_SECONDS', 0.5):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                self.m.run(s)
        folder, rec = self.record()
        self.assertEqual(rec['status'], 'timeout')
        self.assertIsNone(rec['returncode'])
        self.assertEqual(rec['timeout_seconds'], 0.5)
        self.assertEqual(caught.exception.output, b'\xffout')
        self.assertEqual(caught.exception.stderr, b'\x00err')
        self.verify_stream(folder, rec, 'stdout', caught.exception.output)
        self.verify_stream(folder, rec, 'stderr', caught.exception.stderr)
        self.assertEqual(caught.exception.evidence_record, rec)

    def test_unavailable_empty_and_binary_timeout_capture_are_distinct(self):
        for out in (None, b'', b'\xff\x00'):
            for err in (None, b'', b'\x80err'):
                with self.subTest(out=out, err=err), tempfile.TemporaryDirectory() as td:
                    target = Path(td) / 'records'
                    exc = subprocess.TimeoutExpired(['synthetic'], 1800, output=out, stderr=err)
                    with patch.dict(os.environ, {ENV: str(target)}), patch.object(self.m.subprocess, 'run', side_effect=exc):
                        with self.assertRaises(subprocess.TimeoutExpired) as caught:
                            self.m.run(self.script)
                    self.assertIs(caught.exception, exc)
                    paths = list(target.glob('invocation-*/process.json'))
                    self.assertEqual(len(paths), 1)
                    rec = json.loads(paths[0].read_bytes())
                    self.verify_stream(paths[0].parent, rec, 'stdout', out)
                    self.verify_stream(paths[0].parent, rec, 'stderr', err)
                    self.assertIsNone(rec['returncode'])

    def test_real_spawn_error_retains_unknown_output_and_original_error(self):
        s = self.child("print('must not execute')\n")
        missing = str(self.root / 'missing-interpreter')
        with patch.object(self.m.sys, 'executable', missing):
            with self.assertRaises(FileNotFoundError) as caught:
                self.m.run(s)
        folder, rec = self.record()
        self.assertEqual(rec['status'], 'spawn_error')
        self.assertIsNone(rec['returncode'])
        self.assertEqual(rec['exception']['type'], 'FileNotFoundError')
        self.verify_stream(folder, rec, 'stdout', None)
        self.verify_stream(folder, rec, 'stderr', None)
        self.assertEqual(caught.exception.evidence_record, rec)

    def test_each_write_failure_still_attempts_other_evidence(self):
        original = Path.write_bytes
        for failed in ('stdout.bin', 'stderr.bin', 'process.json'):
            with self.subTest(failed=failed), tempfile.TemporaryDirectory() as td:
                target = Path(td) / 'records'
                attempted = []
                def write(path, data):
                    attempted.append(path.name)
                    if path.name == failed:
                        raise OSError('synthetic write refusal')
                    return original(path, data)
                exc = subprocess.TimeoutExpired(['synthetic'], 1800, output=b'out', stderr=b'err')
                with patch.dict(os.environ, {ENV: str(target)}), patch.object(self.m.subprocess, 'run', side_effect=exc), patch.object(Path, 'write_bytes', write):
                    with self.assertRaises(subprocess.TimeoutExpired) as caught:
                        self.m.run(self.script)
                self.assertIs(caught.exception, exc)
                self.assertEqual(attempted, ['stdout.bin', 'stderr.bin', 'process.json'])
                rec = caught.exception.evidence_record
                self.assertEqual(len(rec['evidence_errors']), 1)
                self.assertIn(failed, rec['evidence_errors'][0])
                self.assertTrue(any('evidence' in note for note in caught.exception.__notes__))
                folder = next(target.glob('invocation-*'))
                for name in {'stdout.bin', 'stderr.bin', 'process.json'} - {failed}:
                    self.assertTrue((folder / name).is_file())

    def test_all_write_failures_do_not_replace_primary_timeout(self):
        exc = subprocess.TimeoutExpired(['synthetic'], 1800, output=b'out', stderr=b'err')
        with patch.object(self.m.subprocess, 'run', side_effect=exc), patch.object(Path, 'write_bytes', side_effect=OSError('synthetic full disk')):
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                self.m.run(self.script)
        self.assertIs(caught.exception, exc)
        self.assertTrue(hasattr(exc, 'evidence_record'), 'retain failure metadata in memory')
        self.assertEqual(len(exc.evidence_record['evidence_errors']), 3)
        self.assertIsNone(exc.evidence_record['returncode'])

    def test_completed_child_with_failed_evidence_cannot_report_success(self):
        self.child("print('actual completed child')\n")
        with patch.object(Path, 'write_bytes', side_effect=OSError('synthetic full disk')):
            with self.assertRaises(RuntimeError) as caught:
                self.m.run(self.script)
        self.assertEqual(caught.exception.evidence_record['returncode'], 0)
        self.assertEqual(len(caught.exception.evidence_record['evidence_errors']), 3)

    def test_invalid_destination_stops_before_child(self):
        for target in (PACKET / 'forbidden-evidence', self.script.parent / 'forbidden-evidence'):
            with self.subTest(target=target), patch.dict(os.environ, {ENV: str(target)}), patch.object(self.m.subprocess, 'run') as child:
                with self.assertRaises(ValueError):
                    self.m.run(self.script)
                child.assert_not_called()
                self.assertFalse(target.exists())
        self.evidence.write_text('not a directory')
        with patch.object(self.m.subprocess, 'run') as child:
            with self.assertRaises(OSError):
                self.m.run(self.script)
            child.assert_not_called()

    def test_failed_custody_creates_no_child_evidence(self):
        with patch.object(self.m, 'tree_failures', return_value=['synthetic custody refusal']), patch.object(self.m.subprocess, 'run') as child:
            self.assertEqual(self.m.main(), 1)
            child.assert_not_called()
        self.assertFalse(self.evidence.exists())

    def test_workflow_wires_tests_and_capture_outside_source_tree(self):
        text = (ROOT / '.github/workflows/ts-small-kappa.yml').read_text()
        self.assertIn("'tests/test_ts_small_kappa_replay_evidence.py'", text)
        self.assertIn('-p test_ts_small_kappa_replay_evidence.py', text)
        self.assertIn('QS_REPLAY_EVIDENCE_DIR="$out/children" python', text)
        self.assertIn('cp tests/test_ts_small_kappa_replay_evidence.py "$out/"', text)
        self.assertIn('set -euo pipefail', text)
        self.assertIn('git diff --exit-code', text)
        self.assertIn('contents: read', text)
        self.assertIn("python-version: '3.11.16'", text)


if __name__ == '__main__':
    unittest.main()
