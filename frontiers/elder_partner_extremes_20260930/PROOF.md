# Distant actual elder partners: selection, lifetime fractions and the thirteenth-power companion tail

**Object:** OA-ELDER-EXTREMES-20260930-v1.
**Author:** OpenAI / GPT-6 Astra Pro, foreground owner-authorized continuation.
**Disposition:** AUTHOR-SIDE CONDITIONAL CANDIDATE; NONAUTHOR REVIEW OPEN.
**Scientific effect:** NONE. No parent proof, register, Boolean, prize or earlier
verdict changes. This conversation authored the cluster sources; no independent
revalidation or organizational independence is claimed.

## 1. The actual estimand and the two source interfaces

Fix d>=2, L>0, b real, k>0 and an axial/transverse orthonormal frame. Use the
exact variance-one periodized field, original endpoint observations and the
one full determinant-tilted pair-Palm law Q_r^W of the sources. Write F_r for
failure of the prescribed saddle to be the ordinary elder partner of the
prescribed maximum. Let T_r be the ACTUAL replacement-partner displacement
from the midpoint divided by r and let

    lambda_r=(b-d_f(M))/(k r^3).                              (1)

Out-of-chart or essential partners may be given an isolated sentinel. The
source interface says their probability on F_r is o(r^3). We do not identify
an arbitrary witness or farthest root with an elder partner.

The two exact input types are deliberately separate:

- **ELDER2:** PR170 at79f18f0cb318fceccd5bdf4e6dad29815165bc7d,
  PROOF.md, Theorem E and Sections8.6-8.8. In d=2 it supplies the actual highest
  local saddle, the full failure measure and its weak location/lifetime marks.
- **ELDERD:** PR175 at9c6a73489c5ed2465a3cf65dcc950eeeae074b05,
  PROOF.md, H1/S1-S3/M1. In d>=3 it supplies the hard-negative-fibre bridge,
  the extended spectral failure measure, and the actual weak marked law.
- **R:** PR166 RADIAL_TAIL.md at80059a97cd8eb32d1a17a0ad9cb22cb2a0d7b337,
  R4-R13, supplies the exact root-resolved density of the limiting microscopic
  measure and its Gaussian majorant. This is used to integrate the already
  identified selector, NOT to establish actual elder pairing from counts.
- **C:** PR169 PROOF.md at56a7904f9ad7d409c31e23195c0e7eeab230613a,
  E10-E25, supplies the deterministic companion/height map, inner/outer sectors
  and exact shape integrals. Its whole-cluster maximum theorem is not used as
  an elder theorem.
- **D:** COMPANION_RATIO.md at that same PR169 head, D1-D7, supplies the exact
  unit-square density/height formulas. Only Section6 below needs this input.

All complete commit/path/blob/SHA256 bindings are in SOURCES.json. ELDER2 and
ELDERD are distinct author-side source candidates with source-bound reviews;
this consumer is conditional on their displayed mathematical interfaces. It
neither promotes their status nor discharges a missing premise by citation.
The prior source proofs and review bodies remain unchanged.

The common limiting microscopic measure is denoted M. Its restriction to
n>0, where n is the number of extra strict-window cubic saddles, is the finite
failure measure mu_F with mass a_F=a1+a2>0. It is NOT the global nonempty count
measure: remote singleton mass is absent. With theta=(s,h,O,tau),

 dM=(c_m/z0) H(h) h0(A0,Rot_O tau)
                  9k^2(4s^2-B^2) ds dh dO dtau,            (2)

on the positive hard/typed domain. Here H is the ordered hard spectral
polynomial, A0=O diag(0,-h)O^T, B=beta-a^2/(12k), and s<-|B|/2.
The scalar case has empty hard products; a normalized soft sign-frame
augmentation changes no physical integral. There is one full z0 and no
additional pin density or root multiplicity.

