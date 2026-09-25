import unittest
import thin_tube as p
import two_scale as m

class TwoScale(unittest.TestCase):
    def test_rank_survives_both_compactified_endpoints(self):
        rows=m.contact_rows()
        for alpha,beta in [(1,0),(0,1),(0,-1)]:
            evaluated=[[p.substitute(q,{1:p.constant(alpha),2:p.constant(beta),3:p.constant(2)}).get(p.ZERO,0) for q in row] for row in rows]
            minors=[evaluated[0][i]*evaluated[1][j]-evaluated[0][j]*evaluated[1][i] for i,j in [(0,1),(0,2),(1,2)]]
            self.assertGreater(sum(q*q for q in minors),0)


class UniformAlgebra(unittest.TestCase):
    def test_all_45_residual_basis_elements_have_both_uniform_limits(self):
        rows=m.contact_rows(); count=0
        for i in range(9):
            for j in range(9-i):
                f=p.completed_monomial(i,j); count+=1
                jets=[p.midpoint_contact(f,4,0),p.midpoint_contact(f,2,1),p.midpoint_contact(f,0,2)]
                for component in (1,2):
                    expected=p.add(*(p.mul(a,b) for a,b in zip(rows[component-1],jets)))
                    self.assertEqual(m.contact_limit(f,component),expected,(i,j,component))
                    self.assertTrue(all(order>=0 for order in m.normalized_orders(f,component)))
        self.assertEqual(count,45)

    def test_target_is_exact_inverse_delta_drift(self):
        from fractions import Fraction as Q
        expected=p.add(p.scale(p.power(p.u,2),6),p.constant(Q(-3,2)))
        self.assertEqual(m.normalized_orders(p.target_cubic(),1),{-1:expected})
        self.assertEqual(m.normalized_orders(p.target_cubic(),2),{})
        with self.assertRaises(ValueError):m.contact_limit(p.target_cubic(),1)

    def test_all_three_minors_exact(self):
        from fractions import Fraction as Q
        gap=p.add(p.power(p.u,2),p.constant(Q(-1,4)))
        a=p.scale(p.mul(p.u,gap),Q(1,6));b=p.scale(gap,Q(1,2))
        self.assertEqual(m.minors(),[p.mul(p.mul(a,b),p.power(p.x,2)),
                                    p.mul(p.mul(a,p.x),p.z),
                                    p.mul(p.u,p.power(p.z,2))])

    def test_gram_determinant_equals_sum_of_three_squared_minors(self):
        rows=m.contact_rows()
        gram=[[p.add(*(p.mul(rows[i][k],rows[j][k]) for k in range(3))) for j in range(2)] for i in range(2)]
        self.assertEqual(p.determinant(gram),p.add(*(p.power(q,2) for q in m.minors())))

    def test_uniform_lower_bound_identity(self):
        aa,bb=p.power(p.x,2),p.power(p.z,2)
        lhs=p.add(p.scale(p.add(p.power(aa,2),p.power(bb,2)),2),p.scale(p.power(p.add(aa,bb),2),-1))
        self.assertEqual(lhs,p.power(p.add(aa,p.scale(bb,-1)),2))

    def test_original_contact_is_recovered_at_bounded_t_over_r(self):
        # unnormalized (alpha,beta)=(1,v) is the same matrix before the
        # common sqrt(1+v^2) divisor. This is an exact polynomial identity.
        old=p.contact_rows(); rows=m.contact_rows()
        for i in range(2):
            for j in range(3):
                self.assertEqual(p.substitute(rows[i][j],{1:p.constant(1),2:p.v}),old[i][j])

    def test_dropping_longitudinal_jet_loses_axis_rank(self):
        rows=m.contact_rows();rows[0][0]={}
        evaluated=[p.substitute(q,{1:p.constant(1),2:{},3:p.constant(2)}) for q in m.minors(rows)]
        self.assertEqual(evaluated,[{},{},{}])

    def test_dropping_transverse_jet_loses_outer_rank(self):
        rows=m.contact_rows();rows[1][2]={}
        evaluated=[p.substitute(q,{1:{},2:p.constant(1),3:p.constant(2)}) for q in m.minors(rows)]
        self.assertEqual(evaluated,[{},{},{}])

    def test_unsubtracted_transverse_linear_pin_is_rejected(self):
        with self.assertRaises(ValueError):m.contact_limit(p.mul(p.x,p.z),1)

    def test_power_exponents_and_strict_parameter_domain(self):
        from fractions import Fraction as Q
        self.assertEqual(m.power_width_exponent(1),-10)
        self.assertEqual(m.power_width_exponent(Q(1,2)),Q(-13,2))
        for gamma in (0,-1,2,True,0.5):
            with self.assertRaises(ValueError):m.power_width_exponent(gamma)

    def test_normalization_ledger(self):
        # density r^-3 delta^-2, determinants delta^-6, Z^-1 r^-2;
        # integrate dx dz =r^2 du dt.
        self.assertEqual(-3-2+2,-3)
        self.assertEqual(-2-6,-8)

    def test_nonclaims_and_component_rejection(self):
        for key in ('original_proof_changed','analytic_verification_by_tests','independent_review','fixed_scaled_annulus_closed'):
            self.assertIs(m.report()[key],False)
        for component in (0,3,True,'1'):
            with self.assertRaises(ValueError):m.normalized_orders({},component)

if __name__=='__main__': unittest.main()
