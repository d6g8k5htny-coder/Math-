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
f.put(A/'started.json',{'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'scope':'New64 archive/metadata association after actual final root GO; original separate streams'})
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
validation={**receipt,'status':'PASS','checks_passed':len(checks),'completed_checks':checks,'capture_identities':captures,'scope':'New64 metadata associations only; no Lean/proof/kernel/control/old-hash replay'}
vid=f.write(R/'METADATA_VALIDATION_RECEIPT.json',validation)
report='''# Stage64 exact scratch proposal ready

Exactly ONE actual quotient saddle-collar proposition/no public data appends to qualified63:64 modules/1134 written=1125Prop+9data/32 inputs. Positive original period/sample, actual point criticality and FULL complementary Hessian inertia1 derive, for every ambient open O, ONE positive radius and injective quotient chart with source inside O/EXACT centered Point2 Pi-norm target ball/ordered actual saddle identity. SAME chart supplies both nonempty strict branches/JoinedIn equivalence and ALL nonnegative-delta lower traces. No global hm, bare index, desired chart/certificate or norm-isometry premise.

Same normalized original cos(pi*x)+2*cos(pi*y) actual sample supplies both saddles, small O and seam controls with actual local hypotheses. TWO complete private production TEXT authors chart/geometry each freeze then integrateONCE, helper executions/hashes/objects0; producer owns actual amendments and ALL ordinary Controls, no extra ordinary helper. Production kernel excludes ordinary. Sole fixed-chart mutation claims WHOLE strict trace path connected; independent same-chart inverse(0,+/-rho/2) nonempty witnesses/coordinate1 IVT counterproof passes before ONE importing False. No global-hm fixture proof, changed chart/field/level/carrier/radius or second mutation.

One fully captured metadata cycle passed seven bounded associations. All counts/IDs come from actual immutable records. Actual mathematical verification and documentary calls remain separately tagged by scope_kind, with all original source/harness/runner/context snapshots/history/observed ACKs/full actual patches/failures/commands/cwd/times/exits/split streams retained. The prospective important-documentary OUTER split-capture requirement is recorded before execution; actual retained captures and any explicit limits remain distinct, with each new ID cached once. Any actual capture limit remains explicitly disclosed, never backdated or fabricated by replaying old work. THIS metadata worker and outer wrapper have full original separate captures/durable identity/copy/check journals.

Inherited6822 manifest KEY prefix and independent checksum ROW prefix remain separate; only README/SCOPE/lakefile old digests change. Append own source/four PRECODE64 bindings/new64 evidence without manifest/sums SELF entries. Existing IDs reused, unrecorded NEW immutable metadata alone first-identified. Five installed bindings and ALL objects SKIP after root's single eligible final own copy. No old proof/hash/kernel/control/object campaign or ilean refresh. Root alone applies/publishes; no shared/Git/cache/external action here.

Packager64 proof-author FALSE/prior62A disclosed, independent credit0. Root/final nonauthor reviewer actual reading scopes and limits remain separately attributed; no63 review transfers. ScientificNONE/same-family0; provider process separate from reusable mathematics. Allfuture65 proper root EXTRA docs excluded64archive/manifest/registry. No public uppercut/adjacency/critical-event/exhaustive elder/once-count/Borel/Rice/PairLaw/Parent or wider-goal completion, hosted64CI or remote64publication claimed.
'''
f.durable(R/'REPORT.md',report.encode());rid=f.identity(R/'REPORT.md')
cid=f.write(R/'CUSTODY_IDENTITIES.json',{'status':'FROZEN64_IDENTITIES','files':list(f.identities().values()),'journal':'IDENTITY_JOURNAL.jsonl','self_and_final_handoff':'Recorded after snapshot; no recursive self identity claim'})
c=f.read(R/'FINAL_INPUTS.json')
handoff={'status':'FINAL_READY_FROZEN_ROOT_ONLY_APPLY_NOT_APPLIED','source_cut':result['source_cut'],'qualified_baseline':result['qualified_baseline'],'overlay_root':str(R/'overlay'),'apply_plan':f.identities()[str(R/'APPLY_PLAN.json')],'copy_plan':f.identities()[str(R/'COPY_PLAN.json')],'counts':result['counts'],'manifest_identity':result['manifest_identity'],'sums_identity':result['sums_identity'],'catalog_identity':result['catalog_identity'],'metadata_receipt_identity':vid,'report_identity':rid,'custody_snapshot_identity':cid,'actual_metadata_executions':1,'failed_metadata_executions':0,'metadata_checks_passed':len(checks),'actual_worker_capture':receipt,'capture_identities':captures,'outer_launcher_capture':'launcher-captures/metadata-attempt-001/{started.json,stdout.log,stderr.log,receipt.json}; full original wrapper+seal streams, no selfhash claimed','identity_journal':'IDENTITY_JOURNAL.jsonl','copy_journal':'ARCHIVE_PROGRESS.jsonl','check_journal':'VALIDATION_PROGRESS.jsonl','own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','actual_owned_constants':result['owned_constants'],'owned_foreign_generated':c['inventory_summary']['foreign_generated_count'],'production_helpers_once':len(c['production_helper_integrations']),'Controls_only_helper_once':0,'packager_is_64_proof_author':False,'packager_proof_role':'64 metadata only; prior62A does not transfer proof authorship','independent_scientific_review_credit':0,'old_payload_hashes':0,'proof_replays':0,'shared_mutations':0,'scientific_effect':'NONE','same_family_credit':0,'canonical_authority':f.AUTHORITY}
f.write(R/'FINAL_HANDOFF.json',handoff);print(json.dumps({'status':handoff['status'],'counts':result['counts']},sort_keys=True),flush=True)
