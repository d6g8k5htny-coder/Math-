"""Fail-closed current/historical source byte checks; no analytic acceptance."""
import hashlib,json,pathlib,re,subprocess

def require(ok,message):
    if not ok:raise ValueError(message)

def identity(b):
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()}

def loads(s):
    def pairs(items):
        d={}
        for k,v in items:
            require(k not in d,'duplicate JSON key');d[k]=v
        return d
    return json.loads(s,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite JSON')))

def safe_path(s):
    p=pathlib.PurePosixPath(s)
    require(not p.is_absolute() and str(p)==s and '..' not in p.parts and p.parts,'unsafe path')
    return p

def unique_paths(entries):
    paths=[e['path'] for e in entries]
    require(len(paths)==len(set(paths)),'duplicate source path')
    for p in paths:safe_path(p)

def read_checked(root,e):
    root=pathlib.Path(root);rel=safe_path(e['path'])
    require(not root.is_symlink(),'root symlink forbidden')
    for i in range(1,len(rel.parts)+1):
        require(not root.joinpath(*rel.parts[:i]).is_symlink(),'source symlink forbidden')
    path=root.joinpath(*rel.parts);require(path.is_file(),'missing regular file')
    b=path.read_bytes();actual=identity(b)
    require(all(actual[k]==e[k] for k in actual if k in e),'source identity mismatch')
    require('sha256' in e and 'git_blob' in e,'incomplete identity')
    return b

def upstream(repo,entries):
    unique_paths(entries);repo=pathlib.Path(repo)
    for e in entries:
        require(re.fullmatch('[0-9a-f]{40}',e['commit']) is not None,'invalid pinned commit')
        obj=e['commit']+':'+e['path']
        b=subprocess.check_output(['git','-C',str(repo),'show',obj],stderr=subprocess.PIPE,timeout=20)
        actual=identity(b)
        require(all(actual[k]==e[k] for k in actual if k in e),'historical source differs: '+e['id'])
        if e.get('current_required',True):read_checked(repo,e)
    return len(entries)
