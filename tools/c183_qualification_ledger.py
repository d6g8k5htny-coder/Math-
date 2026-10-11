"""Offline supplied-byte C183 Q1/Q6 evidence ledger; never an experiment runner."""
import argparse
import ast
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

SOURCE_COMMIT = '81c31f5d61c509256f8d13a4635ca0c85fb8d989'
PR_HEAD = '8177f47bbb66b7cc0dca430941832740a5480dee'
BASE_COMMIT = '2ca3bf262f34a729589ad87eefe6cf6af5adcb6c'
WRAPPER_BLOB = 'fcf6480529d6b521628e2635e7c1e271ecfa39a4'
MANIFEST_SHA = '4a3e0808f0426e926b361a40afcb610b52201a559fcba56e918b8b3603afe6ec'
ARCHIVE_SHA = 'ce224c87fffea10a41b0d3403eee59b81b4b05f06e809ce6623863dd311da65c'
ARCHIVE_BYTES = 507793
MAX_MEMBER = 1024 * 1024
MAX_TOTAL = 16 * 1024 * 1024
EMPTY_SHA = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
MEMBERS = {
    'tests_normal.stderr': (9022, '4d3902bfbee7114ea8d76bf5b7153a9688ee2ef199aded677526b574751df6b9'),
    'tests_normal.stdout': (0, EMPTY_SHA),
    'mutation_normal_accept_numeric_required.stderr': (11843, '04dfaed26d621ca0e651e3a1a27cf92865bb336972048421fbc6ad3610e231e9'),
    'mutation_normal_accept_numeric_required.stdout': (0, EMPTY_SHA),
    'REPORT.json': (325, 'b60b7149a69c6a1223a18937b976e9ef179b1c8039b92794550e717d7f21d119'),
}
METHOD = r'test_[A-Za-z0-9_]+ \([A-Za-z0-9_.]+\)'
ROW = re.compile(r'^(' + METHOD + r') \.\.\. (.+)$')
SUMMARY_HEADER = re.compile(r'^Ran [0-9]+ tests? in [0-9]+\.[0-9]+s$', re.MULTILINE)
SUMMARY = re.compile(r'\nRan ([0-9]+) tests? in ([0-9]+\.[0-9]+)s\n\n'
                     r'(OK|FAILED \((?:failures=[0-9]+(?:, errors=[0-9]+)?|errors=[0-9]+)\))\n\Z')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(raw):
    require(type(raw) is bytes, 'bytes required')
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    def reject(value):
        raise ValueError('nonfinite JSON: ' + value)
    def finite_float(value):
        number = float(value)
        require(math.isfinite(number), 'nonfinite JSON numeric value')
        return number
    require(type(raw) in (bytes, str), 'JSON text required')
    result = json.loads(raw, object_pairs_hook=pairs, parse_constant=reject, parse_float=finite_float)
    require(type(result) is dict, 'JSON object required')
    return result


def planned_cases():
    """Predeclared population only; no argument can mark a case executed."""
    result = []
    def add(group, cell, mode, variant, full_suite):
        result.append({'id': '/'.join((group, cell, mode, variant)), 'group': group,
                       'cell': cell, 'mode': mode, 'variant': variant,
                       'full_suite': full_suite, 'execution': 'NOT_RUN', 'outcomes': None})
    for cell in 'UIMDHTQ':
        for mode in ('normal', 'optimized'):
            for variant in ('baseline', 'accept_numeric_required'):
                add('matrix', cell, mode, variant, True)
    for mode in ('normal', 'optimized'):
        for shape in ('empty', 'populated'):
            add('control', 'pure_cleanup', mode, shape, False)
        add('control', 'late_entry', mode, 'known_writer', False)
        add('control', 'wrapper_refusal', mode, 'numeric_with_error', True)
        for enabled in ('enabled', 'disabled'):
            add('control', 'maintenance', mode, enabled, False)
    return result


