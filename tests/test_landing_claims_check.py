from __future__ import annotations

import io
import json
from pathlib import Path
import subprocess
import tempfile
import types
import unittest

import tools.landing_claims_check as check


def run_git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


class LandingClaimsCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        run_git(self.root, "init")
        run_git(self.root, "config", "user.email", "test@example.com")
        run_git(self.root, "config", "user.name", "Landing Claim Test")
        (self.root / "frontiers" / "a").mkdir(parents=True)
        (self.root / "reviews").mkdir()
        (self.root / "frontiers" / "a" / "PROOF.md").write_text("# Theorem A\n")
        (self.root / "reviews" / "a.md").write_text("# Review A\n")
        self.queue_url = "https://github.com/d6g8k5htny-coder/main/issues/86"
        self._write_landing(self.queue_url, ["frontiers/a/PROOF.md"])
        run_git(self.root, "add", ".")
        run_git(self.root, "commit", "-m", "fixture")
        self.commit = run_git(self.root, "rev-parse", "HEAD")
        self.blob = run_git(self.root, "rev-parse", "HEAD:frontiers/a/PROOF.md")
        self.review_blob = run_git(self.root, "rev-parse", "HEAD:reviews/a.md")
        self.old_root = check.ROOT
        check.ROOT = self.root

    def tearDown(self):
        check.ROOT = self.old_root
        self.tmp.cleanup()

    def _write_landing(self, queue_url: str, paths: list[str]):
        rows = "\n".join(f"| Topic | [Proof]({p}) | Scope |" for p in paths)
        (self.root / "README.md").write_text(
            "# Landing\n\n"
            f"[Work queue]({queue_url})\n\n"
            "## Read a result\n\n"
            "| Topic | Proof | Review |\n|---|---|---|\n"
            f"{rows}\n\n"
            "## Run a calculation\n"
        )

    def manifest(self):
        return {
            "schema_version": 1,
            "object": "TEST",
            "repository": "d6g8k5htny-coder/Math-",
            "allowed_dispositions": ["HOLD_WITH_DOMAIN", "REVIEWED_SCOPED"],
            "live_queue": {
                "repo": "d6g8k5htny-coder/main",
                "issue": 86,
                "url": self.queue_url,
                "required_state": "open",
            },
            "claims": [{
                "claim_id": "a",
                "advertised_label": "A",
                "claim_type": "derived theorem",
                "statement_path": "frontiers/a/PROOF.md",
                "statement_heading": "Theorem A",
                "source": {"commit": self.commit, "blob": self.blob},
                "domain": "fixture domain",
                "measure": "fixture measure",
                "required_dependencies": [],
                "review": {
                    "kind": "local_file",
                    "path": "reviews/a.md",
                    "source": {"commit": self.commit, "blob": self.review_blob},
                },
                "disposition": "HOLD_WITH_DOMAIN",
                "disposition_reason": "fixture",
            }],
        }

    def test_valid_manifest_passes(self):
        report = check.validate_manifest(self.manifest(), (self.root / "README.md").read_text())
        self.assertEqual(report["claim_count"], 1)
        self.assertEqual(report["live_queue"]["issue"], 86)

    def test_missing_local_source_fails_closed(self):
        (self.root / "frontiers" / "a" / "PROOF.md").unlink()
        with self.assertRaisesRegex(check.ClaimManifestError, "missing/not regular"):
            check.validate_manifest(self.manifest(), (self.root / "README.md").read_text())

    def test_closed_or_stale_queue_link_is_rejected(self):
        self._write_landing("https://github.com/d6g8k5htny-coder/main/issues/61", ["frontiers/a/PROOF.md"])
        with self.assertRaisesRegex(check.ClaimManifestError, "Work queue"):
            check.validate_manifest(self.manifest(), (self.root / "README.md").read_text())

    def test_unmanifested_landing_claim_is_rejected(self):
        (self.root / "frontiers" / "b").mkdir()
        (self.root / "frontiers" / "b" / "PROOF.md").write_text("# B\n")
        self._write_landing(self.queue_url, ["frontiers/a/PROOF.md", "frontiers/b/PROOF.md"])
        with self.assertRaisesRegex(check.ClaimManifestError, "landing/manifest mismatch"):
            check.validate_manifest(self.manifest(), (self.root / "README.md").read_text())

    def test_positive_disposition_cannot_use_unresolved_external_dependency(self):
        manifest = self.manifest()
        manifest["claims"][0]["disposition"] = "REVIEWED_SCOPED"
        manifest["claims"][0]["required_dependencies"] = [{
            "kind": "external",
            "id": "missing-parent",
            "binding_status": "UNRESOLVED_EXTERNAL",
            "reference": "external:missing-parent",
        }]
        with self.assertRaisesRegex(check.ClaimManifestError, "positive disposition depends"):
            check.validate_manifest(manifest, (self.root / "README.md").read_text())

    def test_support_dependency_can_use_github_issue_review(self):
        manifest = self.manifest()
        manifest["claims"][0]["required_dependencies"] = [{
            "kind": "support",
            "id": "parent-source",
            "path": "frontiers/a/PROOF.md",
            "source": {"commit": self.commit, "blob": self.blob},
            "review": {
                "kind": "github_issue",
                "repo": "d6g8k5htny-coder/main",
                "number": 63,
            },
        }]
        report = check.validate_manifest(manifest, (self.root / "README.md").read_text())
        self.assertEqual(report["claim_count"], 1)

    def test_remote_queue_closed_is_rejected(self):
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return json.dumps({"state": "closed"}).encode()
        old = check.urllib.request.urlopen
        check.urllib.request.urlopen = lambda *args, **kwargs: Response()
        try:
            with self.assertRaisesRegex(check.ClaimManifestError, "is closed"):
                check.verify_issue_open(self.manifest()["live_queue"])
        finally:
            check.urllib.request.urlopen = old

    def test_current_blob_drift_is_rejected(self):
        (self.root / "frontiers" / "a" / "PROOF.md").write_text("# changed\n")
        with self.assertRaisesRegex(check.ClaimManifestError, "current landing source drift"):
            check.validate_manifest(self.manifest(), (self.root / "README.md").read_text())


if __name__ == "__main__":
    unittest.main()
