# Frozen complete shared context62 — producer personal GO ACK

Producer personally FULLREAD actual ROOT_GO.json and adopted CONTROL_CONTRACT.md before62 code/harness/helper text. Pickup6475693627 actual17:16:11UTC28October2026/fullMATCH17:16:25; GO17:19:28.323257; checkpoint17:45; hard19:00UTC or invocation end, no extension. Root accepts the pre-GO typed proposals. This context makes all abbreviations actual typed PRIVATE Lean declarations, not display metavariables. Exactly one authored public Prop/no public data. Main ownership is the new SourceActualTorusRegularSlab.lean and this construct scratch; root alone shared metadata/cache/Git/external/canonical object placement. No61 source/private/helper/dependency or repeated old check.

Every helper personally FULLREADs this SAME complete document and ACKs with actual observed UTC/ordering before ANY proof text. All3 are TEXT ONLY: zero Lean/probes/checks/kernels/controls/hashes/objects/Git/cache/external. Each COMPLETE original freezes before ONE integration, producer firstIDs and all actual amendments. No fourth helper/ordinary Controls delegation. Main producer owns every execution/amendment, zero/empty/quotient/components/public/fixtures/Controls. No partial kernel. Initial producer check, if needed, covers WHOLE actual normalizedFieldData section in this source context, not names/probes.

Read accepted materials (readings already completed remain reusable):
- /workspace/scratch/actual-source-regular-slab-publication/SOURCE_ACTUAL_TORUS_REGULAR_SLAB.md
- same publication SOURCE_ACTUAL_TORUS_REGULAR_SLAB_PLAN.md and _CONTROLS.md and _CONTENDERS.json
- /workspace/scratch/actual-source-regular-slab-preflight/REPORT.md (exact API quotes)
- /workspace/scratch/actual-source-regular-slab-source-review/PREFLIGHT.md
- /workspace/scratch/actual-source-regular-slab-precode-review/REPORT.md
- /workspace/scratch/canonical-component-event-api-preflight/ACTUAL_API_REUSE_MAP.md

## Literal production header

```lean
import SourceConditionalMajorant
import SourceActualFoldTorus
import SourceFiniteTrig
import SourceSmoothConditionalKernel
import ClosedSuperlevel
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.Dual
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.ExistUnique
import Mathlib.Analysis.Normed.Field.Basic
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Topology.Maps.Basic
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Positivity
import Lean.Elab.Tactic.Omega

noncomputable section
open Set Filter
open I4SmoothCarrier I4LifetimeField
open UniversalLaw.Spec.Lifetime
open scoped Topology BigOperators Matrix
set_option autoImplicit false
namespace I4SourceActualTorusRegularSlab
```

ClosedSuperlevel is the accepted inputs/elder/ClosedSuperlevel.lean binding, root verified by public import read, not a probe. No umbrellaMathlib/Flow/dynamics/59/60/61. No open scoped ContDiff; binder spelling omega. Physical E2 is Euclidean; Pi source coordinates have Pi/sup norm. Keep literal coordinates2 operator norms in bounds; inverse Riesz isometry concerns E2/its dual only.

## Exact common producer-owned PRIVATE definitions

These are actual Lean declarations, before all helper sections. All helper sections omit imports/namespace/end and contain ONLY private new declarations. No helper may regenerate these shared definitions or change their types silently.

