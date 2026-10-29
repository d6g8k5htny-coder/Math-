#!/usr/bin/env python3
"""Assertion-only adapter mutations with the same positive test harness in both modes.

Python subprocess/file logic is real. External Lean/build/checker responses in selected
admission-harness tests are synthetic and cannot qualify a repaired gate.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
CORE=Path(os.environ.get('DETERMINANT_CORE_PATH',str(ROOT/'compiled_inventory.py' if (ROOT/'compiled_inventory.py').exists() else ROOT.parent/'cbz_hosted_determinant_census/native_successor/frontiers/determinant_moment_20261025/compiled_inventory.py'))).resolve()
POLICY='test_determinant_inventory.py'
HARNESS='test_determinant_admission_harness.py'
HARNESS_SOURCE = '''"""One exact unittest selection; no Lean process is executed."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path.cwd()/'tests'))
selection, report = sys.argv[1:]
suite = unittest.defaultTestLoader.loadTestsFromName(selection)
def test_cases(node):
    if isinstance(node, unittest.TestSuite):
        return [case for child in node for case in test_cases(child)]
    return [node]
cases = test_cases(suite)
loaded = [case.id() for case in cases]
for case in cases:
    case._adapter_mutation_phase = 'setup'
    for method, phase in (('_callSetUp', 'setup'), ('_callTestMethod', 'test'),
                          ('_callTearDown', 'teardown'), ('doCleanups', 'cleanup')):
        original = getattr(case, method)
        def wrapped(*args, _case=case, _original=original, _phase=phase, **kwargs):
            _case._adapter_mutation_phase = _phase
            return _original(*args, **kwargs)
        setattr(case, method, wrapped)
failure_details = []
class RecordingResult(unittest.TextTestResult):
    def record_failure(self, test, error, parent):
        failure_details.append(dict(test_id=test.id(), parent_test_id=parent.id(),
            phase=getattr(parent, '_adapter_mutation_phase', 'outside_test'),
            exception_type=error[0].__name__, is_assertion=issubclass(error[0], AssertionError)))
    def addFailure(self, test, error):
        self.record_failure(test, error, test)
        super().addFailure(test, error)
    def addSubTest(self, test, subtest, error):
        if error is not None and issubclass(error[0], test.failureException):
            self.record_failure(subtest, error, test)
        super().addSubTest(test, subtest, error)
result = unittest.TextTestRunner(verbosity=2, resultclass=RecordingResult).run(suite)
record = dict(selection=selection, loaded_test_ids=loaded, tests_run=result.testsRun,
    failure_ids=[test.id() for test, detail in result.failures],
    error_ids=[test.id() for test, detail in result.errors],
    skipped_ids=[test.id() for test, detail in result.skipped],
    expected_failure_ids=[test.id() for test, detail in result.expectedFailures],
    unexpected_success_ids=[test.id() for test in result.unexpectedSuccesses],
    failure_details=failure_details, optimization=sys.flags.optimize, successful=result.wasSuccessful())
