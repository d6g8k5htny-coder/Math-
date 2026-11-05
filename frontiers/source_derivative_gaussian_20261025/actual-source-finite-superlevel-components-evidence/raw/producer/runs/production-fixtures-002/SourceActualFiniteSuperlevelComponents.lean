import SourceActualTorusSuperlevelLocalBasis
import SourcePinPreservingQuartic
import SourceFiniteTrig
import Mathlib.Topology.Connected.LocallyPathConnected
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Convert
import Lean.Elab.Tactic.Omega

noncomputable section
open Set Filter Topology
open UniversalLaw.Spec.Lifetime
open I4LifetimeField I4SmoothCarrier
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourceActualFiniteSuperlevelComponents

private theorem actualClosedSuperlevel_compact
    {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L) (a : ℝ) :
    CompactSpace (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-a)) := by
  let _ : Fact (0 < L) := ⟨hL⟩
  have hclosed : IsClosed (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-a)) := by
    simpa only [TorusFiltration.superlevel_set, neg_neg] using
      (isClosed_le continuous_const
        (SourceActualFoldTorus.actualTorusField_continuous hL.ne' omega) :
        IsClosed {q | a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega q})
  exact isCompact_iff_compactSpace.mp hclosed.isCompact

/-
Stage63 Helper A: complete original actual public61-to-subtype LP adapter.
Literal input: final common CONTEXT003. No imports/namespace/end/common defs.
Complete unelaborated TEXT only; zero helper Lean/probes/checks/hashes.
-/

private theorem actualClosedSuperlevel_locallyPathConnected
    {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L)
    (hm : UniversalLaw.Spec.Lifetime.IsMorseDistinct 2 L
      (I4LifetimeField.actualField 2 L omega)) (a : ℝ) :
    LocallyPathConnectedSpace (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-a)) := by
  let F : I4Torus.SourceTorus 2 L → ℝ :=
    SourceActualFoldTorus.actualTorusField hL.ne' omega
  let S : Set (I4Torus.SourceTorus 2 L) :=
    TorusFiltration.superlevel_set F (-a)
  have hlevel (y : S) : a ≤ F y.val := by
    have hy : -(-a) ≤ F y.val := y.property
    simpa only [neg_neg] using hy
  change LocallyPathConnectedSpace S
  refine ⟨fun x => ?_⟩
  rw [hasBasis_self]
  intro N hN
  obtain ⟨U, hU, hUN⟩ := (mem_nhds_subtype S x N).1 hN
  obtain ⟨O, hOU, hO, hxO⟩ := mem_nhds_iff.1 hU
  obtain ⟨V, hV, hxV, hVO, hpc⟩ :=
    I4SourceActualTorusSuperlevelLocalBasis.actualSource_torus_closedSuperlevel_localPathConnectedBasis
      hL omega hm a x.val (hlevel x) O hO hxO
  let W : Set S := (Subtype.val : S → I4Torus.SourceTorus 2 L) ⁻¹' V
  have hWopen : IsOpen W := hV.preimage continuous_subtype_val
  have hxW : x ∈ W := hxV
  have hWnhds : W ∈ 𝓝 x := hWopen.mem_nhds hxW
  have hWN : W ⊆ N := by
    intro y hy
    exact hUN (hOU (hVO hy))
  have htrace : V ∩ {z : I4Torus.SourceTorus 2 L | a ≤ F z} ⊆ S := by
    intro z hz
    change -(-a) ≤ F z
    simpa only [neg_neg] using (show a ≤ F z from hz.2)
  have hpreimage :
      (Subtype.val : S → I4Torus.SourceTorus 2 L) ⁻¹'
        (V ∩ {z : I4Torus.SourceTorus 2 L | a ≤ F z}) = W := by
    ext y
    change (y.val ∈ V ∧ a ≤ F y.val) ↔ y.val ∈ V
    exact ⟨And.left, fun hy => ⟨hy, hlevel y⟩⟩
  have hWpc : IsPathConnected W := by
    have hp := hpc.preimage_coe htrace
    rw [hpreimage] at hp
    exact hp
  exact ⟨W, hWnhds, hWpc, hWN⟩


private theorem consumeFiniteClosedSubtype
    {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L) (a : ℝ)
    (hpc : LocallyPathConnectedSpace (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-a))) :
    Finite (ZerothHomotopy (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-a))) := by
  let _ := actualClosedSuperlevel_compact hL omega a
  let _ := hpc
  infer_instance

