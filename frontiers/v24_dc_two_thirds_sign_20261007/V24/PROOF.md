# Lifetime note V24: the `ℓ^{2/3}` coefficients `c₃` and `R_{2/3}` of the torus field at `L ≥ 10`, with explicit transfer bounds

Object: `CL-V24-TWO-THIRDS-TRANSFER-20261007-v1`. Claim: main#229 6031577374; its scope `L ≥ 24` is widened here to `L ≥ 10`.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 7 October 2026, for Dylan Roy (delegated AI
work). The same session wrote #242, #244 and notes C3, SL and C7. The consumed packets in turn consume OpenAI-authored
sources, among them [P] and [R]. The density-sandwich method of §2 is that of OpenAI's
`frontiers/cusp_torus_transfer_20261001` and of #219's Lemma S.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph, STATUS,
PROOF_INDEX, prize or Boolean change. Same GitHub account as every lane; organizational independence 0. The numbers proved
here are explicit inequalities: Theorem V's table, Lemma K's constant and Lemma J's interval. The controls check each in
exact rational arithmetic (§7). No model value is certified: `J`, `Ĩ`, `D` and `J/30 − Ĩ` are known only numerically. The
`R_{2/3}` half rests on #244's Theorem A, which is conditional (*Not claimed*). Before posting, three clean-context Claude
subagents of this session refereed the draft in the three slices of §8, against the consumed sources. All three returned
AMEND. The one blocking finding (Slice B) was about scope: Lemma K reaches #242's `I` only through #244's Theorem A, which is
conditional, and the draft did not say so. The condition is now stated wherever it applies. Every finding is applied, and
the controls comment lists them. These are author-side reads and earn no review credit.

**What is new.**
- **Theorem V (the transfer)** (§5). Take `d ∈ {2, 3}`, a real `L ≥ 10` and the [P] torus field. Then note C3's coefficient
  `c₃(L)` and note SL's `R_{2/3}(L)` differ from their model values `c₃^∞ = (J/30)𝒮_d` and `R^∞ = Ĩ𝒮_d` by at most the
  following multiples of `𝒮_d := ∫_{S^{d−1}}∫_RF₀ db dσ`, with the model's `F₀` (#242's Corollary 1′):

  | `d` | `c₃`, `L ≥ 10` | `R_{2/3}`, `L ≥ 10` | `c₃`, `L ≥ 24` | `R_{2/3}`, `L ≥ 24` |
  |---|---|---|---|---|
  | 2 | `5.88·10⁻⁹` | `7.81·10⁻⁶` | `4.88·10⁻¹¹⁰` | `6.48·10⁻¹⁰⁷` |
  | 3 | `1.97·10⁻⁷` | `4.97·10⁻⁴` | `1.64·10⁻¹⁰⁸` | `4.13·10⁻¹⁰⁵` |

  This quantifies note C3's Proposition G″. For the integrated coefficient, it also supplies the transfer that note SL's
  *Not claimed* leaves open ("the transfer of `F` (or `H`) to the torus field is not proved here"): `R_{2/3}(L) = Ĩ𝒮_d` up
  to `η_R𝒮_d`, at #244 Theorem A's conditional scope. The model value `Ĩ` itself stays uncertified.
- **Corollary V1** (§5). `c₃(L) > 0` for every real `L ≥ 10`, in `d = 2` and `d = 3`. So one may take `L₀(d) = 10` in note
  C3's Proposition G″, and for SIDE24 (`d = 3`, `L = 24`) the remainder `O(ℓ^{2/3})` of note LU's Theorem P⁺ is of exact order `ℓ^{2/3}`. Note C3's
  Remark 5 left this open.
- **Corollary V2** (§5). For `L ≥ 24`, note C7's `ℓ^{2/3}` coefficient satisfies
  `|c₃(L) − R_{2/3}(L) − (J/30 − Ĩ)𝒮_d| ≤ 4.2·10⁻¹⁰⁵𝒮_d` (`d = 3`; `6.5·10⁻¹⁰⁷𝒮_d` in `d = 2`), at #244 Theorem A's
  conditional scope. Its sign at SIDE24 is therefore that of the model number `J/30 − Ĩ` whenever
  `|J/30 − Ĩ| > 4.2·10⁻¹⁰⁵`, in particular whenever `D ≤ 0.61` (below). Write `Ĩ = Ĩ_quad + D`, with the closed form
  `Ĩ_quad = −(112/675)Γ(1/6)12^{−1/6} ≈ −0.6104057` and `D` a Gaussian integral of `I − I_quad` ((5.3)). With `J ≥ 1/2000`
  (Lemma J), the coefficient is positive as soon as `D ≤ 0.61`. Numerically `D ≈ 0.0767`, but `D` is not certified here.
- **The route.** Each coefficient has the form `𝒦^ψ` of (0.3), for a weight `ψ`. Split `ψ` into a polynomial part, whose
  `k`-integral is a finite sum of Gamma functions (Lemma 4), and nonnegative parts. Each nonnegative part is homogeneous of
  degree `−5/6` under scaling of the jet covariance, so a Gaussian density sandwich transfers it (Lemma 3). The polynomial
  parts transfer by explicit bounds on conditional Gaussian moments. The model's polynomial part of `c₃` vanishes exactly
  (note C3's (G.3)). For `R_{2/3}`, Lemma K bounds `|Φ − I_quad|` by `324(t² + |t|³ + |χ₀| + χ₀²)`, where `Φ` is #244's closed
  form of `I`. That makes the nonnegative parts of `R_{2/3}` finite, with an explicit bound.

**Not claimed.**
- No certified value of `J`, `Ĩ`, `D` or `J/30 − Ĩ`; only `J ∈ [1/2000, 10]` (Lemma J). So the sign of note C7's coefficient
  at `L = 24` is not proved here; Corollary V2 reduces it to the single model number `D`.
- The `R_{2/3}` half rests on #244's Theorem A. That half comprises the identity `I = Φ` (Lemma 0 for `R_{2/3}`), Lemma K as
  applied to `I`, the `R_{2/3}` columns of Theorem V, `D` and Corollary V2. Theorem A is conditional on merged author-side
  candidates, at their stated conditional scope: #170 Theorem E(1), [CUB] Theorem C, and [CUB]'s height identities
  (C8)–(C11), with its `B = 0` paragraph (#244's disposition). The `c₃` half and Corollary V1 do not use #244.
- Nothing for `d ≥ 4`: the floor of Lemma 1 and the image bound of Lemma 2 are checked for `d = 2, 3` only. Nothing for
  `L < 10`.
- No rate: Theorems C3, SL and C7 keep their `o(ℓ^{2/3})`, and nothing here touches them.
- Nothing new about the coefficients `c`, `c₁` and `c₂` at `L = 24`; Remark 2 cites the packets that transfer them.
- Nothing beyond the scope of the consumed sources. In particular, Corollary V2 is about the coefficient that note C7
  identifies, at that note's scope.

**Consumed.**
- Note C3 (main#229 6027862273; Slices A, B and C PASS): §0 ((0.1)–(0.3) and (C3)); Lemma 0 and its proof (the formula
  (1.1), and evenness); §3's identity `a₁ = (1/10)∫F₀db` and its domination; Theorem C3, for Corollary V1; and
  Proposition G ((G.1)–(G.3), with `J`).
- Note SL (main#229 6028358916; Slices A and B PASS): (0.1), (SL), Lemma SL₀'s bound (1.1), and Remark 2 (the model value
  `R^∞ = Ĩ𝒮_d`).
- #242 `frontiers/soft_rejected_pairs_20261002/PROOF.md` (blob `271412db`): §0 (with the Gaussian kernel's odd and even
  jets (0.3)); (2.5), the definition of `I`; Theorem 1 ((1.0a), (1.0), and `𝔇 > 0`, so `𝒮_d > 0`); (1.1a)–(1.1b) and the
  uniform bound of its proof of Corollary 1′ (through note C3 §3); (3.1); Lemma 3's bound `I ≤ (8000/3)max(1, |t|³, χ₀²)`;
  Proposition 4(1) (`F = F₀H`); Corollary 1′ (the values of `𝒮_d`); and (4.2).
- #244 `frontiers/soft_closed_form_20261002/PROOF.md` (blob `c69f92b1`): Theorem A ((2.5)), Remarks 1–4, Lemma B.2(a)
  and (c), and Corollary A.1 (`ψ_e` on `χ₀ = 0`). Theorem A is conditional on #170 Theorem E(1), [CUB] Theorem C and
  [CUB]'s (C8)–(C11), with its `B = 0` paragraph (#244's disposition); see *Not claimed*.
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md` (blob `a97bf528`): Lemma R ((R.1)–(R.2)) and Step U4, through
  note C3's Lemma 0 and §3.
- [P] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`), §1: the normalized kernel
  `K_L`.
- [R] `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`): (R5), the bound `π₀ ≤ Ce^{−cb²}`.

**Cited only.**
- Note C7 (main#229 6030039377; read in every slice): Theorem C7, for Corollary V2. Note LU (main#229 6025486512, successor
  6026230530): Theorem P⁺, for Corollary V1.
- OpenAI's `frontiers/cusp_torus_transfer_20261001/PROOF.md` (blob `de3d85fd`): (T12)–(T15), the image bound and the
  sandwich, here at derivative order 6 and for a larger jet vector. #219's Lemma S.
