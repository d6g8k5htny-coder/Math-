# D5: compact collar and fixed-scaled-ball synthesis

Object: OA-D5-COMPACT-COLLAR-20260928-v1.
Author: OpenAI / ChatGPT, foreground continuation.
Disposition: AUTHOR-SIDE ANALYTIC CANDIDATE; NONAUTHOR REVIEW REQUIRED.
Scientific effect: NONE. No status, proof-index verdict, graph, prize, or seal changes.

## 1. Intent, sources, and exact claim

This note addresses the region between the two punctured endpoint disks and the reviewed fixed annulus. It is not a global RN, elder-selection, or quantitative lifetime theorem. All constants are qualitative; the torus side and outer scaled radius are fixed.

The unchanged companion `PUNCTURED_PIN_PROOF.md` is OA-D5-PUNCTURED-PIN-20260928-v1, 23771 bytes, SHA256 `f972e50bc07674ebce9d971d1a1bd4dba2f8036dde37ecb57d8a44a35650f76a`. Its publication statement records the earlier local-delivery event, not the current repository publication. The present file is new, not an edit to that frozen source.

Read also `frontiers/rn_annulus_bridge_20260925/PROOF.md` in `d6g8k5htny-coder/Math-` at `582c05b4c5a28dca164605313a0ac8bad81206d5` (original blob `6f317515b3d417661f86e2fed09bc7d950899c2b`), especially its endpoint regression and deterministic three-Hessian argument. The reviewed short-edge source is Math-#103 at `be08396071d43a14fa4f3d6d1cb8bdd4cccaf6d2`, merged at `582c05b4c5a28dca164605313a0ac8bad81206d5`. Claude's review of that source is comment `5871487348`: its deterministic confirmation is not a review of this new Gaussian collar argument.

Use the exact variance-one periodized planar Gaussian field with fixed T>0 and covariance

    K_T(h) = sum_(n in Z^2) exp(-|h+Tn|^2/2)
             / sum_(n in Z^2) exp(-|Tn|^2/2).

Birth marks b are in a fixed compact interval; 0<k_-<=k<=k_+<infinity. Frames range over O(2). In frame coordinates set

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Let Q_r be the continuous Gaussian regression law of these six observations. Write F_j(H)=|det H| on nonsingular symmetric matrices of negative index j, and zero otherwise. Retain the original weight and normalizer

    W_r=F_2(H_M)F_1(H_S), Z_r=E_Qr W_r,
    dQ_r^W=(W_r/Z_r)dQ_r.

For fixed R>=1 and 0<eta<=1/4, define the compact scaled collar

    C_(eta,R) = {(u,v): u^2+v^2<=R^2,
                       (u+1/2)^2+v^2>=eta^2,
                       (u-1/2)^2+v^2>=eta^2}.

**Collar candidate.** There are C,r_*>0, uniform in the stated marks, frames, indices and Borel E subset C_(eta,R), such that

    E_(Q_r^W) N_j(r E) <= C r^3 |E|,  0<r<=r_*.        (C1)

N_j counts all-height critical points of index j; |E| is planar area. Equivalently, the physical-area intensity is at most Cr. Constants may depend on T,R,eta and the mark ranges. This is not uniform as R grows, eta shrinks, T varies, or k approaches zero.

**Synthesis candidate.** Combining (C1) with the companion punctured-pin theorem gives the same estimate for every Borel subset of

    {|(u,v)|<=R} minus {(-1/2,0),(1/2,0)}.              (C2)

The two prescribed critical points must be removed. Including them adds fixed atoms. The synthesis depends on BOTH candidate proofs being correct; no review of one is transferred to the other.

## 2. Endpoint estimates being consumed

The companion's Sections 3 and 7 give, for the exact field,

    sup_(r,b,k,frame) E_Qr ||f||_(C^m)^s < infinity
    for every fixed finite m,s,
    Z_r >= c_Z r^2.                                    (C3)

