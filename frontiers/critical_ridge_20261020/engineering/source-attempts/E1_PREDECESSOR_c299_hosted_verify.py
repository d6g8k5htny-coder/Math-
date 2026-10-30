#!/usr/bin/env python3
"""C299 scoped hosted verification; no scientific promotion or human review.

Run from the existing pinned formal/ Lake environment. Sources are pinned by an
explicit manifest digest in the dedicated workflow. Every attempt retains exact
streams and a receipt before any failure is raised. No retry is performed.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import time

PREFIX = 'frontiers/critical_ridge_20261020'
WORKFLOW = '.github/workflows/c299-critical-ridge.yml'
MANIFEST = 'HOSTED_SOURCE_MANIFEST.json'
MODULES = ('Lifetime', 'TorusTopology', 'MorseFiniteCritical',
           'CriticalRidge', 'CriticalRidgeAxiomAudit')
REPLAY_MODULES = MODULES[1:]
AUDIT_MODULES = MODULES[:4]
NEGATIVES = ('WithoutCriticality', 'WithoutNegativeDefiniteness')
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
# Candidate-2 source names; formal execution and final diagnostic review pending.
REQUIRED = ('UniversalLaw.Spec.Lifetime.IsSmooth', 'UniversalLaw.Spec.Lifetime.IsCriticalPoint', 'UniversalLaw.Spec.Lifetime.hessian', 'TorusMorseFinite.literal_hessian_eq_fderiv', 'TorusCriticalRidge.restrictCovector', 'TorusCriticalRidge.ridgeAddition', 'TorusCriticalRidge.negativePartialGradient', 'TorusCriticalRidge.negativeHessianBlock', 'TorusCriticalRidge.negativeHessianBlock_apply', 'TorusCriticalRidge.negativeHessianBlock_isInvertible', 'TorusCriticalRidge.negativePartialGradient_contDiff', 'TorusCriticalRidge.negativePartialGradient_hasFDerivAt', 'TorusCriticalRidge.exists_negative_partial_gradient_ridge')
MATHLIB_PIN = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
LEAN_VERSION = '4.34.1'
PACKAGE_PINS = {
    'plausible': '118aa17ee84656b8bd727fef7c458ee8c833385c',
    'LeanSearchClient': 'ddf04cf3949fa556442341e87d47f9f6e6074707',
    'importGraph': 'e928b72544873815af278d38681b31c0293588e3',
    'proofwidgets': '106ff4fafc74ef4ac99d81dbf3ab399118f497a5',
    'aesop': '355695d523e41d0554926416cba2a2b3544fbbc9',
    'Qq': '6a489d9af5d0c47e5b259e2e8bcdfc1811b5a259',
    'batteries': 'f2effa3d803fda822b1f97b806c47cf2adfbcbc2',
    'Cli': 'e92c9f15fdfacc8536f31cfb3b7ad26c3c8cd204',
    'mathlib': MATHLIB_PIN,
}


def now():
    return datetime.now(timezone.utc).isoformat()


def identity(path):
    data = Path(path).read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def safe_source(path, root):
    path, root = Path(path).absolute(), Path(root).absolute()
    if not path.is_relative_to(root):
        raise RuntimeError(f'source outside repository: {path}')
    parts = path.relative_to(root).parts
    for n in range(1, len(parts) + 1):
        if root.joinpath(*parts[:n]).is_symlink():
            raise RuntimeError(f'symlinked source: {path}')
    if not path.is_file():
        raise RuntimeError(f'source missing or not regular: {path}')


def verify_file(path, expected, root):
    safe_source(path, root)
    if (set(expected) != {'bytes', 'sha256'} or
            type(expected['bytes']) is not int or expected['bytes'] < 1 or
            not re.fullmatch('[0-9a-f]{64}', expected['sha256'])):
        raise RuntimeError(f'invalid expected source identity: {path}')
    actual = identity(path)
    if actual != expected:
        raise RuntimeError(f'source identity mismatch: {path}: {actual}')
    return actual


def verify_sources(root, manifest_sha256):
    root = Path(root)
    packet = root / PREFIX
    path = packet / MANIFEST
    safe_source(path, root)
    if not re.fullmatch('[0-9a-f]{64}', manifest_sha256):
        raise RuntimeError('explicit frozen manifest SHA-256 required')
    if identity(path)['sha256'] != manifest_sha256:
        raise RuntimeError('frozen source manifest identity mismatch')
    manifest = json.loads(path.read_text())
    if manifest.get('schema_version') != 1 or manifest.get('scientific_effect') != 'NONE':
        raise RuntimeError('invalid C299 manifest schema or scientific-effect field')
    expected = {f'project/{m}.lean' for m in MODULES} | {
        f'negative-project/{m}.lean' for m in NEGATIVES}
    if set(manifest.get('files', {})) != expected:
        raise RuntimeError('manifest must bind exactly five modules and two controls')
    sources = {rel: verify_file(packet / rel, spec, root)
               for rel, spec in manifest['files'].items()}
    origins = manifest.get('source_origins', {})
    if set(origins) != {'Lifetime', 'TorusTopology', 'MorseFiniteCritical'}:
        raise RuntimeError('all three frozen input source origins are required')
    for name, origin in origins.items():
        if (not isinstance(origin, dict) or not re.fullmatch('[0-9a-f]{40}', origin.get('commit', ''))
                or not isinstance(origin.get('path'), str) or not origin['path']
                or Path(origin['path']).is_absolute() or '..' in Path(origin['path']).parts):
            raise RuntimeError(f'invalid input source origin: {name}')
    upstream = root / 'specifications/lean_statements_20261010/Specifications/Lifetime.lean'
    verify_file(upstream, manifest['files']['project/Lifetime.lean'], root)
    config = {}
    for rel in ('formal/lean-toolchain', 'formal/lakefile.toml', 'formal/lake-manifest.json'):
        safe_source(root / rel, root)
        config[rel] = identity(root / rel)
    if (root / 'formal/lean-toolchain').read_text().strip() != 'leanprover/lean4:v' + LEAN_VERSION:
        raise RuntimeError('Lean toolchain pin changed')
    if f'rev = "{MATHLIB_PIN}"' not in (root / 'formal/lakefile.toml').read_text():
        raise RuntimeError('Lake mathlib pin changed')
    lock = json.loads((root / 'formal/lake-manifest.json').read_text())
    if {p['name']: p['rev'] for p in lock['packages']} != PACKAGE_PINS:
        raise RuntimeError('dependency lock pins changed')
    support = {}
    for rel in (WORKFLOW, PREFIX + '/c299_hosted_verify.py',
                PREFIX + '/test_c299_hosted_verify.py'):
        safe_source(root / rel, root)
        support[rel] = identity(root / rel)
    return {'manifest': identity(path), 'files': sources, 'source_origins': origins,
            'source_origin_limit': 'Remote origin byte equality is a separate owner custody check.',
            'formal_config': config, 'support_files': support, 'dependency_pins': PACKAGE_PINS}


def audit_records(output):
    """Join Lean's wrapped AXIOMS arrays; reject interrupted or truncated records."""
    pending = None
    for line in output.splitlines():
        if pending is not None:
            if 'CRITICAL_RIDGE_AUDIT_' in line:
                raise RuntimeError('audit declaration interrupted before closing axiom list')
            pending += ' ' + line.strip()
            if ']' in line:
                yield pending
                pending = None
            continue
        if 'CRITICAL_RIDGE_AUDIT_' not in line:
            continue
        marker = line[line.index('CRITICAL_RIDGE_AUDIT_'):].strip()
        if marker.startswith('CRITICAL_RIDGE_AUDIT_PROGRESS '):
            continue
        if marker.startswith('CRITICAL_RIDGE_AUDIT_DECL ') and 'AXIOMS [' in marker and ']' not in marker:
            pending = marker
            continue
        yield marker
    if pending is not None:
        raise RuntimeError('truncated audit axiom list')


