#!/usr/bin/env python3
"""Bounded C8 source mutations with structured unittest and per-CLI health evidence."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).absolute().parents[1]
TOOL = Path("tools/check_c8_quarantine.py")
TEST = Path("tests/test_c8_quarantine.py")
PACKET = Path("frontiers/c8_elder_failure_coefficient_20261001")
RECORD = Path("quarantine/Q-C8-ELDER-FAILURE-BINARY64-20261029.json")
EXPECTED_TESTS = 41
CASES = [
    ("admission_flag", 'require(doc.get("cbz_certificate_admitted") is False, "certificate admission must remain false")',
     'require(True, "certificate admission must remain false")', "test_record_admission_must_be_typed_false", 1),
    ("frozen_manifest", 'require(blob(raw) == MANIFEST_BLOB, "frozen packet manifest identity differs")',
     'require(True, "frozen packet manifest identity differs")', "test_refreshed_manifest_cannot_rebind_changed_sources", 1),
    ("source_bytes", 'require(all(actual[k] == entry[k] for k in ("git_blob", "sha256", "bytes")),',
     'require(True,', "test_changed_source_cannot_rebind_only_quarantine_metadata", 1),
    ("denied_bijection", 'and {v["json_pointer"] for v in listed} == set(denied)',
     'and True', "test_denied_inventory_cannot_duplicate_or_change_an_endpoint", 1),
    ("denied_endpoints", 'and all(v == denied[v["json_pointer"]] for v in listed)',
     'and True', "test_denied_interval_endpoints_cannot_be_rewritten", 1),
    ("exact_inventory", 'require(doc.get("exact_rational_exceptions") == exceptions, "exact rational exception inventory differs")',
     'require(True, "exact rational exception inventory differs")', "test_false_exact_rational_witness_refuses", 1),
    ("fraction_containment", 'require(F(pair[0]) <= exact <= F(pair[1]), "exact rational containment failed")',
     'require(True, "exact rational containment failed")', "test_fraction_checker_rejects_a_false_endpoint", 0),
    ("source_denial", 'if denied:\n                report["problems"].append("quarantined numerical source: " + path)',
     'if False:\n                report["problems"].append("quarantined numerical source: " + path)', "test_direct_packet_source_refuses", 1),
    ("output_denial", 'if path in checked["denied"]:', 'if False:',
     "test_all_106_published_denied_outputs_are_mechanically_denied", 1),
    ("renamed_copy", 'denied = blob(regular(root, path)) in checked["copied"]',
     'denied = False', "test_renamed_c8_result_copy_cannot_evade_denial", 1),
    ("shared_engine_scope", 'COPY_SOURCES = ("RESULTS.json", "certificate.py", "boxes.py", "torus.py")',
     'COPY_SOURCES = ("RESULTS.json", "certificate.py", "boxes.py", "torus.py", "ia.py")',
     "test_shared_ia_or_c2_source_is_not_quarantined_by_byte_equality", 1),
    ("index_typed_false", 'and entry == wanted and entry.get("cbz_certificate_admitted") is False,',
     'and entry == wanted,', "test_index_boolean_false_cannot_be_replaced_by_zero", 1),
    ("unknown_admission", '        code = 2', '        code = 0', "test_unknown_output_is_not_coverage_or_admission", 1),
]

HELPER = r'''
import importlib.util,json,pathlib,subprocess,sys,unittest
work=pathlib.Path(sys.argv[1]);result_path=pathlib.Path(sys.argv[2]);selector=sys.argv[3]
spec=importlib.util.spec_from_file_location("test_c8_quarantine",work/"tests/test_c8_quarantine.py")
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
try:
    cmd=[sys.executable,"-B","-S",*(["-O"] if sys.flags.optimize else []),str(t.SCRIPT),"--root",str(work)]
    child=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
    smoke=t.observe_cli(child)
    smoke["healthy"]=smoke["healthy"] and child.returncode==0 and json.loads(child.stdout).get("status")=="QUARANTINE_INTEGRITY_OK"
except (OSError,subprocess.TimeoutExpired,ValueError,UnicodeError) as exc:
    smoke={"healthy":False,"problems":[type(exc).__name__]}
t.CLI_HEALTH.clear()
_PHASE_COUNTERS = ('setup_entered', 'setup_completed', 'body_entered', 'body_exited',
                   'teardown_entered', 'teardown_completed', 'cleanup_entered', 'cleanup_completed',
                   'failure_count', 'error_count')
_ACTIVE_TEST = None


class PhaseResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lifecycle = {'schema': 'unittest.body-phase/v1', 'tests': [], 'events': []}

    def startTest(self, test):
        global _ACTIVE_TEST
        supported = all(getattr(type(test), name) is getattr(unittest.TestCase, name)
                        for name in ('run', '_callSetUp', '_callTestMethod', '_callTearDown',
                                     '_callCleanup', 'doCleanups'))
        row = {'id': test.id(), 'supported': supported, **{name: 0 for name in _PHASE_COUNTERS}}
        test._qualification_record = row; test._qualification_phase = 'start'
        self.lifecycle['tests'].append(row); _ACTIVE_TEST = test
        super().startTest(test)

    def stopTest(self, test):
        global _ACTIVE_TEST
        _ACTIVE_TEST = None
        super().stopTest(test)

    def event(self, test, kind, err):
        event = {'id': test.id(), 'phase': getattr(test, '_qualification_phase', 'unknown'),
                 'kind': kind, 'exception': err[0].__name__, 'assertion': issubclass(err[0], AssertionError)}
        self.lifecycle['events'].append(event)
        row = getattr(test, '_qualification_record', None)
        if row is not None: row['failure_count' if kind == 'failure' else 'error_count'] += 1

    def addFailure(self, test, err):
        self.event(test, 'failure', err); super().addFailure(test, err)

    def addError(self, test, err):
        self.event(test, 'error', err); super().addError(test, err)

    def addSubTest(self, test, subtest, err):
        if err is not None:
            self.event(test, 'failure' if issubclass(err[0], test.failureException) else 'error', err)
        super().addSubTest(test, subtest, err)


def install_phases():
    originals = {}
    for method, phase, entered, completed in (
        ('_callSetUp', 'setup', 'setup_entered', 'setup_completed'),
        ('_callTestMethod', 'body', 'body_entered', 'body_exited'),
        ('_callTearDown', 'teardown', 'teardown_entered', 'teardown_completed'),
        ('_callCleanup', 'cleanup', 'cleanup_entered', 'cleanup_completed'),
    ):
        original = getattr(unittest.TestCase, method); originals[method] = original
        def tracked(test, *args, _original=original, _phase=phase, _entered=entered, _completed=completed, **kwargs):
            test._qualification_phase = _phase
            row = getattr(test, '_qualification_record', None)
            if row is None: return _original(test, *args, **kwargs)
            row[_entered] += 1
            if _phase == 'body':
                try: return _original(test, *args, **kwargs)
                finally: row[_completed] += 1
            answer = _original(test, *args, **kwargs)
            row[_completed] += 1
            return answer
        setattr(unittest.TestCase, method, tracked)
    return originals

class Result(PhaseResult):
    def __init__(self,*args):
        super().__init__(*args);self.bad=[];self.broken=[]
    def addFailure(self,test,err):
        self.bad.append({"id":test.id(),"kind":err[0].__name__});super().addFailure(test,err)
    def addError(self,test,err):
        self.broken.append({"id":test.id(),"kind":err[0].__name__});super().addError(test,err)
    def addSubTest(self,test,subtest,err):
        if err is not None:
            target=self.bad if issubclass(err[0],test.failureException) else self.broken
            target.append({"id":test.id(),"kind":err[0].__name__})
        super().addSubTest(test,subtest,err)
suite=unittest.TestSuite([t.C8Quarantine(selector.rsplit(".",1)[-1])]) if selector else unittest.defaultTestLoader.loadTestsFromTestCase(t.C8Quarantine)
selected_ids=[test.id() for test in suite]
originals=install_phases()
original_observe=t.observe_cli
def observed_cli(child):
    row=original_observe(child)
    row.update(test_id=_ACTIVE_TEST.id() if _ACTIVE_TEST is not None else None,
               phase=getattr(_ACTIVE_TEST,"_qualification_phase","unknown"))
    return row
t.observe_cli=observed_cli
try:r=unittest.TextTestRunner(stream=sys.stderr,verbosity=2,resultclass=Result).run(suite)
finally:
    for name,original in originals.items():setattr(unittest.TestCase,name,original)
    t.observe_cli=original_observe
report={"tests_run":r.testsRun,"failures":r.bad,"errors":r.broken,"skipped":[x.id() for x,_ in r.skipped],"cli_health":t.CLI_HEALTH,"smoke":smoke,"selected_ids":selected_ids,"lifecycle":r.lifecycle,"expected_failures":[x.id() for x,_ in r.expectedFailures],"unexpected_successes":[x.id() for x in r.unexpectedSuccesses]}
result_path.write_text(json.dumps(report,indent=2)+"\n")
raise SystemExit(0 if r.wasSuccessful() else 1)
'''


class MutationError(ValueError):
    pass


def require(condition, message):
    if not condition:raise MutationError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def apply_mutation(source, before, after):
    require(before != after and source.count(before) == 1, "stale, duplicate or no-op mutation anchor")
    changed = source.replace(before, after, 1)
    try:compile(changed, "<c8-source-mutant>", "exec")
    except SyntaxError as exc:raise MutationError("noncompiling mutant") from exc
    return changed


def body_evidence(lifecycle, expected, failure_ids):
    counters = {'setup_entered', 'setup_completed', 'body_entered', 'body_exited',
                'teardown_entered', 'teardown_completed', 'cleanup_entered', 'cleanup_completed',
                'failure_count', 'error_count'}
    if (not isinstance(lifecycle, dict) or set(lifecycle) != {'schema', 'tests', 'events'}
            or lifecycle['schema'] != 'unittest.body-phase/v1'
            or not isinstance(expected, list) or not expected
            or any(type(value) is not str or not value for value in expected)
            or len(expected) != len(set(expected))): return False
    rows, events = lifecycle['tests'], lifecycle['events']
    if not isinstance(rows, list) or not isinstance(events, list) or len(rows) != len(expected): return False
    if any(not isinstance(row, dict) or set(row) != {'id', 'supported'} | counters for row in rows): return False
    if [row['id'] for row in rows] != expected: return False
    for row in rows:
        if row['supported'] is not True or any(type(row[key]) is not int or row[key] < 0 for key in counters): return False
        if any(row[key] != 1 for key in ('setup_entered', 'setup_completed', 'body_entered', 'body_exited',
                                         'teardown_entered', 'teardown_completed')): return False
        if row['cleanup_entered'] != row['cleanup_completed'] or row['error_count'] != 0: return False
        if row['failure_count'] != failure_ids.count(row['id']): return False
    if len(events) != len(failure_ids): return False
    for event, failure_id in zip(events, failure_ids):
        if (not isinstance(event, dict) or set(event) != {'id', 'phase', 'kind', 'exception', 'assertion'}
                or event['id'] != failure_id or failure_id not in expected
                or event['phase'] != 'body' or event['kind'] != 'failure'
                or type(event['exception']) is not str or not event['exception']
                or event['assertion'] is not True): return False
    return True


def check_run(result, count, selector=None, minimum_cli=1):
    require(isinstance(result.get("smoke"), dict) and result["smoke"].get("healthy") is True,
            "unhealthy CLI smoke; a crash is not a kill")
    health = result.get("cli_health")
    require(isinstance(health, list) and all(isinstance(v, dict) and v.get("healthy") is True for v in health),
            "unhealthy CLI invocation; a crash/invalid JSON is not a kill")
    selected=result.get("selected_ids")
    require(isinstance(selected,list) and len(selected)==count and len(set(selected))==count
            and all(type(value) is str and value.startswith("test_c8_quarantine.C8Quarantine.") for value in selected)
            and (selector is None or selected==[selector]), "selected test identity differs")
    require(all(v.get("phase")=="body" and v.get("test_id") in selected for v in health),
            "CLI health lacks selected-body provenance")
    require(len(health) >= minimum_cli, "CLI control did not execute")
    failures=result.get("failures")
    require(isinstance(failures,list) and all(isinstance(v,dict) and type(v.get("id")) is str for v in failures)
            and result.get("expected_failures")==[] and result.get("unexpected_successes")==[]
            and body_evidence(result.get("lifecycle"),selected,[v["id"] for v in failures]),
            "incomplete lifecycle or non-body assertion; fixtures do not kill mutants")
    require(type(result.get("tests_run")) is int and result["tests_run"] == count and count > 0
            and result.get("errors") == [] and result.get("skipped") == [], "test count/errors/skips do not qualify")
    if selector:
        require(result.get("returncode") == 1 and result.get("failures") == [{"id": selector, "kind": "AssertionError"}],
                "mutant lacks its one intended assertion failure")
    else:
        require(result.get("returncode") == 0 and result.get("failures") == [], "unmodified baseline is not healthy")


def materialize(work):
    work.mkdir(parents=True)
    shutil.copytree(ROOT / PACKET, work / PACKET)
    for relative in (TOOL, TEST, RECORD, Path("PROOF_INDEX.md")):
        target = work / relative;target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)


def run_suite(work, output, label, mode, selector=None):
    report_path = output / (label + "-" + mode + ".json")
    log_path = output / (label + "-" + mode + ".log")
    require(not report_path.exists() and not report_path.is_symlink()
            and not log_path.exists() and not log_path.is_symlink(), "observation output already exists")
    command = [sys.executable, "-B", "-S", *(["-O"] if mode == "optimized" else []),
               "-c", HELPER, str(work), str(report_path), selector or ""]
    env = {k: v for k, v in os.environ.items() if k not in {"PYTHONHOME", "PYTHONPATH", "PYTHONOPTIMIZE", "PYTHONSTARTUP", "PYTHONINSPECT"}}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        child = subprocess.run(command, cwd=work, env=env, capture_output=True, text=True, timeout=60)
        stdout, stderr, code = child.stdout, child.stderr, child.returncode
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        stdout, stderr, code = "", type(exc).__name__, 127
    log = output / (label + "-" + mode + ".log");log.write_text(stdout + stderr)
    result = json.loads(report_path.read_text()) if report_path.is_file() else {"smoke": {"healthy": False}, "startup_error": True}
    result.update(returncode=code, command=command, log=log.name, log_sha256=sha(log.read_bytes()))
    report_path.write_text(json.dumps(result, indent=2) + "\n")
    return result


def execute(output):
    require(not output.is_symlink(), "symlink mutation output")
    if output.exists() and any(output.iterdir()):
        previous = output.with_name(output.name + ".previous-" + uuid.uuid4().hex)
        output.replace(previous);output.mkdir(parents=True);(output / "history").mkdir()
        previous.replace(output / "history" / previous.name)
    else:output.mkdir(parents=True, exist_ok=True)
    result = {"schema": "cbz.c8-mutation-cut/v1", "status": "RUNNING", "expected_baseline_methods": EXPECTED_TESTS,
              "declared_mutants": len(CASES), "source_binding": {}, "baselines": {}, "mutants": [],
              "scope": "Declared C8 quarantine guards only; no arithmetic/theorem/global A3 admission."}
    def retain():(output / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    retain()
    try:
        require(CASES and len({v[0] for v in CASES}) == len(CASES), "empty or duplicate mutation inventory")
        inputs = [TOOL, TEST, RECORD, Path("PROOF_INDEX.md"), Path(__file__).absolute().relative_to(ROOT),
                  Path("tests/test_c8_quarantine_mutations.py"),
                  Path("tests/test_c8_quarantine_workflow.py"), Path("tools/c8_quarantine_registry.json"),
                  Path(".github/workflows/c8-elder-failure-coefficient.yml"), Path("docs/cbz/C8_QUARANTINE.md"),
                  *[p.relative_to(ROOT) for p in sorted((ROOT / PACKET).iterdir())]]
        binding = {p.as_posix(): sha((ROOT / p).read_bytes()) for p in inputs}
        result["source_binding"] = binding
        source = (ROOT / TOOL).read_text();mutants = {name: apply_mutation(source, before, after) for name, before, after, _, _ in CASES}
        sources = output / "sources";sources.mkdir()
        (sources / "original.py").write_text(source);shutil.copyfile(ROOT / TEST, sources / TEST.name)
        for relative in inputs:
            target = sources / relative;target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        for name, text in mutants.items():(sources / (name + ".py")).write_text(text)
        retain()
        with tempfile.TemporaryDirectory(prefix="c8-source-mutations-") as directory:
            work = Path(directory) / "repo";materialize(work)
            for mode in ("normal", "optimized"):
                row = run_suite(work, output, "baseline", mode);result["baselines"][mode] = row;retain()
                check_run(row, EXPECTED_TESTS)
            for name, before, after, method, minimum in CASES:
                selector = "test_c8_quarantine.C8Quarantine." + method
                row = {"id": name, "selector": selector, "mutation_locations": 1,
                       "mutated_source_sha256": sha(mutants[name].encode()), "runs": {}}
                result["mutants"].append(row);(work / TOOL).write_text(mutants[name]);retain()
                try:
                    for mode in ("normal", "optimized"):
                        trial = run_suite(work, output, name, mode, selector);row["runs"][mode] = trial;retain()
                        check_run(trial, 1, selector, minimum)
                    row["outcome"] = "KILLED_BY_INTENDED_ASSERTION_BOTH_MODES_WITH_HEALTHY_CLI"
                finally:(work / TOOL).write_text(source)
                retain()
        require(all(sha((ROOT / p).read_bytes()) == digest for p, digest in binding.items()), "source inputs changed during mutation cut")
        result.update(status="PASS", killed_mutants=len(CASES));retain();return result
    except (ValueError, OSError, KeyError, TypeError) as exc:
        result.update(status="REFUSED", reason=str(exc));retain();raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".lake/c8-quarantine/mutations")
    args = parser.parse_args(argv)
    try:result = execute(args.output.absolute())
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("C8 mutation gate REFUSED: " + str(exc), file=sys.stderr);return 1
    print(json.dumps({"status": result["status"], "declared_mutants": result["declared_mutants"],
                      "killed_mutants": result["killed_mutants"]}));return 0


if __name__ == "__main__":
    raise SystemExit(main())
