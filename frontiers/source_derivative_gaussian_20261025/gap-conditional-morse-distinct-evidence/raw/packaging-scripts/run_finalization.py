#!/usr/bin/env python3
"""One actual future metadata worker + durable result seal; never any Lean/proof execution."""
from pathlib import Path
import json,subprocess,sys,time
import custody as f
R=f.R;A=R/'metadata-attempts/attempt-001'
if A.exists():raise RuntimeError('Prior actual metadata attempt preserved; no automatic restart or check replay.')
A.mkdir(parents=True);f.syncdirs(A)
cmd=[sys.executable,str(R/'finalize_metadata.py')];start=f.now();tick=time.monotonic()
f.put(A/'started.json',{'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'scope':'Only new59 scratch archive/metadata association after actual final rootGO; full actual stdout/stderr.'})
for n in ['custody.py','archive_prepare.py','finalize_metadata.py','run_finalization.py','launch_finalization.py']:
    f.durable(A/n,(R/n).read_bytes());f.identity(A/n)
with (A/'stdout.log').open('wb')as out,(A/'stderr.log').open('wb')as err:
    proc=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
    out.flush();f.os.fsync(out.fileno());err.flush();f.os.fsync(err.fileno())
f.syncdirs(A)
receipt={'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'ended_utc':f.now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':proc.returncode,'stdout':'stdout.log','stderr':'stderr.log','full_actual_capture':True,'old_hashes':0,'proof_replays':0}
f.put(A/'execution_receipt.json',receipt)
captures={n:f.identity(A/n)for n in ['started.json','stdout.log','stderr.log','execution_receipt.json']}
if proc.returncode:
    f.write(R/'FAILED_METADATA_ATTEMPT.json',{'status':'ACTUAL_FAILURE_PRESERVED_SCOPED_CONTINUATION_ONLY','receipt':receipt,'captures':captures,'reuse_completed_checks_and_identities':'VALIDATION_PROGRESS.jsonl and IDENTITY_JOURNAL.jsonl; invalidate only affected checks after a concrete defect.'})
    print((A/'stderr.log').read_text());sys.exit(proc.returncode)
result=f.read(R/'ASSEMBLY_RESULT.json');checks=[json.loads(x)for x in (R/'VALIDATION_PROGRESS.jsonl').read_text().splitlines()if json.loads(x)['event']=='check_passed']
validation={**receipt,'status':'PASS','checks_passed':len(checks),'completed_checks':checks,'capture_identities':captures,'scope':'New59 metadata associations only; no Lean/kernel/control/proof/oldhash replay.'}
vid=f.write(R/'METADATA_VALIDATION_RECEIPT.json',validation)
report='''# Stage59 exact scratch proposal ready

One module/one proposition appends to qualified58:59modules/1129written=1120Prop+9data/32inputs. All original failures, final receipts/split streams/source-harness snapshots/helper originals/full actual patches and historical pending records are retained. Four production helper sections and the fifth Controls-only section retain separate qualification coverage. The sole DBtheta negative keeps its immutable Controls003 binding; the later positive-only companion is not represented as its import.

Exactly one metadata attempt passed its bounded new association checks. Worker and outer wrapper command/cwd/start/end/exit/full original separate streams are retained; identity/copy/check intents and results are durably synced before advancing. Recorded identities are reused and only unrecorded new immutable packaging payload receives a first identity. Old manifest-key and independent checksum-row prefixes are preserved separately. Only README/SCOPE/lakefile inherited digests change; no manifest/sums self entry.

Root alone applies/publishes. Five installed bindings and all objects are SKIP; the eligible own object was already root-copied once. No shared repository/config/cache/Git/external action or math replay occurred here. Current-source hostedCI/publication is not claimed. Actual root/reviewer reading scopes remain verbatim; no inherited58review or independent-family/scientific acceptance credit is inferred. Same-family0/scientificNONE; process separate from mathematical evidence.
'''
f.durable(R/'REPORT.md',report.encode());rid=f.identity(R/'REPORT.md')
cid=f.write(R/'CUSTODY_IDENTITIES.json',{'status':'FROZEN59_IDENTITIES','files':list(f.identities().values()),'journal':'IDENTITY_JOURNAL.jsonl','self_and_final_handoff':'Their identities are recorded after this snapshot; no recursive self identity claim.'})
handoff={'status':'FINAL_READY_FROZEN_ROOT_ONLY_APPLY_NOT_APPLIED','source_cut':result['source_cut'],'qualified_baseline':result['qualified_baseline'],'overlay_root':str(R/'overlay'),'apply_plan':f.identities()[str(R/'APPLY_PLAN.json')],'copy_plan':f.identities()[str(R/'COPY_PLAN.json')],'counts':result['counts'],'manifest_identity':result['manifest_identity'],'sums_identity':result['sums_identity'],'catalog_identity':result['catalog_identity'],'metadata_receipt_identity':vid,'report_identity':rid,'custody_snapshot_identity':cid,'actual_metadata_executions':1,'failed_metadata_executions':0,'metadata_checks_passed':len(checks),'actual_worker_capture':receipt,'capture_identities':captures,'outer_launcher_capture':'launcher-captures/metadata-attempt-001/{started.json,stdout.log,stderr.log,receipt.json}; full actual wrapper+seal streams; no selfhash claimed','identity_journal':'IDENTITY_JOURNAL.jsonl','copy_journal':'ARCHIVE_PROGRESS.jsonl','check_journal':'VALIDATION_PROGRESS.jsonl','own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','actual_owned_constants':167,'owned_foreign_generated':2,'production_helpers_once':4,'Controls_only_helper_once':1,'source60_uninspected':True,'old_payload_hashes':0,'proof_replays':0,'shared_mutations':0,'scientific_effect':'NONE','same_family_credit':0,'canonical_authority':f.AUTHORITY}
f.write(R/'FINAL_HANDOFF.json',handoff);print(json.dumps({'status':handoff['status'],'counts':result['counts']},sort_keys=True),flush=True)
