"""Evidence-directory tests of the lifetime note DD replay wrapper (QS_REPLAY_EVIDENCE_DIR); fixtures are not mathematical evidence."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'frontiers/lifetime_dd_model_d_20261013/replay.py'


def load():
    spec = importlib.util.spec_from_file_location('dd_replay_evidence_subject', WRAPPER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.m = load()
        self.tmp = Path(tempfile.mkdtemp(prefix='dd-evidence-'))
        self.script = self.tmp / 'child' / 'script.py'
        self.script.parent.mkdir()
        self.script.write_text("import sys\nsys.stdout.write('out\\n')\nsys.stderr.write('')\nsys.exit(0)\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_no_evidence_without_env(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop('QS_REPLAY_EVIDENCE_DIR', None)
            self.assertIsNone(self.m.evidence_directory(self.script))
            code, out, err = self.m.run(self.script)
        self.assertEqual((code, out, err), (0, b'out\n', b''))

    def test_empty_env_rejected(self):
        with mock.patch.dict(os.environ, {'QS_REPLAY_EVIDENCE_DIR': ''}):
            with self.assertRaises(ValueError):
                self.m.evidence_directory(self.script)

    def test_evidence_inside_child_directory_rejected(self):
        with mock.patch.dict(os.environ, {'QS_REPLAY_EVIDENCE_DIR': str(self.script.parent / 'ev')}):
            with self.assertRaises(ValueError):
                self.m.evidence_directory(self.script)

    def test_evidence_inside_checkout_rejected(self):
        with mock.patch.dict(os.environ, {'QS_REPLAY_EVIDENCE_DIR': str(ROOT / 'ev')}):
            with self.assertRaises(ValueError):
                self.m.evidence_directory(self.script)

    def test_records_written_outside(self):
        ev = self.tmp / 'evidence'
        with mock.patch.dict(os.environ, {'QS_REPLAY_EVIDENCE_DIR': str(ev)}):
            code, out, err = self.m.run(self.script)
        self.assertEqual(code, 0)
        folders = [p for p in ev.iterdir() if p.is_dir()]
        self.assertEqual(len(folders), 1)
        rec = json.loads((folders[0] / 'process.json').read_text())
        self.assertEqual(rec['returncode'], 0)
        self.assertEqual(rec['scientific_effect'], 'NONE')
        self.assertEqual(rec['stdout']['sha256'], hashlib.sha256(b'out\n').hexdigest())
        self.assertEqual((folders[0] / 'stdout.bin').read_bytes(), b'out\n')
        self.assertEqual((folders[0] / 'stderr.bin').read_bytes(), b'')
        self.assertTrue(rec['command'][0] == sys.executable and rec['command'][1] == '-B')

    def test_each_invocation_gets_its_own_folder(self):
        ev = self.tmp / 'evidence'
        with mock.patch.dict(os.environ, {'QS_REPLAY_EVIDENCE_DIR': str(ev)}):
            self.m.run(self.script)
            self.m.run(self.script)
        self.assertEqual(len([p for p in ev.iterdir() if p.is_dir()]), 2)

    def test_timeout_is_an_exception(self):
        self.script.write_text("import time\ntime.sleep(5)\n")
        with mock.patch.object(self.m, 'PROCESS_TIMEOUT_SECONDS', 1):
            with self.assertRaises(self.m.subprocess.TimeoutExpired):
                self.m.run(self.script)

    def test_timeout_evidence_is_retained(self):
        self.script.write_text("import sys, time\nsys.stdout.write('partial\\n')\nsys.stdout.flush()\ntime.sleep(5)\n")
        ev = self.tmp / 'evidence'
        with mock.patch.dict(os.environ, {'QS_REPLAY_EVIDENCE_DIR': str(ev)}):
            with mock.patch.object(self.m, 'PROCESS_TIMEOUT_SECONDS', 1):
                with self.assertRaises(self.m.subprocess.TimeoutExpired):
                    self.m.run(self.script)
        folders = [p for p in ev.iterdir() if p.is_dir()]
        self.assertEqual(len(folders), 1)
        rec = json.loads((folders[0] / 'process.json').read_text())
        self.assertEqual(rec['status'], 'timeout')
        self.assertIsNone(rec['returncode'])
        self.assertEqual((folders[0] / 'stdout.bin').read_bytes(), b'partial\n')

    def test_report_is_one_json_line(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.m.report('x', (0, b'a', b''), 'why')
        rec = json.loads(buf.getvalue())
        self.assertEqual(rec['replay'], 'x')
        self.assertEqual(rec['stdout_sha256'], hashlib.sha256(b'a').hexdigest())


if __name__ == '__main__':
    unittest.main()
