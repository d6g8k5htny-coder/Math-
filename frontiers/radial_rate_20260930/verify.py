"""Exact packet replay; --local-only does not authenticate upstream Git sources."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

IDS={'R','SC','P'}
MUTANTS=('omit-shift','omit-density-term','drop-a-shear','odd-term-survives',
         'unsigned-is-signed','wrong-b-integral','wrong-density-factor','wrong-tv-root')


def read_json(path):
    if path.is_symlink() or not path.is_file():raise ValueError('regular JSON file required')
    def unique(pairs):
        ans={}
        for k,v in pairs:
            if k in ans:raise ValueError('duplicate JSON key')
            ans[k]=v
        return ans
    ans=json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    if not isinstance(ans,dict):raise ValueError('JSON object required')
    return ans


def path_parts(path):
    if not isinstance(path,str) or not path:raise ValueError('nonempty path required')
    p=PurePosixPath(path)
    if p.is_absolute() or str(p)!=path or any(x in ('.','..') or not re.fullmatch('[A-Za-z0-9_.-]+',x) for x in p.parts):
        raise ValueError('unsafe path')
    return p.parts


def identity(data,e):
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if type(e['bytes']) is not int or len(data)!=e['bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256'] or blob!=e['git_blob']:
        raise ValueError('identity mismatch: '+e['path'])


def git(root,*args):
    run=subprocess.run(['git','--no-replace-objects',*args],cwd=root,
                       env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'),capture_output=True,timeout=45)
    if run.returncode:raise ValueError('Git object read failed: '+run.stderr.decode(errors='replace')[:200])
    return run.stdout


def sources(root):
    es=read_json(root/'SOURCES.json')['sources']
    if not isinstance(es,list) or len(es)!=len(IDS) or {e['id'] for e in es}!=IDS:
        raise ValueError('missing, duplicate or unexpected source IDs')
    seen=set()
    for e in es:
        parts=path_parts(e['path']);commit=e['commit']
        if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('exact commit required')
        pair=(commit,e['path'])
        if pair in seen:raise ValueError('duplicate source binding')
        seen.add(pair)
        if git(root,'cat-file','-t',commit).strip()!=b'commit':raise ValueError('not a commit object')
        for j in range(1,len(parts)+1):
            prefix='/'.join(parts[:j]);records=git(root,'ls-tree','--full-tree','-z',commit,'--',prefix).split(b'\0')
            records=[x for x in records if x]
            if len(records)!=1:raise ValueError('missing or ambiguous source path')
            meta,name=records[0].split(b'\t',1);mode,kind,blob=meta.decode().split()
            if name.decode()!=prefix:raise ValueError('path mismatch')
            if j<len(parts) and (mode,kind)!=('040000','tree'):raise ValueError('non-tree ancestor')
            if j==len(parts) and (kind!='blob' or mode not in ('100644','100755')):raise ValueError('nonregular source')
        if blob!=e['git_blob']:raise ValueError('source tree/blob mismatch')
        identity(git(root,'cat-file','blob',blob),e)
    return len(es)


def inventory(root):
    if not root.is_dir() or any(p.is_symlink() for p in (root,*root.parents)):raise ValueError('symlink packet path')
    es=read_json(root/'MANIFEST.json')['files'];names=[e['path'] for e in es]
    if not names or len(names)!=len(set(names)) or 'MANIFEST.json' in names:raise ValueError('bad packet inventory')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):raise ValueError('packet membership mismatch')
    for e in es:
        p=root/e['path']
        if len(path_parts(e['path']))!=1 or p.is_symlink() or not p.is_file():raise ValueError('regular flat payload required')
        identity(p.read_bytes(),e)
    return len(es)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--local-only',action='store_true');args=parser.parse_args()
    root=Path(__file__).absolute().parent;inventory(root)
    nsource=0 if args.local_only else sources(root)
    expected=(root/'RESULTS.json').read_bytes()
    for flags in (['-B','-S'],['-B','-O','-S']):
        subprocess.run([sys.executable,*flags,'-m','unittest','discover','-v'],cwd=root,check=True,timeout=120)
        command=[sys.executable,*flags,str(root/'rate.py')]
        run=subprocess.run(command,capture_output=True,check=True,timeout=45)
        if run.stdout!=expected or run.stderr:raise ValueError('deterministic replay mismatch')
        for mutant in (*MUTANTS,'unknown'):
            run=subprocess.run(command+['--mutant',mutant],capture_output=True,timeout=45)
            if run.returncode!=(2 if mutant=='unknown' else 1):raise ValueError('negative control not rejected: '+mutant)
    inventory(root)
    print(json.dumps({'passed':True,'source_count':nsource,'source_pins_checked':not args.local_only,
                      'mathematical_acceptance':False,'scientific_effect':'NONE'},sort_keys=True))

if __name__=='__main__':main()
