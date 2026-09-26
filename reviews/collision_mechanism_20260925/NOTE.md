# Critical-simplex suppression, a typed cubic contact kernel, and marked lifetime transfer

**Object:** OA-SIMPLEX-CONTACT-TRANSFER-20260925-v1. **Author:** OpenAI / ChatGPT.
**Disposition:** author-side derivations for separate review. No independent acceptance, global RN closure, or scientific-status promotion.

This develops the two mechanisms explicitly requested by Dylan: three-critical-point Hessian suppression and a precise version of the collision-to-lifetime exponent principle. It does not edit Cursor PR9/PR14 or the existing PR16 proof. Parent fixed-transverse candidate: Math PR16, source32b80ee085dc6a40113d1e46e333cda50d57ba21, TRANSVERSE_BOUND_CANDIDATE.md SHA256f64c954245f17bcbc64a5ccf58a60689cf2a2fd85362f8321c0f64ff66584e36.

## A. Quantitative geometry, not mere noncollinearity

Let f be C^{2,1} on a convex neighborhood K and let its Hessian satisfy

    ||H(x)-H(y)|| <= L||x-y||.

For x0,...,xk, 1<=k<=d, put ei=xi-x0, E=[e1 ... ek], V=range(E), and assume E has full column rank. Let G have columns grad f(xi)-grad f(x0). Taylor's integral formula gives

    H(x0)E=G-R,   ||R||_F <= (L/2)(sum_i||ei||^4)^(1/2).

Since EE^+=P_V,

    ||H(x0)P_V|| <= [||G||_F+(L/2)(sum_i||ei||^4)^(1/2)]/sigma_min(E). (A1)

Transporting to xj adds L||xj-x0||. In particular, for xi=x0+r vi, zero gradients and sigma_min([vi])>=sigma_*>0,

    ||H(xj)P_V|| <= Lr[(sum_i||vi||^4)^(1/2)/(2sigma_*)+||vj||].       (A2)

This proves the desired O(r) full-Hessian bound for a uniformly shaped planar triangle. In dimension d it takes d+1 affinely independent, uniformly shaped critical points to force the full norm small. With only k independent displacement directions, k singular values are small; if the other singular values are bounded by K2,

    |det H(xj)| <= delta_j^k K2^(d-k),  delta_j=||H(xj)P_V||.        (A3)

Three noncollinear points in dimension three do not force the third direction small: adding z^2/2 in that direction is a counterexample.

For approximately critical points ||grad f(xi)||<=epsilon, add 2sqrt(k)*epsilon/(r*sigma_*) to (A2). Thus an O(r^2) gradient tolerance is required to retain an O(r) Hessian estimate; fixed numerical tolerance is not scale-uniform.

### Explicit planar chart constant

For M=(-r/2,0), S=(r/2,0), X=(ru,rv), |(u,v)|<=B and |v|>=eta, put D=B+1/2,

    C0=(1/2)[1+(D^2+D)/eta],  CH=C0+D.

Then ||H_M||<=C0 Lr, ||H_S||<=(C0+1)Lr, ||H_X||<=CH Lr, and

    |det H_M det H_S det H_X| <= CH^6 L^6 r^6.                      (A4)

Proof: the two endpoints give ||H_M e_x||<=Lr/2. The M-to-X Taylor identity bounds H_M(u+1/2,v) by (Lr/2)[(u+1/2)^2+v^2]. Subtract its longitudinal component and divide by v to bound the second column. Transport the Hessian to the other two points. No probability or independence assumption enters.

### Sharpness and a necessary qualification

The cubic f_r=x^3/3-rx^2/2+z^3/3-rz^2/2 has critical points (0,0),(r,0),(0,r) and Hessians diag(-r,-r),diag(r,-r),diag(-r,r). Its triple determinant magnitude is exactly r^6. The power cannot improve under these assumptions alone.

Conversely f_r=(z-x^2)^2/2+x^4/4-rx^3+r^2x^2 has three noncollinear critical points (0,0),(r,r^2),(2r,4r^2), uniformly bounded third derivatives on a common compact set, but f_zz=1. Its scaled triangle flattens. Thus noncollinearity at each r, without a uniform shape bound, does NOT imply full-Hessian O(r).

## B. A stronger exact result: the intermediate cubic witness is a saddle

Every polynomial of total degree at most three satisfying the six pins at (-1/2,0),(1/2,0), with heights0,-k and zero gradients, k>0, is

    P(s,t)=-k/2+2ks^3-(3k/2)s+(A/2)t^2
             +(q/2)(s^2-1/4)t+(c/2)st^2+(d/6)t^3.                 (B1)

