# Stage64 COMPLETE literal context001 before helper TEXT/execution

ROOT_GO was personally read in full after FULL personal reading of the four published proper64 documents and four accepted design reports. Root adoption/no-hm revision supersedes historical drafts. This context defines the complete literal header, shared private types, chart/geometry/transport/public targets, source-local fixtures, ordinary mutation and custody. No helper proof TEXT or64 Lean execution has begun. Root FULL acceptance, EACH helper PERSONAL FULL ACK and explicit release precede helper proof text.

## Locked authority/paths

- Source: `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025/SourceActualQuotientSaddleCollar.lean`, existing root-confirmed isolated taskworktree.
- Producer scratch: `/workspace/scratch/actual-source-quotient-saddle-collar-construct`.
- Helper A `/root/actual_canonical_capture_application` ONLY `/workspace/scratch/actual-source-quotient-saddle-collar-chart-text`.
- Helper B `/root/actual_canonical_partner_preflight` ONLY `/workspace/scratch/actual-source-quotient-saddle-collar-geometry-text`.
- These paths were LOCKED in GO before this context; no independent renaming or inferred alternatives.
- Fresh native6478705132 actual19:35:23/fullGETMATCH19:38:05. GO19:41:48.802880 follows COMPLETE adopted controls copy19:41:48.802646. CP19:55, hard22:30UTC28Oct/end, no automatic extension.
- Root alone shared metadata/config/cache/Git/registry/external/eligible new own-object placement. Producer owns only new source/scratch/all actual amendments/executions/custody.
- PUBLIC60 only for the local normal form; no global hm, private60/61/62/63 fixture/normalizer/ordinary body or old object promotion. No63 mathematical dependency.
- Completed applicable verification/mathematics reused under owner guidance; new check only for actual new text/defect/uncovered obligation. Provider process separate/same-family science credit0/science NONE. No unchanged CI polling.

## Literal common imports/header for production AND ordinary Controls

Ordinary Controls prepends `import SourceActualQuotientSaddleCollar`. The remainder is identical:

```lean
import SourceActualMorseLocalModel
import SourceActualFoldTorus
import SourceFiniteTrig
import SourcePinPreservingQuartic
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Instances.ZMultiples
import Mathlib.Topology.OpenPartialHomeomorph.Constructions
import Mathlib.Topology.OpenPartialHomeomorph.Composition
import Mathlib.Topology.OpenPartialHomeomorph.IsImage
import Mathlib.Topology.OpenPartialHomeomorph.Basic
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Convert
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Abel
import Lean.Elab.Tactic.Omega

noncomputable section
open Set Filter Topology
open UniversalLaw.Spec.Lifetime
open I4LifetimeField I4SmoothCarrier
open scoped BigOperators Topology
set_option autoImplicit false
```

Production namespace `I4SourceActualQuotientSaddleCollar`; ordinary namespace `QuotientSaddleCollarControls`. Helper sections omit imports/namespace/end and common definitions/structures. No umbrella imports. Use `_root_.AddCircle` explicitly if ambiguity arises; actual torus is always `I4Torus.SourceTorus 2 L`.

### Exact positive-period/discrete instance binding

Inside the actual chart theorem from hL, derive locally:

```lean
let _ : Fact (0 < L) := ⟨hL⟩
let _ : DiscreteTopology (AddSubgroup.zmultiples L) := inferInstance
```

The actual old public instance in `Mathlib.Topology.Instances.ZMultiples` is `instance {a : ℝ} : DiscreteTopology (AddSubgroup.zmultiples a)`. Positive-period Fact is required separately by AddCircle interval charts. Neither is a public caller premise or exported global instance.

The old constructor is `AddCircle.openPartialHomeomorphCoe L a : OpenPartialHomeomorph ℝ (_root_.AddCircle L)` under these local instances. Its source is exactly Ioo a (a+L), forward quotient coercion, target complement of projected a. For each i use a=coordinates2X i-L/2. `OpenPartialHomeomorph.pi` takes the finite family directly. `(coordinates 2).toHomeomorph.toOpenPartialHomeomorph` supplies the physical-to-Pi homeomorphism. Compose on actual source/target intersections, restrict source to O, shrink the INVERSE to a contained centered open ball, then invert to obtain exact target equality. No norm isometry, unrestricted representative, atlas or noninjective-image separation.

