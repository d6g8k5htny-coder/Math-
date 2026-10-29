#!/usr/bin/env python3
"""Stage66 metadata custody; importing this file performs no action."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

R=Path('/workspace/scratch/actual-source-regular-local-collar-packaging')
P=Path('/workspace/scratch/actual-source-regular-local-collar-construct')
U=Path('/workspace/scratch/actual-source-regular-local-collar-publication')
B=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
A=R/'archive-prep'
E='actual-source-regular-local-collar-evidence'
SOURCE='SourceActualRegularLocalCollar.lean'
BASE='263b9d4329043e6debd299a8c27327ee515670d7'
EMPTY='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
AUTHORITY=['https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md','https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md','https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261025_REVIEW_FAMILIES.md']
_ids=None
_copies=None
_intents=None
_bank={}
_new_allowed=set()

def now():return datetime.now(timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def read(path):return json.loads(Path(path).read_text())
def syncdirs(directory):
    for path in [directory,*directory.parents]:
        if path==R or R in path.parents:
            fd=os.open(path,os.O_RDONLY|os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
        if path==R:break
def append(name,record):
    path=R/name;path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as stream:
        stream.write(json.dumps({'recorded_utc':now(),**record},ensure_ascii=False)+'\n')
        stream.flush();os.fsync(stream.fileno())
    syncdirs(path.parent)
def durable(path,raw):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        require(path.read_bytes()==raw,'Preserve changed immutable metadata under a new path: '+str(path));return
    with path.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    syncdirs(path.parent)
def put(path,value):durable(path,(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
def identities():
    global _ids,_intents
    if _ids is None:
        path=R/'IDENTITY_JOURNAL.jsonl'
        rows=[json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        _ids={row['path']:row for row in rows if row['event']=='identity_recorded'}
        _intents={row['path'] for row in rows if row['event']=='hash_intent'}
    return _ids
def refresh_progress():
    """A separately spawned worker may append progress after this process cached it."""
    global _ids,_copies,_intents
    _ids=None;_copies=None;_intents=None
    return identities()
def allow_first_identity(path):_new_allowed.add(str(Path(path)))
def retain(path,record):
    path=Path(path);raw=path.read_bytes()
    require(len(raw)==record['bytes'],'Known identity size differs: '+str(path))
    old=_bank.get(raw)
    if old:require(old['sha256']==record['sha256'],'Contradictory identities for exact retained bytes')
    _bank[raw]={'bytes':record['bytes'],'sha256':record['sha256'],'identity_source':str(path)}
def identity(path,retained=None):
    path=Path(path);key=str(path);known=identities().get(key)
    if known:
        require(path.stat().st_size==known['bytes'],'Recorded immutable metadata size changed')
        if retained:require((known['bytes'],known['sha256'])==(retained['bytes'],retained['sha256']),'Contradictory supplied identity')
        return known
    raw=path.read_bytes();record=retained or _bank.get(raw)
    if record:
        require(len(raw)==record['bytes'],'Retained copy size differs')
        row={'path':key,'bytes':len(raw),'sha256':record['sha256'],'hash_computed_here':False,'origin':'Existing exact-byte identity reused','identity_source':record.get('identity_source')}
    elif not raw:
        row={'path':key,'bytes':0,'sha256':EMPTY,'hash_computed_here':False,'origin':'Literal known EMPTY identity reused; zero hashes'}
    else:
        require(key in _new_allowed,'Missing known identity or explicit NEW immutable-payload authority: '+key)
        require(key not in _intents,'Unresolved first-identity intent; preserve uncertainty: '+key)
        append('IDENTITY_JOURNAL.jsonl',{'event':'hash_intent','path':key,'reason':'Explicitly authorized FIRST identity of previously unrecorded NEW66 metadata payload'})
        _intents.add(key)
        row={'path':key,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'hash_computed_here':True,'origin':'FIRST necessary NEW66 immutable metadata identity, once'}
    append('IDENTITY_JOURNAL.jsonl',{'event':'identity_recorded',**row});_ids[key]=row
    _bank[raw]={'bytes':row['bytes'],'sha256':row['sha256'],'identity_source':key}
    return row
def write(path,value):
    put(path,value);allow_first_identity(path);return identity(path)
def text(path,value):
    durable(path,value.encode());allow_first_identity(path);return identity(path)
def copied(source,destination,retained=None,first_new=False):
    global _copies
    source=Path(source);destination=Path(destination)
    if _copies is None:
        path=R/'ARCHIVE_PROGRESS.jsonl'
        rows=[json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
        _copies={row['destination'] for row in rows if row['event']=='copy_complete'}
    if str(destination) in _copies:
        require(destination.is_file(),'Completed copy missing');return identity(destination,retained)
    append('ARCHIVE_PROGRESS.jsonl',{'event':'copy_intent','source':str(source),'destination':str(destination)})
    durable(destination,source.read_bytes())
    if first_new:allow_first_identity(destination)
    record=identity(destination,retained)
    append('ARCHIVE_PROGRESS.jsonl',{'event':'copy_complete','destination':str(destination),'sha256':record['sha256']})
    _copies.add(str(destination));return record
