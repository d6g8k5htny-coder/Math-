"""C294 serial isolated build / standard named-module kernel replay (not --fresh)."""
from pathlib import Path
from datetime import datetime, timezone
import fcntl, hashlib, json, os, signal, stat, subprocess, sys, time, uuid

ROOT = Path(__file__).resolve().parent
PROJECT, BUILD = ROOT / 'final-project', ROOT / 'final-build'
C291 = ROOT.parent / 'continuation291'
CACHE = Path('$PINNED_PROJECT')
BIN = Path('$LEAN_RUNTIME/bin')
MODULES = ['Lifetime', 'TorusTopology', 'SuperlevelBar', 'ClosedSuperlevel', 'MorseFiniteCritical', 'CriticalLevelAttainment', 'CriticalLevelAxiomAudit']
NEW = MODULES[5:]
BASE_SHA = 'b78b6e0f99bd38c633ae2677c55698363b1290e6d4318e505991c8df259ae2e3'
MANIFEST_SHA = 'd63753befccc21923783a5085148e3ff028d97134ea52f5a08bd87ecf1b0b043'
EXE_SHA = {'lean': '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554',
           'leanchecker': 'cfde41cb11dde58c84e9c60c551fd104bb2fc1104ad44dca932a923120272a35'}
# C294 immutable Lifetime development load hit240s with empty diagnostics.
# Set a bounded600s final phase cap before freezing; no thread/memory expansion.
TIMEOUT = 600


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def stamp(p):
    s = p.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'nonregular/hardlinked file: ' + str(p))
    return [s.st_size, s.st_mtime_ns, s.st_ino]


def write(p, data):
    with p.open('x') as f:
        f.write(json.dumps(data, indent=2) + '\n')


def dependency_paths(roots):
    paths = []
    for root in map(Path, roots):
        require(root.is_dir() and all(not p.is_symlink() for p in [root, *root.parents]), 'unsafe dependency root')
        for p in root.rglob('*'):
            require(not p.is_symlink(), 'dependency symlink: ' + str(p))
            if p.is_file() and ('.olean' in p.name or '.so' in p.name or p.name.endswith(('.ir', '.ir.sig', '.dylib', '.dll'))):
                paths.append(str(p))
    return sorted(set(paths))


def dependencies(baseline):
    """Reuse bytes only at identical size/mtime_ns/inode; hash metadata deltas."""
    rows = baseline['artifacts']
    expected_paths = sorted(v['path'] for v in rows)
    require(len(expected_paths) == len(set(expected_paths)), 'duplicate baseline dependency path')
    require(dependency_paths(baseline['roots']) == expected_paths, 'dependency pathset changed')
    result, delta = [], []
    for row in rows:
        p = Path(row['path']); before = stamp(p)
        if before != row['stat']:
            digest = sha(p)
            require(stamp(p) == before, 'dependency changed while hashing: ' + str(p))
            delta.append({'path': str(p), 'old_stat': row['stat'], 'stat': before, 'sha256': digest})
            require(digest == row['sha256'], 'dependency bytes changed: ' + str(p))
        result.append(dict(row, stat=before))
    require(dependency_paths(baseline['roots']) == expected_paths, 'dependency pathset changed during check')
    return dict(baseline, artifacts=result), {'reused': len(rows) - len(delta), 'rehashed': delta,
        'mode': 'C291 byte hashes plus unchanged metadata reuse; changed metadata rehashed; NOT full fresh byte rehash'}


