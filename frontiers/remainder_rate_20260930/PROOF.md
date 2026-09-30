# The remainder of Theorem R has a rate: `ν_eld(ℓ) = cℓ^{−1/3} + O(ℓ^{1/4})`

Object: CL-D2-REMAINDER-RATE-20260930-v1.1 (v1 → v1.1, same day, before any nonauthor read: the exponent `1/6` of v1
is raised to `1/4` by the sign-window majorant Lemma W, which the clean-context referee pass on v1 suggested as a
heuristic and which turns out to need only the sign structure of the typed weight and Lemma E's Steps 1–3; Lemma B,
Lemma F′ and the assembly are otherwise unchanged; v1's ledger and its `1/6` survive as a parenthetical in §4. A second
referee pass, on v1.1's §§3–5, found Lemma W proved and the assembly correct, and corrected the dependency
statements, Remark 1 and the term count of §4).
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 30 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register,
graph, STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is claimed. Same GitHub account as
every lane; zero organizational independence. **Dependency:** this note consumes Theorem R+ (R+.3), all of Lemma E
(Steps 1–5 through (E.1); Steps 1–3 alone for Lemma W (W.1), (W.3), (W.4)), and §2 ((2.1), the domination, the
`k = 0` identity) of Math- #191 (`frontiers/remainder_vanishing_20260930/PROOF.md`, v1.1, blob `441152df`; an unmerged
author-side candidate of this session with one nonauthor read, xAI 5369140697, findings applied). It cannot be integrated before #191 and
must be rebound if #191 changes. Everything else consumed is merged and reviewed: [R], [C7-K], [182], [Z] and the
reconciled [P] chain.

## 0. Statement

