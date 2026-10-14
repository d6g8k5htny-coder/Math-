"""Real-process contract regressions; synthetic packets are not mathematical evidence."""
import ast
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / 'frontiers/fixed_r_inverse_lifetime_20260930/verify.py'
MUTANTS = (
    'lose-determinant-weight', 'wrong-cubic-power', 'wrong-soft-direction',
    'admit-critical-inverse', 'drop-endpoint-margin', 'unconditional-tail-shortcut',
)
REASONS = (
    'retain original maximum determinant weight', 'cubic lifetime scale',
    'correct Schur soft direction', 'critical inverse moment diverges',
    'strict endpoint above birth', 'retain weighted near-zero eigenvalue integral',
)
UNKNOWN = (
    'usage: inverse.py [-h] [--mutant {' + ','.join(MUTANTS) + '}]\n'
    "inverse.py: error: argument --mutant: invalid choice: 'unknown' (choose from "
    + ', '.join(MUTANTS) + ')\n'
).encode()
STAGES = [(mode, label) for mode in ('normal', 'optimized')
          for label in ('baseline', *MUTANTS, 'unknown')]
RECORDS = []  # In-process inspection only; no audit files written in the checkout.


def entry(path, data, **extra):
    return dict(path=path, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                git_blob=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
                **extra)


CHECKER = r'''
import json,sys
from pathlib import Path
mode='optimized' if sys.flags.optimize else 'normal'
label='baseline' if len(sys.argv)==1 else sys.argv[2]
trace=Path(__file__).parent.parent/'children.jsonl'
with trace.open('a') as f:f.write(json.dumps([mode,label])+'\n')
exitcode=0 if label=='baseline' else 2 if label=='unknown' else 1
out=b'{"fixture":true}\n' if label=='baseline' else b''
err=UNKNOWN if label=='unknown' else b''
if label in MUTANTS:
    out=json.dumps({'error':REASONS[MUTANTS.index(label)],'passed':False}).encode()+b'\n'
if (mode,label)==TARGET:
    if CASE=='crash':raise RuntimeError('synthetic unrelated crash')
    if CASE=='silent':out=err=b''
    if CASE=='wrong-reason':out=b'{"error":"other failure","passed":false}\n'
    if CASE=='extra-key':out=out.rstrip()[:-1]+b',"extra":true}\n'
    if CASE=='passed-int':out=out.replace(b'false',b'0')
    if CASE=='passed-null':out=out.replace(b'false',b'null')
    if CASE=='passed-true':out=out.replace(b'false',b'true')
    if CASE=='duplicate-key':out=out.rstrip()[:-1]+b',"passed":false}\n'
    if CASE=='nan':out=out.rstrip()[:-1]+b',"extra":NaN}\n'
    if CASE=='trailing':out+=b'{}'
    if CASE=='stderr':err+=b'unexpected stderr\n'
    if CASE=='wrong-exit':exitcode=0 if label!='baseline' else 1
    if CASE=='wrong-exit-two':exitcode=2
    if CASE=='unknown-reason':err=b'inverse.py: error: unrelated failure\n'
    if CASE=='unknown-stdout':out=b'unexpected stdout\n'
    if CASE=='unknown-extra':err+=b'additional diagnostic\n'
    if CASE=='unknown-choices':err=err.replace(b'wrong-cubic-power',b'other-choice')
    if CASE=='unknown-wrapping':err=b' \n '.join(err.split())+b'\n'
    if CASE in ('unknown-quoted','unknown-quoted-wrong'):
        err=err.replace((', '.join(MUTANTS)).encode(),(', '.join(repr(s) for s in MUTANTS)).encode())
        if CASE=='unknown-quoted-wrong':err=err.replace(b'wrong-cubic-power',b'other-choice')
    if CASE=='json-format':out=json.dumps(json.loads(out),sort_keys=True,indent=3).encode()+b'\n'
    if CASE=='baseline-changed':out=b'{"fixture":false}\n'
    if CASE=='dirty-end':(Path(__file__).parent/'extra').write_text('not in manifest')
sys.stdout.buffer.write(out);sys.stderr.buffer.write(err);raise SystemExit(exitcode)
'''
SUITE = r'''
import sys,unittest
from pathlib import Path
class Probe(unittest.TestCase):
    def test_live_suite(self):
        with (Path(__file__).parent.parent/'suites.txt').open('a') as f:
            f.write(('optimized' if sys.flags.optimize else 'normal')+'\n')
        self.assertFalse(FAIL_SUITE,'intended synthetic test-suite failure')
'''


