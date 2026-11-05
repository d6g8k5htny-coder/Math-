# Stage65 complete pre-text context, version001

This is the literal binding before any helper proof text or Lean execution. The producer personally read ROOT_GO and all nine proper design documents; their completed readings and all applicable qualified64 evidence are reused. Root alone owns Git, shared metadata/cache, canonical eligible-object copying and external actions. Producer owns this new source, own scratch, all actual amendments/executions/custody. Helper B owns ONLY `/workspace/scratch/actual-source-saddle-uppercuts-geometry-text`; one complete private geometry text section, no imports/namespace/end/common definitions, no execution/probe/check/hash/object/Git/cache/external action. Root full-context acceptance, B personal full ACK and explicit root TEXT release must precede helper proof text. No other proof-text helper or ordinary author.

## Literal production header

```lean
import SourceActualQuotientSaddleCollar
import SourceFiniteTrig
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.PathConnected
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
namespace I4SourceActualSaddleUppercuts
```

No global positivity/discrete/quotient instance is introduced. Any `Fact (0 < L)` and discrete zmultiples instance required by a public operation is derived locally from the literal hL. Point2 below is the actual finite Pi normed space, never EuclideanSpace and never an isometry assertion. The ordinary header is EXACTLY the same imports, additionally prepended `import SourceActualSaddleUppercuts`, with namespace `ActualSaddleUppercutsControls` instead. All definitions below are private in production and reproduced freshly within ordinary context as ordinary-owned names; ordinary never imports private source names.

## Complete common literal definitions

```lean
private abbrev Point2 := Fin 2 → ℝ
private def saddleValue (u : Point2) : ℝ := -(u 0)^2 + (u 1)^2
private def targetUpper (rho eps : ℝ) : Set Point2 :=
  Metric.ball 0 rho ∩ {u | eps ≤ saddleValue u}
private def targetUpperPos (rho eps : ℝ) : Set Point2 :=
  targetUpper rho eps ∩ {u | 0 < u 1}
private def targetUpperNeg (rho eps : ℝ) : Set Point2 :=
  targetUpper rho eps ∩ {u | u 1 < 0}

private structure ClosedBranchFacts (rho eps : ℝ) : Prop where
  plus_pc : IsPathConnected (targetUpperPos rho eps)
  minus_pc : IsPathConnected (targetUpperNeg rho eps)
  disjoint : Disjoint (targetUpperPos rho eps) (targetUpperNeg rho eps)
  partition : targetUpper rho eps = targetUpperPos rho eps ∪ targetUpperNeg rho eps
  plus_witness : (![0, rho/2] : Point2) ∈ targetUpperPos rho eps
  minus_witness : (![0, -rho/2] : Point2) ∈ targetUpperNeg rho eps

private def upperTrace {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (eps : ℝ) : Set (I4Torus.SourceTorus 2 L) :=
  phi.source ∩ {z | F q + eps ≤ F z}

private structure InheritedCollar {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop where
  center_mem : q ∈ phi.source
  center_eq : phi q = 0
  source_sub : phi.source ⊆ O
  target_eq : phi.target = Metric.ball 0 rho
  field_eq : ∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2
  lower_pc : ∀ delta : ℝ, 0 ≤ delta →
    IsPathConnected (phi.source ∩ {z | F q - delta ≤ F z})
  strict_test : ∀ p ∈ phi.source ∩ {z | F q < F z},
    ∀ r ∈ phi.source ∩ {z | F q < F z},
    JoinedIn (phi.source ∩ {z | F q < F z}) p r ↔ 0 < (phi p 1)*(phi r 1)

private def UpperClause {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) (eps : ℝ) : Prop :=
  let U := upperTrace F q phi eps
  let Bplus := U ∩ {z | 0 < phi z 1}
  let Bminus := U ∩ {z | phi z 1 < 0}
  IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
    U = Bplus ∪ Bminus ∧
    (∀ p ∈ U, ∀ r ∈ U, JoinedIn U p r ↔ 0 < (phi p 1)*(phi r 1))

private def UniformCutResult {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  q ∈ phi.source ∧ phi q = 0 ∧ phi.source ⊆ O ∧
  phi.target = Metric.ball 0 rho ∧
  (∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2) ∧
  (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | F q-delta ≤ F z})) ∧
  0 < rho^2/4 ∧ ∀ eps : ℝ, 0 < eps → eps < rho^2/4 → UpperClause F q phi eps

private def CutoffEquality {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (rho : ℝ)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  0 < rho^2/16 ∧ rho^2/16 < rho^2/4 ∧
  phi.symm (![0, rho/4] : Point2) ∈ upperTrace F q phi (rho^2/16) ∧
  phi.symm (![0, -rho/4] : Point2) ∈ upperTrace F q phi (rho^2/16) ∧
  F (phi.symm (![0, rho/4] : Point2)) = F q + rho^2/16 ∧
  F (phi.symm (![0, -rho/4] : Point2)) = F q + rho^2/16 ∧
  0 < phi (phi.symm (![0, rho/4] : Point2)) 1 ∧
  phi (phi.symm (![0, -rho/4] : Point2)) 1 < 0
```

