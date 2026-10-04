# Small-lifetime doublets: an exact shape limit and a singular companion-moment crossover

Object: OA-SMALL-LIFETIME-SHAPE-20260930-v1.
Author: OpenAI / GPT-6 Astra Pro, foreground continuation after the owner's
new September 30 instruction and interrupted-session screenshot.
Disposition: AUTHOR-SIDE CONDITIONAL CANDIDATE; NONAUTHOR REVIEW OPEN.
Scientific effect NONE. No source proof, register, Boolean, prize or existing
review changes. This conversation authored the source cluster calculations;
its reconstruction here is not an independent review of those premises.

## 1. Precisely which law is being conditioned

This paper studies an EXPLICIT, finite-dimensional probability measure. Its
interpretation as an actual Gaussian elder-partner law is conditional on [E].
The original field separation r tends to zero first, and the selected partner's
microscopic radius threshold tends to infinity second, as in [E]. We then
condition the resulting lifetime fraction e to be at most epsilon and take
epsilon to zero. A further large companion-ratio limit is taken only afterward.
This is NOT the fixed-r small-lifetime problem of PR182, and that theorem is
neither consumed nor re-proved here.

Immutable sources (full identities in SOURCES.json):
[E] PR181 PROOF.md at ae343a1c2a0070476fed4d31a15b6911831edd4d,
blob 91f88e392fb8aa947dac4fc81c2b45f783fa66cd: its explicit selected shape law,
(4)-(7), (15)-(17), and its doublet square density and heights (20)-(23).
[C] PR169 PROOF.md at 56a7904f9ad7d409c31e23195c0e7eeab230613a,
blob 19a6044f2066643b5baab34ce5b6b6efb431e84a: deterministic companion-root
involution and strict doublet classifier E12-E17. No new Gaussian or
actual-pairing conclusion is inferred from polynomial roots alone.

Put E0=888807/280. In the coordinates of [E], x=-u-1/2 and
v=6(e+x), the selected shape probability Pi has density

 dPi(e,x)=E0^-1 K(e,x) de dx,
 K(e,x)=10368(e-x^2)(e+x^2+2x)(e+2ex+x^2),                (1)

on 0<e<1 and a(e)<x<b(e), where

 a(e)=sqrt(1-e)-1,
 b(e)>0 solves 3b^2+2b^3=e.                              (2)

The root b(e) is unique in (0,1/2). K is strictly positive on the interior.
The mass is one: integrate e first on the two polynomial strips
-1<x<0, -2x-x^2<e<1 and 0<x<1/2, 3x^2+2x^3<e<1;
the exact integral of K is E0. The same elementary integrations reproduce
[E]'s first two unnormalized moments. Thus (1) can also be taken as a
self-contained definition independent of its conditional field interpretation.

Let n in {1,2} be the number of window roots in that limiting local configuration.
For doublets, V is the other/selected radius ratio in the ALREADY-FORMED extreme
geometry. The selected root is the higher saddle, not a finite-scale
physical-radius minimum. The two roots are asymptotically antipodal and V>1.
On singletons define V=1 and the other marks by a sentinel; their mass will
vanish in the new limit. None of the claims concern the global torus count.

Write Pi_epsilon=Pi(. | e<=epsilon), and let Pi_epsilon,2 additionally condition
on n=2. The parameter epsilon is a lifetime cutoff, not r or the radius cutoff.
Total variation is half the full L1 distance of probability densities.

## 2. Exact singleton boundary, before taking a limit

**Lemma 1.** Let c(e)>0 be the unique root of

                  2c^3+3e c^2=e^2.                     (3)

On the support of (1), n=1 exactly for x<=c(e), and n=2 exactly for x>c(e),
up to tie null sets. In particular 0<c(e)<b(e) for 0<e<1. It would be false
to assert that every sufficiently short, but nonzero, e already forces a doublet.

Proof. For x<=0, u>=-1/2 lies on the singleton side of the cubic classifier.
For x>0 set p=x+1/2, A=12p^2-3=12x(1+x) and v=6(e+x).
The source doublet inequalities are v<A and

 (v-A)^2(2v+A)-12(v-Ap)^2>0.

