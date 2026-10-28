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

namespace I4SourceActualQuotientSaddleCollar

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

/-
Stage64 Helper A: complete original actual quotient saddle-chart section.
Final literal context002 supplies Point2, physicalProjection and ChartFacts.
No imports/namespace/end/common definitions. Unelaborated TEXT ONLY.
-/

private theorem quotientSaddleChart {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O)
    (hXO : physicalProjection L X ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
        ChartFacts (SourceActualFoldTorus.actualTorusField hL.ne' omega)
          (physicalProjection L X) O rho phi := by
  let _ : Fact (0 < L) := ⟨hL⟩
  let _ : DiscreteTopology (AddSubgroup.zmultiples L) := inferInstance
  let c := I4LifetimeField.coordinates 2
  let q : I4Torus.SourceTorus 2 L := physicalProjection L X
  let F : I4Torus.SourceTorus 2 L → ℝ :=
    SourceActualFoldTorus.actualTorusField hL.ne' omega
  let g := I4LifetimeField.actualField 2 L omega
  let intervals : ∀ i : Fin 2, OpenPartialHomeomorph ℝ (_root_.AddCircle L) :=
    fun i => _root_.AddCircle.openPartialHomeomorphCoe L (c X i - L / 2)
  let productChart : OpenPartialHomeomorph Point2 (I4Torus.SourceTorus 2 L) :=
    OpenPartialHomeomorph.pi intervals
  let e : OpenPartialHomeomorph (UniversalLaw.Spec.Lifetime.E 2)
      (I4Torus.SourceTorus 2 L) :=
    c.toHomeomorph.toOpenPartialHomeomorph.trans productChart
  have heProjection (Y : UniversalLaw.Spec.Lifetime.E 2) :
      e Y = physicalProjection L Y := by
    rfl
  have hXe : X ∈ e.source := by
    change X ∈ (Set.univ : Set (UniversalLaw.Spec.Lifetime.E 2)) ∧
      c X ∈ Set.pi Set.univ
        (fun i : Fin 2 => Set.Ioo (c X i - L / 2) (c X i - L / 2 + L))
    refine ⟨Set.mem_univ X, ?_⟩
    intro i _hi
    constructor <;> linarith
  have hqTarget : q ∈ e.target := by
    change physicalProjection L X ∈ e.target
    rw [← heProjection X]
    exact e.mapsTo hXe
  have heInverse : e.symm q = X := by
    change e.symm (physicalProjection L X) = X
    rw [← heProjection X]
    exact e.left_inv hXe
  obtain ⟨_hj, psi, hXpsi, hpsiX, _hzero, _hC1, _hC1inv, hpsiIdentity, _hBasis⟩ :=
    I4SourceActualMorseLocalModel.actualSource_c1_quadratic_localModel
      hL omega X 1 hcrit hI
  have hcoverIdentity (Y : UniversalLaw.Spec.Lifetime.E 2) (hY : Y ∈ psi.source) :
      g Y = g X - (psi Y 0)^2 + (psi Y 1)^2 := by
    have h := hpsiIdentity Y hY
    norm_num [Fin.sum_univ_two] at h
    dsimp [g]
    linarith
  have hpullback (Y : UniversalLaw.Spec.Lifetime.E 2) :
      F (physicalProjection L Y) = g Y := by
    exact SourceActualFoldTorus.actualTorusField_pullback hL.ne' omega (c Y)
  let k : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2 :=
    (e.symm.trans psi).restrOpen O hO
  have hqk : q ∈ k.source := by
    change (q ∈ e.target ∧ e.symm q ∈ psi.source) ∧ q ∈ O
    exact ⟨⟨hqTarget, by simpa only [heInverse] using hXpsi⟩, hXO⟩
  have hkq : k q = 0 := by
    change psi (e.symm q) = 0
    rw [heInverse, hpsiX]
  have hkSubset : k.source ⊆ O := by
    intro z hz
    exact hz.2
  have hkIdentity (z : I4Torus.SourceTorus 2 L) (hz : z ∈ k.source) :
      F z = F q - (k z 0)^2 + (k z 1)^2 := by
    have hztarget : z ∈ e.target := hz.1.1
    have hzpsi : e.symm z ∈ psi.source := hz.1.2
    have hzProjection : physicalProjection L (e.symm z) = z := by
      calc
        physicalProjection L (e.symm z) = e (e.symm z) := (heProjection _).symm
        _ = z := e.right_inv hztarget
    have hzfield : F z = g (e.symm z) := by
      calc
        F z = F (physicalProjection L (e.symm z)) := congrArg F hzProjection.symm
        _ = g (e.symm z) := hpullback _
    have hqfield : F q = g X := hpullback X
    change F z = F q - (psi (e.symm z) 0)^2 + (psi (e.symm z) 1)^2
    rw [hzfield, hqfield]
    exact hcoverIdentity (e.symm z) hzpsi
  have hzeroTarget : (0 : Point2) ∈ k.target := by
    rw [← hkq]
    exact k.mapsTo hqk
  obtain ⟨rho, hrho, hball⟩ := Metric.isOpen_iff.1 k.open_target 0 hzeroTarget
  let phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2 :=
    (k.symm.restrOpen (Metric.ball (0 : Point2) rho) Metric.isOpen_ball).symm
  have hqphi : q ∈ phi.source := by
    change q ∈ k.source ∧ k q ∈ Metric.ball (0 : Point2) rho
    refine ⟨hqk, ?_⟩
    rw [hkq]
    exact Metric.mem_ball_self hrho
  have hphiZero : phi q = 0 := by
    change k q = 0
    exact hkq
  have hphiSource : phi.source ⊆ O := by
    intro z hz
    exact hkSubset hz.1
  have hphiTarget : phi.target = Metric.ball (0 : Point2) rho := by
    change k.target ∩ Metric.ball (0 : Point2) rho = Metric.ball (0 : Point2) rho
    exact Set.inter_eq_right.mpr hball
  refine ⟨rho, hrho, phi, ?_⟩
  exact {
    center_mem := hqphi
    center_zero := hphiZero
    source_subset := hphiSource
    target_eq := hphiTarget
    identity := fun z hz => hkIdentity z hz.1
  }

end I4SourceActualQuotientSaddleCollar
