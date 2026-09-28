"""Exact finite controls for the new same-r height-decoupling argument.

This is not a Gaussian-field simulator or a continuum theorem verifier.
"""
import argparse
from fractions import Fraction as F
import io
import json
import unittest

MUTANT = None

def tv(p, q):
    if len(p) != len(q):
        raise ValueError('matching finite mark spaces required')
    scale = 1 if MUTANT == 'tv-factor' else F(1, 2)
    return scale*sum(abs(a-b) for a,b in zip(p,q))


def own_spatial_product(mu):
    if len(mu) != 4 or any(v < 0 for v in mu):
        raise ValueError('four nonnegative mark masses required')
    mass=sum(mu)
    if mass == 0:
        if MUTANT == 'allow-zero':
            return [F(0)]*4
        raise ValueError('positive mean mass required')
    if MUTANT == 'wrong-marginal':
        return [F(1, 4)]*4
    divisor=F(2) if MUTANT == 'ignore-mass' else 2*mass
    return [(mu[0]+mu[1])/divisor]*2+[(mu[2]+mu[3])/divisor]*2


def normalized_mean(singletons, pair_mass):
    if len(singletons) != 4 or pair_mass < 0 or any(v < 0 for v in singletons):
        raise ValueError('nonnegative configuration weights required')
    mu=list(singletons)
    mu[0] += pair_mass
    if MUTANT != 'drop-pair-weight':
        mu[2] += pair_mass
    mass=sum(mu)
    if mass <= 0:
        raise ValueError('positive mean mass required')
    return [v/mass for v in mu]


class HeightTests(unittest.TestCase):
    def test_probability_tv_half_convention(self):
        self.assertEqual(tv([F(1), F(0)], [F(0), F(1)]), 1)

    def test_equal_probability(self):
        self.assertEqual(tv([F(1, 3), F(2, 3)], [F(1, 3), F(2, 3)]), 0)

    def test_own_not_contact_marginal(self):
        self.assertEqual(own_spatial_product([F(3, 10), F(3, 10), F(1, 5), F(1, 5)]),
                         [F(3, 10), F(3, 10), F(1, 5), F(1, 5)])

    def test_normalization_handles_small_mass(self):
        self.assertEqual(own_spatial_product([F(3, 100), F(3, 100), F(1, 50), F(1, 50)]),
                         [F(3, 10), F(3, 10), F(1, 5), F(1, 5)])

    def test_zero_mass_excluded(self):
        with self.assertRaises(ValueError):
            own_spatial_product([F(0)]*4)

    def test_mean_needs_two_pair_points(self):
        # Four mark bins: A0,A1,B0,B1. A multiple configuration has A0 and B0.
        p = F(1, 100)
        self.assertEqual(normalized_mean([p, 2*p, p, 2*p], p), [F(1, 4)]*4)

    def test_pair_mixture_bound(self):
        for r in (F(1, 2), F(1, 3), F(1, 10)):
            mass = r**3; p2 = r**5/2
            sig = [mass/4-p2, mass/4, mass/4-p2, mass/4]
            p1 = sum(sig)
            mean = normalized_mean(sig, p2)
            single = [v/p1 for v in sig]
            self.assertEqual(mean, [F(1, 4)]*4)
            self.assertEqual(tv(single, mean), r*r/(2*(1-r*r)))
            self.assertLessEqual(tv(single, mean), r*r)

    def test_mean_uniform_does_not_force_singleton_uniform(self):
        r = F(1, 10); mass = r**3; p2 = r**5/2
        sig = [mass/4-p2, mass/4, mass/4-p2, mass/4]
        single = [v/sum(sig) for v in sig]
        self.assertGreater(tv(single, [F(1, 4)]*4), r**3)

    def test_exact_height_change_of_variables(self):
        for r in (F(1, 2), F(1, 7)):
            k = F(6, 5); length = k*r**3
            # An affine within-window density gives TV = slope*length/(8*mean).
            base = F(2); slope = F(3)
            average = base-slope*length/2
            self.assertEqual((slope*length*length/4)/(2*length*average),
                             slope*length/(8*average))

    def test_average_distance_integral(self):
        # Integral_0^1 [theta^2/2+(1-theta)^2/2] dtheta = 1/3.
        self.assertEqual(F(1, 6)+F(1, 6), F(1, 3))

    def test_homogeneous_gradient_pin_cancellation(self):
        # g=x^2*z-r^2*z/4+(x^2-r^2/4)^2. Both values/gradients vanish at M,S.
        for r in (F(1, 2), F(1, 11), F(1, 101)):
            for x in (-r/2, r/2):
                self.assertEqual(x*x-r*r/4, 0)
                self.assertEqual(4*x*(x*x-r*r/4), 0)
                beta = (2*x)/r
                alpha = (12*x*x-r*r)/r
                self.assertEqual(abs(beta), 1)
                self.assertEqual(alpha, 2*r)
                self.assertLessEqual(abs(alpha), 1)

    def test_tv_marginal_contraction(self):
        p=[F(1, 10),F(2, 10),F(3, 10),F(4, 10)]; q=[F(1, 4)]*4
        self.assertLessEqual(tv([p[0]+p[2], p[1]+p[3]], [F(1, 2)]*2), tv(p,q))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutant', choices=['tv-factor', 'wrong-marginal', 'drop-pair-weight', 'ignore-mass', 'allow-zero'])
    args=parser.parse_args()
    global MUTANT
    MUTANT=args.mutant
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(HeightTests)
    result=unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    print(json.dumps({'tests':result.testsRun, 'passed':result.wasSuccessful(),
                     'failures':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.failures),
                     'errors':sorted(t.id().rsplit('.',1)[-1] for t,_ in result.errors)}, sort_keys=True))
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':
    raise SystemExit(main())