Direct expansion gives

 (v-A)^2(2v+A)-12(v-Ap)^2
             =432(1-e)(2x^3+3e x^2-e^2).                (4)

The second inequality therefore reduces to the positive sign in (3).
It implies the first: if e>=x+2x^2 (equivalently v>=A), the expression
2x^3+3e x^2-e^2 is decreasing in e on that range, and at e=x+2x^2 it equals
x^2(2x-1)(x+1)<0 for 0<x<1/2. The expression in x is strictly increasing
for x>0, negative at zero, and at x=b(e) is 2b(e)^3(1-e)>0.
This proves the unique boundary and the classification. At equality the
companion lies at the excluded window height; treating it as one root rather
than two has no effect on the absolutely continuous measure. QED.

Two DIFFERENT scales appear as e decreases:

 b(e)=sqrt(e)[1/sqrt(3)+O(sqrt(e))],
 c(e)=e^(2/3)[2^(-1/3)+O(e^(1/3))],
 a(e)=-e/2+O(e^2).                                     (5)

For b, divide its equation by e. For c, set c=e^(2/3)z and obtain
2z^3+3e^(1/3)z^2=1. The implicit-function theorem at the respective positive
roots gives both estimates, with bounded derivatives on a small fixed interval.

## 3. Normalized shape limit and a sharp singleton probability

Define, under Pi_epsilon,

             Y=e/epsilon,        W=x/sqrt(e).           (6)

**Theorem 1 (shape and multiplicity).** The law of (Y,W) converges in total
variation at O(sqrt(epsilon)) to independent variables with densities

 f_Y(y)=4y^3, 0<y<1,
 f_W(w)=(81/13)w(1-w^4), 0<w<1/sqrt(3).                 (7)

The singleton probability has the more singular expansion

 Pi_epsilon(n=1)=C_s epsilon^(1/3)+O(epsilon^(2/3)),
                   C_s=(486/169)2^(-2/3)>0.             (8)

Consequently doublets tend to probability one. For the TAGGED joint law,

 dTV(Law_Pi_epsilon(n,Y,W), delta_2 x Law(Y,W in (7)))
             =C_s epsilon^(1/3)+O(epsilon^(1/2)).        (9)

No rate is asserted for physical marks obtained through epsilon-dependent
singular maps; their convergence below is weak.

Proof of (7). Put delta=sqrt(e). From (1), after x=delta w,

 K(e,x)dx=10368 e^3 Phi_delta(w) dw,
 Phi_delta(w)=(1-w^2)[2w+delta(1+w^2)]
                                      [1+w^2+2delta w]. (10)

Its interval is l(delta)<w<h(delta), with
l(delta)=-delta/(1+sqrt(1-delta^2)) and
3h(delta)^2+2delta h(delta)^3=1. On any small fixed interval in delta>=0,
l,h are smooth and all interval endpoints and coefficients are bounded.
Therefore the L1 difference between the interval-extended Phi_delta and
Phi_0(w)=2w(1-w^4)1_(0,1/sqrt(3)) is O(delta). This includes the moving
boundary contribution; Phi_0 does not vanish at its upper endpoint.

Its integral is A0=26/81. Hence, writing unnormalized shape masses,

 A_epsilon=integral_(e<=epsilon) K de dx
              =832 epsilon^4[1+O(sqrt(epsilon))].        (11)

The normalized density of (Y,W) is proportional to
y^3 Phi_(sqrt(epsilon y))(w), with the same interval restrictions. The L1
estimate, integrated over y, is O(sqrt(epsilon)), and the normalizing constant
tends to A0/4. This gives exactly (7). Both densities integrate to one.

Proof of (8). The unnormalized singleton density at e is
S(e)=integral_(a(e))^(c(e)) K(e,x)dx. Put tau=e^(1/3), x=e^(2/3)z. Then

 S(e)=10368 e^(10/3) integral
     (1-tau z^2)(2z+tau+tau^2 z^2)(1+tau z^2+2tau^2z) dz. (12)