- #216 and #223 (the model values `c_{2,∞}` and `c_{3,∞}`), note C3 §5 (`J`'s value) and #244 §5 (`Ĩ`'s value), for
  Remark 1.
- [SIDE24] `coefficients/side24_v1/PROOF.md` (blob `44b66f04`) and `frontiers/c2_torus_transfer_20261001/NOTE.md` (blob
  `5ce5bad2`), for Remark 2.
- The Monte Carlo comment main#229 6033651797, for Remark 3.

**Prior work and overlap.** Before drafting I searched main#229 (every comment since 6 October), the Math- tree at `0793dc26`
and the project archive.
- Note C3's Proposition G″ gives `c₃(L) → c₃^∞` with an unquantified `L₀(d)`. Its Remark 5 says that a modulus of continuity
  "would show that the digits of §5 are unchanged at `L = 24`". Note SL's *Not claimed* says that the transfer of `F` (or
  `H`) to the torus field "is not proved here", and its Remark 2 says the same of the values of `R_{2/3}`.
- OpenAI's `cusp_torus_transfer` proves the density sandwich for one nonnegative, homogeneous integrand (the `c₁` integral)
  and bounds `c₁[K_L]/c₁[φ] − 1`. `c2_torus_transfer` transfers `c₂` by ball arithmetic.
- Neither applies to `c₃` or `R_{2/3}` directly: their integrands change sign, and the positive and negative pieces diverge
  separately at `k → 0`. Lemma 4's exact Gamma-function treatment of the polynomial parts is what makes the sandwich
  usable here. No packet, note or claim quantifies C3's `L₀(d)` or transfers `R_{2/3}`. This note's claim is 6031577374.

## 0. Setting and statements

