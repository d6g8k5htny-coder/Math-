"""Read-only, base-owned source-identity verifier for Math- PR #547.

This program is intended to run only from trusted Math- default-branch code
under pull_request_target or workflow_dispatch. It reads PR metadata, the PR
changed-file API, the base/head Git trees and the current main ref. It never
checks out, imports, executes, downloads, or interprets candidate files.

A PASS establishes only the exact source identities and path/mode boundary
listed below. It is not a security certification, test result, proof result,
or scientific acceptance.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

REPOSITORY = "d6g8k5htny-coder/Math-"
PULL_NUMBER = 547
BASE_REF = "main"
BASE_SHA = "19a55750451b8016b50d1d20be6a18c021807ecb"
BASE_TREE_SHA = "0e28d1077fffb77e66ff635a112899ccb091b3ba"
HEAD_REF = "dcl/contact-small-gap-mutant-identity-20261030"
HEAD_SHA = "aba43cce0fad06c8ed8a6f6f8e5dfc1b495ffa8b"

BASE_WORKFLOW_PATH = ".github/workflows/contact-small-gap.yml"
BASE_WORKFLOW = {
    "sha": "86cadd90ac8c68ded41e462d8c5f249780886dda",
    "size": 4164,
}
EXPECTED_HEAD_FILES = {
    ".github/workflows/contact-small-gap.yml": {
        "sha": "10e958e0026b16d84155fc2f38f6539bbf54aed1",
        "size": 7170,
    },
    "reviews/contact_kernel_tail_20260925/run_validation.py": {
        "sha": "c60624104972b5f619dfcf7c63429e573297125f",
        "size": 7061,
    },
    "reviews/contact_kernel_tail_20260925/SOURCE_FILES.json": {
        "sha": "a096b6bc5643b983ade7c9f3d02b6490e932ebab",
        "size": 1338,
    },
}

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
PER_PAGE = 100
MAX_FILE_PAGES = 30  # GitHub's list-PR-files ceiling is 3,000 entries.
MAX_TREE_ENTRIES = 100_000
MAX_RESPONSE_BYTES = 32 * 1024 * 1024
MAX_EVENT_BYTES = 1 * 1024 * 1024
ALLOWED_ROUTE = re.compile(
    r"/repos/d6g8k5htny-coder/Math-/(?:"
    r"git/ref/heads/main|pulls/547|pulls/547/files\?per_page=100&page=[1-9][0-9]*|"
    r"compare/[0-9a-f]{40}\.\.\.[0-9a-f]{40}|"
    r"git/commits/[0-9a-f]{40}|git/trees/[0-9a-f]{40}\?recursive=1)\Z"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON object key")
        result[key] = value
    return result


def reject_constant(_token: str):
    raise ValueError("non-finite JSON value")


def strict_json(raw: bytes):
    def finite_float(token: str):
        value = float(token)
        require(value not in (float("inf"), float("-inf")) and value == value,
                "non-finite JSON number")
        return value

    try:
        text = raw.decode("utf-8", errors="strict")
        return json.loads(text, object_pairs_hook=unique_object,
                          parse_constant=reject_constant, parse_float=finite_float)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid UTF-8 JSON") from exc


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class GitHubAPI:
    """GET-only GitHub API client. Redirects and oversized responses fail closed."""

    def __init__(self, token: str):
        require(isinstance(token, str) and bool(token), "read-only GitHub token missing")
        self._token = token
        self._opener = urllib.request.build_opener(NoRedirect())

    def get(self, route: str):
        require(isinstance(route, str) and ALLOWED_ROUTE.fullmatch(route) is not None,
                "API route outside the fixed read-only endpoint allowlist")
        request = urllib.request.Request(
            "https://api.github.com" + route,
            headers={
                "Authorization": "Bearer " + self._token,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "contact-small-gap-trust-read-only",
            },
            method="GET",
        )
        try:
            with self._opener.open(request, timeout=25) as response:
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            # Do not print response bodies, request headers, or credential data.
            raise ValueError(f"GitHub API GET failed with HTTP {exc.code}") from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise ValueError("GitHub API GET unavailable") from None
        require(len(raw) <= MAX_RESPONSE_BYTES, "GitHub API response exceeds size limit")
        return strict_json(raw)


def load_event(path: str):
    require(isinstance(path, str) and bool(path), "GitHub event path missing")
    try:
        raw = Path(path).read_bytes()
    except OSError:
        raise ValueError("GitHub event payload unavailable") from None
    require(len(raw) <= MAX_EVENT_BYTES, "GitHub event payload exceeds size limit")
    event = strict_json(raw)
    require(isinstance(event, dict), "GitHub event payload is not an object")
    return event


def sha40(value, message: str) -> str:
    require(isinstance(value, str) and HEX40.fullmatch(value) is not None, message)
    return value


def full_name(value, message: str) -> str:
    require(isinstance(value, dict) and value.get("full_name") == REPOSITORY, message)
    return REPOSITORY


def event_snapshot(event, env):
    """Validate the trusted event envelope and return its PR snapshot, if any."""
    require(env.get("GITHUB_REPOSITORY") == REPOSITORY, "workflow repository mismatch")
    require(env.get("GITHUB_REF") == "refs/heads/main", "workflow must run from the trusted main ref")
    workflow_sha = sha40(env.get("GITHUB_SHA"), "workflow commit SHA missing or invalid")
    full_name(event.get("repository"), "event repository mismatch")

    event_name = env.get("GITHUB_EVENT_NAME")
    if event_name == "pull_request_target":
        require(type(event.get("number")) is int and event["number"] == PULL_NUMBER,
                "event pull request number mismatch")
        pr = event.get("pull_request")
        require(isinstance(pr, dict), "pull request event snapshot missing")
        require(type(pr.get("number")) is int and pr["number"] == PULL_NUMBER,
                "event pull request number mismatch")
        base = pr.get("base")
        head = pr.get("head")
        require(isinstance(base, dict) and isinstance(head, dict),
                "event base/head snapshot missing")
        full_name(base.get("repo"), "event base repository mismatch")
        full_name(head.get("repo"), "event head repository mismatch")
        snapshot = {
            "number": PULL_NUMBER,
            "base_ref": base.get("ref"),
            "base_sha": sha40(base.get("sha"), "event base SHA invalid"),
            "head_ref": head.get("ref"),
            "head_sha": sha40(head.get("sha"), "event head SHA invalid"),
        }
        require(snapshot["base_ref"] == BASE_REF, "event base ref mismatch")
        require(snapshot["head_ref"] == HEAD_REF, "event head ref mismatch")
        require(snapshot["head_sha"] == HEAD_SHA, "event head SHA mismatch")
        require(workflow_sha == snapshot["base_sha"],
                "workflow commit does not match event base snapshot")
        return PULL_NUMBER, snapshot

    if event_name == "workflow_dispatch":
        inputs = event.get("inputs", {})
        require(isinstance(inputs, dict), "workflow-dispatch inputs malformed")
        requested = env.get("PR_NUMBER")
        payload_number = inputs.get("pr_number")
        if requested is not None:
            require(str(requested) == str(PULL_NUMBER), "manual dispatch PR number must be 547")
        if payload_number is not None:
            require(str(payload_number) == str(PULL_NUMBER), "manual dispatch payload PR number must be 547")
        require(requested is not None or payload_number is not None,
                "manual dispatch PR number missing")
        # GITHUB_SHA is checked against the live default-branch ref below.
        return PULL_NUMBER, None

    raise ValueError("unsupported workflow event")


def validate_live_pr(pr, expected_number: int, live_main_sha: str):
    require(isinstance(pr, dict), "live pull request response malformed")
    require(type(pr.get("number")) is int and pr["number"] == expected_number,
            "live pull request number mismatch")
    require(pr.get("state") == "open" and pr.get("merged_at") is None,
            "target pull request is not open and unmerged")
    base = pr.get("base")
    head = pr.get("head")
    require(isinstance(base, dict) and isinstance(head, dict),
            "live pull request base/head missing")
    full_name(base.get("repo"), "live base repository mismatch")
    full_name(head.get("repo"), "live head repository mismatch")
    require(base.get("ref") == BASE_REF, "live base ref mismatch")
    require(base.get("sha") == live_main_sha, "live PR base does not match current trusted main")
    require(head.get("ref") == HEAD_REF, "live head ref mismatch")
    require(head.get("sha") == HEAD_SHA, "live head SHA drift")
    return {
        "number": expected_number,
        "base_ref": base["ref"],
        "base_sha": base["sha"],
        "head_ref": head["ref"],
        "head_sha": head["sha"],
    }


def list_changed_files(api):
    """Read every changed-file page; fail closed at the API's 3,000-file cap."""
    rows = {}
    completed = False
    for page in range(1, MAX_FILE_PAGES + 1):
        data = api.get(f"/repos/{REPOSITORY}/pulls/{PULL_NUMBER}/files?per_page={PER_PAGE}&page={page}")
        require(isinstance(data, list), "changed-file API response is not a list")
        require(len(data) <= PER_PAGE, "changed-file API page exceeds requested size")
        for item in data:
            require(isinstance(item, dict), "changed-file entry malformed")
            path = item.get("filename")
            require(isinstance(path, str) and bool(path), "changed-file path missing")
            require(path not in rows, "duplicate changed-file path")
            rows[path] = item
        if len(data) < PER_PAGE:
            completed = True
            break
    require(completed, "changed-file API reached 3,000-file ceiling; result may be truncated")
    require(set(rows) == set(EXPECTED_HEAD_FILES), "changed-file set differs from exact three-path contract")
    for path, expected in EXPECTED_HEAD_FILES.items():
        item = rows[path]
        require(item.get("status") == "modified", "changed-file status is not modified")
        require(item.get("previous_filename") is None, "renamed path is outside the exact delta")
        require(item.get("sha") == expected["sha"], "changed-file blob identity mismatch")
    return rows