The lower endpoint is -tau/(1+sqrt(1-tau^3)); the upper endpoint solves
2z^3+3tau z^2=1. They converge to 0 and 2^(-1/3), smoothly in tau. Thus

 S(e)=10368*2^(-2/3)e^(10/3)[1+O(e^(1/3))].              (13)

Integrate from zero to epsilon and divide by (11). The coefficient is
10368*(3/13)/832 times 2^(-2/3), namely C_s. The relative error is
O(epsilon^(1/3)); the smaller normalization error O(sqrt(epsilon)) does not
change it. This proves (8).

Finally replace n by 2 without changing (Y,W). The TV distance between the
original tagged law and this replacement is exactly Pi_epsilon(n=1).
The replacement is O(sqrt(epsilon)) from the limit in (7). The triangle and
reverse-triangle inequalities give (9). QED.

The nonzero singleton error is not an artifact of numerics: its e^(2/3)
spatial-jet boundary (3) is thinner than, but sits inside, the main sqrt(e)
shape scale. Conditioning only on an exact e gives the analogous singleton
probability (81/26)2^(-2/3)e^(1/3)[1+O(e^(1/3))].

## 4. Limiting companion geometry and a tail of exponent ONE

**Theorem 2.** Under Pi_epsilon, the companion ratio, defined on doublets,
converges in distribution to

                 V0=(1-W^2)/(2W^2)>1.                  (14)

It is independent of Y in (7). Its exact density and survival function are

 g(v)=(81/13)[(2v+1)^(-2)-(2v+1)^(-4)], v>1,
 P(V0>t)=81/[26(2t+1)]-27/[26(2t+1)^3], t>=1.            (15)

In particular P(V0>t)~(81/52)t^-1. Its nonnegative moments are finite exactly
below 1; E[min(V0,T)]~(81/52)log T. The reciprocal rho0 has density

                 (324/13)(1+rho)/(2+rho)^4, 0<rho<1.    (16)

The other saddle's downward height e_c satisfies, jointly,

 (e/epsilon, e_c/e, e_c/epsilon)
                  -> (Y, H(V0), Y H(V0)),
 H(v)=v^3(v+2)/(2v+1).                                 (17)

This convergence is weak, including sentinel removal using (8).

Proof. Write delta=sqrt(e), u=-1/2-delta w, v_shape=6(delta^2+delta w).
Substituting in the exact companion involution yields the following rational
identities, wherever a counted companion exists:

 D_delta(w)=4w^3+delta(3w^4+6w^2-1)+4delta^2w^3,
 V_delta(w)=(1-w^2)[2w+delta(1+w^2)]/D_delta(w),
 e_c/e=(1-w^2)^3[1+3w^2+delta(6w+2w^3)+delta^2(1+3w^2)]
                                                   /D_delta(w)^2. (18)

On each compact subset of 0<w<1/sqrt(3), the denominator stays positive for
small delta and the configuration is a doublet by (3)-(5). The maps converge
uniformly there to (14) and to
(1-w^2)^3(1+3w^2)/(16w^6)=H(V0). Tightness and the vanishing mass of the omitted
boundary strips under (7), together with (8), allow these compacts to exhaust.
This is a continuous-mapping argument on compact restrictions, not an assumed
uniform estimate near w=0. Formula (15) follows by changing variables
w^2=1/(2v+1) in (7); integration gives the survival formula. All remaining
tail and moment assertions in (15)-(16) follow directly. QED.

Geometric interpretation, conditional on [E]: the selected extreme radius q
is Pareto(11), independent of the shape and cusp parameters before and after
conditioning on e<=epsilon. In the third limit the local two-saddle positions
are {sigma q e_*, -sigma q V0 e_*}; both full indices are d-1. Their normalized
downward heights divided by epsilon are Y and Y H(V0). The direction e_* and
its model dependence are those of [E]; no spatial TV or original-field
independence claim is introduced.

Since H(v)~v^3/2, the lifetime RATIO has tail exponent1/3:

 P(H(V0)>t)~[81/(52*2^(1/3))]t^-1/3.                    (19)