```lean
private abbrev E2 := UniversalLaw.Spec.Lifetime.E 2

private def normalizedVelocity (g : E2 → ℝ) (c : ℝ) (X : E2) : E2 :=
  (max c (‖gradient g X‖ ^ 2))⁻¹ • gradient g X

private abbrev CoverSuperlevel {L : ℝ} (omega : SmoothSample 2 L) (a : ℝ) :=
  {X : E2 | a ≤ actualField 2 L omega X}

private abbrev TorusSuperlevel {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :=
  {q : I4Torus.SourceTorus 2 L |
    a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega q}

private def coverProjection (L : ℝ) (X : E2) : I4Torus.SourceTorus 2 L :=
  I4Torus.torusProjection 2 L (coordinates 2 X)

private def NormalizedFieldFacts {L : ℝ} (omega : SmoothSample 2 L)
    (a b c A : ℝ) (Kp M K : ℝ≥0) : Prop :=
  let g := actualField 2 L omega
  let p := gradient g
  let V := normalizedVelocity g c
  0 < c ∧ 0 ≤ A ∧
    (∀ X : E2, ‖p X‖ ≤ A) ∧ LipschitzWith Kp p ∧
    (∀ (X : E2) (n : Fin 2 → ℤ), p (X + latticeVec 2 L n) = p X) ∧
    (∀ X : E2, a ≤ g X → g X ≤ b → c ≤ ‖p X‖ ^ 2) ∧
    (∀ X : E2, ‖V X‖ ≤ (M : ℝ)) ∧ LipschitzWith K V ∧
    (∀ (X : E2) (n : Fin 2 → ℤ), V (X + latticeVec 2 L n) = V X) ∧
    (∀ X : E2, fderiv ℝ g X (V X) = ‖p X‖ ^ 2 / max c (‖p X‖ ^ 2)) ∧
    (∀ X : E2, 0 ≤ fderiv ℝ g X (V X) ∧ fderiv ℝ g X (V X) ≤ 1) ∧
    (∀ X : E2, a ≤ g X → g X ≤ b → fderiv ℝ g X (V X) = 1)

private def FiniteHorizonFacts (L : ℝ) (V : E2 → E2) (T : ℝ)
    (H : ℝ → E2 → E2) : Prop :=
  (∀ X : E2, H 0 X = X) ∧
    ContinuousOn (fun z : E2 × ℝ => H z.2 z.1)
      (Set.univ ×ˢ Set.Icc (0 : ℝ) T) ∧
    (∀ (X : E2) (t : ℝ), t ∈ Set.Icc (0 : ℝ) T →
      HasDerivAt (fun u => H u X) (V (H t X)) t) ∧
    (∀ t : ℝ, t ∈ Set.Icc (0 : ℝ) T → ∀ (X : E2) (n : Fin 2 → ℤ),
      H t (X + latticeVec 2 L n) = H t X + latticeVec 2 L n)

private def HeightHittingFacts {L : ℝ} (omega : SmoothSample 2 L)
    (a b : ℝ) (hab : a ≤ b) (H : ℝ → E2 → E2)
    (Rcover : CoverSuperlevel omega a → CoverSuperlevel omega b) : Prop :=
  let g := actualField 2 L omega
  (∀ (X : E2) (t : ℝ), t ∈ Set.Icc (0 : ℝ) (b-a) →
    g X ≤ g (H t X) ∧ g (H t X) ≤ g X + t) ∧
  (∀ X : E2, a ≤ g X → g X ≤ b → ∀ t : ℝ, 0 ≤ t → t ≤ b-g X →
    g (H t X) = g X + t) ∧
  Continuous Rcover ∧
  (∀ X : CoverSuperlevel omega a,
    (Rcover X).val = H (max 0 (b-g X.val)) X.val) ∧
  (∀ X : CoverSuperlevel omega b,
    Rcover ⟨X.val, hab.trans X.property⟩ = X) ∧
  (∀ X : CoverSuperlevel omega a,
    JoinedIn {Y : E2 | a ≤ g Y} X.val (Rcover X).val) ∧
  (∀ X Y : CoverSuperlevel omega a, ∀ n : Fin 2 → ℤ,
    Y.val = X.val + latticeVec 2 L n →
    (Rcover Y).val = (Rcover X).val + latticeVec 2 L n)
```

Private Prop bundles expose every finite clause. They are proved outputs/internal structural inputs only, never desired final endpoint premises. Final public declaration spells literal objects without any private alias.

## Exact THREE helper-owned private theorem signatures

Signatures below are not proof bodies. Helper A owns every needed PRIVATE actual-source bound/periodicity/compact-cell/floor/max/reciprocal lemma through normalizedFieldData. Root selects old public Fourier upper bounds with actual operator-norm factors, compact CLOSED physical-cell squared floor; not a duplicate compact-upper-bound campaign.

