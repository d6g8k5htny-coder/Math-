# Localized forcing, full Fourier support, and the qualitative planar SARD-G conclusion

Object: OA-SARD-NONVANISHING-CLOSURE-20260929-v1.
Author: OpenAI / ChatGPT. Status: AUTHOR-SIDE PROOF; nonauthor review required.
Scientific effect NONE. This is not a quantitative or regional C103 certificate.

## 1. Exact scope and conclusion

On the fixed flat torus T_L^2, consider the centered variance-one Gaussian field
with covariance

 K_L(x-y)= [sum_{m in Z^2} exp(-|x-y+Lm|^2/2)]
                           / [sum_{m in Z^2} exp(-|Lm|^2/2)]. (N1)

All constants and neighborhoods in this manuscript are local/existential for
fixed L. Use ascending gradient flow x'=grad f; reversing its sign exchanges
stable and unstable conventions without changing the no-connection event.

**Theorem S (qualitative planar no-connection candidate).** Almost surely the
field has finitely many nondegenerate critical points, with distinct critical
values, and no gradient trajectory connects two different index-one saddles.
Precisely, the connection event has outer Gaussian measure zero and is null in
the completed Gaussian probability space. This does not assert in advance that
the uncompleted connection event itself is Borel.

The proof assembles: the ACTUAL first-closed-contact charts of [RC-S] (not the
old endpoint-admitting predicate); the corrected joint C^1 regularity proved in
A2_FIXED_FRAME.md; the explicit interior perturbation in Sections 2-4 below;
full Fourier support; and the mesh/genericity and countable Gaussian slicing
arguments in Sections 5-7. No A2, A3/A4 or genericity black-box assumption remains
inside this new composition. The source-level R1/R2 geometry is consumed at its
pinned proof, with its separate review status retained. This is an author-side
composition pending review, not a canonical advancement of the old SG source.

The theorem is unconditioned. It does not apply a full-support proof to a
coalescing pair-conditioned field, and gives no bound uniform under conditioning.
There is no 3D Morse-Smale conclusion, no regional intensity, no RN/JETMOD claim,
no numerical probability of a near-connection, and no new quantitative C103 gate.

## 2. An interior perturbation cannot be canceled by endpoint variation

Fix a zero of a robust chart: a genuine saddle connection from p to q, with its
unstable and stable launches in disjoint endpoint neighborhoods. Along its compact
regular arc write gamma(t), 0<=t<=T, with central first section hit at t=c in (0,T).
By uniqueness and strict increase of f, the arc is embedded. Pick t_0 in (0,c),
strictly after the unstable launch. A small coordinate neighborhood O of gamma(t_0)
can be chosen disjoint from both endpoint neighborhoods and from the entire
stable travel half gamma([c,T]); it meets the remaining trajectory only inside
a small time interval J compactly contained in (0,c).

Why O exists matters. An embedded compact arc is a homeomorphism onto its image.
Remove a small open parameter interval around t_0; its remaining compact image
is disjoint from a smaller compact subarc. Their distance is positive. Choose
O inside that separation, small enough for a local coordinate graph. This rules
out hidden returns through the support of the perturbation.

Let h in C^2 be supported in O. The original vector field and every endpoint local
germ are unchanged near their entire defining endpoint neighborhoods. The fixed
cutoff construction in A2_FIXED_FRAME.md, followed by local finite flow, makes
both launch points EXACTLY unchanged for f+epsilon h. The stable travel half and
its central hit are also unchanged, since the field is unchanged on a neighborhood
of that half. The unstable variation w therefore satisfies

 w'=H_f(gamma(t))w+grad h(gamma(t)),  w(0)=0, 0<=t<=c.          (N2)

Let Sigma have unit normal n and unit tangent tau, and V_c=grad f(gamma(c)).
Transversality means n.V_c!=0. Correction for the moving hit time projects the
fixed-time variation by

 Pi=I-V_c n^T/(n.V_c).                                       (N3)

