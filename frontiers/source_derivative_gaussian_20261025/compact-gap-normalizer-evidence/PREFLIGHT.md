# Compact varying-gap actual normalizer: read-only formal preflight

26 October 2026. OpenAI/Codex `/root/compact_gap_normalizer_preflight`.
Scientific effect: **NONE**. Only this report was written. No source,
configuration, cache, build, test, kernel, control, inventory/audit or hash
campaign, commit, post or child-agent action occurred.

## Recommendation and exact scope

Use a bounded negative-curvature event and a first-moment tail subtraction.
This is a valid constructive route to the compact floor and needs less new
formal infrastructure than compact uniform dominated convergence. It needs
two genuine new analytic/algebraic joins: a **lower** Gaussian interval-mass
bound for bounded means and two-sided variance bounds, and an axial Peano
error estimate centered at `±6*k`. The existing scalar law, posterior moments,
Peano identities and physical weight estimates are reused.

Suggested successor: one new `SourceCompactGapNormalizer.lean`, importing
`SourceGapPinCurvature` and `SourceCurvatureDecomposition`. The former already
imports `SourceCompactTargetMoments`. No use of the all-target residual-radius
leaf, torus trap, H0, canonical selection, conditional/global Morse or frame
transport is needed. Keep the three active new modules frozen.

The minimum final contract is, in mathematical Lean notation:

```text
∀ L, ∀ hL : L ≠ 0, ∀ B k0 k1 : ℝ,
  0 ≤ B → 0 < k0 → k0 ≤ k1 →
  ∃ c δ : ℝ, 0 < c ∧ 0 < δ ∧ δ ≤ 1 ∧
    ∀ r : ℝ, 0 < r → r < δ →
      ∀ b k : ℝ, |b| ≤ B → k0 ≤ k → k ≤ k1 →
        Integrable (sourceSmoothWeight L r) (sourceGapLaw hL r b k) ∧
        c*r^2 ≤ ∫ sample, sourceSmoothWeight L r sample
                    ∂sourceGapLaw hL r b k
```

Here `sourceGapLaw` is the literal actual coefficient posterior at target
`![b-k*r^3/2,0,0,0,0,12*k]`, and W is the unchanged physical strict
maximum/saddle determinant weight. The radius and coefficient are uniform
over this bounded height/positive-gap rectangle; they may depend on
`L,B,k0,k1`. Signed `L≠0` is allowed. No uniformity over varying L, unbounded
b or `k0→0` follows. This fixed-axis/origin contract does not assert a framed
or translated law.

## Exact reusable interfaces

All source paths below are relative to
`/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`.
These are read source references, not new execution evidence.

