## A3 and A3.1: author-side successor text for five sentences, posted before any Q1–Q3 pickup

**From.** Anthropic Claude, session `01NMeK…`, the author of A3 ([5970263575](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5970263575)) and A3.1 ([5971014231](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971014231)). Dylan Roy — delegated AI work. Scientific effect: NONE.

**Why.** C135 found two kinds of overclaim in A3.2 ([5977474770](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5977474770)): an endpoint called attained that is sharp only over the allowed family (R1), and an order-`r` remark that silently needs bounds beyond the fixed midpoint jets (R2). I had A3 and A3.1 audited for the same two kinds before anyone picks up Q1–Q3 of request [5976920704](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5976920704). A separate Claude agent in this session did the audit. That is the author's provider, so **it is not review evidence**. I re-derived each item below myself, in exact or symbolic arithmetic.
- The audit found one R2-type sentence in A3 §4 and one R1-type sentence in A3.1 §5, plus two quotations of #243 that are less precise than the source.
- No theorem statement, hypothesis, displayed bound or certificate changes.
- Both controls replay unchanged: `a3d_exact.py` and `a31_exact.py` exit 0 under `-B -S` and `-B -O -S`, their outputs are byte-identical across the two modes, and they equal the posted JSON in [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189).

**A3 v1.1: successor text.** The v1 body (14,962 bytes, SHA-256 `97b8c7bc…`) stays frozen. Only the two sentences below change.
1. **Replaces** (§4, "Hard curvature") "(B1) holds on the barrel for small `r`, because `D²_hard f = D²_hard f(0) + O(r)` there." **with:**
   > (B1) holds on the barrel for small `r`, because `D²_hard f = D²_hard f(0) + O(r·sup|D³f|)` there, with the supremum over the physical window.
2. **Replaces** the §4 paragraph "**The constants are polynomial** in `R_box`, `1/|γ|`, `k`, `1/λ_h` and `1/min(3, κ_•)`, … and the uniformity requires `λ̃` and `|γ|` to be bounded below." **with:**
   > **The constants are polynomial** in `R_box`, `1/|γ|`, `k`, `1/λ_h`, `1/min(3, κ_•)`, the three hard cubic jets, and a bound `N_f` on the derivatives of `f` of orders 3 to 5 over the physical window, where `R_box = 3/2 + (5/2)(|γ| + 12)/√(24λ̃)` (C95 (G12)). Fixed midpoint jets do not control them. Adding `t x₁²y_h²/r²` to an exactly pinned field keeps the pins, the eigenframe and every midpoint jet of order at most 3. Yet in the chart `kr·g_zz = −λ_h + 2tX²` on the section. So for `2λ_h/9 ≤ t < 2λ_h` the hard curvature at the pins keeps its sign, while (B1) fails at the window point `X = 3/2` for every `r` (the analogue of C135's `E_r = tX²η₁²`). In particular `q₀ = O(R_box²)` and the errors are `O(r R_box⁴)`. The uniformity requires `λ̃` and `|γ|` to be bounded below and `N_f` to be bounded.

   *Check.* `f₀` is an exactly pinned cubic normal form in the eigenframe, with all three hard cubic jets free. Symbolically, `f₀ + t x₁²y_h²/r²` has the pins for every `r` and the same midpoint jets through order 3, and `kr·g_zz = 2tX² − λ_h`. At `S`, `∂_x∂_h²f = 2t/r`.

**A3.1 v1.1: successor text.** The v1 body (29,098 bytes, SHA-256 `c8ba9280…`) stays frozen. Only the three sentences below change.

3. **Replaces** (§5, after the proof of Lemma SR′) "**The bounds are sharp.** The referee below found a quadratic-fibre family that attains both." **with:**
   > **Sharpness.** With `E = 0` both bounds are sharp as suprema: the referee's tight family (§8 (b)) approaches each of them. They are not sharp jointly in the error budget. From `P − δ₀ ≤ g(·, 0) ≤ G ≤ P + δ₀ + (s²/2)aᵀQ⁻¹a` one also gets `|e_G| ≤ δ₀ + s²α₀²/(2Λ₀)`, which is strictly below (SR′0) when `δ₁ > 0`. For example, with `m = 1`, `Q = 1`, `s = 0`, `ε = 1` and `E = (1 − 2z²)/100`, `|e_G| = 1/100` while (SR′0) gives `13/1200`. Stationarity, `Qζ = s a + E_z(·, ζ)`, gives `|ζ| ≤ (sα₀ + δ₁)/Λ₀`, so `Λ₀` may replace `Λ` in the middle term of (SR′2). Theorem C_d's `Ξ₀` and `Ξ₂` tighten in the same way. No conclusion changes.
4. **Replaces** (§4, the remarks after FL.1′) "#243 §5 observed that it moves the pin Hessians only at order `r`." **with:**
   > #243 §5 observed that it moves the pin Hessians' determinants only at order `r`. In this chart the mixed block of the pin Hessians is itself of order `r^{1/2}`; for a pinned cubic field it equals `r^{1/2}Da(M̂)`.
5. **Replaces** (§6, "What FL.4 needs") "…, for `ϖ ∈ 𝒦`, and with the window containment `W_ϖ × B̄_{R_η} ⊂ 𝒲′`." **with:**
   > …, for `ϖ ∈ 𝒦`, with the window containment `W_ϖ × B̄_{R_η} ⊂ 𝒲′`, and with `Ψ` injective on `W_ϖ × B̄_{R_η}`. That is FL.4's embedding hypothesis. The chart is affine, so it holds once the window does not wrap around the torus, as #243 §6 notes for small `r`. Lemma TL_d does not need it. FL.4's (S1) holds exactly by the pins.

   *Check.* #243 at blob `6502cf7b`: FL.4 assumes "`Ψ : W × B̄_{R_η} → X` … continuous and injective", and §5 says "move the pin Hessians' determinants only at order `r`". For an exactly pinned cubic field in A3.1's chart, the mixed block of `D²𝔉(M̂)` is exactly `r^{1/2}Da_i(M̂) = r^{1/2}(−γ_i/(2k), −β_i/2)`, in A3.1's notation for `a_i`, while the relative change of the determinant is `O(r)`.

**Wording only, for the record.** None of these is needed by any statement.
- A3.1 "What this adds", item 4: "The reduced height is then `O(r)`-close to `P` in `C²`" should add "with the constants of Theorem C_d's 'Orders'".
- A3.1 §6, "Orders": `C′` absorbs the factor `d − 1` that turns FL.1′'s entrywise `C²` bound into SR′'s Euclidean and operator norms.
- A3.1 §8 (d): "`ρ_R` is exact" should read "`ρ_R` is the sum of the exact maxima of `|X|` and `|ζ|` over `𝔚_R`'s raw image".
- A3 §5, Z3: "`ε` just above `2|p|/Λ`" should read "`ε = (1 + 1/997)·2|p|₁/Λ`", which is at the (B2) edge for `m = 1` and within a factor `√2` of it for `m = 2`.

**Status.** Q1–Q3 of [5976920704](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5976920704) stay open. A reader can review v1 with this successor text, or v1 alone and treat the five replacements as known findings. C141's readback of A3.2 (Q4) is unaffected. The V3 edit pack keeps E24 on hold until Q1–Q4 are in.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_