The mismatch coordinate is the signed tangent coordinate, so its derivative is

 L_f(h)=tau^T Pi w(c).                                       (N4)

In particular endpoint-supported derivative terms have not been ignored; they
vanish for THIS specially supported perturbation by exact localization.
For general h the joint C^1 regularity gives a bounded linear derivative L_f on
X with |L_f(h)|<=C||h||C1. Only the supported perturbation is needed to prove it
is nonzero. No formula claiming endpoint variation is a finite list of two-jets
is asserted.

## 3. The covector calculation and a concrete potential perturbation

Let Phi(t,s) be the fundamental matrix of w'=H_f(gamma(t))w. Define

 b_c=Pi^T tau,     b(t)=Phi(c,t)^T b_c.                       (N5)

Pi fixes the tangent tau, so b_c.tau=1 and b_c!=0. Also b_c.V_c=0 because Pi V_c=0.
Invertibility of Phi gives b(t)!=0. The adjoint identity is

 b'=-H_f(gamma(t))^T b,     b(t).grad f(gamma(t))=0.           (N6)

The last equality follows by differentiating the pairing; the vector grad f
along the orbit solves V'=H_f V. Duhamel now gives

 L_f(h)=integral_0^c b(t).grad h(gamma(t)) dt.                 (N7)

