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
([RM] (11), [LP] (5.4)), `Y_x = (f_x, f_z, f)(x)`, `H_x` the Hessian at `x`, `F_j(H) = |det H| 1{index H = j}`. The
field is the centered unit-variance Gaussian field on `X = R^2/(L Z^2)` with the exact kernel of [LP] section 2,
`K_L(z) = sum_n exp(-|z + Ln|^2/2) / sum_n exp(-|Ln|^2/2)`. Everything is a finite-dimensional Gaussian
computation: the 13-vector of jets (seven at `0`, six at `x`) has covariance
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
the correlations.

**Exact control of the Hessian integrator.** For the unconditional planar Hessian (`Var h_1 = Var h_3 = 3`,
`Cov(h_1, h_3) = 1`, `Var h_2 = 1`) write `h_1 = a + c`, `h_3 = a - c` with `a ~ N(0, 2)`, `c ~ N(0, 1)` independent;
then `det H = a^2 - (c^2 + h_2^2) = a^2 - rho^2` with `rho^2 ~ Exp(mean 2)`, so
`E|det H| = 2 E[(rho^2 - a^2)_+] = 4 E exp(-a^2/2) = 4/sqrt3`, `E F_1 = 2/sqrt3`, `E F_0 = E F_2 = 1/sqrt3`,
`E det H = 0`. (Total critical-point density `2/(pi sqrt3) = 0.3676`, maxima `1/(2 pi sqrt3) = 0.0919`: the
Longuet-Higgins values for this spectrum.) The integrator reproduces these to `{{absdet_err}}` (absolute).

**Coordinates adapted to the cone `det H = 0`.** The integrals `E[A_0^2 1{A_0 < 0} |det H| 1{index j}]` over the
conditional Gaussian law of `(A_0, H_x)` are computed with `A_0` integrated out in closed form
(`E[A^2 1{A < 0}] = (m^2 + s^2) Phi(-m/s) - m s phi(m/s)` for `A | H ~ N(m, s^2)`, `m` affine in `H`) and the
three Hessian coordinates written as `a = tr H / 2` and polar `(rho, theta)` in the traceless plane `(c, h_2)`.
Then `det H = a^2 - rho^2`, the kink of `|det H|` is the coordinate surface `rho = |a|`, and the index is read off
from `rho < |a|` (definite; sign of `a` separates minimum and maximum) or `rho > |a|` (saddle). The `a`-range is
split at `0`, the `rho`-range at `|a|`, the `theta` nodes are those of the periodic trapezoid rule under an
analytic map concentrating them at the angular position of the (generally offset and anisotropic) conditional
mean; every piece of the integrand is smooth, and the nested rule converges geometrically on the exact control
(`{{absdet_err_hi}}` at the higher order).

**Ill-conditioned points.** Near the pin axis the conditional law of `Y_x` given `U_0` has variances down to
`|x|^6`, and the double-precision regression can lose positivity where `Lambda` is already below `10^(-20)`. Such
points (`{{exact_count}}` in the whole run) are recomputed in 50-digit decimal arithmetic; none carries weight.

## 3. Method

`Lambda_j(x)` is evaluated on midpoint grids (spacing `h`, reflection symmetry `z -> -z` used) and integrated by
the midpoint rule:

- continuum kernel, hole constant `c_hole,j = integral_(R^2) (Lambda_j - Lambda_inf,j) dx` on `[-6, 6]^2`
  (`h = 0.15`; the neglected exterior has `|Lambda - Lambda_inf| < 10^(-6) Lambda_inf`, correlations at distance 6
  being of size `K(6) = e^(-18)`);
- periodized kernel at `L = 6`, direct integral over the fundamental domain `[-3, 3]^2` (`h = 0.15`);
- periodized kernel at `L = 12`, direct integral (`h = 0.2`), compared with `L^2 Lambda_inf + c_hole`.

Then `integral_X Lambda ~ L^2 Lambda_inf + c_hole` for `L = 12, 24` (the periodization correction being
`O(e^(-18))` at `L >= 12`), and the remote singleton mass is `k` times that.

## 4. Values

