# Implementation plan: finite pin-kernel checkpoint

26 October 2026. OpenAI/Codex draft for `/root`; root-frozen precode plan; native implementation pickup follows. Controlling frozen interface: `SOURCE_FINITE_PIN_KERNEL.md` in this directory. Only scratch documents were written. No code, build, kernel, audit, controls, hashes, git operations, repository/cache mutations, external posts or subagents were run.

## Evidence and ownership

Reuse root's completed 45-module / 1083-target / 32-input qualification at published `8d86a06e8b78d3dc183bd705caad548778fe8511`. The owner rule in `/workspace/AGENTS.md` forbids replay merely for a new session/handoff; additional checking must identify a changed or uncovered obligation and stay within it. Pending different-family process requirements do not invalidate completed mathematical evidence. Scientific effect NONE; same-family/provider-distinct review credit 0.

Root retains contract freeze, implementation pickup authorization, final cache/inventory/registration, commits and publication. This plan does not authorize changes to `lakefile.toml` or other shared files. The active actual-candidate producer/frozen helpers remain outside scope.

Canonical mandate/delegation links to carry in later pickup/handoff:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

## 1. Freeze the finite target before implementation

Root freezes the nine public declarations in the companion contract and confirms isolated ownership of proposed `SourceFinitePinKernel.lean`. Namespace: `I4SourceFinitePinKernel`. Direct packet imports: `SourceRawPinConditioning` and `ContactJetCovariance`. No import of the Sard-heavy `SourceMorseIncidence`; no dependency change.

No fresh source inventory or old mathematical check is needed solely to adopt this draft. If root identifies a new dependency change after the supplied published identity, name it and inspect only its effect on these APIs.

## 2. Implement the finite pairing and generic residual result

Define `finitePairing` using `Finsupp.sum` and `residualCoefficient` as the original observation rows minus an arbitrary finite linear combination of pin rows. Prove `finitePairing_residualCoefficient` by expanding finite support and commuting finite sums. Prove `residualCoefficient_summable` by finite sums of scalar multiples and subtraction.

Prove the Gram theorem through existing `coefficientGram_posDef_of_separating`. For a nonzero row combination, suppose every coefficient were zero, pair with each finite witness, use `hker` and `hright`, and conclude every coordinate of that combination is zero. This proof uses no matrix inverse, spectral theorem, covariance fact or Gaussian law. Keep auxiliary pairing linearity local/private; do not grow a general API without a direct use.

Concrete proof input reused: `ContactJetCovariance.lean:77–120`, namespace `I4ContactGram`. The row-summability obligations are new only for `residualCoefficient`; the old Gram identity/positivity proof is reused unchanged.

## 3. Implement the finite same-carrier shift

Define `finiteShiftSample v ω` to have coefficients `ω.val+v`. Use existing `I4Smooth.goodSample_finite_change_iff` (`inputs/SourceSmooth.lean:243`) with `v.support` to preserve every derivative-order summability class. This avoids another envelope/moment proof and works for every L. Add the coefficient evaluation theorem.

Do not identify random coefficient samples with ℓ² vectors. Here only deterministic finite directions are Finsupps, while samples remain in `SmoothSample 2 L`.

## 4. Prove raw pin response, then every-target posterior commutation

First prove the literal raw pin response using `SourceRawPinConditioning.rawPins_series` (`:39`) and finite-support series addition. Reuse sample-weighted derivative summability from `SourceSmoothConditionalKernel.lean:60`; `rawPinCoefficient` is exactly the corresponding `rawDerivativeCoefficient` row. If a private support/series conversion helper is needed, keep its statement finite and its scope local.

Then prove the sample equality by subtype extensionality and `rawPosteriorSample_val` (`SourceRawPinConditioning.lean:207`). The raw pin input to the correction is unchanged under `hker`, so the correction is unchanged coefficient by coefficient. The shifted original sample remains on both sides. No use of raw/confluent RCD uniqueness, no target restriction and no covariance-invertibility proof is needed.

Keep the stronger correct hypotheses: `hL : L≠0`, arbitrary `r`, arbitrary `t`, arbitrary `ω`, and explicit finite pin-kernel identities. The `r=0`/singular case is a deterministic commutation equality under existing definitions, not an assertion of fiber support or conditional-distribution validity there.

## 5. Root's finite completion checkpoint

Implementation stops after the nine public declarations and necessary private proof helpers. The new uncovered obligations are exact elaboration of these declarations, their finite-sum identities, carrier construction and same-sample equality. Root should qualify only that new scope with the established exact-source procedure; applicable old dependency checks remain reusable. This draft performs no qualification or controls and creates no registration/cache evidence.

Report the final assumptions, public declaration inventory and any deviation from the frozen contract. Distinguish formal mathematical verification from outstanding provider-distinct/process review. Root alone handles registration/cache composition and publication.

Do not continue into actual trigonometric interpolation, actual remote 2-jet full rank, Gaussian free-coordinate independence from the entire conditioned residual, endpoint Hessian determinant nullity, equal-value incidence, global conditional Morse/distinct, or canonical elder/H0 semantics. Those are separate later checkpoints with their own substantive obligations.
