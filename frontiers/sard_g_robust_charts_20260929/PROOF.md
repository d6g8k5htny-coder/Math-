# SARD-G robust charts: a source-level A1/A5/A6 successor

Object: OA-SARD-ROBUST-CHARTS-20260929-v1.
Author: OpenAI / ChatGPT, 29 September 2026.
Disposition: AUTHOR-SIDE INTERFACE REPAIR; source-bound nonauthor review required.
Scientific effect NONE. The original manuscript, AMEND reviews, STATUS, graph,
lemma flags and prizes are unchanged. This note is not a C103 regional certificate.

## 1. The downstream defect and the precise replacement contract

The strict-gradient successor SG, at main commit a1fc9581, correctly excludes
hidden critical points and equality at the gradient margin. Its Conditions 2–3
still allow an endpoint hit of a finite closed section. The boundary review BR
shows that such a field can belong to a purported chart while arbitrarily close
fields do not. Thus A1's openness assertion fails for that written predicate and
A6 cannot apply its open-interval slicing to it. Harper's standalone RI note
identifies the missing geometric conditions but explicitly does not amend SG.

This is an explicit alternative chart definition and its associated slicing
proof, not another suggestion to amend the predicate later. It replaces SG
Section 3's chart/first-hit definition, Section 6's countable-direction choice,
and Sections 7–8's application to those charts. It does not rewrite SG Sections
4–5 or claim a new verification of their endpoint-support and RKHS-injectivity
arguments. All source identities are in SOURCE_MAP.json.

The repaired claims are:

**R1 (robust first contact).** A finite arc whose FIRST CONTACT with the CLOSED
section is transverse, in its relative interior, after launch and before its
terminal parameter, with positive compact open-tube clearance, has a continuous
first-hit map under C1 arc perturbations. If the parameter-to-arc map is C1,
its hit parameter and hit point are C1 as well.

**R2 (chart contract, A1).** Under the local-branch continuity premise A2-T below,
the actual chart sets U_chi^rob defined in Section 4 are open in C2, have a
countable index set, and cover every nondegenerate saddle connection by a zero
of their mismatch. If the branch maps satisfy A2-D, that mismatch is C1.

**R3 (Gaussian directions, A5).** For the C2-valued centered Gaussian field,
rational finite combinations of point evaluations at a fixed countable dense
set supply covariance images dense in its Cameron–Martin space. Normalizing
these gives a countable separating family of Gaussian slicing directions with
an independent residual. Norm separability of the Banach dual is neither used
nor asserted.

**R4 (conditional application, A6).** If A2-D and the original A3–A4 directional
nonvanishing implication hold on the new charts, the charted connection event
is contained in a Borel Gaussian null set. With a separately justified full-
measure generic set this yields the completed-measure almost-sure conclusion.
No statement that every point of a Gaussian shift line is Morse is required.

R1 and R3 are proved here. R2 explicitly uses A2-T; the C1 part and R4 explicitly
use A2-D. The statement is not an independent proof of invariant-manifold
parameter regularity, A3–A4, finite-jet nondegeneracy or any regional Kac–Rice
estimate. In particular an accepted R1 does not, by itself, promote C103.

## 2. Functional setting and the unaltered premises

Let X=C2(T_L^2) with its separable Banach norm. Let mu be the centered Gaussian
law of the same smooth periodized field, Q:X* -> X its covariance operator,
and H its Cameron–Martin Hilbert space, continuously embedded in X. The smooth
sample-path and Gaussian moment assumptions of SG ensure that Q is defined by
Bochner integration and the reproducing identity below applies. This note uses
no special isotropic rotation of a conditioned field.

For each pair of rational nested endpoint boxes and continuation neighborhoods,
retain SG's exact critical-point predicate: the CLOSED outer box contains exactly
one critical point, it lies in the interior continuation neighborhood, its index
is one and its spectral gap is greater than a specified positive rational margin.
The gradient minimum on the compact continuation complement is STRICTLY greater
than its specified positive rational threshold eta. The two outer boxes are
compactly disjoint. Equality is not accepted.

**A2-T, explicit imported topological premise.** Around every field with these
hyperbolic tracked saddles there are open field neighborhoods on which the four
local stable/unstable branch germs have fixed-label embedded C1 parameterizations
on compact intervals, continuously depending on the field in the C1 arc topology.
They represent the full germs near the saddle, not arbitrary selected orbit
pieces. They stay inside their declared endpoint neighborhoods. The regular flow
arcs launched from them depend continuously in C1 on the field on their declared
finite time intervals. Ordinary gradient time may be used; an equivalent
normalized flow is used only on regions with a positive gradient lower bound.

