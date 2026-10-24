## A3.8 Slice 3 — PASS_SCOPED_CONDITIONAL on the rate assembly; notation correction and source reconciliation

**Dylan Roy — delegated AI mathematical review. Actual performer OpenAI / GPT-6 Astra Pro**, session `qs-a38-rate-audit-20261006`, pickup6007792473. Nonauthor of Claude's A3.8; earlier QS work and the contemporaneous Slice2 report are visible. Not blind; same-account organizational-independence credit0; scientific effect NONE. No source write, merge or accepted-status change.

**Source:** frozen A3.8 comment6007704303 (created/updated01:52:57Z), controls6007706590 (01:53:09Z). The author-declared body hashes are afd2271252aa66c7e99f8fd7cb5ad194d881a56dcddcb9c726438f879b2c6451 and c12bbbc241648bcf61850c3f134bddc5e02557f4f786ddc1433f358047fce88a; I read the native text but have NOT freshly recomputed those two body hashes. Direct runtime GitHub retrieval failed DNS. Relevant A3.4/A3.6/A3.7 definitions and proof steps were fetched directly, rather than inferred from a diagonal formula.

### 1. Exact verdict boundary

The thirteen-term ledger, Proposition6.1's measure conversion, both schedules, admissibility checks, total-mass consequence and conditional-law normalization are correct **given the displayed input estimates/certificates and their uniformity**. I found no rate-changing error in §6. This does not independently discharge Slices1/2 or A3.3/A3.4/A3.7, identify a published lifetime coefficient, prove a log-free endpoint, extend to d≥4, or prove optimality of the underlying stochastic rate.

**A38-S3-NOTATION-01 (minor required clarification):** §0 explicitly defines measures on **X=R×R×[0,π)×R^9**, but the total-mass expressions in §0 and QFE3's proof use R^11. The angle has not been marginalized in the stated object. Please use **ν(X)** consistently for total mass, or explicitly define a separate angular marginal. Replacing R^11 by X is the source-preserving correction; no rate or Gaussian integral changes. This item is not a counterexample to the estimates, but remains a wording amendment until author readback. In particular do not silently drop dθ in the coefficient.

### 2. Ledger and normalization

I read A3.6 §0, M3(g), Good^E(3.1), and A3.7 CorollaryLE3(3.2)/§5. The rejected good event needs the radius, value-error and local-endpoint conditions. The elder event needs the radius, barrel, reduced-height tolerance and two Hessian controls. A3.7 replaces exactly the two level-band charges of the older elder proof. Their complements map to all nine rows of A3.8's table and its thirteen unique summands; no inverse hard-gap term is silently dropped by the assembly. Proof of the H-dependent *bounds* for these rows remains the other slices' scope.

On the covered sector the two deterministic certificates give the symmetric-difference containment. With μ_r=r^-5 E[W·1_D] and Z_r=r²z_r, **r^-3 Q_r^W(V∩D)=μ_r(V)/z_r**: the normalizer is divided out once. The z_r floor is Λ-independent by the stated input. On T∩{γ≠0}, F_r and Rsec are complements of H_r and E relative to that sector, up to the stated null sets; leakage off T is charged separately. For |φ|≤1 this gives the bad-mass term plus ∫_D |g_r/z_r−g_0/z_0|. The variation norm has **no 1/2** in this source. Tail restriction adds ν_r(D^c)+ν_0(D^c), with no unjustified cancellation of positive masses.

Taking φ=1 gives |r^-3(1−p_r)−α^(3)|≤ε_r. Since α^(3)≥M_*>0, ε_r≤M_*/2 gives m_r≥M_*/2 and

`||ν_r/m_r−ν_0/m_0||_var ≤ 2 ε_r/m_r ≤ 4 ε_r/M_*`.

This establishes exactly the conditional raw-jet statement, not full-field or persistence-event transfer.

### 3. QFE3: every closed form and the whole β interval

Writing a summand as r^a H^h w^j, the substitution is **a−hα−jβ/8**, with α=(2−3β)/16. In the order of (6.1), I independently obtain:

`β; (2+13β)/8; 1/2+β/4; 1/2+5β/4; 1−β/2; (2+21β)/16; (26−7β)/16; (14−5β)/4; 2+β/2; 3/2+β/4; 1+5β/4; (10+5β)/16; (10+19β)/16`.

These match all thirteen displayed entries. Their differences from β are affine and nonnegative at both endpoints0,2/3, which certifies the entire interval—not merely the author's60 sampled β values. The mα and far-tail terms are ≥β with **m=ceil(16β/(2−3β))**, and1>β.

I also reconstructed the eleven α upper bounds, in H-carrying ledger order:

`(2−β)/12, (2−3β)/8, (6−5β)/32, (1−β)/7, (2−2β)/3, (4−3β)/4, (3−2β)/8, (4−3β)/8, (8−5β)/32, (4−5β)/12, (12−9β)/56`.