The norms cover the whole torus, hence every local Taylor segment. Its endpoint frame is an invertible combination of the original six observations with bounded targets and a positive contact covariance. Positive Fourier variances on the whole lattice imply positive definite covariance for every finite list of distinct one-site derivative monomials; compactness of O(2) makes that floor uniform. The Gaussian-decaying Fourier amplitudes also give all fixed derivative-supremum moments. Gaussian regression on the endpoint frame proves the moment assertion. The normalizer uses an event where the residual transverse curvature is in [-2,-1], giving the prescribed endpoint types and determinants of order r, with uniformly positive probability.

These are explicit source-bound imports from the companion, not independently accepted premises. A defect in either (C3) blocks this application and the synthesis. The polynomial observation floor below is proved UNCONDITIONALLY and only then passed to the six-pin Schur complement; it does not incorrectly assert that all Taylor coefficients remain free after conditioning.

## 3. Degree-five value-and-gradient interpolation at three sites

Let a=(-1/2,0), b=(1/2,0), c=(u,v) with c in C_(eta,R). All three are distinct and their pairwise distances are bounded below by min(1,eta). Let P_5 be the scalar polynomials in two variables of total degree at most five. Its dimension is 21. Consider

    B_c: P_5 -> R^9,
    P |-> (P(a),grad P(a),P(b),grad P(b),P(c),grad P(c)).

**Lemma.** B_c is onto, including collinear configurations and c=(0,0). Its smallest row singular value has a uniform positive lower bound on C_(eta,R), using the fixed monomial basis.

**Proof.** Choose a unit direction w such that the three projections t_i=w dot x_i are distinct. Only three forbidden perpendicular directions need be avoided. Let z_i=w_perp dot x_i and

    L_i(t)=product_(j!=i) (t-t_j)/(t_i-t_j).

The polynomials

    h_i(t)=[1-2 L_i'(t_i)(t-t_i)] L_i(t)^2,
    d_i(t)=(t-t_i)L_i(t)^2,
    e_i(t,z)=(z-z_i)L_i(t)^2

have total degree at most five. At the three sites, h_i has value delta_ij and zero gradient; d_i has zero values, w-direction derivative delta_ij and zero transverse derivative; e_i has zero values and w-direction derivatives, and transverse derivative delta_ij. The double zero at the other sites eliminates their derivative responses, including when their z coordinates differ. These nine polynomials prescribe arbitrary values and directional gradients. The two directions form an orthonormal basis, so B_c is onto in the original coordinates as well.

The entries of B_c are continuous polynomials in (u,v). Surjectivity holds at every point of the compact collar, hence the least eigenvalue of B_c B_c^T has a positive minimum. A single continuous choice of w is NOT needed: w proves pointwise surjectivity, while compactness is applied to the fixed monomial evaluation matrix itself. QED.

This is why a midpoint-axis degeneracy of the older three-column annulus frame is not an obstruction to the following coarse estimate. No claim that that smaller frame is invertible at the midpoint is made.

## 4. A deliberately coarse, uniform polynomial covariance floor

Before conditioning, collect the nine observations

    V_r = (f(ra), r grad f(ra), f(rb), r grad f(rb),
           f(rc), r grad f(rc)).

Taylor-expand f about the midpoint through total degree five. Let J_5 contain the 21 coefficients D^alpha f(0)/alpha! and let D_r be diagonal with entries r^|alpha|. In every fixed L^s, uniformly over the collar and frames,

    V_r = B_c D_r J_5 + R_r,  ||R_r||_(L^s) <= C_s r^6. (C4)

For the gradient entries the Taylor error is O(r^5) before multiplication by r, so it is also O(r^6). Derivatives through degree six suffice; their supremum moments are supplied by the exact Fourier series. This is not a numerical Fourier truncation.

For 0<r<=1, the smallest diagonal entry of D_r is r^5. The covariance of J_5 is uniformly positive definite. Therefore, for every unit row t in R^9,

    std(t B_c D_r J_5) >= c r^5 ||t B_c|| >= c' r^5.

Centering R_r changes only the constant in its L^2 bound. The L^2 triangle inequality now gives

    std(t V_r) >= c' r^5-C r^6 >= (c'/2)r^5

for all sufficiently small r, uniformly. Hence

    Cov(V_r) >= c r^10 I_9.                            (C5)

Remove the auxiliary witness VALUE observation. Next unscale the gradient entries by r^-1. Since this unscaling is diagonal with entries at least one, the covariance lower bound c r^10 still holds for the eight raw observations consisting of the original six pins and grad f(X).

