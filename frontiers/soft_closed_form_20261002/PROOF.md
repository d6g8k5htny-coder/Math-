# The closed form of the soft rejected set: an explicit `I(t, χ₀)`, `t* = 2/3`, and the expansion of `H` to `k⁴`

Object: CL-SOFT-CLOSED-FORM-20261002-v1.
Author: Anthropic Claude (configured model `claude-opus-5-5`), session https://claude.ai/code/session_01NMeKEismAyeqgdB4sy2NJU,
2 October 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE. Theorem A and everything after it are conditional on merged author-side candidates,
at their stated conditional scope:
- #170 Theorem E(1);
- [CUB] Theorem C;
- [CUB]'s height identities (C8)–(C11), with its `B = 0` paragraph.

Nonauthor review is required. Scientific effect: NONE. No register, graph, STATUS, PROOF_INDEX, prize or Boolean change.

## 0. Summary

**The object.** Math- #242 (open) studies the fold-scale soft model. For `φ > 0` and `(t, χ₀) ∈ R²` it is the cubic (#242
(2.3))

    G(X, z) = A₀(X) + ½(X² − ¼)z − ½(1 − βX)z² + (χ/6)z³,    A₀(X) = 2(X + ½)²(X − 1)/(24φ),    β = 2tφ,  χ = χ₀φ².     (0.1)