def run_case(case='valid', mode='normal', label='baseline', guard=None, inventory=None):
    """Run the complete verifier, including real historical Git reads and source guards."""
    with tempfile.TemporaryDirectory(prefix='fixed-r-protocol-') as td:
        repo=Path(td); packet=repo/'packet'; packet.mkdir()
        env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                   PYTHONDONTWRITEBYTECODE='1', LC_ALL='C.UTF-8')
        def git(*args):
            return subprocess.run(['git','-c','user.name=Fixture',
                '-c','user.email=fixture@example.invalid','-c','maintenance.auto=false',
                '-c','commit.gpgsign=false',*args],cwd=repo,env=env,
                capture_output=True,check=True,timeout=15).stdout
        git('init','-q'); parent=b'synthetic historical model\n'
        (repo/'P.md').write_bytes(parent);git('add','P.md');git('commit','-qm','synthetic parent')
        sha=git('rev-parse','HEAD').decode().strip()
        source=entry('P.md',parent,id='P',commit=sha)
        if guard=='source-hash':source['sha256']='0'*64
        if guard=='source-path':source['path']='../P.md'
        if guard=='source-noncommit':source['commit']=git('rev-parse','HEAD^{tree}').decode().strip()
        es=[] if guard=='source-empty' else [source]
        text=VERIFY.read_text()
        if inventory is not None:
            tree=ast.parse(text)
            node=next(n for n in tree.body if isinstance(n,ast.Assign)
                and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets))
            lines=text.splitlines(keepends=True)
            text=''.join(lines[:node.lineno-1])+f'MUTANTS={inventory!r}\n'+''.join(lines[node.end_lineno:])
        (packet/'verify.py').write_text(text)
        header=f'MUTANTS={MUTANTS!r}\nREASONS={REASONS!r}\nUNKNOWN={UNKNOWN!r}\nTARGET={(mode,label)!r}\nCASE={case!r}\n'
        (packet/'inverse.py').write_text(header+CHECKER)
        (packet/'test_fixture.py').write_text(f'FAIL_SUITE={guard=="suite-fail"!r}\n'+SUITE)
        (packet/'RESULTS.json').write_bytes(b'{"fixture":true}\n')
        (packet/'SOURCES.json').write_text(json.dumps({'sources':es}))
        manifest={'files':[entry(p.name,p.read_bytes()) for p in sorted(packet.iterdir())]}
        (packet/'MANIFEST.json').write_text(json.dumps(manifest))
        if guard=='payload-change':(packet/'inverse.py').write_text('changed')
        if guard=='packet-extra':(packet/'extra').write_text('extra')
        if guard=='packet-duplicate':
            manifest['files'].append(manifest['files'][0]);(packet/'MANIFEST.json').write_text(json.dumps(manifest))
        if guard=='manifest-duplicate-key':(packet/'MANIFEST.json').write_text('{"files":[],"files":[]}')
        flags=['-B','-S']+(['-O'] if sys.flags.optimize else [])
        proc=subprocess.run([sys.executable,*flags,str(packet/'verify.py')],cwd=repo,
                            env=env,capture_output=True,timeout=30)
        trace=repo/'children.jsonl'; suites=repo/'suites.txt'
        seen=[tuple(json.loads(s)) for s in trace.read_text().splitlines()] if trace.exists() else []
        suite_seen=suites.read_text().splitlines() if suites.exists() else []
        RECORDS.append({'case':case,'target':[mode,label],'guard':guard,
            'inventory':inventory,'returncode':proc.returncode,'children':seen,'suites':suite_seen,
            'stdout':proc.stdout.decode(errors='backslashreplace'),
            'stderr':proc.stderr.decode(errors='backslashreplace')})
        return proc,seen,suite_seen