Let Sigma_X=Cov_Qr(grad f(X)). The Schur variational formula gives

    t Sigma_X t^T = inf_s Var(t grad f(X)+s endpoint_observations)
                  >= c r^10 ||t||^2.                   (C6)

Thus Sigma_X>=c r^10 I_2. Its largest eigenvalue is bounded above because conditioning a Gaussian vector decreases its centered covariance.

IMPORTANT: the ninth value is an AUXILIARY UNCONDITIONAL Gram coordinate, deleted before the Schur complement. No witness value is conditioned, and no height-window factor appears anywhere. The actual Kac-Rice application has exactly six-plus-two observations.

## 5. The pinned cubic drift is separated from zero near the axis

In midpoint coordinates write D(u)=u^2-1/4. The exact endpoint cubic is

    H_r(x)=b-k r^3/2-(3k r^2/2)x+2k x^3.

With endpoint-law actual jets T_3=f_xxz(0), C_3=f_xzz(0), S_0=f_zz(0), Taylor and the original pins give, uniformly on |u|,|v|<=R,

    G_1 := f_x(ru,rv)/r^2
         = 6k D(u)+uv T_3+(v^2/2) C_3+O_(L^s)(r),
    G_2 := f_z(ru,rv)/r
         = v S_0+O_(L^s)(r).                            (C7)

For example, the endpoint Hermite remainder gives g'(ru)-H_r'(ru)=O_(L^s)(r^3); the transverse-gradient interpolant vanishes at the pins and gives h'(ru)=r u T_3+O_(L^s)(r^2). Expanding in rv supplies the uv and v^2 terms. The second line retains the f_zz(0) term; the other cubic terms carry an extra r. All remainder constants depend only on fixed R and the source moment bounds. In particular,

    |E_Qr G_1-6kD(u)| <= C(|v|+r),
    Var_Qr(G_1) <= C(v^2+r^2).                         (C8)

Choose a fixed v_0>0 sufficiently small. For |v|<=v_0<=eta/2, the collar inequalities give |u+1/2|,|u-1/2|>=eta/2 and |D(u)|>=eta^2/4. After reducing v_0 and r_* using (C8),

    |E_Qr G_1| >= d_0>0.                               (C9)

The drift can have either sign. Its absolute value, not its sign, is used. The lower bound on k is essential. Without a collar separation from both pins, this step would not be uniform.

For any positive Gaussian covariance Sigma and mean m,

    m^T Sigma^-1 m >= m_1^2 / Sigma_11.                 (C10)

This is Cauchy-Schwarz in the covariance inner product. Applying it to the first physical gradient component and using (C8)-(C9) gives a Gaussian factor exp[-c/(r^2+v^2)]. It is valid for the JOINT density, not a replacement of that density by a marginal probability.

## 6. Very near the axis: polynomial loss is harmless

Take |v|<=r^(1/3), with r_* small enough that this strip lies inside |v|<=v_0. By (C6), the two-dimensional density prefactor is at most C r^-10. Since r^2+v^2<=2 r^(2/3),

    p_(grad f(X)|pins)(0)
      <= C r^-10 exp[-c r^(-2/3)].                     (C11)

We also need a full-field conditional sixth moment, not just a finite Hessian moment. Put K=1+C||f||_(C^3) on the torus, large enough to dominate Hessian norms and their Lipschitz constants. Under Q_r, K has all fixed moments by (C3). Cross-covariances of f and its first three derivatives with grad f(X) are uniformly bounded by Cauchy-Schwarz. The inverse of Sigma_X is at most C r^-10. Subtracting the full Gaussian regression on grad f(X) gives an independent residual with C^3 sixth moment at most C r^-60, by the triangle inequality. The conditional mean at grad f(X)=0 has the same coarse bound; the endpoint-conditioned gradient mean is bounded. Consequently

    E_Qr[K^6 | grad f(X)=0] <= C r^-60.                 (C12)

This estimate is intentionally very loose. No independence of the three Hessians is used. The construction retains the original endpoint pins, and the norm covers all required segments.

