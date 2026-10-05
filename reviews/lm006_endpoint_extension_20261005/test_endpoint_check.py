"""Exact algebra controls; these are not a Gaussian-field or Lean proof."""
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path
import random
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'endpoint_check.py'


def eval_poly(p, x):
    return sum((a * x**j for j, a in enumerate(p)), Q(0))


def derivative(p, order=1):
    for _ in range(order):
        p = [j * a for j, a in enumerate(p)][1:]
    return p or [Q(0)]


def integrate(p, lo=Q(-1, 2), hi=Q(1, 2)):
    return sum((a * (hi**(j+1) - lo**(j+1)) / (j+1)
                for j, a in enumerate(p)), Q(0))


class EndpointTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SOURCE.is_file(), 'endpoint implementation is missing')
        spec = importlib.util.spec_from_file_location('endpoint_check_under_test', SOURCE)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)

    def test_frame_is_invertible_on_arbitrary_rational_pins(self):
        rng = random.Random(1005)
        for r in (Q(1,128), Q(1,7), Q(2), Q(5,2)):
            for _ in range(30):
                raw = tuple(Q(rng.randint(-20,20), rng.randint(1,9)) for _ in range(6))
                p = self.m.frame(raw, r)
                self.assertEqual(self.m.unframe(p, r), raw)

    def test_prescribed_pins_have_bounded_transformed_values(self):
        for r in (Q(1,128), Q(1,3), Q(2)):
            for b in (Q(6,5), Q(-3), Q(0)):
                raw = (b, Q(0), Q(0), b-r**3/6, Q(0), Q(0))
                self.assertEqual(self.m.frame(raw, r), (b-r**3/12, Q(0), Q(0), Q(0), Q(0), Q(2)))
                self.assertEqual(self.m.prescribed_pins(b,r), raw)

    def test_cubic_frame_kernel_on_monomials(self):
        for r in (Q(1,64), Q(1,3), Q(1), Q(5,2)):
            for j in range(14):
                f = [Q(0)]*j+[Q(1)]
                d = derivative(f)
                raw = (eval_poly(f,-r/2), eval_poly(d,-r/2), Q(0),
                       eval_poly(f,r/2), eval_poly(d,r/2), Q(0))
                lhs = self.m.frame(raw,r)[5]
                self.assertEqual(lhs, self.m.kernels(f,[Q(0)],r)['P5'])

    def test_endpoint_kernels_on_general_polynomials(self):
        rng = random.Random(1105)
        for r in (Q(1,50), Q(1,2), Q(7,3)):
            for _ in range(30):
                f = [Q(rng.randint(-5,5)) for _ in range(10)]
                h = [Q(rng.randint(-5,5)) for _ in range(8)]
                direct = self.m.direct(f,h,r)
                kernels = self.m.kernels(f,h,r)
                for key in ('P3','P4','P5','Aminus','Aplus','Bminus','Bplus'):
                    self.assertEqual(direct[key],kernels[key],key)

    def test_kernel_masses_and_lower_degree_annihilation(self):
        self.assertEqual(integrate([Q(3,2),Q(0),Q(-6)]),1)
        self.assertEqual(integrate([Q(-1,2),Q(1)]),Q(-1,2))
        self.assertEqual(integrate([Q(1,2),Q(1)]),Q(1,2))
        for j in range(3):
            f = [Q(0)]*j+[Q(1)]
            values = self.m.kernels(f,[Q(0)],Q(1,2))
            self.assertEqual(values['P5'],0)
            self.assertEqual(values['Aminus'],0)
            self.assertEqual(values['Aplus'],0)

    def test_exact_cubic_and_transverse_limits(self):
        # F'''=2, H''=a=4. No finite-r approximation is used.
        for r in (Q(1,1000),Q(1,2),Q(3)):
            v = self.m.direct([Q(6,5),0,0,Q(1,3)],[0,0,Q(2)],r)
            self.assertEqual((v['Aminus'],v['Aplus'],v['Bminus'],v['Bplus']),(-1,1,-2,2))
            self.assertEqual(v['P5'],2)

    def test_subtraction_is_load_bearing(self):
        # F=x^2: raw F''/r diverges, whereas the adjusted endpoint is zero.
        for r in (Q(1,2),Q(1,8),Q(1,128)):
            v=self.m.direct([0,0,Q(1)],[0],r)
            self.assertEqual((v['Aminus'],v['Aplus']),(0,0))
            self.assertGreater(Q(2)/r,0)

    def test_full_dimension_gaussian_eighth_moment(self):
        self.assertEqual(self.m.gaussian_norm8(6),5760)
        self.assertEqual(self.m.gaussian_norm8(1),105)
        self.assertEqual(self.m.gaussian_norm8(2),384)

    def test_bad_radius_and_shape_rejected(self):
        for r in (Q(0),Q(-1),0.5,True):
            with self.assertRaises((ValueError,TypeError)):
                self.m.frame((Q(0),)*6,r)
        with self.assertRaises(ValueError):
            self.m.frame((Q(0),)*5,Q(1))
        for d in (0,-1,2.5,True):
            with self.assertRaises((ValueError,TypeError)):
                self.m.gaussian_norm8(d)

    def test_baseline_checks_and_normal_optimized_cli(self):
        outputs=[]
        for mode in ([],['-O']):
            p=subprocess.run([sys.executable,'-B',*mode,'-S',str(SOURCE)],capture_output=True,check=False)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertEqual(p.stderr,b'')
            result=json.loads(p.stdout)
            self.assertTrue(result['passed'])
            self.assertGreater(result['total'],500)
            outputs.append(p.stdout)
        self.assertEqual(*outputs)

    def test_mutants_fail_in_both_modes(self):
        for mode in ([],['-O']):
            for mutation in ('M1','M2','M3','M4','M5'):
                p=subprocess.run([sys.executable,'-B',*mode,'-S',str(SOURCE),'--mutant',mutation],capture_output=True,check=False)
                self.assertEqual(p.returncode,1,(mutation,p.stdout,p.stderr))
                self.assertIn(b'ENDPOINT_CHECK_FAIL',p.stderr)
                self.assertEqual(p.stdout,b'')

    def test_invalid_cli_arguments(self):
        for mode in ([],['-O']):
            for args in (['--mutant','BAD'],['--unknown'],['--mutant']):
                p=subprocess.run([sys.executable,'-B',*mode,'-S',str(SOURCE),*args],capture_output=True,check=False)
                self.assertEqual(p.returncode,2,p.stderr)
                self.assertEqual(p.stdout,b'')


if __name__=='__main__':
    unittest.main()
