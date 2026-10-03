# Compact positive-gap Gaussian transfer in the planar soft layer

Object: C102-COMPACT-POSITIVE-GAP-GAUSSIAN-TRANSFER-20261003-v1.
Author: OpenAI/Codex reader_surface_audit, acting for Dylan Roy — delegated AI work.
Root01a0bbb5 contributed analytical coordination and a coordinate-factor cross-check; that is author-side work, not nonauthor review.
Disposition: frozen author-side proof candidate when accompanied by its final byte identity; fresh nonauthor review required. Organizational independence 0; human review NONE; personal reading PENDING; scientific effect NONE.

This note proves a Gaussian and determinant-weight transfer on one fixed compact positive-gap interval under the original field law. In particular it makes the cutoff dependence explicit and proves a rate for the full normalizer and the candidate prefactor. It does not extend an actual elder-failure event theorem.

## 1. Model, sources, coordinates and statement

Fix L>0 and the centered variance-one Gaussian field on X=R^2/(L Z^2) with covariance

    K_L(z) = sum_{n in Z^2} exp(-|z+Ln|^2/2)
             / sum_{n in Z^2} exp(-|Ln|^2/2).

Fix a nonempty compact birth set B0 in R and K=[k_-,k_+] with 0<k_-<=k_+<infinity. All constants below may depend on L,B0,K and the explicitly indicated moment exponents. They are uniform in b in B0, k in K and every orthonormal frame R=(u,e), including either orientation. They are not asserted uniform as L varies or k_- decreases to zero. The torus need not be invariant under arbitrary rotations: R stays a parameter throughout.

The exact source set is in SOURCE_IDENTITIES.json, with byte-for-byte copies in sources/. C91 is native main229 comment5963566666, SHA256 74a9ee276c3647276deb544c6d83e3cf21f708f55f9009fa4db5cc49c9d0e9aa. C92 is native comment5963825788, SHA256 6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a. The pinned Math- commit for P/E1/E2/REC/CUB is 044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43. P is blob dfed3b8d318a3ab1950957f393307733a4bef3f2; CUB is blob bb446d08db8a944537a743ad550b88c1c2ad5758. P is read with its E1 inverse-square-root congruence correction, E2 Borel repair and REC reading rule/embedding amendment. Only P's Gaussian/normalizer coordinates and its candidate ledger are used; no cap or elder-selection theorem is used to prove the estimates here. CUB supplies the comparison convention and contact parity; both are re-derived below. C92 motivates the fixed-k argument, whose required estimates are re-derived with compact k and explicit cutoffs. C101 is not an input and its draft has not been read for this work. Source headers are historical metadata, not current acceptance registers.

In the periodic lift in frame R put M=(-r/2,0), S=(r/2,0). Let Q_{r,b,k,R}, abbreviated Q_r, be the continuous Gaussian regression law at

    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Let

    W_r=|det H_M det H_S| 1{H_M negative definite, index(H_S)=1},
    Z_r=E_{Q_r} W_r,  z_r=Z_r/r^2,  dQ_r^W=(W_r/Z_r)dQ_r,
    N=1+max_{|alpha|<=4} sup_X |D_R^alpha f|.

The index counts strictly negative eigenvalues; the weight is zero at singular endpoints. Z_r is the FULL normalizer, with no soft-layer restriction, pin density, coordinate Jacobian or adjacency event in it.

Write the physical midpoint jets as

    J=(A,a,beta,c)=(f_zz,f_xxz,f_xzz,f_zzz)(0),
    y=(lambda,gamma,B,C)=(-k A/r,a,k beta,k^2 c), t=(gamma,B,C),
    |t|=|gamma|+|B|+|C|.