def validate_audit(output, modules=AUDIT_MODULES, required=REQUIRED):
    """Read every module-origin record, not just a total or public-name sample."""
    counts, names, current, seen = {}, {}, None, set()
    total = None
    for marker in audit_records(output):
        m = re.fullmatch(r'CRITICAL_RIDGE_AUDIT_MODULE (\S+) COUNT (\d+)', marker)
        if m:
            current, count = m.group(1), int(m.group(2))
            if total is not None or current not in modules or current in counts or count < 1:
                raise RuntimeError('invalid or duplicate audit module census')
            counts[current], names[current] = count, []
            continue
        m = re.fullmatch(r'CRITICAL_RIDGE_AUDIT_DECL (\S+) AXIOMS \[([^\[\]]*)\]', marker)
        if m:
            name, raw_axioms = m.groups()
            axioms = {s.strip() for s in raw_axioms.split(',') if s.strip()}
            if current is None or total is not None or name in seen or not axioms <= ALLOWED_AXIOMS:
                raise RuntimeError('invalid, repeated or forbidden audit declaration')
            names[current].append(name)
            seen.add(name)
            continue
        m = re.fullmatch(r'CRITICAL_RIDGE_AUDIT_STANDARD_ONLY_PASS COUNT (\d+)', marker)
        if m and total is None:
            total = int(m.group(1))
            continue
        raise RuntimeError(f'unrecognized or repeated audit marker: {marker}')
    if (tuple(counts) != tuple(modules) or total != len(seen) or total != sum(counts.values())
            or any(len(names[m]) != counts[m] for m in counts)
            or not set(required) <= seen):
        raise RuntimeError('incomplete audit census or missing required target')
    return {'module_counts': counts, 'declaration_count': total,
            'required_targets': list(required), 'allowed_axioms': sorted(ALLOWED_AXIOMS),
            'module_declarations': names}


