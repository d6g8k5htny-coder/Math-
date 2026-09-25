from fractions import Fraction as Q
import unittest
import pin_compatibility as m


class PinCompatibility(unittest.TestCase):
    def test_left_height(self):
        for r in (Q(1,3),Q(1,10),Q(1,100)):
            p=m.family(r,k=Q(6,5),b=2,a=3,c=4,d=5,D=7)
            self.assertEqual(m.derivative(p,-r/2,0),2)

    def test_right_height(self):
        r=Q(1,10);k=Q(6,5);p=m.family(r,k,b=2,a=3,c=4,d=5,D=7)
        self.assertEqual(m.derivative(p,r/2,0),2-k*r**3)

    def test_longitudinal_gradient_pins(self):
        r=Q(1,10);p=m.family(r,k=Q(6,5),a=3,c=4,d=5,D=7)
        for x in (-r/2,r/2):self.assertEqual(m.derivative(p,x,0,1,0),0)

    def test_transverse_gradient_pins(self):
        r=Q(1,10);p=m.family(r,a=3,c=4,d=5,D=7)
        for x in (-r/2,r/2):self.assertEqual(m.derivative(p,x,0,0,1),0)

    def test_endpoint_types_do_not_remove_witness(self):
        r=Q(1,10);p=m.family(r,A=-2)
        hm=m.hessian(p,-r/2,0);hs=m.hessian(p,r/2,0)
        self.assertLess(hm['xx'],0);self.assertGreater(hm['det'],0)
        self.assertLess(hs['det'],0)

    def test_midpoint_offsets(self):
        r=Q(1,10);k=Q(6,5);a=Q(3);D=Q(7);b=Q(2)
        p=m.family(r,k,b=b,a=a,D=D)
        self.assertEqual(m.derivative(p,0,0),b-k*r**3/2+D*r**4/384)
        self.assertEqual(m.derivative(p,0,0,1,0),-3*k*r**2/2)
        self.assertEqual(m.derivative(p,0,0,2,0),-D*r**2/24)
        self.assertEqual(m.derivative(p,0,0,3,0),12*k)
        self.assertEqual(m.derivative(p,0,0,0,1),-a*r**2/8)
        self.assertEqual(m.derivative(p,0,0,1,1),0)

    def test_scaled_transverse_fx_exact(self):
        r=Q(1,17);y1=Q(2);y2=Q(1,3)
        p=m.family(r,k=2,A=-3,a=4,c=5,d=6)
        rows=m.corrected_rows(y1,y2,k=2,A=-3,a=4,c=5,d=6)
        self.assertEqual(m.derivative(p,r*y1,r*y2,1,0)/r**2,rows['grad_x_r2'])

    def test_scaled_transverse_fz_exact(self):
        r=Q(1,17);y1=Q(2);y2=Q(1,3)
        p=m.family(r,k=2,A=-3,a=4,c=5,d=6)
        rows=m.corrected_rows(y1,y2,k=2,A=-3,a=4,c=5,d=6)
        self.assertEqual(m.derivative(p,r*y1,r*y2,0,1),r*rows['grad_z_r1']+r**2*rows['grad_z_r2'])

    def test_height_next_coefficient_exact(self):
        r=Q(1,17);y1=Q(2);y2=Q(1,3);b=Q(7)
        p=m.family(r,k=2,b=b,A=-3,a=4,c=5,d=6)
        rows=m.corrected_rows(y1,y2,k=2,A=-3,a=4,c=5,d=6)
        self.assertEqual(m.derivative(p,r*y1,r*y2)-b,r**2*rows['height_r2']+r**3*rows['height_r3'])

    def test_unshifted_fx_is_disproved(self):
        r=Q(1,10);k=Q(1);y1=Q(2);p=m.family(r,k,A=-2)
        actual=m.derivative(p,r*y1,0,1,0)/r**2
        self.assertEqual(actual,Q(45,2));self.assertNotEqual(actual,6*k*y1**2)
        self.assertEqual(actual-6*k*y1**2,-3*k/2)

    def test_unshifted_axial_fz_is_disproved(self):
        r=Q(1,10);y=Q(2);a=Q(2);p=m.family(r,a=a)
        actual=m.derivative(p,r*y,0,0,1)/r**2
        self.assertEqual(actual,Q(15,4));self.assertNotEqual(actual,a*y**2/2)

    def test_axial_k_is_fixed_not_free(self):
        k=Q(6,5);y=Q(2)
        self.assertGreater(6*k*(y*y-Q(1,4)),0)
        # Varying free mixed jet does not change the leading longitudinal row.
        self.assertEqual(m.corrected_rows(y,0,k=k,a=0)['grad_x_r2'],m.corrected_rows(y,0,k=k,a=99)['grad_x_r2'])

    def test_quartic_noise_first_occurs_at_r3(self):
        r=Q(1,10);k=Q(6,5);y=Q(2);D=Q(7);p=m.family(r,k,D=D)
        leading=r*r*6*k*(y*y-Q(1,4))
        self.assertEqual(m.derivative(p,r*y,0,1,0)-leading,D*r**3*y*(y*y-Q(1,4))/6)
        self.assertEqual(m.derivative(p,0,0,4,0),D)

    def test_quartic_compensating_value(self):
        r=Q(1,10);k=Q(6,5);y=Q(2);D=-36*k/(r*y)
        self.assertEqual(m.derivative(m.family(r,k,D=D),r*y,0,1,0),0)

    def test_invalid_radius_rejected(self):
        with self.assertRaises(ValueError):m.family(0)

    def test_witness_is_not_global_closure(self):
        self.assertFalse(m.witness()['mathematical_program_closed'])


if __name__=='__main__':unittest.main()
