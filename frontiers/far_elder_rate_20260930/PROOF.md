# Short bars are born at soft maxima: a rate for the far elder density

Object: CL-FAR-ELDER-RATE-20260930-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 30 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register,
graph, STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is claimed. Same GitHub account as
every lane; zero organizational independence.

## 0. Statement

Fixed `d ≥ 2`, torus `X = R^d/(LZ^d)`, the variance-one periodized Gaussian field of [P] §1, and a fixed
separation `ρ ∈ (0, L/2]`. For `y ∈ X` with `dist(0, y) ≥ ρ` write, as in [P] §14 and [Z] §1,

    O_y = (f(0), ∇f(0), f(y), ∇f(y)),      v_{b,ℓ} = (b, 0, b − ℓ, 0),
    p_y(v) = the Gaussian density of O_y at v,      Q_{y,b,ℓ} = the regression law given O_y = v_{b,ℓ},
    W(f) = |det H_0 det H_y| 1{H_0 < 0, index H_y = d − 1},      e_y(f) = the Borel ordinary elder mark
    ([P] §8: the global superlevel elder death partner of the maximum at 0 is the saddle at y).

The far elder density per unit volume at lifetime `ℓ` is the canonical marked Kac–Rice version ([P] §9 read as
[E2]; the height Jacobian is 1 on this domain, [P] §14)

    ν_eld^{far,ρ}(ℓ) = ∫_{dist(0,y) ≥ ρ} ∫_R p_y(v_{b,ℓ}) E_{Q_{y,b,ℓ}}[W(f) e_y(f)] db dy.            (0.1)

The argument of [P] §14 gives `ν_eld^{far,ρ}(ℓ) ≤ C` for `0 < ℓ ≤ 1` ((14.1) is its case `ρ = r_0`); [Z] (Z11)–(Z12),
with the dominator of [Z] §4 on `D_ρ × R`, give `ν_eld^{far,ρ}(ℓ) → 0` as `ℓ ↓ 0` with no rate. The SIDE24 manuscript
(30 July 2026 revision, supplement Proposition A.3.2, restated as A.3.2′ in the 2026-08-01 amendment) asserts an
`O(ℓ)` bound for this quantity on `(0, ℓ_0]`; the July audit (F-02) found the supplement's proof of the rate invalid,
and no repository record proves it.

**Theorem F.** There is `C = C(d, L, ρ) < ∞` such that

    ν_eld^{far,ρ}(ℓ) ≤ C ℓ^{2/3},        0 < ℓ ≤ 1.                                                (0.2)

**Lemma 1 (deterministic; every short bar is born at a soft maximum).** Let `f ∈ C³(X)`, let `M` be a point
with `∇f(M) = 0` and `D²f(M) < 0`, put `λ = λ_min(−D²f(M)) > 0` and
`K = 1 + sup_X ‖D²f‖_op + sup_X ‖D³f‖_op`. With `a_L = min(1, L/4)` and `R = a_Lλ/K`,

    f(M + z) ≤ f(M) − (λ/3)|z|²        for |z| ≤ R,                                                 (1.1)
    ℓ(M) := f(M) − d_f(M) ≥ c_L λ³/K²,   c_L = a_L²/3,                                              (1.2)

where `d_f(M) = sup{min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M)}` is the ordinary superlevel maximin of [P] §8
(`d_f = −∞` for an essential maximum, and (1.2) then holds trivially). Equivalently: a finite `H_0` bar of
lifetime `ℓ` is born at a maximum with

    λ_min(−D²f(M)) ≤ (ℓK²/c_L)^{1/3}.                                                            (1.3)

Lemma 1 is (8)–(9) of Math- #182 §3 (OpenAI; integrated into `main` on 2026-09-30 at `2a10ed3`, blob `0d401877`;
accepted at Slice A by this author on 2026-09-30); its five-line proof is repeated in §1 so that this note is
self-contained and consumes nothing unmerged.