Here B is a scalar jet, distinct from the birth set B0. Set

    F_r(X,zeta)=(f(rX,rk zeta)-b)/(k r^3),
    G_y=2X^3-3X/2-1/2+(gamma/2)(X^2-1/4)zeta
                       -(lambda/2)zeta^2+(B/2)X zeta^2+(C/6)zeta^3,
    h_M=6lambda+3B-gamma^2/4, h_S=6lambda-3B+gamma^2/4,
    a_M=4h_M=24lambda-gamma^2+12B,
    a_S=4h_S=24lambda+gamma^2-12B,
    w(y)=(h_M)_+(h_S)_+.

These are the C91 anisotropic coordinates. In particular B=k beta and C=k^2 c; they are not the unscaled physical jets when k differs from one. On the typed model support h_M,h_S>0,

    w=h_M h_S <=36lambda^2,  lambda>0;                  (1.1)

else w=0. Thus everywhere 0<=w<=36(lambda_+)^2. Equality in the upper bound is possible, so this is a useful quadratic bound instead of a generic quartic matrix-norm bound.

Let U_r be the six centered observations defined in Lemma 1, with target v_{r,k}; let rho_{r,k}(A,a,beta,c) be the JOINT physical-jet density of J under Q_r. At contact U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz)(0), v_{0,k}=(b,0,0,12k,0,0). Define

    g_0(y)=k^-4 rho_{0,k}(0,gamma,B/k,C/k^2) w(y),
    z_0=36k^2 E[f_zz(0)^2 1{f_zz(0)<0} | U_0=v_{0,k}].   (1.2)

The density rho_{0,k} at A=0 includes the marginal density of A at zero. It is not the normalized law of the other jets given A=0. Dependence on b,k,R is suppressed, not averaged.

For Lambda>=0 let H=1+Lambda and D_Lambda=[-Lambda,Lambda] x R^3. Introduce the unnormalized finite measure

    mu_r(E)=r^-5 E_{Q_r}[W_r 1{y in E}], E subset D_Lambda.

There is a fixed r0>0 depending only on L,B0,K such that the following assertions hold. Estimates involving Lambda require exactly

    0<r<=r0,    r H/k_-<=1.                             (1.3)

There is no additional implicit condition that Lambda be fixed. In particular Lambda may be chosen as a deterministic function of r subject to (1.3). No smallness of r H^4 is required for the inequalities; convergence along growing cutoffs requires that extra quantity tend to zero.

**Gaussian-transfer theorem.** The measure mu_r has the exact density

    g_r(y)=k^-4 rho_{r,k}(-r lambda/k,gamma,B/k,C/k^2)
                     E_{Q_r}[W_r/r^4 | J=(-r lambda/k,gamma,B/k,C/k^2)]. (1.4)

For every fixed finite q>=0 and p>=1 there are finite constants C_q,C_{p,q}, independent of Lambda,r,b,k,R within (1.3), such that

    integral_{D_Lambda}(1+|t|)^q |g_r-g_0| dy <= C_q r H^4,             (1.5)
    r^-5 E_{Q_r}[W_r N^p (1+|t|)^q 1{y in D_Lambda}]
                                                   <= C_{p,q} H^3. (1.6)

These preserve the actual correlated weight W_r. There is no replacement of a remainder or a Hessian by an independent sample.

Let T={a_M>0,a_S>0} be the model typed region. For its absolute typing-margin strip and the adjacent outside strip, put

    E_{Lambda,delta}={y in D_Lambda cap T:
                          min(a_M(y),a_S(y))<=delta},
    Eout_{Lambda,delta}={y in D_Lambda outside T:
                          min(|a_M(y)|,|a_S(y)|)<=delta},
    0<delta<=1.

The model and actual measures satisfy

    integral_E (1+|t|)^q g_0 dy <= C_q H delta^2,
    integral_E (1+|t|)^q g_r dy
                         <= C_q [H delta^2+r H^3 delta],
    integral_Eout (1+|t|)^q g_r dy <= C_q r H^3 delta,
    integral_{D_Lambda outside T}(1+|t|)^q g_r dy <= C_q r H^4.       (1.7)