def require_final_predicates():
    """Draft stop: replace only after exact source/fixtures/diagnostics review.

    This explicit stop blocks final acceptance AFTER both control attempts.
    Development may collect actual build/kernel/diagnostic evidence. The draft
    parser supplies reviewable intended-type logic; synthetic fixture tests are
    not actual Lean diagnostics or final acceptance.
    """
    raise RuntimeError('PENDING_C299_NEGATIVE_PREDICATES: actual diagnostics and final source freeze required')


def validate_negative(name, returncode, output):
    return validate_negative_draft(name, returncode, output)


def validate_negative_draft(name, returncode, output):
    """Candidate diagnostic parser; final observed spelling must be reviewed."""
    if name not in NEGATIVES:
        raise RuntimeError('unknown negative control')
    flat = ' '.join(output.split())
    forbidden = ('unknown identifier', 'unknown module', 'file not found', 'no such file',
                 'memory_exception', 'out of memory', 'unexpected token', 'unsolved goals',
                 'maximum recursion', 'maximum heartbeats', 'failed to', 'panic', 'sorry')
    if (returncode != 1 or output.count('error:') != 1
            or any(x in flat.lower() for x in forbidden)):
        raise RuntimeError('negative control failed for an unrelated reason')
    pattern = (r'\A[^\n]*' + re.escape(name) + r'\.lean:\d+:\d+: error: Type mismatch\s*\n'
               r'(?P<expression>.*?)\nhas type\s*\n(?P<actual>.*?)'
               r'\nbut is expected to have type\s*\n(?P<expected>.*?)\s*\Z')
    match = re.fullmatch(pattern, output.strip(), flags=re.S)
    if match is None:
        raise RuntimeError('expected one source-bound type-mismatch diagnostic')
    expression, actual, expected = (' '.join(match.group(k).split())
                                    for k in ('expression', 'actual', 'expected'))
    target = 'TorusCriticalRidge.exists_negative_partial_gradient_ridge'
    if target not in expression or 'f p V hsmooth' not in expression:
        raise RuntimeError('wrong actual theorem application')
    if name == 'WithoutCriticality':
        if not re.fullmatch(r'fun hcritical => ' + re.escape(target)
                            + r' f p V hsmooth hcritical hneg', expression):
            raise RuntimeError('wrong criticality-omission application')
        premise = r'IsCriticalPoint d f p'
    else:
        if expression != target + ' f p V hsmooth hcritical':
            raise RuntimeError('wrong negative-definiteness-omission application')
        premise = r'\(∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0\)'
    if not re.fullmatch(premise + r' → ' + re.escape(expected), actual):
        raise RuntimeError('actual type is not the omitted premise followed by the expected conclusion')
    # Fixed candidate-2 binder names and all four same-ridge conclusion fields.
    conclusion = (r'∃ r, r 0 = 0 ∧ ContDiffAt ℝ 2 r 0 ∧ '
                  r'\(∀ᶠ w in 𝓝 0, ∀ \(z : ↥V\), \(fderiv ℝ f \(p \+ w \+ ↑\(r w\)\)\) ↑z = 0\) ∧ '
                  r'∀ \(w : E d\) \(z : ↥V\), hessian d f p \(w \+ ↑\(\(fderiv ℝ r 0\) w\)\) ↑z = 0')
    if not re.fullmatch(conclusion, expected):
        raise RuntimeError('expected conclusion does not match all four candidate ridge fields')
    return {'control': name, 'diagnostic_source': name + '.lean',
            'draft_only': True, 'actual_diagnostic_observed': False}


