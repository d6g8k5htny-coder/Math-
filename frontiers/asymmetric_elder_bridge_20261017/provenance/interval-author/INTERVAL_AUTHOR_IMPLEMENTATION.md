# Actual singular-H0 interval summand: author implementation

Author: OpenAI/Codex `/root/elder_interval_lean_20261017`, assigned by Root under Main419 pickup 6240826507. This is author implementation, not nonauthor review or scientific acceptance. The final source is frozen at 16006 bytes / SHA-256 `3dab19342c307f6b70f4fa05ac913b4ead083742a56408db71b45276c0acb9ab`.

**Current evidence boundary:** actual source elaboration and the combined positive-control/35-target axiom audit passed with warnings treated as errors. Root owns the later joined bridge and kernel verification; no kernel PASS is claimed in this report yet. Two prepared semantic mutants have not been executed. This author has paused all Lean launches after handing the serial runtime slot to Root.

## What the implementation constructs

`interval-project/ElderInterval.lean` imports the exact existing `OrdinaryH0.lean`, which imports the exact existing `ClosedSuperlevel.lean`. Its homology objects and maps are the existing Mathlib singular-H0 filtration; no replacement homology functor or compatibility hypothesis is introduced.

The coefficient is an arbitrary field k, including positive characteristic. `elderActive m d t` means `-m ≤ t ∧ t < -d`. `elderFiber` is the submodule of k consisting of all coefficients on active levels and only zero elsewhere. `elderFiberMap` preserves the coefficient before death and annihilates it at and after death. The interval functor's identity and composition laws are proved, including inactive zero fibers. Thus the object is the actual interval `[-m,-d)` in the source's increasing parameter t=-height.

The explicit `ElderTrap` premises are:

- `d<m`, `g M=m`, and `m<g P`;
- M belongs to the fixed D and P is outside D;
- every point of D has height at most m;
- at each active closed superlevel, D cuts out a clopen subset;
- M and P are joined by an actual path in the closed superlevel at height d.

The record contains no H0 equality, elder relation, natural transformation, interval certificate, split, or barcode conclusion. The geometric analytic ridge construction and the derivation of these topological consequences remain separate inputs. Root's subsequent `ElderBridge.lean` is intended to derive the clopen cut and this record from the closed-domain/boundary premises; that file is not authored here.

Clopenness is proved to make membership in D constant on actual paths, using path components inside connected components. `ElderTrap.componentInside` then descends this predicate through the actual `ZerothHomotopy` quotient. No local path connectivity or finiteness of the outside components is assumed.

`elderProjection` uses the actual proved C264 `ordinaryH0_filtrationIso`, followed by the coproduct universal map assigning 1 to components inside D and 0 to all others. Its value on every actual ordinary-H0 point class is proved. `elderDifference` is the actual morphism `[M]-[P]`; its inclusion transport is proved using actual singular-H0 point-class naturality. The closed path makes this difference zero at and after death.

The section is the coefficient inclusion from the interval fiber followed by that actual point-class difference. The retraction is the actual component-indicator projection followed by the active-fiber coefficient lift, and zero on inactive levels. Their naturality proofs cover:

- active-to-active maps;
- prebirth-to-active retraction maps, where the height ceiling excludes every source point from D;
- active-to-death section maps, where the actual closed path kills the difference;
- the remaining inactive zero-fiber maps.

`elderSection_retraction` proves the constructed section followed by the constructed retraction is the interval identity. `elderKernelProjection` and `elderDirectSummand` then construct the natural isomorphism

`H0 filtration ≅ elderInterval ⊞ kernel(elderRetraction)`.

The explicit formulas are v ↦ (qv,v-jqv) and (c,w) ↦ jc+w. Both inverse identities are proved in the functor category. This is one actual natural direct summand. It does not prove a simultaneous choice of splits for all local traps or an exhaustive barcode decomposition.

## Actual source and runtime evidence

