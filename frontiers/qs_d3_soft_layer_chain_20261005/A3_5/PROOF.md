## QS addendum A3.5: the `d = 3` analytic good event at the `r³` rare-layer scale (C91 (W4) and C93 §§3–4 in `d = 3`, with C92 (J6)–(J7))

**Object.** `CL-QS-A3-5-GOOD-EVENT-20261005-v1`.

**Who.** Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, the author of QS and A3–A3.4. Dylan Roy — delegated AI work.

**Claim.** This delivers claim [5999339489](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999339489) and releases it. Author-side. Scientific effect: NONE. The executable and its stdout are in a companion controls comment, posted right after this one.

**Consumed (merged; read, not edited).**
- **C91** (`frontiers/planar_soft_layer_chain_20261003/C91/PROOF.md`, blob `92c9c479`): Theorem 1, (W3)–(W5), applied on the plane `η = 0`. Its proof (W6)–(W11) is re-run in `d = 3`: (W9) also for the hard direction, (W10) for the three-dimensional remainder. Also the matrix of (W15).
- **C92** and **C93** (same folder, `C92/PROOF.md` blob `4f6598a1`, `C93/PROOF.md` blob `204fd6f3`): the arguments of C92 (J6)–(J7), (J20) and C93 §§3–4, (E13)–(E20), re-run here in `d = 3`. Only their arguments are reused, not their `d = 2` statements.
- **#243** (`frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7b`): the eigenframe, the jets (0.2) and the chart (0.4).

**Consumed (author-side, reviewed).**
- **A3** ([5970263575](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5970263575)): Lemma SR, and the hypotheses (B1)–(B3), (E1_d)–(E3_d) of QS-E′_d and QS-R_d.
- **A3.1** ([5971014231](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971014231)): Lemma SR′ and its proof; QS §7's identity `G_k(X, ζ) = P_QS(X + γζ/12, γζ)`; Theorem C_d; Remark M.
- A3 and A3.1 are read with the erratum [5998430951](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5998430951). All three readbacks of that erratum PASS.
- **A3.4** ([5999129544](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999129544)): the density identity (J₃.18), the moment bound (E₃.7), (J₃.4)–(J₃.5) and (E₃.6).
  - Its reads: slice 1 PASS; slices 2 and 3 AMEND (wording and bookkeeping), with the mathematics PASS_SCOPED.
  - The amendments are applied in the successor [5999301338](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5999301338), whose three readbacks PASS.
  - A3.4's actual-measure statements are conditional on A3.3 ([5998500022](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5998500022)).
- **A3.3's reads:** S1 PASS_SCOPED; S2 PASS_ANALYTIC_SCOPED; S3 PASS. S2's control correction A33-S2-C1 is applied in [6000124833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6000124833) and was read back PASS by Grok Bot agent 2 ([6000234028](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6000234028)).

§§1–3 below are deterministic. They use C91's Taylor argument and the proofs of A3's Lemma SR and A3.1's Lemma SR′, and nothing probabilistic. §4 is conditional on A3.4, and through it on A3.3.

**What is new.**
1. **Lemma FW₃**, the `d = 3` analogue of C91 (W4)–(W5). The remainder `E` of A3.1's FL.1′ satisfies `|E|_j ≤ K_j^{(3)} N r w^{4−j}` (`j ≤ 2`) on the cube `{|X|, |ζ|, |η| ≤ w}`. The constants are explicit, and only a `C⁴` norm is used. A blockwise form holds on a barrel box whose hard side may be much longer than `w`. FL.1′ left the dependence on `w` implicit.
2. **Proposition D₃**, the reduced height on growing windows, in raw coordinates:
   - `sup|G − G_k| ≤ Nrw⁴(K₀ + C_e kN/λ₂)` and `sup‖D²(G − G_k)‖ ≤ Nrw²(D_h + C_h kN/λ₂)`, with explicit constants;
   - all barrel conditions follow from the single event `λ₂ > C_B kN²rw⁴`;
   - there is no factor `1/γ`, and no lower bound `w ≥ ε`.
3. **Lemma T₃**, C93 (E13)/(E16) in `d = 3`: the normalized Hessian error is at most `L_i` times the raw one, with `L_i = 1/3 + (γ² + 144)/(12a_i)`. The chart's `1/γ` cancels.
4. **Theorem G₃** (conditional on A3.4), C93 (E14)–(E15) and (E18)–(E20) in `d = 3`. On the soft layer the analytic good event has `Q_r^W(D_Λ ∖ G₃) ≤ C[r⁴ + r⁵w⁴ + r⁶w⁸ + r⁷w^{16} + r³(rw⁴)^p]`. So `Q_r^W(G₃ | D_Λ) = 1 − O(r)` for `w = r^{−β}` with `0 ≤ β ≤ 3/16`. The two new terms come from the hard gap, and `3/16` is sharp for `G₃` (Remark 1 after the theorem).
5. **Corollary FW₃′** (conditional on A3.4), C92 (J6)–(J7) in `d = 3`; and **Lemma E₃⁺** (conditional on A3.4), A3.4's (E₃.2) with the hard eigenvalue kept in the integrand.

### 0. Setting and notation

- **As in A3.4 §0.**
  - `d = 3`; the pins, `Q_r`, `W_r`, `Z_r`, `Q_r^W`; the spectral coordinates `(λ̃, λ₂, θ, t)`; the eigenframe `(u, e₁, e₂)`.
  - The jets `γ, B, C₃`, and `γ₂ := ∂_u²∂_{e₂}f(0)`, `β₂ := ∂_u∂_{e₁}∂_{e₂}f(0)`, `ν₂ := ∂_{e₁}²∂_{e₂}f(0)`.
  - `Y`, `a_M`, `a_S`, `D_Λ`, `T = {λ₂ > 0, a_M > 0, a_S > 0}`, `h`, `A_* = 12Λ` and the polynomial weight `P = 1 + |λ₂| + |t|`.

  Here `Λ` is always the soft-layer cutoff. Constants depend only on `L`, `B₀`, `k_±`, `Λ` and the stated budgets and exponents. They are uniform in `b`, `k`, the frame and `0 < r ≤ r₀`, and `r₀ ≤ 1`.
