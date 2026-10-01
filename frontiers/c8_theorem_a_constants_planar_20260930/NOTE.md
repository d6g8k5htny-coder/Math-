# Explicit cap-route constants for Theorem A in the plane: `Q^W(G_r^c) <= C r^3` with certified `C`

**Object:** `CL-C8-THEOREM-A-CONSTANTS-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude.
**Kind:** author-side theorem (Theorem E), proved with explicit constants and certified by exact rational interval
arithmetic (standard library only). **Scientific effect:** NONE. Catalog entry C8 (`reviews/candidates_pending_20260928/CANDIDATES.md`:
"explicit finite `C`, `r_*`, `z_*`, `c_{B,K}`, `c_{d,L}` on a declared compact-mark / torus band; OPEN") stays OPEN, and no
catalog edit is made. What this packet supplies, in `d = 2`:
- on the band `B = [0, 1]`, `K = [1/2, 2]`, uniformly over frames and torus sides `L >= 10`, explicit cap-route pairs
  `(C, r_*)` for [LP] (7.8), and therefore for [LP] Theorem A (1.1);
- a normalizer floor `z_*` on `(0, r_*]`;
- (v1.1) the same at the single fixed-axis SIDE24 point `(b, k) = (6/5, 1/6)` of [CAP] section 1 (Theorem E'). There the only
  constant on record, `2.4 x 10^23`, is replaced by `39322.8` for `r <= 1/4096`.

No STATUS, PROOF_INDEX, GRAPH or catalog edit. Same GitHub account as every lane; zero organizational-independence credit.
The author will not merge.

**Sources** (pins in `SOURCE_MAP.json`):
- [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, sections 1, 3, 7 and 8:
  - the model and the law `Q`, `W_r`, `Z_r`;
  - the contact frame (3.1)–(3.3);
  - the good event `G_r`, Theorem A (1.1) and the cap bound (7.8);
  - the §8 implication "on `G_r` the global elder partner of `M` is `S`".
- [CAP] `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md`, section 1: the cylinder `D`, the norms `M_3`, `M_4`
  and condition (1).
- [G] Math-#203 at `a388580`, read-only: Theorem G and the sharp cap coefficient `c_G(0, 2)`, used for the lower-bound sanity
  check and the comparison.
- [Z] Math-#195 at `6e7746b`, read-only: the floor on `[1/64, 1/2]`, comparison only.

Unlike [G], this packet does **not** consume [LP] (4.1), (4.2), (5.4), (5.5) or (7.5)–(7.7). Every estimate below is proved
here with its constant. From [LP] it uses only the definitions, the pins, and (for the consequence on `1 - p_r` alone) the §8
implication.

## 0. Statement

**Setting** ([LP] section 1, `d = 2`; as in [G] section 0):
- The torus `X = (R / L Z)^2` and the kernel
  `K_L(z) = sum_n exp(-|z + Ln|^2/2) / sum_n exp(-|Ln|^2/2)`.
- An orthonormal frame `R` with axial unit vector `u`, and the pins `M = -(r/2) u`, `S = (r/2) u`, `f(M) = b`,
  `f(S) = b - k r^3`, `grad f(M) = grad f(S) = 0`.
- The Gaussian regression law `Q = Q_{r,b,k,R}`, the typed weight `W_r = |det H_M det H_S| 1{H_M < 0, det H_S < 0}`,
  `Z_r = E_Q W_r`, and `dQ^W = (W_r / Z_r) dQ`.
- In frame coordinates `(x, y)`: `D = [-2r, 2r]^2`, `M_j = max_{a + c = j} sup_D |partial_x^a partial_y^c f|`, and the good
  event `G_r = {-f_yy(M) > (4/(3k)) r M_3^2, r M_4 <= 3k/10}` ([LP] section 7, [CAP] (1)).
- Theorem A of [LP] is `0 <= 1 - p_r <= C r^3` ([LP] (1.1)). Its proof bounds the larger probability `Q^W(G_r^c)` in (7.8) and
  uses `1 - p_r <= Q^W(G_r^c)` (§8).
- A **cap-route constant** is any `C` with `Q^W(G_r^c) <= C r^3` for `0 < r <= r_*`. Every cap-route constant is a constant
  for [LP] (1.1); the converse fails (see [G] v1.2, section 5, item 1).

**Theorem E.** Let `B = [0, 1]` and `K = [1/2, 2]`. For every torus side `L >= 10`, every orthonormal frame `R`, every
`b in B`, `k in K`, every `r_*` in the table, and every `0 < r <= r_*`,

    Q^W(G_r^c) <= C(r_*) r^3        and        Z_r / r^2 >= z(r_*).

The same holds for the reference kernel `exp(-|z|^2/2)` on `R^2`, since every enclosure below contains the case
`M_1 = 0`, `Theta = 1` of section 2. The table lists, for each `r_*`:
- `C(r_*)`, an exact rational, with its decimal;
- upper bounds for `C / c_G(0, 2)` and `C r_*^3`, and the floor `z(r_*)`;
- the cell (`r`-band; `b`; `k`) at which the maximum is attained.

| `r_*` | `C(r_*)` | `C / c_G(0,2) <=` | `C r_*^3 <=` | `z(r_*)` | maximizing cell |
|---|---|---|---|---|---|
| `1/4096` | `26776575319/5000 = 5355315.0638` | `1.005814` | `0.0000779301` | `8.995379` | `[31/131072, 1/4096]`; `[0, 1/64]`; `[63/32, 2]` |
| `1/2048` | `53623024479/10000 = 5362302.4479` | `1.007127` | `0.0006242542` | `8.990755` | `[31/65536, 1/2048]`; `[0, 1/64]`; `[63/32, 2]` |
| `1/1024` | `2151134031/400 = 5377835.0775` | `1.010044` | `0.0050084993` | `8.981500` | `[31/32768, 1/1024]`; `[0, 1/64]`; `[63/32, 2]` |
| `1/512` | `54156592391/10000 = 5415659.2391` | `1.017148` | `0.0403498057` | `8.962953` | `[31/16384, 1/512]`; `[0, 1/64]`; `[63/32, 2]` |
| `1/256` | `93707999311/10000 = 9370799.9311` | `1.759987` | `0.5585432012` | `8.921798` | `[15/4096, 1/256]`; `[1/4, 1]`; `[1/2, 1]` |
| `1/128` | `87390113247/250 = 349560452.9880` | `65.653041` | `166.6834130230` | `8.841791` | `[5/1024, 11/2048]`; `[1/4, 1]`; `[1/2, 1]` |
| `1/64` | `14397396179923/10000 = 1439739617.9923` | `270.406115` | `5492.1707839673` | `8.676320` | `[15/1024, 1/64]`; `[1/4, 1]`; `[1/2, 1]` |

`c_G(0, 2)` is replaced by its certified lower end `5324360.4426` ([G]). v1 had `C(1/256) = 34071677.7914`; the Hölder exponents of
section 7 bring it below `16777216 = 256^3`. All other entries are equal to v1's or below them by less than `10^-7`
relative.

**Theorem E' (the SIDE24 point).** The same holds at the single point `(b, k) = (6/5, 1/6)`, for every `L >= 10`, every frame
and the reference kernel. That point lies outside the band (`k < 1/2`). It is the parameter point of the fixed-x-axis
SIDE24 law of [CAP] section 1 (torus side 24, `0 < r <= 1/20`).

| `r_*` | `C'(r_*)` | `C' / c_G(6/5, 1/6) <=` | `C' r_*^3 <=` | `z'(r_*)` |
|---|---|---|---|---|
| `1/4096` | `19661409/500 = 39322.8180` | `1.100348` | `5.8 x 10^-7` | `3.226690` |
| `1/2048` | `215461191/5000 = 43092.2382` | `1.205825` | `5.1 x 10^-6` | `3.222401` |
| `1/1024` | `1604824613/1250 = 1283859.6904` | `35.93` | `0.0012` | `3.213821` |
| `1/512` | `1173169654911/10000 = 117316965.4911` | `3283` | `0.8741` | `3.196649` |
| `1/256`, `1/128` | `815443379659/5000 = 163088675.9318` | `4564` | `> 1` | `3.162091`, `3.092963` |
| `1/64` | `5553365927589/5000 = 1110673185.5178` | `31080` | `> 1` | `2.953979` |

`c_G(6/5, 1/6)` is replaced by its certified lower end `35736.7352` ([G]). The contact value of the floor at this point is
`z_0 = 36 k^2 E[w^2 1{w < 0}] = 3.2310`.

**Corollary (explicit Theorem A on the band).**
- **Explicit pairs.** Since `0 <= 1 - p_r <= Q^W(G_r^c)` ([LP] §8), [LP] (1.1) holds on `B x K`, uniformly over frames and
  `L >= 10`, with every pair `(C(r_*), r_*)` of the table. The pairs that are informative at `r = r_*` (`C r_*^3 < 1`) are those
  with `r_* <= 1/256`. Examples: `(C, r_*) = (5415659.2391, 1/512)`, where the bound at `r = r_*` is below `0.0404`, and
  `(9370799.9311, 1/256)`, where it is below `0.559`.
- **What was missing.** [LP] §16 lists "a numerical `r_*` or `C` on a prescribed band" among the items it does not supply.
  The only explicit constant on record before this packet is [CAP] (2)–(3): `1 - p_elder(r) <= min(1, 2.4 x 10^23 r^3)` for
  the fixed-axis SIDE24 law, nontrivial only below `r = 1.6 x 10^-8`.
- **The SIDE24 law (Theorem E').** For that law, `1 - p_elder(r) <= 39322.8180 r^3` for `r <= 1/4096` and
  `<= 43092.2382 r^3` for `r <= 1/2048`, within `10%` and `21%` of the sharp cap coefficient `c_G(6/5, 1/6) = 35736.8`. The
  bound stays below `1` up to `r = 1/512` (`C' r_*^3 <= 0.874`).
