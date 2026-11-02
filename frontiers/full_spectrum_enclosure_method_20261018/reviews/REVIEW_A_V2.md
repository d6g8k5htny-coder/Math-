# Completed exact V2 nonauthor mathematical-method review A

**Decision: ACCEPT_SCOPED_ANALYTIC_METHOD** for exact `technical/source-author/TECHNICAL_METHOD_V2.md`, **32,593B / SHA256 `8bdea4b42e9efd2d846cd1aa73691e8194fa26cd937ac02b79991334f88204f6`**. The positive-integer spectral cutoff and method-radius corrections close the V1 domain findings. I found no remaining material mathematical-method defect within this bounded review. Acceptance is restricted to the in-principle deterministic enclosure method for the explicit algebraic collision expression C_alg(d,L), under its stated computable-input/outward-interval premises. It is not an executed interval, a proof of ordinary-bar asymptotics, a certified coefficient result, software/formal validation, scientific acceptance or runtime admission.

Actual reviewer `/root/native_capture_resume_review_a`, OpenAI/Codex, is a NONAUTHOR of V1/V2 and any enclosure implementation. I supplied the actual V1 M14 objection and analytic counterexample through Root; Root supplied correction direction and relayed actual A/B findings to the author. I therefore have correction/source exposure and do not claim blind or uninfluenced corroboration of the repair. I independently assess its mathematics rather than count Root's direction or another reviewer's conclusion as approval. Organization independence credit0; provider/blind credit0. Root retains review claim WE2296. A previously failed dispatch supplied no review or acceptance credit; this actual completed report supplies this verdict.

## Exact inputs and retained negative history

| Exact object | Bytes | SHA256 |
|---|---:|---|
| Original `independent-derivation.md` |24027|`f38c085ab5b15368e6989a1fd6298490f3b671f5a6c3a01bcdc81b516022bc33`|
| Author `TECHNICAL_METHOD_V1.md` |31426|`d9476da4e8ce2411f43483545901ff2dc59941d4d175c9620030ee33e04c7cf2`|
| Author `TECHNICAL_METHOD_V2.md` |32593|`8bdea4b42e9efd2d846cd1aa73691e8194fa26cd937ac02b79991334f88204f6`|
| `CORRECTION_LOG_V2.md` |5584|`6078229b6156e153a25a311213e652ee32bc1bb8d9de03fea36a320711ecc663`|
| `EXACT_TEXT_EDITS_V2.json` |5915|`8237449f52f82b97a26ec7d842f2ab083ec155fc4021c5c9a6240d1b8bd1b87d`|
| `V1_TO_V2_TEXT_DIFF.patch` |12207|`df54b46cdb862759363df3604e7fb94c4ec2c1e330ac726d561b66abc6778e61`|
| `REVIEW_INPUT_V2.md` |1916|`cdf41f1cf1dcdfee72b1cdde3a675e4bd30cc333526c683d0be79a0c3e19d913`|
| My retained `review/MATH_REVIEW_A_V1.md` |17586|`5006fb2c1b881e8c436665e45fc62ef526f1763da3f98a716d317e231d7eb39a`|

Author objects are under `work/num-i2-technical-unit-20261017-2303/technical/source-author/`; the original remains at `work/theorem-continuation-20261008/blind-oct08-1022/independent-derivation.md`. All rows above were freshly rehashed for this review. I fully read the414-line V2, complete actual unified diff, correction log and exact edit list, and inspected the actual assistance record/source bindings. The629-line original was fully read in my V1 review; it remains byte-identical, and that substantive analytic review is retained rather than given an invented new read timestamp.

V1 and my **AMEND_REQUIRED** verdict remain unchanged. The fractional-M counterexample remains a valid refutation of its literal all-real-M statement. V2 does not retroactively assert that V1 already had the needed guard. I do not automatically transfer V1's partial PASS to V2: the new exact source, full diff and corrected proof steps were checked here.

## Complete edit closure — no hidden mathematical change

Independently applying each of the eleven declared old/new replacements once to exact V1 reconstructs exact V2, byte for byte. Reversing all eleven reconstructs V1. The retained patch is exactly equal to my independently computed unified diff, not merely a similar preview. All33displayed mathematical blocks and all31M-equation tags/formula bodies are unchanged.

The only mathematical semantic restrictions are:

1. V2:175 now chooses a POSITIVE INTEGER spectral cutoff M>=1 with M>=sqrt(k/alpha).
2. V2:193 propagates this to positive integer M>=max{1,sqrt(k/alpha_lo)} for interval-L uniform tails.
3. V2:332 repeats the positive-integer cutoff in certificate Step1.
4. V2:333 chooses a POSITIVE INTEGER Gaussian radius R and states tail convergence along the integers.
5. V2:334 explicitly uses that radius and rational endpoints, hence exact rational box volumes.

The remaining edits disclose version/claim/history, actual Root-relayed review assistance and immutable correction status. In particular V2 no longer incorrectly carries V1's sole-input statement as a claim that this correction had no review input. I did not independently reacquire native claim/closeout records; their lifecycle is attributed to the actual source and Root's task, not converted into mathematical evidence.

## Fresh analytic resolution of the cutoff defect

For the corrected positive integer M and f(x)=x^(2k)exp(-alpha*x^2), the derivative has sign determined by k-alpha*x^2. Hence f is nonincreasing on[M,infinity) once M>=sqrt(k/alpha). For every omitted integer m>=M+1, f(x)>=f(m) on[m-1,m]. Summing these complete unit intervals proves

  sum_(m=M+1)^infinity f(m) <= integral_M^infinity f(x)dx.

