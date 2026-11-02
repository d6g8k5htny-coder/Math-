"""C291 audit-only recovery of an observed final 420-second timeout.

Adapted from run_lean.py and the existing owner's finish_serial_checks.py.
Shares the development runner's serial lock; never writes a dependency cache.
Requires final-project and FINAL_SOURCE_INVENTORY.json prepared by the parent.
"""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT / 'final-project'
BUILD = ROOT / 'final-build'
CACHE = Path('@PINNED_DEPENDENCY_CACHE@')
BIN = Path('@PINNED_LEAN_RUNTIME@/bin')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def object_map():
    return {p.name: sha(p) for p in sorted(BUILD.iterdir())
            if p.is_file() and ('.olean' in p.name or p.name.endswith(('.ir', '.ir.sig')))}


def is_module_object(name, module):
    return name in {module + s for s in ['.olean', '.olean.private', '.olean.server', '.ir', '.ir.sig']}


def dependency_paths(roots):
    return sorted({p for root in roots for p in Path(root).rglob('*')
                   if p.is_file() and ('.olean' in p.name or '.so' in p.name or
                     p.name.endswith(('.ir', '.ir.sig', '.dylib', '.dll')))})


def dependency_metadata_unchanged(artifacts, roots):
    require([str(p) for p in dependency_paths(roots)] == [v['path'] for v in artifacts],
            'dependency artifact path set changed')
    for item in artifacts:
        path = Path(item['path'])
        stat = path.stat()
        require(not path.is_symlink(), 'dependency object became a symlink')
        require([stat.st_size, stat.st_mtime_ns, stat.st_ino] == item['stat'],
                'dependency artifact metadata changed: ' + str(path))


