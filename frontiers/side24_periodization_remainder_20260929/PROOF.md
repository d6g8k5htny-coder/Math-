# SIDE24 periodization: the second-order remainder is below 10⁻²¹⁸ (explicit D²Φ majorant)

**Object:** CL-SIDE24-PERIODIZATION-REMAINDER-20260929-v1. **Author:** Anthropic Claude (session
`session_01NMeKEismAyeqgdB4sy2NJU`). **Disposition:** author-side proof candidate; **nonauthor analytic review
required**. Scientific effect: NONE. No register, `STATUS`, `PROOF_INDEX`, `GRAPH`, prize or premise changes; no
existing enclosure is changed.

## Scope and exact sources

This note closes the open item of `frontiers/side24_periodization_20260929/PROOF.md` §5 (PR #144, v1.1, blob
`56f4af15…`): an explicit majorant for the second functional derivative of the coefficient, so that the closed-form
leading correction `P_3(24) e^{−288}` is certified as the *exact* correction up to a remainder of relative size
`< 10^{−218}`. It consumes, without re-proving:

- the **shape** of eq. (15.2) of UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1 (blob `dfed3b8d…`, SHA256 `9350ad6e…`):
  `c_{d,L} = Γ(7/6)/(24^{1/3}√π) ∫_{S^{d−1}} p_G(0) p_{V_u}(0) τ_u^{4/3} D_u dσ(u)` with `τ_u² = Var(f_{xxx} | G = 0)`
  and `D_u = E[det(A_u)² 1{A_u ≺ 0} | V_u = 0]`, read with the reconciliation reading rule — exactly as
  `coefficients/side24_v1` and #144 consume it;