- Exact accepted proposal: 28291 bytes / `6d07631c068019bf9f081ad0b6f50325679e3ab554f221265e002d5c047f17ac`.
- Exact integrated nonauthor mathematical review: 25687 bytes / `16678abc7de50986b0fc6d54303449bf1b4c5ba8b10f6a3ccc7f9d03a97a4e9f`.
- Exact OrdinaryH0: 19803 bytes / `3d6b0d6b53413c484b1d010bccf0d53ae7f75becb2d747868f22dbd673fe0a88`.
- Exact ClosedSuperlevel: 8088 bytes / `90d1481b75d9c6d14e462c3fbf0bf7c7cdd0efb9eaad68d6732400658753b1c2`.
- All nine dependency HEADs match the exact formal manifest and have clean tracked working trees before and after source elaboration. The private project uses APFS clones; prior source checkouts and caches were not edited.
- Runtime reports Lean 4.34.1. No new toolchain was downloaded. The private Mathlib cache command reused 5570 already cached files, with 3338 already decompressed; it downloaded zero files.
- ClosedSuperlevel baseline: actual exit 0, 126.439 seconds, empty stdout/stderr.
- OrdinaryH0 baseline: actual exit 0, 116.520 seconds, empty stdout/stderr.
- ElderInterval final source: `proof-5.json`, actual exit 0, 269.496 seconds, empty stdout/stderr, warnings-as-errors enabled, two Lean threads.
- Frozen compiled artifact: 839672 bytes / `5a93f68a6f4a21d2d3b8ab453e2231dbcf0f9cb6da07ce2e62d5ed1b75508836`.

The full Mathlib imports are memory intensive on the observed 16 GiB machine. Root and this author agreed to serialize subsequent heavy imports. A quiet stdout while the actual process remained live was not treated as a failure or restarted.

The initial ClosedSuperlevel baseline was interrupted before a terminal receipt or output artifact was retained. Its process was later verified absent; its exit is **UNOBSERVED**. The original empty streams and interrupted observation are retained. The bounded resumed baseline above is the actual passing verification, not a reconstructed timestamp or claimed success for the old process.

Source attempts 1–4 and their exact source preimages/compiler outputs are retained. Attempts 1–3 exposed local proof-engineering issues (subtype extensionality, categorical rewrite transparency, naturality binders, coproduct evaluation and the linear-map boundary). Attempt 4 had no remaining proof goal, but two deprecated theorem-name warnings failed warnings-as-errors. The final source uses the current theorem names and passed. No `sorry`, new axiom, or premise weakening was used to obtain that result.

## Controls and audit scope

The positive controls pin closed birth, open death, zero prebirth fibers, active coefficient transport, zero death maps, the actual singular-H0 split in characteristic two, and the natural kernel-complement isomorphism over the rationals. The ordinary individual point class is proved nonzero using the actual C264 augmentation theorem; the dying class is its difference with the older point class.

The axiom census covers all 34 explicitly named definitions, theorems and structure plus the generated reassociation theorem: 35 printed targets. An earlier generator missed three same-line `@[simp]` helpers; the separate nonauthor reviewer identified this and the census/audit file was corrected before execution. Structure-generated constructors, recursors and field projections are covered transitively by the source/module checks rather than counted as separately printed audit targets.

The first combined control/audit command exited 1 after 313.513 seconds because one control applied the death theorem at d=0 without simplifying `-0` to `0`. It emitted all 35 axiom targets, each with exactly `propext`, `Classical.choice` and `Quot.sound`, and no other proof diagnostic. The harness failure and its exact preimage are preserved. Only that control was corrected by explicit `neg_zero` normalization; the frozen implementation source was not changed.

The corrected combined command actually exited 0 after 52.740 seconds, with 4896 bytes of stdout and empty stderr. Its nine positive examples and eight signature checks elaborated. All 35 printed targets exactly match the census and have only the three standard axioms above; this was checked against the literal output. The corrected control/audit source is 3561 bytes / `b515d40bc0f58a71c3afa80e3ae7fae53725f3d713c2df2df110ba2814a4ece3`. Its receipt is `controls-and-35-target-audit-corrected.json`; the parsed exact result is `AXIOM_AUDIT_AND_POSITIVE_CONTROL_RESULT.json`.

Two source mutants are prepared from the final frozen source: changing open death to closed death, and weakening the D height ceiling from m to m+1. Their exact bytes and changes are bound in `MUTATION_SPEC.json`. An earlier unexecuted preparation based on an earlier draft is preserved under `mutation-v1-prepared-not-executed/` and carries no execution credit. Actual mutant executions remain pending at the time of this report.

## Retained limits

This formalizes the critical topological/categorical interface for one interval summand under explicit trap premises. It does not formalize the analytic ridge, eigenframe and derivative estimates; smooth quotient charts or Hessian inertia; all short global bars; singular-mark escape estimates; canonical Morse elder labels or multiplicity; full interval decomposition; higher homology; the probabilistic process theorem; universality of the exponent; or scientific acceptance.

No native issue comment, branch, PR, workflow, source adoption, scientific status or previous candidate was changed by this author. Root controls integration, the joined bridge, native delivery, and the full active research goal, which remains unmet.
