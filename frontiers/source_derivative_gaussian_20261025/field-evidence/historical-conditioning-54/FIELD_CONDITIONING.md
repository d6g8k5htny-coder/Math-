# Actual conditioning on the smooth coefficient carrier

`SourceSmoothConditionalKernel.lean` constructs a conditional law for the entire
actual `SmoothSample 2 L` carrier. For `L != 0`, it proves this law is a
`HasCondDistrib` of the original sample given its confluent pins at every
sufficiently small positive separation. The fixed-separation theorem uses the
explicit premise that the actual pin covariance is invertible; the final
corollary derives that premise eventually from the completed actual source
limits. Full-carrier conditioning and residual independence are conclusions.

The coefficient sampling map is literal. With actual pin observations `X`,
coefficient rows `a_i`, and covariance `G`, it sends each original sample to

    posteriorSample(x,omega)(m)
      = omega(m) + sum_i a_i(m) * (G^(-1) * (x-X(omega)))_i.

The proof derives preservation of every `goodSample` summability order and
joint measurability. The resulting measurable Markov kernel is exactly the
pushforward of `smoothLaw` by this map for every pin value, including null pins.
When `G` is invertible, every posterior sample has pins exactly `x`; the kernel
charges that fiber with probability one.

The conditional-law proof uses actual finite joint Gaussian coefficient laws,
derived zero cross-covariances and independence of every finite residual
restriction. It then proves independence of the full residual coefficient
process. A measurable carrier reconstruction turns that process result into
`HasCondDistrib id X K smoothLaw` on the original smooth carrier. It does not
replace the infinite source by a finite field or assume the desired independence.

The new law joins the completed endpoint construction precisely:

- Its adjusted-endpoint marginal equals the existing canonical endpoint kernel
  at every pin value.
- Under current pin invertibility, its physical normalized-endpoint marginal
  equals the actual physical kernel, including the literal correction away
  from the prescribed pin.
- At the prescribed null pin, its physical marginal is exactly the law used by
  the completed physical moment and normalizer estimates.
- Every measurable carrier functional inherits the specified conditional law.
  This includes arbitrary measurable carrier-event indicators, beyond finite
  endpoint observables.
- The literal smooth field also inherits the law under its coordinate-product
  sigma algebra. No stronger topological function-space law is selected here.

The new scope is one module with **54 public declarations: 48 theorems,
5 lemmas and 1 named Markov instance**. Source SHA256 is
`664892acb12d40e5bf20075e1ef633efdd4a54ae1308c714308eab3a4deaa517`,
at source commit `9c7984ea30eb6b09969405998bf5d195d793a08d` on
`codex/whole-field-conditioning-20261025`.

`FIELD_EVIDENCE_CATALOG.json` records the actual final compile, controls,
54-declaration axiom audit and named kernel replay. Each final subprocess
exited 0 and binds the same production source hash before and after. The
axiom reports contain only `propext`, `Classical.choice` and `Quot.sound`.
Controls cover reconstruction at a sample's own pins, an empty residual
restriction, the real obstruction at zero separation, arbitrary measurable
carrier events, and the final nonzero-scale-only eventual result. Earlier
failures and helper records retain their actual provenance; an empty helper
log is not promoted to a missing process receipt.

Actual OpenAI author-side contributions are credited: main implementation by
`uniform_jet_moment_sources`; carrier/projection/reconstruction support by
`normalizer_palm_research` and its `gaussian_reference_probe` helper; process
support by `regression_kernel`, with `gaussian_api` finite-index and
`endpoint_means` coefficient-covariance helpers. None supplies independent
scientific review. Different-family review remains separate.

The base fourteen-module/182-target package and its 23 inputs are referenced
by their unchanged manifests and receipts. This new-scope catalog does not
copy or recheck that baseline, broaden its review scope, or change its README,
manifest or evidence catalog. The packaging itself runs no Lean, kernel or tests.

The original research goal remains active. Full-carrier weighting/Palm and
Gamma-majorant extensions require their own actual source and qualification;
their results are not inferred from these 54 declarations. Geometric
Kac–Rice/Palm identification, the requested field-dependent event estimates,
GT5 and further parent conclusions remain part of that original goal.
Scientific effect NONE; no scientific-status or parent acceptance is claimed.
