# Continuum crosswalk: every held step, its planar line, and its `d`-dimensional replacement

Review aid for the `d >= 3` continuum read of CL-D5-DIMENSION-LIFT-20260929-v1. Scientific effect NONE; this file
asserts no verdict. It lists, for each continuum step that the xAI Slice A and Slice B records hold (Math-#141
comments 5894274124 and 5894406926), the exact planar line it lifts, the place in `PROOF.md` where the
`d`-dimensional argument is written, and the only things that change. Planar line numbers refer to the byte-pinned
sources of `SOURCE_MAP.json`: [PP] blob `d8acf0bc`, [CP] blob `b5647907`, [IW] blob `f53a527c`.

Verdict columns record what is already on file; they are not claims. "xAI planar" refers to the planar (P2)
continuum record 5894512272 (Grok: (P10), (P11), (P12), (P18), region II ACCEPT for the planar source, no `d > 2`
transfer) and to #111; "xAI lift" refers to Slice A/B on this packet. Identities and rank claims accepted by Slice A/B
are listed only where a continuum step depends on them. "OpenAI A+B" refers to the OpenAI nonauthor review 5357858391
(bound to `c709854`): ACCEPT of every pending row of tables A and B at fixed `d`, fixed torus, compact marks and small
`r`, subject to the accepted algebraic lemmas, hence Theorems P_d and C_d analytically discharged at that source;
source-exposed (the reviewer authored the planar [PP]/[CP] inputs), with the xAI planar record as the independent base.
"OpenAI C" refers to the follow-up OpenAI nonauthor review 5357882570 (same binding `c709854`): ACCEPT of every pending
row of table C and of the analytic G_d composition at that source, same scope; with it the crosswalk A+B+C is complete.
Its one wording clarification (the §6.5 "axis bound" is the axis-safe endpoint-short-column/Hadamard bound valid
throughout the small strip) is written into `PROOF.md` §6.4–§6.5.

## A. Pin ball, Theorem P_d (§4), planar source [PP]