**Corollary F1 (far bars).** For every `t ∈ (0, 1]`, `E N_eld^{far,ρ}(0, t] ≤ (3/5)C t^{5/3}` per unit volume, and
for every real `q > −5/3`, `E Σ_{far elder bars, ℓ_i ≤ t} ℓ_i^q ≤ C_q t^{q + 5/3}`. In particular the far elder
population has inverse-lifetime integrability at least up to `p < 5/3`, against the `p < 2/3` threshold of the
leading `ℓ^{−1/3}` density ([P] §12, [R] §8).

**Corollary F2 (for the manuscript).** In the near/far decomposition of Theorem R ([R] §7, with `ρ = r_0`),
`ν_eld(ℓ) = ν_eld^{near}(ℓ) + O(ℓ^{2/3})` for `0 < ℓ ≤ 1`. This sharpens only the far term; Theorem R's absolute
`O(1)` remainder (R1) is dominated by its near terms (R16), (R18) and by the `O(1)` of [P] (14.1), and is
unchanged. What (0.2) supplies is a proven far-elder rate that may replace the manuscript's unproven `O(ℓ)`
(Proposition A.3.2 / A.3.2′) in the V3 text; the same proof gives `C(ℓ_0)ℓ^{2/3}` on any range `(0, ℓ_0]`. The
manuscript uses A.3.2 only to conclude that the far elder contribution is `o(ℓ^{−1/3})`, which boundedness already
gives.

**What is not claimed.** No rate for the far *rejected* density (on `D_ρ` it tends to `∫_{D_ρ}∫Ψ_0 db dy ∈
(0, B_{d,L})`, [Z] (Z5), and has the lower bound `c_*` of [U] (U1) at `ρ = r_0`); no near-pair statement beyond
(1.3); no numerical `C`; no uniformity in `L`, `d` or `ρ ↓ 0`; nothing about the true
order of `ν_eld^{far,ρ}` (§4 explains why it is expected to be far smaller than `ℓ^{2/3}`).

## 1. Proof of Lemma 1

Since `K ≥ sup‖D²f‖_op ≥ λ`, `R = a_Lλ/K ≤ a_L ≤ L/4 < L/2`, so the ball `B(M, R)` is embedded in the torus.
For a unit vector `v` and `0 < t ≤ R`, Taylor's theorem with the global third-derivative bound gives

    f(M + tv) ≤ f(M) + (t²/2) vᵀD²f(M)v + (K/6)t³ ≤ f(M) − (λ/2)t² + (K/6)t³.

For `t ≤ R ≤ λ/K` the cubic term is at most `(K/6)t²(λ/K) = (λ/6)t²`, which gives (1.1). Hence no point of
`B(M, R)` lies above `f(M)`, and every continuous path from `M` to a point above `f(M)` crosses the sphere
`|z − M| = R`, on which `f ≤ f(M) − λR²/3` by (1.1). Therefore `d_f(M) ≤ f(M) − λR²/3`, i.e.
`ℓ(M) ≥ λR²/3 = (a_L²/3)λ³/K²`, which is (1.2); (1.3) is (1.2) solved for `λ`. If no path to an older point
exists, `d_f = −∞` and (1.2) is trivial. ∎

The bound has the right exponent for the near law: for a pinned pair at separation `r` and gap `ℓ = kr³`, the
axial curvature at `M` satisfies `λ ≤ −f_xx(M) ≤ 6kr + r²M_4/2` ([P] (5.2)), and `K ≥ 1 + sup|f_xxx| ≥ 1 + 12k`
exactly, because the pinned row `U_3 = 12k` of [P] (3.1) is an average of `f_xxx` against a nonnegative kernel.
With `λ = 6kr`, `c_Lλ³/K² = 216c_Lk³r³/K² ≤ 216c_Lk²/(1 + 12k)² · ℓ < ℓ/2` for `c_L ≤ 1/3`. So for near pairs (1.3)
is satisfied automatically with the same exponent (`λ ≍ ℓ^{1/3}` on both sides), while for far pairs it is a
genuine restriction.

## 2. Fixed-separation Gaussian facts (reconstructed; no contact limit)

Let `D_ρ = {y ∈ X : dist(0, y) ≥ ρ}`, compact. Append to `O_y` the independent entries of `H_0 = D²f(0)` and
`H_y = D²f(y)`:

    V_y = (O_y, H_0, H_y)   (2(d + 1) + d(d + 1) coordinates).

