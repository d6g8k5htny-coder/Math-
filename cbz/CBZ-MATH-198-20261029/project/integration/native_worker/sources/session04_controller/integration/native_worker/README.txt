Native source-exposed reuse of all49 original P15 endpoints

The trusted native worker now advertises57 tasks: the original8 plus all49
p15.<OriginalTargetName> IDs in endpoint_tasks.json. Each new fixed action
reuse_<OriginalTargetName> supplies a checked wrapper of the exact original target.
Generic targets universally bind finite X, Fintype, DecidableEq and RealizedData F;
concrete targets retain their original Prop. Wrappers live in
../../formal/Integration/EndpointTasks.lean and import the unchanged completion
proof chain. All source-exposed records remain training_eligible=false.

The original closedGate/ExprDag v2 acceptance code is byte-identical to the sealed
baseline. Acceptance still requires a closed exact requested target, empty-context
kernel body/type check, checked theorem insertion and transitive axiom allowlist.
The new wrapper constants are trusted imported source proofs; this is explicit
proof reuse, not discovery, learning or general-purpose typed lemma synthesis.

Executed evidence
  evidence/build01/results.json —6 fresh native modules compiled
  evidence/session02/results.json — actual49 exports, fresh49 rechecks, controls
  evidence/saved_verify_final.json — saved request/stdout/export/receipt bindings
  evidence/unit_normal_final.txt / unit_optimized_final.txt —7 tamper tests each

Run offline without Lean:
  python -B verify_native_saved.py
  python -B -m unittest discover -s tests -v
  python -B -O -m unittest discover -s tests -v
The offline checker starts no kernel and creates no new proof acceptance.

For a fresh native campaign, after preparing the root formal cache:
  python -B native.py build --build-dir build/NEW --output evidence/NEW_BUILD --formal-cache /ABS/FORMAL_CACHE
  python -B native.py sessions --build-dir build/NEW --output evidence/NEW_CAMPAIGN
Both commands hold ../../.native.lock. All compiles and Python session controllers
use ../../support/process.py run_recorded with120s limits; Lean runs -j1 -M11000.
Controller transport is the new engine_audit LeanWorker directly, never the old
RuntimeConfig.worker factory. The Linux exec guard sets PR_SET_PDEATHSIG(SIGKILL)
so outer-controller timeout cannot leave an orphan Lean worker. These operational
unsafe bootstrap/guard components are outside the formal proof import graph.

The native build records all17 resolved completion dependency .olean hashes and
current exact source/catalog bindings. build01/session02 use disclosed exploratory
root/prior caches. Root final fresh-cache proof-chain/body/type/axiom audit is a
separate evidence boundary; it includes all49 original endpoints and wrappers.
Toolchains/precompiled Mathlib/shared libraries remain externally trusted. Exclude
integration/native_worker/build from portable source inventories/ZIPs.

Lifecycle evidence
session01 used the previous0.3s grace: budget worker acknowledged shutdown and was
then forcibly terminated(-9), despite mathematically valid proofs and confirmed
handle drops. That receipt and exact old worker bytes are preserved. The new
transport allows configurable positive finite shutdown_grace<=5s, default2s,
with explicit acknowledgement/forced-termination/grace/teardown receipts.
Session02 repeated the complete campaign: all4 workers returned0, acknowledgement
true, forced termination false; measured teardown0.436--0.511s explains the prior
cutoff. Stubborn-process bounded-kill tests remain. A shutdown acknowledgement
never substitutes for an accepted proof. Valid proof and cleanup facts are separate.

The32-request native phase accepts3 identity proofs, then reports request_capacity
with all handles confirmed dropped and3 requests reserved before shutdown; an
additional fresh worker rechecks its last accepted proof. Wide frontier eviction,
restart serialization, eligible corpus and trained routing remain separate gaps.
No speedup claim follows. Native workers still peak around9GiB RSS.

CURRENT FINISH-ONLY CONTRIBUTION SNAPSHOT
Following the CBZ0 freeze directive, the adapter is self-contained:
pinned_runtime.py is a byte-identical copied selector and its inventory reference
is local; cold native execution no longer imports earlier package Python code.
The one-time prepare.py generator retains its explicitly historical source input.

Current acceptance evidence is build02 +session04. Build02 uses the complete
fresh root build/final02 cache; --formal-evidence explicitly binds its passing
fresh result, original17 source hashes and actual compiled output hashes, plus
wrapper source. There is no prior-cache fallback. Session04 repeats the full
49+49+three-control+32-request campaign with that source/output boundary.
All4 current native workers exit0/ACKtrue/forcedfalse. Offline bindings and9
normal/9optimized tests pass: evidence/saved_verify_final04.json and
unit_{normal,optimized}_final04.txt. Earlier01/02/03 evidence remains historical;
session03 repeated the old adapter before the local selector bridge was completed.

Cold replay can use fresh user-chosen build/evidence directories outside ROOT:
  python -B native.py build --build-dir /ABS/NEW_BUILD --output /ABS/NEW_BUILD_EVIDENCE --formal-cache /ABS/FRESH_FORMAL_CACHE --formal-evidence /ABS/FRESH_FORMAL_RESULTS.json
  python -B native.py sessions --build-dir /ABS/NEW_BUILD --output /ABS/NEW_CAMPAIGN
If ROOT/checksum_manifest.json exists, both writable directories must be outside
the payload. An existing ROOT native lock is opened read-only; if omitted from a
sealed payload, replay uses a sibling shared lock for that payload. Destination
and missing/tampered formal output/source binding controls run offline. A supplied
cache missing any required module rejects; no old cache is consulted.

verification_index.json identifies the current contribution for import into the
CBZ repository. This work creates no additional standalone sealed package.
