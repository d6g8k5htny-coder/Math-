# Cap I4: source-bound companion, not a closure claim

Author-side implementation: OpenAI / GPT-6 Astra Pro, delegated by Dylan Roy on October 5, 2026. Independence credit: 0. Scientific effect: NONE. Alignment review: pending. The existence of proof text is not kernel-check evidence; only an exact-head successful replay supplies that evidence. **The concrete matrix-density transport remains OPEN.**

## Custody and isolation

Base: `c08e83597f94f923b8411dc13cdf28be3f214b37` in `d6g8k5htny-coder/Math-`.
Source: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, Git blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, especially (6.2) and (7.1)–(7.8).
Coordination: main#229, originating comment 6001689465; acknowledgement 6001710889.

This directory is deliberately **outside `formal/`**. It imports the unchanged pinned formal package but does not change its 40-target manifest, acceptance records, proof bodies, source receipts, integration branches, queue, or required-check aggregate. Its workflow is push-only on `chatgpt/cap-i4-source-bridge-20261005`. No PR or merge is requested. The source gate verifies the original source blob, an unchanged `formal/` tree, and additive-only changes in this directory plus the dedicated workflow. Replay reports SHA256 of the actual source and companion bytes.

## Implemented statements

`goodCap`, `depthEvent`, and `fourthEvent` encode exactly

```
G = { (4/(3k)) r M3² < λ AND r M4 ≤ 3k/10 }
Eλ = { λ ≤ (4/(3k)) r M3² }
E4 = { 3k/10 < r M4 }.
```

`cap_failure_eq_union` proves equality of the complement with the union, and `cap_failure_subset` supports a separately supplied deterministic implication from the cap event to a target event. Equality at the depth threshold is bad; equality at the fourth-derivative threshold is good. `cap_union_mass` and `cap_cubic_of_tails` give the finite-measure union and `C3 r³ + C4 r⁴ ≤ (C3+C4)r³` assembly on `0≤r≤1`.

`fourth_moment_tail` reuses the **actual existing** `p02_lm009_markov_event` finite-measure API. `E4_specialization` has exactly epsilon `3k/10` and yields `(ν E4).toReal ≤ (M/(3k/10)^4) r^4` from an integrable fourth moment under the same finite measure ν. In particular ν may be the constructed weighted probability law, or the unnormalized finite measure with density `W/r²` used in source (7.7). The identification of that density and its uniform joint moment remain explicit model work, not consequences of Markov. No fifth-root surrogate or square-root transfer is used.

`double_soft_integral` and `matrix_soft_integral` implement the actual source integral:

```
∫₀^(DrU²) λ(λ+ErU) dλ
  = r³ [(D³/3) U⁶ + (ED²/2) U⁵].
```

The retained saddle mixed-square contribution is the second term. `spectral_kernel_eq` multiplies by `r² P U^(2m)` and gives **exactly** `r⁵ spectralEnvelope`, without throwing away either soft factor. `depth_numerator_r5` integrates that identity against an arbitrary remaining-coordinate measure, requiring a genuine integrable polynomial envelope and its moment bound. `weighted_depth_r3` uses the existing `weightedLaw_event_real` identity and the FULL lower normalizer `cZ r² ≤ ∫ W` to yield `(M/cZ)r³`. It does not call the Cauchy–Schwarz transfer.

## Exact minimal OPEN interface

The missing source-to-formal theorem has the following conclusion; in the code it is a **definition of a proposition**, not an axiom and not an asserted proof:

```lean
MatrixDepthTransport μ W lam M3 k r ν m D E P U
```

Its full expansion is:

```lean
(∫ x in depthEvent k r lam M3, W x ∂μ) ≤
  ∫ z, r ^ 2 * P z * U z ^ (2 * m) *
    (∫ t in (0 : ℝ)..(D * r * U z ^ 2),
      t * (t + E * r * U z)) ∂ν
```

The consumer already proves the desired numerator power and normalized probability power from this pre-integration statement and:

```lean
Integrable (fun z => spectralEnvelope m D E (P z) (U z)) ν
(∫ z, spectralEnvelope m D E (P z) (U z) ∂ν) ≤ M
Integrable W μ
0 ≤ᵐ[μ] W
MeasurableSet (depthEvent k r lam M3)
0 < r
0 < cZ
0 ≤ M
cZ * r ^ 2 ≤ ∫ x, W x ∂μ
```

For the **source realization when m≥2**, the missing adapter must construct the measurable ordered-eigenvalue/angle pushforward of `B=-A_M`, its domination by symmetric-matrix Lebesgue measure with the source Gaussian density majorant, and the residual-J disintegration. Choose `U=J+Λ` and let `P` absorb the nonnegative Gaussian/Vandermonde/angular majorant and fixed constants. The remaining-coordinate measure covers `0≤λ₂≤…≤λ_m` with no positive lower cutoff on λ₂. Prove the typed determinant bound (6.2), the source depth cutoff (7.1), then Tonelli/change-of-variables and interval extension with that positive majorant. Prove the displayed integrable envelope and its uniform bound from the Gaussian polynomial moments and residual moment order `2m+6`.

This requires **no eigenvalue independence**, GOE identity, inverse-eigenvalue moment, or exclusion of corank-two/higher intersections. Repeated-eigenvalue boundary strata are handled by the measure change of variables, not an assumption that λ₂ stays away from zero. The abstract ν may be coupled; only the concrete source adapter uses the independence of the whole residual J from the matrix. Merely supplying the desired `O(r³)` tail as a hypothesis would not discharge this interface.

## The separate m=1 argument

The m≥2 argument must not hold Λ fixed when Λ=λ. `scalar_near_or_far` proves source (7.5) from its expanded depth inequality:

```
λ ≤ 2DrJ²+2Drλ²  ⇒  λ ≤ 4DrJ² OR λ > 1/(4Dr).
```

`scalar_soft_integral` supplies the near-branch calculation:

```
r² J⁴ ∫₀^(4DrJ²) λ(λ+ErJ²) dλ
  = r⁵ (64D³/3 + 8ED²) J¹⁰.
```

`scalar_far_fourth_moment` retains the far event and gives its fourth-moment bound on any supplied finite measure, matching (7.6). With density `W/r²`, this is `O(r⁴)` before restoring the prefactor, hence `O(r⁶)` in the numerator. The scalar density/near-branch domination, uniform `J¹⁰` moment, and weighted far joint moment are still source-model inputs. This packet does not claim to instantiate them or to close every dimension. There is no auxiliary s-integration or invented tail in this source bridge.

## Reproduction and trust boundary

From an exact checkout of this branch with its pinned Lean toolchain installed:

```sh
bash companions/cap_i4_source_bridge_20261005/replay.sh
```

This runs companion regression/mutation controls, original formal Python tests in normal and optimized modes, the original source gate, original 40-target executable gate and its negative controls, then the companion Lean build with warnings as errors, boundary examples, all 20 declaration axiom closures, fresh `leanchecker`, and two rejection controls (dropped mixed soft term and discarded scalar far disjunct). Allowed transitive axioms are only `propext`, `Classical.choice`, and `Quot.sound`. The static contract gate is not a substitute for Lean or analytic alignment review.

The dedicated workflow is read-only and does not dispatch an integrator. Logs go to `.lake/cap-i4-evidence/`; the original gate's local receipts remain in their original generated directory. This README deliberately carries no self-awarded kernel status and does not reuse a prior receipt for new bytes.
