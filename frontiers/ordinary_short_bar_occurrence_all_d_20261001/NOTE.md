# Ordinary short-bar occurrence in every dimension d >= 2

Object: C52-ALL-D-ORDINARY-SHORT-BAR-OCCURRENCE-20261001-v1.
Author lane: Anthropic / Claude (session 015wNj8L…), under Dylan Roy's delegation. Additive conditional candidate.
Scientific effect: NONE. C8 OPEN. No STATUS, PROOF_INDEX, GRAPH, prize or premise edit.

**Credit.** The argument is OpenAI/Codex's C52 (Math-#235, head `c463777`: `FOLD_ISOLATION.md` blob `a3d4e7c4`,
`PROOF.md` blob `69ff20a6`). C52 proves the planar case and states that it makes "no extension of the present planar
lemma to other dimensions" (FOLD_ISOLATION §8). This packet supplies that extension. Its planar case `d = 2` is exactly
C52's Theorem O, so it neither supersedes nor edits #235. C52's files are cited, not consumed as premises: every step
used here is restated and proved below in dimension d.

## 0. Statement

Fix `d >= 2` and `L > 0`. Let X be the centered, variance-one periodized Gaussian field on `T_L^d = R^d/(L Z^d)` with
covariance

    K_L(z) = sum_{n in Z^d} exp(-|z + L n|^2/2) / sum_{n in Z^d} exp(-|L n|^2/2).

Use ordinary SUPERLEVEL H0 persistence. A finite bar is born at a maximum M and dies at its actual global elder-selected
merging saddle S, of index d-1. Exclude the essential global-maximum class. Let `K_tau` be the number of finite bars of
lifetime in `(0, tau]` in ONE field on the WHOLE torus. Its expectation is not divided by volume.

The seven sources P, CAP, E1, E2, REC, R and T are pinned in `SOURCES.json` at Math- `7fe06b0`. They are the sources
C52 consumes, and each is stated for every fixed `d >= 2`:
- [P] "Fix a dimension d>=2";
- [CAP] "Let d>=2";
- [R] and [T] "for each fixed d>=2" and "Fix d>=2";
- [REC] §1 "for fixed d >= 2";
- [E2] uses the pair map into `R^(2d)`.

[P] is read through [CAP, E1, E2, REC] under REC's mandatory reading rule, with an embedded `r_0 < L/(4 sqrt 2)`.

**Theorem O_d (conditional on these interfaces).** As tau decreases to zero with d and L fixed,

    B_tau := E[K_tau 1{K_tau >= 2}] = o(tau^(2/3)).                                        (O1)

Put `m_tau = E K_tau`, `p_tau = P(K_tau > 0)` and `e_tau = m_tau - p_tau`. Then

    0 <= e_tau = E[(K_tau - 1)_+] <= B_tau = o(tau^(2/3)),
    p_tau = L^d (3/2) c_{d,L} tau^(2/3) + o(tau^(2/3)),                                     (O2)
    TV(law(K_tau | K_tau > 0), delta_1) = P(K_tau >= 2)/p_tau -> 0,                          (O3)

with `c_{d,L} > 0` the coefficient of [P] Theorem C, given explicitly by [P] (15.2).

Condition a field on `K_tau > 0` and pick one of its short bars uniformly. For every common measurable mark, the law
of that mark is within `e_tau/m_tau = o(1)` in total variation of the intensity-normalized mark law:

    TV(F_tau, I_tau) <= e_tau/m_tau.                                                        (O4)

With T's cubic mark, the field-first law converges in total variation to

    (2/3) y^(-1/3) dy  g(q) dq,   g = A_0/(3 c_{d,L} k^(2/3)) on R x (0, inf) x S^(d-1).     (O5)

The only new analytic input is Lemma F_d (§2), the dimension-d ordinary-fold isolation. Sections 3–4 are C52's
consumer, transcribed with `L^d`, `S^(d-1)`, the exponent `2d` and `c_{d,L}`.

**Not claimed:**
- a rate for the little-o;
- factorial moments, a Poisson law, or independent regions;
- an increasing-volume limit, or the limit `d -> infinity`;
- uniqueness of auxiliary witnesses;
- reacceptance of any source.

