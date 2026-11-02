"""Project actual terminal C291 evidence into a public, source-bound packet.

Do not run before final results. No compiler, dependency cache, or network is
used. The only writes are a new evidence/final directory and a private root
PUBLIC_EVIDENCE_PROJECTION.json; existing deliveries are never overwritten.

PUBLIC_EVIDENCE_INPUTS.json schema (all paths relative to this C291 root):
  schema_version: 1
  private_identifier_inventory_complete: true
  private_identifiers: [the complete known private Drive ID inventory]
  files: [{source, destination, sha256, role}, ...]
  gates: {source_inventory, final_sequence, dependency_rehash, review_text,
          review_acceptance, negative_index}
Each gate value names a source in files. destination is relative to
publication-package/evidence/final. Every selected file must have an actual
raw hash, and every terminal final run requires its full START/RECEIPT/logs.
Fixture destinations must end in .lean.txt, avoiding Lake source discovery.

Roles: source_inventory, final_sequence, dependency_rehash, final_review,
review_acceptance, negative_index, final_start, final_receipt, final_stdout,
final_stderr, negative_start, negative_receipt, negative_stdout,
negative_stderr, negative_fixture, negative_manifest, negative_acceptance,
verification_script, supporting_evidence.

NEGATIVE_FINAL_INDEX uses the parent-agreed status PASS and receipt paths.
Its two_part_acceptance is either an object or a listed JSON path, with status
PASS, positive_baseline_receipt_sha256, binding_probe_receipt_sha256,
baseline_source_sha256, and baseline_objects. This preserves the original
positive baseline's wrapper failure while binding the actual successful
compilation and the separate actual proof-reference observation.

This exporter checks terminal identities and projection completeness. It does
not replace verify_execution.py, verify_mutations.py, or substantive review.
The acceptance metadata is required to bind the actual review and gate files.

Known agent identifiers in full review prose are preserved literally. The
package's older blanket agent-prefix hygiene rule needs the parent's explicit
agent token allowlist when final prose is added; do not rewrite attribution.
"""

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent
PACKAGE = ROOT / "publication-package"
MANIFEST = ROOT / "PUBLIC_EVIDENCE_INPUTS.json"
PRIVATE_PROJECTION = ROOT / "PUBLIC_EVIDENCE_PROJECTION.json"
FINAL = PACKAGE / "evidence/final"
RUNTIME = "@PINNED_LEAN_RUNTIME@"
CACHE = "@PINNED_DEPENDENCY_CACHE@"
REPLACEMENTS = [
    {"label": "c291_root", "original": str(ROOT), "logical": "@C291_ROOT@"},
    {"label": "pinned_runtime", "original": RUNTIME, "logical": "@PINNED_LEAN_RUNTIME@"},
    {"label": "pinned_dependency_cache", "original": CACHE, "logical": "@PINNED_DEPENDENCY_CACHE@"},
]
NEW = ["SourceThetaBridge", "SourceLifetimeGeometry", "SourceLifetimeField",
       "SourceLifetimeControls", "SourceLifetimeAxiomAudit"]
GATE_ROLES = {
    "source_inventory": "source_inventory", "final_sequence": "final_sequence",
    "dependency_rehash": "dependency_rehash", "review_text": "final_review",
    "review_acceptance": "review_acceptance", "negative_index": "negative_index",
}
ROLES = set(GATE_ROLES.values()) | {
    "final_start", "final_receipt", "final_stdout", "final_stderr",
    "negative_start", "negative_receipt", "negative_stdout", "negative_stderr",
    "negative_fixture", "negative_manifest", "negative_acceptance",
    "verification_script", "supporting_evidence",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def relative_path(value):
    require(isinstance(value, str) and value and "\\" not in value,
            "expected a nonempty POSIX relative path")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and path.as_posix() == value,
            "noncanonical or escaping relative path: " + value)
    require(path.parts and path.parts[0] != ".", "invalid relative path")
    return path