def runtime():
    for name, digest in EXE_SHA.items():
        stamp(BIN / name); require(sha(BIN / name) == digest, 'executable identity: ' + name)
    manifest = CACHE / 'lake-manifest.json'
    manifest_raw = manifest.read_bytes()
    require(hashlib.sha256(manifest_raw).hexdigest() == MANIFEST_SHA, 'manifest identity changed')
    roots, paths = [str(BIN.parent / 'lib/lean')], [str(BUILD)]
    for dep in json.loads(manifest_raw)['packages']:
        p = CACHE / '.lake/packages' / dep['name']
        require((p / '.git/HEAD').read_text().strip() == dep['rev'], 'dependency revision: ' + dep['name'])
        root = p / '.lake/build/lib'
        # Match C291: every package revision is pinned, but Cli has no compiled lib.
        if root.is_dir():
            roots.append(str(root))
        if (root / 'lean').is_dir():
            paths.append(str(root / 'lean'))
    return roots, paths


def source_map():
    require(PROJECT.is_dir() and not PROJECT.is_symlink(), 'final project missing/unsafe')
    require({p.name for p in PROJECT.iterdir()} == {m + '.lean' for m in MODULES}, 'final source pathset changed')
    return {p.name: sha(p) for p in sorted(PROJECT.iterdir()) if stamp(p)}


def objects():
    require(BUILD.is_dir() and not BUILD.is_symlink(), 'final build missing/unsafe')
    result = {}
    for p in sorted(BUILD.iterdir()):
        stamp(p)
        require(any(is_object(p.name, m) for m in MODULES), 'unexpected final build path: ' + p.name)
        result[p.name] = sha(p)
    return result


def is_object(name, module):
    return name in {module + s for s in ('.olean', '.olean.private', '.olean.server', '.ir', '.ir.sig')}