- **Near-optimal for the cap route.** The constants are within `0.6%`–`1.8%` of the smallest possible cap-route constant on
  the band for `r_* <= 1/512`. Every cap-route constant valid for the reference kernel at `(b, k) = (0, 2)` is at least
  `c_G(0, 2) > 5324360.44` ([G] Theorem G, v1.2 section 5 item 1), and this certificate's scope includes the reference kernel.
  This statement concerns the cap route only. The true elder-failure coefficient at `(0, 2)` is
  `alpha_1 + alpha_2 = 2.18` ([G] section 5 from [S]/[NUM]), so the cap criterion overstates the failure rate by about
  `2.4 x 10^6`; this certificate cannot remove that slack.
- **Normalizer floor.** `z(r_*)` is an explicit `z_*` for [LP] (5.5) on `(0, r_*]`. The contact value at the band's
  weakest corner, `(b, k) = (0, 1/2)`, is `36 k^2 E[w^2 1{w < 0}] = 9`, and `z(1/4096) = 8.9954` lies within `0.06%` of it.
  [Z] gives `Z_r / r^2 >= 3.5044` on `[1/64, 1/2]` for `L >= 12`. Together: `Z_r / r^2 >= 3.5044` on all of `(0, 1/2]` for
  `L >= 12`, and `Z_r / r^2 >= 8.6763` on `(0, 1/64]` already for `L >= 10`.

