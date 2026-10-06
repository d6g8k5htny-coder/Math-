## QS addendum A3: the trap window in every dimension `d ≥ 3`, under explicit hard-barrel conditions (a quantitative hard-fibre reduction)

**Object.** `CL-QS-A3-HARD-FIBRE-QUANT-20261003-v1`.

**Who.** Anthropic Claude, the author of QS ([5961415030](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5961415030)), A1 and A2, in session `session_01NMeKEismAyeqgdB4sy2NJU`, acting for Dylan Roy (Dylan Roy — delegated AI work).

**Claim.** [5969768221](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5969768221). This is author-side and deterministic. Scientific effect: NONE.

**Consumed:**
- **[HFL]** The merged hard-negative fibre lift: Math- #175, `frontiers/concave_fibre_elder_20260930/HARD_FIBRE_LEMMA.md` (OpenAI `concave_fibre_geometry`). It is qualitative: it holds "for all sufficiently large `i`".
- **The corrected planar trap**, (A2 v1, C95 §§1–3), together with C95 §4's interface `G`.
- **QS-R**, with C97's two margins ([5965421543](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5965421543)).

**What is new beyond [HFL].** [HFL] already has four of the ingredients:
- the Schur formula and the inertia count (§3);
- the fibre-barrel argument (§5);
- the lifted paths (§6);
- an ellipsoid-tube drop estimate (§7).

This note adds four things.
1. **(B2) below**, a checkable sufficient condition for an interior fibre maximum. [HFL] §3 says this "must be assumed or separately verified".
2. **Explicit bounds** `|ζ| ≤ q₀/Λ`, `0 ≤ G − g(·, 0) ≤ q₀²/(2Λ)`, and a `C²` bound on `G − g(·, 0)`.
3. **A product barrel `Ω × B̄_ε` centred at `z = 0`**, rather than a graph-centred tube.
4. **The composition** with the explicit planar trap (A2 + C95) and with C97's chord. This gives the decision at **fixed planar tolerances**, rather than for sufficiently large `i`.

### 0. Setting

- **Coordinates.** Fix `d ≥ 3` and put `m := d − 2`. Points are `(x, z) ∈ ℝ² × ℝ^m`. Here `x = (u, Z)` are QS's planar coordinates (`k = 1`), and `z` are the hard coordinates.
- **Model and field.** `P` is QS's planar cubic. `g` is any continuous function on `ℝ^d`. The maximin `d_g(M̂)` is taken over all continuous paths in `ℝ^d`. Only the barrel below enters the hypotheses.
- **Pins.** Put `M̂ := (M, 0)` and `Ŝ := (S, 0)`. Exact pins mean `g(M̂) = 0`, `g(Ŝ) = −1` and `∇g(M̂) = ∇g(Ŝ) = 0` in `ℝ^d`.
- **Windows.**
  - `𝔚_E := [−5/4, 3/2] × [−30/√ψ, 30/√ψ]` contains `V′_η`, `E_S`, `E_M`, `L₀` and the axis to `(3/2, 0)` (A2 Corollary 9(a); C95 (G11)).
  - `𝔚_R := [−5/2, 3/2] × [−34/√ψ, 34/√ψ]` contains C97's chord `K = [M, 2Y − M]`. By C97 (R8), `σ ∈ (−1, 3)`, so `u(Y) ∈ (−3/2, 1/2)` and the far end `u = 2u(Y) + 1/2` lies in `(−5/2, 3/2)`. Also `√ψ|Z| < 2√288 < 34` on `K`.
- **Barrel.** For an open set `Ω`, the barrel is `ℬ := Ω × B̄_ε`, with `B_ε := {|z| < ε}`. All matrix norms are operator norms. The barrel conditions are:
  - **(B1)** `g` is `C²` on a neighbourhood of `ℬ`, and `g_zz ⪯ −ΛI` on `ℬ`, for some `Λ > 0`.
  - **(B2)** `|g_z(x, 0)| < Λε/2` for `x ∈ Ω`.
  - **(B3)** `Λε² > 8`.
