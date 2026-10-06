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


def selector_fixture(installed):
    selector = json.loads(baseline_bytes("SELECTOR_REGION.json"))
    if installed:
        proposal = PROPOSAL["selector_region_proposal"]
        for name, value in proposal["cells"].items():
            for region in proposal["regions"]:
                selector["selectors"][name][region] = value
        selector["covered_region_ids"] = proposal["resulting_covered_region_ids"]
        selector["open_region_ids"] = proposal["resulting_open_region_ids"]
    return selector


def nested_booleans(value, path=()):
    """Paths of every Boolean strictly below a node's top level (R-1 class)."""
    if isinstance(value, dict):
        for key, item in value.items():
            yield from nested_booleans(item, path + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from nested_booleans(item, path + (index,))
    elif isinstance(value, bool) and len(path) > 1:
        yield path


def set_path(record, path, value):
    for key in path[:-1]:
        record = record[key]
    record[path[-1]] = value


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

    def test_nested_boolean_cannot_be_number_or_string(self):
        # R-1 (Math-#250 5972612166, reproduced by Codex at 08f86862): a nested Boolean such as
        # review_basis[i].source_exposed must keep its exact type; 1 == True must not pass as the proposal.
        cases = [(node["id"], path, node) for node in PROPOSAL["proposed_graph_nodes"]
                 for path in nested_booleans({k: v for k, v in node.items() if k != "id"})]
        self.assertEqual(len(cases), 5)
        for nid, path, proposed in cases:
            current = proposed
            for key in path:
                current = current[key]
            substitutes = (1, 1.0, "true") if current is True else (0, 0.0, "false")
            for stage in ("open", "reviewed"):
                for value in substitutes:
                    with self.subTest(node=nid, path=path, stage=stage, value=value):
                        graph = graph_fixture(stage)
                        set_path(graph["nodes"][nid], path, value)
                        self.assertEqual(state(graph), "partial")
                        set_path(graph["nodes"][nid], path, current)
                        self.assertEqual(state(graph), "installed")

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
        return self.run_text(json.dumps(graph), json.dumps(selector_fixture(installed_selector)))

    def run_text(self, graph_text, selector_text):
        (self.root / witness.GRAPH).write_text(graph_text)
        (self.root / witness.SELECTOR).write_text(selector_text)
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

    def test_nested_integer_boolean_is_rejected_by_full_checker(self):
        for stage in ("open", "reviewed"):
            with self.subTest(stage=stage):
                graph = graph_fixture(stage)
                graph["nodes"]["math.c6-component.palm-proof"]["review_basis"][0]["source_exposed"] = 1
                run, result = self.run_graph(graph)
                self.assertEqual(run.returncode, 1)
                self.assertFalse(result["checks"]["TRANSITIONS"])
                self.assertFalse(result["passed"])
                self.assertNotEqual(run.stdout, (PACKET / "RESULTS_INSTALLED.json").read_bytes())


    def test_duplicate_keys_and_non_finite_constants_are_rejected_by_full_checker(self):
        # R-2: a loose parse keeps the last duplicate and accepts NaN/Infinity, so each text below would reach the
        # pinned installed output. The checker must refuse the input instead.
        graph = json.dumps(graph_fixture("open"))
        selector = json.dumps(selector_fixture(True))
        node = '"%s": {' % witness.WITNESS
        self.assertEqual(graph.count(node), 1)
        self.assertTrue(selector.startswith("{"))
        cases = {
            "duplicate GRAPH key": (graph.replace(node, node + '"classification": "REFUTED", ', 1), selector,
                                    "duplicate JSON key"),
            "duplicate SELECTOR key": (graph, selector.replace("{", '{"regions": [], ', 1), "duplicate JSON key"),
            "NaN in GRAPH": (graph.replace(node, node + '"note": NaN, ', 1), selector, "non-finite"),
            "-Infinity in GRAPH": (graph.replace(node, node + '"note": -Infinity, ', 1), selector, "non-finite"),
            "Infinity in SELECTOR": (graph, selector.replace("{", '{"note": Infinity, ', 1), "non-finite"),
        }
        for name, (graph_text, selector_text, reason) in cases.items():
            with self.subTest(case=name):
                run, result = self.run_text(graph_text, selector_text)
                self.assertEqual(run.returncode, 1)
                self.assertFalse(result["passed"])
                self.assertIn(reason, result["input_error"])
                self.assertNotEqual(run.stdout, (PACKET / "RESULTS_INSTALLED.json").read_bytes())
        run, result = self.run_text(graph, selector)
        self.assertEqual((run.returncode, run.stdout), (0, (PACKET / "RESULTS_INSTALLED.json").read_bytes()))

    def test_every_json_input_goes_through_the_strict_loader(self):
        # GRAPH is read in several checks; one strict read is enough to refuse the run, so the full-CLI cases above
        # cannot see a single loose call site. This guard keeps json.loads inside load_json only.
        source = ENTRY.read_text(encoding="utf-8")
        self.assertEqual(source.count("json.loads("), 1)
        self.assertIn("object_pairs_hook=pairs, parse_constant=constant)", source)


class SiblingProposals(unittest.TestCase):
    """Math-#167 and Math-#173 compare proposed fields with plain equality. That is exact today only because every
    Boolean they compare on a live node is a top-level controlling flag, which the hard gate types exactly. Fail if a
    nested or other compared Boolean is ever proposed there, so R-1 cannot reappear unnoticed."""

    META = ("id", "create_if_absent", "cross_record")

    def test_compared_booleans_are_top_level_controlling_only(self):
        for record in ("reviews/register_alignment_20260930", "reviews/c6_residual_closure_20260930"):
            data = json.loads((ROOT / record / "PROPOSED_TRANSITIONS.json").read_text())
            fields = [{k: v for k, v in n.items() if k not in self.META} for n in data["proposed_graph_nodes"]]
            fields += [t["proposed"] for t in data["transitions"] if isinstance(t.get("proposed"), dict)]
            self.assertTrue(fields)
            for compared in fields:
                with self.subTest(record=record, node=compared.get("source") or compared.get("kind")):
                    self.assertEqual(list(nested_booleans(compared)), [])
                    self.assertEqual({k for k, v in compared.items() if isinstance(v, bool)} - {"controlling"}, set())


if __name__ == "__main__":
    unittest.main()