## 1. Coordinates and exact identities

In frame coordinates `M = (-h, 0)`, `S = (h, 0)` with `h = r/2`, and the midpoint is `0`. The six pins are the
preconditioned functionals of [LP] (3.1): `U0 = (f(M) + f(S))/2`, `U1 = (f(S) - f(M))/r`, `U2 = (f_x(S) - f_x(M))/r`,
`U3 = (6/r^2)[f_x(M) + f_x(S) - 2(f(S) - f(M))/r]`, `V0 = (f_y(M) + f_y(S))/2`, `V1 = (f_y(S) - f_y(M))/r`. Under `Q` their
values are exactly `(b - k r^3/2, -k r^2, 0, 12k, 0, 0)` ([LP] (3.3)). The twelve targets are:

    w   = f_yy(M),
    v   = f_xy(M)/r + (f_y(M) - f_y(S))/r^2,
    om  = (f_yy(S) - f_yy(M))/r,
    Y   = f_yyy(0),
    T   = f_xx(M)/r^2 + (4 f_x(M) + 2 f_x(S))/r^3 + 6 (f(M) - f(S))/r^4,
    tau = (f_xx(S) - f_xx(M))/r^3 - 6 (f_x(M) + f_x(S))/r^4 - 12 (f(M) - f(S))/r^5,
    nu  = (f_xy(M) + f_xy(S))/r^2 + 2 (f_y(M) - f_y(S))/r^3,
    X_alpha = partial^alpha f(0),   |alpha| = 4.

Each functional is a sum of terms `c r^p partial_x^a partial_y^e f(x_0 r, 0)` with a common **weight** `a - p`. Since the pins
hold exactly under `Q`, almost surely:

    f_xx(M) = r^2 T - 6kr,   f_xx(S) = r^2 (T + r tau) + 6kr,   f_xy(M) = r v,   f_xy(S) = r (r nu - v),   f_yy(S) = w + r om.   (I1)

Write `lambda = -w`, `c1 = 6k - rT`, `c2 = 6k + rT + r^2 tau` and `e = (r nu - v)^2`. Then `det H_M = r P1` and
`det H_S = -r P2`, with

    P1 = c1 lambda - r v^2,     P2 = c2 (lambda - r om) + r e,                                    (I2)

so `H_M < 0, det H_S < 0` holds exactly when `c1 > 0, P1 > 0, P2 > 0`, and then `W_r = r^2 P1 P2`. (`f_xx(M) = -r c1`.)

## 2. The Gaussian law on an `r`-band (Lemma 1)