## Producer-supplied private common definitions/structures

These literal bytes precede BOTH helper sections, and helpers NEVER redeclare them:

```lean
private abbrev Point2 := Fin 2 → ℝ

private def physicalProjection (L : ℝ) (X : UniversalLaw.Spec.Lifetime.E 2) :
    I4Torus.SourceTorus 2 L :=
  I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)

private def saddleQ (u : Point2) : ℝ := -(u 0)^2 + (u 1)^2

private def targetStrict (rho : ℝ) : Set Point2 :=
  Metric.ball 0 rho ∩ {u | 0 < saddleQ u}

private def targetPlus (rho : ℝ) : Set Point2 :=
  targetStrict rho ∩ {u | 0 < u 1}

private def targetMinus (rho : ℝ) : Set Point2 :=
  targetStrict rho ∩ {u | u 1 < 0}

private def targetLower (rho delta : ℝ) : Set Point2 :=
  Metric.ball 0 rho ∩ {u | -delta ≤ saddleQ u}

private structure ChartFacts {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop where
  center_mem : q ∈ phi.source
  center_zero : phi q = 0
  source_subset : phi.source ⊆ O
  target_eq : phi.target = Metric.ball (0 : Point2) rho
  identity : ∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2

private structure SaddleGeometry (rho : ℝ) : Prop where
  plus_pc : IsPathConnected (targetPlus rho)
  minus_pc : IsPathConnected (targetMinus rho)
  disjoint : Disjoint (targetPlus rho) (targetMinus rho)
  partition : targetStrict rho = targetPlus rho ∪ targetMinus rho
  joined_iff : ∀ u ∈ targetStrict rho, ∀ v ∈ targetStrict rho,
    JoinedIn (targetStrict rho) u v ↔ 0 < (u 1) * (v 1)
  lower_pc : ∀ delta : ℝ, 0 ≤ delta → IsPathConnected (targetLower rho delta)

private def CollarFacts {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  ChartFacts F q O rho phi ∧
  let W := phi.source ∩ {z | F q < F z}
  let Bplus := W ∩ {z | 0 < phi z 1}
  let Bminus := W ∩ {z | phi z 1 < 0}
  IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
    W = Bplus ∪ Bminus ∧
    (∀ p ∈ W, ∀ r ∈ W, JoinedIn W p r ↔ 0 < (phi p 1) * (phi r 1)) ∧
    (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | F q-delta ≤ F z}))
```

These are PRIVATE implementation definitions/Prop bundles, not public data or supplied desired certificates. Point2 is exactly the actual Pi/max norm type Fin2→ℝ, not physical Euclidean E2. Both geometry and chart witness coherence are explicit.

## Helper A exact COMPLETE production endpoint

ONE complete PRIVATE text section, all needed private old-chart membership/composition/restriction lemmas, ending exactly:

```lean
private theorem quotientSaddleChart {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O)
    (hXO : physicalProjection L X ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
        ChartFacts (SourceActualFoldTorus.actualTorusField hL.ne' omega)
          (physicalProjection L X) O rho phi
```

Actual source inputs only; A derives ALL ChartFacts internally using PUBLIC60, local positive/discrete bindings, centered product quotient chart, actual pullback and exact inverse ball restriction inside every O. No assumed chart/normal-form certificate, old private definition, C1-Torus atlas, fixture, finite geometry, transport/public API, standalone execution or partial delivered endpoint. Preserve signs ordered−coordinate0²+coordinate1² at j1.

## Exact PUBLIC60 statement ONLY (accepted dependencies reused)

