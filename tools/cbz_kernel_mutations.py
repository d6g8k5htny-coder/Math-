#!/usr/bin/env python3
"""Nine bounded source-guard mutations; crashes/errors/skips never count as kills."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = Path("tools/cbz_kernel_gate.py")
TEST = Path("tests/test_cbz_kernel_gate.py")
EXPECTED_BASELINE_TESTS = 66
CASES = [
    ("independent_census",
     'require(header_count == origins[module] + module_aliases,\n                "independent compiled census disagreement: " + render_name(module))',
     'require(True, "independent compiled census disagreement: " + render_name(module))',
     "test_independent_census_disagreement_is_refused"),
    ("unused_custom_axiom",
     'bad_declarations = [row for row in public_rows if row["kind"] not in SAFE_KINDS]',
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
     'if terminal is None:\n        terminal = (len(counts), len(declarations), len(declarations), len(unique_names), len(unique_names))',
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

def _tests(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from _tests(item)
        else:
            yield item

def child_suite(work, selector=None):
    """Bespoke collector: failures in fixture lifecycle are never test-body kills."""
    test_path = Path(work) / TEST
    spec = importlib.util.spec_from_file_location("test_cbz_kernel_gate", test_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(selector) if selector else loader.loadTestsFromModule(module)
    tests = list(_tests(suite))
    expected = [test.id() for test in tests]
    phases, started, returned = {}, [], []

    def wrap(test, attribute, phase):
        original = getattr(test, attribute)
        test_id = test.id()
        def call(*args, **kwargs):
            phases[test_id] = phase
            if phase == "body":
                started.append(test_id)
            value = original(*args, **kwargs)
            if phase == "body":
                returned.append(test_id)
            return value
        setattr(test, attribute, call)

    for test in tests:
        for attribute, phase in (("_callSetUp", "setup"), ("_callTestMethod", "body"),
                                 ("_callTearDown", "teardown"), ("doCleanups", "cleanup")):
            wrap(test, attribute, phase)

    class PhaseResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.failure_events, self.error_events = [], []
        def event(self, test, error):
            return {"test": test.id(), "phase": phases.get(test.id(), "fixture"),
                    "assertion": issubclass(error[0], AssertionError)}
        def addFailure(self, test, error):
            self.failure_events.append(self.event(test, error))
            super().addFailure(test, error)
        def addError(self, test, error):
            self.error_events.append(self.event(test, error))
            super().addError(test, error)
        def addSubTest(self, test, subtest, error):
            if error is not None:
                target = self.failure_events if issubclass(error[0], test.failureException) else self.error_events
                target.append(self.event(test, error))
            super().addSubTest(test, subtest, error)

    result = unittest.TextTestRunner(verbosity=2, resultclass=PhaseResult).run(suite)
    lifecycle = {"schema": "cbz.kernel.mutation-lifecycle/v1", "tests_run": result.testsRun,
                 "expected_ids": expected, "body_started": started, "body_returned": returned,
                 "failure_events": result.failure_events, "error_events": result.error_events,
                 "skipped": len(result.skipped), "expected_failures": len(result.expectedFailures),
                 "unexpected_successes": len(result.unexpectedSuccesses)}
    print("CBZM|" + json.dumps(lifecycle, sort_keys=True))
    return 0 if result.wasSuccessful() else 1

def suite_result(returncode, output):
    runs = re.findall(r"^Ran ([0-9]+) tests? in .+$", output, re.M)
    summaries = re.findall(r"^(?:OK(?: \([^\n]*\))?|FAILED \([^\n]*\))$", output, re.M)
    records = re.findall(r"^CBZM\|([^\n]+)$", output, re.M)
    valid = len(runs) == len(summaries) == len(records) == 1
    summary = summaries[0] if summaries else ""
    counts = {}
    if "(" in summary:
        for entry in summary.split("(", 1)[1].removesuffix(")").split(","):
            if "=" in entry:
                key, value = entry.strip().rsplit("=", 1)
                if key in {"failures", "errors", "skipped"} and value.isdigit():
                    counts[key] = int(value)
    lifecycle = {}
    if valid:
        try:
            def unique(pairs):
                row = {}
                for key, value in pairs:
                    if key in row:
                        raise ValueError("duplicate lifecycle key")
                    row[key] = value
                return row
            lifecycle = json.loads(records[0], object_pairs_hook=unique)
            required = {"schema", "tests_run", "expected_ids", "body_started", "body_returned",
                        "failure_events", "error_events", "skipped", "expected_failures", "unexpected_successes"}
            valid = (isinstance(lifecycle, dict) and set(lifecycle) == required
                     and lifecycle["schema"] == "cbz.kernel.mutation-lifecycle/v1")
            for field in ("tests_run", "skipped", "expected_failures", "unexpected_successes"):
                valid = valid and type(lifecycle[field]) is int and lifecycle[field] >= 0
            for field in ("expected_ids", "body_started", "body_returned"):
                values = lifecycle[field]
                valid = valid and isinstance(values, list) and all(isinstance(v, str) and v for v in values)
                valid = valid and len(values) == len(set(values))
            for field in ("failure_events", "error_events"):
                values = lifecycle[field]
                valid = valid and isinstance(values, list) and all(
                    isinstance(v, dict) and set(v) == {"test", "phase", "assertion"}
                    and isinstance(v["test"], str) and v["phase"] in {"setup", "body", "teardown", "cleanup", "fixture"}
                    and type(v["assertion"]) is bool for v in values)
            valid = valid and lifecycle["tests_run"] == int(runs[0])
            valid = valid and len(lifecycle["failure_events"]) == counts.get("failures", 0)
            valid = valid and len(lifecycle["error_events"]) == counts.get("errors", 0)
            valid = valid and lifecycle["skipped"] == counts.get("skipped", 0)
        except (ValueError, TypeError, KeyError):
            valid, lifecycle = False, {}
    return {"returncode": returncode, "valid_protocol": bool(valid),
            "tests_run": int(runs[0]) if len(runs) == 1 else 0,
            "assertion_failures": counts.get("failures", 0), "test_errors": counts.get("errors", 0),
            "tests_skipped": counts.get("skipped", 0),
            "failing_tests": [row["test"] for row in lifecycle.get("failure_events", [])],
            "error_tests": [row["test"] for row in lifecycle.get("error_events", [])],
            "has_assertion_error": "AssertionError" in output, "summary": summary,
            "expected_tests": lifecycle.get("expected_ids", []),
            "body_started": lifecycle.get("body_started", []), "body_returned": lifecycle.get("body_returned", []),
            "failure_events": lifecycle.get("failure_events", []), "error_events": lifecycle.get("error_events", []),
            "expected_failures": lifecycle.get("expected_failures", 0),
            "unexpected_successes": lifecycle.get("unexpected_successes", 0)}

def require_baseline(result):
    expected = result["expected_tests"]
    require(result["valid_protocol"] and result["returncode"] == 0
            and result["tests_run"] == EXPECTED_BASELINE_TESTS and len(expected) == EXPECTED_BASELINE_TESTS
            and result["body_started"] == result["body_returned"] == expected
            and result["assertion_failures"] == result["test_errors"] == result["tests_skipped"] == 0
            and result["expected_failures"] == result["unexpected_successes"] == 0
            and not result["failing_tests"] and not result["error_tests"] and result["summary"] == "OK",
            "unmodified baseline is not healthy in every declared test body")

def require_kill(result, selector):
    event = {"test": selector, "phase": "body", "assertion": True}
    require(result["valid_protocol"] and result["returncode"] == 1 and result["tests_run"] == 1
            and result["assertion_failures"] == 1 and result["test_errors"] == result["tests_skipped"] == 0
            and result["expected_failures"] == result["unexpected_successes"] == 0
            and result["expected_tests"] == result["body_started"] == [selector]
            and result["failure_events"] == [event] and not result["error_events"]
            and result["failing_tests"] == [selector] and result["has_assertion_error"],
            "mutant was not killed by its selected test-body assertion; fixture failures/errors/skips are not kills")

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
    command = [sys.executable, "-B", "-S", *(["-O"] if mode == "optimized" else []),
               str(Path(__file__).resolve()), "--_child-root", str(work)]
    if selector:
        command += ["--_child-selector", selector]
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
        binding = {"tool_sha256": sha(source.encode()), "test_sha256": sha(tests), "runner_sha256": sha(Path(__file__).read_bytes())}
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
                and sha((ROOT / TEST).read_bytes()) == binding["test_sha256"]
                and sha(Path(__file__).read_bytes()) == binding["runner_sha256"],
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
    parser.add_argument("--_child-root", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--_child-selector", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args._child_root is not None:
        return child_suite(args._child_root, args._child_selector)
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

