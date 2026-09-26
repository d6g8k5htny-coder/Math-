# Angular tails of the typed contact kernel and a conditional full-annulus limit

**Object:** OA-CONTACT-ANGULAR-TAIL-20260925-v1.  
**Author:** OpenAI / ChatGPT.  
**Disposition:** author-side derivations; separate review required. Scientific status unchanged.

## 0. Sources, independence and the boundary of this extension

The source kernel is Math- PR25, exact commit `ad35e46d15c2815c36746442808a1626a9724e8a`, `reviews/collision_mechanism_20260925/NOTE.md`, SHA256 `530dd3efaa965c850ea9e6575f42d3952c3efe6a89b2b5355b6afb4285c9d37e`. Its Gaussian realization as a finite-r count limit remains under review. The statements below concerning the explicitly defined Gaussian integral are proved directly as properties of that integral; interpreting them as asymptotics of actual finite-r critical-point counts consumes PR25's extra regression/Kac-Rice interfaces.

The earlier fixed-transverse *upper bound* in PR16 has now received a recorded nonauthor R1-R5 ACCEPT in PR26, review commit `c360f46bf5d3e4bfbb77be98d5e671b5b834d403`. Reviewer self-identifies as xAI/Grok 4.7 through Cursor. This record does not independently certify PR25's stronger limit, the new angular claims here, an organizationally independent review, or any whole-annulus/global RN claim.

PR22 and PR28 already construct finite-r annulus bounds. This work does NOT duplicate them. Section 6 supplies an explicit composition theorem whose uniform-domination premise can be discharged by PR28 only after that source is separately reviewed. PR28 source: `dedc69e1b786f7ad148e6b66718277f4145c99cd`, `frontiers/rn_annulus_bridge_20260925/PROOF.md`, SHA256 `d55e2c03bb17e7977ff94130cc1ff21e54840cd1e20dc4e41ea9ad52228beb05`.

Throughout, the physical endpoint heights are b and b-k*r^3. Thus k is the coefficient of r^3, not the historical alternative mark 6*ell/r^3.

## 1. The typed cubic integral in a fixed domain

Write D=u^2-1/4 and parameterize the free cubic jet by

    q = 6k(w-2u)/v,
    c = 12k(u^2+1/4-u*w)/v^2,
    d = 6k[-2u^3-(3/2)u-1+2theta+3wD]/v^3,                 (1.1)

where v != 0, k>0 and 0<theta<1. The endpoint maximum and saddle types are equivalent to

    L(theta)=-1-2sqrt(theta) < w < U(theta)=1-2sqrt(1-theta). (1.2)

In particular -3<w<1 and U-L<=4. Let

    P_theta(w)=[4theta-(w+1)^2]
               *[(w-1)^2-4(1-theta)]
               *[(w+1-2theta)^2+4theta(1-theta)].           (1.3)

It is positive on (1.2), a degree-six polynomial, and bounded on the compact closure of this (theta,w) domain. The triple filtered determinant is

    T=(9k^2)^3 |v|^-6 P_theta(w).                           (1.4)

Let g be the actual Gaussian density of (a,q,c,d) conditional on the endpoint contact pins, where a=f_zz(0), with mean mu and positive covariance Sigma. Keep all correlations. Let z0>0 be the full endpoint-only contact normalizer from PR25. Then its proposed leading saddle kernel is the explicit integral

    Lambda(u,v;b,k,frame)
      = 104976 k^8/(z0 |v|^13)
        * integral_0^1 integral_L^U
            g(0,q(w),c(w),d(w)) P_theta(w) dw dtheta.       (1.5)

Indeed 104976=24*6*9^3: the original factor 24k/|v|^6, dq=6k/|v| dw, and the determinant product (1.4). This ledger will be tested independently. The limiting maximum and minimum kernels from the cubic model are zero, as in PR25.

This representation has a FIXED integration domain independent of u,v,b,k. It is the useful starting point for angular estimates and differentiation; no limit-dependent jet interval has been hidden.

## 2. Gaussian damping beats the apparent axial singularity