All these functionals are distinct derivative evaluations at two distinct sites, so by [P] §2 their covariance
`Γ_y` is positive definite for each `y ≠ 0`; it is continuous in `y`, hence uniformly positive definite on the
compact `D_ρ` (this is the compactness argument of [P] §14, applied to the enlarged list). Consequently:

(a) the joint density of `V_y` at `(v_{b,ℓ}, H_0, H_y)` is at most `C exp[−c(|v_{b,ℓ}|² + |H_0|² + |H_y|²)]`,
    and since `|v_{b,ℓ}|² ≥ b²`,

        p_y(v_{b,ℓ}) · density(H_0, H_y | O_y = v_{b,ℓ}) ≤ C exp[−c(b² + |H_0|² + |H_y|²)],                  (2.1)

    uniformly for `y ∈ D_ρ`, `b ∈ R` and every `ℓ` (`V_y` is centred; only the uniform eigenvalue bounds of `Γ_y`
    enter);

(b) regressing the whole field on `V_y` ([P] §4's argument at a fixed pair of sites) gives `f = m + g` with
    `g` independent of `V_y`, `E‖g‖_{C³}^q ≤ C_q` uniformly on `D_ρ`, and `‖m‖_{C³} ≤ C(1 + |b| + |H_0| + |H_y|)`
    for `ℓ ≤ 1` (the regression coefficients are fixed smooth covariance derivatives times the uniformly
    bounded `Γ_y^{−1}`). Hence, with `K = 1 + sup‖D²f‖ + sup‖D³f‖`, for every `q ≥ 1`

        E[K^q | V_y = (v_{b,ℓ}, H_0, H_y)] ≤ C_q (1 + |b| + |H_0| + |H_y|)^q.                                (2.2)

    Under the regular conditional law the field is smooth almost surely ([E2] §9.1 constructs it on `C²`; the
    same regression gives a `C^∞` version), so `K` is a.s. finite and (2.2) is a statement about that law.

Nothing here tends to `r = 0`; no normalizer or cap estimate is used.

## 3. Proof of Theorem F

Fix `y ∈ D_ρ`, `b`, `0 < ℓ ≤ 1`, and work under `Q = Q_{y,b,ℓ}`. On the event `{W(f) > 0, e_y(f) = 1}` the point
`0` is a nondegenerate maximum with `f(0) = b`, and its death partner is the saddle at `y` with
`f(y) = b − ℓ`, so `d_f(0) = b − ℓ` and Lemma 1 gives, with `λ = λ_min(−H_0)`,

    ℓ ≥ c_L λ³/K²,      i.e.      K ≥ (c_L λ³/ℓ)^{1/2}.

Hence, pathwise,

    W(f) e_y(f) ≤ W(f) 1{K ≥ (c_Lλ³/ℓ)^{1/2}}.                                                       (3.1)

`W` is a function of `(H_0, H_y)`, so conditioning on `V_y` and applying Markov's inequality with (2.2),

    E_Q[W e_y] ≤ E_Q[ W · min{1, C_q(1 + |b| + |H_0| + |H_y|)^q (ℓ/(c_Lλ³))^{q/2}} ].                       (3.2)

Multiply by `p_y(v_{b,ℓ})` and use (2.1); bound `(1 + |b| + |H_0| + |H_y|)^q ≤ (1 + |b|)^q(1 + |H_0|)^q(1 + |H_y|)^q`,
take the two Hessian factors outside the minimum (`min{1, xy} ≤ y·min{1, x}` for `y ≥ 1`), and integrate `H_y`
against `|det H_y|(1 + |H_y|)^q e^{−c|H_y|²}` (a constant). For `H_0` use the ordered spectral
coordinates of `−H_0 = O diag(λ_1 ≤ … ≤ λ_d) Oᵀ` on the cone `{H_0 < 0}` (Lebesgue Jacobian
`const · ∏_{i<j}(λ_j − λ_i)`, finite angular volume, as in [P] §7): with `|det H_0| = ∏λ_j`, bounding the
Vandermonde and `∏_{j≥2}λ_j` by a polynomial in `|λ|`, extending `λ_2, …, λ_d` to `(0, ∞)` and integrating them,

    p_y(v_{b,ℓ}) E_Q[W e_y]
      ≤ C e^{−cb²} ∫_0^∞ λ_1 min{1, A (ℓ/λ_1³)^{q/2}} (1 + λ_1)^N e^{−cλ_1²} dλ_1,      A = C(1 + |b|)^q.      (3.3)

Let `u = (A^{2/q}ℓ)^{1/3}`, the point where the two arguments of the minimum agree. If `u ≥ 1`, bound the minimum by
`1`: the integral is at most `C ≤ Cu²`. If `u < 1`, split at `u` (on `[0, u]` bound `(1 + λ_1)^N e^{−cλ_1²} ≤ 2^N`):

    ∫_0^u λ_1 (1 + λ_1)^N e^{−cλ_1²} dλ_1 ≤ 2^{N−1} u²,
    ∫_u^∞ λ_1 · A ℓ^{q/2} λ_1^{−3q/2} (1 + λ_1)^N e^{−cλ_1²} dλ_1
        ≤ A ℓ^{q/2} [ C ∫_u^1 λ^{1 − 3q/2} dλ + C ] ≤ C A ℓ^{q/2} (u^{2 − 3q/2} + 1) ≤ C u²,

using `3q/2 > 2` (any `q > 4/3`; take `q = 2`) and `Aℓ^{q/2} = u^{3q/2}`, `u ≤ 1`. In every case the integral in (3.3) is at most
`Cu² = C A^{4/(3q)} ℓ^{2/3} = C (1 + |b|)^{4/3} ℓ^{2/3}`. Therefore

    p_y(v_{b,ℓ}) E_Q[W e_y] ≤ C (1 + |b|)^{4/3} e^{−cb²} ℓ^{2/3},

and integrating over `b ∈ R` and `y ∈ D_ρ` (volume at most `L^d`) in (0.1) proves (0.2). ∎

The proof retains the determinant weight throughout: the factor `λ_1` inside (3.3) is `|det H_0|`'s soft
eigenvalue, and it is what turns the barrier constraint `λ_1 ≲ ℓ^{1/3}` into the mass `ℓ^{2/3}`. Dropping the weight
(a raw Gaussian conditioning on the two types) would give only `ℓ^{1/3}`.

## 4. What the rate does and does not say

* (1.3) is deterministic and general: for any `C³` function on the torus, on the Morse distinct-critical-value
  locus (where the bar born at `M` has lifetime `f(M) − d_f(M)`), every finite bar of lifetime `ℓ` is born at a
  maximum whose weakest curvature is at most `(ℓK²/c_L)^{1/3}`; off that locus (1.1) still shows that the
  component of `{f > f(M) − λR²/3}` containing `M` lies inside `B(M, R)` with `M` as its unique maximum. For the near population this is the
  scaling `λ ≍ 6kr = 6(k²ℓ)^{1/3}` already built into [P]; for the far population it is a genuine restriction,
  and (0.2) is its cost under the Kac–Rice weight.
* The bound is not expected to be sharp. For `y` to be the death saddle of `0` at gap `ℓ` with `dist(0, y) ≥ ρ`,
  the superlevel component of `0` at level `b − ℓ` must reach `y` without meeting any point above `b`: the field
  stays within a band of width `ℓ` along *some* curve of length `≥ ρ`. I expect the probability of such an
  event to decay faster than any power of `ℓ` (for a fixed curve it is a small-ball event of a smooth Gaussian
  process; here the curve is chosen by the field, and no such estimate is proved anywhere in the repository);
  the barrier captures only its first factor, a soft maximum. Nothing beyond (0.2) is claimed.
* Corollary F1 follows from (0.2) by integrating `ℓ^{2/3}` (for the count) and `ℓ^{q + 2/3}` (for the moments,
  finite at `0` iff `q > −5/3`). Corollary F2 is (0.2) inserted into [R] §7, where the far term entered only as
  the `O(1)` of [P] (14.1).
* Consistency with [U] and [Z]: the far *rejected* density has the positive lower bound `c_*` ([U] (U1), at
  `ρ = r_0`) and, on `D_ρ`, tends to the positive limit `∫_{D_ρ}∫Ψ_0 db dy` ([Z] (Z5)); (0.2) says the far *elder*
  density is the vanishing part, at rate at least `ℓ^{2/3}`. Nothing in (0.2) bears on the rejected part.
* Method. The barrier–Markov–spectral route is that of Math- #182 §§2–4 (fixed-`r` pinned pair, upper bound of
  its Theorem 1), including the remark that dropping the determinant weight would give `ℓ^{1/3}`. What is new
  here is the transplant to a far saddle pinned at gap `ℓ`, the uniformity over the compact separation set
  `D_ρ`, the `b`-growth bookkeeping and the `(b, y)` integration that turns it into a density rate.

