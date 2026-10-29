# Stage66 complete literal context001 — pending root FULL acceptance

Creator6482857252, actual native22:57:35UTC28Oct2026; root initial context-only
GO observed22:59:17.678739. Proper SPEC/PLAN/CONTROLS/CONTENDERS were normally
published in263b9d4329043e6debd299a8c27327ee515670d7 BEFORE this context.
Producer `/root/regular_collar_prospective` personally FULL-read the ten
required adopted/design/delta documents at22:40:10; that onboarding is
separate from this effective complete-context freeze and later acceptance.

This document freezes literal intended declarations and their ownership.
Its Lean fences are TYPE/DEFINITION CONTRACTS for later review, NOT executed
or elaborated code, proof candidates, fixture implementations, ordinary
proof bodies or a False harness. There is no `sorry`, axiom, hidden assumed
proof or certificate premise. The only source-like file created so far is
the imports/open/namespace-only INITIAL_SOURCE_COMMON.lean.txt. No module
SourceActualRegularLocalCollar.lean, fixture implementation, ordinary source,
harness, Lean/probe/check, object or proof-helper candidate exists by this
context-only bootstrap. All typed joins listed below remain unelaborated.

Root must personally FULL-read and accept this ENTIRE effective document,
including all actual positive and ordinary/negative contracts, before
separate applicable TEXT release. The optional ONE complete physical TEXT
helper must personally FULL-ACK that same accepted context before its own
explicit release. No helper source/candidate is authorized by delivery.

## 1. Literal imports, opens, instances and source ownership

The initial header contains exactly:

```lean
import SourceActualFoldTorus
import SourceFiniteTrig
import SourceSmoothConditionalKernel
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Topology.OpenPartialHomeomorph.Constructions
import Mathlib.Topology.OpenPartialHomeomorph.IsImage
import Mathlib.Topology.Instances.AddCircle.Defs
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Calculus.FDeriv.Pi
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

noncomputable section
set_option autoImplicit false
open Set Filter
open scoped BigOperators
open UniversalLaw.Spec.Lifetime I4SmoothCarrier I4LifetimeField

namespace I4SourceActualRegularLocalCollar
```

No import64/65, umbrella Mathlib, C1 manifold/ODE/flow engine, foreign private
or generated declaration. SourceActualFoldTorus supplies only its qualified
PUBLIC actual quotient/projection interfaces. SourceFiniteTrig supplies the
PUBLIC original finite-source construction; SourceSmoothConditionalKernel
supplies PUBLIC zeroSample. No prior private60–65 body, fixture or ordinary
binary is a dependency or copy source. Narrow public interface blocks were
read to pin the context; this was not a new verification/API campaign.

Existing instances on `E 2`, `Fin 2 → ℝ` and product AddCircle are inferred
from those imports. Positive period needs only LOCAL bindings, introduced
inside quotient construction, with literal proposition `Fact (0 < L)` and
`DiscreteTopology (AddSubgroup.zmultiples L)` (the existing additive subgroup
notation may print `zmultiples L`). These are derived from hL and the old
public real-period instance; no global instance or extra public premise.
The exact instance elaboration remains a producer typed obligation.

All new declarations except the sole production theorem are PRIVATE,
including common aliases, intermediate maps, local charts, geometry,
actual fixture definitions/consumers and generated helpers. Exhaustive
module-index ownership includes generated declarations and any declaration
outside the main namespace; lexical privacy is not the inventory rule.

## 2. Literal common objects and coordinate convention

The following prospective private common definitions fix names/directions;
they are transparent conveniences inside the new module, never public inputs:

```lean
private abbrev Point2 := Fin 2 → ℝ
private abbrev E2 := UniversalLaw.Spec.Lifetime.E 2
private abbrev Torus2 (L : ℝ) := I4Torus.SourceTorus 2 L

private def Q : E2 ≃L[ℝ] Point2 := I4LifetimeField.coordinates 2
private def cover (L : ℝ) (Y : E2) : Torus2 L :=
  I4Torus.torusProjection 2 L (Q Y)
private def actualG (L : ℝ) (ω : I4SmoothCarrier.SmoothSample 2 L) : E2 → ℝ :=
  I4LifetimeField.actualField 2 L ω
private def actualF {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L) : Torus2 L → ℝ :=
  SourceActualFoldTorus.actualTorusField hL.ne' ω
private def coordField (L : ℝ) (ω : I4SmoothCarrier.SmoothSample 2 L)
    (y : Point2) : ℝ := actualG L ω (Q.symm y)
private def physicalBasis0 : E2 := Q.symm ![1, 0]
private def physicalBasis1 : E2 := Q.symm ![0, 1]
private def smallO (L : ℝ) (X : E2) : Set (Torus2 L) :=
  cover L '' Metric.ball X (1 / 8 : ℝ)
```

Here E2 has its PHYSICAL Euclidean norm; Point2 has its existing Pi/MAX
norm. Q is an actual continuous-linear equivalence, not a norm isometry.
`cover L X` is q, and c is the SAME original actual height
`actualG L ω X = actualF hL ω (cover L X)`. The exact equality comes from
PUBLIC actualTorusField_pullback and the literal definition of actualField,
not a newly chosen field or a polynomial replacement.

Public dependencies fixed for the producer/helper:

- `I4LifetimeField.coordinates 2` and its actual inverse.
- `I4LifetimeField.actualField_smooth 2 hL ω : IsSmooth 2 (...)`, specialized
  at the finite order1; no order0 IFT application.
- `SourceActualFoldTorus.actualTorusField`, actualTorusField_pullback,
  torusProjection2L_continuous/open/surjective.
- `ContDiffAt.toOpenPartialHomeomorph`, its coe equality,
  mem_toOpenPartialHomeomorph_source and image_mem_toOpenPartialHomeomorph_target.
- `AddCircle.openPartialHomeomorphCoe L a`, finite
  `OpenPartialHomeomorph.pi`, composition/symm/restrOpen and existing
  continuous-linear-equivalence-to-homeomorph interfaces.
- Existing convex/nonempty path-connectivity and continuous-image APIs.

No old strict/inventory/kernel/control/CI/source/object digest is repeated
to establish these carried eligible interfaces.

## 3. Optional ONE complete PRIVATE physical-adapter interface

This is the ENTIRE possible proof-TEXT helper assignment. It has no supplied
chart, chosen partial, derivative inverse, hm, inertia or desired conclusion
as a premise. Exact final private interface:

```lean
private theorem actual_physical_submersion_chart
    {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L) (X : E2)
    (hreg : fderiv ℝ (I4LifetimeField.actualField 2 L ω) X ≠ 0) :
    ∃ e : OpenPartialHomeomorph E2 Point2,
      X ∈ e.source ∧ e X = 0 ∧ (0 : Point2) ∈ e.target ∧
      ∀ Y ∈ e.source,
        I4LifetimeField.actualField 2 L ω Y =
          I4LifetimeField.actualField 2 L ω X + e Y 1
```

The optional complete section must itself prove all private finite-coordinate,
continuous-linear inverse, actual derivative, regularity and positive-order
IFT joins needed for this result. It returns a physical chart only; it does
not author quotient restrictions, finite geometry, public assembly, actual
fixtures, ordinary controls, counterproof, False harness or execution.

For exact formulas set x=Q X, f=coordField L ω,
`d = fderiv ℝ f x`, `a = d ![1,0]`, `b = d ![0,1]`.
Derive d≠0 from hreg via the actual Q/Q.symm derivative rules. Every
`v : Point2` satisfies `d v = a * v 0 + b * v 1`; hence a≠0 or b≠0.
These facts are internally proved, never new public assumptions.

If a≠0, the literal augmented Pi map and its derivative/inverse are:

