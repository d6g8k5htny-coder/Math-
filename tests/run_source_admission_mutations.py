#!/usr/bin/env python3
"""Eighteen bounded source checker mutations, same-copy controls, both Python modes.

No Lean execution; this is not federation G0 or compiled-adapter qualification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DETP='frontiers/determinant_moment_20261025'
CAPP='frontiers/cap_first_exit_lean_20261002'
helper='tools/lean_packet_admission.py'
shared=['-m','unittest','discover','-s','tests','-p','test_lean_packet_admission.py','-v']
MUTATIONS=[
 ('helper-forbidden-token-removal',helper,"    require(not bad, 'forbidden token in source module ' + module + ': ' + repr(sorted(bad)))","    pass  # MUTANT: remove forbidden-token refusal",shared),
 ('helper-census-equality-removal',helper,"    require(actual == expected, 'source declaration census mismatch')","    pass  # MUTANT: remove exact census comparison",shared),
]
for prefix,packet in [('determinant',DETP),('cap',CAPP)]:
 gate=packet+'/gate.py'
 check=("    admission['check_census'](source_census, m['source_admission']['census'])" if prefix=='determinant' else "    admission['check_census'](source_census, m['source_admission']['census'])")
 testdir=packet+('/tests' if prefix=='determinant' else '')
 MUTATIONS.append((prefix+'-census-adapter-removal',gate,check,'    pass  # MUTANT: adapter skips census', ['-m','unittest','discover','-s',testdir,'-p','test_gate.py','-k','digest_rebound_omitted','-v']))
 MUTATIONS.append((prefix+'-helper-integrity-removal',gate,"    require(sha(data) == digest, 'admission helper hash mismatch')",'    pass  # MUTANT: execute unverified helper',shared))
 MUTATIONS.append((prefix+'-helper-symlink-removal',gate,"    require(all(not part.is_symlink() for part in (helper, *helper.parents)),\n            'symlink admission helper')",'    pass  # MUTANT: accept helper symlinks',shared))
MUTATIONS.append(('helper-continuation-admission-removal', helper,
                '    check_continuation(admitted_continuation, continuation)',
                '    pass  # MUTANT: arbitrary whitespace is admitted again', shared))
MUTATIONS.append(('helper-direct-placeholder-token-removal', helper,
                'sorry admit sorryAx axiom', 'sorry admit axiom', shared))
for prefix, packet in [('determinant', DETP), ('cap', CAPP)]:
    old = ("        source_census.extend(admission['census'](text, module, continuation_bindings[module], declaration_bindings[module]))"
           if prefix == 'determinant' else "    source_census = admission['census'](text, MODULE, continuation_bindings[MODULE], declaration_bindings[MODULE])")
    new = old.replace('continuation_bindings[module]' if prefix == 'determinant' else 'continuation_bindings[MODULE]',
                      "admission['continuation_binding'](text)")
    testdir = packet + ('/tests' if prefix == 'determinant' else '')
    MUTATIONS.append((prefix + '-continuation-input-autoapproval', packet + '/gate.py', old, new,
                    ['-m', 'unittest', 'discover', '-s', testdir, '-p', 'test_gate.py', '-k', 'rebound_unknown', '-v']))
MUTATIONS.append(('helper-variable-tail-boundary-removal', helper,
                "or re.fullmatch(r'variable(?:[ \\t]+(?:\\{[^{}\\n]*\\}|\\[[^\\[\\]\\n]*\\]|\\([^()\\n]*\\)))+[ \\t]*', line)",
                "or re.match(r'^variable[ \\t]+[\\{\\[(]', line)", shared))
MUTATIONS.append(('helper-open-command-wrapper-refusal-removal', helper,
                "        require(not (tokens and tokens[0] == 'open' and 'in' in tokens), 'unsupported command wrapper at ' + where)",
                '        pass  # MUTANT: permit open command wrappers', shared))

MUTATIONS.append(('helper-declaration-header-binding-removal', helper,
                '    check_declarations(admitted_declarations, declarations)',
                '    pass  # MUTANT: admit unreviewed declaration tails', shared))

MUTATIONS.append(('helper-declaration-physical-line-alignment-regression', helper,
                "    raw_lines, code_lines = text.split('\\n'), code.split('\\n')\n"
                "    require(len(raw_lines) == len(code_lines), 'unsupported physical-line correspondence')\n"
                "    lines = [raw + '\\n' for raw, line in zip(raw_lines, code_lines, strict=True) if DECL.match(line)]",
                "    lines = [raw + '\\n' for raw, line in zip(text.splitlines(), code.splitlines()) if DECL.match(line)]",
                ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_lean_packet_admission.py',
                 '-k', 'physical_header', '-v']))

runner_status = ('    valid_status = type(result.returncode) is int and '
                 'result.returncode in (0, 1)')
for name, replacement, selection in [
    ('runner-exact-exit-status-removal', '    valid_status = type(result.returncode) is int', 'exit_status'),
    ('runner-returncode-int-type-removal', '    valid_status = result.returncode in (0, 1)', 'returncode_type'),
]:
    MUTATIONS.append((name, 'tests/run_source_admission_mutations.py', runner_status, replacement,
                      ['-m', 'unittest', 'discover', '-s', 'tests',
                       '-p', 'test_source_admission_mutations.py', '-k', selection, '-v']))


def replace_anchor(source, old, new):
    if source.count(old) != 1:
        raise ValueError('mutation anchor must occur exactly once')
    return source.replace(old, new)


def run_unittest(args):
    """Emit actual unittest lifecycle evidence for this bounded experiment.

    Unsupported/custom lifecycles lacking a recorded body entry fail closed.
    Fixture failures keep their original unittest transcript and exit status.
    """
    if args[:3] != ['-m', 'unittest', 'discover']:
        raise ValueError('unsupported scoped unittest invocation')
    class PhaseResult(unittest.TextTestResult):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self.records, self.events = [], []

        def startTest(self, test):
            test._source_supported = all(
                getattr(type(test), method) is getattr(unittest.TestCase, method)
                for method in ('run', '_callSetUp', '_callTestMethod', '_callTearDown', 'doCleanups'))
            test._source_phase = 'start'
            test._source_record = {'id': test.id(), 'body_entered': False}
            self.records.append(test._source_record)
            super().startTest(test)

        def event(self, test, kind):
            self.events.append({'id': test.id(), 'phase': getattr(test, '_source_phase', 'unknown'),
                                'kind': kind})

        def addFailure(self, test, err):
            self.event(test, 'failure')
            super().addFailure(test, err)

        def addError(self, test, err):
            self.event(test, 'error')
            super().addError(test, err)

        def addSubTest(self, test, subtest, err):
            if err is not None:
                self.event(test, 'failure' if issubclass(err[0], test.failureException) else 'error')
            super().addSubTest(test, subtest, err)

    class PhaseRunner(unittest.TextTestRunner):
        resultclass = PhaseResult

    originals = {}
    try:
        for method, phase in [('_callSetUp', 'setup'), ('_callTestMethod', 'body'),
                              ('_callTearDown', 'teardown'), ('doCleanups', 'cleanup')]:
            original = getattr(unittest.TestCase, method)
            originals[method] = original
            def tracked(test, *a, _original=original, _phase=phase, **kw):
                test._source_phase = _phase
                if _phase == 'body' and getattr(test, '_source_supported', False):
                    test._source_record['body_entered'] = True
                return _original(test, *a, **kw)
            setattr(unittest.TestCase, method, tracked)
        program = unittest.TestProgram(module=None, argv=['phase-unittest', *args[2:]],
                                       testRunner=PhaseRunner, exit=False)
        result = program.result
        print('SOURCE_MUTATION_PHASES|' + json.dumps({'tests': result.records, 'events': result.events}),
              file=sys.stderr)
        return 0 if result.wasSuccessful() else 1
    finally:
        for method, original in originals.items():
            setattr(unittest.TestCase, method, original)


def phase_evidence(text, count, failures):
    lines = re.findall(r'^SOURCE_MUTATION_PHASES\|(.+)$', text, re.M)
    if len(lines) != 1:
        return False, False
    try:
        evidence = json.loads(lines[0])
        if not isinstance(evidence, dict) or set(evidence) != {'tests', 'events'}:
            return False, False
        tests, events = evidence['tests'], evidence['events']
        if not isinstance(tests, list) or not isinstance(events, list) or len(tests) != count:
            return False, False
        if not all(isinstance(t, dict) and set(t) == {'id', 'body_entered'} and
                   isinstance(t['id'], str) and bool(t['id']) and t['body_entered'] is True for t in tests):
            return False, False
        ids = [t['id'] for t in tests]
        if len(set(ids)) != count:
            return False, False
        body_failures = len(events) == failures and all(
            isinstance(e, dict) and set(e) == {'id', 'phase', 'kind'} and e['id'] in ids
            and e['phase'] == 'body' and e['kind'] == 'failure' for e in events)
        return not events, body_failures
    except (ValueError, TypeError):
        return False, False


def classify(result, expected_count=None):
    """Accept only exact integer status 0 controls or status 1 assertion kills."""
    valid_status = type(result.returncode) is int and result.returncode in (0, 1)
    text = result.stderr
    matches = re.findall(r'^Ran ([0-9]+) tests? in ', text, re.M)
    count = int(matches[0]) if len(matches) == 1 else 0
    errors = any(marker in text for marker in
                 ('ERROR:', 'ImportError', 'ModuleNotFoundError', 'SyntaxError', 'skipped=',
                  'expected failures=', 'unexpected successes='))
    discovered = count > 0 and (expected_count is None or count == expected_count)
    failures = re.findall(r'^FAIL: test_', text, re.M)
    failed_summary = re.search(r'^FAILED \(failures=([1-9][0-9]*)\)\s*$', text, re.M)
    clean_phases, body_failures = phase_evidence(text, count, len(failures))
    control = (valid_status and clean_phases and result.returncode == 0 and discovered and not errors and not failures
               and re.search(r'^OK\s*$', text, re.M) is not None and 'FAILED' not in text)
    killed = (valid_status and body_failures and result.returncode != 0 and discovered and not errors and bool(failures)
              and 'AssertionError:' in text and failed_summary is not None
              and int(failed_summary.group(1)) == len(failures))
    return dict(collected=count, control_pass=control, killed=killed)


def complete(records):
    expected = {(case[0], mode) for case in MUTATIONS for mode in (False, True)}
    expected |= {(name, mode) for name in ('control-helper', 'control-cap', 'control-determinant')
                 for mode in (False, True)}
    keys = [(record['name'], record['optimized']) for record in records]
    return len(keys) == len(set(keys)) and set(keys) == expected and all(record['passed'] for record in records)


def prepare_output(path):
    path = path.resolve()
    if path.exists():
        raise FileExistsError('output directory already exists: ' + str(path))
    if path.is_relative_to(ROOT):
        raise ValueError('--output must be outside the source repository')
    path.mkdir(parents=True, exist_ok=False)
    return path


def copy_sources(root):
    # Same packet/helper/shared-test/Cap-pin paths as the exercised round-1 harness.
    for packet in (DETP, CAPP):
        shutil.copytree(ROOT / packet, root / packet, ignore=shutil.ignore_patterns('.lake', '__pycache__'))
    (root / 'tools').mkdir()
    shutil.copy2(ROOT / helper, root / helper)
    (root / 'tests').mkdir()
    shutil.copy2(ROOT / 'tests/test_lean_packet_admission.py', root / 'tests/test_lean_packet_admission.py')
    for name in ('run_source_admission_mutations.py', 'test_source_admission_mutations.py'):
        shutil.copy2(ROOT / 'tests' / name, root / 'tests' / name)
    manifest = json.loads((ROOT / CAPP / 'MANIFEST.json').read_text())
    for pin in manifest['pins_on_main']:
        dst = root / pin['path']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / pin['path'], dst)


def run_process(root, args, output, label, optimized, timeout=180):
    argv = [sys.executable, '-B'] + (['-O'] if optimized else []) + ['-S', str(Path(__file__).resolve()), '--_unittest'] + args
    result = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=timeout)
    log = output / (label + '.log')
    log.write_text(result.stdout + result.stderr)
    return result, dict(argv=argv, exit_code=result.returncode, log=log.name,
                        sha256=hashlib.sha256(log.read_bytes()).hexdigest())


def run_case(case, optimized, output, control=False):
    name, path, old, new, args = case
    label = name + ('-optimized' if optimized else '-normal')
    with tempfile.TemporaryDirectory(prefix='cbz-source-mutant-') as temp:
        root = Path(temp)
        copy_sources(root)
        baseline, baseline_record = run_process(root, args, output, label + '-baseline', optimized)
        baseline_check = classify(baseline)
        baseline_record.update(baseline_check)
        if not baseline_check['control_pass']:
            raise RuntimeError(label + ': unmodified selected control did not pass with nonzero discovery')
        source_path = root / path
        source_path.write_text(replace_anchor(source_path.read_text(), old, new))
        if path == helper and not control:
            # Deliberate isolation: the intended helper removal, rather than its
            # independent SHA boundary, must be killed by the retained tests.
            digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
            for packet, manifest_name in ((DETP, 'manifest.json'), (CAPP, 'MANIFEST.json')):
                manifest_path = root / packet / manifest_name
                metadata = json.loads(manifest_path.read_text())
                metadata['source_admission']['helper_sha256'] = digest
                manifest_path.write_text(json.dumps(metadata))
        result, observation = run_process(root, args, output, label, optimized)
        classification = classify(result, baseline_check['collected'])
        record = dict(name=name, optimized=optimized, control=control, baseline=baseline_record,
                      **observation, **classification)
        record['passed'] = classification['control_pass'] if control else classification['killed']
        return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='fresh directory outside the repository')
    args = parser.parse_args()
    records = []
    try:
        output = prepare_output(args.output)
        controls = [('control-helper', helper, 'import hashlib', 'import hashlib', shared)]
        for prefix, packet in (('determinant', DETP), ('cap', CAPP)):
            testdir = packet + ('/tests' if prefix == 'determinant' else '')
            controls.append(('control-' + prefix, helper, 'import hashlib', 'import hashlib',
                             ['-m', 'unittest', 'discover', '-s', testdir, '-p', 'test_gate.py', '-v']))
        for case in controls + MUTATIONS:
            for optimized in (False, True):
                record = run_case(case, optimized, output, case in controls)
                records.append(record)
                (output / 'mutation-summary.json').write_text(json.dumps(records, indent=2) + '\n')
                print(record['name'], 'optimized' if optimized else 'normal',
                      'PASS' if record['passed'] else 'FAIL', flush=True)
        if not complete(records):
            raise RuntimeError('incomplete or failed mutation/control matrix')
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('SOURCE_MUTATION_GATE_FAIL: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(run_unittest(sys.argv[2:]) if sys.argv[1:2] == ['--_unittest'] else main())
