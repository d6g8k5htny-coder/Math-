"""Exact finite controls for the joint-mass scalar reduction, not a field proof."""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / 'reviews' / 'd2_joint_mass_schur_20261006'


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def poly_sub(a, b):
    out = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): out[i] += x
    for i, x in enumerate(b): out[i] -= x
    while len(out) > 1 and out[-1] == 0: out.pop()
    return out


def poly_der(a):
    return [i * a[i] for i in range(1, len(a))]


class JointMassTests(unittest.TestCase):
    def setUp(self):
        path = PACKET / 'joint_mass.py'
        self.assertTrue(path.is_file(), 'missing joint-mass implementation')
        spec = importlib.util.spec_from_file_location('joint_mass_under_test', path)
        self.j = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.j)

    def test_residual_square_identity(self):
        for p, q in [(F(1,4), F(1,4)), (F(1,5), F(2,5)), (F(1,3),F(1,6))]:
            for u, v in [(F(1),F(4)),(F(1,3),F(3)),(F(2),F(5,2))]:
                P=p+q; w=1-P; a=p*u+q*v
                for z in [F(0),F(1,2),F(2),F(5)]:
                    s=a+w*z
                    g=p*u*u+q*v*v+w*z*z-s*s
                    self.assertEqual(g, self.j.variance_floor(s,p,q,u,v))
                    # Splitting residual mass increases variance by w Var(residual).
                    eps=F(1,4)
                    if z>=eps:
                        actual=p*u*u+q*v*v+w*((z-eps)**2+(z+eps)**2)/2-s*s
                        self.assertEqual(actual-g,w*eps**2)

    def test_attaining_laws(self):
        for p,q in [(F(1,4),F(1,4)),(F(1,7),F(2,7))]:
            for u,v in [(F(1),F(4)),(F(1,2),F(3))]:
                a=p*u+q*v; c=a/(p+q)
                for k in range(9):
                    s=a+(c-a)*F(k,8)
                    law=self.j.attaining_squared_law(s,p,q,u,v)
                    self.assertEqual(sum(m for _,m in law),1)
                    self.assertTrue(all(y>=0 and m>=0 for y,m in law))
                    self.assertEqual(sum(y*m for y,m in law),s)
                    self.assertEqual(sum(y*y*m for y,m in law)-s*s,
                                     self.j.variance_floor(s,p,q,u,v))

    def test_endpoint_reduction(self):
        for s in [F(1,3),F(1),F(5,4),F(5,2),F(7)]:
            for g in [F(1,7),F(9,8),F(3),F(15)]:
                e0,e1=self.j.endpoints(s*s,g)
                self.assertEqual(self.j.schur(s,g,F(0)),e0)
                self.assertEqual(self.j.schur(s,g,F(1,4)),e1)
                for k in range(17):
                    self.assertGreaterEqual(self.j.schur(s,g,F(k,64)),min(e0,e1))

    def test_strict_box_improvement(self):
        p=q=F(1,4); u=F(1);v=F(4); a=F(5,4);c=F(5,2)
        box=min(self.j.endpoints(a*a,F(9,8)))
        self.assertEqual(box,F(153,86))
        for k in range(33):
            s=a+(c-a)*F(k,32)
            joint=min(self.j.endpoints(s*s,self.j.variance_floor(s,p,q,u,v)))
            self.assertGreater(joint,box)

    def test_mass_one_boundary(self):
        p=F(1,3);q=F(2,3);u=F(1);v=F(4);a=p*u+q*v
        self.assertEqual(self.j.variance_floor(a,p,q,u,v),F(2))
        self.assertEqual(self.j.attaining_squared_law(a,p,q,u,v),[(u,p),(v,q)])
        with self.assertRaises(ValueError): self.j.variance_floor(a+1,p,q,u,v)

    def test_invalid_domains(self):
        for vals in [(0,F(1,4),1,4),(F(1,2),F(3,4),1,4),
                     (F(1,4),F(1,4),0,4),(F(1,4),F(1,4),1,1)]:
            with self.assertRaises(ValueError): self.j.parameters(*map(F,vals))
        with self.assertRaises(ValueError): self.j.variance_floor(F(1),F(1,4),F(1,4),F(1),F(4))
        with self.assertRaises(ValueError): self.j.schur(F(1),F(1),F(-1))
        with self.assertRaises(ValueError): self.j.schur(F(1),F(1),F(1,3))
        with self.assertRaises(ValueError): self.j.endpoints(F(0),F(1))

    def test_homogeneity_and_swap(self):
        p=F(1,4);q=F(1,3);u=F(1);v=F(4);s=F(2)
        g=self.j.variance_floor(s,p,q,u,v)
        self.assertEqual(g,self.j.variance_floor(s,q,p,v,u))
        for k in [F(1,2),F(2),F(7)]:
            scaled=self.j.variance_floor(k*s,p,q,k*u,k*v)
            self.assertEqual(scaled,k*k*g)
            for t in [F(0),F(1,8),F(1,4)]:
                self.assertEqual(self.j.schur(k*s,scaled,t),k*k*self.j.schur(s,g,t))

    def test_derivative_coefficients(self):
        # Independent coefficient operations derive both rational derivatives.
        n0=poly_mul([59,-40,8],[59,-40,24]);d0=[472,-320,128]
        diff0=poly_sub(poly_mul(poly_der(n0),d0),poly_mul(n0,poly_der(d0)))
        self.assertEqual(diff0,[64*x for x in self.j.POLY_P])
        n1=[0,0,236,-160,96];d1=[59,-40,40]
        diff1=poly_sub(poly_mul(poly_der(n1),d1),poly_mul(n1,poly_der(d1)))
        self.assertEqual(diff1,[0]+[8*x for x in self.j.POLY_R])

    def test_bernstein_and_unique_root(self):
        b0=self.j.bernstein(self.j.POLY_P,F(5,4),F(5,2))
        b1=self.j.bernstein(self.j.POLY_R,F(5,4),F(5,2))
        self.assertEqual(b0,list(map(F,[-2125,F(-8351,4),F(-10127,4),F(-5639,2),-2626,405])))
        self.assertEqual(b1,[F(9899,4),F(14099,4),F(35311,6),F(10806),F(21881)])
        self.assertTrue(all(x<0 for x in b0[:-1]) and b0[-1]>0)
        self.assertTrue(all(x>0 for x in b1))
        for k in range(17):
            t=F(k,16); s=F(5,4)+F(5,4)*t
            for coeff,b in [(self.j.POLY_P,b0),(self.j.POLY_R,b1)]:
                from math import comb
                n=len(b)-1
                self.assertEqual(self.j.evaluate(coeff,s),sum(b[j]*comb(n,j)*t**j*(1-t)**(n-j) for j in range(n+1)))

    def test_certified_example(self):
        c=self.j.certify_example()
        lo,hi=map(F,c['minimizer_rational_interval'])
        L,U=map(F,c['schur_rational_interval'])
        self.assertLess(lo,hi)
        self.assertLess(self.j.evaluate(self.j.POLY_P,lo),0)
        self.assertGreater(self.j.evaluate(self.j.POLY_P,hi),0)
        self.assertLess(F(2464780131951,10**12),lo)
        self.assertLess(hi,F(2464780131952,10**12))
        self.assertLess(F(2076345574173,10**12),L)
        self.assertLess(U,F(2076345574174,10**12))
        gl=F(9,8)+(hi-F(5,2))**2;gu=F(9,8)+(lo-F(5,2))**2
        self.assertEqual(L,self.j.endpoints(lo*lo,gl)[0])
        self.assertEqual(U,self.j.endpoints(hi*hi,gu)[0])
        self.assertLessEqual(F(c['schur_decimal_outer'][0]),L)
        self.assertGreaterEqual(F(c['schur_decimal_outer'][1]),U)
        self.assertLessEqual(F(c['minimizer_decimal_outer'][0]),lo)
        self.assertGreaterEqual(F(c['minimizer_decimal_outer'][1]),hi)
        self.assertGreater(L,F(2))
        self.assertLess(U,min(self.j.endpoints(F(25,16),F(43,16))))
        self.assertEqual(c['scientific_effect'],'NONE')
        self.assertFalse(c['independently_reviewed'])

    def test_source_inventory(self):
        path=PACKET/'SOURCES.json'
        self.assertTrue(path.is_file(),'missing source inventory')
        data=json.loads(path.read_text())
        expected={str((PACKET/name).relative_to(ROOT)) for name in ['NOTE.md','joint_mass.py','RESULTS.json']}
        expected.add(str(Path(__file__).relative_to(ROOT)))
        self.assertEqual({r['path'] for r in data['files']},expected)
        self.assertEqual(len(data['files']),4)
        for record in data['files']:
            b=(ROOT/record['path']).read_bytes()
            self.assertEqual(len(b),record['bytes'])
            self.assertEqual(hashlib.sha256(b).hexdigest(),record['sha256'])
        self.assertEqual(data['scientific_effect'],'NONE')

    def test_results_reproduction(self):
        path=PACKET/'RESULTS.json'
        self.assertTrue(path.is_file(),'missing reference output')
        self.assertEqual(path.read_text(),self.j.render_certificate())


if __name__=='__main__':
    unittest.main(verbosity=2)