The absolute product of three planar Hessian determinants is at most C K^6. Divide once by the original normalizer in (C3), multiply (C11) and (C12), and use weighted Kac-Rice:

    rho_j^W(X) <= C r^-72 exp[-c r^(-2/3)].             (C13)

The 111th positive term of exp(c r^(-2/3)) gives

    exp[-c r^(-2/3)] <= 111! c^-111 r^74.

Thus (C13)<=C r^2<=C r. The exact longitudinal midpoint and the entire q=0 collar are covered. The power 111 is just a convenient integer, not an optimal constant.

## 7. The rest of the near-axis strip: a sharper transverse covariance

For r^(1/3)<=|v|<=v_0, use the reduced gradient G in (C7) and J=(T_3,C_3,S_0). Conditional on the six pins, J has covariance bounded above and below: its three monomials are distinct from those in the contact endpoint frame. Write

    G=(6kD(u),0)+B(u,v)J+R,
    B = [uv, v^2/2, 0; 0, 0, v],  ||R||_(L^2)<=Cr.     (C14)

The rows are orthogonal in coefficient space, and

    det(B B^T)=u^2 v^4+v^6/4,
    trace(B B^T)<=C_R v^2.

Therefore the smallest singular value of B is at least c_R v^2, including u=0. The centered remainder changes any standard deviation by at most Cr. Since

    r/v^2 <= r^(1/3) -> 0

on this region, the L^2 perturbation argument gives

    c v^4 I_2 <= Cov_Qr(G) <= C v^2 I_2.                (C15)

The lower bound is deliberately weaker than the determinant expression, but sufficient. The physical gradient map is diag(r^2,r), with determinant r^3. Using (C9) and the upper variance bound in (C15),

    p_(grad f(X)|pins)(0)
        <= C r^-3 |v|^-4 exp[-c/v^2].                  (C16)

Regress the whole field on G. Its cross-covariance derivatives through degree three are bounded and the inverse covariance has norm at most C|v|^-4. The bounded mean and centered moments of G, together with (C3), yield

    E_Qr[K^6 | grad f(X)=0] <= C |v|^-24.               (C17)

As before, the residual-field construction and triangle inequality prove this estimate directly. It is a supremum moment after the additional witness condition, not an endpoint-only substitute.

The deterministic three-critical-point estimate from the fixed-annulus source applies on every bounded noncollinear triangle, without requiring |u|>1:

    |det H_M det H_S det H_X| <= C_R r^6 |v|^-6 K^6.    (C18)

To see this, the M-to-S critical-segment identity gives ||H_M e_x||<=Lr/2. The M-to-X identity gives a bound on H_M(u+1/2,v); subtract its e_x part and divide by v to bound the other column. Transport by the Lipschitz bound to S and X. All three Hessian norms are at most C_R r L/|v|; each determinant is quadratic in dimension two. This argument is deterministic and remains valid under the full Gaussian conditioning.

Combining (C3), (C16)-(C18),

    rho_j^W(X) <= C r |v|^-34 exp[-c/v^2] <= C' r.      (C19)

The last bound follows, for example, from the 17th positive exponential-series term. The r powers are -2-3+6=1; the v powers are -4-24-6=-34. There is no extra factor for a height window.

## 8. Transverse compact remainder

For |v|>=v_0 in the bounded collar, the matrix B in (C14) has a fixed positive singular-value floor. Its O_(L^2)(r) error can be absorbed uniformly. The reduced gradient mean, inverse covariance and full conditional C^3 sixth moment are bounded, so the physical density is O(r^-3). Estimate (C18), with |v|>=v_0, gives a conditional determinant product O(r^6). Division by Z_r>=c_Zr^2 leaves rho_j^W<=Cr.

This also checks the interface at u near either endpoint coordinate but with substantial transverse displacement. No assertion that D(u) stays away from zero is needed in this third region. The three regions cover C_(eta,R), and their overlaps use compatible estimates.

## 9. Weighted Kac-Rice and integration

