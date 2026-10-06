"""Evidence-parser controls; synthetic logs never count as Lean execution."""
import importlib.util
import ast
from pathlib import Path
import unittest
HERE=Path(__file__).resolve().parent
class EvidenceChecks(unittest.TestCase):
    def setUp(self):
        path=HERE/'check_evidence.py'
        self.assertTrue(path.exists(),'missing evidence validator implementation')
        spec=importlib.util.spec_from_file_location('polar_validator',path)
        self.mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(self.mod)
        self.names=['CapI4Polar.a','CapI4Polar.b']
        self.good="'CapI4Polar.a' depends on axioms: [propext, Classical.choice, Quot.sound]\n'CapI4Polar.b' does not depend on any axioms\n"
    def test_valid(self):
        self.mod.audit_axioms(self.good,self.names)
        # The genuine third hosted attempt found an ambiguous `spectrum`
        # in a generated simp list. Check the actual emitted literal sources.
        tree=ast.parse((HERE/'check_evidence.py').read_text())
        probes=[node.value for node in ast.walk(tree) if isinstance(node,ast.Constant)
                and isinstance(node.value,str) and 'example' in node.value]
        self.assertEqual(len(probes),3)
        for text in probes:
            self.assertNotRegex(text,r'(?<![.\w])(?:spectrum|radius|eigenvalues)\b')
    def test_foreign_text(self):
        for bad in ['error: import failed\n','unrelated\n',"'foreign' depends on axioms: [sorryAx]\n"]:
            with self.assertRaises(ValueError): self.mod.audit_axioms(self.good+bad,self.names)
    def test_missing_duplicate_and_forbidden(self):
        for bad in [self.good.splitlines()[0],self.good+self.good,self.good.replace('propext','sorryAx'),self.good.replace('Classical.choice','MyAxiom')]:
            with self.assertRaises(ValueError): self.mod.audit_axioms(bad,self.names)
    def test_universe_wrapped_type_headers(self):
        text='@CapI4Polar.a : ℝ → ℝ\n@CapI4Polar.b.{u_1,\n u_2} : ℝ\n'
        self.mod.audit_types(text,self.names)
    def test_types_fail(self):
        for bad in ['','CapI4Polar.a : ℝ\n','CapI4Polar.a : ℝ\nCapI4Polar.b : ℝ\nerror: bad\n']:
            with self.assertRaises(ValueError): self.mod.audit_types(bad,self.names)
    def test_intended_false_goal(self):
        self.mod.audit_negative('/tmp/RejectOrder.lean:4:2: error: unsolved goals\n⊢ False\n',1)
    def test_wrong_negative_exit_or_reason(self):
        for text,status in [('',0),('timeout',1),('error: unknown identifier\n⊢ False\n',1),('error: unsolved goals\n⊢ True\n',1),('error: unsolved goals\n⊢ False\n',2)]:
            with self.assertRaises(ValueError): self.mod.audit_negative(text,status)
if __name__=='__main__': unittest.main(verbosity=2)
