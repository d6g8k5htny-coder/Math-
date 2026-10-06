"""Small source-bound evidence checker. Does not certify source/model alignment."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE=Path(__file__).resolve().parent
ALLOWED={'propext','Classical.choice','Quot.sound'}

def audit_axioms(text,names):
    pattern=re.compile(r"'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)")
    matches=list(pattern.finditer(text))
    if [m.group(1) for m in matches]!=names:
        raise ValueError('axiom inventory mismatch')
    if pattern.sub('',text).strip(): raise ValueError('unmatched axiom evidence')
    for m in matches:
        axioms={s.strip() for s in (m.group(2) or '').split(',') if s.strip()}
        if not axioms<=ALLOWED: raise ValueError('forbidden axiom')

def audit_types(text,names):
    found=re.findall(r'^@?(CapI4Polar\.\w+)(?:\.\{[^}]*\})?\s*:',text,re.M)
    if found!=names or re.search(r'\b(error|warning):',text):
        raise ValueError('type inventory or diagnostic mismatch')

def audit_negative(text,status):
    if status!=1 or not re.fullmatch(r'(?:[^\n]*:\d+:\d+: )?error: unsolved goals\n⊢ False\s*',text):
        raise ValueError('not the intended concrete false-goal failure')

def sha(data): return hashlib.sha256(data).hexdigest()

def source():
    manifest=json.loads((HERE/'SOURCES.json').read_text())
    expected=manifest['files']
    actual={p.name for p in HERE.iterdir()}
    if actual!=set(expected)|{'SOURCES.json'}: raise ValueError('packet inventory mismatch')
    for name,ident in expected.items():
        p=HERE/name
        if p.is_symlink() or sha(p.read_bytes())!=ident['sha256']:
            raise ValueError('source bytes mismatch: '+name)
    root=HERE.parent.parent
    # In the repository the side directory is companions/<name>/.
    for path,blob in manifest['local_source_blobs'].items():
        p=root/path
        data=p.read_bytes()
        if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=blob:
            raise ValueError('pinned source mismatch: '+path)
    return manifest

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode',choices=['source','emit','check'])
    ap.add_argument('out',nargs='?',type=Path)
    a=ap.parse_args(); manifest=source(); names=manifest['declarations']
    if a.mode=='source':
        print(json.dumps({'manifest_sha256':sha((HERE/'SOURCES.json').read_bytes()),
          'files':manifest['files'],'source_blobs':manifest['local_source_blobs']},sort_keys=True)); return
    if a.out is None: raise ValueError('output directory required')
    if a.mode=='emit':
        (a.out/'Audit.lean').write_text('import CapI4Polar\n'+''.join('#print axioms '+n+'\n' for n in names))
        (a.out/'Types.lean').write_text('import CapI4Polar\nset_option pp.universes true\n'+''.join('#check @'+n+'\n' for n in names))
        (a.out/'Positive.lean').write_text('import CapI4Polar\nopen CapI4Polar\nexample : CapI4Polar.spectrum 0 (0, 0) = (0, 0) := by norm_num [CapI4Polar.spectrum, CapI4Polar.radius]\nexample (t : ℝ) (z : ℝ × ℝ) : (CapI4Polar.spectrum t z).1 ≤ (CapI4Polar.spectrum t z).2 := CapI4Polar.spectrum_ordered t z\n')
        (a.out/'RejectOrder.lean').write_text('import CapI4Polar\nopen CapI4Polar\nexample : (CapI4Polar.spectrum 0 (1, 0)).1 = (CapI4Polar.spectrum 0 (1, 0)).2 := by\n  norm_num [CapI4Polar.spectrum, CapI4Polar.radius]\n')
        (a.out/'RejectOffDiagonal.lean').write_text('import CapI4Polar\nopen CapI4Polar\nexample : (CapI4Polar.eigenvalues (0, (1, 0))).1 * (CapI4Polar.eigenvalues (0, (1, 0))).2 = 0 := by\n  rw [CapI4Polar.eigenvalues_product]\n  norm_num\n'); return
    audit_axioms((a.out/'axioms.log').read_text(),names)
    audit_types((a.out/'types.log').read_text(),names)
    for control in ['RejectOrder','RejectOffDiagonal']:
        audit_negative((a.out/(control+'.log')).read_text(),int((a.out/(control+'.status')).read_text()))
    print(json.dumps({'declarations':len(names),'axioms':sorted(ALLOWED),
       'scope':'polar sub-interface only; entry-volume and concrete model not supplied',
       'evidence_parsers':'PASS'},sort_keys=True))
if __name__=='__main__': main()