def main():
    require(len(sys.argv) == 3, 'usage: run_final_phase.py build|kernel Module')
    kind, module = sys.argv[1:]
    require((kind, module) == ('build', 'SourceLifetimeAxiomAudit'), 'recovery is audit-only')
    require(module.isidentifier(), 'expected simple module basename')
    inventory_path = ROOT / 'FINAL_SOURCE_INVENTORY.json'
    inventory = json.loads(inventory_path.read_text())
    inventory_sha = sha(inventory_path)
    dependency_inventory_path = ROOT / 'FINAL_DEPENDENCY_ARTIFACTS.json'
    require(sha(dependency_inventory_path) == inventory['dependency_artifact_inventory_sha256'],
            'dependency artifact inventory changed')
    dependency_inventory = json.loads(dependency_inventory_path.read_text())
    dependency_artifacts = dependency_inventory['artifacts']
    dependency_roots = dependency_inventory['roots']
    expected = {v['name']: v['sha256'] for v in inventory['sources']}
    require(module + '.lean' in expected, 'module not in frozen source inventory')
    require(PROJECT.is_dir() and BUILD.is_dir(), 'final isolated directories missing')
    require(not PROJECT.is_symlink() and not BUILD.is_symlink(), 'symlink final directories')
    require(sha(BIN / 'lean') == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554', 'Lean identity changed')
    require(sha(BIN / 'leanchecker') == 'cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35', 'kernel checker identity changed')
    manifest = CACHE / 'lake-manifest.json'
    require(sha(manifest) == 'd63753befccc21923783a5085148e3ff028d97134ea52f5a08bd87ecf1b0b043', 'dependency manifest changed')
    paths = [str(BUILD)]
    for dep in json.loads(manifest.read_text())['packages']:
        p = CACHE / '.lake/packages' / dep['name']
        require((p / '.git/HEAD').read_text().strip() == dep['rev'], 'dependency pin changed: ' + dep['name'])
        b = p / '.lake/build/lib/lean'
        if b.is_dir():
            paths.append(str(b))
    env = os.environ.copy()
    env['LEAN_PATH'] = os.pathsep.join(paths)
    env['LEAN_NUM_THREADS'] = '2'
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        print(json.dumps({'stage': 'WAITING_FOR_C291_SERIAL_SLOT', 'kind': kind, 'module': module}), flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        before = {n: sha(PROJECT / n) for n in expected}
        require(before == expected, 'frozen source changed before execution')
        objects_before = object_map()
        require(not any(is_module_object(n, module) for n in objects_before), 'audit output already exists')
        failed = json.loads((ROOT / 'FINAL_SEQUENCE_RESULT.json').read_text())
        require(failed['status'] == 'HOLD_FAILED_PHASE' and len(failed['phases']) == 19, 'original failure absent')
        successful_builds = {}
        for p in sorted((ROOT / 'final-runs').glob('*/RECEIPT.json')):
            v = json.loads(p.read_text())
            if (v.get('kind') == 'build' and v.get('returncode') == 0 and
                    not v.get('timed_out') and v.get('source_unchanged') and
                    v.get('imported_objects_unchanged') and not v.get('integrity_error') and
                    v.get('object_sha256') and
                    v.get('inventory_sha256') == inventory_sha):
                successful_builds.update(v['produced_objects'])
        for name, digest in objects_before.items():
            require(successful_builds.get(name) == digest,
                    'existing final object lacks this-source successful rebuild receipt: ' + name)
        dependency_metadata_unchanged(dependency_artifacts, dependency_roots)
        out = BUILD / (module + '.olean')
        if kind == 'build':
            command = [str(BIN / 'lean'), '-j2', '-M4096']
            if module in inventory['new_modules']:
                command.append('-DwarningAsError=true')
            command += ['-o', str(out), str(PROJECT / (module + '.lean'))]
        else:
            require(out.is_file(), 'kernel replay requires actual final object')
            command = [str(BIN / 'leanchecker'), '-v', module]
        run = ROOT / 'final-runs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + kind + '-' + module + '-' + uuid.uuid4().hex[:8])
        run.mkdir(parents=True)
        receipt = {'kind': kind, 'module': module, 'command': command, 'started_utc': now(),
                   'source_before': before, 'inventory_sha256': inventory_sha,
                   'objects_before': objects_before, 'lean_path': paths,
                   'dependency_artifact_inventory_sha256': sha(dependency_inventory_path),
                   'dependency_artifact_count': len(dependency_artifacts),
                   'dependency_check': 'initial full byte hashes; stat/size/inode checks each phase; final full byte rehash required',
                   'executable_sha256': sha(Path(command[0])), 'runner_sha256': sha(Path(__file__)),
                   'timeout_seconds': 900, 'threads': 2,
                   'kernel_scope': 'standard named-module replay against imports; not --fresh or an external verifier',
                   'scientific_effect': 'NONE'}
        start = time.monotonic()
        with (run / 'stdout.txt').open('wb') as stdout, (run / 'stderr.txt').open('wb') as stderr:
            proc = subprocess.Popen(command, cwd=PROJECT, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
            receipt['child_pid'] = proc.pid
            (run / 'START.json').write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps({'stage': 'RUNNING', 'kind': kind, 'module': module, 'child_pid': proc.pid, 'run': str(run)}), flush=True)
            timed_out = False
            try:
                code = proc.wait(timeout=900)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    code = proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    code = proc.wait()
        integrity_error = None
        after = {}
        objects_after = {}
        imported_unchanged = False
        try:
            after = {n: sha(PROJECT / n) for n in expected}
            objects_after = object_map()
            expected_existing = dict(objects_before)
            expected_names = set(objects_before)
            if kind == 'build':
                expected_existing = {n: h for n, h in expected_existing.items()
                                     if not is_module_object(n, module)}
                if code == 0:
                    expected_names = set(expected_existing) | {
                        n for n in objects_after if is_module_object(n, module)}
            imported_unchanged = (set(objects_after) == expected_names and
                all(objects_after.get(n) == h for n, h in expected_existing.items()))
            dependency_metadata_unchanged(dependency_artifacts, dependency_roots)
        except Exception as exc:
            integrity_error = repr(exc)
        receipt.update(returncode=code, timed_out=timed_out, ended_utc=now(),
                       seconds=time.monotonic() - start, source_after=after,
                       source_unchanged=before == after, objects_after=objects_after,
                       imported_objects_unchanged=imported_unchanged,
                       integrity_error=integrity_error)
        for stream in ['stdout', 'stderr']:
            receipt[stream + '_sha256'] = sha(run / (stream + '.txt'))
        good = code == 0 and not timed_out and before == after and imported_unchanged and integrity_error is None
        if good:
            receipt['object_sha256'] = sha(out)
            receipt['produced_objects'] = {n: h for n, h in objects_after.items()
                                           if is_module_object(n, module)}
        (run / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({'stage': 'FINISHED', 'kind': kind, 'module': module, 'returncode': code,
                          'timed_out': timed_out, 'seconds': receipt['seconds'],
                          'source_unchanged': before == after, 'run': str(run)}), flush=True)
        return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
