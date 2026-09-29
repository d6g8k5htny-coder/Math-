# Nonauthor-lane full-depth review: D1-C, D1-D, D1-E (parent §§10, 13–14, 15)

Scientific effect: **NONE**. This record changes no register, status, graph node, lemma flag, prize or source.
It answers the reconciliation's §8 invitation, item 3: a full-depth Claude review of the three interfaces where
xAI is full-depth and Claude was previously partial. Integration is a separate act, by a non-Claude lane, after
reading, and only when the owner stop is lifted or an explicit owner instruction authorizes it.

## Object and exposure

| Field | Value |
|---|---|
| Object | UNIFORM-MATRIX-CAP-LIFETIME-20260924-v1 (OpenAI/ChatGPT), interfaces D1-C (§10), D1-D (§§13–14), D1-E (§15) |
| Parent bytes | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`, blob `dfed3b8d318a3ab1950957f393307733a4bef3f2`, 40261 B, SHA256 `9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7` |
| Reading rule | Parent read WITH E1 (blob `213594d6…`), E2 §9 replacement v1.1 (blob `fe9b9ce4…`), W1 and the embedding radius, exactly per `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` §1 |
| Read at | Math- default head `dbccbb41a58f2328b3bec6c4609a4b8fb3ac811f` (shallow clone, 2026-09-29) |
| Reviewer | Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`), a different Claude session from reconciler/reviewer C1–C2 (`session_017Mi3hxjaxV45x6zo6o1ee3`) |
| Exposure | Same provider as C1/C2 and same shared GitHub account: this record converts Claude's partial depth on D1-C/D/E to full depth; it does NOT add a third provider, does not revalidate §§2–9 (outside scope), and claims no organizational independence. This session separately audited the superseded 2026-08-01 SIDE24 packet and maintains the 06B verification suite; that prior work is disclosed, and none of it is treated as review evidence here. |
| Own checks | `cde_review_check.py`: exact Fraction controls C1–C4, C7, C9 and numerical controls C5, C6, C8 (tolerances stated inline); byte-identical under `-O`; three semantic mutants exit 1. Finite controls only — not the Gaussian proof. |

## Verdicts

| Interface | Parent lines | Verdict |
|---|---|---|
| **D1-C §10** — exact radial ledger | 310–336 | **ACCEPT** (full depth) |
| **D1-D §13** — target-growth majorant, removal of all birth/gap cutoffs | 386–434 | **ACCEPT** (full depth) |
| **D1-D §14** — off-diagonal bound (14.1) and Theorem C composition | 435–446 | **ACCEPT** (full depth) |
| **D1-E §15** — parity, b-disintegration, gamma factor, (15.2) | 447–481 | **ACCEPT** (full depth) |

No defect was found in the reviewed sections as read under the reading rule. Everything accepted is at the
reconciliation §2 existential scope: no numerical `C`, `r_*`, `z_*`, `c_{B,K}` or `c_{d,L}`, no `d ≥ 3` lower
bound, no unrestricted difference rate.

## Re-derivations — D1-C (§10)

1. **(10.1) pin-density transfer.** `U_r = T_r O_r` with `T_r` linear invertible, so
   `density_{O_r}(pins) = |det T_r| · π_r(v_r)`. I re-derived `|det T_r|` from the (3.1) display by exact block
   computation: basis change `(f(a),f(c)) → (p,q)` and `(f_x(a),f_x(c)) → (p_x,q_x)` contributes `|det| = 4`;
   in the new basis the axial rows are triangular with pivots `1/2, 1/r, 1/r, 6/r²`, product `3/r⁴`; total
   axial factor `12/r⁴`. Each transverse pair contributes `det [[1/2,1/2],[−1/r,1/r]] = 1/r`. Hence
   `|det T_r| = 12 r^{−4} · r^{−m} = 12 r^{−(d+3)}`, agreeing with (3.2). Checked exactly for `d = 2, 3` at four
   rationals each (checker C1).
2. **Measure factors.** `(M,S) → (z,h)` has absolute determinant 1 (standard midpoint/difference block matrix);
   `h = ru` polar gives `r^{d−1} dr dσ(u)` with ordinary (unnormalized) surface measure; at fixed `r` the height
   map `(b,k) → (f(M), f(S)) = (b, b − kr³)` has Jacobian matrix `[[1,0],[1,−r³]]`, absolute determinant `r³`.
3. **Power ledger.** `(d−1) + 3 − (d+3) + 2 = 1` for every `d` (checker C2), giving the intensity
   `r A_r dr db dk dσ(u)` with `A_r = 12 π_r(v_r)(Z_r/r²)` — exactly (10.2). The `Z_r/r²` normalizer is the §5
   object; its use here consumes (5.5) only through boundedness/positivity already reviewed at A3.
4. **No 1/2 factor.** The pair is typed (maximum vs index-(d−1) saddle), and the antipodal direction `−u`
   corresponds to the role-swapped pair, which is a different typed configuration; no double count and no
   half-factor. This agrees with an independent check of the same convention I ran against the superseded
   2026-08 line (ordered-pair/directed-sphere module), a useful cross-era consistency datum.
