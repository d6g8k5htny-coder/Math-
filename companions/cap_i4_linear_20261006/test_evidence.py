"""Synthetic evidence tests; no synthetic result is a hosted Lean receipt."""
import importlib.util
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
class EvidenceTests(unittest.TestCase):
 def setUp(self):
  p=HERE/'replay.py';self.assertTrue(p.is_file(),'missing replay implementation')
  spec=importlib.util.spec_from_file_location('linear_replay',p)
  self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def test_axioms_valid(self):
  self.m.axioms("'CapI4Linear.a' depends on axioms: [propext]\n",['CapI4Linear.a'])
 def test_axioms_unmatched(self):
  good="'CapI4Linear.a' depends on axioms: [propext]\n"
  for suffix in ['error: bad\n',"'Foreign' depends on axioms: [sorryAx]\n"]:
   with self.assertRaises(ValueError):self.m.axioms(good+suffix,['CapI4Linear.a'])
 def test_axioms_forbidden_missing_duplicate(self):
  for text in ["'CapI4Linear.a' depends on axioms: [sorryAx]\n",'']:
   with self.assertRaises(ValueError):self.m.axioms(text,['CapI4Linear.a'])
  with self.assertRaises(ValueError):self.m.axioms("'CapI4Linear.a' does not depend on any axioms\n"*2,['CapI4Linear.a'])
 def test_negative_valid(self):
  self.m.negative('/tmp/test.lean:4:2: error: unsolved goals\n⊢ False\n',1)
 def test_negative_unrelated(self):
  for text,status in [('error: unknown identifier\n⊢ False\n',1),('error: unsolved goals\n⊢ True\n',1),('error: unsolved goals\n⊢ False\n',2),('',0)]:
   with self.assertRaises(ValueError):self.m.negative(text,status)
 def test_duplicate_json(self):
  with self.assertRaises(ValueError):self.m.strict_json('{"a":1,"a":2}')
 def test_types(self):
  self.m.types('@CapI4Linear.a : ℝ\n@CapI4Linear.b.{u,\n v} : ℝ\n',['CapI4Linear.a','CapI4Linear.b'])
  for text in ['foreign text\nCapI4Linear.a : ℝ\n','CapI4Linear.a : ℝ\nerror: bad\n','CapI4Linear.a : ℝ\nForeign.a : ℝ\n']:
   with self.assertRaises(ValueError):self.m.types(text,['CapI4Linear.a'])
if __name__=='__main__':unittest.main(verbosity=2)
