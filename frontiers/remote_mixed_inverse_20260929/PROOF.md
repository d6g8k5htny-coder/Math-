# Mixed inverse distance and height-gap moments of remote critical-point pairs

Object: OA-REMOTE-MIXED-INVERSE-20260929-v1.
Author: OpenAI / ChatGPT, 29 September 2026.
Disposition: AUTHOR-SIDE MATHEMATICAL CANDIDATE; nonauthor analytic review required.
Scientific effect NONE. No existing source, review verdict, registry, graph, lemma
flag or prize is changed. All constants in the Gaussian claims are existential.

## 1. Exact objects and the new question

Use RM/RC/RP/RI in SOURCE_MAP.json. The field is the same variance-one periodized
Gaussian field on a fixed torus of side L, in a FIXED dimension d>=2. The original
maximum and saddle pins are M=-(r/2)u and S=(r/2)u, heights b and b-kr^3, with both
gradients zero. Birth marks b range over a compact real set, gap marks k over a
compact subset of (0,infinity) bounded away from zero; all orthonormal pin frames
are permitted. Constants may depend on these fixed parameters, never uniformly
on growing d,L or vanishing remote exclusion.

Q_r is the original endpoint-conditioned Gaussian law. Retain the full weight
W_r=F_d(H_M)F_(d-1)(H_S) and the endpoint-only normalizer Z_r=E_Qr W_r. The index
convention counts negative eigenvalues; F_j is the absolute determinant on index
j, zero at singular Hessians. Q_r^W=(W_r/Z_r)Q_r. No witness-conditioned denominator
or adjacency event is introduced.

Fix rho>0 and a deterministic positive-volume Borel E inside the same remote
region D_rho. E is FIXED as r varies. Count every critical index in E with height
in I_r=(b-kr^3,b). All pairs are ordered and distinct. Write

    delta=dist(x,x'), Delta=|f(x')-f(x)|,
    theta=(b-f(x))/(kr^3), theta'=(b-f(x'))/(kr^3),
    G=|theta-theta'|=Delta/(kr^3).