```lean
I4SourceActualMorseLocalModel.actualSource_c1_quadratic_localModel
  {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L)
  (X : UniversalLaw.Spec.Lifetime.E 2) (j : ℕ)
  (hc : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
  (hi : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X j) :
  j ≤ 2 ∧ ∃ psi : OpenPartialHomeomorph (UniversalLaw.Spec.Lifetime.E 2) (Fin 2 → ℝ),
    X ∈ psi.source ∧ psi X = 0 ∧ (0 : Fin 2 → ℝ) ∈ psi.target ∧
    ContDiffOn ℝ 1 psi psi.source ∧ ContDiffOn ℝ 1 psi.symm psi.target ∧
    (∀ x ∈ psi.source, I4LifetimeField.actualField 2 L omega x =
      I4LifetimeField.actualField 2 L omega X +
      ∑ i : Fin 2, (if i.val < j then (-1 : ℝ) else 1) * (psi x i)^2) ∧
    (∀ O : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen O → X ∈ O →
      ∃ V : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen V ∧ X ∈ V ∧
        V ⊆ O ∩ psi.source ∧
        IsPathConnected (V ∩ {x | I4LifetimeField.actualField 2 L omega X ≤
          I4LifetimeField.actualField 2 L omega x}))
```

No hM/global IsMorseDistinct premise. Only the chart/ordered identity portion is consumed. Actual smoothness/nondegeneracy normalization is already qualified60; do not reprove it. Exact old PUBLIC pullback: F(torusProjection2L x)=smoothSourceField2Lomega x, hence F(physicalProjection L Y)=actualField2Lomega Y.

Reading honesty: producer's requested1002–1018 slice exposed the public statement1002–1015 plus three incidental lines of its proof stub. No private helper definition/proof body was inspected, used, copied or supplied here. The only helper input is the public statement above. A final rg for discrete-zmultiples in AddCircle.Real had no match/exit1; actual public instance was then read in the directly imported ZMultiples file. These are read-only binding observations, not Lean/API probes/checks or mathematical failures; exact tool outputs remain in conversation, not reconstructed original split files.

## Helper B exact COMPLETE finite Point2 geometry endpoint

ONE complete PRIVATE text section, including any needed private finite norm/cone/convex/star/path/IVT lemmas, ending:

```lean
private theorem saddleConeGeometry (rho : ℝ) (hrho : 0 < rho) : SaddleGeometry rho
```

Prove all six fields on the literal common sets. IsPathConnected includes nonemptiness, with actual `(0,±rho/2)` witnesses in the Pi norm ball. Strict Q>0 cones are u1>|u0| or u1<−|u0| and convex; same-sign joining/cross-sign IVT gives joined_iff. For EVERY delta≥0, centered lower Q≥−delta trace is star convex about0 via homogeneity, not a chart selected per delta. No assumed source chart, new public data/global incidence, maximum/minimum/positive CLOSED uppercut, execution or desired-geometry hypothesis.

## Producer-owned transport and actual assembly interfaces

```lean
private theorem transportSaddleCollar {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (hrho : 0 < rho) (hchart : ChartFacts F q O rho phi)
    (hgeometry : SaddleGeometry rho) : CollarFacts F q O rho phi

private theorem actualSaddleCollar {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O) (hXO : physicalProjection L X ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
        CollarFacts (SourceActualFoldTorus.actualTorusField hL.ne' omega)
          (physicalProjection L X) O rho phi
```

Transport uses actual source-target homeomorphism/inverse/continuity, exact set/image/preimage identities and structural actual quadratic identity. Generic chart facts are instantiated by quotientSaddleChart; none is a final public input.

## SOLE PUBLIC proposition — literal expanded no-private-alias type

```lean
theorem actualSource_quotient_saddle_local_collar {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1) :
    let F := SourceActualFoldTorus.actualTorusField hL.ne' omega
    let q := I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)
    let c := F q
    ∀ O : Set (I4Torus.SourceTorus 2 L), IsOpen O → q ∈ O →
      ∃ rho : ℝ, 0 < rho ∧
        ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) (Fin 2 → ℝ),
          q ∈ phi.source ∧ phi q = 0 ∧ phi.source ⊆ O ∧
          phi.target = Metric.ball (0 : Fin 2 → ℝ) rho ∧
          (∀ z ∈ phi.source, F z = c-(phi z 0)^2+(phi z 1)^2) ∧
          let W := phi.source ∩ {z | c < F z}
          let Bplus := W ∩ {z | 0 < phi z 1}
          let Bminus := W ∩ {z | phi z 1 < 0}
          IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
            W = Bplus ∪ Bminus ∧
            (∀ p ∈ W, ∀ r ∈ W, JoinedIn W p r ↔ 0 < (phi p 1)*(phi r 1)) ∧
            (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | c-delta ≤ F z}))
```