Independence and E[Y^(1/3)]=12/13 give
P(YH(V0)>t)~[243/(169*2^(1/3))]t^-1/3. A bounded-tail envelope from (15)
justifies dominated convergence in Y. The nonnegative moment thresholds for
these two limits are1/3. These are height ratios/scaled marks, not the
unscaled bounded height e_c at a positive epsilon.

## 5. Why exponent13 at fixed epsilon is consistent with exponent1 in the limit

Use [E]'s doublet square coordinates (rho,z) in (0,1)^2. Its unnormalized
selected density and lifetime are

 J(rho,z)=165888 rho^12 z^7(1+z)^4 R(rho,z),
 R=(1+rho z)^4(1+rho z+rho)^7/
                       [(1+rho)^5(1+2rho z+rho)^9],
 e(rho,z)=rho^3 z^2(1+z)(rho z+rho+2)/
                       [(rho+1)(2rho z+rho+1)].         (20)

The normalization on e<=epsilon,n=2 is
B_epsilon=integral J 1{e<=epsilon} d rho dz.
By (8)-(11),

 B_epsilon=832 epsilon^4[1+O(epsilon^(1/3))].             (21)

This is a SHAPE normalization, not the original Gaussian endpoint normalizer.
There is no extra D or E0 in the conditional density J/B_epsilon.
The coefficient R and the positive function e/(rho^3 z^2) extend continuously
to the closed square, with finite positive upper/lower bounds. Thus

 c rho^3z^2<=e(rho,z)<=C rho^3z^2,
 c rho^12 z^7<=J(rho,z)<=C rho^12 z^7.                   (22)

**Theorem 3 (a uniform tail envelope in the algebraic law).** For sufficiently
small epsilon and all T>=1,

 Pi_epsilon,2(V>T)
       <= C min(T^-1, epsilon^-4 T^-13).                 (23)

For each FIXED epsilon>0,

 Pi_epsilon,2(V>T)
       ~ [165888 H0/(13 B_epsilon)] T^-13,
                         H0=6401/3960.                 (24)

Hence its nonnegative moments are finite exactly for p<13 at every positive
epsilon. The exponent1 emerges only after epsilon->0. There is no
contradiction or unmentioned transfer of uniform integrability.

Proof. The event e<=epsilon implies z<=min(1,C sqrt(epsilon)rho^-3/2).
Integration of the bound rho^12 z^7 gives

 integral_(rho<1/T,e<=epsilon) J
          <= C integral_0^(1/T) min(rho^12,epsilon^4)d rho.

Divide by (21), and either bound the integrand by epsilon^4 or by rho^12.
This proves (23). At fixed epsilon, for all sufficiently small rho the entire
z interval satisfies e<=epsilon, by the uniform upper bound in (22). Moreover
R(rho,z)->1 uniformly. Direct integration then gives (24). A positive lower
bound on any interior z subinterval shows divergence at p>=13, while the
upper bound J<=C rho^12 z^7 gives finiteness below13. QED.

The crossover scale in this envelope is T of order epsilon^-1/3. The two terms
in (23) are bounds, not an asserted exact uniform crossover profile.

## 6. Complete companion-moment crossover within the explicit law

**Theorem 4.** Under Pi_epsilon,2, as epsilon->0:

 0<=p<1: E[V^p] -> E[V0^p]<infinity;
 p=1:    E[V] = (27/52) log(1/epsilon)+O(1);
 1<p<13: E[V^p] ~ K_p epsilon^(-(p-1)/3),
 p>=13:  E[V^p]=infinity for every fixed epsilon>0,       (25)

where the positive finite coefficient is explicitly

 K_p=2592/[13(13-p)] * 2^(-(13-p)/3)
        * integral_0^1 z^((2p-5)/3)(1+z)^((p-1)/3) dz.   (26)

For example K_4=30/13, K_7=441/65, and K_10=3270/91.
The normalization may instead be Pi_epsilon with the moment restricted to n=2;
its leading asymptotics agree because Pi_epsilon(n=2)->1. No statement is made
about these moments in the original finite-r field.

Proof for p<1. The first bound in (23), uniformly in epsilon, supplies uniform
integrability of V^p (use any intervening power less than1). The weak limit in
Theorem2 gives convergence. The case p=0 is normalization.

