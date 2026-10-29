#!/usr/bin/env python3
"""Bounded companion driver, adapted from #317 check.py (812d0262).

Reuses the pinned core axiom audit. Neither this small inventory nor a receipt
is a general Lean declaration scanner or independent scientific acceptance.
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
PACKAGE='companions/d2_square_schur_20261006'
WORKFLOW='.github/workflows/d2-square-schur.yml'
REPO='d6g8k5htny-coder/Math-'
CORE_TREE='57c1b1a49f0ff75508a2c17e475ea21ab5b74043'
CORE_MANIFEST='ba7d11e43574e39da3c759e0501399a6dcd1b7da32b157a4a6b01f5c133b3062'
CORE_GATE='f5972ef37a113f70d8b75cac254181d91af05a53933612fd92889a626d1abe73'

CORE_SOURCE_IDENTITY='0db28eb324ec322a44a020337b31647cd46357356ba0c6d91c02c394f7af57ae'
CORE_IDENTITY_PATH='tools/required_formal_check.py'
CORE_IDENTITY_SHA256='6c27355237b45d3999298522c141984ff5b7c114f18b3c555cc45989976fc6dc'
CORE_IDENTITY_BLOB='0b9d694bdf888c75826ca07ae176c5a5c43b8880'
TARGETS=tuple('D2SquareSchur.'+n for n in ('weighted_square_identity','weighted_square_lower',
    'schur_no_upper','schur_from_lower_inputs'))
CONTROLS=('RejectSignedWeights','RejectEndpointMaximum','RejectOutsideDirection')
PAYLOADS={PACKAGE+'/'+n for n in ('D2SquareSchur.lean','Contract.lean','SCOPE.md','check.py','test_check.py','replay.sh')}|{WORKFLOW}

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

def metadata():return strict((SIDE/'SOURCE_FILES.json').read_bytes())

def core_identity():
    """Bind the outside-tree validator before evaluating its verified bytes."""
    path = ROOT / CORE_IDENTITY_PATH
    require(not any(p.is_symlink() for p in (path, *path.parents)) and path.is_file(),
            'core identity validator missing or symlink')
    raw = path.read_bytes()
    framed = b'blob ' + str(len(raw)).encode() + b'\0' + raw
    require(sha(raw) == CORE_IDENTITY_SHA256
            and hashlib.sha1(framed).hexdigest() == CORE_IDENTITY_BLOB,
            'core identity validator changed')
    namespace = {'__name__': 'bound_d2_core_identity', '__file__': str(path)}
    exec(compile(raw, str(path), 'exec'), namespace)
    manifest = ROOT / 'formal/manifest.json'
    manifest_raw = manifest.read_bytes()
    require(sha(manifest_raw) == CORE_MANIFEST, 'core manifest changed')
    digest = namespace['manifest_identity'](manifest, manifest_raw)
    require(digest == CORE_SOURCE_IDENTITY, 'core source identity changed')
    return digest


def validate_core_receipt(core, current):
    """The current core receipt binds the composite source, not the raw manifest."""
    require(isinstance(core, dict), 'invalid core receipt')
    require(core.get('checked_commit') == current['checked_commit'],
            'core executed different source')
    require(core.get('manifest_sha256') == core_identity(), 'core receipt manifest')
    require(core.get('formalization_status') == 'kernel-checked', 'no core kernel receipt')





def source():
    meta=metadata();head=git('rev-parse','HEAD')
    require(set(meta)=={'version','scientific_effect','core_tree','targets','files'},'manifest schema')
    require(meta['version']==1 and type(meta['version']) is int,'manifest version')
    require(meta['scientific_effect']=='NONE' and meta['core_tree']==CORE_TREE,'scope')
    require(meta['targets']==list(TARGETS) and set(meta['files'])==PAYLOADS,'fixed inventory')
    require(re.fullmatch('[0-9a-f]{40}',head) is not None,'invalid HEAD')
    require(git('rev-parse',head+':formal')==CORE_TREE,'core tree changed')
    require(sha((ROOT/'formal/manifest.json').read_bytes())==CORE_MANIFEST,'core manifest changed')
    require(sha((ROOT/'formal/gate.py').read_bytes())==CORE_GATE,'core verifier changed')
    core_identity()
    if os.environ.get('GITHUB_ACTIONS')=='true':
        require(os.environ.get('GITHUB_SHA')==head and os.environ.get('GITHUB_REPOSITORY')==REPO,'host/source mismatch')
        require(os.environ.get('GITHUB_RUN_ID') and os.environ.get('GITHUB_RUN_ATTEMPT'),'missing run identity')
    expected=PAYLOADS|{PACKAGE+'/SOURCE_FILES.json'}
    actual=set(git('ls-tree','-r','--name-only',head,'--',PACKAGE).splitlines())|{WORKFLOW}
    require(actual==expected,'tracked membership')
    ids={}
    for name in sorted(expected):
        path=ROOT/name
        require(not any(p.is_symlink() for p in (path,*path.parents)),'symlink source')
        ids[name]=identity(path.read_bytes())
        require(git('rev-parse',head+':'+name)==ids[name]['git_blob'],'dirty source: '+name)
        if name in PAYLOADS:require(meta['files'][name]==ids[name],'source identity: '+name)
    helper_id=identity((ROOT/CORE_IDENTITY_PATH).read_bytes())
    require(git('rev-parse',head+':'+CORE_IDENTITY_PATH)==helper_id['git_blob'],'dirty core identity validator')
    ids[CORE_IDENTITY_PATH]=helper_id
    git('diff','--exit-code','HEAD','--','formal',PACKAGE,WORKFLOW,CORE_IDENTITY_PATH)
    return {'checked_commit':head,'repository':REPO,'run_id':os.environ.get('GITHUB_RUN_ID','local'),
       'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local'),'core_tree':CORE_TREE,
       'sources':ids,'declarations':list(TARGETS),'scientific_effect':'NONE'}

def types(text):
    require('error:' not in text and 'warning:' not in text,'type diagnostic')
    matches=list(re.finditer(r'^D2SquareSchur\.[A-Za-z][A-Za-z0-9_]*',text,re.M))
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
    (out/'Audit.lean').write_text('import D2SquareSchur\n'+'\n'.join('#print axioms '+n for n in TARGETS)+'\n')
    (out/'Types.lean').write_text('import D2SquareSchur\nset_option pp.explicit true\n'+'\n'.join('#check '+n for n in TARGETS)+'\n')
    expressions={
      'RejectSignedWeights':'(-2 : ℝ) * 1 / (-2 + 1) * (0 - 1)^2 ≤ (-2) * (0 - 2)^2 + 1 * (1 - 2)^2',
      'RejectEndpointMaximum':'max (2 - (1 : ℝ)^2) (2 * 1^2) ≤ d2Schur 1 2 0',
      'RejectOutsideDirection':'min (2 - (1 : ℝ)^2) (2 * 1^2) ≤ d2Schur 1 2 1'}
    for label,statement in expressions.items():
        (out/(label+'.lean')).write_text('import D2SquareSchur\nopen ResearchFormalCoreR1\nexample : '+statement+' := by\n  norm_num [d2Schur, d2Alpha, d2Gamma, d2DetV]\n')

LEAN_VERSION=re.compile(r'Lean \(version 4\.34\.1, [^()\r\n]+, commit 5045d0056413266e57c625dcd7c365b10e377c52, Release\)')


def final_runtime(out,core,lock):
    """The companion's own Lean runs follow the core gate, so the core's observations do not cover them.
    replay.sh observes the runtime and the dependencies again after the companion's last Lean execution;
    both must equal the core gate's equal preflight and final observations, the exact release and the lock."""
    version=core.get('lean_version')
    require(isinstance(version,str) and LEAN_VERSION.fullmatch(version) is not None,'core receipt runtime is not the pinned release')
    obs=core.get('observations')
    require(isinstance(obs,dict) and set(obs)=={'preflight','final'} and isinstance(obs['final'],dict) and obs['final']==obs['preflight'],
            'core receipt lacks equal preflight and final observations')
    require(obs['final'].get('lean_version')==version and obs['final'].get('dependency_revisions')==lock
            and obs['final'].get('dependency_worktrees')=='CLEAN','core final observation differs from the lock')
    for name in ('toolchain.log','toolchain-final.log'):
        require((out/name).is_file() and (out/name).read_text()==version+'\n','companion runtime differs from the core gate: '+name)
    require((out/'packages-final.log').is_file(),'missing final dependency observation')
    seen={}
    for line in (out/'packages-final.log').read_text().splitlines():
        parts=line.split(' ')
        require(len(parts)==3 and parts[0] not in seen,'malformed final dependency record')
        seen[parts[0]]=(parts[1],parts[2])
    require(set(seen)==set(lock),'final dependency set differs from the lock')
    for name,(head,state) in sorted(seen.items()):
        require(head==lock[name],'final dependency HEAD differs from the lock: '+name)
        require(state=='clean','final dependency worktree is not clean: '+name)
    return {'lean_version':version,'dependency_revisions':dict(sorted(lock.items())),'dependency_worktrees':'CLEAN'}


def finish(out):
    current=source();require(strict((out/'source.json').read_bytes())==current,'source changed during execution')
    ax=core_gate().audit_axioms((out/'axioms.log').read_text(),list(TARGETS))
    types((out/'types.log').read_text())
    for label in ('build','contract','axioms','types','leanchecker'):
        require((out/(label+'.status')).read_bytes()==b'0\n','unsuccessful process: '+label)
    for label in CONTROLS:
        require((out/(label+'.status')).read_bytes()==b'1\n','negative status: '+label)
        negative((out/(label+'.log')).read_text(),label,1)
    raw=(ROOT/'formal/.lake/formal-evidence/receipt.json').read_bytes();core=strict(raw)
    validate_core_receipt(core,current)
    final=final_runtime(out,core,strict((ROOT/'formal/manifest.json').read_bytes())['dependency_revisions'])
    result={**current,'axioms':ax,'theorem_count':4,'definition_count':0,'core_receipt_sha256':sha(raw),'final_observation':final,
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
