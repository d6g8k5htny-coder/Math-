"""Independent finite exact fixtures for PUNCTURED_PIN_PROOF.md.

The continuum, Gaussian supremum moments, Fourier tail and Kac--Rice theorem
are NOT verified by these finite tests. All arithmetic here is rational.
"""
from fractions import Fraction as F
import itertools
import unittest
import pin_frame as subject


def derivative(poly, axis):
    out={}
    for powers,coef in poly.items():
        if powers[axis]:
            lower=list(powers); lower[axis]-=1
            out[tuple(lower)]=coef*powers[axis]
    return out

def evaluate(poly,x,z):
    return sum((v*x**a*z**b for (a,b),v in poly.items()),F(0))

def fixture(r,k,a4,t,s,c,d,birth=F(7,5)):
    # Actual physical polynomial, before substitution x=rp,z=rq.
    return {(0,0):birth,(3,0):2*k-a4*r/12,
        (2,0):-3*k*r+a4*r*r/24,(4,0):a4/24,
        (2,1):t/2,(1,1):-r*t/2,(0,2):s/2,(1,2):c/2,(0,3):d/6}

def minor(rows,i,j):
    return rows[0][i]*rows[1][j]-rows[0][j]*rows[1][i]

def gram_det(rows):
    a=sum(x*x for x in rows[0]); b=sum(x*y for x,y in zip(*rows))
    c=sum(x*x for x in rows[1])
    return a*c-b*b