def parse_outcomes(raw, expected_ids, *, termination='exited'):
    """Parse conventional unittest evidence, never a summary as execution.

    This is not hostile-producer authentication. Historical inputs have separate
    exact-byte gates; other supplied text is only an observation of that text.
    """
    require(type(expected_ids) in (list, tuple) and bool(expected_ids), 'method list required')
    require(all(type(x) is str and re.fullmatch(METHOD, x) for x in expected_ids), 'invalid method identity')
    require(len(set(expected_ids)) == len(expected_ids), 'duplicate expected method')
    require(termination in ('exited', 'timed_out', 'interrupted'), 'terminal child state required')
    require(raw is None or type(raw) is bytes, 'raw stderr bytes or absent required')
    payload = b'' if raw is None else raw
    require(len(payload) <= MAX_MEMBER, 'stderr bound exceeded')
    limitations = []
    try:
        text = payload.decode('utf-8')
    except UnicodeDecodeError:
        text = payload.decode('utf-8', errors='replace')
        limitations.append('invalid_utf8')
    if raw is None:
        limitations.append('stderr_absent')
    outcomes, seen = [], set()
    for line in text.splitlines():
        match = ROW.fullmatch(line)
        if match is None:
            if line.startswith('test_') and ' ... ' in line:
                require(line == text.splitlines()[-1] and not text.endswith('\n'), 'unsupported outcome row')
            continue
        method, status = match.groups()
        require(method in expected_ids, 'unknown method outcome')
        require(method not in seen, 'duplicate method outcome')
        require(status in ('ok', 'FAIL', 'ERROR'), 'unsupported or skipped outcome')
        seen.add(method)
        outcomes.append({'method': method, 'status': status})
    counts = {status: sum(x['status'] == status for x in outcomes) for status in ('ok', 'FAIL', 'ERROR')}
    require(len(SUMMARY_HEADER.findall(text)) <= 1, 'multiple summary blocks refused')
    summary = SUMMARY.search(text)
    summary_count, summary_seconds = None, None
    if summary:
        summary_count = int(summary.group(1))
        summary_seconds = float(summary.group(2))
        require(math.isfinite(summary_seconds), 'nonfinite summary duration')
        require(len(seen) <= summary_count <= len(expected_ids), 'summary population contradiction')
        claimed_fail = re.search(r'failures=([0-9]+)', summary.group(3))
        claimed_error = re.search(r'errors=([0-9]+)', summary.group(3))
        claimed = {'FAIL': int(claimed_fail.group(1)) if claimed_fail else 0,
                   'ERROR': int(claimed_error.group(1)) if claimed_error else 0}
        unsuccessful = claimed['FAIL'] + claimed['ERROR']
        require(unsuccessful <= summary_count, 'summary status population contradiction')
        require(summary.group(3) == 'OK' or unsuccessful > 0, 'FAILED without failure or error')
        claimed['ok'] = summary_count - unsuccessful
        for status in counts:
            require(counts[status] <= claimed[status], 'observed status exceeds summary: ' + status)
            if len(seen) == summary_count:
                require(counts[status] == claimed[status], 'status total mismatch: ' + status)
    else:
        limitations.append('terminal_summary_absent')
    complete = bool(summary and len(seen) == summary_count == len(expected_ids)
                    and not limitations and termination == 'exited')
    return {'expected_count': len(expected_ids), 'observed_count': len(outcomes),
            'outcomes': outcomes, 'counts': counts, 'complete': complete,
            'termination': termination, 'limitations': limitations,
            'stderr': {**identity(payload), 'present': raw is not None},
            'summary_count': summary_count, 'summary_seconds': summary_seconds}


def original_predicate(raw, returncode, mutant, expected_tests=71):
    """Evaluate original output conditions, without executing the wrapper.

    UNKNOWN preserves an unavailable child return code. This keeps the original
    substring predicate; parse_outcomes is a separate stricter gate.
    """
    require(type(raw) is bytes and type(mutant) is bool, 'bytes and exact Boolean required')
    require(returncode is None or type(returncode) is int, 'integer or absent returncode required')
    require(type(expected_tests) is int and expected_tests > 0, 'positive test count required')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        return 'REFUSED'
    if f'Ran {expected_tests} tests' not in text or 'skipped=' in text:
        return 'REFUSED'
    if mutant and (any(x in text for x in ('SyntaxError', 'ImportError', '\nERROR:'))
                   or 'AssertionError' not in text or 'FAILED (failures=' not in text):
        return 'REFUSED'
    if returncode is None:
        return 'UNKNOWN'
    return 'ACCEPTED' if ((returncode != 0) if mutant else (returncode == 0)) else 'REFUSED'