def save_report(evidence, report):
    (evidence / 'RESULT.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')


def save_phase(evidence, report, record):
    (evidence / (record['name'] + '.receipt.json')).write_text(
        json.dumps(record, indent=2, sort_keys=True) + '\n')
    save_report(evidence, report)


def object_inventory(build):
    result = {}
    for path in sorted(Path(build).iterdir()):
        safe_source(path, build)
        result[path.name] = identity(path)
    return result


def validate_objects(before, after, build_module=None):
    if any(after.get(name) != spec for name, spec in before.items()):
        raise RuntimeError('previous local input object changed or disappeared')
    additions = set(after) - set(before)
    if build_module is None:
        if additions:
            raise RuntimeError('non-build phase added an unexpected local object')
        return
    allowed = {build_module + suffix for suffix in
               ('.olean', '.olean.private', '.olean.server', '.ilean', '.ir')}
    if build_module + '.olean' not in additions or not additions <= allowed:
        raise RuntimeError('build must add only its own target object outputs')


def run_phase(name, args, cwd, env, evidence, report, expected_success=True,
              timeout=900, build_dir=None, build_module=None):
    """Persist raw streams, per-phase receipt, and aggregate receipt before raise."""
    if not re.fullmatch('[A-Za-z0-9_-]+', name):
        raise RuntimeError('unsafe phase name')
    evidence = Path(evidence)
    out_path, err_path = evidence / (name + '.stdout'), evidence / (name + '.stderr')
    start, utc_start = time.monotonic(), now()
    timed_out, spawn_error, code = False, None, None
    objects_before, objects_after, object_error = None, None, None
    with out_path.open('xb') as stdout, err_path.open('xb') as stderr:
        try:
            if build_dir is not None:
                objects_before = object_inventory(build_dir)
        except (OSError, RuntimeError) as exc:
            object_error = str(exc)
        if object_error is None:
            try:
                proc = subprocess.Popen(args, cwd=cwd, env=env, stdout=stdout, stderr=stderr,
                                        start_new_session=True)
                try:
                    code = proc.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    try:
                        os.killpg(proc.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    try:
                        code = proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        code = proc.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired) as exc:
                spawn_error = str(exc)
        if build_dir is not None:
            try:
                objects_after = object_inventory(build_dir)
                if object_error is None:
                    validate_objects(objects_before, objects_after, build_module)
            except (OSError, RuntimeError) as exc:
                object_error = str(exc)
    valid = (not timed_out and spawn_error is None and object_error is None and
             (code == 0 if expected_success else code == 1))
    record = {'name': name, 'command': list(args), 'cwd': str(cwd),
              'started_at': utc_start, 'finished_at': now(),
              'duration_seconds': round(time.monotonic() - start, 6),
              'timeout_seconds': timeout, 'timed_out': timed_out,
              'spawn_error': spawn_error, 'exit_code': code,
              'stdout_sha256': identity(out_path)['sha256'], 'stdout_bytes': out_path.stat().st_size,
              'stderr_sha256': identity(err_path)['sha256'], 'stderr_bytes': err_path.stat().st_size,
              'objects_before': objects_before, 'objects_after': objects_after,
              'object_validation_error': object_error,
              'status': 'PASS' if valid else 'FAIL'}
    report['phase_results'].append(record)
    save_phase(evidence, report, record)
    print(f'C299 {name}: exit={code} timeout={timed_out} seconds={record["duration_seconds"]}', flush=True)
    if not valid:
        raise RuntimeError(f'C299 {name} unexpected exit: {code}; timed_out={timed_out}; '
                           f'spawn_error={spawn_error}; object_error={object_error}')
    output = out_path.read_bytes().decode('utf8', 'replace') + '\n' + err_path.read_bytes().decode('utf8', 'replace')
    return record, output, code


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True, timeout=30).strip()


