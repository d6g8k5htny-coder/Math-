# Numerical values of the remote singleton coefficient k ∫_X Λ of ν(1) in dimension d = 3 (continuum kernel `exp(-|x|^2/2)`, not periodized; not certified)

Object `CL-C6-REMOTE-COEFF-D3-NUMERICS-20260930-v1`. Author: Anthropic Claude (Claude Code
`session_015wNj8LPTKXsaT68G3DgPPh`). **Numerical evaluation only** (exact quadrature for the far field and the
pin weight, Monte Carlo with reported standard errors for the correlation hole). Not a proof, not an enclosure.
Scientific effect NONE: no register, catalog, GRAPH, STATUS or source change; nothing consumed is revalidated.

## 1. What is evaluated

[RM] (13), in every fixed `d >= 2`, defines the contact kernel

    Lambda_j(x; b, k, u) = p_(Y_x | U_0 = v_0)(0, b) / z_0 . E[w_0 F_j(H_x) | U_0 = v_0, Y_x = (0, b)],

with `U_0 = (f, f_x, f_xx, f_xxx, f_y, f_z, f_xy, f_xz)(0)`, `v_0 = (b, 0, 0, 12k, 0, 0, 0, 0)`, `A_0 = D_y^2 f(0)` the
`2 x 2` transverse Hessian at the pin, `w_0 = (6k)^2 (det A_0)^2 1{A_0 < 0}` ([RM] (10)), `z_0 = E[w_0 | U_0 = v_0]`
([RM] (11)), `Y_x = (grad f(x), f(x))`, `H_x = D^2 f(x)` and `F_j(H) = |det H| 1{index H = j}`, `j = 0, ..., 3`.
`Lambda = sum_j Lambda_j` is the density in [SC] (22), `beta_far = k integral_(X \ {0}) Lambda dx`, so that the
cluster-law coefficients are `nu_1 = a_1 + beta_far`, `nu_2 = a_2` ([SC] (20)–(22); [CL] (1.4)). Math-#174 evaluated
this in `d = 2`; this note evaluates the formula (13) in `d = 3` with the continuum covariance `K(x) = exp(-|x|^2/2)` in
place of [RM]'s `K_L`; no [RM] theorem is asserted for it.

Exact structure used (all checked in `remote3.py --check`):

