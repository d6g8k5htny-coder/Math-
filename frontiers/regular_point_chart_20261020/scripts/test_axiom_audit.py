"""Hosted real-Lean controls for the C296 axiom policy; no scientific acceptance.

Run from the package after its pinned dependencies and RegularPointChart build
exist. Every fixture is a separate source copy under .lake/c296-audit-evidence;
production Lean sources are never changed. This script does not install tools.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "RegularPointChartAxiomAudit.lean"
PREFIX = "UniversalLaw.Spec.Lifetime."
REQUIRED = (
    PREFIX + "regularPointDerivative_range_eq_top",
    PREFIX + "regularPointHasStrictFDerivAt",
    PREFIX + "regularPointChart",
    PREFIX + "regularPointChart_fst",
    PREFIX + "regularPointChart_self",
    PREFIX + "mem_regularPointChart_source",
    PREFIX + "mem_regularPointChart_target",
)
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
AUDITED_ANCHOR = "  let audited := names\n"
ALLOWLIST_ANCHOR = (
    "  let allowed : List Name := [`propext, `Classical.choice, `Quot.sound]\n"
)
BLOCK_ANCHOR = "open Lean Elab Command in\nrun_cmd do\n"
CONTAMINATION = (
    "axiom C296Forbidden : False\n"
    "theorem C296Contaminated : False := C296Forbidden\n\n"
)
TIMEOUT_SECONDS = 90
MAX_READ_BYTES = 4 * 1024 * 1024


class ControlFailure(RuntimeError):
    """An expected semantic behavior was absent, distinct from process setup."""


def require(condition, message):
    if not condition:
        raise ControlFailure(message)


def replace_once(source, old, new):
    require(source.count(old) == 1, "fixture anchor missing or nonunique: " + repr(old))
    return source.replace(old, new, 1)


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def source_snapshot():
    paths = [p for p in ROOT.iterdir() if p.is_file()]
    paths += [p for p in (ROOT / "scripts").iterdir() if p.is_file()]
    paths += [ROOT.parent / "critical_level_attainment_20261020/final-project/Lifetime.lean",
              ROOT.parents[1] / ".github/workflows/c296-regular-point-chart.yml"]
    return {str(p.relative_to(ROOT.parents[1])): sha(p) for p in sorted(paths)}


def save_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def emit_evidence(directory, report):
    # The hosted job has no artifact upload: retain readable evidence in its log
    # even when a semantic validator fails. Raw files remain unchanged on disk.
    for record in report["processes"]:
        for stream in ("stdout", "stderr"):
            path = directory / (record["case"] + "." + stream)
            with path.open("rb") as handle:
                raw = handle.read(MAX_READ_BYTES)
            metadata = {"case": record["case"], "stream": stream,
                        "sha256": record[stream + "_sha256"],
                        "total_bytes": record[stream + "_bytes"],
                        "emitted_bytes": len(raw),
                        "truncated": record[stream + "_bytes"] > len(raw),
                        "decoding": "utf-8 with replacement for invalid bytes"}
            print("=== C296_AUDIT_STREAM_BEGIN " + json.dumps(metadata, sort_keys=True) + " ===")
            decoded = raw.decode("utf-8", "replace")
            print(decoded, end="" if decoded.endswith("\n") else "\n")
            print("=== C296_AUDIT_STREAM_END " + record["case"] + " " + stream + " ===")
    print("=== C296_AUDIT_RESULT_BEGIN ===")
    print(json.dumps(report, indent=2, sort_keys=True))
    print("=== C296_AUDIT_RESULT_END ===")


def stop_child(process):
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=5)


def run_lean(directory, label, source, report):
    source_path = directory / (label + ".lean")
    source_path.write_text(source, encoding="utf-8")
    stdout_path = directory / (label + ".stdout")
    stderr_path = directory / (label + ".stderr")
    command = ["lake", "env", "lean", str(source_path)]
    record = {"case": label, "command": command, "cwd": str(ROOT),
              "source_sha256": sha(source_path), "timeout_seconds": TIMEOUT_SECONDS,
              "timed_out": False, "spawn_error": None, "cleanup_error": None,
              "exit_code": None, "classification": "NOT_CLASSIFIED"}
    process = None
    started = time.monotonic()
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        try:
            process = subprocess.Popen(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                       start_new_session=True)
            try:
                record["exit_code"] = process.wait(timeout=TIMEOUT_SECONDS)
            except subprocess.TimeoutExpired:
                record["timed_out"] = True
        except OSError as error:
            record["spawn_error"] = repr(error)
        finally:
            if process is not None:
                try:
                    stop_child(process)
                except (OSError, subprocess.TimeoutExpired) as error:
                    record["cleanup_error"] = repr(error)
                record["exit_code"] = process.poll()
    record["duration_seconds"] = time.monotonic() - started
    for name, path in (("stdout", stdout_path), ("stderr", stderr_path)):
        record[name + "_bytes"] = path.stat().st_size
        record[name + "_sha256"] = sha(path)
    report["processes"].append(record)
    save_json(directory / (label + ".receipt.json"), record)
    save_json(directory / "RESULT.json", report)
    require(not record["timed_out"], label + ": PROCESS_TIMEOUT, not a policy rejection")
    require(record["spawn_error"] is None, label + ": PROCESS_SETUP_FAILURE")
    require(record["cleanup_error"] is None, label + ": PROCESS_CLEANUP_FAILURE")
    require(max(record["stdout_bytes"], record["stderr_bytes"]) <= MAX_READ_BYTES,
            label + ": OUTPUT_LIMIT, not a policy rejection")
    stdout = stdout_path.read_bytes().decode("utf-8", "strict")
    stderr = stderr_path.read_bytes().decode("utf-8", "strict")
    return record, stdout, stderr, source_path


def policy_records(stdout):
    declarations = {}
    for line in stdout.splitlines():
        match = re.search(r"(?:^|: info: )C296_AXIOM_DECL (\S+) AXIOMS \[([^\]]*)\]$", line)
        if match:
            name, axioms = match.groups()
            require(name not in declarations, "duplicate audit declaration: " + name)
            declarations[name] = {a.strip() for a in axioms.split(",") if a.strip()}
    return declarations


def successful_audit(result, allowed=ALLOWED):
    record, stdout, stderr, _ = result
    require(record["exit_code"] == 0, record["case"] + ": audit did not succeed")
    require(stderr == "" and "error:" not in stdout,
            record["case"] + ": successful audit has error output")
    declarations = policy_records(stdout)
    require(set(REQUIRED) <= set(declarations), "successful audit omitted a required target")
    counts = re.findall(r"(?:^|: info: )C296_AXIOM_POLICY_PASS COUNT ([0-9]+)$", stdout, re.M)
    require(len(counts) == 1 and int(counts[0]) == len(declarations),
            "missing or inconsistent audit completion inventory")
    for name, axioms in declarations.items():
        require(axioms <= allowed, "successful audit admitted forbidden axioms at " + name)
    return declarations


def policy_rejection(result, marker, detail=None):
    record, stdout, stderr, source_path = result
    require(record["exit_code"] == 1, record["case"] + ": expected policy exit 1")
    require(stderr == "", record["case"] + ": policy diagnostic unexpectedly on stderr")
    # An intended exception must be the sole error at this exact fixture source.
    errors = [line for line in stdout.splitlines() if "error:" in line]
    pattern = re.escape(str(source_path)) + r":\d+:\d+: error: " + re.escape(marker) + r"(?:\s.*)?$"
    require(len(errors) == 1 and re.fullmatch(pattern, errors[0]) is not None,
            record["case"] + ": unrelated/setup/syntax error is not the policy rejection")
    require("C296_AXIOM_POLICY_PASS" not in stdout, "rejected audit printed a success marker")
    if detail is not None:
        require(detail in errors[0], record["case"] + ": wrong policy witness")


def classified_failure(result, diagnostic_pattern, classification):
    record, stdout, stderr, source_path = result
    require(record["exit_code"] == 1, classification + ": wrong exit status")
    require(stderr == "", classification + ": unexpected stderr")
    errors = [line for line in stdout.splitlines() if "error:" in line]
    prefix = re.escape(str(source_path)) + r":\d+:\d+: error: "
    require(len(errors) == 1 and re.match(prefix, errors[0]) is not None,
            classification + ": missing source-bound error")
    require(re.search(diagnostic_pattern, errors[0]) is not None,
            classification + ": unexpected diagnostic")
    require("C296_AXIOM_" not in stdout, classification + ": masquerading as policy output")
    try:
        policy_rejection(result, "C296_AXIOM_FORBIDDEN", "C296Forbidden")
    except ControlFailure:
        return
    raise ControlFailure(classification + ": incorrectly accepted as a policy rejection")


def main():
    evidence = ROOT / ".lake/c296-audit-evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="run-", dir=evidence))
    report = {"schema_version": 1, "status": "FAIL", "scientific_effect": "NONE",
              "python_optimized": bool(sys.flags.optimize), "processes": [],
              "controls": [], "evidence_directory": str(directory)}
    before = source_snapshot()
    report["source_before"] = before
    save_json(directory / "RESULT.json", report)

    def check(label, source, validator, classification):
        result = run_lean(directory, label, source, report)
        validator(result)
        result[0]["classification"] = classification
        save_json(directory / (label + ".receipt.json"), result[0])
        report["controls"].append({"case": label, "classification": classification})
        save_json(directory / "RESULT.json", report)
        return result

    try:
        candidate = AUDIT.read_text(encoding="utf-8")
        print_only = "import RegularPointChart\n\n" + "\n".join(
            "#print axioms " + name for name in REQUIRED) + "\n"
        # This is the original seven-print audit plus one explicit contamination
        # witness. Its rc0 must demonstrate the old policy defect, not setup RED.
        old_contaminated = print_only + "\n" + CONTAMINATION + "#print axioms C296Contaminated\n"

        def old_printing_only(result):
            record, stdout, stderr, _ = result
            require(record["exit_code"] == 0 and stderr == "" and "error:" not in stdout,
                    "printing-only baseline must elaborate successfully")
            require(all(name in stdout for name in REQUIRED), "baseline target output missing")
            require(re.search(r"C296Contaminated[^\n]*depends on axioms[^\n]*C296Forbidden", stdout)
                    is not None, "baseline did not expose the transitive forbidden axiom")
            require("C296_AXIOM_POLICY_PASS" not in stdout, "baseline was not printing-only")

        check("printing-only-forbidden", old_contaminated, old_printing_only,
              "BASELINE_POLICY_DEFECT_OBSERVED_EXIT_ZERO")
        check("positive", candidate, successful_audit, "COMPLETE_ALLOWED_INVENTORY")
        contaminated = replace_once(candidate, BLOCK_ANCHOR, CONTAMINATION + BLOCK_ANCHOR)
        contaminated = replace_once(contaminated, AUDITED_ANCHOR,
                                    "  let audited := names.push `C296Contaminated\n")
        check("forbidden", contaminated,
              lambda r: policy_rejection(r, "C296_AXIOM_FORBIDDEN", "C296Forbidden"),
              "TRANSITIVE_FORBIDDEN_AXIOM_REJECTED")
        missing = replace_once(candidate, AUDITED_ANCHOR,
                               "  let audited := names.filter (· != `" + REQUIRED[-1] + ")\n")
        check("missing-target", missing,
              lambda r: policy_rejection(r, "C296_AXIOM_MISSING_TARGET", REQUIRED[-1]),
              "MISSING_REQUIRED_TARGET_REJECTED")
        empty = replace_once(candidate, AUDITED_ANCHOR, "  let audited := (#[] : Array Name)\n")
        check("empty-inventory", empty, lambda r: policy_rejection(r, "C296_AXIOM_EMPTY"),
              "EMPTY_AUDITED_INVENTORY_REJECTED")
        weakened = replace_once(contaminated, ALLOWLIST_ANCHOR,
                                ALLOWLIST_ANCHOR.rstrip("\n")[:-1] + ", `C296Forbidden]\n")

        def kill_allowlist_mutant(result):
            declarations = successful_audit(result, ALLOWED | {"C296Forbidden"})
            require("C296Forbidden" in declarations.get("C296Contaminated", set()),
                    "allowlist mutant did not exercise transitive contamination")
            try:
                policy_rejection(result, "C296_AXIOM_FORBIDDEN", "C296Forbidden")
            except ControlFailure as error:
                report["allowlist_mutant_rejection_failure"] = str(error)
                return
            raise ControlFailure("forbidden-axiom control failed to kill weakened allowlist")

        check("allowlist-weakened", weakened, kill_allowlist_mutant,
              "WEAKENED_ALLOWLIST_KILLED_BY_FORBIDDEN_CONTROL")
        check("setup-failure", "import C296FixtureMissingModuleNeverPublished\n",
              lambda r: classified_failure(r,
                  r"unknown module prefix 'C296FixtureMissingModuleNeverPublished'|"
                  r"object file .*C296FixtureMissingModuleNeverPublished.*does not exist",
                  "SETUP_FAILURE"), "SETUP_FAILURE_NOT_POLICY_REJECTION")
        check("syntax-failure", "import RegularPointChart\ndef C296Broken : Nat := )\n",
              lambda r: classified_failure(r, r"unexpected token '\)'", "SYNTAX_FAILURE"),
              "SYNTAX_FAILURE_NOT_POLICY_REJECTION")
        require(len(report["controls"]) == 8, "incomplete audit-control campaign")
        report["status"] = "PASS_ENGINEERING_CONTROLS_ONLY"
    except Exception as error:
        report["failure"] = type(error).__name__ + ": " + str(error)
    finally:
        after = source_snapshot()
        report["source_after"] = after
        report["production_sources_unchanged"] = before == after
        if before != after:
            report["status"] = "FAIL"
            report["source_failure"] = "production source bytes changed"
        save_json(directory / "RESULT.json", report)
        emit_evidence(directory, report)
    print(json.dumps({"status": report["status"], "evidence_directory": str(directory),
                      "controls_completed": len(report["controls"]),
                      "scientific_effect": "NONE"}, sort_keys=True))
    return 0 if report["status"] == "PASS_ENGINEERING_CONTROLS_ONLY" else 1


if __name__ == "__main__":
    sys.exit(main())
