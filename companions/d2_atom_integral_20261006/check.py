#!/usr/bin/env python3
"""Fixed six-target companion driver, adapted from #343 check.py bdeba903.

Exact source/run custody plus the unchanged core axiom parser. This explicit
small-module inventory is not the separate general Lean declaration scanner.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess

SIDE=Path(__file__).resolve().parent
ROOT=SIDE.parents[1]
PACKAGE='companions/d2_atom_integral_20261006'
WORKFLOW='.github/workflows/d2-atom-integral.yml'
REPO='d6g8k5htny-coder/Math-'
CORE_TREE='d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14'
CORE_MANIFEST='5d7ccdb0885af7bf4a2aa6ec4dce5f5c41435bb10a0a7a426a8af286d4f035e4'
CORE_GATE='958b149ea3a4ce735644a2079f817b5deddf5dc0d5ca347904ad09db6ad47d68'
CONSUMED={
 'companions/d2_moment_bridge_20261006/D2MomentBridge.lean':'b3184107e290189b91e3e18fd2aa1cb631bb9bde',
 'companions/d2_square_schur_20261006/D2SquareSchur.lean':'4855c92d55254969e1de7f8cf8dec2bdc027cf69'}
TARGETS=tuple('D2AtomIntegral.'+n for n in ('two_event_integral_lower','two_radius_integral_lower',
    'second_moment_floor','fourth_gap_floor','residual_moment_floor','schur_floor_of_radius_masses'))
FALSE_STATEMENTS={
 'RejectOverlappingEvents':'(1 : ℝ) * 1 + 1 * 1 ≤ 1',
 'RejectNonProbabilityGap':'(1 : ℝ) * 1 / (1+1) * (1-4)^2 ≤ 17-5^2',
 'RejectZeroRadiusStrictness':'(0 : ℝ) < 1/2-(1/2)^2/(1/2)'}
CONTROLS=tuple(FALSE_STATEMENTS)
PAYLOADS={PACKAGE+'/'+n for n in ('D2AtomIntegral.lean','Contract.lean','SCOPE.md','check.py','test_check.py','replay.sh')}|{WORKFLOW}

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def identity(raw):
    return {'bytes':len(raw),'sha256':sha(raw),
            'git_blob':hashlib.sha1(b'blob %d\0'%len(raw)+raw).hexdigest()}

def strict(raw):
    def pairs(items):
        out={}
        for k,v in items:
            require(k not in out,'duplicate JSON key');out[k]=v
        return out
    def reject(_):raise ValueError('noninteger JSON number')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=reject,parse_float=reject)

def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True,text=True,timeout=30).stdout.strip()

def source():
    meta=strict((SIDE/'SOURCE_FILES.json').read_bytes());head=git('rev-parse','HEAD')
    require(set(meta)=={'version','scientific_effect','core_tree','targets','files'},'manifest schema')
    require(type(meta['version']) is int and meta['version']==1,'manifest version')
    require(meta['scientific_effect']=='NONE' and meta['core_tree']==CORE_TREE,'scope')
    require(meta['targets']==list(TARGETS) and set(meta['files'])==PAYLOADS,'fixed inventory')
    require(re.fullmatch('[0-9a-f]{40}',head) is not None,'invalid HEAD')
    require(git('rev-parse',head+':formal')==CORE_TREE,'core tree changed')
    require(sha((ROOT/'formal/manifest.json').read_bytes())==CORE_MANIFEST,'core manifest changed')
    require(sha((ROOT/'formal/gate.py').read_bytes())==CORE_GATE,'core verifier changed')
    if os.environ.get('GITHUB_ACTIONS')=='true':
        require(os.environ.get('GITHUB_SHA')==head and os.environ.get('GITHUB_REPOSITORY')==REPO,'host/source mismatch')
        require(os.environ.get('GITHUB_RUN_ID') and os.environ.get('GITHUB_RUN_ATTEMPT'),'missing run identity')
    expected=PAYLOADS|{PACKAGE+'/SOURCE_FILES.json'}
    actual=set(git('ls-tree','-r','--name-only',head,'--',PACKAGE).splitlines())|{WORKFLOW}
    require(actual==expected,'tracked membership')
    ids={}
    for name in sorted(expected|set(CONSUMED)):
        path=ROOT/name
        require(not any(p.is_symlink() for p in (path,*path.parents)),'symlink source')
        ids[name]=identity(path.read_bytes())
        require(git('rev-parse',head+':'+name)==ids[name]['git_blob'],'dirty source: '+name)
        if name in PAYLOADS:require(meta['files'][name]==ids[name],'source identity: '+name)
        if name in CONSUMED:require(CONSUMED[name]==ids[name]['git_blob'],'consumed source changed: '+name)
    git('diff','--exit-code','HEAD','--','formal',PACKAGE,WORKFLOW,*CONSUMED)
    return {'checked_commit':head,'repository':REPO,'run_id':os.environ.get('GITHUB_RUN_ID','local'),
       'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local'),'core_tree':CORE_TREE,
       'sources':ids,'declarations':list(TARGETS),'scientific_effect':'NONE'}

def types(text):
    require('error:' not in text and 'warning:' not in text,'type diagnostic')
    matches=list(re.finditer(r'^D2AtomIntegral\.[A-Za-z][A-Za-z0-9_]*',text,re.M))
    require([m.group() for m in matches]==list(TARGETS),'type inventory')
    require(not text[:matches[0].start()].strip(),'type preamble')
    return list(TARGETS)

def negative(text,control,status):
    require(control in CONTROLS,'unknown control')
    require(type(status) is int and status==1,'negative exit must be exactly one')
    pattern=r'(?:[^\r\n]*[/\\])?'+control+r'\.lean:[0-9]+:[0-9]+: error: unsolved goals\s*\n⊢ False\s*'
    require(re.fullmatch(pattern,text) is not None,'not the intended False-goal diagnostic')
    return control

def core_gate():
    path=ROOT/'formal/gate.py'
    require(sha(path.read_bytes())==CORE_GATE,'core verifier changed')
    spec=importlib.util.spec_from_file_location('bound_core_gate',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def emit(out):
    (out/'Audit.lean').write_text('import D2AtomIntegral\n'+'\n'.join('#print axioms '+n for n in TARGETS)+'\n')
    (out/'Types.lean').write_text('import D2AtomIntegral\nset_option pp.explicit true\n'+'\n'.join('#check '+n for n in TARGETS)+'\n')
    for label,statement in FALSE_STATEMENTS.items():
        (out/(label+'.lean')).write_text('import D2AtomIntegral\nexample : '+statement+' := by\n  norm_num\n')

def finish(out):
    current=source();require(strict((out/'source.json').read_bytes())==current,'source changed during execution')
    ax=core_gate().audit_axioms((out/'axioms.log').read_text(),list(TARGETS))
    types((out/'types.log').read_text())
    for label in ('dependency-moment','dependency-square','build','contract','axioms','types','leanchecker'):
        require((out/(label+'.status')).read_bytes()==b'0\n','unsuccessful process: '+label)
    for label in CONTROLS:
        require((out/(label+'.status')).read_bytes()==b'1\n','negative status: '+label)
        negative((out/(label+'.log')).read_text(),label,1)
    raw=(ROOT/'formal/.lake/formal-evidence/receipt.json').read_bytes();core=strict(raw)
    require(core['checked_commit']==current['checked_commit'] and core['manifest_sha256']==CORE_MANIFEST,'core identity')
    require(core['formalization_status']=='kernel-checked','no core kernel receipt')
    result={**current,'axioms':ax,'theorem_count':6,'definition_count':0,'core_receipt_sha256':sha(raw),
       'formalization_status':'kernel-checked','alignment_status':'PENDING_INDEPENDENT_REVIEW',
       'scientific_acceptance':False,'log_sha256':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}}
    (out/'receipt.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=('source','emit','finish','negative'))
    ap.add_argument('path',type=Path,nargs='?');ap.add_argument('--control',choices=CONTROLS);ap.add_argument('--status',type=int)
    a=ap.parse_args()
    if a.command=='source':out=source()
    elif a.command=='emit':emit(a.path);out={'emitted':True}
    elif a.command=='finish':out=finish(a.path)
    else:out={'negative':negative(a.path.read_text(),a.control,a.status)}
    print(json.dumps(out,sort_keys=True,indent=2))

if __name__=='__main__':main()
