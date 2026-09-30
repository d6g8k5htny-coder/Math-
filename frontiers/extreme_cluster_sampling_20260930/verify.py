"""Fail-closed packet replay and historical source authentication, stdlib only.

Default verification requires the real project Git source commits. --local-only
skips project source authentication explicitly; real isolated Git regressions
still run. No mode confers mathematical acceptance.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

SOURCE_IDS=frozenset({'RADIAL','MICRO','SC','CUB'})
HEX40=re.compile(r'[0-9a-f]{40}\Z')
HEX64=re.compile(r'[0-9a-f]{64}\Z')
MUTANTS=('drop-companion-sign','point-is-cluster','close-window','drop-log2',
         'double-count-inner','lose-height-jacobian','wrong-tail-power',
         'uniform-cluster-from-point')


def no_symlinks(path: Path) -> Path:
    """Check spelling before resolve; a symlinked ancestor must not disappear."""
    path=Path(os.path.abspath(path))
    for p in (path,*path.parents):
        if p.is_symlink(): raise ValueError('symlink prohibited: '+str(p))
    return path


def read_json(path: Path) -> dict:
    path=no_symlinks(path)
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result: raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    obj=json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)
    if not isinstance(obj,dict): raise ValueError('JSON object required: '+str(path))
    return obj


def source_path(text: str) -> PurePosixPath:
    if not isinstance(text,str) or not text or '\\' in text or '\0' in text:
        raise ValueError('invalid path')
    p=PurePosixPath(text)
    if p.is_absolute() or '..' in p.parts or str(p)!=text or str(p)=='.':
        raise ValueError('noncanonical source path: '+text)
    return p


def check_identity(data: bytes, entry: dict) -> None:
    if not isinstance(entry,dict): raise ValueError('identity entry must be an object')
    size=entry.get('bytes'); sha=entry.get('sha256'); blob=entry.get('git_blob')
    if type(size) is not int or size<0 or not isinstance(sha,str) or not HEX64.fullmatch(sha):
        raise ValueError('invalid size/hash metadata')
    if not isinstance(blob,str) or not HEX40.fullmatch(blob): raise ValueError('invalid blob identity')
    actual_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if len(data)!=size or hashlib.sha256(data).hexdigest()!=sha or actual_blob!=blob:
        raise ValueError('identity mismatch: '+str(entry.get('path')))


def git(root: Path, *args: str) -> bytes:
    env=os.environ.copy()
    for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY',
                'GIT_ALTERNATE_OBJECT_DIRECTORIES','GIT_NAMESPACE'):
        env.pop(key,None)
    env['GIT_NO_REPLACE_OBJECTS']='1'
    command=['git','--no-replace-objects','--literal-pathspecs',*args]
    try:
        return subprocess.run(command,cwd=root,env=env,capture_output=True,
                              check=True,timeout=60).stdout
    except (subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc:
        raise ValueError('Git authentication failed: '+' '.join(args)) from exc


def verify_sources(root: Path, required_ids=None) -> int:
    root=no_symlinks(root)
    required=SOURCE_IDS if required_ids is None else frozenset(required_ids)
    entries=read_json(root/'SOURCES.json').get('sources')
    if not isinstance(entries,list) or not entries or not required:
        raise ValueError('nonempty exact source inventory required')
    ids=[]; paths=[]
    for entry in entries:
        if not isinstance(entry,dict) or not isinstance(entry.get('id'),str):
            raise ValueError('invalid source entry')
        ids.append(entry['id'])
        commit=entry.get('commit'); path=entry.get('path')
        if not isinstance(commit,str) or not HEX40.fullmatch(commit):
            raise ValueError('literal full commit identity required')
        p=source_path(path); paths.append((commit,path))
        # Reject tree/blob/annotated-tag objects, rather than peeling them.
        if git(root,'cat-file','-t',commit)!=b'commit\n':
            raise ValueError('declared source object is not a commit')
        for count in range(1,len(p.parts)+1):
            prefix='/'.join(p.parts[:count])
            raw=git(root,'ls-tree','--full-tree','-z',commit,'--',prefix)
            records=[record for record in raw.split(b'\0') if record]
            if len(records)!=1: raise ValueError('missing/ambiguous source path: '+prefix)
            try:
                header,name=records[0].split(b'\t',1)
                mode,kind,object_sha=header.split()
            except ValueError as exc: raise ValueError('malformed Git tree record') from exc
            if name.decode('utf-8')!=prefix: raise ValueError('Git path mismatch')
            if count<len(p.parts):
                if (mode,kind)!=(b'040000',b'tree'):
                    raise ValueError('non-tree source ancestor: '+prefix)
            else:
                if mode not in (b'100644',b'100755') or kind!=b'blob':
                    raise ValueError('source must be a regular file: '+prefix)
                if object_sha.decode()!=entry.get('git_blob'):
                    raise ValueError('source path/blob mismatch: '+prefix)
                check_identity(git(root,'cat-file','blob',object_sha.decode()),entry)
    if len(ids)!=len(set(ids)) or set(ids)!=required or len(paths)!=len(set(paths)):
        raise ValueError('missing, duplicate or unexpected source identity')
    return len(entries)


def verify_inventory(root: Path) -> int:
    root=no_symlinks(root)
    entries=read_json(root/'MANIFEST.json').get('files')
    if not isinstance(entries,list) or not entries: raise ValueError('empty packet inventory')
    names=[]
    for entry in entries:
        if not isinstance(entry,dict): raise ValueError('invalid packet identity')
        text=entry.get('path'); p=source_path(text)
        if len(p.parts)!=1 or text=='MANIFEST.json': raise ValueError('flat packet leaf required')
        names.append(text)
        path=no_symlinks(root/text)
        if not path.is_file(): raise ValueError('missing regular packet file: '+text)
        check_identity(path.read_bytes(),entry)
    if len(names)!=len(set(names)): raise ValueError('duplicate packet path')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):
        raise ValueError('complete packet inventory mismatch')
    return len(entries)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-only',action='store_true')
    args=parser.parse_args()
    root=no_symlinks(Path(__file__).absolute().parent)
    verify_inventory(root)
    n_sources=0 if args.local_only else verify_sources(root)
    expected=(root/'RESULTS.json').read_bytes()
    for flags in (['-B','-S'],['-B','-O','-S']):
        subprocess.run([sys.executable,*flags,'-m','unittest','discover','-v'],
                       cwd=root,check=True,timeout=180)
        command=[sys.executable,*flags,str(root/'extremes.py')]
        result=subprocess.run(command,cwd=root,capture_output=True,check=True,timeout=60)
        if result.stdout!=expected or result.stderr:
            raise ValueError('deterministic mathematical output mismatch')
        for name in MUTANTS+('unknown',):
            result=subprocess.run(command+['--mutant',name],cwd=root,
                                  capture_output=True,timeout=60)
            if result.returncode!=(2 if name=='unknown' else 1):
                raise ValueError('negative control did not reject: '+name)
    verify_inventory(root)
    print(json.dumps({'passed':True,'source_pins_checked':not args.local_only,
                      'source_count':n_sources,'scientific_effect':'NONE',
                      'mathematical_acceptance':False},sort_keys=True))


if __name__=='__main__': main()
