#!/usr/bin/env python3
"""UNEXECUTED R2 adapter hosted collector candidate; no scientific promotion.

Adapted as source text from C299 c299_hosted_verify.py at Math- commit
c8d66bde8ce496c1007e4a3f6b0a9f9f93762bfb. Original collector and its inert-control
results do not validate these adaptations. No local syntax/test/Lean run occurred.

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
import resource
import shutil
import signal
import subprocess
import time

PREFIX = 'frontiers/quotient_closed_superlevel_lpc_adapter_20261020'
WORKFLOW = '.github/workflows/quotient-closed-superlevel-lpc-adapter.yml'
MANIFEST = 'HOSTED_SOURCE_MANIFEST.json'
MODULES = ('Lifetime', 'TorusTopology', 'SuperlevelBar', 'ClosedSuperlevel',
           'MorseFiniteCritical', 'CriticalLevelAttainment',
           'QuoClosedSuperlevelAdapter', 'QuoClosedSuperlevelAudit')
INPUT_MODULES = MODULES[:6]
REPLAY_MODULES = ('QuoClosedSuperlevelAdapter',)
NEGATIVES = ('OmittedEuclideanLPC',)
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
REQUIRED = tuple('TorusCriticalAttainment.QuotientSuperlevelAdapter.' + name for name in (
    'torus_proj_isOpenQuotientMap', 'closedSuperlevel_preimage',
    'quotient_closedSuperlevel_lpc_of_euclidean',
    'quotient_death_attainment_of_euclidean_closedLPC'))
PHASE_SECONDS = 360
DRIVER_SECONDS = 3900
EXPECTED_BASE = '8c226134ac0a0169dbb43311082e5353ed5c922c'
EXPECTED_BRANCH = 'codex/quotient-closed-superlevel-lpc-adapter-20261020-r2'
ORIGIN_COMMIT = '7af365e8c8db1ae0275d4efe08a70a678f153ca2'
ORIGIN_PREFIX = 'frontiers/critical_level_attainment_20261020/final-project/'


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
        raise RuntimeError('invalid adapter source manifest')
    expected = {f'project/{m}.lean' for m in MODULES} | {
        f'negative-project/{m}.lean' for m in NEGATIVES}
    if set(manifest.get('files', {})) != expected:
        raise RuntimeError('manifest must bind exactly eight modules and one control')
    if manifest.get('build_order') != list(MODULES) or manifest.get('required_targets') != list(REQUIRED):
        raise RuntimeError('stale or substituted build/target inventory')
    sources = {rel: verify_file(packet / rel, spec, root)
               for rel, spec in manifest['files'].items()}
    actual_lean = {str(p.relative_to(packet)) for folder in ('project', 'negative-project')
                   for p in (packet / folder).rglob('*.lean')}
    if actual_lean != expected:
        raise RuntimeError('missing or extra actual Lean source')
    origins = manifest.get('source_origins', {})
    if set(origins) != set(INPUT_MODULES):
        raise RuntimeError('all six frozen input source origins are required')
    for name, origin in origins.items():
        if origin != {'commit': ORIGIN_COMMIT, 'path': ORIGIN_PREFIX + name + '.lean'}:
            raise RuntimeError('wrong frozen source origin: ' + name)
    config = {}
    for rel, spec in manifest['formal_config'].items():
        config[rel] = verify_file(root / rel, spec, root)
    if set(config) != {'formal/lean-toolchain', 'formal/lakefile.toml', 'formal/lake-manifest.json'}:
        raise RuntimeError('exact three formal configuration files required')
    if (root / 'formal/lean-toolchain').read_text().strip() != 'leanprover/lean4:v' + LEAN_VERSION:
        raise RuntimeError('Lean toolchain pin changed')
    lock = json.loads((root / 'formal/lake-manifest.json').read_text())
    if {p['name']: p['rev'] for p in lock['packages']} != PACKAGE_PINS:
        raise RuntimeError('dependency lock pins changed')
    support = {}
    for rel, spec in manifest['support_files'].items():
        support[rel] = verify_file(root / rel, spec, root)
    expected_support = {PREFIX + '/' + n for n in (
        'quo_hosted_verify.py', 'test_quo_hosted_verify.py', 'EXECUTION_CONTRACT.md',
        'TARGET_INVENTORY.json', 'DEPENDENCY_LOCK.json', 'PROVENANCE.md')}
    if set(support) != expected_support:
        raise RuntimeError('exact collector/control/contract/inventory/lock/provenance set required')
    safe_source(root / WORKFLOW, root)
    return {'manifest': identity(path), 'files': sources, 'source_origins': origins,
            'formal_config': config, 'support_files': support,
            'workflow_observed': identity(root / WORKFLOW),
            'workflow_binding_limit': 'Exact workflow/commit binding requires external prepublication review.',
            'dependency_pins': PACKAGE_PINS}


def validate_audit(output, required=REQUIRED):
    """Require all four fully qualified #print axioms reports; no empty target gate."""
    if tuple(required) != REQUIRED or len(required) != 4 or not ALLOWED_AXIOMS:
        raise RuntimeError('exact nonempty four-target and standard-axiom inventories required')
    if 'error:' in output.lower():
        raise RuntimeError('audit emitted an error')
    pattern = (r"'([^']+)' (?:does not depend on any axioms|"
               r"depends on axioms:\s*\[([^\[\]]*)\])")
    found = {}
    for match in re.finditer(pattern, output, flags=re.S):
        name, raw = match.groups()
        if name in found or name not in required:
            raise RuntimeError('duplicate or extra audit target')
        axioms = {s.strip() for s in (raw or '').split(',') if s.strip()}
        if not axioms <= ALLOWED_AXIOMS:
            raise RuntimeError('forbidden axiom in target report')
        found[name] = sorted(axioms)
    if set(found) != set(required):
        raise RuntimeError('missing exact target axiom report')
    return {'required_targets': list(required), 'allowed_axioms': sorted(ALLOWED_AXIOMS),
            'target_axioms': found, 'scope': 'Four explicit transitive axiom reports; not full dependency census.'}


