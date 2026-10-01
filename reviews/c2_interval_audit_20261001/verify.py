"""Verify this packet and the exact PR223 output/source bindings, not its theorem."""
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

def main():
    p=argparse.ArgumentParser();p.add_argument('--local-only',action='store_true');a=p.parse_args()
    root=Path(__file__).absolute().parent;inventory(root)
    count=0
    if not a.local_only:
        src=read_json(root/'SOURCE_BINDINGS.json');es=src['files']
        required={'ia.py','elem.py','gam.py','certificate.py','RESULTS.json','NOTE.md'}
        if len(es)!=6 or {e['path'].split('/')[-1] for e in es}!=required:raise ValueError('source inventory mismatch')
        outputs=None
        for e in es:
            data=read_source(root,src['commit'],e);count+=1
            if e['path'].endswith('/RESULTS.json'):outputs=json.loads(data)
        import oracle
        for key,pair in oracle.PUBLISHED.items():
            d,which=key.split('.');which='c2 / c' if which=='ratio' else which
            if list(pair)!=outputs['values']['d='+d][which]:raise ValueError('copied published interval mismatch')
    import oracle
    expected=json.loads((root/'RESULTS.json').read_text())
    if json.loads(json.dumps(oracle.results()))!=expected:raise ValueError('recomputed results mismatch')
    print(json.dumps({'historical_sources_checked':not a.local_only,'source_bindings_checked':count,
                      'independent_numerical_outputs_checked':9,'scientific_effect':'NONE',
                      'Gaussian_derivation_reviewed':False},sort_keys=True))

if __name__=='__main__':main()
