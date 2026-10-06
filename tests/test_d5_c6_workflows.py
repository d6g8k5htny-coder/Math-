"""Actual shell/subprocess controls for three frozen D5/C6 checker interfaces.

Fixtures have self-consistent manifests and a real committed Git tree. They are
synthetic protocol tests, not mathematical evidence. Set WORKFLOW_SOURCE_ROOT to
an original source checkout to demonstrate pre-repair failures with this suite.
"""
from pathlib import Path
import hashlib
from concurrent.futures import ThreadPoolExecutor
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(os.environ.get('WORKFLOW_SOURCE_ROOT', Path(__file__).resolve().parents[1]))
HERE = Path(__file__).resolve().parents[1]
HELPER = Path('tools/d5_c6_replay.py')
TEST_PATH = 'tests/test_d5_c6_workflows.py'
CONFIG = {
    'd5': ('d5-dimension-lift', 'd5_dimension_lift_20260929', 'lift_exact_check.py'),
    'palm': ('c6-palm-route', 'c6_palm_route_20260929', 'palm_exact_check.py'),
    'factorial': ('c6-factorial-moment', 'c6_factorial_moment_20260929', 'c6_check.py'),
}
# Independent expectations characterized from the unchanged source CLIs in both
# Python modes. Test fixtures do not import the implementation's contract table.
CONTRACTS = {
    'd5': {
        'drop-frobenius-order': ('check_x', 'two-soft-direction exterior inequality failed in d=3'),
        'drop-s0-block': ('check_g', 'frame rank drop in d=2'),
        'drop-a4-column': ('check_g', 'frame rank drop in d=2'),
        'degree-four': ('check_r', 'degree-four axis rank is not d'),
        'row-operation-third': ('check_ro', 'height row has a negative power of s'),
        'euler-coefficient': ('check_eu', 'Euler identity remainder is not minus the quartic part'),
        'adjugate-sign': ('check_tb', 'block determinant identity failed'),
        'one-soft-direction': ('check_l', 'pin region I ledger is not r^3'),
        'flat-shell': ('check_l', 'shell sum is not bounded by the dyadic constants'),
        'weight-one-less-power': ('check_w', 'pin weight is not integrable in d=2'),
    },
    'palm': {
        'no-slab': ('check_pk', 'retained ball within zeta_0/2 of the witness sphere'),
        'weak-zeta': ('check_pk', 'zeta_0 exceeds eta_j/8'),
        'lambda-too-large': ('check_ex', 'Markov term does not decay in d=2'),
        'series-ratio': ('check_tl', 'no index makes the series ratio fall below 2^(-1/(4d)) for d=2 p=1'),
        'factorial-power': ('check_pw', '(N)_q <= N Psi^(q-1) fails at N=3 Psi=5 q=2'),
        'schur-upper': ('check_sc', 'Schur complement is not bounded above by c I'),
        'forget-mark-power': ('check_lg', 'R1 region II absorption power is not 6+3d in d=2'),
    },
    'factorial': {
        'wrong-elimination': 'ELIMINATION', 'touching-balls': 'PACKING',
        'no-log': 'RADIAL', 'short-remainder': 'REMAINDER',
    },
}
FACTORIAL_BASE = {
    'object': 'CL-C6-FACTORIAL-20260929-v1',
    'checks': dict.fromkeys(['ELIMINATION', 'CAP_ATTAINED', 'REMAINDER', 'PACKING', 'RADIAL'], True),
    'passed': True,
    'scope': 'finite identities and one quadrature only; the analytic proof is PROOF.md',
}


