#!/usr/bin/env python3
"""Verify immutable upstream Git trees; byte custody is not mathematical acceptance."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def git(repo, *args):
    return subprocess.run(["git", "--no-replace-objects", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def verify(repo, manifest):
    if type(manifest.get("schema")) is not int or manifest["schema"] != 1 or manifest.get("scientific_effect") != "NONE":
        raise ValueError("unexpected source manifest scope")
    sources = manifest.get("sources")
    if not isinstance(sources, list) or [s.get("id") for s in sources] != ["MF", "SC"]:
        raise ValueError("exactly the MF and SC interfaces are required")
    verified = []
    for source in sources:
        commit, blob, digest = (source.get(k, "") for k in ("commit", "git_blob", "sha256"))
        if not (re.fullmatch("[0-9a-f]{40}", commit)
                and re.fullmatch("[0-9a-f]{40}", blob)
                and re.fullmatch("[0-9a-f]{64}", digest)):
            raise ValueError("invalid immutable identity")
        name = source.get("path", "")
        path = PurePosixPath(name)
        if not name or path.is_absolute() or ".." in path.parts or str(path) != name:
            raise ValueError("invalid repository-relative source path")
        if type(source.get("bytes")) is not int or source["bytes"] < 1:
            raise ValueError("invalid source size")
        if git(repo, "cat-file", "-t", commit).strip() != b"commit":
            raise ValueError(source["id"] + ": expected an actual historical commit")
        # --full-tree is essential: callers may run from a nested packet directory.
        listing = git(repo, "ls-tree", "--full-tree", "-z", commit, "--", name)
        expected = ("100644 blob " + blob + "\t" + name + "\0").encode()
        if listing != expected:
            raise ValueError(source["id"] + ": historical commit/path/blob mismatch")
        data = git(repo, "cat-file", "blob", blob)
        if len(data) != source["bytes"] or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(source["id"] + ": source bytes mismatch")
        if hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest() != blob:
            raise ValueError(source["id"] + ": Git blob content mismatch")
        verified.append({"id": source["id"], "commit": commit, "path": name,
                         "git_blob": blob, "sha256": digest, "bytes": len(data)})
    return {"scientific_effect": "NONE", "historical_sources_verified": verified}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args()
    manifest = json.loads(Path(__file__).with_name("SOURCES.json").read_text(),
                          object_pairs_hook=no_duplicates,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))
    print(json.dumps(verify(Path(args.repo_root).resolve(), manifest), sort_keys=True))


if __name__ == "__main__":
    main()
