"""Replay exact algebra and byte custody; --local-only excludes source Git objects."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

IDS={'E','C'}
MUTANTS=('all-doublets-finite','wrong-shape-normalization','retain-exponent13',
         'lose-ratio-jacobian','wrong-height-ratio','lose-moment-crossover')


def read_json(path):
    if path.is_symlink() or not path.is_file():raise ValueError('regular JSON file required')
    def unique(pairs):
        out={}
        for key,value in pairs:
            if key in out:raise ValueError('duplicate JSON key')
            out[key]=value
        return out
    value=json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    if not isinstance(value,dict):raise ValueError('JSON object required')
    return value


def path_parts(path):
    if not isinstance(path,str) or not path:raise ValueError('nonempty path required')
    p=PurePosixPath(path)
    if p.is_absolute() or str(p)!=path or any(x in ('.','..') or not re.fullmatch('[A-Za-z0-9_.-]+',x) for x in p.parts):
        raise ValueError('unsafe or noncanonical path')
    return p.parts


def identity(data,entry):
    if type(entry.get('bytes')) is not int or entry['bytes']!=len(data):raise ValueError('missing or incorrect source size')
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if entry.get('git_blob')!=blob or entry.get('sha256')!=hashlib.sha256(data).hexdigest():
        raise ValueError('identity mismatch: '+entry['path'])


def git(root,*args):
    run=subprocess.run(['git','--no-replace-objects',*args],cwd=root,
                       env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'),
                       capture_output=True,timeout=45)
    if run.returncode:raise ValueError('Git object read failed: '+run.stderr.decode(errors='replace')[:160])
    return run.stdout


def sources(root):
    entries=read_json(root/'SOURCES.json')['sources']
    if not isinstance(entries,list) or len(entries)!=len(IDS) or {e['id'] for e in entries}!=IDS:
        raise ValueError('source inventory mismatch')
    seen=set()
    for e in entries:
        ps=path_parts(e['path']);commit=e['commit']
        if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('full commit required')
        key=(commit,e['path'])
        if key in seen:raise ValueError('duplicate source binding')
        seen.add(key)
        if git(root,'cat-file','-t',commit).strip()!=b'commit':raise ValueError('source object is not a commit')
        for j in range(1,len(ps)+1):
            prefix='/'.join(ps[:j])
            records=[x for x in git(root,'ls-tree','--full-tree','-z',commit,'--',prefix).split(b'\0') if x]
            if len(records)!=1:raise ValueError('missing or ambiguous source path')
            meta,name=records[0].split(b'\t',1);mode,kind,blob=meta.decode().split()
            if name.decode()!=prefix:raise ValueError('source path mismatch')
            if j<len(ps) and (mode,kind)!=('040000','tree'):raise ValueError('non-tree source ancestor')
            if j==len(ps) and (kind!='blob' or mode not in ('100644','100755')):raise ValueError('nonregular source file')
        if blob!=e.get('git_blob'):raise ValueError('source tree/blob mismatch')
        identity(git(root,'cat-file','blob',blob),e)
    return len(entries)


def inventory(root):
    if not root.is_dir() or any(p.is_symlink() for p in (root,*root.parents)):raise ValueError('nonregular packet directory')
    entries=read_json(root/'MANIFEST.json')['files'];names=[e['path'] for e in entries]
    if not names or len(names)!=len(set(names)) or 'MANIFEST.json' in names:raise ValueError('invalid packet inventory')
    if sorted(x.name for x in root.iterdir())!=sorted(names+['MANIFEST.json']):raise ValueError('packet membership mismatch')
    for e in entries:
        p=root/e['path']
        if len(path_parts(e['path']))!=1 or p.is_symlink() or not p.is_file():raise ValueError('regular flat file required')
        identity(p.read_bytes(),e)
    return len(entries)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-only',action='store_true');args=parser.parse_args()
    root=Path(__file__).absolute().parent;inventory(root)
    source_count=0 if args.local_only else sources(root)
    expected=(root/'RESULTS.json').read_bytes()
    for flags in (['-B','-S'],['-B','-O','-S']):
        subprocess.run([sys.executable,*flags,'-m','unittest','discover','-v'],cwd=root,check=True,timeout=120)
        command=[sys.executable,*flags,str(root/'shape.py')]
        run=subprocess.run(command,capture_output=True,check=True,timeout=45)
        if run.stdout!=expected or run.stderr:raise ValueError('deterministic replay mismatch')
        for name in (*MUTANTS,'unknown'):
            run=subprocess.run(command+['--mutant',name],capture_output=True,timeout=45)
            if run.returncode!=(2 if name=='unknown' else 1):raise ValueError('negative control not rejected: '+name)
    inventory(root)
    print(json.dumps({'passed':True,'source_pins_checked':not args.local_only,
                      'source_count':source_count,'mathematical_acceptance':False,
                      'scientific_effect':'NONE'},sort_keys=True))

if __name__=='__main__':main()
