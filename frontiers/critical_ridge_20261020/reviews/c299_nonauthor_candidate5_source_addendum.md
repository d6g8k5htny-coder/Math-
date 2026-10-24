# C299 candidate5 nonauthor source-repair addendum

Review time: 2026-10-20 15:04:04 UTC. Reviewer: OpenAI Codex `/root/c299_nonauthor_review`, delegated by `/root` for Dylan Roy. Source author: `/root/adapter_feasibility_c292`. Actual nonauthor review, same-provider source exposure, organizational/provider independence credit 0, human review credit 0, scientific effect NONE.

**Disposition: ACCEPT_SCOPED_SOURCE_REPAIR for the exact candidate5 bytes, limited to the next declared hosted development attempt.** I found no concrete source blocker in this finite repair after reconstructing its equality obligations against the actual prior diagnostic and the pinned tactic implementation. Candidate5 remains entirely uncompiled. This review does not certify that the compiler will discharge all generated instance equalities or that the proof has passed any formal gate.

Candidate4 is concretely blocked as written by its actual hosted failure. The earlier candidate4 source review remains historical and is not retrospectively rewritten as compilation success.

## Identities and actual negative evidence

Fresh native reads establish candidate5 `project/CriticalRidge.lean` at **8966 bytes**, SHA-256 `669b94138531a694f134d24ee9d34ecf6cda5ccec125e2bac279f9e49e1a4aae`. Its separate source-attempt snapshot has the same hash. `execution/author/CANDIDATE5.diff` is 2162 bytes, SHA-256 `df231756fa1c33bacf3745127bcbac0b3fd0aa98e64254519a54af6c02664200`; `CANDIDATE5_FREEZE.json` is 1393 bytes, SHA-256 `cc3eedc74710c0c90e5663fec859640c48b3836bfeaa0514a53a0babc9b4c7de`. Direct frozen-snapshot comparison reproduces the declared change from candidate4 `f3a515bd0a984c8a8affbfc79f4768e7a357b7798eee8990a5a34adbdcf6f0f7`.

Actual hosted3 ran candidate4 at PR491 head `5e63005bd6d8288695fbbc974e40336dca87e77f`, tested merge `011a9683382b474cfcf0046ebaec365452277654`, run **39443604910**, attempt 1. Root's retained disposition identifies its original artifact as 479747 bytes, SHA-256 `73c7f4a1c1cc83fc74408bc9f885969e9704a7d6c6af32fa6aed071aaddcff5a`.

I read and hash-checked the complete actual failing phase stdout and receipt: stdout 3405 bytes, SHA-256 `dd5794a1cb3365b1f4a25e170496e0b697b5b45f4f6a8b5cd9350fbde1946351`; receipt SHA-256 `58be4e1e89eb9fce6ac069faade532a6592c9135093a77c463576cbe30f647b1`. The process exited 1 after **17.057773 seconds**, with no outer timeout and empty stderr. It reported the still-invalid direct restriction derivative composition, deterministic typeclass limits at 20000 heartbeats and deterministic `isDefEq`/`whnf` limits at 200000. These compiler-internal failures are not an outer process timeout. Three upstream builds passed; the ridge object is absent and no audit/kernel/negative phases were reached.

I subsequently read `hosted-development3/DISPOSITION.json`, SHA-256 `5628c92d06eba0868e030c389f4ccecce019d93ac682db45818e9c9a846d5236`. That file was absent during my first preparation read and was available for this final addendum. Original artifact/remote custody remains root's verification; I made no new remote fetch.

## Source-level reasoning for the changed tactics

Candidate5 removes both declaration-wide `backward.isDefEq.respectTransparency false` settings and introduces no replacement declaration/global option or increased resource cap. This removes the setting associated with the additional hosted3 typeclass/definitional-equality regression. It does not itself prove that compilation will now stay within limits.

The derivative proof returns to the bilinear `.clm_comp` expression that actually elaborated in candidate3. That earlier run displayed a remaining equality between the intended derivative and

`compL (Df at the base point) ∘ 0 + (compL.flip V.subtypeL) ∘ (D²f p ∘ ridgeAddition V)`.

Candidate5 handles that specific obligation: `ContinuousLinearMap.comp_zero` and `zero_add` remove the first summand; extensionality on the ambient-product direction and `z : V` reduces the second summand to the defining application of `restrictCovector`. I checked the pinned definitions and their reflexive `flip_apply` and `compL_apply` lemmas. Their value-level reduction is the same covector restriction, with no new derivative or Hessian assumption.

The change from `convert` to `convert!` is also material. I read the actual pinned `Mathlib/Tactic/Convert.lean`: the expensive variant uses default transparency in its post-step and allows congruence between different head constants. It still builds an equality proof and casts with equality; all generated side goals must be discharged. It does not admit equality or bypass kernel checking. The proof now applies its `first` branches to **every** generated goal using `<;>`. Reflexive instance-coherence goals are attempted with `rfl`; the derivative equality receives the zero-composition simplification and extensional reduction above. This directly addresses the extra instance-equality branches and leftover derivative equality seen in candidate3, rather than repeating candidate4's failed direct application.

For the final graph chain rule, candidate5 explicitly supplies outer function `G`, derivative `D`, graph function `w ↦ (w, r w)` and graph derivative `(id, Dr 0)` to the pinned `HasFDerivAt.comp`. It then converts each premise into the theorem's expected instance types. The only nonreflexive point equality intended there is `(0, r 0) = (0, 0)`, proved by `Prod.ext rfl hr0`; its orientation matches target-to-source conversion. The graph derivative and final function-composition identifications use reflexivity. This is the same chain-rule argument at the same base point, with the instance reconciliation made explicit at the application.

These source reductions explain why the new terms target the observed failures. Successful elaboration remains an empirical gate: I did not run a goal-state probe, compiler or test, so I cannot certify the precise goals that `convert!` will generate in this concrete environment. Should an unhandled goal or internal limit remain, its actual failure must be retained and this source disposition must not be reported as a repair PASS.

## Unchanged mathematical and execution boundary

The frozen diff changes no declaration binder or result type. There remain four definitions and five theorems. No import, axiom, `sorry`, `admit`, unsafe declaration, assumed ridge/chart/inverse, warning suppression or cap increase is introduced. The same literal hypotheses still derive one ridge with all four original conclusions. The explicit IFT eventual-equation proof from candidate4 remains unchanged.

The prior mathematical review, including the nonorthogonal cross-block, zero-subspace, degenerate restriction and missing-criticality cases, still applies. No broader theorem is asserted. Full module-origin/private/generated census and allowed transitive axioms require actual audit evidence; nine public source declarations do not supply that evidence.

I performed source/diff/hash/receipt reads and pinned API/tactic source inspection only. I wrote this review file; I did not edit author or support sources, execute Lean/tests/mathematical programs, invoke a workflow/master, or mutate public state. Root owns publication identity checks and the next declared hosted attempt. Final compilation, kernel/census/negative diagnostics, actual negative qualification, final support review, evidence acceptance and custody remain pending. Critical basis, quotient/full LPC, C294 hclosedLPC, bars and scientific promotion remain OPEN.
