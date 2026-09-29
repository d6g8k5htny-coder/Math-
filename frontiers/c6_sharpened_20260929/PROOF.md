# C6 successor: a super-exponential Rouché-degree tail, and the bound in every dimension

Object: CL-C6-SHARPENED-20260929-v1.
Author: Anthropic Claude (Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`).
Disposition: AUTHOR-SIDE CANDIDATE; nonauthor review required.
Scientific effect: NONE. No register, graph, catalog, lemma flag or prize changes.

**Relation to #140.** This is a successor to CL-C6-FACTORIAL-20260929-v1 (Math-#140,
`frontiers/c6_factorial_moment_20260929/PROOF.md`). That file is **not modified**; this note cites it as [C6].
- The route in §3 was proposed by OpenAI in
  [#140 comment 5893989971](https://github.com/d6g8k5htny-coder/Math-/pull/140#issuecomment-5893989971).
- Its arithmetic was checked in [5894002968](https://github.com/d6g8k5htny-coder/Math-/pull/140#issuecomment-5894002968).
- This note writes the route out in full and adds the dimension-`d` form.

## 1. Statements

The setting, law `Q_r^W`, window `I_r` and count `N` (window critical points off the pins) are as in [C6] §1, on
`T^d = ℝ^d/Tℤ^d`. The pins, the weight `W_r = F_d(H_M)F_{d−1}(H_S)` and the normalizer `Z_r` are those of
`imports/lifetime_parent_20260925` [LP] in fixed dimension `d`. Put `L = log(1/r)`.

**Theorem S₂ (`d = 2`).** There are `C` and `0 < r_* < e^{−e}` such that for `0 < r ≤ r_*`

    E_{Q_r^W} N(N−1) ≤ C r³ [L / log L]²,
    E_{Q_r^W} (N)_q ≤ C_q r³ [L / log L]^{2(q−1)}      (each fixed integer q ≥ 2).        (S2)

This sharpens [C6]'s `r³ L²`.

**Theorem S_d (every fixed `d ≥ 2`, conditional).** Assume Theorem G_d of Math-#141:
`E_{Q_r^W} N ≤ C r³`, which is under review. Then

    E_{Q_r^W} N(N−1) ≤ C r³ [L / log L]^d,    E_{Q_r^W} (N)_q ≤ C_q r³ [L / log L]^{d(q−1)}.        (Sd)

For `d = 2`, G_2 is the reviewed (I5), so S₂ is unconditional.

**Consequence.** With the recorded lower obstruction `E N(N−1) ≥ 2c r³`, the planar optimal order lies between `r³`
and `r³[L/log L]²`. `Θ(r³)` is **not** claimed. The Palm route of [C6] §9 remains the separate route to it.

**Inputs.**

From [C6], used verbatim:
- the pathwise cap (§2);
- Lemma R (§3);
- the protected cover (§5), including the measurability paragraph;
- Lemma D and Lemma E (§6, fixed annuli, unchanged), which OpenAI review 5355120953 accepts in `d = 2`.

Their `d`-dimensional forms are in §4 below.

From [LP], accepted in the D1 reconciliation, all in fixed `d`:
- `W_r/r²` has bounded moments of every order ((4.1), (5.1));
- `Z_r ≥ z_* r²` ((5.5)).

The first moment: (I5) in `d = 2`; Theorem G_d of #141 in `d ≥ 3`.

## 2. Growth lemma for the complexified gradient

**Lemma G.** Uniformly in `r ≤ r_*`, marks, frames and centres `c`, for every `R ≥ 1`,

    E_{Q_r} [ sup_{z ∈ Ω_R(c)} |F(z)|² + sup_{z ∈ Ω_R(c)} ‖DF(z)‖² ] ≤ C e^{C R²}.                      (G)

Here `F` is the complexified gradient and `Ω_R(c)` the Hermitian ball in `ℂ^d`.

*Proof.*
- **Series.** Write `f = Σ_n σ_n(ξ_n cos(n'·x) + ζ_n sin(n'·x))`, with `n' = 2πn/T`,
  `σ_n = κ e^{−|n'|²/4}` and i.i.d. standard `ξ, ζ`.
- **Mode bounds.** For `|Im z| ≤ R`, each derivative of order `k ≤ 2` of `cos(n'·z)` or `sin(n'·z)` has modulus
  `≤ |n'|^k e^{R|n'|}`.
- **Minkowski.** This gives `‖sup_{Ω_R}|∂^α f|‖_{L²} ≤ C Σ_n |n'|^k e^{−|n'|²/4 + R|n'|}`.
- **Completing the square.** `−s²/4 + Rs = R² − (s/2 − R)²`. The lattice sum of `|n'|^k e^{−(|n'|/2 − R)²}` is
  `O((1+R)^{k+d})`: shells of width `O(1)` around radius `2R` carry `O((1+R)^{d−1})` points. Hence
  `E sup |∂^α f|² ≤ C (1+R)^{2k+2d} e^{2R²} ≤ C e^{3R²}`.
- **Under `Q_r`.** The regression correction is `c(z)(e − E_r(f))`, with `c(z) = Cov(f(z), E_r)Cov(E_r)^{−1}`.
  - `Cov(∂^α f(z), ℓ) = ℓ(∂^α K_T(z − ·))`, and for complex `h = a + ib`,
    `|e^{−(h+Tm)·(h+Tm)/2}| = e^{−|a+Tm|²/2 + |b|²/2}`. So these entries grow at most like `C(1+R)^{C} e^{R²/2}`.
  - The functionals `E_r` have `C⁴`-dual norms bounded uniformly in `r`, and `Cov(E_r)^{−1}` is bounded ([C6] §4,
    [LP] §3). The targets `e` are bounded, and `E|E_r(f)|²` is bounded.
- (G) follows. ∎

## 3. Lemma M⁺: a super-exponential degree tail

Keep [C6]'s cover, its protected annuli `A'_j = {η_j/2 ≤ |z − c_j| ≤ 3η_j}`, its test spheres `ρ ∈ [η_j, 2η_j]` and its
Lemma D, **unchanged**. Change only the Cauchy radius used for the Taylor remainder.

**Lemma M⁺.** There are `C, m_0` (depending on `d`, `T`, `η`) such that for `m ≥ m_0`, all `j`, `r ≤ r_*`, marks and
frames,

    Q_r(m_j* > m) ≤ C exp(−(m log m)/(8d)).                                                       (M+)

*Proof.* Take the [C6] §5 cover with `η ≤ 1/8`. This is allowed, because `η ∈ (0, T/20)` is free there, and it gives
every `η' := η_j ≤ 1/8`. Fix `j` and write `c = c_j`.

**(a) Remainder with a growing radius.**
- Put `R_m = √m`, with `m ≥ 16`, so that `2η'/R_m ≤ 1/2`, and `S_m = sup_{Ω_{R_m}(c)} |F|`.
- Cauchy's estimate on complex lines ([C6] §6 (a)) gives, on `Ω_{2η'}(c)`,

      |F − T_m| ≤ S_m Σ_{k>m} (2η'/R_m)^k ≤ S_m a_m,    a_m := 2 (2η'/√m)^{m+1} ≤ m^{−m/2}.           (3.1)

  The last inequality uses `2η' ≤ 1/4`: `a_m ≤ 2·4^{−m−1} m^{−(m+1)/2} ≤ m^{−m/2}`.