def regular_source(relative):
    path = ROOT.joinpath(*relative_path(relative).parts)
    current = ROOT
    for part in relative_path(relative).parts:
        current = current / part
        require(not current.is_symlink(), "symlink input: " + relative)
    require(path.is_file(), "missing regular input: " + relative)
    return path


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from strings(key)
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def privacy_check(text, identifiers):
    # Decoding URLs catches escaped private links; JSON strings are inspected
    # separately as well, so unicode-escaped paths cannot bypass this check.
    variants = [text]
    for _ in range(3):
        decoded = unquote(variants[-1]).replace("\\/", "/")
        if decoded == variants[-1]:
            break
        variants.append(decoded)
    for value in variants:
        require(not re.search(r"/(?:Users|home)/", value), "residual private filesystem path")
        require(not re.search(r"(?:drive|docs)\.google\.com", value, re.I),
                "residual Google Drive/Docs URL")
        for identifier in identifiers:
            require(identifier not in value, "residual listed private identifier")
        for rule in REPLACEMENTS:
            require(rule["original"] not in value, "residual explicit private prefix")


def project_bytes(data, destination, identifiers):
    text = data.decode("utf-8", errors="strict")
    counts = {}
    for rule in sorted(REPLACEMENTS, key=lambda r: (-len(r["original"]), r["label"])):
        # Replace an exact root prefix only, never an arbitrary matching fragment.
        pattern = re.compile(re.escape(rule["original"]) + r"(?=$|[/\s\"'\],}:)])")
        text, count = pattern.subn(lambda _: rule["logical"], text)
        counts[rule["label"]] = count
    privacy_check(text, identifiers)
    if destination.endswith(".json"):
        parsed = json.loads(text)
        for value in strings(parsed):
            privacy_check(value, identifiers)
    return text.encode("utf-8"), counts


def load_inputs():
    manifest_bytes = regular_source(MANIFEST.name).read_bytes()
    config = json.loads(manifest_bytes)
    require(config.get("schema_version") == 1, "unsupported input schema")
    require(config.get("private_identifier_inventory_complete") is True,
            "explicit complete private-identifier inventory is required")
    identifiers = config.get("private_identifiers")
    require(isinstance(identifiers, list) and all(isinstance(v, str) and len(v) >= 10 for v in identifiers),
            "private_identifiers must list actual nonempty private IDs")
    require(len(identifiers) == len(set(identifiers)), "duplicate private identifier")
    entries = {}
    destinations = set()
    records = config.get("files")
    require(isinstance(records, list) and records, "explicit input files are required")
    for item in records:
        require(set(item) == {"source", "destination", "sha256", "role"}, "unexpected file-entry schema")
        source = item["source"]
        dest = relative_path(item["destination"]).as_posix()
        require(source not in entries and dest not in destinations, "duplicate source or destination")
        require(item["role"] in ROLES, "unknown input role")
        require(re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None, "invalid expected digest")
        require(not source.startswith("publication-package/"), "do not export an existing public projection recursively")
        require(not source.startswith("final-build/"), "compiled objects are not public evidence inputs")
        require(not PurePosixPath(source).name.startswith("FINAL_DEPENDENCY_ARTIFACTS"),
                "export the rehash summary, not the large dependency inventory")
        require(dest != "PUBLIC_EVIDENCE_PROJECTION.json", "reserved public mapping filename")
        require(not dest.endswith(".lean"), "evidence must not add Lake source roots")
        if item["role"] == "negative_fixture":
            require(source.endswith(".lean") and dest.endswith(".lean.txt"), "full negative fixture must use .lean.txt")
        path = regular_source(source)
        data = path.read_bytes()
        require(sha(data) == item["sha256"], "raw input hash mismatch: " + source)
        data.decode("utf-8", errors="strict")
        entries[source] = {**item, "raw": data}
        destinations.add(dest)
    reserved = destinations | {"PUBLIC_EVIDENCE_PROJECTION.json"}
    for dest in reserved:
        require(not any(parent.as_posix() in reserved for parent in PurePosixPath(dest).parents
                        if parent.as_posix() != "."), "destination file/directory collision: " + dest)
    gates = config.get("gates")
    require(isinstance(gates, dict) and set(gates) == set(GATE_ROLES), "exact gate references are required")
    for name, role in GATE_ROLES.items():
        require(gates[name] in entries and entries[gates[name]]["role"] == role,
                "missing or wrong-role actual gate: " + name)
    return manifest_bytes, config, entries, identifiers