Its pins are the maximum `M = (−½, 0)` at level `0` and the saddle `S = (½, 0)` at level `L_S = −1/(24φ)`. The configuration is
typed iff `φ < 1/|1 − t|` (#242 (2.4)). It is *elder* (`e = 1`) iff `S` kills `M` in the superlevel filtration of `G`.

#242 defines the rejected set `𝓡(t, χ₀) := {φ ∈ (0, 1/|1 − t|): e = 0}` and

    I(t, χ₀) := ∫_{𝓡(t, χ₀)} φ^{−2}(φ^{−2} − (1 − t)²) dφ                                                            (#242 (2.5))

and computes `I` numerically by a one-dimensional scan. `I` determines:
- the Gaussian fold-scale rejection function `H(k) = e^{−12k²}E[γ⁶I(t, χ₀)]/800` (#242 Proposition 4);
- the coefficient `R_{2/3} = (∫∫F₀ db dσ)·Ĩ`, with `Ĩ = ∫_0^∞ v⁴[H(v^{−3}) − 1]dv` (#242 (4.2)).

**Notation.** Throughout,

    ψ := 1/φ,    c′ := 1 − t,    R := χ₀ + 8 − 12t,    σ := R/8,    g_{c′}(ψ) := 16(ψ − 2c′)²(ψ + c′).                 (0.2)

**What is new.**

| | Statement | Status |
|---|---|---|
| **Theorem A** | For `(t, χ₀)` off the curve `Δ = {σ² = c′³}`, and all but at most three `φ`: the configuration is elder iff `ψ ≥ 2c′` and `R² ≤ g_{c′}(ψ)`. Hence `𝓡(t, χ₀) = (1/ψ_e, 1/\|c′\|)`, where `ψ_e` is the largest real root of `g_{c′}(ψ) = R²` (explicit, (2.6)), and `I(t, χ₀) = Φ(c′, R) := \|c′\|δ² + δ³/3` with `δ = ψ_e − \|c′\|`. | proof, conditional (above) |
| **Corollary A.1** | `χ₀ = 0`: the cubic factors, `ψ_e = 3/2 − 2t + (3/2)√(1 − 4t/3)` for `t ≤ 2/3` and `ψ_e = t` for `t ≥ 2/3`. So `t* = 2/3` exactly: for `t ≥ 2/3` the elder edge is `β = 2`. `I(t, 0)` is elementary, with minimum `4/81` at `t = 2/3`, and `I(t, 0) = t − 2/3` for `t ≥ 1`. The Taylor coefficients of `ψ_e` at `0` are Catalan numbers. | proof (as Theorem A) |
| **Corollaries A.2–A.4** | `I(1, χ₀) = (χ₀ − 4)²/48`. For fixed `t`, `I` is (off `Δ`) a nondecreasing function of `\|R\|`; everywhere `I ≥ (4/3)(1 − t)₊³`, with equality at `χ₀ = 12t − 8`, and `I = 0` exactly on the half-line `t ≥ 1`, `χ₀ = 12t − 8`. `I` has a convex kink along `χ₀ = 12t − 8`, `t < 1`. Exact asymptotics as `t → ±∞` and `\|χ₀\| → ∞`. For `β > 2` and `χ ≤ 0`, every typed configuration is rejected. | proof (as Theorem A) |
| **Theorem B** | `H(k) = 1 + (12/25)k² + h_{7/2}k^{7/2} + (728/25)k⁴ + o(k⁴)`, with `h_{7/2} = 16Γ(9/4)(1728√6 − 4332√2 − 2721)/(2625π) = −10.14404402…`. This is the sharp fractional term that OA-242-C-01 left open, together with the next term. | proof, conditional on Theorem A |

**Prior statements recovered.** #242 obtained the following, by series or numerically:
- `φ_e = 1/3 + t/3 + 10t²/27 + O(t³)`;
- `I(t, 0) = 20/3 − 20t + 52t²/3 + O(t³)`;
- `t* ∈ (0.65, 0.68)`;
- `φ_e|t| → 1/2` and `φ_e|χ₀|^{2/3} → 16^{1/3}`;
- `I(t, 0) ~ (4/3)|t|³` and `I(0, χ₀) ~ χ₀²/48`.

All of these follow from Theorem A, most with exact next terms.

**Numerics** (§5, exploration, outside the repository). Theorem A makes `H` a Gaussian integral of an explicit algebraic
function. Nested Gauss–Legendre quadrature gives:
- `Ĩ = −0.5336676`;
- `R_{2/3} = −0.048779` in `d = 2` and `−0.061375` in `d = 3`.

They lie inside #242 v1.2's stated ranges (`−0.536`, `−0.049 ± 0.003`, `−0.062 ± 0.004`). Most of the difference in `Ĩ`
comes from #242's assembly of `Ĩ`, not from its `H` values (§5).

**Not claimed.**
- No unconditional statement: Theorem A rests on the sources named in the disposition.
- On the curve `Δ`, only what §3 proves separately (the zero set, the minimum over `χ₀`, and `(0, 0)`).
- No field statement. Conjecture 7 of #242 is not addressed.
- No certification of the §5 numbers.
- No change to #242, #243, #170, [CUB] or any other packet.

## 1. Sources

- **#242** (open; consumed at head `b82b0ca`, PROOF blob `ad4beb84`). Used:
  - (2.2)–(2.4): the normalization `φ, t, β, χ₀, χ`, the model (0.1) and typing;
  - the elder rule ("`S` kills `M` in the superlevel filtration of `G`"), read as in Step 1 of Lemma 2's proof: `S` kills
    `M` iff the maximin level of `M` is `L_S`;
  - (2.5): `𝓡` and `I`;
  - Proposition 4: the definition of `H`, with `(γ, B, C₃)` independent `N(0, 2)`, `N(0, 2)`, `N(0, 6)` and
    `(t, χ₀) = (12kB/γ², 576k²C₃/γ³)`;
  - (4.2): `Ĩ`, `R_{2/3}`;
  - §§2, 3 and 5: the values compared.

  Lemma 2's scan is not used. Lemma 3 is compared, not consumed.
- **#170** (merged author-side candidate, OpenAI; `frontiers/local_elder_geometry_20260930/PROOF.md`, blob `ef2aa579`). Used:
  - §2: the typed cubic `P_θ`, the shear quantities `B`, `D`, the null sets `Σ_k`, `Δ_k`, the set `C(P)` of additional
    critical points with values in `(−k, 0)`, and `h_*(P) = max({−k} ∪ P(C(P)))`;
  - **Theorem E(1)**: off `Σ_k ∪ Δ_k`, the maximin connection level of `M` to a point higher than `M` is `h_*(P)`;
  - §3: the critical-chord bound `d_P(M) ≥ h_*(P)`, which holds for every typed cubic. It is used only on `Δ`, in Corollary
    A.2.
- **[CUB]** (merged author-side candidate, OpenAI; `frontiers/planar_cubic_cluster_20260929/PROOF.md`, blob `bb446d08`). Used:
  - §2 (C1)–(C6), **Theorem C**: `n(θ) := #C(P_θ)` satisfies `n = 0` iff `s ≤ B` and `D² ≤ T`, where
    `T = −(s − B)²(B + 2s)/(12k)`. This includes `Δ_k`.
  - the height identities (C8)–(C11) and the `B = 0` paragraph of §2: off `Σ_k`, the only critical points at the heights `0`
    and `−k` are the pins. (This is also used in the proof of [CUB]'s Lemma S.)
- **#243** (open; cited). Its Proposition FL.7 identifies #242's model with #170's cubic in #243's normalization. Lemma 1
  below re-derives that identification in #242's normalization, so this packet does not consume #243.
- **OpenAI Codex's reviews of #242.**
  - The Slice C review (5390667993) proves `H(k) = 1 + (12/25)k² + O(k^{7/2})` (§5 there) and records OA-242-C-01: a sharp
    fractional term would need "analysis of the `γ ≈ √k` transition and a nonzero residual coefficient". Theorem B
    supplies both, conditionally on Theorem A.
  - The complementary v1.2 review (5391986303, §3, D.1) uses the same identification for the coefficient `F = kA∗a_fail`.
- **This packet's clean-context referee** (an Anthropic Claude subagent, same family; report in the project archive)
  contributed three things, credited where they are used:
  - the `k⁴` coefficient of Theorem B, with its two constants;
  - the arguments on `Δ` in Corollary A.2;
  - the decomposition of #242's `Ĩ` error in §5.

## 2. The identification and Theorem A

**Lemma 1 (#242's model is #170's cubic; cf. #243 FL.7).** Fix `φ > 0` and `(t, χ₀)`. Put `k = 1` and

    θ = (s, a, β′, c) := (−1/(24φ), 1, t/12, χ₀/576),                                                                   (2.1)

where `c` is [CUB]'s cubic coefficient, not `c′`. Let `P_θ(X, Z) = 2X³ − 3X/2 − ½ + sZ²/2 + (a/2)(X² − ¼)Z + (β′/2)XZ² +
(c/6)Z³` be #170's typed cubic. Then:
- (i) `G(X, z) = P_θ(X, 24φz)/(24φ)` identically.
- (ii) [CUB]'s shear quantities are

      B := β′ − a²/12 = −c′/12,    D := (c − aβ′/4 + a³/72)/2 = R/1152,    s = −ψ/24,                                (2.2)

  and

      T := −(s − B)²(B + 2s)/12 = (ψ − 2c′)²(ψ + c′)/82944,    1327104(T − D²) = g_{c′}(ψ) − R²,                       (2.3)

      12D² + B³ = (R² − 64c′³)/110592,    12D² + (s − B)²(B + 2s) = (R² − g_{c′}(ψ))/110592.                        (2.4)

  So `θ` is typed (`s < −|B|/2`) iff `ψ > |c′|`, which is #242's typing. Also `θ ∈ Δ₁` iff `σ² = c′³`, and `θ ∈ Σ₁` iff
  `R² = g_{c′}(ψ)`.
- (iii) If `θ` is typed and `θ ∉ Σ₁ ∪ Δ₁`, then `e(G) = 1` iff `n(θ) = 0`.

*Proof.*
- (i) Expand. With `Z = 24φz`:
  - `sZ²/2 = −12φz²`;
  - `(a/2)(X² − ¼)Z = 12φ(X² − ¼)z`;
  - `(β′/2)XZ² = 24tφ²Xz²`;
  - `(c/6)Z³ = 4χ₀φ³z³`.

  Dividing by `24φ` gives `A₀(X) + ½(X² − ¼)z − ½z² + tφXz² + (χ₀φ²/6)z³`, which is (0.1). Here
  `2X³ − 3X/2 − ½ = 2(X + ½)²(X − 1)` (control C1).
- (ii) Substitute (2.1) into [CUB] (C2) and (C5). The identities are polynomial (C1).
- (iii) The map `L(X, z) = (X, 24φz)` is linear and invertible, and fixes `M` and `S`. By (i), `G = (P_θ∘L)/(24φ)`, and
  `24φ > 0`. Paths from `M` to `{G > 0}` correspond under `L` to paths from `M` to `{P_θ > 0}`. Hence the maximin level
  satisfies `d_G(M) = d_{P_θ}(M)/(24φ)`. By #170 Theorem E(1), `d_{P_θ}(M) = h_*(P_θ) ≥ −1`, so
  `d_G(M) = L_S·(−h_*(P_θ))`.
  - Off `Σ₁`, [CUB] (C8)–(C11) and its `B = 0` paragraph make `S` the only critical point at level `−1` and `M` the only one
    at level `0`. Explicitly:
    - a critical value `0` off `Z = 0` would need `u = −½` (which is `M`) or `u = ½ − B/(2s)`, which lies outside the conic's
      real range;
    - a critical value `−1` needs `u = ½` (which is `S`) or `u = u_w` with `D² = T`, that is `Σ₁`.
  - So `S` kills `M` iff `d_G(M) = L_S`, iff `h_* = −1`, iff `C(P_θ) = ∅`, iff `n(θ) = 0`. ∎

Lemma 1 is #243's Proposition FL.7(i)–(iii) with `k = 1` and `γ = 1`. Since `G` depends only on `(φ, β, χ)`, this choice is
no restriction.

**Theorem A (the closed form).** Let `(t, χ₀) ∈ R²` with `σ² ≠ c′³`, and let `φ ∈ (0, 1/|c′|)` with `R² ≠ g_{c′}(1/φ)`; this
excludes at most three values of `φ`. Then

    e = 1   iff   ψ ≥ 2c′  and  R² ≤ 16(ψ − 2c′)²(ψ + c′).                                                            (A)

Let `ψ₀ := max(2c′, −c′)`; note that `ψ₀ ≥ |c′|`. On `[ψ₀, ∞)`, `g_{c′}` increases from `0` to `∞`. Let `ψ_e(t, χ₀)` be its
unique point with `g_{c′}(ψ_e) = R²` (`ψ_e = ψ₀` if `R = 0`); it is the largest real root of `g_{c′}(ψ) = R²`. Then

    𝓡(t, χ₀) = (1/ψ_e, 1/|c′|)  (up to finitely many points),    I(t, χ₀) = Φ(c′, R) := |c′|δ² + δ³/3,    δ := ψ_e − |c′| ≥ 0.   (2.5)

Explicitly, with `y := ψ_e − c′`:

    y = 2c′·cos(⅔·arccos(|σ|c′^{−3/2}))                            if c′ > 0 and σ² ≤ c′³,
    y = A^{2/3} + c′²A^{−2/3},    A := |σ| + √(σ² − c′³),        otherwise (y := 0 if σ = c′ = 0).                      (2.6)

*Proof.*
- **The test.** Off `Δ₁ ∪ Σ₁`, Lemma 1(iii) and [CUB] (C6) give `e = 1` iff `s ≤ B` and `D² ≤ T`. By (2.2)–(2.3), this is
  (A). The excluded `θ` are, by (2.4), `σ² = c′³` and the at most three roots `ψ` of `g_{c′}(ψ) = R²`.
- **Monotonicity.** `g_{c′}′(ψ) = 48ψ(ψ − 2c′)`. This is `> 0` on `(ψ₀, ∞)`: there `ψ > 2c′`, and `ψ > ψ₀ ≥ |c′| ≥ 0`. At
  `ψ₀` one factor of `g_{c′}` vanishes, so `g_{c′}(ψ₀) = 0`.
- **The elder set within the typed range.**
  - For `c′ > 0`, (A) requires `ψ ≥ 2c′ = ψ₀`.
  - For `c′ ≤ 0`, `ψ ≥ 2c′` holds automatically, and typing gives `ψ > −c′ = ψ₀`.
  - In both cases the elder set is `{ψ > |c′|: ψ ≥ ψ₀, g_{c′}(ψ) ≥ R²} = [ψ_e, ∞) ∩ (|c′|, ∞)`.
  - So `𝓡 = {φ: |c′| < 1/φ < ψ_e}`, which is empty iff `ψ_e = |c′|`.
- **The integral.** Under `φ = 1/ψ`, `φ^{−2}(φ^{−2} − c′²)dφ = −(ψ² − c′²)dψ`. So
  `I = ∫_{|c′|}^{ψ_e}(ψ² − c′²)dψ = |c′|δ² + δ³/3`.
- **The roots.** With `ψ = c′ + y`, `g_{c′}/16 = (y − c′)²(y + 2c′) = y³ − 3c′²y + 2c′³`. So `g_{c′}(ψ) = R²` reads
  `y³ − 3c′²y + 2c′³ − 4σ² = 0`.
  - Its discriminant is `432σ²(c′³ − σ²)` (C2).
  - For `c′ > 0` and `σ² ≤ c′³` all roots are real. Viète's form `y = 2c′cos(⅓arccos(2σ²/c′³ − 1) − 2πm/3)` gives the
    largest for `m = 0`. Since `arccos(2x² − 1) = 2arccos x` on `[0, 1]`, this is (2.6).
  - Otherwise, Cardano's formula gives the largest real root.
    - Generically there is one simple real root.
    - When `σ = 0 < −c′`, there is also a double root `y = c′` below it, and Cardano's value is `2|c′|`.
    - The two cube roots are `A^{2/3}` and `(c′³/A)^{2/3}`, because `(|σ| ± √(σ² − c′³))² = 2σ² − c′³ ± 2|σ|√(σ² − c′³)` and
      the product of the two is `c′³`.
  - On `σ² = c′³` both formulas give `y = 2c′`. ∎

**Remarks.**
1. *The parameters.* Only `(t, χ₀)` enters; `k` and `γ` have been scaled out by #242's normalization. In #242's Gaussian
   setting, `(t, χ₀)` has a density, so `Δ` and the excluded `φ` do not affect `I` or `H`.
2. *The point `(0, 0)` lies on `Δ`.* There #242 proves `I(0, 0) = 20/3` directly (elder iff `φ < 1/3`). (2.5) gives `ψ_e = 3`
   and `I = 20/3` there too.
3. *A second form.* Using the cubic for `y`, (2.5) is equivalent to

       Φ(c′, R) = R²/48 + c′y(y + c′) + (2/3)|c′|³ − (4/3)c′³,    y = ψ_e − c′                                     (2.7)

   (C4). At `(0, 0)`: `64/48 + 6 + 2/3 − 4/3 = 20/3`.
4. *A bound.* On `[ψ₀, ∞)`, `g_{c′}(ψ) ≥ 16(ψ − ψ₀)³`, because `ψ − 2c′ ≥ ψ − ψ₀` and `ψ + c′ ≥ ψ − ψ₀`. So
   `ψ_e ≤ ψ₀ + (R²/16)^{1/3}`, `δ ≤ |c′| + (R²/16)^{1/3}`, and

       Φ(c′, R) ≤ C(|c′|³ + R²).                                                                                        (2.8)

   This is the counterpart of #242 Lemma 3's `I ≤ (8000/3)max(1, |t|³, χ₀²)`.

## 3. Consequences

Write `I₀(t) := Φ(1 − t, 8 − 12t)`. On the line `χ₀ = 0`, the curve `Δ` meets only `t = 0` and `t = 3/4`, because
`σ² − c′³ = t²(t − 3/4)` there. By Theorem A, `I(t, 0) = I₀(t)` for `t ∉ {0, 3/4}`. By Remark 2 it also holds at `t = 0`.

**Corollary A.1 (`χ₀ = 0`).** Here `R = 4(2 − 3t)`, and

    (ψ − 2c′)²(ψ + c′) − (2 − 3t)² = (ψ − t)(ψ² + (4t − 3)ψ + 4t² − 3t),                                               (3.1)

with roots `t` and `ψ_± = 3/2 − 2t ± (3/2)S`, where `S := √(1 − 4t/3)` (real for `t ≤ 3/4`). Hence:

    ψ_e(t, 0) = 3/2 − 2t + (3/2)√(1 − 4t/3)   (t ≤ 2/3),        ψ_e(t, 0) = t   (t ≥ 2/3).                                (3.2)

    I₀(t) = 11/3 − 21t/2 + 17t²/2 − 4t³/3 + (3/2)(1 − t)(2 − 3t)√(1 − 4t/3)      (t ≤ 2/3),
    I₀(t) = (2t − 1)²(2 − t)/3                                                (2/3 ≤ t ≤ 1),                             (3.3)
    I₀(t) = t − 2/3                                                           (t ≥ 1).

In particular:
- **The edge switch is at exactly `t* = 2/3`.** For `t ≥ 2/3`, `t ≠ 3/4`, the elder edge is `φ_e = 1/t`, that is `β = 2`.
  #242 §2 (the numerical list after Lemma 3) located `t*` in `(0.65, 0.68)`.
- `I₀` is strictly decreasing on `(−∞, 2/3]` and strictly increasing on `[2/3, ∞)`. Its minimum is `I₀(2/3) = 4/81`.
  - At `t = 2/3` it has a convex kink, with slopes `−13/9` and `5/9`.
  - It is `C²` at `t = 1`, with `I₀′ = 1` and `I₀″ = 0`, but not `C³`.
- **The Catalan series.** For `−3/4 < t ≤ 2/3`, with `C_m` the Catalan numbers `1, 1, 2, 5, 14, …`,

      ψ_e(t, 0) = 3 − 3t − Σ_{m≥1} C_m t^{m+1}/3^m = 3 − 3t − t²/3 − 2t³/9 − 5t⁴/27 − …,
      I₀(t) = 20/3 − 20t + 52t²/3 − 28t³/9 − 7t⁴/27 − 7t⁵/81 − ….                                                         (3.4)

  On `(2/3, 3/4)` the series sums to `ψ_+`, the smaller root. This recovers #242's `φ_e = 1/3 + t/3 + 10t²/27 + O(t³)` and
  `I(t, 0) = 20/3 − 20t + (52/3)t² + O(t³)`.

*Proof.*
- **(3.1).** It is a polynomial identity (C3). Both sides equal `ψ³ − 3c′ψ² + 4c′³ − (2 − 3t)²`, and
  `4(1 − t)³ − (2 − 3t)² = 3t² − 4t³`.
- **(3.2).**
  - `ψ_e` is the largest real root of (3.1).
  - For `t ≤ 2/3`, `ψ_+ ≥ t`. This is clear if `t ≤ ½`. On `[½, 2/3]`, `S² − (2t − 1)² = 4t(2/3 − t) ≥ 0`, so
    `S ≥ 2t − 1`.
  - For `t ∈ (2/3, 3/4]`, `S < 2t − 1`, so `t > ψ_+`. For `t > 3/4`, `ψ_±` are not real.
- **(3.3).**
  - On `t ≤ 2/3`, `|c′| = 1 − t` and `δ = ½ − t + (3/2)S`. Expanding `(1 − t)δ² + δ³/3` and reducing with
    `S² = 1 − 4t/3` gives (3.3) (C3).
  - On `[2/3, 1]`, `δ = 2t − 1`. For `t ≥ 1`, `δ = t − (t − 1) = 1`.
- **Monotonicity, the kink and the slopes.**
  - On `t < 2/3`, differentiate `I₀ = ∫_{c′}^{ψ_e}(ψ² − c′²)dψ` with `dc′/dt = −1` and `ψ_e′ = −2 − 1/S`. This gives
    `I₀′ = −δ[2ψ_e + (ψ_e + c′)/S] < 0`, since `δ > 0` there (C3).
  - On `[2/3, 1]`, `I₀′ = (2t − 1)(3 − 2t) > 0` and `I₀″ = 8 − 8t`. On `[1, ∞)`, `I₀′ = 1`.
  - At `t = 2/3` (`δ = S = 1/3`, `ψ_e = 2/3`, `c′ = 1/3`) both sides of (3.3) equal `4/81`. The one-sided slopes are `−13/9`
    and `5/9`. Their jump, `2`, is the kink of Corollary A.2(c) at `c′ = 1/3`: crossing `R = 0` changes `∂_tI = −∂_{c′}Φ −
    12∂_RΦ` by `12κ(1/3) = 2`.
- **(3.4).**
  - Expand `S = √(1 − 4x)` with `x = t/3`, using `√(1 − 4x) = 1 − 2Σ_{m≥0}C_m x^{m+1}`. This is the Taylor series of `ψ_+`,
    convergent for `|t| ≤ 3/4`.
  - By (3.2), `ψ_e = ψ_+` exactly on `t ≤ 2/3`.
  - The coefficients of `I₀` follow (C3). ∎

**Corollary A.2 (the dependence on `χ₀`).** Fix `t`.
- (a) **Minimum and zero set.** `Φ(c′, ·)` depends on `R` only through `|R|`, and is nondecreasing in `|R|`, with minimum
  `Φ(c′, 0) = (4/3)(c′₊)³`. These hold for all `(t, χ₀)`, including `Δ`:
  - `I(t, χ₀) ≥ (4/3)(1 − t)₊³`, with equality at `χ₀ = 12t − 8`;
  - `I(t, χ₀) = 0` iff `t ≥ 1` and `χ₀ = 12t − 8`.

  On that half-line every typed configuration is elder, except for finitely many `φ`.
- (b) `I(1, χ₀) = (χ₀ − 4)²/48`.
- (c) **The kink.** For fixed `c′`, `Φ(c′, ·)` is even, convex, and smooth on `R ≠ 0`, with `0 ≤ ∂_R²Φ ≤ 1/16` there (Lemma
  B.2). At `R = 0` its derivative jumps by `κ(c′) := (3c′₊)^{3/2}/6`. So `I` has a convex kink along the half-line
  `χ₀ = 12t − 8`, `t < 1`.
  - Moreover `Φ(λ²c′, λ³R) = λ⁶Φ(c′, R)` for `λ > 0`.
  - Across `t = 1`, away from `χ₀ = 4`, `I` is `C²` but not `C³`: by (2.7), `I` is an analytic function of `(c′, R)` plus
    `(2/3)|c′|³`.

*Proof.*
- **Off `Δ`.** Theorem A involves `χ₀` only through `R²`, and `ψ_e` increases with `R²`.
  - At `R = 0`, `ψ_e = ψ₀`. For `c′ > 0` this gives `δ = c′` and `Φ = (4/3)c′³`. For `c′ ≤ 0` it gives `δ = 0` and `Φ = 0`.
  - For `c′ ≤ 0` and `R ≠ 0`, `ψ_e > ψ₀ = |c′|`, so `I > 0`.
  - The minimizing points `R = 0` are not on `Δ`, except `(1, 4)`.
- **On `Δ`** (the referee's arguments).
  - *`c′ > 0`.* For typed `ψ ∈ (c′, 2c′)`, `s > B`, so `n ≥ 1` by (C6), which covers `Δ_k`. #170 §3's critical-chord bound
    `d_P(M) ≥ h_* > −1` holds for every typed cubic. So these `φ` are rejected, and
    `I ≥ ∫_{c′}^{2c′}(ψ² − c′²)dψ = (4/3)c′³ > 0`.
  - *The only point with `c′ ≤ 0`.* This is `(1, 4)`, where `B = D = 0`. In [CUB]'s sheared variables,
    `P = 2u³ − 3u/2 − ½ + (s/2)Z²` with `s < 0`, so `P ≤ 2(u + ½)²(u − 1)`.
    - A path from `M` to `{P > 0}` must reach `u > 1`, hence cross `u = ½`, where `P ≤ −1`.
    - So `d_P(M) ≤ −1`, and with the chord bound `d_P(M) = −1`.
    - By [CUB]'s `B = D = 0` case there are no extra critical points, so `S` kills `M` for every typed `φ`, and
      `I(1, 4) = 0`.
- **(b).** At `c′ = 0`, `g₀(ψ) = 16ψ³`, so `ψ_e³ = R²/16` and `I = ψ_e³/3 = R²/48`. At `χ₀ = 4` this is `0`, as in (a).
- **(c).** This is Lemma B.2 below. The homogeneity holds because `g_{λ²c′}(λ²ψ) = λ⁶g_{c′}(ψ)`. ∎

**Corollary A.3 (asymptotics, exact leading terms).**
- **As `t → −∞` at fixed `χ₀`.** `ψ_e = 2|t| + √(3|t|) + 3/2 + O(|t|^{−1/2})`, so `φ_e|t| → 1/2`. Also

      I = (4/3)|t|³ + 3√3|t|^{5/2} + (17/2)t² + O(|t|^{3/2}).

  #242 fitted `|t|³(4/3 + 5.74|t|^{−1/2})` to a table on `|t| ≤ 400`. With the exact terms,
  `3√3 + (17/2)|t|^{−1/2} ∈ [5.62, 6.05]` on that range.
- **As `|χ₀| → ∞` at fixed `t`.** `ψ_e = (R²/16)^{1/3} + c′ + O(|R|^{−2/3})`, so `φ_e|χ₀|^{2/3} → 16^{1/3}`. Also
  `I = R²/48 + c′(R²/16)^{2/3} + O(|R|^{2/3})`. At `t = 0` this is `I(0, χ₀) = χ₀²/48 + 16^{−2/3}|χ₀|^{4/3} + O(|χ₀|)`.
- **As `t → +∞` at fixed `χ₀`.** `I = t − 2/3 − χ₀/3 + O(1/t)`.

*Proof.*
- **`t → −∞`.** Write `m = 1 + |t|` and `ψ_e = 2m + ρ`. Then `16ρ²(ρ + 3m) = (12m + χ₀ − 4)²`. Matching the orders `m²` and
  `m^{3/2}` gives `ρ = √(3m) − ½ + O(m^{−1/2})`. Then `I = mδ² + δ³/3` with `δ = m + ρ`.
- **`|χ₀| → ∞`.** In `y³ − 3c′²y + 2c′³ = R²/16`, `y = (R²/16)^{1/3} + O(|R|^{−2/3})`. Insert this into (2.7).
- **`t → +∞`.** Write `m = t − 1 = −c′` and `ψ_e = m + δ`. Then `16(3m + δ)²δ = (12m − (χ₀ − 4))²` gives
  `δ = 1 − χ₀/(6m) + O(m^{−2})`, and `I = mδ² + δ³/3`.

These expansions, including the `(17/2)t²` term, were checked in 40- and 60-digit arithmetic (exploration; the referee). ∎

**Corollary A.4 (`β > 2`, `χ ≤ 0`).** If the configuration is typed with `β > 2` and `χ₀ ≤ 0`, it is rejected (off the null
sets of Theorem A).

This reproves, at Theorem A's conditional scope, #242 Lemma 2's statement that case (D′) needs `χ > 0`. Codex's v1.2 readback
(5952577050) gives a direct finite-path proof.

*Proof.* `β > 2` means `ψ < t`.
- If `t < 2/3`, (A) would need `ψ ≥ 2c′ = 2 − 2t > t`, which is impossible.
- If `t ≥ 2/3`:
  - then `t ≥ ψ₀`, and `g_{c′}(t) = 16(3t − 2)²`;
  - and `R = χ₀ + 8 − 12t ≤ −4(3t − 2) ≤ 0`, so `R² ≥ g_{c′}(t)`;
  - an elder `ψ` would satisfy `ψ ≥ ψ₀` and `g_{c′}(ψ) ≥ R² ≥ g_{c′}(t)`, so `ψ ≥ t` because `g_{c′}` is strictly increasing
    on `[ψ₀, ∞)`;
  - this contradicts `ψ < t`. ∎

## 4. Theorem B: the expansion of `H` to order `k⁴`

Let `(γ, B, C₃)` be independent `N(0, 2)`, `N(0, 2)`, `N(0, 6)`, `t = 12kB/γ²`, `χ₀ = 576k²C₃/γ³`, and
`p(γ) = (4π)^{−1/2}e^{−γ²/4}`. #242 Proposition 4 defines `H(k) := e^{−12k²}E[γ⁶I(t, χ₀)]/800`.

Put `T₂(τ) := 20/3 − 20τ + (52/3)τ²` and `R₂(τ) := I₀(τ) − T₂(τ)`. By (3.3) and (3.4), `R₂` is explicit, and
`R₂(τ) = −(28/9)τ³ + O(τ⁴)` at `0`.

**Theorem B.** As `k → 0`,

    H(k) = 1 + (12/25)k² + h_{7/2}k^{7/2} + h₄k⁴ + o(k⁴),    h₄ = 728/25,                                            (4.1)

    h_{7/2} = (216√6/(25π))·Γ(9/4)·Λ = 16Γ(9/4)(1728√6 − 4332√2 − 2721)/(2625π) = −10.144044022514828…,                     (4.2)

    Λ := ∫_0^∞ τ^{−9/2}[R₂(τ) + R₂(−τ)] dτ = 128/105 − (2888√3 + 907√6)/2835 = −1.3290475939905679572…              (4.3)

This is conditional on Theorem A, through `I = Φ(c′, R)` almost surely. The coefficient `h₄` was derived by this packet's
referee; its proof is given below.

**Lemma B.1 (the line `χ₀ = 0`).**
- (a) `R₂(τ) + R₂(−τ) = −(14/27)τ⁴ + O(τ⁶)` near `0`.
  - Hence `|R₂(τ) + R₂(−τ)| ≤ C_Rτ⁴` and `|R₂(τ) + R₂(−τ) + (14/27)τ⁴| ≤ C_Rτ⁶` for all `τ ≥ 0`.
  - Also `|R₂(τ)| ≤ C_R(1 + |τ|³)`.
- (b) The integral (4.3) converges, and equals the value stated.

*Proof of (a).*
- On `[−2/3, 2/3]`, `R₂` is analytic (3.3). Its Taylor polynomial of degree `2` vanishes, and the series (3.4) gives the
  expansion of `R₂(τ) + R₂(−τ)`, which is even.
- For `|τ| ≥ 2/3`, both sides are bounded by `C(1 + |τ|³)` (by (2.8), or by (3.3) for `τ ≥ 1`), which is at most a constant
  times `τ⁴` and `τ⁶`.

*Proof of (b).*
- **The pieces.** On `0 < τ ≤ 2/3`, (3.3) gives

      R₂(τ) + R₂(−τ) = −6 − (53/3)τ² + P₁(τ)S₋(τ) + P₁(−τ)S₊(τ),    P₁(τ) := (3/2)(1 − τ)(2 − 3τ),  S_∓ := √(1 ∓ 4τ/3).

  For `τ > 2/3`:
  - `R₂(τ)` is the polynomial `(2τ − 1)²(2 − τ)/3 − T₂(τ)` on `(2/3, 1]`, and `τ − 2/3 − T₂(τ)` on `(1, ∞)`;
  - `R₂(−τ) = P₀(−τ) + P₁(−τ)S₊(τ) − T₂(−τ)`, where `P₀(τ) = 11/3 − 21τ/2 + 17τ²/2 − 4τ³/3`.
- **The square-root terms have algebraic antiderivatives** (C7; each is a polynomial identity after multiplying by
  `τ^{9/2}S`):

      F₋(τ) := S₋(τ)(1444τ³ − 3711τ² + 3051τ − 810)/(945τ^{7/2}),     F₋′ = τ^{−9/2}P₁(τ)S₋(τ),
      F₊(τ) := −S₊(τ)(1444τ³ + 3711τ² + 3051τ + 810)/(945τ^{7/2}),    F₊′ = τ^{−9/2}P₁(−τ)S₊(τ).

  The polynomial terms integrate termwise to sums of powers `τ^{n−7/2}`.
- **No contribution from `τ = 0`.**
  - Near `0` the total antiderivative `G(τ)` is `τ^{−7/2}` times a power series in `τ`.
  - The integral converges at `0` by (a), so `lim_{τ→0}G(τ)` exists.
  - With only half-integer powers present, this forces `G(τ) = Σ_{j≥4}g_jτ^{j−7/2} → 0`.
- **The endpoints.**
  - At infinity, every polynomial antiderivative vanishes, and `F₊(∞) = −2888√3/2835`.
  - At `2/3`, `S₋ = 1/3` and `τ^{−7/2} = 27√6/16`.
  - Summing the endpoint values exactly in `Q(√3, √6)` gives (4.3) (C7).
  - A floating-point quadrature agrees to `10⁻¹²` (C7), and mpmath quadratures to 39 and 27 digits (exploration; the
    referee). ∎

**Lemma B.2 (`Φ` in `R`).** Fix `c′`. For `R ≠ 0` put `ρ := ψ_e − 2c′`. Then `ρ ≥ max(0, −3c′)`, with `ρ > 0` if `c′ ≤ 0`,
and `R² = 16ρ²(ρ + 3c′)`. Moreover:
- (a) `∂_RΦ = sgn(R)·F(ρ)`, where `F(ρ) := (ρ + c′)(ρ + 3c′)^{3/2}/(6(ρ + 2c′))`.
- (b) `∂_R²Φ = 1/24 + (2x + x² + 2x³)/72` with `x := c′/ψ_e ∈ [−1, ½]`. Hence `0 ≤ ∂_R²Φ ≤ 1/16`, and `∂_R²Φ` is continuous
  on `R ≠ 0`.
- (c) `F` is nondecreasing, and `∂_RΦ(c′, 0±) = ±(3c′₊)^{3/2}/12`. So `Φ(c′, ·)` is convex, and its derivative jumps by
  `κ(c′) = (3c′₊)^{3/2}/6` at `R = 0`.
- (d) For all `r, h`, the symmetric second difference satisfies

      0 ≤ Δ₂ := ½[Φ(c′, r + h) + Φ(c′, r − h)] − Φ(c′, r) ≤ h²/32 + (κ(c′)/2)|h|·1{|r| < |h|}.                        (4.4)

  If `|r| ≥ |h|`, then `Δ₂ = (h²/2)∂_R²Φ(c′, ξ)` for some `ξ` between `r − h` and `r + h`.

*Proof.*
- **The relation.** `ψ_e − 2c′ = ρ` and `ψ_e + c′ = ρ + 3c′`, so `g_{c′}(ψ_e) = R²` reads `R² = 16ρ²(ρ + 3c′)`.
  - For `c′ ≥ 0`, `ρ ≥ 0`.
  - For `c′ < 0`, `ψ_e ≥ |c′|` gives `ρ ≥ 3|c′| > 0`, and `ρ + 3c′ = ψ_e − |c′| ≥ 0`.
- **(a).** `∂_RΦ = (ψ_e² − c′²)∂_Rψ_e`. Differentiating `g_{c′}(ψ_e) = R²` gives
  `∂_Rψ_e = 2R/g_{c′}′(ψ_e) = R/(24ψ_eρ) = sgn(R)√(ρ + 3c′)/(6ψ_e)`. Also `ψ_e² − c′² = (ρ + c′)(ρ + 3c′)`.
- **(b).** `∂_R²Φ = F′(ρ)·dρ/dR`, with `dR/dρ = 6ψ_e/√(ρ + 3c′)`. With `p = ψ_e = ρ + 2c′`, this reduces to the rational
  identity `∂_R²Φ = (3p³ + 2c′p² + c′²p + 2c′³)/(72p³)` (C6), which is (b).
  - The range `x ∈ [−1, ½]` follows from `p ≥ 2c′` when `c′ > 0` and `p ≥ |c′|` when `c′ < 0`.
  - `2x + x² + 2x³` is increasing, since its derivative `2 + 2x + 6x²` has negative discriminant. It equals `−3` at `−1` and
    `3/2` at `½`.
- **(c).** `(log F)′ = 1/(ρ + c′) + (3/2)/(ρ + 3c′) − 1/(ρ + 2c′)`.
  - For `c′ ≥ 0` this is positive, since `1/(ρ + c′) ≥ 1/(ρ + 2c′)`.
  - For `c′ = −m < 0` and `ρ > 3m`: `1/(ρ − m) − 1/(ρ − 2m) = −m/((ρ − m)(ρ − 2m))`. This is smaller in absolute value
    than `(3/2)/(ρ − 3m)`, because `(3/2)(ρ − m)(ρ − 2m) > 3m(ρ − 2m) > m(ρ − 3m)`.
  - The limits at `R → 0±` are `F(0) = (3c′)^{3/2}/12` (`c′ > 0`) and `0` (`c′ ≤ 0`).
- **(d).** `Δ₂ = ½∫_0^{|h|}[∂_RΦ(r + u) − ∂_RΦ(r − u)]du`. The bracket is at most `∫_{r−u}^{r+u}∂_R²Φ + κ·1{|r| < u}`, which
  is at most `u/8 + κ·1{|r| < u}`. If `|r| ≥ |h|`, `Φ` is `C²` on the interval, and Taylor's formula gives the mean-value
  form. ∎

*Proof of Theorem B.* By Theorem A, for almost every `(γ, B, C₃)`, `I(t, χ₀) = Φ(c′, r + χ₀)` with `c′ = 1 − t` and
`r := 8 − 12t`. By (2.8), `γ⁶Φ ≤ C(γ⁶ + 1728k³|B|³ + 331776k⁴C₃²)`, so every expectation below is finite. Write

    E[γ⁶I] = E[γ⁶T₂(t)] + 𝒥_t(k) + 𝒥_χ(k),    𝒥_t(k) := E[γ⁶R₂(t)],    𝒥_χ(k) := E[γ⁶(Φ(c′, r + χ₀) − Φ(c′, r))].   (4.5)

**Step 1 (the quadratic part).** `E[γ⁶] = 120`, `E[γ⁶t] = 0` and `E[γ⁶t²] = 144k²E[B²]E[γ²] = 576k²`. So
`E[γ⁶T₂(t)] = 800 + 9984k²`, as in #242 Proposition 4.

**Step 2 (the `γ ≈ √k` region: `𝒥_t(k) = p(0)Kk^{7/2} + 32256k⁴ + O(k^{9/2})`).**
- Put `γ = √k·g`. Then

      𝒥_t(k) = k^{7/2}∫_R p(√k g) g⁶ ϱ(g) dg,    ϱ(g) := E_B[R₂(12B/g²)] = E[½(R₂(τ) + R₂(−τ))]|_{τ = 12|B|/g²}.

  The second form uses that `B` is symmetric and independent of `γ`.
- **Bounds.** By Lemma B.1(a) and `E[B⁴] = 12`, `|g⁶ϱ(g)| ≤ C·min(1, g^{−2})` and
  `|g⁶ϱ(g) + 64512g^{−2}| ≤ Cg^{−6}` for `|g| ≥ 1`. Here `64512 = (7/27)·12⁴·E[B⁴]`.
- **The leading term.** Since `0 < p(√k g) ≤ p(0)`, dominated convergence and `|p(√k g) − p(0)| ≤ p(0)min(1, kg²/4)` give
  `𝒥_t(k) = p(0)Kk^{7/2} + k^{7/2}∫(p(√k g) − p(0))g⁶ϱ(g)dg`, with `K := ∫_R g⁶ϱ(g)dg`.
- **The correction.**
  - Replace `g⁶ϱ` by `−64512g^{−2}` on `|g| ≥ 1`. By the second bound this costs `O(k^{7/2}·k)`.
  - In the remainder, substitute `w = √k g`. It becomes `−64512√k∫_{|w|≥√k}(p(w) − p(0))w^{−2}dw = 32256√k + O(k)`, since
    `∫_R(p(w) − p(0))w^{−2}dw = −½`.
- **The constant `K`.** For fixed `|B|`, substitute `g = (12|B|/τ)^{1/2}` on `g > 0`; this is justified by the bounds. It
  gives `∫_0^∞ g⁶·½[R₂ + R₂(−·)](12|B|/g²) dg = ¼(12|B|)^{7/2}Λ`. Hence

      K = ½·12^{7/2}·E|B|^{7/2}·Λ,    E|B|^{7/2} = 2^{7/2}Γ(9/4)/√π,

  and `p(0)K/800 = 24^{7/2}Γ(9/4)Λ/(3200π) = h_{7/2}`, using `24^{7/2} = 27648√6`.

**Step 3 (the `χ₀` dependence: `𝒥_χ(k) = 53248k⁴ + o(k⁴)`).**
- Given `(γ, B)`, `χ₀` is symmetric, so `𝒥_χ(k) = E[γ⁶Δ₂(c′, r, χ₀)]`.
- **Away from the kink.** On `{|r| ≥ |χ₀|}`, Lemma B.2(d) gives `γ⁶Δ₂ = 165888k⁴C₃²·∂_R²Φ(c′, ξ)`, with `ξ` between
  `r ± χ₀`.
  - As `k → 0` at fixed `(γ ≠ 0, B, C₃)`: `t → 0`, `χ₀ → 0`, `ξ → 8` and `c′ → 1`.
  - `∂_R²Φ` is continuous at `(1, 8)` and bounded by `1/16`. At `(1, 8)`, `x = 1/3` gives `∂_R²Φ(1, 8) = 13/243`.
  - The indicator tends to `1`.
  - By dominated convergence this part is `165888·(13/243)·E[C₃²]·k⁴ + o(k⁴) = 53248k⁴ + o(k⁴)`.
- **At the kink**, `{|r| < |χ₀|}`. By (4.4), the integrand is at most `γ⁶χ₀²/32 + γ⁶κ(c′)|χ₀|/2`.
  - **The first term.** `γ⁶χ₀² = 331776k⁴C₃²`, and the indicator tends to `0` pointwise, so this term is `o(k⁴)`.
  - **The second term on `|χ₀| ≤ 4`.**
    - The event forces `1/3 < t < 1`, so `κ ≤ 2^{3/2}/6 < ½`.
    - Given `(γ, C₃)`, it puts `B` in an interval of length `8k|C₃|/|γ|` centred at `γ²/(18k)`. This interval lies in
      `{B ≥ γ²/(36k)}`, exactly when `|χ₀| ≤ 4`.
    - So its probability is at most `(8k|C₃|/|γ|)e^{−γ⁴/(5184k²)}`.
    - With `γ⁶|χ₀| = 576k²|C₃||γ|³`, this part is at most `Ck³E[C₃²]∫γ²e^{−γ⁴/(5184k²)}dγ = O(k^{9/2})`.
  - **The second term on `|χ₀| > 4`**, that is `|γ|³ < 144k²|C₃|`.
    - Use `κ(c′) ≤ C(1 + |t|^{3/2})`. Then `γ⁶κ|χ₀| ≤ Ck²|C₃|(|γ|³ + (12k|B|)^{3/2})`.
    - Integrate over `|γ| < (144k²|C₃|)^{1/3}`, where the density of `γ` is at most `p(0)`. This gives
      `O(k^{14/3} + k^{25/6})`.

**Step 4.**
- `E[γ⁶I]/800 = 1 + (312/25)k² + h_{7/2}k^{7/2} + (32256 + 53248)k⁴/800 + o(k⁴)`.
- Multiplying by `e^{−12k²} = 1 − 12k² + 72k⁴ + O(k⁶)` gives (4.1), with `h₄ = 106.88 − 149.76 + 72 = 728/25`. ∎

**Remarks.**
1. *The sign.* `h_{7/2} < 0`, so `H(k) < 1 + (12/25)k²` for small `k`. The fractional term comes from the region `γ ≈ √k`,
   where `|t|` is of order one. There the elder edge is the branch (3.2) of Corollary A.1, which is not analytic across
   `t = 2/3`.
2. *Compared with OA-242-C-01.* Codex's toy function `I_* = T₂` has the same local data and no `k^{7/2}` term. Theorem B shows
   that the actual `I` has one, with coefficient `p(0)K/800`. `K ≠ 0` because `Λ ≠ 0`.
3. *The `C₃` contribution.* Step 3 shows `(H − H₀)(k) = (53248/800)k⁴ + o(k⁴) = 66.56k⁴ + o(k⁴)`, where `H₀` is `H` with
   `C₃ = 0`. #242 §5 used a fitted `Δ_χ ≈ 62.24k⁴` below `k = 0.1` (see §5).
4. *Weaker hypotheses.* The `k^{7/2}` term needs only Step 2, that is, `I(t, 0)` along `χ₀ = 0` together with the symmetry in
   `C₃`. Step 3 needs `Φ`'s convexity and curvature bound.

## 5. Numerical consequences (exploration; outside the repository)

These use numpy, scipy, mpmath and sympy, and are not part of the proof. The scripts and logs are in the project archive,
under `V2_2/frontiers_soft_closed_form_20261002/exploration/`, with a README; SOURCES.json pins their hashes. The referee's
independent scripts are in `referee_checks/` there.

**Theorem A against #242's numerics.**
- *The 101 × 121 table* `Itab2d_v2.npz` (#242 §5(3)). The relative difference has median `1.8·10⁻⁷`.
- *Larger disagreements.* 97 of the 12,221 entries differ by more than `10⁻³` relative. They fall into three classes:
  - **7 entries** with `I < 10⁻⁵`, where the table's grid misses a tiny rejected interval.
  - **54 entries** that are table resolution. Rerunning the same scanner on a finer grid agrees with Theorem A to
    `10⁻⁴`.
  - **36 entries** in thin layers around `β = 2`, where #242's scanner `dec1d.py` itself errs:
    - *Just above `β = 2`, it falsely rejects.* For `a(½) = 1 − β/2 < 0`, the slices just right of `X = ½` lose their
      maximum at a fold at distance `≈ a(½)²/χ`. This distance can be far below the scan's grid step. `dec1d` treats "the
      first grid point is a slice without a maximum" as a trigger. But if the fold value `A₀ + a³/(6χ²)` is below `L_S`,
      the band closes before the fold, and `S` kills `M`. Example: at `(t, χ₀) = (9.005434, 193.926947)` the scanner
      rejects `φ ∈ (0.11104, 0.12491)`; Theorem A gives `(0.11245, 0.12491)`.
    - *Just below `β = 2`, it falsely accepts.* Its tolerance `δ = 10⁻³` treats a band that ends within `10⁻³` of `X = ½`
      as ending at `S`. For `χ < 0` the slices just left of `X = ½` open (at distance `≈ a(½)²/|χ|`), and there the axial
      segment joins `M` to the far region above `L_S`. So the configuration is rejected. Example: at
      `(t, χ₀) = (11.464348642908552, −0.426511285632118)`, a table node, the scanner's edge is `φ = 0.0871798` and
      Theorem A's is `0.0871797`. The table, with its coarser grid, is off by `0.018` in `I`.
- *A fold-aware version of the scan* (with a geometric grid to `10⁻¹⁵` around `½` and bisection for the fold) agrees with
  (A):
  - on 6,000 general typed points, with 0 disagreements;
  - on 6,000 points concentrated in `β ∈ (2, 2.15)`, where `dec1d` itself disagrees on 1,221. The fold-aware scan disagrees
    only within `1.1·10⁻⁵` of `β = 2`, below double precision there. At six of those points an 80-digit version of the same
    scan agrees with (A).
- *The two-dimensional flood fill* `model2d.py` errs the other way near `β = 2`. Its level offset `ε = 2·10⁻³|L_S|` exceeds
  the relevant level gaps. This is why #242's validation did not expose the scanner artifacts. #243's v1.1 referee did
  record that the scanner needed refinement near `X = ½`.
- *A direct maximin computation* by the referee compared (A) with the maximin level computed on a grid, using neither #170,
  [CUB] nor any scan. It found no disagreement at 2,400 typed points in three families (broad, near `β = 2`, and the
  Gaussian law at `k = 0.5`). It also agreed at 400 points on `Δ`, which Theorem A excludes; this is evidence, not proof.

**The function `H`.**
- *Method.* With Theorem A in [CUB]'s variables,

      γ⁶I = 13824k³[(b/2)ξ² + ξ³/3],    b := |B′|,  B′ := B − γ²/(12k),

  where `ξ := x_e − b/2 ≥ 0`, `x_e` is the root `≥ max(−B′, B′/2)` of `(x + B′)²(2x − B′) = 12kD²`, and
  `D = (C₃ − γB/(4k) + γ³/(72k²))/2`.
  - `H` is evaluated by nested Gauss–Legendre quadrature, split at the kinks `B′ = 0` and `D = 0`. Raising the node counts
    from `60³` to `100³` changes `H` by less than `10⁻¹⁰`.
  - The referee's independent quadrature reproduces every printed digit of the `H` row.
- *Values.*

  | `k` | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 1.0 |
  |---|---|---|---|---|---|---|---|---|---|
  | `H` (Theorem A) | 1.0039609 | 1.0040821 | 0.9343640 | 0.7269471 | 0.4395370 | 0.2005857 | 0.0686747 | 0.0176869 | 0.0005098 |
  | #242 v1.2, §5 | 1.0039 | 1.0041 | 0.9345 | 0.7271 | 0.4397 | 0.2007 | 0.0687 | 0.0177 | 0.0005 |
  | `H₀` (`C₃ = 0`) | 0.9976233 | 0.9333611 | 0.7402788 | 0.4662446 | 0.2268015 | 0.0845012 | 0.0241003 | 0.0052729 | 0.0001152 |

- *Comparison with #242.* `H` differs from #242's values by at most `2.0·10⁻⁴`, at `k = 0.4`; this is the scanner artifacts.
  `H₀` agrees with #242's to `1.2·10⁻⁵`, which is table interpolation, since `dec1d` is exact at `χ = 0`.
- *Small `k`.*
  - `(H − 1 − (12/25)k² − h_{7/2}k^{7/2})/k⁴ = 28.94, 28.99, 29.01` at `k = 0.004, 0.002, 0.001` (140 nodes). This is consistent with
    `h₄ = 728/25 = 29.12` and the `√k`-size corrections of Step 2.
  - The referee finds the two `k⁴` constants separately. `𝒥_t` gives `J(k)/√k → 32256`, and `𝒥_χ(k)/k⁴` decreases towards
    `53248`.

**The coefficient `R_{2/3}`.**
- *Method.* `Ĩ = ∫_0^∞q^{−6}[H(q³) − 1]dq`, by Gauss–Legendre on 11 segments of `q ∈ [0.1, 1.2]`.
  - Below `q = 0.1`, the expansion (4.1) is used; this piece contributes `0.04799`. The run used early fitted values
    `−10.13` and `28.7` for `h_{7/2}` and `h₄`; the exact values change `Ĩ` by `−2·10⁻⁹`.
  - Above `q = 1.2`, `H < 2·10⁻¹³`, and the tail contributes `−1.2^{−5}/5`.
- *Accuracy.* With 16 and 24 nodes per segment the results agree to `2.5·10⁻⁸`.

      Ĩ = −0.5336676,    R_{2/3} = 0.0914028·Ĩ = −0.048779 (d = 2),    R_{2/3} = 0.1150058·Ĩ = −0.061375 (d = 3),

  with #242's prefactors (Corollary 1′ there). The referee's independent reconstruction gives `Ĩ ≈ −0.53372`, which agrees
  within its interpolation error of `5·10⁻⁵`.
- *Comparison with #242.* #242 v1.2 reports `Ĩ = −0.536`, `R_{2/3} = −0.049 ± 0.003` (`d = 2`) and `−0.0617`
  (`−0.062 ± 0.004`; `d = 3`). Its ranges contain these values.
- *Where the difference comes from* (the referee's decomposition of `Ĩ_{#242} − Ĩ`, about `−0.0024`):
  - about `−0.0019` from #242's interpolation of `Δ_χ = H − H₀` between its nodes at `k = 0.1, 0.15, 0.2`;
  - about `−0.0008` net from #242's small-`k` model `Δ_χ ≈ 62.24k⁴`, against the exact `66.56k⁴` of Remark 3;
  - only about `+0.0002` from the range `k = 0.25–0.7`, where the scanner artifacts move `H`.

## 6. Relation to other packets

- **#242 (open).** Theorem A describes #242's `𝓡` and `I` exactly, at the conditional scope above. It changes none of #242's
  stated results. It sharpens several:
  - `t*` (§2 there) is exactly `2/3`;
  - the asymptotic constants of §5(3)–(4) there are replaced by exact expansions;
  - the fourth decimals of #242 §5's `H` table at `k = 0.3–0.6` change (§5 here);
  - the small-`k` coefficient of `Δ_χ` is `66.56`, not `≈ 62`;
  - `Ĩ` is `−0.5337`.

  #242's author disclosed the scanner artifact on #242 (comment 5953336662). That comment attributes the `Ĩ` change to the
  scanner; §5 above corrects this. #242 Proposition 4's `H(k) = 1 + (12/25)k² + O(k³)`, and Codex's `O(k^{7/2})`, are
  sharpened by Theorem B.
- **#243 (open).** FL.7 is the same identification as Lemma 1. Through Theorem FL, `F(k; b, u) = F₀H(k)` for the Gaussian kernel
  is now an explicit Gaussian integral of an algebraic function.
- **#170 and [CUB] (merged, at their stated conditional scope).** Theorem E(1), Theorem C and the height identities are
  consumed in Lemma 1(iii) and Theorem A; #170 §3 also in Corollary A.2. The translation (2.2)–(2.4) is new bookkeeping, not
  a new classification.
- **Codex's D.1 (5391986303 §3).** It uses the same classifier identity to identify `F = kA∗a_fail` directly in every fixed
  `d`. Combined with D.1, Theorem A makes `a_fail` explicit for the Gaussian kernel.

## 7. Controls

`closed_form_check.py` uses the Python standard library: exact `Fraction` arithmetic, plus floating point where noted. Its
output is `RESULTS.json`, byte-identical under `-O`. Mutants `M1`–`M9` each fail only their own control. CI checks this by
parsing the checker's stderr against `SOURCES.json`. An unknown label exits 2.

| Control | Checks |
|---|---|
| C1 | Lemma 1: (i) as a polynomial identity in `(X, z)` at 30 random rational `(φ, t, χ₀)`; (2.2)–(2.4) exactly; typing iff `ψ > \|c′\|`, and `s ≤ B` iff `ψ ≥ 2c′` |
| C2 | `g′ = 48ψ(ψ − 2c′)`, `g(ψ₀) = 0`; the shift `y = ψ − c′`; the discriminant `432σ²(c′³ − σ²)`; (2.6) against bisection (floating point) on 600 points, including both branches, `c′ = 0` and `σ = 0`, with the formula's value `≥ ψ₀`; (2.8) at rational points |
| C3 | Corollary A.1: (3.1) as a polynomial identity; (3.3) from (2.5) at rational `S` (`t = 3(1 − S²)/4`); the root ordering behind `t* = 2/3`; the values `20/3`, `4/81`, `1/3`; the derivative formula `I₀′ = −δ[2ψ_e + (ψ_e + c′)/S]` against the exact derivative of (3.3) at rational `S`; the slopes `−13/9`, `5/9`, `1` and `I₀″(1) = 0`; strict monotonicity on a rational grid; the Catalan series (3.4) and the series of `I₀` to order 12 |
| C4 | Corollary A.2: `g₀(ψ) = 16ψ³`, and `I(1, χ₀) = (χ₀ − 4)²/48` with `ψ_e` found independently by bisection (floating point); the minimum `(4/3)c′³` and the zero set in both directions; (2.7) as a polynomial identity given the cubic; `∫_{c′}^{2c′}(ψ² − c′²)dψ = (4/3)c′³` |
| C5 | Corollary A.4 at 400 rational typed points with `β > 2`, `χ₀ ≤ 0`: `g_{c′}(t) = 16(3t − 2)²`, `R² ≥ g_{c′}(t) > g_{c′}(ψ)`, and the failure of (A) |
| C6 | Lemma B.2: (a) at rational points with rational square roots; the reduction of `∂_R²Φ` to `(3p³ + 2c′p² + c′²p + 2c′³)/(72p³)` as a polynomial identity; the range `[0, 1/16]` and `∂_R²Φ(1, 8) = 13/243`; the one-sided limits of `F` (jump `κ`, and `0` for `c′ ≤ 0`) as exact values of `F`; (4.4) at 300 random points (floating point) |
| C7 | Lemma B.1(b): `F₋′`, `F₊′` as polynomial identities after multiplying by `τ^{9/2}S`; the even series of `R₂(τ) + R₂(−τ)`; the exact assembly of `Λ` in `Q(√3, √6)`; a floating-point quadrature of (4.3) (exact series near `0`, Gauss–Legendre elsewhere) within `10⁻¹²`; the two forms of `h_{7/2}` in (4.2), exactly in `Q(√2, √6)`, and its value |
| C8 | Theorem B's bookkeeping: `E[γ⁶] = 120`, `E[γ⁶t²] = 576k²`, `800 + 9984k²`, `312/25 − 12 = 12/25`, `24^{7/2} = 27648√6`; `E\|B\|^{7/2} = 2^{7/2}Γ(9/4)/√π` against a quadrature (floating point); `64512`, `∫(p(w) − p(0))w^{−2}dw = −½` (floating point), `32256`, `53248` and `h₄ = 728/25`; the exponents `7/2`, `4`, `9/2`, `14/3`, `25/6` |
| C9 | Fixed points: #242's exact (D′) witness `(φ, β, χ) = (3/2, 8/3, 20/3)` is elder; `(0, 0)` gives `ψ_e = 3`, `I = 20/3` (Remark 2; on `Δ`); #242's 16 control-S8 decisions (five of them at `(0, 0)`); both §5 examples at full precision |

## 8. Not claimed (expanded)

- Theorem A is conditional on #170 Theorem E(1), [CUB] Theorem C and [CUB]'s height identities (C8)–(C11) (merged author-side
  candidates at their stated conditional scope). Lemma 1(iii) and, on `Δ`, Corollary A.2 (with #170 §3) are where they enter.
  Everything after Theorem A inherits this condition.
- On `Δ`, only Corollary A.2(a)–(b) and `(0, 0)` are claimed. Corollary A.1 at `t = 3/4` is a statement about `I₀`.
- No statement about the actual Gaussian field. The fold-scale limit is #243 (open) and #170/#175 (merged).
- The §5 values are numerical, uncertified exploration.
- Conjecture 7 of #242 (the `ℓ^{2/3}` term of `ρ_rej`) is not addressed. Its missing inputs (i)–(iii) are unchanged.
- No priority for the identification of #242's model with #170's cubic (#243 FL.7, which credits #170).

## 9. Review slices (nonauthor)

- **A** — §§1–2: Lemma 1 against #170 §2 and [CUB] §2, and Theorem A including (2.6).
- **B** — §3: Corollaries A.1–A.4, including the arguments on `Δ`.
- **C** — §4: Lemmas B.1–B.2 and Theorem B (the split (4.5), Step 2's domination and correction, Step 3).
- **D** — §§5–7: whether the numerics are described accurately and kept apart from the proofs, and whether the controls
  match their claims.

Per slice, record ACCEPT, ACCEPT WITH FIXES (with a list), or REJECT (with the failing step).
