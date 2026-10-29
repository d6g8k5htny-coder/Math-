import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parents[1]
TARGET = 'UniversalLaw.Spec.P15.FullTransformedPriceBudget'

class CatalogCliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, '-B', str(ROOT/'catalog.py'), *args],
                              cwd=ROOT, text=True, capture_output=True)
    def test_list_exposes_all_original_targets_and_never_training_credit(self):
        result = self.run_cli('list')
        self.assertEqual(result.returncode, 0, result.stderr)
        catalog = json.loads(result.stdout)
        self.assertEqual(len(catalog['endpoints']), 49)
        self.assertEqual(len({r['target'] for r in catalog['endpoints']}), 49)
        self.assertTrue(all(r['training_eligible'] is False for r in catalog['endpoints']))
        entry = next(r for r in catalog['endpoints'] if r['target'] == TARGET)
        self.assertEqual(entry['theorem'], 'UniversalLaw.P15Closure.fullTransformedPriceBudget')
        self.assertEqual(entry['proof_source'], 'formal/Closure/Assembly.lean')
    def test_export_rechecks_and_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'certificate.json'
            result = self.run_cli('export', TARGET, '--output', str(path))
            self.assertEqual(result.returncode, 0, result.stderr)
            value = json.loads(path.read_text())
            self.assertEqual(value['schema'], 'ul-saved-endpoint-evidence-v1')
            self.assertEqual(value['endpoint']['target'], TARGET)
            self.assertIs(value['endpoint']['training_eligible'], False)
            checked = self.run_cli('verify', '--certificate', str(path))
            self.assertEqual(checked.returncode, 0, checked.stderr)
            receipt = json.loads(checked.stdout)
            self.assertEqual(receipt['verification_kind'], 'saved_source_and_receipt_integrity')
            self.assertFalse(receipt['kernel_executed'])
            self.assertFalse(receipt['structural_worker_certificate'])
            overwritten = self.run_cli('export', TARGET, '--output', str(path))
            self.assertNotEqual(overwritten.returncode, 0)

if __name__ == '__main__': unittest.main()
