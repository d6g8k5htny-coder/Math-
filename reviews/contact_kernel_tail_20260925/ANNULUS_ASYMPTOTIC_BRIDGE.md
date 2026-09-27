# From fixed transverse charts to an entire fixed annulus: a source-explicit bridge

**Object:** OA-ANNULUS-TYPED-BRIDGE-20260925-v1. **Author:** OpenAI / ChatGPT.
**Disposition:** the analytic gluing lemma below is proved from its stated hypotheses.
Its Gaussian application remains CONDITIONAL on the independently reviewed validity
of the exact PR22 and PR25 interfaces. No source status or legacy gate is closed.

## 1. Avoid duplicate work; identify the two existing inputs

**Local typed asymptotic, PR25:** source
`ad35e46d15c2815c36746442808a1626a9724e8a`,
`reviews/collision_mechanism_20260925/NOTE.md`, Section C.
For every fixed eta>0 on the d2 compact transverse chart, the candidate gives a
rescaled height-window mean-density convergence to Lambda_j, with Lambda_1>0
and Lambda_0=Lambda_2=0. This is stronger than PR16's upper bound and is NOT
covered by a review accepting only PR16.

**Quantified whole-annulus domination, PR22:** source
`2804dc1db27ef3b1fdef6bb350b486162692cc4a`,
`frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md`,
17646 bytes, SHA256
`1fd9fe7141e464fd1c09ebf0318d8a701729c9c61ea24f73f7e20a9cf10c552b`.
This candidate already covers the height-restricted count on an entire fixed scaled
annulus. Its extra-conditioned moment and inner two-scale arguments remain review
interfaces. This note does not duplicate or overwrite that proof.

Both use the same exact normalized periodized field, six original endpoint pins,
full endpoint-only typed determinant normalizer Z_r, frame, height convention,
and compact birth/strictly-positive-gap parameters. Their invertible observation
transforms have different formulas but condition on the SAME six original data.
No extra original-pin Jacobian enters either conditional-law normalizer.

## 2. Normalize the density correctly

Fix K={(u,v): A0<=sqrt(u^2+v^2)<=B0}, 1<A0<B0<infinity.
Write rho_(r,j)^W(X) for the height-window intensity per PHYSICAL area, and define

    F_(r,j)(u,v)=r^-1 rho_(r,j)^W(r u,r v).

Then

    E_Qr^W N_j(rE)=r^3 integral_E F_(r,j)(y)dy.           (2.1)

The r^-1 here is essential: spatial area contributes r^2. It is not r^-3 times
the physical-area intensity. All intensities refer to the open interval
b-k*r^3<f<b. The inner estimate below may use an all-height upper bound, but the
conclusion is height-restricted.

## 3. Exact hypotheses for the gluing lemma

Assume nonnegative measurable densities F_r on K and a nonnegative continuous
Lambda off the axis, uniformly over a fixed compact parameter space.

H1. For every eta>0,

    esssup_(K intersect {|v|>=eta}) |F_r-Lambda| -> 0.

H2. There are epsilon0,c,C>0 and h_r=r^(1/24) such that for small r,

    F_r <= C |v|^-96 exp(-c/v^2), h_r<=|v|<=epsilon0.

H3. On |v|<h_r,

    F_r <= C r^-14 exp[-c/(2r^(1/12))].

H4. The proposed contact kernel satisfies a uniform vanishing envelope,

    Lambda <= C |v|^-13 exp(-c/v^2), 0<|v|<=epsilon0.

The constants can differ between H2–H4; use their minimum/maximum as necessary.
The inequalities can be understood for chosen Kac-Rice representatives or almost
everywhere. Set Lambda(u,0)=0. H4 makes this a continuous extension.

The exponents in H2 and H3 are deliberately copied from PR22, not optimized:
its outer PHYSICAL intensity is <=C*k*r*|v|^-96 exp(-c/v^2), while its inner
all-height PHYSICAL intensity is <=C*r^-13 exp[-c/(2r^(1/12))]. Compact k ranges
allow k to be absorbed here. H4 is the new limiting-kernel bound in the companion note.

## 4. Gluing theorem and proof

Under H1–H4,

    esssup_K |F_r-Lambda| -> 0.                          (4.1)

