# Small-lifetime doublets and a companion-moment crossover

OpenAI / GPT-6 Astra Pro. **New conditional consumer; nonauthor analytic review
OPEN. Scientific effect NONE. No self-merge.** This packet recovers the unfinished
small-lifetime calculation, not the separately published fixed-r PR182 theorem.

## Exactly which limit

PR181 defines the limiting shape of a distant actual elder partner. We take that
explicit shape probability, condition its lifetime fraction e<=epsilon, and let
epsilon->0. Its field interpretation is conditional on PR181's own hypotheses
and actual-elder interfaces. Order: original r->0, distant microscopic radius
->infinity, THEN epsilon->0. A later companion-threshold limit is distinct.
No finite-r uniform estimate or unbounded moment transfer is asserted.

## Results in PROOF.md

- The exact singleton/doublet boundary is `2x^3+3e x^2=e^2`, where x=-u-1/2.
  Singletons remain at every positive cutoff. Their conditional probability is
  `(486/169)2^(-2/3) epsilon^(1/3)+O(epsilon^(2/3))`.
- `(e/epsilon,x/sqrt(e))` tends in TV at O(sqrt(epsilon)) to independent densities
  `4y^3` and `(81/13)w(1-w^4)` on `0<y<1`, `0<w<1/sqrt(3)`. Including the
  singleton/doublet tag makes the leading TV error order epsilon^(1/3).
- The other/elder radius ratio tends weakly to `V=(1-W^2)/(2W^2)` with exact tail
  `81/[26(2T+1)]-27/[26(2T+1)^3]`, hence exponent ONE and coefficient81/52.
  The companion/elder height ratio tends to `V^3(V+2)/(2V+1)`, with exponent1/3.
- At each FIXED positive epsilon, the ratio still has tail exponent THIRTEEN.
  A uniform algebraic envelope proves the transition occurs at scales of order
  epsilon^(-1/3), without asserting a full uniform crossover profile.
- The moment transition is explicit: powers p<1 converge; the mean is
  `(27/52)log(1/epsilon)+O(1)`; for1<p<13, the p-th moment is asymptotic to
  `K_p epsilon^(-(p-1)/3)`; powers p>=13 diverge already at positive epsilon.
  K_p is an explicit one-dimensional integral; K4=30/13,K7=441/65,K10=3270/91.

The assertions are proved for the explicit finite-dimensional law, including
normalization and corner domination. They are not consequences of weak moment
convergence alone. In particular the exponent-one law does not overwrite the
fixed-epsilon exponent13, nor PR182's fixed-separation inverse threshold2/3.

## Reproduction

From a full Git checkout containing both pinned source objects:

    python -B -S frontiers/small_lifetime_shape_20260930/verify.py

Standalone download:

    python -B -S verify.py --local-only

The latter explicitly reports source_pins_checked=false. The hosted workflow
must authenticate the actual two source commit/path/size/SHA256/blob bindings.
All real source Git reads disable replacements and check path/object modes.
Local temporary Git repositories test that behavior, not the project sources.

46 unit-test methods pass in each ordinary/optimized Python mode, including
589 rational classifier cases,12 independent square-to-shape Jacobians, exact
polynomial moments, interval root bounds, signed companion identities and16
real-Git/packet regression methods. Six semantic mutants reject in both modes.
The scripts use only the standard library; there is no Lean formalization of
the new analytic results. Finite tests are not independent mathematical review.

## Review requested

A: exact singleton boundary, two scales, normalized TV limit and sharp singleton
coefficient. B: companion/height limits and change-of-variables tail formulas.
C: uniform tail envelope, finite-cutoff exponent13, corner domination, K_p and
the critical mean coefficient27/52. All reviews must bind exact proof bytes and
declare source exposure. Previous PR181 acceptance, if any, is not a new verdict.
