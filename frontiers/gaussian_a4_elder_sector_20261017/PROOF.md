# Actual Gaussian A4 sectors with the global elder partner

Conventional mathematical author proposal, 17 October 2026. Authors: the
OpenAI/Codex A4-sector author, Root01a11cbf (mechanism coauthor), and the
focused ridge/frame coauthor identified in the author result. This exact
proposal requires a separate nonauthor review. All participants are
source-exposed; no organizational, provider, blind, or human independence is
claimed. The mathematical result below is a restricted population theorem on
a fixed two-dimensional flat torus, not a whole-density correction theorem.

## 1. Actual law and theorem

Fix L>0, X=R^2/(L Z^2), its Euclidean metric and orientation, and V=L^2.
Let phi_j be real smooth periodic functions with dense real span in C-infinity(X),
let a_j>0 satisfy sum_j a_j ||phi_j||_Cq<infinity for every integer q>=0,
and let Z_j be the original independent standard real Gaussians. Use the
actual smooth random field

    F=sum_j a_j Z_j phi_j.                                           (1)

All assertions concern each fixed such law separately. One explicit example
uses k_n=2 pi n/L, w_n=exp(-|k_n|^2/2)/sum_m exp(-|k_m|^2/2), a set H containing
one member of each nonzero pair {n,-n}, and independent standard Gaussians:

    F(x)=sqrt(w_0) Z_0 + sum_{n in H} sqrt(2w_n)
            [Z_n^c cos(k_n.x)+Z_n^s sin(k_n.x)].                      (2)

Its covariance is sum_n w_n cos(k_n.(x-y)). The positive exponentially
decreasing weights give every required smooth-norm summability, and Fourier
partial sums give dense smooth span. No finite-field truncation is performed.
Stationarity and isotropy are not needed in the theorem.

The consumed smooth-Gaussian admission theorem G, exact SHA256
8d992e194f0a898e563c4c3d05b8079cde292f9e87d7ff51030ad12ef5faf319,
proves smoothness, all smooth-norm moments, finite-jet ranks, literal
whole-field Gaussian kernels, all-Borel finite-incidence Rice identities,
and almost-sure Morse/distinct-critical-value behavior for (1). Its full
40231-byte proof and full 38035-byte accepted scoped review were read. Its
finite-incidence appendix was also read. Section 3 recalls exactly the
interfaces used here. Its fold conclusion is not an A4 premise.

Here is the new assertion. There exist a nonempty compact rectangular
parameter box U around (6,22,24), with coordinates (alpha,beta,q), a finite
R>0, and r_0>0, such that the actual ordinary finite superlevel-H0 elder
bars whose birth maxima satisfy the Borel sector mark in Section 2 have
expected lifetime measure per area

    M_A4(B)=V^-1 E N_A4(B),   B subset (0,infinity) Borel.

On a fixed interval (0,ell_0), this measure has the particular finite Borel
density given by (26), and

    nu_A4(ell) ~ C_A4 ell^(4/5),
    M_A4((0,t]) ~ (5/9) C_A4 t^(9/5),       ell,t -> 0+,              (3)

where 0<C_A4<infinity and the explicit contact coefficient is (28).
Every counted maximum dies at the farther of its two nearby saddles in the
selected direction, despite a nearer intervening saddle. The identification
is the genuine global elder death on X. It is not nearest-saddle pairing.

The mark retains bounded hard and mixed jets, a compact regular unfolding
box, a positive fifth ridge derivative, and a residual norm cutoff. Its
complement is NOT asserted negligible. In particular (3) is neither the
leading asymptotic of all bars nor the next term in their density. The
already admitted generic fold density is of order ell^(-1/3) for this same
law. Neither its exponent nor its coefficient is changed by (3).

## 2. The Borel sector at an actual birth maximum

Write J for counterclockwise rotation by pi/2. At a critical point x with
distinct negative Hessian eigenvalues write them (-lambda,a), with

    lambda>0,  -lambda>a,  a in [-2,-1].

