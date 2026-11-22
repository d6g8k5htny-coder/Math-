"""Bounded, provenance-qualified self-mutations for the downstream replay gate."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path('frontiers/downstream_gate_20260925')
HELPER = ROOT / 'tests' / 'run_source_admission_mutations.py'
HELPER_SHA256 = '639b48daed3254a1abd7c23e3b9893f287dcc5256bd4a5543f8611542b4c0544'
CASES = (
    ('origin_bypass', "require(classification['killed'],", 'require(True,', 'test_real_child_origin_and_lifecycle_are_required'),
    ('actual_origin_bypass', "require(classification['killed'],", 'require(True,', 'test_actual_suite_rejects_subject_origin_assertion'),
    ('baseline_bypass', "require(classification['control_pass'],", 'require(True,', 'test_baseline_without_origin_evidence_is_rejected'),
    ('command_bypass', 'require(command == expected,', 'require(True,', 'test_real_child_exit_status_distinguishes_assertions_from_abnormal_termination'),
    ('helper_digest_bypass', 'require(hashlib.sha256(source).hexdigest() == ORIGIN_HELPER_SHA256,', 'require(True,', 'test_missing_or_changed_helper_is_refused'),
    ('process_record_omission', "(out/(name+'.process.json')).write_text(json.dumps(record, sort_keys=True, indent=2, allow_nan=False)+'\\n')", 'pass', 'test_completed_child_records_actual_status_and_stream_hashes'),
)


def _disabled_check(old, indent, anchor_name):
    """Turn one guard into `if False` while retaining its exact anchor text once.

    The self-census requires that anchor. Keeping it here leaves the census able
    to see the anchor, and leaves only the targeted guard disabled.
    """
    if "'''" in old or '\n' not in old or indent.strip() or not anchor_name.isidentifier():
        raise ValueError('unstable self-mutation anchor: ' + anchor_name)
    live = 'if False:' + old[old.index('\n'):]
    if old in live:
        raise ValueError('disabled self-mutation still contains its anchor: ' + anchor_name)
    retained = indent + anchor_name + " = '''" + old + "'''"
    mutant = live + '\n' + retained
    if mutant.count(old) != 1:
        raise ValueError('self-mutation anchor was not retained once: ' + anchor_name)
    return mutant


_SELF_VERDICT = "if not accepted:\n                            raise RuntimeError('self-mutation failed: ' + label)"
_SELF_INVENTORY = ("if len(CASES) != 6 or {case[0] for case in CASES} != expected_names:\n"
                   "            raise ValueError('self-mutation case inventory mismatch')")
_SELF_TIMEOUT = ("except Exception as failure:\n"
                 "            error.add_note('timeout evidence write failed: ' + path.name + ': ' + str(failure))")
_SELF_REPORT = 'if active_error is None:\n                raise'
SELF_CASES = (
    ('self_verdict_bypass', _SELF_VERDICT,
     _disabled_check(_SELF_VERDICT, '                        ', '_self_verdict_anchor'),
     'test_failed_classification_is_refused_and_reported'),
    ('self_inventory_bypass', _SELF_INVENTORY,
     _disabled_check(_SELF_INVENTORY, '        ', '_self_inventory_anchor'),
     'test_duplicate_cases_are_refused_before_children'),
    ('self_timeout_mask', _SELF_TIMEOUT, 'except Exception as failure:\n            raise',
     'test_timeout_evidence_write_failures_do_not_mask_original'),
    ('self_report_mask', _SELF_REPORT, 'if True:\n                raise',
     'test_timeout_evidence_write_failures_do_not_mask_original'),
)
# Kills for the two self-mutants are accepted only when these test bodies fail
# with these assertion messages. A census ValueError or any other assertion does not qualify.
INTENDED_SELF_FAILURES = {
    'self_verdict_bypass': ('test_failed_classification_is_refused_and_reported',
                            'failed classification was accepted'),
    'self_inventory_bypass': ('test_duplicate_cases_are_refused_before_children',
                              'duplicate case inventory was accepted'),
}


def intended_self_failure(stderr, method, message):
    """True only for one authorized body failure of `method` with `message`."""
    marker = 'SOURCE_MUTATION_PHASES|'
    phase_lines = [line for line in stderr.splitlines() if line.startswith(marker)]
    if len(phase_lines) != 1 or not message:
        return False
    try:
        evidence = json.loads(phase_lines[0][len(marker):])
    except ValueError:
        return False
    if not isinstance(evidence, dict):
        return False
    tests, events = evidence.get('tests'), evidence.get('events')
    if (not isinstance(tests, list) or len(tests) != 1 or not isinstance(events, list)
            or len(events) != 1):
        return False
    test, event = tests[0], events[0]
    if not isinstance(test, dict) or not isinstance(event, dict):
        return False
    ident = event.get('id')
    if (type(ident) is not str or not ident.endswith('.' + method) or test.get('id') != ident
            or test.get('body_entered') is not True or event.get('phase') != 'body'
            or event.get('kind') != 'failure' or event.get('origin_authorized') is not True):
        return False
    lines = stderr.splitlines()
    if lines.count('AssertionError: ' + message) != 1:
        return False
    headers = [line for line in lines if line.startswith('FAIL: ')]
    return len(headers) == 1 and headers[0].startswith('FAIL: ' + method + ' (')


def verified_helper():
    if HELPER.is_symlink() or not HELPER.is_file():
        raise ValueError('source provenance helper missing')
    source = HELPER.read_bytes()
    if hashlib.sha256(source).hexdigest() != HELPER_SHA256:
        raise ValueError('source provenance helper identity mismatch')
    spec = importlib.util.spec_from_file_location('_downstream_self_origin', HELPER)
    if spec is None or spec.loader is None:
        raise ValueError('source provenance helper loader unavailable')
    module = importlib.util.module_from_spec(spec)
    exec(compile(source, str(HELPER), 'exec'), module.__dict__)
    return module


def preserve_timeout(output, label, error):
    for stream in ('stdout', 'stderr'):
        path = output / (label + '.' + stream)
        try:
            raw = getattr(error, stream)
            path.write_bytes(raw if raw is not None else b'')
        except Exception as failure:
            error.add_note('timeout evidence write failed: ' + path.name + ': ' + str(failure))


def run(output):
    output = output.resolve()
    if output.exists() or output.is_relative_to(ROOT):
        raise ValueError('new output outside source required')
    output.mkdir(parents=True)
    rows = []
    try:
        origin = verified_helper()
        expected_names = {'origin_bypass', 'actual_origin_bypass', 'baseline_bypass', 'command_bypass', 'helper_digest_bypass', 'process_record_omission'}
        if len(CASES) != 6 or {case[0] for case in CASES} != expected_names:
            raise ValueError('self-mutation case inventory mismatch')
        source = (ROOT / PACKET / 'run_validation.py').read_text()
        for name, old, new, test in CASES:
            if source.count(old) != 1:
                raise ValueError('mutation anchor must occur exactly once: ' + name)
            with tempfile.TemporaryDirectory() as d:
                temp = Path(d)
                (temp / 'tests').mkdir()
                shutil.copy2(ROOT / 'tests' / 'test_downstream_validation.py', temp / 'tests')
                shutil.copy2(HELPER, temp / 'tests')
                shutil.copytree(ROOT / PACKET, temp / PACKET, ignore=shutil.ignore_patterns('__pycache__'))
                target = temp / PACKET / 'run_validation.py'
                for mode, flags in (('normal', []), ('optimized', ['-O'])):
                    for variant, text in (('baseline', source), ('mutant', source.replace(old, new, 1))):
                        target.write_text(text)
                        cmd = [sys.executable, '-E', '-B', *flags, '-S', str(temp / 'tests/run_source_admission_mutations.py'),
                               '--_unittest', '-m', 'unittest', 'discover', '-s', 'tests', '-p',
                               'test_downstream_validation.py', '-k', test, '-v']
                        label = name + '_' + mode + '_' + variant
                        try:
                            result = subprocess.run(cmd, cwd=temp, capture_output=True, text=True, timeout=60)
                        except subprocess.TimeoutExpired as exc:
                            preserve_timeout(output, label, exc)
                            raise
                        (output / (label + '.stdout')).write_text(result.stdout)
                        (output / (label + '.stderr')).write_text(result.stderr)
                        classification = origin.classify(result, 1)
                        accepted = classification['control_pass' if variant == 'baseline' else 'killed']
                        rows.append({'name': name, 'mode': mode, 'variant': variant,
                                     'returncode': result.returncode, 'classification': classification, 'accepted': accepted})
                        if not accepted:
                            raise RuntimeError('self-mutation failed: ' + label)
        self_names = {'self_verdict_bypass', 'self_inventory_bypass', 'self_timeout_mask', 'self_report_mask'}
        if len(SELF_CASES) != 4 or {case[0] for case in SELF_CASES} != self_names:
            raise ValueError('self-runner case inventory mismatch')
        own_source = Path(__file__).read_text()
        for name, old, new, test in SELF_CASES:
            bound = INTENDED_SELF_FAILURES.get(name)
            if bound is not None and (bound[0] != test or type(bound[1]) is not str or not bound[1]):
                raise ValueError('intended self-failure binding mismatch')
            if own_source.count(old) != 1:
                raise ValueError('self-runner mutation anchor must occur exactly once: ' + name)
            with tempfile.TemporaryDirectory() as d:
                temp = Path(d)
                (temp / 'tests').mkdir()
                for name_to_copy in ('test_downstream_origin_mutations.py', 'test_downstream_validation.py'):
                    shutil.copy2(ROOT / 'tests' / name_to_copy, temp / 'tests')
                shutil.copy2(HELPER, temp / 'tests')
                shutil.copytree(ROOT / PACKET, temp / PACKET, ignore=shutil.ignore_patterns('__pycache__'))
                target = temp / 'tests/run_downstream_origin_mutations.py'
                for mode, flags in (('normal', []), ('optimized', ['-O'])):
                    for variant, text in (('baseline', own_source), ('mutant', own_source.replace(old, new, 1))):
                        target.write_text(text)
                        cmd = [sys.executable, '-E', '-B', *flags, '-S', str(temp / 'tests/run_source_admission_mutations.py'),
                               '--_unittest', '-m', 'unittest', 'discover', '-s', 'tests', '-p',
                               'test_downstream_origin_mutations.py', '-k', test, '-v']
                        label = name + '_' + mode + '_' + variant
                        try:
                            result = subprocess.run(cmd, cwd=temp, capture_output=True, text=True, timeout=60)
                        except subprocess.TimeoutExpired as exc:
                            preserve_timeout(output, label, exc)
                            raise
                        (output / (label + '.stdout')).write_text(result.stdout)
                        (output / (label + '.stderr')).write_text(result.stderr)
                        classification = origin.classify(result, 1)
                        accepted = classification['control_pass' if variant == 'baseline' else 'killed']
                        if variant == 'mutant' and name in INTENDED_SELF_FAILURES:
                            method, message = INTENDED_SELF_FAILURES[name]
                            accepted = bool(accepted and intended_self_failure(result.stderr, method, message))
                        rows.append({'name': name, 'mode': mode, 'variant': variant,
                                     'returncode': result.returncode, 'classification': classification, 'accepted': accepted})
                        if not accepted:
                            raise RuntimeError('self-runner mutation failed: ' + label)
        verified_helper()
        if len(rows) != 40:
            raise RuntimeError('self-mutation matrix incomplete')
    finally:
        active_error = sys.exc_info()[1]
        try:
            (output / 'results.json').write_text(json.dumps(rows, sort_keys=True, indent=2) + '\n')
        except Exception as failure:
            if active_error is None:
                raise
            active_error.add_note('self-mutation result write failed: ' + str(failure))
    print(json.dumps({'status': 'PASS', 'rows': len(rows), 'scientific_effect': 'NONE'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    run(args.output)


if __name__ == '__main__':
    main()
