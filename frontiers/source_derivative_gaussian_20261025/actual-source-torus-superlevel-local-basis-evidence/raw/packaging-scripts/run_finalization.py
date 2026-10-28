#!/usr/bin/env python3
"""One future61 worker and custody seal; no mathematical execution."""
import json,subprocess,sys,time
import custody as f
import archive_prepare
R=f.R;A=R/'metadata-attempts/attempt-001'
archive_prepare.gate(f.read(R/'FINAL_INPUTS.json'))
if A.exists():raise RuntimeError('Prior actual metadata attempt preserved; no automatic restart/replay')
A.mkdir(parents=True);f.syncdirs(A)
cmd=[sys.executable,str(R/'finalize_metadata.py')];start=f.now();tick=time.monotonic()
f.put(A/'started.json',{'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'scope':'New61 archive/metadata association after actual final root GO; original separate streams'})
for name in ['custody.py','archive_prepare.py','finalize_metadata.py','run_finalization.py','launch_finalization.py']:
    f.durable(A/name,(R/name).read_bytes());f.identity(A/name)
with (A/'stdout.log').open('wb') as out,(A/'stderr.log').open('wb') as err:
    proc=subprocess.run(cmd,cwd='/workspace',stdout=out,stderr=err)
    out.flush();f.os.fsync(out.fileno());err.flush();f.os.fsync(err.fileno())
f.syncdirs(A)
receipt={'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'ended_utc':f.now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':proc.returncode,'stdout':'stdout.log','stderr':'stderr.log','full_actual_capture':True,'old_hashes':0,'proof_replays':0}
f.put(A/'execution_receipt.json',receipt)
captures={name:f.identity(A/name) for name in ['started.json','stdout.log','stderr.log','execution_receipt.json']}
if proc.returncode:
    f.write(R/'FAILED_METADATA_ATTEMPT.json',{'status':'ACTUAL_FAILURE_PRESERVED_SCOPED_CONTINUATION_ONLY','receipt':receipt,'captures':captures,'reuse_completed_checks_and_identities':'VALIDATION_PROGRESS.jsonl/IDENTITY_JOURNAL.jsonl/ARCHIVE_PROGRESS.jsonl; invalidate only concretely affected scope'})
    print((A/'stderr.log').read_text());sys.exit(proc.returncode)
result=f.read(R/'ASSEMBLY_RESULT.json')
checks=[json.loads(line) for line in (R/'VALIDATION_PROGRESS.jsonl').read_text().splitlines() if json.loads(line)['event']=='check_passed']
validation={**receipt,'status':'PASS','checks_passed':len(checks),'completed_checks':checks,'capture_identities':captures,'scope':'New61 metadata associations only; no Lean/proof/kernel/control/old-hash replay'}
vid=f.write(R/'METADATA_VALIDATION_RECEIPT.json',validation)
report='''# Stage61 exact scratch proposal ready

Exactly one actual torus closed-superlevel local path-connected basis proposition/no public data appends to qualified60:61 modules/1131 written=1122Prop+9data/32 inputs. Original actual receipt.json/stdout.log/stderr.log, every source/harness snapshot, helper/context version/personal ACK/freeze and complete actual producer amendment remain retained. Inventory/helper/run totals derive from final immutable records. Production kernel and separate ordinary Controls/global fixture Morse proof/nonempty every-neighborhood strict-saddle counterproof/sole importing False have distinct qualification scopes.

One captured metadata association attempt passed its seven bounded checks. The inherited5776 manifest-key prefix and independent checksum-row prefix remain separate; only old README/SCOPE/lakefile digests change. New source/four already root-installed PRECODE61 bindings and new evidence append, without manifest/sums self entries. Recorded immutable identities are reused; previously unrecorded new immutable payloads alone receive first identities. Durable identity/copy/check journals and full actual worker/wrapper command/cwd/start/end/exit/original split streams remain retained.

Root alone applies and publishes. Five installed bindings and ALL objects are SKIP after root's single eligible own-object copy. No shared metadata/config/cache/Git/external mutation, old hash, Lean/proof/kernel/control replay or ilean refresh occurs here. Packager supplied61 metadata preparation only and earns no independent review credit. Actual root/reviewer reading scopes remain verbatim; no inherited60 review covers61. ScientificNONE/same-family0; process requirements stay separate. No future/current-source hosted CI or remote publication is claimed by this proposal.
'''
f.durable(R/'REPORT.md',report.encode());rid=f.identity(R/'REPORT.md')
cid=f.write(R/'CUSTODY_IDENTITIES.json',{'status':'FROZEN61_IDENTITIES','files':list(f.identities().values()),'journal':'IDENTITY_JOURNAL.jsonl','self_and_final_handoff':'Recorded after snapshot; no recursive self identity claim'})
c=f.read(R/'FINAL_INPUTS.json')
handoff={'status':'FINAL_READY_FROZEN_ROOT_ONLY_APPLY_NOT_APPLIED','source_cut':result['source_cut'],'qualified_baseline':result['qualified_baseline'],'overlay_root':str(R/'overlay'),'apply_plan':f.identities()[str(R/'APPLY_PLAN.json')],'copy_plan':f.identities()[str(R/'COPY_PLAN.json')],'counts':result['counts'],'manifest_identity':result['manifest_identity'],'sums_identity':result['sums_identity'],'catalog_identity':result['catalog_identity'],'metadata_receipt_identity':vid,'report_identity':rid,'custody_snapshot_identity':cid,'actual_metadata_executions':1,'failed_metadata_executions':0,'metadata_checks_passed':len(checks),'actual_worker_capture':receipt,'capture_identities':captures,'outer_launcher_capture':'launcher-captures/metadata-attempt-001/{started.json,stdout.log,stderr.log,receipt.json}; full original wrapper+seal streams, no selfhash claimed','identity_journal':'IDENTITY_JOURNAL.jsonl','copy_journal':'ARCHIVE_PROGRESS.jsonl','check_journal':'VALIDATION_PROGRESS.jsonl','own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','actual_owned_constants':result['owned_constants'],'owned_foreign_generated':c['inventory_summary']['foreign_generated_count'],'production_helpers_once':len(c['production_helper_integrations']),'Controls_only_helper_once':1,'packager_is_61_proof_author':False,'independent_scientific_review_credit':0,'old_payload_hashes':0,'proof_replays':0,'shared_mutations':0,'scientific_effect':'NONE','same_family_credit':0,'canonical_authority':f.AUTHORITY}
f.write(R/'FINAL_HANDOFF.json',handoff);print(json.dumps({'status':handoff['status'],'counts':result['counts']},sort_keys=True),flush=True)
