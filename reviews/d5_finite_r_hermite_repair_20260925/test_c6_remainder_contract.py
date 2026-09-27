"""Exact finite-pin regression oracle; finite checks are not continuum acceptance.

Fixtures solve six raw endpoint equations by rational Gaussian elimination.
They do not use corrected() or exact_witness() to construct the polynomial.
"""
from fractions import Fraction as Q
from math import factorial
import unittest
import finite_r_contact as subject

PINS = ((0, 0, -1), (0, 0, 1), (1, 0, -1),
        (1, 0, 1), (0, 1, -1), (0, 1, 1))
PIVOTS = ((0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1))
FREE = tuple((i, j) for n in range(7) for i in range(n+1)
             for j in [n-i] if (i, j) not in PIVOTS)
B = Q(3)
C0 = Q(121, 15360)
CX = Q(7,960)+Q(27,320)*B+Q(3,160)*B**2+Q(4,3)*B**3
CA = Q(1,384)+Q(27,640)*B+B**3/6
CY = Q(49,384)+Q(27,640)*B+2*B**2
CH = C0+Q(19,1920)*B+Q(81,1280)*B**2+B**3/160+Q(2,3)*B**4
POINTS = ((Q(2),Q(0)),(Q(-2),Q(0)),(Q(2),Q(1,2)),
          (Q(-2),Q(-1,2)),(Q(0),Q(2)),(Q(3),Q(3)),(Q(1,2),Q(0)))


def derivative(poly, dx=0, dz=0):
    result = {}
    for (i,j), coefficient in poly.items():
        if i >= dx and j >= dz:
            factor = factorial(i)//factorial(i-dx)*factorial(j)//factorial(j-dz)
            result[i-dx,j-dz] = coefficient*factor
    return result


def evaluate(poly, x=0, z=0):
    return sum((c*Q(x)**i*Q(z)**j for (i,j),c in poly.items()), Q(0))


def value(poly, dx=0, dz=0, x=0, z=0):
    return evaluate(derivative(poly,dx,dz),x,z)


def solve(matrix, rhs):
    rows = [[Q(v) for v in row]+[Q(y)] for row,y in zip(matrix,rhs)]
    n=len(rows)
    for col in range(n):
        pivot=next((i for i in range(col,n) if rows[i][col]),None)
        if pivot is None:
            raise ValueError('singular six-pin design')
        rows[col],rows[pivot]=rows[pivot],rows[col]
        scale=rows[col][col];rows[col]=[v/scale for v in rows[col]]
        for i in range(n):
            if i!=col:
                factor=rows[i][col]
                rows[i]=[v-factor*w for v,w in zip(rows[i],rows[col])]
    return [row[-1] for row in rows]


def pin_polynomial(r, free, b=Q(2), k=Q(1)):
    r=Q(r)
    if r<=0:
        raise ValueError('positive separation required')
    free={p:Q(c) for p,c in free.items()}
    if any(p in PIVOTS for p in free):
        raise ValueError('free coordinate overlaps pinned unknown')
    matrix=[];rhs=[];targets=[b,b-k*r**3,0,0,0,0]
    for (dx,dz,sign),target in zip(PINS,targets):
        x=sign*r/2
        matrix.append([value({p:Q(1)},dx,dz,x,0) for p in PIVOTS])
        rhs.append(target-value(free,dx,dz,x,0))
    result=dict(free)
    result.update(zip(PIVOTS,solve(matrix,rhs)))
    return result


def c6_ceiling(poly, radius):
    # Triangle inequality bounds every partial derivative of total order <=6
    # everywhere on the square |x|,|z| <= radius.
    return max(sum((abs(c)*radius**(i+j) for (i,j),c in derivative(poly,dx,n-dx).items()),Q(0))
               for n in range(7) for dx in range(n+1))