```lean
private theorem normalizedFieldData {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hreg : ∀ X : E2, a ≤ actualField 2 L omega X →
      actualField 2 L omega X ≤ b → fderiv ℝ (actualField 2 L omega) X ≠ 0)
    (hne : ∃ X : E2, a ≤ actualField 2 L omega X ∧ actualField 2 L omega X ≤ b) :
    ∃ c A : ℝ, ∃ Kp M K : ℝ≥0, NormalizedFieldFacts omega a b c A Kp M K

private theorem boundedFiniteHorizonFamily {L : ℝ} (V : E2 → E2) (M K : ℝ≥0)
    (hbound : ∀ X : E2, ‖V X‖ ≤ (M : ℝ)) (hlip : LipschitzWith K V)
    (hper : ∀ (X : E2) (n : Fin 2 → ℤ), V (X + latticeVec 2 L n) = V X)
    (T : ℝ) (hT : 0 ≤ T) :
    ∃ H : ℝ → E2 → E2, FiniteHorizonFacts L V T H

private theorem heightHittingData {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (c A : ℝ) (Kp M K : ℝ≥0) (H : ℝ → E2 → E2)
    (hfield : NormalizedFieldFacts omega a b c A Kp M K)
    (hfamily : FiniteHorizonFacts L
      (normalizedVelocity (actualField 2 L omega) c) (b-a) H) :
    ∃ Rcover : CoverSuperlevel omega a → CoverSuperlevel omega b,
      HeightHittingFacts omega a b hab H Rcover
```

A's nonempty-band premise is ONLY internal branch data, not public input. B is ANY finite T≥0 with direct symmetric[-T−1,T+1] Picard, initialradius1/outer1+M*(T+1), center-family uniqueness patch and full derivatives at0/T. No K*time smallness, finite-N machinery or group law. C proves global barriers BEFORE residence, all intermediate[0,t] band membership before unit-speed arrival, τ=max0(b−gX) on lower subtype, continuous Rcover, actual point paths and lattice equivariance. No assumed no-exit/retraction/component certificate.

## Exact producer-owned join signatures

The restricted function is defined by producer before these join declarations, with underlying value exactly coverProjection L X.val and subtype proof solely from actualTorusField_pullback. This declaration's signature, not a helper-proof premise:

```lean
private def restrictedProjection {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    CoverSuperlevel omega a → TorusSuperlevel hL omega a

private theorem zeroWidth_componentBijective {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -a) (t := -a) (neg_le_neg (le_refl a)))

private theorem emptyBand_componentBijective {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hempty : ∀ X : E2, ¬ (a ≤ actualField 2 L omega X ∧ actualField 2 L omega X ≤ b)) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab))

private theorem restrictedProjectionQuotient {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    Continuous (restrictedProjection hL omega a) ∧
      IsOpenMap (restrictedProjection hL omega a) ∧
      Function.Surjective (restrictedProjection hL omega a) ∧
      Topology.IsQuotientMap (restrictedProjection hL omega a)

private theorem descendedHittingData {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (H : ℝ → E2 → E2)
    (Rcover : CoverSuperlevel omega a → CoverSuperlevel omega b)
    (hcover : HeightHittingFacts omega a b hab H Rcover) :
    ∃ R : TorusSuperlevel hL omega a → TorusSuperlevel hL omega b,
      Continuous R ∧
      (∀ q : TorusSuperlevel hL omega b, R ⟨q.val, hab.trans q.property⟩ = q) ∧
      (∀ q : TorusSuperlevel hL omega a,
        JoinedIn {z : I4Torus.SourceTorus 2 L |
          a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z} q.val (R q).val) ∧
      (∀ X : CoverSuperlevel omega a,
        R (restrictedProjection hL omega a X) = restrictedProjection hL omega b (Rcover X))

private theorem closedBand_componentBijective_core {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hreg : ∀ X : E2, a ≤ actualField 2 L omega X →
      actualField 2 L omega X ≤ b → fderiv ℝ (actualField 2 L omega) X ≠ 0) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab))
```

