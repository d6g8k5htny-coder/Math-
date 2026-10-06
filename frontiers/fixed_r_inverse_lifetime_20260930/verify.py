"""Replay the fixed-r inverse-lifetime packet; --local-only excludes historical sources."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

IDS={'P'}
MUTANTS=('lose-determinant-weight','wrong-cubic-power','wrong-soft-direction',
         'admit-critical-inverse','drop-endpoint-margin','unconditional-tail-shortcut')


# Independent expectations from the unchanged inverse.py CLI, not the child under test.
REJECTIONS = {
    'lose-determinant-weight': 'retain original maximum determinant weight',
    'wrong-cubic-power': 'cubic lifetime scale',
    'wrong-soft-direction': 'correct Schur soft direction',
    'admit-critical-inverse': 'critical inverse moment diverges',
    'drop-endpoint-margin': 'strict endpoint above birth',
    'unconditional-tail-shortcut': 'retain weighted near-zero eigenvalue integral',
}


def validate_rejection(result, label):
    """Authenticate the entire failure carrier; only argparse wrapping is normalized."""
    if label not in (*REJECTIONS, 'unknown'):
        raise ValueError('unknown rejection stage')
    if type(result.returncode) is not int or result.returncode != (2 if label=='unknown' else 1):
        raise ValueError('wrong rejection exit: '+label)
    if not isinstance(result.stdout,bytes) or not isinstance(result.stderr,bytes):
        raise ValueError('binary process captures required')
    if label=='unknown':
        usage='usage: inverse.py [-h] [--mutant {' + ','.join(REJECTIONS) + '}]\n'
        prefix="inverse.py: error: argument --mutant: invalid choice: 'unknown' (choose from "
        # Python 3.11 quotes choices; 3.13 displays these string choices without quotes.
        # Both complete forms preserve every label, its order, the argument and the reason.
        expected=[(usage+prefix+choices+')\n').encode('ascii').split() for choices in
                  (', '.join(REJECTIONS), ', '.join(repr(key) for key in REJECTIONS))]
        if result.stdout or result.stderr.split() not in expected:
            raise ValueError('wrong unknown-label diagnostic')
        return
    if result.stderr:
        raise ValueError('unexpected mutant stderr: '+label)
    def unique(pairs):
        out={}
        for key,value in pairs:
            if key in out:raise ValueError('duplicate mutant JSON key')
            out[key]=value
        return out
    def finite_only(value):
        raise ValueError('nonfinite mutant JSON constant: '+value)
    report=json.loads(result.stdout.decode('utf-8'),
                      object_pairs_hook=unique,parse_constant=finite_only)
    if (type(report) is not dict or set(report)!={'passed','error'}
        or type(report['passed']) is not bool or report['passed'] is not False
        or type(report['error']) is not str or report['error']!=REJECTIONS[label]):
        raise ValueError('wrong complete mutant report: '+label)


def read_json(path):
    if path.is_symlink() or not path.is_file():raise ValueError('regular JSON required')
    def unique(pairs):
        out={}
        for k,v in pairs:
            if k in out:raise ValueError('duplicate JSON key')
            out[k]=v
        return out
    data=json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    if not isinstance(data,dict):raise ValueError('JSON object required')
    return data


def parts(path):
    if not isinstance(path,str) or not path:raise ValueError('nonempty path required')
    p=PurePosixPath(path)
    if p.is_absolute() or str(p)!=path or any(x in ('.','..') or not re.fullmatch('[A-Za-z0-9_.-]+',x) for x in p.parts):
        raise ValueError('unsafe or noncanonical path')
    return p.parts


def identity(data,e):
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if type(e['bytes']) is not int or len(data)!=e['bytes']:
        raise ValueError('size mismatch')
    if hashlib.sha256(data).hexdigest()!=e['sha256'] or blob!=e['git_blob']:
        raise ValueError('hash mismatch: '+e['path'])


def git(root,*args):
    run=subprocess.run(['git','--no-replace-objects',*args],cwd=root,
                       env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'),
                       capture_output=True,timeout=45)
    if run.returncode:raise ValueError('Git read failed: '+run.stderr.decode(errors='replace')[:160])
    return run.stdout


def sources(root):
    es=read_json(root/'SOURCES.json')['sources']
    if not isinstance(es,list) or len(es)!=len(IDS) or {e['id'] for e in es}!=IDS:
        raise ValueError('source inventory mismatch')
    seen=set()
    for e in es:
        path=e['path'];ps=parts(path);commit=e['commit']
        if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):
            raise ValueError('full commit identity required')
        if (commit,path) in seen:raise ValueError('duplicate source binding')
        seen.add((commit,path))
        if git(root,'cat-file','-t',commit).strip()!=b'commit':raise ValueError('not a commit object')
        for j in range(1,len(ps)+1):
            prefix='/'.join(ps[:j])
            rows=[s for s in git(root,'ls-tree','--full-tree','-z',commit,'--',prefix).split(b'\0') if s]
            if len(rows)!=1:raise ValueError('missing or ambiguous source path')
            meta,name=rows[0].split(b'\t',1);mode,kind,blob=meta.decode().split()
            if name.decode()!=prefix:raise ValueError('source path mismatch')
            if j<len(ps) and (mode,kind)!=('040000','tree'):raise ValueError('source ancestor not a tree')
            if j==len(ps) and (kind!='blob' or mode not in ('100644','100755')):raise ValueError('source not regular')
        if blob!=e['git_blob']:raise ValueError('source tree/blob mismatch')
        identity(git(root,'cat-file','blob',blob),e)
    return len(es)


def inventory(root):
    if not root.is_dir() or any(p.is_symlink() for p in (root,*root.parents)):
        raise ValueError('regular packet directory required')
    es=read_json(root/'MANIFEST.json')['files'];names=[e['path'] for e in es]
    if not names or len(names)!=len(set(names)) or 'MANIFEST.json' in names:
        raise ValueError('bad packet inventory')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):
        raise ValueError('packet membership mismatch')
    for e in es:
        p=root/e['path']
        if len(parts(e['path']))!=1 or p.is_symlink() or not p.is_file():raise ValueError('regular flat payload required')
        identity(p.read_bytes(),e)
    return len(es)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--local-only',action='store_true');args=ap.parse_args()
    if MUTANTS!=tuple(REJECTIONS):
        raise ValueError('complete ordered mutant inventory required')
    root=Path(__file__).absolute().parent;inventory(root)
    ns=0 if args.local_only else sources(root)
    expected=(root/'RESULTS.json').read_bytes()
    for flags in (['-B','-S'],['-B','-O','-S']):
        subprocess.run([sys.executable,*flags,'-m','unittest','discover','-v'],cwd=root,check=True,timeout=120)
        command=[sys.executable,*flags,str(root/'inverse.py')]
        run=subprocess.run(command,capture_output=True,check=True,timeout=45)
        if run.stdout!=expected or run.stderr:raise ValueError('baseline replay mismatch')
        for m in (*MUTANTS,'unknown'):
            run=subprocess.run(command+['--mutant',m],capture_output=True,timeout=45)
            validate_rejection(run,m)
    inventory(root)
    print(json.dumps({'passed':True,'source_count':ns,'source_pins_checked':not args.local_only,
                      'mathematical_acceptance':False,'scientific_effect':'NONE'},sort_keys=True))

if __name__=='__main__':main()
