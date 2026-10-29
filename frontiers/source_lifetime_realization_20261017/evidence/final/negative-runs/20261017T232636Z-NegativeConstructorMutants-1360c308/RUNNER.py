"""Bounded C291 source-mutation controls; execute only after parent slot authorization.

Uses the common serial lock. Production inputs and imported objects are read-only.
The wrapper succeeds only when the exact intended positive/rejection outcome occurs.
"""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CACHE = Path('@PINNED_DEPENDENCY_CACHE@')
BIN = Path('@PINNED_LEAN_RUNTIME@/bin')
MODULES = {'NegativeFixtureBaseline', 'NegativeConstructorMutants',
           'NegativeUnusedAxiom', 'NegativeUnusedAxiomAudit'}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def objects(path):
    return {p.name: sha(p) for p in sorted(path.iterdir()) if p.is_file() and
            ('.olean' in p.name or p.name.endswith(('.ir', '.ir.sig')))}


def production_sources():
    return {p.name: sha(p) for p in sorted((ROOT / 'project').glob('*.lean'))}


def known_success(module, generation):
    for p in sorted((ROOT / 'negative-runs').glob('*/RECEIPT.json')):
        v = json.loads(p.read_text())
        if v.get('module') == module and v.get('generation') == generation and v.get('control_pass'):
            return v
    return None


