# The large critical ratio has the sharp global essential action

29 October 2026. OpenAI/Codex GPT-6 author-side continuation, with
`large_tau_bridge` and `contact_stability` as same-family author support.
This is a conventional mathematical argument, not qualifying different-family
scientific review or a project-status promotion. No predecessor file is changed.

## 1. Statement, original conventions and the order of limits

Fix d>=2, L>0, omega=2pi/L and the centered real stationary Gaussian field
on T_L^d with covariance

    K(x)=sum_(n in Z^d) a_n exp(i omega n.x),
    a_n=a_(-n)>=0,
    a_n>0 for ||n||_infinity<=3,
    sum_n sqrt(a_n)(1+|n|)^4<infinity.                (LR1)

The spectrum, dimension, volume and unit direction u are fixed. Let H be
the source RKHS with its original covariance normalization. Use precisely
the original Gaussian regression and determinant tilt at M=0,S=ru:

    f(0)=b, f(ru)=b-kr^3, grad f(0)=grad f(ru)=0,
    Q_(r;b,k,u)=the canonical conditional Gaussian law,
    W_r=|det H_0 det H_ru|1{H_0<0,index(H_ru)=d-1},
    P_(r;b,k,u)=(W_r/E_Q W_r)Q_(r;b,k,u),
    E_r={max f<=b}.                                 (LR2)

The Hessian index counts negative eigenvalues. As in the predecessor
path-functional convention, E_r is essentiality.

Let U_0 consist of value, axial first/second/third derivatives, transverse
first derivatives and axial-transverse second derivatives at0. In a fixed
orthonormal (u,y) frame, the contact law Q_(0;b,u) is regression at

    f(0)=b, grad f(0)=0,
    D_u^2 f(0)=0, D_u D_y f(0)=0, D_u^3 f(0)=0.      (LR3)

Under this law define

    A=D_y^2 f(0), B=D_u^2 grad_y f(0), c=D_u^4 f(0),
    Delta=det A,
    Y=(c/12)Delta-(1/4)B^T adj(A)B,
    gamma=c/12-(1/4)B^T A^-1 B on {A<0},
    w_tau=(36tau^2 Delta^2-Y^2)_+1{A<0},
    z_b(tau)=E_(Q_(0;b,u)) w_tau.                   (LR4)

All uses of gamma below occur on A<0. In particular singular matrices
require no inverse convention. Put

    p_E(tau;b,u)
      =E_(Q_(0;b,u))[w_tau 1{gamma<-2tau,max f<=b}]/z_b(tau).
                                                        (LR5)

The critical-window theorem [CW, (CW8)] gives, for each fixed b,u,tau>0,

    lim_(r downarrow0) P_(r;b,tau r,u)(E_r)=p_E(tau;b,u).
                                                        (LR6)

Here the second pin is b-tau r^4. Formula (LR6), including its original
weight, is reused rather than claimed anew.

Define the already established sharp-action minimum [SA, (SA2)]

    C_(1,u)={g in H: g<=0 everywhere, g(0)=0,
                         D_u^2g(0)=0, D_u^4g(0)<=-24},
    I(1,u)=(1/2)min_(g in C_(1,u)) ||g||_H^2.       (LR7)

**Theorem.** For every compact birth interval K and this fixed u,

    lim_(tau->infinity) sup_(b in K)
       |tau^-2 log p_E(tau;b,u)+I(1,u)|=0.          (LR8)

In particular the ordered bridge is

    lim_(tau->infinity) tau^-2 log[
        lim_(r downarrow0) P_(r;b,tau r,u)(E_r)]
      =-I(1,u).                                    (LR9)

This is the same global RKHS energy as the fixed-positive-k theorem
[SA, (SA3)--(SA4)], which states

    lim_(r downarrow0) r^2 log P_(r;b,k,u)(E_r)
      =-I(k,u)=-k^2 I(1,u),   k>0 fixed.            (LR10)

The birth uniformity in (LR8) concerns only the already defined contact
share p_E. No uniformity of the inner r limit in (LR6), interchange of
limits, joint r,tau limit, direction uniformity, or uniformity over spectra,
dimensions or volumes is asserted. The conclusion is a logarithmic rate,
not a probability-prefactor asymptotic or an evaluated numerical minimum.