The actual interface is finite-measure weak convergence, with converging masses,

 r^-3 Q_r^W((T_r,lambda_r) in dot,F_r)
             -> pushforward of mu_F by (T_*,eta_*),         (3)

where T_* is the root with GREATEST cubic height P, and eta_*=-P(T_*)/k.
Thus eta_* is the SMALLEST downward height among the window roots.
The assertion that this is the actual elder partner is precisely the elder
source premise, not a conclusion of the polynomial computations below.

**Order:** first r->0. Then the radius threshold t->infinity inside (3)'s limit.
Any further small-lifetime or large-companion limit is taken third. No uniform
simultaneous limit, finite-r inverse moment, or full lifetime-intensity claim
is made.

## 2. A once-per-elder selector with a fixed shape domain

Use the root variables of R/C:

 u=X+aZ/(12k), b0=3-12u^2, v=(-s)Z^2/k,
 S={-3/2<u<1/2, |b0|/2<v<3-6u},
 eta=u+1/2+v/6,
 Q(u,v)=(4v^2-b0^2)(b0-4uv)>0 on S.                       (4)

A counted companion is given, off an algebraic null set, by

 Lc=4v^2-8b0uv+b0^2,
 t_c=(4v^2-b0^2)/Lc,
 u_c=[2b0v-u(4v^2+b0^2)]/Lc, v_c=v t_c^2.                 (5)

C proves that the map is an involution, t_c<0 on doublets, and that for an
outer-|Z| root eta_c<eta. With p=-u and A(p)=12p^2-3, the outer-root sector is

 O2:
   1/2<p<1,   A/2<v<A p;
   1<=p<3/2,  A/2<v<3+6p.                                (6)

Let E=S\O2, apart from the null equal-height curve where ties are shared.

**Lemma 1.** In a singleton, E retains the sole root. In a doublet it retains
only the higher saddle, i.e. the inner-|Z| root with smaller eta. Thus for any
nonnegative measurable phi,

 integral phi(T_*,eta_*) dmu_F
   = integral [sum_i 1_E(u_i,v_i) phi(z_i,eta_i)] dM.       (7)

The weight on a tied doublet can be 1/2 per root. All tie, height-boundary and
degree-drop sets are source-null. Identity (7) holds for the limiting cubic at
its ACTUAL physical coordinates; it does not order roots by physical radius.

Proof: on a doublet C E17 gives the exact sign identity

 eta_c-eta=2(ell-p)(4p ell-1)^3/(4ell^2-8p ell+1)^2,
                         ell=v/A.

The outer sector has ell<p, so that root is lower and is not the elder choice.
Its companion is higher and is retained. Every other nonempty sector is a
singleton. The weight therefore sums to one per configuration. QED.

The exact masses from C are

 I=integral_S Q=246528/35,
 J=integral_O2 Q=1083417/280,
 D=integral_(inner doublet sector) Q
      =27066286003/223205220-(79298560/4782969)log2.

Consequently

             E0=integral_E Q=I-J=888807/280.               (8)

In particular E0 differs from the maximum-cluster coefficient I-D. The
cancellation of D here is structural: the elder selects the opposite doublet
root, not a modified numerical estimate of the same selector.

## 3. Selected-partner radius and the actual-field transfer

Retain R's positive finite cusp integral J_cusp and put

 C_cusp=(216/11)k^7(c_m/z0)J_cusp,
 gamma(a)=sqrt(1+(a/(12k))^2).

Define G_eld(t)=mu_F(|T_*|>t). Then

 **Theorem 1.**
 G_eld(t) ~ C_cusp E0 t^-11,
 mu_F(n=2,|T_*|>t) ~ C_cusp D t^-11.                     (9)

For every fixed t>0 the radius event is a continuity set of the limiting
selected measure, and therefore

 lim_(t->infinity) t^11 lim_(r->0)
 r^-3 Q_r^W(F_r, |T_r|>t, T_r finite)=C_cusp E0.          (10)