def require_final_predicates():
    raise RuntimeError('PENDING_ADAPTER_NEGATIVE_PREDICATE: actual line25 explicit-LPC diagnostic needs distinct source-bound review')


def validate_negative(name, returncode, output):
    if name != 'OmittedEuclideanLPC' or returncode != 1:
        raise RuntimeError('wrong control or non-diagnostic exit')
    flat = ' '.join(output.split())
    forbidden = ('unknown identifier', 'unknown module', 'file not found', 'no such file',
                 'memory_exception', 'out of memory', 'unexpected token', 'unsolved goals',
                 'maximum recursion', 'maximum heartbeats', 'failed to', 'panic', 'sorry',
                 'failed to synthesize', 'failed to synthesize instance')
    if output.count('error:') != 1 or any(x in flat.lower() for x in forbidden):
        raise RuntimeError('negative control failed for an unrelated reason')
    pattern = (r'\A[^\n]*OmittedEuclideanLPC\.lean:25:\d+: error: Type mismatch\s*\n'
               r'(?P<expression>.*?)\nhas type\s*\n(?P<actual>.*?)'
               r'\nbut is expected to have type\s*\n(?P<expected>.*?)\s*\Z')
    m = re.fullmatch(pattern, output.strip(), flags=re.S)
    if m is None:
        raise RuntimeError('expected exactly line25 explicit missing-LPC type mismatch')
    expression, actual, expected = (' '.join(m.group(k).split())
                                    for k in ('expression', 'actual', 'expected'))
    target = REQUIRED[2]
    if expression not in (target + ' d L hL g hperiodic a',
                          'quotient_closedSuperlevel_lpc_of_euclidean d L hL g hperiodic a'):
        raise RuntimeError('wrong unapplied adapter expression')
    if not expected.startswith('LocallyPathConnectedSpace '):
        raise RuntimeError('expected type is not the quotient LPC proof')
    quotient = (r'LocallyPathConnectedSpace \{ q(?: : torus_quotient d L hL)? // '
                r'a ≤ (?:TorusCriticalAttainment\.)?descendedHeight d L hL g hperiodic q \}')
    if not re.fullmatch(quotient, expected):
        raise RuntimeError('wrong literal quotient or descended-height expected type')
    if not re.fullmatch(r'LocallyPathConnectedSpace \{ x(?: : E d)? // a ≤ g x \} → ' + re.escape(expected), actual):
        raise RuntimeError('actual type is not EXPLICIT Euclidean-LPC argument followed by exact expected proof')
    return {'control': name, 'diagnostic_line': 25, 'draft_only': True,
            'actual_diagnostic_observed': False, 'explicit_missing_argument': True}


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


