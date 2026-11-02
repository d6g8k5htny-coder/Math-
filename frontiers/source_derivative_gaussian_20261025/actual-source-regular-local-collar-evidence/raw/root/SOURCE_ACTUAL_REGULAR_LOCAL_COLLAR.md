# SPEC66 — actual regular-point quotient collar

28 October 2026. **Adopted PRECODE66 contract; implementation inactive.**
Root adopted the complete contracts after the completed full draft/design
readings and independent PASS_DESIGN, plus full actual precision-delta and
independent delta review. Those readings and qualified mathematics are
reused. The accompanying adoption record gives the actual UTC.
This adoption creates documents and documentary identities only: no66
source/helper proof text, harness, Lean execution, object, author seat,
external claim, GO, implementation role or timer is authorized. The draft
author and document reviewers are not66 proof authors by this adoption.
Same-family technical credit0; scientific effect NONE.

Read the companion SPEC, PLAN and CONTROLS. Dated local adoption evidence
is retained at `/workspace/scratch/actual-source-regular-local-collar-preflight/REPORT.md`
and under `/workspace/scratch/actual-source-regular-local-collar-source-review/`
in REPORT.md, PRECODE_REVIEW.md and PRECODE_DELTA_REVIEW.md. Actual draft
history and the full precision patch remain in the preflight/precode-drafts
directory. These are retained local evidence locators, not a claim that
their files are already published. Draft-relative REPORT citations are
corrected in these proper documents BEFORE their first identities.
Qualified/published64 and its all-four-CI evidence are reused;65 is active
separate work. Neither is a mathematical66 dependency. These proper66
documents await later normal publication as explicit extras; they are
excluded from65 source/evidence/registry/manifest qualification.

## Exactly one public proposition; no public data

Proposed module: `SourceActualRegularLocalCollar.lean`.
Namespace: `I4SourceActualRegularLocalCollar`.
Sole authored public proposition:
`actualSource_quotient_regular_local_collar`.
No public definitions, data, aliases, instances, fixture library, generic
submersion/chart library, component record or global instances. All actual
implementation and fixture declarations are private and inventoried.

The exact original objects are:

| Notation | Literal object |
| --- | --- |
| L,hL | Original real L and hL : 0<L |
| omega | I4SmoothCarrier.SmoothSample 2 L |
| E2 | UniversalLaw.Spec.Lifetime.E 2, the physical Euclidean carrier |
| Q | I4LifetimeField.coordinates 2 : E2 ≃L[ℝ] (Fin 2 → ℝ) |
| g | I4LifetimeField.actualField 2 L omega |
| Torus | I4Torus.SourceTorus 2 L, the existing product AddCircle torus |
| F | SourceActualFoldTorus.actualTorusField hL.ne' omega |
| Pi(Y) | I4Torus.torusProjection 2 L (Q Y) |
| X,q,c | Actual X:E2, q=Pi(X), c=F(q)=g(X) |
| Point2 | Fin 2 → ℝ with its existing Pi/max norm |

Besides hL and the original sample/point, the only point input is the
actual condition `fderiv ℝ g X ≠ 0`. No global hm/IsMorseDistinct, actual
criticality, inertia, chosen nonzero partial, supplied derivative inverse,
chart, desired PC, flow, component or event certificate is an input.

## Exact conclusion and quantifier order

For every ambient O⊆Torus with IsOpen O and q∈O, derive one real rho>0 and
one OpenPartialHomeomorph phi from Torus to Point2 satisfying:

1. q∈phi.source, phi(q)=0, phi.source⊆O, and
   phi.target = Metric.ball (0:Point2) rho **exactly**.
2. For every z∈phi.source, the actual same-sample height identity is

       F(z)=c+phi(z)(1).

3. For this **same phi and rho**, for every real epsilon with
   |epsilon|<rho, both actual sets

       phi.source ∩ {z : c+epsilon ≤ F(z)},
       phi.source ∩ {z : F(z)=c+epsilon}

   are IsPathConnected.

IsPathConnected includes nonemptiness and implies connectedness of each
level slice. The closed cut is literally ≤, including equality at its
boundary. The cut/slice is restricted to the open chart source; no whole-
torus closedness of that trace is asserted. Negative epsilon values are
included. The level slice is local, not the entire level set of F.

The order is fixed: actual original inputs, then **every O**, then **one
rho and phi**, structural outputs, then **every |epsilon|<rho**. There is
no new chart, source or radius per epsilon, sign, cut or slice. All outputs
refer to that one original field, period, sample, center and quotient
carrier. The final public type expands these objects through existing
names or transparent bound lets; no private alias leaks into it.

No C1 torus-atlas output or Pi/physical-Euclidean norm isometry is proposed.
The chart is topological, derived from the actual physical IFT. A closed-
sublevel package, generic product collar record and component-map theorem
are unnecessary additional public surface for this leaf.

## Old public mathematical dependencies only

There is **no mathematical dependency on 64 or 65**. Neither qualified
64's public endpoint nor active 65 work is needed to implement 66.
Qualified 60–63 are reused context for the roadmap, but none of their
private bodies, fixtures or control binaries is an input. In particular:
60's critical quadratic model cannot be instantiated at a regular point;
61 does not expose a single chart for nearby cuts; 62 concerns an entirely
regular whole-torus closed band; 63 already supplies all-level component
finiteness. Re-proving those endpoints is outside this unit.

The old public source/API inventory is retained in `/workspace/scratch/actual-source-regular-local-collar-preflight/REPORT.md`:

