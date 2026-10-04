from fractions import Fraction as F
import unittest
import oracle as o

class FirstTests(unittest.TestCase):
    def test_pi(self):
        a,b=o.pi_bounds();self.assertTrue(F('3.14159265358979323846264338327950288')<a<b<F('3.14159265358979323846264338327950289'))
    def test_log(self):
        a,b=o.log_bounds(F(2));self.assertTrue(F('0.69314718055994530941723212145817656')<a<b<F('0.69314718055994530941723212145817657'))
    def test_exp(self):
        a,b=o.exp_bounds(F(1));self.assertTrue(F('2.71828182845904523536028747135266249')<a<b<F('2.71828182845904523536028747135266250'))
    def test_root(self):
        a,b=o.root_bounds(F(12),6);self.assertTrue(a**6<=12<=b**6);self.assertLess(b-a,F(1,10**60))
    def test_gamma_half(self):
        a,b=o.gamma_bounds(F(1,2));p,q=o.root_iv(o.pi_bounds(),2);self.assertTrue(a<=q and p<=b);self.assertLess(b-a,F(1,10**40))
    def test_nine_published_enclosures(self):
        values=o.coefficients();self.assertEqual(len(values),9)
        for k,iv in values.items():
            lo,hi=map(F,o.PUBLISHED[k]);self.assertTrue(lo<iv[0]<=iv[1]<hi,(k,iv));self.assertLess(iv[1]-iv[0],F(1,10**40))


