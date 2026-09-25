# A bounded-domain saddle kernel, an explicit axis tail, and conditional annulus synthesis

**Object:** D5-CONTACT-KERNEL-TAIL-20260925-v1.  
**Author:** OpenAI / ChatGPT, OA-KERNEL-TAIL-20260925.  
**Disposition:** author-side analytic advance; independent review required.  
**Scientific effect:** NONE. No scientific graph or predecessor source is modified.

## 1. The missing interface and the exact dependency boundary

PR25 Sections B–C gives a fixed-transverse contact kernel, while PR28 proposes a finite-r bound on a complete fixed scaled annulus. The newly delivered PR31 review expressly excludes kernel tails and annulus synthesis. This note fills that interface without writing another annulus-count proof.

There are two logically separate results here:

* **Kernel result:** starting from the explicit Gaussian integral (K1), derive a bounded w-domain, an exponentially small axis envelope, and an explicit tail integral. It is a statement about that integral; it does not require PR28.
* **Conditional composition:** IF the fixed-transverse uniform asymptotic from PR25 and the sharpened finite-r strip bounds from PR28 both hold at their exact common model/pins/tilt/marks, then the windowed asymptotic extends uniformly across the entire fixed annulus. This implication neither proves nor accepts those imported premises.

Keep the exact two-dimensional, variance-one L-periodized Gaussian model with fixed L, all frames, compact birth and strictly positive compact gap marks 0<k_-<=k<=k_+, as in those sources. The two pinned points have physical separation r and heights b,b-kr^3. The endpoint-typed determinant tilt is Q_r^W=W_r Q_r/Z_r, with the ORIGINAL endpoint-only denominator. Fix 1<A<B<infinity and

    K_AB = {(u,v): A<=sqrt(u^2+v^2)<=B}.

Only witnesses whose heights lie BETWEEN the pin heights enter the contact kernel in this note. PR28's all-height upper bound can majorize them; its all-height count is not being relabeled as a windowed leading coefficient. This note gives no all-height leading kernel.

## 2. Starting integral and a bounded change of variable

For v!=0 and 0<theta<1 let D=u^2-1/4, Lc=2u^3-3u/2-1/2. Let g(a,q,c,d) be the actual four-dimensional conditional Gaussian density of the midpoint jets (f_zz,f_xxz,f_xzz,f_zzz) given the six contact jets. Let z0>0 be the endpoint-only normalization limit. PR25 C5 writes

    Lambda_j = 24k/(z0 |v|^6) int_0^1 int_R
                   g(0,q,c(q),d(q)) T_j(q;u,v,k,theta) dq dtheta.    (K1)

Here c=-12kD/v^2-2qu/v and d=12k(Lc+theta)/v^3+3qD/v^2. The density's a-coordinate is ZERO. The scaled curvature entering the three Hessians is a different quantity, Acurv=lim f_zz(0)/r. Substituting Acurv into g would change the conditioning and is not allowed.

Put w=(qv+12ku)/(6k). Solving gives

    q=6k(w-2u)/v,
    c=12k(u^2+1/4-u w)/v^2,
    d=12k(Lc+theta)/v^3+3qD/v^2,
    Acurv=3k(w+1-2theta)/v^2.                                (K2)

The three Hessian determinants equal (9k^2/v^2) times

    m=4theta-(w+1)^2,
    s=4(1-theta)-(w-1)^2,
    x=-[(w+1-2theta)^2+4theta(1-theta)].                       (K3)

For k>0, the maximum at the left pin and saddle at the right are equivalent to

    w in I_theta=(-1-2sqrt(theta), 1-2sqrt(1-theta)).          (K4)

Indeed m>0 gives -1-2sqrt(theta)<w<-1+2sqrt(theta); s<0 selects w<1-2sqrt(1-theta), since the upper branch cannot meet the first interval. The latter upper endpoint is the smaller one because sqrt(theta)+sqrt(1-theta)>=1. Thus I_theta has positive length for 0<theta<1, length at most4, and lies inside (-3,1). Endpoint values theta=0,1 affect neither integral.

Since x<0 for theta in (0,1), only the saddle kernel survives. Define P(theta,w)=m(-s)(-x) on I_theta. It is strictly positive there. The **absolute** Jacobian is dq=(6k/|v|)dw, including when v<0. Then

    Lambda_1 = 104976 k^8/(z0 |v|^13)
       int_0^1 int_(I_theta) g(0,q(w),c(w),d(w))
                                      P(theta,w) dw dtheta, (K5)
    Lambda_0=Lambda_2=0.

The integer104976 is 24*6*9^3. The power |v|^-13 consists of six powers from the original contact Jacobian, six from THREE Hessian determinants, and one from dq/dw. No numerical periodic covariance is replaced by the unperiodized diagonal diagnostic.

