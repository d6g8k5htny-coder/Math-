# Essentiality in the critical-gap window

28 October 2026. OpenAI/Codex GPT-6 author-side continuation by `/root`,
with `essential_template`, `essential_gaussian_cost` and
`next_marked_hypothesis` as author support. Same-family technical checks
are not the required different-family scientific review.

## 1. Scope and the existing cusp result

Use the spectral class (1) and the original pins, weight and path-functional
events of [PROOF.md](PROOF.md). Fix b, a direction u, and tau>0, and now set
k=tau r, so that f(S)=b-tau r^4. Limits below first let r tend to zero with
these parameters fixed. No joint r,tau limit is asserted.

The quartic contact model, its typed determinant weight and its local elder
window are EXISTING results: `cusp_second_order_20261001/PROOF.md`, CU.2--CU.4,
with related formulations in the candidate/elder third-order packets. In
that source's notation our B is its transverse vector gamma, and our scalar
gamma below is its Y/det(A)=6 tau phi. Its Remark 8.1 also already contains
the small-tau cubic normalization factor288. We do not claim these as new.

What follows supplies the actual GLOBAL essential indicator, which CU.3's
negative-quartic case leaves as either a finite remote connection or global
essentiality. It also reconstructs the needed contact convergence for the
explicit finite-positivity, C4 class here, rather than assuming the original
full-spectrum covariance or C5 bounds.

## 2. A common regression coupling and the reused weight

Let U_r be the desingularized observations in the main proof, Sigma_r their
covariance, and c_r(x)=Cov(F(x),U_r F). Use one underlying source field F and
define

    f_r=F+c_r Sigma_r^-1(v_r-U_r F).

Its marginal law is exactly Q_r. Its contact limit f_0 has law Q_0, the
continuous Gaussian regression at

    f_0(0)=b, grad f_0(0)=0,
    D_u^2 f_0(0)=0, D_u D_y f_0(0)=0, D_u^3 f_0(0)=0. (CW1)

The target tends to (b,0,...,0), independent of tau. This construction gives
f_r -> f_0 almost surely in C4. Indeed U_r F -> U_0 F for every C3 sample;
the finite covariance inverse converges by the rank proof. Fourier absolute
summability gives c_r -> c_0 in C4: the largest cross derivative has order
4+3=7, controlled by sum a_n(1+|n|)^8<infinity. Thus this is an explicit
coupling, not an unsupported probability convergence to a common random
matrix imported from the older in-law statements.

In a fixed orthonormal (u,y) frame put, under Q_0,

    A=D_y^2 f_0(0), B=D_u^2 grad_y f_0(0), c=D_u^4 f_0(0),
    Delta=det A,
    Y=(c/12)Delta-(1/4)B^T adj(A) B,
    gamma=c/12-(1/4)B^T A^-1 B when det A!=0,
    w_tau=(36 tau^2 Delta^2-Y^2)_+ 1{A<0},
    z(tau)=E_Q0 w_tau.                              (CW2)

The joint conditional Gaussian (A,B,c) is nondegenerate. Appending its
entries to U_0 gives distinct rotated differential monomials of total
degree at most four. A polynomial of that degree vanishing on the cube-two
five-point frequency grid is identically zero. Positive variances on that
cube therefore give full rank. In particular det A=0 has probability zero,
and c conditional on (A,B) has a nonzero constant Gaussian variance.

Exact Taylor expansion using BOTH value and full-gradient pins, and the
C4 coupling, gives

    D_u^2 f_r(M)/r^2 -> -6tau+c/12,
    D_u^2 f_r(S)/r^2 ->  6tau+c/12,
    D_u grad_y f_r(M)/r -> -B/2,
    D_u grad_y f_r(S)/r ->  B/2,
    D_y^2 f_r(M),D_y^2 f_r(S) -> A.                  (CW3)

For example, solving the scalar value/derivative Taylor equations gives
D_u^3 f_r(M)/r ->12tau-c/2, then the two axial entries in (CW3).
The transverse-gradient difference gives the two mixed limits. The correct
congruence HERE is diag(r^-1,I), because the soft Hessian scale is r^2.
Schur complements give the scalar limits gamma-6tau and gamma+6tau.
Consequently W_r/r^4 -> w_tau almost surely outside the zero-probability
boundaries A singular or gamma=+/-6tau. The inverse-free expression in
(CW2) also avoids any inverse-matrix moment assumption.

The refined determinant estimate (25) with k=tau r gives

    W_r/r^4 <= C[tau^2 K_r^(2d-2)+K_r^(2d)],
    sup_(small r) E_Qr exp(eta K_r^2)<infinity,
    Z_r/r^4 -> z(tau)>0.                            (CW4)

