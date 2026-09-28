"""Finite exact tests, not a continuum/Gaussian proof checker."""
from fractions import Fraction as F
from itertools import product
import unittest
import algebra as a


def ev(p,x,z):
    return sum((c*x**i*z**j for (i,j),c in p.items()),F(0))


def diff(p,axis):
    q={}
    for (i,j),c in p.items():
        ij=[i,j]
        if ij[axis]:
            d=ij.copy();d[axis]-=1
            q[tuple(d)]=c*ij[axis]
    return q


def rank(m):
    m=[list(map(F,row)) for row in m];r=0
    for c in range(len(m[0])):
        piv=next((j for j in range(r,len(m)) if m[j][c]),None)
        if piv is None:continue
        m[r],m[piv]=m[piv],m[r]
        pivot=m[r][c];m[r]=[x/pivot for x in m[r]]
        for j in range(r+1,len(m)):
            fac=m[j][c]
            m[j]=[x-fac*y for x,y in zip(m[j],m[r])]
        r+=1
        if r==len(m):break
    return r


def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
           -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
           +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def pinned(r,k,S,T,C,D,quartic=F(0)):
    return {(3,0):2*k,(1,0):-3*k*r*r/2,(0,2):S/2,
            (2,1):T/2,(0,1):-T*r*r/8,(1,2):C/2,
            (0,3):D/6,(0,4):quartic}


