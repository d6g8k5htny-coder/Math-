"""Freeze C291 source inputs and hash the exact pre-existing dependency artifacts.

Run only after development checks and source review. Does not modify caches.
The same serial lock as both Lean runners prevents concurrent C291 compilation.
"""
from pathlib import Path
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import shutil
from run_final_phase import ROOT, CACHE, BIN, dependency_paths

OLD = ['GaussianSeriesFoundation', 'SpectralWeights', 'SourceFourierSeries',
       'SourceLattice', 'SourceKernel', 'SourceGaussianLaw', 'SourceCovariance',
       'SourceC4', 'SourceSmooth', 'SourceTorus', 'SourceTorusC4',
       'SourceSmoothCarrier', 'SourceSmoothControls']
NEW = ['SourceThetaBridge', 'SourceLifetimeGeometry', 'SourceLifetimeField',
       'SourceLifetimeControls', 'SourceLifetimeAxiomAudit']


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write(path, data):
    with path.open('x') as f:
        f.write(json.dumps(data, indent=2) + '\n')


def main():
    with (ROOT / 'lean-slot.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        started = datetime.now(timezone.utc).isoformat()
        project = ROOT / 'final-project'
        build = ROOT / 'final-build'
        require(not project.exists() and not build.exists(), 'final directories already exist')
        require(not (ROOT / 'FINAL_SOURCE_INVENTORY.json').exists(), 'final inventory exists')
        write(ROOT / 'FINAL_PREPARE_START.json', {'started_utc': started,
              'status': 'STARTED_ONCE; absence of final inventory means interrupted preparation'})
        modules = OLD + ['Lifetime'] + NEW
        sources = []
        for m in modules:
            p = ROOT / 'project' / (m + '.lean')
            require(p.is_file() and not p.is_symlink(), 'nonregular source: ' + str(p))
            sources.append({'name': p.name, 'sha256': sha(p), 'bytes': p.stat().st_size})
        names = set(modules)
        imports = {m: [n for line in (ROOT / 'project' / (m + '.lean')).read_text().splitlines()
                       if line.startswith('import ') for n in line[7:].split() if n in names]
                   for m in modules}
        order = []
        pending = list(modules)
        while pending:
            available = [m for m in pending if set(imports[m]) <= set(order)]
            require(bool(available), 'local import cycle')
            for m in available:
                order.append(m)
                pending.remove(m)
        manifest = json.loads((CACHE / 'lake-manifest.json').read_text())
        roots = [BIN.parent / 'lib/lean'] + [
            CACHE / '.lake/packages' / p['name'] / '.lake/build/lib'
            for p in manifest['packages']]
        roots = [p for p in roots if p.is_dir()]
        artifacts = []
        paths = dependency_paths(roots)
        print(json.dumps({'stage': 'HASHING_DEPENDENCY_ARTIFACTS', 'count': len(paths)}), flush=True)
        for i, p in enumerate(paths):
            require(not p.is_symlink(), str(p))
            before = p.stat()
            digest = sha(p)
            after = p.stat()
            stamp = lambda s: [s.st_size, s.st_mtime_ns, s.st_ino]
            require(stamp(before) == stamp(after), 'dependency changed during hashing')
            artifacts.append({'path': str(p), 'sha256': digest, 'stat': stamp(after)})
            if (i + 1) % 20000 == 0:
                print(json.dumps({'stage': 'HASHED', 'count': i + 1}), flush=True)
        require(dependency_paths(roots) == paths, 'dependency path set changed during hashing')
        dep_path = ROOT / 'FINAL_DEPENDENCY_ARTIFACTS.json'
        write(dep_path, {'started_utc': started, 'roots': [str(p) for p in roots],
                         'artifacts': artifacts, 'total_bytes': sum(x['stat'][0] for x in artifacts)})
        project.mkdir()
        build.mkdir()
        for item in sources:
            source = ROOT / 'project' / item['name']
            require(sha(source) == item['sha256'], 'source changed during freeze')
            shutil.copyfile(source, project / item['name'])
            require(sha(project / item['name']) == item['sha256'], 'copy hash mismatch')
        write(ROOT / 'FINAL_SOURCE_INVENTORY.json', {
            'started_utc': started, 'frozen_utc': datetime.now(timezone.utc).isoformat(),
            'sources': sources, 'new_modules': NEW, 'old_modules': OLD,
            'build_order': order, 'local_imports': imports,
            'dependency_artifact_inventory_sha256': sha(dep_path),
            'scientific_effect': 'NONE'})
        write(ROOT / 'evidence/FINAL_BUILD_INITIALIZATION.json', {
            'build_was_created_empty': not any(build.iterdir()),
            'source_inventory_sha256': sha(ROOT / 'FINAL_SOURCE_INVENTORY.json'),
            'initial_objects': [], 'utc': datetime.now(timezone.utc).isoformat()})
        print(json.dumps({'stage': 'FROZEN', 'modules': len(modules), 'order': order}), flush=True)


if __name__ == '__main__':
    main()