def validate_actual_gates(config, entries):
    gates = config["gates"]

    def data(source, role=None):
        require(source in entries, "required actual evidence omitted: " + source)
        if role:
            require(entries[source]["role"] == role, "wrong evidence role: " + source)
        return json.loads(entries[source]["raw"])

    def digest(source):
        require(source in entries, "required hash binding omitted: " + source)
        return entries[source]["sha256"]

    def logs(receipt_source, record, prefix):
        parent = PurePosixPath(receipt_source).parent
        start_source = (parent / "START.json").as_posix()
        start = data(start_source, prefix + "_start")
        require(all(key in record and record[key] == value for key, value in start.items()),
                "START differs from its terminal receipt: " + receipt_source)
        for stream in ("stdout", "stderr"):
            source = (parent / (stream + ".txt")).as_posix()
            require(source in entries and entries[source]["role"] == prefix + "_" + stream,
                    "full actual log omitted: " + source)
            require(digest(source) == record[stream + "_sha256"], "log digest mismatch: " + source)

    inventory = data(gates["source_inventory"])
    invsha = digest(gates["source_inventory"])
    sources = inventory["sources"]
    expected = {v["name"]: v["sha256"] for v in sources}
    require(len(sources) == len(expected) == 19 and inventory["new_modules"] == NEW,
            "incorrect frozen source inventory")
    require(len(inventory["build_order"]) == 19 and
            set(inventory["build_order"]) == {name[:-5] for name in expected}, "incomplete build order")
    for item in sources:
        name = item["name"]
        require(PurePosixPath(name).name == name and name.endswith(".lean"), "invalid source basename")
        frozen = regular_source("final-project/" + name).read_bytes()
        public = PACKAGE / (name if name[:-5] in NEW else "inputs/" + name)
        require(len(frozen) == item["bytes"] and sha(frozen) == item["sha256"], "frozen source mismatch: " + name)
        require(public.is_file() and not public.is_symlink() and public.read_bytes() == frozen,
                "package source differs from final source: " + name)

    sequence = data(gates["final_sequence"])
    require(sequence["status"] == "PASS_LOCAL_SOURCE_BUILD_AND_STANDARD_KERNEL_REPLAY" and
            sequence["source_inventory_sha256"] == invsha, "final 24-phase sequence has not passed")
    phases = [("build", m) for m in inventory["build_order"]] + [("kernel", m) for m in NEW]
    require(len(sequence["phases"]) == 24 and
            [(p["kind"], p["module"]) for p in sequence["phases"]] == phases and
            all(p["returncode"] == 0 for p in sequence["phases"]), "incomplete actual phase sequence")
    final_receipts = {s: data(s) for s, e in entries.items() if e["role"] == "final_receipt"}
    actual_receipts = {p.relative_to(ROOT).as_posix() for p in (ROOT / "final-runs").glob("*/RECEIPT.json")}
    require(set(final_receipts) == actual_receipts and len(final_receipts) == 26,
            "all24successfulquartets and both preservedfailedquartets must be listed")
    recovery = sequence["recovery"]
    failed_source = recovery["failed_receipt"]["path"]
    failed = final_receipts[failed_source]
    require(digest(failed_source) == recovery["failed_receipt"]["sha256"] and
            digest(recovery["failed_sequence"]["path"]) == recovery["failed_sequence"]["sha256"],
            "unbound original audit failure")
    require(failed["returncode"] == -15 and failed["timed_out"] is True and
            failed["timeout_seconds"] == 420 and failed["objects_before"] == failed["objects_after"] and
            failed["source_before"] == failed["source_after"] == expected and
            failed["integrity_error"] is None and "object_sha256" not in failed,
            "incorrect preserved failure")
    logs(failed_source, failed, "final")
    kernel_recovery = sequence["kernel_recovery"]
    kernel_failed_source = kernel_recovery["failed_receipt"]["path"]
    kernel_failed = final_receipts[kernel_failed_source]
    require(digest(kernel_failed_source) == kernel_recovery["failed_receipt"]["sha256"] and
            digest(kernel_recovery["failed_sequence"]["path"]) == kernel_recovery["failed_sequence"]["sha256"],
            "unbound kernel child discovery failure")
    require(kernel_failed["returncode"] == 1 and kernel_failed["timed_out"] is False and
            kernel_failed["objects_before"] == kernel_failed["objects_after"] and
            kernel_failed["source_before"] == kernel_failed["source_after"] == expected and
            kernel_failed["integrity_error"] is None and "object_sha256" not in kernel_failed,
            "incorrect preserved kernel failure")
    logs(kernel_failed_source, kernel_failed, "final")
    keyed = {(r["kind"], r["module"]): (s, r) for s, r in final_receipts.items()
             if s not in {failed_source, kernel_failed_source}}
    require(len(keyed) == 24 and set(keyed) == set(phases), "duplicate or missing final phase receipt")
    runner_hash = digest("run_final_phase.py")
    for phase in phases:
        source, record = keyed[phase]
        require(record["returncode"] == 0 and record["timed_out"] is False and
                record["source_unchanged"] is True and record["imported_objects_unchanged"] is True and
                record["integrity_error"] is None, "failed final phase: " + source)
        require(record["inventory_sha256"] == invsha and
                record["source_before"] == record["source_after"] == expected and
                record["runner_sha256"] == (digest("run_kernel_recovery_phase.py") if phase[0] == "kernel" else digest("run_recovery_phase.py") if phase == ("build", "SourceLifetimeAxiomAudit") else runner_hash), "unbound final phase: " + source)
        logs(source, record, "final")
    for filename in ("prepare_final_inputs.py", "run_final_phase.py", "run_final_sequence.py",
                     "run_recovery_phase.py", "run_recovery_sequence.py",
                     "run_kernel_recovery_phase.py", "run_kernel_recovery_sequence.py",
                     "rehash_final_dependencies.py", "verify_execution.py"):
        require(filename in entries and entries[filename]["role"] == "verification_script",
                "verification program omitted: " + filename)

    rehash = data(gates["dependency_rehash"])
    require(rehash["status"] == "PASS_EXACT_DEPENDENCY_BYTES_AND_PATHSET" and
            rehash["mismatches"] == [] and rehash["final_paths_match"] is True and
            rehash["inventory_sha256"] == inventory["dependency_artifact_inventory_sha256"],
            "terminal dependency rehash has not passed")
    require(datetime.fromisoformat(rehash["started_utc"]) >= datetime.fromisoformat(sequence["ended_utc"]),
            "dependency rehash predates final execution")

    negative = data(gates["negative_index"])
    require(negative["status"] == "PASS", "negative evidence is not final PASS")
    paths = negative["receipts"]
    require(isinstance(paths, list) and len(paths) == len(set(paths)) and paths,
            "invalid selected negative receipt set")
    require(set(paths) == {s for s, e in entries.items() if e["role"] == "negative_receipt"},
            "negative receipt selection does not match final index")
    negative_records = {s: data(s, "negative_receipt") for s in paths}
    for source, record in negative_records.items():
        require(record["timed_out"] is False, "selected negative receipt timed out")
        logs(source, record, "negative")
    required_keys = ["positive_baseline_receipt", "binding_probe_receipt", "mutants_receipt",
                     "axiom_carrier_receipt", "axiom_rejection_receipt"]
    require(all(negative[k] in negative_records for k in required_keys), "required negative receipt omitted")
    baseline_path = negative["positive_baseline_receipt"]
    probe_path = negative["binding_probe_receipt"]
    baseline, probe = negative_records[baseline_path], negative_records[probe_path]
    require(baseline["returncode"] == 0 and baseline["control_pass"] is False and not baseline["errors"],
            "preserve the observed positive compilation and original wrapper failure")
    require(all(value is True for key, value in baseline["checks"].items() if not key.startswith("local_binding:")),
            "baseline has an unresolved non-instrumentation failure")
    require(probe["returncode"] == 0 and probe["control_pass"] is True and
            all(v is True for v in probe["checks"].values()), "binding probe did not pass")
    require(probe["original_compile_receipt_sha256"] == digest(baseline_path) and
            probe["original_baseline_source_sha256"] == baseline["fixture_before"]["NegativeFixtureBaseline"] and
            probe["original_baseline_objects"] == baseline["own_objects_after"], "probe is not bound to actual baseline")
    acceptance = negative["two_part_acceptance"]
    if isinstance(acceptance, str):
        acceptance = data(acceptance, "negative_acceptance")
    require(isinstance(acceptance, dict) and acceptance.get("status") == "PASS", "two-part acceptance is missing")
    require(acceptance["positive_baseline_receipt_sha256"] == digest(baseline_path) and
            acceptance["binding_probe_receipt_sha256"] == digest(probe_path) and
            acceptance["baseline_source_sha256"] == probe["original_baseline_source_sha256"] and
            acceptance["baseline_objects"] == probe["original_baseline_objects"], "two-part acceptance bindings differ")
    for key, code in (("mutants_receipt", 1), ("axiom_carrier_receipt", 0), ("axiom_rejection_receipt", 1)):
        record = negative_records[negative[key]]
        require(record["returncode"] == code and record["control_pass"] is True and
                all(v is True for v in record["checks"].values()), "negative check did not pass: " + key)
    generation = relative_path(negative["generation"])
    fixture_manifest_source = (generation / "MANIFEST.json").as_posix()
    fixture_manifest = data(fixture_manifest_source, "negative_manifest")
    require(digest(fixture_manifest_source) == negative["manifest_sha256"], "negative generation manifest mismatch")
    require(baseline["manifest_sha256"] == probe["original_manifest_sha256"] == negative["manifest_sha256"],
            "baseline/probe refer to a different fixture generation")
    fixture_hashes = {module: info["sha256"] for module, info in fixture_manifest["modules"].items()}
    for source, record in negative_records.items():
        if source != probe_path:
            require(record["manifest_sha256"] == negative["manifest_sha256"] and
                    record["fixture_before"] == fixture_hashes, "negative receipt fixture binding differs: " + source)
    for module, info in fixture_manifest["modules"].items():
        source = (generation / (module + ".lean")).as_posix()
        require(source in entries and entries[source]["role"] == "negative_fixture" and
                digest(source) == info["sha256"] and len(entries[source]["raw"]) == info["bytes"],
                "full bound negative fixture omitted: " + module)
    require(any(e["role"] == "negative_fixture" and e["sha256"] == probe["probe_source_sha256"]
                for e in entries.values()), "full proof-binding probe fixture omitted")
    require(any(e["role"] == "negative_manifest" and e["sha256"] == probe["probe_manifest_sha256"]
                for e in entries.values()), "proof-binding probe manifest omitted")
    exported_runner_hashes = {e["sha256"] for e in entries.values() if e["role"] == "verification_script"}
    for record in negative_records.values():
        require(record["runner_sha256"] in exported_runner_hashes, "actual negative runner omitted")
        if "imported_runner_sha256" in record:
            require(record["imported_runner_sha256"] in exported_runner_hashes, "imported negative runner omitted")

    review = data(gates["review_acceptance"])
    require(review["verdict"] == "ACCEPT_SCOPED_FORMAL_CONSTRUCTOR" and
            review["organizational_independence_credit"] == 0 and review["scientific_effect"] == "NONE",
            "actual final scoped acceptance is missing")
    require(review["review"]["path"] == gates["review_text"] and
            review["review"]["sha256"] == digest(gates["review_text"]) and
            review["review"]["bytes"] == len(entries[gates["review_text"]]["raw"]), "full final review is not bound")
    for field, gate in (("source_inventory_sha256", "source_inventory"),
                        ("final_sequence_sha256", "final_sequence"),
                        ("negative_index_sha256", "negative_index"),
                        ("dependency_rehash_sha256", "dependency_rehash")):
        require(review[field] == digest(gates[gate]), "final acceptance binding mismatch: " + field)
    return {"final_phases": 24, "frozen_sources": 19,
            "negative_receipts": len(paths), "gate_hashes": {k: digest(v) for k, v in gates.items()},
            "scope": "Terminal identity and completeness gates; full semantic verification remains in the exported verifiers and final review."}