## 5. Sources (exact identities in `SOURCES.json`)

| Tag | Source | Consumed |
|---|---|---|
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (`dfed3b8d`) | §1 model; §2 distinct-site rank; §3 (3.1) row `U_3` and §5 (5.2) (only in the near-pair remark of §1); §4 regression argument (used at a fixed pair of sites); §7 spectral Lebesgue coordinates; §8 maximin definition and Borel elder mark; §9 marked Kac–Rice as [E2]; §14 far domain, uniform covariance, height Jacobian 1, (14.1). Read with [E1], [E2], [REC] §1. |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (`213594d6`) | reading rule (not used in any step here). |
| [CAP] | `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md` (`0633aca3`) | reading rule of [REC] §1 (not used in any step here). |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (`fe9b9ce4`) | §9.1–9.4: regular conditional law on the field space, Borel weights on compact off-diagonal domains, the elder/type mark. |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (`75da2597`) | §1 reading rule for [P]; §7 consumption contract (this note consumes only §§2, 4, 7–9, 14 conventions and (14.1)). |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (`5b6328ea`) | cited only: (Z1) notation, Theorem Z, (Z11)–(Z12) as the `o(1)` predecessor. |
| [U] | `frontiers/unrestricted_selection_difference_20260929/PROOF.md` (`5a55b179`) | cited only: (U1). |
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (`247b3ecf`) | cited only: §7 near/far decomposition, §8 moments. |
| [182] | Math- #182 `frontiers/fixed_r_inverse_lifetime_20260930/PROOF.md` (integrated at `2a10ed3` on 2026-09-30; blob `0d401877`) | cited only: §3 (8)–(9) is Lemma 1 and §§2, 4, 7 are the method (see §4); every step is re-proved here, nothing unmerged is consumed. |

