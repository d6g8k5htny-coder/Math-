# Fixed-transverse Gaussian contact: an explicit leading kernel and saddle selection

Object: OA-TYPED-TRANSVERSE-CONTACT-20260925-v1. Author: OpenAI / ChatGPT.
Disposition: author-side analytic extension for separate review; not independent acceptance, not a global RN or persistence-selection theorem.

This note strengthens the fixed-transverse O(k r^3) candidate in Math- PR16, exact source 32b80ee085dc6a40113d1e46e333cda50d57ba21, TRANSVERSE_BOUND_CANDIDATE.md (SHA256 f64c954245f17bcbc64a5ccf58a60689cf2a2fd85362f8321c0f64ff66584e36). The earlier source remains unchanged. The new ingredients are an explicit shape bound, a one-free-jet contact integral and an exact intermediate-saddle identity. The continuum proof below is not certified by the accompanying finite tests.

## 1. Fixed model and population

On the fixed two-dimensional torus of side L>0, take the centered variance-one Gaussian field with covariance

    K_L(z)=sum_{n in Z^2} exp(-|z+Ln|^2/2)
             / sum_{n in Z^2} exp(-|Ln|^2/2).

Fix compact b and k ranges, 0<kmin<=k<=kmax, and an orthonormal local frame. Prescribe

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Let Q_r be Gaussian regression on all six pins. For a symmetric two-by-two matrix H let

    F_j(H)=|det H| 1{H has j negative eigenvalues},

with value zero on singular matrices. Set

    W_r=F_2(H_M) F_1(H_S), Z_r=E_Qr W_r,
    dQ_r^W=(W_r/Z_r)dQ_r.

This is an endpoint-type weighted law, not conditioning on actual persistence adjacency. No original-pin density/Jacobian is multiplied into Z_r.

Let K be the nonempty fixed compact chart

    K={(u,v): A0<=sqrt(u^2+v^2)<=B, |v|>=eta},
    1<A0<B<infinity, 0<eta<B.

For Borel E subset K let N_j(rE) count index-j critical points in rE with height in (b-k r^3,b).

## 2. Proposed refined theorem

There are nonnegative continuous kernels Lambda_j(u,v;b,k,frame) and epsilon(r)->0, uniform on these compact parameters, such that

    |E_Qr^W N_j(rE)-r^3 integral_E Lambda_j(u,v)du dv|
        <= epsilon(r) r^3 area(E).                          (2.1)

The explicit kernels in Section6 satisfy

    Lambda_0=Lambda_2=0,   Lambda_1>0.                       (2.2)

The positive saddle kernel is bounded above and away from zero on each fixed nonempty compact chart/parameter set. Consequently for small r,

    c r^3 area(E) <= E_Qr^W N_1(rE) <= C r^3 area(E),
    E_Qr^W[N_0(rE)+N_2(rE)] = o(r^3) area(E).               (2.3)

Factors k may equivalently be made explicit in the bounds because k is confined to [kmin,kmax]. No estimate uniform as kmin->0 or eta->0 is asserted. The extrema are not forbidden at finite r; their leading r^3 coefficient vanishes. No matching lower probability bound or elder-defect lower bound is inferred from an expected-count asymptotic.

## 3. Gaussian regularity, pins and normalization

Use the exact centered observations

    U_r=((fM+fS)/2,(fS-fM)/r,(fxS-fxM)/r,
         (6/r^2)(fxM+fxS-2(fS-fM)/r),
         (fzM+fzS)/2,(fzS-fzM)/r)

at target (b-k r^3/2,-k r^2,0,12k,0,0). Their contact limit is

    U_0=(f,fx,fxx,fxxx,fz,fxz)_0, v_0=(b,0,0,12k,0,0).

Every Fourier mode of the periodic model has strictly positive variance proportional to exp(-2*pi^2*|n|^2/L^2), and the square roots of these variances are summable after multiplication by any fixed polynomial in |n|. Thus the field has all fixed derivative-supremum moments. Independent finite derivative functionals have positive covariance: zero variance would force a finite derivative distribution to annihilate every Fourier mode and hence every smooth test function.

The coefficients of U_r converge to U_0 by symmetric Taylor formulas, in every fixed Lp norm, with the same convergence for derivative-field cross-covariances. Compactness of O(2) gives uniform inverse covariance bounds; no full rotational invariance of the torus is used. Applying Gaussian regression to a common underlying field gives convergence in every fixed Lp(C^m) and uniform moments on all bounded target sets.

