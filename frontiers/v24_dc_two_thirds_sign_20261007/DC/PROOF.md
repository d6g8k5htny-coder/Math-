# Lifetime note DC: a certified bound `D ≤ 0.4389` for the model number `D`, and the sign of note C7's `ℓ^{2/3}` coefficient at every side `L ≥ 10`

Object: `CL-DC-MODEL-D-UPPER-20261007-v1`. Claim: main#229 6034902581, which took request 1 of 6033651797.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 7 October 2026, for Dylan Roy (delegated AI
work). The same session wrote #242, #244 and notes C3, SL, C7 and V24.
Disposition: AUTHOR-SIDE PROOF CANDIDATE, computer-assisted; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no
register, graph, STATUS, PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; organizational independence
0. Everything about `D` rests on #244's Theorem A, which is conditional (*Not claimed*).

Proposition 2's two numbers are computed by the standard-library script of §9, in outward-rounded decimal arithmetic, and so
are the enclosures of `T₂` and `−Ĩ_quad` (groups T2 and corollary). Every other step is proved by hand. The script also
checks:
- the main polynomial identities the proofs use;
- Lemma 4's constants. Their rational parts are checked exactly. The defining identities `A₁²·14400²·4π = 1`,
  `A₃·57600π = 1`, `(576√6)² = 576²·6` and `φ(0)²·2π = 1` are checked in interval arithmetic (group lemma4).
- after the run, every factor that the production loops used on sampled cells, against independent enclosures of the
  integrand's factors at the corners, edge midpoints and centres of those cells (group corners).

Before posting, three clean-context Claude subagents of this session refereed the draft in the three slices of §10, against
the consumed sources, and ran the controls. All three returned AMEND, with no blocking finding. A fourth read the revision
back and returned AMEND, again with no blocking finding. Every finding is applied, and the controls comment lists them. These
are author-side reads and earn no review credit.

**What is new.**
- **Theorem DC** (§7). `D ≤ 0.4389`. More precisely `D ≤ T₁ + T₂ + T₃` (Proposition 1), with
  - `T₁ ≤ 0.0951690`,
  - `T₂ = (28/15)·12^{−7/6}Γ(7/6) ∈ [0.0953758, 0.0953759]`,
  - `T₃ ≤ 0.248277` (Proposition 2),

  so `D ≤ 0.438822`. This holds at #244 Theorem A's conditional scope. Numerically `D ≈ 0.07674` (note V24, Remark 1), so
  the bound is one-sided and far from sharp.
- **Corollary DC1 (the model).** At #244 Theorem A's conditional scope, `Ĩ ≤ −0.17158` and `J/30 − Ĩ ≥ 0.17160`. So in
  `d = 2, 3` the model value `R^∞ = Ĩ𝒮_d` of note SL's coefficient is negative, and the model value `(J/30 − Ĩ)𝒮_d` of note
  C7's coefficient is positive.
- **Corollary DC2 (the torus field).** At #244 Theorem A's conditional scope, for `d ∈ {2, 3}` and every real side `L ≥ 10`
  (SIDE24 included):
  - `(c₃ − R_{2/3})(L) ≥ 0.1711·𝒮_d > 0`;
  - `R_{2/3}(L) ≤ −0.1710·𝒮_d < 0`.

  So, by note C7's (C7.1), for each such `L` the function `ν_eld(ℓ) − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} − ν_eld^{far,r_0^*}(ℓ)`
  is positive for `0 < ℓ < ℓ₀(d, L)` and of exact order `ℓ^{2/3}`. The threshold `ℓ₀` is not quantified. Note V24's
  Corollary V2 had reduced this sign to `D ≤ 0.61` for `L ≥ 24`. With the `L₀ = 10` columns of its Theorem V, the same
  argument covers every `L ≥ 10` once `D < 0.6099` (in `d = 3`, using `−Ĩ_quad ≥ 0.6104056`). Theorem DC's bound meets
  both conditions.
- **The route.**
  - A sharper form (1.1) of #244's (4.4), with the same proof, lets the kink of `Φ` enter through `(|h| − |r|)₊`.
  - Averaging over `C₃` given `(k, γ, B)` bounds `D` by three terms (Proposition 1):
    - `T₁` is the line `χ₀ = 0`;
    - `T₂` is the curvature slack `1/32 − 13/486` of `I_quad`'s `χ₀²` coefficient, in closed form;
    - `T₃` is the kink.
  - Birnbaum's Mills-ratio inequality (Lemma 3, proved here) bounds the kink's Gaussian factor by an elementary function.
  - `R₂ = I₀ − q₂` is strictly decreasing, by an exact polynomial identity (Lemma 2). So every cell bound of `T₁` is an
    endpoint evaluation.
  - What remains is a two-dimensional and a three-dimensional integral of explicit monotone factors. Proposition 2 bounds
    them by cell sums with closed-form tails.

**Not claimed.**
- No value of `D`, `Ĩ`, `J` or note C7's coefficient: only the bounds and signs above. `T₂` alone exceeds the numerical `D`,
  and a two-sided enclosure needs more (Remark 3).
