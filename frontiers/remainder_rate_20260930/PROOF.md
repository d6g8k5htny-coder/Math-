# The remainder of Theorem R has a rate: `ν_eld(ℓ) = cℓ^{−1/3} + O(ℓ^{1/6})`

Object: CL-D2-REMAINDER-RATE-20260930-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 30 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register,
graph, STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is claimed. Same GitHub account as
every lane; zero organizational independence. **Dependency:** this note consumes Theorem R+ (R+.3) of Math- #191
(`frontiers/remainder_vanishing_20260930/PROOF.md`, v1.1, blob `441152df`; an unmerged author-side candidate of
this session with one nonauthor read, xAI 5369140697, findings applied). It cannot be integrated before #191 and
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

    |ν_eld(ℓ) − c ℓ^{−1/3}| ≤ C ℓ^{1/6},        0 < ℓ ≤ ℓ_0;                                              (0.1)

equivalently

    ν_eld(ℓ) = c ℓ^{−1/3} (1 + O(ℓ^{1/2}))        as ℓ ↓ 0.                                              (0.2)

The proof has two new estimates, both elementary consequences of the deterministic barrier of [182] §3:

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
bottleneck of the ledger in §3.)

**What is not claimed.** No sharpness of the exponent `1/6` (§4 explains what fixes it and that it is not expected
to be the true order); no numerical `C`, `ℓ_0`; no rate for the *candidate* remainder (`ν_cand = cℓ^{−1/3} + B_{d,L}
+ o(1)` of #191 stays without a rate: the far candidate kernel's dependence on `ℓ` is not quantified anywhere);
no rate for `ρ_rej(ℓ) → B_{d,L}` (Theorem Z); no uniformity in `d`, `L`; no finite-radius band; no RN / 24-jet
closure; nothing beyond the existential scope of Theorem R, Theorem R+ and [C7-K].

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

## 3. Proof of Theorem R++

Fix `0 < ρ ≤ r_0^*` and `0 < ℓ ≤ 1`. Splitting the elder density by the separation of the pair,
`dist(M, S) ∈ (0, ρ) ∪ [ρ, r_0^*) ∪ [r_0^*, diam X]` (the boundaries are Lebesgue-null in the pair variables), and using
`ν_eld^{near,ρ} = ν_cand^{near,ρ} − ρ_rej^{near,ρ}` (the definition of the rejected density on the near range,
[C7-K] §§0, 4),

    ν_eld(ℓ) − cℓ^{−1/3} = [ν_cand^{near,ρ}(ℓ) − cℓ^{−1/3}] − ρ_rej^{near,ρ}(ℓ) + ν_eld^{[ρ,r_0^*)}(ℓ) + ν_eld^{far,r_0^*}(ℓ).   (3.1)

The four terms:

(i) `|ν_cand^{near,ρ}(ℓ) − cℓ^{−1/3}| ≤ C(ρ + ℓ²ρ^{−7})` — #191, Theorem R+ (R+.3), stated there "for every
    `r_0 ∈ (0, r_0^*]`". That its `C` depends on `d, L` only — the point needed here, since `ρ` will tend to `0` with
    `ℓ` — is read off its proof (#191 §2, *Domination*, quoted): "`|r^{−2}(A_r − A_0)(b, ℓ/r³, u)| ≤ H(b, ℓ/r³) ≤ Ce^{−cb²}`,
    an integrable majorant on `(0, r_0) × R × S^{d−1}` independent of `ℓ`" — so the near term is at most
    `ρ·|S^{d−1}|·∫_R Ce^{−cb²}db` with `C, c` those of Lemma E's `H`, i.e. of `d, L` — and "the second term of (2.1)
    is at most `∫_{r_0}^∞ r^{−2}(ℓ/r³)²H ≤ Cℓ²r_0^{−7}`".

(ii) `0 ≤ ρ_rej^{near,ρ}(ℓ) ≤ C(ℓ^{1/4} + ρ)` — [C7-K] §4, the proof of (T1) with the cutoff `r_0` replaced by
    `ρ ≤ r_0^{[K]}` (verbatim: the range `k ≥ k_* = ℓ^{1/4}` gives `Cℓ^{1/4}` by (K2), the range `ℓ/ρ³ ≤ k < k_*`
    gives `Cℓ^{1/4} + 3Cρ` by (K1); #191 Remark 2 records the same reading).

(iii) `0 ≤ ν_eld^{[ρ,r_0^*)}(ℓ) ≤ Cℓ^{1/3}(ρ^{−1} + ℓρ^{−5})` — Lemma B (B.2) with `r_0 = r_0^* ≤ r_0^{[R]}`.

(iv) `0 ≤ ν_eld^{far,r_0^*}(ℓ) ≤ Cℓ^{1/3}` — Lemma F′ at `r_0 = r_0^*`.

Now choose `ρ = ℓ^{1/6}` and `ℓ_0 := min{1, (r_0^*)^6}`, so that `ρ ≤ r_0^*` for `ℓ ≤ ℓ_0`. Then
`ℓ²ρ^{−7} = ℓ^{5/6}`, `ℓ^{1/3}ρ^{−1} = ℓ^{1/6}`, `ℓ^{4/3}ρ^{−5} = ℓ^{1/2}`, and (3.1) with (i)–(iv) gives

    |ν_eld(ℓ) − cℓ^{−1/3}| ≤ C(ℓ^{1/6} + ℓ^{5/6} + ℓ^{1/4} + ℓ^{1/6} + ℓ^{1/6} + ℓ^{1/2} + ℓ^{1/3}) ≤ 7C ℓ^{1/6},   0 < ℓ ≤ ℓ_0,

which is (0.1); dividing by `cℓ^{−1/3}` (`c > 0`, [P] (15.2)) gives (0.2). ∎

## 4. Remarks

1. **What fixes the exponent.** In (3.1) the terms `Cρ` of (i) and (ii) bound the candidate excess over the contact
   law below separation `ρ` and the rejected mass below `ρ`; they cancel in the difference `ν_eld^{near,ρ} − cℓ^{−1/3}`,
   which the argument does not track. Whether they are of true order `ρ` is not known: both come from the crude
   majorants `(k + r)²` of [C7-K] (K1) and `r²H` of Lemma E at `k < r`, and #191 §2 states that no near-diagonal
   lower bound on the equal-height kernel is supplied. Against them stands the barrier bound `Cℓ^{1/3}ρ^{−1}` for the
   elder mass at separations above `ρ`; (B.1) improves on (K1) exactly when `k < r³`, i.e. `r > ℓ^{1/6}`. The balance
   `ρ = ℓ^{1/3}/ρ` is `ρ = ℓ^{1/6}`, and the remaining terms (`ℓ^{1/4}` from (K2), `ℓ²ρ^{−7} = ℓ^{5/6}`,
   `ℓ^{4/3}ρ^{−5} = ℓ^{1/2}`, `ℓ^{1/3}` far) are all smaller there. Within this ledger `1/6` is optimal (checker E1):
   any rate `γ` needs `ρ ≤ ℓ^γ` and `ℓ^{1/3}ρ^{−1} ≤ ℓ^γ`, i.e. `γ ≤ 1/6`. Two routes past it, neither taken here:
   (a) a sharper near majorant at `k < r` — the referee pass on this note observed, symbolically on the pinned
   quintic, that at `k = 0` both endpoint determinants equal `Yr² + O(r³)` with the *same* `Y`, so the typed weight
   (opposite signs) lives on a window `|Y| ≲ r` and `E_Q[W_r/r²]` at small `k` is heuristically `O(k²·min(1, k/r) + r⁴)`
   rather than `(k + r)²`; if proved, (i)–(ii) would become `O(ℓ^{1/4} + ρ³)` and, with (B.1) unchanged and
   `ρ = ℓ^{1/12}`, the rate `ℓ^{1/4}` (heuristic, not claimed); (b) a sharper near elder bound than (B.1), which uses
   the soft-maximum barrier only through the determinant weight and nothing about the smallness of the barrier
   event's probability — the spectral refinement of Math- #187 §3 transplanted to the near regime, which needs a
   lower bound on the conditional variance of the axial curvature under the pins (the direction `(α_M + α_S)/2`,
   of conditional size `≍ r`; the Gaussian input is a routine extension of [P] §3 / [R] (R13) with `f_xxxx(0)`
   appended to `U_r` — what is missing is the analysis, not the Gaussian fact). The true order of `ν_eld − cℓ^{−1/3}`
   is expected to be smaller than `ℓ^{1/6}` (Theorem R's first-order contact monomial `ℓ^{1/3}` vanishes by Lemma E;
   at fixed macroscopic separations the elder mass is expected to decay faster than any power, #187 §4, #188);
   nothing about it is claimed, and note that at separations `s ≲ ℓ^{1/4}` the elder intensity is *not* small — it
   carries the leading law `cℓ^{−1/3}` itself.
2. **Consistency.** (0.1) implies (R+.2) of #191 (`ν_eld = cℓ^{−1/3} + o(1)`) and is consistent with Theorem R
   ((R1): `|ν_eld − cℓ^{−1/3}| ≤ C`), with [C7-K] (T1)–(T2) (`ρ_rej = Θ(1)`: `ν_cand − cℓ^{−1/3} = ρ_rej + O(ℓ^{1/6})` is
   `Θ(1)`), with Theorem Z (Z4) and (R+.1) (`ν_cand − cℓ^{−1/3} → B_{d,L}`), and with #187 (Theorem F, `ℓ^{2/3}` for the
   far elder density, sharper than (F′.1)) and #188 (`ℓ^N`). It supersedes #191 Remark 2's conditional route: no
   far-elder rate with a polynomial `ρ`-dependence is needed, because the near-regime Lemma B (whose constants
   are those of [R] (R4)–(R5), uniform in `r ≤ r_0^{[R]}`) covers the separations down to `ρ = ℓ^{1/6}`, and the far
   part is taken at the fixed radius `r_0^*`.
3. **For the manuscript.** Once #191 (Lemma E) and this note both have nonauthor ACCEPTs, Abstract / Theorem 2.1 /
   §3.8 can state, for the pointwise Kac–Rice representative that supplement C.4 fixes,
   `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3}(1 + O(ℓ^{1/2}))`, i.e. `ν_{3,24}(ℓ) = c_{3,24}ℓ^{−1/3} + O(ℓ^{1/6})`, in place of
   `(1 + o(1))`. Until then E10 of the V3 edit pack (`(1 + O(ℓ^{1/3}))`, resting on Theorem R with two reads, `[R·2P]`)
   is the safe statement, and E12 (`(1 + o(ℓ^{1/3}))`, #191 at candidate status) would be strengthened by this
   note, also at candidate status. The candidate density keeps `c_{3,24}ℓ^{−1/3} + B_{3,24} + o(1)` without a rate.
4. **Inputs by status.** Merged and reviewed: [R] (xAI R1–R6; Anthropic full depth #186 integrated), [C7-K] (one
   reviewing provider), [Z] (Anthropic A/B/C reads), [P]/[E1]/[E2]/[REC]. Merged with a caveat: [182] (OpenAI;
   integrated `2a10ed3`) — its §3 barrier was accepted at Slice A by this same author and session and by no other
   provider, so reviewers should treat §1's re-proof of (1.1) as new material. Unmerged, consumed: #191 (R+.3) —
   this note stands or falls with Lemma E of #191 (one nonauthor read, xAI, findings applied, no ACCEPT yet).
   Unmerged, cited only: #187, #188.

## 5. Sources (exact identities in `SOURCES.json`)

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
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (unmerged; v1.1 blob `441152df`, head `abae6d0`) | Theorem R+ (R+.3), Lemma E, the admissible radius `r_0^*`, (2.1) — **consumed, unmerged** |
| #187 | `frontiers/far_elder_rate_20260930/PROOF.md` (unmerged) | Theorem F (`ℓ^{2/3}` far rate, sharper than (F′.1)) and §4 — cited only (Lemma F′ and Remarks 1–2) |
| #188 | `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | `ℓ^N` far rate — cited only (Remark 2) |

## 6. Exact controls (`rate_ledger_check.py`; stdlib; exact rationals; byte-identical under `-O`)

E1 the exponent ledger of §3: with `ρ = ℓ^θ` the seven terms have exponents `θ, 2 − 7θ, 1/4, θ, 1/3 − θ, 4/3 − 5θ, 1/3`;
at `θ = 1/6` their minimum is `1/6`; over a fine rational grid of `θ ∈ (0, 1/3)` and at every breakpoint the
minimum never exceeds `1/6` (optimality within the ledger); and at rational twelfth powers `ℓ = q^{12}` each term
is `≤ ℓ^{1/6}` exactly. Mutant M1 (claims the rate `1/4`) fails: at `θ = 1/4` the ledger gives `1/12`.
E2 the barrier arithmetic of [182] (8)–(9): for rational `0 < λ ≤ K` and `t ≤ a_Lλ/K`, `(K/6)t³ ≤ (λ/6)t²` and
`b − (λ/2)t² + (K/6)t³ ≤ b − (λ/3)t²` exactly; `b − d ≥ c_Lλ³/K² ⇔ λ ≤ ((b − d)K²/c_L)^{1/3}` at rational cubes.
Mutant M2 (radius `2λ/K`) fails.
E3 the determinant/soft-eigenvalue inequality (1.3): for rational symmetric positive definite matrices
`O diag(λ)Oᵀ` with rational orthogonal `O` (Cayley transforms of rational skew matrices), `det ≤ λ_min λ_max^{d−1}`
and `λ_max ≤ ‖·‖_F`; mutant M3 (exponent `d − 2`) fails.
E4 the integrals and the cutoff ledger: `∫_ρ^{r_0}(ℓr^{−6} + r^{−2})dr = ℓ(ρ^{−5} − r_0^{−5})/5 + ρ^{−1} − r_0^{−1} ≤ ℓρ^{−5}/5 + ρ^{−1}`
exactly at rationals; [C7-K] §4's second piece `ℓ^{−1/3}·ℓ^{2/3}·3(ℓ/ρ³)^{−1/3} = 3ρ` and first piece
`ℓ^{−1/3}(3/5)ℓk_*^{−5/3} = (3/5)ℓ^{1/4}` at `k_* = ℓ^{1/4}`, at rational twelfth powers.
Mutants `M1`–`M3` exit 1; an unknown label exits 2.

**What the controls do not test.** They check exponent bookkeeping, the barrier's algebra and the linear-algebra
inequality at rational points. They do not test Lemma B or Lemma F′ as statements about the Gaussian laws (the
moment imports (R4)/(R9)/(2.2), the density bound (R5), the Kac–Rice disintegrations) nor the assembly's use of
#191 (R+.3) and [C7-K] §4 — those are prose only, and they are the review. The controls are not acceptance.

## 7. Review slices

A: Lemma B — the use of the elder mark's definition and of [182] (9), the determinant bound (1.3), the block bound
   for `K_S`, the moment imports, and (B.2)'s integration; the identity behind (B.2).
B: Lemma F′ — the uniform far facts (a), (b), (2.2), and the barrier at `0`.
C: §3 — the decomposition (3.1), the four inputs with their exact provenance (in particular (R+.3) of #191 at
   `ρ → 0` and [C7-K] §4 at cutoff `ρ`), the choice `ρ = ℓ^{1/6}`, the scope and Remarks 1–4.
