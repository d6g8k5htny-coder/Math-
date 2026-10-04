# A typical ordinary fold is the only possible short-bar pair

Object: OA-ORDINARY-FOLD-ISOLATION-20261001-v1.
Authors: OpenAI/Codex root and c52_fold_feasibility, under Dylan Roy's delegation.
This is an analytic candidate with the exact retained source interfaces below.
It is coauthor work, not an independent review or a scientific-status change.

## 1. The observable and the precise new lemma

Fix the planar torus T_L²=R²/(LZ²), with L>0 fixed, and exactly the centered,
unit-variance periodized Gaussian covariance in [P, §1]. Keep the ordinary
finite SUPERLEVEL H0 convention of [P, §8], with the essential global-maximum
class excluded. Write K_tau(f) for the number of such bars whose lifetime is
in (0,tau]. On the Morse/distinct-critical-value locus it is finite; assign
K_tau=0 outside that locus. No spatial, birth-height, gap-mark or witness
restriction is imposed on this count.

Fix b in R, k>0 and an orthonormal planar frame R=(u,e_z). Work in its local
coordinates (x,z), centered at the midpoint. Choose all sufficiently small
r>0 below the embedding radius in [REC, §1]. The exact pins are

    M_r=(-r/2,0), S_r=(r/2,0),
    f(M_r)=b, f(S_r)=b-k r³, grad f(M_r)=grad f(S_r)=0.

Let Q_r=Q_(r,b,k,R) be the whole-field Gaussian regression law at these six
observations. Its typed determinant weight is the unchanged parent weight

    W_r=|det H_(M_r) det H_(S_r)|
          1{H_(M_r)<0, index(H_(S_r))=1},

where index counts negative eigenvalues. This file does not replace W_r by
an unweighted pin probability or by a good-event normalizer.

**Lemma F (ordinary-fold isolation).** There is an explicit coupling F_r
of Q_r, together with its six-contact-jet limit F_0, such that:

1. F_r converges almost surely to F_0 in C4(T_L²) as r decreases to zero.
   The limit obeys

       (F_0,F_0,x,F_0,xx,F_0,xxx,F_0,z,F_0,xz)(0)
                    =(b,0,0,12k,0,0).                  (F1)

2. Put A=F_0,zz(0). Almost surely on {A<0}, the only critical points of
   F_r in one fixed neighborhood of the origin, for all sufficiently small
   r, are M_r and S_r. Every other critical point continues from a finite
   collection of nondegenerate critical points of F_0. Their limiting values
   are pairwise distinct and all different from b.

3. For each fixed y in (0,1], put tau(r)=k r³/y. Almost surely on {A<0},

       K_(tau(r))(F_r)<=1 eventually as r->0.             (F2)

   On the entire coupling space,

       (W_r(F_r)/r²) 1{K_(tau(r))(F_r)>=2}->0
                         almost surely.                (F3)

The neighborhood and the small-radius threshold may depend on the complete
coupled sample, b,k,R,y. No uniform samplewise threshold, rate, growing-volume
limit, or higher-dimensional assertion is made. In (F2) even the identity of
the local pins as actual elder partners is unnecessary: they are the only
possible endpoints of a short finite bar. Positive mean intensity and actual
elder selection remain the separate retained inputs used by PROOF.md.

The same pathwise argument works for any deterministic tau(r)->0. The displayed
choice is the one required when integrating ordinary lifetimes ell=tau y and
the exact pair mark k=ell/r³.

## 2. Exact retained interfaces

The source identities are those fixed by the companion SOURCES.json. The
parent [P] is read together with [CAP,E1,E2,REC], as required by [REC, §1].
In particular its endpoint congruence is the corrected diag(r^(-1/2),1),
and E2 replaces the parent's original §9. The use in this lemma is narrower
than an acceptance or re-proof of the complete source chain.

- [P, §2] gives a smooth Fourier realization on the compact torus, all finite
  moments of global derivative suprema, and linear independence of distinct
  derivative evaluations at distinct sites. Its proof uses every positive
  Fourier coefficient, not a finite spectral sample.
- [P, §3] gives the exact six-row desingularization U_r, its target v_r, and
  positive contact covariance. Appending f_zz(0) gives a positive covariance
  because it is a distinct jet entry.