Exactly one authored public Prop/no public data/global instances. One radius/chart AFTER each O, same witness for EVERY branch and ALL delta. No unused hm, desiredchart/certificate, rotated law/isometry, C1-torus structure or global component claim.

## Producer-owned literal actual fixture definitions (after generic section)

```lean
private def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, Pi.single (0 : Fin 2) 1, 0⟩,
   ⟨2, Pi.single (1 : Fin 2) 1, 0⟩]

private def fixtureSample : I4SmoothCarrier.SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)

private def fixtureTorusField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample

private def fixturePoint (x y : ℝ) : UniversalLaw.Spec.Lifetime.E 2 :=
  (I4LifetimeField.coordinates 2).symm ![x,y]

private def fixtureSmallOpen (X : UniversalLaw.Spec.Lifetime.E 2) :
    Set (I4Torus.SourceTorus 2 2) :=
  physicalProjection 2 '' Metric.ball X (1/8 : ℝ)
```

The last ball is PHYSICAL E2; the output chart target is Pi2. Producer derives actual finite field identity, first/second derivatives and hcrit/FULL complementary inertia once per privacy scope; no old private body copy, global hm/parity/torusDist proof, desiredcert or synthetic quadratic fixture. Required private exact endpoints:

```lean
private theorem fixture_actualField (Y : UniversalLaw.Spec.Lifetime.E 2) :
  I4LifetimeField.actualField 2 2 fixtureSample Y =
    Real.cos (Real.pi * I4LifetimeField.coordinates 2 Y 0) +
      2 * Real.cos (Real.pi * I4LifetimeField.coordinates 2 Y 1)

private theorem fixture_saddleInputs :
  (UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample)
      (fixturePoint 1 0) ∧
   UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample)
      (fixturePoint 1 0) 1 ∧ I4LifetimeField.actualField 2 2 fixtureSample (fixturePoint 1 0) = 1) ∧
  (UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample)
      (fixturePoint 0 1) ∧
   UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample)
      (fixturePoint 0 1) 1 ∧ I4LifetimeField.actualField 2 2 fixtureSample (fixturePoint 0 1) = -1)

private theorem fixture_seamInputs :
  UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample)
      (fixturePoint (-1) 0) ∧
  UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample)
      (fixturePoint (-1) 0) 1 ∧
  I4LifetimeField.actualField 2 2 fixtureSample (fixturePoint (-1) 0) = 1 ∧
  physicalProjection 2 (fixturePoint (-1) 0) = physicalProjection 2 (fixturePoint 1 0)

private theorem fixture_smallOpen (X : UniversalLaw.Spec.Lifetime.E 2) :
  IsOpen (fixtureSmallOpen X) ∧ physicalProjection 2 X ∈ fixtureSmallOpen X
```

The three literal stable private consumer signatures are:

```lean
private theorem fixture_saddlePositive :
  ∃ rho : ℝ, 0 < rho ∧
    ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      CollarFacts fixtureTorusField (physicalProjection 2 (fixturePoint 1 0))
        (fixtureSmallOpen (fixturePoint 1 0)) rho phi

private theorem fixture_saddleNegative :
  ∃ rho : ℝ, 0 < rho ∧
    ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      CollarFacts fixtureTorusField (physicalProjection 2 (fixturePoint 0 1))
        (fixtureSmallOpen (fixturePoint 0 1)) rho phi

private theorem fixture_seam :
  ∃ rho : ℝ, 0 < rho ∧
    ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      CollarFacts fixtureTorusField (physicalProjection 2 (fixturePoint (-1) 0))
        (fixtureSmallOpen (fixturePoint (-1) 0)) rho phi
```

They call actualSaddleCollar with independently derived actual local inputs/small O, hence exercise new actual chart, geometry and transport. Both saddles have genuinely complementary negative/positive lines; seam uses its own physical lift/O. No equality of chosen noncanonical charts.

## Producer-owned ordinary Controls contract and SOLE mutation

