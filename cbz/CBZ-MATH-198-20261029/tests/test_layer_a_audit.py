"""Behavior tests: every case exercises the scanner executable on actual files."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCANNER = Path(os.environ.get("CBZ_SCANNER_UNDER_TEST", str(Path(__file__).resolve().parents[1] / "tools/layer_a_audit.py")))
GOOD = "import Mathlib\nnamespace E\ntheorem α : True := by trivial\nend E\n"
PYTHON = [sys.executable, "-B"] + (["-O"] if sys.flags.optimize else [])


def digest(data):
    return hashlib.sha256(data).hexdigest()


class LayerAScannerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = {"schema": "cbz-layer-a-manifest-v1", "roots": ["src"],
                         "external_imports": {"Mathlib": {"identity": "pinned-test-mathlib", "reason": "fixture dependency"},
                                              "Init": {"identity": "pinned-test-lean", "reason": "implicit prelude"}},
                         "files": []}
        self.quarantine = {"schema": "cbz-quarantine-v1", "entries": []}
        self.add("Proof.lean", GOOD)

    def add(self, name, text, kind="lean_proof", module=None):
        path = self.root / "src" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        data = text.encode() if isinstance(text, str) else text
        path.write_bytes(data)
        row = {"path": "src/" + name, "sha256": digest(data), "kind": kind}
        if name.endswith(".lean"):
            row["module"] = module or name[:-5].replace("/", ".")
        self.manifest["files"] = [r for r in self.manifest["files"] if r["path"] != row["path"]] + [row]
        return path

    def repin(self, name):
        for row in self.manifest["files"]:
            if row["path"] == "src/" + name:
                row["sha256"] = digest((self.root / row["path"]).read_bytes())

    def quarantine_file(self, name):
        row = next(r for r in self.manifest["files"] if r["path"] == "src/" + name)
        self.quarantine["entries"].append({
            "id": "CBQ-TEST-" + str(len(self.quarantine["entries"])), "title": "Explicit test boundary",
            "layer_a_status": "QUARANTINED", "exact_boundary": "This exact source remains unproved",
            "blocking_reason": "Unsupported or incomplete proof", "attempted": "Scanner fixture",
            "resumption_cost": "No resumption planned", "isolation": "No active incoming imports",
            "owner": "none", "maintenance": "zero",
            "location": [{"path": row["path"], "sha256": row["sha256"], "scope": "file"}]})

    def run_scan(self, scanner=SCANNER, manifest_text=None):
        self.assertTrue(scanner.is_file(), "Layer A scanner implementation is missing")
        mp = self.root / "manifest.json"
        mp.write_text(manifest_text if manifest_text is not None else json.dumps(self.manifest))
        qp = self.root / "quarantine.json"
        qp.write_text(json.dumps(self.quarantine))
        result = subprocess.run(PYTHON + [str(scanner), "--root", str(self.root),
                                 "--manifest", str(mp), "--quarantine", str(qp)],
                                text=True, capture_output=True, timeout=15)
        self.assertEqual(result.stderr, "", result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0 if report["ok"] else 1, report)
        self.assertFalse(report["kernel_verified"])
        return report

    def assertBlocked(self, code, report=None):
        report = report or self.run_scan()
        self.assertFalse(report["ok"], report)
        self.assertIn(code, {x["code"] for x in report["issues"]}, report)
        return report

    def test_clean_supported_source_passes_but_has_no_kernel_credit(self):
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["files_checked"], 1)

    def test_nested_comments_strings_raw_strings_and_unicode_names_are_inert(self):
        self.add("Proof.lean", GOOD + '/- sorry /- axiom -/ native_decide -/\n'
                 'def σorry : String := "admit \\\" sorry"\n'
                 'def r : String := r##"axiom \\" sorry"##\n')
        self.assertTrue(self.run_scan()["ok"])

    def test_zero_hash_raw_string_cannot_swallow_a_later_proof_hole(self):
        self.add("Proof.lean", r'''import Mathlib
def first := r"\"
theorem bad : False := by sorry
def last := "\""
''')
        self.assertBlocked("FORBIDDEN_TOKEN")

    def test_projection_numbers_and_axiom_diagnostics_are_supported(self):
        self.add("Proof.lean", GOOD + "def x (h : True ∧ (True ∧ True)) := h.2.1\n#print axioms E.α\n"
                 "def image : Set Nat := id '' Set.univ\ndef preimage : Set Nat := id ⁻¹' Set.univ\n")
        self.assertTrue(self.run_scan()["ok"])

    def test_actual_kernel_skip_option_is_prohibited(self):
        self.add("Proof.lean", "set_option debug.skipKernelTC true\n" + GOOD)
        self.assertBlocked("FORBIDDEN_TOKEN")

    def test_builtin_native_alias_and_native_reflection_axioms_are_prohibited(self):
        for suffix in ("theorem t : True := by decide +native\n",
                       "theorem t : True := by decide /- config -/ + native\n",
                       "#check Lean.ofReduceBool\n", "#check Lean.ofReduceNat\n"):
            with self.subTest(suffix=suffix):
                self.add("Proof.lean", GOOD + suffix)
                self.assertBlocked("FORBIDDEN_TOKEN")

    def test_direct_escapes_are_located_even_after_comments(self):
        for token in ("sorry", "admit", "native_decide", "axiom", "sorryAx"):
            with self.subTest(token=token):
                self.add("Proof.lean", GOOD + "/- inert -/\n" + token + "\n")
                report = self.assertBlocked("FORBIDDEN_TOKEN")
                issue = next(i for i in report["issues"] if i["code"] == "FORBIDDEN_TOKEN")
                self.assertEqual((issue["path"], issue["line"], issue["column"]), ("src/Proof.lean", 6, 1))

    def test_character_double_quote_cannot_hide_later_sorry(self):
        self.add("Proof.lean", GOOD + "def ch : Char := '\"'\ntheorem bad : False := by sorry\n")
        self.assertBlocked("FORBIDDEN_TOKEN")

    def test_escaped_identifier_and_qualified_sorry_axiom_are_caught(self):
        self.add("Proof.lean", GOOD + "#check Lean.«sorryAx»\n")
        self.assertBlocked("FORBIDDEN_TOKEN")

    def test_macro_alias_and_interpolation_are_unsupported_in_proofs(self):
        for addition in ('macro "ok" : tactic => `(tactic| sorry)\n',
                         'def s := s!"{by sorry}"\n', 'opaque bad : False\n'):
            with self.subTest(addition=addition):
                self.add("Proof.lean", GOOD + addition)
                report = self.run_scan()
                self.assertFalse(report["ok"], report)
                self.assertTrue({i["code"] for i in report["issues"]} &
                                {"UNSUPPORTED_METAPROGRAMMING", "UNSUPPORTED_STRING_MACRO"}, report)

    def test_auditor_role_is_explicit_and_still_catches_escapes(self):
        self.add("Proof.lean", 'import Mathlib\nelab "#foo" : command => pure ()\n'
                 'def msg (n : Nat) := s!"count {n}"\n', "lean_auditor")
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["trusted_auditor_files"], ["src/Proof.lean"])
        self.add("Proof.lean", 'import Mathlib\naxiom bad : False\n', "lean_auditor")
        self.assertBlocked("FORBIDDEN_TOKEN")

    def test_auditor_interpolated_identifier_is_executable_code(self):
        for expression in ("sorry", "Lean.sorryAx", "native_decide"):
            with self.subTest(expression=expression):
                self.add("Proof.lean", 'import Mathlib\ndef msg := s!"{' + expression + '}"\n', "lean_auditor")
                self.assertBlocked("FORBIDDEN_TOKEN")

    def test_malformed_or_truncated_lexical_inputs_fail_closed(self):
        for suffix in ('/- outer /- nested -/', 'def s := "unterminated',
                       'theorem bad : True := by\n', 'def x := (1\n', 'def x := «unterminated'):
            with self.subTest(suffix=suffix):
                self.add("Proof.lean", GOOD + suffix)
                self.assertFalse(self.run_scan()["ok"])

    def test_float_aliases_are_not_exact_proof_certificates(self):
        for suffix in ('abbrev F := Float\ndef x : F := 1\n', 'def x : Float32 := 0.5\n',
                       'def x := Float.ofNat 1\n'):
            with self.subTest(suffix=suffix):
                self.add("Proof.lean", GOOD + suffix)
                self.assertBlocked("INEXACT_PROOF_NUMBER")

    def test_lean_real_scientific_literals_are_exact_not_floating(self):
        self.add("Proof.lean", GOOD + 'def x : ℝ := 0.525284915110958116723095\n'
                 'def y : ℝ := 1e-3\ndef z : ℝ := 1_0.5\n')
        self.assertTrue(self.run_scan()["ok"])

    def test_environment_metaprogramming_commands_require_auditor_role(self):
        for keyword in ("run_cmd", "run_meta", "builtin_initialize"):
            with self.subTest(keyword=keyword):
                self.add("Proof.lean", GOOD + keyword + " pure ()\n")
                self.assertBlocked("UNSUPPORTED_METAPROGRAMMING")

    def test_import_graph_requires_every_local_module_and_known_external_pin(self):
        self.add("Proof.lean", "import Missing\ntheorem t : True := by trivial\n")
        self.assertBlocked("UNRESOLVED_IMPORT")
        self.add("Other.lean", GOOD)
        self.add("Proof.lean", "public import Other Mathlib\ntheorem t : True := by trivial\n")
        self.assertTrue(self.run_scan()["ok"])

    def test_escaped_module_name_is_an_unsupported_import_not_a_dotted_alias(self):
        self.add("Proof.lean", "import «Mathlib.Order.Disjointed»\ntheorem t : True := by trivial\n")
        self.assertBlocked("UNSUPPORTED_IMPORT")

    def test_cli_argument_errors_are_terminal_json(self):
        result = subprocess.run(PYTHON + [str(SCANNER)], text=True, capture_output=True, timeout=10)
        self.assertEqual(result.stderr, "")
        report = json.loads(result.stdout)
        self.assertFalse(report["ok"])
        self.assertEqual(report["issues"][0]["code"], "INVALID_ARGUMENT")

    def test_cli_requires_explicit_quarantine_index(self):
        manifest = self.root / "manifest.json"
        manifest.write_text(json.dumps(self.manifest))
        result = subprocess.run(PYTHON + [str(SCANNER), "--root", str(self.root), "--manifest", str(manifest)],
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.stderr, "")
        report = json.loads(result.stdout)
        self.assertFalse(report["ok"])
        self.assertEqual(report["issues"][0]["code"], "INVALID_ARGUMENT")

    def test_oversized_path_component_is_a_json_failure(self):
        self.manifest["roots"] = ["a" * 300]
        self.manifest["files"][0]["path"] = "a" * 300 + "/Proof.lean"
        self.assertBlocked("INVALID_MANIFEST")

    def test_external_allowlist_cannot_shadow_local_module(self):
        self.manifest["external_imports"]["Proof"] = {"identity": "fake", "reason": "shadow"}
        self.assertBlocked("EXTERNAL_SHADOW")

    def test_module_identifier_cannot_relabel_a_quarantined_source_path(self):
        self.add("Unsafe.lean", "axiom bad : False\n", module="Alias")
        self.quarantine_file("Unsafe.lean")
        self.manifest["external_imports"]["Unsafe"] = {"identity": "fake external", "reason": "bypass attempt"}
        self.add("Proof.lean", "import Unsafe\ntheorem t : True := by trivial\n")
        self.assertBlocked("MODULE_PATH_MISMATCH")

    def test_missing_unlisted_and_hash_drift_files_fail(self):
        (self.root / "src/Extra.lean").write_text(GOOD)
        self.assertBlocked("UNLISTED_FILE")
        (self.root / "src/Extra.lean").unlink()
        (self.root / "src/Proof.lean").write_text(GOOD[:-7])
        self.assertBlocked("SOURCE_HASH_MISMATCH")
        (self.root / "src/Proof.lean").unlink()
        self.assertBlocked("MISSING_FILE")

    def test_symlink_leaf_and_parent_are_rejected(self):
        path = self.root / "src/Proof.lean"
        actual = self.root / "actual.lean"
        actual.write_text(GOOD)
        path.unlink(); path.symlink_to(actual)
        self.assertBlocked("SYMLINK")
        path.unlink(); (self.root / "src").rmdir(); (self.root / "src").symlink_to(self.root)
        self.assertBlocked("SYMLINK")

    def test_duplicate_json_keys_bool_metadata_and_duplicate_modules_fail(self):
        self.assertBlocked("INVALID_JSON", self.run_scan(manifest_text='{"schema":"x","schema":"y"}'))
        self.manifest["files"][0]["sha256"] = True
        self.assertBlocked("INVALID_MANIFEST")
        self.manifest["files"][0]["sha256"] = digest(GOOD.encode())
        self.add("Other.lean", GOOD, module="Proof")
        self.assertBlocked("DUPLICATE_MODULE")

    def test_unhashable_schema_values_and_falsy_quarantine_fail_closed(self):
        self.manifest["files"][0]["kind"] = []
        self.assertBlocked("INVALID_MANIFEST")
        self.manifest["files"][0]["kind"] = "lean_proof"
        for malformed in ({}, [], False):
            with self.subTest(malformed=malformed):
                self.quarantine = malformed
                self.assertBlocked("INVALID_QUARANTINE")
        self.quarantine = {"schema": "cbz-quarantine-v1", "entries": []}
        self.quarantine_file("Proof.lean")
        self.quarantine["entries"][0]["location"][0]["scope"] = []
        self.assertBlocked("INVALID_QUARANTINE")

    def test_unreadable_subtree_is_not_silently_omitted(self):
        if os.geteuid() == 0:
            self.skipTest("root bypasses directory permission restrictions")
        hidden = self.root / "src/hidden"
        hidden.mkdir(); (hidden / "unlisted.lean").write_text(GOOD)
        hidden.chmod(0)
        self.addCleanup(hidden.chmod, 0o700)
        self.assertBlocked("INVENTORY_IO_ERROR")

    def test_oversize_and_excessive_nesting_are_terminal_failures(self):
        self.add("Proof.lean", b" " * (2 * 1024 * 1024 + 1))
        self.assertBlocked("RESOURCE_LIMIT")
        self.add("Proof.lean", "/-" * 257 + "-/" * 257)
        self.assertBlocked("RESOURCE_LIMIT")

    def test_lean_file_cannot_be_reclassified_operational(self):
        self.manifest["files"][0]["kind"] = "operational_record"
        self.assertBlocked("INVALID_MANIFEST")

    def test_quarantine_is_exact_explicit_and_dependency_isolated(self):
        self.add("Unproved.lean", "import Mathlib\naxiom x : False\n")
        self.quarantine_file("Unproved.lean")
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["status"], "PASS_WITH_QUARANTINE")
        self.assertEqual(report["quarantined_files"], ["src/Unproved.lean"])
        self.add("Proof.lean", "import Unproved\ntheorem t : True := by trivial\n")
        self.assertBlocked("QUARANTINE_DEPENDENCY")

    def test_quarantine_bad_hash_or_owner_is_not_an_ignore(self):
        self.quarantine_file("Proof.lean")
        self.quarantine["entries"][0]["owner"] = "active person"
        self.assertBlocked("INVALID_QUARANTINE")
        self.quarantine["entries"][0]["owner"] = "none"
        self.quarantine["entries"][0]["location"][0]["sha256"] = "0" * 64
        self.assertBlocked("QUARANTINE_HASH_MISMATCH")

    def test_directory_quarantine_cannot_cover_active_root_or_ancestor(self):
        self.quarantine_file("Proof.lean")
        loc = self.quarantine["entries"][0]["location"][0]
        loc["scope"] = "directory"
        for directory in (self.root, self.root.parent):
            with self.subTest(directory=str(directory)):
                loc["path"] = str(directory)
                self.assertBlocked("INVALID_QUARANTINE")

    def test_obligation_boundary_does_not_quarantine_its_valid_definition_file(self):
        self.add("Proof.lean", "import Mathlib\ndef OpenGoal : Prop := False\n")
        self.quarantine_file("Proof.lean")
        loc = self.quarantine["entries"][0]["location"][0]
        loc["scope"] = "obligation"; loc["path"] += "#OpenGoal"
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["status"], "PASS_WITH_QUARANTINE")
        self.assertEqual(report["quarantined_files"], [])
        self.assertEqual(report["unproved_obligations"][0]["declaration"], "OpenGoal")
        loc["path"] += "::hcert"
        self.assertTrue(self.run_scan()["ok"])

    def test_lone_unicode_surrogates_are_rejected_as_json_input(self):
        self.manifest["external_imports"]["Init"]["reason"] = "\ud800"
        self.assertBlocked("INVALID_JSON")

    def test_external_json_obligation_fragment_is_an_uncertified_reference(self):
        self.quarantine_file("Proof.lean")
        loc = self.quarantine["entries"][0]["location"][0]
        loc["scope"] = "obligation"
        loc["path"] = "metadata/REGISTER.json#claims/0/statements/Some.Target"
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["unproved_obligations"], [])
        self.assertEqual(len(report["quarantine_references_outside_scope"]), 1)

    def test_operational_source_has_integrity_credit_only_and_unsupported_needs_quarantine(self):
        self.add("clock.py", "seconds = 0.25\n", "operational_source")
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["operational_sources_checked"], ["src/clock.py"])
        self.add("blob.bin", b"\xff\x00", "unsupported")
        self.assertBlocked("UNSUPPORTED_FILE")
        self.quarantine_file("blob.bin")
        self.assertTrue(self.run_scan()["ok"])

    def test_exact_rational_certificate_and_operational_timing_have_distinct_credit(self):
        cert = {"schema": "cbz-rational-certificate-v1", "inequalities": [
            {"left": "949/1024", "relation": ">", "right": "11/12"}]}
        self.add("bound.json", json.dumps(cert), "rational_certificate")
        self.add("timing.json", '{"wall_seconds":0.125}', "operational_record")
        report = self.run_scan()
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["exact_certificates_checked"], ["src/bound.json"])
        self.assertEqual(report["operational_records_checked"], ["src/timing.json"])
        cert["inequalities"][0]["right"] = "1"
        self.add("bound.json", json.dumps(cert), "rational_certificate")
        self.assertBlocked("FALSE_RATIONAL_CERTIFICATE")

    def test_rational_float_bool_nan_and_zero_denominator_fail(self):
        for value in (0.5, True, "1/0", "1e-3"):
            with self.subTest(value=value):
                cert = {"schema": "cbz-rational-certificate-v1", "inequalities": [
                    {"left": value, "relation": "<", "right": "1"}]}
                self.add("bound.json", json.dumps(cert), "rational_certificate")
                self.assertBlocked("INVALID_RATIONAL_CERTIFICATE")
        self.add("timing.json", '{"wall_seconds":NaN}', "operational_record")
        self.assertBlocked("INVALID_JSON")

    def test_mutating_scanner_checks_breaks_original_negative_controls(self):
        self.assertTrue(SCANNER.is_file(), "Layer A scanner implementation is missing")
        source = SCANNER.read_text()
        mutations = [("if token.value in FORBIDDEN:", "if False and token.value in FORBIDDEN:", "escape",
                      "test_direct_escapes_are_located_even_after_comments"),
                     ("if path not in entries:", "if False and path not in entries:", "inventory",
                      "test_missing_unlisted_and_hash_drift_files_fail"),
                     ('if kind == "lean_proof" and token.value in {"Float", "Float32", "Float64"}:',
                      'if False and kind == "lean_proof" and token.value in {"Float", "Float32", "Float64"}:',
                      "float_alias", "test_float_aliases_are_not_exact_proof_certificates"),
                     ("                    rational_certificate(data, path)",
                      "                    pass  # deliberately weakened exact-certificate checker",
                      "rational", "test_rational_float_bool_nan_and_zero_denominator_fail")]
        for before, after, label, control in mutations:
            with self.subTest(label=label):
                self.assertEqual(source.count(before), 1, "mutation anchor must identify one actual validation")
                mutant = self.root / (label + ".py")
                mutant.write_text(source.replace(before, after))
                env = dict(os.environ, CBZ_SCANNER_UNDER_TEST=str(mutant))
                result = subprocess.run(PYTHON + ["-m", "unittest",
                                         "test_layer_a_audit.LayerAScannerTests." + control],
                                        cwd=Path(__file__).parent, env=env, text=True,
                                        capture_output=True, timeout=30)
                self.assertNotEqual(result.returncode, 0, "weakened scanner survived the original negative control")
                self.assertIn("FAIL:", result.stderr)
                self.assertNotIn("ERROR:", result.stderr)


if __name__ == "__main__":
    unittest.main()
