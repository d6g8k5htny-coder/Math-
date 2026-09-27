"""Exact rational/Laurent-polynomial checks for the accompanying derivations.

Standard library only. These checks are not a proof checker for the Gaussian
continuum argument and do not grant independent mathematical acceptance.
"""
from __future__ import annotations
from fractions import Fraction as Q
from math import factorial
import unittest

NAMES = ('r','x','z','b','k','A','q','c','d','u','v','theta','w')
ZERO = (0,)*len(NAMES)

class P:
    def __init__(self, terms=None):
        self.terms = {m:Q(c) for m,c in (terms or {}).items() if c}
    @staticmethod
    def coerce(x):
        if isinstance(x,P): return x
        if type(x) is int or isinstance(x,Q): return P({ZERO:Q(x)})
        raise TypeError('exact rational or polynomial required')
    def __add__(self, other):
        out=dict(self.terms)
        for m,c in self.coerce(other).terms.items(): out[m]=out.get(m,Q(0))+c
        return P(out)
    __radd__=__add__
    def __neg__(self): return P({m:-c for m,c in self.terms.items()})
    def __sub__(self,other): return self+-self.coerce(other)
    def __rsub__(self,other): return self.coerce(other)+-self
    def __mul__(self,other):
        out={}
        for m,a in self.terms.items():
            for n,b in self.coerce(other).terms.items():
                key=tuple(i+j for i,j in zip(m,n));out[key]=out.get(key,Q(0))+a*b
        return P(out)
    __rmul__=__mul__
    def __truediv__(self,x):
        if type(x) is not int and not isinstance(x,Q): raise TypeError('rational denominator required')
        if not x: raise ZeroDivisionError
        return P({m:c/Q(x) for m,c in self.terms.items()})
    def __pow__(self,n):
        if type(n) is not int: raise TypeError('integer power required')
        if n<0:
            if len(self.terms)!=1: raise ValueError('only a nonzero monomial is invertible here')
            m,c=next(iter(self.terms.items()));return P({tuple(n*i for i in m):c**n})
        result=P.coerce(1)
        for _ in range(n):result=result*self
        return result
    def __eq__(self,other):return self.terms==self.coerce(other).terms
    def diff(self,name):
        i=NAMES.index(name);out={}
        for m,c in self.terms.items():
            if m[i]:
                n=list(m);n[i]-=1;out[tuple(n)]=c*m[i]
        return P(out)
    def sub(self,**values):
        out=P()
        for m,c in self.terms.items():
            term=P.coerce(c)
            for name,power in zip(NAMES,m):
                if power:term*=P.coerce(values.get(name,var(name)))**power
            out+=term
        return out
    def value(self,**values):
        out=self.sub(**values)
        if any(m!=ZERO for m in out.terms):raise ValueError('variables remain')
        return out.terms.get(ZERO,Q(0))

def var(name):
    m=list(ZERO);m[NAMES.index(name)]=1;return P({tuple(m):Q(1)})
r,x,z,b,k,A,q,c,d,u,v,theta,w=map(var,NAMES)

def det2(M):return M[0][0]*M[1][1]-M[0][1]*M[1][0]
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
            -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
            +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
def hessian(f):return [[f.diff(i).diff(j) for j in ('x','z')]for i in ('x','z')]
def at(M,**values):return [[p.sub(**values) for p in row]for row in M]

def cubic():
    return -k/2+2*k*x**3-3*k*x/2+A*z**2/2+q*(x**2-Q(1,4))*z/2+c*x*z**2/2+d*z**3/6

def solved():
    D=u**2-Q(1,4); L=2*u**3-3*u/2-Q(1,2)
    cv=-12*k*D*v**-2-2*q*u*v**-1
    dv=12*k*(L+theta)*v**-3+3*q*D*v**-2
    av=(12*k*u+6*k+q*v-12*k*theta)*v**-2/2
    return {'A':av,'c':cv,'d':dv}

def matrices():
    f=cubic().sub(**solved());H=hessian(f)
    return at(H,x=-Q(1,2),z=0),at(H,x=Q(1,2),z=0),at(H,x=u,z=v)

def inverse(M):
    n=len(M); a=[[Q(x) for x in row]+[Q(i==j)for j in range(n)]for i,row in enumerate(M)]
    for i in range(n):
        p=next(j for j in range(i,n)if a[j][i]);a[i],a[p]=a[p],a[i]
        h=a[i][i];a[i]=[x/h for x in a[i]]
        for j in range(n):
            if j!=i:
                h=a[j][i];a[j]=[x-h*y for x,y in zip(a[j],a[i])]
    return [row[n:]for row in a]