def main():
    require(len(sys.argv) == 3 and sys.argv[1] in ('build', 'kernel') and sys.argv[2] in MODULES,
            'usage: run_final_phase.py build|kernel Module')
    kind, module = sys.argv[1:]
    # Prior C293 audit exceeded its development 240s cap; C291 required458.5s.
    # Reuse the final900s audit allowance, not an assertion of a C294 failure.
    timeout = 900 if kind == 'build' and module == 'CriticalLevelAxiomAudit' else TIMEOUT
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        run = ROOT / 'final-runs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + kind + '-' + module + '-' + uuid.uuid4().hex[:8])
        run.mkdir(parents=True); (run / 'tmp').mkdir()
        receipt = {'kind': kind, 'module': module, 'started_utc': now(), 'runner_sha256': sha(Path(__file__)),
                   'kernel_scope': 'standard named-module replay against imported dependencies; not --fresh/external verification',
                   'scientific_effect': 'NONE', 'timeout_seconds': timeout, 'threads': 2, 'status': 'PREFLIGHT'}
        write(run / 'START.json', receipt)
        good = False; proc = None; start = time.monotonic()
        try:
            inv_path = ROOT / 'FINAL_SOURCE_INVENTORY.json'; inv_raw = inv_path.read_bytes()
            inv_hash = hashlib.sha256(inv_raw).hexdigest(); inv = json.loads(inv_raw)
            require(inv['runner_sha256'] == receipt['runner_sha256'], 'runner changed after freeze')
            dep_path = ROOT / 'FINAL_DEPENDENCY_ARTIFACTS.json'
            dep_raw = dep_path.read_bytes()
            require(hashlib.sha256(dep_raw).hexdigest() == inv['dependency_artifact_inventory_sha256'], 'dependency inventory changed')
            baseline = json.loads(dep_raw); roots, paths = runtime()
            require(roots == baseline['roots'], 'dependency roots changed')
            _, dep_before = dependencies(baseline)
            before = source_map(); expected = {v['name']: v['sha256'] for v in inv['sources']}
            require(before == expected, 'frozen sources changed')
            prior = objects(); known = {}
            for p in sorted((ROOT / 'final-runs').glob('*/RECEIPT.json')):
                v = json.loads(p.read_text())
                if v.get('kind') == 'build' and v.get('status') == 'PASS' and v.get('inventory_sha256') == inv_hash:
                    known.update(v['produced_objects'])
            require(all(known.get(n) == h for n, h in prior.items()), 'object lacks same-freeze successful build receipt')
            require(all(m + '.olean' in prior for m in inv['local_imports'][module]), 'local imports not built')
            out = BUILD / (module + '.olean')
            require(kind != 'kernel' or out.is_file(), 'kernel requires final object')
            require(kind != 'build' or not any(is_object(n, module) for n in prior), 'module already has outputs; no implicit retry')
            command = ([str(BIN / 'lean'), '-j2', '-M4096'] + (['-DwarningAsError=true'] if module in NEW else []) +
                       ['-o', str(out), str(PROJECT / (module + '.lean'))]) if kind == 'build' else [str(BIN / 'leanchecker'), '-v', module]
            env = {k: v for k, v in os.environ.items() if not k.startswith(('LEAN', 'LAKE', 'LD_', 'DYLD_'))}
            env.update(PATH=os.pathsep.join([str(BIN), '/usr/bin', '/bin', '/usr/sbin', '/sbin']),
                       LEAN_PATH=os.pathsep.join(paths), LEAN_NUM_THREADS='2', TMPDIR=str(run / 'tmp'))
            receipt.update(inventory_sha256=inv_hash, source_before=before, objects_before=prior,
                           dependency_before=dep_before, command=command, process_path=env['PATH'], lean_path=paths,
                           executable_sha256=sha(Path(command[0])), resolved_lean_sha256=sha(BIN / 'lean'))
            write(run / 'PREFLIGHT.json', receipt)
            with (run / 'stdout.txt').open('xb') as stdout, (run / 'stderr.txt').open('xb') as stderr:
                proc = subprocess.Popen(command, cwd=PROJECT, env=env, stdout=stdout, stderr=stderr, start_new_session=True)
                receipt['child_pid'] = proc.pid; write(run / 'PROCESS_START.json', receipt)
                timed_out = False
                try:
                    code = proc.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    timed_out = True; os.killpg(proc.pid, signal.SIGTERM)
                    try:
                        code = proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        os.killpg(proc.pid, signal.SIGKILL); code = proc.wait()
            receipt.update(returncode=code, timed_out=timed_out)
            after, current = source_map(), objects()
            unchanged = all(current.get(n) == h for n, h in prior.items())
            allowed = set(prior) | ({n for n in current if is_object(n, module)} if kind == 'build' else set())
            _, dep_after = dependencies(baseline)
            receipt.update(source_after=after, objects_after=current, dependency_after=dep_after,
                           source_unchanged=after == before, imported_objects_unchanged=unchanged and set(current) == allowed)
            require(sha(inv_path) == inv_hash and sha(dep_path) == inv['dependency_artifact_inventory_sha256'], 'inventory changed during phase')
            good = code == 0 and not timed_out and after == before and unchanged and set(current) == allowed and out.is_file()
            if good:
                receipt['object_sha256'] = sha(out)
                receipt['produced_objects'] = {n: h for n, h in current.items() if is_object(n, module)}
        except Exception as exc:
            receipt['integrity_or_execution_error'] = repr(exc)
        finally:
            if proc is not None and proc.poll() is None:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    proc.wait(timeout=5)
                    receipt['emergency_child_cleanup'] = True
                except subprocess.TimeoutExpired:
                    receipt['cleanup_error'] = 'SIGKILL sent; child not reaped within5seconds'
                    good = False
            for stream in ('stdout', 'stderr'):
                p = run / (stream + '.txt')
                if not p.exists():
                    p.touch(exist_ok=False)
                receipt[stream + '_sha256'] = sha(p)
            receipt['process_reaped'] = proc is None or proc.poll() is not None
            receipt.update(status='PASS' if good else 'HOLD', ended_utc=now(), seconds=time.monotonic() - start)
            write(run / 'RECEIPT.json', receipt)
        print(json.dumps({'status': receipt['status'], 'run': str(run)}), flush=True)
        return 0 if good else 1


if __name__ == '__main__':
    raise SystemExit(main())
