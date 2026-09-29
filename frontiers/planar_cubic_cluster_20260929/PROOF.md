# Exact planar cubic cluster classification and a Gaussian soft-layer coefficient

Object: OA-PLANAR-CUBIC-CLUSTER-20260929-v1.
Author: OpenAI / GPT-6 Astra Pro, foreground continuation session, 29 September 2026.
Disposition: AUTHOR-SIDE CONDITIONAL PROOF CANDIDATE; NONAUTHOR REVIEW OPEN.
Scientific effect: NONE. No parent proof, governing status, Boolean, prize or review disposition is changed. Same GitHub account as other lanes; no organizational-independence credit.

## 1. Scope and exact inputs

This is a planar result, d=2. Fix the exact variance-one periodized Gaussian field on the torus of side L>0, one orthonormal frame, a birth b and a gap mark k>0. Coordinates are (x,z). The pins are

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Q_r is the original Gaussian regression law and W_r=F_2(H_M) F_1(H_S), Z_r=E_Q W_r, dQ_r^W=(W_r/Z_r)dQ_r. In particular Z_r is the FULL normalizer, not one restricted to the event below. All results are for fixed b,k,L and frame. No result uniform as these parameters escape compacts is asserted.

The exact sources at commit 7a1cb09a9d58d179393e6d29146252f714b9c9bf are in SOURCES.json:

- [L] frontiers/window_multiplicity_laws_20260928/LOCAL_MULTIPLICITY.md, equations (L6)-(L13): pinned cubic, its C^2 Taylor remainder, the full ten-dimensional planar jet rank and extra-conditioned C^4 moments.
- [P] imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md, Sections 1-5: exact covariance and law, contact frame, positive Fourier spectrum, smooth Gaussian regression and full normalizer (5.4).

Only these displayed interfaces are consumed; their author-time headers are not being used as a current acceptance register. This note neither revalidates those inputs nor needs the global C6 factorial upper theorem. The results below are new consumers of the pinned Taylor and Gaussian interfaces, not a claimed novelty audit of polynomial critical-point theory.

## 2. Complete deterministic classifier

For real s,a,beta,c and k>0, take exactly [L, (L6)]:

    P(X,Z)=2kX^3-3kX/2-k/2+(s/2)Z^2
           +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(c/6)Z^3.          (C1)

It has the exact values 0,-k and zero gradients at (-1/2,0),(1/2,0). Set

    u=X+aZ/(12k),
    B=beta-a^2/(12k),
    D=(c-a beta/(4k)+a^3/(72k^2))/2.                         (C2)

This determinant-one shear fixes both pins and gives

    P=2ku^3-3ku/2-k/2+(s/2)Z^2+(B/2)uZ^2+(D/3)Z^3.         (C3)

Both Hessian inertia and determinant are preserved under the shear. At the pins the determinants are 3k(B-2s), 3k(B+2s), respectively; the axial entries are -6k,6k. Thus the first pin is a strict maximum and the second a saddle exactly when

    s < -|B|/2.                                            (C4)

Write D_k for this open parameter set in theta=(s,a,beta,c), using (C2). On it put

    T=-(s-B)^2(B+2s)/(12k) >= 0,
    w(theta)=9k^2(4s^2-B^2)>0.                              (C5)

Here w is the positive endpoint determinant product. Let n(theta) count ALL additional critical points of this cubic, anywhere in R^2, with height strictly between -k and 0.

**Theorem C (exact classifier).** Every such critical point is a nondegenerate saddle. There are at most two, and

    if s>B:   n=2 when D^2<T, and n=1 when D^2>=T;
    if s<=B:  n=1 when D^2>T, and n=0 when D^2<=T.           (C6)

These formulas include B=0, D=0, s=B, conic tangencies, and degree-drop cases. Equality is NOT rounded into the open height window. In particular the old witness (s,a,beta,c)=(-3k/2,0,-2k,0) has n=2 and w=45k^4.

### Proof: conic, line, height and inertia

From (C3), stationary points obey

    Q=6k(u^2-1/4)+(B/2)Z^2=0,
    Z(s+Bu+DZ)=0.                                         (C7)

For Z=0 these are precisely the two pins. Every extra point is therefore on the conic Q=0 and the line s+Bu+DZ=0, with Z!=0. At such a point direct substitution gives

    P=-k(u+1/2)+(s/6)Z^2,
    det Hess P=-3k(B+4su).                                 (C8)

