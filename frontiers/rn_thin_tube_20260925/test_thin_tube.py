import unittest
from fractions import Fraction as F
import thin_tube as m

class ExactChecks(unittest.TestCase):
    def test_scalar_hermite_pin_completion(self):
        self.assertEqual(m.completed_axial_quartic(F(1,10),F(1,20)),0)

    def test_all_45_basis_elements_satisfy_six_pins(self):
        count=0
        for i in range(9):
            for j in range(9-i):
                p=m.completed_monomial(i,j); count+=1
                for sign in (-1,1):
                    sub={1:m.scale(m.r,F(sign,2)),2:{}}
                    for q in (p,m.derivative(p,1),m.derivative(p,2)):
                        self.assertEqual(m.substitute(q,sub),{},(i,j,sign))
        self.assertEqual(count,45)

    def test_target_exact_heights_and_slopes(self):
        p=m.target_cubic()
        for sign in (-1,1):
            sub={1:m.scale(m.r,F(sign,2)),2:{}}
            self.assertEqual(m.substitute(p,sub),{} if sign<0 else m.scale(m.power(m.r,3),-1))
            self.assertEqual(m.substitute(m.derivative(p,1),sub),{})

    def test_target_drift_and_no_third_order_term(self):
        q=m.thin_substitute(m.derivative(m.target_cubic(),1))
        expected=m.add(m.scale(m.power(m.u,2),6),m.constant(F(-3,2)))
        self.assertEqual(m.coefficient_r(q,2),expected)
        self.assertEqual(m.coefficient_r(q,3),{})

    def test_all_axial_residual_orders_and_contact_rows(self):
        row=m.contact_rows()[0]
        for i in range(9):
            for j in range(9-i):
                p=m.completed_monomial(i,j); q=m.thin_substitute(m.derivative(p,1))
                for n in range(3): self.assertEqual(m.coefficient_r(q,n),{},(i,j,n))
                ds=[m.midpoint_contact(p,4,0),m.midpoint_contact(p,2,1),m.midpoint_contact(p,0,2)]
                expected=m.add(*(m.mul(a,b) for a,b in zip(row,ds)))
                self.assertEqual(m.coefficient_r(q,3),expected,(i,j))

    def test_all_transverse_residual_orders_and_contact_rows(self):
        row=m.contact_rows()[1]
        for i in range(9):
            for j in range(9-i):
                p=m.completed_monomial(i,j); q=m.thin_substitute(m.derivative(p,2))
                for n in range(2): self.assertEqual(m.coefficient_r(q,n),{},(i,j,n))
                ds=[m.midpoint_contact(p,4,0),m.midpoint_contact(p,2,1),m.midpoint_contact(p,0,2)]
                self.assertEqual(m.coefficient_r(q,2),m.add(*(m.mul(a,b) for a,b in zip(row,ds))),(i,j))

    def test_contact_rank_minor(self):
        rows=m.contact_rows()
        actual=m.determinant([r[:2] for r in rows])
        gap=m.add(m.power(m.u,2),m.constant(F(-1,4)))
        self.assertEqual(actual,m.scale(m.mul(m.u,m.power(gap,2)),F(1,12)))
        for point in (0,F(1,2),F(-1,2)):
            self.assertEqual(m.substitute(actual,{3:m.constant(point)}),{})

    def test_reference_exact_schur(self):
        self.assertEqual(m.reference_schur(),[[24,0,0],[0,2,0],[0,0,2]])

    def test_reference_contact_covariance_has_positive_algebraic_sum(self):
        rows=m.contact_rows(); d=[24,2,2]
        sigma=[[m.add(*(m.scale(m.mul(rows[i][k],rows[j][k]),d[k]) for k in range(3)))
                for j in range(2)] for i in range(2)]
        a,b=rows[0][0],rows[1][1]
        expected=m.add(m.scale(m.mul(m.power(a,2),m.power(b,2)),48),
                       m.scale(m.mul(m.power(a,2),m.power(m.v,2)),48),
                       m.scale(m.mul(m.power(m.u,2),m.power(m.v,4)),4))
        self.assertEqual(m.determinant(sigma),expected)

    def test_omitted_shift_mutant_fails_exact_pin_substitution(self):
        bad=m.add(m.target_cubic(),m.scale(m.mul(m.power(m.r,2),m.x),F(3,2)))
        got=m.substitute(m.derivative(bad,1),{1:m.scale(m.r,F(1,2)),2:{}})
        self.assertNotEqual(got,{})

    def test_wrong_axial_normalization_loses_random_row(self):
        q=m.thin_substitute(m.derivative(m.completed_monomial(4,0),1))
        self.assertEqual(m.coefficient_r(q,2),{})
        self.assertNotEqual(m.coefficient_r(q,3),{})

    def test_wrong_transverse_shift_mutant_fails_pins(self):
        bad=m.mul(m.power(m.x,2),m.z)
        got=m.substitute(m.derivative(bad,2),{1:m.scale(m.r,F(1,2)),2:{}})
        self.assertNotEqual(got,{})

    def test_crude_count_ledger(self):
        p=m.report()['power_ledger']
        self.assertEqual(sum(p[k] for k in ('area','gradient_density','triple_hessian_cost','full_normalizer_division')),-10)
        self.assertNotEqual(3-4-6-2,-10) # false r^-4 Jacobian
        self.assertNotEqual(3-5-6,-10)   # dropped full normalizer

    def test_nonclaims_not_promoted(self):
        r=m.report()
        for k in ('reference_is_periodic_covariance','analytic_proof_checked_by_code','independent_review','full_annulus_closed'):
            self.assertIs(r[k],False)
        self.assertEqual(r['scientific_effect'],'NONE')

    def test_input_and_singular_matrix_controls(self):
        with self.assertRaises(ValueError): m.completed_monomial(-1,2)
        with self.assertRaises(ValueError): m.completed_monomial(True,2)
        with self.assertRaises(ValueError): m.inverse([[1,2],[2,4]])

if __name__=='__main__': unittest.main()