Every source is a retained hypothesis.

## 1. What changes from d = 2

| Step | C52 (d = 2) | Here (every d >= 2), m = d - 1 |
|---|---|---|
| Pins | 6 rows, `|det T_r| = 12 r^-5` | `2d+2` rows, `|det T_r| = 12 r^-(d+3)` ([P] (3.2)) |
| Transverse datum | scalar `A = F_0,zz(0)` | `m x m` block `A = D_y^2 F_0(0)`, with a density on `Sym(m)` |
| Type boundary | `A < 0`, `A > 0`, `A = 0` null | `A < 0`; `lambda_max(A) > 0`; `{lambda_max(A) = 0}` inside `{det A = 0}`, which is null |
| Ridge | intermediate value theorem in z | strict concavity on a ball with inward transverse gradient |
| Types | `2 x 2` sign of the Schur complement | Haynsworth inertia: `In(H) = (m, 0, 0) + In(s)` |
| Mesh `(q, p)` | `(3,4), (4,5), (2,3)` | `(2d-1, 2d), (2d, 2d+1), (d, d+1)` ([P] §8) |
| Volume, sphere | `L^2`, `S^1` | `L^d`, `S^(d-1)` |
| Majorant | `(1+|b|+k)^4` | `(1+|b|+k)^(2d)` ([P] (13.4)) |
| Ledger | `r` | `r` in every d ([P] §10) |

## 2. Lemma F_d: ordinary-fold isolation in dimension d

Fix `b` real, `k > 0` and an orthonormal frame `R = (u, e_1, ..., e_m)`. Use local coordinates `(x, y)`, with `x`
real and `y` in `R^m`, centered at the midpoint. For small `r` put

    M_r = (-r/2, 0),  S_r = (r/2, 0),
    f(M_r) = b,  f(S_r) = b - k r^3,  grad f(M_r) = grad f(S_r) = 0.

These are `2d + 2` scalar observations. `Q_r` is the whole-field Gaussian regression law at them. The typed weight is
[P]'s

    W_r = |det H_(M_r) det H_(S_r)| 1{H_(M_r) < 0, index H_(S_r) = d - 1}.

**Lemma F_d.** There is a coupling `F_r` of `Q_r`, with contact limit `F_0`, such that:
1. `F_r -> F_0` almost surely in `C^4(T_L^d)`.
2. Let `A = D_y^2 F_0(0)`. Almost surely on `{A < 0}` (negative definite), for all small `r`, the only critical
   points of `F_r` in one fixed neighbourhood of `0` are `M_r` and `S_r`.
3. Almost surely on `{A < 0}`, for all small `r`, every other critical point of `F_r` continues a nondegenerate
   critical point of `F_0`, and their limiting values are pairwise distinct and differ from `b`. Off `{A < 0}` no
   local exhaustion is claimed: there §2.5 shows only that the typed weight vanishes eventually.
4. For each fixed `y` in `(0, 1]`, put `tau(r) = k r^3/y`. Almost surely on `{A < 0}`, `K_(tau(r))(F_r) <= 1`
   eventually.
5. On the whole coupling space,

       (W_r(F_r)/r^2) 1{K_(tau(r))(F_r) >= 2} -> 0   almost surely,                         (N0)

   and its expectation tends to 0.

Thresholds may depend on the sample and on `b`, `k`, `R` and `y`. No rate is claimed.

### 2.1 Coupling and contact law

[P] §3 orders the observations as
`O_r = (f(a), f_x(a), f(c), f_x(c), f_y1(a), f_y1(c), ..., f_ym(a), f_ym(c))`, with `a = -r/2` and `c = r/2`. It defines
`U_r = T_r O_r` by four axial rows and two rows per transverse direction:
- the axial rows `(f(a)+f(c))/2`, `(f(c)-f(a))/r`, `(f_x(c)-f_x(a))/r` and
  `(6/r^2)[f_x(a)+f_x(c)-2(f(c)-f(a))/r]`;
- for each `j`, the rows `(f_yj(a)+f_yj(c))/2` and `(f_yj(c)-f_yj(a))/r`.