For example the Hessian on the line is [[12ku,BZ],[BZ,DZ]], whose determinant reduces using Q=0 to the second identity. The height identity follows also by Euler's identity for the cubic, quadratic and linear homogeneous parts.

First take B!=0. On Q=0,

    Z^2=-12k(u^2-1/4)/B,
    P/k=-(u+1/2)[1+(2s/B)(u-1/2)].                         (C9)

If B>0, extra real points have -1/2<u<1/2. Their heights are strictly negative, and P>-k is equivalent to

    -1/2<u<u_w,       u_w=-1/2-B/(2s).                     (C10)

The endpoint-type condition puts u_w in (-1/2,1/2). If B<0, real extra points have |u|>1/2. The right branch u>1/2 lies below -k. On the left branch the height is negative, and the open window is equivalent to

    u_w<u<-1/2,       -3/2<u_w<-1/2.                       (C11)

On (C10) or (C11), B+4su>0: for B<0 use u<-1/2 and B-2s>0; for B>0, at the largest allowed u=u_w it equals -B-2s>0, and it increases as u decreases because s<0. Equation (C8) therefore proves that every in-window point is a nondegenerate saddle. In particular a conic tangency can never occur inside this window.

On the positive-Z branch of the window conic write

    Z(u)=sqrt(-12k(u^2-1/4)/B),
    g(u)=(-s-Bu)/Z(u).

The line condition is D=g(u) on that branch and -D=g(u) on the negative-Z branch. Differentiation, retaining the conic relation, gives

    g'(u)=det Hess P / (B Z(u)^3).                         (C12)

For B>0, g decreases strictly from +infinity at u=-1/2 to sqrt(T) at u=u_w. Thus there is one extra window point precisely when |D|>sqrt(T). Since s<B here, this is (C6).

For B<0, g increases strictly from sign(B-s)*sqrt(T) at u=u_w to +infinity at u=-1/2. (When s=B the starting value is zero.) The number is the sum of the two strict inequalities

    1{D>g(u_w)} + 1{-D>g(u_w)}.

If s>B, the starting value is negative: both branches contribute below the squared threshold, and only one contributes at or above it. If s<=B, the starting value is nonnegative: precisely one branch contributes strictly above the squared threshold, none at or below. This proves (C6) for B!=0. The endpoint identity g(u_w)^2=T follows from

    Z(u_w)^2=-3k(B+2s)/s^2,
    -s-Bu_w=(B-s)(B+2s)/(2s).

For B=0, Q forces u=+/-1/2. If D=0, s<0 forces Z=0, so there are no extras. Otherwise Z=-s/D and the two extra heights are s^3/(6D^2) and -k+s^3/(6D^2). Only the first can be in the window, precisely when D^2>-s^3/(6k)=T; its determinant is 6ks<0. This proves all B=0 cases.

No root at infinity has been silently counted. For B,D!=0, eliminating Z gives

    (12kD^2+B^3)u^2+2B^2s u+Bs^2-3kD^2=0.                (C13)

If its leading coefficient vanishes, its linear coefficient is nonzero because B!=0 and s<0. It has one finite root, included by the monotone-branch argument. If D=0 and B!=0, the line fixes u=-s/B and Q supplies at most two values of Z. The B=D=0 case was already separated. This also proves the claimed upper bound on the number of extra points. QED.

## 3. Window stability without an unnecessary global Morse hypothesis

The transition set is

    Sigma_k={12kD^2+(s-B)^2(B+2s)=0} inside D_k.             (C14)

It is Lebesgue-null in (s,a,beta,c): after clearing fixed positive k denominators it is a nonzero polynomial (its c^2 coefficient is nonzero). No claim is made that the entire cubic is Morse outside Sigma_k: critical points below the window can be degenerate, and that causes no problem here.

**Lemma S.** For theta in D_k outside Sigma_k, the window count is stable under sufficiently small C^2 perturbations on a sufficiently large fixed disk, provided both pins, their zero gradients and their values 0,-k are retained exactly. On a compact subset of D_k disjoint from Sigma_k, the disk and perturbation size can be chosen uniformly.