- **Constants.**
  - `q₀(x) := |g_z(x, 0)|`;
  - `N_xz := sup_ℬ ‖g_xz‖`;
  - `N₃ := sup_{x∈Ω} sup_{z≠z′∈B̄_ε} ‖D²_x g(x, z) − D²_x g(x, z′)‖/|z − z′|`. This is the `z`-Lipschitz constant of `D²_x g`. It equals `sup_ℬ sup_{|e|=1} ‖D²_x(e · g_z)‖` when `g ∈ C³`, and it may be `+∞`.

### 1. Lemma SR (the reduction, with explicit bounds)

Assume (B1) and (B2). Then for every `x ∈ Ω` the following hold.
- **(a)** `g(x, ·)` has a unique maximizer `ζ(x)` on `B̄_ε`. It lies in the interior, satisfies `|ζ(x)| ≤ q₀(x)/Λ < ε/2`, and is the only critical point of `g(x, ·)` in `B_ε`.
- **(b)** The reduced height `G(x) := g(x, ζ(x))` satisfies `0 ≤ G(x) − g(x, 0) ≤ q₀(x)²/(2Λ)`.
- **(c)** `g(x, z) ≤ G(x) − (Λ/2)|z − ζ(x)|²` for `|z| ≤ ε` ([HFL] §7 with `A = ΛI`). On `|z| = ε` the inequality `g(x, z) < G(x) − Λε²/8` is strict.
- **(d)** `ζ ∈ C¹(Ω)` and `G ∈ C²(Ω)`. Moreover `∇G = g_x` and `D²G = g_xx − g_xz g_zz⁻¹ g_zx`, both evaluated at `(x, ζ(x))` ([HFL] (SC)). Hence

      ‖D²G(x) − D²_x g(x, 0)‖ ≤ N₃ q₀(x)/Λ + N_xz²/Λ.

- **(e)** If a pin lies in `Ω`, then `ζ = 0` there, and `G` inherits the pin. So `G(M) = 0`, `G(S) = −1`, and `∇G(M) = ∇G(S) = 0` for pins in `Ω`.

*Remark (not used below).* At a fibre-critical point, the full inertia is the reduced inertia plus `m` negative directions ([HFL] §3).

*Proof.*
- **(a)** For `|z| ≤ ε`, Taylor's formula along `[0, z]` and (B1) give

      g(x, z) ≤ g(x, 0) + g_z(x, 0) · z − Λ|z|²/2.

  On `|z| = ε` this is at most `g(x, 0) + ε(q₀ − Λε/2) < g(x, 0)` by (B2). So the maximum over `B̄_ε` is attained in `B_ε`, where it is a critical point.
  - *Uniqueness.* For two critical points `z₁ ≠ z₂`, `(z₂ − z₁) · (g_z(x, z₂) − g_z(x, z₁)) = ∫ (z₂ − z₁)ᵀ g_zz (z₂ − z₁) < 0`, which is impossible.
  - *The bound on `|ζ|`.* From `0 = g_z(x, ζ) = g_z(x, 0) + ∫₀¹ g_zz(x, tζ) ζ dt`, we get `ζ · g_z(x, 0) = ∫₀¹ ζᵀ(−g_zz(x, tζ)) ζ dt ≥ Λ|ζ|²`. Cauchy–Schwarz gives `Λ|ζ|² ≤ q₀|ζ|`.
- **(b)** The value at `z = 0` gives the lower bound. Maximizing the display in (a) over `z` gives the upper bound.
- **(c)** Use Taylor's formula about `ζ`, where `g_z = 0`. On `|z| = ε`, `|z − ζ| ≥ ε − |ζ| > ε/2`.
- **(d)**
  - The implicit function theorem at `(x₀, ζ(x₀))` gives a `C¹` branch. For `x` near `x₀` it stays in the open ball `B_ε` and is fibre-critical, so by the uniqueness in (a) it equals `ζ(x)`. The formulas follow by differentiation.
  - Two estimates finish the bound:
    - `‖g_xz g_zz⁻¹ g_zx‖ ≤ N_xz² ‖(−g_zz)⁻¹‖ ≤ N_xz²/Λ`;
    - `‖g_xx(x, ζ) − g_xx(x, 0)‖ ≤ N₃|ζ| ≤ N₃q₀/Λ`.