The -1/4 and midpoint terms follow from solving the original pins before blow-up. Let X=(u,v), v!=0, be a third critical point with P(X)=-k*theta, 0<theta<1. Put D=u^2-1/4, Lc=2u^3-3u/2-1/2. Solving the third-point gradient and height conditions leaves one free jet q:

    c=-12kD/v^2-2qu/v,
    d=12k(Lc+theta)/v^3+3qD/v^2,
    A=(12ku+6k+qv-12k*theta)/(2v^2).                              (B2)

The three Hessians are

    B_M=[[-6k,-q/2],[-q/2,A-c/2]],
    B_S=[[6k,q/2],[q/2,A+c/2]],
    B_X=[[12ku+qv,qu+cv],[qu+cv,A+cu+dv]].                       (B3)

With w=(qv+12ku)/(6k), exact expansion gives

    det B_M=(9k^2/v^2)[4theta-(w+1)^2],
    det B_S=(9k^2/v^2)[4(1-theta)-(w-1)^2],
    det B_X=-(9k^2/v^2)[(w+1-2theta)^2+4theta(1-theta)]<0.     (B4)

This is an exact cubic theorem, not just power counting. An intermediate-height noncollinear third critical point must be a nondegenerate saddle in this contact model. For a general smooth field it is a leading-contact conclusion, not an assertion that finite-r extrema are impossible.

The desired endpoint types are feasible. Set w=-1: det B_M=36k^2 theta/v^2>0 and det B_S=det B_X=-36k^2 theta/v^2<0, with (B_M)11<0. For u=2,v=1,k=1,theta=1/2 one obtains q=-30,A=-3,c=75,d=-363/2 and determinant values18,-18,-18. All three gradients vanish and the witness height is exactly-1/2.

Moreover M is a maximum and S a saddle precisely on the bounded interval

    -1-2sqrt(theta)<w<1-2sqrt(1-theta).                         (B5)

This gives an explicit finite integration domain for the typed contact coefficient.

## C. Proposed Gaussian refinement: positive saddle kernel, zero leading extrema kernel

Use the exact variance-one L-periodized covariance sum_n exp(-|z+Ln|^2/2)/sum_n exp(-|Ln|^2/2) in dimension two. Fix compact birth/gap ranges with k bounded above and away from zero, all orthonormal frames, and a fixed nonempty chart

    K={(u,v):1<A0<=sqrt(u^2+v^2)<=B<infinity, |v|>=eta>0}.

Let Q_r be regression on f(M)=b,f(S)=b-kr^3 and both gradients zero. Define F_j(H)=|det H| times its index-j indicator, zero on singular matrices,

    W_r=F_2(H_M)F_1(H_S), Z_r=E_Qr W_r, dQ_r^W=(W_r/Z_r)dQ_r.

There is no actual-pair adjacency condition and no extra pin Jacobian in Z_r. N_j(rE) counts index-j critical points in rE with heights between the pins.

**Author-side refined theorem:** for all Borel E subset K,

    E_Qr^W N_j(rE)=r^3 integral_E Lambda_j(u,v;b,k,frame)du dv
                      +o(r^3)*area(E),                         (C1)

with uniform remainder on the compact parameters. The kernels satisfy

    Lambda_0=Lambda_2=0,  Lambda_1>0.                            (C2)

Thus the saddle mean is genuinely of cubic order on positive-area chart sets, while maxima/minima are lower order. This does not imply an elder-defect lower bound or a matching probability lower bound.

### C1. Full endpoint normalization

Use the exact six-dimensional centered pin transform from PR16, with target
(b-kr^3/2,-kr^2,0,12k,0,0) and limit

    U0=(f,fx,fxx,fxxx,fz,fxz)_0=(b,0,0,12k,0,0).

Positive Fourier variances at every lattice mode imply positive covariance for independent finite derivative functionals. Rapid Fourier decay gives all fixed derivative-supremum moments. Symmetric Taylor convergence and Gaussian regression therefore give bounded covariance inverses, bounded conditional moments and convergence uniformly on the compact marks/frames.

For a=fzz(0) under the endpoint contact law,

    Z_r/r^2 -> z0=36k^2 E[a^2 1{a<0}|U0]>0.                    (C3)

Indeed endpoint axial Hessian entries divided by r tend to -6k and6k, mixed entries are O(r), and transverse entries tend to a. Types stabilize off a=0; a has a nondegenerate Gaussian law and uniform integrability handles the limit. Compactness gives a positive uniform lower bound for z0. This is the full endpoint-only denominator.

### C2. The correct joint witness vector

Set

    J_r=(fx(X)/r^2, fz(X)/r, [f(X)-b-(rv/2)fz(X)]/r^3).

Under Q_r its limit is

    J0=(6kD+quv+cv^2/2, av, kLc+qDv/4-dv^3/12).               (C4)

