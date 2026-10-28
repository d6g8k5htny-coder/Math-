from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
from capture import CaptureRun,put_new,require
from prepare_source_tree import PARENT,SOURCE_PATH,SOURCE_ID,oid

B=Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
REPO=Path('/workspace/Math-curvature-20261026')
SHA='b2d4c91162d98a1daefb5377bf3e65ef8615dd57'
BRANCH='refs/heads/codex/cubic-curvature-20261026'
run=CaptureRun(B/'public-native-source-cut001/action','establish-exact-public-fetched-native-source65-cut')
state={'local_ref_cas_completed':False,'source_index_sync_completed':False,'remote_ref_write':False}
try:
    script=Path(__file__);data=script.read_bytes()
    snapshot=run.path/'INITIAL_EXECUTED_SCRIPT.py';snapshot.write_bytes(data)
    script_id={'path':str(script),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'first_observed_utc':datetime.now(timezone.utc).isoformat(),'immutable_exact_copy':str(snapshot),'identity_effect':'NEW scriptFIRSTIDONCE; exactsnapshotIDreused. Staticapply_patch creation precededcapturedworker; physicalIDobservationinsideworker beforeanyGitoperation.'}
    put_new(run.path/'SCRIPT_FIRST_ID.json',script_id)
    prepared=json.loads((B/'native-source-tree001/action/RESULT.json').read_text())
    require(prepared['status']=='PASS_NEW_SOURCE_BLOB_AND_SOURCE_ONLY_TREE','Completed source-only tree preparation required')
    require(prepared['parent_sha']==PARENT and prepared['source_identity']==SOURCE_ID,'Qualified source/parent differs')
    require(oid(run.command('local-HEAD-before-CAS',['git','rev-parse','HEAD'],REPO))==PARENT,'Local HEAD changed; stop')
    require(run.command('actual-symbolic-branch',['git','symbolic-ref','-q','HEAD'],REPO).decode().strip()==BRANCH,'Actual local branch differs; stop')
    raw=run.command('exact-public-fetched-native-commit',['git','cat-file','commit',SHA],REPO)
    (run.path/'NATIVE_COMMIT.exact.txt').write_bytes(raw)
    headers,message=raw.split(b'\n\n',1)
    lines=headers.splitlines()
    trees=[x[5:].decode() for x in lines if x.startswith(b'tree ')]
    parents=[x[7:].decode() for x in lines if x.startswith(b'parent ')]
    require(trees==[prepared['tree_sha']] and parents==[PARENT],'Fetched native tree/parent differs from exact qualified source-only tree')
    run.event({'event':'EXACT_REMOTE_GIT_OBJECT_TRANSPORT_CLOSED_BEFORE_LOCAL_MOVEMENT','native_sha':SHA,'raw_object':str(run.path/'NATIVE_COMMIT.exact.txt'),'method':'Unauthenticated PUBLIC Git fetch; exact object from Git protocol, no reconstructed metadata candidate'})
    run.command('CAS-owned-local-branch',['git','update-ref','-m','exact public fetched native source65 cut',BRANCH,SHA,PARENT],REPO)
    state['local_ref_cas_completed']=True
    run.command('sync-ONLY-owned-source-index-entry',['git','update-index','--add','--cacheinfo','100644,'+prepared['blob_sha']+','+SOURCE_PATH],REPO)
    state['source_index_sync_completed']=True
    require(oid(run.command('HEAD-after-sourcecut',['git','rev-parse','HEAD'],REPO))==SHA,'Local sourcecut HEAD mismatch')
    result={'status':'PASS_NATIVE_SOURCE_COMMIT_IMPORTED_AND_LOCAL_CUT_ESTABLISHED','native_sha':SHA,'source_cut':SHA,'parent_sha':PARENT,'tree_sha':prepared['tree_sha'],'blob_sha':prepared['blob_sha'],'source_path':SOURCE_PATH,'source_identity':SOURCE_ID,'local_branch_ref':BRANCH,'local_HEAD':SHA,'root_canonical_record_observed_utc':datetime.now(timezone.utc).isoformat(),'exact_commit_transport':'Unauthenticated PUBLIC Git fetch with allcredentialhelpers/authheaders disabled. Nativeplugin lacked raw-byte transport; actualPUBLICvisibility checked independently. No ghcredentialretry/configchange/tokenaccess.','raw_commit_path':str(run.path/'NATIVE_COMMIT.exact.txt'),'root_action_record':str(run.path/'RESULT.json'),'earlier_failed_candidates':['native-source-import001/action/RESULT.json','native-source-import002/action/RESULT.json'],'failure_history':'Both earlier metadata-serialization candidates failed exactSHA gate and causedNOlocalbranch/index/cache/remoteref movement. Preservedfullversions/patches/streams; no furtherguesses or nativecreate_commit retries.','Git_author_committer':'ExactactualnativeGitobject retained, sharedprincipal is not independentproofauthorship.','qualification':'Completed actual65production strict/ALL119std3/ONEkernel plus ordinarystrict/ALL123std3/soleFalse reused; no proof/sourceSHA256 replays.','remote_branch_state':'Root has performedNOremote refupdate; recordedremoteheadee5 unchanged until final65metadata normalfastforward.','future66':'Fourproper66EXTRAs excludedsource-onlycut and65manifest/archive/registry.','script_first_identity':str(run.path/'SCRIPT_FIRST_ID.json'),**state}
    put_new(B/'ROOT_SOURCE_CUT.json',result)
    run.finish(result)
except Exception as e:
    run.finish({'status':'FAIL_PRESERVED_NO_AUTOMATIC_RETRY','exception':repr(e),**state})
    print(str(e),file=sys.stderr)
    raise SystemExit(1)
