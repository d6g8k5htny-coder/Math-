# The bounded remainder of Theorem R: `B_{d,L}` for candidates, `0` for elder pairs

Object: CL-D2-REMAINDER-VANISHING-20260930-v1.
Author: Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), 30 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR REVIEW REQUIRED. Scientific effect: NONE — no register,
graph, STATUS, PROOF_INDEX, prize or Boolean change; no numerical constant is claimed. Same GitHub account as
every lane; zero organizational independence. Everything below is relative to merged, reviewed sources ([R],
[Z], [C7-K] and the reconciled [P] chain); the unmerged Math- #187/#188 are cited only, for the quantitative
Remark 2.

## 0. Statement

Setting, notation and every display number `(Rn)` are those of [R] (`frontiers/three_fronts_20260924/
LIFETIME_REMAINDER.md`, blob `247b3ecf`, Theorem R; xAI R1–R6 on main #67, Anthropic full depth Math- #186):
fixed `d ≥ 2`, `L > 0`, the [P] field on `X = R^d/(LZ^d)`; near pins `M = −ru/2`, `S = ru/2` with heights `b`,
`b − kr³` and zero gradients; the observation rows `U_r`, target `v_r`, density `π_r`, the regression law `Q`,
the coupling `F_r` of [R] (R3)–(R4), `m = d − 1`, `P = 1 + |b| + k`; the scaled endpoint Hessians
`K_i = D_r^{−1}H_iD_r^{−1}` with `α_i = F_{r,xx}(i)/r`, `β_i = ∇_yF_{r,x}(i)/r`, `A_i = D_y²F_r(i)` (`i = M, S`); the
filtered determinants `F_j`; `Z_r/r² = E_Q[F_d(K_M)F_{d−1}(K_S)]`; `A_0 = D_y²F_0(0)`,
`z_0 = E[(6k)²(det A_0)²1{A_0 < 0}]`; `A_r = 12π_r(v_r)Z_r/r²`, `A_0 = 12π_0(v_0)z_0`; the majorant
`H(b,k) = CP^Ne^{−c(b²+k²)}` (`N` enlarged when needed); the near/far split at a separation `r_0`, `a = ℓ/r_0³`; and
`c = c_{d,L}` of [P] (15.2). Admissible radii: `r_0 ≤ r_0^* := min{r_0^{[R]}, L/(4√2), r_0^{[K]}, r_0^{[Z]}}` ([R]'s compactness band on
which (R2)–(R5) hold, the cap-cylinder embedding of [REC] §5, and the radii of [C7-K] (K2) and [Z] §4). [R] proves
`|A_r − A_0| ≤ r(k + r)H` ((R11), first order in `r`) and from it Theorem R, `|ν_eld(ℓ) − cℓ^{−1/3}| ≤ C`, and states
that neither convergence of the remainder nor a second coefficient is identified.

From [Z] (`frontiers/c7_zero_gap_limit_20260929/PROOF.md`, blob `5b6328ea`; Anthropic A/B/C reads on Math- #155):
the unmarked candidate kernel and the equal-height kernel

    Ψ_ℓ^{cand}(b, y) = p_y(v_{b,ℓ}) E_{Q_{y,b,ℓ}}[W],      Ψ_0(b, y) = p_y(v_{b,0}) E_{Q_{y,b,0}}[W]          ((Z2)),

`B_{d,L} = ∫_{X∖{0}}∫_R Ψ_0(b, y) db dy ∈ (0, ∞)` ((Z3)), and Theorem Z (Z4): the rejected density
`ρ_rej(ℓ) = ν_cand(ℓ) − ν_eld(ℓ) → B_{d,L}` as `ℓ ↓ 0`.

**Lemma E (even contact expansion).** There are `C, N` depending on `d, L` only such that for all `b ∈ R`, `k > 0`
and `0 < r ≤ r_0^*`

    |Z_r/r² − z_0(b, k, u)| ≤ C r² P^N,        |A_r − A_0| ≤ r² H(b, k).                            (E.1)

The first-order term of (R11) is absent: the two endpoint corrections enter the typed product with opposite signs
and cancel identically (§1, Steps 1–3), and on the inertia-flip layers the product of the two typed determinants is
`O(r²)` (Step 4).

**Theorem R+.** For every fixed `d ≥ 2`, `L > 0`, as `ℓ ↓ 0`,

    ν_cand(ℓ) = c ℓ^{−1/3} + B_{d,L} + o(1),                                                         (R+.1)
    ν_eld(ℓ)  = c ℓ^{−1/3} + o(1),        i.e.   ν_eld(ℓ) = c ℓ^{−1/3} (1 + o(ℓ^{1/3})).               (R+.2)

So the bounded remainder of Theorem R has the constant term `B_{d,L}` (the equal-height kernel mass of [Z]) for the
candidate density and `0` for the elder density. Moreover, for every `r_0 ∈ (0, r_0^*]`,

    ν_cand^{near,r_0}(ℓ) − cℓ^{−1/3} → ∫_{0<dist(0,y)<r_0}∫_R Ψ_0 db dy,       |ν_cand^{near,r_0}(ℓ) − cℓ^{−1/3}| ≤ C (r_0 + ℓ²r_0^{−7}).   (R+.3)

**What is not claimed.** No rate in (R+.1)–(R+.2) (Remark 2 gives one conditionally); no expansion beyond the
constant term (nothing about `o(1)` being `O(ℓ^{γ})`); no numerical `C`, `ℓ_*`, `B_{d,L}`; no finite-radius band; no
uniformity in `d`, `L`; nothing beyond the existential scope of Theorem R and Theorem Z.

## 1. Proof of Lemma E

Work under the coupling (R3): `F_r` and `F_0` on one probability space, `‖F_r − F_0‖_{L^p(C^q)} ≤ C_{p,q}r²P` (R4).
Let `T ≥ 1 + k` be a random variable with all finite moments bounded by `C_pP^p`, dominating
`1 + ‖F_r‖_{C^7} + ‖F_0‖_{C^7}` and `r^{−2}‖F_r − F_0‖_{C^2}` (this is [R]'s `T` with the `C^7` norm in place of `C^4`;
(R4) supplies the moments for every finite derivative order). Write `f = F_r`, `f_j = ∂_x^jf(0)`, and `O(x)` for
a quantity bounded by `C|x|` with `C = C(d)`.

*Step 1 (axial pins to second order).* The third and fourth rows of `U_r` at their pinned values `0` and `12k`
give, by Taylor's formula with integral remainder (the rules are centred, so the odd orders cancel),

    (f_x(S) − f_x(M))/r = f_2 + (r²/24) f_4 + O(r⁴T) = 0,
    (6/r²)[f_x(M) + f_x(S) − 2(f(S) − f(M))/r] = f_3 + (r²/40) f_5 + O(r⁴T) = 12k.

Taylor expansion of `f_xx` at `∓r/2` to second order, `f_xx(∓r/2) = f_2 ∓ (r/2)f_3 + (r²/8)f_4 + O(r³T)`, and
substitution of the two identities give

    α_M = −6k + (r/12) f_4 + ρ_M,      α_S = 6k + (r/12) f_4 + ρ_S,      |ρ_M| + |ρ_S| ≤ C r² T.          (1.1)

(For a polynomial profile of degree five the expansions are exact, `α_{M,S} = ∓6k + (r/12)f_4 ∓ (r²/120)f_5`;
checker E1.) The first-order coefficients coincide, so

    α_M α_S = −36k² + 6k(ρ_M − ρ_S) + r²(f_4/12)² + (rf_4/12)(ρ_M + ρ_S) + ρ_Mρ_S = −36k² + O(r²(1 + k)T²).   (1.2)

*Step 2 (transverse blocks).* With `B := ∂_xD_y²f(0)` and `‖D_y²f(0) − A_0‖ ≤ r²T` (coupling),

    A_M = A_0 − (r/2)B + O(r²T),      A_S = A_0 + (r/2)B + O(r²T),                                  (1.3)

and `det(A_0 + X) = det A_0 + tr(adj(A_0)X) + O(‖X‖²T^{m−2})`, so

    det A_M det A_S = (det A_0)² + det A_0 · [−(r/2) + (r/2)] tr(adj(A_0)B) + O(r²T^{2m}) = (det A_0)² + O(r²T^{2m}).   (1.4)

The transverse difference row `(f_y(S) − f_y(M))/r = f_{xy}(0) + (r²/24)f_{xxxy}(0) + O(r⁴T) = 0` gives
`f_{xy}(0) = O(r²T)`, hence with `γ := ∇_yf_{xx}(0)`,

    β_M = −γ/2 + O(rT),      β_S = γ/2 + O(rT),      q_i := β_iᵀadj(A_i)β_i = q + O(rT^{m+1}),   q := γᵀadj(A_0)γ/4.   (1.5)

(The sign of `β_i` enters `q_i` quadratically. That `f_{xy}(0)` is `O(r²)` and not `O(r)` is essential: an `O(r)`
value would shift `β_M` and `β_S` by a common `O(1)` and make `q_M − q_S = O(1)`.)

*Step 3 (the product of determinants).* By the exact identity `det K_i = α_i det A_i − r q_i` ([R] Lemma R3.2),

    det K_M det K_S = α_Mα_S det A_M det A_S − r(α_M det A_M q_S + α_S det A_S q_M) + r² q_M q_S.

By (1.2), (1.4) the first term is `−36k²(det A_0)² + O(r²(1 + k)²T^{N_1})`. In the second, by (1.1), (1.3), (1.5),
`α_M det A_M q_S = −6k det A_0 q + O(r(1 + k)T^{N_1})` and `α_S det A_S q_M = +6k det A_0 q + O(r(1 + k)T^{N_1})`, so
the bracket is `O(r(1 + k)T^{N_1})` and the term is `O(r²(1 + k)T^{N_1})`. The third is `O(r²T^{N_1})`. Hence

    | det K_M det K_S + 36k²(det A_0)² | ≤ C r² (1 + k)² T^{N_1}.                                     (1.6)

Structurally, `det K_M = −6k det A_0 + rY + O(r²)` and `det K_S = +6k det A_0 + rY + O(r²)` with the **same**
`Y = (f_4/12)det A_0 + 3k tr(adj(A_0)B) − q`; the product's `r`-term is `6k det A_0(Y − Y) = 0`. This is the
reflection symmetry of the pinned family: reversing the axis exchanges `M` and `S`, and the rows of `U_r` are even
in `r` (checker E2 verifies, on a general pinned quintic in two variables, the exact identity
`det H_M(−r) = det H_S(r)`, hence that `det H_M det H_S/r²` is an even polynomial in `r` with constant term
`−36k²A_0²`, while each single factor is not even).

*Step 4 (inertia).* For `A_i` invertible, Haynsworth's inertia additivity for the block matrix `K_i` gives
`inertia(K_i) = inertia(A_i) + inertia(σ_i)`, `σ_i := α_i − rβ_iᵀA_i^{−1}β_i`. So `index K_M = d` iff
`A_M < 0` and `σ_M < 0`; `index K_S = d − 1` iff (`A_S < 0` and `σ_S > 0`) or (`index A_S = m − 1` and `σ_S < 0`).
Put `u := C_1 r T (1 + T/k)` with `C_1 = C_1(d) ≥ 2` large, and the good event

    G := { λ_max(A_0) ≤ −u } ∩ { k ≥ C_1 r T }.

On `G`: `‖A_i − A_0‖ ≤ rT ≤ u/C_1`, so `A_M, A_S < 0`; `α_S ≥ 6k − CrT > 0` and `rβ_Sᵀ(−A_S)^{−1}β_S ≥ 0`, so
`σ_S > 0`; `α_M ≤ −6k + CrT ≤ −5k` and `rβ_Mᵀ(−A_M)^{−1}β_M ≤ rT²/λ_min(−A_M) ≤ 2rT²/u ≤ 2k/C_1`, so `σ_M < 0`. Hence
on `G` the indices are `d` and `d − 1`, `1{A_0 < 0} = 1`, and

    F_d(K_M)F_{d−1}(K_S) − 36k²(det A_0)²1{A_0<0} = |det K_M det K_S| − 36k²(det A_0)²,

whose absolute value is at most the left side of (1.6). Off `G` there are three cases, on each of which both typed
products are `O(r²)` times a polynomial:

- on `{k < C_1rT}`: `F_d(K_M)F_{d−1}(K_S) ≤ C(k + r)²T^{2d} ≤ Cr²T^{2d+2}` ([R] §4's bound `F_j(K_i) ≤ C(k + r)T^d`,
  `T ≥ 1`) and `36k²(det A_0)² ≤ Cr²T^{2m+2}`;
- on `{λ_max(A_0) ≥ u} ∩ {k ≥ C_1rT}`: `λ_max(A_M) ≥ u − rT > 0`, so `K_M` is not negative definite, `F_d(K_M) = 0`,
  and `1{A_0 < 0} = 0` — both products vanish (this case also contains the pattern `index A_S = m − 1`, `σ_S < 0`,
  which `F_d(K_M) = 0` kills);
- on `{|λ_max(A_0)| < u} ∩ {k ≥ C_1rT}`: by Weyl, `|det A_i| ≤ (|λ_max(A_0)| + rT)T^{m−1} ≤ 2uT^{m−1}`, so
  `|det K_i| ≤ (6k + CrT)·2uT^{m−1} + rT^{m+1} ≤ C(ku + rT²)T^{m−1} ≤ CkuT^{m−1}` (as `rT² ≤ ku/C_1`, i.e.
  `T ≤ k + T`), hence `F_d(K_M)F_{d−1}(K_S) ≤ Ck²u²T^{2m−2}`, and likewise `36k²(det A_0)²1{A_0<0} ≤ 36k²u²T^{2m−2}`;
  with `k²u² = C_1²r²T²(k + T)²` both are `≤ Cr²(k + T)²T^{2m}`.

No smallness of the layers' probability is needed: each typed determinant on the last layer is `O(r)` and their
product `O(r²)`.

*Step 5 (assembly).* Taking expectations, `|Z_r/r² − z_0| ≤ E[Cr²(1 + k)²T^{N_1} + Cr²(k + T)²T^{2m+2}] ≤ Cr²P^N`.
For `A_r − A_0 = 12[π_r(v_r) − π_0(v_0)]Z_r/r² + 12π_0(v_0)[Z_r/r² − z_0]`, use (R5) (`|π_r(v_r) − π_0(v_0)| ≤
Cr²P²e^{−c(b²+k²)}`, `π_0(v_0) ≤ Ce^{−c(b²+k²)}`), (R10) (`Z_r/r² ≤ C(k + r)²P^N`) and the first bound; every term is
`r²` times a polynomial in `P` times the Gaussian factor, i.e. `≤ r²H`. ∎

## 2. Proof of Theorem R+

*The separation variable.* As in [R] §6 and [Z] (Z14), with `r = (ℓ/k)^{1/3}`, `k = ℓ/r³`, `dk = 3ℓr^{−4}dr`,

    ν_cand^{near,r_0}(ℓ) = ∫_0^{r_0}∫_R∫_{S^{d−1}} r^{−2} A_r(b, ℓ/r³, u) dσ(u) db dr,
    c ℓ^{−1/3}            = ∫_0^{∞}∫_R∫_{S^{d−1}} r^{−2} A_0(b, ℓ/r³, u) dσ(u) db dr,

and, by the pin-density and determinant normalizations of [P] (10.1)–(11.1) exactly as in (Z14) but without the
mark, `r^{−2}A_r(b, ℓ/r³, u) = r^{d−1}Ψ_ℓ^{cand}(b, ru)` (the polar factor `r^{d−1}`, the pin density
`12r^{−(d+3)}π_r(v_r)` and the determinant scale `r²`). Hence

    ν_cand^{near,r_0}(ℓ) − cℓ^{−1/3} = ∫_0^{r_0}∫∫ r^{−2}(A_r − A_0)(b, ℓ/r³, u) − ∫_{r_0}^{∞}∫∫ r^{−2}A_0(b, ℓ/r³, u).   (2.1)

*Domination.* By (E.1), `|r^{−2}(A_r − A_0)(b, ℓ/r³, u)| ≤ H(b, ℓ/r³) ≤ Ce^{−cb²}`, an integrable majorant on
`(0, r_0) × R × S^{d−1}` **independent of `ℓ`** — the near-diagonal domination that [Z] §5 records as unavailable
for candidates from (R11) alone (with `r(k + r)H` the integrand is only `≤ (1 + ℓ/r⁴)H`). The second term of (2.1)
is at most `∫_{r_0}^∞ r^{−2}(ℓ/r³)²H ≤ Cℓ²r_0^{−7}` (`A_0 ≤ k²H`).

*Pointwise limit.* Fix `r, b, u`. As `ℓ ↓ 0`, `k = ℓ/r³ ↓ 0` and `A_r(b, k, u) → A_r(b, 0, u)`: the pinned law
`Q_{r,b,k}` is the regression law with target `v_r(b,k)`, affine in the target with the `k`-free covariance of
[R] §2, so `F_r` depends continuously on `k` in `C²`, the typed product is continuous off the type boundaries
(Gaussian-null by nondegeneracy, [Z] §2), and it is dominated by a polynomial in the endpoint Hessians; `π_r(v_r)`
is continuous in the target. Also `A_0(b, k, u) → 0` (`A_0 ≤ k²H`). Since `r^{−2}A_r(b, 0, u) = r^{d−1}Ψ_0(b, ru)`
((Z2) at `y = ru`), dominated convergence in (2.1) gives

    ν_cand^{near,r_0}(ℓ) − cℓ^{−1/3} → ∫_0^{r_0}∫∫ r^{d−1}Ψ_0(b, ru) dσ db dr = ∫_{0<dist(0,y)<r_0}∫_R Ψ_0(b, y) db dy,   (2.2)

and the majorant gives the quantitative form `|ν_cand^{near,r_0} − cℓ^{−1/3}| ≤ C(r_0 + ℓ²r_0^{−7})`. This is (R+.3).
(The signed refinement `ν_cand^{near,r_0} − cℓ^{−1/3} ≥ −C(min(ℓ^{1/4}, r_0) + ℓ²r_0^{−7})` follows from `A_r ≥ 0` on
`r ≥ ℓ^{1/4}` together with (E.1) on `r < ℓ^{1/4}`; a lower bound `≥ −O(ℓ²r_0^{−7})` would need a positive lower bound
on the near-diagonal equal-height kernel, which is not supplied.)

*The far candidate density.* On the compact set `dist(0, y) ≥ r_0`, [P] §14 / (14.1) — the input behind [Z]
(Z16) — bounds the unmarked kernel `Ψ_ℓ^{cand}` by `Ce^{−c''b²}` uniformly in `0 < ℓ ≤ 1` (the two-site jets are
uniformly nondegenerate there), and `Ψ_ℓ^{cand}(b, y) → Ψ_0(b, y)` pointwise as `ℓ ↓ 0` ([Z] §5: "the unmarked
candidate kernel also tends to (Z2)"; by the coupling (Z10), `f_ℓ = f_0 + ℓh_y → f_0` in `C²`, the type boundaries
are null, and the determinant product is dominated). So
`ν_cand^{far,r_0}(ℓ) = ∫_{dist ≥ r_0}∫Ψ_ℓ^{cand} → ∫_{dist ≥ r_0}∫Ψ_0`. Adding (2.2),

    ν_cand(ℓ) − cℓ^{−1/3} → ∫_{X∖{0}}∫_R Ψ_0 db dy = B_{d,L},

which is (R+.1) (`B_{d,L} < ∞` by [Z] (Z17)–(Z18), and the near/far cutoff is spatially null).

*The elder density.* `ν_eld − cℓ^{−1/3} = (ν_cand − cℓ^{−1/3}) − ρ_rej(ℓ) → B_{d,L} − B_{d,L} = 0` by (R+.1) and
Theorem Z (Z4). This is (R+.2). ∎

## 3. Remarks

1. **Where Theorem R's `O(1)` went.** For the candidate density it is real and now identified: the leading law
   `cℓ^{−1/3}` is the small-separation contact mass, and what it misses is exactly the equal-height kernel mass
   `B_{d,L}`, spread over all separations (`O(1)` per unit separation, (R+.3)); by Theorem Z all of it is rejected
   mass. For the elder density the three `O(1)` sources of [R] §§6–7 — the first-order contact monomial
   `k^{−2/3}rk = ℓ^{1/3}` of (R16), the `r_0`-proportional cutoff terms of (R16)–(R18), and the far term — are,
   respectively, an artifact of bounding the endpoints separately (Lemma E), the rejected mass at separations
   `≍ r_0`, and the far rejected mass; none is elder mass in the limit.
2. **A rate (conditional, not claimed).** For fixed `ρ ∈ (0, min(r_0^*, L/4)]`, (R+.3), the loss bound of [C7-K] §4
   (`0 ≤ ν_cand^{near,ρ} − ν_eld^{near,ρ} ≤ C(ρ + ℓ^{1/4})`, the proof of (T1) with cutoff `ρ`; if `a ≥ ℓ^{1/4}`,
   (K2) alone gives `Cℓ^{1/4}`) and a far elder bound give
   `|ν_eld(ℓ) − cℓ^{−1/3}| ≤ C(ρ + ℓ^{1/4} + ℓ²ρ^{−7}) + ν_eld^{far,ρ}(ℓ)`; with Math- #187 the last term is
   `C_ρℓ^{2/3}`, with Math- #188 it is `C_{N,ρ}ℓ^N` (both unmerged candidates). A rate `ℓ^{γ}`, `γ > 0`, follows as
   soon as the far constant is known to be polynomial in `1/ρ` (take `ρ = ℓ^{θ}`, `θ` small, `N` larger than
   `θ` times that degree); the constant's `ρ`-dependence enters through the far-pair nondegeneracy at separation
   `ρ` and, for #188, the `N`-site conditional density and `ℓ_1 = ρ²/(64N²)`. None of this is proved here.
3. **Consistency.** (R+.1) with (Z4) is consistent with [C7-K] (T2) and [U] (U1) (`ρ_rej = Θ(1)`); (R+.3) with
   [P] (14.1) (candidate density `O(1)` at fixed separation) and with [Z] (Z18) (rejected mass below separation `δ`
   is `≤ Cδ`); Lemma E with the remark in Math- #186 ("Where the `O(1)` comes from": at fixed marks the contact error
   is `O(r²)`; that remark also noted that this alone does not improve Theorem R, which is why Theorem R+ needs the
   domination-plus-limit argument of §2 rather than the ledger of (R16)). The `2r_0` of #186's C7 model check is
   the (R17)–(R18) loss term, i.e. the rejected mass at separations `≍ r_0`, in agreement with Remark 1.
4. **For the manuscript.** Once reviewed, (R+.2) supports reading the abstract's `(1 + o(1))` as
   `(1 + o(ℓ^{1/3}))` and, for the candidate density, `cℓ^{−1/3} + B_{3,24} + o(1)`. Until then E10 of the V3 edit
   pack (`(1 + O(ℓ^{1/3}))`, which rests on Theorem R and its two reads, the second still unmerged in Math- #186)
   is the safe statement, and E3's "do not write an `o(1)` remainder for `ν_eld` alone" and E10's "not known to be
   improvable" would be revised by this note when it lands. No `+ c_1 + o(1)` with `c_1 ≠ 0` is claimed for `ν_eld`;
   the claim is precisely that its constant term is `0`.

## 4. Sources (exact identities in `SOURCES.json`)

| Tag | Path | Role |
|---|---|---|
| [R] | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md` (blob `247b3ecf`) | Theorem R; §§2–6: coupling (R2)–(R5), Lemma R3.2, (R8)–(R11), the separation-variable identity — consumed |
| [Z] | `frontiers/c7_zero_gap_limit_20260929/PROOF.md` (blob `5b6328ea`) | (Z2)–(Z4), (Z10)–(Z12), (Z14), (Z16)–(Z18) — consumed |
| [C7-K] | `frontiers/c7_total_bounded_20260929/PROOF.md` (blob `28748b08`) | §4 (T1) proof with cutoff `ρ`, (T2) — Remark 2, Remark 3 |
| [P] | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d`) | §§1–4, 7, 9 (as [E2]), (10.1), (11.1), 14, (15.2) — through [R], [Z] |
| [E1] | `imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md` (blob `213594d6`) | reading rule |
| [E2] | `reviews/d1_section9_borel_repair_20260925/REPAIR.md` (blob `fe9b9ce4`) | §9 replacement |
| [REC] | `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` (blob `75da2597`) | W1, embedding radius, consumption contract |
| [U] | `frontiers/unrestricted_selection_difference_20260929/PROOF.md` (blob `5a55b179`) | (U1) — cited only (Remark 3) |
| #187, #188 | `frontiers/far_elder_rate_20260930/PROOF.md`, `frontiers/far_elder_flat_ridge_20260930/PROOF.md` (unmerged) | far elder rates — cited only (Remark 2) |
| #186 | `reviews/d2_remainder_full_depth_claude_20260930/REVIEW.md` (unmerged) | the review remark that motivated Lemma E — cited only |

## 5. Exact controls (`even_contact_check.py`; stdlib; exact rationals; byte-identical under `-O`)

E1 the axial pin identities on a quintic profile: with `f_2 = −(r²/24)f_4`, `f_3 = 12k − (r²/40)f_5` the pins
`f(∓r/2) = b, b − kr³`, `f_x(∓r/2) = 0` hold exactly and `α_M = −6k + (r/12)f_4 − (r²/120)f_5`,
`α_S = 6k + (r/12)f_4 + (r²/120)f_5`, `α_Mα_S = −36k² + r²(f_4²/144 − kf_5/10) − r⁴f_5²/14400`, at rational
`(r, k, f_4, f_5, b)` — the coefficients `1/24, 1/40, 1/12, 1/120` are the content of Step 1; mutant M1 (drop the
`(r²/40)f_5` pin term) fails.
E2 the reflection symmetry on a general pinned quintic in two variables (six pinned coefficients solved exactly,
fifteen free ones fixed at rationals): `det H_M(−r) = det H_S(r)` exactly at rational `r`; consequently
`det H_M det H_S/r²`, recovered as the polynomial of degree ten in `r` by exact interpolation at eleven rational
`r`, has only even powers, constant term `−36k²A_0²` (`A_0 = f_yy(0)`), and the recorded `r²` coefficient. The parity
is forced by the symmetry, so this is a check of the mechanism of Step 3, not of its bookkeeping; mutant M2
applies the parity test to the single factor `det H_M/r`, which has `r¹, r³, r⁵` terms, and fails.
E3 the block identity `det K = α det A − r βᵀadj(A)β` and Haynsworth's inertia count on rational `3×3` and `4×4`
examples with `A` negative definite, of index `m − 1`, and indefinite, and the scalar Schur complement of both
signs (inertia by exact congruence diagonalisation); the Step 4 case split at rational points: `F_d(K_M) = 0` when
`λ_max(A_M) > 0`, and the layer inequality `|det A| ≤ (|λ_max(A)|)·‖A‖^{m−1}` for `|λ_max(A)|` small.
E4 the ledger of §2 and Remark 2 by exact monomial substitution `r = (ℓ/k)^{1/3}`: `r^{−2}(ℓ/r³)² = ℓ²r^{−8}`
(so `∫_{r_0}^∞ ≍ ℓ²r_0^{−7}`), `k^{−2/3}r^{3}/k = ℓk^{−8/3}`, `ℓκ^{−5/3} = κ^{7/3} = ℓ^{7/12}` at `κ = ℓ^{1/4}`,
`ℓ^{2/3}a^{−1/3} = r_0ℓ^{1/3}`, and `r ≤ k ⇔ ℓ ≤ k⁴`; mutant M3 (claims the loss exponent `1/3`) fails.
E5 the layer algebra of Step 4: `k²u² = C_1²r²T²(k + T)²` and `rT² ≤ ku/C_1` for `u = C_1rT(1 + T/k)`, exactly.
Mutants `M1`–`M3` exit 1; an unknown label exits 2. The controls check identities and bookkeeping; they do not prove
the Gaussian estimates and are not acceptance.

## 6. Review slices

A: Lemma E — Steps 1–3 (the expansions and the product cancellation) and Step 4 (Haynsworth, the good event, the
   three layers), Step 5.
B: §2 — the separation-variable identity against [R] §6 / [Z] (Z14), the `ℓ`-uniform majorant from (E.1), the
   pointwise limit `A_r(b,k,u) → A_r(b,0,u)`, the far candidate limit from [Z], and the use of (Z4).
C: the statement's scope, Remarks 1–4, and the sources' consumption (in particular that nothing unmerged is used).
