# All-frame Gaussian essential and finite-lifetime rates

28 October 2026. OpenAI/Codex GPT-6 author-side candidate by `/root`, with
construction, controls and source analysis from `essential_template`,
`essential_gaussian_cost` and `next_marked_hypothesis`. Exact source identities
and limited reading roles are in [SOURCES.json](SOURCES.json). No qualifying
different-family scientific review or project status promotion is claimed.

## 1. A declared spectral class and the results

Fix d>=2 and L>0, and put omega=2pi/L. On the cubic torus take the centered
real stationary Gaussian field with covariance

    K_a(x)=sum_(n in Z^d) a_n exp(i omega n.x),
    a_n=a_(-n)>=0,
    a_n>0 for every ||n||_infinity<=3,
    sum_n sqrt(a_n)(1+|n|)^4 <infinity.                (1)

The spectrum is fixed; constants can depend on it, d and L. The class
includes the periodized Gaussian covariance and finite Fourier fields whose
spectral box contains this positive cube. No positivity outside the cube,
isotropy or analyticity is required. There is no uniformity over spectra.

Fix a compact birth interval I and J=[k_-,k_+] in (0,infinity). For every
unit direction u, translate the original pins to M=0,S=ru and use exactly

    f(M)=b, f(S)=b-kr^3, grad f(M)=grad f(S)=0,
    W_r=|det H_M det H_S| 1{H_M<0,index(H_S)=d-1},
    Z_r=E_Q W_r, P_r=(W_r/Z_r)Q_r.                    (2)

Q_r is the continuous Gaussian regression version at these original pins.
The index counts negative eigenvalues. Let death d_f(M) be the supremum of
path minima from M to strictly higher endpoints, with value -infinity if
none exists, and X_r=(b-d_f(M))/(kr^3). Define

    E_r={d_f(M)=-infinity},
    L_r={d_f(M)>-infinity, X_r>1}.

For sufficiently small r>0 the full normalizer is positive. Uniformly over
b in I,k in J and ALL orientations, there are positive constants such that

    exp(-C/r^2)<=P_r(E_r)<=C_0 exp(-c/r^2),
    exp(-C/r^2)<=P_r(L_r)<=C_0 exp(-c/r^2).             (3)

For every fixed q>0, writing T_q(r)=r^-3 E_Pr[X_r^q;L_r], there are positive
constants (allowed to depend on q) with

    c_q r^(-4q-3) exp(-C/r^2)<=T_q(r)
                                      <=C_q exp(-c/r^2). (4)

Consequently each probability in (3), and each T_q, has inverse-square
logarithmic order. This is a matching scale, not an optimal rate coefficient
or prefactor asymptotic. The construction also proves that a genuinely
finite lifetime of size at least a/r occurs with probability exp(-O(r^-2)).

These are path-functional statements. Essentiality is Borel since
E_r={max f<=b}; death is Borel by countable polygonal-path approximation,
as detailed in PR522's proof. No full C4 support, marked-law or global Morse
claim is imported for finite-spectrum fields. Ordinary barcode/elder-counting
identification retains any separate hypotheses it needs.

## 2. A fixed lattice right inverse, uniform through coalescence

Complete u to R in O(d), for writing observation rows only. For a function g
on the segment from0 to ru, use

    U0=(g(0)+g(ru))/2,
    U1=(g(ru)-g(0))/r,
    U2=(D_u g(ru)-D_u g(0))/r,
    U3=(6/r^2)[D_u g(0)+D_u g(ru)-2U1],

and for every transverse direction v_j, average D_vj g and the divided
difference (D_vj g(ru)-D_vj g(0))/r. This invertibly re-expresses all original
value/full-gradient pins. The target for f in (2) is

    v_r=(b-kr^3/2,-kr^2,0,12k,0,...,0).                (5)

Every row is uniformly bounded on C3. In particular the potentially singular
row is the exact average

    U3(g)=(6/r^3) integral_0^r t(r-t)D_u^3g(tu) dt.     (6)

Its nonnegative kernel has integral one. At contact the rows become
g,D_u g,D_u^2 g,D_u^3 g,D_vj g,D_u D_vj g at0.

Use the real trigonometric basis on the FIXED frequency cube [-2,2]^d,
and let J_(r,R) be its observation matrix. It has full row rank at contact
for every frame. Indeed, a row relation gives a differential polynomial of
total degree at most three, annihilating exp(i omega n.x) for each lattice
n in that cube. A polynomial of degree at most three in each variable
vanishing on the five-point grid in each coordinate is identically zero,
by successive one-variable interpolation. The rotated differential monomials
in the contact list are independent. Real sine/cosine pairs and the constant
encode exactly this exponential test.