Conditional on a distant actual failed partner, in that same iterated order,
its lifetime fraction and selected shape have the universal laws in Section4.
This is candidate pair-Palm sampling given failure; it does NOT count each
replacement persistence bar once across different rejected candidates.

Proof: inserting (7) into R's root integral gives exactly

 (108 k^7 c_m/z0) Q(u,v)1_E H(h)|Z|^-12
 h0(A0,Rot_O tau(a,a^2/(12k)+k b0/Z^2,
       a^3/(144k^2)+a b0/(4Z^2)+2k(v-b0u)/Z^3,xi))
                      du dv dZ da dxi dh dO.             (11)

The selector 1_E is independent of Z. The radius is still
|T_*|^2=(u-aZ/(12k))^2+Z^2. Under Z=t z it tends, after division by t, to
gamma(a)|z|. For t>=3 the radius condition implies |z|>1/(2gamma(a)).
The source majorant is a polynomial in h times

 Q 1_E |z|^-12 exp[-c(|h|^2+a^2+|xi|^2)]
                         1{|z|>1/(2gamma(a))}.

Integrating z costs only a factor proportional to gamma^11; the remaining
integral is finite. Dominated convergence yields the common C_cusp times the
shape mass E0. Restriction to counted doublets replaces E by the inner sector
and gives D. No hard-eigenvalue inverse or unproved radius ordering enters.

For each t>0 and fixed u,a, the radius equation is a nonconstant quadratic in
Z with at most two solutions, hence null in (11). Thus |T_*| has no positive
atoms. Finite-mass weak convergence in (3), including negligible sentinels,
allows the unbounded exterior-radius indicator by Portmanteau. A bounded
continuous function of the other marks can be inserted as well, since its
only new discontinuity is that sphere. The denominator G_eld(t)>0 for all t,
by the positive tail at large t and monotonicity. This proves the fixed-t
conditional transfer and then (10). No uniformity in a moving t(r) is used.
QED.

Some exact coefficient ratios, independent of the model amplitude, are

 G_eld(t)/F_point(t) -> E0/I=296269/657408,
 G_eld(t)/G_max(t) -> E0/(I-D),
 mu_F(n=2,|T_*|>t)/G_eld(t) -> D/E0.                     (12)

They are approximately0.450662298,0.457796706,0.0345807201, respectively.
These are three different denominators. The final doublet probability concerns
the local cubic configuration of an extreme elder, not the global torus count.
The role of n here is entirely inside the limiting measure; no global-count
moment theorem is needed to identify the actual partner.

For nonnegative powers, the radius of this selected limiting law has moment
threshold11, and

 integral min(|T_*|,t)^11 dmu_F ~11 C_cusp E0 log t.       (13)

The proof is Tonelli applied to (9). It is not uniform integrability of the
finite-r spatial moments in (3).

## 4. An explicit universal lifetime-fraction density

In the extreme-selected limit, the shape density is Q1_E/E0. The normalized
radius q=|T_*|/t is independently Pareto(11), with density11q^-12 on q>1;
its sign is symmetric and the remaining cusp parameters have their original
H gamma^11 h0/J_cusp density. This follows from (11) with q=gamma(a)|z|,
using the same majorant. Projecting to physical spatial marks gives WEAK
convergence. No assertion of spatial total variation is required.

**Theorem 2.** Let e in(0,1). Define

 p_lo(e)=sqrt(1-e)-1/2,
 p_hi(e)=cos((1/3) arccos(2e-1)).                         (14)

Equivalently p_hi is the unique root in(1/2,1) of
2p^3-(3/2)p+1/2=e. The limiting fraction lambda=(b-death)/(k r^3) of a distant
failed elder partner has density

 f_eld(e)=(6/E0) integral_(p_lo(e))^(p_hi(e))
                        Q(-p,6(e+p-1/2)) dp.             (15)

