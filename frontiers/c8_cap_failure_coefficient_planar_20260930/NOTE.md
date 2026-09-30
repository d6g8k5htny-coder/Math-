# The cap-failure probability of Theorem A has an exact leading coefficient in the plane

**Object:** `CL-C8-CAP-FAILURE-COEFFICIENT-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude.
**Kind:** author-side limit theorem (Theorem G) with certified enclosures of its coefficient (exact rational interval
arithmetic; standard library only). **Scientific effect:** NONE. Catalog entry C8 (`reviews/candidates_pending_20260928/CANDIDATES.md`:
"explicit finite `C`, `r_*`, `z_*`, `c_{B,K}`, `c_{d,L}` on a declared band; OPEN") stays OPEN: this packet supplies neither
`C` nor `r_*`; it determines the exact size of the quantity that `C r^3` bounds, hence a lower bound for every admissible `C`.
No STATUS, PROOF_INDEX, GRAPH or catalog edit. Same GitHub account as every lane; zero organizational-independence credit.
The author will not merge.

Sources (pinned in `SOURCE_MAP.json`): [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`
(sections 1, 3, 4, 5, 7: the law `Q`, the weight `W_r`, the normalizer `Z_r`, the contact frame, the coupling (4.2), the
limit (5.4), the good event `G_r` and the bounds (7.5)–(7.8)); [CAP] `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`
(the cylinder `D`, the partial-block norms `M_3`, `M_4`, condition (1), and the recorded constants (2)–(3)); [NUM]
`frontiers/c6_cluster_coefficients_numerics_20260930/RESULTS.json` (the exact planar contact structure and the values of
`alpha_1`, `alpha_2`); [S] `frontiers/local_elder_geometry_20260930/PROOF.md` (Theorem S, (S2): `r^-3 (1 - p_r) -> alpha_1 + alpha_2`);
[Z] `frontiers/c8_normalizer_floor_planar_20260930/NOTE.md` at Math-#195 (the midpoint-jet coordinates; read, not consumed).

## 0. Statement

Setting of [LP] section 1 in `d = 2`: the torus `X = (R / L Z)^2`, the kernel `K_L` (periodized Gaussian, `K_L(0) = 1`),
an orthonormal frame `R` with axial direction `u`, the pins `M = -(r/2) u`, `S = (r/2) u`, `f(M) = b`, `f(S) = b - k r^3`,
`grad f(M) = grad f(S) = 0`, the Gaussian regression law `Q = Q_{r,b,k,R}`, the typed weight
`W_r = |det H_M det H_S| 1{H_M < 0, det H_S < 0}`, `Z_r = E_Q W_r`, `dQ^W = (W_r / Z_r) dQ`. In the frame's coordinates
`(x, y)` let `D = [-2r, 2r]^2` and, for `j = 3, 4`, `M_j = max_{a + c = j} sup_D |partial_x^a partial_y^c f|` ([CAP] section 1;
in `d = 2` the partial-block norm is the maximum of the coordinate partials). The good event of [LP] section 7 / [CAP] (1) is

    G_r = { -f_yy(M) > (4/(3k)) r M_3^2,  r M_4 <= 3k/10 }

(on the typed support `-f_yy(M) = lambda_min(-A_M)`). Theorem A of [LP] is `Q^W(G_r^c) <= C r^3` for `0 < r <= r_*`.

**Theorem G.** Fix `b in R`, `k > 0`, `L`, `R`. Then

    Q^W(G_r^c) = c_G(b, k) r^3 + o(r^3),        r -> 0,

    c_G(b, k) = R(b) J(k),
    R(b) = p_w(0) / E[w^2 1{w < 0}],
    J(k) = (216 k^3)^(-1) E[ integral_{max(a, c)}^{8 M^2} (s - a)(s - c) ds ],
    a = v^2,   c = 6k om - v^2,   M = max(12k, 2|v|, |om|, |Y|),