Their exact lower envelope is **min{(1−β)/7,(2−3β)/8}**, switching atβ=6/13, both1/13. Piecewise-affine endpoint comparison on[0,6/13] and[6/13,2/3] proves no other constraint lies below it. The chosen α has slack: `(1−β)/7−α=(2+5β)/112>0` and `(2−3β)/8−α=α>0`. All six side-condition exponents are positive on0<β<2/3. Atβ=2/3 the balanced radius/band/margin terms are tight and any positive power-law layer growth violates the margin bound. This is a limitation of this ledger/schedule, not a lower bound on the true remainder.

**Optional consequence, not a new claimed theorem or required change:** because the note already identifies this envelope, one can choose α_max itself and m=ceil(β/α_max), reducing the sufficient *polynomial-tail moment order* compared with the convenient half-sized schedule. α_max≤1/7 preserves rH^4→0. Constants still depend on that fixed chosen order; this does not justify β depending on r or remove the endpoint logarithm.

### 4. ER3: every endpoint monomial

For w=r^-1/12 H^-1/3, e=r^2/3 H^-4/3, η_LE=2K2 r^5/6 H^-2/3, the thirteen (r,H) exponent pairs are:

`(2/3,8/3), (4/3,22/3), (2/3,8/3), (4/3,22/3), (2/3,−4/3), (1,7), (4/3,1/3), (8/3,−4/3), (7/3,16/3), (5/3,8/3), (11/6,22/3), (5/6,7/3), (17/12,20/3)`.

Each matches the source. Dividing by r^2/3 H^8/3, the balanced pair is1, the extra e term isH^-4≤1, and every other ratio contains a strictly positive power of r times a fixed power of H. They vanish because **H grows logarithmically**, not for arbitrary H. Taking D_*≥max{1,1/c_actual,1/c_model} makes the two supplied exponential tails O(r). All side conditions hold for sufficiently small r. The error in1−p_r is multiplied by r³ exactly once, giving **r^11/3 log(1/r)^8/3**. At fixed Λ the minimum is2/3 with η exponent5/6 and its square-root charge17/12, as A3.7 §5 actually states. Dropping constant H powers for exponent bookkeeping is not setting the admissible H=1 in the actual measure definition.

### 5. New execution after runtime recovery; original controls only read by me

Initial Python/container calls failed before execution, as disclosed at pickup. A later container recheck succeeded. I then wrote and ran a **separate stdlib/Fraction reviewer probe** from the thirteen monomials, not a substituted copy of `a38_exact.py`.

Fourteen recorded commands (baseline,five named mutants,invalid argument, each normally and with-O) produced expected exits; every paired stdout/stderr is byte-identical. Baseline verifies26 affine coefficient equalities,26 whole-interval endpoint inequalities,44 piecewise-envelope inequalities,all13 endpoint monomials/log comparisons,six admissibility certificates,1000 chosen-tail orders and1000 optional-tail orders,3969 finite positive-measure mass inequalities and3503 conditional-normalization cases,plus exact breakpoint/ordered-coordinate controls. Finite measure examples supplement—not prove—the preceding general inequality.

Mutants deliberately corrupt the power-law α, density H power, endpoint H schedule, endpoint w power or ordered-eigenvalue choice. They reject with their exact expected `RATE_CHECK_FAIL` group, exit1, empty stdout; invalid label exits2. None is a crash counted as intended rejection. Probe SHA256 **69f0d0a69eb511351ce468a87d13cfdbd9449388ce79ad5dfd03f418292e32ea**; baseline stdout SHA256 **f977238a6e87b8812ecb3ea4d24209b0de2470a6702fa8c71cb8667cb0f61c67**.

I read original groupsZ1,Z2,Z7 and dispatch/failure code. Z1 samples60 interior βs plus endpoint/crossover controls; Z2 checks exponent pairs and balance; Z7 checks the fixed-layer minimum and endpoint charges. M1/M2/M3/M12 have the stated algebraic detection reasons. **I did not execute the full original39305-control script or authenticate its bytes locally.** The separate Slice2 reader reports that complete normal/-O execution; those are that reader's runs. No local Lean, full-field simulation, coefficient integration or hidden claim of control-complete source review here.

### 6. Slice2 ordering concern: source evidence, not an overwritten verdict

My source clarification **6007893752** points to A3.4 **5999129544 §0**, which explicitly defines λ₁≤λ₂ and λ̃=kλ₁/r; its eigenframe is the λ₁-eigenline. A3.6/A3.8 import that convention. Thus the larger-eigenvalue labeling in Slice2's schematic objection is outside the actual coordinate image; at r=10^-6,k=1,spectrum{10^-6,10^-2}, the defined λ̃=1, not10^4. This is why I do not adopt that schematic point as a counterexample to the consumed ordered-coordinate implication. The positive-part Jacobian is a consistent secondary check, not the sole source of the definition.

The Slice2 reader owns its own corrected or maintained verdict after reading that exact definition. **This review does not automatically erase its BLOCK or independently accept all of Lemma5.1/5.4.** No whole A3.8 theorem is promoted by a correct conditional rate assembly. Preserve the separate Slice1 uniform-H audit, upstream conditions, and the source-derived/author-side status of the coefficient.

**RELEASE:** Slice3 claim6007792473 is delivered and released. Remaining narrow follow-up is the notation readback and reconciliation of the ordered-coordinate objection by its actual reader/author. No further unchanged rate review, competing implementation, new worker, timer or owner-approval loop is requested.