# D5: Gaussian suppression in a pin-compatible parabolic tube

**Object:** D5-THIN-TUBE-20260925-v1. **Author:** OpenAI / ChatGPT, author-side candidate. **Scientific effect:** NONE. Independent analytic review is OPEN. This note supplies a written proof candidate and exact algebra checks, not a review verdict, formal-kernel proof, or global RN closure.

## 1. Exact law, scope, and claim

Fix L>0. Let F be the centered, variance-one Gaussian field on R^2/(L Z^2) with covariance

    K_L(h) = sum_{n in Z^2} exp(-|h+Ln|^2/2)
                         / sum_{n in Z^2} exp(-|Ln|^2/2).

Keep this FULL periodic covariance. It is not replaced by an isotropic Euclidean reference. Let E=(e_1,e_2) be any orthonormal frame and write f(x,z)=F(x e_1+z e_2) in a local chart. Fix compact birth interval I, 0<k_-<=k<=k_+<infinity, 1<A<B<infinity, and 0<K<infinity. All constants below may depend on these fixed quantities and L, but are uniform in b in I, k in [k_-,k_+], and E in O(2).

Put M=(-r/2,0), S=(r/2,0). Q_r is the continuous Gaussian regression law at ALL SIX original pins

    f(M)=b, f(S)=b-k r^3, f_x(M)=f_x(S)=f_z(M)=f_z(S)=0.

For a symmetric 2x2 matrix H, write F_j(H)=|det H| 1{negative index(H)=j}, extended by zero on singular matrices. Set

    W_r=F_2(H_M) F_1(H_S),   Z_r=E_{Q_r} W_r,
    dQ_r^W=(W_r/Z_r) dQ_r.

There is no adjacency/elder conditioning and no observation-density Jacobian inside Z_r. Define the physical tube

    T_r={ (r u)e_1+(r^2 v)e_2 : A<=|u|<=B, |v|<=K }.

Choose r small enough for this to be an embedded local chart, e.g. r sqrt(B^2+K^2)<L/4 and r<=1. It avoids the pinned sites. Let N_j(T_r) count index-j critical points in this tube, at ALL heights; j=0,1,2.

**Candidate theorem.** There are C,c,r_*>0 such that, for 0<r<=r_*,

    p_{grad f(r u,r^2 v) | six pins}(0) <= C r^-5 exp(-c/r^2),       (T1)
    E_{Q_r^W} N_j(T_r) <= C r^-10 exp(-c/r^2).                     (T2)

The same count bound holds for all indices combined, after changing C, and for any further height restriction, including the between-pin height window. Consequently the expected count and the probability of at least one such witness are O(r^N) for every fixed N>0. This is a shrinking-width tube result ONLY. It does not cover the whole x=r y annulus, pin neighborhoods, the regime r<<|x|<<rho, arbitrary shrinking angular bands, multiple-witness collision integrals, unrestricted marks, d>=3, or numerical/all-cell certificates.

## 2. Nonsingular original-pin coordinates and Gaussian control

For an unconditioned field define

    U_r = ( (f(M)+f(S))/2,
            (f(S)-f(M))/r,
            (f_x(S)-f_x(M))/r,
            (12/r^2)[(f_x(S)+f_x(M))/2 - (f(S)-f(M))/r],
            (f_z(M)+f_z(S))/2,
            (f_z(S)-f_z(M))/r ).                              (T3)

This is an invertible linear transform of the six observations at every r>0. Its imposed target is EXACTLY

    v_r=(b-k r^3/2, -k r^2, 0, 12k, 0, 0),                   (T4)

not its r=0 limit. Symmetric Taylor expansion, in L^2 and with derivatives, gives

    U_r = U_0+O_{L^2}(r^2),
    U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz)_0.                        (T5)

All covariance derivatives of the periodic field are bounded at every fixed order. Its Fourier weights are positive at EVERY lattice frequency. For any finite set of distinct derivative monomials at one site, a zero-variance combination would give a polynomial P(E^T n) vanishing for every n in Z^2. A polynomial vanishing on the integer lattice is identically zero (iterate the one-variable fact). Thus these distinct derivatives have positive-definite covariance. Compactness of O(2) supplies a uniform positive eigenvalue floor for Cov(U_0), inherited by Cov(U_r) for small r. No rotational invariance is assumed.