Fix 1/2<a<=|u|<=B, 0<|v|<=v0<=1, compact b and k in [k_-,k_+] with k_->0, and all orthonormal frames of the exact periodic model at fixed L. Positive contact covariance and compactness imply uniform eigenvalue bounds, bounded mean, and

    g(0,q,c,d) <= C_g exp[-c_g(q^2+c^2+d^2)].              (2.1)

The corrected first-gradient equation is

    u*v*q+(v^2/2)c=-6kD.

By Cauchy-Schwarz,

    q^2+c^2 >= 36k^2 D^2/[v^2(u^2+v^2/4)]
              >= C_*/v^2,  C_*>0.                        (2.2)

Thus (1.5), the bounded type domain and (2.1) give

    0<Lambda(u,v)<=C |v|^-13 exp(-gamma/v^2).              (2.3)

All constants are uniform on the stated compact sets. They may diverge as k_->0 or a->1/2. On any fixed scaled annulus A<=sqrt(u^2+v^2)<=B, A>1, choose a<A and a sufficiently thin fixed strip so that |u|>=a there.

### Consequences at the level of the contact kernel

1. Lambda extends continuously by zero at v=0 in that strip. It is not singular there despite the bare |v|^-13 prefactor.
2. Every algebraic angular moment is finite: integral |v|^-p Lambda du dv < infinity for every fixed finite p on the bounded strip.
3. The omitted axial strip has superalgebraically small coefficient mass: for every N>0,

       integral_{|v|<eta} Lambda du dv <= C_N eta^N.       (2.4)

For example, use a sufficiently high positive term in exp(gamma/v^2) to dominate any inverse power. These conclusions are for the LIMITING kernel. They do not establish uniform integrability of finite-r densities; a moving concentration at v comparable to r remains a separate question.

### Stronger one-sided bound

For u>1/2, theta<=1 and w<=1 imply

    d v^3/(6k) <= -2u^3+3u^2-(3/2)u+1/4
                 = -2(u-1/2)^3.

Therefore

    |d| >= 12k(u-1/2)^3/|v|^3,                            (2.5)
    Lambda <= C |v|^-13 exp(-gamma_+/|v|^6)               (2.6)

uniformly when u>=a>1/2. This is a directional asymmetry created by the ordered maximum/saddle pins. A symmetric-looking bare chart Jacobian would not reveal it.

## 3. Exact elimination of the free-jet integral

For fixed theta, write x(w)=(0,q(w),c(w),d(w))=x0+w*x1. Put Q=Sigma^-1 and

    s=x1^T Q x1 >0,
    m=-x1^T Q(x0-mu)/s,
    h=(x0-mu)^T Q(x0-mu)-s*m^2 >=0.

Then

    g(x(w))=(2pi)^-2(det Sigma)^-1/2
               * exp(-h/2) exp[-s(w-m)^2/2].              (3.1)

Let P_theta(w)=sum_{j=0}^6 p_j(theta) w^j. The inner integral in (1.5) is expressible exactly, in real arithmetic, using only seven truncated Gaussian moments. Set l=sqrt(s)(L-m), h1=sqrt(s)(U-m) and

    I_j(l,h1)=integral_l^h1 t^j exp(-t^2/2)dt.

The recurrence is

    I_0=sqrt(2pi)[Phi(h1)-Phi(l)],
    I_1=exp(-l^2/2)-exp(-h1^2/2),
    I_j=(j-1)I_{j-2}+l^(j-1)exp(-l^2/2)-h1^(j-1)exp(-h1^2/2).

Consequently

    integral_L^U P_theta(w) exp[-s(w-m)^2/2]dw
      = sum_j p_j sum_{i=0}^j binom(j,i)m^(j-i)s^(-(i+1)/2) I_i. (3.2)

After this exact elimination, only the compact theta integral remains. The formulas retain the full periodic covariance and are not restricted to independent jets. The accompanying floating-point helper tests (3.2) on moderate arguments, but it is NOT an interval enclosure; extreme tails need scaled/survival-function arithmetic to avoid cancellation. No certified SIDE24 coefficient is claimed.

## 4. A sharp left-side angular asymptotic in the unperiodized model