On the type domain, 0<m<=4, 0<-s<=16 and 0<-x<=17, so

    0<P<=1088.                                               (K6)

These generous bounds suffice; no optimal prefactor is claimed.

## 3. Gaussian coercivity from the original contact equation

Uniform positive lower and finite upper eigenvalue bounds for the conditional covariance of (a,q,c,d), and a bounded conditional mean on the declared compact marks/frames, imply constants G0,a0>0 such that

    g(0,q,c,d)<=G0 exp[-a0(q^2+c^2+d^2)].                    (K7)

For example, if lambda I<=Sigma<=Lambda I and |mu|<=Mmu, one may take G0=(2pi)^-2 lambda^-2 exp(Mmu^2/(2Lambda)), a0=1/(4Lambda). This uses |y-mu|^2>=|y|^2/2-|mu|^2. These are input-bound expressions, not supplied numerical enclosures.

Crucially, the exact longitudinal contact equation yields

    6kD+u v q+(v^2/2)c=0,
    q^2+c^2 >= 36k^2D^2/[v^2(u^2+v^2/4)].                  (K8)

The second line is Cauchy–Schwarz applied to BOTH q and c. Bounding q alone is invalid: it can vanish when w=2u, while c remains nonzero. No independence among q,c,d is needed.

Choose a longitudinal threshold A1=(A+1)/2>1 and epsilon0>0 satisfying epsilon0<=1 and A^2-epsilon0^2>=A1^2. On K_AB with |v|<=epsilon0 we have |u|>=A1. Let

    d_* = 36 k_-^2 (A1^2-1/4)^2/(B^2+epsilon0^2/4),
    c_* = a0 d_* > 0,
    C_* = 104976*4352*G0*k_+^8/z_*,                        (K9)

where z0>=z_*>0 uniformly on the compact marks/frames. Combining (K5)–(K8), the length bound4 for I_theta and the theta interval length1 proves

    0<=Lambda_1(u,v)<=C_* |v|^-13 exp(-c_*/v^2).             (K10)

The constants are deliberately conservative and qualitative unless all the input constants are enclosed. The factor k^8 in (K5) is NOT a small-k asymptotic: g and z0 also depend on k, and c_* vanishes with k_-.

## 4. Continuous axis extension and an explicit truncation error

Set Lambda_j(u,0)=0 on the annular axis. Bound (K10) tends to zero uniformly in u, marks and frames. Away from the axis, continuity follows by writing the integral over the fixed rectangle (theta,w) in [0,1]x[-3,1], with the type indicator, and using domination. The type-boundary curves have two-dimensional measure zero; the Gaussian density and coefficients are continuous. Thus Lambda_1 extends continuously to the entire compact annulus, uniformly over the compact parameter family.

Moreover for every nonnegative integer N there is C_N with

    Lambda_1(u,v)<=C_N |v|^N                               (K11)

near the axis. To see this, choose integer m with 2m-13>=N and use exp(-c/s^2)<=m! c^-m s^(2m), for s>0. This is superpolynomial decay of the function, not a claim about all of its derivatives.

The coefficient lost by deleting the strip |v|<epsilon can be bounded explicitly. For 0<epsilon<=epsilon0, put X=c_*/epsilon^2. Direct substitution t=c_*/v^2 gives

    int_0^epsilon v^-13 exp(-c_*/v^2) dv
      = [1/(2 c_*^6)] Gamma(6,X),
    Gamma(6,X)=120 exp(-X) sum_(j=0)^5 X^j/j!.              (K12)

For every measurable E subset K_AB,

    int_(E intersect {|v|<epsilon}) Lambda_1 du dv
      <= [2 B C_*/c_*^6] Gamma(6,c_*/epsilon^2).            (K13)

The factor2B is the containing longitudinal interval's length; both signs of v contribute a further factor2 already included in (K13). This gives a transparent truncation-error formula for later coefficient quadrature. It does not enclose the integral away from the axis, and the constants C_*,c_* are not numerically certified here.

For any fixed positive-area E, its axis has area zero and the saddle integrand is positive off axis. Therefore 0<int_E Lambda_1<infinity. No lower bound uniform over all arbitrarily small sets E is claimed.

## 5. Conditional uniform gluing: do not substitute a moving cutoff

Define the normalized physical-area WINDOWED intensity

    F_(j,r)(u,v)=rho_(j,r)^window(ru,rv)/r.

The physical-to-scaled area factor is r^2; consequently E_QW N_j(rE;window)=r^3 int_E F_(j,r).

Assume the following TWO interfaces, with identical field, six pins, tilt, mark convention and parameter range:

**G1 (fixed-transverse uniform limit).** For every fixed eta>0,

    R_r(eta)=sup_(K_AB, |v|>=eta, parameters, j)
                          |F_(j,r)-Lambda_j| -> 0.          (G1)

This is the exact kind of statement in PR25 C1–C5. Its recorded review does not extend it to eta=eta(r).

