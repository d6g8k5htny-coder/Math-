"""Exact sublemma checks for the corrective transverse proof; not continuum review."""
import unittest
from fractions import Fraction as Q
import finite_pin_oracle as o


def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


class TransverseRepairTests(unittest.TestCase):
    def test_joint_height_after_gradient_subtraction(self):
        f=o.family()
        actual=(f-o.b-o.r*o.v*f.diff('y')/2).sub(x=o.r*o.u,y=o.r*o.v)
        expected=(o.k*(2*o.u**3-3*o.u/2-Q(1,2))
                  +o.q*(o.u**2-Q(1,4))*o.v/4-o.d*o.v**3/12)
        self.assertEqual(actual,o.r**3*expected)

    def test_contact_minor_uses_only_unpinned_random_jets(self):
        jx,jy1,_,_,h3=o.contact_rows()
        j3=o.k*(2*o.u**3-3*o.u/2-Q(1,2))+o.q*(o.u**2-Q(1,4))*o.v/4-o.d*o.v**3/12
        minor=det3([[row.diff(name) for name in ('a','c','d')]
                    for row in (jx,jy1,j3)])
        self.assertEqual(minor,o.v**6/24)

    def test_forward_joint_observation_jacobian_and_count_powers(self):
        # Inverse affine map: fx=r^2 J1, fy=r J2, f=b+r^3 J3+r^2 v J2/2.
        forward=det3([[o.r**2,0,0],[0,o.r,0],[0,o.r**2*o.v/2,o.r**3]])
        self.assertEqual(forward,o.r**6)
        self.assertEqual(2+3-6+6-2,3)

    def test_three_gradient_constraints_force_scaled_hessians_in_exact_family(self):
        # Example illustrating the deterministic Hessian power only; no endpoint-type claim.
        f=o.family().sub(k=1,q=0,c=-45,d=156,a=12*o.r)
        self.assertEqual(f.sub(x=-o.r/2,y=0),o.b)
        self.assertEqual(f.sub(x=o.r/2,y=0),o.b-o.r**3)
        for xp,yp in ((-o.r/2,0),(o.r/2,0),(2*o.r,o.r)):
            self.assertEqual(f.diff('x').sub(x=xp,y=yp),0)
            self.assertEqual(f.diff('y').sub(x=xp,y=yp),0)
            for i,j in (('x','x'),('x','y'),('y','y')):
                h=f.diff(i).diff(j).sub(x=xp,y=yp)
                self.assertTrue(all(m[0]>=1 for m in h.terms))
        self.assertEqual(f.sub(x=2*o.r,y=o.r),o.b-o.r**3/2)


if __name__=='__main__':
    unittest.main()
