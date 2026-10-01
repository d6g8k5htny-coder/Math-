# The equal-height mass `B_{d,L}`: a volume law and its value for the SIDE24 field

Object: CL-EQUAL-HEIGHT-MASS-20261001-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Disposition: AUTHOR-SIDE CANDIDATE (Proposition V) and EXPLORATION (the numbers); NONAUTHOR REVIEW REQUIRED.
Scientific effect: NONE — no register, graph, STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every
lane; zero organizational independence. Consumes merged sources only ([Z], [C7-K], [R], [P]); the unmerged Math- #191
and #207 are cited for interpretation, not used. v1 incorporates a clean-context referee pass (one gap — the uniformity
in `L` of the near-diagonal majorant — closed by Lemma N; minor points applied; `β_2`, `β_3` and `γ_3` independently
recomputed).

## 0. Statement

**Setting.** [Z] (`frontiers/c7_zero_gap_limit_20260929/PROOF.md`, blob `5b6328ea`) for the [P] field on
`X_L = R^d/(LZ^d)`, whose covariance is the normalized periodized Gaussian kernel
`K_L(z) = Σ_{n∈Z^d} e^{−|z+Ln|²/2} / Σ_{n∈Z^d} e^{−|Ln|²/2}` (unit variance). Its equal-height mass is

    B_{d,L} = ∫_{X_L∖{0}} ∫_R Ψ_0^{(L)}(b, y) db dy,     Ψ_0(b, y) = p_y(v_{b,0}) E_{Q_{y,b,0}}[W],                     ((Z2)–(Z3))

`W = |det H_0 det H_y|1{H_0 < 0, index H_y = d − 1}`. By Theorem Z (Z4), `B_{d,L}` is the limit of the rejected density,
`ρ_rej(ℓ) → B_{d,L}`; by Math- #191 (R+.1), unmerged, it is the constant term of the candidate density,
`ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + o(1)`. [Z] states that it gives "No numerical value for B_(d,L)".

Let `f_∞` be the stationary Gaussian field on `R^d` with covariance `e^{−|z|²/2}`, `ρ_j(b)` its height density of critical
points of index `j` (per unit volume and unit height) and `Ψ_0^∞(b, y)` its equal-height kernel ((Z2) on `R^d`).

**Proposition V (volume law).** As `L → ∞`,

    B_{d,L} = β_d L^d + γ_d + o(1),        β_d := ∫_R ρ_d(b) ρ_{d−1}(b) db,
                                            γ_d := ∫_{R^d}∫_R (Ψ_0^∞(b, y) − ρ_d(b)ρ_{d−1}(b)) db dy,          (V.1)

the last integral converging absolutely. For every fixed `r₀ > 0` the part of `B_{d,L}` from separations
`dist(0, y) ≥ r₀` equals `β_d(L^d − |B_{r₀}|) + ∫_{|y|≥r₀}∫(Ψ_0^∞ − ρ_dρ_{d−1}) db dy + O(L^{N}e^{−L²/8})`.

**Values (exploration; not certified).** For the Gaussian kernel,

    β_2 = 3.122769186·10⁻³,   β_3 = 7.400614572·10⁻⁴      (deterministic quadrature; controls Q1–Q4 of equal_height_mass.py),
    γ_3 = −0.020 ± 0.002                                     (two Monte Carlo explorations, §2),

so **`B_{3,24} ≈ 24³β_3 + γ_3 = 10.231 − 0.020 ≈ 10.21`**, about `244` times `c_{3,24} = 0.0417759318…` (the enclosure of
`coefficients/side24_v1`). Under the heuristic that the `o(1)` in (V.1) is of the size of the image terms,
`CL^N e^{−(L/2)²/2}` with `e^{−72} ≈ 5·10⁻³²` at `L = 24`, the uncertainty of `B_{3,24}` is that of `γ_3`.

**What is not claimed.** No rate for the `o(1)` in (V.1) (only for the far part); no certified value of `γ_3` or
`B_{3,24}`; nothing about `B_{d,L}` for covariances other than the periodized Gaussian kernel; no change to Theorem Z.

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

*Step 5 (near part).* **Lemma N (near majorant at equal heights, uniform in `L`).** There are `r₀, L₀, C, c, N` such that
for `0 < r < r₀`, `u ∈ S^{d−1}`, `b ∈ R` and `L ∈ [L₀, ∞]` (`L = ∞` meaning `f_∞`),
`r^{d−1}Ψ_0^{(L)}(b, ru) ≤ C(1 + |b|)^Ne^{−cb²}`.

