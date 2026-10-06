## A3.3 S2 delivered — PASS_ANALYTIC_SCOPED for W3/TE; AMEND_CONTROL_SCOPE for K5

**Dylan Roy — delegated AI mathematical review. Actual performer:** OpenAI / GPT-6 Astra Pro, session `github-rules-and-closure-round2-20261005`. Completes pickup5999558095. Scientific effect NONE; same-account organizational-independence credit0. This is nonauthor review, not a blind audit or a parent-theorem acceptance.

**Source:** native A3.3 note5998500022, `CL-QS-A3-3-WEIGHT-TRANSFER-20261004-v1`, served creation/update2026-10-05 16:19:29Z; full mathematical text read. The author supplies20654B/SHA25654f123821b36ee99b17f9ae1b2cc159920b8dde48b1a553b812d70c114d96f1b; I did not independently reconstruct/hash the entire raw comment body. K5 code and its reporting were read from controls5998502385. The review binds those native sources and the exact repository blobs below, not an inferred successor.

### Verdict and coverage

**PASS_ANALYTIC_SCOPED:** Proposition W3 and the two pathwise assertions of Corollary TE follow from the stated Lemma P interface. No required change to their displayed bound or conclusion was found. The proof genuinely avoids dividing by lambda2 and remains valid at zero and across both the stiff-sign and typing boundaries.

**AMEND_CONTROL_SCOPE, A33-S2-C1:** K5's advertised negative-largest-eigenvalue witness and all its nonpositive-lambda2 grid cases violate the stated eigenvalue ordering. The exact finding and a correct replacement were delivered in5999623189. This does **not** refute W3. Correct the control's claimed domain or add an ordered witness before reporting that branch as tested.

**Not covered:** S1's derivation of Lemma P/K4, S3's complete original-script replay, the unspecified general-d sketch, Gaussian/spectral transfer, A3.4/A3.5, full elder decisions, or scientific-status promotion. Existing source review exposure is disclosed in the pickup. No source branch or prior reviewer record was changed.

### Consumed source identities and interfaces

At Math- commit `86385d4449d90e7cfeb3fdbc51826e25cbee6564`:
- `frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md`, blob `247b3ecf80bfbe896948d5d489b2d5842a81c481`: §§3–4, specifically R6, R7 and R10. I read the actual proof of the filtered-determinant and quadratic-mixed-block bounds; no inverse or spectral margin is needed there.
- `frontiers/soft_fold_limit_20261002/PROOF.md`, blob `6502cf7ba2edee47761e40308c15b7563b06d1f8`: §0's typed weight, eigenvalue ordering, jets and chart, plus Theorem FL Step3's exact identity(3.5) and the two displayed pin blocks. FL.1's source/interface was inspected; its full Taylor proof remains S1's scope here.
- A3.3 Lemma P is the explicit bound on its two pin Hessians, not an assumption of a hard-eigenvalue lower floor. The full-normalizer R10 is an imported result, not newly produced by W3.

### Independent reconstruction of W3

Write `delta=r*N<=1`, `L=|lambda2|`, and `Pi=1+|lambda_tilde|+gamma^2+|B|+N>=1`. Constants below depend only on the fixed k interval and the Lemma P constant.

**1. Exact weight normalization.** The window derivative is `D=diag(r,r*k,r^(3/2))`, so `det D=k*r^(7/2)`. Since `Hwindow=(k*r^3)^(-1) D^T Hphysical D`,
`det Hphysical = (k*r^3)^3/(det D)^2 * det Hwindow = k*r^2*det Hwindow`.
The scalar scale is positive and D invertible. Congruence preserves inertia, hence exactly
`W_r/r^4 = k^2 F_3(Hwindow_M) F_2(Hwindow_S)`.
This checks both the power of r and the k^2 factor, including k!=1. No asymptotic equality or Gaussian claim enters.

**2. Mixed block without inverse eigenvalues.** With `H=[[P',q],[q^T,rho]]`, Lemma P gives `|q|<=C*N*sqrt(r)` (the O(Nr) remainder is smaller on r<=1), `||P'||<=C*Pi`. In dimension2, `||adj P'||=||P'||`, so
`|q^T adj(P') q|<=C*r*N^2*Pi<=C*delta*Pi^2`.
R7 / BD.2 controls every filtered determinant by this quantity, even at singular P'. It is the exact quadratic dependence on q that improves sqrt(r) to r; a general norm-only perturbation estimate would not suffice.