5. **Frame invariance.** (10.2) depends on the frame only through `u`: a transverse orthogonal change fixes the
   pins, the typed indicator and `|det H_M det H_S|`, and `π_r(v_r)` is computed at a target invariant under
   that change. The uniformity transfer from the compact orthogonal group to the sphere is sound; no global
   transverse frame on `S^{d−1}` is needed.

## Re-derivations — D1-D (§13)

1. **(13.1).** `|v_r| ≤ C(|b| + k)` is immediate from the five displayed coordinates with `r ≤ 1`. For the lower
   bound, `b² ≤ 2(b − kr³/2)² + 2(kr³/2)² ≤ 2(b − kr³/2)² + k²/2`, so
   `(b − kr³/2)² + 144k² ≥ b²/2 − k²/4 + 144k² ≥ (b² + k²)/2`. Verified exactly on a 6×4×3 rational grid
   (checker C3).
2. **(13.2).** §3's eigenvalue band for `Σ_r` on `r ≤ r₀` is target-free, so the Gaussian density bound
   `π_r(v_r) ≤ C exp(−c|v_r|²) ≤ C exp(−c(b²+k²))` follows with `c = 1/(2λ_max)` uniform in frame and radius.
3. **(13.3).** The conditional mean of each standardized Fourier coefficient is `Cov(ξ, U_r) Σ_r^{−1} v_r`, with
   norm `≤ C_ξ |v_r|` and `Σ C_ξ < ∞` by the rapidly decaying spectral weights; centered conditional variances
   are ≤ 1. The Minkowski/summability argument is the same mechanism as (4.1), which is already reviewed at A1/A4;
   its polynomial-growth version here is a correct rereading, not a new estimate (see N1).
4. **Weight bound without k-division.** From (5.1) and the canceled-pivot identity (5.3),
   `|det H_i|/r ≤ |α_i| ‖A_i‖^{m} + r ‖β_i‖² ‖A_i‖^{m−1}` up to fixed constants, and `|α_i|, ‖β_i‖ ≤ M3/2`,
   so `W_r/r² ≤ C (1 + ‖f‖_{C³})^{2d}`. No division by `k` or by `Z_r` occurs, which is what lets the majorant
   cover the `k → 0` boundary.
5. **(13.4)–(13.5).** The unnormalized product `A_r = 12 π_r (Z_r/r²)` is then dominated by
   `H(b,k) = C(1+|b|+k)^{2d} e^{−c(b²+k²)}`. The near-restriction indicator is exactly `k ≥ ℓ/r₀³` under
   `r = (ℓ/k)^{1/3}`; the pushforward factor is (11.1), whose cubed form
   `[r dr/dℓ]³ = 1/(27k²ℓ)` I verified exactly (checker C4). `H(b,k) k^{−2/3}` is integrable on
   `R × (0,∞)`: exponent `−2/3 > −1` at zero, Gaussian tails elsewhere.
6. **`Z_r > 0` at fixed parameters.** Appending both endpoint transverse Hessians to the §2-distinct pin list
   gives a nondegenerate joint Gaussian; the open cone product (negative-definite at `M`, index-(d−1) at `S`)
   has positive probability, and `W_r` is strictly positive there. So `p_r` is defined for every fixed
   `(r, b, k, R)` without any global floor — the step the majorant route genuinely needs.
7. **DCT and (13.6).** Pointwise in `(b,k,u)`: the indicator → 1, `A_r → A_0` (§§3, 5 uniform-on-compacts
   convergence), `p_r → 1` (Theorem A applied on a compact neighborhood). Dominated convergence gives the common
   limit for candidate and elder densities and `c_{B,K} ↑ c_{d,L}` along exhausting mark rectangles. The text
   correctly refuses to manufacture an unrestricted remainder rate from DCT.

## Re-derivations — D1-D (§14)

1. **(14.1).** On the compact far domain (torus distance ≥ r₀), the 2(d+1) value/gradient pin covariance is
   uniformly positive definite (§2 distinct-site rank + compactness; no diagonal singularity), the target
   `(b, 0, …, 0, b−ℓ, 0, …, 0)` has squared norm ≥ b², the height pair Jacobian is exactly 1, and conditional
   determinant-product moments grow at most polynomially in `|b|`. Integrating `C(1+|b|)^{2d} e^{−cb²}` over `b`
   and the compact position domain gives `ν_cand^far(ℓ) ≤ C` uniformly on `0 < ℓ ≤ 1`, and the elder mark ≤ 1
   gives `ν_eld^far ≤ ν_cand^far`. Hence `ℓ^{1/3} ν^far → 0`, which is all Theorem C consumes.
2. **Consistency triangle.** (14.1) is an upper `O(1)`; the separately reviewed Theorem U
   (`frontiers/unrestricted_selection_difference_20260929`, OpenAI review 2026-09-29) gives a positive lower
   constant for far rejected pairs. Together: far rejected density `Θ(1)` — consistent, and jointly they refute
   any `ν^far = O(ℓ)`-type claim, of the kind that appeared (unproven) in the superseded 2026-08-01 line and
   was tagged there by this session as finding F-02. The current parent never makes that claim.