- from `coefficients/side24_v1/PROOF.md` (blob `44b66f04…`, reviewed: xAI C1–C6, Anthropic PR #152): the reference
  jet covariance `C_ref` (§1), the all-direction image bound `|D^q K_24(0) − D^q K_∞(0)| < E := 21175738586478·10^{−125}`
  for every unit-direction contraction of order `≤ 6` (§2, eq. (2)), and `C_ref ≥ I/3` (§3);
- from #144: the identity `DΦ(J_∞)[J^{(1)}_L]/Φ(J_∞) = P_3(L) e^{−L²/2}`, `P_3(L) = −L²(10L⁴ − 147L² + 315)/105`
  (its Theorem; Slice A identities accepted by xAI/Harper, §4 derivation under xAI Slice B′), and its §1 projection.

Throughout `d = 3`, `m = d − 1 = 2`, `L = 24`, `q := e^{−L²/2} = e^{−288}`, and `c_∞ := c_{3,∞}` is the reference
value (formula (1) of side24_v1), `c_{24} := c_{3,24}` the exact periodized value.

## Theorem R (candidate)

    c_{3,24} / c_{3,∞} − 1 = P_3(24) e^{−288} + ε,      |ε| < 10^{−218},

with `P_3(24) = −620813376/35`, so that `|ε| < 10^{−100} · |P_3(24) e^{−288}|` (the checker records
`|ε| < 6.3·10^{−219}` from the second-order term and `< 6.1·10^{−235}` from the first-order rest). Existential scope
of the parent; nothing numerical about `c_{3,∞}` itself is changed.

## 1. The section representation of the (15.2) integrand

Fix a frame `(x, y_1, y_2)` with axis `u = e_x`, and let `z = (G, t, H) ∈ ℝ^{10}` be the jet coordinates
`G = (f_x, f_{y_1}, f_{y_2})`, `t = f_{xxx}`, `H = (f_{xx}, f_{xy_1}, f_{xy_2}, f_{y_1y_1}, f_{y_1y_2}, f_{y_2y_2})`;
`V_u = (f_{xx}, f_{xy_1}, f_{xy_2})` and `A = A_u` is the transverse `2×2` Hessian. Write `C_u` for the `10×10`
covariance of `z` under a centered Gaussian field with **even** covariance kernel `K`, and

    w(t, A) := |t|^{4/3} det(A)² 1{A ≺ 0},      F(C) := ∫_{ℝ×Sym_2} w(t, A) φ_C(0, t, 0, A) dt dA,

where `φ_C(0, t, 0, A)` is the `10`-dimensional Gaussian density of `z` evaluated on the section `G = 0, V = 0`
(`n_free = 1 + 3 = 4` free coordinates, `n = 10`). `w` is nonnegative and homogeneous of degree `p = 4/3 + 2m = 16/3`.

**Lemma 1 (section identity).** For every even kernel `K` (in particular `K_∞` and `K_24`) and every frame,

    p_G(0) p_{V_u}(0) τ_u^{4/3} D_u = κ F(C_u),      κ := √π / (2^{2/3} Γ(7/6)),

and hence, `F(C_u)` depending on the frame only through the axis `u` (transverse-frame invariance: parent §15,
and Lemma 2 below),

    c_{3,L} = 96^{−1/3} ∫_{S²} F(C_u) dσ(u).                                              (1.1)

*Proof.* `K` even makes `Cov(∂^α f, ∂^β f) = (−1)^{|β|} ∂^{α+β}K(0)` vanish for `|α| + |β|` odd, so the odd block
`(G, t)` is independent of the even block `(V, A)`; in particular `p_{(G,V)}(0,0) = p_G(0) p_V(0)`, the law of `t`
given `G = 0` is centered Gaussian with variance `τ_u²` and is unchanged by also conditioning on `V = 0`, and the law
of `A` given `V = 0` is unchanged by conditioning on `G = 0`. Therefore
`∫ w φ_C(0,t,0,A) dt dA = p_G(0)p_V(0) · E[|t|^{4/3} | G = 0] · E[det(A)²1{A≺0} | V = 0]` and
`E|N(0,τ²)|^{4/3} = τ^{4/3} 2^{2/3} Γ(7/6)/√π = τ^{4/3}/κ` (the standard `E|X|^p = σ^p 2^{p/2}Γ((p+1)/2)/√π`;
checked by quadrature in checker C2). Multiplying by the (15.2) prefactor, `κ Γ(7/6)/(24^{1/3}√π) = 2^{−2/3} 24^{−1/3}
= 96^{−1/3}` (the `Γ(7/6)` and `√π` cancel symbolically; `4·24 = 96`, checker C2). At `C_ref`, (1.1) reproduces
side24_v1's formula (1): `96^{−1/3} · 4π · (2π)^{−3} 3^{−1/2} 6^{2/3} 2^{2/3} Γ(7/6) π^{−1/2} D_2 = (3/2)^{1/3} Γ(7/6) D_2 /(2√3 π^{5/2})`
because `(144/96) = 3/2` (checker C2). ∎

`K_24(z) = Σ_n φ(z + 24n)/Σ_n φ(24n)` is even, so Lemma 1 applies to the periodized field with no isotropy assumption.

## 2. Frame invariance: the first-order term is the isotropic projection (the exact form of #144 §1)

**Lemma 2.** Let `Δ` be any even jet tensor at `0` through order six (a triple of totally symmetric tensors of
ranks 2, 4, 6 — e.g. `K_24 − K_∞`, or its `q`-linear part `qΔ^{(1)}` of §6), and `Δ_u` its `10×10` matrix in a
frame with axis `u`, which transforms covariantly (`Δ_{uR_y} = S Δ_u Sᵀ`). Then `F(C_ref + Δ_u)` does not depend on the choice of transverse frame,
and

    ∫_{S²} dF[C_ref](Δ_u) dσ(u) = 4π · dF[C_ref](Δ̄),

where `Δ̄` is the `O(3)`-Haar average of the perturbation, i.e. the isotropic jet perturbation with
`(δa, δm4, δχ)` given by the direction-averaged axial contractions of #144 §1.

*Proof.* A rotation `R_y` of the transverse plane acts on the jet coordinates by a linear map `S` with `|det S| = 1`
that fixes the section `{G = 0, V = 0}` as a set (it rotates `G` and `V` within themselves) and leaves `w` invariant
(`|t|` is untouched; `det(A)² 1{A ≺ 0}` is `O(2)`-invariant). Hence `F(S C Sᵀ) = F(C)` for every `C`, and
`S C_ref Sᵀ = C_ref`. So `F(C_ref + Δ_{uR_y}) = F(C_ref + Δ_u)` and, differentiating at `C_ref`,
`dF[C_ref](Δ_{uR_y}) = dF[C_ref](Δ_u)`. Averaging over `R_y` and then over `u ∈ S²` averages over Haar measure on the
frame group, and `dF[C_ref]` is linear, so the left side equals `4π dF[C_ref](E_Haar Δ_R) = 4π dF[C_ref](Δ̄)`. An
`O(3)`-invariant even jet perturbation through order six is determined by one scalar per order, and those scalars
are the averaged axial contractions `⟨∂_v^{2j}⟩` — the `(δa, δm4, δχ)` of #144 §1 and §3. ∎

Consequently `dF[C_ref](Δ̄)` is the derivative of `F` along the isotropic family `J = (a, m4, χ)`, which #144 §4
evaluates as `F_ref · [δΩ/9 + δm4/6 − (13/6) δa]`; for the `q`-linear part of `Δ` this is `F_ref · P_3(L) q`.

## 3. Gaussian directional derivatives

**Lemma 3.** For `C ≻ 0`, `Δ` symmetric, `C_t := C + tΔ`, `z` fixed, `y := C_t^{−1} z`, `q_t := zᵀ C_t^{−1} z`,
`a := yᵀΔy − tr(C_t^{−1}Δ)`:

    (d/dt) φ_{C_t}(z) = (1/2) φ_{C_t}(z) · a,
    (d²/dt²) φ_{C_t}(z) = φ_{C_t}(z) · [ a²/4 − yᵀ Δ C_t^{−1} Δ y + (1/2) tr(C_t^{−1} Δ C_t^{−1} Δ) ].

*Proof.* `log φ_{C_t}(z) = const − (1/2) log det C_t − (1/2) q_t`; `(log det C_t)' = tr(C_t^{−1}Δ)`,
`(log det C_t)'' = −tr(C_t^{−1}ΔC_t^{−1}Δ)`, `q_t' = −yᵀΔy`, `q_t'' = 2 yᵀΔC_t^{−1}Δy` (from `y' = −C_t^{−1}Δy`).
Then `φ' = φ (log φ)'` and `φ'' = φ[(log φ)'' + ((log φ)')²]`. The four derivative identities are verified exactly
(rational-function arithmetic, `3×3` example) in checker C3. ∎

## 4. A section-moment majorant

**Lemma 4.** For `C ≻ 0` of size `n = 10`, with `q(z) = zᵀC^{−1}z` and `w` as in §1 (so `p = 16/3`, `n_free = 4`),

    ∫ w(z) φ_C(z) q(z)^k dz  ≤  (4k/e)^k · 2^{n/2} · 2^{−1/3} · F(C) = (4k/e)^k · 2^{14/3} · F(C),   k = 1, 2,

the integral running over the section `G = 0, V = 0` as in §1.

*Proof.* `q^k e^{−q/2} = (q^k e^{−q/4}) e^{−q/4} ≤ (4k/e)^k e^{−q/4}` since `sup_{x≥0} x^k e^{−x/4} = (4k/e)^k`
(attained at `x = 4k`; checker C4). Hence `φ_C q^k ≤ (4k/e)^k 2^{n/2} φ_{2C}` (as `det(2C) = 2^n det C`). Finally the
scaling `φ_{sC}(z) = s^{−n/2} φ_C(z/√s)`, the substitution `z_free = √s z'` on the section and the homogeneity of
`w` give `∫ w φ_{sC} = s^{(p + n_free − n)/2} ∫ w φ_C = s^{−1/3} F(C)` (checker C1; the same exponent `−1/3` occurs
for `d = 2`). ∎

## 5. The second-order bound along the segment

Fix a frame `u`, put `Δ := Δ_u`, `δ := ‖Δ‖_op`, and `C_t := C_ref + tΔ`, `g(t) := F(C_t)`, `t ∈ [0, 1]`.

**Facts used.** (i) Every entry of `Δ` is a unit-direction contraction of `K_24 − K_∞` of order `≤ 6` (the
`t`-`t` entry has order six), so `|Δ_{ij}| < E` and `δ ≤ ‖Δ‖_F ≤ 10E` (side24_v1 (2)). (ii) In these raw
coordinates `C_ref` is block diagonal: odd block `[[1,−3],[−3,15]] ⊕ I_2`, even block `2I_3 + J_3` on the three
diagonal Hessian entries and `I_3` on the three off-diagonal ones; the spectrum is `{8 ± √58, 1, 1}` and
`{5, 2, 2, 1, 1, 1}`, so `λ_ref := λ_min(C_ref) = 8 − √58 > 1/3` (exactly: `(23/3)² = 529/9 > 58`; checker C5), and
`λ_t := λ_min(C_t) ≥ 1/3 − δ`. (iii) `±tΔ ≤ δ I ≤ 3δ C_ref`, so `(1−ε')C_ref ≤ C_t ≤ (1+ε')C_ref`
with `ε' := 3δ`. Then `φ_{C_t} ≤ [(1+ε')/(1−ε')]^{n/2} φ_{(1+ε')C_ref}` pointwise (side24_v1 §4), and Lemma 4's
scaling gives `F(C_t) ≤ (1+ε')^{n/2 − 1/3}(1−ε')^{−n/2} F_ref = (1+ε')^{14/3}(1−ε')^{−5} F_ref ≤ (1 + 32ε') F_ref`
(this is also side24_v1's (4) applied to `C_t`; note that `Δ_u`'s odd–even blocks vanish identically because the
kernel is even, so `C_t` keeps the block structure that side24_v1's factor-wise argument uses). (iv) Differentiation
under the integral in `g(t) = F(C_t)` is justified by the dominating function: for `t ∈ [0,1]`,
`φ_{C_t} ≤ [(1+ε')/(1−ε')]^5 φ_{(1+ε')C_ref}`, `q_t ≤ q_ref/(1−ε')` and `|y|² ≤ q_t/λ_t`, so `|∂_t^j φ_{C_t}(z)|`
for `j = 1, 2` is bounded uniformly in `t` by `const · φ_{(1+ε')C_ref}(z)(1 + q_ref(z))²`, and `w` times this is
integrable on the section (Lemma 4). The same bound makes `dF[C_ref]` the linear functional of Lemma 3, which is
what the Haar-average interchange in Lemma 2 uses.

**Proposition 5.** `|F(C_ref + Δ) − F(C_ref) − dF[C_ref](Δ)| ≤ K δ² F(C_ref)` with

    K = (1/2) · [ (M_2 + 2n M_1 + n²)/4 + M_1 + n/2 ] · (1/3 − δ)^{−2} · (1 + 96δ) < 1393,
    M_k := (4k/e)^k 2^{14/3}   (M_1 < 37.38, M_2 < 220.0; the bracket is < 310).

*Proof.* Taylor: `g(1) − g(0) − g'(0) = ∫_0^1 (1 − t) g''(t) dt`, so it suffices that `|g''(t)| ≤ 2K δ² F_ref`.
By Lemma 3, differentiating under the (absolutely convergent, Gaussian-dominated) integral,
`g''(t) = ∫ w φ_{C_t} [a²/4 − yᵀΔC_t^{−1}Δy + tr(C_t^{−1}ΔC_t^{−1}Δ)/2]`. With `|y|² = zᵀC_t^{−2}z ≤ q_t/λ_t`:
`|yᵀΔy| ≤ δ q_t/λ_t`, `|tr(C_t^{−1}Δ)| ≤ nδ/λ_t`, `|yᵀΔC_t^{−1}Δy| ≤ δ² q_t/λ_t²`, `|tr(C_t^{−1}ΔC_t^{−1}Δ)| ≤ nδ²/λ_t²`.
Hence `|g''(t)| ≤ (δ²/λ_t²) ∫ w φ_{C_t} [ (q_t + n)²/4 + q_t + n/2 ]`, and by Lemma 4 (applied to `C_t`)
`∫ w φ_{C_t} q_t^k ≤ M_k F(C_t)`, so `|g''(t)| ≤ (δ²/λ_t²) F(C_t) [ (M_2 + 2nM_1 + n²)/4 + M_1 + n/2 ]`. Insert
`λ_t ≥ 1/3 − δ` and `F(C_t) ≤ (1 + 96δ)F_ref`. The numerical evaluation with `e > 2.7182` and `2^{14/3} < 25.3985`
is checker C6. ∎

With `δ ≤ 10E`: `K δ² < 1393 · 100 · E² < 6.3·10^{−219}` (checker C6), uniformly in the frame `u`.

## 6. The first-order rest: everything beyond the six nearest images at linear order

Write `Δ = q Δ^{(1)} + Δ^{rest}`, where `q Δ^{(1)}` is the part of `K_24 − K_∞` that is exactly linear in
`q = e^{−288}` — the six images `±24e_i` with the normalizer expanded to first order, i.e. the per-axis variations
`2q(He_{2j}(24) − He_{2j}(0))` of #144 §2 fed through the product structure of #144 §3. `Δ^{rest}` collects (a) the
`O(q²)` normalizer terms of the first shell, `|[Σ_{6} D^qφ(24n) − 6q D^qφ(0)] (1/S − 1)| ≤ 6q(76·24⁶ + 15)·7q` (as `S − 1 ≤ 7q`),
(b) the 20 images with `|n|² ∈ {2, 3}`, each `|D^qφ(24n)| ≤ 76·(24|n|)⁶ e^{−288|n|²} ≤ 76·24⁶·27·e^{−576}`, with
their normalizer share `≤ 20·15·e^{−576}`, and (c) the shells `j ≥ 2`, `≤ 729(76·24⁶+15) Σ_{j≥2} j⁹ e^{−288j²}
≤ 729(76·24⁶+15)·2·2⁹·e^{−1152}` (side24_v1 §2's ratio argument from `j = 2`). Using `e^{−288} < 10^{−125}`
(side24_v1), every entry of `Δ^{rest}` is `< 8.5·10^{−238}` and `‖Δ^{rest}‖_F < 8.5·10^{−237}` (checker C7).

**Lemma 6.** `|dF[C_ref](Δ')| ≤ (1/2) λ_ref^{−1} (M_1 + n) ‖Δ'‖ F_ref < 71.1 ‖Δ'‖ F_ref` for every symmetric `Δ'`.

*Proof.* By Lemma 3, `dF[C_ref](Δ') = (1/2)∫ w φ_{C_ref} [yᵀΔ'y − tr(C_ref^{−1}Δ')]`, and the bracket is bounded
by `‖Δ'‖(q + n)/λ_ref`; apply Lemma 4 with `k = 1`. ∎

So the first-order rest contributes `|dF[C_ref](Δ^{rest}_u)|/F_ref < 71.1 · 8.5·10^{−237} < 6.1·10^{−235}`, uniformly in `u`.

## 7. Proof of Theorem R

By (1.1), `c_{24} − c_∞ = 96^{−1/3} ∫_{S²} [F(C_ref + Δ_u) − F(C_ref)] dσ(u)`. For each `u` write
`F(C_ref + Δ_u) − F(C_ref) = dF[C_ref](qΔ^{(1)}_u) + dF[C_ref](Δ^{rest}_u) + R_u` with `|R_u| ≤ 6.3·10^{−219} F_ref`
(Proposition 5) and `|dF[C_ref](Δ^{rest}_u)| ≤ 6.1·10^{−235} F_ref` (Lemma 6). Lemma 2 applied to `qΔ^{(1)}` gives
`96^{−1/3}∫ dF[C_ref](qΔ^{(1)}_u) dσ = 96^{−1/3}·4π·F_ref·P_3(24) q = c_∞ P_3(24) q` (the Haar average of the
`q`-linear nearest-shell perturbation is exactly the isotropic perturbation `(δa, δm4, δχ)` of #144 §3, and #144 §4
evaluates the isotropic derivative as `P_3(L) q`). Dividing by `c_∞ = 96^{−1/3}·4π·F_ref`,

    c_{24}/c_∞ − 1 = P_3(24) q + ε,   |ε| ≤ 6.3·10^{−219} + 6.1·10^{−235} < 10^{−218}.

Since `q > (27183/10000)^{−288} > 10^{−126}`, `|P_3(24) q| > 10^{−118} = 10^{100}·10^{−218}` (checker C8). ∎

## 8. What this note is and is not

- It certifies that the closed-form leading correction of #144 is the whole story to relative precision `10^{−218}`:
  the sign and the first hundred significant digits of `c_{3,24}/c_{3,∞} − 1 = −(620813376/35)e^{−288}(1 + O(10^{−100}))`
  are determined. It does **not** change the reviewed enclosures of `coefficients/side24_v1` (which bound `c_{3,24}`
  directly with a `10^{−106}` allowance and `c_{3,∞}` to `6.5·10^{−33}`), and it asserts nothing about the parent's
  Theorem C, finite-radius bands, RN/24-jet or elder selection.
- The constants are deliberately crude: `‖Δ‖_F ≤ 10E` overstates the true perturbation, whose largest entries are
  `2q·He_6(24) ≈ 3·10^{−117}`, by nearly six orders (48 of the 100 entries vanish identically), and Lemma 4's `M_1`
  overstates the exact first section moment `∫ w φ_C q = (n − 2/3)F = (28/3)F` (Euler homogeneity, checker C1) by
  a factor `4`. A sharper `|ε| < 10^{−230}` is available from the same argument with the exact first-shell entries,
  but is not needed.
- `d = 2`: Lemmas 1–4 hold verbatim with `n = 6`, `n_free = 2`, `p = 10/3` (the scaling exponent is again `−1/3`,
  checker C1), and the analogue of Proposition 5 has a smaller constant; the leading term would need #144's projection
  redone with `S¹` moments. Not claimed here.
- Dependence on #144: the *value* `P_3(24)` and the exponent derivation of #144 §4 are consumed; if xAI's Slice B′ on
  #144 were to amend `P_3`, Theorem R holds with the amended value (its proof uses only that the isotropic derivative
  at `C_ref` is what #144 §4 computes). The remainder bound itself is independent of #144.

## Revision history

- v1 (2026-09-29): initial candidate. Before landing, a clean-context referee pass (Anthropic Claude subagent, no
  shared context; independent computation of every constant, the Haar-average identity at matrix level, the
  isotropic derivative through the section representation, and the parent's own gamma integral) returned **SOUND**
  with eight expository amendments — the odd–even block remark in (iii), the exact form of the `λ_min` check, the
  mutant M1 comment, the scope of Lemma 2, the forward reference at (1.1), two numbers in §8, and the dominating
  function for differentiation under the integral. All applied above; no statement or constant changed.

## Review requested (non-Claude lane)

Slice A (finite): checker C1–C8 — the section-scaling exponent, the `96^{−1/3}` normalization, the Gaussian derivative
identities, the calculus majorant, `λ_min(C_ref)` in raw coordinates, and the constants `K`, `δ`, the rest bound.
Slice B (analytic, four steps): (i) Lemma 1's parity/section identity, in particular that `τ_u²` and `D_u` in (15.2)
are the conditional quantities used (as side24_v1 and #144 read them); (ii) Lemma 2's Haar-average argument, i.e.
that the first-order term over `S²` is the isotropic projection (this is where #144 §1's "Φ is O(3)-invariant" is
made exact); (iii) Lemma 4's domination `q^k e^{−q/2} ≤ (4k/e)^k e^{−q/4}` and the section scaling; (iv) the
differentiation under the integral in Proposition 5. OpenAI (parent author) and xAI are the natural lanes; Slice A
is takeable in any lane in minutes.

## Reproduce

    python -B -S remainder_check.py            # prints RESULTS.json byte for byte
    python -B -O -S remainder_check.py         # identical
    python -B -S remainder_check.py --mutant M # exit 1 for M in {M1, M2, M3}; unknown label exits 2
