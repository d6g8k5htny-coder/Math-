# The candidate density with remainder `ℓ^{3/5}`: a reflection parity removes the `ℓ^{1/2}` term

Object: CL-CANDIDATE-PARITY-RATE-20261001-v1.1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 1 October 2026.
**v1.1 (wording only; no estimate or conclusion changes):** the six nonblocking corrections of the C55 nonauthor reviews
(OpenAI Codex, on head `a6b6788`: Slice A 5385194600, Slice B 5385169112, Slice C 5385136758 with addendum
5940107723) are applied. (1) In Lemma Π, `det K_i` is affine in `k` *at fixed free jets*, not along the laws `Q̄_{r,k}`,
under which the odd free jets have `k`-dependent means. (2) The moment bounds before Lemma Π, and Lemma Π, are stated
for signed `k` with `1 + |k|`. (3) In Lemma Λ, `φ″` is given as a distribution. (4) In Lemma Λ's kink step, `ρ` is the
unnormalized Weyl-coordinate slice, and the measure is stated. (5) The case `m = 1` of that step is spelled out.
(6) In Step U2 (b)(iii), the `f₄`-windows are the two one-sided threshold-crossing strips, centred at the shifted
points.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register, graph,
STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is certified. Same GitHub account as every lane;
zero organizational independence.

**What is new.** Math- #218 proves the candidate lifetime density to third order with remainder `O(ℓ^{4/11})`; Math- #229
improves this to `O(ℓ^{3/7})`. #229 Remark 1 explains why a two-region (fold/cusp) argument stops at `3/7`: its error
terms come in two matching pairs whose leading coefficients are not identified, namely the boundary layer of the fold
expansion against the `κ^{−1}` tail of the cusp kernel, and the truncation `A₂(k) − A₂(0) = O(k)` against the linear
cusp error `rκ = k`. This note uses a single region and proves `O(ℓ^{3/5})`. In particular **the candidate density has
no term of order `ℓ^{1/2}`**, although #218 §0 and #229 §0 record `ℓ^{1/2}` as the formal next order. Three ingredients:
- **Parity and reflection** (§§1–2). After the birth height is integrated out, the field splits into independent even
  and odd parts, the pin rows are even in the separation `r`, and point reflection `z ↦ −z` maps the problem at gap `k`
  to the one at `−k`. Parts of this are on file: #191 Lemma E Step 3 records that `det H_M det H_S/r²` is even in `r`,
  and #232 §§1, 3 uses the same birth-integrated basis and proves that the fold coefficient is even in `k` (Theorem J).
  New here is the use of the reflection for the conditional laws inside the cusp layer (Lemma Λ; Lemma U, Step U2).
- **A uniform two-scale kernel** (§4, Lemma U). For `k ≥ r²` the typed kernel equals the fixed-cone kernel plus a
  *layer* term, and the layer is, up to `O(r² + r min(k, 1/k))`, the cusp kernel's own tail `𝓐(κ) − 𝐀₂(0)`. So one
  formula, `r^{−2}𝐀_0 + [𝐀₂(k) − 𝐀₂(0)] + 𝓐(κ)`, approximates the kernel from the fold scale through the cusp scale,
  and no fold/cusp split point is needed. At the cusp scale it shows that the `O(r)` correction of the candidate cusp
  kernel vanishes.
- **A layer comparison lemma** (§3, Lemma Λ). Moving the gap parameter from `k` to `0` inside the layer costs
  `O(k²/(1 + κ))`, not `O(k²)`: the first order vanishes by reflection, and the kink of the weight is controlled through
  the density of its location (with Lemma D″, a bound for two small eigenvalues).

**Dependencies (consumed; both merged on 1 October 2026 with the reviewed blobs).**
- Math- #207 (`frontiers/cusp_second_order_20261001/PROOF.md`, blob `f6df5a73`; merged at `566b1a1`): §0
  (`Y`, `Δ`, `E₀`); §4 (4.1) (`𝒜^{cand}`, `𝒜^{con}`); §7: Lemma L (7.1)–(7.2), the decomposition of `B_{d,L}`, `I^{cand}`
  ((CU′.1), (7.3)).
- Math- #218 (`frontiers/candidate_third_order_20261001/PROOF.md`, blob `70ca57ef`; merged at `fb6ee97`): §0 (`A₂`,
  the coefficient `c₂` (0.1), the cusp kernels restated); §1 (Lemma D (1.1) and its proof; `T` and (1.2)); Step F1
  ((2.1)–(2.2) and the free-jet nondegeneracy); Step F3; (F.2) and the surrogate remark after Lemma F; Lemma C's Step C1
  (its three cases); the proof of Lemma O; §4 (the decomposition and the bounds on `J₂`–`J₅`).

**Merged inputs.** [R] (§2 rows and target; (R2)–(R5)); [P] (§2 finite-jet rank) with [E1], [E2], [REC]; [Z]
((Z2)–(Z3): `B_{d,L}`); Math- #191 (`441152df`: `r_0^*`, (2.1) and Lemma E Step 4 directly, Step 3 for attribution;
Lemma E Steps 1–3 through #218); Math- #198 (`abfb98ae`: (W.4) directly; (3.1), the sign window of §3 and Lemma W through
#218 and #207).
**Cited only:** #229 (Theorem T⁺, superseded here for `ν_cand`; Remarks 1–2), #232 (merged at `7fe06b0`: an independent
derivation of the same second coefficient (2.3), and the birth-integrated basis), #216 (values of `c₂`; the formal law (0.2); its
Monte Carlo), #223 (`c` and `c₂` in closed form, with certified enclosures), #214 (`d = 1`), #220 (the elder density; not
used).

## 0. Statement