[P] (3.2)–(3.4) give

    |det T_r| = 12 r^-(d+3),
    v_r = (b - k r^3/2, -k r^2, 0, 12k, 0, ..., 0),
    U_0 = (f, f_x, f_xx, f_xxx, f_y1, f_xy1, ..., f_ym, f_xym)(0),
    v_0 = (b, 0, 0, 12k, 0, ..., 0).                                                       (N1)

The `check.py` controls verify the first two lines exactly for `d = 2..6`.

For one smooth unconditioned sample F, define

    F_r(q) = F(q) + C_r(q) Sigma_r^-1 (v_r - U_r(F)),

with `Sigma_r = Cov U_r(F)` and `C_r(q) = Cov(F(q), U_r(F))`. This is [R] §2's regression formula. Gaussian regression
gives `law(F_r) = Q_r`, and `U_r(F_r) = v_r` exactly.

**Pathwise convergence.** Each row of `U_r(F)` converges to its row of `U_0(F)` for every smooth F. The fourth axial
row is an averaged third derivative ([P] §3): its two Taylor contributions are `(r^2/4) F_xxx` and `(r^2/12) F_xxx`.
The transverse rows are averages and difference quotients of `f_yj`.

[P] §2's rapidly summable positive spectrum gives:
- `C_r -> C_0` in global `C^4`;
- `Sigma_r -> Sigma_0`, which is positive definite by [P] §3, so `Sigma_r^-1 -> Sigma_0^-1`.

Hence, on the full-probability event that F is smooth,

    ||F_r - F_0||_(C^4(T_L^d)) -> 0.                                                       (N2)

This holds along the whole continuous family `r -> 0` at fixed `(b, k, R)`, and `F_0` has the regression law at
`U_0 = v_0`.

**The transverse block has a density.** Adjoin the `m(m+1)/2` entries `f_(yi yj)(0)`, `i <= j`, to `U_0`. They are
distinct derivative functionals, so [P] §2–§3 make the enlarged covariance positive definite. Hence

    A = D_y^2 F_0(0) has a nondegenerate Gaussian density on Sym(m),                        (N3)

and correlations with the rest of the field are retained.

`{det A = 0}` is the zero set of a nonzero polynomial on `Sym(m)`, so it has Lebesgue measure 0 and probability 0. In
particular `P(lambda_max(A) = 0) = 0`.

### 2.2 The complete local ridge

Fix a sample satisfying (N2), (N10) below, and `A < 0`. Choose `a_0 > 0` with `A <= -a_0 I`. Let `B_eta` be the closed
ball of radius `eta` in `R^m`.

**Choice of the box.**
- By continuity, choose `eta > 0` and `delta_1 > 0` such that `D_y^2 F_0 <= -(a_0/2) I` on
  `Q = [-delta_1, delta_1] x B_eta`.
- Since `grad_y F_0(0) = 0`, shrink to `delta <= delta_1` so that `|grad_y F_0(x, 0)| <= a_0 eta/8` for `|x| <= delta`.
- By (N2), for all small `r`, on `Q_delta = [-delta, delta] x B_eta`:

      D_y^2 F_r <= -(a_0/4) I,    |grad_y F_r(x, 0)| <= a_0 eta/6.                          (N4a)

**Transverse uniqueness.** Fix `|x| <= delta` and `|y| = eta`. Then

    <grad_y F_r(x, y), y> = <grad_y F_r(x, 0), y> + int_0^1 y^T D_y^2 F_r(x, t y) y dt
                         <= (a_0 eta/6) eta - (a_0/4) eta^2 < 0.

So `y -> F_r(x, y)` is strictly concave on the convex ball `B_eta`, and its gradient points strictly inward on the
boundary sphere.
- Its maximum over `B_eta` is attained in the interior, so it is a critical point.
- A strictly concave function has at most one critical point in a convex set, because any critical point is its
  unique maximizer.

Hence for every `|x| <= delta` there is exactly one `y = psi_r(x)` in the open ball with `grad_y F_r(x, psi_r(x)) = 0`.
This replaces C52's planar intermediate-value step.

