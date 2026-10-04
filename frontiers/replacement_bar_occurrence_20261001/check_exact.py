"""Finite exact controls and source identity; not a continuum proof certificate."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath

SOURCE_MANIFEST_SHA256 = '320f64d3feebd7a694fc33458cf5c768207411525e89df6fd786f75990f5fc60'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def contained_file(root, relative):
    require(isinstance(relative, str) and bool(relative), 'invalid source path')
    parts = PurePosixPath(relative)
    require(not parts.is_absolute() and str(parts) == relative
            and all(p not in ('', '.', '..') for p in parts.parts)
            and '\\\\' not in relative, 'noncanonical source path')
    target = root
    for part in parts.parts:
        target = target / part
        require(not target.is_symlink(), 'symlink source')
    require(target.is_file() and root in target.resolve().parents,
            'source must be a contained regular file')
    return target


def verify_entry(root, entry):
    root = Path(root).resolve()
    data = contained_file(root, entry.get('local_path')).read_bytes()
    require(type(entry.get('bytes')) is int and len(data) == entry['bytes'],
            'source byte count')
    require(hashlib.sha256(data).hexdigest() == entry.get('sha256'),
            'source SHA256')
    blob = hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()
    require(blob == entry.get('blob'), 'source Git blob')


def verify_sources(repo=None, manifest_path=None):
    script = Path(__file__).absolute()
    require(not script.is_symlink(), 'symlink checker')
    root = Path(repo).resolve() if repo is not None else script.resolve().parents[2]
    if manifest_path is None:
        manifest_path = contained_file(root, 'frontiers/replacement_bar_occurrence_20261001/SOURCES.json')
    data = Path(manifest_path).read_bytes()
    require(hashlib.sha256(data).hexdigest() == SOURCE_MANIFEST_SHA256,
            'source manifest digest')
    manifest = json.loads(data)
    entries = manifest['sources']
    require(len(entries) == 10, 'ten exact sources required')
    require(len({e['key'] for e in entries}) == 10, 'duplicate source key')
    for entry in entries:
        verify_entry(root, entry)
    return len(entries)


def rational(value):
    require(type(value) in (int, F), 'exact rational required')
    return F(value)


def count_statistics(law):
    require(isinstance(law, dict) and bool(law), 'nonempty count law required')
    require(all(type(n) is int and n >= 0 for n in law), 'invalid count')
    probs = {n:rational(p) for n,p in law.items()}
    require(all(p >= 0 for p in probs.values()) and sum(probs.values()) == 1,
            'invalid probability law')
    return tuple(sum((p*term(n) for n,p in probs.items()),F(0)) for term in
                 (lambda n:n,lambda n:int(n>0),lambda n:max(n-1,0),
                  lambda n:n if n>=2 else 0,lambda n:n*(n-1)))


def mark_statistics(fields):
    total=average=event=excess=F(0)
    probability=F(0)
    for raw_probability,raw_marks in fields:
        p=rational(raw_probability)
        require(p>=0, 'negative probability')
        marks=tuple(rational(v) for v in raw_marks)
        n=len(marks)
        probability += p
        total += p*sum(marks,F(0))
        if n:
            average += p*sum(marks,F(0))/n
            event += p
            excess += p*(n-1)
    require(probability==1, 'invalid probability law')
    return total,average,event,excess


def cubic_hessian(parameters, point):
    k,s,a,beta,q=map(rational,parameters)
    x,z=map(rational,point)
    return 12*k*x+a*z, a*x+beta*z, s+beta*x+q*z


def annulus_budget(C,R,delta,epsilon):
    C,R,delta,epsilon=map(rational,(C,R,delta,epsilon))
    require(C>=0 and R>0 and delta>=0 and epsilon>=0, 'invalid annulus parameters')
    return C/R**2+C/R+epsilon+C*delta


if __name__=='__main__':
    print(json.dumps({'verified_sources':verify_sources(),
                      'scope':'Exact source identity only; run test_exact.py for finite controls.'}))