def main():
    require(len(sys.argv) == 3, 'usage: run_negative.py GENERATION MODULE')
    generation, module = sys.argv[1:]
    require(re.fullmatch('[0-9a-f]{16}', generation) is not None, 'invalid generation')
    require(module in MODULES, 'unknown fixture module')
    project = HERE / 'generations' / generation
    manifest_path = project / 'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    source = project / (module + '.lean')
    require(sha(source) == manifest['modules'][module]['sha256'], 'fixture bytes changed')
    require(sha(BIN / 'lean') == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554', 'Lean binary changed')
    dependency_manifest = CACHE / 'lake-manifest.json'
    require(sha(dependency_manifest) == 'd63753befccc21923783a5085148e3ff028d97134ea52f5a08bd87ecf1b0b043', 'dependency manifest changed')
    build = project / 'build'
    paths = [str(build), str(ROOT / 'build')]
    dependency_roots = []
    for dep in json.loads(dependency_manifest.read_text())['packages']:
        d = CACHE / '.lake/packages' / dep['name']
        require((d / '.git/HEAD').read_text().strip() == dep['rev'], 'dependency revision changed')
        b = d / '.lake/build/lib/lean'
        if b.is_dir():
            paths.append(str(b))
            dependency_roots.append(b)
    env = os.environ.copy()
    env['LEAN_PATH'] = os.pathsep.join(paths)
    env['LEAN_NUM_THREADS'] = '2'
    (ROOT / 'negative-runs').mkdir(exist_ok=True)
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        print(json.dumps({'stage': 'WAITING_FOR_C291_SERIAL_SLOT', 'module': module}), flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        require(sha(ROOT / manifest['baseline_source_path']) == manifest['baseline_source_sha256'], 'production field differs from fixture source')
        require(sha(ROOT / manifest['baseline_audit_path']) == manifest['baseline_audit_sha256'], 'production audit differs from fixture source')
        before_sources = production_sources()
        before_objects = objects(ROOT / 'build')
        baseline_receipts = {}
        required = ['SourceThetaBridge', 'SourceLifetimeGeometry', 'SourceLifetimeField',
                    'SourceLifetimeControls', 'SourceLifetimeAxiomAudit']
        for name in required:
            for receipt_path in sorted((ROOT / 'runs').glob('*/RECEIPT.json')):
                v = json.loads(receipt_path.read_text())
                if (v.get('source') == name + '.lean' and v.get('returncode') == 0 and
                    not v.get('timed_out') and v.get('source_unchanged') and
                    v.get('source_sha256') == before_sources[name + '.lean'] and
                    v.get('output_sha256') == before_objects[name + '.olean']):
                    baseline_receipts[name] = str(receipt_path.relative_to(ROOT))
            require(name in baseline_receipts, 'missing exact positive development receipt: ' + name)
        positive_acceptance = None
        if module == 'NegativeConstructorMutants':
            positive = known_success('NegativeFixtureBaseline', generation)
            if not positive:
                acceptance_path = ROOT / 'negative-runs' / ('positive-acceptance-' + generation) / 'TWO_PART_ACCEPTANCE.json'
                acceptance = json.loads(acceptance_path.read_text())
                require(acceptance['status'] == 'PASS' and acceptance['generation'] == generation,
                        'missing two-part positive acceptance')
                require(sha(ROOT / acceptance['positive_baseline_receipt']) == acceptance['positive_baseline_receipt_sha256'],
                        'original baseline receipt changed')
                require(sha(ROOT / acceptance['binding_probe_receipt']) == acceptance['binding_probe_receipt_sha256'],
                        'binding probe receipt changed')
                require(acceptance['baseline_source_sha256'] == manifest['modules']['NegativeFixtureBaseline']['sha256'],
                        'two-part baseline source mismatch')
                require(all(objects(build).get(n) == h for n, h in acceptance['baseline_objects'].items()),
                        'two-part baseline objects changed')
                probe_receipt = json.loads((ROOT / acceptance['binding_probe_receipt']).read_text())
                require(probe_receipt['control_pass'] and probe_receipt['returncode'] == 0 and
                        not probe_receipt['timed_out'] and acceptance['bindings_verified'] == 21,
                        'binding probe did not actually pass')
                positive_acceptance = {'path': str(acceptance_path.relative_to(ROOT)), 'sha256': sha(acceptance_path)}
        if module == 'NegativeUnusedAxiomAudit':
            require(known_success('NegativeUnusedAxiom', generation), 'unused-axiom carrier must compile first')
        dependency_stats = {str(p): (p.stat().st_size, p.stat().st_mtime_ns, p.stat().st_ino)
                            for d in dependency_roots for p in d.rglob('*') if p.is_file()}
        fixture_before = {n: sha(project / (n + '.lean')) for n in MODULES}
        own_objects_before = objects(build)
        timeout_seconds = 420 if module == 'NegativeUnusedAxiomAudit' else 240
        command = [str(BIN / 'lean'), '-j2', '-M4096']
        if module != 'NegativeConstructorMutants':
            command.append('-DwarningAsError=true')
        command += ['-o', str(build / (module + '.olean')), str(source)]
        run = ROOT / 'negative-runs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + module + '-' + uuid.uuid4().hex[:8])
        run.mkdir()
        (run / 'RUNNER.py').write_bytes(Path(__file__).read_bytes())
        receipt = {
            'generation': generation, 'module': module, 'command': command,
            'started_utc': now(), 'manifest_sha256': sha(manifest_path),
            'fixture_before': fixture_before, 'production_sources_before': before_sources,
            'production_objects_before': before_objects, 'own_objects_before': own_objects_before,
            'baseline_development_receipts': baseline_receipts, 'lean_path': paths,
            'two_part_positive_acceptance': positive_acceptance,
            'runner_sha256': sha(Path(__file__)), 'executable_sha256': sha(BIN / 'lean'),
            'dependency_file_metadata_count': len(dependency_stats),
            'timeout_seconds': timeout_seconds, 'threads': 2, 'scientific_effect': 'NONE',
            'scope': 'Development source-bound mutation controls; fresh source closure and kernel replay remain separately parent-owned',
        }
        start = time.monotonic()
        with (run / 'stdout.txt').open('wb') as stdout, (run / 'stderr.txt').open('wb') as stderr:
            child = subprocess.Popen(command, cwd=project, env=env, stdout=stdout,
                stderr=stderr, start_new_session=True)
            receipt['child_pid'] = child.pid
            (run / 'START.json').write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps({'stage': 'RUNNING', 'module': module, 'child_pid': child.pid, 'run': str(run)}), flush=True)
            timeout = False
            try:
                code = child.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                timeout = True
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    code = child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    code = child.wait()
        output = (run / 'stdout.txt').read_text()
        errors = [{'line': int(m.group(1)), 'column': int(m.group(2)), 'message': m.group(3)}
                  for m in re.finditer(r'^.+\.lean:(\d+):(\d+): error(?:\([^)]*\))?: (.*)$', output, re.M)]
        stderr_text = (run / 'stderr.txt').read_text()
        expected_stderr = (not stderr_text) or (module == 'NegativeUnusedAxiomAudit' and all(
            re.fullmatch(r'LIFETIME_AUDIT_PROGRESS (?:START|[A-Za-z0-9_.]+ COUNT [0-9]+)', line)
            for line in stderr_text.splitlines()))
        checks = {'not_timed_out': not timeout,
                  'stderr_empty_or_exact_audit_progress': expected_stderr,
                  'manifest_unchanged': sha(manifest_path) == receipt['manifest_sha256'],
                  'production_sources_unchanged': production_sources() == before_sources,
                  'production_objects_unchanged': objects(ROOT / 'build') == before_objects,
                  'own_imported_objects_unchanged': all(objects(build).get(n) == h
                      for n, h in own_objects_before.items() if not n.startswith(module + '.')),
                  'fixtures_unchanged': {n: sha(project / (n + '.lean')) for n in MODULES} == fixture_before,
                  'no_import_or_unknown_identifier_failure': not bool(re.search(
                      r'unknown (?:identifier|constant|module)|object file .+ does not exist|failed to import',
                      output + (run / 'stderr.txt').read_text(), re.I)),
                  'dependency_metadata_unchanged': all(Path(p).is_file() and
                      (Path(p).stat().st_size, Path(p).stat().st_mtime_ns, Path(p).stat().st_ino) == stat
                      for p, stat in dependency_stats.items())}
        if module == 'NegativeFixtureBaseline':
            checks['compiler_success'] = code == 0
            checks['no_errors'] = not errors
            for case in manifest['constructor_cases']:
                for suffix in manifest['positive_binding_required_local_suffixes']:
                    checks['local_binding:' + case['name'] + ':' + suffix] = case['namespace'] + '.' + suffix in output
        elif module == 'NegativeConstructorMutants':
            checks['compiler_rejected'] = code == 1
            for case in manifest['constructor_cases']:
                lo, hi = case['required_error_line_range']
                checks['intended_range_rejection:' + case['name']] = any(lo <= e['line'] <= hi for e in errors)
            checks['no_errors_outside_mutant_namespaces'] = all(any(
                c['combined_namespace_range'][0] <= e['line'] <= c['combined_namespace_range'][1]
                for c in manifest['constructor_cases']) for e in errors)
        elif module == 'NegativeUnusedAxiom':
            checks['compiler_success'] = code == 0
            checks['no_errors'] = not errors
            checks['axiom_is_private_and_unused'] = source.read_text().count('c291UnusedCustomAxiom') == 1 and 'private axiom c291UnusedCustomAxiom : False' in source.read_text()
        else:
            checks['compiler_rejected'] = code == 1
            checks['whole_module_private_axiom_rejection'] = (
                'LIFETIME_AUDIT_MODULE NegativeUnusedAxiom COUNT' in output and
                any('forbidden transitive axiom' in e['message'] and
                    'c291UnusedCustomAxiom' in e['message'] and '_private.' in e['message'] for e in errors))
            checks['no_false_success_marker'] = 'LIFETIME_AUDIT_STANDARD_ONLY_PASS' not in output
        passed = all(checks.values())
        receipt.update(returncode=code, timed_out=timeout, ended_utc=now(),
            seconds=time.monotonic()-start, errors=errors, checks=checks, control_pass=passed,
            stdout_sha256=sha(run / 'stdout.txt'), stderr_sha256=sha(run / 'stderr.txt'),
            production_sources_after=production_sources(), production_objects_after=objects(ROOT / 'build'),
            own_objects_after=objects(build))
        (run / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({'stage': 'FINISHED', 'module': module, 'returncode': code,
            'timed_out': timeout, 'control_pass': passed, 'failed_checks': [k for k,v in checks.items() if not v],
            'seconds': receipt['seconds'], 'errors': errors, 'run': str(run)}), flush=True)
        return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