```text
A(y)       = ![y 1 - x 1, f y - f x]
DA(v)      = ![v 1, a * v 0 + b * v 1]
DAinv(w)   = ![(w 1 - b * w 0) / a, w 0].
```

Otherwise b≠0, and:

```text
A(y)       = ![y 0 - x 0, f y - f x]
DA(v)      = ![v 0, a * v 0 + b * v 1]
DAinv(w)   = ![w 0, (w 1 - a * w 0) / b].
```

Both branches put ACTUAL HEIGHT in target coordinate1, with coefficient1.
The genuine physical augmented map is `fun Y : E2 => A (Q Y)`; its actual
invertible derivative is the derived finite2 equivalence composed with Q.
Prove both inverse laws, linearity and continuity; finite dimensionality
does not excuse an absent actual equivalence or derivative equality.

The old public IFT's exact input shape is:

```lean
ContDiffAt.toOpenPartialHomeomorph
  (f : E → F) (hf : ContDiffAt ℝ n f a)
  (hf' : HasFDerivAt f (f' : E →L[ℝ] F) a) (hn : n ≠ 0)
```

Here `f' : E ≃L[ℝ] F` is the ACTUAL derived derivative equivalence, not an
assumed invertibility certificate, and n=1. The precise elaborated calling
syntax must follow the qualified PUBLIC declaration; this displayed order
records its logical parameters. The returned forward map is the actual
augmented function, maps X to zero, includes X in source and zero in target,
and gives the exact actual height equation above on its source.

Helper executions/probes/builds/checks/hashes/objects/kernel/inventory/
ordinary/Git/cache/shared/external actions are ZERO. Before ANY candidate:
root FULL accepts this complete context, helper personally FULL ACKs it,
then root separately releases TEXT. Freeze the complete helper original,
literal imports/context/provenance/ACK with actual observed UTC BEFORE
producer FIRST IDs and ONE integration. Preserve every later actual full
amendment patch and version. No regenerated replacement original, helper
object, second hidden proof author or separate target/kernel lineage.

## 4. Producer-owned quotient/O/exact-ball interfaces

The producer owns the entire quotient construction, including its private
lemmas. Its final structural result is literally:

```lean
private theorem actual_quotient_regular_chart
    {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L) (X : E2)
    (hreg : fderiv ℝ (I4LifetimeField.actualField 2 L ω) X ≠ 0)
    (O : Set (Torus2 L)) (hO : IsOpen O) (hXO : cover L X ∈ O) :
    ∃ ρ : ℝ, 0 < ρ ∧
      ∃ φ : OpenPartialHomeomorph (Torus2 L) Point2,
        cover L X ∈ φ.source ∧ φ (cover L X) = 0 ∧
        φ.source ⊆ O ∧ φ.target = Metric.ball (0 : Point2) ρ ∧
        ∀ z ∈ φ.source,
          actualF hL ω z = actualF hL ω (cover L X) + φ z 1
```

The construction takes the actual physical chart result; no corresponding
physical chart is an input of the public theorem. For each i use the
PUBLIC AddCircle chart with a=(Q X)i-L/2, source `(a,a+L)`, hence containing
(Q X)i because hL>0. Its finite product forward function is the literal
period-L projection. Compose with Q's actual homeomorphism to obtain the
physical-to-quotient local chart, and compose its inverse with the actual
physical submersion chart. Track X/q and every genuine source/target through
composition. No global fundamental representative or branch cut at the seam.

Restrict the quotient-to-Pi chart to O by `restrOpen O hO`; zero belongs to
its genuine open target. Choose ρ>0 with the centered Pi ball contained in
that target. Restrict the INVERSE to that ball using its openness, then
invert. This makes the final target EXACTLY that ball and preserves source
inside O, center and actual height. A bare open-target neighborhood or
arbitrary source shrink is not the exact-target conclusion.

The first physical milestone and then exact quotient/O/ball milestone are
individually reviewable. If an exact typed join fails, report that join;
do not add certificate premises or expand to a C1 atlas/relative flow.

