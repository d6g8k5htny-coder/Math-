from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
from capture import CaptureRun,put_new,require
B=Path('/workspace/scratch/actual-source-saddle-uppercuts-publication')
P=Path('/workspace/scratch/actual-source-saddle-uppercuts-construct')
run=CaptureRun(B/'producer-closure-adoption001/action','root-first-adoption-of-actual-closed-producer-records')
try:
    script=Path(__file__);scriptdata=script.read_bytes();snapshot=run.path/'INITIAL_EXECUTED_SCRIPT.py';snapshot.write_bytes(scriptdata)
    put_new(run.path/'SCRIPT_FIRST_ID.json',{'path':str(script),'bytes':len(scriptdata),'sha256':hashlib.sha256(scriptdata).hexdigest(),'first_observed_utc':datetime.now(timezone.utc).isoformat(),'immutable_exact_copy':str(snapshot),'effect':'NEWscriptFIRSTIDONCE; exactcopyIDreused. Staticcreationbeforecapture; observedidentitybeforeadoptionactions.'})
    cache=json.loads((P/'FIRST_ID_CACHE.json').read_text());docs=json.loads((P/'FINAL_DOCUMENT_IDS.json').read_text())
    rows=[];new_hashes=0;reused=0
    for name in docs['final_closed_capture_paths_for_root_FIRST_adoption']:
        p=Path(name);st=p.stat();marker=[st.st_size,st.st_mtime_ns];known=cache.get(name)
        if known and known.get('marker')==marker:
            row={**known,'root_adoption_effect':'Known producerFIRSTID REUSED, no rehash'};reused+=1
        elif st.st_size==0:
            row={'path':name,'bytes':0,'sha256':'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855','marker':marker,'first_observed_utc':datetime.now(timezone.utc).isoformat(),'root_adoption_effect':'Knownexactempty-payload identity reused; zeroactualbytes implyknownemptySHA withoutrehash'};reused+=1
        else:
            data=p.read_bytes();row={'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'marker':marker,'first_observed_utc':datetime.now(timezone.utc).isoformat(),'root_adoption_effect':'Previouslyunhashed closedactualdocumentarypayload FIRSTIDONCE'};new_hashes+=1
        rows.append(row)
    cut=json.loads((B/'ROOT_SOURCE_CUT.json').read_text());copy=json.loads((B/'ROOT_OWN_OBJECT_COPY.json').read_text());copyaction=json.loads((B/'native-own-copy001/action/RESULT.json').read_text())
    require(cut['status']=='PASS_NATIVE_SOURCE_COMMIT_IMPORTED_AND_LOCAL_CUT_ESTABLISHED' and copy['status']=='PASS_ROOT_ONLY_ELIGIBLE_OWN_COPY_ONCE','Actual completed rootcut/copyrequired')
    addendum={'status':'ROOT_ACTUAL_CUT_COPY_BINDING_SUPERSEDES_HISTORICAL_PENDING_ONLY','observed_utc':datetime.now(timezone.utc).isoformat(),'producer_frozen_documents':'FINAL_IDS/FINAL_READY actualPENDINGrootobservationsremainimmutablehistorical; no regeneration/rewrites/rechecks','source_cut':cut['source_cut'],'parent':cut['parent_sha'],'source_Gitblob':cut['blob_sha'],'source_identity_reused':cut['source_identity'],'source_cut_record':str(B/'ROOT_SOURCE_CUT.json'),'own_copy_record':str(B/'ROOT_OWN_OBJECT_COPY.json'),'own_copy_action_record':str(B/'native-own-copy001/action/RESULT.json'),'own_copy_started_utc':copyaction['started_utc'],'own_copy_ended_utc':copyaction['ended_utc'],'own_object_identity_reused':copy['own_object_identity'],'copy_count':1,'further_copy_actions':'ALL_SKIP/noold-helper-ordinary-ileanpromotion','remote_ref':'Stillqualified64ee5; no remote refupdate bycut/copy. NativeSOURCEcommitexistsandisexactlocalHEAD; finalnormalFFpublicationpending.','mathematical_evidence':'All15calls/119production+123ordinary/std3/ONEkernel/soleFalseclosed/reused. This is onlynewprocessbinding.','producer_closed_counts':{'math':15,'documentary':25,'all_workers':40,'outer':40,'entry':40,'all_original_split_streams':240},'historical_raw_transport':'BothfailedGitmetadatareconstructionsretainedwithoutmovement; exactunauthPUBLICGitfetchclosedraw-objectbinding. APIUTCnormalizedawayactualGit-0500offset. No Ghcredentialretry.'}
    addendum_bytes=(json.dumps(addendum,indent=2)+'\n').encode();(B/'ROOT_CUT_COPY_ADDENDUM.json').write_bytes(addendum_bytes)
    addendum_id={'path':str(B/'ROOT_CUT_COPY_ADDENDUM.json'),'bytes':len(addendum_bytes),'sha256':hashlib.sha256(addendum_bytes).hexdigest(),'first_observed_utc':datetime.now(timezone.utc).isoformat(),'origin':'NEWadditiveprocessbindingpayloadFIRSTIDONCE'}
    result={'status':'ROOT_ADOPTED_ALL_NINE_ACTUAL_CLOSED_PATHS_AND_ACTUAL_CUT_COPY_BINDING','adopted_utc':datetime.now(timezone.utc).isoformat(),'rows':rows,'new_closed_payload_hashes':new_hashes,'reused_closed_payload_IDs':reused,'FINAL_DOCUMENT_IDS_self_reused':cache[str(P/'FINAL_DOCUMENT_IDS.json')],'cut_copy_addendum':addendum_id,'producer_cache_modified':False,'producer_generator_or_math_replayed':False,'self_identity':'Thisadoptionrecordnotselfhashed; anylaternecessaryFIRSTIDonce/cache.'}
    put_new(B/'ROOT_PRODUCER_CLOSURE_ADOPTION.json',result)
    run.finish(result)
except Exception as e:
    run.finish({'status':'FAIL_PRESERVED_NO_AUTOMATIC_RETRY','exception':repr(e)})
    print(str(e),file=sys.stderr)
    raise SystemExit(1)
