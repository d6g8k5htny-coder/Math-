#!/usr/bin/env python3
"""One future60 metadata worker and seal; no mathematical execution."""
from pathlib import Path
import json,subprocess,sys,time
import custody as f
R=f.R;A=R/'metadata-attempts/attempt-001'
if A.exists():raise RuntimeError('Prior actual metadata attempt preserved; no automatic restart/replay.')
A.mkdir(parents=True);f.syncdirs(A)
cmd=[sys.executable,str(R/'finalize_metadata.py')];start=f.now();tick=time.monotonic()
f.put(A/'started.json',{'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'scope':'New60 archive/metadata association after actual final rootGO; full original separate streams.'})
for n in ['custody.py','archive_prepare.py','finalize_metadata.py','run_finalization.py','launch_finalization.py']:
    f.durable(A/n,(R/n).read_bytes());f.identity(A/n)
with (A/'stdout.log').open('wb')as out,(A/'stderr.log').open('wb')as err:
    proc=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
    out.flush();f.os.fsync(out.fileno());err.flush();f.os.fsync(err.fileno())
f.syncdirs(A)
receipt={'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'ended_utc':f.now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':proc.returncode,'stdout':'stdout.log','stderr':'stderr.log','full_actual_capture':True,'old_hashes':0,'proof_replays':0}
f.put(A/'execution_receipt.json',receipt);captures={n:f.identity(A/n)for n in ['started.json','stdout.log','stderr.log','execution_receipt.json']}
if proc.returncode:
    f.write(R/'FAILED_METADATA_ATTEMPT.json',{'status':'ACTUAL_FAILURE_PRESERVED_SCOPED_CONTINUATION_ONLY','receipt':receipt,'captures':captures,'reuse_completed_checks_and_identities':'VALIDATION_PROGRESS.jsonl/IDENTITY_JOURNAL.jsonl; invalidate only affected scope after concrete defect.'})
    print((A/'stderr.log').read_text());sys.exit(proc.returncode)
result=f.read(R/'ASSEMBLY_RESULT.json');checks=[json.loads(x)for x in (R/'VALIDATION_PROGRESS.jsonl').read_text().splitlines()if json.loads(x)['event']=='check_passed']
validation={**receipt,'status':'PASS','checks_passed':len(checks),'completed_checks':checks,'capture_identities':captures,'scope':'New60 metadata associations only; no Lean/proof/kernel/control/oldhash replay.'}
vid=f.write(R/'METADATA_VALIDATION_RECEIPT.json',validation)
report='''# Stage60 exact scratch proposal ready

One actual-source local C1 quadratic model proposition/no public data appends to qualified59:60modules/1130written=1121Prop+9data/32inputs. All actual production/ordinary attempts and their original RECORD.json/stdout.txt/stderr.txt, source/harness snapshots/helper originals/full actual patches remain retained. Three production helper sections are covered by the owned production strict/inventory/onekernel. Ordinary Controls and its independent actual weighted1/omitted2 counterproof and sole importing-False have separate qualification; production kernel does not cover them.

One actual captured metadata attempt passed bounded new associations. Old5458 manifest-key and independent checksum-row prefixes are preserved separately; only README/SCOPE/lakefile inherited digests change. New source/four root-installed PRECODE bindings and new evidence append; no manifest/sums SELF entry. Durable identity/copy/check intents/results and full worker/wrapper/seal command/time/exit/original separate streams are retained. Recorded source/helper/evidence identities are reused; only unrecorded new immutable packaging payload receives a first identity.

Root alone applies/publishes. Five installed bindings and all objects are SKIP after root's one eligible own-object copy. No shared metadata/config/cache/Git/external mutation, old hash, proof/kernel/control replay or ilean refresh occurred here. Actual root/nonauthor-reviewer reading scopes stay verbatim. Packager authored branchA and has no independent scientific review credit; same-family0/scientificNONE. No probability/globalMorse/quotient/slab/elder/counting/Rice/Parent or Cinf-chart claim is inferred. Future/current-source hostedCI or remote publication is not claimed by this scratch proposal.
'''
f.durable(R/'REPORT.md',report.encode());rid=f.identity(R/'REPORT.md')
cid=f.write(R/'CUSTODY_IDENTITIES.json',{'status':'FROZEN60_IDENTITIES','files':list(f.identities().values()),'journal':'IDENTITY_JOURNAL.jsonl','self_and_final_handoff':'Recorded after snapshot; no recursive self identity claim.'})
classification=f.read(f.P/'INVENTORY_CLASSIFICATION.json')
handoff={'status':'FINAL_READY_FROZEN_ROOT_ONLY_APPLY_NOT_APPLIED','source_cut':result['source_cut'],'qualified_baseline':result['qualified_baseline'],'overlay_root':str(R/'overlay'),'apply_plan':f.identities()[str(R/'APPLY_PLAN.json')],'copy_plan':f.identities()[str(R/'COPY_PLAN.json')],'counts':result['counts'],'manifest_identity':result['manifest_identity'],'sums_identity':result['sums_identity'],'catalog_identity':result['catalog_identity'],'metadata_receipt_identity':vid,'report_identity':rid,'custody_snapshot_identity':cid,'actual_metadata_executions':1,'failed_metadata_executions':0,'metadata_checks_passed':len(checks),'actual_worker_capture':receipt,'capture_identities':captures,'outer_launcher_capture':'launcher-captures/metadata-attempt-001/{started.json,stdout.log,stderr.log,receipt.json}; full actual wrapper+seal streams; no selfhash claimed','identity_journal':'IDENTITY_JOURNAL.jsonl','copy_journal':'ARCHIVE_PROGRESS.jsonl','check_journal':'VALIDATION_PROGRESS.jsonl','own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','actual_owned_constants':result['owned_constants'],'owned_foreign_generated':len(classification['foreign_generated_names']),'production_helpers_once':3,'Controls_only_helper_once':1,'packager_is_branch_A_proof_author':True,'independent_scientific_review_credit':0,'old_payload_hashes':0,'proof_replays':0,'shared_mutations':0,'scientific_effect':'NONE','same_family_credit':0,'canonical_authority':f.AUTHORITY}
f.write(R/'FINAL_HANDOFF.json',handoff);print(json.dumps({'status':handoff['status'],'counts':result['counts']},sort_keys=True),flush=True)