Use the common-field coupling

    m_r(t)=Cov(f(t),U_r) Cov(U_r)^-1 v_r,
    R_r(t)=f(t)-Cov(f(t),U_r) Cov(U_r)^-1 U_r.                 (T6)

The law of m_r+R_r is Q_r; R_r is centered and independent of U_r. Because v_r is uniformly bounded and the observation Gram inverse is bounded, every fixed-order derivative of m_r is uniformly bounded. Derivative variances of R_r are bounded by their unconditioned variances. Therefore their pointwise L^p norms are uniformly bounded for every fixed p<infinity. This suffices for Taylor remainders by their integral formulas and Minkowski; no deterministic bound on a random C^6 norm is silently imposed.

The same coupling yields derivative-level R_r(0)->R_0(0) at rate O_{L^2}(r^2), for every fixed derivative order. R_0 is the centered residual after conditioning on U_0. The residual R_r satisfies the six HOMOGENEOUS finite-r pins identically.

## 3. Derive the homogeneous residual rows before scaling

Write all unlabelled derivatives at the midpoint. For g=R_r restricted to z=0, the two endpoint slope equations and equal endpoint heights give

    g_x = -(r^2/8)g_xxx+O_{L^p}(r^4),
    g_xx = -(r^2/24)g_xxxx+O_{L^p}(r^4),
    g_xxx=O_{L^p}(r^2), hence g_x=O_{L^p}(r^4).             (T7)

For clarity, the height difference divided by r is g_x+(r^2/24)g_xxx+O(r^4)=0; subtract this from the mean slope equation g_x+(r^2/8)g_xxx+O(r^4)=0. Their difference is (r^2/12)g_xxx+O(r^4)=0, proving the third assertion. The odd slope difference divided by r gives the second assertion. Uniform higher derivative moments justify these symmetric remainders.

The transverse zero-gradient pins similarly yield

    R_{r,z}=-(r^2/8)R_{r,xxz}+O_{L^p}(r^4),
    R_{r,xz}=-(r^2/24)R_{r,xxxz}+O_{L^p}(r^4).             (T8)

Taylor first to (r u,0), then to (r u,r^2 v). Uniformly on the declared compact (u,v)-domain,

    R_{r,x}(r u,0)=r^3 a(u)R_{r,xxxx}(0)+O_{L^p}(r^4),
    R_{r,xz}(r u,0)=r u R_{r,xxz}(0)+O_{L^p}(r^2),
    R_{r,z}(r u,0)=r^2 b(u)R_{r,xxz}(0)+O_{L^p}(r^3),
    R_{r,zz}(r u,0)=R_{r,zz}(0)+O_{L^p}(r),                (T9)

where

    a(u)=u(u^2-1/4)/6,   b(u)=(u^2-1/4)/2.

It follows that the centered, normalized gradient

    Y_r=(r^-3 R_{r,x}(r u,r^2 v), r^-2 R_{r,z}(r u,r^2 v))

converges uniformly in L^2 to

    Y_0 = [ a(u)   u v   0 ] [ R_{0,xxxx} ]
          [   0    b(u)  v ] [ R_{0,xxz}  ].              (T10)
                                [ R_{0,zz}   ]

This is a two-dimensional Gaussian residual, not a deterministic contact equation. The r^3 longitudinal scale is essential. The older r^2 scale retains the deterministic drift but loses its first nontrivial random compensation term.

## 4. Genuine covariance rank, not k used as a random coordinate

Let V=(R_{0,xxxx},R_{0,xxz},R_{0,zz}). The nine distinct monomials comprising U_0 and these three derivatives have positive-definite joint covariance by Section 2. Their Schur complement gives

    lambda I <= Cov(V) <= Lambda I                          (T11)

uniformly in E, with constants for the exact periodic model. In (T10), the first two columns have minor

    a(u)b(u)=u(u^2-1/4)^2/12.                               (T12)

