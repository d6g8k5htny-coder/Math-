"""Complete-shell regression fixtures; synthetic protocols, not theorem proofs."""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = 'frontiers/remainder_rate_20260930'
WORKFLOW = ROOT / '.github/workflows/remainder-rate.yml'
HELPER = ROOT / 'tools/remainder_rate_replay.py'
STAGES = ('baseline', 'M1', 'M2', 'M3', 'M4', 'M9')
# Independently measured native reports, not imported from the production helper.
BASELINE = {'checks': {'E1_exponent_ledger': {'info': {'grid_points': 208, 'relative_exponents': {'v1': '1/2', 'v1.1': '7/12'}, 'twelfth_power_points': 4, 'v1': {'rate': '1/6', 'theta': '1/6'}, 'v1.1': {'rate': '1/4', 'theta': '1/12'}}, 'passed': True}, 'E2_barrier_arithmetic': {'info': {'barrier_cases': 48, 'solved_form_points': 4}, 'passed': True}, 'E3_soft_eigenvalue_determinant': {'info': {'matrices': 5, 'sizes': [2, 3, 4]}, 'passed': True}, 'E4_integrals_and_cutoff_ledger': {'info': {'cutoff_ledger_points': 3, 'integral_points': 3, 'window_integral_points': 3}, 'passed': True}, 'E5_sign_window': {'info': {'exact_equality_cases': 0, 'near_boundary_case': True, 'same_sign_instances': 13858, 'typed_instances': 15962}, 'passed': True}}, 'mutant': None, 'object': 'CL-D2-REMAINDER-RATE-20260930-v1.1', 'passed': True, 'scientific_effect': 'NONE'}
MUTATIONS = {'M1': ('E1_exponent_ledger', {'info': 'v1.1 ledger minimum at theta = 1/12 is 1/4, not the claimed rate 1/3', 'passed': False}), 'M2': ('E2_barrier_arithmetic', {'info': 'cubic term not dominated at t = 3/25 (lambda 1/5, K 3)', 'passed': False}), 'M3': ('E3_soft_eigenvalue_determinant', {'info': "det <= lambda_min lambda_max^(d-1) fails (spectrum ['1/100', '2'])", 'passed': False}), 'M4': ('E5_sign_window', {'info': '|det K_i| bound fails at (Fraction(0, 1), Fraction(-2, 1), Fraction(-3, 1), Fraction(1, 3), Fraction(-2, 5), Fraction(1, 10))', 'passed': False})}
REPORTS = {'baseline': BASELINE}
for name, (check, value) in MUTATIONS.items():
    report = copy.deepcopy(BASELINE)
    report['mutant'] = name
    report['passed'] = False
    report['checks'][check] = value
    REPORTS[name] = report


def replay_shell(text):
    marker = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(marker) != 1:
        raise ValueError('exactly one original replay step required')
    tail = text.split(marker, 1)[1].split('        run: |\n', 1)[1]
    lines = []
    for line in tail.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    if not lines or lines[0] != 'set -euo pipefail':
        raise ValueError('strict shell missing')
    return '\n'.join(lines) + '\n'


def identity(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()}


