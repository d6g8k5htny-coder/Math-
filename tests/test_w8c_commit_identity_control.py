"""Proposed control (W8c): checked_commit must be a 40-character lowercase hex
string. Length, hex class, lowercase, and str-type are separate predicates.

Positive: a real 40-lowercase-hex commit is accepted (exit 0, that commit
reported, empty stderr). Negative: exit 1, stderr exactly
'REQUIRED_FORMAL_CHECK_FAILED: invalid commit', empty stdout.
Needs checked_commit is aligned with GITHUB_SHA, so a mismatch check cannot
substitute for exact(). The non-string case calls main() with an injected env
because a process environment cannot hold an int. Offline: no network.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'required_formal_check.py'
REFUSAL = 'REQUIRED_FORMAL_CHECK_FAILED: invalid commit\n'
SHA = '9fd261135b41daf1e377f9ef2db193fee6ec36be'
SPEC = importlib.util.spec_from_file_location('required_check_w8c_commit', SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def base(**over):
    env = {
        'GITHUB_SHA': SHA,
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


def run_main(env):
    payload = dict(env)
    payload['REQUIRED_FORMAL_NEEDS'] = json.dumps(needs_for(env))
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(M.os, 'environ', payload), \
         mock.patch.object(sys, 'argv', ['required_formal_check.py', 'aggregate']), \
         contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = M.main()
        except SystemExit as exc:
            code = exc.code
    return code, out.getvalue(), err.getvalue()


class CommitIdentityControl(unittest.TestCase):
    def assert_accepted(self, code, out, err, sha):
        self.assertEqual((code, err), (0, ''))
        self.assertIn('"conclusion": "success"', out)
        self.assertIn('"checked_commit": "%s"' % sha, out)

    def assert_refused(self, code, out, err):
        self.assertEqual(code, 1)
        self.assertEqual(err, REFUSAL)
        self.assertEqual(out, '')

    def test_lowercase_40_hex_accepted(self):
        self.assert_accepted(*run_cli(base()), SHA)

    def test_short_commit_refused(self):
        # 39 hex chars: only the length bound can refuse once outputs are aligned.
        self.assert_refused(*run_cli(base(GITHUB_SHA='a' * 39)))

    def test_long_commit_refused(self):
        self.assert_refused(*run_cli(base(GITHUB_SHA='a' * 41)))

    def test_uppercase_commit_refused(self):
        # Same length, hex, but not lowercase.
        self.assert_refused(*run_cli(base(GITHUB_SHA='A' * 40)))

    def test_nonhex_commit_refused(self):
        # Same length, lowercase, but not hex.
        self.assert_refused(*run_cli(base(GITHUB_SHA='g' * 40)))

    def test_nonstring_commit_refused(self):
        # int whose decimal form is 40 hex digits. Aligned as JSON numbers so
        # only the str conjunct inside exact() can refuse.
        self.assert_refused(*run_main(base(GITHUB_SHA=int('1' * 40))))


if __name__ == '__main__':
    unittest.main()