class C6RemainderContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases=[]
        for r in (Q(1,5),Q(1,11),Q(1,31)):
            for monomial in FREE:
                free={(0,2):Q(-1)}
                free[monomial]=free.get(monomial,Q(0))+Q(1,7)
                p=pin_polynomial(r,free)
                cls.cases.append((r,p,c6_ceiling(p,B*r)))

    def test_all_twenty_two_free_directions_are_used(self):
        self.assertEqual(len(FREE),22)
        self.assertTrue({(6,0),(5,1),(0,6),(4,2)}.issubset(FREE))

    def test_raw_six_pins_hold_in_every_generated_fixture(self):
        for r,p,_ in self.cases:
            self.assertEqual(value(p,0,0,-r/2,0),2)
            self.assertEqual(value(p,0,0,r/2,0),2-r**3)
            for sign in (-1,1):
                self.assertEqual(value(p,1,0,sign*r/2,0),0)
                self.assertEqual(value(p,0,1,sign*r/2,0),0)

    def test_symmetric_longitudinal_average_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p,1,0)+r*r*value(p,3,0)/8),M*r**4/384)

    def test_symmetric_longitudinal_difference_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p,2,0)+r*r*value(p,4,0)/24),M*r**4/1920)

    def test_third_longitudinal_derivative_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p,3,0)-12),Q(3,80)*M*r*r)

    def test_midpoint_height_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p)-2+r**3/2),C0*M*r**4)

    def test_midpoint_longitudinal_drift_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p,1,0)/r**2+Q(3,2)),Q(7,960)*M*r*r)

    def test_symmetric_transverse_average_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p,0,1)+r*r*value(p,2,1)/8),M*r**4/384)

    def test_symmetric_transverse_difference_bound(self):
        for r,p,M in self.cases:
            self.assertLessEqual(abs(value(p,1,1)+r*r*value(p,3,1)/24),M*r**4/1920)

    def test_longitudinal_blowup_uniform_remainder(self):
        for r,p,M in self.cases:
            for u,v in POINTS:
                px,_,_,_=subject.corrected(1,u,v,value(p,0,2),value(p,2,1),value(p,1,2),value(p,0,3))
                self.assertLessEqual(abs(value(p,1,0,r*u,r*v)/r**2-px),CX*M*r)

    def test_axial_transverse_blowup_uniform_remainder(self):
        for r,p,M in self.cases:
            for u in (-B,Q(-2),Q(1,2),Q(2),B):
                _,_,pz,_=subject.corrected(1,u,0,value(p,0,2),value(p,2,1),value(p,1,2),value(p,0,3))
                self.assertLessEqual(abs(value(p,0,1,r*u,0)/r**2-pz),CA*M*r)

    def test_transverse_leading_blowup_uniform_remainder(self):
        for r,p,M in self.cases:
            for u,v in POINTS:
                _,pz,_,_=subject.corrected(1,u,v,value(p,0,2),value(p,2,1),value(p,1,2),value(p,0,3))
                self.assertLessEqual(abs(value(p,0,1,r*u,r*v)/r-pz),CY*M*r)

    def test_height_blowup_uniform_remainder(self):
        for r,p,M in self.cases:
            for u,v in POINTS:
                a=value(p,0,2)
                _,_,_,h=subject.corrected(1,u,v,a,value(p,2,1),value(p,1,2),value(p,0,3))
                self.assertLessEqual(abs((value(p,0,0,r*u,r*v)-2)/r**2-a*v*v/2-r*h),CH*M*r*r)

    def test_cubic_rows_match_constraint_solved_oracle(self):
        r=Q(1,10000)
        p=pin_polynomial(r,{(0,2):-1,(2,1):Q(5,2),(1,2):Q(7,2),(0,3):Q(11,6)})
        for u,v in POINTS:
            px,pz,pa,h=subject.corrected(1,u,v,value(p,0,2),value(p,2,1),value(p,1,2),value(p,0,3))
            self.assertEqual(value(p,1,0,r*u,r*v)/r**2,px)
            self.assertEqual((value(p,0,0,r*u,r*v)-2)/r**2,value(p,0,2)*v*v/2+r*h)
            if v==0:
                self.assertEqual(value(p,0,1,r*u,0)/r**2,pa)

    def test_quartic_longitudinal_error_is_really_order_r(self):
        ratios=[]
        for r in (Q(1,5),Q(1,11),Q(1,31)):
            p=pin_polynomial(r,{(4,0):1,(0,2):-1})
            px=subject.corrected(1,2,0,-2,0,0,0)[0]
            ratios.append((value(p,1,0,2*r,0)/r**2-px)/r)
        self.assertEqual(ratios,[Q(30)]*3)

    def test_required_endpoint_types_are_realized(self):
        r=Q(1,5);p=pin_polynomial(r,{(0,2):-1})
        self.assertEqual(value(p,1,1,-r/2,0),0)
        self.assertEqual(value(p,1,1,r/2,0),0)
        self.assertLess(value(p,2,0,-r/2,0),0)
        self.assertLess(value(p,0,2,-r/2,0),0)
        self.assertLess(value(p,2,0,r/2,0)*value(p,0,2,r/2,0),0)


if __name__ == '__main__':
    unittest.main()
