# The equal-height mass `B_{d,L}`: a volume law and its value for the SIDE24 field

Object: CL-EQUAL-HEIGHT-MASS-20261001-v1.2.1.
- v1.2.1 (4 October 2026) applies Grok Bot agent 15's read of the v1.2 status lines (5976336060; AMEND, wording only).
  It changes no statement, proof, number or control. The changed bytes are listed at the end of §6.
- v1.2 (2 October 2026) is a status update. It changes no statement, proof, number or control.
  - Math- #191 and #207 are now merged.
  - The merged #218 (Theorem T) and #229 (Theorem T⁺) give the candidate density with this `B_{d,L}` as its constant
    term, with rates, at their stated scope. Both are author-side proof candidates with scoped, conditional nonauthor
    reviews.
  - The merged #229, Proposition W⁺, proves the upper bound in the near-diagonal heuristic of §2, up to a factor
    `log(2/r)`, for the torus kernel. It is an author-side proof candidate. Codex's PASS_TECHNICAL / ACCEPT_SCOPED
    5381412814 is conditional on its imported interfaces.
  - Codex's Slice A review (5379568217) is a scoped analytic ACCEPT of Proposition V at v1.1, NOTE blob `ed0d3fa8`,
    with the consumed [P], [R] and [Z] interfaces as hypotheses. v1.2 does not touch Proposition V or its proof.
