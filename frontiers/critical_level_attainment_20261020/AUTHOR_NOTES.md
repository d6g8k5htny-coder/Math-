# C294 author notes — conditional attainment at literal death

Author: OpenAI/Codex agent `/root/adapter_feasibility_c292`, delegated by the
parent for Dylan Roy. Same-provider and source/design exposure are explicit.
No organizational independence or human review is claimed. This is a new
formal implementation unit of the already delivered conventional C292 argument,
not a claim of a new conventional theorem or of full C292 formalization.

Claim supplied and verified by parent: R17 Work Events 2392,
`2afaffe8-cf58-4bc7-9824-7585f9feb788`, 2026-10-20 08:18:25.505179 UTC through
10:18:25.505179 UTC. Canonical pickup:
[Math #419 / 6286648588](https://github.com/d6g8k5htny-coder/Math-/pull/419#issuecomment-6286648588);
mirror:
[Main #419 / 6286653565](https://github.com/d6g8k5htny-coder/main/pull/419#issuecomment-6286653565).
Parent handles continuing ownership, review, final isolated verification,
publication and custody. Shared libraries and all previous deliveries are
unchanged.

## Exact acceptance boundary

The public declarations are
`TorusCriticalAttainment.quotient_death_attainment` and
`TorusCriticalAttainment.euclidean_death_attainment`.
Their inputs are literal Lifetime smoothness, period-L periodicity, and Morse
distinctness, a positive real period, a starting point, and C263 nonessentiality.
The one additional geometric premise is

```lean
LocallyPathConnectedSpace
  {q : torus_quotient d L hL //
    superlevelBar_deathHeight g M ≤ descendedHeight d L hL g hperiodic q}
```

Here `descendedHeight` is exactly C263 `torus_descend`, using the identical
Lifetime/C263 lattice-vector formula. There is no product-torus replacement
or half-open representative-domain compactness assumption.

The quotient theorem derives one strictly older literal quotient critical point,
an actual path to it in the closed death superlevel, and equality with death at
some path parameter. The Euclidean theorem lifts this one path from the
prescribed representative M, derives literal criticality of the resulting
endpoint, and preserves every path height. It does not select one Euclidean
representative consistently across separate strict-level lifts.

No fixed endpoint, finite event list, supplied path, trap, or desired death
identity is an input. Neither theorem claims strict death drop. The hypotheses
in fact permit every natural dimension; C292's positive-dimensional
nondegenerate-maximum locus specializes them without changing its d or L.
Only the nondegeneracy conjunct of Morse distinctness is used, through C293.
The distinct-critical-values conjunct is retained in the public source-facing
signature.

## Proof and reuse

For each a below the literal death delta, form the connected component K_a of
the starting quotient point in the closed superlevel {F >= a}. C263's strict
cut supplies a path to a strictly higher point and hence a higher point in K_a.
C263 already proves delta <= g(M), so no strict-death-drop or Taylor argument
is needed here.

K_a is compact and connected. A maximizer of F on K_a lies strictly above g(M)
and therefore in the interior of {F >= a}. Ambient local connectedness implies
that K_a is a neighborhood of that maximizer. It is consequently a local
maximum on the quotient. Pulling back through the continuous projection and
using Fermat's theorem proves literal Euclidean criticality, hence membership
in C293's quotient critical set.

Intersect that finite critical set with {F > g(M)}. This compact older set
meets every K_a. Since the K_a form a downward-directed family of closed sets,
compactness supplies one older critical Q in all of them. This is an actual
fixed-endpoint argument, without assuming a candidate/event list.

The directed intersection of the K_a is preconnected. The new elementary
helper proves this by normal separation and the existing compact
directed-closed-family lemma: a separation of the intersection would give a
separation of one K_a. This argument concerns compact sets, not path space.
Every point of the intersection lies in {F >= delta}, so M and Q belong to
the same connected component of that actual closed level.

The explicit closed-level local-path-connectivity premise is used at this last
step to turn connected-component membership into a path. If the path never
equalled delta, its heights would all be strictly above delta, contradicting
C263's `superlevelBar_death_not_mem_clearance`. Finally, specified-start
covering-map lifting preserves the whole path and C293's quotient derivative
identifies the lifted endpoint as a literal critical point.

Before adding this helper, inspected C258 `DEATH_PAIR_PROOF.md` and
`NEXT_TASK.md`: these are a conventional proof and a formal dependency list,
not a Lean intersection implementation. C258 expressly leaves formal
realization open. Also inspected the actual frozen `ClosedSuperlevel`,
`OrdinaryH0`, `ElderClearance`, `ElderInterval`, and `ElderBridge`
declarations. The existing trap has a `closed_path` input; its attainment
theorem assumes the displayed path and its closed-height bound.
`OrdinaryH0` explicitly supplies no critical-level attainment theorem.
`ClosedSuperlevel` is reused unchanged, including its closed-level definition
and `superlevel_neg_height`/`superlevel_isClosed` facts. No generic
compact-directed-connected-intersection theorem was located in these modules
or in the pinned Mathlib search.

The immutable module DAG is:

```text
Lifetime ───────┐
               ├── MorseFiniteCritical ──┐
TorusTopology ─┘                         │
SuperlevelBar ───────────────────────────┼── CriticalLevelAttainment
ClosedSuperlevel ────────────────────────┘
```

Exact source bytes, SHA-256 and Git blobs are in `SOURCE_INPUTS.json`.
Mathlib is pinned at `d13f23b723b8a846827a245b89c10fc7d3f11612`.
The runtime is the existing Lean 4.34.1 binary, SHA-256
`1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`.

## Remaining mathematical boundary

The implication from literal Morse data to local path connectivity of the
actual closed death superlevel remains open in this formal development.
No smooth Morse normal-form theorem was found at the pin.
The submersion file defines its property through local normal forms and lists
the implication from a derivative right inverse/surjectivity as future work.
C293's inverse-function argument for the derivative map proves critical-point
isolation, not a quadratic normal form for g.

This unit does not prove the full C292 trap/frontier package, strict death
drop, a saddle index, actual elder pairing, exhaustive once-counted bars,
all-small-bars converses, regional shrinking-collision statements, or any
probabilistic/asymptotic conclusion. There is no coefficient-field input or
limit-order change: this is deterministic geometry of one literal sample
function at fixed d and positive L.

## Development evidence

Development writes are confined to C294. The runner serializes Lean,
uses two threads and a 4096 MB limit, retains stdout/stderr and receipts,
and stores each compiled source snapshot by SHA-256. Shared dependencies
are read only.

The first fresh Lifetime dependency build timed out at 240.03 seconds with
empty diagnostics and unchanged exact source. This failure is retained.
The three C293 dependency objects were then copied only after live source
and object hashes matched C293's terminal receipt. That explicit development
reuse is recorded in `evidence/DEVELOPMENT_OBJECT_REUSE.json`; it is not
fresh C294 source-build evidence.

The independent fresh ClosedSuperlevel build also timed out at 240.06 seconds
with empty diagnostics and unchanged source. Its old object was copied only
after its live hash and source hash matched the existing successful build
record and reviewed compiled-artifact manifest. This separate development
reuse is in `evidence/CLOSED_SUPERLEVEL_OBJECT_REUSE.json`.
The original 240-second runner is retained in evidence. Later development
invocations have a bounded 600-second limit. A one-second sample of the
running SuperlevelBar process located the active worker in Lean import
finalization (`lean_mark_persistent`), not theorem elaboration.
SuperlevelBar then passed a fresh build in 204.61 seconds with clean output.

The main module's first three attempts failed elaboration in 92.74, 75.04,
and 67.34 seconds. Their exact source snapshots and diagnostics are retained.
Corrections made actual set-membership inequalities explicit, installed the
actual quotient's derived ambient local-path-connectivity instance explicitly,
used the existing JoinedIn subtype/component API, and replaced obsolete
proof-local `letI` style with `let`. The public endpoint signatures and
mathematical hypotheses did not change.

The fourth main-module attempt passed in 73.72253683299999 seconds, return code
zero, with empty stdout and stderr and unchanged source. Receipt:
`runs/20261020T084025Z-CriticalLevelAttainment-deeba258/RECEIPT.json`,
SHA-256 `e64482068df7b48ac984c156054188b09b4ef865b504e6d1faa39334875aab1c`.

Stable main source: 14,338 bytes,
SHA-256 `ec4b6ceb9475143434c25269bccc45cdd627d83af359609007001c9284bb9a12`,
Git blob `1579751ec03c14f3dfd90df98db7a37d8ca74e09`.
Development object SHA-256:
`ea5f6a80ee778ec7708ddc1775cfbf829372127958a0db23efc7a7e1c7d5e235`.
`AUTHOR_MODULE_INVENTORY.json` binds these records and lists the thirteen
explicit declarations; this count is not a generated/transitive axiom census.
Proof edits stopped at this clean source.

Status: **clean author development compilation passed**. This does not claim
fresh C294 compilation of all reused dependencies. Parent's isolated final
source builds, standard named-module kernel replays, complete axiom census,
omitted-LPC negative invocation, exact-artifact nonauthor review, publication
and custody remain separate work. No final acceptance or scientific promotion
is claimed.
