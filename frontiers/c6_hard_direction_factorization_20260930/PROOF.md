# Hard-direction factorization: the near cluster coefficients of the Gaussian kernel in every dimension are the planar ones times an explicit factor R_d(b)

**Object:** CL-C6-HARD-DIRECTION-FACTORIZATION-20260930-v1.
**Author:** Anthropic Claude (Claude Code `session_015wNj8LPTKXsaT68G3DgPPh`), foreground owner-authorized continuation.
**Disposition:** AUTHOR-SIDE CANDIDATE; NONAUTHOR REVIEW OPEN. Scientific effect NONE: no register, catalog, GRAPH,
STATUS or source change; nothing in any consumed source is revalidated or promoted.

## 0. Statement

Fix `d >= 2`, `m = d - 1`, `b` real, `k > 0`, and the unit Gaussian kernel `K(x) = exp(-|x|^2/2)` on `R^d`
(the continuum limit of the periodized parent kernel of [LP] section 2; the size of the torus corrections is
stated in section 6). Let `dM^(d)` be the limiting near cluster measure [SC] (17) on `(s, h, O, tau)`, with the
spectral constant `c_m` of [SC] (8), the full normalizer `z0^(d) = lim Z_r / r^2` of [LP], the raw conditional
jet density `h_0` of [SC] section 2, and the endpoint weight `w(s, a, beta) = 9k^2 (4s^2 - B^2)` on the typed
domain `s < -|B|/2`, `B = beta - a^2/(12k)`. For `d = 2` it is the planar measure `z0^(-1) w h_0(0, a, beta, c)
ds da dbeta dc` of [CUB] section 4 / [SC] (17) with empty hard products.

**Theorem 1 (hard-direction factorization).** For every nonnegative measurable `g` of the soft cubic
coordinates `(s, a, beta, c)`,

    integral g(s, a, beta, c) dM^(d)(s, h, O, tau) = R_d(b) integral g(s, a, beta, c) dM^(2)(s, a, beta, c),   (1)

with

    R_d(b) = N_d(b) m_(2,b) / m_(d,b),                                                                     (2)
    N_d(b) = c_m (2 pi)^(-m(m-1)/4) integral_(0 < h_2 < ... < h_m) prod_j h_j^3 phi_2(h_j - b) prod_(i<j) (h_j - h_i) dh,
    m_(d,b) = E[(det A)^2 1{A negative definite}],   A = -b I_m + G_m,
    m_(2,b) = E[A^2 1{A < 0}],                        A ~ N(-b, 2),