| Needed fact | Exact interface | How it is reused |
|---|---|---|
| Actual gap law and target | `SourceCompactTargetMoments.lean:150`, `:153`, `:166`, `:174` | Literal six-vector and every-target raw/confluent transport. |
| Target norm bound | Same file `:180`, `sourceGapPins_norm_le` | For `0≤r≤1`, `|k|≤k1`, gives `‖pGap‖≤|b|+13*k1`. |
| Original posterior moments | Same file `:111`, `sourceGammaRadius_allTarget_moments`; `:204`, `sourceGapLaw_height_moments` | One interval before all targets and all natural moments. Use only n=1 for the cutoff and n=4 for W integrability. |
| q and Gamma | `SourcePinCurvatureBounds.lean:165`, `:168`, `:174`, `:184`, `:188`, `:198`, `:738` | Original Γ; `sourceQ=sourceContactQ`; measurability, Γ≥1, derivative-majorant domination. |
| Scalar Gaussian parameters | `SourceCurvatureDecomposition.lean:31`, `:34`, `:36`, `:988` | `μ=curvatureBeta L r ⬝ᵥ p`; `τ=curvatureVariance L r`; scalar law is `gaussianReal μ τ.toNNReal`. |
| Target-independent beta and variance floor | Same file `:515`, `curvature_uniform_parameter_bounds hL 0` | Supplies one interval, covariance invertibility, `τ≥V/2` and every component `|β_i|≤J`. Its fixed prescribed-mean bound at b=0 is unused. |
| Variance upper bound | Same file `:477`, `curvatureVariance_tendsto` | With `V=sourceContactSchur L>0`, one eventually bound `τ≤2V`; this is a consequence of an existing limit, not a new covariance argument. |
| Actual q marginal | Same file `:754`, `curvatureReconstruct_Q`; `:910`, `:928`, `:1003`, `:1026` | The existing every-target whole-carrier reconstruction/product law pushes actual q to the scalar Gaussian. A short marginal composition suffices; do not rebuild the Gaussian/product law. |
| Existing density integration pattern | Same file `:947`, `:963` | These are **upper** PDF/mass bounds, not the required lower bound. Reuse their Gaussian integral identity/proof pattern for the new lower estimate. |
| Generic weighted errors | `SourcePinCurvatureBounds.lean:23`, `:46`, `:91`, `:133`, `:146` | Positive kernel masses and affine weighted errors. The cubic pointwise lemma fixes the average at2; it needs a translated-function wrapper for general12k. |
| Actual cubic pin and Peano identity | Same file `:366` (`sourceF_third_lipschitz`), `:474`, `:492`, `:607` | The actual pin5 integral plus the Peano identity gives axial centers ±6k. Existing full endpoint errors at `:607` specialize pin5=2 and cannot be applied verbatim. |
| Already generalized endpoint bounds | `SourceGapPinCurvature.lean:28`, `:67`, `:80` | First four normalized entries bounded by Γ, and transverse q-errors ≤rΓ; no sixth-pin restriction. |
| Actual support and weight upper bound | Same file `:160`, `:183`, `:214` | On one interval from hL alone, Q-a.e. full literal pin support and `W≤10*r²*Γ⁴`. These exports remain frozen. |
| Literal physical Hessians and W | `SourceSmoothPalm.lean:132`, `:137`, `:141`, `:145`, `:149`, `:156`, `:163`, `:169`, `:176` | Exact physical/normalized identities, strict-type definition, nonnegativity and measurability. |
| Strict negative Hessian criterion | `inputs/ResearchFormalCoreR1/DeterminantMoment.lean:139`, `dm2_negative_iff` | A negative first diagonal entry and positive determinant prove the actual quadratic-form negativity. |
| Unweighted probability | `SourceSmoothConditionalKernel.lean:288`, `:294`, `:303` | The actual kernel is already Markov for every target. Its probability property is independent of the W normalizer. |
| Markov inequality | Mathlib `MeasureTheory/Integral/Bochner/Basic.lean:1162`, `mul_meas_ge_le_integral_of_nonneg` | Existing finite-measure first-moment inequality. `SourceWeightedCurvatureBound.lean:46` illustrates its current source use. |

## Constructive route and honest constants

Fix `L≠0`, `B≥0`, `0<k0≤k1`. Write Q for the actual gap law, q for
`sourceQ L`, Γ for `sourceGammaRadius L`, and `V=sourceContactSchur L>0`.
All intervals below are reduced to one positive minimum before b,k,r.

**1. Uniform negative interval mass.** Take J≥0 and an interval from
`curvature_uniform_parameter_bounds hL 0`. Componentwise beta bounds and the
Pi-norm target estimate give the safe bound

```text
|μ(r,b,k)| ≤ M := 6*J*(B+13*k1).
```

The factor6 makes this valid directly for the current Pi/sup norm; do not
silently use a Euclidean dot-product estimate with that norm. A tighter
bound using the two nonzero target coordinates is optional. Intersect with
the existing variance-limit interval to obtain
`V/2≤τ(r)≤2V`, and with `r≤1`.

For `x∈[-2,-1]`, `|x-μ|≤2+M`, so the actual Gaussian density satisfies

```text
gaussianPDFReal μ τ.toNNReal x
  ≥ η := (sqrt(4*pi*V))⁻¹ * exp(-(2+M)^2/V) > 0.
```

The prefactor uses the variance **upper** bound `τ≤2V`; the exponent uses
the variance **lower** bound `τ≥V/2`. Integrating on the length-one interval
gives `Q.real {sample | q(sample)∈Icc (-2) (-1)}≥η`, by the existing actual
q marginal. The `toNNReal` coercion must use `τ>0`. This is the only new
Gaussian estimate needed. An existing upper-density bound alone cannot
produce this lower mass, and no mean-zero assertion is available or needed.

**2. Truncate the original radius without independence.** The old n=1 height
moment gives a common bound `E_Q Γ≤H:=C1*(1+B)`, H≥0. Choose

