"""Real full-shell C6 numerical workflow contracts; fixtures are not mathematics."""
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
WORKFLOW = ROOT / '.github/workflows/c6-cluster-coefficients-numerics.yml'
HELPER = ROOT / 'tools/c6_coefficient_numerics_replay.py'
PACKET = 'frontiers/c6_cluster_coefficients_numerics_20260930'
STAGES = ('baseline', 'cubic-sign', 'antiderivative', 'typed-boundary')
REPORTS = {
    'baseline': {'mode': 'check', 'passed': True, 'scientific_effect': 'NONE'},
    'cubic-sign': {'error': 'classifier agrees with the direct critical-point count on the typed domain', 'passed': False},
    'antiderivative': {'error': '[LM] cubic mass 48 k^5 on n = 2', 'passed': False},
    'typed-boundary': {'error': 'classifier agrees with the direct critical-point count on the typed domain', 'passed': False},
}


def replay_shell(text):
    """Extract only the actual replay step, not its preceding test invocation."""
    marker = '      - name: Verify manifest and main-resident pins, replay exact controls and GH40, reject mutants\n'
    if text.count(marker) != 1:
        raise ValueError('expected one named replay step')
    tail = text.split(marker, 1)[1].split('        run: |\n', 1)[1]
    lines = []
    for line in tail.splitlines():
        if line and not line.startswith('          '):
            break
        lines.append(line[10:] if line else '')
    if not lines or lines[0] != 'set -euo pipefail':
        raise ValueError('strict replay shell missing')
    return '\n'.join(lines) + '\n'


