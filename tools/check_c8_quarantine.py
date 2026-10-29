#!/usr/bin/env python3
"""One frozen C8 quarantine boundary. Integrity and exact witnesses never grant admission."""
from fractions import Fraction as F
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat

QID = "Q-C8-ELDER-FAILURE-BINARY64-20261029"
BASE = "e877242cf68fb24c605066f16dd07f513ee75a1d"
PACKET = "frontiers/c8_elder_failure_coefficient_20261001"
RECORD = "quarantine/" + QID + ".json"
MANIFEST_BLOB = "1efc243fa447e7162644b939b2cd2200270e9874"
OBJECT = "CL-C8-ELDER-FAILURE-COEFFICIENT-20261001-v1"
DENIED_SOURCES = (PACKET, PACKET + "/RESULTS.json", PACKET + "/certificate.py",
                  PACKET + "/boxes.py", PACKET + "/torus.py")
COPY_SOURCES = ("RESULTS.json", "certificate.py", "boxes.py", "torus.py")
MOMENT_IDENTITY = "6*(6*k + 1/(4*k) + 5/(216*k^3))"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member: " + ascii(key))
        result[key] = value
    return result


def strict_json(raw):
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite JSON: " + value)))
    except UnicodeError as exc:
        raise ValueError("invalid UTF-8 JSON") from exc


def regular(root, relative):
    pure = PurePosixPath(relative)
    require(not pure.is_absolute() and pure.parts and ".." not in pure.parts
            and pure.as_posix() == relative, "unsafe local source path")
    for i in range(1, len(pure.parts)):
        path = root.joinpath(*pure.parts[:i])
        mode = path.lstat().st_mode
        require(stat.S_ISDIR(mode), "regular local source ancestor required: " + relative)
        require(mode & 0o444 and mode & 0o111, "unreadable local source ancestor: " + relative)
    path = root / relative
    mode = path.lstat().st_mode
    require(stat.S_ISREG(mode), "regular local source required: " + relative)
    require(mode & 0o444, "unreadable local source: " + relative)
    return path.read_bytes()


def normalized_consumer(value):
    require(isinstance(value, str) and value and not value.startswith("/")
            and not any(x in value for x in ("\\", ":", "\0")), "unsafe consumer path")
    result = posixpath.normpath(value)
    require(result != ".." and not result.startswith("../"), "unsafe consumer path")
    return result


def pointer(path):
    return "/" + "/".join(x.replace("~", "~0").replace("/", "~1") for x in path)


def canonical_pointer(value):
    require(isinstance(value, str) and value.startswith("/results/")
            and not re.search(r"~(?![01])", value), "invalid output pointer")
    path = [part.replace("~1", "/").replace("~0", "~") for part in value[1:].split("/")]
    require(pointer(path) == value, "invalid output pointer")
    return value


def interval_pairs(document):
    rows = {}
    def walk(value, path):
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, path + [key])
        elif isinstance(value, list) and len(value) == 2 and all(isinstance(v, str) for v in value):
            key = pointer(path)
            require(key not in rows, "duplicate published output")
            rows[key] = {"path": path, "json_pointer": key, "interval": value}
    walk(document["results"], ["results"])
    require(len(rows) == 109, "frozen 109-output inventory differs")
    return rows


def exact_exceptions(document):
    result = []
    for k, label in ((F(1, 2), "k=0.5"), (F(1), "k=1"), (F(2), "k=2")):
        exact = 6 * (6 * k + F(1) / (4 * k) + F(5) / (216 * k ** 3))
        row = document["results"][label]
        pair = row["parts"]["E[2T]"]
        require(row["E[2T] exact"] == str(exact), "exact rational identity differs")
        require(F(pair[0]) <= exact <= F(pair[1]), "exact rational containment failed")
        result.append({"path": ["results", label, "parts", "E[2T]"], "interval": pair,
                       "exact_value": str(exact), "identity": MOMENT_IDENTITY, "k": str(k),
                       "method": "Exact Fraction formula and exact decimal containment; no binary64 execution."})
    return result


