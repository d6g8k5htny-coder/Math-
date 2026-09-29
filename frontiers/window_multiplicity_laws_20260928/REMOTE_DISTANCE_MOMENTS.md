# Remote pair distances: a moment transition and a nonuniform-integrability effect

Object: OA-WINDOW-MULTIPLICITY-DISTANCE-20260928-v1.
Author: OpenAI / ChatGPT, foreground research session, 28 September 2026.
Disposition: AUTHOR-SIDE PROOF CANDIDATE; NONAUTHOR ANALYTIC REVIEW REQUIRED.
Scientific effect: NONE. This is a new analytic consumer, not a status change.

## 1. The quantities and two different limits

Retain the exact fixed-remote model and fixed positive-volume Borel E of
REMOTE_PAIR_LAW.md. Counts are ordered and sum all indices. Let

    M_p(r)=E_Qr^W sum_{x!=x' counted in E} dist(x,x')^p,
    p>=0, M_0(r)=E_Qr^W[N(E)(N(E)-1)].                    (D1)

Distances are physical torus distances. This note obtains a boundary-layer versus
fixed-distance transition at p=1. A typical pair under the normalized factorial
mean is a distance of order r apart, but a much rarer macroscopic pair can dominate
an unbounded distance moment. No pair-occurrence probability is inferred.

Write A_0=integral_E sum_ij K_ij from (R3). More generally, for 0<=p<7, define

    A_p = [3*12^((p+2)/3)*k^((p+5)/3)]
                / [4(p+2)(p+5)z_0]
        * integral_E dx integral_S de p_{Y|Q0}(0,0,b)
          E_Q0[w_0 |T|^((4-p)/3)(det A)^2 |Y=(0,0,b)].    (D2)

Here Y,T,A,w_0,z_0 have exactly the definitions in (R1)-(R3), and index summation
has removed chi. The conditional expectation in (D2) is finite for p<7; the
possible negative power of T for p>4 is integrable because (4-p)/3>-1 and the
weighted conditional Gaussian density is bounded near zero.

