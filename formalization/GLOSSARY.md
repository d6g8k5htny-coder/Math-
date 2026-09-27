# Formal glossary — project terms to standard mathematics to Lean

**Scientific effect: NONE.** This table renames nothing in the sources. It maps each project-specific term to the standard mathematical object it denotes and to the Lean/Mathlib carrier that formalizes it (or records that none exists yet). A term that cannot be mapped is either ill-defined or genuinely new; novelty must then be justified against the literature, not assumed.

Columns: **Project term** as used in the proofs · **Standard mathematics** · **Lean carrier** (`✓` present, `spec` specified as a `Prop`/`def` only, `—` none yet) · **Where the term is defined informally**.

## Gaussian lifetime / SIDE24 family (D1–D3)

| Project term | Standard mathematics | Lean carrier | Informal source |
|---|---|---|---|
| SIDE24, SIDE24 periodized Gaussian model | Centered stationary Gaussian random field on the torus `(ℝ/24ℤ)^d`, `d ∈ {2,3}`, variance one, covariance `K_24(z) = Σ_{n∈ℤ^d} e^{-|z+24n|²/2} / Σ_n e^{-|24n|²/2}` (periodization of the Bargmann-Fock kernel) | — (field not formalized; the coefficient enters as parameter `c24`) | [PROOF.md](../coefficients/side24_v1/PROOF.md) "Scope and exact parent"; parent [UNIFORM_MATRIX_CAP_AND_LIFETIME.md](../imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md) |
| Bargmann-Fock (unperiodized) covariance | `K_∞(z) = e^{-|z|²/2}` on `ℝ^d`; the reference covariance | — | PROOF.md §1; certificates `bf_six_pin_*` |
| Lifetime (of a bar), lifetime density | Length `ℓ = f(M) − f(S)` of a finite bar in the superlevel-set `H₀` persistence barcode of the field, where `M` is the local maximum that births the bar and `S` the index-`(d−1)` saddle that kills it; the lifetime density is the expected number of such bars per unit volume per unit `ℓ` | — | Parent Theorem C; [LIFETIME_REMAINDER.md](../frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md) |
| Lifetime coefficient `c_{d,24}` | The constant `c_{d,L}` in parent Eq. 15.2: leading coefficient of the small-lifetime asymptotic `ν(ℓ) ~ c ℓ^{-1/3}`-type law, expressed as a finite Gaussian/angular integral after eliminating birth and gap | `spec` (`MathFormalReal.Side24.cRef` is the *reference* coefficient; the periodic one is the parameter `c24`) | PROOF.md "Scope and exact parent"; parent §15 |
| Reference coefficient `c_{d,ref}` | `Γ(7/6)(3/2)^{1/3} D_{d−1} / (2√3 π^{d−1} √π)`: the same expression evaluated for `K_∞` | ✓ `MathFormalReal.Side24.cRef` | PROOF.md §1 display (1) |
| Cone moment `D_m` | `E[det(A)² 1{A ≺ 0}]` for the `m×m` Gaussian symmetric matrix `A = Q + √(2/3) Z I_m` (GOE-type `Q`, independent scalar `Z`): the expectation of the squared determinant restricted to the negative-definite cone | ✓ values `MathFormalReal.Side24.coneMoment` (`4/3`, `29/6 − √6`); the integral definition — | PROOF.md §1 |
| Elder rule, elder pairing, elder partner | The pairing of critical points by the elder rule of persistent homology: when two superlevel components merge at a saddle, the younger (lower-birth) one dies; the surviving component is the elder. An "elder partner" of a maximum is the saddle that kills its bar | — | Parent §§8–9; Curry arXiv:1706.06059 §3 |
| Elder mark, Borel elder mark | The measurable indicator (a mark in the marked point process of critical points) recording whether an ordered maximum/saddle pair is an actual elder pairing | — | Parent §8; [Section 9 Borel repair](../reviews/d1_section9_borel_repair_20260925/REPAIR.md) |
| Candidate density `ν_cand` vs elder density `ν_eld` | Intensity (per unit volume) of *all* ordered maximum/saddle pairs with given height difference, vs the intensity of those pairs that are elder pairings; the latter is a conditional/marked intensity of the former | — | Parent Theorem B |
| Birth mark `b`, gap mark `k` | `b = f(M)` (height of the maximum) and `k = (f(M) − f(S))/r³` (height gap scaled by the cube of the pair distance `r`) | — | Parent §11; remote-window PROOF.md §1 |
| Pin, pinned maximum/saddle, full pin Jacobian | Conditioning the Gaussian field on `∇f(M) = ∇f(S) = 0` and on the heights `(f(M), f(S))`; the Jacobian is the change of variables `(M,S) ↦ (z, h)` with polar separation `r^{d−1} dr dσ(u)` and height factor `r³ db dk` | — | Parent §11 |
| Marked Kac-Rice | The Kac-Rice (Rice) formula for the expected number of zeros of `∇f` weighted by a measurable mark; background Armentano–Azaïs–León arXiv:2304.07424 | — | Parent §9; remote-window PROOF.md §5 |
| Image sum, omitted periodic images | The terms `n ≠ 0` of the lattice sum defining `K_24`; bounded uniformly in PROOF.md §2 | ✓ constants `MathFormalCore.Side24.imageConstant_eq`, `sixtyE_lt_eps`, `exp_neg_288_lt` | PROOF.md §2 |
| Odd block | The `2×2` covariance `[[1,−3],[−3,15]]` of `(∂₁f, ∂₁³f)` at a point for `K_∞` | ✓ `oddBlock_traceDet`, `oddBlock_minEigen_gt_third` | PROOF.md §3 |
| Outward rational arithmetic, `10^{-80}` grid | Interval arithmetic over `ℚ` with endpoints rounded away from the interval to multiples of `10^{-80}` | ✓ endpoints `refLo2`… and `transfer_d2/d3`; the interval library itself — | PROOF.md §5; `coefficient.py` |

