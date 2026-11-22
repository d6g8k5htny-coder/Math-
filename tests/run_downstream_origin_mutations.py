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
HELPER_SHA256 = '197b0b75014c00fde2010fa0521583b9a91a519097fe3cabebc83aa4aa9193cf'
CASES = (
    ('origin_bypass', "require(classification['killed'],", 'require(True,', 'test_real_child_origin_and_lifecycle_are_required'),
    ('actual_origin_bypass', "require(classification['killed'],", 'require(True,', 'test_actual_suite_rejects_subject_origin_assertion'),
    ('baseline_bypass', "require(classification['control_pass'],", 'require(True,', 'test_baseline_without_origin_evidence_is_rejected'),
    ('command_bypass', 'require(command == expected,', 'require(True,', 'test_real_child_exit_status_distinguishes_assertions_from_abnormal_termination'),
    ('helper_digest_bypass', 'require(hashlib.sha256(source).hexdigest() == ORIGIN_HELPER_SHA256,', 'require(True,', 'test_missing_or_changed_helper_is_refused'),
    ('process_record_omission', "(out/(name+'.process.json')).write_text(json.dumps(record, sort_keys=True, indent=2, allow_nan=False)+'\\n')", 'pass', 'test_completed_child_records_actual_status_and_stream_hashes'),
)
SELF_CASES = (
    ('self_verdict_bypass', "if not accepted:\n                            raise RuntimeError('self-mutation failed: ' + label)",
     "if False:\n                            raise RuntimeError('self-mutation failed: ' + label)", 'test_failed_classification_is_refused_and_reported'),
    ('self_inventory_bypass', "if len(CASES) != 6 or {case[0] for case in CASES} != expected_names:\n            raise ValueError('self-mutation case inventory mismatch')",
     "if False:\n            raise ValueError('self-mutation case inventory mismatch')", 'test_duplicate_cases_are_refused_before_children'),
    ('self_timeout_mask', "except Exception as failure:\n            error.add_note('timeout evidence write failed: ' + path.name + ': ' + str(failure))",
     'except Exception as failure:\n            raise', 'test_timeout_evidence_write_failures_do_not_mask_original'),
    ('self_report_mask', 'if active_error is None:\n                raise',
     'if True:\n                raise', 'test_timeout_evidence_write_failures_do_not_mask_original'),
)


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