def identity(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def fixture_script():
    # The fixture emits independently specified reports. The production helper is
    # never imported here, so a broken helper cannot define its own oracle.
    return '''import json, os, sys
from pathlib import Path
reports = ''' + repr(REPORTS) + '''
a = sys.argv[1:]
if not a or a[0] != '--check': raise RuntimeError('unsafe/non-check invocation')
name = a[2] if len(a) == 3 and a[1] == '--mutant' else 'baseline'
if a != (['--check'] if name == 'baseline' else ['--check','--mutant',name]):
    raise RuntimeError('unexpected invocation')
mode = sys.flags.optimize
with open(os.environ['C6NUM_TEST_TRACE'], 'a') as f:
    f.write(json.dumps([mode, name])+'\\n')
row = dict(reports[name]); code = 0 if name == 'baseline' else 1
out = (json.dumps(row, sort_keys=True)+'\\n').encode(); err = b''
if os.environ['C6NUM_TEST_CASE'] == 'dirty':
    Path('RESULTS.json').write_text('changed after preflight\\n')
if mode == int(os.environ['C6NUM_TEST_MODE']) and name == os.environ['C6NUM_TEST_STAGE']:
    case = os.environ['C6NUM_TEST_CASE']
    if case == 'crash': raise RuntimeError('unrelated synthetic crash')
    if case == 'silent': out = b''
    elif case == 'garbage': out = b'unrelated failure\\n'
    elif case == 'stderr': err = b'unexpected stderr\\n'
    elif case == 'wrong-exit': code = 1 if name == 'baseline' else 0
    elif case == 'signalled': os.kill(os.getpid(), 15)
    elif case == 'wrong-report': row = {'passed': not row['passed'], 'error':'unrelated'}
    elif case == 'wrong-reason': row['error'] = 'unrelated mathematical check'
    elif case == 'wrong-effect': row['scientific_effect'] = 'ACCEPT'
    elif case == 'wrong-mode': row['mode'] = 'full'
    elif case == 'integer-bool': row['passed'] = int(row['passed'])
    elif case == 'float-bool': row['passed'] = float(row['passed'])
    elif case == 'null-bool': row['passed'] = None
    elif case == 'missing': del row['passed']
    elif case == 'extra': row['extra'] = 'not in measured report'
    elif case == 'array': row = [row]
    if case in ('wrong-report','wrong-reason','wrong-effect','wrong-mode',
                'integer-bool','float-bool','null-bool','missing','extra','array'):
        out = (json.dumps(row, sort_keys=True)+'\\n').encode()
    if case == 'duplicate':
        out = out.rstrip()[:-1] + b', "passed": false}\\n'
    elif case == 'trailing': out += b'{}\\n'
    elif case == 'nonfinite': out = out.replace(b'false', b'NaN').replace(b'true', b'Infinity')
    elif case == 'bad-utf8': out = b'\\xff'+out
    elif case == 'formatted': out = (' \\n'+json.dumps(row, indent=4)+' \\n').encode()
sys.stdout.buffer.write(out); sys.stderr.buffer.write(err); sys.exit(code)
'''


class WorkflowContractTests(unittest.TestCase):
    def run_case(self, case='valid', stage='baseline', mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix='c6num-test-') as tmp:
            home = Path(tmp); repo = home/'repo'; repo.mkdir()
            packet = repo/PACKET; packet.mkdir(parents=True)
            trace = home/'trace.jsonl'
            (packet/'coefficients.py').write_text(fixture_script())
            (packet/'RESULTS.json').write_text('{}\n')
            consumed = repo/'consumed.txt'; consumed.write_bytes(b'fixed synthetic upstream\n')
            pin = identity('consumed.txt', consumed.read_bytes())
            pin.update(current_required=True, git_blob=hashlib.sha1(
                b'blob %d\0'%len(consumed.read_bytes())+consumed.read_bytes()).hexdigest())
            (packet/'SOURCE_MAP.json').write_text(json.dumps({'sources':[pin]}))
            manifest = [identity(p.name, p.read_bytes()) for p in sorted(packet.iterdir())]
            (packet/'SOURCE_FILES.json').write_text(json.dumps({'files':manifest}))
            if HELPER.exists():
                (repo/'tools').mkdir(); shutil.copyfile(HELPER, repo/'tools'/HELPER.name)
            # Isolate every real synthetic Git repo from user signing/hooks and
            # asynchronous maintenance; do not suppress postflight or cleanup.
            env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                       GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid',
                       PYTHONDONTWRITEBYTECODE='1', C6NUM_TEST_TRACE=str(trace),
                       C6NUM_TEST_CASE=case, C6NUM_TEST_STAGE=stage, C6NUM_TEST_MODE=str(mode))
            env['PATH'] = str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
            for args in (['init','-q'], ['config','gc.auto','0'], ['config','maintenance.auto','false'],
                         ['config','core.hooksPath',os.devnull], ['config','commit.gpgsign','false'],
                         ['add','.'], ['commit','-q','-m','synthetic fixture']):
                subprocess.run(['git',*args],cwd=repo,env=env,capture_output=True,check=True,timeout=20)
            if guard == 'source':
                (packet/'coefficients.py').write_text(fixture_script()+'\n# tamper\n')
            elif guard == 'pin': consumed.write_bytes(b'wrong upstream\n')
            elif guard == 'extra': (packet/'extra.txt').write_text('unexpected')
            elif guard == 'missing': (packet/'RESULTS.json').unlink()
            elif guard == 'symlink':
                target = home/'RESULTS.json'; shutil.copyfile(packet/'RESULTS.json',target)
                (packet/'RESULTS.json').unlink();(packet/'RESULTS.json').symlink_to(target)
            elif guard == 'nested':
                source = packet/'RESULTS.json'; (packet/'subdir').mkdir();source.rename(packet/'subdir/RESULTS.json')
                for row in manifest:
                    if row['path']=='RESULTS.json': row['path']='subdir/RESULTS.json'
                (packet/'SOURCE_FILES.json').write_text(json.dumps({'files':manifest}))
            shell = replay_shell(WORKFLOW.read_text())
            result = subprocess.run(['bash','--noprofile','--norc','-c',shell],cwd=repo,env=env,
                                    capture_output=True,timeout=30)
            calls = [json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else []
            saved = os.environ.get('C6NUM_TEST_SAVE')
            if saved:
                dest=Path(saved)/(case+'-'+stage+'-'+str(mode)+'-'+str(guard));dest.mkdir(parents=True,exist_ok=True)
                (dest/'stdout').write_bytes(result.stdout);(dest/'stderr').write_bytes(result.stderr)
                (dest/'result.json').write_text(json.dumps({'case':case,'stage':stage,'mode':mode,'guard':guard,
                    'returncode':result.returncode,'calls':calls},sort_keys=True)+'\n')
            return result, calls

    def rejected(self, case, stage, mode):
        result,calls=self.run_case(case,stage,mode)
        target=[mode,stage]
        self.assertIn(target,calls, 'target never reached: '+result.stderr.decode(errors='replace'))
        self.assertEqual(calls.count(target),1)
        self.assertNotEqual(result.returncode,0,'invalid report admitted: '+repr((case,stage,mode,calls)))

    def test_valid_complete_inventory(self):
        result,calls=self.run_case()
        self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
        self.assertEqual(calls,[[m,s]for m in(0,1)for s in STAGES])

    def test_harmless_json_formatting(self):
        for mode in(0,1):
            for stage in STAGES:
                with self.subTest(mode=mode,stage=stage):
                    result,calls=self.run_case('formatted',stage,mode)
                    self.assertEqual(result.returncode,0,result.stderr.decode(errors='replace'))
                    self.assertEqual(len(calls),8)

    def test_silent_and_garbage_reports(self):
        for case in('silent','garbage'):
            for mode in(0,1):
                for stage in STAGES:
                    with self.subTest(case=case,mode=mode,stage=stage):self.rejected(case,stage,mode)

    def test_wrong_reports_and_reasons(self):
        for mode in(0,1):
            for stage in STAGES:
                with self.subTest(mode=mode,stage=stage):self.rejected('wrong-report',stage,mode)
            for stage in STAGES[1:]:
                with self.subTest(reason=stage,mode=mode):self.rejected('wrong-reason',stage,mode)
            for case in('wrong-effect','wrong-mode'):
                with self.subTest(case=case,mode=mode):self.rejected(case,'baseline',mode)

    def test_exact_boolean_types(self):
        for case in('integer-bool','float-bool','null-bool'):
            for mode in(0,1):
                for stage in STAGES:
                    with self.subTest(case=case,mode=mode,stage=stage):self.rejected(case,stage,mode)

    def test_duplicate_nonfinite_and_trailing_json(self):
        for case in('duplicate','nonfinite','trailing','bad-utf8'):
            for mode in(0,1):
                for stage in('baseline','antiderivative'):
                    with self.subTest(case=case,mode=mode,stage=stage):self.rejected(case,stage,mode)

    def test_complete_shape(self):
        for case in('missing','extra','array'):
            for mode in(0,1):
                for stage in('baseline','typed-boundary'):
                    with self.subTest(case=case,mode=mode,stage=stage):self.rejected(case,stage,mode)

    def test_stderr_is_not_ignored(self):
        for mode in(0,1):
            for stage in STAGES:
                with self.subTest(mode=mode,stage=stage):self.rejected('stderr',stage,mode)

    def test_runtime_crash_is_not_intended_rejection(self):
        for mode in(0,1):
            for stage in STAGES[1:]:
                with self.subTest(mode=mode,stage=stage):self.rejected('crash',stage,mode)

    def test_wrong_exit_and_signal(self):
        for case in('wrong-exit','signalled'):
            for mode in(0,1):
                for stage in STAGES:
                    with self.subTest(case=case,mode=mode,stage=stage):self.rejected(case,stage,mode)

    def test_source_guards_run_before_children(self):
        for guard in('source','pin','extra','missing','symlink','nested'):
            with self.subTest(guard=guard):
                result,calls=self.run_case(guard=guard)
                self.assertNotEqual(result.returncode,0)
                self.assertEqual(calls,[])

    def test_tracked_mutation_fails_postflight(self):
        result,calls=self.run_case('dirty')
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(len(calls),8)
        self.assertIn(b'changed after preflight',result.stdout)


if __name__ == '__main__':
    unittest.main()
