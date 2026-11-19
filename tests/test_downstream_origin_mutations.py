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
        with mock.patch.object(M, 'CASES', (M.CASES[0],) * 4):
            with mock.patch.object(M, 'verified_helper', return_value=origin):
                with mock.patch.object(M.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '', '')) as run:
                    with self.assertRaisesRegex(ValueError, 'case inventory'):
                        M.run(output)
                    run.assert_not_called()
        self.assertEqual(json.loads((output / 'results.json').read_text()), [])

    def test_failed_classification_is_refused_and_reported(self):
        output = self.out / 'failed'
        response = subprocess.CompletedProcess(['synthetic'], 0, '', '')
        origin = mock.Mock()
        origin.classify.return_value = {'control_pass': False, 'killed': False, 'collected': 0}
        with mock.patch.object(M, 'verified_helper', return_value=origin):
            with mock.patch.object(M.subprocess, 'run', return_value=response):
                try:
                    M.run(output)
                except Exception as exc:
                    self.assertIsInstance(exc, RuntimeError)
                    self.assertIn('self-mutation failed', str(exc))
                else:
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


if __name__ == '__main__':
    unittest.main()