It remains to choose h as a SCALAR POTENTIAL, not an arbitrary vector forcing.
In a fixed local Euclidean coordinate rotation, the regular C^2 trajectory is
a C^2 graph y=g(x) on O, with x(t) strictly monotone. Since b is perpendicular
to its tangent, on a smaller interval it has the form

 b(t)=a(t)(-g'(x(t)),1),

where a is continuous, nonzero, and of constant sign. Choose a nonnegative C^2
function phi supported strictly inside that x interval, not identically zero,
and a smooth transverse cutoff zeta equal to one near zero. Set

 h(x,y)=sign(a) phi(x)(y-g(x)) zeta(y-g(x)).                   (N8)

The rectangle and cutoffs are small enough that h is supported in O; extend it
by zero globally. It is C^2. Along the orbit its gradient is
sign(a) phi(x)(-g'(x),1), so

 b(t).grad h(gamma(t))=|a(t)| phi(x(t))(1+g'(x(t))^2)>=0,

with a strictly positive integral. Thus L_f(h)>0. This explicitly proves
nonvanishing at every robust connection using only C^2 regularity. If a smooth
h is desired, approximate this compactly supported C^2 function in C^2 inside
O by smooth functions; continuity of L_f preserves strict positivity.

The construction is field-dependent only as an EXISTENCE witness for L_f!=0.
It is not selected measurably and is not itself used as a random Gaussian shift
direction. Countably many deterministic Fourier directions are chosen next.

## 4. From a local bump to a deterministic Cameron-Martin direction

Poisson summation gives Fourier weights

 a_n=[2pi/(L^2 Z_L)] exp(-2pi^2 |n|^2/L^2)>0,
 Z_L=sum_m exp(-|Lm|^2/2),   sum_n a_n=1.                    (N9)

Every real trigonometric polynomial therefore belongs to the Cameron-Martin
space H: its RKHS norm is a FINITE sum of squared Fourier coefficients divided
by positive a_n (with the corresponding real-mode convention). Such polynomials
are dense in C^2. One direct proof uses periodic smoothing followed by Fourier
truncation of the smoothed function, or product Fejer means applied also to each
of the continuous derivatives of orders <=2.

Since L_f is continuous on C^2 and is nonzero on (N8), it cannot vanish on all
trigonometric polynomials. By linearity it is nonzero on at least one individual
real Fourier mode. These modes all lie in H. This proves the A3/A4 nonvanishing
interface WITHOUT differentiating an RKHS kernel or representing every endpoint
variation by distributions. Positivity of EVERY Fourier weight is essential;
a band-limited or otherwise restricted spectrum is not covered by this argument.

It also verifies compatibility with [RC-S] R3: a nonzero continuous L_f|H is
nonzero on its countable evaluation-image family. Thus one may use its already
written Gaussian decomposition. Section 7 instead gives a simpler equivalent
Fourier-coordinate decomposition for this particular periodic model.

## 5. Smooth sample paths and finite-jet covariance floors

Choose one representative n in each pair {n,-n}, n!=0. An exact real realization is

 f(x)=sqrt(a_0)Z_0+sum_{n+}sqrt(2a_n)
          [Z_n^c cos(2pi n.x/L)+Z_n^s sin(2pi n.x/L)],          (N10)

with independent standard real Gaussians. For every integer k,

 sum_n sqrt(a_n)(1+|n|)^k E|Z_n| < infinity.

Tonelli gives almost-sure absolute uniform convergence of all derivative series
through order k; a countable intersection in k gives smooth paths. Their C^k
norms also have finite fixed moments by the corresponding sum/Minkowski bound.
This realization has covariance (N1); its C^2-valued law is the Gaussian law used
in [RC-S]. No finite Fourier truncation is substituted for the exact field.

Any finite set of distinct derivative functionals at one point is linearly
independent as distributions when symmetric duplicates are removed. The same
holds for gradients at two distinct points together with their value difference:
use test functions supported separately near the two points to isolate each
coefficient. If a linear combination had zero variance, positivity of all a_n
would force it to vanish on every Fourier mode. It would then vanish as a
finite-order distribution, by Fourier approximation of smooth tests, contrary
to independence. Hence its covariance is positive definite.

In particular (grad f,H_f) at one point is a nondegenerate five-dimensional
Gaussian vector. Also

 (grad f(x),grad f(y),f(x)-f(y))                               (N11)

is nondegenerate for x!=y. Covariance varies continuously with the points, so
on dist(x,y)>=epsilon its smallest eigenvalue has a positive minimum. Gaussian
densities are therefore uniformly bounded on that compact separated set. These
floors are qualitative for each fixed separation; no uniform lower floor as
x->y is claimed or needed here.

## 6. Two elementary mesh arguments establish the full-measure generic set

This supplies the genericity input explicitly, not through an unverified claim
that every field along a Gaussian shift line is generic.

### 6.1 Morse critical points

Localize to ||f||C3<=M. If grad f(x)=0 and det H_f(x)=0, at a mesh point x_delta
within C delta one has |grad f(x_delta)|<=C_M delta,
||H_f(x_delta)||<=C_M, and |det H_f(x_delta)|<=C_M delta. There are O(delta^-2)
mesh points. For a symmetric matrix [[a,b],[b,c]] in a bounded box, the volume of

 |ac-b^2|<=epsilon                                           (N12)

is O_M(sqrt(epsilon)). Indeed split |a|<=sqrt(epsilon), which has volume
O_M(sqrt(epsilon)), from |a|>sqrt(epsilon), where at each fixed a,b the permitted
c interval has length at most 2epsilon/|a|<=2sqrt(epsilon). This rough bound is
sufficient even near the double-zero matrix.

The joint five-variable density bound from Section 5 gives probability
O_M(delta^2 sqrt(delta)) per mesh point. The union bound gives O_M(sqrt(delta)),
which tends to zero along any sequence of refining meshes. The bad event is
contained in every such mesh union, so it has probability zero on ||f||C3<=M.
Take a countable union over M. Nondegenerate zeros of grad f are isolated;
compactness then makes their number finite.

### 6.2 Distinct critical values

Fix separation epsilon>0 and localize to ||f||C2<=M. If two separated critical
points have equal values, (N11) at a nearby mesh pair has norm <=C_M delta.
For small delta the pair remains separated by epsilon/2. There are O(delta^-4)
mesh pairs. The five-dimensional Gaussian density bound gives probability
O_{M,epsilon}(delta^5) for each, and hence O_{M,epsilon}(delta) for the union.
Let delta->0, then take the countable union over M and separations epsilon=1/n.
Every distinct pair has some positive separation, so almost surely all critical
values are distinct.

The relevant events can be formulated by minima of continuous functions on compact
sets at fixed norm/separation bounds; alternatively the mesh unions supply Borel
null supersets directly. This is enough for the completed-measure conclusion.
There is no reliance on a sampled gradient minimum as a certified continuum bound.

## 7. Countable Fourier slicing closes the qualitative connection event

Use the robust charts of [RC-S] with fixed-frame branch parameterizations from
A2_FIXED_FRAME.md. The chart domains are open in C^2, form a countable family,
and cover every nondegenerate connection. Their mismatches D_chi are jointly
constructed and Frechet C^1. At every connection zero their derivative is
nonzero on some deterministic real Fourier mode by Sections 2-4.

For a mode let h_j be its function in the expansion (N10), INCLUDING its standard-
Gaussian scale sqrt(a_0) or sqrt(2a_n). Its Fourier coefficient xi_j is standard
normal, and the residual g_j=f-xi_j h_j is independent of xi_j. One can check
this from the independent series, or by vanishing cross-covariances and the
Gaussian characteristic functional. Subtracting one smooth mode leaves a
C^2-valued residual. All modes are countably indexed. The constant mode has
zero mismatch derivative, but at least one nonconstant mode is nonzero.

For fixed chi,j let

 B_chi,j={f in U_chi: D_chi(f)=0, D D_chi(f)[h_j]!=0}.         (N13)

This is Borel because U_chi is open and both scalar maps are continuous. For
EVERY fixed residual g, the validity set I_g={t:g+t h_j in U_chi} is open. The
function t->D_chi(g+t h_j) is C^1 there. Each zero counted in (N13) has nonzero
derivative, hence is isolated among all zeros on its validity interval. The
regular zeros are countable: each has a rational-endpoint interval containing
no other zero. Accumulation at singular zeros or interval boundaries is allowed.

Independence and Tonelli therefore give mu(B_chi,j)=0, since the scalar Gaussian
charges no countable set. The union over chi,j is a Borel null set containing all
nondegenerate connections. Section 6 supplies a full-measure set of Morse fields
with distinct critical values. The connection event is thus outer-null and null
in the completion. A self-connection is excluded separately by strict increase
of f along every nonconstant gradient trajectory. This proves Theorem S as a
qualitative source-level composition.

An equivalent ending applies [RC-S] R3/R4 after supplying A2-D and A3/A4 from this
packet and genericity from Section 6. We wrote the mode argument to show that the
concrete periodic theorem does not need any norm-separable Banach dual, abstract
measurable chart selector, or assertion about all shifted fields being Morse.

## 8. What this resolves mathematically, and what it does not authorize

The packet supplies explicit source arguments for local parameter regularity,
nonzero Cameron-Martin variation, the full-measure generic set, and their actual
composition with the robust first-contact predicate. It avoids proving the false
strong C1-into-C1 statement and does not attempt to repair it by enlarging the
field norm to C3, changing the Gaussian law, or allowing an endpoint hit.

The original SG/BR/RI and conditional [RC-S] reviews remain historical evidence.
A nonauthor review of A2, of the localized-forcing/Fourier argument, and of this
assembly is still needed before any canonical downstream status fold. In particular
Theorem S is not a new regional Kac-Rice estimate, does not prove a deterministic
normalizer floor on a numerical interval, and does not settle conditioned SARD-G,
RN/JETMOD, P0.1 or any 3D claim. Such consumers must expose the exact measure and
object they use rather than treating an unconditioned null set as universally null.

The methods are classical contraction, variation of constants, Fourier support,
mesh bounds and Gaussian slicing. No historical-priority or exhaustive novelty
claim is made. Finite tests check selected exact identities and logical exclusions;
they are not proofs of the infinite-dimensional or measure-theoretic statements.
