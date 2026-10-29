#!/usr/bin/env python3
"""Stage60 immutable archive only; no proof or old-payload hash campaign."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
R=Path('/workspace/scratch/actual-source-morse-local-model-packaging-proposal')
P=Path('/workspace/scratch/actual-source-morse-local-model-construct')
U=Path('/workspace/scratch/actual-source-morse-local-model-publication')
B=Path('/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025')
A=R/'archive-prep';E='actual-source-morse-local-model-evidence'
SOURCE='SourceActualMorseLocalModel.lean'
CUT=None;BASE='29e76f91af5f88606ca3f4f8e39ee88c1022fd73'
SRC_SHA='d6776bd34a2ae1371c2af8fbfcc54d2a536e7c96b2e4db517a5f4a81b4128cd5'
OBJ_SHA='7bc2d9fc1edcbd936dc04b583fa2b4642fc6fd968c594350df8eec28093d7ad3'
AUTHORITY=['https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md','https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md','https://github.com/d6g8k5htny-coder/main/blob/main/governance/OWNER_DECISION_20261025_REVIEW_FAMILIES.md']
def now():return datetime.now(timezone.utc).isoformat()
def require(ok,message):
    if not ok:raise RuntimeError(message)
def syncdirs(directory):
    for p in [directory,*directory.parents]:
        if p==R or R in p.parents:
            fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
            try:os.fsync(fd)
            finally:os.close(fd)
        if p==R:break
def append(name,obj):
    path=R/name;path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a')as f:f.write(json.dumps({'recorded_utc':now(),**obj},ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
    syncdirs(path.parent)
def durable(path,raw):
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():require(path.read_bytes()==raw,'Prior immutable payload differs; preserve and version '+str(path));return
    with path.open('wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    syncdirs(path.parent)
def put(path,obj):durable(path,(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
def read(path):return json.loads(path.read_text())
def identities():
    p=R/'IDENTITY_JOURNAL.jsonl'
    return {x['path']:x for x in map(json.loads,p.read_text().splitlines())if x['event']=='identity_recorded'}if p.exists()else{}
bank={}
def retain(path,rec):
    raw=path.read_bytes();require(len(raw)==rec['bytes'],'Recorded size mismatch '+str(path))
    if raw in bank:require(bank[raw]['sha256']==rec['sha256'],'Contradictory retained identity')
    bank[raw]={'bytes':rec['bytes'],'sha256':rec['sha256'],'identity_source':str(path)}
def identity(path,retained=None):
    known=identities().get(str(path))
    if known:
        require(path.stat().st_size==known['bytes'],'Recorded payload size changed')
        if retained:require((known['bytes'],known['sha256'])==(retained['bytes'],retained['sha256']),'Contradictory supplied identity')
        return known
    raw=path.read_bytes();rec=retained or bank.get(raw)
    if rec:
        require(len(raw)==rec['bytes'],'Retained copied size mismatch')
        info={'path':str(path),'bytes':len(raw),'sha256':rec['sha256'],'origin':'Existing identity reused for exact immutable NEW60 bytes; no hash','hash_computed_here':False,'identity_source':rec.get('identity_source')}
    else:
        j=R/'IDENTITY_JOURNAL.jsonl';prior=[x for x in map(json.loads,j.read_text().splitlines())if x['event']=='hash_intent'and x['path']==str(path)]if j.exists()else[]
        require(not prior,'Unresolved hash intent: preserve uncertainty and require explicit bounded identity recovery '+str(path))
        append('IDENTITY_JOURNAL.jsonl',{'event':'hash_intent','path':str(path),'reason':'First custody of previously unrecorded immutable NEW60 archive/packaging payload only.'})
        info={'path':str(path),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'origin':'First custody identity of previously unrecorded immutable NEW60 payload','hash_computed_here':True}
    append('IDENTITY_JOURNAL.jsonl',{'event':'identity_recorded',**info});bank[raw]={'bytes':info['bytes'],'sha256':info['sha256'],'identity_source':str(path)}
    return info
def write(path,obj):put(path,obj);return identity(path)
def copied(src,dst,retained=None):
    append('ARCHIVE_PROGRESS.jsonl',{'event':'copy_intent','source':str(src),'destination':str(dst)})
    durable(dst,src.read_bytes());rec=identity(dst,retained)
    append('ARCHIVE_PROGRESS.jsonl',{'event':'copy_complete','destination':str(dst),'sha256':rec['sha256']});return rec