ENVIRONMENT_POLICY = (
    'Remove inherited LEAN*, LAKE*, LD_* and DYLD_* overrides, except the '
    'Lake-provided LEAN_PATH; prepend the fresh local object directory to that '
    'path and set LEAN_NUM_THREADS=2. Retain declared PATH for launcher lookup. '
    'Only PATH/HOME/LANG/LC_ALL/TMPDIR and Lake LEAN_PATH are retained. Record '
    'only selected non-secret path/thread values and removed variable names.')
ENVIRONMENT_KEYS = ('PATH', 'LEAN_PATH', 'LEAN_NUM_THREADS')


def environment_override(name):
    return name.startswith(('LEAN', 'LAKE', 'LD_', 'DYLD_'))


def json_digest(value):
    data = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    return hashlib.sha256(data).hexdigest()


def build_environment(inherited, build):
    """Preserve Lake's dependency search path, stripping other tool overrides."""
    env = {k: v for k, v in inherited.items() if k in ('PATH', 'HOME', 'LANG', 'LC_ALL', 'TMPDIR', 'LEAN_PATH')}
    if not env.get('PATH'):
        raise RuntimeError('explicit nonempty launcher PATH required')
    inherited_lean_path = env.get('LEAN_PATH', '')
    removed = sorted(name for name in inherited
                     if environment_override(name) and name != 'LEAN_PATH')
    for name in removed:
        env.pop(name, None)
    env['LEAN_PATH'] = str(Path(build).resolve())
    if inherited_lean_path:
        env['LEAN_PATH'] += os.pathsep + inherited_lean_path
    env['LEAN_NUM_THREADS'] = '2'
    contract = {
        'policy': ENVIRONMENT_POLICY,
        'retained_lake_lean_path': inherited_lean_path,
        'removed_variable_names': removed,
        'selected_environment': {key: env[key] for key in ENVIRONMENT_KEYS},
    }
    contract['sha256'] = json_digest(contract)
    return env, contract


def resolve_lean_launcher(env):
    launcher = shutil.which('lean', path=env['PATH'])
    if launcher is None:
        raise RuntimeError('missing Lean launcher on declared PATH')
    return Path(launcher).resolve()


def phase_environment(env, contract):
    selected = {key: env.get(key) for key in ENVIRONMENT_KEYS}
    unexpected = sorted(name for name in env if environment_override(name)
                        and name not in ('LEAN_PATH', 'LEAN_NUM_THREADS'))
    measured = {'selected_environment': selected,
                'unexpected_override_names': unexpected}
    error = None
    if contract is not None:
        body = {key: value for key, value in contract.items() if key != 'sha256'}
        if (contract.get('policy') != ENVIRONMENT_POLICY
                or contract.get('sha256') != json_digest(body)
                or selected != contract.get('selected_environment')
                or selected['LEAN_NUM_THREADS'] != '2' or unexpected):
            error = 'phase environment differs from declared policy or selected values'
    return selected, json_digest(measured), unexpected, error