The first strip lies inside the MODEL typed region. The next two estimates retain actual off-T leakage separately; they do not assume actual and model typing already agree. The inside-strip powers also imply C_q[H^2 delta^2+r H^4 delta]. The margin is absolute in a_M,a_S, not relative and not an inverse-margin moment.

Independently of Lambda, uniformly on the fixed compact parameters,

    0<z_*<=z_0<=z^*<infinity,
    |z_r-z_0|<=C_z r,  z_r>=z_*/2,
    E_{Q_r}[(W_r/r^2)N^p]<=C_p,  E_{Q_r^W}N^p<=C_p.                 (1.8)

Consequently the density of eta_r(E)=r^-3 Q_r^W(y in E) is g_r/z_r, and

    integral_{D_Lambda}(1+|t|)^q |g_r/z_r-g_0/z_0| dy <= C_q r H^4,
    integral_E (1+|t|)^q g_r/z_r dy
                         <= C_q [H delta^2+r H^3 delta].             (1.9)

The outside-strip and full off-T estimates in (1.7) also hold after division by z_r.

Let pi_r(R;v_{r,k}) be the density of U_r at its exact target, not the circle constant. Then

    pi_r=pi_0+O(r^2),
    A_r:=12 pi_r z_r=A_0+O(r),  A_0:=12 pi_0 z_0>0,                 (1.10)

with uniform bounds and a positive uniform floor for A_0. These are prefactors in P's candidate pair ledger. No actual elder-failure event or lifetime-density refinement is asserted here.

## 2. Lemma 1: one original field law and uniformly nondegenerate regression

Write x_-=-r/2, x_+=r/2, evaluating at transverse coordinate zero. Define

    U_r=((f(x_-)+f(x_+))/2,
         (f(x_+)-f(x_-))/r,
         (f_x(x_+)-f_x(x_-))/r,
         (6/r^2)[f_x(x_-)+f_x(x_+)-2(f(x_+)-f(x_-))/r],
         (f_z(x_-)+f_z(x_+))/2,
         (f_z(x_+)-f_z(x_-))/r).

This is an invertible linear transformation T_r of the six original pin observations with

    |det T_r|=12 r^-5,
    v_{r,k}=(b-k r^3/2,-k r^2,0,12k,0,0).             (2.1)

For example the four axial rows have absolute determinant 12/r^4, and the transverse average/difference block has absolute determinant 1/r. At r=0 the continuous contact vector is U_0 above. Set V_r=(U_r,J), Gamma_r=Cov(V_r), and Sigma_r=Cov(U_r). Neither covariance depends on b or k; they depend on r and R under the original covariance K_L.

**Proof of uniform rank and rates.** The Fourier coefficients of K_L are strictly positive at every n in Z^2 and proportional to exp(-2 pi^2 |n|^2/L^2). Their square roots times any fixed polynomial in |n| are summable. Thus the real Fourier expansion converges in each finite C^m mean norm, and all fixed derivative-supremum moments are finite. At contact V_0 lists exactly the ten distinct planar jets of orders zero through three. A vanishing-variance linear combination would give a degree-at-most-three polynomial multiplier vanishing on the entire integer lattice. Fix one lattice coordinate, use the one-variable polynomial zero theorem in the other, and then apply it to the coefficient polynomials. The polynomial is zero. Rotation is an invertible substitution, so this proves rank in every frame.

The frame space O(2) is compact. Covariances depend continuously on it, so Gamma_0 has a uniform positive least eigenvalue and finite greatest eigenvalue. Centered differences give U_r-U_0=O(r^2) in every fixed finite L^p norm, uniformly in frame. In the apparently singular fourth row the exact expansion is f_xxx+(r^2/40)f_xxxxx+O(r^4); its integral-remainder form and Fourier summability justify the rate without cancellation of uncontrolled quantities. The same O(r^2) estimate holds for cross-covariances with the field and any fixed number of position derivatives, in their uniform norm. Hence for all sufficiently small r,

    cI<=Gamma_r<=CI,
    ||Gamma_r-Gamma_0||+||Gamma_r^-1-Gamma_0^-1||<=Cr^2. (2.2)

