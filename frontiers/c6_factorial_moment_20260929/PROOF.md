# C6: the torus-wide second factorial moment is `O(r³ log²(1/r))`

Object: CL-C6-FACTORIAL-20260929-v1.
Author: Anthropic Claude (Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`).
Disposition: AUTHOR-SIDE CANDIDATE; nonauthor review required.
Version: v1.2.
- v1.1 added the record-keeping completions requested in OpenAI review 5355120953: `m* = ∞`, measurability, integer
  `q`, and `r_* < 1`. That review ACCEPTs §§4–6 (Lemmas E, D and M) at stated scope.
- v1.2 answers the bounded xAI/Grok read of Lemma R and §8 (#140 comment 5894209739). It adds two explicit sentences
  to Lemma R, and exact citations for the inputs of §8 (§1): the D1 parent's §5 for `W_r` and `Z_r`, and the (I5) row
  with the (P2) HOLD it inherits. §§4–7 are byte-identical to v1.1.
- There is no theorem change. Lemma R and the §8 assembly still need a nonauthor verdict; the xAI read found no
  contradiction and is not a C6-L ACCEPT.
Scientific effect: NONE. No register, graph, lemma flag, prize or premise changes. The catalog entry C6 and the D5
collision node are not moved by this file.

## 1. Setting and result

**The law.** This note uses the setting of the reviewed D5 sources (`PUNCTURED_PIN_PROOF.md` (P1),
`frontiers/intermediate_window_20260928/PROOF.md` (I2)):
- `f` is the centered variance-one Gaussian field on `T² = ℝ²/Tℤ²` with covariance `K_T`, for fixed `T`.
- The pins are `M, S` with `|M − S| = r`, `f(M) = b`, `f(S) = b − kr³` and `∇f(M) = ∇f(S) = 0`. Here `b` lies in a
  compact interval, `0 < k_− ≤ k ≤ k_+`, and frames range over `O(2)`.
- `Q_r` is the Gaussian regression law of the six pins. `W_r = F_2(H_M)F_1(H_S)`, `Z_r = E_{Q_r}W_r`, and
  `dQ_r^W = (W_r/Z_r) dQ_r`.

**The count.** `I_r = (b − kr³, b)` is the between-pin window. `N` is the number of critical points in
`T² ∖ {M, S}` with height in `I_r` (all indices). This is the count of catalog C6.

**Theorem C6-L.** There are `C > 0` and `0 < r_* < 1`, uniform in `b`, `k`, frames, such that for `0 < r ≤ r_*`

    E_{Q_r^W}[N(N − 1)] ≤ C r³ log²(1/r).                                  (C6L)

More generally, for each fixed integer `q ≥ 2`, `E_{Q_r^W}[(N)_q] ≤ C_q r³ log^{2(q−1)}(1/r)`.

**Consequence for C6.** The validated lower obstruction (`docs/integration/2026-09-29-reviewed-window-and-inverse.md`)
is `E N(N − 1) ≥ 2 P(N ≥ 2) ≥ 2c r³`. So the optimal order of the torus-wide second factorial moment lies between
`r³` and `r³ log²(1/r)`. §9 isolates the one estimate that would remove the logarithm.

**Inputs consumed.** Each is cited at an exact reviewed row, never at the (P2) count row.
- **(I5)** `E_{Q_r^W} N ≤ C r³`, for the window count `N` of this note (heights in `I_r`, pins removed):
  `frontiers/intermediate_window_20260928/PROOF.md` (I5).
  - Verdicts: `reviews/d5_i5_planar_f_20260928/REVIEW.md` (xAI), row "I5 … **ACCEPT** as corollary of C2 + I4 + D4 A";
    `reviews/d5_intermediate_window_claude_20260928/REVIEW.md`, I5 ACCEPT with the explicit tiling (N1).
  - (I5) is a window first moment and is used only as one. Nothing here upgrades it to all heights.
  - Its local part is (C2), which consumes (P2). The (P2) continuum steps carry an xAI HOLD (#111) and a Claude ACCEPT
    (`reviews/d5_punctured_pin_continuum_claude_20260929/`); the Claude record is not a second independent vote.
  - So C6-L holds exactly at the scope of the D5 reading rule `reviews/d5_reconciliation_20260929/`, and no stronger.
- **(W2)** `‖W_r‖_{L²(Q_r)} ≤ C r²` and **(Z)** `Z_r ≥ z_* r²`. Primary source: the D1 parent
  `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d…`) §5.
  - The sentence "det H_i/r and W_r/r^2 have uniformly bounded moments of every finite order" gives (W2).
  - (5.5) `0 < z_* ≤ Z_r/r² ≤ z^*` gives (Z).
  - Both are component (I) of the D1 reading rule (`reviews/d1_chain_reconciliation_20260928/`), consumed by the
    register row D1 (Theorem A, accepted at stated scope). Full-depth nonauthor review of that interface is C1
    (Anthropic), with partial xAI checks G3 of the UI majorant and of `z_* > 0`.
  - At `d = 2`, `L = T` the D1 law is this note's law: the same covariance `K_T`, the same six observations (P1)
    (`M = −(r/2)u`, `S = (r/2)u`), and the same weight, since `F_2(H_M)F_1(H_S) = |det H_M det H_S| 1{H_M < 0,
    index(H_S) = 1}`. The parent's `r < L/(4√2)` is absorbed into `r_*`.
- The same two facts are (P13)–(P14) of `reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md` §7. There (W2)
  follows from `det H_M/r, det H_S/r = O_{L^s}(1)`, by (P13) and the bounded moments of `S_0`. They are covered by
  the Claude continuum record rows "§3 endpoint regression … ACCEPT" and "§7 (P13)–(P14) … ACCEPT"; #111 has no
  standalone row for them. The D1 citation above is the primary one.

Everything else is proved here, from standard facts: multidimensional Rouché, Bézout, Cauchy estimates and
Gaussian regression.

## 2. The pathwise cap

Let `Ψ` be any random variable with `Ψ ≥ #{critical points of f on T²}`. Since `N ≤ Ψ`, pathwise

    N(N − 1) ≤ N·Ψ ≤ λ N + Ψ² 1{Ψ > λ}        for every λ > 0,                 (2.1)

and `(N)_q ≤ N Ψ^{q−1} ≤ λ^{q−1} N + Ψ^q 1{Ψ > λ}`. The rest of the note constructs a `Ψ` whose tail under `Q_r` is
stretched-exponential, uniformly in `r`.

## 3. Rouché–Bézout cap

For `c ∈ ℂ²` put `Ω_ρ(c) = {z ∈ ℂ²: |z − c| < ρ}` (Hermitian norm).

**Lemma R.** Let `F: ℂ² → ℂ²` be holomorphic near `Ω̄_ρ(c)`, with `c` real. Let `P` be a polynomial map of degree
`≤ m`. If `|F − P| < |P|` on `∂Ω_ρ(c)`, then `F` has at most `m²` zeros in the real ball `B_ℝ(c, ρ)`.

Here `|·|` is the Hermitian norm of `ℂ²` throughout. It defines the ball `Ω_ρ(c)`, and the same norm is used on
both sides of the value inequality `|F − P| < |P|`. Only this consistency on the value side is used in step 3.

*Proof.*
1. **`P` has finitely many zeros in `Ω_ρ`.** `Z(P) ∩ ∂Ω_ρ = ∅`, so `Z(P) ∩ Ω_ρ = Z(P) ∩ Ω̄_ρ` is a compact analytic
   subset of the open set `Ω_ρ`, hence finite.
   - Explicitly, let `V` be an irreducible component of `Z(P)` that meets `Ω_ρ`. Then `V ∩ Ω_ρ = V ∩ Ω̄_ρ` is compact.
   - If `dim V ≥ 1`, then `V` is pure-dimensional, so `V ∩ Ω_ρ` is a compact analytic set of positive dimension.
     The maximum principle for the coordinate functions on its irreducible components rules this out.
   - So no positive-dimensional component of `Z(P)` meets `Ω_ρ`. In particular none meets the real ball
     `B_ℝ(c, ρ) ⊂ Ω_ρ`.
2. **Bézout.** The refined Bézout inequality bounds the isolated zeros of `P`, counted with multiplicity, by `m²`.
3. **Rouché.** The homotopy `P + t(F − P)`, `t ∈ [0, 1]`, has no zero on `∂Ω_ρ`. So the Brouwer degrees of `P` and `F`
   on `Ω_ρ` agree, and `F` also has finitely many zeros in `Ω_ρ`. For holomorphic maps, the local degree at an
   isolated zero is its multiplicity, which is at least 1. So `#Z(F) ∩ Ω_ρ ≤ m²` counting multiplicity.
4. **Real zeros.** Real zeros of a real-analytic `F` in `B_ℝ(c, ρ) ⊂ Ω_ρ` are among these. ∎

## 4. Complexification and moments

**The entire extension.** By Poisson summation, `f = Σ_n σ_n(ξ_n cos(n'·x) + ζ_n sin(n'·x))` with `n' = 2πn/T`,
i.i.d. standard `ξ, ζ`, and `σ_n² ∝ exp(−|n'|²/2) > 0`.
- On `{|Im z| ≤ Y}`, `|cos(n'·z)|, |sin(n'·z)| ≤ e^{|n'|Y}`, and `Σ_n σ_n |n'|^k e^{|n'|Y} < ∞`.
- So `f` extends a.s. to an entire function on `ℂ²`, real on `ℝ²` with `f(z̄) = conj f(z)`.
- By Minkowski, `E sup_{|Im z| ≤ Y, Re z ∈ [0,T]²} |∂^k f(z)|^p < ∞` for all `k, p, Y`.

**Under `Q_r`.** `f_{Q_r} = f + c(·)(e − E_r(f))`, with `E_r` and `e` from (P3). The coefficient
`c(z) = Cov(f(z), E_r)Cov(E_r)^{−1}` is entire. `Cov(f(z), E_r) = E_r[K_T(z − ·)]`, and each entry of `E_r` is a
difference quotient with `C⁴`-dual norm bounded uniformly in `r`. `Cov(E_r)^{−1}` is bounded (PUNCTURED_PIN §3).

Hence, with `F = ∇f` complexified, for every compact complex domain `D` and every `p`,

    sup_{r ≤ r_*, b, k, frame} E_{Q_r}[ sup_D |F|^p + sup_D ‖DF‖^p ] < ∞.                  (4.1)

## 5. The cover

By stationarity put the midpoint `o = (M + S)/2` at the origin, so `|M|, |S| ≤ r/2`. Fix `η ∈ (0, T/20)`.
- **The ball around the pins.** Center `c_0 = o`, radius `η_0 = η`.
- **Small balls.** Centers `c_1, …, c_J` form a finite `η/16`-net of `{|x| ≥ 7η/8}`, with radius `η_j = η/8`.

These real balls cover `T²`.

For each `j` the complex annulus `A'_j = {η_j/2 ≤ |z − c_j| ≤ 3η_j}` has real slice at distance at least `η/4` from
the pins:
- for `j = 0`, `|x| ≥ η/2`;
- for `j ≥ 1`, `|x| ≥ 7η/8 − 3η/8 = η/2`, taking `r ≤ η/2`.

**The degree.** Let `T_m^{(j)}` be the degree-`m` Taylor polynomial of `F` at `c_j`. Define

    m_j* = min{ m ≥ 1 : ∃ ρ ∈ [η_j, 2η_j] with |F − T_m^{(j)}| < |T_m^{(j)}| on ∂Ω_ρ(c_j) },
    Ψ = Σ_{j=0}^{J} (m_j*)².                                                    (5.1)

Put `m_j* = ∞` if no degree works. Lemma M shows that this has probability zero. By Lemma R,
`Ψ ≥ #{critical points on T²}`, pins included.

**Measurability.** For fixed `m`, the map `ρ ↦ min_{∂Ω_ρ(c_j)} (|T_m^{(j)}| − |F − T_m^{(j)}|)` is continuous on
`[η_j, 2η_j]`, because `F` is continuous on the compact complex ball. So the set of admissible `ρ` is relatively
open, and it is nonempty iff it contains a rational `ρ`. Hence `{m_j* ≤ m}` is a countable union of events
`{min_{∂Ω_ρ}(|T_m| − |F − T_m|) > 0}`, `ρ ∈ ℚ`. Each of these is measurable as the minimum of a continuous random
field over a compact set. `m_j*` and `Ψ` are therefore random variables, which licenses the probability and
expectation operations below.

## 6. Lemma M: the Rouché degree has a uniform exponential tail

**Lemma M.** There are `C, m_0` such that `Q_r(m_j* > m) ≤ C 2^{−m/4}` for all `m ≥ m_0`, all `j`, `r ≤ r_*`, `b`, `k`
and frames.

*Proof.* Fix `j` and write `c = c_j`, `η' = η_j`, `S = sup_{Ω_{4η'}(c)} |F|` and `L = sup_{Ω_{3η'}(c)} ‖DF‖`.

**(a) Remainder.** For `w ∈ ℂ²`, the homogeneous expansion `F(c + w) = Σ_k P_k(w)` satisfies
`|P_k(w)| ≤ S(|w|/4η')^k`. This is Cauchy's estimate for `ζ ↦ F(c + ζw/|w|)` on `|ζ| < 4η'`. Hence on `Ω_{2η'}(c)`,

    |F − T_m| ≤ S Σ_{k>m} 2^{−k} = S 2^{−m}.                                         (6.1)

**(b) Failure means near-zeros on every sphere.**
- If `m_j* > m`, then for every `ρ ∈ [η', 2η']` some `z_ρ ∈ ∂Ω_ρ` has `|T_m(z_ρ)| ≤ S2^{−m}`, hence
  `|F(z_ρ)| ≤ 2S2^{−m}`.
- Put `λ = 2^{m/8}`, `ε = 2λ2^{−m}` and `δ = ε/λ = 2^{1−m}`. Take `m ≥ m_0` so that `δ ≤ η'/2`.
- On `{S ≤ λ, L ≤ λ}` we get `|F| ≤ 2ε` on each ball `B(z_ρ, δ)`.
- The radii `ρ_i = η' + 2iδ`, `0 ≤ i ≤ ⌊η'/2δ⌋`, give pairwise disjoint balls inside `A'_j`. So the sublevel volume
  `V := Leb₄{z ∈ A'_j : |F(z)| ≤ 2ε}` satisfies

      V ≥ (η'/2δ)(π²/2)δ⁴ = (π²/4) η' δ³.                                           (6.2)

**(c) Markov.** By Lemma D below, `E V ≤ ∫_{A'_j} C min(1, ε⁴/|Im z|²) d⁴z ≤ C ε⁴(1 + log(1/ε))`. Hence

    Q_r(m_j* > m, S ≤ λ, L ≤ λ) ≤ 4 E V / (π² η' δ³) ≤ C λ³ ε (1 + log(1/ε)) / η' ≤ C m 2^{−m/2}.

**(d) Truncation.** `Q_r(S > λ) + Q_r(L > λ) ≤ C 2^{−m/4}` by (4.1) with `p = 2`. ∎

**Lemma D.** Uniformly for `z ∈ A'_j` (all `j`), `r ≤ r_*`, `b`, `k`, frames,
`Q_r(|F(z)| ≤ 2ε) ≤ C min(1, ε⁴/|Im z|²)`.

*Proof.* Write `z = x + itu` with `u ∈ S¹` and `t = |Im z|`. For real `f`:
- `Re ∂_i f(z) = (∂_i f(z) + ∂_i f(z̄))/2` and `Im ∂_i f(z) = (∂_i f(z) − ∂_i f(z̄))/2i`. These are evaluations at
  the two complex points `z, z̄`.
- Set `G(x, u, t) = (Re F(z), Im F(z)/t)` for `t > 0`. Since `Im F(x + itu)/t = ∫_0^1 Re DF(x + istu)u ds`, `G`
  extends continuously to `t = 0` with `G = (∇f(x), D²f(x)u)`.

**Claim.** The `Q_r`-covariance `Σ̂` of `G` has determinant `≥ c > 0` on the compact parameter set, including
`r ∈ [0, r_*]`. At `r = 0` the six pins are replaced by their contact limit `E_0`, the jet at `o` of (P3).

Then, since `|Re F| ≤ 2ε` and `|Im F| ≤ 2ε` force `G` into a set of volume `C ε²(ε/t)²`,

    Q_r(|F(z)| ≤ 2ε) ≤ ‖density of G‖_∞ · C ε²(ε/t)² ≤ C ε⁴/t².

**Proof of the claim.**
- By continuity in all parameters (for `E_r`, (P3)) and compactness, it suffices that `Σ̂ > 0` at every parameter.
- `Σ̂` is degenerate iff some nonzero real combination `ℓ` of the four `G`-functionals and the six pin functionals
  has `Var ℓ(f) = 0`.
- `Var ℓ(f) = Σ_n σ_n² |ℓ(e^{in'·})|²`, so this means `ℓ(e^{in'·}) = 0` for all `n ∈ ℤ²`. In other words,
  `Σ_w P_w(n) e^{in'·w} = 0` on `ℤ²`, where `w` runs over the evaluation points and the `P_w` are polynomials.
- **For `t > 0`** the points are `z`, `z̄` (non-real, distinct mod `Tℤ²`) and the real pins. Lemma E gives `P_z ≡ 0`
  and `P_{z̄} ≡ 0`, that is `α_i/2 ± β_i/(2it) = 0` for the coefficients of `Re ∂_i` and `Im ∂_i/t`. So `α = β = 0`,
  and then the pin coefficients vanish too.
- **For `t = 0`** the points are `x` and the pins (or `o`), with `|x − o| ≥ η/4`. `P_x(n) = i a·n' − (u·n')(b·n')`
  vanishes identically only if `a = 0` and `b = 0`, because `u ≠ 0`. ∎

**Lemma E.** Let `w_1, …, w_K ∈ ℂ²` be pairwise distinct mod `Tℤ²` and `P_k` polynomials. If
`Σ_k P_k(n) e^{2πi n·w_k/T} = 0` for all `n ∈ ℤ²`, then every `P_k = 0`.

*Proof.*
- `χ_k(n) = e^{2πi n·w_k/T}` are distinct characters of `ℤ²`. Two coincide iff `w_k − w_l ∈ Tℤ²`.
- For the shifts `τ_e g(n) = g(n + e)`, `e ∈ {e_1, e_2}`, each `P_kχ_k` lies in the joint generalized eigenspace of
  the commuting operators `(τ_{e_1}, τ_{e_2})` with eigenvalue pair `(χ_k(e_1), χ_k(e_2))`. These pairs are distinct.
- Joint generalized eigenspaces for distinct eigenvalue pairs are independent. This holds on the finite-dimensional
  shift-invariant span of `{n^α χ_k}`. So every `P_kχ_k = 0`, and `χ_k ≠ 0` gives `P_k = 0`. ∎

## 7. Tail of `Ψ`

By Lemma M, `Q_r(Ψ > λ) ≤ Σ_j Q_r(m_j* > (λ/(J+1))^{1/2}) ≤ C exp(−c λ^{1/2})`. So `sup_r E_{Q_r} Ψ^p < ∞` for
every `p`.

## 8. Proof of Theorem C6-L

Take expectations in (2.1) under `Q_r^W`.

**First term.** `E_{Q_r^W} N ≤ C r³` by (I5), summed over indices.

**Second term.** `E_{Q_r^W}[Ψ²1{Ψ > λ}] = Z_r^{−1} E_{Q_r}[W_r Ψ² 1{Ψ > λ}]`. By (W2),
`‖W_r‖_{L²(Q_r)} ≤ C r²`, and `Z_r ≥ z_* r²` by (Z) (§1). Hence

    E_{Q_r^W}[Ψ² 1{Ψ > λ}] ≤ C E_{Q_r}[Ψ⁴ 1{Ψ > λ}]^{1/2} ≤ C (E_{Q_r}Ψ⁸)^{1/4} Q_r(Ψ > λ)^{1/4}
                           ≤ C exp(−c λ^{1/2}/4).

**Choice of `λ`.** For `0 < r ≤ r_* < 1`, `λ = (C' log(1/r))²` makes the second term at most `r³`. This gives (C6L). The `q`-th factorial
moment is identical, with `λ^{q−1}` and `Ψ^q`. ∎

## 9. What would remove the logarithm

**The pin mechanism.** This is a remark; nothing in §§2–8 uses it.
- In local coordinates `X = M + r(p, q)` with `S_0 = f_zz(M) = rσ`, (P4)–(P6) give
  `(f_x, f_z)(X)/r² = (F_1, F_2) + O(r)`, where
  - `F_1 = 6kp(p−1) + (p−½)qT_3 + q²C_3/2`,
  - `F_2 = σq + ½p(p−1)T_3 + pqC_3 + q²D/2`, with `D = f_zzz(M)`.
- **Elimination.** For `T_3 ≠ 0` the identity `F_1 − (12k/T_3)F_2 = q·ℓ(p, q)` holds exactly, with `ℓ` linear.
- **At most two extra points.** The leading-order critical points are therefore the pins (`q = 0`) plus
  `{ℓ = 0} ∩ {F_2 = 0}`. A line meets a conic in at most two points.
- **The line and pin degeneracy.** `ℓ(0,0) = 2 det DF(0,0)/T_3` and `ℓ(1,0) = −2 det DF(1,0)/T_3`. So the line passes
  through a pin exactly when that pin is degenerate. On the support of `W_r` (`M` a nondegenerate maximum, `S` a
  saddle) both values have the sign of `T_3`.
- All of this is checked in `c6_check.py`. It is why `Θ(r³)` is expected: extra critical points appear near the pins
  in at most pairs, on the event `S_0 = O(r)`, which has `Q_r^W`-probability `O(r³)`.

**Palm route to `O(r³)`.** Since `N(N−1) ≤ NΨ`, the weighted Kac–Rice formula with the global Borel mark `Ψ` gives
`E N(N−1) ≤ ∫ ρ_1^{Ψ}(X) dX`. Removing the logarithm therefore reduces to two statements:

- **(M')** Lemma M under the Gaussian conditioning `{E_r = e, ∇f(X) = 0, f(X) = h}`, uniformly in `X` and in
  `h ∈ I_r`. Here `X` may lie in some annulus, where the conditioned `F` vanishes. The density bound near `z = X`
  becomes `min(1, ε⁴/|z−X|^{5})` or similar; this is still integrable with a positive power of `ε` left over, which
  suffices.
- **(H)** The Hölder upgrade of the reviewed first-moment proofs (P2, C1, I3/I4, remote Theorem A). Each bounds the
  intensity by `Z^{−1}∫_{I_r} p(0,h) E[A | ∇f(X) = 0, f(X) = h] dh`, with the determinant product `A` bounded
  pathwise by (geometry)·`K^c`. The marked version replaces `E[K^c|·]` by `E[K^{cp}|·]^{1/p}·E[Ψ^{q}|·]^{1/q}`.

(M') plus (H) give `E N(N−1) ≤ C r³`, hence `Θ(r³)`. Neither is claimed here.

## 10. Finite companion

`c6_check.py` (stdlib, exact rationals where possible) checks:
- the elimination identity and the pin-degeneracy values of `ℓ` on a rational grid;
- a rational instance with exactly two extra leading-order critical points, so the cap `4` is attained;
- the geometric remainder `Σ_{k>m} 2^{−k} = 2^{−m}`;
- the packing count (6.2);
- the radial integral `∫_{|y|≤R} min(1, ε⁴/|y|²) = πε⁴(1 + 2 ln(R/ε²))` and its logarithmic growth;
- the exponent arithmetic of (c) and §8 at `r = 2^{−k}`.

Mutants `wrong-elimination`, `touching-balls`, `no-log`, `short-remainder` must fail.

## 11. Scope

**Claimed:** Theorem C6-L, Lemmas R, M, D and E, at existential constants for fixed `T` and compact marks.

**Not claimed:**
- `Θ(r³)`;
- numerical constants;
- uniformity in `T` or as `k ↓ 0`;
- `d > 2`;
- elder pairing;
- any status for (I5) beyond the D5 reading rule (§1), in particular nothing that bypasses the (P2) continuum HOLD;
- any STATUS, GRAPH or catalog change.

**Prior art.** Finiteness of moments of critical-point counts for nondegenerate Gaussian fields is due to Gass and
Stecconi (arXiv:2305.17586; Probab. Theory Relat. Fields 2024). Lemma M is a uniform tail bound for the analytic
pinned family. No novelty claim is made.