**Proof.** Equations (C10)-(C11), and the B=0 case, give |u|<=3/2 for all critical points with heights in [-k,0]. From (C8), P>=-k also gives

    Z^2 <= 12k/|s|.                                       (C15)

A compact subset of D_k has |s| bounded below and a bounded. The inverse shear therefore bounds all these points in one disk. Choose a strictly larger disk. The only critical points at the boundary heights are the pins, unless theta is in Sigma_k. Theorem C makes all critical points inside the window nondegenerate; the two pin Hessians are nondegenerate by (C4).

Choose disjoint small neighborhoods of those finitely many roots. In each, the implicit-function theorem gives one and only one nearby zero for a small C^2 perturbation. The pins stay the same by hypothesis. On the remaining compact set where the height is in a small enlargement of [-k,0], the gradient has a positive minimum; hence no new in-window zero is possible. Points of sufficiently different height cannot enter the window under a small C^0 perturbation. This argument uses no assumption on critical points at lower heights. A finite-cover argument gives uniformity over a compact parameter set avoiding Sigma_k. QED.

For any fixed compact C subset of D_k, choose R_C large enough using (C15) and the shear. For each fixed R>=R_C, Lemma S applies pointwise for almost every theta in C. It is not necessary to assume C avoids Sigma_k for integration below, since that set is null.

## 4. An explicit Gaussian law in every compact soft-jet sector

Return to the exact field. At its midpoint define the physical jet

    J=(A,a,beta,c)=(f_zz,f_xxz,f_xzz,f_zzz),
    Theta_r=(f_zz/r, f_xxz, f_xzz, f_zzz).                  (G1)

The field remains conditioned on the original six endpoint observations. Let h_r(A,a,beta,c) be the density of J under Q_r. The nonsingular contact limit is

    U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz),
    U_0=(b,0,0,12k,0,0),                                 (G2)

and h_0 is the corresponding joint density of J under this contact law Q_0. [L] and [P] give full rank for (U_0,J), hence h_0 is a strictly positive Gaussian density. Their regression argument gives h_r->h_0 locally uniformly.

Let A_0=f_zz under Q_0. The FULL normalizer limit from [P, (5.4)] is

    Z_r/r^2 -> z_0=36k^2 E_Q0[A_0^2 1{A_0<0}]>0.           (G3)

Fix any compact Borel C subset of D_k. For R>=R_C let N_{r,R} count additional critical points in the physical disk of radius Rr, excluding M,S, with heights strictly in (b-kr^3,b).

**Theorem G (compact-sector limit).** As r decreases to zero, the finite measures

    mu_{r,C}(E,j)=r^-3 Q_r^W{Theta_r in E cap C, N_{r,R}=j}

converge in full total variation on C times the nonnegative integers to

    d mu_C(theta,j)
       = 1_C(theta) 1{j=n(theta)}
         [w(theta)/z_0] h_0(0,a,beta,c) ds da d beta dc.    (G4)

The limit is supported on j=0,1,2. In particular, for j in {0,1,2},

    r^-3 Q_r^W{Theta_r in C, N_{r,R}=j} -> Lambda_j(C),
    Lambda_j(C)=z_0^-1 integral_C w h_0(0,a,beta,c) 1{n=j} dtheta. (G5)

The same scaled probability for N_{r,R}>=3 tends to zero within C. If C has positive four-dimensional Lebesgue measure, its limiting total mass is positive, and the law of (Theta_r,N_{r,R}) conditional on Theta_r in C under Q_r^W converges in probability total variation to mu_C/mu_C(C times N_0).

### Proof: retain the rare density before any remainder estimate

Append J to the nonsingular endpoint frame U_r. Its covariance Gamma_r tends to a positive-definite ten-dimensional covariance at r=0: these are exactly all planar jet entries through degree three. Targets (v_r,rs,a,beta,c), theta in C, are bounded. For one unconditioned smooth Gaussian field F, the regression coupling

    f_r^theta = F + Cov(F,V_r) Gamma_r^-1(t_r(theta)-V_r(F)),
    V_r=(U_r,J),    t_r=(v_r,rs,a,beta,c),                  (G6)

has exactly the required conditional law. The coefficient functions converge in C^4 and Gamma_r^-1 stays bounded. The averaged contact functionals are bounded by a fixed multiple of ||F||_{C^3}; [P]'s Fourier summability therefore yields, uniformly for small r and theta in C,

    ||f_r^theta||_{C^4} <= C_C(1+||F||_{C^4})              (G7)

