#!/usr/bin/env python3
"""Nine bounded source-guard mutations; crashes/errors/skips never count as kills."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
TOOL = Path("tools/cbz_kernel_gate.py")
TEST = Path("tests/test_cbz_kernel_gate.py")
EXPECTED_BASELINE_TESTS = 52
CASES = [
    ("independent_census",
     'require(first == second, "independent compiled census disagreement: " + render_name(name))',
     'require(True, "independent compiled census disagreement: " + render_name(name))',
     "test_independent_census_disagreement_is_refused"),
    ("unused_custom_axiom",
     'bad_declarations = [row for row in declarations if row["kind"] not in SAFE_KINDS]',
     'bad_declarations = []',
     "test_unused_custom_axiom_is_refused_even_with_empty_union"),
    ("unsafe_definition",
     'SAFE_KINDS = frozenset({"theorem", "def", "inductive", "ctor", "rec"})',
     'SAFE_KINDS = frozenset({"theorem", "def", "inductive", "ctor", "rec", "unsafe"})',
     "test_unsafe_definition_is_refused"),
    ("transitive_sorry",
     'bad = set(axioms) - ALLOWED_AXIOM_NAMES',
     'bad = set()',
     "test_transitive_sorry_is_refused"),
    ("head_blob_binding",
     'require(blob == entry["blob"], "consumed bytes differ from HEAD blob: " + relative)',
     'require(True, "consumed bytes differ from HEAD blob: " + relative)',
     "test_assume_unchanged_cannot_hide_bytes_from_commit_attestation"),
    ("dependency_link_payload_binding",
     'require(link_blob == entry["blob"] and data.hex() == reviewed["payload_hex"],\n                    "symlink payload differs from HEAD blob: " + relative)',
     'require(True, "symlink payload differs from HEAD blob: " + relative)',
     "test_changed_reviewed_link_target_cannot_hide_behind_clean_git_status"),
    ("source_subdirectory_omission",
     'if stat.S_ISDIR(mode):\n                    walk(path)',
     'if stat.S_ISDIR(mode):\n                    continue',
     "test_unreadable_source_directory_is_refused_even_for_privileged_runner"),
    ("terminal_completeness",
     'require(terminal is not None, "missing END audit marker")',
     'if terminal is None:\n        terminal = (len(counts), len(declarations), len(declarations))',
     "test_missing_terminal_marker_is_refused"),
    ("native_control_nontheorem",
     'require(any(row["kind"] == "theorem" and decode_name(row["encoded_name"]) == ("unusedCBZNative",)\n                        for row in exc.declarations), "native control omitted its actual theorem")',
     'require(True, "native control omitted its actual theorem")',
     "test_native_control_requires_the_actual_named_theorem"),
]

class MutationError(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise MutationError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def suite_result(returncode, output):
    runs = re.findall(r"^Ran ([0-9]+) tests? in .+$", output, re.M)
    summaries = re.findall(r"^(?:OK(?: \([^\n]*\))?|FAILED \([^\n]*\))$", output, re.M)
    valid = len(runs) == 1 and len(summaries) == 1
    summary = summaries[0] if valid else ""
    counts = dict(re.findall(r"(failures|errors|skipped)=([0-9]+)", summary))
    return {"returncode": returncode, "valid_protocol": valid,
            "tests_run": int(runs[0]) if valid else 0,
            "assertion_failures": int(counts.get("failures", 0)),
            "test_errors": int(counts.get("errors", 0)),
            "tests_skipped": int(counts.get("skipped", 0)),
            "failing_tests": re.findall(r"^FAIL: [^\n]* \(([^\n)]+)\)$", output, re.M),
            "error_tests": re.findall(r"^ERROR: [^\n]* \(([^\n)]+)\)$", output, re.M),
            "has_assertion_error": "AssertionError" in output,
            "summary": summary}

def require_baseline(result):
    require(result["valid_protocol"] and result["returncode"] == 0
            and result["tests_run"] == EXPECTED_BASELINE_TESTS
            and result["assertion_failures"] == result["test_errors"] == result["tests_skipped"] == 0
            and not result["failing_tests"] and not result["error_tests"]
            and result["summary"].startswith("OK"), "unmodified 52-test baseline is not healthy")

def require_kill(result, selector):
    require(result["valid_protocol"] and result["returncode"] == 1 and result["tests_run"] == 1
            and result["assertion_failures"] == 1 and result["test_errors"] == 0
            and result["tests_skipped"] == 0 and result["failing_tests"] == [selector]
            and not result["error_tests"] and result["has_assertion_error"],
            "mutant was not killed by its one intended assertion; errors/skips/crashes are not kills")

def apply_mutation(source, before, after):
    require(before != after and source.count(before) == 1, "stale, duplicate or no-op mutation anchor")
    changed = source.replace(before, after, 1)
    require(changed != source, "unchanged mutation")
    try:
        compile(changed, "<cbz-kernel-mutant>", "exec")
    except SyntaxError as exc:
        raise MutationError("mutant does not compile") from exc
    return changed

def run_suite(work, output, label, mode, selector=None):
    command = [sys.executable, "-B", "-S", *(["-O"] if mode == "optimized" else [])]
    if selector:
        command += ["-m", "unittest", selector, "-v"]
        cwd = work / "tests"
    else:
        command += ["-m", "unittest", "discover", "-s", "tests", "-p", TEST.name, "-v"]
        cwd = work
    environment = {k: v for k, v in os.environ.items()
                   if k not in {"PYTHONHOME", "PYTHONPATH", "PYTHONOPTIMIZE", "PYTHONSTARTUP", "PYTHONINSPECT"}}
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        child = subprocess.run(command, cwd=cwd, env=environment, capture_output=True, text=True, timeout=60)
        stdout, stderr, code = child.stdout, child.stderr, child.returncode
    except subprocess.TimeoutExpired as exc:
        def text(value):
            return value.decode("utf-8", "backslashreplace") if isinstance(value, bytes) else value or ""
        stdout, stderr, code = text(exc.stdout), text(exc.stderr), 124
    except OSError as exc:
        stdout, stderr, code = "", str(exc), 127
    path = output / (label + "-" + mode + ".log")
    path.write_text(stdout + stderr)
    result = suite_result(code, stdout + stderr)
    result.update(command=command, cwd=str(cwd), log=path.name, log_sha256=sha(path.read_bytes()))
    return result

def execute(output):
    require(not output.is_symlink(), "symlink mutation output")
    if output.exists() and any(output.iterdir()):
        previous = output.with_name(output.name + ".previous-" + uuid.uuid4().hex)
        output.replace(previous)
        output.mkdir(parents=True)
        (output / "history").mkdir()
        previous.replace(output / "history" / previous.name)
    else:
        output.mkdir(parents=True, exist_ok=True)
    report = {"schema_version": 1, "status": "RUNNING", "scope": "Nine Python source guards only; generated Lean mutation is executed by the real control preflight.",
              "source_binding": None, "expected_baseline_tests": EXPECTED_BASELINE_TESTS,
              "declared_mutants": len(CASES), "baselines": {}, "mutants": []}
    output.mkdir(parents=True, exist_ok=True)
    def retain():
        (output / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    retain()
    try:
        require(CASES and len({c[0] for c in CASES}) == len(CASES), "empty or duplicate declared mutation inventory")
        source = (ROOT / TOOL).read_text()
        tests = (ROOT / TEST).read_bytes()
        binding = {"tool_sha256": sha(source.encode()), "test_sha256": sha(tests)}
        report["source_binding"] = binding
        retain()
        # Check every declared location before running; a stale case is never dropped.
        mutated = {name: apply_mutation(source, before, after) for name, before, after, _ in CASES}
        with tempfile.TemporaryDirectory(prefix="cbz-kernel-mutations-") as temp:
            work = Path(temp)
            (work / TOOL.parent).mkdir()
            (work / TEST.parent).mkdir()
            (work / TOOL).write_text(source)
            (work / TEST).write_bytes(tests)
            for mode in ("normal", "optimized"):
                result = run_suite(work, output, "baseline", mode)
                report["baselines"][mode] = result
                retain()
                require_baseline(result)
            for name, before, after, method in CASES:
                selector = "test_cbz_kernel_gate.NativeGateTests." + method
                row = {"id": name, "selector": selector, "mutation_location_count": 1,
                       "mutated_source_sha256": sha(mutated[name].encode()), "runs": {}}
                report["mutants"].append(row)
                (work / TOOL).write_text(mutated[name])
                try:
                    for mode in ("normal", "optimized"):
                        result = run_suite(work, output, name, mode, selector)
                        row["runs"][mode] = result
                        retain()
                        require_kill(result, selector)
                    row["outcome"] = "KILLED_BY_INTENDED_ASSERTION_IN_BOTH_MODES"
                finally:
                    (work / TOOL).write_text(source)
                retain()
        require(sha((ROOT / TOOL).read_bytes()) == binding["tool_sha256"]
                and sha((ROOT / TEST).read_bytes()) == binding["test_sha256"],
                "auditor source/test changed during mutation execution")
        report.update(status="PASS", killed_mutants=len(report["mutants"]),
                      threshold="All nine declared nonstale mutants killed in both modes; zero errors/skips/startup failures")
        retain()
        return report
    except (MutationError, OSError, ValueError, TypeError) as exc:
        report.update(status="REFUSED", reason=str(exc))
        retain()
        raise

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(".lake/cbz-kernel/mutations"))
    args = parser.parse_args(argv)
    output = args.output if args.output.is_absolute() else ROOT / args.output
    try:
        report = execute(output)
    except (MutationError, OSError, ValueError, TypeError) as exc:
        print("CBZ kernel mutation gate REFUSED: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps({"status": report["status"], "declared_mutants": report["declared_mutants"],
                      "killed_mutants": report["killed_mutants"], "scope": report["scope"]}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