## 5. Producer-owned same-chart target geometry

Complete private geometry interfaces, valid on the actual Pi norm:

```lean
private theorem pi_closed_upper_trace_pc
    (ρ ε : ℝ) (hρ : 0 < ρ) (hε : |ε| < ρ) :
    IsPathConnected ((Metric.ball (0 : Point2) ρ) ∩ {u | ε ≤ u 1})

private theorem pi_level_trace_pc
    (ρ ε : ℝ) (hρ : 0 < ρ) (hε : |ε| < ρ) :
    IsPathConnected ((Metric.ball (0 : Point2) ρ) ∩ {u | u 1 = ε})
```

Each set is convex, and `![0,ε]` is an ACTUAL member since |ε|<ρ and ρ>0.
Thus nonempty PC, including negative ε and equality, is proved directly.
For the same φ from the structural theorem, the exact image identities are:

```text
φ.symm '' (ball 0 ρ ∩ {u | ε ≤ u 1})
  = φ.source ∩ {z | actualF hL ω (cover L X) + ε ≤ actualF hL ω z}
φ.symm '' (ball 0 ρ ∩ {u | u 1 = ε})
  = φ.source ∩ {z | actualF hL ω z = actualF hL ω (cover L X) + ε}.
```

Prove both inclusions using actual source/target membership, forward and
backward inverse laws and the original height identity. Apply inverse
continuity ONLY on its genuine target. There is no chart/radius/source
reselection per ε, sign, trace or slice.

## 6. Sole public declaration — fully expanded actual type

This literal type fixes all public quantifiers and avoids private aliases.
There is no public structural helper or public fixture/data declaration.

```lean
theorem actualSource_quotient_regular_local_collar
    {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L)
    (X : UniversalLaw.Spec.Lifetime.E 2)
    (hreg : fderiv ℝ (I4LifetimeField.actualField 2 L ω) X ≠ 0) :
    ∀ O : Set (I4Torus.SourceTorus 2 L), IsOpen O →
      I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ O →
      ∃ ρ : ℝ, 0 < ρ ∧
        ∃ φ : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) (Fin 2 → ℝ),
          I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ φ.source ∧
          φ (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) = 0 ∧
          φ.source ⊆ O ∧ φ.target = Metric.ball (0 : Fin 2 → ℝ) ρ ∧
          (∀ z ∈ φ.source,
            SourceActualFoldTorus.actualTorusField hL.ne' ω z =
              SourceActualFoldTorus.actualTorusField hL.ne' ω
                (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) + φ z 1) ∧
          ∀ ε : ℝ, |ε| < ρ →
            IsPathConnected (φ.source ∩ {z |
              SourceActualFoldTorus.actualTorusField hL.ne' ω
                (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) + ε ≤
                  SourceActualFoldTorus.actualTorusField hL.ne' ω z}) ∧
            IsPathConnected (φ.source ∩ {z |
              SourceActualFoldTorus.actualTorusField hL.ne' ω z =
                SourceActualFoldTorus.actualTorusField hL.ne' ω
                  (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) + ε})
```

One authored public Prop, public data/aliases/global instances0. The
nonzero derivative is literal ACTUAL fderiv, selected coordinates stay
private, every O precedes one φ/ρ, and every ε follows that one witness.
IsPathConnected supplies nonemptiness; level slices are local, and the
closed uppercut is literally ≤, with equality and negative ε retained.

## 7. ALL actual finite fixtures — exact data, independent scopes

The following are complete prospective fixture contracts; no fixture
implementation/proof body is written by this context. Production-private
and ordinary scopes EACH reconstruct this same actual original sample
independently using PUBLIC inputs, not an old private fixture or object.

Literal finite source data:

```text
L = 2, hL : 0 < (2 : ℝ)
poly : I4SourceFiniteTrig.TrigPoly
  = [⟨1, ![(1 : ℤ), 0], 0⟩, ⟨2, ![(0 : ℤ), 1], 0⟩]
ω : I4SmoothCarrier.SmoothSample 2 2
  = I4SourceFinitePinKernel.finiteShiftSample
      (I4SourceFiniteTrig.toSource 2 poly)
      (I4SourceSmoothConditional.zeroSample 2 2).
```

These exact values are NOT generic hypotheses or a standalone polynomial
substitution. The actual smooth sample is the actual result of the PUBLIC
constructor. Derive original sourceC2=π normalization and exact field by
PUBLIC toSource_eval, finite-shift coefficient/evaluation identities and
zero-sample expansion. The required own-private result in EACH scope is:

```lean
private theorem fixture_actual_formula (Y : E2) :
    I4LifetimeField.actualField 2 2 fixtureSample Y =
      Real.cos (Real.pi * (Q Y) 0) +
        2 * Real.cos (Real.pi * (Q Y) 1)
```

Here fixtureSample is the private actual constructor result above, created
only after TEXT release. It is not an axiom/parameter or new public API.
Physical lifts and fixed actual neighborhoods are:

```text
Xx    = Q.symm ![(1/2 : ℝ), 0]
Xy    = Q.symm ![0, (1/2 : ℝ)]
Xseam = Q.symm ![(-3/2 : ℝ), 0]
Xmax  = Q.symm ![(0 : ℝ), 0]
qX    = cover 2 X
OX    = cover 2 '' Metric.ball X (1/8 : ℝ).
```

The displayed radius is a PHYSICAL E2 ball. PUBLIC openness of the literal
projection composed with Q proves IsOpen OX and center membership. No
physical/Pi norm identification. Exact expected actual value/fderiv rows:

| Lift | g value | actual fderiv on physicalBasis0 | on physicalBasis1 |
| --- | --- | --- | --- |
| Xx | 2 | -Real.pi | 0 |
| Xy | 1 | 0 | -2*Real.pi |
| Xseam | 2 | -Real.pi | 0 |
| Xmax | 3 | 0 | 0 |

Every value and actual fderiv evaluation must be proved from that original
actual field, not a numerical regularity tag. For Xmax prove the whole
linear functional is zero via coordinate basis, not only the two table
entries without an extensionality step. Positive rows imply actual fderiv≠0
using π>0. The seam requires literal `cover 2 Xseam = cover 2 Xx` using
the existing period2 AddCircle quotient. No coincidence of independently
selected noncanonical charts is asserted.

### Complete positive consumers in BOTH scopes

For each of Xx, Xy and Xseam, a private consumer must ACTUALLY CALL the new
public endpoint with derived hL, the actual sample, actual nonzero fderiv
and its OX. It must not take a desired abstract chart as its starting
positive premise. Its existential result keeps the SAME selected ρ/φ and
all structural outputs from section6 and the universal all-ε assertion.

For every ε in the literal finite set `{0, ρ/2, -ρ/2}`, derive |ε|<ρ from
ρ>0 and consume both IsPathConnected outputs, nonemptiness and connectedness.
Additionally, all the following belong to the returned private existential
consumer package for that same selected φ (q,c,F denote that actual case):

```text
u  = ![0, ε],           z  = φ.symm u
u- = ![-ρ/2, ε],        z- = φ.symm u-
u+ = ![ρ/2, ε],         z+ = φ.symm u+.

u,u-,u+ ∈ φ.target = Metric.ball (0 : Point2) ρ;
z,z-,z+ ∈ φ.source;
φ z = u, φ z- = u-, φ z+ = u+;
F z = c+ε, F z- = c+ε, F z+ = c+ε;
z ∈ φ.source ∩ {p | F p = c+ε};
z ∈ φ.source ∩ {p | c+ε ≤ F p};
z-,z+ ∈ φ.source ∩ {p | F p = c+ε};
z- ≠ z+;
JoinedIn (φ.source ∩ {p | F p = c+ε}) z- z+.
```