**Regularity of the ridge.** The implicit function theorem gives `psi_r` in `C^3`, because `D_y^2 F_r` is invertible
and `F_r` is in `C^4`.
- Strong monotonicity of `-grad_y F_r` gives `|psi_r(x) - psi_0(x)| <= (4/a_0) sup |grad_y F_r - grad_y F_0|`.
- The derivatives of `psi_r` are rational in derivatives of `F_r` through order four. Their only denominators are
  `(D_y^2 F_r)^-1`, with norm at most `4/a_0`. For example `psi_r' = -(D_y^2 F_r)^-1 F_r,xy` on the ridge.
- Hence `psi_r -> psi_0` in `C^3([-delta, delta])`.

**The reduced function.** Put `g_r(x) = F_r(x, psi_r(x))` and `v = (1, psi_r'(x))`. Differentiating
`grad_y F_r(x, psi_r(x)) = 0` gives `D^2 F_r[v, (0, w)] = 0` for every `w` in `R^m`. The chain rule then gives

    g_r'   = F_r,x = D F_r[v],
    g_r''  = D^2 F_r[v, v] + D F_r[(0, psi_r'')] = D^2 F_r[v, v],
    g_r''' = D^3 F_r[v, v, v] + 3 D^2 F_r[v, (0, psi_r'')] + D F_r[(0, psi_r''')]
           = D^3 F_r[v, v, v].                                                              (N4)

Substituting `psi_r' = -(D_y^2 F_r)^-1 F_r,xy`:

    g_r'' = F_r,xx - F_r,xy^T (D_y^2 F_r)^-1 F_r,xy =: s_r,                                    (N5)

which is the Schur complement of the transverse block in the Hessian. Two exact checks support these:
- `check.py` verifies (N4), (N5) and `psi' = -(D_y^2 F)^-1 F_xy` exactly, by power series of the implicit ridge, on
  random rational quartics with `m = 1..5`.
- It also checks that `g'''` differs from the raw axial `F_xxx` off contact. The ridge correction is real.

**Contact values.** By (N1), `F_0,xy(0) = 0`, so `psi_0'(0) = 0`. Hence

    g_0'(0) = g_0''(0) = 0,    g_0'''(0) = F_0,xxx(0) = 12k > 0.

**Exactly two local critical points.** Shrink `delta` so that `g_0''' >= 9k` on `[-delta, delta]`. By (N2), (N4) and
`C^3` convergence of `psi_r`, `g_r''' >= 6k` there for small `r`, so `g_r'` is strictly convex.
- At the pins, `grad F_r = 0`, so `grad_y F_r(+-r/2, 0) = 0`. Transverse uniqueness gives `psi_r(+-r/2) = 0`, and then
  `g_r'(+-r/2) = 0`.
- A strictly convex function has at most two zeros.
- Every critical point of `F_r` in `Q_delta` lies on the ridge.

Hence `M_r` and `S_r` are the only critical points of `F_r` in `Q_delta`. This holds at every intermediate scale
within the fixed box at once.

**Types.** `g_r''` is strictly increasing, and `g_r'` vanishes at both pins, so `g_r''(-r/2) < 0 < g_r''(r/2)`.
Haynsworth's inertia additivity for `H = [[F_xx, F_xy^T], [F_xy, D_y^2 F]]` with invertible `D_y^2 F < 0` gives

    In(H) = In(D_y^2 F) + In(s) = (m, 0, 0) + In(s).                                         (N6)

So:
- `M_r` is a nondegenerate maximum;
- `S_r` is a nondegenerate saddle of index `m = d - 1`.

`check.py` verifies (N6) by exact symmetric elimination for `d = 2..6`. This is a statement about Hessian type, not
about elder matching.

**The contact field.** At `r = 0`, `g_0'(x) > 0` for every `x != 0` in `[-delta, delta]`. So `0` is the only critical
point of `F_0` in `Q_delta`.

### 2.3 Conditional genericity of remote critical points and values