For fixed r, work in an open neighborhood of the compact collar that still avoids the two endpoints. Distinct-site derivative nondegeneracy follows either from Fourier uniqueness or the local polynomial floor just proved after slightly enlarging the compact chart. The endpoint-conditioned field has smooth paths and continuous Gaussian conditional laws. For the counted field grad f, use the nonnegative weight W_r times the indicator of the nonsingular index-j witness Hessian. Endpoint filtered determinants are continuous through singular matrices; the witness-type set is open; hence the mark is lower semicontinuous. Auxiliary endpoint and witness Hessians are jointly Gaussian with grad f under Q_r. Truncation and monotone convergence handle unbounded marks.

Armentano--Azais--Leon, arXiv:2304.07424v3, Theorems 2.2 and 7.1 and Remark 8, therefore give at the fixed zero gradient level

    rho_j^W(X) = Z_r^-1 p_(grad f(X)|pins)(0)
       * E_Qr[W_r F_j(H_X) | grad f(X)=0].              (C20)

Q_r is Gaussian; the tilted law Q_r^W is not claimed Gaussian. The witness determinant is counted exactly once. The mean shift is that of the exact original pins. Integration uses dX=r^2 du dv. The bounds in Sections 6--8 imply (C1).

## 10. Gluing, with a precise remaining boundary

Choose eta=1/4. Partition a Borel subset of the fixed scaled ball into its intersections with the two punctured radius-1/4 endpoint disks and the remaining collar. Assign disk boundaries to the disks and the remainder to the collar, so no double counting is needed. The companion's theorem applies to the disks, this note applies to the remainder, and translating between midpoint and endpoint scaled coordinates preserves area. Taking the minimum of their positive radius cutoffs and maximum of their constants proves (C2) at author-side level.

Choosing any fixed R greater than the inner radius A>1 of the reviewed annulus supplies an actual overlapping cover to that annulus. This repairs the old geometric hole between scaled endpoint disks reaching midpoint radius at most 3/4 and the annulus beginning beyond 1. No limiting process eta->0 or R->infinity is used.

This synthesis does NOT cover R=R(r)->infinity, the intermediate range r<<|X|<<rho, shrinking multiple-witness separation, unrestricted gap marks, changing torus side, dimensions above two, numerical constants, or an elder-pairing/selection claim. It does not recover missing historical RN/JETMOD/24-jet carriers. No scientific-status promotion follows from publication or passing finite tests.

## 11. Reproduction and review requests

`collar_algebra.py` and `test_collar_algebra.py` provide exact rational finite checks of the degree-five cardinal functions, the nine-row value/gradient matrix including midpoint-axis configurations, the failure of degree four on a collinear triple, the transverse Gram identity, scale orders, crossover and power ledgers, and the disk/collar cover. The complete analytic interpolation and compactness argument is in the proof, not replaced by the sampled ranks. The auxiliary ninth value is tested as distinct from the actual eight conditioned observations.

`run_collar_validation.py --output NEW_DIRECTORY` runs ten named tests in normal and optimized modes and verifies six deliberate mutants by assertion failures, not syntax/import failures. The finite result summary is separate from any continuum or Gaussian acceptance. The prior pin suite is retained unchanged and rerun separately.

Review priorities: (i) interpolation surjectivity for arbitrary collinear/noncollinear triples and the compact uniform floor; (ii) the r^5 Taylor standard-deviation floor versus r^6 error; (iii) deletion of the auxiliary value and the Schur variational inequality; (iv) whole-field moments after additional conditioning; (v) the drift bound away from both pins; (vi) r^(1/3) crossover and the two power ledgers; (vii) exact compatibility with the companion and reviewed annulus. A defect in any load-bearing interface blocks consumption as a closed dependency.

## 12. External reconnaissance and attribution

Primary framework inspected in this pass: Armentano, Azais and Leon, *On a general Kac-Rice formula for the measure of a level set*, arXiv:2304.07424v3, https://arxiv.org/html/2304.07424v3, especially Theorems 2.2/7.1 and Remark 8. These justify the framework subject to checked hypotheses; they are not credited with this collar estimate.

The existing local sources already use Taylor interpolation, exact pin regression, deterministic Hessian suppression and Gaussian absorption. The new element here is the explicit compact-collar application, using a degree-five auxiliary nine-row polynomial floor before discarding the witness value, with a sharper transverse estimate away from a shrinking axis strip. No worldwide-first or comprehensive novelty claim is made.