def run_phase(name, args, cwd, env, evidence, report, expected_success=True,
              timeout=PHASE_SECONDS, build_dir=None, build_module=None):
    """Persist raw streams, per-phase receipt, and aggregate receipt before raise."""
    if not re.fullmatch('[A-Za-z0-9_-]+', name):
        raise RuntimeError('unsafe phase name')
    evidence = Path(evidence)
    out_path, err_path = evidence / (name + '.stdout'), evidence / (name + '.stderr')
    start, utc_start = time.monotonic(), now()
    timed_out, spawn_error, code = False, None, None
    sampled_rss_peak_bytes, child_selected_env, process_reaped = 0, None, False
    objects_before, objects_after, object_error = None, None, None
    contract = report.get('environment_contract')
    selected_env, env_digest, override_names, env_error = phase_environment(env, contract)
    with out_path.open('xb') as stdout, err_path.open('xb') as stderr:
        try:
            if build_dir is not None:
                objects_before = object_inventory(build_dir)
        except (OSError, RuntimeError) as exc:
            object_error = str(exc)
        if object_error is None and env_error is None:
            try:
                proc = subprocess.Popen(args, cwd=cwd, env=env, stdout=stdout, stderr=stderr,
                                        start_new_session=True)
                try:
                    deadline = min(start + timeout, report.get('driver_deadline_monotonic', start + timeout))
                    while proc.poll() is None:
                        try:
                            status = Path(f'/proc/{proc.pid}/status').read_text()
                            match = re.search(r'^VmRSS:\s+(\d+) kB$', status, re.M)
                            if match:
                                sampled_rss_peak_bytes = max(sampled_rss_peak_bytes, int(match.group(1)) * 1024)
                            raw_env = Path(f'/proc/{proc.pid}/environ').read_bytes()
                            measured = dict(item.decode().split('=', 1) for item in raw_env.split(b'\0') if b'=' in item)
                            child_selected_env = {key: measured.get(key) for key in ENVIRONMENT_KEYS}
                            if child_selected_env != selected_env:
                                env_error = 'observed child environment differs from selected effective environment'
                                os.killpg(proc.pid, signal.SIGTERM)
                        except (OSError, UnicodeError, ValueError):
                            pass
                        if time.monotonic() >= deadline:
                            raise subprocess.TimeoutExpired(args, timeout)
                        time.sleep(0.25)
                    code = proc.wait()
                    process_reaped = True
                except subprocess.TimeoutExpired:
                    timed_out = True
                    try:
                        os.killpg(proc.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    try:
                        code = proc.wait(timeout=5)
                        process_reaped = True
                    except subprocess.TimeoutExpired:
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        code = proc.wait(timeout=5)
                        process_reaped = True
            except (OSError, subprocess.TimeoutExpired) as exc:
                spawn_error = str(exc)
            finally:
                # Reap of the direct child does not imply group cleanup.
                # Always KILL the original group after a timeout, including
                # when the parent exits on TERM. Detached sessions are outside
                # this process-group scope.
                if timed_out or env_error is not None:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
        if build_dir is not None:
            try:
                objects_after = object_inventory(build_dir)
                if object_error is None:
                    validate_objects(objects_before, objects_after, build_module)
            except (OSError, RuntimeError) as exc:
                object_error = str(exc)
    valid = (not timed_out and spawn_error is None and object_error is None and env_error is None and
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
              'selected_environment': selected_env,
              'environment_sha256': env_digest,
              'environment_contract_sha256': contract.get('sha256') if contract else None,
              'unexpected_override_names': override_names,
              'environment_validation_error': env_error,
              'observed_child_selected_environment': child_selected_env,
              'sampled_child_rss_peak_bytes': sampled_rss_peak_bytes,
              'sampled_rss_limit': 'Observation only; 250ms sampling, not a resident-memory enforcement guarantee.',
              'children_cumulative_maxrss_kib': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
              'process_reaped': process_reaped,
              'timeout_group_kill_policy': 'KILL original group after timeout or effective-environment abort; detached sessions not asserted.',
              'status': 'PASS' if valid else 'FAIL'}
    report['phase_results'].append(record)
    save_phase(evidence, report, record)
    print(f'ADAPTER {name}: exit={code} timeout={timed_out} seconds={record["duration_seconds"]}', flush=True)
    if not valid:
        raise RuntimeError(f'ADAPTER {name} unexpected exit: {code}; timed_out={timed_out}; '
                           f'spawn_error={spawn_error}; object_error={object_error}; environment_error={env_error}')
    output = out_path.read_bytes().decode('utf8', 'replace') + '\n' + err_path.read_bytes().decode('utf8', 'replace')
    return record, output, code


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True, timeout=30).strip()