Main derives literal product-projection equality→actual integer-lattice difference from old public AddCircle APIs, then fiber independence from C equivariance. Restricted openness uses SATURATED full preimage and actual relative-open image identity; no unjustified arbitrary quotient restriction. Actual point paths suffice; no global quotient flow/homotopy. The component argument proves THIS existing map bijective, not an unrelated equivalence.

## Sole public declaration

```lean
theorem actualSource_closedSlab_componentInclusion_bijective
    {L : ℝ} (hL : 0 < L) (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hreg : ∀ X : UniversalLaw.Spec.Lifetime.E 2,
      a ≤ I4LifetimeField.actualField 2 L omega X →
      I4LifetimeField.actualField 2 L omega X ≤ b →
      fderiv ℝ (I4LifetimeField.actualField 2 L omega) X ≠ 0) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab))
```

Only this authored public proposition; no public definitions/data/instances/auxiliary theorem/generic engine. No private alias leaks into this type; no supplied floor/flow/retract/component conclusion. No IsMorseDistinct/probability/critical-count premise. CLOSED hreg includes both endpoints.

## Exact primary/auxiliary fixture bindings and production consumers

Old PUBLIC I4SourceFiniteTrig.TrigPoly/TrigTerm coeff:ℝ, frequency:Fin2→ℤ, offset:ℝ; toSource(L:ℝ)(p:TrigPoly):I4Source.SourceMode2→₀ℝ includes actual Fourier normalization. PUBLIC I4SourceFinitePinKernel.finiteShiftSample v omega and I4SourceSmoothConditional.zeroSample d L preserve original SmoothSample carrier.

Producer-owned PRIVATE definitions (later ordinary namespace reconstructs SAME formulas independently of private names):

```lean
private def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, ![(2 : ℤ), 0], 0⟩, ⟨(1/2 : ℝ), ![(0 : ℤ), 1], 0⟩]
private def fixtureSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)
private def fixturePoint (x y : ℝ) : E2 := (coordinates 2).symm ![x,y]
```

Exact producer-owned PRIVATE facts/consumer endpoints:

```lean
private theorem fixture_actualField (X : E2) :
    actualField 2 2 fixtureSample X =
      Real.cos (2*Real.pi*X 0) + (1/2 : ℝ)*Real.cos (Real.pi*X 1)
private theorem fixture_criticalHeights (X : E2)
    (hc : IsCriticalPoint 2 (actualField 2 2 fixtureSample) X) :
    actualField 2 2 fixtureSample X ∈ ({3/2,1/2,-1/2,-3/2} : Set ℝ)
private theorem fixture_fieldBounds (X : E2) :
    (-3/2 : ℝ) ≤ actualField 2 2 fixtureSample X ∧ actualField 2 2 fixtureSample X ≤ 3/2
private theorem fixture_closedRegular_noCritical (X : E2)
    (ha : (0 : ℝ) ≤ actualField 2 2 fixtureSample X)
    (hb : actualField 2 2 fixtureSample X ≤ 1/4) :
    fderiv ℝ (actualField 2 2 fixtureSample) X ≠ 0
private theorem fixture_closedRegular :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
      (s := -(1/4 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (by norm_num : (0 : ℝ) ≤ 1/4)))
private theorem fixture_zeroWidth :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
      (s := -(0 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (le_refl (0 : ℝ))))
private theorem fixture_emptyBand :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
      (s := -(-2 : ℝ)) (t := -(-3 : ℝ)) (neg_le_neg (by norm_num : (-3 : ℝ) ≤ -2)))
private theorem fixture_emptyBand_whole_nonempty :
    TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (2 : ℝ) = Set.univ ∧
    TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (3 : ℝ) = Set.univ ∧
    (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (2 : ℝ)).Nonempty
```

