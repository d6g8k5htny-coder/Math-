from pathlib import Path
from datetime import datetime,timezone
import difflib,hashlib,json
B=Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
R=B/'native-runtime';S=B/'native-runtime-message-amendment001';S.mkdir(exist_ok=False)
old=(R/'import_native_source_commit.py').read_text();new=(R/'import_native_source_commit_observed_message.py').read_text()
patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='initial/import_native_source_commit.py',tofile='amended/import_native_source_commit_observed_message.py'))
(S/'FULL_ACTUAL.patch').write_text(patch)
rows=[]
for name in ['import_native_source_commit_observed_message.py','freeze_message_amendment.py']:
    p=R/name;data=p.read_bytes();row={'path':str(p),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'first_observed_utc':datetime.now(timezone.utc).isoformat(),'identity_effect':'NEW runtime-version payload FIRSTIDONCE; oldoriginal runtime ID reused, NOTrehashed'}
    dest=S/name;dest.write_bytes(data);row['immutable_exact_copy']=str(dest);rows.append(row)
r={'status':'ROOT_RUNTIME_MESSAGE_SERIALIZATION_AMENDMENT_FROZEN','observed_utc':datetime.now(timezone.utc).isoformat(),'cause':'Concrete native-source-import001 exactSHA mismatch; no branch/index/cache/ref movement occurred. FirstcandidateusedrequestedmessagewithfinalLF; newcandidateusesliteralactualGit-dataAPI.message bytes, no newline modification or alternativeauthor/date/offset. SuccessacceptedONLYnativeSHA match. No native create_commit/tree retry and no proof verification replay.','prior_failure':str(B/'native-source-import001/action/RESULT.json'),'rows':rows,'full_patch':str(S/'FULL_ACTUAL.patch'),'old_initial_runtime':'native-runtime-initial-frozen/import_native_source_commit.py preserved'}
(B/'ROOT_NATIVE_MESSAGE_AMENDMENT_FIRST_IDS.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
