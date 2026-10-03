# Full bounded-layer comparison for the designated persistence pairing

Object: C98-BOUNDED-LAYER-PAIRING-COMPARISON-20261003-v1.
Author: OpenAI/Codex root01a0bbb5, for Dylan Roy — delegated AI work.
R17 claim2439a0f3-c86c-4ce9-9c92-1b801a59b5c1, WE632 read back.
AUTHOR-SIDE CANDIDATE; full nonauthor review pending. Personal reading
PENDING; independent human review NONE; organizational independence0;
scientific effect NONE.

## 0. The theorem and its exact inputs

Use the full setting of C97: a normalized periodized Gaussian field on a
fixed planar torus of side L>0; gap mark k=1; b in a fixed nonempty compact
birth set B0; all orthonormal frames; fixed finite Lambda>0. Pins are
M_r=(-r/2,0), S_r=(r/2,0), values b,b-r^3 and zero gradients. Q_r is the
continuous pinned Gaussian regression law, W_r is the actual typed product
of absolute Hessian determinants, and Q_r^W=(W_r/Z_r)Q_r uses the FULL
normalizer Z_r=E_Q W_r=r^2 z_r. These definitions and their analytic premises
are unchanged; parent P is read with E1/E2 and the reconciliation.

The raw jets and domain are

    theta=(lambda,gamma,B1,C3), lambda=-f_zz(0)/r,
    (gamma,B1,C3)=(f_xxz(0),f_xzz(0),f_zzz(0)),
    D_Lambda={|lambda|<=Lambda},
    D=gamma^2-12B1, J=8gamma^3-144B1 gamma+576C3,
    a_M=24lambda-D, a_S=24lambda+D,
    T={a_M>0,a_S>0}.

Here D without a subscript is a scalar polynomial, not the domain.
On T and gamma!=0 put

    psi=24lambda/gamma^2, c=D/gamma^2, R=J/gamma^3,
    P(u,Z)=2u^3-3u/2-1/2-(psi+2cu)Z^2/48+RZ^3/3456.       (B1)

Then psi>|c|, P(M)=0, P(S)=-1 at M=(-1/2,0),S=(1/2,0).
Let mu be the maximum of P(Y)+1 over the finite set of extra nondegenerate
saddles of P, and -infinity if this set is empty. Retain C95/C97's events

    E={D_Lambda,T,gamma!=0,psi>=2c,
                          R^2<=16(psi-2c)^2(psi+c),mu<0},
    Rsec={D_Lambda,T,gamma!=0,mu>0}.                      (B2)

H_r is C96's designated finite ordinary-superlevel H0 death event, defined
false off the Borel Morse/distinct-value typed-pin locus. The event is about
the chosen maximum and saddle, not gradient-branch adjacency.

Write mu_r(B)=r^(-5)E_Q[W_r 1_{theta in B}] on D_Lambda. C92 gives
densities g_r and

    g_0(theta)=rho_0(0,gamma,B1,C3) a_M a_S 1_T/16,
    dmu_0=g_0 dtheta, m_Lambda=mu_0(D_Lambda),
    integral_D |g_r/z_r-g_0/z0|<=Cr,
    z_r=z0+O(r), 0<z_*<=z0<=z^*,
    Q_r^W(D_Lambda)=r^3 m_Lambda/z0+O(r^4).              (B3)

rho_0 is the JOINT contact density at its A coordinate zero, not a
probability-normalized conditional t-density. C92 supplies uniform positive
lower and finite upper bounds for m_Lambda. All constants in this note may
depend on L,B0,Lambda; they are uniform in b/frame for sufficiently small r.

**Theorem BL.** With m_E=mu_0(E),m_R=mu_0(Rsec),

    E={D_Lambda,T,gamma!=0,mu<0} exactly,
    m_Lambda=m_E+m_R, 0<m_*<=m_E,m_R<=m^*<infinity,        (B4)
    Q_r^W(D_Lambda intersect (H_r symmetric_difference E))
                                                   <=C r^(7/2), (B5)
    Q_r^W(D_Lambda intersect H_r)
                             =r^3 m_E/z0+O(r^(7/2)),
    Q_r^W(D_Lambda minus H_r)
                             =r^3 m_R/z0+O(r^(7/2)),    (B6)
    Q_r^W(H_r | D_Lambda)=m_E/m_Lambda+O(sqrt(r)).        (B7)

In particular the limiting conditional probability in B7 lies uniformly
strictly between0 and1 for these fixed parameter sets. It is not1.