def read_tree(api, commit_sha: str, expected_tree_sha: str | None = None):
    sha40(commit_sha, "tree commit SHA invalid")
    commit = api.get(f"/repos/{REPOSITORY}/git/commits/{commit_sha}")
    require(isinstance(commit, dict) and commit.get("sha") == commit_sha
            and isinstance(commit.get("tree"), dict), "Git commit/tree metadata unavailable")
    tree_sha = sha40(commit["tree"].get("sha"), "Git commit tree SHA invalid")
    if expected_tree_sha is not None:
        require(tree_sha == expected_tree_sha, "Git commit tree identity mismatch")
    data = api.get(f"/repos/{REPOSITORY}/git/trees/{tree_sha}?recursive=1")
    require(isinstance(data, dict) and data.get("truncated") is False,
            "Git tree unavailable or truncated")
    require(data.get("sha") == tree_sha, "Git tree root identity mismatch")
    entries = data.get("tree")
    require(isinstance(entries, list) and len(entries) <= MAX_TREE_ENTRIES,
            "Git tree entries missing or excessive")
    by_path = {}
    for row in entries:
        require(isinstance(row, dict), "Git tree entry malformed")
        path = row.get("path")
        require(isinstance(path, str) and bool(path), "Git tree path missing")
        require(path not in by_path, "duplicate Git tree path")
        by_path[path] = row
    return by_path


