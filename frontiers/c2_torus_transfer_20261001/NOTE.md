# The third-order coefficient `c2` on the finite torus: transfer for every `L >= 10`, `d = 1, 2, 3`

**Object:** CL-C2-TORUS-TRANSFER-20261001-v1.
**Author:** Anthropic Claude (Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`), 1 October 2026. Author of the
reference packet `frontiers/c2_exact_20261001` ([C2X]).
**Scope claim:** Math-#223 comment 5934236720. The task was posted in Math-#223 comment 5933574379 (with the finite-part
starting inequality used in Lemma F) and listed as unsupplied in main#229 (5933485698).
**Disposition:** author-side. An explicit bound for every real `L >= L0`, every orthonormal frame and `d = 1, 2, 3` on
the difference between the coefficient `c2` of the normalized periodic Gaussian kernel and its closed-form reference value.
It is certified in exact rational ball arithmetic with the standard library. There is also one structural lemma
(Lemma E) valid for every stationary kernel.
**Scientific effect:** NONE. No `STATUS`, `PROOF_INDEX`, `GRAPH`, claim, catalog, prize or source-body change. Same GitHub
account as every lane; zero organizational-independence credit. Nothing in `frontiers/c2_exact_20261001/` or in
Math-#216, #218, #220 or #224 is touched.
**Delivered under:** Dylan Roy's explicit instructions in this session, given after the 2026-09-27 owner stop (quoted in
`SOURCE_MAP.json`, `delivered_under`). `OWNER_STOP.md` addresses Cursor agents and automations and is untouched.

## 0. Statement

**The torus.** This is the field of [SIDE24] (1)–(2) and Math-#224 (T1), for any real side `L` and any `d`:

    K_L(z) = sum_{n in Z^d} phi(z + L n) / sum_{n in Z^d} phi(L n),        phi(z) = exp(-|z|^2/2).

Fix an orthonormal frame with axial vector `u`. The pins sit at `M = -r u/2` and `S = r u/2`. Let `A~_r^{K,u}(b, k)` be the
fixed-cone surrogate of the two-point kernel of [R] §§2–4 for the covariance `K` in this frame, exactly as in [C2X] §1.
Its fold expansion is `A~_r = A_0 + r^2 A_2 + O(r^3)` (§3). Put

    F^u_K(k) = integral_R A_2^{K,u}(b, k) db,
    T(F) = f.p. integral_0^oo F(k) k^(-4/3) dk = integral_0^oo [F(k) - F(0)] k^(-4/3) dk,
    c2[K, u] = (1/3) |S^(d-1)| T(F^u_K),       c2[K] = (1/3) integral_(S^(d-1)) T(F^u_K) d sigma(u).

`c2[K]` is the expression of Math-#218 (0.1). For `K = phi` it does not depend on `u` and equals the closed form of [C2X]
§0. #218's Theorem T, which identifies this expression as a coefficient of the candidate density, is an unmerged
author-side candidate for `d >= 2`. In `d = 1` the theorem below is a transfer of the explicitly defined fixed-cone
expression, not an extension of #218's density theorem (review 5383099127, item 3).

**Theorem C2T.** For `d in {1, 2, 3}`, every `L0` in the table, every real `L >= L0` and every orthonormal frame,

    |c2[K_L, u] - c2[phi]| <= eps_d(L0),   hence   |c2[K_L] - c2[phi]| <= eps_d(L0),

with these values (rounded up):

| `d` | `L >= 10` | `L >= 12` | `L >= 16` | `L >= 24` |
|---|---|---|---|---|
| `1` | `1.41035e-13` | `1.42699e-22` | `5.66439e-46` | `4.09547e-114` |
| `2` | `2.09404e-12` | `2.02307e-21` | `7.57841e-45` | `5.20139e-113` |
| `3` | `1.00039e-10` | `9.20576e-20` | `3.23748e-43` | `2.09418e-111` |

**Relative to `c2[phi]`** (using the lower endpoints of [C2X]'s enclosures), the error is below:
- `6.2e-13`, `9.5e-12` and `6.3e-10` for `L >= 10`;
- `1.8e-113`, `2.4e-112` and `1.3e-110` for `L >= 24`.

**Corollary (SIDE24).** [C2X] widened its published enclosures by `1e-14` relative beyond the certified enclosure (§5
there). That margin is much larger than `eps_d(24) <= 2.1e-111`, so the published intervals contain the torus values as
they stand:
- `c2[K_24] in [0.2215244106266632, 0.2215244106267110]` in `d = 2`;
- `c2[K_24] in [0.1612340491269447, 0.1612340491269810]` in `d = 3`.

With [SIDE24]'s enclosures of `c_{d,24}`, the interval quotients give
`c2[K_24]/c_{2,24} in [3.017759261945395, 3.017759261946047]` and
`c2[K_24]/c_{3,24} in [3.859496174547459, 3.859496174548329]`.

**Three-term law, with its sources.** The law is `nu/(c ell^(-1/3)) - 1 = (c1/c) ell^(7/12) + (c2/c) ell^(2/3) + ...`.
On the SIDE24 torus in `d = 3` its coefficients are `-5.071062...` and `3.859496174548...`, to the stated digits. The sources
of each piece are:
- **`c1/c`** comes from [CU] (Math-#219, an unmerged author-side certificate). It is consumed, not accepted here.
- **Math-#224** plays two separate roles:
  - its (T1) defines the torus kernel used throughout;
  - its `c1` transfer is a separate unmerged author-side candidate, and nothing here inherits status from it.
- **The identification as density coefficients** is conditional on the chain in §8.

**Lemma E (no `r^1` term for every stationary kernel).** Let `K` be any smooth stationary covariance (no isotropy or
evenness needed) whose pin and transverse covariances are nondegenerate at `r = 0`. Then `A~_r(b, k)` is smooth in `r` up
to `r = 0`, and at fixed `v_1 = b - k r^3/2` its Taylor expansion in `r` contains only even powers: for every `N`,
`A~_r(b, k) = sum_{j<N} r^(2j) a_j(b - k r^3/2, k) + O(r^(2N))`. If `K` is moreover real-analytic, as the Gaussian `phi`
and the torus kernels `K_L` are, then `A~_r(b, k) = Atilde(r^2, b - k r^3/2, k)` exactly near `r = 0`, with `Atilde`
real-analytic. In either case

    A~_r = A_0 + r^2 A_2 - (k/2) r^3 d_b A_0 + O(r^4):

there is no `r^1` term, and the `r^3` coefficient is `-(k/2) d_b A_0`. (v1.3: smoothness alone does not give analyticity.
A smooth positive-spectrum covariance can have a Taylor series of radius zero, for example spectral density
`exp(-sqrt|xi|)`; 5938497821.)

On the torus this decides, for the surrogate, the question left open in Math-#227 ("whether the torus `A_r` has an `r^1` term
at all"): it has none. With the consumed comparison `A_r = A~_r + O(r^3)`, the typed `A_r` has none either. This does not
remove #227's certified `beta r` allowance, accept #227's premises, or close C8 ([L'], cited only).

**Relation to Math-#232** ([FJ], merged at `7fe06b0`). #232 gives the general eight-jet local stability interface (a
birth-marginalized finite-jet formula with an analytic budget, `< 1e-60` for `L >= 24`). This packet gives sharper
torus-specific constants for every `L >= 10`, together with Lemma E. The two are compatible, and neither supersedes the other.

## 1. What is consumed, and how the proof runs

- **[C2X] §§1–2 (main, `f9ebba1`).** The pin rows, the target `v_r`, the fixed-cone surrogate and its exact series derivation.
  `exact.py` and `pseries.py` are carried as byte-identical copies, and this packet's pipeline is a re-implementation over balls
  that `reference_checks` compares with them identically (§3).
- **[SIDE24] (1)–(2) (main).** The normalized periodic kernel.
- **[T] (Math-#218, unmerged) (0.1) and Lemma F.** The definition of `c2`, and its identification as the `ell^(1/3)`
  coefficient of the candidate density for `d >= 2` (an author-side candidate). Consumed, not reviewed.
- **[CU] (Math-#219, unmerged).** The certified `c1/c` enclosure quoted in §0. Consumed, not accepted.
- **[D] §2.2 (Math-#216, unmerged).** `A_r = A~_r + O(r^3)`; consumed, as in [C2X].

**The route.**
1. The jet covariances of `K_L` lie in explicit balls around those of `phi` (Lemma J).
2. The exact derivation of [C2X], run in ball arithmetic, encloses the coefficients of the `A_2`-integrand
   `kappa e^(-E(b, k, x)) H(b, k, x)` of `K_L` (Lemma P).
3. The finite part is controlled additively by `Delta(0)`, a weighted integral of `Delta'` and an integral of `|Delta|`
   (Lemma F).
4. Each of these is bounded by explicit absolute Gaussian moments (Lemma G).

There is no multiplicative sandwich: `A_2` is signed, and `c2` is a finite part.

## 2. Lemma J: the jets of `K_L`

`Cov(d^a f(0), d^b f(0)) = (-1)^|b| d^(a+b) K(0)` in the frame coordinates. `K_L` is even, so `d^g K_L(0) = 0` exactly when
`|g|` is odd. For even `|g|`, write `delta = sum_(n != 0) phi(. + p_n)` with `p_n = L R n` (`R` the frame rotation) and
`theta_1 = sum_(n != 0) phi(L n)`. Then

    d^g K_L(0) - d^g phi(0) = [d^g delta(0) - theta_1 d^g phi(0)] / (1 + theta_1),
    |d^g delta(0)| <= sum_(n != 0) prod_i |He_(g_i)(p_(n,i))| phi(p_n) <= sum_(n != 0) prod_i He*_(g_i)(L |n|) e^(-L^2 |n|^2 / 2).

Here `d^m e^(-t^2/2) = (-1)^m He_m(t) e^(-t^2/2)`, `He*_m(s) = sum_j m!/(j!(m-2j)! 2^j) s^(m-2j)` majorizes `|He_m|` on
`|t| <= s` and is nondecreasing, and `|p_(n,i)| <= |p_n| = L|n|` in every frame.

- **Shells `|n|^2 <= 4`** are enumerated exactly; every such `n` has `|n_i| <= 2`.
- **The tail `|n|^2 = s >= 5`** uses `#{n : |n|^2 = s} <= (3 sqrt s)^d` and `He*_m(t) <= (t + m)^m <= (2t)^m` for
  `m <= t`, with `|g| <= L sqrt5`. The `s`-th term is at most `3^d (2L)^|g| s^a e^(-L^2 s/2)`, where `a = (d + |g|)/2`.
  Consecutive ratios are at most `(6/5)^a e^(-L^2/2) <= 1/2`, so the tail is at most `2 * 3^d (2L)^|g| 5^a e^(-5L^2/2)`.

**Monotonicity in `L`.** Each shell term has logarithmic `L`-derivative at most `|g|/L - L s <= 0` when `|g| <= L^2`,
because `t He*'(t) <= m He*(t)`. The tail bound and `theta_1` also decrease. So the value at `L0` bounds every `L >= L0`.

The radius used for `d^g K_L(0)` is the image bound plus `theta_1 |d^g phi(0)|`. The certificate queries jets up to order `20`
and requires `|g|^2 <= 5 L0^2` and `|g| <= L0^2`. At `L0 = 10`, `theta_1 <= 1.16e-21` in `d = 3`.

## 3. Lemma P: the ball pipeline

A ball `B(c, rho)` is the rational interval `[c - rho, c + rho]`.
- Sums, products and reciprocals (when `|c| > rho`) are the standard outward rules.
- The radii are rounded up by an outward dyadic ceiling rule (`rup`), with at least 64-bit relative precision. This
  affects precision only, not outwardness.
- The operands are integers, Fractions or balls throughout. Float scalars are not certified: `B(1) + 0.1` would round the
  center without a radius. The certificate never uses one. Reuse elsewhere should coerce or reject floats (review C49).
- The centers are exact. With all radii zero the arithmetic is exactly [C2X]'s, so the centers of every output are the
  reference values.

`transfer.kernel(d, jetcov)` repeats [C2X] §2 with `pseries.R = 8` (series exact through `r^5`) and polynomials truncated
at `r^4`:
1. the pin covariance `S_r`, its inverse and determinant, by Gauss–Jordan over series of balls;
2. conditioning of the Hessian entries on the pins and then on the **full** transverse block. In `d = 3` that block is
   `T = [[x1, x3], [x3, x2]]`, with no rotation reduction, because the torus is not isotropic;
3. `F = E[det H_M det H_S | T, U_r = v_r]` by Isserlis;
4. `(det ratio)^(-1/2) exp(-(dq + dQ)/2) F`. The `r^0` parts of the determinant ratio and of `q`, `Q` are removed
   structurally rather than by subtracting equal balls, which would leave spurious radii.

The output is the integrand `G` (balls), `E = (q_0 + Q_0)/2` (a homogeneous quadratic form in `w = (b, k, x)`), `det S_0` and
`det T_0`. For the surrogate,

    A~_r^{K,u}(b, k) = kappa_K integral_(T < 0) e^(-E) G dx / r^2,   kappa_K = -12 (2 pi)^(-(p + n_T)/2) (det S_0 det T_0)^(-1/2),

and the `A_2`-integrand is `kappa_K e^(-E) H` with `H = [r^4] G`. As in [C2X] §2.3, `A~_r` is real-analytic near
`r = 0`, because `K_L` and `phi` are real-analytic and the `r = 0` covariances are nondegenerate. Every pivot is certified by `|c| > rho`.

**Reference check (exact).** With zero radii, `kernel` reproduces [C2X]'s `kernel_data` identically:
- the coefficients of `G` through `r^4`, `E` and `det S_0` in `d = 1, 2`;
- in `d = 3`, the same on the slice `x3 = 0`, which is the diagonal slice [C2X] evaluates.

## 4. Lemma E: evenness in `r` at fixed `v_1`

Relabel the two points: `r -> -r` sends `M = -r u/2` to `+r u/2` and `S` to `-r u/2`. Every pin row of [R] is invariant under
this relabelling as a linear form in the jets at `0`, because each is symmetric in `(M, S)` together with the sign of `r`.
The rows are `(f(M) + f(S))/2`, `(f(S) - f(M))/r`, `(f_u(S) - f_u(M))/r`,
`6 r^(-2)(f_u(M) + f_u(S) - 2(f(S) - f(M))/r)`, and the transverse pairs.

The relabelling swaps `H_M` and `H_S`, which leaves `det H_M det H_S` unchanged, and it fixes `T = D_Theta^2 f(0)`. The
target is `v_r = (b - k r^3/2, -k r^2, 0, 12k, 0, ...)`, whose entries other than `v_1 = b - k r^3/2` depend on `r` only
through `r^2`. Hence the integrand `e^(-(q + Q)/2) (det ratio)^(-1/2) F`, as a function of `(r, v_1, k, x)`, is even in `r` as a
formal power series. The coefficients are finite sums of jet covariances, so no property of `K` beyond stationarity and
smoothness is used.
- **Smooth `K`.** The rows are averages of derivatives against smooth kernels, so the covariances, the regression and the
  cone integral are smooth in `r` up to `0`. Integrating the even formal series over the fixed cone gives the even
  finite-order expansion of Lemma E, to every order.
- **Real-analytic `K`.** The series converge near `r = 0`, which gives the exact form
  `A~_r = Atilde(r^2, b - k r^3/2, k)` with `Atilde` real-analytic.

**Exact checks (controls.py).** For anisotropic product kernels `prod_i e^(-s_i z_i^2/2)` (rational jets, not isotropic,
`d = 1, 2, 3`, two `s` each) the exact integrand has `G_0 = G_1 = G_3 = 0` and
`G_5 = -(k/2)(d_b G_2 - (d_b E) G_2)`, as Lemma E predicts.

## 5. Lemmas F and G: the finite part and the Gaussian bounds

**Lemma F.** For `C^1` functions `F_1, F_2` on `[0, oo)` with integrable decay, put `Delta = F_1 - F_2`. Then

    |T(F_1) - T(F_2)| <= 3 |Delta(0)| + 3 integral_0^1 |Delta'(s)| s^(-1/3) ds + integral_1^oo |Delta(k)| k^(-4/3) dk.

*Proof.* `T(F) = integral_0^1 [F - F(0)] k^(-4/3) + integral_1^oo F k^(-4/3) - 3F(0)`. Next,
`|Delta(k) - Delta(0)| <= integral_0^k |Delta'|`. Exchanging the order of integration gives
`integral_s^1 k^(-4/3) dk = 3(s^(-1/3) - 1) <= 3 s^(-1/3)`.

This is the inequality of 5933574379 with its second-derivative term replaced by a first-derivative one, so no evenness in
`k` is needed.

**Lemma G.** Write `g_K = kappa_K e^(-E_K) H_K` and, for the derivative, `g'_K = kappa_K e^(-E_K) H'_K`, where
`H' = d_k H - (d_k E) H` is formed in ball arithmetic. Pointwise,

    |g_L - g_ref| <= |kappa_ref| e^(-E_ref) [ (|e_kappa| + |dE|) e^(|dE|) |H_L| + |H_L - H_ref| ],

where:
- `|kappa_ref| = 12 (2 pi)^(-(p + n_T)/2) (det S_0 det T_0)^(-1/2)` is the magnitude of the negative constant
  `kappa_ref`; `bound_core` bounds it above by `kap` (review C49-F01, 5382406982);
- `kappa_L = kappa_ref (1 + e_kappa)`, with `|e_kappa| <= rho/(1 - rho)` and `rho` the relative radius of
  `det S_0 det T_0`;
- `|dE| = |E_L - E_ref| <= sum_i eta_i w_i^2`, from the radii of `E`'s coefficients via
  `|w_i w_j| <= (w_i^2 + w_j^2)/2`;
- `|H_L| <= sum (|c| + rho)|w^e|` and `|H_L - H_ref| <= sum rho |w^e|` over `H`'s monomials.

**Gaussian floor.** A rational `t` with `M - t diag(M)` positive definite, where `E_ref = w^T M w`, is certified by exact
`LDL^T` and bisection. It gives `e^(-E_ref + |dE|) <= prod_i e^(-a_i w_i^2)` with `a_i = t M_ii - eta_i > 0`.

The bounds then enlarge the cone and the `b`-line to all of `R^(1 + n_T)`:
- `|Delta(0)|` uses the monomials with no `k`;
- `integral_0^1 |Delta'| s^(-1/3)` uses `s^(j - 1/3) <= s^(j-1)` on `(0, 1]` for `j >= 1`, and `integral_0^1 s^(-1/3) = 3/2`
  for `j = 0`;
- `integral_1^oo |Delta| k^(-4/3)` is bounded by `integral_0^oo |Delta|`.

Each is a finite sum of products `integral |t|^n e^(-a t^2) dt = Gamma((n+1)/2) a^(-(n+1)/2)`, bounded above in
rationals: `sqrt(pi) < sqrt(355/113)`, `pi > 333/106`, and `isqrt` bounds. Finally
`eps = (1/3)|S^(d-1)| * [3 Delta_0 + 3 Delta'_w + Delta_int]`, with `|S^1| <= 2 * 355/113` and `|S^2| <= 4 * 355/113`. It
bounds every frame, and therefore the average over `u`.

## 6. Numbers (`RESULTS.json`)

| `d` | `L0` | `t` | `min a_i` | `max eta_i` | `3 Delta_0` | `3 Delta'_w` | `Delta_int` | `eps` |
|---|---|---|---|---|---|---|---|---|
| `1` | `10` | `1` | `0.75` | `9.4e-16` | `1.3e-14` | `2.0e-13` | `1.7e-15` | `1.41e-13` |
| `2` | `10` | `1/2` | `0.125` | `1.9e-15` | `3.4e-14` | `9.6e-13` | `8.9e-15` | `2.09e-12` |
| `3` | `10` | `0.3675` | `0.0919` | `2.8e-15` | `5.3e-13` | `2.3e-11` | `2.2e-13` | `1.00e-10` |

At `L0 = 24` every radius and bound is smaller by a factor of about `1e-101`. `H` has 9, 50 and 1006 monomials in `d = 1, 2, 3`.

**Slack.** The bound is conservative. Controls with explicit perturbations (§7) show it exceeds the true change of `c2` by
factors of `1e4` (`d = 1`) to `1e8` (`d = 3`). The causes are ball radii that grow through elimination and Isserlis without
cancellation, the absolute moments, and the cone enlarged to the whole space. The true torus change is of order `e^(-L^2/2)` times polynomial factors, so none of this matters for the conclusions.

## 7. Verification and controls

- `python3 -B -S transfer.py --check` recomputes `reference_checks` and all 12 bounds and compares them with `RESULTS.json`
  exactly. It takes about two minutes, mostly the `d = 3` ball Isserlis step, and passes identically under `-B -O -S`.
- **Five seeded defects must each exit 1:**
  - `no-image`: the image sums are dropped;
  - `no-theta`: the normalization term is dropped;
  - `drop-ratio`: the transverse determinant ratio is dropped;
  - `eta-half`: the exponent radius is halved;
  - `fp-const`: the finite-part constant `1` replaces `3`.
- **`controls.py`** (exact and floating; not part of the certificate). It takes about 13 seconds:
  - **Lemma E**, exact: six anisotropic kernels (§4).
  - **Reference:** a floating integrator applied to [C2X]'s exact data reproduces `c2` inside [C2X]'s certified intervals
    in `d = 1, 2, 3`.
  - **Falsification of Lemmas F, G and P at a measurable scale.** For the even isotropic mixtures
    `K = (1 - eps) phi + eps phi(sqrt s .)`, with `s = 2` or `1/2` and `eps = 1e-3` or `1e-5`:
    - `c2[K]` is computed directly, by the exact derivation with `K`'s jets and then closed-form floating integration;
    - the bound of `bound_core`, fed with the balls `(phi-jet, |K-jet - phi-jet|)`, must exceed `|c2[K] - c2[phi]|`;
    - all 12 cases pass. The true changes are `1e-7` to `1e-3`.

## 8. What this does not do

- **The definition and identification are consumed.**
  - **Candidate density.** That `c2[K_L]` is its `ell^(1/3)` coefficient is [T]'s claim: Math-#218, an unmerged
    author-side candidate for `d >= 2`.
  - **Elder density.** The identification is [E3]'s (Math-#220). That is an unmerged author-side candidate which consumes
    the unmerged #207 and #218 and the now-merged #187. The complete chain is #191/#198 (merged) → #207 → #218 → #220.
  - Neither identification is reviewed here, and the transfer of the fixed-cone expression does not depend on either
    (review 5383099127, item 2).
  - So is the typed replacement `A_r = A~_r + O(r^3)` ([D] §2.2) on the torus. Lemma E and Theorem C2T are statements
    about the surrogate.
- **`d = 1, 2, 3` only;** the pipeline runs unchanged in `d = 4` given time. Lattices other than `L Z^d` are not treated,
  although Lemma J only needs `|p_n| >= L|n|`-type counts.
- **Conservative constants** (§6). They are not estimates of the true torus deviation.
- **No review** of [C2X], [T], [D], [SIDE24], [CU], [E3], [L'], [FJ] or Math-#224. Same GitHub account as every lane; zero
  organizational-independence credit. **I will not merge.**

## 9. Provenance

- **Sources** (`SOURCE_MAP.json`). The workflow verifies these on the checked-out tree:
  - [C2X] `frontiers/c2_exact_20261001/{exact.py, pseries.py, NOTE.md, RESULTS.json}` on `main` (since `f9ebba1`; unchanged at `7fe06b0`). `exact.py` and
    `pseries.py` are also carried byte-identically in this directory.
  - [SIDE24] `coefficients/side24_v1/PROOF.md`.
- **Unmerged, recorded and not checked on this tree:**
  - [T] Math-#218 `PROOF.md` (blob `70ca57ef`);
  - [D] Math-#216 `NOTE.md` (blob `aa078a9c`);
  - [CT] Math-#224 `PROOF.md`, for (T1) and as the `c1` analogue (cited);
  - [CU] Math-#219 at `7a04873`: `NOTE.md` (blob `7dccfa97`) and `RESULTS.json` (blob `8bbd0b0c`), consumed for `c1/c`;
  - [E3] Math-#220 at `70dcf31`: `PROOF.md` (blob `c8767dde`), cited for the conditional elder identification;
  - [L'] Math-#227 at `2d1ec7c`: `NOTE.md` (blob `138521e8`), cited only.
- **On `main` since `7fe06b0`, cited only:** [FJ] Math-#232
  `frontiers/c2_finite_jet_transfer_20261001/PROOF.md` (blob `54cc4a1a`).
- **Files:**
  - the certificate: `transfer.py`, `ball.py`, `exact.py`, `pseries.py`;
  - `controls.py`;
  - `RESULTS.json`, `SOURCE_MAP.json`, `SOURCE_FILES.json`.
