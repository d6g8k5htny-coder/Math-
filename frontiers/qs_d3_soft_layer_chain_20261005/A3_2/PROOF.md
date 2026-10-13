## QS addendum A3.2: the `d ≥ 3` determinant weight in the window chart, and a map toward a `d ≥ 3` rate

**Object.** `CL-QS-A3-2-WEIGHT-FACTORIZATION-20261003-v1`.

**Who.** Anthropic Claude, the author of QS, A2, A3 and A3.1 ([5971014231](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971014231)), in session `session_01NMeKEismAyeqgdB4sy2NJU`. Dylan Roy — delegated AI work.

**Claim.** [5971258702](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971258702). This is author-side and deterministic. Scientific effect: NONE.

**Consumed (read, not edited):**
- **A3.1:** the chart of §0, Lemma N_d, Lemma SR′ and Theorem C_d.
- **A3:** Lemma SR.
- **[P] §1:** the weight `W_r = |det H_M det H_S| 1{H_M < 0, index H_S = d − 1}`.
- **#242:** Proposition 2′(c), which gives the factor `(λ₂⋯λ_m)²` and the remark that it is not uniform as `λ₂ → 0`.
- **SC** (`frontiers/spectral_cluster_closure_20260929/PROOF.md`): §5's limit `W_r/r⁴ → ∏h_j² w`, and (17).
- **HD:** Math-#184 Theorem 1, for the continuum kernel.
- **#175:** PROOF (E3)–(E7), together with SOURCE_INTERFACE (T1)–(T5).
- **C104.**
- **The planar chain C91–C103**, as incorporated in Math-#249.

### 1. Lemma WF (the weight in the window chart, exactly)

**Setting.**
- Let `f ∈ C²(X)` have the exact pins of [P] §1.
- Fix any orthonormal frame (axial unit vector, `e₁, …, e_{d−1}`) and any `γ ≠ 0`, `k > 0` and `r > 0`.
- Let `Ψ(u, Z, η) := Φ(u − Z/12, Z/γ, η)`, where `Φ(X, ζ, η)` is the midpoint plus `rX·axis + rkζe₁ + r^{3/2} Σ_{i≥2} η_i e_i`. Put `g := (f∘π∘Ψ − b)/(kr³)`.
- A3.1's chart is the special case in which `γ` and the frame are the midpoint jet and eigenframe of #243 §0. That case needs `f ∈ C³`.
- Write `x = (u, Z)` and `p̂ = (p, 0)` for `p ∈ {M, S}`.
- Suppose `g_ηη(p̂)` is nonsingular at both pins, and put `Σ_p := (g_xx − g_xη g_ηη⁻¹ g_ηx)(p̂)`.

**Statement.**

    W_r = k^{2(d−2)} γ⁴ r⁴ · |det g_ηη(M̂)| |det g_ηη(Ŝ)| · |det Σ_M| |det Σ_S|
          · 1{In g_ηη(M̂) + In Σ_M = (0, d, 0),  In g_ηη(Ŝ) + In Σ_S = (1, d − 1, 0)},          (WF)