**(a) Exact series.** Let `F`, `F'` be functionals of weights `w_F`, `w_F'`, with `w = w_F + w_F'`. For the reference kernel
`G(z) = exp(-|z|^2/2)`,

    Cov(F, F') = sum_gamma h(g_x) h(g_y) pi_gamma r^(g_x - w).

- `h(n) = (d/dt)^n exp(-t^2/2)` at `t = 0`, which is `(-1)^(n/2) (n-1)!!` for even `n` and `0` for odd `n`.
- `pi_gamma` is the exact rational `sum c c' (-1)^(a'+e') (x_0 - x_0')^m / m!`. The sum runs over pairs of terms with
  `g_y = e + e'` and `m = g_x - a - a' >= 0`.
- **Regularity:** `pi_gamma = 0` for every `g_x < w`. This is checked exactly for all 252 ordered pairs of the 18 functionals,
  so no negative power of `r` occurs.

**(b) Truncation at `g_x <= NX = 60`.** For one pair with `A = a + a'`, the `g_x`-th term is at most
`|c c'| |h(g_y)| (g_x^A / g_x!!) r^(g_x - w)`, because `|h(n)|/(n - A)! <= n^A / n!!`. For `r <= 1/64` the terms with
`g_x > 60` therefore sum to at most `2 |c c'| |h(g_y)| 61^A r^(61 - w)`.

**(c) Torus remainder, uniform in `L >= 10`, the frame and `r`.**
- **Decomposition.** `K_L = (G + rho) / Theta` with `rho(z) = sum_{n != 0} G(z + p_n)`, where `p_n` runs over the rotated
  lattice `L R^T Z^2`, and `Theta = 1 + sum_{n != 0} exp(-|p_n|^2/2)`, which lies in `[1, 1 + theta_1(L)]`.
- **Bound on `rho`.** `rho` is entire. On the complex polydisc `{|z_1|, |z_2| <= 1}`:
  - `|exp(-(z + p)^2/2)| <= e exp(-|Re z + p|^2/2)`;
  - at most `8j` lattice points have sup-norm index `j`, each at distance `>= jL`;
  - `|Re z| <= 3/2`.

  Hence `|rho| <= M_1(L) := e sum_{j >= 1} 8j exp(-(jL - 3/2)^2/2)`, independently of the frame.
- **Cauchy estimates** give `|partial^gamma rho(0)| <= g_x! g_y! M_1`.
- **Effect on the covariance.** The regularity in (a) is an identity in the Taylor coefficients of any kernel, so the
  `rho`-part of the covariance is `sum_{g_x >= w} partial^gamma rho(0) pi_gamma r^(g_x - w)`. Using
  `g_x!/(g_x - A)! <= w^A e^(g_x - w)` (valid because `A <= w`: every power `p` is `<= 0`), it is bounded by
  `sum |c c'| g_y! max(w, 1)^A M_1 / (1 - e r)`.
- **Values.** `M_1(10) < 4.46 x 10^-15` and `theta_1(10) < 1.55 x 10^-21`. Both decrease in `L`, so the enclosures computed
  at `L = 10` hold for every `L >= 10`, for every frame, and for the reference kernel (`rho = 0`, `Theta = 1`).
- **Why no `r^-10`.** The remainder is applied to the regular series, not to the raw pin functionals. This removes the
  `r^-10` amplification that forces `L >= 12` in [Z].

**(d) Regression.** Interval Gaussian elimination on the six pins gives, uniformly over `r in [r_0, r_1]` (each power `r^p`
is enclosed by `[r_0^p, r_1^p]`):
- the `Q`-means `mu_F = b alpha_F + k beta_F` of the twelve targets;
- their `Q`-covariance `C`, scaled by `Theta^-1 in [1/(1 + theta_1), 1]`;
- the pin energy `E = v_r^T Sigma_r^-1 v_r = e_bb b^2 + 2 e_bk b k + e_kk k^2`, scaled by `Theta in [1, 1 + theta_1]`.

At contact (reference kernel) these reduce to `w ~ N(-b, 2)`, `v ~ N(0, 1/2)`, `om ~ N(0, 2)`, `Y ~ N(0, 6)` (as in [G]
section 2.2) and `E -> 3b^2/2 + 24 k^2`.

The **regression on `w`**: `beta_F = C(F, w)/C(w, w)` and `F_g = F - beta_F (w - mu_w)`. Then `F_g` is independent of `w`
under `Q`, with mean `mu_F` and covariance `C - C(., w) C(w, .)/C(w, w)`. The `g`-block of `(v, om, Y)` is factored by an
interval Cholesky decomposition with lower-triangular entries `l_ij`.

## 3. Third and fourth derivatives on `D` (Lemmas 2 and 3)

Write `A_alpha = sup_D |partial^alpha f|` for `|alpha| = 4`.

**Lemma 2 (averaging identities).** For every `C^4` function satisfying the pins, and every `z in D`:

    |f_xxx(z)| <= 12k   + r Delta_1,    Delta_1 = (5/2) A_40 + 2 A_31,
    |f_xxy(z)| <= 2|v|  + r Delta_2,    Delta_2 = (5/2) A_31 + 2 A_22,
    |f_xyy(z)| <= |om|  + r Delta_3,    Delta_3 = (5/2) A_22 + 2 A_13,
    |f_yyy(z)| <= |Y|   + r Delta_4,    Delta_4 = 2 A_13 + 2 A_04,

so `M_3 <= max_i (B_i + r Delta_i)` with `B = (12k, 2|v|, |om|, |Y|)`.

*Proof.* Let `g(t) = f(t, 0)` and `q(t) = f_y(t, 0)`.
- **`f_xxx`.** `U3` annihilates quadratics and equals `g'''` on cubics. Its Peano kernel is
  `U3 = integral_{-h}^{h} K(t) g'''(t) dt` with `K(t) = 3(h^2 - t^2)/(4h^3) >= 0` and `integral K = 1`; under `Q`,
  `U3 = 12k`.
- **`f_xxy`.** The pins give `q(+-h) = 0`, so Taylor's formula at `-h` yields
  `-2v = integral_{-h}^{h} (2(h - t)/r^2) q''(t) dt`, an average of `f_xxy(t, 0)` (weights `>= 0` with total `1`).
- **`f_xyy`.** `om = (1/r) integral_{-h}^{h} f_xyy(t, 0) dt`.
- **`f_yyy`.** `Y = f_yyy(0)`.

In each case `|partial^beta f(z) - partial^beta f(t, 0)| <= |z_x - t| A_{beta + e_x} + |z_y| A_{beta + e_y}` along the segment,
which stays in the convex set `D`. Use `|z_x - t| <= 5r/2` and `|z_y| <= 2r` (and `|z_x| <= 2r` for `Y`).

**Lemma 3 (fourth derivatives).**
- **Entire field.** Under `Q` the field is almost surely entire. The torus field is
  `sum_m sqrt(lambda_m)(xi_m cos + eta_m sin)(2 pi m.z/L)` with `lambda_m` decaying like `exp(-2 pi^2 |m|^2/L^2)`, which
  converges on compacts of `C^2`, and the regression adds finitely many entire functions.
- **Taylor bound.** Hence `A_alpha <= |X_alpha| + T_alpha`, where
  `T_alpha = sum_{beta != 0} |partial^(alpha+beta) f(0)| (2r)^|beta| / beta!`.
- **Gaussian bounds.** For every `gamma`, the `Q`-law of `partial^gamma f(0)` is Gaussian with standard deviation at most
  `s_gamma` and `|mean| <= s_gamma sqrt(E)` (Cauchy–Schwarz in the `Sigma_r^-1` inner product), where
  `s_gamma^2 = (2g_x - 1)!!(2g_y - 1)!! + (2g_x)!(2g_y)! M_1` bounds the unconditioned variance.
- **Norm bound.** Therefore `||T_alpha||_p <= S_alpha (sqrt(E) + ||N(0,1)||_p)`, with

      S_alpha(r_1) = sum_{1 <= |beta| <= 24} s_{alpha+beta} (2r_1)^|beta| / beta!  +  2^(|alpha|+1) 26 . 29^8 (4r_1)^25 / (1 - 8r_1).

  The tail term uses `s_gamma <= 2^|gamma| gamma! sqrt(1 + M_1)` and `(alpha+beta)!/beta! <= (n + 4)^4` at `|beta| = n`, and
  requires `4 r_1 <= 1/16`.
- **Dependence on `w`.** The regression coefficient of `partial^gamma f(0)` on `w` is at most `s_gamma / sigma_w`. So
  `A_alpha <= A_alpha^g + B_alpha |w - mu_w|`, with `B_alpha = |beta_{X_alpha}| + S_alpha / sigma_w`, where `A_alpha^g` is the
  same bound for the `w`-independent field. The `g`-part of each jet has the same mean and a smaller variance.

## 4. Regression on `w` and the failure set (Lemma 4)

**The `g`-measurable bound on `M_3`.** By Lemmas 2–3 and the regression,

    M_3 <= max_i (y_i + bar-beta_i |w - mu_w|),

with the `g`-measurable parts

    y_1 = 12k + r Delta_1^g,   y_2 = 2|v_g| + r Delta_2^g,   y_3 = |om_g| + r Delta_3^g,   y_4 = |Y_g| + r Delta_4^g,

and the coefficients

    bar-beta_1 = r((5/2) B_40 + 2 B_31),
    bar-beta_2 = 2|beta_v| + r((5/2) B_31 + 2 B_22),
    bar-beta_3 = |beta_om| + r((5/2) B_22 + 2 B_13),
    bar-beta_4 = |beta_Y| + r(2 B_13 + 2 B_04).

On `lambda >= 0`, `|w - mu_w| <= lambda + |mu_w|`. Put `y_i' = y_i + bar-beta_i |mu_w|`, `a = 4/(3k)` and
`x_i = a r bar-beta_i y_i'`.

**Lemma 4.** If `lambda <= a r M_3^2`, then for some `i`, `lambda <= a r (y_i' + bar-beta_i lambda)^2`. For `x_i <= 1/4` the two
roots of this quadratic satisfy

    lambda_-^(i) <= a r y_i'^2 / (1 - 3 x_i),        lambda_+^(i) >= (1 - 3x_i) / (a r bar-beta_i^2) >= 1 / (4 a r bar-beta_i^2).

*Proof.* `lambda_- = 2 a r y'^2 / (1 - 2x + sqrt(1 - 4x))` and `lambda_+ = (1 - 2x + sqrt(1 - 4x)) / (2 a r bar-beta^2)`.
Then use `sqrt(1 - 4x) >= 1 - 4x`.

**The cover.** Put `X_0 = 1/64` and `kappa = 3/(1 - 3X_0)`, so that `1/(1 - 3x) <= 1 + kappa x` for `x <= X_0`. On the typed
support,

    G_r^c  subset  N  u  F  u  X  u  A,
    N = {lambda <= r U,  x_i <= X_0 for all i},    U = max_i a y_i'^2 (1 + kappa x_i),
    F = {lambda >= lambda_far},  lambda_far = 1/(4 a r bar-beta^2),  bar-beta = max_i bar-beta_i,
    X = {x_i > X_0 for some i},    A = {r M_4 > 3k/10}.

`U` is `g`-measurable, so on `N` the failure is a `lambda`-interval `[0, rU]` that depends only on the `g`-parts.

## 5. The main term

On `N`, every target `F` is bounded by its `g`-measurable majorant `bar-F = |F_g| + |beta_F| (|mu_w| + rU)`.

**Density of `lambda` (v1.1).** Two bounds hold for the density `p` of `lambda` on the failure window `[0, rU]`:
- `p <= bar-p = phi(max(0, mu_w)/sigma_w)/sigma_w`, its supremum on `[0, infinity)`;
- `p(lambda) <= p_0 + lambda L_p`, where:
  - `p_0 = phi(m_0/sigma_hi)/sigma_lo` bounds `p(0)` over the box, with `m_0` the smallest `|mu_w|` in the box (`0` if the
    enclosure of `mu_w` contains `0`);
  - `L_p = 0.24198/sigma_lo^2 >= phi(1)/sigma_w^2 = sup |p'|`.

The second bound matters when `-mu_w = b > 0` is far from `0`: at `b = 6/5` the first gives `0.2821` while `p(0) = 0.1967`. The
term `lambda L_p` costs one more power of `U`. From (I2),

    W_r <= r^2 |c1| lambda (|c2| (lambda + r |om|) + r e)

on the typed support (positive parts; this covers both signs of `c1`, `c2`). Integrating over `lambda = r u in [0, rU]`
gives

    E_Q[W_r 1_N] <= r^5 bar-p E_g[ |bar-c1 bar-c2| (U^3/3 + bar-om U^2/2) + |bar-c1| bar-e U^2/2 ],

and, with the linear density bound, the same integral with one more factor `lambda <= rU`:

    E_Q[W_r 1_N] <= r^5 p_0 E_g[ ... as above ... ] + r^6 L_p E_g[ |bar-c1 bar-c2| (U^4/4 + bar-om U^3/3) + |bar-c1| bar-e U^3/3 ].

The certificate uses the smaller of the two.

**Normalization by `K = 12k`.** Write `U = a K^2 tilde-U` with `a K^2 = 192k`, and
`|c1 c2|/(36k^2) <= 1 + eps`, where `eps <= (2r|T| + r^2|tau|)/(6k) + r|T|(r|T| + r^2|tau|)/(36k^2)`. Then

    E_Q[W_r 1_N] / (36 k^2 r^5)  <=  min( bar-p (A + B + C),  p_0 (A + B + C) + r L_p (A' + B' + C') ),
    A  = (aK^2)^3/3 . E[tilde-U^3 (1 + eps)],   B  = (aK^2)^2/2 . E[bar-om tilde-U^2 (1 + eps)],
    C  = (aK^2)^2/(12k) . E[(1 + r|bar-T|/(6k)) bar-e tilde-U^2],
    A' = (aK^2)^4/4 . E[tilde-U^4 (1 + eps)],   B' = (aK^2)^3/3 . E[bar-om tilde-U^3 (1 + eps)],
    C' = (aK^2)^3/(18k) . E[(1 + r|bar-T|/(6k)) bar-e tilde-U^3].

**Moments of `tilde-U`.** With `tilde-y_i = y_i'/K`, `F_k = 1 + kappa X_0`, `eta_1 = 16 kappa r bar-beta_1` and
`Z_1 = tilde-y_1^2 (1 + eta_1 tilde-y_1)`:
- `tilde-U <= max(Z_1, F_k tilde-y_i^2)` for `i = 2, 3, 4`.
- Since `tilde-y_1 >= 1`,
  `max(Z_1, F_k tilde-y_i^2)^p <= Z_1^p + F_k^p sum_i (tilde-y_i^(2p) - c^(2p))_+` with `c = 1 - kappa X_0/2 <= F_k^(-1/2)`.
- Each `tilde-y_i <= u_i + delta_i` (`i >= 2`), where `u_i` is the half-normal of the `i`-th Cholesky variable and
  `delta_i` collects the means, the off-diagonal Cholesky terms, `bar-beta_i |mu_w|` and `r Delta_i^g`.
- With a parameter `theta > 0`:
  `(u + delta)^n - c^n <= (1 + theta)^(n-1) (u^n - (c(1 - theta))^n)_+ + (1 + 1/theta)^(n-1) delta^n`.
- `E[u^q (u^n - c'^n)_+]` is in closed form through the incomplete Gaussian moments
  `M_j(x) = integral_x^infinity t^j phi(t) dt = x^(j-1) phi(x) + (j - 1) M_(j-2)(x)`.
- `tilde-y_1 = 1 + bar-beta_1 |mu_w|/K + (r/K) Delta_1^g` is expanded binomially.
- The `delta`-terms and every cross term are bounded by Hölder's inequality, with Gaussian `L^p` norms
  (`||N||_p <= ((p - 1)!!)^(1/p)` for `p` a power of two, `||N||_1 <= 4/5`) and the bounds of Lemma 3.

**Parameter choices (v1.1).** Every pair `(X_0, theta)` gives a valid bound. Each box uses the smaller of the bounds for
`(X_0, theta) = (1/64, 1/32)` and `(1/1024, 1/256)`. The second pair matters at small `k`, where the free third derivatives
`2|v|, |om|, |Y|` often exceed `12k`, so the factor `F_k^3 = (1 + kappa X_0)^3` and the split loss `(1 + theta)^5` multiply
the leading term. In v1 these were `1.155` and `1.166`; with the second pair they are `1.009` and `1.020`.

**The factors `bar-om` and `bar-e`.**
- In `bar-om`, the part that shares its Gaussian variable with `u_3` is integrated exactly; the rest goes through Hölder.
- `bar-e = (r |bar-nu| + |bar-v|)^2`. Write `|bar-v| <= v_0 + d_v`, where `v_0 = l_11 |z_1|` is the Cholesky part, the
  variable of `u_2`, and `d_v = |mu_v| + |beta_v| (|mu_w| + rU)`. With `theta_E = 1/16`:

      bar-e <= (1 + theta_E)^2 v_0^2 + (1 + theta_E)(1 + 1/theta_E) d_v^2 + (1 + 1/theta_E) r^2 bar-nu^2.

  The `v_0^2` term is integrated exactly against `u_2`; the rest goes through Hölder.

## 6. The normalizer floor (Lemma 5)

Let `G_0 = {r|T| <= 3k/2, r^2|tau| <= 3k/2}`. On `G_0`:

    c1 >= 9k/2,   3k <= c2 <= 9k,   c1 c2 >= 36k^2 (1 - (2r|T| + r^2|tau|)/(6k)),

and, pointwise,

    W_r / r^2  >=  1_{G_0} { 36k^2 [ lambda_+^2 - r om_+ lambda_+ - ((2r|T| + r^2|tau|)/(6k)) lambda_+^2 ] - r c2 v^2 lambda_+ }.

*Proof.* By (I2), `W_r/r^2 >= 1_{G_0} c2 (c1 lambda - r v^2)_+ (lambda - r om_+)_+`. If `lambda <= r om_+`, the right side
above is at most `0`. Otherwise use `(x - y)_+ z >= xz - yz` and `c1 c2 lambda (lambda - r om_+) >= 36k^2 (1 - ...) lambda (lambda - r om_+)`.

Taking expectations, with Cauchy–Schwarz on `G_0^c` and Hölder on the `T`, `tau` terms:

    Z_r / (36 k^2 r^2)  >=  E[lambda_+^2] - ||lambda||_4^2 P(G_0^c)^(1/2) - (2r||T||_2 + r^2||tau||_2) ||lambda||_4^2/(6k)
                            - r E[|om| lambda_+] - (r/(3k)) E[v^2 lambda_+]

(the certificate uses `1/(3k)` where `c2 <= 9k` would allow `1/(4k)`).
- `E[lambda_+^2] = E[(sigma z + m)_+^2]` is increasing in `m` and `sigma`, so it is evaluated at the lower endpoints.
- `E[|om| lambda_+]` and `E[v^2 lambda_+]` are split by the regression; the `g`-parts are independent of `lambda`.
- `P(G_0^c)` is bounded by Gaussian tails of `T` and `tau`.

The bound of the main term is divided by this floor.

## 7. Rare branches

**Weight bound.** For `q in {2, 4, 8, 16}`, by Hölder,

    ||W_r 1_typed||_q <= r^2 g_1(q) g_2(q),
    g_1(q) = (6k + r||T||_{4q}) ||lambda||_{4q},
    g_2(q) = (6k + r||T||_{4q} + r^2||tau||_{4q})(||lambda||_{4q} + r||om||_{4q}) + r (r||nu||_{4q} + ||v||_{4q})^2.

Then `E_Q[W_r 1_E] <= ||W_r 1_typed||_q P(E)^(1 - 1/q)` for `E = F, X, A`, and each box uses the smallest of the four bounds.
v1 used `q = 2` only. A larger `q` gains when the probabilities are small and loses when they are not, because `||W||_q`
grows with `q`.
- `P(A) <= sum_alpha [P(|X_alpha| > (7/8) t) + P(T_alpha > t/8)]` with `t = 3k/(10r)`: a Gaussian tail plus Markov's
  inequality at `p = 32` with Lemma 3.
- `P(F) <= bar-Phi((lambda_far - |mu_w|)/sigma_w)`.
- `P(X) <= sum_i P(y_i' > X_0/(a r bar-beta_i))`: Markov at `p = 32` on `r Delta_1` for `i = 1`; a Gaussian tail of `u_i`
  plus Markov on `delta_i` for `i >= 2`.

`bar-Phi(x)` is computed from its series for `x <= 12`, and beyond that from Mills' bound `phi(x)/x` with
`e^(-y) <= 40!/y^40`.

## 8. Bands, boxes, and the last band

**Bands.** `(0, 1/64]` is covered by `[0, 2^-29]` and 152 bands. Each octave `[2^-(j+1), 2^-j]` is split into equal
sub-bands:
- 8 sub-bands for `j = 6, 7, 8`;
- 16 for `j = 9, ..., 12`;
- 4 for `j = 13, ..., 28`.

**Per band.** On each band `[r_0, r_1]`:
- the law is enclosed uniformly (Lemma 1);
- every `r`-monotone quantity is taken at its worst endpoint: thresholds and `S_alpha` at `r_1`, the tail divided by `r_0^3`.

**Boxes.** 28 boxes per band:

    b in {[0, 1/64], [1/64, 1/16], [1/16, 1/4], [1/4, 1]},
    k in {[1/2, 1], [1, 3/2], [3/2, 7/4], [7/4, 15/8], [15/8, 31/16], [31/16, 63/32], [63/32, 2]}.

That makes 4284 box bounds. `C(r_*)` is their maximum over the bands with `r_1 <= r_*`, and `z(r_*)` is the minimum over
the same boxes of `36 k_lo^2` times the floor of Lemma 5. The SIDE24 point is evaluated on every band as a degenerate box
`b = 6/5`, `k = 1/6`, which gives `C'(r_*)` and `z'(r_*)` in the same way.

**The last band `[0, R]`, `R = 2^-29`.** The main term does not depend on `r`, and the tail is divided by `(R/2)^3`. This is
justified as follows:
- every Gaussian-tail argument is `>= 3` at `R` (checked), and it at least doubles when `r` halves;
- no tail probability reaches `1` at `R` (checked);
- every Markov piece scales like `r^32` or faster.

So each halving of `r` divides each probability by more than `64`. After the power `1 - 1/q` with `q >= 2` it still divides
each piece by more than `8`, for the `q` chosen at `R`. The tail term over `r^3` therefore attains its supremum over `(0, R]`
on `[R/2, R]`.

## 9. Arithmetic

- **Representation:** exact rationals.
- **Transcendentals:** `exp`, `Phi`, `pi` and `sqrt` are enclosed with outward rounding to `2^-160`, by series with explicit
  remainders (`exp` as a fixed-point series; `pi` from Machin's formula).
- **Upper bounds:** rounded upward to 200 significant bits (dyadic).
- **Square roots of upper bounds:** taken without an absolute rounding floor.
- **Matrices:** interval Gaussian elimination with midpoint pivoting, and an interval Cholesky decomposition whose pivots
  must be positive.

Each failed precondition exits through `require`. Standard library only.

## 10. Controls (floating point; not part of the certificate)

`theorem_a.py --mc R B K N SEED` evaluates `Q^W(G_r^c)/r^3` and `Z_r/r^2` end to end from the definitions:
- the degree-8 jet at `0` is sampled under `Q` for the reference kernel;
- the field near `D` is rebuilt from it;
- `W_r`, `M_3` and `M_4` are evaluated directly (maxima over a `9 x 9` grid of `D`).

Means over seeds, with the standard error of the mean:

| `(r, b, k)` | seeds x samples | `Q^W(G_r^c)/r^3` | `Z_r/r^2` | certified (cell containing the point) |
|---|---|---|---|---|
| `(1/512, 0, 2)` | `4 x 20000` | `4.840e6 +- 0.035e6` | `144.2 +- 0.8` | `C <= 5415659.24`; `Z/r^2 >= 139.21` |
| `(1/1024, 0, 2)` | `6 x 20000` | `5.192e6 +- 0.053e6` | `144.7 +- 0.6` | `C <= 5377835.08`; `Z/r^2 >= 139.37` |
| `(1/512, 0, 1/2)` | `6 x 20000` | `8.74e4 +- 0.19e4` | `9.04 +- 0.04` | cell bound `<= 724033.37` (the cell reaches `k = 1`); `Z/r^2 >= 8.9629` |

The limits as `r -> 0` are `c_G(0, 2) = 5324360.44`, `c_G(0, 1/2) = 85120.5` and `z_0 = 144`, `9`.

Two biases point the same way:
- the grid maxima slightly underestimate `M_3` and `M_4`;
- at finite `r` the density of `lambda` decreases across the failure window (by about `8%` at `r = 1/512`, `(0, 2)`).

Both explain why the finite-`r` estimates at `k = 2` sit below `c_G`, and why the estimate approaches `c_G` as `r` halves.
The certified `C` must exceed `c_G` (it holds as `r -> 0`), and it does by the margins in the table. The controls only check
that no gross error separates the certificate from the definitions.

## 11. What this does not do

- **Proofs and reviews of sources.** Not a proof or a review of [LP]'s proof of Theorem A or of [CAP]. The consequence for
  `1 - p_r` uses [LP] §8, which rests on the deterministic cap theorem of [CAP], as a statement.
- **Scope.** Planar only (`d = 2`); `d >= 3` would need the eigenvalue boundary layer of [LP] section 7. The band
  `b in [0, 1]`, `k in [1/2, 2]`, and the single SIDE24 point `(6/5, 1/6)`. No other `k < 1/2`: a smaller `k` lowers every
  threshold `3k/(10r)` and `12k`, and at the SIDE24 point the tail branches already dominate for `r > 1/2048`.
- **Lower bounds.** No lower bound for the constant of [LP] (1.1) itself (see [G] v1.2).
- **Large `r_*`.** For `r_* >= 1/128` (band) and `r_* >= 1/256` (SIDE24 point) the table values are certified but exceed `1`
  at `r = r_*`. There the tail branches `A` and `X` dominate, and the method stops being informative.
- **Other C8 constants.** `c_{B,K}` and `c_{d,L}` are not addressed (Math-#197 and the SIDE24 coefficient packets).
- **Controls.** The Monte Carlo controls are floating point and are not part of the certificate. There is none at the SIDE24
  point: there the failure probability (`c_G r^3 < 5 x 10^-6` for `r <= 1/2048`) is beyond reach of sampling.
- **C8.** C8 stays OPEN; this packet changes no catalog entry. Nonauthor reads are requested on the PR.

## 12. Verification and provenance

- `python3 -B -S theorem_a.py --check --procs N` (also with `-B -O -S`) replays exactly, and compares with `RESULTS.json`:
  - the parameters, the band list, and 11 sampled bands (the last band and the band ending at each `r_*` among them);
  - both `C` tables as the maxima of the stored records;
  - `C > c_G(0, 2)` and `C' > c_G(6/5, 1/6)` for every `r_*`;
  - the canonical layout of `RESULTS.json` (one line per band record).

  It takes about one minute on four cores.
- `--check-full` replays all 153 bands (about ten minutes on four cores).
- Mutants `no-delta` (drop the fourth-derivative terms of Lemma 2), `cap-half` (halve the cap constant `4/(3k)`),
  `no-zfloor-correction` (drop the corrections of Lemma 5) and `no-om-term` (drop the `om` terms `B`, `B'`) exit 1.
- Without flags, the script regenerates `RESULTS.json` (about ten minutes on four cores).
- Workflow `.github/workflows/c8-theorem-a-constants-planar.yml` checks:
  - the manifest and the main-resident pins ([LP], [CAP]);
  - `--check-full` and `--check` in the two interpreter modes;
  - the four mutants;
  - a clean tree.

**Revisions.** v1 (`f3d41b5`): Theorem E on the band.

v1.1 adds:
- Theorem E' at the fixed-axis SIDE24 point;
- the linear density bound for `lambda` (section 5);
- the per-box choice between two `(X_0, theta)` pairs (section 5);
- the Hölder exponents `q in {2, 4, 8, 16}` for the rare branches (section 7);
- `RESULTS.json` regenerated.

The band constants change only in the last digits, except `C(1/256)`, which drops from `3.41 x 10^7` to `9.37 x 10^6`.

Author lane Anthropic / Claude, 30 September – 1 October 2026. Scientific effect NONE. The author will not merge.