- [R, §2, R2–R4] gives the same whole-field regression coupling and its smooth
  covariance convergence. The pathwise convergence needed here is proved
  directly below from that regression formula and the averaged functionals;
  it is not inferred from Lp convergence alone.
- [P, §8] supplies the finite-dimensional rank plus overdetermined mesh method.
  Section 4 below checks its covariance hypotheses at the new contact law,
  including both kinds of critical-value separation.
- [P, §5] with [E1] supplies the endpoint determinant scale and conditional
  moments. The endpoint type boundary is also addressed directly in §7.
- [P, §8; E2, §9.4; P, §14] specify the ordinary global elder observable:
  every finite bar has one maximum birth and one distinct merging-saddle
  death. A local ascending branch is not substituted for that global mark.

Neither the C50/C51 replacement-bar theorem nor a double-soft cubic cluster
limit is used as an analytic premise. Those concern a different population.

## 3. Global smooth coupling at an ordinary six-pin contact

For a=-r/2 and c=r/2, [P, §3] defines U_r by the four axial rows

    (f(a,0)+f(c,0))/2,
    (f(c,0)-f(a,0))/r,
    (f_x(c,0)-f_x(a,0))/r,
    (6/r²)[f_x(a,0)+f_x(c,0)
                         -2(f(c,0)-f(a,0))/r],

followed by the two transverse rows

    (f_z(a,0)+f_z(c,0))/2,
    (f_z(c,0)-f_z(a,0))/r.

Its exact target and limit are

    v_r=(b-k r³/2,-k r²,0,12k,0,0),
    U_0=(f,f_x,f_xx,f_xxx,f_z,f_xz)(0),
    v_0=(b,0,0,12k,0,0).                                (F4)

For a smooth unconditioned field F, write

    Sigma_r=Cov(U_r(F)), C_r(q)=Cov(F(q),U_r(F)),
    F_r(q)=F(q)+C_r(q) Sigma_r^(-1)(v_r-U_r(F)).          (F5)

Use the same underlying F for every r, and the analogous expression at r=0.
Gaussian regression proves law(F_r)=Q_r. Applying U_r to (F5) shows that the
pins hold exactly, because U_r(C_r)=Sigma_r. There is no artificial independent
field introduced for the remote part of the torus.

Here is a pathwise justification for the limit. For every deterministic
smooth F, each row of U_r(F) tends to its row of U_0(F). For the fourth row,
Taylor expansion on the centered interval gives

    F_x(a,0)+F_x(c,0)=2F_x(0)+(r²/4)F_xxx(0)+o(r²),
    2(F(c,0)-F(a,0))/r=2F_x(0)+(r²/12)F_xxx(0)+o(r²),

and their difference times 6/r² tends to F_xxx(0). Equivalently this row
is an averaged third derivative with a bounded integral kernel, as in [P, §3].
The apparent negative powers of r therefore cause no pathwise discontinuity.

The positive and rapidly decreasing Fourier spectrum in [P, §2] permits
termwise differentiation of the covariance to every fixed finite order.
Consequently C_r->C_0 in global C4, Sigma_r->Sigma_0, and Sigma_r^(-1)
converges because Sigma_0 is positive definite. Together with (F4), passing
to the limit term by term in (F5) proves

    ||F_r-F_0||_(C4(T_L²))->0                           (F6)

on the probability-one event that F is smooth. This is convergence of the
whole continuous family as r->0, not just convergence along one subsequence.
It is asserted for each fixed b,k,R; a common probability-one set over all
uncountably many target laws is not required.

The limiting field has the regression law at U_0=v_0 and satisfies (F1).
The conditional variance of A=F_0,zz(0) is strictly positive: adjoining f_zz
to the six entries of U_0 is an independent list by [P, §2]. Thus A has a
nondegenerate scalar Gaussian density, in particular P(A=0)=0. Correlations
between A and the remaining field are retained.

## 4. Conditional genericity of all remote critical points and values

All assertions in this section concern the contact-conditioned law of F_0
at a fixed b,k,R. The forced degenerate critical point at 0 is excluded from
the remote domains.

