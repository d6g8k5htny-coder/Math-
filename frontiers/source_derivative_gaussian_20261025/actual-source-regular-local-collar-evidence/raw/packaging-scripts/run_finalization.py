#!/usr/bin/env python3
"""One future stage66 metadata worker and immutable handoff; no action on import."""
import json,os,subprocess,sys,time
import custody as f
import archive_prepare

def main():
    R=f.R;c=f.read(R/'FINAL_INPUTS.json');archive_prepare.gate(c)
    folder=R/'metadata-attempts/attempt-001'
    f.require(not folder.exists(),'Prior actual66 metadata attempt exists; preserve it and request only affected scoped recovery')
    folder.mkdir(parents=True)
    for row in c['metadata_script_identities']:f.retain(row['source'],row)
    for row in c['existing_file_identities']:
        if not archive_prepare.artifact(row['source']):f.retain(row['source'],row)
    cmd=[sys.executable,str(R/'finalize_metadata.py')];start=f.now();tick=time.monotonic()
    f.put(folder/'STARTED.json',{'attempt':1,'command_argv':cmd,'cwd':'/workspace','start_utc':start,
        'scope':'NEW66 metadata assembly and seven associations only; original split streams, no mathematics/old hashes/shared/external actions'})
    for name in ['custody.py','archive_prepare.py','finalize_metadata.py','capture_boundary.py','run_finalization.py','launch_finalization.py','entry_finalization.py']:
        f.copied(R/name,folder/name)
    code=None;failure=None
    try:
        with (folder/'stdout.log').open('xb') as out,(folder/'stderr.log').open('xb') as err:
            process=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
            code=process.returncode;out.flush();os.fsync(out.fileno());err.flush();os.fsync(err.fileno())
    except BaseException as exc:failure=repr(exc)
    # The child writes its own journal rows; reload instead of sealing stale parent caches.
    f.refresh_progress()
    receipt={'attempt':1,'command_argv':cmd,'cwd':'/workspace','start_utc':start,'end_utc':f.now(),
        'elapsed_seconds':time.monotonic()-tick,'exit_code':code,'spawn_or_worker_exception':failure,
        'stdout':'stdout.log','stderr':'stderr.log','full_actual_capture':True,'old_payload_hashes':0,'proof_replays':0}
    f.put(folder/'execution_receipt.json',receipt)
    captures={}
    for name in ['STARTED.json','stdout.log','stderr.log','execution_receipt.json']:
        f.allow_first_identity(folder/name);captures[name]=f.identity(folder/name)
    if code!=0 or failure is not None:
        f.write(R/'FAILED_METADATA_ATTEMPT.json',{'status':'ACTUAL_FAILURE_PRESERVED_SCOPED_RECOVERY_ONLY',
            'receipt':receipt,'capture_identities':captures,'reuse':'Retain completed identity/copy/check journals; no blind attempt restart or proof replay'})
        return code if code is not None and code>0 else 1
    result=f.read(R/'ASSEMBLY_RESULT.json')
    checks=[json.loads(line) for line in (R/'VALIDATION_PROGRESS.jsonl').read_text().splitlines() if json.loads(line)['event']=='check_passed']
    f.require(len(checks)==7,'Exactly seven final66 metadata associations')
    validation={**receipt,'status':'PASS','checks_passed':len(checks),'completed_checks':checks,
        'capture_identities':captures,'scope':'NEW66 metadata associations only; no Lean/proof/kernel/control/old-hash replay'}
    vid=f.write(R/'METADATA_VALIDATION_RECEIPT.json',validation)
    report='''# Stage66 exact scratch proposal ready

Exactly one actual quotient regular-local-collar proposition/no public data appends to qualified65:66modules/1136written=1127Prop+9data/32inputs. Original actual nonzero-fderiv yields EVERY prescribed open O ONE centered rho/phi/exact finite-Pi2 target and ordered F=c+coordinate1. SAME phi/rho serves ALL |epsilon|<rho NONEMPTY path-connected CLOSED uppercuts AND level slices. No64/65 mathematical dependency or desired chart/certificate/norm-isometry premise.

Both actual partial alternatives, seam/small physical O and zero/positive/negative exact level-slice witnesses are retained. At most ONE complete private physical-adapter TEXT original is integrated once with zero helper executions/hashes/objects; producer owns all joins/actual positives/ordinary Controls/counterproof/amendments/executions. Separate complete production and ordinary inventories/std3 and EXACTLY ONE final production named kernel qualify distinct scopes. Sole mutation removes only nonzero-fderiv at the SAME actual maximum0/c3; independently passed ordinary global bound contradicts the inverse positive coordinate target before ONE importingFalse. No ordinary named kernel.

One metadata cycle passes seven bounded associations. All final sizes/counts/IDs/worker and outer/entry capture schemas derive from actual frozen inputs. Original initial external root65-labelled freeze and dedicated66 captures, initial known-EMPTY metadata hash issue/forward fix, all versions/full actual patches/ACK/freezes/development failures and reading limits remain honest. Current root and nonauthor technical FULL/structured/bounded reading are separate; no old aggregate/source/math verification replay. Current packager proof-authorFALSE/independentcredit0/scienceNONE/samefamily0; historical65 script provenance does not assign current proof/review roles.

Inherited9685 manifest KEY prefix and independent checksum ROW prefix are preserved separately. Only README/SCOPE/lakefile old digests change; source/four published-before-code proper66 documents/new evidence append without self entries. Five installed bindings and ALL object actions SKIP after root ONLY eligible new own-object copy once. Root alone applies/Git/cache/external normal publication. Closed metadata outer/entry captures and immutable handoff are separate later publication tail, no recursive archive reseal. Existing65 CI is not66 CI. Future67 proper root EXTRA docs are excluded66archive/manifest/registry. OpenDraft/noReady/noMerge; completed applicable verification reusable, provider-distinct process separate. Broader research remains ACTIVE_UNMET.
'''
    rid=f.text(R/'REPORT.md',report)
    cid=f.write(R/'CUSTODY_IDENTITIES.json',{'status':'FROZEN66_IDENTITIES','files':list(f.identities().values()),
        'journal':'IDENTITY_JOURNAL.jsonl','self_and_handoff':'Recorded after snapshot; no recursive self identity'})
    handoff={'status':'FINAL_READY_FROZEN_ROOT_ONLY_APPLY_NOT_APPLIED','source_cut':result['source_cut'],'qualified_baseline':f.BASE,
        'overlay_root':str(R/'overlay'),'apply_plan':f.identities()[str(R/'APPLY_PLAN.json')],
        'copy_plan':f.identities()[str(R/'COPY_PLAN.json')],'counts':result['counts'],'manifest_identity':result['manifest_identity'],
        'sums_identity':result['sums_identity'],'catalog_identity':result['catalog_identity'],'metadata_receipt_identity':vid,
        'report_identity':rid,'custody_snapshot_identity':cid,'actual_metadata_executions':1,'failed_metadata_executions':0,
        'metadata_checks_passed':len(checks),'actual_worker_capture':receipt,'capture_identities':captures,
        'entry_outer_capture':'{entry,outer}-captures/metadata-attempt-001/{STARTED.json,stdout.log,stderr.log,RECEIPT.json}; actual wrappers close later, no premature completion or selfhash',
        'identity_journal':'IDENTITY_JOURNAL.jsonl','copy_journal':'ARCHIVE_PROGRESS.jsonl','check_journal':'VALIDATION_PROGRESS.jsonl',
        'own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','production_helpers_once':len(c['production_helper_integrations']),
        'Controls_only_helper_once':0,'packager_is_66_proof_author':False,'packager_role':'66 metadata only',
        'independent_scientific_review_credit':0,'old_payload_hashes':0,'proof_replays':0,'shared_mutations':0,
        'scientific_effect':'NONE','same_family_credit':0,'canonical_authority':f.AUTHORITY}
    f.write(R/'FINAL_HANDOFF.json',handoff)
    print(json.dumps({'status':handoff['status'],'counts':result['counts']},sort_keys=True),flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