There is also a joint jet/Boolean-mark statement. For every real bounded
Borel phi(theta,h) on D_Lambda times{0,1},

    |r^(-3)E_QW[1_D phi(theta,1_H)]
       -(1/z0)integral_D phi(theta,1_E(theta))dmu_0|
                                    <=C ||phi||_infinity sqrt(r). (B8)

Thus the rescaled finite measures have the displayed O(sqrt(r)) total
variation bound, where the norm means the supremum over |phi|<=1 (no hidden
factor1/2 convention). Conditional on D_Lambda, the law of (theta,1_H)
converges with that rate to the pushforward of mu_0/m_Lambda by
theta -> (theta,1_E(theta)). This is neither TV of field laws nor TV of
real-valued replacement-location or death-height marks.

Exact reviewed inputs, retained in SOURCE_IDENTITIES.json:

- C82 proof5959920397,11253-byte mathematical prefix SHA256
  f390ad99b07ec4eda9160191d776cfc3a53ca628976165987d9a61ab79816827,
  review5959988102: finite extra branches and critical identities.
- C92 proof5963825788,19567B SHA256
  6fa4c3d6d1e8c3d8590c865802d5df061ad5b17652ddc7fd7bf5c5e8b8de084a,
  review5963946854: actual joint jet density, B3/full normalization.
- C93 proof5964167051,15545B SHA256
  f25f86cc66ae335b4832ea53670646815567ec7854fa0386f8c57f6939e0af1c,
  review5964232937: E6, QW(D_Lambda intersect T^c)<=Cr^4.
- C95 proof5964938563,16185B SHA256
  c0d9ee72352fafe91f96a8b6187c978f09ee3c187d5f4c7c2462c0187750d2e1,
  review5965062739; C96 proof5965141133,7657-byte suffix SHA256
  7198ff636e330749428ded6938776dad612f6bdb51ad62359b445f016df13a7a,
  review5965199940: QW(E minus H_r)<=Cr^(7/2), positive m_E,
  and the maximin/H0 a.s. identification.
- C97 proof5965421543,16098B SHA256
  acf83958e6ea650d83bf811b2beacc03b553637dc4a3160012567c7f0a300a57,
  review5965531981,23585B SHA256
  1de14fcabaad502e6fe36f79bcb3992841551d766ef41ceaba9c8155b5655212:
  QW(Rsec intersect H_r)<=Cr^(7/2), positive m_R and the limited
  E-union-Rsec comparison. C94's retained analytic premises remain in C95.

The algebra below is a direct reconstruction of the pertinent SM saddle-arc
structure, with its provenance credited. SM5959038812, review5959754319 and
amendment5961281898 are read together. No withdrawn variable-width integral,
SM global death claim, or unreviewed source-wide promotion is consumed.
Current merged Math244 and Math170 retain respectively blobs c69f92b1076399fb9f8917bb273e15348b0a497e
and ef2aa57959ea9f721bbf2316ce94cf616c1c9113. Their qualitative model/compact
sector history is not asserted newly discovered. The present addition is
the explicit whole bounded-layer rate and joint Boolean measure composition.

## 1. Algebraic coverage, including absent and exceptional saddles

At an extra critical point set sigma=-2u. C82, or direct differentiation,
gives

    sigma^2-cZ^2/36=1, RZ=48(psi-c sigma),
    P+1=(sigma+1)/2-psi Z^2/144,
    det Hess P=(c-sigma psi)/4.                           (B9)

Such a point is a saddle exactly when sigma psi>c. There are at most two
extra nondegenerate saddles, including the R^2=64c^3 degree drop; at c<0
tangency the degenerate point is not a saddle. These are C82's explicit
finite polynomial branches, not an exclusion of parameter values. Their
guarded finite maximum makes mu Borel, with the empty-set convention.

We prove the implication

    mu<0 => psi>2c and R^2<16(psi-2c)^2(psi+c).            (B10)

This is all the deterministic coverage needed, since E already includes
mu<0. It is not an invocation of a global maximin classifier.

Reflection Z->-Z changes R to -R and preserves all critical heights/types.
It suffices to handle R>=0.

**Case c>0,R>0.** Set y=psi/c>1. On 1<sigma<y choose
Z=6sqrt((sigma^2-1)/c)>0. Equation B9 requires

    R_+(sigma)=8sqrt(c)(psi-c sigma)/sqrt(sigma^2-1),
    R_+'(sigma)=8sqrt(c)(c-psi sigma)/(sigma^2-1)^(3/2)<0. (B11)

