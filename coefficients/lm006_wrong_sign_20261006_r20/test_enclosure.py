"""Arithmetic and enclosure regressions; not an independent proof review."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import itertools
import json
import math
import subprocess
import sys
import unittest
P=Path(__file__).with_name('enclose.py')
class EnclosureTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(P.is_file(), 'enclosure implementation missing')
        spec=importlib.util.spec_from_file_location('enclose',P)
        self.m=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.m)
    def test_rational_rounding(self):
        for x in (F(0),F(1,3),F(7,9),F(23,7)):
            lo,hi=self.m.fixed(x)
            self.assertLessEqual(F(lo,self.m.SCALE),x)
            self.assertGreaterEqual(F(hi,self.m.SCALE),x)
            self.assertLessEqual(hi-lo,1)
    def test_square_root_enclosure(self):
        for x in (F(0),F(1,7),F(2),F(9,4),F(100)):
            lo,hi=self.m.sqrt_bounds(x)
            self.assertLessEqual(lo*lo,x);self.assertGreaterEqual(hi*hi,x)
    def test_exponential_bounds(self):
        for x in (F(0),F(1,8),F(1),F(3),F(25),F(36),F(40)):
            lo,hi=self.m.exp_neg(x)
            self.assertTrue(0<=lo<=hi<=1)
            self.assertLess(hi-lo,F(1,10**30))
            # This binary64 comparison is only a loose supplemental screen.
            self.assertAlmostEqual(float((lo+hi)/2),math.exp(-float(x)),places=14)
        a,b=self.m.exp_neg(F(1,2));c,d=self.m.exp_neg(1)
        self.assertTrue(a*a<=d and b*b>=c)
    def test_exponential_against_unrounded_alternating_sums(self):
        for x in (F(1,8),F(1,2),F(1)):
            # Distinct high-order rational reference, without scaling or rounding.
            ref_hi=sum(((-x)**k/F(math.factorial(k)) for k in range(61)),F(0))
            ref_lo=ref_hi+(-x)**61/F(math.factorial(61))
            lo,hi=self.m.exp_neg(x)
            self.assertLessEqual(lo,ref_lo)
            self.assertGreaterEqual(hi,ref_hi)
    def test_pi_and_cdf(self):
        lo,hi=self.m.pi_bounds()
        self.assertTrue(F('3.14159265358979323846264338327950288')<lo<hi<F('3.14159265358979323846264338327950289'))
        self.assertEqual(self.m.cdf_positive(F(0)),(F(1,2),F(1,2)))
        for x in (F(1,4),F(1,2),F(9,10)):
            a,b=self.m.cdf_positive(x)
            self.assertTrue(F(1,2)<a<=b<1)
            self.assertAlmostEqual(float((a+b)/2),.5*(1+math.erf(float(x)/math.sqrt(2))),places=14)
    def test_image_moment_bound(self):
        report=self.m.image_bounds()
        self.assertTrue(report['exp288_lower_gt_10pow125'])
        self.assertLess(report['m2_error'],F(1,10**118))
        self.assertLess(report['m4_error'],F(1,10**118))
    def test_j_exact(self):
        self.assertEqual(self.m.j(F(2),F(1)),F(1,3))
        self.assertEqual(self.m.j(F(3),F(1)),F(5,6))
        for d,u in itertools.product(range(9),range(10)):
            val=self.m.j(F(d),F(u))
            self.assertTrue(0<=val<=F(d**3,24))
            if 0<=u<=d:self.assertEqual(val,self.m.j(F(d),F(d-u)))
    def test_rectangle_extrema(self):
        for d0,u0 in itertools.product(range(7),range(7)):
            d1,u1=F(d0+2),F(u0+2)
            lo,hi=self.m.cell_bounds(F(d0),d1,F(u0),u1)
            for d,u in itertools.product((F(d0),F(d0+1),d1),(F(u0),F(u0+1),u1)):
                self.assertTrue(lo<=self.m.j(d,u)<=hi)
    def test_density_parameter_intervals(self):
        var=(F(199,100),F(201,100))
        for x in (F(0),F(1),F(3)):
            lo,hi=self.m.density(x,var)
            actual=math.exp(-float(x*x)/4)/math.sqrt(4*math.pi)
            self.assertLess(float(lo),actual);self.assertGreater(float(hi),actual)
    def test_normalizer(self):
        data=self.m.parameters()
        z=data['z0'];p=data['p0']
        self.assertTrue(F(3)<z[0]<z[1]<4)
        self.assertTrue(F(19,100)<p[0]<p[1]<F(21,100))
    def test_grid_refines_and_tails_positive(self):
        small=self.m.enclosure(16);large=self.m.enclosure(32)
        self.assertTrue(0<small['coefficient'][0]<=large['coefficient'][0])
        self.assertGreaterEqual(small['coefficient'][1],large['coefficient'][1])
        self.assertGreater(large['tail'],0)
        self.assertLess(large['tail'],F(1,10**7))
    def test_independent_inner_primitive(self):
        # Integrate the two clipped affine factors independently at their roots.
        for d,u in itertools.product((F(i,3) for i in range(13)),(F(i,4) for i in range(17))):
            knots=sorted({F(0),d,*[x for x in (u,d-u) if 0<x<d]})
            primitive=lambda t:u*(d-u)*t-d*t*t/2+t**3/3
            value=F(0)
            for left,right in zip(knots,knots[1:]):
                t=(left+right)/2
                if d-u-t>0 and u-t>0:value+=primitive(right)-primitive(left)
            self.assertEqual(value,self.m.j(d,u))
    def test_full_rectangle_sum_against_fraction_reference(self):
        # Independent coordinate-based sum, not the optimized integer units.
        n=8;v=self.m.parameters()['variance_D'];low=high=F(0)
        for i,k in itertools.product(range(n),repeat=2):
            d0,d1=F(12*i,n),F(12*(i+1),n)
            b0,b1=F(4*k,n),F(4*(k+1),n)
            jl,ju=self.m.cell_bounds(d0,d1,b0*b0,b1*b1)
            dl=self.m.density(d1,v)[0];du=self.m.density(d0,v)[1]
            bl=self.m.density(b1,(v[0]/4,v[1]/4))[0]
            bu=self.m.density(b0,(v[0]/4,v[1]/4))[1]
            low+=2*(d1-d0)*(b1-b0)*jl*dl*bl
            high+=2*(d1-d0)*(b1-b0)*ju*du*bu
        actual=self.m.enclosure(n)
        self.assertEqual(actual['gamma'][0],low)
        self.assertEqual(actual['gamma'][1],high+actual['tail'])
        # Check normalization after, not within, the untilted Gaussian integral.
        p=self.m.parameters()
        self.assertEqual(actual['coefficient'][0],low*p['p0'][0]/p['z0'][1])
        self.assertEqual(actual['coefficient'][1],(high+actual['tail'])*p['p0'][1]/p['z0'][0])
    def test_invalid_inputs(self):
        for value in (0,1,True,3.0):
            with self.assertRaises((ValueError,TypeError)):self.m.enclosure(value)
        with self.assertRaises(ValueError):self.m.sqrt_bounds(F(-1))
        with self.assertRaises(ValueError):self.m.exp_neg(F(-1))
        with self.assertRaises(ValueError):self.m.cdf_positive(F(2))
    def test_cli(self):
        results=[]
        for flags in (['-B','-S'],['-B','-O','-S']):
            r=subprocess.run([sys.executable,*flags,str(P),'--grid','32'],capture_output=True,text=True,timeout=40)
            self.assertEqual((r.returncode,r.stderr),(0,''))
            self.assertFalse(json.loads(r.stdout)['independently_reviewed']);results.append(r.stdout)
        self.assertEqual(*results)
if __name__=='__main__':unittest.main(verbosity=2)