For a unit soft eigenvector u put v=Ju. Use raw symmetric derivative
coordinates, one entry F_{u^i v^(n-i)} for each i=0,...,n, at each order
n=0,...,5. In particular, order zero is F, order one has two entries,
order two has three, and so on. This full 5-jet is a vector of dimension
1+2+3+4+5+6=21, denoted J_{x,u}F. Its entries are actual derivatives,
not derivatives divided by factorials. In this frame F_uv=0. Put

    gamma=F_uuv, eta=F_uuuv, B=F_uvv,
    T=F_uuu,
    Q4=F_uuuu-3 gamma^2/a,
    Q5=F_uuuuu-10 eta gamma/a+15 gamma^2 B/a^2.                       (4)

These are precisely the third, fourth and fifth derivatives of the
transverse maximizing ridge through x, as proved in Section 5. Q4 is not
the raw fourth derivative. Let zeta be the ordered list of the other twelve
entries of orders 3,4,5: exclude T,F_uuuu,F_uuuuu and retain every other
entry once. Thus gamma,eta,B are entries of zeta. Fix their block

    zeta in [-1,1]^12,      b=F(x) in [-1,1].                        (5)

Different fixed bounded boxes with nonempty interior would work. For
Q5!=0 exactly one of the two soft directions has Q5>0: reversal
(u,v)->(-u,-v) fixes even-order entries and negates odd-order entries,
so Q5 changes sign. Use this unique direction. Set

    r=-Q4/36,  alpha=lambda/r^3,  beta=T/r^2,  q=Q5.                 (6)

Require 0<r<r_0 and (alpha,beta,q) in U, where U is specified below.
At each x,u let Gamma_{x,u}=Cov(J_{x,u}F),

    c_{x,u}(y)=Cov(F(y),J_{x,u}F),
    H_{x,u}f=f-c_{x,u} Gamma_{x,u}^-1 J_{x,u}f.                     (7)

Require additionally ||H_{x,u}F||_C7<=R. Use any fixed increasing smooth
norm built from Euclidean tensor norms on X. Because the full jet transforms
invertibly under frame changes, the projection H is in fact independent
of the chosen orthonormal frame at x. The notation retains u to identify
the joint kernel used in the formulas. The residual cutoff is an actual
law-dependent Borel observable of the field, not an auxiliary independent
random variable and not a cutoff on a target-dependent total field norm.

All these tests are Borel. On the simple-eigenvalue locus the eigenline and
its two local unit lifts are continuous; finitely/countably many angle charts
and the sign test Q5>0 give a unique Borel lift. Formula (7) is a continuous
linear operation at each parameter and depends smoothly on x,u. Norms,
jet entries, and the rational expressions (4) are Borel on a<=-1.
The Morse/distinct-height locus is Borel, and (1) belongs to it almost
surely by G. On that locus every maximum has a unique birth label. Count
its actual ordinary finite elder bar if and only if this mark holds.
Set the count to zero on the null complement. The deterministic proof
below also specifies its lifetime without using conditional global Morse
genericity. No essential class can carry this mark, because an explicitly
constructed point has larger height than the birth.

## 3. Literal kernels and the one-point all-Borel Rice identity

All twenty-one jet coordinates are independent continuous linear functionals
on smooth functions: a polynomial times a cutoff prescribes any 5-jet at x.
Dense smooth span in (1) therefore implies positive definite Gamma_{x,u}.
Indeed a row annihilating all coefficient columns would annihilate every
smooth function; a finite subset of columns already spans R^21. Compactness
of X times S^1 and smooth covariance give positive covariance floors and
uniform bounds for Gamma^-1 and the global smooth norms of c Gamma^-1.
The resulting Gaussian density p_{x,u}(z) is positive, finite and smooth
in all finite variables. There is no independence assumption between
jet orders or entries.

For each literal jet value z define a whole-field conditional law by

    f_z=R_{x,u}+m_{x,u}(z),
    R_{x,u}=H_{x,u}F,  m_{x,u}(z)=c_{x,u}Gamma_{x,u}^-1 z.            (8)

