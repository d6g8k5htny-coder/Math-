# Certified planar near cluster coefficients `alpha_1`, `alpha_2` and the elder-failure constant `C_fail^{B,K}`

**Object:** CL-C8-ELDER-FAILURE-COEFFICIENT-20261001-v1.
**Author:** Anthropic Claude (Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`), 1 October 2026.
**Disposition:** certified numerical enclosures. Binary64 interval arithmetic with outward rounding encloses explicit
finite-dimensional Gaussian integrals that the sources define. Author-side; no review yet.
**Scientific effect:** NONE. No `STATUS`, `PROOF_INDEX`, `GRAPH`, claim, catalog, prize or source-body change. Same GitHub
account as every lane; zero organizational-independence credit.

## 0. Statement

Planar model, reference (continuum) kernel `K(z) = exp(-|z|^2/2)`. `(a, beta, c) ~ N(0, diag(2, 2, 6))` are the odd
contact jets and `I_1`, `I_2` the near failure integrals of [NUM] §§2–3 (recalled in §1). Write `J_j(k) = E[I_j]` and
`J_fail = J_1 + J_2`. By [NUM] §2, from [CL] Theorem N or [CUB] Theorem F,

    alpha_j(b, k) = (p_b(0)/z_0) J_j(k),      p_b(0)/z_0 = phi(b/sqrt2) / (sqrt2 36 k^2 m_(2,b)),
    m_(2,b) = (b^2 + 2) Phi(b/sqrt2) + sqrt2 b phi(b/sqrt2),

with `nu(2) = alpha_2` ([NUM] §1) and `a_fail = alpha_1 + alpha_2` the selector-failure coefficient of [S] (S2).

**Theorem (certified enclosures).** The following intervals contain the exact values. The certificate's own intervals
(`RESULTS.json`, 10 digits) are rounded further outward here.

| `k` | `J_fail = J_1 + J_2` | `J_1` | `J_2` | `J_2 / J_fail` | near Palm excess `2J_2/(J_1 + 2J_2)` |
|---|---|---|---|---|---|
| `1/2` | `[36.7830581, 36.7868003]` | `[35.673609, 35.680652]` | `[1.10614, 1.10945]` | `[0.030069, 0.030162]` | `[0.058377, 0.058563]` |
| `1` | `[172.846360, 172.860205]` | `[169.58395, 169.60709]` | `[3.25312, 3.26241]` | `[0.018819, 0.018875]` | `[0.036941, 0.037052]` |
| `2` | `[1111.98227, 1112.03079]` | `[1103.1296, 1103.2057]` | `[8.82508, 8.85263]` | `[0.0079360, 0.0079612]` | `[0.015746, 0.015797]` |

| `k` | `b` | `p_b(0)/z_0` | `alpha_1` | `alpha_2 = nu(2)` | `a_fail = alpha_1 + alpha_2` |
|---|---|---|---|---|---|
| `1/2` | `0` | `[0.031343862, 0.031343869]` | `[1.118148, 1.118370]` | `[0.034670, 0.034775]` | `[1.152923, 1.153041]` |
| `1/2` | `1` | `[0.0089740288, 0.0089740307]` | `[0.3201360, 0.3201993]` | `[0.0099266, 0.0099563]` | `[0.3300922, 0.3301259]` |
| `1` | `0` | `[0.0078359656, 0.0078359673]` | `[1.328854, 1.329036]` | `[0.025491, 0.025565]` | `[1.354418, 1.354527]` |
| `1` | `1` | `[0.0022435072, 0.0022435077]` | `[0.3804628, 0.3805148]` | `[0.0072984, 0.0073193]` | `[0.3877820, 0.3878132]` |
| `2` | `0` | `[0.0019589914, 0.0019589919]` | `[2.161021, 2.161171]` | `[0.017288, 0.017343]` | `[2.178363, 2.178459]` |
| `2` | `1` | `[0.00056087680, 0.00056087692]` | `[0.6187198, 0.6187626]` | `[0.0049497, 0.0049653]` | `[0.6236851, 0.6237124]` |

**Corollary 1 (the elder-failure constant).** On `B x K = [0, 1] x [1/2, 2]`, the coefficient of [S] §9 for the reference
kernel,

    C_fail^{B,K} = integral_(B x K x S^1) A_0^ref a_fail / (3 k^(5/3)) db dk dsigma(u) = const I_b I_k,
    const = 4 / (sqrt2 (2 pi)^(5/2) sqrt12),   I_b = integral_0^1 exp(-b^2) db,
    I_k = integral_(1/2)^2 exp(-12 k^2) k^(-5/3) J_fail(k) dk,

satisfies

    I_k in [0.4421366, 0.4432234],      C_fail^{B,K} in [0.00272445, 0.00273116].

This is the reference-kernel value of the constant of [S] §9, which states `nu_rej^{B,K}(ell) ~ C_fail^{B,K} ell^(2/3)`
and `E N_rej^{B,K}(0, t] ~ (3/5) C_fail^{B,K} t^(5/3)` for the torus model. The torus constant differs by the torus
corrections, which are not certified here (§10).

**Corollary 2 (`d = 3`, conditional on Math-#175 and Math-#184).**
- Math-#175 (OpenAI/Codex, open, AUTHOR_SIDE / HOLD) is [FIB]:
  - its Theorem F, (S3), identifies `(1 - p_r)/r^3 -> a_1 + a_2` in fixed `d >= 3`;
  - its (L1) is `C_fail^{B,K} = integral_(B x K x S^(d-1)) A_0 a_fail / (3k^(5/3))`.
- Math-#184 (open) is [HD]. Its Theorem 1 gives `a_j^(d) = R_d(b) alpha_j` with `R_d = N_d m_(2,b) / m_(d,b)`.

In `d = 3`, for the reference kernel, the derivation of §1 gives
`A_0^ref,(3) = 432 (2 pi)^-4 12^(-1/2) k^2 exp(-12k^2) exp(-3b^2/4) m_(3,b)`: the transverse jet `f_xy2` adds a factor
`(2 pi)^(-1/2)`, `p_G(0) = (2 pi)^(-3/2)` and `z_0 = 36 k^2 m_(3,b)`. Both `m_(3,b)` and `m_(2,b)` cancel. With
`N_3(b) = pi (2 pi)^(-1/2) g(b)` ([HD] (2), `m = 2`) we have `exp(-3b^2/4) phi(b/sqrt2) N_3(b) = exp(-b^2) g(b) / 2`, so

    C_fail^(3),{B,K} = 4 pi (4/sqrt2) (2 pi)^-4 12^(-1/2) I_b^(3) I_k,      I_b^(3) = (1/2) integral_0^1 exp(-b^2) g(b) db,

with `g(b) = (b^3 + 6b) Phi(b/sqrt2) + sqrt2 (b^2 + 4) phi(b/sqrt2)`. The certificate checks `N_3(0) = 2 sqrt2` ([HD] (3)) and
gives

    I_b^(3) in [1.513649, 1.513684],      C_fail^(3),{B,K} in [0.00440581, 0.00441675].

At `b = 0`, `R_3(0) = (32 + 28 sqrt2)/17`:

| `k` | `alpha_1^(3)` | `alpha_2^(3) = nu^(3)(2)` | `a_fail^(3)` |
|---|---|---|---|
| `1/2` | `[4.709246, 4.710177]` | `[0.14602, 0.14646]` | `[4.855704, 4.856199]` |
| `1` | `[5.596663, 5.597427]` | `[0.10736, 0.10767]` | `[5.704330, 5.704788]` |
| `2` | `[9.101458, 9.102086]` | `[0.072812, 0.073040]` | `[9.174497, 9.174898]` |

**Consequences.**
- **`nu(2)` and `a_fail` are certified.** At `(b, k) = (0, 1)`: `alpha_2 = nu(2)` is in `[0.025491, 0.025565]` and `a_fail` in
  `[1.354418, 1.354527]`. The two-point share `J_2/J_fail` decreases from
  `3.01%` at `k = 1/2` to `0.79%` at `k = 2`.
- **[NUM]'s open digit is settled.** At `k = 2`, [NUM] observed that Gauss–Hermite and Monte Carlo disagree on `J_2` by
  2.6% and said the third digit of `alpha_2(2)` was not established. The certified `J_2(2)` is in `[8.82508, 8.85263]`. It
  excludes the GH60 value `8.641` and is consistent with the Monte Carlo value `8.875 +- 0.073`. The Gauss–Hermite
  sequence had not converged there.
- **The cap route overstates the lifetime difference by about `1.5 x 10^5`.** Math-#215 (open) certifies
  `nu_cand - nu_eld <= C_{B,K}(r_*) ell^(2/3)` through the cap criterion, with `C_{B,K}(1/4096) = 402.5297`. As
  `r_* -> 0`, that route can give no less than `Gamma_2 = 307.51` (floating). The leading constant of the difference is
  `C_fail^{B,K}`, about `0.00273`: `1.47 x 10^5` times smaller than `C_{B,K}(1/4096)` and `1.13 x 10^5` times
  smaller than `Gamma_2`.
- **The same holds in `d = 3`, conditionally.** `C_fail^(3),{B,K}` is about `0.00441`. That is `2.73 x 10^5` times
  smaller than Math-#215's `C_{B,K}^(3)(1/4096) = 1205.7089` and `1.23 x 10^5` times smaller than
  `Gamma_3 = 540.97`.

## 1. What is evaluated

[NUM] §3 (from [CUB] (C2)–(C3) and [CL] (3.12)) defines, with `B = beta - a^2/(12k)`, `D = (c - a beta/(4k) +
a^3/(72k^2))/2`, the typed domain `s < -|B|/2`, the weight `w_0 = 9k^2 (4s^2 - B^2)` and

    g(s) = -2s^3 + 3Bs^2 - B^3 - 12k D^2,

the classification: `n = 2` iff `s > B` and `g(s) > 0`; `n = 1` iff `g(s) < 0`; `n = 0` iff `s <= B` and `g(s) > 0`.
Then `I_j = integral_(s < -|B|/2) w_0 1{n = j} ds`. [NUM] §2 gives the prefactor `p_b(0)/z_0`. Here `p_b(0)` is the density
at `0` of `A = f_zz | (f, f_xx, f_xz) = (b, 0, 0) ~ N(-b, 2)`, and `z_0 = 36 k^2 m_(2,b)`.

The reference integrand of [S] §9 is `A_0^ref = 12 pi_0 z_0`. [LP] §15 factorizes `pi_0 = p_(f,V_u)(b, 0) p_G(0)
phi_tau(12k)`. With the jet covariances of [NUM] §2 these factors are:
- `(f, f_xx)` has covariance `[[1, -1], [-1, 3]]`, and `f_xz` is independent with variance `1`. So
  `p_(f,V_u)(b, 0) = exp(-3b^2/4) / (2 pi sqrt2 sqrt(2 pi))`.
- `p_G(0) = 1/(2 pi)`.
- `tau^2 = Var(f_xxx | grad f = 0) = 15 - 9 = 6`.

Hence `pi_0 = (2 pi)^-3 12^(-1/2) exp(-3b^2/4 - 12k^2)` and

    A_0^ref = 432 (2 pi)^-3 12^(-1/2) k^2 exp(-12 k^2) exp(-3b^2/4) m_(2,b).

In `A_0^ref a_fail / (3 k^(5/3))`, `m_(2,b)` and `k^2` cancel, `exp(-3b^2/4) phi(b/sqrt2) / sqrt2 = exp(-b^2) / (2 sqrt pi)`,
and the circle gives `2 pi`. This leaves `const I_b I_k` with the `const` above.

## 2. Reduction to one root (Lemma 1)

Put `x = -s` and `P(x) = (x + B)^2 (2x - B)`. Expanding, `g(s) = P(x) - T` with `T = 12k D^2`. The typed domain is
`x > |B|/2`.

- **`B >= 0`.** `P` increases on `x >= B/2` from `P(B/2) = 0`. So `n = 1` exactly on `(B/2, x_b)`, and `n = 2` never
  occurs (it needs `x < -B`).
- **`B < 0`.** `P` decreases on `(|B|/2, |B|)` from `|B|^3/2` to `0`, then increases.
  - If `T < |B|^3/2`: `n = 2` on `(|B|/2, x_m)` and `n = 1` on `(x_m, x_b)`.
  - Otherwise: `n = 1` on `(|B|/2, x_b)`.

Here `x_b >= max(-B, B/2)` is the **big root** and `x_m in [|B|/2, |B|]` the **middle root** of `P = T`. In every case
the failure set `{n >= 1}` is the single interval `|B|/2 < x < x_b` (up to null sets). With the antiderivative
`9k^2 (4x^3/3 - B^2 x)`:

    I_fail = I_1 + I_2 = 3k^2 H,     H   = |B|^3 + 4 x_b^3 - 3B^2 x_b = 2(B_-)^3 + 2T + V,   V = -3B(2x_b - B)(x_b + B),
    I_2 = 3k^2 H_2,                  H_2 = |B|^3 + 4 x_m^3 - 3B^2 x_m   on {B < 0, T < |B|^3/2}, 0 elsewhere.

The identity `2T + V = (x + B)(2x - B)^2 = 4x^3 - 3B^2 x + B^3` holds at either root. The controls `(0, -2k, 0)` (`H_2 = 16k^3`,
`I_2 = 48k^5`) and `(0, 0, c)` (`H = 2T = 24k D^2`, `I_1 = 72k^3 D^2`) agree with [NUM] §3.

**Scaled coordinates.** `a^ = a / sqrt k ~ N(0, 2/k)`, `c^ = sqrt(k) c ~ N(0, 6k)`. Then `B = beta - a^2/12` and
`T = 3u^2` with `u = c^ + d` and `d = -a^ beta/4 + a^3/72`, so `J_fail(k) = 3k^2 E[H]` and `J_2(k) = 3k^2 E[H_2]` with
`k`-free integrands. Exactly, `E[2T] = 6 E[u^2] = 6 (6k + 1/(4k) + 5/(216 k^3))`. Also `E[2(B_-)^3] = 4 integral_0^inf
phi_(sqrt(2/k))(a) g(a^2/12) da` with `g(m) = E[(m - beta)_+^3]`.

## 3. Monotonicity and the `(B, w)`-calculus (Lemma 2)

Let `r = B/x`, so `r in [-1, 2]` on the big root and `r in [-2, -1]` on the middle root. Let `w = |u| = (T/3)^(1/2)`.
Implicit differentiation of `P(x) = T` gives:
- `x_T = 1/(6x(x + B))` (positive on the big root, negative on the middle root);
- `x_B = -(x - B)/(2x)`;
- `r_B = (2x - B)(x + B)/(2x^3)`;
- `H_T = (4 - r^2)/(2(1 + r))`;
- `V_T = -r(r + 4)/(2(1 + r))`;
- `H_B / x^2 = -(3/2)(r - 2)^2 (r + 1)` for `B > 0` and `-(3/2)(r + 2)(r^2 - r + 2)` for `B < 0`;
- `V_B = -(3/2) x^2 (r - 2)^2 (r + 1)`.

Therefore:
- `H` is non-increasing in `B` and non-decreasing in `T`.
- `V` is non-increasing in `B`. In `T` it is non-increasing for `B > 0` and non-decreasing for `B < 0`.
- `H_2` is non-increasing in both.
- On the big root, `x` increases in `T` and, for fixed `T`, is unimodal in `B` with minimum `x = B` at `B = (T/4)^(1/3)`.
  `r` is non-decreasing in `B`, increasing in `T` for `B < 0` and decreasing for `B > 0`.
- On the middle root, `x` and `r` are non-increasing in both `B` and `T`.

In `(B, w)` with `sigma = +1` on the big root and `-1` on the middle root:

    V_w  = -sigma sqrt3 x^(3/2) r (4 + r)(2 - r)^(1/2)
    V_BB = x p(r),           p(r) = 6 + 3r - 9r^2/2 - 3r^3/4 + 3r^4/4
    V_Bw = -sigma (sqrt3/2) x^(1/2) e(r),    e(r) = (2 - r)^(3/2)(4 + 2r + r^2)    (decreasing on r <= 2)
    V_ww = g(r) = -r(4 - r + r^2)                                                    (strictly decreasing)

- The `T`-derivatives blow up as `T -> 0` for `B < 0` (`V_TT ~ T^(-3/2)`). The `(B, w)`-Hessian is bounded: its entries are
  `x p(r)`, `x^(1/2) e(r)` and `g(r)` with `r` in a bounded range. At the triple point `(0, 0)` it is bounded but
  discontinuous, and `V` is `C^(1,1)` there, which is all the integral remainder needs.
- `V` depends on `u` only through `w`, with a kink at `u = 0` when `B < 0` (`V_w(B, 0) = 9|B|^(3/2)`).
- On the support boundary `T = |B|^3/2` the middle root is `|B|/2` (`r = -2`). There `H_2 = 0`,
  `H_2,B = -(3/2) x^2 (r + 2)(r^2 - r + 2) = 0` and `H_2,T = (4 - r^2)/(2(1 + r)) = 0`. So the zero extension of `H_2` is
  `C^1` and piecewise `C^2`.

All formulas were checked against finite differences of the root map (relative agreement `6e-6` at step `1e-4`) and
symbolically.

## 4. Box enclosures (Lemma 3)

For a box `Q` of jet coordinates, let `[B_l, B_h] x [T_l, T_h]` contain its image. The ranges of `B` and `d` are exact
up to outward rounding: `d` is linear in `beta`, and its `a`-extremes are at the ends or at `a = +-sqrt(6 beta)`. The
`u`-range is the `c`-range plus the `d`-range. Two enclosures of `integral_Q F dmu` (`F = V`, `H`, `H_2`) are formed and intersected; an empty
intersection would raise.

- **First order.** `I_1 = mu(Q) [min F, max F]`. The extremes sit at rectangle corners by Lemma 2, so the corner roots
  suffice (four big roots, or two middle roots).
- **Second order** (only if the `u`-range of `Q` avoids `0`, so `w = s u` with a fixed sign `s`). Take a float point
  `(B*, w*)` of the rectangle and Taylor's formula with integral remainder along the segment to `(B, w)` (the rectangle
  is convex):

      F = F* + F_B* dB + F_w* dw + 1/2 (h_BB dB^2 + 2 h_Bw dB dw + h_ww dw^2).

  - Each averaged Hessian entry `h` lies in the interval range `S` of the second derivative over the rectangle,
    computed from the corner ranges of `x` and `r`, with `p` evaluated in mean-value form. For `H_2` on boxes meeting
    the support boundary, the ranges are hulled with `0`.
  - Hence `integral_Q F dmu` lies in

        F* m + F_B* E[dB] + s F_w* E[du] + 1/2 (S_BB E[dB^2] + S_ww E[du^2]) + s c E[dB du] +- delta (E[dB^2] E[du^2])^(1/2),

    where `c` and `delta` are the centre and radius of `S_Bw`.
  - The six moments are exact Gaussian polynomial moments (orders `a <= 6`, `beta, c <= 2`). The second-order part
    has width `O(diam(S) h^2 mu(Q))`, so the scheme is third order.
- **Partial moments.** `M_n = (n - 1) s^2 M_(n-2) + s^2 (x_0^(n-1) phi(x_0) - x_1^(n-1) phi(x_1))`. Cell masses are
  differences of upper tails `Q(t)` on the side away from `0`, so they keep relative precision far out.
- **Roots.** The roots are bracketed by Newton iteration from a Cardano / trigonometric start. The bracket is then
  verified: `P(a) - T < 0 < P(b) - T` for the big root, reversed for the middle root. The sign test is a binary64
  evaluation of `(x + B)^2 (2x - B) - T` with an a priori rounding bound.
- **Refinement.** An initial `8^3` grid covers `[-8 sigma, 8 sigma]^3`. Boxes are bisected depth-first along their
  standardized widest side until the enclosure width is at most `10^-8`. Partial sums are rounded outward, and the
  initial cells are dealt to processes in a fixed pattern.

## 5. Exact and one-dimensional parts; tails

- `E[2T]` is the exact rational above.
- `E[2(B_-)^3]` is a one-dimensional integral over `4000` cells, each by second-order Taylor expansion about the
  midpoint.
  - `G(a) = g(a^2/12)` has `G'' = g''(m) a^2/36 + g'(m)/6`.
  - `g' = 3[(m^2 + 2) Phi(m/sqrt2) + sqrt2 m phi(m/sqrt2)]` and `g'' = 6[m Phi(m/sqrt2) + sqrt2 phi(m/sqrt2)]` are increasing,
    so `G''` is bounded by its values at the cell ends.
  - The tail `a > 12 sigma` uses `g(m) <= m^3 + 6m + sqrt2 (m^2 + 4)/sqrt(2 pi)`.
- **Outside the box.** Lemma 1 and `x_b <= |B| + (T/2)^(1/3)` (since `P(|B| + t) >= 2t^3`) give
  `|V|, H, H_2 <= 17|B|^3 + 8T`. This is a polynomial in `|a|, |beta|, |c|`, integrated over the complement by the union
  bound with exact tail moments.

These are expectations over the scaled law. `J_fail = 3k^2 (E[2(B_-)^3] + E[2T] + E[V])` and `J_2 = 3k^2 E[H_2]`. The
tail bound enters `E[V]` with both signs and `E[H_2]` from above.

| `k` | `E[2(B_-)^3]` | `E[2T]` exact | `E[V]` boxes | `E[H_2]` boxes | tail bound |
|---|---|---|---|---|---|
| `1/2` | `[8.3574312330, 8.3574329380]` | `199/9` (`22.11111111`) | `[18.5755374, 18.5805207]` | `[1.4748651, 1.4792648]` | `1.5E-9` |
| `1` | `[5.8760207620, 5.8760219460]` | `1355/36` (`37.63888888`) | `[14.1005477, 14.1051535]` | `[1.0843739, 1.0874697]` | `3.3E-10` |
| `2` | `[5.0934267220, 5.0934277450]` | `20957/288` (`72.76736111`) | `[14.8044089, 14.8084356]` | `[0.73542405, 0.73771834]` | `2.1E-10` |

## 6. The `k`-integral

`I_k` is a four-dimensional box integral in the original coordinates `(a, beta, c, k)`, with weight
`W(k) = 3k^(1/3) exp(-12k^2)` (that is, `3k^2 exp(-12k^2) k^(-5/3)`):

    B = beta - a^2/(12k),   u = sqrt(k) c - a beta/(4 sqrt k) + a^3/(72 k^(3/2)).

- Each 4D box maps into a box of scaled coordinates, so the rectangle machinery of §4 applies unchanged.
- The Taylor moments are polynomials in `(a, beta, c)` times `k^(p/2)`, `p = -6..2`. Their `k`-factors
  `K_p = integral W(k) k^(p/2) dk` are enclosed on the `4096` elementary dyadic cells of `[1/2, 2]` by midpoint (below)
  and trapezoid (above) rules on `24` sub-cells. This is valid because every `f(k) = k^q exp(-12k^2)` with
  `q in [-8/3, 4/3]` is convex on `[1/2, 2]`: `f''/f = (24k - q/k)^2 - q/k^2 - 24 >= 87 - 16/3 - 24` for `q >= 0` and
  `>= 120` for `q < 0`.
- `k`-cells are dyadic and never finer than elementary.
- The tail is bounded uniformly in `k` by `17|B|^3 + 8T <= 68|beta|^3 + (68/216 + 576/5184) a^6 + 144 c^2 + 9 a^2 beta^2`.

Values:
- `int_K W(k) dk` is in `[0.00907557755, 0.00907557942]`;
- `const` is in `[0.008250963314, 0.008250964965]`;
- `I_b = sqrt(pi)(Phi(sqrt2) - 1/2)` is in `[0.7468240581, 0.7468242075]`;
- `I_k` (boxes plus tail) is in `[0.4421366, 0.4432234]`.

`I_b^(3)` is integrated on `100000` cells of `[0, 1]`. On each cell `exp(-b^2)` decreases and `g` increases (both positive),
so the cell integral lies between `h exp(-b_1^2) g(b_0)` and `h exp(-b_0^2) g(b_1)`.

## 7. Arithmetic

Every `+, -, *, /, sqrt` is IEEE binary64 round-to-nearest, widened outward by one ulp. No libm transcendental is
trusted:
- `pi` comes from Machin's series with a rational remainder, and `ln 2` from `sum 1/(j 2^j)`.
- `exp(-y)`: `y = n ln2 + r` with `r in [0, 0.75]`, a degree-18 Taylor polynomial with the a priori bound
  `(56u + 10^-19) e^0.75`, then exact scaling by `2^-n`. The observed relative width is below `4e-13` for `y <= 700`.
- `Phi(t)` for `t < 2` is `1/2 + phi(t) sum t^(2n+1)/(2n+1)!!`, with an a priori summation bound and a geometric tail.
- `Q(t) = 1 - Phi(t)` for `t >= 2` is `phi(t) R(t)`, where `R` is Laplace's continued fraction
  `1/(t + 1/(t + 2/(t + ...)))`. It has positive elements, so consecutive approximants bracket `R`.

libm `pow`, `acos` and `cos` only seed iterations whose results are verified.

## 8. Verification

- **`--check`** (CI, under `-B -S` and `-B -O -S`) runs two stages:
  - a self-test: every box enclosure, and its first- and second-order parts separately, on `13` fixed 3D boxes and
    `2` 4D boxes contains a pure-Python Gauss–Legendre value (`12`–`16` points per axis; relative slack `1e-9`, or
    `1e-6` on the `C^1` support boundary of `H_2`), and the `k`-moments contain Gauss–Legendre values;
  - the full replay.
- The replayed enclosures must lie inside the published ones and be at most `2 x 10^-7` relatively (plus one unit of
  the 10th digit) tighter. The leaf counts must agree:
  - `V`: `1,209,983`, `1,096,831`, `951,074` at `k = 1/2, 1, 2`;
  - `H_2`: `1,131,985`, `799,321`, `583,149`;
  - `I_k` (4D): `997,266`.
- A full replay takes about 10 minutes on four cores.
- **Mutants** exit 1 at the self-test:
  - `vw-sign` flips `V_w`;
  - `ww-drop` drops `V_ww`;
  - `corner-swap` swaps the monotonicity corners of `V`;
  - `mid-branch` gives `H_2` the big-root sign of `V_w`;
  - `k-weight` drops `k^(1/3)` from `W`.
- **Development checks** (not in the packet):
  - `1,200` random 3D boxes and `250` random 4D boxes, `0` failures against `numpy` Gauss–Legendre;
  - the full-`H` integrand, boxed directly, gives an enclosure of `J_fail(1/2)` that intersects the split one
    (`controls.py`).

## 9. Comparisons (floating controls, `controls.py`)

Floating values of [NUM] (`RESULTS.json`, GH40 / GH60 Gauss–Hermite, Monte Carlo with `10^6` samples) against the
certified enclosures. "in" marks a value inside the enclosure; the last column is the Monte Carlo deviation from
the enclosure midpoint in Monte Carlo standard errors.

| `k` | | certified | GH40 | GH60 | MC `+-` s.e. | (MC - mid)/s.e. |
|---|---|---|---|---|---|---|
| `1/2` | `J_1` | `[35.67361, 35.68065]` | `35.652` (-0.069%) | `35.676` in (-0.004%) | `35.5595 +- 0.0856` | `-1.37` |
| `1/2` | `J_2` | `[1.106149, 1.109449]` | `1.1211` (+1.205%) | `1.1085` in (+0.065%) | `1.11467 +- 0.00619` | `+1.11` |
| `1` | `J_1` | `[169.584, 169.6071]` | `169.63` (+0.023%) | `169.61` (+0.009%) | `169.374 +- 0.283` | `-0.78` |
| `1` | `J_2` | `[3.253122, 3.262409]` | `3.2494` (-0.256%) | `3.2554` in (-0.073%) | `3.28057 +- 0.0222` | `+1.03` |
| `2` | `J_1` | `[1103.13, 1103.206]` | `1104.2` (+0.097%) | `1103.7` (+0.046%) | `1102.63 +- 1.69` | `-0.32` |
| `2` | `J_2` | `[8.825089, 8.85262]` | `8.4211` (-4.726%) | `8.6412` (-2.236%) | `8.87486 +- 0.0727` | `+0.50` |

Every Monte Carlo value is within `1.4` standard errors of the certified value. GH60 is inside the enclosure for
`J_1(1/2)`, `J_2(1/2)` and `J_2(1)`, within `0.05%` of it for `J_1(1)` and `J_1(2)`, and `2.2%` low for `J_2(2)`.

Other controls (`controls.py`):
- the floating Simpson value of `E[2(B_-)^3]` lies inside its enclosure at all three `k`;
- the direct box enclosure of `3k^2 E[H]` at `k = 1/2`, `[36.778523711, 36.792370494]` (`444127` leaves, tolerance
  `1e-7`), intersects the split enclosure of `J_fail(1/2)`;
- `C_{B,K}(1/4096) / C_fail^{B,K}` is in `[1.474, 1.477] x 10^5`, and `Gamma_2 / C_fail^{B,K}` in
  `[1.126, 1.129] x 10^5`.
- `d = 3`:
  - `C_{B,K}^(3)(1/4096) / C_fail^(3),{B,K}` is in `[2.730, 2.737] x 10^5`, and `Gamma_3 / C_fail^(3),{B,K}` in
    `[1.225, 1.228] x 10^5`;
  - Math-#184's floating `a_fail^(3)(0, k)` (`4.8558` at `k = 1/2`, `5.705` at `k = 1`) agree with the certified values to
    `0.003%` and `0.008%`.

## 10. What this does not do

- **Reference kernel only.** The torus model of [LP] and [S] has jet covariances within `O(exp(-L^2/2))` of these
  (lattice sums: `1.4e-13` at `L = 24`, [NUM]). No perturbation bound for `J_j` is proved, so the torus `alpha_j` and
  `C_fail^{B,K}` are not certified. The torus `A_0` is within `eps_2 <= 3.96e-10` of `A_0^ref` by Theorem L of
  Math-#215 (open).
- **Conditional identification.**
  - The certified numbers are the Gaussian integrals that [NUM] (from [CL] Theorem N, [CUB] Theorems C and F) and
    [S] §9 define.
  - That `a_fail` is the selector-failure coefficient and `C_fail^{B,K}` the lifetime constant are statements of
    [S]: AUTHOR_SIDE / HOLD, consumed, not reviewed.
  - `nu(1) = alpha_1 + k integral_X Lambda` also contains the remote part of [RM], which is not evaluated here.
  - Corollary 2 is conditional in addition on [FIB] (Math-#175, open, AUTHOR_SIDE / HOLD) and [HD] (Math-#184,
    open). Its pointwise values are given only at `b = 0`; `R_3(1)` would need `m_(3,1)`, which is not certified here.
- **Coverage.**
  - Pointwise coefficients only at `k = 1/2, 1, 2` and `b = 0, 1`, plus the band integral `C_fail^{B,K}`.
  - No other band, no `k -> 0`, no `d >= 3`.
- No rate, no finite-`r` statement.
- Not a review of [NUM], [S], [CL], [CUB], [LP] or Math-#215.

## 11. Provenance

- **Sources:** `SOURCE_MAP.json` pins [NUM], [S], [LP], [CL], [CUB] and the [NUM] results on `main` `3e0a91b`.
  Math-#215 (`d748c2a`, open) is pinned for comparison constants only. Math-#175 (`701dff4`) and Math-#184 (`d37ff5d`),
  both open, are pinned for Corollary 2.
- **Packet files:**
  - `certificate.py` (drivers, exact parts, tails, assembly, self-test, replay), `boxes.py` (roots, Taylor boxes) and
    `ia.py` (interval arithmetic), all standard-library Python;
  - `controls.py` (floating controls);
  - `RESULTS.json`, the certificate's output.
- **Manifest:** `SOURCE_FILES.json`.