## 2. Fixed contact regression and its Gaussian action

Write the contact regression as

    f=mu_b+G,
    mu_b=R_0(b,0,...,0),
    G=F-R_0U_0F,    nu=law(G).                      (LR11)

The bounded regression map R_0 is fixed once u and the source spectrum are
fixed. Thus nu is independent of b, and mu_b is bounded in C4 and H when
b ranges over K. The conditional Cameron-Martin space is

    H_0=H cap ker U_0

with its inherited H norm. This follows because Id-R_0U_0 is the orthogonal
projection on H off the contact observation-representer span. The finite
covariance gap follows from the positive frequency cube in (LR1).

The centered fields G/tau obey the good Gaussian C4 large-deviation
principle at speed tau^2 with rate

    J(g)=(1/2)||g||_H^2 for g in H_0,
         +infinity otherwise.                      (LR12)

The construction and normalization of this LDP are [SA, section2]. In
particular (LR1) gives a real Fourier expansion with summable C4 mode norms.
After the bounded contact projection, finite Fourier truncations give
finite-dimensional Gaussian LDPs; omitted tails have exponential-square
bounds whose parameters tend to infinity. The coordinate map ell2->C4 is
compact, identifying the good rate and inherited norm in (LR12). This
argument neither requires nor asserts full C4 support. The fixed drift
mu_b/tau tends to zero uniformly for b in K, although the proof below can
use the single centered law nu throughout.

Every g in C_(1,u) belongs to H_0. Indeed a C4 maximum at0 has zero gradient
and negative-semidefinite Hessian. Its zero axial quadratic entry forces
the whole axial Hessian row to vanish. Its restriction to the axial line
has zero third derivative, since a nonzero cubic would be positive on one
side of0. Thus the contact constraints add no restriction to (LR7).

For later use recall why its strict recovery profiles exist [SA, sections4--5].
Let

    q(x)=sum_i 2(1-cos(omega x_i))/omega^2,
    s_i(x)=sin(omega x_i)/omega,   P_u=Id-uu^T.

The finite Fourier field -q^2 is feasible and has axial fourth derivative
-24. The feasible set is closed and convex in H, so it has a unique
minimum-norm element g_*. Its norm is strictly positive, since the fourth
derivative functional is bounded and its value is at most -24. Scaling
would decrease the norm if its fourth derivative were strictly smaller
than -24; hence c(g_*)=-24. Total spatial inversion is an RKHS isometry
preserving the feasible set. Uniqueness makes g_* even and hence B(g_*)=0.

For 0<epsilon<2 set

    g_epsilon=g_*-epsilon q^2-epsilon|P_us|^2.       (LR13)

These fields belong to H_0 and converge to g_* in H. They have unique
global maximum0 at0 because q>0 away from0. Their contact jets satisfy

    A_epsilon<0, B_epsilon=0,
    c_epsilon=-24(1+epsilon),
    gamma_epsilon=-2(1+epsilon) in (-6,-2).          (LR14)

Here the sine penalty has hard transverse Hessian -2epsilon I, zero axial
Hessian and zero axial fourth derivative: P_us(tu)=O(t^3). All added modes
belong to the positive finite spectral cube. The underlying minimizer,
evenness and construction (LR13) are reused from [SA].

## 3. The full normalizer and polynomial weight moments

Let m=d-1 and define

    C_b=36 E_(Q_(0;b,u))[Delta^2 1{A<0}].           (LR15)

The Gaussian vector A has a full density on Sym(m), by the contact jet
rank argument in [CW, section2]. Thus C_b is finite and strictly positive.
Using the inverse-free polynomial Y in (LR4),

    0<=36Delta^2 1{A<0}-w_tau/tau^2
      =min(36Delta^2,Y^2/tau^2)1{A<0}
      <=Y^2/tau^2.                                 (LR16)

Consequently dominated convergence gives

    z_b(tau)/tau^2 -> C_b.                          (LR17)

This also holds uniformly on K, with an O_K(tau^-2) error: in the common
coupling (LR11), A_b,B_b,c_b depend affinely on b and Gaussian jets, while
Y_b is a polynomial in those variables. Hence E sup_(b in K)|Y_b|^2<infinity,
and (LR16) gives the claimed bound directly.