Proof. Let epsilon>0. Since both angular envelopes vanish at the origin, choose
eta in(0,epsilon0) so that their suprema over0<|v|<=eta are <epsilon. For small r,
h_r<eta. Split K into three regions.

- |v|>=eta: H1 bounds the difference by epsilon for sufficiently small r.
- h_r<=|v|<eta: H2 and H4 bound the absolute difference by2epsilon.
- |v|<h_r: H3 tends to zero faster than any power of r, and H4 bounds Lambda by
  epsilon; the difference is <2epsilon for sufficiently small r.

This proves(4.1), uniformly over the declared compact parameter space. No substitution
of eta(r) into unspecified fixed-chart constants occurs: the cutoff-region bounds
H2/H3 are explicit inputs. No convergence-rate claim is extracted from qualitative H1.

The much weaker condition sup F_r<=C and finite measure K would suffice for total
variation via a fixed-eta strip split. Here the stronger available bounds yield
uniform density convergence as well. Axis and fixed boundary curves have zero
expected counts by absolute continuity; a density representative at the axis
is immaterial to the expected-count statement.

## 5. Conditional Gaussian conclusion

If the PR25 local asymptotic and PR22 quantified bounds survive their separate
analytic reviews, apply the lemma to each index j. For all Borel E subset K,
including r-dependent E_r,

    |E_Qr^W N_j(rE)-r^3 integral_E Lambda_j(y)dy|
        <= epsilon(r) r^3 area(E), epsilon(r)->0.         (5.1)

On the FULL fixed annulus the limiting kernel has

    Lambda_1>0 off the axis, Lambda_1=0 on the axis,
    Lambda_0=Lambda_2=0 everywhere.

Consequently, for the whole annulus or any fixed positive-area Borel subset,

    E_Qr^W N_1(rE) ~ r^3 C_E, C_E=integral_E Lambda_1>0,
    E_Qr^W[N_0(rE)+N_2(rE)] = o(r^3).                   (5.2)

There is NO uniform positive lower bound for Lambda_1 over the whole annulus,
since it vanishes on the axis. The upper-bound uniformity over arbitrary Borel
sets does not imply a single positive lower constant times area(E) for every E.
That would fail for sets concentrating near the axis.

This upgrades a fixed-annulus upper bound to a candidate saddle-resolved leading
law, but ONLY through the named interfaces. It is not an independent proof of
those inputs, an elder-defect lower bound, or a probability lower bound.

## 6. An explicit belt-truncation error decomposition

For any fixed eta<epsilon0 and r with h_r<eta, define

    e_eta(r)=esssup_(|v|>=eta)|F_r-Lambda|,
    A_eta=sup_(0<|v|<=eta) C |v|^-96 exp(-c/v^2),
    B_eta=sup_(0<|v|<=eta) C |v|^-13 exp(-c/v^2),
    I(r)=C r^-14 exp[-c/(2r^(1/12))].

Then esssup|F_r-Lambda| is at most

    max{e_eta(r), A_eta+B_eta, I(r)+B_eta}.              (6.1)

For integrated coefficients, use the exact gamma tail in the companion note to
replace B_eta by an explicit integral bound. This isolates three computations:
fixed-angle approximation, outer angular tail, and inner two-scale remainder.
No error is hidden in an unnamed shrinking-chart constant.

## 7. Architecture and review contract

The synthesis record must retain dependency edges to BOTH source identities.
An ACCEPT review of PR16's O(r^3) fixed-angle upper bound cannot be used as
acceptance of PR25's positive leading kernel or PR22's shrinking-cutoff estimates.

Reviewer assignments should therefore be disjoint:
- existing PR26 reviewer: finish its already-assigned PR22 fixed-annulus review;
  PR25 B–C review is queued next, not a preemption;
- existing PR27 reviewer: independently audit TWO_SCALE_ADDENDUM S6–S21;
- a separate reviewer, once available: check this gluing proof and the kernel
  tail/small-gap algebra; no author self-acceptance.

Current provider identities are reviewer-declared, not independently attested by
the coordinator. A bot acknowledgment is not a finished review. Codex's reported
review-usage limit and disabled Bugbot are not circumvented by alternate launches.

Still outside scope: growing outer radius, r<<distance<<rho, pin neighborhoods,
witness-witness collisions, dimension>=3, kmin->0 at finite r, uniform-L limits,
full persistence-pair selection, evaluated numerical24-jet constants.