The residual is a smooth centered Gaussian field independent of the full
jet; its own 5-jet at x is exactly zero. This formula specifies the kernel
at every z, including the degenerate limit below. It is not conditioning
on an event with positive probability. For clarity about Borel marks, G
derives its Rice identity from actual finite original coefficient minors.
Fix a smooth independent tail; solve the two critical equations for two
invertible original Gaussian coordinates; the incidence Jacobian is
|det Hess f| divided by the gradient-minor determinant. Ordinary finite
Gaussian fiber integration cancels that denominator. Equal-dimensional
smooth Sard, local inverse charts and ordinary change of variables give
the counting identity for every nonnegative Borel whole-field mark.
Integrate the smooth tails and sum a disjoint minor/chart partition.

The literal fiber agrees with (8), not just almost everywhere in z:
the tail receives its Bayes density p_block(z-J tail)/p_full(z), and the
remaining finite block its affine Gaussian kernel. Completing the joint
Gaussian square gives the regression characteristic function at EVERY
target. Countably many field evaluations generate the smooth Borel
sigma-field, so the resulting whole-field laws agree. Thus arbitrary
Borel marks transfer at the zero-gradient and full-jet targets used here.
No continuity of the elder indicator on a null fiber is required.

In particular the exact one-point identity, with height and higher-jet
disintegration, is

    E sum_{x: grad F(x)=0} w(x,F)
      = integral_X integral p_fixed(z) |det H|
             E[w(x,f_z)] d(non-gradient jet z) dx,                  (9)

where the two gradient entries of z are set to zero and the remaining
nineteen entries have raw Lebesgue measure. This follows equally by
disintegrating the one-point identity at gradient zero using the same
literal block/tail calculation. Its total unmarked integral is finite
by G's compact covariance floors and conditional Hessian moments.

The unconditional Morse/distinct-height statement is used only to identify
the original bar count almost surely. Under a literal degenerate limiting
jet the field need not be globally Morse. None of the global trapping or
density arguments assumes that it is.

## 4. Eigenframe and reduced-jet changes, with exact multiplicities

Let theta be the angle of u in a fixed oriented Euclidean frame. In raw
Hessian coordinates (H11,H12,H22),

    H=R_theta diag(-lambda,a) R_theta^T,
    |d(H11,H12,H22)/d(lambda,a,theta)|=|a+lambda|.                   (10)

For example at theta=0 the three derivative columns have diagonal entries
(-1,0,0), (0,0,1), and (0,-lambda-a,0); their determinant has absolute
value |a+lambda|. Conjugation by a plane rotation has determinant one
on the three raw symmetric entries, so the same formula holds at every
theta. This uses dH11 dH12 dH22, not an orthonormalized Frobenius volume.

Angles in [0,pi) count each soft eigenline once. We instead use theta in
[0,2pi) together with Q5>0. Exactly one of each antipodal pair satisfies
this condition, so this also counts once. There is NO additional factor
1/2. In the full jet, the SO(2) action on each Sym^n(R^2) has determinant
one: its determinant is a continuous homomorphism from the compact connected
circle to positive real numbers, hence one. The gradient rotation also has
determinant one. In the combined change of variables the theta derivatives
of the higher entries form only a lower off-diagonal block; (10) is
therefore the only frame Jacobian. The Rice weight at the maximum is

    |det H|=lambda(-a).                                             (11)

Keep b,a,zeta fixed. Changing the pure fourth/fifth entries to (Q4,Q5)
has absolute determinant one. The correction to F_uuuu in (4) depends
only on a,zeta; the correction to F_uuuuu also depends only on a,zeta.
Consequently the inverse target for (6) is

    F=b, (F_u,F_v)=(0,0),
    (F_uu,F_uv,F_vv)=(-alpha r^3,0,a),
    T=beta r^2,
    F_uuuu=-36r+3 gamma^2/a,
    F_uuuuu=q+10 eta gamma/a-15 gamma^2 B/a^2,
    remaining entries=zeta.                                       (12)

Denote this vector z_r and its r=0 value z_0. It is a smooth bounded
function of all parameters for 0<=r<=r_0 and a in [-2,-1]. The nonlinear
jet correction has not been replaced by a fictional independent Gaussian
law of Q4,Q5; the density is the full original joint p_{x,u}(z_r).

Finally,

    |d(lambda,T,Q4)/d(alpha,beta,r)|=36 r^5.                         (13)