def verify_sources(files):
    """Verify supplied historical source bytes; parse AST as inert data only."""
    require(type(files) is dict and 'SOURCE_FILES.json' in files, 'historical source mapping required')
    manifest_raw = files['SOURCE_FILES.json']
    require(identity(manifest_raw) == {'bytes': 1760, 'sha256': MANIFEST_SHA}, 'historical manifest identity mismatch')
    pins = strict_json(manifest_raw)['files']
    require(set(files) == set(pins) | {'SOURCE_FILES.json'}, 'historical source membership mismatch')
    for name, expected in pins.items():
        require(identity(files[name]) == expected, 'historical source identity mismatch: ' + name)
    method_ids = []
    for name in ('test_hard_gate.py', 'test_transition_contract.py'):
        tree = ast.parse(files[name].decode('utf-8'))
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for method in cls.body:
                if isinstance(method, ast.FunctionDef) and method.name.startswith('test_'):
                    method_ids.append(f'{method.name} ({name[:-3]}.{cls.name}.{method.name})')
    require(len(method_ids) == len(set(method_ids)) == 71, 'historical method identity mismatch')
    wrapper = ast.parse(files['run_validation.py'].decode('utf-8'))
    assignments = [node.value for node in wrapper.body if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'MUTANTS' for t in node.targets)]
    require(len(assignments) == 1, 'mutation assignment missing or ambiguous')
    mutations = ast.literal_eval(assignments[0])
    require(type(mutations) is dict and len(mutations) == 24, 'mutation population mismatch')
    gate = files['hard_gate.py'].decode('utf-8')
    anchors = {}
    for name, (old, new) in mutations.items():
        require(type(old) is str and type(new) is str and gate.count(old) == 1, 'nonunique mutation anchor: ' + name)
        anchors[name] = {'count': 1, 'anchor_sha256': hashlib.sha256(old.encode()).hexdigest()}
    old, new = mutations['accept_numeric_required']
    numeric = gate.replace(old, new).encode('utf-8')
    return {'source_commit': SOURCE_COMMIT, 'wrapper_blob': WRAPPER_BLOB,
            'pristine': {name: identity(raw) for name, raw in sorted(files.items())},
            'numeric_mutant': identity(numeric), 'method_ids': sorted(method_ids),
            'mutation_anchors': anchors, 'inspection': 'STATIC_ONLY_NO_PROJECT_EXECUTION'}


def historical_ledger(members):
    require(type(members) is dict and set(members) == set(MEMBERS), 'historical member set mismatch')
    for name, (size, digest) in MEMBERS.items():
        require(identity(members[name]) == {'bytes': size, 'sha256': digest}, 'historical member identity mismatch: ' + name)
    baseline = members['tests_normal.stderr']
    method_ids = [m.group(1) for line in baseline.decode('utf-8').splitlines() if (m := ROW.fullmatch(line))]
    require(len(method_ids) == len(set(method_ids)) == 71, 'historical baseline method population mismatch')
    first = parse_outcomes(baseline, method_ids)
    second_raw = members['mutation_normal_accept_numeric_required.stderr']
    second = parse_outcomes(second_raw, method_ids)
    require(first['complete'] and second['complete'], 'historical terminal outcome evidence incomplete')
    require(first['counts'] == {'ok': 71, 'FAIL': 0, 'ERROR': 0}, 'historical baseline counts changed')
    require(second['counts'] == {'ok': 68, 'FAIL': 2, 'ERROR': 1}, 'historical mutant counts changed')
    for record, raw, mutant in ((first, baseline, False), (second, second_raw, True)):
        record.update(returncode=None, returncode_provenance='NOT_RECORDED',
                      execution_origin='HISTORICAL_RECORDED_OUTPUT',
                      wrapper_decision=original_predicate(raw, None, mutant))
    return {'baseline': first, 'numeric_mutant': second,
            'original_report': strict_json(members['REPORT.json']),
            'member_identities': {n: identity(b) for n, b in sorted(members.items())}, 'cause': 'UNKNOWN'}


def stop_after_child(termination, unexpected_error, *, expected_error_control=False, wrapper_refused=False):
    """Pure decision about later scheduling; does not interrupt or run anything."""
    require(termination in ('exited', 'timed_out', 'interrupted'), 'child must be terminal')
    require(all(type(x) is bool for x in (unexpected_error, expected_error_control, wrapper_refused)), 'exact Boolean required')
    require(not expected_error_control or wrapper_refused, 'expected ERROR control must remain wrapper-refused')
    return termination != 'exited' or (unexpected_error and not expected_error_control)


def safe_member(name):
    require(type(name) is str and bool(name), 'member name required')
    path = PurePosixPath(name)
    require(not path.is_absolute() and not any(x in ('', '.', '..') for x in name.split('/'))
            and '\\' not in name and ':' not in name and '\x00' not in name, 'unsafe member name')