Setting and notation are those of [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`)
and of #191 §0: fixed `d ≥ 2`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`; the elder lifetime density `ν_eld(ℓ)`
(the manuscript's `ν_{3,24}` at `d = 3`, `L = 24`), the candidate density `ν_cand(ℓ)`, the rejected density
`ρ_rej = ν_cand − ν_eld`, all per unit volume ([C7-K] §0); the near pins `M = −ru/2`, `S = ru/2` at heights `b`,
`b − kr³`, the regression law `Q = Q_{r,b,k}`, the typed weight `W_r = |det H_M det H_S|1{H_M < 0, index H_S = d − 1}`,
`W_r/r² = F_d(K_M)F_{d−1}(K_S)` in the scaled Hessians of [R] §4, the pin density `π_r(v_r)`, `P = 1 + |b| + k`; the
elder mark `e = 1{d_f(M) = f(S)}` with the maximin `d_f(M) = sup{min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M)}` ([P] §8;
Borel, [E2] §9); the leading coefficient `c = c_{d,L}` of [P] (15.2); superscripts `near,ρ` / `far,ρ` for the
separation ranges `dist(M, S) < ρ` / `≥ ρ` ([R] §7, [C7-K] §4); and the admissible radius
`r_0^* = min{r_0^{[R]}, L/(4√2), r_0^{[K]}, r_0^{[Z]}}` of #191 §0. `C, N` denote constants depending on `d, L` only,
changing from line to line.

**Theorem R++ (rate for the elder remainder).** For the canonical marked Kac–Rice version of the elder density
([P] §9 read as [E2]; the version every input below concerns, and the pointwise representative the manuscript's
supplement C.4 fixes), there are `C < ∞` and `ℓ_0 ∈ (0, 1]` depending on `d, L` only such that

    |ν_eld(ℓ) − c ℓ^{−1/3}| ≤ C ℓ^{1/4},        0 < ℓ ≤ ℓ_0;                                              (0.1)

equivalently

    ν_eld(ℓ) = c ℓ^{−1/3} (1 + O(ℓ^{7/12}))        as ℓ ↓ 0.                                             (0.2)

The proof has three new estimates. Two are elementary consequences of the deterministic barrier of [182] §3
(Lemmas B, F′); the third (Lemma W) is a majorant for the unmarked near-pair weight that improves [C7-K] (K1) at
small gap marks, using only the sign structure of the typed weight and the expansions of #191 Lemma E, Steps 1–3:

**Lemma B (short elder bars at near separations are born at soft maxima).** For `0 < r ≤ r_0^{[R]}`, `b ∈ R`,
`k > 0`, with `ℓ = kr³`,

    E_Q[(W_r/r²) e] ≤ C ℓ^{1/3} r^{−1} (k + r) P^N,                                                        (B.1)

and consequently, for `0 < ρ ≤ r_0 ≤ r_0^{[R]}`, the elder density at separations in `[ρ, r_0)` satisfies (an empty
range, and `0`, when `ρ = r_0`)

    ν_eld^{[ρ,r_0)}(ℓ) := ∫_ρ^{r_0}∫_R∫_{S^{d−1}} r^{−2} A_r^{eld}(b, ℓ/r³, u) dσ(u) db dr ≤ C ℓ^{1/3} (ρ^{−1} + ℓρ^{−5}),   (B.2)

where `A_r^{eld} := 12π_r(v_r)E_Q[(W_r/r²)e]` (the elder-marked version of [R]'s `A_r`; [C7-K] §4, [Z] (Z13)–(Z14)).

**Lemma F′ (far elder density, crude rate).** For every fixed `r_0 ∈ (0, L/2]` there is `C = C(d, L, r_0)` with

    ν_eld^{far,r_0}(ℓ) ≤ C ℓ^{1/3},        0 < ℓ ≤ 1.                                                    (F′.1)

(Math- #187, unmerged, proves `Cℓ^{2/3}` by keeping the determinant weight through a spectral integration; (F′.1)
is the one-line version that needs no Hessian density, and it suffices here because the far term is not the
bottleneck of the ledger in §4.)

**Lemma W (sign-window majorant for the near-pair weight).** For `0 < r ≤ r_0^{[R]}`, `b ∈ R`, `k ≥ 0` (the pinned
family at `k = 0` included: nothing below divides by `k`, and (R2)–(R5) do not depend on the target),

    E_Q[W_r/r²] ≤ C (k² + r⁴(1 + k)²) P^N.                                                                (W.1)

(Compare [C7-K] (K1): `C(k + r)²P^N`. Since `k² + r⁴(1 + k)² ≤ 2(1 + r_0)²(k + r)²`, (W.1) is never worse; for `k < r`
it is better by the factor `k²/r² + r²`.) Consequently, for `0 < ρ ≤ r_0^*` and `0 < ℓ ≤ 1`:

    |ν_cand^{near,ρ}(ℓ) − cℓ^{−1/3}| ≤ C (min(ℓ^{1/4}, ρ) + ρ³ + ℓ²ρ^{−7}),                                     (W.2)
    0 ≤ ρ_rej^{near,ρ}(ℓ) ≤ C (ℓ^{1/4} + ρ³),                                                                (W.3)
    ∫_{0 < dist(0,y) < ρ} ∫_R Ψ_0(b, y) db dy ≤ C ρ³                                                       (W.4)

— (W.2) sharpens #191 (R+.3) (`C(ρ + ℓ²ρ^{−7})`) for `ρ ≳ ℓ^{1/4}`, (W.3) sharpens [C7-K] §4's near rejected bound
(`C(ℓ^{1/4} + ρ)`), and (W.4) says the equal-height kernel mass of [Z] (Z3) below separation `ρ` is `O(ρ³)`, sharpening
[Z] (Z18)'s `Cδ` for the limit object (the radial density `r^{d−1}Ψ_0(b, ru)` is `O(r²)`). (W.1), (W.3), (W.4) use only
Steps 1–3 of Lemma E; (W.2) uses (E.1), i.e. all of Lemma E.

**What is not claimed.** No sharpness of the exponent `1/4` in either direction (§5 explains what fixes it — the
transition `r = k` at separation `ℓ^{1/4}` — and records, as unproved, a formal leading-order computation from the
second referee pass suggesting that `ℓ^{1/4}` is the true order, with a negative coefficient); no numerical `C`, `ℓ_0`; no rate for the *candidate* remainder (`ν_cand = cℓ^{−1/3} + B_{d,L} + o(1)` of
#191 stays without a rate: the far candidate kernel's dependence on `ℓ` is not quantified anywhere); no rate for
`ρ_rej(ℓ) → B_{d,L}` (Theorem Z); no uniformity in `d`, `L`; no finite-radius band; no RN / 24-jet closure; nothing
beyond the existential scope of Theorem R, Theorem R+ and [C7-K].

## 1. Proof of Lemma B

Under `Q` the field is almost surely `C^∞` (`Q` is the law of `F_r` in the coupling [R] (R3); [E2] §9.1). Fix a
realisation `f` in the event `{W_r > 0} ∩ {e = 1}`. Then `∇f(M) = 0`, `f(M) = b`, `H_M = D²f(M) < 0`, and, by the
definition of the elder mark, `d_f(M) = f(S) = b − kr³ = b − ℓ`, i.e. `b − d_f(M) = ℓ`. This is exactly the
situation of [182] §3, whose display (9) reads, for any `C³` field with `f(M) = b`, `∇f(M) = 0`, `H_M < 0`,
`λ := λ_min(−H_M)`, `K := 1 + ‖D²f‖_{∞,op} + ‖D³f‖_{∞,op}` (suprema over the torus), `a_L = min(1, L/4)`,
`c_L = a_L²/3`:

    b − d_f(M) ≥ c_L λ³ / K².                                                                          (1.1)

(Its proof, [182] §3 (8): for a unit vector `v` and `0 < t ≤ R := a_Lλ/K`, Taylor's theorem gives
`f(M + tv) ≤ b − (λ/2)t² + (K/6)t³ ≤ b − (λ/3)t²`, since `t ≤ λ/K`; the ball `B(M, R)` is embedded (`R ≤ L/4`), no
point of it lies above `b`, every path from `M` to a point above `b` crosses its boundary sphere, on which
`f ≤ b − λR²/3`; hence `d_f(M) ≤ b − λR²/3 = b − c_Lλ³/K²`.) So on the elder event

    λ_min(−H_M) ≤ (ℓ K² / c_L)^{1/3}.                                                                  (1.2)

Since `−H_M > 0` with eigenvalues `λ = λ_1 ≤ … ≤ λ_d ≤ ‖H_M‖_op ≤ K`,

    |det H_M| = ∏_j λ_j ≤ λ_1 K^{d−1} ≤ c_L^{−1/3} ℓ^{1/3} K^{d − 1/3}.                                     (1.3)

By the scaling dictionary of [R] §4 (`|det H_i|/r = |det K_i|`), `W_r/r² = (|det H_M|/r)·F_{d−1}(K_S)` on the support
of `W_r`, and [R] §4 bounds the typed scaled determinant at `S` through the exact block identity of Lemma R3.2 with
(R8)–(R9) — quoted: "The exact block determinant also gives `F_j(K_i) <= C(k+r) T^d`" — where `T ≥ 1 + k` is [R]'s
dominating variable with `‖T‖_p ≤ C_pP` for every `p` ((R9), from (R4)). Therefore, on `{W_r > 0} ∩ {e = 1}`,

    W_r/r² ≤ C ℓ^{1/3} r^{−1} (k + r) K^{d − 1/3} T^d,                                                    (1.4)

and `(W_r/r²)e ≤` the right side of (1.4) everywhere (`e ∈ {0, 1}`, `W_r ≥ 0`). Taking `E_Q`: `K ≤ C_d(1 + ‖F_r‖_{C³})`
has `‖K‖_p ≤ C_pP` by [R] (R4) with `q = 3` ("for finite p>=1 and each finite derivative order q,
`||1+||F_r||_{C^q}+||F_0||_{C^q}||_p <= C_{p,q} P`"), so Hölder gives `E_Q[K^{d−1/3}T^d] ≤ CP^N`, which is (B.1).

For (B.2): by [R] (R5), `π_r(v_r) ≤ Ce^{−c(b²+k²)}` for `r ≤ r_0^{[R]}`, so with `k = ℓ/r³`

    r^{−2} A_r^{eld}(b, ℓ/r³, u) ≤ C ℓ^{1/3} r^{−3} (ℓr^{−3} + r) P^N e^{−c(b²+k²)} ≤ C ℓ^{1/3} (ℓ r^{−6} + r^{−2}) (1 + |b|)^N e^{−cb²},

using `(1 + |b| + k)^N ≤ 2^N(1 + |b|)^N(1 + k)^N` and `(1 + k)^Ne^{−ck²} ≤ C`. Integrating over `S^{d−1}`, `b ∈ R` and
`r ∈ [ρ, r_0)`:

    ∫_ρ^{r_0} (ℓ r^{−6} + r^{−2}) dr = ℓ(ρ^{−5} − r_0^{−5})/5 + (ρ^{−1} − r_0^{−1}) ≤ ℓρ^{−5}/5 + ρ^{−1},

which is (B.2). ∎

The identity behind (B.2) — that the elder density at lifetime `ℓ` from separations in `[ρ, r_0)` is
`∫_ρ^{r_0}∫∫ r^{−2}A_r^{eld}(b, ℓ/r³, u)` — is the marked Kac–Rice disintegration of [P] §§9–10 read as [E2]: [P]
(10.2) gives the elder intensity `r A_r p_r dr db dk dσ` per unit volume with `A_r p_r = 12π_r(v_r)E_Q[(W_r/r²)e]`;
pushing forward at fixed `r` with `dk = dℓ/r³` gives the `ℓ`-density `r^{−2}A_r^{eld} dr db dσ`. In the `k` variable
this is [C7-K] §4's rejected intensity identity with the mark `e` in place of `1 − e`, and in the `r` variable it is
[Z] (Z13)–(Z14) with `e` in place of `1 − e`; for the unmarked weight the same display is [R] §6 and #191 (2.1).

## 2. Proof of Lemma F′

Write `D_{r_0} = {y ∈ X : dist(0, y) ≥ r_0}` (compact) and, as in [Z] §1 and [C7-K] §4, `O_y = (f(0), ∇f(0), f(y), ∇f(y))`,
`v_{b,ℓ} = (b, 0, b − ℓ, 0)`, `p_y` the density of `O_y`, `Q_{y,b,ℓ}` the regression law given `O_y = v_{b,ℓ}`,
`W = |det H_0 det H_y|1{H_0 < 0, index H_y = d − 1}`, `e_y = 1{d_f(0) = f(y)}`. The far elder density is the marked
Kac–Rice integral on this domain ([P] §9 as [E2], §14: the height Jacobian is `1` there),

    ν_eld^{far,r_0}(ℓ) = ∫_{D_{r_0}} ∫_R p_y(v_{b,ℓ}) E_{Q_{y,b,ℓ}}[W e_y] db dy.                             (2.1)

*Uniform Gaussian facts on `D_{r_0}`.* `Γ_y := Cov(O_y)` is positive definite for every `y ≠ 0` ([P] §2, distinct-site
rank) and continuous in `y`, hence `λ_min(Γ_y) ≥ c_0 > 0` on the compact `D_{r_0}` — the compactness argument of
[P] §14, used again in [Z] (Z16). Consequently:

(a) `p_y(v) ≤ (2πc_0)^{−(d+1)} exp(−|v|²/(2 tr Γ_y)) ≤ Ce^{−cb²}` at `v = v_{b,ℓ}` (`|v_{b,ℓ}|² ≥ b²`, `tr Γ_y ≤ C`);

(b) (Gaussian regression at two fixed sites, [P] §4's argument; [Z] §2, (Z10).) With
`ψ^y := Γ_y^{−1}Cov(O_y, f(·))` — `2d + 2` smooth functions on `X` with `‖ψ^y_j‖_{C³} ≤ C` uniformly on `D_{r_0}`
(covariance derivatives are bounded, `‖Γ_y^{−1}‖ ≤ 1/c_0`) — the field decomposes as `f = Σ_j O_y^j ψ^y_j + g_y`
with `g_y` a centred Gaussian field independent of `O_y`; under `Q_{y,b,ℓ}` the field has the law of
`Σ_j v_{b,ℓ}^j ψ^y_j + g_y`. Since `‖g_y‖_{C³} ≤ ‖f‖_{C³} + C|O_y|` and `E‖f‖_{C³}^p + E|O_y|^p ≤ C_p` ([P] §2, quoted:
"the field has a smooth version and all finite moments of its global derivative suprema exist"), `E‖g_y‖_{C³}^p ≤ C_p`
uniformly on `D_{r_0}`. Hence, for
`0 < ℓ ≤ 1` (`|v_{b,ℓ}| ≤ 2|b| + 1`), `K = 1 + ‖D²f‖_{∞,op} + ‖D³f‖_{∞,op} ≤ C(1 + |b| + ‖g_y‖_{C³})` and

    E_{Q_{y,b,ℓ}}[K^p] ≤ C_p (1 + |b|)^p        for every p ≥ 1, uniformly for y ∈ D_{r_0}, 0 < ℓ ≤ 1.        (2.2)

*The barrier.* On `{W > 0} ∩ {e_y = 1}` the point `0` is a nondegenerate maximum with `f(0) = b`, and
`d_f(0) = f(y) = b − ℓ` by the definition of the mark; [182] §3 (9), i.e. (1.1) with `M = 0`, gives
`λ_min(−H_0) ≤ (ℓK²/c_L)^{1/3}`, hence `|det H_0| ≤ c_L^{−1/3}ℓ^{1/3}K^{d−1/3}` as in (1.3), while `|det H_y| ≤ ‖H_y‖^d ≤ K^d`.
So `W e_y ≤ Cℓ^{1/3}K^{2d−1/3}` and, by (2.2), `E_{Q_{y,b,ℓ}}[W e_y] ≤ Cℓ^{1/3}(1 + |b|)^{2d}`. With (a) in (2.1),

    ν_eld^{far,r_0}(ℓ) ≤ C ℓ^{1/3} · vol(D_{r_0}) · ∫_R (1 + |b|)^{2d} e^{−cb²} db ≤ C ℓ^{1/3}.        ∎

## 3. Proof of Lemma W and of (W.2)–(W.4)

*The structure of the two scaled determinants.* Work under the coupling (R3) of [R] as in #191 §1 (`f = F_r`, `T` the
dominating variable with `‖T‖_p ≤ C_pP`, `A_0 = D_y²F_0(0)`, `Δ := det A_0`). #191 Lemma E, Steps 1–3, give — pathwise,
for `0 < r ≤ r_0^{[R]}` — the expansions #191-(1.1), #191-(1.3), #191-(1.5) and hence, multiplying out
`det K_i = α_i det A_i − rq_i` (Lemma R3.2 of [R]),

    det K_M = −6kΔ + rY + R_M,        det K_S = +6kΔ + rY + R_S,        |R_M| + |R_S| ≤ C r² (1 + k) T^{N_1},        (3.1)

with the *same* `Y = (f_4/12)Δ + 3k tr(adj(A_0)B) − q` (#191 §1, the display after (1.6): "`det K_M = −6k det A_0 + rY +
O(r²)` and `det K_S = +6k det A_0 + rY + O(r²)` with the same `Y`"). The `(1 + k)`-quantified remainder is derived here,
not quoted: with `τ := tr(adj(A_0)B)`, `det A_i = Δ ∓ (r/2)τ + E′_i`, `|E′_i| ≤ Cr²T^m` (from #191-(1.3)), `α_i = ∓6k +
(r/12)f_4 + ρ_i`, `|ρ_i| ≤ Cr²T` (#191-(1.1)), `q_i = q + O(rT^{m+1})` (#191-(1.5)), multiplying out gives

    R_M = −6kE′_M − (r²/24)f_4τ + (r/12)f_4E′_M + ρ_M det A_M − r(q_M − q),
    R_S = +6kE′_S + (r²/24)f_4τ + (r/12)f_4E′_S + ρ_S det A_S − r(q_S − q),

each term `≤ Cr²(1 + k)T^{N_1}` (the `k`-linear term is `6kE′_i`; the `O(r)` error of `q_i` enters as `r·O(rT^{m+1})`);
the `r`-linear terms — `(r/12)f_4Δ` from `α_i det A_i`, `+3krτ` from `(∓6k)(∓(r/2)τ)`, and `−rq` — are the same at
both endpoints, which is (3.1).

*The sign window.* On the support of `W_r`, `index K_M = d` and `index K_S = d − 1` (`K_i` is congruent to `H_i`), so
`det K_M` has the sign `(−1)^d` and `det K_S` the sign `(−1)^{d−1}`: `det K_M · det K_S < 0`. Put `w := rY`. By (3.1)
the product is `(w − 6kΔ + R_M)(w + 6kΔ + R_S)`, negative only when `w` lies strictly between the two roots
`6kΔ − R_M` and `−6kΔ − R_S`; hence

    |w| ≤ 6k|Δ| + max(|R_M|, |R_S|),        |det K_i| ≤ |w| + 6k|Δ| + |R_i| ≤ 12k|Δ| + 2 max(|R_M|, |R_S|)    (i = M, S),

and therefore, on the support of `W_r`,

    W_r/r² = |det K_M det K_S| ≤ (12k|Δ| + 2Cr²(1 + k)T^{N_1})² ≤ C (k²Δ² + r⁴(1 + k)²T^{2N_1}).                  (3.2)

Off the support `W_r = 0`. Taking expectations: `E[Δ²] ≤ E[T^{2m}] ≤ CP^{2m}` and `E[T^{2N_1}] ≤ CP^{2N_1}` (`|Δ| ≤ ‖A_0‖^m ≤
T^m`; (R4) bounds the moments of `F_0` as well as of `F_r`, and `W_r` is a functional of `F_r` alone, whose marginal on
the coupling space is `Q`, so a bound that holds pathwise on the coupling space bounds `E_Q`), which is (W.1). ∎

*Proof of (W.2).* Put `r_1 := ℓ^{1/4}` (so `r ≤ r_1 ⇔ k = ℓ/r³ ≥ r`) and use #191 (2.1): `ν_cand^{near,ρ} − cℓ^{−1/3} =
∫_0^ρ∫∫ r^{−2}(A_r − A_0)(b, ℓ/r³, u) − ∫_ρ^∞∫∫ r^{−2}A_0`. On `0 < r < min(r_1, ρ)`: #191 Lemma E (E.1) — Steps 1–5 —
`|r^{−2}(A_r − A_0)| ≤ H(b, k) ≤ Ce^{−cb²}`, contributes at most `C min(r_1, ρ)`. On `r_1 ≤ r < ρ` (empty if `ρ ≤ r_1`):
`|A_r − A_0| ≤ A_r + A_0` with `A_r = 12π_r(v_r)E_Q[W_r/r²] ≤ C(k² + r⁴(1 + k)²)P^Ne^{−c(b²+k²)}` by (W.1) and (R5), and
`A_0 ≤ k²H` (#191 §2); so `r^{−2}|A_r − A_0| ≤ C(ℓ²r^{−8} + r²)(1 + |b|)^Ne^{−cb²}` (the factor `(1 + k)^{N}e^{−ck²}` is
bounded), which integrates to `C(ℓ²r_1^{−7}/7 + ρ³/3) = C(ℓ^{1/4}/7 + ρ³/3)`. The tail is `≤ Cℓ²ρ^{−7}` (#191 §2). ∎

*Proof of (W.3).* `ρ_rej^{near,ρ} = ∫_0^ρ∫∫ r^{−2}A_r^{rej}` with `A_r^{rej} = 12π_r(v_r)E_Q[(W_r/r²)(1 − e)]` ([C7-K] §4, [Z]
(Z13)). On `0 < r ≤ min(r_1, ρ)`: `1 − e ≤ 1_{G_r^c}` on the generic locus ([C7-K] §4) and (K2) (valid as `r ≤ k` and
`r ≤ ρ ≤ r_0^{[K]}`) give `r^{−2}A_r^{rej} ≤ C r^{−2}(r³/k)P^Ne^{−c(b²+k²)} = C(r⁴/ℓ)(…)`, which integrates to
`≤ Cr_1⁵/(5ℓ) = Cℓ^{1/4}/5` — this is [C7-K] §4's first piece in the `r` variable. On `r_1 < r ≤ ρ`: `1 − e ≤ 1` and (W.1)
as in the proof of (W.2) give `≤ C(ℓ^{1/4} + ρ³)`. ∎

*Proof of (W.4).* By #191 §2 (the pointwise limit), `r^{d−1}Ψ_0(b, ru) = r^{−2}A_r(b, 0, u)` ((Z2) at `y = ru`, the `k = 0`
member of the pinned family: the pin Jacobian `12r^{−(d+3)}`, the polar factor `r^{d−1}`, the determinant scale `r²`),
and (W.1) at `k = 0` with (R5) gives `A_r(b, 0, u) ≤ Cr⁴(1 + |b|)^Ne^{−cb²}`; so
`∫_{0<dist<ρ}∫Ψ_0 = ∫_0^ρ∫∫ r^{−2}A_r(b, 0, u) ≤ C∫_0^ρ r² dr = Cρ³/3`. ∎

(Lemma W (W.1) does not use Step 4 of Lemma E; it needs the sign structure of the typed weight, which is exact, and
the expansions (3.1), which are Steps 1–3. The window `|rY| ≤ 6k|Δ| + O(r²)` is where the typed weight lives at
small `k`: for `k = 0` both endpoint determinants are `rY + O(r²)` with the same `rY`, so a max/saddle pair can only
be typed when `|Y| = O(r)` — this is the observation of the referee pass on v1, made rigorous. (W.2), by contrast,
needs (E.1) on `r < ℓ^{1/4}`: (W.1) alone gives `∫_0 r^{−2}k² dr = ∞`, and [R] (R11) alone gives only `O(1)`.)

## 4. Proof of Theorem R++

Fix `0 < ρ ≤ r_0^*` and `0 < ℓ ≤ 1`. Splitting the elder density by the separation of the pair,
`dist(M, S) ∈ (0, ρ) ∪ [ρ, r_0^*) ∪ [r_0^*, diam X]` (the boundaries are Lebesgue-null in the pair variables), and using
`ν_eld^{near,ρ} = ν_cand^{near,ρ} − ρ_rej^{near,ρ}` (the definition of the rejected density on the near range,
[C7-K] §§0, 4),

    ν_eld(ℓ) − cℓ^{−1/3} = [ν_cand^{near,ρ}(ℓ) − cℓ^{−1/3}] − ρ_rej^{near,ρ}(ℓ) + ν_eld^{[ρ,r_0^*)}(ℓ) + ν_eld^{far,r_0^*}(ℓ).   (4.1)

The four terms:

(i) `|ν_cand^{near,ρ}(ℓ) − cℓ^{−1/3}| ≤ C(min(ℓ^{1/4}, ρ) + ρ³ + ℓ²ρ^{−7})` — (W.2). (Without Lemma W, #191 (R+.3) gives
    `C(ρ + ℓ²ρ^{−7})`, stated there "for every `r_0 ∈ (0, r_0^*]`"; that its `C` depends on `d, L` only — the point
    needed since `ρ` tends to `0` with `ℓ` — is read off its proof, #191 §2, *Domination*, quoted:
    "`|r^{−2}(A_r − A_0)(b, ℓ/r³, u)| ≤ H(b, ℓ/r³) ≤ Ce^{−cb²}`, an integrable majorant on `(0, r_0) × R × S^{d−1}`
    independent of `ℓ`", and "the second term of (2.1) is at most `∫_{r_0}^∞ r^{−2}(ℓ/r³)²H ≤ Cℓ²r_0^{−7}`". The proof
    of (W.2) uses exactly these two displays on the ranges `r < r_1` and `r ≥ ρ`.)

(ii) `0 ≤ ρ_rej^{near,ρ}(ℓ) ≤ C(ℓ^{1/4} + ρ³)` — (W.3). (Without Lemma W, [C7-K] §4 — the proof of (T1) with the cutoff
    `r_0` replaced by `ρ ≤ r_0^{[K]}`, verbatim: the range `k ≥ k_* = ℓ^{1/4}` gives `Cℓ^{1/4}` by (K2), the range
    `ℓ/ρ³ ≤ k < k_*` gives `Cℓ^{1/4} + 3Cρ` by (K1) — gives `C(ℓ^{1/4} + ρ)`; #191 Remark 2 records the same reading.)

(iii) `0 ≤ ν_eld^{[ρ,r_0^*)}(ℓ) ≤ Cℓ^{1/3}(ρ^{−1} + ℓρ^{−5})` — Lemma B (B.2) with `r_0 = r_0^* ≤ r_0^{[R]}`.

(iv) `0 ≤ ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{1/3}` — Lemma F′ at `r_0 = r_0^*`.

Now choose `ρ = ℓ^{1/12}` and `ℓ_0 := min{1, (r_0^*)^{12}}`, so that `ρ ≤ r_0^*` for `ℓ ≤ ℓ_0`. Then `min(ℓ^{1/4}, ρ) =
ℓ^{1/4}`, `ρ³ = ℓ^{1/4}`, `ℓ²ρ^{−7} = ℓ^{17/12}`, `ℓ^{1/3}ρ^{−1} = ℓ^{1/4}`, `ℓ^{4/3}ρ^{−5} = ℓ^{11/12}`, and (4.1) with (i)–(iv)
(eight terms, five of them `ℓ^{1/4}`) gives

    |ν_eld(ℓ) − cℓ^{−1/3}| ≤ C(ℓ^{1/4} + ℓ^{1/4} + ℓ^{17/12} + ℓ^{1/4} + ℓ^{1/4} + ℓ^{1/4} + ℓ^{11/12} + ℓ^{1/3}) ≤ 8C ℓ^{1/4},   0 < ℓ ≤ ℓ_0,

which is (0.1); dividing by `cℓ^{−1/3}` (`c > 0`, [P] (15.2)) gives (0.2). ∎

(With the v1 inputs — (R+.3) and [C7-K] §4 in place of (W.2)–(W.3) — the same assembly at `ρ = ℓ^{1/6}` gives the
ledger `ℓ^{1/6} + ℓ^{5/6} + ℓ^{1/4} + ℓ^{1/6} + ℓ^{1/6} + ℓ^{1/2} + ℓ^{1/3}`, i.e. the rate `ℓ^{1/6}` of v1; checker E1 keeps
both ledgers.)

## 5. Remarks

1. **What fixes the exponent, and whether it is sharp.** In (4.1) with (W.2)–(W.3) the leading `ρ`-dependence is `ρ³`
   (the candidate excess and the rejected mass at separations in `(ℓ^{1/4}, ρ)`, both `O(r²)` per unit separation by
   Lemma W) against `ℓ^{1/3}ρ^{−1}` (Lemma B above `ρ`); the balance is `ρ = ℓ^{1/12}`, where both equal `ℓ^{1/4}`. But
   `ℓ^{1/4}` also appears three times *independently of `ρ`*, all from the transition `r = k` at separation `ℓ^{1/4}`
   where the pinned pair stops being a "cap" pair: the (E.1) excess `C min(ℓ^{1/4}, ρ)` below `ℓ^{1/4}`, the (K2) loss at
   `r ≤ k` ([C7-K] §4's first piece), and the tail `∫_{r > ℓ^{1/4}} r^{−2}k²` of the leading law `A_0 ≍ k²`. So within this
   ledger `1/4` is optimal (checker E1), trivially: the ledger has `ρ`-free `ℓ^{1/4}` terms. Whether `1/4` is the true
   order is **open**; the second referee pass on this note gave a formal leading-order computation (not proved,
   recorded here as a route) indicating that it is, with a *negative* coefficient: at `k = κr` (the cusp scale
   `r ≍ k ≍ ℓ^{1/4}`), (3.1) gives `det K_{M,S} = r(Y ∓ 6κΔ) + O(r²)`, so to leading order the typed event is
   `{A_0 < 0, |Y| < 6κ|Δ|}` (verified exactly on 160 pinned sextics in `d = 2` by the referee) and on it
   `W_r/r² = r²(36κ²Δ² − Y²) + O(r³) < 36k²Δ²`: the candidate kernel sits strictly *below* the contact kernel throughout
   the cusp scale, and integrating over `s = rℓ^{−1/4}` gives a contribution `I^{cand}ℓ^{1/4}` with
   `I^{cand} = −(96/7)·6^{1/4}∫∫ π_0(v_0(b, 0)) E_0[|Y_0|^{7/4}|det A_0|^{1/4}1{A_0 < 0}] dσ db < 0`, while the rejected part
   at `κ ≍ 1` is `O(1)` so `I^{eld} ≤ I^{cand}`. Unless elder mass at separations `ℓ^{1/4} ≪ r ≲ ℓ^{1/12}` (which the ledger
   only bounds by `ℓ^{1/4}`) compensates at that order, `ν_eld(ℓ) = cℓ^{−1/3} + I^{eld}ℓ^{1/4} + o(ℓ^{1/4})` with
   `I^{eld} < 0` would be the next term — the contact law *overcounts* at `k < r`, where `|A_r − A_0| ≍ k²`
   (Lemma W's window makes `A_r = o(k²) + O(r⁴)` as `(r, k/r) → 0`, against `A_0 ≥ c(b)k²`), so no `k < r` refinement of
   Lemma E of the form `O(k²r² + r⁴)` can exist, and the "k²-tail" is not an artifact of the bounds. Nothing about
   this is claimed. What *would* sharpen Lemma B (the spectral refinement of Math- #187 §3 in the near regime, which
   needs a lower bound on the conditional variance of the axial curvature under the pins — a routine extension of
   [P] §3 / [R] (R13) with `f_xxxx(0)` appended to `U_r`) would not touch the three `ρ`-free `ℓ^{1/4}` terms. Note
   finally that at separations `s ≲ ℓ^{1/4}` the elder intensity is *not* small — it carries the leading law
   `cℓ^{−1/3}` itself; and that (0.1) does not use Theorem Z (Z4), so (0.1) with (R+.1) re-derives (Z4) independently.
2. **Consistency.** (0.1) implies (R+.2) of #191 (`ν_eld = cℓ^{−1/3} + o(1)`) and is consistent with Theorem R
   ((R1): `|ν_eld − cℓ^{−1/3}| ≤ C`), with [C7-K] (T1)–(T2) (`ρ_rej = Θ(1)`: `ν_cand − cℓ^{−1/3} = ρ_rej + O(ℓ^{1/4})` is
   `Θ(1)`), with Theorem Z (Z4) and (R+.1) (`ν_cand − cℓ^{−1/3} → B_{d,L}`), with [Z] (Z18) (rejected mass below
   separation `δ` is `≤ Cδ`; (W.3)–(W.4) give `C(ℓ^{1/4} + δ³)` and `Cδ³` for the limit), and with #187 (Theorem F,
   `ℓ^{2/3}` for the far elder density, sharper than (F′.1)) and #188 (`ℓ^N`). It supersedes #191 Remark 2's conditional
   route: no far-elder rate with a polynomial `ρ`-dependence is needed, because the near-regime Lemma B (whose
   constants are those of [R] (R4)–(R5), uniform in `r ≤ r_0^{[R]}`) covers the separations down to `ρ = ℓ^{1/12}`,
   and the far part is taken at the fixed radius `r_0^*`. (W.4) also says that the equal-height kernel's radial
   density `r^{d−1}Ψ_0(b, ru)` is `O(r²)` near the diagonal, which supersedes #191 Remark 1's "`O(1)` per unit
   separation" there; [Z] itself proves only that there is no diagonal atom and (Z18)'s `Cδ`, and the picture of
   `B_{d,L}` as a macroscopic-separation mass is [C7-K] §4's remark, with which (W.4) agrees.
3. **For the manuscript.** Once #191 (Lemma E) and this note both have nonauthor ACCEPTs, Abstract / Theorem 2.1 /
   §3.8 can state, for the pointwise Kac–Rice representative that supplement C.4 fixes,
   `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3}(1 + O(ℓ^{7/12}))`, i.e. `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3} + O(ℓ^{1/4})`, in place of
   `(1 + o(1))`. Until then E10 of the V3 edit pack (`(1 + O(ℓ^{1/3}))`, resting on Theorem R with two reads, `[R·2P]`)
   is the safe statement, and E12 (`(1 + o(ℓ^{1/3}))`, #191 at candidate status) would be strengthened by this
   note, also at candidate status. The candidate density keeps `c_{3,24}ℓ^{−1/3} + B_{3,24} + o(1)` without a rate.
4. **Inputs by status.** Merged and reviewed: [R] (xAI R1–R6; Anthropic full depth #186 integrated), [C7-K] (one
   reviewing provider), [Z] (Anthropic A/B/C reads), [P]/[E1]/[E2]/[REC]. Merged with a caveat: [182] (OpenAI;
   integrated `2a10ed3`) — its §3 barrier was accepted at Slice A by this same author and session and by no other
   provider, so reviewers should treat §1's re-proof of (1.1) as new material. Unmerged, consumed: #191 — (R+.3),
   all of Lemma E ((E.1) in (W.2); Steps 1–3 in (3.1)), §2 ((2.1), the domination, the `k = 0` identity) — this
   note stands or falls with Lemma E of #191 (one nonauthor read, xAI, findings applied, no ACCEPT yet). Unmerged,
   cited only: #187, #188.

## 6. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | §§2, 4, 6–7: (R3)–(R5), the scaling dictionary and the block determinant bound `F_j(K_i) ≤ C(k + r)T^d`, (R8)–(R9), the near/far decomposition — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K1), (K2), §4 (the rejected intensity identity; the proof of (T1) with cutoff `ρ`) — consumed |
| [182] | `frontiers/fixed_r_inverse_lifetime_20260930/PROOF.md` (blob `0d401877`) | §3 (8)–(9), the deterministic barrier — consumed (re-proved in §1) |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | §1 notation, §2 (Z10) regression at fixed sites, (Z13)–(Z14), (Z16) — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 distinct-site rank, §4 regression, §8 maximin and elder mark, §§9–10 as [E2], §14, (15.2) — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement: regular conditional law, Borel marks, (9.1) |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | reading rule, consumption contract |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (unmerged; v1.1 blob `441152df`, head `abae6d0`) | Theorem R+ (R+.3) and its §2 (domination, pointwise limit, (2.1)); Lemma E ((E.1) and Steps 1–3: (1.1), (1.3), (1.5), the structural display after (1.6)); the admissible radius `r_0^*` — **consumed, unmerged** |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (unmerged) | Theorem F (`ℓ^{2/3}` far rate, sharper than (F′.1)) and §4 — cited only (Lemma F′ and Remarks 1–2) |
| #188 | `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | `ℓ^N` far rate — cited only (Remark 2) |

## 7. Exact controls (`rate_ledger_check.py`; stdlib; exact rationals; byte-identical under `-O`)

E1 the exponent ledgers of §4: with `ρ = ℓ^θ` the v1.1 terms have exponents `1/4, 3θ, 2 − 7θ, 1/4, 3θ, 1/3 − θ,
4/3 − 5θ, 1/3` and the v1 terms `θ, 2 − 7θ, 1/4, θ, 1/3 − θ, 4/3 − 5θ, 1/3`; at `θ = 1/12` (v1.1) and `θ = 1/6` (v1) the
minima are `1/4` and `1/6`; over a fine rational grid of `θ ∈ (0, 1/3)` and at every breakpoint neither minimum exceeds
its value (optimality within each ledger); and at rational twelfth powers `ℓ = q^{12}` each term is `≤ ℓ^{1/4}`
(resp. `ℓ^{1/6}`) exactly. Mutant M1 (claims the rate `1/3` for v1.1) fails: the ledger's minimum is `1/4` at every `θ`.
E2 the barrier arithmetic of [182] (8)–(9): for rational `0 < λ ≤ K` and `t ≤ a_Lλ/K`, `(K/6)t³ ≤ (λ/6)t²` and
`b − (λ/2)t² + (K/6)t³ ≤ b − (λ/3)t²` exactly; `b − d ≥ c_Lλ³/K² ⇔ λ ≤ ((b − d)K²/c_L)^{1/3}` at rational cubes.
Mutant M2 (radius `2λ/K`) fails.
E3 the determinant/soft-eigenvalue inequality (1.3): for rational symmetric positive definite matrices
`O diag(λ)Oᵀ` with rational orthogonal `O` (Cayley transforms of rational skew matrices), `det ≤ λ_min λ_max^{d−1}`
and `λ_max ≤ ‖·‖_F`; mutant M3 (exponent `d − 2`) fails.
E4 the integrals and the cutoff ledger: `∫_ρ^{r_0}(ℓr^{−6} + r^{−2})dr = ℓ(ρ^{−5} − r_0^{−5})/5 + ρ^{−1} − r_0^{−1} ≤ ℓρ^{−5}/5 + ρ^{−1}`
exactly at rationals; [C7-K] §4's second piece `ℓ^{−1/3}·ℓ^{2/3}·3(ℓ/ρ³)^{−1/3} = 3ρ` and first piece
`ℓ^{−1/3}(3/5)ℓk_*^{−5/3} = (3/5)ℓ^{1/4}` at `k_* = ℓ^{1/4}`, at rational twelfth powers; the (W.2)–(W.3) integrals
`∫_{r_1}^ρ(ℓ²r^{−8} + r²)dr ≤ ℓ²r_1^{−7}/7 + ρ³/3` and `∫_0^{r_1} r⁴/ℓ dr = r_1⁵/(5ℓ) = ℓ^{1/4}/5` at `r_1 = ℓ^{1/4}`.
E5 the sign window of Lemma W: for rational `(k, D, Y, R_M, R_S, r)` on a grid including `k = 0`, whenever
`(rY − 6kD + R_M)(rY + 6kD + R_S) < 0` (the typed sign pattern) one has `|rY| ≤ 6k|D| + max(|R_M|, |R_S|)` and both
`|det K_i| ≤ 12k|D| + 2 max(|R_M|, |R_S|)`, exactly; the bound is sharp (approached as `rY → ±6kD` with `R_M = R_S = 0`,
where the product tends to `0` from below); and it is *not* implied without the sign condition (same-sign instances
violate it). Mutant M4 (drops the factor `2` on the remainder) fails.
Mutants `M1`–`M4` exit 1; an unknown label exits 2.

**What the controls do not test.** They check exponent bookkeeping, the barrier's algebra, a linear-algebra
inequality and the sign-window inequality at rational points. They do not test Lemma B, Lemma F′ or Lemma W as
statements about the Gaussian laws (the expansions (3.1) imported from #191, the moment imports (R4)/(R9)/(2.2), the
density bound (R5), the Kac–Rice disintegrations) nor the assembly's use of #191 and [C7-K] — those are prose only,
and they are the review. The controls are not acceptance.

## 8. Review slices

A: Lemma B — the use of the elder mark's definition and of [182] (9), the determinant bound (1.3), the block bound
   for `K_S`, the moment imports, and (B.2)'s integration; the identity behind (B.2).
B: Lemma F′ — the uniform far facts (a), (b), (2.2), and the barrier at `0`.
C: Lemma W and (W.2)–(W.4) — the expansions (3.1) against #191 Lemma E Steps 1–3 (in particular the remainder bound
   `Cr²(1 + k)T^{N_1}`), the sign window, the moments, and the three integrations.
D: §4 — the decomposition (4.1), the four inputs with their exact provenance, the choice `ρ = ℓ^{1/12}`, the scope
   and Remarks 1–4.