Let a=fzz(0) under the endpoint contact law. It has a nondegenerate Gaussian conditional distribution. From the finite pins,

    fxx(M)/r -> -6k, fxx(S)/r -> 6k,
    fxz(M),fxz(S)=O_Lp(r), fzz(M),fzz(S)->a.

It follows, by continuity of the endpoint types off a=0 and uniform integrability, that

    Z_r/r^2 -> z0,
    z0=36k^2 E[a^2 1{a<0}|U_0=v_0]>0.                     (3.1)

Continuity and compactness make the convergence and positive lower bound uniform. Only endpoint conditioning belongs in this denominator.

## 4. Joint gradient/height density with the original-pin terms retained

At X=(ru,rv), use

    J_r=(fx(X)/r^2, fz(X)/r,
         [f(X)-b-(rv/2)fz(X)]/r^3).                       (4.1)

Write the finite-r midpoint jets a=fzz, q=fxxz, c=fxzz, d=fzzz. The exact finite-pin correction, proved in GEOMETRY_AND_CUBIC_INDEX.md and obtained for smooth fields by Taylor remainder estimates, gives

    J_r -> J_0=(6k D+quv+cv^2/2,
                av,
                k Lc+qDv/4-dv^3/12),                    (4.2)

where D=u^2-1/4 and Lc=2u^3-3u/2-1/2. The remainder is O_Lp(r), uniformly on K under endpoint conditioning, with all necessary higher moments finite.

Let g(a,q,c,d) denote the nondegenerate four-dimensional conditional Gaussian density of these four jets given U_0=v_0. They are independent derivative functionals modulo U_0, although they need not be probabilistically independent. The minor of J_0 on columns (a,c,d) is v^6/24. Hence the three-by-three conditional covariance of J_0 is uniformly positive on |v|>=eta, as is that of J_r for small r.

The exact affine Jacobian from (fx,fz,f) to J_r has absolute determinant r^-6. At height b-k r^3 theta and gradient zero, J_r=(0,0,-k theta). Thus the physical joint density is

    p_(grad,height|pins)(0,b-k r^3 theta)
        = r^-6 p_(J_r|pins)(0,0,-k theta).                 (4.3)

In particular it is at most C r^-6 on the whole fixed chart and theta in [0,1]. A leading height row dependent on a gradient row cannot replace this joint normalization.

## 5. Small Hessians, conditional moments and the contact matrices

On the three-zero-gradient event, the deterministic shape theorem bounds every Hessian by CH*r*M3, where M3 is a bound on the third derivative tensor on the local convex neighborhood. The conditional law given the additional J_r target can be realized by a second linear Gaussian regression:

    F_r^*=F_r^Q+Cov(F_r^Q,J_r) Cov(J_r)^-1 (target-J_r).

The covariance inverse is uniformly bounded. The base derivative-supremum moments and cross-covariances are uniformly bounded. Therefore all fixed conditional C^m moments, including E[M3^6], are uniformly bounded over the chart, marks and theta. These are moment bounds under the *extra witness constraints*, not borrowed blindly from endpoint-only conditioning.

This immediately yields the upper bound

    E[W_r F_j(H_X)|pins,J_r=target] <= C r^6,

and, with (4.3), spatial r^2, height k r^3 and (3.1), the earlier O(k r^3) estimate.

For the limit coefficient, the same common-field regression construction converges in Lp(C^m) to the contact-conditioned field. The witness-gradient relation yields

    a_r/r -> A= -[qD/2+cuv+dv^2/2]/v,

although the unscaled limiting a itself is zero. It is essential not to confuse these two limits. Consequently

    (H_M/r,H_S/r,H_X/r) -> (B_M,B_S,B_X),                  (5.1)

with the matrices in GEOMETRY_AND_CUBIC_INDEX.md, Section4. The constraints J_0=(0,0,-k theta) solve

    a=0,
    c(q)=-12kD/v^2-2qu/v,
    d(q)=12k(Lc+theta)/v^3+3qD/v^2,
    A(q)=(12ku+6k+qv-12k theta)/(2v^2).                   (5.2)

