# Actual carrier conditioning, determinant weighting and derivative tails

This four-module extension proves a conditional law on the entire actual smooth
coefficient carrier, constructs its literal normalized Hessian-weighted
probability, and derives measurable global derivative majorants with uniform
conditional moments and tails. The source-model inputs are nonzero `L`, a fixed
arbitrary real height `b`, and the natural derivative/moment orders where used.
Posterior drift is retained. No final conditioning, moment, normalizer or tail
conclusion is inserted as a model premise.

| Module | Registered audit targets | Result |
|---|---:|---|
| `SourceSmoothConditionalKernel` | 54 | Whole-carrier `HasCondDistrib`, exact all-pin fiber and physical endpoint marginals, every measurable carrier functional, and the `L != 0`-only eventual conditioning result. The 54 include a named Markov instance. |
| `SourceSmoothPalm` | 27 | Literal actual raw-Hessian maximum/saddle weight on the full carrier; normalized density probability; all measurable carrier-event bound; exact weighted endpoint pushforward and full raw-pin/strict-type support. |
| `GaussianWeightedMajorants` | 8 | Sharp natural moments for weighted absolute Gaussian series, and a separately proved exponential estimate and Gaussian upper tail. Only standard Gaussian marginals are needed; coordinate independence is not assumed. |
| `SourceConditionalMajorant` | 20 | Global pointwise derivative bounds, uniform actual conditional moments, drift-retaining Gaussian upper tails, and every requested natural polynomial cutoff rate under the conditional and weighted carrier laws. |

The registered ledger has **109 declarations: 95 theorems, 13 lemmas and one
Markov instance**. `SourceSmoothPalm` also exports the named probability instance
`sourceSmoothLaw_isProbabilityMeasure`; it is disclosed separately with
transitive dependency coverage. Thus the complete named theorem/lemma/instance
inventory has **110 declarations and two instances**, without relabeling the
extra instance or inventing direct print output.

## Conditioning and literal full-carrier weight

For actual pins `X`, coefficient rows `a_i` and covariance `G`, posterior
sampling is the explicit coefficient shift

    posteriorSample(x,omega)(m)
      = omega(m) + sum_i a_i(m) * (G^(-1) * (x-X(omega)))_i.

Every source summability order and joint measurability are proved preserved.
The resulting measurable Markov kernel is specified at every pin value,
including null pins. Current covariance invertibility gives exact pin support
and the full-carrier conditional law. Completed actual covariance limits supply
that invertibility at all sufficiently small positive separations from `L != 0`
alone. Actual finite Gaussian laws and zero cross-covariances establish full
residual-process independence; that independence is not assumed.

At the prescribed pins, its physical endpoint marginal is exactly the law used
by the completed endpoint estimates. `SourceSmoothPalm` defines `W_r` from the
strict maximum/saddle determinant weight of the actual raw endpoint Hessians,
then defines the actual full-carrier measure by density `W_r / integral W_r`.
For fixed `L != 0,b`, the proof derives a small-radius interval with
`integral W_r^2 <= C*r^4`, `integral W_r >= c*r^2` and a probability measure.
Every measurable carrier event satisfies

    weighted.real(E) <= sqrt(C)/c * sqrt(conditional.real(E)).

The weighted physical endpoint pushforward is the previously constructed
weighted endpoint law. The carrier law has full mass on the literal prescribed
values and zero gradients, and on the strict maximum/saddle type selected by
positive weight. This is an explicit source probability; no geometric
critical-point-process Palm identity or global Morse property is inferred.

## Gaussian series and actual derivative control

For nonnegative summable weights with total `W`, the generic series `Gamma_w`
obeys, for every natural `n`,

    integral Gamma_w^n <= W^n * E|N(0,1)|^n.

The natural moment constant is retained exactly. A separate folded-Gaussian
exponential argument, finite Jensen inequality and infinite-limit argument prove

    integral exp(t*Gamma_w) <= 2*exp(t^2*W^2/2),

and hence `P{R <= Gamma_w} <= 2*exp(-R^2/(2*W^2))` for `W>0,R>=0`.
The Gaussian tail is not inferred merely from all fixed moments.

For the actual field, the measurable `Gamma_k` dominates the operator norm of
`D^k f(x)` at every spatial point. Actual posterior algebra derives a fixed
positive summable weight and drift `a >= 0` with
`Gamma_k(posterior) <= a + Gamma_w`, uniformly for small positive `r`.
This yields every natural conditional moment on one radius interval uniform in
the moment order, and constants `a,s,delta` with

    Q_r{a+R <= Gamma_k} <= 2*exp(-R^2/(2*s^2)).

Both conditional and actual weighted carrier probabilities assign the cutoff
`{r^(-1) < Gamma_k}` a bound `M_n*r^n` for every requested natural order `n`.
The weighted proof uses conditional order `2n` and retains the square-root loss.
No posterior centering is substituted. The measurable Gamma certificate avoids
assuming measurability or identification of an arbitrary uncountable supremum.

## Qualification and remaining original goal

`FIELD_EVIDENCE_CATALOG.json` binds each frozen source, actual commands/exits,
raw logs, controls and 109 direct axiom reports. The four new named kernel
replays and final production compiles exited 0. Only the three standard axioms
appear. The extra probability instance is recorded as a dependency of printed
parents, not as an invented direct audit. Gaussian-majorant production is clean;
its controls retain two actual deprecation warnings. Positive and false
controls distinguish strict boundaries, zero normalizers, posterior drift,
absolute values and nonunit weights. Failures retain their original records.

Actual helpers are OpenAI author-side contributions: carrier/projection support
from `normalizer_palm_research/gaussian_reference_probe`; process and density
support from `regression_kernel/gaussian_api`; covariance and raw-pin support
from `regression_kernel/endpoint_means`; separate exponential support from
`gaussian_reference_probe`. Conditional-majorant implementation is by
`dm2_landed_composition`; its `peano_strategy` contribution was earlier read-only
Lp API research, not a later implementation helper that was never created.
Different-family scientific review remains separate.

The original 54-declaration snapshot is preserved unchanged. The fourteen-module
baseline and 23 inputs are referenced through their existing manifests/receipts;
they are neither duplicated nor rechecked. Packaging runs no Lean, kernel or
tests and does not edit the old baseline README/manifest/catalog.

The original goal remains active. Historical midpoint nine-jet/event
normalization, any specifically required chart-supremum representation,
geometric Kac–Rice/Palm and Morse/elder/counting identification, P0.2 and later
parents require their actual remaining joins. A read-only single-curvature
parent proposal is outside this qualified four-module scope. Scientific effect
NONE; no parent closure or scientific-status acceptance is claimed.
