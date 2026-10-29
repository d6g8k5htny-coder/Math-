#!/usr/bin/env python3
"""Determinant Git-identity mutations; real isolated Git, no Lean or gate receipt."""
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


CASES=(('omit-head-blob-attestation', [("_require(blob==entry[2],'source bytes differ from HEAD blob: '+relative)", "_require(True,'MUTATION: raw HEAD blob attestation omitted')")], 'test_self_consistently_rebound_dirty_source_and_manifest_refuse'), ('omit-source-index-head-match', [("_require(index.get(relative)==entry,'source index differs from HEAD: '+relative)", "_require(True,'MUTATION: source index/HEAD match omitted')")], 'test_staged_file_differs_from_head_even_when_live_bytes_restored'), ('omit-bound-sha-match', [("_require(digest==expected_sha256,'source bytes differ from bound SHA256: '+relative)", "_require(True,'MUTATION: bound source SHA omitted')")], 'test_wrong_manifest_digest_is_refused'), ('omit-caller-manifest-match', [("_require(canonical(manifest)==canonical(actual),'caller manifest differs from committed manifest bytes')", "_require(True,'MUTATION: caller manifest match omitted')")], 'test_different_caller_manifest_refuses_even_with_original_digest'), ('omit-previous-state-match', [('_require(type(previous) is dict and canonical(previous)==canonical(state),', '_require(True,')], 'test_new_native_head_requires_new_execution_identity'), ('omit-endpoint-head-stability', [("_require(final_head==head and final_tree==tree_id,'HEAD/tree changed during source qualification')", "_require(True,'MUTATION: endpoint HEAD/tree stability omitted')")], 'test_head_change_during_observation_is_refused'), ('omit-source-ancestor-symlink-refusal', [("_require(not any(p.is_symlink() for p in (path,*path.parents)),'symlink source or ancestor: '+relative)", "_require(True,'MUTATION: source ancestor symlink check omitted')")], 'test_shared_helper_directory_symlink_is_refused'), ('omit-live-source-mode-match', [("_require(('100755' if mode & stat.S_IXUSR else '100644')==entry[0],'source mode differs from HEAD: '+relative)", "_require(True,'MUTATION: live source mode match omitted')")], 'test_actual_executable_mode_drift_refuses_even_when_git_filemode_disabled'), ('omit-unregistered-source-refusal', [("_require(relative in files,'unregistered Lean/Python source: '+relative)", "_require(True,'MUTATION: unregistered source check omitted')")], 'test_unregistered_lean_and_python_sources_are_refused'), ('inherit-foreign-git-environment', [("environment={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}", 'environment=dict(os.environ)')], 'test_foreign_git_environment_does_not_redirect_identity'), ('allow-duplicate-manifest-json-keys', [('actual=json.loads(raw,object_pairs_hook=unique)', 'actual=json.loads(raw)')], 'test_duplicate_manifest_keys_are_refused'), ('omit-unmerged-index-refusal', [("_require(stage=='0','unmerged Git index refused')", "_require(True,'MUTATION: unmerged stage refused omitted')")], 'test_unmerged_single_stage_index_entry_is_refused'), ('omit-final-index-stability', [("_require(all(final_index.get(row['path'])==index[row['path']] for row in records),", '_require(True,')], 'test_index_change_during_observation_is_refused'))

CASES+=(
    ('restore-any-execute-bit-mode', [('mode & stat.S_IXUSR','mode & 0o111')],
     'test_non_owner_execute_bits_do_not_preserve_executable_component_source'),
    ('omit-head-source-inventory', [
        ("_require_bound_git_sources(tree,files,'HEAD')",'pass # MUTATION: HEAD source inventory omitted')],
     'test_hidden_head_only_unbound_lean_and_python_sources_are_refused'),
    ('omit-index-source-inventories', [
        ("_require_bound_git_sources(index,files,'index')",'pass # MUTATION: initial index source inventory omitted'),
        ("_require_bound_git_sources(final_index,files,'final index')",'pass # MUTATION: final index source inventory omitted')],
     'test_hidden_index_only_unbound_lean_and_python_sources_are_refused'),
    ('omit-final-index-source-inventory', [
        ("_require_bound_git_sources(final_index,files,'final index')",'pass # MUTATION: final index source inventory omitted')],
     'test_unbound_source_added_to_index_during_observation_is_refused'),
    ('omit-inventory-walk-error-handler', [
        ('followlinks=False,onerror=inventory_error','followlinks=False')],
     'test_explicit_directory_inventory_io_error_is_refused'),
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


def run_selected(source, selection, mode, evidence, harness):
    if mode not in ('normal', 'optimized'):
        raise ValueError('unknown Python mode')
    evidence = Path(evidence).absolute()
    evidence.mkdir(parents=True, exist_ok=False)
    summary = evidence/'unittest-result.json'
    command = [sys.executable, *(['-O'] if mode == 'optimized' else []), '-B', '-S',
               str(Path(harness).absolute()), selection, str(summary)]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
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
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'evidence/mutations',
        help='Retained evidence parent; each run creates a unique child. Native use: .lake/...')
    arguments=parser.parse_args(argv)
    original=(ROOT/'determinant_git_identity.py').read_text()
    destination=create_run_directory(arguments.output)
    harness=destination/'unittest_harness.py';harness.write_text(HARNESS_SOURCE)
    results=[]
    for name,replacements,test in CASES:
        changed=original
        for before,after in replacements:
            if changed.count(before)!=1:raise ValueError('mutation must identify one site: '+name)
            changed=changed.replace(before,after,1)
        compile(changed,name,'exec')
        selection='test_determinant_git_identity.DeterminantGitIdentityTests.'+test
        for mode in ('normal','optimized'):
            case=destination/name/mode;executions={}
            for label,text in (('baseline',original),('mutant',changed)):
                source=case/label/'source';source.mkdir(parents=True)
                (source/'determinant_git_identity.py').write_text(text)
                shutil.copytree(ROOT/'tests',source/'tests',ignore=shutil.ignore_patterns('__pycache__'))
                executions[label]=run_selected(source,selection,mode,case/label/'logs',harness)
            row=dict(scope='DETERMINANT_GIT_IDENTITY_MUTATIONS_ONLY',mutation=name,mode=mode,
                replacement_sites=len(replacements),test=selection,
                mutated_source_sha256=hashlib.sha256(changed.encode()).hexdigest(),
                external_process_responses='Actual isolated Git/filesystem; no Lean executed',
                **classify_pair(executions['baseline'],executions['mutant']),**executions)
            (case/'result.json').write_text(json.dumps(row,indent=2)+'\n');results.append(row)
    record=dict(scope='DETERMINANT_GIT_IDENTITY_MUTATIONS_ONLY',
        baseline_source_sha256=hashlib.sha256(original.encode()).hexdigest(),
        actual_mutants=len(CASES),execution_pairs=len(results),modes=['normal','optimized'],
        all_killed=len(results)==2*len(CASES) and all(row['killed'] for row in results),
        results=results,kernel_or_cbz_status='NOT_AWARDED')
    (destination/'results.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(results=str(destination/'results.json'),actual_mutants=len(CASES),
        execution_pairs=len(results),all_killed=record['all_killed']),indent=2))
    return 0 if record['all_killed'] else 1


if __name__=='__main__':sys.exit(main())