This is a continuous strictly decreasing bijection from(1,y) onto(0,infinity),
with the endpoints reversed. Its point is a nondegenerate saddle because
sigma>1>c/psi. Its height satisfies

    P+1=(sigma+1)[2-y(sigma-1)]/4.                        (B12)

If mu<0, this saddle's value is negative, hence sigma>sigma*=1+2/y.
Since sigma<y, y>2 follows from y^2-y-2=(y-2)(y+1)>0. The point sigma*
is then inside(1,y), and

    R_+(sigma*)=q:=4(psi-2c)sqrt(psi+c)>0.

Monotonicity implies R<q. Another negative-Z saddle, if present, cannot
invalidate this necessary condition obtained from the positive-Z saddle.
This also covers the degree drop without dividing by its quadratic coefficient.

**Case c>0,R=0.** B9 forces sigma=y and Z=+/-6sqrt((y^2-1)/c).
Both points are nondegenerate saddles and have

    mu=-(y-2)(y+1)^2/4.                                  (B13)

Thus mu<0 implies y>2, and0=R<q. At y=2 the two heights are tied at-1
and mu=0, so this equality case is not incorrectly put into mu<0.

**Case c<0.** Put a=-c>0,y=psi/a>1. For R>0 the line equation forces Z>0,
because psi+a sigma>0 for -1<sigma<1. All nondegenerate saddles are on
sigma in(-1/y,1), where

    R_-(sigma)=8sqrt(a)(psi+a sigma)/sqrt(1-sigma^2),
    R_-'(sigma)=8sqrt(a)(a+psi sigma)/(1-sigma^2)^(3/2)>0. (B14)

This branch runs from the tangency value
R_t=8sqrt(a(psi^2-a^2)) to infinity. The full ellipse/line intersection
has no saddle for0<=R<=R_t: below tangency there is no intersection, at
tangency the only point has determinant0, and for R>R_t exactly one of
the two intersections has sigma>-1/y. These facts also follow by the
unique minimum of R_-(sigma) on(-1,1) at-1/y. For R=0 the positive line
right side directly rules out any extra critical point.

Here psi>2c automatically, and q=4(psi+2a)sqrt(psi-a)>R_t, since

    q^2-R_t^2=16psi^2(psi-a)>0.                           (B15)

Consequently the no-saddle and tangency cases (mu=-infinity) satisfy B10.
For R>R_t the unique saddle's height is

    P+1=(sigma+1)[2-y(1-sigma)]/4.

If mu<0 then sigma<sigma*=1-2/y. This point lies strictly in(-1/y,1),
and R_-(sigma*)=q. Monotonicity gives R<q, proving B10.

**Case c=0.** If R=0 there are no extra critical points and mu=-infinity;
psi>0 and0<16psi^3. If R!=0 the sole extra saddle is sigma=1,Z=48psi/R,
and mu=1-16psi^3/R^2. Thus mu<0 gives R^2<16psi^3. All cases of B10
are proved, including empty saddle sets. B4's exact equality of E follows.

## 2. Neutral sets are null under the ACTUAL law as well as the model

If mu=0, some extra nondegenerate saddle has P+1=0. By B9,
Z^2=72(sigma+1)/psi. Because Z!=0 and psi>0, sigma+1>0. Substituting
into the conic and dividing by this positive factor gives

    sigma=1+2c/psi, Z^2=144(psi+c)/psi^2,
    R^2=16(psi-2c)^2(psi+c).                             (B16)

No division by R is needed; psi=2c,R=0 is included. We require only this
inclusion, not that every point on the algebraic surface has mu=0.
In raw jets, B16 implies

    F(theta):=J^2-16(24lambda-2D)^2(24lambda+D)=0.        (B17)

For every fixed(lambda,gamma,B1), F is a quadratic polynomial in C3 with
nonzero leading coefficient576^2. It has at most two real zeros. Tonelli
on bounded boxes, followed by countable exhaustion, shows {F=0} has
four-dimensional Lebesgue measure zero. The hyperplane gamma=0 is null too.

For each fixed sufficiently small r>0, C92 J8 gives a nondegenerate
four-dimensional Gaussian density for(A,gamma,B1,C3) under Q_r. The map
A=-r lambda is invertible, so theta has a density. Hence these raw sets
are Q_r-null and Q_r^W-null by absolute continuity W_r/Z_r. Dependence of
W_r on the full field does not change this implication. The model mu_0
has its displayed Lebesgue density, so the sets are mu_0-null as well.

