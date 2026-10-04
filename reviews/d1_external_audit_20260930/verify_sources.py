"""Verify packet and historical source bytes; this never certifies their mathematics."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess

IDS = {'P','CAP','E1','E2','REC','R','R_REVIEW','SIDE24','REGION','FORMAL'}


def read_json(path):
    def unique(pairs):
        out={}
        for k,v in pairs:
            if k in out:raise ValueError('duplicate JSON key')
            out[k]=v
        return out
    if path.is_symlink() or not path.is_file():raise ValueError('regular JSON required')
    out=json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    if not isinstance(out,dict):raise ValueError('JSON object required')
    return out


def safe_path(path):
    if not isinstance(path,str) or not path:raise ValueError('path required')
    p=PurePosixPath(path)
    if p.is_absolute() or str(p)!=path or any(x in ('.','..') or not re.fullmatch('[A-Za-z0-9_.-]+',x) for x in p.parts):
        raise ValueError('unsafe source path')
    return p.parts


def git(root,*args):
    result=subprocess.run(['git','--no-replace-objects',*args],cwd=root,
        env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'),capture_output=True,timeout=45)
    if result.returncode:raise ValueError('historical Git object unavailable: '+result.stderr.decode(errors='replace')[:180])
    return result.stdout


def identity(data,entry):
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if blob!=entry['git_blob']:raise ValueError('Git blob mismatch: '+entry['path'])
    if 'bytes' in entry and (type(entry['bytes']) is not int or len(data)!=entry['bytes']):
        raise ValueError('size mismatch: '+entry['path'])
    if 'sha256' in entry and hashlib.sha256(data).hexdigest()!=entry['sha256']:
        raise ValueError('SHA256 mismatch: '+entry['path'])


def verify_bindings(root,commit,entries):
    if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('full commit required')
    if not entries or len({e['path'] for e in entries})!=len(entries):raise ValueError('nonempty unique inventory required')
    if git(root,'cat-file','-t',commit).strip()!=b'commit':raise ValueError('not a commit object')
    for entry in entries:
        ps=safe_path(entry['path'])
        for j in range(1,len(ps)+1):
            prefix='/'.join(ps[:j])
            rows=[x for x in git(root,'ls-tree','--full-tree','-z',commit,'--',prefix).split(b'\0') if x]
            if len(rows)!=1:raise ValueError('missing source path')
            meta,name=rows[0].split(b'\t',1);mode,kind,blob=meta.decode().split()
            if name.decode()!=prefix:raise ValueError('path mismatch')
            if j<len(ps) and (mode,kind)!=('040000','tree'):raise ValueError('non-tree ancestor')
            if j==len(ps) and (kind!='blob' or mode not in ('100644','100755')):raise ValueError('nonregular source')
        if blob!=entry['git_blob']:raise ValueError('historical tree/blob mismatch')
        identity(git(root,'cat-file','blob',blob),entry)
    return len(entries)


def verify_packet(root):
    entries=read_json(root/'MANIFEST.json')['files']
    names=[e['path'] for e in entries]
    if not names or len(names)!=len(set(names)) or 'MANIFEST.json' in names:raise ValueError('bad manifest')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):raise ValueError('packet membership drift')
    for entry in entries:
        path=root/entry['path']
        if len(safe_path(entry['path']))!=1 or path.is_symlink() or not path.is_file():raise ValueError('flat regular payload required')
        identity(path.read_bytes(),entry)
    return len(entries)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--local-only',action='store_true');args=ap.parse_args()
    root=Path(__file__).absolute().parent
    count=verify_packet(root)
    source=read_json(root/'SOURCES.json');entries=source['sources']
    if len(entries)!=len(IDS) or {e['id'] for e in entries}!=IDS:raise ValueError('source-set omission or duplicate')
    n=0 if args.local_only else verify_bindings(root,source['commit'],entries)
    print(json.dumps({'packet_files_checked':count,'source_bindings_checked':n,
        'historical_sources_checked':not args.local_only,'scientific_effect':'NONE',
        'full_D1_formal_verification':False},sort_keys=True))

if __name__=='__main__':main()
