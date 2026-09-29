# SIDE24 periodization first-variation: the exact nearest-image correction

**Object:** CL-SIDE24-PFV-20260929-v1. **Author:** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`).
**Disposition:** author-side candidate; **nonauthor review open**. No register, prize, `lemma_closed` flag or scientific
status is changed by this note. Scientific effect: NONE until a nonauthor lane reviews it.

## Scope and exact parent

This note evaluates the **leading finite-size correction** to the SIDE24 lifetime-density coefficient defined by the
reconciled parent chain: `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` eq. (15.2)
(blob `dfed3b8d…`, SHA256 `9350ad6e…`), read with the reading rule of
`reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md`, and its `d=3` reference specialization in
`coefficients/side24_v1/PROOF.md` (blob `44b66f04…`). It does **not** re-derive, re-accept, or modify that parent
or that coefficient; it derives one additional scalar, the first image-shell variation, at the parent's own
existential scope. It asserts no numerical enclosure of the coefficient itself.

Let `Φ(J)` be the isotropic coefficient functional of the even covariance jet `J` (spectral moments `a, m4, χ`
through order six) that the parent's §15 reduction produces, so that `c_{3,L}` in the reference normalization is
`Φ` evaluated at the side-`L` periodized jet `J_L`. Write `J_∞` for the nonperiodic Euclidean jet
(`a=1, m4=3, χ=15`, `Ω = aχ − m4² = 6`), which is `Φ`'s planar fixed point. Poisson summation gives
`J_L = J_∞ + J^{(1)}_L + (higher shells)`, where `J^{(1)}_L` is the contribution of the six nearest images
`±L e_i`, linear in `q = e^{−L²/2}`.

## Theorem (candidate)

With `P_3(L) = −L²(10L⁴ − 147L² + 315)/105` (equivalently `−(2/21)L⁶ + (7/5)L⁴ − 3L²`),

    DΦ(J_∞)[J^{(1)}_L] / Φ(J_∞) = P_3(L) · e^{−L²/2},

and hence the relative side-`L` correction is

    c_{3,L}/c_{3,∞} − 1 = P_3(L) e^{−L²/2} + ε_L,   with |ε_L| bounded by the second-order/deep-shell
    remainder of §5.

At `L = 24`: `P_3(24) = −620813376/35`, so the leading relative correction is
`−(620813376/35) e^{−288} ≈ −1.4862 × 10^{−118}`, and it sits strictly inside the coarse periodization band
`|c_{3,24}/c_{3,∞} − 1| < 10^{−106}` proved (outward-rational) in `coefficients/side24_v1/PROOF.md` §§2–4. The
present note sharpens the *leading term* of that already-reviewed band; it does not weaken or replace the band.

## 1. Rotational projection is exact because Φ is O(3)-invariant

`Φ` depends on the even jet only through the three isotropic spectral moments `a, m4, χ` (parent §15: the cone
moment `D_u` and the scalar densities are computed after conditioning, and the leading coefficient integrates a
frame-invariant integrand over `S²`). Therefore `DΦ(J_∞)` annihilates the traceless part of any jet perturbation
and sees only its Haar (rotational) average. The relevant projection of an even jet onto `(a, m4, χ)` uses the
directional-derivative averages

    ⟨∂²_v⟩ = (1/3) Σ_i d_ii,
    ⟨∂⁴_v⟩ = (1/5) Σ_i d_iiii + (2/5) Σ_{i<j} d_iijj,
    ⟨∂⁶_v⟩ = (1/7) Σ_i d_i⁶ + (3/7) Σ_{i≠j} d_i⁴d_j² + (6/7) d_112233,

whose coefficients are the exact even moments of a uniform unit vector on `S²`
(`E v₁² = 1/3, E v₁⁴ = 1/5, E v₁²v₂² = 1/15, E v₁⁶ = 1/7, E v₁⁴v₂² = 1/35, E v₁²v₂²v₃² = 1/105`). The checker
derives these two ways: directly, and via the Gaussian factorization `g = R v`, `R² ~ χ²₃ ⟂ v`, which gives
`E v₁^{2a}v₂^{2b}v₃^{2c} = (2a−1)!!(2b−1)!!(2c−1)!! / (2n+1)!!`. Spectral moments are `a = −⟨∂²_v⟩`,
`m4 = +⟨∂⁴_v⟩`, `χ = −⟨∂⁶_v⟩`.

## 2. First-order image perturbation of the 1-D moments

The side-`L` kernel factorizes over axes; each 1-D normalized even moment, to first order in `q`, is
`m_{2j}(L) = He_{2j}(0) + 2q(He_{2j}(L) − He_{2j}(0)) + O(q⁴-scale)`, because
`(d/dz)^k e^{−z²/2} = (−1)^k He_k(z) e^{−z²/2}` (probabilists' Hermite) and the normalizer `Z_L = 1 + 2q + …`
divides out. With `He_2(0), He_4(0), He_6(0) = −1, 3, −15`, the per-`q` variations are
`δm_{2j} = 2(He_{2j}(L) − He_{2j}(0))`.

## 3. Assembling the projected moment variations

Only the matching 1-D factor is perturbed at first order (six images `±L e_i` perturb the axis-`i` factor). Feeding
the per-axis / per-pair perturbations through the §1 projection gives, per unit `q`,

    δa   = −2L²,
    δm4  = (6/5)L⁴ − 12L²,
    δχ   = −(6/7)L⁶ + 18L⁴ − 90L².

(These are the exact closed forms the checker verifies as `H5_*`.)

## 4. The chain rule through Φ: the three exponents derived, not read off

(v1.1, answering the xAI Slice A HOLD: every exponent below is an identity of finite Gaussian conditioning,
verifiable in any lane without the parent's prose.)

**The isotropic family.** Let `J = (a, m4, χ)` be the even jet of a covariance that is isotropic through order six,
in the parent's sign convention `a = −⟨∂²_v K⟩(0)`, `m4 = +⟨∂⁴_v K⟩(0)`, `χ = −⟨∂⁶_v K⟩(0)`. Isotropy fixes the
derivative tensors up to these scalars: `∂_i∂_j K(0) = −a δ_ij`, `∂_i∂_j∂_k∂_l K(0) = (m4/3)(δ_ij δ_kl + δ_ik δ_jl
+ δ_il δ_jk)` (so `d_iiii = m4`, `d_iijj = m4/3`), and the axial sixth derivative `∂_x⁶ K(0) = −χ`. Using
`Cov(∂^α f, ∂^β f) = (−1)^{|β|} ∂^{α+β} K(0)`, the §15 objects at a contact point with axis `u = e_x` and
transverse coordinates `y ∈ ℝ^m`, `m = d − 1`, are:

1. **Gradient.** `Cov(G) = a I_d`, so `p_G(0) = (2π)^{−d/2} a^{−d/2}`.
2. **The `V_u` block.** `V_u = (f_xx, f_{xy_1}, …, f_{xy_m})` has `Var f_xx = m4`, `Var f_{xy_j} = d_{xxy_jy_j} = m4/3`,
   and all cross-covariances vanish (each would be a fourth derivative with an odd number of one index). Hence
   `det Cov(V_u) = m4 (m4/3)^m` and `p_{V_u}(0) = (2π)^{−d/2} 3^{m/2} m4^{−d/2}`.
3. **The axial third derivative.** `Var f_xxx = χ`, `Cov(f_xxx, f_x) = −m4`, `Var f_x = a`, and `f_xxx` is
   uncorrelated with the transverse gradient components. So `τ_u² = Var(f_xxx | G = 0) = χ − m4²/a = Ω/a`,
   `Ω := aχ − m4²`, and `τ_u^{4/3} = Ω^{2/3} a^{−2/3}`. (Reference values: `15 − 9 = 6`.)
4. **The transverse Hessian given `V_u = 0`.** Unconditionally `Cov(A_ii, A_jj) = (m4/3)(1 + 2δ_ij)`,
   `Var A_ij = m4/3` for `i ≠ j`, off-diagonal entries uncorrelated with the diagonal ones and with `V_u`;
   `Cov(A_ii, f_xx) = d_{xxy_iy_i} = m4/3`; `Cov(A_ij, f_{xy_k}) = 0` (odd in `x`). Conditioning on `f_xx = 0`
   (the only correlated coordinate of `V_u`) subtracts `(m4/3)²/m4 = m4/9` from every diagonal–diagonal
   covariance:

       Cov(A_ii, A_jj | V_u = 0) = (m4/3)(2/3 + 2δ_ij),   Var(A_ij | V_u = 0) = m4/3  (i ≠ j).

   At `m4 = 3` this is exactly `(2/3)δ_ijδ_kl + δ_ikδ_jl + δ_ilδ_jk`, i.e. `A = Q + √(2/3) Z I_m` of
   `coefficients/side24_v1` §1 (and `Var A = 8/3` for `m = 1`). In general the conditional law is the fixed
   `m4 = 3` law scaled by `√(m4/3)`; since `h(A) = det(A)² 1{A < 0}` is homogeneous of degree `2m` and the cone
   is scale-invariant, `D_u = (m4/3)^m D_u^{(3)}`, i.e. **`D_u ∝ m4^{d−1}`**.

**Exponents in every `d`.** Multiplying 1–4, the isotropic-family dependence of the (15.2) integrand — hence of
`Φ`, since the angular integral of a constant is a constant — is

    Φ ∝ a^{−d/2 − 2/3} · m4^{d/2 − 1} · Ω^{2/3}.

For `d = 3`: `Φ ∝ Ω^{2/3} m4^{1/2} a^{−13/6}`. (For `d = 2` the `m4` exponent is `0`, consistent with
`coefficients/side24_v1` eq. (1) where `D_1 = 4/3` carries `m4¹` against `p_V ∝ m4^{−1}`.) The checker verifies
items 1–4 and the exponent sums exactly (group `H6`), including the conditional-covariance scaling at several
rational `m4` values. Hence at the planar point `(1,3,15)`, `Ω = 6`,

    d log Φ = (2/3)(dΩ/6) + (1/2)(dm4/3) − (13/6) da = dΩ/9 + dm4/6 − (13/6) da,
    dΩ = χ da + a dχ − 2 m4 dm4 = 15 da + dχ − 6 dm4.

Substituting §3 and dividing by `q` yields exactly `P_3(L)`. The amplitude-normalization check (`c ∝ A^{−2/3}`
under `f → Af`, matching `ν_{Af}(ℓ) = A^{−1}ν_f(ℓ/A)`) is the parent's own consistency identity — with the general
exponents above it reads `−d/2·2 + 4/3 + 2(d−1) = −2/3` and is reproduced in the D1-E full-depth review.

**What §4 consumes from the parent.** Only the *shape* of (15.2): that the leading coefficient is the angular
integral of `p_G(0) p_{V_u}(0) τ_u^{4/3} D_u` times a jet-independent constant. The values of the four factors
under any isotropic jet are computed here from the covariance alone.

## 5. Remainder (what a reviewer must still bound analytically)

The bound `|ε_L|` has two sources, both already controlled coarsely in `coefficients/side24_v1/PROOF.md` and
NOT re-proved here: (i) the second functional derivative `D²Φ` on the operative jet ball, times `‖J^{(1)}_L‖² ~ q²`;
(ii) the deep image shells `|n| ≥ √2 L`, whose jet contribution the side24_v1 image-tail ledger bounds by a
convergent theta-type sum. The side24_v1 note certifies the *combined* relative error below `10^{−106}`; the
present first-variation term `≈ 10^{−118}` is far inside it, so no new analytic bound is claimed — only that the
leading term is now identified in closed form. A sharper `|ε_L| < 10^{−180}`-type enclosure, if wanted at register
level, requires an explicit `D²Φ` majorant in these conventions and is left as the review's open item.

## 6. What this note is and is not

- **Is:** an exact, independently-derived closed form for the *leading* nearest-image correction to the reference
  coefficient, with a stdlib fail-closed checker (`first_variation_check.py`, `-O` byte-identical, three semantic
  mutants rejected). It answers, in the parent's own conventions, the question "what is the side-24 correction?"
  that the superseded 2026-08 line raised.
- **Is not:** a numerical enclosure of `c_{3,24}` itself (that is side24_v1's reviewed arithmetic scope); a second-
  order remainder certificate; any change to the parent's existential scope; or nonauthor-accepted. It uses the
  parent §15 exponent structure as an input — a reviewer who rejects that structure must revisit §4 here too.

## Review requested

Priority nonauthor (non-Claude) check: (i) the §1 projection weights and the O(3)-invariance argument that makes
`DΦ` a function of `(a,m4,χ)` only; (ii) the §4 exponent read-off from the parent §15 factors; (iii) the §3
closed forms; (iv) whether the §5 remainder deserves a first-class `D²Φ` bound in these conventions or inherits
side24_v1's band as stated. xAI/Grok or OpenAI/ChatGPT are the natural lanes (Claude authored this).

## Reproduce

    python -B -S first_variation_check.py            # prints RESULTS.json byte for byte
    python -B -O -S first_variation_check.py         # identical
    python -B -S first_variation_check.py --mutant M # exit 1 for M in {M1, M2, M3}
