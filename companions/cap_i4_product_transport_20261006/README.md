# Cap I4: density and residual-product-law transport

Dylan Roy — delegated AI work. Actual author OpenAI / GPT-6 Astra Pro,
`cap-i4-product-transport-20261006-r14`; pickup main#229/6014390438.
Scientific effect NONE. Organizational-independence credit 0. No self-merge.

This isolated child of f58dc11eec08327a920cdd6f99da276178437405 adds six
conditional measure-theoretic interfaces. It does not modify the spectral
composition, its separate author's branch, production formal/, or the main queue.

## Intended contract

1. Measurability of the residual/eigenvalue positive-cone test.
2. The existing exact pi/gap inequality under actual `volume.withDensity p`.
3. Integration over a residual measure, allowing a nonseparable kernel K(j,l).
4. The same inequality under an actual product measure.
5. Pullback to a measurable pair (J,B) whose JOINT pushforward equals that product.
6. An arbitrary orientation-dependent weight pointwise bounded by the positive
   spectral/residual kernel inherits the integral bound.

All six exact types are frozen in Contract.lean. The initial source is a stub:
it deliberately cannot satisfy those contract applications. A successful full
hosted run is required before saying the new statements are kernel-checked.

The density p, spectral envelope H and kernel K have explicit measurable-input
requirements. The matrix law is s-finite where Tonelli needs it; an actual
probability density satisfies this condition. The outer residual measure is not
silently normalized or assumed to be a conditional law. Nonnegative ENNReal
integrals allow infinity. No product of separate K moments is asserted.

The joint-law premise is the missing model interface, NOT a conclusion inferred
from marginal laws. Original-law independence can establish that identity;
conditioning on typing in general destroys it. The finite tests retain explicit
Bernoulli countermodels for both mistakes. They are not Gaussian counterexamples.

## Relation to the depth envelope

The caller may choose a measurable K depending on r, j, lambda and Lambda,
including the indicator lambda <= D r (j+Lambda)^2 and the complete two-soft-factor
majorant A r^2 Lambda (j+Lambda)^3 lambda (lambda+E r (j+Lambda)). A pointwise
bound of the actual weight by this kernel is a separate input. This module neither
proves that pointwise field bound nor evaluates the moving spectral integral,
and never replaces it by a Cauchy–Schwarz estimate. The cap geometry, moments,
uniform constants and full normalizer still need their own concrete realization.

## Source binding and replay

The five parent Lean modules and inherited evidence helper are fixed by Git blobs
in replay.py. The same script pins P (dfed3b8d...) and its inverse-congruence erratum,
Lean4.34.1 and all nine revisions from the unchanged formal/lake-manifest.json.
The density API is mathlib d13f23b723b8a846827a245b89c10fc7d3f11612,
MeasureTheory/Measure/WithDensity.lean blob5614894732293f9dbc288ad091284a54d909a3f4.
The spectral input's completed kernel receipt does not replace its separately
requested alignment review main#229/6009704131, still unobserved at preparation.

Run from a complete checkout with pinned dependencies installed:

```sh
ROOT="$PWD"
(cd formal && lake env python3 -B -S "$ROOT/companions/cap_i4_product_transport_20261006/replay.py")
```

The replay is a scoped adaptation of the source-authenticated spectral runner
03169fcc86253431dec52bbe103830866f241739, not a new evidence framework. It compiles
all five exact parents, then this child, the exact Contract, six axiom/type reports,
and fresh leanchecker. Two inherited factor/sign false-goal controls are scalar
sanity controls, not proofs of joint-law factorization. Partial timeout output is
retained, but no completed receipt is manufactured. All failure records remain.
Source tests in normal and optimized Python are finite/source checks only.
No local Lean or full-repository run is claimed where unavailable. Nonauthor
alignment, actual successful execution and eligible future integration are distinct.
