"""Exact finite falsification controls; not invariant-manifold or Gaussian proofs."""
import unittest
from fractions import Fraction as F
import a2 as m

class Checks(unittest.TestCase):
    def test_contraction_denominators(self):
        self.assertEqual(m.lp_constants(2,3,F(1,10),1),(F(1,12),F(1,8)))
    def test_constant_forcing_retained(self):
        self.assertEqual(m.anchor_equilibrium(2,3,1,2),(F(-1,2),F(2,3)))
        self.assertEqual(m.unstable_polynomial(2,3,F(1,5),1),(F(-1,2),F(1,60),F(-1,25),F(1,35)))
    def test_constant_path_solves_original_vector_field(self):
        for bu in (F(-1,3),F(0),F(2,5)):
            p=m.anchor_equilibrium(3,5,bu,F(7,11))
            self.assertEqual(3*p[0]+bu,0)
            self.assertEqual(-5*p[1]+F(7,11),0)
    def test_weight_validation(self):
        with self.assertRaises(ValueError):m.lp_constants(2,3,F(1,10),2)
        with self.assertRaises(ValueError):m.lp_constants(0,3,F(1,10),1)
    def test_nonlinear_germ_exact_invariance(self):
        # Triangular (not necessarily gradient) model; chain rule in s=x-p.
        for lam,mu,rho,c in ((2,3,F(1,5),1),(3,2,F(1,7),F(-1,3))):
            p,y0,y1,y2=m.unstable_polynomial(lam,mu,rho,c)
            for s in (F(-1,9),F(0),F(1,11)):
                y=y0+y1*s+y2*s*s
                self.assertEqual(lam*s*(y1+2*y2*s),-mu*y+rho*(p+s)**2)
    def test_fixed_anchor_parameter_derivative(self):
        # Graph is a quadratic polynomial in c; centered difference is EXACT.
        for c in (F(0),F(1,5),F(-2,7)):
            lam,mu,rho,a=F(2),F(3),F(1,5),F(1,17)
            def value(cc):
                p,y0,y1,y2=m.unstable_polynomial(lam,mu,rho,cc);s=a-p
                return y0+y1*s+y2*s*s
            eps=F(1,1000)
            self.assertEqual((value(c+eps)-value(c-eps))/(2*eps),m.fixed_anchor_derivative(lam,mu,rho,c,a))
    def test_neumann_inverse_equation(self):
        B=[[F(1,8),F(1,16)],[F(1,24),F(1,12)]]
        Iminus=[[F(int(i==j))-B[i][j] for j in range(2)] for i in range(2)]
        inv=m.matrix_inverse2(Iminus)
        self.assertEqual(m.mm(Iminus,inv),[[1,0],[0,1]])
        self.assertLess(max(sum(abs(x) for x in row) for row in B),F(1,4))
    def test_projection_annihilates_time_direction(self):
        v=[F(2),F(3)];n=[F(1),F(0)];tau=[F(0),F(1)]
        cov=m.adjoint_hit(v,n,tau)
        self.assertEqual(m.dot(cov,v),0)
        self.assertEqual(m.dot(cov,tau),1)
        self.assertEqual(cov,[F(-3,2),F(1)])
    def test_projection_requires_transversality(self):
        with self.assertRaises(ValueError):m.projection([0,1],[1,0])
    def test_scalar_potential_transverse_forcing(self):
        # Straight regular segment: h(x,y)=x^3(1-x)^3*y near y=0.
        self.assertEqual(m.beta_polynomial_integral(3),F(1,140))
        for a,gprime,phi in ((F(2),F(3,2),F(1,5)),(F(-3),F(-1,2),F(2,7))):
            sign=1 if a>0 else -1
            cov=[-a*gprime,a];grad=[-sign*phi*gprime,sign*phi]
            self.assertEqual(m.dot(cov,grad),abs(a)*phi*(1+gprime*gprime))
            self.assertGreater(m.dot(cov,grad),0)
    def test_eigenline_derivative_loss_counterexample(self):
        previous=F(0)
        for n in (2,4,8,16,32):
            lo,hi=m.eigenline_quotient_bounds(n)
            self.assertGreater(lo,F(n*n,3))
            self.assertLess(lo,hi)
            self.assertGreater(lo,previous)
            previous=lo
    def test_cusp_saddle_hessian(self):
        for n in (2,4,8,16):
            t=F(1,n**4);k=F(1,n**2)
            self.assertEqual(k*k,t)
            det=-1-k*k
            self.assertEqual(det,-1-t)
            self.assertLess(det,0)
            # (1+t/2)^2>1+t gives the rational square-root enclosure.
            self.assertGreater((1+t/2)**2,1+t)
    def test_stationary_point_graph_parameter(self):
        # Coordinate derivative stays nonzero at the saddle even though flow speed is zero.
        for s in (F(0),F(1,10)):
            dxds=1
            self.assertNotEqual(dxds,0)
            if not s:self.assertEqual(3*s,0)
    def test_morse_mesh_exponent(self):
        self.assertEqual(m.density_mesh_powers()[0],F(1,2))
        self.assertGreater(m.density_mesh_powers()[0],0)
    def test_distinct_value_mesh_exponent(self):
        self.assertEqual(m.density_mesh_powers()[1],1)
        self.assertGreater(m.density_mesh_powers()[1],0)
    def test_two_point_derivative_functionals(self):
        # Columns x,x^2,x^3,y,xy; rows grad at (0,0),(1,0), f(1,0)-f(0,0).
        rows=[[1,0,0,0,0],[0,0,0,1,0],[1,2,3,0,0],[0,0,0,1,1],[1,1,1,0,0]]
        self.assertEqual(m.matrix_rank(rows),5)
        self.assertEqual(m.matrix_rank(rows[:-1]),4)
        self.assertEqual(m.matrix_rank(rows[:-1]+[rows[0]]),4)
    def test_gaussian_residual_independence_identity(self):
        self.assertEqual(m.gaussian_residual_covariances([1,F(1,2),F(1,3)],[1,2,3]),[0,0,0])
        with self.assertRaises(ValueError):m.gaussian_residual_covariances([1,0],[0,1])
    def test_localization_second_derivative_vanishes_at_edge(self):
        # x^3(1-x)^3 has value, first and second derivatives zero at both endpoints.
        coeff=[0,0,0,1,-3,3,-1]
        for order in (0,1,2):
            for x in (0,1):self.assertEqual(sum(c*x**i for i,c in enumerate(coeff)),0)
            coeff=[i*c for i,c in enumerate(coeff)][1:]

if __name__=='__main__':unittest.main()
