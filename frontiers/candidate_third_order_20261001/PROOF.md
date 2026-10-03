# The candidate density to third order: `ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/11})`

Object: CL-CANDIDATE-THIRD-ORDER-20261001-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
Before submission, a clean-context same-family referee read the whole note (`REFEREE_1.md` in the project archive). It
found no major issue, and its five minor findings and eight nits are applied:
- (1.2) is restricted to jets with uniformly invertible covariance;
- the uniform nondegeneracy of the free jets is proved on all of `(0, r_0^*]`;
- the elder requirements of Remark 1 are corrected;
- the relation to Math- #216's computation is stated exactly;
- control T5 is described as implemented, and a `d = 3` case is added.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
zero organizational independence.
**Dependencies (unmerged, consumed):**
- Math- #191 (`frontiers/remainder_vanishing_20260930/PROOF.md`, v1.1 blob `441152df`): Lemma E, Steps 1–4, its
  dominating variable `T` and the good event; §2 (2.1)–(2.2); the admissible radius `r_0^*`.
- Math- #198 (`frontiers/remainder_rate_20260930/PROOF.md`, v1.1 blob `abfb98ae`): (3.1), the sign window, (W.4); (W.1)
  only through #207 Lemma L.
- Math- #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, v1.1 blob `f6df5a73`): §0 (the cusp objects), the
  candidate part of Theorem CU.4's definitions, Lemma CU.5's nondegeneracy of the free jets, §7 (Lemma L (7.1)–(7.2),
  the far identity, the decomposition of `B_{d,L}`, the integral (7.3)).

This note cannot be integrated before those three and must be rebound if any of them changes.
**Merged inputs:** [R], [P] with [E1]/[E2]/[REC], and [Z] (Z2)–(Z3). The numerical value of `c₂` is Math- #216's
(cited, not consumed; §5).

## 0. Statement

Setting and notation are those of [R] (`frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf`),
#191 §0, #198 §0 and #207 §0:
- fixed `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`;
- near pins `M = −ru/2`, `S = ru/2` with heights `b`, `b − kr³` and zero gradients;
- the pin vector `U_r` and target `v_r = (b − kr³/2, −kr², 0, 12k, 0, …, 0)` with density `π_r`, the pinned law
  `Q = Q_{r,b,k}`, the coupling `(F_r, F_0)` of [R] (R3)–(R4), and `P = 1 + |b| + k`;
- the scaled endpoint Hessians `K_M`, `K_S` of [R] §4, the filtered determinants `F_j`,
  `Z_r/r² = E_Q[F_d(K_M)F_{d−1}(K_S)]`, `A_r = 12π_r(v_r)Z_r/r²`, and the contact kernel
  `A_0 = 12π_0(v_0)z_0`, `z_0 = 36k²E[(det A_0)²1{A_0 < 0}]`, `A_0 = D_y²F_0(0)`;