Its columns have rows (r^3,0,3 alpha r^2), (0,r^2,2 beta r),
(0,0,-36), so the claim is exact. Combining (10)-(13), the density
before lifetime pushforward carries the precise factor

    36 alpha(-a)|a+alpha r^3| r^8 dr.                              (14)

It tends, after division by r^8, to 36 alpha a^2. There is one Rice
determinant and one spectral-coordinate Jacobian. No second Rice
determinant, independent saddle density, probability-normalized sphere
measure, or extra unordered-pair half is present.

## 5. Actual ridge derivatives and uniform conditional bounds

Let all compact parameters range as in (5), a in [-2,-1], and in a
sufficiently small closed rectangular U around (6,22,24). Its exact open
stability requirements are given in Section 6. From (8), all smooth-norm
moments of R_{x,u} are uniformly bounded over X times S^1. For instance
||R||_C7<=||F||_C7+C||F||_C5, with one finite constant. Choose R so large
that

    h(x,u):=P(||R_{x,u}||_C7<=R)>=1/2  for every x,u.                (15)

This follows directly from a uniform first-moment bound and Markov; no
small-ball or threshold-atom assertion is needed. The same residual is
used for EVERY r in (8), now with z=z_r. On the cutoff event the fields

    f_r=R_{x,u}+m_{x,u}(z_r)                                      (16)

and their r derivatives are bounded in C7 by one deterministic constant.
The residual distribution, the cutoff event, and its threshold do not
depend on r. All constants from now on are uniform over the compact
parameters and all residuals in this event, for this one fixed law.

Use embedded Euclidean coordinates (s,t) centered at x in frame (u,v).
There is a fixed small coordinate rectangle on which f_vv<=-1/2.
This follows from f_vv(0)=a<=-1 and the uniform C3 bound. Since f_v(0)=0
and f_uv(0)=0, the implicit equation f_v(s,h_r(s))=0 has a unique
smooth ridge on |s|<=rho, with

    h_r(0)=h'_r(0)=0,  |h_r(s)|<=C s^2.                           (17)

Existence with uniform bounds can also be seen without a parameterwise
implicit radius: f_v(s,0)=O(s^2), while f_v decreases in t with slope
at most -1/2; evaluate at t=+-C_1 s^2 and use the intermediate value
theorem. The implicit derivative formulas then give the uniform bounds
and smooth r dependence on a common rectangle. Shrink rho so that this
ridge stays inside it. Write g_r(s)=f_r(s,h_r(s)). Transverse strict
concavity implies f_r(s,t)<=g_r(s), and more quantitatively

    f_r(s,h_r(s)+z)<=g_r(s)-z^2/4                               (18)

whenever the displayed points stay in that rectangle.