theorem actualSource_finite_closedSuperlevel_components
    {L : ℝ} (hL : 0 < L) (omega : I4SmoothCarrier.SmoothSample 2 L)
    (hm : UniversalLaw.Spec.Lifetime.IsMorseDistinct 2 L
      (I4LifetimeField.actualField 2 L omega)) :
    ∀ a : ℝ, Finite (ZerothHomotopy (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField hL.ne' omega) (-a))) := by
  intro a
  exact consumeFiniteClosedSubtype hL omega a
    (actualClosedSuperlevel_locallyPathConnected hL omega hm a)

private def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, Pi.single (0 : Fin 2) 1, 0⟩,
   ⟨2, Pi.single (1 : Fin 2) 1, 0⟩]

private def fixtureSample : I4SmoothCarrier.SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)

private def fixtureTorusField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample

private def fixtureProjection (x : Fin 2 → ℝ) : I4Torus.SourceTorus 2 2 :=
  I4Torus.torusProjection 2 2 x

private theorem finiteField_value (p : I4SourceFiniteTrig.TrigPoly)
    (X : UniversalLaw.Spec.Lifetime.E 2) :
    I4LifetimeField.actualField 2 2
      (I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 p)
        (I4SourceSmoothConditional.zeroSample 2 2)) X =
      I4SourceFiniteTrig.eval 2 p (I4LifetimeField.coordinates 2 X) := by
  calc
    _ = I4SourceFinitePinKernel.finitePairing
        (fun m => I4Source.modeCoefficient 2 2 m (I4LifetimeField.coordinates 2 X))
        (I4SourceFiniteTrig.toSource 2 p) := by
      change (∑' m, I4Source.modeCoefficient 2 2 m (I4LifetimeField.coordinates 2 X) *
        ((I4SourceSmoothConditional.zeroSample 2 2).val m +
          I4SourceFiniteTrig.toSource 2 p m)) = _
      simp only [I4SourceSmoothConditional.zeroSample, zero_add]
      unfold I4SourceFinitePinKernel.finitePairing Finsupp.sum
      apply tsum_eq_sum
      intro m hm
      rw [Finsupp.notMem_support_iff.mp hm, mul_zero]
    _ = _ := I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0) p _

private theorem fixture_actualField (X : UniversalLaw.Spec.Lifetime.E 2) :
    I4LifetimeField.actualField 2 2 fixtureSample X =
      Real.cos (Real.pi * I4LifetimeField.coordinates 2 X 0) +
        2 * Real.cos (Real.pi * I4LifetimeField.coordinates 2 X 1) := by
  rw [fixtureSample, finiteField_value]
  norm_num [I4SourceFiniteTrig.eval, I4SourceFiniteTrig.termEval, fixturePolynomial,
    I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two, Pi.single_apply]

private theorem fixture_pullback (x : Fin 2 → ℝ) :
    fixtureTorusField (fixtureProjection x) =
      Real.cos (Real.pi * x 0) + 2 * Real.cos (Real.pi * x 1) := by
  unfold fixtureTorusField fixtureProjection
  rw [SourceActualFoldTorus.actualTorusField_pullback]
  simpa only [I4LifetimeField.actualField, ContinuousLinearEquiv.apply_symm_apply] using
    fixture_actualField ((I4LifetimeField.coordinates 2).symm x)

private theorem fixture_fieldBounds (q : I4Torus.SourceTorus 2 2) :
    -3 ≤ fixtureTorusField q ∧ fixtureTorusField q ≤ 3 := by
  rcases SourceActualFoldTorus.torusProjection2L_surjective 2 q with ⟨x, rfl⟩
  change -3 ≤ fixtureTorusField (fixtureProjection x) ∧
    fixtureTorusField (fixtureProjection x) ≤ 3
  rw [fixture_pullback]
  constructor <;> linarith [Real.neg_one_le_cos (Real.pi * x 0),
    Real.neg_one_le_cos (Real.pi * x 1), Real.cos_le_one (Real.pi * x 0),
    Real.cos_le_one (Real.pi * x 1)]

private theorem coordinate_max_zero {x : ℝ} (hx : Real.cos (Real.pi * x) = 1) :
    (x : AddCircle (2 : ℝ)) = 0 := by
  rcases (Real.cos_eq_one_iff _).mp hx with ⟨k, hk⟩
  apply (AddCircle.coe_eq_zero_iff (2 : ℝ)).mpr
  refine ⟨k, ?_⟩
  rw [zsmul_eq_mul]
  apply (mul_left_cancel₀ Real.pi_ne_zero)
  nlinarith

