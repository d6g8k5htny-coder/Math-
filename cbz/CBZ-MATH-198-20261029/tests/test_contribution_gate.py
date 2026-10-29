"""Campaign reporting must preserve real failures and refuse empty green runs."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1]/'tools/contribution_gate.py'

class GateTests(unittest.TestCase):
    def test_cli_exists_and_documents_local_scope(self):
        result = subprocess.run([sys.executable, '-B', str(TOOL), '--help'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('contribution', result.stdout)

    def module(self):
        spec = importlib.util.spec_from_file_location('contribution_gate', TOOL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_failed_child_is_retained_and_prevents_local_pass(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'out'
            result = m.execute_jobs([{'id':'failure','argv':[sys.executable,'-c','raise SystemExit(7)'], 'cwd':tmp}], out, {})
            self.assertEqual(result['status'], 'FAILED')
            self.assertFalse(result['cbz_zero'])
            self.assertEqual(result['records'][0]['returncode'], 7)
            self.assertTrue((out/'failure/receipt.json').is_file())
            self.assertEqual(json.loads((out/'results.json').read_text())['status'], 'FAILED')

    def test_success_requires_observed_child_and_retains_streams(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'out'
            result = m.execute_jobs([{'id':'real','argv':[sys.executable,'-c','print("observed")'], 'cwd':tmp}], out, {})
            self.assertEqual(result['status'], 'LOCAL_CONTRIBUTION_PASS')
            self.assertFalse(result['cbz_zero'])
            self.assertEqual((out/'real/stdout.txt').read_text(), 'observed\n')
            with self.assertRaises(FileExistsError):
                m.execute_jobs([{'id':'x','argv':[sys.executable,'-c','pass'], 'cwd':tmp}], out, {})

    def test_empty_and_duplicate_plans_reject(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            for jobs in ([], [{'id':'x','argv':['x'],'cwd':tmp}]*2):
                with self.assertRaises(ValueError):
                    m.execute_jobs(jobs, Path(tmp)/'out', {})

    def test_frozen_source_drift_rejects_real_success(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp)/'source.txt'; source.write_text('before')
            frozen = {str(source):m.sha(source)}
            argv = [sys.executable,'-c','from pathlib import Path; import sys; Path(sys.argv[1]).write_text("after")',str(source)]
            result = m.execute_jobs([{'id':'drift','argv':argv,'cwd':tmp}], Path(tmp)/'out', frozen)
            self.assertEqual(result['status'], 'FAILED')
            self.assertEqual(result['failure'], 'SOURCE_DRIFT')

    def test_umbrella_mathlib_is_explicit_external_and_missing_owned_import_rejects(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); source=root/'source'; (source/'formal').mkdir(parents=True)
            file=source/'formal'/'Example.lean'; file.write_text('import Mathlib\ntheorem example : True := True.intro\n')
            out=root/'out'; out.mkdir()
            manifest=m.prepare_scan(source,out)
            self.assertIn('Mathlib',manifest['external_imports'])
            file.write_text('import General.Missing\n')
            with self.assertRaisesRegex(ValueError,'unresolved project import'):
                m.prepare_scan(source,out)

    def test_timeout_kills_and_records_child(self):
        m = self.module()
        with tempfile.TemporaryDirectory() as tmp:
            result = m.execute_jobs([{'id':'timeout','argv':[sys.executable,'-c','import time; time.sleep(20)'], 'cwd':tmp,'timeout':0.1}], Path(tmp)/'out', {})
            self.assertEqual(result['status'], 'FAILED')
            self.assertTrue(result['records'][0]['timed_out'])

if __name__ == '__main__': unittest.main()