The same holds for Sigma_r. The constants are frame uniform, not a claim that different frames have identical covariance. Since v_{r,k}-v_{0,k}=O_K(r^2), the physical law J|U_r=v_{r,k} has bounded mean, uniformly elliptic covariance, and mean/covariance differences O_K(r^2) from contact. This follows directly from the block inverse and Schur complement formulas.

For any finite target s=(v_{r,k},J), take one unconditioned smooth field F with covariance K_L. The exact further conditional law is the law of

    f_{r,s}=F+Cov(F,V_r) Gamma_r^-1(s-V_r(F)).           (2.3)

Each conditioned observation has the specified mean and zero residual variance. This defines a continuous regression version for every target used here. The centered residual covariance is

    K_L-Cov(F,V_r) Gamma_r^-1 Cov(V_r,F),              (2.4)

independent of s, in particular independent of k at fixed r,R. The same formula with U_r alone defines Q_r. Multiplying a field sampled under Q_{r,b,1,R} by k and adding b(1-k) preserves the endpoint values required at gap k, but multiplies its centered residual covariance by k^2. The residual has a positive variance at unpinned generic evaluations by full-spectrum rank. For k!=1 this gives a different law. Thus amplitude scaling is not a legitimate identification with Q_{r,b,k,R}. Equation (2.3), with the original covariance, is the required construction. QED.

## 3. Lemma 2: conditional density and derivative moments with explicit cutoff control

For y in D_Lambda define s(y)=(v_{r,k},-r lambda/k,gamma,B/k,C/k^2). By (1.3), |r lambda/k|<=1. Since k remains in K, the other target coordinates have size at most C_K(1+|t|). Differentiating the mean in (2.3) through order four and using (2.2) gives a C^4 norm bound C(1+|t|). For the centered residual, each real Fourier coefficient has conditional variance no greater than its original variance. Minkowski's inequality and the summable Fourier weights bound its C^4 norm in every fixed L^p. No independence between its coefficients is needed. Therefore

    E[N^p | V_r=s(y)]<=C_p(1+|t|)^p, p>=1.            (3.1)

This bound is independent of Lambda under (1.3). In particular it is not C92's fixed-cutoff constant silently reused at a growing cutoff.

Gaussian interpolation also gives positive constants C,c, uniform under (1.3), such that with j(y)=(-r lambda/k,gamma,B/k,C/k^2) and j_0(t)=(0,gamma,B/k,C/k^2),

    rho_{r,k}(j(y))<=C exp(-c|t|^2),
    |rho_{r,k}(j(y))-rho_{0,k}(j_0(t))|
                    <=C r H (1+|t|)^2 exp(-c|t|^2).   (3.2)

Indeed interpolate the conditional means and covariance matrices: their differences are O(r^2), uniform ellipticity holds along the straight segment, and the derivative of a Gaussian density is the density times a polynomial of degree at most two with O(r^2) coefficients. The shift of the A coordinate is at most r|lambda|/k_-; interpolate it along [-1,1], differentiating once. Bounded means and this bounded A coordinate give one Gaussian majorant in the other three coordinates. The scaling (gamma,B/k,C/k^2) has upper and lower norm bounds depending only on K, so the majorant can be written in |t|. Integrating the two derivatives proves (3.2), using r<=1 and H>=1. These statements concern the JOINT physical-jet density, including its A density factor. QED.

## 4. Lemma 3: exact anisotropic determinant transfer and its actual moments

The map from y to J is diagonal with absolute determinant

    |det D_y J|=(r/k) * 1 * (1/k) * (1/k^2)=r/k^4.     (4.1)

Let D_k=diag(1,k). The chain rule at either endpoint gives

    Hess F_r=(1/(k r)) D_k H_i D_k,
    H_i/r=k D_k^-1 (Hess F_r) D_k^-1.                 (4.2)

