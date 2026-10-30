"""Exact finite specialization checks; no continuum or Lean-kernel claim.

Run from any directory: python3 test_adapter.py. Mutants are real temporary
adapter source files, run by child unittest processes in both Python modes.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TARGET = 'ResearchFormalCoreR1.p02_lm009_moment40_tail'
ADAPTER_FILE = Path(os.environ.get('MOMENT_TAIL_ADAPTER_FILE', HERE / 'adapter.py'))


def load_adapter():
    # Missing implementation is a collected assertion, never an import crash.
    if not ADAPTER_FILE.is_file():
        return None
    spec = importlib.util.spec_from_file_location('moment_tail_under_test', ADAPTER_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A = load_adapter()


def case(p=(1,), R=(1,), r=1, epsilon='1/2', M=1, target=TARGET):
    return dict(target=target, p=list(p), R=list(R), r=r, epsilon=epsilon, M=M)


def oracle(c):
    """Independent integer cross-products decide the strict signed event.

    This avoids evaluating r*R**5 in the adapter's arithmetic expression.
    Finite expectations are accumulated separately with Fraction.
    """
    p, values = list(map(F, c['p'])), list(map(F, c['R']))
    r, e = F(c['r']), F(c['epsilon'])
    event = []
    for x in values:
        left = e.numerator * r.denominator * x.denominator**5
        right = r.numerator * x.numerator**5 * e.denominator
        event.append(left < right)
    mass = sum((w for w, inside in zip(p, event) if inside), F(0))
    moment = sum((w * x**40 for w, x in zip(p, values)), F(0))
    bound = F(c['M']) * (r / e)**8
    return event, mass, moment, bound


class AdapterPresence(unittest.TestCase):
    def test_missing_adapter_is_collected_assertion(self):
        self.assertIsNotNone(A, 'finite MomentTail adapter missing: empirical coverage gap')


class UsesAdapter(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(A, 'finite MomentTail adapter missing: empirical coverage gap')


class SemanticTests(UsesAdapter):
    def check_case(self, c):
        expected = oracle(c)
        result = A.evaluate_case(c, source_root=ROOT)
        self.assertEqual(result['status'], 'OBSERVED_BOUND', result)
        self.assertEqual(result['event'], expected[0])
        self.assertEqual(F(result['event_mass']), expected[1])
        self.assertEqual(F(result['moment40']), expected[2])
        self.assertEqual(F(result['bound']), expected[3])
        self.assertLessEqual(expected[1], F(result['bound']))
        return result

    def test_epsilon_denominator(self):
        result = self.check_case(case(r='1/2', epsilon='1/4'))
        self.assertEqual(result['bound'], '256')

    def test_r_eighth_power(self):
        result = self.check_case(case(R=(2,), r='1/16', epsilon=1, M=2**40))
        self.assertEqual(result['bound'], '256')

    def test_fortieth_moment(self):
        result = self.check_case(case(R=(2,), epsilon=16, M=2**40))
        self.assertEqual(result['bound'], '256')
        self.assertEqual(result['moment40'], str(2**40))

    def test_strict_signed_event(self):
        result = self.check_case(case(p=('1/2','1/2'), R=(1,-1), epsilon=1))
        self.assertEqual(result['event'], [False, False])
        self.assertEqual(result['event_mass'], '0')

    def test_pathologies_and_no_r_upper_bound(self):
        for c in [case(r=17), case(R=(0,), M=0),
                  case(p=(0,1), R=(10**20,0), M=0),
                  case(p=('1/3','2/3'), R=('-1/3','2/3'), r=100,
                       epsilon='1/1000000', M=1),
                  case(r='1/1000000000000000000', epsilon='1/100000000000000000000'),
                  case(r=10**20, epsilon=10**19, M=10**40),
                  case(epsilon='999999/1000000'),case(epsilon='1000001/1000000')]:
            with self.subTest(c=c): self.check_case(c)

    def test_seeded_generator_matches_independent_oracle(self):
        generated = list(A.generate_cases(seed=193, count=173))
        self.assertEqual(len(generated), 173)
        for c in generated: self.check_case(c)


class DomainTests(UsesAdapter):
    def test_invalid_inputs_never_observed(self):
        bad = [None, [], {}, case(p=(),R=()), case(p=(1,0),R=(1,)),
               case(p=(-1,2),R=(1,2)),case(p=('1/2',)),case(r=0),case(r=-1),
               case(epsilon=0),case(M=-1),case(r=True),case(r=0.5),
               case(r='NaN'),case(r='Infinity'),case(r='1/0'),case(r='1.5'),
               case(r=' 1'),case(r='1/2/3'),case(r=[]),case(p=(True,)),
               case(R=(float('inf'),)),dict(case(),extra=1)]
        for c in bad:
            with self.subTest(c=c):
                self.assertEqual(A.evaluate_case(c,source_root=ROOT)['status'],'INVALID')

    def test_false_moment_premise_is_not_counterexample(self):
        result = A.evaluate_case(case(R=(2,),M=1),source_root=ROOT)
        self.assertEqual(result['status'],'FALSE_PREMISE')
        self.assertNotIn('bound',result)

    def test_fortieth_moment_premise_admission(self):
        # R=2 has moment40=2**40, so M=2**20 is insufficient.
        # A moment20 validator wrongly admits this input. This is an
        # admission regression, not a valid mathematical counterexample.
        result=A.evaluate_case(case(R=(2,),r=1,epsilon=16,M=2**20),source_root=ROOT)
        self.assertEqual(result['status'],'FALSE_PREMISE',result)
        report=A.run_campaign(cases=[case(R=(2,),r=1,epsilon=16,M=2**20)],source_root=ROOT)
        self.assertEqual(report['status'],'REFUSED')
        self.assertEqual(report['counts']['valid'],0)
        self.assertEqual(report['counts']['counterexamples'],0)

    def test_unknown_target_is_unsupported(self):
        result = A.evaluate_case(case(target='Gaussian'),source_root=ROOT)
        self.assertEqual(result['status'],'UNSUPPORTED')

    def test_fraction_input_and_canonical_identity(self):
        x=A.evaluate_case(case(r=F(1,2)),source_root=ROOT)
        y=A.evaluate_case(case(r='2/4'),source_root=ROOT)
        self.assertEqual(x,y)
        self.assertEqual(len(x['case_id']),64)

    def test_source_tampering_and_missing_source_refuse(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for path in A.SOURCE_FILES:
                dst=root/path; dst.parent.mkdir(parents=True,exist_ok=True)
                dst.write_bytes((ROOT/path).read_bytes())
            self.assertEqual(A.evaluate_case(case(),source_root=root)['status'],'OBSERVED_BOUND')
            for path in A.SOURCE_FILES:
                old=(root/path).read_bytes()
                (root/path).write_bytes(old+b'\n')
                self.assertEqual(A.evaluate_case(case(),source_root=root)['status'],'SOURCE_MISMATCH')
                (root/path).write_bytes(old)
            (root/A.SOURCE_FILES[0]).unlink()
            self.assertEqual(A.evaluate_case(case(),source_root=root)['status'],'SOURCE_MISMATCH')
            self.assertEqual(A.run_campaign(seed=1,count=10,source_root=root)['status'],'REFUSED')


class CampaignTests(UsesAdapter):
    def test_replay_distinctness_counts_and_source_binding(self):
        x=A.run_campaign(seed=41,count=257,source_root=ROOT)
        self.assertEqual(x,A.run_campaign(seed=41,count=257,source_root=ROOT))
        self.assertEqual(x['status'],'BOUNDED_OBSERVATIONS')
        self.assertEqual(x['counts'],dict(attempted=257,valid=257,invalid=0,
            false_premise=0,unsupported=0,source_mismatch=0,counterexamples=0,distinct_valid=257))
        self.assertNotEqual(x['cases_digest'],A.run_campaign(seed=42,count=257,source_root=ROOT)['cases_digest'])
        self.assertEqual(x['source_binding']['status'],'VERIFIED')
        self.assertEqual(x['source_binding']['reference_commit'],'19a55750451b8016b50d1d20be6a18c021807ecb')
        self.assertFalse(x['full_federation_admitted'])
        self.assertEqual(x['scientific_effect'],'NONE')

    def test_empty_invalid_unsupported_false_premise_cannot_green(self):
        for population in [[],[case(r=0)],[case(target='other')],[case(M=0)],
                           [case(),case(r=0)], [case(),case(target='other')]]:
            report=A.run_campaign(cases=population,source_root=ROOT)
            self.assertEqual(report['status'],'REFUSED',report)
        for count in [0,-1,True,1.2]:
            self.assertEqual(A.run_campaign(count=count,source_root=ROOT)['status'],'REFUSED')

    def test_duplicate_observations_not_distinct_credit(self):
        report=A.run_campaign(cases=[case(),case(r='1/1')],source_root=ROOT)
        self.assertEqual(report['counts']['attempted'],2)
        self.assertEqual(report['counts']['distinct_valid'],1)
        self.assertEqual(report['counts']['valid'],2)

    def test_10000_actual_distinct_valid_seeded_pathologies(self):
        report=A.run_campaign(seed=20261030,count=10019,source_root=ROOT)
        self.assertEqual(report['status'],'BOUNDED_OBSERVATIONS')
        self.assertEqual(report['counts']['valid'],10019)
        self.assertEqual(report['counts']['distinct_valid'],10019)
        self.assertEqual(report['counts']['counterexamples'],0)
        # Compare every generated observation with the independent oracle,
        # including event membership, not just the mathematically slack bound.
        for c in A.generate_cases(seed=20261030,count=10019):
            result=A.evaluate_case(c,source_root=ROOT)
            event,mass,moment,bound=oracle(c)
            self.assertEqual(result['status'],'OBSERVED_BOUND',result)
            self.assertEqual(result['event'],event)
            self.assertEqual(F(result['event_mass']),mass)
            self.assertEqual(F(result['moment40']),moment)
            self.assertEqual(F(result['bound']),bound)


class CliTests(UsesAdapter):
    def invoke(self,args,payload):
        command=[sys.executable,*(['-O'] if sys.flags.optimize else []),
                 str(ADAPTER_FILE),'--source-root',str(ROOT),*args]
        result=subprocess.run(command,input=payload,text=True,capture_output=True,check=False)
        evidence=os.environ.get('MOMENT_TAIL_EVIDENCE_DIR')
        if evidence:
            destination=Path(evidence)/('parent-O' if sys.flags.optimize else 'parent-normal')
            destination.mkdir(parents=True,exist_ok=True)
            stem='cli-'+hashlib.sha256((json.dumps(args)+payload).encode()).hexdigest()[:16]
            (destination/(stem+'.stdin')).write_text(payload)
            (destination/(stem+'.stdout')).write_text(result.stdout)
            (destination/(stem+'.stderr')).write_text(result.stderr)
            (destination/(stem+'.json')).write_text(json.dumps(dict(argv=command,
                parent_optimization=sys.flags.optimize,returncode=result.returncode),indent=2)+'\n')
        return result

    def test_evaluate_success_and_rejections_have_json_and_exit(self):
        good=self.invoke(['evaluate'],json.dumps(case()))
        self.assertEqual(good.returncode,0,good.stderr)
        report=json.loads(good.stdout)
        self.assertEqual(report['status'],'OBSERVED_BOUND')
        self.assertIn('execution',report)
        # All other required fields are valid: silently choosing either
        # duplicate r value would wrongly produce an observed bound.
        duplicate=json.dumps(case())[:-1]+',"r":2}'
        for payload in [duplicate, 'NaN',json.dumps(case(r=0.5)),
                        json.dumps(case(target='unknown')),json.dumps(case(r=0))]:
            bad=self.invoke(['evaluate'],payload)
            self.assertEqual(bad.returncode,2,bad.stdout+bad.stderr)
            self.assertIn(json.loads(bad.stdout)['status'],['INVALID','UNSUPPORTED'])

    def test_cli_campaign_and_empty_input(self):
        good=self.invoke(['campaign','--count','31','--seed','77'],'')
        self.assertEqual(good.returncode,0,good.stderr)
        self.assertEqual(json.loads(good.stdout)['counts']['distinct_valid'],31)
        bad=self.invoke(['campaign','--stdin-cases'],'[]')
        self.assertEqual(bad.returncode,2)
        self.assertEqual(json.loads(bad.stdout)['status'],'REFUSED')


class MutationTests(UsesAdapter):
    def test_real_source_mutants_fail_intended_assertions_zero_errors_both_modes(self):
        source=ADAPTER_FILE.read_text()
        mutations=[
            ('epsilon', 'bound = (M / epsilon ** 8) * r ** 8', 'bound = M * r ** 8', 'SemanticTests.test_epsilon_denominator'),
            ('r16', 'bound = (M / epsilon ** 8) * r ** 8', 'bound = (M / epsilon ** 8) * r ** 16', 'SemanticTests.test_r_eighth_power'),
            ('moment20', 'bound = (M / epsilon ** 8) * r ** 8',
             'bound = (sum((w * x ** 20 for w, x in zip(p, values)), F(0)) / epsilon ** 8) * r ** 8', 'SemanticTests.test_fortieth_moment'),
            ('moment20_admission',
             'moment = sum((weight * value ** 40 for weight, value in zip(p, values)), F(0))',
             'moment = sum((weight * value ** 20 for weight, value in zip(p, values)), F(0))',
             'DomainTests.test_fortieth_moment_premise_admission'),
            ('weak_event','event = [epsilon < r * value ** 5 for value in values]',
             'event = [epsilon <= r * value ** 5 for value in values]', 'SemanticTests.test_strict_signed_event')]
        with tempfile.TemporaryDirectory() as directory:
            for name,before,after,test in mutations:
                self.assertEqual(source.count(before),1,'mutation anchor must identify exactly one source cut')
                mutant=Path(directory)/(name+'.py'); mutant.write_text(source.replace(before,after))
                for optimized in [False,True]:
                    with self.subTest(mutant=name,optimized=optimized):
                        env=dict(os.environ,MOMENT_TAIL_ADAPTER_FILE=str(mutant),
                                 MOMENT_TAIL_MUTANT_NAME=name)
                        command=[sys.executable,*(['-O'] if optimized else []),
                                 str(Path(__file__).resolve()),test]
                        result=subprocess.run(command,
                            env=env,text=True,capture_output=True,check=False)
                        output=result.stdout+result.stderr
                        self.assertEqual(result.returncode,1,output)
                        self.assertIn('FAIL:',output)
                        self.assertIn('FAILED (failures=1)',output)
                        self.assertNotIn('ERROR:',output)
                        identity=json.loads(result.stdout.splitlines()[0])
                        self.assertEqual(identity['optimization'],int(optimized))
                        self.assertEqual(identity['source_sha256'],hashlib.sha256(mutant.read_bytes()).hexdigest())
                        evidence=os.environ.get('MOMENT_TAIL_EVIDENCE_DIR')
                        if evidence:
                            destination=Path(evidence)/('parent-O' if sys.flags.optimize else 'parent-normal')
                            destination.mkdir(parents=True,exist_ok=True)
                            stem=name+('-O' if optimized else '-normal')
                            (destination/(stem+'.py')).write_bytes(mutant.read_bytes())
                            (destination/(stem+'.stdout')).write_text(result.stdout)
                            (destination/(stem+'.stderr')).write_text(result.stderr)
                            (destination/(stem+'.json')).write_text(json.dumps(dict(
                                argv=command,returncode=result.returncode,identity=identity,
                                parent_optimization=sys.flags.optimize,intended_test=test,
                                failures=1,errors=0,source_cut=dict(before=before,after=after),
                                mathematical_counterexample_credit=False if name=='moment20_admission' else None
                            ),indent=2)+'\n')


if __name__ == '__main__':
    if os.environ.get('MOMENT_TAIL_MUTANT_NAME'):
        print(json.dumps(dict(mutant=os.environ['MOMENT_TAIL_MUTANT_NAME'],
            optimization=sys.flags.optimize,argv=sys.argv,
            source_sha256=hashlib.sha256(ADAPTER_FILE.read_bytes()).hexdigest())),flush=True)
    unittest.main()