The integrand is a polynomial, so (15) is an explicit algebraic density with
one radical and one specified cubic root. It is strictly positive on(0,1).
This is a density of the LIMITING conditional mark, not an assertion that the
original fixed-r persistence intensity has this density or converges in TV.

Proof: eta=e sets v=6(e+p-1/2), dv=6 de. The full shape region at fixed e gives

 sqrt(1-e)-1/2 < p < 1/2+sqrt(e).

For p>1/2 write x=p-1/2. The lower shape condition becomes x^2<e, while the
upper edge v=A p of the outer strip becomes e<3x^2+2x^3. For p>=1 the entire
shape interval is outer. It follows that O2 removes exactly

 p_hi(e)<p<1/2+sqrt(e).

What remains is precisely (15). The cubic is strictly increasing for p>1/2;
4cos^3(theta)-3cos(theta)=cos(3theta) gives (14). Nonnegativity, normalization
and strict positivity follow from the original selected shape integral.

Every nonnegative integer moment is rational. To see this directly, integrate
Q(u,v)(u+1/2+v/6)^j over S and subtract the same polynomial integral over the
two strips (6), all of which have polynomial bounds and rational endpoints.
The first three unnormalized moments are

 E0=888807/280,
 E1=3524743221/1361360,
 E2=190490806059/87127040.

Thus

 E[lambda]=1174914407/1440459878,
 E[lambda^2]=63496935353/92189432192.                     (16)

They are approximately0.8156522961481611 and0.6887658795940618.
Neither is the point-intensity nor the maximum-anchor lifetime mean. All
shape factors are universal in the fixed model parameters; directions and
C_cusp need not be universal. QED.

For reproducible evaluation, with x=p-1/2 the unnormalized density integrand is

 10368(e-x^2)(e+x^2+2x)(e+2ex+x^2).                      (17)

Its integration endpoints are sqrt(1-e)-1 and the nonnegative root of
3x^2+2x^3=e. The companion uses rational bisection plus interval polynomial
evaluation to enclose (15), not unconstrained floating quadrature.

## 5. A fourth-power small-lifetime law and its inverse-moment threshold

**Theorem 3.** In the limiting probability law of Section4,

 f_eld(e) ~ (3328/E0)e^3,
 P(lambda<=e) ~ (832/E0)e^4=(232960/888807)e^4,
 f_eld(1-) =1312200/296269.                              (18)

Consequently E[lambda^-p] is finite exactly for nonnegative p<4. At the critical
order, the capped inverse moment has asymptotic

 E[min(lambda^-1,T)^4] ~ (3328/E0)log T.                  (19)

All three limits occur INSIDE the already-formed extreme-elder mark law: r->0,
then distant-partner radius->infinity, then e->0 (or T->infinity). Weak marked
convergence alone would not justify analogous finite-r inverse moments.

Proof: use (17), put x=sqrt(e)z and divide the density numerator by e^3. The
lower endpoint tends to0, the upper to1/sqrt(3), and the integrand tends to

 10368*2z(1-z^4).

The scaled intervals lie in a fixed compact set for all small e and the
integrands have a common polynomial bound. Hence their limit integral is
10368(1/3-1/81)=3328. Integrating this density asymptotic gives the CDF formula.
At e=1 the integral of (17) over x in[-1,1/2] is98415/7; division by E0 gives
the endpoint in (18). Continuity and strict positivity away from zero then
show that only the lower endpoint controls inverse-moment integrability.
Finally lambda^-1 has tail coefficient832/E0 at exponent4; Tonelli gives
4*(832/E0)log T in (19). QED.

## 6. The more distant companion has a thirteenth-power ratio tail

This section conditions the limiting extreme-ELDER law further on a doublet.
Let rho=|Z_inner/Z_outer| in(0,1) and z in(0,1) be D's unit-square coordinates
of the OUTER root. Write L(rho,z) for D2's unnormalized density:

 L=165888 rho z^7(z+1)^4 (rho z+1)^4(rho z+rho+1)^7
                  /[(rho+1)^5(2rho z+rho+1)^9].          (20)

