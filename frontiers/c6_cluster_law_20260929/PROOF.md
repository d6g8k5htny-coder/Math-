# The cluster law of the C6 window count: `r^(-3) Q_r^W{N = n} -> nu(n)`, with `nu` carried by `{1, 2}`

**Object:** CL-C6-CLUSTER-LAW-20260929-v1.2.
**Version:** v1.2, 30 September 2026 (v1.0 and v1.1 on 29 September; v1.1 answered the OpenAI Codex review of Math-#159:
spectral chart in place of the shear chart, exclusion lemma in the full transverse space, `K_4 <= kappa` split with a
marked Kac–Rice tail, domination without `D^(-1)`, `n in {1, 2}` in Proposition 4.4, uniform integrability in
Corollary X; v1.2 (and its follow-up on the singular-slice `kappa` mixture and the raw three-site whitening, after
review 5360034762) answers the OpenAI nonauthor review 5359895261 of v1.1: the full normalizer restored in both marked
displays (Lemmas 4.2, 5.2), Lemma 5.1 re-proved by whitening against the midpoint five-jet, the choice of `kappa` by
Fubini on the limit law, an explicit integrable majorant for §6.2 from the new Lemma 3.6 on the sheared cubic, and the
corrected §8 remark: every extra window critical point is a saddle; the Corollary X scope wording follows the OpenAI
follow-up 5359999003).
**Author:** Anthropic Claude (Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`), 29 September 2026.
**Disposition:** author-side proof candidate. **Nonauthor analytic review is required.** This note stacks on merged
sources only: [LP], [DL], [C6], [RM], [RC], [EDL], [LM], and it answers the "unknown conditional cluster law" left
open by [RCL] (Math-#153) and the "no positional law of the pairs" non-claim of [C6] §9.
**Scientific effect:** NONE. No `STATUS`, `PROOF_INDEX` verdict, `GRAPH` node, claim, `lemma_closed` flag, catalog
entry, prize or source body changes. Same GitHub account as every other lane; zero organizational-independence credit.

## 0. Why this note exists

[C6] proves `E_(Q_r^W)[(N)_q] <= C_q r^3` for the number `N` of window critical points other than the pins, in every
fixed dimension, and [EDL] proves the matching lower bound `Q_r^W{N >= 2} >= c r^3`. [RCL] turned these bounds into
elementary rare-cluster consequences and stated their essential limitation: the conditional law of `N` given `N > 0`,
that is the measure `nu_r(n) = r^(-3) Q_r^W{N = n}`, is "actual, generally unknown, `r`-dependent", it has weighted-`l1`
subsequential limits (its Theorem S), and the premises alone cannot force a unique limit (its §6 examples).

This note proves that in the exact Gaussian model the limit exists, identifies it, and shows that it is carried by
`{1, 2}`: at scale `r` around the pins the field has, on the rare event that produces window critical points at all,
the normal form of a planar cubic with the two pins among its critical points; a planar cubic has at most four critical
points; so at most two extra ones exist, and their number in the window is a measurable function of the scaled
third-order jets. Away from the pins the count is the single-point contact intensity of [RM]. The two regions do not
interact at order `r^3`. The mechanism is the one that [EDL] §§3–9 and [LM] §§2–6 used for the lower bound; here it is
run as a dominated-convergence limit over the whole rare configuration set instead of on one open box.

## 1. Setting and results

### 1.1 Model and count

Fix `d >= 2`, `m = d - 1`, `L > 0`. `f` is the centered variance-one Gaussian field on `X = R^d/(L Z^d)` with the exact
normalized periodized Gaussian covariance of [LP] §1. Fix compact `B = [b_-, b_+]` and `K = [k_-, k_+]`, `0 < k_-`.
Frames `R` range over `O(d)`; `u = R e_1` is the axial direction and `y in R^m` the transverse coordinates, with the
midpoint of the pins at the origin. The pins are

    M = -(r/2) u,  S = (r/2) u,  f(M) = b,  f(S) = b - k r^3,  grad f(M) = grad f(S) = 0.

`Q_r` is the Gaussian regression on these `2(d+1)` observations; `F_j(H) = |det H|` if `H` is nonsingular with `j`
negative eigenvalues and `0` otherwise; `W_r = F_d(H_M) F_(d-1)(H_S)`, `Z_r = E_(Q_r) W_r`, `dQ_r^W = (W_r/Z_r) dQ_r`;
`I_r = (b - k r^3, b)`. `N = N_r` is the number of critical points of `f` in `X minus {M, S}` with height in `I_r`, all
indices. For `0 < rho <= 1` and `A >= 4` write

    N_near^A = #{ window critical points, other than the pins, in the ball |X| <= A r },
    N_mid^(A,rho) = #{ ... with A r < |X| < rho },
    N_far^rho = #{ ... with |X| >= rho },

distances measured from the midpoint, so that `N = N_near^A + N_mid^(A,rho) + N_far^rho`. Constants `C, c, r_*`
depend on `d, L, B, K` and, where stated, on `A` or `rho`; never on `r, b, k, R`. `K_4` denotes a fixed multiple of
`1 + ||f||_(C^4(X))`. Nothing is uniform as `k -> 0`, as marks grow, or as `d` or `L` vary. No constant is numerical.

### 1.2 Statements

Section 3 defines, for every frame `R` and mark pair `(b, k)`, a reduced weight `m_(b,k,R)` on `R^4` (a nonnegative
continuous function of the scaled soft curvature `s` and of the three planar cubic jets `(a_3, beta, c_3)`, obtained
from the `Q_0`-density of the midpoint jets on the singular slice by integrating out the stable directions, (3.11)),
the pin weight

    w_0(s, a_3, beta) = [ -6k(s - beta/2) - a_3^2/4 ]_+ . [ a_3^2/4 - 6k(s + beta/2) ]_+,          (1.1)

the planar cubic

    F_0(X, Z) = 2k X^3 - (3k/2) X - k/2 + (s/2) Z^2 + (a_3/2)(X^2 - 1/4) Z + (beta/2) X Z^2 + (c_3/6) Z^3,   (1.2)

whose critical points other than `(-1/2, 0)` and `(1/2, 0)` number at most two (Lemma 3.2), and the count

    N_oo(s, a_3, beta, c_3) = #{ critical points (X, Z) of F_0, other than (-+1/2, 0), with F_0(X, Z) in (-k, 0) }.

Let `z_0 = z_0(b, k, R) > 0` be the limiting normalizer of [LP] (5.4), `Lambda_j(x; b, k, u)` the contact kernel of
[RM] (13) and `Lambda = sum_j Lambda_j`. Put, for `n in {1, 2}`,

    nu_near(n) = z_0^(-1) integral_(R^4) m(s, a_3, beta, c_3) w_0(s, a_3, beta) 1{ N_oo = n } ds da_3 dbeta dc_3,   (1.3)

    nu(2) = nu_near(2),      nu(1) = nu_near(1) + k integral_X Lambda(x; b, k, u) dx.                                 (1.4)

**Theorem N (cluster law).** All the integrals in (1.3)–(1.4) are finite, the functions `nu(1), nu(2)` are strictly
positive and continuous on `B x K x O(d)`, and, uniformly on that compact set,

    r^(-3) Q_r^W{ N = 1 } -> nu(1),     r^(-3) Q_r^W{ N = 2 } -> nu(2),     r^(-3) Q_r^W{ N >= 3 } -> 0.      (1.5)

**Corollary Lambda (asymptotic factorial moments).** Uniformly on the same set, for every fixed integer `q >= 1`,

    r^(-3) E_(Q_r^W)[ (N)_q ] -> Lambda_q,    Lambda_1 = nu(1) + 2 nu(2),   Lambda_2 = 2 nu(2),   Lambda_q = 0 (q >= 3).   (1.6)

In particular `E_(Q_r^W) N ~ Lambda_1 r^3`, `E_(Q_r^W)[N(N-1)] ~ 2 nu(2) r^3`, and every factorial moment of order at
least three is `o(r^3)`; the Palm excess of [C6] Corollary P converges: `E_sb[N - 1] -> 2 nu(2)/(nu(1) + 2 nu(2))`.

**Corollary S (the limit of [RCL] is unique and identified).** With `nu_r(n) = r^(-3) Q_r^W{N = n}`, the weighted-`l1`
convergence of [RCL] Theorem S holds along the full family `r -> 0`, with the limit `nu = nu(1) delta_1 + nu(2) delta_2`;
`lambda = nu(1) + nu(2)`; the positive conditional law `F_r = Law(N | N > 0)` converges in total variation to
`F_oo = (nu(1) delta_1 + nu(2) delta_2)/lambda`; the canonical compound Poissonization `CP(p, F_r)` of [RCL] Theorem C
has the same `r -> 0` limits; and the independent-replica limit of [RCL] §7 is `CP(t nu)` with this explicit `nu`.
None of the three non-implication examples of [RCL] §6 occurs in the model.

**Corollary X (near point-intensity limit, with a sequential radius limit).** For every bounded continuous `phi` on
`R^2 x R`, uniformly on the compact parameter set,

    r^(-3) E_(Q_r^W) sum_(X in near window critical points) phi( (X . u)/r, |X_perp|/r, (f(X) - b)/r^3 )
       -> z_0^(-1) integral m w_0 sum_(critical points (X,Z) of F_0 in the window) phi( X, |Z|, F_0(X,Z) ),

where the inner sum runs over the extra critical points of `F_0`, `X` is the scaled axial coordinate and `|Z|` the
scaled transverse distance (§3.2: the rotated chart makes the physical ball a scaled ball). Scope: this is a statement
about the intensity measure of the near points, obtained with `r -> 0` at a fixed near radius `A` first and `A -> oo`
second (§6.5). It does not by itself give convergence of the law of the random configuration (expectations of sums
determine only the intensity), and it concerns near points only: the remote singleton part `k integral Lambda` of
`nu(1)` escapes the `1/r` scaling.

### 1.3 What the results are not

Existential constants, fixed `d` and `L`, compact marks. No rate in (1.5)–(1.6); no numerical value of `nu(1)`, `nu(2)`
or `Lambda_q`; no uniformity as `k -> 0`; no statement about the elder selection of the extra points; no spatial
independence between distinct pin pairs; no configuration law for the scaled positions (Corollary X is a near
point-intensity limit with a sequential radius limit); nothing about the remote pair kernel beyond consistency with [RC]. §9 lists
the non-claims. The note is conditional on the consumed sources at the exact bytes of §2.

### 1.4 The planar case

For `d = 2` there are no stable directions: `m = 1`, the chart of §3.2 is trivial, `m(s, a_3, beta, c_3)` is the
`Q_0`-density of `(f_zz, f_xxz, f_xzz, f_zzz)(0)` at `f_zz = 0`, evaluated at `(a_3, beta, c_3)`, and every consumed
regional bound is a reviewed planar statement ([PP], [CP], [IW] through [DL], [RM], [RC]). Theorem N at `d = 2` is
therefore conditional on this note's own steps only.

## 2. Sources consumed, with the exact interface

Identities (bytes, sha256, git blob, commit on `main`) are in `SOURCE_MAP.json`.

| Tag | Source | What is consumed |
|---|---|---|
| [LP] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` | The model; §2 distinct-site jet rank and positive spectrum; §3 the contact frame `U_r` with target `v_r -> v_0`, the uniform covariance sandwich and the density bound (3.5) for the transverse Hessian; §4 uniform conditional derivative moments; (5.1)–(5.5) endpoint identities, block determinant identity, `Z_r/r^2 -> z_0 > 0`; (13.3) the polynomial target-growth version of the conditional `C^m` moments. |
| [DL] | `frontiers/d5_dimension_lift_20260929/PROOF.md` | Theorem I_d, (1.5)–(1.6): the window shell bound `E_(Q_r^W) N_(r,j)({A_0 r <= |X| <= rho}) <= C r^3 (A_0^(-2) + rho^2)`, uniform in `A_0 >= 4` and `rho <= s_0`; the regime frames of §§4–6 (as re-expressed in [C6] §6) for Lemma 5.2. |
| [C6] | `frontiers/c6_palm_route_20260929/PROOF.md` | Theorem Q (uniform integrability in Corollary Lambda); Lemma 5.1 (marked Kac–Rice for `sigma(f)`-measurable marks, gradient-only kernel); (5.3) the conditional Hölder insertion and the §6 regime table with the squared determinant weight (Lemma 5.3); Lemma 4.1's frame parameter `beta` and the regime bounds `beta <= poly(chi, |v|^(-1), r^(-1), s^(-1))`. |
| [RM] | `frontiers/remote_window_20260924/PROOF.md` | Theorem A (2) with the contact kernel `Lambda_j` of (13), its continuity, positivity and the remote nondegeneracy of §§2–3; the Kac–Rice representation (12). |
| [RC] | `frontiers/remote_collision_20260928/PROOF.md` | Corollary D (fixed-remote second factorial moment `<= C r^5 |E|`) and Corollary E (`Q_r^W{N_j(E) >= 1} = k r^3 integral_E Lambda_j + O(r^4 |E|)`), for `E` contained in `D_rho`, every fixed `d`. |
| [EDL] | `frontiers/elder_dimension_lift_20260928/PROOF.md` | §2 (complete third-order jets and their positive-definite joint covariance with `U_0`), (A11)–(A16) (the rare set and the conditional `C^4` control), (A17) (the normal form on the soft plane; here written in a rotated rather than sheared frame), (A26)–(A28) (the rescaled full gradient and the stable block), §9 (block-triangular stability of the extra critical points). Used as the source of the normal form; the shear chart (A8)–(A10) is replaced by the spectral chart of §3.2; the lower bound (A4) is not consumed. |
| [LM] | `frontiers/window_multiplicity_laws_20260928/LOCAL_MULTIPLICITY.md` | (L4)–(L8) the planar normal form and its exact cubic with two extra saddles (used as the positivity witness), (L7) the `C^2` remainder, §6 the exponent arithmetic `r . r^4 / r^2`. |
| [RCL] | `frontiers/c6_rare_cluster_laws_20260929/PROOF.md` | §§2, 4, 6, 7 statements (Theorems C, S, the identity (6.2), the replica limit (7.1)), consumed only in Corollary S as the statements whose hypotheses this note identifies. |

Nothing else is imported. In particular no elder-selection statement, no numerical enclosure and no Fourier-cutoff
tail is used. For `d = 2` the planar sources behind [DL] are [PP] `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md`,
[CP] `reviews/d5_local_collar_20260928/COLLAR_PROOF.md`, [IW] `frontiers/intermediate_window_20260928/PROOF.md`, cited
where [DL] cites them.

## 3. The scaled model near the pins

### 3.1 Midpoint jets and the contact frame

Write the transverse coordinates as `y = (z, w)` with `z in R` along the first transverse axis `e_z = R e_2` and
`w in R^n`, `n = d - 2` (empty for `d = 2`). At the midpoint `0` let

    A = D_y^2 f(0) in Sym_m,     T = ( partial^alpha f(0) )_(|alpha| = 3, alpha != (3, 0, ..., 0)),

the transverse Hessian and the third derivatives other than `f_xxx`, and `J = (A, T)`. By [LP] §3 the contact frame
`U_r` is an invertible re-expression of the `2(d+1)` pins with target `v_r -> v_0 = (b, 0, 0, 12k, 0, ..., 0)` and
contact limit `U_0 = (f, f_x, f_xx, f_xxx, f_y, f_xy)(0)`; the entries of `(U_0, J)` are every independent derivative
of order at most three at one site, once each ([EDL] §2), so their covariance is uniformly positive definite on
`O(d)`, and `J` under `Q_r` is a nondegenerate Gaussian vector with means, covariances and inverse covariances
converging, uniformly on the compact parameter set, to those of `J` under `Q_0`, the regression on `U_0 = v_0`. Write
`p_r(j)` for the Lebesgue density of `J` under `Q_r` and `p_0` for its limit; both are bounded by `C exp(-c |j|^2)`
([LP] (3.5) for the `A` block, the same Schur argument for `T`).

For every target `j` of `J` and every `r`, the regular conditional law of `f` given `(U_r, J) = (v_r, j)` is the Gaussian
regression `f = m_r(j) + Res_r`, with `m_r(j)` affine in `j` with `C^4`-bounded coefficient functions and `Res_r` a
centered Gaussian field independent of `(U_r, J)` whose `C^4(X)` moments of every order are bounded uniformly in `r`
([EDL] (A14)–(A15), [LM] (L12)); by [LP] (13.3),

    E[ K_4^p | U_r = v_r, J = j ] <= C_p (1 + |j|)^p      for every fixed p.                                          (3.1)

Since `Res_r -> Res_0` in `C^4(X)` in every `L^p` (the coefficient functions converge with all derivatives, [LP] §3),
and `m_r(j_r) -> m_0(j)` in `C^4` whenever `j_r -> j`, the conditional laws converge: for every bounded functional `Phi`
of the field that is continuous at `Q_0`-almost every `f` in the `C^4` topology, `E[Phi(f) | (U_r, J) = (v_r, j_r)] ->
E[Phi(f) | (U_0, J) = (v_0, j)]`. This is the device of [LP] §13 and [RM] §5, and it is used below with `Phi` the
indicator that the scaled count equals `n`.

### 3.2 The spectral chart and the singular slice

For `d = 2`, `A = f_yy(0)` is a scalar; put `sigma = A`, and there is no `D`, no `U` and no `w`. For `d >= 3` write the
eigenvalues of `A` as `lambda_1, ..., lambda_m` and let `sigma` be the eigenvalue of least modulus; `Q_r`-almost
surely it is unique and simple, since `A` has a Lebesgue density ([LP] (3.5)). Let `u_1` be a unit eigenvector for
`sigma`, `U in O(m)` an orthogonal matrix with first column `u_1`, and `D = diag(lambda_2, ..., lambda_m)` the
remaining eigenvalues in a fixed order, so that

    A = U diag(sigma, D) U^T,      |sigma| <= |lambda_j|  (j >= 2).                                                 (3.2)

The Weyl integration formula for real symmetric matrices (e.g. Anderson, Guionnet, Zeitouni, *An Introduction to Random
Matrices*, §2.5) writes Lebesgue measure on `Sym_m` in these coordinates as

    dA = c_m  prod_(j >= 2) |sigma - lambda_j| . Delta(D)  dsigma dD dU,      Delta(D) = prod_(2 <= i < j) |lambda_i - lambda_j|,   (3.3)

with `dU` the Haar measure on `O(m)` and `c_m` a fixed positive constant (the restriction `|sigma| <= |lambda_j|`
selects one of the `m` eigenvalue labellings). The density factor is a polynomial in `(sigma, D)`, and it equals
`c_m |det D| Delta(D)` on the singular slice `{sigma = 0}`.

Rotate the transverse coordinates by `U`: `f~(x, z, w) = f( R diag(1, U) (x, z, w) )`, with `z in R` along `u_1` and
`w in R^n`, `n = m - 1`. Since `diag(1, U)` is orthogonal, `f~` has the same `C^4` norm as `f`, its transverse Hessian
at `0` is `diag(sigma, D)` (so `f~_zw(0) = 0`, `f~_ww(0) = D`), and the physical ball `|X| <= A r` is the scaled ball
`X^2 + Z^2 + |rW|^2 <= A^2` in the coordinates `(x, z, w) = (rX, rZ, r^2 W)` used below. Let `tau` be the third
derivatives of `f~` at `0` other than `f~_xxx`; `tau` is the image of `T` under a fixed orthogonal representation of
`diag(1, U)`, so `|tau| = |T|` and `T -> tau` has Jacobian one for fixed `U`. Write `j = (sigma, U, D, tau)` and
`chart(j)` for the raw jet `(A, T)`.

The chart replaces the shear of [EDL] (A8)–(A10) by a rotation; no unbounded coefficient enters, at the price of the
polynomial density (3.3). Configurations in which a second eigenvalue is also small (`|lambda_2|` small) are not
excluded from the chart; they are handled by the domination of §4, whose dominating function does not involve
`D^(-1)` (Lemma 4.3), and by the almost-sure nonsingularity of `D` in the pointwise limits.

### 3.3 The normal form

Let `F_r(X, Z, W) = [ f~(rX, rZ, r^2 W) - b ] / r^3` and

    s = sigma / r,   a_3 = tau_xxz,   beta = tau_xzz,   c_3 = tau_zzz,   Q_j(X, Z) = (tau_xxw_j / 2)(X^2 - 1/4) + tau_xzw_j X Z + (tau_zzw_j / 2) Z^2.

**Lemma 3.1 (normal form, [EDL] (A17), (A26)–(A28); [LM] (L6)–(L7)).** For every `R_0 >= 1` there is `C = C(d, R_0)`
such that on `{|(X, Z)| <= R_0, |W| <= R_0}`, uniformly in `b, k, R`, `0 < r <= 1`,

    || F_r(., ., 0) - F_0 ||_(C^2) <= C r K_4,                                                                     (3.4)
    r^(-2) grad f~(rX, rZ, r^2 W) = ( partial_X F_0, partial_Z F_0, D W + Q(X, Z) ) + O( r K_4 (1 + |D|) ),          (3.5)

with `F_0` as in (1.2) (the pins are exactly retained: `F_0(-+1/2, 0) = 0, -k` and `grad F_0(-+1/2, 0) = 0`, checked
exactly in the finite control `NF`). Moreover, for `|(X, Z)| <= R_0` and physical `|w| <= R_0 r`,
`|partial_w f~| >= (sigma_min(D) - C r K_4 R_0)|w| - r^2 |Q| - C r^3 K_4`, so if `D` is nonsingular and
`r <= r_0(K_4, R_0, D)`, every critical point of `f~` in the physical ball of radius `R_0 r` has
`|W| <= C |Q(X,Z)| / sigma_min(D) + 1`.

*Proof.* The Taylor expansion of `f~` at the midpoint through order three, with the pin identities of [LM] §3
(`f~_xxx(0) = 12k + O(r K_4)`, `f~_x(0) = -(r^2/8) f~_xxx(0) + O(r^3 K_4)`, `f~_z(0) = -(r^2/8) f~_xxz(0) + O(r^3 K_4)`,
`f~_xx(0), f~_xz(0) = O(r^2 K_4)`, `f~(0) - b = -(r^3/24) f~_xxx(0) + O(r^4 K_4)`, and, from the two transverse gradient
pins, `f~_w(0) = -(r^2/8) f~_xxw(0) + O(r^3 K_4)`, `f~_xw(0) = O(r^2 K_4)`, while `f~_zw(0) = 0` exactly), is (A17) of
[EDL] on `w = 0` and gives (3.4). Differentiating in `w` and using `D_w^2 f~(0) = D`, `D_(zw) f~(0) = 0` gives (3.5),
the last block being `r^2 (D W + Q) + O(r^3 K_4)` before division. The lower bound on `|partial_w f~|` is (3.5) read at
physical `w = r^2 W` with `|W| <= R_0 / r`: the quadratic remainder `K_4 |w|^2 <= K_4 R_0 r |w|` is relative to the
linear term `D w`. ∎

Consequently, when `D` is nonsingular and `r <= r_0(K_4, R_0, D)`, the critical points of `f~` in the physical ball of
radius `R_0 r` are in bijection with the zeros of the reduced planar gradient

    grad G_r(X, Z),   G_r(X, Z) = F_r(X, Z, W_*(X, Z)),   W_*(X, Z) = the unique solution of the third block of (3.5) = 0,

`W_* = -D^(-1) Q(X, Z) + O(r K_4 (1 + |D^(-1)|)^2)`, and

    || G_r - F_0 ||_(C^2({|(X,Z)| <= R_0})) <= C r K_4 (1 + |D^(-1)|)^2 (1 + |tau|)^2.                              (3.6)

Indeed `F_r(X, Z, W) - F_r(X, Z, 0) = r (Q . W + W^T D W / 2) + O(r^2 K_4)` on bounded `W`, and the implicit function
`W_*` is `C^2` with the stated bound because the third block of (3.5) has derivative `D + O(r K_4)` in `W`. The index of a
critical point of `f~` equals the index of the corresponding critical point of `G_r` plus the index of `D` ([EDL] §9:
the full Hessian is block triangular up to `O(r)` with diagonal blocks the planar Hessian of `G_r` and `D`), and its
height satisfies `(f~ - b)/r^3 = G_r` at the point. The bound (3.6) is used only for the pointwise limits of §4.2, at
fixed jets with `D` nonsingular; it is not used for domination.

### 3.4 The planar cubic

**Lemma 3.2 (at most two extra critical points).** For every `(k, s, a_3, beta, c_3)` with `k > 0`, the resultant of
`partial_X F_0` and `partial_Z F_0` with respect to `Z` equals `(X^2 - 1/4) Q_2(X)` identically in
`(X, s, a_3, beta, c_3, k)`, where

    Q_2(X) = c_2 X^2 + s c_1 X + c_0,
      c_2 = a_3^3 c_3/4 - 3 a_3^2 beta^2/16 - (9/2) a_3 beta c_3 k + 3 beta^3 k + 9 c_3^2 k^2,
      c_1 = -a_3^2 beta/4 - 3 a_3 c_3 k + 6 beta^2 k,
      c_0 = 3 s^2 beta k - ( a_3 beta/8 - 3 c_3 k/2 )^2                                                         (3.7)

(finite control `RS`, exact polynomial identity). Let `E_k` be the set of `(s, a_3, beta, c_3)` for which the two
quadratics `partial_X F_0, partial_Z F_0` have a common factor, or `Q_2` vanishes identically, or some common zero other
than the pins is degenerate, or has height in `{-k, 0}`. `E_k` is a proper algebraic subset of `R^4`, hence
Lebesgue-null, and off `E_k` the critical points of `F_0` are isolated, at most four with multiplicity (Bézout for two
conics), two of them the pins; so the extra real critical points number at most two, they are nondegenerate, and
`N_oo in {0, 1, 2}`. On `E_k` put `N_oo := 0` (the value is irrelevant: `E_k` is null for every `k`).

*Proof.* The resultant identity is an exact computation (the Sylvester determinant of two quadratics in `Z`), verified
symbolically in `RS`. The pins are the zeros of `partial_X F_0 = 6k X^2 - 3k/2 + a_3 X Z + (beta/2) Z^2` and
`partial_Z F_0 = s Z + (a_3/2)(X^2 - 1/4) + beta X Z + (c_3/2) Z^2` on `Z = 0`, which explains the factor `X^2 - 1/4`.
Off `E_k`, for each root `X_*` of `Q_2` the two quadratics in `Z` are not proportional (they have no common factor), so
they share at most one root `Z`; if they are proportional at `X_*`, the extra points are the at most two zeros of
`partial_X F_0(X_*, .)` (the [LM] configuration, where control `EX` exhibits `X_* = -3/4` as a double root of `Q_2`).
Bézout's theorem bounds the number of isolated common zeros of two conics by four. `E_k` is defined by polynomial
equations in the jets (common factor: vanishing of the resultant as a polynomial in `X`; degeneracy and boundary
heights: vanishing of the Hessian determinant, or of `F_0` or `F_0 + k`, at a common zero, eliminated through the
resultant), and it is proper because the configurations of §7 (exact rational examples with `0`, `1` and `2` extra
critical points in the window, all nondegenerate) lie outside it. The example `(0, 0, 0, 0)`, where the lines
`X = -+1/2` consist of critical points, lies in `E_k`. ∎

### 3.5 Large soft curvature excludes near critical points

**Lemma 3.3 (exclusion, full transverse space).** There are `C = C(d)` and `r_0(kappa, R_0) > 0` such that, if
`K_4 <= kappa`, `r <= r_0(kappa, R_0)`, and the transverse Hessian `A` at the midpoint satisfies `|lambda_j| >= S r`
for every eigenvalue, with

    S >= S_*(tau, R_0, kappa, k) := C (1 + |tau|)^2 (1 + R_0)^3 (1 + kappa)^2 / k^2,                               (3.8)

then the only critical points of `f` in the physical ball of radius `R_0 r` about the midpoint are the two pins.
Equivalently, on `{K_4 <= kappa}`, `N^(R_0) >= 1` forces `|s| = |sigma|/r <= S_*(tau, R_0, kappa, k)` for `r <= r_0`.

*Proof.* Work in the original pin frame (no rotation is needed), with scaled coordinates `x = rX`, `y = rY`,
`|(X, Y)| <= R_0`. From the two transverse gradient pins and the pin identities ([LM] §3, [EDL] (A17), the same
computation as (3.4) in every transverse direction),

    grad_y f(rX, 0) = (r^2/2)(X^2 - 1/4) grad_y f_xx(0) + O(r^3 K_4 (1 + R_0)^3),      D_y^2 f(rX, 0) = A + O(r K_4 R_0),

so at a critical point, `0 = grad_y f(rX, rY) = r^2 [ (1/2)(X^2 - 1/4) grad_y f_xx(0) ] + (A + O(r K_4 R_0)) r Y + O(r^2 K_4 R_0^2)`.
Dividing by `r` and using `|A Y| >= S r |Y|`,

    (S r - C r K_4 R_0) |Y| <= C r (1 + |tau|)(1 + R_0)^2 + C r K_4 R_0^2,     i.e.     |Y| <= delta := C (1 + |tau| + kappa R_0^2)(1 + R_0)^2 / (S - C kappa R_0),

which is small for `S` large. In the axial equation, `f_x(rX, rY)/r^2 = 6k X^2 - 3k/2 + X grad_y f_xx(0) . Y + O((1 + |tau|) |Y|^2) + O(r K_4 (1 + R_0)^3)`
([LM] §3, [EDL] (A17): the term `f_xy(0) . Y / r` is `O(r K_4 |Y|)` by the pin identity `f_xy(0) = O(r^2 K_4)`), so
`|6k X^2 - 3k/2| <= C (1 + |tau|) R_0 delta + C (1 + |tau|) delta^2 + C r kappa (1 + R_0)^3`. Since
`|6k X^2 - 3k/2| = 6k |X - 1/2| |X + 1/2|`, for `delta` and `r` small this forces `X` within `C (1 + |tau|) R_0 delta / k`
of `-+1/2`. Hence every critical point in the scaled ball lies within scaled distance
`rho := delta + C (1 + |tau|) R_0 delta / k` of a pin.

At a pin `P`, `grad f(P) = 0` exactly and, for `|xi| <= 1`, `|grad f(P + r xi)| >= sigma_min(H_P) r |xi| - K_4 r^2 |xi|^2 / 2`.
The Hessian `H_P` is `r` times the block matrix with axial entry `-+6k + O(r K_4)`, mixed axial–transverse row
`O(1 + |tau|)` (the entries `-+(1/2) grad_y f_xx(0) + O(r K_4)`), and transverse block `A/r + O(K_4)` whose eigenvalues
have modulus at least `S - C kappa`. For `S >= C (1 + |tau|)^2 / k + C kappa`, the Schur complement of the transverse
block is `-+6k + O((1 + |tau|)^2 / (S - C kappa))`, so `sigma_min(H_P) >= c k r`, and no other zero of `grad f` lies
within scaled distance `rho_pin := c k / kappa` of `P`. The two conclusions are incompatible as soon as
`rho < rho_pin`, which holds when `S >= S_*` with the constant of (3.8). ∎

The lemma uses no planar reduction and no inverse of `D`; the only randomness it sees is through the deterministic
bound `K_4 <= kappa`. Note that on the singular slice `|sigma| <= |lambda_j|` for all `j`, so the hypothesis is exactly
`|s| >= S_*`.

### 3.6 The weight on the singular slice

**Lemma 3.4 (pin Hessians).** With `M_2(M) = [[-6k, -a_3/2], [-a_3/2, s - beta/2]]` and `M_2(S) = [[6k, a_3/2],
[a_3/2, s + beta/2]]` (exact second derivatives of `F_0` at the pins, control `NF`), the Hessians of `f~` at the pins are

    H~_i = [[ r M_2(i) + O(r^2 K_4), r c_i + O(r^2 K_4) ], [ r c_i^T + O(r^2 K_4), D + O(r K_4) ]],   i in {M, S},

with `c_i in R^(2 x n)` linear in `tau` (the entries `-+tau_xxw/2, -+tau_xzw/2`), and

    det H~_i = r^2 det D . det M_2(i) + O( r^3 K_4^d (1 + |tau|)^2 (1 + |s|)^2 ),                                 (3.9)

exactly as polynomials: the determinant of a matrix whose two soft rows are `O(r)` and whose stable block is `O(1)` is
`r^2` times the product of the soft-block and stable-block determinants plus `r^3` times a polynomial in the entries
(control `BD` checks this for `d = 3` and `d = 4` with exact rational arithmetic in `r`); the remainder involves no
inverse of `D`. The rotation `diag(1, U)` is orthogonal, so `det H_i = det H~_i` and the index is unchanged. Moreover,
by Hadamard's inequality applied to the two soft rows, the row of the least stable eigenvalue `lambda_2` (whose
entries are `O(r K_4)` off the diagonal and `lambda_2 + O(r K_4)` on it) and the remaining rows,

    r^(-4) W_r <= C (1 + |s| + |tau| + K_4)^4 ( |lambda_2| + r K_4 )^2 K_4^(2d - 6)      (d >= 3),                   (3.10)