Target membership uses the literal max norm, including the two off-center
points when ε=±ρ/2. Distinctness follows from actual inverse coordinates
and ρ>0. JoinedIn is consumed from THAT actual level slice's PC result.
Equality at z is a genuine closed-boundary consumer. Retain `φ.source⊆OX`
and universal `∀ε, |ε|<ρ → ...`; three fixed specializations do not replace
the all-ε result. No new public target, second mutation, or chart per case
within one positive package. Independently selecting charts for different
actual X/O invocations is permitted and their equality is not claimed.

## 8. Independent ordinary maximum counterproof — full contract

Ordinary module prospective header imports `SourceActualRegularLocalCollar`
and the same old PUBLIC finite-source inputs needed to reconstruct the
actual fixture; namespace `RegularLocalCollarControls`. All fixture data and
proofs stay PRIVATE, except the named closed mutation Prop and its negation
below. Ordinary is authored by the producer, with NO extra TEXT helper.

The ordinary scope reconstructs its OWN actual fixture and proves all
positive cases above using the public endpoint. Its negative counterproof
is independent of the production collar proof/PC conclusions and uses only
the original actual sample, PUBLIC quotient pullback/surjectivity and cosine
bounds. Required private interface:

```lean
private theorem fixture_global_quotient_bound
    (z : I4Torus.SourceTorus 2 2) :
    SourceActualFoldTorus.actualTorusField (show (2 : ℝ) ≠ 0 from two_ne_zero)
      fixtureSample z ≤ 3
```

The actual source period proof may use an equivalent explicitly typed
nonzero2 proof; proof irrelevance must not masquerade as a different sample.
For every z choose an actual lift by PUBLIC projection surjectivity,
transport by actualTorusField_pullback, use the independently derived
actual formula and cos≤1 with coefficients1 and2. No bound is supplied as
a production premise. Retain actual Xmax value3, actual fderiv zero, Omax
openness and qmax membership.

Before any negative harness, prove the structural impossibility for
ARBITRARY putative chart outputs, with exact typed shape:

```lean
private theorem no_regular_chart_at_actual_maximum
    (ρ : ℝ) (hρ : 0 < ρ)
    (φ : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) (Fin 2 → ℝ))
    (hsource : cover 2 Xmax ∈ φ.source)
    (hcenter : φ (cover 2 Xmax) = 0)
    (hinside : φ.source ⊆ smallO 2 Xmax)
    (htarget : φ.target = Metric.ball (0 : Fin 2 → ℝ) ρ)
    (hheight : ∀ z ∈ φ.source,
      actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample z =
        actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample
          (cover 2 Xmax) + φ z 1) : False
```

These are outputs assumed ONLY within a counterproof of a FALSE mutation,
not extra premises of production. The literal independent witness is
`u=![0,ρ/2]` and `z=φ.symm u`; hρ and htarget imply u∈φ.target, so
z∈φ.source and φ z=u. Actual max value3 and hheight force Fz=3+ρ/2>3,
contradicting the independently passed global bound. Every target/source/
inverse step is explicit. No production theorem/PC/uppercut output,
inherited critical-neighborhood PC, 64/65, hm or global Morse result is
called inside this counterproof. No empty-trace argument or endpoint-only
path inference is used.

## 9. Sole CLOSED ordinary mutation and negative interface

The ONLY altered mathematical input is deletion of actual fderiv!=0.
Every other actual input/output is retained. The ordinary closed Prop is
the fixed actual Xmax/Omax instance of that full weakened conclusion.
For precision, its exact intended logical expansion is:

