# Frozen precode contract: SourceFinitePinKernel

26 October 2026. Draft prepared by OpenAI/Codex `/root/conditional_remote_jet_preflight` for `/root`. Root froze this bounded contract before implementation. The original drafting worker wrote scratch only; root now owns its publication, pickup and all final cache/registration/commit actions.

## Purpose and boundary

Add one isolated module, proposed repository path
`frontiers/source_derivative_gaussian_20261025/SourceFinitePinKernel.lean`, namespace `I4SourceFinitePinKernel`.

It supplies two concrete joins:

1. Explicit finite pin-kernel right-inverse witnesses force positive definiteness of a residual coefficient Gram matrix.
2. A finite original coefficient shift with zero raw pin pairings commutes exactly with the existing every-target `rawPosteriorSample`.

The generic theorem has explicit algebraic witness hypotheses; it does not claim to construct actual remote jet witnesses. The source theorem is a deterministic equality on the existing carrier. Neither declaration is a conditional-Morse, actual remote-rank, density, Sard, endpoint determinant-nullity or elder theorem. There is no new Gaussian law, conditional kernel or choice of null-fiber version.

## Reused authority and verification

Read and carry `/workspace/AGENTS.md`: completed applicable verification is reusable on unchanged material under the same assumptions/dependencies. A new agent, session or handoff does not justify replay. Any additional check must name the changed scope, defect or uncovered obligation. Mathematical evidence and pending different-family/provider-distinct process obligations remain separate.

Root supplies completed qualification of **45 modules / 1083 targets / 32 inputs**, published at `8d86a06e8b78d3dc183bd705caad548778fe8511`. Reuse that evidence; no checks were rerun for this draft. Scientific effect **NONE**; same-family/provider-distinct credit **0**. Canonical standing links:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Providing these links is not evidence that a successor has read them.

## Source dependencies and representation choices

Use `import SourceRawPinConditioning` and an explicit `import ContactJetCovariance` for the two source interfaces. A direct standard Finsupp import may be added only if the pinned import graph does not already expose its definitions. Do not import `SourceMorseIncidence`: its finite replacement/Sard infrastructure is unnecessary for these statements. Reuse the pinned Lean `v4.34.1` and Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`; do not change dependencies.

Use finitely supported functions `ι →₀ ℝ` for deterministic finite coefficient directions. They express finite support without assuming a countable coefficient index or putting random infinite samples in ℓ². Generic Gram statements need neither `[Countable ι]` nor `[Fintype ι]`. Matrix row indices remain `Fin p` and `Fin q` to match existing `I4ContactGram.coefficientGram`. Permit `p=0` and `q=0` without special restrictions.

The signatures below are precise proposed interfaces, **not elaboration-checked code**. Standard namespace qualification may be explicit in the implementation. Use `noncomputable section` and the packet's `set_option autoImplicit false` convention.

## A. Generic finite witness and residual Gram

Proposed public definitions:

```lean
finitePairing {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) : ℝ
  := v.sum (fun m z => a m * z)

residualCoefficient {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ) (j : Fin q) (m : ι) : ℝ
  := b j m - ∑ i, R j i * a i m
```

The multiplication order in `finitePairing` is fixed as **observation coefficient times direction coefficient**. This agrees with `scalarSeries` and avoids incompatible pairing conventions in future witness modules. `R` is arbitrary: no covariance interpretation, normal equations or invertibility is required here.

Proposed directly useful public lemmas:

```lean
finitePairing_residualCoefficient {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ) (j : Fin q) (v : ι →₀ ℝ) :
    finitePairing (residualCoefficient a b R j) v =
      finitePairing (b j) v - ∑ i, R j i * finitePairing (a i) v

residualCoefficient_summable {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ)
    (ha : ∀ i, Summable (a i)) (hb : ∀ j, Summable (b j))
    (j : Fin q) :
    Summable (residualCoefficient a b R j)

