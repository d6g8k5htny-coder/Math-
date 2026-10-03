"""C107 frozen source custody only; no mathematical acceptance.

Follows the repository's full-history commit/path/blob verifier conventions.
Run with Python standard library; no network calls or source writes.
"""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE_KEYS = frozenset(("P", "E1", "E2", "REC", "RM", "RC"))
SOURCE_CUT = "7e2344166e989ae94e5732e445f445598fc75c4c"
FROZEN_FILES = {
    "PROOF.md": (29606, "d94f8f2f7e809da37465729d3eca5f9793bce5fc5410d9f83e61db259ddf73df"),
    "SOURCE_IDENTITIES.json": (2931, "f03da4be8cae14588d7e6e1d215091293dbad199bc9a0013cccca995a4c05a8c"),
    "CONTROLS_DESIGN.md": (4171, "963a797c28c5872097421187d3332e7e9041435d1eb31fca0a186e8dab4f6de7"),
    "author_controls.py": (16587, "9063ffb1c09c3ea62cc5dd7e0663ba4a9dada240ff7f9504a5bebfd7e92fec87"),
    "author_controls.normal.stdout": (2228, "a73652695fffc2fa8275f0b9a1119394beca4b5a6e4c690ef615d88ffcbc1d97"),
    "AUTHOR_CONTROL_RUNS.json": (3214, "ee15e53018b87d160a0824c684b0eac8b0b598bd24bd3bf49298a1d3edb79bfe"),
    "AUTHOR_CONTROLS_FREEZE.json": (1127, "a055e23dce305cf8b454b6c9786902d131962e56640493a0bc14f21c3aa75d0d"),
    "author_controls.normal.stderr": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "author_controls.optimized.stdout": (2228, "a73652695fffc2fa8275f0b9a1119394beca4b5a6e4c690ef615d88ffcbc1d97"),
    "author_controls.optimized.stderr": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "author_controls.launch_failure.stdout": (0, "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    "author_controls.launch_failure.stderr": (62, "4e74f59b4c51ae140112c2a67d336374a7b6afbbca5a9d0387ad98a7627359ef"),
    'review/AUTHOR_CHECKER_REPLAY.json': (2924, '4d0f7f0163875c4c363c6eef012f442052ed17fc124a5fd87a6be6173e457bf6'),
    'review/CONTROL_DESIGN.md': (4140, '161b0c0dc3b18db32a7ba61a868a944d5767c8b780281901ccc5c9f1435f51bb'),
    'review/INDEPENDENT_RUNS.json': (6623, '3ca33cc27729378744721b0a3bcc988b733410d3394b5dda4f2ca6048c29a424'),
    'review/REVIEW.md': (17536, 'df2785862ca5bc0620773d9ce71d1c5c11b4d53a6ebbbc93a3a3b0ed5e76fab8'),
    'review/REVIEW_RECEIPT.json': (1545, 'e27bcaa40d1c5d976e30de89e1748a4f66e27ae2c6f3155d41311d60e03d27ea'),
    'review/independent_controls.py': (11156, 'ae449870aa408a5437d5990b50d331a8af3d4eb063c8c7476f781677530ca873'),
    'review/ENGINEERING_REVIEW.md': (8795, '43d8bdd07cc40f9792cf62b71bf4067b2101013a2a53215c50681aca93ebbf80'),
    'review/ENGINEERING_RUNS.json': (8801, 'ac99011d56f5fdd0674a798bace78de7560c160849c4bce9460b4f047ffbe5fe'),
    'review/ENGINEERING_RECEIPT.json': (1837, 'aa2e927079db8e6f4f6db0a9b998066e082e2b31f928cf7aa32838974516e87b'),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(path):
    require(isinstance(path, str) and path and "\\" not in path
            and "\0" not in path, "invalid path")
    pure = PurePosixPath(path)
    require(not pure.is_absolute() and str(pure) == path
            and all(p not in ("", ".", "..") for p in path.split("/")),
            "noncanonical path: " + path)
    return pure


def contained(base, rel):
    pure = canonical(rel)
    base = Path(base)
    require(not base.is_symlink(), "symlink packet root")
    target = base
    for part in pure.parts:
        target = target / part
        require(not target.is_symlink(), "symlink path: " + rel)
    require(target.is_file() and base.resolve() in target.resolve().parents,
            "not a contained regular file: " + rel)
    return target


def unique_json(raw):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def blob_id(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def identity(data, entry):
    require(type(entry["bytes"]) is int and entry["bytes"] > 0,
            "invalid byte count")
    require(len(data) == entry["bytes"]
            and hashlib.sha256(data).hexdigest() == entry["sha256"]
            and blob_id(data) == entry["git_blob"], "source bytes mismatch")


def git(root, *args):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", GIT_OPTIONAL_LOCKS="0")
    result = subprocess.run(
        ["git", "--no-replace-objects", "-C", str(root), *args],
        capture_output=True, env=env, timeout=30,
    )
    require(result.returncode == 0, "git " + args[0] + " failed: "
            + result.stderr.decode(errors="replace").strip())
    return result.stdout


def historical(root, cut, entry):
    require(isinstance(cut, str) and re.fullmatch("[0-9a-f]{40}", cut),
            "forty-hex source commit required")
    path = entry["source_path"]
    canonical(path)
    blob = entry["git_blob"]
    require(isinstance(blob, str) and re.fullmatch("[0-9a-f]{40}", blob),
            "forty-hex source blob required")
    require(git(root, "cat-file", "-t", cut).strip() == b"commit",
            "source cut is not a commit")
    listing = git(root, "ls-tree", "--full-tree", "-z", cut, "--", path)
    require(listing == ("100644 blob " + blob + "\t" + path + "\0").encode(),
            "historical commit/path/blob mismatch")
    identity(git(root, "cat-file", "blob", blob), entry)


def current_source(root, entry):
    identity(contained(root, entry["source_path"]).read_bytes(), entry)


def verify(packet=HERE, root=ROOT):
    packet = Path(packet)
    for rel, (size, sha) in FROZEN_FILES.items():
        raw = contained(packet, rel).read_bytes()
        require(len(raw) == size and hashlib.sha256(raw).hexdigest() == sha,
                "frozen anchor mismatch: " + rel)
    manifest = unique_json(contained(packet, "SOURCE_IDENTITIES.json").read_bytes())
    require(manifest["repository"] == "d6g8k5htny-coder/Math-",
            "source repository mismatch")
    require(manifest["source_cut"] == SOURCE_CUT, "source cut mismatch")
    sources = manifest["sources"]
    require(isinstance(sources, dict) and set(sources) == SOURCE_KEYS,
            "exactly six declared source keys required")
    for key, entry in sources.items():
        require(entry["local_path"] == "sources/" + key + ".md",
                "source snapshot path mismatch: " + key)
        expected_url = ("https://github.com/d6g8k5htny-coder/Math-/blob/"
                        + SOURCE_CUT + "/" + entry["source_path"])
        require(entry["url"] == expected_url, "source URL mismatch: " + key)
        identity(contained(packet, entry["local_path"]).read_bytes(), entry)
        current_source(root, entry)
        historical(root, SOURCE_CUT, entry)
    return len(sources)


def main():
    try:
        count = verify()
    except (ValueError, KeyError, TypeError, OSError, subprocess.TimeoutExpired) as exc:
        print("source custody FAILED:", exc)
        return 1
    print(json.dumps({"verified_sources": count, "frozen_files": len(FROZEN_FILES),
                      "historical_pins_checked": True,
                      "current_sources_checked": True,
                      "remote_review_authenticity_checked": False,
                      "mathematical_acceptance": False,
                      "scientific_effect": "NONE"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