For distinct x,x' in E define the fixed-distance contact pair kernel

    Lambda_2(x,x') = p_{(grad f(x),grad f(x'),f(x),f(x'))|Q0}(0,0,b,b)/z_0
        * E_Q0[w_0 |det H_x det H_x'|
                  | grad f(x)=grad f(x')=0, f(x)=f(x')=b]. (D3)

This is the all-index sum of the joint kernel in [RM, Section 6]; it is not a
product of two one-point kernels. Let

    B_p=k^2 integral_{E x E, x!=x'} dist(x,x')^p
                                              Lambda_2(x,x') dx dx'. (D4)

Below we prove B_p is finite and strictly positive for p>=0, including at the
collision diagonal where a compact-separation argument alone is insufficient.

**Theorem D (distance moments).** For each fixed p>=0,

    0<=p<1: M_p(r)=r^(5+p) A_p+o(r^(5+p));
    p=1:    M_1(r)=r^6(A_1+B_1)+o(r^6);
    p>1:    M_p(r)=r^6 B_p+o(r^6).                       (D5)

The constants A_p and B_p are the explicit conditional integrals above, not
numerical enclosures. The p=1 formula has **two positive contributions**. Simply
extending the microscopic limit's first moment to the full pair measure would
miss B_1.

## 2. A sharper determinant estimate that retains the small height difference

[RC]'s uniform bound used |det H_x|<=C delta K^d, with K>=1+||f||C3. For distance
moments we need the extra cancellation forced by nearly equal heights.
Use K=C_d(1+||f||C4), the exact collision frame V_delta, and its last target t.
The Peano formula gives

    D^3 f(x)[e,e,e] = -12t+O(delta K).

From the gradient Taylor identity (R7), in a frame beginning with e,

    H_x=[[delta alpha,delta beta^T],[delta beta,A]],
    alpha=6t+O(delta K), |beta|<=K, ||A||<=K.

The analogous axial entry at x' is -6t+O(delta K). The exact block determinant
identity, valid even when A is singular, gives

    |det H_x|, |det H_x'|
       <= C delta (|t| K^(d-1)+delta K^d).               (D6)

Taking the product, multiplying the original endpoint bound W_r<=C r^2 K^{2d},
and conditioning as in [RC, Lemma 2] gives, after division by Z_r and multiplication
by the density of V_delta, a bound of the form

    C delta^2 (t^2+delta^2)(1+|t|)^(-q)                  (D7)

for any prescribed finite q, by choosing sufficiently many Gaussian moments and
using the covariance sandwich. Constants depend only on the fixed compact model
parameters. The polynomial exponents are absorbed by Gaussian decay, not by an
independence assertion.

Let a=k r^3/delta^3. For delta>=r the possible t-values lie in [-a,a], with a
uniformly bounded. Integrating t^2+delta^2 over the actual second-height window
is at most C(a^3+delta^2 a). The first-height window has length k r^3. Combining
with the same polar and value-coordinate Jacobians as (R9), the pair intensity
integrated over locations, directions, and heights has the radial envelope

    delta<=r: C |E| r^3 delta ddelta;
    r<=delta<=eta_0:
              C |E| (r^12 delta^(-8)+r^6) ddelta.       (D8)

These are upper bounds; the two terms in the second line need not be separate
independent processes. At distances >=eta_0, [RC, Lemma 5] gives O(r^6), and
multiplication by any fixed nonnegative power of distance changes only its constant.

## 3. Integrability and positivity of the fixed-distance kernel

At the contact endpoint law Q_0, set both remote witness heights equal to b.
The same collision frame has exactly t=0. Equation (D6) then bounds each witness
determinant by C delta^2 K^d. Its product supplies delta^4, while the joint gradient/
height density supplies delta^(-d-3). Conditional moments remain uniformly bounded.
Hence for 0<delta<eta_0,

    Lambda_2(x,x+delta e) <= C delta^(1-d).               (D9)

The polar radial density is bounded, so (D4) is locally integrable for p>-1.
Elsewhere it is bounded on separated compact sets. This proves finiteness for
all p>=0. Full joint conditional support of the two Hessians and B_0 at distinct
sites makes Lambda_2 strictly positive off the diagonal. For a positive-volume
E, E x E has positive measure off the diagonal, indeed at some fixed positive
separation. Thus B_p>0.

For every fixed epsilon>0, the common-regression argument of [RM, Section 6]
gives uniformly on dist(x,x')>=epsilon the pair mean density

    k^2 r^6 Lambda_2(x,x') + O_epsilon(r^7).              (D10)

The fixed-distance contribution divided by r^6 therefore converges to the
corresponding part of B_p. An estimate uniform all the way to the diagonal is
not being assumed in (D10); (D8)-(D9) are what justify the limiting exhaustion.

## 4. Proof of the three regimes

For 0<=p<1, repeat the blown-up proof in REMOTE_PAIR_LAW.md with the extra factor
(delta/r)^p=s^p. Its original envelope s min(1,s^-3) now has an integrable pth
moment precisely in this range. The separated contribution is O(r^(1-p)) after
division by r^(5+p), so it vanishes. The radial identity is

    integral_0^infinity s^(p+1)(k-s^3|t|)_+ ds
       = 3 k^((p+5)/3)|t|^(-(p+2)/3)/((p+2)(p+5)).       (D11)

Multiplying by the same 36t^2 and substituting T=-12t yields (D2) and the first
line of (D5). The fixed-Borel spatial-indicator argument is unchanged.

For p>1, divide by r^6 and bound all distances below epsilon using (D8). The
part delta<=r is O(r^(p-1)). The r^12 term on [r,epsilon] becomes

    C r^6 integral_r^epsilon delta^(p-8) ddelta,

which tends to zero for each fixed epsilon: it is O(r^(p-1)) if p<7,
O(r^6 log(epsilon/r)) if p=7, and O(r^6 epsilon^(p-7)) if p>7. The remaining
r^6 term contributes at most C epsilon^(p+1). Therefore the normalized small-
distance mass has limsup <=C epsilon^(p+1). Combine (D10) with this bound and
let epsilon decrease to zero, using (D9). This proves the third line of (D5).

At p=1 split into delta<=Ar, Ar<delta<epsilon, and delta>=epsilon, with A>=1.
The first part divided by r^6 converges to the truncated microscopic coefficient
A_1(A), obtained from (D2)'s blown-up integral by s<=A. The third part converges
to B_1(epsilon). The middle part is bounded after division by r^6 by

    C A^-6+C epsilon^2,                                 (D12)

since r^6 integral_{Ar}^epsilon delta^-7 ddelta <= C A^-6.
All contributions are nonnegative. Take first r->0, then A->infinity and
epsilon->0. The truncated coefficients converge to A_1 and B_1, respectively,
and the middle bound vanishes. This proves the exact sum in the middle line of
(D5), without an unproved uniform-integrability assumption. In particular

    A_1=(k^2/(2z_0)) integral_E dx integral_S de
            p_{Y|Q0}(0,0,b) E[w_0 |T| (det A)^2 |Y=(0,0,b)].

## 5. The limiting scaled separation and its seventh-power tail

Normalize the ordered-pair mean by M_0(r) and set S_r=dist(x,x')/r. The L^1
blown-up convergence in REMOTE_PAIR_LAW.md implies total-variation convergence
of its probability law to a nondegenerate S on (0,infinity). This is again pair
weighting, not conditioning on an event and choosing a pair.

To describe its tail, define

    Psi_E(t)=integral_E dx integral_S de
        p_{V_0|Q0}(0,0,b,t)
        E_Q0[w_0(det A)^2 | V_0=(0,0,b,t)].

Here V_0's last coordinate is -T/12. After summing all indices the expression is
continuous and strictly positive at t=0; no artificial zero from the definition
of chi at T=0 is inserted into Psi. Uniform Gaussian regression also makes it
bounded near zero and rapidly decreasing after polynomial weights at infinity.
The limit density of S is

    g_S(s)=(36/(z_0 A_0)) s
           integral_R t^2(k-s^3|t|)_+ Psi_E(t) dt.        (D13)

With t=kv/s^3, the integral equals
k^4 s^-9 integral_{-1}^1 v^2(1-|v|)Psi_E(kv/s^3)dv.
Since the elementary integral of v^2(1-|v|) is 1/6,

    g_S(s) ~ [6k^4 Psi_E(0)/(z_0 A_0)] s^-8,
    P(S>R) ~ [6k^4 Psi_E(0)/(7z_0 A_0)] R^-7.            (D14)

Consequently E[S^p] is finite for 0<=p<7 and infinite for p>=7. For p<7 its
finite value is A_p/A_0. Near s=0, (D13) is O(s), so there is no additional
positive-moment obstruction there.

## 6. Why convergence in TV does not give convergence of these moments

Although the limit S has a finite first moment, (D5) implies

    E[S_r] -> (A_1+B_1)/A_0 > E[S]=A_1/A_0.              (D15)

For every p>1,

    E[S_r^p] ~ (B_p/A_0) r^(1-p) -> infinity.             (D16)

In particular this happens for 1<p<7 even though E[S^p]<infinity. The reason is
a vanishing pair-weighted mass of order r at fixed positive physical distances,
where S_r is of order 1/r. Its contribution to an unbounded pth moment is order
r^(1-p). Total variation controls bounded observables, not unbounded ones.

For 0<=p<1 the moments do converge, to A_p/A_0. Fixed quantiles of the physical
pair distance are asymptotic to r times the corresponding quantiles of S, while
its root-mean-square distance is asymptotic to sqrt(r B_2/A_0). This follows from
(D5), the strictly positive continuous density in (D13), and M_0(r)~A_0 r^5.
Neither quantiles nor moments here refer to uniformly selecting a pair from an
event-conditioned sample.

## 7. Review boundary

This note depends on the new remote pair limit in this packet plus the already
specified fixed-distance kernel in [RM]. The sharper determinant bound (D6),
height-constrained radial envelope (D8), diagonal integrability (D9), and the
p=1 two-cutoff limit are additional analytic obligations. The finite exact tests
check representative identities and power constants; they do not certify those
Gaussian or limiting arguments. All remote/model/mark restrictions and the
non-claims about global collisions, higher counts, elder selection, numerical
constants, and scientific status remain in force.