- Everything about `D`, `Ĩ` and `R_{2/3}` uses `I = Φ`, that is #244's Theorem A. Theorem A is conditional on merged
  author-side candidates at their stated scope: #170 Theorem E(1), [CUB] Theorem C, and [CUB]'s height identities (C8)–(C11)
  with its `B = 0` paragraph (#244's disposition). Corollary DC2 also inherits the scopes of notes C7 and V24.
- Nothing for `d ≥ 4` or `L < 10` (note V24's scope). No rate, and no uniformity in `L` of the threshold `ℓ₀`: (C7.1) keeps
  its `o(ℓ^{2/3})`.
- Proposition 2 is computer-assisted. The script ran on CPython 3.11.15 with libmpdec 2.5.1 (Python's `decimal`), with
  directed rounding. Its rigor assumes the documented correct rounding of `exp` and `ln`, which it widens by one unit in the
  last place. Square roots are verified by squaring.

**Consumed.**
- Note V24 (main#229 6034159111; Slices A, B and C PASS):
  - Theorem V's table, the `L₀ = 10` columns;
  - the identity `Ĩ = Ĩ_quad + D`, with `D` as in (5.3) and `Ĩ_quad = −(112/675)Γ(1/6)12^{−1/6}` (proof of Corollary V2);
  - Lemma J (`J ≥ 1/2000`);
  - the absolute convergence of (5.3) (Lemma K with V24's (5.1));
  - `I_quad` (§0).
- #244 `frontiers/soft_closed_form_20261002/PROOF.md` (blob `c69f92b1`):
  - Theorem A ((2.5)–(2.6)), and Remarks 1 and 4 ((2.8));
  - §3's `I₀(t) := Φ(1 − t, 8 − 12t)`, (3.3) and (3.4);
  - Lemma B.1(a)'s growth bound;
  - Lemma B.2(b)–(c) and the proof of (d);
  - §4's `T₂(τ)`, `R₂`, and the law of `(γ, B, C₃)` and of `(t, χ₀)`.
- Note C7 (main#229 6030039377; read in every slice): Theorem C7 and (C7.1) at every `L`, for Corollary DC2.
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): Theorem 1 (`𝔇 > 0`, so `𝒮_d > 0`).

**Cited only.**
- The Monte Carlo comment main#229 6033651797 (Remark 2).
- Z. W. Birnbaum, *An inequality for Mill's ratio*, Ann. Math. Statist. 13 (1942) 245–246, for Lemma 3, which is proved
  here.

**Prior work and overlap.**
- Before drafting I read main#229 from 6033651797 (which posted the request) to 6034841394 and found no other claim on `D`.
- Note V24 (Remark 2 and *Not claimed*) leaves `D` uncertified. Its controls certify only `Γ(7/6) ≥ 0.9277`,
  `12^{−1/6} ≥ 0.6608` and the constant `0.6103`.
- #244 certifies none of its §5 numbers.
- No packet on Math- `main` at `7d2f6250` encloses `Ĩ`, `D` or `J`.

## 0. Setting

As in #244 §4 and note V24 §5. Let `(γ, B, C₃)` be independent `N(0, 2)`, `N(0, 2)` and `N(0, 6)`. For `k > 0`, put
`t = 12kB/γ²` and `χ₀ = 576k²C₃/γ³`.
- `I` is #242's (2.5), and `Φ(c′, R)` is #244's closed form (2.5)–(2.6). For `k > 0`, `(t, χ₀)` has a density, so by Theorem A
  `I(t, χ₀) = Φ(1 − t, χ₀ + 8 − 12t)` almost surely.
- `I_quad(t, χ₀) := 20/3 − 20t + (8/9)χ₀ + (52/3)t² − (4/3)tχ₀ + (13/486)χ₀²`, as in note V24 §0.
- `q₂(t) := I_quad(t, 0)`; this is #244 §4's `T₂(τ)`, renamed here to avoid a clash.
- `I₀(t) := Φ(1 − t, 8 − 12t)` (#244 §3), `R₂ := I₀ − q₂` (#244 §4), and `R₂ₑ(t) := ½(R₂(t) + R₂(−t))`.
- `D := (1/2400)∫_0^∞ k^{−8/3}e^{−12k²}E[γ⁶(I − I_quad)(t, χ₀)] dk` (note V24 (5.3)); the integral converges absolutely.
- `κ(c′) := (3c′₊)^{3/2}/6` (#244 Lemma B.2(c)). `φ` and `Q` are the standard normal density and upper tail, and
  `ϑ(a) := E(Z − a)₊ = φ(a) − aQ(a)` for `a ≥ 0`.
- `s := 576√6·k²/|γ|³` is the standard deviation of `χ₀` given `(γ, B)`.

## 1. The averaged second difference

**Lemma 1.** For all real `c′`, `r` and `h`, the second difference `Δ₂` of #244's (4.4) satisfies

    0 ≤ Δ₂ := ½[Φ(c′, r + h) + Φ(c′, r − h)] − Φ(c′, r) ≤ h²/32 + (κ(c′)/2)(|h| − |r|)₊.                       (1.1)

Hence, for `X ~ N(0, s²)` with `s > 0`,

    0 ≤ E[Φ(c′, r + X)] − Φ(c′, r) ≤ s²/32 + κ(c′)·s·ϑ(|r|/s).                                             (1.2)

*Proof.* #244's proof of Lemma B.2(d) writes

    Δ₂ = ½∫_0^{|h|}[∂_RΦ(c′, r + u) − ∂_RΦ(c′, r − u)] du.

- *The bracket.* By Lemma B.2(b), `0 ≤ ∂_R²Φ ≤ 1/16` off `R = 0`. By (c), the derivative jumps by `κ(c′) ≥ 0` at `R = 0`,
  which lies in `(r − u, r + u)` exactly when `|r| < u`. So the bracket lies between `0` and `u/8 + κ(c′)·1{|r| < u}`. In
  particular `Δ₂ ≥ 0`.
- *Integration.* `½∫_0^{|h|} u/8 du = h²/32` and `½∫_0^{|h|} κ·1{u > |r|} du = (κ/2)(|h| − |r|)₊`. That is (1.1). #244's
  (4.4) is the weaker `(κ/2)|h|·1{|r| < |h|}`.
- *(1.2).* `E[Φ(c′, r + X)]` is finite by #244's (2.8). As `X` is symmetric, `E[Φ(c′, r + X)] = Φ(c′, r) + E[Δ₂(c′, r, X)]`.
  Then `E[X²] = s²` and `E[(|X| − |r|)₊] = 2E[(X − |r|)₊] = 2sϑ(|r|/s)`. ∎

## 2. The decomposition

**Proposition 1.** `D ≤ T₁ + T₂ + T₃`, where the three integrals converge absolutely and

    T₁ := (1/2400)∫_0^∞ k^{−8/3}e^{−12k²}E[γ⁶R₂(t)] dk,
    T₂ := (1/32 − 13/486)(1/2400)∫_0^∞ k^{−8/3}e^{−12k²}E[γ⁶s²] dk = (28/15)·12^{−7/6}Γ(7/6),                (2.1)
    T₃ := (1/2400)∫_0^∞ k^{−8/3}e^{−12k²}E[γ⁶κ(1 − t)·s·ϑ(|8 − 12t|/s)] dk.

*Proof.* Fix `k > 0` and `(γ, B)` with `γ ≠ 0`. Then `c′ = 1 − t` and `r = 8 − 12t` are fixed, and `χ₀ ~ N(0, s²)`.
- *Theorem A.* For this fixed `t`, the curve `Δ` meets the line `{t} × R` in at most two points. So Theorem A gives
  `I(t, χ₀) = Φ(c′, r + χ₀)` for all but finitely many `C₃`.
- *The bound.* By (1.2) and `Φ(c′, r) = I₀(t)`,

      E_{C₃}[I(t, χ₀)] ≤ I₀(t) + s²/32 + κ(1 − t)·s·ϑ(|8 − 12t|/s).

  Also `E_{C₃}[I_quad(t, χ₀)] = q₂(t) + (13/486)s²`, since `χ₀` is centred. Subtract, multiply by `γ⁶ ≥ 0`, and integrate
  over `(γ, B)` and then `k`.
- *Fubini applies:*
  - `D`'s integrand is absolutely integrable (note V24).
  - `|R₂(t)| ≤ C|t|³`: near `0` by #244's (3.4), and elsewhere by Lemma B.1(a)'s `|R₂(τ)| ≤ C_R(1 + |τ|³)`. Also
    `E[γ⁶|t|³] = 1728k³E|B|³`.
  - `γ⁶s² = 1990656k⁴`.
  - `κ(1 − t) ≤ C(1 + |t|^{3/2})` and `ϑ ≤ φ(0)`, so `γ⁶κs ≤ Ck²(|γ|³ + (12k|B|)^{3/2})`.

  In each case `k^{−8/3}e^{−12k²}` times the bound is integrable on `(0, ∞)`.
- *The closed form.* `∫_0^∞ k^{4/3}e^{−12k²}dk = ½·12^{−7/6}Γ(7/6)`, and `(1/32 − 13/486)·1990656/(2·2400) = 28/15` (C, group
  T2). ∎

## 3. The line `χ₀ = 0`

**Lemma 2.**
- (a) `R₂` is strictly decreasing on `R`, and `R₂(0) = 0`.
- (b) For every `t ≥ 0`, `R₂ₑ(t) ≤ U(t) := (2/3)t³ + (3√3/2)t^{5/2} + (5√3/2)t^{3/2} + √3·t^{1/2}` and `R₂ₑ(t) ≤ 10t³`.

*Proof.* (a) For `t ≤ 2/3`, write the first line of #244's (3.3) as `R₂ = P₀ + P₁S − q₂`. Here `S = √(1 − 4t/3)`,
`P₀(t) = 11/3 − 21t/2 + 17t²/2 − 4t³/3` and `P₁(t) = (3/2)(1 − t)(2 − 3t)`.
- *`t < 2/3`.* Here `S ∈ (1/3, ∞)` and `t = 3(1 − S²)/4`. Since `dS/dt = −2/(3S)`,
  `16S·R₂′ = 16S·P₀′ + 16S²·P₁′ − (32/3)P₁ − 16S·q₂′`. Substituting `t = 3(1 − S²)/4` gives the polynomial identity (C,
  group R2_monotone)

      16S·R₂′(t) = (S − 1)²W(S),    W(S) := −36S³ − 207S² − 94S + 1.                                       (3.1)

  `W′ < 0` on `S ≥ 0`, and `W(1/3) = −164/3`. So `R₂′ < 0` on `t < 2/3`, except at `t = 0` (`S = 1`).
- *`2/3 < t < 1`.* `R₂′ = (2t − 1)(3 − 2t) + 20 − (104/3)t = 21 − 4(t − 1)² − (104/3)t ≤ 21 − 208/9 < 0`.
- *`t > 1`.* `R₂′ = 1 + 20 − (104/3)t < 0`.

`R₂` is continuous: the pieces of #244's (3.3) agree at `2/3` and at `1` (C). And `R₂(0) = 11/3 + 3 − 20/3 = 0`.

(b) By (a), `R₂(t) ≤ 0` for `t ≥ 0`, so `R₂ₑ(t) ≤ ½R₂(−t)`.
- *`U`.* For `t ≥ 0`, the first line of #244's (3.3) applies at `−t`:

      R₂(−t) = −3 − (19/2)t − (53/6)t² + (4/3)t³ + (3/2)(1 + t)(2 + 3t)·S₊,    S₊ = √(1 + 4t/3) ≤ 1 + (2/√3)√t.

  The factor `(3/2)(1 + t)(2 + 3t)` is positive, so
  `R₂(−t) ≤ (4/3)t³ − (13/3)t² − 2t + √3(2t^{1/2} + 5t^{3/2} + 3t^{5/2})`. Dropping `−(13/3)t² − 2t` gives `2U(t)`.
- *`10t³`, for `t ≥ 1`.* `U(t) ≤ (2/3 + 5√3)t³ ≤ 9.33t³`.
- *`10t³`, for `0 ≤ t ≤ 1`.* By (3.1) at `−u`, `|R₂′(−u)| = (S₊ − 1)²|W(S₊)|/(16S₊)`, with `S₊ = √(1 + 4u/3) ∈ [1, √(7/3)]`.
  - So `16S₊ ≥ 16` and `S₊ − 1 ≤ 2u/3`.
  - Since `W` decreases, `|W(S₊)| ≤ |W(√(7/3))| = 178√(7/3) + 482 ≤ 755`.
  - Hence `R₂(−t) ≤ (755/108)t³ ≤ 7t³`, and `R₂ₑ(t) ≤ 3.5t³`. ∎

## 4. The kink factor

**Lemma 3 (Birnbaum's bound).** For `a ≥ 0`, `Q(a) ≥ 2φ(a)/(a + √(a² + 4))`. Hence

    ϑ(a) ≤ θ⁺(a) := 2φ(a)/(2 + a² + a√(a² + 4)) ≤ φ(a) ≤ φ(0).                                          (4.1)

`θ⁺` is decreasing. For `r ≥ 0`, `s ↦ s·θ⁺(r/s)` is nondecreasing on `s > 0`, and `r ↦ s·θ⁺(r/s)` is nonincreasing.

*Proof.* Let `ω := √(x² + 4)`, `b(x) := (ω − x)/2 = 2/(x + ω)` and `h := Q − φb`.
- *`h > 0`.* With `φ′ = −xφ`, `h′ = φ·(−1 + xb − b′) = φ·(x³ + 3x − (x² + 1)ω)/(2ω)`. Since
  `(x² + 1)²(x² + 4) − x²(x² + 3)² = 4` (C, group mills), `(x² + 1)ω > x³ + 3x ≥ 0` on `x ≥ 0`. So `h′ < 0`. As `h(x) → 0`
  for `x → ∞`, `h > 0` on `[0, ∞)`.
- *(4.1).* `ϑ(a) = φ(a) − aQ(a) ≤ φ(a)(1 − a·b(a)) = φ(a)(2 + a² − aω)/2`, and `(2 + a²)² − a²(a² + 4) = 4` (C) turns this
  into `θ⁺(a)`. `θ⁺ ≤ φ` because its denominator is at least `2`.
- *Monotonicity.* `θ⁺` is a product of positive decreasing factors. For `r > 0`, `s·θ⁺(r/s) = r·θ⁺(a)/a` with `a = r/s`, and
  `θ⁺(a)/a` decreases in `a`. For `r = 0` it is `s·φ(0)`. ∎

## 5. The integrals in the variables `(τ, g, t)`

Write `p(x) := (4π)^{−1/2}e^{−x²/4}` and `m_q(g) := g^q e^{−g²/4}`. `m_q` is log-concave on `g > 0`, with maximum at `g² = 2q`.

**Lemma 4.** Let

    M(τ) := (2/√(4π))∫_0^∞ m_{8/3}(g)e^{−12τ²g⁴} dg,    N(τ) := ∫_0^∞ m_{11/3}(g)e^{−12τ²g⁴} dg,
    K(τ) := ∫_{−∞}^1 e^{−t²/(576τ²)}κ(1 − t) dt.

Then `M` and `N` decrease in `τ`, `K` increases, and

    T₁ = ∫_0^∞dτ ∫_0^∞dt  A₁·τ^{−11/3}M(τ)e^{−t²/(576τ²)}·R₂ₑ(t),                                 A₁ := 1/(14400√(4π)),   (5.1)
    T₃ = ∫_0^∞dτ ∫_0^∞dg ∫_{−∞}^1dt  A₃·τ^{−11/3}m_{8/3}(g)e^{−12τ²g⁴}e^{−t²/(576τ²)}κ(1 − t)·s·ϑ(|8 − 12t|/s),  (5.2)

with `s = 576√6·τ²g` in (5.2) and `A₃ := 1/(57600π)`. (The script calls `A₁` and `A₃` `C1` and `C3`.)

*Proof.* The set `γ = 0` is null. Fix `γ ≠ 0` and substitute `k = τγ²`.
- *The substitution.* `γ⁶k^{−8/3}dk = τ^{−8/3}|γ|^{8/3}dτ` and `e^{−12k²} = e^{−12τ²γ⁴}`. Also `t = 12τB` and `s = 576√6·τ²|γ|`.
- *The densities.* In `t`, `B` has density `p(t/(12τ))/(12τ)`. An even function of `γ` has `E = 2∫_0^∞p(g)(·)dg`.
- *(5.1).* `B ↦ −B` replaces `R₂` by `R₂ₑ` on `t ≥ 0`, with a factor `2`. The constant is `(1/2400)·2·(4π)^{−1/2}/12 = A₁`, and
  the extra `τ^{−1}` turns `τ^{−8/3}` into `τ^{−11/3}`.
- *(5.2).* The constant is `(1/2400)·2(4π)^{−1/2}·(4π)^{−1/2}/12 = A₃`.
- *The order of integration.* It may be changed: by Tonelli for `T₃`, whose integrand is nonnegative, and for `T₁` by
  Proposition 1's absolute convergence.
- *Monotonicity.* This is that of the integrands. ∎

## 6. The enclosure

**Proposition 2.** `T₁ ≤ 0.0951690` and `T₃ ≤ 0.248277`.

*Proof (computer-assisted; §9).* Every bound below is evaluated in decimal arithmetic with 24 significant digits, and each
operation is rounded in the safe direction.

**Cell bounds.** On a box, each factor of (5.1) or (5.2) is monotone in each variable:
- `τ^{−11/3}`, `M` and `N` decrease in `τ`; `e^{−t²/(576τ²)}` increases in `τ` and decreases in `|t|`; `e^{−12τ²g⁴}`
  decreases in `τ` and in `g`;
- `m_q` is unimodal; `κ(1 − t)` decreases in `t`;
- `s·θ⁺(|8 − 12t|/s)` increases in `s` and decreases in `|8 − 12t|` (Lemma 3);
- `sup_{[t₀, t₁]} R₂ₑ ≤ ½(R₂(t₀) + R₂(−t₁))` for `0 ≤ t₀ ≤ t₁` (Lemma 2(a)).

So on a box, the integrand's supremum is at most the product of the factors' suprema. Each supremum is taken at a known corner,
or, for `m_q`, at its peak if the peak lies in the cell. `ϑ` is replaced by `θ⁺` (Lemma 3). The box's integral is at most its
volume times that product. In `T₁`, a cell whose `R₂ₑ`-bound is negative uses the infimum of the weight instead, which is
still an upper bound.

**The partitions.**
- *`T₁`.*
  - `τ` runs from `10⁻⁴` to `τ_N = 1002.77`, each point `1.02` times the last, rounded up to 6 significant digits (814 cells).
  - `t` runs over `0`, then a geometric grid of ratio `1.01` from `10⁻⁷`.
  - On the `τ`-cell `[τ_a, τ_b]` the `t`-cells cover `[0, 12τ_bβ_H]`, with `β_H = 9`; the cells below `0.012τ_a` are merged
    into one.
- *`T₃`, `τ ∈ [0.002, 2.00809]`.* The cells are three-dimensional, with `τ`-ratio `1.02` (349 cells).
  - `g` covers `[0, G]` in 48 equal cells, with `G = min(14, 3(12τ_a²)^{−1/4})` rounded up.
  - `t` covers `[−12τ_bβ_H, 1]` on one fixed grid: step `0.005` on `[−1, 1]`, and relative step `2%` below `−1`.
  - `θ⁺` is read from a decreasing table at `a = j/200`, `j ≤ 8000`, at the largest node `≤ a`.
- *`T₃`, `τ ∈ [2.00809, 1008.04]`.* Here `ϑ ≤ φ(0)`, so the integrand is at most
  `A₃φ(0)·576√6·τ^{−5/3}·m_{11/3}(g)e^{−12τ²g⁴}·e^{−t²/(576τ²)}κ(1 − t)`. On a `τ`-cell this integrates to at most
  `A₃φ(0)576√6·τ_a^{−5/3}N(τ_a)K(τ_b)(τ_b − τ_a)`. The `τ`-ratio is `1.02` (314 cells).
- *One-dimensional factors.* `M`, `N` and `K` are bounded by the same kind of monotone cell sums (`200` or `280` equal
  `g`-cells, or the `t`-grid), each with a closed-form tail. `M` is enclosed from both sides.

**The tails.** These are closed-form bounds; each uses the moments `∫_0^∞e^{−u²/V}u^n du = ½V^{(n+1)/2}Γ((n+1)/2)`. The Gamma
values are bounded crudely: `Γ ≤ 1` on `[1, 2]`, `Γ(3/4) ≤ 4/3`, `Γ(11/12) ≤ 12/11` and `Γ(7/3) ≤ 4/3`.
- *`t` beyond the grid.* For `t ≥ T ≥ 12τ_bβ_H` and `τ ≤ τ_b`,
  `e^{−t²/(576τ²)} ≤ e^{−β_H²/8}e^{−t²/(1152τ_b²)}`.
  - In `T₁`, use `R₂ₑ ≤ U` or `R₂ₑ ≤ 10t³` (Lemma 2(b)), whichever gives the smaller tail.
  - In `T₃`, use `κ(1 + u) ≤ (3^{3/2}/6)(u^{3/2} + (3/2)(1 + u^{1/2}))` and `ϑ ≤ φ(0)`.
- *`g` beyond `G`.*
  `∫_G^∞ m_q e^{−12τ²g⁴} ≤ min(e^{−G²/8}·½8^{(q+1)/2}Γ((q+1)/2), e^{−6τ²G⁴}·¼(6τ²)^{−(q+1)/4}Γ((q+1)/4))`. It is
  combined with `K ≤ K̄`, where `K̄(τ) := (3^{3/2}/6)[1 + ½(24τ)^{5/2}Γ(5/4) + (3/4)(24τ√π + (24τ)^{3/2}Γ(3/4))]`.
- *`τ < 10⁻⁴` in `T₁`.* Use `R₂ₑ ≤ 10t³` and `M ≤ M(0) = 2^{8/3}Γ(11/6)/√π`. This gives
  `≤ 10·A₁M(0)·½·576²·(3/4)·(10⁻⁴)^{4/3}`.
- *`τ > τ_N` in `T₁`.* Use `R₂ₑ ≤ U` and `M(τ) ≤ (2/√(4π))·¼·12^{−11/12}Γ(11/12)·τ^{−11/6}`. The four powers of `U` then
  integrate in closed form.
- *`τ < τ_L = 0.002` in `T₃`.* With `κ(2/3) = 2^{3/2}/6` and `N(0) = ½4^{7/3}Γ(7/3)`:
  - (a) for `t ∈ (1/3, 1]`, the bound is `A₃φ(0)576√6·N(0)·(2/3)κ(2/3)·∫_0^{τ_L}τ^{−5/3}e^{−1/(5184τ²)}dτ`;
  - (b) for `t ≤ 1/3`, `|8 − 12t| ≥ 4`, so `s·ϑ ≤ s·φ(4/s)`, and `g²/8 + 8/(576√6τ²g)² ≥ 2/(576√6τ²)`. The bound is
    `A₃φ(0)576√6·½8^{7/3}Γ(7/3)·K̄(τ_L)·∫_0^{τ_L}τ^{−5/3}e^{−2/(576√6τ²)}dτ`.

  Both integrands increase on `(0, τ_L]`, by the conditions `τ_L² < 6/(5·5184)` and `5·576√6τ_L² < 12` (group tails). So
  each integral is at most `τ_L^{−2/3}` times its exponential at `τ_L`. The total is below `10⁻²⁰`.
- *`τ > 1008.04` in `T₃`.* Use `N(τ) ≤ ¼(12τ²)^{−7/6}Γ(7/6)` and `K ≤ K̄`.

**The result.** The script finds (each part rounded up separately):
- `T₁`: cells `0.0923349`, tails `0.0028342`; total `0.0951690`.
- `T₃`: three-dimensional cells `0.169987`, separable part `0.0748797`, tails `0.0034105`; total `0.248277`.

**What the controls check.**
- *The constants (group lemma4).*
  - Lemma 4's rational parts `A₁√(4π) = (1/2400)·2/12` and `A₃π = (1/2400)·2/12/4` are checked exactly, with the exponent
    bookkeeping.
  - The defining identities of `A₁`, `A₃`, `576√6` and `φ(0)` are checked in interval arithmetic, written independently of
    the lines that build the constants (mutants M11, M15 and M18).
- *The cell code (group corners).*
  - The production loops record the factors they actually use on sampled cells:
    - five `τ`-cells of `T₁`, six `t`-cells each;
    - five `τ`-cells of the three-dimensional part of `T₃`, with five `t`-cells and four `g`-cells each;
    - three `τ`-cells of the separable part, with four `t`-cells each.
  - After the run, each recorded factor is compared with an independent enclosure of the matching factor of the integrand,
    at the cell's corners, edge midpoints and centre: 3,640 one-sided checks.
  - This catches a wrong corner, inside a helper or at a call site (mutants M13, M14, M16 and M17).
- *The normalizations.* The machinery, run on simpler integrands, must bracket closed forms.
  - `t²` in place of `R₂ₑ` in (5.1) brackets `(1/2400)∫k^{−8/3}e^{−12k²}E[γ⁶t²]dk = (576/4800)12^{−1/6}Γ(1/6) = 0.4414541`.
  - `s` in place of `κ(1 − t)·s·ϑ(|8 − 12t|/s)` (that is, `κ = ϑ = 1`), with `t` over all of `R`, in (5.2): separate
    three-dimensional and separable loops bracket `(576√6/2400)(8/√π)·½·12^{−1/6}Γ(1/6) = 4.8806340`.
  - The `t`-cells bracket `∫e^{−t²/(576τ²)}dt = 24τ√π` at five values of `τ`.

  These brackets are wide, with upper/lower ratios `2.14`, `2.59` and `1.56`. They catch an error by a factor outside about
  `[0.74, 1.59]` in `A₁` or `M`, or outside `[0.875, 1.37]` in `A₃·576√6` (mutants M4, M5 and M10).
- *The printed numbers.* Group assembly asserts every certified number, so any change that raises one fails.
- *What no control cross-checks.*
  - The tails, which total `0.0062`. They rest on the derivations above and on Slice C's reading.
  - Cells that are not sampled. The loops treat every cell alike, so a uniform error would show up on the samples.
  - The correctness of libmpdec. ∎

## 7. Proofs of Theorem DC and the corollaries

*Theorem DC.* By Propositions 1 and 2, `D ≤ 0.0951690 + 0.0953759 + 0.248277 ≤ 0.438822` (group assembly; the parts are
rounded up separately). ∎

*Corollary DC1.* By note V24, `Ĩ = Ĩ_quad + D`, with `−Ĩ_quad = (112/675)Γ(1/6)12^{−1/6} ∈ [0.6104056, 0.6104057]` (from
`Γ(1/6)`'s series enclosure). So `Ĩ ≤ −0.6104056 + 0.438822 = −0.1715836 ≤ −0.17158`. With `J ≥ 1/2000` (note V24, Lemma J),
`J/30 − Ĩ ≥ 1/60000 + 0.1715836 ≥ 0.1716002 ≥ 0.17160`. `𝒮_d > 0` by #242's Theorem 1 (group corollary). ∎

*Corollary DC2.* Note V24's Theorem V at `L₀ = 10` gives:
- `|c₃(L) − (J/30)𝒮_d| ≤ η_c𝒮_d` and `|R_{2/3}(L) − Ĩ𝒮_d| ≤ η_R𝒮_d`;
- `(η_c, η_R) = (1.97·10⁻⁷, 4.97·10⁻⁴)` in `d = 3` and `(5.88·10⁻⁹, 7.81·10⁻⁶)` in `d = 2`.

So `(c₃ − R_{2/3})(L) ≥ (0.1716002 − η_c − η_R)𝒮_d ≥ 0.1711𝒮_d` and `R_{2/3}(L) ≤ (−0.1715836 + η_R)𝒮_d ≤ −0.1710𝒮_d` (group
corollary). Note C7's Theorem C7 holds at every `L`, and (C7.1) gives

    ν_eld(ℓ) − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} − ν_eld^{far,r_0^*}(ℓ) = (c₃ − R_{2/3})(L)·ℓ^{2/3} + o(ℓ^{2/3}).

The coefficient is positive. So for each such `L` the left side is positive for `0 < ℓ < ℓ₀(d, L)` and is
`∼ (c₃ − R_{2/3})(L)ℓ^{2/3}`; `ℓ₀` is not quantified. ∎

## 8. Remarks

1. **Where the bound is lost.** Numerically (exploration, outside the repository; Slice A of the author-side referee):
   - `T₁ ≈ 0.04357` and `T₃ ≈ 0.15569`, or `T₃ ≈ 0.16514` with `θ⁺` in place of `ϑ`; `D ≈ 0.07674`.
   - The decomposition costs `T₁ + T₂ + T₃ − D ≈ 0.218`, and all of it is curvature. After averaging, Lemma 1's kink term is
     exact. The distributional second derivative of `Φ(c′, ·)` is `∂_R²Φ(c′, R)dR + κ(c′)δ₀` (B.2(b)–(c)), and the
     Taylor formula gives

         E[Φ(c′, r + X)] − Φ(c′, r) = s²∫_R ∂_R²Φ(c′, r + sv)ϑ(|v|) dv + κ(c′)·s·ϑ(|r|/s).

     So `T₃` is exactly the kink's share of `D`. The loss is `∂_R²Φ ≤ 1/16`, against a weighted mean of `∂_R²Φ` close to
     `1/24` (its value at large `|R|`). This identity is not used in the proof.
   - The cell sums add about `0.05` to `T₁`, whose cells keep the positive and negative parts of `R₂ₑ` apart. They add about
     `0.08` to `T₃` beyond `θ⁺`, and `θ⁺` itself adds `0.009`.
2. **Monte Carlo.** On `[10⁻⁴, 3·10⁻²]` the field-level Monte Carlo of 6033651797 prefers the four-term law, which has C7's
   positive model coefficient, over the three-term law (χ² 84 → 23 in `d = 3`, 44 → 7 in `d = 2`). Corollary DC2 proves the
   sign; it says nothing about the fitted values.
3. **Toward a value.** A two-sided enclosure of `D`, and so a value of note C7's coefficient, could go two ways.
   - *Direct.* Cubature of `I − I_quad`, with cells at the kinks `χ₀ = 12t − 8` and `t = 2/3` and at the curve `Δ`.
   - *Through Remark 1's identity.* It gives `D = T₁ + T₃ − (1990656/4800)∫_0^∞k^{4/3}e^{−12k²}(13/243 − A(k))dk`. Here
     `A(k) := E[∂_R²Φ(1 − t, 8 − 12t + sV)]`, taken over `(γ, B)` at fixed `k` and an independent `V` with density
     `2ϑ(|v|)`. `∂_R²Φ` is bounded (Lemma B.2(b)), and it is scale-invariant by #244's Corollary A.2(c),
     `Φ(λ²c′, λ³R) = λ⁶Φ(c′, R)`. This route needs no cells at the kink.

   Either way, a value also needs an enclosure of note C3's `J`. Note V24 had already called a sign bound a low-precision
   task, since the numerical margin is a factor of about 8.
4. **What changed downstream.** Note V24's *Not claimed* said that "the sign of note C7's coefficient at `L = 24` is not
   proved here". It is now proved, at #244 Theorem A's conditional scope, for every `L ≥ 10`. So at SIDE24 the fourth term
   of note C7's elder law is positive and of exact order `ℓ^{2/3}`.

## 9. Controls (`dc_exact.py`; standard library; deterministic; byte-identical under `-O`)

`python3 -B -S dc_exact.py` and `python3 -B -O -S dc_exact.py` exit `0`. Each prints the same 1117-byte stdout, one JSON line
and its newline, with SHA-256 `2310779578f5a41422b994b7cb826e32b54afc12c74204d732dd569989b6fa11`. Each run takes about 55 s. The script is 47,023 bytes,
SHA-256 `aa84277881b07b445184b7d8db970f0e2d20405f07735e9b021e77e89d7251af`, and it is in the controls comment. The arithmetic is outward-rounded decimal, not exact rational. The
identities are checked in exact rationals.

| Group | What it checks |
|---|---|
| pi, gamma | `π` by Machin's formula in exact rationals. `Γ(a)` for ten values of `a`, by the alternating series of `γ(a, 50)` (220 exact terms; the terms decrease from `n = 49`), plus `0 ≤ Γ(a, 50) ≤ 50^{a−1}e^{−50}` for `a ≤ 1` and `≤ 50^{a−1}e^{−50}/(1 − (a − 1)/50)` for `1 < a ≤ 3`. `Γ(1) = Γ(2) = 1` and `Γ(½)² = π` are enclosed, and so are the crude Gamma bounds of §6 |
| R2_formula | the pieces of #244's (3.3) agree at `2/3` and `1`; `R₂(0) = 0`; `R₂(t)/t³ ∈ (−3.2, −3.0)` at `t = 10⁻³, 10⁻²` |
| R2_monotone | the identity (3.1); `W(1/3) < 0` and `W′ ≤ 0`; the derivatives on `(2/3, 1)` and `(1, ∞)`, as polynomials, and their bounds |
| R2_majorant | the expansions of `R₂(−t)` and `P₁(−t)` in Lemma 2(b); `|W(√(7/3))| ≤ 755`; `(1 + 2u/3)² − (1 + 4u/3) = 4u²/9`; `(4/9)(755/16)/3 = 755/108 ≤ 7`; `2/3 + 5√3 ≤ 10` |
| mills | `(x² + 1)²(x² + 4) − x²(x² + 3)² = 4`, `(x² + 2)² − x²(x² + 4) = 4`, and Lemma 3's two reductions modulo `ω² = x² + 4` |
| theta_table | the table is decreasing; at eleven test points, `θ⁺(a)` is below its table entry |
| T2 | `(1/32 − 13/486)·1990656/4800 = 28/15`; `T₂ ∈ [0.0953758, 0.0953759]` |
| lemma4 | Lemma 4's exponent bookkeeping and rationals `A₁√(4π) = 1/14400`, `A₃π = 1/57600` (exactly); `A₁²·14400²·4π`, `A₃·57600π`, `(576√6)²/(576²·6)` and `φ(0)²·2π` all enclose `1` |
| gstar | the peaks of `m_{8/3}` and `m_{11/3}` at `g² = 16/3` and `22/3` |
| g_machinery | the `g`-cell enclosures of `M(0⁺)` and `N(0⁺)` contain `2^{8/3}Γ(11/6)/√π` and `½4^{7/3}Γ(7/3)` |
| corners | after the run: every factor the production loops used on a sampled cell dominates (for a negative `T₁` cell, the weight is dominated by) the integrand's matching factor at the cell's corners, edge midpoints and centre (§6) |
| T1_moment, T3_moment, t_machinery | the normalization brackets of §6 |
| partition | every grid increases; consecutive cells share endpoints; every `t`-range reaches `12τ_bβ_H` |
| tails | the monotonicity conditions used for `τ < 0.002` |
| assembly | `T₁ ≤ 0.0951690`, `T₃ ≤ 0.248277`, `D ≤ 0.438822 ≤ 0.61` |
| corollary | `−Ĩ_quad ∈ [0.6104056, 0.6104057]`; `Ĩ ≤ −0.17158`; `J/30 − Ĩ ≥ 0.17160`; for `d = 2, 3`, the coefficient `≥ 0.1711` and `R_{2/3} ≤ −0.1710` (in units of `𝒮_d`). Lower bounds are printed rounded down, upper bounds rounded up |

Eighteen mutants each exit `1`, with empty stdout and `FAILED: <group>` on stderr:

| Mutant | Change | Group |
|---|---|---|
| M1 | `−207 → −206` in `W` | R2_monotone |
| M2 | `x² + 4 → x² + 3` in Lemma 3's identity | mills |
| M3 | `13/486 → 13/480` | T2 |
| M4 | `A₁` doubled | T1_moment |
| M5 | `A₃` doubled | T3_moment |
| M6 | `17/2 → 8` in `P₀` | R2_formula |
| M7 | one `τ`-cell of `T₁` skipped | partition |
| M8 | Gamma series truncated at 20 terms | gamma |
| M9 | table index rounded up | theta_table |
| M10 | `M`'s factor `2/√(4π) → 2/(4π)` | g_machinery |
| M11 | `576√6 → 576√3` | lemma4 |
| M12 | `T₁`'s `t`-range halved | partition |
| M13 | `s` taken at `τ_a` instead of `τ_b` | corners |
| M14 | `κ(1 − t)` taken at the right end of the `t`-cell | corners |
| M15 | `12 → 6` in `A₁`'s rational | lemma4 |
| M16 | `T₁`'s `τ`-factor taken at `τ_b` | corners |
| M17 | the three-dimensional loop passes the `g`-cells' `θ⁺` indices in reverse order (a call-site error) | corners |
| M18 | `φ(0) = 1/√(2π) → 1/√(4π)` | lemma4 |

Invalid invocations exit `2` with `usage: dc_exact.py [--mutant M1..M18]`: `M0`, `M19`, a bare `--mutant`, an extra argument,
and an unknown flag.

## 10. Review slices

- **A: §§0–2 and §4.** Lemma 1, Proposition 1 (the decomposition, Fubini and `T₂`'s closed form) and Lemma 3. Groups mills
  and T2; mutants M2 and M3.
- **B: §§3 and 5.** Lemma 2 (monotonicity and the majorants) and Lemma 4 (the change of variables, the constants `A₁` and
  `A₃`, and the monotonicity of `M`, `N` and `K`).
  - Groups R2_formula, R2_monotone, R2_majorant, lemma4, T1_moment and T3_moment.
  - Mutants M1, M4, M5, M6, M11, M15 and M18.
- **C: §§6–7, the header and the controls.**
  - Proposition 2: the cell bounds, the partitions, every tail and the rigor of the arithmetic.
  - Theorem DC and Corollaries DC1–DC2, against note V24's table and note C7.
  - The remaining groups; mutants M7–M10, M12–M14, M16 and M17.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_