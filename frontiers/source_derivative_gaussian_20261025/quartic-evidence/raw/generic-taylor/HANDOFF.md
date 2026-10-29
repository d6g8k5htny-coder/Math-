# New fifth-order quartic-transfer scratch proofs

26 October 2026, OpenAI/Codex `/root/normalizer_palm_research`.
Source candidate read: revised PROOF_CANDIDATE.md SHA256
`e501b80eed7702005d9dacbb9711fc030cf84716f464abbf124d98cc90c394dd`.
No production files were changed. Existing source/Peano kernel-mass evidence
was reused; no baseline proofs, builds, tests, or gates were rerun.

Namespace: `I4ActualQuarticTransfer`.

`SymmetricPeano.lean` exports:

- `peanoCubic_first_moment`: the odd weighted moment is zero.
- `peanoCubic_normalized_second_moment`: exactly
  `6 * integral peanoCubic(u)*u^2 = 1/20`.
- `symmetric_cubic_pin_second_order`: for continuous real g, the literal
  `6 * integral peanoCubic(u)*g(r*u)=2`, and the explicit pointwise bound
  `|g(r*u)-t-r*u*c| <= G*r^2*u^2/2` on [-1/2,1/2], proves
  `|t-2| <= G*r^2/40`. It proves the integral identity and the variable
  quadratic-majorant comparison; it does not replace them with assumptions.

`EndpointCoefficients.lean` exports:

- `endpoint_taylor_low_coefficients`: exact zero values of v at +/-r/2,
  r>0, and explicit degree-three endpoint Taylor-remainder bounds imply
  `|A+T*r^2/8| <= G*r^4/384` and
  `|B+C*r^2/24| <= G*r^3/192`.
- `corrected_axial_constant`: the first recovered bound together with
  `|T-2| <= G*r^2/40` implies
  `|A+r^2/4| <= (11/1920)*G*r^4`.

These are honest generic lemmas. The actual fifth-derivative Taylor remainder,
chain-rule/derivative identifications, coefficient table, Euclidean/operator C1
comparison, LM004 robustness validity, and measurable capture/branch application
remain to be supplied. No final actual Taylor estimate or capture theorem is
claimed, and this coauthor proof work gives no independent scientific-review credit.

## Genuine scalar Taylor bridge added afterward

`ScalarTaylorRemainder.lean` now derives the scalar Taylor estimate from
`ContDiff Real infinity g` and an actual global bound on the absolute
`(n+1)`th iterated derivative. It uses the Lagrange remainder theorem, with
the sharp denominator `(n+1)!`, rather than Mathlib's coarser `n!` estimate.

Its public APIs in the same namespace are:

- `scalarTaylor g n x`: the univ-based Taylor polynomial about zero.
- `scalar_taylor_remainder g hg n G hG x`: the generic sharp factorial bound,
  including x=0 and either sign of x.
- `scalarTaylor_one`, `scalarTaylor_three`: exact expansions in global
  derivatives at zero.
- `scalar_taylor_one_bound`: `|g x-g 0-x*deriv g 0| <= G*x^2/2`.
- `scalar_taylor_three_bound`: the explicit degree-three polynomial has
  remainder at most `G*x^4/24`.

No Taylor-remainder hypothesis appears in those new statements. The remaining
actual-source join is to prove the directional/gradient/Hessian scalar-curve
derivative identifications and bounds from the source's Gamma5, then compose
these lemmas with the previously compiled Peano and endpoint arithmetic.
The generic n=2 theorem also gives the Hessian scalar-curve denominator 6.

`scalar-taylor-02.json` records an actual clean exit-0 compilation and before/
after SHA256 `7b7dd01d1193ad381654ae3b4bb9e3fa32ad10bdd7a53b8f607cf884917832d8`.
The first failed local attempt is retained as `scalar-taylor-01.log`.
Only the new scratch file was checked; the earlier compiled helper evidence
was retained without rerunning it. The actual bridge owner received the APIs
and compiled source directly.

## Actual scalar-source composition completed afterward

The bridge owner requested and received two further convenience APIs,
`scalarTaylor_two` and `scalar_taylor_two_bound`, with the sharp absolute cubic
remainder `G*|x|^3/6`. This justified addition is recorded in the clean
`scalar-taylor-03.json` receipt; the final expanded scalar helper source SHA256 is
`4753458af4bdcce2e9d34872d28db9e57ea07ca8fff6b85d4e1eec197fd50059`.

`ActualCurveBounds.lean` proves actual sourceF/sourceH smoothness and their
arbitrary-order scalar derivative bounds by the literal source majorants,
plus smoothness and composition identities for iterated scalar derivatives.
Clean receipt: `actual-curve-01.json`; source SHA256
`0cc08b5f5585bdb5a295f41cf75b0c1064a4803091d899575687d16e9337fb6f`.
The bridge owner incorporated this source and the generic helpers into their
new production module; subsequent scratch imports reuse its resulting olean.

`ActualAxialCoefficients.lean`, namespace `I4SourcePinPreservingQuartic`, now
composes the sharp generic results for the literal smooth source:

- `source_axial_third_error hL r hr omega hp` proves
  `|sourceAxialThird L omega-2| <= r^2*Gamma5/40`.
- `source_low_pin_coefficients hL r hr omega hp` proves the four actual
  origin derivative bounds with constants 11/1920, 1/384, 1/192, 1/192
  in the exact raw-U order expected by the LM001 comparison.

Here `hp` is exactly `sourcePhysicalPins L r omega`; no Taylor error estimate,
axial cubic bound, lower-coefficient bound, Gaussian law or curvature threshold
is assumed. The scalar Taylor remainders follow from the actual smooth source
and Gamma5. Literal pin5=2 is derived from the four zero gradients and the
height gap before applying the Peano identity.

Clean receipt: `actual-axial-02.json`; source SHA256
`023cc6344d0182d75abd073cca9e352b57cc4adccf90e6c4c87920adfa39729e`.
The first local actual-axial attempt, retained as `actual-axial-01.log`, only
needed explicit eta-unfolding of scalar source curves. No mathematical
hypothesis was weakened or desired conclusion added to obtain the success.

These actual scalar joins are complete as compiled scratch proofs and have
been handed to the production owner. Their completion does not by itself
supply the remaining multivariable Euclidean/operator C1 comparison, the
LM004 scientific qualification, or a measurable capture/branch theorem.

New verification only:

- `symmetric-peano-02.json`: actual command, cwd, exit 0, before/after source
  SHA256, and empty-log hash. Source SHA256
  `e155326a61a86aa14696a0aec797e2f7e8c13a368b15af269fa4cd0a979e3eab`.
- `endpoint-coefficients-02.json`: corresponding actual exit-0 command receipt.
  Source SHA256
  `90d018783844623c9fae4b1a309d2ae5de8c022ccc08bd5192f843cc685febde`.
- Failed first attempts remain in `symmetric-peano-01.log` and
  `endpoint-coefficients-01.log`. They record local function-expression
  elaboration, cancellation-inequality API, and absolute-value token issues;
  no mathematical conclusion was weakened to pass.

Both successful commands were `lake env lean <absolute scratch source path>`
from `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`.
The two proofs use neither sorry/admit, custom axioms nor native_decide.