- By Lemma G, `E S_m² ≤ C e^{Cm}`. The Lipschitz constant `L = sup_{Ω_{3η'}(c)} ‖DF‖` is on the **fixed** annulus
  and has bounded moments.

**(b) Failure means near-zeros on every sphere.** This is [C6] §6 (b), with new cutoffs:

    λ_m = m^{m/(8d)},   ε_m = 2 λ_m a_m,   δ_m = ε_m / λ_m = 2 a_m.

- If `m_j* > m`, every sphere `∂Ω_ρ`, `ρ ∈ [η', 2η']`, has a point `z_ρ` with `|T_m(z_ρ)| ≤ S_m a_m`.
- On `{S_m ≤ λ_m, L ≤ λ_m}` this gives `|F(z_ρ)| ≤ ε_m`, and then `|F| ≤ 2ε_m` on `B(z_ρ, δ_m)`.
- Radii `2δ_m` apart give disjoint balls inside `A'_j` once `δ_m ≤ η'/2`, which holds for `m ≥ m_0`. So

      V := Leb_{2d}{z ∈ A'_j : |F(z)| ≤ 2ε_m} ≥ c_d η' δ_m^{2d−1}.                                  (3.2)

**(c) Markov.** The `d`-dimensional Lemma D (§4) gives `E V ≤ C ε_m^{2d}(1 + log(1/ε_m))`. Hence

    Q_r(m_j* > m, S_m ≤ λ_m, L ≤ λ_m) ≤ C λ_m^{2d−1} ε_m (1 + log(1/ε_m)) / η'
                                      ≤ C λ_m^{2d} a_m · m log m ≤ C m^{−m/4} m log m.               (3.3)

Here `λ_m^{2d} = m^{m/4}` and `log(1/ε_m) ≤ m log m`.

**(d) Truncation.**

    Q_r(S_m > λ_m) ≤ C e^{Cm} m^{−m/(4d)},    Q_r(L > λ_m) ≤ C m^{−m/(4d)}.                           (3.4)

**(e) Conclusion.** Adding (3.3) and (3.4) gives `C e^{Cm} m^{−m/(4d)} ≤ C exp(−(m log m)/(8d))` once
`log m ≥ 8dC`. So `m_0` is at least `e^{8dC}`: large, but a constant. ∎

**Why the sharpening appears.** With [C6]'s fixed radius `4η'`, the remainder factor is only `2^{−m}`, so the tail is
merely exponential. With radius `√m`, the remainder factor `m^{−m/2}` is super-exponential. The price is the
`e^{Cm}` growth of `S_m` (Lemma G), and that price is still super-exponentially small against `m^{−m/(4d)}`.

## 4. The `d`-dimensional forms of [C6]'s Lemmas R, D and E, and of the cover

- **Lemma R in `ℂ^d`.**
  - Rouché for holomorphic maps `ℂ^d → ℂ^d` on `Ω_ρ` is the degree argument of [C6] §3, word for word.
  - A compact analytic subset of `Ω_ρ` is finite.
  - The refined Bézout inequality bounds the isolated zeros of `d` polynomials of degree `≤ m` in `d` variables by
    `m^d`, counted with multiplicity.
  - So a ball whose Rouché test passes at degree `m` carries at most `m^d` real critical points.
- **Lemma E on `ℤ^d`.** Shifts `τ_{e_1}, …, τ_{e_d}` commute, and distinct characters of `ℤ^d` have distinct
  eigenvalue `d`-tuples. The proof of [C6] §6 is unchanged.
- **Lemma D in `d` dimensions.**
  - `G = (Re F(z), Im F(z)/t) ∈ ℝ^{2d}`, with `t = |Im z|`. Its `t = 0` limit is `(∇f(x), D²f(x)u)`.
  - At `t = 0` the polynomial symbols `i a·n'` and `−(b·n')(u·n')` vanish only for `a = b = 0`.
  - At `t > 0` the points `z, z̄` are non-real and distinct from the pins mod `Tℤ^d`.
  - Compactness then gives a uniform floor for the conditional covariance. Hence
    `Q_r(|F(z)| ≤ 2ε) ≤ C ε^d (ε/t)^d = C ε^{2d}/t^d`, capped by 1.
  - Over the annulus, `∫_{|t|≤R} min(1, ε^{2d}/|t|^d) d^d t = |S^{d−1}| ε^{2d}(1/d + log(R/ε²))`.
    So `E V ≤ C ε^{2d}(1 + log(1/ε))`.
- **Cover.** [C6] §5's construction (big ball at the midpoint, a small-ball net of `{|x| ≥ 7η/8}`) is dimension-free.
  The real slices of the annuli stay `≥ η/4` from the pins.

## 5. Proof of Theorems S₂ and S_d

Put `Ψ = Σ_j (m_j*)^d`, which is `≥` the total critical count by §4 (Lemma R). By (M+),

    Q_r(Ψ > x) ≤ Σ_j Q_r(m_j* > (x/J')^{1/d}) ≤ C exp(−c x^{1/d} log x),      J' = number of balls.     (5.1)

In particular `sup_r E_{Q_r} Ψ^p < ∞` for all `p`.

**The cap.** As in [C6] (2.1), `N(N−1) ≤ λN + Ψ² 1{Ψ > λ}` pathwise. Then:
- `E_{Q_r^W} N ≤ C r³`, by (I5) for `d = 2` and by G_d for `d ≥ 3`.
- `E_{Q_r^W}[Ψ² 1{Ψ>λ}] ≤ Z_r^{−1}‖W_r‖_{L²}‖Ψ² 1{Ψ>λ}‖_{L²} ≤ C (E Ψ⁸)^{1/4} Q_r(Ψ > λ)^{1/4}`, by [LP] (5.1) and
  (5.5).

**Choice of `λ`.** Take `λ = A^d [L/log L]^d`, with `A` large. For `r ≤ r_*`,
`log λ = d(log A + log L − log log L) ≥ log L`, so `λ^{1/d} log λ ≥ A L`. By (5.1),
`Q_r(Ψ > λ)^{1/4} ≤ C exp(−c A L/4) ≤ r³` once `A ≥ 12/c`. Hence

    E_{Q_r^W} N(N−1) ≤ C r³ λ + C r³ ≤ C r³ [L/log L]^d.

**Factorial moments.** The `(N)_q` bound is identical, using `(N)_q ≤ λ^{q−1}N + Ψ^q 1{Ψ > λ}`. ∎

## 6. Scope

**Claimed.** Lemmas G and M⁺, the `d`-dimensional forms of §4, Theorem S₂, and Theorem S_d **conditional on G_d**
(#141). All constants are existential, for fixed `T` and compact marks.

**Not claimed.**
- `Θ(r³)`;
- the witness-conditioned (M′) or the marked upgrade (H) of [C6] §9;
- numerical constants;
- uniformity in `T`, `d`, or as `k ↓ 0`;
- any register, graph or catalog change;
- any change to [C6]'s reviewed bytes.

A defect in Lemma G's uniformity under `Q_r` blocks both theorems.

**Prior art.** Gass–Stecconi (arXiv:2305.17586, PTRF 2024) prove finiteness of moments of critical-point counts. No
novelty claim is made.

## 7. Finite companion

`sharp_check.py` (stdlib) checks:
- the completing-square identity;
- the lattice-shell sum growth against `(1+R)^{k+d}e^{R²}` for `d = 2, 3`;
- the remainder bound (3.1) exactly at perfect-square `m`;
- the exponent bookkeeping `λ_m^{2d} = m^{m/4}` and `λ_m² = m^{m/(4d)}`;
- the Lemma D radial integral in `d = 2, 3`;
- the choice `λ = A^d[L/log L]^d`, with `λ^{1/d} log λ ≥ A L`, at `r = 2^{−k}`.

Mutants `fixed-radius`, `wrong-cutoff`, `planar-cap` and `drop-loglog` must fail.
