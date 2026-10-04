# Isolation of a single selected maximum in the full-field coupling

Object: OA-SELECTED-BAR-OCCURRENCE-GLOBAL-20261001-v1.
Author/coauthor: OpenAI/Codex `/root/c51_excess_feasibility`, under the
delegation of `/root` and Dylan Roy. Same-provider author-side mathematical
work; no independent-provider or organizational-independence credit.
Scientific effect NONE. This is an additive conditional proof candidate;
no imported hypothesis, acceptance, status, prize, premise, C8 conclusion,
or program closure is changed.

## 1. Scope and exact source interfaces

Use the fixed planar torus and exact covariance of [P] §1. The seven
retained source files [P], [CAP], [E1], [E2], [REC], [CUB], [ELDER] have the
same bytes as C50 `SOURCES.json`, pinned at Math commit
`044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43`. They remain imported hypotheses,
read with [REC]'s W1/embedded-chart rule, [E1]'s congruence erratum, and
[E2]'s Section 9 replacement. No new analytic input is silently substituted.

The specific interfaces used below are:

* [P] §§2–3: strictly positive Fourier spectrum, smooth full-field version,
  finite derivative-functional rank, and convergent averaged contact
  functionals. Its §8 supplies the rank-plus-mesh proof method; the
  full-contact-jet adaptation is proved explicitly below.
* [CUB] (C1)–(C13), (G6)–(G9): the exact cubic, nonsingular appended
  ten-dimensional jet covariance, full-field regression coupling, global
  C4 envelope, and fixed-disk rescaled C2 convergence.
* [ELDER] §4: the homogeneous cubic gradient has no nonzero zero off Delta;
  the elementary calculation is repeated below.
* C50 `ROOTS.md` R1: finite all-root classification and the additional
  all-root Hessian null set; these algebraic details are also displayed
  below. Its R3 supplies the fixed-disk root-continuation argument.

No cap-failure estimate, factorial count moment, spatial independence, or
multi-point Kac–Rice calculation is needed in this companion. The main
consumer separately retains [ELDER] S9 to exhaust its failure measure.

Let `B_birth` and `K_gap` be C50's fixed positive-length compact intervals,
with `K_gap subset (0,infinity)`, and let `0<c0<C0` be fixed. For a finite
maximum M, let `D_h(M)` count saddles S such that

    c0 h <= dist(M,S) <= C0 h,
    (f(M)-f(S))/dist(M,S)^3 in K_gap,
    S differs from the actual global elder partner of M.

Define

    N_h(f)=#{finite maxima M: f(M) in B_birth, D_h(M)>0}.

Use C50's actual elder convention and exclusion of the essential class;
set N_h to zero off the Morse/distinct-value locus. Every selected maximum
has a distinct saddle within distance C0 h. This necessary condition is
the only feature of the selection rule used in this companion.

## 2. Cubic notation and generic parameters

