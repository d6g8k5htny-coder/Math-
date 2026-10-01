# Mixed window geometry: the scale distinction and a fixed-scaled falsifier

Read-only source-bound mathematical note, 30 September 2026.
Disposition: AUTHOR_SIDE / HOLD. This note is not a new repository verdict,
count/rate packet, independent-provider review, or register transition.
Scientific effect NONE. No GitHub, STATUS, GRAPH, navigation, or source edits.

## Model and exact source boundary

Fix the variance-one periodized Gaussian field on a torus of side L>0,
an orthonormal frame, birth b in R, and positive gap mark k>0. The pins are
M=(-r/2,0), S=(r/2,0), their values are b,b-kr^3, and both gradients vanish.
Use the original endpoint Gaussian regression Q_r, endpoint determinant mark
W_r, and FULL endpoint-only normalizer Z_r=E_Qr W_r. Write P_r=Q_r^W.
N_r counts all additional critical points in I_r=(b-kr^3,b), excluding M,S.
In d=2, W_r=F_2(H_M)F_1(H_S). No adjacency or persistence selection is conditioned.

Immutable reads: main 98fdb54954a2d9ac0b8ba8ca03e279701f70d751;
PR162 head 382c0f9ff2281f43651ddbdf2e9b36dd52e2c6bf;
PR166 head be9b7fa95de9b7e59a67347640e157ed3027f624.
Full proofs and source manifests were fetched using GitHub tools. The proof
copies used below have matching Git blob hashes. Applications keep their source
hypotheses and review boundaries; publication does not remove those conditions.

| Tag | Exact path and Git blob | Interface used |
|---|---|---|
| MAIN-MIX | frontiers/c6_cluster_law_20260929/PROOF.md; ba492c8e62e58bfc055fc8254c790e893d346ba5 | Current repaired main proof, §5 Lemmas5.1–5.2, (5.3a)–(5.4) |
| C6 | frontiers/c6_palm_route_20260929/PROOF.md; 89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5 | §1 Theorem Q, total factorial upper bounds; ordinary fourth moment follows with the first moment |
| DL | frontiers/d5_dimension_lift_20260929/PROOF.md; 9d82c707fdb17d3072a8930f26dabedf59e456fc | Theorem I_d, (1.5)–(1.6), height-window shell and annulus bounds |
| CUB | frontiers/planar_cubic_cluster_20260929/PROOF.md; bb446d08db8a944537a743ad550b88c1c2ad5758 | §2 (C3)–(C11), exact planar classifier; §4 (G3), (G6)–(G10), compact-sector regression and rare density |
| SC | frontiers/spectral_cluster_closure_20260929/PROOF.md; 16c56821b52fd76b0be791622b9c3809eafde75a | PR162, §7 (23)–(24), fixed-origin-jet alternative mixed proof |
| TS | frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md; a32fd5f7d941bbe1fe943df045b1e0fbec8d691c | PR166, §4 Theorem L, (L1)–(L3) |

MAIN-MIX's actual successor review is OpenAI5360192822 at
f7c33955d005c03d1010835f52f500c4b853a847, bound to the blob above. It accepts
the repaired conditional theorem and specifically its near/far expectation.
It is source-exposed and provides zero organizational-independence credit.
This current 70131-byte proof differs from the historical 51313-byte source
1ce3769e76c540ab03b42f2deb6f2d1124459a81 criticized by SC.
MAIN-MIX SOURCE_MAP.json is blob ef51c582d0b1c874aabb01fce3b35c10631f7fc6.

SC's separate §7–8 ACCEPT is OpenAI5359879627, same-provider nonauthor scrutiny.
TS's actual conditional Slice A ACCEPT is Anthropic5360227991 at mathematical
head 7c82252533c3fe14ee262f7f87c0549c10968592, bound to the same TS blob.
TS SOURCES.json, blob59d11113e208965fefeaadd1bd5866585e77dc82, pins its SC/CUB/
RM/C6/P interfaces. That consumer review does not revalidate its parents.
The falsifier below consumes CUB's Gaussian (G6)–(G10) interface as a conditional
source premise; it does not infer acceptance of that interface from the separate
deterministic-classifier review. This note itself remains AUTHOR_SIDE / HOLD.

## What the existing scale statements establish

For fixed finite A>=4 and fixed positive physical rho, MAIN-MIX (5.4) gives

    P_r(N_A>0,N_far^rho>0)
        <= E_r[N_A 1{N_far^rho>0}] <= C_(A,rho) r^(9/2),