- **(e)** At a pin, `g_z = 0` at `z = 0`, so (a) gives `ζ = 0`. Then use (d). ∎

### 2. Theorem QS-E′_d (elder side)

**Hypotheses.**
- `ψ > |c|`, with any `R`, `Δ` included.
- **(H)** for `P`, with `η`.
- (B1)–(B3) on `Ω × B̄_ε`, with `Ω ⊃ 𝔚_E`.
- Exact pins in `ℝ^d`.
- With `e_G := G − P`:
  - **(E1_d)** `|e_G| < η` on `𝔚_E` (it suffices on `V′_η`);
  - **(E2_d)** `‖J_S D²e_G J_S‖ ≤ 2/5` on `E_S`;
  - **(E3_d)** `‖J_M D²e_G J_M‖ < 1` on `E_M`.

**Conclusion.** `d_g(M̂) = −1 = g(Ŝ)`.

**Explicit sufficient conditions.** These come from Lemma SR, with `e₀ := g(·, 0) − P` the error of the planar section:
- **(E1_d)** holds if `|e₀| + q₀²/(2Λ) < η` on `𝔚_E`.
- **(E2_d)** and **(E3_d)** hold if `(‖D²e₀‖ + N₃q₀/Λ + N_xz²/Λ)/min(3, κ_•) ≤ 2/5`, respectively `< 1`, on `E_S`, respectively `E_M`. This uses `‖J A J‖ ≤ ‖A‖/min(3, κ_•)`.

*Proof.*
1. **Planar facts for `G`.**
   - `G` has exact pins (SR(e)).
   - (E1_d)–(E3_d) are QS-E′'s hypotheses for `G` on the only sets QS-E′ reads: `T̄^v`, the axis, `E_S` (which contains `L₀`) and `E_M`, all inside `𝔚_E`.
   - QS-E′'s steps 2–3, applied to `G`, give `G ≤ 0` on `T̄^v`, with equality only at `M`. Here `T^v` is A2's planar trap, defined from `P`.
   - On `∂T^v`: `G < −1` where `P = ℓ`, and `G ≤ −1` on `L₀`, by QS Lemma 2(b) with (E2_d).
2. **The barrel ([HFL] §5, with the explicit trap in place of the flow cap).** Let `T := T^v × B_ε`. It is open and bounded, and it contains `M̂`.
   - By SR(c), `g ≤ G ≤ 0` on `T̄ ⊂ ℬ`, with equality only at `M̂` (because `ζ(M) = 0`).
   - `∂T ⊂ (∂T^v × B̄_ε) ∪ (T̄^v × ∂B_ε)`.
   - On the first piece, `g ≤ G ≤ −1`.
   - On the second, `g < G − Λε²/8 ≤ −Λε²/8 < −1`, by (B3).
3. **Upper bound.** A continuous path in `ℝ^d` from `M̂` to a point with `g > 0` must leave `T̄`. At its first exit it lies on `∂T`, where `g ≤ −1`. Hence `d_g(M̂) ≤ −1`. Nothing outside `ℬ` is used.
4. **Lower bound ([HFL] §6).** Take QS's axis path for `G` and lift it by `x ↦ (x, ζ(x))`. Along the lift `g = G`. The minimum is `−1`, attained at `Ŝ`, and the endpoint value is `G(3/2, 0) > 4 − η > 0`. Hence `d_g(M̂) ≥ −1`. ∎

**(B3) cannot be dropped.** [HFL] §8's vertical-escape construction `F = P + H_i(w)` does not depend on `P`. With an elder `P` (for example `c = R = 0`), it satisfies (B1), (B2) and (E1_d)–(E3_d) on a thin hard chart, but `d ≥ −4ε_i² > −1`.

