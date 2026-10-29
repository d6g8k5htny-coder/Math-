"""Real-Git source-custody contracts for the determinant gate."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[3]
DRIVER = REPOSITORY / "frontiers/determinant_moment_20261025/gate.py"

def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.STDOUT, text=True).strip()

def digest(data):
    return hashlib.sha256(data).hexdigest()

class SourceCustody(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "CBZ test")
        git(self.repo, "config", "user.email", "test@example.invalid")
        self.root = self.repo / "frontiers" / "determinant"
        self.root.mkdir(parents=True)
        self.driver = self.root / "gate.py"
        self.driver.write_bytes(DRIVER.read_bytes())
        self.proof = self.root / "Claim.lean"
        self.proof.write_text("theorem claim : True := by trivial\n")
        self.manifest = self.root / "manifest.json"
        self._write_manifest()
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "initial")
        self.initial_head = git(self.repo, "rev-parse", "HEAD")
        spec = importlib.util.spec_from_file_location("determinant_custody_test_driver", self.driver)
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)

    def _write_manifest(self):
        self.m = {"files": {"Claim.lean": digest(self.proof.read_bytes()), "gate.py": digest(self.driver.read_bytes())}}
        self.manifest.write_text(json.dumps(self.m, sort_keys=True) + "\n")

    def call_guard(self, expected_head=None):
        guard = getattr(self.gate, "source_custody", None)
        self.assertTrue(callable(guard), "source_custody guard is missing")
        return guard(self.m, digest(self.manifest.read_bytes()), expected_head=expected_head)

    def test_clean_committed_source_is_admitted(self):
        self.assertEqual(self.call_guard(expected_head=self.initial_head), self.initial_head)

    def test_dirty_refreshed_manifest_is_rejected(self):
        self.proof.write_text("theorem claim : True := by exact True.intro\n")
        self._write_manifest()
        with self.assertRaisesRegex(ValueError, "source|manifest|working"):
            self.call_guard(expected_head=self.initial_head)

    def test_staged_change_is_rejected(self):
        self.proof.write_text("theorem claim : True := by exact True.intro\n")
        self._write_manifest()
        git(self.repo, "add", ".")
        with self.assertRaisesRegex(ValueError, "index|source|manifest"):
            self.call_guard(expected_head=self.initial_head)

    def test_assume_unchanged_cannot_hide_source_bytes(self):
        git(self.repo, "update-index", "--assume-unchanged", str(self.proof.relative_to(self.repo)))
        self.proof.write_text("different\n")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "source|working"):
            self.call_guard(expected_head=self.initial_head)

    def test_skip_worktree_cannot_hide_source_bytes(self):
        git(self.repo, "update-index", "--skip-worktree", str(self.proof.relative_to(self.repo)))
        self.proof.write_text("different\n")
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "source|working"):
            self.call_guard(expected_head=self.initial_head)

    def test_head_drift_is_rejected(self):
        (self.repo / "change.txt").write_text("change\n")
        git(self.repo, "add", "change.txt")
        git(self.repo, "commit", "-qm", "new head")
        with self.assertRaisesRegex(ValueError, "HEAD|head|commit"):
            self.call_guard(expected_head=self.initial_head)

    def test_loaded_driver_substitution_is_rejected(self):
        self.driver.write_bytes(self.driver.read_bytes() + b"\n# replacement\n")
        self._write_manifest()
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-qm", "replace loaded driver")
        new_head = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "driver|loaded|identity"):
            self.call_guard(expected_head=new_head)

class DependencyCustody(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        dep = self.root / ".lake" / "packages" / "dep"
        dep.mkdir(parents=True)
        git(dep, "init", "-q")
        git(dep, "config", "user.name", "CBZ test")
        git(dep, "config", "user.email", "test@example.invalid")
        (dep / ".gitignore").write_text("*.lean\n")
        (dep / "A.lean").write_text("theorem a : True := by trivial\n")
        git(dep, "add", "-f", "A.lean")
        git(dep, "add", ".gitignore")
        git(dep, "commit", "-qm", "dependency")
        self.dep = dep
        self.m = {"dependency_revisions": {"dep": git(dep, "rev-parse", "HEAD")}}
        spec = importlib.util.spec_from_file_location("dependency_custody_test_driver", DRIVER)
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)
        self.gate.ROOT = self.root

    def test_clean_dependency_is_admitted(self):
        self.assertEqual(self.gate.dependency_state(self.m), self.m["dependency_revisions"])

    def test_assume_unchanged_dependency_source_is_rejected(self):
        git(self.dep, "update-index", "--assume-unchanged", "A.lean")
        (self.dep / "A.lean").write_text("different\n")
        self.assertEqual(git(self.dep, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "dependency.*(source|tracked|working)"):
            self.gate.dependency_state(self.m)

    def test_skip_worktree_dependency_source_is_rejected(self):
        git(self.dep, "update-index", "--skip-worktree", "A.lean")
        (self.dep / "A.lean").write_text("different\n")
        self.assertEqual(git(self.dep, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "dependency.*(source|tracked|working)"):
            self.gate.dependency_state(self.m)

    def test_ignored_untracked_lean_source_is_rejected(self):
        (self.dep / "Hidden.lean").write_text("axiom hidden : False\n")
        self.assertEqual(git(self.dep, "status", "--porcelain"), "")
        with self.assertRaisesRegex(ValueError, "dependency.*(Lean|source|untracked)"):
            self.gate.dependency_state(self.m)

if __name__ == "__main__":
    unittest.main()