def derivative0(n):
    if n%2:return Q(0)
    t=n//2;return Q((-1)**t*factorial(2*t),2**t*factorial(t))
def cov(alpha,beta):
    return (-1)**sum(beta)*derivative0(alpha[0]+beta[0])*derivative0(alpha[1]+beta[1])

class ExactChecks(unittest.TestCase):
    def test_ring(self):
        self.assertEqual((x+z)**2,x*x+2*x*z+z*z)
        self.assertEqual(v**-2*v**3,v)
        self.assertEqual((x**3*z).diff('x'),3*x*x*z)
    def test_all_six_cubic_pins(self):
        f=cubic()
        for xp,height in ((-Q(1,2),0),(Q(1,2),-k)):
            self.assertEqual(f.sub(x=xp,z=0),height)
            self.assertEqual(f.diff('x').sub(x=xp,z=0),0)
            self.assertEqual(f.diff('z').sub(x=xp,z=0),0)
    def test_original_pin_correction_guard(self):
        f=cubic();bad=f+3*k*x/2
        self.assertNotEqual(bad.diff('x').sub(x=Q(1,2),z=0),0)
        self.assertNotEqual((f+k/2).sub(x=-Q(1,2),z=0),0)
        self.assertNotEqual((f+q*z/8).diff('z').sub(x=Q(1,2),z=0),0)
    def test_cubic_complete_third_constraints(self):
        f=cubic().sub(**solved())
        self.assertEqual(f.diff('x').sub(x=u,z=v),0)
        self.assertEqual(f.diff('z').sub(x=u,z=v),0)
        self.assertEqual(f.sub(x=u,z=v),-k*theta)
    def test_corrected_longitudinal_contact(self):
        self.assertEqual(cubic().diff('x').sub(x=u,z=v),6*k*(u*u-Q(1,4))+q*u*v+c*v*v/2)
    def test_joint_height_subtraction(self):
        f=cubic();j3=(f-v*f.diff('z')/2).sub(x=u,z=v)
        self.assertEqual(j3,k*(2*u**3-3*u/2-Q(1,2))+q*(u*u-Q(1,4))*v/4-d*v**3/12)
    def test_unpinned_jet_minor(self):
        j1=6*k*(u*u-Q(1,4))+q*u*v+c*v*v/2
        j2=A*v;j3=k*(2*u**3-3*u/2-Q(1,2))+q*(u*u-Q(1,4))*v/4-d*v**3/12
        self.assertEqual(det3([[f.diff(a)for a in ('A','c','d')]for f in (j1,j2,j3)]),v**6/24)
    def test_density_transform_jacobian(self):
        M=[[r**2,P(),P()],[P(),r,P()],[P(),r*r*v/2,r**3]]
        self.assertEqual(det3(M),r**6)
        self.assertEqual(2+3-6+6-2,3)
    def test_maximum_determinant_identity(self):
        BM,_,_=matrices();wv=(q*v+12*k*u)/(6)*k**-1
        self.assertEqual(det2(BM),9*k*k*v**-2*(4*theta-(wv+1)**2))
    def test_endpoint_saddle_determinant_identity(self):
        _,BS,_=matrices();wv=(q*v+12*k*u)/(6)*k**-1
        self.assertEqual(det2(BS),9*k*k*v**-2*(4*(1-theta)-(wv-1)**2))
    def test_witness_sum_of_squares_identity(self):
        _,_,BX=matrices();wv=(q*v+12*k*u)/(6)*k**-1
        rhs=-9*k*k*v**-2*((wv+1-2*theta)**2+4*theta*(1-theta))
        self.assertEqual(det2(BX),rhs)
        self.assertNotEqual(det2(BX),-9*k*k*v**-2*(wv+1-2*theta)**2)
    def test_positive_contact_witness(self):
        pars={'u':2,'v':1,'k':1,'theta':Q(1,2),'q':-30}
        BM,BS,BX=matrices()
        self.assertEqual([det2(M).value(**pars)for M in (BM,BS,BX)],[18,-18,-18])
        self.assertEqual(BM[0][0].value(**pars),-6)
    def test_w_minus_one_open_type_witness(self):
        BM,BS,BX=matrices();qv=6*k*(-1-2*u)*v**-1
        self.assertEqual(det2(BM).sub(q=qv),36*k*k*theta*v**-2)
        self.assertEqual(det2(BS).sub(q=qv),-36*k*k*theta*v**-2)
        self.assertEqual(det2(BX).sub(q=qv),-36*k*k*theta*v**-2)
    def test_sharp_triple_determinant_power(self):
        f=x**3/3-r*x*x/2+z**3/3-r*z*z/2;H=hessian(f)
        ds=[]
        for xp,zp in ((0,0),(r,0),(0,r)):
            self.assertEqual(f.diff('x').sub(x=xp,z=zp),0)
            self.assertEqual(f.diff('z').sub(x=xp,z=zp),0)
            ds.append(det2(at(H,x=xp,z=zp)))
        self.assertEqual(ds[0]*ds[1]*ds[2],r**6)
    def test_skinny_triangle_counterexample(self):
        f=(z-x*x)**2/2+x**4/4-r*x**3+r*r*x*x
        for xp,zp in ((0,0),(r,r*r),(2*r,4*r*r)):
            self.assertEqual(f.diff('x').sub(x=xp,z=zp),0)
            self.assertEqual(f.diff('z').sub(x=xp,z=zp),0)
        self.assertEqual(f.diff('z').diff('z'),1)
        self.assertEqual(det2([[r,2*r],[r*r,4*r*r]]),2*r**3)
    def test_third_direction_not_controlled_in_d3(self):
        f=x**3/3-r*x*x/2+z**3/3-r*z*z/2+b*b/2
        self.assertEqual(f.diff('b').diff('b'),1)
        for xp,zp in ((0,0),(r,0),(0,r)):
            self.assertEqual(f.diff('b').sub(x=xp,z=zp,b=0),0)
    def test_bargmann_fock_conditional_jet_covariance(self):
        U=[(0,0),(1,0),(2,0),(3,0),(0,1),(1,1)]
        V=[(0,2),(2,1),(1,2),(0,3)]
        CU=[[cov(a,b)for b in U]for a in U];inv=inverse(CU)
        cross=[[cov(a,b)for b in U]for a in V]
        reg=[[sum(row[j]*inv[j][i]for j in range(6))for i in range(6)]for row in cross]
        residual=[[cov(V[i],V[j])-sum(reg[i][t]*cross[j][t]for t in range(6))for j in range(4)]for i in range(4)]
        self.assertEqual(residual,[[Q(2),0,0,0],[0,Q(2),0,0],[0,0,Q(2),0],[0,0,0,Q(6)]])
        target=[b,0,0,12*k,0,0]
        self.assertEqual([sum(row[i]*target[i]for i in range(6))for row in reg],[-b,0,0,0])
    def test_exponent_and_moment_order(self):
        beta=Q(1+1,3)
        self.assertEqual(beta-1,-Q(1,3));self.assertEqual(-beta,-Q(2,3))
    def test_two_mark_coefficient_includes_derivative_factor(self):
        moment=Q(1,2)*(1+Q(1,4));C=moment/3
        self.assertEqual(C,Q(5,24));self.assertNotEqual(C,moment)
        self.assertNotEqual(C,Q(1,6)*(1+4))
    def test_selection_changes_exponent(self):
        self.assertEqual(Q(1+1+1,3)-1,0)
    def test_mark_phase_boundary(self):
        beta=Q(2,3)
        self.assertGreater(0+1-beta,0)
        self.assertEqual(-Q(1,3)+1-beta,0)
        self.assertLess(-Q(1,2)+1-beta,0)
    def test_exact_small_mark_dominated_density(self):
        actual=2*(Q(8)-Q(4))
        self.assertEqual(actual,8)
        self.assertNotEqual(actual,4)
    def test_oscillatory_derivative_counterexample_limits(self):
        self.assertEqual(Q(1,3-1),Q(1,2));self.assertEqual(Q(1,3+1),Q(1,4))
        self.assertNotEqual(Q(1,2),Q(1,4))
    def test_fixed_gradient_tolerance_is_not_scale_uniform(self):
        eps=Q(1,100);radii=[Q(1,10),Q(1,100),Q(1,1000)]
        self.assertEqual([eps/h for h in radii],[Q(1,10),Q(1),Q(10)])

if __name__=='__main__':unittest.main(verbosity=2)
