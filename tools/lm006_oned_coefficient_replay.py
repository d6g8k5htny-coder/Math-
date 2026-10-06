#!/usr/bin/env python3
"""Replay the frozen PR380 one-dimensional LM006 coefficient certificate.

Standard library / POSIX only. Execution/custody interlock, not theorem acceptance.
"""
import argparse, hashlib, json, os, re, signal, subprocess, sys, time
from pathlib import Path, PurePosixPath

REPOSITORY='d6g8k5htny-coder/Math-'
SOURCE_COMMIT='8fe14358a1ee5d7ef7d7e20520391f62f432fe04'
PACKET='coefficients/lm006_wrong_sign_oned_20261006_a62c'
EXECUTION_FILES=('tools/lm006_oned_coefficient_replay.py','tests/test_lm006_oned_coefficient_replay.py','.github/workflows/lm006-oned-coefficient.yml')
PINS={
 PACKET+'/NOTE.md':'db27645e62bf846835b1daeb6c51f1eb3b417f1e',
 PACKET+'/oned.py':'5015dee3a660b67c42ccab13a976626e6e2d02cc',
 PACKET+'/test_oned.py':'62e54422726f1caffab62e2e3fe38d297013e52d',
 PACKET+'/RESULTS.json':'506833403f2dee91553d1a8dfc6eef6ee5c8faf8',
 PACKET+'/SOURCES.json':'a6de8d4113cedf548b17c750da406f8aa6705eb4',
 PACKET+'/PRIOR_WORK.md':'1fb9afde1490b8e86c3b1d453f1c16a45b35a352',
 'coefficients/lm006_wrong_sign_20261006_r20/enclose.py':'e680ddb7aa0abd4b6aab2cac6a54c1ff28efc782',
 'reviews/lm006_wrong_sign_asymptotic_20261006/NOTE.md':'ea914c1b8e0b8180b645f3f626e2081ab87700b9'}
DEPENDENCIES=('coefficients/lm006_wrong_sign_20261006_r20/enclose.py','reviews/lm006_wrong_sign_asymptotic_20261006/NOTE.md')
TEST_NAMES=('test_cli', 'test_conditional_formula_against_positive_integral', 'test_error_tail_and_quotient_attachment', 'test_exact_fourth_derivative_algebra', 'test_interval_arithmetic', 'test_invalid_resolution', 'test_low_resolution_is_genuine_enclosure', 'test_nonzero_integrand_and_scaling', 'test_parent_authentication', 'test_product_derivative_identity', 'test_reduction_from_truncated_moments', 'test_simpson_weights_and_error', 'test_tail_exact_series', 'test_tail_is_present_and_small', 'test_tail_sanity_and_domain')
MAX_STREAM_BYTES=4*1024*1024

class ReplayError(ValueError): pass

def require(ok,reason):
    if not ok: raise ReplayError(reason)
def sha256(raw): return hashlib.sha256(raw).hexdigest()
def git_blob(raw): return hashlib.sha1(b'blob %d\0'%len(raw)+raw).hexdigest()

def source_file(root,relative):
    require(type(relative) is str and relative and '\\' not in relative and not relative.startswith('/') and all(x not in ('','.','..') for x in relative.split('/')),'unsafe_path')
    p=Path(root)
    for part in PurePosixPath(relative).parts:
        p=p/part; require(not p.is_symlink(),'source_symlink')
    require(p.is_file(),'source_missing'); return p

def validate_snapshot(root,pins=None):
    pins=PINS if pins is None else pins; result={}
    for name,expected in pins.items():
        raw=source_file(root,name).read_bytes(); actual=git_blob(raw)
        require(actual==expected,'source_identity: '+name)
        result[name]={'bytes':len(raw),'sha256':sha256(raw),'git_blob':actual}
    names=sorted(Path(n).name for n in pins if n.startswith(PACKET+'/'))
    require(sorted(p.name for p in (Path(root)/PACKET).iterdir())==names,'packet_membership')
    return result

def check_output(stdout,stderr,expected,kind):
    if kind=='tests':
        prefix='\n'.join(n+' (test_oned.OneDimensionalTests.'+n+') ... ok' for n in TEST_NAMES).encode()
        pattern=re.escape(prefix+b'\n\n'+b'-'*70)+rb'\nRan 15 tests in [0-9]+(?:\.[0-9]+)?s\n\nOK\n'
        require(stdout==b'' and re.fullmatch(pattern,stderr) is not None,'test_report_mismatch'); return
    require(kind=='exact','unknown_contract'); require(stderr==b'','unexpected_stderr'); require(stdout==expected,'stdout_mismatch')

