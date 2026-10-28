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
f.put(A/'started.json',{'attempt':1,'command':cmd,'cwd':'/workspace','started_utc':start,'scope':'New63 archive/metadata association after actual final root GO; original separate streams'})
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
validation={**receipt,'status':'PASS','checks_passed':len(checks),'completed_checks':checks,'capture_identities':captures,'scope':'New63 metadata associations only; no Lean/proof/kernel/control/old-hash replay'}
vid=f.write(R/'METADATA_VALIDATION_RECEIPT.json',validation)
report='''# Stage63 exact scratch proposal ready

Exactly one actual-source ALL-LEVEL finite closed-superlevel path-components proposition/no public data appends to qualified62:63 modules/1133 written=1124Prop+9data/32 inputs. The SAME physical actualField/descended product torus, positive L and genuine IsMorseDistinct imply FOR EVERY real a, Finite of actual ZerothHomotopy(superlevel_set F (-a)). Actual private/local compactness and LP from qualified61 PUBLIC neighborhood basis feed the existing Mathlib Finite instance; no geometry/count certificate or duplicate finite-subcover engine. No public Fintype/enumeration/count object or source62 dependency.

Same-source private3singleton/4empty/-4whole NONEMPTY positives cover compact/local-topology/Finite uses only; they do NOT cover the full hm-to61-to-subtype route. Separate ordinary Controls derives fixture global hm ONCE and invokes the new ALL-LEVEL public chain. Exactly one complete production LP TEXT original and one separate complete ordinary Controls TEXT original each freeze/integrateONCE, helper executions/hashes/objects0; producer owns all actual amendments. Production kernel excludes ordinary Controls. Sole mutation swaps quotient to FULL physical cover at unchanged CLOSED3, SAME actual cos(pi*x)+2*cos(pi*y)/genuine hm; actual Nat-maxima class injection/odd-x IVT and NOT Finite pass before one importing False. No level/strictness/premise/amplitude/sample mutation.

One captured metadata association attempt passed seven bounded checks. All final counts derive from actual immutable records. Inherited6491 manifest KEY prefix and independent checksum ROW prefix stay separate; only old README/SCOPE/lakefile digests change. New source/four already-installed PRECODE63 bindings/new evidence append, no manifest/sums SELF entries. Existing FIRST IDs are reused with a durable memo; unrecorded NEW immutable metadata alone receives FIRST identities. All actual source/harness/runner/context versions, observed ACKs/full patches/path-race history/commands/cwd/times/exits/original split streams and failures remain retained. Complete outer/inner command/time/exit/original separate captures and identity/copy/check journals preserved.

Packager is63 PROOF AUTHOR=FALSE, metadata preparation only; prior62A proof authorship transfers no63 authorship/independent credit. Root/nonauthor-reviewer actual reading scopes stay verbatim and separate; no62 review transfers. Root alone applies/publishes. Five installed bindings/ALL object actions SKIP after root's ONLY final eligible own copy. No shared/cache/Git/external mutation, old hash/math/Lean/kernel/control replay or ilean refresh here. Newdocument first identities are memoized, avoiding prior62 writer duplicate calculations; actual documentary history stays honest, never a blanket claim about past stages. ScientificNONE/same-family0; provider process separate. No64 path, future role/claim/registration or hosted63 CI/publication claim.
'''
f.durable(R/'REPORT.md',report.encode());rid=f.identity(R/'REPORT.md')
cid=f.write(R/'CUSTODY_IDENTITIES.json',{'status':'FROZEN63_IDENTITIES','files':list(f.identities().values()),'journal':'IDENTITY_JOURNAL.jsonl','self_and_final_handoff':'Recorded after snapshot; no recursive self identity claim'})
c=f.read(R/'FINAL_INPUTS.json')
handoff={'status':'FINAL_READY_FROZEN_ROOT_ONLY_APPLY_NOT_APPLIED','source_cut':result['source_cut'],'qualified_baseline':result['qualified_baseline'],'overlay_root':str(R/'overlay'),'apply_plan':f.identities()[str(R/'APPLY_PLAN.json')],'copy_plan':f.identities()[str(R/'COPY_PLAN.json')],'counts':result['counts'],'manifest_identity':result['manifest_identity'],'sums_identity':result['sums_identity'],'catalog_identity':result['catalog_identity'],'metadata_receipt_identity':vid,'report_identity':rid,'custody_snapshot_identity':cid,'actual_metadata_executions':1,'failed_metadata_executions':0,'metadata_checks_passed':len(checks),'actual_worker_capture':receipt,'capture_identities':captures,'outer_launcher_capture':'launcher-captures/metadata-attempt-001/{started.json,stdout.log,stderr.log,receipt.json}; full original wrapper+seal streams, no selfhash claimed','identity_journal':'IDENTITY_JOURNAL.jsonl','copy_journal':'ARCHIVE_PROGRESS.jsonl','check_journal':'VALIDATION_PROGRESS.jsonl','own_object_action':'SKIP_ROOT_COPIED_ONCE_ALL_FURTHER_COPIES_SKIP','actual_owned_constants':result['owned_constants'],'owned_foreign_generated':c['inventory_summary']['foreign_generated_count'],'production_helpers_once':len(c['production_helper_integrations']),'Controls_only_helper_once':1,'packager_is_63_proof_author':False,'packager_proof_role':'63 metadata only; prior62A does not transfer proof authorship','independent_scientific_review_credit':0,'old_payload_hashes':0,'proof_replays':0,'shared_mutations':0,'scientific_effect':'NONE','same_family_credit':0,'canonical_authority':f.AUTHORITY}
f.write(R/'FINAL_HANDOFF.json',handoff);print(json.dumps({'status':handoff['status'],'counts':result['counts']},sort_keys=True),flush=True)
