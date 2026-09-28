"""Finite rational laws test the probability algebra, not a Gaussian theorem."""
from fractions import Fraction as F
from itertools import product
import unittest
import finite_law as a


def laws():
    for aa,bb,cc,dd in product(range(3), repeat=4):
        p={():1-F(aa+bb+cc+dd,12),(0,):F(aa,12),(1,):F(bb,12),
           (0,1):F(cc,12),(0,0,1):F(dd,12)}
        if sum(F(len(c))*w for c,w in p.items())<=1:
            yield p


def brute_tv(p,q):
    return sum(abs(p.get(k,F(0))-q.get(k,F(0))) for k in set(p)|set(q))/2


def brute_mean(p):
    return {x:sum(w*c.count(x) for c,w in p.items()) for x in {x for c in p for x in c}}


class FiniteLawTests(unittest.TestCase):
    def test_two_point_sharp_identity(self):
        p={():F(3,4),(0,1):F(1,4)}
        b=a.bernoulli(a.mean_measure(p))
        self.assertEqual(b,{():F(1,2),(0,):F(1,4),(1,):F(1,4)})
        self.assertEqual(a.tv(p,b),F(1,2))
        self.assertEqual(a.multiple_point_mass(p),F(1,2))
        self.assertEqual(a.factorial(p),F(1,2))

    def test_grid_exact_identity_and_factorial_bound(self):
        for p in laws():
            mu=a.mean_measure(p); b=a.bernoulli(mu)
            self.assertEqual(mu,brute_mean(p))
            self.assertEqual(sum(b.values()),1)
            self.assertEqual(a.tv(p,b),brute_tv(p,b))
            h=sum(len(c)*w for c,w in p.items() if len(c)>=2)
            self.assertEqual(a.multiple_point_mass(p),h)
            self.assertEqual(a.tv(p,b),h)
            self.assertLessEqual(h,a.factorial(p))

    def test_conditional_nonempty_configuration_law(self):
        for p in laws():
            mu=a.mean_measure(p); m=sum(mu.values())
            if not m: continue
            one={(x,):w/m for x,w in mu.items()}
            q=a.nonempty(p)
            self.assertEqual(q,{c:w/sum(v for d,v in p.items() if d) for c,w in p.items() if c})
            self.assertEqual(sum(q.values()),1)
            self.assertLessEqual(a.tv(q,one),a.multiple_point_mass(p)/m)

    def test_conditional_unique_location_law(self):
        for p in laws():
            mass=sum(w for c,w in p.items() if len(c)==1)
            if not mass: continue
            mu=a.mean_measure(p); m=sum(mu.values())
            target={(x,):v/m for x,v in mu.items()}
            q=a.unique(p)
            self.assertEqual(sum(q.values()),1)
            self.assertLessEqual(a.tv(q,target),a.multiple_point_mass(p)/m)

    def test_count_tail_and_mean_minus_event(self):
        for p in laws():
            m=sum(a.mean_measure(p).values()); event=sum(v for c,v in p.items() if c)
            tail=sum(v for c,v in p.items() if len(c)>=2); q=a.factorial(p)
            self.assertGreaterEqual(m-event,0)
            self.assertLessEqual(m-event,q/2)
            if event:
                self.assertLessEqual(tail/event,a.conditional_multiple_bound(q,event))
        p={():F(3,4),(0,1):F(1,4)}
        self.assertEqual(a.conditional_multiple_bound(a.factorial(p),F(1,4)),1)

    def test_multiplicity_not_distinct_site_count(self):
        p={():F(7,8),(0,0,1):F(1,8)}
        self.assertEqual(a.mean_measure(p),{0:F(1,4),1:F(1,8)})
        self.assertEqual(a.factorial(p),F(3,4))
        self.assertEqual(a.multiple_point_mass(p),F(3,8))

    def test_mean_one_boundary(self):
        self.assertEqual(a.bernoulli({0:F(2,3),1:F(1,3)}),{():F(0),(0,):F(2,3),(1,):F(1,3)})

    def test_mean_above_one_rejected(self):
        with self.assertRaises(ValueError): a.bernoulli({0:F(5,4)})
        with self.assertRaises(ValueError): a.bernoulli({0:F(-1,4)})

    def test_empty_conditioning_rejected(self):
        self.assertEqual(a.bernoulli({}),{():F(1)})
        with self.assertRaises(ValueError): a.nonempty({():F(1)})
        with self.assertRaises(ValueError): a.unique({():F(3,4),(0,1):F(1,4)})

    def test_bad_law_inputs_rejected(self):
        for p in [{():F(1,2)}, {():F(3,2),(0,):F(-1,2)}, {(1,0):F(1)}, {(True,):F(1)}]:
            with self.assertRaises((TypeError,ValueError)): a.mean_measure(p)
        with self.assertRaises(TypeError): a.mean_measure({():1.0})

    def test_first_moment_does_not_imply_fifth_order_error(self):
        for n in [2,4,16,64]:
            r=F(1,n); p={():1-r**3/2,(0,1):r**3/2}
            self.assertEqual(sum(a.mean_measure(p).values()),r**3)
            self.assertEqual(a.tv(p,a.bernoulli(a.mean_measure(p))),r**3)
            self.assertEqual(a.tv(p,a.bernoulli(a.mean_measure(p)))/r**5,1/r**2)

    def test_mark_dependence_not_independence(self):
        # At site0 only mark0; at site1 only mark1. Encoded marks remain atoms.
        p={():F(3,4),(0,):F(1,8),(3,):F(1,8)}
        self.assertEqual(a.nonempty(p),{(0,):F(1,2),(3,):F(1,2)})
        independent={(0,):F(1,4),(1,):F(1,4),(2,):F(1,4),(3,):F(1,4)}
        self.assertEqual(a.tv(a.nonempty(p),independent),F(1,2))

    def test_normalized_mean_perturbation_bound(self):
        for aa,bb,cc,dd in product(range(1,4),repeat=4):
            mu={0:F(aa,12),1:F(bb,12)}; nu={0:F(cc,12),1:F(dd,12)}
            m=sum(mu.values()); n=sum(nu.values())
            delta=sum(abs(mu[x]-nu[x]) for x in mu)
            self.assertLessEqual(a.tv({x:v/m for x,v in mu.items()},{x:v/n for x,v in nu.items()}),delta/m)
            self.assertLessEqual(a.tv(a.bernoulli(mu),a.bernoulli(nu)),delta)

    def test_explicit_remote_rate_model(self):
        for n in [4,8,16,32,64]:
            r=F(1,n); c=r**5/4
            p={(0,):r**3/3+r**4/4,(1,):2*r**3/3-r**4/4,(0,1):c}
            p[()]=1-sum(p.values()); mu=a.mean_measure(p); m=sum(mu.values())
            self.assertEqual(a.tv(p,a.bernoulli(mu)),r**5/2)
            self.assertLessEqual(a.tv(a.nonempty(p),{(x,):v/m for x,v in mu.items()}),r**2/2)
            self.assertLessEqual(a.tv(a.nonempty(p),{(0,):F(1,3),(1,):F(2,3)}),r)

if __name__=='__main__':unittest.main(verbosity=2)