Compactness of O(d), and uniform convergence of this FINITE matrix at r=0,
give J J^T>=lambda_D I on a common radius interval. The function

    D_(r,R)y=sum_j phi_j [J^T(JJ^T)^(-1)y]_j           (7)

is therefore an exact right inverse U D=Id, uniformly bounded from Euclidean
data to C4 and to the source RKHS. The latter holds because these finitely
many spectral weights are positive by (1). This fixed inverse is chosen
once; there is no growing-bandwidth/inverse-norm circularity or global choice
of a transverse basis on the sphere.

## 3. Explicit periodic trial fields in cube three

Let

    s_i(x)=sin(omega x_i)/omega,
    q(x)=sum_i 2(1-cos(omega x_i))/omega^2,
    s_*=s(ru), lambda=r/|s_*|, v=s_*/|s_*|,
    w=r s_*/|s_*|^2, ell(x)=w.s(x), z(x)=(Id-vv^T)s(x). (8)

For all small r, uniformly in u, lambda=1+O(r^2), w=u+O(r^2), v=u+O(r^2).
All denominators are nonzero. The hard penalty |z|^2 and its FULL gradient
vanish exactly at0 and ru, while ell(ru)=r. Use

    p=(L/2,0,...,0), q_p=q(p)=4/omega^2,
    Gamma=(2k_++1)/q_p,
    h_j=b-5kr ell^2+6k ell^3-2k q^2/r-|z|^2/r
                                         +j Gamma q^3/r, j=0,1. (9)

These are literal periodic trigonometric polynomials, not rotated local
polynomials. Every frequency lies in [-3,3]^d. Their RKHS norms are at most
C/r, uniformly over the parameter family, because their finitely many
coefficients are O(1/r) and all required variances are positive.

M already has the exact value and full gradient pins. At S,

    q(S)=r^2+O(r^4), grad q(S)=2s_*,
    grad ell(S)=u+O(r^2).

The field value defect is O(r^5), and every gradient defect is O(r^4).
For example the essential trial gradient there is exactly

    8kr^2 grad ell(S)-(8k/r)q(S)s_*=O(r^4).           (10)

The factor eight includes grad q=2s. The extra finite-lifetime term adds
only O(r^5) value and O(r^4) gradient defects. Thus the entire desingularized
observation defect is O(r^2); U3 divides the gradient error by r^2 and the
value error by r^3, while all other rows lose fewer powers.

Correct the pins by

    a_j=D_(r,R)(v_r-U h_j), hhat_j=h_j+a_j.

Then hhat_j has exactly (2), and

    ||a_j||_C4+||a_j||_H<=C r^2,
    a_j(0)=0, grad a_j(0)=0,
    ||hhat_j||_H<=C/r.                               (11)

The correction uses only cube-two modes. Final templates remain in cube
three. Exact row conversion, not a numerical solve at nearly singular raw
pins, establishes these identities.

## 4. Global essential geometry and the local sine chart

The global identity

    q-|s|^2=sum_i (1-cos(omega x_i))^2/omega^2>=0

implies q>=ell^2/lambda^2+|z|^2. For r small, lambda^4<=20/19. Therefore

    r(b-h_0)>=k ell^2[(19/10)ell^2-6r ell+5r^2]+|z|^2
             >=(k/14)(ell^4+r^2ell^2)+|z|^2.          (12)

The exact positive remainder is

    (19/10)ell^2-6r ell+5r^2-(ell^2+r^2)/14
           =(64/35)(ell-105r/64)^2+(3/448)r^2.        (13)

A zero in the actual deficit forces ell=z=0, hence s=0; the original
deficit then equals 2kq^2/r, forcing q=0 and x=M on the torus. Thus the
uncorrected essential trial already has a unique global maximum.
Outside any fixed small neighborhood of M, r(b-h_0) tends uniformly to
2kq^2+|P_(u perpendicular)s|^2, strictly positive there. This gives a
common positive gap of order1/r away from M.

Near M, use (ell,z) as a genuine local chart, choosing any orthonormal basis
of v-perpendicular for z. Its inverse is componentwise principal arcsine of
omega[(ell/lambda)v+z], divided by omega. On a fixed small product chart
both maps have uniformly bounded derivatives through order four, uniformly
in r and orientation. The pins map EXACTLY to (0,0),(r,0). No global choice
of transverse basis is needed; the template uses the projector itself.