- **Changes of letters.**
  - A3.4's model weight `w = (a_M)₊(a_S)₊` is written `w_λ` here. The letter `w` is the window size, as in C91–C93.
  - QS's planar cubic is written `P_QS`, and A3's barrel curvature is written `Λ_b`.
  - The hard coefficient is A3.1's `a_i` with `i = 2`, written `a₂`. It is unrelated to the typing quantities `a_M`, `a_S` and `a_i` (`i ∈ {M, S}`).
- **The field norm.** `N := 1 + max_{0≤m≤4} sup_{torus} ‖D^m f‖`, with operator norms of the symmetric `m`-linear forms. It bounds every coordinate partial of order at most 4 in every orthonormal frame, in particular in the eigenframe. A3.4's `N` (frame partials) satisfies `N_{A3.4} ≤ N ≤ 9N_{A3.4}`, since `‖D^m f‖ ≤ 3^{m/2} max|∂^α f|`. So (J₃.10) and (E₃.7) hold for this `N` with constants multiplied by `9^p`.
- **The chart.** `Φ(X, ζ, η) := rXu + rkζe₁ + r^{3/2}ηe₂` and `𝔉 := (f∘π∘Φ − b)/(kr³)` (#243 (0.4)). The model is `G_k(X, ζ) − (λ₂/(2k))η² + r^{1/2}η·a₂(X, ζ)`, with
  - `G_k = 2X³ − 3X/2 − 1/2 + (γ/2)(X² − ¼)ζ − (λ̃/2)ζ² + (kB/2)Xζ² + (k²C₃/6)ζ³` (#243 (0.2));
  - `a₂ = (γ₂/(2k))(X² − ¼) + β₂Xζ + (k/2)ν₂ζ²` (A3.1 §4).

  The error is `E := 𝔉 − G_k + (λ₂/(2k))η² − r^{1/2}η·a₂`. This is A3.1's FL.1′ remainder, written in raw coordinates.
- **Windows.** `Ω_w := {|X| < w, |ζ| < w}`; the cube `𝒲_w := {|X|, |ζ|, |η| ≤ w}`; the barrel box `𝒲_{w,v} := Ω̄_w × [−v, v]`. For a function on a window, `|E|_j` is the largest supremum of an exact-order-`j` coordinate derivative, as in C91.
- **C91's constants.** `M1 := max(1/k₋, 1)`, `M2 := max(1/k₋, 1, k₊)`, and (W3) with `H = 1 + k₊`:
  - `K₀ = 9/(64k₋) + 1/16 + (1 + k₊)⁴/(24k₋)`;
  - `K₁ = 33/(128k₋) + 1/16 + M1(1 + k₊)³/6`;
  - `K₂ = 17/(48k₋) + 1/24 + M2(1 + k₊)²/2`.

### 1. Lemma FW₃ (the window error in `d = 3`)

Put `H₃ := 2 + k₊` and
- `K₀^{(3)} := 9/(64k₋) + 1/16 + 35/(48k₋) + 1/2 + H₃⁴/(24k₋)`,
- `K₁^{(3)} := 33/(128k₋) + 1/16 + 25/(16k₋) + 1 + M1H₃³/6`,
- `K₂^{(3)} := 17/(48k₋) + 1/24 + 49/(24k₋) + 1 + M2H₃²/2`,
- `A₁ := (1/48 + 1/24 + (1 + k₊)³/6)/k₋`, `A₂ := 1 + 2/k₋`, `A₃ := 1/(24k₋) + (1 + 1/k₋)H₃²/2`, `A₄ := max(1 + 2/k₋, H₃ max(1, k₊))`,
- `c₀ := 5/(8k₋) + 1 + k₊/2`, `c₁ := 2 + 1/k₋ + k₊`, `c₂ := 1 + max(1/k₋, k₊)`.

At `k₋ = k₊ = 1`: `K^{(3)} = (923/192, 945/128, 127/16)`, `(A₁, A₂, A₃, A₄) = (67/48, 3, 217/24, 3)` and `(c₀, c₁, c₂) = (17/8, 4, 2)`.

**Lemma FW₃.** Let `f ∈ C⁴` have the exact pins, and let `0 < r ≤ 1` and `w ≥ 1`. No Gaussian or nondegeneracy hypothesis is used.
- **(i) The cube.** On `𝒲_w`, `|E|_j ≤ K_j^{(3)} N r w^{4−j}` for `j = 0, 1, 2`.
- **(ii) The barrel box.** Let `v ≥ 0` with `r^{1/2}v ≤ w`. Then:
  - **(FW.0)** `|E(·, ·, 0)|_j ≤ K_j N r w^{4−j}` on `Ω̄_w`, for `j = 0, 1, 2` (planar derivatives);
  - **(FW.1)** `|E_η(·, ·, 0)| ≤ A₁ N r^{3/2} w³` on `Ω̄_w`;
  - **(FW.2)** `|E_ηη| ≤ A₂ N r w` on `𝒲_{w,v}`;
  - **(FW.3)** `|E_Xη| + |E_ζη| ≤ N r[(1 + 1/k₋)v + A₃ r^{1/2}w²]` on `𝒲_{w,v}`;
  - **(FW.4)** `|E_XX|, |E_Xζ|, |E_ζζ| ≤ (K₂ + A₄) N r w²` on `𝒲_{w,v}`.
- **(iii) The hard coefficient.** On `Ω̄_w`: `|a₂| ≤ c₀Nw²`, `|∂_X a₂| + |∂_ζ a₂| ≤ c₁Nw` and `‖D²a₂‖ ≤ c₂N`.

*Proof.*
1. **Taylor in the eigenframe.** Let `𝒯f` be the cubic Taylor polynomial of `f` at `0` in coordinates `(x, y₁, y₂)` along `(u, e₁, e₂)`.
   - As in C91 (W10), for `|α| = m ≤ 2`, `|D^α(f − 𝒯f)(x)| ≤ N|x|₁^{4−m}/(4−m)!`.
   - In the chart, `|Φ|₁ = r|X| + rk|ζ| + r^{3/2}|η|`. This is at most `r(2 + k)w ≤ rH₃w` on `𝒲_w`, and also on `𝒲_{w,v}` because `r^{3/2}v ≤ rw`.
   - A chart derivative of order `m`, with `j` derivatives in `ζ` and `l` in `η`, multiplies by `r^{m−j−l}(rk)^j r^{3l/2}/(kr³)`. So the remainder contributes at most `N k^{j−1} r^{1+l/2}(H₃w)^{4−m}/(4−m)! ≤ N r k^{j−1}(H₃w)^{4−m}/(4−m)!`.

   These are the last summands of the `K_j^{(3)}`.
2. **The pinned coefficients.** Along the axis, C91 (W7)–(W8) hold verbatim. For both transverse directions, C91 (W9) gives `|∂_{e_i}f(0) + r²γ_i/8| ≤ Nr³/48` and `|∂_u∂_{e_i}f(0)| ≤ Nr²/24`, with `γ₁ = γ`. The eigenframe gives `∂_{e₁}∂_{e₂}f(0) = 0` and `∂_{e₂}²f(0) = −λ₂` exactly. No fifth derivative is used.
3. **The polynomial part.** After division by `kr³`, `𝒯f` minus the model is a combination of C91's six monomials and five hard monomials:

   | monomial | coefficient`/(Nr)` at most | `m = 0` | `m = 1` | `m = 2` |
   |---|---|---|---|---|
   | `η` | `1/(48k₋)` | 1 | 1 | 0 |
   | `Xη` | `1/(24k₋)` | 1 | 1 | 1 |
   | `Xη²` | `1/(2k₋)` | 1 | 2 | 2 |
   | `ζη²` | `1/2` | 1 | 2 | 2 |
   | `η³` | `1/(6k₋)` | 1 | 3 | 6 |

   - The rows `η` and `Xη` come from step 2, and the row `η³` is the jet `∂_{e₂}³f(0)` with chart factor `r^{3/2}/(6k)`. All three use `r^{1/2} ≤ 1`. The rows `Xη²` and `ζη²` are third-order jets, at most `N`.
   - The monomials `x²y₂`, `xy₁y₂` and `y₁²y₂`, together with the pin term `−r²γ₂/8`, give `r^{1/2}η·a₂` exactly. The term `y₂²` gives `−(λ₂/(2k))η²` exactly.
   - As in C91, the columns bound exact-order-`m` derivatives on `𝒲_w` after division by `w^{4−m}`, for `w ≥ 1`. Their weighted sums are `35/(48k₋) + 1/2`, `25/(16k₋) + 1` and `49/(24k₋) + 1`.

   With C91's column sums and step 1, this proves (i).
4. **(FW.0).** On `η = 0`, `E` is C91's `F_r − G_k` for the planar section `(x, y₁) ↦ f(xu + y₁e₁)`. C91's proof of Theorem 1 uses only Taylor's theorem at `0` and on the pin segment, so it applies to the section. The section has the planar pins, and its `N` is at most ours.
5. **(FW.1).** Put `Q(x, y₁) := ∂_{e₂}f(xu + y₁e₁)`. Then `E_η(X, ζ, 0) = (Q(rX, rkζ) − r²k·a₂(X, ζ))/(kr^{3/2})`.
   - Expand `Q` to order 2 at `0`; its third derivatives are at most `N`.
   - Its jets are `Q(0) = ∂_{e₂}f(0)`, `Q_x(0) = ∂_u∂_{e₂}f(0)`, `Q_{y₁}(0) = 0`, `Q_xx = γ₂`, `Q_{xy₁} = β₂` and `Q_{y₁y₁} = ν₂`.
   - So `|Q − r²ka₂| ≤ Nr³[1/48 + |X|/24 + (|X| + k|ζ|)³/6]`, by step 2.
6. **(FW.2).** `E_ηη = [∂_{e₂}²f(Φ) − ∂_{e₂}²f(0)]/k`. The mean value theorem bounds this by `N|Φ|₁/k ≤ N r w(2 + k)/k`, using `r^{1/2}v ≤ w`.
7. **(FW.3).** Put `p := ∂_u∂_{e₂}f` and `p′ := ∂_{e₁}∂_{e₂}f`. Expanding both to first order,
   - `E_Xη = [p(0) + r^{3/2}∂_u∂_{e₂}²f(0)·η + R₂(Φ)]/(kr^{1/2})`;
   - `E_ζη = [r^{3/2}∂_{e₁}∂_{e₂}²f(0)·η + R₂′(Φ)]/r^{1/2}`, since `p′(0) = 0`.

   Here `|p(0)| ≤ Nr²/24` (step 2) and `|R₂|, |R₂′| ≤ N|Φ|₁²/2 ≤ Nr²H₃²w²/2`.
8. **(FW.4).** At `η = 0` these are C91's bounds `K₂Nrw²`. Moreover
   - `∂_ηE_XX = r^{1/2}k^{−1}[∂_u²∂_{e₂}f(Φ) − γ₂]`;
   - `∂_ηE_Xζ = r^{1/2}[∂_u∂_{e₁}∂_{e₂}f(Φ) − β₂]`;
   - `∂_ηE_ζζ = r^{1/2}k[∂_{e₁}²∂_{e₂}f(Φ) − ν₂]`.

   By the mean value theorem and `|Φ|₁ ≤ r(2 + k)w`, each is at most `N r^{3/2} w(2 + k)` times `1/k`, `1` or `k`. Integrating over `|η| ≤ v ≤ r^{−1/2}w` adds at most `max_{k∈[k₋,k₊]}(2 + k)max(1/k, 1, k)·Nrw² = A₄Nrw²`.
9. **(iii).** Use the triangle inequality with `|γ₂|, |β₂|, |ν₂| ≤ N` and `w ≥ 1`. ∎

**Remarks.**
- **The window powers cannot be lowered.** Add `−(λ₂/2)y₂²` to C91's family (W12). The error is then C91's exact `(tr/k)(X² − ¼)²` for every `η`, so C91 §1.3's obstruction applies to (i) and to (FW.0).
- **The hard side may exceed `w`.** In (ii) the box `𝒲_{w,v}` allows `v` up to `r^{−1/2}w`. Proposition D₃ uses this with `v = ε = 4√(k/λ₂)`.
- **The constants are nearly attained** (§7). Exactly pinned near-extremal families reach 98–99.9% of the bounds (FW.1)–(FW.2), and 91–98% of (FW.0), (FW.3) and (FW.4).

### 2. Lemma SR′_b and Proposition D₃ (the reduced height on growing windows)

**Lemma SR′_b (A3.1's Lemma SR′ with blockwise budgets).** Take A3.1 §5's setting with its planar model written `G₀`: `g = G₀ − ½zᵀQ_hz + s z·a + E` near `Ω × B̄_ε`, with a constant `Q_h ⪰ Λ₀I` and `α_j` as there. Let the budgets be:
- `δ₀ ≥ sup_Ω|E(·, 0)|` and `δ₁ ≥ sup_Ω|E_z(·, 0)|`;
- `δ_zz ≥ sup‖E_zz‖`, `δ_xz ≥ sup‖E_xz‖` and `δ_xx ≥ sup‖E_xx‖`, over `Ω × B̄_ε`.

Put `Λ_b := Λ₀ − δ_zz > 0`, and suppose `sα₀ + δ₁ < Λ_bε/2`. Then (B1) and (B2) hold with `Λ_b`, and with `e_G := G − G₀`:

    |e_G| ≤ δ₀ + (sα₀ + δ₁)²/(2Λ_b),        ‖D²e_G‖ ≤ δ_xx + sα₂(sα₀ + δ₁)/Λ_b + (sα₁ + δ_xz)²/Λ_b.             (SR′_b)

*Proof.* This is A3.1's proof of SR′ with the budgets kept apart.
- (B1) uses only `E_zz`.
- (B2) and the value bound use only `E(·, 0)` and `E_z(·, 0)`, through SR(b).
- The Hessian bound reads `E_xx` and `E_xz` at `(x, ζ(x))`, where `|ζ(x)| < ε/2`. ∎

**Proposition D₃.** Let `0 < r ≤ 1` and `w ≥ 1` with `r^{1/2}w ≤ 1`. Put `Ω := Ω_w`, `ε := 4√(k/λ₂)` and `ξ := kN/λ₂`, and set

    C_B := max(16, 2A₂, (c₀ + A₁)²),    C_e := (c₀ + A₁)²,    D_h := 2(K₂ + A₄),
    c₃ := c₁ + 1 + 1/k₋ + A₃,    C_h := 2c₂(c₀ + A₁) + 2c₃².

At `k₋ = k₊ = 1`: `C_B = 16`, `C_e = 28561/2304`, `D_h = 259/24` and `C_h = 134377/288`. Suppose

    λ₂ > C_B k N² r w⁴.                                                                                        (B_r)

Then:
- **(a) The barrel.** `r^{1/2}ε < w`. On `Ω × [−ε, ε]`, `g := 𝔉` satisfies (B1)–(B3) with `Λ_b := λ₂/k − A₂Nrw > λ₂/(2k)`. So A3's Lemma SR applies, and the reduced height `G(X, ζ) := max_{|η|≤ε} 𝔉(X, ζ, η)` is defined and `C²` on `Ω`.
- **(b) The bounds.** In raw coordinates, with operator norms,

      sup_Ω |G − G_k| ≤ N r w⁴ (K₀ + C_e ξ),        sup_Ω ‖D²(G − G_k)‖ ≤ N r w² (D_h + C_h ξ).                (D₃)

  No factor `1/γ` appears.

*Proof.* Apply Lemma SR′_b with `x = (X, ζ)`, `z = η`, `G₀ = G_k`, `Q_h = λ₂/k`, `s = r^{1/2}` and the hard coefficient `a₂`. Lemma FW₃(ii) with `v = ε` gives the budgets:
- `δ₀ = K₀Nrw⁴`, `δ₁ = A₁Nr^{3/2}w³`, `δ_zz = A₂Nrw`;
- `δ_xz = Nr[(1 + 1/k₋)ε + A₃r^{1/2}w²]` and `δ_xx = 2(K₂ + A₄)Nrw²`, since a `2 × 2` operator norm is at most twice the largest entry;
- `α₀ = c₀Nw²`, `α₁ = c₁Nw` and `α₂ = c₂N`, by FW₃(iii).

1. **(a).**
   - Since `N, w ≥ 1`, (B_r) gives `λ₂ > 16kr/w²`, that is `r^{1/2}ε < w`.
   - (B_r) also gives `δ_zz < λ₂/(2k)`, so `Λ_b > λ₂/(2k)`.
   - Next, `sα₀ + δ₁ ≤ r^{1/2}Nw²(c₀ + A₁rw) ≤ r^{1/2}Nw²(c₀ + A₁)`, since `rw ≤ r^{1/2}w ≤ 1`. By (B_r) this is `≤ √(λ₂/k) < Λ_bε/2`.
   - Finally `Λ_bε² > (λ₂/(2k))(16k/λ₂) = 8`, which is (B3).
2. **The value bound.** `δ₀ + (sα₀ + δ₁)²/(2Λ_b) ≤ K₀Nrw⁴ + (c₀ + A₁)²rN²w⁴·k/λ₂`.
3. **The Hessian bound.**
   - By (B_r), `rk/λ₂ < 1/16`, so `rε = 4r^{1/2}(rk/λ₂)^{1/2} < r^{1/2}`. Also `r^{3/2}w² ≤ r^{1/2}w`. Hence `sα₁ + δ_xz ≤ c₃Nr^{1/2}w`.
   - With `1/Λ_b < 2k/λ₂`, the two quotients in (SR′_b) are at most `2c₂(c₀ + A₁)Nrw²ξ` and `2c₃²Nrw²ξ`. ∎

**Remarks.**
1. **No lower bound on `w`.** The barrel's hard side `ε` may exceed `w`, up to `r^{−1/2}w`. A3.1's Theorem C_d assumed `w ≥ ε` only so that FL.1′ could be applied on a cube.
2. **Against A3.1's "Orders".** There, `Ξ₀, Ξ₂ ≤ C″χ_γ²N(1 + kN/λ₂)r` at fixed `w`. (D₃) makes the dependence on `w` explicit and drops `χ_γ`, because it works in raw coordinates. The dependence on `γ` moves to `L_i` in Lemma T₃.
3. **The mechanism.** By SR(b), pointwise `0 ≤ G(x) − 𝔉(x, 0) ≤ q₀(x)²/(2Λ_b)`, with `q₀(x) = |r^{1/2}a₂(x) + E_η(x, 0)|`. To leading order the bound is `rk·a₂(x)²/(2λ₂)`. For the model field (`E ≡ 0`) this is the exact value. #242 §2's "Consistency with Theorem 1" computes it formally.

### 3. Lemma T₃ (the normalized Hessian transfer)

On `T ∩ {γ ≠ 0}`, put `κ_i := a_i/(12γ²)`, `J_i := diag(1/√3, 1/√κ_i)` and

    T_i := [[1, −1/12], [0, 1/γ]] J_i = [[1/√3, −1/(12√κ_i)], [0, 1/(γ√κ_i)]],    i ∈ {M, S}.             (T₃.1)

- These `κ_i` are QS §1's: `κ_S = (ψ + c)/48 = a_S/(12γ²)` and `κ_M = (ψ − c)/48 = a_M/(12γ²)`, with QS §7's `ψ = 24λ̃/γ²` and `c = 1 − 12kB/γ²`.
- C91's (W15) is the same matrix. C91's `a_i` is `4a_i`, the normalization of C93.

**Lemma T₃.** Let `φ(u, Z) := (u − Z/12, Z/γ)` be QS §7's chart. For every `C²` function `e` of `(X, ζ)`, `J_i D²_{(u,Z)}(e∘φ) J_i = T_iᵀ (D²e∘φ) T_i`. Hence, on `(B_r) ∩ T ∩ {γ ≠ 0}`,

    H_i := sup_Ω ‖T_iᵀ D²(G − G_k) T_i‖ ≤ L_i N r w² (D_h + C_h ξ),        L_i := ‖T_i‖_F² = 1/3 + (γ² + 144)/(12a_i).   (T₃.2)

`H_i` bounds `‖J_i D²e_G J_i‖` on every set whose raw image lies in `Ω`. In particular it bounds A3's (E2_d) and (E3_d) on `E_S` and `E_M` when their raw images lie in `Ω`.

*Proof.* `φ` is linear with matrix `[[1, −1/12], [0, 1/γ]]`, so the first identity is the chain rule. Next, `‖TᵀMT‖ ≤ ‖T‖²‖M‖ ≤ ‖T‖_F²‖M‖`. Finally, `‖T_i‖_F² = 1/3 + 1/(144κ_i) + 1/(γ²κ_i) = 1/3 + (γ² + 144)/(144γ²κ_i)`, and `144γ²κ_i = 12a_i`. ∎

As in C91 (W16), the apparent `1/γ` cancels. `L_i` keeps only the typing-edge pole `1/a_i`, and `γ = 0` stays outside the chart. C93's `L_i` is `3L_i`, and C91's bound `(2ε₂/3)[1 + (γ² + 144)/a_i^{C91}]` is `2ε₂L_i`.

### 4. The weighted failure bounds (conditional on A3.4)

**Lemma E₃⁺ (the joint edge–gap majorant).** For `i ∈ {M, S}`, finite `m, q ≥ 0` and nonnegative measurable `φ` on `(0, A_*) × (0, ∞)`:

    r^{−5} E_{Q_r}[W_r N^m P^q 1_{D_Λ∩T} φ(a_i, λ₂)] ≤ C_{m,q} ∫₀^∞ ∫₀^{A_*} φ(y, λ₂) λ₂(λ₂²y + r) e^{−cλ₂²} dy dλ₂.     (E₃⁺)

If `φ` depends on `λ₂` alone, the right side can be replaced by `C∫₀^∞ φ(λ₂) λ₂(λ₂² + r) e^{−cλ₂²} dλ₂`.

*Proof.* This is the proof of (E₃.2), keeping `λ₂` in the integrand. Use (J₃.18) with `F = P^q1_Tφ(a_i, λ₂)` and the moment `N^m`, then (E₃.7). On `T`:
- `λ̃ > 0`, so `(λ₂ − rλ̃/k)₊ ≤ λ₂`;
- `w_λ = y(12λ̃ − y) ≤ 12Λy` with `y = a_i`;
- the change of variables `B → y` holds `(λ̃, λ₂, θ, γ)` and the other jets fixed, with Jacobian at most `1/(3k₋)` (A3.4 §5, step 1).

`ρ_r(Ψ_r, t) ≤ Ce^{−c(λ₂²/2 + |t|²)}` absorbs `P^{m+q+25}` into half of its exponent. The remaining integrals over `λ̃ ∈ (0, Λ]`, `θ` and the other jets are bounded. For `φ = φ(λ₂)`, integrate `y` over `(0, A_*)`. ∎

**Corollary FW₃′ (C92 (J6)–(J7) in `d = 3`).** For finite `p ≥ 1`, deterministic `τ > 0` and `w ≥ 1`, `0 < r ≤ r₀` and `j ∈ {0, 1, 2}`, with `|E|_j` over `𝒲_w`:

    Q_r^W(D_Λ ∩ {|E|_j > τ}) ≤ C_p r³ (K_j^{(3)} r w^{4−j}/τ)^p.                                              (FW₃′.1)

If `w = r^{−β}` and `τ = r^ς` with `β, ς ≥ 0` and `4β + ς < 1`, a union over `j` gives `Q_r^W(D_Λ ∩ {max_j |E|_j > r^ς}) ≤ C_p r^{3+p(1−4β−ς)} = o(r³)`.

*Proof.* By FW₃(i), `1{|E|_j > τ} ≤ (K_j^{(3)}Nrw^{4−j}/τ)^p`. By (J₃.18) and (E₃.7), `r^{−5}E_{Q_r}[W_rN^p1_{D_Λ}] = ∫_{D_Λ} g_r^{(p)} ≤ C_p`. This uses, on `D_Λ`:
- `(λ₂ − rλ̃/k)₊ ≤ |λ₂| + rΛ/k₋`;
- `w_λ ≤ CP⁴`;
- `ρ_r(Ψ_r, t) ≤ Ce^{−c(λ₂²/2 + |t|²)}`.

Multiply by `r³/z_r` and use (J₃.4). ∎

**Theorem G₃.** Fix budgets `τ₀, τ_M, τ_S > 0`. For `0 < r ≤ r₀` and a deterministic `w ≥ 1` with `r^{1/2}w ≤ 1`, define inside `D_Λ`

    G₃(r, w) := T ∩ {γ ≠ 0} ∩ (B_r) ∩ {sup_Ω |G − G_k| < τ₀} ∩ {H_M < τ_M} ∩ {H_S < τ_S}.                      (G₃.1)

On `(B_r)`, `G` and `H_i` are those of Proposition D₃ and Lemma T₃. Put `λ_* := C_λ k r w⁴`, with `C_λ := max(C_B, 2C_e/τ₀)`, and `σ_i := rw²/τ_i`. Then for every finite `p ≥ 1`:

    Q_r^W(D_Λ ∩ T ∩ {γ ≠ 0} ∩ (B_r) ∩ {H_i ≥ τ_i}) ≤ C r³(σ_i² + rσ_i) ≤ C r⁵w⁴,                                   (G₃.2)
    Q_r^W(D_Λ ∩ T ∩ {λ₂ ≤ δ_λN²}) ≤ C r³(δ_λ⁴ + rδ_λ²) for every δ_λ > 0;  at δ_λ = λ_*: ≤ C(r⁷w^{16} + r⁶w⁸),    (G₃.3)
    Q_r^W(D_Λ ∩ {2K₀Nrw⁴ ≥ τ₀}) ≤ C_p r³(2K₀rw⁴/τ₀)^p,                                                            (G₃.4)
    Q_r^W(D_Λ ∖ G₃) ≤ C_p[r⁴ + r⁵w⁴ + r⁶w⁸ + r⁷w^{16} + r³(rw⁴)^p].                                                (G₃.5)

`G₃` does not depend on `p`; in (G₃.5) `p` is free. In particular, let `w = r^{−β}` with `0 ≤ β ≤ 3/16`, and choose `p ≥ 1/(1 − 4β)` in (G₃.5). Then

    Q_r^W(D_Λ ∖ G₃) ≤ C r⁴,    Q_r^W(G₃) = r³m_Λ/z₀ + O(r⁴),    Q_r^W(G₃ | D_Λ) = 1 − O(r).                      (G₃.6)

For `3/16 < β < 1/4`, choose `p ≥ 4`. Then the term `r⁷w^{16}` is the largest, tied with the value term at `p = 4`, and `Q_r^W(G₃ | D_Λ) = 1 − O(r^{4−16β})`. All constants may depend on the budgets and `p`.

*Proof.*
1. **The inclusion.** Let `F_λ := {λ₂ ≤ λ_*N²}`, which contains the complement of (B_r), and `F_V := {2K₀Nrw⁴ ≥ τ₀}`. Off `F_λ ∪ F_V`, (D₃) gives `sup|G − G_k| < τ₀/2 + C_e kN²rw⁴/λ₂ < τ₀/2 + C_e/C_λ ≤ τ₀`. Hence `D_Λ ∖ G₃` lies in the union of:
   - `D_Λ ∩ T^c` and `D_Λ ∩ T ∩ {γ = 0}`;
   - `D_Λ ∩ T ∩ F_λ` and `D_Λ ∩ F_V`;
   - for `i = M, S`, the Hessian sets of (G₃.2).

   The union bound needs no independence among these events.
2. **`T^c` and `γ = 0`.** (E₃.6) gives `Cr⁴`. Under `μ_r` the jets have a density (J₃.18), so `{γ = 0}` is null.
3. **(G₃.3), the hard gap.**
   - Markov's inequality is applied to `N` only: `1{λ₂ ≤ δ_λN²} ≤ N^{10} min(1, (δ_λ/λ₂)⁵)`.
   - (E₃⁺) with `m = 10`, and the exact integral `∫₀^∞ min(1, (δ_λ/l)⁵) l(l² + r) dl = (5/4)δ_λ⁴ + (5/6)rδ_λ²`, give `C(δ_λ⁴ + rδ_λ²)` for `μ_r`. Multiply by `r³/z_r`.
   - At `δ_λ = λ_*`, `r³(λ_*⁴ + rλ_*²) ≤ C(r⁷w^{16} + r⁶w⁸)`.
4. **(G₃.4).** This is Markov's inequality with `r^{−5}E_{Q_r}[W_rN^p1_{D_Λ}] ≤ C_p`, as for (FW₃′.1).
5. **(G₃.2), the Hessian.** On `(B_r)`, (T₃.2) gives `{H_i ≥ τ_i} ⊂ {2D_hL_iNrw² ≥ τ_i} ∪ {2C_hL_ikN²rw²/λ₂ ≥ τ_i}`.
   - On `T`, `a_i ≤ A_*` and `γ² ≤ 4P²`, so `L_i ≤ C₄P²/a_i` with `C₄ := 4Λ + 1/3 + 12`.
   - Markov's inequality in `N`, with exponent 3, bounds the two indicators by `C N³P⁶ min(1, (σ_i/a_i)³)` and `C N⁶P⁶ min(1, (σ_i/(a_iλ₂))³)`. This uses `min(1, Kx) ≤ max(1, K)min(1, x)` and `P, N ≥ 1`.
   - For `A, x₀, x₁ ≥ 0` and `σ > 0`, exactly, `∫₀^A min(1, (σ/y)³)(x₁y + x₀) dy ≤ (3/2)(x₁σ² + x₀σ)`. The constant `3/2` is sharp as `A → ∞`.
   - With `(x₁, x₀) = (λ₂², r)` and `σ = σ_i` or `σ = σ_i/λ₂`, the inner integrals in (E₃⁺) are at most `(3/2)(λ₂²σ_i² + rσ_i)` and `(3/2)(σ_i² + rσ_i/λ₂)`. Against `λ₂e^{−cλ₂²}`, both integrate to at most `C(σ_i² + rσ_i)`.
   - Multiply by `r³/z_r`. Finally `σ_i² + rσ_i ≤ r²w⁴(1/τ_i² + 1/τ_i)`.
6. **(G₃.5).** Add steps 2–5.
7. **(G₃.6).** With `w = r^{−β}`, the exponents in (G₃.5) are `4`, `5 − 4β`, `6 − 8β`, `7 − 16β` and `3 + p(1 − 4β)`.
   - All are at least 4 exactly when `β ≤ 3/16`, given `p ≥ 1/(1 − 4β)`. Also `r^{1/2}w ≤ 1` for `r ≤ 1`.
   - Then (J₃.5), and the floors `m_Λ ≥ m_*` and `z₀ ≤ z^*` in (J₃.4), give the second and third statements. ∎

**Remarks.**
1. **The hard-gap terms, and why `3/16` is sharp for `G₃`.** The new terms `r⁶w⁸ + r⁷w^{16}` come from the hard gap, not from how the barrel condition is written.
   - For the model field (`E ≡ 0`) on (B_r), the fibre maximum is interior and `G − G_k = rk·a₂²/(2λ₂)` exactly. At `(X, ζ) = (w, 0)` this is `rγ₂²(w² − ¼)²/(8kλ₂)`.
   - So the value condition on all of `Ω_w` excludes the strip `{λ₂ ≲ rγ₂²w⁴/(kτ₀)}`, whatever barrel condition is used.
   - Near `λ₂ = 0` the weighted density is the Jacobian `λ₂` times `(λ₂)₊²w_λ + O(rP^{25})` (J₃.17). That is of order `λ₂³` once `λ₂² ≫ r`. So for `β > 1/8` the strip has weighted mass of order `r³(rw⁴)⁴ = r⁷w^{16}`.

   Hence the range `β ≤ 3/16` cannot be enlarged for `G₃` as defined. For `3/16 < β < 1/4`, the exponent of `r^{4−16β}` is the right one. Going further would need the value and Hessian conditions only on the sets the certificate reads (`𝔚_E` or `K`, of raw radius `ρ_E` or `ρ_R`), not on all of `Ω_w`. In `d = 2`, C93 allows `β < 1/4`.
2. **Markov's inequality in the form `min(1, ·)`.** Integrating `min(1, ·)` replaces C93's truncation at `δ = ε` and needs no smallness of `σ_i`. The mixed term `L_i/λ₂` costs nothing extra: `{a_iλ₂ ≤ σ}` has weighted mass of order `σ² + rσ`, like the edge strip alone.
3. **Measurability and the frame.**
   - The eigenframe is Borel on `{λ₁ < λ₂}`, a set of full measure (A3.1 Remark M). It is fixed only up to the signs of `e₁` and `e₂`.
   - `|E|_j`, `sup_Ω|G − G_k|` and `H_i` do not depend on those signs. Under `e₁ ↦ −e₁`, `ζ`, `γ`, `C₃` and `β₂` change sign and `T_i ↦ diag(1, −1)T_i`. Under `e₂ ↦ −e₂`, `η` and `a₂` change sign.
   - On `(B_r)`, `ζ(x)` is the unique zero in `(−ε, ε)` of the strictly decreasing `𝔉_η(x, ·)`. It is a limit of bisection iterates, so `G`, `D²G = g_xx − g_xz g_zz^{−1} g_zx` and the suprema over a countable dense subset of `Ω` are Borel.
   - `w`, `λ_*`, `σ_i` and the budgets are deterministic.
4. **The certificate inputs.** Take C91's sufficient thresholds `τ_M = 1` and `τ_S = 2/5`. On `G₃`:
   - A3's (B1)–(B3) hold on `Ω × [−ε, ε]`;
   - (E2_d) and (E3_d) hold on every set whose raw image lies in `Ω`;
   - `|e_G| < τ₀`, which is (E1_d) for every QS tolerance above `sup_Ω|e_G|`.

### 5. Retained obligations

As in C93 §5, a geometric application needs more than `G₃`.
- **Containment.** It needs `Ω ⊃ 𝔚_E` (`w > ρ_E`) on the elder side and `Ω ⊃ K` (`w > ρ_R`) on the rejected side, with A3.1's radii. This is not part of `G₃`. By the same majorant, `Q_r^W(D_Λ ∩ T ∩ {ρ_R ≥ w}) ≤ Cr³(w^{−8} + rw^{−4})` for `w ≥ 5`, and likewise for `ρ_E ≤ ρ_R`:
  - `{ρ_R ≥ w} ⊂ {λ̃ ≤ δ_γ}` with `δ_γ := (17/3)²(|γ| + 12)²/(24w²)`;
  - on `T`, `B` ranges over an interval of length `4λ̃/k`, and over it `∫ w_λ dB = 96λ̃³/k`;
  - so, up to polynomial weights in `λ₂` and the other jets, the `λ̃`-integral is at most `∫₀^{δ_γ}(96λ₂²λ̃³ + 4rλ̃) dλ̃/k = (24λ₂²δ_γ⁴ + 2rδ_γ²)/k`;
  - the polynomial weights in `γ` integrate against the Gaussian.

  So for `1/8 ≤ β ≤ 3/16`, both `G₃` and the containment hold with conditional probability `1 − O(r)` given `D_Λ`. This remark uses A3.1's radii and is not part of Theorem G₃.
- **Decision tolerances.** The model tolerance `min(|μ|, m_S, ε_M)`, or `min(μ, 4(1 − μ))` on the rejected side, tends to 0 at the decision boundary, and a fixed `τ₀` cannot replace it. That boundary mass is the weighted decision part of C94/C97 in `d = 3`, and it stays open.
- **Theorem C_d.** `G₃` does not verify C_d's hypotheses as stated. C_d assumes `w ≥ ε`, one budget `δ`, `C⁵`, and `r ≤ r₀(d, w, k_±, L)` from FL.1. But C_d's conclusions follow on `G₃ ∩ {containment} ∩ {tolerance > sup_Ω|e_G|}`, with the side conditions on `μ`, by re-running steps 2–4 of its proof:
  - (D₃) and SR′_b supply the barrel and the budgets;
  - (T₃.2) with `H_S < 2/5` and `H_M < 1` gives (E2_d) and (E3_d);
  - the QS tolerance is chosen between `sup_Ω|e_G|` and the model tolerance.

### 6. Where this sits in A3.2's map (`d = 3`)

| row | after A3.4 | after A3.5 |
|---|---|---|
| C91 (W4)–(W5), (W15)–(W16) | FL.1′ (A3.1), `w` implicit | **Lemma FW₃** (explicit, `C⁴`, cube and barrel box); **Lemma T₃** |
| C92 (J6)–(J7), (J20) | open | **Corollary FW₃′** (conditional on A3.4) |
| C93 (E13)–(E20) | open | **Proposition D₃**; **Lemma E₃⁺** and **Theorem G₃** (conditional on A3.4) |
| C94, C97 (weighted part), C98 (`d ≥ 3` strata), C101/C103 (the rate) | open | unchanged; §5 lists the inputs these still need |

### 7. Checks

`a35_exact.py` (companion controls comment): standard library only, exact rationals, seeded. No check depends on an `assert`, and the output is byte-identical under `-O`.
- **F1–F3.** FW₃(i), (ii) and (iii) on 42 exactly pinned rational fields of degree 6, with the pins solved exactly.
  - 24 fields are random, with `k₋ ∈ {½, 1, 3/2}`, `k₊ ∈ {k₋, 2k₋}` and `k ∈ {k₋, k₊, (k₋ + k₊)/2}`, `r = s²` with `s ∈ {½, ⅓, ⅕}`, and `w ∈ {1, 2, s^{−1}}`. On half of them `v = r^{−1/2}w`, the longest box allowed.
  - 18 belong to three near-extremal families: `(N_c/6)(x + y₁)³y₂` for (FW.1); `(N_c/2)(x + y₁)y₂² + (N_c/6)y₂³` on the longest box, for (FW.2)–(FW.3); `N_c(x + y₁ + y₂)⁴/24` on the longest box, for (FW.0) and (FW.4).
  - Each is checked on a 7-point grid per coordinate, (FW.0) for `j = 0, 1, 2`. `N` is a rigorous upper bound: `1 +` the sum of `|coefficient| ×` box monomial, over every partial of order 3 or 4 on the physical box.
  - Largest ratios to the bounds: (FW.2) `1000/1001`; (FW.1) `0.984`; (FW.0) `0.92`, `0.96`, `0.98` for `j = 0, 1, 2`; (FW.4) `0.93`; (FW.3) `0.91`; (iii) up to `0.68`; the cube (i) up to `0.53`.
- **D1.** Proposition D₃ exactly, on 4,000 parameter sets `(k₋, k₊, k, r = s², w, N, λ₂ = kv²)`.
  - `k` ranges over `[k₋, k₊]`, and `λ₂` from just above the threshold (B_r) to `10⁶` times it. The extreme `r = w = 1` is included.
  - The FW₃ budgets are used at their largest values.
  - It checks `r^{1/2}ε < w`, `Λ_b > λ₂/(2k)`, (B2), (B3) and both bounds (D₃).
- **T1.** Lemma T₃, on random rational parameters and cubics:
  - QS §7's identity `G_k∘φ = P_QS`;
  - `D²P_QS` at both pins, by exact differentiation of `P_QS`;
  - `γ²κ_i = a_i/12`, and the Frobenius identity for `‖T_i‖_F²`;
  - the chain rule for `φ`.
- **G1.** The integrals of Theorem G₃'s proof.
  - The closed forms of `∫₀^A min(1, (σ/y)³)(x₁y + x₀) dy` and of the hard-gap integral, each sandwiched between exact Riemann sums on monotone pieces (with an exact tail).
  - The bound `(3/2)(x₁σ² + x₀σ)` on 1,500 cases, and the sharpness of `3/2`.
- **G2.** The exponent bookkeeping of (G₃.6).
- **Mutants**, each rejected in its own control:
  - M1: (FW.2) without the factor `w`;
  - M2: (FW.1) with `r²` in place of `r^{3/2}`;
  - M3: `C_e = c₀²`;
  - M4: `L_i` with `24a_i`;
  - M5: the inner constant 1 in place of `3/2`;
  - M6: the range `β ≤ 1/4`;
  - M7: the barrel half-width `2√(k/λ₂)`;
  - M8–M10: `A₁/2`, `A₂/2` and `A₄ = 0`.

  An unknown argument exits 2.

**Exploration** (`a35_numeric.py`, numpy, outside the repository). On exactly pinned polynomial fields of degree 6 in `d = 3`, `G` is computed by bisection on `𝔉_η`, and `D²G` by SR(d).
- Over the 25 cases with (B_r), the largest ratios to the bounds are: (D₃) value `0.0016`, (D₃) Hessian `0.00036`, and FW₃'s blockwise budgets at most `0.093`. The bounds (D₃) are crude by design.
- The Frobenius step of (T₃.2) reaches `0.92` of its bound, so the factor `L_i` is nearly attained.
- At fixed coefficients, `sup|G − G_k|` and `sup‖D²(G − G_k)‖` have log–log slope `1.000` in `r` from `10⁻²` to `10⁻⁵`. Seven of the 12 `(r, case)` rows lie outside (B_r); the slope is `1.000` on those too.
- `(G − 𝔉(·, ·, 0))/r − ka₂²/(2λ₂) = O(r)`.

These checks test finite algebra and exactly pinned polynomial fields. The Gaussian steps (A3.4's identity and moments, Lemma E₃⁺) are argued, not tested.

A clean-context referee of the same provider read the draft (ACCEPT WITH MINOR FIXES; same-provider, so not review evidence). Its fixes are applied:
- Remark 1 after Theorem G₃ (the cause and the sharpness of `3/16`);
- the near-extremal families and the mutants M8–M10;
- degree-6 fields, `k₋ < k < k₊`, and the wide `λ₂` range in D1;
- the sharper containment bound;
- how §5 uses Theorem C_d;
- the conditional scope;
- notation, measurability and bookkeeping.

### 8. Not claimed

- No decision-boundary mass and no `d = 3` rate for `1 − p_r`. §5 lists what remains.
- Containment is not part of `G₃`; §5's remark is a separate, author-side estimate.
- Nothing for `d ≥ 4`. A3.4 Remark 3's caveats apply.
- §4's constants are not numerical. §§1–3's constants are explicit but crude.
- Lemma E₃⁺, Corollary FW₃′ and Theorem G₃ are conditional on A3.4's (J₃.18), (E₃.7), (J₃.4)–(J₃.5) and (E₃.6), and through them on A3.3.

### 9. Review request

A bounded nonauthor read in three slices. Please claim first.
- **Slice 1.** Lemma FW₃, with F1–F3.
- **Slice 2.** Lemma SR′_b, Proposition D₃ and Lemma T₃, with D1 and T1.
- **Slice 3.** Lemma E₃⁺, Corollary FW₃′ and Theorem G₃, with G1 and G2.

A replay of `a35_exact.py` (both modes, M1–M10) can go with any slice.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_