# Proposed adapter hosted development contract — UNSELECTED / UNOPENED

This is authored source only. No local script validation, inert control, Lean,
Lake, compiler, kernel checker, mathematical program, or CI run was executed.
Actual distinct pre-execution source review and a later explicit parent
selection remain required. This file does not admit itself.

The source target is conditional transport of explicit Euclidean closed-level
LPC to the literal descended-height torus quotient, plus its existing quotient
attainment consumer. Euclidean LPC remains an input. This is root claim
5b03a98b-71a4-43b7-a12e-d52c45e21681 / Work Events2507 assistance, not C299's ridge.
org=0, human=0, scientific effect NONE. The original 80-line candidate is
3981 bytes, SHA2561e0450504de823c0db0c666c0cae3dea133c9bca3e05e746949491fca4a481a1.

## Exact prospective publication/event scope

Repository d6g8k5htny-coder/Math-, exact base
8c226134ac0a0169dbb43311082e5353ed5c922c. Proposed new branch:
codex/quotient-closed-superlevel-lpc-adapter-20261020.
Only additions below frontiers/quotient_closed_superlevel_lpc_adapter_20261020/
and .github/workflows/quotient-closed-superlevel-lpc-adapter.yml are eligible.
Parent's selected operator shape is create the fresh named branch at the exact
base first, then one guarded expected-old-head update from that base to the
reviewed leaf. The formal event must have before==exact base, after==tested leaf,
created=false, forced=false, deleted=false, exact branch and run attempt1.
The leaf has exactly one parent, the exact base. No PR opening, workflow_dispatch,
main push, schedule, workflow_call, subsequent update, or rerun is admitted here.
The external parent must bind the actual commit/tree/manifest/workflow and actual
nonauthor review before publishing a ref. Source code cannot establish its own
external admission. No ref or native publication was performed in this unit.

## Existing pinned setup and explicit bootstrap allowance

Use unchanged formal/lean-toolchain, lakefile.toml and lake-manifest.json:
Lean4.34.1 release source commit5045d0056413266e57c625dcd7c365b10e377c52;
Mathlibd13f23b723b8a846827a245b89c10fc7d3f11612; all nine dependency revisions
in DEPENDENCY_LOCK.json. Configuration byte hashes are in the source manifest.

The pinned leanprover/lean-action@f061402b660e0c34644504b324e830f2991d4865
is permitted, IF a later distinct contract selects it, in one bootstrap step
with a15-minute platform timeout, build/test/lint/auto-config false,
use-mathlib-cache true and use-github-cache false. This explicitly permits
installation and dependency/cache utility compilation and cache download.
It does not compile these local proof modules and does not establish their
precompiled availability. No cold Mathlib theorem build or fallback is allowed.

Bootstrap is not claimed to use only one Lean process: the action invokes
lake exe cache get, and this packet does not qualify a Lake-worker limiter.
Known cache-utility source closure is18 Cache modules plus
Batteries.Tactic.OpenPrivate and bundled Lean/Lake modules. No18-helper manual
bootstrap is selected. Cache/Requests.lean at the Mathlib pin has curl retry5
(up to6 attempts per transfer) and HTTPS redirect max5; parallel download
concurrency is inherited from that pinned client/curl, NOT separately bounded
by this proposal. The single whole bootstrap15-minute platform deadline bounds
this allowance. There are zero outer bootstrap retries and zero compiler,
source-program, workflow or unchanged native retries.

The action's pinned install_elan.sh fetches elan's master installer; it is not
fully hermetic despite the action pin. Runtime Lean/leanchecker executable
paths, byte hashes, versions, platform, actual package HEADs, tracked cleanliness
and effective search paths must be captured before formal source execution.
At the pre/post formal boundaries, the collector fully byte-inventories selected
dependency .lean/.olean/.private/.server/.ir/.so/.a files and bundled Lean library
artifacts, with equal pathsets and hashes required. The two complete inventories
consume the same65-minute driver budget; I/O cost is unmeasured and can cause HOLD.
This is boundary custody, not a fresh dependency rebuild or provenance proof.
Missing caches/imports or mismatch stops; no broad build repairs are authorized.
Bootstrap cancellation and child cleanup are GitHub platform behavior here,
not a locally proved process-group guarantee.

## Exact finite hosted sequence and budgets

One Ubuntu24.04 job,90-minute platform cap: up to5minutes source/inert checks,
15minutes bootstrap,65minutes collector,5minutes upload. This is a conservative
hard upper bound, not an observed duration or a promise it fits the current
cooperative lease. Parent must select a valid admission/lease window before
push and must stop or make an actual material-evidence renewal before expiry.
Nothing here renews a claim.

Source preflight:
python3 -B -S <prefix>/quo_hosted_verify.py source --manifest-sha256 <literal>.
Then inert controls in normal and optimized Python modes, before any Lean:
python3 -B -S -m unittest discover -s <prefix> -p test_quo_hosted_verify.py -v
and the same command with -O. These are nine newly authored inert methods,
unexecuted here; the original C29913-control result does not transfer.