## Sole helper B endpoint

```lean
private theorem closedSaddleBranchGeometry (rho : ℝ) (hrho : 0 < rho)
    (eps : ℝ) (heps : 0 < eps) (hbound : eps < rho^2/4) :
    ClosedBranchFacts rho eps
```

The COMPLETE section proves both sign branches path connected and nonempty, disjointness and exact partition, with fixed witnesses ±rho/2. Derive actual Pi ball coordinate inequalities. Same-sign connections use the whole three-segment path through H=max(v,v′), m=max(|u|,|u′|), proving EVERY point stays in strict box and CLOSED quadratic constraint; reflect for negative branch. No supplied geometry/path certificate, no sqrt/SOC/Euclidean isometry, no no-cross IVT or lower-star reproof. Helper may add private supporting definitions/theorems, but never duplicate common definitions. Complete original, separate exact imports/context/provenance/freeze metadata, ZERO execution/hash, before producer FIRST IDs and ONE integration. No further helper regenerated originals; producer owns all real fixes and full actual patches.

## Complete producer join interfaces

```lean
private theorem actualInheritedCollar {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O)
    (hqO : I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
      InheritedCollar (SourceActualFoldTorus.actualTorusField hL.ne' omega)
        (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) O rho phi

private theorem transportClosedUpper {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (h : InheritedCollar F q O rho phi) (eps : ℝ) (heps : 0 < eps)
    (hg : ClosedBranchFacts rho eps) : UpperClause F q phi eps

private theorem actualUniformSaddleCuts {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O)
    (hqO : I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
      UniformCutResult (SourceActualFoldTorus.actualTorusField hL.ne' omega)
        (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) O rho phi

private theorem cutoffEquality {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (hrho : 0 < rho)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (h : UniformCutResult F q O rho phi) : CutoffEquality F q rho phi
```

Exactly ONE syntactic internal call to PUBLIC64 `I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar` occurs in actualInheritedCollar. Only its PUBLIC statement is consumed. Project its SAME rho/phi, exact ordered field identity and ALL delta lower traces unchanged. No second call/shrink/rechoice, no 64 private proof/helper/fixture/ordinary code, no normal-form or lower-star/no-cross proof. Upper no-cross is derived by Ueps⊆strict trace and PUBLIC64 strict_test; same-sign connections are new finite geometry transported by the actual inverse map.

## Exact sole public statement, no private aliases in type

```lean
theorem actualSource_quotient_saddle_uniform_closed_uppercuts {L : ℝ} (hL : 0 < L)
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
          (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | c-delta ≤ F z})) ∧
          0 < rho^2/4 ∧
          (∀ eps : ℝ, 0 < eps → eps < rho^2/4 →
            let U := phi.source ∩ {z | c+eps ≤ F z}
            let Bplus := U ∩ {z | 0 < phi z 1}
            let Bminus := U ∩ {z | phi z 1 < 0}
            IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
              U = Bplus ∪ Bminus ∧
              (∀ p ∈ U, ∀ r ∈ U, JoinedIn U p r ↔ 0 < (phi p 1)*(phi r 1)))
```

Only this public Prop theorem; public data/global instances0. Standard axioms only propext/Quot.sound/Classical.choice; no admissions/customaxioms/native_decide/implemented_by/full Mathlib umbrella. No global hm, no desired chart premise, no chart canonical equality, no branchmerger/lowerseparation/elder/countprobability claim.

## Complete actual finite fixture definitions and consumers

