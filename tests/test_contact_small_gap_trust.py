"""Adverse controls for the base-owned, read-only contact-small-gap verifier."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".github" / "scripts"))
import verify_contact_small_gap_trust as verifier  # noqa: E402


class FakeAPI:
    def __init__(self):
        self.pr = {
            "number": verifier.PULL_NUMBER,
            "state": "open",
            "merged_at": None,
            "base": {"ref": verifier.BASE_REF, "sha": "9" * 40,
                     "repo": {"full_name": verifier.REPOSITORY}},
            "head": {"ref": verifier.HEAD_REF, "sha": verifier.HEAD_SHA,
                     "repo": {"full_name": verifier.REPOSITORY}},
        }
        self.main_sha = "9" * 40
        self.pr["base"]["sha"] = self.main_sha
        self.pages = [[
            {"filename": path, "status": "modified", "sha": value["sha"]}
            for path, value in verifier.EXPECTED_HEAD_FILES.items()
        ]]
        self.base_tree = {
            verifier.BASE_WORKFLOW_PATH: {
                "path": verifier.BASE_WORKFLOW_PATH, "mode": "100644", "type": "blob",
                "sha": verifier.BASE_WORKFLOW["sha"], "size": verifier.BASE_WORKFLOW["size"],
            }
        }
        self.head_tree = {
            path: {"path": path, "mode": "100644", "type": "blob",
                   "sha": value["sha"], "size": value["size"]}
            for path, value in verifier.EXPECTED_HEAD_FILES.items()
        }
        self.truncated = False
        self.head_tree_sha = "7" * 40

    def get(self, route):
        if route == f"/repos/{verifier.REPOSITORY}/git/ref/heads/main":
            return {"object": {"sha": self.main_sha}}
        if route == f"/repos/{verifier.REPOSITORY}/compare/{self.main_sha}...{verifier.HEAD_SHA}":
            return {"base_commit": {"sha": self.main_sha},
                    "merge_base_commit": {"sha": verifier.BASE_SHA}}
        if route == f"/repos/{verifier.REPOSITORY}/pulls/{verifier.PULL_NUMBER}":
            return copy.deepcopy(self.pr)
        prefix = f"/repos/{verifier.REPOSITORY}/pulls/{verifier.PULL_NUMBER}/files?per_page=100&page="
        if route.startswith(prefix):
            page = int(route[len(prefix):])
            return copy.deepcopy(self.pages[page - 1] if page <= len(self.pages) else [])
        if route == f"/repos/{verifier.REPOSITORY}/git/commits/{verifier.BASE_SHA}":
            return {"sha": verifier.BASE_SHA, "tree": {"sha": verifier.BASE_TREE_SHA}}
        if route == f"/repos/{verifier.REPOSITORY}/git/commits/{verifier.HEAD_SHA}":
            return {"sha": verifier.HEAD_SHA, "tree": {"sha": self.head_tree_sha}}
        if route == f"/repos/{verifier.REPOSITORY}/git/trees/{verifier.BASE_TREE_SHA}?recursive=1":
            return {"sha": verifier.BASE_TREE_SHA, "truncated": self.truncated,
                    "tree": list(copy.deepcopy(self.base_tree).values())}
        if route == f"/repos/{verifier.REPOSITORY}/git/trees/{self.head_tree_sha}?recursive=1":
            return {"sha": self.head_tree_sha, "truncated": self.truncated,
                    "tree": list(copy.deepcopy(self.head_tree).values())}
        raise AssertionError("unexpected API route: " + route)


def pr_event():
    return {
        "repository": {"full_name": verifier.REPOSITORY},
        "number": verifier.PULL_NUMBER,
        "pull_request": {
            "number": verifier.PULL_NUMBER,
            "base": {"ref": verifier.BASE_REF, "sha": "9" * 40,
                     "repo": {"full_name": verifier.REPOSITORY}},
            "head": {"ref": verifier.HEAD_REF, "sha": verifier.HEAD_SHA,
                     "repo": {"full_name": verifier.REPOSITORY}},
        },
    }


def pr_env():
    return {
        "GITHUB_REPOSITORY": verifier.REPOSITORY,
        "GITHUB_EVENT_NAME": "pull_request_target",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_SHA": "9" * 40,
    }


def dispatch_event():
    return {"repository": {"full_name": verifier.REPOSITORY},
            "inputs": {"pr_number": "547"}}


def dispatch_env():
    return {
        "GITHUB_REPOSITORY": verifier.REPOSITORY,
        "GITHUB_EVENT_NAME": "workflow_dispatch",
        "GITHUB_REF": "refs/heads/main",
        "GITHUB_SHA": "9" * 40,
        "PR_NUMBER": "547",
    }


class TrustVerifierTests(unittest.TestCase):
    def setUp(self):
        self.api = FakeAPI()
        self.event = pr_event()
        self.env = pr_env()

    def assert_rejected(self, event=None, env=None, api=None):
        with self.assertRaises(ValueError):
            verifier.verify(event if event is not None else self.event,
                            env if env is not None else self.env,
                            api if api is not None else self.api)

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(ValueError):
            verifier.strict_json(b'{"number":547,"number":548}')

    def test_nonfinite_json_number_rejected(self):
        with self.assertRaises(ValueError):
            verifier.strict_json(b'{"value":1e999}')

    def test_api_route_allowlist_rejects_unexpected_path(self):
        client = verifier.GitHubAPI("test-token")
        with self.assertRaises(ValueError):
            client.get(f"/repos/{verifier.REPOSITORY}/contents/README.md")

    def test_exact_pull_request_target_snapshot_passes(self):
        result = verifier.verify(self.event, self.env, self.api)
        self.assertEqual(result["disposition"], "PASS_SCOPED_SOURCE_IDENTITY")
        self.assertEqual(result["scientific_effect"], "NONE")

    def test_manual_dispatch_reads_same_live_pr(self):
        result = verifier.verify(dispatch_event(), dispatch_env(), self.api)
        self.assertEqual(result["pull_request"], 547)

    def test_default_branch_can_advance_without_changing_original_merge_base(self):
        result = verifier.verify(self.event, self.env, self.api)
        self.assertEqual(result["base"]["original_merge_base_sha"], verifier.BASE_SHA)
        self.assertEqual(result["base"]["current_sha"], self.api.main_sha)

    def test_stale_event_head_rejected(self):
        event = copy.deepcopy(self.event)
        event["pull_request"]["head"]["sha"] = "a" * 40
        self.assert_rejected(event=event)

    def test_wrong_event_pull_number_rejected(self):
        event = copy.deepcopy(self.event)
        event["number"] = 548
        self.assert_rejected(event=event)

    def test_wrong_event_repository_rejected(self):
        event = copy.deepcopy(self.event)
        event["repository"]["full_name"] = "attacker/Math-"
        self.assert_rejected(event=event)

    def test_wrong_event_base_ref_rejected(self):
        event = copy.deepcopy(self.event)
        event["pull_request"]["base"]["ref"] = "release"
        self.assert_rejected(event=event)

    def test_wrong_event_head_ref_rejected(self):
        event = copy.deepcopy(self.event)
        event["pull_request"]["head"]["ref"] = "attacker-branch"
        self.assert_rejected(event=event)

    def test_fork_head_rejected(self):
        event = copy.deepcopy(self.event)
        event["pull_request"]["head"]["repo"]["full_name"] = "attacker/Math-"
        self.assert_rejected(event=event)

    def test_live_pr_fork_head_rejected(self):
        self.api.pr["head"]["repo"]["full_name"] = "attacker/Math-"
        self.assert_rejected()

    def test_live_pr_head_drift_rejected(self):
        self.api.pr["head"]["sha"] = "b" * 40
        self.assert_rejected()

    def test_live_pr_base_drift_rejected(self):
        self.api.pr["base"]["sha"] = "c" * 40
        self.assert_rejected()

    def test_closed_pr_rejected(self):
        self.api.pr["state"] = "closed"
        self.assert_rejected()

    def test_merged_pr_rejected(self):
        self.api.pr["merged_at"] = "2026-10-30T00:00:00Z"
        self.assert_rejected()

    def test_manual_dispatch_payload_must_match_environment(self):
        event = dispatch_event()
        event["inputs"]["pr_number"] = "548"
        self.assert_rejected(event=event, env=dispatch_env())

    def test_wrong_manual_dispatch_ref_rejected(self):
        env = dispatch_env()
        env["GITHUB_REF"] = "refs/heads/untrusted"
        self.assert_rejected(event=dispatch_event(), env=env)

    def test_wrong_manual_dispatch_number_rejected(self):
        env = dispatch_env()
        env["PR_NUMBER"] = "548"
        self.assert_rejected(event=dispatch_event(), env=env)

    def test_wrong_merge_base_rejected(self):
        original_get = self.api.get
        def changed(route):
            value = original_get(route)
            if route.startswith(f"/repos/{verifier.REPOSITORY}/compare/"):
                value["merge_base_commit"]["sha"] = "8" * 40
            return value
        self.api.get = changed
        self.assert_rejected()

    def test_moved_default_branch_ref_rejected(self):
        self.api.main_sha = "d" * 40
        self.env["GITHUB_SHA"] = verifier.BASE_SHA
        self.assert_rejected()

    def test_extra_changed_path_rejected(self):
        self.api.pages[0].append({"filename": "unexpected.txt", "status": "added", "sha": "e" * 40})
        self.assert_rejected()

    def test_missing_changed_path_rejected(self):
        self.api.pages[0].pop()
        self.assert_rejected()

    def test_duplicate_changed_path_rejected(self):
        self.api.pages[0].append(copy.deepcopy(self.api.pages[0][0]))
        self.assert_rejected()

    def test_wrong_changed_file_blob_rejected(self):
        self.api.pages[0][0]["sha"] = "f" * 40
        self.assert_rejected()

    def test_changed_file_pagination_reaches_3000_ceiling_rejected(self):
        self.api.pages = [[{"filename": f"x/{i}", "status": "modified", "sha": "1" * 40}
                           for i in range(verifier.PER_PAGE)] for _ in range(verifier.MAX_FILE_PAGES)]
        self.assert_rejected()

    def test_wrong_base_tree_root_rejected(self):
        original_get = self.api.get
        def changed(route):
            value = original_get(route)
            if route == f"/repos/{verifier.REPOSITORY}/git/trees/{verifier.BASE_TREE_SHA}?recursive=1":
                value["sha"] = "6" * 40
            return value
        self.api.get = changed
        self.assert_rejected()

    def test_truncated_base_tree_rejected(self):
        self.api.truncated = True
        self.assert_rejected()

    def test_missing_candidate_tree_path_rejected(self):
        self.api.head_tree.pop(next(iter(self.api.head_tree)))
        self.assert_rejected()

    def test_symlink_mode_rejected(self):
        path = next(iter(self.api.head_tree))
        self.api.head_tree[path]["mode"] = "120000"
        self.assert_rejected()

    def test_executable_mode_rejected(self):
        path = next(iter(self.api.head_tree))
        self.api.head_tree[path]["mode"] = "100755"
        self.assert_rejected()

    def test_wrong_candidate_blob_rejected(self):
        path = next(iter(self.api.head_tree))
        self.api.head_tree[path]["sha"] = "2" * 40
        self.assert_rejected()

    def test_wrong_candidate_size_rejected(self):
        path = next(iter(self.api.head_tree))
        self.api.head_tree[path]["size"] += 1
        self.assert_rejected()

    def test_wrong_base_workflow_blob_rejected(self):
        self.api.base_tree[verifier.BASE_WORKFLOW_PATH]["sha"] = "3" * 40
        self.assert_rejected()

    def test_base_workflow_symlink_rejected(self):
        self.api.base_tree[verifier.BASE_WORKFLOW_PATH]["mode"] = "120000"
        self.assert_rejected()

    def test_non_modified_changed_file_status_rejected(self):
        self.api.pages[0][0]["status"] = "renamed"
        self.assert_rejected()

    def test_non_pr_event_rejected(self):
        env = dict(self.env)
        env["GITHUB_EVENT_NAME"] = "push"
        self.assert_rejected(env=env)

    def test_event_snapshot_must_match_live_pr(self):
        self.api.pr["head"]["sha"] = "4" * 40
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()