After bootstrap, the single collector command is:
cd formal
lake env python3 -B -S ../<prefix>/quo_hosted_verify.py execute --manifest-sha256 <literal>
where <prefix> is the exact package path above (the "../" is relative to formal).

The collector resolves actual runtime binaries through measured lean --print-prefix,
then invokes measured absolute binaries. Runtime probes30seconds each. It makes
eight fresh local builds in exactly this order:
Lifetime, TorusTopology, SuperlevelBar, ClosedSuperlevel, MorseFiniteCritical,
CriticalLevelAttainment, QuoClosedSuperlevelAdapter, QuoClosedSuperlevelAudit.
Sources are project/<module>.lean; outputs are fresh isolated
.lake/quo-closed-superlevel-hosted-evidence/objects/<module>.olean.
All six input sources are exact PR487 head7af365e8c8db1ae0275d4efe08a70a678f153ca2
copies, not assumed cached .oleans.

Build commands are:
<measured lean> -j2 -M14000 [-DwarningAsError=true] -o <fresh objects>/<module>.olean <project>/<module>.lean
The warning flag is used for CriticalLevelAttainment, QuoClosedSuperlevelAdapter
and QuoClosedSuperlevelAudit; the six source inputs retain their prior options.
Each formal phase cap360seconds; collector's shared3900-second deadline and the
65-minute platform step cap also apply. Only one formal process runs at a time
after bootstrap, with two Lean threads. There is no Lake build fan-out for local
proof modules and no automatic resumption.

The internal Lean -M14000 is NOT an RSS or kernel memory-limit guarantee.
The collector records /proc/meminfo, samples direct-child VmRSS every250ms,
records cumulative completed-child ru_maxrss, and discloses sampling limitations.
No RLIMIT_RSS enforcement is claimed. Actual feasibility, host-memory headroom
and missing binary/cache failures remain runtime observations; this design has
not qualified them.

After positive output emission and all builds, one declared standard named-module
replay runs: <measured leanchecker> -v QuoClosedSuperlevelAdapter, at360seconds.
The binary must actually exist and be executable and is byte-hashed before use.
No --fresh/all-Mathlib replay, external checker, or full-import rebuild is claimed.

The audit build executes exactly four #print axioms commands. Every fully
qualified target in TARGET_INVENTORY.json must appear exactly once; the standard
axiom allowlist is the nonempty fixed set propext/Classical.choice/Quot.sound.
Missing, extra, duplicated or forbidden reports fail. This is not a complete
module-origin declaration census.

Exactly one negative runs after the positive .olean exists and its hash is
linked by the positive receipt:
<measured lean> -j2 -M14000 <negative-project>/OmittedEuclideanLPC.lean.
It must return1, not time out, and issue precisely one source-bound line25
Type mismatch showing the unapplied actual adapter expression, actual type
EXPLICIT Euclidean closed-superlevel LPC -> the exact quotient LPC proof, and
that expected quotient LPC proof. A typeclass search, missing import, syntax
failure, changed level/height, wrong declaration, signal, extra error or resource
failure is not a successful negative. Source/object hashes must remain unchanged.

The diagnostic parser is newly authored and deliberately remains draft.
require_final_predicates ALWAYS returns PENDING/HOLD after the development
collection. Synthetic inert fixtures cannot qualify the actual new Lean spelling.
A later distinct source-bound review must assess the actual full diagnostic and
unchanged source/object evidence; original HOLD receipts must not be rewritten.

## Custody and stop behavior

Every actual formal child gets its exact command, cwd, selected effective
PATH/LEAN_PATH/LEAN_NUM_THREADS, environment-policy digest, selected observed
/proc child environment where observable, selected binary identity, source
snapshot and before/after local object identities. The allowlisted child
environment excludes credential/token variables; only selected nonsecret
environment values are retained publicly. Package HEADs and search paths are
actual evidence, not just intended inputs.

The collector captures complete raw stdout and stderr separately, their hashes,
exit/timeout, sampled memory, process reaping and receipts before raising.
Timeout sends TERM to the child's process group, waits5seconds, then KILL and
waits5seconds if needed; KILL also addresses the original group after a parent
exits on TERM. This does not assert cleanup of descendants that detach sessions.
No unresolved failure is converted to success.
The first unexpected build/audit/kernel failure stops subsequent formal phases.
The single negative failure is retained as HOLD; no second negative or retry.
Existing evidence directories/stream files refuse overwrite.

Always-upload uses a pinned artifact action with90-day retention, including
sources, objects, raw streams and receipts. Missing/cancelled upload is HOLD.
Parent must read back exact run/attempt/commit/tree/artifact bytes separately.
No full cached-library provenance authentication or scientific acceptance follows.

Old root403STOP, Graph localSTOP, missed14:20 and14:35 clocks and the immutable
partial-recovery record remain historical and operationally preserved. This
separate source continuation does not authorize an unchanged local/native retry.