These estimates give uniform integrability. Strict positivity follows
because A has full density on a strictly negative ball and, conditional on
(A,B), gamma has an everywhere positive Gaussian density and can fall in
(-6tau,6tau). This extends the reused weight result to the stated class.

## 3. Excluding a competing point at the pinned height

Almost surely, f_0 has no critical point x!=0 at height b. Here is a finite
mode proof at the actual contact regression. The periodic function q in
the main proof is positive away from0, and q^2 has a zero of order four at0.
Thus q^2 times ANY first-jet trigonometric basis at x kills all the contact
rows (CW1), while giving arbitrary value/full-gradient at x. All modes fit
in cube three. Conditional covariance of (f_0(x),grad f_0(x)) is therefore
positive definite off0. On each compact set separated from0 it has a
positive common gap. The overdetermined-zero mesh argument in main §11,
with d+1 target coordinates and d parameter coordinates, excludes zeros of
(f_0(x)-b,grad f_0(x)). C2 bounds suffice; countable exhaustion completes
the assertion. This statement does not require f_0 to be Morse at0, where
it is deliberately degenerate.

It follows that, on {max f_0<=b}, the pinned point is the unique global
maximum. A second point at height b would itself be a critical maximum.
In particular there is a strict gap below b outside every neighborhood
of0. Conditional Gaussian density also excludes gamma=-2tau.

## 4. A fixed-neighborhood argument for the essential indicator

On {A<0}, choose a small fixed physical coordinate chart (x,y) about0 in
which the transverse Hessian is strictly negative. The implicit function
theorem gives the unique transverse ridge y_r(x), for f_r and all small r,
with y_r(0)=y_r(r)=0. The ridges converge in C3 to y_0. Put
g_r(x)=f_r(x,y_r(x)). Although y_r is only C3, the envelope identity
g_r'=D_x f_r(x,y_r(x)) gives g_r in C4 and convergence in C4. The contact
constraints yield

    y_0'(0)=0, y_0''(0)=-A^-1 B,
    g_0''''(0)=c-3B^T A^-1 B=12gamma.                (CW5)

The exact ridge pins are g_r(0)=b, g_r(r)=b-tau r^4 and
g_r'(0)=g_r'(r)=0. Cubic Hermite interpolation consequently gives, for each
x in that FIXED interval,

    g_r(x)-b=tau(2r x^3-3r^2 x^2)
                      +(g_r''''(xi)/24)x^2(x-r)^2,  (CW6)

where xi is between the nodes 0,r,x. The repeated-node remainder is valid
also when x is outside [0,r].