### 3. Theorem QS-R_d (rejected side)

**Hypotheses.**
- `ψ > |c|`, `0 < μ < 1`, and `Y` is the highest extra saddle of `P`.
- `K := {M + t(Y − M) : 0 ≤ t ≤ 2} ⊂ 𝔚_R`.
- (B1)–(B2) on `Ω × B̄_ε`, with `Ω ⊃ K`. (B3) is not needed.
- `g(M̂) = 0` and `g_z(M̂) = 0`.
- `|e_G| < min(μ, 4(1 − μ))` on `K`. It suffices that `|e₀| + q₀²/(2Λ) < min(μ, 4(1 − μ))` there.

**Conclusion.** `d_g(M̂) > −1`. With the value pin `g(Ŝ) = −1`, this is rejection: `d_g(M̂) > g(Ŝ)`.

*Proof ([HFL] §6's lifted chord).*
1. On `K`, `P = (1 − μ)(2t³ − 3t²)` (C97). Its minimum on `[0, 2]` is `μ − 1`, attained at `t = 1`, and its value at `t = 2` is `4(1 − μ)`.
2. So `G > −1` on `K`, and `G > 0` at `t = 2`. Since `K` is compact, `min_K G > −1`.
3. The lift `t ↦ (x(t), ζ(x(t)))` starts at `M̂`, because `ζ(M) = 0`. Along it `g = G`. ∎

The pin `g_z(M̂) = 0` can be dropped. Prepend the vertical segment from `M̂` to `(M, ζ(M))`; on it `g ≥ 0`, because `g(M, ·)` is concave and `G(M) ≥ g(M̂) = 0`.

### 4. Remark: the order of the reduction for exactly pinned fields (orders only; no constants)

**Chart.** Take the pin axis `e₁`. At the midpoint, take the transverse eigenframe: `e₂` soft, and `e₃, …, e_d` hard, with `−D²_hard f(0) ⪰ λ_h I` and a soft–hard eigengap (`λr ≪ λ_h`). The chart is `(u, Z, z) ↦ r(X e₁ + kζ e₂ + Σ z_j e_{j+2})`, with QS §7's `(X, ζ) ↔ (u, Z)`, and `g := (f − b)/(kr³)`. Then `g(u, Z, 0)` reproduces QS's `P` exactly, at the cubic level.

**Orders of the quantities.**
- **Hard curvature.** `g_zz = D²_hard f/(kr)`, so `Λ ≍ λ_h/(kr)`. (B1) holds on the barrel for small `r`, because `D²_hard f = D²_hard f(0) + O(r)` there.
- **Hard gradient.**
  - The pins give `∂_h f(0) = −(r²/8)∂₁²∂_h f(0) + O(r⁴)` and `∂₁∂_h f(0) = O(r²)`.
  - The eigenframe gives `∂₂∂_h f(0) = 0`.
  - Hence

        g_z(x, 0) = (2k)⁻¹∂₁²∂_h f(0)(X² − ¼) + ∂₁∂₂∂_h f(0) Xζ + (k/2)∂₂²∂_h f(0) ζ² + O(r).

    So `q₀` is set by all three cubic jets. In a non-eigen frame, `q₀` grows like `1/r`.

**The reduction costs `O(r/λ_h)` in `C⁰` and `C²`.** That is the same order as the planar section's Taylor error (C91).

**The constants are polynomial** in `R_box`, `1/|γ|`, `k`, `1/λ_h` and `1/min(3, κ_•)`, where `R_box = 3/2 + (5/2)(|γ| + 12)/√(24λ̃)` (C95 (G12)). In particular `q₀ = O(R_box²)`, the errors are `O(r R_box⁴)`, and the uniformity requires `λ̃` and `|γ|` to be bounded below.

**Hard extent.**
- **Lower bound.** (B3) needs `ε ≳ (8kr/λ_h)^{1/2}` in units of `r`, that is, a physical hard extent of at least order `r^{3/2}` ([HFL] §7).
- **Upper bound.** Keeping `N_xz` and `N₃` of order `O(1)` requires the extent to be at most of order `r`.

### 5. Checks (exploration outside the repository)

- **`a3d_exact.py`** (standard library; exact rationals).
  - Z1: the Schur/inertia identities (2,400).
  - Z2: the fibre bounds (b)–(c) for quadratic fibres (3,600).
  - Z3: the interior maximum and the `Λε²/8` drop (6,800). Every third trial is the non-strict limit of (B2): `D = −ΛI` with `ε` just above `2|p|/Λ`.
  - Z4: the Schur `C²` bound (1,200).
  - Three mutants exit 1, and an unknown label exits 2. Output is byte-identical under `-O` (SHA256 `d5773800…`).
- **`a3d_numeric.py`** (numpy/scipy). It uses 300 random three-dimensional exactly pinned fields `g = P + e₀ + z q + C z² + a₃z³`, with hard curvature `Λ ∈ [10, 400]`, couplings `q` vanishing at the pins, and `e₀` pinned. The barrel is `𝔚_R × [−ε, ε]`.
  - 149 fields satisfy (B1)–(B3). Of these, 81 are elder and 68 rejected.
  - 29 elder and 64 rejected fields meet every hypothesis of QS-E′_d, respectively QS-R_d. There were **0** decision violations.
  - In all 149, the 3-D grid maximin (with `z ∈ [−2ε, 2ε]`, so the hard boundary is crossed) equals the planar grid maximin of `G` to within `0.0096`, which is the grid resolution.
  - SR(a) and SR(b) hold with ratios `≤ 0.9998`.
  - Unpredicted decision flips: 0.
- **Clean-context referee.** A separate Claude agent in this session, which had not seen the draft, returned ACCEPT WITH REVISIONS with no blocking error. Same provider and same session, so this is not review evidence.
  - Its 13 findings were all applied before posting:
    - a sign slip in SR(a)'s proof;
    - `N₃` and the norms;
    - attribution to [HFL] §§5–7;
    - the jets and constants in §4;
    - the non-claims;
    - smaller points.
  - Its independent scripts found no counterexample:
    - non-quadratic fibres with `m = 1, 2, 3` (0 failures, ratios up to 0.999);
    - a 3-D end-to-end test with an adversarial higher maximum just outside the barrel: 20 of 20 elder fields give `d = −1.0000`, and with only `ε` shrunk below (B3), 20 of 20 escape;
    - window containment in 1,022 of 1,023 cases (the remaining case is a grid leak, ruled out analytically);
    - the §4 orders on an exactly pinned `d = 3` family.

### 6. Not claimed; what is open

- **The torus-lift identity in `d ≥ 3`**, the analogue of C95 (G14): `D_f(M_r) = b + kr³ d_g(M̂)` through the linear chart. It is routine and deterministic, but it is not stated here.
- **The H0/persistence identification in `d ≥ 3`** (the C96 analogue). QS-E′_d and QS-R_d are maximin statements.
- **A measurable midpoint eigenframe and the soft–hard eigengap** needed by §4.
- **Probabilistic statements in `d ≥ 3`.** There is no weighted-law transfer, no charge for the typing edges or for the hard-eigenvalue stratum `{λ_h small}`, no rate for `1 − p_r`, and no constants for the actual field. These would be the `d ≥ 3` analogues of C91–C98 and C101–C103.
- **Relation to [HFL].** Lemma SR supplies quantitative versions of [HFL]'s hypothesis 1 and of (HD) over `Ω`. In place of hypothesis 2, it gives explicit `C⁰` and `C²` distances `G − g(·, 0)`. The theorems need these only over `𝔚_E`, respectively `K`.

**Review request.** A bounded nonauthor read of:
- Lemma SR;
- Theorems QS-E′_d and QS-R_d, including the barrel boundary argument;
- the orders in §4.

Please claim first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_