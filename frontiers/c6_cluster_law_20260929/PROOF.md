# The cluster law of the C6 window count: `r^(-3) Q_r^W{N = n} -> nu(n)`, with `nu` carried by `{1, 2}`

**Object:** CL-C6-CLUSTER-LAW-20260929-v1.
**Version:** v1.0, 29 September 2026.
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
from the `Q_0`-density of the midpoint jets on the singular slice by integrating out the stable directions, (3.8)),
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

**Corollary X (scaled positional law).** For every bounded continuous `phi` on `R^2 x R`, uniformly on the compact
parameter set,

    r^(-3) E_(Q_r^W) sum_(X in near window critical points) phi( (X . u)/r, |X_perp|/r, (f(X) - b)/r^3 )
       -> z_0^(-1) integral m w_0 sum_(critical points (X,Z) of F_0 in the window) phi( X, |Z| (1 + |q|^2)^(1/2), F_0(X,Z) ),

where the inner sum runs over the extra critical points of `F_0` and `q` is the shear parameter of the chart of §3.2
(so that `|Z|(1+|q|^2)^(1/2)` is the scaled transverse distance); the right side is the weighted law of the scaled
configuration. In `d = 2`, `q` is absent and the scaled transverse coordinate is `|Z|`.

### 1.3 What the results are not

Existential constants, fixed `d` and `L`, compact marks. No rate in (1.5)–(1.6); no numerical value of `nu(1)`, `nu(2)`
or `Lambda_q`; no uniformity as `k -> 0`; no statement about the elder selection of the extra points; no spatial
independence between distinct pin pairs; nothing about the remote pair kernel beyond consistency with [RC]. §9 lists
the non-claims. The note is conditional on the consumed sources at the exact bytes of §2.

### 1.4 The planar case

For `d = 2` there are no stable directions: `m = 1`, the chart of §3.2 is the identity, `m(s, a_3, beta, c_3)` is the
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
| [EDL] | `frontiers/elder_dimension_lift_20260928/PROOF.md` | §2 (complete third-order jets and their positive-definite joint covariance with `U_0`), §3 (the unit-Jacobian shear chart (A8)–(A10)), (A11)–(A16) (the rare set and the conditional `C^4` control), (A17) (the normal form on the sheared soft plane), (A26)–(A28) (the rescaled full gradient and the stable block), §9 (block-triangular stability of the extra critical points). Used as the source of the chart and of the normal form; the lower bound (A4) is not consumed. |
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

### 3.2 The shear chart and the singular slice

Decompose `A = [[a, v^T], [v, D]]` with `a in R`, `v in R^n`, `D in Sym_n`, and on `{det D != 0}` set

    sigma = a - v^T D^(-1) v,      q = D^(-1) v,      y = S(z, w) = (z, w - q z),      S = [[1, 0], [-q, I_n]],       (3.2)

exactly [EDL] (A8)–(A9), so that `S^T A S = diag(sigma, D)`; the map `(a, v, D) -> (sigma, v, D)` has Jacobian one ([EDL] (A10)), and with
the linear change `L = diag(1, S)` of the transverse coordinates, `f~(x, z, w) = f(R L (x, z, w))` has
`f~_zz(0) = sigma`, `f~_zw(0) = 0`, `f~_ww(0) = D`. Let `tau` be the third derivatives of `f~` at `0` other than
`f~_xxx`; for fixed `(v, D)` the map `T -> tau` is triangular with unit diagonal, so `(a, v, D, T) -> (sigma, v, D, tau)`
has Jacobian one on `{det D != 0}`. `L` has determinant one, is not orthogonal, and its norm is at most `C(1 + |q|)`.

Write `j = (sigma, v, D, tau)` in these coordinates and `chart(sigma, v, D, tau)` for the corresponding raw jet. The
singular slice is `{sigma = 0}`. For `d = 2` there is no `w`: `sigma = a = f_zz(0)`, `q` and `D` are absent and the
chart is the identity.

*Why one chart suffices.* Under `Q_r^W` the endpoint Hessians have indices `d` and `d - 1` and, by [LP] (5.1)–(5.2),
their transverse blocks are `A + O(r K_4)`; the weight vanishes unless `A_M` is negative definite, so on the support of
the weight `A` is negative semidefinite up to `O(r)` and its eigenvalues other than the soft one are negative and of
order one on the rare set of §3.5. Restricting `A` to `e_z^perp` gives `D`, which is then negative definite unless the
soft eigenvector is orthogonal to `e_z`, a set of `A` of Lebesgue measure zero. The chart therefore covers the whole
rare set up to a null set of jets, for every `d`. Configurations with two soft transverse eigenvalues have `D` nearly
singular and are covered by Lemma 4.3, which bounds their contribution by `C eta` uniformly in `r`.

