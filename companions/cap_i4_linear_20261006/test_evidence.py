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

 # Extract the actual nested helper unchanged; this tests process plumbing, not Lean.
 def process_helper(self, directory, runner):
  import ast, json, os, subprocess
  from types import SimpleNamespace
  tree=ast.parse((HERE/'replay.py').read_text())
  main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
  helper=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
  scope={'root':directory,'out':directory,'records':[],'env':os.environ.copy(),
         'sha':self.m.sha,'json':json,
         'subprocess':SimpleNamespace(run=runner,TimeoutExpired=subprocess.TimeoutExpired)}
  exec(compile(ast.Module(body=[helper],type_ignores=[]),'replay.py::execute','exec'),scope)
  return scope['execute'],scope['records']
 def test_checker_budget_and_real_child_receipts(self):
  import json, subprocess, sys, tempfile
  budgets=[]
  def observed(*args,**kwargs):
   budgets.append(kwargs['timeout'])
   return subprocess.run(*args,**kwargs)
  with tempfile.TemporaryDirectory() as td:
   directory=Path(td);execute,records=self.process_helper(directory,observed)
   self.assertEqual(execute('build',[sys.executable,'-c','print(17)']),'17\n')
   self.assertEqual(execute('leanchecker',[sys.executable,'-c','print(19)']),'19\n')
   self.assertEqual(budgets,[300,900])
   self.assertEqual([r['exit'] for r in records],[0,0])
   self.assertEqual(json.loads((directory/'processes.json').read_text()),records)
   for row in records:
    self.assertEqual(self.m.sha((directory/(row['label']+'.log')).read_bytes()),row['log_sha256'])
 def test_checker_timeout_retains_partial_not_completion(self):
  import subprocess, tempfile
  budgets=[]
  def timed_out(cmd,**kwargs):
   budgets.append(kwargs['timeout'])
   raise subprocess.TimeoutExpired(cmd,kwargs['timeout'],output=b'partial-out\n',stderr=b'partial-err\n')
  with tempfile.TemporaryDirectory() as td:
   directory=Path(td);execute,records=self.process_helper(directory,timed_out)
   with self.assertRaises(subprocess.TimeoutExpired):
    execute('leanchecker',['leanchecker','--fresh','CapI4Linear'])
   self.assertEqual((directory/'leanchecker.log').read_bytes(),b'partial-out\npartial-err\n')
   self.assertEqual(records,[])
   self.assertFalse((directory/'processes.json').exists())
   self.assertFalse((directory/'verdict.json').exists())
   self.assertEqual(budgets,[900])
 def test_nonzero_child_is_still_failure(self):
  import contextlib, io, subprocess, sys, tempfile
  with tempfile.TemporaryDirectory() as td:
   directory=Path(td);execute,records=self.process_helper(directory,subprocess.run)
   with contextlib.redirect_stdout(io.StringIO()),self.assertRaisesRegex(ValueError,'build exit 7'):
    execute('build',[sys.executable,'-c','print("intentional-failure");raise SystemExit(7)'])
   self.assertEqual([r['exit'] for r in records],[7])
   self.assertFalse((directory/'verdict.json').exists())
if __name__=='__main__':unittest.main(verbosity=2)