```lean
private def fixturePoly : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, Pi.single (0 : Fin 2) 1, 0⟩, ⟨2, Pi.single (1 : Fin 2) 1, 0⟩]
private def fixtureSample : I4SmoothCarrier.SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 fixturePoly)
    (I4SourceSmoothConditional.zeroSample 2 2)
private def fixturePoint (x y : ℝ) : UniversalLaw.Spec.Lifetime.E 2 :=
  (I4LifetimeField.coordinates 2).symm ![x,y]
private def fixtureCenter (x y : ℝ) : I4Torus.SourceTorus 2 2 :=
  I4Torus.torusProjection 2 2 ![x,y]
private def fixtureOpen (x y : ℝ) : Set (I4Torus.SourceTorus 2 2) :=
  I4Torus.torusProjection 2 2 '' (I4LifetimeField.coordinates 2 ''
    Metric.ball (fixturePoint x y) (1/8))
private def fixtureField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample

private theorem fixture_field (u : Fin 2 → ℝ) :
    fixtureField (I4Torus.torusProjection 2 2 u) =
      Real.cos (Real.pi*u 0) + 2*Real.cos (Real.pi*u 1)
private theorem fixture_positive_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 1 0)
private theorem fixture_positive_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 1 0) 1
private theorem fixture_negative_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 0 1)
private theorem fixture_negative_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 0 1) 1
private theorem fixture_seam_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint (-1) 0)
private theorem fixture_seam_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint (-1) 0) 1
private theorem fixture_heights : fixtureField (fixtureCenter 1 0) = 1 ∧
    fixtureField (fixtureCenter 0 1) = -1 ∧ fixtureField (fixtureCenter (-1) 0) = 1
private theorem fixture_open (x y : ℝ) : IsOpen (fixtureOpen x y) ∧
    fixtureCenter x y ∈ fixtureOpen x y
private theorem fixture_seam : fixtureCenter (-1) 0 = fixtureCenter 1 0
private theorem fixture_positive_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 1 0) (fixtureOpen 1 0) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter 1 0) rho phi
private theorem fixture_negative_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 0 1) (fixtureOpen 0 1) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter 0 1) rho phi
private theorem fixture_seam_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter (-1) 0) (fixtureOpen (-1) 0) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter (-1) 0) rho phi
```

Full actual HessianHasInertia includes complementary finite dimensions and strict negative/positive subspaces; derive all fields freshly through public finite-source/actual-derivative APIs. No assumed saddle certificate, no hm and no old private fixture text. Same source, literal period2 and cosine1/2 field for production/ordinary. Small O is the actual projected PHYSICAL E2 ball1/8, transported by coordinates as a homeomorphism without an isometry claim. Equality examples eps*=rho²/16 use inverse ±rho/4 and prove EXACT field equality and CLOSED-cut membership, not merely strict-above examples.

## Complete ordinary witness/zero-path/mutation contract

Ordinary uses its own same common definitions and fresh actual fixture proofs, plus these literal definitions/signatures in its namespace. `ordinary_positive_consumer`, `ordinary_negative_consumer`, `ordinary_seam_consumer` have EXACTLY the three corresponding fixture consumer types above, with ordinary-owned names, and each consumes the NEW public65 theorem. No ordinary importing private production APIs, source concatenation or old control binary/body.