where `phi_2` is the `N(0, 2)` density and `G_m` is the `m x m` GOE matrix with independent `N(0, 2)` diagonal and
`N(0, 1)` off-diagonal entries (`N_2 = 1`, `m_(2,b)` is Math-#168's `m_(2,b)`, `R_2 = 1`). The factor `R_d(b)` does
not depend on `k`.

**Corollary 1 (near coefficients).** The [SC] (20) coefficients satisfy `a_j^(d)(b, k) = R_d(b) a_j^(2)(b, k)`,
`j = 1, 2`. Hence `a_2 / a_1` (the near doublet-to-singleton ratio, `nu_near(2)/nu_near(1)`), and every law
obtained by normalizing a function of `(s, a, beta, c)` under `dM` by a positive finite mass (`0 < integral g dM
< infinity`; the factor `R_d(b)` is positive and finite and cancels) — the conditional law of the soft cubic given
`n >= 1`, the shape region measure `Q du dv` of [R] (R9)–(R10), the Pareto-11 radius law and the constants
`E eta = 5771/7062`, `I, J, D, E0` and all ratios of [R], [E], [Q], [ELD] — are the same in every dimension
`d >= 2`, for the continuum-kernel measures `dM^(d)`. The radial-tail constant of [R] (R13) satisfies `C_*^(d) = R_d(b) C_*^(2)`, since (R12)'s `J_cusp`
integrand has the same hard-direction factor (section 3).

**Corollary 2 (conditional, elder statements).** Where a source identifies `lim r^(-3) (1 - p_r) = a_1 + a_2`
(#170 Theorem S in `d = 2`, #175 Theorem F in `d >= 3`, both unmerged drafts), the elder-failure coefficient in
dimension `d` is `R_d(b) (alpha_1 + alpha_2)^(2)`, and the conditional lifetime-fraction and shape laws given
failure (#170 section 8.8, #175 M1, #179/#181's `S \ O2` laws) are dimension-independent. This corollary inherits
those sources' conditional status and promotes nothing. It concerns the sources' statements read for the same
continuum-kernel model as Theorem 1; the sources are stated for the periodized field on `T_L^d`, and a finite-`L`
theorem does not transfer to the continuum measures by replacing its covariance in notation, so no new
actual-field theorem is claimed here.

**Closed form.** `m_(3,0) = (7 - 4 sqrt2)/2`, `N_3(0) = 2 sqrt2`, hence

    R_3(0) = 4 sqrt2 / (7 - 4 sqrt2) = (32 + 28 sqrt2)/17 = 4.21164586743804...                          (3)

Numerical values of `R_d(b)` for `d = 3, 4, 5` and `b = 0, 1`, the resulting `a_1, a_2, z0` in `d = 3, 4, 5`, and
the Monte Carlo and finite-`r` controls are in section 5 and `RESULTS.json`.

## 1. Sources and exposure

- [SC] `frontiers/spectral_cluster_closure_20260929/PROOF.md` (main, blob `16c56821`): section 2 (4), (7), (8),
  (9); section 5 (17); section 6 (19)–(20). Consumed as the definition of `dM^(d)`, `c_m`, `h_0`, `a_j`.
- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`): the model,
  `Q_r`, `W_r = F_d(H_M) F_(d-1)(H_S)`, `Z_r / r^2 -> z0 > 0`, the moment bounds used in Lemma 2.
- [CUB] `frontiers/planar_cubic_cluster_20260929/PROOF.md` (blob `bb446d08`): the classifier `n(s, a, beta, c)`
  and the planar contact structure.
- [R] `frontiers/two_scale_cluster_geometry_20260929/RADIAL_TAIL.md` (blob `0f14417e`): (R11)–(R13).
- [Q] `frontiers/radial_rate_20260930/PROOF.md` (blob `65f24b1f`, merged with #176): (21) the planar odd
  variances `v_a = v_beta = 2`, `v_c = 6` in the continuum, matching Lemma 1.
- [NUM] `frontiers/c6_cluster_coefficients_numerics_20260930/RESULTS.json` (blob `2648314f`, Math-#168): the
  planar values `alpha_1, alpha_2` (GH60, floating, not certified) multiplied in section 5.
- Unmerged, quoted only for Corollary 2 and the list of dimension-independent laws: [E] Math-#169 `PROOF.md`
  `19a6044f`, [ELD] Math-#181 `PROOF.md` `91f88e39` and Math-#179 `PROOF.md` `1310dc11`, #170 `ef2aa579`,
  #175 `923d3236`.

Exposure: I authored [NUM] (Math-#168) and the numerical packets Math-#174/#178, and [CL] (Math-#159); I authored
none of [SC], [LP], [CUB], [R], [Q], [E], [ELD]. Same GitHub account as every lane; zero organizational-independence
credit. Lemma 2 in `d = 2` is the normalizer identification of Math-#168 (accepted as an identity in the xAI read
5360559751); its `d >= 3` form is new here.

## 2. Lemma 1: the conditional jet law at contact

Let `U_0 = (f, grad f, f_xx, f_(x y_i) (i = 1..m), f_xxx)` at the midpoint, with values `(b, 0, 0, 0, 12k)`, and
let `A = (f_(y_i y_j))` be the transverse Hessian and `T` the list of third derivatives other than `f_xxx`, as in
[SC] section 2. For the Gaussian kernel, `Cov(d^alpha f(0), d^beta f(0)) = (-1)^|alpha| d^(alpha+beta) K(0)` and
`d^gamma K(0) = prod_i (-1)^(gamma_i/2) (gamma_i - 1)!!` when every `gamma_i` is even, `0` otherwise.

**Lemma 1.** Conditionally on `U_0`:

1. `A = -b I_m + G_m` with `G_m` as in section 0 (independent `N(0,2)` diagonal, `N(0,1)` off-diagonal entries);
2. `T` is centered Gaussian, independent of `A`, with independent components of variance `6` (`T_iii`), `2`
   (`T_iij`, `i != j`, including `T_(xx y_i)` and `T_(x y_i y_i)`) and `1` (`T_ijk`, distinct indices);
3. the law of `(A, T)` is invariant under transverse rotations `y -> O y`, `O in O(m)`: `h_0(O A O^t, Rot_O T) =
   h_0(A, T)`; and it does not depend on `k`.

Proof. Parity: a covariance `(-1)^|alpha| d^(alpha+beta) K(0)` vanishes unless `alpha + beta` is even in every
coordinate, so the even jets `(f, f_xx, f_(x y_i), A)` and the odd jets `(grad f, f_xxx, T)` are independent, and
within each parity class the regression on `U_0` is the finite computation `Cov(target, U_0) Cov(U_0)^(-1)`. For
the even class the unconditional covariances are `Var f = 1`, `Var f_xx = Var A_ii = 3`, `Var f_(x y_i) = Var A_ij =
1` (`i != j`), `Cov(f, f_xx) = Cov(f, A_ii) = -1`, `Cov(f_xx, A_ii) = Cov(A_ii, A_jj) = 1`, all others zero;
conditioning on `(f, f_xx) = (b, 0)` (the `f_(x y_i)` are uncorrelated with `A`) gives `E[A_ii] = -b`,
`Var A_ii = 3 - 1 = 2`, `Cov(A_ii, A_jj) = 1 - 1 = 0`, and `A_ij` untouched: item 1. For the odd class,
`Cov(T_(x x y_i), f_(y_i)) = -1`, `Cov(T_(x y_i y_i), f_x) = -1`, `Cov(T_(y_i y_i y_i), f_(y_i)) = -3`,
`Cov(T_(y_i y_i y_j), f_(y_j)) = -1`, `Cov(T_(x y_i y_i), f_xxx) = 3` (the only nonzero covariance of a component
of `T` with `f_xxx`), `Cov(f_x, f_xxx) = -3`, `Var f_xxx = 15`, and the unconditional variances of `T` are `15`,
`3`, `1` by multiplicity. Regress jointly on `(grad f, f_xxx)`: for `T_(x y_i y_i)` the coefficients on
`(f_x, f_xxx)` are `(-1, 3) [[1, -3], [-3, 15]]^(-1) = (-1, 0)`, so the coefficient on `f_xxx` vanishes although the
raw covariance does not, the observed value `12k` never enters, and the conditional variance is `3 - 1 = 2`;
for `T_(y_i y_i y_i)` the coefficient on `f_(y_i)` is `-3` and the variance `15 - 9 = 6`; for `T_(y_i y_i y_j)` (`i != j`; unconditional
variance `3`) the coefficient on `f_(y_j)` is `-1` and the variance `3 - 1 = 2`; `T_(xx y_i)` has `Cov(., f_(y_i)) = -1`, variance `3 - 1 = 2`; the
distinct-index components `T_(ijk)` are uncorrelated with `U_0` and keep variance `1`. Every conditional mean is
`0` because the coefficients on the two nonzero observations `f = b` and `f_xxx = 12k` are all zero, and every
conditional cross covariance vanishes: item 2. Item 3: the three blocks of `T` (`T_(xx .)` an isotropic vector, `T_(x . .)` a GOE-type
matrix with the variances of item 2, `T_(. . .)` an isotropic symmetric 3-tensor) and `A` are each `O(m)`-invariant
and mutually independent, and no value of `U_0` other than `b` enters. The computation is carried out exactly in
rational arithmetic for `d = 2, 3, 4, 5` in `factorization.py` (`lemma_one`), including the vanishing of every
even/odd cross covariance and of every coefficient on `f` and `f_xxx` in the odd regression. In `d = 2` this is
Math-#168's exact contact structure (`A_0 ~ N(-b, 2)`, odd jets `N(0, diag(2, 2, 6))`), and [Q] (21) at `L = infinity`. QED

## 3. Lemma 2: the full normalizer

**Lemma 2.** `z0^(d) = lim_(r->0) Z_r / r^2 = 36 k^2 m_(d,b)`, with `m_(d,b) = E[(det A)^2 1{A negative
definite}]` for `A` as in Lemma 1.

Proof. Under `Q_r` the fixed jets at the midpoint converge in law to their `U_0`-conditional law ([SC] section 2,
`h_r -> h_0` locally uniformly), and every fixed `C^q` moment is bounded uniformly in `r` ([LP], quoted as [SC] (6)).
With `K` the `C^4` bound, Taylor expansion from the midpoint gives, in the frame `(x, y)`,

    H_M = [[ -6kr + O(r^2 K),  -(r/2) T_(xx .) + O(r^2 K) ], [ ., A + O(r K) ]],
    H_S = [[  6kr + O(r^2 K),   (r/2) T_(xx .) + O(r^2 K) ], [ ., A + O(r K) ]],

because `f_xx(0) = [f_x(S) - f_x(M)]/r + O(r^2 K) = O(r^2 K)` and `f_(x y_i)(0) = O(r^2 K)` are pinned by the
endpoint gradients while `f_xxx(0) = 12k + O(rK)`. Expanding the determinants along the first row, each
off-diagonal term carries two factors of order `r`, so `det H_M = -6kr det A + O(r^2 K^d)` and `det H_S = 6kr det A
+ O(r^2 K^d)`. On `{det A != 0}` (probability one) and for `r` small enough (depending on the realization), the
eigenvalue of `H_M` continuing the `x`-direction is `-6kr + O(r^2 K) < 0` and that of `H_S` is `6kr + O(r^2K) > 0`,
the remaining eigenvalues being those of `A` up to `O(rK)`; hence `1{index H_M = d} 1{index H_S = d - 1} ->
1{A negative definite}` and `W_r / r^2 -> 36 k^2 (det A)^2 1{A negative definite}` pointwise. Domination:
`W_r / r^2 <= C K^(2d)` ([LP], [SC] section 1) with all moments of `K` bounded uniformly in `r`, so dominated
convergence gives `Z_r / r^2 -> 36 k^2 E[(det A)^2 1{A negative definite}]` with `A` distributed as in Lemma 1. QED

The `d = 2` case, `z0 = 36 k^2 m_(2,b)`, is Math-#168's identification. The Monte Carlo evaluation of `E_Q W_r /
r^2` under the exact finite-`r` endpoint regression (`f`, `grad f` at both pins; `r = 0.1, 0.05`; section 5)
agrees with `36 k^2 m_(d,b)` within statistical error in `d = 2` and `d = 3`.

## 4. Proof of Theorem 1

In (17) write `tau = (a, beta, c, xi)` in the eigenframe `(x, e_soft, e_hard)`: `a = tau_(xxz)`, `beta =
tau_(xzz)`, `c = tau_(zzz)` and `xi` the remaining `(m+2)(m+1)m/6 + m(m+1)/2 + m - 3` tensor entries. By Lemma
1(3), `h_0(O diag(0, -h) O^t, Rot_O tau) = h_0(diag(0, -h), tau)`, and by Lemma 1(1)–(2) this equals

    p_A(diag(0, -h)) p_T(tau),   p_A(diag(0, -h)) = phi_2(b) prod_(j=2..m) phi_2(h_j - b) (2 pi)^(-m(m-1)/4),

the density of `-b I + G_m` in the upper-triangular coordinates at a matrix with diagonal `(0, -h_2, ..., -h_m)`
and zero off-diagonal entries (`phi_2(0 + b)` for the soft entry, `phi_2(-h_j + b)` for the hard ones,
`phi_1(0) = (2 pi)^(-1/2)` for each of the `m(m-1)/2` off-diagonal entries). The integrand of (17) depends on
`xi` only through `p_T`, and the `xi`-marginal of `p_T` is the planar odd density `p_odd(a, beta, c) = N(0,
diag(2, 2, 6))` (Lemma 1(2)). The normalized Haar integral is `1`. What remains is

    integral g dM^(d) = (c_m / z0^(d)) phi_2(b) (2 pi)^(-m(m-1)/4)
        integral_(0<h_2<...<h_m) prod h_j^3 prod_(i<j)(h_j - h_i) prod phi_2(h_j - b) dh
        integral g(s, a, beta, c) w(s, a, beta) p_odd(a, beta, c) ds da dbeta dc
      = (phi_2(b) N_d(b) / z0^(d)) integral g w p_odd ds da dbeta dc,

where `prod h_j^3 prod_(i<j)(h_j - h_i)` is the `[SC] (17)` hard weight `prod_(j>=2) h_j^3 prod_(2<=i<j<=m)
(h_j - h_i)`. For `d = 2` the same display reads `integral g dM^(2) = (phi_2(b) / z0^(2)) integral g w p_odd`
(`c_1 = 1`, no hard variables). Dividing, and inserting Lemma 2 for both normalizers,

    integral g dM^(d) / integral g dM^(2) = N_d(b) z0^(2) / z0^(d) = N_d(b) m_(2,b) / m_(d,b) = R_d(b).

The factor is independent of `g`, `k` (both `z0` carry the same `36 k^2`) and of the soft integral, which is the
whole content of (1). The classifier `n` of [CUB] depends on `(s, a, beta, c)` only, so `g = 1{n = j}` gives
Corollary 1 for `a_j`; `g = Q 1_E |Z|^(-12) ...` after [R]'s change of variables (R10) (which acts on `(s, beta, c)`
at fixed `a` and does not touch `h`, `O`, `xi`) gives the statement for `C_*` and for every shape functional; the
cusp integrand of (R12) is `h_0` at `beta = a^2/(12k)`, `c = a^3/(144k^2)`, so `J_cusp^(d) = [N_d(b)/c_m] phi_2(b)
integral gamma^11 p_odd(a, a^2/(12k), a^3/(144k^2)) da` and `(c_m / z0^(d)) J_cusp^(d) = R_d(b) (1/z0^(2))
J_cusp^(2)`. QED

**Closed form (3).** At `b = 0`, `m_(2,0) = 1`; `N_3(0) = c_2 (2 pi)^(-1/2) integral_0^infinity h^3 phi_2(h) dh =
sqrt(pi/2) . (1/2) E|N(0,2)|^3 = sqrt(pi/2) . 4/sqrt(pi) = 2 sqrt2`, using `c_2 = pi` from (8) (`H_2 = 2 sqrt(pi)`);
and, in polar coordinates `(l_1, l_2) = rho (cos theta, sin theta)` for the eigenvalues of `A = G_2`, whose joint
density is `|l_1 - l_2| e^(-(l_1^2 + l_2^2)/4) / (8 sqrt(2 pi))`,

    m_(3,0) = E[l_1^2 l_2^2 1{l_1, l_2 < 0}]
            = (sqrt2 / (32 sqrt(2 pi))) integral_0^infinity rho^6 e^(-rho^2/4) drho
              integral_(3pi/4)^(5pi/4) |sin u| cos^2(2u) du
            = (sqrt2 / (32 sqrt(2 pi))) . 120 sqrt(pi) . 2(7 - 4 sqrt2)/15 = (7 - 4 sqrt2)/2,

so `R_3(0) = 2 sqrt2 / ((7 - 4 sqrt2)/2) = 4 sqrt2 (7 + 4 sqrt2)/17 = (32 + 28 sqrt2)/17`. `factorization.py`
reproduces both closed forms to `1e-10` by quadrature.

## 5. Values (floating; `RESULTS.json`)

`c_1 = 1`, `c_2 = pi`, `c_3 = 19.7392088`, `c_4 = 194.818182` ([SC] (8) through Mehta's integral, `H_m =
(2 pi)^(m/2) prod_(j<=m) Gamma(1 + j/2) / (Gamma(3/2)^m m!)`); the eigenvalue densities normalize to `1` to `1e-9`
for `d <= 4` and to `1.9e-8` (`b = 0`) and `4.6e-6` (`b = 1`) for `d = 5`, where the full-line four-dimensional
integral is evaluated at order `40`; the one-sided integrals `N_5`, `m_5` themselves are converged to `1e-14`
across orders `30/40/50` (`quadrature_orders`).

| `d` | `b` | `N_d(b)` | `m_(d,b)` | `m_(d,b)` (Monte Carlo) | `R_d(b)` |
|---|---|---|---|---|---|
| 2 | 0 | 1.0000000000 | 1.0000000000 | (exact `m_(2,b)`) | 1.0000000000 |
| 2 | 1 | 1.0000000000 | 2.7201411062 | (exact `m_(2,b)`) | 1.0000000000 |
| 3 | 0 | 2.8284271247 | 0.6715728753 | 0.6718 ± 0.0109 | 4.2116458674 |
| 3 | 1 | 9.4233005488 | 5.5480602736 | 5.5474 ± 0.0442 | 4.6201205312 |
| 4 | 0 | 3.4705627485 | 0.2974694707 | 0.3093 ± 0.0273 | 11.6669543930 |
| 4 | 1 | 42.2684338363 | 8.3062048780 | 8.5096 ± 0.1829 | 13.8421946076 |
| 5 | 0 | 2.2462120246 | 0.0856492086 | 0.0535 ± 0.0166 | 26.2257183973 |
| 5 | 1 | 109.5752982564 | 8.9602511317 | 8.4727 ± 0.5598 | 33.2647231231 |

`R_3(0)` agrees with `(32 + 28 sqrt2)/17` to `1e-12`. The nested Gauss–Legendre orders `40/60/80` (`30/40/50` for
`d = 5`) agree to `1e-14` relative. Monte Carlo `N_3(b)` (density of the largest eigenvalue of `-bI + G_2` at `0`
times the conditional second moment of the other eigenvalue, bin half-width `0.05`): `b = 0`: `2.8822 ± 0.0286` against `2.8284`; `b = 1`: `9.3532 ± 0.0683` against `9.4233`.

**Near coefficients in `d = 3, 4, 5`** (`a_j^(d) = R_d(b) alpha_j^(2)`; `alpha_j^(2)` are Math-#168's GH60 values,
`b`-dependent, floating, not certified; `z0^(d) = 36 k^2 m_(d,b)`):

| `k` | `b` | `d` | `R_d` | `a_1` | `a_2` | `a_1 + a_2` | `a_2 / a_1` (all `d`) | `z0^(d)` |
|---|---|---|---|---|---|---|---|---|
| 1/2 | 0 | 2 | 1.000000 | 1.1182 | 0.034745 | 1.153 | 0.03107 | 9.0000 |
| 1/2 | 0 | 3 | 4.211646 | 4.7095 | 0.14634 | 4.8558 | 0.03107 | 6.0442 |
| 1/2 | 0 | 4 | 11.666954 | 13.046 | 0.40537 | 13.451 | 0.03107 | 2.6772 |
| 1/2 | 0 | 5 | 26.225718 | 29.326 | 0.91122 | 30.237 | 0.03107 | 0.7708 |
| 1/2 | 1 | 2 | 1.000000 | 0.32016 | 0.0099479 | 0.3301 | 0.03107 | 24.4813 |
| 1/2 | 1 | 3 | 4.620121 | 1.4792 | 0.045961 | 1.5251 | 0.03107 | 49.9325 |
| 1/2 | 1 | 4 | 13.842195 | 4.4316 | 0.1377 | 4.5693 | 0.03107 | 74.7558 |
| 1/2 | 1 | 5 | 33.264723 | 10.65 | 0.33091 | 10.981 | 0.03107 | 80.6423 |
| 1 | 0 | 2 | 1.000000 | 1.3291 | 0.025509 | 1.3546 | 0.01919 | 36.0000 |
| 1 | 0 | 3 | 4.211646 | 5.5975 | 0.10744 | 5.705 | 0.01919 | 24.1766 |
| 1 | 0 | 4 | 11.666954 | 15.506 | 0.29761 | 15.804 | 0.01919 | 10.7089 |
| 1 | 0 | 5 | 26.225718 | 34.856 | 0.66899 | 35.525 | 0.01919 | 3.0834 |
| 1 | 1 | 2 | 1.000000 | 0.38052 | 0.0073035 | 0.38783 | 0.01919 | 97.9251 |
| 1 | 1 | 3 | 4.620121 | 1.7581 | 0.033743 | 1.7918 | 0.01919 | 199.7302 |
| 1 | 1 | 4 | 13.842195 | 5.2673 | 0.1011 | 5.3684 | 0.01919 | 299.0234 |
| 1 | 1 | 5 | 33.264723 | 12.658 | 0.24295 | 12.901 | 0.01919 | 322.5690 |
| 2 | 0 | 2 | 1.000000 | 2.1621 | 0.016928 | 2.179 | 0.00783 | 144.0000 |
| 2 | 0 | 3 | 4.211646 | 9.106 | 0.071295 | 9.1773 | 0.00783 | 96.7065 |
| 2 | 0 | 4 | 11.666954 | 25.225 | 0.1975 | 25.423 | 0.00783 | 42.8356 |
| 2 | 0 | 5 | 26.225718 | 56.703 | 0.44395 | 57.147 | 0.00783 | 12.3335 |
| 2 | 1 | 2 | 1.000000 | 0.61903 | 0.0048467 | 0.62387 | 0.00783 | 391.7003 |
| 2 | 1 | 3 | 4.620121 | 2.86 | 0.022392 | 2.8824 | 0.00783 | 798.9207 |
| 2 | 1 | 4 | 13.842195 | 8.5687 | 0.067089 | 8.6358 | 0.00783 | 1196.0935 |
| 2 | 1 | 5 | 33.264723 | 20.592 | 0.16122 | 20.753 | 0.00783 | 1290.2762 |

**Finite-`r` normalizer** (`E_Q W_r / r^2` by Monte Carlo under the exact endpoint regression, `k = 1`,
`400000` samples each, against `36 k^2 m_(d,b)`):

| `d` | `b` | `r` | `E_Q W_r / r^2` | s.e. | `36 k^2 m_(d,b)` |
|---|---|---|---|---|---|
| 2 | 0 | 0.1 | 35.531 | 0.126 | 36.0000 |
| 2 | 0 | 0.05 | 36.015 | 0.127 | 36.0000 |
| 2 | 1 | 0.1 | 96.994 | 0.229 | 97.9251 |
| 2 | 1 | 0.05 | 97.998 | 0.231 | 97.9251 |
| 3 | 0 | 0.1 | 23.799 | 0.285 | 24.1766 |
| 3 | 0 | 0.05 | 24.076 | 0.296 | 24.1766 |
| 3 | 1 | 0.1 | 197.026 | 1.127 | 199.7302 |
| 3 | 1 | 0.05 | 199.340 | 1.140 | 199.7302 |

## 6. Non-claims and the torus

- The theorem is for the continuum kernel only. The [SC] measure for the periodized field on the torus `T_L^d`
  uses the one-site jet covariances of `K_L`, which differ from the continuum values by image terms. At finite `L`
  the transverse rotational invariance of Lemma 1(3) is broken, so the exact step that extracts a common
  hard-direction factor is not available. The quoted planar one-site deviations of Math-#168 (`8.8e-4` relative at
  `L = 6`, `2e-14` at `L = 12`, `1.4e-13` at `L = 24`) are diagnostics for those covariance entries only. No
  finite-`L` factorization identity, coefficient error bound, relative accuracy or higher-dimensional correction
  is established in this packet. Obtaining one requires a separate perturbation estimate for the relevant
  conditional covariance, the numerator integrals and the full normalizer; a small covariance perturbation does
  not give a uniform relative error over arbitrary nonnegative `g` (tail indicators `1{x >= a}` under `N(0, 1)`
  against `N(0, 1 + delta)` have unbounded relative error as `a -> infinity`).
- Nothing is said about the remote singleton coefficient `beta_far` ([SC] (22), two-site) or the contact kernel
  `Lambda(x)`; the dimension dependence of `nu(1) = a_1 + beta_far` is not reduced by this note.
- No rate, no finite-`r` statement, no uniformity in `d`, `k`, `b` or `L`. The sources' theorems are consumed at
  their stated conditional scopes; Corollary 2 inherits the unmerged status of #170/#175/#179/#181.
- The planar inputs `alpha_j^(2)` are floating-point values with the empirical precision reported in Math-#168
  (about `2e-4` relative against Monte Carlo); the `d >= 3` products inherit it. `R_d(b)` itself is a
  quadrature value converged to `1e-14`, and exact for `(d, b) = (3, 0)`.
- The Monte Carlo columns are consistency checks with reported standard errors, not enclosures.

## 7. Verification and review obligations

`python -B -S factorization.py --check` and `-B -O -S` exit `0`: exact Lemma 1 in `d = 2..5`; `c_1 = 1`, `c_2 =
pi`; eigenvalue-density normalization to `1e-9` for `d <= 4` and to `1e-5` for `d = 5` (observed `4.6e-6` at
`b = 1`, section 5); `m_(2,0) = 1`, `m_(3,0) = (7 - 4 sqrt2)/2`, `N_3(0) = 2 sqrt2`, `R_3(0) = (32 + 28 sqrt2)/17`,
`R_2 = 1`; `m_(2,b) > 0` at `b = -12` (stable tail evaluation); replay of every `N_d, m_d, R_d` against
`RESULTS.json` to `1e-9` relative; the Monte Carlo and finite-`r` entries within `4` standard errors (plus the
stated bin and `O(r)` allowances). Mutants
`drop-vandermonde`, `hard-power-two`, `drop-spectral-constant` exit `1`. The full run regenerates `RESULTS.json`
deterministically (seeded) in about ten minutes.

Requested bounded nonauthor read (OpenAI or xAI): **Slice A** Lemma 1 and Lemma 2 (the conditional jet law and
the normalizer identification in `d >= 3`, including the index bookkeeping of `H_M`, `H_S`); **Slice B** the proof
of Theorem 1 (the `p_A` density at `diag(0, -h)` in the upper-triangular coordinates, the trivial Haar integral, the
`xi`-marginal, the `c_m` bookkeeping against [SC] (8)–(9) and (17)) and the closed form (3); **Slice C** whether
the corollaries and non-claims are stated at the right conditional scope. The author will not merge.