This section concerns the contact law of `F_0` at fixed `(b, k, R)`. Consider the maps:

    Z_M(x, v) = (grad F_0(x), H F_0(x) v) in R^(2d),   x != 0, |v| = 1,      (q, p) = (2d-1, 2d),
    Z_V(x, z) = (grad F_0(x), grad F_0(z), F_0(x) - F_0(z)) in R^(2d+1),
                                                         x != z, both != 0,  (q, p) = (2d, 2d+1),
    Z_b(x)    = (grad F_0(x), F_0(x) - b) in R^(d+1),    x != 0,             (q, p) = (d, d+1).   (N7)

These are [P] §8's counts, and `check.py` lists them for `d = 2..6`; each has `p - q = 1`. For `d = 2` they are C52's
`(3,4)`, `(4,5)` and `(2,3)`.

**Positive conditional covariance.** Suppose a nonzero combination of the entries had zero variance modulo `U_0`. By
[P] §2, `Var(T f) = sum_n a_n |T^(n)|^2` with every `a_n > 0`, and every Fourier coefficient of the corresponding
distribution `T` vanishes. Hence `T = 0` as a distribution on `T_L^d`. Its remote part is supported away from `0`, and
then:
- **`Z_M`.** The second-order part at `x` is `sum_ij beta_i v_j d_i d_j delta_x`, with symbol `(beta . xi)(v . xi)`.
  This polynomial vanishes identically only if `beta = 0`, since `v != 0`. Equivalently, `H -> H v` maps `Sym(d)`
  onto `R^d`; `check.py` checks the rank. The first-order part then vanishes as well.
- **`Z_V`.** The parts at the distinct supports `x` and `z` each have order zero and order one. They vanish
  separately.
- **`Z_b`.** The argument is the same; the constant `b` shifts only the mean.

**Zero exclusion.**
- Exhaust each domain by countably many compact charts at positive distance from `0`, and for `Z_V` also from the
  diagonal. Cover the sphere by finitely many charts.
- Covariance continuity and positivity bound the Gaussian density uniformly on each chart, whatever the conditional
  mean.
- On `{||Z||_(C^1) <= N}`, an `epsilon`-mesh and a union bound give probability `O(N^p epsilon^(p-q))`, which tends to
  0. Then take the union over `N`.

Hence, almost surely:

    every off-origin critical point of F_0 is nondegenerate;
    distinct off-origin critical points have distinct values;
    no off-origin critical point has value b.                                               (N10)

A degenerate critical point `x` would give a zero of `Z_M` at a unit kernel vector `v`.

### 2.4 Global root exhaustion and value separation

This step is dimension-free; it is C52 §6 verbatim in `T_L^d`. It uses §2.2, so it holds on `{A < 0}`, which is fixed
throughout this subsection. Take a closed box `V` inside `Q_delta` with `0` in its interior.
- Outside `int V`, `F_0` has finitely many critical points `p_1, ..., p_n`, all nondegenerate. An accumulation point
  would be a degenerate critical point, contradicting (N10).
- The contraction `q -> q - H_j^-1 grad F_r(q)` on small balls `B_j` gives exactly one nondegenerate continued root
  `p_j(r) -> p_j` in each.
- On the compact remainder, `|grad F_0|` has a positive minimum, so `F_r` has no critical point there for small `r`.
- §2.2 exhausts `V`.

Hence the full critical set of `F_r` is eventually

    {M_r, S_r, p_1(r), ..., p_n(r)}.                                                        (N11)

Let `Delta` be the minimum of 1 and of every `|v_j - b|` and `|v_i - v_j|` (`i != j`), where `v_j = F_0(p_j)`. Then
`Delta > 0` by (N10). For small `r`, every critical-value gap involving a remote point is at least `Delta/2`. The two
pins differ by exactly `k r^3`.

Once `tau(r) < Delta/2`:
- a bar of lifetime at most `tau(r)` has its two endpoints among critical points whose values differ by less than
  `Delta/2`;
- so its endpoints are `M_r` and `S_r`;
- a maximum births at most one bar.

Hence `K_(tau(r))(F_r) <= 1`. The local pair is not asserted to be an actual elder pair; if it is not, the count is 0.

### 2.5 The typed boundary and the weighted vanishing statement