This is nonzero on A<=|u|<=B, A>1, independent of v. Continuity on the compact tube-parameter domain implies uniform upper/lower eigenvalue bounds for Cov(Y_0), inherited by Sigma_r=Cov(Y_r) through uniform L^2 convergence. The three derivatives in V are random residual jets; k is fixed and is NOT counted as a covariance direction.

An exact Euclidean covariance calculation in the accompanying code gives Cov(V)=diag(24,2,2) for the NONPERIODIC covariance exp(-|h|^2/2). That is an algebra sanity check only. Neither its numerical values nor Euclidean isotropy are used to establish (T11) for K_L.

## 5. Singular target and the compensation-density estimate

Apply the same finite-r slope/height identities to the bounded deterministic mean m_r, now using the nonzero prescribed height gap. They yield

    m_{r,xxx}(0)=12k+O(r^2),
    m_{r,x}(0)=-(3/2)k r^2+O(r^4),
    m_{r,xx}(0)=-(r^2/24)m_{r,xxxx}(0)+O(r^4).

The transverse identities have the same form as (T8). Hence

    r^-3 m_{r,x}(r u,r^2 v)=6k(u^2-1/4)/r+O(1),
    r^-2 m_{r,z}(r u,r^2 v)=O(1).                          (T13)

Call this vector mu_r. In particular |mu_r|>=c_0/r for small r, uniformly, because k>=k_->0 and u^2-1/4>=A^2-1/4>0; also |mu_r|<=C_0/r. By (T11)-(T12), lambda_* I<=Sigma_r<=Lambda_* I. Under Q_r, grad f has the law diag(r^3,r^2)(mu_r+Y_r). Therefore its density at zero is

    r^-5 (2 pi)^-1 det(Sigma_r)^-1/2
               exp[-(1/2) mu_r^T Sigma_r^-1 mu_r]
      <= C r^-5 exp(-c/r^2).                              (T14)

This proves (T1). Both the finite-r shift -1/4 and the first random residual order were retained. This is not an inference from a scalar density to a joint density: Section 4 establishes the full two-row covariance rank.

## 6. The three Hessians under the rare witness condition

Do not retain the unconditioned W_r=O(r^2) heuristic after additionally conditioning on grad f at the witness. Instead stack the independent entries of H_M,H_S,H_w into a nine-component Gaussian vector H. Under Q_r its mean and covariance are uniformly bounded, by Section 2. The covariance of H with Y_r is uniformly bounded by Cauchy-Schwarz and Section 4. Conditional on grad f(w)=0, equivalently Y_r=-mu_r,

    E[H | Y_r=-mu_r]=E H+Cov(H,Y_r)Sigma_r^-1(-mu_r)=O(r^-1),
    Cov(H | Y_r=-mu_r) <= Cov(H).                          (T15)

The absolute product of the three 2x2 determinants is bounded by C|H|^6. Gaussian moments and (T15) therefore give

    E[ W_r F_j(H_w) | grad f(w)=0, six pins ] <= C r^-6.   (T16)

This deliberately crude polynomial cost is harmless against the exponential penalty. It retains all three determinants in ONE conditional expectation and does not factor endpoint/witness dependence.

## 7. The ORIGINAL full normalizer has a quadratic floor

This is calculated under Q_r with endpoint pins ONLY, not under the additional witness pin. Put A_r=f_zz(0). Its limiting conditional law is a nondegenerate one-dimensional Gaussian, with bounded mean and variance bounded above and below uniformly in the compact marks/frame domain. The identities above imply, in every fixed L^p,

    f_xx(M)=-6kr+O(r^2),       f_xx(S)=6kr+O(r^2),
    f_xz(M),f_xz(S)=O(r),     f_zz(M),f_zz(S)=A_r+O(r).

Consequently

    det H_M/r=-6k A_r+O_{L^p}(r),
    det H_S/r= 6k A_r+O_{L^p}(r).                         (T17)

The Gaussian probability of -2<=A_r<=-1 is bounded below by p_0>0 uniformly for small r. Intersect this with the events where both determinant errors are smaller than 3k_- and f_xx(M)/r<-3k_-; the excluded probability is O(r^p) by the preceding uniform moment bounds. On the intersection, H_M is negative definite (negative longitudinal diagonal and positive determinant), det H_S<0, and both absolute determinants are at least 3k_- r. Thus

    Z_r=E_Q W_r >= c_Z r^2.                              (T18)