where N_A counts points in B(0,Ar) and N_far^rho those at physical distance
at least rho. Its remote covariance floor is proved by five-jet whitening,
with the complete raw collar frame and the residualized pin gradient frame.
All observation targets and the original W_r/Z_r are retained. Constants are
not uniform as A grows or rho shrinks.

This existing event estimate also implies the counted mixed little-o. Let
E={N_A>0,N_far^rho>0}. C6 and the first moment give E_r N_r^4<=Cr^3, and
N_A N_far^rho<=N_r^2 1_E. Hence

    r^-3 E_r[N_A N_far^rho]
       <= (r^-3 E_r N_r^4)^(1/2) (r^-3 P_r(E))^(1/2) -> 0.

SC has a different proof: its r^(9/2) estimate is only on a fixed compact
origin-jet box. Exhaustion gives its full o_(A,rho)(r^3) without claiming that
global polynomial rate. TS (L2) explicitly converts that result to counted
mixed pair mass. The two arguments and their review bindings are not interchangeable.

TS (L1) gives the stronger localization statement for ANY deterministic cutoff

    delta_r -> 0,                  delta_r/r -> infinity:

for every fixed q>=2, with N_in counting points inside delta_r,

    r^-3 E_r[(N_r)_q-(N_in)_q] -> 0.

Thus all leading second-factorial mass is inside every such shrinking physical
ball. Its coefficient is 2a2 and its ordered-pair limit is TS (L3). This is a
conditional PR166 result, not a main-register update. Its proof takes r->0 at
fixed near and remote cutoffs, then the near cutoff to infinity and the physical
remote cutoff to zero. No convergence rate or spatial-moment interchange is supplied.

DL's height-window intermediate estimate is uniform in A0 and rho:

    E_r N({A0 r<=|x|<=rho}) <= C r^3(A0^-2+rho^2),
    A0>=4, A0 r<rho<=s0.

It explains the middle-region sandwich. A shell s(r) with s/r->infinity and
s->0 is genuinely intermediate. In contrast, fixed A0 and fixed rho leave a
possibly nonzero r^3 coefficient. The following exact sector proves why a
fixed large multiple of r cannot be treated as a fixed physical remote cutoff.

## Exact fixed-scaled mixed sector

This construction is planar, d=2. Fix k>0. Pick an integer n>=4 and a fixed z>0.
Define

    alpha = (1/2) sqrt(1+3/n^2),
    lambda = 9k/(n^2 z^2),
    t = (n alpha+1)/(n+1),
    a=0,  beta=B=-lambda,  s=-lambda t,
    D=lambda(1-alpha)/((n+1)z),  c=2D.

Since 1/2<alpha<1, one has 1/2<t<1. CUB (C3) is

    P(u,Z)=2ku^3-3ku/2-k/2+sZ^2/2+B uZ^2/2+D Z^3/3.

Here a=0, so the sheared coordinate u equals the original axial coordinate X.
The endpoints have the required types because

    s=-lambda t < -lambda/2 = -|B|/2,

and their positive determinant product is

    w=9k^2(4s^2-B^2)=9k^2 lambda^2(4t^2-1)>0.

The two proposed extra roots are

    (u1,Z1)=(-alpha,z),          (u2,Z2)=(-1,-nz).

Their stationarity is exact. CUB (C7) requires

    Q=6k(u^2-1/4)+(B/2)Z^2=0,
    s+Bu+DZ=0                 when Z!=0.

At the first point, alpha^2-1/4=3/(4n^2), giving

    Q1=9k/(2n^2)-lambda z^2/2=0,
    s+B u1+D Z1
       =lambda[-t+alpha+(1-alpha)/(n+1)]=0.

At the second point,

    Q2=9k/2-lambda n^2 z^2/2=0,
    s+B u2+D Z2
       =lambda[1-t-n(1-alpha)/(n+1)]=0.

Both Z coordinates are nonzero. For B<0, CUB (C11) puts a root in the strict
height window precisely when u_w<u<-1/2, where

    u_w=-1/2-B/(2s)=-1/2-1/(2t)<-1.

Both roots satisfy this strict inequality since -1<u1<-1/2 and u2=-1.
For an explicit height check, CUB (C8) gives their downward normalized heights

    eta_i=-P(u_i,Z_i)/k
         =u_i+1/2+2t(u_i^2-1/4).

Thus

    eta1=(alpha-1/2)[-1+2t(alpha+1/2)]>0,
    eta2=(3t-1)/2 in (1/4,1).