def audit(root):
    require((root / RECORD).exists(), "missing quarantine record")
    record_raw = regular(root, RECORD)
    doc = strict_json(record_raw)
    require(isinstance(doc, dict) and doc.get("schema") == "cbz.quarantine/v1" and doc.get("id") == QID,
            "unsupported quarantine record")
    require(doc.get("classification") == "QUARANTINED" and doc.get("layer_a") == "A3"
            and doc.get("layer_a_status") == "A3_NOT_PROVEN", "explicit A3 classification required")
    require(doc.get("cbz_certificate_admitted") is False, "certificate admission must remain false")
    require(doc.get("owner") is None, "owner must remain unassigned")
    require(type(doc.get("maintenance")) is int and doc["maintenance"] == 0, "maintenance must remain zero")
    require(isinstance(doc.get("isolation"), dict) and doc["isolation"].get("global_A3_audit") is False,
            "limited opt-in scope must remain explicit")
    boundary = doc.get("not_proven_boundary")
    require(isinstance(boundary, list) and boundary and all(isinstance(v, str) and v.strip() for v in boundary),
            "nonempty mathematical boundary required")
    for field in ("title", "mathematical_arithmetic_gap"):
        require(isinstance(doc.get(field), str) and doc[field].strip(), "nonempty record field: " + field)
    snapshot = doc.get("source_snapshot")
    require(isinstance(snapshot, dict) and snapshot.get("repository") == "d6g8k5htny-coder/Math-"
            and snapshot.get("commit") == BASE and snapshot.get("packet_path") == PACKET
            and snapshot.get("packet_object") == OBJECT, "exact source snapshot required")
    require(doc.get("denied_certificate_sources") == list(DENIED_SOURCES), "exact denied source inventory required")
    raw = regular(root, PACKET + "/SOURCE_FILES.json")
    require(blob(raw) == MANIFEST_BLOB, "frozen packet manifest identity differs")
    manifest = strict_json(raw)
    entries = manifest["files"]
    names = [v["path"] for v in entries]
    require(len(names) == 10 and len(set(names)) == 10 and all(PurePosixPath(v).name == v for v in names),
            "frozen packet manifest inventory differs")
    expected_names = set(names) | {"SOURCE_FILES.json"}
    require({v.name for v in (root / PACKET).iterdir()} == expected_names, "packet tree differs from frozen manifest")
    expected = {}
    for name in sorted(expected_names):
        data = regular(root, PACKET + "/" + name)
        expected[PACKET + "/" + name] = {"path": PACKET + "/" + name, "git_blob": blob(data),
                                          "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    for entry in entries:
        actual = expected[PACKET + "/" + entry["path"]]
        require(all(actual[k] == entry[k] for k in ("git_blob", "sha256", "bytes")),
                "packet source identity differs: " + entry["path"])
    sources = doc.get("source_files")
    require(isinstance(sources, list) and len(sources) == 11
            and all(isinstance(v, dict) and isinstance(v.get("path"), str) and type(v.get("bytes")) is int for v in sources)
            and {v["path"] for v in sources} == set(expected)
            and all(v == expected[v["path"]] for v in sources), "exact packet inventory required")
    require(snapshot.get("manifest") == expected[PACKET + "/SOURCE_FILES.json"], "snapshot manifest identity differs")
    document = strict_json(regular(root, PACKET + "/RESULTS.json"))
    pairs = interval_pairs(document)
    exceptions = exact_exceptions(document)
    exact = {pointer(v["path"]): v for v in exceptions}
    denied = {key: value for key, value in pairs.items() if key not in exact}
    listed = doc.get("denied_outputs")
    require(type(doc.get("denied_output_count")) is int and doc["denied_output_count"] == 106
            and isinstance(listed, list) and len(listed) == 106
            and all(isinstance(v, dict) and isinstance(v.get("json_pointer"), str) for v in listed)
            and {v["json_pointer"] for v in listed} == set(denied)
            and all(v == denied[v["json_pointer"]] for v in listed), "exact denied output inventory required")
    require(doc.get("exact_rational_exceptions") == exceptions, "exact rational exception inventory differs")
    index = regular(root, "PROOF_INDEX.md").decode("utf-8")
    matches = re.findall(r"<!-- CBZ_C8_QUARANTINE (\{[^\n]*\}) -->", index)
    entry = strict_json(matches[0].encode()) if len(matches) == 1 else None
    wanted = {"id": QID, "classification": "QUARANTINED", "layer_a_status": "A3_NOT_PROVEN",
              "cbz_certificate_admitted": False, "record": RECORD}
    require(isinstance(entry, dict) and entry == wanted and entry.get("cbz_certificate_admitted") is False,
            "canonical index quarantine classification differs")
    copied = {expected[PACKET + "/" + name]["git_blob"] for name in COPY_SOURCES}
    return {"denied": denied, "exact": exact, "copied": copied,
            "record_sha256": hashlib.sha256(record_raw).hexdigest(), "packet_manifest_git_blob": MANIFEST_BLOB}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    parser.add_argument("--consume", action="append", default=[])
    parser.add_argument("--consume-output", action="append", default=[])
    args = parser.parse_args(argv)
    report = {"quarantine_id": QID, "status": "QUARANTINE_INTEGRITY_OK", "scientific_effect": "NONE",
              "layer_a_status": "A3_NOT_PROVEN", "cbz_certificate_admitted": False,
              "scope": "C8 packet, exact 106 denial paths, three Fraction witnesses and canonical index only; descriptive consumer metadata and global downstream isolation are not certified.",
              "preserved_packet_files": 0, "denied_output_count": 0, "exact_exception_count": 0,
              "source_decisions": [], "output_decisions": [], "problems": []}
    try:
        root = args.root.absolute()
        require(".." not in root.parts and not any(p.is_symlink() for p in (root, *root.parents)), "symlink checkout or unsafe root")
        checked = audit(root)
        report.update(preserved_packet_files=11, denied_output_count=len(checked["denied"]),
                      exact_exception_count=len(checked["exact"]), record_sha256=checked["record_sha256"],
                      packet_manifest_git_blob=checked["packet_manifest_git_blob"])
        for value in args.consume:
            path = normalized_consumer(value)
            denied = path in DENIED_SOURCES or path.startswith(PACKET + "/")
            if not denied and ((root / path).exists() or (root / path).is_symlink()):
                denied = blob(regular(root, path)) in checked["copied"]
            report["source_decisions"].append({"source": path, "decision": "DENIED" if denied else "NOT_COVERED"})
            if denied:
                report["problems"].append("quarantined numerical source: " + path)
        for value in args.consume_output:
            path = canonical_pointer(value)
            if path in checked["denied"]:
                report["output_decisions"].append({"output": path, "decision": "DENIED"})
                report["problems"].append("quarantined numerical output: " + path)
            elif path in checked["exact"]:
                report["output_decisions"].append({"output": path, "decision": "EXACT_RATIONAL_WITNESS_ONLY",
                                                   "exact_value": checked["exact"][path]["exact_value"]})
            else:
                report["output_decisions"].append({"output": path, "decision": "NOT_COVERED"})
    except (ValueError, OSError, KeyError, TypeError) as exc:
        report["problems"].append(str(exc))
    if report["problems"]:
        report["status"] = "REFUSED"
        code = 1
    elif args.consume or args.consume_output:
        report["status"] = "NOT_COVERED"
        code = 2
    else:
        code = 0
    print(json.dumps(report, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
