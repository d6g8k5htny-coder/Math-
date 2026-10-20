# C294: conditional path attainment at the actual death height

For a literal smooth, periodic Morse-distinct field, C294 derives a strictly older critical endpoint and a path whose minimum equals the **actual C263 superlevel-bar death height**, provided the actual closed death superlevel is locally path connected. That local path connectivity is an explicit geometric hypothesis and remains to be derived from the literal Morse data. This is one formal dependency toward the ordinary-persistence bridge, not completion of that bridge.

Let delta be superlevelBar_deathHeight g M on the actual period-lattice quotient. The two public theorems in [CriticalLevelAttainment.lean](final-project/CriticalLevelAttainment.lean) are:

- TorusCriticalAttainment.quotient_death_attainment: a quotient critical point Q with F(Q)>g(M), a path from the actual projection of M to Q, F>=delta along the path, and equality F=delta at some parameter.
- TorusCriticalAttainment.euclidean_death_attainment: a prescribed-start lift from M to an actual literal critical point y, with g(y)>g(M) and the same attained minimum delta.

Neither the endpoint nor a path, finite event list, saddle pairing or attained death is an input. C293's actual finite projected critical set supplies a single older endpoint across all strict subdeath levels. Compact connected intersection plus the explicit closed-level LPC hypothesis supplies the path. C263's strict-clearance exclusion forces equality at death. The Euclidean endpoint is chosen by lifting this one final path, rather than silently fixing representatives across earlier lifts.

## Exact statement and scope

Inputs retain positive L, all natural dimensions d, literal IsSmooth, IsLPeriodic, IsMorseDistinct and nonessential superlevelBar_isEssential. The extra premise is:

```lean
LocallyPathConnectedSpace
  {q : torus_quotient d L hL //
    superlevelBar_deathHeight g M ≤ descendedHeight d L hL g hperiodic q}
```

The full Morse predicate is retained; the finite-critical-set dependency uses its nondegeneracy part. A nondegenerate starting maximum is not assumed or proved by this conditional unit, and strict death drop is not a conclusion. Ambient torus LPC alone does not discharge the closed-subtype premise.

[Scope and unresolved bridge](SCOPE.md), [author argument](AUTHOR_NOTES.md), [root mathematical check](evidence/ROOT_MATHEMATICAL_CHECK.md) and [exact nonauthor review](reviews/NONAUTHOR_REVIEW.md) explain the proof, inference controls and exposure. The actual Morse-to-closed-LPC theorem, strict death drop, full trap/frontier/ceiling adapter, elder pairing, once-counted exhaustive bars, field-first sampling, all-small-bars converse and regional shrinking multiple-witness collision estimate remain open. No stochastic normalizer or limit order is changed.

## Actual local formal evidence

The frozen inventory is SHA256 **a819e8a4cf37b3b3527dd32045fc08c5dd5967022c2d70c1ee009add352a1f2d**. The main proof is14338bytes, SHA256 **ec4b6ceb9475143434c25269bccc45cdd627d83af359609007001c9284bb9a12**, Git blob1579751ec03c14f3dfd90df98db7a37d8ca74e09.

- Seven fresh serial builds into an initially empty isolated output directory passed: Lifetime, TorusTopology, SuperlevelBar, ClosedSuperlevel, MorseFiniteCritical, CriticalLevelAttainment, CriticalLevelAxiomAudit. Both new modules used warnings-as-errors.
- Two standard named-module leanchecker replays passed: CriticalLevelAttainment and CriticalLevelAxiomAudit. These use imported dependencies; they are not --fresh or external independent replays.
- The complete module-origin axiom census contains235 unique declarations, including generated/private declarations:103/38/25/32/20/17 across those six source/proof modules. Every transitive axiom is among propext, Classical.choice, Quot.sound. The13 explicit new declarations are not confused with the17 module-origin declarations.
- The actual omitted-LPC fixture was rejected with a type mismatch showing the missing LocallyPathConnectedSpace input, rc1 without timeout. Sources and imported objects were unchanged. This checks the implemented conditional interface; it is not a counterexample to the open Morse-to-LPC theorem.

Full final commands, streams and receipts are in final-runs/, negative-final/, FINAL_SEQUENCE_RESULT.json and the frozen audit source. [Replay guide](REPLAY.md) describes the pinned Lean4.34.1/Mathlib environment and actual limits. Dependency checks reuse83897 previously hashed artifacts through exact pathset and unchanged metadata; they do not claim a full fresh cache rehash. [Execution history](evidence/EXECUTION_HISTORY.md) retains the distinction between failed development attempts, source-bound object reuse during development and these fresh final builds. The private archive preserves complete native development attempts and original receipts.

## Sources, ownership and delivery

[Public source bindings](PUBLIC_SOURCE_BINDINGS.json) identify all five immutable formal inputs. C293's MorseFiniteCritical source is pinned to unmerged PR482 head0ea97aff489f9420632b4cee81ad82dbec5fe88e. No claim is made that it is on default Main. Existing companion, C258 component-kernel, production registration and C293 hosted-engineering owners retain their scopes. This package only adds frontiers/critical_level_attainment_20261020/.

This source package records local formal execution. **LOCAL_ONLY_NOT_REGISTERED_IN_HOSTED_FORMAL** applies to the new modules. Existing hosted jobs may verify their registered targets; actual exact-head hosted results, raw GitHub-byte readback, one private archive's raw readback, final artifact master and R17 registration are reported in the later terminal delivery record. Publication of this source package alone does not establish those later steps. The immutable private archive is accompanied by external final custody/master records to avoid a circular self-receipt.

Public text records replace local filesystem prefixes with symbolic roots. PUBLIC_PROJECTION.json separately records native and projected hashes; Lean source bytes are unchanged. Embedded native receipt hashes continue to refer to the original native bytes, not to the projected text.

Proof author: OpenAI Codex /root/adapter_feasibility_c292. Separate nonauthor reviewer: OpenAI Codex /root/c292_geometry_review, with prior C292/C293 and design/source exposure disclosed. Root01a0bbb5 coordinated, authored controls and performed execution/custody; /root/current_pr_triage_c292 audited ownership/source routes and adapted packaging. All are AI work delegated for Dylan Roy. Organizational independence0, human review0, scientific effect NONE. No personal human review by Dylan is claimed.

[Owner mandate](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md) · [Standing delegation](https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md).