class PinFrameTests(unittest.TestCase):
    def test_axis_quartic_column_is_not_zero(self):
        rows=subject.frame_rows(F(1,8),F(0),F(1),F(0))
        self.assertNotEqual(minor(rows,0,1),0)

    def test_all_three_minors(self):
        for p,q,(alpha,beta) in itertools.product(
            [F(-1,4),F(-1,16),F(0),F(1,16),F(1,4)],
            [F(-1,4),F(0),F(1,128)],
            [(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-3,5),F(4,5)),(F(3,5),F(-4,5))]):
            with self.subTest(p=p,q=q,alpha=alpha,beta=beta):
                rows=subject.frame_rows(p,q,alpha,beta)
                a=(p-1)*(2*p-1)/12; b=(p-1)/2; c=p-F(1,2)
                self.assertEqual(minor(rows,0,1),a*b*alpha**2)
                self.assertEqual(minor(rows,0,2),a*alpha*beta)
                self.assertEqual(minor(rows,1,2),c*beta**2)

    def test_cauchy_binet_floor_at_rational_compactification(self):
        for p,q,(alpha,beta) in itertools.product(
            [F(i,16) for i in range(-4,5)],
            [F(-1,4),F(0),F(1,2**50)],
            [(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1)),
             (F(3,5),F(4,5)),(F(-3,5),F(4,5)),(F(3,5),F(-4,5)),(F(-3,5),F(-4,5))]):
            rows=subject.frame_rows(p,q,alpha,beta)
            self.assertEqual(gram_det(rows),sum(minor(rows,i,j)**2 for i in range(4) for j in range(i+1,4)))
            self.assertGreaterEqual(gram_det(rows),F(9,131072))

    def test_exact_gradient_against_physical_polynomial(self):
        for r,k,(a4,t,s,c,d),p,q in itertools.product(
            [F(1,8),F(1,64)], [F(1),F(6,5),F(-1),F(-6,5)],
            [(F(1),F(-2),F(3),F(4),F(-1)),(F(-3),F(1),F(-2),F(0),F(5))],
            [F(-1,4),F(0),F(1,8),F(1,2**40)],
            [F(-1,8),F(0),F(1,2**45)]):
            poly=fixture(r,k,a4,t,s,c,d)
            actual=(evaluate(derivative(poly,0),r*p,r*q)/r**2,
                    evaluate(derivative(poly,1),r*p,r*q)/r)
            self.assertEqual(subject.gradient_numerators(r,k,p,q,(a4,t,s,c,d)),actual)

    def test_endpoint_frame_target_and_raw_invertibility(self):
        r=F(1,17); birth=F(8,5); k=F(6,5)
        data=(birth,F(0),F(0),birth-k*r**3,F(0),F(0))
        self.assertEqual(subject.endpoint_frame(r,data),(birth,F(0),F(0),F(0),-12*k,F(0)))
        # Independently invert the six linear frame rows for arbitrary data.
        raw=(F(2),F(3),F(5),F(7),F(11),F(13))
        e=subject.endpoint_frame(r,raw)
        g0,gp0,h0,dgp,defect,dh=e
        gpr=gp0+r*dgp; hr=h0+r*dh
        gr=g0+r*(gpr+gp0)/2+r**3*defect/12
        self.assertEqual((g0,gp0,h0,gr,gpr,hr),raw)

    def test_relative_longitudinal_remainder_retains_p(self):
        for r,p in itertools.product([F(1,8),F(1,256)],
                 [F(-1,4),F(0),F(1,4),F(1,2**60),F(-1,2**60)]):
            # u=x^2(x-r)^2(x+2r), whose fourth derivative at zero is zero.
            poly={(5,0):F(1),(3,0):-3*r*r,(2,0):2*r**3}
            actual=evaluate(derivative(poly,0),r*p,F(0))
            self.assertEqual(subject.relative_remainder(r,p),actual)
            self.assertLessEqual(abs(actual),7*r**4*abs(p))
            for x in [F(0),r]:
                self.assertEqual(evaluate(poly,x,F(0)),0)
                self.assertEqual(evaluate(derivative(poly,0),x,F(0)),0)

    def test_transverse_remainder_retains_p(self):
        for r,p in itertools.product([F(1,8),F(1,64)], [F(0),F(1,4),F(1,2**60),F(-1,4)]):
            poly={(3,0):F(1),(1,0):-r*r}
            self.assertEqual(evaluate(poly,r*p,F(0)),r**3*p*(p*p-1))
            self.assertLessEqual(abs(evaluate(poly,r*p,F(0))),r**3*abs(p))

    def test_axis_allowed_but_conditioned_pin_excluded(self):
        self.assertTrue(subject.valid_point(F(1,8),F(1,2**60),F(0)))
        self.assertTrue(subject.valid_point(F(1,8),F(0),F(1,2**60)))
        self.assertFalse(subject.valid_point(F(1,8),F(0),F(0)))
        self.assertFalse(subject.valid_point(F(0),F(1,8),F(0)))
        self.assertFalse(subject.valid_point(F(1,8),F(1,4),F(1,4)))

    def test_outer_slope_and_inner_axis_ratio_bounds(self):
        for r,p,q in itertools.product([F(1,4),F(1,32),F(1,256)],
                [F(-1,8),F(0),F(1,2**30)],
                [F(-1,16),F(0),F(1,2**40)]):
            if p==q==0: continue
            delta2=q*q+r*r*p*p; chi2=p*p/delta2
            if abs(q)>=r*abs(p):
                t2=p*p/(q*q)
                self.assertGreaterEqual(chi2,t2/2)
                self.assertLessEqual(chi2,t2)
                self.assertLessEqual(q*q/delta2,1)
            else:
                self.assertGreaterEqual(chi2,1/(2*r*r))
                self.assertLessEqual(chi2,1/(r*r))
                self.assertLessEqual((p*p+q*q)/delta2,2/(r*r))

    def test_scale_ledger_has_one_normalizer_and_no_height_factor(self):
        self.assertEqual(subject.scale_ledger(),{
            'outer_intensity':1,'axial_prefactor':-10,'axial_after_sixth_term':2,
            'fixed_scaled_area_count':3,'nested_scaled_area_count':5,
            'height_window_factors':0,'endpoint_normalizers':1})

    def test_no_squared_triangle_area_error(self):
        # Exact right triangles make sigma=1, d/r varies down to 2^-30.
        for ratio in [F(1,4),F(1,32),F(1,2**30)]:
            r=F(1,8); d=r*ratio
            coarse=F(1,4)*4*F(1,2)*r**4*d*d
            self.assertLessEqual(coarse,r**4*d*d)
            # f=x^3/3-rx^2/2+z^3/3-dz^2/2, L=2.
            exact_product=(r*d)**3
            self.assertLessEqual(exact_product,2**6*r**4*d*d)

if __name__=='__main__':
    unittest.main(verbosity=2)