This section assumes ONLY the unperiodized covariance exp(-|h|^2/2). Then

    (a,q,c,d)|U0 ~ N((-b,0,0,0),diag(2,2,2,6)),
    g(0,q,c,d)=(16 pi^2 sqrt(3))^-1
                  exp[-b^2/4-q^2/4-c^2/4-d^2/12].          (4.1)

This covariance is not substituted for the exact finite-L model.

Fix -3/2<u<-1 and k>0. Define

    D=u^2-1/4,
    Q0=-6kD/u,
    w0=u+1/(4u),
    theta0=-(2u-3)(2u+1)^3/(32u).                         (4.2)

Then 0<theta0<1 and w0 lies strictly inside the typed interval at theta0. For an explicit sign proof,

    1-theta0=(2u-1)^3(2u+3)/(32u),
    F1=-(2u-1)^2(2u+1)^3/(16u^2),
    F2=-(2u-1)^3(2u+1)^2/(16u^2),
    F3=(2u-1)^3(2u+1)^3/(32u^2).

All three F factors are positive on -3/2<u<-1, as are theta0 and 1-theta0. The special point c=d=0 has q=Q0/v. Its scaled triple determinant is

    T0=5832 k^6 D^8/u^6 >0.                               (4.3)

The change from (q,theta) to the now-free variables (c,d) is exactly

    q=Q0/v-cv/(2u),
    w=w0-cv^2/(12ku),
    theta=theta0+cD v^2/(8ku)+d v^3/(12k),
    |det d(q,theta)/d(c,d)|=|v|^4/(24k|u|).               (4.4)

Let K_v=1+v^2/(4u^2), and let independent variables C_v,D_v have laws

    C_v ~ N(Q0/(2u K_v),2/K_v),   D_v ~ N(0,6).

Define Tbar_v(C_v,D_v)=(9k^2)^3 P_theta(w) when (theta,w) lies in the type domain, and zero otherwise, using (4.4). Completing the Gaussian square yields the EXACT expression

    Lambda(u,v)=|v|^-8 exp[-Q0^2/(4v^2)]
        * exp[-b^2/4+Q0^2/(16u^2 K_v)]
          /(4pi z0 |u| sqrt(K_v)) * E[Tbar_v].              (4.5)

For every fixed (c,d), the type indicator tends to one, and Tbar_v->T0. The transformed integrands admit a fixed polynomial-times-Gaussian envelope, because K_v>=1, the means stay bounded and theta,w are affine in c,d with bounded coefficients. Dominated convergence gives

    Lambda(u,v) ~ A_-(u,b,k)|v|^-8 exp[-I_-(u,k)/v^2],     (4.6)

where

    I_-(u,k)=9k^2(u^2-1/4)^2/u^2,
    A_-(u,b,k)=1458 k^6 (u^2-1/4)^8/(pi z0 |u|^7)
                 *exp[-b^2/4+9k^2(u^2-1/4)^2/(4u^4)].     (4.7)

This is a theorem about the specified contact integral, not a simultaneous finite-r/thin-belt theorem. Compact subintervals of (-3/2,-1) permit uniform convergence; endpoints require separate boundary analysis. The proof deliberately does not classify all negative u.

### 4.1 Actual periodic covariance: an exact marginal formula and sharp log rate

The BF diagonal covariance is not needed to obtain a sharp logarithmic rate. Let g be ANY fixed nondegenerate Gaussian contact density in (a,q,c,d), including the exact finite-L periodic density. Keep the same u interval and the exact coordinate transformation (4.4), and put

    V_v=q+(v/(2u))*c.

Let p_(a,V_v) be the actual joint Gaussian marginal density, and condition (c,d) on a=0,V_v=Q0/v. The coordinate change has unit determinant in the q coordinate. Therefore the EXACT identity is

    Lambda=|v|^-8/(z0|u|) * p_(a,V_v)(0,Q0/v)
                 * E[Tbar_v(c,d)|a=0,V_v=Q0/v].             (4.8)

The conditional covariance of (c,d) stays bounded, and its conditional mean is O(1/|v|). Hence v^2*c and v^3*d tend to zero in probability; (w,theta) tends to the strict interior point(w0,theta0). The typed polynomial Tbar is bounded on its fixed type domain and zero elsewhere. Bounded convergence in probability thus gives its conditional expectation tending to T0, uniformly on compact parameter sets. In particular

    Lambda ~ T0 |v|^-8/(z0|u|) * p_(a,V_v)(0,Q0/v).         (4.9)

