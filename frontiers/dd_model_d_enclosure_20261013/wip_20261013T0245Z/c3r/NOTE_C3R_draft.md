# Note C3-R — a rate after the `ℓ^{2/3}` term: Theorem C3 with `O(ℓ^{2/3+δ})` (v1.0)

*Posted for two bounded nonauthor reads (Slices A and B, summoned below) under claim [6145251763](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6145251763); the controls comment follows this one. The frozen bytes are this served body (hash it) and the control script pinned in the controls comment.*

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`.
Scientific effect NONE until read. Scope: note C3's (the torus field of #237 §0, `d ≥ 2`, every `L`), consuming exactly
C3's sources at their stated scopes: note LU (Theorem U⁼, Lemma Π in its deterministic form, §2), #237 (Lemma R, Lemma K,
Step U4), #218 (Lemma D, (1.2)), #229 ((W⁺.2)), #242 (§4, for the remarks only). Nothing else; no numerical constant is
certified. Python standard library only (`fractions`).

## 0. Statement

Note C3 (Math- `frontiers/lifetime_two_thirds_chain_20261007/C3/PROOF.md`) proves, in every `d ≥ 2` and for every `L`,

    ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + c₃ℓ^{2/3} + o(ℓ^{2/3}),                              (C3)

with `c₃ = (1/3)∫_S∫_0^∞ 𝐄(k, u)k^{−5/3}dk dσ(u)`, and its Remark 4 says why there is no rate: Lemmas F₃ and T₁ are used only
pointwise in `k` and `κ`, and Theorem U⁼ only as a dominating function. This note keeps the error terms that C3's proofs of
F₃ and T₁ already contain, quantifies the two limits those proofs leave as `o(1)`, and integrates in C3's fold variable
with a split between the fold side and the cusp side. Notation is C3's (§0: `m = d − 1`, `s = (−1)^m`, `𝐓_r`, `𝐒_r`, `𝐀_0`,
`𝐀₂`, `𝓐`, `κ = k/r`, `A`, `P`, `e`, `U_red`, `𝔏`, `𝐋_F`, `a₁`, `𝐄`, the edge expectation (0.2), the identities (I.1)–(I.2),
the thresholds `r₄`, `ρ`) and note LU's (`𝔗`, Lemma Π's deterministic form, Theorem U⁼). Constants `C, c, N, ℓ₀, r₅`
depend only on `d` and `L` (and on the exponents `α`, `α′` where these are chosen), never on `k`, `κ`, `r`, `ℓ` or `u`;
`N` denotes a finite exponent whose value may change from line to line, and `θ := 1/(16(m + 1))` is C3's.

**Theorem C3-R.** In every `d ≥ 2` and for every `L` there are `δ = δ(d) > 0` and `ℓ₀ > 0` such that for `0 < ℓ ≤ ℓ₀`

    ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + c₃ℓ^{2/3} + O(ℓ^{2/3+δ}),                            (C3-R)

with the same `c₃` as (C3). Admissible values: `δ(2) = 1/30`, `δ(3) = 1/50`, `δ(4) = 1/51`, `δ(5) = 1/70`, `δ(6) = 1/89`; in
general `δ(d)` is the value `σ` of Lemma 4 below, and it is positive for every `d`.

**Lemma F₃-R (the fold layer, with error).** Let `0 < α < α_max := 1/2 − mθ/2` for `m ≥ 2` (for `m = 1` no `α` enters).
There are `C, c, N, r₅ > 0` such that for `0 < r ≤ r₅`, `k > 0` and `u`, whenever

    r^{1−2α−mθ} ≤ c k (1 + k)^{−N}     (`m ≥ 2`),        r^{1−θ} ≤ c k (1 + k)^{−N}     (`m = 1`),                         (V)

one has, with `η′ := max(r^{α}, r^{2α/(m−1)})` for `m ≥ 2` and `η′ := r` for `m = 1`,

    |(𝐓_r(k, u) − 𝐒_r(k, u))/r − 𝐋_F(k, u)| ≤ C e^{−ck²}(1 + k)^N [η′(1 + k^{−1}) + r(1 + k^{−2})].                      (F₃-R)

**Lemma T₁-R (the cusp tail, with error).** For `m ≥ 2` let `0 < α′ < α′_max := (1/2)min(1, 2/(m − 1))`; for `m = 1` put
`α′ := 1`. There is `C` such that for `κ ≥ 1` and `u`

    |κ(𝓐(κ, u) − 𝐀₂(0, u)) − a₁(u)| ≤ C κ^{−α′}.                                                                       (T₁-R)

**Lemma 4 (the integration).** Let `m ≥ 2`, `α`, `α′` as above, `a_eff := α` for `m ≤ 3` and `a_eff := 2α/(m − 1)` for
`m ≥ 4`, and `v(α) := (1 − 2α − mθ)/(3(4 − 2α − mθ))`. For every `σ` with `0 < σ ≤ min(v(α), 1/12)`, (C3-R) holds with

    δ = min(σ, a_eff/3 − σ(a_eff + 5), α′/3 − σ(5 + 4α′), 1/3 − 9σ)                                                       (4.0)

whenever this is positive. For `m = 1`, (C3-R) holds with `δ = min(σ, 1/3 − 9σ)` for `0 < σ ≤ min((1 − θ)/(3(4 − θ)), 1/12)`.

The admissible values above come from (4.0): `d = 2`: `σ = 1/30`; `d = 3`: `α = 23/60`, `α′ = 499/1000`, `σ = 1/50`
(`v(23/60) = 23/1149 > 1/50`); `d = 4`: `α = 3/8`, `α′ = 499/1000`, `σ = 1/51`; the values for `d = 5, 6` are from the
control script's grid (§6). Any `σ` admissible in Lemma 4 is a valid exponent; the theorem states one.

## 1. The route

C3 §4 gives, for `ℓ ≤ ρ³` (its fixed split `ρ = min(r₄, r₀/2) ≤ 1`) and integrated over `u ∈ S^{d−1}`,

    ν_cand − cℓ^{−1/3} − B_{d,L} − I^{cand}ℓ^{1/4} − c₂ℓ^{1/3} = ∫_0^ρ∫_S D_r(ℓ/r³, u) dσ(u) dr + O(ℓ),
    D_r(k, u) = 𝐓_r(k, u) − 𝐓_r(0, u) − r^{−2}𝐀_0(k, u) − [𝐀₂(k, u) − 𝐀₂(0, u)] − 𝓐(k/r, u),                            (1.1)

and, in the fold variable `r = ℓ^{1/3}s` (`k = s^{−3}`, `κ = ℓ^{−1/3}s^{−4}`), with `φ_r(k, u) := D_r(k, u)/r`,

    ∫_0^ρ D_r(ℓ/r³, u) dr = ℓ^{2/3}∫_0^{ρℓ^{−1/3}} s φ_{ℓ^{1/3}s}(s^{−3}, u) ds,        c₃ = ∫_S∫_0^∞ s𝐄(s^{−3}, u) ds dσ(u).   (1.2)

Theorem U⁼ gives `|φ_r(k)| ≤ C(r min(1, κ) + min(k, 1/k))`, hence `|sφ| ≤ 2Cs min(1, s^{−3})` on `s ≤ ρℓ^{−1/3}`, and C3
proves `|𝐄(k)| ≤ C min(k, 1/k)`. Writing `φ = 𝐄 + (φ − 𝐄)` and splitting at `S ≥ 1`,

    ℓ^{−2/3}[ν_cand − (main terms) − c₃ℓ^{2/3}] = ∫_S[∫_0^S s(φ − 𝐄) ds] dσ + O(1/S) + O(ℓ^{1/3}),                        (1.3)

where `O(1/S)` collects `∫_S^{ρℓ^{−1/3}} s|φ| ds ≤ 2C/S` and `∫_S^∞ s|𝐄| ds ≤ C/S`, and `O(ℓ^{1/3})` is the `O(ℓ)` of (1.1)
divided by `ℓ^{2/3}`. The decomposition of C3 §4 (its "pointwise limit") reads, exactly,

    φ_r(k) − 𝐄(k) = E_F + E_K + E_0 − E_T/k,
    E_F := (𝐓_r(k) − 𝐒_r(k))/r − 𝐋_F(k),      E_K := (𝐒_r(k) − r^{−2}𝐀_0(k) − 𝐀₂(k))/r,
    E_0 := −𝐓_r(0)/r,                           E_T := κ(𝓐(κ) − 𝐀₂(0)) − a₁,                                               (1.4)

since `(𝐀₂(0) − 𝓐(κ))/r = −(1/k)·κ(𝓐(κ) − 𝐀₂(0))` and `𝐄 = 𝐋_F − a₁/k`. Lemma K (K.1) gives `|E_K| ≤ Cr(1 + k)^N e^{−ck²}`;
#229 (W⁺.2) at `κ = 0`, integrated in `b` as in LU §4, gives `|E_0| ≤ Cr² log(2/r)`; Lemmas F₃-R and T₁-R bound `E_F` and
`E_T`. §4 does the integration.

## 2. Proof of Lemma F₃-R

This is C3 §2 with three changes: the localization scale `η := r^{α}` is left free (C3 takes `α = 1/4`), every constant's
dependence on `k` is written out, and the final limit is quantified. We follow C3's steps and notation (`g ~ Q̄_{r,k}`,
`𝔗 := 1 + ‖g‖_{C^{N₀}(𝔅)}`, `Λ := r^{−2}Π(1_{typed} − 1{A < 0})`, `𝔊 := {𝔗 ≤ r^{−θ}}`, `𝔈 := {λ_{m−1} ≤ −η, |P| ≥ η²}`,
`𝔈 := Ω` if `m = 1`). Two facts supply every `k`-dependence:

- (J) *Moments.* `E[𝔗^p | J] ≤ C_p(1 + k + |J|)^p` for the free-jet vector `J` (#218 (1.2); #237 (R.4)), and under `Q̄_{r,k}`
  the even jets have a centred law not depending on `k` while the odd jets have means `k·w` and a covariance independent of
  `k` ((R.2)). So every polynomial `Π_0` of degree `q` in the jets satisfies `E|Π_0|^p ≤ C_p(1 + k)^{pq}`, and `|W| ≤ C(1 + k)^N𝔗^m`,
  `|U|, |V| ≤ C(1 + k)^N𝔗^N` pathwise on the relevant events (the polynomials `U`, `V`, `W`, `W₀` of C3 (1.2) and #237 (2.1)
  have coefficients polynomial in `k`).
- (G) *The prefactor.* `𝐓_r − 𝐒_r = 12 p_{V_r}(v(k)) E_{Q̄_{r,k}}[Λ]`, and `p_{V_r}(v(k)) ≤ Ce^{−ck²}` with
  `|p_{V_r}(v(k)) − p_{V_0}(v(k))| ≤ Cre^{−ck²}`: `V_r` is centred Gaussian with covariance smooth and uniformly
  nondegenerate in `r` ((R.4)), and `v(k) = kv(1)`.

Every error below is first bounded for `E[Λ]/r` (that is, before the prefactor), with polynomial factors `(1 + k)^N` kept;
the prefactor then supplies `e^{−ck²}`. We write `𝔼_r[φ; λ_m = 0⁻]` for the edge expectation (C3 (0.2)) under `Q̄_{r,k}`.

*Step 1 (the endpoint quantities).* Lemma Π at gap `k`, deterministic form (LU §2, with the remainder
`O(r³(1 + |k|)^N(1 + ‖g‖)^N)` of #237's proof), gives C3's (2.1) with

    |ε_±| ≤ Cr²(1 + k)^N𝔗^N,        |m_i| ≤ C(1 + κ)(1 + k)^N𝔗^N,        |Λ| ≤ C(1 + κ)²(1 + k)^N𝔗^N.                     (2.1)

*Step 2 (localization).* As in C3, with the `k`-dependence from (J):
- *Off `𝔊`.* `P(𝔊^c | J) ≤ C_pr^p(1 + k + |J|)^{p/θ}`, so `E[|Λ|1_{𝔊^c}] ≤ C_p(1 + κ)²r^p(1 + k)^{N_p}` for every `p`.
- *Where `Λ ≠ 0` on `𝔊`.* As in C3: `Λ = 0` if `λ ≥ 2r𝔗`; if `λ ≤ −2r𝔗`, `Λ = (x² − y²)1{|x| ≥ y}` vanishes unless
  `6κ|Δ| ≤ |x| + |y − 6κsΔ| ≤ C(1 + k)^N𝔗^N`. So on `𝔊`, `Λ ≠ 0` only on `{|λ| < 2r𝔗} ∪ {A < 0, |Δ| ≤ C(1 + k)^N(r/k)𝔗^N}`,
  and there `|Λ| ≤ C(1 + k)^N𝔗^N`.
- *On `𝔊 ∖ 𝔈`* (`m ≥ 2`). Off `𝔈` a second eigenvalue lies within `η′` of `0`. The two-eigenvalue bounds of C3 Step 2 (the
  Weyl density of `A`, whose law does not depend on `k` by (R.2), has a bounded joint density of two eigenvalues; #218
  Lemma D's second bound for `{A < 0, |Δ| ≤ δ}`) give probabilities `≤ Cεη′` with `ε = 2r𝔗` and `≤ Cδη′` with
  `δ = C(1 + k)^N(r/k)𝔗^N`. With the layer device of #237 Step U2 (a) for the factors `𝔗^N` (condition on `A`, sum over
  dyadic layers of `𝔗`, use (J)),

      E[|Λ|1_{𝔊∖𝔈}] ≤ C(1 + k)^N(r + r/k)η′.                                                                           (2.2)

*Step 3 (typedness near the edge, on `𝔊 ∩ 𝔈`).* Since `‖A_i − A‖ ≤ r𝔗 ≤ r^{1−θ}` and `η = r^{α}` with `α < α_max < 1 − θ` (`m ≥ 2`), for
`r ≤ r₅` the second-largest eigenvalues of `A_M`, `A_S` are `≤ −η + r^{1−θ} < −η/2`, and on `{|λ| < 2r𝔗}` the top eigenvalue
`λ` is simple with gap `≥ η/2`. First-order eigenvalue perturbation (the second-order term is `≤ ‖A_M − A‖²/gap`) gives

    λ_M = λ − (r/2)B_ee + O(r^{2−α}𝔗²),                                                                              (2.3)

and C3's decomposition `Λ = Λ₁ + Λ₂ + Λ₃` on `𝔊 ∩ 𝔈` holds verbatim (Haynsworth; the sign of `det H_S`). For `m = 1` there is
no second eigenvalue, `A_M = λ_M` exactly, and `λ_M = λ − (r/2)B_ee + O(r²𝔗)`.

*Step 4 (`Λ₃` and `Λ₂`).* `|Λ₃| ≤ y² ≤ Cr²(1 + k)^N𝔗^N` as in C3 (for `λ ≥ 0`, `y > |x| ≥ 0` forces `y ≤ |rsV + ε₋|`). For
`Λ₂`: on `𝔊 ∩ 𝔈 ∩ {λ < 0 ≤ λ_M}` the Schur complement of `A_M` in `K_M` is

    σ_M = α_M − r(β_M·e_{M,m})²/λ_M − rΣ_{j<m}(β_M·e_{M,j})²/λ_j(A_M) ≤ −6k + Cr𝔗 + 2r^{1−α}|β_M|² ≤ −6k + Cr^{1−θ} + Cr^{1−α−2θ},

using `α_M = −6k + O(r𝔗)`, `|β_M| ≤ C𝔗`, `λ_j(A_M) ≤ −η/2` for `j < m` and `λ_M > 0`. So `σ_M < 0`, hence `𝔞 > 0`, `|x| ≥ y`
and `Λ₂ = 0`, as soon as `Cr^{1−α−2θ} < 3k` (and `r ≤ r₅`); this is implied by (V), since `1 − α − 2θ > 1 − 2α − mθ` for
`m ≥ 2` (and for `m = 1` the sum over `j < m` is empty, so `σ_M < α_M < 0` once `Cr^{1−θ} < 3k`, which is (V)).

*Step 5 (the layer `Λ₁`).* With `a := |P||U_red|`, `β := 6κ|P|` and C3's (2.3) (`x² − y² = a² − β²λ² + ϱ`):
- *Where `y < 0`.* `6κ|λ||P| ≤ |rsV + ε₋| ≤ Cr(1 + k)^N𝔗^N` is a `λ`-interval of length `≤ Cr²(1 + k)^N𝔗^N/(k|P|)`; the
  Vandermonde factor `|P|` of the Weyl density at `λ_m = 0` cancels the `1/|P|` (#218 Lemma D's second bound), and with
  `|Λ| ≤ C(1 + k)^N𝔗^N` and the layer device this set costs `≤ C(1 + k)^N r²/k`.
- *The perturbation.* On `𝔊 ∩ 𝔈`, `β = 6κ|P| ≥ 6k r^{2α−1}` and `|W| ≤ C(1 + k)^N𝔗^m ≤ C(1 + k)^N r^{−mθ}` (J). Under (V)
  (with its `N` at least that of `W`) and `r ≤ r₅`, `2|W| ≤ β`, so `|λ||W| ≤ β|λ|/2` and positivity forces
  `β|λ| ≤ 2a + Cr(1 + k)^N𝔗^N`, i.e. `|λ| ≤ (r/(3k))(|U_red| + Cr^{1−2α}(1 + k)^N𝔗^N)`. There
  `|ϱ| ≤ C(r/k)(1 + a)²(1 + k)^N𝔗^N + Cr(1 + a)(1 + k)^N𝔗^N` (C3's control E8 with the coefficients tracked), and
  `|(a² − β²λ² + ϱ)₊ − (a² − β²λ²)₊| ≤ |ϱ|` where either is positive; integrating over the `λ`-window of length `≤ C(r/k)(1 + a)`
  and over `Rest` with the layer device, this costs `≤ C(1 + k)^N r²(1 + k^{−2})`. For `m = 1`, `P = 1` and the same bound
  holds with `β = 6κ`, under `r^{1−θ} ≤ ck(1 + k)^{−N}`.
- *The main part.* Put `γ := 1 − α` (C3: `3/4`). On `𝔈 ∩ {|U_red| < 6kr^{−γ}}`, `a/β = r|U_red|/(6k) < r^{1−γ} = η ≤ |λ_{m−1}|`
  (for `m = 1` there is no constraint and the event `{|U_red| ≥ 6kr^{−γ}}` is not removed: `J` is then a Gaussian density in
  `λ`, smooth on `R`, so the main part runs over all `Rest` and the `U_red` term below is absent), so (I.2) applies and

      ∫_{−∞}^0 (a² − β²λ²)₊ J(λ, Rest) dλ = J(0⁻, Rest)P²|U_red|³/(9κ) + O((a/β)²a² sup_{|λ|≤a/β}|∂_λJ|),

  with `J` the joint density of `(λ_m, Rest)` under `Q̄_{r,k}`, `C¹` in `λ` on `(λ_{m−1}, ∞)` with `|∂_λJ| ≤ C(1 + |Rest|)^Nq(Rest)`,
  `q` Gaussian; the error integrates over `Rest` to `≤ C(1 + k)^N r²k^{−2}`. The event `{|U_red| ≥ 6kr^{−γ}}` has, given
  `A`, Gaussian tails: `U_red = 3kB_ee − γ_e²/4` with `(γ_e, B_ee)` Gaussian of mean `O(k)` and bounded variance, so
  `P(|U_red| ≥ 6kr^{−γ} | A) ≤ C_p(r^{γ}(1 + k)²/k)^p` for every `p`; against the weight `|Λ| ≤ C(1 + k)^N𝔗^N` this costs
  `≤ C_p(1 + k)^N(r^{γ}(1 + k)²/k)^p`, and the same event's share of the edge term,
  `(r/(9k))𝔼_r[P²|U_red|³1_𝔈1{|U_red| ≥ 6kr^{−γ}}; λ_m = 0⁻] ≤ C_p(1 + k)^N(r/k)(r^{γ}(1 + k)²/k)^p` (Hölder under C3 (1.1)),
  is absorbed the same way. Integrating over `Rest` on `𝔈`:

      E[Λ₁] = (r/(9k)) 𝔼_r[P²|U_red|³1_𝔈; λ_m = 0⁻] + O((1 + k)^N r²(1 + k^{−2})) + O_p((1 + k)^N(r^{γ}(1 + k)²/k)^p).     (2.4)

*Step 6 (the limit, quantified).* Three estimates replace C3's "as `r ↓ 0`":
- (a) *The truncation.* The edge density (C3 (1.1)) integrates `P²h_k(e)|V(λ′, 0)|p_A(·)` over `λ₁ < ⋯ < λ_{m−1} < 0` and
  `O`, with `h_k(e) ≤ C(1 + k)^N`. The set `𝔈^c = {λ_{m−1} > −η} ∪ {|P| < η²}` lies in `{−η < λ_{m−1} < 0} ∪ {min_{j<m}|λ_j| < η^{2/(m−1)}}`,
  and the density of each `λ_j` given the rest is bounded by a Gaussian-weighted polynomial, so

      0 ≤ 𝔼_r[P²|U_red|³(1 − 1_𝔈); λ_m = 0⁻] ≤ C(1 + k)^N η′,                                                            (2.5)

  under `Q̄_{r,k}` for every `0 ≤ r ≤ r₅` (the edge expectation under `Q̄_{r,k}` exists by the argument of C3 Lemma 0). For `m = 1`
  there is nothing to truncate.
- (b) *The `r`-dependence.* By (R.4), the law of the finite jet vector `(A, γ, B)` under `Q̄_{r,k}` is Gaussian with mean and
  covariance smooth in `r ∈ [0, r_0^*]`, uniformly nondegenerate, the mean affine in `k` and the covariance
  independent of `k` ((R.2) holds for every `r`). The edge expectation `𝔼_r[P²|U_red|³; λ_m = 0⁻]` is (C3 (1.1)) an integral
  of a fixed polynomial-times-`|V|` against this Gaussian density restricted to `λ_m = 0`, i.e. a smooth function of the
  density's parameters on the nondegenerate set, with derivatives bounded by Gaussian-weighted polynomials in `k`; composed
  with the smooth parameter map, it is a smooth function of `r` (evenness is not used), so

      |𝔼_r[P²|U_red|³; λ_m = 0⁻] − 𝔏(k, u)| ≤ C(1 + k)^N r.                                                              (2.6)

- (c) *The prefactor*, (G): `|12p_{V_r}(v(k)) − 12p_{V_0}(v(k))| ≤ Cre^{−ck²}`, and `𝔏(k, u) ≤ C(1 + k)^N` (C3 Lemma 0).

*Conclusion.* Collecting Steps 2–6, for `r ≤ r₅` under (V): with `𝐋_F = (12/(9k))p_{V_0}(v(k))𝔏`,

    (𝐓_r − 𝐒_r)/r − 𝐋_F = 12p_{V_r}(v(k))·[E[Λ]/r − (1/(9k))𝔏] + (12/(9k))𝔏·[p_{V_r}(v(k)) − p_{V_0}(v(k))],

and `E[Λ]/r − (1/(9k))𝔏` is bounded by `C(1 + k)^N` times
`[r^{p−1}(1 + κ)² + (1 + 1/k)η′ + r + r/k + r(1 + k^{−2}) + rk^{−2} + r^{−1}(r^{γ}(1 + k)²/k)^p + η′/k + r/k]`
(off `𝔊`; (2.2); `Λ₃`; `{y < 0}`; the perturbation; the main part; the `U_red` event; (2.5) and (2.6), each carrying the
factor `1/(9k)`). Under (V) and `r ≤ r₅`, `r^{−1}(r^{γ}(1 + k)²/k)^p ≤ Cr(1 + k)^{2p}`: for `m ≥ 2`, (V) gives
`r^{γ}(1 + k)²/k ≤ c^{−1}r^{α+mθ}(1 + k)^{2−N}`, since `γ − (1 − 2α − mθ) = α + mθ > 0`, so `p ≥ 2/(α + mθ)` suffices; for
`m = 1` the term is absent (Step 5). Also `r^{p−1}(1 + κ)² ≤ r^{p−3}(1 + k)²`. With `r ≤ η′`, the bracket is
`≤ C(1 + k)^N[η′(1 + 1/k) + r(1 + k^{−2})]`, and the prefactor contributes `e^{−ck²}`. This is (F₃-R). ∎

(The `N` in (V) is the one of `|W| ≤ C(1 + k)^N𝔗^m` and of the `U_red` tail; both are finite and depend only on `d`. (V) is only
used to make `2|W| ≤ β`, `Λ₂ = 0` and the `U_red` event rare; §4 applies the lemma only where (V) holds with room.)

## 3. Proof of Lemma T₁-R

This is C3 §3 with the localization scale `η := κ^{−α_T}` left free and the two tail thresholds adjusted. Recall C3 (3.1):
`𝓐(κ) − 𝐀₂(0) = 12p_{V_0}(v(0))E_{Q̄_{0,0}}[(Y′² − 36κ²Δ²)₊1{A < 0}]`, and `𝔈_κ := {λ_{m−1} ≤ −η, |P| ≥ η²}` (`Ω` if `m = 1`),
`η′ := max(η, η^{2/(m−1)})`. All laws here are at `k = 0`, so no `k`-dependence enters.

- *Off `𝔈_κ`* (`m ≥ 2`): C3's dyadic-layer argument gives `E[Y′²1{A < 0, |Δ| ≤ |Y′|/(6κ)}1_{𝔈_κ^c}] ≤ Cκ^{−1}η′` verbatim (its
  `η′` is ours).
- *On `𝔈_κ`*: with `a := |P|γ_e²/4`, `β := 6κ|P| ≥ 6κη² = 6κ^{1−2α_T}`, and `ϱ = −Pγ_e²λW₀/2 + λ²W₀²`. Fix `0 < a₀ < 1 − 2α_T`.
  Off `{|W₀| ≥ κ^{a₀}}`, whose cost against the weight `Y′²` is `O(κ^{−p})` for every `p` (`W₀` is a polynomial in the
  Gaussian vector `(A, γ, f₄)`), `β ≥ 6κ^{1−2α_T} ≥ 2κ^{a₀} ≥ 2|W₀|` for `κ ≥ 1`, so positivity forces `|λ| ≤ γ_e²/(12κ)`.
  This window lies in `(λ_{m−1}, 0)`, where the density is `C¹` in `λ`, unless `γ_e² ≥ 12κ^{1−α_T}`, an event of cost
  `O(κ^{−p})` (given `A`, `γ_e` is centred Gaussian with bounded variance; the weight is `Y′²`). There C3's bound
  `|ϱ| ≤ (1 + |P|)(1 + γ_e²)²(1 + |W₀|)²/κ` holds (control E9 of C3), so the perturbation costs `O(κ^{−2})` as in C3 §2 Step 5
  (the window has length `≤ γ_e²/(6κ)`), and (I.2) gives

      E[(Y′² − 36κ²Δ²)₊1{A < 0}1_{𝔈_κ}] = (1/(9κ))𝔼_0[P²(γ_e²/4)³1_{𝔈_κ}; λ_m = 0⁻] + O(κ^{−2}),

  the (I.2) error being `O((a/β)²a² sup|∂_λJ|) = O(κ^{−2})` after integration.
- *The truncation.* As in (2.5) at `k = 0` and `r = 0`: `0 ≤ 𝔼_0[P²(γ_e²/4)³(1 − 1_{𝔈_κ}); λ_m = 0⁻] ≤ Cη′`.

Multiplying by `12p_{V_0}(v(0))κ` and using `a₁ = (12/9)p_{V_0}(v(0))𝔏(0, u)` (C3 (0.3)),
`|κ(𝓐(κ) − 𝐀₂(0)) − a₁| ≤ C(η′ + κ^{−1} + κ^{1−p})`. With `η′ = κ^{−min(α_T, 2α_T/(m−1))}` and `α_T < 1/2` (any `a₀ > 0`
works), every `α′ < (1/2)min(1, 2/(m − 1))` is attained. For `m = 1` the off-`𝔈_κ` and truncation terms are absent and the
bound is `C(κ^{−1} + κ^{1−p})`, so `α′ = 1`. ∎

## 4. Proof of Theorem C3-R (Lemma 4)

Fix `m ≥ 2`, `α`, `α′`, `σ` as in Lemma 4, put `S := c_Sℓ^{−σ}` (with `0 < c_S ≤ 1` fixed below) and `k_G := (C₁ log(1/ℓ))^{1/2}` with `C₁ := 4/c` for the `c` of
(F₃-R) and (K.1). We bound `∫_0^S s|φ − 𝐄| ds` by (1.4), term by term, uniformly in `u`, for `ℓ ≤ ℓ₀`; on `s ≤ S`,
`r = ℓ^{1/3}s ≤ ℓ^{1/3−σ} ≤ r₅`.

*The large-`k` end, `s ≤ s_G := k_G^{−1/3}` (so `k ≥ k_G`).* Here we do not use (F₃-R). Directly from (G), (2.1) and (J),
`|𝐓_r − 𝐒_r|/r ≤ Ce^{−ck²}(1 + κ)²(1 + k)^N r^{−1}`, and `|𝐋_F(k)| ≤ Ce^{−ck²}(1 + k)^N`. Here `κ ≥ 1` (so
`(1 + κ)² ≤ 4k²/r²`), `r^{−3} = k/ℓ`, and, for `k ≥ k_G`, `e^{−ck²} ≤ e^{−ck_G²/2}e^{−ck²/2} = ℓ²e^{−ck²/2}` with
`sup_k e^{−ck²/2}(1 + k)^{N+3} ≤ C`; so `s|E_F| ≤ Cℓ^{−1}·ℓ²·s` and `∫_0^{s_G} s|E_F| ds ≤ Cℓ s_G² ≤ Cℓ`. (`E_K`, `E_0` and
`E_T/k` are bounded on all of `(0, S]` below.)

*The fold side, `s_G ≤ s ≤ S`.* Here `k = s^{−3} ≤ k_G`, so `(1 + k)^N ≤ C(log(1/ℓ))^{N/2}` and
`e^{−ck²}(1 + k)^N ≤ C`. Condition (V), with `n := 1 − 2α − mθ > 0`: `r^{n} = ℓ^{n/3}s^{n}`. For `1 ≤ s ≤ S`, `k ≤ 1` and
`ck(1 + k)^{−N} ≥ c2^{−N}s^{−3}`, so (V) holds if `ℓ^{n/3}S^{n+3} ≤ c2^{−N}`, i.e. `c_S^{n+3}ℓ^{n/3 − σ(n+3)} ≤ c2^{−N}`; for
`σ ≤ v(α) = n/(3(n + 3))` the power of `ℓ` is `≥ 0`, so this holds for `ℓ ≤ 1` once `c_S^{n+3} ≤ c2^{−N}` (control E2 checks
`0 < v(α) < 1/12`). For `s_G ≤ s ≤ 1` (`1 ≤ k ≤ k_G`), (V) follows from `ℓ^{n/3} ≤ c2^{−N}k_G^{1−N}`, which holds for `ℓ ≤ ℓ₀`.
Then (F₃-R), (K.1), (W⁺.2) and (T₁-R) (valid since `κ = ℓ^{−1/3}s^{−4} ≥ ℓ^{−1/3}S^{−4} = c_S^{−4}ℓ^{−1/3+4σ} ≥ 1` for
`σ ≤ 1/12`) give, with `η′ = r^{a_eff}`:

    |φ − 𝐄| ≤ C[ℓ^{a_eff/3}s^{a_eff}(1 + s³) + ℓ^{1/3}s(1 + s⁶) + ℓ^{1/3}s + ℓ^{2/3}s² log(2/(ℓ^{1/3}s)) + ℓ^{α′/3}s^{3+4α′}],

the terms being `E_F` (both parts, `r(1 + k^{−2}) = ℓ^{1/3}s(1 + s⁶)`), `E_K`, `E_0` and `E_T/k = κ^{−α′}k^{−1}`. Integrating
`s(·)` from `0` to `S` (`S ≥ 1` for `ℓ ≤ ℓ₀`; the `E_F` bound is used on `[s_G, S]` only, and `s ≤ s_G` is covered above; the
`E_K`, `E_0` and `E_T/k` bounds hold on all of `(0, S]`, since (K.1), (W⁺.2) and (T₁-R) need neither (V) nor `k ≤ k_G`):

    ∫_0^S s|φ − 𝐄| ds ≤ C[ℓ^{a_eff/3}S^{a_eff+5} + ℓ^{1/3}S^9 + ℓ^{1/3}S³ + ℓ^{2/3}S⁴log(1/ℓ) + ℓ^{α′/3}S^{5+4α′}].              (4.1)

*Conclusion.* By (1.3), with `S = c_Sℓ^{−σ}` (the constant `c_S` enters only `C`),

    |ℓ^{−2/3}[ν_cand − (main terms) − c₃ℓ^{2/3}]| ≤ C[ℓ^{a_eff/3−σ(a_eff+5)} + ℓ^{1/3−9σ} + ℓ^{1/3−3σ} + ℓ^{2/3−4σ}log(1/ℓ) + ℓ^{α′/3−σ(5+4α′)} + ℓ^{σ} + ℓ^{1/3} + ℓ],

and every exponent is at least `δ` of (4.0) (the `ℓ^{2/3−4σ}log` term is dominated by `ℓ^{1/3−9σ}` for `σ ≤ 1/12`, and the last
two terms by `ℓ^{σ}`). This is (C3-R). For `m = 1`, (F₃-R) has no `η′` term, (T₁-R) has `α′ = 1`, and (V) reads
`r^{1−θ} ≤ ck(1 + k)^{−N}`, whose fold-variable form is `σ ≤ (1 − θ)/(3(4 − θ))`; the same integration gives the stated `δ`. ∎

*The numbers.* (4.0) is maximized, for `m = 2`, at the crossing `a_eff/(3(a_eff + 6)) = v(α)`, i.e. `α* = (6 − 12θ)/15 = 23/60`,
`σ* = 23/1149 = 0.02002…`, with `α′` close to `1/2` not binding (`α′/3 − σ(5 + 4α′) > σ`); so `δ(3) = 1/50 < σ*` is
admissible. For `m = 1`: `1/3 − 9σ = σ` at `σ = 1/30 ≤ (1 − θ)/(3(4 − θ))`. The control script (§6) verifies these and reports
the grid optima for `d = 4, 5, 6` (`δ(4) ≥ 1159/58773 > 1/51`, `δ(5) ≥ 779/54177 > 1/70`, `δ(6) ≥ 7735/686757 > 1/89`).

## 5. Remarks

1. *What the rate is and is not.* `δ(3) = 1/50` is far from the formally expected next term `ℓ^{3/4}` (#242's matched
   count: cusp-side powers `ℓ^{(j+1)/4}`, fold-side `ℓ^{(j+1)/3}`; `ℓ^{3/4}` is `j = 2` on the cusp side), and it is not
   claimed to be sharp in any sense: it is what C3's proof gives once its error terms are kept. Three things limit it:
   the localization scales (`η = r^{α}` with `α < 1/2 − mθ/2` forced by `2|W| ≤ 6κ|P|` on `𝔈`; `η = κ^{−α_T}` with
   `α_T < 1/2`), the validity condition (V) that confines the fold-side analysis to `r^{1−2α−mθ} ≲ k` (the strip and the
   perturbation), and the crude domination `|φ − 𝐄| ≤ Cs^{−3}` on the cusp side `s > S`, which costs `1/S`. The first two
   could be improved by a finer localization (the eigenvalue gap is only needed for the perturbation of `λ_M`, not for the
   layer itself); the third needs the cusp-side expansion to second order (`κ(𝓐(κ) − 𝐀₂(0)) = a₁ + a₂/κ + …`) and its
   matching with the fold side on `1 ≪ κ`, `k ≪ 1` — C3 Remark 4's two ingredients, not attempted here.
2. *What is inherited.* Note C7 consumes Theorem C3 for the candidate density in its (C7.2) and Corollary E1 (to be checked
   there: where C7 uses C3's remainder as a black box, it inherits `O(ℓ^{2/3+δ})`; where it uses note SL's `o(ℓ^{2/3})`,
   SL would need its own quantification). Nothing here changes a statement of C3, LU, #237, #218, #229 or #242.
3. *Uniformity.* Every bound is uniform in `u ∈ S^{d−1}` (C3's and LU's constants are), so the integration over `S^{d−1}`
   in (1.3) is immediate; `ℓ₀` depends on `d`, `L` and the chosen `(α, α′, σ)`.
4. *The log threshold.* The large-`k` end uses only the Gaussian prefactor and the crude bound (2.1), so the polynomial
   degrees `N` never enter `δ`; they enter `ℓ₀` through (V) and the `(log(1/ℓ))^{N/2}` factors.
5. *Author-side referee round.* Before posting, two clean-context referee passes in the same session (Anthropic Claude
   subagents; same provider and session, so not review evidence) read §§0–2 and §§3–6 against C3 and LU. Both were AMEND
   with no blocking finding; their changes are applied here: `m = 1` takes no `α` and keeps the `U_red` event; the sign of
   `E_T/k` in (1.4); `O(r)` rather than `O(r²)` in (G), (2.6) and Step 6(c) (evenness in `r` is not used); `(1 + k)²` in the
   `U_red` tail and that event's share of the edge term; the large-`k` end keeps half the Gaussian; `S := c_Sℓ^{−σ}` so that
   (V) holds up to `σ = v(α)`. No stated `δ(d)` changed.

## 6. Dependencies, scope, not claimed, controls

**Consumed.** Exactly note C3's sources, at their stated scopes, plus note C3 itself (its statements, (I.1)–(I.2), Lemma 0,
and the proofs of F₃, T₁ and C3 as the skeleton): note LU (Theorem U⁼, §2's deterministic Lemma Π with the
`O(r³(1 + |k|)^N(1 + ‖g‖)^N)` remainder, §4's decomposition), #237 (Lemma R (R.2), (R.4); Lemma K (K.1); Step U2 (a)'s
layer device; Step U4), #218 (Lemma D; (1.2)), #229 ((W⁺.2)). Nothing else.

**Not claimed.** No sharpness of `δ`; no statement about `ν_eld` or `ρ_rej` (Remark 2 only says what C7 could inherit);
nothing for `L < L₀` beyond C3's scope (C3's Proposition G″ and the sign of `c₃(L)` are untouched); no certified number;
nothing pointwise in `b`; no uniformity in `d` or `L`.

**Controls** (`c3r_exact.py`, Python standard library, exact rationals, deterministic, stdout byte-identical under `-O`):
E1 the exponent arithmetic of Lemma 4 for `d = 2, …, 6` (the six exponents of (4.1) and (1.3), the validity caps `σ ≤ v(α)`, `σ ≤ 1/12`,
the closed-form optimum for `m = 2` at `α* = 23/60` with `σ* = 23/1149 > 1/50`, the admissibility of `δ(2) = 1/30` and
every stated `δ(d)`, `d = 2, …, 6`, with every term `≥ δ`); E2 the positivity `0 < v(α) < 1/12` on `0 < α < α_max` (exact
endpoints, monotonicity); E3 the exponents of (4.1) re-derived term by term from the substitution `r = ℓ^{1/3}s`, `k = s^{−3}`,
`κ = ℓ^{−1/3}s^{−4}` (with `a_eff = min(α, 2α/(m − 1))` derived independently) agree with the table at 56 points. Mutants
(`c3r_mutants.py`, each must be rejected): M1 the T₁-R term with `4α′` replaced by `2α′`; M2 `v(α)` with `mθ` dropped; M3 the
`m = 1` rate `1/30` replaced by `1/29`; M4 `a_eff = α` for every `m`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
