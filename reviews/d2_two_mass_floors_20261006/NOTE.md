# Quantitative two-mass floors for the d2 moment interface

Object: D2-TWO-MASS-FLOORS-20261006-v1.
Dylan Roy — delegated AI work. Author: OpenAI / GPT-6 Astra Pro,
`continuation-d2-proof-execution-audit-20261006`; author exposure to D2Schur and
AUD-309-REVIEW-STRICTNESS-01. Scientific effect NONE; organizational-independence
credit 0. This is an additive analytical candidate, not an accepted scientific
status or a Lean theorem. Claim: main#229/6008048138.

## 1. Scope and predecessor distinction

The existing #302 NOTE section 4/C7 already gives two-radius Gram floors. The
qualitative #317 companion proves actual-integral residual identities and strict
positivity from suitable atoms. This note does not rebrand either as new. Its
additional result is a locally normalized, sharp two-mass lower bound, compared
explicitly with the older pair bounds, and its propagation through the existing
d2 scalar formulas. No reviewed packet, gate, manifest, dependency or verdict is
modified. The elementary completion-of-squares argument is included in full.

Let X be a measurable real random variable on a probability space, with finite
second, fourth and sixth moments. Write

    m2 = E[X^2], m4 = E[X^4], m6 = E[X^6],
    G = m4 - m2^2, Delta = m6 - m4^2/m2.

Take distinct squared radii s,t > 0 and lower masses p,r > 0 such that

    P(X^2=s) >= p, P(X^2=t) >= r.

Thus p+r <= 1. The masses aggregate both signs; no symmetry or independence is
assumed. Put H(u,v)=uv/(u+v) for nonnegative u,v with positive sum, and

    ell = p*s + r*t,
    g = H(p,r)*(s-t)^2,
    d = H(p*s,r*t)*(s-t)^2.

All three numbers are strictly positive. The conclusion is

    m2 >= ell, G >= g, Delta >= d.                         (1)

A zero radius is allowed for the G bound, but then d=0 and strict Delta does NOT
follow. Merely having nonconstant |X| does not imply Delta>0. The zero/+-1 example
from AUD-309-REVIEW-STRICTNESS-01 has G=1/4 and Delta=0.

## 2. Complete proof and exact hypotheses

For u,v>0 and real A,B,c, expansion gives

    u(A-c)^2 + v(B-c)^2
      = H(u,v)(A-B)^2 + (u+v)(c-(u*A+v*B)/(u+v))^2.       (2)

Hence the left side is at least its first term, for EVERY c; equality occurs at
the displayed weighted mean. This is an exact algebraic identity, not a numerical
interpolation or a reliance on a finite test grid.

The two disjoint level sets yield m2 >= p*s+r*t. Probability normalization and
integrability give G=E[(X^2-m2)^2]. Retaining only those two nonnegative level-set
contributions, and then applying (2) with (u,v,A,B,c)=(p,r,s,t,m2), proves G>=g.

For m2>0, expansion and linearity of the integrals give

    Delta = E[(X^3-(m4/m2)X)^2]
          = E[X^2 (X^2-m4/m2)^2].                        (3)

All terms are integrable by the stated moment assumptions. Retaining the same
level sets gives p*s*(s-m4/m2)^2+r*t*(t-m4/m2)^2. Apply (2) with u=p*s,v=r*t to
obtain Delta>=d. Lower masses can replace actual masses because every retained
squared contribution is nonnegative. No distributional independence was used.

The Delta part of the argument also holds for a nonnegative measure not
normalized to probability, provided the moments are integrable and m2>0. The
unscaled G identity requires probability normalization: for a finite measure of
total mass M, the centered integral is m4-2*m2^2+M*m2^2, not generally m4-m2^2.
For example, 2*delta_1 gives centered integral 2 but m4-m2^2=-2. The executable
`floors` helper deliberately accepts probability-mass inputs only.

## 3. Individual sharpness, not simultaneous optimizer claims

Fix exact p,r,s,t with s,t>0, s!=t and p+r<=1. These are squared-radius laws; each
is realized by X=sqrt(Y), or by any split of each mass between the two signs.

For Delta, the law of Y=X^2 assigning p to s, r to t and 1-p-r to 0 attains d.
Indeed, c=m4/m2=(p*s^2+r*t^2)/(p*s+r*t), the weighted mean in (2) with u=p*s,v=r*t;
the remaining zero atom contributes nothing to the residual (3).

For G, put c0=(p*s+r*t)/(p+r). Assign p to s, r to t and 1-p-r to c0. This law
has m2=c0 and attains g. Thus neither constant in (1) can be increased uniformly
using just these two exact masses/radii.

For p+r<1, these are different extremizers. The residual-optimal nonzero squared
radius is (p*s^2+r*t^2)/(p*s+r*t), strictly larger than c0 by
p*r*(s-t)^2/((p*s+r*t)*(p+r)). We do NOT claim simultaneous attainment of both
floors by a common law when unassigned mass remains. The later combined scalar
bounds are valid conservative consequences, not asserted optimal joint bounds.

## 4. Comparison with the existing lattice Gram floors

For s=h^2,t=4h^2, p=P(|X|=h), r=P(|X|=2h), (1) reads

    G >= 9*h^4*p*r/(p+r),
    Delta >= 36*h^6*p*r/(p+4*r).                          (4)