### 3.3 The normal form

Let `F_r(X, Z, W) = [ f~(rX, rZ, r^2 W) - b ] / r^3` and

    s = sigma / r,   a_3 = tau_xxz,   beta = tau_xzz,   c_3 = tau_zzz,   Q_j(X, Z) = (tau_xxw_j / 2)(X^2 - 1/4) + tau_xzw_j X Z + (tau_zzw_j / 2) Z^2.

**Lemma 3.1 (normal form, [EDL] (A17), (A26)–(A28); [LM] (L6)–(L7)).** For every `R_0 >= 1` there is `C = C(d, R_0)`
such that on `{|(X, Z)| <= R_0, |W| <= R_0}`, uniformly in `b, k, R`, `0 < r <= 1`,

    || F_r(., ., 0) - F_0 ||_(C^2) <= C r K_4 (1 + |q|)^3,                                                          (3.3)
    r^(-2) grad f~(rX, rZ, r^2 W) = ( partial_X F_0, partial_Z F_0, D W + Q(X, Z) ) + O( r K_4 (1 + |q|)^3 (1 + |D|) ),  (3.4)

with `F_0` as in (1.2) (the pins are exactly retained: `F_0(-+1/2, 0) = 0, -k` and `grad F_0(-+1/2, 0) = 0`, checked
exactly in the finite control `NF`). Moreover, for `|(X, Z)| <= R_0` and physical `|w| <= R_0 r`, the `w`-gradient
satisfies `|partial_w f~| >= (sigma_min(D) - C r K_4 R_0)|w| - r^2 |Q| - C r^3 K_4`, so every critical point of `f~` in
the physical ball of radius `R_0 r` has `|W| <= C |Q(X,Z)| / sigma_min(D) + 1` once `r <= r_0(K_4, R_0, D)`.

*Proof.* The Taylor expansion of `f~` at the midpoint through order three, with the pin identities of [LM] §3
(`f~_xxx(0) = 12k + O(r K_4)`, `f~_x(0) = -(r^2/8) f~_xxx(0) + O(r^3 K_4)`, `f~_z(0) = -(r^2/8) f~_xxz(0) + O(r^3 K_4)`,
`f~_xx(0), f~_xz(0) = O(r^2 K_4)`, `f~(0) - b = -(r^3/24) f~_xxx(0) + O(r^4 K_4)`, and `f~_w(0) = -(r^2/8) f~_xxw(0)
+ O(r^3 K_4)`, `f~_xw(0) = O(r^2 K_4)`, `f~_zw(0) = 0` exactly), is (A17) of [EDL] on `w = 0` and gives (3.3); the
factor `(1 + |q|)^3` bounds the derivatives of `f~` through order four in terms of those of `f` under the shear.
Differentiating in `w` and using `D_w^2 f~(0) = D`, `D_(zw) f~(0) = 0` gives (3.4), the last block being `r^2 (D W +
Q) + O(r^3)` before division. The lower bound on `|partial_w f~|` is (3.4) read at physical `w = r^2 W` with
`|W| <= R_0 / r`: the quadratic remainder `K_4 |w|^2 <= K_4 R_0 r |w|` is relative to the linear term `D w`. ∎

Consequently, for `r <= r_0(K_4, R_0, D)` the critical points of `f~` in the physical ball of radius `R_0 r` are in
bijection with the zeros of the reduced planar gradient

    grad G_r(X, Z),   G_r(X, Z) = F_r(X, Z, W_*(X, Z)),   W_*(X, Z) = the unique solution of the third block of (3.4) = 0,

`W_* = -D^(-1) Q(X, Z) + O(r K_4 (1 + |q|)^3 (1 + |D^(-1)|)^2)`, and

    || G_r - F_0 ||_(C^2({|(X,Z)| <= R_0})) <= C r K_4 (1 + |q|)^3 (1 + |D^(-1)|)^2 (1 + |tau|)^2.                  (3.5)

Indeed `F_r(X, Z, W) - F_r(X, Z, 0) = r^(-3)[ r^2 partial_w f~ . W r^2 ... ] = r (Q . W + W^T D W / 2) + O(r^2)`, which
is `O(r)` in `C^2` on bounded `W`; the implicit function `W_*` is `C^2` with the stated bound because the third block
of (3.4) has derivative `D + O(r)` in `W`. The index of a critical point of `f~` equals the index of the corresponding
critical point of `G_r` plus the index of `D` ([EDL] §9: the full Hessian is block triangular up to `O(r)` with diagonal
blocks the planar Hessian of `G_r` and `D`), and its height satisfies `(f~ - b)/r^3 = G_r` at the point.

### 3.4 The planar cubic

