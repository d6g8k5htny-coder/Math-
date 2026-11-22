#!/usr/bin/env python3
"""Twenty bounded source checker mutations, same-copy controls, both Python modes.

No Lean execution; this is not federation G0 or compiled-adapter qualification.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
import unittest.mock

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

MUTATIONS.extend([
    ('runner-equal-code-is-not-identity', 'tests/run_source_admission_mutations.py',
     'any(frame.f_code is code for code in ' + 'unittest_codes)',
     'any(frame.f_code == code for code in unittest_codes)',
     ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_source_admission_mutations.py',
      '-k', 'equal_origin_self_mutant_has_single_outer_transcript', '-v']),
    ('runner-origin-code-check-removal', 'tests/run_source_admission_mutations.py',
     '                          bool(suffix) and all(' + 'any(frame.f_code is code for code in test._source_oracle_codes) or',
     '                          bool(suffix) and all(True or any(frame.f_code is code for code in test._source_oracle_codes) or',
     ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_source_admission_mutations.py',
      '-k', 'origin_bypass_self_mutant_is_detected_without_nested_transcript', '-v']),
    ('runner-origin-verdict-removal', 'tests/run_source_admission_mutations.py',
     "            and e['phase'] == 'body' and e['kind'] == 'failure' and " +
     "e['origin_authorized'] is True",
     "            and e['phase'] == 'body' and e['kind'] == 'failure' and True",
     ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_source_admission_mutations.py',
      '-k', 'origin_bypass_self_mutant_is_detected_without_nested_transcript', '-v']),
])


def replace_anchor(source, old, new):
    if source.count(old) != 1:
        raise ValueError('mutation anchor must occur exactly once')
    return source.replace(old, new)


RUNNER_EVIDENCE_ENV = 'CBZ_SOURCE_RUNNER_EVIDENCE'
RUNNER_NONCE_ENV = 'CBZ_SOURCE_RUNNER_NONCE'
RUNNER_SENTINEL = 'SOURCE_MUTATION_RUNNER_COMPLETE'
# The parent creates the evidence file and nonce. The runner writes them only
# after unittest returns. A child that reads the path or nonce can still write
# the sentinel; this is not a sandbox against that case.


def open_runner_channel():
    """Return (path, nonce) for a parent-owned evidence file."""
    nonce = secrets.token_hex(16)
    descriptor, path = tempfile.mkstemp(prefix='cbz-runner-evidence-')
    os.close(descriptor)
    os.chmod(path, 0o600)
    return path, nonce


def runner_child_env(path, nonce):
    env = os.environ.copy()
    env[RUNNER_EVIDENCE_ENV] = path
    env[RUNNER_NONCE_ENV] = nonce
    return env


def publish_runner_record(payload):
    """Write the completion record after unittest has returned.

    Stdout carries the same record for a parent that did not create a channel.
    The nonce file is written only when the parent passed one in.
    """
    encoded = json.dumps(payload)
    print(RUNNER_SENTINEL + '|' + encoded, file=sys.stdout, flush=True)
    path = os.environ.get(RUNNER_EVIDENCE_ENV)
    if path:
        Path(path).write_text(encoded + '\n')


def run_unittest(args):
    """Emit actual unittest lifecycle evidence for this bounded experiment.

    Unsupported/custom lifecycles lacking a recorded body entry fail closed.
    Fixture failures keep their original unittest transcript and exit status.
    The completion record is published only after unittest returns, so an
    import-time os._exit that replaces stderr is not runner evidence.
    """
    if args[:3] != ['-m', 'unittest', 'discover']:
        raise ValueError('unsupported scoped unittest invocation')
    def code_objects(container, module, seen=None):
        seen = set() if seen is None else seen
        if id(container) in seen:
            return []
        seen.add(id(container))
        result = []
        for value in vars(container).values():
            if isinstance(value, types.FunctionType):
                while isinstance(value, types.FunctionType):
                    result.append(value.__code__)
                    value = getattr(value, '__wrapped__', None)
            elif isinstance(value, type) and value.__module__ == module:
                result.extend(code_objects(value, module, seen))
        return result

    unittest_codes = (code_objects(unittest.case, unittest.case.__name__) +
                      code_objects(unittest.mock, unittest.mock.__name__))
    oracle_helpers = {'test_gate.SourceGate': ('assertGateFails',)}

    class PhaseResult(unittest.TextTestResult):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self.records, self.events = [], []
            self.authorized = {code.co_filename for code in unittest_codes}

        def startTest(self, test):
            test._source_supported = all(
                getattr(type(test), method) is getattr(unittest.TestCase, method)
                for method in ('run', '_callSetUp', '_callTestMethod', '_callTearDown', 'doCleanups'))
            test._source_phase = 'start'
            test._source_record = {'id': test.id(), 'body_entered': False}
            test.failureException = AssertionError
            helper_names = oracle_helpers.get(type(test).__module__ + '.' + type(test).__qualname__,
                                              getattr(type(test), 'CBZ_MUTATION_ORACLE_HELPERS', ()))
            if (type(helper_names) is not tuple or
                any(type(name) is not str or not name or not hasattr(type(test), name)
                    for name in helper_names)):
                raise TypeError('CBZ_MUTATION_ORACLE_HELPERS must be a tuple of exact method names')
            test._source_oracle_codes = [getattr(type(test), test._testMethodName).__code__]
            test._source_oracle_codes.extend(getattr(type(test), name).__code__ for name in helper_names)
            self.authorized.update(code.co_filename for code in test._source_oracle_codes)
            test._source_record['module'] = test._source_oracle_codes[0].co_filename
            self.records.append(test._source_record)
            super().startTest(test)

        def event(self, test, kind, err):
            frames = []
            traceback = err[2]
            while traceback is not None:
                frames.append(traceback.tb_frame)
                traceback = traceback.tb_next
            selected_code = getattr(type(test), test._testMethodName).__code__
            selected = next((index for index, frame in enumerate(frames)
                             if frame.f_code is selected_code), None)
            active = sys._getframe()
            selected_active = False
            while active is not None:
                selected_active = selected_active or active.f_code is selected_code
                active = active.f_back
            suffix = frames[selected:] if selected is not None else frames
            authorized = (issubclass(err[0], AssertionError) and (selected is not None or selected_active) and
                          bool(suffix) and all(any(frame.f_code is code for code in test._source_oracle_codes) or
                                               any(frame.f_code is code for code in unittest_codes) for frame in suffix))
            self.events.append({'id': test.id(), 'phase': getattr(test, '_source_phase', 'unknown'),
                                'kind': kind, 'origin_authorized': authorized,
                                'origin_frames': [
                                    {'file': frame.f_code.co_filename, 'function': frame.f_code.co_qualname,
                                     'line': frame.f_lineno} for frame in suffix]})

        def addFailure(self, test, err):
            self.event(test, 'failure', err)
            super().addFailure(test, err)

        def addError(self, test, err):
            self.event(test, 'error', err)
            super().addError(test, err)

        def addSubTest(self, test, subtest, err):
            if err is not None:
                self.event(test, 'failure' if issubclass(err[0], test.failureException) else 'error', err)
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
        phase = {'tests': result.records, 'events': result.events,
                 'authorized_files': sorted(result.authorized)}
        print('SOURCE_MUTATION_PHASES|' + json.dumps(phase), file=sys.stderr)
        status = 0 if result.wasSuccessful() else 1
        # Publish only after unittest returns. Import-time os._exit never reaches this.
        publish_runner_record({'sentinel': RUNNER_SENTINEL, 'nonce': os.environ.get(RUNNER_NONCE_ENV),
                               'status': status, **phase})
        return status
    finally:
        for method, original in originals.items():
            setattr(unittest.TestCase, method, original)


def frames_in_authorized_modules(event, allowed):
    frames = event['origin_frames']
    return all(isinstance(frame, dict) and set(frame) == {'file', 'function', 'line'}
               and isinstance(frame['file'], str) and frame['file'] in allowed
               and isinstance(frame['function'], str) and bool(frame['function'])
               and type(frame['line']) is int and frame['line'] > 0
               for frame in frames)


def phase_evidence(text, count, failures):
    lines = re.findall(r'^SOURCE_MUTATION_PHASES\|(.+)$', text, re.M)
    if len(lines) != 1:
        return False, False
    try:
        evidence = json.loads(lines[0])
        if not isinstance(evidence, dict) or set(evidence) != {'tests', 'events', 'authorized_files'}:
            return False, False
        tests, events, authorized_files = evidence['tests'], evidence['events'], evidence['authorized_files']
        if (not isinstance(authorized_files, list) or not authorized_files or
                any(type(name) is not str or not name for name in authorized_files) or
                len(set(authorized_files)) != len(authorized_files)):
            return False, False
        allowed = set(authorized_files)
        if not isinstance(tests, list) or not isinstance(events, list) or len(tests) != count:
            return False, False
        if not all(isinstance(t, dict) and set(t) == {'id', 'body_entered', 'module'} and
                   isinstance(t['id'], str) and bool(t['id']) and t['body_entered'] is True and
                   isinstance(t['module'], str) and t['module'] in allowed for t in tests):
            return False, False
        ids = [t['id'] for t in tests]
        if len(set(ids)) != count:
            return False, False
        fail_ids = re.findall(r'^FAIL: test_\S* \(([^)\n]+)\)', text, re.M)
        if len(fail_ids) != len(re.findall(r'^FAIL: test_', text, re.M)):
            return False, False
        event_ids = [e['id'] for e in events if isinstance(e, dict)]
        if len(event_ids) != len(events) or event_ids != fail_ids:
            return False, False
        body_failures = len(events) == failures and all(
            isinstance(e, dict) and set(e) == {
                'id', 'phase', 'kind', 'origin_authorized', 'origin_frames'} and e['id'] in ids
            and e['phase'] == 'body' and e['kind'] == 'failure' and e['origin_authorized'] is True
            and isinstance(e['origin_frames'], list) and bool(e['origin_frames']) and
            frames_in_authorized_modules(e, allowed) for e in events)
        return not events, body_failures
    except (ValueError, TypeError):
        return False, False


def runner_phase(result, runner_evidence, runner_nonce):
    """Return the phase object bound to a completed runner, or None.

    An explicit channel, including an empty one, is required when the parent
    created it. Stdout is only the fallback for a parent that did not.
    """
    channel_supplied = runner_evidence is not None or hasattr(result, 'runner_evidence')
    if runner_evidence is None and not channel_supplied:
        found = re.findall('^' + re.escape(RUNNER_SENTINEL) + r'\|(.+)$', result.stdout or '', re.M)
        if len(found) != 1:
            return None
        raw, nonce = found[0], None
    else:
        raw = runner_evidence if runner_evidence is not None else result.runner_evidence
        nonce = runner_nonce if runner_nonce is not None else getattr(result, 'runner_nonce', None)
    if not isinstance(raw, str) or not raw:
        return None
    try:
        record = json.loads(raw)
    except ValueError:
        return None
    if (not isinstance(record, dict) or record.get('sentinel') != RUNNER_SENTINEL or
            record.get('status') != result.returncode or
            (nonce is not None and record.get('nonce') != nonce)):
        return None
    phase = {key: record.get(key) for key in ('authorized_files', 'events', 'tests')}
    stderr_lines = re.findall(r'^SOURCE_MUTATION_PHASES\|(.+)$', result.stderr or '', re.M)
    if len(stderr_lines) != 1:
        return None
    try:
        stderr_phase = json.loads(stderr_lines[0])
    except ValueError:
        return None
    if stderr_phase != phase:
        return None
    return phase


def classify(result, expected_count=None, runner_evidence=None, runner_nonce=None):
    """Accept status 0 controls or status 1 assertion kills only with runner evidence.

    Stderr alone is not evidence. The record must be the parent's nonce file, or
    the stdout completion line when that parent did not create a channel, and it
    must match the stderr phase line. A child that reads the path or nonce can
    still forge the file; this is not a sandbox against that case.
    """
    valid_status = type(result.returncode) is int and result.returncode in (0, 1)
    text = result.stderr or ''
    matches = re.findall(r'^Ran ([0-9]+) tests? in ', text, re.M)
    count = int(matches[0]) if len(matches) == 1 else 0
    errors = any(marker in text for marker in
                 ('ERROR:', 'ImportError', 'ModuleNotFoundError', 'SyntaxError', 'skipped=',
                  'expected failures=', 'unexpected successes='))
    discovered = count > 0 and (expected_count is None or count == expected_count)
    failures = re.findall(r'^FAIL: test_', text, re.M)
    failed_summary = re.search(r'^FAILED \(failures=([1-9][0-9]*)\)\s*$', text, re.M)
    bound = runner_phase(result, runner_evidence, runner_nonce) is not None
    clean_phases, body_failures = phase_evidence(text, count, len(failures)) if bound else (False, False)
    control = (valid_status and bound and clean_phases and result.returncode == 0 and discovered and not errors and not failures
               and re.search(r'^OK\s*$', text, re.M) is not None and 'FAILED' not in text)
    killed = (valid_status and bound and body_failures and result.returncode != 0 and discovered and not errors and bool(failures)
              and failed_summary is not None
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
    channel, nonce = open_runner_channel()
    try:
        result = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=timeout,
                                env=runner_child_env(channel, nonce))
        try:
            evidence = Path(channel).read_text(encoding='utf-8')
        except OSError:
            evidence = ''
    finally:
        try:
            os.unlink(channel)
        except OSError:
            pass
    result.runner_evidence = evidence
    result.runner_nonce = nonce
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
