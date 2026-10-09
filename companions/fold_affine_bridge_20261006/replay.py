#!/usr/bin/env python3
"""Source-bound bounded fold companion replay. Source, kernel and alignment stay separate."""
import argparse
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import resource
import threading
import signal
import subprocess
import sys
import time

SIDE=Path(__file__).resolve().parent
ROOT=SIDE.parents[1]
PACKAGE='companions/fold_affine_bridge_20261006'
WORKFLOW='.github/workflows/fold-affine-bridge.yml'
REPO='d6g8k5htny-coder/Math-'
BASE='34618d0d032f4361c1ec163f3b4cfd6ad01ab814'
CORE_TREE='d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14'
CORE_GATE='958b149ea3a4ce735644a2079f817b5deddf5dc0d5ca347904ad09db6ad47d68'
CORE_MANIFEST='5d7ccdb0885af7bf4a2aa6ec4dce5f5c41435bb10a0a7a426a8af286d4f035e4'
DEFINITIONS=tuple('FoldAffineBridge.'+n for n in ('affinePotential','plusPoint','minusPoint','physicalSeparation'))
TARGETS=tuple('FoldAffineBridge.'+n for n in (
 'fold_hasDerivAt','fold_deriv','fold_second','fold_critical','fold_nondegenerate','fold_curvature',
 'affine_hasDerivAt','affine_deriv','affine_hasDerivAt_deriv','affine_second','affine_coordinates',
 'affine_critical','affine_orientation','affine_distinct','affine_curvature','affine_nondegenerate',
 'affine_curvature_sign','separation_eq','separation_nonneg','separation_zero','affine_signed_gap',
 'affine_absolute_gap','affine_increments','affine_local_signs','affine_zero_degenerate',
 'affine_zero_increment','affine_zero_crossing','affine_constant_a','affine_constant_c'))
CONTROLS=('RejectMissingScale','RejectZeroNondegenerate','RejectSignedCurvature')
PAYLOADS={PACKAGE+'/'+n for n in ('FoldAffineBridge.lean','Contract.lean','README.md','replay.py','test_contract.py')}|{WORKFLOW}

def require(ok,message):
    if not ok:raise ValueError(message)

def strict_json(raw):
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'duplicate JSON key');result[k]=v
        return result
    def reject(value):raise ValueError('nonfinite JSON number: '+value)
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)

def identity(raw):
    return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
            'git_blob':hashlib.sha1(b'blob %d\0'%len(raw)+raw).hexdigest()}

def validate_metadata(meta):
    require(type(meta) is dict and set(meta)=={'version','scientific_effect','core_tree','targets','definitions','files'},'metadata schema')
    require(type(meta['version']) is int and meta['version']==1,'metadata version')
    require(meta['scientific_effect']=='NONE' and meta['core_tree']==CORE_TREE,'metadata scope')
    require(meta['targets']==list(TARGETS) and meta['definitions']==list(DEFINITIONS),'declaration inventory')
    require(type(meta['files']) is dict and set(meta['files'])==PAYLOADS,'file inventory')
    for name,item in meta['files'].items():
        require(type(item) is dict and set(item)=={'bytes','sha256','git_blob'},'file identity schema: '+name)
        require(type(item['bytes']) is int and item['bytes']>=0,'byte count')
        require(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}',item['sha256']) is not None,'sha256')
        require(type(item['git_blob']) is str and re.fullmatch('[0-9a-f]{40}',item['git_blob']) is not None,'git blob')

def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True,text=True,timeout=30).stdout.strip()

