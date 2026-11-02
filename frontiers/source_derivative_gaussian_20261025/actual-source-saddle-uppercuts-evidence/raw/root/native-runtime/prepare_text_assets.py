from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
from capture import CaptureRun,put_new
B=Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
S=Path('/workspace/scratch/actual-source-saddle-uppercuts-native-publication-plan/transport')
run=CaptureRun(B/'prepublication-text-assets001/action','exact-text-aliases-and-metadata-transfer-runtime')
try:
    script=Path(__file__);data=script.read_bytes();snapshot=run.path/'INITIAL_EXECUTED_SCRIPT.py';snapshot.write_bytes(data)
    put_new(run.path/'SCRIPT_FIRST_ID.json',{'path':str(script),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'first_observed_utc':datetime.now(timezone.utc).isoformat(),'immutable_exact_copy':str(snapshot),'effect':'NEWscriptFIRSTIDonce/exactcopyIDreused'})
    (B/'raw-git-text-aliases').mkdir(exist_ok=False);(B/'native-transfer-runtime').mkdir(exist_ok=False)
    pairs=[(B/('native-source-import00'+str(i)+'/action/CANDIDATE_RAW_COMMIT.bin'),B/('raw-git-text-aliases/failed-import00'+str(i)+'.exact.txt')) for i in [1,2]]
    pairs += [(S/n,B/'native-transfer-runtime'/n) for n in ['prepare_blob_lz4.py','lz4_transport.js','README.md']]
    rows=[]
    for source,destination in pairs:
        payload=source.read_bytes();payload.decode('utf-8')
        sha=hashlib.sha256(payload).hexdigest()
        with destination.open('xb') as stream:stream.write(payload)
        rows.append({'source':str(source),'destination':str(destination),'bytes':len(payload),'sha256':sha,'first_observed_utc':datetime.now(timezone.utc).isoformat(),'origin':'Previouslyunhashedmetadatautility/rawGitpayload FIRSTIDONCE; EXACTbytecopyIDreused BOTHpaths/no newline changes','source_ends_LF':payload.endswith(b'\n')})
    record={'status':'EXACT_METADATA_TEXT_ASSETS_FROZEN_NO_MATH_OR_GIT_ACTION','observed_utc':datetime.now(timezone.utc).isoformat(),'rows':rows,'archive_policy':'Only exact.txtaliases archived, original.bin/isolated.index/.olean/otherbinaries retainedworkspace/excluded. OriginalsecondcandidatehasNOlastLF andcopyretainsit.','runtime_scope':'NewGitbyteTRANSFERONLY/no65mathematicalhelper/oldprooforSHAreplay; LZ4proposalstaticrootFULLread3788tokens, notyetexecutedoruploadqualified','identity_self':'Notselfhashed; anylaternecessaryFIRSTIDONCE/cache.'}
    put_new(B/'ROOT_METADATA_TEXT_ASSET_IDS.json',record);run.finish(record)
except Exception as e:
    run.finish({'status':'FAIL_PRESERVED_NO_AUTOMATIC_RETRY','exception':repr(e)})
    print(str(e),file=sys.stderr);raise SystemExit(1)