Here (a,q,c,d)=(fzz,fxxz,fxzz,fzzz)_0 are four unpinned random jets. Their conditional covariance given U0 is positive. The minor of J0 on columns(a,c,d) is v^6/24, uniformly nonzero off axis. Hence the J_r covariance stays uniformly positive. The exact physical-gradient/height to J_r Jacobian is r^-6, and at height b-kr^3 theta the target is(0,0,-k theta).

### C3. Extra conditioning and scaled Hessian convergence

The Gaussian regression coupling after J_r=(0,0,-k theta) has uniformly bounded C^m moments because the targets and inverse J_r covariances are bounded. This checks derivative moments AFTER the witness constraints. Formula(A4) then bounds the full triple determinant expectation by Cr^6.

The same coupling converges in Lp(C^m) to its contact version. The witness-gradient constraint gives a_r/r -> A in(B2), whereas the unscaled limiting a is zero. These are different limits. Taylor expansion then gives (H_M/r,H_S/r,H_X/r)->(B_M,B_S,B_X). Filtered determinants are continuous through singular matrices and have polynomial growth. Uniform derivative moments imply uniform integrability, proving convergence of the triple determinant product divided by r^6. All statements are uniform on the declared compact chart, marks and theta.

### C4. Explicit one-free-jet integral

Let g(a,q,c,d) be the four-dimensional conditional Gaussian density given U0, retaining its actual periodic covariance and correlations. Define T_j=F_2(B_M)F_1(B_S)F_j(B_X). Then

    Lambda_j=24k/(z0 |v|^6) integral_0^1 integral_R
                 g(0,q,c(q),d(q)) T_j(q;u,v,k,theta) dq dtheta. (C5)

The factor24/|v|^6 is the contact transformation determinant. The matrices use the scaled a_r/r limit A(q), not the unscaled density coordinate a=0. Gaussian decay and polynomial growth justify finiteness/continuity. Alternatively (B5) gives a finite w-interval with dq=(6k/|v|)dw; theta=sin^2(phi) smooths its square-root endpoints for quadrature.

By(B4), T_0=T_2=0. Near theta=1/2,w=-1, T_1 is positive, and g is positive. Thus Lambda_1>0, uniformly away from zero on fixed compact parameter sets.

Finally marked Kac-Rice and height disintegration give

    E_Qr^W N_j(rE)=[k r^5/Z_r] integral_E integral_0^1
       p_(J_r|pins)(0,0,-k theta)
       E[W_r F_j(H_X)/r^6|pins,J_r=(0,0,-k theta)] dtheta du dv.

Together with(C3) this proves(C1) under the detailed regression/regularity argument above. This use of marked Kac-Rice needs separate analytic review, not just the finite algebra tests.

### C5. Boundaries

No eta->0, shrinking positive-gap cutoff, axial/thin-belt, intermediate-scale, witness/pin collision, d3, numerical enclosure or historical24jet closure is claimed. Counted saddles are not automatically elder-failure witnesses. For the unperiodized Bargmann-Fock field alone, exact Gaussian jet regression gives mean(-b,0,0,0), covariance diag(2,2,2,6) for(a,q,c,d)|U0. That diagnostic is not substituted for finite-L covariance.

## D. Marked collision-to-lifetime transfer theorem

Let (Z,lambda) be sigma-finite and let the candidate-pair intensity be r^alpha a(r,z)dr dlambda, 0<r<r0, alpha>-1. Let p(r,z) in[0,1] be the actual-pair selection factor and b(r,z)=a(r,z)p(r,z). Set beta=(alpha+1)/m>0. Assume:

1. b(r,z)->b0(z), 0<=b(r,z)<=G(z).
2. kappa(z)>0 and integral G(z)kappa(z)^(-beta)dlambda<infinity.
3. h(r,z) is strictly increasing C1 with h(0+,z)=0,
   h/(kappa r^m)->1 and h_r/(m kappa r^(m-1))->1.
4. Uniformly c0 kappa r^m<=h<=C0 kappa r^m and h_r>=c1 kappa r^(m-1), with positive fixed constants.

Then the local pushforward density obeys

    nu_local(ell)/ell^(beta-1) ->
        (1/m) integral b0(z)kappa(z)^(-beta)dlambda(z).       (D1)

The coefficient must be positive to conclude a positive asymptotic law.

Proof. Invert ell=h(r,z) to r=R(ell,z). Change of variables gives nu_local=integral R^alpha b(R,z)/h_r(R,z) dlambda, with integrand zero when no inverse lies below r0. The normalized integrand tends pointwise to b0 kappa^-beta/m. Uniform h and h_r bounds dominate it by a constant times G kappa^-beta. Dominated convergence proves(D1).