and `r^(-4) W_r <= C (1 + |s| + |tau| + K_4)^4` for `d = 2`.

*Proof.* The entries follow from Lemma 3.1 by differentiating (3.4)–(3.5) once more at the pins:
`partial_X^2 F_0 = 12k X + a_3 Z`, `partial_X partial_Z F_0 = a_3 X + beta Z`, `partial_Z^2 F_0 = s + beta X + c_3 Z`,
evaluated at `(-+1/2, 0)`, and the mixed soft–stable entries are the derivatives of `Q`. The determinant expansion is
the Leibniz formula: every term contains at least two factors from the two soft rows, each `O(r)`; the terms with
exactly two such factors and the identity permutation on the stable block give `r^2 det M_2 det D`; the remaining terms
carry `r^3`. (3.10) is Hadamard's inequality with the stated row norms. ∎

**Lemma 3.5 (weight limit).** Write `w_0` as in (1.1). If `D` is nonsingular and `det M_2(M) != 0 != det M_2(S)`,
then under the conditional law of §3.1 with `sigma = r s`,

    r^(-4) W_r -> (det D)^2 w_0(s, a_3, beta)     in probability as r -> 0.

Here `w_0 > 0` exactly when `M_2(M)` is negative definite (index `d` at `M`, given `D < 0`) and `M_2(S)` has one negative
eigenvalue (index `d - 1` at `S`); if `D` is not negative definite the limit weight is `0` because the index conditions
fail.