The function A->(det A)^2 1{A<0} is continuous, including at the boundary
of the negative-definite cone, where det A=0. Gaussian polynomial moments
and the affine mean dependence therefore make C_b continuous in b.
Its positivity gives a positive minimum on K. In particular, for all
sufficiently large tau,

    c_K tau^2<=z_b(tau)<=C_K tau^2,   b in K.        (LR18)

For every fixed p>1 the literal original contact weight satisfies

    0<=w_tau/tau^2<=36Delta^2 1{A<0},
    sup_(b in K,tau>=1) E_(Q_(0;b,u))
                            [(w_tau/tau^2)^p]<infinity. (LR19)

Only polynomial Gaussian moments are used. There is no inverse-matrix
moment assumption or substitute normalizer.

## 4. Upper bound: the negative sector forces the same global cone

On A<0, its inverse is negative definite. Therefore

    gamma=c/12-(1/4)B^T A^-1B>=c/12,
    gamma<-2tau implies c<-24tau.                  (LR20)

Let T_(tau,b) be the event in (LR5), also including A<0; its intersection
with the support of w_tau is exactly

    {A<0,-6tau<gamma<-2tau,max f<=b}.

For the unweighted upper estimate it is enough to use the larger event

    T_(tau,b) subset {max f<=b,c<=-24tau}.           (LR21)

If f=mu_b+G satisfies the right side, then, uniformly over b in K,

    max(G/tau)<=C_K/tau,
    D_u^4(G/tau)(0)<=-24+C_K/tau.                   (LR22)

For delta>0 introduce the C4-closed set

    F_delta={h: max h<=delta,D_u^4h(0)<=-24+delta}.

For each delta, (LR22) and the single centered LDP (LR12) give

    limsup_(tau->infinity) tau^-2 log
          sup_(b in K) Q_(0;b,u)(T_(tau,b))
      <=-inf_(F_delta)J.                           (LR23)

Goodness of J implies

    lim_(delta downarrow0) inf_(F_delta)J=I(1,u).   (LR24)

Indeed the infima increase as delta decreases and are at most I(1,u).
If their limit were smaller, near-minimizers would lie in one compact
rate sublevel set and have a convergent subsequence. Its limit would
belong to H_0, be nonpositive, have value and axial second derivative zero
by H_0 membership, and have axial fourth derivative at most -24. It would
therefore be in C_(1,u), contradicting the purported smaller energy.

Apply Holder to the numerator in (LR5), using (LR18)--(LR19). For every
fixed p>1,

    p_E(tau;b,u)<=C_(K,p)
                 Q_(0;b,u)(T_(tau,b))^(1-1/p).     (LR25)

Take the tau upper limit first, then delta down to zero in (LR23)--(LR24),
and finally p to infinity. This proves

    limsup_(tau->infinity) sup_(b in K)
                tau^-2 log p_E(tau;b,u)<=-I(1,u).   (LR26)

Letting p grow before the tau limit is neither used nor justified by a
uniform bound on the constants in (LR19).

## 5. A one-contact C4 stability lemma controls all physical scales

The following deterministic fact is the contact version of the fixed-chart
ridge argument in [CW, sections4--5]. It involves no pair at finite r.

**Contact stability lemma.** Suppose g is C4, satisfies the zero-target
contact rows, has a unique global maximum0 at0, and in the (u,y) frame

    A_g<0,
    c_g-3B_g^T A_g^-1B_g<0.                        (LR27)

Then every sufficiently C4-close function h satisfying the same derivative
contact rows, and with h(0)=beta close to zero, has unique global maximum
beta at0. The assertion is uniform over any family converging to g in C4
with those exact contact rows.

**Proof.** In one fixed chart the transverse Hessian of g is strictly
negative. For all sufficiently close h, the implicit function theorem
gives a unique transverse ridge y_h(x), with y_h(0)=0 and convergence
to y_g in C3. Put R_h(x)=h(x,y_h(x)). Although y_h is only C3, the envelope
identity

    R_h'(x)=D_u h(x,y_h(x))

