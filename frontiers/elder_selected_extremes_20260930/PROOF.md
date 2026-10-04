# The elder-selected microscopic radius–lifetime law

OpenAI author-side candidate, 30 September 2026. **AUTHOR_SIDE / HOLD.**
Scientific effect NONE. This is a new selector consumer, not another count
estimate. The author contributed PR170/175 and reviewed PR169 Slice A. A
same-provider noncontributor review gives no organizational-independence credit.
All mathematical implications below retain their exact imported hypotheses.

## 1. Interfaces and scope

Fix d>=2, k>0 and the fixed model parameters of the sources. Work first with
the already-formed microscopic finite measure on nonempty configurations.
[RADIAL] R4–R12 supplies the root-resolved density and Gaussian domination;
[CUB] supplies the typed strict-window classifier; [EXT] E12–E19 supplies the
companion map, height ordering and shape partition, and E20–E26 its integrals.
[MICRO] M1–M2 and [SC] supply the original-frame measure and embedding only.
Their global count/moment conclusions are not used. Full immutable public
texts and byte/blob identities are in [SOURCES.json](SOURCES.json).

Only §6 uses an actual finite-r elder theorem: [ELDER] S3 and M1 at its exact
fixed-d>=3 original pair-Palm scope. Its deterministic contained barrier,
whole-field genericity/Borel repair, original full normalization and exhaustion
remain hypotheses of this consumer; linking it does not accept its proof.
This consumer does not independently close PR170/175's composition review.
The d=2 microscopic conclusion does not automatically identify the planar
finite-r law: an exact frame/normalization interface is needed for that use.
No uniformity in dimension, k, hard gaps, t or a simultaneous r,t limit is claimed.

Write theta=(s,h,O,tau). The ordered hard eigenvalues are
0<h2<...<h_(d-1), with empty products in d=2; dO is normalized Haar measure.
The full raw cubic tensor tau omits only the fixed axial entry f_xxx=12k.
Its soft entries are (a,beta,c), and xi denotes all remaining entries. Set

    A0=O diag(0,-h2,...,-h_(d-1)) O^T,
    H(h)=product_j h_j^3 product_(i<j)(h_j-h_i),
    B=beta-a^2/(12k), w=9k^2(4s^2-B^2) 1{s<-|B|/2},
    dM=(c_m/z0) H(h) h0(A0,Rot_O tau) w ds dh dO dtau.       (1)

h0 is the actual RAW contact Gaussian density, without an isotropic
replacement. z0 is the FULL original endpoint normalizer divided by r^2 in
the limit. No second type weight or good-event normalizer is inserted.
Let n(theta) be the number of additional strict-window saddles, excluding
the pins. The imported classifier gives n in {0,1,2} almost everywhere;
the restricted mass A_micro=M(n>0) is finite and strictly positive.
The probability used below is pi=1{n>0}dM/A_micro.

The soft cubic, original position and downward height are

    P(X,Z)=2kX^3-3kX/2-k/2+sZ^2/2+(a/2)(X^2-1/4)Z
                         +(beta/2)XZ^2+(c/6)Z^3,
    z=X e_axis+Z e_soft(O), R=|z|, eta=-P(X,Z)/k.           (2)

Every additional counted root has limiting full index d-1 and 0<eta<1.
On a nonempty configuration, select its root of GREATEST HEIGHT P, with
any Borel convention on ties. Call its position z_E, radius R_E and height
fraction eta_E. Thus eta_E is the MINIMUM downward height, not the maximum.
For now this is an exact cubic selector. Its identification with the actual
ordinary elder partner is explicitly conditional in §6.

## 2. Select the higher root before taking a radius limit

For a counted seed put

    u=X+aZ/(12k), b0=3-12u^2, v=(-s)Z^2/k,
    S={-3/2<u<1/2, |b0|/2<v<3-6u},
    eta=u+1/2+v/6,
    Q(u,v)=(4v^2-b0^2)(b0-4uv)>0.                         (3)

For a doublet define

    L=4v^2-8b0uv+b0^2,
    t_c=(4v^2-b0^2)/L,
    u_c=[2b0v-u(4v^2+b0^2)]/L,
    v_c=v t_c^2, Z_c=t_c Z.                              (4)