This gives the required qualitative floor directly; it does not import the numerical H3 floor or its radius, nor does it make an assertion about its historical certificate.

## 8. Weighted Kac-Rice and the tube count

For each fixed r>0, the tube lies away from M,S. Positive Fourier weights imply nondegenerate finite jets at any collection of distinct sites: a finite distribution consisting of derivative evaluations with all Fourier coefficients zero is the zero distribution, and its coefficients can be isolated with local test functions. Consequently, away from the pins, the conditioned gradient value together with the three independent symmetric-Hessian entries has nonsingular joint law. This is nondegeneracy in the gradient/Hessian jet subspace, not in the larger space of unconstrained vector-field derivatives. Local scalar-polynomial perturbations preserving the endpoint pins make gradient evaluation surjective; Gaussian transversality (equivalently the local Morse criterion) then gives almost surely regular zeros there. Gaussian regression provides the continuous conditional law at grad f=0. The field is smooth, and determinant weights have all finite Gaussian moments at fixed r. These verify the local hypotheses for weighted Kac-Rice.

Precisely, use Stecconi's weighted Kac-Rice Theorem 29 and its nonnegative-weight extension, Section 8.4, in arXiv:2103.10853v1, printed pages 20 and 44. For this application one may take the gradient map on the torus minus the two pinned sites; endpoint Hessians are measurable limits of derivatives of that map. Thus the weight W_r is a measurable functional of the underlying map. Truncation/monotone convergence handles the unbounded nonnegative weight. The same formula can be read as Kac-Rice under the absolutely continuous tilted law, Section 4.4, printed page 23. No Gaussianity of Q_r^W is asserted.

For any Borel subset D of the tube,

    E_{Q_r^W} N_j(D)
      = Z_r^-1 int_D p_{grad f(w)|pins}(0)
              E[W_r F_j(H_w)|grad f(w)=0,pins] dw.         (T19)

Using (T14), (T16), (T18), and area(T_r)=4K(B-A)r^3 gives

    E_{Q_r^W}N_j(T_r) <= C r^-2 * r^3 * r^-5 * r^-6
                                     * exp(-c/r^2)
                           = C r^-10 exp(-c/r^2).

There is NO additional height-window factor here: this proof bounds ALL witness heights. Restricting the count to the between-pin window only reduces it. Since exp(-c/r^2) dominates each fixed inverse power, (T2) implies O(r^N) for every fixed N; Markov gives the corresponding existence-probability upper bound. No probability lower bound is inferred from an expectation.

## 9. Source bindings, limitations, and exact review questions

Project context actually inspected: Math- PR19 head ee8629f37977f4132da4c5af7e1dd61e9d94aa1d (finite-r repair); PR17 e707da6f1451c08a7ca3fcd393ee4f2b4d636dcc (pin falsifier); PR9 cc663ba08cd15d9690e921c7931db6eb07768ac5 (unresolved chart program); base main baca69c394ab42130c61771bee74e808703f1ce7. This note rederives the identities it consumes; it does not accept those PRs or edit them.

The exact polynomial tests verify pin compatibility, contact-row coefficients, covariance algebra for a clearly labelled Euclidean reference, and the power ledger. They do NOT verify uniform Gaussian estimates, the Kac-Rice application, the full theorem, or organizational independence. The author's exposure to earlier OpenAI work is disclosed. No priority claim is made for this argument.

Independent review should attack separately: (R1) six-pin transform and target; (R2) uniform L^p Taylor remainders and centered contact rows; (R3) periodic covariance rank and compactness; (R4) joint Gaussian large-deviation target; (R5) extra-conditioning Hessian cost; (R6) original full-normalizer floor; (R7) marked Kac-Rice and exact physical tube; (R8) excluded regimes. In particular, fixed K in |z|<=Kr^2 CANNOT be replaced by a diverging K(r), and k_->0 cannot be removed by this proof.
