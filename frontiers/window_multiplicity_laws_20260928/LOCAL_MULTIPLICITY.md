# A local two-saddle mechanism: global window multiplicity has order r^3

Object: OA-WINDOW-MULTIPLICITY-LOCAL-20260928-v1.
Author: OpenAI / ChatGPT, foreground research session, 28 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR ANALYTIC REVIEW REQUIRED.
Scientific effect: NONE. This note does not change a governing status or a prior proof.

## 1. Setting and statements

Use the exact **planar**, variance-one periodized Gaussian field, endpoint observations,
and determinant tilt of [RM] and [IW] in SOURCE_MAP.json. The torus side L is fixed.
Birth marks b range over a fixed compact interval and k over [k_-,k_+], with k_->0.
Frames range over O(2); stationarity permits the midpoint to be zero. In a local frame,

    M=(-r/2,0), S=(r/2,0),
    f(M)=b, f(S)=b-k r^3, grad f(M)=grad f(S)=0.

Q_r is continuous Gaussian regression on these six actual observations. It has no
adjacency or elder-pairing condition. F_j(H) is |det H| on nonsingular Hessians of
negative index j, and zero otherwise. Set

    W_r=F_2(H_M) F_1(H_S), Z_r=E_Qr W_r,
    dQ_r^W=(W_r/Z_r)dQ_r, I_r=(b-k r^3,b).

Let N_r count additional critical points on the torus, excluding M,S, whose heights
belong to I_r. Let A_r be the event that **two distinct additional saddles** in the
physical ball B(0,2r) have heights in I_r. No restriction on other critical points
is made. Balls are embedded by reducing r_*.

**Theorem L.** There are positive c,C,r_*, depending only on the fixed parameter
ranges and L, such that, uniformly in b,k,frame and 0<r<=r_*,

    c r^3 <= Q_r^W(A_r) <= Q_r^W{N_r>=2} <= C r^3.             (L1)

Consequently,

    E_Qr^W[N_r(N_r-1)] >= c r^3,                              (L2)
    Q_r^W{N_r>=2 | N_r>=1} >= c_0>0.                         (L3)

The expectation in (L2) is allowed to be an extended nonnegative number; no finite
upper estimate for it is being supplied. The conditioning in (L3) is well-defined
by (L1). The upper bound in (L1) consumes the already integrated planar global
HEIGHT-WINDOW first moment [IW, (I5)]. The lower bound has a direct Gaussian
jet-box proof below and does not consume any global elder-selection assertion.

In particular, a torus-wide extension of [RC]'s remote O(r^5) factorial bound is
false under these assumptions. A torus-wide conditional-uniqueness assertion
1-O(r^2) is also false. These statements do **not** contradict [RC] or the remote
singleton-law candidate [SL]: their spatial exclusion radius is fixed and positive,
whereas the event A_r occurs a distance of order r from the pins.

## 2. An exact cubic with strict, stable window witnesses

For k>0 define

    G_k(X,Z)=k(2X^3-3X/2-1/2-3Z^2/4-XZ^2).                  (L4)

Its gradient is k(6X^2-3/2-Z^2, -(3/2+2X)Z). Its four critical points and
Hessian data are as follows; all entries are exact.

| Point | Height | Hessian or determinant | Type |
|---|---|---|---|
| M_*=(-1/2,0) | 0 | diag(-6k,-k/2), det=3k^2 | maximum |
| S_*=(1/2,0) | -k | diag(6k,-5k/2), det=-15k^2 | saddle |
| P_+=(-3/4,sqrt(15/8)) | -7k/32 | det=-15k^2/2 | saddle |
| P_-=(-3/4,-sqrt(15/8)) | -7k/32 | det=-15k^2/2 | saddle |

At P_+ and P_- the Hessian is [[-9k,-2kZ],[-2kZ,0]]. The extra points
satisfy |P_+|^2=|P_-|^2=39/16<4. Their height -7k/32 lies strictly in (-k,0).
The endpoint determinant weight of this scaled cubic is 45k^4.

The equal heights of P_+ and P_- cause no stability problem: we require each
critical point to be nondegenerate and its height to be strictly inside the window,
not an equality between their heights. A perturbation can and generally will split
them while preserving both witnesses.

Choose disjoint small closed disks about P_+,P_- inside B(0,2), avoiding M_*,S_*.
The implicit-function theorem applied to the gradient at these nondegenerate zeros
gives a C^2 neighborhood of G_1 with a saddle in each disk. Shrink the neighborhood
so the two saddle heights lie, for example, strictly between -1 and 0. For fields
with the two pins exactly retained, shrink it again so their Hessians have the
specified indices and their determinant magnitudes exceed 3/2 and 15/2.
Multiplying by k and using k_->0 makes these neighborhoods uniform for the compact
k range. Thus there is a fixed epsilon_0>0 such that a scaled field within
k epsilon_0 of G_k in C^2(B(0,2)) has the two witnesses and

    F_2(H_scaled(M_*)) F_1(H_scaled(S_*)) >= (45/4) k^4.      (L5)