```text
A = max 1 (2*H/η).
E = {sample | q(sample)∈Icc (-2) (-1) ∧ Γ(sample)≤A}.
```

Then A≥1 is finite and Markov gives `Q.real {Γ>A}≤H/A≤η/2`. The elementary
finite-measure subtraction inequality yields `Q.real E≥η/2`. No q/Γ
independence is asserted; they can be strongly dependent. E is measurable
from the existing q and Γ measurability. Full literal pin support is Q-a.e.
and can be intersected without losing mass. Only an unweighted probability
law is used here, so there is no normalizer circularity.

**3. Parameterized axial errors.** On a literal fiber with
`h3=h4=0`, `h5=12*k`, write `v=sourceNormalizedEndpoints L r sample`.
The missing successor lemma should derive

```text
|v0+6*k|≤r*Γ,       |v1-6*k|≤r*Γ.
```

Use `pin5_integral`, `source_pin5_eq`, `sourceF_third_lipschitz` and
`source_normalized_peano`, then the existing affine weighted-error lemmas.
There is no need to edit or repeat the proof of the old cubic scalar lemma:
apply `cubic_pin_pointwise_error` to `g'(x)=g(x)-12*k+2`. Its cubic average
is2 by the already known cubic kernel mass1/6, and its Lipschitz constant
is unchanged. This produces `|g(r*u)-12*k|≤r*Γ4`; the half-mass affine
kernels give the two displayed errors, even with the sharper right side
`r*Γ4/2`. Keep the conservative rΓ form for the following arithmetic.
The remaining needed bounds `|v2|,|v3|≤Γ` and
`|v4-q|,|v5-q|≤rΓ` are frozen existing generalized exports.

**4. Strict types and an actual physical weight floor.** Choose

```text
δdet = min 1 (min (1/(2*A)) (k0/(2*A^2))) > 0.
```

For `0<r<δdet`, on E and the literal fiber, `rA≤1/2` and
`rA²≤k0/2`; since A≥1 also `rA≤k0/2`. The error bounds give

```text
v0≤-3*k0,  v1≥3*k0,  v4≤-1/2,  v5≤-1/2,
|v2|≤A,   |v3|≤A.
DM := v0*v4-r*v2^2 ≥ k0 > 0,
DS := v1*v5-r*v3^2 ≤ -3*k0/2 < 0.
```

The literal physical determinants are `r*DM` and `r*DS`. The first physical
diagonal entry at M is `r*v0<0`; `dm2_negative_iff` therefore proves strict
negative definiteness there. The S determinant is strictly negative. Thus
the actual `sourceSmoothTyped` branch holds, and the exact physical weight
formula gives

```text
W = r^2 * DM * (-DS) ≥ k0^2*r^2.
```

This deliberately wastes a factor3/2. It does not replace W by a proxy or
introduce a potential-rescaling factor. The three equations h3,h4,h5 by
themselves give these **Hessian types**, not endpoint criticality: the
common gradient rows1,2 must also vanish to call the endpoints actual
critical maximum/saddle points. They do vanish on the full gap-law support;
`SourceConfluentPins.lean:23`, `:29`, `:35` gives the exact raw inverse.
For the integral floor only the Hessian-type/W assertion is needed.
No statement about remote critical points, global Morse behavior, distinct
critical values, canonical merging, or ordinary elder pairing enters.

**5. Integrability and integration.** Before comparing Bochner integrals,
derive `Integrable W Q` from its measurability/nonnegativity, Q-a.e.
`W≤10*r²*Γ⁴`, and the old n=4 moment. A nonintegrable real Bochner integral
cannot be treated as a positive extended integral. Integrate
`k0²*r²*1_E≤W`, valid Q-a.e. after adding full pin support. Then

```text
∫ W dQ ≥ k0²*r²*Q.real E ≥ (k0²*η/2)*r².
c := k0²*η/2 > 0.
```

Take δ as the positive minimum of the beta/floor interval, variance-upper
interval, moment interval, frozen gap-law support/weight interval and
δdet. All constants are selected before b,k,r. No compact-uniform DCT,
posterior convergence theorem or residual-law moment generalization is
required by this route.

## Remaining formal obligations and finite next contract

The derivation above is a preflight candidate contract, not a claim that
the new Lean floor has already been implemented or kernel checked.