Its total mass is J. The elder is the inner root. C E18-E19 give the deterministic
change-of-variables identity

 Q(T)|det DT|=Q|t_c|^11,  integral rho^11 L =D.

**Theorem 4.** Under the limiting extreme elder law given a doublet, (rho,z)
has density

                       rho^11 L(rho,z)/D.               (21)

It is NOT L/J. The scalar radial ratio q=|T_*|/threshold remains independent
Pareto(11). In physical positions divided by that threshold the configuration is

          { epsilon q e_*, -epsilon q rho^-1 e_* },      (22)

where the first point is the actual limiting elder and the second the farther,
lower saddle. Its heights are respectively

 eta_eld=rho^3 z^2(z+1)(rho z+rho+2)
                         /[(rho+1)(2rho z+rho+1)],
 eta_other=z^2(rho z+1)(rho z+2rho+1)
                         /[(rho+1)(2rho z+rho+1)].       (23)

Let V=R_other/R_eld=1/rho in this limit, and H0=6401/3960. Then

 P(V>T | extreme elder, doublet) ~ C13 T^-13,
                       C13=165888 H0/(13D)>0.           (24)

Its nonnegative moments are finite exactly below13. Conditional further on
V>T, (T/V,z) converges in total variation on the fixed scalar-coordinate
unit square to independent densities13y^12 and z^7(z+1)^4/H0. In particular

 eta_eld V^3 -> 2z^2(z+1),  eta_other -> z^2             (25)

as a further weak-mark consequence. No spatial TV is claimed for (22).

Proof: the inner-selected shape measure is Q on the inner sector. Pull it
back to the outer sector through the companion involution. The weighted
Jacobian gives exactly the factor rho^11, and then D's unit-square bijection
gives (21). Equivalently the physical inner-radius cutoff has asymptotic
rho gamma(a)|Z_outer|>threshold, giving the same rho^11 after radial integration.
It is not legitimate to retain the old maximum-conditioned doublet density.
The linear transformation of the sign and the radial change q=rho gamma|Z|
yield independence and (22)-(23).

The rational factor multiplying165888 rho z^7(z+1)^4 in (20) converges uniformly
to1 as rho->0 and is bounded on the closed square. Thus the numerator of (21)
is asymptotic to165888 rho^12 z^7(z+1)^4, whose integral over rho<1/T gives
165888 H0/(13D) T^-13. Substituting rho=y/T and dividing by that mass proves
the normalized L1/TV claim. The uniform height limits of (23) give (25).
Moment integrability follows since V>=1 and the tail coefficient is positive.
The density L/J from maximum selection instead has a second-power tail for
1/rho; that is a different measure, not a contradiction. QED.

## 7. Review obligations and excluded conclusions

A: actual-selector composition (1)-(11), matching ELDER2/ELDERD's failure
measure to the root density without a count substitute; no lost sign/Haar/
normalizer; fixed-t continuity and the iterated-limit order.
B: selected shape interval, all polynomial integrals and moments, density
(15), fourth-power endpoint and inverse-moment threshold (18)-(19).
C: rho^11 reweighting, thirteenth-power companion ratio, scalar TV versus
moving spatial marks, and the independence/height statements (21)-(25).

The tests corroborate exact algebra, root domains and interval arithmetic.
They do not prove the Gaussian or actual-pairing sources, grant the new
consumer independent acceptance, or formalize these theorems in Lean.
No original r-limit rate, growing-volume/vanishing-k uniformity, finite-r
inverse moments, unrestricted lifetime density, replacement-bar intensity,
remote singleton elder coefficient or across-pair independence is claimed.
The finite physical-radius ordering counterexample in C is retained: the
elder selector is based on height before taking any radius limit.