**Lemma 3.2 (at most two extra critical points).** For every `(k, s, a_3, beta, c_3)` with `k > 0`, the critical points
of `F_0` in `C^2` other than the two pins are the common zeros of the two quadratics `partial_X F_0, partial_Z F_0`
whose `X`-coordinates are the roots of

    Q_2(X) = c_2 X^2 + s c_1 X + c_0,
      c_2 = a_3^3 c_3/4 - 3 a_3^2 beta^2/16 - (9/2) a_3 beta c_3 k + 3 beta^3 k + 9 c_3^2 k^2,
      c_1 = -a_3^2 beta/4 - 3 a_3 c_3 k + 6 beta^2 k,
      c_0 = 3 s^2 beta k - ( a_3 beta/8 - 3 c_3 k/2 )^2,                                                        (3.6)

in the sense that the resultant of `partial_X F_0` and `partial_Z F_0` with respect to `Z` equals `(X^2 - 1/4) Q_2(X)`
identically in `(X, s, a_3, beta, c_3, k)` (finite control `RS`, exact polynomial identity). Hence, whenever the two
quadratics have no common factor, `F_0` has at most four critical points counted with multiplicity, two of which are
the pins, and the extra real critical points are at most two; when they have a common factor the set of critical points
is a curve, which happens only on a proper algebraic subset of the jet space. Away from a proper algebraic subset of
`(s, a_3, beta, c_3)` (for fixed `k`), the extra critical points are nondegenerate, their heights are not in `{-k, 0}`,
and `N_oo in {0, 1, 2}`.

*Proof.* The resultant identity is an exact computation (the Sylvester determinant of two quadratics in `Z`), verified
symbolically in `RS`. The pins are the zeros of `partial_X F_0 = 6k X^2 - 3k/2 + a_3 X Z + (beta/2) Z^2` and
`partial_Z F_0 = s Z + (a_3/2)(X^2 - 1/4) + beta X Z + (c_3/2) Z^2` on `Z = 0`, which explains the factor `X^2 - 1/4`.
If the two quadratics in `Z` are coprime for the given `X`, they share at most one root; so each root `X_*` of `Q_2`
carries at most one extra critical point unless `partial_Z F_0(X_*, .) = 0` identically, which requires
`s + beta X_* = 0`, `c_3 = 0` and `a_3 (X_*^2 - 1/4) = 0`; in that case the extra points are the (at most two) zeros of
`partial_X F_0(X_*, .)` (as in the [LM] configuration, where control `EX` exhibits `X_* = -3/4` as a double root of `Q_2`). Bézout's
theorem bounds the number of isolated common zeros of two conics by four. The nondegeneracy statements define
proper algebraic subsets because the configurations of §7 (exact rational examples with `0`, `1` and `2` extra
critical points in the window, all nondegenerate) lie outside them. ∎

**Lemma 3.3 (large soft curvature excludes near critical points).** There is `C = C(d)` such that, if `|(X, Z)| <=
R_0`, `r <= r_0(K_4, R_0, D)`, `(X, Z, W)` is a critical point of `f~` in the scaled coordinates, and `(X, Z)` is at
scaled distance at least `rho_pin = c k / (K_4 (1 + |tau|))` from both pins, then

    |s| <= C (1 + |tau|)^3 (1 + R_0)^2 K_4 (1 + |q|)^3 (1 + |D^(-1)|)^2 / k^2 =: S_*(tau, q, D, K_4, R_0).           (3.7)

Equivalently: for `|s| > S_*` the only critical points of `f~` in the physical ball of radius `R_0 r` are the pins.

*Proof.* At a zero of `grad G_r`, (3.5) gives `|partial_Z F_0(X, Z)| <= eps := C r K_4 (...)`. From the formula for
`partial_Z F_0`, `|s| |Z| <= (|a_3|/2)(R_0^2 + 1) + |beta| R_0 |Z| + (|c_3|/2) |Z|^2 + eps`, so for
`|s| >= 2 |beta| R_0 + |c_3| R_0 + 1` one has `|Z| <= C (1 + |tau|)(1 + R_0)^2 / |s|`. Inserting this in
`|partial_X F_0| <= eps` gives `|6k X^2 - 3k/2| <= C (1 + |tau|)^2 (1 + R_0)^2 / |s| + eps`, hence `X` lies within
`C (1 + |tau|)^2 (1 + R_0)^2 / (k |s|)` of `+-1/2`. So the zero is within scaled distance `C (1 + |tau|)^3 (1 + R_0)^2
/ (k |s|)` of a pin. At a pin the scaled Hessian of `G_r` is `M_2 + O(r)` with `M_2` given in Lemma 3.5 below; for
`|s| >= C(1 + |tau|)^2/k` its least singular value is at least `c k`, and `|grad G_r(xi)| >= c k |xi - pin| - C K_4
(1 + |q|)^3 |xi - pin|^2` for `|xi - pin| <= 1`, so no other zero lies within scaled distance `rho_pin` of a pin. The
two conclusions are incompatible when `|s|` exceeds the right side of (3.7). ∎