*Proof.* (3.9) gives `r^(-2) det H~_M -> det D . det M_2(M)`, and the index of `H~_M` converges to `index(M_2(M)) +
index(D)` because eigenvalues are continuous and the limits are nonsingular. `F_d(H_M) = |det H_M| 1{index = d}` gives
the first factor; the second factor is the same at `S`. The condition `index M_2(M) = 2` is `det M_2(M) > 0` (its
`(1,1)` entry is `-6k < 0`), and `index M_2(S) = 1` is `det M_2(S) < 0` (its `(1,1)` entry is `6k > 0`); these are the
two positive parts in (1.1). ∎

### 3.7 The reduced weight

Let `p_0` be the `Q_0`-density of the raw jet `J = (A, T)` (§3.1). Define

    m(s, a_3, beta, c_3) := integral p_0( chart(0, U, D, tau) ) c_m |det D| Delta(D) (det D)^2 1{D < 0} dU dD dtau_rest,   (3.11)

where `tau_rest` collects the entries of `tau` other than `(a_3, beta, c_3)` (those involving a `w` index), `dU` is the
Haar measure, and `c_m |det D| Delta(D)` is the density (3.3) on the singular slice. The integrand does not depend on
`s`; `m` is a bounded, strictly positive, continuous function of `(a_3, beta, c_3)` with Gaussian decay (the density
`p_0` is Gaussian and nondegenerate, `|chart(0, U, D, tau)| >= c (|D| + |tau|)`, and the Weyl factor is polynomial), and
it depends continuously on `(b, k, R)`. In `d = 2`, `m(s, a_3, beta, c_3) = p_0(0, a_3, beta, c_3)`, the density of
`(f_zz, f_xxz, f_xzz, f_zzz)(0)` at `f_zz = 0`.

