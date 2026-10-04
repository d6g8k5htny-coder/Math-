"""Finite exact controls only; the continuum argument is in PROOF.md."""
from fractions import Fraction as F
from itertools import product
import random
import unittest
import controls as c

class PolynomialTests(unittest.TestCase):
    def test_ring(self):
        self.assertEqual(c.mul([1,2],[3,-1]),[F(3),F(5),F(-2)])
        self.assertEqual(c.add([1,2],[2,-2]),[F(3)])
    def test_empty_and_singular(self):
        self.assertEqual(c.det([]),[F(1)])
        self.assertEqual(c.det([[[1],[2]],[[2],[4]]]),[F(0)])
    def test_adjugate_identity(self):
        a=[[[1,1],[2]],[[3],[4,-1]]]
        adj=c.adj(a);d=c.det(a)
        for i,j in product(range(2),repeat=2):
            got=c.add(*(c.mul(a[i][k],adj[k][j]) for k in range(2)))
            self.assertEqual(got,d if i==j else [F(0)])
    def test_two_by_two_directional_derivatives(self):
        a=[[1,2],[2,5]];b=[[3,1],[1,-2]];cc=[[0,1],[1,4]]
        Delta,db,dc,dbb,jb=c.det_data(a,b,cc)
        self.assertEqual((Delta,db,dc,dbb),(F(1),F(9),F(0),F(-14)))
        self.assertEqual(jb,[[F(-2),F(-1)],[F(-1),F(3)]])
    def test_endpoint_identity_all_matrix_types(self):
        rng=random.Random(20261001)
        count=0
        for m in range(4):
            for sample in range(16):
                def mat():
                    a=[[F(rng.randrange(-4,5),3) for _ in range(m)] for _ in range(m)]
                    return [[a[min(i,j)][max(i,j)] for j in range(m)] for i in range(m)]
                a,b,cc=mat(),mat(),mat()
                if sample%4==0:a=[[F(0) for _ in range(m)] for _ in range(m)]
                g=[F(rng.randrange(-3,4),2) for _ in range(m)]
                h=[F(rng.randrange(-3,4),2) for _ in range(m)]
                k=F(sample+1,7);f4=F(sample-4,3);f5=F(7-sample,2)
                direct=c.endpoint_product(a,b,cc,g,h,f4,f5,k)
                pred=c.weight2(a,b,cc,g,h,f4,f5,k)
                Delta=c.det_data(a,b,cc)[0]
                self.assertEqual(c.coef(direct,0),36*k*k*Delta*Delta)
                self.assertEqual(c.coef(direct,1),0)
                self.assertEqual(c.coef(direct,2),pred)
                self.assertTrue(all(c.coef(direct,j)==0 for j in range(1,len(direct),2)))
                count+=1
        self.assertEqual(count,64)
    def test_common_first_coefficient_is_not_cusp_Y_at_fixed_k(self):
        # The fixed-k expansion retains 3k Ddet(A)[B].
        a=[[2]];b=[[1]];cc=[[0]];g=[0];h=[0]
        w=c.weight2(a,b,cc,g,h,0,0,F(1))
        self.assertEqual(w,-9)
        self.assertNotEqual(w,0)
    def test_fifth_derivative_is_load_bearing(self):
        self.assertEqual(c.weight2([],[],[],[],[],0,120,1),12)
        self.assertNotEqual(c.weight2([],[],[],[],[],0,120,1),0)
    def test_inverse_free_at_singular_A(self):
        # Here Delta=0 and common=-9/4+21=75/4, hence -common^2.
        self.assertEqual(c.weight2([[0]],[[1]],[[2]],[3],[4],5,6,7),-F(5625,16))

