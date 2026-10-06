"""Synthetic whole-shell regressions and authentic child-diagnostic PTY checks.

The workflow fixture commits synthetic source/manifest/upstream bytes, then runs
the actual verification block with real subprocesses and measured report fixtures.
LegacyTerminalTests separately invokes the authentic C6 invalid-label command.
This is protocol coverage, not a field calculation.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('LEGACY_SOURCE_ROOT', str(ROOT)))
CONTRACTS = json.loads((ROOT/'tools/legacy_json_contracts.json').read_text())
WORKFLOWS = {'local-pairing':'local-pairing.yml','far-elder':'far-elder-rate.yml','c6-cluster':'c6-cluster-law.yml'}
ACTIVE = {k:v for k,v in CONTRACTS['families'].items() if not os.environ.get('LEGACY_TEST_FAMILY') or k == os.environ['LEGACY_TEST_FAMILY']}
if not ACTIVE:
    raise SystemExit('unknown test family')
UNKNOWN = {'local-pairing':'M9','far-elder':'M9','c6-cluster':'unknown'}
CHOICES = ('pins-not-critical','wrong-pin-hessian','drop-sigma-jacobian',
           'three-extra-points','cross-term-not-small','window-closed','index-sign',
           'shear-drop-cubic','s-bound-constant')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob %d\0'%len(data)+data).hexdigest()

def row(path, data):
    return {'path':path,'bytes':len(data),'sha256':digest(data),'git_blob':blob(data)}

def verification_shell(path):
    lines=path.read_text().splitlines()
    start=next(i for i,line in enumerate(lines) if 'name: Verify sources,' in line)
    start=next(i for i in range(start,len(lines)) if lines[i].strip()=='run: |')+1
    end=start
    while end<len(lines) and (not lines[end].strip() or lines[end].startswith('          ')):
        end+=1
    return textwrap.dedent('\n'.join(lines[start:end]))+'\n'

CHILD = r'''
import argparse, json, os, sys
from pathlib import Path
family = FAMILY
reports = REPORTS
baseline = BASELINE
unknown = UNKNOWN
label = sys.argv[2] if len(sys.argv)>2 else 'baseline'
mode = 'optimized' if sys.flags.optimize else 'normal'
with open(os.environ['LEGACY_TRACE'], 'a') as f:
    f.write(json.dumps([label,mode])+'\n')
if label == 'baseline':
    output = baseline
    rc = 0
elif label == unknown:
    if family == 'c6-cluster':
        import io, contextlib
        parser=argparse.ArgumentParser(prog=Path(__file__).name)
        parser.add_argument('--mutant', choices=CHOICES)
        stream=io.StringIO()
        try:
            with contextlib.redirect_stderr(stream):parser.parse_args(['--mutant',unknown])
        except SystemExit as exc:
            if exc.code != 2:raise
        diagnostic=stream.getvalue()
    else: diagnostic='unknown mutant label\n'
    if os.environ.get('LEGACY_TARGET')==label and os.environ.get('LEGACY_MODE')==mode:
        kind=os.environ.get('LEGACY_FAULT','')
        if kind=='unknown-wrong':diagnostic='unrelated permission failure\n'
        elif kind=='unknown-stdout':print('extra stdout')
    sys.stderr.write(diagnostic)
    sys.exit(2)
else:
    output=json.dumps(reports[label],sort_keys=True)+'\n';rc=1
if os.environ.get('LEGACY_TARGET')==label and os.environ.get('LEGACY_MODE')==mode:
    kind=os.environ.get('LEGACY_FAULT','')
    if kind=='crash':raise RuntimeError('unrelated fixture crash')
    if kind=='silent':sys.exit(rc)
    if kind=='stderr':sys.stderr.write('unexpected diagnostic\n')
    if kind=='wrong-exit':rc=0 if label!='baseline' else 1
    if kind=='wrong-reason':
        value=json.loads(output)
        if 'error' in value:value['error']='unrelated mathematical check'
        else:
            name=next(k for k,v in value['checks'].items() if v['passed'] is False)
            value['checks'][name]['info']='unrelated mathematical check'
        output=json.dumps(value)+'\n'
    if kind=='format':output=' \n'+json.dumps(json.loads(output),indent=4,sort_keys=False)+'\n\t'
    if kind=='duplicate':output=output.rstrip()[:-1]+', "passed": false}\n'
    if kind=='bool-int':output=output.replace('false','0')
    if kind=='bool-float':output=output.replace('false','0.0')
    if kind=='nonfinite':output=output.rstrip()[:-1]+', "unexpected": NaN}\n'
    if kind=='trailing':output+='{}\n'
    if kind=='extra':
        value=json.loads(output);value['unexpected']='x';output=json.dumps(value)+'\n'
    if kind=='missing':
        value=json.loads(output);del value['passed'];output=json.dumps(value)+'\n'
    if kind=='malformed':output='not JSON\n'
sys.stdout.write(output)
sys.exit(rc)
'''

class LegacyWorkflowTests(unittest.TestCase):
    maxDiff=None
    def case(self,family,label='baseline',mode='normal',fault='',tamper=None):
        with tempfile.TemporaryDirectory(prefix='legacy-json-test-') as td:
            outside=Path(td);repo=outside/'repo';repo.mkdir()
            trace=outside/'trace';contract=json.loads(json.dumps(CONTRACTS))
            entry=contract['families'][family];directory=repo/entry['directory'];directory.mkdir(parents=True)
            base=(ROOT/entry['directory']/'RESULTS.json').read_bytes() if (ROOT/entry['directory']/'RESULTS.json').exists() else BASELINES[family].encode()
            script=CHILD.replace('FAMILY',repr(family)).replace('REPORTS',repr(entry['mutants'])).replace('BASELINE',repr(base.decode())).replace('UNKNOWN',repr(UNKNOWN[family])).replace('CHOICES',repr(CHOICES))
            data=script.encode();(directory/entry['script']).write_bytes(data)
            (directory/'RESULTS.json').write_bytes(base)
            upstream=b'synthetic upstream; no scientific authority\n'
            (repo/'upstream.txt').write_bytes(upstream)
            pin=row('upstream.txt',upstream)
            files=[row(entry['script'],data),row('RESULTS.json',base)]
            if family=='c6-cluster':
                sm=json.dumps({'inputs':[pin],'planar_sources_behind_DL':[]}).encode()
                (directory/'SOURCE_MAP.json').write_bytes(sm)
                files.append(row('SOURCE_MAP.json',sm))
                (directory/'SOURCE_FILES.json').write_text(json.dumps({'files':files}))
            else:
                (directory/'SOURCES.json').write_text(json.dumps({'files':files,'consumed':[pin],'cited_only':[]}))
            (repo/'tools').mkdir()
            helper=SOURCE/'tools/legacy_json_replay.py'
            if helper.exists():shutil.copyfile(helper,repo/'tools/legacy_json_replay.py')
            entry['script_git_blob']=blob(data)
            # Only source authentication is re-bound for this synthetic fixture.
            (repo/'tools/legacy_json_contracts.json').write_text(json.dumps(contract))
            env=os.environ.copy();env.update({'LEGACY_TRACE':str(trace),'LEGACY_TARGET':label,'LEGACY_MODE':mode,'LEGACY_FAULT':fault,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0'})
            for cmd in [['git','init','-q'],['git','add','.'],['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','synthetic fixture']]:
                subprocess.run(cmd,cwd=repo,check=True,capture_output=True,timeout=15,env=env)
            if tamper=='packet':(directory/entry['script']).write_bytes(data+b'\n')
            if tamper=='upstream':(repo/'upstream.txt').write_bytes(upstream+b'x')
            shell=verification_shell(SOURCE/'.github/workflows'/WORKFLOWS[family])
            result=subprocess.run(['bash','-c',shell],cwd=repo,env=env,capture_output=True,timeout=45)
            events=[json.loads(s) for s in trace.read_text().splitlines()] if trace.exists() else []
            return result,events

    def rejected(self,fam,label,mode,fault):
        result,events=self.case(fam,label,mode,fault)
        self.assertNotEqual(result.returncode,0,(fam,label,mode,fault,'false acceptance',events))
        self.assertEqual(events[-1],[label,mode],(fam,label,mode,fault,events,result.stderr.decode(errors='replace')))

    def test_reference_custody(self):
        canonical=json.dumps(CONTRACTS['families'],sort_keys=True,separators=(',',':')).encode()
        self.assertEqual(digest(canonical),'2aa3e27caf5adf27646d5a762ab6bd12974235aa8e0390450504f399aa02417d')
        for fam,entry in ACTIVE.items():
            self.assertEqual(digest(BASELINES[fam].encode()),entry['baseline_sha256'])

    def test_valid_complete_inventory(self):
        for fam,entry in ACTIVE.items():
            with self.subTest(family=fam):
                p,events=self.case(fam)
                self.assertEqual(p.returncode,0,p.stderr.decode(errors='replace'))
                labels=['baseline',*ORDERS[fam],UNKNOWN[fam]]
                self.assertEqual(events,[[label,mode] for mode in ['normal','optimized'] for label in labels])

    def test_crashes_each_mutant_each_mode(self):
        for fam,entry in ACTIVE.items():
            for label in entry['mutants']:
                for mode in ['normal','optimized']:
                    with self.subTest(family=fam,label=label,mode=mode):self.rejected(fam,label,mode,'crash')

    def test_wrong_reasons_each_mutant_each_mode(self):
        for fam,entry in ACTIVE.items():
            for label in entry['mutants']:
                for mode in ['normal','optimized']:
                    with self.subTest(family=fam,label=label,mode=mode):self.rejected(fam,label,mode,'wrong-reason')

    def test_silent_each_mutant_each_mode(self):
        for fam,entry in ACTIVE.items():
            for label in entry['mutants']:
                for mode in ['normal','optimized']:
                    with self.subTest(family=fam,label=label,mode=mode):self.rejected(fam,label,mode,'silent')

    def test_baseline_stderr(self):
        for fam in ACTIVE:
            for mode in ['normal','optimized']:
                with self.subTest(family=fam,mode=mode):self.rejected(fam,'baseline',mode,'stderr')

    def test_json_contract(self):
        for fam in ACTIVE:
            label=ORDERS[fam][0]
            for fault in ['stderr','duplicate','bool-int','bool-float','nonfinite','trailing','extra','missing','malformed']:
                for mode in ['normal','optimized']:
                    with self.subTest(family=fam,fault=fault,mode=mode):self.rejected(fam,label,mode,fault)

    def test_unknown_diagnostics(self):
        for fam in ACTIVE:
            for mode in ['normal','optimized']:
                for fault in ['unknown-wrong','unknown-stdout']:
                    with self.subTest(family=fam,mode=mode,fault=fault):self.rejected(fam,UNKNOWN[fam],mode,fault)

    def test_harmless_mutant_json_formatting(self):
        for fam in ACTIVE:
            for mode in ['normal','optimized']:
                with self.subTest(family=fam,mode=mode):
                    p,events=self.case(fam,ORDERS[fam][0],mode,'format')
                    self.assertEqual(p.returncode,0,p.stderr.decode(errors='replace'))

    def test_wrong_exit_remains_rejected(self):
        for fam in ACTIVE:
            for mode in ['normal','optimized']:
                with self.subTest(family=fam,mode=mode):self.rejected(fam,ORDERS[fam][0],mode,'wrong-exit')

    def test_source_guards_before_children(self):
        for fam in ACTIVE:
            for what in ['packet','upstream']:
                with self.subTest(family=fam,what=what):
                    p,events=self.case(fam,tamper=what)
                    self.assertNotEqual(p.returncode,0)
                    self.assertEqual(events,[])

    def test_baseline_bytes_remain_exact(self):
        for fam in ACTIVE:
            for mode in ['normal','optimized']:
                with self.subTest(family=fam,mode=mode):self.rejected(fam,'baseline',mode,'format')

@unittest.skipUnless(os.name == 'posix', 'real PTY regression requires POSIX')
class LegacyTerminalTests(unittest.TestCase):
    """Compare the real captured checker with a parent attached to a real PTY."""

    def diagnostic_case(self, width, columns, optimized):
        import fcntl
        import pty
        import struct
        import termios
        script = ROOT/'frontiers/c6_cluster_law_20260929/cluster_law_check.py'
        self.assertEqual(blob(script.read_bytes()),
                         '91f485f529e09bebcd92f5a8f41d87bf01efc6d6')
        env = os.environ.copy()
        env.pop('COLUMNS', None)
        env.pop('LINES', None)
        if columns is not None:
            env['COLUMNS'] = columns
        flags = ['-B', '-O', '-S'] if optimized else ['-B', '-S']
        code = '''
import importlib.util, json, os, subprocess, sys
spec = importlib.util.spec_from_file_location('legacy_parent', sys.argv[1])
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
expected = helper._unknown_stderr('c6-cluster', 'cluster_law_check.py')
child_flags = ['-B', '-O', '-S'] if sys.flags.optimize else ['-B', '-S']
child = subprocess.run([sys.executable, *child_flags, sys.argv[2], '--mutant', 'unknown'],
                       capture_output=True, timeout=15)
print(json.dumps({'tty':sys.stdout.isatty(), 'width':os.get_terminal_size(1).columns,
                  'returncode':child.returncode, 'stdout':child.stdout.hex(),
                  'actual':child.stderr.hex(), 'expected':expected.hex()}), file=sys.stderr)
'''
        master, slave = pty.openpty()
        try:
            fcntl.ioctl(slave, termios.TIOCSWINSZ,
                        struct.pack('HHHH', 24, width, 0, 0))
            run = subprocess.run(
                [sys.executable, *flags, '-c', code,
                 str(SOURCE/'tools/legacy_json_replay.py'), str(script)],
                stdout=slave, stderr=subprocess.PIPE, env=env, timeout=30)
        finally:
            os.close(slave)
            os.close(master)
        self.assertEqual(run.returncode, 0, run.stderr.decode(errors='replace'))
        record = json.loads(run.stderr)
        self.assertTrue(record['tty'])
        self.assertEqual(record['width'], width)
        self.assertEqual(record['returncode'], 2)
        self.assertEqual(record['stdout'], '')
        self.assertEqual(record['actual'], record['expected'], record)

    def test_unknown_diagnostic_uses_child_pipe_width(self):
        for width in (30, 80, 220):
            for optimized in (False, True):
                with self.subTest(width=width, optimized=optimized):
                    self.diagnostic_case(width, None, optimized)

    def test_columns_override_matches_captured_child(self):
        for width in (30, 220):
            for columns in ('35', '80', '220', ' 110 '):
                for optimized in (False, True):
                    with self.subTest(width=width, columns=columns, optimized=optimized):
                        self.diagnostic_case(width, columns, optimized)

    def test_invalid_columns_use_pipe_fallback(self):
        for width in (30, 220):
            for columns in ('', '0', '-3', 'not-a-number'):
                for optimized in (False, True):
                    with self.subTest(width=width, columns=columns, optimized=optimized):
                        self.diagnostic_case(width, columns, optimized)


@unittest.skipUnless(os.name == 'posix', 'synthetic signer probe requires POSIX')
class LegacySigningTests(unittest.TestCase):
    """Exercise real Git with an inert signer, without any real signing key."""

    def signing_environment(self, folder):
        signer = folder/'inert-signer'
        signer.write_text('#!/bin/sh\nprintf "invoked\\n" >> "$LEGACY_SIGN_TRACE"\nexit 17\n')
        signer.chmod(0o700)
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        settings = [('commit.gpgsign', 'true'), ('gpg.format', 'openpgp'),
                    ('gpg.program', str(signer.resolve())),
                    ('user.signingkey', 'synthetic-test-key-not-a-real-key')]
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_CONFIG_COUNT=str(len(settings)),
                   GIT_TRACE2_EVENT=str((folder/'git-trace.jsonl').resolve()),
                   LEGACY_SIGN_TRACE=str((folder/'signer.calls').resolve()))
        for i,(key,value) in enumerate(settings):
            env['GIT_CONFIG_KEY_'+str(i)] = key
            env['GIT_CONFIG_VALUE_'+str(i)] = value
        return env

    def test_disposable_commits_never_invoke_inherited_signer(self):
        code = '''
import importlib.util,json,subprocess,sys
from pathlib import Path
p=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('signing_fixture',p)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def configured():
    return subprocess.check_output(['git','config','--bool','--get','commit.gpgsign'],text=True).strip()
before=configured()
r,events=m.LegacyWorkflowTests().case(sys.argv[2])
after=configured()
print(json.dumps({'before':before,'after':after,'returncode':r.returncode,
                  'stderr':r.stderr.decode(),'events':events}))
'''
        flags = ['-B','-O','-S'] if sys.flags.optimize else ['-B','-S']
        for family in ACTIVE:
            with self.subTest(family=family), tempfile.TemporaryDirectory() as td:
                folder = Path(td)
                env = self.signing_environment(folder)
                result = subprocess.run([sys.executable,*flags,'-c',code,
                                         str(Path(__file__).resolve()),family],
                                        cwd=folder,env=env,capture_output=True,timeout=60)
                calls = folder/'signer.calls'
                called = calls.read_text() if calls.exists() else ''
                self.assertEqual(result.returncode,0,
                                 (called,result.stderr.decode(errors='replace')))
                self.assertEqual(result.stderr,b'')
                report = json.loads(result.stdout)
                self.assertEqual(report['returncode'],0,report)
                self.assertEqual(report['stderr'],'')
                self.assertEqual((report['before'],report['after']),('true','true'))
                labels = ['baseline',*ORDERS[family],UNKNOWN[family]]
                self.assertEqual(report['events'],[[label,mode] for mode in
                                 ['normal','optimized'] for label in labels])
                trace = [json.loads(line) for line in
                         (folder/'git-trace.jsonl').read_text().splitlines() if line]
                commits = [e for e in trace if e.get('event')=='start'
                           and 'commit' in e.get('argv',[])]
                self.assertEqual(len(commits),1,'must observe actual fixture commit')
                self.assertEqual(called,'','disposable commit invoked inherited signer')

    def test_inert_signer_is_reached_when_signing_is_requested(self):
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td)
            env = self.signing_environment(folder)
            repo = folder/'positive-control';repo.mkdir()
            (repo/'payload').write_text('synthetic positive control\n')
            for command in (['git','init','-q'],['git','add','.']):
                subprocess.run(command,cwd=repo,env=env,check=True,
                               capture_output=True,timeout=15)
            result = subprocess.run(['git','-c','user.name=Fixture',
                                     '-c','user.email=fixture@example.invalid',
                                     'commit','-qm','signer positive control'],
                                    cwd=repo,env=env,capture_output=True,timeout=15)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual((folder/'signer.calls').read_text(),'invoked\n')
            trace = [json.loads(line) for line in
                     (folder/'git-trace.jsonl').read_text().splitlines() if line]
            self.assertTrue(any(e.get('event')=='child_start' and any(
                str(arg)==str((folder/'inert-signer').resolve())
                for arg in e.get('argv',[])) for e in trace),
                'positive control must observe a real signer child')
            configured = subprocess.check_output(
                ['git','config','--bool','--get','commit.gpgsign'],
                cwd=repo,env=env,text=True).strip()
            self.assertEqual(configured,'true')


ORDERS={'local-pairing':['M1','M2','M3','M4'],'far-elder':['M1','M2','M3','M4'],'c6-cluster':['pins-not-critical','wrong-pin-hessian','drop-sigma-jacobian','three-extra-points','shear-drop-cubic','s-bound-constant','cross-term-not-small','window-closed','index-sign']}
# BASELINES inserted below from native RESULTS, independently hash-bound above.
BASELINES = {'c6-cluster': '{\n  "groups": [\n    "NF",\n    "RS",\n    "EX",\n    "BD",\n    "EU",\n    "SH",\n    "TW",\n    "LG"\n  ],\n  "ledger": {\n    "cross_term_exponent": "9/2",\n    "hadamard_row_factors": {\n      "3": 6,\n      "4": 8\n    },\n    "soft_slice_exponent": 3,\n    "ui_tail": "1/(M-1)"\n  },\n  "mathematical_acceptance": false,\n  "object": "CL-C6-CLUSTER-LAW-20260929-v1.2",\n  "passed": true,\n  "q2_terms": 12,\n  "schema": 1,\n  "scientific_effect": "NONE",\n  "scope": "exact identities, exact configurations and exponent bookkeeping only",\n  "typed_window": {\n    "family_size": 201720,\n    "typed_in_window": 2590\n  }\n}\n', 'far-elder': '{\n "checks": {\n  "B1_barrier_polynomial": {\n   "info": {\n    "K": "22",\n    "R": "1/11",\n    "grid_points_in_ball": 1793,\n    "lambda": "2"\n   },\n   "passed": true\n  },\n  "B2_algebra_and_constants": {\n   "info": {\n    "L=1": {\n     "a_L": "1/4",\n     "c_L": "1/48"\n    },\n    "L=2": {\n     "a_L": "1/2",\n     "c_L": "1/12"\n    },\n    "L=24": {\n     "a_L": "1",\n     "c_L": "1/3"\n    },\n    "L=4": {\n     "a_L": "1",\n     "c_L": "1/3"\n    }\n   },\n   "passed": true\n  },\n  "I1_split_integral": {\n   "info": {\n    "q=2,u=1/100": "149/1000000",\n    "q=2,u=1/4": "5/64",\n    "q=2,u=1/9": "25/1458",\n    "q=4,u=1/100": "299999999/4000000000000",\n    "q=4,u=1/4": "767/16384",\n    "q=4,u=1/9": "9841/1062882"\n   },\n   "passed": true\n  },\n  "I2_exponent_ledger": {\n   "info": {\n    "count exponent": "5/3",\n    "inverse moment threshold": "-5/3",\n    "u^2 exponent of ell": "2/3"\n   },\n   "passed": true\n  },\n  "N1_near_consistency": {\n   "info": {\n    "6*sqrt(6 c_L) < 12 for c_L <= 1/3": true\n   },\n   "passed": true\n  }\n },\n "object": "CL-FAR-ELDER-RATE-20260930-v1",\n "passed": true,\n "scientific_effect": "NONE"\n}\n', 'local-pairing': '{\n  "checks": {\n    "I0_I3_identities": {\n      "info": 144,\n      "passed": true\n    },\n    "N1_n0_grid": {\n      "info": {\n        "n0_points_with_U_hypothesis": 0,\n        "n0_typed_grid_points": 135\n      },\n      "passed": true\n    },\n    "P1_path_cases": {\n      "info": {\n        "cases": {\n          "U": 2160,\n          "V": 4680,\n          "V_at_other_root": 2160\n        },\n        "min_margin": "1/1200",\n        "samples": 6840\n      },\n      "passed": true\n    },\n    "P2_elder_witness": {\n      "info": {\n        "Z1_squared": "15/8",\n        "n": 2,\n        "saddle_height": "-7/32",\n        "u0": "-3/4",\n        "vertical_line_constant": true\n      },\n      "passed": true\n    }\n  },\n  "object": "CL-LOCAL-PAIRING-20260930-v1",\n  "passed": true,\n  "scientific_effect": "NONE"\n}\n'}

if __name__ == "__main__":
    unittest.main(verbosity=2)
