"""Whole original verification shell, real Git/Bash/Python; numerical child is a fixture.

Frozen report deltas were measured from unchanged checker d521770d at37bd017b
in both Python modes BEFORE the repair. They are not learned from a test child.
Successful remote API retrieval is not simulated or claimed by this suite;
all original remote source checks remain in the executed shell unchanged.
"""
from pathlib import Path
import copy
from concurrent.futures import ThreadPoolExecutor
import threading
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / '.github/workflows/third-order-rate.yml'
PACKET = 'frontiers/third_order_rate_20261001'
MUTANTS = tuple('M'+str(i) for i in range(1, 9))
SEQUENCE = [(mode, m) for mode in (0, 1) for m in ('baseline', *MUTANTS, 'M9')]
BASELINE_SHA = '7f877f034baaa5b7c8a879a76dd2b825e57869478fdc396897cde1da9bf10ade'
# None below deletes the sole obsolete M2 exponent entry; no native delta sets null.
DELTAS = {'M1': [(('checks', 'R1_exponent_ledger', 'candidate_least'), '4/11'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'F: l rho_f^-2 (finite part)'), '5/11'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'F: rho_f^2'), '6/11'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'F: rho_f^5/l (Lemma F layer)'), '4/11'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'K: Lemma C+ r^1 kappa^1'), '5/11'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'K: rho_f^5/l (Lemma O tail)'), '4/11'),
        (('checks', 'R1_exponent_ledger', 'elder_least'), '4/11'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'F: l rho_f^-2 (finite part)'), '5/11'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'F: rho_f^2'), '6/11'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'F: rho_f^5/l (Lemma F layer)'), '4/11'),
        (('checks',
          'R1_exponent_ledger',
          'elder_terms',
          'F: rho_f^5/l (rejected fold mass, [C7-K] (K2))'),
         '4/11'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'K: Lemma CE+ r^1 kappa^1'), '5/11'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'K: Lemma CE+ r^2 kappa^3'), '6/11'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'K: Lemma CE+ r^3/2 kappa^2'), '1/2'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', "K: rho_f^5/l (Lemma O/O' tail)"), '4/11'),
        (('checks', 'R1_exponent_ledger', 'passed'), False),
        (('checks', 'R1_exponent_ledger', 'rho_f'), 'l^3/11'),
        (('mutant',), 'M1'),
        (('passed',), False)],
 'M2': [(('checks', 'R1_exponent_ledger', 'candidate_least'), '2/7'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'K: Lemma C+ r^1 kappa^1'), None),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'K: Lemma C+ r^1 kappa^2'), '2/7'),
        (('checks', 'R1_exponent_ledger', 'passed'), False),
        (('checks', 'R1_exponent_ledger', 'remark1_maxmin', 'drop_linear_cand'), '4/11'),
        (('mutant',), 'M2'),
        (('passed',), False)],
 'M3': [(('checks', 'R2_lemma_L', 'equality_instances'), 41),
        (('checks', 'R2_lemma_L', 'passed'), False),
        (('mutant',), 'M3'),
        (('passed',), False)],
 'M4': [(('checks', 'R3_refined_B4', 'passed'), False), (('mutant',), 'M4'), (('passed',), False)],
 'M5': [(('checks', 'R4_typed_window', 'passed'), False), (('mutant',), 'M5'), (('passed',), False)],
 'M6': [(('checks', 'R1_exponent_ledger', 'a'), 'l^2/15'),
        (('checks', 'R1_exponent_ledger', 'elder_least'), '2/5'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'I: [a,r0*] l^(2/3) a^-2'), '2/5'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'I: [a,r0*] l^(5/3) a^-7'), '11/15'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'I: [rho_c,a] a^4 (log)'), '8/15'),
        (('checks', 'R1_exponent_ledger', 'intermediate_least'), '2/5'),
        (('checks', 'R1_exponent_ledger', 'passed'), False),
        (('mutant',), 'M6'),
        (('passed',), False)],
 'M7': [(('checks', 'R6_C_plus_CE_plus_bookkeeping', 'passed'), False),
        (('mutant',), 'M7'),
        (('passed',), False)],
 'M8': [(('checks', 'R1_exponent_ledger', 'candidate_least'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'J2: rho_c^3'), '3/4'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'J3: l rho_c^-2'), '1/2'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'J3: l^2 rho_c^-7'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'J4: l^2 rho_c^-7'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'K: Lemma C+ r^1 kappa^0'), '1/2'),
        (('checks', 'R1_exponent_ledger', 'candidate_terms', 'K: l^2 rho_c^-7 (upper tail)'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'elder_least'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'I: [rho_c,a] l^3 rho_c^-11 (log)'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'J4: l^2 rho_c^-7'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'K: Lemma CE+ r^1 kappa^0'), '1/2'),
        (('checks', 'R1_exponent_ledger', 'elder_terms', 'K: l^2 rho_c^-7 (upper tail)'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'hypotheses'), False),
        (('checks', 'R1_exponent_ledger', 'intermediate_least'), '1/4'),
        (('checks', 'R1_exponent_ledger', 'passed'), False),
        (('checks', 'R1_exponent_ledger', 'rho_c'), 'l^1/4'),
        (('mutant',), 'M8'),
        (('passed',), False)]}


