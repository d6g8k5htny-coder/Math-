"""Proposed control (W8c): context() must allow only the two pinned execution
repositories and refuse anything else with the handled refusal.

Positive: d6g8k5htny-coder/main and d6g8k5htny-coder/Math- are accepted
(exit 0, conclusion success, empty stderr), so a reject-everything stub fails.
Negative: the exact refusal — exit 1, stderr
'REQUIRED_FORMAL_CHECK_FAILED: unexpected execution repository', empty stdout.
Needs outputs are aligned with the env value, so a later equality check cannot
substitute for the allowlist. Offline: no network. Drives the job command
`python3 -B -S tools/required_formal_check.py aggregate`.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'required_formal_check.py'
REFUSAL = 'REQUIRED_FORMAL_CHECK_FAILED: unexpected execution repository\n'


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
        [sys.executable, '-B', *(['-O'] if sys.flags.optimize else []), '-S', str(SCRIPT), 'aggregate'],
        cwd=ROOT, env=full, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


import unittest


class RepositoryAllowlistControl(unittest.TestCase):
    def assert_accepted(self, code, out, err, repo):
        self.assertEqual((code, err), (0, ''))
        self.assertIn('"conclusion": "success"', out)
        self.assertIn('"repository": "%s"' % repo, out)

    def assert_refused(self, code, out, err):
        self.assertEqual(code, 1)
        self.assertEqual(err, REFUSAL)
        self.assertEqual(out, '')

    def test_main_repository_accepted(self):
        self.assert_accepted(*run_cli(base(GITHUB_REPOSITORY='d6g8k5htny-coder/main')),
                             'd6g8k5htny-coder/main')

    def test_math_repository_accepted(self):
        self.assert_accepted(*run_cli(base(GITHUB_REPOSITORY='d6g8k5htny-coder/Math-')),
                             'd6g8k5htny-coder/Math-')

    def test_unpinned_repository_refused(self):
        # Aligned on both sides: only the allowlist can refuse this string.
        self.assert_refused(*run_cli(base(GITHUB_REPOSITORY='d6g8k5htny-coder/other')))

    def test_empty_repository_refused(self):
        self.assert_refused(*run_cli(base(GITHUB_REPOSITORY='')))


if __name__ == '__main__':
    unittest.main()