def script_source(family, behavior, target, mode):
    baseline = json.dumps(FACTORIAL_BASE if family == 'factorial' else
                          {'fixture': family, 'passed': True}, sort_keys=True).encode() + b'\n'
    start = f'''import json, sys
from pathlib import Path
FAMILY={family!r}
BEHAVIOR={behavior!r}
TARGET={target!r}
MODE={mode!r}
CONTRACTS={CONTRACTS[family]!r}
BASELINE={baseline!r}
if len(sys.argv)==1:
    if BEHAVIOR=='baseline_stderr' and sys.flags.optimize==MODE:
        sys.stderr.write('unexpected baseline stderr\\n')
    if BEHAVIOR=='baseline_wrong':
        sys.stdout.buffer.write(b'wrong baseline\\n')
    elif BEHAVIOR=='baseline_exit':
        sys.stdout.buffer.write(BASELINE)
        raise SystemExit(1)
    else:
        sys.stdout.buffer.write(BASELINE)
    raise SystemExit(0)
MUT=sys.argv[sys.argv.index('--mutant')+1]
if MUT not in CONTRACTS: raise SystemExit(2)
ACTIVE=MUT==TARGET and sys.flags.optimize==MODE
if ACTIVE and BEHAVIOR=='crash': raise RuntimeError('not the intended rejection')
if ACTIVE and BEHAVIOR=='empty': raise SystemExit(1)
if ACTIVE and BEHAVIOR=='exit_zero': raise SystemExit(0)
if ACTIVE and BEHAVIOR=='stderr': sys.stderr.write('unexpected mutant stderr\\n')
if ACTIVE and BEHAVIOR=='prefix': sys.stdout.write('unexpected prefix\\n')
if ACTIVE and BEHAVIOR=='whitespace': sys.stdout.write(' \\n\\t')
'''
    if family == 'factorial':
        start += '''doc=json.loads(BASELINE)
doc['checks'][CONTRACTS[MUT]]=False
doc['passed']=False
if ACTIVE:
    if BEHAVIOR=='wrong_check':
        doc['checks']=dict.fromkeys(doc['checks'], True)
        doc['checks']['CAP_ATTAINED']=False
    elif BEHAVIOR=='extra_failure': doc['checks']['CAP_ATTAINED']=False
    elif BEHAVIOR=='boolean_int': doc['passed']=0
    elif BEHAVIOR=='check_int': doc['checks'][CONTRACTS[MUT]]=0
    elif BEHAVIOR=='extra_key': doc['unexpected']=True
    elif BEHAVIOR=='missing_key': del doc['scope']
    elif BEHAVIOR=='object': doc['object']='other packet'
    elif BEHAVIOR=='scope': doc['scope']='unbounded mathematical acceptance'
raw=json.dumps(doc,sort_keys=True)
if ACTIVE and BEHAVIOR=='formatting': raw=json.dumps(doc,indent=2,sort_keys=False)
if ACTIVE:
    if BEHAVIOR=='duplicate': raw=raw[:-1]+',"passed":false}'
    elif BEHAVIOR=='nested_duplicate': raw=raw.replace('"CAP_ATTAINED": true','"CAP_ATTAINED":true,"CAP_ATTAINED":true')
    elif BEHAVIOR=='nan': raw=raw.replace('"passed": false','"passed": NaN')
    elif BEHAVIOR=='infinity': raw=raw.replace('"passed": false','"passed": Infinity')
    elif BEHAVIOR=='overflow': raw=raw.replace('"passed": false','"passed": 1e999')
    elif BEHAVIOR=='floating_zero': raw=raw.replace('"passed": false','"passed": 0.0')
    elif BEHAVIOR=='malformed': raw='not JSON'
    elif BEHAVIOR=='trailing': raw+=' unexpected'
print(raw)
raise SystemExit(1)
'''
    else:
        start += '''MESSAGE=CONTRACTS[MUT][1]
if ACTIVE and BEHAVIOR=='wrong_message': MESSAGE='wrong assertion'
class OtherAssertion(AssertionError): pass
def require(ok,message):
    if not ok:
        if ACTIVE and BEHAVIOR=='subclass': raise OtherAssertion(message)
        raise AssertionError(message)
def wrong_group(): require(False,MESSAGE)
'''
        for group in sorted({v[0] for v in CONTRACTS[family].values()}):
            start += f'def {group}(): require(False,MESSAGE)\n'
        start += '''if ACTIVE and BEHAVIOR=='wrong_group': wrong_group()
if ACTIVE and BEHAVIOR=='direct_assertion': raise AssertionError(MESSAGE)
if ACTIVE and BEHAVIOR=='other_file':
    exec(compile('def require(ok,message):\\n    raise AssertionError(message)\\nrequire(False,MESSAGE)', '<other-source>', 'exec'))
globals()[CONTRACTS[MUT][0]]()
'''
    return start.encode(), baseline


