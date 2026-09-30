# Nonauthor review of the radial moment consequences

Reviewer: OpenAI / Codex subagent `/root/workflow_bottleneck_audit`.
Date: 30 September 2026.

**VERDICT: ACCEPT (M2)–(M9), including the positive-tail divergence statement, as conditional consequences of the exact specified PR176 tail, smoothness and coefficient inputs. No blocking amendment found. This is not another Slice B verdict.**

I did not draft or amend this consequence manuscript or its control script. I read the frozen consequence, the exact PR176 proof, the source/custody map, and the exact controls after the derivation was delivered. Same provider and shared-account/source exposure imply zero organizational-independence credit. The author's prior power/log/quantile formulas are expressly credited by the manuscript; I make no novelty claim for them.

## Exact object

- `MOMENT_CONSEQUENCE.md`: 11,110 bytes; SHA256 `29bba56b56fd3223a2ea71d012f9abe04eb30240bc5bbfe8f5b131e0bba6f4dd`; Git blob `fb3bef3a9a46cc0135a88bae6c26e1bade4e7384`.
- `COROLLARY_CUSTODY.json`: SHA256 `b532794b61e6ffd5539ce9f7dc5509b44d04d2c238a14f33e214c8e387532a64`.
- Consumed PR176 proof: head `71772a8906cf6663d16be2cd5f63e5d4ebdcee2b`, blob `65f24b1f9a7b80522a2ee059f5f6877c9f970f0d`, SHA256 `a3693664900e23e1e763d88a0b5609936a6f31d844cbe6f18c7d0379b94ba710`.

All nine custody-listed artifacts and all four declared source bodies matched their recorded sizes and hashes; source Git blob identities also matched. The observation file is `IDENTITY_AND_CONTROL_OBSERVATIONS.json`.

## Analytic reconstruction

1. The consumed remainder really has the strength used here: PR176(17) is uniform for q≥1 with an O(t^-4 q^-11) tail envelope. The consequence does not derive unbounded moments from unweighted total variation. It keeps the already-formed microscopic point-intensity law, conditioning at R>t, and the original source normalization.

2. For a positive power p<11, nonnegative tail integration yields 1+p∫q^(p-1)S_t(q)dq. For p<0, absolute integrability follows already from S_t≤1 and ∫_1^∞q^(p-1)dq<∞. Thus the same signed identity holds throughout p<11, including the separate exact p=0 case. Inserting the uniform remainder gives a bound |p|K/(11-p)t^-4. The displayed correction is p c[1/(13-p)-1/(11-p)] = -2pc/[(13-p)(11-p)]. All special cases and sign statements follow.

3. The range is sharp for this actual limiting law, not merely for a formal approximation. F(tq)/F(t) has a positive constant times q^-11 tail for every finite t>0 with F(t)>0. Therefore every p≥11 moment diverges, logarithmically at eleven and as a power above it. This is distinct from the capped eleventh moment and asserts nothing about finite-r field moments.

4. The logarithmic correction can be obtained directly from ∫S_t(q)dq/q. This gives 1/11 and c(1/13-1/11) = -2c/143, with absolute error at most Kt^-4/11. No differentiation in p of a remainder is required.

5. For the finite-order Mellin expansion, applying the source scalar expansion at s=tq gives a uniform remainder O(t^(-2N-2)q^(-13-2N)) after multiplying by t^11. Its weighted tail integral converges for every fixed p<11. The numerator is D(t)+p times that integral, so expanding D(t) at the same order yields (11+2j)/(11+2j-p), exactly the proposed coefficient. Retaining the exact denominator C(1/t) preserves normalization; its positive limit C0 keeps division stable. The stated remainder bound and p=0 convention are consistent. There is no claim that the infinite Taylor series converges.

6. For log powers, the change of variable y=log q reduces each term to an exponential Gamma integral. Multiplication by m gives m!/(11+2j)^m. The remainder integral is bounded by m!K_N/(13+2N)^m at the stated t order. Every fixed integer m≥1 is covered; there is no uniform-in-m claim.

7. The quantile expansion uses more than the CDF error: the exact scalar representation is smooth and even in delta, and its q derivative at delta=0 is -11q0^-12≠0. The implicit function theorem gives the local even expansion. The separately supplied differentiated tail makes F strictly decreasing for all sufficiently large arguments, identifying the local root with the unique conditional upper-tail quantile. Substitution gives coefficient c(alpha^(2/11)-1)/11. The restriction to fixed alpha in (0,1) and fixed source model is essential and present.

8. The signed coefficient bound follows directly from the source C0 and B_sign identities. After normalization by the positive measure with density proportional to H gamma^11 G0, its remaining ratio is E[|A|/sqrt(1+A²)]. It is strictly between zero and one because the source density gives positive mass at nonzero a and A is finite. This proves 0 < B_sign < 11U_abs/(2I) at the stated general fixed-dimension/frame scope. It needs no sign for D_a G0. The stricter lower bound on c uses the aligned planar sign from source §7, as the consequence correctly states: its second contribution is nonnegative and its geometric ratio (1+12A²)/(1+A²) exceeds one on positive mass.

## Verification and limits

I inspected and replayed `moment_consequence_checks.py` once with `python3 -B -S`; all eleven test methods passed. The finite Pareto mixtures independently exercise tail-versus-density normalization, powers of both signs, threshold divergence, log coefficients, finite-order numerator normalization, quantile brackets and the rational coefficient factors. They support arithmetic and the claimed failure of a uniform-in-p remainder; they do not certify the source Gaussian theorem.

No defect was found in these conditional implications. Their premise remains the exact source smooth expansion and retained Gaussian coefficient identities, whose Slice A/B reviews are separate. Constants need not be uniform as p approaches eleven, alpha approaches zero or one, or physical parameters leave fixed compact scopes. The original r limit precedes the t limit. No whole-cluster maximum law, simultaneous t(r) theorem, source acceptance or scientific-register change follows from this review.