**A2-D, additional differential premise.** On those neighborhoods the local
parameterizations and finite regular flow maps are C1 in the field parameter and
the arc parameter, so the implicit-function derivative for transverse hitting
is defined on X. A2-T alone is not a differentiability theorem. Any regularity
loss at the C2-field/C1-vector-field interface must be resolved in A2's own
review, not hidden inside the first-hit argument.

**A3–A4, imported nonvanishing premise.** At a chart zero corresponding to a
connection, the derivative of the mismatch is a continuous linear functional
on X whose restriction to H is nonzero. The original route uses a curve
contribution plus endpoint-supported terms and positivity of Fourier weights.
The endpoint neighborhoods remain disjoint from the compact interior test arc
in the new charts, so the SUPPORT hypothesis is unchanged. This note records
that compatibility but does not independently discharge that route.

The generic full-measure set of nondegenerate critical points and distinct
critical values is another named input. R4 will state precisely where it is
needed, instead of assuming it for an entire one-dimensional shift line.

## 3. The finite-section first-contact lemma with the missing early-prefix proof

Work in a local Euclidean chart near a nondegenerate closed segment
Sigma=[a,b]. Its boundary relative to the supporting line is the two-point set
{a,b}, not its ambient topological boundary, which would be the whole segment.
Write n for a unit normal, and s for a signed coordinate along the supporting
line. Let T be an open tube in the surface. Suppose a C1 embedded arc gamma on
[0,H] is defined on a slightly larger parameter neighborhood when required by
local differentiation, and satisfies:

(F1) gamma(0) is not in Sigma and the FIRST time tau of contact with the CLOSED
     Sigma exists, with 0<tau<H. No earlier tangent or endpoint contact counts
     as harmless; each is an earlier contact with the closed set.
(F2) gamma(tau) is in relint(Sigma), equivalently its distance to {a,b} is positive.
(F3) gamma([0,tau]) is compactly contained in the OPEN tube T, including launch
     and hit. In a compact ambient surface this gives a positive metric distance
     to T^c. For a closed tube an explicit strict positive boundary clearance
     would instead be required; mere membership in a closed tube is insufficient.
(F4) n.gamma'(tau) is nonzero. This is a local condition at the actual first hit.

One may require positive rational lower margins on tau, H-tau, endpoint distance,
compact tube clearance and the absolute normal derivative, and on regular-flow
speed where it is used. All comparisons must be strict. These quantitative
versions are useful for the countable family but do not change the proof.

**Proof of R1.** Choose epsilon>0 so [tau-epsilon,tau+epsilon] lies in (0,H),
gamma on that interval stays in one supporting-line chart and in T, its tangential
coordinate lies a positive distance from both endpoints, and its normal derivative
has constant sign with absolute value bounded below. Its signed normal values at
tau-epsilon and tau+epsilon therefore have opposite signs with positive slack.

The EARLY PREFIX gamma([0,tau-epsilon]) is compact and disjoint from the CLOSED
segment Sigma. Its distance from Sigma is consequently strictly positive. This
is the step that a phrase such as 'all conditions are strict' does not supply:
the whole travelled arc has zero distance to the section at the hit, so it cannot
be used as a separated prefix. Nor may the closed segment be replaced by relint
in this compact-set argument.

Small C1 perturbations preserve early-prefix separation, endpoint and tube margins,
the normal derivative's sign and lower bound on the terminal interval, and the
opposite signs at its ends. The intermediate-value theorem gives one zero of the
normal coordinate in this interval; strict monotonicity makes it unique. Its
point lies in the relative interior of Sigma. No earlier contact is possible in
the prefix or in the terminal interval before that zero. Thus the continued zero
is still the first CLOSED contact. Later contacts beyond this interval are
irrelevant to this definition. The positive terminal-time slack ensures that the
continued hit is still inside the declared arc domain.

The zero and hit point are continuous under C1 arc perturbations. If gamma is
Gamma(f,t) with C1 parameter dependence, the scalar implicit-function theorem
applies to n.(Gamma(f,t)-a), and

    d tau_f[h] = - n.(D_f Gamma(f,tau_f)[h])
                    / (n.partial_t Gamma(f,tau_f)).          (R1a)

The hit-point derivative follows by the chain rule. This proves R1 and all its
strict-margin variants. The local terminal argument also persists under small
changes of the finite segment endpoints, a fact used for rational approximation
in the coverage proof. Earlier crossings of the SUPPORTING LINE outside Sigma
are allowed; only actual contacts with Sigma are excluded. QED.