Write sigma_q|a^2=Var(q|a)>0 under the endpoint contact law. Gaussian density evaluation gives

    lim_{v->0} v^2 log Lambda = -Q0^2/(2 sigma_q|a^2)
      = -18 k^2 D^2/(u^2 sigma_q|a^2).                    (4.10)

This applies to the actual correlated periodic contact kernel. At fixed L the covariance depends on the frame but not on the witness position v. Uniformity holds on compact u/mark/frame sets with positive conditional variance floor. Formula (4.9), not the BF amplitude (4.7), is the correct full-covariance prefactor statement: variation of Var(V_v|a) and its mean can generate subleading exponential terms. Dropping correlations can therefore change the answer even though the v^-2 scale survives.

For explicit computation, if Sigma is the covariance and mu the mean in coordinate order(a,q,c,d), set t=v/(2u). Then

    m_v=mu_q+t mu_c-(Sigma_aq+t Sigma_ac)*mu_a/Sigma_aa,
    s_v^2=Sigma_qq+2t Sigma_qc+t^2 Sigma_cc
             -(Sigma_aq+t Sigma_ac)^2/Sigma_aa,

and p_(a,V_v)(0,Q0/v) is the product of the marginal N(mu_a,Sigma_aa) density at0 and N(m_v,s_v^2) density atQ0/v. The exact-rational helpers retain the Schur term and test it on a correlated positive covariance as well as on the BF diagonal case.

## 5. A different sharp logarithmic rate on the right side

Still in the unperiodized model, fix u>1/2 and k>0. Equation (2.5) and the d^2/12 Gaussian cost imply

    limsup_{v->0}|v|^6 log Lambda(u,v)
        <= -12k^2(u-1/2)^6.

The least possible magnitude of d*v^3 is approached at theta->1 and w->1, on the closure of the type domain. To prove the matching lower bound, choose a FIXED small interior neighborhood near that corner where P_theta(w)>0 and the cubic numerator is within epsilon of its corner value. On that neighborhood the q and c costs are respectively O(v^-2) and O(v^-4); after multiplication by |v|^6 they vanish. The d cost approaches the displayed constant as epsilon->0. Polynomial factors and the fixed neighborhood area do not affect the logarithmic rate. Hence

    lim_{v->0}|v|^6 log Lambda(u,v)
        = -12k^2(u-1/2)^6.                               (5.1)

Compare this to (4.6): on a left-side interval the kernel decays like exp(-I_-/v^2), while on the right it decays on the much faster exp(-I_+/v^6) scale. This is not a claim that the ordered endpoint-conditioned model is reflection symmetric. Swapping maximum/saddle roles changes the conditioning problem.

Only the logarithmic right-side rate is proved here; no right-side prefactor is asserted. Neither sharp statement is uniform as k approaches zero.

### 5.1 Actual periodic covariance: the right-side rate is a conditional-variance invariant

For the general Gaussian contact density, let

    sigma_d|a,q,c^2=Var(d|a,q,c)>0.

On the compact typed(theta,w) domain, the q,c,d coordinates scale respectively as v^-1,v^-2,v^-3. Thus multiplying the full Gaussian quadratic exponent by |v|^6 kills every term except the d^2 term, uniformly over this domain. The precision entry Q_dd is1/sigma_d|a,q,c^2. The extremal numerator from (2.5) is approached at(theta,w)=(1,1), while positive typed neighborhoods approach it from the interior. The same upper/lower argument as in Section5 yields

    lim_{v->0}|v|^6 log Lambda
       = -72 k^2(u-1/2)^6/sigma_d|a,q,c^2.                 (5.2)

For BF this conditional variance is6, reproducing (5.1). For the exact periodic model the formula keeps its actual conditional variance. The v^-2 left and v^-6 right logarithmic scales therefore are not artifacts of replacing the field by unperiodized BF. The explicit elementary amplitude (4.7) IS specific to BF. No simultaneous finite-r limit or k->0 uniformity follows from this contact-integral analysis.

## 6. Conditional composition: from local chart limits to an entire fixed annulus