- the candidate density `ν_cand(ℓ) = ∫_0^{r_0}∫_R∫_{S^{d−1}} r^{−2}A_r(b, ℓ/r³, u) dσ db dr + ν_cand^{far,r_0}(ℓ)` (#191
  (2.1); the far part as in #207 §7), `c = c_{d,L}` of [P] (15.2), and `B_{d,L}` of [Z] (Z3).

**Cusp objects (#207 §0).**
- The jets at `0` under the contact law at the zero-gap target `v_0(b, 0)`: `f₄ = ∂_u⁴f(0)`, `γ = ∇_Θ∂_u²f(0)`,
  `A = D_Θ²f(0)`, `Δ = det A` and `Y = (f₄/12)Δ − γᵀadj(A)γ/4`. `E_0[· | b]` is the expectation under that law.
- With `κ > 0`, the candidate and contact cusp kernels are
  `𝒜^{cand}(b, κ, u) = 12π_0(u; v_0(b, 0))E_0[(36κ²Δ² − Y²)1{A < 0, |Y| < 6κ|Δ|} | b]` and
  `𝒜^{con}(b, κ, u) = 12π_0(u; v_0(b, 0))E_0[36κ²Δ²1{A < 0} | b]`. So
  `𝒜^{cand} − 𝒜^{con} = −12π_0E_0[min(Y², 36κ²Δ²)1{A < 0} | b]`.
- `I^{cand} := ∫_{S^{d−1}}∫_R∫_0^∞(𝒜^{cand} − 𝒜^{con})(b, s^{−4}, u) ds db dσ(u)`, which equals
  `−12·(8/7)6^{1/4}∫∫π_0E_0[|Y|^{7/4}|Δ|^{1/4}1{A<0} | b] db dσ` (#207 (7.3)).

**The fold coefficient.** Lemma F below shows that at fixed `(b, k, u)`, `A_r = A_0 + r²A₂ + O(r³(1 + k^{−1}))`. The
coefficient `A₂(b, k, u)` is `C¹` in `k ∈ [0, ∞)`, and its value at `k = 0` is
`A₂(b, 0, u) = −12π_0(u; v_0(b, 0))E_0[Y²1{A < 0} | b]`. Define

    c₂ := (1/3) ∫_{S^{d−1}} ∫_R ∫_0^∞ [A₂(b, k, u) − A₂(b, 0, u)] k^{−4/3} dk db dσ(u).                     (0.1)

This is the Hadamard finite part at `k = 0` of `(1/3)∫∫∫A₂k^{−4/3}`. It is the coefficient that Math- #216 defines. Its
numerical values there, for the Gaussian kernel, are `0.22152441` in `d = 2` and `0.16123405` in `d = 3` (§5).

**Theorem T (the candidate density to third order).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{4/11}).                           (T.1)

The integral (0.1) converges absolutely.

**Corollary T′ (a rate for #207's (CU′.1)).**
`ν_cand(ℓ) − cℓ^{−1/3} − B_{d,L} − I^{cand}ℓ^{1/4} = O(ℓ^{1/3})`. This settles, for the candidate density, the open item
"a rate for the `o(ℓ^{1/4})`" of #207 §0 and of the concordance (§9 item 6).

**How it works.** Three scales meet.
- *Fold scale `r ≍ ℓ^{1/3}`.* Here `k ≍ 1`, and the kernel has the even expansion `A_r = A₀ + r²A₂ + …`. Integrating
  `A₂` in `r` produces `c₂ℓ^{1/3}`, but `∫A₂k^{−4/3}dk` diverges at `k = 0`, because `A₂(b, 0) ≠ 0`.
- *Cusp scale `r ≍ ℓ^{1/4}`.* Here `κ = k/r ≍ 1`, and #207's cusp kernels apply, with an explicit rate `O(r(1 + κ)²)`
  (Lemma C). They produce `I^{cand}ℓ^{1/4}`.
- *Overlap.* As `κ → ∞` the cusp loss `𝒜^{cand} − 𝒜^{con}` tends to `A₂(b, 0)` at rate `κ^{−1}` (Lemma O). The two
  scales therefore match: the divergent part of the fold integral is exactly the part of the cusp integral that the
  finite part removes.
- *Larger separations.* They need no elder decision: Lemma L of #207 bounds the gap dependence.

**What is not claimed.**
- No statement about the elder density `ν_eld` or the rejected density beyond #207. The `ℓ^{1/3}` term of `ν_eld` needs
  three things not supplied here (§5, Remark 1):
  - an elder version of Lemma C (a quantitative Proposition CU.3);
  - a bound `o(ℓ^{1/3})` for elder pairs at intermediate separations `ℓ^{1/4} ≪ r ≤ r₁`;
  - a far elder bound `o(ℓ^{1/3})`, which exists only in the unmerged candidates #187 and #188.
- No certified numerical value of `c₂`, `I^{cand}` or `B_{d,L}`.
- No sharpness of the exponent `4/11`. Formally the next term is of order `ℓ^{1/2}`.
- No uniformity in `d` or `L`; no finite-radius band.
- Nothing beyond the existential scope of [R], [Z], #191, #198 and #207.

## 1. Two Gaussian facts

**Lemma D (eigenvalue and determinant layers).** Let `G` be a random symmetric `m × m` matrix whose law has a density
bounded by `C_φ exp(−c_φ|G − μ|²)` on `Sym(m) ≅ R^{m(m+1)/2}`. For every `n ≥ 0` there is
`C = C(m, n, C_φ, c_φ)`, independent of `μ`, such that for `ε > 0`

    E[(1 + ‖G‖)^n 1{|λ_max(G)| < ε}] ≤ C(1 + |μ|)^{n′} ε,        E[(1 + ‖G‖)^n 1{|det G| < ε}] ≤ C(1 + |μ|)^{n′} ε,   n′ := n + m(m−1)/2.   (1.1)

*Proof.* Use eigenvalue coordinates `G = OΛOᵀ`, under which Lebesgue measure on `Sym(m)` is
`c_m|V(λ)| dλ dO`, with `V(λ) = ∏_{i<j}(λ_i − λ_j)` and `dO` the Haar measure (the Weyl integration formula; this is
[R] §5's Lebesgue eigenvalue-coordinate change, with the same Vandermonde factor).
- *First bound.* Integrate `λ_max` over `(−ε, ε)`. The remaining integrand `(1 + max|λ_i|)^n|V|C_φe^{−c_φ|Λ−OᵀμO|²}` has
  an integral over the other eigenvalues and `O` that is bounded by `C(1 + |μ|)^{n′}`, uniformly in the value of
  `λ_max`. The Vandermonde factor costs at most `(1 + max|λ_i|)^{m(m−1)/2}`, and the Gaussian bound absorbs it at the
  price of the power of `1 + |μ|`.
- *Second bound.* On `{|det G| < ε}`, let `i*` index an eigenvalue of least modulus and put
  `D := ∏_{j≠i*}|λ_j| > 0`. Then `|λ_{i*}| < ε/D`. Since `|λ_{i*}| ≤ |λ_j|`, each factor `|λ_{i*} − λ_j| ≤ 2|λ_j|`, so
  `|V(λ)| ≤ 2^{m−1}D|V′|`, where `V′` is the Vandermonde product of the other `m − 1` eigenvalues.
- Integrating `λ_{i*}` over an interval of length `2ε/D` against a density at most `C_φ` gives at most
  `2^m C_φ ε|V′|`. The factor `D` cancels.
- The remaining integral of `(1 + max|λ_j|)^n|V′|` against the Gaussian bound in the other eigenvalues is
  `≤ C(1 + |μ|)^{n′}`. Summing over the `m` choices of `i*` gives (1.1). ∎

(For `m = 1` both statements are the bounded density of a Gaussian variable.)

**Conditional moments of `T`.** Let `T := 1 + k + ‖F_r‖_{C⁹} + ‖F_0‖_{C⁹} + r^{−2}‖F_r − F_0‖_{C⁴}`. This is #191's
dominating variable with larger norm indices; [R] (R4) holds for every finite derivative order, so `‖T‖_p ≤ C_pP`.
Let `J₀` be a finite vector of derivatives of `F_r` at `0` whose covariance under `Q` is uniformly invertible for
`r ≤ r_0^*`. Any vector of free jets qualifies (§2, Step F1).
- Under the coupling (R3), `F_r`, `F_0` and `(F_r − F_0)/r²` are affine images of one Gaussian field `F`. Their
  coefficients are bounded uniformly in `r ≤ r_0^{[R]}` by (R2).
- Conditionally on `J₀`, `F` is Gaussian. Because `Cov_Q(J₀)` is uniformly invertible, the regression coefficients
  are bounded uniformly in `r`, so the conditional mean has `C^q` norms `≤ C(P + |J₀|)`. The conditional covariance is at
  most `Cov F`, so the conditional `C^q`-norm moments of the centred part are dominated by those of `F` (Anderson's
  inequality).
- Hence

      E[T^p | J₀] ≤ C_p (P + |J₀|)^p.                                                              (1.2)

  The hypothesis is needed. For a pinned jet such as `∂_u²F_r(0)`, whose `Q`-variance is `O(r⁴)`, conditioning on an
  `O(1)` value forces `f₄ ≍ r^{−2}`.

## 2. The fold expansion

**Lemma F.** There are `C, c, N` and a function `A₂(b, k, u)` such that for `0 < r ≤ min(r_0^*, 1/2)`, `k > 0`,
`b ∈ R` and `u ∈ S^{d−1}`

    |A_r(b, k, u) − A_0(b, k, u) − r² A₂(b, k, u)| ≤ C r³ (1 + k^{−1}) P^N e^{−c(b² + k²)}.                     (F.1)

Moreover, `A₂(b, ·, u)` extends to a `C¹` function on `[0, ∞)` with

    |A₂(b, k, u)| + |∂_kA₂(b, k, u)| ≤ C P^N e^{−c(b² + k²)},        A₂(b, 0, u) = −12π_0(u; v_0(b, 0)) E_0[Y² 1{A < 0} | b].   (F.2)

*Proof.* Fix `N₀ = 9`. Write `f = F_r` and `A := D_y²f(0)`.

*Step F1 (free jets and the product polynomial).* Let `J` be the vector of all partial derivatives of `f` at `0` of
order `≤ N₀`, in the frame `(u, Θ)`.
- The *pinned* jets are `f(0)`, `∂_uf(0)`, `∂_u²f(0)`, `∂_u³f(0)`, `∇_Θf(0)` and `∇_Θ∂_uf(0)`. The others are *free*;
  write `J′` for them. `A` and `f₄` are free.
- *The free jets are uniformly nondegenerate under `Q`.* For each `r ∈ (0, r_0^*]`, `(J′, U_r)` is an invertible linear
  image of distinct derivative functionals at the three distinct sites `0` and `±ru/2`. These are linearly independent,
  by [P] §2: "Any finite list of distinct derivative evaluation functionals at distinct sites is linearly independent."
  At `r = 0`, `(J′, U_0)` is a list of distinct jets at one point, again independent. The Gram matrix of `(J′, U_r)` is
  continuous on the compact set `[0, r_0^*] × {frames}`, so it is uniformly invertible there. Hence `Cov_Q(J′)`, the
  Schur complement, is uniformly invertible. #207 Lemma CU.5 makes the same argument for `r ≤ r₁`.
- Each pin row is a centred difference rule. Taylor's formula with integral remainder writes it as the corresponding
  pinned jet plus a polynomial in `r` and the higher jets, plus an error `≤ Cr^{N₀−3}T`. Here `T` (§1) controls the
  `C⁹` norms. For example
  `(f_x(S) − f_x(M))/r = ∂_u²f(0) + (r²/24)∂_u⁴f(0) + … `, the series that #191 Step 1 truncates at second order.
- Under `Q` the rows equal their targets. Hence each pinned jet equals a polynomial in `(J′, r, b, k)` up to
  `O(r^{N₀−3}T)`. The `1/r` and `1/r²` of the rows are absorbed because the rules are centred.
- Expanding the entries of `K_M`, `K_S` at `x = ∓r/2` by Taylor's formula to the same order and substituting gives, for
  `r ≤ 1`, a polynomial `Φ(J′; r, k)` with

      −det K_M det K_S = Φ(J′; r, k) + ϱ,        |ϱ| ≤ C r⁴ T^{n₀}.                                       (2.1)

  The entry `α_i = f_xx(x_i)/r` has an explicit `1/r`. It is a polynomial once `∂_u²f(0)` is replaced by its pin
  expansion `−(r²/24)f₄ − …`. This is the mechanism of #191 (1.1).
- Write `Φ = Φ₀ + rΦ₁ + r²Φ₂ + r³Φ₃(J′; r, k)`, with `|Φ₃| ≤ C(1 + k)²(1 + |J′|)^{n₀}` for `r ≤ 1`.
- By #191 Lemma E, Steps 1–3, and #198 (3.1),
  `det K_M = −6kΔ_r + rY + O(r²)` and `det K_S = +6kΔ_r + rY + O(r²)`, with the *same* `Y`. Here
  `Δ_r = det A` and `Y = (f₄/12)Δ_r + 3k tr(adj(A)B) − γᵀadj(A)γ/4`. #191 states this with its coupled `A_0`; with
  `A = D_y²F_r(0)` the same expansions hold, since #191 replaced `A` by `A_0` only through `‖A − A_0‖ ≤ r²T`. Hence

      Φ₀ = 36k²Δ_r²,        Φ₁ = −[(−6kΔ_r)Y + Y(6kΔ_r)] = 0,        Φ₂|_{k=0} = −Y²|_{k=0}.                 (2.2)

  The last identity holds because at `k = 0` both determinants are `rY + O(r²)`.
- (2.2) is an identity of polynomials in `J′`, not only pathwise. Apply (2.1) and the expansions above to the pinned
  polynomial fields of degree `≤ N₀ − 1` with arbitrary free jets: for these `ϱ = 0` and `T < ∞`, so the coefficients of
  `r⁰`, `r¹` and (at `k = 0`) `r²` in `Φ − 36k²Δ_r²` and `Φ + r²Y²` must vanish identically. Control T5 checks (2.2)
  exactly on such fields in `d = 2` and `d = 3`.

*Step F2 (the typed indicator and its layers).* Let `υ := C₁rT(1 + T/k)` and
`G := {λ_max(A) ≤ −υ} ∩ {k ≥ C₁rT}`. This is #191 Step 4's good event (#191's `u`) with `A` in place of `A_0`. Its
proof uses only `‖A_i − A‖ ≤ (r/2)‖F_r‖_{C³} ≤ rT` and `‖β_i‖ ≤ CT`, which hold for `A`.
- *On `G`.* `K_M`, `K_S` have indices `d`, `d − 1` and `A < 0`. So `F_d(K_M)F_{d−1}(K_S) = −det K_M det K_S`, and by
  (2.1) this equals `Φ1{A<0} + ϱ`.
- *On `{λ_max(A) ≥ rT}`.* `λ_max(A_M) ≥ rT − (r/2)T > 0`, so `F_d(K_M) = 0`. Also `1{A<0} = 0`.
- *On the rest of `G^c`.* This set lies in `{|λ_max(A)| < υ} ∪ {k < C₁rT}`. There, #191 Step 4's three cases bound
  both `F_d(K_M)F_{d−1}(K_S)` and `|Φ|1{A<0}` (the latter through (2.1)) by `C r²(k + T)²T^{N₂}`.

Hence

    |E_Q[F_d(K_M)F_{d−1}(K_S)] − E_Q[Φ 1{A<0}]| ≤ C r⁴P^N + E[g(T)(1{k < C₁rT} + 1{|λ_max(A)| < υ})],   g(t) := Cr²(k + t)²t^{N₂}.

Bound the two layer terms separately.
- *First term.* `E[g(T)1{T > k/(C₁r)}] ≤ (C₁r/k)E[g(T)T] ≤ Cr³k^{−1}P^N`.
- *Second term: dyadic split.* Since `T ≥ 1` and `υ` increases with `T`, split by `T ∈ [2^j, 2^{j+1})`, with
  `υ_j := C₁r2^{j+1}(1 + 2^{j+1}/k)`:

      E[g(T)1{|λ_max(A)| < υ}] ≤ Σ_{j≥0} g(2^{j+1}) E[1{|λ_max(A)| < υ_j} P(T ≥ 2^j | A)]
                               ≤ Σ_{j≥0} g(2^{j+1}) C_p 2^{−jp} E[(P + ‖A‖)^p 1{|λ_max(A)| < υ_j}].

  The second line uses (1.2) with `J₀ = A`.
- *The law of `A`.* Under `Q`, `A` is a Gaussian vector with mean `O(P)` and uniformly nondegenerate covariance
  (Step F1). This also makes (1.2) applicable with `J₀ = A`.
- So Lemma D gives `E[(P + ‖A‖)^p1{|λ_max(A)| < υ_j}] ≤ CP^{2p+m(m−1)/2}υ_j`. Taking `p > N₂ + 4`, the sum is
  `≤ Cr³(1 + k^{−1})P^N`.

Hence

    E_Q[F_d(K_M)F_{d−1}(K_S)] = E_Q[Φ(J′; r, k)1{A<0}] + O(r³(1 + k^{−1})P^N).                                (2.3)

*Step F3 (smoothness of the pinned law in `r`).* Under `Q`, `J′` is Gaussian with mean `μ_r` and covariance `Γ_r`, both
built from `Cov(J′, U_r)`, `Cov(U_r)` and `v_r`.
- The rows of `U_r` are centred, so they are even functionals of `r`. The covariances are therefore smooth even
  functions of `r`, and `Γ_r` is uniformly nondegenerate (Step F1).
- The target is `v_r = v_0 + r²(0, −k, 0, …) + r³(−k/2, 0, …)`. Hence
  `μ_r = μ_0 + r²μ_2 + r³μ_3 + O(r⁴P)` with `|μ_3| ≤ Ck`, and `Γ_r = Γ_0 + r²Γ_2 + O(r⁴)`.
- For `g = Ψ(J′)1{A<0}` with `Ψ` a polynomial, `E_{N(μ,Γ)}[g]` is a smooth function of `(μ, Γ)`: differentiate the
  Gaussian density under the integral. Its derivatives are bounded by `E[|g|(1 + |J′|)^n]`-type moments.
- So `E_Q[Φ₀1{A<0}] = 36k²(e_0 + r²e_2 + O(r³(1 + k)P^N))` and `E_Q[Φ₂1{A<0}] = E_0[Φ₂1{A<0}] + O(r²P^N)`. The
  `r³`-term contributes `O(r³(1 + k)²P^N)`. Here `e_0 = E_0[Δ²1{A<0} | v_0(b, k)]` and `E_0` is the law at `r = 0`, which
  is the contact law at `v_0(b, k)`, the law of the jets of `F_0`.
- Likewise `π_r(v_r) = π_0(v_0) + r²π_2 + O(r³(1 + k)P^Ne^{−c(b²+k²)})`. The density of `U_r` is smooth in `(r², v)`
  with uniformly nondegenerate covariance, as in the proof of [R] (R5).
- Multiplying, with (2.3) and `A_0 = 12π_0(v_0)·36k²e_0`, gives (F.1) with

      A₂ := 12[π_2·36k²e_0 + π_0(v_0)(36k²e_2 + E_0[Φ₂1{A<0} | v_0(b, k)])].                                     (2.4)

*Properties (F.2).*
- Every ingredient of (2.4) is a polynomial in `k`, or a Gaussian expectation whose target is affine in `k`, times
  `π_0(v_0(b, k)) ≤ Ce^{−c(b²+k²)}`. This gives the bounds and the `C¹` extension to `k = 0`.
- At `k = 0` the first two terms vanish, because of the factor `k²`. By (2.2), the third is
  `−12π_0(v_0(b, 0))E_0[Y²1{A<0} | v_0(b, 0)]`.
- At `r = 0` the free jets have the contact law. So `Y` is #207's `Y` and `E_0[· | v_0(b, 0)]` is #207's `E_0[· | b]`. ∎

(*The surrogate.* Replace the true typed indicator by `1{A < 0}`. The surrogate kernel `12π_r(v_r)E_Q[Φ1{A<0}]` is
smooth in `r` at every `k ≥ 0`, with no boundary layer, and by Step F3 its `r²`-coefficient is `A₂`. Step F2 shows that
the replacement changes `A_r` by `O(r³(1 + k^{−1}))`; this is the boundary layer of the typed region near `det A = 0`.

Math- #216 computes a numerical approximation of this surrogate in three steps:
- it truncates the jets at order `N = 12, 10, 8` (`d = 1, 2, 3`);
- it conditions them on the correspondingly truncated pin rows, which differ from `Q` by `O(r^{N−3})`-type terms;
- it extracts the `r²`-coefficient by least squares on `(1, r², r³, r⁴)` over five separations, then integrates by
  Gauss–Legendre quadrature.

For `N ≥ 6` the exact `r²`-coefficient of the truncated surrogate equals `A₂`, so #216's values are numerical
approximations of (0.1), not exact evaluations.)

## 3. The cusp kernel with a rate

**Lemma C.** There are `C, c, N` such that for `0 < r ≤ min(r_0^*, 1/2)`, `b ∈ R`, `u ∈ S^{d−1}` and `κ > 0` with
`k := κr ≤ 1`

    |r^{−2}(A_r − A_0)(b, κr, u) − (𝒜^{cand} − 𝒜^{con})(b, κ, u)| ≤ C r (1 + κ)² (1 + |b|)^N e^{−cb²}.               (C.1)

*Proof.* Work on the coupling space with `T` as in §1 and `Δ := det A_0`, where `A_0 = D_y²F_0(0)`. As in [R] and
#191, `A_0` denotes both this matrix and the contact kernel; the meaning is clear from context. With this `T`,
`‖A_i − A_0‖ ≤ (r/2)‖F_r‖_{C³} + ‖F_r − F_0‖_{C²} ≤ (r/2 + r²)T ≤ rT` for `r ≤ 1/2`, which is [R] (R9).

*Step C1 (pathwise comparison).* By #198 (3.1),
`det K_M = r(Y − 6κΔ) + R_M` and `det K_S = r(Y + 6κΔ) + R_S`, with `|R_i| ≤ Cr²(1 + k)T^{N₁}` and
`Y = (f₄/12)Δ + 3k tr(adj(A_0)B) − q`. Here `B = ∂_xD_y²F_r(0)`, `q = γᵀadj(A_0)γ/4`, and `f₄`, `γ = ∇_y∂_x²F_r(0)` are
jets of `F_r` (#191 (1.5)). Put `m_i := det K_i/r`, `η := Cr(1 + k)T^{N₁} ≥ |R_i|/r`, and

    w_κ(A, Y) := (36κ²(det A)² − Y²) 1{A < 0, |Y| < 6κ|det A|} = (36κ²(det A)² − Y²)_+ 1{A < 0}.

Then `r^{−2}F_d(K_M)F_{d−1}(K_S) = |m_Mm_S|1{typed}`. There are three cases.
- *Case 1: `λ_max(A_0) < −rT`.* Since `‖A_i − A_0‖ ≤ rT`, `A_M, A_S < 0`. By Haynsworth's inertia additivity
  (#191 Step 4), `index K_i = m + 1{s·det K_i < 0}`, where `s := (−1)^m = sign Δ`.
  - So `typed ⟺ s m_M < 0 < s m_S`. Because `sΔ = |Δ|`, the limit indicator is
    `1{|Y| < 6κ|Δ|} ⟺ s(Y − 6κΔ) < 0 < s(Y + 6κΔ)`.
  - *If both hold:* `|m_Mm_S − (Y − 6κΔ)(Y + 6κΔ)| ≤ 2η(|Y| + 6κ|Δ|) + η² ≤ 24ηκ|Δ| + η²`.
  - *If exactly one holds:* for some `i`, the factor `Y ∓ 6κΔ` and `m_i` differ in sign or one of them vanishes. Hence
    `|Y ∓ 6κΔ| ≤ |R_i|/r ≤ η`, and the other factor is `≤ 12κ|Δ| + η` in modulus. Both weights are then
    `≤ 2η(12κ|Δ| + 3η)`.
- *Case 2: `λ_max(A_0) > rT`.* Then `λ_max(A_M) > 0`, so `F_d(K_M) = 0`. Also `1{A_0 < 0} = 0`, so both weights vanish.
- *Case 3: `|λ_max(A_0)| ≤ rT`.* Then `|Δ| ≤ rT·T^{m−1}`, so `w_κ ≤ 36κ²r²T^{2m}`. If the pair is typed, the sign
  window of #198 §3 gives `|m_i| ≤ 12κ|Δ| + 2η`, so `|m_Mm_S| ≤ C(κr + η)²T^{2m}`.

In all cases, since `|Δ| ≤ T^m` and `κr = k ≤ 1`,

    |r^{−2}F_d(K_M)F_{d−1}(K_S) − w_κ(A_0, Y)| ≤ C r (1 + κ) T^{N}.                                             (C.2)

*Step C2 (to the contact jets).* Let `Y_0 := (f₄^{(0)}/12)Δ − (γ^{(0)})ᵀadj(A_0)γ^{(0)}/4`, built from the jets of
`F_0`. Then `|Y − Y_0| ≤ 3κr|tr(adj(A_0)B)| + Cr²T^N`: the `C⁴`-jets of `F_r` and `F_0` differ by `≤ r²T`.
- `w_κ(A, ·)` is Lipschitz with constant `12κ|det A|`. If both values are positive,
  `|Y² − Y′²| ≤ (|Y| + |Y′|)|Y − Y′| ≤ 12κ|Δ||Y − Y′|`. If only `w(A, Y) > 0`, then
  `w(A, Y) ≤ (6κ|Δ| − |Y|)·12κ|Δ| ≤ 12κ|Δ||Y − Y′|`.
- Hence `|w_κ(A_0, Y) − w_κ(A_0, Y_0)| ≤ Cκ(κr + r²)T^N`.
- `(A_0, Y_0)` are jets of `F_0`, whose law is the contact law at `v_0(b, k)`. With (C.2) and `E[T^N] ≤ CP^N`,

      |r^{−2}Z_r/r² − E_0[w_κ(A, Y) | v_0(b, k)]| ≤ C r(1 + κ)²P^N.

*Step C3 (densities and the target).* By (R5), `|π_r(v_r) − π_0(v_0(b, k))| ≤ Cr²P²e^{−c(b²+k²)}`, and
`E_0[w_κ] ≤ C(1 + κ)²P^N`. Also `r^{−2}A_0(b, κr, u) = 12π_0(v_0(b, k))36κ²E_0[Δ²1{A<0} | v_0(b, k)]` exactly. Hence

    r^{−2}(A_r − A_0)(b, κr, u) = −12π_0(v_0(b, k))E_0[min(Y², 36κ²Δ²)1{A<0} | v_0(b, k)] + O(r(1 + κ)²P^Ne^{−c(b²+k²)}).

It remains to move the target from `v_0(b, k)` to `v_0(b, 0)`, which uses the parity factorization of [P] §15.
- *Parity.* The covariance of the field is even, so jets of even and odd order at `0` are uncorrelated, hence
  independent. The pin rows split the same way: `f`, `∂_u²f`, `∇_Θ∂_uf` are even; `∂_uf`, `∂_u³f`, `∇_Θf` are odd.
  The target's even part is `(b, 0, 0)`, and its odd part is `(0, 12k, 0)`.
- *Even jets.* The conditional law of the even jets `(A, f₄)` does not depend on `k`.
- *Odd jets.* The odd jets have a `k`-independent covariance and a mean shift `12k·w` with `w` fixed. In particular
  `γ = γ̄ + 12k w_γ`, with `γ̄` the `k = 0` version.
- *Density.* `π_0(v_0(b, k)) = p_even(b, 0, 0)p_odd(0, 12k, 0)`, and the second factor is
  `p_odd(0, 0, 0)(1 + O(k²))`.
- *The integrand.* `|min(Y², c) − min(Ȳ², c)| ≤ (|Y| + |Ȳ|)|Y − Ȳ|` for every `c ≥ 0`. The shift of `γ` moves `Y` by
  `≤ Ck(|γ̄| + k)‖A‖^{m−1}`, so the expectation moves by `O(kP^N)`, with no growth in `κ`.
- Hence the two targets differ by `O(k(1 + |b|)^Ne^{−cb²}) = O(κr(…))`, which proves (C.1). ∎

(The `κ²` in (C.1) comes only from the `3k tr(adj(A_0)B)` term in `Y`. That term is odd in the odd jets. A parity
argument would reduce its expected contribution to `O(k²)`, and (C.1) to `O(r(1 + κ))`. This would improve the
exponent `4/11` in (T.1) to `3/7`; it is not needed here.)

## 4. The overlap and the proof of Theorem T

**Lemma O (overlap).** For `κ ≥ 1`,

    0 ≤ (𝒜^{cand} − 𝒜^{con})(b, κ, u) − A₂(b, 0, u) ≤ C κ^{−1} (1 + |b|)^N e^{−cb²}.                                  (O.1)

*Proof.*
- By (F.2) and the definitions, the difference is `12π_0E_0[(Y² − 36κ²Δ²)_+1{A<0} | b] ≥ 0`. It is at most
  `12π_0E_0[Y²1{|Δ| < |Y|/(6κ)} | b]`.
- *Dyadic split.* Split by `|Y| ∈ [2^{j−1}, 2^j)` for `j ≥ 1`, and `|Y| < 1` for `j = 0`. Given `A`, the jets `(f₄, γ)`
  are Gaussian with mean affine in `(A, b)` and bounded covariance. `Y` is a polynomial in them with coefficients
  polynomial in `A`, so `P(|Y| ≥ t | A) ≤ C_p t^{−p}(1 + |b| + ‖A‖)^{n_p}`.
- Under `E_0[· | b]`, `A` is a nondegenerate Gaussian symmetric matrix with mean `O(1 + |b|)`. By Lemma D,

      E_0[Y²1{|Δ| < |Y|/(6κ)}] ≤ Σ_{j≥0} 4^j E_0[1{|det A| < 2^j/(6κ)} min(1, C_p2^{−(j−1)p}(1 + |b| + ‖A‖)^{n_p})]
                               ≤ Σ_j 4^j C_p 2^{−(j−1)p}(1 + |b|)^{n_p+m(m−1)/2} · 2^j/κ ≤ Cκ^{−1}(1 + |b|)^{n_p+m(m−1)/2}.

  Take `p > 3`; the factor `π_0 ≤ Ce^{−cb²}` completes the proof. ∎

(The mechanism, concentration on `|Δ| ≲ |Y|/κ` with mass `≍ 1/κ`, is the one #207 Remark 1 records for the rejected
cusp mass.)

**Proof of Theorem T.**

*Setup.* Put `ρ_f := ℓ^{1/4 + 1/44}` and `ρ_c := ℓ^{1/4 − 1/36}`. Fix `r_0 ∈ (0, r_0^*]` and take `ℓ` so small that
`ρ_c < r_0` and `ℓρ_f^{−3} ≤ 1`. By #191 (2.1) and #207 §7's decomposition of `B_{d,L}`,

    ν_cand(ℓ) − cℓ^{−1/3} − B_{d,L} = F + K + J₂ + J₃ + J₄ + J₅,

with the integrands taken at `(b, ℓ/r³, u)` unless stated otherwise, and inner integrals `db dσ(u)`:
- `F := ∫_0^{ρ_f}∫∫ r^{−2}(A_r − A_0)`;
- `K := ∫_{ρ_f}^{ρ_c}∫∫ r^{−2}(A_r − A_0)`;
- `J₂ := −∫_0^{ρ_c}∫∫ r^{−2}A_r(b, 0, u)`;
- `J₃ := ∫_{ρ_c}^{r_0}∫∫ r^{−2}[A_r(b, ℓ/r³, u) − A_r(b, 0, u)]`;
- `J₄ := −∫_{ρ_c}^∞∫∫ r^{−2}A_0`;
- `J₅ := ∫_{dist(0,y)≥r_0}∫(Ψ_ℓ^{cand} − Ψ_0) db dy`.

Here #207 §7 records `cℓ^{−1/3} = ∫_0^∞∫∫r^{−2}A_0` and
`B_{d,L} = ∫_0^{r_0}∫∫r^{−2}A_r(b, 0, u) + ∫_{dist≥r_0}∫Ψ_0`. The far candidate density is `∫_{dist≥r_0}∫Ψ_ℓ^{cand}`.

*`F`: the fold region.* Here `k = ℓ/r³ ≥ r`.
- By (F.1), `r^{−2}(A_r − A_0) = A₂(b, ℓ/r³, u) + E_F` with `|E_F| ≤ C(r + r/k)(1 + |b|)^Ne^{−cb²}`, using
  `P^Ne^{−ck²} ≤ C(1 + |b|)^N`. Here `r/k = r⁴/ℓ`.
- So `|∫E_F| ≤ C(ρ_f² + ρ_f⁵/ℓ)`.
- With `k = ℓ/r³`, `dr = −(1/3)ℓ^{1/3}k^{−4/3}dk` and `K₀ := ℓ/ρ_f³`, we have
  `ℓ^{1/3}K₀^{−1/3} = ρ_f` and

      ∫_0^{ρ_f} A₂(b, ℓ/r³, u) dr = (ℓ^{1/3}/3)∫_{K₀}^∞ A₂ k^{−4/3} dk
                                 = (ℓ^{1/3}/3)∫_0^∞ (A₂(k) − A₂(0)) k^{−4/3} dk + ρ_f A₂(b, 0, u) − (ℓ^{1/3}/3)∫_0^{K₀}(A₂(k) − A₂(0))k^{−4/3}dk.

- The integrals converge absolutely by (F.2). The last term is `O(ℓ^{1/3}K₀^{2/3}) = O(ℓρ_f^{−2})`, uniformly with the
  factor `(1 + |b|)^Ne^{−cb²}`.
- So `F = c₂ℓ^{1/3} + ρ_f∫∫A₂(b, 0, u) + O(ρ_f² + ρ_f⁵/ℓ + ℓρ_f^{−2})`. The convergence of (0.1) is part of this.

*`K`: the cusp region.* Here `k = ℓ/r³ ≤ ℓρ_f^{−3} ≤ 1`.
- By (C.1) with `κ = ℓ/r⁴`, `r^{−2}(A_r − A_0) = (𝒜^{cand} − 𝒜^{con})(b, ℓ/r⁴, u) + E_K`, where
  `∫_{ρ_f}^{ρ_c}|E_K| ≤ C∫_{ρ_f}^{ρ_c} r(1 + ℓr^{−4})² dr ≤ C(ρ_c² + ℓρ_f^{−2} + ℓ²ρ_f^{−6})`.
- With `r = sℓ^{1/4}`, the main term is `ℓ^{1/4}∫_σ^S(𝒜^{cand} − 𝒜^{con})(b, s^{−4}, u) ds`, where
  `σ = ρ_fℓ^{−1/4} = ℓ^{1/44}` and `S = ρ_cℓ^{−1/4} = ℓ^{−1/36}`.
- *Upper tail.* `|𝒜^{cand} − 𝒜^{con}| ≤ 12π_0·36κ²E_0[Δ²] ≤ Cs^{−8}(…)`, so `∫_S^∞ = O(S^{−7})`.
- *Lower end.* By Lemma O, `∫_0^σ(𝒜^{cand} − 𝒜^{con}) ds = σA₂(b, 0, u) + O(σ⁵)`.
- So `K = ℓ^{1/4}·(the I^{cand} integrand) − ρ_f∫∫A₂(b, 0, u) + O(ℓ^{1/4}σ⁵ + ℓ^{1/4}S^{−7} + ρ_c² + ℓρ_f^{−2} + ℓ²ρ_f^{−6})`.

*The overlap cancels.* The terms `±ρ_f∫∫A₂(b, 0, u)` of `F` and `K` cancel. Note `ℓ^{1/4}σ⁵ = ρ_f⁵/ℓ` and
`ℓ^{1/4}S^{−7} = ℓ²ρ_c^{−7}`.

*`J₂`–`J₅`.*
- `|J₂| ≤ Cρ_c³` by #198 (W.4).
- `|J₃| ≤ C∫_{ρ_c}^∞(ℓ²r^{−8} + ℓr^{−3}) dr ≤ C(ℓ²ρ_c^{−7} + ℓρ_c^{−2})` by #207 (7.1); here `k ≤ 1`.
- `0 ≤ −J₄ ≤ Cℓ²ρ_c^{−7}`, since `A_0 ≤ k²H`.
- `|J₅| ≤ C_{r_0}ℓ` by #207 (7.2).

*Exponents.* With `ρ_f = ℓ^{1/4+1/44}` and `ρ_c = ℓ^{1/4−1/36}`:

| Term | Exponent |
|---|---|
| `ρ_f²` | `6/11` |
| `ρ_f⁵/ℓ` | `4/11` |
| `ℓρ_f^{−2}` | `5/11` |
| `ℓ²ρ_f^{−6}` | `4/11` |
| `ρ_c²` | `4/9` |
| `ρ_c³` | `2/3` |
| `ℓ²ρ_c^{−7}` | `4/9` |
| `ℓρ_c^{−2}` | `5/9` |
| `ℓ` | `1` |

The least is `4/11`. So
`ν_cand − cℓ^{−1/3} − B_{d,L} = I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{4/11})`, which is (T.1). The exponents are checked
exactly by checker T1. ∎

## 5. Remarks

1. **The elder density.** For `ν_eld` the same decomposition needs the following.
   - *An elder Lemma C.* This is a quantitative Proposition CU.3 of #207. The decision's height margin is
     `κ·min(1, 12||φ| − 1/3|)`, linear in the distance from the window's edge.
     - Suppose the elder cusp error is `C r^θ(1 + κ)^N(1 + |b|)^Ne^{−cb²}`. In this ledger,
       `θ > max(2/5, (N + 1)/4)` suffices. The fold end needs `θ > (N + 1)/4`, given `ρ_f = ℓ^{1/4+a}` with
       `a > 1/60`. The top end needs `θ > 2/5`, given `ρ_c = ℓ^{1/4−b}` with `b > 1/84`.
     - Lemma C's candidate rate, `θ = 1` with `N = 2`, meets this.
     - The bare condition `θ > 1/3` would need a sharper treatment of the `S^{−7}` tails (referee M-3).
   - *The fold-region elder deficit.* `A_r − A_r^{eld} ≤ Cr³/k` ([C7-K] (K2)) contributes `O(ρ_f⁵/ℓ)`, like the boundary
     layer in `F`. This input is available.
   - *Intermediate separations.* The elder density from `ρ_c ≤ r ≤ r₁` must be `o(ℓ^{1/3})`. On file, #198's Lemma B
     gives `O(ℓ^{1/3}ρ^{−1})` and #207's Lemma CU.5 route gives `o(ℓ^{1/4})`; neither suffices.
   - *The far part.* `ν_eld^{far,r₁} = o(ℓ^{1/3})` is needed. #198's Lemma F′ (`O(ℓ^{1/3})`) does not suffice. The
     unmerged candidates Math- #187 (`O(ℓ^{2/3})`) and #188 (`O(ℓ^N)`) would.

   The formal value of the elder `ℓ^{1/3}` coefficient is the same `c₂` (Math- #216).
2. **The value of `c₂`.** By the parenthetical remark after Lemma F, Math- #216's `c2_check.py` computes a numerical
   approximation of (0.1). It uses truncated jets and pin rows, a least-squares fit in `r` over five separations, and
   Gauss–Legendre quadrature. The exact `r²`-coefficient of its truncated surrogate is `A₂`.
   - For the Gaussian kernel `e^{−|z|²/2}` (the SIDE24 covariance up to factors `1 + O(e^{−L²/8})`):
     `c₂ = 0.22152441` (`d = 2`), `0.16123405` (`d = 3`); `c₂/c = 3.017759`, `3.859496`.
   - These are numerical values, stable to `≤ 7·10⁻¹⁰` under the variations of #216 §2.4; they are not certified.
   - With #207's `I^{cand}` (`−0.1772744` in `d = 2`; `−0.1394041` in `d = 3`; exploration), the SIDE24 candidate
     density is `ν_cand ≈ 0.0417759ℓ^{−1/3} + B_{3,24} − 0.1394041ℓ^{1/4} + 0.1612340ℓ^{1/3}`. The value
     `B_{3,24} ≈ 10.21` comes from Math- #211 (exploration).
3. **Monte Carlo.** Math- #216 §3 compares the full-field Monte Carlo with the *adjacent*-pair density, not with
   `ν_cand`. Formally the two have the same `ℓ^{−1/3}`, `ℓ^{1/4}` and `ℓ^{1/3}` coefficients, but adjacent pairs have no
   `B_{d,L}` term; nothing on file proves the adjacent-pair expansion. Theorem T is the Kac–Rice statement; the Monte
   Carlo is exploration.
4. **`d = 1`.** In `d = 1` the analogous structure is Math- #214's Proposition 2.2. There, part (c) is the fold
   coefficient `B₂^{(1)}`, part (d) is the cusp, and the finite part is `B₂^{(2)}`. Its proof is self-contained (Rice
   formula on the circle).
5. **What Lemma C adds to #207.** #207's CU.4 is a limit at fixed `κ` with dominated convergence. Lemma C gives the rate
   `O(r(1 + κ)²)` uniformly for `κr ≤ 1`, for the candidate kernel. Only the candidate kernel is treated: the
   elder mark needs Proposition CU.3, whose margins are not quantified in #207.

## 6. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | (R2)–(R5), (R9), §4 scaled Hessians, Lemma R3.2, §5 eigenvalue coordinates — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §2 finite-jet rank, §4 regression, §§9–10 as [E2], §15 parity factorization and (15.2) — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | reading rule |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z2)–(Z3): `Ψ_0`, `B_{d,L}` — consumed |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (unmerged; v1.1 blob `441152df`) | Lemma E Steps 1–4, `T`, §2 (2.1), `r_0^*` — **consumed, unmerged** |
| #198 | `frontiers/remainder_rate_20260930/PROOF.md` (unmerged; v1.1 blob `abfb98ae`) | (3.1), the sign window, (W.4) — **consumed, unmerged**; (W.1) only through #207 Lemma L |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (unmerged; v1.1 blob `f6df5a73`) | §0 cusp objects; Lemma CU.5's nondegeneracy of free jets; §7 Lemma L (7.1)–(7.2), the far identity, the decomposition of `B_{d,L}`, (7.3) — **consumed, unmerged** |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | (K2), in Remark 1 only — cited |
| #216 | `frontiers/third_order_coefficient_20261001/` (unmerged) | numerical values of `c₂` — cited only |
| #214 | `frontiers/d1_third_order_law_20261001/PROOF.md` (unmerged) | the `d = 1` analogue — cited only |
| #187, #188 | `frontiers/far_elder_rate_20260930/PROOF.md`, `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | far elder bounds, in Remark 1 only — cited only |
| #211 | `frontiers/equal_height_mass_value_20261001/` (unmerged) | `B_{3,24} ≈ 10.21`, in Remark 2 only — cited only |

## 7. Exact controls (`thmT_check.py`; stdlib; exact rationals; byte-identical under `-O`)

- **T1** the exponent ledger of §4 with `ρ_f = ℓ^{1/4+1/44}`, `ρ_c = ℓ^{1/4−1/36}`: every exponent `≥ 4/11`, with equality
  exactly for `ρ_f⁵/ℓ` and `ℓ²ρ_f^{−6}`, and `4/11 > 1/3`; the hypotheses `ρ_f < ℓ^{1/4} < ρ_c` and `ℓρ_f^{−3} ≤ 1`.
- **T2** the pathwise case analysis of Step C1 on random rational data: the two weights, the case bounds
  `24ηκ|Δ| + η²` and `2η(12κ|Δ| + 3η)`, and Case 3's sign-window bound.
- **T3** the Lipschitz bound of Step C2 (constant `12κ|Δ|`) and the identity
  `(36κ²Δ² − Y²)_+ − 36κ²Δ² = −min(Y², 36κ²Δ²)`.
- **T4** Lemma D's Vandermonde inequality `∏_{j≠i*}|λ_{i*} − λ_j| ≤ 2^{m−1}∏_{j≠i*}|λ_j|` for random rational spectra,
  `m = 1…5`.
- **T5** the product structure (2.2) on exactly pinned polynomial fields in `d = 2` and `d = 3`.
  - Polynomial fields of degree 7 with random rational free jets are used.
  - The pinned jets are solved from the pin rows symbolically, as exact polynomials in `r`.
  - `det K_i = det H_i/r` is computed exactly as a polynomial in `r`, at `k = 0` and at random rational `k > 0`.
  - The constant terms are `∓6kΔ`, and `det K_M`, `det K_S` share the `r¹` coefficient
    `Y = (f₄/12)Δ + 3k tr(adj(A)B) − γᵀadj(A)γ/4`.
  - The product has constant term `−36k²Δ²` and no `r¹` term. At `k = 0` its `r²` coefficient is `Y²`.
- **Mutants.** Each exits 1:
  - M1 `ρ_f = ℓ^{1/4+1/40}`;
  - M2 drop the factor `2^{m−1}` in T4;
  - M3 Lipschitz constant `6κ|Δ|` in T3;
  - M4 a one-sided axial row in T5, which produces an `r¹` term.

  An unknown label exits 2.

**What the controls do not test.** Lemma D, (1.2), Steps F2–F3, Step C3, Lemma O and the assembly as statements about
random fields; these are proved in prose. T5 tests the deterministic structure (2.2) on polynomial fields only.

## 8. Review slices

- **A** §1–§2: Lemma D (eigenvalue coordinates, the Vandermonde cancellation), (1.2), and Lemma F. For Lemma F:
  - the pin reduction (2.1);
  - (2.2) against #191 and #198;
  - the good event and the dyadic layer bound (2.3);
  - the smoothness in `r²` (Step F3) and the properties (F.2).
- **B** §3: Lemma C. The three cases (Haynsworth, the sign window), the Lipschitz step, and the parity factorization
  for the target shift.
- **C** §4: Lemma O, the decomposition `F + K + J₂ + … + J₅`, the finite-part manipulation, the overlap cancellation and
  the exponents.