Path(report).write_text(json.dumps(record, indent=2)+'\\n')
sys.exit(0 if result.wasSuccessful() else 1)
'''
CASES=(
 ('omit-internal-proof-presence',[("for record in contract['internal']:\n        if observed[record] != 1:","for record in contract['internal']:\n        if False:")],POLICY,'test_missing_proof_valued_instance_rejects'),
 ('blanket-user-proof-exception',[("known_internal = (code == 'extra_theorem' and note == '' and len(by_name[name]) == 1\n                          and by_name[name][0] in contract['internal'])","known_internal = (code == 'extra_theorem')")],POLICY,'test_new_axiom_free_private_proof_is_not_blanket_allowed'),
 ('blanket-IR-metadata-exception',[("known_IR_count = (code == 'codegen_extra' and name in contract['extras']\n                          and len(table[name]) == 1 and table[name][0][2] == contract['extras'][name]\n                          and note == str(contract['extras'][name]))","known_IR_count = (code == 'codegen_extra')"),("if actual != expected:","if False:")],POLICY,'test_changed_IR_extra_count_rejects_and_is_not_an_allowlist'),
 ('omit-core-findings',[("base = core.inventory_violations(inventory, contract['targets'], modules,\n        reported_axioms=reported_axioms, bound=contract['bound'])","base = []")],POLICY,'test_forbidden_axiom_behind_non_target_cannot_be_filtered'),
 ('blanket-auxiliary-exception',[("known_compat_aux = (code == 'unbound_auxiliary' and note == '' and compatibility is not None\n                           and by_name[name] == [compatibility[0]]\n                           and by_name[compatibility[1][3]] == [compatibility[1]])","known_compat_aux = (code == 'unbound_auxiliary')")],POLICY,'test_even_bound_unknown_auxiliary_cannot_bypass_parent_rule'),
 ('omit-positive-baseline-digest',[("require(clean['sha256'] == digest,","require(True,")],HARNESS,'test_changed_positive_baseline_digest_refuses_before_injection'),
 ('skip-required-checker-stage',[("run(['lake','env','leanchecker',PACKAGE],label+'_leanchecker',output,cwd=clone)","pass  # MUTATION: required checker omitted")],HARNESS,'test_prerequisite_failure_is_not_counted_as_an_admission_rejection'),
 ('ignore-exact-rejection-reason',[("require(sorted(got) == sorted(wanted),","require(True,")],HARNESS,'test_unrelated_IR_drift_fails_exact_reason_check'),
 ('coerce-numeric-name-components-to-strings',[("return tuple(result)","return tuple(str(x) for x in result)")],POLICY,'test_actual_census_accepts_all157_constants_without_changing_core'),
 ('execute-stale-core-bytecode',[("exec(compile(source, str(path), 'exec'), core.__dict__)","import importlib.util\n    spec = importlib.util.spec_from_file_location('pinned_determinant_inventory_core', path)\n    core = importlib.util.module_from_spec(spec)\n    spec.loader.exec_module(core)")],POLICY,'test_stale_timestamp_pyc_cannot_replace_verified_core_bytes'),
 ('omit-output-symlink-refusal',[("require(not any(p.is_symlink() for p in (output, *output.parents)),\n            'symlink admission output or ancestor refused')","require(True, 'MUTATION: output symlink refusal omitted')")],HARNESS,'test_output_symlink_outside_work_is_also_refused'),
 ('replace-canonical-containment-with-lexical',[("require(not output.resolve().is_relative_to(work.resolve()),","require(not output.is_relative_to(work),")],HARNESS,'test_resolved_dotdot_output_containment_refuses_before_cleanup'),
)


def classify_execution(record):
    """Only a named assertion FAILURE is adverse evidence; ERROR is always invalid."""
    selection = record.get('selection')
    list_fields = ('loaded_test_ids', 'failure_ids', 'error_ids', 'skipped_ids',
                   'expected_failure_ids', 'unexpected_success_ids')
    details = record.get('failure_details')
    if (type(record.get('returncode')) is not int or type(selection) is not str or not selection or
        any(type(record.get(key)) is not list or any(type(value) is not str for value in record[key])
            for key in list_fields) or
        record['loaded_test_ids'] != [selection] or type(record.get('tests_run')) is not int or
        record['tests_run'] != 1 or record['error_ids'] or record['skipped_ids'] or
        record['expected_failure_ids'] or record['unexpected_success_ids'] or record.get('protocol_error') or
        type(details) is not list or len(details) != len(record['failure_ids'])):
        return 'INVALID'
    if record.get('returncode') == 0 and record.get('successful') is True and not record['failure_ids']:
        return 'PASS'
    if (record.get('returncode') == 1 and record.get('successful') is False and record['failure_ids'] and
        all(type(detail) is dict and detail.get('test_id') == name and
            detail.get('parent_test_id') == selection and detail.get('phase') == 'test' and
            detail.get('is_assertion') is True and type(detail.get('exception_type')) is str and
            bool(detail['exception_type']) and (name == selection or name.startswith(selection+' '))
            for name, detail in zip(record['failure_ids'], details))):
        return 'ASSERTION_FAILURE'
    return 'INVALID'


def classify_pair(baseline, mutant):
    same_harness = all(type(baseline.get(key)) is str and bool(baseline[key]) and
                       baseline[key] == mutant.get(key) for key in ('selection','mode','harness_sha256'))
    baseline_passed = baseline.get('classification') == 'PASS'
    killed = same_harness and baseline_passed and mutant.get('classification') == 'ASSERTION_FAILURE'
    status = ('KILLED' if killed else 'HARNESS_MISMATCH' if not same_harness else
              'INVALID_BASELINE' if not baseline_passed else
              'SURVIVED' if mutant.get('classification') == 'PASS' else 'INVALID_MUTANT')
    return dict(same_harness=same_harness, baseline_passed=baseline_passed, killed=killed, status=status)


def create_run_directory(parent):
    parent = Path(parent).absolute()
    parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    return Path(tempfile.mkdtemp(prefix='run-'+stamp+'-', dir=parent))


def run_selected(source, selection, mode, evidence, harness, core):
    if mode not in ('normal', 'optimized'):
        raise ValueError('unknown Python mode')
    evidence = Path(evidence).absolute()
    evidence.mkdir(parents=True, exist_ok=False)
    summary = evidence/'unittest-result.json'
    command = [sys.executable, *(['-O'] if mode == 'optimized' else []), '-B', '-S',
               str(Path(harness).absolute()), selection, str(summary)]
    environment = dict(os.environ, DETERMINANT_CORE_PATH=str(Path(core).absolute()), PYTHONDONTWRITEBYTECODE='1')
    environment.pop('PYTHONOPTIMIZE', None)
    record = {}
    try:
        process = subprocess.run(command, cwd=source, env=environment, capture_output=True, timeout=60)
        stdout, stderr, returncode = process.stdout, process.stderr, process.returncode
        try:
            record = json.loads(summary.read_text())
            if type(record) is not dict or record.get('selection') != selection or record.get('optimization') != (1 if mode == 'optimized' else 0):
                record = dict(protocol_error='unittest report selection/mode mismatch')
        except (OSError, ValueError) as error:
            record = dict(protocol_error=str(error))
    except subprocess.TimeoutExpired as error:
        stdout, stderr, returncode = error.stdout or b'', error.stderr or b'', None
        record = dict(protocol_error='unittest subprocess timed out')
    except OSError as error:
        stdout, stderr, returncode = b'', str(error).encode(), None
        record = dict(protocol_error='unittest subprocess could not start')
    (evidence/'stdout.log').write_bytes(stdout)
    (evidence/'stderr.log').write_bytes(stderr)
    record.update(selection=selection, mode=mode, command=command, returncode=returncode,
                  harness_sha256=hashlib.sha256(Path(harness).read_bytes()).hexdigest())
    record['classification'] = classify_execution(record)
    (evidence/'result.json').write_text(json.dumps(record, indent=2)+'\n')
    return record


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'evidence/mutations',
                        help='Evidence parent; a new unique child preserves all prior logs. Native use: .lake/...')
    arguments = parser.parse_args(argv)
    original = (ROOT/'determinant_inventory.py').read_text()
    destination = create_run_directory(arguments.output)
    harness = destination/'unittest_harness.py'
    harness.write_text(HARNESS_SOURCE)
    results = []
    for name, replacements, module, test in CASES:
        changed = original
        for before, after in replacements:
            if changed.count(before) != 1:
                raise ValueError('mutation must identify one source site: '+name)
            changed = changed.replace(before, after, 1)
        compile(changed, name, 'exec')
        class_name = 'DeterminantPolicyTests' if module == POLICY else 'AdmissionHarnessTests'
        selection = module[:-3]+'.'+class_name+'.'+test
        for mode in ('normal', 'optimized'):
            case = destination/name/mode
            executions = {}
            for label, text in (('baseline', original), ('mutant', changed)):
                source = case/label/'source'
                source.mkdir(parents=True)
                (source/'determinant_inventory.py').write_text(text)
                shutil.copytree(ROOT/'tests', source/'tests', ignore=shutil.ignore_patterns('__pycache__'))
                executions[label] = run_selected(source, selection, mode, case/label/'logs', harness, CORE)
            row = dict(scope='DETERMINANT_ADAPTER_MUTATION_UNIT_TESTS_ONLY', mutation=name, mode=mode,
                       replacement_sites=len(replacements), test=selection,
                       mutated_source_sha256=hashlib.sha256(changed.encode()).hexdigest(),
                       external_process_responses='Synthetic for harness cases; no Lean execution',
                       **classify_pair(executions['baseline'], executions['mutant']), **executions)
            (case/'result.json').write_text(json.dumps(row, indent=2)+'\n')
            results.append(row)
    record = dict(scope='DETERMINANT_ADAPTER_MUTATION_UNIT_TESTS_ONLY',
                  baseline_source_sha256=hashlib.sha256(original.encode()).hexdigest(),
                  actual_mutants=len(CASES), execution_pairs=len(results), modes=['normal','optimized'],
                  all_killed=len(results) == 2*len(CASES) and all(row['killed'] for row in results),
                  results=results, kernel_or_cbz_status='NOT_AWARDED')
    (destination/'results.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(results=str(destination/'results.json'), actual_mutants=len(CASES),
                         execution_pairs=len(results), all_killed=record['all_killed']), indent=2))
    return 0 if record['all_killed'] else 1


if __name__=='__main__':sys.exit(main())
