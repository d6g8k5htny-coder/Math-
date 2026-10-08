"""Proposed control (W8c): workflow run_id must match [1-9][0-9]* (no zero,
no leading zero, digits only). Those predicates are isolated.

Positive: '123' and '7' are accepted (exit 0, that run_id reported, empty
stderr). Negative: exit 1, stderr exactly
'REQUIRED_FORMAL_CHECK_FAILED: invalid run ID', empty stdout.
Formal outputs run_id is aligned with GITHUB_RUN_ID, so the later equality
check cannot substitute for exact(). Offline: no network. Drives
`python3 -B -S tools/required_formal_check.py aggregate`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'required_formal_check.py'
REFUSAL = 'REQUIRED_FORMAL_CHECK_FAILED: invalid run ID\n'


def base(**over):
    env = {
        'GITHUB_SHA': '9fd261135b41daf1e377f9ef2db193fee6ec36be',
        'GITHUB_REPOSITORY': 'd6g8k5htny-coder/Math-',
        'GITHUB_RUN_ID': '123',
        'GITHUB_RUN_ATTEMPT': '2',
    }
    env.update(over)
    return env


def needs_for(env):
    sha, repo, run, attempt = (env['GITHUB_SHA'], env['GITHUB_REPOSITORY'],
                               env['GITHUB_RUN_ID'], env['GITHUB_RUN_ATTEMPT'])
    return {
        'checks': {'result': 'success', 'outputs': {'checked_commit': sha}},
        'formal': {'result': 'success', 'outputs': {
            'checked_commit': sha, 'repository': repo, 'run_id': run,
            'run_attempt': attempt, 'receipt_sha256': 'b' * 64,
        }},
    }


def run_cli(env):
    full = os.environ.copy()
    full.pop('REQUIRED_FORMAL_NEEDS', None)
    full.update(env)
    full['REQUIRED_FORMAL_NEEDS'] = json.dumps(needs_for(env))
    proc = subprocess.run(
        [sys.executable, '-B', '-S', str(SCRIPT), 'aggregate'],
        cwd=ROOT, env=full, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


class RunIdBindingControl(unittest.TestCase):
    def assert_accepted(self, code, out, err, run_id):
        self.assertEqual((code, err), (0, ''))
        self.assertIn('"conclusion": "success"', out)
        self.assertIn('"run_id": "%s"' % run_id, out)

    def assert_refused(self, code, out, err):
        self.assertEqual(code, 1)
        self.assertEqual(err, REFUSAL)
        self.assertEqual(out, '')

    def test_multidigit_run_id_accepted(self):
        self.assert_accepted(*run_cli(base(GITHUB_RUN_ID='123')), '123')

    def test_single_nonzero_digit_accepted(self):
        self.assert_accepted(*run_cli(base(GITHUB_RUN_ID='7')), '7')

    def test_zero_run_id_refused(self):
        self.assert_refused(*run_cli(base(GITHUB_RUN_ID='0')))

    def test_leading_zero_run_id_refused(self):
        # Digits only, but a leading zero. The bare-zero alternative does not match.
        self.assert_refused(*run_cli(base(GITHUB_RUN_ID='01')))

    def test_nonnumeric_run_id_refused(self):
        self.assert_refused(*run_cli(base(GITHUB_RUN_ID='12a')))

    def test_empty_run_id_refused(self):
        self.assert_refused(*run_cli(base(GITHUB_RUN_ID='')))


if __name__ == '__main__':
    unittest.main()