For nonnegative inverse exponents q,beta define the nonnegative extended moment

    H_(q,beta)(r)=E_Qr^W sum_(x!=x') delta^(-q) Delta^(-beta).    (M1)

The sums are over counted pairs. Powers zero are one. At zero height difference,
negative powers are defined by increasing truncation. Distinct critical values
hold on the generic locus; equivalently, the off-diagonal value density shows
that this zero-height set has zero expected pair count. Tonelli/truncation makes
(M1) well-defined without assuming its integrability. Almost-sure finite point
counts do not imply finite expectations of inverse powers.

This note asks for the simultaneous distance AND actual height-gap singularity.
A product of two separately finite-moment claims is not enough. The cubic relation
Delta=delta^3|t| makes their strengths interact. RP's unweighted gap law and RI's
inverse-distance theorem are credited, not presented as new results here.

Put lambda=q+3beta. The claimed finite domain in the nonnegative quadrant is

    q>=0, beta>=0, lambda<2.                                  (M2)

### Theorem M: sharp domain, asymptotic coefficient and tilted height law

For every sufficiently small fixed r>0, (M1) is finite IF AND ONLY IF (M2) holds.
For each fixed (q,beta) in (M2), as r goes to zero,

    H_(q,beta)(r)=r^(5-q-3beta) D_(q,beta)+o(r^(5-q-3beta)),      (M3)

with a strictly positive finite contact coefficient specified below. Uniformity
is on the fixed compact mark/frame sets for this fixed E; no little-o rate or
uniformity up to the exponent boundary is asserted.

Let A_p be RI's microscopic distance coefficient. Then

    D_(q,beta)=k^(-beta) A_(-q)
              (2-q)(5-q)/[(2-q-3beta)(5-q-3beta)].             (M4)

Define a probability measure by weighting the EXPECTED ordered-pair measure with
delta^(-q)Delta^(-beta), and normalizing by H_(q,beta)(r). This is not a rule for
sampling a field conditioned on multiple points. Its joint height-deficit law
converges in total variation (the probability convention) to

    h_alpha(a,b)=alpha(alpha+1)|a-b|^(alpha-1)/2,
    alpha=(2-q-3beta)/3>0,       (a,b) in (0,1)^2.              (M5)

Thus G tends to Beta(alpha,2), with

    E G=alpha/(alpha+2),
    Var G=2alpha/[(alpha+2)^2(alpha+3)].                        (M6)

These are limits of weighted critical-point marks, not persistence lifetimes.
At q=beta=0, alpha=2/3 recovers RP, including mean1/4 and variance9/176. Inverse
distance weighting q=1,beta=0 gives alpha=1/3 and mean1/7. The same height law
comes from q=0,beta=1/3, but the location/direction/jet weighting is different.
No equivalence of those full pair measures is claimed.

### Fixed-r diagonal refinement and cutoffs

For 0<=beta<1, let j_(r,beta)(delta) be the radial expected pair density weighted
by Delta^(-beta), but NOT by delta^(-q). At each fixed sufficiently small r,

    j_(r,beta)(delta)~J_(r,beta) delta^(1-3beta),
    0<J_(r,beta)<infinity.                                    (M7)

For fixed delta_0>0 in the collision chart and beta<1, restrict (M1) to
 epsilon<delta<=delta_0. As epsilon decreases to zero with r fixed,

    lambda=2: H_cut~J_(r,beta) log(delta_0/epsilon),
    lambda>2: H_cut~J_(r,beta) epsilon^(2-lambda)/(lambda-2).    (M8)

No bounded remainder at the logarithmic threshold follows from (M7). For beta>=1,
a positive distance cutoff need not regularize the height-gap singularity; (M8)
is deliberately not asserted there. Infinite total moments for that range are
proved separately below. No arbitrary coupled cutoff epsilon(r) is claimed.

## 2. What is actually imported

RM supplies smooth conditional regression, positive Fourier spectrum and the
independence of distinct derivative functionals, the original full normalizer,
deterministic endpoint identities and all required finite field-norm moments.
RC supplies the two-witness Kac-Rice measure, its collision observation frame,
a joint covariance floor through r=delta=0, target-density decay times conditional
moment bounds, and the fixed-positive-separation estimates. RP supplies the coupled
conditional field construction, determinant limits and fixed-Borel translation
argument. RI identifies A_p and the positive fixed-r conditional jet list.

These are used at their exact fixed-remote scopes. In particular W_r/r^2 under
ADDITIONAL witness conditioning uses coupled field moments and endpoint identities.
Z_r/r^2->z_0 is a SEPARATE endpoint-only assertion. The latter alone would not
supply the former. The three relevant spatial sites at fixed r are M,S,x; at
positive witness separation there are four. The full observation vectors are
nonduplicated. The fixed-r support argument is not a uniform full endpoint-Hessian
covariance assertion as r tends to zero.

C4's p=1 distance crossover and its upper tail are not needed by this proof.
C5's single-point height law is a different sampling object and is not an input.
No historical blocked executable is consumed or recreated.

## 3. Uniform weighted domination in the two collision variables

In a near-diagonal chart, x'=x+delta e with delta<eta_0<=rho/2, use RC's EXACT frame

    V_delta=(grad f(x), [grad f(x')-grad f(x)]/delta, f(x),
       [f(x')-f(x)-(delta/2)e.(grad f(x)+grad f(x'))]/delta^3).

At the zero gradient targets its last coordinate is t=(f(x')-f(x))/delta^3.
Its delta=0 extension is (grad f,H e,f,-T/12), with T=D^3f[e,e,e]. Put

    delta=r s, f(x)=b-r^3 z.

The two height windows are exactly

    0<z<k,        (z-k)/s^3<t<z/s^3.                           (M9)

The physical inverse weight is

    delta^(-q)Delta^(-beta)=r^(-q-3beta)s^(-q-3beta)|t|^(-beta).

No k factor occurs in this expression; a k factor reappears on converting to
normalized gap G. Dropping it later would confuse actual and normalized gaps.

RP's unweighted blown-up expected pair density, after /r^5, is bounded by
C s(1+|t|)^(-N)1_(M9) for any sufficiently large N. Hence the weighted density,
after dividing by r^(5-q-3beta), has the uniform bound

    C s^(1-q-3beta)|t|^(-beta)(1+|t|)^(-N)1_(M9).              (M10)

In (M2), beta<2/3<1. For s<=1, the z range has bounded length and the t factor is
integrable on the real line, giving C s^(1-q-3beta). For s>=1, the windows imply
|t|<k/s^3, and integrating |t|^(-beta) over that interval gives at most
C s^(-3(1-beta)). The integrated bound is therefore

    C s^(1-q-3beta) for s<=1,
    C s^(-2-q) for s>=1.                                      (M11)

Both ends are integrable exactly on (M2) within q,beta>=0. This statement concerns
the envelope; the necessity direction for the ACTUAL moment is not inferred from
failure of an upper bound, and will be proved by a positive diagonal coefficient.

For rigor with arbitrary fixed Borel E, first truncate s to [s_0,S_0], t away from
zero and infinity, and then remove 1_E(x+rse) by continuity of translation in L1.
On the truncated sets the remaining coefficients are uniformly bounded. The
integrable (M10) controls the removed regions, and (M11) controls the s tails.
This avoids assuming almost every boundary point of E has a useful pointwise
limit. It does not permit arbitrary oscillating E_r or field-selected sets.

At separated positions delta>=eta_0, the weight delta^(-q) is bounded. The joint
value density times all determinant moments is uniformly bounded over the compact
height targets by distinct-site regression. Since beta<1,

    integral_(I_r x I_r) |y-y'|^(-beta)dy dy'
      =2(kr^3)^(2-beta)/[(1-beta)(2-beta)].                    (M12)

The separated contribution is O(r^(6-3beta)), which divided by r^(5-q-3beta) is
O(r^(1+q)) and tends to zero. This argument uses the full value density; an
unweighted separated-pair bound alone would not control the inverse height gap.

## 4. Compute the coefficient without discarding correlations

Let Q_0 be the contact endpoint Gaussian law, with contact weight w_0 and full
normalizer z_0>0. At remote x and direction e set

    Y=(grad f(x),H_x e,f(x)),
    A=H_x restricted to e-perp, T=D^3f(x)[e,e,e].

At bounded nonzero t, the coupled limit of the normalized determinant product is
36t^2(det A)^2, while W_r/r^2->w_0 under this same conditioning. Let
Psi(x,e,t) denote the conditional target density of (Y,-T/12) at (0,0,b,t) times
E[w_0(det A)^2 | Y=(0,0,b),-T/12=t]. This is a nonnegative smooth-in-target Gaussian
weighted density with sufficient integrable moment control, not a product of
independent Hessian/height distributions. The ordinary sphere measure is de.

Integrating z in (M9) gives (k-s^3|t|)_+. Put lambda=q+3beta. For t!=0,

    integral_0^infinity s^(1-lambda)(k-s^3|t|)_+ ds
      =3 k^((5-lambda)/3)|t|^(-(2-lambda)/3)
         /[(2-lambda)(5-lambda)].                            (M13)

Indeed the upper root is s_max=(k/|t|)^(1/3), and direct integration gives
k s_max^(2-lambda)/(2-lambda)-|t| s_max^(5-lambda)/(5-lambda).
Multiplying by 36|t|^(2-beta) yields the exponent

    2-beta-(2-q-3beta)/3=(4+q)/3.                              (M14)

The beta-dependence cancels in this T moment, but NOT in the coefficient or its
k exponent. Converting t=-T/12 gives

    D_(q,beta)=
      3*12^((2-q)/3)*k^((5-q)/3-beta)
      /[4(2-q-3beta)(5-q-3beta)z_0]
      * integral_E dx integral_S de p_(Y|Q0)(0,0,b)
          E[w_0 |T|^((4+q)/3)(det A)^2 |Y=(0,0,b)].            (M15)

In (M2), 0<=q<2, so the exponent of |T| lies in [4/3,2). All needed moments
are finite. The positive full conditional support in RP/RI makes the integral
strictly positive. Its uniform compact-parameter finiteness and continuity follow
from the same regression/moment bounds. The k power in front is NOT a pure scaling
law: Q_0 also depends on k through the endpoint target f_xxx(0)=12k.

(M10) and the coupled convergence prove weighted L1 convergence of the complete
blown-up densities. Tonelli away from t=0 followed by monotone exhaustion proves
(M15) without assigning meaning to an undefined zero-times-infinity product.
This proves (M3). Comparing (M15) with RI's A_p at p=-q proves (M4).

## 5. The universal height law after mixed weighting

For t!=0 set g=s^3|t|/k. The weighted radial element transforms as

    s^(1-q-3beta)ds
      =(1/3)(k/|t|)^alpha g^(alpha-1)dg,
    alpha=(2-q-3beta)/3.

With z=k theta, for each sign of t the allowed lower of the two deficit marks
ranges freely over (0,1-g). The leading density has no dependence on that lower
mark. The remaining t power is again (4+q)/3, independent of beta. Thus the gap
has unnormalized density g^(alpha-1)(1-g), and

    integral_0^1 g^(alpha-1)(1-g)dg=1/[alpha(alpha+1)].          (M16)

Interchanging the ordered pair swaps the two heights, leaves delta and Delta
unchanged, and preserves its expected weighted measure. Equal heights are null.
Consequently both triangles have equal mass. This proves (M5), including its
factor one-half, and G~Beta(alpha,2). Conditional on G=g, the smaller deficit is
uniform on (0,1-g), and the orientation is equiprobable. These statements describe
the LIMIT law; exact finite-r uniformity or independence is not claimed.

Weighted L1 convergence from Section 4 contracts under the measurable height
pushforward; normalization by its converging positive mass proves probability TV
convergence in (M5). This is not deduced from RP's UNWEIGHTED TV convergence, since
our inverse weights are unbounded. All bounded limiting height moments follow.

The marginal deficit density and height correlation are

    f_alpha(a)=(alpha+1)[a^alpha+(1-a)^alpha]/2,
    Corr(theta,theta')=(2-alpha-alpha^2)/(2+alpha+alpha^2).      (M17)

To derive the correlation, use the conditional uniform smaller mark: writing
m1=E G and m2=E G^2, E theta^2=1/3-m1/6+m2/3 and
E(theta theta')=1/3-m1/6-m2/6, with E theta=1/2. This gives (M17) and recovers
2/7 for the original alpha=2/3 law, versus 7/11 at alpha=1/3.

As a SEPARATE exponent-boundary limit taken AFTER the field limit, alpha down to
zero gives G->0 in probability and the marginal density tends to uniform in L1.
The joint law therefore tends weakly to (U,U), U uniform on (0,1). Its TV distance
from that diagonal law is nevertheless exactly one for every alpha>0, since the
joint density is absolutely continuous and the diagonal measure is singular.
This boundary observation does not justify a simultaneous r/exponent limit.

## 6. A positive fixed-r coefficient proves necessity

First fix 0<=beta<1 and a sufficiently small positive r. Use the SAME full RC
value-gradient frame at x,x+delta e, but now integrate y=f(x) directly over I_r.
The second height is y'=y+delta^3t, with dy'=delta^3dt. Its contribution has the
radial factors

    delta^(d-1) * delta^(-d-3) * delta^3 * delta^2
        * delta^(-3beta) = delta^(1-3beta).                    (M18)

The normalized pair determinants divided by delta^2 tend to (T^2/4)(det A)^2.
For almost every y in I_r and bounded t, the second window indicator tends to
one. The fixed-r coupled field moments bound the pre-limit integrand by
C_r |t|^(-beta)(1+|t|)^(-N)1_{y in I_r}. This is integrable for beta<1. Boundary
heights are Lebesgue null; no indicator is differentiated. Integrable truncation
and the fixed-Borel L1 translation remove the second spatial indicator as before.
Thus (M7) follows with

    J_(r,beta)=12^beta/(4Z_r) integral_E dx integral_S de
      p_(grad f(x),H_x e |Q_r)(0,0)
      E_Qr[W_r 1_{f(x) in I_r}|T|^(2-beta)(det A)^2
                         |grad f(x)=0,H_x e=0].               (M19)

The raw finite-r observation list and endpoint/witness Hessian/third-derivative
complements have positive covariance at their distinct sites, by RM/RI's exact
positive-spectrum argument. They charge the open set with correct endpoint
indices, witness height strictly inside I_r, nonsingular A and nonzero T.
The integrand in (M19) is strictly positive there. Compactness in x,e at FIXED r
and bounded conditional moments give 0<J_(r,beta)<infinity. No uniform full raw
endpoint-Hessian covariance floor as r->0 is inferred from this fixed-r claim.

The positive radial asymptotic, rather than a failed envelope estimate, gives
integrability exactly when 1-q-3beta>-1 for beta<1. Separated-position finiteness
uses (M12). The matching lower and upper comparisons near zero prove the cutoff
equivalences (M8) by first fixing a coefficient-error tolerance, then sending
epsilon to zero, then sending that tolerance to zero. No quantitative error rate
in (M7) is available, so no bounded logarithmic remainder is claimed.

For beta>=1, take the already divergent moment at q=0,beta_0=2/3. Every counted
height gap satisfies 0<Delta<ell_r=kr^3. Also delta is at most the finite torus
diameter D_T. For q>=0,

    delta^(-q) Delta^(-beta)
      >= D_T^(-q) ell_r^(-(beta-beta_0)) Delta^(-beta_0).        (M20)

The prefactor is strictly positive for fixed r, and Tonelli preserves the
inequality. Hence (M1) is infinite there. This closes the entire nonnegative
quadrant without wrongly claiming that a distance cutoff makes a beta>=1
height singularity integrable. The fixed-r necessity and sufficiency are proved.

## 7. Contact matching and a residue check

For beta<1, disintegrate (M19) in y=b-kr^3theta, giving dy=kr^3dtheta. The contact
frame (U_r,grad f,H e,f) has the uniform covariance sandwich through r=0.
Extra-conditioned endpoint identities and moment bounds give W_r/r^2->w_0;
separately Z_r/r^2->z_0. Since 2-beta>1, the T moment is continuous and uniformly
integrable. Dominated convergence therefore yields

    J_(r,beta)/r^3 -> J_(0,beta)>0,
    J_(0,beta)=12^beta k/(4z_0) integral_E dx integral_S de
       p_(Y|Q0)(0,0,b)E[w_0|T|^(2-beta)(det A)^2|Y].           (M21)

For fixed beta in [0,2/3), increase q to q_*=2-3beta from below. Formula (M15)
and dominated continuity of its positive T moments give the residue identity

    (2-q-3beta)D_(q,beta) -> J_(0,beta).                       (M22)

At the boundary the remaining denominator is3, the power of12 becomes beta,
the k power is1, and the T power is2-beta. This checks the collision coefficient
and the microscopic coefficient independently; it is not a theorem about
arbitrary coupled limits q(r), beta(r) or epsilon(r).

## 8. Scope and falsification targets

The new conclusions are the sharp coupled domain, the mixed coefficient, the
weighted beta family, and the fixed-r weighted diagonal/cutoff/contact formulas.
The cases beta=0 reuse RI, and q=beta=0 reuse RP. No generic critical-point
repulsion, Kac-Rice theorem, beta integral or Gaussian regression identity is
claimed as an invention. Limited primary-source reconnaissance is recorded;
no exhaustive novelty or worldwide-priority claim is made.

Nonauthor review should target: the t=0 singularity before and after conditioning;
both integrated ends of (M10); the actual two-height separated estimate (M12);
beta cancellation in (M14); preserving W once/Z once; positivity of (M19), not
just an upper envelope; fixed-r versus contact/exponent limits; and probability
TV on the correctly WEIGHTED expected-pair measure. No same-index threshold,
field-event sampling law, arbitrary real two-exponent domain, uniform-in-d bound,
rho->0 extension, C4 crossover import, numerical Gaussian coefficient, or global
pin-inclusive assertion is included.

The finite suite checks rational exponents, coefficient factors, beta moments,
correlation, cutoff algebra and boundary sensitivity. It does not prove a Gaussian
covariance floor, Kac-Rice applicability, weighted dominated convergence or the
support argument. Those remain the written analytic obligations above. The new
program is not a reconstruction of #116's unavailable historical executable.