This is an ordinary open stability assertion about finitely many nondegenerate
zeros. It neither counts all critical points in the ball nor assumes a globally
Morse contact field.

## 3. Pinned Taylor normal form, including the transverse linear term

All derivatives below are at the physical midpoint. Write

    s=f_zz(0)/r, a=f_xxz(0), beta=f_xzz(0), c=f_zzz(0),
    P_{k,s,a,beta,c}(X,Z)
       =2kX^3-3kX/2-1/2*k + (s/2)Z^2
         +(a/2)(X^2-1/4)Z +(beta/2)XZ^2 +(c/6)Z^3.          (L6)

If ||f||_{C^4}<=K and the actual endpoint observations hold, multivariate Taylor
expansion gives, uniformly on B(0,3),

    || (f(rX,rZ)-b)/r^3 - P_{k,s,a,beta,c} ||_{C^2(B(0,3))} <= C r K. (L7)

Here and below harmless norm-equivalence constants depend on the fixed dimension.
To check all potentially dangerous divided powers of r, put h=r/2. The positive
Hermite/Peano identity for the endpoint heights and gradients gives

    f_xxx(0)=12k+O(r K).

Adding and subtracting the two endpoint expansions of f_x and f_z gives

    f_x(0)=-(r^2/8)f_xxx(0)+O(r^3K),
    f_z(0)=-(r^2/8)f_xxz(0)+O(r^3K),
    f_xx(0)=O(r^2K),  f_xz(0)=O(r^2K).

Expanding f at M and using its height b then yields

    f(0)-b=-(r^3/24)f_xxx(0)+O(r^4K)
          =-k r^3/2+O(r^4K).

Taylor remainders for derivatives of order 0,1,2 have sizes respectively r^4K,
r^3K,r^2K. After the coordinate and value rescaling each becomes O(rK).
This proves (L7). The term -a Z/8 is essential: omitting it violates the two
transverse gradient pins. The polynomial in (L6) itself satisfies both height and
both gradient pins exactly for arbitrary s,a,beta,c.

The cubic (L4) is (L6) at

    s=-3k/2, a=0, beta=-2k, c=0.                            (L8)

No exact degree-three assumption is imposed on the random field; (L7) controls
its higher-order terms on the event used below.

## 4. A rare jet box with probability bounded below by a constant times r

Use the nonsingular endpoint frame U_r of [RM, Section 2]. Its target v_r is bounded
and it converges to

    U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz), v_0=(b,0,0,12k,0,0).

Append the **physical**, not rescaled, vector

    J=(f_zz,f_xxz,f_xzz,f_zzz) at 0.                        (L9)

At r=0, (U_0,J) consists of the ten independent planar jet entries of orders at
most three. The positive Fourier spectrum of the exact periodized Gaussian field
makes its covariance positive definite: a zero-variance combination annihilates
every Fourier mode, hence is a zero distribution; arbitrary smooth prescribed
jets at the site force all its coefficients to vanish. Frame rotation preserves
linear independence. Continuity and compactness in O(2) give a uniform positive
covariance floor through sufficiently small r>=0. The corresponding upper bound
is finite as well.

It follows by a Schur complement that J under Q_r has a covariance sandwich and
bounded mean, uniformly in the compact marks and frame. Its Gaussian density is
therefore bounded **below** on any fixed compact target box.

For a small fixed epsilon>0 let B_r be the target box

    |f_zz + (3k/2)r| < epsilon k r,
    |f_xxz| < epsilon k,
    |f_xzz + 2k| < epsilon k,
    |f_zzz| < epsilon k.                                  (L10)

All these physical targets lie in a fixed compact box. Its Lebesgue volume is
16 epsilon^4 k^4 r, so

    Q_r{J in B_r} >= c_J r.                                (L11)

The small factor r is attached to exactly one coordinate, f_zz. Treating the
rescaled coordinate f_zz/r as having a uniformly nondegenerate density would lose
this factor and would be wrong.

## 5. Remainder control AFTER the rare jet restriction

A bounded unconditioned moment is not enough to subtract a fixed tail error from
an event of probability order r. Instead regress the entire smooth field on the
joint observation vector (U_r,J), at each target (v_r,j) with j in B_r.

For an unconditioned field copy F the usual regression representation is

    F(z)+Cov(F(z),V)Cov(V)^{-1}((v_r,j)-V), V=(U_r,J).

