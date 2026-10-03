# Numerical values of the remote singleton coefficient k ∫_X Λ of ν(1) in dimension d = 3 (parent kernel; not certified)

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
this in `d = 2`; this note does `d = 3` for the continuum kernel `K(x) = exp(-|x|^2/2)`.

Exact structure used (all checked in `remote3.py --check`):

- **Contact law at the pin.** Given `U_0 = v_0`, `A_0 = -b I_2 + G_2` with `G_2` the GOE matrix of diagonal variance
  `2` and off-diagonal variance `1` (exact rational regression; Math-#184 Lemma 1), so that
  `z_0 = 36 k^2 m_(3,b)`, `m_(3,b) = E[(det A_0)^2 1{A_0 < 0}]`, `m_(3,0) = (7 - 4 sqrt2)/2` (Math-#184 Lemma 2,
  companion, conditional; the finite-`r` normalizer `Z_r / r^2` was corroborated there by Monte Carlo).
- **Far field.** At separation `|x| -> infinity` the two sites decouple: `p_(Y_x | U_0)(0, b) -> phi(b) (2 pi)^(-3/2)`,
  `E[w_0 F_j(H_x)] -> z_0 E[F_j(H_b)]` with `H_b = -b I_3 + G_3` (Hessian at a level-`b` critical point of the
  unconditioned field), hence

      Lambda_inf_j(b) = phi(b) (2 pi)^(-3/2) E[|det(-b I_3 + G_3)| 1{index = j}],

  evaluated by the ordered-eigenvalue quadrature (Vandermonde density with `c_3` of [SC] (8)); at `b = 0` the split
  is symmetric under `j <-> 3 - j`. Integrated over the level, `integral Lambda_inf_j(b) db` is the density of
  index-`j` critical points of the unconditioned field, whose classical closed forms in this normalization (unit
  kernel: `sigma_0 = 1`, per-component `sigma_1 = 1`, `sigma_2^2 = 15`) are `(29 sqrt3 - 18 sqrt2)/(72 pi^2)` for
  maxima and for minima and `(29 sqrt3 + 18 sqrt2)/(72 pi^2)` for each saddle index (Bardeen–Bond–Kaiser–Szalay
  1986); the quadrature reproduces all four to `1e-12`, an exact control of the far-field machinery (the `d = 2`
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
boundary, and against the exact `m_(3,b)` the rule is accurate to `1e-8`), and `E[F_j(H_x) | A_0]`, a six-dimensional
Gaussian expectation of `|det H| 1{index}`, is Monte Carlo: `H_x | A_0` is Gaussian with mean affine in `A_0`, the
budget of `4 x 40000` standard normals (four independent seeds) is allocated to the cone nodes in proportion to their
weights, and the same normals are used at every `x` (common random numbers). The correlation hole

    c_hole_j = integral (Lambda_j(x) - Lambda_j(x_far)) d^3x,   x_far = (10, 0, 0),

is estimated by the difference of the two common-random-number estimates, cell by cell, on the cylinder `|x_1| <= 6`,
`r <= 6` (`h = 0.4`); the standard error is the spread of the four batch means. `Lambda(x_far) = Lambda_inf` to
`1e-16`. The torus integral is then `integral_X Lambda = L^3 Lambda_inf + c_hole` for `L >= 12` (the depletion radius
is about `3`, section 3); no direct periodized integral is computed (at `L = 6` the additive form is not valid, as in
`d = 2`, and no value is given).

## 3. Values (`RESULTS.json`; `k in {1/2, 1, 2}`, `b in {0, 1}`)

Far field: `Lambda_inf(0) = 0.08574653`, `Lambda_inf(1) = 0.06501408` (index split `j = 0..3`: `0.001226, 0.041647, 0.041647, 0.001226` at `b = 0`, `0.000021, 0.006298, 0.047850, 0.010845` at `b = 1`);
`E|det G_3| = 3.3851375013`; level-integrated densities by index `0.0348624089, 0.1065073050, 0.1065073050, 0.0348624089` (closed forms `0.0348624089`, `0.1065073050`).
`m_(3,0) = 0.6715728753`, `m_(3,1) = 5.5480602736`; `z_0 = 36 k^2 m_(3,b)`.

The `integral_X Lambda` and `nu` columns are continuum-kernel approximations of the finite-torus quantities (the
parent's periodized covariance is not used; `RESULTS.json` keys `remote_total.approx_L3_lambda_inf_plus_hole`,
`assembled_nu.approx_nu1_L`, `assembled_nu.approx_nu2_over_nu1_L`); see section 5.

| `k` | `b` | `c_hole = integral (Lambda - Lambda_inf)` (± s.e.) | `integral_X Lambda`, `L = 12` | `L = 24` | `a_1^(3)` | `nu(1)` at `L = 24` | `nu(2)/nu(1)` at `L = 24` |
|---|---|---|---|---|---|---|---|
| `1/2` | `0` | -1.883 ± 0.025 | 146.29 | 1183.48 | 4.71 | 596.4 | 2.45e-04 |
| `1/2` | `1` | -1.231 ± 0.005 | 111.11 | 897.52 | 1.479 | 450.2 | 1.02e-04 |
| `1` | `0` | -3.133 ± 0.029 | 145.04 | 1182.23 | 5.598 | 1187.8 | 9.04e-05 |
| `1` | `1` | -2.309 ± 0.006 | 110.04 | 896.45 | 1.758 | 898.2 | 3.76e-05 |
| `2` | `0` | -4.575 ± 0.035 | 143.59 | 1180.78 | 9.106 | 2370.7 | 3.01e-05 |
| `2` | `1` | -3.473 ± 0.009 | 108.87 | 895.28 | 2.86 | 1793.4 | 1.25e-05 |

Index decomposition of the hole at `k = 1`: `b = 0`: `-0.132 ± 0.006, -2.936 ± 0.017, -0.263 ± 0.023, 0.198 ± 0.006`; `b = 1`: `-0.001 ± 0.000, -0.282 ± 0.006, -1.823 ± 0.008, -0.202 ± 0.001`.

The pin depletes a region of radius about `3` (as in `d = 2`): along the axis `Lambda/Lambda_inf` is below `1e-3`
at `|x_1| <= 2` and `0.0329` at `2.5`, `0.62` at `3`, `1.01` at `4`, `1` at `5`; transversally `0.182` at `0.5`, `0.237` at `1`, `0.644` at `2`, `0.998` at `3`, `1` at `4`; along the `45` degree ray `0.00917` at `1`, `0.777` at `2`, `1.07` at `2.5`, `1.03` at `3`, `1` at `4` (values at
`k = 1, b = 0`, `160000` samples per point, Monte Carlo error about `0.7 %` per point). The three profiles are within
Monte Carlo noise of `1` from `|x| = 4` on.

**Reading.** `a_j^(3) = R_3(b) alpha_j^(2)` (Math-#184; `R_3(0) = (32 + 28 sqrt2)/17 = 4.2116458674`, `R_3(1) = 4.6201205312`) with
Math-#168's planar `alpha_j`. On the parent torus sizes the remote singletons dominate `nu(1)` by a factor of order
`10^2`–`10^3` (`L^3 Lambda_inf = 13824 Lambda_inf` at `L = 24`), so the two-point share of a nonempty window is
`nu(2)/(nu(1) + nu(2))` of order `1e-4` at `L = 12` and `1e-5` at `L = 24`, smaller than in `d = 2` (Math-#174) by
the factor `L Lambda_inf^(3) / Lambda_inf^(2)` up to the near terms.

## 4. Precision (empirical, not bounds)

- Far field: quadrature orders `30`, `40` agree to `1e-12`; the Monte Carlo at the decoupled point `x_far` reproduces
  `z_0 E[|det| 1{j}]` within its statistical error (`1.052, 0.985, 1.001, 1.137` at `b = 0`, indices `j = 0..3`; the maxima/minima indices
  carry `1.4 %` of the mass and have correspondingly larger errors).
- Cone quadrature for the pin weight: `1e-8` relative against the exact `m_(3,b)` at the far point; at the near point
  `(0, 1, 0)` the `16 x 12 x 12` and `20 x 16 x 16` rules differ by `7e-5` relative.
- Monte Carlo: per-point relative error about `1.28 / sqrt(160000) = 0.3 %` on `Lambda`; the hole standard errors are
  in the table (batch means of four independent seeds; common random numbers make the far cells contribute almost no
  noise).
- Grid (`k = 1, b = 0`, two batches): hole `-3.155 ± 0.055` (`h = 0.6`), `-3.133 ± 0.029` (`h = 0.4`, tabulated), `-3.138 ± 0.057` (`h = 0.3`);
  cutoff `Rc = 5` instead of `6`: `-3.164 ± 0.056`. These differences are measured, not bounds; the grid error of the
  tabulated values is of the order of the difference between `h = 0.4` and `h = 0.3`.
- Near-pin points: the conditioning never lost positivity on the grid (`r >= 0.2`); `Lambda` is below `1e-20
  Lambda_inf` on the axis for `|x_1| <= 1.5`.

## 5. What this does not do

Not certified. Continuum kernel only: no periodized (finite-`L`) jets, so the values at `L = 12, 24` are the additive
approximation `L^3 Lambda_inf + c_hole` and no `L = 6` value is given. `d = 3` only; the pin direction is immaterial by
isotropy. The assembled `nu(1)`, `nu(2)` inherit Math-#168's empirical precision on `alpha_j` and are conditional on
Math-#184's factor `R_3(b)` (unmerged). No rate, no finite-`r` statement. Values of the formulas [RM] (13) and [SC]
(22); not a re-review of either.

## 6. Verification

`python -B -S remote3.py --check` and `-B -O -S`: exact rational contact law (`A_0 | U_0 = -b I + GOE(2, 1)`),
`c_2 = pi`, `m_(3,0) = (7 - 4 sqrt2)/2`, eigenvalue-density normalization, far-field index symmetry at `b = 0`, the
decoupled density `phi(b) (2 pi)^(-3/2)` at `x_far`, the far-point Monte Carlo against `z_0 E|det| 1{j}` within
`10 %` for the three largest indices, replay of the far field and of `R_3(b)` against `RESULTS.json`, and replay of
one kernel point per `b` with the stored seeds to `1e-9`. Mutants `hermite-sign`, `det-abs`, `weight-indicator` exit
`1`. The full run regenerates `RESULTS.json` deterministically (seeded) in about an hour.

## 7. Provenance

Pins (`SOURCE_MAP.json`, all on `main`): [RM] `b383bfcc`, [SC] `16c56821`, [CL] `ba492c8e`, [LP] `dfed3b8d`,
[NUM] `2648314f` (Math-#168), [NUM2] `3e4a7ddb` (Math-#174, merged). Unmerged companion: Math-#184 `PROOF.md`
`91d22fce` (Lemma 2 and `R_3(b)`, recomputed here from the displayed formulas).
