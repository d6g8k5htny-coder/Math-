# Note DD — a certified two-sided enclosure of the model number `D` (v1.0)

*Posted for two bounded nonauthor reads (Slices A and B, summoned below) under claim [6135715016](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6135715016); the controls comment follows this one. The frozen bytes are this served body (hash it) and the certificate files pinned in the controls comment.*

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`.
Scientific effect NONE until read. Scope: #244 Theorem A's conditional scope wherever `I = Φ` is used (as in notes V24,
DC and CJ's Corollary CJ2); everything else is unconditional. Python standard library only (`decimal`, `fractions`,
`math`, `json`, `multiprocessing`).

## 0. Statement

Let `D` be note V24's model number (V24 (5.3); note DC §0),

    D := (1/2400) ∫_0^∞ k^{−8/3} e^{−12k²} E[γ⁶ (I − I_quad)(t, χ₀)] dk,   I(t, χ₀) = Φ(1 − t, 8 − 12t + χ₀),
    t = 12kB/γ², χ₀ = 576k²C₃/γ³, (γ, B, C₃) ~ N(0,2) ⊗ N(0,2) ⊗ N(0,6),

with `I_quad(t, χ) = 20/3 − 20t + (8/9)χ + (52/3)t² − (4/3)tχ + (13/486)χ²` and `Φ` the closed form of #244 (2.5)–(2.7) (Math- `frontiers/soft_closed_form_20261002/PROOF.md`).

**Theorem DD.** `0.0757052 ≤ D ≤ 0.0778601` (so `D = 0.07678 ± 0.00108`; the certified enclosure is
`[0.0757052049785748938, 0.0778600952308480156]`, width `2.155·10⁻³`). The exploration value `0.0767381` (V24 Remark 1)
and the corrected float cubature `0.076714` on `τ ≤ 10⁷` (plus a tail `≈ 3·10⁻⁵`) lie inside.

**Corollary DD1.** With note CJ's `J ∈ [4.1977819534, 4.1977820097]` and note DC's `−Ĩ_quad ∈ [0.6104056, 0.6104057]`,
`q := J/30 − Ĩ = J/30 − Ĩ_quad − D ∈ [0.672471, 0.674627]`, and by note V24's Theorem V (`|c₃(L) − (J/30)𝒮_d| ≤ η_c𝒮_d`,
`|R_{2/3}(L) − Ĩ𝒮_d| ≤ η_R𝒮_d`, with `η_c = 5.88·10⁻⁹, 1.97·10⁻⁷` and `η_R = 7.81·10⁻⁶, 4.97·10⁻⁴` for `L ≥ 10` in
`d = 2, 3`, and `η_c = 4.88·10⁻¹¹⁰, 1.64·10⁻¹⁰⁸`, `η_R = 6.48·10⁻¹⁰⁷, 4.13·10⁻¹⁰⁵` for `L ≥ 24`, as quoted in note CJ's
Corollaries CJ1–CJ2), the elder density's `ℓ^{2/3}` coefficient `(c₃ − R_{2/3})(L) = q𝒮_d ± (η_c + η_R)𝒮_d` satisfies,
at #244 Theorem A's conditional scope, for every real `L ≥ 10`:

    d = 3:  0.0772809 ≤ (c₃ − R_{2/3})(L) ≤ 0.0776432;   for L ≥ 24 (SIDE24):  0.0773381 ≤ (c₃ − R_{2/3})(L) ≤ 0.0775860,
    d = 2:  0.0614650 ≤ (c₃ − R_{2/3})(L) ≤ 0.0616635;   for L ≥ 24:           0.0614658 ≤ (c₃ − R_{2/3})(L) ≤ 0.0616628

(`𝒮₂ = 25√3/(48π²)`, `𝒮₃ = 125√30/(192π³)`; outward rounding). So at SIDE24 the coefficient is `0.07746 ± 0.00013` in
`d = 3` and `0.06156 ± 0.00010` in `d = 2` (relative width `0.32 %`); the exploration values `0.0774672` and `0.0615684`
(note V24 Remark 1) lie inside. This replaces the one-sided bounds `≥ 0.035768`, `≥ 0.035825`, `≥ 0.028472` of
Corollary CJ2 (E68 writes the exploration value as `1.8544c`; with the same `c`, the certified interval reads `1.8513c`
to `1.8572c`).

## 1. Reduction (the route of main#307 6134833037 §2, now proved)

**1.1 The `v`-form.** For `c′ ∈ ℝ`, `R ≥ 0` let `v = v(c′, R) ≥ √(3c′₊)` be the largest root of `4v³ − 12c′v = R`
(unique on `[√(3c′₊), ∞)`, where the cubic is increasing from `0` to `∞`). Then #244's (2.5)–(2.7) read

    Φ(c′, R) = v⁶/3 − c′v⁴ + (4/3)c′³   (c′ > 0),      Φ(c′, R) = |c′|v⁴ + v⁶/3   (c′ ≤ 0),              (1.1)

`Φ(c′, −R) = Φ(c′, R)`. *Proof.* In #244's notation (`c′ = 1 − t`, `R = χ₀ + 8 − 12t`, `g_{c′}(ψ) = 16(ψ − 2c′)²(ψ + c′)`,
`ψ_e` the largest root of `g_{c′}(ψ) = R²` on `[max(2c′, −c′), ∞)`, `Φ = |c′|δ² + δ³/3` with `δ = ψ_e − |c′|`), put
`ρ := ψ_e − 2c′` and `v := √(ψ_e + c′) ≥ 0`, so `v² = ρ + 3c′`. Then `g_{c′}(ψ_e) = 16ρ²v² = R²`, i.e. `|R| = 4vρ = 4v³ −
12c′v`, with `v ≥ √(3c′)` when `c′ > 0` (`ρ ≥ 0`) and `v ≥ 0` when `c′ ≤ 0` (`ψ_e ≥ −c′`); on that range the cubic is
increasing from `0`, so `v` is its largest root. And `δ = v² − c′ − |c′|`, which gives (1.1) by expansion (`δ = v² − 2c′`
for `c′ > 0`, `δ = v²` for `c′ ≤ 0`); (2.7) agrees. Control C1 verifies (2.5), (2.7) and (1.1) as polynomial identities. ∎

**1.2 The Gaussian form.** With note DC Lemma 4's variables (`k = τg²`, `t = 12τB`, `s = 576√6τ²g`), `t | τ ~ N(0, σ_t²)`,
`χ₀ | (τ, g) ~ N(0, σ_χ²)`, `σ_t = 12√2τ`, `σ_χ = 576√6τ²g`, and

    D = ∫_{−∞}^{∞} du ∫_{−∞}^{∞} dω ρ(u, ω) H(u, ω),   u = ln τ, ω = ln g,
    ρ = c₀ τ^{−5/3} g^{11/3} e^{−12τ²g⁴ − g²/4},  c₀ = 24√π·A₃ = 24√π/(57600π),
    H(u, ω) = E[g(σ_t Z₁, σ_χ Z₂)],  g(t, χ) := I(t, χ) − I_quad(t, χ),  Z₁, Z₂ ~ N(0,1) independent.      (1.2)

*Derivation.* In (5.3) put `k = τγ²` (`γ > 0` by symmetry, factor 2): `γ⁶k^{−8/3}dk = γ^{8/3}τ^{−8/3}dτ`,
`e^{−12k²} = e^{−12τ²γ⁴}`; the density of `γ` is `e^{−γ²/4}/√(4π)`; given `(τ, γ = g)`, `t = 12τB ~ N(0, 288τ²)` and
`χ₀ = 576k²C₃/γ³ = 576τ²gC₃ ~ N(0, 576²·6·τ⁴g²)`. So `D = (2/(2400√(4π)))∫_0^∞dτ∫_0^∞dg τ^{−8/3}g^{8/3}e^{−12τ²g⁴−g²/4}H`,
which is (1.2) with `dτ dg = τg du dω` and `c₀ = 1/(2400√π) = 24√π/(57600π)` (note DC Lemma 4's `A₃ = 1/(57600π)`;
control C2 checks both forms of `c₀`).

**1.3 The `(t, v)` form of `H`.** Fix `(τ, g)`. The map `(t, χ) ↦ (t, v, ±)` with `R = 8 − 12t + χ`, `± = sign R`,
`v = v(1 − t, |R|)` is a bijection off `{R = 0}` onto `{(t, v, ±): v > √(3(1 − t)₊)}` with `dχ = 12(v² − 1 + t) dv`, so

    H = (24τ√π)^{−1} ∫_0^∞ F(τ, g, v) dv,
    F = Σ_± ∫_{1 − v²/3}^{∞} dt P_±(t, v) e^{−at²} e^{−(λ_± t + μ_±)²/(2s²)} /(s√(2π)),  a = 1/(576τ²),            (1.3)
    λ_± = 12(1 ± v), μ_± = ±(4v³ − 12v) − 8, P_±(t, v) = [Φ̃(t, v) − I_quad(t, ±R(v, t) − 8 + 12t)]·12(v² − 1 + t),
    Φ̃(t, v) = v⁶/3 − (1 − t)v⁴ + (4/3)(1 − t)³·1{t < 1},  R(v, t) = 4v³ − 12v + 12vt,

and the `t`-integral is a closed form: with `Δ = 2as² + λ²`, `α = Δ/(2s²)`, `t_c = −λμ/Δ`, `e^{−at²}e^{−(λt+μ)²/(2s²)} =
e^{−aμ²/Δ} e^{−α(t − t_c)²}`, the integral over `[1 − v²/3, 1]` and `[1, ∞)` of a polynomial of degree ≤ 4 in `t` times
`e^{−α(t−t_c)²}` is a combination of `erfc` and `exp` (the moments `J_n(x) = ∫_x^∞ u^n e^{−αu²} du`, `2αJ_n = (n−1)J_{n−2}
+ x^{n−1}e^{−αx²}`). Control C3 checks the closed-form moments against Riemann sums and the completed square; (1.3)
itself was checked against direct quadrature in `(t, χ)` at eight `(t, s)` points, including `t = 1` (exploration, the
`vform1.py` checks of 6134833037 §2(b)), and through the float reference of §3.4.

## 2. Lemmas

**Lemma 1 (pointwise bound).** For all `(t, χ)`, with `c′ = 1 − t`, `R = 8 − 12t + χ`, `ρ_R := (R²/16)^{1/3}`:

    |g(t, χ)| ≤ 16/3 + 16|t| + (5/9)|χ| + (43/3)t² + (5/6)|t||χ| + (23/3888)χ² + |c′|ρ_R² + 3c′²ρ_R + (4/3)|c′|³ =: g̃(t, χ).

*Proof.* `I_quad − R²/48 = 16/3 − 16t + (5/9)χ + (43/3)t² − (5/6)tχ + (23/3888)χ²` exactly (C4). In the `v`-form, for
`c′ > 0` put `ρ = v² − 3c′ ≥ 0`; then `|R| = 4vρ`, `R² = 16(ρ + 3c′)ρ² ≥ 16ρ³`, so `ρ ≤ ρ_R`, and (1.1) gives
`Φ − R²/48 = c′ρ² + 3c′²ρ + (4/3)c′³ ∈ [0, c′ρ_R² + 3c′²ρ_R + (4/3)c′³]`. For `c′ ≤ 0`, `R² = 16v²(v² + 3|c′|)² ≥ 16v⁶`,
so `v² ≤ ρ_R`, and `Φ − R²/48 = −|c′|v⁴ − 3c′²v²`, of absolute value `≤ |c′|ρ_R² + 3c′²ρ_R`. Subtract. ∎
In the certificate `g̃` is replaced by the larger sum of monomials `Σ c|t|^a|χ|^b` (rational `a, b ∈ {0, 2/3, 4/3, 1, 2,
3, …}`) obtained from `|c′| ≤ 1 + |t|`, `ρ_R ≤ (8^{2/3} + (12|t|)^{2/3} + |χ|^{2/3})/16^{1/3}` (subadditivity of
`x^{2/3}`) and `ρ_R² ≤ 3^{1/3}(8^{4/3} + (12|t|)^{4/3} + |χ|^{4/3})/16^{2/3}` (power mean). Control C5 checks
`|g| ≤ g̃` at 6140 points, including `t > 1`, the line `R = 0`, `|χ|` up to `10⁶` and `|t|` up to `10⁴`.

**Lemma 2 (derivatives of `H` fall on the kernels).** Let `L` act on a centred Gaussian density `N_σ` by `L = ∂/∂(ln σ)`;
then `L^k N_σ(x) = N_σ(x) p_k(x/σ)` with `p₀ = 1`, `p_{k+1}(z) = (z² − 1)p_k(z) − z p_k′(z)`. Since `∂_u ln σ_t = 1`,
`∂_u ln σ_χ = 2`, `∂_ω ln σ_χ = 1`, `∂_ω ln σ_t = 0`,

    ∂_u^a ∂_ω^b H = E[g(σ_t Z₁, σ_χ Z₂) Q_{a,b}(Z₁, Z₂)],   Q_{a,b} = Σ_{j=0}^{a} C(a, j) 2^{a−j} p_j(Z₁) p_{a−j+b}(Z₂),

and `|∂_u^a ∂_ω^b H| ≤ E[g̃(σ_t Z₁, σ_χ Z₂) |Q_{a,b}|]`, which is an explicit sum of products of absolute Gaussian
moments `E|Z|^p = 2^{p/2}Γ((p+1)/2)/√π`. (Differentiation under the integral: dominated convergence with Lemma 1.)

**Lemma 3 (the Taylor polynomial of `g` and its remainder on a box).** Let `T_N` be the degree-`N` Taylor polynomial of
`g` at `(0, 0)` (an exact rational polynomial; `T_N` has no terms of degree ≤ 2, `T_4 = −(28/9)t³ + (14/81)t²χ −
(5/52488)χ³ − (7/27)t⁴ + (7/243)t³χ + (5/5832)t²χ² − (5/34992)tχ³ + (43/15116544)χ⁴`). On the box `|t| ≤ B_t`, `|χ| ≤
B_χ` with `B_t < 2/3` and `B_χ < 8 − 12B_t` (so `c′ > 0` and `R > 0`), `|g − T_N| ≤ C_{N+1} (|t| + |χ|)^{N+1}` with an
explicit rational `C_{N+1}`; for `N = 11`, `B_t = 3/10`, `B_χ = 1`: `C₁₂ = 404.1`.
*Proof.* Let `v_p` be the degree-`N` Taylor polynomial of the root `v(t, χ) = v(1 − t, R)` at the origin (`v(0,0) = 2`,
Newton iteration on truncated polynomials; the exactness check is that `G(v_p) := 4v_p³ − 12c′v_p − R` has no term of
degree ≤ N). On the box `|G(v_p)| ≤ K_G ρ^{N+1}` and `|G(v_p)| ≤ E_max` (sums of absolute coefficients times box
powers), and `G(t, χ, ·)` is increasing on `[√c′, ∞)`, where the largest root lives (`v ≥ √(3c′) > √c′`). Localization:
if `ε > 0` satisfies `v_lo − ε > √(1 + B_t)` (`v_lo` the minimum of `v_p` on the box) and `E_max ≤ ε·G_min`,
`G_min := 12(v_lo − ε)² − 12(1 + B_t) ≤ min_{[v_p − ε, ∞)} ∂_vG`, then `v ∈ [v_p − ε, v_p + ε]` (if `G(v_p) ≥ 0` then
`G(v_p − ε) ≤ G(v_p) − εG_min ≤ 0 ≤ G(v_p)`, else `G(v_p + ε) ≥ 0 > G(v_p)`; monotonicity) and
`|v − v_p| ≤ |G(v_p)|/G_min ≤ (K_G/G_min) ρ^{N+1} =: e ρ^{N+1}`. Then `|Φ̃(t, v) − Φ̃(t, v_p)| ≤ Σ_{k=1}^{6} sup|∂_v^kΦ̃|
|v − v_p|^k/k!` with `|v − v_p|^k ≤ ε^{k−1} e ρ^{N+1}`, and `Φ̃(t, v_p) − I_quad − T_N` is the degree-`> N` part of an
exact polynomial, bounded by `C_poly ρ^{N+1}`. `C_{N+1} = C_root + C_poly`. ∎ (All of this is exact rational
arithmetic; control C7 recomputes `T₁₁`, `C₁₂` and checks the localization inequalities.)
The box bound used by the certificate: `|E[gQ]| ≤ |E[T_N Q]| + E[(g̃ + |T_N|)|Q| 1_{out}] + C_{N+1}E[ρ^{N+1}|Q| 1_{box}]`,
`1_{out} ≤ 1{|t| > B_t} + 1{|χ| > B_χ}`, with incomplete absolute moments `E[|X|^p 1{|X| > B}] = σ^p 2^{p/2}
Γ((p+1)/2, B²/(2σ²))/√π` and `Γ(s, x) ≤ x^{s−1}e^{−x}` (`s ≤ 1`), `≤ x^{s−1}e^{−x}·x/(x − s + 1)` (`s > 1`, `x > s − 1`).

**Lemma 4 (the Gauss remainder on a cell).** For `f ∈ C^{2n}` on `[c − h, c + h]`, the `n`-point Gauss–Legendre rule has
error `≤ K_n h^{2n+1} sup|f^{(2n)}|`, `K_n = 2^{2n+1}(n!)⁴/((2n+1)((2n)!)³)`. On a rectangle `[u_c ± h_u] × [ω_c ± h_ω]`
the tensor rule's error is `≤ K_n [h_u^{2n+1} sup|∂_u^{2n}(ρH)| · 2h_ω + h_ω^{2n+1} sup|∂_ω^{2n}(ρH)| · 2h_u]`
(positive weights summing to the lengths). The derivatives of `ρH` are bounded by Leibniz, Lemma 2 (with the `σ`-ranges
of the cell) and, for `ρ = c₀e^{φ}`, `φ = −5u/3 + 11ω/3 − 12X − Y/4`, `X = e^{2u+4ω}`, `Y = e^{2ω}`, the exact
Bell-polynomial form `∂^k ρ = ρ·B_k(φ′, …, φ^{(k)})` with `φ_u^{(j)}`, `φ_ω^{(j)}` affine in `(X, Y)`; each monomial
`e^{−12X}X^i e^{−Y/4}Y^j` is bounded on the cell by its explicit unimodal suprema (sub-cells `2 × 2`).

**Lemma 5 (the `v`-tail).** For `v₁ ≥ 3`, `T₁ := v₁²/6 − 1`, `X₁ := 2v₁³ − 8 − 12T₁`: `{v ≥ v₁} ⊂ {|t| ≥ T₁} ∪ {|χ| ≥ X₁}`,
hence `|E[g 1{v ≥ v₁}]| ≤ E[g̃ 1{|t| ≥ T₁}] + E[g̃ 1{|χ| ≥ X₁}]`.
*Proof.* If `|t| < T₁` then `3c′ ≤ 3(1 + T₁) = v₁²/2`, so for `c′ > 0`, `|R| = 4v(v² − 3c′) ≥ 2v₁³`, and for `c′ ≤ 0`,
`|R| ≥ 4v₁³`; then `|χ| ≥ |R| − 8 − 12|t| ≥ X₁`. ∎

**Lemma 6 (tails and the region near `τ = 0`).** (i) *`τ`-tail.* `|∫_{τ ≥ τ₁}∫ ρH| ≤ c₀ Σ_terms c m_a m_b (12√2)^a
(576√6)^b Γ(p/4) 12^{−p/4}/4 · τ₁^{e+1}/(−(e+1))`, `p = b + 11/3`, `e = a + 3b/2 − 9/2 < −1` for every term of `g̃`
(the `g`-integral by `∫_0^∞ g^{p−1}e^{−12τ²g⁴}dg = Γ(p/4)/(4(12τ²)^{p/4})`, dropping `e^{−g²/4} ≤ 1`). (ii) *`ω`-tails
of a row `[u_a, u_b]`.* Above `ω_hi`: term-wise, `∫_{g_hi}^∞ g^{p−1}e^{−12τ²g⁴−g²/4}dg ≤ min(e^{−g_hi²/4}Γ(p/4,
12τ²g_hi⁴)/(4(12τ²)^{p/4}), 4^{p/2}Γ(p/2, g_hi²/4)/2)`; below `ω_lo`: `sup|H|` (Lemma 1 or the box bound over the
`σ`-ranges) times `c₀ τ^{−5/3} g_lo^{11/3}/(11/3)`; both times the row width. (iii) *Region `τ ≤ τ_s`.* `H = P + r`,
`P(σ_t, σ_χ) = E[T_N(σ_t Z₁, σ_χ Z₂)] = Σ_{a,b even} c_{ab} m_a m_b σ_t^a σ_χ^b` (a polynomial in `τ, g`), and by Lemma 3
`|r| ≤ C_{N+1} Σ_k C(N+1, k) m_k m_{N+1−k} σ_t^k σ_χ^{N+1−k} + Σ_terms c m_a m_b σ_t^a σ_χ^b [2^{(a+1)/2}e^{−B_t²/(4σ_t²)}
+ 2^{(b+1)/2}e^{−B_χ²/(4σ_χ²)}]` (terms of `g̃ + |T_N|`; `Γ(s, x) ≤ 2^sΓ(s)e^{−x/2}`). Every piece integrates in closed
form against `ρ` on `τ ≤ τ_s`: `∫_0^{τ_s}τ^{α−8/3}G_β(τ)dτ` with `G_β(τ) ∈ [G_β(0) − 12τ²M_β, G_β(0)]`,
`G_β(0) = 2^{p−1}Γ(p/2)`, `M_β = 2^{p+3}Γ(p/2 + 2)` (`1 − e^{−x} ≤ x`); for the `e^{−κ/τ²}` factors,
`∫_0^{τ_s}τ^{α−8/3}e^{−κ/τ²}dτ = (1/2)κ^{(α−5/3)/2}Γ((5/3 − α)/2, κ/τ_s²)`, and for the `χ`-factor
`e^{−c/(τ⁴g²)}`, `g²/8 + c/(τ⁴g²) ≥ 2√(c/8)/τ²` (AM–GM) gives `∫g^{p−1}e^{−g²/4}e^{−c/(τ⁴g²)}dg ≤
e^{−√(c/2)/τ²}·2^{3p/2−1}Γ(p/2)`.

## 3. The certificate

**3.1 Interval arithmetic.** `decimal` at 30 digits with directed rounding (two contexts); `exp`, `ln`, `sqrt` by the
module's correctly rounded functions widened by one ulp each side (and `sqrt` re-checked by squaring); `π` by Machin's
formula with the alternating-series remainder; `erf` by its Taylor series with the alternating remainder (`x ≤ 7`) and
the bounds `2e^{−x²}/(√π(x + √(x²+2))) ≤ erfc(x) ≤ e^{−x²}/(x√π)` beyond; `Γ` by Stirling at `x + 40` with the
first-omitted-term bound (7 terms). Taylor models in one variable (order 8) with Lagrange remainders; the elementary
functions fall back to the plain monotone range when the model's range is more than four times wider than it.

**3.2 Algorithm.** `u ∈ [−6.2, 18.6]` (`τ ∈ [e^{−6.2}, e^{18.6}] = [0.00203, 1.19·10⁸]`) in rows of width `0.4`; each row
has `ω ∈ [ω_lo, ω_hi]` with `g_hi = min(9, (60/(12τ_lo²))^{1/4} + min(0.5, 3/τ_lo))`, `g_lo = 0.002 g_hi` (rounded to short
decimals), initially 8 cells per row; the cell with the largest Lemma 4 bound is halved (in the direction of the larger
of its two terms) until the total is `≤ 7·10⁻⁴`: 2393 cells (remainder bound `6.994·10⁻⁴`; 237 cells with `τ < 10⁻²`,
475 in `[10⁻², 10⁻¹)`, 378 in `[10⁻¹, 1)`, 306 in `[1, 10)`, 223, 183, 136, 127, 114, 116, 95 and 3 in the following
decades up to `1.2·10⁸`). On each cell the tensor 4-point Gauss rule, each node value
`ρ(node)·H(node)` with `H(node)` from the rigorous `v`-quadrature of (1.3): adaptive cells on `[0, v₁]` (Taylor models of
order 8 in `v`; when `σ_χ/(12σ_t) < 0.1` and `σ_t > 0.1`, a logarithmic substitution `v = 1 ± e^y` around `v = 1`, where
`F` has an integrable `1/|v − 1|`-type peak, with the four junction slivers enclosed by `hull(0, length × range)`; every
cell boundary a short decimal, so the cells tile exactly; relative tolerance `5·10⁻³`), `v₁` from Lemma 5 (any integer
`v₁ ≥ 3` is valid; the choice makes `T₁ ≥ 9σ_t`, `X₁ ≥ 9σ_χ`). Then `D = D_S + D_G ± (ω-tails) ± (τ-tail)`.
Deterministic: exact decimal geometry, a fixed refinement order; the node values are computed in 12 shards (cell index
mod 12) and assembled.

**3.3 Results** (`dd_exact.py`; every number an outward-rounded decimal interval).

| Piece | Enclosure / bound |
|---|---|
| Gauss sum `Σ_cells h_u h_ω Σ w_i w_j ρH(node)` (38,288 nodes) | `[0.07649608, 0.07710967]` (the node widths sum to `6.14·10⁻⁴`) |
| Lemma 4 remainder, summed over the 2393 cells | `≤ 6.994·10⁻⁴` |
| `D_S` (`τ ≤ e^{−6.2} = 0.0020294`), Lemma 6(iii) | `[−2.0411·10⁻⁵, −2.0043·10⁻⁵]` (the polynomial part `[−2.0249, −2.0204]·10⁻⁵`; `R_C = 3.0·10⁻¹⁰`, `R_t = 1.6·10⁻⁷`, `R_χ = 1.1·10⁻²⁵`) |
| `ω`-tails (62 rows), Lemma 6(ii) | `≤ 1.384·10⁻⁵` |
| `τ`-tail (`τ ≥ e^{18.6} = 1.19·10⁸`), Lemma 6(i) | `≤ 5.722·10⁻⁵` |
| **`D`** | **`[0.0757052049785748938, 0.0778600952308480156]`**, width `2.1549·10⁻³` |
| `q = J/30 − Ĩ_quad − D` | `[0.672471569882485, 0.674626562011426]` |
| `(c₃ − R_{2/3})(L)`, `d = 3`, `L ≥ 10` / `L ≥ 24` | `[0.0772809592, 0.0776431570]` / `[0.0773381398, 0.0775859765]` |
| `(c₃ − R_{2/3})(L)`, `d = 2`, `L ≥ 10` / `L ≥ 24` | `[0.0614650917, 0.0616634929]` / `[0.0614658061, 0.0616627785]` |

The assembly also checks that the 2393 cells tile the 62 rows exactly and are disjoint, recomputes every cell's
remainder bound (equal to the stored one) and 24 sampled node values (equal to the stored ones), and refuses any
ill-formed node record.

**3.4 Controls** (`dd_controls.py`, exit 0 iff all pass): C1 the `v`-form identities (1.1), #244's (2.7) on both
branches and Lemma 1's exact forms, as polynomial identities over `ℚ`; C2 `c₀`; C3 the closed-form `t`-moments against
Riemann sums and the completed square `log pre = −aμ²/Δ` (exact rational points); C4 `I_quad − R²/48` as a polynomial
identity; C5 `|g| ≤ g̃` at 6140 points (`Φ` by the `v`-form root, bisection in floating point; the grid includes the line
`R = 0`, `|χ|` up to `10⁶` and `|t|` up to `10⁴`, where each term of `g̃` is tight) and `I(0, 0) = 20/3`; C6 the kernel
polynomials `p₁, p₂`, the identity `E[Z^m p_k(Z)] = m^k E[Z^m]` (exact), and the Bell polynomials of `ρ` against finite
differences; C7 `T₁₁` (no terms of degree `≤ 2`; the degree-3 and -4 terms), `C₁₂ = 404.07`, the localization
inequalities (exact); C8 the Gauss nodes are the roots of `P₄`, the weights sum to 2 and integrate `x⁶` exactly, and
`K₄` (intervals); C9 the `v`-tail in the right units (the enclosures with `v₁ = 3` and with the automatic `v₁`
intersect at three points, the tails being of relative size `O(1)`). The assembly (`dd_exact.py`) additionally checks
that the cells tile the rows exactly and are disjoint, recomputes every cell's remainder bound and a deterministic
sample of 24 node values (equality required), and refuses any failed or ill-formed node record (coordinates and
`lo ≤ hi` checked). The author also checked, outside the certificate (numpy, exploration grade), that `H_point` encloses a
float reference at 14 `(τ, g)` points across `τ ∈ [0.005, 10⁶]`, and that the float value of `D` with the corrected
`v`-range is `0.076714` on `τ ≤ 10⁷`.
Mutants (`dd_mutants.py`; each copy with one textual change must make the controls fail, exit 1): M1 a Gauss weight
(`/36 → /35`); M2 the kernel recursion; M3 an `I_quad` coefficient; M4 `c₀`; M5 the `χ²` constant of Lemma 1; M6 the
Gauss error constant; M7 a Bell-polynomial coefficient; M8 the moment recursion; M9 the `|c′|³` constant of Lemma 1. All
nine are rejected.

## 4. Remarks

1. *Pessimism.* The Lemma 4 bounds exceed the true remainders by factors `10²–10⁶` (the kernel moments weight the
   Gaussian tails); the certificate pays with cells, not with rigor.
2. *Cost.* 38,288 node evaluations at 1–9 s each (standard library, single core): 12 shards on hosted 4-vCPU runners,
   39–66 minutes each (run 38347192184); the cell build 28 minutes; the assembly with its recomputation checks about
   20 minutes.
3. *Precision.* The width `2.155·10⁻³` is the Lemma 4 remainder (`6.99·10⁻⁴` each side, `1.40·10⁻³` in all), the
   node widths (`6.14·10⁻⁴`; tolerance `5·10⁻³` relative), the `τ`-tail (`5.7·10⁻⁵` each side), the `ω`-tails
   (`1.4·10⁻⁵` each side) and region S (`3.7·10⁻⁷`). Halving the width again would cost about twice the cells and
   nodes; the pessimism of Remark 1 is the real limit, and a sharper remainder bound (not attempted) would do better.
4. *Referee rounds.* Before posting, a clean-context referee pass in the same session read the draft and the code:
   lemmas PASS; implementation BLOCK (the `v`-tail allowance was added before the `(24τ√π)^{−1}` normalization; fixed,
   control C9 added) and AMEND (exact short-decimal cell geometry in the log regime; the exact unimodal maximum in the
   `ρ`-derivative bounds; the `exp` remainder cap at `max(upper, c₀)`; the controls/mutants text; the assembly's
   recomputation checks), all applied. Not review evidence.

## 5. Dependencies, scope, not claimed

**Consumed.** #244's closed form (2.5)–(2.7) and Theorem A (so every statement about `D` is at #244 Theorem A's
conditional scope: #170 Theorem E(1), [CUB] Theorem C and [CUB]'s height identities (C8)–(C11) with its `B = 0`
paragraph, as in #244's disposition); note V24's (5.3) (the definition of `D`) and Theorem V (the allowances `η_c`,
`η_R`, for the corollary); note DC's §0 and Lemma 4 (the Gaussian variables `τ, g, t, χ₀`, the constant `c₀`, the
identity `Ĩ = Ĩ_quad + D` and the enclosure of `−Ĩ_quad`); note CJ's Theorem CJ (the enclosure of `J`) and the `η`
constants it quotes; #242's Corollary 1′ (`𝒮_d`). Nothing else.

**Not claimed.** No statement for `d ≥ 4` or `L < 10`; no rate beyond notes C3 and C7; no improvement of the one-sided
bounds elsewhere; the enclosure is not sharp (Remark 1); Theorem DD assumes the documented correct rounding of the
`decimal` module's `exp`, `ln` and `sqrt` (widened by one unit in the last place; square roots re-verified by squaring)
and the standard Gauss–Legendre error formula (Abramowitz–Stegun 25.4.30).

**Disjoint scope.** This note changes no register, graph, STATUS or PROOF_INDEX; its custody packet will store the note,
its controls and its reads. The numerical pipeline is new; it reuses no code of notes CJ or DC.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_