class IndependentControls(unittest.TestCase):
    def test_exact_bernoulli_numbers(self):
        self.assertEqual([o.bernoulli(n) for n in (0,1,2,4,6,10,12,22)], [F(1),-F(1,2),F(1,6),-F(1,30),F(1,42),F(5,66),-F(691,2730),F(854513,138)])
    def test_gamma_recurrence(self):
        for x in (F(1,6),F(5,6),F(1,2),F(2)):
            a=o.times((x,x),o.gamma_bounds(x));b=o.gamma_bounds(x+1)
            self.assertTrue(a[0]<=b[1] and b[0]<=a[1])
    def test_gamma_reflection(self):
        a=o.times(o.gamma_bounds(F(1,6)),o.gamma_bounds(F(5,6)));b=o.times((F(2),F(2)),o.pi_bounds())
        self.assertTrue(a[0]<=b[1] and b[0]<=a[1])
    def test_gamma_integers(self):
        for x,ans in ((1,1),(2,1),(5,24)):
            a,b=o.gamma_bounds(F(x));self.assertTrue(a<=ans<=b)
    def test_log_reduction(self):
        for x in (F(1,7),F(7),F(97,13)):
            a=o.plus(o.log_bounds(x),o.log_bounds(1/x));self.assertTrue(a[0]<=0<=a[1])
    def test_log_multiplication(self):
        a=o.plus(o.log_bounds(F(2)),o.log_bounds(F(3)));b=o.log_bounds(F(6));self.assertTrue(a[0]<=b[1] and b[0]<=a[1])
    def test_exp_reciprocal(self):
        a=o.times(o.exp_bounds(F(7,5)),o.exp_bounds(-F(7,5)));self.assertTrue(a[0]<=1<=a[1])
    def test_exp_log(self):
        for x in (F(1,3),F(3),F(12)):
            a=o.exp_iv(o.log_bounds(x));self.assertTrue(a[0]<=x<=a[1])
    def test_exact_root(self):
        self.assertEqual(o.root_bounds(F(4),2),(F(2),F(2)))
        self.assertEqual(o.root_bounds(F(64),6),(F(2),F(2)))
    def test_radical_brackets(self):
        for x in (F(2),F(6),F(12),F(13,71)):
            for n in (2,3,6):
                lo,hi=o.root_bounds(x,n);self.assertTrue(lo**n<=x<=hi**n);self.assertLessEqual(hi-lo,F(1,o.SCALE))
    def test_all_corner_arithmetic(self):
        for a in ((-F(5,7),F(2,3)),(F(1,11),F(2,7)),(-F(3),-F(1))):
            for b in ((-F(2),F(3)),(F(1,19),F(7,9)),(-F(7,3),-F(1,8))):
                for op,fn in ((o.plus,lambda x,y:x+y),(o.minus,lambda x,y:x-y),(o.times,lambda x,y:x*y)):
                    lo,hi=op(a,b)
                    for x in a:
                        for y in b:self.assertTrue(lo<=fn(x,y)<=hi)
                if not b[0]<=0<=b[1]:
                    lo,hi=o.over(a,b)
                    for x in a:
                        for y in b:self.assertTrue(lo<=x/y<=hi)
    def test_outward_rounding_signs(self):
        for x in (F(1,3),-F(1,3),F(1,10**100),-F(1,10**100)):
            a,b=o.enclosure(x);self.assertTrue(a<=x<=b)
    def test_outward_decimal(self):
        for x in ((F(1,3),F(2,3)),(-F(2,3),-F(1,3))):
            a,b=map(F,o.decimal_pair(x,50));self.assertTrue(a<=x[0]<=x[1]<=b)
    def test_alternative_atoms(self):
        one=o.coefficients()['1.c2'];base=o.over(o.gamma_bounds(F(5,6)),o.power(o.root_bounds(F(12),6),5));den=o.times(o.pi_bounds(),o.root_iv(o.pi_bounds(),2));other=o.over(o.times((F(9),F(9)),base),den)
        self.assertTrue(one[0]<=other[1] and other[0]<=one[1])
    def test_ratio_closed_forms(self):
        base=o.over(o.gamma_bounds(F(5,6)),o.times(o.power(o.root_bounds(F(12),6),4),o.gamma_bounds(F(1,6))))
        ks={1:(F(54),F(54)),2:(F(78),F(78)),3:o.times((F(18,25),F(18,25)),o.minus((F(141),F(141)),o.root_bounds(F(6),2)))}
        for d,k in ks.items():
            a=o.times(k,base);b=o.coefficients()[f'{d}.ratio'];self.assertTrue(a[0]<=b[1] and b[0]<=a[1])
    def test_negative_cone_term_load_bearing(self):
        d3=o.coefficients()['3.c'];base=o.over(o.gamma_bounds(F(1,6)),o.root_bounds(F(12),6));p=o.power(o.pi_bounds(),2);p=o.times(p,o.root_iv(o.pi_bounds(),2));bad=o.over(o.times((F(29,72),F(29,72)),base),p)
        self.assertGreater(bad[0],d3[1])
    def test_cached_rational_cannot_admit_float_alias(self):
        for func in (o.log_bounds,o.lngamma_bounds,o.gamma_bounds):
            func.cache_clear()
            func(F(1,2))
            with self.subTest(function=func.__name__),self.assertRaises(TypeError):
                func(0.5)
            func(F(1))
            with self.subTest(function=func.__name__),self.assertRaises(TypeError):
                func(True)

    def test_domain_rejections(self):
        for x in (True,0.5,'1/6'):
            with self.assertRaises(TypeError):o.gamma_bounds(x)
        with self.assertRaises(ValueError):o.log_bounds(F(0))
        with self.assertRaises(ValueError):o.gamma_bounds(F(-1,6))
        with self.assertRaises(ValueError):o.root_bounds(-F(1),2)
        with self.assertRaises(ValueError):o.over((F(1),F(1)),(-F(1),F(1)))
    def test_declared_float_free(self):
        values=o.coefficients()
        self.assertTrue(all(type(x) is F for ab in values.values() for x in ab))
    def test_numerical_interval_shrink_mutant(self):
        for key,iv in o.coefficients().items():
            midpoint=sum(iv)/2
            false_upper=midpoint-F(1,10**30)
            self.assertFalse(iv[1]<=false_upper)

if __name__=='__main__':unittest.main()