- **On `{A < 0}`,** §2.4 makes the event in (N0) eventually false.
- **On `{lambda_max(A) > 0}`,** let `w` be a unit eigenvector with `w^T A w > 0`. By (N2) and `M_r -> 0`,
  `D_y^2 F_r(M_r) -> A`, so `(0, w)^T H_(M_r) (0, w) > 0` eventually. Then `H_(M_r)` is not negative definite, and
  `W_r(F_r) = 0` eventually.
- **The remaining event** `{lambda_max(A) = 0}` has probability 0 by (N3).

This proves (N0).

[P] (4.1), (5.1) and (5.3) give, in every `d`, uniformly bounded moments of `W_r/r^2` of every finite order on a
compact neighbourhood of the fixed target ([P] §5: "det H_i/r and W_r/r^2 have uniformly bounded moments of every
finite order"). Almost-sure convergence plus uniform integrability give

    E[(W_r(F_r)/r^2) 1{K_(k r^3/y)(F_r) >= 2}] -> 0,                                          (N12)

and the same holds after multiplication by the actual elder indicator `0 <= J_eld <= 1`. This is an UNNORMALIZED
expectation; no lower floor for `Z_r` is used.

## 3. The weighted counting identity in dimension d

Let `H_tau(f) = 1{K_tau(f) >= 2}`. It is a bounded Borel whole-field mark on the Morse distinct-value locus, and is 0
off it. [E2]'s finite-measure identity on location x `C^2` field space admits it.

Counting once per actual finite bar gives

    B_tau = E sum_{(M,S) actual, 0 < ell <= tau} H_tau(f).                                    (C)

Use midpoint stationarity and the directed separation `S - M = r u`, with `u` in `S^(d-1)`. [P] §10's ledger is

    spatial r^(d-1) x height r^3 x pin 12 r^-(d+3) x determinant r^2 = 12 r,

which is checked in `check.py` for `d = 2..6`. The near marked intensity per unit volume is therefore

    r A_r^(H_tau)(q) dr dq,
    A_r^(H_tau) = 12 pi_r(v_r) E_Q[(W_r/r^2) J_eld H_tau] <= A_r,    q = (b, k, u).          (C1)

For `ell = k r^3` and `y = ell/tau`, `r dr = tau^(2/3) y^(-1/3) dy/(3 k^(2/3))`, also checked exactly. Hence

    B_tau^near/(L^d tau^(2/3))
      = int_0^1 int_{R x (0,inf) x S^(d-1)} 1{k >= tau y/r_0^3} y^(-1/3)/(3 k^(2/3))
                                            A_{(tau y/k)^(1/3)}^(H_tau)(q) dsigma db dk dy.   (C2)

## 4. Proof of Theorem O_d

**Near part.** For fixed `q` and `y`, `r = (tau y/k)^(1/3) -> 0` and `tau = k r^3/y`. By (N12) and continuity of
`pi_r(v_r)` at fixed `q`, `A_r^(H_tau)(q) -> 0`. [P] (13.4) gives, for all `b`, all `k > 0` and `0 < r <= r_0`,

    0 <= A_r^(H_tau)(q) <= A_r(q) <= H(b, k) = C (1 + |b| + k)^(2d) exp[-c(b^2 + k^2)].

The dominating function `y^(-1/3) H(b, k)/(3 k^(2/3))` is integrable on `(0,1] x R x (0, inf) x S^(d-1)`:
- `int y^(-1/3) = 3/2`;
- `k^(-2/3)` is integrable at 0;
- Gaussian tails control the polynomial;
- `S^(d-1)` has finite measure.

Dominated convergence gives `B_tau^near = o(L^d tau^(2/3))`.

**Far part.** For `r >= r_0`, `H_tau <= 1`, and [P] (14.1) gives `nu_eld^far(ell) <= C` for `0 < ell <= 1`. So
`B_tau^far <= L^d C tau = o(tau^(2/3))`. Near and far cover all ordered distinct endpoint pairs. This proves (O1).

**(O2) and (O3).** For every integer `K >= 0`,
- `K = 1{K > 0} + (K - 1)_+`;
- `(K - 1)_+ <= K 1{K >= 2}`;
- `2 P(K >= 2) <= E[K 1{K >= 2}]`.

[P] Theorem C, (1.3), gives `nu_eld^all(ell) ~ c_{d,L} ell^(-1/3)` per unit volume. Integrating over `(0, tau]` gives
`m_tau = L^d (3/2) c_{d,L} tau^(2/3) + o(tau^(2/3))` ([P] §12). With (O1) this yields (O2). Then
`TV(law(K_tau | K_tau > 0), delta_1) = P(K_tau >= 2)/p_tau <= B_tau/(2 p_tau) -> 0`, which is (O3).

**(O4).** Let `U_tau` be the empirical probability measure on a field's short bars, `I_tau = E[K_tau U_tau]/m_tau` and
`F_tau = E[1{K_tau > 0} U_tau]/p_tau`. Then

    I_tau = (p_tau/m_tau) F_tau + (e_tau/m_tau) D_tau,    D_tau = E[(K_tau - 1)_+ U_tau]/e_tau,

and therefore `TV(F_tau, I_tau) <= e_tau/m_tau`. This is dimension-free and uniform over marks. If `e_tau = 0`, the two
laws agree.

**(O5).** [T] Proposition 3 / (T4) is stated for `q` in `R x (0, inf) x S^(d-1)` and every `d >= 2`. It gives
`I_tau -> (2/3) y^(-1/3) dy g(q) dq` in total variation, with `g = A_0/(3 c k^(2/3))` and zero cemetery mass. (O4)
transfers this to `F_tau`. The coefficient is [P] (15.2):

    c_{d,L} = Gamma(7/6)/(24^(1/3) sqrt(pi))
                 int_{S^(d-1)} p_G(0) p_(V_u)(0) tau_u^(4/3) D_u dsigma(u) > 0.

Unbounded mark moments do not converge without a separate uniform-integrability argument.

## 5. Boundaries

- Every source interface is a retained hypothesis:
  - the actual global elder identification;
  - Theorem C's positive leading mean;
  - (13.4) and (14.1);
  - E2's Borel-mark identity;
  - T's (T4).

  This packet does not reaccept any of them.
- The count is of actual ordinary finite bars. It is not a uniqueness theorem for auxiliary witnesses or for
  replacement bars. C50/C51 (Math-#233, #234) are not premises.
- `d` and `L` are fixed. No uniformity in `d` is claimed. Constants and thresholds depend on `d`, `L` and the sample.
- Same account as every other lane, so organizational-independence credit is 0. Dylan Roy's personal reading is
  PENDING.

## 6. Exact controls

`check.py` uses the standard library and rationals only. It checks the finite identities:
- (N1) `|det T_r| = 12 r^-(d+3)` and `T_r(pins) = v_r`;
- (N4) and (N5) by exact power series of the implicit ridge, together with the contact values;
- (N6) Haynsworth inertia;
- the mesh counts and the rank of `H -> H v`;
- the ledger exponent;
- the lifetime Jacobian.

These cover `d = 2..6`. `test_check.py` adds unit tests and 17 implementation mutants. Each mutant must fail in both
`-B -S` and `-B -O -S`. `verify_sources.py` authenticates the seven `current_required` sources by bytes, SHA256 and Git
blob. It checks both the working-tree copy and the historical `commit:path -> blob` entry, via `git ls-tree`. The two
`cited_unmerged` C52 entries are checked the same way when their commit is present locally, and otherwise reported as
unavailable; they are not premises.

The controls do not prove the continuum analysis, including:
- genericity;
- uniform integrability;
- dominated convergence;
- the persistence identification.

## 7. Requested nonauthor review (OpenAI / xAI lanes)

- **Slice A, §2.2:** the ball argument for transverse uniqueness, the `C^3` ridge convergence, (N4)–(N6), and the
  two-zero conclusion.
- **Slice B, §§2.1, 2.3, 2.5:** the density of `A` on `Sym(m)`, the `{lambda_max(A) = 0}` null boundary, the
  conditional covariance positivity for (N7), and the uniform integrability.
- **Slice C, §§0, 3–5:** the source scope in general `d`, (C1)–(C2), the domination, and the occurrence and mark
  conclusions. This includes checking that [T] (T4) and [E2] are indeed used only within their stated general-d scope.
