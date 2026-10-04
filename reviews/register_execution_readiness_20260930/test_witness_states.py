"""Bounded witness-state regressions; fixtures never modify the live register."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "reviews/c6_witness_collision_reconciliation_20260929"
ENTRY = PACKET / "reconciliation_check.py"
SPEC = importlib.util.spec_from_file_location("witness_checker", ENTRY)
witness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(witness)
PROPOSAL = json.loads((PACKET / "PROPOSED_TRANSITIONS.json").read_text())
BASELINE = Path(__file__).with_name("fixtures") / "witness_baseline"
BASELINE_SOURCES = json.loads((BASELINE / "SOURCE.json").read_text())
HISTORICAL_EDGE = {
    "from": "math.rn-region.witness-collision",
    "to": "math.d5-component.offpin-second-moment-review",
    "required": True,
    "relation": "requires_evidence",
}


def edge_fields(edge):
    return {key: edge[key] for key in ("from", "to", "required", "relation")}


def baseline_bytes(name):
    """Historical test inputs stay independent of the live register's execution state."""
    data = (BASELINE / name).read_bytes()
    identity = BASELINE_SOURCES["files"][name]
    if len(data) != identity["bytes"] or hashlib.sha256(data).hexdigest() != identity["sha256"]:
        raise ValueError("historical witness fixture identity mismatch: " + name)
    return data


def graph_fixture(stage):
    """Compose normative JSON directly, without the checker's state/build helpers."""
    graph = json.loads(baseline_bytes("GRAPH.json"))
    if stage != "baseline":
        for node in PROPOSAL["proposed_graph_nodes"]:
            graph["nodes"][node["id"]] = {k: copy.deepcopy(v) for k, v in node.items() if k != "id"}
        graph["edges"] += [edge_fields(e) for e in PROPOSAL["proposed_graph_edges"]
                           if stage == "reviewed" or e["from"] != witness.WITNESS]
        if stage == "reviewed":
            graph["nodes"][witness.WITNESS]["classification"] = "PROVED_REVIEWED"
    return graph


def state(graph):
    return witness.installed_state(graph, PROPOSAL["proposed_graph_nodes"],
                                   PROPOSAL["proposed_graph_edges"])["state"]


class WitnessStates(unittest.TestCase):
    def test_baseline_and_both_documented_installed_states(self):
        for stage, expected in (("baseline", "baseline"), ("open", "installed"), ("reviewed", "installed")):
            with self.subTest(stage=stage):
                self.assertEqual(state(graph_fixture(stage)), expected)

    def test_historical_offpin_edge_is_preserved(self):
        for stage in ("baseline", "open", "reviewed"):
            with self.subTest(stage=stage):
                graph = graph_fixture(stage)
                self.assertIn(HISTORICAL_EDGE, graph["edges"])
                self.assertEqual(state(graph), "baseline" if stage == "baseline" else "installed")

    def test_old_witness_must_remain_literal_noncontrolling(self):
        for stage in ("baseline", "open", "reviewed"):
            for value in (True, 0, None):
                with self.subTest(stage=stage, value=value):
                    graph = graph_fixture(stage)
                    graph["nodes"][witness.WITNESS]["controlling"] = value
                    self.assertEqual(state(graph), "partial")

    def test_component_boolean_cannot_be_integer_zero(self):
        for node in PROPOSAL["proposed_graph_nodes"]:
            if node.get("controlling") is False:
                with self.subTest(node=node["id"]):
                    graph = graph_fixture("open")
                    graph["nodes"][node["id"]]["controlling"] = 0
                    self.assertEqual(state(graph), "partial")

    def test_malformed_proposal_edge_is_not_absent_or_exact(self):
        # Even an extra malformed parallel edge must not disappear in set intersection.
        for proposed in PROPOSAL["proposed_graph_edges"]:
            for field, value in (("required", not proposed["required"]),
                                 ("required", int(proposed["required"])),
                                 ("relation", "unrecognized_relation")):
                wrong = edge_fields(proposed)
                wrong[field] = value
                if wrong == HISTORICAL_EDGE and type(wrong["required"]) is bool:
                    continue
                for stage in ("open", "reviewed"):
                    with self.subTest(stage=stage, source=proposed["from"], target=proposed["to"],
                                      field=field, value=value):
                        graph = graph_fixture(stage)
                        graph["edges"].append(wrong)
                        self.assertEqual(state(graph), "partial")

    def test_each_witness_edge_is_partial_while_open_or_missing_after_review(self):
        for proposed in PROPOSAL["proposed_graph_edges"]:
            if proposed["from"] != witness.WITNESS:
                continue
            with self.subTest(target=proposed["to"]):
                edge = edge_fields(proposed)
                graph = graph_fixture("open")
                graph["edges"].append(edge)
                self.assertEqual(state(graph), "partial")
                graph = graph_fixture("reviewed")
                graph["edges"].remove(edge)
                self.assertEqual(state(graph), "partial")

    def test_selector_cannot_run_ahead_of_graph(self):
        self.assertFalse(witness.selector_state_ok(True, "baseline"))
        self.assertFalse(witness.selector_state_ok(True, "partial"))
        self.assertTrue(witness.selector_state_ok(False, "baseline"))
        self.assertTrue(witness.selector_state_ok(True, "installed"))


class WitnessCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        needed = set(witness.INVENTORY) | {
            witness.HERE + "/PROPOSED_TRANSITIONS.json",
            witness.HERE + "/RECONCILIATION.md", witness.D5_TRANSITIONS, "PROOF_INDEX.md", witness.CATALOG,
        }
        for relative in needed:
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        for relative, name in ((witness.GRAPH, "GRAPH.json"), (witness.SELECTOR, "SELECTOR_REGION.json")):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(baseline_bytes(name))

    def run_graph(self, graph, installed_selector=True):
        (self.root / witness.GRAPH).write_text(json.dumps(graph))
        selector = json.loads(baseline_bytes("SELECTOR_REGION.json"))
        if installed_selector:
            proposal = PROPOSAL["selector_region_proposal"]
            for name, value in proposal["cells"].items():
                for region in proposal["regions"]:
                    selector["selectors"][name][region] = value
            selector["covered_region_ids"] = proposal["resulting_covered_region_ids"]
            selector["open_region_ids"] = proposal["resulting_open_region_ids"]
        (self.root / witness.SELECTOR).write_text(json.dumps(selector))
        flags = ["-O"] if sys.flags.optimize else []
        run = subprocess.run([sys.executable, "-B", *flags, "-S", str(ENTRY)], cwd=self.root,
                             capture_output=True, timeout=60)
        self.assertEqual(run.stderr, b"")
        return run, json.loads(run.stdout)

    def test_accepted_states_keep_exact_pinned_outputs(self):
        for stage, filename in (("baseline", "RESULTS.json"), ("open", "RESULTS_INSTALLED.json"),
                                ("reviewed", "RESULTS_INSTALLED.json")):
            with self.subTest(stage=stage):
                run, result = self.run_graph(graph_fixture(stage), stage != "baseline")
                self.assertEqual(run.returncode, 0)
                self.assertTrue(result["passed"])
                self.assertEqual(run.stdout, (PACKET / filename).read_bytes())

    def test_wrong_required_edge_is_rejected_by_full_checker(self):
        graph = graph_fixture("open")
        graph["edges"].append({"from": witness.WITNESS,
                               "to": "math.c6-witness-collision-factorial-moment",
                               "required": False, "relation": "requires_evidence"})
        run, result = self.run_graph(graph)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(result["checks"]["TRANSITIONS"])
        self.assertFalse(result["passed"])

    def test_controlling_witness_is_rejected_by_full_checker(self):
        graph = graph_fixture("reviewed")
        graph["nodes"][witness.WITNESS]["controlling"] = True
        run, result = self.run_graph(graph)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(result["checks"]["OBLIGATION"])
        self.assertFalse(result["passed"])

    def test_integer_controlling_component_is_rejected_by_full_checker(self):
        graph = graph_fixture("open")
        graph["nodes"]["math.c6-witness-collision-factorial-moment"]["controlling"] = 0
        run, result = self.run_graph(graph)
        self.assertEqual(run.returncode, 1)
        self.assertFalse(result["checks"]["TRANSITIONS"])
        self.assertFalse(result["passed"])


if __name__ == "__main__":
    unittest.main()
