"""An interrupted child must remain visible in the campaign, not only on disk."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('project_rebuild', ROOT/'rebuild.py')
rebuild = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rebuild)


class BuildAccountingTest(unittest.TestCase):
    def test_retained_interrupted_child_is_in_failed_campaign(self):
        def interrupted(command, output, **kwargs):
            output.mkdir()
            receipt = {'command':command, 'succeeded':False, 'returncode':-9,
                       'failure':{'type':'KeyboardInterrupt','message':''},
                       'wait4':{'user_seconds':0.125,'system_seconds':0.025,
                                'max_rss_kib':64},
                       'scope':'Synthetic failure-control receipt; no native process.'}
            (output/'receipt.json').write_text(json.dumps(receipt))
            raise RuntimeError('synthetic retained interruption')

        with tempfile.TemporaryDirectory() as work:
            root = Path(work)
            lean = root/'fixture-lean'; lean.write_bytes(b'not an executable; accounting fixture only')
            mathlib = root/'fixture-mathlib'; mathlib.mkdir()
            (mathlib/'lean-toolchain').write_text('leanprover/lean4:v4.34.1\n')
            with patch.object(rebuild, 'run_recorded', interrupted), \
                 patch.object(rebuild, 'LEAN_SHA', rebuild.sha(lean)), \
                 patch.object(rebuild.subprocess, 'check_output', return_value=rebuild.MATHLIB_COMMIT+'\n'):
                with self.assertRaisesRegex(RuntimeError, 'synthetic retained interruption'):
                    rebuild.run(
                        lean, mathlib,
                        root/'build', root/'evidence')
            result = json.loads((root/'evidence/results.json').read_text())
            self.assertEqual(result['status'], 'FAILED')
            self.assertEqual(len(result['records']), 1)
            record = result['records'][0]
            self.assertEqual(record['module'], result['order'][0])
            self.assertFalse(record['succeeded'])
            self.assertEqual(record['returncode'], -9)
            self.assertEqual(record['failure']['type'], 'KeyboardInterrupt')
            self.assertEqual(record['wait4']['user_seconds'], 0.125)
            self.assertEqual(record['wait4']['system_seconds'], 0.025)
            self.assertTrue((root/'evidence'/record['receipt']).is_file())


if __name__ == '__main__':
    unittest.main()