in this coupling, with all fixed moments finite. Internal Gaussian correlations are retained; no independence of a jet and its remainder is assumed.

The pinned Taylor argument [L, (L7)] extends from radius 3 to any fixed radius R simply by changing its Taylor-remainder constant: the endpoint identities are unchanged, and powers of R enter only that constant. Thus

    ||(f_r^theta(rX,rZ)-b)/r^3 - P_theta||_{C^2(B_R)}
        <= C_R r ||f_r^theta||_{C^4} -> 0                 (G8)

pathwise. For almost every theta in C, Lemma S gives N_{r,R}=n(theta) eventually. The endpoint Hessians divided by r converge to those of P_theta. Consequently

    W_r(f_r^theta)/r^4 -> w(theta),
    W_r(f_r^theta)/r^4 <= C_C(1+||F||_{C^4})^4.             (G9)

This is the r^4 soft-sector determinant scale, not the typical r^2 weight scale used in the full normalizer.

The change A=rs in the PHYSICAL four-dimensional jet density has Jacobian r. Disintegration therefore gives the density of mu_{r,C} at (theta,j) as

    1_C(theta) [r^2/Z_r] h_r(rs,a,beta,c)
       E[ (W_r(f_r^theta)/r^4) 1{N_{r,R}=j} ].            (G10)

Indeed r^-3 times r from the jet density times r^4 from W_r divided by Z_r equals r^2/Z_r. This is the ledger r*r^4/r^2=r^3 before the r^-3 rescaling.

For a fixed good theta, the l1 difference over j between the conditional vector inside (G10) and w(theta)delta_{n(theta)} tends to zero. It is bounded by the expectation of |W_r/r^4-w| plus twice the expectation of (W_r/r^4)1{N_{r,R}!=n}; (G7)-(G9) dominate both. On C the Gaussian density h_r is uniformly bounded, and r^2/Z_r is bounded by (G3). Dominated convergence in theta and F proves full l1 convergence of the joint densities, hence (G4). Normalization follows by positive limiting total mass. These limits can equivalently be proved along every sequence r_i->0, avoiding any common-null-set assertion for uncountably many conditional laws. QED.

## 5. Finite nonempty coefficient integrals and actual global lower bounds

Define, only for j=1,2,

    alpha_j=z_0^-1 integral_{D_k} w(theta) h_0(0,a,beta,c)
                                      1{n(theta)=j} dtheta. (G11)

**Theorem F.** Both alpha_1 and alpha_2 are finite and strictly positive. They are explicit integrals, not numerical enclosures. With N_r the GLOBAL window count,

    liminf r^-3 Q_r^W{N_r>=2} >= alpha_2,
    liminf r^-3 E_QrW[N_r(N_r-1)] >= 2 alpha_2,
    liminf r^-3 E_QrW[N_r] >= alpha_1+2 alpha_2.             (G12)

**Proof of finiteness.** Put x=-s>0 and M=|B|. On the nonempty sector, (C6) gives either s>B, which forces x<M, or D^2>T. If x>=2M, then |s-B|>=x/2 and -B-2s>=x, so T>=x^3/(48k). Therefore every nonempty sector satisfies

    0<x<=2|B|+(48kD^2)^(1/3)=H.

Since w<=36k^2 x^2, integration in s gives

    integral w 1{n>=1} ds <=12k^2 H^3
                         <=384k^2 |B|^3+2304k^3 D^2.       (G13)

Both |B|^3 and D^2 are bounded by a fixed-degree polynomial in (a,beta,c), at fixed k. The slice h_0(0,a,beta,c) has Gaussian decay and hence all polynomial moments. This proves finiteness. Positivity follows from open neighborhoods of theta=(-3k/2,0,-2k,0), where n=2, and theta=(-k,0,0,2k), where n=1. The weight and the Gaussian density are strictly positive there.

Take an increasing compact exhaustion C_m of D_k. Theorem G identifies the limits for each fixed C_m and a disk large enough for that compact. Two local points imply at least two global points, and the bounded statistic 1{N_{r,R}=1}+2 1{N_{r,R}=2} is at most N_r. Apply these inequalities, then (G5), and finally monotone convergence as m increases. This proves (G12) without any assertion that the compact exhaustion captures ALL scaled global intensity. QED.