```lean
-- In namespace RegularLocalCollarControls, with that scope's private
-- actual fixtureSample/Xmax/cover/smallO definitions fixed as above.
def omittedNonzeroDerivativeMutation : Prop :=
  ∃ ρ : ℝ, 0 < ρ ∧
    ∃ φ : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) (Fin 2 → ℝ),
      cover 2 Xmax ∈ φ.source ∧ φ (cover 2 Xmax) = 0 ∧
      φ.source ⊆ smallO 2 Xmax ∧
      φ.target = Metric.ball (0 : Fin 2 → ℝ) ρ ∧
      (∀ z ∈ φ.source,
        actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample z =
          actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample
            (cover 2 Xmax) + φ z 1) ∧
      ∀ ε : ℝ, |ε| < ρ →
        IsPathConnected (φ.source ∩ {z |
          actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample
            (cover 2 Xmax) + ε ≤
              actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample z}) ∧
        IsPathConnected (φ.source ∩ {z |
          actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample z =
            actualF (show (0 : ℝ) < 2 from zero_lt_two) fixtureSample
              (cover 2 Xmax) + ε})

theorem not_omittedNonzeroDerivativeMutation :
    ¬ omittedNonzeroDerivativeMutation
```

These two declarations alone are PUBLIC in ordinary Controls solely for
the importing negative. They are not production targets/public data and
are included in ALL ordinary-owned classification/std3. The Prop is closed;
fixtureSample/Xmax are fixed definitions, not free arguments, axioms,
assumed mutation hypotheses or a hidden desired-chart certificate. The
proof of its negation must consume the independent impossibility above.

ONLY AFTER complete ordinary strict PASS AND separate exhaustive ALL-owned
ordinary classified standard3 inventory PASS may one later importing
negative assert this CLOSED Prop. Its contract is exactly:

```text
Import only the already-passed ordinary Controls module and its transitive
qualified public dependencies. Assert the no-premise proposition
RegularLocalCollarControls.omittedNonzeroDerivativeMutation.
Reduce using the already-passed public negation to a single intended
unresolved False. No assumed mutation, hypothesis, axiom, parameter,
admit, sorry, private-name access or extra mathematical premise.
```

The exact harness implementation is NOT written here. Its complete initial
text/context/FIRST ID and prospective invocation entry must be frozen BEFORE
its ONE invocation. A parameterized implication from an assumed mutation
is not this negative. Reuse the passed actual bound/counterproof; do not
replay their construction in a second campaign. Intended mathematical
False is the only rejection; setup/API/type/source errors do not count.
No ordinary named kernel. No second range/equality/ρ/target/sample mutation.

## 10. Dedicated runner, original versions and qualification order

The initial prospective artifacts are:

- `INITIAL_SOURCE_COMMON.lean.txt`: imports/open/namespace header only.
- `FROZEN_CONTEXT.md`: this complete review contract, no proofs executed.
- `CONTROL_CONTRACT.md`: root's exact14724B copy, first ID
  805ccbfa39de792035c5979af62187fcccec2e6fdbe7451e3515ab09c3a932c7 REUSED.
- `runner/capture66.py`: dedicated entry/outer stream/status capture.
- `runner/record_run.py`: actual documentary/math worker, initial snapshots
  and new-version first-ID cache. Separate root mathematical release gates
  any future `math` invocation; initial context GO cannot enable it.
- `runner/bootstrap_context.py`: documentary context-ID binding only.
- `BOOTSTRAP_PLAN.md`: exact scope and launch order.

The FIRST actual stage66 documentary invocation is an external literal
Python-c freezer under THREE already frozen root65
`native-runtime/capture.py` wrappers: entry, outer and worker. It preserves
this initial metadata amendment's actual originals and FULL patch, then
FIRST-hashes only the explicit NEW66 context/header/plan/runner versions,
creates immutable exact snapshots with inherited IDs and seeds the copied
controls' known ID before ANY new66 script's own first execution.
The first invocation's original argv/code/cwd/start/end/status and full
separate streams remain in `initial-external-freeze001/{entry,outer,worker}`.
The wrapper operation fields honestly retain legacy `root65-*-capture`
labels; actual stage66 paths and literal commands identify this use.
No old utility copy/hash or mathematical replay is performed.