coefficientGram_posDef_of_finite_kernel_rightInverse
    {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ)
    (ha : ∀ i, Summable (a i)) (hb : ∀ j, Summable (b j))
    (v : Fin q → ι →₀ ℝ)
    (hker : ∀ i s, finitePairing (a i) (v s) = 0)
    (hright : ∀ j s,
      finitePairing (b j) (v s) = if j = s then 1 else 0) :
    (I4ContactGram.coefficientGram (residualCoefficient a b R)).PosDef
```

The Gram theorem must derive row separation from the finite identities. For every nonzero `z : Fin q → ℝ`, pairing `fun m => ∑ j, z j * residualCoefficient a b R j m` with `v s` equals `z s`. Thus some original coefficient of that row combination is nonzero. Apply existing `I4ContactGram.coefficientGram_posDef_of_separating` with `residualCoefficient_summable`.

Do not assume Gram positivity, a separating predicate, a rank predicate, a right inverse for the residual matrix, or an already established conditional covariance. The *pin-kernel and original-observation pairings* are the substantive finite witness input. Do not prove a second infinite Gram sum-of-squares theorem: reuse the existing one.

Keep elementary finite-pairing linearity/row-combination helpers private unless a later proof in this module actually uses their public form. No generic Finsupp linear-map library or Schur-complement API is part of this checkpoint.

## B. Same-carrier finite shift and raw posterior equality

Proposed public carrier map, restricted to the currently needed planar source:

```lean
finiteShiftSample {L : ℝ}
    (v : I4Source.SourceMode 2 →₀ ℝ)
    (ω : I4SmoothCarrier.SmoothSample 2 L) :
    I4SmoothCarrier.SmoothSample 2 L
```

Its coefficient value is exactly `fun m => ω.val m + v m`. Establish carrier membership with existing `I4Smooth.goodSample_finite_change_iff 2 L`, finite set `v.support`, and equality of the original and shifted functions outside this set. This construction holds for **every real L**; it needs neither `L≠0` nor an amplitude/summability estimate.

Proposed evaluation and pin adapters:

```lean
@[simp] finiteShiftSample_val {L : ℝ}
    (v : I4Source.SourceMode 2 →₀ ℝ)
    (ω : I4SmoothCarrier.SmoothSample 2 L)
    (m : I4Source.SourceMode 2) :
    (finiteShiftSample v ω).val m = ω.val m + v m

