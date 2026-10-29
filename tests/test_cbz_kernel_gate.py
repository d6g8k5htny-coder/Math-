"""CBZ native gate refusals: omitted source, forged census, stale output and bad child exit."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOL = Path(__file__).resolve().parents[1] / "tools" / "cbz_kernel_gate.py"
gate = None
if TOOL.exists():
    spec = importlib.util.spec_from_file_location("cbz_kernel_gate", TOOL)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

BASE = """CBZ|MODULE|s4d|2|2
CBZ|DECL|s4d|s4d/s74|theorem
CBZ|DECL|s4d|s4d/s64|def
CBZ|AXIOMS|
CBZ|END|1|2|3
"""
NATIVE = """CBZ|MODULE|s4d|2|2
CBZ|DECL|s4d|s756e7573656443425a4e6174697665|theorem
CBZ|DECL|s4d|s756e7573656443425a4e6174697665/s5f6e6174697665/s6e61746976655f646563696465/s61785f31375f33|axiom
CBZ|AXIOMS|s756e7573656443425a4e6174697665/s5f6e6174697665/s6e61746976655f646563696465/s61785f31375f33
CBZ|END|1|2|3
"""

class NativeGateTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(gate, "CBZ native gate is not implemented")

    def project(self, root, lake='name = "fixture"\n[[lean_lib]]\nname = "M"\n'):
        p = root / "formal"
        p.mkdir()
        (p / "lakefile.toml").write_text(lake)
        (p / "lean-toolchain").write_text("leanprover/lean4:v4.34.1\n")
        (p / "lake-manifest.json").write_text(json.dumps({"packages": []}))
        return p

    def test_orphan_native_module_is_included_even_without_an_import(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (p / "M.lean").write_text("def x : Nat := 1\n")
            (p / "Orphan.lean").write_text("theorem hidden : True := True.intro\n")
            report = gate.project_inventory(root, "formal")
            self.assertEqual([x["module"] for x in report["modules"]], ["M", "Orphan"])

    def test_srcdir_is_removed_from_actual_module_identity(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root, 'name = "fixture"\n[[lean_lib]]\nname = "Inputs"\nsrcDir = "inputs"\nroots = ["M"]\n')
            (p / "inputs").mkdir()
            (p / "inputs/M.lean").write_text("def x : Nat := 1\n")
            report = gate.project_inventory(root, "formal")
            self.assertEqual(report["modules"][0]["module"], "M")
            self.assertEqual(report["modules"][0]["path"], "inputs/M.lean")

    def test_two_source_paths_cannot_shadow_one_module(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root, 'name = "fixture"\n[[lean_lib]]\nname = "M"\n[[lean_lib]]\nname = "Inputs"\nsrcDir = "inputs"\n')
            (p / "M.lean").write_text("def x : Nat := 1\n")
            (p / "inputs").mkdir();(p / "inputs/M.lean").write_text("def x : Nat := 2\n")
            with self.assertRaisesRegex(gate.GateError, "duplicate module"):
                gate.project_inventory(root, "formal")

    def test_source_symlink_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (root / "external").write_text("def x : Nat := 1\n")
            (p / "M.lean").symlink_to(root / "external")
            with self.assertRaisesRegex(gate.GateError, "symlink"):
                gate.project_inventory(root, "formal")

    def test_source_directory_symlink_cannot_hide_a_module(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (p / "M.lean").write_text("def x : Nat := 1\n")
            external = root / "external";external.mkdir()
            (external / "Hidden.lean").write_text("axiom hidden : False\n")
            (p / "hidden").symlink_to(external, target_is_directory=True)
            with self.assertRaisesRegex(gate.GateError, "symlink"):
                gate.project_inventory(root, "formal")

    def test_unreadable_source_directory_is_refused_even_for_privileged_runner(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (p / "M.lean").write_text("def x : Nat := 1\n")
            hidden = p / "hidden";hidden.mkdir()
            (hidden / "Hidden.lean").write_text("axiom hidden : False\n")
            hidden.chmod(0)
            try:
                with self.assertRaisesRegex(gate.GateError, "unreadable|inaccessible"):
                    gate.project_inventory(root, "formal")
            finally:
                hidden.chmod(0o700)

    def test_invalid_utf8_native_source_is_refused_at_inventory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (p / "M.lean").write_bytes(b"def x := 1\n\xff")
            with self.assertRaisesRegex(gate.GateError, "UTF-8"):
                gate.project_inventory(root, "formal")

    def test_native_module_system_source_is_refused_until_sidecars_are_qualified(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (p / "M.lean").write_text("module\npublic def x : Nat := 1\n")
            with self.assertRaisesRegex(gate.GateError, "module-system"):
                gate.project_inventory(root, "formal")

    def test_absolute_or_parent_project_escape_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "own";root.mkdir()
            outside = self.project(Path(d))
            (outside / "M.lean").write_text("def x : Nat := 1\n")
            for relative in (str(outside), "../formal"):
                with self.subTest(relative=relative), self.assertRaisesRegex(gate.GateError, "project path|escape"):
                    gate.project_inventory(root, relative)

    def test_root_cache_is_explicitly_excluded(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root)
            (p / "M.lean").write_text("def x : Nat := 1\n")
            (p / ".lake/packages").mkdir(parents=True)
            (p / ".lake/packages/Dependency.lean").write_text("axiom external : False\n")
            report = gate.project_inventory(root, "formal")
            self.assertEqual([x["module"] for x in report["modules"]], ["M"])
            self.assertEqual(report["excluded_cache_dirs"], [".lake"])

    def test_missing_declared_library_root_cannot_pass_inventory(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);p = self.project(root, 'name = "fixture"\n[[lean_lib]]\nname = "M"\nroots = ["Missing"]\n')
            (p / "M.lean").write_text("def x : Nat := 1\n")
            with self.assertRaisesRegex(gate.GateError, "root"):
                gate.project_inventory(root, "formal")

    def test_tracked_native_module_cannot_be_omitted_from_filesystem_census(self):
        snapshot = {"projects": [{"project": "formal", "modules": [{"path": "M.lean"}]}]}
        with self.assertRaisesRegex(gate.GateError, "coverage"):
            gate.require_tracked_coverage(snapshot, {"formal/M.lean", "formal/hidden/Hidden.lean"})

    def test_valid_compiled_census_preserves_total_and_every_declaration(self):
        r = gate.parse_audit(BASE, ["M"])
        self.assertEqual(r["declaration_count"], 2)
        self.assertEqual(r["module_counts"], {"M": 2})
        self.assertEqual(sorted(x["name"] for x in r["declarations"]), ["M.d", "M.t"])

    def test_omitted_registered_module_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "module"):
            gate.parse_audit(BASE, ["M", "Omitted"])

    def test_independent_census_disagreement_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "census"):
            gate.parse_audit(BASE.replace("s4d|2|2", "s4d|2|1"), ["M"])

    def test_duplicate_constant_cannot_satisfy_count(self):
        with self.assertRaisesRegex(gate.GateError, "duplicate"):
            gate.parse_audit(BASE.replace("s4d/s64", "s4d/s74"), ["M"])

    def test_missing_terminal_marker_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "END"):
            gate.parse_audit(BASE.replace("CBZ|END|1|2|3\n", ""), ["M"])

    def test_false_terminal_total_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "count"):
            gate.parse_audit(BASE.replace("END|1|2|3", "END|1|1|3"), ["M"])

    def test_unrecognized_protocol_record_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "protocol"):
            gate.parse_audit(BASE + "CBZ|MADE_UP|green\n", ["M"])

    def test_unused_custom_axiom_is_refused_even_with_empty_union(self):
        with self.assertRaisesRegex(gate.GateError, "axiom"):
            gate.parse_audit(BASE.replace("s4d/s64|def", "s4d/s64|axiom"), ["M"])

    def test_unsafe_definition_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "unsafe"):
            gate.parse_audit(BASE.replace("s4d/s64|def", "s4d/s64|unsafe"), ["M"])

    def test_transitive_sorry_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "sorryAx"):
            gate.parse_audit(BASE.replace("CBZ|AXIOMS|", "CBZ|AXIOMS|s736f7272794178"), ["M"])

    def test_native_reduce_axiom_is_refused(self):
        with self.assertRaisesRegex(gate.GateError, "Lean.ofReduceBool"):
            gate.parse_audit(BASE.replace("CBZ|AXIOMS|", "CBZ|AXIOMS|s4c65616e/s6f66526564756365426f6f6c"), ["M"])

    def test_pinned_native_generated_axiom_control_is_qualified_only_as_expected_refusal(self):
        result = gate.validate_control(NATIVE, "M", "native")
        self.assertEqual(result["forbidden_axioms"], ["unusedCBZNative._native.native_decide.ax_17_3"])

    def test_native_control_cannot_accept_an_unrelated_generated_axiom(self):
        with self.assertRaises(gate.GateError):
            gate.validate_control(NATIVE.replace("s61785f31375f33", "s61785f6f74686572"), "M", "native")

    def test_native_control_requires_the_actual_named_theorem(self):
        with self.assertRaises(gate.GateError):
            gate.validate_control(NATIVE.replace("s756e7573656443425a4e6174697665|theorem", "s756e7573656443425a4e6174697665|def"), "M", "native")

    def test_module_single_component_alias_cannot_impersonate_dotted_module(self):
        text = BASE.replace("CBZ|MODULE|s4d|", "CBZ|MODULE|s412e42|").replace("CBZ|DECL|s4d|", "CBZ|DECL|s412e42|")
        with self.assertRaisesRegex(gate.GateError, "module"):
            gate.parse_audit(text, ["A.B"])

    def committed_repo(self, root):
        subprocess.run(["git", "init", "--quiet", str(root)], check=True)
        (root / "M.lean").write_text("def x : Nat := 1\n")
        subprocess.run(["git", "-C", str(root), "add", "M.lean"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=CBZ test", "-c", "user.email=cbz-test@example.invalid", "commit", "--quiet", "-m", "fixture"], check=True)
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()

    def test_assume_unchanged_cannot_hide_bytes_from_commit_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);head = self.committed_repo(root)
            subprocess.run(["git", "-C", str(root), "update-index", "--assume-unchanged", "M.lean"], check=True)
            (root / "M.lean").write_text("def x : Nat := 999\n")
            self.assertEqual(subprocess.check_output(["git", "-C", str(root), "status", "--porcelain"], text=True), "")
            with self.assertRaisesRegex(gate.GateError, "HEAD blob"):
                gate.attest_sources(root, head, {"M.lean"})

    def test_matching_commit_bytes_receive_canonical_blob_attestation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);head = self.committed_repo(root)
            report = gate.attest_sources(root, head, {"M.lean"})
            self.assertEqual(report["files"], 1)
            self.assertEqual(report["commit"], head)

    def test_dependency_clean_label_cannot_hide_changed_tracked_sources(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);dependency = root / "formal/.lake/packages/mathlib"
            dependency.mkdir(parents=True)
            head = self.committed_repo(dependency)
            subprocess.run(["git", "-C", str(dependency), "update-index", "--assume-unchanged", "M.lean"], check=True)
            (dependency / "M.lean").write_text("def x : Nat := 999\n")
            with self.assertRaisesRegex(gate.GateError, "HEAD blob"):
                gate.share_dependencies(root, {"projects": [{"project": "formal"}]}, {"mathlib": head})

    def dependency_link_repo(self, root, relative="docs/README.md", payload="../README.md"):
        dependency = root / "formal/.lake/packages/batteries"
        dependency.mkdir(parents=True)
        self.committed_repo(dependency)
        link = dependency / relative
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(payload)
        subprocess.run(["git", "-C", str(dependency), "add", relative], check=True)
        subprocess.run(["git", "-C", str(dependency), "-c", "user.name=CBZ test", "-c", "user.email=cbz-test@example.invalid", "commit", "--quiet", "-m", "link fixture"], check=True)
        head = subprocess.check_output(["git", "-C", str(dependency), "rev-parse", "HEAD"], text=True).strip()
        return dependency, head

    def reviewed_link_policy(self, head):
        payload = b"../README.md"
        return {("batteries", head): {"docs/README.md": {
            "git_blob": hashlib.sha1(b"blob 12\0" + payload).hexdigest(),
            "payload_hex": payload.hex(), "role": "documentation alias"}}}

    def test_reviewed_dependency_link_payload_is_attested_without_following(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);dependency, head = self.dependency_link_repo(root)
            self.assertFalse((dependency / "docs/README.md").exists(), "fixture target must be absent")
            with patch.object(gate, "DEPENDENCY_METADATA_LINKS", self.reviewed_link_policy(head), create=True):
                result = gate.share_dependencies(root, {"projects": [{"project": "formal"}]}, {"batteries": head})
            report = result["batteries"]["tracked_source_attestation"]
            link = next(row for row in report["source_records"] if row["path"] == "docs/README.md")
            self.assertEqual(report["symlink_files"], 1)
            self.assertEqual(link["mode"], "120000")
            self.assertEqual(link["kind"], "symlink_payload")
            self.assertEqual(link["payload_hex"], b"../README.md".hex())
            self.assertEqual(link["sha256"], hashlib.sha256(b"../README.md").hexdigest())
            self.assertEqual(link["role"], "documentation alias")
            self.assertIs(link["target_followed"], False)

    def test_changed_reviewed_link_target_cannot_hide_behind_clean_git_status(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);dependency, head = self.dependency_link_repo(root)
            subprocess.run(["git", "-C", str(dependency), "update-index", "--assume-unchanged", "docs/README.md"], check=True)
            link = dependency / "docs/README.md";link.unlink();link.symlink_to("../M.lean")
            self.assertEqual(gate.git_output(dependency, "status", "--porcelain"), "")
            with patch.object(gate, "DEPENDENCY_METADATA_LINKS", self.reviewed_link_policy(head), create=True):
                with self.assertRaisesRegex(gate.GateError, "HEAD blob"):
                    gate.attest_sources(dependency, head, {"docs/README.md"}, dependency="batteries")

    def test_documentation_symlink_is_refused_by_default(self):
        with tempfile.TemporaryDirectory() as d:
            dependency, head = self.dependency_link_repo(Path(d))
            with self.assertRaisesRegex(gate.GateError, "source mode"):
                gate.attest_sources(dependency, head, {"docs/README.md"})

    def test_dependency_source_configuration_and_gate_links_remain_refused(self):
        for name in ("Hidden.lean", "lakefile.toml", "lakefile.lean", "lake-manifest.json", "lean-toolchain", "tools/cbz_kernel_gate.py"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                root = Path(d);dependency, head = self.dependency_link_repo(root, name)
                with patch.object(gate, "DEPENDENCY_METADATA_LINKS", self.reviewed_link_policy(head), create=True):
                    with self.assertRaisesRegex(gate.GateError, "source mode"):
                        gate.share_dependencies(root, {"projects": [{"project": "formal"}]}, {"batteries": head})

    def test_reviewed_metadata_link_with_symlinked_ancestor_is_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d);dependency, head = self.dependency_link_repo(root)
            (dependency / "docs").rename(root / "external-docs")
            (dependency / "docs").symlink_to(root / "external-docs", target_is_directory=True)
            with patch.object(gate, "DEPENDENCY_METADATA_LINKS", self.reviewed_link_policy(head), create=True):
                with self.assertRaisesRegex(gate.GateError, "symlink.*ancestor"):
                    gate.attest_sources(dependency, head, {"docs/README.md"}, dependency="batteries")

    def test_reviewed_metadata_link_must_retain_git_symlink_mode(self):
        with tempfile.TemporaryDirectory() as d:
            dependency, head = self.dependency_link_repo(Path(d))
            link = dependency / "docs/README.md";link.unlink();link.write_bytes(b"../README.md")
            with patch.object(gate, "DEPENDENCY_METADATA_LINKS", self.reviewed_link_policy(head), create=True):
                with self.assertRaisesRegex(gate.GateError, "symlink mode"):
                    gate.attest_sources(dependency, head, {"docs/README.md"}, dependency="batteries")

    def test_metadata_link_review_does_not_transfer_to_another_revision(self):
        with tempfile.TemporaryDirectory() as d:
            dependency, head = self.dependency_link_repo(Path(d))
            with patch.object(gate, "DEPENDENCY_METADATA_LINKS", self.reviewed_link_policy("0" * 40), create=True):
                with self.assertRaisesRegex(gate.GateError, "source mode"):
                    gate.attest_sources(dependency, head, {"docs/README.md"}, dependency="batteries")

    def test_metadata_link_must_match_the_independently_reviewed_git_blob(self):
        with tempfile.TemporaryDirectory() as d:
            dependency, head = self.dependency_link_repo(Path(d))
            policy = self.reviewed_link_policy(head)
            policy[("batteries", head)]["docs/README.md"]["git_blob"] = "0" * 40
            with patch.object(gate, "DEPENDENCY_METADATA_LINKS", policy, create=True):
                with self.assertRaisesRegex(gate.GateError, "reviewed metadata"):
                    gate.attest_sources(dependency, head, {"docs/README.md"}, dependency="batteries")

    def test_standard_core_axiom_is_the_explicit_exception(self):
        r = gate.parse_audit(BASE.replace("CBZ|AXIOMS|", "CBZ|AXIOMS|s70726f70657874"), ["M"])
        self.assertEqual(r["axioms"], ["propext"])

    def test_quoted_single_component_cannot_impersonate_standard_axiom(self):
        # This encodes one string component, not the two-component core Name.
        with self.assertRaisesRegex(gate.GateError, "forbidden transitive axiom"):
            gate.parse_audit(BASE.replace("CBZ|AXIOMS|", "CBZ|AXIOMS|s436c6173736963616c2e63686f696365"), ["M"])

    def test_terminal_marker_cannot_precede_more_protocol_records(self):
        text = BASE.replace("CBZ|END|1|2|3\n", "")
        with self.assertRaisesRegex(gate.GateError, "terminal"):
            gate.parse_audit("CBZ|END|1|2|3\n" + text, ["M"])

    def test_negative_control_refuses_missing_axiom_report(self):
        text = BASE.replace("CBZ|AXIOMS|\n", "")
        with self.assertRaises(gate.GateError):
            gate.validate_control(text, "M", "unused_axiom")

    def test_negative_control_refuses_unrelated_parser_failure(self):
        with self.assertRaises(gate.GateError):
            gate.validate_control(BASE + "CBZ|MADE_UP|axiom\n", "M", "unused_axiom")

    def test_negative_control_must_name_its_actual_forbidden_axiom(self):
        text = BASE.replace("CBZ|AXIOMS|", "CBZ|AXIOMS|s736f7272794178")
        with self.assertRaises(gate.GateError):
            gate.validate_control(text, "M", "native")

    def test_negative_sorry_control_accepts_only_complete_refusal(self):
        text = BASE.replace("CBZ|AXIOMS|", "CBZ|AXIOMS|s736f7272794178")
        result = gate.validate_control(text, "M", "sorry")
        self.assertEqual(result["forbidden_axioms"], ["sorryAx"])

    def test_empty_project_is_refused_but_empty_aggregator_is_visible(self):
        empty = "CBZ|MODULE|s4d|0|0\nCBZ|AXIOMS|\nCBZ|END|1|0|0\n"
        with self.assertRaisesRegex(gate.GateError, "empty"):
            gate.parse_audit(empty, ["M"])
        r = gate.parse_audit(BASE.replace("CBZ|AXIOMS|", "CBZ|MODULE|s52|0|0\nCBZ|AXIOMS|").replace("END|1|2|3", "END|2|2|3"), ["M", "R"])
        self.assertEqual(r["module_counts"]["R"], 0)

    def test_source_hash_change_prevents_reusing_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "M.lean";p.write_text("def x := 1\n")
            before = gate.digest(p);p.write_text("def x := 2\n")
            with self.assertRaisesRegex(gate.GateError, "changed"):
                gate.require_unchanged({"M.lean": before}, Path(d))

    def test_fresh_native_build_removes_old_objects_keeps_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d);(p / ".lake/build/lib/lean").mkdir(parents=True)
            (p / ".lake/build/lib/lean/Old.olean").write_text("old")
            (p / ".lake/packages").mkdir()
            (p / ".lake/packages/keep").write_text("dependency")
            gate.fresh_build_directory(p)
            self.assertFalse((p / ".lake/build").exists())
            self.assertEqual((p / ".lake/packages/keep").read_text(), "dependency")

    def test_symlink_build_directory_is_refused_before_removal(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d);(p / ".lake").mkdir();(p / "victim").mkdir()
            (p / ".lake/build").symlink_to(p / "victim", target_is_directory=True)
            with self.assertRaisesRegex(gate.GateError, "symlink"):
                gate.fresh_build_directory(p)
            self.assertTrue((p / "victim").is_dir())

    def test_real_child_failure_retains_evidence_and_raises(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            with self.assertRaisesRegex(gate.GateError, "exit 7"):
                gate.run_logged([sys.executable, "-c", "import sys; print('actual failure'); sys.exit(7)"], "bad", p, p, 5)
            self.assertEqual(json.loads((p / "bad.json").read_text())["returncode"], 7)
            self.assertIn("actual failure", (p / "bad.stdout").read_text())

    def test_real_child_success_retains_output_digest(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            r = gate.run_logged([sys.executable, "-c", "print('actual success')"], "ok", p, p, 5)
            self.assertEqual(r["returncode"], 0)
            self.assertEqual(r["stdout_sha256"], gate.digest(p / "ok.stdout"))

    def test_git_identity_ignores_inherited_foreign_repository_selectors(self):
        with tempfile.TemporaryDirectory() as d:
            own, foreign = Path(d) / "own", Path(d) / "foreign"
            own.mkdir();foreign.mkdir()
            subprocess.run(["git", "init", "--quiet", str(own)], check=True)
            subprocess.run(["git", "init", "--quiet", str(foreign)], check=True)
            with patch.dict(os.environ, {"GIT_DIR": str(foreign / ".git"), "GIT_WORK_TREE": str(foreign)}):
                actual = gate.git_output(own, "rev-parse", "--show-toplevel")
            self.assertEqual(Path(actual), own)

if __name__ == "__main__":
    unittest.main()

