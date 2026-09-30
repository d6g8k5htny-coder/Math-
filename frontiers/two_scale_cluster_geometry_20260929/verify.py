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

ACCEPTED_MANUSCRIPTS = {
    'TWO_SCALE_LAW.md': {
        'bytes': 17139,
        'sha256': 'e81d7fe09d25c3266eb8e62922756f54761d7f74d692fb35d9a8071fffd73769',
        'git_blob': 'a32fd5f7d941bbe1fe943df045b1e0fbec8d691c',
        'review_ids': (5360227991,),
    },
    'RADIAL_TAIL.md': {
        'bytes': 12533,
        'sha256': '250897858c8b314c0ff85ec1860a725efacfdae0ff7409fced4cadf7bfb85973',
        'git_blob': '0f14417ef7038b9c6f50e4b01e393a58b7b5e3a4',
        'review_ids': (5360178611, 5360216551),
    },
}
ESSENTIAL_PACKET_LEAVES = frozenset(('TWO_SCALE_LAW.md','RADIAL_TAIL.md','REVIEW_RECORD.md',
                                     'ACCEPTED_BINDINGS.json','SOURCES.json','RESULTS.json',
                                     'geometry.py','verify.py'))


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
    return subprocess.run(['git','--no-replace-objects',*args],cwd=root,check=True,capture_output=True,
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
    if git(root,'cat-file','-t',commit).strip()!=b'commit':
        raise ValueError('source identity must name a commit object')
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


def verify_acceptance_bindings(root):
    """Bind the accepted mathematical bytes to the actual scoped review ids.

    MANIFEST.json is intentionally not authoritative for these identities: a
    coordinated manuscript+manifest refresh must still fail until this explicit
    acceptance contract is changed under review.
    """
    data=read_json(root/'ACCEPTED_BINDINGS.json')
    if data.get('schema')!=1 or data.get('accepted_mathematical_head')!='7c82252533c3fe14ee262f7f87c0549c10968592':
        raise ValueError('unexpected acceptance-binding schema/head')
    rows=data.get('manuscripts')
    if not isinstance(rows,list) or {r.get('path') for r in rows}!=set(ACCEPTED_MANUSCRIPTS):
        raise ValueError('accepted manuscript membership mismatch')
    for row in rows:
        path=row['path']; expected=ACCEPTED_MANUSCRIPTS[path]
        pure=safe_path(path)
        if len(pure.parts)!=1:raise ValueError('flat accepted manuscript required')
        for key in ('bytes','sha256','git_blob'):
            if row.get(key)!=expected[key]:raise ValueError('accepted manuscript binding changed: '+path)
        identity((root/path).read_bytes(),{'path':path,'bytes':expected['bytes'],
                                           'sha256':expected['sha256'],'git_blob':expected['git_blob']})
        reviews=row.get('reviews')
        if not isinstance(reviews,list):raise ValueError('accepted review list required: '+path)
        ids=tuple(r.get('id') for r in reviews)
        if ids!=expected['review_ids'] or len(ids)!=len(set(ids)):
            raise ValueError('accepted review binding changed: '+path)
        for review in reviews:
            if review.get('provider')!='Anthropic Claude' or not str(review.get('url','')).startswith('https://github.com/d6g8k5htny-coder/Math-/pull/166#'):
                raise ValueError('accepted review provenance malformed: '+path)
    return len(rows)

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


def verify_essential_inventory(root):
    names={e['path'] for e in read_json(root/'MANIFEST.json')['files']}
    if not ESSENTIAL_PACKET_LEAVES <= names:
        raise ValueError('essential accepted/replay leaf missing from packet inventory')
    return len(ESSENTIAL_PACKET_LEAVES)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-only',action='store_true')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    count=verify_inventory(root)
    verify_essential_inventory(root)
    accepted_count=verify_acceptance_bindings(root)
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
    verify_essential_inventory(root)
    verify_acceptance_bindings(root)
    print(json.dumps({'passed':True,'packet_leaves':count,'accepted_manuscripts':accepted_count,'source_count':source_count,
                      'source_pins_checked':not args.local_only,'scientific_effect':'NONE',
                      'mathematical_acceptance':False},sort_keys=True))


if __name__=='__main__':main()