def write_json(path,value):
    with Path(path).open('x',encoding='utf-8',newline='\n') as f: json.dump(value,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')

def run_step(argv,cwd,logs,name,expected,kind,timeout=900):
    require(os.name=='posix','posix_required');require(re.fullmatch(r'[a-z][a-z0-9_-]*',name) is not None,'unsafe_step_name')
    logs=Path(logs); out=logs/(name+'.stdout');err=logs/(name+'.stderr');proc=logs/(name+'.process.json')
    require(not any(p.exists() or p.is_symlink() for p in (out,err,proc)),'step_evidence_exists')
    start=time.monotonic_ns();record={'command':list(map(str,argv)),'returncode':None,'timed_out':False,'status':'FAIL','timeout_seconds':timeout};failure=None
    with out.open('xb') as so,err.open('xb') as se:
        try:
            child=subprocess.Popen(argv,cwd=cwd,stdout=so,stderr=se,start_new_session=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
            try: record['returncode']=child.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                record['timed_out']=True;failure='timeout'
                try: os.killpg(child.pid,signal.SIGKILL)
                except ProcessLookupError: pass
                record['returncode']=child.wait(timeout=5)
        except OSError as exc: failure='spawn_error';record['detail']=type(exc).__name__+': '+str(exc)
    record['elapsed_ns']=time.monotonic_ns()-start;sizes=(out.stat().st_size,err.stat().st_size)
    if max(sizes)>MAX_STREAM_BYTES: failure=failure or 'output_too_large';record.update(stdout_bytes=sizes[0],stderr_bytes=sizes[1])
    else:
        a,b=out.read_bytes(),err.read_bytes();record.update(stdout_bytes=len(a),stderr_bytes=len(b),stdout_sha256=sha256(a),stderr_sha256=sha256(b))
        if failure is None:
            try: require(record['returncode']==0,'unexpected_exit');check_output(a,b,expected,kind)
            except ReplayError as exc: failure=str(exc)
    if failure is None: record['status']='PASS'
    else: record['failure']=failure
    write_json(proc,record)
    if failure is not None: raise ReplayError(failure)
    return record

def git(root,*args):
    p=subprocess.run(['git',*args],cwd=root,capture_output=True,timeout=30);require(p.returncode==0,'git_command_failed');return p.stdout.decode('ascii').strip()
def git_head(root):
    h=git(root,'rev-parse','HEAD');require(re.fullmatch('[0-9a-f]{40}',h) is not None,'invalid_git_head');return h

def execution_sources(root,head):
    result={}
    for name in EXECUTION_FILES:
        raw=source_file(root,name).read_bytes();committed=git(root,'rev-parse',head+':'+name);require(committed==git_blob(raw),'execution_source_drift');result[name]={'git_blob':committed,'sha256':sha256(raw),'bytes':len(raw)}
    return result

def host_identity(head,env):
    if env.get('GITHUB_ACTIONS')=='true':
        require(env.get('GITHUB_REPOSITORY')==REPOSITORY and env.get('GITHUB_SHA')==head,'host_identity')
        for k in ('GITHUB_RUN_ID','GITHUB_RUN_ATTEMPT'): require(re.fullmatch('[1-9][0-9]*',env.get(k,'')) is not None,'host_identity')

def execute(root,output,mode):
    root,output=Path(root).resolve(),Path(output).resolve();require(mode in ('normal','optimized'),'invalid_mode');require(not output.is_relative_to(root),'evidence_inside_source');require(not output.exists(),'evidence_exists');output.mkdir(parents=True)
    receipt={'schema_version':1,'object':'LM006-ONED-COEFFICIENT-REPLAY','repository':REPOSITORY,'source_commit':SOURCE_COMMIT,'mode':mode,'scientific_acceptance':False,'formal_verification':False,'status':'FAIL','steps':{},'run_id':os.environ.get('GITHUB_RUN_ID'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),'event':os.environ.get('GITHUB_EVENT_NAME')}
    try:
        before=validate_snapshot(root);head=git_head(root);receipt['tested_commit']=head;host_identity(head,os.environ);receipt['execution_sources']=execution_sources(root,head);receipt['sources']=before
        require(Path(__file__).resolve()==root/EXECUTION_FILES[0],'driver_location');require(git(root,'status','--porcelain','--untracked-files=no')=='','tracked_source_dirty')
        packet=root/PACKET;flags=['-B']+(['-O'] if mode=='optimized' else [])+['-S']
        specs=[('tests',['-m','unittest','test_oned','-v'],None,'tests'),('coefficient',['oned.py','--panels','1024'],(packet/'RESULTS.json').read_bytes(),'exact')]
        for name,args,expected,kind in specs:
            try: run_step([sys.executable,*flags,*args],packet,output,name,expected,kind)
            finally:
                p=output/(name+'.process.json')
                if p.is_file(): receipt['steps'][name]={'process_sha256':sha256(p.read_bytes()),'record':json.loads(p.read_bytes())}
        require(validate_snapshot(root)==before,'source_changed_during_execution');require(execution_sources(root,head)==receipt['execution_sources'],'execution_source_drift');require(git_head(root)==head,'head_changed_during_execution');require(git(root,'status','--porcelain','--untracked-files=no')=='','tracked_source_dirty');receipt['status']='PASS'
    except Exception as exc: receipt['failure']=type(exc).__name__+': '+str(exc);raise
    finally: write_json(output/'receipt.json',receipt)
    return receipt

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path('.'));p.add_argument('--output',type=Path,required=True);p.add_argument('--mode',choices=('normal','optimized'),required=True);a=p.parse_args()
    try: result=execute(a.root,a.output,a.mode)
    except Exception as exc: print('LM006_ONED_REPLAY_FAIL: '+type(exc).__name__+': '+str(exc),file=sys.stderr);return 1
    print(json.dumps(result,sort_keys=True,indent=2,allow_nan=False));return 0
if __name__=='__main__': raise SystemExit(main())