Without the derivative hypotheses, the cumulative theorem still holds under monotonicity and the same comparison/envelope assumptions:

    N_local(ell) ~ ell^beta/(alpha+1) * integral b0 kappa^-beta dlambda. (D2)

Proof: integrate r^alpha b from0 to min(r0,R), use its pointwise limit b0 R^(alpha+1)/(alpha+1), and the same integrable domination. One may not differentiate(D2) without additional control.

### D1. Counterexample: cubic splitting need not give a density coefficient

Take alpha=1, m=3, a=p=kappa=1 and h(r)=r^3[1+r sin(1/r)], 0<r<1/4. Then h~r^3, h'>0, and

    nu(h(r)) h(r)^(1/3)
       =[1+r sin(1/r)]^(1/3)/[3-cos(1/r)+4r sin(1/r)].

Along r=1/(2pi n) this is1/2; along r=1/((2n+1)pi) it is1/4. No density coefficient exists, although the cumulative law is ell^(2/3)/2. Thus ell~kappa r^m alone is insufficient.

### D2. Exact small-kappa phase diagram

For dmu=r^alpha kappa^q dr dkappa on(0,1)^2, alpha,q>-1 and ell=kappa r^m, exact integration gives

    nu(ell)=ell^(beta-1)/m * integral_ell^1 kappa^(q-beta)dkappa.

With delta=q+1-beta this is ell^(beta-1)(1-ell^delta)/(m delta) if delta!=0, and ell^(beta-1)log(1/ell)/m if delta=0. Therefore:

- q+1>beta: exponent beta-1;
- q+1=beta: exponent beta-1 plus log(1/ell);
- q+1<beta: exponent q, dominated by small marks.

For alpha=1,m=3, the transition is q=-1/3. Taking q=-1/2 gives exactly2[ell^-1/2-ell^-1/3], not the proposed universal ell^-1/3. This phase diagram is proved for this product-intensity model; arbitrary dependent models require their own hypotheses.

### D3. Selection, strata and normalization

If p~r^gamma p0, replace alpha by alpha+gamma; the exponent is(alpha+gamma+1)/m-1. A positive pairing limit preserves the exponent, while vanishing pairing can change it. The transverse saddle-count theorem is only one ingredient of a potential all-failure selection bound.

For an exact lifetime map and compact marks, a radial amplitude error O(r^delta) produces a density error O(ell^(beta-1+delta/m)). Unbounded marks require stronger negative moments and cutoff-tail estimates. In the cubic alpha=1 case, first-order amplitude error gives a bounded absolute density error on compact marks, not automatically on all marks.

For a finite collection of positive collision strata the smallest beta dominates; equal exponents add. A bounded nonlocal density is negligible only when beta<1. A full persistence theorem must separately bound all nonlocal/other-stratum contributions.

For alpha=1,m=3 and positive selection limit,

    C=(1/3) integral a0 p0 kappa^-2/3 dlambda,
    nu_local~C ell^-1/3,  N_local~(3/2)C ell^2/3.

Here ell=kappa r^3. Historical files using kappa_old=6ell/r^3 instead require kappa=kappa_old/6 and the corresponding6^(2/3) coefficient factor and transformed mark measure. Do not mix conventions.

## E. Review, attribution and what is genuinely new

The simplex estimate is Taylor plus linear algebra; the transfer law is a standard pushforward argument. Neither should be advertised as a worldwide-first discovery. Relevant prior tools include Gass–Stecconi's multi-point Kergin interpolation/determinant renormalization and Breiman-type regular-variation moment conditions. The potential research contribution is the precise pin-compatible typed contact kernel, its saddle identity/application, and verification of a common hypothesis package across persistence models. No novelty is certified here.

Sources inspected:
- Armentano, Azais, Leon, On a general Kac-Rice formula for the measure of a level set, arXiv:2304.07424v3, Sections7–8: https://arxiv.org/html/2304.07424v3
- Gass, Stecconi, The number of critical points of a Gaussian field: finiteness of moments, PTRF190 (2024), arXiv:2305.17586, Section2: https://arxiv.org/html/2305.17586v2
- Muirhead, A second moment bound for critical points of planar Gaussian fields in shrinking height windows, SPL160 (2020): https://arxiv.org/abs/1901.11336
- Denisov, Zwart, On a theorem of Breiman and a class of random difference equations, JAP44 (2007),1031–1046: https://doi.org/10.1239/jap/1197908822

Separate reviewer tasks: verify(A1) including shape assumptions; independently derive(B4) from(B1); check the extra-conditioned regression/UI and full-normalizer limit in(C); challenge(D) with small-mark/derivative counterexamples. No author self-acceptance and no overwrite of earlier evidence.