Equation (11) and Taylor at M give |a_j|<=C r^2(ell^2+|z|^2) in this chart.
It is negligible relative to (12) for small r. A fixed bounded C4 zero-pin
field perturbation g is harmless as well. Its expression G in this chart
has a uniformly bounded C4 norm, zero values/full gradients at both pins,
and the Hermite/Taylor bounds

    |G(ell,0)|<=C_B ell^2(ell-r)^2,
    |grad_z G(ell,0)|<=C_B |ell(ell-r)|,
    |G(ell,z)|<=C_B[ell^2(ell-r)^2
                         +|ell(ell-r)||z|+|z|^2].     (14)

Use ell^2(ell-r)^2<=2(ell^4+r^2ell^2). Its coefficient C_B is absorbed
by k_-/(14r) as r decreases. Young's inequality absorbs the mixed term
into |z|^2/(4r)+C C_B^2 r ell^2(ell-r)^2, again negligible relative to the
axial margin. The last C_B|z|^2 is absorbed by |z|^2/r. The same arguments
leave a fixed fraction of the margin after adding a_j and g.

Consequently hhat_0+g has M as its unique global maximum for EVERY g in any
fixed bounded zero-pin C4 ball, once r is sufficiently small. Outside the
chart the order1/r deficit dominates a_j=O(r^2) and bounded g.

## 5. A separate finite, very long lifetime

For j=1 the numerator deficit subtracts Gamma q^3. In the sine chart,
q<=C(ell^2+|z|^2). On a small fixed chart of radius rho,

    Gamma q^3<=C Gamma[rho^2 ell^4+rho^4 |z|^2].       (15)

Choose rho small enough, independently of r and u, to absorb this into half
the ell^4 and |z|^2 margins in (12). The r^2ell^2 margin is not consumed.
Equations (11),(14) then preserve positivity near M for hhat_1+g as well.
On the boundary of a smaller fixed embedded ball about M, the surviving
numerator gap has a common positive lower bound a_*>0: the chart Jacobians
are uniformly nondegenerate, so ell^4+|z|^2 cannot vanish on that boundary.

At p, s=0, ell=z=0 and

    r(b-h_1(p))=q_p^2(2k-Gamma q_p)<=-q_p^2.          (16)

Thus an endpoint strictly older than b exists, even after a_j and bounded g.
All older points are outside the positive inner ball. Every continuous path
from M to an older point crosses its boundary, where f<=b-a_*/(2r).
The connected compact torus supplies a path, so death is finite and

    d_f(M)<=b-a_*/(2r),
    X_r>=a_*/(2k_+ r^4)>1.                           (17)

This is a global separating barrier for the finite-lifetime template. It
does not identify the pinned saddle S as the actual elder partner.

## 6. Literal pin types and determinant weight

In the sine chart the essential or finite trial Hessian at M has axial
entry -10kr, mixed entries0, and hard block -2I/r. At S, expansion of
q=ell^2/lambda^2+|z|^2+O((|ell|+|z|)^4) gives

    h_(ell ell)(S)=2kr+O(r^3),
    h_(ell z)(S)=O(r^3),
    h_(zz)(S)=-2I/r+O(r).                            (18)

The q^3 term contributes only O(r^3) to the axial entry there. The spatial
C4 correction has second derivatives O(r^2). Exact zero pins for g in the
chart give G_(ell ell)=O(B r^2), G_(ell z)=O(B r), G_(zz)=O(B) at both pins.

Hence the hard block remains negative of order1/r, its inverse is O(r),
and the mixed Schur correction is O(r^3). The soft Schur entries are
negative of order r at M and positive of order r at S, uniformly compact
marks. These are the required literal endpoint types. Since the final pins
are critical, Hessians transform by an ACTUAL congruence under the chart;
its Jacobian determinant is uniformly bounded above and away from zero.
The physical determinants therefore obey

    |det H_M|,|det H_S|>=c r^(2-d),
    W_r>=c r^(4-2d)>=c r^2, r<=1.                    (19)

No independence, surrogate type or restricted normalizer replaces the
original weight in this lower bound.

## 7. Gaussian and full-normalizer estimates for class (1)