The scalar k is positive; congruence preserves inertia. In dimension two the determinant factor in the second identity is k^2/(det D_k)^2=1. Thus exactly

    det(H_i/r)=det Hess F_r,
    D_r:=W_r/r^4=F_2(Hess F_r|_M) F_1(Hess F_r|_S),    (4.3)

where F_j(T)=|det T|1{index(T)=j}, set to zero on singular matrices. There is no additional k^4 multiplying D_r.

For comparison, CUB uses theta=(s,a,beta,c) with s=A/r. Here theta=(-lambda/k,gamma,B/k,C/k^2), dtheta=k^-4 dy. Its isotropic-coordinate polynomial P_theta obeys F's cubic identity G_y(X,zeta)=P_theta(X,k zeta)/k. Consequently its two endpoint determinant product equals w(y), consistently with (4.2). An amplitude change of this deterministic polynomial is an algebraic identity; it is not a change-of-law statement about the Gaussian field.

At the pins, the model Hessians are

    L_M=[[-6,-gamma/2],[-gamma/2,-lambda-B/2]],
    L_S=[[ 6, gamma/2],[ gamma/2,-lambda+B/2]].          (4.4)

Their pivots -6 and 6 imply F_2(L_M)=(h_M)_+ and F_1(L_S)=(h_S)_+, for every signed lambda and every t. For the saddle, F_1(T)=(-det T)_+ for all symmetric two-by-two T. For the maximum, use the negative first pivot and the determinant criterion. Their product is w, including all boundary cases. The two untruncated factors sum to 12lambda; this proves (1.1).

For precision about the deterministic input, put S_K=1+k_+, M1=max(k_-^-1,1), M2=max(k_-^-1,1,k_+). C91's exact pin Taylor argument gives, on |X|,|zeta|<=w0 with w0>=1 and r S_K w0<=L/4,

    |F_r-G_y|_j<=K_j N r w0^(4-j), j=0,1,2,
    K0=9/(64k_-)+1/16+S_K^4/(24k_-),
    K1=33/(128k_-)+1/16+M1 S_K^3/6,
    K2=17/(48k_-)+1/24+M2 S_K^2/2.                    (4.5)

The norms are maxima of coordinate derivative suprema of exact order j. C91 derives these by the two value/two axial derivative pins and the transverse gradient pins followed by C^4 Taylor's formula; its coefficients are evaluated at the actual midpoint jets. No Gaussian assertion is an input to (4.5). We use it only at w0=1 for the weight comparison. It gives

    ||Hess F_r|_i-L_i||_op<=2K2 r N.                  (4.6)

For symmetric two-by-two X,Y, including different types and singular cases,

    |F_j(X)-F_j(Y)|<=2 max(||X||,||Y||)||X-Y||.         (4.7)

When both contribute, telescope the two columns of the determinant and use Hadamard's inequality. If just one contributes, the connecting segment reaches a singular matrix; telescope from the contributing endpoint to that matrix. Along that segment the norm is at most the endpoint maximum and the length at most ||X-Y||. When neither contributes the difference is zero. This proves (4.7) without falsely making the inertia indicator itself Lipschitz.

With d=1+|lambda|+|t|, (4.4)-(4.7) give pointwise for the actual conditional field

    |D_r-w(y)|<=C r N(d+rN)^3.                         (4.8)

All four endpoint/model matrix norms are bounded by C(d+rN); each filtered determinant is at most the square of that bound, and the product difference yields (4.8). Combining with (3.1), for every fixed p>=1,

    |E[D_r | V_r=s(y)]-w(y)|
                       <=C r (H+|t|)^3(1+|t|)^4,
    E[D_r N^p | V_r=s(y)]
       <=C_p {lambda_+^2(1+|t|)^p
                        +r d^3(1+|t|)^(p+4)}
       <=C_p H^2(1+|t|)^(p+7).                       (4.9)

For the first two inequalities expand N(d+rN)^3, multiply by N^p when appropriate, and use its actual conditional moments through order p+4. For the last use d<=H(1+|t|), w<=36lambda_+^2, and rH<=k_- from (1.3), absorbing the fixed k_- into the constant. No N/jet/weight independence has been inserted. The first line also holds by taking the p=0 expansion directly. QED.