Setting and notation are those of #218 §0 and #207 §0: fixed `d ≥ 2`, `m = d − 1`, `L > 0`, the [P] field `f` on the torus
`R^d/(LZ^d)`; a unit vector `u` with an orthonormal frame `Θ` of `u^⊥` (coordinate `x` along `u`, `y` along `Θ`); pins
`M = −ru/2` (height `b`, a maximum) and `S = ru/2` (height `b − kr³`, an index-`(d−1)` saddle); `κ := k/r`; the scaled
endpoint Hessians `K_M`, `K_S` with `det K_i = det H_i/r`; the candidate kernel `A_r(b, k, u) = 12π_r(v_r)E_Q[F_d(K_M)
F_{d−1}(K_S)]`, so that `ν_cand(ℓ) = ∫_0^{r_0}∫_R∫_{S^{d−1}} r^{−2}A_r(b, ℓ/r³, u) dσ db dr + ν_cand^{far,r_0}(ℓ)`; the
contact kernel `A_0`; the fold coefficient `A₂` and `c₂` of #218 (0.1); the cusp kernels `𝒜^{cand}`, `𝒜^{con}` of #207 (4.1)
(restated in #218 §0); `I^{cand}` of #207 (CU′.1); `c = c_{d,L}` and `B_{d,L}`.

*Jets at `0`.* `A := ∇_Θ²f(0)`, `B := ∂_uA`, `C := ∂_u²A`, `γ := ∇_Θ∂_u²f(0)`, `η := ∇_Θ∂_u³f(0)`, `f₄ := ∂_u⁴f(0)`,
`f₅ := ∂_u⁵f(0)`; `Δ := det A` and `A^♯ := adj A`; `Y′ := (f₄/12)Δ − γᵀA^♯γ/4`, the cusp variable `Y` of #207 §0 built from
the jets of `f` at `0`. Jets of even order (`A`, `C`, `η`, `f₄`) are called *even*, jets of odd order (`B`, `γ`, `f₅`)
*odd*; the parity map `𝒫` negates the odd ones.

*Birth-integrated kernels.* `𝐓_r(k, u) := ∫_R r^{−2}A_r(b, k, u) db`; `𝐀_0(k, u)` and `𝐀₂(k, u)`, defined for `k ∈ R` in
Lemma K and equal to `∫A_0 db` and `∫A₂ db` for `k ≥ 0`; `𝓐(κ, u) := ∫_R(𝒜^{cand} − 𝒜^{con})(b, κ, u) db`.

**Theorem P (the candidate density with remainder `ℓ^{3/5}`).** For every `d ≥ 2` and `L > 0`, as `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + I^{cand} ℓ^{1/4} + c₂ ℓ^{1/3} + O(ℓ^{3/5}).                                (P.1)

**Corollary P′ (no `ℓ^{1/2}` term).** If `ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + eℓ^{1/2} + o(ℓ^{1/2})`,
then `e = 0`. (Indeed `ℓ^{3/5} = o(ℓ^{1/2})`.)

**What is not claimed.**
- Nothing about the elder or rejected densities beyond #229. Lemma U is not proved for the elder kernel (Remark 3), and
  the Monte Carlo of #216 suggests that the elder and rejected densities carry further terms that the adjacent-pair
  density does not (Remark 4).
- No sharpness of `3/5`. The ledger's remaining terms are `ρ³ + ℓ²ρ^{−7} + ℓρ^{−2}` at the split `ρ = ℓ^{1/5}`, and
  `ℓ^{2/3}` from the fold-scale part of Lemma U (Remark 2).
- No certified numerical value of `I^{cand}` or `B_{d,L}` (those of `c`, `c₂` are #223's); no uniformity in `d` or `L`;
  no finite-radius band.
- Nothing beyond the existential scope of [R], [P], [Z], #191, #198, #207 and #218.

## 1. Birth integration, parity and reflection

**Rows.** [R] §2's rows at the pins `x_M := −r/2` and `x_S := r/2` on the axis `u` are `(f(x_M) + f(x_S))/2`,
`(f(x_S) − f(x_M))/r`, `(f_x(x_S) − f_x(x_M))/r`, `T_r := (6/r²)[f_x(x_M) + f_x(x_S) − 2(f(x_S) − f(x_M))/r]` and the
transverse rows `(f_{y_j}(x_M) + f_{y_j}(x_S))/2`, `(f_{y_j}(x_S) − f_{y_j}(x_M))/r`, with target
`(b − kr³/2, −kr², 0, 12k, 0, …, 0)` and Jacobian factor `12`. Replace the second row by
`(f_x(x_M) + f_x(x_S))/2 = (f(x_S) − f(x_M))/r + r²T_r/12`. This adds a multiple of `T_r` to it (determinant `1`), and
its target is `−kr² + r²·12k/12 = 0` (control Q2). The first row is the midpoint height `b′ = b − kr³/2`. What remains is

    V_r := ((∇f(x_M) + ∇f(x_S))/2, (∇f(x_S) − ∇f(x_M))/r, T_r) ∈ R^{2d+1},        target v(k) := (0_d, 0_d, 12k).        (1.1)

For `k ∈ R` write `p_{V_r}` for the density of `V_r` and `Q̄_{r,k}` for the law of the field given `V_r = v(k)` (Gaussian
regression). Put `f_e(z) := (f(z) + f(−z))/2` and `f_o(z) := (f(z) − f(−z))/2`.

**Lemma R (birth integration, parity, reflection).** For `0 < r ≤ r_0^*`, `k ∈ R` and `u ∈ S^{d−1}`:
- (R.1) *Birth integration.* For `k ≥ 0`, `𝐓_r(k, u) = 12p_{V_r}(v(k))E_{Q̄_{r,k}}[r^{−2}Π 1_{typed}]` with
  `Π := −det K_M det K_S`. The fixed-cone surrogate `𝐒_r(k, u) := 12p_{V_r}(v(k))E_{Q̄_{r,k}}[r^{−2}Π1{A<0}]`, defined for
  `k ∈ R`, equals `∫_R 12π_r(v_r)E_Q[r^{−2}Π1{A<0}] db` for `k ≥ 0`.
- (R.2) *Parity.* Under `Q̄_{r,k}` the fields `f_e` and `f_o` are independent; `f_e` is centred and its law does not depend
  on `k`; `f_o` has a covariance independent of `k` and a mean linear in `k`. So the even jets have a centred law that does
  not depend on `k`, the odd jets have means `k·w` (`w` fixed) and a covariance independent of `k`, and the two families
  are independent. Moreover `p_{V_r}(v(−k)) = p_{V_r}(v(k))`.
- (R.3) *Reflection.* For `f̃(z) := f(−z)`, `V_r(f̃) = 𝔭V_r(f)`, where `𝔭` negates the first and last blocks. So
  `f ~ Q̄_{r,k}` implies `f̃ ~ Q̄_{r,−k}`. The jets of `f̃` at `0` are those of `f` with `𝒫` applied; `Π(f̃) = Π(f)` and
  `A(f̃) = A(f)`; typed and anti-typed configurations are exchanged.
- (R.4) *Evenness in `r`.* The rows of `V_r`, extended to `0 < |r| ≤ r_0^*` by the same formulas, are even in `r`, and
  `V_0 := lim_{r→0}V_r = (∇f(0), ∂_u∇f(0), ∂_u³f(0))`. For every finite vector `J₀` of free jets at `0`, the covariance of
  `(V_r, J₀)` is a smooth even function of `r ∈ [−r_0^*, r_0^*]`, uniformly nondegenerate (also in `u`). Hence
  `p_{V_r}(v(k))` and the `Q̄_{r,k}`-law of `J₀` (mean and covariance) are smooth even functions of `r`; at `r = 0` the law is
  the conditional law given `V_0 = v(k)`. Pathwise, `Π` is even in `r`.

*Proof.* (R.1) In [R]'s Kac–Rice representation, `π_r(v_r)E_Q[·]` is the density of [R]'s pin vector at its target times
the conditional expectation. The row change is unimodular, with the target computed above, so this equals
`p_{(b′,V_r)}(b′, v(k))E[· | b′, V_r = v(k)]`. Integrating over `b′ ∈ R` gives `p_{V_r}(v(k))E[· | V_r = v(k)]`: by Tonelli
for `𝐓_r`, whose integrand is nonnegative, and by Fubini for `𝐒_r`, whose integrand is absolutely integrable.
(R.2) `Cov(f(z) + f(−z), f(w) − f(−w)) = 0` because the covariance is even, so the Gaussian fields `f_e`, `f_o` are
independent. Since `x_M = −x_S`, the average gradient is `∇f_o(x_S)`, and `T_r` is a functional of `f_o` (it is built from
`f_x(x_M) + f_x(x_S) = 2∂_xf_o(x_S)` and `f(x_S) − f(x_M) = 2f_o(x_S)`), while the gradient difference is `2∇f_e(x_S)/r`.
So `V_r = v(k)` conditions `f_e` on a zero target and `f_o` on a target linear in `k`, and Gaussian regression gives means
linear in the targets and covariances that do not depend on them. Jets of even order at `0` are functionals of `f_e`,
those of odd order of `f_o`. Finally the law of `V_r` is invariant under `𝔭` by (R.3), and `𝔭v(k) = v(−k)`.
(R.3) `∇f̃(z) = −∇f(−z)` and `D²f̃(z) = D²f(−z)`. So the average gradient and `T_r` change sign, the gradient difference
does not, and the two endpoint Hessians are exchanged; `Π` is symmetric in them, and `A(f̃) = ∇_Θ²f(0)`. The
unconditioned field is invariant in law under `z ↦ −z`, and Gaussian regression is equivariant under the linear
isomorphism `𝔭`. Exchanging the endpoint Hessians exchanges the two index conditions, that is, typed and anti-typed pairs.
(R.4) Each row is unchanged under `r ↦ −r`: the endpoints are exchanged and every rule is centred. Taylor's formula gives
the limits ([R] §2: `T_r = f_xxx(0) + (r²/40)f₅ + O(r⁴)`). The covariances are centred difference quotients of
derivatives of the smooth covariance function, hence smooth and even in `r`. For each `r ∈ [0, r_0^*]` and frame they are
nondegenerate by [P] §2 (distinct derivative functionals at distinct sites, or distinct jets at one point, are linearly
independent), as in #218 Step F1, and uniformly so by compactness. `Π = −det H(x_M) det H(x_S)/r²` is symmetric under
the exchange `r ↦ −r`; #191 Lemma E Step 3 records this as `det H_M(−r) = det H_S(r)`. ∎

The birth-integrated basis (1.1), with its evenness in `r` and the independence of the odd and even families, is also the
one Math- #232 §1 uses; nothing here depends on #232. The typed indicator is not even in `r` or `k`: both `r ↦ −r` and
the reflection exchange it with the anti-typed one.

## 2. The product and its second coefficient

With the jets of §0 put `Δ_B := D det(A)[B] = tr(A^♯B)`, `Δ_C := tr(A^♯C)`, `Δ_BB := D²det(A)[B, B]` and
`A^♯_B := D adj(A)[B]` (polynomials, defined for singular `A`), and

    U := Y′ + 3kΔ_B,
    V := (3k/4)(Δ_C + Δ_BB) + (f₄/24)Δ_B + (f₅/120)Δ − (1/12)γᵀA^♯η − (1/8)γᵀA^♯_Bγ.                                (2.1)

Write `V = V_o + kV_e` with `V_e := (3/4)(Δ_C + Δ_BB)`; `V_e` is even and `V_o` is odd under `𝒫`. Let `T` be #218 §1's
dominating variable. Under `Q̄_{r,k}`, for `k ∈ R`, `E[T^p] ≤ C_p(1 + |k|)^p`: mix #218's bound `C_p(1 + |b′| + |k|)^p`
over the conditional law of the midpoint height `b′ = f_e(x_S)`, which is centred Gaussian and does not depend on `k`
(Lemma R (R.2)). #218 states its bound for `k ≥ 0`; the Gaussian regression behind it is linear in the targets, so for
signed `k` it holds with `|k|`. Likewise, for a finite jet vector `J₀` with uniformly invertible covariance, (1.2) gives
`E[T^p | J₀] ≤ C_p(1 + |k| + |J₀|)^p`. For `k ≥ 0` these read `1 + k`, as written where only `k ≥ 0` occurs.

**Lemma Π.** Pathwise,

    det K_M = −6kΔ + rU − r²V + O(r³(1 + |k|)T^N),    det K_S = 6kΔ + rU + r²V + O(r³(1 + |k|)T^N),
    Π = 36k²Δ² + r²(12kΔV − U²) + O(r⁴(1 + |k|)^N T^N).                                                           (2.2)

Under `(k, jets) ↦ (−k, 𝒫jets)`, `Δ`, `Y′` and `U` are invariant and `V` changes sign. At fixed free jets, `det K_M` and
`det K_S` are affine in `k`. This is a statement about the pinned polynomial fields of the proof, not about the laws
`Q̄_{r,k}` at different `k`: under those, the odd free jets have means `k·w` (Lemma R (R.2)), and these mean shifts are
kept wherever they matter (Step U2 (b)(ii)).

*Proof.* By #218 Step F1, `Π` equals a polynomial `Φ(J′; r, k)` in the free jets `J′` up to `O(r⁴T^{n₀})`, and the
coefficients of `Φ` are identities of polynomials, which may be read off on exactly pinned polynomial fields. On those
fields, with the height row pinned at the midpoint `b′`, every pinned jet is an even polynomial in `r` (Lemma R (R.4);
with [R]'s row at fixed `b`, `f(0)` would carry a term `−kr³/2`, which does not enter the Hessians). So `Π` is even in `r`,
and `Φ` has no odd powers of `r`. The pins give `f_xx(0) = −r²f₄/24 + O(r⁴)`, `f_xxx(0) = 12k − r²f₅/40 + O(r⁴)` and
`∇_yf_x(0) = −r²η/24 + O(r⁴)`. Expanding `α_i = f_xx(x_i)/r`, `β_i = ∇_yf_x(x_i)/r` and `A_i = ∇_Θ²f(x_i)` and using
`det K_i = α_i det A_i − rβ_iᵀadj(A_i)β_i` gives the first two lines; their product gives (2.2), the `r`-odd terms
cancelling. At fixed free jets only `α_i` depends on `k`, affinely, so there `det K_i` is affine in `k`. The parity
statement is read off (2.1):
`B`, `γ`, `f₅` are odd and `A`, `C`, `η`, `f₄` even, so `Δ_B` and `A^♯_B` are odd and `Δ_BB` (quadratic in `B`) is even.
Control Q3 checks (2.2) exactly on fourteen pinned polynomial fields in `d = 1, 2, 3, 4`, with general free jets; control
Q2 checks the evenness, the reflection and the affinity in `k` at fixed free jets. ∎

(2.2) is #232's (2.3) (`W₂ = 12kΔV − U²`, with remainder `O(r³)` there), obtained independently here; the absence of the
`r³` term is the pathwise evenness of Lemma R (R.4).

**Lemma K (the surrogate; `𝐀₂` is even in `k`).** There are `C, c, N` such that for `0 < r ≤ r_0^*`, `k ∈ R` and `u`,

    r²𝐒_r(k, u) = 𝐀_0(k, u) + r²𝐀₂(k, u) + ϱ_S,        |ϱ_S| ≤ C r⁴ (1 + |k|)^N e^{−ck²},                          (K.1)

where `𝐀_0` and `𝐀₂` are smooth even functions of `k ∈ R`, equal for `k ≥ 0` to `∫A_0(b, k, u) db` and `∫A₂(b, k, u) db`.
In particular `|𝐀₂(k, u) − 𝐀₂(0, u)| ≤ Ck²` for all `k ≥ 0`, uniformly in `u`.

*Proof.* Condition on `A`. Given `(V_r, A) = (v(k), A)`, the entries of the Hessians at `x_M` and `x_S` are jointly Gaussian,
with means affine in `(k, A)` and a covariance independent of `(k, A)` and smooth in `r`: `(V_r, A)` is uniformly
nondegenerate (Lemma R (R.4) with `J₀ ⊃ A`), and the covariances of the endpoint Hessian entries with `(V_r, A)` and
with each other are smooth in `r` by the argument of (R.4). So
`Ψ(r; k, A) := E[−det H_M det H_S | A, V_r = v(k)]` is a polynomial in `(k, A)` whose coefficients are smooth functions of
`r`, even because `r ↦ −r` exchanges the endpoints and preserves the product. Pathwise `−det H_M det H_S = r²Π`, so `Ψ`
vanishes at `r = 0`, and `Ψ = r²Ψ̃` with `Ψ̃(r; k, A) = E[Π | A, V_r = v(k)]` smooth and even in `r`. Hence

    r²𝐒_r(k, u) = 12 ∫_{A<0} p_{(V_r, A)}(v(k), A) Ψ̃(r; k, A) dA

is smooth and even in `r`, with fourth `r`-derivative bounded by `C(1 + |k|)^Ne^{−ck²}` uniformly in `u` (the frames form a
compact set); this gives (K.1). At `r = 0` it is `12p_{V_0}(v(k))·36k²E_{Q̄_{0,k}}[Δ²1{A<0}]`, which is `∫A_0 db` for `k ≥ 0`
(disintegrate in `b′` as in (R.1)). By #218's surrogate remark after Lemma F (through Step F3), at fixed `b` the surrogate
is `A_0 + r²A₂ + O(r³(1 + k)²P^Ne^{−c(b²+k²)})`. Integrating in `b` and comparing with (K.1) identifies the `r²`-coefficient
as `∫A₂ db`; the `r³` terms at fixed `b` (the birth shift `b ↦ b′` and #218's `r³Φ₃`) disappear after the `b`-integral, which
is even in `r`. Evenness in `k`: by Lemma R (R.2)–(R.3), `r²𝐒_r(−k, u) = r²𝐒_r(k, u)`. Finally `∂_k𝐀₂(0, u) = 0`,
`sup_{|k|≤1, u}|∂_k²𝐀₂| < ∞`, and `|𝐀₂(k)| + |𝐀₂(0)| ≤ C` for `k ≥ 1`. ∎

(For the Gaussian kernel, control Q4 computes exactly, in `d = 1, 2, 3`, the `A`-integrand `H(k, A)` of the birth-integrated
`r²` coefficient (#232 (3.2)): `H = h₀ + h₂k² + h₄k⁴`, with no odd powers, and the density exponent is `a = 12`. This is
#232's Theorem J; the `d = 1, 2` polynomials agree with its §4.)

## 3. Layer tools

Throughout, `X := Y² − 36κ²Δ²` for a cusp variable `Y ∈ {Y′, U}`, and the *layer* is `{A < 0, X > 0} = {A < 0, |Y| > 6κ|Δ|}`.

**Lemma D′ (bounded density of the determinant).** Under the hypothesis of #218 Lemma D, for every interval `I ⊂ R`,
`E[(1 + ‖G‖)^n 1{det G ∈ I}] ≤ C(1 + |μ|)^{n′}|I|`.

*Proof.* #218's proof of Lemma D's second bound, with `(−ε, ε)` replaced by `I`: on `{det G ∈ I}`, an eigenvalue `λ_{i*}`
of least modulus lies in an interval of length `|I|/D`, `D := ∏_{j≠i*}|λ_j|`, and the Vandermonde factor satisfies
`|𝒱(λ)| ≤ 2^{m−1}D|𝒱′|`; `D` cancels. ∎

**Lemma D″ (two small eigenvalues).** Let `m ≥ 2`, let `G` be as in #218 Lemma D, and let `D_G` be the product of the
`m − 1` largest eigenvalue moduli of `G`. Then for `0 < ε ≤ 1`, `E[(1 + ‖G‖)^n 1{D_G < ε}] ≤ C(1 + |μ|)^{n′}ε²`.

*Proof.* Use Weyl coordinates, as in #218's proof of Lemma D, with the eigenvalues ordered by modulus,
`x₁ = |λ_(1)| ≤ x₂ = |λ_(2)| ≤ … ≤ x_m`, so that `D_G = x₂⋯x_m`. Since `|λ_(1) − λ_(2)| ≤ 2x₂` and `|λ_(i) − λ_(j)| ≤ 2x_j`
for `i ≤ 2 < j`, the Vandermonde factor is `|𝒱(λ)| ≤ 2^{2m−3}x₂∏_{j≥3}x_j²|𝒱″|`, where `𝒱″` is the Vandermonde factor of
`λ_(3), …, λ_(m)`. Integrating `λ_(1)` over `[−x₂, x₂]` gives at most `2^{2m−2}D_G²|𝒱″| ≤ 2^{2m−2}ε²|𝒱″|` on `{D_G < ε}`.
Then `λ_(2)` ranges over an interval of length `≤ 2x₃` (of length `≤ 2ε` if `m = 2`), and the remaining integral, with
the Gaussian weight, is `≤ C(1 + |μ|)^{n′}`. ∎

**Lemma Λ₀ (layer probability).** Consider a Gaussian law of the jets under which `A` is centred, with covariance in a
fixed compact set of positive definite matrices, and the other jets have, given `A`, means affine in `(A, k)` with bounded
coefficients and bounded covariances. Examples are `Q̄_{r,k}` for `0 ≤ r ≤ r_0^*` and `k ≥ 0` (Lemma R (R.2), (R.4)) and the
linear interpolation of the means and covariances of two such laws. For nonnegative functions `p` and `ω` of the jets
that are bounded by polynomials, and `κ > 0`,

    E[p 1{A < 0, |Y| ≥ 6κ|Δ| − ω}] ≤ C(1 + k)^N / (1 + κ),

with `C` and `N` depending on `p` and `ω` but not on `κ`, `k`, `r` or `u`.

*Proof.* For `κ ≤ 1` bound the indicator by `1`. For `κ ≥ 1` the event lies in `{|Δ| ≤ (|Y| + ω)/(6κ)}`. Given `A`, the
other jets are Gaussian with means affine in `(A, k)`, so `P(|Y| + ω ≥ t | A) ≤ C_pt^{−p}(1 + k + ‖A‖)^{n_p}`. Dyadic
layers of `|Y| + ω` and Lemma D give the bound, as in #218's proof of Lemma O. ∎

**Lemma Λ (the gap inside the layer).** Let `κ > 0` be a parameter and, for `s ∈ R`,
`Λ(s) := 12p_{V_0}(v(s))E_{Q̄_{0,s}}[(U_s² − 36κ²Δ²)₊1{A<0}]`, where `U_s := Y′ + 3sΔ_B`. Then `Λ` is even, and for
`0 ≤ k ≤ 1`, with `C` independent of `κ`, `k` and `u`,

    |Λ(k) − Λ(0)| ≤ C k² / (1 + κ).                                                                              (Λ.1)

*Proof.* *Evenness:* by Lemma R (R.2)–(R.3), `U_{−s}(𝒫·) = U_s(·)`, `Δ(𝒫·) = Δ(·)` and `p_{V_0}(v(−s)) = p_{V_0}(v(s))`.

*Reduction.* `p_{V_0}(v(s)) = p_{V_0}(v(0))e^{−as²}`, with `a > 0` bounded above and below. Hence the density factor
contributes `|e^{−ak²} − 1|·12p_{V_0}(v(0))E_{Q̄_{0,k}}[(U_k² − 36κ²Δ²)₊1{A<0}]`, which is `≤ Ck²/(1 + κ)` by Lemma Λ₀.
By (R.2), under `Q̄_{0,s}` the free jets can be realized as `ζ₀ + s·w`, with `ζ₀ ~ Q̄_{0,0}` and `w` supported on the odd jets.
Then `U_s(ζ₀ + sw) = Y₀ + sY₁ + s²Y₂`, with `Y₀ := Y′(ζ₀)`, `Y₁ := 3tr(A^♯B₀) − w_γᵀA^♯γ₀/2` and
`Y₂ := 3tr(A^♯w_B) − w_γᵀA^♯w_γ/4`. Here `γ₀`, `B₀` are the odd jets of `ζ₀`, and `w_γ`, `w_B` are the components of `w`.
`Y₁` is odd, `Y₂` is even, and neither involves `f₄`. Since `Λ(s)e^{as²}` is even in `s`, it remains to bound

    E[½(φ(Y₀ + kY₁ + k²Y₂) + φ(Y₀ − kY₁ + k²Y₂)) − φ(Y₀)],        φ(y) := (y² − θ²)₊,  θ := 6κ|Δ|,  on {A < 0}.

*Integrate `f₄` first.* Given the other jets, `f₄` is Gaussian with mean `m₄`, linear in the other even jets, and a
variance `σ₄²` bounded above and below (a Schur complement; #218 Step F1). Write `Y₀ = (Δ/12)f₄ + β` with
`β := −γ₀ᵀA^♯γ₀/4`. Then `Φ(t) := E_{f₄}[φ(Y₀ + t)]` is `E[φ(Z + t)]` for `Z ~ N(μ_Z, σ_Z²)`, where `μ_Z := (Δ/12)m₄ + β`
and `σ_Z := |Δ|σ₄/12`. `φ` is convex, and as a distribution `φ″ = 2·1{|y| > θ} + 2θ(δ_{−θ} + δ_θ)`: `φ″ = 0` on
`|y| < θ`, `φ″ = 2` on `|y| > θ`, and `φ′` jumps by `2θ` at `±θ`. Hence `Φ` is convex and smooth, with

    Φ″(t) = 2P(|Z + t| > θ) + 2θ[p_Z(θ − t) + p_Z(−θ − t)],        θ p_Z(x) = (72κ/(√(2π)σ₄)) e^{−(x − μ_Z)²/(2σ_Z²)}.  (3.1)

(`Δ` cancels in the second identity.) In particular `Φ″ ≤ 2 + 288κ/(√(2π)σ₄) ≤ C(1 + κ)` (two bumps). Write the quantity to be bounded
as `E[Φ(t₀) − Φ(0)] + E[½(Φ(t₀ + h) + Φ(t₀ − h)) − Φ(t₀)]`, with `t₀ := k²Y₂` and `h := kY₁`.

*The case `κ ≤ 1`.* `|Φ′(t)| ≤ 2E_{f₄}|Z + t|`, and the second difference is at most `h²·sup Φ″ ≤ Ch²`. So the quantity is
`O(k²)`.

*The case `κ ≥ 1`.*
- *First part.* `|Φ(t₀) − Φ(0)| ≤ |t₀|·sup_{|t|≤|t₀|}|Φ′(t)|` and `|Φ′(t)| ≤ 2E_{f₄}[(|Z| + |t₀|)1{|Z| ≥ θ − |t₀|}]`. By
  Lemma Λ₀ (with `ω = |t₀|`) this part is `≤ Ck²κ^{−1}`.
- *Second part, bulk.* The symmetric second difference of a convex function is `½∫_{−|h|}^{|h|}(|h| − |τ|)Φ″(t₀ + τ)dτ`.
  The first term of (3.1) contributes `≤ h²P_{f₄}(|Z| ≥ θ − |t₀| − |h|)`, which is `≤ Ck²κ^{−1}` by Lemma Λ₀ (with
  `ω = |t₀| + |h|`).
- *Second part, kink.* By (3.1) the second term contributes
  `K := (72κ/(√(2π)σ₄))∫(|h| − |τ|)₊ Σ_± e^{−g_±²/(2σ_Z²)} dτ`, where `g_± := ±θ − μ_Z − t₀ − τ`. Note that `K ≤ Cκh²`.
  - *Coordinates.* Use Weyl coordinates for `A`, as in Lemma D′: `λ` is an eigenvalue of least modulus and `D` the product
    of the other moduli (`D := 1` if `m = 1`), so `|Δ| = |λ|D`, and `λ < 0` on `{A < 0}`. In the Weyl-coordinate
    integral, fix the eigenvectors `O`, the other eigenvalues `λ′` and the free jets `𝐠` other than `A` and `f₄`, and
    use the *unnormalized* slice `ρ(λ)dλ := c_m q_{A|𝐠}(O diag(λ, λ′)Oᵀ)|𝒱(λ, λ′)|dλ`, to be integrated afterwards over
    `dλ′ dO dP_𝐠`. Here `q_{A|𝐠}` is the Gaussian density of `A` given `𝐠` on the symmetric matrices and `𝒱` the
    Vandermonde factor. (A normalized conditional density of `λ` would carry the inverse of the slice integral, which is
    not bounded uniformly; it is not used.) Then `λ` ranges over `[−x₂, 0)`, where `x₂` is the second smallest modulus
    (over `(−∞, 0)` if `m = 1`), and `ρ(λ) ≤ C2^{m−1}D|𝒱′|p̄`, where `𝒱′` is the Vandermonde factor of the other
    eigenvalues and `p̄ := sup_λ q_{A|𝐠}(O diag(λ, λ′)Oᵀ)`.
  - *Dependence on `λ`.* `θ = −6κDλ` is linear in `λ`; `A^♯`, `β`, `m₄`, `Y₁` and `Y₂` are affine; `μ_Z` is quadratic. Let
    `P := C₀(1 + ‖A‖ + |𝐠|)^{N₀}`, with `C₀`, `N₀` chosen so that `|μ_Z′| + |t₀′| ≤ P/2` and `|m₄| ≤ P` on the range of `λ`.
    For `m ≥ 2`, `‖A‖ = x_m` does not depend on `λ`; for `m = 1` the conditions below cut out an interval of `λ`.
  - *Main set* `𝔐 := {P ≤ κD and P ≤ κ}`. Here `|g_±′| ≥ 6κD − P/2 ≥ 3κD`, so each `g_±` is monotone in `λ`, and
    `|Δm₄|/12 ≤ θ/72`. Where `|g| ≥ θ/2`, `e^{−g²/(2σ_Z²)} ≤ e^{−648κ²/σ₄²}`, and the contribution is
    `≤ Cκh²e^{−648κ²/σ₄²} ≤ Ch²κ^{−1}`. Where `|g| < θ/2`, `|β + t₀ + τ| > θ/2 − θ/72 > θ/4`. On the support
    `|τ| < |h(λ)|` of the weight, `|β + t₀ + τ| ≤ M₀ := sup_λ(|β| + |t₀| + |h|)`, a polynomial in `(‖A‖, 𝐠)` that does
    not depend on `λ`. (For `m = 1`, `adj A = 1`, so `β`, `Y₁` and `Y₂`, hence `t₀` and `h`, do not depend on `λ`, and
    `M₀` and `H` below are finite although `λ` ranges over `(−∞, 0)`.) So `|λ| < M₀/(1.5κD)`. Hence
    `σ_Z < σ̄ := M₀σ₄/(18κ)` there. Bound `(|h| − |τ|)₊ ≤ (H − |τ|)₊` with `H := sup_λ|h|`, and change variables `λ ↦ g`
    (`|dλ/dg| ≤ 1/(3κD)`): `∫e^{−g²/(2σ̄²)}ρ dλ ≤ C D|𝒱′|p̄·√(2π)σ̄/(3κD) = C|𝒱′|p̄M₀σ₄/κ²`. With the prefactor and
    `∫(H − |τ|)₊dτ = H²` this gives `≤ C|𝒱′|p̄M₀H²/κ`, and integrating over `dλ′ dO dP_𝐠` gives
    `E[K1_𝔐] ≤ Ck²(1 + k)^Nκ^{−1}`. No largeness of `κ` is used beyond `κ ≥ 1`.
  - *Exceptional set* `𝔐^c ⊂ {D < P/κ} ∪ {P > κ}`. Use `K ≤ Cκh²`. For `m ≥ 2`, Lemma D″, applied given `𝐠` in dyadic
    layers of `‖A‖`, gives `E[h²1{D < P/κ}] ≤ Ck²κ^{−2}`. For `m = 1`, `D = 1` and this set is `{P > κ}`. By Markov,
    `E[h²1{P > κ}] ≤ C_pk²κ^{−p}`. So `E[K1_{𝔐^c}] ≤ Ck²κ^{−1}`.

Summing gives (Λ.1). ∎

## 4. A uniform two-scale kernel

**Lemma U.** There are `C, r₃ > 0` such that for `0 < r ≤ r₃`, `k ≥ r²` (that is, `κ ≥ r`) and `u ∈ S^{d−1}`,

    |𝐓_r(k, u) − r^{−2}𝐀_0(k, u) − [𝐀₂(k, u) − 𝐀₂(0, u)] − 𝓐(k/r, u)| ≤ C(r² + r min(k, 1/k)).                  (U.1)

*Proof.* Terms evaluated at the target `v(k)` carry the factor `p_{V_r}(v(k)) ≤ Ce^{−ck²}`, which absorbs polynomial growth
in `k`. The zero-gap terms `Λ(0)`, `𝐀₂(0)` and `𝓐` do not carry it; they are compared directly.

*Step U1 (the surrogate).* By Lemma K, `𝐒_r = r^{−2}𝐀_0 + 𝐀₂ + O(r²(1 + k)^Ne^{−ck²})`.

*Step U2 (the typed kernel is the surrogate plus the layer).* Work under `Q̄ := Q̄_{r,k}`, with `T` as in §2,
`m_i := det K_i/r` and `s := (−1)^m`. Put `X := U² − 36κ²Δ²` and `ε := −r^{−2}Π − X`. By Lemma Π, `ε = −12kΔV + ε₂` with
`|ε₂| ≤ Cr²(1 + k)^NT^N`. By (R.1),

    𝐓_r − 𝐒_r = 12p_{V_r}(v(k)) (E_Q̄[X₊1{A<0}] + E_Q̄[G]),        G := r^{−2}Π(1_{typed} − 1{A<0}) − X₊1{A<0}.

Split according to #218 Step C1's cases, with `A = ∇_Θ²f(0)` in place of #218's `A_0`. Step C1 uses `‖A_i − A‖ ≤ rT` for
the endpoint matrices `A_i := ∇_Θ²f(x_i)`, which holds since `‖A_i − A‖ ≤ (r/2)‖f‖_{C³} ≤ rT`, and the expansions of
`det K_i`, which Lemma Π supplies with `A` in place of `A_0`.
- *Case 2* (`λ_max(A) > rT`): the pair is not typed and `A ≮ 0`, so `G = 0`.
- *Case 3* (`|λ_max(A)| ≤ rT`). Here `|Δ| ≤ rT^m`, and #218's Case 3 gives `|r^{−2}Π|1_{typed} = |m_Mm_S|1_{typed} ≤
  C(k + r(1 + k))²T^N`. The surrogate weight itself is not small here (`−r^{−2}Π ≈ U²`, and `U` is not small when `Δ` is),
  so compare with the layer integrand. On `{A < 0}`, `r^{−2}Π(1_{typed} − 1) − X₊ = r^{−2}Π1_{typed} − (−X)₊ + ε`
  (control Q5), with `(−X)₊ ≤ 36κ²Δ² ≤ 36k²T^{2m}` and `|ε| ≤ C(k|Δ| + r²)(1 + k)^NT^N ≤ C(kr + r²)(1 + k)^NT^N`. On
  `{0 < λ_max(A) ≤ rT}` only `r^{−2}Π1_{typed}` is present. So `|G| ≤ C(k + r)²(1 + k)^NT^N` on Case 3. Its probability,
  with the weight `T^N`, is `≤ Cr(1 + k)^N` (Lemma D with dyadic layers in `T`, and (1.2) with `J₀ = A`). So Case 3
  contributes `O(r(k + r)²(1 + k)^N)`.
- *Case 1* (`λ_max(A) < −rT`). Here `A, A_M, A_S < 0`, and by Haynsworth's inertia additivity (#218 Step C1; #191 Step 4)
  the pair is typed iff `s m_M < 0 < s m_S`. Since `r^{−2}Π = −m_Mm_S`, `r^{−2}Π(1_{typed} − 1) = (m_Mm_S)₊ −
  |m_Mm_S|1_{anti}`, where `anti := {s m_M > 0 > s m_S}` (control Q5). With `m_Mm_S = X + ε`,

      G = [(X + ε)₊ − X₊ − ε1{X>0}] + ε1{X>0} − |m_Mm_S|1_{anti}.

  - (a) The bracket is at most `|ε|1{|X| ≤ |ε|}` in modulus (control Q5). On the dyadic layer `{T ∈ [2^j, 2^{j+1})}`,
    `|ε| ≤ ε̄_j := C(k|Δ| + r²)(1 + k)^N2^{(j+1)N}`, which does not involve `f₄`; and by (1.2), with `J₀` the finite jet
    vector, `P(T ≥ 2^j | J₀) ≤ C_p2^{−jp}(1 + k + |J₀|)^p`. Integrate `f₄` given the other jets. `U` is affine in `f₄` with
    slope `Δ/12`, and `f₄` has a bounded conditional density (#218 Step F1), also after multiplication by the polynomial
    weight `(1 + k + |J₀|)^p`, which contains `|f₄|^p`. So `{|X| ≤ ε̄_j}` has conditional probability
    `≤ C min(1, ε̄_j/(κΔ²))` when `36κ²Δ² > 2ε̄_j`, and `≤ C min(1, ε̄_j^{1/2}/|Δ|)` otherwise.
    - On the first set `κ|Δ| ≥ cr`, and there `E[ε̄_j min(1, ε̄_j/(κΔ²))] ≤ C2^{2jN}(1 + k)^N(kr + r³log(2/r))` (use
      `k/κ = r` and Lemma D in dyadic layers).
    - The second set needs `|Δ| ≤ C2^{jN}r/κ`, which has probability `≤ C2^{jN}r/κ`; there the cost is
      `≤ ε̄_j ≤ C2^{jN}(1 + k)^Nr²`. Since `κ ≥ r`, `r³/κ ≤ r²`.

    Summing over `j`, (a) is `O((1 + k)^N(kr + r²))`.
  - (b) `ε1{X>0}`. First replace `1_{Case 1}` by `1{A<0}`, at cost `≤ E[|ε|1_{Case 3}] ≤ Cr(kr + r²)(1 + k)^N`. The `ε₂`
    part is `≤ Cr²(1 + k)^N/(1 + κ)` by (1.2) and Lemma Λ₀. What remains, `−12kE[ΔV1{X>0}1{A<0}]`, is a Gaussian expectation
    of finitely many free jets. By (R.2), their law has a covariance independent of `k` and odd means `k·w`.
    - `12k²|E[ΔV_e1{X>0}1{A<0}]|`: on `{X > 0}`, `|Δ| < |U|/(6κ)`, so by Lemma Λ₀ this is
      `≤ Ck²(1 + k)^N/(1 + κ)² ≤ C(1 + k)^Nr²`.
    - `12kE[ΔV_o1{X>0}1{A<0}]`, in three steps:
      - (i) With the law at `k = 0` (which is `𝒫`-invariant by (R.2)) and `Y′` in place of `U` in `X`, the expectation
        vanishes: `ΔV_o` is odd and `1{Y′² > 36κ²Δ²}1{A<0}` is even.
      - (ii) Moving the odd mean from `0` to `k·w` costs, by the Gaussian score (no derivative of an indicator is
        taken), `≤ Ck·sup E[|ΔV_o|(1 + |jets|)1{|Y′| > 6κ|Δ|}1{A<0}] ≤ Ck(1 + k)^N/(1 + κ)²`. On the layer
        `|Δ| < |Y′|/(6κ)`, so Lemma Λ₀ applies along the interpolation.
      - (iii) Replacing `Y′` by `U` in the indicator (`U − Y′ = a := 3kΔ_B`). The two indicators differ only where `Y′`
        lies in one of the two one-sided threshold-crossing strips between `±6κ|Δ|` and `±6κ|Δ| − a`, each of length
        `|a|` and centred at `±6κ|Δ| − a/2`. (If `|a| > 12κ|Δ|`, the strips overlap and the difference set is smaller;
        only this containment is used.) Since `Y′ = (Δ/12)f₄ + β` with `β := −γᵀA^♯γ/4`, this is `f₄` in two windows `W`
        of total length `≤ 72k|Δ_B|/|Δ|`, centred at `f₄ = 12(±6κ|Δ| − a/2 − β)/Δ`. (Windows centred at the unshifted
        points `12(±6κ|Δ| − β)/Δ` would need total length `144k|Δ_B|/|Δ|`; the bounds below hold with either.) Write
        `ΔV_o = Δ(a₁f₄ + a₀)` with `a₁ = Δ_B/24` and `a₀` free of `f₄`. Since `sup_x(1 + |x|)p_{f₄}(x) ≤ C(1 + |m₄|)`,
        the factor `Δ` cancels the `1/|Δ|` of the window length: `E_{f₄}[|ΔV_o|1_W] ≤ Ck(1 + |m₄|)(|a₁| + |a₀|)|Δ_B|`,
        uniformly in `Δ`. For `k ≤ 1` and
        `|Δ| > (|β| + 3|Δ_B|)/(3κ)`, on `W` we have `|Δf₄|/12 = |Y′ − β| ≥ 6κ|Δ| − 3|Δ_B| − |β| > 3κ|Δ|`, so
        `W ⊂ {|f₄| > 36κ}`. There `(1 + |x|)p_{f₄}(x) ≤ C(1 + |m₄|)^Nκ^{−N}`, and this part costs `O(kκ^{−N})`. The
        complementary set `{|Δ| ≤ (|β| + 3|Δ_B|)/(3κ)}` has probability `≤ C/κ`, with the polynomial weights (Lemma D in
        dyadic layers of `|β| + |Δ_B|`). So this step costs `≤ Ck(1 + k)^N/(1 + κ)`. For `k > 1`, Lemma Λ₀ applied to
        each indicator gives `≤ C(1 + k)^N/(1 + κ)`, and the Gaussian factor absorbs the missing `k`.

      Hence `|12kE[ΔV_o1{X>0}1{A<0}]| ≤ Ck²(1 + k)^N/(1 + κ)`, and `k²/(1 + κ) = k²r/(k + r) ≤ kr`.

    In all, (b) is `O((1 + k)^N(kr + r²))`.
  - (c) *The anti-typed sliver.* By Lemma Π, `s m_S − s m_M = 12κ|Δ| + O(r(1 + k)T^N)`. On `anti` the left side is
    negative, so `|m_M| + |m_S| = −(s m_S − s m_M) ≤ Cr(1 + k)T^N`. Hence `|U| = |m_M + m_S|/2 + O(r²(1 + k)T^N) ≤
    Cr(1 + k)T^N`. Integrating `f₄`, then using Lemma D in layers, this event has probability `≤ Cr log(2/r)(1 + k)^N`.
    Its weight is `|m_Mm_S| ≤ Cr²(1 + k)^NT^N`, so (c) is `O(r³log(2/r)(1 + k)^N)`.

  Collecting, with the Gaussian factor (control Q6):
  - for `k ≤ 1`, `kr = r min(k, 1/k)` and `r(k + r)² ≤ 2kr + 2r²`;
  - for `k ≥ 1`, `(1 + k)^Ne^{−ck²}(kr + r²) ≤ C(r² + r/k)`.

  Hence `𝐓_r − 𝐒_r = 12p_{V_r}(v(k))E_{Q̄_{r,k}}[X₊1{A<0}] + O(r² + r min(k, 1/k))`, the main term being over all of
  `{A < 0}`.

*Step U3 (the layer across laws).* Let `L_r(k) := 12p_{V_r}(v(k))E_{Q̄_{r,k}}[X₊1{A<0}]`. Throughout, `κ = k/r` is a fixed
parameter of the weight.
- *`k ≥ 1`.* `L_r(k) ≤ Ce^{−ck²}(1 + k)^N/(1 + κ)` and `Λ(0) ≤ C/(1 + κ)` (Lemma Λ₀), so `|L_r(k) − Λ(0)| ≤ C/(1 + κ) ≤ Cr/k`.
- *`k ≤ 1`, from `r` to `0` at fixed `(k, κ)`.* `Λ(k)` is the same functional at `r = 0`. By Lemma R (R.4), the laws of the
  finitely many jets involved under `Q̄_{r,k}` and `Q̄_{0,k}` have means and covariances that differ by `O(r²(1 + k))`, and
  `p_{V_r}(v(k)) − p_{V_0}(v(k)) = O(r²)`. The Gaussian score along the linear interpolation, with Lemma Λ₀ applied to each
  interpolating law, gives `|L_r(k) − Λ(k)| ≤ Cr²/(1 + κ)`.
- *`k ≤ 1`, from `k` to `0` at `r = 0`.* By Lemma Λ, `|Λ(k) − Λ(0)| ≤ Ck²/(1 + κ) ≤ Ckr`.

*Step U4 (the identity).* By #218 (F.2) and #218 §0, `A₂(b, 0, u) = −12π_0E_0[Y²1{A<0} | b]` and
`(𝒜^{cand} − 𝒜^{con})(b, κ, u) = −12π_0E_0[min(Y², 36κ²Δ²)1{A<0} | b]`, with `π_0 = π_0(v_0(b, 0))`. Since
`y² − min(y², c²) = (y² − c²)₊` (control Q5), the difference is `12π_0E_0[(Y² − 36κ²Δ²)₊1{A<0} | b]`. The contact law at
`v_0(b, 0)` conditions `(f(0), V_0)` on `(b, v(0))`, and `Y = Y′` there. So integrating in `b` (as in (R.1)) gives
`Λ(0) = 𝓐(κ, u) − 𝐀₂(0, u)`.

Steps U1–U4 together give (U.1). ∎

At the cusp scale (`κ` fixed, `k = κr ≤ 1`, `r ≤ min(κ, r₃)`), (U.1) and Lemma K give, after the `b`-integral,
`𝐓_r − r^{−2}𝐀_0 = 𝓐(κ) + O((1 + κ)²r²)`. So the `O(r)` correction allowed by #218 Lemma C and #229 Lemma C⁺ vanishes. In
the fold regime (`k` fixed, `r → 0`), the layer `𝓐(κ) − 𝐀₂(0) = O(κ^{−1}) = O(r/k)` is the boundary layer of #218 (F.1),
now identified rather than bounded. That is how Lemma U resolves the matching pairs of #229 Remark 1.

## 5. Proof of Theorem P

Put `ρ := ℓ^{1/5}` and take `ℓ` so small that `ρ ≤ r₃` and `ρ < r_0 ≤ r_0^*`. By #191 (2.1) and #207 §7's decomposition of
`B_{d,L}`, as in #218 §4 with its two inner regions merged into one (`F + K`),

    ν_cand − cℓ^{−1/3} − B_{d,L} = ∫_0^ρ∫_S[𝐓_r(ℓ/r³, u) − r^{−2}𝐀_0(ℓ/r³, u)] dσ dr + J₂ + J₃ + J₄ + J₅,

with `J₂ = −∫_0^ρ∫∫r^{−2}A_r(b, 0, u)`, `J₃ = ∫_ρ^{r_0}∫∫r^{−2}[A_r(b, ℓ/r³, u) − A_r(b, 0, u)]`,
`J₄ = −∫_ρ^∞∫∫r^{−2}A_0` and `J₅ = ∫_{dist(0,y)≥r_0}∫(Ψ_ℓ^{cand} − Ψ_0)`.

*The main term.* For `r ≤ ρ`, `k = ℓ/r³ ≥ r²`, so Lemma U applies.
- `∫_0^ρ[𝐀₂(ℓ/r³) − 𝐀₂(0)]dr = (ℓ^{1/3}/3)∫_{ℓρ^{−3}}^∞[𝐀₂(k) − 𝐀₂(0)]k^{−4/3}dk`. By (0.1) of #218 this is `c₂ℓ^{1/3}`
  (after `∫dσ`) minus `(ℓ^{1/3}/3)∫_0^{ℓρ^{−3}}`, which is `O(ℓ^{1/3}(ℓρ^{−3})^{5/3}) = O(ℓ²ρ^{−5})` by Lemma K.
- `∫_0^ρ𝓐(ℓ/r⁴)dr = ℓ^{1/4}∫_0^{ρℓ^{−1/4}}𝓐(s^{−4})ds = I^{cand}ℓ^{1/4} − O(ℓ^{1/4}(ρℓ^{−1/4})^{−7}) =
  I^{cand}ℓ^{1/4} − O(ℓ²ρ^{−7})`. This uses `|𝒜^{cand} − 𝒜^{con}| ≤ Cκ²` (#218 §4) and the convergence at `s → 0`, where
  `𝓐 → 𝐀₂(0)`; `I^{cand} = ∫_S∫_0^∞𝓐(s^{−4}) ds dσ` (#207 §7).
- The error of (U.1) integrates to `C∫_0^ρ(r² + r min(ℓ/r³, r³/ℓ))dr ≤ C(ρ³ + (6/5)ℓ^{2/3})` (control Q1).

*The rest* (#218 §4, #207 §7, #198).
- `|J₂| ≤ Cρ³` (#198 (W.4)).
- `|J₃| ≤ C(ℓ²ρ^{−7} + ℓρ^{−2})` (#207 (7.1); here `k ≤ ℓρ^{−3} ≤ 1`).
- `0 ≤ −J₄ ≤ Cℓ²ρ^{−7}`.
- `|J₅| ≤ Cℓ` (#207 (7.2)).

*The ledger* (control Q1; exponents of `ℓ` at `ρ = ℓ^{1/5}`):

| Term | Source | Exponent |
|---|---|---|
| `ρ³` | the `r²` part of Lemma U; `J₂` | **3/5** |
| `ℓ²ρ^{−7}` | the cusp tail; `J₃`; `J₄` | **3/5** |
| `ℓρ^{−2}` | `J₃` | **3/5** |
| `ℓ^{2/3}` | the `r min(k, 1/k)` part of Lemma U (fold scale) | 2/3 |
| `ℓ²ρ^{−5}` | the finite part of `𝐀₂` | 1 |
| `ℓ` | `J₅` | 1 |

The least exponent is `3/5`. The split is optimal for this ledger, and it is exactly the edge `κ = r` of Lemma U's range.
This proves (P.1). ∎

(Lemma K's `O(k²)` is not needed for (P.1). With #218's `C¹` bound `𝐀₂(k) − 𝐀₂(0) = O(k)`, the finite-part row becomes
`ℓρ^{−2}`, again of exponent `3/5` (control Q1). Lemma K is used for the cusp-scale statement after Lemma U.)

## 6. Remarks

1. **The `ℓ^{1/2}` order.** #218 §0 ("Formally the next term is of order `ℓ^{1/2}`") and #229 anticipated an `ℓ^{1/2}` term.
   #229 §0 says the same; its Remark 1 says "formally `𝒜₃` produces the next term, of order `ℓ^{1/2}`", where `𝒜₃` is the
   `O(r)` correction of the cusp kernel. For the candidate density the term is absent. After the `b`-integral, the
   cusp-scale expansion of the candidate kernel has no `O(r)` term (Lemma U with Lemma K). The would-be term is
   `12κrΔV_o` in `r^{−2}Π` (Lemma Π), which is odd under `𝒫`, while the dependence of the law and of `U` on `k` is even
   (Lemmas R and Λ).
   - Reflection alone does not make the expansion even to all orders. It exchanges typed and anti-typed pairs, whose
     `O(r³log(2/r))` contribution (Step U2 (c)) is not expanded here.
   - #216's formal law (0.2) concerns the elder density, with remainder `O(ℓ^{1/2})`. Theorem P neither confirms nor
     contradicts it (Remark 3).
2. **What the method leaves.**
   - *The fold scale.* There `𝓐(κ) − 𝐀₂(0) − [𝐓_r − 𝐒_r]` is `O(r min(k, 1/k))`. This comes from the `k`-dependence of
     the layer coefficient (Lemma Λ) and from Step U2 (b), and it integrates to `O(ℓ^{2/3})`. It is plausibly the next
     term, but neither its non-vanishing nor the sharpness of Lemma Λ is proved. The referee's numerics support a nonzero
     `k²/κ` coefficient for the Gaussian kernel in `d = 2` (README, review record).
   - *What fixes `3/5`.* Three terms balance at `ρ = ℓ^{1/5}`:
     - `ρ³`, from the `r²` part of Lemma U and from `J₂`;
     - `ℓ²ρ^{−7}`, from the cusp tail, `J₃` and `J₄`;
     - `ℓρ^{−2}`, from `J₃` via #207 (7.1).

     They are fixed together with the cap `ρ ≤ ℓ^{1/5}`, which Lemma U's range `κ ≥ r` imposes. Sharpening the `r²` part of
     Lemma U alone would not change `3/5`.
   - *A route to `2/3` (not attempted).* An exponent `2/3` would follow from a version of Lemma U for `𝐓_r(k) − 𝐓_r(0)`
     with three properties:
     - it absorbs `J₂`;
     - it holds for all `k > 0`, so that `ρ` can be fixed;
     - its error is `O(r²min(1, κ) + r min(k, 1/k))`.

     With `ρ` fixed, the remaining terms are `O(ℓ^{3/4})`, `O(ℓ^{2/3})` and `O(ℓ)`.
3. **The elder density.**
   - *Formally.* The leading elder window `{|Y′| < 2κ|Δ|}` (#229 Remark 2) is `𝒫`-even, so formally the elder cusp kernel
     has no `O(r)` term either.
   - *Why the proof does not transfer.* Reflection does not make the elder kernel even in `k`, since it exchanges typed and
     anti-typed configurations. Lemma U is not available for the elder kernel: the elder decision's bad events (#220
     Lemma Q; #229 Lemma CE⁺: `κ²r^{3/2}`, `κ³r²`) are not uniform in the fold regime. The intermediate elder mass is also
     only known to be `O(ℓ^{4/9}log(1/ℓ))` (#229).
   - Theorem P says nothing new about `ν_eld` or `ρ_rej`.
4. **Numerical evidence** (exploration; project archive `V2_2/frontiers_candidate_parity_rate_20261001/exploration/`; not
   part of the proof).
   - *The cusp kernel's `O(r)` coefficient.* `d = 2`, Gaussian kernel.
     - *Method.* `r^{−2}A_r(b, κr)` was computed by exact Gaussian conditioning of the two endpoint Hessians on the pin
       rows (mpmath, 60 digits), then by Monte Carlo with common random numbers over ten separations
       `r ≤ c := 0.1/(1 + κ)²` (`cusp_parity_mc.py`, `cusp_parity_fine.py`).
     - *Fits.* Polynomial fits `g₀ + g₁r + g₂r² + …` of degree 2–4 were made for `κ ∈ {1/2, 1, 2, 4}` and `b ∈ {0, 1}`.
       Across the grid the linear term changes the kernel by `|g₁c/g₀| ≤ 5·10⁻⁵`, against `|g₂c²/g₀| ≈ 3–8·10⁻³` for the
       quadratic term.
     - *Check.* `g₀` agrees with a Monte Carlo value of `𝒜^{cand}(κ)` within `0.6%` (about two standard errors of that
       value; `g₀` is lower in all eight cases).
   - *The layer* (`layer_match_mc.py`). At fixed `k ∈ {0.05, 0.1, 0.2, 0.4, 0.8}` and `r ∈ [0.005, 0.04]`, the
     typed-minus-surrogate difference agrees with the cusp tail `𝒜(κ) − A₂(0)` within `O(rk)`, as (U.1) predicts. The
     relative discrepancy is `O(k²)`, and the factor `p_{V_r}(v(k)) = O(e^{−12k²})` makes it of order one at `k ≈ 1`, the
     fold scale.
   - *The full-field Monte Carlo of #216.*
     - *Data.* Binned counts in the project archive, `V2_2/numerics_lifetime_mc_20261001/results/mc{2,3}_final.json`;
       fits by `refit_mc.py` and `scan_p.py`.
     - *What it measures.* The *adjacent*-pair density, not `ν_cand`. Formally the two have the same `ℓ^{−1/3}`,
       `ℓ^{1/4}` and `ℓ^{1/3}` coefficients, but adjacent pairs have no `B_{d,L}` term, and nothing on file proves the
       adjacent-pair expansion (#218 Remark 3). So the comparison concerns the common formal coefficients only.
     - *Adjacent pairs.* The residual about the three-term law gives `ℓ^{1/2}` coefficients, fitting `ℓ^{1/2}` and `ℓ^{3/4}`
       jointly, of:
       - `−0.003 ± 0.005` (`d = 2`) and `+0.003 ± 0.007` (`d = 3`) on `[10⁻⁴, 0.3]`;
       - `+0.000 ± 0.020` and `−0.023 ± 0.030` on `[10⁻⁴, 0.1]`.

       All are consistent with zero. A single extra power (scanned over `p ∈ [0.10, 1.20]`) is best fitted at
       `p ≈ 0.7–0.8` (`d = 2`) and `0.68` (`d = 3`, on `[10⁻⁴, 0.3]`).
     - *Elder and rejected pairs.* These residuals behave differently: they are not consistent with zero. A single extra
       power fits best at `p ≈ 0.14–0.33` in six of eight fits; the others are `0.54` (elder, `d = 3`, `[10⁻⁴, 0.1]`) and
       a poor fit (rejected, `d = 2`, `[10⁻⁴, 0.3]`). So the data do not single out `ℓ^{1/2}`. In the joint
       `ℓ^{1/2} + ℓ^{3/4}` fits the `ℓ^{1/2}` coefficients are `+0.033 ± 0.004` and `+0.054 ± 0.005` (elder), and
       `−0.038 ± 0.002` and `−0.049 ± 0.004` (rejected).
     - *Conclusion.* This is consistent with Theorem P and with Remark 3. Explaining the elder residual (non-analytic
       decision effects, or Monte Carlo systematics) is open.
5. **`d = 1`.** In `d = 1` the layer is exponentially small in `κ` (the window is on `f₄` alone), and there is no
   transverse layer. The same reflection removes the `O(r)` cusp term. This is consistent with #214 §0 ("the numerics of
   §6.2 suggest the next terms are `O(h^{3/4})`").
6. **Consistency.**
   - (P.1) implies #229 (T⁺.1) and #218 (T.1).
   - Lemma U at fixed `κ` implies, after the `b`-integral, #229 (C⁺.1) for `r ≤ min(κ, r₃)`, in the stronger form
     `O((1 + κ)²r²)`.
   - Lemma K and (2.2) agree with #232 (J1) and (2.3).
   - #229 Remark 2 bounded the kink of the candidate weight by `O(κk²)` and expected `O(k²)`. Lemma Λ controls the kink
     through the density of its location instead, and gets `O(k²/(1 + κ))` for the layer part.
   - With `c` and `c₂` from #223 (certified enclosures there) and `I^{cand}` from #207 (exploration), the SIDE24 candidate
     density is `ν_cand ≈ 0.0417759ℓ^{−1/3} + B_{3,24} − 0.1394041ℓ^{1/4} + 0.1612340ℓ^{1/3} + O(ℓ^{3/5})`.

## 7. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (`247b3ecf`) | §2 rows, target, Jacobian 12; (R2)–(R5) — consumed |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (`dfed3b8d`) | §2 finite-jet rank — consumed |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (`213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (`fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (`75da2597`) | reading rule |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (`5b6328ea`) | (Z2)–(Z3): `Ψ_0`, `B_{d,L}` — consumed |
| #191 | `frontiers/remainder_vanishing_20260930/PROOF.md` (`441152df`, merged) | `r_0^*`, (2.1), Lemma E Step 4; Lemma E Steps 1–3 through #218 — consumed |
| #198 | `frontiers/remainder_rate_20260930/PROOF.md` (`abfb98ae`, merged) | (W.4); (3.1), §3 sign window and Lemma W through #218 and #207 — consumed |
| #207 | `frontiers/cusp_second_order_20261001/PROOF.md` (`f6df5a73`, merged at `566b1a1`) | §0 (`Y`, `Δ`, `E₀`); §4 (4.1); §7 Lemma L (7.1)–(7.2), the `B_{d,L}` decomposition, `I^{cand}` ((CU′.1), (7.3)) — consumed |
| #218 | `frontiers/candidate_third_order_20261001/PROOF.md` (`70ca57ef`, merged at `fb6ee97`) | §0 (`A₂`, `c₂`); §1 (Lemma D, `T`, (1.2)); Steps F1 and F3, (F.2), the surrogate remark; Lemma C Step C1; Lemma O's proof; §4 — consumed |
| #229 | `frontiers/third_order_rate_20261001/PROOF.md` (unmerged) | Theorem T⁺, (C⁺.1), Remarks 1–2 — cited |
| #232 | `frontiers/c2_finite_jet_transfer_20261001/PROOF.md` (`54cc4a1a`, merged at `7fe06b0`) | (2.3), §1, (3.2), §4, Theorem J — cited (independent agreement) |
| #216, #223, #214, #220 | as in `SOURCES.json` | `c₂` and #216's formal law (0.2); `c`, `c₂` enclosures; `d = 1`; the elder density — cited |

## 8. Exact controls (`parity_check.py`; stdlib; exact rationals; byte-identical under `-O` and on CPython 3.10–3.14)

| Control | Checks |
|---|---|
| Q1 | the ledger of §5: least `3/5` at `ρ = ℓ^{1/5}`, attained by `ρ³`, `ℓ²ρ^{−7}`, `ℓρ^{−2}`; the split is optimal on a grid and is the edge `k = r²`; the ledger without Lemma K also gives `3/5`; the closed form `∫_0^∞ r min(k, 1/k) dr = (6/5)ℓ^{2/3}` (antiderivatives evaluated exactly at three values); `3/5 > 1/2 > 3/7 > 4/11` |
| Q2 | Lemma R and the evenness of Lemma Π on fourteen exactly pinned polynomial fields (`d = 1, 2, 3, 4`): pinned jets even in `r`; `Π` even; the new row of §1 has target `0` (a consistency identity); point reflection maps the pins at `k` to those at `−k` and preserves `Π`; `det K_M` and `det K_S` affine in `k` at fixed free jets (at `d + 1` values of `k`, which determine a polynomial of degree `≤ d`) |
| Q3 | (2.2) exactly on the same fields: `det K_{M,S} = ∓6kΔ + rU ∓ r²V + …`, `Π = 36k²Δ² + r²(12kΔV − U²) + …`, with `Δ_BB = ∂_t²det(A + tB)` and `A^♯_B = ∂_t adj(A + tB)` at `t = 0` in general form (so `d = 4` tests the terms that vanish or simplify for `m ≤ 2`); `U` invariant and `V` odd under `(k, odd jets) ↦ (−k, −odd jets)` |
| Q4 | Lemma K for the Gaussian kernel: the `A`-integrand `H(k, A)` of the birth-integrated `r²` coefficient (exact Gaussian conditioning and Isserlis) has only `k⁰, k², k⁴` terms in `d = 1, 2, 3`, and `a = 12`; the `d = 1, 2` polynomials equal #232 §4's |
| Q5 | Step U2's pointwise algebra on rational grids: `y² − min(y², c²) = (y² − c²)₊`; `|(x + e)₊ − x₊ − e1{x>0}| ≤ |e|1{|x| ≤ |e|}`; the Case 1 sign decomposition with the anti-typed term; the Case 3 identity `P(1_{typed} − 1) − X₊ = P1_{typed} − (−X)₊ + ε` |
| Q6 | the inequality `(r² + min(1, k²))/(1 + κ) ≤ 2(r² + r min(k, 1/k))` for `k ≥ r²` on a rational grid; and, as consistency identities that cannot fail, `k/(1 + κ) ≤ r`, `r³/κ ≤ r²` (equivalent to `k ≥ r²`) and `kr = r min(k, 1/k)` for `k ≤ 1` |

Mutants `M1`–`M8` each fail only their own control:
- M1: the split `ℓ^{1/6}`;
- M2: the height of `M` in place of the midpoint;
- M3: `U` without `3kΔ_B`;
- M4: `V` without `f₅`;
- M5: a constant offset in `T_r`'s target;
- M6: the decomposition without the anti-typed term;
- M7: a false bookkeeping inequality;
- M8: the saddle's Hessian at `r/2 + r⁴`, which breaks the endpoint symmetry of `Π` (its evenness in `r` and its
  reflection invariance, both checked in Q2).

An unknown label exits 2.

    python3 -B -S parity_check.py                 # exit 0, output = RESULTS.json
    python3 -B -S parity_check.py --mutant M3     # exit 1

The controls check exact algebra, symmetry and arithmetic. The Gaussian layer estimates of §§3–4 (Lemmas D″, Λ₀, Λ, U)
are proved in prose only.

## 9. Review slices

- **A** §§1–2: Lemma R (birth integration, parity, reflection, evenness in `r`), Lemma Π, Lemma K.
- **B** §3: Lemmas D′, D″, Λ₀ and Λ (the coupling, the `f₄`-smoothing, the kink: main set, change of variables,
  exceptional set).
- **C** §§4–5: Lemma U (Steps U1–U4: the case analysis, (a)–(c), the comparison of laws) and the proof of Theorem P with
  its ledger.