class FixedRProtocolTests(unittest.TestCase):
    def check_many(self, cases):
        # Independent disposable roots; assertions are reported by the parent thread.
        cases=list(cases)
        with ThreadPoolExecutor(max_workers=4) as pool:
            jobs=[pool.submit(self.assert_case,*case) for case in cases]
            for case,job in zip(cases,jobs):
                with self.subTest(case=case):job.result()

    def assert_case(self,case,mode,label,accepted=False):
        proc,seen,suites=run_case(case,mode,label)
        want=STAGES if accepted or case=='dirty-end' else STAGES[:STAGES.index((mode,label))+1]
        if accepted:
            self.assertEqual(proc.returncode,0,proc.stderr.decode())
            record=json.loads(proc.stdout)
            self.assertIs(record['passed'],True);self.assertEqual(record['source_count'],1)
            self.assertIs(record['source_pins_checked'],True)
            self.assertIs(record['mathematical_acceptance'],False)
        else:self.assertNotEqual(proc.returncode,0,'unrelated/invalid child response was admitted')
        self.assertEqual(seen,want,'verifier must stop at the actual failing stage')
        self.assertEqual(suites,['normal'] if len(want)<=8 else ['normal','optimized'])

    def test_dedicated_workflow_wiring(self):
        text=(ROOT/'.github/workflows/fixed-r-inverse-lifetime.yml').read_text()
        self.assertIn("      - 'tests/test_fixed_r_replay_protocol.py'",text)
        for flags in ('-B -S','-B -O -S'):
            self.assertIn('python '+flags+' tests/test_fixed_r_replay_protocol.py',text)
        self.assertIn('python -B -S frontiers/fixed_r_inverse_lifetime_20260930/verify.py',text)
        self.assertIn('git fetch --no-tags origin 7a1cb09a9d58d179393e6d29146252f714b9c9bf',text)

    def test_valid_and_formatting(self):
        self.assert_case('valid','normal','baseline',True)
        for mode in ('normal','optimized'):
            self.assert_case('json-format',mode,MUTANTS[0],True)
            self.assert_case('unknown-wrapping',mode,'unknown',True)

    def test_every_mutant_rejects_unrelated_failure(self):
        self.check_many((case,mode,label) for mode in ('normal','optimized')
            for label in MUTANTS for case in ('crash','silent','wrong-reason'))

    def test_strict_complete_json_and_exit(self):
        self.check_many((case,mode,MUTANTS[1]) for mode in ('normal','optimized')
            for case in ('extra-key','passed-int','passed-null','passed-true','duplicate-key',
                         'nan','trailing','stderr','wrong-exit','wrong-exit-two'))

    def test_unknown_contract(self):
        self.check_many((case,mode,'unknown') for mode in ('normal','optimized')
            for case in ('silent','unknown-reason','unknown-stdout','unknown-extra','unknown-choices','wrong-exit'))

    def test_pinned_and_local_argparse_forms(self):
        self.check_many((case,mode,'unknown',case=='unknown-quoted')
            for mode in ('normal','optimized') for case in ('unknown-quoted','unknown-quoted-wrong'))

    def test_baseline_and_final_inventory(self):
        for mode in ('normal','optimized'):
            for case in ('stderr','baseline-changed','wrong-exit'):
                with self.subTest(mode=mode,case=case):self.assert_case(case,mode,'baseline')
        self.assert_case('dirty-end','optimized','unknown')

    def test_preflight_source_guards_and_suite_failure(self):
        for guard in ('source-hash','source-path','source-noncommit','source-empty','payload-change',
                      'packet-extra','packet-duplicate','manifest-duplicate-key','suite-fail'):
            with self.subTest(guard=guard):
                proc,seen,suites=run_case(guard=guard)
                self.assertNotEqual(proc.returncode,0);self.assertEqual(seen,[])
                self.assertEqual(suites,['normal'] if guard=='suite-fail' else [])

    def test_mutant_inventory_is_complete_before_execution(self):
        for inv in (MUTANTS[1:],MUTANTS+(MUTANTS[0],),tuple(reversed(MUTANTS))):
            with self.subTest(inventory=inv):
                proc,seen,suites=run_case(inventory=inv)
                self.assertNotEqual(proc.returncode,0,'incomplete/duplicated/reordered inventory admitted')
                self.assertEqual(seen,[]);self.assertEqual(suites,[])


if __name__=='__main__':unittest.main()