The coefficient functions have uniformly bounded C^4 norms: derivatives of the
covariance kernel are bounded, the integral observation frames have uniformly
bounded derivative-covariance norms, and Cov(V)^{-1} is uniformly bounded. The
Gaussian Fourier series has finite moments of its C^4 norm. Targets are bounded.
The triangle and moment inequalities therefore give, for every fixed finite p,

    sup_{r,marks,frame,j in B_r}
       E[||f||_{C^4}^p | U_r=v_r,J=j] < infinity.            (L12)

Choose a finite K large enough that Markov's inequality gives conditional
probability at least 1/2 to ||f||_{C^4}<=K at **every** such target. Integrating
this conditional probability against the jet density over B_r gives

    Q_r{J in B_r, ||f||_{C^4}<=K} >= (c_J/2)r.              (L13)

This uses a continuous Gaussian regular conditional kernel; it is not a claim of
independence between J and the field remainder. The rare event is retained before
any tail estimate is applied.

## 6. Tilt and normalization: r times r^4 divided by r^2

Choose epsilon in (L10) so (L6) is within k epsilon_0/2 of (L4) on B(0,3), hence on B(0,2).
Then choose r_* small enough that the C r K error in (L7) is below the remaining
k_- epsilon_0/2 margin. On the event in (L13), the stability argument gives A_r.
Since H_f(rX)=r H_scaled(X) in dimension two, each physical endpoint determinant
is r^2 times its scaled determinant. Equation (L5) implies

    W_r >= c_W r^4                                        (L14)

on that event, with c_W>0 uniform in the marks.

The full normalizer satisfies 0<Z_r<=C_Z r^2. This follows directly from the
endpoint gradient-average determinant bound W_r<=C r^2(1+||f||_{C^3})^4 and the
uniform Q_r moments, or from [RM, (11)]. In particular we do not replace Z_r by a
normalizer restricted to this rare configuration. Thus

    Q_r^W(A_r) >= E_Qr[W_r 1{J in B_r, ||f||C4<=K}]/Z_r
                >= (c_W c_J/(2C_Z)) r^3.                  (L15)

For the upper bound sum [IW, (I5)] over indices and use
1{N_r>=2}<=N_r/2. This proves (L1). The inequalities
N_r(N_r-1)>=2*1{N_r>=2} and
Q_r^W{N_r>=1}<=E_Qr^W N_r<=C r^3 prove (L2) and (L3).

## 7. Sharp obstruction to a global Bernoulli-configuration approximation

Let Xi_r be the finite global window point process, retaining any of location,
index and normalized height as marks. Its mean measure mu_r has mass m_r<=C r^3,
so m_r<=1 for small r. Define Ber(mu_r) to be empty with probability 1-m_r and
otherwise a singleton with distribution mu_r/m_r.

The elementary identity in the parallel singleton-law candidate [SL] is useful,
but we rederive it here so this corollary does not consume an unreviewed premise.
Write sigma for the singleton submeasure, eta for the mean measure on N>=2,
h=eta(S)=E[N;N>=2], alpha=P(N>=2), and s=P(N=1). The difference between Law Xi
and Ber(mu) has masses h-alpha on the empty stratum, minus the nonnegative
measure eta on the singleton stratum, and mass alpha on the multiple stratum.
Its full variation is 2h; therefore probability TV is exactly h. Applying (L1),

    c r^3 <= dTV(Law Xi_r,Ber(mu_r)) <= C r^3.             (L16)

Indeed h>=2P(N_r>=2) and h<=m_r. Thus the global exact-mean Bernoulli error is
of the **same order** as the global occurrence probability, unlike the remote
r^5 error. More generally, any probability law supported only on empty and
singleton configurations differs from Law Xi_r by at least c r^3, by testing
the event N>=2. Conditional on nonemptiness, its distance from every singleton
law is at least c_0 from (L3). No global factorial-moment upper bound was needed.

## 8. What this closes and what it does not

This supplies an existential, all-small-r lower mechanism for **local multiple
window saddles** under the original maximum/saddle determinant tilt. Together
with the existing first moment it fixes the global multiple-occurrence probability
order at r^3. It therefore rules out a proposed uniform extension of remote
single-point asymptotics to the whole torus.

It does not give a global upper bound on the second factorial moment, a numerical
constant or cutoff, a global limit measure, or a distribution of persistence
partners. The weaker event A_r by itself does not determine elder pairing. The separate
ELDER_LOWER_AND_DENSITY_GAP.md uses the stronger specific jet-box event and an
explicit path to a point above the birth height to prove an elder-failure lower bound. No result for d>2, shrinking gap mark k, growing torus, random
selected spatial domain, or all-height count is asserted. The Gaussian jet-box and
stability arguments above are analytic proof obligations for a nonauthor reviewer;
the exact polynomial tests are not their substitute.