def main():
    require(len(sys.argv) == 1, "usage: python3 -B export_public_evidence.py")
    require(not FINAL.exists() and not PRIVATE_PROJECTION.exists(), "public export already exists; never overwrite")
    require(PACKAGE.is_dir() and not PACKAGE.is_symlink(), "missing regular publication package")
    manifest_bytes, config, entries, identifiers = load_inputs()
    checks = validate_actual_gates(config, entries)
    planned = []
    public_files = []
    for source, entry in sorted(entries.items(), key=lambda pair: pair[1]["destination"]):
        projected, counts = project_bytes(entry["raw"], entry["destination"], identifiers)
        public_path = "evidence/final/" + entry["destination"]
        record = {"source": source, "public_path": public_path,
                  "original_sha256": entry["sha256"], "exported_sha256": sha(projected),
                  "original_bytes": len(entry["raw"]), "exported_bytes": len(projected),
                  "role": entry["role"], "replacement_counts": counts}
        public_files.append(record)
        planned.append((entry["destination"], projected))
    common = {"schema_version": 1, "transformation": "explicit-prefix-projection-v1",
              "status": "PASS_ACTUAL_TERMINAL_EVIDENCE_PROJECTION",
              "input_manifest_sha256": sha(manifest_bytes), "exporter_sha256": sha(Path(__file__).read_bytes()),
              "checks": checks, "files": public_files,
              "known_private_identifier_count": len(identifiers),
              "scientific_effect": "NONE",
              "scope": "Derived public projection; raw and exported hashes are distinct when explicit filesystem prefixes were replaced. No original receipt outcome or full log content was omitted."}
    public_mapping = {**common, "replacements": [{"label": r["label"], "logical": r["logical"]} for r in REPLACEMENTS]}
    public_bytes = json_bytes(public_mapping)
    privacy_check(public_bytes.decode(), identifiers)
    private_mapping = {**common, "replacements": REPLACEMENTS,
                       "public_mapping_sha256": sha(public_bytes),
                       "private_identifier_inventory_sha256": sha(json_bytes(identifiers))}
    private_bytes = json_bytes(private_mapping)
    # Re-read every input immediately before the first write. This includes the
    # accepted review and manifest, so no active result can change unnoticed.
    require(MANIFEST.read_bytes() == manifest_bytes, "input manifest changed during planning")
    for source, entry in entries.items():
        require(regular_source(source).read_bytes() == entry["raw"], "input changed during planning: " + source)
    require(validate_actual_gates(config, entries) == checks, "terminal bindings changed during planning")
    staging = PACKAGE / "evidence" / ("final.pending-" + sha(manifest_bytes)[:16])
    pending_private = PRIVATE_PROJECTION.with_suffix(".json.pending")
    require(not staging.exists() and not pending_private.exists(), "interrupted export exists; inspect before recovery")
    require(not (PACKAGE / "evidence").is_symlink(), "symlink evidence directory")
    staging.mkdir()
    for relative, content in planned + [("PUBLIC_EVIDENCE_PROJECTION.json", public_bytes)]:
        target = staging.joinpath(*relative_path(relative).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(content)
        require(target.read_bytes() == content, "projected byte readback failed")
    with pending_private.open("xb") as stream:
        stream.write(private_bytes)
    require(pending_private.read_bytes() == private_bytes, "private projection readback failed")
    require(not FINAL.exists() and not PRIVATE_PROJECTION.exists(), "concurrent export detected")
    os.rename(staging, FINAL)
    os.rename(pending_private, PRIVATE_PROJECTION)
    print(json.dumps({"status": common["status"], "files": len(public_files),
                      "public_mapping_sha256": sha(public_bytes),
                      "private_mapping_sha256": sha(private_bytes)}, sort_keys=True))


if __name__ == "__main__":
    main()
