"""Finite source-bound C2 oracle qualification; no general arithmetic proof."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DEFAULT_ORACLE = HERE.parents[1] / 'reviews/c2_interval_audit_20261001/oracle.py'
ORACLE_SHA256 = 'b462b1b24613f74abd66042e0f347f69423595e9a1aedf1c6b45197425afe075'
TEST = HERE / 'test_qualification.py'
CASES = (
    'test_q_exact_rejections', 'test_q_fraction_inputs', 'test_cached_exact_inputs_reject_float_alias',
    'test_enclosure_outward', 'test_enclosure_reversed', 'test_corner_arithmetic',
    'test_division_zero_guard', 'test_power_exact_negative', 'test_atan_remainder',
    'test_log_remainder', 'test_log_domain', 'test_exp_remainder', 'test_exp_zero_reciprocal',
    'test_root_brackets', 'test_root_domain', 'test_gamma_zero_log_at_one', 'test_gamma_domain',
    'test_decimal_outward', 'test_coefficients_nine_contained', 'test_results_table_and_scope',
    'test_results_wrong_interval_rejected', 'test_results_missing_reference_rejected',
    'test_qualification_rejects_missing_computed_key', 'test_results_extra_computed_key_rejected',
    'test_qualification_rejects_falsified_reference',
)
MUTATIONS = (
    ('exact-type-guard', "    if type(x) not in (int,F):raise TypeError('exact int/Fraction required')",
     '    pass', 'test_q_exact_rejections'),
    ('upper-rounding', 'F(ceil(b*SCALE),SCALE)', 'F(floor(b*SCALE),SCALE)', 'test_enclosure_outward'),
    ('zero-division-guard', "if b[0]<=0<=b[1]:raise ValueError('division by interval containing zero')",
     'if b[0]<=0<=b[1]:return (F(-999),F(999))', 'test_division_zero_guard'),
    ('atan-remainder', 'tail=x**(2*terms+1)/(2*terms+1)', 'tail=F(0)', 'test_atan_remainder'),
    ('log-remainder', 'rem=2*u**(2*terms+1)/((2*terms+1)*(1-u*u))', 'rem=F(0)', 'test_log_remainder'),
    ('exp-remainder', 'tail=t**(K+1)/factorial(K+1)/(1-t/F(K+2))', 'tail=F(0)', 'test_exp_remainder'),
    ('root-upper-endpoint', 'return lo,lo if lo**n==t else F(k+1,SCALE)',
     'return lo,lo', 'test_root_brackets'),
    ('gamma-remainder', 'rem=abs(bernoulli(2*K+2))/((2*K+2)*(2*K+1)*y**(2*K+1))',
     'rem=F(0)', 'test_gamma_zero_log_at_one'),
    ('decimal-upper-rounding', 'vals=[floor(iv[0]*den),ceil(iv[1]*den)]',
     'vals=[floor(iv[0]*den),floor(iv[1]*den)]', 'test_decimal_outward'),
    ('results-containment', "        if not ref[0]<a[0]<=a[1]<ref[1]:raise ArithmeticError('published containment failed: '+key)",
     '        pass', 'test_results_wrong_interval_rejected'),
    ('missing-reference-silent-skip', '    for key,a in coefficients().items():',
     '    for key,a in coefficients().items():\n        if key not in PUBLISHED:continue',
     'test_results_missing_reference_rejected'),
    ('computed-key-omission', "        out[f'{d}.c']=c;out[f'{d}.c2']=c2;out[f'{d}.ratio']=over(c2,c)",
     "        out[f'{d}.c']=c;out[f'{d}.c2']=c2", 'test_results_table_and_scope'),
)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pinned_source(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('oracle source pin mismatch')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORACLE_SHA256: raise ValueError('oracle source pin mismatch')
    return raw.decode('utf-8')


def substitute(source, before, after):
    if not before or before == after or source.count(before) != 1:
        raise ValueError('mutation anchor must occur exactly once and change source')
    return source.replace(before, after)


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


def classify(report, exit_code, cases, source_hash, intended=None):
    expected = ['__main__.OracleQualification.' + case for case in cases]
    if not isinstance(report, dict) or report.get('schema') != 'c2.oracle.qualification-observation.v1':
        return 'INVALID'
    if (report.get('test_ids') != expected or type(report.get('tests_run')) is not int
            or report['tests_run'] != len(cases) or not cases
            or report.get('oracle_sha256') != source_hash):
        return 'INVALID'
    for key in ('failures', 'errors', 'skipped', 'unexpected_successes'):
        if not isinstance(report.get(key), list) or any(type(x) is not str for x in report[key]):
            return 'INVALID'
    if report['errors'] or report['skipped'] or report['unexpected_successes']:
        return 'INVALID'
    if report.get('expected_failures') != [] or not body_evidence(report.get('lifecycle'), expected, report['failures']):
        return 'INVALID'
    if exit_code == 0 and report.get('was_successful') is True and not report['failures']:
        return 'PASS' if intended is None else 'SURVIVED'
    named = '__main__.OracleQualification.' + str(intended)
    if (intended is not None and exit_code == 1 and report.get('was_successful') is False
            and report['failures'] and all(test == named for test in report['failures'])
            and named in expected):
        return 'KILLED'
    return 'INVALID'


def probe(source, output, cases=None, intended=None):
    """Run explicitly selected tests; this alone does not qualify an arbitrary source."""
    source, output = Path(source).absolute(), Path(output).absolute()
    if source.is_symlink() or not source.is_file(): raise ValueError('regular probe source required')
    output.mkdir(parents=True, exist_ok=False)
    source_hash = digest(source)
    command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    command += ['-S', str(TEST), '--report-json', str(output / 'observation.json')]
    expected_cases = sorted(CASES) if cases is None else list(cases)
    if cases is not None:
        for case in cases: command += ['--case', case]
    environment = {'PATH': os.defpath, 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
                   'PYTHONHASHSEED': '0', 'C2_ORACLE_UNDER_TEST': str(source)}
    timed_out = False
    try:
        process = subprocess.run(command, cwd=output, env=environment, capture_output=True, timeout=60)
        code, stdout, stderr = process.returncode, process.stdout, process.stderr
    except subprocess.TimeoutExpired as error:
        code, stdout, stderr, timed_out = None, error.stdout or b'', error.stderr or b'', True
    (output / 'stdout.log').write_bytes(stdout); (output / 'stderr.log').write_bytes(stderr)
    try:
        path = output / 'observation.json'
        if path.is_symlink() or path.stat().st_size > 1024*1024: raise ValueError('invalid observation')
        report = json.loads(path.read_text())
    except (ValueError, OSError, UnicodeError): report = None
    classification = classify(report, code, expected_cases, source_hash, intended)
    if timed_out or digest(source) != source_hash: classification = 'INVALID'
    record = {'classification': classification, 'exit_code': code, 'timed_out': timed_out,
        'source_sha256': source_hash, 'command': command, 'intended_assertion': intended,
        'observation': report, 'stdout_sha256': hashlib.sha256(stdout).hexdigest(),
        'stderr_sha256': hashlib.sha256(stderr).hexdigest()}
    (output / 'process.json').write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
    return record


def campaign(oracle, output, mutations=MUTATIONS):
    source = pinned_source(oracle)
    names = [item[0] for item in mutations]
    if not names or len(names) != len(set(names)): raise ValueError('unique nonempty mutation inventory required')
    prepared = []
    for name, before, after, case in mutations:
        if case not in CASES: raise ValueError('unknown intended mutation test')
        prepared.append((name, substitute(source, before, after), case))
    output = Path(output).absolute(); output.mkdir(parents=True, exist_ok=False)
    baseline = probe(oracle, output / 'baseline')
    if baseline['source_sha256'] != ORACLE_SHA256 or digest(oracle) != ORACLE_SHA256:
        baseline = {**baseline, 'classification': 'INVALID', 'source_pin_matches': False}
    records = []
    if baseline['classification'] == 'PASS':
        for name, text, case in prepared:
            directory = output / name; directory.mkdir()
            mutant = directory / 'oracle.py'; mutant.write_text(text)
            record = probe(mutant, directory / 'execution', [case], case)
            records.append({'name': name, **record})
    original_unchanged = digest(oracle) == ORACLE_SHA256
    qualified = original_unchanged and baseline['classification'] == 'PASS' and len(records) == len(prepared) and all(
        record['classification'] == 'KILLED' for record in records)
    result = {'schema': 'c2.oracle.finite-mutation-cut.v1',
        'qualified_in_declared_scope': qualified, 'baseline': baseline, 'mutations': records,
        'declared_mutants': len(prepared), 'killed': sum(r['classification'] == 'KILLED' for r in records),
        'oracle_sha256': ORACLE_SHA256, 'original_source_unchanged': original_unchanged,
        'tests_sha256': digest(TEST), 'runner_sha256': digest(__file__),
        'python': sys.version, 'optimize': sys.flags.optimize, 'scientific_effect': 'NONE',
        'source_analytic_derivation_revalidated': False, 'kernel_verified': False,
        'semantic_completeness': False, 'federation_certificate': False,
        'scope': 'Pinned nine supplied closed forms and explicit finite source mutations only'}
    (output / 'REPORT.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--oracle', type=Path, default=DEFAULT_ORACLE)
    parser.add_argument('--evidence-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = campaign(args.oracle, args.evidence_dir)
    except (OSError, ValueError, UnicodeError) as error:
        print(json.dumps({'qualified_in_declared_scope': False, 'error': str(error)}), file=sys.stderr)
        return 2
    print(json.dumps({key: result[key] for key in ('qualified_in_declared_scope', 'declared_mutants', 'killed',
        'oracle_sha256', 'semantic_completeness', 'kernel_verified', 'federation_certificate')}, sort_keys=True))
    return 0 if result['qualified_in_declared_scope'] else 1


if __name__ == '__main__': raise SystemExit(main())