## 4. The actual successor predicate, including every local branch label

Fix a countable atlas of local-branch field neighborhoods supplied by A2-T.
Here is why it may be fixed countably without assuming a countable norm-dense
subset of X*: for each choice of rational isolating data, its hyperbolic field
locus is an open subspace of the second-countable space X. The local field
neighborhoods of A2-T form an open cover. A countable subcover exists by Lindelof.
Choose one local-branch chart on each selected neighborhood once and for all,
with a fixed compact parameter interval after shrinking if needed. Products of
the two endpoint atlases and the finite branch labels remain countable.

This is a countable topological atlas, not a computable enumeration of arbitrary
real fields. It is chosen ONCE, not as a measurable 'first chart' depending on a
random realization. Every field is allowed to belong to multiple charts.

A label chi consists of one such atlas index; SG's rational isolating boxes,
continuation neighborhoods, strict spectral/gradient margins; branch signs; all
local closed rational sections; a central closed rational segment Sigma; a
finite rational polygonal open tube covering the compact regular travel arcs;
finite rational positive parameter/time horizons; and positive rational lower
clearances and speed/normal-angle margins. Keep the endpoint-support neighborhoods
disjoint from the compact interior test subarc as required by A3.

Define U_chi^rob to be EXACTLY the set of fields satisfying all of the following:

(P1) The field belongs to the specified local-branch atlas domain and satisfies
     the CLOSED-outer-box uniqueness and STRICT spectral/gradient predicate of
     Section 2 for each tracked saddle.
(P2) EVERY local branch-label section is met by its specified compact local
     germ arc according to (F1)–(F4), with the declared strict margins. The local
     arc parameter is a graph coordinate, not physical time from a stationary
     saddle. It may start at the saddle, which lies OFF the local section.
     There is no positive-flow-speed requirement at that stationary launch.
     Its positive-parameter first section hit defines the regular launch point.
(P3) From these regular launch points, the forward unstable and backward stable
     flow arcs are defined through their declared finite horizons. EACH meets
     the same central CLOSED Sigma by (F1)–(F4), with strict launch/terminal,
     endpoint, open-tube, regular-speed and transverse-normal margins.
(P4) Any other section hit used to specify a branch or mismatch is governed by
     the SAME conditions. It is not enough to repair only the central section.
     Separation of endpoint neighborhoods from the interior test arc is strict.

Later returns after a first hit are immaterial. No predicate based on 'the first
relative-interior hit while ignoring earlier closed-boundary contacts' is used.
No degenerate field is admitted by overriding an invalid local predicate after
slicing has begun. A degeneracy elsewhere on the torus need not invalidate this
local chart, and the new definition does not say otherwise.

On U_chi^rob define the mismatch by the ACTUAL robust first-contact points,

    D_chi(f)=s(z_u(f))-s(z_s(f)),                               (R2a)

where s is the fixed signed coordinate on central Sigma. This definition is not
a post hoc restriction of the old possibly discontinuous hit map.

## 5. Openness and C1 regularity of the defined charts

For P1 the unique saddle continues in a small ball by the nondegenerate-zero
implicit-function theorem. The gradient has a positive minimum on the rest of
the compact outer box outside that ball; small C1 perturbations cannot create a
new zero there. The saddle stays inside its continuation neighborhood and its
index/spectral gap persist under C2 perturbations. On each fixed compact exclusion
set K, |min_K|grad f|-min_K|grad g||<=||grad f-grad g||_infinity, so a STRICT
margin remains strict. No sampled minimum is being substituted for this argument.

A2-T supplies the local arcs continuously in C1. R1 first continues every local
section hit and hence both regular launch points. Continuous finite-time flow
dependence then supplies both travel arcs. Apply R1 again to the central hits.
Compact travel speed and tube-clearance minima are continuous under uniform arc
and C1 vector-field convergence; their strict bounds persist. There are finitely
many conditions per chart, so a sufficiently small C2 ball preserves all of them.
Therefore U_chi^rob is open.

Under A2-D the same applications of (R1a), composition, and the chain rule give
C1 launch points, central hit times/points, and D_chi on U_chi^rob. This C1 conclusion
uses A2-D explicitly; the geometric lemma has not proved invariant-manifold
parameter differentiability. Different overlapping charts need not have identical
mismatch functions away from their connection zeros. The slicing argument only
uses each on its own open domain.

## 6. Countable coverage still includes every genuine connection