def read_zip_members(raw, required, *, expected_sha256, expected_bytes):
    """Generic custody primitive; canonical historical identity is in build_ledger."""
    require(type(expected_bytes) is int and 0 < expected_bytes <= MAX_TOTAL, 'archive bound invalid')
    require(identity(raw) == {'bytes': expected_bytes, 'sha256': expected_sha256}, 'archive identity mismatch')
    require(type(required) in (list, tuple) and len(required) == len(set(required)), 'unique member list required')
    for name in required:
        safe_member(name)
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            infos = archive.infolist()
            require(0 < len(infos) <= 1000, 'archive member population invalid')
            for info in infos:
                safe_member(info.orig_filename)
                require(info.orig_filename == info.filename, 'normalized archive member name refused')
            names = [x.filename for x in infos]
            require(len(names) == len(set(names)), 'archive member population invalid')
            require(sum(x.file_size for x in infos) <= MAX_TOTAL, 'archive expanded bound exceeded')
            require(set(required) <= set(names), 'required archive member absent')
            for info in infos:
                safe_member(info.filename)
                require(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG), 'nonregular archive member')
                require(info.file_size <= MAX_MEMBER and not info.flag_bits & 1, 'member size or encryption refused')
            result = {}
            for info in infos:
                # All bounded members are CRC-checked; no archive-controlled writes.
                with archive.open(info) as stream:
                    payload = stream.read(MAX_MEMBER + 1)
                require(len(payload) == info.file_size, 'member read size mismatch')
                if info.filename in required:
                    result[info.filename] = payload
            return result
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError) as error:
        raise ValueError('archive unreadable') from error


def build_ledger(*, members=None, source_files=None, archive_raw=None):
    gates = {'historical_members': 'NOT_RUN', 'archive_identity': 'NOT_RUN', 'source_identity': 'NOT_RUN'}
    if archive_raw is not None:
        decoded = read_zip_members(archive_raw, list(MEMBERS), expected_sha256=ARCHIVE_SHA, expected_bytes=ARCHIVE_BYTES)
        require(members is None or members == decoded, 'provided members differ from archive')
        members = decoded
        gates['archive_identity'] = 'VERIFIED'
    history = historical_ledger(members) if members is not None else None
    source = verify_sources(source_files) if source_files is not None else None
    if history is not None:
        gates['historical_members'] = 'VERIFIED'
    if source is not None:
        gates['source_identity'] = 'VERIFIED'
    if history is not None and source is not None:
        require(sorted(x['method'] for x in history['baseline']['outcomes']) == source['method_ids'], 'source/output method join mismatch')
    return {'schema_version': 1, 'meaning': 'offline evidence qualification only; no collector or theorem acceptance',
            'source_repository': 'd6g8k5htny-coder/Math-', 'source_commit': SOURCE_COMMIT,
            'historical_pr_head': PR_HEAD, 'historical_base': BASE_COMMIT,
            'historical_run': {'run': 37742226653, 'attempt': 1, 'job': 113195346919, 'artifact': 11534366248},
            'gates': gates, 'historical': history, 'source_identity': source,
            'helper_identity': identity(Path(__file__).read_bytes()), 'observer_identity': None,
            'planned_cases': planned_cases(), 'cause': 'UNKNOWN', 'runtime_provenance': 'INCOMPLETE_HISTORICAL',
            'missing_historical_provenance': ['effective_fixture_config', 'effective_environment', 'writer_pid_start',
                                            'residual_entries', 'binary_library_hashes', 'mount_identity'],
            'early_stop': 'STOP_SCHEDULING_AFTER_CHILD_EXIT_OR_CAP; interrupted outcomes remain partial',
            'promotion_permission': False, 'scientific_effect': 'NONE',
            'pr397_disposition': 'HOLD / NOT_READY / NO_MERGE'}


def read_regular(path, limit):
    path = Path(path)
    require(not any(part.is_symlink() for part in (path, *path.parents)), 'symlink input refused')
    metadata = path.stat()
    require(stat.S_ISREG(metadata.st_mode) and metadata.st_size <= limit, 'regular bounded input required')
    with path.open('rb') as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, 'input read bound exceeded')
    return raw


def main(argv=None, *, output=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, help='original11534366248 ZIP; exact identity required')
    parser.add_argument('--sources', type=Path, help='historical package directory; never imported')
    args = parser.parse_args(argv)
    output = sys.stdout if output is None else output
    try:
        archive = read_regular(args.archive, MAX_TOTAL) if args.archive else None
        source = None
        if args.sources:
            manifest = read_regular(args.sources / 'SOURCE_FILES.json', MAX_MEMBER)
            require(identity(manifest) == {'bytes': 1760, 'sha256': MANIFEST_SHA}, 'historical manifest identity mismatch')
            pins = strict_json(manifest)['files']
            source = {'SOURCE_FILES.json': manifest}
            for name in pins:
                safe_member(name)
                source[name] = read_regular(args.sources / name, MAX_MEMBER)
        result = build_ledger(archive_raw=archive, source_files=source)
        print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False), file=output)
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({'valid': False, 'error': str(error), 'promotion_permission': False,
                          'scientific_effect': 'NONE'}, sort_keys=True), file=output)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
