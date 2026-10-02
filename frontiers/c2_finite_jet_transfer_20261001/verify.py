"""Check exact packet/source bytes and arithmetic outputs, never theorem acceptance."""
import argparse,hashlib,json,os,re,subprocess
from pathlib import Path,PurePosixPath


def unique(items):
    d={}
    for k,v in items:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d


def load(p):
    if p.is_symlink() or not p.is_file():raise ValueError('regular JSON required')
    x=json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=unique)
    if not isinstance(x,dict):raise ValueError('JSON object required')
    return x


def safe(path):
    if not isinstance(path,str) or not path:raise ValueError('path required')
    p=PurePosixPath(path)
    if p.is_absolute() or str(p)!=path or any(x in ('.','..') or not re.fullmatch('[A-Za-z0-9_.-]+',x) for x in p.parts):
        raise ValueError('unsafe path')
    return p.parts


def identity(data,e):
    if type(e['bytes']) is not int or len(data)!=e['bytes']:raise ValueError('byte count mismatch')
    if hashlib.sha256(data).hexdigest()!=e['sha256']:raise ValueError('SHA256 mismatch')
    if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=e['git_blob']:
        raise ValueError('Git blob mismatch')
    return True


def inventory(root):
    if any(p.is_symlink() for p in (root,*root.parents)):raise ValueError('symlink packet root')
    es=load(root/'MANIFEST.json')['files'];names=[e['path'] for e in es]
    if not names or len(names)!=len(set(names)) or 'MANIFEST.json' in names:raise ValueError('invalid inventory')
    if sorted(p.name for p in root.iterdir())!=sorted(names+['MANIFEST.json']):raise ValueError('membership drift')
    for e in es:
        if len(safe(e['path']))!=1:raise ValueError('flat packet required')
        p=root/e['path']
        if p.is_symlink() or not p.is_file():raise ValueError('regular payload required')
        identity(p.read_bytes(),e)
    return len(es)


def git(root,*args):
    out=subprocess.run(['git','--no-replace-objects',*args],cwd=root,
        env=dict(os.environ,GIT_NO_REPLACE_OBJECTS='1'),capture_output=True,timeout=30)
    if out.returncode:raise ValueError('historical Git object unavailable')
    return out.stdout


def historical(root,e):
    commit=e['commit']
    if not isinstance(commit,str) or not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('full commit required')
    ps=safe(e['path'])
    if git(root,'cat-file','-t',commit).strip()!=b'commit':raise ValueError('not a commit')
    for n in range(1,len(ps)+1):
        prefix='/'.join(ps[:n])
        rows=[r for r in git(root,'ls-tree','--full-tree','-z',commit,'--',prefix).split(b'\0') if r]
        if len(rows)!=1:raise ValueError('missing or ambiguous source')
        meta,name=rows[0].split(b'\t',1);mode,kind,blob=meta.decode().split()
        if name.decode()!=prefix:raise ValueError('path mismatch')
        if n<len(ps) and (mode,kind)!=('040000','tree'):raise ValueError('non-tree ancestor')
        if n==len(ps) and (kind!='blob' or mode not in ('100644','100755')):raise ValueError('nonregular source')
    if blob!=e['git_blob']:raise ValueError('historical binding mismatch')
    data=git(root,'cat-file','blob',blob);identity(data,e);return data


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--local-only',action='store_true');a=p.parse_args()
    root=Path(__file__).absolute().parent;count=inventory(root)
    import controls
    if controls.results()!=load(root/'RESULTS.json'):raise ValueError('arithmetic output drift')
    sources=load(root/'SOURCES.json')['sources']
    if len(sources)!=5 or {e['id'] for e in sources}!={'P','R','NUM_NOTE','NUM_INTERVAL','T'}:
        raise ValueError('source inventory drift')
    checked=0
    if not a.local_only:
        for e in sources:
            data=historical(root,e);checked+=1
            if e['id']=='NUM_INTERVAL':
                parsed=json.loads(data,object_pairs_hook=unique)
                for d,pair in controls.REFERENCE_C2.items():
                    if list(pair)!=parsed['values']['d='+d]['c2']:raise ValueError('reference interval copy mismatch')
    print(json.dumps({'packet_files_checked':count,'historical_sources_checked':not a.local_only,
        'source_bindings_checked':checked,'arithmetic_transport_outputs_checked':3,
        'analytic_proof_verified_by_program':False,'scientific_effect':'NONE'},sort_keys=True))

if __name__=='__main__':main()