where `w` has the law of `f_yy(0)` given `(f, f_xx, f_xy)(0) = (b, 0, 0)`, `p_w` is its density, and `(v, om, Y)` has the law of
`(-f_xxy/2, f_xyy, f_yyy)(0)` given `(f_x, f_y, f_xxx)(0) = (0, 0, 12k)`, all under the unconditioned field with kernel
`K_L(R .)`; `w` is independent of `(v, om, Y)`. For the reference kernel `exp(-|z|^2/2)` (equivalently `L -> infinity`),

    w ~ N(-b, 2),   v ~ N(0, 1/2),   om ~ N(0, 2),   Y ~ N(0, 6),   independent,

    R(b) = [phi(b/sqrt2) / sqrt2] / [(2 + b^2) Phi(b/sqrt2) + sqrt2 b phi(b/sqrt2)],

and `J(k) = 2359296 k^3 (1 + delta(k))` with `delta(k) -> 0` rapidly (`delta(1/6) = 52.7`, `delta(1/2) = 0.0232`,
`delta(3/4) = 1.3e-4`, `delta(1) = -1.3e-6`, `|delta(k)| < 2e-6` for `k >= 1`; both signs occur).

**Certified values (reference kernel).** `J(k)` at `k in {1/6, 1/2, 3/4, 1, 3/2, 2}`, `R(b)` at `b in {0, 1/4, 1/2, 3/4, 1, 6/5}`
and the products, all as rational enclosures (section 4). Two headline numbers:

    c_G(0, 2)     in  [5324360.4426, 5324360.4427]      (the maximum over the Math-#195 band B = [0, 1], K = [1/2, 2] among the grid points),
    c_G(6/5, 1/6) in  [35736.7352, 35736.8785]    (SIDE24's fixed-axis parameters, the only pair for which an explicit C is on record).

**Corollary (what this says about `C` and `r_*`).** Every constant `C` for which [LP] Theorem A holds at `(b, k)` satisfies
`C >= c_G(b, k)`, and every band containing `(0, 2)` needs `C > 5.3 x 10^6`; the cap route cannot give a nontrivial bound
(`C r^3 < 1`) above `r = c_G^{-1/3}`, which is `5.7 x 10^-3` at `(0, 2)`, `3.4 x 10^-2` at `(1, 1/2)`, and `3.0 x 10^-2` at
`(6/5, 1/6)`. The recorded constant of [CAP] (2)–(3), `C3_new + C4_new / 20 < 2.4 x 10^23` at `(6/5, 1/6)`, exceeds the sharp
coefficient there by a factor above `6 x 10^18`. Against the true failure coefficient `alpha_1 + alpha_2` of [S] (S2) (the
actual elder-pairing failure, values from [NUM]) the cap criterion overstates the failure rate by the `b`-free factor
`36 k^2 J(k) / (J_1(k) + J_2(k))`: `7.4 x 10^4` at `k = 1/2`, `4.9 x 10^5` at `k = 1`, `2.4 x 10^6` at `k = 2` (section 5).

## 1. Notation and the exact identities

Write `lambda = -f_yy(M)`, and the six midpoint-jet coordinates of [Z] section 2 (exact for every `C^2` function with the
pins; only their definitions are used here):

    w = f_yy(M),                     om = (f_yy(S) - f_yy(M)) / r,
    T = (f_xx(M) + 6 k r) / r^2,     tau = (f_xx(S) - f_xx(M) - 12 k r) / r^3,
    v = f_xy(M) / r,                 nu = (f_xy(S) + f_xy(M)) / r^2.

They recover `f_xx(M) = r^2 T - 6kr`, `f_xx(S) = r^2 (T + r tau) + 6kr`, `f_xy(M) = r v`, `f_xy(S) = r (r nu - v)`,
`f_yy(S) = w + r om`. Each of `T`, `tau`, `nu`, `v`, `om` is a linear functional of `f` annihilating the polynomials of
degree `<= 3, 4, 3, 2, 2` respectively along the pin segment (the pins supply `f_x(M) = f_x(S) = f_y(M) = f_y(S) = 0`
and `f(S) - f(M) = -k r^3`), so by Taylor's formula with integral remainder

    |T| <= C ||f||_{C^4(D)},  |tau| <= C ||f||_{C^5(D)},  |nu| <= C ||f||_{C^4(D)},  |v| <= C ||f||_{C^3(D)},  |om| <= C ||f||_{C^3(D)}   (1.1)

with absolute constants, for `r <= 1`, and as `r -> 0` (pathwise, for a `C^5` function) `T -> f_xxxx(0)/12`,
`v -> -f_xxy(0)/2`, `om -> f_xyy(0)`, `nu -> f_xxxy(0)/... ` (a fixed combination of the 4-jet), `tau` to a fixed combination of the 5-jet.
The determinants are exactly

    det H_M = r^2 [ (6k - r T) u_r - v^2 ],                                      u_r := lambda / r = -w / r,
    det H_S = r^2 [ (6k + r T + r^2 tau)(om - u_r) - (r nu - v)^2 ],                                        (1.2)

so on `{u_r = u}`:  `W_r = r^4 |(6k - rT) u - v^2| |(6k + rT + r^2 tau)(om - u) - (r nu - v)^2| 1{type}`, with `type` =
`{f_xx(M) < 0, det H_M > 0, det H_S < 0}`.

## 2. Proof of Theorem G

**2.1 Coupling.** Let `G` be the unconditioned field (kernel `K_L(R .)`) and `U_r(G)` the six pin functionals in the
preconditioned form [LP] (3.1), with target `v_r` and covariance `Sigma_r`. The Gaussian regression coupling

    f_r = G + kappa_r(z) . (v_r - U_r(G)),        kappa_r(z) = Cov(G(z), U_r) Sigma_r^{-1},                   (2.1)

realizes `Q_r` for every `r` on one probability space ([LP] (4.2)). As `r -> 0`, `U_r(G) -> U_0(G) = (f, f_x, f_xx, f_xxx, f_y, f_xy)(0)`
(Taylor), `v_r -> v_0 = (b, 0, 0, 12k, 0, 0)`, `Sigma_r -> Sigma_0` (positive definite, [LP] section 3), and
`Cov(G(z), U_{r,i}) -> Cov(G(z), U_{0,i})` in every `C^q(X)` (difference quotients of derivatives of `K_L`). Hence
`f_r -> f_0 := G + kappa_0 . (v_0 - U_0(G))` in `C^q(X)` almost surely and in every `L^p`, for every `q`; `f_0` has the
contact law `Q_0` (the field given the contact jet `U_0 = v_0`). All `Q_r`-moments of `||f_r||_{C^q(X)}` are bounded
uniformly in `r <= 1` ([LP] (4.1)).

**2.2 Regression on `w`.** Under `Q_r`, `w = f_r,yy(M)` is `N(mu_w(r), sigma_w(r)^2)` with `(mu_w, sigma_w) -> (mu_w(0), sigma_w(0))`,
the parameters of `f_yy(0)` given the contact pins (`(-b, sqrt2)` for the reference kernel). Put `g_r(z) = Cov_Q(f_r(z), w) / sigma_w(r)^2`
and `f_r^perp = f_r - (w - mu_w(r)) g_r`, independent of `w`, with `g_r -> g_0` in every `C^q` and `f_r^perp -> f_0^perp` as in 2.1.
For any functional `Psi`,

    E_Q[Psi(f_r)] = integral p_{w,r}(omega) E[Psi(f_r^perp + (omega - mu_w(r)) g_r)] d omega.                  (2.2)

The law of `f_r^perp + (0 - mu_w(0)) g_0` in the limit is the contact law given `f_yy(0) = 0`: by the parity of `K_L`
(`K_L(-z) = K_L(z)`, so all odd-order derivatives of `K_L` vanish at 0), the odd jets `(f_x, f_y, f_xxx, f_xxy, f_xyy, f_yyy)(0)`
are independent of the even jets `(f, f_xx, f_xy, f_yy)(0)`, and the conditioning on `f_yy(0) = 0` leaves the law of the odd
3-jet given `(f_x, f_y, f_xxx) = (0, 0, 12k)` unchanged. That law is `N(mu_odd, Sigma_odd)`; for the reference kernel the odd
covariances are `E f_x^2 = E f_y^2 = 1`, `E f_x f_xxx = -3`, `E f_x f_xyy = E f_y f_xxy = -1`, `E f_y f_yyy = -3`,
`E f_xxx^2 = E f_yyy^2 = 15`, `E f_xxy^2 = E f_xyy^2 = 3`, `E f_xxx f_xyy = E f_xxy f_yyy = 3`, the rest zero, so the two groups
`(f_x, f_xxx, f_xyy)` and `(f_y, f_xxy, f_yyy)` are independent, and the regression gives `f_xyy | (f_x = 0, f_xxx = 12k) ~ N(0, 2)`,
`(f_xxy, f_yyy) | f_y = 0 ~ N(0, diag(2, 6))`; likewise `f_yy | (f, f_xx, f_xy) = (b, 0, 0) ~ N(-b, 2)` ([NUM] `exact_structure`).
Hence `v = -f_xxy/2 ~ N(0, 1/2)`, `om = f_xyy ~ N(0, 2)`, `Y = f_yyy ~ N(0, 6)`, independent, as stated.

**2.3 The three negligible parts.** (i) `Q^W(r M_4 > 3k/10) <= (10 r / 3k)^p E_Q[(W_r/r^2) M_4^p] / (Z_r / r^2) = O(r^p)` for every
`p`, by the uniform moments and the floor [LP] (5.5) (this is [LP] (7.7) with `p = 4`). (ii) On the depth failure
`{lambda <= (4/(3k)) r M_3^2}`, the part `{lambda > sqrt r}` is contained in `{M_3 >= (3k/4)^(1/2) r^(-1/4)}`, so its `Q^W`-mass is
at most `E_Q[(W_r/r^2) M_3^p] (4/(3k))^(p/2) r^(p/4) / z_* = O(r^(p/4))`, which is `o(r^3)` for `p > 12`. (iii) `Z_r / r^2 -> z_0(b, k) = 36 k^2 E[w^2 1{w < 0}]`
by [LP] (5.4). It remains to show

    r^(-5) E_Q[ W_r 1{lambda <= (4/(3k)) r M_3^2} 1{lambda <= sqrt r} ]  ->  p_w(0) E[ I(v, om, Y) ],
    I = integral_{max(a, c)}^{8 M^2} (s - a)(s - c) ds / (6k).                                                (2.3)

**2.4 The main term.** Apply (2.2) with `omega = -r u`, `u in (0, r^(-1/2)]`:

    r^(-5) E_Q[...] = integral_0^{r^(-1/2)} p_{w,r}(-r u) E[ r^(-4) W_r(u) 1{u <= (4/(3k)) M_3(u)^2} ] du,

where `W_r(u)`, `M_3(u)` are evaluated on the field `f_r(u) := f_r^perp + (-r u - mu_w(r)) g_r`. Since `r u <= sqrt r`, the
field `f_r(u)` differs from `f_r^perp - mu_w(r) g_r` by at most `sqrt r ||g_r||_{C^5}` in `C^5(X)`, uniformly in `u`.

*Pointwise limit.* Fix `u > 0`. By 2.1, 2.2 and (1.1), the coordinates of `f_r(u)` converge almost surely:
`v -> v`, `om -> om`, `T`, `tau`, `nu` to finite limits, `M_3(u) -> max(|f_xxx|, |f_xxy|, |f_xyy|, |f_yyy|)(0) = max(12k, 2|v|, |om|, |Y|) = M`
(the supremum of a continuous function over the shrinking square `D_r`, the third partials of `f_r(u)` converging uniformly to
those of the limit field, whose `f_xxx(0)` is pinned at `12k`). By (1.2), `r^(-4) W_r(u) -> (6ku - v^2)(6k(u - om) + v^2)`
on `{6ku > v^2, 6k(om - u) - v^2 < 0}` and to `0` on the complement, except on the null set `{6ku = v^2} cup {6k(u - om) = -v^2}`
(`(v, om)` has a density); `f_xx(M) = r^2 T - 6kr < 0` eventually. With `s = 6ku`, `a = v^2`, `c = 6k om - v^2`, the limit is
`(s - a)(s - c) 1{s > max(a, c)}`. The indicator `1{u <= (4/(3k)) M_3(u)^2}` converges to `1{u <= (4/(3k)) M^2} = 1{s <= 8 M^2}`
for every `u` with `P(u = (4/(3k)) M^2) = 0`, i.e. for all `u` except `u = 192 k` (the atom of `M` at `12k`); a single `u` is
Lebesgue-null. And `p_{w,r}(-ru) -> p_w(0)`.

*Domination.* Let `N_r = 1 + ||f_r^perp||_{C^5(X)} + ||g_r||_{C^5(X)}`. For `r <= 1` and `u <= r^(-1/2)`, all of `|T|, |tau|, |nu|, |v|, |om|`
on `f_r(u)` are bounded by `C N_r` by (1.1), so `r^(-4) W_r(u) <= C (1 + u)^2 N_r^4`, and `M_3(u) <= C N_r`, so
`1{u <= (4/(3k)) M_3(u)^2} <= 1{u <= C N_r^2}`. Therefore the `u`-integrand is bounded by `sup_r sup p_{w,r} . C (1 + u)^2 N_r^4 1{u <= C N_r^2}`,
whose `du`-integral is at most `C N_r^{10}`, with `sup_r E N_r^{10} < infinity` by 2.1. Dominated convergence (in `u` and on the
probability space) gives (2.3), where the limit field is the contact field given `f_yy(0) = 0` and `E` is over the law of 2.2.

**2.5 Conclusion.** `Q^W(G_r^c) = [E_Q(W_r 1_{depth, lambda <= sqrt r}) + o(r^5)] / Z_r = r^3 [p_w(0) E I + o(1)] / [z_0 + o(1)]`, and
`p_w(0) E[I] / z_0 = p_w(0) / (36 k^2 E[w^2 1{w<0}]) . E[I] = R(b) J(k)`, with `J(k) = E[I] / (36 k^2) = (216 k^3)^(-1) E[integral (s-a)(s-c) ds]`.
The lower limit `max(a, c) <= 8 M^2` always: `M >= 2|v|` gives `8 M^2 >= 32 v^2 >= a`, and `M >= max(12k, |om|)` gives
`8 M^2 >= 96 k |om| >= 6k om >= c`. QED.

**Remarks.** (a) `R(b)` for the reference kernel: with `beta = b / sqrt2`, `p_w(0) = phi(beta)/sqrt2` and
`E[w^2 1{w<0}] = (2 + b^2) Phi(beta) + sqrt2 b phi(beta)` (integrate `(sqrt2 t - b)^2 phi(t)` over `t < beta`); `R` is strictly
decreasing on `b >= 0` (numerator decreasing; the denominator's derivative is `2 b Phi(beta) + 2 sqrt2 phi(beta) > 0`).
(b) The leading size of `J`: since `M >= 12k` is forced by the pinned `f_xxx(0)`, `E[F(8M^2)] >= (512/3)(12k)^6 - 8 E[v^4 M^2]`,
and `J(k) = (512/3)(12k)^6 / (216 k^3) (1 + delta(k)) = 2359296 k^3 (1 + delta(k))` with `delta -> 0` as `k` grows (the
free third derivatives `2|v|, |om|, |Y|` rarely exceed `12k`); `delta(k) > 0` for `k <= 3/4` and `|delta(k)| < 2e-6` for
`k >= 1` on the grid (both signs; the term `-8 E[v^4 M^2]` is negative). (c) For the torus kernel in a general frame the
same formula holds with the exact Gaussian laws `w ~ N(mu_w, sigma_w^2)`, `(v, om, Y) ~ N(mu_odd, Sigma_odd)` read off the
derivatives of `K_L(R .)` at 0; these differ from the reference values by `O(L^6 e^{-L^2/2})` (image sums), which is not
enclosed here (section 6). (d) Theorem G is a statement about the sufficient criterion `G_r`, not about the elder pairing:
the actual failure `1 - p_r` is `(alpha_1 + alpha_2) r^3 + o(r^3)` by [S] (S2), and `G_r^c` contains the failure event
([LP] section 8), so `c_G >= alpha_1 + alpha_2` necessarily; the size of the gap is in section 5.

## 3. Reduction of `J(k)` to three one-dimensional integrals

With `F(s) = s^3/3 - (a + c) s^2/2 + a c s`, `integral_{max(a,c)}^{8M^2} (s-a)(s-c) ds = F(8M^2) - F(max(a, c))`. Since `M` depends on
`om` only through `|om|`, and `a + c = 6k om`, `a c = v^2 (6k om - v^2)` are odd in `om` up to the `-v^4` term,
`E[(a + c) M^4] = 0` and `E[a c M^2] = -E[v^4 M^2]`. Hence

    216 k^3 J(k) = (512/3) I1 - 8 I2 - I3,    I1 = E[M^6],   I2 = E[v^4 M^2],   I3 = E[F(max(a, c))].

Write `m = 12k`, `F_1(t) = P(|N(0,2)| <= t) = 2 Phi(t/sqrt2) - 1` (the law of `2|v|` and of `|om|`), `F_3(t) = 2 Phi(t/sqrt6) - 1`
(the law of `|Y|`), `sigma_v^2 = 1/2`.

- `I1 = m^6 + integral_m^infinity 6 t^5 [1 - F_1(t)^2 F_3(t)] dt`  (`P(M > t) = 1 - F_1^2 F_3` for `t >= m`).
- `I2 = H E[v^4 1{|v| <= 6k}] + 4 E[v^6 1{|v| > 6k}] + integral_m^infinity 2t [1 - F_1(t) F_3(t)] E[v^4 1{6k < |v| < t/2}] dt`, where
  `H = m^2 + integral_m^infinity 2t [1 - F_1 F_3] dt = E[max(m, |om|, |Y|)^2]`: condition on `v`; `E[max(m_v, |om|, |Y|)^2] = m_v^2 + integral_{m_v}^infinity 2t (1 - F_1 F_3)`
  with `m_v = max(m, 2|v|)`, and exchange the order of integration on `{2|v| > m}`.
- `I3 = 2 integral_0^infinity G(v) rho_v(v) dv`, where for fixed `v` the `om`-expectation is closed: with `theta = v^2/(3k)`
  (the point `c = a`), `F(max(a,c)) = -(2/3) v^6 + 3k v^4 om` on `{om <= theta}` and `= [3 v^2 c^2 - c^3]/6` on `{om > theta}`, `c = 6k om - v^2`;
  the truncated moments `E[om^j 1{om <= theta}]`, `E[om^j 1{om > theta}]`, `j <= 3`, are `Phi`, `phi` at `theta/sqrt2` times polynomials.

Every remaining integral is one-dimensional with an integrand built from polynomials, `Phi(t/sigma)` and `phi(t/sigma)`.
The truncated Gaussian moments use `M_j(x) = integral_x^infinity u^j phi(u) du`, `M_0 = 1 - Phi`, `M_1 = phi`, `M_j = x^(j-1) phi(x) + (j-1) M_(j-2)`.

## 4. Certification and values

`cap_coefficient.py` (standard library; exact rational interval arithmetic with outward rounding to `2^-160`; `exp(-t)` by the
alternating series in fixed point with an integer rounding budget, `pi` by Machin, `Phi` by the fixed-point series of [Z]).
Each one-dimensional integral over `[m, m + 30]` (in `t`) or `[0, 8]` (in `v`) is enclosed by cells of width `1/512` with the
mean-value bound

    integral_cell f  in  h f(mid) +- (h^2/8) width(f'(cell)),

`f'` obtained by forward-mode interval differentiation (a pair (value, derivative) propagated through `+`, `x`, `Phi`, `phi`, `M_j`);
the tails beyond the ranges are bounded in closed form (`1 - F_1^2 F_3 <= 2(1 - F_1) + (1 - F_3)`, `integral_T^infinity t^5 (1 - Phi(t/sigma)) dt <= (sigma^6/6) M_6(T/sigma)`, and
polynomial majorants of `|F(max(a,c))|` against the incomplete moments of `v`). The enclosures of `I1`, `I2`, `I3` are combined exactly;
`J`, `R` and `c_G` are printed as decimal brackets (rounded outward).

| `k` | `J(k)` | width | `J / (2359296 k^3)` |
|---|---|---|---|
| `1/6` | `[586678.1211613003, 586680.4730695802]` | `2.35190827979` | `[53.71198619, 53.71220152]` |
| `1/2` | `[301744.4364470241, 301744.4616663935]` | `0.025219369345` | `[1.02316771, 1.02316780]` |
| `3/4` | `[995454.6123240485, 995454.6129283207]` | `0.000604272143` | `[1.00012720, 1.00012721]` |
| `1` | `[2359292.9611053703, 2359292.9611122569]` | `0.000006886435` | `[0.99999871, 0.99999872]` |
| `3/2` | `[7962621.6645357431, 7962621.6645378716]` | `0.000002128399` | `[0.99999970, 0.99999971]` |
| `2` | `[18874366.3403946311, 18874366.3403964820]` | `0.000001850785` | `[0.99999991, 0.99999992]` |

| `b` | `R(b)` |
|---|---|
| `0` | `[0.282094791773, 0.282094791774]` |
| `1/4` | `[0.211225157119, 0.211225157120]` |
| `1/2` | `[0.155804629374, 0.155804629375]` |
| `3/4` | `[0.113118131654, 0.113118131655]` |
| `1` | `[0.080766267688, 0.080766267689]` |
| `6/5` | `[0.060913700223, 0.060913700224]` |

`c_G(b, k) = R(b) J(k)` (four decimals, rounded outward):

| `b` \ `k` | `1/6` | `1/2` | `3/4` | `1` | `3/2` | `2` |
|---|---|---|---|---|---|---|
| `0` | `[165498.8424, 165499.5059]` | `[85120.5339, 85120.5411]` | `[280812.5615, 280812.5618]` | `[665544.2565, 665544.2566]` | `[2246214.1004, 2246214.1005]` | `[5324360.4426, 5324360.4427]` |
| `1/4` | `[123921.1783, 123921.6752]` | `[63736.0159, 63736.0214]` | `[210265.0568, 210265.0571]` | `[498342.0264, 498342.0265]` | `[1681906.0121, 1681906.0122]` | `[3986740.9957, 3986740.9958]` |
| `1/2` | `[91407.1672, 91407.5337]` | `[47013.1800, 47013.1841]` | `[155096.4369, 155096.4371]` | `[367588.7653, 367588.7654]` | `[1240613.3172, 1240613.3173]` | `[2940713.6523, 2940713.6524]` |
| `3/4` | `[66363.9329, 66364.1990]` | `[34132.7668, 34132.7698]` | `[112603.9658, 112603.9660]` | `[266878.8117, 266878.8118]` | `[900716.8857, 900716.8858]` | `[2135033.0565, 2135033.0566]` |
| `1` | `[47383.8021, 47383.9922]` | `[24370.7719, 24370.7740]` | `[80399.1536, 80399.1538]` | `[190551.2868, 190551.2869]` | `[643111.2328, 643111.2329]` | `[1524412.1243, 1524412.1244]` |
| `6/5` | `[35736.7352, 35736.8785]` | `[18380.3701, 18380.3717]` | `[60636.8238, 60636.8239]` | `[143713.2641, 143713.2642]` | `[485032.7490, 485032.7491]` | `[1149707.4931, 1149707.4932]` |

**Controls (floating, not part of the certificate).** Monte Carlo of `J(k)` from the definition (`2 x 10^5` samples of
`(v, om, Y)`, seed 2026) and a two-dimensional midpoint quadrature in `(v, om)` with the `Y`-expectation in closed form:
- `k = 1/6`: Monte Carlo `574856.1 +- 7874.9` (`-1.50` s.e. from the certified midpoint), quadrature `586681.402`.
- `k = 1/2`: Monte Carlo `301413.4 +- 238.0` (`-1.39` s.e. from the certified midpoint), quadrature `301744.426`.
- `k = 3/4`: Monte Carlo `995377.2 +- 43.1` (`-1.80` s.e. from the certified midpoint), quadrature `995454.613`.
- `k = 1`: Monte Carlo `2359221.4 +- 58.1` (`-1.23` s.e. from the certified midpoint), quadrature `2359292.961`.
- `k = 3/2`: Monte Carlo `7962462.0 +- 130.8` (`-1.22` s.e. from the certified midpoint), quadrature `7962621.665`.
- `k = 2`: Monte Carlo `18874082.4 +- 232.6` (`-1.22` s.e. from the certified midpoint), quadrature `18874366.340`.

The `--check` mode requires the Monte Carlo value within four standard errors and the quadrature within `3 x 10^-4` of the
certified midpoint, the enclosure widths below `10^-5` relative, `J >= 2359296 k^3` for `k <= 3/4` and `|J / (2359296 k^3) - 1| < 2 x 10^-6`
for `k >= 1`, the closed-form `R(b)` against a floating evaluation, `R` decreasing on the grid, the two headline inequalities,
and the exact arithmetic of [CAP] (3).

## 5. Consequences for `C`, `r_*`, and the size of the cap criterion's slack

1. **Lower bound for every admissible `C`.** If `Q^W(G_r^c) <= C r^3` for all small `r` at `(b, k)`, then `C >= c_G(b, k)`.
   On the band of Math-#195 (`B = [0, 1]`, `K = [1/2, 2]`) the grid maximum is at `(0, 2)`: `C > 5.32 x 10^6`. Since `R` is
   decreasing in `b`, the band maximum over `b` is at `b = 0` for every `k`; the dependence on `k` is `~ k^3`.
2. **Where the cap route can be nontrivial.** `C r^3 < 1` forces `r < c_G(b,k)^{-1/3}`: `5.7 x 10^-3` at `(0, 2)`,
   `3.4 x 10^-2` at `(1, 1/2)` (the band's smallest `c_G` among the grid points), `3.0 x 10^-2` at `(6/5, 1/6)`. Any `r_*`
   for which Theorem A's bound is informative on the band is below `6 x 10^-3` at the band's corner, whatever the proof.
3. **The recorded constant.** [CAP] (2)–(3) give, for the fixed-axis SIDE24 law (`b = 6/5`, `k = 1/6`),
   `C3_new + C4_new/20 < 2.4 x 10^23` (exact rational arithmetic, replayed in `--check`), against `c_G(6/5, 1/6) = 35736.8`:
   a factor above `6 x 10^18` between the recorded and the sharp coefficient. The slack is in the moment bounds
   (`||T||_8 < 320` for a supremum over a set of diameter `<= 6r`, `||M_4||_8 < 340`), not in the geometry.
4. **The criterion against the truth.** The actual elder-pairing failure has coefficient `alpha_1 + alpha_2` ([S] (S2)), and
   by [NUM] `alpha_j = (p_b(0)/z_0) J_j(k)` with the same `b`-factor as `c_G` (`R(b) = 36 k^2 p_b(0)/z_0`), so the ratio is `b`-free:

       c_G / (alpha_1 + alpha_2) = 36 k^2 J(k) / (J_1(k) + J_2(k)),

   with `J_1 + J_2` from [NUM] (GH60: `36.785`, `172.87`, `1112.3` at `k = 1/2, 1, 2`): `7.4 x 10^4`, `4.9 x 10^5`, `2.4 x 10^6`.
   (At `b = 0`: `alpha_1 + alpha_2 = 1.153, 1.355, 2.179` against `c_G = 8.5 x 10^4, 6.7 x 10^5, 5.3 x 10^6`.) The sufficient
   condition `lambda > (4/(3k)) r M_3^2` with `M_3 >= 12k` forced fails whenever `lambda <= 192 k r`, a set of `w`-probability of
   order `192 k r p_w(0)` whose typed weight is of order `(192 k r)^2`, while the actual failure requires the competing saddle
   geometry of [S]; the ratio grows like `k^3 . 36 k^2 / (J_1 + J_2)(k)`.

## 6. What this does not do

Not a proof or a review of [LP] Theorem A, of [CAP], or of [S]: (5.4), (5.5), (7.6)–(7.7), the coupling (4.2) and the
uniform moments (4.1) are consumed as statements; [S] (S2) and the [NUM] values are quoted for comparison only. No upper
bound `C` and no `r_*` are supplied (C8 stays OPEN on both). No rate in the `o(r^3)`. The certified numbers are for the
reference kernel; for the torus kernel `K_L` in a frame `R` the coefficient is the same formula with the exact jet law at 0,
whose deviation from the reference (`O(L^6 e^{-L^2/2})`) is not enclosed here. Planar only (`d = 2`); the same argument in
`d >= 3` would need the eigenvalue boundary layer of [LP] section 7 and is not attempted. Nothing on `p_r` beyond the
comparison in section 5.

## 7. Verification and provenance

`python3 -B -S cap_coefficient.py --check --procs 2` (also `-B -O -S`): recomputes every enclosure and compares the decimal
records exactly with `RESULTS.json`; about four minutes per `k` on one core (`k = 1/6` first, then the others in parallel).
Mutants `no-third-jet` (drop `|Y|` from `M`), `sign-lo` (add `I3` instead of subtracting), `variance-yyy` (`Var Y = 2`) exit 1.
`cap_coefficient.py --procs 4` regenerates `RESULTS.json` (about eight minutes on four cores); `--quick K` certifies one `k`.
Workflow `.github/workflows/c8-cap-failure-coefficient-planar.yml`: manifest, main-resident pins ([LP], [CAP], [NUM], [S]),
both modes, mutants, clean tree.

Author lane Anthropic / Claude, 30 September 2026. Scientific effect NONE. The author will not merge.