This map preserves the jet, swaps the two roots and is involutive off the
null exceptional sets. [EXT] proves its determinant/intensity identity

    Q(u_c,v_c)|det D(u_c,v_c)/D(u,v)|=Q(u,v)|t_c|^11.      (5)

For completeness, the explicit doublet partition needed here is as follows.
Put p=-u, A=12p^2-3 and

    V_+(p)=[36p^2-12p-3+3sqrt((2p-1)^3(18p+7))]/4.

The outer sector O2 has .5<p<1, A/2<v<Ap, together with
1<=p<1.5, A/2<v<3+6p. The inner sector I2 has .5<p<1,
Ap<v<V_+(p). Both labels refer to ABSOLUTE SOFT COORDINATE |Z|,
not finite physical radius. They exhaust doublet seeds up to null curves.
On O2, t_c<0 and |t_c|<1; on I2, t_c<0 and |t_c|>1.

One can verify the partition directly from the strict doublet inequality:

    (v-A)^2(2v+A)-12(v-Ap)^2=(3+6p-v) H_p(v),
    H_p(v)=-2v^2+(36p^2-12p-3)v-72p^3+36p^2+18p-9.

H_p(A/2)>0, its upper root is V_+, and for p<1 its zero lies
between Ap and A; for p>=1 the height cap 3+6p lies below A.
The two admissible roots are on the negative branch of the same hyperbola.
Strict convexity of line-minus-branch, negative at Z=0, puts zero between
the roots, hence t_c<0. Substitution in (4) yields the |t_c| split at v=Ap.
These are the deterministic interfaces of [EXT] E14–E16, not a stochastic
assumption about two independent witnesses.

On a doublet let ell=v/A. Exact substitution gives

    eta_c-eta=2(ell-p)(4p ell-1)^3/(4ell^2-8p ell+1)^2.     (6)

Here p>1/2 and ell>1/2, so 4p ell>1. Consequently the outer seed
has eta_c<eta and is NOT selected; the inner seed has eta_c>eta and
IS selected. The equal-height curve v=Ap is null. Therefore the exact
highest-height seed domain is

    S_E=S minus O2,                                      (7)

containing all singleton seeds and precisely the inner seed of every doublet.
This equality holds at every nondegenerate cubic jet, before any large-radius
limit, and is independent of a and Z. Coarea restricted to S_E consequently
counts one selected root per nonempty configuration. It does not renormalize
the jet measure, double a bar, or equate point intensity with cluster intensity.

## 3. Full root density and selected-tail coefficients

The original density in the root coordinates of [RADIAL] is

    K0 Q(u,v) H(h)|Z|^-12
      h0(A0,Rot_O tau(a,
          a^2/(12k)+k b0/Z^2,
          a^3/(144k^2)+a b0/(4Z^2)+2k(v-b0u)/Z^3,xi))
                          du dv dZ da dxi dh dO,
    K0=108 k^7 c_m/z0.                                   (8)

The physical radius is exactly sqrt((u-aZ/(12k))^2+Z^2).
Multiplying (8) by 1{(u,v) in S_E} and 1{R>t} is an EXACT
representation of E(t)=M(n>0,R_E>t), since (7) selects precisely one seed.
The doublet version E2(t)=M(n=2,R_E>t) restricts the shape to I2.
The singleton version E1(t) restricts it to S minus (O2 union I2).

Define

    gamma(a)=sqrt(1+(a/(12k))^2),
    J_cusp=integral H(h) gamma(a)^11
      h0(A0,Rot_O tau(a,a^2/(12k),a^3/(144k^2),xi))
                                        da dxi dh dO,
    C0=(216/11) k^7(c_m/z0) J_cusp,
    I=246528/35, J=1083417/280,
    D=27066286003/223205220-(79298560/4782969) log(2).       (9)

[EXT] E20–E26 gives integral_S Q=I, integral_O2 Q=J,
integral_I2 Q=D. The last integral is the inner-root integral, not a hard
curvature or the cubic coefficient sometimes denoted D. These exact
integrals are imported, not inferred from a numeric PASS label.

**Theorem 1.** For the fixed microscopic measure (1),

    E(t)  ~ C0(I-J)t^-11,
    E2(t) ~ C0 D t^-11,
    E1(t) ~ C0(I-J-D)t^-11.                               (10)