- `inputs/SourceLifetimeGeometry.lean`: actual coordinate equivalence,
  original actual field, and `actualField_smooth` for positive L.
- `SourceActualFoldTorus.lean`: the actual descended field, its exact
  pullback, and the open/continuous/surjective original projection.
- Old public positive-order
  `ContDiffAt.toOpenPartialHomeomorph`, its forward-function equality,
  and basepoint source/target membership facts.
- `AddCircle.openPartialHomeomorphCoe` and finite
  `OpenPartialHomeomorph.pi` on this exact product carrier; actual physical
  coordinate homeomorphism, composition and open restriction/inversion.
- Old public convex/path-connected set and continuous-image APIs for the
  elementary Point2 traces.
- Old public finite-source conversion/shift/zero-sample interfaces for
  genuine owned controls, as specified in CONTROLS.

Root and the eventual producer freeze the exact needed import list and
complete context before any source/helper text. No umbrella Mathlib,
global manifold/ODE/Flow engine, foreign-private/generated declaration or
new normal-form proof is needed. No further API campaign is authorized by
these drafts.

## Actual finite2 physical construction

The scalar condition is used internally, not replaced by a desired
invertibility premise. In Pi coordinates let x=Q X and f(y)=g(Q.symm y).
Its actual derivative d at x is nonzero. Put a=d(1,0), b=d(0,1). The finite
basis implies a≠0 or b≠0. Height is always output coordinate 1.

If a≠0, use the actual augmentation

    A(y)=(y1-x1, f(y)-c).

Its derivative sends (v0,v1) to (v1,a*v0+b*v1); the explicit inverse is
(w0,w1)↦((w1-b*w0)/a,w0). Otherwise b≠0, use

    A(y)=(y0-x0, f(y)-c),

with derivative (v0,v1)↦(v0,a*v0+b*v1) and inverse
(w0,w1)↦(w0,(w1-a*w0)/b). These are genuine continuous linear equivalences,
composed with Q for the physical derivative. Their actual inverse laws,
continuity and HasFDerivAt equality are proved privately.

Specialize actualField_smooth at positive order 1. Its composition with Q
and the retained affine coordinate give the required actual ContDiffAt
of the physical augmented map. The old public IFT consumes this actual
HasFDerivAt with the derived continuous linear equivalence and nonzero
smoothness order. It returns a physical chart centered at X with actual
height g=c+coordinate 1. No supplied inverse, Hessian or hm is introduced.

For each coordinate of x use the injective old quotient chart on
(xi-L/2,xi+L/2). Its finite product, with Q, is a local quotient map whose
forward function is Pi. Compose its inverse with the physical chart.
Positive L supplies the required local Fact/discreteness bindings; these
are derived internally, not new public assumptions.

Restrict the quotient chart to O. Choose a centered positive ball inside
its open target containing 0, restrict the **inverse** to that ball and
invert. This makes the target exactly that ball and source contained in O.
Retain every source/target membership and inverse law. No global continuous
fundamental representative or arbitrary image shrinking is a substitute.

For |epsilon|<rho, the target ball is the literal Pi box. Its intersections
with u1≥epsilon and u1=epsilon are convex and contain (0,epsilon). Map
these two nonempty PC sets by the same actual inverse chart. Exact height
and inverse equations identify their images with the two actual traces.
No further shrinking or chart reselection occurs.

## Controls and authority boundary

CONTROLS fixes the actual original period-2 field
cos(pi*x)+2*cos(pi*y), the two regular partial cases, seam lift, small O,
and equality slices for epsilon=0,±rho/2 with distinct actual inverse
points. The sole mutation omits only derivative≠0 and applies the unchanged
conclusions to the same sample at its actual maximum. Its independent
counterproof uses the actual global bound F≤3 and inverse(0,rho/2), a
nonempty source point forced above 3 by the linear-height identity.

No desired chart becomes a public input. The source/target properties in
that counterproof are outputs of the falsely weakened existence claim,
not a surrogate premise for the true production theorem. Ordinary Controls
must pass independently before one importing False assertion. Ordinary
Controls alone exposes a named closed mutation Prop and its proved negation
publicly, solely for that importing negative; these are not production
public declarations or frontier targets. Its strict PASS and a separate
exhaustive ALL-owned/private/data/generated/foreign-generated standard3
inventory PASS precede the negative. The negative is a CLOSED assertion of
the mutation, with no assumed mutation/hypothesis/axiom/parameter. Freeze
its exact FIRST identity and pre-run snapshot before its single invocation.
There is no ordinary named kernel and exactly one final complete production
kernel. All complete actual controls and custody context freeze before any
future code, and the first documentary worker/outer invocation entry is
preserved from the FIRST important invocation, not the first success.

This leaf can supply regular pieces of a later finite critical-level
cover. Qualified/published 64 (all four CI checks reused) and active 65
remain a separate critical-cover roadmap, with no 66 dependency. Uniform
adjacency/overlap persistence, clearance, lower compact clopen separation,
actual critical-event component inclusions, maximum/minimum event leaves,
global saddle mergers, exhaustive elder/H0/once counts, Borel counts,
Rice/PairLaw and Parent remain OPEN. No actual global two-arms merger or
canonical component labeling follows from this local submersion chart.

Workspace AGENTS requires reuse of completed applicable verification and
accepted mathematics. A new agent/session/head/freeze/handoff/process is
not a recheck reason. Provider-distinct process remains separate. Root
alone owns shared metadata/config/cache, Git/sourcecuts/registration,
external actions, publication and one eligible new own-object placement.
Delivery does not establish recipient reading, qualification or authority.