class CovarianceTests(unittest.TestCase):
    def test_reference_covariances(self):
        q=[[F(1)]]
        self.assertEqual(c.jet_cov((1,),(3,),q),-3)
        self.assertEqual(c.jet_cov((2,),(4,),q),-15)
        self.assertEqual(c.jet_cov((4,),(4,),q),105)
        self.assertEqual(c.jet_cov((3,),(4,),q),0)
    def test_odd_even_blocks(self):
        for d in (1,2,3):
            q=[[F(2) if i==j else F(1,3) for j in range(d)] for i in range(d)]
            out=c.blocks(d,q)
            self.assertTrue(out['parity_zero'])
            self.assertLessEqual(out['maximum_order'],8)
            self.assertGreater(c.det([[ [x] for x in row] for row in out['odd0']])[0],0)
            self.assertGreater(c.det([[ [x] for x in row] for row in out['even0']])[0],0)
    def test_order_ten_not_requested(self):
        with self.assertRaises(ValueError):c.jet_cov((5,),(5,),[[1]])
        self.assertEqual(c.jet_cov((5,),(3,),[[1]]),-105)
    def test_d1_pin_covariance_coefficients(self):
        out=c.blocks(1,[[1]])
        self.assertEqual(out['odd0'],[[F(1),F(-3)],[F(-3),F(15)]])
        self.assertEqual(out['odd2'],[[-F(3,4),F(9,4)],[F(9,4),-F(21,4)]])
        self.assertEqual(out['even0'],[[F(3)]])
        self.assertEqual(out['even2'],[[-F(5,4)]])
    def test_positive_definite_basis_dimension(self):
        for d in (1,2,3,4):
            out=c.blocks(d,[[int(i==j) for j in range(d)] for i in range(d)])
            self.assertEqual(len(out['odd0'])+len(out['even0']),(d+1)*(d+2)//2)
    def test_anisotropic_odd_jet_means_depend_on_gap(self):
        q=[[F(1),F(1,3)],[F(1,3),F(2)]]
        out=c.blocks(2,q);inv=c.inverse(out['odd0']);pins=[(1,0),(0,1),(3,0)]
        def mean(jet):
            return 12*sum(c.jet_cov(jet,pins[j],q)*inv[j][-1] for j in range(3))
        self.assertEqual(mean((2,1)),4)
        self.assertEqual(mean((1,2)),F(4,3))
    def test_birth_marginal_is_not_birth_zero(self):
        var=F(105)-F(15)**2/3
        inv=c.inverse([[1,-1],[-1,3]])
        cross=[F(3),F(-15)]
        fixed=105-sum(cross[i]*inv[i][j]*cross[j] for i,j in product(range(2),repeat=2))
        self.assertEqual(var,30);self.assertEqual(fixed,24)
    def test_matrix_inverse(self):
        a=[[F(3),F(-2)],[F(-2),F(5)]];inv=c.inverse(a)
        for i,j in product(range(2),repeat=2):
            self.assertEqual(sum(a[i][k]*inv[k][j] for k in range(2)),int(i==j))
        with self.assertRaises(ValueError):c.inverse([[0]])

class MellinAndRegressionTests(unittest.TestCase):
    def test_reference_d1(self):
        out=c.d1((1,3,15,105))
        self.assertEqual(out['a'],12)
        self.assertEqual(out['p'],[-F(5,24),F(9,2),F(108)])
        self.assertEqual(out['den2'],18)
        self.assertEqual(c.mellin_factor(out['a'],out['p']),F(9,8))
        # Sphere factor 2/3, and density normalization is pi^-3/2.
        self.assertEqual(F(2,3)*c.mellin_factor(out['a'],out['p']),F(3,4))
    def test_d2_independent_reference_regression(self):
        q=[[1,0],[0,1]];out=c.blocks(2,q)
        odd=[(1,0),(0,1),(3,0)];ev=[(2,0),(1,1),(0,2)]
        oi=c.inverse(out['odd0']);ei=c.inverse(out['even0'])
        def reg(jet,pins,inv,target):
            return sum(c.jet_cov(jet,pins[i],q)*inv[i][j]*target[j]
                       for i,j in product(range(len(pins)),repeat=2))
        def var(jet,pins,inv):
            x=[c.jet_cov(jet,p,q) for p in pins]
            return c.jet_cov(jet,jet,q)-sum(x[i]*inv[i][j]*x[j]
                       for i,j in product(range(len(pins)),repeat=2))
        self.assertEqual(reg((4,0),ev,ei,[0,0,1]),F(3,4))
        self.assertEqual(reg((2,2),ev,ei,[0,0,1]),-F(3,4))
        self.assertEqual(var((4,0),ev,ei),F(57,2))
        self.assertEqual(var((2,1),odd,oi),2)
        self.assertEqual(var((1,2),odd,oi),2)
        self.assertEqual(reg((1,2),odd,oi,[0,0,12]),0)
        self.assertEqual(reg((5,0),odd,oi,[0,0,12]),-120)
        tr=lambda a,b:sum(a[i][j]*b[j][i] for i,j in product(range(len(a)),repeat=2))
        self.assertEqual(-tr(oi,out['odd2'])/2-tr(ei,out['even2'])/2,F(23,32))
        z=[ei[i][-1] for i in range(3)]
        self.assertEqual(sum(z[i]*out['even2'][i][j]*z[j] for i,j in product(range(3),repeat=2))/2,-F(1,256))
    def test_d2_independent_cone_integral(self):
        # A|H*u=0 is N(0,8/3). These are its negative-half moments.
        moments={0:F(1,2),2:F(4,3),4:F(32,3)}
        H0={4:-F(1,256),2:-F(13,96),0:-F(3,4)}
        H2={4:-F(9,64),2:F(57,8),0:F(-18)}
        H4={2:F(108)}
        p=[sum(v*moments[j] for j,v in poly.items()) for poly in (H0,H2,H4)]
        self.assertEqual(p,[-F(43,72),-F(1),F(144)])
        # 12*p_O*p_(H*u) = (1/2)*pi^(-5/2), sphere=2*pi.
        self.assertEqual(c.mellin_factor(12,p)/3,F(13,18))
    def test_d1_spatial_scaling(self):
        base=c.d1((1,3,15,105));bf=c.mellin_factor(base['a'],base['p'])
        for lam in (F(1,4),F(4),F(9)):
            out=c.d1(tuple(v*lam**j for j,v in enumerate((1,3,15,105),1)))
            f=c.mellin_factor(out['a'],out['p'])
            sixth=(base['den2']/out['den2'])**3*(out['a']/base['a'])*(f/bf)**6
            self.assertEqual(sixth,lam**3)
    def test_amplitude_scaling(self):
        base=c.d1((1,3,15,105));bf=c.mellin_factor(base['a'],base['p'])
        for amp in (F(1,8),F(8),F(27)):
            out=c.d1(tuple(v*amp**2 for v in (1,3,15,105)))
            f=c.mellin_factor(out['a'],out['p'])
            sixth=(base['den2']/out['den2'])**3*(out['a']/base['a'])*(f/bf)**6
            self.assertEqual(sixth,amp**(-8))
    def test_eighth_moment_is_required(self):
        a=c.d1((1,3,15,105));b=c.d1((1,3,15,106))
        self.assertNotEqual(a['p'],b['p'])
        self.assertNotEqual(c.mellin_factor(a['a'],a['p']),c.mellin_factor(b['a'],b['p']))
    def test_wrong_subtraction_changes_coefficient(self):
        self.assertEqual(c.mellin_factor(F(12),[1,0,0]),-3)
        self.assertNotEqual(c.mellin_factor(F(12),[-F(5,24),F(9,2),108]),F(1,2)*F(9,2)/12+F(5,12)*108/144)
    def test_cubature_moments(self):
        for j,expected in enumerate((1,0,1,0,3)):
            self.assertEqual(sum(w*x**j for x,w in c.cubature()),expected)
    def test_anisotropic_conditional_parity_and_degree(self):
        # Synthetic Gaussian affine conditional law: one odd and one even
        # Gaussian coordinate. Exact cubature matches every needed moment.
        def expectation(k):
            total=F(0)
            for (z,wz),(v,wv) in product(c.cubature(),repeat=2):
                a=[[-2,1],[1,-3]]
                b=[[k+z,2*k-z],[2*k-z,-k+2*z]]
                cc=[[1+v,2-v],[2-v,3+2*v]]
                g=[2*k+z,-k+3*z];h=[v+1,2-v]
                total+=wz*wv*c.weight2(a,b,cc,g,h,3+2*v,5*k+z,k)
            return total
        y0,y1,y2=map(expectation,(F(0),F(1),F(2)))
        p4=(y2-4*y1+3*y0)/12;p2=y1-y0-p4
        self.assertNotEqual(p4,0)
        for k in (F(-3),F(-1,2),F(3),F(5)):
            self.assertEqual(expectation(k),y0+p2*k*k+p4*k**4)
    def test_input_rejections(self):
        with self.assertRaises(TypeError):c.exact(0.5)
        with self.assertRaises(TypeError):c.exact(True)
        with self.assertRaises(ValueError):c.mellin_factor(0,[1,2,3])
        with self.assertRaises(ValueError):c.d1((1,1,1,1))

class ExplicitBoundTests(unittest.TestCase):
    def test_coefficient_majorant_budget(self):
        out=c.bound_budget()
        self.assertLess(out['weight_l1'],2000)
        self.assertLess(out['moment8_integral'],10**15)
        self.assertLess(out['H_bound'],10**22)
        self.assertLess(out['H_derivative_bound'],10**25)
        self.assertLess(out['p_bound'],10**41)
        self.assertLess(out['p_derivative_bound'],10**44)
        self.assertLess(out['final_bound'],10**50)
    def test_uniform_conditioning_floor(self):
        self.assertGreater(F(3,8)-10*F(1,10**4),F(1,3))
        self.assertLess(F(105)+F(1,10**4),106)
    def test_exponential_certificates(self):
        self.assertGreater(c.exp_partial(F(50),120),F(10**22,2))
        self.assertGreater(c.exp_partial(F(288),400),10**125)
    def test_lattice_geometric_ratio(self):
        self.assertLess(F(2**10,1+150+150**2//2),F(1,2))
        for d in (1,2,3):
            for j in range(1,20):
                self.assertLessEqual((2*j+1)**d-(2*j-1)**d,(3**d-1)*j**(d-1))
    def test_L10_is_inside_covariance_box(self):
        self.assertLess(2*c.image_polynomial(3,F(10))/10**22,F(1,10**4))
    def test_SIDE24_budgets(self):
        expected=(461984450376,28868660309280,471182508197544)
        for d,val in enumerate(expected,1):
            self.assertEqual(c.image_polynomial(d,F(24)),val)
            self.assertLess(F(10**50)*val/10**125,F(1,10**60))
    def test_reference_intervals_transport_outward(self):
        for lo,hi in c.REFERENCE_C2.values():
            lo,hi=F(lo),F(hi)
            self.assertLess(lo-F(1,10**16),lo-F(1,10**60))
            self.assertGreater(hi+F(1,10**16),hi+F(1,10**60))
    def test_no_unrestricted_dimension_numerical_claim(self):
        with self.assertRaises(ValueError):c.image_polynomial(4,F(24))
        with self.assertRaises(ValueError):c.image_polynomial(3,F(9))

if __name__=='__main__':unittest.main()