File `QuotientSaddleCollarControls.lean`, namespace `QuotientSaddleCollarControls`, same literal common imports prefixed by new public module. Producer alone authors ordinary TEXT/proofs/edits; NO third/helper ordinary author. Reconstruct same fixture definitions with private removed; define ordinary `physicalProjection` literally as above, no production-private call. Reuse actual field/local facts within this scope once, with no global hm.

Ordinary uses its own literal `physicalProjection`, `fixturePolynomial`, `fixtureSample`, `fixtureTorusField`, `fixturePoint`, `fixtureSmallOpen` definitions, as above with private removed. Its derived local input/open theorems `saddleInputs`, `seamInputs`, `smallOpen` have exactly the production fixture_saddleInputs/fixture_seamInputs/fixture_smallOpen types with private removed. No assumed positive certificate or global hm.

The following ordinary predicate is producer-defined, fully expanded, and is NOT a production-private API:

```lean
def OrdinaryCollar (X : UniversalLaw.Spec.Lifetime.E 2) : Prop :=
  let q := physicalProjection 2 X
  let c := fixtureTorusField q
  ∃ rho : ℝ, 0 < rho ∧
    ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) (Fin 2 → ℝ),
      q ∈ phi.source ∧ phi q = 0 ∧ phi.source ⊆ fixtureSmallOpen X ∧
      phi.target = Metric.ball (0 : Fin 2 → ℝ) rho ∧
      (∀ z ∈ phi.source, fixtureTorusField z = c-(phi z 0)^2+(phi z 1)^2) ∧
      let W := phi.source ∩ {z | c < fixtureTorusField z}
      let Bplus := W ∩ {z | 0 < phi z 1}
      let Bminus := W ∩ {z | phi z 1 < 0}
      IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
        W = Bplus ∪ Bminus ∧
        (∀ p ∈ W, ∀ r ∈ W, JoinedIn W p r ↔ 0 < (phi p 1)*(phi r 1)) ∧
        (∀ delta : ℝ, 0 ≤ delta →
          IsPathConnected (phi.source ∩ {z | c-delta ≤ fixtureTorusField z}))

theorem positiveSaddle : OrdinaryCollar (fixturePoint 1 0)
theorem negativeSaddle : OrdinaryCollar (fixturePoint 0 1)
theorem seamSaddle : OrdinaryCollar (fixturePoint (-1) 0)

def chosenRadius : ℝ
def chosenChart : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) (Fin 2 → ℝ)
def chosenCenter : I4Torus.SourceTorus 2 2 := physicalProjection 2 (fixturePoint 1 0)
def chosenHeight : ℝ := fixtureTorusField chosenCenter
def chosenSource : Set (I4Torus.SourceTorus 2 2) := chosenChart.source
def chosenStrictTrace : Set (I4Torus.SourceTorus 2 2) :=
  chosenSource ∩ {z | chosenHeight < fixtureTorusField z}

theorem chosenChart_structure :
  0 < chosenRadius ∧ chosenCenter ∈ chosenChart.source ∧ chosenChart chosenCenter = 0 ∧
    chosenChart.source ⊆ fixtureSmallOpen (fixturePoint 1 0) ∧
    chosenChart.target = Metric.ball (0 : Fin 2 → ℝ) chosenRadius ∧
    (∀ z ∈ chosenChart.source,
      fixtureTorusField z = chosenHeight-(chosenChart z 0)^2+(chosenChart z 1)^2)

def strictPointPlus : I4Torus.SourceTorus 2 2 := chosenChart.symm ![0,chosenRadius/2]
def strictPointMinus : I4Torus.SourceTorus 2 2 := chosenChart.symm ![0,-chosenRadius/2]
theorem strictPoints_mem :
  strictPointPlus ∈ chosenStrictTrace ∧ strictPointMinus ∈ chosenStrictTrace
theorem not_pathConnected_chosenStrictTrace : ¬ IsPathConnected chosenStrictTrace
```

The typed chosenRadius/chosenChart signatures above are normative declarations whose bodies later choose ONE witness from positiveSaddle (Classical.choose and its SAME existential specification); neither is an additional premise. The three positive theorems independently derive local actual premises/open small O, then call the new PUBLIC theorem. chosenChart_structure extracts ONLY structural fields, NEVER branch/JoinedIn fields. No re-selection for delta or counterproof.