Private actual descended-field bounds are derived from fixture_fieldBounds and exact pullback. The regular band has actual witness fixturePoint(1/4)(1/2) with field0. fixture_closedRegular explicitly instantiates derived normalizedFieldData and boundedFiniteHorizonFamily as well as the actual core; no supplied desired c/H. ZeroWidth and emptyBand exercise their distinct private branches. Empty-band levels are WHOLE NONEMPTY torus, not an empty-domain convention. All fixture facts once per privacy scope, no61 fixture/proof copy.

## Separate ordinary Controls and sole negative

Producer ONLY; no fourth helper. Ordinary file TorusRegularSlabControls.lean: imports first `SourceActualTorusRegularSlab`, then the SAME old-public imports above; same noncomputable/open/scoped/autoImplicit header, `namespace TorusRegularSlabControls`. It contains NO production-private aliases/definitions/calls and no source concatenation. Reconstructs identical fixture formulas, proves actual field/critical heights/bounds once in ordinary scope; invokes sole public endpoint at [0,1/4], [0,0],[-3,-2], with whole-nonempty empty-band fact.

Ordinary auxiliary polynomial EXACT [⟨1,![(1:ℤ),0],0⟩], same old toSource2/finiteShift/zeroSample22 route; separator H is its actualTorusField with continuous/pullback cos(πx). No auxiliary y. Primary F fixed everywhere; primary_le_separator says ∀q,Fq≤2*(Hq)^2−1/2. mutant_a=−1/2,mutant_b=0; openBand_noCritical derives actual fderiv≠0 on the OPEN band from critical heights. upperPoint0/1 are subtype members of literal closed F≥0 represented by physical(0,0)/(1,0); upperClasses_ne via H/IVT; lowerImages_eq via actual lower projected horizontal path and EXISTING inclusion. Then exact map noninjective/nonbijective.

`openBandVariantAtFixture` is exactly `(∀X:E2, (−1/2:ℝ)<gX → gX<(0:ℝ) → fderiv ℝ g X≠0) → Function.Bijective (TorusFiltration.superlevel_componentInclusion F (s:=-(0:ℝ)) (t:=-(-1/2:ℝ)) (neg_le_neg (by norm_num : (-1/2:ℝ)≤0)))`. Both superlevel traces remain CLOSED. not_openBandVariantAtFixture proves its negation using the already TRUE open-band premise and independently proved collision. No extra mutation/emptydomain/countatlas claim. One future negative is authored ONLY AFTER complete ordinary Controls PASS; imports ONLY passed ordinary object and falsely asserts openBandVariantAtFixture, reduced by its passed negation to one mathematical False. No name/private/time/carrier failure qualifies.

## Original delivery/custody

A `/root/remote_jet_gaussian_construct`: /workspace/scratch/actual-source-regular-slab-normalized-field-text/NormalizedSection.ORIGINAL.lean.txt
B `/root/actual_canonical_capture_application`: /workspace/scratch/actual-source-regular-slab-finite-horizon-text/FiniteHorizonSection.ORIGINAL.lean.txt
C `/root/actual_canonical_partner_preflight`: /workspace/scratch/actual-source-regular-slab-height-hitting-text/HeightHittingSection.ORIGINAL.lean.txt

Each supplies one COMPLETE private production section plus immutable original full context/imports/provenance/freeze notice, no source/harness execution/hash. Producer retains FIRST IDs before ONE integration and full actual patches after. Never regenerate originals after integration. No helper objects or standalone helper checks. All3 receive this SAME full context; mathematical interface dependencies do not imply already qualified proofs.

Initial runner/fullcontext MUST be snapshotted before first actual run. Before ANY runner/context change preserve oldversion plus full exact patch; every real run retains source/harness/runner/context snapshots, complete separate original stdout/stderr, commands/cwd/actual UTC start/end/exit and owned firstIDs. Reuse completed applicable verification; no source61 check/copy/hash/math replay for this new session/scope. Root only eligible OWN final object placement after complete qualification, exactly once; no partial kernel/cache promotion. No admissions/customaxioms/native_decide/implemented_by/foreign-private or generated APIs/fullMathlibumbrella. Allowed standard axioms propext/Classical.choice/Quot.sound. Provider-distinct process separate, same-family0/scienceNONE.
