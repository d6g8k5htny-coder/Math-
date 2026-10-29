#!/usr/bin/env python3
"""Source-bound companion evidence, not an acceptance engine or a general Lean parser."""
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
PACKAGE='companions/d2_moment_bridge_20261006'
WORKFLOW='.github/workflows/d2-moment-bridge.yml'
CORE_TREE='c506a5ff25864023a57369a5a9f0f55046283905'
CORE_MANIFEST='ba7d11e43574e39da3c759e0501399a6dcd1b7da32b157a4a6b01f5c133b3062'
CORE_GATE='c532ac880f31545199d3034fac19ccc79a6b23e514aa4a6543b9f5fbc6cb8952'

CORE_SOURCE_IDENTITY='3cfc23e4b595a31a6a7e7e0bd964973c42e4c33c0f8008a38383f6cfb6210800'
CORE_IDENTITY_PATH='tools/required_formal_check.py'
CORE_IDENTITY_SHA256='6c27355237b45d3999298522c141984ff5b7c114f18b3c555cc45989976fc6dc'
CORE_IDENTITY_BLOB='0b9d694bdf888c75826ca07ae176c5a5c43b8880'
REPO='d6g8k5htny-coder/Math-'
CONTROLS=('RejectZeroAtom','RejectSameRadius')


def require(condition,message):
    if not condition:raise ValueError(message)


def sha(raw):return hashlib.sha256(raw).hexdigest()

def blob(raw):return hashlib.sha1(b'blob %d\0'%len(raw)+raw).hexdigest()

def strict(raw):
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'duplicate JSON key')
            result[k]=v
        return result
    def nonfinite(_):raise ValueError('nonfinite JSON')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=nonfinite)


def git(*args):
    return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()


def metadata():return strict((SIDE/'SOURCE_FILES.json').read_bytes())

def names(meta):
    result=['D2MomentBridge.'+n for n in meta['definitions']+meta['theorems']]
    require(result and len(result)==len(set(result)),'duplicate/empty declaration list')
    require(all(re.fullmatch(r'D2MomentBridge\.[A-Za-z][A-Za-z0-9_]*',n) for n in result),'invalid declaration')
    return result


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
    require(re.fullmatch(r'[0-9a-f]{40}',head),'invalid HEAD')
    require(meta['core_tree']==CORE_TREE and meta['scientific_effect']=='NONE','source scope')
    require(git('rev-parse',head+':formal')==CORE_TREE,'core tree changed; new source review required')
    require(sha((ROOT/'formal/manifest.json').read_bytes())==CORE_MANIFEST,'core manifest changed')
    require(sha((ROOT/'formal/gate.py').read_bytes())==CORE_GATE,'core verifier changed')
    core_identity()
    if os.environ.get('GITHUB_ACTIONS')=='true':
        require(os.environ.get('GITHUB_SHA')==head and os.environ.get('GITHUB_REPOSITORY')==REPO,'host/source mismatch')
        require(os.environ.get('GITHUB_RUN_ID') and os.environ.get('GITHUB_RUN_ATTEMPT'),'run identity absent')
    expected=set(meta['files'])|{PACKAGE+'/SOURCE_FILES.json'}
    actual=set(git('ls-tree','-r','--name-only',head,'--',PACKAGE).splitlines())|{WORKFLOW}
    require(actual==expected,'tracked companion membership')
    ids={}
    for path in sorted(expected):
        require(path.startswith(PACKAGE+'/') or path==WORKFLOW,'unexpected source path')
        p=ROOT/path
        require(not any((ROOT.joinpath(*Path(path).parts[:i])).is_symlink() for i in range(1,len(Path(path).parts)+1)),'symlink source')
        raw=p.read_bytes();bid=blob(raw)
        require(git('rev-parse',head+':'+path)==bid,'dirty execution/source bytes: '+path)
        if path in meta['files']:
            require(meta['files'][path]=={'bytes':len(raw),'sha256':sha(raw),'git_blob':bid},'manifest source mismatch: '+path)
        ids[path]={'sha256':sha(raw),'git_blob':bid,'bytes':len(raw)}
    helper_raw=(ROOT/CORE_IDENTITY_PATH).read_bytes()
    helper_blob=blob(helper_raw)
    require(git('rev-parse',head+':'+CORE_IDENTITY_PATH)==helper_blob,'dirty core identity validator')
    ids[CORE_IDENTITY_PATH]={'bytes':len(helper_raw),'sha256':sha(helper_raw),'git_blob':helper_blob}
    git('diff','--exit-code','HEAD','--','formal',PACKAGE,WORKFLOW,CORE_IDENTITY_PATH)
    return {'checked_commit':head,'repository':REPO,'run_id':os.environ.get('GITHUB_RUN_ID','local'),
            'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT','local'),'core_tree':CORE_TREE,
            'sources':ids,'declarations':names(meta),'scientific_effect':'NONE'}