The symmetric omitted Fourier modes give the factor2h^(2k), which is exactly M14. M15's integration-by-parts recurrence and Mills base bound are unchanged and valid. The interval-L majorant uses h upper and alpha lower endpoints; V2:193 now supplies the same integer cutoff condition for its monotonic majorant. All four moments k=0,1,2,3 remain subject to their stated threshold; an eventual implementation must satisfy the threshold for every moment it encloses.

The old real-M counterexample k=0,alpha=1,M=9/10 no longer lies in the domain. Restricting the evaluation cutoff to integers changes neither the full original spectral law nor the target moments: finite-sum-plus-certified-tail intervals still converge to the original infinite sums. It does not replace the field by a cutoff model or increase an allowed numerical/resource limit. This closes A-M1 at source-method level without executing an enclosure.

## Fresh analytic resolution of rational Gaussian boxes

M25–M27 remain valid for every real R>0. For the IMPLEMENTED METHOD described by the text, choosing R among positive integers is sufficient: the certified upper bound has a fixed finite positive prefactor times exp(-R^2/4), which tends to zero along that unbounded integer sequence. Thus one can search for an integer with certified tail<=epsilon/3 without weakening the tolerance or changing the Gaussian distribution.

The compact integration rectangle now has angular endpoints+/-1 and Gaussian endpoints+/-R, all rational. Finite dyadic/rational subdivision gives rational endpoints and exact rational volumes. Refining boxes does not change the chosen tail radius or lose the already allocated remainder. Moment/input intervals can also be refined, keeping all true values enclosed. The compact interval-width criterion remains a computable stopping test under faithful convergent outward operations and effectively specified positive tolerance/input data. It establishes no particular runtime or practical feasibility.

## Final core and whole-method analytic check

The unchanged M1–M19 core remains consistent with the exact original:

- Physical gradient/Hessian factors give the original(2pi)^(-d)a^(-d/2) and full sphere AREA measure, with no additional common-height density, L^(-d) or point-pair half.
- The full Hessian Frobenius covariance has diagonal block beta*I+a^2*11^T and orthonormal off-diagonal variance2a^2; its eigenvalue floors/ceiling are exactly M6. The constraint-map norm lies between|v|^2/2 and|v|^2, and Schur complementation plus the free-coordinate sqrt(2) conversion gives M7–M9 without changing the original Gaussian measure.
- The odd-polynomial residuals have norms nu3,a*beta,a^3 and expansion coefficients e_i^3,3e_i^2e_j,6e_ie_je_k. Their orthogonality gives M10; expansion recovers M3. Jensen and the full sixth radial moment give M11. Retaining spectral atoms0,+/-h,+/-2h yields the exact positive M12/M13 witnesses, including the factor72.
- Dominant-coordinate faces cover the sphere up to measure-zero ties. Their Gram determinant is(1+|x|^2)^(-d), giving M17. The reflection sends sigma*e_j to e with a denominator>=2(1+1/sqrt(d)), giving a smooth orthonormal transverse frame without a global-frame assumption.

I rechecked that the correction does not affect the later analytic pathway: determinant-squared vanishing on the cone boundary gives the M20/M21 continuity enclosure; original free-coordinate Cholesky transformation cancels its own Gaussian determinant; its positive pivots and the conservative free-coordinate/Frobenius bound give M23/M24. The chi-square exponential moment gives M25/M26 and its prefactors; M27 uses the correct angular volume, covariance determinant floor and sixth-moment upper bound. The Gamma endpoint estimates and guarded compact convergence argument remain valid under the stated outward-interval assumptions. The detailed algebra supporting those checks is retained in my unchanged17,586B V1 review and was checked for continued applicability to the exact unchanged V2 formulas/proof paragraphs.

M30 remains a LIMITED conditional estimate: whitening the pin vector and bounding the regression projection yields the stated Hilbert second-moment inequality only with its actual covariance-floor premise. V2:363–365 still requires the same-field uniform small-r floor/cross-covariance convergence and does not use this estimate as an automatic marked-event/genericity theorem.

## Strict scope after acceptance

The positive result is a source-bound ANALYTIC METHOD for C_alg under computable fixed d>=2,L>0 and faithful certified interval operations. No interval backend/code was implemented, tested or executed by this review; no coefficient value/digits, empirical field, diagnostic result or accepted final enclosure exists here. Mathematical review agreement is not a formal proof/kernel check or a software certificate.

Most importantly, this acceptance does not identify C_alg with the proven coefficient of the ordinary finite-bar observable. G1–G4 remain unaccepted: elder/Morse once-counting; uniform good-fold isolation and older-branch support; same-field density-scale exhaustion across small/degenerate jet sectors; and marked Kac–Rice/disintegration/measurability/approximation. The original uniform-tube, conditionalC4 and marked-measure qualifications remain. A justified density representative/integrated count statement and finite-ell error functions in M31 still need their actual mathematical work. Numerical integration error is not that asymptotic error.

All five missing-input gates,113retained failures, historical source cuts, TA/TRIG stops and broader scientific acceptance remain unchanged. No new blind/provider credit, universal policy waiver, model/native admission or resource authorization is created. I performed only inert source reading/text reconstruction/hashes and symbolic analytic review, and wrote this private immutable report. No math/numerical/model/native/project execution, source edit, new claim or external write occurred.
