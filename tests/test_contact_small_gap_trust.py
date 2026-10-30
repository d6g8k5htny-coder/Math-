"""No-network adverse controls for the trusted Math-#547 source verifier."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "verify_contact_small_gap_trust.py"
spec = importlib.util.spec_from_file_location("contact_small_gap_trust", SCRIPT)
trust = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trust)

REPO = trust.REPOSITORY
BASE = trust.EXPECTED_MERGE_BASE
HEAD = trust.EXPECTED_HEAD
BASE_TREE = "1" * 40
HEAD_TREE = "2" * 40


def repo_object():
    return {"full_name": REPO, "id": 123456789, "fork": False, "default_branch": "main"}


def tree_rows(side):
    rows = {}
    for path, identity in trust.EXPECTED_FILES.items():
        parts = path.split("/")
        for index in range(1, len(parts)):
            parent = "/".join(parts[:index])
            rows[parent] = {"path": parent, "type": "tree", "mode": "040000", "sha": "a" * 40}
        blob = identity["base_blob"] if side == "base" else identity["head_blob"]
        size = identity["base_size"] if side == "base" else identity["head_size"]
        rows[path] = {"path": path, "type": "blob", "mode": "100644", "sha": blob, "size": size}
    return list(rows.values())


def make_pr(base_sha=BASE):
    repo = repo_object()
    return {
        "number": trust.PR_NUMBER,
        "state": "open",
        "merged": False,
        "changed_files": len(trust.EXPECTED_FILES),
        "base": {"ref": "main", "sha": base_sha, "repo": copy.deepcopy(repo)},
        "head": {"ref": trust.HEAD_REF, "sha": HEAD, "repo": copy.deepcopy(repo)},
    }


def make_event(event_name="pull_request_target", base_sha=BASE):
    event = {"repository": repo_object()}
    if event_name == "pull_request_target":
        event["pull_request"] = make_pr(base_sha)
    else:
        event["inputs"] = {"pr_number": str(trust.PR_NUMBER)}
    return event


def make_env(event_name="pull_request_target", base_sha=BASE):
    return {
        "GITHUB_REPOSITORY": REPO,
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_SHA": base_sha,
        "PR_NUMBER": str(trust.PR_NUMBER),
    }


class FakeAPI:
    def __init__(self, base_sha=BASE):
        self.pr = make_pr(base_sha)
        self.files = [
            {"filename": path, "status": "modified", "sha": identity["head_blob"]}
            for path, identity in trust.EXPECTED_FILES.items()
        ]
        self.base_tree = tree_rows("base")
        self.head_tree = tree_rows("head")
        self.base_truncated = False
        self.head_truncated = False
        self.routes = []
        self.error_route = None

    def get(self, route):
        self.routes.append(route)
        if route == self.error_route:
            raise trust.VerificationError("synthetic API error")
        if route == f"/repos/{REPO}/pulls/{trust.PR_NUMBER}":
            return copy.deepcopy(self.pr)
        if route.startswith(f"/repos/{REPO}/pulls/{trust.PR_NUMBER}/files?"):
            if "page=1" in route:
                return copy.deepcopy(self.files)
            return []
        if route == f"/repos/{REPO}/commits/{self.pr['base']['sha']}":
            return {"sha": self.pr["base"]["sha"], "commit": {"tree": {"sha": BASE_TREE}}}
        if route == f"/repos/{REPO}/commits/{HEAD}":
            return {"sha": HEAD, "commit": {"tree": {"sha": HEAD_TREE}}}
        if route == f"/repos/{REPO}/git/trees/{BASE_TREE}?recursive=1":
            return {"sha": BASE_TREE, "truncated": self.base_truncated, "tree": copy.deepcopy(self.base_tree)}
        if route == f"/repos/{REPO}/git/trees/{HEAD_TREE}?recursive=1":
            return {"sha": HEAD_TREE, "truncated": self.head_truncated, "tree": copy.deepcopy(self.head_tree)}
        if "/compare/" in route:
            return {
                "status": "identical" if self.pr["base"]["sha"] == BASE else "ahead",
                "ahead_by": 0 if self.pr["base"]["sha"] == BASE else 1,
                "behind_by": 0,
                "merge_base_commit": {"sha": BASE},
            }
        raise AssertionError("unexpected API route: " + route)


class VerifierTests(unittest.TestCase):
    def run_verify(self, event_name="pull_request_target", event=None, env=None, api=None):
        api = api or FakeAPI()
        event = event if event is not None else make_event(event_name)
        env = env if env is not None else make_env(event_name)
        return trust.verify(event_name, event, env, api)

    def test_pull_request_target_positive(self):
        result = self.run_verify()
        self.assertEqual(result["disposition"], "PASS_SCOPED_SOURCE_IDENTITY")
        self.assertEqual(result["candidate_head_sha"], HEAD)
        self.assertEqual(set(result["changed_paths"]), set(trust.EXPECTED_FILES))

    def test_manual_dispatch_positive_after_unrelated_base_advance(self):
        advanced = "b" * 40
        api = FakeAPI(base_sha=advanced)
        result = self.run_verify(
            "workflow_dispatch", make_event("workflow_dispatch", advanced), make_env("workflow_dispatch", advanced), api
        )
        self.assertEqual(result["trusted_base_sha"], advanced)

    def test_stale_event_head_rejected(self):
        event = make_event()
        event["pull_request"]["head"]["sha"] = "c" * 40
        with self.assertRaises(trust.VerificationError):
            self.run_verify(event=event)

    def test_live_head_drift_rejected(self):
        api = FakeAPI()
        api.pr["head"]["sha"] = "c" * 40
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_event_pr_rejected(self):
        event = make_event()
        event["pull_request"]["number"] = 548
        with self.assertRaises(trust.VerificationError):
            self.run_verify(event=event)

    def test_wrong_live_pr_rejected(self):
        api = FakeAPI()
        api.pr["number"] = 548
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_event_repository_rejected(self):
        event = make_event()
        event["repository"]["full_name"] = "attacker/Math-"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(event=event)

    def test_wrong_base_ref_rejected(self):
        api = FakeAPI()
        api.pr["base"]["ref"] = "release"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_head_ref_rejected(self):
        api = FakeAPI()
        api.pr["head"]["ref"] = "attacker-branch"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_fork_head_rejected(self):
        api = FakeAPI()
        api.pr["head"]["repo"]["full_name"] = "attacker/Math-"
        api.pr["head"]["repo"]["id"] = 1
        api.pr["head"]["repo"]["fork"] = True
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_trusted_ref_rejected(self):
        env = make_env()
        env["GITHUB_REF"] = "refs/heads/feature"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(env=env)

    def test_extra_changed_path_rejected(self):
        api = FakeAPI()
        api.files.append({"filename": "extra.txt", "status": "modified", "sha": "d" * 40})
        api.pr["changed_files"] += 1
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_missing_changed_path_rejected(self):
        api = FakeAPI()
        api.files.pop()
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_duplicate_changed_path_rejected(self):
        api = FakeAPI()
        api.files.append(copy.deepcopy(api.files[0]))
        api.pr["changed_files"] += 1
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_renamed_changed_path_rejected(self):
        api = FakeAPI()
        api.files[0]["previous_filename"] = "old-name.yml"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_truncated_base_tree_rejected(self):
        api = FakeAPI()
        api.base_truncated = True
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_truncated_head_tree_rejected(self):
        api = FakeAPI()
        api.head_truncated = True
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_missing_tree_path_rejected(self):
        api = FakeAPI()
        api.head_tree = [row for row in api.head_tree if row.get("path") != ".github/workflows/contact-small-gap.yml"]
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_symlink_mode_rejected(self):
        api = FakeAPI()
        for row in api.head_tree:
            if row.get("path") == ".github/workflows/contact-small-gap.yml":
                row["mode"] = "120000"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_tree_mode_at_file_path_rejected(self):
        api = FakeAPI()
        for row in api.head_tree:
            if row.get("path") == ".github/workflows/contact-small-gap.yml":
                row["type"] = "tree"
                row["mode"] = "040000"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_symlink_parent_rejected(self):
        api = FakeAPI()
        for row in api.head_tree:
            if row.get("path") == ".github/workflows":
                row["type"] = "blob"
                row["mode"] = "120000"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_candidate_blob_rejected(self):
        api = FakeAPI()
        for row in api.head_tree:
            if row.get("path") == ".github/workflows/contact-small-gap.yml":
                row["sha"] = "d" * 40
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_candidate_size_rejected(self):
        api = FakeAPI()
        for row in api.head_tree:
            if row.get("path") == ".github/workflows/contact-small-gap.yml":
                row["size"] += 1
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_wrong_base_blob_rejected(self):
        api = FakeAPI()
        for row in api.base_tree:
            if row.get("path") == ".github/workflows/contact-small-gap.yml":
                row["sha"] = "d" * 40
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_api_error_rejected(self):
        api = FakeAPI()
        api.error_route = f"/repos/{REPO}/pulls/{trust.PR_NUMBER}"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_manual_dispatch_wrong_pr_rejected(self):
        event = make_event("workflow_dispatch")
        event["inputs"]["pr_number"] = "548"
        with self.assertRaises(trust.VerificationError):
            self.run_verify("workflow_dispatch", event, make_env("workflow_dispatch"), FakeAPI())

    def test_event_live_changed_file_count_mismatch_rejected(self):
        event = make_event()
        event["pull_request"]["changed_files"] = 4
        with self.assertRaises(trust.VerificationError):
            self.run_verify(event=event)

    def test_event_live_state_mismatch_rejected(self):
        event = make_event()
        event["pull_request"]["state"] = "closed"
        with self.assertRaises(trust.VerificationError):
            self.run_verify(event=event)

    def test_base_source_drift_after_base_advance_rejected(self):
        api = FakeAPI(base_sha="b" * 40)
        for row in api.base_tree:
            if row.get("path") == ".github/workflows/contact-small-gap.yml":
                row["sha"] = "d" * 40
        with self.assertRaises(trust.VerificationError):
            self.run_verify("workflow_dispatch", make_event("workflow_dispatch", "b" * 40), make_env("workflow_dispatch", "b" * 40), api)

    def test_changed_file_api_blob_mismatch_rejected(self):
        api = FakeAPI()
        api.files[0]["sha"] = "d" * 40
        with self.assertRaises(trust.VerificationError):
            self.run_verify(api=api)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaises(trust.VerificationError):
            trust.strict_json(b'{"a":1,"a":2}')

    def test_nonfinite_json_rejected(self):
        with self.assertRaises(trust.VerificationError):
            trust.strict_json(b'{"a":NaN}')

    def test_malformed_json_rejected(self):
        with self.assertRaises(trust.VerificationError):
            trust.strict_json(b'{')

    def test_no_redirect_handler_rejects_redirect(self):
        handler = trust.NoRedirect()
        request = urllib.request.Request("https://api.github.com/repos/example/repo")
        with self.assertRaises(trust.VerificationError):
            handler.redirect_request(request, None, 302, "Found", {}, "https://example.org")

    def test_api_requests_are_get_only(self):
        class Response:
            status = 200
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size): return b'{"ok":true}'
        class Opener:
            def __init__(self): self.methods = []
            def open(self, request, timeout):
                self.methods.append(request.get_method())
                return Response()
        opener = Opener()
        api = trust.GitHubAPI("test-token", opener=opener)
        self.assertEqual(api.get(f"/repos/{REPO}/pulls/547"), {"ok": True})
        self.assertEqual(api.get(f"/repos/{REPO}/compare/{BASE}...{HEAD}?per_page=1"), {"ok": True})
        self.assertEqual(opener.methods, ["GET", "GET"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