### 3.8 The typed window geometry of the planar cubic

Put `B = beta - a_3^2/(12k)`, `D = ( c_3 - a_3 beta/(4k) + a_3^3/(72k^2) )/2`, `u = X + a_3 Z/(12k)`, and
`C(u) = 2k u^3 - (3k/2) u - k/2 = (k/2)(u - 1)(2u + 1)^2`. Then, identically in `(X, Z, s, a_3, beta, c_3, k)`,

    F_0(X, Z) = G(u, Z) := C(u) + (s + B u) Z^2 / 2 + (D/3) Z^3                                                  (3.12)

(control `SH`, as the polynomial identity with `k` cleared). The shear `(X, Z) -> (u, Z)` is linear and unimodular,
so critical points, heights and Hessian determinants of `F_0` and `G` correspond, and the pins are `(u, Z) = (-+1/2, 0)`.
The typed domain of Lemma 3.5 is `{w_0 > 0} = {s < -|B|/2}`, since `det M_2(M) = -6k(s - B/2)` and
`det M_2(S) = 6k(s + B/2)`, and there `w_0 = 9k^2(4s^2 - B^2)`.

**Lemma 3.6 (saddles only, and the range of `s`).** Let `s < -|B|/2` and let `(X, Z)` be a critical point of `F_0`
other than the pins with `F_0(X, Z) in (-k, 0)`. Then `Z != 0`, the planar Hessian of `F_0` at `(X, Z)` has determinant
`-3k(B + 4 s u) < 0`, so the point is a nondegenerate saddle (index `1` in the plane, hence index `d - 1` in the full
model when the stable block is negative definite), and

    -s <= 2|B| + (32 k D^2)^(1/3).                                                                                  (3.13)

In particular, on `{w_0 > 0}`, `N_oo >= 1` forces `|s| <= 2|B| + (32 k D^2)^(1/3) <= C_k (1 + |a_3| + |beta| + |c_3|)^2`,
with `C_k` bounded for `k` in a compact subset of `(0, oo)`, and every counted point is nondegenerate (the degeneracy
clause in the definition of `E_k` is vacuous on the typed window). Both statements are exercised on an exact rational
family in control `TW`.

*Proof.* Write `x = -s > |B|/2 >= 0` and `w = s + B u`. The gradient of `G` is `partial_u G = 6k u^2 - 3k/2 + (B/2) Z^2`,
`partial_Z G = Z (w + D Z)`, and its Hessian determinant is `12 k u (w + 2 D Z) - B^2 Z^2`. A critical point with
`Z = 0` has `6k u^2 = 3k/2`, so it is a pin; hence `Z != 0` and `w + D Z = 0`.

*Case `D != 0`.* Then `Z = -w/D`, and the first gradient equation reads `B w^2 / D^2 = 3k (1 - 4u^2)`. The height is
`G = C(u) + w Z^2/2 + (D/3) Z^3 = C(u) + w^3/(6 D^2)`, and the Hessian determinant is
`12 k u (w - 2w) - B^2 w^2/D^2 = -12 k u w - 3k B (1 - 4u^2) = -3k (B + 4 u (w - B u)) = -3k (B + 4 s u)`.

(a) `B = 0`: `u = -+1/2`. At `u = 1/2`, `w = s` and `G = -k + s^3/(6D^2) < -k`, outside the window. At `u = -1/2`,
`w = s` and `G = -x^3/(6 D^2)`, in the window iff `x^3 < 6 k D^2`, which implies (3.13); the determinant is
`-3k . 4 s (-1/2) = 6 k s < 0`.

(b) `B > 0`: `1 - 4u^2 = B w^2/(3k D^2) >= 0` gives `|u| <= 1/2`, and `|u| = 1/2` forces `w = 0`, a pin; so `|u| < 1/2`.
Then `w = -x + B u <= -x + B/2 < 0` and `C(u) <= 0`, so `G > -k` gives `|w|^3/(6D^2) < k + C(u) <= k`, i.e.
`|w| < (6 k D^2)^(1/3)`; with `|w| = x - B u >= x - B/2` this is `x < B/2 + (6 k D^2)^(1/3)`, which implies (3.13).
For the sign, write `|w|^3/(6 D^2) = |w| k (1 - 4u^2)/(2B)` and `k + C(u) = (k/2)(u + 1)(2u - 1)^2` (the identity
`2 + (u - 1)(2u + 1)^2 = (u + 1)(2u - 1)^2`): the window inequality `G > -k` becomes `|w| (1 + 2u) < B (u + 1)(1 - 2u)`,
i.e. `x < B u + B (u + 1)(1 - 2u)/(1 + 2u) = B/(1 + 2u)`. Hence `B + 4 s u = B - 4 x u > B (1 - 2u)/(1 + 2u) > 0` when
`u > 0`, and `B - 4 x u >= B > 0` when `u <= 0`: the determinant is negative.

(c) `B < 0`: `4u^2 - 1 = |B| w^2/(3k D^2) >= 0` gives `|u| >= 1/2`, and `|u| = 1/2` forces `w = 0`, a pin; so `|u| > 1/2`.
Now `w^3/(6D^2) = w k (4u^2 - 1)/(2|B|)` with `w = -x - |B| u`, and expanding,

    G = (k/2)(2u + 1) [ -1 - (x/|B|)(2u - 1) ].

For `u > 1/2` both factors give `G <= -k`: outside the window. For `u < -1/2` put `t = -u > 1/2`, so
`G = -(k/2)(2t - 1)( x (2t + 1)/|B| - 1 )`; since `x > |B|/2` the bracket is positive, `G < 0`, and `G > -k` reads
`(2t - 1)( x (2t + 1) - |B| ) < 2|B|`. The determinant is `-3k( -|B| + 4 x t ) < 0` because `4 x t > 2 x > |B|`. For (3.13)
assume `x >= 2|B|` (otherwise it holds) and put `delta = 2t - 1 > 0`: the window inequality gives `delta (2x - |B|) < 2|B|`,
hence `delta < 4|B|/(3x) <= 2/3` and `t < 5/6`; then `w^2 = (3 k D^2/|B|) delta (delta + 2) < 32 k D^2/(3x)`, while
`|w| = x - |B| t >= 7x/12`; so `x^3 < (144/49)(32/3) k D^2 < 32 k D^2`.

