#!/usr/bin/env python3
"""Replay the local contribution gates. This command never declares federation CBZ-0."""
import argparse
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from recorded_process import run_recorded, validate_command

HERE = Path(__file__).resolve().parents[1]
ORIGINAL = '/workspace/scratch/universal-law-project-closure'

def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            digest.update(block)
    return digest.hexdigest()

def write(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')

def freeze_inputs(roots, exclude=()):
    """Exact file names and bytes, with only explicitly declared path exclusions."""
    roots = sorted({str(Path(root).absolute()) for root in roots})
    exclusions = sorted({str(Path(path).absolute()) for path in exclude})
    files = {}
    for value in exclusions:
        path = Path(value)
        if not any(path != Path(root) and path.is_relative_to(Path(root)) for root in roots):
            raise ValueError('exclusion must be strictly inside an inventoried root')

    def excluded(path):
        return any(path == Path(item) or path.is_relative_to(Path(item)) for item in exclusions)

    def retain(path):
        if path.is_symlink(): raise ValueError('symlink in immutable input inventory: '+str(path))
        if not path.is_file(): raise ValueError('unsupported immutable input: '+str(path))
        files[str(path)] = sha(path)

    for name in roots:
        root = Path(name)
        if root.is_symlink(): raise ValueError('symlink inventory root')
        if root.is_file():
            retain(root)
            continue
        if not root.is_dir(): raise ValueError('missing inventory root: '+name)
        def unreadable(error): raise error
        for directory, dirs, names in os.walk(root, followlinks=False, onerror=unreadable):
            base = Path(directory)
            kept = []
            for entry in sorted(dirs):
                path = base/entry
                if excluded(path): continue
                if path.is_symlink(): raise ValueError('symlink in immutable input inventory: '+str(path))
                kept.append(entry)
            dirs[:] = kept
            for entry in sorted(names):
                path = base/entry
                if not excluded(path): retain(path)
    return {'schema':'cbz-frozen-inputs-v1','roots':roots,'excluded_paths':exclusions,
            'files_sha256':dict(sorted(files.items()))}

def _sources_match(frozen, inventory):
    try:
        if any(Path(path).is_symlink() or not Path(path).is_file() or sha(path)!=digest
               for path,digest in frozen.items()): return False
        if inventory is not None:
            current = freeze_inputs(inventory['roots'], inventory['excluded_paths'])
            if current != inventory: return False
        return True
    except (OSError, ValueError, TypeError, KeyError):
        return False

def validate_jobs(jobs):
    if type(jobs) not in (list, tuple) or not jobs:
        raise ValueError('nonempty literal job plan required')
    ids, normalized = [], []
    for job in jobs:
        if type(job) is not dict or set(job) - {'id','argv','cwd','timeout'} or not {'id','argv','cwd'} <= set(job):
            raise ValueError('job must contain only id, literal argv, cwd and optional timeout')
        identity = job['id']
        if type(identity) is not str or not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', identity):
            raise ValueError('invalid job ID')
        validate_command(job['argv'], job.get('timeout',300), job['cwd'], 32*1024*1024)
        # Fail before *any* launch for strings not representable as OS argv.
        try:
            for argument in job['argv']: os.fsencode(argument)
            os.fsencode(os.fspath(job['cwd']))
        except (TypeError, ValueError, UnicodeError) as exc:
            raise ValueError('job contains an invalid OS argument/path') from exc
        ids.append(identity)
        normalized.append({'id':identity,'argv':list(job['argv']),
                           'cwd':str(Path(job['cwd']).resolve()),'timeout':job.get('timeout',300)})
    if len(set(ids)) != len(ids):
        raise ValueError('empty, duplicate or invalid job IDs')
    return normalized

def execute_jobs(jobs, output, frozen, env=None, *, inventory=None):
    jobs = validate_jobs(jobs)
    # Fail on unserializable metadata before starting any job, not while trying
    # to retain its terminal receipt after work has already executed.
    json.dumps({'plan':jobs,'sources_sha256':frozen,'input_inventory':inventory},allow_nan=False)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    result = {'schema':'cbz-local-contribution-run-v1', 'status':'RUNNING', 'cbz_zero':False,
              'scope':'Only the explicit local contribution plan; no federation git/PR closure or universal theorem claim.',
              'plan':jobs, 'sources_sha256':frozen, 'input_inventory':inventory, 'records':[]}
    failure = None
    try:
        for job in jobs:
            if not _sources_match(frozen, inventory):
                failure = 'SOURCE_DRIFT'
                break
            leaf = output/job['id']
            try:
                receipt = run_recorded(job['argv'], leaf, cwd=job['cwd'], env=env,
                                       timeout=job.get('timeout', 300), max_output_bytes=32*1024*1024)
            except BaseException:
                if (leaf/'receipt.json').is_file():
                    result['records'].append({'id':job['id'], **json.loads((leaf/'receipt.json').read_text())})
                raise
            result['records'].append({'id':job['id'], **receipt})
            if not receipt['succeeded']:
                failure = 'CHILD_FAILED:'+job['id']
                break
            if not _sources_match(frozen, inventory):
                failure = 'SOURCE_DRIFT'
                break
        result['status'] = 'FAILED' if failure else 'LOCAL_CONTRIBUTION_PASS'
    except BaseException as exc:
        failure = type(exc).__name__+': '+str(exc)
        result['status'] = 'FAILED'
        raise
    finally:
        result['source_unchanged_final'] = _sources_match(frozen, inventory)
        if not result['source_unchanged_final']:
            failure = failure or 'SOURCE_DRIFT'
            result['status'] = 'FAILED'
        result['failure'] = failure
        write(output/'results.json', result)
    return result

def prepare_scan(source, output):
    """Exact inventory of the entire formal directory; no implicit suffix ignore."""
    files, modules, external = [], set(), {'Init'}
    paths = sorted((source/'formal').rglob('*'))
    for path in paths:
        if path.is_symlink(): raise ValueError('symlink in formal inventory')
        if path.is_dir(): continue
        if path.suffix != '.lean': raise ValueError('unsupported active formal file: '+str(path))
        module = path.relative_to(source/'formal').with_suffix('').as_posix().replace('/', '.')
        modules.add(module)
        auditor = path.name == 'FinalAudit.lean' or path.name == 'AllDeclarationsAudit.lean'
        files.append({'path':path.relative_to(source).as_posix(), 'sha256':sha(path),
                      'kind':'lean_auditor' if auditor else 'lean_proof','module':module})
    for item in files:
        for imported in re.findall(r'^import\s+([^\n]+)', (source/item['path']).read_text(), re.M):
            for name in imported.split():
                if name not in modules:
                    if name not in {'Lean','Init','Mathlib'} and not name.startswith('Mathlib.'):
                        raise ValueError('unresolved project import: '+name)
                    external.add(name)
    manifest = {'schema':'cbz-layer-a-manifest-v1','roots':['formal'],'files':files,
                'external_imports':{name:{'identity':'Pinned Lean4.34.1 / Mathlib d13f23b723b8a846827a245b89c10fc7d3f11612',
                                          'reason':'Explicit external dependency; actual runtime pins checked by fresh rebuild.'} for name in sorted(external)}}
    quarantine = copy.deepcopy(json.loads((HERE/'QUARANTINE.json').read_text()))
    for entry in quarantine['entries']:
        for location in entry['location']:
            path = location['path']
            if path == ORIGINAL or path.startswith(ORIGINAL+'/'):
                location['path'] = str(source)+path[len(ORIGINAL):]
    write(output/'layer_a_manifest.json', manifest)
    write(output/'relocated_quarantine.json', quarantine)
    return manifest

def plan(source, output, build, lean, mathlib):
    py = sys.executable
    jobs = []
    def add(name, argv, cwd, timeout=300):
        jobs.append({'id':name,'argv':list(map(str,argv)),'cwd':str(cwd),'timeout':timeout})
    for optimized in (False, True):
        flags = [py,'-B']+(['-O'] if optimized else [])
        suffix = 'optimized' if optimized else 'normal'
        add('auditor-tests-'+suffix, flags+['-m','unittest','discover','-s','tests','-v'], HERE)
    add('layer-a-scan', [py,'-B',HERE/'tools/layer_a_audit.py','--root',source,
                        '--manifest',output/'layer_a_manifest.json','--quarantine',output/'relocated_quarantine.json'],HERE)
    for folder, label in [(source,'proof-runner'),(source/'integration/engine_audit','engine'),
                           (source/'integration/corpus_admission','corpus'),(source/'integration/native_worker','native-adapter')]:
        for optimized in (False,True):
            flags=[py,'-B']+(['-O'] if optimized else [])
            add(label+('-optimized' if optimized else '-normal'), flags+['-m','unittest','discover','-s','tests','-v'],folder)
    add('catalog', [py,'-B',source/'integration/engine_audit/catalog.py','verify'],source/'integration/engine_audit')
    add('fresh-proof', [py,'-B',source/'rebuild.py','--lean',lean,'--mathlib-root',mathlib,
                       '--build-dir',build/'formal','--output',output/'formal-evidence'],source,1800)
    add('owned-kernel-audit', [py,'-B',HERE/'tools/owned_kernel_audit.py','--source',source,
                             '--formal-cache',build/'formal','--formal-evidence',output/'formal-evidence/results.json',
                             '--lean',lean,'--mathlib-root',mathlib,'--output',output/'owned-kernel-evidence',
                             '--parent-lock-held'],HERE,1800)
    native=source/'integration/native_worker/native.py'
    add('native-build',[py,'-B',native,'build','--build-dir',build/'native','--output',output/'native-build-evidence',
                         '--formal-cache',build/'formal','--formal-evidence',output/'formal-evidence/results.json'],source,900)
    add('native-sessions',[py,'-B',native,'sessions','--build-dir',build/'native','--output',output/'native-session-evidence'],source,600)
    add('native-saved-bindings',[py,'-B',source/'integration/native_worker/verify_native_saved.py','--campaign',output/'native-session-evidence'],source)
    return jobs

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--build-dir',type=Path,required=True)
    parser.add_argument('--lean',type=Path,required=True)
    parser.add_argument('--mathlib-root',type=Path,required=True)
    args=parser.parse_args()
    source,output,build,lean,mathlib=[p.resolve() for p in (args.source,args.output,args.build_dir,args.lean,args.mathlib_root)]
    if output.exists() or build.exists(): raise ValueError('new evidence/build directories required')
    if output.is_relative_to(source) or build.is_relative_to(source): raise ValueError('outputs must be outside immutable source')
    prep=output.with_name(output.name+'-inputs'); prep.mkdir(parents=True,exist_ok=False)
    prepare_scan(source,prep)
    jobs=plan(source,output,build,lean,mathlib)
    # Prepared inputs remain hash-bound in a sibling directory before the first child.
    jobs[2]['argv']=[str(prep/'layer_a_manifest.json') if x==str(output/'layer_a_manifest.json') else
                     str(prep/'relocated_quarantine.json') if x==str(output/'relocated_quarantine.json') else x for x in jobs[2]['argv']]
    inventory=freeze_inputs([source,HERE/'tools',HERE/'tests',HERE/'QUARANTINE.json',
                             prep/'layer_a_manifest.json',prep/'relocated_quarantine.json'],
                            exclude=[source/'build',source/'integration/native_worker/build',
                                     source/'.native.lock',source/'.git'])
    frozen=inventory['files_sha256']
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',UL_LEAN=str(lean),UL_MATHLIB_ROOT=str(mathlib))
    with (HERE/'.native.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        result=execute_jobs(jobs,output,frozen,env,inventory=inventory)
    print(json.dumps({'status':result['status'],'cbz_zero':False,'result':str(output/'results.json')}))
    return 0 if result['status']=='LOCAL_CONTRIBUTION_PASS' else 1

if __name__=='__main__': raise SystemExit(main())