```lean
private def ordinaryChosen :
    {rho : ℝ // 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 1 0) (fixtureOpen 1 0) rho phi}
private def chosenRho : ℝ := ordinaryChosen.val
private def chosenPhi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2 :=
  Classical.choose ordinaryChosen.property.2
private def chosenCenter : I4Torus.SourceTorus 2 2 := fixtureCenter 1 0
private def chosenBound : ℝ := chosenRho^2/4
private def chosenTrace (eps : ℝ) : Set (I4Torus.SourceTorus 2 2) :=
  upperTrace fixtureField chosenCenter chosenPhi eps
private def plusPoint : I4Torus.SourceTorus 2 2 := chosenPhi.symm (![0,chosenRho/2] : Point2)
private def minusPoint : I4Torus.SourceTorus 2 2 := chosenPhi.symm (![0,-chosenRho/2] : Point2)
private def boundaryTargetPoint (t : unitInterval) : Point2 :=
  ![0, (1-2*(t : ℝ))*chosenRho/2]
def nonnegativeUpperMutation : Prop :=
  ∀ eps : ℝ, 0 ≤ eps → eps < chosenBound → UpperClause fixtureField chosenCenter chosenPhi eps

private theorem chosen_positive : 0 < chosenRho
private theorem chosen_structural : chosenCenter ∈ chosenPhi.source ∧
    chosenPhi chosenCenter = 0 ∧ chosenPhi.source ⊆ fixtureOpen 1 0 ∧
    chosenPhi.target = Metric.ball 0 chosenRho ∧
    ∀ z ∈ chosenPhi.source, fixtureField z = fixtureField chosenCenter -
      (chosenPhi z 0)^2 + (chosenPhi z 1)^2
private theorem boundaryTargetPoint_mem (t : unitInterval) :
    boundaryTargetPoint t ∈ chosenPhi.target
private def boundaryPath : Path plusPoint minusPoint
private theorem boundaryPath_formula (t : unitInterval) :
    boundaryPath t = chosenPhi.symm (boundaryTargetPoint t)
private theorem boundaryPath_source (t : unitInterval) : boundaryPath t ∈ chosenPhi.source
private theorem boundaryPath_coordinates (t : unitInterval) :
    chosenPhi (boundaryPath t) = boundaryTargetPoint t
private theorem boundaryPath_zero_cut (t : unitInterval) : boundaryPath t ∈ chosenTrace 0
private theorem boundaryPath_midpoint :
    boundaryPath ⟨(1/2 : ℝ), by constructor <;> norm_num⟩ = chosenCenter
private theorem boundary_joined : JoinedIn (chosenTrace 0) plusPoint minusPoint
private theorem boundary_endpoint_product :
    (chosenPhi plusPoint 1)*(chosenPhi minusPoint 1) = -chosenRho^2/4
private theorem ordinary_cutoff_equality : CutoffEquality fixtureField chosenCenter chosenRho chosenPhi
theorem nonnegativeUpperMutation_false : ¬ nonnegativeUpperMutation
```

The zero counterproof consumes ONLY chosen_positive/chosen_structural and actual inverse geometry, never production upper-branch facts, inherited lower_pc, or a second public64 call. Full vertical target segment stays in ball, inverse continuous on that target segment, every time is in actualsource/CLOSED zero cut, midpoint is actual q, endpoints ±rho/2 have negative sign product. Thus actual JoinedIn contradicts mutated iff at eps0. Same chosen phi/source/rho/field/CLOSEDcut and upper bound; ONLY mutation is `0 < eps`→`0 ≤ eps`. No bound-removal or other negative. The sole False harness imports ONLY the actually passed ordinary module and applies its independently proved nonnegativeUpperMutation_false to the one deliberately false mutation premise/statement. No concatenation/private foreign names/second mutation.

## Execution, inventory and immutable custody

Before first important worker: freeze this complete context and initial runner/outer-entry scripts. Every actual run has label/scope, command/argv/cwd/start/end/elapsed/exit, initial and affected versions/full actual patches, before/after source/object/context/runner bindings and FULL separate original stdout/stderr. Capture inner worker AND enclosing outer AND driver-entry streams from FIRST invocation. No invented UTC or replay to repair a missing capture. New payload identities once, known identical copied context/import/source/runner IDs reused with actual snapshot mappings. Original helper text frozen+FIRST IDs before exactly ONE integration; all later actual amendments producer-owned. Root/helper ACKs use observed actual UTC only. Original artifacts never regenerated after freeze.

Initial milestone is COMPLETE closedSaddleBranchGeometry in actual frozen context, no isolated name/API/partial probe. Then full actual production transport/fixtures. New strict Werror finalsource compile once per actual change, dynamic exact-own-module-index inventory ALL new constants including private propositions/bundles/data/generated and separate foreign-generated classification, recursive standard3 axiom streams; source-review early PASS before exactly ONE final named-own-module kernel. No partial/helper kernels. Completed checks on unchanged material reused.

NEW explicit ordinary obligation: AFTER ordinary strict PASS, BEFORE soleFalse, run a SEPARATE ordinary-owned-module-index inventory of EVERY new ordinary mathematical constant (public/private/data/Propbundles/generated/foreign-generated), exhaustive classification and recursive standard3 axiom qualification. Parameterize generic module-index collector by actual ordinary module/object/import only. Source65 inventory/kernel does not qualify ordinary. NO ordinary named kernel. Dynamic actual source AND ordinary counts, never96 guessed. Then exactlyONE negative harness, expected exit1 and exactlyONE False/empty stderr, with exact passing ordinary source/object/receipt binding. All failed new attempts/full streams retained honestly. Ordinary False is after its counterproof and inventory PASS, not a source result.

