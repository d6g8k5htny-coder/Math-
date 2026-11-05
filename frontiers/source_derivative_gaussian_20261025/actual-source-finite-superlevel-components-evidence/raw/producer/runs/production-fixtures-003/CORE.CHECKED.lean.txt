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

end I4SourceActualFiniteSuperlevelComponents