- v1.1 (v1 → v1.1 after Codex P1 4151471466: the near part now has the same
quantified rate as the far part — Step 5 rewritten through a uniformly nondegenerate rescaled jet vector — and the SIDE24
value is stated with its exact status; Codex P2 4151471472: the Monte Carlo sample count is validated).
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Disposition: AUTHOR-SIDE CANDIDATE (Proposition V) and EXPLORATION (the numbers); NONAUTHOR REVIEW REQUIRED.
Scientific effect: NONE — no register, graph, STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every
lane; zero organizational independence. Consumes merged sources only ([Z], [R], [P]). [C7-K] is cited only since v1.1
(§4: v1's Lemma N, superseded by Step 5). Math- #191 and #207 (merged since; v1.2) are cited for interpretation, not
used. v1 incorporated a clean-context referee pass (one gap — the uniformity
in `L` of the near-diagonal majorant — closed in v1 by a majorant, Lemma N, and in v1.1 by the quantitative Step 5;
minor points applied; `β_2`, `β_3` and `γ_3` independently recomputed).

## 0. Statement

**Setting.** [Z] (`frontiers/c7_zero_gap_limit_20260929/PROOF.md`, blob `5b6328ea`) for the [P] field on
`X_L = R^d/(LZ^d)`, whose covariance is the normalized periodized Gaussian kernel
`K_L(z) = Σ_{n∈Z^d} e^{−|z+Ln|²/2} / Σ_{n∈Z^d} e^{−|Ln|²/2}` (unit variance). Its equal-height mass is

    B_{d,L} = ∫_{X_L∖{0}} ∫_R Ψ_0^{(L)}(b, y) db dy,     Ψ_0(b, y) = p_y(v_{b,0}) E_{Q_{y,b,0}}[W],                     ((Z2)–(Z3))

`W = |det H_0 det H_y|1{H_0 < 0, index H_y = d − 1}`. By Theorem Z (Z4), `B_{d,L}` is the limit of the rejected density,
`ρ_rej(ℓ) → B_{d,L}`; by Math- #191 (R+.1) (merged), it is the constant term of the candidate density,
`ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + o(1)`. (v1.2: the merged #218 (Theorem T) and #229 (Theorem T⁺) give
`ν_cand = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{3/7})`, at their stated scope.) [Z] states that it gives "No numerical value for B_(d,L)".

Let `f_∞` be the stationary Gaussian field on `R^d` with covariance `e^{−|z|²/2}`, `ρ_j(b)` its height density of critical
points of index `j` (per unit volume and unit height) and `Ψ_0^∞(b, y)` its equal-height kernel ((Z2) on `R^d`).

**Proposition V (volume law).** There are `C, N, L₀` such that for `L ≥ L₀`

    B_{d,L} = β_d L^d + γ_d + ε_L,   |ε_L| ≤ C L^N e^{−L²/8},   β_d := ∫_R ρ_d(b) ρ_{d−1}(b) db,
                                            γ_d := ∫_{R^d}∫_R (Ψ_0^∞(b, y) − ρ_d(b)ρ_{d−1}(b)) db dy,          (V.1)

the last integral converging absolutely. (`C`, `N` are existential, as everywhere in the chain; they are not computed.)

**Values (exploration; not certified).** For the Gaussian kernel,

    β_2 = 3.122769186·10⁻³,   β_3 = 7.400614572·10⁻⁴      (deterministic quadrature; controls Q1–Q4 of equal_height_mass.py),
    γ_3 = −0.020 ± 0.002                                     (two Monte Carlo explorations, §2),

so `24³β_3 + γ_3 = 10.231 − 0.020 ≈ 10.21`, and **`B_{3,24} = 10.21 ± 0.002 + ε_{24}`** with `|ε_{24}| ≤ C·24^N e^{−72}`
(`e^{−72} ≈ 5·10⁻³²`; `C`, `N` not computed). That is about `244` times `c_{3,24} = 0.0417759318…` (the enclosure of
`coefficients/side24_v1`). **Status of this value:** exploration. `β_3` is deterministic (to `10⁻⁸`) and `γ_3` is Monte
Carlo; the remainder is proved exponentially small in `L²` but with unquantified constants. So `B_{3,24} ≈ 10.21` is the
value of the asymptotic formula at `L = 24`, not a certified enclosure.

**What is not claimed.** No numerical `C`, `N` in (V.1); no certified value of `γ_3` or `B_{3,24}`; nothing about
`B_{d,L}` for covariances other than the periodized Gaussian kernel; no change to Theorem Z.

## 1. Proof of Proposition V

For `y` in the fundamental cell `C_L = [−L/2, L/2)^d ∖ {0}` (the torus point identified with its representative), let
`Σ_L(y)` be the covariance matrix of the jet vector `J(y) = (O_y, H_0, H_y)` of `f_L` (`O_y = (f, ∇f)(0), (f, ∇f)(y)`, the
two Hessians), and `Σ_∞(y)` that of `f_∞`. Gaussian regression ([Z] §2, (Z10)) writes the kernel as a function of the
covariance:

    Ψ_0(b, y) = F(Σ(y); b),    F(Σ; b) := φ_{Σ_OO}(v_b) E[W(b m_Σ + S_Σ^{1/2}ζ)],  ζ ~ N(0, I),

`m_Σ = Σ_HOΣ_OO^{−1}e`, `S_Σ = Σ_HH − Σ_HOΣ_OO^{−1}Σ_OH`, `e = (1, 0, …, 0, 1, 0, …, 0)` (so `v_b = be`).

*Step 1 (Lipschitz dependence).* Let `𝒦_c` be the set of covariance matrices with eigenvalues in `[c, 1/c]`. On `𝒦_c`, the
maps `Σ ↦ m_Σ, S_Σ, S_Σ^{1/2}` are Lipschitz, and `|∂_Σ φ_{Σ_OO}(v_b)| ≤ C_c(1 + b²)e^{−c'b²}`. The function `W` is continuous and
piecewise polynomial of degree `2d` in the two Hessians, vanishing where an index changes, so
`|W(H) − W(H')| ≤ C(1 + |H| + |H'|)^{2d−1}|H − H'|` (on each factor this is [R] Lemma R3.1 (R6): along the segment from `H` to
`H'` an index change passes through a singular matrix). Hence `|F(Σ; b) − F(Σ'; b)| ≤ C_c‖Σ − Σ'‖(1 + |b|)^Ne^{−c'b²}` on `𝒦_c`.

*Step 2 (nondegeneracy away from the diagonal).* `Σ_∞(y)` is continuous in `y`, nondegenerate for every `y ≠ 0` (the
distinct-site jet rank of [P] §2 and [Z] §2 on `R^d`: a zero-variance combination of jets at `0` and `y` is a distribution
`T` with `∫|T̂(ξ)|²e^{−|ξ|²/2}dξ = 0`, so `T̂ ≡ 0` and `T = 0`), and tends to the
block-diagonal `diag(Σ₁, Σ₁)` as `|y| → ∞`, `Σ₁` the nondegenerate one-point jet covariance. So `Σ_∞(y) ∈ 𝒦_c` for
`|y| ≥ r₀`, with `c = c(r₀) > 0`.

*Step 3 (image terms).* Up to the normalization factor `(Σ_n e^{−|Ln|²/2})^{−1} = 1 + O(e^{−L²/2})`, every entry of
`Σ_L(y) − Σ_∞(y)` is a sum over `n ≠ 0` of derivatives of order at most four of `e^{−|z|²/2}` at points `z ∈ {Ln, ±y + Ln}`,
and `|±y + Ln| ≥ L|n|_∞ − |y|_∞ ≥ L|n|_∞/2` for `y ∈ C_L`. Hence
`‖Σ_L(y) − Σ_∞(y)‖ ≤ CL^Ne^{−L²/8}`, uniformly in `y ∈ C_L`. In particular `Σ_L(y) ∈ 𝒦_{c/2}` for `|y| ≥ r₀` and `L ≥ L₀`, and
the one-point densities satisfy `ρ_j^{(L)} = ρ_j + O(L^Ne^{−L²/2})`.

*Step 4 (far part).* For `y ∈ C_L`, `|y| ≥ r₀`, Steps 1–3 give `|Ψ_0^{(L)}(b, y) − Ψ_0^∞(b, y)| ≤ CL^Ne^{−L²/8}(1 + |b|)^Ne^{−c'b²}`.
The cross block of `Σ_∞(y)` consists of derivatives of `e^{−|y|²/2}` of order at most four, so
`‖Σ_∞(y) − diag(Σ₁, Σ₁)‖ ≤ C(1 + |y|)⁴e^{−|y|²/2}`. At the block-diagonal covariance the two sites are independent and
`F(diag(Σ₁, Σ₁); b) = ρ_d(b)ρ_{d−1}(b)`. Hence `|Ψ_0^∞(b, y) − ρ_dρ_{d−1}(b)| ≤ C(1 + |y|)⁴e^{−|y|²/2}(1 + |b|)^Ne^{−c'b²}`, which
is integrable over `{|y| ≥ r₀} × R`. Integrating over `C_L ∖ B_{r₀}` gives the far statement of Proposition V; the tail
`∫_{R^d∖C_L}` of the last integrand is `O(L^Ne^{−L²/8})`.

*Step 5 (near part, quantitative).* For `|y| < r₀` the jets at `0` and `y` degenerate as `y → 0`, so Step 1 does not
apply to `Σ(y)` directly. Rescale instead.

Write `y = ru` with `M = −ru/2`, `S = ru/2` after the translation of [R] §2. Form the vector `J̃(r, u)` of:
- the observation rows `U_r` of [R] §2: the averages and divided differences of `f` and `∇f` at the pins, ending in
  `U_3 = (6/r²)[f_x(M) + f_x(S) − 2(f(S) − f(M))/r]`;
- the rescaled Hessian combinations
  `[(f_xx(S) + f_xx(M))/2 − (f_x(S) − f_x(M))/r]/r²`, `[(f_xx(S) − f_xx(M))/r − U_3]/r²`,
  `[(f_xy_j(S) + f_xy_j(M))/2 − (f_y_j(S) − f_y_j(M))/r]/r²`, `(f_xy_j(S) − f_xy_j(M))/r`, `(A_S + A_M)/2`, `(A_S − A_M)/r`.

By Taylor's formula with integral remainder (centred rules), `J̃(r, u)` converges in `L²` as `r → 0`. Its limit is a
list of *distinct* partial derivatives at `0`, with nonzero coefficients:
- from the rows: `f, f_x, f_xx, f_xxx, f_y_j, f_xy_j`;
- from the Hessian combinations: `f_xxxx/12, f_xxxxx/60, f_xxxy_j/12, f_xxy_j, f_y_jy_l, f_xy_jy_l`.

That list is nondegenerate by the finite-jet rank of [P] §2 (on `R^d` by Step 2's Fourier argument). By continuity and
compactness, the covariance `Σ̃_L(r, u)` of `J̃` has eigenvalues in `[c, 1/c]` for `r ≤ r₀`, all frames and
`L ∈ [L₀, ∞]`. Its entries are divided differences of `K_L`, i.e. averages of derivatives of `K_L` over the segment, so
`‖Σ̃_L(r, u) − Σ̃_∞(r, u)‖ ≤ C‖K_L − K_∞‖_{C^q(B_{2r₀})} ≤ CL^Ne^{−L²/8}`.

**The kernel in rescaled variables.** On the event `U_r = v_r(b, 0)` (equal heights, `k = 0`), the scaled Hessians of
[R] §4 are affine in `J̃` with coefficients polynomial in `r`:
- `α_{M,S} = r(Ũ_a ∓ (r/2)Ũ_b)` (cf. #191 (1.1) at `k = 0`);
- `β_{M,S} = rŨ_c ∓ Ũ_d/2`;
- `A_{M,S} = Ũ_e ∓ (r/2)Ũ_f`.

So `det K_i = α_i det A_i − r β_iᵀadj(A_i)β_i` is `r` times a polynomial in `(J̃, r)`. Hence
`W̃ := W_r/r⁴ = |(det K_M/r)(det K_S/r)|1{typed}` is continuous and piecewise polynomial in `(J̃, r)`, and vanishes where
an index changes. By the separation-variable form of the kernel ([Z] (Z14); #191 (2.1)),

    r^{d−1}Ψ_0(b, ru) = r^{−2}A_r(b, 0, u) = 12 π_r(v_r(b, 0)) E_Q[W̃] = F̃(Σ̃(r, u); b),

with `F̃` of the same form as `F` in Step 1. Step 1's argument applies verbatim on the uniformly nondegenerate set and gives:
- `|r^{d−1}(Ψ_0^{(L)} − Ψ_0^∞)(b, ru)| ≤ CL^Ne^{−L²/8}(1 + |b|)^Ne^{−c'b²}`;
- `r^{d−1}Ψ_0^∞(b, ru) ≤ C(1 + |b|)^Ne^{−c'b²}`.

Integrating over `r < r₀`, `u` and `b`, the near parts for `L` and `∞` differ by `O(L^Ne^{−L²/8})`, and the near part of
`γ_d` converges absolutely. This replaces any appeal to the uniformity in `L` of [Z] (Z15), whose proof uses
whole-torus norms. (v1's Lemma N — the pointwise bound behind [C7-K] (K1) at `k = 0` with local seminorms — gave only a
majorant and hence `o(1)`.)

Adding the near and far parts, `B_{d,L} = β_dL^d + γ_d + O(L^Ne^{−L²/8})`. ∎

(The constants `C`, `N` come from compactness and continuity; quantifying them would turn `B_{3,24} ≈ 10.21` into an
enclosure, together with a certified `γ_3`.)

## 2. The numbers

*`β_d` (deterministic).* Given `f = b` and `∇f = 0`, the Hessian of `f_∞` is `−bI + G`. Here `G` has `Var G_ii = 2`,
`Cov(G_ii, G_jj) = 0` (`i ≠ j`), `Var G_ij = 1` (exact, Q1), i.e. a scaled GOE with density `∝ exp(−tr G²/4)`. Hence

    ρ_j(b) = φ(b)(2π)^{−d/2} E[|det(G − bI)|1{index(G − bI) = j}],

computed by nested Gauss–Legendre quadrature over the ordered eigenvalues against `|Δ(λ)|e^{−Σλ²/4}`. The normalization
equals Mehta's closed form (Q2). The total densities reproduce the closed forms to `10⁻⁸`:
- `d = 2`: `n_max = 1/(2π√3)`, `n_sad = 1/(π√3)`;
- `d = 3`: Bardeen–Bond–Kaiser–Szalay (1986), `(29 ∓ 6√6)/(5^{3/2}8π²R_*³)` with `R_*³ = 27/(15√15)` (Q3).

Two resolutions agree to `10⁻⁸` (Q4):

    β_2 = 3.122769186·10⁻³,    β_3 = 7.400614572·10⁻⁴,    24³β_3 = 10.230610.

*`γ_3` (Monte Carlo, exploration).* Write `I(s) := ∫Ψ_0^∞(b, se₁) db`. Then `γ_3 = 4π∫_0^∞ s²(I(s) − β_3) ds`, where `I(s)` uses
the exact two-point conditional law (Hermite covariance derivatives), Monte Carlo over the Hessian residual, and
Gauss–Hermite quadrature in `b`.
- **Shipped stdlib exploration** (`python3 gamma_explore.py 200000`, 2·10⁵ residual samples per separation, step `0.25`
  to `4.5`): `γ_3 = −0.0210 ± 0.0013` (batch standard error), `GAMMA.json`.
- **Independent check by the referee** (10⁶ samples per separation, a control variate tied to the decoupled law,
  cutoff varied from `4.5` to `6.5`, not shipped): `γ_3 = −0.0200 ± 0.0001`.
- **Development run** (numpy, 2·10⁵ samples per separation, step `0.1`, not shipped): `γ_3 = −0.019 ± 0.001`. Its
  plateau `I(s) = 7.436·10⁻⁴ ± 0.029·10⁻⁴` on `s ∈ [4.5, 6]` matches `β_3` to within 1.2 standard errors.

*Shape of `I(s)`* (shipped `GAMMA.json`). `I(s)` rises roughly linearly from about `0.09β_3` at `s = 0.25`, through `0.34β_3`
(`s = 1`) and `0.70β_3` (`s = 2`), and reaches `β_3` by `s ≈ 3.5–4`. Equal-height maximum/index-2-saddle pairs are depleted
at short range, so `γ_3 < 0`. (The referee observed, heuristically, that at equal heights the two endpoint axial
curvatures agree to leading order. That suggests `r^{d−1}Ψ_0 = O(r³)` and `I(s) ∝ s^{4−d}` near `0`, consistent with the
linear rise in `d = 3`; the `O(1)` bound of Step 5 is far from sharp here.)
*v1.2.* The merged #229 (Proposition W⁺, (W⁺.2) at `k = 0` and (W⁺.3); an author-side proof candidate with Codex's
scoped, conditional review 5381412814) proves the upper half of this heuristic for the torus kernel, up to a factor
`log(2/r)`, conditional on #229's imported interfaces. Precisely, `r^{d−1}Ψ_0(b, ru) ≤ Cr³log(2/r)(1 + |b|)^Ne^{−cb²}`
for `0 < r ≤ r_0^*`, so the equal-height mass below separation `ρ` is `O(ρ⁴log(2/ρ))`. The mechanism is the typed
window `|Y| ≲ r`, of conditional probability `O(r log(2/r))`. No matching lower bound or exact power is proved. #229
notes that the `d = 2` exploration suggests the logarithm may be an artifact.

## 3. Consequences (with the values of §2; exploration-level numbers)

- **Theorem Z's corollaries become quantitative for the SIDE24 field.** Per unit volume:
  - the expected rejected count with gap in `(0, t]` is `B_{3,24}t + o(t) ≈ 10.2t` ((Z7));
  - `ρ_rej(ℓ)/ν_cand(ℓ) ~ (B/c)ℓ^{1/3} ≈ 244ℓ^{1/3}` ((Z8));
  - the cumulative ratio is `≈ 163t^{1/3}` ((Z9)).
- **Size of the candidate density.** In `ν_cand(ℓ) = cℓ^{−1/3} + B + o(1)` (#191, merged; with rates, #218 and #229), the constant exceeds the singular term once
  `ℓ > (c/B)³ ≈ 6.8·10⁻⁸`. Unmarked max/index-2-saddle pairs with small height gap on the side-24 torus are therefore
  overwhelmingly unrelated, far-apart pairs. By Theorem Z the elder rule removes all of them in the limit; the elder
  density has no constant term (#191 (R+.2)).
- **With #207 (CU′.2)** (merged), `ρ_rej(ℓ) ≈ 10.21 + 0.072ℓ^{1/4}` for small `ℓ`.

## 4. Sources

| Tag | Path / reference | Role |
|---|---|---|
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z2)–(Z4), §2 (nondegeneracy, (Z10)), §4 (Z15)–(Z17), (Z7)–(Z9) — consumed |
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2) near-pair nondegeneracy, (R3) the regression form, Lemma R3.1 (R6) — consumed (Steps 1, 5) |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | §2, the pointwise bound behind (K1) — cited (v1's Lemma N, superseded by Step 5) |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 distinct-site jet rank, §3 near-pair nondegeneracy, (5.1)–(5.3), the field — consumed |
| side24_v1 | `coefficients/side24_v1/PROOF.md` (blob `44b66f04`) | the value `c_{3,24} = 0.0417759318…` in §§0, 3 — cited only |
| #191, #207 | `frontiers/remainder_vanishing_20260930/PROOF.md` (`441152df`), `frontiers/cusp_second_order_20261001/PROOF.md` (`f6df5a73`); merged since v1.1 | interpretation of `B_{d,L}` as `ν_cand`'s constant term; `ρ_rej`'s `ℓ^{1/4}` term — cited only |
| #218, #229 | `frontiers/candidate_third_order_20261001/PROOF.md` (`70ca57ef`), `frontiers/third_order_rate_20261001/PROOF.md` (`110ed33a`); merged | Theorems T and T⁺ (`B_{d,L}` with rates); Proposition W⁺ (§2's heuristic) — cited only (v1.2) |
| [BBKS] | J. M. Bardeen, J. R. Bond, N. Kaiser, A. S. Szalay, *The statistics of peaks of Gaussian random fields*, Astrophys. J. 304 (1986) 15–61 | closed-form densities of maxima and saddles in `d = 3` (control Q3) — external |
| [Mehta] | M. L. Mehta, *Random Matrices*, 3rd ed., Elsevier (2004), the Selberg/Mehta integral | GOE normalization (control Q2) — external |

## 5. Controls and exploration

`equal_height_mass.py` (stdlib; `RESULTS.json` its output, byte-identical under `-O`):
- **Q1:** the conditional Hessian law, in exact rationals.
- **Q2:** the scaled-GOE normalization against Mehta.
- **Q3:** the total densities against the closed forms (`d = 2`; BBKS for `d = 3`).
- **Q4:** `β_2`, `β_3` at two resolutions.
- **Mutants:** M1 (the unconditioned diagonal variance `3`), M2 (no Vandermonde factor) and M3 (index-`d` points counted as
  saddles) exit 1; an unknown label exits 2.

The controls test the one-point densities and `β_d` only. Proposition V is proved in prose. `gamma_explore.py`
(stdlib, Monte Carlo, fixed seed, not replayed by the workflow; output `GAMMA.json`) is exploration.

## 6. Review slices

A: Proposition V. This covers:
- the Lipschitz dependence of the Kac–Rice kernel on the covariance (Step 1);
- far-field nondegeneracy (Step 2);
- the image bound (Step 3);
- the far integration (Step 4);
- the uniformity in `L` of (Z15)'s constants, and the dominated convergence (Step 5).

B: The numbers. This covers:
- the conditional Hessian law;
- the reduction to scaled-GOE eigenvalue integrals and the quadrature;
- the agreement with the BBKS densities;
- `β_3`, the Monte Carlo design for `γ_3`, and `B_{3,24} ≈ 10.21`.

**Changed bytes in v1.2** (status update, against v1.1 at `8e89fe8`, NOTE blob `ed0d3fa8`):
- *Header:* the object label and version list, and the sentence on #191 and #207.
- *§0:* "(merged)" for #191, and the parenthetical on #218 and #229.
- *§2:* the v1.2 paragraph after the `γ_3` heuristic.
- *§3:* "merged" for #191 and #207.
- *§4:* the #191/#207 row and the new #218/#229 row.
- *§6:* this list.

Proposition V, its proof (Steps 1–5), §1, every number, `equal_height_mass.py`, `RESULTS.json`, `gamma_explore.py` and
`GAMMA.json` are unchanged.

**Changed bytes in v1.2.1** (wording only, against v1.2 at `f35b28b`, NOTE blob `1d265140`; Grok Bot agent 15,
5976336060):
- *Header:* the object label; the v1.2.1 line; the three v1.2 sub-bullets on #218, #229 and Slice A, replaced by the
  verdict's text (findings 4–6); and the consumed-sources sentence, which now lists [C7-K] as cited only, as §4 does
  (finding 7, third bullet).
- *§2:* the first sentence of the v1.2 paragraph, replaced by the verdict's text (finding 4).
- *§6:* this list.

§0, §1, §§3–5, Proposition V and its proof (Steps 1–5), every number, `equal_height_mass.py`, `RESULTS.json`,
`gamma_explore.py` and `GAMMA.json` are unchanged.