Filtered determinants F_j are continuous through singular matrices: on crossing an index boundary the determinant vanishes. Their growth is polynomial. The deterministic bound plus uniform conditional derivative moments supplies uniform integrability of the triple product. Thus the full product expectation divided by r^6 converges to its contact counterpart. All convergence is uniform by compactness and the Gaussian regression bounds. This yields an o(1) remainder; no explicit convergence rate is claimed here.

## 6. One-free-jet formula for the leading kernel

Define

    T_j(q;u,v,k,theta)=F_2(B_M)F_1(B_S)F_j(B_X).

Changing variables from (a,q,c,d) to (J_1,J_2,J_3,q) at contact has Jacobian |v|^6/24. Hence

    Lambda_j(u,v;b,k,frame)
      = 24k / (z0 |v|^6)
          integral_0^1 integral_R
            g(0,q,c(q),d(q)) T_j(q;u,v,k,theta) dq dtheta.  (6.1)

This is a one-dimensional Gaussian integral for each fixed height fraction theta, followed by a compact theta integral. It retains all correlations through g; it is not a product of independent expectations. The constants and g use the exact periodic covariance, not an unperiodized approximation.

Gaussian decay in q and polynomial growth of T_j make the integral finite, uniformly on compact parameter sets. Their continuous dependence and domination prove continuity.

The exact cubic identity gives

    det B_X=-(9k^2/v^2)[(w+1-2theta)^2+4theta(1-theta)],
    w=(qv+12ku)/(6k).

Thus T_0=T_2=0 for theta in (0,1), proving Lambda_0=Lambda_2=0. For theta near1/2 and w near-1, all three desired type factors in T_1 are strictly positive. The conditional density g is strictly positive there. Therefore Lambda_1>0. Compactness yields a uniform positive minimum on each fixed nonempty chart and compact mark/frame set.

The type restrictions also make the free-jet integration bounded. In the variable
w=(qv+12ku)/(6k), M is a maximum and S a saddle exactly when

    -1-2 sqrt(theta) < w < 1-2 sqrt(1-theta), 0<theta<1.     (6.2)

Indeed det B_M>0 bounds w between -1±2sqrt(theta); det B_S<0 selects the left branch w<1-2sqrt(1-theta). The displayed upper bound is smaller than -1+2sqrt(theta). Thus (6.1) can be evaluated on a finite interval after dq=(6k/|v|)dw. Setting theta=sin^2(phi), 0<=phi<=pi/2, removes square roots from the interval endpoints for a smooth quadrature parametrization. This is useful computational structure, not a quadrature error enclosure.

Finally the marked Kac-Rice identity gives, after X=r(u,v), height=b-k r^3 theta,

    E_Qr^W N_j(rE)
      = [k r^5/Z_r] integral_E integral_0^1
          p_(J_r|pins)(0,0,-k theta)
          E[W_r F_j(H_X)/r^6 | pins,J_r=(0,0,-k theta)]
          dtheta du dv.                                    (6.3)

The endpoint and witness determinants occur once each. Since Z_r/r^2->z0,
(6.3) and uniform convergence prove (2.1).

## 7. Exact-model diagnostic, not a periodization substitute

For the unperiodized covariance exp(-|x-y|^2/2), direct finite-jet regression gives

    (a,q,c,d)|U_0=v_0 ~ N((-b,0,0,0), diag(2,2,2,6)).

The accompanying code checks that covariance and mean by exact rational Schur algebra. It is useful for implementing a numerical prototype of (6.1). It is NOT a replacement for the exact finite-L covariance in the theorem, and no finite-L numerical coefficient or rigorous quadrature enclosure is delivered here. The separate unperiodized quadrature diagnostic is explicitly uncertified.

## 8. Review and exclusions

Separate review is needed for the uniform Gaussian regression/covariance statements, passage to scaled Hessians after the extra pins, full normalizer, and marked Kac-Rice/disintegration. The exact polynomial identities are independently checked by the delivered standard-library script but do not constitute continuum verification.

The theorem is a proposed local count asymptotic only. It does not show that every counted saddle prevents elder pairing. It does not settle eta->0, a shrinking kappa lower cutoff, the intermediate spatial scale, higher dimensions, witness-witness collisions or full RN/24-jet certificates.

Framework attribution: Armentano–Azais–Leon, arXiv:2304.07424v3, Theorem7.1 and Section8.1. Related multi-point interpolation and determinant control: Gass–Stecconi, arXiv:2305.17586. Those sources do not themselves supply this exact six-pin contact kernel or authorize a novelty claim.