def checker_source():
    # This child never imports production validation or learns its own oracle.
    return 'import json, os, sys\nfrom pathlib import Path\nreports = ' + repr(REPORTS) + r'''
a = sys.argv[1:]
name = 'baseline' if not a else a[1] if len(a) == 2 and a[0] == '--mutant' else 'BAD'
if name not in ('baseline', 'M1', 'M2', 'M3', 'M4', 'M9'):
    raise RuntimeError('unexpected command inventory')
mode = sys.flags.optimize
with open(os.environ['REMAINDER_TRACE'], 'a') as f:
    f.write(json.dumps([mode, name])+'\n')
code = 0 if name == 'baseline' else 2 if name == 'M9' else 1
out = b'' if name == 'M9' else (json.dumps(reports[name], indent=1, sort_keys=True)+'\n').encode()
err = b'unknown mutant label\n' if name == 'M9' else b''
if os.environ['REMAINDER_CASE'] == 'dirty':
    Path(os.environ['REMAINDER_RESULTS']).write_text('changed after preflight\n')
if name == os.environ['REMAINDER_STAGE'] and mode == int(os.environ['REMAINDER_MODE']):
    case = os.environ['REMAINDER_CASE']
    if case == 'crash': raise RuntimeError('unrelated synthetic crash')
    if case == 'silent': out = b''; err = b''
    elif case == 'garbage': out = b'not the intended report\n'
    elif case == 'stderr': err += b'unrelated stderr\n'
    elif case == 'wrong-exit': code = 0 if name != 'baseline' else 1
    elif case == 'signal': os.kill(os.getpid(), 15)
    elif case == 'unknown-wrong': err = b'an unrelated error\n'
    elif case == 'unknown-extra': out = b'not empty\n'
    elif case == 'unknown-prefix': err = b'prefix unknown mutant label\n'
    elif case == 'formatted': out = (' \n'+json.dumps(reports[name], indent=3)+' \n').encode()
    elif name != 'M9':
        row = reports[name]
        if case == 'wrong-reason':
            for v in row['checks'].values():
                if v['passed'] is False: v['info'] = 'unrelated reason'
        elif case == 'wrong-mutant': row['mutant'] = 'M4' if name != 'M4' else 'M1'
        elif case == 'integer-bool': row['passed'] = int(row['passed'])
        elif case == 'nested-bool': row['checks']['E4_integrals_and_cutoff_ledger']['passed'] = 1
        elif case == 'nested-float': row['checks']['E4_integrals_and_cutoff_ledger']['info']['integral_points'] = 3.0
        elif case == 'wrong-positive-info': row['checks']['E4_integrals_and_cutoff_ledger']['info']['integral_points'] = 4
        elif case == 'missing': del row['checks']['E4_integrals_and_cutoff_ledger']
        elif case == 'extra': row['checks']['extra'] = {'passed': True}
        elif case == 'wrong-object': row['object'] = 'UNRELATED'
        elif case == 'array': row = [row]
        out = (json.dumps(row, indent=1, sort_keys=True)+'\n').encode()
        if case == 'duplicate': out = out.rstrip()[:-1] + b',"passed":false}\n'
        elif case == 'nonfinite': out = out.replace(b'15962', b'NaN')
        elif case == 'trailing': out += b'{}\n'
        elif case == 'bad-utf8': out = b'\xff'+out
sys.stdout.buffer.write(out);sys.stderr.buffer.write(err);sys.exit(code)
'''