The older #302/C7 floors are 9*h^4*p*r and 36*h^8*p*r/m2. The first new bound is
at least the old because p+r<=1. The second is at least the old because
m2>=h^2*(p+4*r). This is only a symbolic comparison; it does not replace the
existing outward enclosures or supply new numerical values for any period.
The comparison is not a claim that the old, correct bounds were defective.

## 5. Explicit all-direction scalar bounds

This section uses the exact algebraic formulas of the existing D2Schur source.
It does not identify a Gaussian/Palm covariance with those scalar expressions.
For q in the CLOSED interval [0,1/4], set

    D(q) = m2^2*m4 + (m4-3*m2^2)*(m4+m2^2)*q,
    N = m2^2*(m4^2-m2^4), S(q)=N/D(q),
    T(q) = Delta*(1-3*q) + 9*q*m2*G.

The endpoint identities are

    D(0)=m2^2*m4, D(1/4)=G*(m4+3*m2^2)/4,
    T(0)=Delta, T(1/4)=(Delta+9*m2*G)/4.

Both D and T are affine. Given ACTUAL upper bounds m2<=U2 and m4<=U4, define

    D_lower = min{ell^2*(ell^2+g), g*(4*ell^2+g)/4},
    D_upper = max{U2^2*U4, (U4-ell^2)*(U4+3*U2^2)/4},
    N_lower = ell^2*g*(2*ell^2+g),
    T_lower = min{d, (d+9*ell*g)/4}.

Then

    0 < D_lower <= D(q) <= D_upper,
    0 < N_lower/D_upper <= S(q),
    0 < T_lower <= T(q).                                 (5)

Proof: m4=m2^2+G, m2>=ell and G>=g give each determinant endpoint lower bound
and N>=N_lower. For the upper bound, m2^2*m4<=U2^2*U4, and
G<=U4-ell^2 while m4+3*m2^2<=U4+3*U2^2. All factors are nonnegative;
U4-ell^2>=g>0 follows from the actual assumptions. Affine interpolation now
bounds D at every q. Divide the positive N lower bound by the D upper bound;
using the LOWER determinant in this division would give the wrong direction.
Similarly both T endpoints dominate their indicated expressions, so affine
interpolation proves the final bound. Formula S=N/D uses D>0 just established,
not Lean's totalized division at zero. The determinant lower bound and T bound
do not require U2,U4; only the explicit Schur bound above uses them.

## 6. Uniform-input interface and its limits

H is nondecreasing in each nonnegative argument: for u'>=u and v>0,

    H(u',v)-H(u,v)=v^2*(u'-u)/((u'+v)*(u+v)) >= 0.

Suppose a family has certified lower masses p_-,r_->0, lower squared radii
s_-,t_->0, and a certified separation |s-t|>=eta>0. Then uniform substitutes are

    ell_- = p_-*s_-+r_-*t_-,
    g_- = H(p_-,r_-)*eta^2,
    d_- = H(p_-*s_-,r_-*t_-)*eta^2.

Together with actual uniform U2,U4 these may be used in (5). They are inputs,
NOT certificates supplied here. Overlapping radius intervals do not establish a
positive eta. Two merely positive masses need not be bounded away from zero.
In particular X -> epsilon*X scales G by epsilon^4 and Delta by epsilon^6;
strict positivity alone cannot give a uniform positive floor. No claim is made
uniformly over all L, all marks, or the actual periodic spectral family.

A follow-on Lean development may first formalize (2) and its inequalities, then
use the actual-integral identities from #317 and measurable level-set bounds.
This packet adds ZERO Lean declarations and does not alter the primary 63-target
manifest. The existing qualitative companion's review is not a review of (1)-(6).

## 7. Reproduction, controls and source map

Run, from this directory:

    python -B -S test_two_mass.py
    python -B -O -S test_two_mass.py
    python -B -S two_mass.py
    python -B -O -S two_mass.py

The checker uses Fraction only. Its seven mutations must exit1 with exactly the
named failing check and empty stderr: M1 square completion; M2 fourth floor;
M3 Delta floor; M4 wrong tau endpoint; M5 omitted probability normalization;
M6 wrong Schur denominator endpoint; M7 zero-atom strictness. M9 exits2 with
exactly `unknown mutant\n`. These are finite controls, not a continuum proof.
The dedicated workflow validates source membership/hashes and pinned upstream
blobs, then runs both test modes and authentic baseline/mutation protocols.
Configured CI is not successful execution; actual run identity is recorded in
the PR, separately from the theorem's ordinary mathematical review.

SOURCES.json records exact immutable upstream files. The consumed algebraic
source is Math- commit 2f8b6f372be383d752e9dd30d38234faa977243c:
- formal/ResearchFormalCoreR1/D2Schur.lean (scalar definitions and endpoint facts);
- reviews/side24_d2_certified_small_L_claude_20261005/NOTE.md, sections2/4 (original
  reduction and C7 comparison only; its numerical outputs are not recertified).
The #317 actual-integral source at b122462634460a8bb9e88406072cb7a356957407 is
motivating correspondence, not needed as an accepted premise: (2)-(3) are proved
above. Its existing review and kernel evidence do not transfer to this note.
No private cloud source is an input to this packet.
