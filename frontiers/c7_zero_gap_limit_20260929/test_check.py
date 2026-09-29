"""Finite controls for the C7 zero-gap candidate; no continuum proof assertion."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F
import hashlib

HERE = Path(__file__).resolve().parent
MOD = None
if (HERE/'check.py').is_file():
    spec = importlib.util.spec_from_file_location('c7_zero_gap_check', HERE/'check.py')
    MOD = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(MOD)

class ZeroGapTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MOD, 'Missing zero-gap finite-control implementation')

    def test_exact_lifetime_to_radius_pushforward(self):
        self.assertEqual(MOD.pushforward_exponents(), (F(1), F(0), F(-2)))
        for r in (F(1,100), F(1,3), F(1)):
            for k in (F(1,1000), F(2,7), F(3)):
                ell = k*r**3
                # Coarea expressed without fractional powers of rational numbers.
                self.assertEqual((1/(3*r*k))*(3*ell/r**4), r**-2)

    def test_dimension_and_ordered_pair_normalization(self):
        for d in range(2,13):
            self.assertEqual(MOD.radial_ledger(d), (1, -2))
        self.assertEqual(MOD.ordered_height_jacobian(), F(1))
        self.assertEqual(MOD.parent_pin_prefactor(), 12)

    def test_piecewise_radial_majorant(self):
        for r in (F(1,100), F(1,7), F(1,2), F(1)):
            for k in (r/100, r/2, r, 2*r, F(5)):
                value = MOD.radial_bound(r,k)
                self.assertGreater(value,0)
                self.assertLessEqual(value,4)
                self.assertEqual(value, r/k if k>=r else (1+k/r)**2)

    def test_why_the_two_branches_are_needed(self):
        r,k=F(1,100),F(1,10000)
        self.assertGreater(r/k,4)  # K2 may not be used when k < r.
        self.assertGreater(r**-2,4)  # Crude K1 without (k+r)^2 is not uniform.
        self.assertLessEqual(MOD.radial_bound(r,k),4)
        self.assertLessEqual(MOD.radial_bound(r,F(100)),1)

    def test_local_concavity_barrier_and_strictness(self):
        self.assertEqual(MOD.barrier_drop(F(2),F(1,2),F(1,3)),F(1,12))
        self.assertTrue(MOD.barrier_excludes_gap(2,F(1,2),F(1,3),1,F(1,24)))
        self.assertFalse(MOD.barrier_excludes_gap(2,F(1,2),F(1,3),1,F(1,12)))
        self.assertFalse(MOD.barrier_excludes_gap(2,F(1,2),F(1,3),1,F(1,10)))
        with self.assertRaises(ValueError):
            MOD.barrier_excludes_gap(2,0,F(1,2),1,F(1,100))
        with self.assertRaises(ValueError):
            MOD.barrier_drop(2,2,1)

    def test_positive_typed_hessian_open_set_example(self):
        for d in range(2,8):
            self.assertEqual(MOD.typed_diagonal_weight([-1]*d,[1]+[-1]*(d-1)),1)
            self.assertEqual(MOD.typed_diagonal_weight([-1]*d,[-1]*d),0)
            self.assertEqual(MOD.typed_diagonal_weight([0]+[-1]*(d-1),[1]+[-1]*(d-1)),0)
        self.assertEqual(MOD.typed_diagonal_weight([-2,-3],[4,-5]),120)

    def test_normalization_total_variation_inequality(self):
        examples = [([1,2,0],[2,3,4]), ([0,1],[1,0]), ([2,4],[1,2]), ([F(1,1000),1],[1,1])]
        for a,b in examples:
            tv,bound = MOD.normalized_tv(a,b)
            self.assertLessEqual(tv,bound)
            self.assertLessEqual(tv,1)
        self.assertEqual(MOD.normalized_tv([2,4],[1,2])[0],0)
        with self.assertRaises(ValueError):
            MOD.normalized_tv([0,0],[1,1])
        with self.assertRaises(ValueError):
            MOD.normalized_tv([-1,3],[1,1])

    def test_rejected_moments_and_pole(self):
        for q in (F(-9,10),F(-2,3),F(0),F(3,2),F(5)):
            self.assertEqual(MOD.moment_case(q),'finite')
            self.assertEqual(MOD.moment_coefficient(q)*(q+1),1)
        self.assertEqual(MOD.moment_case(-1),'logarithmic')
        self.assertEqual(MOD.moment_case(F(-4,3)),'power-divergent')
        with self.assertRaises(ValueError):
            MOD.moment_coefficient(-1)

    def test_intensity_sampling_not_fixed_radius_probability(self):
        self.assertEqual(MOD.sampling_ledger(), (F(1,3),F(1,3),F(2,3)))
        # rho -> B, nu_cand ~ c*ell^(-1/3); cumulatives are Bt and (3/2)c*t^(2/3).
        self.assertEqual(MOD.sampling_ledger()[2],1/F(3,2))
        self.assertNotEqual(MOD.sampling_ledger()[0],3)

    def test_invalid_scalar_and_dimension_inputs(self):
        for x in (True,1.0,'1',None):
            with self.assertRaises((ValueError,TypeError)):
                MOD.exact(x)
        for d in (True,1,0,-2,F(3,2)):
            with self.assertRaises((ValueError,TypeError)):
                MOD.radial_ledger(d)
        for r,k in ((0,1),(1,0),(-1,2),(2,1)):
            with self.assertRaises(ValueError):
                MOD.radial_bound(r,k)

    def test_source_checker_rejects_identity_and_path_mutations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            data=b'bounded source\n'
            (root/'source.txt').write_bytes(data)
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            row={'path':'source.txt','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':blob}
            MOD.verify_identity(root,row)
            for key,bad in (('bytes',0),('sha256','0'*64),('git_blob','0'*40),('path','../source.txt')):
                with self.assertRaises(ValueError):
                    MOD.verify_identity(root,{**row,key:bad})
            (root/'alias.txt').symlink_to(root/'source.txt')
            with self.assertRaises(ValueError):
                MOD.verify_identity(root,{**row,'path':'alias.txt'})

    def test_cli_both_modes_and_semantic_mutants(self):
        outputs=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            proc=subprocess.run([sys.executable,*flags,str(HERE/'check.py')],capture_output=True,timeout=20)
            self.assertEqual(proc.returncode,0,proc.stderr.decode())
            report=json.loads(proc.stdout)
            self.assertTrue(report['passed'])
            self.assertFalse(report['scientific_acceptance'])
            outputs.append(proc.stdout)
            for mutant in MOD.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,str(HERE/'check.py'),'--mutant',mutant],capture_output=True,timeout=20)
                self.assertEqual(bad.returncode,1,(mutant,bad.stdout,bad.stderr))
            bad=subprocess.run([sys.executable,*flags,str(HERE/'check.py'),'--mutant','UNKNOWN'],capture_output=True,timeout=20)
            self.assertEqual(bad.returncode,2)
        self.assertEqual(outputs[0],outputs[1])
        if (HERE/'RESULTS.json').is_file():
            self.assertEqual(outputs[0],(HERE/'RESULTS.json').read_bytes())

if __name__=='__main__':
    unittest.main()