def verify_packages(root):
    result = {}
    for name, expected in PACKAGE_PINS.items():
        path = root / 'formal/.lake/packages' / name
        actual = git(path, 'rev-parse', 'HEAD')
        if actual != expected or git(path, 'status', '--porcelain', '--untracked-files=no'):
            raise RuntimeError(f'installed dependency mismatch or tracked change: {name}')
        result[name] = actual
    return result


def hosted_context(root):
    keys = ('GITHUB_SHA', 'GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT', 'GITHUB_REPOSITORY',
            'GITHUB_EVENT_NAME', 'GITHUB_WORKFLOW', 'GITHUB_JOB')
    if any(not os.environ.get(k) for k in keys):
        raise RuntimeError('actual GitHub execution context required')
    if os.environ['GITHUB_REPOSITORY'] != 'd6g8k5htny-coder/Math-':
        raise RuntimeError('wrong repository')
    head = git(root, 'rev-parse', 'HEAD')
    if head != os.environ['GITHUB_SHA']:
        raise RuntimeError('tested checkout does not match GITHUB_SHA')
    context = {k.lower(): os.environ[k] for k in keys}
    context['tested_commit'] = head
    context['tested_tree'] = git(root, 'rev-parse', 'HEAD^{tree}')
    context['tested_parents'] = git(root, 'show', '-s', '--format=%P', 'HEAD').split()
    event_path = Path(os.environ.get('GITHUB_EVENT_PATH', '/nonexistent'))
    if event_path.is_file():
        event = json.loads(event_path.read_text())
        if 'pull_request' in event:
            context['pull_request'] = {
                'number': event['number'], 'head_sha': event['pull_request']['head']['sha'],
                'base_sha': event['pull_request']['base']['sha']}
    context['executor'] = 'GitHub-hosted runner executing C299 verification code'
    context['human_review_credit'] = 0
    return context


