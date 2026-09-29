"""Exact finite illustrations. They do not verify any infinite-dimensional premise."""
from fractions import Fraction as F
import unittest
import charts as c

SECTION=(F(0),F(1))
TUBE=(-3,3,-2,3)
GOOD=[(0,-1,F(1,2)),(2,1,F(1,2))]

class ChartTests(unittest.TestCase):
    def test_endpoint_hit_excluded(self):
        self.assertFalse(c.robust_hit([(0,-1,0),(2,1,0)],SECTION,TUBE))

    def test_earlier_endpoint_not_hidden_by_later_interior(self):
        path=[(0,-1,-1),(2,1,1),(3,1,F(1,2)),(5,-1,F(1,2))]
        self.assertFalse(c.robust_hit(path,SECTION,TUBE))
        self.assertEqual(c.closed_contacts(path,SECTION)[0]['time'],1)

    def test_terminal_hit_excluded(self):
        self.assertFalse(c.robust_hit([(0,-1,F(1,2)),(1,0,F(1,2))],SECTION,TUBE))

    def test_launch_on_section_excluded(self):
        self.assertFalse(c.robust_hit([(0,0,F(1,2)),(2,1,F(1,2))],SECTION,TUBE))

    def test_compact_prefix_tube_clearance(self):
        path=[(0,-1,F(1,2)),(1,-1,4),(2,-1,F(1,2)),(4,1,F(1,2))]
        self.assertFalse(c.robust_hit(path,SECTION,TUBE))

    def test_tube_boundary_excluded(self):
        path=[(0,-3,F(1,2)),(4,1,F(1,2))]
        self.assertFalse(c.robust_hit(path,SECTION,TUBE))

    def test_strict_gradient_threshold(self):
        self.assertFalse(c.gradient_slack(F(1),F(1)))
        self.assertTrue(c.gradient_slack(F(3,2),F(1)))

    def test_transverse_corner_not_certified(self):
        path=[(0,-1,F(1,2)),(1,0,F(1,2)),(2,-1,F(1,2))]
        self.assertFalse(c.robust_hit(path,SECTION,TUBE))

    def test_robust_interior_family(self):
        for eps in [F(i,100) for i in range(-20,21)]:
            p=[(0,-1,F(1,2)+eps),(2,1,F(1,2)+eps)]
            self.assertTrue(c.robust_hit(p,SECTION,TUBE))
            self.assertEqual(c.closed_contacts(p,SECTION)[0]['time'],1)

    def test_hitting_time_continuity_model(self):
        for eps in (F(-1,8),F(0),F(1,8)):
            p=[(0,-1+eps,F(1,2)),(2,1+eps,F(1,2))]
            self.assertTrue(c.robust_hit(p,SECTION,TUBE))
            self.assertEqual(c.closed_contacts(p,SECTION)[0]['time'],1-eps)

    def test_earlier_collinear_contact_excluded(self):
        p=[(0,0,-1),(2,0,1),(3,1,F(1,2)),(5,-1,F(1,2))]
        self.assertFalse(c.robust_hit(p,SECTION,TUBE))
        self.assertEqual(c.closed_contacts(p,SECTION)[0]['time'],1)

    def test_relative_interior_only_time_jumps(self):
        # Smooth embedded gamma(t)=((t-1)(t-2),(t-1)^2+eps), roots at1,2.
        for eps in (F(0),F(1,100),F(1,10000)):
            interior=[t for t in (1,2) if 0<(t-1)**2+eps<2]
            self.assertEqual(min(interior),2 if eps==0 else 1)
            self.assertEqual(min(t for t in (1,2) if 0<=(t-1)**2+eps<=2),1)

    def test_gaussian_residual_orthogonality(self):
        Q=[[F(2),F(1)],[F(1),F(3)]];a=[F(1),F(2)]
        var,b,R=c.gaussian_split(Q,a)
        self.assertEqual(var,18)
        self.assertEqual(sum(x*y for x,y in zip(a,b)),1)
        self.assertEqual([sum(row[j]*a[j] for j in range(2)) for row in R],[0,0])
        for i in range(2):
            for j in range(2):
                self.assertEqual(R[i][j]+var*b[i]*b[j],Q[i][j])

    def test_degenerate_gaussian_direction_rejected(self):
        with self.assertRaises(ValueError):c.gaussian_split([[1,1],[1,1]],[1,-1])

    def test_distinct_evaluations_span_polynomials(self):
        for n in range(1,7):
            V=[[F(i)**j for j in range(n)] for i in range(n)]
            self.assertEqual(c.rank(V),n)
            self.assertEqual(c.rank(V+[V[0]]),n)

    def test_regular_zeros_only(self):
        # p(t)=t(t-1)^2; the zero at1 has derivative0.
        self.assertTrue(c.regular_zero([0,1,-2,1],0))
        self.assertFalse(c.regular_zero([0,1,-2,1],1))
        self.assertFalse(c.regular_zero([0,1,-2,1],2))

    def test_all_local_sections_checked(self):
        bad=[(0,-1,0),(2,1,0)]
        self.assertFalse(c.chart_hits([bad,GOOD],SECTION,TUBE))
        self.assertTrue(c.chart_hits([GOOD,GOOD],SECTION,TUBE))

    def test_positive_quantitative_margins(self):
        self.assertTrue(c.robust_hit(GOOD,SECTION,TUBE,margin=F(1,4)))
        self.assertFalse(c.robust_hit(GOOD,SECTION,TUBE,margin=F(1,2)))

    def test_invalid_path_and_section(self):
        with self.assertRaises(ValueError):c.robust_hit([(0,-1,0),(0,1,0)],SECTION,TUBE)
        with self.assertRaises(ValueError):c.robust_hit(GOOD,(1,0),TUBE)
        with self.assertRaises(ValueError):c.robust_hit(GOOD,SECTION,TUBE,margin=F(-1))

if __name__=='__main__':unittest.main()