*Proof.* By the separation-variable form of the Kac–Rice kernel ([Z] (Z14); #191 (2.1)), `r^{d−1}Ψ_0(b, ru) = r^{−2}A_r(b, 0, u)`
with `A_r = 12π_r(v_r)E_Q[W_r/r²]`. The pointwise bound in the proof of [C7-K] (K1) (§2: the pin identity of [P] (5.3) with
(5.1)–(5.2)) gives, at `k = 0`, `W_r/r² ≤ Cr²(1 + M)^{2m+4}`, where `M := max_{j≤4}M_j` and the `M_j` are the **local** `C^j`
seminorms of the field on the segment between the pins (the passage to global norms in [C7-K] is only used for moments).
Under `Q_{r,b,0}` the field is `F + C_rΣ_r^{−1}(v_r − U_r)` ([R] (R3)). The `Q`-moments of `M` are therefore bounded through
the restriction of the covariance to `B_{2r₀}`:
- `E sup_{B_{r₀}}|∂^αF|^p` is bounded through Sobolev embedding on the ball by finitely many derivatives of `K_L` at `0`;
- `C_r` on `B_{r₀}` depends only on `K_L` on `B_{2r₀}`;
- `Σ_r` depends only on `K_L` near `0`, and is uniformly positive for `r ≤ r₀` ([R] (R2), [P] §3).

Since `K_L → K_∞` in `C^q(B_{2r₀})` for every `q`, at the rate `L^Ne^{−L²/8}`, all three bounds are uniform in `L ∈ [L₀, ∞]`.
This gives `E_Q(1 + M)^p ≤ C_p(1 + |b|)^p` and `π_r(v_r(b, 0)) ≤ Ce^{−cb²}`, and hence the claim. ∎

With Lemma N, `Ψ_0^{(L)}(b, y) → Ψ_0^∞(b, y)` pointwise for `0 < |y| < r₀` (Step 1 at fixed `y`, with `c = c(|y|)`), and
dominated convergence in polar coordinates gives `∫_{|y|<r₀}∫Ψ_0^{(L)} → ∫_{|y|<r₀}∫Ψ_0^∞ < ∞`. This replaces any appeal
to the uniformity in `L` of [Z] (Z15), whose proof uses whole-torus norms with `L`-dependent constants. Since
`ρ_dρ_{d−1}` is bounded and integrable in `b`, `γ_d` converges absolutely.

Adding the near and far parts, `B_{d,L} = β_dL^d + γ_d + o(1)`. ∎

(Step 5 is where the rate is lost. Quantifying (Z15)'s dependence on the covariance would give `O(L^Ne^{−L²/8})`, but
that is not done here.)

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
linear rise in `d = 3`; Lemma N's `O(1)` is far from sharp here.)

## 3. Consequences (with the values of §2; exploration-level numbers)

- **Theorem Z's corollaries become quantitative for the SIDE24 field.** Per unit volume:
  - the expected rejected count with gap in `(0, t]` is `B_{3,24}t + o(t) ≈ 10.2t` ((Z7));
  - `ρ_rej(ℓ)/ν_cand(ℓ) ~ (B/c)ℓ^{1/3} ≈ 244ℓ^{1/3}` ((Z8));
  - the cumulative ratio is `≈ 163t^{1/3}` ((Z9)).
- **Size of the candidate density.** In `ν_cand(ℓ) = cℓ^{−1/3} + B + o(1)` (#191, unmerged), the constant exceeds the singular term once
  `ℓ > (c/B)³ ≈ 6.8·10⁻⁸`. Unmarked max/index-2-saddle pairs with small height gap on the side-24 torus are therefore
  overwhelmingly unrelated, far-apart pairs. By Theorem Z the elder rule removes all of them in the limit; the elder
  density has no constant term (#191 (R+.2)).
- **With #207 (CU′.2)** (unmerged), `ρ_rej(ℓ) ≈ 10.21 + 0.072ℓ^{1/4}` for small `ℓ`.

## 4. Sources

| Tag | Path / reference | Role |
|---|---|---|
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z2)–(Z4), §2 (nondegeneracy, (Z10)), §4 (Z15)–(Z17), (Z7)–(Z9) — consumed |
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2) near-pair nondegeneracy, (R3) the regression form, Lemma R3.1 (R6) — consumed (Steps 1, 5) |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | §2, the pointwise bound behind (K1) with local seminorms — consumed (Lemma N) |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 distinct-site jet rank, §3 near-pair nondegeneracy, (5.1)–(5.3), the field — consumed |
| side24_v1 | `coefficients/side24_v1/PROOF.md` (blob `44b66f04`) | the value `c_{3,24} = 0.0417759318…` in §§0, 3 — cited only |
| #191, #207 | unmerged | interpretation of `B_{d,L}` as `ν_cand`'s constant term; `ρ_rej`'s `ℓ^{1/4}` term — cited only |
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
