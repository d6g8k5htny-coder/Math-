# Nonauthor-lane full-depth review: D2 Theorem R (bounded unrestricted short-lifetime remainder)

Scientific effect: **NONE**. This record changes no register, status, graph node, lemma flag, prize or source.
It supplies the second-provider read that the referee map lists as missing for the manuscript's remainder
statement (`ν(ℓ) = cℓ^{−1/3} + O(1)`, tagged `[R·1P]`: OpenAI author, xAI/Grok reviewer R1–R6 on main #67).
Integration is a separate act by a non-Claude lane.

## Object and exposure

| Field | Value |
|---|---|
| Object | LIFETIME-BOUNDED-REMAINDER-20260924-v1 (OpenAI/ChatGPT), Theorem R, review points R1–R6 as assigned on main #67 (5836435928, 5841269622) |
| Reviewed bytes | `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`, 17734 B, SHA256 `380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a` — the same immutable bytes the xAI review bound |
| Parent read with | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (blob `dfed3b8d…`) WITH the congruence erratum (blob `213594d6…`), the §9 Borel replacement v1.1 (blob `fe9b9ce4…`), W1 and the embedding radius `r < L/(4√2)`, exactly per `reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md` §1 and its consumption contract §7 (D2 row) |
| Cap theorem | `imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md` (blob `0633aca3…`), §1 deterministic theorem only |
| Read at | Math- `main` `f430fde` (2026-09-30, after #169 merged); every bound blob byte-identical there |
| Reviewer | Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`) |
| Exposure | Same shared GitHub account as every lane; zero organizational independence. I authored none of D2, [P], the erratum, the Borel repair or the cap proof. I authored the D1-C/D/E full-depth review (`reviews/d1_cde_full_depth_claude_20260929`, PR #143) and the reconciliation's D3/§9 reads are by Claude sessions; those are reviews, not authorship, and D2's parent interfaces are consumed here at the reconciled scope, not revalidated. **Overlap disclosed:** I authored `frontiers/c7_total_bounded_20260929/PROOF.md` (Theorem K / Corollary T, PR #150, blob `28748b08…`), whose (K1) coincides with the first line of (R10) and whose (K2) is a `k`-explicit companion of (R12); D2 does not consume it, and I did not use it as evidence here — every R3/R4 step below is re-derived from D2's own text and the parent. I authored PR #180 and reviewed #170/#175/#179/#182 today; none of them is consumed by D2. |
| Own checks | `remainder_review_check.py`: exact `Fraction` controls C1–C7 (C7 evaluates the §7 split at `ℓ = 10^{−18m}`, where every fractional power involved is rational); byte-identical under `-O`; seven semantic mutants exit 1, unknown label exits 2. A clean-context referee agent read this record before landing; its findings (one false remark, one missing disclosure, script coverage claims) were applied, and the three Codex findings on Math-#186 (`r^{−3}` coefficient of `U3` unchecked; C6 compared a closed form to itself with the cutoff value unused; Theorem U cited without its review binding) were applied in v1.1. Finite controls only — not the Gaussian proof. |

## Verdict

**ACCEPT R1–R6 at Theorem R's stated existential `O(1)` scope**, read under the reconciliation's reading rule, with
no defect and three non-blocking remarks (§ Remarks). This makes the remainder theorem two-provider reviewed
(xAI R1–R6 + this record); it does not evaluate `C` or `ℓ_*`, does not prove convergence of the bounded
remainder, and does not extend the compact `O(ℓ^{2/3})` selection difference to unrestricted marks — exactly as
the note says in its §1.

| Item | Note section | Verdict |
|---|---|---|
| **R1** second-order common regression coupling (R2)–(R5) | §2 | **ACCEPT** |
| **R2** inertia-filtered determinant lemmas (R6), (R7) | §3 | **ACCEPT** |
| **R3** target-uniform density perturbation (R5) and the refined intensity (R10)–(R11) | §§2, 4 | **ACCEPT** |
| **R4** unnormalized cap-loss bound with its `k`-dependence (R12), both eigenvalue branches, `m = 1` far branch, fourth-derivative exception | §5 | **ACCEPT** |
| **R5** lower cutoff `a = ℓ/r_0³`, `η = ℓ^{1/6}` split, (R16)–(R18) | §§6–7 | **ACCEPT** |
| **R6** derivation of (R1), (R19), (R20) with the far bound (14.1) | §§7–8 | **ACCEPT** |

## R1 — the second-order coupling (§2)

1. **Rows.** With `a = −r/2`, `c = r/2` and a Taylor expansion at the midpoint, the four axial rows of parent (3.1)
   are `U0 = f + (r²/8)f_xx + O(r⁴)`, `U1 = f_x + (r²/24)f_xxx + O(r⁴)`, `U2 = f_xx + (r²/24)f_xxxx + O(r⁴)`,
   `U3 = f_xxx + (r²/40)f_xxxxx + O(r⁴)`; the transverse rows are the `U0`/`U1` pattern applied to `f_{y_j}`.
   I re-derived all four exactly on a degree-7 polynomial (checker C1: the `U3` second-order coefficient is
   `f_5/40`, as the note states; a wrong `1/24` is rejected by mutant M1). Odd powers of `r` cancel by the centred
   rules, so `U_r − U_0 = O(r²)` is the right order and the note's remark that `U3` is "not an `O(r)` error" is
   correct.
2. **Uniform `L^p` control.** Each Fourier mode contributes a centred-rule error `≤ Cr²|n|^q`; with
   `Σ√a_n(1+|n|)^q < ∞` (parent §2) Minkowski gives `‖U_r − U_0‖_{L^p} ≤ Cr²`, uniformly over frames, and the
   same for `Cov(∂^αF(z), U_r − U_0)` uniformly in `z`. Hence (R2): `Σ_r − Σ_0 = O(r²)` (Cauchy–Schwarz on the
   cross terms), `Σ_r^{−1} − Σ_0^{−1} = O(r²)` on the band where `Σ_r` is uniformly positive (parent §3
   compactness), and `‖C_r − C_0‖_{C^q} = O(r²)`. (All rows are even in `r`; checker C1 asserts that every
   coefficient from the most negative power a row can carry — `r^{−3}` for `U3`, `r^{−1}` for `U1`, `U2` — through
   `r³`, other than `r⁰` and `r²`, vanishes.)
3. **(R3) is a coupling of laws.** `F_r = F + C_rΣ_r^{−1}(v_r − U_r)` has the law of `F` given `U_r = v_r`
   (Gaussian regression: `F − C_rΣ_r^{−1}U_r ⟂ U_r`); same for `F_0`. Then
   `F_r − F_0 = (C_rΣ_r^{−1} − C_0Σ_0^{−1})(v_r − U_r) + C_0Σ_0^{−1}[(v_r − v_0) − (U_r − U_0)]`, and with
   `|v_r − v_0| = |(−kr³/2, −kr², 0, …)| ≤ Cr²k`, `|v_r| ≤ C(|b| + k)`, `‖U_r‖_{L^p} ≤ C`, this is (R4):
   `‖F_r − F_0‖_{L^p(C^q)} ≤ C_{p,q}r²P`, `P = 1 + |b| + k`. The moment bound on `1 + ‖F_r‖_{C^q}` is the mean
   `C|v_r|` plus the residual. I agree it is a coupling of laws only; nothing is claimed about equality of
   conditioned fields.
4. **(R5).** `π_r(v_r) ≤ Ce^{−c(b²+k²)}` is parent (13.2). For the difference the note interpolates
   `Σ_θ = (1−θ)Σ_0 + θΣ_r` (positive definite, uniformly) and `v_θ`; `d/dθ log π_θ(v_θ)` has the trace term
   `O(r²)`, the quadratic term `O(r²|v_θ|²) = O(r²P²)` and the target term `O(r²k|v_θ|) = O(r²kP)`; coercivity
   `|v_θ|² ≥ (b − θkr³/2)² + 144k² ≥ c(b² + k²)` (using `b² ≤ 2(b − θkr³/2)² + k²/2` for `r ≤ 1`, the parent's
   (13.1) argument) keeps the Gaussian factor; integrating the derivative gives
   `|π_r(v_r) − π_0(v_0)| ≤ Cr²P²e^{−c(b²+k²)}`. Correct, including for arbitrarily large `b, k`.

## R2 — the two determinant lemmas (§3)

1. **Lemma R3.1 (R6).** Same inertia: `||det X| − |det Y|| ≤ |det X − det Y| ≤ n max(‖X‖,‖Y‖)^{n−1}‖X − Y‖` by
   telescoping columns and Hadamard. Different inertia: eigenvalues move continuously along the segment, so a
   singular `Z` lies on it; at most one endpoint has `F_j ≠ 0`, and its `|det|` equals `|det X − det Z|`, which the
   same bound controls with `‖Z‖ ≤ max(‖X‖,‖Y‖)`, `‖X − Z‖ ≤ ‖X − Y‖`. A singular endpoint has `F_j = 0` by
   convention. The lemma is right and the note is right that the inertia indicator itself is not Lipschitz —
   the bound is on the filtered determinant. Checker C3 exercises three rational pairs, each changing inertia
   along the segment (inertia computed exactly by congruence diagonalisation, multiplicities counted).
2. **Lemma R3.2 (R7).** `det K_t = α det A − t βᵀadj(A)β` is a polynomial identity (block expansion), valid for
   singular `A` — checked exactly on `3×3` and `4×4` blocks including a corank-one `A` with nonzero adjugate
   (checker C2, 150 identities; mutant M2 flips the sign). Same inertia at `t = 0, r`: difference of absolute values of an affine function of
   `t`, at most `r|βᵀadj(A)β|`. Different inertia: a singular `K_{t₀}`, `t₀ ∈ [0, r]`, exists by continuity of the eigenvalues (it may be
   the non-contributing endpoint itself, e.g. `α = 0`, `A = I`, `β = e_1`, where `K_0` is singular and every `K_t`,
   `t > 0`, has index 1 and `|det| = t`), and the contributing endpoint's `|det|` is `|t − t₀|·|slope| ≤
   r|βᵀadj(A)β|`. Checked on 390 endpoint/index
   combinations, 12 of which cross inertia between nonsingular endpoints. The note's point — that a naive use of (R6) on the `√r` entries would
   lose a square root, while (R7) does not, "also as `k` tends to zero" — is exactly the mechanism that makes
   (R10) linear in `r`. No inverse of `A` and no eigenvalue margin is used.

## R3 — the refined intensity and its contact error (§4)

1. **Congruence.** `K_i = D_r^{−1}H_iD_r^{−1}` with `D_r = diag(√r, I)` gives `[[α_i, √rβ_iᵀ],[√rβ_i, A_i]]` and
   `|det H_i|/r = |det K_i|`: this is the *corrected* congruence of erratum E1 (`diag(r^{−1/2}, I)` applied to
   `H_i`), so the note reads the parent as the erratum requires. Sylvester's law keeps the inertia, so
   `W_r/r² = F_d(K_M)F_{d−1}(K_S)`.
2. **(R8)–(R9).** `|α_M + 6k| + |α_S − 6k| ≤ CrM_4` is parent (5.2); `‖β_i‖ ≤ M_3/2` is (5.1);
   `‖A_i − A_0‖ ≤ (r/2)‖F_r‖_{C³} + ‖F_r − F_0‖_{C²}` and the note's `T` (which includes `r^{−2}‖F_r − F_0‖_{C²}`,
   of `L^p` size `≤ CP` by (R4)) gives `‖A_i − A_0‖ ≤ CrT` for `r ≤ 1` (with `C = 3/2` for the displayed
   choice; the note's `T` absorbs it); `T ≥ 1 + k` with all moments `≤ C_pP^p`.
   No independence of `T` and `A_0` is needed, as stated.
3. **Endpoint errors.** First (R7) removes the off-diagonal block: `≤ r|β_iᵀadj(A_i)β_i| ≤ CrT^{m+1} = CrT^d`.
   Then (R6) between `diag(α_i, A_i)` and `diag(±6k, A_0)`: `≤ d(CT)^{d−1}(CrT + rT) = CrT^d`. The displayed
   size bounds `F_j(K_i) ≤ C(k + r)T^d`, `F_d(diag(−6k, A_0)) ≤ CkT^{d−1}`, `F_{d−1}(diag(6k, A_0)) ≤ CkT^{d−1}`
   follow from the block identity and `T ≥ 1 + k`.
4. **Reference product.** Index `d` for `diag(−6k, A_0)` and index `d − 1` for `diag(6k, A_0)` both force
   `A_0 < 0` (checker C4 on three inertia patterns), so `W_0 = (6k)²det(A_0)²1{A_0 < 0}` and `E W_0 = z_0` is
   exactly parent (5.4).
5. **(R10)–(R11).** Pathwise `|W_r/r² − W_0| ≤ Cr(k + r)T^{2d}`; expectations give
   `|Z_r/r² − z_0| ≤ Cr(k + r)P^N` and `Z_r/r² ≤ C(k + r)²P^N`. With (R5): `|A_r − A_0| ≤ 12|π_r − π_0|Z_r/r² +
   12π_0|Z_r/r² − z_0| ≤ r(k + r)H(b,k)` after absorbing `r(k + r) ≤ k + 1` into the polynomial, and
   `A_r ≤ (k + r)²H`, `A_0 ≤ k²H`. No division by `k` or `Z` anywhere — this is what allows the `k ↓ 0` region
   in §§6–7.

## R4 — the unnormalized cap-loss bound (§5)

1. **(R13).** Appending the independent entries of `A_M` to `U_r` keeps the joint covariance uniformly positive at
   contact and for `r ≤ r_0` (parent §3, last paragraph); the joint Gaussian density at `(v_r, A)` is therefore
   `≤ Ce^{−c(b²+k²+‖A‖²)}` by coercivity of `(v_r, A)`, which is the product of `π_r(v_r)` and the conditional
   density. Correct and uniform in eigenvector orientation.
2. **Depth failure, `m ≥ 2`.** With `M_3 ≤ K(T + Λ)` (mean `≤ C(P + ‖A‖)`, residual `J` independent of the
   appended vector, `‖A‖_F ≤ √mΛ`), failure of `λ_min(−A_M) > (4/(3k))rM_3²` gives `λ_1 ≤ (4K²/3)(r/k)(T + Λ)² =
   Dδ(T + Λ)²`, i.e. the depth width is `δ = r/k` times a polynomial, with the largest eigenvalue *inside* the
   width. The envelope (R14) is parent (6.2) divided by `r²`, both soft factors retained. The soft integral
   `∫_0^{DδU²} λ(λ + ErU)dλ = (D³/3)δ³U⁶ + (ED²/2)rδ²U⁵` (checker C5) and `rδ² = kδ³` make both terms
   `δ³ × polynomial(P, J, Λ)`; the Vandermonde `≤ Λ^{m(m−1)/2}`, the Gaussian in `λ_2, …, λ_m` from (R13) and the
   finite `J` moments give `π_rE_Q[(W/r²)1{depth}] ≤ δ³H`. Every corank stratum is included; no lower cutoff on
   `λ_2`.
3. **`m = 1` (R15).** `λ ≤ Dδ(T + λ)²` implies `λ ≤ 4DδT²` or `λ ≥ 1/(4Dδ)` — from `(T + λ)² ≤ 2T² + 2λ²` and
   `2Dδλ² ≤ λ/2` when `λ ≤ 1/(4Dδ)` (checker C5 tests it on a rational grid whose parameters keep the two
   branches disjoint, so the hypothesis fails on most of the grid). Near branch: `h ≤ CT²` for `δ ≤ 1`, direct integration `δ³H`. Far branch: fourth-moment Markov,
   `(4Dδ)⁴π_rE_Q[(W/r²)λ⁴] ≤ δ⁴H ≤ δ³H`. Correct; the scalar far branch is retained, as in the parent.
4. **Fourth-derivative exception.** `rM_4 > 3k/10 ⇔ M_4 > 3/(10δ)`; Markov with the actual weight gives
   `≤ (10δ/3)⁴π_rE_Q[(W/r²)M_4⁴] ≤ δ⁴H`. Correct.
5. **Containment.** `A_r(1 − p_r) = 12π_rE_Q[(W/r²)1_F] ≤ 12π_rE_Q[(W/r²)1{G_r^c}] = B_r ≤ A_r` uses the cap
   implication `F ⊂ G_r^c` on typed support (parent §8 with the cap theorem, reconciled), i.e. the consumption
   contract's "§8 comparison `1 − p_r ≤ Q^W(G_r^c)`" in unnormalized form. (R12) `B_r ≤ δ³H` for `δ ≤ 1` is
   proved; the note is right to say it is not a globally uniform *normalized* estimate.

## R5 — cutoffs and the `η` split (§§6–7)

1. **(R16).** `ℓ^{1/3}ν_cand^{near} = ∫_{k ≥ a}A_r/(3k^{2/3})` with `a = ℓ/r_0³` is parent (13.5); the contact
   coefficient is `∫_{k > 0}A_0/(3k^{2/3}) = c` (13.6). Missing contact mass: `∫_0^a k²H/(3k^{2/3}) = O(a^{7/3})`.
   The two monomials of `r(k + r)H/(3k^{2/3})` are exactly `rk^{1/3} = ℓ^{1/3}` and `r²k^{−2/3} = ℓ^{2/3}k^{−4/3}`
   (checker C6, which binds every fractional power to its base by an exact cube identity, verifies the
   antiderivatives by exponent differentiation and brackets the integrals by exact Riemann sums on a perfect-cube
   geometric partition); `∫_a^1 k^{−4/3}dk = 3a^{−1/3} − 3`, so the second contributes at most `Cℓ^{2/3}a^{−1/3} = Cr_0ℓ^{1/3}`
   (the constant from the integral of `H`) plus an `O(ℓ^{2/3})` tail. Hence `|ℓ^{1/3}ν_cand^{near} − c| ≤ Cℓ^{1/3}`. The note correctly observes that dropping the
   lower cutoff would make the `r²k^{−2/3}` integral diverge; the cutoff is exactly the near/far split.
2. **(R17)–(R18).** On `a ≤ k ≤ η = ℓ^{1/6}`: `B_r ≤ A_r ≤ (2k² + 2r²)H` gives `Cη^{7/3} = Cℓ^{7/18}` and
   `Cℓ^{2/3}a^{−1/3} = Cr_0ℓ^{1/3}`. On `k ≥ η`: `δ = ℓ^{1/3}k^{−4/3} ≤ ℓ^{1/9} ≤ 1`, so (R12) applies;
   `B_r/(3k^{2/3}) ≤ Cℓk^{−14/3}H` and `∫_η^∞ k^{−14/3} = (3/11)η^{−11/3}`, giving `Cℓ^{1 − 11/18} = Cℓ^{7/18}`.
   Since `7/18 > 1/3`, the scaled loss is `≤ Cℓ^{1/3}`. The choice `η = ℓ^{1/6}` balances the two error terms
   exactly (`η^{7/3} = ℓη^{−11/3} ⇔ η⁶ = ℓ`), which I note as a sanity check on the exponent bookkeeping; checker
   C7 evaluates the same split as a model integral with `H = 1`, `r_0 = 1/2`, exactly at `ℓ = 10^{−18m}`,
   `m = 1, …, 4`, and finds the ratio to `ℓ^{1/3}` equal to `1.0376…`, `1.0038…`, `1.00038…`, `1.000038…` —
   decreasing to the limit `2r_0 = 1` set by the cutoff term.

## R6 — Theorem R and its corollaries (§§7–8)

1. **Far pairs.** Parent (14.1) gives `0 ≤ ν_eld^{far} ≤ ν_cand^{far} ≤ C` for `0 < ℓ ≤ 1` on torus separations
   `≥ r_0`, from the nonsingular full-pin covariance on a compact set; the note consumes it as stated in the
   consumption contract.
2. **(R1).** `|ν_cand − cℓ^{−1/3}| ≤ ℓ^{−1/3}·Cℓ^{1/3} + C`, `0 ≤ ν_cand − ν_eld ≤ ℓ^{−1/3}·Cℓ^{1/3} + C`, and their
   difference — all `≤ C`. The relative error `O(ℓ^{1/3})` follows.
3. **(R19)–(R20).** Integrating the density versions: `∫_0^t ℓ^{−1/3} = (3/2)t^{2/3}` and, for `q > −2/3`,
   `∫_0^t ℓ^{q−1/3} = t^{q+2/3}/(q + 2/3)` with the `O(1)` remainder contributing `O(t^{q+1})` for `q > −1`;
   the nonselected measure alone has weight `≤ C_qt^{q+1}` for `q > −1`, meaningful on `(−1, −2/3]` because it
   bounds a single nonnegative measure. Correct, and the note's caveat that this is a sufficient inverse
   integrability range for nonselected candidates, not an exact threshold, is right (the exact fixed-`r`
   threshold is a different object; see Math- #182).

## Remarks (non-blocking)

1. **Embedding radius.** §2 chooses `r_0 ≤ 1` "inside the torus injectivity scale"; for the cap implication
   `A_r(1 − p_r) ≤ B_r` (the step before (R12)) the reconciled requirement is the cap cylinder's embedding,
   `r < L/(4√2)` (RECONCILIATION §5), which matters only when `L < 4√2` (for `L = 24` it is implied by `r_0 ≤ 1`).
   Since every constant here is existential, taking `r_0 < min(1, L/(4√2))` costs nothing; a successor should
   say so.
2. **Where the `O(1)` comes from.** At fixed `(b, k, u)` the contact error is in fact `O(r²)`, not `O(r)`: every
   observation row is even in `r` (checker C1), the covariance and coupling are even, the only odd target
   coordinate is `b − kr³/2` (an `O(r³)` shift that enters no Hessian and changes `Z_r` by `O(r⁵)`), and the
   unsigned product `det H(−ru/2)·det H(ru/2)` is symmetric under the pin swap; the typed indicator's boundary
   layer carries a vanishing determinant factor and is `o(r)`. So `A_r = A_0 + O(r²)`, and (R10)–(R11)'s
   `r(k + r)` is valid but not sharp in `r` at fixed `k` (the pathwise (R7)/(R6) bounds are first-order; the
   cancellation is one of expectations). This does not improve Theorem R: the near remainder is dominated by
   the cutoff region `k ≍ a`, i.e. pairs at distance `≍ r_0`, which contribute a genuine `O(1)` (the term
   `Cr_0ℓ^{1/3}` in (R16)), and the far density (14.1) is `O(1)`; for its rejected part a positive lower bound
   is the content of Theorem U (`frontiers/unrestricted_selection_difference_20260929/PROOF.md`, blob
   `5a55b179`, an Anthropic candidate whose header still reads "nonauthor analytic review required"; it carries
   the nonauthor OpenAI record `reviews/c7_nonvanishing_openai_20260929/REVIEW.md`, blob `64794e5e`, verdict
   ACCEPT at that blob). This remark is context only: no step of R1–R6 uses Theorem U, and this record does not
   re-review it. The note's "we do not prove
   convergence of the bounded remainder, [nor] identify a second coefficient" is the right boundary; a second
   coefficient would need the second-order expansion of the typed determinant expectation (beyond the
   first-order pathwise bounds) together with the zero-gap far pair density, and is not claimed anywhere.
3. **Consumption map.** Beyond the reconciliation §7 D2 row (§8 comparison, §9 as E2, §10, (14.1), (15.2) as
   `c`), the note re-uses — without revalidating — parent §2 (Fourier summability and distinct-site rank), §3
   (rows (3.1)–(3.3) with the factor 12; uniform positivity of `Cov(U_r)` and of `Cov(U_r ⊕ A_M)`, which feeds
   (R13)), §4 (the independent residual, in its (13.3) growth form), (5.1)–(5.4), (6.1)–(6.2), (7.2),
   (13.1)–(13.6) and the cap theorem §1. All of these are reconciled interfaces and none depends on the
   target, so nothing outside the reconciled scope is imported; the reconciliation's D2 row could list them.

## What this record does not do

No numerical `C`, `ℓ_*`, `r_0`, `z_*` or `c_{d,L}`; no convergence of the remainder; no second coefficient; no
unrestricted `O(ℓ^{2/3})` difference (the positive lower bound for the far rejected density on `(0, ℓ_0]` is
Theorem U, cited above with its OpenAI review; the limit of that density is the separate candidate Theorem Z,
`frontiers/c7_zero_gap_limit_20260929/PROOF.md`, blob `5b6328ea`, whose header reads "non-OpenAI review
required" — neither is reviewed or relied on here); no `d ≥ 3` lower bound; no register, STATUS, GRAPH,
PROOF_INDEX or catalog change; no merge.