rawPins_finiteShiftSample {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (v : I4Source.SourceMode 2 →₀ ℝ)
    (ω : I4SmoothCarrier.SmoothSample 2 L) :
    I4SourceConfluentPins.rawPins L r (finiteShiftSample v ω) =
      I4SourceConfluentPins.rawPins L r ω +
        fun i => finitePairing
          (I4SourceRawPinConditioning.rawPinCoefficient L r i) v

rawPosteriorSample_finiteShiftSample {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (t : Fin 6 → ℝ)
    (v : I4Source.SourceMode 2 →₀ ℝ)
    (hker : ∀ i, finitePairing
      (I4SourceRawPinConditioning.rawPinCoefficient L r i) v = 0)
    (ω : I4SmoothCarrier.SmoothSample 2 L) :
    I4SourceRawPinConditioning.rawPosteriorSample hL r t
      (finiteShiftSample v ω) =
    finiteShiftSample v
      (I4SourceRawPinConditioning.rawPosteriorSample hL r t ω)
```

`rawPins_finiteShiftSample` follows from the existing literal `rawPins_series` and finite-support series addition. For the sample-weighted raw row summability, unfold only `rawPinCoefficient` and reuse `I4SourceSmoothConditional.derivativeCoefficient_weighted_summable` at the corresponding existing `rawDerivativeOrder/Point/Directions (Fin.castAdd 6 i)`. A private one-line adapter for that summability is permitted; it need not become a new public theorem.

For finite-support series addition, either specialize existing `scalarSeries_add_finiteShift` to one direction or use `Summable.tsum_add` plus a sum over `v.support`; both are the same accepted series algebra. Keep any Finsupp/finite-sum conversion lemma private. Do not refactor the accepted general series helper to accommodate this module.

The posterior equality is proved by `Subtype.ext`, `rawPosteriorSample_val`, `rawPins_finiteShiftSample` and `hker`, followed by addition commutativity/associativity. It holds at **every literal target and every source sample**, even at `r=0` or when the raw covariance is singular under the existing total inverse convention. Its only source analytic premise is `hL : L≠0`, used for the actual raw series identity. It asserts commutation, not existence of an arbitrary raw fiber in those degenerate cases.

Do not add `r≠0`, a small-radius bound, covariance invertibility, a Gaussian hypothesis, a global Morse hypothesis or positive gap to this equality. Such assumptions are unnecessary here and belong only to later applications that use actual conditioning or global genericity.

## Public inventory and explicit exclusions

The intended public inventory is **nine declarations**: two generic definitions; three generic lemmas; one sample map; its coefficient evaluation; the raw pin response; and posterior commutation. Small private finite-sum/summability adapters may be added when concretely necessary. A public finite-family/scalar-shift wrapper is unnecessary: a finite sum or scalar multiple of witness directions is itself a Finsupp and can be passed to the one-shift theorem.

No measurability theorem for a varying Finsupp parameter space is requested. No probability/independence decomposition is requested. No actual trigonometric witness, positive conditional covariance for a remote source jet, endpoint Hessian density, critical-value-tie result, `IsMorseDistinct` inhabitant or Lifetime/H0 semantics is requested. Do not advertise the generic Gram theorem as any of those conclusions.

Future implementation verification applies only to this new module and any newly declared small adapters. Preserve and reuse all applicable source/dependency evidence. Root chooses and runs the required exact-source qualification and process steps after freeze; this draft starts none of them.

## Root-frozen qualification and control contract

The new uncovered obligations are only these new finite algebra, carrier and posterior statements. Reuse qualified45/1083/32 and unchanged imports. Producer owns ONLY SourceFinitePinKernel.lean and /workspace/scratch/finite-pin-kernel-construct. Root owns every configuration, production cache, registry, commit and external action. No worker subagents, old source edits or old verification replays.

Before source code, freeze concrete controls for: observation-times-direction finite pairing on nontrivial support; arbitrary correction R; nontrivial cancellation with a=(1,1), b=(0,1), v=(-1,1); residual summability and genuine Gram PosDef; p=0 and q=0 edge cases where useful; finite shift coefficient evaluation and preservation of the literal original carrier; exact raw pin response; posterior commutation at arbitrary six-target vector, with r=0 and arbitrary r instances and no extra invertibility premise. Controls should instantiate the changed mathematical content, not just #check names.

A counterexample-backed negative control drops ONLY the pin-kernel witness hypothesis in the generic Gram claim: one coefficient, a=b=1, R=1 and v=1 satisfy the original-observation right inverse but yield zero residual Gram, which is not positive definite. Record this as a finite algebra counterexample, never an actual source-jet sample. Require intended rejection at exactly one False with no unrelated elaboration error. Do not weaken assumptions or invent desired source rank.

Freeze final source before strict Werror compile, exhaustive actual-module-index axiom classification and exactly ONE own-module kernel. Inventory includes private and generated constants and any generated declarations in imported namespaces; only the six intended written public propositions enter the target registry. Three public definitions and generated constants stay inventory-only. No Prop-valued bundles, sorry/admit/custom axioms/native_decide/implemented_by or umbrella import Mathlib. Standard axioms only propext, Classical.choice, Quot.sound.

Retain every development/control invocation, command, actual exit, wall time, full streams, source/object identity and failed attempt. One isolated new-module qualification only; no helper/control objects enter production cache. A read-only source/spec technical review may inspect existing evidence without replay. Do not compile merely to create an ilean. Scope amendments require root acknowledgement before new public targets.

Root's complete current by-path check is SOURCE_FINITE_PIN_KERNEL_CONTENDERS.json. It records no overlapping foreign packet paths; current default main180d6406 lacks these new outputs. Native pickup and post-claim contention read precede substantive code. Scientific effect NONE; different-family alignment remains separate from mathematics.
