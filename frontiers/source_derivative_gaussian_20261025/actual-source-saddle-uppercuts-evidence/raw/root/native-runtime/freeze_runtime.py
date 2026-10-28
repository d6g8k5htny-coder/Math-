from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
B=Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
R=B/'native-runtime'
S=B/'native-runtime-initial-frozen'
S.mkdir(exist_ok=False)
rows=[]
for p in sorted(R.glob('*.py')):
    data=p.read_bytes()
    row={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'first_observed_utc':datetime.now(timezone.utc).isoformat(),'origin':'NEWrootnativepublisherinitialruntimeFIRSTIDONCE'}
    dest=S/p.name;dest.write_bytes(data)
    row['immutable_exact_copy']=str(dest);row['copy_identity']='same known bytecopy ID reused, no rehash'
    rows.append(row)
record={'observed_freeze_utc':datetime.now(timezone.utc).isoformat(),'rows':rows,'ordering':'Initial exact static runtime files created by root apply_patch BEFORE first captured invocation. This first documentary worker freezes their FIRSTphysicalIDs and exactcopies BEFORE any Gitobject/sourcecut/cache/remote operation. Worker+outer+entryoriginalsplitcapture starts with this first runtime-freeze invocation.','authorship':'Metadatautilityproposal remote_jet_gaussian_construct; no65 mathematical/proof/helper/ordinary authorship. Root personallyFULLallfouroriginalscripts6514tokens, then exacttransfer/staticnewfreeze script.','proof_or_old_hash_checks':0}
(B/'ROOT_NATIVE_RUNTIME_FIRST_IDS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