This proves, separately under both measures,

    {D_Lambda,T,gamma!=0} = E disjoint_union Rsec
                                    modulo a null set.  (B18)

There is no simultaneous probability-one assertion across uncountably
many pinned laws. Nullity holds for each parameter; the quantified bounds
inherited from the parents are uniform. No near-boundary rate is deduced
from nullity. C94/C97 already supplied those quantitative level-band rates.
We do not discard the degree-drop or tangency sets to prove B10/B18.

## 3. Full bounded-layer error and mass

The unclassified part of D_Lambda is now contained, up to an actual null
set, in T^c. C93 E6 bounds its probability by Cr^4. On E the mismatch
is E minus H_r; on Rsec it is Rsec intersect H_r. Consequently

    QW(D_Lambda intersect (H_r symmetric_difference E))
      <=QW(E minus H_r)+QW(Rsec intersect H_r)+QW(D_Lambda intersect T^c)
      <=C1 r^(7/2)+C2 r^(7/2)+C3 r^4<=C r^(7/2)         (B19)

for0<r<=1. This proves B5. T^c is small, not asserted null at finite r.
C96's a.s. designated-event identification is the only topological input
in the two parent sector bounds. No new topology or witness-count inference
enters B19.

The model is supported on T and gives no mass to gamma0 or F0, so B18
implies m_Lambda=m_E+m_R. The fixed-parameter uniform positive bounds for
m_E and m_R come respectively from C94/C95 and C97's explicit positive
jet boxes; the upper bounds follow from C92's m_Lambda bound. These facts
prove the remaining claims in B4. Apply B3 to1_E and subtract/add the
nonnegative mismatch bounded by B19 to prove the first line of B6.
Subtract it from B3's total D mass to obtain the second. Dividing the
first by QW(D)=r^3[m_Lambda/z0+O(r)], whose bracket has a uniform positive
floor, proves B7. Uniform separation of m_E/m_Lambda from0 and1 follows
from both positive numerator floors and the finite m_Lambda ceiling.

## 4. The joint jet/Boolean measure, with its normalization explicit

Replace phi(theta,1_H) by phi(theta,1_E). On the mismatch set its change
is at most2||phi||_infinity and elsewhere zero. By B19 the change after
r^-3 rescaling is at most C||phi||_infinity sqrt(r). For the replacement,
the exact jet disintegration and B3 give

    r^-3 E_QW[1_D phi(theta,1_E)]
                       =integral_D phi(theta,1_E)g_r/z_r dtheta,
    |integral_D phi(theta,1_E)(g_r/z_r-g_0/z0)dtheta|
                                            <=Cr||phi||_infinity. (B20)

Combining proves B8. The observable is a function of the raw jets and
one Boolean mark; no replacement of a full-field conditional law is made.

For completeness, let nu_r be the rescaled joint measure in B8 and nu_0
its limit. Their masses satisfy a_r=nu_r(1)=m_Lambda/z0+O(r) and
a_0=m_Lambda/z0>=a_*>0. For |phi|<=1,

    |nu_r(phi)/a_r-nu_0(phi)/a_0|
       <=||nu_r-nu_0||/a_r+|a_r-a_0|/a_r
       <=C sqrt(r).                                      (B21)

This proves the asserted conditional TV conclusion. In particular it
does not replace z0 by1 or turn the rare D event of order r^3 into a
probability-one event under the original full weighted law.

## 5. Boundary of this delivery

The missing E/Rsec coverage is supplied at this exact fixed bounded layer;
B8 quantifies the resulting joint raw-jet/Boolean law. Previously proved
qualitative classification is credited rather than relabeled as novel.
The proof neither depends on nor repairs every claim in SM, Math244 or
Math170. No source is overwritten and no historical disposition is changed.

Lambda remains fixed. No uniform-in-Lambda constants, exhaustion as
Lambda->infinity, all gap marks, other dimensions, infinite-volume limit,
replacement-location/death-height TV, regional shrinking multiple-witness
collision, all-small-bars converse, intermediate/coarea composition or
final global density/remainder completion is proved here. Existing scoped
D1/D2 acceptances are neither enlarged nor withdrawn. Exact algebra checks
support transcription and falsify specified errors; they do not prove the
Gaussian/topological parent premises or the continuous inequalities.
