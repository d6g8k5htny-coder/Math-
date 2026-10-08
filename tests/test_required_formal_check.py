"""Negative controls for current-run required formal checks; stdlib only."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/required_formal_check.py'
SPEC = importlib.util.spec_from_file_location('required_check', SCRIPT)
M = importlib.util.module_from_spec(SPEC)
if SCRIPT.exists():
    SPEC.loader.exec_module(M)

class RequiredCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = {'GITHUB_SHA': 'a'*40, 'GITHUB_REPOSITORY': 'd6g8k5htny-coder/main',
                    'GITHUB_RUN_ID': '123', 'GITHUB_RUN_ATTEMPT': '2'}
        self.manifest = self.root/'manifest.json'
        self.manifest.write_text('{"source":"fixture"}\n')
        self.log = self.root/'build.log'; self.log.write_text('fixture build log\n')
        self.receipt = self.root/'receipt.json'
        self.record = {'checked_commit': self.env['GITHUB_SHA'],
            'repository': self.env['GITHUB_REPOSITORY'], 'workflow_run_id': '123',
            'formalization_status': 'kernel-checked', 'scientific_effect':'NONE',
            'manifest_sha256':hashlib.sha256(self.manifest.read_bytes()).hexdigest(),
            'logs':{'build.log':hashlib.sha256(self.log.read_bytes()).hexdigest()}}
        self.write_receipt()
        self.needs = {'checks': {'result':'success','outputs':{'checked_commit':'a'*40}},
                      'formal': {'result':'success','outputs':{
                          'checked_commit':'a'*40,'repository':self.env['GITHUB_REPOSITORY'],
                          'run_id':'123','run_attempt':'2','receipt_sha256':'b'*64}}}

    def write_receipt(self): self.receipt.write_text(json.dumps(self.record))
    def binding(self): return M.bind_receipt(self.receipt,self.manifest,self.env,'a'*40)
    def decision(self): return M.aggregate(self.needs,self.env)

    def test_implementation_exists(self):
        self.assertTrue(hasattr(M,'aggregate'), 'required-check bridge is missing')
    def test_success(self):
        result=self.decision()
        self.assertEqual(result['checked_commit'],'a'*40)
        self.assertEqual(result['scientific_effect'],'NONE')
        self.assertEqual(result['conclusion'],'success')
    def test_every_unsuccessful_result_refused(self):
        for job in ('formal','checks'):
            for result in ('failure','cancelled','skipped','neutral','timed_out','pending','',None,True):
                with self.subTest(job=job,result=result):
                    prior=self.needs[job]['result'];self.needs[job]['result']=result
                    with self.assertRaises(ValueError):self.decision()
                    self.needs[job]['result']=prior
    def test_missing_dependency(self):
        del self.needs['formal']
        with self.assertRaises(ValueError):self.decision()
    def test_extra_dependency(self):
        self.needs['other']={'result':'success'}
        with self.assertRaises(ValueError):self.decision()
    def test_each_output_required(self):
        for field in tuple(self.needs['formal']['outputs']):
            old=self.needs['formal']['outputs'].pop(field)
            with self.subTest(field=field),self.assertRaises(ValueError):self.decision()
            self.needs['formal']['outputs'][field]=old
    def test_formal_commit_drift(self):
        self.needs['formal']['outputs']['checked_commit']='c'*40
        with self.assertRaises(ValueError):self.decision()
    def test_existing_checks_commit_drift(self):
        self.needs['checks']['outputs']['checked_commit']='c'*40
        with self.assertRaises(ValueError):self.decision()
    def test_changed_test_merge_commit(self):
        self.env['GITHUB_SHA']='c'*40
        with self.assertRaises(ValueError):self.decision()
    def test_repository_substitution(self):
        self.needs['formal']['outputs']['repository']='d6g8k5htny-coder/Math-'
        with self.assertRaises(ValueError):self.decision()
    def test_stale_run(self):
        self.needs['formal']['outputs']['run_id']='122'
        with self.assertRaises(ValueError):self.decision()
    def test_stale_attempt(self):
        self.needs['formal']['outputs']['run_attempt']='1'
        with self.assertRaises(ValueError):self.decision()
    def test_no_numeric_identity_coercion(self):
        self.env['GITHUB_SHA']=int('1'*40)
        with self.assertRaises(ValueError):self.decision()
    def test_bad_digest(self):
        for value in ('main','B'*64,1,'b'*63):
            self.needs['formal']['outputs']['receipt_sha256']=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.decision()
    def test_binding_preserves_receipt(self):
        before=self.receipt.read_bytes(); result=self.binding()
        self.assertEqual(self.receipt.read_bytes(),before)
        self.assertEqual(result['receipt_sha256'],hashlib.sha256(before).hexdigest())
        self.assertEqual(result['run_attempt'],'2')
    def test_unproved_receipt_refused(self):
        self.record['formalization_status']='specified';self.write_receipt()
        with self.assertRaises(ValueError):self.binding()
    def test_receipt_drift(self):
        self.record['checked_commit']='c'*40;self.write_receipt()
        with self.assertRaises(ValueError):self.binding()
    def test_manifest_drift(self):
        self.manifest.write_text('changed')
        with self.assertRaises(ValueError):self.binding()
    def test_log_tamper(self):
        self.log.write_text('changed')
        with self.assertRaises(ValueError):self.binding()
    def test_empty_logs_refused(self):
        self.record['logs']={};self.write_receipt()
        with self.assertRaises(ValueError):self.binding()
    def test_symlink_log_refused(self):
        self.log.unlink();other=self.root/'other';other.write_text('fixture build log\n');self.log.symlink_to(other)
        with self.assertRaises(ValueError):self.binding()
    def test_traversal_log_refused(self):
        self.record['logs']={'../build.log':'b'*64};self.write_receipt()
        with self.assertRaises(ValueError):self.binding()
    def test_duplicate_json_keys_refused(self):
        with self.assertRaises(ValueError):M.strict_json('{"formal":{},"formal":{}}')
    def test_actual_cli_failure(self):
        env={**os.environ,**self.env,'REQUIRED_FORMAL_NEEDS':json.dumps(self.needs)}
        good=subprocess.run([sys.executable,'-B','-S',str(SCRIPT),'aggregate'],env=env,capture_output=True,text=True)
        self.assertEqual(good.returncode,0,good.stderr)
        self.needs['formal']['result']='failure';env['REQUIRED_FORMAL_NEEDS']=json.dumps(self.needs)
        bad=subprocess.run([sys.executable,'-B','-S',str(SCRIPT),'aggregate'],env=env,capture_output=True,text=True)
        self.assertNotEqual(bad.returncode,0)
        self.assertNotIn('"conclusion": "success"',bad.stdout)

    # Mutation-gap controls: each test refuses a weakening that the tests above still admit.
    def test_attempt_identity_is_exact(self):
        for value in ('0', '01', 'x', '1 ', ''):
            with self.subTest(value=value):
                self.env['GITHUB_RUN_ATTEMPT']=value;self.needs['formal']['outputs']['run_attempt']=value
                with self.assertRaises(ValueError):self.decision()
                with self.assertRaises(ValueError):self.binding()
    def test_checkout_head_must_be_tested_commit(self):
        with self.assertRaises(ValueError):M.bind_receipt(self.receipt,self.manifest,self.env,'c'*40)
    def test_symlinked_receipt_or_manifest_refused(self):
        for target in ('receipt','manifest'):
            with self.subTest(target=target):
                path=getattr(self,target);real=self.root/('real-'+target);real.write_bytes(path.read_bytes())
                path.unlink();path.symlink_to(real)
                with self.assertRaises(ValueError):self.binding()
                path.unlink();path.write_bytes(real.read_bytes())
    def test_non_object_receipt_refused(self):
        for text in ('[]','"receipt"','1','null'):
            self.receipt.write_text(text)
            with self.subTest(text=text),self.assertRaises(ValueError):self.binding()
    def test_every_receipt_identity_field_required_and_compared(self):
        for key,value in (('repository','d6g8k5htny-coder/Math-'),('workflow_run_id','122'),('scientific_effect','POSITIVE')):
            with self.subTest(key=key,value=value):
                prior=self.record[key];self.record[key]=value;self.write_receipt()
                with self.assertRaises(ValueError):self.binding()
                self.record[key]=prior
        for key in ('checked_commit','repository','workflow_run_id','formalization_status','scientific_effect'):
            with self.subTest(missing=key):
                prior=self.record.pop(key);self.write_receipt()
                with self.assertRaises(ValueError):self.binding()
                self.record[key]=prior
    def test_non_object_log_map_refused(self):
        for logs in (['build.log'],'build.log'):
            self.record['logs']=logs;self.write_receipt()
            with self.subTest(logs=logs),self.assertRaises(ValueError):self.binding()
    def test_log_digest_shape_checked_before_log_read(self):
        self.record['logs']={'absent.log':'not-a-digest'};self.write_receipt()
        with self.assertRaisesRegex(ValueError,'log digest'):self.binding()
    def test_nonfinite_json_refused(self):
        for text in ('{"a":NaN}','{"a":Infinity}','{"a":-Infinity}'):
            with self.subTest(text=text),self.assertRaises(ValueError):M.strict_json(text)
    def test_non_object_dependency_outputs_refused(self):
        for value in (None,[],'x'):
            self.needs['checks']['outputs']=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.decision()
    def test_receipt_digest_is_an_exact_string(self):
        for value in ('b'*65,'b'*64+'\n',int('1'*64)):
            self.needs['formal']['outputs']['receipt_sha256']=value
            with self.subTest(value=value),self.assertRaises(ValueError):self.decision()
    def test_cli_needs_refuse_duplicate_keys(self):
        failed=json.dumps({**self.needs['formal'],'result':'failure'})
        text='{"checks":%s,"formal":%s,"formal":%s}'%(json.dumps(self.needs['checks']),failed,json.dumps(self.needs['formal']))
        env={**os.environ,**self.env,'REQUIRED_FORMAL_NEEDS':text}
        # -E: ignore ambient PYTHON* (PYTHONOPTIMIZE, PYTHONPATH, ...); the child runs in the outer mode only.
        run=subprocess.run([sys.executable,'-E','-B',*(['-O']*sys.flags.optimize),'-S',str(SCRIPT),'aggregate'],
                           env=env,capture_output=True,text=True)
        self.assertNotEqual(run.returncode,0)
        self.assertIn('duplicate JSON key',run.stderr)

class WiringTests(unittest.TestCase):
    def setUp(self):
        self.is_main=(ROOT/'.github/workflows/workspace-landing.yml').exists()
        self.parent_name='workspace-landing.yml' if self.is_main else 'downstream-gate.yml'
        self.child_name='formal-verification.yml' if self.is_main else 'formal-lean.yml'
        self.parent=(ROOT/'.github/workflows'/self.parent_name).read_text()
        self.child=(ROOT/'.github/workflows'/self.child_name).read_text()
    def test_parent_required_name_is_aggregate(self):
        name='verify' if self.is_main else 'math-downstream-gates'
        self.assertIn('  required:\n    name: '+name+'\n    if: ${{ always() }}\n    needs: [checks, formal]\n',self.parent)
    def test_same_revision_reusable_workflow(self):
        self.assertIn('    uses: ./.github/workflows/'+self.child_name,self.parent)
        self.assertIn('  workflow_call:\n',self.child)
        self.assertNotIn('pull_request:',self.child)
        self.assertNotIn('push:',self.child)
        self.assertNotIn('head.sha',self.child)
    def test_parent_no_path_filters_or_skip_override(self):
        self.assertIn('  pull_request:',self.parent)
        self.assertNotIn('paths:',self.parent)
        self.assertNotIn('continue-on-error:',self.parent+self.child)
        self.assertNotIn('pull_request_target:',self.parent+self.child)
    def test_required_calls_validator(self):
        self.assertIn('python3 -B -S tools/required_formal_check.py aggregate',self.parent)
        self.assertIn('REQUIRED_FORMAL_NEEDS: ${{ toJSON(needs) }}',self.parent)
    def test_outputs_are_bound_to_executed_receipt(self):
        self.assertIn('python3 -B -S tools/required_formal_check.py receipt',self.child)
        for key in ('checked_commit','repository','run_id','run_attempt','receipt_sha256'):
            self.assertIn(key+':',self.child)
    def test_synthetic_control_uses_no_proof_edits(self):
        self.assertIn('python3 -B -S -m unittest discover -s tests -p test_required_formal_check.py -v',self.parent)
        self.assertIn('python3 -B -O -S -m unittest discover -s tests -p test_required_formal_check.py -v',self.parent)

# ---------------------------------------------------------------------------
# W8c mutation-gap controls. Folded into this discovery target so the
# downstream-replay commands (pattern test_required_formal_check.py) run
# them. Helpers are prefixed per control. ROOT and SCRIPT above are the
# same paths. Imports already present at the top of this module are not
# repeated.
# ---------------------------------------------------------------------------

# Proposed control (W8c): context() must allow only the two pinned execution
# repositories and refuse anything else with the handled refusal.
#
# Positive: d6g8k5htny-coder/main and d6g8k5htny-coder/Math- are accepted
# (exit 0, conclusion success, empty stderr), so a reject-everything stub fails.
# Negative: the exact refusal — exit 1, stderr
# 'REQUIRED_FORMAL_CHECK_FAILED: unexpected execution repository', empty stdout.
# Needs outputs are aligned with the env value, so a later equality check cannot
# substitute for the allowlist. Offline: no network. Drives the job command
# `python3 -B -S tools/required_formal_check.py aggregate`.

_w8c_repo_REFUSAL = 'REQUIRED_FORMAL_CHECK_FAILED: unexpected execution repository\n'


def _w8c_repo_base(**over):
    env = {
        'GITHUB_SHA': '9fd261135b41daf1e377f9ef2db193fee6ec36be',
        'GITHUB_REPOSITORY': 'd6g8k5htny-coder/Math-',
        'GITHUB_RUN_ID': '123',
        'GITHUB_RUN_ATTEMPT': '2',
    }
    env.update(over)
    return env


def _w8c_repo_needs_for(env):
    sha, repo, run, attempt = (env['GITHUB_SHA'], env['GITHUB_REPOSITORY'],
                               env['GITHUB_RUN_ID'], env['GITHUB_RUN_ATTEMPT'])
    return {
        'checks': {'result': 'success', 'outputs': {'checked_commit': sha}},
        'formal': {'result': 'success', 'outputs': {
            'checked_commit': sha, 'repository': repo, 'run_id': run,
            'run_attempt': attempt, 'receipt_sha256': 'b' * 64,
        }},
    }


def _w8c_repo_run_cli(env):
    full = os.environ.copy()
    full.pop('REQUIRED_FORMAL_NEEDS', None)
    full.update(env)
    full['REQUIRED_FORMAL_NEEDS'] = json.dumps(_w8c_repo_needs_for(env))
    full.pop('PYTHONOPTIMIZE', None)
    proc = subprocess.run(
        [sys.executable, '-B', *(['-O'] if sys.flags.optimize else []), '-S', str(SCRIPT), 'aggregate'],
        cwd=ROOT, env=full, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


class RepositoryAllowlistControl(unittest.TestCase):
    def assert_accepted(self, code, out, err, repo):
        self.assertEqual((code, err), (0, ''))
        self.assertIn('"conclusion": "success"', out)
        self.assertIn('"repository": "%s"' % repo, out)

    def assert_refused(self, code, out, err):
        self.assertEqual(code, 1)
        self.assertEqual(err, _w8c_repo_REFUSAL)
        self.assertEqual(out, '')

    def test_main_repository_accepted(self):
        self.assert_accepted(*_w8c_repo_run_cli(_w8c_repo_base(GITHUB_REPOSITORY='d6g8k5htny-coder/main')),
                             'd6g8k5htny-coder/main')

    def test_math_repository_accepted(self):
        self.assert_accepted(*_w8c_repo_run_cli(_w8c_repo_base(GITHUB_REPOSITORY='d6g8k5htny-coder/Math-')),
                             'd6g8k5htny-coder/Math-')

    def test_unpinned_repository_refused(self):
        # Aligned on both sides: only the allowlist can refuse this string.
        self.assert_refused(*_w8c_repo_run_cli(_w8c_repo_base(GITHUB_REPOSITORY='d6g8k5htny-coder/other')))

    def test_empty_repository_refused(self):
        self.assert_refused(*_w8c_repo_run_cli(_w8c_repo_base(GITHUB_REPOSITORY='')))

# Proposed control (W8c): checked_commit must be a 40-character lowercase hex
# string. Length, hex class, lowercase, and str-type are separate predicates.
#
# Positive: a real 40-lowercase-hex commit is accepted (exit 0, that commit
# reported, empty stderr). Negative: exit 1, stderr exactly
# 'REQUIRED_FORMAL_CHECK_FAILED: invalid commit', empty stdout.
# Needs checked_commit is aligned with GITHUB_SHA, so a mismatch check cannot
# substitute for exact(). The non-string case calls main() with an injected env
# because a process environment cannot hold an int. Offline: no network.

import contextlib
import io
from unittest import mock

_w8c_commit_REFUSAL = 'REQUIRED_FORMAL_CHECK_FAILED: invalid commit\n'
_w8c_commit_SHA = '9fd261135b41daf1e377f9ef2db193fee6ec36be'
_w8c_commit_SPEC = importlib.util.spec_from_file_location('required_check_w8c_commit', SCRIPT)
_w8c_commit_M = importlib.util.module_from_spec(_w8c_commit_SPEC)
_w8c_commit_SPEC.loader.exec_module(_w8c_commit_M)


def _w8c_commit_base(**over):
    env = {
        'GITHUB_SHA': _w8c_commit_SHA,
        'GITHUB_REPOSITORY': 'd6g8k5htny-coder/Math-',
        'GITHUB_RUN_ID': '123',
        'GITHUB_RUN_ATTEMPT': '2',
    }
    env.update(over)
    return env


def _w8c_commit_needs_for(env):
    sha, repo, run, attempt = (env['GITHUB_SHA'], env['GITHUB_REPOSITORY'],
                               env['GITHUB_RUN_ID'], env['GITHUB_RUN_ATTEMPT'])
    return {
        'checks': {'result': 'success', 'outputs': {'checked_commit': sha}},
        'formal': {'result': 'success', 'outputs': {
            'checked_commit': sha, 'repository': repo, 'run_id': run,
            'run_attempt': attempt, 'receipt_sha256': 'b' * 64,
        }},
    }


def _w8c_commit_run_cli(env):
    full = os.environ.copy()
    full.pop('REQUIRED_FORMAL_NEEDS', None)
    full.update(env)
    full['REQUIRED_FORMAL_NEEDS'] = json.dumps(_w8c_commit_needs_for(env))
    full.pop('PYTHONOPTIMIZE', None)
    proc = subprocess.run(
        [sys.executable, '-B', *(['-O'] if sys.flags.optimize else []), '-S', str(SCRIPT), 'aggregate'],
        cwd=ROOT, env=full, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _w8c_commit_run_main(env):
    payload = dict(env)
    payload['REQUIRED_FORMAL_NEEDS'] = json.dumps(_w8c_commit_needs_for(env))
    out, err = io.StringIO(), io.StringIO()
    with mock.patch.object(_w8c_commit_M.os, 'environ', payload), \
         mock.patch.object(sys, 'argv', ['required_formal_check.py', 'aggregate']), \
         contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = _w8c_commit_M.main()
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
        self.assertEqual(err, _w8c_commit_REFUSAL)
        self.assertEqual(out, '')

    def test_lowercase_40_hex_accepted(self):
        self.assert_accepted(*_w8c_commit_run_cli(_w8c_commit_base()), _w8c_commit_SHA)

    def test_short_commit_refused(self):
        # 39 hex chars: only the length bound can refuse once outputs are aligned.
        self.assert_refused(*_w8c_commit_run_cli(_w8c_commit_base(GITHUB_SHA='a' * 39)))

    def test_long_commit_refused(self):
        self.assert_refused(*_w8c_commit_run_cli(_w8c_commit_base(GITHUB_SHA='a' * 41)))

    def test_uppercase_commit_refused(self):
        # Same length, hex, but not lowercase.
        self.assert_refused(*_w8c_commit_run_cli(_w8c_commit_base(GITHUB_SHA='A' * 40)))

    def test_nonhex_commit_refused(self):
        # Same length, lowercase, but not hex.
        self.assert_refused(*_w8c_commit_run_cli(_w8c_commit_base(GITHUB_SHA='g' * 40)))

    def test_nonstring_commit_refused(self):
        # int whose decimal form is 40 hex digits. Aligned as JSON numbers so
        # only the str conjunct inside exact() can refuse.
        self.assert_refused(*_w8c_commit_run_main(_w8c_commit_base(GITHUB_SHA=int('1' * 40))))

# Proposed control (W8c): workflow run_id must match [1-9][0-9]* (no zero,
# no leading zero, digits only). Those predicates are isolated.
#
# Positive: '123' and '7' are accepted (exit 0, that run_id reported, empty
# stderr). Negative: exit 1, stderr exactly
# 'REQUIRED_FORMAL_CHECK_FAILED: invalid run ID', empty stdout.
# Formal outputs run_id is aligned with GITHUB_RUN_ID, so the later equality
# check cannot substitute for exact(). Offline: no network. Drives
# `python3 -B -S tools/required_formal_check.py aggregate`.

_w8c_run_REFUSAL = 'REQUIRED_FORMAL_CHECK_FAILED: invalid run ID\n'


def _w8c_run_base(**over):
    env = {
        'GITHUB_SHA': '9fd261135b41daf1e377f9ef2db193fee6ec36be',
        'GITHUB_REPOSITORY': 'd6g8k5htny-coder/Math-',
        'GITHUB_RUN_ID': '123',
        'GITHUB_RUN_ATTEMPT': '2',
    }
    env.update(over)
    return env


def _w8c_run_needs_for(env):
    sha, repo, run, attempt = (env['GITHUB_SHA'], env['GITHUB_REPOSITORY'],
                               env['GITHUB_RUN_ID'], env['GITHUB_RUN_ATTEMPT'])
    return {
        'checks': {'result': 'success', 'outputs': {'checked_commit': sha}},
        'formal': {'result': 'success', 'outputs': {
            'checked_commit': sha, 'repository': repo, 'run_id': run,
            'run_attempt': attempt, 'receipt_sha256': 'b' * 64,
        }},
    }


def _w8c_run_run_cli(env):
    full = os.environ.copy()
    full.pop('REQUIRED_FORMAL_NEEDS', None)
    full.update(env)
    full['REQUIRED_FORMAL_NEEDS'] = json.dumps(_w8c_run_needs_for(env))
    full.pop('PYTHONOPTIMIZE', None)
    proc = subprocess.run(
        [sys.executable, '-B', *(['-O'] if sys.flags.optimize else []), '-S', str(SCRIPT), 'aggregate'],
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
        self.assertEqual(err, _w8c_run_REFUSAL)
        self.assertEqual(out, '')

    def test_multidigit_run_id_accepted(self):
        self.assert_accepted(*_w8c_run_run_cli(_w8c_run_base(GITHUB_RUN_ID='123')), '123')

    def test_single_nonzero_digit_accepted(self):
        self.assert_accepted(*_w8c_run_run_cli(_w8c_run_base(GITHUB_RUN_ID='7')), '7')

    def test_zero_run_id_refused(self):
        self.assert_refused(*_w8c_run_run_cli(_w8c_run_base(GITHUB_RUN_ID='0')))

    def test_leading_zero_run_id_refused(self):
        # Digits only, but a leading zero. The bare-zero alternative does not match.
        self.assert_refused(*_w8c_run_run_cli(_w8c_run_base(GITHUB_RUN_ID='01')))

    def test_nonnumeric_run_id_refused(self):
        self.assert_refused(*_w8c_run_run_cli(_w8c_run_base(GITHUB_RUN_ID='12a')))

    def test_empty_run_id_refused(self):
        self.assert_refused(*_w8c_run_run_cli(_w8c_run_base(GITHUB_RUN_ID='')))
if __name__=='__main__':unittest.main()