def shell_step(family):
    workflow = (ROOT / '.github/workflows' / (CONFIG[family][0] + '.yml')).read_text()
    start = workflow.index("          set -euo pipefail\n", workflow.index("      - name: Verify sources, replay both modes, reject mutants"))
    end = workflow.index('          git diff --exit-code', start) + len('          git diff --exit-code')
    return textwrap.dedent(workflow[start:end]) + '\n'


def run_fixture(family, behavior='valid', target=None, mode=0):
    target = target or next(iter(CONTRACTS[family]))
    with tempfile.TemporaryDirectory(prefix='d5-c6-protocol-') as td:
        root = Path(td)
        packet = root / 'frontiers' / CONFIG[family][1]
        packet.mkdir(parents=True)
        source, baseline = script_source(family, behavior, target, mode)
        payloads = {CONFIG[family][2]: source, 'RESULTS.json': baseline, 'NOTE.md': b'Synthetic protocol fixture, not mathematics.\n'}
        for name, raw in payloads.items(): (packet / name).write_bytes(raw)
        manifest = {'files': [{'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                              for name, raw in sorted(payloads.items())]}
        (packet / 'SOURCE_FILES.json').write_text(json.dumps(manifest))
        # The predecessor workflows do not have/use the helper; that is not an
        # error in the red-phase fixture. Candidate workflows copy their helper.
        if (ROOT / HELPER).exists():
            (root / HELPER).parent.mkdir(parents=True)
            shutil.copyfile(ROOT / HELPER, root / HELPER)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH='')
        env.pop('PYTHONOPTIMIZE', None)
        for cmd in (['git', 'init', '-q'], ['git', 'add', '.'],
                    ['git', '-c', 'user.name=Protocol Fixture', '-c', 'user.email=fixture@example.invalid',
                     '-c', 'commit.gpgsign=false', 'commit', '-qm', 'synthetic test sources']):
            subprocess.run(cmd, cwd=root, env=env, check=True, capture_output=True)
        if behavior == 'bad_manifest':
            manifest['files'][0]['sha256']='0'*64
            (packet/'SOURCE_FILES.json').write_text(json.dumps(manifest))
        elif behavior == 'extra_file': (packet/'extra.txt').write_text('extra')
        elif behavior == 'symlink':
            p=packet/'NOTE.md'; p.unlink(); p.symlink_to(packet/'RESULTS.json')
        elif behavior == 'dirty_tree': (root/'tracked-dirty').write_text('first')
        if behavior == 'dirty_tree':
            subprocess.run(['git','add','tracked-dirty'],cwd=root,check=True,capture_output=True)
            (root/'tracked-dirty').write_text('changed')
        result = subprocess.run(['bash', '-c', shell_step(family)], cwd=root, env=env,
                                capture_output=True, timeout=30)
        return result


class WorkflowProtocolTests(unittest.TestCase):
    def verify(self, family, behavior, success=False, targets=None, modes=(0, 1)):
        jobs=[(family, behavior, target, mode) for mode in modes
              for target in targets or [next(iter(CONTRACTS[family]))]]
        # Independent committed temporary repositories; assertions stay in the
        # unittest thread. No shared checker globals or test-result mutation.
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda args: run_fixture(*args), jobs))
        for (_, _, target, mode), result in zip(jobs, results):
            with self.subTest(family=family, behavior=behavior, target=target, mode=mode):
                if success:
                    self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
                    self.assertEqual(result.stderr,b'')
                else:
                    self.assertNotEqual(result.returncode,0,'bad result admitted: '+result.stdout.decode(errors='replace'))

    def test_valid_native_failure_carriers(self):
        for family in CONFIG: self.verify(family,'valid',True)

    def test_every_named_mutant_crash_is_rejected(self):
        for family in CONFIG: self.verify(family,'crash',targets=CONTRACTS[family])

    def test_assertion_whitespace_output_is_rejected(self):
        for family in ('d5','palm'):
            self.verify(family,'whitespace')

    def test_factorial_valid_json_formatting_is_accepted(self):
        self.verify('factorial','formatting',True)

    def test_baseline_stderr_is_rejected(self):
        for family in CONFIG: self.verify(family,'baseline_stderr')

    def test_every_named_mutant_wrong_exit_is_rejected(self):
        for family in CONFIG: self.verify(family,'exit_zero',targets=CONTRACTS[family])

    def test_invalid_mutant_output(self):
        for family in CONFIG:
            for behavior in ('empty','stderr','prefix'):
                self.verify(family,behavior)

    def test_assertion_identity_and_origin(self):
        for family in ('d5','palm'):
            for behavior in ('wrong_message','wrong_group','direct_assertion','other_file','subclass'):
                self.verify(family,behavior)

    def test_factorial_exact_failure_set_and_types(self):
        for behavior in ('wrong_check','extra_failure','boolean_int','check_int','extra_key','missing_key','object','scope'):
            self.verify('factorial',behavior,targets=CONTRACTS['factorial'])

    def test_strict_factorial_json(self):
        for behavior in ('duplicate','nested_duplicate','nan','infinity','overflow','floating_zero','malformed','trailing'):
            self.verify('factorial',behavior)

    def test_existing_baseline_and_source_guards(self):
        for family in CONFIG:
            for behavior in ('baseline_wrong','baseline_exit','bad_manifest','extra_file','symlink','dirty_tree'):
                self.verify(family,behavior,modes=(0,))

    def test_all_workflows_run_regressions_and_track_inputs(self):
        for family in CONFIG:
            text=(ROOT/'.github/workflows'/(CONFIG[family][0]+'.yml')).read_text()
            with self.subTest(family=family):
                self.assertIn("- 'tools/d5_c6_replay.py'",text)
                self.assertIn("- 'tests/**'",text)
                self.assertIn('fetch-depth: 0',text)
                self.assertIn('python -B -S -m unittest discover -s tests -v',text)
                self.assertIn('python -B -O -S -m unittest discover -s tests -v',text)
                self.assertIn("python-version: '3.11.16'",text)
                self.assertNotIn('continue-on-error',text)


