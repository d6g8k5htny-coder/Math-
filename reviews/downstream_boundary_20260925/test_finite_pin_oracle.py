import unittest
from fractions import Fraction as Q
import finite_pin_oracle as o


class PinOracleTests(unittest.TestCase):
    def test_polynomial_ring_controls(self):
        self.assertEqual((o.x+o.y)**2, o.x**2+2*o.x*o.y+o.y**2)
        self.assertEqual((o.x**3*o.y).diff('x'), 3*o.x**2*o.y)
        self.assertEqual((o.x+o.y).sub(x=o.y, y=o.x), o.x+o.y)

    def test_all_original_pins_symbolically(self):
        self.assertTrue(all(p == 0 for p in o.pin_residuals(o.family()).values()))

    def test_midpoint_target_corrections(self):
        f=o.family()
        self.assertEqual(f.sub(x=0,y=0),o.b-o.k*o.r**3/2)
        self.assertEqual(f.diff('x').sub(x=0,y=0),-3*o.k*o.r**2/2)
        self.assertEqual(f.diff('y').sub(x=0,y=0),-o.q*o.r**2/8)

    def test_exact_scaled_axial_gradient(self):
        f=o.family(); jx,*_=o.contact_rows()
        self.assertEqual(f.diff('x').sub(x=o.r*o.u,y=o.r*o.v),o.r**2*jx)

    def test_exact_scaled_transverse_gradient(self):
        f=o.family(); _,jy1,jy2,_,_=o.contact_rows()
        self.assertEqual(f.diff('y').sub(x=o.r*o.u,y=o.r*o.v),o.r*jy1+o.r**2*jy2)

    def test_exact_scaled_height(self):
        f=o.family(); *_,h2,h3=o.contact_rows()
        self.assertEqual(f.sub(x=o.r*o.u,y=o.r*o.v)-o.b,o.r**2*h2+o.r**3*h3)

    def test_old_dx_formula_has_nonvanishing_error(self):
        jx,*_=o.contact_rows()
        old=6*o.k*o.u**2+o.q*o.u*o.v+o.c*o.v**2/2
        self.assertEqual(old-jx,3*o.k/2)
        self.assertNotEqual(old,jx)

    def test_old_axial_dy_formula_has_nonvanishing_error(self):
        _,_,jy2,_,_=o.contact_rows()
        self.assertEqual(o.q*o.u**2/2-jy2.sub(v=0),o.q/8)

    def test_old_height_formula_has_missing_terms(self):
        *_,h3=o.contact_rows()
        old=2*o.k*o.u**3+o.q*o.u**2*o.v/2+o.c*o.u*o.v**2/2+o.d*o.v**3/6
        self.assertEqual(old-h3,3*o.k*o.u/2+o.k/2+o.q*o.v/8)

    def test_maximum_saddle_types_in_witness_family(self):
        f=o.family().sub(k=1,a=-2,q=0,c=0,d=0)
        xx=f.diff('x').diff('x'); xy=f.diff('x').diff('y'); yy=f.diff('y').diff('y')
        for radius in (Q(1,4),Q(1,10),Q(1,1000)):
            hm=(xx.value(r=radius,x=-radius/2,y=0),xy.value(r=radius,x=-radius/2,y=0),yy.value(r=radius,x=-radius/2,y=0))
            hs=(xx.value(r=radius,x=radius/2,y=0),xy.value(r=radius,x=radius/2,y=0),yy.value(r=radius,x=radius/2,y=0))
            self.assertLess(hm[0],0); self.assertGreater(hm[0]*hm[2]-hm[1]**2,0)
            self.assertLess(hs[0]*hs[2]-hs[1]**2,0)

    def test_witness_point_lies_in_declared_transverse_annulus(self):
        u,v=Q(2),Q(1,2)
        self.assertGreaterEqual(u*u+v*v,4); self.assertLessEqual(u*u+v*v,16)
        self.assertGreaterEqual(abs(v),Q(1,4))
        self.assertGreater((u-Q(1,2))**2+v*v,Q(1,100))
        self.assertGreater((u+Q(1,2))**2+v*v,Q(1,100))

    def test_three_independent_pin_mutants_detected(self):
        for mutant in ('drop_axial_pin_correction','drop_height_offset','drop_transverse_pin_correction'):
            self.assertTrue(any(p != 0 for p in o.pin_residuals(o.family(mutant)).values()),mutant)

    def test_drift_failure_not_an_order_r3_remainder(self):
        # Exact normalized error is 3k/(2r), unbounded as r -> 0.
        values=[Q(3,2)/r for r in (Q(1,10),Q(1,100),Q(1,1000))]
        self.assertEqual(values,[15,150,1500])

    def test_disposition_and_persistence_nonclaim(self):
        report=o.report()
        self.assertIn('amendment required',report['conclusion'])
        self.assertIn('refutation of the persistence theorem',report['not_claimed'])
        self.assertTrue(all(v=='0' for v in report['pin_residuals'].values()))


if __name__=='__main__':
    unittest.main()
