"""Finite exact algebra tests; not continuum Gaussian certification."""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import unittest
import remote_window as m


class ExactControls(unittest.TestCase):
    def test_refuses_inexact_inputs(self):
        for x in (True, False, 0.5, '1/2', None):
            with self.assertRaises(TypeError): m.exact(x)

    def test_matrix_shape_and_symmetry(self):
        for a in ([], [[1,2]], [[1,2],[3,4]]):
            with self.assertRaises(ValueError): m.symmetric(a)

    def test_determinants(self):
        self.assertEqual(m.determinant([[0,2],[3,4]]), -6)
        self.assertEqual(m.determinant([[1,2,3],[2,4,6],[0,0,1]]),0)
        self.assertEqual(m.determinant([[2,1,0],[1,3,1],[0,1,4]]),18)

    def test_inertia_diagonal(self):
        self.assertEqual(m.inertia([[-2,0,0],[0,0,0],[0,0,3]]),(1,1,1))
        self.assertEqual(m.inertia([[1,0],[0,2]]),(0,0,2))

    def test_inertia_zero_diagonal_pivot(self):
        self.assertEqual(m.inertia([[0,2],[2,0]]),(1,0,1))
        self.assertEqual(m.inertia([[0,1,0],[1,0,0],[0,0,0]]),(1,1,1))
        self.assertEqual(m.inertia([[0,1,2],[1,0,3],[2,3,0]]),(2,0,1))

    def test_inertia_congruence(self):
        for a,b,c in product((-2,0,3),repeat=3):
            # P=[[1,1,0],[0,1,1],[0,0,1]], so P^T diag(a,b,c) P below.
            h=[[a,a,0],[a,a+b,b],[0,b,b+c]]
            self.assertEqual(m.inertia(h),(sum(v<0 for v in (a,b,c)),sum(v==0 for v in (a,b,c)),sum(v>0 for v in (a,b,c))))

    def test_filtered_det_type(self):
        a=[[-2,0],[0,3]]
        self.assertEqual(m.typed_det(a,1),6)
        self.assertEqual(m.typed_det(a,2),0)
        self.assertEqual(m.typed_det([[0,0],[0,-1]],1),0)
        with self.assertRaises(ValueError): m.typed_det(a,True)

    def test_adjugate_singular_transverse(self):
        self.assertEqual(m.quadratic_slope([[0,0],[0,2]],[3,4]),18)
        self.assertEqual(m.quadratic_slope([[0]],[3]),9)

    def test_affine_determinant(self):
        a=[[2,1],[1,0]]; beta=(1,2)
        for s in (0,Q(1,3),1,2):
            self.assertEqual(m.determinant(m.block(3,beta,a,s)),3*m.determinant(a)-s*s*m.quadratic_slope(a,beta))

    def test_index_crossing_bound(self):
        # [[1,s],[s,1]] changes inertia at s=1.
        for s in (Q(1,2),1,2):
            for j in range(3):
                self.assertTrue(m.block_bound(1,[1],[[1]],s,j)['holds'])
        self.assertEqual(m.block_bound(1,[1],[[1]],2,1)['lhs'],3)

    def test_singular_index_bound(self):
        for a in ([[0]],[[0,0],[0,-2]],[[0,1],[1,0]]):
            beta=[1]*len(a)
            for j in range(len(a)+2):
                self.assertTrue(m.block_bound(0,beta,a,Q(1,2),j)['holds'])

    def test_matrix_grid(self):
        checks=0
        for a0,alpha,beta,s in product((-1,0,2),(-2,0,1),(-1,1),(Q(1,2),1)):
            for j in range(3):
                self.assertTrue(m.block_bound(alpha,[beta],[[a0]],s,j)['holds'])
                checks+=1
        self.assertEqual(checks,108)

    def test_congruence_radius_factor(self):
        r=Q(1,4); h=[[-r,r],[r,-2]]
        k=[[-1,Q(1,2)],[Q(1,2),-2]]
        self.assertEqual(m.determinant(h),r*m.determinant(k))
        self.assertEqual(m.inertia(h),m.inertia(k))

    def test_inverse_and_schur(self):
        self.assertEqual(m.inverse([[2,1],[1,2]]),((Q(2,3),Q(-1,3)),(Q(-1,3),Q(2,3))))
        mu,c=m.conditional([[2,1],[1,3]],[4])
        self.assertEqual(mu,(Q(2),)); self.assertEqual(c,((Q(5,2),),))

    def test_joint_residual_correlation_retained(self):
        _,c=m.conditional([[2,1,1],[1,3,2],[1,2,3]],[0])
        self.assertEqual(c,((Q(5,2),Q(3,2)),(Q(3,2),Q(5,2))))
        self.assertEqual(m.square_product_moment(c[0][0],c[1][1],c[0][1]),Q(43,4))
        self.assertNotEqual(Q(43,4),c[0][0]*c[1][1])

    def test_bad_conditioning_refused(self):
        for c,t in (([[1,1],[1,1]],[0]),([[1,0],[0,1]],[]),([[1,0],[0,1]],[0,0])):
            with self.assertRaises(ValueError): m.conditional(c,t)

    def test_pin_determinant(self):
        for d in (2,3,4,5):
            for r in (Q(1,2),Q(1,10)):
                self.assertEqual(abs(m.determinant(m.pin_transform(d,r))),12/r**(d+3))

    def test_pin_target(self):
        for d in (2,3):
            r,b,k=Q(1,10),Q(6,5),Q(1,6)
            expected=(b-k*r**3/2,-k*r**2,Q(0),12*k,*([Q(0)]*(2*(d-1))))
            self.assertEqual(m.transformed_target(d,r,b,k),expected)

    def test_centered_fifth_degree(self):
        r=Q(2,5); a=-r/2; c=r/2
        v=(a**5,5*a**4,c**5,5*c**4,0,0)
        transformed=tuple(sum(x*y for x,y in zip(row,v)) for row in m.pin_transform(2,r))
        self.assertEqual(transformed[3],3*r*r)

    def test_window_cubic_width(self):
        self.assertEqual(m.window_length(Q(1,10),Q(1,6)),Q(1,6000))
        with self.assertRaises(ValueError): m.window_length(1,0)

    def test_window_polynomial(self):
        r,k=Q(1,2),Q(2); w=k*r**3
        self.assertEqual(m.window_polynomial([3,2,6],r,k),3*w+w*w+2*w**3)

    def test_single_count_ledger(self):
        result=m.count_ledger(1)
        self.assertEqual(result['numerator_power'],5)
        self.assertEqual(result['mean_power'],3)
        self.assertEqual(result['determinant_factors'],3)
        self.assertEqual(result['normalizers'],1)

    def test_separated_factorial_ledger(self):
        for q in range(2,9):
            data=m.count_ledger(q)
            self.assertEqual(data['mean_power'],3*q)
            self.assertEqual(data['determinant_factors'],q+2)
            self.assertEqual(data['endpoint_weights'],1)
        self.assertEqual(m.count_ledger(3)['unordered_divisor'],6)

    def test_scope_fixed_radius(self):
        s=m.FixedRemoteScope(2,Q(24),Q(1))
        s.check_radius(Q(1,10))
        for r in (0,2):
            with self.assertRaises(ValueError): s.check_radius(r)
        for rho in (0,6):
            with self.assertRaises(ValueError): m.FixedRemoteScope(2,Q(24),Q(rho))

    def test_torus_distance_and_remote_membership(self):
        s=m.FixedRemoteScope(2,Q(24),Q(1))
        self.assertEqual(s.distance_squared((23,0),(0,0)),1)
        self.assertTrue(s.contains((23,0)))
        self.assertFalse(s.contains((Q(1,2),0)))

    def test_mutually_separated_domain(self):
        s=m.FixedRemoteScope(2,Q(24),Q(1))
        self.assertTrue(s.tuple_allowed(((2,0),(4,0)),1))
        self.assertFalse(s.tuple_allowed(((2,0),(2,0)),1))
        self.assertFalse(s.tuple_allowed(((0,0),(4,0)),1))
        with self.assertRaises(ValueError): s.tuple_allowed(((2,0),(4,0)),0)

    def test_mean_scaling_exact_model(self):
        # Analytic test kernel 5+2r+depth; NOT a realization of the Gaussian field.
        for r in (Q(1,10),Q(1,20),Q(1,100)):
            k=Q(1,6)
            integral=m.window_polynomial([5+2*r,1],r,k)
            scaled=integral/(k*r**3)
            self.assertEqual(scaled-5,2*r+k*r**3/2)
            self.assertLessEqual(scaled-5,3*r)

    def test_metadata_scope_and_output(self):
        data=m.result()
        self.assertFalse(data['gaussian_integral_numerically_evaluated'])
        self.assertFalse(data['legacy_RN_24jet_discharged'])
        self.assertFalse(data['independent_analytic_acceptance'])
        self.assertEqual(data,json.loads(Path(__file__).with_name('RESULTS.json').read_text()))


if __name__=='__main__':
    unittest.main()
