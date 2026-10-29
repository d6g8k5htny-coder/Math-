"""Pinned runtime selection and identity records; does not build or fetch artifacts."""
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess

LEAN_SHA = 'e8baaa71855a616dc351028f3ad2200051b0671f423a1696a100e809302d5550'
MATHLIB_COMMIT = 'd13f23b723b8a846827a245b89c10fc7d3f11612'
DEFAULT_PROJECT = Path(__file__).resolve().parent.parent
INVENTORY = DEFAULT_PROJECT/'references/runtime/external_runtime_inventory.json'

def worker_entry(project):
    return 'WorkerBootstrap.lean' if (Path(project)/'lean/WorkerBootstrap.lean').is_file() else 'ClosedProofWorker.lean'

def _hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

@dataclass(frozen=True)
class RuntimeConfig:
    lean: Path
    mathlib_root: Path
    build_dir: Path
    project_root: Path = DEFAULT_PROJECT

    def identities(self):
        lean, mathlib, project = Path(self.lean).resolve(), Path(self.mathlib_root).resolve(), Path(self.project_root).resolve()
        if _hash(lean) != LEAN_SHA: raise ValueError('Lean executable SHA256 mismatch')
        commit = subprocess.run(['git','-C',str(mathlib),'rev-parse','HEAD'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout.strip()
        if commit != MATHLIB_COMMIT: raise ValueError('Mathlib commit mismatch')
        if (mathlib/'lean-toolchain').read_text().strip() != 'leanprover/lean4:v4.34.1': raise ValueError('Lean toolchain mismatch')
        sources = {str(p.relative_to(project)): _hash(p) for p in sorted((project/'lean').rglob('*.lean'))}
        if not sources or 'lean/ClosedProofWorker.lean' not in sources: raise ValueError('worker source missing')
        build = Path(self.build_dir).resolve()
        manifest_path = build/'build_manifest.json'
        try:
            manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            raise ValueError('missing or invalid build manifest') from exc
        if not isinstance(manifest, dict) or manifest.get('schema') != 'ul-build-v1' or manifest.get('sources') != sources:
            raise ValueError('build manifest source mismatch')
        if manifest.get('runtime') != {'lean_executable_sha256':LEAN_SHA, 'mathlib_commit':commit}:
            raise ValueError('build manifest runtime mismatch')
        outputs = manifest.get('outputs')
        if not isinstance(outputs, dict) or not outputs:
            raise ValueError('build manifest outputs missing')
        expected = {str(Path(name).relative_to('lean').with_suffix('.olean')) for name in sources if name != 'lean/'+worker_entry(project)}
        if not expected.issubset(outputs): raise ValueError('build manifest missing compiled modules')
        actual = set()
        for directory, dirs, files in os.walk(build, followlinks=False):
            base = Path(directory)
            for entry in dirs:
                if (base/entry).is_symlink(): raise ValueError('symlink in build directory')
            for entry in files:
                path = base/entry
                if path.is_symlink() or not path.is_file(): raise ValueError('invalid build artifact')
                rel = path.relative_to(build).as_posix()
                if rel != 'build_manifest.json': actual.add(rel)
        if actual != set(outputs): raise ValueError('build inventory mismatch')
        for name, digest in outputs.items():
            if not isinstance(name, str) or not isinstance(digest, str): raise ValueError('invalid build output entry')
            pure = PurePosixPath(name)
            if pure.is_absolute() or pure.as_posix() != name or any(part in ('.', '..') for part in pure.parts): raise ValueError('noncanonical build output')
            output = (build/name).resolve()
            if not output.is_relative_to(build) or not output.is_file() or _hash(output) != digest:
                raise ValueError('build output mismatch: '+name)
        inventory = {'path':str(INVENTORY), 'sha256':_hash(INVENTORY)} if INVENTORY.is_file() else {'path':str(INVENTORY), 'available':False}
        return {'lean_executable':str(lean),'lean_executable_sha256':LEAN_SHA,'mathlib_root':str(mathlib),'mathlib_commit':commit,'lean_toolchain':'leanprover/lean4:v4.34.1','sources_sha256':sources,'build_manifest_sha256':_hash(manifest_path),'compiled_outputs_sha256':outputs,'external_runtime_inventory_reference':inventory,'trust_boundary':'Precompiled cache and shared libraries are external trusted artifacts; executable SHA does not bind shared libraries.'}

    def command(self):
        self.identities()
        return [str(Path(self.lean).resolve()), '-j1','-DElab.async=false','-DautoImplicit=false','-M11000','--run',str(Path(self.project_root).resolve()/'lean'/worker_entry(self.project_root))]

    def environment(self):
        mathlib = Path(self.mathlib_root).resolve()
        packages = mathlib/'.lake'/'packages'
        paths = [Path(self.build_dir).resolve(), mathlib/'.lake'/'build'/'lib'/'lean']
        if packages.is_dir(): paths.extend(p/'.lake'/'build'/'lib'/'lean' for p in sorted(packages.iterdir()) if (p/'.lake'/'build'/'lib'/'lean').is_dir())
        paths.append(Path(self.lean).resolve().parent.parent/'lib'/'lean')
        env = os.environ.copy()
        env['LEAN_PATH'] = os.pathsep.join(map(str, paths))
        return env

    def worker(self, *, receipt_dir, **kwargs):
        from .worker import LeanWorker
        identities = self.identities()
        command = [str(Path(self.lean).resolve()), '-j1','-DElab.async=false','-DautoImplicit=false','-M11000','--run',str(Path(self.project_root).resolve()/'lean'/worker_entry(self.project_root))]
        return LeanWorker(command, receipt_dir=receipt_dir, env=self.environment(), metadata=identities, **kwargs)