def source():
    meta=strict_json((SIDE/'SOURCE_FILES.json').read_bytes());validate_metadata(meta)
    head=git('rev-parse','HEAD')
    require(git('rev-parse',head+':formal')==CORE_TREE,'primary formal tree changed')
    require(identity((ROOT/'formal/gate.py').read_bytes())['sha256']==CORE_GATE,'core gate changed')
    require(identity((ROOT/'formal/manifest.json').read_bytes())['sha256']==CORE_MANIFEST,'core manifest changed')
    expected=PAYLOADS|{PACKAGE+'/SOURCE_FILES.json'}
    require(set(git('ls-tree','-r','--name-only',head,'--',PACKAGE).splitlines())|{WORKFLOW}==expected,'tracked membership')
    ids={}
    for name in sorted(expected):
        path=ROOT/name
        require(not any(p.is_symlink() for p in (path,*path.parents)),'symlink source: '+name)
        ids[name]=identity(path.read_bytes())
        require(ids[name]['git_blob']==git('rev-parse',head+':'+name),'dirty source: '+name)
        if name in PAYLOADS:require(ids[name]==meta['files'][name],'source identity: '+name)
    git('diff','--exit-code','HEAD','--','formal',PACKAGE,WORKFLOW)
    if os.environ.get('GITHUB_ACTIONS')=='true':
        require(os.environ.get('GITHUB_SHA')==head and os.environ.get('GITHUB_REPOSITORY')==REPO,'host/source mismatch')
        require(os.environ.get('GITHUB_RUN_ID') and os.environ.get('GITHUB_RUN_ATTEMPT'),'missing run identity')
    return {'repository':REPO,'checked_commit':head,'core_tree':CORE_TREE,'sources':ids,
            'targets':list(TARGETS),'definitions':list(DEFINITIONS),'scientific_effect':'NONE',
            'run_id':os.environ.get('GITHUB_RUN_ID','local'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local')}

def validate_negative(label,status,stdout,stderr):
    require(label in CONTROLS,'unknown control')
    require(type(status) is int and status==1,'negative exit must be exactly one')
    require(stderr==b'','negative stderr')
    pattern=rb'(?:[^\r\n]*[/\\])?'+label.encode()+rb'\.lean:[0-9]+:[0-9]+: error: unsolved goals\s*\n\xe2\x8a\xa2 False\s*'
    require(re.fullmatch(pattern,stdout) is not None,'not the intended named False-goal diagnostic')
    return label

def parse_proc_stat(text,ticks,page_size):
    prefix,separator,tail=text.rpartition(')')
    require(bool(separator),'malformed proc stat')
    pid,comm=prefix.split(' (',1);fields=tail.split()
    require(len(fields)>=22,'short proc stat')
    return {'pid':int(pid),'name':comm,'process_group':int(fields[2]),'start_ticks':int(fields[19]),
            'user_cpu_seconds':int(fields[11])/ticks,'system_cpu_seconds':int(fields[12])/ticks,
            'rss_kib':max(0,int(fields[21]))*page_size//1024}

def read_process_group(group):
    items=[];unreadable=0
    ticks=os.sysconf('SC_CLK_TCK');page_size=os.sysconf('SC_PAGE_SIZE')
    for path in Path('/proc').iterdir():
        if not path.name.isdecimal():continue
        try:item=parse_proc_stat((path/'stat').read_text(),ticks,page_size)
        except (FileNotFoundError,ProcessLookupError):continue
        except PermissionError:unreadable+=1;continue
        if item['process_group']!=group:continue
        try:
            match=re.search(r'^VmHWM:\s+([0-9]+)\s+kB$',(path/'status').read_text(),re.M)
            item['hwm_kib']=int(match.group(1)) if match else None
        except (FileNotFoundError,ProcessLookupError):item['hwm_kib']=None
        items.append(item)
    return {'processes':items,'unreadable_stat_entries':unreadable}

def run_process(out,label,argv,timeout=600,require_success=True,cwd=ROOT,env=None,
                capture_resources=False,resource_interval=.5):
    require(resource_interval>0,'resource interval must be positive')
    started=time.monotonic();timed_out=False
    usage_before=resource.getrusage(resource.RUSAGE_CHILDREN) if capture_resources else None
    process=subprocess.Popen(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    stop=threading.Event();samples=[];capture_errors=[]
    def monitor():
        try:
            with (out/(label+'.resources.jsonl')).open('w') as stream:
                while True:
                    sample={'elapsed_seconds':round(time.monotonic()-started,6),**read_process_group(process.pid)}
                    stream.write(json.dumps(sample,sort_keys=True)+'\n');stream.flush();samples.append(sample)
                    if stop.wait(resource_interval):break
        except Exception as error:capture_errors.append(repr(error))
    worker=threading.Thread(target=monitor,name='bounded-resource-sampler',daemon=True) if capture_resources else None
    if worker:worker.start()
    try:
        try:stdout,stderr=process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out=True;os.killpg(process.pid,signal.SIGKILL);stdout,stderr=process.communicate()
    finally:
        if worker:stop.set();worker.join()
    (out/(label+'.stdout')).write_bytes(stdout);(out/(label+'.stderr')).write_bytes(stderr)
    record={'argv':argv,'exit_code':process.returncode,'timed_out':timed_out,'seconds':round(time.monotonic()-started,6)}
    if capture_resources:
        after=resource.getrusage(resource.RUSAGE_CHILDREN);seen={}
        for sample in samples:
            for item in sample['processes']:
                key=(item['pid'],item['start_ticks']);old=seen.get(key,{'user_cpu_seconds':0,'system_cpu_seconds':0})
                seen[key]={'user_cpu_seconds':max(old['user_cpu_seconds'],item['user_cpu_seconds']),
                           'system_cpu_seconds':max(old['system_cpu_seconds'],item['system_cpu_seconds'])}
        summary={'observations_only':True,'sample_interval_seconds':resource_interval,'sample_count':len(samples),
          'capture_error':'; '.join(capture_errors) if capture_errors else None,
          'observed_peak_group_rss_sum_kib':max((sum(p['rss_kib'] for p in v['processes']) for v in samples),default=0),
          'observed_peak_process_hwm_kib':max((p['hwm_kib'] or 0 for v in samples for p in v['processes']),default=0),
          'observed_process_cpu_user_seconds':sum(v['user_cpu_seconds'] for v in seen.values()),
          'observed_process_cpu_system_seconds':sum(v['system_cpu_seconds'] for v in seen.values()),
          'children_user_cpu_delta_seconds':after.ru_utime-usage_before.ru_utime,
          'children_system_cpu_delta_seconds':after.ru_stime-usage_before.ru_stime,
          'children_cumulative_maxrss_before_kib':usage_before.ru_maxrss,
          'children_cumulative_maxrss_after_kib':after.ru_maxrss,
          'limits':'Samples can miss fast/exited processes or final peaks; group RSS sums may double-count shared pages. Child CPU deltas may exclude unreaped descendants on forced kill. Cumulative maxrss is not the checker-only peak.'}
        (out/(label+'.resources.json')).write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
        record['resource_capture_error']=summary['capture_error']
    (out/(label+'.status.json')).write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    sys.stdout.buffer.write(stdout);sys.stderr.buffer.write(stderr)
    if timed_out:raise RuntimeError(label+' timed out')
    if require_success and process.returncode!=0:raise RuntimeError(label+' exit '+str(process.returncode))
    if capture_errors:raise RuntimeError(label+' resource capture failed: '+str(capture_errors))
    return process.returncode

def rational_controls():
    def f(s,x):return -x**3/3+s*s*x
    cases=0
    for s in map(Q,[-2,-1,0,1,2]):
        for a in map(Q,[-3,-2,-1,1,2,3]):
            for b in map(Q,[-2,0,3]):
                for c in map(Q,[-3,-1,0,1,3]):
                    p=(s-b)/a;m=(-s-b)/a;r=2*abs(s)/abs(a)
                    gap=c*f(s,a*p+b)-c*f(s,a*m+b)
                    require(abs(p-m)==r and abs(gap)==abs(c)*abs(a)**3*r**3/6,'rational affine gap')
                    require(gap==c*(2*s)**3/6,'signed gap')
                    require((p==m)==(s==0),'degenerate points')
                    for h in (Q(-1,5),Q(1,7)):
                        gp=c*(f(s,a*(p+h)+b)-f(s,a*p+b))
                        gm=c*(f(s,a*(m+h)+b)-f(s,a*m+b))
                        require(gp==-c*(a*h)**2*(s+a*h/3) and gm==c*(a*h)**2*(s-a*h/3),'increments')
                        if s and c and abs(h)<abs(s)/abs(a):
                            require(c*s*gp<0 and c*s*gm>0,'local signs')
                        if s==0 and c:
                            require(gp*c*(f(s,a*(p-h)+b)-f(s,a*p+b))<0,'zero crossing')
                    cases+=1
    return {'cases':cases,'failed':0,'reference':{'separation':'1','absolute_gap':'4'},'kernel_evidence':False}

def emit(out):
    names=DEFINITIONS+TARGETS
    (out/'Audit.lean').write_text('import FoldAffineBridge\n'+'\n'.join('#print axioms '+n for n in names)+'\n')
    (out/'Types.lean').write_text('import FoldAffineBridge\nset_option pp.explicit true\n'+'\n'.join('#check '+n for n in names)+'\n')
    expressions={
      'RejectMissingScale':('abs (affinePotential 1 2 0 3 (plusPoint 1 2 0)-affinePotential 1 2 0 3 (minusPoint 1 2 0)) = (1/6 : ℝ)',
        'norm_num [affinePotential, foldPotential, plusPoint, minusPoint]'),
      'RejectZeroNondegenerate':('deriv (deriv (foldPotential 0)) 0 ≠ 0','norm_num [fold_second]'),
      'RejectSignedCurvature':('deriv (deriv (foldPotential (-1))) (-1) < 0','norm_num [fold_second]')}
    for label,(statement,tactic) in expressions.items():
        (out/(label+'.lean')).write_text('import FoldAffineBridge\nopen ResearchFormalCoreR1 FoldAffineBridge\nexample : '+statement+' := by\n  '+tactic+'\n')

def execute(out):
    require(not out.exists(),'output already exists');out.mkdir(parents=True)
    before=source();(out/'source.json').write_text(json.dumps(before,sort_keys=True,indent=2)+'\n')
    emit(out)
    run_process(out,'core-execute',[sys.executable,'-B','-S','formal/gate.py','--execute'],timeout=1200)
    build=out/'build';build.mkdir()
    env={**os.environ,'BQ_BUILD':str(build),'BQ_SIDE':str(SIDE)}
    prefix=['lake','env','bash','-c','export LEAN_PATH="$BQ_BUILD:$BQ_SIDE:${LEAN_PATH:-}"; export LEAN_SRC_PATH="$BQ_SIDE:${LEAN_SRC_PATH:-}"; exec "$@"','--']
    def lean(label,args,success=True,timeout=600,capture_resources=False):
        return run_process(out,label,prefix+args,timeout=timeout,require_success=success,cwd=ROOT/'formal',env=env,capture_resources=capture_resources)
    lean('toolchain',['lean','--version'])
    require((out/'toolchain.stdout').read_text().startswith('Lean (version 4.34.1,'),'wrong Lean version')
    lean('build',['lean','-DwarningAsError=true','--root='+str(SIDE),'-o',str(build/'FoldAffineBridge.olean'),str(SIDE/'FoldAffineBridge.lean')])
    lean('contract',['lean','-DwarningAsError=true','--root='+str(SIDE),str(SIDE/'Contract.lean')])
    lean('axioms',['lean','-DwarningAsError=true','--root='+str(out),str(out/'Audit.lean')])
    lean('types',['lean','-DwarningAsError=true','--root='+str(out),str(out/'Types.lean')])
    lean('leanchecker',['leanchecker','--fresh','FoldAffineBridge'],timeout=1200,capture_resources=True)
    for label in CONTROLS:
        status=lean(label,['lean','-DwarningAsError=true','--root='+str(out),str(out/(label+'.lean'))],False)
        validate_negative(label,status,(out/(label+'.stdout')).read_bytes(),(out/(label+'.stderr')).read_bytes())
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        run_process(out,'companion-tests-'+mode,[sys.executable,'-B',*flags,'-S',str(SIDE/'test_contract.py')])
        for suite in ('tests','formal/tests'):
            run_process(out,suite.replace('/','-')+'-'+mode,[sys.executable,'-B',*flags,'-S','-m','unittest','discover','-s',suite,'-v'])
    require(source()==before,'source changed during execution')
    gate_path=ROOT/'formal/gate.py'
    require(identity(gate_path.read_bytes())['sha256']==CORE_GATE,'core audit changed')
    spec=importlib.util.spec_from_file_location('unchanged_core_gate',gate_path)
    gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    axioms=gate.audit_axioms((out/'axioms.stdout').read_text(),list(DEFINITIONS+TARGETS))
    require((out/'axioms.stderr').read_bytes()==b'' and (out/'types.stderr').read_bytes()==b'','audit diagnostic stderr')
    text=(out/'types.stdout').read_text()
    require('error:' not in text and 'warning:' not in text,'type diagnostic')
    require(re.findall(r'^FoldAffineBridge\.[A-Za-z][A-Za-z0-9_]*',text,re.M)==list(DEFINITIONS+TARGETS),'type inventory')
    raw=(ROOT/'formal/.lake/formal-evidence/receipt.json').read_bytes();core=strict_json(raw)
    require(core['checked_commit']==before['checked_commit'] and core['manifest_sha256']==CORE_MANIFEST,'core receipt identity')
    require(core['formalization_status']=='kernel-checked','no core kernel receipt')
    result={**before,'axioms':axioms,'core_receipt_sha256':identity(raw)['sha256'],
      'formalization_status':'kernel-checked','alignment_status':'PENDING_INDEPENDENT_REVIEW',
      'scientific_acceptance':False,'logs':{p.name:identity(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}}
    (out/'receipt.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('command',choices=('source','controls','execute'))
    ap.add_argument('--out',type=Path,default=ROOT/'.lake/fold-affine-bridge-evidence');a=ap.parse_args()
    result=source() if a.command=='source' else rational_controls() if a.command=='controls' else execute(a.out.resolve())
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