ONLY AFTER that external freezer and all three wrappers actually close,
the first DEDICATED66 worker is
`record_run.py context-bootstrap001 documentary -- python3 runner/bootstrap_context.py`,
under the now-pre-frozen dedicated66 entry and outer wrappers. It reuses
the externally cached NEW66 initial script/context/header/plan IDs and known
control-copy ID; it does NOT claim that a script's self-hash occurs before
its own start. Before launching its child it snapshots these exact known
versions with inherited IDs and records literal argv/cwd/prospective start,
outer/entry locations and nonsecret environment selection. Its later receipt
retains actual end/status/duration, full separate original stdout/stderr and
before/after IDs. First external and later dedicated invocations remain
separate original records. No fictional first-success history, relabeling
of the later worker as the first invocation or reconstructed prior stream.

The new worker tracks ONLY its own initial context/header/runners, later
new source/ordinary/harness versions, own full patches and NEW own/ordinary
output objects. It never rehashes unchanged old proof or known copy; it
never snapshots/copies a binary object. Necessary new object IDs may be
collected when those new artifacts later arise, cached once. All actual
later versions precede their invocations; preserve full originals/deltas,
helper one-integration lineage and actual failures. Known exact snapshot
copies inherit IDs without repeat hashing. Root owns all canonical copies.

After separate TEXT and mathematical execution releases, the prospective
qualification order is: complete physical milestone; complete quotient/
exact-ball/geometry/public assembly; ALL owned production private positives;
reusable final strict success; exhaustive actual module-index ALL-owned
classification/std3; early nonauthor full final source review; EXACTLY ONE
complete final production named-own-module kernel after final freezes;
separate producer-authored ordinary positives/counterproof strict PASS;
separate exhaustive ALL ordinary-owned/private/data/generated/foreign-
generated classified standard3 PASS; exact initial CLOSED harness freeze;
ONE intended False invocation; final evidence/custody review and root
publication. No ordinary/helper/fixture named kernel. Requalification is
limited to a specific new change/defect/uncovered obligation; a new agent,
session/head/freeze/handoff/provider process is not a reason to replay.

No sorry/custom axiom/native_decide/implemented_by/umbrella Mathlib/private
or generated foreign API. Transitive axioms only propext, Classical.choice,
Quot.sound or subsets. Exactly one production authored public Prop;
production public data/aliases/global instances0. Ordinary named mutation
Prop+negation are separately classified, not added frontier targets.

Root alone owns shared metadata/config/cache, Git/sourcecuts/registration,
external messages/publication and the eligible final NEW own-object copy
ONCE after an actual sourcecut; old/helper/ordinary/further object actions
all SKIP. Producer only its own new source/scratch after applicable release.

## 11. Limits and current bound

Regular collar mathematical construction is accepted but not elaborated.
The concrete remaining typed joins are actual derivative transport through
Q, finite2 CLE/inverse laws/actual derivative equality, positive-order IFT,
local positive-period Fact/discreteness, quotient/O/inverse-ball source-
target equations, and exact target-image trace identities. Report actual
typed defects narrowly; no new public certificate premise or broad engine.

Planning estimates are risks, not promises. Current unit checkpoint
23:20UTC28Oct and HARD03:30UTC29Oct/end whichever first/no automatic
extension. Earlier closed65 times and completed mathematical/CI evidence
remain separate reusable history; no further old CI poll or math campaign.

Uniform finite adjacency, overlap/clearance persistence, lower compact
clopen separation, actual critical-event component inclusions, maximum/
minimum event leaves, global saddle/elder choices, exhaustive H0/once-count,
Borel/Rice/PairLaw and Parent remain OPEN. The original goal ACTIVE_UNMET
continues beyond a local theorem. OpenDraft/noReady/noMerge/samefamily0/
scienceNONE; provider-distinct process separate; 014KMath403 STOP/no denial
workaround; no foreign role release or Main seat. Owner `/workspace/AGENTS.md`
completed-verification REUSE applies across all handoffs.
