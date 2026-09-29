#!/usr/bin/env python3
"""Fail-closed checks for the D5 graph/proof-index/C6 catalog fold."""
import copy
import json
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[2]
GRAPH=ROOT/"frontiers/downstream_gate_20260925/GRAPH.json"
PROP=ROOT/"reviews/d5_reconciliation_20260929/PROPOSED_TRANSITIONS.json"
INDEX=ROOT/"PROOF_INDEX.md"
CAND=ROOT/"reviews/candidates_pending_20260928/CANDIDATES.md"

def load(path):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise ValueError("duplicate JSON key: "+k)
            out[k]=v
        return out
    return json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite JSON: "+x)))

def realized(graph,proposal):
    nodes=graph["nodes"]; edges=graph["edges"]
    if len({(e["from"],e["to"],e.get("relation")) for e in edges})!=len(edges): return False
    for n in proposal["proposed_graph_nodes"]:
        actual=nodes.get(n["id"])
        if actual is None: return False
        for k,v in n.items():
            if k!="id" and actual.get(k)!=v: return False
    have={(e["from"],e["to"],e.get("relation"),e.get("required")) for e in edges}
    for e in proposal["proposed_graph_edges"]:
        if (e["from"],e["to"],e.get("relation"),True) not in have: return False
    for tr in proposal["graph"]:
        if nodes.get(tr["node"],{}).get("classification")!=tr["proposed"]: return False
    return nodes["math.rn-region.witness-collision"]["classification"]=="OPEN_ACTIVE"

class FoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g=load(GRAPH); cls.p=load(PROP)
        cls.index=INDEX.read_text(encoding="utf-8")
        cls.cand=CAND.read_text(encoding="utf-8")
    def test_proposal_realized(self): self.assertTrue(realized(self.g,self.p))
    def test_missing_node_rejected(self):
        g=copy.deepcopy(self.g);g["nodes"].pop("math.d5-component.collar-proof")
        self.assertFalse(realized(g,self.p))
    def test_stale_fingerprint_rejected(self):
        g=copy.deepcopy(self.g);g["nodes"]["math.d5-component.punctured-pin-proof"]["fingerprint"]="0"*64
        self.assertFalse(realized(g,self.p))
    def test_missing_edge_rejected(self):
        g=copy.deepcopy(self.g);g["edges"]=[e for e in g["edges"] if not (e["from"]=="math.d5-pin-neighborhood-first-moment" and e["to"]=="math.d5-component.collar-proof")]
        self.assertFalse(realized(g,self.p))
    def test_witness_closure_rejected(self):
        g=copy.deepcopy(self.g);g["nodes"]["math.rn-region.witness-collision"]["classification"]="PROVED_REVIEWED"
        self.assertFalse(realized(g,self.p))
    def test_index_scope_and_open_boundary(self):
        self.assertIn("D5 planar pin/collar/intermediate first moment",self.index)
        self.assertIn("C6 planar Fourier upper bound",self.index)
        self.assertIn("C6 sharp Palm route",self.index)
        self.assertIn("NO COMPLETE REGIONAL PROOF YET",self.index)
        self.assertIn("`math.rn-region.witness-collision` remains `OPEN_ACTIVE`",self.index)
        self.assertNotIn("the claimed summed pin-neighborhood bound remains AMEND",self.index)
    def test_catalog_records_only_reviewed_bound(self):
        sec=self.cand.split("## C6.",1)[1].split("\n## C7.",1)[0]
        self.assertIn("r^3 log(1/r)",sec)
        self.assertIn("E[N(N-1)]=Theta(r^3)",sec)
        self.assertRegex(sec,r"They do\s+not close the regional shrinking-witness mechanism")
        self.assertIn("`math.rn-region.witness-collision` remains `OPEN_ACTIVE`",sec)
        self.assertNotIn("No global factorial upper bound",sec)
    def test_later_packets_are_separate_from_open_regional_mechanism(self):
        for source in (
            "frontiers/d5_dimension_lift_20260929/PROOF.md",
            "frontiers/c6_palm_route_20260929/PROOF.md",
            "frontiers/c6_rare_cluster_laws_20260929/PROOF.md",
        ):
            self.assertIn(source,self.index)
        sec=self.cand.split("## C6.",1)[1].split("\n## C7.",1)[0]
        self.assertIn("separate reviewed/merged packets",sec)
        self.assertRegex(sec,r"They do\s+not close the regional shrinking-witness mechanism")
        heading=self.cand.split("## C6.",1)[1].splitlines()[0]
        self.assertNotIn("sharp order open",heading)
    def test_declarative_source_preserved(self):
        self.assertIs(self.p["declarative"],True)
        self.assertIs(self.p["executed"],False)

if __name__=="__main__":
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FoldTests))
    raise SystemExit(0 if result.wasSuccessful() else 1)