## 6. Finite controls

`far_elder_check.py` (standard library, exact rationals): B1 the barrier inequality (1.1) on an explicit polynomial
at rational points of the ball; B2 the algebraic core of (1.1) (`Kt³/6 ≤ λt²/6` for `t ≤ λ/K`) and the constants
`a_L`, `c_L`; I1 the split integral of §3 in closed form and the inequality `∫_0^u λ dλ + ∫_u^1 λ(u/λ)^{3q/2} dλ ≤
u²(1/2 + 1/(3q/2 − 2))` at rational `u, q`; I2 the exponent ledger (`u³ = A^{2/q}ℓ`, `u² ∝ ℓ^{2/3}`, the `5/3`
threshold and count exponent); N1 the near-pair consistency inequality `6(6c_L)^{1/2} < 12`; mutants `M1`–`M4`
exit 1, unknown label exits 2. These are algebra and calculus controls; they do not prove the Gaussian step.

## 7. Review division

* **Slice A (deterministic):** Lemma 1 and §1. Lemma 1 is OpenAI's (#182) and was accepted there by this author;
  a provider distinct from both is xAI.
* **Slice B (Gaussian):** §2 and §3 — the uniform fixed-separation regression, the conditional Markov step (3.2),
  the spectral integration (3.3) and the split. Best read by a lane not exposed to [P]'s authorship.
* **Slice C (consequences):** Corollaries F1–F2 and the honest §4.