class RemainderWorkflowTests(unittest.TestCase):
    def run_case(self, case='valid', stage='baseline', mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix='remainder-fixture-') as tmp:
            home = Path(tmp); repo = home/'repo'; repo.mkdir()
            packet = repo/PACKET; packet.mkdir(parents=True)
            trace = home/'calls.jsonl'
            (packet/'rate_ledger_check.py').write_text(checker_source())
            (packet/'RESULTS.json').write_text(json.dumps(BASELINE, indent=1, sort_keys=True)+'\n')
            records = {}
            for name in ('consumed', 'cited_only', 'consumed_unmerged'):
                data = ('synthetic pinned '+name+'\n').encode()
                (repo/(name+'.txt')).write_bytes(data)
                records[name] = [identity(name+'.txt',data)]
            records.update(files=[identity(x.name,x.read_bytes()) for x in sorted(packet.iterdir())],
                           mutants=['M1','M2','M3','M4'])
            (packet/'SOURCES.json').write_text(json.dumps(records))
            if HELPER.exists():
                (repo/'tools').mkdir();shutil.copyfile(HELPER,repo/'tools'/HELPER.name)
            env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home),GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,
                GIT_AUTHOR_NAME='Fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',
                GIT_COMMITTER_NAME='Fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid',
                PYTHONDONTWRITEBYTECODE='1',REMAINDER_TRACE=str(trace),REMAINDER_CASE=case,
                REMAINDER_STAGE=stage,REMAINDER_MODE=str(mode),REMAINDER_RESULTS=str(packet/'RESULTS.json'))
            env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
            for args in (['init','-q'],['config','core.hooksPath',os.devnull],
                         ['config','commit.gpgsign','false'],['config','maintenance.auto','false'],
                         ['config','gc.auto','0'],['add','.'],['commit','-qm','synthetic controls']):
                subprocess.run(['git',*args],cwd=repo,env=env,capture_output=True,check=True,timeout=15)
            if guard == 'source':
                with (packet/'rate_ledger_check.py').open('a') as f:f.write('\n# altered source\n')
            elif guard in ('consumed','cited_only','consumed_unmerged'):
                (repo/(guard+'.txt')).write_bytes(b'changed pin\n')
            elif guard == 'extra': (packet/'extra.txt').write_bytes(b'extra')
            elif guard == 'missing': (packet/'RESULTS.json').unlink()
            elif guard == 'symlink':
                shutil.copyfile(packet/'RESULTS.json',home/'target');(packet/'RESULTS.json').unlink()
                (packet/'RESULTS.json').symlink_to(home/'target')
            elif guard == 'mutant-inventory':
                records['mutants']=['M1','M2','M3'];(packet/'SOURCES.json').write_text(json.dumps(records))
                subprocess.run(['git','add','.'],cwd=repo,env=env,check=True,capture_output=True,timeout=15)
                subprocess.run(['git','commit','-qm','coherent inventory variant'],cwd=repo,env=env,check=True,capture_output=True,timeout=15)
            result=subprocess.run(['bash','--noprofile','--norc','-c',replay_shell(WORKFLOW.read_text())],
                                  cwd=repo,env=env,capture_output=True,timeout=20)
            calls=[json.loads(x) for x in trace.read_text().splitlines()] if trace.exists() else []
            if saved:=os.environ.get('REMAINDER_SAVE'):
                dest=Path(saved)/(case+'-'+stage+'-'+str(mode)+'-'+str(guard));dest.mkdir(parents=True,exist_ok=True)
                (dest/'stdout').write_bytes(result.stdout);(dest/'stderr').write_bytes(result.stderr)
                (dest/'record.json').write_text(json.dumps({'case':case,'stage':stage,'mode':mode,
                    'guard':guard,'returncode':result.returncode,'calls':calls},sort_keys=True)+'\n')
            return result,calls

    def reject_at(self, case, stage, mode):
        result,calls=self.run_case(case,stage,mode)
        order=[[m,s] for m in (0,1) for s in STAGES]
        end=order.index([mode,stage])+1
        self.assertIn([mode,stage],calls,'intended stage not reached')
        self.assertNotEqual(result.returncode,0,'invalid admission: '+repr((case,stage,mode)))
        self.assertEqual(calls,order[:end],'rejection must stop at the intended stage')

    def test_valid_full_inventory(self):
        result,calls=self.run_case()
        self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
        self.assertEqual(calls,[[m,s] for m in (0,1) for s in STAGES])

    def test_each_mutant_reason_crash_and_silence(self):
        for case in ('wrong-reason','crash','silent','stderr','garbage','wrong-mutant'):
            for mode in (0,1):
                for stage in STAGES[1:5]:
                    with self.subTest(case=case,mode=mode,stage=stage):self.reject_at(case,stage,mode)

    def test_complete_nested_json_contract(self):
        for case in ('integer-bool','nested-bool','nested-float','wrong-positive-info',
                     'missing','extra','wrong-object','array','duplicate','nonfinite','trailing','bad-utf8'):
            for mode in (0,1):
                with self.subTest(case=case,mode=mode):self.reject_at(case,'M1',mode)

    def test_baseline_exact_bytes_exit_and_stderr(self):
        for case in ('silent','garbage','stderr','wrong-exit','formatted'):
            for mode in (0,1):
                with self.subTest(case=case,mode=mode):self.reject_at(case,'baseline',mode)

    def test_unknown_label_exact_contract(self):
        for case in ('silent','unknown-wrong','unknown-extra','unknown-prefix','wrong-exit','signal'):
            for mode in (0,1):
                with self.subTest(case=case,mode=mode):self.reject_at(case,'M9',mode)

    def test_mutant_formatting_and_wrong_exits(self):
        for mode in (0,1):
            for stage in STAGES[1:5]:
                with self.subTest(mode=mode,stage=stage):
                    result,calls=self.run_case('formatted',stage,mode)
                    self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
                    self.assertEqual(calls,[[m,s]for m in (0,1)for s in STAGES])
                    self.reject_at('wrong-exit',stage,mode)

    def test_guards_stop_before_replay(self):
        for guard in ('source','consumed','cited_only','consumed_unmerged','extra','missing','symlink'):
            with self.subTest(guard=guard):
                result,calls=self.run_case(guard=guard)
                self.assertNotEqual(result.returncode,0);self.assertEqual(calls,[])

    def test_full_mutant_inventory_required(self):
        result,calls=self.run_case(guard='mutant-inventory')
        self.assertNotEqual(result.returncode,0);self.assertEqual(calls,[])

    def test_tracked_mutation_fails_postflight(self):
        result,calls=self.run_case('dirty')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(calls,[[m,s]for m in (0,1)for s in STAGES])
        self.assertIn(b'changed after preflight',result.stdout)

    def test_regression_is_wired_in_both_modes(self):
        text=WORKFLOW.read_text()
        for path in ('tools/remainder_rate_replay.py','tests/test_remainder_rate_workflow.py'):
            self.assertIn("- '"+path+"'",text)
        for flags in ('-B -S','-B -O -S'):
            self.assertIn('python '+flags+' -m unittest discover -s tests -p test_remainder_rate_workflow.py -v',text)


if __name__ == '__main__':
    unittest.main()
