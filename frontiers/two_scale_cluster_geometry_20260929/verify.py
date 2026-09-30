"""Fail-closed local packet and historical Git-source verification.

Default replay verifies all six declared project source objects. --local-only
excludes those objects explicitly; real local Git fixtures still test the code.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

SOURCE_IDS = frozenset(('SC','CUB','RM','C6','P','D5'))
MUTANTS = ('omit-jet-factor-two','omit-z-reflection','power-ten','wrong-cusp',
           'height-reversed','wrong-window','wrong-k-power','half-root-jacobian')


def read_json(path):
    path=Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('regular JSON source required: '+str(path))
    def unique(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('duplicate JSON key: '+key)
            result[key]=value
        return result
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)


def safe_path(path):
    if not isinstance(path,str) or not path or '\\' in path or '\0' in path:
        raise ValueError('unsafe path')
    pure=PurePosixPath(path)
    if pure.is_absolute() or str(pure)!=path or any(p in ('.','..') for p in path.split('/')):
        raise ValueError('unsafe path: '+path)
    return pure


def identity(data,entry):
    expected_bytes=entry['bytes']
    if type(expected_bytes) is not int or expected_bytes<0:
        raise ValueError('invalid source size')
    sha=hashlib.sha256(data).hexdigest()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if len(data)!=expected_bytes or sha!=entry['sha256'] or blob!=entry['git_blob']:
        raise ValueError('identity mismatch: '+entry['path'])


def git(root,*args):
    return subprocess.run(['git',*args],cwd=root,check=True,capture_output=True,
                          timeout=60).stdout


def tree_entry(root,commit,path):
    # --full-tree is essential: callers run from a NESTED packet directory.
    data=git(root,'ls-tree','-z','--full-tree',commit,'--',path)
    records=[r for r in data.split(b'\0') if r]
    if len(records)!=1:raise ValueError('missing or ambiguous source: '+path)
    header,found=records[0].split(b'\t',1)
    mode,kind,blob=header.decode('ascii').split()
    if found.decode('utf-8')!=path:raise ValueError('source path substitution')
    return mode,kind,blob


def verify_source_entry(root,entry):
    commit=entry['commit'];path=entry['path'];pure=safe_path(path)
    if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):
        raise ValueError('immutable forty-hex commit required')
    for length in range(1,len(pure.parts)):
        prefix='/'.join(pure.parts[:length])
        mode,kind,blob=tree_entry(root,commit,prefix)
        if mode!='040000' or kind!='tree':raise ValueError('non-tree source ancestor')
    mode,kind,blob=tree_entry(root,commit,path)
    if mode not in ('100644','100755') or kind!='blob':
        raise ValueError('regular Git blob required: '+path)
    if blob!=entry['git_blob']:raise ValueError('Git tree/blob identity mismatch: '+path)
    identity(git(root,'cat-file','blob',blob),entry)


def verify_sources(root):
    entries=read_json(root/'SOURCES.json')['sources']
    if not isinstance(entries,list) or len(entries)!=len(SOURCE_IDS):
        raise ValueError('six source entries required')
    ids=[e['id'] for e in entries]
    if len(set(ids))!=len(ids) or set(ids)!=SOURCE_IDS:
        raise ValueError('missing, duplicate or unexpected source identity')
    for entry in entries:verify_source_entry(root,entry)
    return len(entries)


def verify_inventory(root):
    entries=read_json(root/'MANIFEST.json')['files']
    if not isinstance(entries,list) or not entries:raise ValueError('empty packet inventory')
    names=[e['path'] for e in entries]
    if len(set(names))!=len(names) or 'MANIFEST.json' in names:
        raise ValueError('duplicate or self-referential packet inventory')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):
        raise ValueError('packet inventory mismatch')
    for entry in entries:
        pure=safe_path(entry['path'])
        path=root/entry['path']
        if len(pure.parts)!=1 or path.is_symlink() or not path.is_file():
            raise ValueError('flat regular packet leaf required')
        identity(path.read_bytes(),entry)
    return len(entries)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-only',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    count=verify_inventory(root)
    source_count=0 if args.local_only else verify_sources(root)
    expected=(root/'RESULTS.json').read_bytes()
    for flags in (['-B','-S'],['-B','-O','-S']):
        subprocess.run([sys.executable,*flags,'-m','unittest','discover','-v'],cwd=root,
                       check=True,timeout=120)
        command=[sys.executable,*flags,str(root/'geometry.py')]
        result=subprocess.run(command,check=True,capture_output=True,timeout=60)
        if result.stdout!=expected or result.stderr:
            raise ValueError('deterministic checker output mismatch')
        for mutant in MUTANTS+('unknown',):
            result=subprocess.run(command+['--mutant',mutant],capture_output=True,timeout=60)
            if result.returncode!=(2 if mutant=='unknown' else 1):
                raise ValueError('negative control not rejected: '+mutant)
    verify_inventory(root)
    print(json.dumps({'passed':True,'packet_leaves':count,'source_count':source_count,
                      'source_pins_checked':not args.local_only,'scientific_effect':'NONE',
                      'mathematical_acceptance':False},sort_keys=True))


if __name__=='__main__':main()