shows that R_h is C4, and that R_h->R_g in C4. The exact mixed contact
rows give y_h'(0)=0. Differentiating the transverse ridge equation gives
y_h''(0)=-A_h^-1B_h. The reduced derivatives consequently satisfy

    R_h(0)=beta,
    R_h'(0)=R_h''(0)=R_h'''(0)=0,
    R_g''''(0)=c_g-3B_g^T A_g^-1B_g.                (LR28)

By (LR27), shrink this fixed chart and choose eta>0 so that R_h''''<=-eta
throughout its axial interval, for all sufficiently close h. Taylor's
one-node integral formula, valid for either sign of x, gives

    R_h(x)-beta
      =(x^4/6) integral_0^1 (1-t)^3 R_h''''(tx)dt
      <=-eta x^4/24.                               (LR29)

Transverse strict concavity gives h(x,y)<=R_h(x), with equality only on
the ridge. Thus h<beta in the chart except at0. The unique global maximum
of g supplies a strict negative gap on the compact complement of a smaller
chart; C0 closeness and beta->0 preserve a strict gap below beta there.
These two regions cover the torus. All constants may be chosen uniformly
for a C4-convergent family. This proves the lemma.

In particular (LR29) controls every scale x->0, not only points in a
bounded rescaled window. No unproved finite-pin approximation, C5 remainder
bound or genericity of remote critical values is needed.

## 6. Matching lower bound with the full weight and exact CM cost

Fix epsilon in (0,2), and choose a finite B so that the symmetric centered
conditional ball

    B_B={V in ker U_0: ||V||_C4<=B}

has nu probability a_B>0. Such a ball exists for every Gaussian Radon law;
the source Fourier-majorant bound also permits a_B>=1/2 for a suitable B.
For b in K and V in B_B set

    f_(tau,b,V)=mu_b+tau g_epsilon+V,
    H_(tau,b,V)=f_(tau,b,V)/tau.                    (LR30)

All the contact rows (LR3) hold exactly, and

    H_(tau,b,V)->g_epsilon in C4

uniformly over b in K,V in B_B. By (LR14), g_epsilon satisfies the contact
stability lemma. It follows that for all sufficiently large tau,

    max f_(tau,b,V)=b,

uniquely at0, uniformly over this entire family.

The jets also converge uniformly after scaling:

    A(f_(tau,b,V))/tau -> A_epsilon,
    B(f_(tau,b,V))/tau -> 0,
    c(f_(tau,b,V))/tau -> c_epsilon.

Since A_epsilon is strictly negative, inverse matrices are bounded on
these normalized hard blocks. Homogeneity of gamma then gives

    gamma(f_(tau,b,V))/tau -> gamma_epsilon in (-6,-2).

The literal determinant weight consequently has the uniform limit

    w_tau(f_(tau,b,V))/tau^(2d)
      ->(det A_epsilon)^2(36-gamma_epsilon^2)>0.     (LR31)

Here Delta has degree d-1 and the scalar factor contributes tau^2. Thus
there is c_epsilon>0 such that every field (LR30) lies in the numerator
event and has w_tau>=c_epsilon tau^(2d), uniformly in b,V, for all
sufficiently large tau.

The shift tau g_epsilon belongs to the conditional Cameron-Martin space
H_0, with its exact inherited norm. Translation and symmetry of B_B give

    Q_(0;b,u)(mu_b+tau g_epsilon+B_B)
      =nu(tau g_epsilon+B_B)
      >=a_B exp(-tau^2||g_epsilon||_H^2/2).         (LR32)

For completeness, the Cameron-Martin formula writes the probability as
exp(-tau^2||g_epsilon||_H^2/2) times the integral over B_B of an exponential
of a centered Gaussian linear functional. Reflection V->-V replaces that
exponential by its cosh average, which is at least one. No additional
mean-energy term appears: the conditional mean in (LR30) is exactly mu_b.

Equations (LR18), (LR31)--(LR32) now give, uniformly for b in K,

    p_E(tau;b,u)>=c_(K,epsilon) tau^(2d-2)
                       exp(-tau^2||g_epsilon||_H^2/2). (LR33)

The polynomial factor is the full-weight lower estimate divided by the
full normalizer. Taking the lower limit and then epsilon down to zero,
using ||g_epsilon-g_*||_H->0, yields

    liminf_(tau->infinity) inf_(b in K)
                tau^-2 log p_E(tau;b,u)>=-I(1,u).   (LR34)

Together with (LR26), this proves (LR8). Inserting the existing pointwise
critical-window limit (LR6) proves the ordered statement (LR9). The rate
does not depend on birth because the energy constraint (LR7) does not.

## 7. Priority, source identities and precise addition

The quartic contact weight, local elder sector and fixed-ratio limit are
existing results, with their attribution retained through [CW]. The
global essential formula (LR5), the sharp energy (LR7), its even minimizer
and strict profiles (LR13) are also reused from their named sources.

There is already a large-kappa rejection-tail theorem: [SR, section1,
Theorem1] proves that the total rejected cusp kernel has a 1/kappa tail.
That theorem concerns both signs of the rejected local sector, not the
global essential share. Its Step1 already observes that its negative
variable z<=-24kappa forces f4<=-24kappa and has a Gaussian exponentially
small upper bound. Thus exponential suppression of the negative sector
is not a new claim here. The polynomial total rejection tail is produced
by the positive-z sector with a soft transverse curvature. It does not
give an essential-share asymptotic.

The addition here is the matching exact global action for the already
defined contact essential share at large ratio: its coefficient is
I(1,u), the same constrained RKHS minimum as the fixed-positive-k
rare-event coefficient. The one-contact recovery proof supplies the
matching lower action, with exact contact rows, all-scale stability and
the original polynomial determinant weight. Compact-birth uniformity is
proved above for this large-ratio statement only.

Exact reading identities:

- **[SA]** [SHARP_ACTION.md](https://github.com/d6g8k5htny-coder/Math-/blob/fc5ecb67f4a9d6cfb1dec066499ca2daa1147b3b/frontiers/essential_sharp_asymptotics_20261028/SHARP_ACTION.md),
  publication carrier commit `fc5ecb67f4a9d6cfb1dec066499ca2daa1147b3b`
  (Math- #525), path `frontiers/essential_sharp_asymptotics_20261028/SHARP_ACTION.md`,
  git blob `472016cb579e1de87f0993e9d1cfbe3ce315f7c5`, 13524 bytes,
  SHA-256 `26237d1bc5d1f07875e5e20e6f51483adff332d8c5a8b2f81e23ee2c1f4c6673`.
  The local read at `5bc29c3b12a7ed4bf1d9a780cc64c71e136bd718` has these
  exact bytes; the publication record supplied the same-blob carrier
  crosswalk. The carrier object is not present in the local git object
  database, so no local `git show` verification of that carrier is claimed.
- **[CW]** [CRITICAL_WINDOW.md](https://github.com/d6g8k5htny-coder/Math-/blob/5a30296bfc6c9c886d483c87e80e2eb2d9ea047d/frontiers/all_frame_gaussian_rates_20261028/CRITICAL_WINDOW.md),
  publication commit `5a30296bfc6c9c886d483c87e80e2eb2d9ea047d`, path
  `frontiers/all_frame_gaussian_rates_20261028/CRITICAL_WINDOW.md`,
  git blob `520e22f219c2a6e63f229fe20755be2188b4ab50`, 13380 bytes,
  SHA-256 `16d15a49b5c484205c85b00d10b26c173072c946ee5be7f7da2c1d3a4ce97b17`.
- **[SR]** [soft_rejected_pairs PROOF.md](https://github.com/d6g8k5htny-coder/Math-/blob/7d63d08f6cfadfd9c2ef28039a370d741126f9a0/frontiers/soft_rejected_pairs_20261002/PROOF.md),
  commit `7d63d08f6cfadfd9c2ef28039a370d741126f9a0`, path
  `frontiers/soft_rejected_pairs_20261002/PROOF.md`,
  git blob `271412dbc96a29590f5f805258e15c9e335cb430`, 91967 bytes,
  SHA-256 `ee2930c1434bb765d11da0690a2abf3ab330d544ce7ede1ae076a4c29e206c75`.

The exact transitive source roles and source restrictions of [SA] and [CW]
are retained. These citations do not transfer historical scientific
acceptance labels, change formal status or supply independent review.
