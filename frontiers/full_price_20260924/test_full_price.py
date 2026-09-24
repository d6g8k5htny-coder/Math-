"""Finite exact controls; no Gaussian simulation or independent analytic review."""
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial
from pathlib import Path
import importlib.util
import unittest
import full_price as f


class FullPrice(unittest.TestCase):
    def test_exp_contains_e_bracket(self):
        lo,hi=f.exp_one_bounds(); self.assertGreater(lo,Q('2.718281828459045235360287471352'))
        self.assertLess(hi,Q('2.718281828459045235360287471353')); self.assertLess(lo,hi)
    def test_exp_refinement(self):
        a,b=f.exp_one_bounds(12); c,d=f.exp_one_bounds(24)
        self.assertLess(a,c); self.assertLess(d,b)
    def test_log_one(self): self.assertEqual(f.log_bounds(1),(0,0))
    def test_log_reciprocal(self):
        a,b=f.log_bounds(Q(3)); c,d=f.log_bounds(Q(1,3))
        self.assertLessEqual(a+c,0); self.assertGreaterEqual(b+d,0)
    def test_log_two(self):
        a,b=f.log_bounds(2); self.assertGreater(a,Q(2,3)); self.assertLess(b,Q(7,10))
    def test_log_bounds_order(self):
        for x in (Q(1,7),Q(9,7),Q(17),Q(128)):
            a,b=f.log_bounds(x); self.assertLess(a,b)
    def test_inexact_refused(self):
        for x in (True,0.5,'1/2'):
            with self.assertRaises(TypeError): f.rational(x)
        f.log_bounds(Q(1)); f.log_bounds(Q(1,2))
        for x in (True,0.5,'1/2'):
            with self.assertRaises(TypeError): f.log_bounds(x)
    def test_log_domain_refused(self):
        for x in (0,-1):
            with self.assertRaises(ValueError): f.log_bounds(x)
    def test_terms_refused(self):
        for n in (True,0,257):
            with self.assertRaises(ValueError): f.exp_one_bounds(n)
    def test_phi_zero(self): self.assertEqual(f.phi_bounds(0),(0,0))
    def test_phi_one(self): self.assertEqual(f.phi_bounds(1),(1,1))
    def test_phi_cap(self): self.assertEqual(f.phi_bounds(Q(2,3)),(1,1))
    def test_phi_half(self):
        a,b=f.phi_bounds(Q(1,2)); self.assertGreater(a,Q(2,3)); self.assertLess(b,1)
    def test_phi_domain(self):
        for p in (-1,2):
            with self.assertRaises(ValueError): f.phi_bounds(p)
    def test_good_endpoints(self):
        self.assertEqual(f.capacity_good([0,0,0],1),1)
        self.assertEqual(f.capacity_good([1,1,1],1),0)
    def test_good_half(self): self.assertEqual(f.capacity_good([Q(1,2)]*3,1),Q(1,2))
    def test_recursion_enumeration(self):
        masks={m for m in range(8) if m.bit_count()<=1}
        for ps in product((Q(0),Q(1,4),Q(1,2),Q(2,3),Q(1)),repeat=3):
            self.assertEqual(f.capacity_good(ps,1),f.downset_good(3,masks,ps))
    def test_binomial_matches_recursion(self):
        for n in range(1,10):
            for a in range(n):
                self.assertEqual(f.binomial_good(n,a,Q(3,5)),f.capacity_good([Q(3,5)]*n,a))
    def test_odd_majority_recurrence(self):
        for a in range(1,8):
            for p in (Q(1,2),Q(3,5),Q(2,3),Q(4,5)):
                n=2*a+1
                difference=f.binomial_good(n+2,a+1,p)-f.binomial_good(n,a,p)
                expected=p*(1-2*p)*comb(n,a)*p**a*(1-p)**(n-a)
                self.assertEqual(difference,expected);self.assertLessEqual(difference,0)
    def test_extra_trials_reduce_good(self):
        for n in range(3,10): self.assertLessEqual(f.binomial_good(n+1,1,Q(3,5)),f.binomial_good(n,1,Q(3,5)))
    def test_coordinate_concavity(self):
        for A,B,z in product((Q(1,5),Q(1,2),Q(1)),repeat=3):
            self.assertLess(f.coordinate_second_derivative(A,B,z),0)
    def test_zero_slice_coefficients(self):
        self.assertEqual(f.coordinate_second_derivative(0,1,1),0)
        self.assertEqual(f.coordinate_second_derivative(1,0,1),0)
    def test_class_hypotheses(self):
        self.assertFalse(f.realized_class(1,1)['full_price_uniform_guarantee'])
        for a in (1,2,7): self.assertTrue(f.realized_class(a,2)['full_price_uniform_guarantee'])
    def test_original_block_size(self): self.assertEqual(f.realized_class(1,408)['block_size'],409)
    def test_invalid_class(self):
        for a,d in ((0,2),(1,0),(True,2),(1,2.0)):
            with self.assertRaises(ValueError): f.realized_class(a,d)
    def test_constant_interval(self):
        h,r=f.reference_bounds()
        self.assertGreater(h[0],Q('1.182760344597922'))
        self.assertLess(h[1],Q('1.182760344597924'))
        self.assertGreater(r[0],Q('0.845479817248985'))
        self.assertLess(r[1],Q('0.845479817248988'))
    def test_rational_slack(self):
        h,r=f.reference_bounds();self.assertGreater(h[0],Q(7,6));self.assertLess(r[1],Q(6,7))
        self.assertEqual(f.exp_one_bounds(6)[1],Q(31967,11760))
        self.assertEqual(Q(87,32)-f.exp_one_bounds(6)[1],Q(11,23520))
        lower=sum((Q(11,6)**j/factorial(j) for j in range(6)),Q(0))
        self.assertEqual(lower-Q(197,32),Q(26081,933120))
    def test_demand_one_reference_fails(self):
        h,r=f.reference_bounds(2,1);self.assertLess(h[1],1);self.assertGreater(r[0],1)
    def test_reference_extremum(self):
        h,_=f.reference_bounds(3,1)
        for a,n in ((1,4),(2,5),(3,7),(2,7)):
            other,_=f.reference_bounds(n,a);self.assertGreater(other[0],h[1])
    def test_full_probability_triples(self):
        for ps in product((Q(0),Q(1,4),Q(1,2),Q(2,3),Q(1)),repeat=3):
            self.assertTrue(f.local_budget_check(ps,1),ps)
    def test_full_probability_quintuples(self):
        for ps in product((Q(1,4),Q(1,2),Q(3,4)),repeat=5):
            self.assertTrue(f.local_budget_check(ps,2),ps)
    def test_non_downset_refused(self):
        with self.assertRaises(ValueError): f.downset_good(2,{0,3},[Q(1,2)]*2)
    def test_sharp_cover_at_unit_prices(self):
        # Only the full triple obstructs two colors; every possible generator costs one.
        costs=[]
        for cover in range(1,1<<8):
            costs.append(sum(1 for mask in range(8) if cover&(1<<mask)))
        self.assertEqual(min(costs),1)
    def test_decimal_outward(self):
        self.assertEqual(f.decimal_outward((Q(1,3),Q(2,3)),2),{'lower':'0.33','upper':'0.67'})
        self.assertEqual(f.decimal_outward((Q(-2,3),Q(-1,3)),2),{'lower':'-0.67','upper':'-0.33'})
    def test_original_price_counterexample_preserved(self):
        self.assertEqual(f.capacity_good([Q(1,2)]*2,1),Q(3,4))
        self.assertGreater(Q(4,9),f.log_bounds(Q(4,3))[1])
    def test_result_scope(self):
        r=f.result();self.assertFalse(r['scientific_acceptance']);self.assertIn('all independent',r['probability_domain'])
        self.assertEqual(r['palette'],'unchanged K>=K_H(d)')


if __name__=='__main__': unittest.main()