Prospective runner/outer/entry capture is mandatory for documentary/metadata workers too. Final docwriter receipt closes AFTER it writes index: actual additive closure/index+allowlist addenda after run; no recursive self-ID and no replay generator. Cached FIRST IDs for new outputs; known copies reuse existing IDs. Root final FULLdocs reading→reviewer final custody→root FINAL_GO→root-only one metadata attempt/apply/push; producer no shared edits/copy/Git/external. Root sole new eligible65 own object copiedONCE after cut, all further copies SKIP. Existing64 object/check/CI/hash/copy never replayed. Provider/process review tracked separately; scienceNONE/samefamily0. B is a proof-text author, reviewer has no65proof authorship.

Deadline CP21:20UTC, HARD23:30UTC28October or invocation end, no autoextension. Report actual obstruction/status honestly. Future66 is no source dependency/role/code/GO. Original downstream goal remains unmet beyond this bounded local result.

## Amendment002: ordinary public mutation interface and reused64 lineage

The ordinary `nonnegativeUpperMutation` Prop definition is PUBLIC within ActualSaddleUppercutsControls. Thus the sole importing-only False harness can name the precise false premise using public APIs. All production names/privacy/output and the sole mutation remain unchanged. Ordinary `nonnegativeUpperMutation_false` is public as already stated. B geometry has no dependent change; personal FULL001 reading plus entire002delta ACK before proof text.

Qualified PUBLIC64 lineage is REUSED, never rechecked/rehashed/copied: published normal head ee5b141d5ff41a0a9040256a8025690ec22d7266; source-only cut57f73698fb84efd56166fda57639557794312754, parentf4825c3e3bd0e2d2c46157096e76b9ab17dbbb71; source40252B SHAe0e0a0f77bd75bbbd8994d620ee43b18b2edd50d7649cd8cb9837e7148762265, Gitblob39bce1145fcd714b049bfd4ec941390a0b286f10; ownobject1654224B SHAa57489eb917c4f2fd4d314ab5f7ae9dea60619caf9160e044700114551c1e15e. Root canonical eligible64 copy occurred ONCE20:25:01.660046; all further copies SKIP. Existing authoritative /workspace/scratch/actual-source-quotient-saddle-collar-publication/ROOT_SOURCE_CUT.json and ROOT_OWN_OBJECT_COPY.json bind these known identities. All prior64 mathematical and metadata checks/full nonauthor review and all4CI SUCCESS already completed; no new65 session/process reason changes that evidence.

## Amendment003: literal physical small neighborhood

The fixtureOpen definition now retains ROOT_GO's exact projected PHYSICAL E2 ball of radius1/8, first mapped by the actual coordinates map and then the torus projection. The earlier Pi-ball shape is historical001/002 only. This corrects the concrete reviewer GO/context alignment finding. No isometry, norm equality, public/math/geometry interface, control mutation or helper scope changes. Full earlier context reading plus entire003delta is the effective preTEXT context.

## Amendment004: sole closed assertion harness, no assumed mutation

The sole importing-only negative is a CLOSED assertion of the ordinary PUBLIC nonnegativeUpperMutation with NO mutation hypothesis, axiom, parameter, local assumed proof or supplied certificate. The independently passed negation rewrites the asserted proposition to the intended ONE unsolved False. Its COMPLETE planned literal text is:

```lean
import SaddleUppercutsControls

example : ActualSaddleUppercutsControls.nonnegativeUpperMutation := by
  rw [show ActualSaddleUppercutsControls.nonnegativeUpperMutation ↔ False from
    ⟨ActualSaddleUppercutsControls.nonnegativeUpperMutation_false, fun h => h.elim⟩]
```

The actual complete harness, FIRST identity and pre-run immutable snapshot are frozen BEFORE its exactly ONE invocation, AFTER ordinary strict PASS and its separate ALL-owned-ID/std3 inventory PASS. Expected exit1, ONE unsolved False, empty stderr. Earlier001 prose about applying negation to a false mutation premise is superseded by this exact no-premise assertion; all historical bytes remain immutable. No B geometry/header/interface, production theorem, mutation, positive/counterproof or verification-count change. No further speculative context changes.
