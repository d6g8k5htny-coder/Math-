"""Bounded C8 quarantine controls; integrity success never grants admission."""
from fractions import Fraction as F
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_c8_quarantine.py"
PACKET = "frontiers/c8_elder_failure_coefficient_20261001"
QID = "Q-C8-ELDER-FAILURE-BINARY64-20261029"
RECORD = "quarantine/" + QID + ".json"
EXACT = {"k=0.5": "199/9", "k=1": "1355/36", "k=2": "20957/288"}
CLI_HEALTH = []


def observe_cli(child):
    """Independent child health before semantic assertions; no crashed CLI is a kill."""
    errors = []
    if child.returncode not in (0, 1, 2):errors.append("unexpected exit")
    if child.stderr:errors.append("unexpected stderr")
    def unique(items):
        value = {}
        for key, item in items:
            if key in value:raise ValueError("duplicate JSON member")
            value[key] = item
        return value
    try:
        doc = json.loads(child.stdout, object_pairs_hook=unique,
                         parse_constant=lambda v: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
        valid = (isinstance(doc, dict) and doc.get("status") in {"QUARANTINE_INTEGRITY_OK", "REFUSED", "NOT_COVERED"}
                 and type(doc.get("cbz_certificate_admitted")) is bool
                 and isinstance(doc.get("scientific_effect"), str)
                 and all(isinstance(doc.get(k), str) and doc[k] for k in ("quarantine_id", "scope", "layer_a_status"))
                 and all(type(doc.get(k)) is int and doc[k] >= 0
                         for k in ("preserved_packet_files", "denied_output_count", "exact_exception_count"))
                 and isinstance(doc.get("problems"), list) and all(isinstance(v, str) for v in doc["problems"])
                 and isinstance(doc.get("source_decisions"), list) and isinstance(doc.get("output_decisions"), list))
        if valid:
            for field, key in (("source_decisions", "source"), ("output_decisions", "output")):
                valid = valid and all(isinstance(v, dict) and isinstance(v.get(key), str)
                                      and isinstance(v.get("decision"), str) for v in doc[field])
            valid = valid and all(v.get("decision") != "EXACT_RATIONAL_WITNESS_ONLY" or isinstance(v.get("exact_value"), str)
                                  for v in doc["output_decisions"])
        if not valid:errors.append("invalid report structure")
    except (ValueError, TypeError):
        errors.append("invalid JSON")
    row = {"returncode": child.returncode, "healthy": not errors, "problems": errors,
           "stdout_sha256": hashlib.sha256(child.stdout.encode()).hexdigest(),
           "stderr_sha256": hashlib.sha256(child.stderr.encode()).hexdigest()}
    CLI_HEALTH.append(row)
    return row


def pointer(path):
    return "/" + "/".join(x.replace("~", "~0").replace("/", "~1") for x in path)


class C8Quarantine(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), "C8 quarantine tool is missing")
        temp = tempfile.TemporaryDirectory(prefix="c8-quarantine-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        shutil.copytree(ROOT / PACKET, self.root / PACKET)
        (self.root / "PROOF_INDEX.md").write_bytes((ROOT / "PROOF_INDEX.md").read_bytes())
        record = self.root / RECORD
        record.parent.mkdir()
        if (ROOT / RECORD).is_file():
            record.write_bytes((ROOT / RECORD).read_bytes())

    def cli(self, *args, root=None):
        flags = ["-B", "-S", *(["-O"] if sys.flags.optimize else [])]
        env = {k: v for k, v in os.environ.items() if k not in {"PYTHONHOME", "PYTHONPATH", "PYTHONOPTIMIZE"}}
        try:
            child = subprocess.run([sys.executable, *flags, str(SCRIPT), "--root", str(root or self.root), *args],
                                   env=env, capture_output=True, text=True, timeout=15)
        except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
            CLI_HEALTH.append({"healthy": False, "problems": [type(exc).__name__]})
            raise
        observe_cli(child)
        return child

    def report(self, child):
        self.assertEqual(child.stderr, "", child)
        result = json.loads(child.stdout)
        self.assertIs(result["cbz_certificate_admitted"], False)
        self.assertEqual(result["scientific_effect"], "NONE")
        return result

    def refused(self, diagnostic, *args, root=None):
        child = self.cli(*args, root=root)
        self.assertEqual(child.returncode, 1, child)
        result = self.report(child)
        self.assertEqual(result["status"], "REFUSED")
        self.assertTrue(any(diagnostic in v for v in result["problems"]), result)
        return result

    def change(self, callback):
        path = self.root / RECORD
        value = json.loads(path.read_text())
        callback(value)
        path.write_text(json.dumps(value) + "\n")

    def pairs(self):
        rows = {}
        def walk(value, path):
            if isinstance(value, dict):
                for key, item in value.items():
                    walk(item, path + [key])
            elif isinstance(value, list) and len(value) == 2 and all(isinstance(x, str) for x in value):
                rows[pointer(path)] = value
        walk(json.loads((self.root / PACKET / "RESULTS.json").read_text())["results"], ["results"])
        self.assertEqual(len(rows), 109)
        exceptions = {pointer(["results", k, "parts", "E[2T]"]) for k in EXACT}
        return rows, exceptions

    def test_integrity_success_does_not_admit_arithmetic(self):
        child = self.cli();self.assertEqual(child.returncode, 0, child)
        result = self.report(child)
        self.assertEqual(result["status"], "QUARANTINE_INTEGRITY_OK")
        self.assertEqual(result["layer_a_status"], "A3_NOT_PROVEN")
        self.assertEqual((result["preserved_packet_files"], result["denied_output_count"], result["exact_exception_count"]), (11, 106, 3))

    def test_all_106_published_denied_outputs_are_mechanically_denied(self):
        rows, exceptions = self.pairs();denied = set(rows) - exceptions
        args = [x for p in sorted(denied) for x in ("--consume-output", p)]
        child = self.cli(*args);self.assertEqual(child.returncode, 1, child)
        result = self.report(child)
        self.assertEqual({d["output"] for d in result["output_decisions"] if d["decision"] == "DENIED"}, denied)
        self.assertEqual(len(result["output_decisions"]), 106)

    def test_three_fraction_witnesses_remain_explicitly_nonadmitting(self):
        rows, exceptions = self.pairs()
        args = [x for p in sorted(exceptions) for x in ("--consume-output", p)]
        child = self.cli(*args);self.assertEqual(child.returncode, 2, child)
        result = self.report(child);self.assertEqual(result["status"], "NOT_COVERED")
        self.assertEqual(len(result["output_decisions"]), 3)
        for d in result["output_decisions"]:
            self.assertEqual(d["decision"], "EXACT_RATIONAL_WITNESS_ONLY")
            lo, hi = map(F, rows[d["output"]]);exact = F(d["exact_value"])
            self.assertLessEqual(lo, exact);self.assertLessEqual(exact, hi)
            self.assertIn(str(exact), EXACT.values())

    def test_mixed_exception_and_denied_output_refuses(self):
        self.refused("quarantined numerical output", "--consume-output", "/results/k=1/parts/E[2T]",
                     "--consume-output", "/results/k=1/J_fail")

    def test_unknown_output_is_not_coverage_or_admission(self):
        child = self.cli("--consume-output", "/results/not-present")
        self.assertEqual(child.returncode, 2, child)
        self.assertEqual(self.report(child)["output_decisions"][0]["decision"], "NOT_COVERED")

    def test_packet_and_normalized_source_aliases_refuse(self):
        for name in (PACKET, "./" + PACKET + "/RESULTS.json", "frontiers/unused/../c8_elder_failure_coefficient_20261001/certificate.py"):
            with self.subTest(name=name):
                self.refused("quarantined numerical source", "--consume", name)

    def test_direct_packet_source_refuses(self):
        self.refused("quarantined numerical source", "--consume", PACKET + "/RESULTS.json")

    def test_renamed_c8_result_copy_cannot_evade_denial(self):
        dest = self.root / "mirror/results.json";dest.parent.mkdir()
        dest.write_bytes((self.root / PACKET / "RESULTS.json").read_bytes())
        self.refused("quarantined numerical source", "--consume", "mirror/results.json")

    def test_shared_ia_or_c2_source_is_not_quarantined_by_byte_equality(self):
        for name in ("frontiers/c2_exact_20261001/ia.py", "mirror/shared_ia.py"):
            dest = self.root / name;dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((self.root / PACKET / "ia.py").read_bytes())
            child = self.cli("--consume", name);self.assertEqual(child.returncode, 2, child)
            self.assertEqual(self.report(child)["source_decisions"][0]["decision"], "NOT_COVERED")

    def test_unrelated_analytic_proof_is_not_certified_or_refuted(self):
        child = self.cli("--consume", "frontiers/planar_compact_k_chain_20261006/PD/PROOF.md")
        self.assertEqual(child.returncode, 2, child)
        self.assertEqual(self.report(child)["status"], "NOT_COVERED")

    def test_missing_record_refuses(self):
        (self.root / RECORD).unlink();self.refused("missing quarantine record")

    def test_record_admission_must_be_typed_false(self):
        for value in (True, 0):
            self.change(lambda d: d.update(cbz_certificate_admitted=value))
            self.refused("admission must remain false")

    def test_classification_and_isolation_limits_cannot_be_promoted(self):
        self.change(lambda d: d.update(layer_a_status="A3_PROVEN"));self.refused("A3 classification")

    def test_owner_and_maintenance_cannot_be_invented(self):
        self.change(lambda d: d.update(owner="invented"));self.refused("owner must remain unassigned")
        self.change(lambda d: d.update(owner=None, maintenance=True));self.refused("maintenance must remain zero")

    def test_source_snapshot_is_exact(self):
        self.change(lambda d: d["source_snapshot"].update(commit="0" * 40));self.refused("source snapshot")

    def test_empty_or_duplicated_source_inventory_refuses(self):
        self.change(lambda d: d.update(source_files=[]));self.refused("packet inventory")

    def test_source_byte_count_requires_an_integer(self):
        self.change(lambda d: d["source_files"][0].update(bytes=float(d["source_files"][0]["bytes"])))
        self.refused("packet inventory")

    def test_packet_changes_and_extra_files_refuse(self):
        path = self.root / PACKET / "ia.py";path.write_bytes(path.read_bytes() + b"\n# altered\n")
        self.refused("packet source identity")
        (self.root / PACKET / "extra.py").write_text("pass\n");self.refused("packet tree differs")

    def test_refreshed_manifest_cannot_rebind_changed_sources(self):
        changed = self.root / PACKET / "ia.py";changed.write_bytes(changed.read_bytes() + b"\n# altered\n")
        def ident(path):
            raw = path.read_bytes()
            return {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                    "git_blob": hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()}
        manifest = self.root / PACKET / "SOURCE_FILES.json";doc = json.loads(manifest.read_text())
        for row in doc["files"]:
            if row["path"] == "ia.py":row.update(ident(changed))
        manifest.write_text(json.dumps(doc) + "\n")
        def rebind(d):
            for row in d["source_files"]:
                if row["path"] in (PACKET + "/ia.py", PACKET + "/SOURCE_FILES.json"):row.update(ident(self.root / row["path"]))
            d["source_snapshot"]["manifest"].update(ident(manifest))
        self.change(rebind);self.refused("frozen packet manifest")

    def test_changed_source_cannot_rebind_only_quarantine_metadata(self):
        p = self.root / PACKET / "ia.py";raw = p.read_bytes() + b"\n# changed\n";p.write_bytes(raw)
        def rebind(d):
            for row in d["source_files"]:
                if row["path"] == PACKET + "/ia.py":
                    row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                               git_blob=hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest())
        self.change(rebind);self.refused("packet source identity")

    def test_denied_inventory_cannot_be_emptied(self):
        self.change(lambda d: d.update(denied_outputs=[]));self.refused("denied output inventory")

    def test_denied_inventory_cannot_duplicate_or_change_an_endpoint(self):
        self.change(lambda d: d["denied_outputs"].__setitem__(0, d["denied_outputs"][1]));self.refused("denied output inventory")

    def test_exact_exceptions_cannot_be_removed(self):
        self.change(lambda d: d.update(exact_rational_exceptions=[]));self.refused("exact rational exception")

    def test_false_exact_rational_witness_refuses(self):
        self.change(lambda d: d["exact_rational_exceptions"][0].update(exact_value="1"));self.refused("exact rational exception")

    def test_fraction_checker_rejects_a_false_endpoint(self):
        spec = importlib.util.spec_from_file_location("c8_exact_control", SCRIPT)
        module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        results = json.loads((self.root / PACKET / "RESULTS.json").read_text())
        results["results"]["k=1"]["parts"]["E[2T]"] = ["1", "1"]
        with self.assertRaisesRegex(ValueError, "exact rational containment"):
            module.exact_exceptions(results)

    def test_denied_interval_endpoints_cannot_be_rewritten(self):
        self.change(lambda d: d["denied_outputs"][0].update(interval=["1", "1"]))
        self.refused("denied output inventory")

    def test_global_isolation_is_not_claimed_by_integrity_success(self):
        self.change(lambda d: d["isolation"].update(global_A3_audit=True))
        self.refused("limited opt-in scope")

    def test_mathematical_boundary_cannot_be_emptied(self):
        self.change(lambda d: d.update(not_proven_boundary=[]));self.refused("nonempty mathematical boundary")

    def test_snapshot_manifest_cannot_disagree_with_source(self):
        self.change(lambda d: d["source_snapshot"]["manifest"].update(git_blob="0" * 40))
        self.refused("snapshot manifest identity")

    def test_denial_sources_and_global_isolation_scope_are_exact(self):
        self.change(lambda d: d.update(denied_certificate_sources=[]));self.refused("denied source inventory")

    def test_missing_or_promoted_index_marker_refuses(self):
        (self.root / "PROOF_INDEX.md").write_text("# No C8 quarantine marker\n")
        self.refused("canonical index quarantine")

    def test_index_boolean_false_cannot_be_replaced_by_zero(self):
        p = self.root / "PROOF_INDEX.md";p.write_text(p.read_text().replace('"cbz_certificate_admitted":false', '"cbz_certificate_admitted":0'))
        self.refused("canonical index quarantine")

    def test_duplicate_json_members_refuse(self):
        p = self.root / RECORD;raw = p.read_text().rstrip();p.write_text(raw[:-1] + ',"cbz_certificate_admitted":false}')
        self.refused("duplicate JSON member")

    def test_invalid_utf8_and_nonfinite_json_refuse(self):
        p = self.root / RECORD;p.write_bytes(b'\xff');self.refused("UTF-8")
        p.write_text('{"bad":NaN}');self.refused("nonfinite JSON")

    def test_symlink_source_or_packet_ancestor_refuses(self):
        p = self.root / PACKET / "ia.py";raw = p.read_bytes();p.unlink()
        target = self.root / "outside-ia.py";target.write_bytes(raw);p.symlink_to(target)
        self.refused("regular local source")

    def test_symlink_record_and_index_refuse(self):
        p = self.root / RECORD;raw = p.read_bytes();p.unlink();target = self.root / "record.json";target.write_bytes(raw);p.symlink_to(target)
        self.refused("regular local source")

    def test_symlink_packet_directory_cannot_hide_sources(self):
        p = self.root / PACKET;target = self.root / "external-packet";p.rename(target);p.symlink_to(target, target_is_directory=True)
        self.refused("regular local source")

    def test_symlink_index_refuses(self):
        p = self.root / "PROOF_INDEX.md";raw = p.read_bytes();p.unlink();target = self.root / "index.md";target.write_bytes(raw);p.symlink_to(target)
        self.refused("regular local source")

    def test_symlink_checkout_root_refuses(self):
        with tempfile.TemporaryDirectory() as d:
            alias = Path(d) / "alias";alias.symlink_to(self.root, target_is_directory=True)
            self.refused("symlink checkout", root=alias)

    def test_unreadable_source_refuses_even_for_privileged_runner(self):
        p = self.root / PACKET / "ia.py";p.chmod(0)
        try:self.refused("unreadable local source")
        finally:p.chmod(0o644)

    def test_unsafe_source_paths_and_output_pointers_refuse(self):
        for name in ("", "../outside", "/tmp/source", "a\\b", "x:y"):
            with self.subTest(name=name):self.refused("unsafe consumer path", "--consume", name)
        for name in ("", "results/a", "/results/~2", "/results/a~"):
            with self.subTest(name=name):self.refused("invalid output pointer", "--consume-output", name)


if __name__ == "__main__":
    unittest.main()
