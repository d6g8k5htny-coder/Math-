# Author-side review: new moment and scalar modules

Verdict: **no Critical, Important, or Minor findings** in either reviewed source cut. Both modules satisfy their frozen requirements, and their theorem statements and proof routes provide the requested mathematical task quality within the stated module scopes.

This is an OpenAI same-family author-side source review. It supplies **zero different-family scientific-review credit**. The modules are published at PR51419d2608; separately authenticated different-family scientific alignment remains pending. Scientific effect: NONE.

## Scope and evidence reused

Reviewed the frozen `SOURCE_COMPACT_TARGET_MOMENTS.md` and `SOURCE_ADAPTIVE_FOLD_SCALAR_BARRIER.md` before the two-file `REVIEW_PACKAGE.diff`, then each module's `SCOPE.md`, `HANDOFF.md`, and evidence catalog. Source identities supplied by the qualified packet:

| Module | Source cut | SHA256 |
| --- | --- | --- |
| `SourceCompactTargetMoments` | `e2c819cf8161f0dc37de113f0157a058ba0fd2ec` | `4fc28898f09381b4bfd0a15324556d2f3cb68f4b39063aa3acf12db7759ccfc8` |
| `AdaptiveFoldScalarBarrier` | `bb5a32ef10a06289ab14680b5ed1cf809d3457d6` | `cfe6a63a789ae085c2351d9d0be9bcf998f911d8c2e80bb01e1dd9e2b74c30d5` |

The applicable completed warning-as-error compiles, one named kernel check per new module, axiom inventories and meaningful controls are reused as evidence. The original 29-module/25-input evidence is likewise retained. No compile, build, test, kernel, axiom, hash audit or control was rerun. No source, registration, manifest, commit or post was changed. Only this report was written.

Narrow inherited interfaces were read to resolve whether the new proof genuinely uses the actual covariance/contact limit, original-sample posterior map, Gaussian weighted-series moments, existing radius, and every-target raw/confluent transport. This was source-interface review, not renewed verification or a broad review of old mathematics. Pending provider-distinct process requirements do not erase the completed mathematical evidence.

## `SourceCompactTargetMoments`

**Specification compliance: pass. Mathematical task quality: pass.** Line references below are to `frontiers/source_derivative_gaussian_20261025/SourceCompactTargetMoments.lean`.

- Lines 28–41 derive actual inverse bounds and actual `IsUnit` on one positive interval from inherited contact-limit results. Taking the prescribed-bound helper at fixed height zero introduces no target, moment, invertibility, variance or normalizer premise. The inherited helper derives its inverse bound by continuity at the nondegenerate actual contact covariance; the additionally intersected interval supplies actual invertibility.
- Lines 45–90 construct a fixed nonnegative summable original-coefficient weight and a nonnegative affine constant. The posterior sampling majorant retains the full linear dependence on the literal target norm. The use of the existing order-five majorant bounds the existing `sourceGammaRadius`; it does not substitute a new radius or a different Gaussian law.
- Lines 93–147 derive integrability and integral bounds by prior Gaussian weighted-series moments and measurable posterior pushforward. The final quantifier order at lines 111–116 is `exists δ ... forall n, exists C ... forall r ... forall p`: the same actual positive interval works for every natural moment and every six-dimensional target. Neither a desired moment bound nor a unit interval is assumed. The interval's upper bound by one is proved, and the moment constant is an actual finite prior integral.
- Lines 150–178 use the genuine target `(b-k*r^3/2,0,0,0,0,12*k)`, its actual posterior kernel, the exact `k=1/6` specialization, and the raw target `(b,b-k*r^3,0,0,0,0)`. The raw identity uses the inherited every-target sampling equality, including probability-zero targets, rather than an almost-everywhere conditional-law uniqueness argument. The fixed row-five value two is used only for the exact specialization.
- Lines 180–224 bound the varying-gap target norm and deduce `C_n(1+|b|)^n` for all heights and bounded `|k|`, reusing the all-target interval before choosing the moment or target. The auxiliary norm lemma's `0 <= r <= 1` hypotheses are discharged from that interval in the final theorem; they are not unproved final premises.

The architecture proves the requested uniformity through an explicit samplewise domination and prior moments. It is substantive all-target mathematics rather than a wrapper around an assumed desired estimate. No corrective change is requested.

## `AdaptiveFoldScalarBarrier`

**Specification compliance: pass. Mathematical task quality: pass.** Line references below are to `frontiers/source_derivative_gaussian_20261025/AdaptiveFoldScalarBarrier.lean`.

- Lines 24–44 state exactly `J=[-3/2,3/2]`, `q=(x^2-1/4)/2`, the correct middle/exterior comparisons and strict signs, derivative margins at both nodes, arm gains of at least `5/12`, separation `1/4`, and the required asymmetric ceiling and floor. The `ScalarBarrier` structure is the conclusion bundle, not a hypothesis of the final adapter.
- Lines 47–74 differentiate the actual quadratic and the primitive `x^3/6-x/8`, deriving both exact comparison-arm integrals `5/12` by FTC. Lines 92–154 derive comparisons from convexity and zero pins, then strict signs and node derivative margins from those comparisons and explicit derivative jets.
- Lines 155–182 derive continuity and arm integrability from the actual jets; FTC turns the comparisons into actual potential gains. The exact gap `1/6` combines with `5/12` to yield the two separations `1/4` at lines 218–219. Gains are correctly inequalities; exactness refers to the quadratic comparison integrals, not an unsupported equality for arbitrary `a`.
- Lines 183–227 establish the three appropriate monotonicity pieces and combine them on the asymmetric domains. They do not assert the false ceiling on the whole symmetric interval. The completed canonical-fold positive control and mathematical negative control for the full symmetric ceiling remain applicable evidence.
- Lines 231–250 assume only explicit first/second derivative jets, `a2 >= 1`, the two zero pins, the actual antiderivative jet, and the normalized potential gap. They derive convexity of `a-q` from derivatives `a1-x` and `a2-1`, then apply the convex core. There is no hidden desired barrier or elder conclusion. Endpoint continuity and interior differentiation obligations are supplied explicitly. Imports at lines 1–6 use narrow mathlib APIs; the old full umbrella and generic interpolation/topological library are not reproduced.

The final theorem provides a usable deterministic derivative-to-barrier adapter with the correct normalization and constants. No corrective change is requested.

## Scope boundary and process status

The moment module proves actual unweighted all-target source-radius moments and raw/confluent specialization. It does not by itself prove angular/weighted normalizer bounds, rotation or geometric Palm statements, capture, elder conclusions, or a parent probability theorem. The scalar module proves normalized deterministic scalar comparisons; it does not construct an actual ridge, ambient rectangle, physical chart or attained path, nor prove elder death or instantiate a parent theorem. Source comments and evidence scopes accurately maintain these boundaries.

Conventional all-angle parent claims, if supported by their existing conventional evidence, are distinct from what these two Lean modules establish. This narrow review neither reopens their completed mathematics nor supplies missing formal bridges or provider-distinct scientific acceptance.

Standing onboarding/handoff links (inclusion does not establish that a future recipient has read them):

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Carry forward `/workspace/AGENTS.md`: completed applicable verification is reusable; unchanged material under the same assumptions/dependencies must not be rechecked merely for a new agent/session/handoff. Provider-distinct review is a separate process obligation.