def identity(path, raw):
    return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest())


def native_reports():
    raw = (ROOT/PACKET/'RESULTS.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != BASELINE_SHA:
        raise ValueError('test reference baseline changed')
    baseline = json.loads(raw)
    reports = {'baseline': raw.decode()}
    for name, changes in DELTAS.items():
        obj = copy.deepcopy(baseline)
        for keys, value in changes:
            node = obj
            for key in keys[:-1]:
                node = node[key]
            if value is None:
                del node[keys[-1]]
            else:
                node[keys[-1]] = value
        reports[name] = json.dumps(obj, indent=1, sort_keys=True)+'\n'
    return reports


def verification_shell():
    # Deliberately restricted to this workflow's uniquely named literal run block.
    text = WORKFLOW.read_text()
    name = '      - name: Verify sources, replay both modes, reject mutants\n'
    if text.count(name) != 1:
        raise ValueError('verification step not unique')
    tail = text.split(name, 1)[1]
    block = tail.split('        run: |\n', 1)[1]
    return ''.join(line[10:] if line.startswith('          ') else line
                   for line in block.splitlines(keepends=True))


def fixture_script(reports):
    return ('import os,sys,json\nfrom pathlib import Path\nREPORTS = '+repr(reports)+'\n'+r"""
m = sys.argv[2] if len(sys.argv)>2 else 'baseline'
mode = int(sys.flags.optimize)
with open(os.environ['TRACE'], 'a') as f:
    f.write(json.dumps([mode,m])+'\n')
out = b'' if m == 'M9' else REPORTS[m].encode()
err = b'unknown mutant label\n' if m == 'M9' else b''
rc = 2 if m == 'M9' else (0 if m == 'baseline' else 1)
case = os.environ['CASE']
if m == os.environ['TARGET'] and mode == int(os.environ['TARGET_MODE']):
    if case == 'crash': raise RuntimeError('unrelated synthetic failure')
    elif case == 'silence': out = err = b''
    elif case == 'stderr': err += b'unexpected warning\n'
    elif case == 'wrong_exit': rc = 0 if m != 'baseline' else 1
    elif case == 'wrong_report': out = REPORTS['M2' if m != 'M2' else 'M1'].encode()
    elif case == 'wrong_baseline': out += b' '
    elif case == 'unknown_reason': err = b'wrong failure reason\n'
    elif case == 'unknown_stdout': out = b'noise\n'
    elif case == 'unknown_exit': rc = 1
    else:
        obj = json.loads(out)
        if case == 'format':
            out = (' \n'+json.dumps(obj,ensure_ascii=False,sort_keys=False)+' \n').encode()
        elif case == 'duplicate': out = out.replace(b'"passed": false', b'"passed": false, "passed": false', 1)
        elif case == 'trailing': out += b'{}'
        elif case == 'nonfinite': out = out.replace(b'"passed": false', b'"passed": NaN', 1)
        elif case == 'float': out = out.replace(b'6108', b'6108.0', 1)
        elif case == 'int_bool':
            obj['passed']=0; out=json.dumps(obj).encode()
        elif case == 'missing':
            del obj['checks']['R5_W_plus_bookkeeping']; out=json.dumps(obj).encode()
        elif case == 'extra':
            obj['extra']=True; out=json.dumps(obj).encode()
        elif case == 'wrong_info':
            obj['checks']['R2_lemma_L']['instances']+=1; out=json.dumps(obj).encode()
        elif case == 'wrong_mutant':
            obj['mutant']='M8'; out=json.dumps(obj).encode()
        elif case == 'not_json': out=b'FAILED some other check\n'
if case == 'dirty' and mode==1 and m=='M9':
    Path('consumed.txt').write_text('changed after preflight\n')
sys.stdout.buffer.write(out);sys.stderr.buffer.write(err);sys.exit(rc)
""")


class ThirdOrderProtocolTests(unittest.TestCase):
    counter = 0
    evidence_lock = threading.Lock()

    def run_case(self, case='valid', target='M1', mode=0, guard=None):
        with tempfile.TemporaryDirectory(prefix='third-order-test-') as tmp:
            home=Path(tmp);repo=home/'repo';repo.mkdir();packet=repo/PACKET;packet.mkdir(parents=True)
            reports=native_reports()
            (packet/'r37_check.py').write_text(fixture_script(reports))
            (packet/'RESULTS.json').write_text(reports['baseline'])
            for name in ('consumed.txt','cited.txt'):
                (repo/name).write_text('fixed '+name+'\n')
            manifest={'files':[identity(p.name,p.read_bytes()) for p in sorted(packet.iterdir())],
                      'mutants':list(MUTANTS),'consumed':[identity('consumed.txt',(repo/'consumed.txt').read_bytes())],
                      'cited_only':[identity('cited.txt',(repo/'cited.txt').read_bytes())],
                      'consumed_unmerged':[],'cited_unmerged':[]}
            if guard=='missing_mutant': manifest['mutants'].pop()
            if guard=='duplicate_mutant': manifest['mutants'].append('M1')
            if guard=='reordered_mutant': manifest['mutants'].reverse()
            (packet/'SOURCES.json').write_text(json.dumps(manifest))
            env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
            env.update(HOME=str(home),XDG_CONFIG_HOME=str(home/'xdg'),GIT_CONFIG_NOSYSTEM='1',
                       PYTHONDONTWRITEBYTECODE='1',GH_TOKEN='synthetic-no-network-token',
                       GH_REPOSITORY='fixture/repo',TRACE=str(home/'trace'),CASE=case,
                       TARGET=target,TARGET_MODE=str(mode))
            for cmd in (['git','init','-q'],['git','add','.'],
                        ['git','-c','user.name=Fixture','-c','user.email=f@example.invalid',
                         '-c','commit.gpgsign=false','commit','-qm','fixture']):
                subprocess.run(cmd,cwd=repo,env=env,capture_output=True,check=True,timeout=15)
            if guard=='packet_tamper': (packet/'r37_check.py').write_text('# changed\n')
            if guard=='packet_missing': (packet/'RESULTS.json').unlink()
            if guard=='packet_extra': (packet/'extra.txt').write_text('extra')
            if guard=='packet_symlink':
                (packet/'r37_check.py').rename(home/'saved.py');(packet/'r37_check.py').symlink_to(home/'saved.py')
            if guard=='consumed_tamper': (repo/'consumed.txt').write_text('changed')
            if guard=='cited_missing': (repo/'cited.txt').unlink()
            if guard=='cited_symlink':
                (repo/'cited.txt').rename(home/'saved.txt');(repo/'cited.txt').symlink_to(home/'saved.txt')
            shell=verification_shell()
            result=subprocess.run(['bash','-c',shell],cwd=repo,env=env,capture_output=True,timeout=45)
            trace=[tuple(json.loads(s)) for s in (home/'trace').read_text().splitlines()] if (home/'trace').exists() else []
            # Optional external evidence is never committed or used to choose an expectation.
            destination=os.environ.get('THIRD_ORDER_TEST_EVIDENCE')
            if destination:
                folder=Path(destination);folder.mkdir(parents=True,exist_ok=True)
                with type(self).evidence_lock:
                    type(self).counter+=1;stem=f'{type(self).counter:04d}'
                meta={'case':case,'target':target,'mode':mode,'guard':guard,
                      'returncode':result.returncode,'trace':trace,
                      'stdout_sha256':hashlib.sha256(result.stdout).hexdigest(),
                      'stderr_sha256':hashlib.sha256(result.stderr).hexdigest()}
                for suffix,raw in [('json',(json.dumps(meta,sort_keys=True)+'\n').encode()),
                                   ('stdout',result.stdout),('stderr',result.stderr)]:
                    with (folder/f'{stem}.{suffix}').open('xb') as f:f.write(raw)
            return result,trace

    def check_cases(self, cases):
        # Each case owns its repo, HOME, process environment and external trace.
        # Parallelism changes only fixture scheduling, not any verifier command.
        with ThreadPoolExecutor(max_workers=4) as pool:
            executions = list(pool.map(lambda c: self.run_case(*c[:3]), cases))
        for (case,target,mode,valid), (p,trace) in zip(cases,executions):
            with self.subTest(case=case,target=target,mode=mode):
                self.assertEqual(p.returncode,0 if valid else 1,(case,target,mode,p.stderr))
                expected=SEQUENCE if valid else SEQUENCE[:SEQUENCE.index((mode,target))+1]
                self.assertEqual(trace,expected,(case,target,mode))
                if valid:
                    self.assertIn(b'"mathematical_acceptance": false',p.stdout)
                    self.assertEqual(p.stderr,b'')

    def test_valid_and_formatting(self):
        self.check_cases([('valid','M1',0,True)]+[
            ('format',target,mode,True) for mode in (0,1) for target in MUTANTS])

    def test_crash_silence_wrong_report_each_mutant(self):
        self.check_cases([(case,target,mode,False) for mode in (0,1)
                          for target in MUTANTS for case in ('crash','silence','wrong_report')])

    def test_stderr_and_exit_each_mutant(self):
        self.check_cases([(case,target,mode,False) for mode in (0,1)
                          for target in MUTANTS for case in ('stderr','wrong_exit')])

    def test_complete_typed_report_and_json(self):
        self.check_cases([(case,'M1',mode,False) for mode in (0,1)
                          for case in ('duplicate','trailing','nonfinite','float','int_bool',
                                       'missing','extra','wrong_info','wrong_mutant','not_json')])

    def test_baseline_exact_exit_stdout_and_stderr(self):
        self.check_cases([(case,'baseline',mode,False) for mode in (0,1)
                          for case in ('stderr','wrong_exit','wrong_baseline','silence')])

    def test_unknown_exact_contract(self):
        self.check_cases([(case,'M9',mode,False) for mode in (0,1)
                          for case in ('silence','unknown_reason','unknown_stdout','unknown_exit','stderr')])

    def test_source_guards_before_children(self):
        for guard in ('packet_tamper','packet_missing','packet_extra','packet_symlink',
                      'consumed_tamper','cited_missing','cited_symlink'):
            with self.subTest(guard=guard):
                p,trace=self.run_case(guard=guard)
                self.assertEqual(p.returncode,1);self.assertEqual(trace,[])
                self.assertNotIn(b'"mathematical_acceptance": false',p.stdout)

    def test_exact_mutant_inventory_before_children(self):
        for guard in ('missing_mutant','duplicate_mutant','reordered_mutant'):
            with self.subTest(guard=guard):
                p,trace=self.run_case(guard=guard)
                self.assertEqual(p.returncode,1);self.assertEqual(trace,[])

    def test_postflight_mutation_is_rejected(self):
        p,trace=self.run_case('dirty')
        self.assertEqual(p.returncode,1);self.assertEqual(trace,SEQUENCE)
        self.assertIn(b'diff --git',p.stdout)

    def test_unconditional_two_mode_wiring(self):
        text=WORKFLOW.read_text()
        self.assertIn("      - 'reviews/third_order_protocol_20261006/test_third_order_rate_workflow.py'",text)
        self.assertFalse((ROOT/'tests/test_third_order_rate_workflow.py').exists())
        for flags in ('-B -S','-B -O -S'):
            self.assertIn('python '+flags+' -m unittest discover -s reviews/third_order_protocol_20261006 -p test_third_order_rate_workflow.py -v',text)


if __name__=='__main__':
    unittest.main()
