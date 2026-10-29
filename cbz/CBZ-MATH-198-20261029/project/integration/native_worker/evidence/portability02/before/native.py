"""Serialized bounded build/session campaigns for49 trusted endpoint reuse tasks."""
import argparse
import fcntl
import json
from pathlib import Path
import shutil
import sys
import time

from runtime_support import HERE,ROOT,FORMAL_EVIDENCE,config,rt,dependency_bindings,environment,validate_build,require
sys.path.insert(0,str(ROOT))
from support.process import run_recorded

ORDER=['ClosedProofCore','ExprCodec','ExprDag','Integration.EndpointTasks','TrustedTasks','ClosedProofWorker']

def write(path,value): path.write_text(json.dumps(value,indent=2)+'\n')

def validate_destinations(root,build_dir,output):
    sealed=(Path(root)/'checksum_manifest.json').exists()
    require(not sealed or (not Path(build_dir).resolve().is_relative_to(Path(root).resolve())
                           and not Path(output).resolve().is_relative_to(Path(root).resolve())),
            'sealed payload requires build and evidence paths outside the payload')
    return sealed

def build(build_dir,output,formal_cache,formal_evidence=FORMAL_EVIDENCE):
    output.mkdir(parents=True,exist_ok=False)
    require(not build_dir.exists() or not any(build_dir.iterdir()),'refuse nonempty native build cache')
    build_dir.mkdir(parents=True,exist_ok=True)
    sources={p.relative_to(HERE).as_posix():rt._hash(p) for p in sorted((HERE/'lean').rglob('*.lean'))}
    dependencies=dependency_bindings(formal_cache,formal_evidence)
    frozen=output/'frozen_sources'; shutil.copytree(HERE/'lean',frozen)
    result={'schema':'ul-native-endpoint-build-v1','status':'RUNNING','sources':sources,
            'formal_dependencies':dependencies,'formal_cache':str(formal_cache),
            'formal_evidence':{'path':str(formal_evidence),'sha256':rt._hash(formal_evidence)},
            'scope':'Fresh worker/wrapper build bound to the supplied fresh formal source/output evidence. External Lean/Mathlib/shared-library trust remains.','records':[]}
    try:
        lean = Path(config(build_dir).lean).resolve()
        require(rt._hash(lean)==rt.LEAN_SHA,'pinned Lean mismatch')
        for module in ORDER:
            relative=Path(*module.split('.')).with_suffix('.lean')
            source=frozen/relative; target=build_dir/relative.with_suffix('.olean')
            target.parent.mkdir(parents=True,exist_ok=True)
            command=[str(lean),'-j1','-M11000','-DElab.async=false','-DautoImplicit=false',
                     '--root='+str(frozen),'-o',str(target),str(source)]
            receipt=run_recorded(command,output/module,timeout=120,cwd=ROOT,
                                 env=environment(build_dir,formal_cache),max_output_bytes=4*1024*1024)
            result['records'].append({'module':module,'source_sha256':rt._hash(source),'receipt':receipt})
            require(receipt['succeeded'],'native module compile failed: '+module)
        require(sources=={p.relative_to(HERE).as_posix():rt._hash(p) for p in sorted((HERE/'lean').rglob('*.lean'))},'native source drift')
        manifest={'schema':'ul-build-v1','sources':sources,
                  'outputs':{p.relative_to(build_dir).as_posix():rt._hash(p) for p in sorted(build_dir.rglob('*.olean'))},
                  'runtime':{'lean_executable_sha256':rt.LEAN_SHA,'mathlib_commit':rt.MATHLIB_COMMIT},
                  'formal_dependencies':dependencies,'formal_cache':str(formal_cache),
                  'formal_evidence':{'path':str(formal_evidence),'sha256':rt._hash(formal_evidence)}}
        write(build_dir/'build_manifest.json',manifest)
        _,identities,_=validate_build(build_dir)
        result.update(status='PASS',runtime_identities=identities)
    except BaseException as exc:
        result.update(status='FAILED',error={'type':type(exc).__name__,'reason':str(exc)})
        raise
    finally: write(output/'results.json',result)
    return result

def sessions(build_dir,output):
    output.mkdir(parents=True,exist_ok=False)
    cfg,identities,manifest=validate_build(build_dir)
    code_paths=[*HERE.glob('*.py'),ROOT/'integration/engine_audit/ul_engine/search.py',
                ROOT/'integration/engine_audit/ul_engine/worker.py']
    code_hashes={str(p.relative_to(ROOT)):rt._hash(p) for p in sorted(code_paths)}
    result={'schema':'ul-native-endpoint-campaign-v1','status':'RUNNING','runtime_identities':identities,
            'controller_transport_sources_sha256':code_hashes,
            'source_exposed':True,'training_eligible':False,'native_guard_sha256':rt._hash(HERE/'exec_guard.py'),
            'scope':'Actual fixed-macro proof reuse and fresh-worker structural certificate rechecks; not discovery, training or a speedup benchmark.','records':[]}
    try:
        for mode in ['produce','recheck','budget']:
            command=[sys.executable,'-B',str(HERE/'session.py'),mode,'--build-dir',str(build_dir),'--output',str(output/mode)]
            if mode=='recheck': command += ['--certificates',str(output/'produce')]
            receipt=run_recorded(command,output/(mode+'-controller'),timeout=120,cwd=ROOT,
                                 env=environment(build_dir,manifest['formal_cache']),max_output_bytes=4*1024*1024)
            result['records'].append({'mode':mode,'receipt':receipt})
            require(receipt['succeeded'],'native session failed: '+mode)
        require(code_hashes=={str(p.relative_to(ROOT)):rt._hash(p) for p in sorted(code_paths)},'controller or new transport source changed during campaign')
        result['status']='PASS'
    except BaseException as exc:
        result.update(status='FAILED',error={'type':type(exc).__name__,'reason':str(exc)})
        raise
    finally: write(output/'results.json',result)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['build','sessions'])
    parser.add_argument('--build-dir',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--formal-cache',type=Path,default=ROOT/'build/final02')
    parser.add_argument('--formal-evidence',type=Path,default=FORMAL_EVIDENCE)
    args=parser.parse_args()
    build_dir=args.build_dir.resolve(); output=args.output.resolve()
    sealed=validate_destinations(ROOT,build_dir,output)
    begin=time.monotonic()
    lock_path=ROOT/'.native.lock'
    # A sealed payload is never mutated to create a missing lock file. Cold
    # replays share the sibling lock named for that extracted payload instead.
    if sealed and not lock_path.exists(): lock_path=ROOT.parent/(ROOT.name+'.native.lock')
    with lock_path.open('r' if sealed and lock_path.is_relative_to(ROOT) else 'a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        waited=time.monotonic()-begin
        value=build(build_dir,output,args.formal_cache.resolve(),args.formal_evidence.resolve()) if args.mode=='build' else sessions(build_dir,output)
        write(output/'lock_receipt.json',{'lock':str(lock_path),'wait_wall_seconds':waited,'serialized':True})
    print(json.dumps({'status':value['status'],'output':str(output)}))

if __name__=='__main__': main()