For n>=4, alpha<=sqrt(19)/8<11/20 and t<2/3. Therefore eta1<1/50<1,
so both height inequalities can also be checked without the classifier.
Their Hessian determinants, by CUB (C8), are

    det Hess P at root1 = -3k lambda(4t alpha-1)<0,
    det Hess P at root2 = -3k lambda(4t-1)<0.

They are strict, nondegenerate saddles. The cubic has exactly these two extra
in-window points by Theorem C. They remain distinct and away from the pins.

## Pin and collar locations in physical coordinates

For z=1/10, the first root's physical distance from M is

    r sqrt((alpha-1/2)^2+1/100).

Using alpha-1/2<1/20, this is less than (sqrt(5)/20)r<r/4. It is positive,
so the root is in the punctured endpoint disk. Its midpoint distance is below
(sqrt(5)/4)r<4r. The second root's midpoint distance is

    r sqrt(1+n^2/100) > (n/10)r.

For any prescribed fixed A, choose the finite integer n>10A. The first point
is near the maximum pin and the second is outside the fixed scaled ball Ar.
Both distances still tend to zero physically with r.

For a compact-collar example instead take z=1. Then both distances from the
first root to the pins exceed r/4, and its midpoint radius is at most
(sqrt(83)/8)r<1.2r. It lies inside the fixed collar C(1/4,4). The second root's
radius exceeds nr; choose a finite n>A. These are two variants of the same
construction, not a change of the conditioned endpoint law.

Because n and z are fixed before r->0, a sufficiently large FIXED scaled radius
R contains both roots with strict spatial margins. For sufficiently small r,
the Rr chart embeds in the fixed torus. No limit n=n(r)->infinity is used.

## Positive Gaussian coefficient and the order on fixed scaled sets

Choose disjoint small bounded open spatial neighborhoods U,V of the two roots.
For z=1/10, ensure U lies in the punctured radius-1/4 disk about (-1/2,0) and
V lies outside the radius-A midpoint ball. For z=1, ensure U lies in C(1/4,4)
and V lies outside radius A. Both closures fit inside one fixed radius R ball.

The strict typing, heights, nondegenerate roots and spatial margins persist
on a sufficiently small compact four-dimensional jet box C of positive volume
around theta0=(s,a,beta,c). Allow a to vary in this box and evaluate positions
in the ORIGINAL coordinates X=u-aZ/(12k). Root continuity preserves the same
U,V inclusions after reducing the box. This avoids treating the measure-zero
slice a=0 itself as a positive Gaussian event.

On C, the two stable extra roots consist of exactly one point in U and one in V.
CUB (G6)–(G9) couple the actual endpoint-conditioned field on C, give C^2
convergence to this cubic in the fixed R ball, and yield

    W_r/r^4 -> w(theta),       Z_r/r^2 -> z0>0.

The same inverse-function/root-stability argument makes both spatial indicators
eventually one for almost every coupled realization and theta in C. Retaining
those indicators in CUB's actual disintegration (G10), then using its compact
domination, gives

    r^-3 P_r{Theta_r in C, N_(rU)>=1, N_(rV)>=1}
        -> m_C,
    m_C=z0^-1 integral_C w(theta) h0(0,a,beta,c) dtheta > 0.

Here h0 is the strictly positive contact Gaussian density from CUB (G2)–(G3).
On the compact box w and h0 have positive minima, so

    m_C >= (min_C w)(min_C h0) |C|/z0 > 0.

The power is the original rare-density ledger r*r^4/r^2=r^3: one curvature
coordinate A=rs, two soft endpoint determinants, and the FULL original normalizer.
No normalized soft-sector or witness-conditioned normalizer is introduced.

Consequently E_r[N_(rU)N_(rV)] has a positive order-r^3 lower bound.
Since U and V are disjoint,

    2 N_(rU)N_(rV) <= (N_r)_2,

and C6 Theorem Q supplies the order-r^3 upper bound. Conditional on those exact
source interfaces, this fixed-scaled mixed raw pair mass is therefore Theta(r^3).
The coefficient can become small as the fixed A and chosen n grow; it remains
strictly positive for every finite choice. This is consistent with all iterated
or shrinking-cutoff localization statements above.

Both counted extra points in this sector are saddles. Their factorial pair is
not a maximum–saddle persistence pair, and no elder matching of either point has
been asserted. That separate height-mark/selection problem is unchanged.