class ReplayHelperTests(unittest.TestCase):
    def load_helper(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('d5_c6_under_test', HERE / HELPER)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_timeout_is_never_a_rejection(self):
        helper=self.load_helper()
        flags=['-B','-O','-S'] if sys.flags.optimize else ['-B','-S']
        with tempfile.TemporaryDirectory() as td:
            script=Path(td)/'checker.py'
            for family in CONFIG:
                baseline=json.dumps(FACTORIAL_BASE if family=='factorial' else {'fixture':family}).encode()+b'\n'
                for phase in ('baseline','mutant'):
                    script.write_text('import sys,time\nBASE='+repr(baseline)+'\n'+
                        ("time.sleep(3)\n" if phase=='baseline' else '')+
                        "if len(sys.argv)==1:\n sys.stdout.buffer.write(BASE)\n raise SystemExit(0)\n"+
                        "time.sleep(3)\n")
                    with self.subTest(family=family,phase=phase):
                        with self.assertRaises(subprocess.TimeoutExpired) as caught:
                            helper.replay(script,baseline,list(CONTRACTS[family]),family,flags,timeout=0.5)
                        command=caught.exception.cmd
                        is_mutant='--mutant' in command or '--assertion' in command
                        self.assertEqual(is_mutant,phase=='mutant',command)

    def test_control_inventory_cannot_drop_or_add_labels(self):
        helper=self.load_helper()
        for family in CONFIG:
            names=list(CONTRACTS[family])
            for labels in (names[:-1],names+['unknown'],list(reversed(names))):
                with self.subTest(family=family,labels=labels):
                    with self.assertRaisesRegex(ValueError,'inventory'):
                        helper.replay('unused',b'',labels,family,['-B','-S'],1)

    def test_unknown_adapter_labels_exit_two(self):
        for family in ('d5','palm'):
            cp=subprocess.run([sys.executable,'-B','-S',str(HERE/HELPER),
                               '--assertion',family,'unused','unknown'],capture_output=True,timeout=5)
            with self.subTest(family=family):
                self.assertEqual(cp.returncode,2)
                self.assertEqual(cp.stdout,b'')
                self.assertIn(b'unknown mutant',cp.stderr)

    def test_protocol_does_not_coerce_boolean_or_accept_duplicates(self):
        helper=self.load_helper()
        self.assertFalse(helper.exact_value({'passed':0},{'passed':False}))
        self.assertTrue(helper.exact_value({'passed':False},{'passed':False}))
        for raw in (b'{"x":1,"x":1}',b'{"x":NaN}',b'{"x":1e999}',b'{"x":0.0}',b'{} trailing'):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError): helper.strict_json(raw)


if __name__ == '__main__':
    unittest.main()