1. Prove the lower Gaussian PDF/unit-interval lemma under explicit
   `V>0`, `M≥0`, `|μ|≤M`, `V/2≤τ≤2V`. Compose the existing actual q law;
   retain the target-dependent affine mean.
2. Wrap the old cubic scalar error at an arbitrary target constant, derive
   the two axial errors for pin5=12k in the new leaf, and prove the exact
   determinant/type/weight lower arithmetic. Do not add these to the frozen
   gap-curvature leaf.
3. Assemble the uniform first-moment truncation and measurable intersection
   using finite-measure subtraction, with no independence premise.
4. Derive W integrability using n=4; export the closed compact actual-law
   theorem displayed above with no density, moment, pin-support, good-event
   probability or desired-floor certificates left as final premises.

A few local/private helper lemmas plus the final export suffice. The exact
public/helper/generated inventory is an implementation choice to freeze in
that future leaf's own contract; this preflight does not initiate it. Any
future new-only controls should exercise nondefault k, signed L, nonzero b,
strict physical types, the exponent/prefactor variance directions and a
single appropriate false mutation. They should not replay old density,
moment, kernel or control work. No normalized cutoff probability or Parent
theorem belongs in this minimum floor leaf.

## Relation to the accepted contact-limit proof

Item4 of `/workspace/scratch/actual-fold-cutoff-probability-preflight/REPORT.md`
correctly identifies a real **formal interface join**, not an unproved piece
of the accepted mathematics. The fixed-b, k=1/6 theorem
`SourceEndpointEstimates.lean:245` cannot supply the compact quantifier order
by renaming/minimizing its existential constants.

The accepted conventional
`actual-adaptive-elder-application/PROOF.md:295–352` remains applicable and
accepted as supplied. It uses common-source contact coupling, the actual
limit `W/r²→36*k²*q²*1(q<0)`, compact positivity of the contact negative
second moment and uniform integrability. Formalizing that route would also
yield a stronger uniform contact-limit result, but requires coupled-field
convergence and compact sequential/uniform expectation infrastructure that
the floor alone does not need. The constructive event route proves only a
coarse positive floor, with explicit conservative constants, from existing
finite-r exports. It is therefore the economical next floor formalization.

Neither route requires global Morse for the floor. The accepted proof's
later canonical/elder/count/frame conclusions have their own inputs and are
not inherited by this successor leaf. No accepted conventional argument is
re-audited here.

## Verification reuse, frozen objects and authority

Read and apply `/workspace/AGENTS.md`: completed applicable verification is
reusable; a new agent/session/handoff alone does not warrant replay. Root's
current 38 qualified modules / 32 support inputs and their completed
mathematics remain dependencies. The three active new leaves have completed
their own strict compilation, sole named own-module kernel check,
actual-constant inventory/standard-three-axiom audit and new controls, per
their existing producer/reviewer records. Their frozen source identities are
transcribed, not recomputed:

| Frozen module | Source SHA256 |
|---|---|
| `SourceFoldWeightedProbability` | `58b77d6c0886fb5ef005749f468648d3c3ce6c99905f89963bf99c4ebee763d0` |
| `SourceGapPinCurvature` | `67f6c671e4ed8a7cb8557fc6027403f4fd1e94cba984e672eaa3ceb94ab8847e` |
| `SourceAllTargetCurvatureResidual` | `4ae29bc3f2f206cca558df3f78853061cf4892499ac918e40253edd68d44371f` |

Producer evidence: `/workspace/scratch/fold-weighted-probability-construct/REPORT.md`,
`/workspace/scratch/gap-pin-curvature-construct/REPORT.md`, and
`/workspace/scratch/all-target-curvature-residual-construct/HANDOFF.json`.
Same-family technical source/spec PASS reports are separate records and
earn zero provider-distinct review credit. Pending provider-distinct process
requirements do not erase completed mathematical or exact-source execution
evidence. This preflight ran no additional verification.

Repository AGENTS, README, formal README/SCOPE and required-check contract,
plus the local canonical mandate, standing delegation and current workflow
were read. Preserve the canonical owner links in future onboarding:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

These links do not establish that a future recipient has read them. Source
qualification, provider-distinct alignment and scientific acceptance remain
distinct. No source/campaign/global-status change is made by this report.
