from pathlib import Path
from datetime import datetime, timezone
import json, shutil

def now(): return datetime.now(timezone.utc).isoformat()
pub = Path('/workspace/scratch/actual-source-quotient-saddle-collar-publication')
work = Path('/workspace/scratch/actual-source-quotient-saddle-collar-construct')
work.mkdir(exist_ok=True)
assert not (work/'ROOT_GO.json').exists()
ids = json.loads((pub/'PRECODE64_IDENTITIES.json').read_text())
ctrl = next(x for x in ids['files'] if x['path'].endswith('_CONTROLS.md'))
src = Path('/workspace/Math-curvature-20261026')/ctrl['path']
dst = work/'CONTROL_CONTRACT.md'
assert not dst.exists()
shutil.copyfile(src, dst)
assert dst.stat().st_size == ctrl['bytes']
copy = {'completed_utc':now(), 'source':str(src), 'destination':str(dst), 'bytes':ctrl['bytes'], 'sha256_reused':ctrl['sha256'], 'identity_origin':'Existing proper64 first ID reused, no hash', 'ordering':'COMPLETE controls copy BEFORE GO and ANY64 code/harness/helperprooftext'}
(pub/'ROOT_CONTROL_CONTRACT_COPY.json').write_text(json.dumps(copy,indent=2)+'\n')
actual = {'recorded_utc':now(), 'normal_publication':'f4825c3e3bd0e2d2c46157096e76b9ab17dbbb71', 'push_completed_utc':'2026-10-28T19:24:41.549784+00:00', 'native_SPEC_blob':'6ade1e5a71b47869d18f7018b356de8e7e41bddb', 'paths':[x['path']for x in ids['files']], 'firstIDs_reused':True, 'before_ANY64code':True, 'excluded63_manifest_archive_registry':True}
(pub/'ROOT_PRECODE_PUBLICATION.json').write_text(json.dumps(actual,indent=2)+'\n')
go = json.loads((pub/'ROOT_GO64_TEMPLATE.json').read_text())
go.update(issued_utc=now(), complete_controls_copy=copy, proper_PRECODE_publication=actual, generation_history='GO64_GENERATION_001.json preserves earlier parse-before-execution failure; this corrected activation has full prospective separate capture.')
(work/'ROOT_GO.json').write_text(json.dumps(go,indent=2)+'\n')
(pub/'ROOT_GO64_COPY.json').write_text(json.dumps(go,indent=2)+'\n')
print(json.dumps({'status':go['status'], 'issued_utc':go['issued_utc'], 'controls_copied_before':copy['completed_utc'], 'ROOT_GO':str(work/'ROOT_GO.json')}))
