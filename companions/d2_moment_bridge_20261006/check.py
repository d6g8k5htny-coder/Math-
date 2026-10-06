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
CORE_TREE='d7422c6b1acbf3e20c75a1ed7fc13fc30125ec14'
CORE_MANIFEST='5d7ccdb0885af7bf4a2aa6ec4dce5f5c41435bb10a0a7a426a8af286d4f035e4'
CORE_GATE='958b149ea3a4ce735644a2079f817b5deddf5dc0d5ca347904ad09db6ad47d68'
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


def source():
    meta=metadata();head=git('rev-parse','HEAD')
    require(re.fullmatch(r'[0-9a-f]{40}',head),'invalid HEAD')
    require(meta['core_tree']==CORE_TREE and meta['scientific_effect']=='NONE','source scope')
    require(git('rev-parse',head+':formal')==CORE_TREE,'core tree changed; new source review required')
    require(sha((ROOT/'formal/manifest.json').read_bytes())==CORE_MANIFEST,'core manifest changed')
    require(sha((ROOT/'formal/gate.py').read_bytes())==CORE_GATE,'core verifier changed')
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
    git('diff','--exit-code','HEAD','--','formal',PACKAGE,WORKFLOW)
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
    require(receipt['checked_commit']==current['checked_commit'],'core executed different source')
    require(receipt['manifest_sha256']==CORE_MANIFEST,'core receipt manifest')
    require(receipt['formalization_status']=='kernel-checked','no core kernel receipt')
    result={**current,'axioms':ax,'theorem_count':len(metadata()['theorems']),
      'definition_count':len(metadata()['definitions']),'core_receipt_sha256':sha(raw),
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