*Case `D = 0`, `B != 0`.* Then `w = 0`, i.e. `u = x/B`, and `Z^2 = 3k (1 - 4u^2)/B`. The height is `G = C(u)`, which lies
in `(-k, 0)` iff `u in (-1, 1) \ {-+1/2}` (`C(-1) = -k`, `C(-1/2) = 0`, `C(1/2) = -k`, `C(1) = 0`, `C` decreasing on
`[-1/2, 1/2]`, `k + C(u) = (k/2)(u + 1)(2u - 1)^2`), so `x = |B| |u| < |B|`; the Hessian determinant is `-B^2 Z^2 < 0`.

*Case `D = 0`, `B = 0`.* `partial_Z G = s Z` with `s != 0`: there is no critical point off `Z = 0`. ∎

## 4. The near limit

### 4.1 Scaled representation

Fix `A >= 4` and write `N^A = N_near^A`. For every Borel set `E` of field configurations,

    Q_r^W(E) = Z_r^(-1) integral p_r(j) E[ W_r 1_E | U_r = v_r, J = j ] dj,                                        (4.1)

by the tower property with the regular conditional law of §3.1. Change variables to the spectral coordinates
`(sigma, U, D, tau)` with the density (3.3) and then `sigma = r s`:

    r^(-3) Q_r^W(E) = (r^2 / Z_r) integral ds dU dD dtau  p_r( chart(rs, U, D, tau) )  c_m prod_(j>=2) |rs - lambda_j| Delta(D)  r^(-4) E[ W_r 1_E | U_r = v_r, J = chart(rs, U, D, tau) ],   (4.2)

the `s`-integral being over `{ |rs| <= min_j |lambda_j| }`. The factor `r` from `dsigma = r ds` and the factor `r^(-4)`
from the weight combine with `r^2/Z_r -> 1/z_0` ([LP] (5.4)) to the exponent `1 + 4 - 2 = 3` of [LM] §6.

### 4.2 Convergence of the scaled count

**Lemma 4.1.** Fix `A >= 4`, fix `kappa > 0` outside the countable set `Kap_0` defined after the proof, and fix `(s, U, D, tau)` with `D` nonsingular and `(s, a_3, beta, c_3)` outside `E_k` and outside
the null set of jets for which an extra critical point of `F_0` lies on the circle `X^2 + Z^2 = A^2`. Let
`j_r = chart(rs, U, D, tau)` and `j_0 = chart(0, U, D, tau)`. Then, under the conditional laws `Q_(r, j_r)` of §3.1,

    1{ N^A = n } 1{K_4 <= kappa}  ->  1{ N_oo^A = n } 1{K_4 <= kappa}     in probability,
    N_oo^A := #{ extra critical points (X, Z) of F_0 with X^2 + Z^2 < A^2 and F_0(X, Z) in (-k, 0) },

and likewise for the counts restricted to any fixed index, and for the scaled positions and heights (Corollary X).

*Proof.* Couple the conditional laws as in §3.1: `f = m_r(j_r) + Res_r` with `Res_r -> Res_0` in `C^4` in probability
and `m_r(j_r) -> m_0(j_0)` in `C^4`. Fix a realization with `K_4 < oo` along which the convergence holds; `K_4(f_r) -> K_4(f_0)` for it, so `1{K_4 <= kappa}`
converges whenever `K_4(f_0) != kappa`, an event of full `Q_(0, j_0)`-probability for the jets admitted below. By Lemma 3.1 (applicable since `D` is nonsingular and `r -> 0`), every
critical point of `f~` in the physical ball `X^2 + Z^2 + |rW|^2 <= A^2` has bounded `W`, so its `(X, Z)` lies in the disc
of radius `A + O(r)`, and by (3.6) `G_r -> F_0` in `C^2` on the disc of radius `A + 1`. The extra critical points of `F_0`
there are finitely many and nondegenerate, none lies on the circle of radius `A`, and none has height in `{-k, 0}`.
Ordinary `C^1` stability (the inverse function theorem on disjoint small discs around the nondegenerate zeros, plus
`|grad F_0| >= delta > 0` on the complement of those discs in the disc of radius `A + 1`, which `C^1`-closeness
preserves for small `r`) gives: for small `r`, `grad G_r` has exactly one zero in each small disc and none elsewhere;
each converges to the corresponding zero of `grad F_0`, its `G_r`-height converges (so its window membership
stabilizes), its planar Hessian converges (so its index stabilizes), and by the bijection of §3.3 these are exactly
the critical points of `f~` in the physical ball other than the pins, which are the two fixed nondegenerate zeros
`(-+1/2, 0)` of `grad F_0` and attract no other zero. Hence `N^A -> N_oo^A` for every such realization; convergence in
probability follows, together with the convergence of scaled positions and heights. ∎

**Choice of `kappa`.** Only the limit law enters the argument above, and Proposition 4.4 integrates it over the
singular slice, not over full jet space: the limit targets are `j_0 = chart(0, U, D, tau)`, and the coordinate `s`
does not enter `Q_(0, j_0)`. Let `mu_l` be the finite measure `dU ⊗ Leb(dD) ⊗ Leb(dtau) ⊗ Q_(0, chart(0, U, D, tau))`
on `{ |D| + |tau| <= l } x C^4(X)`, `l in N`, with `dU` the Haar measure; this is exactly the measure on the slice that
(4.2) reduces to at `r = 0`. The `K_4`-marginal of each `mu_l` has countably many atoms; let `Kap_0` be the countable
union of these atom sets over `l`. For `kappa` outside `Kap_0`, Fubini on `mu_l` gives
`integral Q_(0, chart(0, U, D, tau)){K_4 = kappa} dU dD dtau = mu_l{K_4 = kappa} = 0` for every `l`, hence
`Q_(0, chart(0, U, D, tau)){K_4 = kappa} = 0` for `(dU ⊗ Leb ⊗ Leb)`-almost every `(U, D, tau)`, and therefore for
almost every `(s, U, D, tau)` in the domain of (4.2) and (4.4). These are the jets admitted in Lemma 4.1 and all that
Proposition 4.4 integrates over. No union of atom sets over uncountably many conditional laws is used, and no
full-dimensional null set is invoked on the codimension-one slice. The complement of `Kap_0` is unbounded, and
`kappa -> oo` in Proposition 4.4 and §6.5 is taken along it. (For the uniformity in the parameters, `Kap_0` is formed
at the limit parameter of the sequential argument, which is the only place where the pointwise statement is used.)

### 4.3 The large-`K_4` tail

**Lemma 4.2.** For every `A >= 4` and every fixed `p >= 1` there is `C(A, p)` such that for `0 < r <= r_*` and
`kappa >= 1`,

    r^(-3) Q_r^W{ N^A >= 1, K_4 > kappa } <= C(A, p) kappa^(-p/2).                                                   (4.3)

*Proof.* `Q_r^W{N^A >= 1, K_4 > kappa} <= E_(Q_r^W)[N^A 1{K_4 > kappa}]`, and the mark `W_r 1{K_4 > kappa}` is
`sigma(f)`-measurable and nonnegative, so [C6] Lemma 5.1 under `Q_r` (gradient-only kernel, all heights, which dominates
the windowed count), divided once by the full normalizer, gives

    E_(Q_r^W)[ N^A 1{K_4 > kappa} ] <= Z_r^(-1) sum_j integral_(|X| <= A r) p_(grad f(X) | U_r)(0) E_(Q_r)[ W_r F_j(H_X) 1{K_4 > kappa} | U_r, grad f(X) = 0 ] dX.

The left side is under the weighted law; the right side is under `Q_r`, with the original weight `W_r` inside the
conditional expectation and `Z_r^(-1)` outside, once each (this is the form of [C6] (6.3) and of [DL] (4.10); the
unnormalized integral is `Z_r` times the left side, not the left side).

