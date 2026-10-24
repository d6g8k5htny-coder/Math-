"""Behavior controls for the new bounded coefficient layer (no target run)."""
import copy
import importlib
import json
from fractions import Fraction as F
from pathlib import Path
import unittest


class PrimitiveTests(unittest.TestCase):
    def modules(self):
        for name in ('coefficient', 'verify_coefficient'):
            self.assertTrue((Path(__file__).parent/(name+'.py')).exists(),
                            'new certificate behavior missing: '+name)
        return importlib.import_module('coefficient'), importlib.import_module('verify_coefficient')

    def test_sixth_root_perfect_and_nonperfect(self):
        p,v=self.modules()
        for x in (F(0),F(1),F(64),F(2),F(1,7),F(10**12)):
            w=p.root_witness(x)
            lo,hi=v.root(w,x)
            self.assertLessEqual(lo**6,x)
            self.assertGreaterEqual(hi**6,x)
            self.assertLessEqual(hi-lo,F(1,2**96))
        self.assertEqual(p.root_witness(F(64)),['2/1','2/1'])

    def test_root_rejects_narrowed_or_wrong_mesh(self):
        p,v=self.modules()
        for w,x in [(['1/1','1/1'],F(2)),(['0/1','2/1'],F(2)),(['-1/1','1/1'],F(1))]:
            with self.assertRaises(ValueError):v.root(w,x)

    def test_gamma_extrema_and_tail_factor(self):
        p,v=self.modules()
        self.assertEqual(p.cell_order(0), (0,1))
        self.assertEqual(p.cell_order(2047), (2047,2048))
        self.assertEqual(p.cell_order(2048), (2049,2048))
        self.assertEqual(p.cell_order(4095), (4096,4095))
        lo,hi,tail=p.gamma_accumulate([(F(1),F(1))]*4097)
        # A synthetic exp witness of one isolates exact Darboux/tail factors.
        self.assertEqual(tail,F(65))
        # The synthetic values isolate the tail, without pretending to obey
        # the exponential's monotonic-integrand hypothesis.
        import moment_kernel
        self.assertEqual(moment_kernel.exp_negative(F(0),bits=96,pairs=24)['result'],['1/1','1/1'])
        e=[F(x) for x in moment_kernel.exp_negative(F(1),bits=96,pairs=24)['result']]
        self.assertTrue(F(1,3)<e[0]<=e[1]<F(3,8))
        with self.assertRaises(ValueError):v.gamma_bounds({'endpoints':[]})

    def test_positive_hulls_and_interior_ratio_adverse_control(self):
        p,v=self.modules()
        m={'mu2':(F(1),F(1)),'mu4':(F(4),F(4)),'mu6':(F(20),F(20))}
        s=p.scalar_bounds(m)
        self.assertEqual(s['D'],(F(4),F(21,4)))
        self.assertEqual(s['V'],(F(4),F(31,4)))
        # V^4/D^9 is the sixth power of the varying angular ratio.
        r=lambda t:(4+15*t)**4/(4+5*t)**9
        self.assertGreater(r(F(4,25)),max(r(F(0)),r(F(1,4))))
        with self.assertRaises(ValueError):p.scalar_bounds({'mu2':(F(1),F(1)),'mu4':(F(1),F(1)),'mu6':(F(1),F(1))})

    def test_constant_identity_in_sixth_power(self):
        p,v=self.modules()
        # Synthetic rational Gamma/pi/scalars isolate every power and 2pi cancellation.
        s={'a':(F(2),F(2)),'H':(F(3),F(3)),'V':(F(5),F(5)),'D':(F(7),F(7))}
        expected=F(11)**6*2**6*3**6*5**4/(4**6*24**2*F(13)**9*7**9)
        self.assertEqual(p.sixth_bounds(s,(F(11),F(11)),(F(13),F(13))),(expected,expected))

    def test_request_and_json_guards(self):
        p,v=self.modules()
        p.check_request(copy.deepcopy(p.REQUEST))
        for key,value in [('d',True),('L','25/1'),('gamma_cells',2048),('goal','1/20')]:
            q=copy.deepcopy(p.REQUEST);q[key]=value
            with self.assertRaises(ValueError):p.check_request(q)
        for text in ('{"a":1,"a":2}','{"a":NaN}','['*10000):
            with self.assertRaises(ValueError):v.strict_json(text)

    def test_width_goal_and_false_status(self):
        p,v=self.modules()
        self.assertEqual(p.outcome((F(1),F(101,100))),'TOLERANCE_MET')
        self.assertEqual(p.outcome((F(1),F(102,100))),'HOLD_TARGET_UNMET')
        with self.assertRaises(ValueError):p.outcome((F(0),F(1)))
        with self.assertRaises(ValueError):v.verify({'schema':'wrong'})

    def test_checker_independently_rejects_false_width_status(self):
        p,v=self.modules()
        self.assertTrue(hasattr(v,'finish'),'checker width behavior missing')
        self.assertEqual(v.finish((F(1),F(101,100)),'1/100','TOLERANCE_MET'),'TOLERANCE_MET')
        self.assertEqual(v.finish((F(1),F(102,100)),'1/50','HOLD_TARGET_UNMET'),'HOLD_TARGET_UNMET')
        for width,status in [('1/100','TOLERANCE_MET'),('0/1','HOLD_TARGET_UNMET')]:
            with self.assertRaises(ValueError):v.finish((F(1),F(102,100)),width,status)

    def test_budget_and_checker_dependency_boundary(self):
        self.modules()
        from contract import Budget
        b=Budget();b.calls=8192
        with self.assertRaises(ValueError):b.tick(call=True)
        b=Budget();b.start-=181
        with self.assertRaises(ValueError):b.tick()
        import ast
        tree=ast.parse((Path(__file__).parent/'verify_coefficient.py').read_text())
        imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        imports += [a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names]
        self.assertNotIn('coefficient',imports)