Let K_AB={A<=sqrt(u^2+v^2)<=B}, 1<A<B<infinity. Let n_{r,j}(y) be the density, with respect to scaled area dy, of

    r^-3 E_Qr^W N_j(r dy; b-kr^3<f<b).

Assume two source-bound interfaces:

(P) The PR25 fixed-transverse limit holds uniformly on every compact subset with |v|>=eta>0: n_{r,j}->Lambda_j.

(D) A finite-r uniform domination n_{r,j}(y)<=C holds on the whole annulus and compact marks, for all small r. PR28's candidate physical-area all-height bound rho_j^W(ry)<=Cr would imply (D) for the height-restricted population. PR28 is not accepted merely by being named here.

Then

    integral_K |n_{r,j}-Lambda_j|dy ->0,                    (6.1)

and therefore

    sup_{E Borel subset K}
       |r^-3 E N_j(rE)-integral_E Lambda_j dy| ->0.        (6.2)

Proof: convergence holds almost everywhere because the axis has zero area. Domination gives Lambda_j<=C almost everywhere and permits dominated convergence. Uniformity over the compact mark/frame set follows either by uniform convergence off a fixed strip and a bound4B*C*eta for each of the two strip contributions, or a compact-subsequence argument. Thus the total variation bound is uniform, but it is not automatically o(1)*area(E) uniformly over arbitrarily small sets touching the axis.

Since PR25's Lambda_1 is positive off axis and Lambda_0=Lambda_2=0,

    E N_1(rK)=C_K r^3+o(r^3), 0<C_K<infinity,
    E[N_0(rK)+N_2(rK)]=o(r^3),                             (6.3)

CONDITIONALLY on (P) and (D). The coefficient tail can be truncated near v=0 with the superalgebraic estimate (2.4). That coefficient-tail estimate alone does NOT replace (D).

Counterexample to silently swapping limits: n_r(v)=r^-1 1{|v|<r} tends to zero at every fixed v!=0 but has integral2. Pointwise/contact limits cannot exclude a moving mass concentration. This is exactly the role of the separate finite-r domination work in PR22/PR28.

## 7. Reproducibility, interpretation and next review

The code contains 26 distinct test methods: exact rational original-pin/third-point/Hessian/coordinate identities and scope checks, plus explicitly floating-point Gaussian-integral diagnostics. Nine deliberately incorrect implementations are run separately in normal and optimized modes. Test-first RED is retained. Tests are not independent proof verification.

The optional numerical diagnostic evaluates (4.5) on a 9-standard-deviation square with Simpson grids80,160,320. It factors out the exponentially small term, avoiding underflow. It is unperiodized, truncated and not certified. For b=0,k=1,u=-5/4, I_-=3969/400 and A_- is approximately116.47037548. The normalized kernel should tend to this amplitude; agreement at multiple grids does not establish a rigorous quadrature enclosure.

Prior-method attribution: Gaussian regression and marked Kac-Rice (Armentano–Azais–Leon, arXiv:2304.07424v3); multi-point interpolation and determinant renormalization (Gass–Stecconi, arXiv:2305.17586); shrinking-window critical-point estimates (Muirhead, arXiv:1901.11336). These sources supply methodology, not this particular typed-kernel identity or angular asymptotic. No worldwide novelty claim is made.

Review split: independent algebra/Gaussian-integral review for Sections1,3–5; independent analyst for uniform contact envelope and the precise conditional composition in Sections2,6; PR25 reviewer checks the imported realization as a Gaussian count limit. Prior PR26 ACCEPT applies to the older upper bound only. No full elder-rule, persistence lifetime, growing-annulus, pin/witness-collision, small-k, dimension-three or numerical24-jet closure follows here.

### Preserved failed local validation

The first full mutation replay (22-test version) stopped because our `reverse_max_type` mutant made a diagnostic test take log(0) after a zero type weight, alongside its intended assertion failures. This was a defect in the review harness, not a mathematical counterexample. A strict-positive type-weight assertion was added before the logarithm; the mutant is now rejected by assertions only. The failed report/logs are retained separately. The later correlated-Gaussian extension has its own test-first RED record. No validation failure is relabelled as a baseline success.
