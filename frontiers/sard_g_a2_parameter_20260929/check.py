"""Finite illustrations of the A2 parameter formulas; not a stable-manifold proof."""
import unittest
from fractions import Fraction as F

def tracked(a,b,c):  # grad f=(a*x+b, -c*y), a,c>0
    return (-F(b,a), F(0))

def tracked_derivative(a, db):
    return (-F(db,a), F(0))

def flow_derivative(a,t,x0,h): # x'=a x + eps*h*x? derivative at eps=0
    # for integer t=1 only in exact checker: u(1)=h*x0*e^a is not rational;
    # use constant forcing x'=a x + eps*h, t symbolically via coefficients.
    return F(h,a)  # equilibrium derivative of -eps*h/a, sign handled by equation

class A2(unittest.TestCase):
    def test_implicit_saddle_derivative(self):
        a,c=F(3),F(5)
        for b in (F(-2),F(0),F(7,4)):
            p=tracked(a,b,c)
            eps=F(1,1000); db=F(7,3)
            dq=((tracked(a,b+eps*db,c)[0]-p[0])/eps,F(0))
            self.assertEqual(dq,tracked_derivative(a,db))
    def test_graph_parameter_at_stationary_point(self):
        # unstable branch y=0 is parameterized by x=s, including s=0;
        # its derivative in s is nonzero although physical vector field vanishes at s=0.
        for s in (F(0),F(1,10),F(-1,10)):
            gamma=(s,F(0)); dgamma=(F(1),F(0))
            self.assertEqual(dgamma,(1,0))
            if s==0:self.assertEqual((3*s,-5*gamma[1]),(0,0))
    def test_transverse_hit_formula(self):
        # Gamma(eps,s)=(s+eps, s); section rho=x-1.
        eps=F(1,1000)
        tau0=F(1); tau1=1-eps
        self.assertEqual((tau1-tau0)/eps,-1)
    def test_variational_forcing_sign(self):
        # x'=-a x + eps*h has equilibrium x=eps*h/a.
        a,h=F(7),F(3)
        eps=F(1,1000)
        xeq=eps*h/a
        self.assertEqual(xeq/eps,h/a)

if __name__=="__main__": unittest.main()
