"""Exact finite algebra and budget checks; NOT an analytic theorem verifier."""
import unittest
from fractions import Fraction as Q
import thin_tube as p
import annulus as a

class AnnulusChecks(unittest.TestCase):
    def test_height_contact_minor(self):
        m=a.contact_matrix()
        minor=p.determinant([[row[i] for i in (0,2,3)] for row in m])
        self.assertEqual(minor,p.scale(p.power(p.v,6),Q(1,24)))

    def test_contact_rows_on_all_45_pin_completed_monomials(self):
        count=0
        for i in range(9):
            for j in range(9-i):
                f=p.completed_monomial(i,j); count+=1
                jets=[p.midpoint_contact(f,*ij) for ij in ((0,2),(2,1),(1,2),(0,3))]
                actual=a.extract_contact(f)
                expected=[p.add(*(p.mul(c,q) for c,q in zip(row,jets))) for row in a.contact_matrix()]
                self.assertEqual(actual,expected,(i,j))
        self.assertEqual(count,45)

    def test_exact_deterministic_drift(self):
        gx,gz,h=a.extract_contact(p.target_cubic())
        self.assertEqual(gx,p.add(p.scale(p.power(p.u,2),6),p.constant(Q(-3,2))))
        self.assertEqual(gz,{})
        self.assertEqual(h,p.add(p.scale(p.power(p.u,3),2),p.scale(p.u,Q(-3,2)),p.constant(Q(-1,2))))

    def test_height_subtraction_cancels_quadratic_but_retains_cubic(self):
        self.assertEqual(a.extract_contact(p.power(p.z,2))[2],{})
        self.assertEqual(a.extract_contact(p.power(p.z,3))[2],p.scale(p.power(p.v,3),Q(-1,2)))

    def test_cauchy_binet_lower_floor_contains_squared_minor(self):
        m=a.contact_matrix()
        gram=[[p.add(*(p.mul(x,y) for x,y in zip(r,s))) for s in m] for r in m]
        from itertools import combinations
        minors=[p.determinant([[row[j] for j in cols] for row in m]) for cols in combinations(range(4),3)]
        self.assertEqual(p.determinant(gram),p.add(*(p.power(q,2) for q in minors)))
        self.assertIn(p.scale(p.power(p.v,6),Q(1,24)),minors)

    def test_safe_cutoff_has_strict_perturbation_margin(self):
        self.assertEqual(a.cutoff_margin(Q(1,24)),Q(1,2))
        self.assertTrue(a.cutoff_safe(Q(1,24)))
        self.assertFalse(a.cutoff_safe(Q(1,12)))
        self.assertFalse(a.cutoff_safe(Q(1,6)))

    def test_conservative_angular_exponents(self):
        x=a.ledger()
        self.assertEqual((x['eigenfloor_t'],x['density_t'],x['sixth_moment_t'],x['geometric_t'],x['total_angular_t']),(12,18,72,6,96))

    def test_complete_r_power_ledger(self):
        x=a.ledger()
        self.assertEqual(x['raw_density_r']+x['triple_determinant_r']+x['height_window_r']+x['normalizer_r'],1)
        self.assertEqual(x['physical_intensity_r']+x['area_r'],3)
        self.assertEqual(x['count_r'],3)

    def test_missing_height_window_is_not_cubic(self):
        x=a.ledger()
        self.assertEqual(x['count_r']-x['height_window_r'],0)

    def test_triangle_inverse_checks_noncollinearity(self):
        for u,t in ((Q(2),Q(1,3)),(Q(-3,2),Q(-1,7)),(Q(0),Q(2))):
            mat=[[Q(1),u+Q(1,2)],[Q(0),t]]
            inv=a.triangle_inverse(u,t)
            self.assertEqual([[sum(mat[i][k]*inv[k][j] for k in range(2)) for j in range(2)] for i in range(2)],[[1,0],[0,1]])
        with self.assertRaises(ValueError):a.triangle_inverse(2,0)

    def test_axis_requires_inner_chart(self):
        m=a.contact_matrix()
        for row in m:
            for entry in row:self.assertEqual(p.substitute(entry,{4:{}}),{})
        self.assertIs(a.ledger()['outer_chart_covers_axis'],False)

    def test_analytic_nonclaims_remain_explicit(self):
        x=a.ledger()
        self.assertIs(x['analytic_verification'],False)
        self.assertIs(x['independent_review'],False)
        self.assertIs(x['global_RN_closed'],False)
        self.assertEqual(x['scientific_effect'],'NONE')

if __name__=='__main__':unittest.main()