Fix a nondegenerate saddle-to-saddle gradient connection. Choose compactly
separated rational isolating boxes with each saddle the only zero in its outer
box. Choose rational continuation neighborhoods and smaller rational spectral and
gradient thresholds. The required strict minima exist by compactness.

Choose atlas neighborhoods containing the field for the corresponding local
germs. On each selected branch, choose a small local section through an interior
point of its regular part, transverse to that branch, lying inside the endpoint
neighborhood. Shrink the segment so the earlier compact local germ prefix avoids
its closure; local monotonicity in a graph coordinate then gives first closed
contact in its relative interior. Extend the local parameter interval a little
past the hit. The same construction applies to every label section required.

The connection's compact regular arc between these launches is embedded: a
repeated point of a nonstationary orbit would be periodic, while f strictly
increases along ascending gradient time. Choose a small central transverse
segment near an interior point. By shrinking it, the two compact earlier travel
prefixes avoid its closure. Their local transverse crossings are of the same
geometric connection, so they hit the central segment at the same point.
Extend both travel arcs a small positive time past that point, away from the
endpoint neighborhoods. An open tubular neighborhood of the compact travelled
arcs has positive clearance, positive regular speed and a central transverse
normal bound. A finite rational polygonal tube may be chosen within it and
around the arcs; a finite coordinate cover handles torus winding.

All these properties have strict slack. The proof of R1, with segment endpoints
as additional finite-dimensional parameters, shows that close rational segment
endpoints preserve them. Hence the initially chosen local and central sections
can be replaced by rational ones. Rational horizons and smaller positive rational
margins complete a label chi. The field lies in U_chi^rob, and its mismatch is zero.
Thus

    Connection intersect Omega_gen
        subset union_chi {f in U_chi^rob:D_chi(f)=0}.           (R2b)

The index set is countable. No realization is asked to select a first chart,
and no measurable-selection or analytic-projection theorem is needed.

## 7. Countable Gaussian directions without a norm-dense Banach dual

Let S={x_n} be a fixed countable dense subset of the torus (rational coordinates
after rescaling by L). Let ell_n be point evaluation at x_n, a continuous linear
functional on X, and k_n=Q ell_n in H. For h in H the covariance/RKHS identity is

    <h,k_n>_H=ell_n(h)=h(x_n).                                  (R3a)

If h is orthogonal to every k_n, it vanishes on S. The embedding H -> C2 implies
continuity, so h vanishes everywhere and is the zero vector. Therefore the real
linear span of {k_n} is dense in H. Rational finite linear combinations are also
dense: approximate finitely many real coefficients by rationals in a fixed finite
sum before approximating h by such sums.

Enumerate all rational finite combinations ell of the ell_n, remove those with
variance v_ell=ell(Qell)=0, and set

    h_ell=Qell/sqrt(v_ell),
    xi_ell=ell(f)/sqrt(v_ell),
    g_ell=f-xi_ell h_ell.                                      (R3b)

The h_ell are dense in the unit sphere of H (or merely a countable separating
family would suffice). This construction needs neither X* norm separability nor
a countable dense family in X*. The old dual-density sentence in SG is replaced,
not treated as an extra unproved assumption.

The scalar xi_ell is standard Gaussian. For any a in X*,

    Cov(a(f),xi_ell)=a(Qell)/sqrt(v_ell)=a(h_ell),
    Cov(a(g_ell),xi_ell)=0.                                    (R3c)

The pair (g_ell,xi_ell) is jointly Gaussian since it is a continuous linear image
of f. The vanishing cross-covariances imply independence. This Banach-valued
independence can be checked on a countable separating family of derivative
point-evaluations and then extended to the Borel sigma algebra. Indeed C2 norm
balls are generated by derivative evaluations of orders at most two on S using
suprema on the countable dense set. No probability measure on a nonseparable
norm-dual is introduced.

Because H embeds continuously in X, D_chi'(f)|_H is continuous. If it is nonzero,
it cannot vanish on the dense h_ell family. Thus at every charted connection
satisfying the A3–A4 premise, at least one direction has

    D_chi'(f)[h_ell] != 0.                                     (R3d)

This proves the needed A5 direction/decomposition statement for the new source.
It does not prove A3–A4's nonvanishing premise.

## 8. A6 applied to these charts, not to an uncorrected predecessor

