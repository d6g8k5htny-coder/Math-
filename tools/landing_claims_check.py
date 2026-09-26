"""Fail-closed validator for claims/LANDING_CLAIMS.json and Math-/README.md.

This checker verifies identity, scope metadata, landing coverage, and the live work
queue. It never promotes scientific status. Remote issue verification is opt-in
and read-only.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "claims" / "LANDING_CLAIMS.json"
DEFAULT_LANDING = ROOT / "README.md"

POSITIVE_DISPOSITIONS = {"REVIEWED_SCOPED", "PROVED_REVIEWED"}
REQUIRED_FIELDS = {
    "claim_id", "advertised_label", "claim_type", "statement_path",
    "statement_heading", "source", "domain", "measure",
    "required_dependencies", "review", "disposition", "disposition_reason",
}


class ClaimManifestError(ValueError):
    pass


def strict_json(text: str):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ClaimManifestError(f"duplicate JSON key: {key}")
            out[key] = value
        return out
    def constant(value):
        raise ClaimManifestError(f"non-finite JSON constant: {value}")
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def git(*args: str, cwd: Path | None = None) -> str:
    workdir = ROOT if cwd is None else cwd
    result = subprocess.run(
        ["git", "-C", str(workdir), *args],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode:
        raise ClaimManifestError(
            "git command failed: " + " ".join(args) + "\n" + result.stderr.strip()
        )
    return result.stdout.strip()


def safe_relpath(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ClaimManifestError("nonempty repository-relative path required")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "\\" in value or ":" in value:
        raise ClaimManifestError(f"unsafe repository-relative path: {value}")
    return p.as_posix()


def verify_source_binding(binding: dict, path: str, *, current_required: bool = True) -> None:
    if not isinstance(binding, dict):
        raise ClaimManifestError(f"source binding for {path} must be an object")
    commit = binding.get("commit")
    blob = binding.get("blob")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ClaimManifestError(f"full immutable commit required for {path}")
    if not isinstance(blob, str) or not re.fullmatch(r"[0-9a-f]{40}", blob):
        raise ClaimManifestError(f"Git blob SHA required for {path}")
    path = safe_relpath(path)
    if git("cat-file", "-t", commit) != "commit":
        raise ClaimManifestError(f"pinned revision is not a commit: {commit}")
    try:
        pinned = git("rev-parse", f"{commit}:{path}")
    except ClaimManifestError as exc:
        raise ClaimManifestError(f"pinned source path is missing: {path}") from exc
    if pinned != blob:
        raise ClaimManifestError(
            f"pinned blob mismatch for {path}: manifest={blob} git={pinned}"
        )
    if current_required:
        current = ROOT / path
        if not current.is_file() or current.is_symlink():
            raise ClaimManifestError(f"advertised local source is missing/not regular: {path}")
        current_blob = git("hash-object", "--", path)
        if current_blob != blob:
            raise ClaimManifestError(
                f"current landing source drift for {path}: manifest={blob} current={current_blob}"
            )


def landing_result_paths(text: str) -> set[str]:
    start = text.find("## Read a result")
    end = text.find("## Run a calculation")
    if start < 0 or end < 0 or end <= start:
        raise ClaimManifestError("README must contain Read a result before Run a calculation")
    section = text[start:end]
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", section)
    return {
        safe_relpath(link)
        for link in links
        if link.startswith(("frontiers/", "coefficients/"))
    }


def landing_work_queue(text: str) -> str:
    match = re.search(r"\[Work queue\]\(([^)]+)\)", text)
    if not match:
        raise ClaimManifestError("README has no Work queue link")
    return match.group(1)


def _validate_review(review: dict) -> None:
    if not isinstance(review, dict) or review.get("kind") not in {"github_issue", "local_file"}:
        raise ClaimManifestError("review must be github_issue or local_file")
    if review["kind"] == "github_issue":
        if not isinstance(review.get("repo"), str) or type(review.get("number")) is not int:
            raise ClaimManifestError("github_issue review requires repo and integer number")
    else:
        path = safe_relpath(review.get("path"))
        verify_source_binding(review.get("source"), path, current_required=True)


def _validate_dependency(dep: dict, claim_ids: set[str]) -> None:
    if not isinstance(dep, dict) or dep.get("kind") not in {"claim", "external", "support"}:
        raise ClaimManifestError("dependency kind must be claim/external/support")
    if not isinstance(dep.get("id"), str) or not dep["id"]:
        raise ClaimManifestError("dependency id required")
    if dep["kind"] == "claim":
        if dep["id"] not in claim_ids:
            raise ClaimManifestError(f"unknown internal dependency: {dep['id']}")
    elif dep["kind"] == "external":
        if dep.get("binding_status") not in {"UNRESOLVED_EXTERNAL", "IMPORTED_FRAMEWORK", "BYTE_BOUND_EXTERNAL"}:
            raise ClaimManifestError(f"external dependency {dep['id']} has invalid binding_status")
        if not isinstance(dep.get("reference"), str) or not dep["reference"]:
            raise ClaimManifestError(f"external dependency {dep['id']} requires reference")
    else:
        path = safe_relpath(dep.get("path"))
        verify_source_binding(dep.get("source"), path, current_required=True)
        review = dep.get("review")
        if review is not None:
            if isinstance(review, dict) and review.get("kind") in {"github_issue", "local_file"}:
                _validate_review(review)
            else:
                # Backward-compatible support-review record: exact local review file
                # with path/source but no top-level review kind.
                if not isinstance(review, dict):
                    raise ClaimManifestError("support review must be an object")
                rpath = safe_relpath(review.get("path"))
                verify_source_binding(review.get("source"), rpath, current_required=True)


def validate_manifest(manifest: dict, landing_text: str) -> dict:
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ClaimManifestError("schema_version 1 required")
    if manifest.get("repository") != "d6g8k5htny-coder/Math-":
        raise ClaimManifestError("unexpected repository identity")
    allowed = manifest.get("allowed_dispositions")
    if not isinstance(allowed, list) or not all(isinstance(x, str) for x in allowed):
        raise ClaimManifestError("allowed_dispositions must be a string list")
    claims = manifest.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ClaimManifestError("nonempty claims list required")

    ids = [c.get("claim_id") for c in claims if isinstance(c, dict)]
    if len(ids) != len(claims) or any(not isinstance(x, str) or not x for x in ids):
        raise ClaimManifestError("every claim requires a nonempty claim_id")
    if len(set(ids)) != len(ids):
        raise ClaimManifestError("duplicate claim_id")
    claim_ids = set(ids)

    paths = []
    unresolved_positive = []
    for claim in claims:
        missing = REQUIRED_FIELDS - set(claim)
        if missing:
            raise ClaimManifestError(f"{claim['claim_id']} missing fields: {sorted(missing)}")
        if claim["disposition"] not in allowed:
            raise ClaimManifestError(f"{claim['claim_id']} has unknown disposition")
        if not isinstance(claim["domain"], str) or not claim["domain"].strip():
            raise ClaimManifestError(f"{claim['claim_id']} requires domain")
        if not isinstance(claim["measure"], str) or not claim["measure"].strip():
            raise ClaimManifestError(f"{claim['claim_id']} requires measure")
        path = safe_relpath(claim["statement_path"])
        paths.append(path)
        verify_source_binding(claim["source"], path, current_required=True)
        _validate_review(claim["review"])
        deps = claim["required_dependencies"]
        if not isinstance(deps, list):
            raise ClaimManifestError(f"{claim['claim_id']} dependencies must be a list")
        for dep in deps:
            _validate_dependency(dep, claim_ids)
            if (
                dep.get("kind") == "external"
                and dep.get("binding_status") == "UNRESOLVED_EXTERNAL"
                and claim["disposition"] in POSITIVE_DISPOSITIONS
            ):
                unresolved_positive.append((claim["claim_id"], dep["id"]))

    if len(set(paths)) != len(paths):
        raise ClaimManifestError("duplicate advertised statement_path")

    manifest_paths = set(paths)
    landing_paths = landing_result_paths(landing_text)
    if manifest_paths != landing_paths:
        missing_manifest = sorted(landing_paths - manifest_paths)
        missing_landing = sorted(manifest_paths - landing_paths)
        raise ClaimManifestError(
            f"landing/manifest mismatch: unmanifested={missing_manifest} unadvertised={missing_landing}"
        )

    queue = manifest.get("live_queue")
    if not isinstance(queue, dict):
        raise ClaimManifestError("live_queue object required")
    if type(queue.get("issue")) is not int or queue.get("required_state") != "open":
        raise ClaimManifestError("live_queue requires integer issue and required_state=open")
    if landing_work_queue(landing_text) != queue.get("url"):
        raise ClaimManifestError("README Work queue does not match manifest live_queue")
    if unresolved_positive:
        raise ClaimManifestError(
            "positive disposition depends on unresolved external source: "
            + ", ".join(f"{cid}->{dep}" for cid, dep in unresolved_positive)
        )

    return {
        "object": manifest.get("object"),
        "claim_count": len(claims),
        "advertised_paths": sorted(manifest_paths),
        "live_queue": queue,
        "unresolved_external_positive_count": 0,
        "scientific_effect": "NONE",
        "meaning": "identity/scope/navigation validation only; never theorem acceptance",
    }


def verify_issue_open(queue: dict) -> dict:
    repo = queue["repo"]
    issue = queue["issue"]
    url = f"https://api.github.com/repos/{repo}/issues/{issue}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "landing-claims-check/1",
    }
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = strict_json(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, UnicodeError) as exc:
        raise ClaimManifestError(f"cannot verify live queue issue: {exc}") from exc
    state = payload.get("state")
    if state != queue["required_state"]:
        raise ClaimManifestError(
            f"advertised live queue issue {repo}#{issue} is {state}, expected {queue['required_state']}"
        )
    return {"repo": repo, "issue": issue, "state": state}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--landing", type=Path, default=DEFAULT_LANDING)
    parser.add_argument("--verify-issues", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        manifest = strict_json(args.manifest.read_text())
        landing = args.landing.read_text()
        report = validate_manifest(manifest, landing)
        if args.verify_issues:
            report["live_queue_verification"] = verify_issue_open(manifest["live_queue"])
        payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            out = args.output.resolve()
            if out.exists():
                raise ClaimManifestError("output must be new")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(payload)
        print(payload, end="")
        return 0
    except (ClaimManifestError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print("LANDING_CLAIM_CHECK_REFUSED: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())