For evaluating (G11), the s integral is one-dimensional polynomial integration over sectors cut by the cubic T(s)=D^2 and the typed endpoint boundary. Its antiderivative is

    integral 9k^2(4s^2-B^2) ds =12k^2 s^3-9k^2 B^2 s.      (G14)

For checks: at D=0 and B<0, the n=2 slice integrates over B<s<B/2 and equals -6k^2 B^3. At B=0 and D!=0, the n=1 slice integrates over -(6kD^2)^(1/3)<s<0 and equals 72k^3 D^2. The outer integration remains over the original (a,beta,c) coordinates; no shear Jacobian in jet space has been silently omitted.

## 6. Exact birth-height factorization of the limiting sector law

**Theorem B.** Fix k,L and frame, and choose C independently of b. The NORMALIZED limit law in Theorem G is independent of birth height b. Likewise the ratio alpha_2/(alpha_1+alpha_2) of the coefficient integrals in (G11) is independent of b. This is not a statement about the full global count conditioned on nonemptiness.

**Proof.** The covariance kernel is even, not necessarily isotropic. At a common site, the covariance between an even-total-order derivative and an odd-total-order derivative is a derivative of odd total order of K at zero, hence vanishes. Gaussianity gives independence of the even and odd jet blocks. In (G2) the even pins are (f,f_xx,f_xz)=(b,0,0), and the odd pins are (f_x,f_xxx,f_z)=(0,12k,0). The appended A=f_zz is even, while (a,beta,c) are odd. Conditioning these independent blocks separately preserves independence. Thus

    h_0(0,a,beta,c)=p_b(0) q_k(a,beta,c),
    z_0=36k^2 m_{2,b},
    m_{2,b}=E[A_0^2 1{A_0<0} | even pins].                (G15)

The Gaussian density q_k depends on k,L,frame, but not b. In (G4) and (G11) the entire b dependence is the common strictly positive scalar p_b(0)/(36k^2 m_{2,b}), which cancels on normalization and in the indicated ratio. This parity separation is claimed at contact in the LIMIT; no finite-r birth independence is asserted.

For an explicit scalar check, if A_0 has mean m_b and variance sigma_A^2 under the even pins, then

    p_b(0)=phi(m_b/sigma_A)/sigma_A,
    m_{2,b}=(m_b^2+sigma_A^2) Phi(-m_b/sigma_A)
                     -m_b sigma_A phi(m_b/sigma_A).        (G16)

Here phi and Phi are the standard normal density and CDF. Equation (G16) follows by expanding (m_b+sigma_A Z)^2 and integrating the standard Gaussian first and second truncated moments by parts. No numerical Gaussian coefficient is asserted. QED.

## 7. Precise remaining gap and review division

The deterministic classification is complete on the typed planar cubic domain. The Gaussian conclusion is complete only within each fixed compact soft-jet sector, with unbounded field remainders controlled AFTER conditioning. The nonempty coefficient integrals are finite and give the global LOWER bounds (G12).

What is NOT proved is that all local/global r^-3 intensity is exhausted by these sectors. In particular one still needs a uniform scaled tail bound for large jets, approach to the typed boundary, and spatial scales outside each fixed Rr disk; remote singleton contributions must also be accounted for before identifying the full global count law. Finiteness of the limiting integrals alone is not that tightness theorem. No uniqueness or support {1,2} theorem for the global C6 intensity follows here, and Theorem B is not a global birth-independence statement. No elder-pairing claim, d>=3 transfer, RN/24-jet/JETMOD closure or formal Lean proof is made.

Nonauthor review requested:
A. (C2)-(C14): exact shear, endpoint signs, height-window classification, saddle types, boundary and degree-drop cases.
B. Lemma S and (G6)-(G10): compact stability, full-field conditional coupling, the rare Jacobian, domination and joint total-variation limit.
C. (G11)-(G16): finite positive integrals, justified lower-bound exhaustion, birth factorization and the global non-claims.

The standard-library checker compares (C6) with a separate exact conic-root calculation at 600 rational points; tests include exact boundaries, linear degeneration, shear identities and the r^3 ledger. Those finite controls do not prove the Gaussian or compactness steps. They are not substitutes for the three analytic review slices.
