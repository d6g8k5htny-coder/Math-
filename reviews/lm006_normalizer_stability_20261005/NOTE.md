# LM006: quantitative stability of the normalized typed endpoint weight

Dylan Roy — delegated AI mathematical work. Author: OpenAI / GPT-6 Astra Pro,
session `round12-audit-completion-20261005`, 5 October 2026 (Central Time).
Scientific effect NONE. This is an additive analytic companion, not a Lean
formalization or a revision of any historical proof or acceptance record.

## 1. Scope and prior work

The historical P02-LM-006 body, 9,147 bytes, SHA256
`239ed094f70aa4352021572ad8bdc0c6ac6404edab4e1d7e61addec0c6659150`,
fixes the exact side24 six-pin law at b=6/5 and gap r^3/6. Its §§2,4 define
six endpoint coordinates and the physical Hessians. Math-#301 supplies a
separate conditional endpoint convergence/moment argument; its unchanged
NOTE is blob `551aa563562bc88a19e33d146259c03aa2d318f6` at merge
`e31b6ad8356e0760c8a7fb6e816ff640c45176c9`.

Filtered-determinant continuity and a common regression coupling already appear
in `frontiers/remote_window_20260924/PROOF.md`, §§3–4, particularly (5),(8),
blob `b383bfcc88ec4ad497dff01fb6640e429ba24a84`, at Math- commit
`f4c33a98a982d50aa490e49ce9327c755682527c`. This note does NOT claim a new
general filtered-determinant continuity theorem or a new qualitative O(r) rate
for that remote-window theorem. Its contribution is an explicit scalar formula
and constants for the particular six-coordinate normalizer, requiring only a
specified endpoint-vector coupling. All proofs below are self-contained.

Notation: x_+=max(x,0), x_-=max(-x,0), and ||.|| is the Euclidean norm.
Use v=(a_-,a_+,b_-,b_+,c_-,c_+) in R^6 and 0<=r<=1. Set

    M_r(v) = [[r a_-, r b_-], [r b_-, c_-]],
    S_r(v) = [[r a_+, r b_+], [r b_+, c_+]],
    F_r(v) = [(a_-)_- (c_-)_- - r b_-^2]_+,
    G_r(v) = [r b_+^2 - a_+ c_+]_+,
    T_r(v) = F_r(v) G_r(v).                                      (1)

At r=0, (1) defines a continuous extension, not division by zero in a physical
normalizer. The concrete torus application stays on 0<r<=r0<24, further
restricted to r<=1; there is no assertion of compatible unequal-height pins at
a period-sized separation. The original all-r wording is not silently repaired.

## 2. Exact identity, including every singular boundary

For r>0,

    T_r(v) = r^-2 |det M_r(v) det S_r(v)|
             1_{M_r(v) negative definite} 1_{det S_r(v)<0}.    (2)

Proof. Write D_-=a_-c_--r b_-^2 and D_+=a_+c_+-r b_+^2. Both physical
determinants are r D_i. Negative definiteness of M_r is equivalent to a_-<0
and D_->0. These imply c_-<0. Conversely, if both a_-,c_- are negative and
D_->0, the maximum type holds. If either is nonnegative, the first factor of
(1) is zero; if either is zero, it is also zero. Thus the maximum-filtered
normalized determinant is exactly F_r. For the 2x2 saddle, index one is
exactly det S_r<0, so the filtered normalized absolute determinant is G_r.
All singular cases contribute zero. Multiplication proves (2).

Consequently T is continuous jointly in (r,v), even where the index indicators
are discontinuous. It is nonnegative and satisfies, for 0<=r<=1,

    0 <= T_r(v) <= ||v||^4.                                  (3)

Indeed F_r<=|a_-c_-| when positive, and G_r<=r b_+^2+|a_+c_+|. Each is
bounded by the squared norm of its respective three-coordinate block, hence
by ||v||^2. The coarse bound (3) is sufficient; no sharp constant is claimed.

For every real a,q let

    v0(a,q)=(-1,1,-a/2,a/2,q,q).

Then, including q=0,

    T_0(v0(a,q))=(q_-)^2.                                    (4)