def validate_publication_changes(changed):
    if not changed:
        raise RuntimeError('empty publication diff')
    for line in changed:
        fields = line.split('\t', 1)
        if len(fields) != 2:
            raise RuntimeError('invalid git name-status tab record')
        status, rel = fields
        if status != 'A' or not (rel.startswith(PREFIX + '/') or rel == WORKFLOW):
            raise RuntimeError('publication changes a foreign or preexisting source')

def validate_push_event(event, head):
    if (event.get('before') != EXPECTED_BASE or event.get('after') != head
            or event.get('created') is not False or event.get('deleted') is not False
            or event.get('forced') is not False
            or event.get('ref') != 'refs/heads/' + EXPECTED_BRANCH):
        raise RuntimeError('exact normal existing-branch base-to-leaf push required')


def verify_packages(root):
    result = {}
    for name, expected in PACKAGE_PINS.items():
        path = root / 'formal/.lake/packages' / name
        actual = git(path, 'rev-parse', 'HEAD')
        if actual != expected or git(path, 'status', '--porcelain', '--untracked-files=no'):
            raise RuntimeError(f'installed dependency mismatch or tracked change: {name}')
        result[name] = actual
    return result

def dependency_artifact_inventory(root, env, prefix, deadline):
    """Full byte inventory at two boundaries; cost is inside the driver budget."""
    roots = [Path(s).resolve() for s in env['LEAN_PATH'].split(os.pathsep) if s]
    local = (root / '.lake/quo-closed-superlevel-hosted-evidence/objects').resolve()
    roots = [p for p in roots if p != local]
    roots.append((prefix / 'lib/lean').resolve())
    roots += [(root / 'formal/.lake/packages' / name).resolve() for name in PACKAGE_PINS]
    result = {}
    for directory in dict.fromkeys(roots):
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob('*')):
            if time.monotonic() > deadline:
                raise RuntimeError('dependency custody exceeded whole driver deadline')
            if not path.is_file() or '.git' in path.parts:
                continue
            if not path.name.endswith(('.lean', '.olean', '.olean.private', '.olean.server', '.ir', '.so', '.a')):
                continue
            if path.is_symlink():
                raise RuntimeError('unqualified symlink dependency artifact: ' + str(path))
            result[str(path)] = identity(path)
    if not result:
        raise RuntimeError('empty dependency artifact inventory')
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
    context['executor'] = 'GitHub-hosted runner executing unqualified adapter collector candidate'
    if os.environ['GITHUB_EVENT_NAME'] != 'push' or os.environ['GITHUB_RUN_ATTEMPT'] != '1':
        raise RuntimeError('only first-attempt push route allowed')
    if os.environ.get('GITHUB_REF') != 'refs/heads/' + EXPECTED_BRANCH:
        raise RuntimeError('wrong exact owned branch')
    if context['tested_parents'] != [EXPECTED_BASE]:
        raise RuntimeError('fresh one-parent leaf must preserve exact admitted base')
    if not event_path.is_file():
        raise RuntimeError('actual push event file required')
    event = json.loads(event_path.read_text())
    validate_push_event(event, head)
    changed = git(root, 'diff', '--name-status', EXPECTED_BASE, head).splitlines()
    validate_publication_changes(changed)
    context['human_review_credit'] = 0
    return context