def source_only(root, digest):
    evidence = root / '.lake/c299-hosted-evidence'
    evidence.mkdir(parents=True, exist_ok=False)
    report = {'status': 'HOLD_SOURCE_PREFLIGHT', 'scientific_effect': 'NONE',
              'phase_results': [], 'started_at': now()}
    save_report(evidence, report)
    try:
        report['context'] = hosted_context(root)
        report['source_identity'] = verify_sources(root, digest)
        snapshots = evidence / 'source-snapshot'
        for relative in report['source_identity']['files']:
            dest = snapshots / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / PREFIX / relative, dest)
        shutil.copyfile(root / PREFIX / MANIFEST, evidence / MANIFEST)
        for relative in report['source_identity']['support_files']:
            dest = snapshots / 'repository' / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / relative, dest)
        report['status'] = 'PASS_SOURCE_PREFLIGHT_ONLY'
    except BaseException as exc:
        report['status'], report['failure'] = 'HOLD_SOURCE_PREFLIGHT_FAILED', repr(exc)
        raise
    finally:
        save_report(evidence, report)


def execute(root, digest):
    packet, formal = root / PREFIX, root / 'formal'
    evidence = root / '.lake/c299-hosted-evidence'
    report = json.loads((evidence / 'RESULT.json').read_text())
    if report['status'] != 'PASS_SOURCE_PREFLIGHT_ONLY' or report['phase_results']:
        raise RuntimeError('exact unused source preflight required; no automatic retry')
    build = evidence / 'objects'
    build.mkdir(exist_ok=False)
    report.update(status='HOLD_NOT_COMPLETED', started_execution_at=now(),
                  memory_limit='-M14000', threads=2, phase_timeout_seconds=900,
                  memory_limit_reason='Explicit Linux execution budget; not a claim that C299 requires this amount.',
                  verification_scope='Five fresh local objects; four standard named-module kernel replays; full four-module axiom census; two omitted-premise interface controls.',
                  replay_limit='Not a --fresh replay or rebuild of the full dependency closure.')
    save_report(evidence, report)
    try:
        context = hosted_context(root)
        if context != report['context']:
            raise RuntimeError('execution context changed since source preflight')
        source_before = verify_sources(root, digest)
        if source_before != report['source_identity']:
            raise RuntimeError('inputs changed since source preflight')
        report['packages_before'] = verify_packages(root)
        env = dict(os.environ)
        env['LEAN_PATH'] = str(build) + os.pathsep + env.get('LEAN_PATH', '')
        env['LEAN_NUM_THREADS'] = '2'
        launcher = shutil.which('lean')
        if launcher is None:
            raise RuntimeError('missing Lean launcher')
        launcher = Path(launcher).resolve()
        report['lean_launcher'] = {'path': str(launcher), **identity(launcher)}
        # Resolve the toolchain prefix through the selected launcher, then execute
        # the measured toolchain binaries directly; an elan shim is not the runtime.
        _, prefix_output, _ = run_phase('runtime-print-prefix',
            [str(launcher), '--print-prefix'], formal, env, evidence, report, timeout=30)
        prefix = Path(prefix_output.strip())
        if not prefix.is_absolute() or not prefix.is_dir():
            raise RuntimeError('Lean did not return an existing absolute toolchain prefix')
        runtimes = {}
        for executable in ('lean', 'leanchecker'):
            binary = (prefix / 'bin' / executable).resolve()
            if not binary.is_file() or not os.access(binary, os.X_OK):
                raise RuntimeError(f'missing toolchain runtime: {executable}')
            runtimes[executable] = {'path': str(binary), **identity(binary)}
        report['runtimes'] = runtimes
        report['machine'] = {'platform': platform.platform(), 'machine': platform.machine(),
                             'python': platform.python_version()}
        _, version, _ = run_phase('runtime-version', [runtimes['lean']['path'], '--version'],
                                  formal, env, evidence, report, timeout=30)
        if 'version ' + LEAN_VERSION not in version:
            raise RuntimeError('wrong Lean runtime version')
        report['lean_version_output'] = version
        for module in MODULES:
            args = [runtimes['lean']['path'], '-j2', '-M14000']
            if module != 'Lifetime':
                args += ['-DwarningAsError=true']
            args += ['-o', str(build / (module + '.olean')),
                     str(packet / 'project' / (module + '.lean'))]
            rec, output, _ = run_phase('build-' + module, args, packet / 'project', env, evidence, report,
                                       build_dir=build, build_module=module)
            obj = build / (module + '.olean')
            safe_source(obj, evidence)
            rec['object'] = identity(obj)
            if module == 'CriticalRidgeAxiomAudit':
                report['audit'] = validate_audit(output)
            if verify_sources(root, digest) != source_before:
                raise RuntimeError('inputs changed during build')
            save_phase(evidence, report, rec)
        built_objects = object_inventory(build)
        expected_main = {m + '.olean' for m in MODULES}
        allowed_outputs = {m + suffix for m in MODULES for suffix in
                           ('.olean', '.olean.private', '.olean.server', '.ilean', '.ir')}
        if not expected_main <= set(built_objects) or not set(built_objects) <= allowed_outputs:
            raise RuntimeError('unexpected complete final object set')
        report['objects_after_builds'] = built_objects
        save_report(evidence, report)
        for module in REPLAY_MODULES:
            run_phase('kernel-' + module, [runtimes['leanchecker']['path'], '-v', module],
                      packet / 'project', env, evidence, report, build_dir=build)
        report['negative_classification_errors'] = []
        report['negative_predicates_qualified'] = False
        for name in NEGATIVES:
            rec = None
            try:
                rec, output, code = run_phase('negative-' + name,
                    [runtimes['lean']['path'], '-j2', '-M14000', str(packet / 'negative-project' / (name + '.lean'))],
                    packet / 'negative-project', env, evidence, report, expected_success=False,
                    build_dir=build)
                validate_negative(name, code, output)
                rec['candidate_parser_match'] = True
            except RuntimeError as exc:
                # run_phase persists its receipt before raising. Preserve a
                # rejected spelling/exit and gather the second distinct control.
                if rec is None:
                    rec = report['phase_results'][-1]
                    if rec['name'] != 'negative-' + name:
                        raise
                rec['candidate_parser_match'] = False
                rec['negative_classification_error'] = str(exc)
                report['negative_classification_errors'].append({'control': name, 'error': str(exc)})
                if rec.get('object_validation_error') is not None:
                    save_phase(evidence, report, rec)
                    raise
            rec['intended_missing_premise_rejection'] = False
            rec['diagnostic_qualification_pending'] = True
            save_phase(evidence, report, rec)
        report['packages_after'] = verify_packages(root)
        report['source_identity_after'] = verify_sources(root, digest)
        if report['source_identity_after'] != source_before:
            raise RuntimeError('inputs changed during verification')
        for executable, spec in runtimes.items():
            if identity(spec['path']) != {k: spec[k] for k in ('bytes', 'sha256')}:
                raise RuntimeError(f'runtime changed: {executable}')
        report['objects'] = object_inventory(build)
        if report['objects'] != built_objects:
            raise RuntimeError('local objects changed during kernel or negative phases')
        if report['negative_classification_errors']:
            raise RuntimeError('C299 negative diagnostics require source-bound review: '
                               + repr(report['negative_classification_errors']))
        require_final_predicates()
        report['status'] = 'PASS_HOSTED_C299_EXACT_TARGETS'
        report['completed_at'] = now()
        print('C299_HOSTED_FORMAL_PASS: scoped formal execution only; scientific effect NONE.', flush=True)
    except BaseException as exc:
        report['status'], report['failure'] = 'HOLD_NOT_COMPLETED', repr(exc)
        raise
    finally:
        save_report(evidence, report)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('source', 'execute'))
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    # Published location is exactly frontiers/<packet>/c299_hosted_verify.py.
    root = Path(__file__).resolve().parents[2]
    if args.mode == 'source':
        source_only(root, args.manifest_sha256)
    else:
        execute(root, args.manifest_sha256)


if __name__ == '__main__':
    main()
