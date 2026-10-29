#!/usr/bin/env python3
"""One source-bound cusp quarantine boundary, not a general A3 certifier."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re

QID = "Q-CUSP-BINARY64-20261029"
BASE = "8151f592918a845bf19eb8eafaf8444540a32734"
PACKET = "frontiers/cusp_coefficient_certified_20261001"
RECORD = "quarantine/" + QID + ".json"
MANIFEST_BLOB = "e9624bdeb78e9fe37f8fbacf45958b9b93f1cf95"
DENIED = frozenset((
    PACKET,
    "frontiers/cusp_torus_transfer_20261001/RESULTS.json",
    "frontiers/cusp_torus_transfer_20261001/transfer.py",
    "frontiers/c2_torus_transfer_20261001/NOTE.md",
    "frontiers/c2_torus_transfer_20261001/SOURCE_MAP.json",
    "frontiers/c2_exact_20261001/NOTE.md",
    "frontiers/third_order_coefficient_20261001/NOTE.md",
    "frontiers/third_order_coefficient_20261001/README.md",
    "frontiers/third_order_coefficient_20261001/SOURCES.json",
    "frontiers/remainder_vanishing_20260930/ERRATUM_20261004.md",
))


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member " + ascii(key))
        result[key] = value
    return result


def strict_json(raw):
    return json.loads(raw, object_pairs_hook=unique_object)


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def regular(root, relative):
    path = root / relative
    if not path.is_file() or any(p.is_symlink() for p in [path, *path.parents]
                                 if p != root and root in p.parents):
        raise ValueError("regular local source required: " + relative)
    return path.read_bytes()


def normalized_consumer(value):
    if (not isinstance(value, str) or not value or value.startswith("/")
            or "\\" in value or ":" in value or "\0" in value):
        raise ValueError("unsafe consumer path: " + ascii(value))
    result = posixpath.normpath(value)
    if result == ".." or result.startswith("../"):
        raise ValueError("unsafe consumer path: " + ascii(value))
    return result


def audit(root):
    record_path = root / RECORD
    if not record_path.is_file():
        raise ValueError("missing quarantine record: " + RECORD)
    doc = strict_json(regular(root, RECORD))
    if not isinstance(doc, dict) or doc.get("schema") != "cbz.quarantine/v1" or doc.get("id") != QID:
        raise ValueError("unsupported quarantine record")
    if (doc.get("classification") != "QUARANTINED" or doc.get("layer_a") != "A3"
            or doc.get("layer_a_status") != "A3_NOT_PROVEN"):
        raise ValueError("quarantine A3 classification must remain explicit")
    if doc.get("cbz_certificate_admitted") is not False:
        raise ValueError("certificate admission must remain false")
    if doc.get("owner") is not None:
        raise ValueError("owner must remain unassigned")
    if type(doc.get("maintenance")) is not int or doc["maintenance"] != 0:
        raise ValueError("maintenance must remain zero")
    for field in ("title", "mathematical_arithmetic_gap"):
        if not isinstance(doc.get(field), str) or not doc[field].strip():
            raise ValueError("nonempty quarantine field required: " + field)
    boundary = doc.get("not_proven_boundary")
    if not isinstance(boundary, list) or not boundary or not all(isinstance(x, str) and x.strip() for x in boundary):
        raise ValueError("not-proven boundary must be nonempty")
    snapshot = doc.get("source_snapshot")
    if (not isinstance(snapshot, dict) or snapshot.get("commit") != BASE
            or snapshot.get("packet_path") != PACKET):
        raise ValueError("quarantine source snapshot must remain exact")
    denied = doc.get("denied_certificate_sources")
    if (not isinstance(denied, list) or not all(isinstance(x, str) for x in denied)
            or len(denied) != len(DENIED) or set(denied) != DENIED):
        raise ValueError("denied source inventory must remain exact")
    raw = regular(root, PACKET + "/SOURCE_FILES.json")
    if blob(raw) != MANIFEST_BLOB:
        raise ValueError("frozen packet manifest identity mismatch")
    manifest = strict_json(raw)
    entries = manifest["files"]
    names = [entry["path"] for entry in entries]
    if any(Path(name).name != name for name in names) or len(names) != 15 or len(set(names)) != 15:
        raise ValueError("frozen packet manifest inventory mismatch")
    expected_names = set(names) | {"SOURCE_FILES.json"}
    if {p.name for p in (root / PACKET).iterdir()} != expected_names:
        raise ValueError("packet tree differs from frozen manifest")
    expected = {}
    for name in sorted(expected_names):
        data = regular(root, PACKET + "/" + name)
        row = {"path": PACKET + "/" + name, "git_blob": blob(data),
               "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        expected[row["path"]] = row
    for entry in entries:
        actual = expected[PACKET + "/" + entry["path"]]
        if any(actual[key] != entry[key] for key in ("git_blob", "sha256", "bytes")):
            raise ValueError("packet source identity mismatch: " + entry["path"])
    sources = doc.get("source_files")
    if (not isinstance(sources, list) or len(sources) != 16
            or any(not isinstance(x, dict) or not isinstance(x.get("path"), str)
                   or type(x.get("bytes")) is not int for x in sources)
            or {x["path"] for x in sources} != set(expected)
            or any(x != expected[x["path"]] for x in sources)):
        raise ValueError("exact packet inventory required in quarantine record")
    if snapshot.get("manifest") != expected[PACKET + "/SOURCE_FILES.json"]:
        raise ValueError("snapshot manifest identity mismatch")
    index = (root / "PROOF_INDEX.md").read_text(encoding="utf-8")
    matches = re.findall(r"<!-- CBZ_CUSP_QUARANTINE (\{[^\n]*\}) -->", index)
    wanted = {"id": QID, "classification": "QUARANTINED",
              "layer_a_status": "A3_NOT_PROVEN", "cbz_certificate_admitted": False, "record": RECORD}
    entry = strict_json(matches[0]) if len(matches) == 1 else None
    if (not isinstance(entry, dict) or entry != wanted
            or entry.get("cbz_certificate_admitted") is not False):
        raise ValueError("canonical index quarantine classification mismatch")
    return {x["git_blob"] for x in sources}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--consume", action="append", default=[],
                        help="test explicit numerical-certificate source admission; unrelated sources are NOT_COVERED")
    args = parser.parse_args(argv)
    report = {"quarantine_id": QID, "scope": "one-packet quarantine integrity and explicit source admission only",
              "layer_a_status": "A3_NOT_PROVEN", "cbz_certificate_admitted": False,
              "status": "QUARANTINE_INTEGRITY_OK", "preserved_packet_files": 0, "problems": []}
    try:
        root = args.root.resolve()
        known_blobs = audit(root)
        report["preserved_packet_files"] = 16
        for value in args.consume:
            path = normalized_consumer(value)
            denied = path in DENIED or path.startswith(PACKET + "/")
            if not denied and (root / path).exists():
                denied = blob(regular(root, path)) in known_blobs
            if denied:
                report["problems"].append("quarantined numerical source: " + path)
    except (ValueError, OSError) as exc:
        report["problems"].append(str(exc))
    if report["problems"]:
        report["status"] = "REFUSED"
        code = 1
    elif args.consume:
        report["status"] = "NOT_COVERED"
        code = 2
    else:
        code = 0
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
