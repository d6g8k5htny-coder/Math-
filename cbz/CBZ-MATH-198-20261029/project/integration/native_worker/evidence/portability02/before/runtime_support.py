"""Runtime selection for this derivative; no worker is launched by this module."""
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
import pinned_runtime as rt
rt.INVENTORY = HERE/'sources/external_runtime_inventory.json'
LEAN = Path('/workspace/scratch/universal-law-toolchains/lean-4.34.1-linux/bin/lean')
MATHLIB = Path('/workspace/scratch/universal-law-toolchains/mathlib-d13f23b7')
FORMAL_EVIDENCE = ROOT/'evidence/final02/results.json'

def config(build):
    lean = Path(os.environ.get('UL_LEAN', str(LEAN)))
    mathlib = Path(os.environ.get('UL_MATHLIB_ROOT', str(MATHLIB)))
    return rt.RuntimeConfig(lean, mathlib, Path(build), HERE)

def require(condition, reason):
    if not condition: raise ValueError(reason)

def dependency_bindings(formal_cache, formal_evidence=FORMAL_EVIDENCE):
    sys.path.insert(0, str(ROOT/'integration/engine_audit'))
    import catalog
    value=catalog.verify_catalog()
    require((HERE/'lean/Integration/EndpointTasks.lean').read_bytes() ==
            (ROOT/'formal/Integration/EndpointTasks.lean').read_bytes(), 'wrapper source copies differ')
    fresh=json.loads(Path(formal_evidence).read_text())
    require(fresh['status']=='PASS' and fresh['cache_was_fresh'] is True
            and fresh['old_project_cache_on_lean_path'] is False, 'formal evidence is not a fresh passing build')
    require(fresh['runtime']=={'lean_executable_sha256':rt.LEAN_SHA,'mathlib_commit':rt.MATHLIB_COMMIT,
            'trust':fresh['runtime']['trust']}, 'formal evidence runtime mismatch')
    bindings={}
    for source in value['provenance']['copied_formal_sources_sha256']:
        module=source[7:-5].replace('/', '.')
        relative=source[7:-5]+'.olean'
        found=Path(formal_cache)/relative
        require(found.is_file(), 'missing compiled formal dependency: '+module)
        require(not found.is_symlink(), 'symlink compiled formal dependency')
        digest=rt._hash(found)
        require(fresh['sources'][source]==value['provenance']['copied_formal_sources_sha256'][source]
                and fresh['outputs'][relative]==digest, 'formal source/output evidence mismatch: '+module)
        bindings[module]={'path':str(found.resolve()),'sha256':digest,'source_sha256':fresh['sources'][source]}
    require(fresh['sources']['formal/Integration/EndpointTasks.lean']==rt._hash(ROOT/'formal/Integration/EndpointTasks.lean'), 'fresh wrapper source evidence mismatch')
    return bindings

def environment(build, formal_cache):
    import os
    env=config(build).environment()
    env['LEAN_PATH']=os.pathsep.join([str(Path(build).resolve()),str(Path(formal_cache).resolve()),
                                     env['LEAN_PATH']])
    env['PYTHONDONTWRITEBYTECODE']='1'
    return env

def validate_build(build):
    cfg=config(build)
    identities=cfg.identities()
    manifest=json.loads((Path(build)/'build_manifest.json').read_text())
    dependencies=manifest['formal_dependencies']
    require(rt._hash(Path(manifest['formal_evidence']['path']))==manifest['formal_evidence']['sha256'],'formal evidence source changed')
    require(dependency_bindings(manifest['formal_cache'],manifest['formal_evidence']['path']) == dependencies, 'formal compiled dependency changed')
    return cfg, identities, manifest