## 5. Lemma 4: cutoff-explicit density, moment and typing-edge estimates

Disintegrate the actual law of J under Q_r. Equations (4.1) and W_r=r^4 D_r give

    r^-5 * (r/k^4) * r^4 = k^-4,

which proves the exact density (1.4). All integrands are nonnegative for the identity, so Tonelli applies before any signed comparison. Using (3.2), (4.9), w<=36H^2 and the bounded k^-4 factor, one obtains

    |g_r-g_0|<=C r H^3 (1+|t|)^7 exp(-c|t|^2).         (5.1)

The determinant comparison contributes r(H+|t|)^3(1+|t|)^4, bounded by rH^3(1+|t|)^7. The density comparison contributes rH times a quadratic polynomial times w<=36H^2. Both have a common Gaussian majorant. Integration over a lambda interval of length 2Lambda<=2H and the Gaussian t integral proves (1.5). The same disintegration using the last line of (4.9) proves (1.6); its lambda factor is H and its conditional-weight factor H^2. These derivations explain the stated cutoff powers rather than absorbing them in unspecified cutoff constants.

Fix t. Each a_i is an affine function of lambda with derivative 24. The union of the two strips |a_i|<=delta has lambda length at most

    2 * (2delta/24)=delta/6.                           (5.2)

On the model support inside that union, both a_M,a_S are positive, one is at most delta, and a_M+a_S=48lambda<=48Lambda. Therefore

    w=a_M a_S/16 <=3Lambda delta <=3H delta.           (5.3)

Multiply (5.3) by the common Gaussian density majorant and integrate using (5.2). This gives C_q H delta^2. Integrate (5.1) over the same slices to bound the difference by C_q r H^3 delta. This proves the inside-strip estimates. On Eout and on all of D_Lambda outside T, g_0 is identically zero. Integrating (5.1) over the same strip slices gives C_q r H^3 delta for Eout; integrating over the full lambda interval gives C_q r H^4 for all off-T leakage. These are the remaining parts of (1.7) and retain actual weight where the model weight vanishes. No division by gamma, a_M or a_S occurs. In particular gamma=0 is included in these raw-coordinate Gaussian statements, regardless of its exclusion from a different rescaled geometric chart. QED.

## 6. Lemma 5: full normalizer rate without a spurious square-root loss

Use (2.3) with U_r alone to couple f_r with f_0 under their corresponding six-observation targets from the same unconditioned field. The O(r^2) estimates in Lemma 1 give, for each fixed p>=1,

    || ||f_r-f_0||_{C^2} ||_{L^p} <= C_p r^2,
    ||N(f_r)||_{L^p}+||N(f_0)||_{L^p}<=C_p.            (6.1)

The first follows by subtracting the two regression formulas: covariance functions and inverse matrices differ by O(r^2) in C^2, targets differ by O(r^2), and U_r(F)-U_0(F)=O(r^2) in L^p. Multiplication by the remaining uniformly bounded matrices preserves the rate. These are compact-target estimates under the original field, not amplitude rescalings.

Let A_c=f_{0,zz}(0). Put alpha_i=f_{r,xx}(i)/r, beta_i=f_{r,xz}(i)/r and A_i=f_{r,zz}(i). The exact gradient and height pins yield

    |alpha_M+6k|+|alpha_S-6k|<=C r N(f_r),
    |beta_i|<=N(f_r)/2,
    |A_i-A_c|<=C r T,                                 (6.2)

where one can choose T>=1 with every fixed moment uniformly bounded, by taking a constant multiple of 1+N(f_r)+N(f_0)+r^-2||f_r-f_0||_{C^2}. For the alpha bounds, the height difference and zero endpoint derivatives make 12k a positive weighted average of f_xxx on the segment; its variation is at most r||f||_{C^4}. Equivalently they follow from C91's axial pin identities. For beta, integral_{-r/2}^{r/2} f_xz=0 and the f_xxz Lipschitz bound give the endpoint average estimate. For A_i, compare with its midpoint using a third derivative, and then use (6.1).