def verify_tree_entry(tree, path: str, expected: dict, label: str):
    row = tree.get(path)
    require(isinstance(row, dict), f"{label}: required path missing")
    require(row.get("type") == "blob", f"{label}: entry is not a blob")
    require(row.get("mode") == "100644", f"{label}: entry is not a regular non-executable file")
    require(row.get("sha") == expected["sha"], f"{label}: Git blob identity mismatch")
    require(type(row.get("size")) is int and row["size"] == expected["size"],
            f"{label}: blob size mismatch")


def verify(event, env, api):
    number, snapshot = event_snapshot(event, env)
    workflow_sha = sha40(env.get("GITHUB_SHA"), "workflow commit SHA missing or invalid")

    # Confirm the workflow was checked out at the live trusted default-branch ref.
    ref_data = api.get(f"/repos/{REPOSITORY}/git/ref/heads/{BASE_REF}")
    require(isinstance(ref_data, dict) and isinstance(ref_data.get("object"), dict),
            "trusted main ref response malformed")
    live_main_sha = sha40(ref_data["object"].get("sha"), "trusted main ref SHA invalid")
    require(live_main_sha == workflow_sha, "trusted main ref moved after workflow checkout")

    live_pr = api.get(f"/repos/{REPOSITORY}/pulls/{number}")
    live_snapshot = validate_live_pr(live_pr, number, live_main_sha)
    if snapshot is not None:
        require(snapshot == live_snapshot, "event PR snapshot is stale or differs from live PR")

    comparison = api.get(f"/repos/{REPOSITORY}/compare/{live_main_sha}...{HEAD_SHA}")
    require(isinstance(comparison, dict), "base/head comparison response malformed")
    base_commit = comparison.get("base_commit")
    merge_base = comparison.get("merge_base_commit")
    require(isinstance(base_commit, dict) and base_commit.get("sha") == live_main_sha,
            "comparison base commit identity mismatch")
    require(isinstance(merge_base, dict) and merge_base.get("sha") == BASE_SHA,
            "candidate no longer descends from the pinned original base")

    list_changed_files(api)
    base_tree = read_tree(api, BASE_SHA, BASE_TREE_SHA)
    verify_tree_entry(base_tree, BASE_WORKFLOW_PATH, BASE_WORKFLOW, "trusted base workflow")
    head_tree = read_tree(api, HEAD_SHA)
    for path, expected in EXPECTED_HEAD_FILES.items():
        verify_tree_entry(head_tree, path, expected, f"candidate {path}")

    return {
        "disposition": "PASS_SCOPED_SOURCE_IDENTITY",
        "meaning": "Exact PR/event/ref/path/mode/blob identities verified; no candidate code was executed.",
        "repository": REPOSITORY,
        "pull_request": PULL_NUMBER,
        "base": {"ref": BASE_REF, "current_sha": live_main_sha,
                 "original_merge_base_sha": BASE_SHA,
                 "original_tree_sha": BASE_TREE_SHA,
                 "original_workflow_blob": BASE_WORKFLOW["sha"]},
        "head": {"ref": HEAD_REF, "sha": HEAD_SHA},
        "changed_paths": sorted(EXPECTED_HEAD_FILES),
        "candidate_blobs": {path: value["sha"] for path, value in EXPECTED_HEAD_FILES.items()},
        "scientific_effect": "NONE",
    }


def main() -> int:
    try:
        event = load_event(os.environ.get("GITHUB_EVENT_PATH", ""))
        api = GitHubAPI(os.environ.get("GH_TOKEN", ""))
        result = verify(event, os.environ, api)
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:  # fail closed; never disclose request headers or token
        message = str(exc) if isinstance(exc, (ValueError, OSError)) else "unexpected verifier failure"
        print("FAIL_CLOSED: " + message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