Thus a null-probability type boundary is unnecessary for convergence of the
DETERMINANT-WEIGHTED variable using this representation. It can still be
necessary for a claim about the bare indicator, which is not made here.
If Q has an atom at zero, (4) remains true. This observation does not change
the old proof's hypotheses or automatically settle its concrete-field inputs.

## 3. Deterministic quantitative bound

For v,w in R^6 and r,s in [0,1],

    |T_r(v)-T_s(w)|
      <= (||v||+||w||)^3 ||v-w|| + |r-s| ||w||^4.             (5)

Proof of the fixed-r part. Reorder v into blocks v_-=(a_-,b_-,c_-) and
v_+=(a_+,b_+,c_+), and similarly w. The projection
P(a,b,c)=(a_-,b,c_-) is norm-contracting and 1-Lipschitz. The quadratic form
ac-rb^2 has symmetric matrix with eigenvalues 1/2,-1/2,-r; its operator norm
is at most1. The form rb^2-ac has the same norm bound. For any symmetric H
with ||H||<=1,

    |x^T Hx-y^T Hy| <= (||x||+||y||)||x-y||.

Composition with P and then positive part therefore gives

    |F_r(v)-F_r(w)| <= S ||v_--w_-||,
    |G_r(v)-G_r(w)| <= S ||v_+-w_+||,
    S=||v||+||w||.

Using nonnegative factors, F_r(v)<=||v||^2, G_r(w)<=||w||^2, and the product
difference split,

    |T_r(v)-T_r(w)|
      <= S (||v||^2 ||v_+-w_+|| + ||w||^2 ||v_--w_-||)
      <= S sqrt(||v||^4+||w||^4) ||v-w||
      <= S^3 ||v-w||.

For fixed w, positive part is 1-Lipschitz in r. The same product split yields

    |T_r(w)-T_s(w)|
      <= |r-s| [F_r(w)b_+^2 + G_s(w)b_-^2]
      <= |r-s| ||w||^2 (b_+^2+b_-^2)
      <= |r-s| ||w||^4.

The triangle inequality completes (5). In particular the proof divides by
neither a transverse eigenvalue nor a distance to a type boundary.

## 4. Expectation and normalizer error under an explicitly given coupling

Let X,Y be any coupled R^6-valued random vectors on ONE probability space.
Assume E(||X||+||Y||)^6<infinity and E||X-Y||^2<infinity. Then their fourth
moments are finite, and (5) with Cauchy–Schwarz gives

    |E T_r(X)-E T_s(Y)|
      <= [E(||X||+||Y||)^6]^(1/2) [E||X-Y||^2]^(1/2)
         + |r-s| E||Y||^4.                                  (6)

No Gaussian or independence premise occurs in (6). It bounds normalizers,
not probabilities of arbitrary events on an unconstructed common field space.
In particular an event depending on the entire field cannot be identified with
an endpoint-vector event merely because its normalizer is controlled.

## 5. Gaussian specialization allowing singular covariance

Suppose endpoint laws are N(m_r,Sigma_r) and N(m_0,Sigma_0) on R^6, with
positive-semidefinite covariances, which may be singular. Choose explicitly
A_r A_r^T=Sigma_r and A_0 A_0^T=Sigma_0 with the SAME finite number of columns.
For example their symmetric positive-semidefinite roots are 6x6 choices.
Using a common standard Gaussian Z defines the legitimate coupling

    X=m_r+A_r Z,  Y=m_0+A_0 Z,
    e_r^2=||m_r-m_0||^2+||A_r-A_0||_F^2=E||X-Y||^2.          (7)

This is a coupling that realizes each marginal; it is not asserted optimal
among Gaussian couplings and not claimed as a construction of the full fields.
Assume ||m_i||<=M and ||Sigma_i||_op<=Lambda for i=r,0. For standard Gaussian
Z_6, radial integration gives E||Z_6||^(2k)=6*8*...*(6+2k-2): the ratios
follow by integration by parts in the integral of t^(5+2k) exp(-t^2/2).
Thus the fourth, sixth and eighth moments are48,480,5760 respectively.
A singular Gaussian has the square-root representation with Z_6, so the bound
uses the marginal covariance norm, irrespective of the chosen factor width.
From ||x+y||^p<=2^(p-1)(||x||^p+||y||^p),

    E||X||^6, E||Y||^6 <= 32(M^6+480 Lambda^3),
    E(||X||+||Y||)^6 <= 2048(M^6+480 Lambda^3),
    E||Y||^4 <= 8(M^4+48 Lambda^2).