Assume A2-D and the A3–A4 premise. For each fixed chi and ell define

    B_chi,ell={f in U_chi^rob:D_chi(f)=0,
                              D_chi'(f)[h_ell]!=0}.            (R4a)

This is Borel: U_chi^rob is open, and both scalar functions are continuous there.
Fix a residual g in (R3b). The validity set

    I_g={t in R:g+t h_ell in U_chi^rob}

is open and is a countable disjoint union of open intervals. On each interval
F_g(t)=D_chi(g+t h_ell) is C1. At every zero contributing to B_chi,ell, F_g'(t) is
nonzero. The scalar inverse/implicit-function theorem makes that zero isolated
among the zeros in its interval. Such a subset of R is countable: each point can
be assigned a rational-endpoint isolating interval containing no other zero.
Accumulation at singular zeros or at interval boundaries is allowed and does
not destroy this countability argument.

The conditional scalar law is standard Gaussian, by the INDEPENDENT residual
construction, so it charges that countable set with probability zero for every
fixed g. The inverse image of (R4a) under (g,t)->g+t h_ell is Borel, so Tonelli
applies to the residual law times the scalar Gaussian law. Hence mu(B_chi,ell)=0.
By (R2b) and (R3d),

    Connection intersect Omega_gen subset union_chi,ell B_chi,ell.

The union is countable and Borel null. If the connection event itself has not
separately been proved Borel, its immediate conclusion is outer measure zero,
and it is measurable and null in the completed Gaussian probability space.
With the separate assumption mu(Omega_gen)=1 this gives the conditional almost-
sure conclusion. Fields outside Omega_gen along a shift line are not assumed
absent; only the open validity intervals and their regular zeros are used.

This completes A6's application to the actual successor predicate, CONDITIONAL
on the inputs explicitly stated above. The full C103 or any downstream regional
estimate still requires its own premise and review chain.

## 9. Boundary examples that the new predicate actually excludes

The BR torus example is F(x,y)=sin(2pi x)(2-cos(2pi y)). Its two saddles on y=0
are connected; central Sigma={(1,y):0<=y<=1/200} is first hit at its lower endpoint.
All the old strict speed, gradient and angle margins can hold. Vertical field
translation moves the branch below the segment. The new P3 excludes the unshifted
field because F2 fails. This does not exclude the connection from the UNION of
new charts: a central segment with endpoints on opposite sides of the hit and
smaller positive margins supplies a valid chart.

Simply replacing the closed segment by its relative interior is not enough.
For a concrete smooth embedded arc on 0<=t<=5/2, use

    gamma_eps(t)=((t-1)(t-2),(t-1)^2+eps),
    Sigma={(0,y):0<=y<=2}.

At eps=0 there is a transverse endpoint contact at t=1 and an interior contact
at t=2. A rule that ignores the first contact and asks only for the first INTERIOR
hit chooses t=2. For every small positive eps it chooses t=1 instead. The arcs
converge in C1, yet that rule is discontinuous. Our F1 sees the earlier closed
contact and F2 rejects its endpoint at eps=0. This is a geometric first-hit
counterexample, not a newly asserted gradient connection on the torus.

The launch and terminal slacks are independently necessary. On gamma(t)=(t-1,1/2)
for 0<=t<=1, the hit is transverse and interior but at terminal time; shifting
x slightly negative makes it miss the section on that domain. An arc starting
on the section has first contact at zero and is likewise excluded. Compact tube
clearance must include the whole prefix, not merely its hit: a path can leave a
tube and return before a good transverse hit. Every local label is checked, since
a discontinuous local launch would invalidate even a well-behaved central hit.

## 10. What the finite controls can and cannot establish

The standard-library program tests rational piecewise-affine paths against a
closed vertical segment and an open rectangular tube. It certifies only that
finite model and is deliberately stricter at polyline corners than the smooth
lemma: its transverse hit must lie inside one affine piece. It neither samples
an ODE nor certifies arbitrary fields' gradient minima, stable manifolds or
infinite-dimensional chart membership.

Tests exercise the real endpoint/earlier-contact/terminal/tube/local-label
failures, strict scalar gradient margins, rational moving-hit models, the smooth
polynomial first-interior counterexample, exact finite Gaussian covariance
splitting, finite evaluation rank, and exclusion of singular slicing zeros.
Semantic mutants independently remove each important condition. The tests do
not substitute for R1's compact-prefix argument, the infinite-dimensional RKHS
density proof, A2 regularity or the Tonelli measurability argument.

The current proof is an additive source-level alternative. Independent review
must decide the R1/R2/R3/R4 claims at their exact dependency scope. Publishing it,
passing its tests or merging it as a candidate does not flip the predecessor's
AMEND, assert an independently closed A2–A4 chain, or promote C103.