Cauchy–Schwarz on the conditional expectation and Markov's inequality with the conditional moments
`E[K_4^p | U_r, grad f(X) = 0] <= C_p (1 + beta_X)^p` ([C6] Lemma 4.4 with the frame parameter `beta_X` of [C6] Lemma 4.1)
bound the integrand by `p_(grad f(X)|U_r)(0) E[(W_r F_j(H_X))^2 | .]^(1/2) (C_p (1 + beta_X)^p)^(1/2) kappa^(-p/2)`. By
[C6] (5.3) and the §6 regime table, the density times the square root of the squared-weight conditional moment is
bounded, in every regime, by the source's unmarked intensity bound times `(1 + beta_X)^(3d)`, and the regime's
Gaussian penalty absorbs any fixed power of `(1 + beta_X)` by raising the index of the exponential series in [C6] §6.2
(the recorded ledgers `2n >= 6 + 3d`, `2n/3 >= 15 + 39d` are the choices for [C6]'s degree); the regional ledgers of
[C6] §6, which are stated for the normalized quantity `Z_r^(-1) E_(Q_r) N^(W_r Xi)`, then give
`Z_r^(-1) integral_(|X| <= A r) (...) dX <= C(A, p) r^3`. ∎

### 4.4 Domination on `{K_4 <= kappa}`

**Lemma 4.3.** Fix `A >= 4` and `kappa >= 1`. There is `r_0(kappa, A) > 0` and an integrable function
`g_(A, kappa)(s, U, D, tau)` on `R x O(m) x R^n x R^(dim tau)`, not depending on `r`, such that for `0 < r <= r_0` and all
`(s, U, D, tau)` in the domain of (4.2),

    p_r( chart(rs, U, D, tau) ) c_m prod_(j>=2) |rs - lambda_j| Delta(D)  r^(-4) E[ W_r 1{ N^A >= 1 } 1{K_4 <= kappa} | U_r = v_r, J = chart(rs, U, D, tau) ] <= g_(A, kappa)(s, U, D, tau),

and the same without the indicator `1{N^A >= 1}`, with `integral_(|s| <= S) g < oo` for every `S`.

*Proof.* Write `j = chart(rs, U, D, tau)`. On `{K_4 <= kappa}`, Lemma 3.3 gives `1{N^A >= 1} <= 1{ |s| <= S_*(tau, A, kappa, k) }`,
a deterministic indicator with `S_*` polynomial in `|tau|` by (3.8); note that it does not involve `D`. On the same
event, (3.10) gives `r^(-4) W_r <= C (1 + |s| + |tau| + kappa)^4 (|lambda_2| + r kappa)^2 kappa^(2d - 6)`, again with no
inverse of `D`. The density satisfies `p_r(j) <= C exp(-c |j|^2) <= C exp(-c (|D|^2 + |tau|^2))` (the chart is an
isometry in `T` and `|A| >= |D|`), and the Weyl factor is bounded by `C (1 + |s| r + |D|)^(m(m-1)/2)`. Hence the left
side is at most

    g_(A, kappa) := C(A, kappa) exp(-c (|D|^2 + |tau|^2)) (1 + |D|)^(m(m-1)/2) (1 + |s| + |tau|)^4 (|lambda_2| + 1)^2 1{ |s| <= S_*(tau, A, kappa, k) },

which is integrable: bounded `s`-range for each `tau`, polynomial growth in `|tau|` against the Gaussian factor
(`S_*` is polynomial in `|tau|`), Gaussian decay in `D`, and finite Haar measure in `U`. Without the count indicator,
the bound is the same without `1{|s| <= S_*}`, integrable over bounded `s`. ∎

Remark (nearly singular stable block). Nothing in `g_(A, kappa)` blows up as `lambda_2 -> 0`: the factor
`(|lambda_2| + r kappa)^2` in (3.10) only helps, and the exclusion range `S_*` is independent of `D`. The inverse
`D^(-1)` enters only the pointwise limits of Lemma 4.1, at fixed jets with `D` nonsingular, which is `Q_0`-almost
every jet.

### 4.5 The near limit for fixed `A`

**Proposition 4.4.** For every `A >= 4` and `n in {1, 2}`, uniformly on the compact parameter set,

    r^(-3) Q_r^W{ N^A = n } -> nu_near^A(n) := z_0^(-1) integral m w_0 1{ N_oo^A = n } ds da_3 dbeta dc_3,          (4.4)

and `r^(-3) Q_r^W{ N^A >= 3 } -> 0`. The integrals are finite. Moreover `nu_near^A(n) -> nu_near(n)` as `A -> oo`, and
`integral m w_0 N_oo ds da_3 dbeta dc_3 < oo`.

*Proof.* Fix `kappa` as in Lemma 4.1 and split `1 = 1{K_4 <= kappa} + 1{K_4 > kappa}`. By Lemma 4.2 the second part
contributes at most `C(A, 2) kappa^(-1)` to `r^(-3) Q{N^A = n}` for `n >= 1`, uniformly in `r`. For the first part apply
(4.2) with `E = {N^A = n, K_4 <= kappa}`. The integrand converges pointwise, for `Q_0`-almost every `(s, U, D, tau)`
(`D` nonsingular, jets off `E_k` and off the circle-null set), to
`p_0(chart(0, U, D, tau)) c_m |det D| Delta(D) (det D)^2 w_0(s, a_3, beta) E_0[1{K_4 <= kappa} | j_0] 1{N_oo^A = n}`, by
Lemma 4.1, Lemma 3.5 (convergence in probability of `r^(-4) W_r` together with the uniform `L^2` bound (3.1) gives
convergence of the conditional expectation of its product with a bounded functional) and the continuity of the
density and of the Weyl factor. Lemma 4.3 dominates uniformly in `r`. The prefactor `r^2/Z_r -> z_0^(-1)`. Hence

    limsup / liminf  r^(-3) Q{N^A = n}  are within  C(A, 2)/kappa  of  z_0^(-1) integral (...) E_0[1{K_4 <= kappa} | j_0] 1{N_oo^A = n};

let `kappa -> oo` along the complement of `Kap_0` (monotone convergence on the right, `E_0[1{K_4 <= kappa}|j_0] -> 1`) and integrate out `(U, D, tau_rest)`
to obtain (4.4) with the reduced weight (3.11). For `n >= 3` the pointwise limit of the indicator is zero by Lemma 3.2.
Finiteness (see also the explicit majorant of §6.2, from Lemma 3.6): by Fatou's lemma applied along `r -> 0` to the `K_4 <= kappa` part of the representation (4.2) with `E = {N^A >= 1}` (the integrand converges pointwise to the (4.4)-integrand times `E_0[1{K_4 <= kappa}|j_0]`, and the latter tends to `1` as `kappa -> oo`), `integral m w_0 N_oo^A <= liminf r^(-3) E N^A <= C`, where the last bound is [DL] Theorems P_d, C_d and I_d (pin balls and collar of scaled radius `4`, shells from `4r` to `A r`: `C r^3 (1 + sum_j (r/s_j)^2 + s_j^2) <= C r^3` uniformly in `A <= 1/r`). The `A -> oo` limit: `N_oo^A` is nondecreasing in `A` with limit `N_oo`, so
`integral m w_0 N_oo < oo` by monotone convergence and the uniform bound; then `1{N_oo^A = n} -> 1{N_oo = n}`
pointwise (for every jet, once `A` exceeds the radius of the finitely many extra critical points) and is dominated by
`N_oo`, so dominated convergence gives `nu_near^A(n) -> nu_near(n)`. Uniformity on the compact parameter set: the
dominating functions and all limits depend continuously on `(b, k, R)`, so a sequence of parameters along which the
convergence fails would have a convergent subsequence contradicting the pointwise statement at the limit parameter,
exactly as in [LP] §5. ∎

## 5. The middle and far regions, and the absence of cross terms

### 5.1 Shells

By [DL] Theorem I_d, (1.6), summed over the `d + 1` indices, for `A >= 4` and `rho <= s_0`,

    E_(Q_r^W) N_mid^(A, rho) <= C r^3 ( A^(-2) + rho^2 ),                                                         (5.1)

with `C` independent of `A` and `rho`.

### 5.2 The far region

By [RC] Corollary E applied to `E = D_rho = {|x| >= rho}` and summed over indices, and by [RC] Corollary D,

    Q_r^W{ N_far^rho >= 1 } = k r^3 integral_(D_rho) Lambda dx + O(r^4),      Q_r^W{ N_far^rho >= 2 } <= C r^5,      (5.2)

with constants depending on `rho`. The function `rho -> k integral_(D_rho) Lambda` is nondecreasing as `rho` decreases
and bounded: indeed, for `rho' < rho`, `k integral_(rho' <= |x| < rho) Lambda = lim_r r^(-3) E N_(r)({rho' <= |x| < rho})
<= C rho^2` by (5.2) applied on the annulus and (5.1). So `k integral_X Lambda dx := lim_(rho -> 0)` exists and is
finite, and `k integral_(D_rho) Lambda -> k integral_X Lambda` with error at most `C rho^2`.

### 5.3 The witness-conditioned far first moment

**Lemma 5.1.** Let `X` be a point of the near region `|X| <= A r` and `Q_X` the regression of `Q_r` on the additional
observation `grad f(X) = 0` (the gradient-only kernel of [C6] Lemma 5.1, defined for every `X`). There are
`r_0(A, rho) > 0` and `C(rho)` such that, for `r <= r_0` and `rho <= s_0`, with `Y_x = (grad f(x), f(x))`,

    Cov_(Q_X)( Y_x ) >= (gamma_rho/4) I     for every x in D_rho,                                                    (5.3a)
    E_(Q_X)[ N_far^rho ] <= C(rho) k r^3 (1 + beta_X)^(2d),                                                          (5.3)

where `gamma_rho > 0` is the `r`-independent floor (5.3b) and `beta_X` is the frame parameter of [C6] Lemma 4.1 for the
regime containing `X` (bounded by a polynomial in `chi`, `|v|^(-1)`, `r^(-1)` as recorded in the [C6] §6 table).

*Proof.* Two facts. Let `J_5` be the complete midpoint Taylor jet through order five (the `C(d+5, 5)` coefficients
`D^alpha f(0)/alpha!`), a nondegenerate Gaussian vector that does not depend on `r`.

(i) By the distinct-site jet rank of [LP] §2, `(J_5, Y_x)` is a list of distinct derivative functionals at the two
distinct sites `0` and `x`, so its covariance is positive definite; the Schur complement is continuous in `(x, R)` and
`{x in D_rho} x O(d)` is compact, so

    Cov( Y_x | J_5 ) >= gamma_rho I,     Cov( Y_x ) <= M I,                                                          (5.3b)

with `gamma_rho > 0` and `M` independent of `r`.

(ii) The vector to whiten is chosen regime by regime so that its whole remainder is small relative to its floor.
In the collar (`|X| >= r/4` in the scaled pin-ball coordinates, [DL] §5), let `V` be the raw three-site scaled vector
of [DL] §5.2, `V = ( f(ra), r grad f(ra), f(rb), r grad f(rb), f(rc), r grad f(rc) )`, with `a, b` the pins and
`c = X/r`. Taylor's formula through total degree five gives `V = B_c D_r J_5 + R_V` with `||R_V||_(L^2) <= C r^6`, where
`B_c` has a uniform row singular-value floor on the collar ([DL] §5.1, Lemma) and `D_r = diag(r^|alpha|) >= r^5 I`; with
`Cov(J_5) >= c I` this gives `Cov(V) >= c r^10 I` for small `r` (the remainder is absorbed exactly as in [DL] (5.1)). In
the pin ball let `V = (U_r, Y)`: the contact frame `U_r` of [LP] §3 is `T_U J_5 + R_U` with `||R_U||_(L^2) <= C r` and
`Cov(U_r) >= c I`, and `Y` is the normalized gradient frame of [DL] (4.2), `Y = dvec + B J + R` with `||R||_(L^2) <= C r`
and `Cov_(Q_r)(Y) >= c_0 I` ([DL] (4.5)); the joint floor `lambda_min Cov(V) >= c` follows from the two floors and the
bounded entries (for jointly Gaussian `(U, Y)`, `Var(a . U + b . Y) >= Var(b . Y | U)` and
`Var(a . U + b . Y) >= (std(a . U) - std(b . Y))^2`). In both cases

    V = T_V J_5 + R_V,     ||Cov(V)^(-1/2)|| ||R_V||_(L^2) <= eta_r := C r,                                          (5.3c)

by `C r^(-5) . C r^6` in the collar and `C . C r` in the pin ball, uniformly in `X` in the near region. The σ-algebra
of `Q_X`, generated by `(U_r, grad f(X))`, is contained in that of `V`: equal in the pin ball (`Y` is an invertible
image of `grad f(X)` given `U_r`), and strictly smaller in the collar, where `V` also carries the witness value `f(X)`.

Whitening. Put `Ut := Cov(V)^(-1/2) (V - E V)`, so `Cov(Ut) = I` and `Ut = T J~_5 + E` with `J~_5` the centred jet and
`||E||_(L^2) <= eta_r` by (5.3c). The σ-algebra of `Q_X` is that of `V`, hence that of `Ut`. For a unit vector `e`,
`Var(e . Y_x | V) = min_a Var(e . Y_x - a . Ut)`, attained at `a = Cov(e . Y_x, Ut)` with `|a|^2 <= Var(e . Y_x) <= M`.
Since `e . Y_x - a . T J~_5` is `e . Y_x` minus a linear function of `J_5`, its variance is at least `Var(e . Y_x | J_5)
>= gamma_rho` by (5.3b). Therefore

    std( e . Y_x - a . Ut ) >= std( e . Y_x - a . T J~_5 ) - |a| ||E||_(L^2) >= gamma_rho^(1/2) - M^(1/2) eta_r >= gamma_rho^(1/2)/2

for `r <= r_0(A, rho)`, i.e. `Cov(Y_x | V) >= (gamma_rho/4) I`, uniformly in `X` and in the regime. Conditional
covariances of a Gaussian vector increase under coarsening of the conditioning (`Cov(Y | G) = Cov(Y | F) + Cov(E[Y | F] | G)`
for `G` contained in `F`), so `Cov_(Q_X)(Y_x) = Cov(Y_x | U_r, grad f(X)) >= Cov(Y_x | V) >= (gamma_rho/4) I`. This is
(5.3a); no witness value is pinned in the kernel `Q_X`, it is only used inside the whitened vector.

Consequences. By (5.3a) the conditional density of `Y_x` at `(0, t)` under `Q_X` is at most `C(rho)`. For the
conditional mean of `H_x` use the frame of `Q_X` itself, `V' = (U_r, Lambda)` with `Lambda` the regime frame of [C6]
Lemma 4.1 (an invertible image of `grad f(X)` given `U_r`): `E[H_x | V', Y_x]` is `E H_x` plus a linear function, with
coefficients bounded by `M'^(1/2)` (bounded cross-covariances against the whitened vector), of the whitened target
`Cov(V')^(-1/2)(tau' - E V')` and of `Y_x - E Y_x`. The joint floor of `V'` is at least a constant times
`min(1, lambda_min Cov_(Q_r)(Lambda))` (same inequalities as in (ii)), the target of `U_r` is bounded, and
`||Cov_(Q_r)(Lambda)^(-1)||` and `|tau - E Lambda|` are what `beta_X` bounds, so the whitened target has norm at most
`C (1 + beta_X)^(3/2)`; the conditional covariance of `H_x` is bounded. Hence `E[ F_j(H_x) | Y_x = (0, t), V ] <= C E[(1 + |H_x|)^d | ...] <=
C (1 + beta_X)^(3d/2) (1 + |t|)^d`. Apply the Kac–Rice formula of [RM] (12) under `Q_X` to `D_rho` and the window of
length `k r^3`, on which `|t|` is bounded: (5.3) follows, with the exponent `2d >= 3d/2`. ∎

**Lemma 5.2 (no near–far cross term).** For `A >= 4` and `rho <= s_0`,

    Q_r^W{ N_near^A >= 1, N_far^rho >= 1 } <= E_(Q_r^W)[ N_near^A 1{ N_far^rho >= 1 } ] <= C(A, rho) r^(9/2).       (5.4)

*Proof.* The mark `W_r 1{N_far^rho >= 1}` is `sigma(f)`-measurable and nonnegative, so [C6] Lemma 5.1 under `Q_r`
(gradient-only kernel, all heights, which dominates the windowed near count), divided once by the full normalizer, gives

    E_(Q_r^W)[ N_near^A 1{N_far >= 1} ] <= Z_r^(-1) sum_j integral_(|X| <= A r) p_(grad f(X) | U_r)(0) E_(Q_r)[ W_r F_j(H_X) 1{N_far >= 1} | U_r, grad f(X) = 0 ] dX,

the left side under the weighted law and the right side under `Q_r` with `W_r` inside and `Z_r^(-1)` outside, once
each. Cauchy–Schwarz on the conditional expectation (which is `E_(Q_X)` at the target), `1{N_far >= 1} <= N_far`, and
(5.3) bound the integrand by

    p_(grad f(X)|U_r)(0) E_(Q_X)[ (W_r F_j(H_X))^2 ]^(1/2) ( C k r^3 (1 + beta_X)^(2d) )^(1/2).

By [C6] (5.3) and the §6 regime table, the density times the square root of the squared-weight conditional moment is
bounded, in every regime, by the source's unmarked intensity bound times `(1 + beta_X)^(3d)`, and the regime's
Gaussian penalty absorbs the additional `(1 + beta_X)^d` as it absorbs [C6]'s marked factor: in every regime of
[C6] §6.2 the absorption of a power of `beta_X` is by an exponential factor in the degeneracy variable, and any fixed
polynomial degree is absorbed by raising the index of the exponential series there (the ledgers `2n >= 6 + 3d`,
`2n/3 >= 15 + 39d` are the recorded choices for [C6]'s degree; a larger `n` serves here at the cost of the constant). The
regional ledgers of [C6] §6, stated for the normalized quantity, then give `Z_r^(-1) integral_(|X| <= A r) (...) dX <= C(A) r^3`.
Multiplying by `(C k r^3)^(1/2)` gives (5.4). ∎

Remark. Only `o(r^3)` is needed; the exponent `9/2` is what Cauchy–Schwarz delivers and is not claimed sharp.

## 6. Proof of Theorem N and of the corollaries

### 6.1 The sandwich

Fix `A >= 4` and `rho <= s_0`. Write `N_rest = N_mid^(A,rho) + N_far^rho`. From the inclusions

    {N = 2} subset {N^A = 2} cup {N^A = 1, N_rest >= 1} cup {N_rest >= 2},
    {N^A = 2} subset {N = 2} cup {N^A >= 1, N_rest >= 1},

and the same with `2` replaced by `n >= 3` (upper inclusion only),

    | Q{N = 2} - Q{N^A = 2} | <= Q{N^A >= 1, N_mid >= 1} + Q{N^A >= 1, N_far >= 1} + Q{N_mid >= 1} + Q{N_far >= 2}
                              <= 2 C r^3 (A^(-2) + rho^2) + C(A, rho) r^(9/2) + C(rho) r^5,

by (5.1), (5.4) and (5.2); similarly `Q{N >= 3} <= Q{N^A >= 3} + (the same error)`. For `n = 1`,

    Q{N = 1} = Q{N^A = 1, N_rest = 0} + Q{N^A = 0, N_rest = 1},
    | Q{N^A = 1, N_rest = 0} - Q{N^A = 1} | <= Q{N^A >= 1, N_rest >= 1},
    | Q{N^A = 0, N_rest = 1} - Q{N_far^rho = 1} | <= Q{N^A >= 1, N_rest >= 1} + Q{N_mid >= 1},

and `Q{N_far^rho = 1} = k r^3 integral_(D_rho) Lambda + O(r^4) + O(r^5)` by (5.2). Divide by `r^3`, let `r -> 0` using
Proposition 4.4, then let `A -> oo` and `rho -> 0` using Proposition 4.4's `A -> oo` limit and §5.2:

    lim r^(-3) Q{N = 2} = nu_near(2),   lim r^(-3) Q{N = 1} = nu_near(1) + k integral_X Lambda,   lim r^(-3) Q{N >= 3} = 0,

with the error after `r -> 0` bounded by `C(A^(-2) + rho^2)`, which is what makes the two outer limits exist. The
limits exist as full limits (not along subsequences) because the sandwich bounds `liminf` and `limsup` between
quantities that differ by `C(A^(-2) + rho^2)`. Uniformity on the compact parameter set is inherited from Proposition
4.3, (5.1), (5.2) and (5.4), whose constants are uniform. This proves (1.5) modulo positivity and continuity.

### 6.2 Positivity and continuity

`nu(2) >= nu_near(2) > 0`: the [LM] cubic (L4), that is `(s, a_3, beta, c_3) = (-3k/2, 0, -2k, 0)`, has two extra
critical points `P_+-` at height `-7k/32` in the window and pin weight `w_0 = 3k^2 . 15k^2 = 45 k^4 > 0` (control `EX`,
matching [LM] (L5)); by Lemma 3.2 these properties persist on an open neighbourhood of that jet, on which `m > 0`, so
the integral (1.3) over that neighbourhood is positive. `nu_near(1) > 0`: the exact jet `(s, a_3, beta, c_3) =
(-1/2, 3, 1/3, 0)` at `k = 1` (rescaled by `k` in general) has extra critical points `(-3/2, 3)` at height `-1/2` (in the
window) and `(45/22, -357/11)` at height `-9947/121` (outside), with pin weights `7/4` and `17/4` (control `EX`); the
same open-neighbourhood argument applies. `nu(1) >= k integral_X Lambda > 0` by the positivity of `Lambda_j` in [RM].
Finiteness and continuity of (1.3), with an explicit majorant. On `{w_0 > 0}` the pin weight is
`w_0 = 9k^2 (4 s^2 - B^2) <= 36 k^2 s^2`, and by Lemma 3.6 the indicator `1{N_oo >= 1}` is supported on
`|B|/2 < -s <= 2|B| + (32 k D^2)^(1/3)`. Hence, for every `n >= 1`,

    m w_0 1{N_oo = n} <= 36 k^2 s^2 m 1{ |B|/2 < -s <= 2|B| + (32 k D^2)^(1/3) },

and integrating in `s` gives at most `12 k^2 m ( 2|B| + (32 k D^2)^(1/3) )^3 <= C_K m (1 + |a_3| + |beta| + |c_3|)^6` for
parameters in a compact set `K` (the constant depends on `K` through `k` only). Since `m <= C_K exp(-c_K (a_3^2 +
beta^2 + c_3^2))` uniformly on `K` (§3.7), this majorant is integrable uniformly on `K`. It proves the finiteness of
(1.3) a second time (independently of the Fatou argument of Proposition 4.4), and it does not depend on `A`, so it also
dominates the `A -> oo` step of Proposition 4.4. Continuity in `(b, k, R)`: `m`, `w_0`, `z_0`, `F_0` and `Lambda` depend
continuously on the parameters, the indicator `1{N_oo = n}` is continuous off the null set `E_k` (every counted point
is a nondegenerate saddle by Lemma 3.6, and the boundary heights are excluded off `E_k`), and the integrand of (1.3) is
dominated uniformly on `K` by the integrable majorant above; dominated convergence in the parameters gives continuity.

### 6.3 Corollary Lambda

`(N)_q = sum_n (n)_q 1{N = n}`. For `M >= q + 1`, `sum_(n > M) (n)_q Q{N = n} <= E[(N)_(q+1)]/(M - q) <= C_(q+1) r^3 /
(M - q)` by [C6] Theorem Q. Hence `r^(-3) E[(N)_q]` is within `C_(q+1)/(M - q)` of `sum_(n <= M) (n)_q r^(-3) Q{N = n}`,
which converges to `(1)_q nu(1) + (2)_q nu(2)` by (1.5); let `M -> oo`. This gives (1.6). The Palm statement is the
quotient of `Lambda_2` by `Lambda_1`.

### 6.4 Corollary S

[RCL] Theorem S extracts subsequential limits of `nu_r`; (1.5) identifies every subsequential limit with `nu`, so the
full family converges in the weighted `l1` sense of [RCL] (6.1) (the tail bound of [RCL] is uniform, so coordinatewise
convergence upgrades to weighted-`l1` convergence exactly as in its proof). The statements about `F_r`, `CP(p, F_r)`
and `CP(t nu)` are [RCL] Theorems C, S and (7.1) with the limit inserted. The three examples of [RCL] §6 have,
respectively, a non-convergent `nu_r`, a limit carried by `{2}` alone (`nu(1) = 0`), and a limit law with unbounded
support; each is excluded by (1.5) (existence of the limit, `nu(1) > 0`, `nu(n) = 0` for `n >= 3`).

### 6.5 Corollary X

Same proof as Proposition 4.4 with the functional `Phi^A = sum_(extra near critical points) phi(scaled data)` in place of
the indicator. Two adjustments. First, `Phi^A` is not bounded (`|Phi^A| <= sup|phi| N^A`), so before applying (4.2)
truncate at `N^A <= M`: by [C6] Theorem Q, `r^(-3) E[N^A 1{N^A > M}] <= r^(-3) E[(N)_2]/(M - 1) <= C_2/(M - 1)`
uniformly in `r`, which is the uniform integrability needed; on `{N^A <= M}` the functional is bounded, Lemma 4.1
gives the convergence of the scaled positions and heights, and Lemma 4.3 dominates with `M sup|phi|`. Let
`kappa -> oo`, then `M -> oo`, then `A -> oo` (the `A -> oo` step as in Proposition 4.4, dominated by `sup|phi| N_oo`).
Second, the transverse scaled distance: in the rotated chart of §3.2 the physical transverse displacement of a
critical point at scaled coordinates `(X, Z, W)` is `r (Z, rW)` with `|W|` bounded by Lemma 3.1, so `|X_perp|/r = |Z| + O(r)`.
Third, the index: by Lemma 3.6 every limit point in the sum is a nondegenerate saddle of `F_0`, of index `d - 1` in
the full model (Lemma 3.1, stable block negative definite on `{w_0 > 0}`), so the index marginal of the near law is
concentrated on `d - 1` and `nu_near(n)` is carried by index-`(d - 1)` points; the remote singleton part of `nu(1)`
carries the index-specific kernels `Lambda_j` of [RM], all `j`.

## 7. The reduced integral, and exact configurations

### 7.1 Structure of `nu_near`

The integrand of (1.3) depends on the full jet only through `(s, a_3, beta, c_3)`: the count `N_oo` and the pin weight
`w_0` are functions of the planar cubic (1.2) alone, and the stable directions enter only through `m`. Hence `nu_near(n)`
is a four-dimensional integral for every `d`:

    nu_near(n) = z_0^(-1) integral_(R^4) m(s, a_3, beta, c_3) w_0(s, a_3, beta) 1{ N_oo(s, a_3, beta, c_3) = n } ds da_3 dbeta dc_3.

The domain of integration is bounded in `s` from above by the index conditions (`s < beta/2 - a_3^2/(24k)` and
`s < a_3^2/(24k) - beta/2`) and, for the extra critical points to lie in the window, from below: for `|s| -> oo` with
`(a_3, beta, c_3)` fixed, the extra critical points of `F_0` are either the pins' neighbours excluded by Lemma 3.3 or
lie at scaled distance of order `|s|`, where the Euler identity for the cubic part gives `F_0 = s^3 zeta^2 / 6 + O(s^2)`
along the rescaled solutions `(X, Z) = s (xi, zeta)` of the limiting system `6k xi^2 + a_3 xi zeta + (beta/2) zeta^2 = 0`,
`zeta (1 + beta xi + c_3 zeta / 2) + (a_3/2) xi^2 = 0` (control `EU`); `zeta = 0` forces `xi = 0`, so on nontrivial
solutions `|zeta|` is bounded below and the height leaves the window `(-k, 0)` for large `|s|`. This is the reason the
near count carries no logarithm although the shells' all-height count would (compare [DL] §8: the height window is
load-bearing for the shells), and it is the analytic content of Lemma 3.3 and Lemma 4.3.

### 7.2 Exact configurations (finite control `EX`)

With `k = 1` and jets `(s, a_3, beta, c_3)`:

| Jets | Extra critical points `(X, Z)` | Heights | In window | Pin weights `(w_M, w_S)` | `N_oo` |
|---|---|---|---|---|---|
| `(-3/2, 0, -2, 0)` ([LM] (L4)) | `(-3/4, +-sqrt(15/8))` | `-7/32, -7/32` | yes, yes | `(3, 15)` | 2 |
| `(-55/48, 5/2, -5/3, -5/2)` | `(-2, 3)`, `(-783/1616, -129/1616)` | `-27/32`, `-4735/83566592` | yes, yes | `(5/16, 215/16)` | 2 |
| `(-1/2, 3, 1/3, 0)` | `(-3/2, 3)`, `(45/22, -357/11)` | `-1/2`, `-9947/121` | yes, no | `(7/4, 17/4)` | 1 |
| `(-33/10, 3, -12/5, -3)` | `(-2, 5/2)`, `(-282/541, -1495/1082)` | `-41/16`, `-3199921/4682896` | no, yes | `(207/20, 117/4)` | 1 |
| `(-396, -3, -204, -3)` | `(-2, 1/2)`, `(-263314/140087, -115623/280174)` | `-119/8`, `< -k` | no, no | `(7047/4, 11961/4)` | 0 |
| `(1000, 2, 1, -1)` | none real (`Q_2` has negative discriminant) | — | — | `w_0 = 0` (index conditions fail) | 0 |

All entries are exact rationals or exact quadratic irrationals verified by the control. The scaling `k -> 1` is the
substitution `(s, a_3, beta, c_3, X, Z) -> (k s, k a_3, k beta, k c_3, X, Z)`, under which `F_0` scales by `k`.

## 8. Remarks on the mechanism

- The cubic (1.2) is the two-parameter family that the four pins leave free at order three on the soft plane; its
  extra critical points appear and disappear in pairs through fold points (the discriminant of `Q_2`), which is why
  `N_oo` takes the values `0, 1, 2` and why `nu(1)` has a near contribution at all: a pair with one member above the
  upper window edge or below the lower one. No statement about elder selection is made. By Lemma 3.6 every extra
  critical point with height in the window is a nondegenerate saddle of the planar cubic, of index `d - 1` in the full
  model; maxima or degenerate critical points of `F_0` occur only outside the window (control `TW`). This does not
  affect the count coefficients, but it is the correct input for any positional or index-law consumer (Corollary X).
- The `r^3` is `r` (the soft transverse curvature must be `O(r)`, one Lebesgue direction) times `r^4/r^2` (the pin
  weight on a soft configuration relative to the normalizer). Nothing is small in the third-order jets.
- The far contribution to `nu(1)` is the integral of the reviewed contact kernel; its integrability near the pins is a
  consequence of the shell bound, not a new estimate.
- The near–far cross term is bounded by Cauchy–Schwarz inside the marked Kac–Rice integrand (Lemma 5.2); it is the
  only place where a witness-conditioned bound on the remote count is needed, and only its order `o(r^3)` is used.

## 9. What this note does not establish

No rate of convergence in (1.5)–(1.6); no numerical value or enclosure of `nu(1)`, `nu(2)`, `z_0`, `m` or
`integral Lambda`; no uniformity in `k`, `L` or `d`; no elder-selection statement about the extra points; no joint
law of the clusters of distinct pin pairs; no all-height near count (the window is load-bearing, §7.1); no register or
catalog change. The catalog entry C6 and the GRAPH node `math.rn-region.witness-collision` are not moved by this packet.

## 10. Finite controls

`cluster_law_check.py` (standard library, exact rationals and exact polynomial arithmetic over `Q`) verifies:

- `NF`: the pin conditions of `F_0` (values `0` and `-k`, vanishing gradients at `(-+1/2, 0)`) as polynomial identities in
  `(s, a_3, beta, c_3, k)`; the pin Hessian blocks `M_2(M), M_2(S)` of Lemma 3.4.
- `RS`: the resultant of `partial_X F_0, partial_Z F_0` in `Z` equals `(X^2 - 1/4) Q_2(X)` with the coefficients (3.7),
  as an identity in `Q[X, s, a_3, beta, c_3, k]`.
- `EX`: the six configurations of §7.2: exact critical points, heights, window membership, pin weights, `N_oo`; the
  [LM] weight `45 k^4`; the [LM] double root of `Q_2`.
- `BD`: the block-determinant expansion (3.9) for `d = 3` and `d = 4` as an exact identity in `r` (the `r^2`
  coefficient is `det D . det M_2`, the remainder is divisible by `r^3`).
- `EU`: the Euler identity `xi G_xi + zeta G_zeta = 3 G_3 + zeta^2` for the limiting cubic-plus-quadratic `G`, hence
  `G = zeta^2/6` at its critical points, and `zeta = 0 => xi = 0`.
- `SH`: the shear identity (3.12), `F_0(X, Z) = C(u) + (s + Bu) Z^2/2 + (D/3) Z^3` with `u = X + a_3 Z/(12k)`, as the
  polynomial identity in `Q[u, Z, s, a_3, beta, c_3, k]` obtained by clearing `k` (`(12k)^3 F_0` with `12k X = 12k u - a_3 Z`).
- `TW`: on an exact rational family of critical points of `G` (parametrized by `(u, Z, D, k)`, `B` and `s` solved
  exactly), the Hessian-determinant identity `det = -3k(B + 4su)` at every critical point, the height identity
  `G = C(u) + w^3/(6D^2)`, and, on every typed in-window sample, `det < 0` and `(-s - 2|B|)_+^3 <= 32 k D^2` (Lemma 3.6);
  the number of typed in-window samples is recorded.
- `LG`: the exponent ledgers: `1 + 4 - 2 = 3`; the cross term `3 + 3/2 > 3`; the shell error `A^(-2) + rho^2`; the
  Hadamard exponent of (3.10) (`4 + 2 + (2d - 6) = 2d` soft-and-stable row factors for `d = 3, 4`); the large-`K_4`
  tail `kappa^(-p/2) -> 0`; the uniform-integrability step of §6.3 and §6.5 (`1/(M - 1) -> 0`).

Nine mutants (`pins-not-critical`, `wrong-pin-hessian`, `drop-sigma-jacobian`, `three-extra-points`,
`cross-term-not-small`, `window-closed`, `index-sign`, `shear-drop-cubic`, `s-bound-constant`) each exit `1`. The controls verify identities, exact
configurations and exponent bookkeeping only. They do not verify the Gaussian regression, the dominated convergence,
the stability argument or the Kac–Rice steps; those are the written arguments and the cited sources.

## 11. Attribution and reconnaissance

The mechanism of §§3–4 is the rare-set construction of [EDL] §§3–9 and [LM] §§2–6, used here as a limit theorem
rather than as a lower bound. The dominated-convergence device is that of [LP] §13 and [RM] §5. The local normal form
is a cusp-type unfolding of a planar cubic; no novelty is claimed for that algebra, which is classical (V. I. Arnold,
*Catastrophe Theory*, 3rd ed., Springer 1992, for the fold and cusp normal forms; the specific pinned cubic is the
one written in [LM] (L6) and [EDL] (A17)). `RECONNAISSANCE.md` records that the external literature check remained
blocked by the Consensus monthly quota and that no citation was invented.