@unittest.skipUnless((Path(__file__).parent/'RESULT.json').exists(),'frozen target not evaluated yet')
class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import verify_coefficient as v
        cls.v=v
        cls.c=v.strict_json((Path(__file__).parent/'RESULT.json').read_bytes())

    def test_complete_certificate(self):
        result=self.v.verify(self.c,self.c['source_commit'])
        self.assertEqual(result['verification'],'ACCEPT_BOUNDS_ONLY')
        self.assertEqual(result['outcome'],'TOLERANCE_MET')
        self.assertIs(result['scientific_acceptance'],False)

    def test_changed_l_source_pin_and_primitive_are_rejected(self):
        variants=[]
        for f in ('L','implementation','sources','moment','gamma'):
            c=copy.deepcopy(self.c)
            if f=='L':c['request']['L']='25/1'
            elif f=='implementation':c['implementation']['coefficient.py']='0'*64
            elif f=='sources':c['sources']['method_v2']='0'*64
            elif f=='moment':c['moment_certificate']['bounds']['mu2']=['0/1','0/1']
            else:c['gamma']['endpoints'][0]['levels'][0]=['0/1','0/1']
            variants.append(c)
        for c in variants:
            with self.assertRaises(ValueError):self.v.verify(c,self.c['source_commit'])

    def test_altered_sixth_power_constant_is_rejected(self):
        c=copy.deepcopy(self.c);c['sixth_bounds'][0]='0/1'
        with self.assertRaisesRegex(ValueError,'SIXTH_POWER'):self.v.verify(c,self.c['source_commit'])

    def test_altered_final_coefficient_is_rejected(self):
        c=copy.deepcopy(self.c);c['bounds'][0]='0/1'
        with self.assertRaisesRegex(ValueError,'FINAL_BOUND'):self.v.verify(c,self.c['source_commit'])


if __name__=='__main__':unittest.main()