First, at x!=0 and |v|=1 consider

    Z_M(x,v)=(grad F_0(x),H F_0(x)v) in R4.              (F7)

Its conditional covariance is positive definite. Otherwise a nonzero linear
combination of these four functionals would lie in the Gaussian L2 span of
U_0. With the positive Fourier spectrum, subtracting this contact combination
gives a distribution of derivative evaluations whose every Fourier coefficient
is zero. The distribution is therefore zero. Its supports x and 0 are
disjoint, so its part at x must vanish. The first-derivative and second-
derivative orders cannot cancel. The symbol for the latter is
`(beta dot xi)(v dot xi)`; since v!=0, it vanishes identically only if beta=0.
The first-derivative coefficients then vanish also, a contradiction.

For two distinct points x,z both different from 0 consider

    Z_V(x,z)=(grad F_0(x),grad F_0(z),
                              F_0(x)-F_0(z)) in R5.    (F8)

The same covariance argument applies. At support x a putative zero
distribution has an order-zero coefficient lambda and its two independent
first-derivative coefficients. They all vanish; this gives lambda=0 and
then the two first-derivative coefficients at z vanish. None can be canceled
by the observations supported at 0. Thus the residual covariance is positive.

To exclude a critical value equal to the contact birth b use

    Z_b(x)=(grad F_0(x),F_0(x)-b) in R3, x!=0.           (F9)

The constant b changes the mean, not the covariance. The three remote jet
entries are linearly independent modulo U_0 by the same disjoint-support
argument, so the covariance is again positive definite.

For completeness, the zero-exclusion step is as follows. Exhaust these
parameter domains by countably many compact sets with positive distance
from 0 and, for (F8), from x=z. Cover the unit circle in (F7) by finitely
many coordinate charts. On each compact chart, covariance continuity and
positivity give a uniform upper bound for the Gaussian density of each
Z-map. Its conditional mean has no effect on that density upper bound.

If a random C1 map from a compact q-dimensional chart to Rp has a zero and
its C1 norm is at most M, one of O(epsilon^(-q)) points in an epsilon-mesh
has image of norm at most C M epsilon. The probability at each mesh point
is at most C'(M epsilon)^p by the bounded density. The union bound therefore
gives C'' M^p epsilon^(p-q), which tends to zero whenever p>q. Fix M first,
then take the countable union over integer M. Smoothness makes the random
C1 norm finite. No independence among mesh values is assumed.

In (F7), (F8) and (F9), respectively, (q,p) is (3,4), (4,5), and (2,3).
The compact exhaustion therefore proves, almost surely:

- every off-origin critical point of F_0 is nondegenerate;
- two distinct off-origin critical points have different values;
- no off-origin critical point has value b.             (F10)

These are statements about the actual smooth contact-conditioned field.
They do not follow merely from nonsingularity at a finite set of sampled
locations. They remain valid on intersection with {A<0}, without imposing
an independent law on the remote field.

## 5. A complete local ridge and exactly two pinned critical points

Fix one sample satisfying (F6), (F10), and A<0. Set a0=-A>0. By continuity,
choose a coordinate rectangle around 0 on which

    F_0,zz <= -a0/2.

First choose a sufficiently small transverse half-width eta>0 inside that
rectangle. Since F_0,z(0)=F_0,xz(0)=0, shrinking an axial half-width delta>0
ensures |F_0,z(x,0)|<=a0 eta/8 for |x|<=delta. Integration in z then gives
strict opposite signs on z=-eta and z=eta, with a margin at least
3 a0 eta/8. By global C4 convergence, for all small enough r,

    F_r,zz <= -a0/4,
    F_r,z(x,-eta)>0>F_r,z(x,eta), |x|<=delta.             (F11)

It follows by the intermediate-value theorem and strict decrease in z that,
for every |x|<=delta, exactly one z=psi_r(x) in (-eta,eta) solves F_r,z=0.
The implicit-function theorem gives psi_r in C3. The uniform derivative
floor in (F11), uniform convergence of the derivatives of F_r through order
four, and implicit differentiation give

    psi_r->psi_0 in C3([-delta,delta]).                  (F12)

