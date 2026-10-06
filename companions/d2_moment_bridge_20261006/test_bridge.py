"""Exact finite-law and protocol controls, not substitutes for arbitrary-law Lean proofs."""
from fractions import Fraction as F
import importlib.util
import itertools
import json
from pathlib import Path
import re
import unittest
import subprocess
import tempfile
import hashlib
import os

SIDE = Path(__file__).resolve().parent
THEOREMS = '''residual_sq_expand residual_sq_integrable residual_integral_eq_delta delta_nonneg delta_eq_zero_iff_residual cubicResidual_eq_zero_iff delta_eq_zero_iff_support delta_pos_iff_not_support property_of_ae_of_atom moment_two_pos_of_atom delta_pos_of_two_atoms square_gap_integrable square_gap_integral fourth_gt_second_sq_of_two_atoms tau_pos_of_two_atoms zero_atom_counterexample'''.split()
DEFINITIONS = ['moment', 'cubicResidual']


def moments(law):
    return [sum(p*x**k for x,p in law) for k in (2,4,6)]


def laws():
    # Zero plus two possible radii, including absent and equal-radius atoms.
    for a,b,z,u,v in itertools.product((F(1,2),F(1),F(2)),(F(1),F(2),F(3)),range(3),range(3),range(3)):
        if u+v == 0:
            continue
        total=z+u+v
        yield [(F(0),F(z,total)),(a,F(u,2*total)),(-a,F(u,2*total)),
               (b,F(v,2*total)),(-b,F(v,2*total))]