### 3.5 The weight on the singular slice

**Lemma 3.4 (pin Hessians).** With `M_2(M) = [[-6k, -a_3/2], [-a_3/2, s - beta/2]]` and `M_2(S) = [[6k, a_3/2],
[a_3/2, s + beta/2]]` (exact second derivatives of `F_0` at the pins, control `NF`), the Hessians of `f~` at the pins are

    H~_i = [[ r M_2(i) + O(r^2 K_4), r c_i + O(r^2 K_4) ], [ r c_i^T + O(r^2 K_4), D + O(r K_4) ]],   i in {M, S},

with `c_i in R^(2 x n)` linear in `tau` (the entries `-+tau_xxw/2, -+tau_xzw/2`), and

    det H~_i = r^2 det D . det M_2(i) + O( r^3 K_4^d (1 + |tau|)^2 (1 + |s|)^2 ),                                 (3.8)

exactly as polynomials: the determinant of a matrix whose two soft rows are `O(r)` and whose stable block is `O(1)` is
`r^2` times the product of the soft-block and stable-block determinants plus `r^3` times a polynomial in the entries
(control `BD` checks this for `d = 3` and `d = 4` with exact rational arithmetic in `r`). The congruence `L` has
determinant one, so `det H_i = det H~_i` and the index is unchanged.

*Proof.* The entries follow from Lemma 3.1 by differentiating (3.3)–(3.4) once more at the pins:
`partial_X^2 F_0 = 12k X + a_3 Z`, `partial_X partial_Z F_0 = a_3 X + beta Z`, `partial_Z^2 F_0 = s + beta X + c_3 Z`,
evaluated at `(-+1/2, 0)`, and the mixed soft–stable entries are the derivatives of `Q`. The determinant expansion is
the Leibniz formula: every term contains at least two factors from the two soft rows, each `O(r)`; the terms with
exactly two such factors and the identity permutation on the stable block give `r^2 det M_2 det D`; the remaining terms
carry `r^3`. ∎

**Lemma 3.5 (weight limit).** On the singular slice write `w_0` as in (1.1). If `D` is negative definite and
`det M_2(M) != 0 != det M_2(S)`, then under the conditional law of §3.1 with `sigma = r s`,

    r^(-4) W_r -> (det D)^2 w_0(s, a_3, beta)     in probability as r -> 0,

and `r^(-4) W_r <= C K_4^(2d) (1 + |s| + |tau|)^(2d)` pathwise. Here `w_0 > 0` exactly when `M_2(M)` is negative
definite (index `d` at `M`, given `D < 0`) and `M_2(S)` has one negative eigenvalue (index `d - 1` at `S`).

*Proof.* (3.8) gives `r^(-2) det H~_M -> det D . det M_2(M)`, and the index of `H~_M` converges to `index(M_2(M)) +
index(D)` because eigenvalues are continuous and the limits are nonsingular. `F_d(H_M) = |det H_M| 1{index = d}` gives
the first factor; the second factor is the same at `S`. The condition `index M_2(M) = 2` is `det M_2(M) > 0` (its
`(1,1)` entry is `-6k < 0`), and `index M_2(S) = 1` is `det M_2(S) < 0` (its `(1,1)` entry is `6k > 0`); these are the
two positive parts in (1.1). The pathwise bound is Hadamard's inequality on the rows of `H~_i` with the entry bounds
of Lemma 3.4. ∎

### 3.6 The reduced weight

Let `p_0` be the `Q_0`-density of the raw jet `J = (A, T)` (§3.1). Define, on `{D < 0}`,

    m(s, a_3, beta, c_3) := integral p_0( chart(0, v, D, tau) ) (det D)^2 1{D < 0} dv dD dtau_rest,             (3.9)

where `tau_rest` collects the entries of `tau` other than `(a_3, beta, c_3)` (those involving a `w` index), and the
unit-Jacobian chart is used with `sigma = 0`. The integrand does not depend on `s`; `m` is a bounded, strictly positive,
continuous function of `(a_3, beta, c_3)` with Gaussian decay (the density `p_0` is Gaussian and nondegenerate, the
integral over `v, D` converges by (3.5)-type decay of [LP] since `|chart(0, v, D, tau)| >= c(|v| + |D|)`), and it
depends continuously on `(b, k, R)`. In `d = 2`, `m(s, a_3, beta, c_3) = p_0(0, a_3, beta, c_3)`, the density of
`(f_zz, f_xxz, f_xzz, f_zzz)(0)` at `f_zz = 0`.

## 4. The near limit

### 4.1 Scaled representation

