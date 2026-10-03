"""Source identity only, not proof acceptance.

Path/commit/blob and flat-inventory helpers are reused from the c2 audit verifier
at a7421bbb / blob c6fb38bf91bf76f07c171b0120eb86ed18028513. The small caller
changes bind three distinct source interfaces at their own historical commits.
"""
import argparse,hashlib,json,os,re,subprocess
from pathlib import Path,PurePosixPath

def read_json(p):
    if p.is_symlink() or not p.is_file():raise ValueError('regular JSON required')
    def unique(items):
        d={}
        for k,v in items:
            if k in d:raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    out=json.loads(p.read_text(),object_pairs_hook=unique)
    if not isinstance(out,dict):raise ValueError('JSON object required')
    return out

def safe(path):
    if not isinstance(path,str) or not path:raise ValueError('path required')
    p=PurePosixPath(path)
    if p.is_absolute() or str(p)!=path or any(x in ('.','..') or not re.fullmatch('[A-Za-z0-9_.-]+',x) for x in p.parts):
        raise ValueError('unsafe path')
    return p.parts

def git(root,*args):
    r=subprocess.run(['git','--no-replace-objects',*args],cwd=root,env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'),
                     capture_output=True,timeout=30)
    if r.returncode:raise ValueError('historical Git read failed')
    return r.stdout

def read_source(root,commit,e):
    if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('full commit required')
    if git(root,'cat-file','-t',commit).strip()!=b'commit':raise ValueError('not a commit')
    parts=safe(e['path'])
    for j in range(1,len(parts)+1):
        path='/'.join(parts[:j]);rows=[x for x in git(root,'ls-tree','--full-tree','-z',commit,'--',path).split(b'\0') if x]
        if len(rows)!=1:raise ValueError('missing or ambiguous path')
        info,name=rows[0].split(b'\t',1);mode,kind,blob=info.decode().split()
        if name.decode()!=path:raise ValueError('path mismatch')
        if j<len(parts) and (mode,kind)!=('040000','tree'):raise ValueError('non-tree ancestor')
        if j==len(parts) and (kind!='blob' or mode not in ('100644','100755')):raise ValueError('nonregular file')
    if blob!=e['git_blob']:raise ValueError('blob mismatch')
    data=git(root,'cat-file','blob',blob)
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=blob:raise ValueError('source byte mismatch')
    return data

def inventory(root):
    if any(p.is_symlink() for p in (root,*root.parents)):raise ValueError('symlink packet path')
    es=read_json(root/'MANIFEST.json')['files'];names=[e['path'] for e in es]
    if not names or len(names)!=len(set(names)) or 'MANIFEST.json' in names:raise ValueError('invalid inventory')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):raise ValueError('inventory drift')
    for e in es:
        p=root/e['path']
        if len(safe(e['path']))!=1 or p.is_symlink() or not p.is_file():raise ValueError('regular flat file required')
        data=p.read_bytes()
        if type(e['bytes']) is not int or e['bytes']!=len(data) or hashlib.sha256(data).hexdigest()!=e['sha256']:
            raise ValueError('payload byte mismatch')
    return len(es)

def verify_bound_sources(root,src):
    es=src['files']
    if len(es)!=3 or {e['tag'] for e in es}!={'P','RATE','O'}:raise ValueError('source inventory mismatch')
    for e in es:
        data=read_source(root,e['commit'],e)
        if type(e['bytes']) is not int or len(data)!=e['bytes']:raise ValueError('source size mismatch')
        if 'sha256' in e and hashlib.sha256(data).hexdigest()!=e['sha256']:raise ValueError('source sha256 mismatch')
    return len(es)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--local-only',action='store_true');args=parser.parse_args()
    root=Path(__file__).absolute().parent
    files=inventory(root)
    count=0 if args.local_only else verify_bound_sources(root,read_json(root/'SOURCE_BINDINGS.json'))
    print(json.dumps({'packet_payloads_checked':files,'historical_sources_checked':not args.local_only,
        'source_bindings_checked':count,'proof_verified':False,'scientific_effect':'NONE'},sort_keys=True))

if __name__=='__main__':main()