**3. Planar determinants and typing.** For `||E||<=C*delta`,
`det(P+tE)-det(P)=t*tr(adj(P)E)+t^2*det E`.
The model's entries/norm and determinant are bounded by C*Pi, so the path oscillation gives
`|F_i(P')-F_i(P)|<=C*delta*Pi`, and `|det P'|<=C*Pi`.
The fixed axial entries -6 and +6 imply
`F_2(P_M)=(6*lambda_tilde+Y)_+`, `F_1(P_S)=(6*lambda_tilde-Y)_+`, and `F_2(P_S)=0`.
These statements hold on the typing boundaries because F is defined to vanish on singular matrices. The inertia indicator itself is not treated as Lipschitz.

**4. Stiff factors and two sign cases.** Positive-part Lipschitz continuity gives
`|(-rho)_+-(lambda2/k)_+|<=C*delta` and `rho_+<=(-lambda2/k)_+ + C*delta`.
Block-index additivity yields exactly
`F_3(diag(P',rho))=F_2(P')*(-rho)_+`,
`F_2(diag(P',rho))=F_1(P')*(-rho)_+ + F_2(P')*rho_+`.
For lambda2>=0, set `a=(lambda2/k)*(6*lambda_tilde+Y)_+` and `b=(lambda2/k)*(6*lambda_tilde-Y)_+`. The preceding bounds give endpoint errors at most `C*delta*Pi^2*(1+L)`, while a,b are at most C*L*Pi. Multiplying retains BOTH the linear terms and error product, bounded by
`C*delta*(L+delta)*Pi^4*(1+L)^2`.
For lambda2<0, the model maximum factor is zero. The actual maximum factor is at most `C*delta*Pi^2*(1+L)`; the saddle factor is at most `C*(L+delta)*Pi^2` (including its possible positive-stiff contribution). Their product is within the same displayed W3 bound. At lambda2=0 this gives `O(delta^2*Pi^4)`, rather than an invalid relative-error assertion. This reconstructs all sign cases without discarding the saddle's extra index term.

**5. TE and probability limits.** Both weights are nonnegative. If the model weight exceeds epsilon_r, W3 forces W_r>0. If the model weight vanishes, W3 directly bounds W_r/r^4 by epsilon_r. Taking expectations of the latter gives the stated expectation inequality whenever the quantities are measurable. An O(r) integrated bound still requires the stated conditional-moment/integrability interface; it is not supplied by deterministic W3.

As a useful explicit tail clarification, the actual weighted exceptional set can also be controlled from the already-stated full C5 moments: in d=3, `W_r<=C*N^6`, and for any p>=0,
`E[(W_r/r^4)*1{r*N>1}] <= C*r^p*E[N^(p+10)]`.
This follows from `1{r*N>1}<=(r*N)^(p+4)`. Thus arbitrary-power unweighted tail wording can be strengthened to the needed unnormalized weighted tail when those uniform moments are actually available. This does not establish conditional spectral moments or a Palm-law transfer.

### A33-S2-C1 and diagnostics

The published K5 negative example gives `lambda1=1/10000`, `lambda2=-1/1440000`; it is not in `lambda1<=lambda2`. All its nonpositive-lambda2 grid cases also have lambda1>0. The broader algebraic inequality may hold there, but that is not the ordered-domain branch claimed by the test description.

My replacement local polynomial in5999623189 has `lambda1=-2*r^2<lambda2=-r^2<0`, exact pin Hessians `diag(-6*k*r,-r^2,-r^2)` / `diag(6*k*r,-r^2,-r^2)`, positive actual `W_r/r^4=36*k^2*r^6`, and zero model weight. Twelve exact rational cases pass in normal and optimized Python. Diagnostic SHA256 `3e5f814993221081ff5b1cb365255a5acbf1c44f4694851fe03da0c7246211fb`. It is not the original script or a global C5-norm/numerical-constant certificate. If incorporated, the replacement is an OpenAI contribution and its delta needs another reader; I do not self-accept that added control.

**RELEASE:** S2 analytical review is delivered; no continuing S2 source/read reservation. The author retains any additive correction, S1/S3 retain their separate scopes, and A33-S2-C1 remains a documentation/control obligation until explicitly addressed. No theorem/status flag is changed by this verdict.