def core_gate():
    path=ROOT/'formal/gate.py'
    require(sha(path.read_bytes())==CORE_GATE,'core verifier changed')
    spec=importlib.util.spec_from_file_location('bound_core_gate',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def types(text,targets):
    require('error:' not in text and 'warning:' not in text,'type diagnostic')
    matches=list(re.finditer(r'^D2MomentBridge\.[A-Za-z][A-Za-z0-9_]*',text,re.M))
    actual=[m.group() for m in matches]
    require(actual==targets and len(set(actual))==len(actual),'type inventory mismatch')
    require(not text[:matches[0].start()].strip(),'unrecognized type preamble')
    return actual


def negative(text,control,status):
    require(control in CONTROLS,'unknown negative control')
    require(type(status) is int and status==1,'negative exit must be exactly one')
    pattern=r'(?:[^\r\n]*[/\\])?'+control+r'\.lean:[0-9]+:[0-9]+: error: unsolved goals\s*\n⊢ False\s*'
    require(re.fullmatch(pattern,text) is not None,'not the intended False-goal diagnostic')
    return control


def emit(out):
    target=names(metadata())
    (out/'Audit.lean').write_text('import D2MomentBridge\n'+'\n'.join('#print axioms '+n for n in target)+'\n')
    (out/'Types.lean').write_text('import D2MomentBridge\nset_option pp.explicit true\n'+'\n'.join('#check '+n for n in target)+'\n')
    (out/'Positive.lean').write_text('''import D2MomentBridge
open D2MomentBridge ResearchFormalCoreR1
example (c x : ℝ) : cubicResidual c x = 0 ↔ x = 0 ∨ x ^ 2 = c :=
  cubicResidual_eq_zero_iff c x
example : cubicResidual 1 (0 : ℝ) = 0 := by norm_num [cubicResidual]
example : cubicResidual 1 (2 : ℝ) ≠ 0 := by norm_num [cubicResidual]
example : d2Delta (1 / 2) (1 / 2) (1 / 2) = 0 := zero_atom_counterexample.2
''')
    for name,statement in [
        ('RejectZeroAtom','(1 / 2 : ℝ) ^ 2 < 1 / 2 → 0 < d2Delta (1 / 2) (1 / 2) (1 / 2)'),
        ('RejectSameRadius','0 < d2Delta (1 : ℝ) 1 1')]:
        (out/(name+'.lean')).write_text('import D2MomentBridge\nopen ResearchFormalCoreR1\nexample : '+statement+' := by\n  norm_num [d2Delta]\n')


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
    initial=strict((out/'source.json').read_bytes());current=source()
    require(initial==current,'source changed across execution')
    target=names(metadata())
    ax=core_gate().audit_axioms((out/'axioms.log').read_text(),target)
    types((out/'types.log').read_text(),target)
    for control in CONTROLS:
        status=int((out/(control+'.status')).read_text())
        negative((out/(control+'.log')).read_text(),control,status)
    for label in ('build','positive','axioms','types','leanchecker'):
        require((out/(label+'.status')).read_text()=='0\n','missing successful process: '+label)
    core=ROOT/'formal/.lake/formal-evidence/receipt.json'
    raw=core.read_bytes();receipt=strict(raw)
    validate_core_receipt(receipt,current)
    final=final_runtime(out,receipt,strict((ROOT/'formal/manifest.json').read_bytes())['dependency_revisions'])
    result={**current,'axioms':ax,'theorem_count':len(metadata()['theorems']),
      'definition_count':len(metadata()['definitions']),'core_receipt_sha256':sha(raw),'final_observation':final,
      'formalization_status':'kernel-checked','alignment_status':'PENDING_INDEPENDENT_REVIEW',
      'scientific_acceptance':False,'log_sha256':{p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}}
    (out/'receipt.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=('source','emit','finish','negative'))
    ap.add_argument('path',type=Path,nargs='?')
    ap.add_argument('--control',choices=CONTROLS)
    ap.add_argument('--status',type=int)
    args=ap.parse_args()
    if args.command=='source':result=source()
    elif args.command=='emit':emit(args.path);result={'emitted':True}
    elif args.command=='finish':result=finish(args.path)
    else:result={'negative':negative(args.path.read_text(),args.control,args.status)}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':main()