We spell out why the earlier upper argument extends to (1). Its real Fourier
expansion has a finite C4 majorant S4=sum_j ||phi_j||_C4. Also (1) implies
sum a_n(1+|n|)^8<infinity. Thus all contact covariances and cross-covariances
needed through derivative order four are continuous, uniformly in frames.
The cube-two polynomial argument of §2 gives positive covariance for the
contact observations AND after appending the independent transverse Hessian
entries. Additional nonnegative spectral modes cannot destroy this rank.

Compactness yields a common covariance gap, bounded inverse and bounded pin
energy v_r^T Sigma_r^-1 v_r. Under Q_r, every original standardized Fourier
coefficient is m_j+eta_j, with |m_j|<=M0, centered Gaussian eta_j of variance
at most one; their correlations are retained. For K=1+||f||_C4, weighted
Jensen gives, with D0=1+M0 S4,

    E_Q exp(eta K^2)
       <=exp(2eta D0^2)(1-4eta S4^2)^(-1/2),
                                  0<eta<1/(4S4^2).    (20)

For completeness, K<=D0+sum_j w_j|eta_j|. Weighted Cauchy then Jensen on
finite sums, adding missing weight at zero, bounds the exponential square
by the Gaussian marginal integral; monotone convergence gives (20).
This proves a uniform estimate, not a growth inference from fixed moments.

The gradient pins and Hadamard yield W_r/r^2<=C_d K^(2d). The contact
transverse Gaussian A_0 has a full matrix density. With the correct
congruence diag(r^(-1/2),I), the pin Hessians converge jointly IN LAW to
diag(-6k,A_0),diag(6k,A_0). The singular-boundary set det A_0=0 is null.
Uniform integrability from (20) therefore gives, uniformly in compact marks
and frames,

    Z_r/r^2 ->36k^2 E[det(A_0)^2 1{A_0<0}]>0,
    z_* r^2<=Z_r<=z^* r^2.                           (21)

Continuity and compactness give the strict common floor, since a full
Gaussian matrix density charges a negative-definite ball. Dividing once
by Z_r and absorbing K^(2d) into (20) proves E_Pr exp(lambda K^2)<=C.
No full C4 support or almost-sure global Morse theorem is used here.

The deterministic sharp axial lemma of PR522 then implies

    E_r union L_r subset {K>=A/r}, A>0,

uniformly since k>=k_-. Exponential Markov proves the upper probabilities
in (3). On finite deaths, X_r<=2K/(k_-r^3); polynomial absorption in the
same exponential-square estimate proves the upper (4), including its r^-3
normalization. These arguments use only the stated spectral conditions.

## 8. Gaussian translation supplies both lower bounds

The centered conditional law nu_r has zero pins and
E_nu ||g||_C4<=S4 by marginal variance contraction. Its symmetric event
A_B={||g||_C4<=B}, with B=max(1,2S4), has probability at least1/2.
For either exact template hhat_j, hhat_j-mu_r lies in the conditional
Cameron-Martin pin kernel with norm at most ||hhat_j||_H<=C/r.
Translation and reflection on A_B give

    Q_r(hhat_j+A_B)
       >=nu_r(A_B) exp(-||hhat_j-mu_r||_H^2/2)
       >=(1/2)exp(-C_H/r^2).                         (22)

This is the cosh>=1 symmetry argument; it costs no new small-ball estimate.
The j=0 event is essential by §4. The j=1 event has finite lifetime at
least (17). Both have W_r>=c r^2 by (19). Dividing by the SAME full
Z_r<=z^*r^2 proves the lower (3) after absorbing a fixed prefactor.
Using (17) on the j=1 event gives the sharper displayed lower (4).

## 9. What improved and what remains

This removes the coordinate-axis restriction from the matching essential
scale, supplies a matching finite-long-lifetime scale, and derives both
for the wider explicit spectral class (1). Only a fixed finite set of
positive frequencies is needed; no approximate torus rotation or full-support
assumption is hidden in the construction.

The exponent constants are not optimal; the lower templates have large
hard curvature and are not claimed to minimize a Gaussian action. The
controlled vanishing-gap extension and an ordinary-H0 reading are supplied
below. Sharp rate limits, prefactors, uniformity across spectra/dimension/
volume and global counting intensities remain separate questions, as does
different-family scientific review of this packet. Historical proofs,
hypotheses and scientific status remain unchanged.

## 10. A controlled vanishing-gap extension and an actual obstruction