At s=0 the exact derivatives are

    g_r(0)=b, g'_r(0)=0, g''_r(0)=-alpha r^3,
    g'''_r(0)=beta r^2, g''''_r(0)=-36r, g'''''_r(0)=q.              (19)

To verify the nonlinear entries rather than assume them, write
h_r(s)=c s^2+d s^3+O(s^4), c=-gamma/(2a). The coefficient of s^4 in
f(s,h(s)) beyond the pure fourth term is a c^2/2+gamma c/2
=-gamma^2/(8a), hence the fourth correction is -3 gamma^2/a.
At order s^5 the d terms cancel because ac+gamma/2=0; what remains
is eta c/6+B c^2/2=-eta gamma/(12a)+B gamma^2/(8a^2).
Multiplication by 120 gives exactly Q5 in (4). No lambda-dependent
term is missing, because f_uv(0)=h'(0)=f_v(0)=0.

The ridge is C6 in s under a C7 field bound and g'_r=f_u(s,h_r(s)),
so g_r is C7 with uniform bounds. Its parameter derivative satisfies
the envelope identity partial_r g_r=(partial_r f_r)(s,h_r(s)), because
f_v=0 on the ridge; this is C6 in s with uniform bounds. Taylor's
integral remainder therefore gives

    g_r(s)=b-alpha r^3 s^2/2+beta r^2 s^3/6
                -3r s^4/2+q s^5/120+E_r(s),
    |E_r^(j)(s)|<=C|s|^(6-j), j=0,1,2,
    |partial_r E_r(s)|<=C|s|^6.                                  (20)

The last inequality follows by Taylor-expanding partial_r g at zero;
its derivatives through order five are the derivatives of (19). The
same bounds for mixed derivatives needed below follow by differentiating
the integral remainder. In particular on every fixed bounded xi interval,

    r^-5(g_r(r xi)-b)=P_{alpha,beta,q}(xi)+O(r) in C2_xi,
    |partial_r [r^-5(g_r(r xi)-b)]|<=C,                           (21)

where

    P_{alpha,beta,q}(xi)=-alpha xi^2/2+beta xi^3/6
                              -3 xi^4/2+q xi^5/120.

The bounds in (21) hold also after one xi derivative of the r derivative,
as follows from E_s=O(s^5) and partial_r E_s=O(s^5).

## 6. A nonempty regular unfolding box and all nearby critical points

At (alpha,beta,q)=(6,22,24),

    P(xi)=xi^5/5-3xi^4/2+11xi^3/3-3xi^2,
    P'(xi)=xi(xi-1)(xi-2)(xi-3).                                  (22)

The maxima at 0,2 have heights 0,-4/15; the minima at 1,3 have heights
-19/30,-9/10. In particular the height order is

    P(3)<P(1)<P(2)<P(0)=0.

Choose a sufficiently small epsilon>0 and let U be the closed rectangular
box |alpha-6|<=epsilon, |beta-22|<=epsilon, |q-24|<=epsilon. Require:
alpha,beta,q positive; the three nonzero roots xi_1,xi_2,xi_3 of P'
are simple and lie respectively in (3/4,5/4), (7/4,9/4), (11/4,13/4);
all adjacent gaps in the preceding strict height order exceed 1/8;
and 1/2<L_0:=-P(xi_3)<3/2. These are finitely many open conditions
on coefficients at a polynomial with simple real roots. Their base
values satisfy them strictly, so such an epsilon exists and U has
positive three-dimensional volume. This defines an actual nonempty
compact sector; no numerical plot or probabilistic genericity is used.

For the exact g_r, (21) and the implicit-function theorem give roots
0,s_1(r),s_2(r),s_3(r), with

    s_i(r)=r[xi_i+O(r)],
    b>g_r(s_2)>g_r(s_1)>g_r(s_3),
    Delta(r):=b-g_r(s_3)=r^5 L_r,
    L_r=L_0+O(r),  |partial_r L_r|<=C.                            (23)

All these estimates are uniform on the compact boxes and residual cutoff.
To justify the derivative bound, the scaled reduced functions in (21)
have bounded r derivative in C1, and their three roots have uniformly
nonzero derivative in xi. Their roots therefore have bounded r
derivatives. At a critical root differentiation of the critical value
has no root-motion term, so the same bound follows for L_r.

There are exactly these four critical points in the whole fixed ridge
interval [-rho,rho], once r_0 is small. Here is the needed exclusion,
which local root perturbation alone would not prove. For s<0 the four
displayed terms of

    g'_r(s)=-alpha r^3 s+(beta/2)r^2s^2-6rs^3+(q/24)s^4+O(s^5)

are positive. Shrink rho so the remainder is at most q_min |s|^4/96;
then g'_r(s)>0 on [-rho,0). For s>=C_2 r choose a fixed C_2>4 so large
that 6/C_2+alpha_max/C_2^3<q_min/48. The positive beta term may be
discarded; the same remainder estimate gives g'_r(s)>0 up to rho.
On the compact scaled interval [0,C_2], (21), the simple roots of P',
and a positive derivative floor away from small disjoint root intervals
give exactly the three stated positive roots and the anchored root 0.
Near zero use the derivative floor of P' itself, P''(0)=-alpha<0.
There are no others. The transverse equation has exactly the one ridge,
so these are all critical points in the coordinate tube.

The same Taylor expansion at fixed endpoints, after shrinking rho and
then r_0, yields uniform constants c_0>0 with

    g_r(-rho)<=b-c_0 rho^5,  g_r(rho)>=b+c_0 rho^5.                 (24)

At r=0 the leading quintic has these signs; its remainder is O(rho^6),
and the r-dependent lower terms tend uniformly to zero at fixed rho.
The critical signs are maximum at 0, saddle at s_1, maximum at s_2,
saddle at s_3, because the transverse Hessian is negative and the
reduced second derivatives alternate. Inertia follows from the Hessian
Schur complement g'' on the ridge. All four are nondegenerate for r>0.

## 7. A physical enclosure and the actual global elder death

Choose a fixed delta>0 small enough that the curved tube

    D_r={ (s,t): -rho<=s<=s_3(r), |t-h_r(s)|<=delta }

is inside the embedded rectangle with transverse concavity. All choices
can be made uniformly: (17) keeps the ridge O(rho^2) from the axis;
one may first choose the transverse rectangle, then rho, then a fixed
delta, for example a sufficiently small positive multiple of rho^2.
It need not shrink with r. Decrease r_0 until

    Delta(r)<min(c_0 rho^5/2,delta^2/8).

On the left face, f<=g(-rho)<b-Delta; on both side faces, (18) and
max_{[-rho,s_3]}g=b give f<=b-delta^2/4<b-Delta; on the right face,
f<=g(s_3)=d_r:=b-Delta, with equality only on the ridge. Thus the
entire boundary of D_r has height at most d_r. Its entire interior
has height at most b. The point M=(0,0) has height b and lies inside.

Every continuous path from M to ANY point of height greater than b
must leave D_r and hence cross its boundary at height <=d_r. This
is a purely global assertion: no detour elsewhere on the torus can
avoid that boundary. On the other hand the actual ridge path from
s=0 to s=rho reaches P=(rho,h_r(rho)) with height greater than b by
(24). Its minimum is d_r: the intervening first saddle has strictly
higher height, and there are no further critical points before rho.
For every c<d_r this is a path in {f>c} to a point higher than b.

Define the intrinsic elder threshold of a point at height b by the
supremum of rational c<b for which it is connected in {f>c} to a
point of value >b. Connectivity is Borel using countable chains of
small basis balls whose closure minima exceed c. The boundary argument
gives threshold <=d_r, and the ridge path gives threshold >=d_r.
Consequently the intrinsic threshold is EXACTLY d_r on every field
(16) under the residual cutoff, even if remote critical points are
degenerate or share heights. No unconditional-Morse statement has
been applied to a conditional field.

For the original Gaussian field, which is Morse with distinct critical
values almost surely, classical H0 elder linear algebra identifies this
threshold with the unique ordinary finite bar death of M. It is the
actual index-one saddle at s_3. The saddle at s_1 is closer in physical
distance, since s_1/r tends to a number near one and s_3/r to one near
three; ridge offsets are O(r^2). It does not kill M. Its two incident
local components have maxima M and the lower maximum at s_2; at this
earlier level the lower maximum dies. This can also be seen directly
by enclosing the s_2 maximum between the gate s_1 and a point between
s_2,s_3 whose ridge height is below g(s_1), with the same transverse
side walls. The ridge reaches M at height at least g(s_1), giving its
death g(s_1). Thus the profile is an actual global selector counterexample
to assigning each maximum to its nearest saddle, not merely an algebraic
ordering of candidate roots.

Only the birth at M is selected by the sector (6): for the other maximum
the third and fourth jet relations would have to be tested afresh, and
it is not counted a second time for M's bar. The unique birth labeling
and the unique Q5>0 soft orientation are the once-counting rules.

## 8. Exact actual-bar measure and the density pushforward

Let K be the product of the boxes for b,a,zeta and U, with Lebesgue
measure db da dzeta d alpha d beta dq. Use ordinary arc length dtheta
on S^1, of total mass 2 pi, and dx on X. Let mu_{x,u} be the actual
Gaussian residual law in (8), and write A_R={||R||_C7<=R}. The repeated
letter R in this event means the fixed cutoff constant on the right;
inside integrals the residual is denoted omega to avoid ambiguity.
The exact one-point identity (9), changes (10)-(14), and the deterministic
death identification give, for every Borel B subset (0,infinity),

    M_A4(B)=(36/V) integral_{X,S^1,K} integral_0^r0
      alpha(-a)|a+alpha r^3| r^8 p_{x,u}(z_r)
      integral 1{||omega||_C7<=R} 1{Delta(r,omega) in B}
                        mu_{x,u}(d omega) dr dK dtheta dx.          (25)

This is a measure of actual ordinary bars. The inner lifetime is not
an artificial sampled normal-form amplitude; it is the proved global
death difference of the conditionally coupled actual Gaussian field.
The root and its value are jointly Borel (indeed continuous on the
bounded local fields) by the uniform simple-root construction. Every
operation in (25) therefore permits Tonelli for nonnegative marks.

Decrease r_0 again. From (23), uniformly,

    Delta'(r)=r^4(5 L_r+r partial_r L_r)>0,
    0<c<=L_r<=C,   0<c<=5 L_r+r partial_r L_r<=C.

In particular min Delta(r_0,omega)>0 uniformly in all marks and cutoff
residuals. Choose ell_0 below this positive lower bound. For each
0<ell<ell_0 and each such mark/residual, there is exactly one inverse
r_ell in (0,r_0), with Delta(r_ell,omega)=ell. Ordinary one-dimensional
change of variables on every fiber of (25) gives the Borel density

    nu_A4(ell)=(36/V) integral_{X,S^1,K} integral_{||omega||<=R}
      alpha(-a)|a+alpha r_ell^3| p_{x,u}(z_{r_ell})
      [r_ell^4/(5 L_{r_ell}+r_ell partial_r L_{r_ell})]
                                   mu_{x,u}(d omega) dK dtheta dx. (26)

No derivative of a cumulative asymptotic is taken. The fourth power
in (26) is the exact r^8/Rice mass divided by the r^4 lifetime derivative.
The representative is finite for every ell in this interval by compact
marks, uniform covariance floors, and the displayed lower bounds.

Since ell=r_ell^5 L_{r_ell},

    r_ell^4/ell^(4/5)=L_{r_ell}^(-4/5),
    r_ell ->0 uniformly,  r_ell=O(ell^(1/5)).                       (27)

Every other factor in the integrand of ell^(-4/5)nu_A4 converges uniformly
over marks and cutoff residuals to its r=0 value. For example the density
is uniformly smooth on the compact set of z_r, and L_r-L_0=O(r),
while the denominator tends uniformly to 5L_0. For varying x,u, integrals
may be written using the single original field F and omega=H_{x,u}F;
this supplies a joint Borel kernel and an ordinary fixed probability
space for dominated convergence. There is no assertion that a varying
norm-cutoff boundary has zero probability; its event is fixed in r.
All limiting factors except the indicator are independent of omega.
Thus the coefficient in (3) is exactly

    C_A4=(36/(5V)) integral_{X,S^1,K}
        alpha a^2 L_0(alpha,beta,q)^(-9/5)
        p_{x,u}(z_0(b,a,zeta,q)) h(x,u)
                                     dK dtheta dx.                (28)

The notation z_0 retains its full twenty-one entries from (12), with
the gradient, soft Hessian, T and Q4 pins equal to zero in reduced
coordinates, and Q5=q. The raw fourth/fifth entries retain their mixed
jet corrections. No factorization of this joint Gaussian density is
asserted. The universal scalar 36/5 comes from the chosen definition
r=-Q4/36 and the fifth-order height map; it is not a universal numerical
coefficient for every differently normalized A4 sector.

The integration domain is compact with positive finite Lebesgue measure.
The full joint Gaussian density has a positive lower bound on its compact
target set, alpha>0, |a|>=1, L_0 is bounded above and below, and h>=1/2.
It follows directly that 0<C_A4<infinity. Uniform bounds in (26)-(27)
give an integrable fixed bound after dividing by ell^(4/5), proving (3).
In fact they give the law/sector-dependent estimate

    nu_A4(ell)=C_A4 ell^(4/5)+O(ell),       ell ->0+,                (29)

because all remaining errors are uniformly O(r_ell). This estimate is
only for this fixed marked sector. Integrating the density asymptotic
yields (5/9)C_A4 t^(9/5). Equation (25) also gives that power directly
from r^8 dr. Density power 4/5 and cumulative power 9/5 are distinct.

## 9. Exclusions and why this is not a whole-density correction

Every bound above is uniform over exactly the stated compact marks and
the fixed residual cutoff. The proof excludes, rather than declares
negligible, the following regions:

* Fold/cusp discriminants: U stays a positive distance from multiple
  roots, root collisions and critical-height ties. Other scaled unfoldings
  can change the elder partner and can dominate a whole-population term.
* Vanishing fifth ridge derivative: q stays near 24, in particular away
  from zero. No sixth-order contact admission or matching is supplied.
* A second soft Hessian direction: a lies in [-2,-1]. No small-hard-
  eigenvalue tail bound or higher-corank singularity law is supplied.
* Large height, mixed jets and residual norms: all have the fixed bounds
  in (5), Section 5 and U. Gaussian tails make ordinary moments finite,
  but do not by themselves prove that the omitted sectors are smaller
  than ell^(4/5) in a matched whole-density expansion.
* Other homology degrees, other dimensions or curved geometries, and
  convergence of point processes or higher factorial moments are not
  claimed here. The geometric proof explicitly uses a two-dimensional
  ridge and a single hard transverse direction.

The theorem is not vacuous after these restrictions: (15) gives at least
half of every literal residual law, the finite target density is uniformly
positive, the sector has positive finite-dimensional volume, and (28) is
strictly positive. It is an actual Gaussian higher-singularity population
inside a field whose leading generic-bar law is already known. It supplies
a concrete taxonomy entry and a falsification of nearest-saddle selection;
it does not substitute for matching the rest of the taxonomy.

As a diagnostic only, a potential A_k with height r^(k+1), control weights
k-1,...,1 on derivatives 2,...,k, and a one-point Rice weight r^(k-1)
would have radial cumulative degree (k-1)(k+2)/2. The corresponding formal
cumulative prediction is k/2-1/(k+1), giving 2/3,5/4,9/5 for k=2,3,4.
This is not a general A_k theorem: observation changes, corank, selection,
and complements must be proved separately. For k=4 those ingredients
have been proved above only on this regular compact sector.

## 10. Classical imports, source custody, and evidence boundary

The conventional mathematical imports are finite-dimensional inverse and
implicit function theorems, Taylor's integral remainder, Euclidean plane
coordinate changes, elementary finite Gaussian regression and uniqueness,
Tonelli and dominated convergence, and ordinary finite-dimensional change
of variables. The one-point all-Borel identity and original Morse/distinct-
height facts are imported from the exact fully read G proof, which derives
them using finite original coefficient minors, smooth equal-dimensional
Sard, and ordinary smooth incidence area change of variables. The global
H0 interpretation uses the classical Morse level/handle and elder linear
algebra package already explicit in G. The threshold enclosure itself was
proved for every conditional cutoff field and does not import a stochastic
global-selector hypothesis.

The earlier Math240 fifth-order ridge correction was inspected only in
its setting/notation and equation (0.1); this source is not imported as an
A4 theorem. The corrections (4) were independently reconstructed here.
The scout identifies actual older A3 results and prevents claiming them as
new. It is an ownership/source survey, not mathematical acceptance of this
proposal. Exact input copies, SHA256 identities and read extents are in
INPUT_MANIFEST.json. The focused contributor's complete derivation is an
author contribution, not independent review. New exact controls check the
polynomial heights/derivatives, the two Jacobians, nonlinear ridge
corrections, exponent ledger and refusal cases. Those controls are finite
algebra checks, not a random-field experiment or proof of asymptotics.

No old control suite was rerun. No field realization, numerical Rice
integration, coefficient enclosure, sampler/grid qualification, Lean command,
kernel audit, source-branch edit, remote mutation or scientific promotion
was performed for this author unit. The source is a local conventional
proof proposal until the separate exact-source review. No provider-distinct
acceptance, blind50-model validation, Hk theorem, manuscript acceptance,
external uptake, or institutional adoption follows. The larger research
goal remains ACTIVE / UNMET.