Suppose gamma<-2tau. Choose a with gamma/2<a<-tau. Shrink the chart so
that, for all sufficiently small r, g_r''''/24<=a throughout it. Writing
rho=-a/tau>1, the bracket after factoring tau x^2 in (CW6) is at most

    2r x-3r^2-rho(x-r)^2
      =-rho[x-(1+1/rho)r]^2+(1/rho-1)r^2 <0.       (CW7)

Hence g_r(x)<b for every x!=0 in the fixed chart. Transverse strict
concavity makes f_r(x,y)<=g_r(x), with equality only on the ridge.
This controls the entire intermediate region r<<|x|<<1; compact scaled
Taylor convergence alone would not suffice for that purpose.

If also max f_0<=b, §3 gives the fixed positive gap outside a smaller chart;
uniform C0 convergence preserves it. Thus f_r has no point above b, and is
essential, for all sufficiently small r. If max f_0>b, uniform convergence
instead preserves a strictly older point and essentiality fails.

For gamma>-2tau, the microscopic ridge expansion at x=rt is

    r^-4(g_r(rt)-b) ->
       P_(tau,gamma)(t)=tau(2t^3-3t^2)+(gamma/2)t^2(t-1)^2.

At t=2 its value is 4tau+2gamma>0, so essentiality again fails eventually.
Combining the cases on the support of w_tau proves the weighted-indicator
limit, and (CW4) supplies uniform integrability:

    P_r(E_r) -> p_E(tau)
      := E_Q0[w_tau 1{gamma<-2tau, max f_0<=b}]/z(tau). (CW8)

There is no claim of convergence of unweighted indicators on the
zero-weight part of the contact space.

## 5. The limit has genuinely positive essential and remote mass

For every fixed tau>0,

    0<p_E(tau)<1.                                   (CW9)

This requires a support argument, but not a full C4-support assumption.
Choose tau<a<3tau and T>0. With s,q as in the main proof and the fixed
projector onto u-perpendicular, consider the finite Fourier contact fields

    H_0=b-a q^2-T|P_(u perpendicular)s|^2,
    H_1=H_0+G q^3,

where G is large enough that H_1(p)>b at p=(L/2,0,...,0). They satisfy
every row (CW1), are in the source RKHS, and have

    A=-2T I, B=0, c=-24a, gamma=-2a in (-6tau,-2tau).

H_0 has a unique global maximum at0. Its contact relative small C4 ball
retains that property: along the ridge the contact rows force zero second
and third derivatives and a strictly negative fourth derivative; the hard
block stays strictly negative and the complement has a positive gap.
The H_1 ball retains a strictly older point, the same strict jet inequalities,
and a positive local deficit on a fixed small surrounding sphere. The
q^3 term has order six and changes none of these contact jets.

Every centered Gaussian Radon measure on C4 gives positive mass to every
ball about0. One elementary proof covers a positive-mass compact set by
finitely many sufficiently small balls; one has positive mass. Two
independent samples in it have a small difference, whose law after division
by sqrt(2) is the original centered Gaussian law. Apply this to the centered
conditional law. Since H_j-mu_0 is in its Cameron-Martin kernel, equivalent
Gaussian translation gives positive probability to each of the relative
balls just described. On them w_tau is strictly positive. The H_0 ball
makes (CW8)'s numerator positive; the H_1 ball gives positive mass to its
complement. This proves (CW9).

## 6. Finite remote connections and moment divergence at every fixed tau

The local decision theorem CU.3 of the existing cusp source is deterministic
and requires only C2 closeness on its fixed rescaled window. It therefore
applies here: C4 Taylor expansion with the exact pins gives that closeness
to its quartic polynomial, in scaled C2, along our coupling. To see the
regularity point explicitly, write the physical coordinates as
(rX,r^2 Xi). Taylor remainders through derivative order two are
o((|x|+|y|)^(4-j)); multiplication by the scaled derivative factors
r^(p+2q-4) leaves o(1) for p+q<=2 on bounded (X,Xi). The dropped terms of
weighted degree greater than four tend to zero. Exact pin equations give
the same contact coefficients as (CW3). Moving from our M=0 to the source's
midpoint coordinates is just translation by ru/2. No stochastic theorem
or C5 error rate is imported from that source.

Outside the null boundaries gamma=+/-2tau,+/-6tau, its conclusions on the
typed support are:

- If -2tau<gamma<2tau, S is the actual elder partner, so X_r=1 eventually.
- If gamma>2tau, death is above f(S), so X_r<1 eventually.
- If gamma<-2tau, the local trap forces death below f(S), or essentiality.

Only in the last branch does §4 identify finite versus essential by whether
max f_0>b. It would be false to use that global criterion for finite death
in the other branches: a microscopic older point can appear even when the
contact field's maximum equals b. Weighted dominated convergence now gives

    P_r(L_r) -> p_L(tau)
      := E_Q0[w_tau 1{gamma<-2tau, max f_0>b}]/z(tau)>0. (CW10)

The H_1 neighborhood in §5 proves strict positivity. It also proves a
stronger size statement without any continuity assumption on death. Choose
that neighborhood small enough that every contact field in it is below
b-2eta on a fixed small surrounding sphere inside the ridge chart of §4,
above b+2eta at p, and has
w_tau bounded below by a positive constant. For each coupled sample in
this positive-probability neighborhood, uniform convergence preserves a
drop of at least eta on the sphere and an older endpoint. Every path to
an older point crosses the sphere, since §4 preserves the local maximum
on its interior. Thus the death is finite and b-d_f(M)>=eta. Fatou's lemma
with (CW4) gives a positive limiting lower bound for the P_r probability
of this event. In particular X_r>=eta/(tau r^4) there.

Finally (CW4), its exponential-square estimate and the normalizer floor
give uniform moments of K_r under P_r at each fixed tau. On finite deaths
X_r<=2K_r/(tau r^4). Consequently, for every fixed q>0 and tau>0 there are
strict positive constants c_(q,tau),C_(q,tau) such that

    c_(q,tau) r^(-4q-3)<=r^-3 E_Pr[X_r^q;L_r]
                                 <=C_(q,tau) r^(-4q-3). (CW11)

This extends the moderate-gap nonvanishing conclusion to EVERY fixed
positive critical ratio, and identifies the normalized finite-moment
divergence rate. The finite-versus-essential split is the global addition
to the existing local cusp decision.

All these statements first take r to zero at fixed tau. They do not give
uniform lower bounds as tau tends to zero, an optimal rare-event coefficient
as tau tends to infinity, or a global counting-intensity expansion. In
particular the existing 288 tau^3 normalization does not determine an
essential-share asymptotic: the event {max f_0<=b} depends on the field
when its effective quartic curvature approaches zero. The original cusp
weight and local elder sector remain attributed to their existing sources.
