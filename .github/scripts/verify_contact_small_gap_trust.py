"""Read-only source-identity check for the exact Math-#547 candidate.

This verifier runs only from trusted base-branch code. It never checks out,
imports, executes, downloads or interprets candidate files. A PASS establishes
only the pinned PR/path/tree identity described below; it is not a review,
security certification, proof result or scientific acceptance.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
import urllib.error
import urllib.request

REPOSITORY = "d6g8k5htny-coder/Math-"
EXPECTED_REPOSITORY_ID = 1385716596
PR_NUMBER = 547
HEAD_REF = "dcl/contact-small-gap-mutant-identity-20261030"
EXPECTED_MERGE_BASE = "19a55750451b8016b50d1d20be6a18c021807ecb"
EXPECTED_HEAD = "aba43cce0fad06c8ed8a6f6f8e5dfc1b495ffa8b"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_TREE_ENTRIES = 100_000
MAX_FILE_PAGES = 30
PAGE_SIZE = 100

# These are the exact base/head Git blob identities observed for PR #547.
# Base identities must remain present in the live base tree; head identities
# must remain present in the candidate tree. No candidate bytes are fetched.
EXPECTED_FILES = {
    ".github/workflows/contact-small-gap.yml": {
        "base_blob": "86cadd90ac8c68ded41e462d8c5f249780886dda",
        "base_size": 4164,
        "head_blob": "10e958e0026b16d84155fc2f38f6539bbf54aed1",
        "head_size": 7170,
    },
    "reviews/contact_kernel_tail_20260925/SOURCE_FILES.json": {
        "base_blob": "0f73583343b98ec78cd20ad90b2a4935ea2b34fe",
        "base_size": 1338,
        "head_blob": "a096b6bc5643b983ade7c9f3d02b6490e932ebab",
        "head_size": 1338,
    },
    "reviews/contact_kernel_tail_20260925/run_validation.py": {
        "base_blob": "97dbbe04417655b527db287fd12e97a41cc6db35",
        "base_size": 3914,
        "head_blob": "c60624104972b5f619dfcf7c63429e573297125f",
        "head_size": 7061,
    },
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON object key")
        result[key] = value
    return result


def reject_constant(_token):
    raise VerificationError("non-finite JSON constant")


def finite_float(token: str) -> float:
    value = float(token)
    require(math.isfinite(value), "non-finite JSON number")
    return value


def strict_json(raw: bytes):
    require(isinstance(raw, bytes), "JSON input must be bytes")
    try:
        text = raw.decode("utf-8", errors="strict")
        return json.loads(
            text,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except VerificationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        raise VerificationError("malformed JSON") from exc


def sha40(value, message: str) -> str:
    require(isinstance(value, str) and HEX40.fullmatch(value) is not None, message)
    return value


def exact_int(value, message: str) -> int:
    require(type(value) is int and value >= 0, message)
    return value


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise VerificationError("API redirect refused")


class GitHubAPI:
    """GET-only GitHub REST client. Redirects and oversized responses fail closed."""

    def __init__(self, token: str, opener=None):
        require(isinstance(token, str) and bool(token), "read-only GitHub token missing")
        self._token = token
        self._opener = opener if opener is not None else urllib.request.build_opener(NoRedirect())

    def get(self, route: str):
        path = route.split("?", 1)[0] if isinstance(route, str) else ""
        segments = path.split("/")
        require(
            isinstance(route, str)
            and route.startswith(f"/repos/{REPOSITORY}/")
            and not any(ch in route for ch in ("\r", "\n", "#", "\\", " "))
            and all(segment not in (".", "..") for segment in segments),
            "invalid fixed-repository API route",
        )
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
            with self._opener.open(request, timeout=20) as response:
                require(getattr(response, "status", 200) == 200, "unexpected API status")
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except VerificationError:
            raise
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError) as exc:
            raise VerificationError("GitHub API request failed") from exc
        require(len(raw) <= MAX_RESPONSE_BYTES, "API response exceeds size limit")
        return strict_json(raw)


def repo_identity(value, label: str) -> int:
    require(isinstance(value, dict), f"{label} repository missing")
    require(value.get("full_name") == REPOSITORY, f"{label} repository mismatch")
    repo_id = value.get("id")
    require(type(repo_id) is int and repo_id == EXPECTED_REPOSITORY_ID,
            f"{label} canonical repository ID mismatch")
    require(value.get("fork") is False, f"{label} fork repository refused")
    return repo_id


def event_snapshot(event_name: str, event: dict, env: dict) -> tuple[int, str | None, int]:
    require(event_name in ("pull_request_target", "workflow_dispatch"), "unsupported event")
    require(env.get("GITHUB_REPOSITORY") == REPOSITORY, "workflow repository mismatch")
    require(env.get("GITHUB_REF") == "refs/heads/main", "workflow must run from trusted main")
    trusted_sha = sha40(env.get("GITHUB_SHA"), "trusted workflow SHA missing")
    repo = event.get("repository") if isinstance(event, dict) else None
    event_repo_id = repo_identity(repo, "event")
    require(repo.get("default_branch") == "main", "event default branch mismatch")

    try:
        supplied_number = int(str(env.get("PR_NUMBER", "")), 10)
    except (TypeError, ValueError) as exc:
        raise VerificationError("PR number input invalid") from exc
    require(supplied_number == PR_NUMBER, "unexpected PR number input")

    if event_name == "pull_request_target":
        snapshot = event.get("pull_request")
        require(isinstance(snapshot, dict), "pull_request event snapshot missing")
        require(snapshot.get("number") == PR_NUMBER, "event PR number mismatch")
        require(snapshot.get("state") == "open" and snapshot.get("merged") is False,
                "event PR state is not open")
        require(exact_int(snapshot.get("changed_files"), "event changed_files invalid") == len(EXPECTED_FILES),
                "event changed-file count mismatch")
        base = snapshot.get("base")
        head = snapshot.get("head")
        require(isinstance(base, dict) and isinstance(head, dict), "event base/head missing")
        require(base.get("ref") == "main", "event base ref mismatch")
        require(head.get("ref") == HEAD_REF, "event head ref mismatch")
        event_base_sha = sha40(base.get("sha"), "event base SHA invalid")
        event_head_sha = sha40(head.get("sha"), "event head SHA invalid")
        require(event_base_sha == trusted_sha, "stale event base SHA")
        require(event_head_sha == EXPECTED_HEAD, "stale or unexpected event head SHA")
        base_repo_id = repo_identity(base.get("repo"), "event base")
        head_repo_id = repo_identity(head.get("repo"), "event head")
        require(base_repo_id == head_repo_id == event_repo_id, "event head is not same-repository")
        return supplied_number, event_head_sha, event_repo_id

    inputs = event.get("inputs")
    require(isinstance(inputs, dict), "manual dispatch inputs missing")
    try:
        input_number = int(str(inputs.get("pr_number", "")), 10)
    except (TypeError, ValueError) as exc:
        raise VerificationError("manual dispatch PR number invalid") from exc
    require(input_number == PR_NUMBER == supplied_number, "manual dispatch PR mismatch")
    return supplied_number, None, event_repo_id


def pr_snapshot(pr: dict) -> tuple:
    require(isinstance(pr, dict), "live PR response missing")
    require(pr.get("number") == PR_NUMBER, "live PR number mismatch")
    require(pr.get("state") == "open" and pr.get("merged") is False, "target PR is not open")
    base = pr.get("base")
    head = pr.get("head")
    require(isinstance(base, dict) and isinstance(head, dict), "live PR base/head missing")
    require(base.get("ref") == "main", "live PR base ref mismatch")
    require(head.get("ref") == HEAD_REF, "live PR head ref mismatch")
    base_sha = sha40(base.get("sha"), "live PR base SHA invalid")
    head_sha = sha40(head.get("sha"), "live PR head SHA invalid")
    require(head_sha == EXPECTED_HEAD, "live PR head drift")
    base_repo_id = repo_identity(base.get("repo"), "live PR base")
    head_repo_id = repo_identity(head.get("repo"), "live PR head")
    require(base_repo_id == head_repo_id, "live PR fork/head repository refused")
    return (
        pr.get("number"), pr.get("state"), pr.get("merged"),
        base.get("ref"), base_sha, base_repo_id,
        head.get("ref"), head_sha, head_repo_id,
        exact_int(pr.get("changed_files"), "live PR changed_files invalid"),
    )


def require_event_pr_matches_live(event_pr: dict, pr: dict) -> None:
    require(isinstance(event_pr, dict), "event PR snapshot missing")
    require(event_pr.get("number") == pr.get("number") == PR_NUMBER,
            "event/live PR number mismatch")
    require(event_pr.get("state") == pr.get("state"), "event/live PR state mismatch")
    require(event_pr.get("merged") == pr.get("merged"), "event/live merged state mismatch")
    require(event_pr.get("changed_files") == pr.get("changed_files"),
            "event/live changed-file count mismatch")
    event_base = event_pr.get("base")
    event_head = event_pr.get("head")
    live_base = pr.get("base")
    live_head = pr.get("head")
    require(all(isinstance(x, dict) for x in (event_base, event_head, live_base, live_head)),
            "event/live PR base/head missing")
    require(event_base.get("ref") == live_base.get("ref"), "event/live base ref mismatch")
    require(event_base.get("sha") == live_base.get("sha"), "event/live base SHA mismatch")
    require(event_head.get("ref") == live_head.get("ref"), "event/live head ref mismatch")
    require(event_head.get("sha") == live_head.get("sha"), "event/live head SHA mismatch")
    require(repo_identity(event_base.get("repo"), "event base") ==
            repo_identity(live_base.get("repo"), "live base"),
            "event/live base repository mismatch")
    require(repo_identity(event_head.get("repo"), "event head") ==
            repo_identity(live_head.get("repo"), "live head"),
            "event/live head repository mismatch")


def compare_merge_base(api: GitHubAPI, base_sha: str, head_sha: str, *, require_base_ancestor=False) -> None:
    route = f"/repos/{REPOSITORY}/compare/{base_sha}...{head_sha}?per_page=1"
    data = api.get(route)
    require(isinstance(data, dict), "compare response missing")
    merge = data.get("merge_base_commit")
    require(isinstance(merge, dict), "merge base missing")
    require(sha40(merge.get("sha"), "merge-base SHA invalid") == EXPECTED_MERGE_BASE,
            "unexpected merge base")
    if require_base_ancestor:
        require(exact_int(data.get("behind_by"), "compare behind_by invalid") == 0,
                "expected base is not an ancestor")
        require(data.get("status") in ("ahead", "identical"), "base ancestry status invalid")


def changed_files(api: GitHubAPI, pr: dict) -> dict:
    count = exact_int(pr.get("changed_files"), "changed file count invalid")
    require(count == len(EXPECTED_FILES), "unexpected changed file count")
    rows = []
    for page in range(1, MAX_FILE_PAGES + 1):
        batch = api.get(f"/repos/{REPOSITORY}/pulls/{PR_NUMBER}/files?per_page={PAGE_SIZE}&page={page}")
        require(isinstance(batch, list), "changed-file page is not a list")
        rows.extend(batch)
        if len(batch) < PAGE_SIZE:
            break
    else:
        raise VerificationError("changed-file pagination limit reached")
    require(len(rows) == count, "changed-file pagination incomplete or truncated")

    observed = {}
    for row in rows:
        require(isinstance(row, dict), "changed-file entry malformed")
        path = row.get("filename")
        require(isinstance(path, str) and path not in observed, "missing or duplicate changed path")
        require(row.get("status") == "modified", "changed path is not a modification")
        require("previous_filename" not in row, "renamed path refused")
        observed[path] = sha40(row.get("sha"), "changed-file blob SHA invalid")
    require(set(observed) == set(EXPECTED_FILES), "changed path set mismatch")
    for path, identity in EXPECTED_FILES.items():
        require(observed[path] == identity["head_blob"], f"changed-file blob mismatch: {path}")
    return observed


def commit_tree(api: GitHubAPI, commit_sha: str) -> str:
    data = api.get(f"/repos/{REPOSITORY}/commits/{commit_sha}")
    require(isinstance(data, dict) and sha40(data.get("sha"), "commit response SHA invalid") == commit_sha,
            "commit identity mismatch")
    commit = data.get("commit")
    require(isinstance(commit, dict) and isinstance(commit.get("tree"), dict), "commit tree missing")
    return sha40(commit["tree"].get("sha"), "commit tree SHA invalid")


def tree_entries(api: GitHubAPI, tree_sha: str, label: str) -> dict:
    data = api.get(f"/repos/{REPOSITORY}/git/trees/{tree_sha}?recursive=1")
    require(isinstance(data, dict), f"{label} tree response missing")
    require(sha40(data.get("sha"), f"{label} tree SHA invalid") == tree_sha, f"{label} tree identity mismatch")
    require(data.get("truncated") is False, f"{label} tree is truncated")
    entries = data.get("tree")
    require(isinstance(entries, list) and len(entries) <= MAX_TREE_ENTRIES, f"{label} tree entries unavailable")
    result = {}
    for row in entries:
        require(isinstance(row, dict), f"{label} tree entry malformed")
        path = row.get("path")
        require(isinstance(path, str) and bool(path) and path not in result, f"{label} tree path missing or duplicate")
        result[path] = row
    return result


def verify_tree_path(entries: dict, path: str, expected_blob: str, expected_size: int, label: str) -> None:
    parts = path.split("/")
    for index in range(1, len(parts)):
        parent = "/".join(parts[:index])
        row = entries.get(parent)
        require(isinstance(row, dict), f"{label} parent path missing: {parent}")
        require(row.get("type") == "tree" and row.get("mode") == "040000",
                f"{label} parent is not a real tree: {parent}")
    row = entries.get(path)
    require(isinstance(row, dict), f"{label} path missing: {path}")
    require(row.get("type") == "blob" and row.get("mode") == "100644",
            f"{label} path is not a regular non-executable blob: {path}")
    require(sha40(row.get("sha"), f"{label} blob SHA invalid: {path}") == expected_blob,
            f"{label} blob identity mismatch: {path}")
    require(exact_int(row.get("size"), f"{label} blob size invalid: {path}") == expected_size,
            f"{label} blob size mismatch: {path}")


def verify(event_name: str, event: dict, env: dict, api: GitHubAPI) -> dict:
    number, event_head_sha, event_repo_id = event_snapshot(event_name, event, env)
    pr = api.get(f"/repos/{REPOSITORY}/pulls/{number}")
    snapshot = pr_snapshot(pr)
    live_base_sha = snapshot[4]
    live_head_sha = snapshot[7]
    require(snapshot[5] == snapshot[8] == event_repo_id, "live PR repository differs from event repository")
    require(live_base_sha == sha40(env.get("GITHUB_SHA"), "trusted workflow SHA missing"),
            "live PR base differs from trusted workflow commit")
    if event_head_sha is not None:
        require(event_head_sha == live_head_sha, "stale event/live PR head mismatch")
        require_event_pr_matches_live(event["pull_request"], pr)

    # The trusted base may advance when this verifier is integrated. It must
    # remain descended from the original merge base, and the three affected
    # base-tree entries must remain byte-identical to their recorded base blobs.
    compare_merge_base(api, EXPECTED_MERGE_BASE, live_base_sha, require_base_ancestor=True)
    compare_merge_base(api, EXPECTED_MERGE_BASE, live_head_sha, require_base_ancestor=True)
    compare_merge_base(api, live_base_sha, live_head_sha)

    changed = changed_files(api, pr)
    base_tree_sha = commit_tree(api, live_base_sha)
    head_tree_sha = commit_tree(api, live_head_sha)
    base_tree = tree_entries(api, base_tree_sha, "base")
    head_tree = tree_entries(api, head_tree_sha, "head")
    for path, identity in EXPECTED_FILES.items():
        verify_tree_path(base_tree, path, identity["base_blob"], identity["base_size"], "base")
        verify_tree_path(head_tree, path, identity["head_blob"], identity["head_size"], "head")

    # Re-read the PR only after every compare, file-list and tree request. A
    # mid-run change to the PR snapshot must not leave a stale PASS behind.
    final_pr = api.get(f"/repos/{REPOSITORY}/pulls/{number}")
    final_snapshot = pr_snapshot(final_pr)
    require(final_snapshot == snapshot, "live PR snapshot changed during verification")
    require(final_snapshot[5] == final_snapshot[8] == event_repo_id,
            "final PR repository differs from event repository")
    require(final_snapshot[4] == sha40(env.get("GITHUB_SHA"), "trusted workflow SHA missing"),
            "final PR base differs from trusted workflow commit")
    if event_head_sha is not None:
        require(event_head_sha == final_snapshot[7], "final event/live PR head mismatch")
        require_event_pr_matches_live(event["pull_request"], final_pr)

    return {
        "disposition": "PASS_SCOPED_SOURCE_IDENTITY",
        "repository": REPOSITORY,
        "pull_request": PR_NUMBER,
        "event": event_name,
        "trusted_base_sha": final_snapshot[4],
        "expected_merge_base": EXPECTED_MERGE_BASE,
        "candidate_head_sha": final_snapshot[7],
        "changed_paths": sorted(changed),
        "scope": "exact source identity only; no review, security certification, proof or scientific acceptance",
    }


def main() -> int:
    try:
        event_path = os.environ.get("GITHUB_EVENT_PATH", "")
        require(bool(event_path), "event payload path missing")
        with open(event_path, "rb") as stream:
            event_raw = stream.read(MAX_RESPONSE_BYTES + 1)
        require(len(event_raw) <= MAX_RESPONSE_BYTES, "event payload exceeds size limit")
        event = strict_json(event_raw)
        event_name = os.environ.get("GITHUB_EVENT_NAME", "")
        api = GitHubAPI(os.environ.get("GH_TOKEN", ""))
        result = verify(event_name, event, os.environ, api)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        # The token and response bodies are never included in diagnostics.
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