- **Contact law at the pin.** Given `U_0 = v_0`, `A_0 = -b I_2 + G_2` with `G_2` the GOE matrix of diagonal variance
  `2` and off-diagonal variance `1` (exact rational regression; Math-#184 Lemma 1), so that
  `z_0 = 36 k^2 m_(3,b)`, `m_(3,b) = E[(det A_0)^2 1{A_0 < 0}]`, `m_(3,0) = (7 - 4 sqrt2)/2` (Math-#184 Lemma 2,
  companion, conditional; the finite-`r` normalizer `Z_r / r^2` was corroborated there by Monte Carlo).
- **Far field.** For the continuum kernel `K` only (on the torus `|x| <= sqrt3 L/2` and `K_L` does not decorrelate),
  at separation `|x| -> infinity` the two sites decouple: `p_(Y_x | U_0)(0, b) -> phi(b) (2 pi)^(-3/2)`,
  `E[w_0 F_j(H_x)] -> z_0 E[F_j(H_b)]` with `H_b = -b I_3 + G_3` (Hessian at a level-`b` critical point of the
  unconditioned field), hence

      Lambda_inf_j(b) = phi(b) (2 pi)^(-3/2) E[|det(-b I_3 + G_3)| 1{index = j}],

  evaluated by the ordered-eigenvalue quadrature (Vandermonde density with `c_3` of [SC] (8)); at `b = 0` the split
  is symmetric under `j <-> 3 - j`. Integrated over the level, `integral Lambda_inf_j(b) db` is the density of
  index-`j` critical points of the unconditioned field, whose classical closed forms in this normalization (unit
  kernel: `Var f = 1`; `Var f_i = 1` per component, i.e. BBKS `sigma_1^2 = E|grad f|^2 = 3`; `Var f_ii = 3`,
  `Cov(f_ii, f_jj) = Var f_ij = 1`, i.e. BBKS `sigma_2^2 = E(Lap f)^2 = 15`; `R_* = sqrt3 sigma_1/sigma_2 = 3/sqrt15`) are `(29 sqrt3 - 18 sqrt2)/(72 pi^2)` for
  maxima and for minima and `(29 sqrt3 + 18 sqrt2)/(72 pi^2)` for each saddle index (maxima/minima: Bardeen–Bond–Kaiser–Szalay
  1986, `n_pk`; index 1 and 2: the same expression with the opposite sign, as in Azaïs–Delmas, arXiv:1911.02300,
  Prop. 3.7, an attribution taken from the Slice A review 5403289484 and not checked here against the source; the
  values themselves are checked numerically); the quadrature reproduces all four to `6e-11` (absolute; check
  tolerance `1e-9`), an exact control of the far-field machinery (the `d = 2`
  analogue in Math-#174 was the Longuet-Higgins total `2/(pi sqrt3)`).
- **Symmetry.** `Lambda` depends on `(x_1, r)`, `r = |x_perp|`, only (rotations about the pin axis leave `U_0`, `v_0`
  and the kernel invariant); the spatial integrals are cylindrical midpoint rules with weight `2 pi r`.

## 2. Method

At each `x = (x_1, r, 0)` the joint Gaussian law of the 21 jets (8 in `U_0`, 3 in `A_0`, 4 in `Y_x`, 6 in `H_x`) is
formed from `Cov(d^alpha f(s), d^beta f(t)) = (-1)^|alpha| d^(alpha+beta) K(t - s)` (products of probabilists'
Hermite polynomials), and `(A_0, H_x)` is conditioned on `(U_0, Y_x) = (v_0, 0, b)`; `p_(Y_x | U_0)(0, b)` is the
conditional Gaussian density. Then

    E[w_0 F_j(H_x) | .] = 36 k^2 integral_(A_0 < 0) (det A_0)^2 p(A_0) E[F_j(H_x) | A_0] dA_0 :

the `A_0` integral is a nested Gauss–Legendre cone quadrature in `(a, c, e) = ((a_11 + a_22)/2, (a_11 - a_22)/2,
a_12)` (cone `a < 0`, `c^2 + e^2 < a^2`; `20 x 16 x 16` nodes; the integrand vanishes to second order on the cone
boundary; against the exact `m_(3,b)` at the decoupled point the rule is accurate to `1e-8`; in the cells nearest the
pin (`r = 0.2` at `h = 0.4`, `r = 0.15` at `h = 0.3`) the conditional `A_0` law is narrow and the rule is `1`–`3 %`
off in the cone mass, which changes the hole by at most about `1e-4` at `h = 0.4`, as measured in the Slice B review
5403404967), and `E[F_j(H_x) | A_0]`, a six-dimensional
Gaussian expectation of `|det H| 1{index}`, is Monte Carlo: `H_x | A_0` is Gaussian with mean affine in `A_0`, the
budget of `4 x 40000` standard normals (four independent seeds) is allocated to the cone nodes in proportion to their
weights (rounded, with a floor of one draw per node; at `40000` draws per batch the floor overshoots the budget by
about `11 %`, and the overshoot, about `2450` nodes carrying `4`–`5 %` of the cone weight, reuses the first draws of
the batch; each node's draws are still standard normal, so the estimator is unbiased, and the batch spread contains
the induced correlation), and the same normals are used at every `x` (common random numbers). The correlation hole

    c_hole_j = integral (Lambda_j(x) - Lambda_j(x_far)) d^3x,   x_far = (10, 0, 0),

is estimated by the difference of the two common-random-number estimates, cell by cell, on the cylinder `|x_1| <= 6`,
`r <= 6` (`h = 0.4`); the standard error is the spread of the four batch means. `Lambda(x_far) = Lambda_inf` to
`1e-16` (every cross-covariance between the two sites is below `2e-17` at `|x| = 10`). The torus integral is then approximated by `L^3 Lambda_inf + c_hole` for `L >= 12` (continuum kernel; not checked
against a periodized integral in `d = 3`; the depletion radius
is about `3`, section 3); no direct periodized integral is computed (at `L = 6` the additive form is not valid, as in
`d = 2`, and no value is given).

## 3. Values (`RESULTS.json`; `k in {1/2, 1, 2}`, `b in {0, 1}`)

Far field: `Lambda_inf(0) = 0.08574653`, `Lambda_inf(1) = 0.06501408` (index split `j = 0..3`: `0.001226, 0.041647, 0.041647, 0.001226` at `b = 0`, `0.000021, 0.006298, 0.047850, 0.010845` at `b = 1`);
`E|det G_3| = 3.3851375013`; level-integrated densities by index `0.0348624089, 0.1065073050, 0.1065073050, 0.0348624089` (closed forms `0.0348624089`, `0.1065073050`).
`m_(3,0) = 0.6715728753`, `m_(3,1) = 5.5480602736`; `z_0 = 36 k^2 m_(3,b)`.

The `integral_X Lambda` and `nu` columns are continuum-kernel approximations of the finite-torus quantities (the
parent's periodized covariance is not used; `RESULTS.json` keys `remote_total.approx_L3_lambda_inf_plus_hole`,
`assembled_nu.approx_nu1_L`, `assembled_nu.approx_nu2_over_nu1_L`); see section 5. The `a_1^(3)`, `nu(1)` and
`nu(2)/nu(1)` columns are moreover conditional on Math-#184's `R_3(b)` (unmerged) and on Math-#168's uncertified GH60
`alpha_j`.

| `k` | `b` | `c_hole = integral (Lambda - Lambda_inf)` (± s.e.) | `integral_X Lambda`, `L = 12` | `L = 24` | `a_1^(3)` | `nu(1)` at `L = 24` | `nu(2)/nu(1)` at `L = 24` |
|---|---|---|---|---|---|---|---|
| `1/2` | `0` | -1.883 ± 0.025 | 146.29 | 1183.48 | 4.71 | 596.4 | 2.45e-04 |
| `1/2` | `1` | -1.231 ± 0.005 | 111.11 | 897.52 | 1.479 | 450.2 | 1.02e-04 |
| `1` | `0` | -3.133 ± 0.029 | 145.04 | 1182.23 | 5.598 | 1187.8 | 9.04e-05 |
| `1` | `1` | -2.309 ± 0.006 | 110.04 | 896.45 | 1.758 | 898.2 | 3.76e-05 |
| `2` | `0` | -4.575 ± 0.035 | 143.59 | 1180.78 | 9.106 | 2370.7 | 3.01e-05 |
| `2` | `1` | -3.473 ± 0.009 | 108.87 | 895.28 | 2.86 | 1793.4 | 1.25e-05 |

Index decomposition of the hole at `k = 1`: `b = 0`: `-0.132 ± 0.006, -2.936 ± 0.017, -0.263 ± 0.023, 0.198 ± 0.006`; `b = 1`: `-0.0008 ± 0.0004, -0.282 ± 0.006, -1.823 ± 0.008, -0.202 ± 0.001`.

The pin depletes a region of radius about `3` (as in `d = 2`): along the axis `Lambda/Lambda_inf` is below `1e-3`
at `|x_1| <= 2` and `0.0329` at `2.5`, `0.62` at `3`, `1.01` at `4`, `1` at `5`; transversally `0.182` at `0.5`, `0.237` at `1`, `0.644` at `2`, `0.998` at `3`, `1` at `4`; along the `45` degree ray `0.00917` at `1`, `0.777` at `2`, `1.07` at `2.5`, `1.03` at `3`, `1` at `4` (values at
`k = 1, b = 0`, `160000` samples per point, Monte Carlo error about `0.2`–`0.7 %` per point). The three profiles are within
Monte Carlo noise of `1` from `|x| = 5` on (on the axis `1.013` at `4`, a residual overshoot of about `1 %`).

**Reading.** `a_j^(3) = R_3(b) alpha_j^(2)` (Math-#184; `R_3(0) = (32 + 28 sqrt2)/17 = 4.2116458674`, `R_3(1) = 4.6201205312`) with
Math-#168's planar `alpha_j` (conditional, as above). On the parent torus sizes the remote singletons dominate
`nu(1)`: `k integral_X Lambda / a_1` is about `15.5`–`76` at `L = 12` and `126`–`626` at `L = 24`
(`L^3 Lambda_inf = 13824 Lambda_inf` at `L = 24`), so the two-point share of a nonempty window
`nu(2)/(nu(1) + nu(2))` is between `1.0e-4` and `1.9e-3` at `L = 12` and between `1.25e-5` and `2.45e-4` at `L = 24`
(largest at `k = 1/2, b = 0`), smaller than in `d = 2` (Math-#174, additive values) by about
`L Lambda_inf^(3) / (R_3(b) Lambda_inf^(2))`, i.e. about `2` at `L = 12` and `4` at `L = 24` (observed `2.04`–`2.25`
and `4.00`–`4.28`).

## 4. Precision (empirical, not bounds)

- Far field: quadrature orders `30`, `40` agree to `1e-12`; the Monte Carlo at the decoupled point `x_far` reproduces
  `z_0 E[|det| 1{j}]` at `b = 0` to within 1.5 % for the saddle indices and 14 % for the extremal indices (at `b = 1`: `1.234, 0.962, 1.003, 1.025`, i.e. 3.8 % for `j = 1` and 23 % for `j = 0`, which carries `3e-4` of the mass; observed ratios, no
  error computed; `1.052, 0.985, 1.001, 1.137` at `b = 0`, indices `j = 0..3`, from `40000` samples, seed `2026`, the
  sample `--check` uses; the maxima/minima indices carry `1.4 %` of the mass and have correspondingly larger errors:
  over the four seed batches `j = 3` is `1.113 ± 0.020` at `b = 0` and `1.027 ± 0.006` at `b = 1`).
- Cone quadrature for the pin weight: `1e-8` relative against the exact `m_(3,b)` at the far point; at the near point
  `(0, 1, 0)` the `16 x 12 x 12` and `20 x 16 x 16` rules differ by `7e-5` relative.
- Monte Carlo: per-point relative error nominally `1.28 / sqrt(160000) = 0.3 %` on `Lambda` (observed four-batch
  spread `0.2`–`0.7 %` on the ray profiles); the hole standard errors are in the table (batch means of four
  independent seeds, 3 degrees of freedom; the grid rows use two seeds, 1 degree of freedom; common random numbers make the far cells contribute almost no
  noise).
- Grid (`k = 1, b = 0`, seeds 2026–2027 only; same-seed `h = 0.4` value `-3.143 ± 0.056`): `h = 0.6`: `-3.155`,
  `h = 0.3`: `-3.138`, `Rc = 5`: `-3.164`. Same-seed differences from `h = 0.4, Rc = 6` (common random numbers):
  `-0.011`, `+0.005`, `-0.021`. The last is systematic (identical in both batches) and is a midpoint-grid alignment
  effect, not the cutoff: the `Rc = 5` run also shifts the `x_1` cell centres by `h/2` (`hr = 5/12`); shifting the
  centres at `Rc = 6` gives `-0.019`, `-0.021` on the same two seeds, while the cells of the `Rc = 6` grid outside the
  `Rc = 5` box contribute `1e-5` (measured here; on nested grids the Slice B review 5403404967 finds the shell
  `5 < |x| <= 6` at most `7e-5` over the six rows and `6 < |x| <= 8` below `1e-6`). Against `h = 0.1`, that review's
  paired runs give a grid error of the tabulated `h = 0.4` hole of about `-0.013` at `k = 1, b = 0` (`O(h^2)`:
  `-0.007` at `h = 0.31`, `-0.003` at `h = 0.2`), systematic and about `0.45` of the reported s.e. These differences
  are measured, not bounds.
- Near-pin points: the conditioning never lost positivity on the grid (`r >= 0.2`); `Lambda` is below `1e-20
  Lambda_inf` on the axis for `|x_1| <= 1.5`.

## 5. What this does not do

Not certified. Continuum kernel only: no periodized (finite-`L`) jets, so the values at `L = 12, 24` are the additive
approximation `L^3 Lambda_inf + c_hole` and no `L = 6` value is given. `d = 3` only; the pin direction is immaterial by
isotropy. The assembled `nu(1)`, `nu(2)` inherit Math-#168's empirical precision on `alpha_j` (at `k = 2` Math-#168 finds GH60 `J_2` 2.6 % (3.2 s.e.) below
MC and does not establish the third digit of `alpha_2(2)`; the `k = 2` `nu(2)/nu(1)` entries inherit this) and are
conditional on
Math-#184's factor `R_3(b)` (unmerged). No rate, no finite-`r` statement. Values of the formulas [RM] (13) and [SC]
(22); not a re-review of either.

## 6. Verification

`python -B -S remote3.py --check` and `-B -O -S`: exact rational contact law (`A_0 | U_0 = -b I + GOE(2, 1)`),
`c_2 = pi`, `m_(3,0) = (7 - 4 sqrt2)/2`, eigenvalue-density normalization, far-field index symmetry at `b = 0`, the
decoupled density `phi(b) (2 pi)^(-3/2)` at `x_far`, the far-point Monte Carlo against `z_0 E|det| 1{j}` within
`10 %` for `j = 0, 1, 2` and within `5 %` for `j = 1, 2` at `b = 0` with the fixed seed `2026` (across seeds the s.d. at
`40000` samples is about `8 %, 1.4 %, 1.3 %` for `j = 0, 1, 2`, so the `j = 0` gate is weak), replay of the far field and of `R_3(b)` against `RESULTS.json`, and replay of
one kernel point per `b` with the stored seeds to `1e-9`. Mutants `hermite-sign`, `det-abs`, `weight-indicator` exit
`1`. The full run regenerates `RESULTS.json` deterministically (seeded) in about an hour.

## 7. Provenance

Pins (`SOURCE_MAP.json`, all on `main`): [RM] `b383bfcc`, [SC] `16c56821`, [CL] `ba492c8e`, [LP] `dfed3b8d`,
[NUM] `2648314f` (Math-#168), [NUM2] `3e4a7ddb` (Math-#174, merged). Unmerged companion: Math-#184 `PROOF.md`
`91d22fce` (Lemma 2 and `R_3(b)`, recomputed here from the displayed formulas).

Revision (Slice A review 5403289484, Slice B review 5403404967 and Slice C review 5974291103 on Math-#192; wording, one regeneration fix, one
added check gate): `full_run` writes the far-point controls from the first batch (the sample `--check` uses), so the
stored `controls` block regenerates; the far-point ratios are stated as observed values with their sample; the
BBKS normalization, attribution and `6e-11` control precision are stated exactly; the continuum-kernel scope is
stated in section 1; the Reading paragraph is corrected (the `d = 2` / `d = 3` share factor carries `R_3(b)`); the
conditional status of the assembled columns, the grid rows' same-seed differences (the `Rc = 5` effect is grid
alignment, per the Slice B review 5403404967, re-measured here), the cone-rule accuracy near the pin, the node
allocation of the Monte Carlo budget and the ray-profile precision are stated; `--check` gains a `5 %` gate for `j = 1, 2`. The readback 5974705557 restricted the far-point ratio sentence to
`b = 0` and added the `b = 1` ratios. `RESULTS.json` unchanged.
