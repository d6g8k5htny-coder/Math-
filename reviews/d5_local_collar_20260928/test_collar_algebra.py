"""Finite algebra controls; they do not verify the analytic Gaussian proof."""
from fractions import Fraction as F
import itertools
import unittest
import collar_algebra as a

class CollarControls(unittest.TestCase):
    def test_cardinal_values_and_derivatives(self):
        for nodes in [(F(-1),F(0),F(2)),(F(-1,2),F(1,2),F(0)),(F(-2),F(3,7),F(5))]:
            for i in range(3):
                h,d,ell2=a.cardinals(nodes,i)
                for j,t in enumerate(nodes):
                    self.assertEqual(a.evaluate(h,t), F(i==j))
                    self.assertEqual(a.evaluate(a.derivative(h),t),0)
                    self.assertEqual(a.evaluate(d,t),0)
                    self.assertEqual(a.evaluate(a.derivative(d),t),F(i==j))
                    self.assertEqual(a.evaluate(ell2,t),F(i==j))
                    if i!=j:
                        self.assertEqual(a.evaluate(a.derivative(ell2),t),0)
                self.assertLessEqual(len(h)-1,5)
                self.assertLessEqual(len(d)-1,5)
    def test_full_nine_row_rank_including_midpoint_and_axis(self):
        for u,v in itertools.product([F(-2),F(-1),F(-1,4),F(0),F(1,4),F(1),F(2)],
                                      [F(0),F(1,1000000),F(-1,8),F(1,4),F(1)]):
            p=[(F(-1,2),F(0)),(F(1,2),F(0)),(u,v)]
            self.assertEqual(a.rank(a.jet_matrix(p)),9)
    def test_degree_four_obstruction_on_collinear_triple(self):
        pts=[(F(-1,2),F(0)),(F(1,2),F(0)),(F(0),F(0))]
        self.assertEqual(a.rank(a.jet_matrix(pts,4)),8)
    def test_pin_collision_is_excluded(self):
        self.assertFalse(a.in_collar(F(-1,2),F(0),F(1,4),F(2)))
        self.assertFalse(a.in_collar(F(1,2),F(0),F(1,4),F(2)))
        self.assertTrue(a.in_collar(F(0),F(0),F(1,4),F(2)))
    def test_transverse_gram_identity(self):
        for u,v in itertools.product([F(-2),F(0),F(1,2),F(1)],[F(1,1000),F(-1,8),F(1)]):
            b=a.transverse_block(u,v)
            g=[[sum(x*y for x,y in zip(p,q)) for q in b] for p in b]
            self.assertEqual(g[0][0]*g[1][1]-g[0][1]*g[1][0],u*u*v**4+v**6/4)
    def test_covariance_floor_and_relative_remainder_orders(self):
        self.assertEqual(a.floor_orders(),{'jet_degree':5,'std_floor':5,'variance_floor':10,'remainder':6})
        for n in [2,10,100]:
            r=F(1,n)
            self.assertEqual(r**6/r**5,r)
    def test_crossover_overlap(self):
        for n in [2,7,1000]:
            r=F(1,n**3); v=F(1,n)
            self.assertEqual(r/v**2,F(1,n))
            self.assertLessEqual(r*r+v*v,2*v*v)
            self.assertTrue(a.near_axis(F(0),r))
            self.assertTrue(a.near_axis(v,r))
    def test_power_ledger(self):
        self.assertEqual(a.powers(),{'near_raw':-72,'near_absorption':F(74),'near_final':F(2),
                                    'transverse_r':1,'transverse_v':-34,'transverse_absorption':34})
    def test_ninth_value_not_conditioned(self):
        self.assertEqual(a.observations(),{'auxiliary_gram':9,'actual_conditioning':8,'height_window_factor':0})
    def test_collar_pin_disk_cover(self):
        for u,v in itertools.product([F(n,8) for n in range(-12,13)],[F(n,8) for n in range(-8,9)]):
            if u*u+v*v>4 or (u,v) in [(F(-1,2),F(0)),(F(1,2),F(0))]:
                continue
            pin=((u+F(1,2))**2+v*v<=F(1,16) or (u-F(1,2))**2+v*v<=F(1,16))
            self.assertTrue(pin or a.in_collar(u,v,F(1,4),F(2)))

if __name__=='__main__': unittest.main()
