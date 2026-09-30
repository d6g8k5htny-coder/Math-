# Numerical values of the remote singleton coefficient `k integral_X Lambda` (planar, parent kernel)

**Object:** `CL-C6-REMOTE-COEFF-NUMERICS-20260930-v1`. **Author lane:** Anthropic / Claude. **Kind:** numerical
note. **Scientific effect:** NONE. **Certified:** no (floating-point quadrature with convergence checks; not an
enclosure). Companion of the near-coefficient note `frontiers/c6_cluster_coefficients_numerics_20260930`
(Math-#168), which evaluated `nu_near(1) = alpha_1` and `nu(2) = alpha_2` and listed the remote part of `nu(1)` as
not evaluated. This note evaluates that part.

## 1. What is evaluated

[CL] (1.4) writes the one-point cluster coefficient as

    nu(1) = nu_near(1) + k integral_X Lambda(x; b, k, u) dx,        Lambda = sum_j Lambda_j,

with `Lambda_j` the contact kernel of [RM] (13):

    Lambda_j(x) = p_(Y_x | U_0 = v_0)(0, b) / z_0 . E[ w_0 F_j(H_x) | U_0 = v_0, Y_x = (0, b) ],

`U_0 = (f, f_x, f_z, f_xx, f_xz, f_xxx)(0) = (b, 0, 0, 0, 0, 12k)` the contact observation, `A_0 = f_zz(0)` the soft
curvature, `w_0 = (6k)^2 A_0^2 1{A_0 < 0}` ([RM] (10) at `d = 2`), `z_0 = E[w_0 | U_0 = v_0] = 36 k^2 m_(2,b)`
([RM] (11), [LP] (5.4)) with `m_(2,b) = E[A_0^2 1{A_0 < 0} | U_0]` taken under the same kernel as the numerator
(continuum: `A_0 | U_0 ~ N(-b, 2)` exactly; `L = 6`: the periodized conditional law, `m_(2,0) = 1.0000175`), `Y_x = (f_x, f_z, f)(x)`, `H_x` the Hessian at `x`, `F_j(H) = |det H| 1{index H = j}`. The
field is the centered unit-variance Gaussian field on `X = R^2/(L Z^2)` with the exact kernel of [LP] section 2,
`K_L(z) = sum_n exp(-|z + Ln|^2/2) / sum_n exp(-|Ln|^2/2)`. Orientation: the continuum kernel is isotropic, so
continuum quantities (`Lambda_inf`, `c_hole`, sample kernels, profiles) hold for every pin direction `u`; the
square torus is not rotation-invariant, and every `L`-periodized value in this note is computed with the pin
direction `u = e_1` aligned with a lattice axis (the image lattice is written in pin-frame coordinates). No other
orientation is computed. Everything is a finite-dimensional Gaussian computation: the 13-vector of jets (seven at `0`, six at `x`) has covariance
`Cov(d^alpha f(s), d^beta f(t)) = (-1)^|alpha| (d^(alpha+beta) K_L)(t - s)`, with
`d^a_x d^c_z exp(-|z|^2/2) = (-1)^(a+c) He_a(x_1) He_c(z) exp(-|z|^2/2)` (probabilists' Hermite polynomials).

[CL] section 5.1 shows `k integral_X Lambda = lim_(rho -> 0) k integral_(D_rho) Lambda` exists, with
`k integral_(|x| < rho) Lambda <= C rho^2`; so `Lambda` is integrable at the pin and the torus integral of the
kernel is the right object. A direct scaling check is consistent with this: at a critical point `x` of the contact
field at level `b` with `|x| = eps` small, the Euler identity `x . grad f = 3 C + A_0 z^2 + 4 q + ...` for the cubic
part `C`, the soft quadratic `A_0 z^2 / 2` and the quartic part `q` forces `A_0 z^2 = O(eps^4)`, i.e. `A_0 = O(eps^2)`;
the density of `Y_x` at `(0, b)` is `O(eps^(-6))` while `w_0 |det H_x| = O(eps^4 . eps^2)`, so `Lambda = O(1)` as
`x -> 0`. (A first guess `A_0 = O(eps)` would give `Lambda ~ eps^(-2)` and a logarithmically divergent integral;
it is wrong exactly because of the Euler identity.) The computed values confirm boundedness and, in fact,
`Lambda(x) -> 0` as `x -> 0` (section 4).

## 2. Exact structure

**Far field.** As `|x| -> infinity` the two sites decouple: `p_(Y_x | U_0)(0, b) -> phi(b)/(2 pi)` (`f`, `f_x`,
`f_z` independent with unit variance), `E[w_0 | U_0] / z_0 -> 1`, and `H_x | (f = b, grad f = 0)` has `h_1 = f_xx`,
`h_3 = f_zz ~ N(-b, 2)` independent (`Var f_xx = 3`, `Cov(f_xx, f_zz) = 1`, `Cov(f, f_xx) = -1`, regression on
`f = b` removes the common part), `h_2 = f_xz ~ N(0, 1)`. Hence

    Lambda_inf,j(b) = phi(b)/(2 pi) . E[ F_j(H) | f = b, grad f = 0 ],

the ordinary height-resolved density of index-`j` critical points at level `b`, per unit height and area. It is
`k`-free; the `k`-dependence of `Lambda(x)` enters only through the conditioning on `f_xxx(0) = 12k` and dies with
the correlations. It is also closed-form: with `h_1 = a + c`, `h_3 = a - c` (`a ~ N(-b, 1)`, `c ~ N(0, 1)`, `h_2 ~
N(0, 1)` independent) `det H = a^2 - rho^2`, `rho^2 ~ Exp(mean 2)`, and

    E F_1 = sqrt2 e^(-b^2/4),
    E F_2 = (b^2+1) Phi(b) + b phi(b) - 2 Phi(b) + sqrt2 e^(-b^2/4) Phi(b/sqrt2),   E F_0 = E F_2 |_(b -> -b),
    E|det H_b| = b^2 - 1 + 2 sqrt2 e^(-b^2/4),        Lambda_inf(b) = phi(b) E|det H_b| / (2 pi),

so `Lambda_inf(0) = (2 sqrt2 - 1)/(2 pi)^(3/2) = 0.1160934862...`, and `integral Lambda_inf(b) db = 2/(pi sqrt3)`, the
total critical-point density. The quadrature reproduces these closed forms to `9e-13` (absolute), a
second exact end-to-end control of the Hessian integrator with a non-centered mean.

**Exact control of the Hessian integrator.** For the unconditional planar Hessian (`Var h_1 = Var h_3 = 3`,
`Cov(h_1, h_3) = 1`, `Var h_2 = 1`) write `h_1 = a + c`, `h_3 = a - c` with `a ~ N(0, 2)`, `c ~ N(0, 1)` independent;
then `det H = a^2 - (c^2 + h_2^2) = a^2 - rho^2` with `rho^2 ~ Exp(mean 2)`, so
`E|det H| = 2 E[(rho^2 - a^2)_+] = 4 E exp(-a^2/2) = 4/sqrt3`, `E F_1 = 2/sqrt3`, `E F_0 = E F_2 = 1/sqrt3`,
`E det H = 0`. (Total critical-point density `2/(pi sqrt3) = 0.3676`, maxima `1/(2 pi sqrt3) = 0.0919`: the
Longuet-Higgins values for this spectrum.) The integrator reproduces these to `9.7e-11` (absolute).

**Coordinates adapted to the cone `det H = 0`.** The integrals `E[A_0^2 1{A_0 < 0} |det H| 1{index j}]` over the
conditional Gaussian law of `(A_0, H_x)` are computed with `A_0` integrated out in closed form
(`E[A^2 1{A < 0}] = (m^2 + s^2) Phi(-m/s) - m s phi(m/s)` for `A | H ~ N(m, s^2)`, `m` affine in `H`) and the
three Hessian coordinates written as `a = tr H / 2` and polar `(rho, theta)` in the traceless plane `(c, h_2)`.
Then `det H = a^2 - rho^2`, the kink of `|det H|` is the coordinate surface `rho = |a|`, and the index is read off
from `rho < |a|` (definite; sign of `a` separates minimum and maximum) or `rho > |a|` (saddle). The `a`-range is
split at `0`, the `rho`-range at `|a|`, the `theta` nodes are those of the periodic trapezoid rule under an
analytic map concentrating them at the angular position of the (generally offset and anisotropic) conditional
mean; every piece of the integrand is smooth, and the nested rule converges geometrically on the exact control
(`1.8e-14 relative on Lambda_inf(0) between orders` at the higher order).

**Ill-conditioned points.** Near the pin the conditional law of `Y_x` given `U_0` has variances down to `|x|^6`,
and the double-precision regression can lose positivity, either in the Hessian block (near the axis, where
`Lambda` is below `10^(-20)`) or in the Schur complement `Var(A_0 | H_x)` (near the pin in the transverse sector,
where `Lambda` is small but not negligible: at `r = 0.05` transverse a clamped `Var(A_0 | H_x)` would misreport
`Lambda` by a factor ten). The full `4 x 4` conditional covariance of `(A_0, H_x)` is therefore Cholesky-factored,
and any nonpositive pivot sends the point (`{{exact_count}}` in the whole run) to a 50-digit decimal regression.

## 3. Method

`Lambda_j(x)` is evaluated on midpoint grids (spacing `h`, reflection symmetry `z -> -z` used) and integrated by
the midpoint rule:

- continuum kernel, hole constant `c_hole,j = integral_(R^2) (Lambda_j - Lambda_inf,j) dx` on `[-6, 6]^2`
  (`h = 0.15`). The sixth-order jet correlations decay only like `He_6(|x|) e^(-|x|^2/2)` (`0.32` at distance 4,
  `4.4e-4` at 6), so the cutoff is checked directly: `Lambda/Lambda_inf - 1` is `3.6e-5` (axis), `3.1e-6` (45 deg),
  `4.4e-7` (transverse) at `|x| = 5`, and `4.8e-9`, `4.4e-10`, `3.8e-11` at `|x| = 6`; the neglected exterior
  contributes less than `10^(-7)` to `c_hole`;
- periodized kernel at `L = 6`, direct integral over the fundamental domain `[-3, 3]^2` (`h = 0.15`);
- periodized kernel at `L = 12`, direct integral (`h = 0.2`), compared with `L^2 Lambda_inf + c_hole`.

Then `integral_X Lambda ~ L^2 Lambda_inf + c_hole` for `L = 12, 24` (the periodization correction being
`O(e^(-18))` at `L >= 12`), and the remote singleton mass is `k` times that.

## 4. Values

**Far field** (`k`-free), per unit height and area:

| `b` | `Lambda_inf` | minima `j = 0` | saddles `j = 1` | maxima `j = 2` | `p_inf = phi(b)/(2 pi)` |
|---|---|---|---|---|---|
| `0.0` | 0.116093 | 0.01315 | 0.0897936 | 0.01315 | 0.0634936 |
| `1.0` | 0.0848309 | 0.000850618 | 0.0424155 | 0.0415649 | 0.0385108 |

(At `b = 0`: `E|det H_0| = 1.82843` with `h_1, h_3 ~ N(0, 2)`, `h_2 ~ N(0, 1)`.)

**Correlation hole** `c_hole = integral_(R^2) (Lambda - Lambda_inf) dx` (dimension of an area times a density
per height; negative means depletion):

| `k` | `b` | `c_hole` | `j = 0` | `j = 1` | `j = 2` | `c_hole / Lambda_inf` (effective depleted area) |
|---|---|---|---|---|---|---|
| `0.5` | `0.0` | -1.08414 | -0.302824 | -0.88442 | 0.103108 | -9.338 |
| `1.0` | `0.0` | -1.63115 | -0.313786 | -1.3325 | 0.0151367 | -14.05 |
| `2.0` | `0.0` | -2.1382 | -0.330282 | -1.75684 | -0.0510768 | -18.42 |
| `0.5` | `1.0` | -0.750629 | -0.00830817 | -0.260797 | -0.481524 | -8.849 |
| `1.0` | `1.0` | -1.18448 | -0.0055866 | -0.464948 | -0.713947 | -13.96 |
| `2.0` | `1.0` | -1.56814 | -0.00268732 | -0.636506 | -0.928945 | -18.49 |

The pinned pair depletes its neighbourhood: along the pin axis the contact field is `b + 2k x_1^3 + ...` to leading
order, a monotone ramp, so window-level critical points near the pins live in the transverse sector only
(`Lambda(x)/Lambda_inf` at `k = 1, b = 0`: on the axis `2e-22` at `|x_1| = 1.5`, `1.6e-6` at `2`, `0.037` at
`2.5`, `0.68` at `3`, `1.02` at `4`; transversally `0.21` at `|z| = 1`, `0.68` at `2`, `1.00` at `3`; the ray
profiles at angles `0, 30, 45, 60, 90` degrees are in `RESULTS.json`, `ray_profile`). Near the pin `Lambda -> 0`
(`near_zero_profile`: `Lambda(0.05, 60 deg) = 0.001`, `Lambda(0.4, 90 deg) = 0.0079` at `k = 1, b = 0`; on the
axis and at `30` degrees it is below `10^(-20)`).

**Remote singleton mass** `R(k, b, L) = k integral_X Lambda dx` and the assembled `nu(1)`, with `alpha_1` from the
companion note ([NUM] = Math-#168 `RESULTS.json`, merged, pinned; GH60 values; `alpha_2` likewise):

| `k` | `b` | `L` | `integral_X Lambda` | `R = k integral_X Lambda` | `alpha_1` (#168) | `nu(1) = alpha_1 + R` | `nu(2) = alpha_2` | `nu(2)/nu(1)` |
|---|---|---|---|---|---|---|---|---|
| `0.5` | `0.0` | `6` (direct) | 3.05738 | 1.52869 | 1.11821 | 2.6469 | 0.0347454 | 0.0131 |
| `0.5` | `0.0` | `12` | 15.6333 | 7.81666 | 1.11821 | 8.93487 | 0.0347454 | 0.00389 |
| `0.5` | `0.0` | `24` | 65.7857 | 32.8929 | 1.11821 | 34.0111 | 0.0347454 | 0.00102 |
| `1.0` | `0.0` | `6` (direct) | 2.54211 | 2.54211 | 1.32906 | 3.87117 | 0.0255091 | 0.00659 |
| `1.0` | `0.0` | `12` | 15.0863 | 15.0863 | 1.32906 | 16.4154 | 0.0255091 | 0.00155 |
| `1.0` | `0.0` | `24` | 65.2387 | 65.2387 | 1.32906 | 66.5678 | 0.0255091 | 0.000383 |
| `2.0` | `0.0` | `6` (direct) | 2.17976 | 4.35953 | 2.1621 | 6.52163 | 0.0169281 | 0.0026 |
| `2.0` | `0.0` | `12` | 14.5793 | 29.1585 | 2.1621 | 31.3206 | 0.0169281 | 0.00054 |
| `2.0` | `0.0` | `24` | 64.7316 | 129.463 | 2.1621 | 131.625 | 0.0169281 | 0.000129 |
| `0.5` | `1.0` | `6` (direct) | 2.237 | 1.1185 | 0.320155 | 1.43866 | 0.00994791 | 0.00691 |
| `0.5` | `1.0` | `12` | 11.465 | 5.73251 | 0.320155 | 6.05267 | 0.00994791 | 0.00164 |
| `0.5` | `1.0` | `24` | 48.112 | 24.056 | 0.320155 | 24.3762 | 0.00994791 | 0.000408 |
| `1.0` | `1.0` | `6` (direct) | 1.81212 | 1.81212 | 0.380523 | 2.19264 | 0.00730347 | 0.00333 |
| `1.0` | `1.0` | `12` | 11.0312 | 11.0312 | 0.380523 | 11.4117 | 0.00730347 | 0.00064 |
| `1.0` | `1.0` | `24` | 47.6781 | 47.6781 | 0.380523 | 48.0587 | 0.00730347 | 0.000152 |
| `2.0` | `1.0` | `6` (direct) | 1.5302 | 3.0604 | 0.619027 | 3.67943 | 0.00484668 | 0.00132 |
| `2.0` | `1.0` | `12` | 10.6475 | 21.295 | 0.619027 | 21.9141 | 0.00484668 | 0.000221 |
| `2.0` | `1.0` | `24` | 47.2945 | 94.589 | 0.619027 | 95.208 | 0.00484668 | 5.09e-05 |

For `L = 6` the direct periodized integral and the approximation `36 Lambda_inf + c_hole` are both given
(`RESULTS.json`, `remote_total`); they differ by between `2.4e-3` and `6.4e-2` relative, most at `k = 2`. At
`L = 6` the depleted region (radius about `3`) fills the fundamental domain, so the depletions around the image
pins overlap and the additive approximation `L^2 Lambda_inf + c_hole` is not valid; the table uses the direct
periodized integral for `L = 6`. (The periodization also changes the one-site covariances by up to `8.8e-4` at
`L = 6`; that is included in the direct value.) For `L = 12` the direct integral at `k = 1, b = 0` is `15.0866`
against `15.0863` from the far field plus hole, so the additive form is accurate to `2e-5` there and better at
`L = 24`.

**Reading.** For the parent torus sizes the remote singletons dominate `nu(1)` (`R ~ L^2 Lambda_inf`: by a factor
`50` at `L = 24`, `k = 1, b = 0`), so the two-point cluster probability relative to a nonempty window is
`nu(2)/(nu(1) + nu(2)) ~ 3.83e-04` at `k = 1, b = 0, L = 24`, against the near-only share `0.019` reported in
#168. The near share is the right object for the cluster geometry; the global share is the right object for the
finite-torus count. The pins do not only deplete: along the `45`-`60` degree rays `Lambda/Lambda_inf` overshoots to
`1.24`-`1.48` at `|x| = 2`-`2.5` (`k = 1, b = 0`) before settling, so the displaced critical points pile up in a
ring; the net hole is nevertheless negative for every `(k, b)` computed, and grows with `k` (steeper ramp
`2k x_1^3`, stronger `f_xxx` conditioning) and shrinks with `b`.

## 5. Precision (empirical, not bounds)

- Quadrature: at the sample points the default orders `(24, 32, 24)` differ from `(32, 48, 32)` by at most `3e-9`
  relative wherever `Lambda > 10^(-2) Lambda_inf`, by `5e-4` at `(0.15, 0.15)` where `Lambda = 2e-5 Lambda_inf`, and
  by up to `4.0e-01` at points where `Lambda < 10^(-16) Lambda_inf` (the recorded maximum, carried entirely by such
  points: the conditional law of `H_x` is extremely anisotropic there and the value is exponentially small anyway).
  On the exact controls the default order is accurate to `9.7e-11` (unconditional Hessian) and
  `9e-13` (far field, both `b`). The `h = 0.3` hole constant changes by `4e-08` between the
  two orders.
- Grid: at `k = 1, b = 0` the hole constant is `-1.629661` (`h = 0.3`), `-1.631148` (`h = 0.15`),
  `-1.631335` (`h = 0.1`): the midpoint rule converges at an observed order of about `2.7` (`Lambda` has a
  conical, direction-dependent limit at the pin), the `h = 0.15` values are within `2e-4` of the `h = 0.1` values,
  and a power-law extrapolation puts the remaining error of the tabulated (`h = 0.15`) hole constants near
  `1e-4` absolute (`1e-4` relative). The `h = 0.3` run on `[-5, 5]^2` differs by `2.1e-03`, which is grid
  placement, not tail (see the direct tail check in section 3).
- The periodized `L = 12` direct integral (`h = 0.2`) agrees with far field plus hole to `2.0e-05` relative.
- The Monte Carlo cross-check of the unconditional control (`2 . 10^5` samples, seed 2026) gives
  `E|det H| = 2.3032 +- 0.0058`, `4/sqrt3 = 2.3094` lying at `1.1` standard errors.

These are observed discrepancies. No error bound is claimed.

## 6. What the numbers are not

Not a proof and not an enclosure. They are values of the formula [RM] (13) integrated as [CL] (1.4) prescribes;
[RM] is an accepted source, [CL] nonauthor-accepted and merged; the numbers do not re-review either. Planar only
(`d = 2`); no rate, no finite-`r` statement; the assembled `nu(1)` inherits the empirical precision of #168's
`alpha_1` (about `0.3%` or better). No register, catalog or STATUS change. Same GitHub account as every lane; zero
organizational-independence credit. The author will not merge.

## 7. Provenance

`remote.py` (standard library; `--check` replays the exact controls, the far field, sixteen sample kernels at two
parameter pairs for the continuum and the `L = 6` kernel, one decimal-regression point and the near-zero profile
against `RESULTS.json`; three mutants `hermite-sign`, `det-abs`, `weight-indicator` must exit 1), `RESULTS.json`
(full run, about 36 minutes), `SOURCE_MAP.json` (pins [LP], [RM], [CL], [RC] on `main`
`7d0c89a`), `SOURCE_FILES.json`, workflow `c6-remote-coefficient-numerics.yml`.