private theorem fixture_maxLevel :
    TorusFiltration.superlevel_set fixtureTorusField (-3) = {fixtureProjection 0} := by
  ext q
  constructor
  · intro hq
    change -(-3 : ℝ) ≤ fixtureTorusField q at hq
    rcases SourceActualFoldTorus.torusProjection2L_surjective 2 q with ⟨x, rfl⟩
    change -(-3 : ℝ) ≤ fixtureTorusField (fixtureProjection x) at hq
    rw [fixture_pullback] at hq
    have hx0 : Real.cos (Real.pi * x 0) = 1 := by
      linarith [Real.cos_le_one (Real.pi * x 0), Real.cos_le_one (Real.pi * x 1)]
    have hx1 : Real.cos (Real.pi * x 1) = 1 := by
      linarith [Real.cos_le_one (Real.pi * x 0), Real.cos_le_one (Real.pi * x 1)]
    apply Set.mem_singleton_iff.mpr
    funext i
    fin_cases i
    · simpa only [fixtureProjection, I4Torus.torusProjection, Pi.zero_apply, AddCircle.coe_zero]
        using coordinate_max_zero hx0
    · simpa only [fixtureProjection, I4Torus.torusProjection, Pi.zero_apply, AddCircle.coe_zero]
        using coordinate_max_zero hx1
  · rintro rfl
    change -(-3 : ℝ) ≤ fixtureTorusField (fixtureProjection 0)
    rw [fixture_pullback]
    norm_num

private theorem fixture_emptyLevel :
    TorusFiltration.superlevel_set fixtureTorusField (-4) = ∅ := by
  ext q
  simp only [Set.mem_empty_iff_false, iff_false]
  change ¬ -(-4 : ℝ) ≤ fixtureTorusField q
  linarith [(fixture_fieldBounds q).2]

private theorem fixture_wholeLevel :
    TorusFiltration.superlevel_set fixtureTorusField 4 = Set.univ := by
  ext q
  simp only [Set.mem_univ, iff_true]
  change -(4 : ℝ) ≤ fixtureTorusField q
  linarith [(fixture_fieldBounds q).1]

private theorem fixture_whole_nonempty :
    Nonempty (TorusFiltration.superlevel_set fixtureTorusField 4) := by
  refine ⟨⟨fixtureProjection 0, ?_⟩⟩
  rw [fixture_wholeLevel]
  trivial

private theorem fixture_maxLocalTopology :
    LocallyPathConnectedSpace (TorusFiltration.superlevel_set fixtureTorusField (-3)) := by
  rw [fixture_maxLevel]
  infer_instance

private theorem fixture_emptyLocalTopology :
    LocallyPathConnectedSpace (TorusFiltration.superlevel_set fixtureTorusField (-4)) := by
  rw [fixture_emptyLevel]
  infer_instance

private theorem fixture_wholeLocalTopology :
    LocallyPathConnectedSpace (TorusFiltration.superlevel_set fixtureTorusField 4) := by
  let _ : LocallyPathConnectedSpace (I4Torus.SourceTorus 2 2) :=
    ((SourceActualFoldTorus.torusProjection2L_open 2).isQuotientMap
      (SourceActualFoldTorus.torusProjection2L_continuous 2)
      (SourceActualFoldTorus.torusProjection2L_surjective 2)).locallyPathConnectedSpace
  rw [fixture_wholeLevel]
  exact isOpen_univ.locallyPathConnectedSpace

private theorem fixture_finite_max :
    Finite (ZerothHomotopy (TorusFiltration.superlevel_set fixtureTorusField (-3))) := by
  exact consumeFiniteClosedSubtype (by norm_num : (0 : ℝ) < 2) fixtureSample 3
    fixture_maxLocalTopology

private theorem fixture_finite_empty :
    Finite (ZerothHomotopy (TorusFiltration.superlevel_set fixtureTorusField (-4))) := by
  exact consumeFiniteClosedSubtype (by norm_num : (0 : ℝ) < 2) fixtureSample 4
    fixture_emptyLocalTopology

private theorem fixture_finite_whole :
    Finite (ZerothHomotopy (TorusFiltration.superlevel_set fixtureTorusField 4)) := by
  simpa [fixtureTorusField] using
    consumeFiniteClosedSubtype (by norm_num : (0 : ℝ) < 2) fixtureSample (-4)
      (by simpa [fixtureTorusField] using fixture_wholeLocalTopology)

end I4SourceActualFiniteSuperlevelComponents
