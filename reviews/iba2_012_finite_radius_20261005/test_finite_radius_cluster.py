"""Exact algebra checks for FR; not a Gaussian-field simulation or Lean proof."""
from fractions import Fraction as F
from math import ceil
import json
from pathlib import Path
import unittest


def mul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x+y for x, y in zip(ka, kb))
            out[key] = out.get(key, F(0)) + va*vb
    return {k: v for k, v in out.items() if v}


def mono(n, i):
    key = [0]*n
    key[i] = 1
    return {tuple(key): F(1)}


def add(a, b, scale=1):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, F(0)) + scale*value
    return {k: v for k, v in out.items() if v}


def soft_integral(p, mutant=None):
    """Integrate prod x_i(x_i+r) V(x) over 0<x_1<...<x_p<r."""
    n = p+1
    poly = {(0,)*n: F(1)}
    for i in range(p):
        poly = mul(poly, mono(n, i))
        if not (mutant == 'drop_saddle' and i == 0):
            poly = mul(poly, add(mono(n, i), mono(n, p)))
    for i in range(p):
        for j in range(i+1, p):
            if mutant == 'drop_vandermonde' and (i, j) == (0, 1):
                continue
            poly = mul(poly, add(mono(n, j), mono(n, i), -1))
    # Integrate x_i from zero to x_(i+1), with x_p interpreted as r.
    for i in range(p):
        nxt = {}
        for powers, coeff in poly.items():
            new = list(powers)
            degree = new[i]+1
            new[i] = 0
            new[i+1] += degree
            key = tuple(new)
            nxt[key] = nxt.get(key, F(0)) + coeff/degree
        poly = {k:v for k,v in nxt.items() if v}
    return {powers[-1]: value for powers, value in poly.items()}


def mixed_power_vector(q: int) -> tuple[int, ...]:
    """Powers for eigenvalues numbered 2,...,q+1, not a probability bound."""
    if type(q) is not int or q < 0:
        raise ValueError('q must be a nonnegative integer')
    return tuple(j+2 for j in range(2,q+2))


def mixed_radial_exponent(alphas: tuple[F, ...]) -> F:
    """Exact homogeneity of the proved upper envelope at eta_j=r**alpha_j."""
    if any(a <= 0 for a in alphas):
        raise ValueError('all exponents must be positive')
    return F(3)+sum((w*min(F(a),F(1)) for w,a in zip(mixed_power_vector(len(alphas)),alphas)),F(0))


class FiniteRadiusAlgebra(unittest.TestCase):
    def test_first_band_integral(self):
        for r in (F(1,2),F(1,16),F(1,100)):
            for t in (F(1),F(2),F(8)):
                A=r*t*t; delta=r*t
                actual=A**3/3+delta*A*A/2
                self.assertEqual(actual,r**3*(t**6/3+t**5/2))
                self.assertLessEqual(actual,F(5,6)*r**3*t**6)

    def test_other_band_integral(self):
        for b in (F(1,100),F(1),F(9)):
            for ratio in (F(0),F(1,4),F(1)):
                delta=b*ratio
                self.assertLessEqual(b**3/3+delta*b*b/2,F(5,6)*b**3)

    def test_exact_full_soft_homogeneity(self):
        for p in range(1,6):
            got=soft_integral(p)
            self.assertEqual(set(got), {3*p+p*(p-1)//2})
            self.assertGreater(next(iter(got.values())),0)
        self.assertEqual(soft_integral(1),{3:F(5,6)})

    def test_diagonal_and_codimension_ledgers(self):
        for q in range(1,13):
            p=q+1; beta=q*(q+7)//2
            self.assertEqual(beta,3*q+p*(p-1)//2)
            self.assertEqual(3+beta,3*p+p*(p-1)//2)
            self.assertEqual(p*(p+1)//2,p+p*(p-1)//2)
        self.assertEqual([3+q*(q+7)//2 for q in range(1,5)],[7,12,18,25])

    def test_dyadic_exponent_can_be_made_summable(self):
        for m in range(2,10):
            for q in range(1,m):
                for a in (F(0),F(1,2),F(7)):
                    beta=q*(q+7)//2; p=q+1
                    moment=ceil(a+10+m-p+beta)
                    exponent=a+8+m-p+beta-moment
                    self.assertLessEqual(exponent,-2)

    def test_large_norm_tail_absorption(self):
        for q in range(1,5):
            beta=q*(q+7)//2; M=3+beta
            for r in (F(1,2),F(1,4),F(1,16)):
                for eta in (F(0),r*r,r,F(1)):
                    self.assertLessEqual(r**M,r**3*(eta+r)**beta)

    def test_limiting_measure_does_not_supply_diagonal_rate(self):
        ratios=[]
        for r in (F(1,2),F(1,4),F(1,8),F(1,16)):
            mass=r**4/4+r**2
            self.assertEqual(mass/r**4,F(1,4)+1/(r*r))
            ratios.append(mass/r**4)
        self.assertTrue(all(x<y for x,y in zip(ratios,ratios[1:])))

    def test_degree_mutants_are_detected(self):
        for p in range(2,6):
            required=3*p+p*(p-1)//2
            for mutant in ('drop_saddle','drop_vandermonde'):
                got=soft_integral(p,mutant)
                self.assertNotIn(required,got)
                self.assertEqual(set(got),{required-1})

    def test_saddle_r_term_cannot_be_dropped_below_r(self):
        ratios=[]
        for r in (F(1,2),F(1,4),F(1,8)):
            eta=r*r
            integral=eta**3/3+r*eta*eta/2
            ratios.append(integral/eta**3)
            self.assertEqual(integral/eta**3,F(1,3)+1/(2*r))
        self.assertTrue(ratios[0]<ratios[1]<ratios[2])


    def test_mixed_power_vector_recovers_equal_width(self):
        for q in range(1,13):
            weights=mixed_power_vector(q)
            self.assertEqual(weights,tuple(range(4,q+4)))
            self.assertEqual(sum(weights),q*(q+7)//2)
        self.assertEqual(mixed_power_vector(0),())

    def test_mixed_radial_exponents_and_saturation(self):
        self.assertEqual(mixed_radial_exponent((F(1,2),F(1,4))),F(25,4))
        self.assertEqual(mixed_radial_exponent((F(2),F(3))),F(12))
        for q in range(1,7):
            for a in (F(1,4),F(1,2),F(1),F(3,2)):
                self.assertEqual(mixed_radial_exponent((a,)*q),3+q*(q+7)//2*min(a,1))
        with self.assertRaises(ValueError): mixed_radial_exponent((F(0),))
        with self.assertRaises(ValueError): mixed_power_vector(-1)

    def test_mixed_vandermonde_bound_on_ordered_domain(self):
        from itertools import combinations
        for p in range(2,5):
            for xs in combinations([F(j,12) for j in range(1,9)],p):
                actual=F(1); upper=F(1)
                for i in range(p):
                    for j in range(i+1,p): actual*=xs[j]-xs[i]
                for j in range(1,p): upper*=xs[j]**j
                self.assertLessEqual(actual,upper)
        self.assertNotEqual(3+4*F(1,2)+5*F(1,4),3+4*F(1,4)+5*F(1,2))

if __name__ == '__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(FiniteRadiusAlgebra)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    rows=[dict(p=p,exponent=3*p+p*(p-1)//2,
               exact_coefficient=str(next(iter(soft_integral(p).values())))) for p in range(1,6)]
    print(json.dumps({'scope':'exact algebra only; no analytic or kernel acceptance',
                      'tests':result.testsRun,'soft_integrals':rows},indent=2))
