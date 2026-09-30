"""Verify packet identities and exact controls; default includes project Git sources."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


def read_json(path):
    def unique(pairs):
        ans = {}
        for k,v in pairs:
            if k in ans: raise ValueError('duplicate JSON key: '+k)
            ans[k] = v
        return ans
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def identity(data, entry):
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if (len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']
            or blob!=entry['git_blob']):
        raise ValueError('identity mismatch: '+entry['path'])


def verify_sources(root):
    entries = read_json(root/'SOURCES.json')['sources']
    ids = [e['id'] for e in entries]
    if not entries or len(ids)!=len(set(ids)): raise ValueError('invalid source inventory')
    for e in entries:
        commit,path=e['commit'],e['path']
        p=PurePosixPath(path)
        if not re.fullmatch('[0-9a-f]{40}',commit) or not path or p.is_absolute() or '..' in p.parts:
            raise ValueError('unsafe source identity')
        data=subprocess.run(['git','show',commit+':'+path],cwd=root,check=True,
                            capture_output=True,timeout=60).stdout
        identity(data,e)


def verify_inventory(root):
    entries=read_json(root/'MANIFEST.json')['files']
    names=[e['path'] for e in entries]
    if len(names)!=len(set(names)): raise ValueError('duplicate packet path')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):
        raise ValueError('packet inventory mismatch')
    for e in entries:
        path=root/e['path']
        if PurePosixPath(e['path']).name!=e['path'] or path.is_symlink() or not path.is_file():
            raise ValueError('flat regular file required')
        identity(path.read_bytes(),e)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-only',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    verify_inventory(root)
    if not args.local_only: verify_sources(root)
    expected=(root/'RESULTS.json').read_bytes()
    mutants=['omit-shear','omit-cubic-shear','close-window','swap-weight-sign',
             'claim-three','drop-jet-jacobian','restrict-normalizer','lose-linear-case']
    for flags in (['-B','-S'],['-B','-O','-S']):
        subprocess.run([sys.executable,*flags,'-m','unittest','discover','-v'],cwd=root,
                       check=True,timeout=120)
        command=[sys.executable,*flags,str(root/'cubic.py')]
        result=subprocess.run(command,capture_output=True,check=True,timeout=30)
        if result.stdout!=expected: raise ValueError('deterministic output mismatch')
        for name in mutants+['unknown']:
            result=subprocess.run(command+['--mutant',name],capture_output=True,timeout=30)
            if result.returncode!=(2 if name=='unknown' else 1):
                raise ValueError('negative control not rejected: '+name)
    print(json.dumps({'passed':True,'source_pins_checked':not args.local_only,
                      'scientific_effect':'NONE','mathematical_acceptance':False},sort_keys=True))


if __name__=='__main__': main()