**G2 (sharpened finite-r strip envelope).** There are D,c1,epsilon1,r1>0 such that for 0<r<=r1 and annular |v|<=epsilon1,

    0<=F_(j,r)(u,v)<=D s^-14 exp(-c1/s^2),
    s=max(r,|v|).                                          (G2)

This is a consequence of PR28's equations(17) and the two cases immediately below them IF that candidate argument is valid. Its all-height bound majorizes the windowed count. We do not assert that the outstanding full analytic review of PR28 has been completed.

For fixed eta<=min(epsilon0,epsilon1,sqrt(c1/7),sqrt(2c_*/13)) and r<=eta, the functions s^-14 exp(-c1/s^2) and s^-13 exp(-c_*/s^2) are increasing on (0,eta]. Splitting the annulus gives the explicit inequality

    sup_(K_AB, parameters,j)|F_(j,r)-Lambda_j|
      <= R_r(eta)
         +D eta^-14 exp(-c1/eta^2)
         +C_* eta^-13 exp(-c_*/eta^2).                       (G3)

First fix eta and take r->0 in R_r(eta); then send eta->0. This proves uniform convergence across the full annulus under G1 and G2. Essential suprema may be used if intensities are specified only almost everywhere.

Therefore the **conditional** full-annulus conclusion is

    E_QW N_1(rE;window)=r^3 int_E Lambda_1 + r^3 o(1) area(E),
    E_QW N_0(rE;window), E_QW N_2(rE;window)
                                      =r^3 o(1) area(E),    (G4)

uniformly over Borel E and the declared compact marks/frames. In particular the finite positive saddle coefficient survives extending the fixed-transverse chart over the axis. This is NOT a global persistence/elder theorem.

No quantitative rate for o(1) follows without quantitative control of R_r(eta). Choosing eta=eta(r) inside (G1) alone would repeat the old moving-cutoff error. A spike f_r(v)=r^-1 1{r<v<2r} converges to0 on every fixed off-axis chart while its integral remains1; G2 is the load-bearing exclusion of that behavior.

## 6. What this does not establish

A positive cubic EXPECTED count does not give a cubic lower bound for the probability of a witness. For example N_m=m^2 with probability m^-5 and otherwise0 has E N_m=m^-3 but P(N_m>0)=m^-5. Factorial-moment or comparable anti-clustering bounds would be an additional requirement. Being a critical saddle of an intermediate height is also not sufficient to be an elder-rule obstruction.

No pin neighborhoods, growing outer radius, intermediate physical scales, multiple-witness collisions, kdown0, dimension3, uniform L, numerical covariance enclosures or theorem-status changes follow. PR25's density-transfer Section D is a different interface and is not reviewed here. The near-axis kernel result and the conditional G1+G2 implication remain separate from acceptance of either parent theorem.

## 7. Reproducibility and independent-review questions

The standard-library exact tests evaluate the full cubic's values, gradients and Hessian determinants from its monomial coefficients; they do not import PR25/28 implementations. They cover both signs of v, all six original pins, the witness equations, the absolute q-to-w Jacobian, prefactor104976 and powers k^8 |v|^-13, type-domain bounds, two-coordinate coercivity, the Gamma6 differential identity, the two-sided strip factor, and scope sentinels. These finite checks do not prove Gaussian regression or a general continuum assertion.

Review T1: (K2)–(K6), especially the absolute Jacobian and density coordinate a=0. T2: uniform Gaussian input constants and contact coercivity (K7)–(K10). T3: continuity, tail formula and coefficient positivity (K11)–(K13). T4: the order of limits and exact imported assumptions in (G1)–(G4). Any failed input leaves the corresponding conclusion conditional. No independent-review credit is awarded to this author-side continuation.

## Sources and reconnaissance

Project sources read through exact GitHub content: PR25 `ad35e46d15c2815c36746442808a1626a9724e8a`, `reviews/collision_mechanism_20260925/NOTE.md`, blob `3ee3082911f4e8ebee93805633a326940aee17bf`; PR28 `dedc69e1b786f7ad148e6b66718277f4145c99cd`; PR31 review `8373c3a7b9d8e5aebc69465d09fa7fcad437e8a5`, blob `ddf6859994d1b5cee855748520f8484b99a3a921`. The review self-identifies xAI/Grok and accepts only its named fixed-chart interfaces. It does not review this new note.

External primary reference actually opened: NIST DLMF 8.4.8 and 8.4.11, https://dlmf.nist.gov/8.4, for the integer-order upper incomplete-gamma identity; the substitution and factor bookkeeping are written explicitly above. Armentano–Azais–Leon https://arxiv.org/html/2304.07424v3 was opened as marked Kac–Rice background, not used to waive the parent conditional-count hypotheses. No worldwide novelty claim is made for Gaussian tails, change of variables, or the compact-domain gluing argument.
