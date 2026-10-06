import importlib.util
import pathlib
import unittest
from decimal import Decimal

class CertificateTests(unittest.TestCase):
    def test_00_checker_exists(self):
        self.assertTrue(pathlib.Path(__file__).with_name('certificate.py').is_file(),
                        'missing outward anisotropic coefficient checker')

    def load(self):
        p=pathlib.Path(__file__).with_name('certificate.py')
        self.assertTrue(p.exists(), 'checker not implemented')
        spec=importlib.util.spec_from_file_location('certificate',p)
        m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        return m

    def test_reference_cone(self):
        m=self.load(); I=m.I
        B=[[I('0.6'),I(0),I(0)],[I(0),I(1),I(0)],[I(0),I(0),I(1)]]
        d,e,meta=m.cone(B)
        ref=I(29)/6-I(6).sqrt()
        self.assertLessEqual(d.lo-e.hi,ref.hi)
        self.assertGreaterEqual(d.hi+e.hi,ref.lo)
        self.assertLess(d.hi-d.lo+2*e.hi,Decimal('1e-35'))
        self.assertLess(d.hi,Decimal(29)/6)

    def test_rounding_and_guards(self):
        m=self.load(); I=m.I
        z=I(1)/3
        self.assertLessEqual(z.lo*3,1)
        self.assertGreaterEqual(z.hi*3,1)
        self.assertLessEqual((I(-2,3)**2).lo,0)
        self.assertGreaterEqual((I(-2,3)**2).hi,9)
        with self.assertRaises((ValueError,TypeError)): I(0.1)
        with self.assertRaises((ValueError,ZeroDivisionError)): I(1)/I(-1,1)
        with self.assertRaises(ValueError): I(-1).sqrt()

    def test_long_exact_input_power_is_outward(self):
        from fractions import Fraction
        m=self.load(); x=Decimal("1."+"0"*75+"1")
        z=m.I(x)**2; exact=Fraction(x)**2
        self.assertLessEqual(Fraction(z.lo),exact)
        self.assertGreaterEqual(Fraction(z.hi),exact)

    def test_moments_and_uniform_bounds(self):
        m=self.load(); p=m.parameters(4)
        self.assertLess(p['a'].lo,Decimal('0.989272393327749635'))
        self.assertGreater(p['a'].hi,Decimal('0.989272393327749634'))
        self.assertGreater(p['Tmin'].lo,Decimal('4.58'))
        self.assertLess(p['Tmax'].hi,Decimal('6.02'))
        self.assertGreater(p['Bmin'].lo,Decimal('0.57'))
        self.assertLess(p['tail'].hi,Decimal('1e-400'))

    def test_reference_angular_normalization(self):
        m=self.load(); r=m.integrate(4,reference=True)
        self.assertLessEqual(Decimal(r['ratio_interval'][0]),1)
        self.assertGreaterEqual(Decimal(r['ratio_interval'][1]),1)
        self.assertEqual(Decimal(r['error_bounds']['angular_ratio']),0)

    def test_square_symmetry_and_frame(self):
        m=self.load(); p=m.parameters(4)
        t=m.PI/7; ph=m.PI/9
        x,e,_=m.direction(t,ph,p)
        y,f,_=m.direction(t,m.PI/2-ph,p)
        self.assertLessEqual(x.lo-e.hi,y.hi+f.hi)
        self.assertLessEqual(y.lo-f.hi,x.hi+e.hi)

if __name__=='__main__': unittest.main()