where `In = (n₊, n₋, n₀)` counts positive, negative and zero eigenvalues. ([P]'s indicator allows a zero eigenvalue. After multiplication by `|det|`, the two indicators give the same product.)
- If `g_ηη ≺ 0` at both pins, the indicator is `1{Σ_M ≺ 0, In Σ_S = (1, 1, 0)}`.
- If A3's (B1)–(B2) hold on `Ω × B̄_ε` with `p ∈ Ω`, then `Σ_p = D²G(p)`, the reduced Hessian. This is SR(d), with `ζ(p) = 0` by SR(e).

*Proof.*
1. **The chart determinant.** `DΨ` is the product of `diag(r, rk, r^{3/2}, …, r^{3/2})`, in the frame above, with `diag(T, I)`, where `T = [[1, −1/12], [0, 1/γ]]`. So `|det DΨ| = k r^{2+3(d−2)/2}/|γ|`.
2. **The Hessians.** Since `Ψ` is affine, `kr³ D²g = DΨᵀ D²f DΨ`. Hence

       det D²f = k^{d−2} γ² r² det D²g,

   and `D²f` and `D²g` have the same inertia, by Sylvester's law.
3. **Schur and Haynsworth.** At `p̂`, Schur's formula gives `det D²g = det g_ηη · det Σ_p`, and Haynsworth's additivity gives `In D²g = In g_ηη + In Σ_p`. ∎

**Corollary WF (the explicit form).**

*Hypotheses.*
- The common hypotheses of A3.1 Theorem C_d (setting, jets, windows, error budget `δ`, and the barrel inequalities), with its `Ξ₂` and QS's `κ_•`.
- At both pins, `θ_p := Ξ₂/min(3, κ_p) < 2`.
  - The elder side (E) of Theorem C_d implies this, with `θ_S ≤ 2/5` and `θ_M < 1`.
  - On the rejected side (R) it is an **extra** hypothesis, and it is necessary. The clean-context referee constructed a rejected-side example that meets every (R) hypothesis but has `κ_M = 0.01` and `W_r = 0`. QS's scaling `(c, ψ, R, Z) ↦ (λ²c, λ²ψ, λ³R, Z/λ)` keeps `μ` fixed while `κ_• → 0`, so no bound on `θ_p` follows from (R).

*Conclusion.* Put

    a_M := 24λ̃ − γ² + 12kB = 48γ²κ_M,     a_S := 24λ̃ + γ² − 12kB = 48γ²κ_S.

Then the type indicator in (WF) equals 1, and

    W_r = r⁴ (λ₂ ⋯ λ_{d−1})² · (a_M a_S/16) · Θ,

with

    (1 − kδ/λ₂)^{2(d−2)} (1 − θ_M/2)² (1 − θ_S/2)²  ≤  Θ  ≤  (1 + kδ/λ₂)^{2(d−2)} (1 + θ_M/2)² (1 + θ_S/2)².

*Proof.*
1. **The hard factor.** `g_ηη = −Q + E_ηη`, with `Q = diag(λ_i)/k ⪰ (λ₂/k)I` and `‖E_ηη‖ ≤ δ < λ₂/(2k)`. By Weyl's inequality,

       det(Q − E_ηη)/det Q ∈ [(1 − kδ/λ₂)^{d−2}, (1 + kδ/λ₂)^{d−2}],

   and `g_ηη ≺ 0`.
2. **The reduced factor.**
   - `Σ_p = D²P(p) + D²e_G(p)`, with `‖J_p D²e_G(p) J_p‖ ≤ θ_p` (Lemma SR′ and A3 §2).
   - `J_S D²P(S) J_S = diag(2, −2)` and `J_M D²P(M) J_M = −2I`.
   - So by Weyl each eigenvalue moves by at most `θ_p < 2`. Hence `det Σ_p / det D²P(p) ∈ [(1 − θ_p/2)², (1 + θ_p/2)²]`, and the inertia is unchanged.
3. **The model values.**
   - `|det D²P(M) det D²P(S)| = 144 κ_M κ_S`, which equals `a_M a_S/(16γ⁴)` by the definitions above.
   - `det Q = ∏λ_i / k^{d−2}`. The powers of `k` cancel against `k^{2(d−2)}`. ∎

Both ends of each range are attained, by diagonal perturbations whose operator norm equals the bound.

**Remarks.**
- **The identity in SC's variables.** With `λ̃ = −ks`, `a = γ`, `β = B` and `B_SC = β − a²/(12k)`, we get `a_M = 12k(B_SC − 2s)` and `a_S = −12k(2s + B_SC)`.
  - On the typed domain `{a_M > 0, a_S > 0} = {s < −|B_SC|/2}`, which C_d's `λ̃ > 0` and `ψ > |c|` enforce, `a_M a_S/16 = 9k²(4s² − B_SC²)` is SC's `w`.
  - So Corollary WF is the finite-`r` version, with explicit errors, of SC §5's limit `W_r/r⁴ → ∏h_j² w` and of #242 Proposition 2′(c).
  - In `d = 2` it is C101's `w_λ = a_M a_S/16` on `T`, at `k = 1`.
- **The size of `Θ − 1`.**
  - Under FL.1′, `Θ − 1 = O(kδ/λ₂ + Ξ₂/min(3, κ_•))`. This is `O(r)` at fixed jets and `λ₂`.
  - It degenerates as `λ₂ → 0` and as `κ_• → 0`.
  - These strata have to be charged separately:
    - **The actual failure measure.** For the `λ₂` strip, #175 gives `lim_{η→0} limsup_{r→0} r⁻³Q_r^W(F_r, h₂ ≤ η) = 0`. This is PROOF (E5) and (E7), or SOURCE_INTERFACE (T3) for the endpoint and (T5) for the midpoint. Its depth branch is bounded by `Cη`, up to an `O(r)` exception, at small `r`.
    - **Review status of that input.** It is in a merged packet. It has an OpenAI slice ACCEPT for the failure exhaustion (5360905887) and a cross-provider composition read (5364258444).
    - **The contact level.** SC (17)'s hard density `∏h_j³ ∏(h_j − h_i)` gives `{h₂ ≤ t}` mass `O(t⁴)`. One `h_j²` comes from the hard determinant and one `h` from the soft–hard Vandermonde, as C104 §1 notes for `d = 3`.
    - **The typing edges `κ_• → 0`.** They are where `θ_p < 2` can fail, and they are the `d ≥ 3` counterpart of C93's edge envelopes.

### 2. A map toward a `d ≥ 3` rate for `1 − p_r`

In `d = 2` at `k = 1`, C101 (an author-side frozen candidate with a nonauthor PASS) proves `1 − p_r = r³(α₁ + α₂) + O_β(r^{3+β})`. It uses C91–C98 together with its own estimates, which are uniform as the cutoff grows. The table gives the `d ≥ 3` counterpart of each input. "Reviewed" means same-provider unless stated otherwise.

| `d = 2` input | role in C101 | `d ≥ 3` counterpart | status |
|---|---|---|---|
| C91 (pinned Taylor formulas) | window error | #242 (2.6); #243 FL.1 (both landed); A3.1 FL.1′, which is `O(Nr)` once `r^{1/2}η·a` is removed | FL.1′ author-side; FL.1's constants not explicit |
| C92 (actual regression, determinants, full normalizer) | finite-`r` law of the raw jets | [P] §§2–5 (qualitative, every `d`). C104 Lemmas 1–3 are torus-versus-continuum at contact (explicit, `d = 3`); they are not a finite-`r` regression. | **open** at finite `r` |
| C93 (typing-edge substitutions, Hessian formula) | weight algebra and edge envelopes | Lemma WF, and Corollary WF on the elder side (author-side); the `λ₂` strip by #175 (E5)/(T5) | rejected-side typing (`θ_p < 2`) and edge envelopes **open** |
| C94 with C82 (weighted saddle-level estimate) | mass near the decision boundary | the reduced height is planar (A3.1 Theorem C_d, author-side). HD Theorem 1 gives the contact-level soft law as `R_d(b)` times the planar law for the continuum kernel. On the `d = 3` torus C104 compares only the restricted coefficients `a_j`. | finite-`r` weighted estimate **open** |
| C95 (corrected trap, (G14)) | elder certificate | A3 QS-E′_d; A3.1 Theorem C_d and Lemma TL_d | author-side |
| C96 (maximin and H0 death) | event identification | the lemma is dimension-free (reviewed); its `d ≥ 3` use is A3.1 Corollary H_d | Corollary H_d author-side |
| C97 (two-margin chord) | rejected certificate and its weighted estimate | A3 QS-R_d; A3.1 Theorem C_d (R) | deterministic certificate author-side; weighted part **open** |
| C98 (sector coverage) | exhaustion of typed jets | the planar `(ψ, c, R)` sector algebra is unchanged | the `d ≥ 3` strata of A3.1 §9 are **open** |
| C101 and C103 (the rate) | — | — | **open** |
| CUB and the coefficient | `α₁ + α₂` | HD: `R_d(b)` times the planar value (continuum kernel; open PR with OpenAI reads); C104: the `a_j` on the `d = 3` torus (reviewed by OpenAI and Anthropic) | at those scopes |

**Qualitative `d ≥ 3` results already on file**, outside the table: [P]'s cap route in every `d`, and #175 Theorems H and F (merged; slice-reviewed).

**Summary.**
- *On file at author-side status*, for `k ∈ [k_−, k_+]` with `λ₂ > 0`, `γ ≠ 0` and `λ̃ > 0`:
  - the deterministic decision certificates: A3 QS-E′_d and QS-R_d; A3.1 Theorem C_d, Lemma TL_d and Corollary H_d;
  - the elder-side weight factorization, Corollary WF.
- *Not on file:*
  - rejected-side pin typing;
  - the measurability of the full certificate event;
  - the `d ≥ 3` strata;
  - the finite-`r` regression and weighted estimates, which are the C92, C93, C94, C97 and C101 analogues.

This map claims none of the open items.

### 3. Checks (exploration outside the repository)

- **`a32_exact.py`** (standard library; exact rationals), 8,291 checks:
  - W1, the chart determinant and inertia in `d = 3, 4` (600);
  - W2, Schur and Haynsworth (800);
  - W3, the conventions (1,500);
  - W4, the `Θ` ranges (5,391). These include the operator-norm extremes, which attain both ends of the reduced range.

  Four mutants exit 1, an unknown label exits 2, and the output under `-O` is byte-identical. The file's SHA-256 is `52d90865…` and its stdout's is `f2f5d0ae…`.
- **`a32_numeric.py`** (numpy). On 40 exactly pinned degree-6 fields in `d = 3`:
  - The largest values of `|W_r/(r⁴λ₂²a_Ma_S/16) − 1|` are `4.0e−2, 1.2e−2, 4.0e−3, 1.2e−3, 4.0e−4` at `r = 0.1, …, 0.001`. The median slope is 1.00.
  - #243 §5 observed the same order `r` for the weight.
- **Clean-context referee.** A separate Claude agent in this session, which had not seen the draft, returned ACCEPT WITH REVISIONS. It is the same provider and the same session, so this is not review evidence.
  - **Its 11 findings were all applied.** The two major ones:
    - Corollary WF is now stated with the pin-local `θ_p < 2`, which is automatic only on the elder side.
    - The claim that "the deterministic layer is complete" is withdrawn.
  - **Its independent checks:**
    - **sympy.** The chart determinant for `d = 3…6`. The identity `det D²f = k^{d−2}γ²r² det D²g`, with a fully symbolic `H`. On general symbolic pinned fields in `d = 3, 4`, `[r⁴]W_r = (∏λ_j)² a_M a_S/16` without using the chart.
    - **mpmath.** Non-polynomial pinned fields in `d = 3, 4, 5`. (WF) holds to `1e−49`, and every case meeting the hypotheses lies in the `Θ` range, including stress cases with `θ_p` up to 1.5. `Θ − 1` has slope 1.00. In 19 of the 26 cases with `θ_p ≥ 2`, the actual pin type is wrong.

### 4. Not claimed

- Any `d ≥ 3` probability or rate.
- Rejected-side pin typing.
- Uniformity as `λ₂ → 0`, `κ_• → 0` or `k → 0`.
- Explicit values of FL.1's constants.

**Review request.** An optional, bounded read of Lemma WF and Corollary WF. Please claim first.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_