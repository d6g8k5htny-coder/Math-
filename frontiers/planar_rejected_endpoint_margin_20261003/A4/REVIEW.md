# C117 — full nonauthor review of QS addendum A4

**Verdict: ACCEPT / PASS_TECHNICAL_SCOPED, conditional on the retained source interfaces. No required amendment found.** This verdict applies to the exact A4 body below, its local endpoint inequality and certificate, both endpoint-strip estimates, the fixed-layer sector bounds, and the growing-layer raw-jet failure-measure rate for each fixed 0<beta<2/3. It is additive review evidence; it does not rewrite or supersede C97/C101, promote scientific status, or discharge their parent hypotheses.

**Exact target.** [main#229 comment5972396791](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972396791), created and last updated 2026-10-03T18:53:16Z; object CL-QS-A4-LOCAL-ENDPOINT-PLANAR-RATES-20261003-v1; **16544 UTF-8 bytes**, SHA256 **acd172c5f8626aa3b7be5ac691786eefa6d6f243a32909502dfdbd79c8066a7c**. Fresh native readback matched the entry copy exactly. Line references below address that frozen A4 body or the byte-identical PR249 source copies.

**Actual reviewer and exposure.** Dylan Roy — delegated AI review. The substantive reconstruction and executions were performed by OpenAI/Codex subagent /root/next_math_triage under root coordination, claim f39fde6a-1320-44ac-8af1-dfd0026901ff / Work Events711 and [native pickup5972431044](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972431044). I did not author A4. I previously coauthored C113, authored C115's historical-source checker repair, and read C50/C51 and PR249 material for integration/triage. Root has C91–C103 source/author exposure and is the coordinator, not a second review vote.

The earlier bounded ownership query incidentally printed the complete A4 author-control comment before this review assignment and before my design freeze. Consequently these are independently reconstructed **nonauthor controls with disclosed author-checker exposure, not blind controls**. That correction is [5972529830](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5972529830). No author code was executed before the reviewer design and implementation freezes. A4 is Anthropic-authored and this reviewer is OpenAI, but the shared-account delegated setting has organizational independence **0**. Human review **NONE**; Dylan's personal reading **PENDING**; scientific/register effect **NONE**.

## 1. Exact scope and source audit

The law is the original variance-one periodized Gaussian field on a fixed admissible planar torus, at **physical k=1**, compact birth parameters and all orthonormal frames. The exact maximum/saddle pins, correlated endpoint determinant W_r, full normalizer Z_r=r²z_r, and actual designated finite ordinary-superlevel H0 death event H_r remain those of C97/C101. Constants may depend on the fixed field/parameter family and chosen epsilon/beta/moment orders; they are not numerical error bars.

I read the consumed statements and the arguments that make their parameters available. This is verification of A4's use of these interfaces, **not a fresh proof or source-wide acceptance of every parent theorem**. In particular the corrected trap is C95's ordered object (historical A2 v1 plus the explicit repairs), not an acceptance of literal unrepaired A2. P/E1/E2/REC, C82, QS local premises, CUB, ELDER and the exact Gaussian/Kac–Rice/normalizer hypotheses retained by C101 remain conditional inputs.

All nine directly consumed native proof bodies were matched by byte length and SHA256 to SOURCES.json at PR249 head **a345492a3a3e605400ccea004b05e9baafce2060**, path prefix frontiers/planar_soft_layer_chain_20261003/. C98 is included because A4 section3 explicitly uses its coverage, although the opening table lists it only through C101. No source bytes were edited.

| Source/native comment | Bytes | SHA256 | Portion used here |
|---|---:|---|---|
| C91 / 5963566666 | 12433 | 74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa | W0–W5, exact mixed second-derivative bound |
| C92 / 5963825788 | 19567 | 6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a | Original weighted moments, full normalizer and raw cubic |
| C93 / 5964167051 | 15545 | f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c | E2 actual moment-weighted edge integral |
| C94 / 5964517708 | 15407 | 0fe4fa2028f8ddbbf5a79df3879bcbd3789f19409fb44ad739caeabedff1af3c | C14/C16 for every fixed p>=1; sector and mass floor |
| C95 / 5964938563 | 16185 | c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1 | G9–G12 corrected trap, G14 periodic path transport |
| C96 / 5965141133 | 7913 | 0758b5de8f4d9e4658ca3c6cf3e52c23d8e12f77999e9c3668ef0bedb15a05f5 | D2 actual designated maximin/finite-H0 identity |
| C97 / 5965421543 | 16098 | acf83958e6ea650d83bf811b2beacc03b553637dc4a3160012567c7f0a300a57 | R6–R10 chord, R15 radius tail, R18 band, R23 mass floor |
| C98 / 5965738339 | 15050 | 3ca1622197bf22cf71ab64f2938ecc0b022ed09487b691d50ae8d2ad1f46d198 | B4 sector coverage and null exceptional sets |
| C101 / 5967063473 | 36333 | 300d0d18abb74332e593e389485c817a3c0ea7c31345194e3cfdd4039ac3b5c4 | Q5–Q38 cutoff-uniform actual law, event comparison and failure tails |

The exact C98 row is independently bound in SOURCE_IDENTITIES.json; the review's source table is validated against that inventory before freeze. C96's consumed **7657-byte proof suffix** also matches SHA256 **7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a**. The full native C96 body is retained separately, so its different full-body hash is not a discrepancy.

## 2. Lemma LE: reconstruction rather than a sampled positivity claim

Write a=u(Y)+1/2, z=Z(Y), g=gamma²>0 and A=a_M>0. C97 R7 gives
h=a²+A z²/(144g), while the raw displacement is v=(a-z/12,z/gamma). Thus the coefficient matrix of 4h-2ell|v|² is exactly

    q11=4-2ell,
    q12=ell/6,
    q22=A/(36g)-ell/72-2ell/g,

with ell=min(1,A/(g+72)). The off-diagonal contribution is 2q12 az=ell az/3; losing that factor would change the claim.

For A=ell(g+72), 0<ell<=1, direct cancellation gives q22=ell/72 and det Q=ell(1-ell)/18. For A>g+72, ell=1 and det Q=(A-g-72)/(18g)>0. In both regimes q11>=2. Therefore Q is positive semidefinite for all permitted parameters and positive definite except on A=g+72. Since the selected extra saddle differs from M, v is nonzero. Equality can occur only at that boundary. At equality the null direction is a=-z/12, exactly the one used by A4's example. No positive lower bound on |gamma| was introduced; gamma=0 remains the inherited null chart exclusion.

The Taylor part retains its exact prerequisites. Both the raw cubic and the actual pinned field have value0 and gradient0 at raw M, hence E(M)=gradient E(M)=0. The entire segment to each chord point lies inside the convex chord, whose raw radius is controlled by Rch. C91's entrywise Hessian bound is K2 N r w², with K2=115/48. For a symmetric2×2 matrix, the operator norm is at most twice its largest entry. The integral Taylor weight has integral1/2, so these two constants cancel and give

    |E(xi)| <= K2 N r w² |xi-M|² <= 4K2 N r w² |v|².

The gradient scaling is r^-2 at k=1, so the exact physical gradient pins really do give the raw gradient zeros. For the endpoint, P(2Y-M)=4h, and the two strict conditions eta_LE N<1 and eta_LE N(gamma²+72)<a_M imply eta_LE N<ell. This gives strictly positive actual endpoint height. Along the chord, E0<mu/2 gives F_r>mu/2-1>-1. The compact chord therefore has positive clearance above the saddle height, and reaches a point strictly above the birth height. This is sufficient for D_f(M_r)>f(S_r), including the global torus path interpretation; it assumes no gradient-flow adjacency.

Measurability follows from C97's finite algebraic saddle branches and lexicographic selection, continuous field-norm/supremum maps on each fixed window, and Borel inequalities. It does not require choosing a continuous saddle through tangencies.

## 3. Sharpness and the h<=1/9 observation

I solved the full stationary system in the proposed example. At gamma=1, psi=86, c=13, R=3400, nonzero-Z critical points satisfy Z=48(psi+2cu)/R. Substitution in P_u=0 is a quadratic. Its two exact solutions are:

- u=-7/12, Z=1; P=-37/72, Hessian determinant -131/6 and trace -583/144. This is a nondegenerate window saddle.
- u=39539/59476, Z=21681/14869; P=-4306029173/1768697288, Hessian determinant 946737/29738 and trace2921697/237904. This is a minimum below the window.

Together with the two Z=0 pins these exhaust the stationary system. Hence the displayed saddle is the sole extra saddle and is selected. Its a_M=73, raw displacement(-1/6,1) and squared norm37/36 give 4h=37/18=2|v|², so the LE matrix constant is attained within the selected-saddle class.

The Taylor sharpness bullet is correctly read as sharpness of the **local integral-Taylor/entrywise-Hessian step** using the M value/gradient pins. The polynomial multiple of (X+1/2+zeta)² does not satisfy the other pin conditions at S and need not be realizable as the full midpoint-defined error E_r. Therefore that bullet does not establish optimality of K2, the complete exact-pin field bound, or the stochastic rate. A4 calls it the Taylor step; no stronger conclusion is needed.

For h>1/9, 4h>(1-h)/2=mu/2, so the uniform condition E0<mu/2 already forces endpoint positivity. At h=1/9 the strict E0 bound still suffices. Thus A4's statement that the new conditions only matter on the possibly larger set h<=1/9 is valid, though inclusion of the equality boundary is unnecessary. It does not remove the separate saddle-clearance requirement.

## 4. Endpoint strips B and B-prime

Put eta=eta_LE>0 and X=N(gamma²+72). If eta X>=a_M and a_M>sqrt(eta), then eta X>sqrt(eta). Thus the failure event is covered by the near strip, this Markov event, and eta N>=1. The strict/non-strict endpoints are consistent.

C93 E2 gives the fixed-layer strip bound by integrating (s+r) from0 to sqrt(eta): C(eta+r sqrt(eta)). Since gamma²+72<=73 Pjet², the second moment of X is bounded by the actual weighted N²Pjet⁴ moment. Squared Markov gives Ceta at the threshold eta^-1/2. The third event costs Ceta², absorbed by Ceta for eta<=1. This proves Lemma B without a reciprocal random margin, a variable-width saddle-level estimate, or independence between the jets and N.

On a growing layer, C101 Q14 gives C(H²eta+rH⁴sqrt(eta)), and Q12 gives mu_r(N²Pjet⁴)<=CH³ under rH<=1. The same two Markov terms are CH³eta and CH³eta². Because H>=1, the strip's H²eta is absorbed by H³eta. This is exactly B-prime. The finite-r rH⁴sqrt(eta) correction remains present.

The moment order in the saddle-clearance estimate is freely selectable but fixed: Q7 covers all fixed p>=0, including p<1 by Jensen, and Q12 carries these weighted moments. Therefore Q23 generalizes to C_p[d+rH⁴+H³(e/d)^p]. Constants may depend on p. For clarity one may choose an integer p>=1 exceeding A4's threshold; no moment order varies with r.

## 5. Fixed-layer results R-prime and E-prime

With w=r^-1/12 and d=r^(2/3-epsilon), e=rw⁴=r^(2/3). The rejected-sector bracket is exactly the union of the inherited radius failure, the inherited saddle-clearance failure and Lemma B:

    w^-8 + rw^-4 + d + r + (e/d)^p + rw² + r^(3/2)w.

Its exponents are 2/3,4/3,2/3-epsilon,1,p epsilon,5/6,17/12. For p>=2/(3epsilon), every exponent is at least2/3-epsilon. Multiplication by the single inherited r³/z_r factor gives r^(11/3-epsilon).

For the elder sector, C94 C14/C16 were stated for every fixed p>=1 and every admissible deterministic w; its earlier choice w=r^-1/16 was only a later specialization. The new exponents are 2/3,4/3,2/3,4/3,2/3-epsilon,1,p epsilon,5/3, so the same rate follows. C95 G9–G12 and G14 are deterministic statements on the controlled patch. Their implication uses no feature specific to the old w exponent: Good supplies the exact pins, value margin, both rescaled Hessian margins and the complete trap/axis within the embedded patch. C96 D2 then identifies this maximin event with the actual designated finite H0 event.

All window conditions hold for sufficiently small r with fixed epsilon and parameters: rw=r^(11/12), e=r^(2/3), eta_LE proportional to r^(5/6), and d→0. The positive sector mass floors and expansions Q(Rsec)=r³m_R/z0+O(r⁴) and Q(E)=r³m_E/z0+O(r⁴) justify the conditional probabilities. The O(r⁴) mass error is smaller than the asserted r^(11/3-epsilon) error. For epsilon>=2/3 the stated combined-sector bound follows directly from the O(r³) total sector mass, as A4 says.

## 6. Growing-layer rate and strict endpoint

C101's common conditions are retained with its old C_H H³e condition removed because the old endpoint estimate is replaced; eta_LE<=1 is inserted. The elder value margin H⁴e+rH⁵sqrt(e), Hessian losses, finite-r off-T leakage, density comparison and all actual/model failure tails remain required.

Starting from these explicit source estimates gives exactly A4's eleven local terms. With alpha=(2-3beta)/16>0, w=r^-beta/8, Lambda=r^-alpha and d=r^beta, the following are the exponent-minus-beta values for the terms not involving p or m:

| Term | Exponent minus beta |
|---|---|
| w^-8 | 0 |
| rH³w^-4 | 5/8+beta/16 |
| H⁴e | 1/2-3beta/4 |
| rH⁵sqrt(e) | 7/8-5beta/16 |
| H³rw² | 5/8-11beta/16 |
| rH⁴sqrt(rw²) | 1-3beta/8 |
| d | 0 |
| rH⁴ | 1/2-beta/4 |
| H⁵r²w⁴ | 11/8-9beta/16 |
| H⁷r²w² | 9/8+beta/16 |
| Scaled far/derivative exceptions | 1-beta |

These affine expressions are nonnegative throughout 0<=beta<=2/3; the admissible open interval is needed for alpha>0 and the Markov balance. The remaining bounds are precisely
p(1-3beta/2)-3alpha>=beta and m alpha>=beta, achieved by the stated fixed choices. All smallness exponents in A4 line199 are positive on the open interval. Fixed prefactors are handled by decreasing r_beta, not by claiming them numerically evaluated.

At beta=3/5, alpha=1/80, the minimum real p is51/8, the minimum integer p is7 and the minimum integer m is48. The resulting physical failure error exponent is3+3/5=18/5.

The endpoint2/3 is genuinely excluded by this argument. Radius-tail control forces omega>=beta/8; the band split requires a positive power in e/d and then p(1-4omega-beta)>=beta+3alpha. At beta=2/3 the left base exponent is at most0, while the required right side is positive. No finite fixed p repairs this. The statement is an attainable family beta<2/3, not optimality of the underlying probability law or an assertion at beta=2/3.

## 7. Normalization, tails and observable boundary

I checked C101's unchanged completion: Q29 is the comparison on D_Lambda; Q32 supplies the **actual failure-marked** tail C_m Lambda^-m+Cr, using endpoint scalar integration under the same W_r; Q34 supplies the model failure tail C_m Lambda^-m. Neither is an unmarked soft-layer tail. Adding these nonnegative omitted masses to the compact comparison gives the variation-norm bound on the full raw-jet failure measure. The norm is sup over |phi|<=1, with no factor1/2.

Using phi=1 then gives r^-3(1-p_r)=alpha1+alpha2+O_beta(r^beta). The coefficient counts failure events once; it is not alpha1+2alpha2. There is exactly one full normalizer, and no extra pin-density or area factor enters the conditional law. C98 coverage and null polynomial account for the two sector boundaries; finite-r typing leakage is retained as rH⁴.

This proves the scoped A4 improvement conditional on those unchanged interfaces. It does not give k-uniform C103 transfer, kappa→0 matching, Conjecture7, once-counted replacement-bar intensity/occurrence, total variation of death/location marks, a quantitative all-bars lifetime law, a growing torus or dimension>=3. C51's newly landed occurrence result is not an input to A4.

## 8. Executed controls and evidence limits

The reviewer design was frozen at **19:01:08.163295Z** (CONTROL_DESIGN.md:4314B, SHA2567f342b6af74b6694d4dc3e1016be7b35ca6b0aba6d6f44023b5e176b34b215e5). The final reviewer program was frozen at **19:07:37.764697Z** (independent_controls.py:9063B, SHA2563ad506bf7c7eb9a9401bc62f249ff47829fbe2d377e032cba5b84bbe32fe3c94). An earlier exploratory reviewer execution also passed; it is not counted as a separate review or included in the final mode comparison.

Final recorded execution completed **19:08:54.105822Z**, CPython **3.11.16**:

- Reviewer normal and optimized modes each passed **477 finite exact checks**, including **10 negative-control rejections**; stdout is byte-identical, stderr empty.
- Controls include symbolic LE coefficient/determinant identities, exact sharpness roots/classification, polynomial Taylor integration, strip boundary configurations, and exact affine ledger inequalities. The negative cases falsify denominator36, a missing mixed quadratic term, a reversed raw shear, a halved Taylor norm factor, a nonzero pinned gradient, an insufficient Markov power, omitted H³ cost, fixed p=2 at beta=3/5, an undersized radius exponent, and the beta=2/3 extension.
- Separately attributed author reproduction: exact extracted a4_exact.py **17262B**, SHA256f880ffb044a3102781c71cb3b4ac65d65260c31588c6835520349e5c7bdc2b95. Both modes reproduce the published502B stdout, SHA256022ff38c96e6378dd4dc9c00e14deebf167443d71fd6d2b0cee6f483d95cc28e, with61603 finite author checks. Each of its six named mutants exits1 in both modes, and BOGUS exits2 in both modes.
- The recorder contains **18 actual invocations**: two reviewer runs, two positive author runs, twelve author mutant runs and two author invalid-label runs. Every expected exit matched, all stderr files are empty, and all protected source/program identities were unchanged before and after.

The finite controls do not prove the continuum Gaussian estimates, uniform constants, source tail exhaustion, Borel/path arguments or inherited topology. Those were assessed above as mathematical reasoning with explicit imported interfaces. No master suite, Lean build, branch/source mutation, external review post or additional scientific acceptance was performed by this reviewer.

**Disposition:** no required amendment. The optional clarifications in section3 concern the limits of the stated sharpness examples, not a gap in the theorem. Publish this as one full nonauthor A4 review with the disclosed exposure and the existing scientific gates unchanged.
