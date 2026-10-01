# The cap-failure coefficient in every dimension: `c_G^(d) = R_d(b) R(b) J^(d)(k)`, certified in `d = 3`

**Object:** `CL-C8-CAP-FAILURE-COEFFICIENT-DIMS-20261001-v1`. **Author lane:** Anthropic / Claude.

**Kind.** An author-side limit theorem (Theorem G_d, `d >= 3`) and certified enclosures of its coefficient in `d = 3`
(exact rational interval arithmetic; standard library only).

**Scientific effect:** NONE. Catalog entry C8 (`reviews/candidates_pending_20260928/CANDIDATES.md`) stays OPEN.
- This packet supplies no `C` and no `r_*` in `d >= 3`.
- It determines the exact size of the cap-failure probability `Q^W(G_r^c)` that the proof of [LP] Theorem A bounds by
  `C_cap r^3` in [LP] (7.8).
- Hence it gives a lower bound for every cap-route constant `C_cap` in `d >= 3`. It gives none for the constant of [LP]
  (1.1), which bounds the smaller probability `1 - p_r` (Math-#203 v1.2, section 5 item 1).

No STATUS, PROOF_INDEX, GRAPH or catalog edit. Same GitHub account as every lane; zero organizational-independence credit.
The author will not merge. Scope claim: Math-#203 comment 5922724441.

**Sources** (pinned in `SOURCE_MAP.json`):
- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`:
  - section 1 (the model in every `d`);
  - section 3 (the pins (3.1)–(3.4));
  - section 4 (the uniform moments (4.1) and the regression on the transverse Hessian (4.2));
  - section 5 (the limit (5.4) and the floor (5.5));
  - section 6 ((6.2));
  - section 7 ((7.1)–(7.4) and (7.7)).
- [CAP] `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`, section 1: the cylinder `D`, the partial-block
  operator norms `M_3`, `M_4`, and condition (1).
- [SC] `frontiers/spectral_cluster_closure_20260929/PROOF.md`: the spectral change of variables and the constant `c_m` of (8).
- [G] Math-#203 at `a388580`, read-only: the planar Theorem G, the factor `R(b)`, and the certified planar `J(k)`
  (`RESULTS.json`, git blob `e3a8e25a`).
- [HD] Math-#184 at `d37ff5d`, read-only: the hard-direction factor `R_d(b)`, its closed form at `b = 0`, its floating values,
  and Corollary 2 (the elder-failure coefficient in dimension `d`). Used for comparison and identification only.

## 0. Statement

**Setting.** This is the setting of [G] section 0 in dimension `d >= 3`, with `m = d - 1` and coordinates `(x, y)` in
`R x R^m`:
- The pins are `M = (-r/2, 0)` and `S = (r/2, 0)` in the frame `R`; the law is `Q = Q_{r,b,k,R}`.
- The typed weight is `W_r = |det H_M det H_S| 1{H_M < 0, index H_S = m}`, with `Z_r = E_Q W_r` and `dQ^W = (W_r/Z_r) dQ`.
- The cylinder is `D = [-2r, 2r] x ball(0, 2r)`, and `M_j = max_{a+c=j} sup_D ||partial_x^a D_y^c f||_op`.
- The good event is `G_r = {lambda_1 > (4/(3k)) r M_3^2, r M_4 <= 3k/10}`, where `lambda_1 = lambda_min(-D_y^2 f(M))`.

**Theorem G_d.** Fix `d >= 3`, `b`, `k > 0`, `L` and `R`. Then `Q^W(G_r^c) = c_G^(d)(b, k) r^3 + o(r^3)` as `r -> 0`, where
`c_G^(d)` is the spectral integral (3.6) below. For the reference kernel `exp(-|z|^2/2)` (equivalently `L -> infinity`):

    c_G^(d)(b, k) = R_d(b) . R(b) . J^(d)(k),
    R(b)     = phi_2(b) / m_(2,b),                     m_(2,b) = E[w^2 1{w < 0}],  w ~ N(-b, 2)          ([G]),
    R_d(b)   = N_d(b) m_(2,b) / m_(d,b),               m_(d,b) = E[det(A)^2 1{A < 0}],  A = -b I_m + GOE_m   ([HD]),
    J^(d)(k) = (216 k^3)^(-1) E[ integral_{max(a,c)}^{8 M^2} (s - a)(s - c) ds ],
    a = v_1^2,  c = 6k Omega_11 - v_1^2,  M = max(12k, 2||v||, ||Omega||_op, ||Y||_op).

The ingredients:
- `phi_2` is the `N(0, 2)` density.
- `N_d(b) = c_m (2 pi)^(-m(m-1)/4) integral_{0 < h_2 < ... < h_m} prod_j h_j^3 phi_2(h_j - b) prod_{i<j} (h_j - h_i) dh`.
- `GOE_m` has `N(0, 2)` diagonal and `N(0, 1)` off-diagonal entries.
- `(v, Omega, Y)` is the contact law of `(-f_xxy/2, f_xyy, f_yyy)(0)`. It is independent of `A` and invariant under rotations
  of `y` (Lemma 1):
  - `v ~ N(0, I_m/2)`;
  - `Omega ~ GOE_m`;
  - `Y` is the symmetric 3-tensor with independent entries `Y_iii ~ N(0, 6)`, `Y_iij ~ N(0, 2)` and `Y_ijk ~ N(0, 1)`.
- `v_1` and `Omega_11` are the components along any fixed unit vector.
- `||Y||_op = sup_{|u| = 1} |Y[u, u, u]|`.

For `d = 2`, `R_2 = 1` and `J^(2) = J` of [G], so the formula is [G]'s Theorem G.

**Certified values in `d = 3`** (reference kernel; section 4; `RESULTS.json`):

    R_3(0) = (32 + 28 sqrt2)/17 = 4.21164586743803890390...,     R(0) = 1/(2 sqrt(pi)) = 0.28209479177387814347...,

| `k` | `J^(3)(k)` (enclosure) | `J^(3)/(2359296 k^3) - 1` | `c_G^(3)(0, k)` (enclosure) |
|---|---|---|---|
| `1/2` | `[301744.44, 521643.95]`; Monte Carlo `342608 ± 514` | MC `0.1617 ± 0.0017` | `[358497.5, 619756.5]`; MC `4.071e5 ± 0.006e5` |
| `3/4` | `[995454.6123, 1011116.6656]`; Monte Carlo `996547 ± 74` | MC `0.00122 ± 0.00007` | `[1182683.06, 1201290.89]` |
| `1` | `[2359292.9611053702, 2359546.6106262951]` | `[-1.3e-6, 1.1e-4]` | `[2803036.72, 2803338.08]` |
| `3/2` | `[7962621.6645357430, 7962621.6650148570]` | `-2.93e-7` | `[9460258.3334, 9460258.3341]` |
| `2` | `[18874366.3403946310, 18874366.3403964821]` | `-8.79e-8` | `[22424320.655069, 22424320.655072]` |

At the band corner of Math-#195 and #206, `(b, k) = (0, 2)`:

    c_G^(3)(0, 2) in [22424320.655069, 22424320.655072]  =  R_3(0) . c_G^(2)(0, 2) . (1 + O(10^-13)).

**Corollary.**
1. **Lower bound for cap-route constants in `d = 3`.**
   - Every `d = 3` cap-route constant `C_cap` valid at `(0, 2)` (reference kernel) satisfies `C_cap >= 2.2424 x 10^7`.
   - Hence the `d = 3` cap route can be nontrivial only below `r = c_G^(3)(0, 2)^(-1/3) = 3.546 x 10^-3`.
   - In the plane the threshold was `5.73 x 10^-3`.
   - This lower bound says nothing about the constant of [LP] (1.1) itself.
2. **The criterion against the truth.**
   - [HD] Corollary 2 states that the actual `d`-dimensional elder-failure coefficient is `R_d(b) (alpha_1 + alpha_2)^(2)`,
     conditional on its sources.
   - Under that reading the factor `R_d(b)` cancels, and the cap criterion's overstatement of the true failure rate is the
     planar one times `J^(d)/J^(2)`:

         c_G^(d) / (alpha_1 + alpha_2)^(d)  =  [c_G / (alpha_1 + alpha_2)]^(2) . J^(d)(k) / J^(2)(k).

   - In `d = 3` the ratio `J^(3)/J^(2)` is `1 + O(10^-4)` for `k >= 1`, `1.0011` at `k = 3/4` and `1.135` at `k = 1/2`
     (Monte Carlo).
   - At the SIDE24 gap `k = 1/6` it is `5.12 ± 0.03` (Monte Carlo): in `d = 3` the free third derivatives dominate the cap
     criterion at small `k`.
3. **Where the dimension enters.** Dimension enters `c_G^(d)` in two ways:
   - through the hard-direction factor `R_d(b)`, the same factor that multiplies the near cluster coefficients ([HD]);
   - through the norms of the free third-derivative blocks, which matter only when they exceed the pinned `12k`.

## 1. Lemma 1: the contact law (reference kernel)

Given the contact jet `(f, f_x, f_xx, f_xxx, f_y, f_xy)(0) = (b, 0, 0, 12k, 0, 0)` ([LP] (3.4)):
- The transverse Hessian is `A_0 = D_y^2 f(0) = -b I + G` with `G ~ GOE_m`.
- The odd 3-jets are `f_xxy ~ N(0, 2 I)`, `f_xyy ~ GOE_m`, and `f_yyy` with independent entries of variances `6, 2, 1`
  (`iii`, `iij`, `ijk`).
- All of these are mutually independent and have mean `0`. The pinned `f_xxx = 12k` has zero regression coefficient on them.

*Proof.*
- **Covariances.** For the reference kernel, `E[partial^alpha f(0) partial^beta f(0)] = (-1)^|beta| prod_i h(alpha_i + beta_i)`
  with `h(n) = (-1)^(n/2)(n-1)!!` for even `n` and `0` for odd `n`.
- **Parity.** Odd and even total orders are uncorrelated. In each coordinate, the parity classes of the transverse indices
  separate the remaining covariances.
- **Example.** `Cov(f_yiyiyi, f_yi) = -3` and `Var f_yiyiyi = 15`, so the conditional variance is `15 - 9 = 6`; `Var f_yiyjyj = 3`
  conditions to `3 - 1 = 2`; `Var f_y1y2y3 = 1` with no pin correlation; every conditional cross-covariance is `0`.

`cap_coefficient_dims.py` verifies the `d = 3` instance exactly. It solves the `8 x 8` rational pin system and checks all 12
conditional means and all 78 conditional covariances.

For `d = 2` the law restricts to [G] section 2.2 (`v ~ N(0, 1/2)`, `Omega ~ N(0, 2)`, `Y ~ N(0, 6)`). Isotropy holds because
rotations `y -> P y` (`P in O(m)`) fix the pins and preserve the reference kernel; parity holds for every even kernel,
including `K_L`.

**The hard-direction integral at `b = 0`.** Write `-A_0 = B`.
- **Joint density.** The ordered eigenvalues of `B` in `d = 3` have joint density
  `(1/(4 sqrt(2 pi))) (lambda_2 - lambda_1) exp(-((lambda_1 - b)^2 + (lambda_2 - b)^2)/4)` on `lambda_1 < lambda_2`. This is the
  `GOE_2` density times the Jacobian `|lambda_2 - lambda_1|` of `(x, y, z) -> (lambda_1, lambda_2, phi)`, which has determinant
  `(cos^2 + sin^2)^2 = 1` times the gap, and `phi in [0, pi)`.
- **`m_(3,0)`.** In polar coordinates on `0 < lambda_1 < lambda_2`,

      m_(3,0) = (1/(4 sqrt(2 pi))) . integral_0^inf rho^6 e^(-rho^2/4) drho . integral_{pi/4}^{pi/2} cos^2 sin^2 (sin - cos) dtheta
              = (1/(4 sqrt(2 pi))) . 120 sqrt(pi) . (7/(30 sqrt2) - 2/15)  =  (7 - 4 sqrt2)/2.

- **`N_3(0)`.** `N_3(0) = sqrt(pi/2) integral_0^inf h^3 phi_2(h) dh = sqrt(pi/2) . (1/2) E|N(0, 2)|^3 = 2 sqrt2`.
- **Result.** With `m_(2,0) = 1`, `R_3(0) = 2 sqrt2 / ((7 - 4 sqrt2)/2) = (32 + 28 sqrt2)/17`, which agrees with [HD] (3).

## 2. The `d`-dimensional weight near the soft eigenvalue

Let `-D_y^2 f(M) = O diag(lambda_1, lambda) O^T` with `lambda = (lambda_2, ..., lambda_m)` ordered and `O in O(m)`. In the frame
`O`, write `v_1 = v . O e_1` and `Omega_11 = (O e_1)^T Omega' (O e_1)`, where
`Omega' = (D_y^2 f(S) - D_y^2 f(M))/r -> Omega`.

The pins give, exactly, the `d`-dimensional versions of [G] (1.1):

    f_xx(M) = r^2 T - 6kr,   f_xx(S) = r^2 (T + r tau) + 6kr,   f_xy(M) = r v,   f_xy(S) = r (r nu - v).

**`H_M`.** By the Schur complement on `A_M = D_y^2 f(M)`, with `lambda_1 = r u`,

    det H_M = det(A_M) (f_xx(M) - f_xy(M)^T A_M^(-1) f_xy(M))
            = (-1)^m r u prod_j lambda_j . (-r c1 + r v_1^2/u + r^2 sum_{j>=2} v_j^2/lambda_j)
            = (-1)^(m+1) r^2 prod_j lambda_j (c1 u - v_1^2 - r u sum_{j>=2} v_j^2/lambda_j),         c1 = 6k - rT.

**`H_S`.** With `A_S = A_M + r Omega'`:
- The soft eigenvalue of `A_S` is `-r(u - Omega'_11) + O(r^2/lambda_2)`.
- `det(A_S) = (-1)^m r (u - Omega'_11) prod_j lambda_j (1 + O(r/lambda_2))`.
- `det H_S = (-1)^m r^2 prod_j lambda_j (c2 (u - Omega'_11) + (r nu - v)_1^2) + O(r^3)`, with `c2 = 6k + rT + r^2 tau`.

**Limit.** On the typed support, therefore,

    W_r / r^4  ->  prod_{j>=2} lambda_j^2 . (6ku - v_1^2)(6k(u - Omega_11) + v_1^2)                          (2.1)

pointwise along the coupling. In `s = 6ku` this is `prod_j lambda_j^2 (s - a)(s - c)`, the planar form [G] (1.2) times
`prod_j lambda_j^2`.

## 3. Proof of Theorem G_d

Steps 1–3 follow [G] section 2 line by line. The new ingredients are the regression on the whole transverse Hessian
([LP] (4.2)), the spectral change of variables ([SC] (8)), and the near-corank strip, which [LP] section 7 controls.

**3.1 Regression on the transverse Hessian.**
- By [LP] (4.2), `f = mu_r + B_r . (A_r - E A_r) + g_r`, where `A_r = D_y^2 f(M)` and `g_r` is independent of `A_r`.
- Under the regression coupling ([G] 2.1), `g_r` and the coefficients converge in every `C^q` norm.
- The Gaussian density `p_{A,r}` of `A_r` on `Sym_m` converges with its derivatives to `p_{A,0}`, the law of `A_0` in
  Lemma 1 ([LP] section 3).
- All moments are uniform ([LP] (4.1)).

**3.2 Negligible parts.**
- **(i) The fourth-derivative branch.** `Q^W(r M_4 > 3k/10) = O(r^p)` for every `p`: Markov on
  `E_Q[(W_r/r^2) M_4^p]` with the floor (5.5), as [LP] (7.7).
- **(ii) The depth branch with `lambda_1 > sqrt r`.** It forces `M_3 >= (3k/4)^(1/2) r^(-1/4)`, which has mass `O(r^(p/4))`.
- **(iii) The near-corank strip** `{lambda_1 <= (4/(3k)) r M_3^2, lambda_2 <= eta}`.
  - Use [LP] (6.2), the inclusion (7.1) `lambda_1 <= D r U^2`, the eigenvalue-measure bound (7.2) and the integration (7.3).
  - These give the integral (7.4) with `lambda_2` restricted to `[0, eta]`.
  - Since `m >= 2`, the integrand of (7.4) is bounded by an integrable function of `(J_r, lambda_3, ..., lambda_m)`, uniformly
    for `lambda_2` in `[0, 1]`. The `lambda_2`-integral over `[0, eta]` is therefore at most `C eta`.
  - Dividing by `Z_r >= z_* r^2` gives a contribution of at most `C eta r^3`.

**3.3 Spectral coordinates.** On `{lambda_1 <= sqrt r, lambda_2 >= eta}`, use [SC] (8) with normalized Haar `dO` and
`lambda_1 = r u`:

    E_Q[W_r 1{depth failure}] = r c_m integral_0^{r^(-1/2)} du integral_{lambda_2 >= eta} dlambda integral dO
        p_{A,r}(-O diag(r u, lambda) O^T) prod_{j>=2}(lambda_j - r u) prod_{2<=i<j}(lambda_j - lambda_i)
        E[ W_r 1{u <= (4/(3k)) M_3^2} | A_r = -O diag(r u, lambda) O^T ].                                (3.1)

**3.4 Pointwise limit.**
- **Weight.** For fixed `(u, lambda, O)`, (2.1) gives the limit of `W_r/r^4`.
- **`M_3`.** `M_3(u) -> M = max(12k, 2||v||, ||Omega||_op, ||Y||_op)`. The block norms are continuous, the cylinder shrinks
  to `0`, and the third partials converge uniformly; at the limit `partial_x^3 f(0) = 12k`, `partial_x^2 D_y f(0) = -2v`,
  `partial_x D_y^2 f(0) = Omega` and `D_y^3 f(0) = Y`.
- **Indicator.** `1{u <= (4/(3k)) M_3^2} -> 1{s <= 8M^2}` off a null set.
- **Remaining factors.** `p_{A,r} -> p_{A,0}` and `prod (lambda_j - r u) -> prod lambda_j`.

**3.5 Domination.**
- **Weight.** By [LP] (6.2) and (7.1), `W_r/r^4 <= C U^(2m) u (u + E U)` on `u <= D U^2`, with `U = J_r + Lambda`.
- **Eigenvalue measure.** (7.2) bounds it by `C exp(-c sum lambda_j^2) Lambda^(m(m-1)/2)`.
- **Integrability.** `J_r` is independent of `A_r` with uniform moments. The majorant of (3.1) is therefore integrable
  uniformly in `r` (this is (7.4)), and dominated convergence applies in `(u, lambda, O)` and on the probability space.

**3.6 Conclusion.** `Z_r/r^2 -> z_0^(d) = (6k)^2 E[det(A_0)^2 1{A_0 < 0}]` ([LP] (5.4)). Letting `r -> 0` and then `eta -> 0`
(by 3.2(iii) and monotone convergence),

    c_G^(d) = (c_m / z_0^(d)) integral dlambda integral dO  p_{A,0}(-O diag(0, lambda) O^T) prod_j lambda_j^3 prod_{i<j}(lambda_j - lambda_i)
                 . E[ integral_{max(a_O, c_O)}^{8M^2} (s - a_O)(s - c_O) ds / (6k) | A_0 = -O diag(0, lambda) O^T ].   (3.6)

Here the typed constraints are `s > a` (`det H_M` sign) and `s > c` (index of `H_S`), and `s <= 8M^2` is the depth failure.

**3.7 The reference kernel.**
- **Independence and invariance.** By Lemma 1, `(v, Omega, Y)` is independent of `A_0`, and its law is invariant under
  `y -> P y`. The inner expectation in (3.6) therefore equals `E[integral ...]/(6k)`, independent of `(lambda, O)`.
- **Density on the boundary.** The density of `-A_0 = b I + G` at `diag(0, lambda)` is
  `(2 pi)^(-m(m-1)/4) phi_2(b) prod_j phi_2(lambda_j - b)`, since the `GOE_m` normalization is `(4 pi)^(-m/2)(2 pi)^(-m(m-1)/4)`.
- **Hard integral.** Hence the hard integral of (3.6) is `phi_2(b) N_d(b)`.
- **Assembly.** `c_G^(d) = phi_2(b) N_d(b) E[...]/(6k . 36 k^2 m_(d,b)) = R(b) R_d(b) J^(d)(k)`. QED.

For the torus kernel `K_L` in a frame `R`, (3.6) holds with the exact torus laws. Parity still gives independence from
`A_0`, but the inner expectation can depend on `O`. The deviation from the reference value is of order `L^q e^(-L^2/2)` and is
**not enclosed here**. Every number in this packet is a reference-kernel value.

## 4. Certified `J^(3)(k)` and `c_G^(3)(0, k)`

Throughout, `P(s) = integral_0^s (x - a)(x - c) dx`, so `216 k^3 J^(d)(k) = E[P(8 M_d^2) - P(m_0)]` with `m_0 = max(a, c)`. Let
`t = 12k`.

**(a) Monotone coupling.** Realize `d = 2` and `d = 3` on one space, the planar variables being `(v_1, Omega_11, Y_111)`.
- **Domination.** `M_3 >= M_2`, since each block norm dominates its `(1,1)` component.
- **Monotonicity.** `dP(8M^2)/dM = 16 M (8M^2 - a)(8M^2 - c) >= 0` for `8M^2 >= m_0`. Hence `J^(2)(k) <= J^(3)(k)`.
- **The difference.** `F(M_3) - F(M_2) = integral_{8M_2^2}^{8M_3^2} (x - a)(x - c) dx` vanishes unless `X_3 > t`, where
  `X_3 = max(2||v||, ||Omega||_op, ||Y||_op)`. It is at most `[(8 Xbar^2)^3/3 + Q (8 Xbar^2)^2 + Q^2 8 Xbar^2] 1{Xbar > t}`, with:
  - `Q = 2 v_1^2 + 6k|Omega_11|`, which dominates `a`, `|c|` and `m_0`;
  - `Xbar = max(Z_v, Z_Om, Z_Y)`, built from:
    - `Z_v = 2||v||`, with `Z_v^2 ~ 2 chi^2_2`;
    - `Z_Om = ||Omega||_F >= ||Omega||_op`, with `Z_Om^2 ~ 2 chi^2_3`;
    - `Z_Y = (Y_111^2 + 3 Y_112^2 + 3 Y_122^2 + Y_222^2)^(1/2) >= ||Y||_op`, with `Z_Y^2 ~ 6 chi^2_4`.

  The last inequality is Cauchy–Schwarz with the weights `binom(3, j)`.
- **Tail bound.** `Xbar^p 1{Xbar > t} <= sum Z_i^p 1{Z_i > t}`. Each `E[Q^j Z_i^p 1{Z_i > t}]` is expanded binomially and
  evaluated in closed form:
  - incomplete gamma functions, `e^(-x) x^j` sums for even degrees of freedom and `erfc` plus such sums for `chi^2_3`;
  - the Gaussian absolute moments of `v_1` and `Omega_11`.
- **Enclosure.** Thus `J^(3)(k) in [J^(2)_lo(k), J^(2)_hi(k) + T_hi^(3)(k)/(216 k^3)]`. This uses [G]'s certified planar
  enclosure, which is the only consumed numerical input.

**(b) Self-contained bracket.** Independently of [G]:

    216 k^3 J^(d)(k) = 512 t^6/3 - 6 t^2 - E[P(m_0)] + T^(d)
    (E[a + c] = 0, E[ac] = -E v_1^4 = -3/4),
    |E[P(m_0)]| <= 2 E[Q^3],
    -2 E[Q^6]/(8t^2)^3 <= T^(d) <= T_hi^(d).

The `d = 2` bracket contains [G]'s certified `J(k)` at every grid `k`; `--check` requires this.
- At `k = 2` the self-contained bracket has relative width `1.1e-6`.
- The coupling enclosure (a) has relative width `1e-13` at `k = 2`, `6e-11` at `3/2`, `1.1e-4` at `1` and `1.6%` at `3/4`.
- At `k = 1/2` the `chi^2` tails are not small (`12k = 6`), and only the lower bound and the Monte Carlo value are informative.

**(c) Values.** `c_G^(3)(0, k) = R_3(0) R(0) J^(3)(k)` with the exact `R_3(0)` and `R(0)` of section 1; the table is in
section 0. Floating `R_3(b) R(b)` from the closed-form inner integral and a Simpson `rho`-quadrature (`RESULTS.json`,
`controls`):

| `b` | `0` | `1/4` | `1/2` | `3/4` | `1` |
|---|---|---|---|---|---|
| `R_3(b)` | `4.2116458674` | `4.3013489393` | `4.3990369319` | `4.5051585717` | `4.6201205312` |
| `R_3(b) R(b)` | `1.188083364` | `0.908553106` | `0.685390319` | `0.509615120` | `0.373149892` |

`R_3(0)` and `R_3(1)` agree with [HD] to `1e-10`. `R_3(b) R(b)` decreases on the grid, so the band corner `b = 0` carries
the largest value among the grid points. Monotonicity in `b` is not proved here.

## 5. Monte Carlo controls (floating; not part of the certificate)

`200000` samples per seed, two seeds, the laws of Lemma 1 (`RESULTS.json`, `controls.mc`):

| `k` | `J^(2)/(2359296 k^3)` | `J^(3)/(2359296 k^3)` | ratio `J^(3)/J^(2)` |
|---|---|---|---|
| `1/6` | `52.67 ± 0.51` (certified [G]: `53.712`) | `275.02 ± 1.44` | `5.12 ± 0.03` |
| `1/2` | `1.0220 ± 0.0006` (certified: `1.0231677`) | `1.1617 ± 0.0018` | `1.135 ± 0.002` |
| `3/4` | `1.00010 ± 0.00003` (certified: `1.0001272`) | `1.00122 ± 0.00007` | `1.0011 ± 0.0001` |

- **Agreement with the certificate.** The `d = 3` values at `k = 3/4` lie inside the certified enclosure (`--check` tests
  this). At `k = 1/2` the Monte Carlo value lies inside the certified bracket.
- **Planar values.** These fall within `2.1` standard errors of [G]'s certified values. A further planar run at `k = 1/2`
  (`4 x 500000` samples, fresh seeds `101`–`404`) gives `1.02363 ± 0.00031`, `1.5` standard errors above the certified
  `1.0231677`. No bias is apparent.
- **`||Y||_op`.** It is computed by a 64-point scan of the circle followed by golden-section refinement.

## 6. What this does not do

- **Sources.** Not a proof or review of [LP], [CAP], [SC], [G] or [HD]. Their cited statements are consumed as such, and the
  enclosure 4(a) uses [G]'s certified planar `J(k)`.
- **Constants.** No upper bound `C` or `C_cap` and no `r_*` in `d >= 3` (C8 stays OPEN), no lower bound for the constant of
  [LP] (1.1), and no rate in the `o(r^3)`.
- **Kernel.** Reference kernel only: the finite-torus deviation is not enclosed.
- **Values.** Certified values in `d = 3` only; for `d >= 4` the formula is stated and not evaluated. `R_3(b)` for `b != 0`
  is floating, as are the Monte Carlo values.
- **Comparison.** The comparison of Corollary item 2 inherits [HD] Corollary 2's conditional status.

## 7. Verification and provenance

- `python3 -B -S cap_coefficient_dims.py --check` (also `-B -O -S`) checks, in about one second:
  - Lemma 1 exactly;
  - the closed form of `m_(3,0)` against its polar evaluation;
  - every certified enclosure against `RESULTS.json` (exact decimal strings), and the containment of [G]'s planar `J(k)` in the
    `d = 2` bracket;
  - the recorded `d = 3` Monte Carlo at `k = 3/4` against the enclosure.
- Mutants exit 1:
  - `no-y-tail` drops the `Y`-block tail;
  - `r3-one` sets `R_3 = 1`;
  - `no-bp` drops `E[P(m_0)]`;
  - `frob-omega-off` replaces the Frobenius `chi^2_3` by `chi^2_1`.
- `--controls --procs N` recomputes the floating controls (a few minutes). Without `--controls`, the script regenerates the
  certified part and keeps the recorded controls.
- Workflow `.github/workflows/c8-cap-failure-coefficient-dims.yml` checks the manifest, the main-resident pins ([LP], [CAP],
  [SC]), both modes, the four mutants, and a clean tree.

Author lane Anthropic / Claude, 1 October 2026. Scientific effect NONE. The author will not merge.