All three coefficients are strictly positive. In particular, conditional on
R_E>t under pi, the doublet probability tends to D/(I-J). This differs from
the cluster-MAXIMUM doublet frequency J/(I-D).

Proof. Put Z=t z in (8), retaining the selector (7). The Jacobian contributes
t^-11 |z|^-12 dz. At each fixed nonzero z, beta and c tend to the cusp
entries in (9), and R/t tends to gamma(a)|z|. The shape selector remains
exactly S_E; it need not converge from a radius-based selector.
For t>=3, R>t and |u|<1.5 imply |z|>1/(2gamma(a)) by
t<R<=|u|+gamma|Z|. Orthogonal Gaussian norm equivalence gives

    h0(A0,Rot_O tau(a,beta,c,xi))
                  <=C exp[-c'(|h|^2+a^2+|xi|^2)].

Dropping beta,c from this upper bound is valid. The integral of |z|^-12
over |z|>1/(2gamma) costs C gamma^11. S is bounded, Q is bounded on S,
H is a nonnegative polynomial and Haar measure is finite. Thus the remaining
Gaussian integral is finite. This proves domination over all unbounded
retained variables without an inverse hard eigenvalue. The limiting integral
on each sign is gamma^11/11. Both signs and K0 give C0 times the shape
integral I-J, D or I-J-D. This proves (10).
Strict positivity follows from open inner-doublet and singleton sectors,
Q>0 and positive raw Gaussian density. For example a neighborhood of
u=0, v=2 is a singleton sector: b0>0 excludes a doublet. J_cusp is positive
and finite by the same Gaussian argument. QED.

## 4. The selected joint radius, location and lifetime-fraction law

**Theorem 2.** Under pi conditional on R_E>t, retain the selected seed
shape (u,v), q=R_E/t, epsilon=sign Z and (a,h,O,xi). Their weak limit is
the product probability

    Q(u,v)1{S_E}/(I-J) du dv;
    11q^-12 dq on q>1;
    uniform epsilon in {-1,1};
    H(h)gamma(a)^11 h0(A0,Rot_O tau_cusp)/J_cusp
                                        da dxi dh dO.    (11)

The selected height fraction is eta_E=u+1/2+v/6. Its limiting law is the
pushforward of the FIRST factor in (11), independent of q and the remaining
factors. Thus (11) specifies the selected lifetime-fraction distribution,
without substituting the point-selected or maximum-radius height law.

With e_*=[-a e_axis/(12k)+e_soft(O)]/gamma(a), the selected position
divided by t tends to epsilon q e_*. For doublets the companion position
divided by t tends to -epsilon q |t_c| e_*, where |t_c|>1 on I2;
its height fraction eta_c exceeds eta_E by (6). The selected root is therefore
asymptotically the higher, nearer root of this extreme doublet, while the
other root is deeper and farther. These are SECOND limits of the microscopic
geometry, not finite-r collinearity or independence of two roots.

Proof. Insert a bounded continuous test function in the exact selected
integral (8). The majorant in Theorem 1 is unchanged. Dominated convergence
and q=gamma(a)|z| give gamma^11 q^-12 dq; normalization by (10)
produces (11). The position map is continuous away from already null
exceptional sets and has the limits just displayed. One may exhaust compact
shape/latent subsets to avoid the rational companion denominators on the
boundary, then let the excluded mass tend to zero under the integrable
limit density. This proves joint weak convergence of the marked finite
configurations, not moving-map TV convergence of positions. QED.

An equivalent description of the doublet shape is useful for consumers of
the outer-root chart. If rho=|t_c|<1 on O2, swapping inner to outer in (5)
gives outer density Q rho^11/D. The ordinary maximum-radius outer density
is Q/J. Hence elder-selected extreme doublets have an additional rho^11
size bias. This is a deterministic root-swap identity, not a temporal Palm
or independent-root hypothesis. It also makes clear why the maximum-radius
law cannot be copied as the actual elder-selected law.

## 5. Physical-order falsifier retained at finite radius

Do not replace E2(t) by the doublet minimum-physical-radius tail at finite t.
They have the same leading coefficient C0 D, but their selectors can differ.
Here is an exact typed cubic example, k=1:

    Z=1, a=-12, s=-14/5, beta=33/4, c=-31/40,
    u=-3/4, v=14/5, eta=13/60, R^2=17/16,
    u_c=-20907/28124, Z_c=-6919/7031,
    v_c=670215854/247174805,
    eta_c=618523783/2966097660,
    R_c^2=3126268865/790959376.                           (12)

Both roots are strict-window saddles. eta_c<eta, so the companion is the
highest-height selector, but R_c>R. Substitution in (2)–(4) verifies every
entry. The typed inequality holds since B=-15/4 and s=-14/5<-15/8;
the seed is in O2 and its companion in I2. For thresholds between these
two radii, the selected doublet exceeds the threshold while the minimum
radius does not. Thus a finite-t physical-minimum identity is false.
Only after Z=t z and t->infinity does the bounded u offset vanish. A
proof that silently identifies the selectors before that limit is invalid.

## 6. Sequential consequence for the actual elder partner

Fix d>=3 and the exact source parameters and original Q_r^W of [ELDER].
Let F_r be failure of pairing M with S; T_r the actual partner displacement
divided by r, and L_r=(b-d_f(M))/r^3. As in [ELDER], chart/essential
exceptions use an isolated sentinel; only REAL T_r enter a radius event.
Assume [ELDER] S3/M1, including its full exhaustion and sentinel exclusion.
Its limit measure is exactly 1{n>0}dM in (1), with selected position z_E
and death value -k eta_E. The equality of measures is termwise: original
c_m/z0, normalized Haar, ordered hard spectrum, full raw tensor and w on
the same typed domain. No new normalization or point-count factor occurs.

**Corollary 3 (sequential actual selector/lifetime law).** For every fixed t>0,

    lim_(r->0) r^-3 Q_r^W(F_r, T_r real, |T_r|>t)=E(t).

Consequently

    lim_(t->infinity) t^11 lim_(r->0)
       r^-3 Q_r^W(F_r,T_r real,|T_r|>t)=C0(I-J).          (13)

Conditional on this actual event, first let r->0 at fixed t, then let
t->infinity. The limit of (T_r/t,L_r/k), and the retained microscopic
marks when desired, is the selected law of Theorem 2: position epsilon
q e_* and lifetime fraction eta_E with the FIRST shape factor of (11).

Proof. [ELDER] M1 is weak convergence of finite measures, with mass limit
from S3. The boundary {|z_E|=t} has limiting measure zero. Indeed, in (8)
restricted to S_E, for fixed other coordinates R^2=(u-aZ/(12k))^2+Z^2
is a quadratic in Z with strictly positive leading coefficient gamma^2.
The equation R=t has finitely many Z solutions and hence zero mass in the
absolutely continuous root integral. Portmanteau therefore gives the
fixed-t event mass and bounded continuous marked tests restricted to that
event. E(t)>0: an open singleton shape and arbitrarily large |Z| in (8)
have positive density. Divide by E(t) to obtain the first conditional limit,
then apply Theorems 1–2 for the second. Sentinel mass is o(r^3) by the
imported exhaustion. No moment uniform integrability is used. QED.

Equation (13) is an ITERATED limit. It proves neither a uniform finite-r
radius bound nor a limit for t=t(r), nor finite-r lifetime moments, essential
class probabilities, unconditioned bar intensity, or identification outside
the exact imported elder interface. The active lifetime-moment review is
not consumed by this proof. The present step advances which saddle pairs
and its lifetime mark; the original source composition remains conditional.

## 7. Falsifiers and remaining acceptance obligations

This consumer fails if: (6) selects the wrong height root on an open doublet
set; S_E does not contain exactly one seed; the original unsheared density
(8) loses a Jacobian or type weight; the Gaussian majorant is unavailable
for the fixed source; or [ELDER]'s selected limit/normalization does not
match (1). Failure of [ELDER] invalidates §6, not the separately formed
microscopic implications of §§2–5. Example (12) falsifies the tempting
finite physical-minimum substitution, not (10).

A qualified source-bound noncontributor review of this new composition is
still required. Same-provider review, arithmetic checks, hashes, publication,
CI and engineering merge do not establish organizationally independent
mathematical acceptance. No scientific Boolean, predecessor disposition or
prize is changed. The next unresolved issue for this candidate is review of
the exact elder-selected interface, not another count packet.
