#!/usr/bin/env python3
"""Exact finite controls and evidence-driver tests; not Lean proof execution."""
from fractions import Fraction as F
import importlib.util
import itertools
from pathlib import Path
import tempfile
import unittest

SIDE=Path(__file__).resolve().parent

class AtomIntegralTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue((SIDE/'check.py').is_file(), 'quantitative integral evidence helper absent')
        spec=importlib.util.spec_from_file_location('atom_check',SIDE/'check.py')
        self.c=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.c)

    def test_json_and_byte_identity(self):
        self.assertEqual(self.c.strict('{"n":1}'), {'n':1})
        for raw in ('{"x":1,"x":2}','{"x":NaN}','{"x":1.0}'):
            with self.assertRaises(ValueError): self.c.strict(raw)
        self.assertNotEqual(self.c.identity(b'x'),self.c.identity(b'x\n'))

    def test_negative_reason_not_generic_failure(self):
        for label in self.c.CONTROLS:
            good=f'/tmp/{label}.lean:4:2: error: unsolved goals\n⊢ False\n'
            self.assertEqual(self.c.negative(good,label,1),label)
            for bad in (good.replace('False','True'),good.replace(label,'Wrong'),good+'extra\n',''):
                with self.assertRaises(ValueError): self.c.negative(bad,label,1)
            for code in (0,2,True):
                with self.assertRaises(ValueError): self.c.negative(good,label,code)

    def test_exact_inventory_and_emitted_commands(self):
        self.assertEqual(len(self.c.TARGETS),6)
        good='\n'.join(n+' : True' for n in self.c.TARGETS)+'\n'
        self.assertEqual(self.c.types(good),list(self.c.TARGETS))
        for bad in (good+good,'warning: bad\n'+good,good.replace(self.c.TARGETS[0],'Other.first')):
            with self.assertRaises(ValueError):self.c.types(bad)
        with tempfile.TemporaryDirectory() as td:
            out=Path(td);self.c.emit(out)
            self.assertEqual(set(p.name for p in out.iterdir()),
                             {'Audit.lean','Types.lean'}|{n+'.lean' for n in self.c.CONTROLS})
            self.assertEqual((out/'Audit.lean').read_text().count('#print axioms '),6)
            for name,statement in self.c.FALSE_STATEMENTS.items():
                self.assertIn('example : '+statement,(out/(name+'.lean')).read_text())

    def test_disjoint_event_integral_lower(self):
        weights=(F(1,6),F(1,3),F(1,2))
        for f in itertools.product((F(0),F(1),F(3)),repeat=3):
            for membership in itertools.product((0,1,2),repeat=3):
                S=[i for i in range(3) if membership[i]==1]
                T=[i for i in range(3) if membership[i]==2]
                a=min((f[i] for i in S),default=F(7))
                b=min((f[i] for i in T),default=F(9))
                lhs=sum(weights[i] for i in S)*a+sum(weights[i] for i in T)*b
                self.assertLessEqual(lhs,sum(weights[i]*f[i] for i in range(3)))

    def test_squared_radius_floors_and_schur(self):
        for a,b,p,q,extra in itertools.product((F(1),F(-1,2)),(F(2),F(-3)),
                (F(1,10),F(1,4)),(F(1,5),F(1,3)),(F(0),F(1,7),F(-4))):
            # Split every retained squared-radius mass equally over both signs.
            law=[(a,p/2),(-a,p/2),(b,q/2),(-b,q/2),(extra,1-p-q)]
            s,t=a*a,b*b
            m2,m4,m6=[sum(w*x**n for x,w in law) for n in (2,4,6)]
            s0=p*s+q*t;g0=p*q/(p+q)*(s-t)**2;d0=p*s*q*t/s0*(s-t)**2
            g=m4-m2*m2;delta=m6-m4*m4/m2
            self.assertGreaterEqual(m2,s0);self.assertGreaterEqual(g,g0);self.assertGreaterEqual(delta,d0)
            for u in (F(0),F(1,16),F(1,4)):
                x=m2*m2;D=(1-4*u)*x*m4+4*u*g*(m4+3*x)/4
                self.assertLessEqual(min(g0,2*s0*s0),x*g*(g+2*x)/D)
            if extra==0:self.assertEqual(delta,d0)

    def test_magnitude_mass_is_not_one_signed_atom(self):
        law=[(F(1),F(1,8)),(F(-1),F(1,8)),(F(2),F(1,8)),(F(-2),F(1,8)),(F(0),F(1,2))]
        self.assertEqual(sum(w for x,w in law if x*x==1),F(1,4))
        self.assertLess(sum(w for x,w in law if x==1),F(1,4))

    def test_necessary_boundaries_have_countermodels(self):
        # Coincident full events each mass1 cannot contribute twice to integral1.
        self.assertGreater(F(1)+F(1),F(1))
        # Non-probability measure delta_1+delta_2: unnormalised gap is negative.
        self.assertEqual(F(17)-F(5)**2,F(-8))
        # Half at0 and half on radius1: positive fourth gap, zero cubic residual.
        self.assertGreater(F(1,2)-F(1,2)**2,0)
        self.assertEqual(F(1,2)-F(1,2)**2/F(1,2),0)

    def test_workflow_preserves_history_and_execution(self):
        root=SIDE.parents[1]
        workflow=(root/self.c.WORKFLOW).read_text()
        self.assertIn('fetch-depth: 0',workflow)
        self.assertIn('persist-credentials: false',workflow)
        for path in self.c.CONSUMED:
            self.assertIn(path,workflow)
        shell=(SIDE/'replay.sh').read_text()
        for required in ('formal/gate.py --execute','-DwarningAsError=true','leanchecker --fresh D2AtomIntegral',
                         '-m unittest discover -s tests','-m unittest discover -s formal/tests','Contract.lean'):
            self.assertIn(required,shell)
        self.assertNotIn('continue-on-error',workflow)
        self.assertNotIn('linter.unnecessarySeqFocus false',shell)

if __name__=='__main__':unittest.main(verbosity=2)