Fix `d ∈ {2, 3}` and `m = d − 1`. The torus field is [P]'s: centred, stationary, with covariance
`K_L(z) = Σ_{n∈Z^d}φ(z + Ln)/Σ_{n∈Z^d}φ(Ln)` on `R^d/(LZ^d)`, `φ(z) = e^{−|z|²/2}`. The *model* is the field on `R^d` with
covariance `φ` (#242 §0, "the Gaussian kernel"; note C3's Proposition G). Notation is note C3's §0 and note SL's §0.

*The jet vector.* For a unit vector `u` and an orthonormal basis `Θ = (θ₁, …, θ_m)` of `u^⊥`, the jets at `0` are
directional derivatives along `u` and the `θ_i`:
- the odd pins `P_o := (∂_uf, ∂_{θ₁}f, …, ∂_{θ_m}f, ∂_u³f)` and the even pins `P_e := (∂_u²f, ∂_u∂_{θ₁}f, …, ∂_u∂_{θ_m}f)`;
  together they are note C3's `V₀ = (∇f(0), ∂_u∇f(0), ∂_u³f(0))`, with `q := 2d + 1` coordinates and the target `v(k)`:
  `P_o = (0, …, 0, 12k)`, `P_e = 0`;
- the even free jets `A := (∂_{θ_i}∂_{θ_j}f)_{i≤j}`;
- the odd free jets `O := (γ, B, C)`, with `γ_i := ∂_u²∂_{θ_i}f`, `B_ij := ∂_u∂_{θ_i}∂_{θ_j}f` (`i ≤ j`) and
  `C_ijl := ∂_{θ_i}∂_{θ_j}∂_{θ_l}f` (`i ≤ j ≤ l`).

Put `X := (P_o, P_e, A, O) ∈ R^N`, with `N = 9` (`d = 2`) or `N = 19` (`d = 3`). For a unit `e ⊥ u`, the projections
`x_e := (g_e, β_e, c_e) := (∂_u²∂_ef, ∂_u∂_e²f, ∂_e³f)` are linear in `O`. They are note C3's `γ_e` and `B_ee`, and #242's
`γ_e`, `B_e` and `C_e`. Let `Σ_{L,u} := Cov(X)` for the torus field and `Σ_∞ := Cov(X)` for the model. Both are
*parity-split*: even and odd jets are uncorrelated. The model is isotropic, so `Σ_∞` depends on neither `u` nor `Θ`. Every
entry is `Cov(∂^αf(0), ∂^βf(0)) = (−1)^{|β|}D^{|α|+|β|}K(0)[…]`, a derivative of the covariance at `0` of order at most `6`
along unit vectors.

*The edge* (note C3 (0.1)–(0.2)). For `a ∈ Sym(m)` with a simple top eigenvalue, `λ_m(a)` is that eigenvalue, `e(a)` a unit
eigenvector (up to sign), and `P(a)` the product of the other eigenvalues (`P := 1` if `m = 1`).

*The functional.* Let `Σ` be a nondegenerate parity-split covariance of `X`, with Gaussian density `p_Σ`. Let `ψ_k(x)` be a
weight, measurable in `(k, x) ∈ [0, ∞) × R³`. Put

    Ψ_Σ^ψ(k) := lim_{ε↓0} ε^{−1} ∫∫ ψ_k(x_{e(a)}) P(a)² 1{−ε < λ_m(a) < 0} p_Σ(v(k), a, o) da do,                    (0.1)

when the limit exists. Here the pins are fixed at `v(k)` and the integral runs over the free coordinates `(a, o)`. Put

    𝒦^ψ(L) := (1/3) ∫_{S^{d−1}} ∫_0^∞ k^{−8/3} (Ψ_{Σ_{L,u}}^ψ(k) − Ψ_{Σ_{L,u}}^ψ(0)) dk dσ(u),                        (0.2)

and `𝒦^ψ(∞)` with `Σ_∞` in place of `Σ_{L,u}`. Replacing `e` by `−e` maps `x_e = (g_e, β_e, c_e)` to `ιx_e`, with
`ι := diag(−1, 1, −1)`. Every weight below is `ι`-invariant, `ψ_k(ιx) = ψ_k(x)`, so the sign of `e(a)` does not matter. The
two weights of interest are

    ψ^c_k(x) := (4/3)|3kβ − g²/4|³,        ψ^R_k(x) := (1/32) g⁶ I(12kβ/g², 576k²c/g³)   (ψ^R := 0 if g = 0),         (0.3)

for `x = (g, β, c)`, with `I` #242's (2.5).
- By #244's Theorem A (conditional; *Not claimed*), `I(t, χ₀) = Φ(1 − t, χ₀ + 8 − 12t)` for `(t, χ₀)` off the curve
  `Δ = {(χ₀ + 8 − 12t)² = 64(1 − t)³}` (#244's `σ² = c′³`, with `σ = R/8` and `c′ = 1 − t`). The at most three `φ` that Theorem A excludes do not affect (2.5), and #244's Remark 2 gives
  `I(0, 0) = Φ(1, 8) = 20/3` at `(0, 0) ∈ Δ`.
- Below, `I` means `Φ` everywhere. For `k > 0` and `g ≠ 0`, `(t, χ₀)` has a density under every law used here, so this
  changes nothing; at `k = 0`, `(t, χ₀) = (0, 0)`.
- Put `I_quad(t, χ₀) := 20/3 − 20t + (8/9)χ₀ + (52/3)t² − (4/3)tχ₀ + (13/486)χ₀²`. It is the Taylor polynomial of `Φ` at
  `(0, 0)` to second order. `Φ` is analytic there, since the largest root `y = 2` of `(y − 2)(y + 1)²` is simple. This was
  checked symbolically and is not used in the proofs.

Constants: `𝒮_d := ∫_{S^{d−1}}∫_RF₀ db dσ` for the model's `F₀` (#242's Corollary 1′: `25√3/(48π²)` in `d = 2` and
`125√30/(192π³)` in `d = 3`), positive by #242's Theorem 1 (`𝔇 > 0`). `J` is note C3's (G), and `Ĩ := ∫_0^∞v⁴(H(v^{−3}) − 1)dv` is #242's (4.2) and note SL's
Remark 2. Finally

    E_d(L) := 3d·3^{d−1}(76d³L⁶ + 15)e^{−L²/2},        δ_d(L) := 4N·E_d(L).                                       (0.4)

**Lemma 0 (the two coefficients).** The limits (0.1) exist for `ψ^c` and `ψ^R`, under `Σ_{L,u}` and `Σ_∞`. Moreover
`c₃(L) = 𝒦^{ψ^c}(L)` and `R_{2/3}(L) = 𝒦^{ψ^R}(L)`, with note C3's (C3) and note SL's (SL); the latter uses `I = Φ` and is
at #244 Theorem A's conditional scope. The model values are
`𝒦^{ψ^c}(∞) = c₃^∞ := (J/30)𝒮_d` and `𝒦^{ψ^R}(∞) = R^∞ := Ĩ𝒮_d`. All four integrals (0.2) converge absolutely.

**Lemma 1 (the model's jet law).**
- (a) The entries of `Σ_∞` are integers of absolute value at most `15`, and `Σ_∞ − I/4` is positive definite. The least
  pivot of its `LDLᵀ` factorization is `3/4` in `d = 2` and `329/556` in `d = 3`, both in the order of control V1 and in
  the order of `X`.
- (b) Given `P_o = (0, …, 0, 12k)`, the odd free jets `O` are centred. For every unit `e ⊥ u`, `x_e` has covariance
  `diag(2, 2, 6)`. The density of `P_o` at its target is `p^o_∞(0)e^{−12k²}`, that is, `q_∞ := 72[(Cov P_o)^{−1}]_{ll} = 12`
  for the `∂_u³f` coordinate `l`.
- (c) Given `P_e = 0`, `A` is centred Gaussian and independent of `(P_o, O)`. The same holds for every parity-split `Σ`.

**Lemma 2 (the image bound).** For `d ∈ {2, 3}`, every real `L ≥ 10`, every `u` and every orthonormal `Θ`, every entry of
`Σ_{L,u} − Σ_∞` has absolute value at most `E_d(L)`. Hence, with `δ = δ_d(L)`,

    (1 − δ)Σ_∞ ≼ Σ_{L,u} ≼ (1 + δ)Σ_∞.                                                                              (0.5)

`E_d` and `δ_d` decrease in `L` on `[10, ∞)`. Rounded up: `δ₂(10) ≤ 7.60·10⁻¹¹`, `δ₂(24) ≤ 6.31·10⁻¹¹²`,
`δ₃(10) ≤ 2.44·10⁻⁹` and `δ₃(24) ≤ 2.03·10⁻¹¹⁰`.

**Lemma 3 (homogeneity and the sandwich).** Let `ρ_k(x) ≥ 0` be `ι`-invariant with `ρ_{sk}(sx) = s⁶ρ_k(x)` for `s > 0`, and
put `Pos_Σ[ρ] := (1/3)∫_0^∞k^{−8/3}Ψ_Σ^ρ(k)dk ∈ [0, ∞]`, per direction `u`.
- (a) For `τ > 0`, `Ψ_{τΣ}^ρ(k) = Ψ_Σ^ρ(k/√τ)` (when the right side exists) and `Pos_{τΣ}[ρ] = τ^{−5/6}Pos_Σ[ρ]`.
- (b) If `Σ` is parity-split, `(1 − δ)Σ_∞ ≼ Σ ≼ (1 + δ)Σ_∞` with `0 ≤ δ ≤ 10⁻⁸`, and (0.1) exists under `Σ` and `Σ_∞`, then
  `|Pos_Σ[ρ] − Pos_{Σ_∞}[ρ]| ≤ (N + 1)δ·Pos_{Σ_∞}[ρ]`.
- (c) Under the same hypothesis, put `w_Σ := p^o_Σ(0)𝔈_Σ`, where `p^o_Σ(0)` is the density of `P_o` at `0` and
  `𝔈_Σ := lim_{ε↓0}ε^{−1}∫P(a)²1{−ε < λ_m(a) < 0}p^e_Σ(0, a)da`, with `p^e_Σ` the density of `(P_e, A)`. Then
  `|w_Σ/w_{Σ_∞} − 1| ≤ 2Nδ`.
- (d) If `Σ` is parity-split and `(1 − δ)Σ_∞ ≼ Σ ≼ (1 + δ)Σ_∞` with `0 ≤ δ < 1` (neither `δ ≤ 10⁻⁸` nor the existence of
  (0.1) is needed), then
  `q_Σ := 72[(Cov_ΣP_o)^{−1}]_{ll} ∈ [12/(1 + δ), 12/(1 − δ)]`.
- (e) Under the hypothesis of (d), for every unit `e ⊥ u`, given `P_o = (0, …, 0, 12k)`, `x_e` is Gaussian with mean `kμ_e`
  and covariance `S_e`, where `|μ_{e,i}| ≤ 12δ/(1 − δ)` and `|(S_e − diag(2, 2, 6))_{ij}| ≤ 6δ`.

**Lemma 4 (the polynomial part).** Let `Π_k(x)` be a polynomial in `(k, x)` with `Π_{−k}(−x) = Π_k(x)` and
`Π_k(ιx) = Π_k(x)`, and `Σ` parity-split and nondegenerate. Put `v_o(k) := (0, …, 0, 12k)`, the odd pins' target, and
`m_Σ(k, e) := E[Π_k(x_e) | P_o = v_o(k)]`. Then `m_Σ(k, e) = Σ_{j even}a_j^Σ(e)k^j`, a polynomial in `k` with only even
powers, whose coefficients are polynomials in `e`, even in `e`. Moreover

    Ψ_Σ^Π(k) = p^o_Σ(0) e^{−q_Σk²} 𝔈_Σ[m_Σ(k, ·)],
    (1/3)∫_0^∞ k^{−8/3}(Ψ_Σ^Π(k) − Ψ_Σ^Π(0)) dk = (1/3) p^o_Σ(0) Σ_j 𝔈_Σ[a_j^Σ] G_j(q_Σ),                          (0.6)

with `𝔈_Σ[φ] := lim_{ε↓0}ε^{−1}∫φ(e(a))P(a)²1{−ε < λ_m(a) < 0}p^e_Σ(0, a)da`, `G₀(q) = −(3/5)Γ(1/6)q^{5/6}`, and
`G_j(q) = (1/2)Γ((3j − 5)/6)q^{−(3j−5)/6}` for even `j ≥ 2`. In particular

    G₂(q) = (1/2)Γ(1/6)q^{−1/6},   G₄(q) = (1/12)Γ(1/6)q^{−7/6},   G₆(q) = (7/72)Γ(1/6)q^{−13/6}.

For `Π^c` and `Π^R` below, which are jointly homogeneous of degree 6 in `(k, x)`, only `j ≤ 6` occurs.

**Lemma K (a global bound for `Φ`).** For all real `t` and `χ₀`,

    |Φ(1 − t, χ₀ + 8 − 12t) − I_quad(t, χ₀)| ≤ 324 (t² + |t|³ + |χ₀| + χ₀²).                                         (K)

So (K) holds for #242's `I` wherever `I = Φ`: off `Δ` at #244 Theorem A's conditional scope, and at `(0, 0)`. Lemma K itself
is a statement about the explicit function `Φ` and is not conditional. Its proof cites #244's Remark 4, (3.1)–(3.2) of
Corollary A.1, and Lemma B.2(a) and (c). #244's disposition places these, like everything after its Theorem A, under that
theorem's condition, but their proofs are algebra and calculus on the cubic and use neither #170 nor [CUB].

**Lemma J.** `1/2000 ≤ J ≤ 10`.

**Theorem V (the transfer).** Let `d ∈ {2, 3}` and `L₀ ∈ {10, 24}`. For every real `L ≥ L₀`, `|c₃(L) − c₃^∞| ≤ η_c𝒮_d` and
`|R_{2/3}(L) − R^∞| ≤ η_R𝒮_d`, with `η_c` and `η_R` the entries of the table above for that `L₀`. The `R_{2/3}` bound is at
#244 Theorem A's conditional scope; the `c₃` bound does not use #244.

**Corollary V1.** For `d ∈ {2, 3}` and every real `L ≥ 10`, `c₃(L) ≥ (1/60000 − 1.97·10⁻⁷)𝒮_d > 0`. So the remainder
`O(ℓ^{2/3})` of note LU's Theorem P⁺ is of exact order `ℓ^{2/3}` for these torus fields, in particular for SIDE24.

**Corollary V2.** For `d ∈ {2, 3}` and every real `L ≥ 24`,

    |(c₃(L) − R_{2/3}(L)) − (J/30 − Ĩ)𝒮_d| ≤ η_{C7}𝒮_d,        η_{C7} = 4.2·10⁻¹⁰⁵ (d = 3),  6.5·10⁻¹⁰⁷ (d = 2).        (V2)

This is at #244 Theorem A's conditional scope. Write `Ĩ = Ĩ_quad + D`, with `Ĩ_quad := −(112/675)Γ(1/6)12^{−1/6}` and `D` as
in (5.3). Then `J/30 − Ĩ ≥ 0.6103 − D`. So `J/30 − Ĩ > 0`, and with it note C7's `ℓ^{2/3}` coefficient at every `L ≥ 24`
(in `d = 2, 3`), as soon as `D ≤ 0.61`.

## 1. The two coefficients and the model's jet law

*Proof of Lemma 0.*
- *Existence.* Each weight here is a function of `(k, x_e)`, and `|ψ^c_k(x)| + |ψ^R_k(x)| ≤ C(1 + k)⁴(1 + |x|)⁶`; for `ψ^R`
  this uses #242's Lemma 3, `g⁶I ≤ (8000/3)max(g⁶, 1728k³|β|³, 331776k⁴c²)`. By Lemma 1(c) (for `Σ_∞`; for the torus field,
  note C3's Lemma 0 proof via #237's Lemma R (R.2)), the odd jets are independent of `A` given the pins. So
  `E[ψ_k(x_e) | A, pins] = h_k(e(A))`, a bounded function of `e` for each `k`. Note C3's proof of Lemma 0 then applies
  verbatim, with `h_k` in place of its `E[|U_red|³ | A]`: by Weyl's integration formula the limit exists, and equals the
  pin density times note C3's (1.1). The same holds under `τΣ_∞` for every `τ > 0`, and for every weight below, since each
  is bounded by `C(1 + k)⁴(1 + |x|)⁶`.
- *`c₃`.* Note C3 defines `𝐄(k, u) = (12/(9k))[p_{V₀}(v(k))𝔏(k, u) − p_{V₀}(v(0))𝔏(0, u)]`, with
  `𝔏(k, u) = 𝔼_{Q̄_{0,k}}[P²|U_red|³; λ_m = 0⁻]` and `U_red = 3kB_ee − γ_e²/4` (C3 (0.1)–(0.3)). A pin density times a
  conditional expectation is the integral against the joint density at the pins, so `p_{V₀}(v(k))𝔏(k, u) =
  Ψ_{Σ_{L,u}}^{|U_red|³}(k)`. Then `𝐄k^{−5/3} = (4/3)k^{−8/3}(Ψ^{|U_red|³}(k) − Ψ^{|U_red|³}(0))`, and (C3) is `𝒦^{ψ^c}(L)`.
  The absolute convergence is note C3's bound `|𝐄| ≤ C min(k, 1/k)`. The model value is note C3's (G.3).
- *`R_{2/3}`.* In (SL) put `v = k^{−1/3}`: `v⁴dv = −(1/3)k^{−8/3}dk`, so
  `R_{2/3} = (1/3)∫_S∫_0^∞k^{−8/3}(ℱ(k, u) − ℱ₀(u))dk dσ`, absolutely convergent by note SL. It remains to show
  `ℱ(k, u) = Ψ^{ψ^R}(k)` for `k ≥ 0` (at `k = 0`, `ℱ(0, ·)` means `ℱ₀`). By note SL (0.1) and #242 (3.1),
  `ℱ(k, u) = ∫_R12π₀(u; v₀(b, k))·lim_ε ε^{−1}E_{v₀(b,k)}[(γ₁⁶/384)(λ₂⋯λ_m)²I(12kB₁/γ₁², 576k²C₁/γ₁³)1{A < 0, λ₁ < ε}]db`.
  As in note C3's proof of the identity `a₁ = (1/10)∫F₀db` (its §3):
  - #242's `λ₁ < ⋯ < λ_m` are the eigenvalues of `−A`, so `{A < 0, λ₁ < ε} = {−ε < λ_m(A) < 0}` and
    `(λ₂⋯λ_m)² = P(A)²`. The eigenvector of `λ₁` is `±e(A)`, so `(γ₁, B₁, C₁) = (±g_e, β_e, ±c_e)` with one sign, and `t`
    and `χ₀` are unchanged. Since `12/384 = 1/32`, the weight is `ψ^R_k(x_e)`.
  - For each `ε`, Tonelli and the disintegration of (R.1) at `r = 0` (as in #237 Step U4) turn the `b`-integral of the
    `ε`-quotients against `π₀(u; v₀(b, k))` into the birth-integrated `ε`-quotient of (0.1).
  - Domination in `b`, for `0 < ε ≤ 1`. By parity (#237's Lemma R (R.2) at `r = 0`), the law of `(A, f₄)` under
    `v₀(b, k)` is its law under `v₀(b, 0)`, and given `A` and `b` the odd jets have a law depending on neither. So
    `E[γ₁⁶I | A, b] ≤ C_k` by #242's Lemma 3, and #242 (1.1a)–(1.1b) give
    `ε^{−1}E₀[(λ₂⋯λ_m)²1{A < 0, λ₁ < ε} | b] ≤ C(1 + |b|)^N` (the bound of #242's proof of Corollary 1′, as used in note
    C3 §3). Also `π₀(u; v₀(b, k)) ≤ Ce^{−cb²}` ([R] (R5)).
  - For each `b`, the `ε`-limit in #242 (3.1) exists, by the same Weyl argument applied conditionally on `b`.

  Dominated convergence gives `ℱ(k, u) = Ψ^{ψ^R}(k)`. At `k = 0`, `I(0, 0) = 20/3` (proved directly in #242's proof of its
  Theorem 1; #244's Remark 2) and
  `ψ^R_0 = (5/24)g⁶`; this is note C3's identity, with `F₀ = (5/24)π₀𝔇`. For the model value, Lemma 1(b)–(c) and #242's
  Proposition 4(1) give `Ψ_∞^{ψ^R}(k) = 25w_∞H(k)`, with `w_∞` as in §3. So
  `𝒦^{ψ^R}(∞) = 25|S^{d−1}|w_∞·(1/3)∫_0^∞k^{−8/3}(H(k) − 1)dk = Ĩ𝒮_d`, which is note SL's Remark 2. ∎

*Proof of Lemma 1.* (a) The entries are `(−1)^{|β|}∂^{α+β}φ(0)`, with `∂^γφ(0) = ∏_i(−1)^{γ_i/2}(γ_i − 1)!!` when every `γ_i`
is even and `0` otherwise (note C3 §5). Every `|α + β| ≤ 6`, so the entries are integers of absolute value at most `5!! = 15`.
The `LDLᵀ` factorization of `Σ_∞ − I/4` is exact (control V1). (b) By #242's (0.3), given `∇f(0) = 0` and for every unit
`e ⊥ u`, the jets `(∂_u³f, g_e, β_e, c_e)` are independent with variances `(6, 2, 2, 6)`, and uncorrelated with every even
jet. Conditioning further on `∂_u³f = 12k` leaves the law of `x_e` unchanged, centred with covariance `diag(2, 2, 6)`, and
gives the density factor `e^{−(12k)²/12} = e^{−12k²}`. Since `O` is determined by the `x_e` over all `e` (the polynomials
`e ↦ ⟨e, γ⟩`, `B[e, e]` and `C[e, e, e]` determine `γ`, `B` and `C`), `O` is centred. Control V1 checks all of this
exactly, on six rational unit vectors `e` in `d = 3` and on `e = ±θ₁` in `d = 2`. (c) Parity: `P_e` and `A` are even, `P_o` and `O` odd; for Gaussian vectors
uncorrelated means independent, and the conditional mean of `A` given `P_e = 0` is `0`. ∎

## 2. The image bound, the sandwich and homogeneity

*Proof of Lemma 2.* This is OpenAI's `cusp_torus_transfer` §4 at derivative order `6`.
- For unit `v₁, …, v_j`, `D^jφ(x)[v₁, …, v_j]` is `φ(x)` times a signed sum over the partial matchings of `{1, …, j}`. Each
  unmatched `i` contributes `x·v_i` and each pair `{i, i′}` contributes `v_i·v_{i′}`. There are `T_j` partial matchings
  (the telephone numbers `1, 1, 2, 4, 10, 26, 76` for `j ≤ 6`), and each term is at most `max(1, |x|)^j` in absolute value.
  So `|D^jφ(x)| ≤ 76|x|⁶φ(x)` for `|x| ≥ 1` and `j ≤ 6`. At `x = 0` only perfect matchings survive: `|D^jφ(0)| ≤ 5!! = 15`.
- The shell `|n|_∞ = a ≥ 1` has `(2a + 1)^d − (2a − 1)^d ≤ 2d·3^{d−1}a^{d−1}` points (by the mean value theorem, at most
  `2d(2a + 1)^{d−1} ≤ 2d(3a)^{d−1}`), with `|n|⁶ ≤ d³a⁶` and
  `e^{−L²|n|²/2} ≤ e^{−L²a²/2}`. For `L ≥ 10` and `s ≤ d + 5 ≤ 8`, successive terms of `Σ_{a≥1}a^se^{−L²a²/2}` have ratio at
  most `2⁸e^{−150} < 1/3`, so the sum is at most `(3/2)e^{−L²/2}`. Hence `Σ_{n≠0}|D^jφ(Ln)| ≤ 228d⁴3^{d−1}L⁶e^{−L²/2}` and
  `S_L := Σ_{n≠0}φ(Ln) ≤ 3d·3^{d−1}e^{−L²/2}`.
- `D^jK_L(0) − D^jφ(0) = [Σ_{n≠0}D^jφ(Ln) − S_LD^jφ(0)]/(1 + S_L)`, so its absolute value is at most
  `3d·3^{d−1}(76d³L⁶ + 15)e^{−L²/2} = E_d(L)`, in every frame. Every entry of `Σ_{L,u} − Σ_∞` is such a difference with
  `j ≤ 6`.
- The perturbation `Δ := Σ_{L,u} − Σ_∞` has operator norm at most its Frobenius norm, at most `N·E_d(L)`. By Lemma 1(a),
  `I ≼ 4Σ_∞`, so `±Δ ≼ NE_d(L)·I ≼ 4NE_d(L)Σ_∞ = δΣ_∞`. This is (0.5).
- `(aL⁶ + b)e^{−L²/2}` with `a, b > 0` decreases when `L² > 6`. The four values are control V2's, from rational upper
  bounds of `e^{−L²/2}` (reciprocals of partial sums of the exponential series). ∎

*Proof of Lemma 3.* (a) In (0.1) under `τΣ`, `p_{τΣ}(v(k), a, o) = τ^{−N/2}p_Σ(v(k/√τ), a/√τ, o/√τ)`, since the target
`v(k)` is linear in `k`. Substitute `a = √τ·a′` and `o = √τ·o′`. The Lebesgue measure gives `τ^{n/2}` with `n = N − q`;
the weight gives `τ³`, at `k/√τ`; `P²` gives `τ^{m−1}`; and the event `{−ε < λ_m < 0}` becomes `{−ε/√τ < λ_m(a′) < 0}`,
which gives `τ^{−1/2}` against `ε^{−1}`. The total exponent is `−q/2 + 3 + (m − 1) − 1/2 = −(2d + 1)/2 + 3 + (d − 2) − 1/2 = 0`.
In `Pos`, `k = √τ·k′` gives `k^{−8/3}dk = τ^{1/2−4/3}k′^{−8/3}dk′ = τ^{−5/6}k′^{−8/3}dk′`. Birth is integrated, so `q` is
`2d + 1` and not `2d + 2` (control V3, mutant M3).

(b) For positive definite `Σ` with `(1 − δ)Σ_∞ ≼ Σ ≼ (1 + δ)Σ_∞`, inverses and determinants give, pointwise on `R^N`
(OpenAI's (T15)),

    ((1 − δ)/(1 + δ))^{N/2} p_{(1−δ)Σ_∞} ≤ p_Σ ≤ ((1 + δ)/(1 − δ))^{N/2} p_{(1+δ)Σ_∞}.                                (2.1)

Multiply by the nonnegative weight, divide by `ε`, let `ε ↓ 0`; the limits under `(1 ± δ)Σ_∞` exist by (a). Then integrate
against `k^{−8/3}dk`. By (a),
`((1 − δ)/(1 + δ))^{N/2}(1 − δ)^{−5/6}Pos_{Σ_∞} ≤ Pos_Σ ≤ ((1 + δ)/(1 − δ))^{N/2}(1 + δ)^{−5/6}Pos_{Σ_∞}`. With
`log((1 + δ)/(1 − δ)) ≤ 2δ/(1 − δ)` and `e^x ≤ 1 + x + x²` for `0 ≤ x ≤ 1`, the upper factor is at most
`e^{Nδ/(1−δ)} ≤ 1 + (N + 1)δ` for `δ ≤ 10⁻⁸`, and the lower factor is at least `e^{−Nδ/(1−δ)} ≥ 1 − (N + 1)δ`.

(c) The principal blocks inherit the sandwich. `p^o_Σ(0) = (2π)^{−(d+1)/2}det(Cov_ΣP_o)^{−1/2}`, so
`p^o_Σ(0)/p^o_{Σ_∞}(0) ∈ [(1 + δ)^{−(d+1)/2}, (1 − δ)^{−(d+1)/2}]`. For `𝔈`, argue as in (a) and (b) on the block `(P_e, A)`,
of dimension `N_e := d + m(m + 1)/2`. The scaling exponent is `−N_e/2 + m(m + 1)/4 + (m − 1) − 1/2 = (d − 5)/2 < 0`, so
`(1 + δ)^{(d−5)/2} ≤ 1 ≤ (1 − δ)^{(d−5)/2}`, and `𝔈_Σ/𝔈_{Σ_∞} ∈ [((1 − δ)/(1 + δ))^{N_e/2}, ((1 + δ)/(1 − δ))^{N_e/2}]`.
Multiply. Since `(d + 1)/2 + N_e ≤ N`, the product lies in `[e^{−Nδ/(1−δ)}, e^{Nδ/(1−δ)}] ⊂ [1 − 2Nδ, 1 + 2Nδ]`. Control V3
also checks the exact factors, as rational inequalities, at `δ_d(10)` and `δ_d(24)`.

(d) From (0.5) on the `P_o` block, `(1 + δ)^{−1}(Cov_{Σ_∞}P_o)^{−1} ≼ (Cov_ΣP_o)^{−1} ≼ (1 − δ)^{−1}(Cov_{Σ_∞}P_o)^{−1}`. Take
the `(l, l)` entry, and `q_∞ = 12` (Lemma 1(b)).

(e) *Covariance.* The conditional covariance `S_Σ` of `O` given `P_o` is the inverse of the `O`-block of the inverse of
`Cov_Σ(P_o, O)`. Inverting the sandwich of that block and restricting to the `O`-block gives
`(1 + δ)^{−1}S_∞^{−1} ≼ S_Σ^{−1} ≼ (1 − δ)^{−1}S_∞^{−1}`, so `(1 − δ)S_∞ ≼ S_Σ ≼ (1 + δ)S_∞`. If `−δS ≼ D ≼ δS` with
`S ≻ 0`, then `|wᵀDw′| ≤ δ(wᵀSw)^{1/2}(w′ᵀSw′)^{1/2}`. Applied to the weights of `g_e`, `β_e` and `c_e`, whose model
variances are `2`, `2` and `6` (Lemma 1(b)), this gives `|(S_e − diag(2, 2, 6))_{ij}| ≤ δ·6`.

*Mean.* Let `Y` be one of `g_e`, `β_e`, `c_e`, with model conditional variance `s_Y ∈ {2, 6}`. Let `Y′ := Y − ℓ(P_o)` be its
residual after the *model's* linear regression `ℓ` on `P_o`. In the model, `Cov_∞(Y′, P_o) = 0`, `Var_∞(Y′) = s_Y`, and
`ℓ(0, …, 0, 12k) = 0` (Lemma 1(b)). Under `Σ`,
`E_Σ[Y | P_o = (0, …, 0, 12k)] = E_Σ[Y′ | P_o = ⋯] = 12k·Cov_Σ(Y′, Z)`, with `Z := ((Cov_ΣP_o)^{−1}e_l)ᵀP_o`. Since
`Cov_∞(Y′, Z) = 0`, the bilinear bound gives `|Cov_Σ(Y′, Z)| ≤ δ·s_Y^{1/2}·Var_∞(Z)^{1/2}`. Moreover
`Var_∞(Z) ≤ (1 − δ)^{−1}Var_Σ(Z) = (1 − δ)^{−1}[(Cov_ΣP_o)^{−1}]_{ll} ≤ (1 − δ)^{−2}[(Cov_{Σ_∞}P_o)^{−1}]_{ll} = (1 − δ)^{−2}/6`.
So `|μ_Y| ≤ 12δ(s_Y/6)^{1/2}/(1 − δ) ≤ 12δ/(1 − δ)`. ∎

## 3. The polynomial part

*Proof of Lemma 4.* By parity and Lemma 1(c), `p_Σ(v(k), a, o) = p^e_Σ(0, a)·p^{oO}_Σ(v_o(k), o)`, where `p^{oO}_Σ` is the
density of `(P_o, O)`. Also `p^{oO}_Σ(v_o(k), o) = p^o_Σ(v_o(k))·p_Σ(o | P_o = v_o(k))`, with `p^o_Σ` the density of `P_o` and
`p^o_Σ(v_o(k)) = p^o_Σ(0)e^{−q_Σk²}`; the factor is `exp(−(1/2)(12k)²[(Cov_ΣP_o)^{−1}]_{ll})`. Integrating `o` first gives
the first line of (0.6).
- *Evenness in `k`.* Given `P_o = v_o(k)`, `x_e ~ N(kμ_e, S_e)`, since the conditional mean is linear in the target. So
  `E[Π_k(x_e)]` is a polynomial in `k` (Isserlis), and
  `m_Σ(−k, e) = E_{N(−kμ_e, S_e)}[Π_{−k}(x)] = E_{N(kμ_e, S_e)}[Π_{−k}(−x)] = m_Σ(k, e)`. So only even powers occur.
- *Evenness in `e`.* `x_{−e} = ιx_e` gives `μ_{−e} = ιμ_e` and `S_{−e} = ιS_eι`, so
  `m_Σ(k, −e) = E_{N(kμ_e, S_e)}[Π_k(ιx)] = m_Σ(k, e)`. So `𝔈_Σ[a_j^Σ]` is well defined, and it exists as in Lemma 0.

Then

    ∫_0^∞k^{−8/3}(e^{−qk²} − 1)dk = (1/2)Γ(−5/6)q^{5/6},        ∫_0^∞k^{j−8/3}e^{−qk²}dk = (1/2)Γ((3j − 5)/6)q^{−(3j−5)/6},

with `Γ(−5/6) = −(6/5)Γ(1/6)`, `Γ(7/6) = Γ(1/6)/6` and `Γ(13/6) = (7/36)Γ(1/6)` (control V4). ∎

*The decomposition.* Put `X_k := g²/4 − 3kβ`, so `|3kβ − g²/4|³ = X_k³ + 2(−X_k)₊³`, and split

    ψ^c = Π^c + ρ^c,            Π^c := (4/3)X_k³,                  ρ^c := (8/3)(3kβ − g²/4)₊³,
    ψ^R = Π^R + ρ^R₊ − ρ^R₋,    Π^R := (1/32)g⁶I_quad(t, χ₀),      ρ^R_± := (1/32)g⁶(I − I_quad)_±(t, χ₀),               (3.1)

with `t = 12kβ/g²` and `χ₀ = 576k²c/g³`. Here `Π^R` is a polynomial:

    Π^R = (1/32)[(20/3)g⁶ − 240kβg⁴ + 512k²cg³ + 2496k²β²g² − 9216k³βcg + (26624/3)k⁴c²].

Both `Π`'s satisfy `Π_{−k}(−x) = Π_k(x)` and `Π_k(ιx) = Π_k(x)`. The `ρ`'s are nonnegative and `ι`-invariant, satisfy `ρ_{sk}(sx) = s⁶ρ_k(x)` (`t` and `χ₀` are
invariant under `(k, x) ↦ (sk, sx)`), and vanish at `k = 0` (`X₀ ≥ 0`; `t = χ₀ = 0` and `I(0, 0) = I_quad(0, 0)`).

*The model.* In the model, `μ_e = 0` and `S_e = diag(2, 2, 6)` for every `e` (Lemma 1(b)). So `a_j^∞` does not depend on
`e`, with `(a₀^∞, a₂^∞) = (5/2, 36)` for `Π^c`, and `(a₀^∞, a₂^∞, a₄^∞) = (25, 312, 1664)` for `Π^R` (control V4; for `Π^c`
this is note C3's `E[X³] = 15/8 + 27k²`). Also `w_∞ := p^o_∞(0)𝔈_∞ = 𝒮_d/(25|S^{d−1}|)`. Indeed, by Lemma 0's identity
at `k = 0` (note C3's identity, which does not use #244), `∫F₀db = (5/24)p^o_∞(0)𝔈_∞[E g⁶] = (5/24)·120·w_∞` in every
direction. By (0.6), with `ĝ_j := G_j/Γ(1/6)`, the polynomial parts of the model, integrated over the directions, are

    (1/3)∫_S w_∞Σ_ja_j^∞G_j(12)dσ = (𝒮_d/75)Γ(1/6)Σ_ja_j^∞ĝ_j(12):   0 for Π^c,   Ĩ_quad𝒮_d = −(112/675)Γ(1/6)12^{−1/6}𝒮_d for Π^R.   (3.2)

Indeed `Σ_ja_j^∞ĝ_j(q) = q^{−1/6}(18 − (3/2)q)` for `Π^c`, which vanishes at `q = 12`; this is note C3's (G.3). For `Π^R`,
`Σ_ja_j^∞ĝ_j(12) = 12^{−1/6}(−180 + 156 + 104/9) = −(112/9)12^{−1/6}`.

## 4. Lemma K and Lemma J

*Proof of Lemma K.* Write `c′ = 1 − t`, `R = χ₀ + 8 − 12t`, `Φ(c′, R) = |c′|δ² + δ³/3` with `δ = ψ_e − |c′|` (#244 (2.5)),
and write `I(t, χ₀)` for `Φ(c′, R)`.
- *Step 1: in `χ₀` at fixed `t`.* By #244's Lemma B.2(a) and (c), `Φ(c′, ·)` is continuous and convex, `C¹` off `R = 0`,
  and there `|∂_RΦ| = (ψ_e − c′)(ψ_e + c′)^{3/2}/(6ψ_e)` (B.2(a) with `ρ = ψ_e − 2c′`). The same follows from #244's cubic:
  with `y := ψ_e − c′`, it reads `(y − c′)²(y + 2c′) = R²/16`, where both `y − c′ = ψ_e − 2c′` and `y + 2c′ = ψ_e + c′` are
  nonnegative because `ψ_e ≥ ψ₀ = max(2c′, −c′)`. In both cases `c′ ≥ 0` (`δ = y`) and `c′ < 0` (`δ = y + 2c′`),
  `dΦ/dy = y(y + 2c′)`. Also `d[(y − c′)²(y + 2c′)]/dy = 3(y − c′)(y + c′)`, and `|R| = 4(y − c′)(y + 2c′)^{1/2}`. Here
  `(ψ_e − c′)/ψ_e ≤ 2`: for `c′ ≥ 0` it is at most `1`, and for `c′ < 0`, `ψ_e ≥ ψ₀ = |c′|`. So
  `|∂_RΦ| ≤ (ψ_e + |c′|)^{3/2}/3`. By #244's Remark 4, `ψ_e ≤ ψ₀ + (R²/16)^{1/3} ≤ 2|c′| + |R/4|^{2/3}`.
  With `(a + b)^{3/2} ≤ √2(a^{3/2} + b^{3/2})` and `|c′|^{3/2} ≤ √2(1 + |t|^{3/2})`,

      |∂_RΦ| ≤ 2√3(1 + |t|^{3/2}) + (√2/12)|R|.

  So `Φ(c′, ·)` is Lipschitz with this local constant. Between `χ₀ = 0` and `χ₀`,
  `|R| ≤ |χ₀| + 8 + 12|t|`. Using `|χ₀||t|^{3/2} ≤ (χ₀² + |t|³)/2` and `|χ₀||t| ≤ (χ₀² + t²)/2`,

      |I(t, χ₀) − I(t, 0)| ≤ (2√3 + 2√2/3)|χ₀| + (√3 + √2/12 + √2/2)χ₀² + √3|t|³ + (√2/2)t².                             (4.1)

- *Step 2: `χ₀ = 0`.* For `t ≤ 2/3`, #244's Corollary A.1 gives `ψ_e = 3/2 − 2t + (3/2)S`, `S := (1 − 4t/3)^{1/2}`, so
  `δ = 1/2 − t + (3/2)S`. Reducing `S² = 1 − 4t/3`, and writing `S = 1 − (2/3)t − (2/9)t² + R_S`,

      I(t, 0) = 20/3 − 20t + (52/3)t² − (8/3)t³ − t⁴ + (3/2)(2 − 5t + 3t²)R_S                                      (4.2)

  (control V7). Taylor's formula for `(1 − x)^{1/2}` at `x = 4t/3` gives `|R_S| ≤ (1/16)|x|³(1 − max(x, 0))^{−5/2}`, so
  `|R_S| ≤ (4/27)3^{5/2}|t|³ ≤ 2.31|t|³` on `|t| ≤ 1/2`. With `|2 − 5t + 3t²| ≤ 21/4` there,
  `|I(t, 0) − I_quad(t, 0)| ≤ (8/3 + 1/2 + (3/2)(21/4)(2.31))|t|³ ≤ 22|t|³` on `|t| ≤ 1/2`. For `|t| ≥ 1/2`, #244's Remark 4
  gives `δ ≤ |c′| + |2 − 3t|^{2/3} ≤ 3|t| + 98^{1/3}|t| ≤ 7.62|t|`, and `|c′| ≤ 3|t|`. So `I(t, 0) ≤ 3|t|δ² + δ³/3 ≤ 322|t|³`,
  and `|I_quad(t, 0)| ≤ (80/3 + 40 + 52/3)t² = 84t²`. Hence `|I(t, 0) − I_quad(t, 0)| ≤ 322(t² + |t|³)` for every `t`.
- *Step 3: the polynomial.* `|I_quad(t, χ₀) − I_quad(t, 0)| ≤ (8/9)|χ₀| + (2/3)(t² + χ₀²) + (13/486)χ₀²`.

Adding (4.1) and Steps 2–3, the coefficients of `|χ₀|`, `χ₀²`, `|t|³` and `t²` are `2√3 + 2√2/3 + 8/9 < 5.3`,
`√3 + 7√2/12 + 2/3 + 13/486 < 3.26`, `322 + √3 < 323.74` and `322 + √2/2 + 2/3 < 323.38`, all below `324` (control V7). This
is (K) for `Φ`. ∎

*Proof of Lemma J.* Here `J = (16/15)∫_0^∞e^{−12k²}E[(3kB − γ²/4)₊³]k^{−8/3}dk` with `γ, B` independent `N(0, 2)` (note C3 (G)).
- *Upper.* `(3kB − γ²/4)₊ ≤ 3kB₊`, and `E[B₊³] = 2^{3/2}(2/π)^{1/2}`. With `∫_0^∞k^{1/3}e^{−12k²}dk = (1/2)12^{−2/3}Γ(2/3)`,
  `12^{−2/3} ≤ 1/5` and `Γ(2/3) = (3/2)Γ(5/3) ≤ 3/2`: `J ≤ (16/15)·27·2^{3/2}(2/π)^{1/2}·(3/20) ≤ 10`.
- *Lower.* Restrict to `k ∈ [1/4, 1/2]`, `B ≥ 1` and `γ² ≤ 1/4`. There `3kB − γ²/4 ≥ 11/16` and `e^{−12k²} ≥ e^{−3}`, and
  `∫_{1/4}^{1/2}k^{−8/3}dk ≥ 2^{8/3}/4 ≥ 63/40`. Let `ϕ(x) := (2π)^{−1/2}e^{−x²/2}` be the standard normal density (not the
  kernel `φ` of §0). Then `P(B ≥ 1) = P(Z ≥ 2^{−1/2}) ≥ (1 − 2^{−1/2})ϕ(1)` and
  `P(γ² ≤ 1/4) = P(|Z| ≤ 2^{−3/2}) ≥ 2^{−1/2}ϕ(2^{−3/2})`, and rational bounds give `J ≥ 5.07·10⁻⁴ ≥ 1/2000` (control V6).
  Note C3's exploration value is `J = 4.1977820`. ∎

## 5. Proof of Theorem V and the corollaries

Fix `d`, `L ≥ L₀` and `u`, and put `δ := δ_d(L₀)`. By Lemma 2 and monotonicity, (0.5) holds with this `δ`. Every bound
below is nondecreasing in `δ`. Per direction, write `Pos_Σ[ρ] := (1/3)∫_0^∞k^{−8/3}Ψ_Σ^ρ(k)dk` (Lemma 3) and
`Γ_Σ[Π] := (1/3)p^o_Σ(0)Σ_j𝔈_Σ[a_j^Σ]G_j(q_Σ)` (the right side of (0.6)).

*The split is legitimate.* By (3.1), `Ψ^ψ = Ψ^Π + Ψ^{ρ₊} − Ψ^{ρ₋}` pointwise in `k`; the limits exist by Lemma 0's argument,
since every piece is bounded by `C(1 + k)⁴(1 + |x|)⁶`. Each of `k^{−8/3}(Ψ^Π(k) − Ψ^Π(0))` and `k^{−8/3}Ψ^{ρ_±}(k)` is
absolutely integrable on `(0, ∞)`, and `Ψ^{ρ_±}(0) = 0` since `ρ_0 = 0` (§3):
- the `Π`'s by Lemma 4;
- the `ρ`'s under `Σ_∞` by the next paragraph, and then under `Σ_{L,u}` by Lemma 3(b).

So, for `ψ = ψ^c` and `ψ = ψ^R`,

    𝒦^ψ(L) = ∫_{S^{d−1}} (Γ_{Σ_{L,u}}[Π] + Pos_{Σ_{L,u}}[ρ₊] − Pos_{Σ_{L,u}}[ρ₋]) dσ(u),                                   (5.0)

with `ρ₋ := 0` for `ψ^c`, and the same at `L = ∞`.

*The nonnegative parts.* In the model, `x_e ~ N(0, diag(2, 2, 6))` is independent of `A` given the pins, for every `e`
(Lemma 1(b)–(c)). So `Ψ_∞^ρ(k) = w_∞e^{−12k²}E[ρ_k(x)]` with `w_∞ = 𝒮_d/(25|S^{d−1}|)` (§3).
- For `ρ^c`, `(1/3)(8/3)∫_0^∞k^{−8/3}e^{−12k²}E[(3kβ − g²/4)₊³]dk = (1/3)(8/3)(15/16)J`, so `Pos_∞[ρ^c] = (5/6)w_∞J` and
  `∫_SPos_∞[ρ^c]dσ = (J/30)𝒮_d = c₃^∞`; with (3.2) this is consistent with Lemma 0. Moreover `J ≤ 10`.
- For `ρ^R_±`, Lemma K gives `ρ^R₊ + ρ^R₋ ≤ (324/32)g⁶(t² + |t|³ + |χ₀| + χ₀²)`, so
  `∫_S(Pos_∞[ρ^R₊] + Pos_∞[ρ^R₋])dσ ≤ 324·M·𝒮_d`, where

      M := (1/2400)∫_0^∞k^{−8/3}e^{−12k²}E[g⁶(t² + |t|³ + |χ₀| + χ₀²)]dk ≤ 0.72 + 0.49 + 6.52 + 23.04 < 31.             (5.1)

  The four terms use `E[g⁶t²] = 576k²`, `E[g⁶|t|³] = 1728k³E|β|³`, `E[g⁶|χ₀|] = 576k²E|c|E|g|³` and
  `E[g⁶χ₀²] = 1990656k⁴`, with `E|β|³ = E|g|³ ≤ 4.52`, `E|c| ≤ 2`, `Γ(1/6) ≤ 6`, `Γ(2/3) ≤ 3/2`, `Γ(7/6) ≤ 1`,
  `12^{−1/6} ≤ 1`, `12^{−2/3} ≤ 1/5` and `12^{−7/6} ≤ 1/18` (control V7).

By Lemma 3(b), the nonnegative parts contribute at most `(N + 1)δ(J/30)𝒮_d ≤ (N + 1)δ(1/3)𝒮_d` to `|c₃(L) − c₃^∞|`, and at
most `(N + 1)δ·324·31·𝒮_d` to `|R_{2/3}(L) − R^∞|`.

*The polynomial parts.* Per direction, write
`Γ_{Σ_{L,u}}[Π] = (1/3)Σ_j[a_j^∞w_L + p^o_L(0)𝔈_L[a_j^L − a_j^∞]]G_j(q_L)`, with `w_L := p^o_L(0)𝔈_L[1]` and the subscript `L`
for `Σ_{L,u}`. By Lemma 3(c)–(d), `|w_L − w_∞| ≤ 2Nδw_∞` and `|q_L − 12| ≤ 12δ/(1 − δ) < 1`. With `ĝ_j := G_j/Γ(1/6)`: on
`[11, 13]`, `|ĝ₀| ≤ (3/5)·13`, `|ĝ_j| ≤ |ĝ_j(1)|` for `j ≥ 2`, and `|ĝ_j′| ≤ 1/2`. Put `α_j := sup_e|a_j^L(e) − a_j^∞|` and
`ε₁ := 2Nδ`. Then

    |Γ_{Σ_{L,u}}[Π] − Γ_{Σ_∞}[Π]| ≤ (Γ(1/6)𝒮_d/(75|S^{d−1}|))·[ε₁|Σ_ja_j^∞ĝ_j(q_L)| + |Σ_ja_j^∞(ĝ_j(q_L) − ĝ_j(12))|
                                                                 + (1 + ε₁)Σ_jα_j sup_{[11,13]}|ĝ_j|].                   (5.2)

- For `Π^c` the first two terms are at most `(3/2)|q_L − 12|` each, since `Σ_ja_j^∞ĝ_j(q) = q^{−1/6}(18 − (3/2)q)`.
- For `Π^R` they are at most `ε₁Σ_j|a_j^∞|sup|ĝ_j|` and `|q_L − 12|Σ_j|a_j^∞|/2`.
- To bound `α_j`, Lemma 3(e) puts `x_e ~ N(kμ_e, S_e)`, with every entry of `μ_e` and of `S_e − diag(2, 2, 6)` in
  `[−η, η]`, `η := 13δ`, uniformly in `e`. Isserlis' theorem writes `E[x^α]` as a sum over the partial matchings of the
  factors: pairs give entries of `S_e`, unmatched factors give `kμ_{e,i}`. Control V5 evaluates these sums in exact
  rational interval arithmetic over that box, for every monomial of `Π^c` and `Π^R`. The resulting enclosures of the `a_j`
  give the `α_j`. The odd powers of `k` vanish exactly (Lemma 4), and their enclosures contain `0`.

*Assembly.* Integrate (5.2) over `S^{d−1}` and add the nonnegative parts. This gives `η_c` and `η_R` as functions of `δ`,
each nondecreasing. Control V8 evaluates them at `δ_d(10)` and `δ_d(24)`, which gives the table. ∎

*Proof of Corollary V1.* `c₃(L) ≥ c₃^∞ − η_c𝒮_d = (J/30 − η_c)𝒮_d ≥ (1/60000 − 1.97·10⁻⁷)𝒮_d > 0` (Lemma J; control V8),
and `𝒮_d > 0`. By note C3's Theorem C3, `c₃(L)` is the coefficient of `ℓ^{2/3}` in `ν_cand`. Since it is nonzero, the
remainder `O(ℓ^{2/3})` of note LU's Theorem P⁺ is attained. ∎

*Proof of Corollary V2.* (V2) is Theorem V for both coefficients: `η_{C7} ≥ η_c + η_R` at `L₀ = 24`. In the model, (5.0) at
`L = ∞` and (3.2) give `Ĩ𝒮_d = R^∞ = Ĩ_quad𝒮_d + ∫_S(Pos_∞[ρ^R₊] − Pos_∞[ρ^R₋])dσ`. So `Ĩ = Ĩ_quad + D`, where

    D := (1/2400)∫_0^∞ k^{−8/3} e^{−12k²} E[g⁶ (I − I_quad)(12kβ/g², 576k²c/g³)] dk,                                   (5.3)

for `g, β, c` independent `N(0, 2)`, `N(0, 2)` and `N(0, 6)`. Then `J/30 − Ĩ = J/30 + (112/675)Γ(1/6)12^{−1/6} − D`. Now
`Γ(1/6) = 6Γ(7/6)`, and `Γ(7/6) ≥ γ(7/6, 64) ≥ 0.9277`, from the alternating series of the lower incomplete gamma function
at `T = 64`, where `T^{1/6} = 2` (control V6). With `12^{−1/6} ≥ 0.6608` and `J ≥ 1/2000`, `J/30 − Ĩ ≥ 0.6103 − D`. Note C7's
Theorem C7 identifies `c₃ − R_{2/3}` as the coefficient of `ℓ^{2/3}` in `ν_eld − ν_eld^{far,r_0^*}`. ∎

## 6. Remarks

1. **Exploration values** (not part of the proofs; quadrature outside the repository).
   - `J = 4.1977819815839` (note C3 §5 and its Slice C referee) and `Ĩ = −0.5336676` (#244 §5).
   - `D = 0.0767381`. This is `Ĩ − Ĩ_quad` with #244's `Ĩ`. Two independent evaluations of (5.3) by this note's referees
     agree: a tensor quadrature split at the kinks gives `0.07673811 ± 5·10⁻⁸`, and a quasi-Monte Carlo gives
     `0.076735 ± 3·10⁻⁶`. The positive and negative parts are about `0.663146` and `0.586408`.
   - So `J/30 − Ĩ = 0.673594`. With `𝒮₃ = 0.1150058` and `𝒮₂ = 0.0914028`, note C7's model coefficient is `0.0774672`
     (`d = 3`) and `0.0615684` (`d = 2`). That is `1.85435c_{3,∞}` and `0.838727c_{2,∞}`, with the model values
     `c_{3,∞} = 0.041775932` and `c_{2,∞} = 0.073406919` of `c` (#216, #223; as in note C3 §5).
   - By Corollary V2 (at #244 Theorem A's conditional scope), the torus coefficients at every `L ≥ 24` differ from the model
     coefficients `(J/30 − Ĩ)𝒮_d` by at most `4.9·10⁻¹⁰⁶` (`d = 3`, which includes SIDE24) and `6·10⁻¹⁰⁸` (`d = 2`). So, if
     the quadrature is right, the digits above are also theirs.
   - Numerically the best constant in (K) is about `2.907`, not `324`.
2. **The four-term law at SIDE24.** Note C7 gives
   `ν_eld = cℓ^{−1/3} + c₁ℓ^{1/4} + c₂ℓ^{1/3} + (c₃ − R_{2/3})ℓ^{2/3} + ν_eld^{far,r_0^*} + o(ℓ^{2/3})` for the torus field,
   at its scope. At `L = 24`, `c` is enclosed by [SIDE24]; `c₁` by OpenAI's `cusp_torus_transfer` together with its
   reference interval; `c₂` by `c2_torus_transfer`'s certified interval `[0.1612340491269447, 0.1612340491269810]`
   (`d = 3`); and the fourth coefficient by Corollary V2, at #244 Theorem A's conditional scope, up to the model numbers `J`
   and `D`. These are cited, not re-derived. So, at that scope, a fully certified four-term elder law at SIDE24 needs, for
   the sign of the fourth coefficient, one more
   certified number: an upper bound `D ≤ 0.61`. That is a low-precision task, since the numerical margin is a factor of
   about eight. The value needs two: enclosures of `D` (equivalently of `Ĩ`) and of `J`. The request is in
   [6033651797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6033651797).
3. **Monte Carlo.** [6033651797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6033651797) (exploration)
   compares the four-term law, with this coefficient and no free parameter, against full-field persistence counts: #216's
   archived fields in `d = 2`, and #216's archived fields plus 2000 new ones in `d = 3`. On `[10⁻⁴, 3·10⁻²]` it lowers the
   field-level χ² from 84 to 23 (`d = 3`) and from 44 to 7 (`d = 2`), over 14 bins. Fitted freely on that range, the
   `ℓ^{2/3}` coefficient is `0.060 ± 0.007` in `d = 3` (2.4 standard errors below `0.0775`) and `0.054 ± 0.009` in `d = 2`;
   with the coefficient fixed, a small negative next-order term `kℓ^{3/4}` accounts for the difference (same comment). It is
   evidence about the coefficient's size, not a proof.
4. **Why the polynomial parts.** The nonnegative parts alone do not suffice. Near `k = 0`, each of `𝐋_Fk^{−5/3}` and
   `a₁k^{−8/3}` (note C3) behaves like `k^{−8/3}`, which is not integrable at `0`; in (0.2), `Ψ^{ψ^c}(k) → Ψ^{ψ^c}(0) > 0`
   against `k^{−8/3}`. The cancellation is exact in Gamma functions (Lemma
   4), and only the perturbation of finitely many conditional moments remains. The nonnegative parts vanish at `k = 0`:
   `E[ρ^c_k] = O(k³)`, and `E[ρ^R_±] = O(k²)` by Lemma K. So they are integrable against `k^{−8/3}`, and the sandwich applies
   to them.
5. **Other `d` and `L`.** The argument is dimension-free except for Lemma 1(a)'s floor, Lemma 2's lattice count (`L ≥ 10`,
   `d ≤ 3`), Lemma 3(c)'s sign `(d − 5)/2 < 0` (so `d ≤ 4`), the restriction `δ ≤ 10⁻⁸` in Lemma 3(b)–(c), and the sizes
   `N`. For `d ≥ 4` it needs the floor for the larger jet vector and the count for `d + 5 > 8`. Neither is checked here.

## 7. Exact controls (`v24_exact.py`; stdlib; exact rationals; deterministic; byte-identical under `-O`)

The script and its stdout are in the next comment, with the extraction rule.
- **V1** The model covariance of `X` in `d = 2, 3` from the derivative formula: symmetry, parity split, entries at most
  `15`, the exact `LDLᵀ` of `Σ_∞ − I/4` (pivots positive; the least, `3/4` and `329/556`, asserted); `q_∞ = 12`; the
  regression of `O` on the `∂_u³f` pin vanishes; `Cov(x_e | P_o) = diag(2, 2, 6)` on six rational unit vectors `e` in
  `d = 3` and on `e = ±θ₁` in `d = 2`.
- **V2** The telephone numbers `T_j` (`j ≤ 6`) and `Σ|coefficients of He_j| = T_j`; the perfect-matching maximum `15`; the
  shell count for `a ≤ 200` (the proof covers every `a`); `3·2⁸ < e^{150}`; rational upper bounds of `E_d(L)` and `δ_d(L)`
  at `L = 10, 24`.
- **V3** The homogeneity exponents `0`, `−5/6` and `(d − 5)/2`; the sandwich factors of Lemma 3(b)–(c) as exact rational
  inequalities at `δ_d(10)` and `δ_d(24)`.
- **V4** The Gamma ratios behind `G_j`, generated from `Γ(s + 1) = sΓ(s)` with `s_j = (3j − 5)/6` derived from the
  substitution `s = qk²` (and `−1 < s₀ < 0 < s_j`); the identity `Π^R = (1/32)g⁶I_quad(12kβ/g², 576k²c/g³)`, exactly on
  the grid `k ∈ {0, …, 4}`, `β, c ∈ {0, 1, 2}`, `g ∈ {1, …, 7}` (315 points; both sides are polynomials of degree at most
  `4, 2, 2, 6` in `k, β, c, g`, so this proves it); the model coefficients `a_j^∞` of `Π^c` and `Π^R` by exact Isserlis; the vanishing for `Π^c` and
  the value `−112/9` for `Π^R` in (3.2); `(1/3)(1/25)(8/3)(15/16) = 1/30`; and `E[g⁶I_quad] = 800 + 9984k² + 53248k⁴`.
- **V5** The interval enclosures of the `a_j` over the box of §5, with `η = 13δ ≥ 12δ/(1 − δ)`.
- **V6** Lemma J's two bounds from rational bounds of `π`, `√2`, `e^{−1/2}`, `e^{−1/16} ≥ 15/16`, `e^{−3}` and `2^{8/3}`; and,
  for Corollary V2, `Γ(7/6) ≥ 0.9277` from the alternating series of `γ(7/6, 64)` (300 terms, with the tail bounded by the
  next term), `12^{−1/6} ≥ 0.6608`, and `(112/675)·6·0.9277·0.6608 + 1/60000 ≥ 0.6103`.
- **V7** Lemma K: the reduction of `I(t, 0)` modulo `S² = 1 − 4t/3`, the identity (4.2), the constants of Steps 1–3, the
  four coefficient bounds `5.3`, `3.26`, `323.74` and `323.38`, the total `< 324`, and `M < 31`.
- **V8** The assembly at `δ_d(10)` and `δ_d(24)`: each of the table's eight entries lies between the computed bound and
  `1.01` times it; `η_c < 1/60000` at `L₀ = 10`; and both bounds are `≤ 10⁻¹⁰⁰` at `L₀ = 24`.
- **V9** Lemma K's Step 1: the polynomial identities `d[(y − c′)²(y + 2c′)]/dy = 3(y − c′)(y + c′)` and `dΦ/dy = y(y + 2c′)`
  for both branches; `(ψ − c′)/ψ ≤ 2` on `ψ ≥ ψ₀`; `(a + b)³ ≤ 2(a^{3/2} + b^{3/2})²` on rational squares; the cubic
  `(y − 2)(y + 1)²` at `(t, χ₀) = (0, 0)` and `Φ(1, 8) = 20/3`; and the vanishing of `ρ^c` at `k = 0`.

Mutants (each rejected with exit 1, empty stdout and `FAILED: <group>` on stderr): M1 floor `1/3` (V1); M2 `T₆ = 75` (V2);
M3 birth pinned, `q = 2d + 2` (V3); M4 `G₄`'s constant `1/6` (V4); M5 `a₂^∞ = 35` for `Π^c` (V4); M6 `J ≥ 1/1000` (V6);
M7 `K = 300` (V7); M8 `η = 12δ` (V5); M9 the claim `≤ 10⁻¹¹⁰` at `L = 24` (V8); M10 `(ψ − c′)/ψ ≤ 3/2` (V9); M11 the
coefficient `−9216` of `Π^R` changed to `−9215` (V4); M12 the nonnegative-part term of `η_R` dropped (V8).

The controls do not test note C3's or note SL's theorems, Lemma 0's dominated convergence, Weyl's formula, the existence
of the edge limits, Isserlis' theorem itself, the Gaussian density inequality (2.1), or #244's Theorem A. They check the
finite algebra and every numerical constant.

## 8. Review slices

- **A** (§§0–2): the setting, Lemma 0 (the identification of `c₃` and `R_{2/3}` as `𝒦^ψ`, and the `b`-integration), Lemma 1,
  Lemma 2 (the image bound and (0.5)), Lemma 3 (homogeneity, the sandwich, the moment bounds (e)), and controls V1–V3.
- **B** (§§3–4): Lemma 4, the decomposition (3.1), the model values (3.2), Lemma K, Lemma J, and controls V4, V6 and V7.
- **C** (§§5–6 and the header): the legitimacy of the split, (5.1)–(5.3), the assembly and the table, Corollaries V1 and
  V2, the remarks, the header for overclaim, and controls V5, V8 and V9.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_