"""Finite algebra and scaling controls, not an analytic proof checker."""
from fractions import Fraction as Q
from math import comb, factorial
import unittest
import annulus_bridge as a


def determinant(m):
    if len(m) == 1:
        return m[0][0]
    return sum(((-1)**j*m[0][j]*determinant([row[:j]+row[j+1:] for row in m[1:]])
                for j in range(len(m))), Q(0))


def gram(m):
    return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in m] for row in m]



def value(p,x=0,z=0):
    return sum((c*x**i*z**j for (i,j),c in p.items()),Q(0))


def dval(p,i,j,x=0,z=0):
    # Avoid integer truncation for rational coefficients in the derivative.
    return sum((c*Q(factorial(px),factorial(px-i))*Q(factorial(pz),factorial(pz-j))
                *x**(px-i)*z**(pz-j)
                for (px,pz),c in p.items() if px>=i and pz>=j),Q(0))


def solve(matrix,rhs):
    rows=[[Q(x) for x in row]+[Q(y)] for row,y in zip(matrix,rhs)]
    for j in range(len(rows)):
        i=next(i for i in range(j,len(rows)) if rows[i][j])
        rows[i],rows[j]=rows[j],rows[i]
        scale=rows[j][j]; rows[j]=[x/scale for x in rows[j]]
        for i in range(len(rows)):
            if i!=j:
                scale=rows[i][j]; rows[i]=[x-scale*y for x,y in zip(rows[i],rows[j])]
    return [row[-1] for row in rows]


def six_pin_cubic(r,k=Q(1),q=Q(0),c=Q(0),d=Q(0),az=Q(-2),birth=Q(0)):
    # Raw endpoint interpolation, independent of a.contact_gradient().
    free={(0,2):az/2,(2,1):q/2,(1,2):c/2,(0,3):d/6}
    pivots=((0,0),(1,0),(2,0),(3,0),(0,1),(1,1))
    rows=[];rhs=[]
    for dx,dz,sign,target in ((0,0,-1,birth),(0,0,1,birth-k*r**3),
                              (1,0,-1,0),(1,0,1,0),(0,1,-1,0),(0,1,1,0)):
        x=sign*r/2
        rows.append([dval({p:Q(1)},dx,dz,x,0) for p in pivots])
        rhs.append(target-dval(free,dx,dz,x,0))
    free.update(zip(pivots,solve(rows,rhs)))
    return free