Consequently, with s=0,

    |E T_r(X)-E T_0(Y)| <= B e_r + D r,                      (8)
    B=sqrt(2048(M^6+480 Lambda^3)),
    D=8(M^4+48 Lambda^2).

Both the mean term and the covariance FACTOR term in (7) are essential. A
bound on covariance differences alone does not control changes in the mean.
No linear Lipschitz estimate for the square-root map at a singular covariance
is assumed. With symmetric roots, covariance convergence does imply factor
convergence: bounded PSD roots have convergent subsequences, any limit is PSD
and squares to Sigma_0, and uniqueness of the PSD square root identifies it.
This compactness proof supplies continuity, not a numerical rate.

For the exact endpoint law in LM006, take Y=v0(a,Q). By (2),(4),

    E T_r(X)=Z_r/r^2,   z0=E[(Q_-)^2],
    |Z_r/r^2-z0| <= B e_r + D r.                            (9)

The conditional endpoint laws and their factor/mean error must actually be
provided by the application, for example after the separate #301 hypotheses
are verified. Equation (9) does not independently prove that identification.
If z0>0 and B e_r+D r<=z0/2, it yields the explicit sufficiency condition

    (z0/2)r^2 <= Z_r <= (3z0/2)r^2.                         (10)

If a proved bound e_r<=K r^alpha with fixed K and alpha>0 is supplied, one
sufficient radius is the minimum of the application's allowed radius,1,
z0/(4D), and (z0/(4BK))^(1/alpha), omitting any term whose denominator is zero.
Neither K,alpha nor a numerical radius is supplied here. For square-integrable
Q, z0>0 is equivalent to P(Q<0)>0; nondegeneracy of Q is sufficient but is not
necessary. Constant Q=-1 gives z0=1; constant Q=0 or+1 gives z0=0 and no
positive lower-normalizer conclusion. No field model is inferred from those
edge-case witnesses.

## 6. Reproduction and negative controls

Run `python -B -S test_stability.py` and again with `-O` from this directory.
The12 methods cover physical determinant/type identities at exactly
729 vectors times3 positive radii =2187 cases; r=0 boundary/limit values;
300 parameter comparisons;500 paired-vector comparisons; the quartic envelope;
Gaussian moment constants; an exact covariance-I finite coupling check; and
CLI/input rejection. These are finite checks, not the continuum proof.

`stability_check.py` prints a deterministic JSON count. Its baseline has2187
physical identities,15 limit values,200 parameter inequalities,200 squared
vector-envelope tests,3 radial moments and1 mean-shift witness (2606 total).
For the vector diagnostic, (||v||+||w||)^6 is bounded above by
8(||v||^2+||w||^2)^3; squaring avoids irrational arithmetic but tests a weaker
finite envelope than the sharp expression in (5).

M1 replaces r by r^2 in (1); M2 selects minima rather than maxima; M3 omits the
saddle positive part; M4 substitutes a one-dimensional sixth moment; M5 drops
the mean error from (7). Each must exit1 with its named STABILITY_FAIL reason.
Unknown arguments/labels exit2. No floating simulation, Lean or dedicated
hosted execution is represented by these Fraction controls.

## 7. Exclusions and audit boundary

Not claimed: a new parent theorem, unconditional historical LM006 acceptance,
full-field event transfer, new numerical coefficient, covariance-error
certificate, sharp constants, uniformity over unbounded marks, or higher-d
analogue. No existing proof/review/status is edited. Historical #281 alignment
and source-admission issue#310 remain separate. A fresh nonauthor review must
inspect the whole argument including (5)–(10), not just the tests or a previous
review of filtered determinants. This note consumes the explicit definitions
above, not another agent's unreviewed proposed rate.
