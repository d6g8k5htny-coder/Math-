#!/usr/bin/env python3
"""Finite diagnostics and exact evidence-parser controls, not Lean execution."""
from fractions import Fraction as F
import importlib.util
import itertools
from pathlib import Path
import unittest

SIDE = Path(__file__).resolve().parent

class Controls(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SIDE/'check.py').is_file(), 'missing evidence helper')
        spec = importlib.util.spec_from_file_location('d2_square_check', SIDE/'check.py')
        self.c = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.c)

    def test_strict_json(self):
        self.assertEqual(self.c.strict('{"ok":true,"n":1}'), {'ok':True,'n':1})
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1.0}', '{}{}'):
            with self.assertRaises(ValueError): self.c.strict(raw)

    def test_negative_controls_accept_exact_reason(self):
        for name in self.c.CONTROLS:
            msg = f'/tmp/{name}.lean:4:2: error: unsolved goals\n⊢ False\n'
            self.assertEqual(self.c.negative(msg,name,1), name)

    def test_negative_controls_reject_wrong_reason(self):
        name = self.c.CONTROLS[0]
        good = f'{name}.lean:4:2: error: unsolved goals\n⊢ False\n'
        bads = (good.replace('False','True'), good.replace(name,'Other'),
                good+'error: another problem\n', 'error: unknown identifier\n', '')
        for text in bads:
            with self.assertRaisesRegex(ValueError,'intended False'): self.c.negative(text,name,1)
        for code in (0,2,True):
            with self.assertRaisesRegex(ValueError,'exit'): self.c.negative(good,name,code)

    def test_type_inventory(self):
        names = self.c.TARGETS
        good = '\n'.join(n+' : True' for n in names)+'\n'
        self.assertEqual(self.c.types(good), list(names))
        for bad in (good+good, good.replace(names[0],'Other.first'),
                    'warning: unused\n'+good, good.replace(names[-1]+' : True\n','')):
            with self.assertRaises(ValueError): self.c.types(bad)

    def test_weighted_square(self):
        for u,v,a,b,c in itertools.product((F(1,3),F(2)),(F(1,4),F(3)),
                (F(-2),F(0),F(2)),(F(-1),F(3)),(F(-2),F(0),F(4))):
            lhs=u*(a-c)**2+v*(b-c)**2
            floor=u*v/(u+v)*(a-b)**2
            rhs=floor+(u+v)*(c-(u*a+v*b)/(u+v))**2
            self.assertEqual(lhs,rhs);self.assertLessEqual(floor,lhs)

    def test_schur_endpoints_and_input_floors(self):
        for s0,g0,sadd,gadd,q in itertools.product((F(1,3),F(1),F(3)),
                (F(1,4),F(2),F(5)),(F(0),F(2)),(F(0),F(3)),
                (F(0),F(1,16),F(1,4))):
            s,g=s0+sadd,g0+gadd;x=s*s
            a=x*(g+x);b=g*(g+4*x)/4;n=x*g*(g+2*x)
            d=(1-4*q)*a+4*q*b
            self.assertLessEqual(min(g,2*x),n/d)
            self.assertLessEqual(min(g0,2*s0*s0),n/d)

    def test_false_witnesses(self):
        # These are also executable Lean rejection contracts, not generalized facts.
        u,v,a,b,c=map(F,(-2,1,0,1,2))
        self.assertGreater(u*v/(u+v)*(a-b)**2,u*(a-c)**2+v*(b-c)**2)
        self.assertGreater(max(F(1),F(2)),F(3,2))
        self.assertGreater(min(F(1),F(2)),F(-3))

    def test_workflow_fetches_required_history(self):
        # The complete root suite resolves historical proof commits.
        text = (SIDE.parents[1]/'.github/workflows/d2-square-schur.yml').read_text()
        checkout = text.split('uses: actions/checkout@', 1)[1].split('\n      - ', 1)[0]
        settings = [line.strip() for line in checkout.splitlines()
                    if not line.lstrip().startswith('#')]
        self.assertIn('fetch-depth: 0', settings)
        self.assertIn('persist-credentials: false', settings)

    def test_identity_binds_every_byte(self):
        a=self.c.identity(b'abc\n');b=self.c.identity(b'abc')
        self.assertEqual(a['bytes'],4)
        self.assertNotEqual(a['sha256'],b['sha256'])
        self.assertNotEqual(a['git_blob'],b['git_blob'])

if __name__=='__main__':unittest.main(verbosity=2)