| Step | [PP] line | `PROOF.md` | What changes in `d` dimensions | Verdicts on file |
|---|---|---|---|---|
| (P4) axial Hermite expansion of `g'(rp)` | 115 | §4.2, first bullet | Nothing: `g(x) = f(x, 0)` is scalar in every `d`. | planar ACCEPT (#111 (P4)) |
| (P7) remainders `ε_1`, `ε_2` | 143 | §4.2, (4.1') with the four-bullet derivation | Vector-valued: `h = grad_y f(·, 0) ∈ R^m` handled componentwise; transverse Taylor remainders `R_3`, `R_2` written with `|y|^3`, `|y|^2`; same powers, constants carry `sqrt(m)` and tensor norms. | lift: derived in this packet (answers the Slice A flag) |
| (P8) error ratios `‖R‖_{L^s} ≤ C_s r` | 162 | §4.2 last paragraph, §4.3 remark after (4.3) | Nothing: the six ratios use only `Δ ≥ |q|`, `Δ ≥ r|p|`. | planar ACCEPT (continuum record n2) |
| (P9) frame floor `det ≥ 9/131072` | 187 | (4.4), block-Schur | `det(BB^T) ≥ (9/64)^{d-1}/2048` via Lemma D3; equals the planar constant at `d = 2`. | lift ACCEPT (Slice A identity) |
| (P10) Schur/compactness floor `c_0 I ≤ Σ ≤ C_0 I` | 193 | (4.5) and the sentence before it | `J` has `2 + 2m + m(m+1)` entries (orders 4, 3, 2, 3), none in `E_0`; positivity by distinct one-site monomials ([LP] §2); compactness over `O(d) × {|p| ≤ 1/4} × S^{d-1}`; `λ_min(BB^T) ≥ det(BB^T)/λ_max^{d-1}` from (4.4); the centered `L^2` triangle inequality with (P8) is unchanged. | xAI planar ACCEPT (P10); lift ACCEPT (OpenAI A+B, item 1) |
| (P11) density `≤ C r^{-3} Δ^{-2} e^{-cχ^2}` | 210 | (4.6) | Jacobian `r^{d+1} Δ^d` in place of `r^3 Δ^2` (the map `grad f ↦ Y` is `diag(r^2Δ, rΔ I_m)`); the mean `dvec` is axial and unchanged; `|dvec + z|^2 ≥ |dvec|^2/2 - |z|^2` in `R^d`. | xAI planar ACCEPT (P11); lift ACCEPT (OpenAI A+B, item 2) |
| (P12) conditional moment `E[K^6 | grad f(X) = 0] ≤ C(1 + χ^6)` | 217 | (4.7) | Same regression on `Y`; stated for every `n` (used at `n = 3d`); cross-covariances through order three bounded by Cauchy–Schwarz and (4.5). | xAI planar ACCEPT (P12); lift ACCEPT (OpenAI A+B, item 2) |
| (P13)–(P14) normalizer `Z_r ≥ c_Z r^2` | 241, 249 | §4.5 | Replaced by [LP] (5.5), which holds in every fixed `d` (accepted as A1–A4 in the D1 reconciliation, Math-#106). | consumed at its accepted row |
| (P15)–(P16) angle-sensitive product | 261, 289 | (4.8) | Lemma D1 replaces the `2 × 2` two-column bound at each Hessian; new factor `K^{3(d-2)}`; segment identity (P15) is one-dimensional. | lift ACCEPT (Slice A, Lemma D1) |
| (P17) angle-free product | 308 | (4.9) | Lemma D2 (Hadamard) in place of the planar two-column bound. | lift ACCEPT (Slice A, Lemma D2 is Hadamard) |
| (P18) weighted Kac–Rice at the zero level | 323 | §4.7, (4.10) | Field `grad f : X → R^d`, parameter and value dimensions agree; same mark `W_r 1{H_X ∈ O_j}`; same framework citation. | xAI planar ACCEPT (P18); lift ACCEPT (OpenAI A+B, item 3) |
| (P19) region I | 341 | (4.11) | `|q|^2 Δ^{-d} ≤ |q|^{2-d}` supplies the weight `ω_d`; `χ^2 ∈ [t^2/2, t^2]` unchanged; `n = 3d` in (4.7). | lift ACCEPT (OpenAI A+B, item 4; ledger identity Slice A) |
| (P20) region II | 361 | (4.12) | Pointwise `r^{-2-4d}` and absorption `2n ≥ 5 + 3d` in place of the planar sixth term; axis included; no division by `q`. | xAI planar ACCEPT (region II); lift ACCEPT (OpenAI A+B, item 4) |
| Integration and Lemma D5 | 367 | §4.8 "Integration", Lemma D5 | Weight `ω_d` integrable: radial exponent `(2-d) + (m-1) = 0`; nested ball `O(r^5)`. | lift ACCEPT (Slice A, weight only) |
| §10.1 reflection to `S` | 377–386 | §4.9 | Any orthogonal transverse map; `b̃ = b - kr^3`, `k̃ = -k`; the original `Z_r` retained. | lift ACCEPT (OpenAI A+B, item 5) |

## B. Collar, Theorem C_d (§5), planar source [CP]

| Step | [CP] line | `PROOF.md` | What changes in `d` dimensions | Verdicts on file |
|---|---|---|---|---|
| §3 degree-five interpolation, three sites | 61–85 | §5.1 | Explicit families `h_i, d_i, e_{i,j}` in `d` variables; generic projection direction. | lift ACCEPT (Slice B, rank) |
| (C4)–(C6) coarse floor `Cov(V_r) ≥ c r^{10} I` | 95, 109, 116 | (5.1) | `3(d+1)` observations; `dim P_5 = C(d+5, 5)`; same `r^5` floor versus `r^6` remainder; principal submatrix and Schur complement unchanged. | lift ACCEPT (OpenAI A+B, item 6) |
| (C7) midpoint expansion `G_1, G_2` | 133 | (5.2) with the sentence after it, and §6.3 (6.2)–(6.3) at `s = r`, `ε = 1` | Vector form: `u v·T_3`, `v^T C_3 v`, `S_0 v`; derived from the vector-valued endpoint identities (6.2), written componentwise in §6.3. | lift: derived in this packet |
| (C8)–(C10) drift, variance, Mahalanobis | 138, 142, 148 | §5.3 | First physical coordinate only; `(C10)` is Cauchy–Schwarz in the covariance inner product in any dimension. | lift ACCEPT (OpenAI A+B, item 7) |
| (C11)–(C13) near-axis strip | 157, 161, 167 | §5.4 | Prefactor `r^{-5d}` (from `det Σ_X ≥ c r^{10d}`), moment `r^{-30d}` (for `K^{3d}`), pointwise `r^{-2-35d}`, absorption `2n/3 ≥ 5 + 34d`. | lift ACCEPT (OpenAI A+B, item 7) |
| (C14)–(C15) frame `B` and `c v^4 ≤ Cov(G) ≤ C v^2` | 180, 193 | §5.5, (5.3) | `BB^T ≥ diag(|v|^4/4, (|v|^2/2) I_m)` by Lemma D3 in place of the explicit `2 × 3` rows; the same `r/|v|^2 ≤ r^{1/3}` perturbation. | Lemma D3 ACCEPT (Slice A); floor use ACCEPT (OpenAI A+B, item 8) |
| (C16)–(C17) density and moment | 198, 202 | (5.4), (5.5) | Jacobian `r^{d+1}`; prefactor `|v|^{-2d}`; moment `|v|^{-12d}`. | lift ACCEPT (OpenAI A+B, item 8) |
| (C18) three soft Hessians | 208 | (5.6) | Lemma D1 with `σ = 1` on the orthonormal pair `(e_x, v̂)`; factor `K^{3(d-2)}`. | lift ACCEPT (Slice B, D1 use) |
| (C19) ledger | 214 | (5.7) | `r^{3-d}` per unit scaled volume; `|v|^{-(14d+6)}` absorbed by `e^{-c/|v|^2}`. | ledger identity accepted; count ACCEPT (OpenAI A+B, items 8–9) |
| §8 compact remainder | 218–223 | §5.6 | Fixed singular-value floor of `B` for `|v| ≥ v_0`; unchanged. | lift ACCEPT (OpenAI A+B, item 8) |
| (C20) Kac–Rice and gluing | 231, 235–242 | §5.7 | `dX = r^d du dv`; the two punctured balls and the collar with `η = 1/4`. | lift ACCEPT (Slice B, tiling bookkeeping) |

## C. Shells, Theorem I_d (§6), planar source [IW]

| Step | [IW] line | `PROOF.md` | What changes in `d` dimensions | Verdicts on file |
|---|---|---|---|---|
| (I6)–(I8) endpoint inputs and shell | 73, 88, 94 | §6 preamble | [LP] (4.1), (5.5) in every `d`; `U_r` extended by the `2m` transverse rows. | consumed at accepted rows |
| §3.1 rank through confluence | 96–147 | §6.1 | Explicit confluent families with determinants `-|v|^{2d+2}` and `u^{2d+6}`; degree-four negative control. | lift ACCEPT (Slice B, rank) |
| (I9)–(I11) remainder and floors `c s^{10}` | 124, 149, 153 | (6.1) | `(d+1)`-dimensional `Σ_X`; the divided-difference argument is one-dimensional along the axis and is applied to each transverse component. | lift ACCEPT (OpenAI C, item 1) |
| (I12) endpoint identities at the midpoint | 167 | (6.2), now with the componentwise derivation in §6.3 | Vector-valued: `grad_y f(0) = -r^2 T_3/8 + O(r^4 K)` and `grad_y f_x(0) = O(r^2 K)` componentwise from the symmetric Taylor formulas; axial identities unchanged. | lift: derived in this packet |
| (I13)–(I16) expansions, row operation, target | 179, 185, 192, 197 | (6.3), (6.4), the Jacobian `s^{d+4}` | Vector form; the row operation subtracts `(s/2) v·grad_y f`; target `τ_{d+1}` bounded through `ε → 0`; exact finite control `RO` in `d = 3`. | lift: derived; `RO` exact |
| (I17)–(I18) Euler identity and `|S_0|` | 208, 212 | (6.5), (6.6) | Euler degree three in every `d`; controls the quadratic form `v̂^T S_0 v̂` only (one entry, not the matrix). | lift ACCEPT (OpenAI C, item 2; finite control `EU` in `d = 3`) |
| (I19) endpoint determinants | 218 | (6.7), (6.8) | Lemma D4 with the gradient equation `|S_0 v̂| ≤ C s K/|v|` supplying the transverse column; same shape `(r + s^2)/|v|^2`. | Lemma D4 and the shape ACCEPT (Slice B); constants ACCEPT (OpenAI C, item 3) |
| (I20) witness determinant | 223 | (6.9) | Lemma D1 on `(e_x, v̂)`. | lift ACCEPT (OpenAI C, item 3) |
| (I21)–(I22) combined product, axis bound | 230, 236 | (6.10) and the sentence after it | `K^{3d}`; on the axis Lemma D2 with `e_x`. | lift ACCEPT (OpenAI C, item 3; axis-safe reading written into §6.4) |
| (I23)–(I26) small axial strip | 245, 258, 264, 270 | §6.5 | Prefactor `s^{-5(d+1)}`, moment `s^{-30d}`, strip volume `O(s^d) ≤ O(s^2)`. | lift ACCEPT (OpenAI C, item 4) |
| (I27)–(I30) transverse floor, density, moment | 279, 290, 297, 301 | (6.11), (6.12), (6.13) | `BB^T ≥ diag(|v|^4/4, (|v|^2/2) I_m, |v|^6/144)` by Lemma D3; `det ≥ c|v|^{2d+8}`; `σ_min(B) ≥ c|v|^3`; prefactor `|v|^{-(d+4)}`; moment `|v|^{-18d}`. | Lemma D3 ACCEPT; floor use ACCEPT (OpenAI C, item 5) |
| (I31)–(I32) shell ledger | 311, 319 | (6.14), (6.15) | `s^{-(d+2)}` in place of `s^{-4}`; `r` powers `-2 + 2 + 3 = 3`, `s` powers `-(d+4) + 2 + d = -2`. | ledger arithmetic ACCEPT (Slice B); count ACCEPT (OpenAI C, item 6) |
| (I33) marked Kac–Rice with height disintegration | 334 | §6.8 | Same framework; `(grad f(X), f(X))` nondegenerate on the closed shell by (6.1). | lift ACCEPT (OpenAI C, item 7) |
| (I34) dyadic sum | 347 | §6.8 | Unchanged. | lift ACCEPT (Slice B) |

## D. What "pending" means here

After OpenAI reviews 5357858391 (tables A, B) and 5357882570 (table C) no row of this crosswalk is pending; the
verdict columns record the item of the review that covers each row. Before those reviews, every pending row is a `d`-dimensional instance of a planar step whose planar version now carries a nonauthor
ACCEPT (xAI 5894512272 for the pin ball; `reviews/d5_collar_count_20260928/` for the collar; `reviews/d5_i5_planar_f_20260928/`
for the shells), with the change listed in the fourth column. A reader can therefore check each row by (i) confirming
the planar step at the cited line, (ii) confirming that the fourth column is the complete list of changes, and (iii)
confirming the exponent arithmetic in `RESULTS.json` (groups `L`, `W`) where it applies.

The three clarifications of reviews 5357858391 and 5357882570 are written into `PROOF.md`: the unscaling step of §5.2 is the
congruence and the Schur variational identity, not an eigenvalue-monotonicity claim under entrywise scaling; and the
collar constants depend on the fixed `d`, `R`, `eta` and the mark compacts (§5.7), with nothing uniform as `d` grows;
and the axis bound of §6.4 is stated as the axis-safe endpoint-short-column/Hadamard bound `W_r |det H_X| / Z_r <= C K^(3d)`
valid throughout `|v| <= s^(1/8)`, which is what §6.5 uses.