Fix `A >= 4` and write `N^A = N_near^A`. For every Borel set `E` of field configurations,

    Q_r^W(E) = Z_r^(-1) integral p_r(j) E[ W_r 1_E | U_r = v_r, J = j ] dj,                                        (4.1)

by the tower property with the regular conditional law of §3.1. Change variables to `(sigma, v, D, tau)` (Jacobian one
on `{det D != 0}`, whose complement is `p_r`-null) and then `sigma = r s`:

    r^(-3) Q_r^W(E) = (r^2 / Z_r) integral ds dv dD dtau  p_r( chart(rs, v, D, tau) )  r^(-4) E[ W_r 1_E | U_r = v_r, J = chart(rs, v, D, tau) ].   (4.2)

The factor `r` from `dsigma = r ds` and the factor `r^(-4)` from the weight combine with `r^2/Z_r -> 1/z_0` ([LP] (5.4))
to the exponent `1 + 4 - 2 = 3` of [LM] §6.

### 4.2 Convergence of the scaled count

**Lemma 4.1.** Fix `A >= 4`, and fix `(s, v, D, tau)` with `D < 0` outside the null set `Z_A` of jets for which some
extra critical point of `F_0` is degenerate, has height in `{-k, 0}`, or lies on the ellipse `X^2 + (1 + |q|^2) Z^2 = A^2`
(each condition is a nontrivial algebraic relation between the jets and the critical points, which are algebraic
functions of the jets, so `Z_A` is a proper algebraic subset, hence Lebesgue-null; Lemma 3.2 and the examples of §7
show the relations are nontrivial), and let `j_r = chart(rs, v, D, tau)`, `j_0 = chart(0, v, D, tau)`. Then, under the
conditional laws `Q_(r, j_r)` of §3.1,

    1{ N^A = n }  ->  1{ N_oo^A = n }     in probability,    N_oo^A := #{ extra critical points (X, Z) of F_0 with X^2 + (1 + |q|^2) Z^2 < A^2 and F_0(X, Z) in (-k, 0) },

and likewise for the counts restricted to any fixed index, and for the joint law of the scaled positions and heights
(Corollary X).

*Proof.* Couple the conditional laws as in §3.1: `f = m_r(j_r) + Res_r` with `Res_r -> Res_0` in `C^4` in probability
and `m_r(j_r) -> m_0(j_0)` in `C^4`. Fix a realization with `K_4 < oo` along which the convergence holds. The physical
ball `|X| <= A r` in the original coordinates is, in the scaled sheared coordinates, `{X^2 + |S(Z, r W)|^2 <= A^2}` with
`|S(Z, rW)|^2 = Z^2 + |rW - qZ|^2 = (1 + |q|^2) Z^2 + O(r)` on bounded `W`; by Lemma 3.1 every critical point in it has
bounded `W`, so its `(X, Z)` lies in the ellipse `E_A = {X^2 + (1+|q|^2) Z^2 <= A^2}` up to `O(r)`. By (3.5),
`G_r -> F_0` in `C^2(E_(A+1))`. The extra critical points of `F_0` in `E_(A+1)` are finitely many and nondegenerate
(Lemma 3.2), none lies on `partial E_A` and none has height in `{-k, 0}` (the jet is outside `Z_A`). Ordinary `C^1` stability (the inverse function theorem
on disjoint balls around the nondegenerate zeros, plus `|grad F_0| >= delta > 0` on the complement of those balls in
`E_(A+1)`, which `C^1`-closeness preserves for small `r`) gives: for `r` small, `grad G_r` has exactly one zero in each
small ball and none elsewhere in `E_(A+1)`; each converges to the corresponding zero of `grad F_0`, its `G_r`-height
converges to the `F_0`-height (so its window membership stabilizes), its planar Hessian converges (so its index
stabilizes), and, by the bijection of §3.3, these are exactly the critical points of `f~` in the physical ball, other
than the pins, which are the two fixed nondegenerate zeros `(-+1/2, 0)` of `grad F_0` and attract no other zero.
Hence `N^A -> N_oo^A` for every such realization; convergence in probability follows. The same argument gives the
convergence of scaled positions and heights. ∎

### 4.3 Domination

**Lemma 4.2 (domination on `{|det D| >= eta}`).** Fix `eta > 0` and `A >= 4`. There is an integrable function
`g_(A, eta)(s, v, D, tau)` on `R x R^n x Sym_n x R^(dim tau)` such that for all `0 < r <= r_*` and all `(s, v, D, tau)`
with `D < 0` and `|det D| >= eta`,

    p_r( chart(rs, v, D, tau) ) r^(-4) E[ W_r 1{ N^A >= 1 } | U_r = v_r, J = chart(rs, v, D, tau) ] <= g_(A, eta)(s, v, D, tau),