class BridgeTests(unittest.TestCase):
    def test_source_exists_and_no_admission(self):
        self.assertTrue((SIDE/'D2MomentBridge.lean').is_file(), 'new Lean module missing')
        text=(SIDE/'D2MomentBridge.lean').read_text()
        code=re.sub(r'/\-.*?\-/', '', text, flags=re.S)
        for token in ('sorry','admit','axiom','unsafe','native_decide'):
            self.assertIsNone(re.search(r'\b'+token+r'\b',code), token)
        self.assertIn('import ResearchFormalCoreR1.D2Schur', text)
        self.assertIn('Integrable (fun w => X w ^ 6) μ', text)

    def test_exact_declared_inventory(self):
        self.assertTrue((SIDE/'SOURCE_FILES.json').is_file(), 'new inventory missing')
        meta=json.loads((SIDE/'SOURCE_FILES.json').read_text())
        text=(SIDE/'D2MomentBridge.lean').read_text()
        self.assertEqual(re.findall(r'^theorem (\w+)',text,re.M),THEOREMS)
        self.assertEqual(re.findall(r'^(?:noncomputable )?def (\w+)',text,re.M),DEFINITIONS)
        self.assertEqual(meta['theorems'],THEOREMS)
        self.assertEqual(meta['definitions'],DEFINITIONS)
        self.assertEqual(meta['scientific_effect'],'NONE')
        self.assertEqual(meta['core_tree'],'d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14')

    def test_residual_identity_and_exact_equality_class(self):
        count=0
        for law in laws():
            m2,m4,m6=moments(law); c=m4/m2; delta=m6-m4*m4/m2
            residual=sum(p*(x**3-c*x)**2 for x,p in law)
            self.assertEqual(delta,residual)
            self.assertGreaterEqual(delta,0)
            one_nonzero_radius=all(x==0 or x*x==c for x,p in law if p>0)
            self.assertEqual(delta==0,one_nonzero_radius)
            count+=1
        self.assertEqual(count,216)

    def test_two_nonzero_distinct_squared_atoms(self):
        strict=0
        for law in laws():
            xs=[x for x,p in law if p>0 and x!=0]
            if any(a*a!=b*b for a,b in itertools.combinations(xs,2)):
                m2,m4,m6=moments(law)
                self.assertGreater(m2,0)
                self.assertGreater(m4,m2*m2)
                self.assertGreater(m6-m4*m4/m2,0)
                for q in (F(0),F(1,16),F(1,8),F(1,4)):
                    delta=m6-m4*m4/m2
                    tau=(1-4*q)*delta+q*(delta+9*m2*(m4-m2*m2))
                    self.assertGreater(tau,0)
                strict+=1
        self.assertGreater(strict,0)

    def test_zero_atom_and_same_radius_countermodels(self):
        law=[(F(0),F(1,2)),(F(1),F(1,4)),(F(-1),F(1,4))]
        m2,m4,m6=moments(law)
        self.assertGreater(m4,m2*m2)
        self.assertEqual(m6-m4*m4/m2,0)
        a,b=F(1),F(-1)
        self.assertNotEqual(a,b)
        self.assertEqual(a*a,b*b)
        self.assertEqual(moments([(a,F(1,2)),(b,F(1,2))]),[1,1,1])

    def test_fourth_gap_needs_probability_normalization(self):
        # Mass2 is NOT probability: raw fourth gap can be negative.
        m2,m4,_=moments([(F(1),F(2))])
        self.assertLess(m4-m2*m2,0)
        for law in laws():
            m2,m4,_=moments(law)
            self.assertEqual(sum(p*(x*x-m2)**2 for x,p in law),m4-m2*m2)

    def test_residual_factorization(self):
        for x,c in itertools.product([F(i,3) for i in range(-9,10)], [F(i,4) for i in range(-8,9)]):
            self.assertEqual((x**3-c*x)**2,x**6-2*c*x**4+c*c*x*x)
            self.assertEqual(x**3-c*x==0,x==0 or x*x==c)

    def checker(self):
        self.assertTrue((SIDE/'check.py').is_file(),'evidence checker missing')
        spec=importlib.util.spec_from_file_location('moment_checker',SIDE/'check.py')
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        return m

    def test_negative_control_accepts_only_intended_false(self):
        m=self.checker()
        text='/tmp/evidence/RejectZeroAtom.lean:4:2: error: unsolved goals\n⊢ False\n'
        self.assertEqual(m.negative(text,'RejectZeroAtom',1),'RejectZeroAtom')
        for bad,status in [(text,0),(text,2),(text.replace('False','True'),1),
                           (text.replace('RejectZeroAtom','Other'),1),
                           (text+'error: unknown identifier\n',1),
                           ('Traceback: bad runtime\n',1),('error: unsolved goals\n',1)]:
            with self.subTest(bad=bad,status=status), self.assertRaises(ValueError):
                m.negative(bad,'RejectZeroAtom',status)
        with self.assertRaises(ValueError):m.negative(text,'Unknown',1)

    def test_final_command_does_not_hash_a_live_tee_output(self):
        # Execute the actual final shell invocation against a synthetic snapshot writer.
        # A live tee destination must not change after the receipt hashes that directory.
        command=next(line for line in (SIDE/'replay.sh').read_text().splitlines()
                     if 'check.py" finish' in line)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); out=root/'evidence'; out.mkdir()
            (root/'check.py').write_text("import pathlib,json,hashlib,time,sys\n"
                "out=pathlib.Path(sys.argv[-1]);time.sleep(0.05)\n"
                "r={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()}\n"
                "(out/'receipt.json').write_text(json.dumps(r))\nprint('completed synthetic fixture')\n")
            run=subprocess.run(['bash','-c','set -euo pipefail\n'+command],
                capture_output=True,env={**os.environ,'SIDE':str(root),'OUT':str(out)})
            self.assertEqual(run.returncode,0,run.stderr)
            recorded=json.loads((out/'receipt.json').read_text())
            for name,digest in recorded.items():
                self.assertEqual(hashlib.sha256((out/name).read_bytes()).hexdigest(),digest,
                                 'receipt hashed an output that was still being written')

    def test_type_inventory_missing_duplicate_unrecognized(self):
        m=self.checker(); names=['D2MomentBridge.a','D2MomentBridge.b']
        self.assertEqual(m.types('D2MomentBridge.a : True\nD2MomentBridge.b : False\n',names),names)
        for bad in ('D2MomentBridge.a : True\n','D2MomentBridge.a : True\nD2MomentBridge.a : True\n',
                    'error: crash\nD2MomentBridge.a : True\nD2MomentBridge.b : False\n'):
            with self.assertRaises(ValueError):m.types(bad,names)


if __name__=='__main__':
    unittest.main(verbosity=2)
