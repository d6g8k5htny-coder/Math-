"""Real-subprocess protocol tests for the certified-d2 workflow's embedded driver.

This executes the exact embedded driver, with an explicitly synthetic checker
and a complete hash-consistent fixture manifest. It does not replay coefficient
arithmetic or change a repository file. Select a candidate with WORKFLOW_UNDER_TEST.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = Path(os.environ.get('WORKFLOW_UNDER_TEST', ROOT / '.github/workflows/side24-d2-certified.yml'))

FIXTURE = r'''import json, os, sys
mode = os.environ['FIXTURE_BEHAVIOR']
expected = {'M1': 'C4_strip_and_error_bound_L4',
            'M2': 'C1_reference_equals_side24_closed_form',
            'M3': 'C6_matches_iba1_diagnostic_L4',
            'M4': 'C9_coarse_rule_consistent_L4'}
if len(sys.argv) == 1:
    if mode == 'baseline_bad':
        print('not the expected baseline'); sys.exit(0)
    print('{"fixture": true}')
    if mode == 'baseline_stderr':
        print('unexpected baseline diagnostic', file=sys.stderr)
    sys.exit(0)
label = sys.argv[2]
if label == 'M9':
    if mode == 'unknown_whitespace':
        print(' unknown mutant ')
    else:
        print('other argparse problem' if mode == 'unknown_wrong' else 'unknown mutant')
    sys.exit(2)
if mode == 'crash':
    raise RuntimeError('synthetic mutant-only runtime failure, not a mathematical rejection')
if mode == 'empty':
    sys.exit(1)
if mode == 'invalid_json':
    print('not json'); sys.exit(1)
payload = {'mutant': label, 'failed_check': expected[label]}
if mode == 'wrong_label':
    payload['mutant'] = 'M0'
if mode == 'wrong_check':
    payload['failed_check'] = 'C3_unrelated_input_corruption'
if mode == 'extra_field':
    payload['unverified'] = True
if mode == 'wrong_type':
    payload = [payload]
if mode == 'duplicate_key':
    print('{"mutant":"M0","mutant":' + json.dumps(label) + ',"failed_check":' + json.dumps(expected[label]) + '}')
else:
    print(json.dumps(payload, sort_keys=True))
if mode == 'stderr':
    print('synthetic traceback after expected JSON', file=sys.stderr)
if mode == 'trailing_text':
    print('unrelated trailing output')
sys.exit(0 if mode == 'wrong_exit' else 1)
'''


def embedded_driver(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    marker = "          python -B -S - <<'PY'\n"
    if text.count(marker) != 1:
        raise ValueError('expected exactly one workflow driver')
    tail = text.split(marker, 1)[1]
    return textwrap.dedent(tail.split('          PY\n', 1)[0])


def run_fixture(behavior: str, flags: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory(prefix='pr302-protocol-') as tmp:
        base = Path(tmp)
        packet = base / 'reviews/side24_d2_certified_small_L_claude_20261005'
        packet.mkdir(parents=True)
        (packet / 'certified_d2.py').write_text(FIXTURE, encoding='utf-8')
        (packet / 'RESULTS.json').write_bytes(b'{"fixture": true}\n')
        records = []
        for name in ('certified_d2.py', 'RESULTS.json'):
            data = (packet / name).read_bytes()
            records.append({'path': name, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest(),
                            'git_blob': hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()})
        (packet / 'SOURCE_FILES.json').write_text(json.dumps({'files': records, 'pins_on_main': []}))
        if behavior == 'bad_manifest':
            (packet / 'RESULTS.json').write_bytes(b'altered after manifest binding\n')
        env = dict(os.environ, FLAGS=flags, FIXTURE_BEHAVIOR=behavior)
        return subprocess.run([sys.executable, '-B', '-S', '-c', embedded_driver(WORKFLOW)],
                              cwd=base, env=env, text=True, capture_output=True, timeout=20)


class WorkflowProtocol(unittest.TestCase):
    def assert_disposition(self, behavior: str, succeeds: bool = False) -> None:
        for flags in ('-B -S', '-B -O -S'):
            with self.subTest(flags=flags, behavior=behavior):
                result = run_fixture(behavior, flags)
                if succeeds:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('mutants PASS', result.stdout)
                else:
                    self.assertNotEqual(result.returncode, 0,
                                        f'{behavior} was incorrectly accepted: {result.stdout}')
                    self.assertNotIn('mutants PASS', result.stdout)

    def test_workflow_triggers_on_protocol_test_changes(self):
        self.assertIn("      - 'tests/test_certified_d2_workflow.py'", WORKFLOW.read_text())

    def test_workflow_executes_protocol_regressions(self):
        self.assertIn("python ${{ matrix.flags }} -m unittest discover -s tests -p test_certified_d2_workflow.py -v",
                      WORKFLOW.read_text())

    def test_intended_failures_are_accepted(self):
        self.assert_disposition('valid', True)

    def test_runtime_crash_is_not_mathematical_rejection(self):
        self.assert_disposition('crash')

    def test_empty_exit_one_is_rejected(self):
        self.assert_disposition('empty')

    def test_non_json_exit_one_is_rejected(self):
        self.assert_disposition('invalid_json')

    def test_wrong_mutant_identity_is_rejected(self):
        self.assert_disposition('wrong_label')

    def test_unrelated_failure_check_is_rejected(self):
        self.assert_disposition('wrong_check')

    def test_ambiguous_duplicate_keys_are_rejected(self):
        self.assert_disposition('duplicate_key')

    def test_wrong_payload_type_is_rejected(self):
        self.assert_disposition('wrong_type')

    def test_unexpected_payload_fields_are_rejected(self):
        self.assert_disposition('extra_field')

    def test_stderr_failure_is_rejected(self):
        self.assert_disposition('stderr')

    def test_trailing_non_json_text_is_rejected(self):
        self.assert_disposition('trailing_text')

    def test_unknown_label_requires_correct_diagnostic(self):
        self.assert_disposition('unknown_wrong')

    def test_wrong_exit_code_is_rejected(self):
        self.assert_disposition('wrong_exit')

    def test_baseline_output_mismatch_stays_rejected(self):
        self.assert_disposition('baseline_bad')

    def test_baseline_stderr_stays_rejected(self):
        self.assert_disposition('baseline_stderr')

    def test_unknown_label_whitespace_stays_rejected(self):
        self.assert_disposition('unknown_whitespace')

    def test_manifest_mismatch_stays_rejected(self):
        self.assert_disposition('bad_manifest')


if __name__ == '__main__':
    unittest.main(verbosity=2)