Proof for 1<p<13. In the numerator integral for V^p set rho=epsilon^(1/3)q.
Then the scaling factor is epsilon^((13-p)/3). For fixed q,z,
R->1 and the cutoff tends to
q^3 A(z)<=1, A(z)=2z^2(1+z).
The resulting integrand is 165888 q^(12-p) z^7(1+z)^4 on that domain.
An integrable domination follows directly from (22): for q near0, p<13;
for q large, the cutoff forces z<=Cq^-3/2, and integration in z bounds the
tail by Cq^-p, integrable exactly when p>1. Dominated convergence is legitimate
on the two-dimensional domain, including its corner, not just at fixed z.
Integrating q first yields

 165888/(13-p) integral_0^1 z^7(1+z)^4 A(z)^(-(13-p)/3) dz.

Dividing by B_epsilon~832epsilon^4 gives (26). The displayed rational cases
follow by binomial expansion, without numerical integration.

Proof for p=1. At fixed rho, the lifetime is strictly increasing in z: its
logarithmic derivative is
2/z+1/(1+z)+rho/(rho z+rho+2)-2rho/(2rho z+rho+1)>0,
since the last term is less than1/z in magnitude. Near z=0, uniformly in
0<=rho<=1,

 e= kappa(rho) z^2[1+O(z)],
 kappa(rho)=rho^3(rho+2)/(rho+1)^2,
 J=165888 rho^12 z^7/(1+rho)^7 [1+O(z)].                 (27)

Choose a sufficiently large fixed M. For rho>=M epsilon^(1/3), the unique
cutoff root has z_epsilon=(epsilon/kappa)^(1/2)[1+O((epsilon/kappa)^(1/2))],
with uniform constants. Integrating J to that root gives

 integral J 1{e<=epsilon} dz
   =20736 epsilon^4 (1+rho)/(2+rho)^4
                    [1+O(epsilon^(1/2)rho^-3/2)].       (28)

After division by B_epsilon and multiplication by rho^-1, the leading integral
from M epsilon^(1/3) to1 is

 integral [(324/13)(1+rho)/(2+rho)^4] d rho/rho.

Its logarithmic coefficient is (81/52)/3=27/52. The integrated relative
cutoff error is bounded, since epsilon^(1/2) integral_(M epsilon^(1/3))^1
rho^-5/2 d rho=O(1). The normalizer error O(epsilon^(1/3)) times the logarithm
is bounded and tends to zero. On rho<M epsilon^(1/3), ignoring the cutoff and
using J<=C rho^12 z^7 gives a bounded contribution to E[V] (at this fixed M).
This proves the O(1) remainder, not just a logarithmic order statement.
The p>=13 assertion was proved in Theorem3. QED.

The moment crossover is a quantitative explanation for why the limiting ratio
can have infinite mean although every positive-epsilon conditional mean is
finite. It does not assert convergence of unbounded observables from weak
convergence alone; each such claim was proved with the explicit corner density.

## 7. Review and verification boundaries

A: Lemma1 and Theorem1 — exact count classification, normalization, two distinct
jet scales, singleton coefficient and tagged/untagged TV distinction.
B: Theorem2 — companion/height substitutions, explicit limiting tail and marks,
sentinels, independence and order of limits.
C: Theorems3-4 — uniform algebraic tail envelope, fixed-epsilon exponent13,
corner domination, exact K_p and the logarithmic coefficient27/52.

All new conclusions are unconditional statements about the explicitly defined
shape measure (1), together with the stated deterministic root-label interface.
Their Gaussian actual-elder interpretation remains CONDITIONAL on the precise
source laws. No numerical model coefficient, new elder-pairing proof, finite-r
inverse moment, fixed-r count certainty, original-field doublet tail exponent1,
uniform r/epsilon/radius limit or Lean formalization is claimed.

The companion scripts test finite exact identities, moments, root brackets and
negative variants. They do not certify dominated convergence, total variation
limits, the field-source hypotheses or independent review authenticity. The
fixed-r inverse-moment threshold2/3 in PR182 and the lifetime-fraction threshold4
in PR181 are different statements; neither is changed by this result.