class BridgeControls(unittest.TestCase):
    def test_missing_geometric_factor_prevents_cubic_count(self):
        ledger=a.power_ledger()
        self.assertEqual(ledger['outer_physical_r_power'],1)
        self.assertEqual(ledger['outer_scaled_r_power'],3)

    def test_outer_inverse_transverse_power(self):
        self.assertEqual(a.power_ledger()['outer_inverse_v_power'],14)

    def test_axis_raw_power_retained_before_exponential(self):
        self.assertEqual(a.power_ledger()['inner_physical_r_power'],-13)

    def test_seventh_exponential_term_absorbs_both_losses(self):
        ledger=a.power_ledger()
        self.assertEqual(ledger['absorption_order'],7)
        self.assertEqual(ledger['inner_after_absorption_r_power'],1)
        self.assertEqual(ledger['outer_after_absorption_v_power'],0)

    def test_no_height_window_inserted(self):
        self.assertEqual(a.power_ledger()['height_window_r_power'],0)
        self.assertTrue(a.result()['all_witness_heights'])

    def test_no_mathematical_acceptance_from_program(self):
        self.assertIs(a.result()['mathematical_acceptance'],False)
        self.assertEqual(a.result()['scientific_effect'],'NONE')
        self.assertIs(a.result()['global_RN_closed'],False)

    def test_covariance_rows_axis_and_outer_aspect(self):
        for u in (Q(-3),Q(-2),Q(3,2),Q(2),Q(3)):
            for alpha,beta in ((Q(1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1)),(Q(3,5),Q(4,5)),(Q(3,5),Q(-4,5))):
                m=a.aspect_matrix(u,alpha,beta)
                self.assertGreater(determinant(gram(m)),0)

    def test_all_three_minors_not_only_axis_minor(self):
        for u in (Q(-2),Q(2)):
            for alpha,beta in ((Q(0),Q(1)),(Q(1),Q(0)),(Q(3,5),Q(4,5))):
                m=a.aspect_matrix(u,alpha,beta)
                actual=[determinant([[row[i],row[j]] for row in m]) for i,j in ((0,1),(0,2),(1,2))]
                self.assertEqual(actual,list(a.aspect_minors(u,alpha,beta)))
                self.assertEqual(determinant(gram(m)),sum(x*x for x in actual))

    def test_compact_rank_floor(self):
        for u in (Q(-3),Q(-2),Q(3,2),Q(2),Q(3)):
            for alpha,beta in ((Q(0),Q(1)),(Q(1),Q(0)),(Q(3,5),Q(4,5)),(Q(5,13),Q(12,13))):
                self.assertGreaterEqual(determinant(gram(a.aspect_matrix(u,alpha,beta))),a.rank_floor(u))

    def test_aspect_domain_rejects_nonunit_pair(self):
        with self.assertRaises(ValueError):
            a.aspect_matrix(Q(2),Q(1),Q(1))

    def test_aspect_domain_rejects_negative_alpha(self):
        with self.assertRaises(ValueError):
            a.aspect_matrix(Q(2),Q(-1),Q(0))

    def test_pin_neighborhood_not_in_axial_rank_domain(self):
        for u in (Q(0),Q(1,2),Q(1),Q(-1)):
            with self.assertRaises(ValueError):
                a.aspect_matrix(u,Q(1),Q(0))

    def test_fixed_transverse_minor_uses_random_jets_not_k(self):
        for u in (Q(-2),Q(0),Q(2)):
            for v in (Q(-2),Q(-1,3),Q(1,5),Q(2)):
                m=a.transverse_matrix(u,v)
                minor=determinant([[row[0],row[2]] for row in m])
                self.assertEqual(minor,-v**3/2)

    def test_exact_six_pin_gradient_and_shift(self):
        for r in (Q(1,7),Q(1,31)):
            for u,v in ((Q(2),Q(0)),(Q(2),Q(1,2)),(Q(0),Q(2)),(Q(-2),Q(-1,3))):
                p=six_pin_cubic(r,k=Q(3),q=Q(5),c=Q(7),d=Q(11))
                expected=a.contact_gradient(3,u,v,5,7)
                self.assertEqual(dval(p,1,0,r*u,r*v)/r**2,expected)
                self.assertEqual(dval(p,1,0,-r/2,0),0)
                self.assertEqual(dval(p,0,1,r/2,0),0)

    def test_original_pin_drift_is_45_over_2(self):
        self.assertEqual(a.contact_gradient(1,Q(2),Q(0),0,0),Q(45,2))

    def test_geometric_suppression_at_axis_uses_crude_branch(self):
        self.assertEqual(a.suppression(Q(1,5),Q(0)),1)

    def test_geometric_suppression_across_crossover(self):
        r=Q(1,5)
        for v in (Q(1,10),Q(1,5),Q(2,5),Q(-2,5)):
            self.assertEqual(a.suppression(r,v), min(Q(1),(r/abs(v))**6))

    def test_incompatible_nonpositive_r_rejected(self):
        for r in (Q(0),Q(-1)):
            with self.assertRaises(ValueError):
                a.suppression(r,Q(1))

    def test_raw_triple_gradient_fixtures_and_hessian_geometry(self):
        B=Q(3); C=16*(B+1)**2
        for r in (Q(1,5),Q(1,31)):
            for u,v in ((Q(2),Q(1,2)),(Q(-2),Q(1,3)),(Q(0),Q(2)),(Q(2),Q(1,17))):
                # Solve the two witness-gradient conditions for az and c.
                base=six_pin_cubic(r,q=Q(1),d=Q(2),az=Q(0),c=Q(0))
                pa=six_pin_cubic(r,q=Q(1),d=Q(2),az=Q(1),c=Q(0))
                pc=six_pin_cubic(r,q=Q(1),d=Q(2),az=Q(0),c=Q(1))
                mat=[];rhs=[]
                for dx,dz in ((1,0),(0,1)):
                    y=dval(base,dx,dz,r*u,r*v)
                    mat.append([dval(pa,dx,dz,r*u,r*v)-y,dval(pc,dx,dz,r*u,r*v)-y])
                    rhs.append(-y)
                az,c=solve(mat,rhs)
                p=six_pin_cubic(r,q=Q(1),d=Q(2),az=az,c=c)
                M3=sum(Q(comb(3,j))*abs(dval(p,3-j,j)) for j in range(4))
                product=Q(1)
                for x,z in ((-r/2,Q(0)),(r/2,Q(0)),(r*u,r*v)):
                    self.assertEqual(dval(p,1,0,x,z),0)
                    self.assertEqual(dval(p,0,1,x,z),0)
                    xx,xz,zz=(dval(p,2,0,x,z),dval(p,1,1,x,z),dval(p,0,2,x,z))
                    self.assertLessEqual(xx*xx+2*xz*xz+zz*zz,(C*r*M3/abs(v))**2)
                    product*=abs(xx*zz-xz*xz)
                self.assertLessEqual(product,(C*r/abs(v))**6*M3**6)

    def test_annulus_small_v_implies_longitudinal_separation(self):
        A=Q(3,2); lower=Q(5,4); eps=Q(1,4)
        self.assertGreater(A*A-eps*eps,lower*lower)
        for u,v in ((Q(3,2),Q(1,5)),(Q(-2),Q(0)),(Q(0),Q(2))):
            if A*A<=u*u+v*v and abs(v)<=eps:
                self.assertGreater(abs(u),lower)

    def test_exponential_absorption_coefficients_exact(self):
        self.assertEqual(a.absorption_constant(Q(2)),Q(factorial(7),2**7))
        with self.assertRaises(ValueError):
            a.absorption_constant(Q(0))


if __name__=='__main__':
    unittest.main()