For example psi_r'=-F_r,xz/F_r,zz on the ridge. The formulas for the next
two derivatives have bounded denominators consisting of powers of F_r,zz
and numerators formed from derivatives through order four. Uniform convergence
of the roots follows first from strict monotonicity and uniform convergence
of F_r,z, and these formulas then prove (F12). Thus the assertion holds on
the entire fixed interval, not merely near a single point.

Define the reduced scalar function and its tangent by

    g_r(x)=F_r(x,psi_r(x)), v_ridge=(1,psi_r'(x)).

Here v_ridge is not the pin-target vector v_r from (F4). Along the ridge,

    g_r'=F_r,x,
    D²F_r[v_ridge,e_z]=d(F_r,z(x,psi_r(x)))/dx=0.

The chain rule through third order yields the exact identity

    g_r'''=D³F_r[v_ridge,v_ridge,v_ridge]
               +3D²F_r[v_ridge,(0,psi_r'')]
               +DF_r[(0,psi_r''')]
            =D³F_r[v_ridge,v_ridge,v_ridge].             (F13)

The last two terms vanish by the displayed ridge identities. At the limit
origin, psi_0(0)=0 and psi_0'(0)=-F_0,xz(0)/A=0, so

    g_0'(0)=g_0''(0)=0, g_0'''(0)=12k>0.                (F14)

Shrink delta again if necessary so that g_0'''>=9k on the whole interval.
Equations (F6),(F12),(F13) then give g_r'''>=6k there for all small r. The
function g_r' is therefore strictly convex. Both exact gradient pins lie
in the rectangle, and transverse uniqueness implies

    psi_r(-r/2)=psi_r(r/2)=0,
    g_r'(-r/2)=g_r'(r/2)=0.

A strictly convex function has at most two distinct zeros: if it had three,
the middle zero would lie strictly below the chord between the outer two,
which is zero, a contradiction. Hence these are the only zeros of g_r'.
Every critical point of F_r in the rectangle lies on the ridge, so the two
pins are the only local critical points. This controls all intermediate
spatial scales within a fixed neighborhood at once; no gap between a ball
of radius O(r) and a fixed-radius region is omitted.

Their types can also be checked without a normal-form approximation.
Strictly increasing g_r'' and the equality of g_r' at its two zeros imply

    g_r''(-r/2)<0<g_r''(r/2).

On the ridge the Hessian Schur complement of its negative transverse entry is

    F_r,xx-F_r,xz²/F_r,zz = g_r''.

Thus M_r has negative definite Hessian, and S_r has one negative and one
positive eigenvalue. Both are nondegenerate. This concerns Hessian type,
not the global elder matching.

