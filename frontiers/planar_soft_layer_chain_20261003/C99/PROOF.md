# Once-counted replacement-bar lifetime densities

Object: C99-WEIGHTED-LIFETIME-DENSITY-20261003-v1.
Authors: OpenAI/Codex `/root` (native coordination identifier root01a0adb2),
`/root/bridge_chain_scan`, and `/root/c93_edge_integral_audit`.
Additional mathematical contributor: OpenAI/Codex root01a0bbb5, who supplied
the total-mass-to-global-L1 corollary in section 6. Custody/coordination:
root01a0bbb5. Dylan Roy — delegated AI work.
The authors supplied the preceding source/feasibility analysis; those analyses
are not nonauthor reviews. Runtime model identifier is not exposed here;
provider OpenAI, executor Codex. Organizational independence 0; human review
NONE; Dylan's personal reading PENDING; scientific effect NONE.

This is an additive conditional consumer proof. It does not amend any source,
declare an integration ready, or change a scientific-status register. The
Conjecture 7 moving-window remainder is not consumed or discharged.

## 0. Exact sources and the inherited hypotheses

[U] is Math233 at commit
`b5bf02879a5645da9a69d9944dee610e6bb14bf6`, path
`frontiers/unique_replacement_bar_intensity_20261001/PROOF.md`, blob
`9c79a672f5d81e04972032b2f1faf185f4664fa5`, 17545 bytes, SHA256
`ba1901cbb4bac037befb21d648172ac3ba04aa370f5377a2919c0da988572552`.
Its ROOTS.md, denoted [ROOTS], has blob
`b27d9ac8111c83f4967d837eee22057583c41eae`, 11969 bytes, SHA256
`29e79b60a382b95cc0fa2375b82845a5558942cf81a2a836262e7479f9d570e6`.
[O] is Math234 at commit
`a38449c30c44733dfb5cd128d11071fac2e0ea98`, path
`frontiers/replacement_bar_occurrence_20261001/PROOF.md`, blob
`724258d33408f754ffc21848196e1fdd80c8bf6a`, 12965 bytes, SHA256
`b49f2ea5975dc05270f51fea4a3574093f726258cdab94888742507c2caa275f`.