and, without the indicator, `p_r(chart(rs, ...)) r^(-4) E[W_r | ...] <= g(s, v, D, tau)` with `integral_(|s| <= S) g < oo`
for every `S`.

*Proof.* Write `j = chart(rs, v, D, tau)`. On `{|det D| >= eta}`, Cramer's rule gives `|D^(-1)| <= C (1 + |D|)^(n-1) / eta`
and `|q| <= C |v| (1 + |D|)^(n-1) / eta`, so the constant `S_*` of (3.7) is `K_4 kappa_0(tau, v, D, A, eta)` with `kappa_0`
polynomial in `(1 + |tau| + |v| + |D|)` and in `A`, with coefficients depending on `eta`. By Lemma 3.3,
`1{N^A >= 1} <= 1{ K_4 >= |s| / kappa_0 }`. Cauchy–Schwarz and the pathwise bound of Lemma 3.5 give

    r^(-4) E[ W_r 1{N^A >= 1} | j ] <= C (1 + |s| + |tau|)^(2d) E[ K_4^(4d) | j ]^(1/2) P( K_4 >= |s|/kappa_0 | j )^(1/2)
                                    <= C (1 + |s| + |tau|)^(2d) (1 + |j|)^(2d) min{ 1, (1 + |j|)^(p/2) kappa_0^(p/2) |s|^(-p/2) },

by (3.1) and Markov, with a fixed `p` such that `p/2 > 4d + 2`. Since `p_r(j) <= C exp(-c |j|^2)` and
`|j| >= c (|v| + |D| + |tau|)` (the chart is a bounded perturbation of the identity on `{|det D| >= eta}`), the right
side times `p_r(j)` is at most

    g_(A, eta) := C_(A, eta) exp(-c (|v|^2 + |D|^2 + |tau|^2)) (1 + |s| + |v| + |D| + |tau|)^(N) min{ 1, (1 + |v| + |D| + |tau|)^(N) |s|^(-p/2) }

for a fixed `N`, which is integrable: in `s` by the tail `|s|^(-p/2)`, in `(v, D, tau)` by the Gaussian factor. The
second statement is the same bound without the minimum, integrated over bounded `s`. ∎

**Lemma 4.3 (nearly singular stable block).** For every `A >= 4` and `eta > 0`,

    limsup_(r -> 0) r^(-3) Q_r^W{ N^A >= 1, |det D| < eta } <= C(A) eta.                                            (4.3)

*Proof.* In `d = 2` there is no `D` and nothing to prove. Otherwise use (4.2) with the crude bound
`E[W_r 1{N^A >= 1} | j] <= E[W_r 1{N^A >= 1} | j]` retained only through Lemma 3.3 and the weight expansion. By (3.8), on
the singular slice

    r^(-4) W_r <= (det D)^2 |det M_2(M) det M_2(S)| + C r K_4^(2d) (1 + |s| + |tau|)^(2d),