The corrected E1 congruence is

    C_i=diag(r^-1/2,1) H_i diag(r^-1/2,1)
       =[[alpha_i,sqrt(r) beta_i],[sqrt(r) beta_i,A_i]],
    det C_i=det H_i/r,
    W_r/r^2=F_2(C_M)F_1(C_S).                         (6.3)

A general Lipschitz bound on C_i would lose sqrt(r). Instead, for every real alpha,A,c and j=1,2,

    |F_j([[alpha,c],[c,A]])-F_j(diag(alpha,A))|<=c^2.   (6.4)

For j=1 both sides are positive parts of c^2-alpha A and -alpha A, so the bound follows from the 1-Lipschitz positive part. For j=2, if alpha>=0 both filtered determinants are zero; if alpha<0 they are (alpha A-c^2)_+ and (alpha A)_+. This proves (6.4), including zero pivots and singular cases.

Apply (6.4) with c=sqrt(r)beta_i, and then (4.7) to compare diag(alpha_M,A_M) with diag(-6k,A_c), and diag(alpha_S,A_S) with diag(6k,A_c). From (6.2) each filtered determinant differs from its reference by at most C r T^2. Each factor and reference is at most C T^2. Their product therefore differs by at most C r T^4. The reference product is exactly

    F_2(diag(-6k,A_c)) F_1(diag(6k,A_c))
                              =36k^2 A_c^2 1{A_c<0}.

Taking expectations gives |z_r-z_0|<=C_z r with no discarded type-edge event and no independent-weight substitution.

The conditional scalar A_c is nondegenerate, with bounded mean and variance uniformly above zero and finite. This is a Schur complement of the positive contact covariance. On any fixed negative interval, for example [-2,-1], its density has a uniform positive lower bound by compactness of the means/variances. Since k>=k_->0, this proves a positive z_* lower bound for z_0; Gaussian moments prove a finite upper bound. Reduce r0 so C_z r0<=z_*/2. Then z_r>=z_*/2 for the FULL normalizer.

Finally the gradient-pin average bounds give |alpha_i|,|beta_i|<=C N and |A_i|<=N. The exact determinant identity det H_i/r=alpha_i A_i-r beta_i^2, with r<=1, gives W_r/r^2<=C N^4. The uniform unconditioned-on-J regression moments in (6.1) prove E_Q[(W_r/r^2)N^p]<=C_p. Division by z_r proves the full tilted moment bound in (1.8). QED.

For reference, contact even/odd parity gives the CUB factorization without changing this proof. Even-total-order jets are independent of odd-total-order jets because K_L is even and odd derivatives at zero vanish. The even pins are (f,f_xx,f_xz)=(b,0,0); the odd pins are (f_x,f_xxx,f_z)=(0,12k,0). Since A is even and (a,beta,c) odd,

    rho_{0,k}(0,a,beta,c)=p_b(0) q_k(a,beta,c),
    z_0=36k^2 m_{2,b},
    m_{2,b}=E[A_c^2 1{A_c<0} | even pins].             (6.5)

Frame and L dependence are suppressed. This is only a contact factorization. It neither makes the finite-r normalizer exactly proportional to k^2 nor identifies the conditional Gaussian laws at different k.

## 7. Lemma 6: normalized transfer, admissibility and candidate prefactor

Exactly

    r^-3 Q_r^W(y in E)=mu_r(E)/z_r.

The identity uses the full r^2 z_r normalizer. For all Lambda, the model weighted mass is bounded by C_q H^3, by (1.1) and the Gaussian majorant. Add and subtract g_0/z_r and use |z_r^-1-z_0^-1|<=Cr, the floor, and (1.5). This proves the first part of (1.9), since rH^3<=rH^4. Division of (1.7) by the full floor proves its second part. In particular a soft-layer renormalization is never substituted for eta_r.