**Far field** (`k`-free), per unit height and area:

| `b` | `Lambda_inf` | minima `j = 0` | saddles `j = 1` | maxima `j = 2` | `p_inf = phi(b)/(2 pi)` |
|---|---|---|---|---|---|
{{far_rows}}

(At `b = 0`: `E|det H_0| = {{EdetH0}}` with `h_1, h_3 ~ N(0, 2)`, `h_2 ~ N(0, 1)`.)

**Correlation hole** `c_hole = integral_(R^2) (Lambda - Lambda_inf) dx` (dimension of an area times a density
per height; negative means depletion):

| `k` | `b` | `c_hole` | `j = 0` | `j = 1` | `j = 2` | `c_hole / Lambda_inf` (effective depleted area) |
|---|---|---|---|---|---|---|
{{hole_rows}}

The pinned pair depletes its neighbourhood: along the pin axis the contact field is `b + 2k x_1^3 + ...` to leading
order, a monotone ramp, so window-level critical points near the pins live in the transverse sector only
(`Lambda(x)/Lambda_inf` is below `10^(-10)` on the axis out to `|x_1| ~ 1.5` and recovers to `1` at `|x| ~ 3`;
the ray profiles at angles `0, 30, 45, 60, 90` degrees are in `RESULTS.json`, `ray_profile`). Near the pin
`Lambda -> 0` (`near_zero_profile`: `Lambda(0.05, 45 deg) = {{near05}}`, `Lambda(0.4, 90 deg) = {{near04}}` at
`k = 1, b = 0`). Almost the whole `k`-dependence of the hole comes from the transverse sector where the
`f_xxx = 12k` conditioning is felt.

**Remote singleton mass** `R(k, b, L) = k integral_X Lambda dx` and the assembled `nu(1)`, with `alpha_1` from the
companion note (Math-#168, GH60 values; `alpha_2` likewise):

| `k` | `b` | `L` | `integral_X Lambda` | `R = k integral_X Lambda` | `alpha_1` (#168) | `nu(1) = alpha_1 + R` | `nu(2) = alpha_2` | `nu(2)/nu(1)` |
|---|---|---|---|---|---|---|---|---|
{{total_rows}}

For `L = 6` the direct periodized integral and the approximation `36 Lambda_inf + c_hole` are both given
(`RESULTS.json`, `remote_total`); they differ by `{{L6_dev}}` relative (the periodization changes the one-site
covariances by up to `8.8e-4` at `L = 6`). For `L = 12` the direct integral at `k = 1, b = 0` is
`{{L12_direct}}` against `{{L12_approx}}` from the far field plus hole.

**Reading.** For the parent torus sizes the remote singletons dominate `nu(1)` by two orders of magnitude at
`L = 24` (`R ~ L^2 Lambda_inf`), so the two-point cluster probability relative to a nonempty window is
`nu(2)/(nu(1) + nu(2)) ~ {{share24}}` at `k = 1, b = 0, L = 24`, against the near-only share `0.019` reported in
#168. The near share is the right object for the cluster geometry; the global share is the right object for the
finite-torus count.

## 5. Precision (empirical, not bounds)

- Quadrature: at the eight sample points the default orders `(24, 32, 24)` differ from `(32, 48, 32)` by at most
  `{{qdev}}` relative; on the exact unconditional control the default order is accurate to `{{absdet_err}}`.
- Grid: at `k = 1, b = 0` the hole constant is `{{hole_h03}}` (`h = 0.3`), `{{hole_h015}}` (`h = 0.15`),
  `{{hole_h01}}` (`h = 0.1`); with the higher quadrature order at `h = 0.3`: `{{hole_h03_hi}}`. Cutting the domain at
  `|x_i| <= 5` instead of `6` changes it by `{{tail_dev}}`.
- The periodized `L = 12` direct integral agrees with far field plus hole to `{{L12_rel}}` relative.

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
(full run, about {{minutes}} minutes), `SOURCE_MAP.json` (pins [LP], [RM], [CL], [RC] on `main`
`7d0c89a`), `SOURCE_FILES.json`, workflow `c6-remote-coefficient-numerics.yml`.