One can go further than the fixed positive gap floor. Fix k_+ and I but
allow 0<k<=k_+. Put beta=k/r. There are fixed M>=1 and r_*>0 such that,
uniformly for beta>=M, all orientations and these marks,

    c_1 exp(-C_1 beta^2)<=P_r(E_r),P_r(L_r)
                                      <=C_0 exp(-c_0 beta^2), (23)

and for every fixed q>0,

    c_q r^(-4q-3)exp(-C_1 beta^2)<=T_q(r)
                  <=C_q beta^(-q)r^(-4q-3)exp(-c_0 beta^2). (24)

These statements retain the explicit moment powers: simply substituting
beta^2 for r^-2 in (4)'s decaying upper bound would be false.

Here are the extra estimates needed to prove (23)-(24). The conditional
Gaussian estimate (20) remains uniform including k=0, because the target
vector and contact inverse remain bounded. The pin averages give

    alpha_M=f_uu(M)/r=-6k+O(rK),
    alpha_S=f_uu(S)/r=6k+O(rK),
    |f_uy(i)/r|<=C K.

The exact Hessian block determinant formula therefore refines (19)'s
upper-bound counterpart to

    |det H_i|/r<=C[kK^(d-1)+rK^d],
    W_r/r^2<=C[k^2K^(2d-2)+r^2K^(2d)],
    Z_r<=C r^2(k^2+r^2).                            (25)

For a lower floor, the entire transverse Gaussian A_M has uniformly bounded
mean and uniformly positive/bounded covariance on the compact family
0<=k<=k_+. It therefore charges a fixed strictly negative matrix ball with
probability p_A>0, uniformly. Choose B so that Q_r(K>B)<=p_A/2. Intersecting
with K<=B leaves probability at least p_A/2, with no independence assumption.
On this event A_S=A_M+O(rB) remains strictly negative. The axial errors and
Schur corrections are bounded by C r(B+B^2). A fixed sufficiently large M
makes these smaller than half the main terms 6k whenever k/r>=M.
The correct types and determinant lower bounds on this event give

    Z_r>=c k^2r^2, beta>=M.                          (26)

Dividing (25) by (26), using r/k<=1/M, and absorbing the polynomial factors
into (20) proves uniform E_Pr exp(lambda K^2)<=C on this whole wedge.
The escape exceptional set is K>=A beta, so exponential Markov gives the
upper probabilities (23). The finite-death size bound gives exactly the
upper (24), since k^-q r^(-3q-3)=beta^-q r^(-4q-3).

For the lower bounds, replace (9) by the SCALED trials

    h_j^sc=b+k[-5r ell^2+6ell^3-2q^2/r-|z|^2/r
                                      +j(3/q_p)q^3/r]. (27)

Every nonbirth term is multiplied by k. The pin correction is O(k r^2).
Its RKHS cost is O(1+beta), uniformly. The local radius for absorbing the
finite-template q^3 term is independent of k, since the same factor k
multiplies every part of that comparison. In the sine chart the essential
margin is now at least

    (beta/14)(ell^4+r^2ell^2)+beta |z|^2.

The fixed zero-pin residual bounds (14) are absorbed by choosing beta>=M
large; this requires a large ratio, not a fixed lower bound on k itself.
The finite profile has an older remote point at height at least b+beta q_p^2/2
and a separating drop a beta, after corrections and bounded noise.

At the pins, soft Hessian magnitudes are order k r=beta r^2 and hard
magnitudes are order beta. Noise errors are O(B r^2), O(B r), O(B) in
the soft, mixed and hard blocks. For large M the Schur error is smaller
than the soft margin. Consequently

    W_r>=c k^(2d)r^(4-2d)

on the translated fixed ball. Divide by the upper Z_r<=C k^2r^2 from (25).
The resulting prefactor is c beta^(2d-2)>=c. Cameron-Martin symmetry then
gives c exp(-C beta^2), proving the lower probabilities (23). The finite
event has X_r>=a/r^4, which proves the lower (24).

This also resolves a genuine boundary question. Along k=M r, essential
probability stays bounded below by a positive constant. Thus no upper bound
Ce^(-c/r^2) can hold uniformly over all k>0. Any pairing-failure event
containing essentiality likewise cannot satisfy a uniform O(r^3) estimate
over all positive gaps. This is an actual Gaussian-model obstruction to
dropping the parent's positive-gap restriction without replacing it by an
appropriate regime; it is not a defect in its stated compact-gap result.

Within beta>=M, (24) gives two further precise consequences:

- If beta^2/log(1/r) tends to infinity, T_q(r) tends to zero.
- If beta^2/log(1/r) tends to zero, T_q(r) tends to infinity.

The critical constant regime is not determined by these bounds. These are
tail conclusions, not a sufficient condition for the entire selection-failure
estimate, which includes mechanisms other than the essential event.

## 11. Conditional genericity and the ordinary-H0 reading

For a further conventional corollary, strengthen the finite positivity
assumption to a_n>0 on [-4,4]^d. Then for EACH fixed admissible pin
configuration, Q_r and P_r are almost surely Morse with distinct critical
values. This is derived at the actual null-pin regression version, not
transferred from unconditioned genericity.

The finite-Fourier interpolation argument is explicit. For a target x and
another site p!=x, choose a coordinate j on which they differ and use

    psi_p(z)=1-cos(omega(z_j-p_j)).

It vanishes in value and full first jet at p and is nonzero at x. Products
of these factors kill the first jets at all unwanted sites. Multiplying
by a trigonometric jet basis at x permits arbitrary desired jets there,
because multiplication by a nonzero value is triangular and invertible on
finite jets. A full second-jet basis fits in cube one: use 1 and sines
for values/gradients, 1-cos_i for diagonal second derivatives and
sin_i sin_j (i<j) for mixed derivatives.

Two killed old pins plus this second-jet basis fit in cube three, giving
full conditional second-jet covariance at every point off M,S. At a pin,
one filter killing the other pin times quadratic functions vanishing in
value/gradient at the target fits in cube two and makes its Hessian arbitrary.
For four distinct sites M,S,x,y, three filters times a first-jet basis fit
in cube four; thus their joint values/full gradients have full covariance.

Apply the elementary overdetermined-zero argument on compact separated
domains. A Lipschitz random map with a uniformly bounded Gaussian density
in R^p, parametrized by a q-dimensional compact domain with p>q, has no
zeros almost surely: on a sample C1 bound N, a mesh of size delta has at
most C delta^-q points; a zero implies a grid value in a ball of radius
C_N delta, with total probability O_N(delta^(p-q)). Let delta tend to zero,
then take the countable union over N and an exhaustion of the domain.

For off-pin Morse nondegeneracy use (grad f(x),Hf(x)v): its target dimension
is 2d, whereas (x,v in S^(d-1)) has dimension 2d-1. Conditional full second
jets give the required covariance rank; C3 sample bounds give Lipschitz
control. At the pins a full Gaussian Hessian misses det=0 almost surely.
For unequal off-pin critical points use
(grad f(x),grad f(y),f(x)-f(y)), with target dimension2d+1 and parameter
dimension2d. The four-site interpolation gives its conditional covariance.
Ties to a pinned height use (grad f(x),f(x)-b), or the lower pinned height,
with dimensions d+1>d. Exhaustions avoid pins and the pair diagonal.
The two pinned values are already distinct. Density bounds on the compact
domains are uniform there by covariance continuity and positivity. C4
samples provide all the needed derivative bounds. This proves the assertion
for Q_r at every fixed target; P_r follows from P_r<<Q_r.

For such fields the path-functional death used above is exactly the ordinary
superlevel-H0 elder death. The dimension-independent component argument is
already written in C96 §1 and the retained structural-universality proof §2.
Its conventional regularity requirements are met here: the finite-regularity
Morse lemma gives local quadratic charts for C4 functions, critical-free
gradient flow gives the deformation between critical levels, and compactness
plus isolated nondegenerate critical points gives finitely many critical
values. At a critical height the closed superlevel has locally path-connected
quadratic-cone charts; at a regular height it has half-space charts.

Consequently a component born at the strict maximum M has joined an older
component at height h precisely when it contains a point of value>b,
equivalently a path to such a point in {f>=h}. Taking the supremum of those
path minima gives its elder death. The unique global maximum is the one
essential class; other maxima give finite bars. This reuses the conventional
component proof with its finite-regularity justification. It does NOT
instantiate an all-orders IsSmooth Lean interface or supply new kernel
evidence. Nor does a uniform estimate imply one common probability-one set
over uncountably many pin parameters.

Thus (3)-(4) and (23)-(24) have their literal ordinary-H0 reading on this
slightly stronger spectral subclass, including the original periodized
Gaussian model. Counting intensities, marked limits, formal alignment and
scientific acceptance retain their separate scope and evidence requirements.