where the remainder does not involve `D^(-1)` (it is the Leibniz expansion of Lemma 3.4). By Lemma 3.3 with Cramer's
rule in the form `|D^(-1)| <= C (1 + |D|)^(n-1) / |det D|`, `N^A >= 1` forces `|s| <= K_4 (1 + |tau| + |v| + |D|)^(N)
A^2 / |det D|^2`. Hence, for `|det D| < eta`,

    integral ds  r^(-4) E[ W_r 1{N^A >= 1} | j ] <= C E[ K_4 (...)^N | j ] A^2 . [ (det D)^2 (1 + |tau|)^4 / |det D|^2 + r (...) / |det D|^2 ]
                                                <= C(A) (1 + |j|)^(N') [ 1 + r / eta^2 ],

using (3.1). The set `{D < 0 : |det D| < eta}` has Lebesgue measure at most `C eta` inside any ball of `Sym_n`, and the
Gaussian density of `J` integrates the polynomial `(1 + |j|)^(N')` over `(v, tau)` and over `D` outside a ball to an
arbitrarily small remainder. Multiplying by `r^2 / Z_r <= C` and letting `r -> 0` gives (4.3). ∎

### 4.4 The near limit for fixed `A`

**Proposition 4.4.** For every `A >= 4` and `n in {0, 1, 2}`, uniformly on the compact parameter set,

    r^(-3) Q_r^W{ N^A = n } -> nu_near^A(n) := z_0^(-1) integral m w_0 1{ N_oo^A = n } ds da_3 dbeta dc_3,          (4.4)

and `r^(-3) Q_r^W{ N^A >= 3 } -> 0`. The integrals are finite, and `nu_near^A(n) -> nu_near(n)` as `A -> oo` (monotone
convergence of the indicators: `N_oo^A = N_oo` for `A` larger than the scaled radius of the finitely many extra
critical points, which is finite for every jet outside the null set).

*Proof.* Apply (4.2) with `E = {N^A = n}` for `n >= 1` (for `n = 0` use the complement). The integrand converges
pointwise for a.e. `(s, v, D, tau)` to `p_0(chart(0, v, D, tau)) (det D)^2 w_0(s, a_3, beta) 1{N_oo^A = n}` by Lemma
4.1, Lemma 3.5 (convergence in probability of `r^(-4) W_r` together with the uniform `L^2` bound of (3.1) gives
convergence of the conditional expectation of the product with a bounded functional) and the continuity of the density.
Split the integral into `{|det D| >= eta}` and `{|det D| < eta}`: on the first set Lemma 4.2 dominates and dominated
convergence applies; the second contributes at most `C(A) eta` in the limit by Lemma 4.3, and `eta` is arbitrary. The
prefactor `r^2/Z_r -> z_0^(-1)`. Integrating out `(v, D, tau_rest)` gives (4.4) with the
reduced weight (3.9). For `n >= 3` the pointwise limit of the indicator is zero by Lemma 3.2. Uniformity on the compact
parameter set: the dominating function and all limits depend continuously on `(b, k, R)`, so a sequence of parameters
along which the convergence fails would have a convergent subsequence contradicting the pointwise statement at the
limit parameter, exactly as in [LP] §5. ∎

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
observation `grad f(X) = 0` (the gradient-only kernel of [C6] Lemma 5.1, defined for every `X`). Then for `rho <= s_0`,

    E_(Q_X)[ N_far^rho ] <= C(rho) k r^3 (1 + beta_X)^d,                                                              (5.3)

where `beta_X` is the frame parameter of [C6] Lemma 4.1 for the regime containing `X` (bounded by a polynomial in
`chi`, `|v|^(-1)`, `r^(-1)` as recorded in the [C6] §6 table).

*Proof.* Apply the Kac–Rice formula of [RM] (12) under `Q_X` to the remote region `D_rho` and the window. It requires
the conditional covariance of `Y_x = (grad f(x), f(x))`, `x in D_rho`, given the conditioning σ-algebra, to be uniformly
nonsingular. Since `|X| <= A r`, only the pin-ball and collar regimes of [DL] §§4–5 occur. The σ-algebra of `(U_r, grad f(X))`
is that of `(U_r, Y')` for the normalized regime frame `Y'` (the frame `Y` of [DL] (4.5) in the pin ball; the
`D_r^(-1)`-scaled interpolation frame of [DL] §5.2 in the collar), an invertible re-expression; these normalized frames
have uniform covariance sandwiches and converge in `L^2` to linear images, of full row rank ([DL] Lemma D3 and §5.1),
of the midpoint jets of order at most five. `Y_x` is a jet at the distinct site `x`, `|x| >= rho`. By the distinct-site
jet rank of [LP] §2 the covariance of the limiting vector `(U_0, lim Y', Y_x)` is uniformly positive definite on the
compact parameter set, so for small `r` its Schur complement, the conditional covariance of `Y_x` given `(U_r, Y')`,
is bounded below by `c(rho) I`, uniformly in `X` and in the regime. Therefore the conditional density of `Y_x` at `(0, t)` is at most `C(rho)`, and the conditional
expectation of `F_j(H_x)` given `Y_x = (0, t)` is at most `C E[(1 + |H_x|)^d | ...] <= C (1 + beta_X)^d`, since the
regression mean of the far jets is linear in the frame targets with bounded coefficients, and the frame target minus
its mean is what `beta_X` measures ([C6] Lemma 4.1 and Lemma 4.4). Integrating over `D_rho` and the window of length
`k r^3` gives (5.3). ∎

**Lemma 5.2 (no near–far cross term).** For `A >= 4` and `rho <= s_0`,

    Q_r^W{ N_near^A >= 1, N_far^rho >= 1 } <= E_(Q_r^W)[ N_near^A 1{ N_far^rho >= 1 } ] <= C(A, rho) r^(9/2).       (5.4)

*Proof.* The mark `1{N_far^rho >= 1}` is `sigma(f)`-measurable and bounded, so [C6] Lemma 5.1 (gradient-only kernel,
all heights, which dominates the windowed near count) gives

    E[ N_near^A 1{N_far >= 1} ] <= sum_j integral_(|X| <= A r) p_(grad f(X) | U_r)(0) E[ W_r F_j(H_X) 1{N_far >= 1} | U_r, grad f(X) = 0 ] dX.

Cauchy–Schwarz on the conditional expectation, `1{N_far >= 1} <= N_far`, and (5.3) bound the integrand by

    p_(grad f(X)|U_r)(0) E[ (W_r F_j(H_X))^2 | . ]^(1/2) ( C k r^3 (1 + beta_X)^d )^(1/2).

By [C6] (5.3) and the §6 regime table, the density times the square root of the squared-weight conditional moment is
bounded, in every regime, by the source's unmarked intensity bound times `(1 + beta_X)^(3d)`, and the regime's
Gaussian penalty absorbs the additional `(1 + beta_X)^(d/2)` as it absorbs [C6]'s marked factor: in every regime of
[C6] §6.2 the absorption of a power of `beta_X` is by an exponential factor in the degeneracy variable, and any fixed
polynomial degree is absorbed by raising the index of the exponential series there (the ledgers `2n >= 6 + 3d`,
`2n/3 >= 15 + 39d` are the recorded choices for [C6]'s degree; a larger `n` serves here at the cost of the constant). The
regional ledgers then give `integral_(|X| <= A r) (...) dX <= C(A) r^3`. Multiplying by `(C k r^3)^(1/2)` gives (5.4). ∎

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
Proposition 4.4, then let `A -> oo` and `rho -> 0` using Proposition 4.4's monotone limit and §5.2:

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
Finiteness of (1.3): the limit integrand is dominated by `g_(A, eta)` on `{|det D| >= eta}` (Lemma 4.2), and its
integral over `{|det D| < eta}` is at most `C eta` by the argument of Lemma 4.3 applied to the limit integrand (the
factor `(det D)^2` against the `|det D|^(-2)` range of `s`); let `eta -> 0`. Continuity in `(b, k, R)`: `m`, `w_0`, `z_0`, `F_0` and `Lambda` depend continuously on
the parameters, the indicator `1{N_oo = n}` is continuous off a null set, and the dominating function of Lemma 4.2 is
locally uniform; dominated convergence in the parameters gives continuity.

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

Same proof as Proposition 4.4 with the bounded functional `sum_(extra near critical points) phi(scaled data)` in place of
the indicator: Lemma 4.1 gives the convergence of the scaled positions and heights, the sum has at most `N^A` terms with
`N^A -> N_oo^A <= 2`, and Lemma 4.2 with `sup |phi|` dominates; then `A -> oo`. The transverse scaled distance of a
critical point at sheared coordinates `(X, Z, W)` is `|S(Z, rW)| = |Z| (1 + |q|^2)^(1/2) + O(r)`.

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
load-bearing for the shells), and it is the analytic content of Lemma 3.3 and Lemma 4.2.

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
  upper window edge or below the lower one. No statement about elder selection is made; the extra points may be maxima
  or saddles (index `2 + (d - 2)` or `1 + (d - 2)`), and both cases have positive weight.
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
- `RS`: the resultant of `partial_X F_0, partial_Z F_0` in `Z` equals `(X^2 - 1/4) Q_2(X)` with the coefficients (3.6),
  as an identity in `Q[X, s, a_3, beta, c_3, k]`.
- `EX`: the six configurations of §7.2: exact critical points, heights, window membership, pin weights, `N_oo`; the
  [LM] weight `45 k^4`; the [LM] double root of `Q_2`.
- `BD`: the block-determinant expansion (3.8) for `d = 3` and `d = 4` as an exact identity in `r` (the `r^2`
  coefficient is `det D . det M_2`, the remainder is divisible by `r^3`).
- `EU`: the Euler identity `xi G_xi + zeta G_zeta = 3 G_3 + zeta^2` for the limiting cubic-plus-quadratic `G`, hence
  `G = zeta^2/6` at its critical points, and `zeta = 0 => xi = 0`.
- `LG`: the exponent ledgers: `1 + 4 - 2 = 3`; the cross term `3 + 3/2 > 3`; the shell error `A^(-2) + rho^2`; the
  tail `p/2 > 4d + 1`; the uniform-integrability step of §6.3.

Seven mutants (`pins-not-critical`, `wrong-pin-hessian`, `drop-sigma-jacobian`, `three-extra-points`,
`cross-term-not-small`, `window-closed`, `index-sign`) each exit `1`. The controls verify identities, exact
configurations and exponent bookkeeping only. They do not verify the Gaussian regression, the dominated convergence,
the stability argument or the Kac–Rice steps; those are the written arguments and the cited sources.

## 11. Attribution and reconnaissance

The mechanism of §§3–4 is the rare-set construction of [EDL] §§3–9 and [LM] §§2–6, used here as a limit theorem
rather than as a lower bound. The dominated-convergence device is that of [LP] §13 and [RM] §5. The local normal form
is a cusp-type unfolding of a planar cubic; no novelty is claimed for that algebra, which is classical (V. I. Arnold,
*Catastrophe Theory*, 3rd ed., Springer 1992, for the fold and cusp normal forms; the specific pinned cubic is the
one written in [LM] (L6) and [EDL] (A17)). `RECONNAISSANCE.md` records that the external literature check remained
blocked by the Consensus monthly quota and that no citation was invented.