def source_only(root, digest):
    evidence = root / '.lake/quo-closed-superlevel-hosted-evidence'
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
    evidence = root / '.lake/quo-closed-superlevel-hosted-evidence'
    report = json.loads((evidence / 'RESULT.json').read_text())
    if report['status'] != 'PASS_SOURCE_PREFLIGHT_ONLY' or report['phase_results']:
        raise RuntimeError('exact unused source preflight required; no automatic retry')
    build = evidence / 'objects'
    build.mkdir(exist_ok=False)
    report.update(status='HOLD_NOT_COMPLETED', started_execution_at=now(),
                  memory_limit='-M14000', threads=2, phase_timeout_seconds=PHASE_SECONDS,
                  driver_deadline_monotonic=time.monotonic() + DRIVER_SECONDS,
                  actual_memory_observation=Path('/proc/meminfo').read_text() if Path('/proc/meminfo').is_file() else None,
                  memory_enforcement_limit='Lean internal -M14000 only; no hard RSS limit is claimed.',
                  memory_limit_reason='Explicit Linux execution budget; not a claim that ADAPTER requires this amount.',
                  verification_scope='Eight fresh local objects; one standard named-module adapter replay; four exact target axiom reports; one explicit Euclidean-LPC omission control.',
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
        env, report['environment_contract'] = build_environment(os.environ, build)
        save_report(evidence, report)
        launcher = resolve_lean_launcher(env)
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
        report['dependency_artifacts_before'] = dependency_artifact_inventory(
            root, env, prefix, report['driver_deadline_monotonic'])
        save_report(evidence, report)
        report['machine'] = {'platform': platform.platform(), 'machine': platform.machine(),
                             'python': platform.python_version()}
        _, version, _ = run_phase('runtime-version', [runtimes['lean']['path'], '--version'],
                                  formal, env, evidence, report, timeout=30)
        if 'version ' + LEAN_VERSION not in version:
            raise RuntimeError('wrong Lean runtime version')
        report['lean_version_output'] = version
        for module in MODULES:
            args = [runtimes['lean']['path'], '-j2', '-M14000']
            if module in ('CriticalLevelAttainment', 'QuoClosedSuperlevelAdapter', 'QuoClosedSuperlevelAudit'):
                args += ['-DwarningAsError=true']
            args += ['-o', str(build / (module + '.olean')),
                     str(packet / 'project' / (module + '.lean'))]
            rec, output, _ = run_phase('build-' + module, args, packet / 'project', env, evidence, report,
                                       build_dir=build, build_module=module)
            obj = build / (module + '.olean')
            safe_source(obj, evidence)
            rec['object'] = identity(obj)
            if module == 'QuoClosedSuperlevelAudit':
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
        report['dependency_artifacts_after'] = dependency_artifact_inventory(
            root, env, prefix, report['driver_deadline_monotonic'])
        if report['dependency_artifacts_after'] != report['dependency_artifacts_before']:
            raise RuntimeError('imported dependency source/artifact byte inventory changed')
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
            raise RuntimeError('ADAPTER negative diagnostics require source-bound review: '
                               + repr(report['negative_classification_errors']))
        require_final_predicates()
        report['status'] = 'PASS_HOSTED_ADAPTER_EXACT_TARGETS'
        report['completed_at'] = now()
        print('ADAPTER_HOSTED_FORMAL_PASS: scoped formal execution only; scientific effect NONE.', flush=True)
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
    # Published location is exactly frontiers/<packet>/quo_hosted_verify.py.
    root = Path(__file__).resolve().parents[2]
    if args.mode == 'source':
        source_only(root, args.manifest_sha256)
    else:
        execute(root, args.manifest_sha256)


if __name__ == '__main__':
    main()