Fix `b in R`, `k>0`, an oriented orthonormal frame, and
`theta=(s,a,beta,q)`. In its original Euclidean coordinates put

    P(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2
           +(a/2)(X^2-1/4)Z+(beta/2)XZ^2+(q/6)Z^3,
    M0=(-1/2,0), S0=(1/2,0),
    u=X+aZ/(12k),
    Bs=beta-a^2/(12k),
    Ds=(q-a beta/(4k)+a^3/(72k^2))/2.

The strict endpoint-typing condition is

    s < -|Bs|/2.                                         (1)

The leading homogeneous cubic is

    H3(X,Z)=2kX^3+(a/2)X^2 Z+(beta/2)XZ^2+(q/6)Z^3.

After the displayed invertible shear,

    H3=2ku^3+(Bs/2)u Z^2+(Ds/3)Z^3.

Retain C50's generic exclusions. In particular define

    Delta=12k Ds^2+Bs^3,
    H=12k Ds^2+Bs^3-4Bs s^2,
    Sigma=12k Ds^2+(s-Bs)^2(Bs+2s).

Work outside `Delta=0`, `H=0`, `Sigma=0`, and `Ds=0`. The last two
exclusions are inherited for compatibility; only Delta and H are needed
for the isolation argument below. Each is a nonzero polynomial zero set
after clearing positive powers of k, hence is Lebesgue null at fixed k.

For H, the exact polynomial numerator is

    U=12k beta-a^2,
    V=72k^2 q-18ka beta+a^3,
    H_poly=V^2+U^3-576k^2 U s^2,
    H=H_poly/(1728k^3).

The q² coefficient of H_poly is `5184k^4>0`. This is a genuine null
exclusion, not a quantitative estimate on neighborhoods of degeneracy.

**Lemma 1 (finite nondegenerate cubic roots and one maximum).** Under (1)
and H!=0, P has at most four finite critical points, all nondegenerate,
and M0 is its only critical point with negative-definite Hessian.

**Proof.** The two pins are critical. Every additional root has Z!=0 and
satisfies the conic and line

    6k(u^2-1/4)+(Bs/2)Z^2=0,
    s+Bs u+Ds Z=0.                                      (2)

When Bs and Ds are nonzero, elimination gives

    (12k Ds^2+Bs^3)u^2+2Bs^2 s u+Bs s^2-3k Ds^2=0.

Its linear coefficient is nonzero because s<0, so the polynomial is not
identically zero and has at most two roots. Each determines Z. If Ds=0
and Bs!=0, the line fixes u and the conic gives at most two Z. If Bs=0
and Ds!=0, the conic fixes u=+/-1/2 and the line fixes Z. If both are
zero, s<0 excludes every extra root. Thus the total is at most four.

At an extra root, the identities from (2) are

    det Hess P=-3k(Bs+4su),
    H Z^2=3k(Bs+4su)^2.                                  (3)

The second follows by expanding `12k(Ds Z)^2` using the line and replacing
`Bs Z^2` by the conic. It involves no division by Bs or Ds. An extra
degenerate root therefore forces H=0. At the pins the determinants are
`3k(Bs-2s)` and `3k(Bs+2s)`; their axial entries are -6k and 6k. Condition
(1) makes M0 a strict maximum and S0 a saddle, both nondegenerate.

Finally every polynomial of degree at most three has at most one critical
point with negative-definite Hessian. If p and q were two, set v=q-p.
Its Hessian is affine, so along their segment it is the convex combination
of two negative-definite matrices. Thus

    0=(grad P(q)-grad P(p)).v
      =integral_0^1 v^T Hess P(p+tv) v dt <0,

a contradiction. Applying this to P proves the last assertion. QED.

**Lemma 2 (homogeneous gradient coercivity).** If Delta!=0, there is c>0
such that `|grad H3(x)|>=c|x|^2` in the original coordinates.

**Proof.** In the sheared coordinates the equations for a homogeneous
critical direction are

    6ku^2+(Bs/2)Z^2=0,
    Z(Bs u+Ds Z)=0.

A nonzero solution has Z!=0. If Bs=0 it exists exactly when Ds=0. If
Bs!=0, eliminate u to get `12k Ds^2+Bs^3=0`. Thus Delta!=0 excludes a
gradient zero on the unit circle. Compactness and homogeneity give the
bound there and at every radius. An invertible linear shear preserves the
bound up to a positive constant. QED.

## 3. Global convergence of the fully conditioned fields

For physical scale r, the exact six pins are at
`M_r=(-r/2,0)`, `S_r=(r/2,0)`, with values `b,b-kr^3` and zero gradients.
Append the physical midpoint jet

    J=(f_zz,f_xxz,f_xzz,f_zzz)=(rs,a,beta,q).

Let f_r^theta be CUB (G6)'s full-field regression coupling, using one
unconditioned smooth field F:

    f_r^theta=F+Cov(F,V_r) Gamma_r^(-1)(t_r(theta)-V_r(F)),
    V_r=(U_r,J), t_r=(v_r,rs,a,beta,q).                    (4)

Here U_r is P §3's nonsingular six-component contact frame, v_r its exact
target, and Gamma_r the covariance of V_r. In particular all random-field
correlations and the prescribed endpoint pins are retained.

**Lemma 3 (global contact limit).** For each fixed target and every
sequence r_i->0, this coupling satisfies, almost surely,

    f_ri^theta -> f_0^theta in C4(T_L^2),                 (5)

where the limiting field has exactly the Gaussian law conditioned on the
full ten-component planar jet

    f(0)=b, grad f(0)=0, Hess f(0)=0,
    (f_xxx,f_xxz,f_xzz,f_zzz)(0)=(12k,a,beta,q).            (6)

Also the rescaled fields converge to P in C2 on every fixed disk.

**Proof.** P §3 expresses every U_r component as an evaluation or an
averaged derivative, including the apparently singular axial third
component. For every smooth F these converge to the corresponding contact
derivative. Together with J their limits are exactly all ten independent
jet entries through order three. Their covariance Gamma_0 is positive
definite by P §2 or CUB's full jet rank, and Gamma_r and its inverse
converge. The cross-covariance coefficient functions in (4) converge in
global C4 by the smooth Fourier covariance and its rapidly summable
derivatives. The targets converge to (6). Taking the limit term by term
in (4) proves (5), with its stated Gaussian regression law. In particular
the sequence has bounded global C4 norm pathwise. The rescaled C2 statement
is exactly CUB (G8); a countable exhaustion of disk radii gives it on
every fixed disk for the same sequence. QED.

The limit's dependence on s disappears from (6), because rs->0. This does
not discard the s coordinate from the finite-r disintegration or the
cubic unfolding.

## 4. Morse genericity off the forced contact point

**Lemma 4 (conditional off-origin Morse property).** For every fixed
target (6), f_0^theta is almost surely Morse on `T_L^2 \ {0}`.

**Proof.** At x!=0 and a unit vector v, consider the random vector

    Z(x,v)=(grad f_0^theta(x), Hess f_0^theta(x)v) in R^4.

Its conditional covariance given (6) is positive definite. Otherwise a
nonzero linear combination of these four observations would equal a
linear combination of the ten contact observations in Gaussian L2.
By P §2's positive Fourier spectrum, the resulting distribution of
derivative evaluations annihilates every Fourier mode and hence is zero.
Its supports x and 0 are disjoint, so its part at x must be zero.
First derivatives and second derivatives are independent orders; the
second derivative part has polynomial symbol `(beta.xi)(v.xi)` and is
zero only when beta=0, since v!=0. The first derivative coefficients then
also vanish. This contradicts a nonzero four-component combination.

On every compact set of x separated from 0, times the unit circle, the
covariance varies continuously and has a positive minimum eigenvalue.
The corresponding four-dimensional Gaussian densities are uniformly
bounded. The conditional mean does not affect the upper density bound.

For completeness apply P §8's mesh argument here. The parameter manifold
(x,v) has dimension three. Cover it by finitely many bounded charts and
an epsilon mesh with O(epsilon^-3) sites. On the event that the C1 norm of
Z is at most M, a zero implies some mesh value has size O(M epsilon).
The density bound and the union bound give probability at most
`C M^4 epsilon`, which tends to zero. First fix M, then let M increase;
the random C1 norm is finite by smoothness. Countably exhaust the torus
away from 0. With probability one there is no simultaneous zero of
`grad f_0(x)` and `Hess f_0(x)v` anywhere with x!=0, which is the assertion.
QED.

This lemma is proved for fixed conditional targets, as are the source
couplings. Fubini permits its use under the absolutely continuous theta
integral. No common probability-one event over uncountably many targets
is required. Distinct remote critical values are not needed for isolation.

## 5. A deterministic bridge across intermediate spatial scales

**Lemma 5 (root-free annulus).** Consider a fixed sequence f_i with scales
r_i->0 in the coupling of Lemma 3 and a generic theta satisfying Lemmas
1–2. On any realization for which (5) and the rescaled convergence hold,
there are fixed R and delta>0 such that, for all sufficiently large i,

    grad f_i(x) != 0 whenever Rr_i <= |x| <= delta.        (7)

The constants can depend on theta and the realization; delta is chosen
inside an embedded torus chart.

**Proof.** The sequence has a finite global C4 bound by (5). Add and
subtract the second-order Taylor expansions of the gradient at the exact
two pins +/-r_i e_x/2. Since both endpoint gradients vanish,

    grad f_i(0)=O(r_i^2),
    Hess f_i(0)e_x=O(r_i^2).

The remainders are O(r_i^3) under the C4 bound. The other independent
Hessian entry is exactly `f_i,zz(0)=r_i s`, hence
`||Hess f_i(0)||=O(r_i)`. By (5)–(6) the third derivatives at zero
converge to those of H3. Taylor's formula for the gradient therefore
gives constants C<infinity and epsilon_i->0 such that

    |grad f_i(x)-grad H3(x)|
      <= C r_i^2+C r_i |x|+epsilon_i |x|^2+C |x|^3        (8)

on a fixed sufficiently small coordinate disk. All derivatives and norms
in (8) are in the original Euclidean coordinates. The r_i² and r_i terms
are consequences of the exact pins, not merely of global convergence.

Let c>0 be Lemma 2's constant. First choose R so that
`C/R²+C/R<c/4`; enlarge it to contain every finite cubic root, with a
root-free boundary. Then choose embedded delta>0 so that `C delta<c/4`.
For i sufficiently large, `epsilon_i<c/4` and `Rr_i<delta`. If
`Rr_i<=|x|<=delta`, the error in (8), divided by |x|², is less than 3c/4.
Lemma 2 gives

    |grad f_i(x)| >= (c/4)|x|^2 >0.

This proves (7). The choices are R first, then delta, then i. The
argument does not apply fixed-disk convergence on a growing disk. QED.

The limit itself has an isolated origin: (6) and Taylor's formula give
`grad f_0(x)=grad H3(x)+O(|x|^3)`. After decreasing delta if necessary,
there is no critical point of f_0 in `0<|x|<=delta`.

## 6. Eventual absence of a second selected maximum

**Theorem G (full-field isolation).** Fix b,k,frame and a typed generic
theta as in §2. Under the full conditional coupling (4), for every fixed
`t>0` and every sequence r_i->0, almost surely

    N_(r_i/t)(f_ri^theta) <= 1

for all sufficiently large i. In particular this holds for each fixed
`t in [c0,C0]` used in the radial integral. The conclusion also holds for
any selection of maxima that requires a distinct saddle within distance
`C0 r_i/t`; actual elder and mark restrictions only reduce that population.

**Proof.** Work on the probability-one event of Lemmas 3–4. Choose R and
delta as in Lemma 5, increasing R to contain all cubic roots. By Lemma 1
all roots are nondegenerate. On the fixed rescaled disk B_R, choose small
disjoint neighborhoods of those roots. C2 convergence supplies exactly
one continued critical root in each, with unchanged inertia. For explicit
uniqueness, fix the inverse limiting Hessian in each neighborhood; the
Newton map `x -> x-H_root^(-1) grad g_i(x)` is a contraction on a
sufficiently small closed ball and maps it into itself. On the compact
complement of these balls the cubic gradient has a positive floor, so
there are no further roots. Thus the physical disk B_(Rr_i) contains
exactly the continued cubic roots. It has exactly one maximum, the exact
pin M_i, whose value remains b. This is all-root stability, including
roots outside the original height window.

By Lemma 5 no additional critical root occurs between that disk and the
fixed disk B_delta. The limiting origin is isolated, and by Lemma 4 all
other critical points of f_0 are nondegenerate. There are finitely many:
they lie in a compact set away from the origin, and any accumulating
critical sequence would have a critical limit, contradicting local root
isolation at a nondegenerate point.

Choose small disjoint balls around the finitely many remote critical
points, all separated from B_(delta/2). Global C2 convergence in Lemma 3
and the same contraction argument give exactly one continued root in
each ball, with unchanged inertia. On the compact remainder outside
B_(delta/2), the limiting gradient has a positive minimum, so it has no
other continued or newly formed roots. Together with the annulus and
inner-disk control, this accounts for all critical points of f_i.

The finitely many remote roots have a positive minimum pairwise distance,
and a positive minimum distance from the origin. These separations
persist with a smaller positive lower bound for their continuations;
the local roots converge to the origin in physical coordinates. Since
`C0 r_i/t -> 0`, for all sufficiently large i every distinct critical
pair at distance at most `C0 r_i/t` lies wholly in the local cubic
cluster. That cluster has only the one maximum M_i.

Every selected maximum counted in N_(r_i/t) has a distinct saddle within
this distance. Hence at most M_i can be selected. The restrictions on
birth, positive normalized gap, finiteness, and the actual global elder
partner cannot create another candidate maximum. This proves the claim
on the Morse/distinct-value locus. Off that locus the prescribed N=0
extension also satisfies the claim. QED.

## 7. What this supplies to the occurrence consumer

For fixed outer b,k,frame,t and almost every typed theta, Theorem G proves
pathwise eventual vanishing of the bounded whole-field event

    1{N_(r_i/t)(f_ri^theta)>=2}.

On the typed complement and its boundary, the consumer uses ELDER S11's
zero limiting typed determinant weight. The exceptional cubic sets are
null under the absolutely continuous physical midpoint-jet density.
No convergence or uniform rate is asserted on those exceptional sets.

The consumer can therefore insert the bounded event into C50's exact
once-per-bar identity and the original physical-jet disintegration. Its
reciprocal denominator is at least one on an eligible pair; the event's
eventual vanishing means no cutoff-boundary convergence of that denominator
is needed. The source C4 determinant envelope handles compact theta boxes,
and the unchanged S9 actual-failure tail handles their complement.

This companion does not itself assert a factorial moment estimate,
quantitative rate, uniformity as marks or L escape their fixed ranges,
Poisson behavior, infinite-volume theorem, higher-dimensional law, or
unrestricted short-bar exhaustion. The full-torus conclusion here is
restricted to the conditional coupling and the stated eventual bounded
event. All seven source hypotheses remain retained exactly.