All small-radius choices can be made before choosing Lambda or delta. Start with the spectral/regression radius in (2.2), and reduce r0 to be at most

    1, L/(8 sqrt(2)), L/[8(1+k_+)], z_*/(2C_z),         (7.1)

omitting the last restriction if C_z=0. This enforces REC's strict embedding bound and C91's w0=1 restriction, in addition to the common full-normalizer floor. The Lambda-dependent condition is precisely r(1+Lambda)/k_-<=1. A separate use of the deterministic Taylor bound on a growing window requires r(1+k_+)w0<=L/4, as explicitly stated in (4.5). Neither a geometric decision certificate nor a random inverse-margin estimate follows from these inequalities. For example Lambda=r^-a with 0<a<1/4 satisfies the cutoff admissibility eventually and makes (1.5) tend to zero. This is a statement about finite jet measures, not about an elder event.

The density pi_r is a six-dimensional Gaussian density. The covariance and exact target differences from contact are O(r^2), with uniformly elliptic covariance and bounded target. The ordinary Gaussian density derivative formula therefore yields |pi_r-pi_0|<=Cr^2. It also gives uniform finite upper bounds and a positive contact lower bound on the compact parameters. Combining with (1.8),

    |12pi_r z_r-12pi_0 z_0|
       <=12|pi_r-pi_0| z_r+12pi_0|z_r-z_0|<=Cr.

This proves (1.10).

To identify the convention rather than add a new Kac–Rice theorem: P §§10–12, read with E2, use midpoint z, directed separation h=ru, birth b and scaled gap k. The original six-pin density is 12r^-5 pi_r. In the plane the spatial polar factor is r dr d sigma(u), with ordinary arc-length measure on S^1, and the height transformation (b,s)=(b,b-kr^3) has Jacobian r^3. The determinant normalizer is r^2 z_r. Thus the exact candidate ledger is

    (12r^-5 pi_r) * (r dr d sigma) * (r^3 db dk) * (r^2 z_r)
                         =r A_r dr db dk d sigma.     (7.2)

Maximum and saddle roles are ordered, so there is no factor 1/2. Reversing the transverse basis changes none of the original zero-gradient pins or determinant weights; the prefactor descends from the frame to the axial direction. This does not invoke rotational invariance of the torus. QED.

## 8. Intended consumer and exact boundary of this leaf

The intended consumer is P §§10–12's compact-window candidate-minus-designated-elder PAIR density. P §11 obtains its O(ell^(2/3)) difference bound from the density identity (11.2) and the compact selection estimate. A future separate event theorem would need to establish, uniformly on the compact parameters, a statement of the form r^-3(1-p_r)=alpha_1+alpha_2+O(r^beta), with bounded coefficient and a specified beta>0, and justify the relevant event/tail composition. C102 does not establish that premise or identify its alpha_j. If it were supplied, (1.10) would provide the prefactor estimate needed in the ledger at r=(ell/k)^(1/3). For 0<beta<=1 the prospective loss coefficient would be the compact integral of A_0(alpha_1+alpha_2)/(3k^(5/3)), with prospective error ell^((2+beta)/3); for beta>1 the prefactor estimate here would only support beta replaced by min(beta,1). This is a map of required future inputs, not a lifetime theorem or a claim that its missing event premise holds.

That candidate-pair population is distinct from C99's once-counted replacement bars. No unrestricted all-gap remainder, all-bar theorem, k approaching zero, growing-L statement, actual failure-event quantitative extension, inverse-margin moment, or whole-field total variation is proved. The small-gap/intermediate/coarea work remains with Conjecture7 owner5957277321. No source, branch, review status or governing theorem Boolean is changed by this author-side leaf.

The accompanying standard-library rational controls check finite coordinate, pin, determinant and normalization identities, with invalid-scaling mutations required to fail. They do not prove Gaussian compactness, infinite Fourier convergence, analytic density rates, or a theorem verdict; those require this argument and a fresh substantive nonauthor review.