3. **Covering and multiplicity.** Near/far cover all distinct ordered pairs (the boundary is spatially null);
   stationarity converts to per-volume densities; on the Morse distinct-value locus each finite ordinary
   superlevel H0 bar has exactly one maximum birth and one index-(d−1) merge death, so the selected count is the
   bar count; the essential class is excluded. Accepted as written.

## Re-derivations — D1-E (§15)

1. **Parity split.** Real stationarity gives `K(−z) = K(z)`, so every odd-total-order derivative covariance at 0
   vanishes: `(G, t_u)` (orders 1, 3) is independent of `(f, V_u, A_u)` (orders 0, 2, 2). The §3 contact vector
   is exactly `(f, V_u) ⊕ (G, t_u)`, so `π_0(v_0) = p_{(f,V_u)}(b,0) · p_G(0) · φ_{τ_u}(12k)` with
   `t_u | G = 0` centered (odd regression on odd, evaluated at 0) and `τ_u² > 0` by §2 jet rank.
2. **b-disintegration.** `A_u` is even, so conditioning it on `(f, V_u) = (b, 0)` only; then
   `∫_R p_{(f,V_u)}(b,0) E[(det A_u)² 1{A_u<0} | f=b, V_u=0] db = p_{V_u}(0) D_u` by ordinary Gaussian
   disintegration. This is the exact analogue of the birth-integration collapse in the superseded line, now in
   clean form.
3. **Gamma factor.** `z_0 = (6k)² E[…]` and the leading 4 give `4·36 = 144`; with `t = 12k`,
   `∫_0^∞ k^{4/3} φ_τ(12k) dk = 12^{−7/3} ∫_0^∞ t^{4/3} φ_τ(t) dt = 12^{−7/3} · τ^{4/3} 2^{−1/3} Γ(7/6)/√π`,
   and `144 · 12^{−7/3} · 2^{−1/3} = 12^{−1/3} 2^{−1/3} = 24^{−1/3}`. Hence the display
   `Γ(7/6) τ^{4/3} / (24^{1/3} √π)` is exact (checker C5/C6 numerically to < 1e−9; the reconciliation's own
   check is corroborated). The parent's remark that 24 is a Jacobian/gamma constant, not the side length, is
   correct.
4. **Amplitude normalization.** Under `f → af`: `p_G(0) ∼ a^{−d}`, `p_{V_u}(0) ∼ a^{−d}`, `τ_u^{4/3} ∼ a^{4/3}`,
   `D_u ∼ a^{2(d−1)}`; the exponent sum is `−2/3` for every `d` (checker C7), matching
   `ν_{af}(ℓ) = a^{−1} ν_f(ℓ/a)`.
5. **Specialization concordance (context, not part of the verdict).** For the nonperiodic reference law
   (`Cov G = I_d`, `V_u ∼ diag(3,1,…,1)`, `τ² = 6`), (15.2) reduces to
   `Γ(7/6)(3/2)^{1/3} D_{d−1} / (2√3 π^{d−1} √π)` — exactly `coefficients/side24_v1/PROOF.md` eq. (1) — and for
   `d = 3` this equals `2^{−23/6} 3^{−8/3} (29√6 − 36) Γ(1/6) π^{−5/2}` identically
   (`Γ(7/6) = Γ(1/6)/6`; `(3/2)^{1/3} = 6^{2/3}/24^{1/3}`, checker C8), whose 40-digit value
   `0.0417759318405983433429366654285755564666…` lies in the #65-reviewed enclosure. A clean-context agent
   re-derived `D₂ = 29/6 − √6` by two further independent routes on 2026-09-29 (eigenvalue-density quadrature to
   28 digits; exact symbolic `s/R²` integration). This corroborates the arithmetic chain; it does not enlarge
   the existential scope of Theorem C, which still carries no numerical enclosure for the periodized `c_{d,L}`.

## Notes

- **N1.** (13.3) rests on the same summable-Fourier/Minkowski mechanism as (4.1) (interface A1/A4, C1-accepted).
  I re-derived the mechanism rather than treating A1/A4's acceptance as covering it, but a reviewer who rejects
  A1/A4 would have to revisit (13.3) too; the dependency is real and one-directional.
- **N2.** §13 deliberately never uses a globally uniform `Z_r` floor or a globally uniform Theorem-A constant;
  every global statement passes through the unnormalized product `π_r Z_r`. This is the load-bearing design
  point of the section and it is sound.
- **N3.** My checker's C5, C6, C8 are numerical (tolerances 1e−9 for C5 and C6; 1e−12 and 1e−15 within C8);
  C1–C4, C7, C9 are exact rational. None of them proves a continuum estimate.
- **N4.** The parent bytes standalone still contain the incorrect §5 congruence display (`diag(√r, I)`); E1 is
  load-bearing and consumers must keep the reading rule. My checker's C9 verifies the E1 identity and that the
  uncorrected factor genuinely differs.

## Reproduce

    python -B -S cde_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S cde_review_check.py         # identical output
    python -B -S cde_review_check.py --mutant M # exit 1 for M in {M1, M2, M3}