class IntermediateTests(unittest.TestCase):
    def test_contact_rank_survives_confluence(self):
        pts=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),
             (F(0),F(-1)),(F(3,5),F(4,5)),(F(6,5),F(1,5))]
        for eps,(u,v) in product([F(0),F(1,4),F(1,32),F(1,2**40)],pts):
            with self.subTest(eps=eps,u=u,v=v):
                self.assertEqual(rank(a.observation_matrix(eps,u,v)),9)

    def test_degree_four_collinear_contact_loses_rank(self):
        for u in [F(1),F(-1),F(2)]:
            self.assertEqual(rank(a.observation_matrix(F(0),u,F(0),degree=4)),8)

    def test_contact_kernel_minors(self):
        for u,v in product([F(-2),F(0),F(3,5)],[F(-1),F(1,8),F(2)]):
            pol=[{(0,2):F(1)},{(0,3):F(1)},{(1,2):F(1)}]
            m=[[ev(p,u,v) for p in pol],
               [ev(diff(p,0),u,v) for p in pol],
               [ev(diff(p,1),u,v) for p in pol]]
            self.assertEqual(det3(m),-v**6)
        for u in [F(-2),F(-1),F(1),F(2)]:
            pol=[{(4,0):F(1)},{(5,0):F(1)},{(2,1):F(1)}]
            m=[[ev(p,u,F(0)) for p in pol],
               [ev(diff(p,0),u,F(0)) for p in pol],
               [ev(diff(p,1),u,F(0)) for p in pol]]
            self.assertEqual(det3(m),u**10)

    def test_hermite_exact_target(self):
        for r,k,b in product([F(1,8),F(1,128)],[F(1),F(6,5)],[F(-1),F(7,5)]):
            raw=(b,F(0),b-k*r**3,F(0),F(0),F(0))
            self.assertEqual(a.hermite_data(r,raw),(b-k*r**3/2,-3*k*r*r/2,F(0),12*k,F(0),F(0)))

    def test_scaled_frame_matches_polynomial(self):
        for eps,s in product([F(1,4),F(1,2**30)],[F(1,8),F(1,32)]):
            r=eps*s
            poly={(0,0):F(3),(1,0):F(2),(3,0):F(-1),(5,0):F(7),(2,1):F(5),(1,1):F(-2)}
            raw=(ev(poly,-r/2,0),ev(diff(poly,0),-r/2,0),ev(poly,r/2,0),
                 ev(diff(poly,0),r/2,0),ev(diff(poly,1),-r/2,0),ev(diff(poly,1),r/2,0))
            frame=a.hermite_data(r,raw)
            matrix=a.observation_matrix(eps,F(1),F(0))
            mons=a.monomials(5)
            coef=[poly.get(ij,F(0))*s**sum(ij) for ij in mons]
            got=[sum(x*y for x,y in zip(row,coef)) for row in matrix[:6]]
            self.assertEqual(got,[x*s**j for x,j in zip(frame,[0,1,2,3,1,2])])

    def test_normalized_value_gradient_of_pinned_cubic(self):
        cases=0
        for eps,s,k,u,v in product([F(1,4),F(1,16)],[F(1,8),F(1,64)],
                [F(1),F(6,5)],[F(-1),F(0),F(3,5)],[F(-1),F(1,8)]):
            r=eps*s;S,T,C,D=F(-2),F(3),F(5),F(-7)
            p=pinned(r,k,S,T,C,D);x,z=s*u,s*v
            fx,fz=ev(diff(p,0),x,z),ev(diff(p,1),x,z)
            actual=a.reduced_value_gradient(s,v,fx,fz,ev(p,x,z))
            de=u*u-eps*eps/4
            expected=(6*k*de+u*v*T+v*v*C/2,
                v*S+s*de*T/2+s*u*v*C+s*v*v*D/2,
                k*(2*u**3-3*eps*eps*u/2)+v*de*T/4-v**3*D/12)
            self.assertEqual(actual,expected);cases+=1
        self.assertEqual(cases,48)

    def test_transverse_three_column_minor(self):
        for eps,u,v in product([F(0),F(1,4)],[F(-1),F(0),F(1)],[F(-1),F(1,100),F(1)]):
            b=a.transverse_matrix(eps,u,v)
            m=[[row[j] for j in [1,2,3]] for row in b]
            self.assertEqual(abs(det3(m)),abs(v)**6/24)
            gram=[[sum(x*y for x,y in zip(p,q)) for q in b] for p in b]
            self.assertGreaterEqual(det3(gram),v**12/576)

    def test_physical_jacobian_includes_height(self):
        for s,v in product([F(1,8),F(1,64)],[F(-1),F(0),F(1,8)]):
            self.assertEqual(det3(a.physical_matrix(s,v)),s**6)

    def test_euler_identity_cancels_cubic(self):
        p={(i,n-i):F((i+1)*(n+1)) for n in range(1,6) for i in range(n+1)}
        for x,z in product([F(-1,4),F(1,8)],[F(-1,8),F(1,16)]):
            exact=3*ev(p,x,z)-x*ev(diff(p,0),x,z)-z*ev(diff(p,1),x,z)
            self.assertEqual(a.euler_remainder(p,x,z),exact)
        p={(i,3-i):F(i+1) for i in range(4)}
        self.assertEqual(a.euler_remainder(p,F(1,7),F(-1,9)),0)

    def test_quartic_height_fixture_needs_s_squared_curvature(self):
        for s in [F(1,8),F(1,32),F(1,128)]:
            r=s**3;k=F(1);q=F(-2)
            S=2*q*s*s;C=3*k*r*r/(s*s);D=-12*q*s
            p=pinned(r,k,S,F(0),C,D,q)
            self.assertEqual(ev(p,0,s),0)
            self.assertEqual(ev(diff(p,0),0,s),0)
            self.assertEqual(ev(diff(p,1),0,s),0)
            self.assertEqual(S,2*q*s*s)
            self.assertTrue(a.height_in_window(r,k,ev(p,0,s)))

    def test_cubic_height_fixture_needs_r_squared_over_s(self):
        for s in [F(1,8),F(1,32),F(1,128)]:
            r=s*s;k=F(1);T=F(2)
            S=r*r*T/(2*s);C=3*k*r*r/s**2;D=-3*r*r*T/(4*s*s)
            p=pinned(r,k,S,T,C,D)
            for x in [-r/2,r/2]:
                self.assertEqual(ev(diff(p,0),x,0),0)
                self.assertEqual(ev(diff(p,1),x,0),0)
            self.assertEqual(ev(p,0,s),0)
            self.assertEqual(ev(diff(p,0),0,s),0)
            self.assertEqual(ev(diff(p,1),0,s),0)

    def test_without_height_window_suppression_fails(self):
        for n in [16,32,64,128]:
            s=F(1,n);r=s**3;k=F(1);S=-s/2
            p=pinned(r,k,S,F(0),3*r*r/s**2,F(1))
            self.assertEqual(ev(diff(p,0),0,s),0)
            self.assertEqual(ev(diff(p,1),0,s),0)
            self.assertEqual(ev(p,0,s),-s**3/12)
            self.assertFalse(a.height_in_window(r,k,ev(p,0,s)))
            self.assertGreaterEqual(abs(S)/(r*r/s+s*s),1/(4*s))

    def test_crossover_relative_error(self):
        for n in [2,4,16,256]:
            s=F(1,n**8);v=F(1,n)
            self.assertEqual(s/v**4,F(1,n**4))
            self.assertLessEqual(s*s+v*v,2*F(1,n*n))

    def test_shell_gain_and_dyadic_sum(self):
        for n in [8,16,32,80]:
            r=F(1,2**n);A=F(4);rho=F(1,8);s=A*r;total=F(0)
            while s<rho:
                self.assertLessEqual((r+s*s)**2/s**2,2*((r/s)**2+s*s))
                total+=a.shell_weight(r,s);s*=2
            self.assertLessEqual(total,F(4,3)*(1/A**2+rho**2))

    def test_one_normalizer_joint_density_and_height_ledger(self):
        self.assertEqual(a.ledger(),{'actual_observations':9,'height_length_r_power':3,
            'endpoint_product_r_power':2,'normalizer_r_power':-2,'raw_density_s_power':-15,
            'raw_moment_s_power':-60,'near_absorption_s_power':75,'near_final_s_power':0,
            'far_density_s_power':-6,'far_product_s_power':2,'far_total_v_power':-60,
            'shell_height_r_power':3,'shell_gain':'(r/s)^2+s^2'})

if __name__=='__main__':unittest.main(verbosity=2)
