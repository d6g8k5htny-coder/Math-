# Pin microdisk gradient desingularization — covariance lemma

**Object:** OA-PIN-MICRO-COV-20260926-v1  
**Author:** OpenAI / ChatGPT  
**Disposition:** author-side lemma for separate review.  
**Scientific effect:** NONE.

This addresses exactly the P5 covariance gap identified in the OpenAI review of Cursor PR53. It does **not** prove the final determinant-weighted pin-disk count and does not change any RN/global status.

## 1. Setup

Use the exact d=2 normalized periodized Gaussian field and the original six endpoint pins

    M=(-r/2,0),  S=(r/2,0),
    f(M)=b, f(S)=b-k r^3,
    grad f(M)=grad f(S)=0,

with b and k in compact sets and k>=k_->0. Put the witness in the physical r^2 endpoint chart

    X=M+r^2(P,Q),

with |P|,|Q|<=K and (P,Q)!=(0,0). Under the endpoint regression law Q_r define

    G_r(P,Q)=( f_x(X)/r^3, f_z(X)/r^2 ).

At (P,Q)=(0,0) this vector is identically zero because X=M. That point is the conditioned pin, not an extra Kac-Rice witness.

## 2. Exact degree-four coefficient matrix

At M write

    S0=f_zz,  T=f_xxz,  R4=f_xxxx.

Solving the endpoint pins through degree four gives

    f_xx(M)=-6kr+(r^2/12)R4,
    f_xxx(M)=12k-(r/2)R4,
    f_xz(M)=-(r/2)T+O(r^2).

In the degree-four Taylor polynomial, the exact coefficients of (S0,T,R4) in G_r are

    B_r(P,Q) =
      [ 0, Q(rP-1/2),  rP(2rP-1)(rP-1)/12 ]
      [ Q, rP(rP-1)/2,                         0 ].

The three 2x2 minors are

    m_ST = -Q^2(2rP-1)/2,
    m_SR = -r P Q (rP-1)(2rP-1)/12,
    m_TR = -r^2 P^2 (rP-1)^2(2rP-1)/24.

If rK<=1/4 then |2rP-1|>=1/2 and |rP-1|>=3/4, so

    |m_ST| >= Q^2/4,
    |m_TR| >= (3/256) r^2 P^2.

By Cauchy-Binet,

    det(B_r B_r^T)=m_ST^2+m_SR^2+m_TR^2
       >= c0 (Q^2+r^2P^2)^2.                     (2.1)

Also tr(B_r B_r^T)<=C0(Q^2+r^2P^2). Therefore, with

    h^2=Q^2+r^2P^2,

both singular values of B_r are comparable to h. The anisotropic scale is forced by the endpoint pin: on Q=0 the first random longitudinal correction appears one order later through R4.

## 3. Conditional Gaussian covariance

Use the desingularized endpoint pin frame from the byte-bound parent source. At contact it contains

    (f, f_x, f_xx, f_xxx, f_z, f_xz),

while (S0,T,R4)=(f_zz,f_xxz,f_xxxx) are distinct residual derivative functionals. The combined finite-jet covariance is positive definite at contact, uniformly over the compact frame set; hence its residual Schur covariance stays uniformly positive for small r.

Taylor-expand the actual G_r through degree four using the integral remainder. On bounded (P,Q), the omitted terms have L2 coefficient norm o(h), uniformly as r->0; the vanishing at (P,Q)=0 is retained rather than replaced by an absolute remainder. Consequently the covariance of the actual normalized gradient satisfies, after reducing r_*,

    c h^2 I_2 <= Cov(G_r(P,Q)|pins) <= C h^2 I_2,      (3.1)

uniformly for every nonzero (P,Q) in the bounded microdisk.

This is the missing uniform statement in PR53 P5: it describes the degeneration *toward* the conditioned pin instead of invoking only pointwise distinct-site nonsingularity.

## 4. Density envelope

The deterministic longitudinal mean is

    E[G_{r,1}] = 6kP(rP-1)+O(h)

uniformly on compact b,k,frames; conditional residual-jet means contribute only O(h). Thus Gaussian coercivity from (3.1) gives

    p_{G_r(P,Q)|pins}(0)
       <= C h^-2 exp[-c P^2/h^2].                    (4.1)

The affine physical-to-normalized gradient map has determinant r^-5, hence

    p_{grad f(X)|pins}(0)
       <= C r^-5 h^-2 exp[-c P^2/h^2].              (4.2)

Two limiting regimes are now one formula:

- Q=0,P!=0: h=r|P| and the cost is exp[-c/r^2];
- |Q|>>r|P|: h~|Q| and the transverse q-normalization is recovered.

For P=tQ away from Q=0, Gaussian decay in t absorbs any fixed polynomial in P/h. This is the correct integrability mechanism for the determinant-repulsion step.

## 5. Remaining determinant lemma

This note closes only the covariance/density part of the microdisk interface. The remaining load-bearing statement is a conditioned determinant estimate of the form

    E[ W_r |det H_X| | pins, grad f(X)=0 ] / Z_r
       <= C r^6 h^2 Poly(P/h),                       (5.1)

or any stronger integrable replacement.

Combined with (4.2), (5.1) would give physical Kac-Rice intensity O(r) times an integrable Gaussian factor. Since the microdisk has physical area O(r^4), its expected witness count would then be O(r^5), well below the cubic scale.

The exact contact algebra reviewed on PR53 already shows two soft factors: after imposing the witness gradients, det(H_M/r) and det(H_X/r) each vanish linearly in the transverse/anisotropic collision parameter while det(H_S/r) remains polynomial. Turning that finite-jet cancellation into the uniform conditional expectation (5.1) is the next theorem, not an inference made here.

## 6. Review request

A nonauthor reviewer should independently check:

1. the degree-four pin solution and matrix B_r;
2. all three minors and the h-scale Cauchy-Binet bound;
3. uniform residual Schur covariance modulo the six endpoint pins;
4. the Taylor remainder as o(h), uniformly across Q=0 and P=0 approaches;
5. the mean/density coercivity in (4.1).

No finite test, green CI, or merge is analytic acceptance.