## RN critical-point counting family (D4–D5)

| Project term | Standard mathematics | Lean carrier | Informal source |
|---|---|---|---|
| RN (RN closure, global RN theorem) | The project's target statement that, conditional on the pins, no other critical point of index `j` lies in the shrinking height window between the pinned maximum and saddle with probability `1 − O(r^5)`-type; "RN count interface" separates the event probability from the expected count | — | [RN_COUNT_INTERFACE.md](../frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md) |
| Height window (between-pin) | The interval `(f(S), f(M))` of heights; shrinking with `r` since `f(M) − f(S) = k r³` | — | Remote-window PROOF.md §1 |
| Witness, witness collision | A "witness" is an additional critical point in the height window; "collision" refers to two witnesses (or a witness and a pin) at vanishing separation, where factorial-moment bounds are not uniform | — | Remote-window PROOF.md §6 |
| Contact kernel `Λ_j` | The continuous positive density factor in the Kac-Rice integrand for an index-`j` critical point at location `x`, conditional on the pins, evaluated at the "contact" (limit) covariance | — | Remote-window PROOF.md §5 |
| Fixed remote region `D_ρ` | The set of points at distance at least `ρ` (independent of `r`) from both pins | — | Remote-window PROOF.md §1 |
| Mesoscopic scaled annulus, thin tube, pin neighborhood, intermediate scale `r ≪ |x| ≪ ρ` | Spatial regions of the count integral expressed in the scaled variable `y = x/r`: `1 < A ≤ |y| ≤ B` (annulus), `|y| ≲ 1` (pin neighborhood), and the uncovered bridge between the annulus and the fixed remote region | — | [GRAPH.json](../frontiers/downstream_gate_20260925/GRAPH.json) region nodes; PROOF_INDEX.md |
| 24-jet, JETMOD, CH-LIFT, Piece-2, `H5` rim | Historical D0 obligations: finite-jet (derivatives through order 24) certificates and their modular/lifting decompositions from earlier project phases. Not defined in the current public proofs; carried as `OPEN_HISTORICAL`/`BLOCKED_ABSENT` graph nodes | — (formalization requires recovering the absent carriers first) | GRAPH.json `hist.*` nodes; [D0 audit](../reviews/d0_custody_audit_20260926/) |
| Six-pin covariance, `Var(f_ts(M) | six linear pins)/r²` | Conditional variance of a mixed second derivative given six linear functionals of the field at two points | — (`formal_kernel_checked: false` recorded in the certificate) | [certificates/](../certificates/) |

## P15 / price-budget family (D6)

| Project term | Standard mathematics | Lean carrier | Informal source |
|---|---|---|---|
| P15 | The project's open problem family on covering "obstructions" of a downset by cheap generators under independent product measures | — | [P15_REALIZED_COVERS.md](../frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md) |
| Downset `D`, realized family, capacity `a_i`, demand `d_i`, clutter `H` | `D ⊆ 2^X` closed under subsets; the realized family is `D = {U : |U ∩ X_i| ≤ a_i ∀i, supp(U) contains no edge of H}` with disjoint blocks `X_i`, `|X_i| = n_i`, block demand `d_i`; `H` is an antichain (clutter) of block-index sets each of size ≥ 2 | — | Full-price PROOF.md §1 |
| Obstruction `O_K(D)`, palette `K`, `K_H(d)` | Sets not partitionable into `≤ K` members of `D` ("K-colourable" fails); `K_H(d)` is the least `K` admitting palette sizes `|P_i| ≥ d_i` with empty intersection over every `H`-edge | — | Full-price PROOF.md §1 |
| Generator, generator-cover price | A set `g ⊆ X`; a family of generators covers `O_K(D)` if every obstruction contains one; its price is `Σ_g Π_{v∈g} c_v` | — | Full-price PROOF.md §1 |
| Hazard | `−log μ_p(D)` where `μ_p` is the product Bernoulli measure with parameters `p_v`: the negative log-probability that a random set lies in `D` | — | Full-price PROOF.md §2 |
| Transformed price `c_v ≤ φ(p_v)` | Price cap as a function of the vertex probability; `φ` is the explicit transform of the price-budget theorem | — | [price_budget PROOF.md](../frontiers/price_budget_20260924/PROOF.md) |
| `3e-2`, `ρ* = 1/[3 − log(3e − 2)]` | ASCII for `3·e − 2` (not `0.03`); `ρ*` is the sharp uniform factor of Theorem F | — | [ASCII_3E_MINUS_2.md](../frontiers/full_price_20260924/ASCII_3E_MINUS_2.md) |

## Process vocabulary (not mathematics)

| Term | Meaning | Where enforced |
|---|---|---|
| Author-side, nonauthor review, organizational independence | Governance roles of the two-key rule; see [REVIEW_TOPOLOGY](https://github.com/d6g8k5htny-coder/governance-/blob/main/REVIEW_TOPOLOGY.md) | `claims/LANDING_CLAIMS.json`, `reviews/` |
| `lemma_closed`, prizes, premises | Scientific registers held outside this repository; always `false`/unchanged here | Every validator |
| `kernel_checked`, alignment review, lane verdict | Layer 1 vocabulary defined in [README.md](README.md) | `formalization/formal_gate.py` |

## Adding a row

When a proof introduces a term not in this table, add the row in the same PR as the proof or its formalization, with the standard object spelled out. If the standard object cannot be named, say so explicitly in the row; that is a finding, not a formatting gap.
