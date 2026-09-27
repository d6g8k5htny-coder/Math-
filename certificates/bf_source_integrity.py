"""Verify two frozen BF source manifests and their ten files, without network.

Manifests bind historical commit1ec186...; hashes do not establish mathematics.
The trusted verifier pins manifest digests; its code is a separate review input.
No current Git HEAD equality or live remote permission claim is made.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

MANIFEST_SHA256 = {'bf_six_pin_scalar_20260926': '25288c80c8ed66390f903dfb39b056e91a03ed0ba11fb26f84942e1d71062e62', 'bf_six_pin_hessian_20260926': 'a0e675733baa7fd3e1bf53be2f18664e72836903b07622970cf8c174510f472c'}
SOURCE_COMMIT='1ec186bb529d36b90d498d34063b0bd4c022639a'
ROOT=Path(__file__).resolve().parents[1]

def read_regular(path:Path,limit:int)->bytes:
    if path.is_symlink() or not path.is_file():raise ValueError('not a regular non-symlink source: '+str(path))
    with path.open('rb') as stream:raw=stream.read(limit+1)
    if len(raw)>limit:raise ValueError('source exceeds byte limit: '+str(path))
    return raw

def verify(root:Path)->dict:
    root=Path(root)
    if root.is_symlink() or not root.is_dir():raise ValueError('invalid verification root')
    parent=root/'certificates'
    if parent.is_symlink() or not parent.is_dir():raise ValueError('invalid certificates directory')
    count=0
    for name,digest in MANIFEST_SHA256.items():
        folder=parent/name
        if folder.is_symlink() or not folder.is_dir():raise ValueError('invalid package directory')
        raw=read_regular(folder/'SOURCE_MANIFEST.json',16384)
        if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('frozen source manifest changed: '+name)
        data=json.loads(raw)
        if data['source_commit']!=SOURCE_COMMIT or data['package_path']!='certificates/'+name:raise ValueError('source attribution mismatch')
        for row in data['files']:
            # Manifest has already matched its frozen digest. Still reject unsafe names.
            filename=row['path']
            if not isinstance(filename,str) or filename in ('.','..') or '/' in filename or '\\' in filename:raise ValueError('unsafe source filename')
            payload=read_regular(folder/filename,row['bytes'])
            blob=hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()
            if len(payload)!=row['bytes'] or hashlib.sha256(payload).hexdigest()!=row['sha256'] or blob!=row['git_blob']:raise ValueError('source identity mismatch: '+name+'/'+filename)
            count+=1
    if count!=10:raise ValueError('source coverage mismatch')
    return {'source_commit':SOURCE_COMMIT,'packages':sorted(MANIFEST_SHA256),'source_files':count,'scientific_effect':'NONE','scientific_acceptance':False,'meaning':'frozen source identities only; not theorem acceptance or remote commit verification'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);args=p.parse_args()
    print(json.dumps(verify(args.root),indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print('REFUSED: '+str(exc),file=sys.stderr);sys.exit(1)
