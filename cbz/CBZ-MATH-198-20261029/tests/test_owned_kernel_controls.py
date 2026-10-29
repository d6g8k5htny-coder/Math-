"""Exact rejection reasons, not arbitrary compiler failure, determine native controls."""
import importlib.util
from pathlib import Path
import sys
import unittest

TOOLS=Path(__file__).resolve().parents[1]/"tools"
sys.path.insert(0,str(TOOLS))
import owned_kernel_audit as audit
import owned_kernel_controls as controls


class NativeControlProtocolTests(unittest.TestCase):
    def receipt(self,returncode=1):
        return {"returncode":returncode,"succeeded":returncode==0,"timed_out":False,
                "output_limit_exceeded":False,"failure":None}

    def test_exact_rejection_not_timeout_signal_bool_or_unrelated_error(self):
        for kind,reason in controls.REASONS.items():
            self.assertTrue(controls.validate_rejection(self.receipt(),"error: "+reason,kind)["observed"])
            for receipt,text in [(self.receipt(0),"OWN_CONTROL_ESCAPED|"+kind),
                                 (self.receipt(-9),reason),(self.receipt(False),reason),
                                 (dict(self.receipt(),timed_out=True),reason),
                                 (self.receipt(),"error: syntax invalid")]:
                with self.subTest(kind=kind,receipt=receipt),self.assertRaises(ValueError):controls.validate_rejection(receipt,text,kind)

    def test_insertion_mutant_must_escape_original_rejection_control(self):
        result=controls.validate_mutant_escape(self.receipt(0),"OWN_CONTROL_ESCAPED|universe\n")
        self.assertTrue(result["mutation_killed"])
        with self.assertRaises(ValueError):controls.validate_mutant_escape(self.receipt(),"OWN_REJECT_DECLARATION")
        with self.assertRaises(ValueError):controls.validate_mutant_escape(self.receipt(0),"")

    def test_reason_in_path_or_unrelated_diagnostic_cannot_impersonate_rejection(self):
        for kind,reason in controls.REASONS.items():
            actual="/tmp/Control.lean:3:0: error: "+reason
            self.assertTrue(controls.validate_rejection(self.receipt(),actual,kind)["observed"])
            for text in ("/tmp/"+reason+"/Control.lean:3:0: error: unexpected identifier",
                         "error: unexpected identifier near "+reason,
                         "source literal contains "+reason):
                with self.subTest(kind=kind,text=text),self.assertRaises(ValueError):
                    controls.validate_rejection(self.receipt(),text,kind)

    def test_native_graph_control_requires_all_emitted_nodes_and_actual_cycle(self):
        for kind in ("self_cycle","mutual_cycle"):
            _,names=controls.render_graph_control(kind)
            encoded=[audit.dotted_name(x)for x in names]
            deps=[encoded[0]]if len(encoded)==1 else [encoded[1],encoded[0]]
            text="".join("OWN_GRAPH_NODE|"+name+"|"+dep+"\n"for name,dep in zip(encoded,deps))+"OWN_GRAPH_COMPLETE|"+str(len(names))+"\n"
            self.assertTrue(controls.validate_graph_control(text,kind,audit.dotted_name,audit.assert_acyclic_bodies)["dependency_cycle_rejected"])
            without_edges="".join("OWN_GRAPH_NODE|"+name+"|\n"for name in encoded)+"OWN_GRAPH_COMPLETE|"+str(len(names))+"\n"
            with self.assertRaises(ValueError):controls.validate_graph_control(without_edges,kind,audit.dotted_name,audit.assert_acyclic_bodies)


if __name__=="__main__":unittest.main()
