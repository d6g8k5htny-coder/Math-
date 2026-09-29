"""Finite exact controls, not a Gaussian-field theorem checker."""
import itertools
import unittest
from fractions import Fraction as F
import lift as m

class LiftTests(unittest.TestCase):
    def test_nonorthogonal_shear_cancels_midpoint_cross_terms(self):
        D = [[F(-2), F(1,5)], [F(1,5), F(-3)]]
        v = [F(1,4), F(-1,7)]
        sigma = F(-3,200)
        A, S = m.chart(D,v,sigma)
        wanted = [[sigma,F(0),F(0)], [F(0),*D[0]], [F(0),*D[1]]]
        self.assertEqual(m.mm(m.tr(S),m.mm(A,S)),wanted)
        self.assertNotEqual(m.mm(m.tr(S),S),m.eye(3))
        self.assertEqual(m.det(S),1)

    def test_raw_soft_entry_need_not_be_order_r(self):
        A,_ = m.chart([[F(-1)]],[F(1,5)],F(-1,100))
        self.assertEqual(A[0][0],F(-1,20))
        self.assertEqual(A[0][0]-F(1,5)**2/F(-1),F(-1,100))

    def test_chart_extends_through_singular_contact(self):
        A,S = m.chart([[F(-1)]],[F(1,5)],F(0))
        self.assertEqual(m.det(A),0)
        self.assertEqual(m.det(S),1)

    def test_full_dimension_determinant_identity(self):
        for n in range(1,5):
            D = [[-F(i+2) if i==j else F(0) for j in range(n)] for i in range(n)]
            v = [F(i+1,20) for i in range(n)]
            A,_ = m.chart(D,v,F(-1,17))
            self.assertEqual(m.det(A),F(-1,17)*m.det(D))

    def test_cubic_tensor_change_has_unit_jacobian(self):
        for d in range(3,6):
            labels,T = m.cubic_change(d,[F(i+1,20) for i in range(d-2)])
            self.assertEqual(m.det(T),1)
            pure = labels.index((3,)+(0,)*(d-1))
            self.assertEqual(T[pure],[F(int(j==pure)) for j in range(len(labels))])
            reduced = [[v for j,v in enumerate(row) if j!=pure]
                       for i,row in enumerate(T) if i!=pure]
            self.assertEqual(m.det(reduced),1)

    def test_raw_chart_volume_is_one_power_of_r(self):
        for d in range(2,9):
            self.assertEqual(m.rare_power(d),1)
            r = F(1,13)
            self.assertEqual(m.band_width(r,F(6,5),F(1,100)),F(12,6500))

    def test_complete_contact_jet_labels(self):
        for d in range(2,8):
            U,J = m.jet_labels(d)
            self.assertEqual(len(U),2*(d+1))
            self.assertEqual(len(U+J),len(set(U+J)))
            self.assertEqual(set(U+J),set(m.multiindices(d,3,upto=True)))

    def test_polynomial_lattice_unisolvence(self):
        for d in (2,3,4):
            labels = m.multiindices(d,3,upto=True)
            V = [[m.monomial(n,a) for a in labels] for n in itertools.product(range(4),repeat=d)]
            self.assertEqual(m.rank(V),len(labels))
            self.assertEqual(m.rank([row+[row[0]] for row in V]),len(labels))

    def test_plane_pins_with_free_transverse_cubic(self):
        k,s,a,beta,c = F(6,5),F(-2),F(3,7),F(-4,5),F(2,3)
        for X,val in ((F(-1,2),0),(F(1,2),-k)):
            f,g = m.plane(X,F(0),k,s,a,beta,c)
            self.assertEqual(f,val)
            self.assertEqual(g,[0,0])

    def test_plane_path_polynomials(self):
        k=F(6,5)
        for t in [F(i,16) for i in range(17)]:
            pts=[(-F(1,2)-t/4, F(0)),(-F(3,4),9*t/4),(-F(3,4)-t/4,F(9,4))]
            want=[-3*t*t/16-t**3/32,F(-7,32),-F(7,32)+51*t/64-9*t*t/32-t**3/32]
            for (X,Z),w in zip(pts,want):
                f,_=m.plane(X,Z,k,-3*k/2,0,-2*k,0)
                self.assertEqual(f,k*w)
        self.assertGreater(F(-7,32)-F(1,64),F(-1,4))
        self.assertGreater(F(17,64)-F(1,64),0)

    def test_path_survives_bounded_spatial_shear(self):
        q=F(1,9)
        maxnorm=F(97,16)
        self.assertLess((1+q)**2*maxnorm,16)

    def test_two_extra_saddle_data(self):
        X,z2=F(-3,4),F(15,8)
        self.assertEqual(6*X*X-F(3,2)-z2,0)
        self.assertEqual(F(3,2)+2*X,0)
        self.assertEqual(2*X**3-F(3,2)*X-F(1,2)-(F(3,4)+X)*z2,F(-7,32))
        self.assertEqual(-4*z2,F(-15,2))
        self.assertLess(X*X+z2,4)

    def test_stiff_modes_do_not_change_weight_power(self):
        for d in range(2,9):
            self.assertEqual(m.weight_power(d),4)
            for r in (F(1,4),F(1,16),F(1,64)):
                HM,HS=m.endpoint_model(d,r,F(1))
                self.assertEqual(abs(m.det(HM)*m.det(HS)),45*r**4)
                self.assertEqual(m.inertia(HM),(d,0))
                self.assertEqual(m.inertia(HS),(d-1,0))

    def test_endpoint_cross_blocks_need_schur_correction(self):
        D=[[F(-2),F(0)],[F(0),F(-3)]]
        for r in (F(1,4),F(1,16),F(1,64)):
            A=[[-6*r,F(0)],[F(0),-r/2]]
            C=[[r/7,r/11],[r/13,r/17]]
            H=m.blocks(A,C,D)
            K=m.schur(A,C,D)
            self.assertEqual(m.det(H),m.det(D)*m.det(K))
            self.assertNotEqual(K,A)
            self.assertEqual(m.inertia(H),(4,0))
            error=max(abs((K[i][j]-A[i][j])/r) for i in range(2) for j in range(2))
            self.assertLess(error,r)

    def test_stiff_elimination_is_order_r_squared(self):
        D=[[F(-2),F(0)],[F(0),F(-3)]]
        Q=[F(1,7),F(-2,9)]
        z=m.solve(D,Q)
        for r in (F(1,4),F(1,16),F(1,64)):
            ell=[r*r*v for v in Q]
            w=[-r*r*v for v in z]
            for i in range(2):
                self.assertEqual(sum(D[i][j]*w[j] for j in range(2))+ell[i],0)
            correction=sum(w[i]*D[i][j]*w[j]/2 for i in range(2) for j in range(2))+sum(ell[i]*w[i] for i in range(2))
            self.assertEqual(correction/r**3,-r*sum(Q[i]*z[i] for i in range(2))/2)

    def test_determinant_tilt_ledger_all_dimensions(self):
        for d in range(2,9):
            self.assertEqual(m.rare_power(d)+m.weight_power(d)-2,3)

    def test_density_loss_ledger(self):
        self.assertEqual(m.loss_powers(),(F(2,3),F(-5,3)))
        self.assertEqual(F(2,3)+1,F(5,3))
        # ell=u^3 gives ell^(2/3-p) d ell = 3 u^(4-3p) du.
        self.assertEqual(4-3*F(5,3),-1)
        self.assertGreater(4-3*F(3,2),-1)
        self.assertLess(4-3*F(2),-1)

    def test_singular_stable_block_is_excluded(self):
        with self.assertRaises(ValueError):
            m.chart([[F(0)]],[F(1)],F(1))

if __name__=='__main__': unittest.main()