`strictPointPlus=chosenChart.symm ![0,chosenRadius/2]` and `strictPointMinus=chosenChart.symm ![0,-chosenRadius/2]`. `strictPoints_mem` proves both actually belong to chosenStrictTrace from exact target/inverse/identity, independently of production branch fields. `not_pathConnected_chosenStrictTrace` uses a hypothetical PC path, coordinate1 continuity/IVT at0 and actual identity F≤c contradicting strict c<F. Fixed rho/phi/source/field/level/carrier/strictness throughout. No use of production branch/JoinedIn result, alternative chosenchart, empty shortcut, global incidence or second mutation.

```lean
def strictPCMutation : Prop := IsPathConnected chosenStrictTrace
theorem not_strictPCMutation : ¬ strictPCMutation
```

After ordinary Controls strict PASS with actual local positives and this independent counterproof, producer authors/runs exactly ONE negative importing ONLY `QuotientSaddleCollarControls` plus its transitive public dependencies, falsely asserting strictPCMutation and using not_strictPCMutation to leave exactly one intended mathematical False. No missingname/typeclass/privateaccess/timeout counts. Production kernel does NOT cover ordinary Controls.

## Delivery, execution and custody

- A: ONE `QuotientChartSection.ORIGINAL.lean.txt`; B: ONE `SaddleGeometrySection.ORIGINAL.lean.txt`, each with exact imports/context/provenance/freeze metadata in its GO-locked scratch.
- Root FULLacceptance + EACH PERSONAL FULLcontext ACK with actually observed UTC (or explicit uninstrumented) BEFORE helper text; explicit release then complete originals freeze before producer FIRST IDs/ONE integration. ZERO helper Lean/probe/check/hash/object/Git/cache/external. All actual amendments producer-owned; no regenerated originals/pasteins/standalone helper lineage.
- Initial runner001 and complete context001 freeze BEFORE first execution. Preserve every actual version BEFORE execution/full actual patch; each command snapshots source/harness/context/runner first, exact command/cwd/start/end/elapsed/exit and FULL original separate stdout/stderr.
- IMPORTANT math, documentary-generator and metadata-worker/outer executions are wrapped PROSPECTIVELY, not retrospectively. Direct tool/file-write histories labeled honestly. Cached FIRST IDs ensure each newly created/changed payload is hashed once and all later references reused. No reconstructed timestamps/freezes/streams and no old payload/check replays.
- Dynamic exhaustive own-module ownership/classification, including private definitions/Prop bundles/generated/foreigngenerated; standard3 ONLY. Exactly ONE final complete named own-module kernel AFTER whole finalsource+private positives/strict/inventory/earlyreview; no partialkernel. Root ONLY eligible new own object ONCE after sourcecut; furthercopiesSKIP, no helper/Controls/ilean/old promotion.

Scope remains local saddle only: no uniform positive CLOSEDuppercuts, regular collars, finite adjacency, lower clopen separation, global H0 merger/unique elder saddle/count/oncecount/Borel/Rice/PairLaw/Parent result. Original larger goal remains active. No future65 role/code/claim/GO/timer is implied.

## Context002 exact pre-text interface refinement

Before any helper proof text or Lean execution, expand the three private fixture consumer signatures to their literal fixed points, and expand the ordinary predicate/positive/chosen object signatures. No imports/instances/private chart or geometry signature/public target/locked path/mathematical/control change. Original001 and complete actual001→002 patch remain immutable. Helpers receive FULL final002 for personal ACK; no earlier helper proof text exists.

## Context003 narrow public convex-ball import amendment

B identified the concrete public convex_ball binding in Mathlib.Analysis.Normed.Module.Convex before dependent geometry text. Add exactly that narrow import to BOTH common headers; no signature/math/public/control/path change. A complete original already froze under002 before this amendment, so it stays immutable and no A regeneration/integration occurs. B personally ACKs this actual import amendment before dependent text. Producer header001 is retained; header002 reflects this import. No Lean/probe or old check was used to decide the amendment.