Full public texts:
[U](https://github.com/d6g8k5htny-coder/Math-/blob/b5bf02879a5645da9a69d9944dee610e6bb14bf6/frontiers/unique_replacement_bar_intensity_20261001/PROOF.md),
[ROOTS](https://github.com/d6g8k5htny-coder/Math-/blob/b5bf02879a5645da9a69d9944dee610e6bb14bf6/frontiers/unique_replacement_bar_intensity_20261001/ROOTS.md),
[O](https://github.com/d6g8k5htny-coder/Math-/blob/a38449c30c44733dfb5cd128d11071fac2e0ea98/frontiers/replacement_bar_occurrence_20261001/PROOF.md).

The seven imported interfaces are pinned at Math commit
`044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43`:

| Key | Canonical Math path | Exact Git blob |
|---|---|---|
| P | imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md | dfed3b8d318a3ab1950957f393307733a4bef3f2 |
| CAP | imports/lifetime_parent_20260925/MARKED_CYLINDER_CAP_PROOF.md | 0633aca3c2a2882b0de4399da0a75d64c2e6b2e1 |
| E1 | imports/lifetime_parent_20260925/ERRATUM_CONGRUENCE.md | 213594d6ca6a86fb938110f4d166d9ce275a02d0 |
| E2 | reviews/d1_section9_borel_repair_20260925/REPAIR.md | fe9b9ce4999908bb3814b500ee2d0ceb0c6f704a |
| REC | reviews/d1_chain_reconciliation_20260928/RECONCILIATION.md | 75da2597971510f843f8d90c743950cb8c177342 |
| CUB | frontiers/planar_cubic_cluster_20260929/PROOF.md | bb446d08db8a944537a743ad550b88c1c2ad5758 |
| ELDER | frontiers/local_elder_geometry_20260930/PROOF.md | ef2aa57959ea9f721bbf2316ce94cf616c1c9113 |

The exact byte/SHA256 identities and canonical links are in
[U's source manifest](https://github.com/d6g8k5htny-coder/Math-/blob/b5bf02879a5645da9a69d9944dee610e6bb14bf6/frontiers/unique_replacement_bar_intensity_20261001/SOURCES.json).
All seven were checked against fetched raw UTF-8 bytes, length, SHA256 and Git
blob identity for this attempt. Read P with E1's congruence, E2's full-field
Borel replacement, REC's W1 wording and embedded-chart restriction.

Consumed interfaces: P §§1–5, its compact failure bound (7.8), fixed-pin
genericity §8 and radial ledger §§9–10; E2's full-field marked pair identity
and two-height disintegration; CUB's complete cubic equations, G6–G10 coupling,
rare determinant scale and full normalizer, and G13 integrability; ELDER
Theorem E including its exact finite-index death/partner statement, S9 actual
weighted-failure exhaustion and S11–S14 envelopes; ROOTS R1–R3 all-root and
integrated cutoff stability; U's exact reciprocal formula (8), compact-box
disintegration (9) and outer domination. O is needed only in §7 below.
These analytic interfaces remain hypotheses of this consumer, not newly
proved or accepted imports.

Historical exact-source reviews are retained:
[U full OpenAI review5382933608](https://github.com/d6g8k5htny-coder/Math-/pull/233#pullrequestreview-5382933608),
[U A/B review5383306337](https://github.com/d6g8k5htny-coder/Math-/pull/233#pullrequestreview-5383306337),
[U C review5384157901](https://github.com/d6g8k5htny-coder/Math-/pull/233#pullrequestreview-5384157901),
[O full OpenAI review5383466767](https://github.com/d6g8k5htny-coder/Math-/pull/234#pullrequestreview-5383466767),
and [O review5384065804](https://github.com/d6g8k5htny-coder/Math-/pull/234#pullrequestreview-5384065804),
with [its exposure-reference correction5938386341](https://github.com/d6g8k5htny-coder/Math-/pull/234#issuecomment-5938386341).
Their stated source-author exposure, conditionality and engineering exclusions
are preserved. They are not reviews of C99.

## 1. Fixed population and conclusions

Use U's fixed planar torus T_L^2 and centered variance-one periodized Gaussian
field. Fix positive-length compact B and K=[k_-,k_+] with k_->0, and
0<c_0<C_0. These parameters, L and dimension two are fixed before h tends to
zero. Work on the ordinary superlevel H0 Morse/distinct-value locus and give
all counting expressions value zero off it. The essential global-maximum
class is excluded; the longest finite bar is not discarded.

For a finite maximum M let S_*(M) be its actual global elder saddle and let
D_h(M) count rejected index-1 candidate saddles S with

    c_0 h <= dist(M,S) <= C_0 h,
    (f(M)-f(S))/dist(M,S)^3 in K,  S != S_*(M).

Define the once-counted, per-unit-area lifetime measure

    eta_h(A)=L^-2 E sum_{finite M: f(M) in B, D_h(M)>0}
                   1{(f(M)-f(S_*(M)))/h^3 in A}.             (D1)

No cutoff is imposed on the ACTUAL partner in this definition. In particular
remote death partners are not removed from finite-h counts. U identifies
h^-5 eta_h weakly with the lifetime marginal eta_0 of C_U, a finite measure
of positive total mass C_U(1).

**Theorem D.** Conditional on the retained interfaces above:

1. For every sufficiently small fixed h>0, eta_h is absolutely continuous on
   (0,infinity), with a finite integrable density q_h.
2. eta_0 is absolutely continuous, with the explicit density (D3) below and
   total mass C_U(1)>0.
3. For every fixed compact J=[j_-,j_+] contained in (0,infinity),

       || h^-5 q_h - q_0 ||_{L1(J)} -> 0.                 (D2)

4. For this SAME fixed-band population the convergence also holds in
   L1(0,infinity), by its existing total-mass limit and nonnegativity.

This is unsmoothed convergence for the specified once-counted compact-band
population. No rate, uniformity over changing bands or J, joint continuous-
mark total variation, all-bar coefficient, global program closure, or
moving-window remainder is asserted.

## 2. Finite-h absolute continuity using the actual pair

This step uses a different exact representation from U's rejected-candidate
sum. Each selected finite bar has exactly one ordered ACTUAL pair (M,S_*(M)).
Its selection 1{f(M) in B,D_h(M)>0} is a whole-field Borel mark by U §4 and
E2. Thus there is no reciprocal D_h in this representation: no rejected
representatives are being counted. U's candidate representation still needs
its reciprocal and will be used in §§4–6.

On any compact ordered-pair domain separated from the diagonal, E2 gives
marked Kac–Rice with endpoint-gradient pins and determinant weight. By P's
distinct-site rank, the two endpoint heights have a nonsingular joint
Gaussian density conditional on those gradients. Disintegrate them as
(b,d) and change coordinates to tau=(b-d)/h^3. A Lebesgue-null set of tau has
a Lebesgue-null preimage in (b,d), since the coordinate transformation is
linear and nonsingular. Integration of the nonnegative Borel conditional
weight therefore gives zero mass to that set.

Exhaust the off-diagonal pair space by dist(x,y)>=1/n. Every actual birth/
death pair is distinct and appears eventually. Nonnegative monotone
convergence proves absolute continuity of the entire selected measure, not
only of a locally truncated actual-pair measure. Its mass is finite: the
selected count is at most the admissible rejected-candidate count, whose
fixed-h compact radial band has finite expected count by U (8) without the
reciprocal multiplier and P's compact bound on A_r. Essential maxima have
zero actual-pair mark throughout.

For clarity an a.e. density is obtained by the same exhaustion of

    q_h(tau)=h^3 L^-2 integral_{x!=y} integral_{b in B}
      p_{O_xy}(b,0,b-h^3 tau,0)
      E[W_xy e_f(x,y) 1{D_h(x)>0} | O_xy=(b,0,b-h^3 tau,0)]
      db dx dy,

where O_xy=(f(x),grad f(x),f(y),grad f(y)),
W_xy=|det H_x det H_y| times the maximum/index-1 type indicators, and e_f
is the actual ordinary elder mark, zero for an essential maximum and off the
generic locus. The factor h^3 is the death-height Jacobian. This is the
un-tilted conditional expectation with W inside it; it introduces no Z.
One may instead use its full tilted law and one Z, but not both conventions
simultaneously. The formula establishes AC, not a density asymptotic.

## 3. Explicit limiting lifetime density

In U (3), on the generic nonempty failure sector write

    z=z(k,theta)=-h_*(k,theta),  0<z<k,
    t_tau=(tau/z)^(1/3).

For each fixed (b,k,u,theta), the map tau=t^3 z is strictly increasing on
[c_0,C_0]. Its derivative is 3t^2 z, so t^4 dt=t^2/(3z) d tau. Tonelli,
which retains the possibly discontinuous reciprocal count, gives

    q_0(tau)=integral_{B x K x S1} A_0(b,k,u)
      integral_{failure}
       [tau^(2/3)/(3 z^(5/3) D_{(t_tau,k)}(theta))]
       1{c_0^3 z < tau < C_0^3 z}
       d mu_fail^(b,k,u)(theta) db dk d sigma(u).          (D3)

The integrand is defined to be zero unless its displayed sector and t-range
hold; D>=1 there. Endpoint choices do not affect an a.e. density.
mu_fail is CUB/ELDER's determinant-weighted Gaussian measure, not an
independent product replacement. Its k, birth and frame dependence remains.

The integral of (D3) over positive tau equals C_U(1), by reversing this
change of variables. Thus q_0 is integrable and eta_0 has no atom at zero.
Its support is contained in (0,C_0^3 k_+). On J every contributing z obeys
z>=j_-/C_0^3, so no inverse-zero-gap singularity is used. Positivity of total
mass comes from U (4), not a claim that q_0 is positive on every chosen J.
This calculation alone would NOT establish (D2).

## 4. An actual scalar family at fixed radius

Set theta=k eta, eta=(eta_s,eta_a,eta_beta,eta_q). ROOTS R2 gives

    P_(k,k eta)=k P_eta,  P_eta=P_(1,eta),
    dtheta=k^4 d eta.                                     (D4)

Let G be the open set of strictly typed eta with a nonempty model window,
excluding Sigma,Delta,D_s=0 and the all-root Hessian polynomial H=0 in
ROOTS R1. All those zero sets are null after positive scaling. On G the
unique highest model window saddle Y_*(eta) varies continuously locally,
and z_eta=-P_eta(Y_*) lies in (0,1). Take any compact E contained in G.
Model roots, their nondegeneracy, the highest-height gap and z_eta have
uniform margins on E, by the root classification, the exclusions and
compactness. In particular all roots are in a common finite disk; Delta's
homogeneous-gradient floor and bounded coefficients supply that disk.

Fix the outer birth/frame and one common smooth unconditioned field F in
CUB G6. At physical separation r, the regression observations V_r and
covariance Gamma_r depend on r and frame, NOT on the imposed target. P (3.3)
and the appended physical jet give the exact target

    (b-k r^3/2,-k r^2,0,12k,0,0;
     r k eta_s,k eta_a,k eta_beta,k eta_q).               (D5)

Consequently the coupled whole field f_r^(k eta) is exactly affine in k.
For its local normalization g_r^k(X,Z)=(f_r^(k eta)(rX,rZ)-b)/r^3,
choose two distinct fixed positive target values k_a,k_b covering K.
Then exactly

    partial_k g_r^k=(g_r^(k_b)-g_r^(k_a))/(k_b-k_a).

G7–G8 at these two targets give, on every fixed disk, in spatial C2,

    g_r^k -> k P_eta,  partial_k g_r^k -> P_eta,           (D6)

uniformly on K x E for each smooth F. The uniformity follows directly from
the compact-target G7 bound, the G8 error bound and affine interpolation;
compact outer births/frames have bounded coefficient functions and inverse
covariances by positive rank and continuity. No remainder is differentiated
in r. This is a correctly conditioned affine family, NOT multiplication of
an arbitrary sampled Gaussian field by k.

The spatial implicit-function theorem now continues Y_* to Y_r(k,eta),
C1 in k. All root neighborhoods and floors can be chosen uniformly on the
displayed compacts. The model highest root remains the highest continued
window root. Criticality removes the location derivative:

    d/dk g_r^k(Y_r(k,eta))=partial_k g_r^k(Y_r(k,eta))
                            -> -z_eta.                   (D7)

### Exact actual-global identification, not just a local root

There is one sufficiently small-r threshold, allowed to depend on F,E and
the fixed outer parameters, such that global maximin death equals this
continued root for every k in K,eta in E. To prove this from the pointwise
source, suppose otherwise and choose violating r_i->0,k_i->k_0,eta_i->eta_0
after subsequences on those compacts. Positively rescale the actual global
functions as

    f_tilde_i=b+(k_0/k_i)(f_(r_i)^(k_i eta_i)-b).

They retain exact pins/gradients, now of heights b,b-k_0 r_i^3, and their
local normalized functions converge C2 on every fixed disk to k_0 P_eta0.
ELDER E(3) applies to this SINGLE fixed generic cubic. It identifies exact
global normalized death with the highest actual continued local saddle
for all sufficiently large i. Uniqueness of the model highest root and
the same local IFT identify this root as Y_(r_i)(k_i,eta_i).

Positive affine scaling preserves paths, older endpoints and maximin:

    d_(f_tilde_i)(M)-b=(k_0/k_i)(d_(f_i)(M)-b).

This contradicts the selected violations. ELDER's doubled critical chord
also supplies an older endpoint, so this maximum is finite. E(3)'s exact
death-LEVEL assertion is deterministic and requires no global Morse
assumption; the assertion that its unique saddle is the ordinary elder
PARTNER is used only on each globally Morse/distinct-value member.
No simultaneous Morse assertion for the uncountable k-family is made.

Put r=th. Thus the actual lifetime on generic members is

    T_h(k)=-t^3 g_(th)^k(Y_(th)(k,eta)),
    T_h -> T_0(k)=t^3 k z_eta,
    T_h' -> t^3 z_eta>0                                  (D8)

in C1(K), uniformly on compact E and the fixed positive t band, for each
F. In particular T_h is eventually an increasing diffeomorphism onto its
image with derivative at least c_0^3 min_E z_eta/2. This takes no t or r
derivative.

### Counts at inverse-image points

Away from image endpoints, k_h(tau)=T_h^-1(tau) tends to
k_0=tau/(t^3 z_eta). Along any sequence h_i->0 these moving-target local
fields converge to k_0 P_eta. ROOTS R1's all-root control in the fixed
candidate disk |Y-M0|<=C_0/t and strict limiting membership margins continue
every admissible root, including those below the pinned window. Their
inertias, radii and normalized gaps stabilize; the actual continued partner
is excluded by the preceding exact-global step. Hence

    D_h(M;k_h(tau),eta) -> D_(t,k_0)(k_0 eta),             (D9)

eventually equality of integers, at almost every integrated inverse point.
ROOTS R2 proves JOINT dt dk dtheta nullity of membership boundaries.
The changes theta=k eta and tau=t^3 k z_eta have positive Jacobians on E,
so that nullity transfers to inverse coordinates. Radius boundaries use t;
gap boundaries use k. The pinned fixed-k endpoint slices are not declared
null. We never differentiate a reciprocal or a cutoff indicator.

For any countable sequence h_i, six-pin Morse/distinct genericity followed
by physical-jet disintegration and Fubini gives the required property for
almost every integrated (t,b,u,eta,F,k) at each h_i. The eventually positive
scalar Jacobian carries those null k-sets to null tau-sets. A countable union
suffices. There is no common probability-one statement over all real h,k.

## 5. Weighted scalar pushforward lemma

We use total variation norm |nu|(R), which equals the L1 norm of a density
for a signed AC measure; probability TV distance conventionally divides it
by two.

Let K be a compact interval and T_i,T_0 increasing C1 maps on K with
T_i->T_0 in C1 and inf_K T_0'>0. For any a_0 in L1(K),

    || (T_i)#(a_0 dk) - (T_0)#(a_0 dk) ||_var -> 0.      (D10)

Proof: first let a_0 be continuous. The density is
1_{T_i(K)} a_0(T_i^-1(tau))/T_i'(T_i^-1(tau)). Images have converging
endpoints, inverses converge on the interior, and denominators have a
positive common floor. On a fixed bounded interval containing all images,
bounded convergence proves L1 convergence, with image endpoints a null
exception. For general a_0 choose continuous v with ||a_0-v||_1 small.
Pushforward contracts variation, so the two approximation errors are at
most 2||a_0-v||_1. Take i->infinity and then the approximation error to zero.
This proves (D10), including discontinuous reciprocal/count weights.

If also ||a_i-a_0||_1->0, split the weighted error exactly into

    (T_i)#((a_i-a_0)dk)
      + [(T_i)#(a_0 dk)-(T_0)#(a_0 dk)].                 (D11)

The first norm is at most ||a_i-a_0||_1 and the second tends to zero by
(D10). Thus weighted pushforwards converge in variation. This is not an
inference from weak convergence. It also does not require pointwise
evaluation of arbitrary L1 weights at moving inverse points. D9 separately
establishes the requested actual inverse-count stability.

There is a useful kernel extension. Suppose the scalar maps have the stated
properties eventually for almost every outer parameter xi, with thresholds
depending on xi. Let sigma_i,xi and sigma_0,xi be the true finite Borel
measure kernels. If their masses are bounded by an integrable function G(xi)
and their conditional variation difference tends to zero a.e., then

    || integral sigma_i,xi dxi - integral sigma_0,xi dxi ||_var
       <= integral ||sigma_i,xi-sigma_0,xi||_var dxi -> 0. (D12)

The norm in the right integrand is measurable: for finite Borel measures on
the real line, variation is the supremum over finite partitions drawn from
the countable algebra of rational intervals (including tails). Regularity
and approximation give the full variation norm from this algebra. Its
supremum is measurable for Borel kernels. Before an eventual smooth-family
threshold the difference is bounded by the two masses, so dominated
convergence still applies. No measurable random-threshold certificate or
uniform threshold over samples is assumed.

## 6. Apply the lemma to the actual weighted measure and exhaust

Use U (8),(9),(11) with r=th and theta=k eta. Let xi=(t,b,u,eta,F), with
outer Lebesgue/arc measure, d eta and the fixed law of the common field F.
The exact scalar-base amplitude before its lifetime pushforward is

    a_h(xi,k)=t^4 A_r (r^2/Z_r)
      h_r(rk eta_s,k eta_a,k eta_beta,k eta_q) k^4
      [W_r(f_r^(k eta))/r^4]
      1_failure 1_finite / D_h(M).                        (D13)

The generic-locus convention is included in the last multiplier. It is
bounded by one and defined as zero when the count vanishes. The actual
lifetime map is Borel; set it to zero whenever its multiplier is zero.
This defines sigma_h,xi for all h, even before a smooth branch is available.
Integrating these kernels gives exactly h^-5 eta_h.

The limit amplitude on the generic nonempty sector is

    a_0(xi,k)=t^4 A_0 z_0^-1
      h_0(0,k eta_a,k eta_beta,k eta_q)
      k^4 w(k,k eta)/D_(t,k)(k eta).                      (D14)

It is zero off that sector and independent of F. In particular
w(k,k eta)=k^4 w(1,eta), so this coordinate expression contains k^8, not
just the k^4 determinant factor. There is exactly one full normalizer:
A_r=12 pi_r Z_r/r^2 cancels Z_r once in (D13), and A_0/z_0=12 pi_0
in (D14). Neither cancellation changes the correlated Gaussian density or
permits independence of a jet and remainder.

On every bounded eta box the common envelope is

    0<=a_h,a_0<=C_T (1+||F||_C4)^4.                     (D15)

This follows from compact outer bounds, k_->0, k_+<infinity, G7/G9's
determinant bound and bounded local physical-jet densities. Its expectation
is finite. Gaussian covariance/rank continuity on compact births, gap and
frame parameters gives the needed uniform constants; no isotropy is used.

For almost every fixed (xi,k), U/ROOTS/ELDER give convergence a_h->a_0.
On generic failure this is actual partner/count stabilization, convergence
of W_r/r^4 and of the Gaussian density and full normalizer. On the typed
empty-window sector actual failure eventually vanishes. Outside strict
typing the limiting determinant-times-type weight is zero, including its
boundary; no selector convergence is presumed there. The polynomial
exclusions have integrated measure zero. Along any arbitrary sequence h_i,
the countable genericity/Fubini argument of §4 and (D15) therefore give

    ||a_(h_i)(xi,.)-a_0(xi,.)||_{L1(K)} -> 0             (D16)

for almost every xi in each fixed box.

Restrict eta to a compact E contained in G. By §4, for almost every xi,
the true scalar measure eventually equals the pushforward by T_h in (D8),
up to the null generic-locus sets in k. Equations D10–D11 and D16 give
conditional variation convergence. D15 bounds both kernel masses by an
integrable multiple of (1+||F||_C4)^4. D12 thus proves variation convergence
after integration over eta in E and all fixed outer parameters and F.
No scalar AC/coarea assertion is made for the leftover conditional kernels.
Their unconditional AC was already proved independently in §2.

It remains to remove the good-sector restriction rather than assume it
captures all scaled intensity. Exhaust the open G by increasing compacts
E_m, for example bounded sets at distance at least 1/m from its complement.
They can be chosen nested and to cover G. On a bounded eta box D15–D16
also give L1 convergence of joint base amplitudes. Thus for each fixed m,T
the omitted mass inside |eta|<=T tends to its limiting omitted mass.
Since a_0 is supported a.e. on G and integrable, those limiting omissions
vanish as m tends to infinity.

For the unbounded complement |eta|>T, theta=k eta implies
|theta|>k_- T. The actual omitted mass in D13 is bounded by the corresponding
outer integral of

    t^4 A_(th) (th)^-3
      Q_(th)^W(failure, |Theta_(th)|>k_- T).              (D17)

ELDER S9 controls precisely this ACTUAL weighted failure tail. Its iterated
limit is zero. P (7.8) and the bound on A_r give a common integrable outer
majorant; reverse Fatou along each sequence, then dominated convergence in
the outer variables, permit integration of S9's pointwise tail limit.
The limiting tail is finite and vanishes by CUB G13 and U's finite outer
coefficient. This is not an inference from the limiting integral alone.

Consequently

    lim_m limsup_(h->0) integral_{eta notin E_m} a_h = 0,
    lim_m integral_{eta notin E_m} a_0 = 0.              (D18)

Pushforward never increases the variation of a positive omitted measure:
its variation is its mass. Combine compact-sector variation convergence
with D18, and restrict the resulting measures to J. Since §2 and §3 give
densities for both full measures, their variation norm on J is exactly
the L1 norm in D2. The proof along every arbitrary sequence h_i->0 proves
the asserted limit. There is no smoothing, no exchange with an unbounded
mark/volume limit, and no reuse of the model Jacobian at finite h.

### Direct global-L1 corollary, with the population unchanged

Put f_h=h^-5 q_h. U with Phi=1 gives
integral f_h=h^-5 I_h(1)->C_U(1)=integral q_0. All densities are nonnegative.
For J=[epsilon,R] inside (0,infinity), split the norm over J and its
complement and use their nonnegative masses. This gives exactly

    ||f_h-q_0||_{L1(0,infinity)}
      <= 2||f_h-q_0||_{L1(J)}
         + |integral f_h-integral q_0|
         + 2 integral_{J^c} q_0.                        (D18a)

First send h to zero at fixed J by D2 and the total-mass limit. Then send
epsilon down to zero and R to infinity; integrability of q_0 makes its
omitted mass vanish. Thus the global norm tends to zero. In particular
neither an atom at zero nor escaping mass at infinity is being inferred
away from local L1 alone: the exact mass equality and limit supply that
control. Actual finite-h partners remain unrestricted as in D1. This
corollary changes neither the candidate bands nor the population, gives no
rate, and asserts no joint-mark or varying-band convergence.

## 7. Optional occurrence-conditioned lifetime consequence

This paragraph additionally consumes O's conditional excess estimate,
not a new proof of it. Let N_h count selected maxima, let m_h be the
unconditional lifetime measure obtained by summing with weight 1/N_h on
N_h>0, and let p_h=P(N_h>0). O (O3),(O4),(O14) imply

    || L^2 eta_h - m_h ||_var
       <= E[(N_h-1)_+]=o(h^5),
    p_h ~ L^2 C_U(1) h^5.                               (D19)

The inequality holds for all bounded measurable lifetime tests, by its
pathwise finite-count proof. Also 0<=m_h<=L^2 eta_h, so m_h and the
field-first conditional lifetime law m_h/p_h have densities. D2,D19 and
the total-mass asymptotic give, on the whole positive lifetime axis,

    density(m_h/p_h) -> q_0/C_U(1) in L1(0,infinity).      (D20)

O's already stated weak mark limit is not itself used to infer this density
limit; the new ingredient is D2. Nothing here gives joint continuous-mark
TV, higher moments, independent occurrences or a Poisson law.

## 8. Scope and falsifiable interfaces

All conclusions retain the exact fixed planar covariance, finite L, fixed
B,K,c_0,C_0, original full W/Z, actual elder mark and once-counted population.
The local proof fixes a positive compact J; its global scalar corollary
uses only the existing same-population total mass. There is no numerical rate or
evaluated cutoff, all-birth/gap exhaustion, varying-L result or global
persistence-coefficient identification. The original weak conclusions and
review histories of U/O remain unchanged, not retroactively enlarged.

Load-bearing new steps are D6's exact affine-k derivative, the diagonal
positive-rescaling application of ELDER E(3), the inverse-count statement D9,
the scalar weighted variation lemma and actual-tail exhaustion D18. Failure
of any of these invalidates D2, even if finite-h AC and formula D3 survive.
In particular spatial remainder convergence cannot be differentiated in r;
the actual global partner cannot be replaced by a merely local saddle;
below-window candidate saddles cannot be dropped from D; and weak convergence
of absolutely continuous measures is not L1 convergence.

Finite exact controls may check the target/scaling/Jacobian ledger and
false-inference examples. They cannot establish the analytic imports,
the global maximin theorem, or the continuum DCT/coarea steps. A fresh
nonauthor whole-proof review, excluding all C99 authors, remains required.