At r=0, (F14) and g_0'''>0 imply g_0'(x)>0 for every nonzero x in the same
interval: integrate the sign of g_0'' from its zero at 0 on either side.
Consequently 0 is the only critical point of F_0 in the fixed rectangle.

## 6. Complete global root exhaustion and critical-value separation

Choose a smaller closed coordinate box V strictly inside the rectangle
from §5, containing 0 in its interior. The limit has no other critical point
in the larger rectangle, so in particular its gradient is nonzero on the
boundary of V. All critical points of F_0 outside the interior of V are
nondegenerate by (F10). There are finitely many: an infinite sequence in this
compact set would have a critical accumulation point there, contradicting
isolation of a nondegenerate critical point. Name them p_1,...,p_m.

Choose disjoint small closed coordinate balls B_j around the p_j, all outside
V, such that the Hessian in each is uniformly close to the invertible matrix
H_j=H F_0(p_j). By C2 convergence the same is true for F_r. The map

    q -> q-H_j^(-1) grad F_r(q)

is a contraction on a sufficiently small fixed B_j, mapping it into itself
for all small enough r: its derivative norm is uniformly below one, and
its value at p_j approaches p_j. The contraction principle supplies exactly
one critical point p_j(r) in B_j, with p_j(r)->p_j. The same Hessian estimate
also makes this root nondegenerate.

On the compact complement of the interiors of V and the B_j, the limiting
gradient has a positive minimum. Uniform C1 convergence excludes any F_r
critical point there for small r. Section 5 already exhausts the roots in V
by the two exact pins. Hence the complete critical set of F_r, eventually,
is exactly

    {M_r,S_r,p_1(r),...,p_m(r)}.                         (F15)

This includes neighborhoods of every chosen boundary; there is no unexamined
boundary layer between the local and remote parts of the domain.

Let v_j=F_0(p_j). By (F10), the finite set of numbers

    {|v_j-b|:1<=j<=m}
       union {|v_j-v_i|:1<=i<j<=m}

contains only strictly positive entries. Let Delta be the minimum of these
entries and 1; if there are no entries, set Delta=1. Smooth convergence and
root convergence imply F_r(p_j(r))->v_j. Both pinned values approach b,
and their positive difference is exactly k r³. For all sufficiently small r,
every absolute difference of two critical values involving at least one
remote critical point is at least Delta/2. The only remaining difference
is that of the two local pins. In particular F_r is then Morse and has
distinct critical values, including at the pins.

If tau(r)->0, then eventually tau(r)<Delta/2. Every finite ordinary superlevel
H0 bar has distinct critical endpoints and lifetime equal to its birth value
minus its killing-saddle value, by the retained convention. Thus any bar of
lifetime in (0,tau(r)] would have to use the two local pins as endpoints.
There is only one local maximum and one local saddle, and a maximum births
at most one H0 bar. Therefore K_(tau(r))(F_r)<=1. This proves (F2).

No continuity of the remote persistence pairing was needed: the exclusion
uses all remote critical-value differences, so any possible remote matching
is covered. Nor was a local saddle silently declared to be the global elder
partner. If the local pair is not an actual finite bar, the count is zero,
which still satisfies the bound.

## 7. The typed boundary and the weighted vanishing statement

On {A<0}, (F2) makes the event in (F3) identically false for all sufficiently
small r. This is an eventual statement, so no rate or bound on the random
threshold is needed to obtain pointwise vanishing.

On {A>0}, global C2 convergence gives F_r,zz(M_r)->A>0. A negative definite
Hessian must have negative value on the transverse coordinate vector. Hence
the maximum-type indicator in W_r is zero for every sufficiently small r;
again the expression in (F3) is identically zero eventually. The remaining
event A=0 is null, as proved in §3. No estimate on a thin neighborhood of
A=0 is silently inferred from this null-set fact.

This proves (F3) almost surely. It can also be integrated at fixed b,k,R,y.
Indeed [P, (4.1),(5.1),(5.3)] gives a uniformly bounded moment of W_r/r² of
some order greater than one on a compact parameter neighborhood of these
fixed targets. The bounded event factor preserves uniform integrability.
Almost-sure convergence plus uniform integrability therefore gives

    E[(W_r(F_r)/r²) 1{K_(k r³/y)(F_r)>=2}]->0.           (F16)

Multiplication by the bounded actual elder indicator does not change this
conclusion. Formula (F16) is an UNNORMALIZED weighted expectation, not a
quotient requiring a target-uniform positive lower bound for Z_r. The
removal of all b,k,y cutoffs uses the independent unnormalized intensity
majorant and off-diagonal estimate in PROOF.md. This lemma itself asserts
no rate of convergence in (F16), no global factorial moment, and no Poisson
or spatial-independence statement.

## 8. What the proof does and does not identify

The new analytic input is isolation of an ordinary fold together with the
absence of a second vanishing critical-value gap anywhere else in the same
conditioned field. Positivity of the transverse Gaussian density, complete
ridge root exhaustion, and remote critical-value separation are all used.
Merely separating remote critical-point positions would not suffice.

The bound counts actual ordinary short finite bars in one field. It is not
a uniqueness theorem for nearby auxiliary witnesses, rejected candidate
saddles, ascent trajectories or critical points in a shrinking height window.
It does not supersede a historical witness-localization or RN/24-jet node.
The existing parent selection theorem supplies any needed identification of
the selected mean persistence intensity; no new global elder theorem is
asserted by replacing that input with (F2).

The limit is fixed L, fixed b,k,R first, with the exact lifetime substitution
tau=k r³/y at fixed y>0. All exceptional-set assertions are for each such
law; integration over targets is handled by measurability and domination in
the consumer. There is no exchange with L->infinity, no numerical radius
threshold, and no extension of the present planar lemma to other dimensions.
