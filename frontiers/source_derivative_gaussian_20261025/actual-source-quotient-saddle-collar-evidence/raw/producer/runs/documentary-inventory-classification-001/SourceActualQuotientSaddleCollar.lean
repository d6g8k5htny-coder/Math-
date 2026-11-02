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

/- Private finite Pi/max-norm saddle geometry.  The producer supplies Point2,
   saddleQ, targetStrict, targetPlus, targetMinus, targetLower and SaddleGeometry. -/

private theorem sc64_weighted_positive {a b x y : ℝ}
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : a + b = 1)
    (hx : 0 < x) (hy : 0 < y) : 0 < a * x + b * y := by
  by_cases ha0 : a = 0
  · have hb1 : b = 1 := by linarith
    simpa [ha0, hb1] using hy
  · have hap : 0 < a := by
      by_contra h
      exact ha0 (le_antisymm (le_of_not_gt h) ha)
    exact add_pos_of_pos_of_nonneg (mul_pos hap hx) (mul_nonneg hb hy.le)

private theorem sc64_positive_cone_iff (u : Point2) :
    (0 < saddleQ u ∧ 0 < u 1) ↔ (-u 1 < u 0 ∧ u 0 < u 1) := by
  constructor
  · rintro ⟨hq, hpos⟩
    have hsq : (u 0)^2 < (u 1)^2 := by
      dsimp [saddleQ] at hq
      linarith
    constructor
    · by_contra h
      have hu : u 0 ≤ -u 1 := le_of_not_gt h
      have hprod : 0 ≤ (-u 0 - u 1) * (-u 0 + u 1) :=
        mul_nonneg (by linarith) (by linarith)
      nlinarith
    · by_contra h
      have hu : u 1 ≤ u 0 := le_of_not_gt h
      have hprod : 0 ≤ (u 0 - u 1) * (u 0 + u 1) :=
        mul_nonneg (by linarith) (by linarith)
      nlinarith
  · rintro ⟨hleft, hright⟩
    have hprod : 0 < (u 1 - u 0) * (u 1 + u 0) :=
      mul_pos (by linarith) (by linarith)
    constructor
    · dsimp [saddleQ]
      nlinarith
    · linarith

private theorem sc64_negative_cone_iff (u : Point2) :
    (0 < saddleQ u ∧ u 1 < 0) ↔ (u 1 < u 0 ∧ u 0 < -u 1) := by
  constructor
  · rintro ⟨hq, hneg⟩
    have hnq : 0 < saddleQ (-u) := by simpa [saddleQ] using hq
    have hnp : 0 < (-u) 1 := by
      change 0 < -(u 1)
      linarith
    have hh := (sc64_positive_cone_iff (-u)).mp ⟨hnq, hnp⟩
    change -(-(u 1)) < -(u 0) ∧ -(u 0) < -(u 1) at hh
    constructor <;> linarith [hh.1, hh.2]
  · rintro ⟨hleft, hright⟩
    have hh : -(-u) 1 < (-u) 0 ∧ (-u) 0 < (-u) 1 := by
      change -(-(u 1)) < -(u 0) ∧ -(u 0) < -(u 1)
      constructor <;> linarith
    have hn := (sc64_positive_cone_iff (-u)).mpr hh
    refine ⟨?_, ?_⟩
    · simpa [saddleQ] using hn.1
    · have hp := hn.2
      change 0 < -(u 1) at hp
      linarith

private theorem sc64_positive_cone_convex :
    Convex ℝ {u : Point2 | -u 1 < u 0 ∧ u 0 < u 1} := by
  intro x hx y hy a b ha hb hab
  have hleft : 0 < a * (x 0 + x 1) + b * (y 0 + y 1) :=
    sc64_weighted_positive ha hb hab (by linarith [hx.1]) (by linarith [hy.1])
  have hright : 0 < a * (x 1 - x 0) + b * (y 1 - y 0) :=
    sc64_weighted_positive ha hb hab (by linarith [hx.2]) (by linarith [hy.2])
  change -(a * x 1 + b * y 1) < a * x 0 + b * y 0 ∧
    a * x 0 + b * y 0 < a * x 1 + b * y 1
  constructor <;> nlinarith

private theorem sc64_negative_cone_convex :
    Convex ℝ {u : Point2 | u 1 < u 0 ∧ u 0 < -u 1} := by
  intro x hx y hy a b ha hb hab
  have hleft : 0 < a * (x 0 - x 1) + b * (y 0 - y 1) :=
    sc64_weighted_positive ha hb hab (by linarith [hx.1]) (by linarith [hy.1])
  have hright : 0 < a * (-x 1 - x 0) + b * (-y 1 - y 0) :=
    sc64_weighted_positive ha hb hab (by linarith [hx.2]) (by linarith [hy.2])
  change a * x 1 + b * y 1 < a * x 0 + b * y 0 ∧
    a * x 0 + b * y 0 < -(a * x 1 + b * y 1)
  constructor <;> nlinarith

private theorem sc64_targetPlus_eq (rho : ℝ) :
    targetPlus rho = Metric.ball (0 : Point2) rho ∩
      {u : Point2 | -u 1 < u 0 ∧ u 0 < u 1} := by
  ext u
  change ((u ∈ Metric.ball (0 : Point2) rho ∧ 0 < saddleQ u) ∧ 0 < u 1) ↔
    (u ∈ Metric.ball (0 : Point2) rho ∧ (-u 1 < u 0 ∧ u 0 < u 1))
  constructor
  · rintro ⟨⟨hball, hq⟩, hsign⟩
    exact ⟨hball, (sc64_positive_cone_iff u).mp ⟨hq, hsign⟩⟩
  · rintro ⟨hball, hcone⟩
    rcases (sc64_positive_cone_iff u).mpr hcone with ⟨hq, hsign⟩
    exact ⟨⟨hball, hq⟩, hsign⟩

private theorem sc64_targetMinus_eq (rho : ℝ) :
    targetMinus rho = Metric.ball (0 : Point2) rho ∩
      {u : Point2 | u 1 < u 0 ∧ u 0 < -u 1} := by
  ext u
  change ((u ∈ Metric.ball (0 : Point2) rho ∧ 0 < saddleQ u) ∧ u 1 < 0) ↔
    (u ∈ Metric.ball (0 : Point2) rho ∧ (u 1 < u 0 ∧ u 0 < -u 1))
  constructor
  · rintro ⟨⟨hball, hq⟩, hsign⟩
    exact ⟨hball, (sc64_negative_cone_iff u).mp ⟨hq, hsign⟩⟩
  · rintro ⟨hball, hcone⟩
    rcases (sc64_negative_cone_iff u).mpr hcone with ⟨hq, hsign⟩
    exact ⟨⟨hball, hq⟩, hsign⟩

private theorem sc64_positive_axis_ball (rho : ℝ) (hrho : 0 < rho) :
    (![0, rho / 2] : Point2) ∈ Metric.ball 0 rho := by
  rw [Metric.mem_ball, dist_zero_right]
  apply (pi_norm_lt_iff hrho).2
  intro i
  fin_cases i
  · simpa using hrho
  · change ‖rho / 2‖ < rho
    rw [Real.norm_eq_abs, abs_of_pos (half_pos hrho)]
    linarith

private theorem sc64_negative_axis_ball (rho : ℝ) (hrho : 0 < rho) :
    (![0, -(rho / 2)] : Point2) ∈ Metric.ball 0 rho := by
  rw [Metric.mem_ball, dist_zero_right]
  apply (pi_norm_lt_iff hrho).2
  intro i
  fin_cases i
  · simpa using hrho
  · change ‖-(rho / 2)‖ < rho
    rw [norm_neg, Real.norm_eq_abs, abs_of_pos (half_pos hrho)]
    linarith

private theorem sc64_plus_pc (rho : ℝ) (hrho : 0 < rho) :
    IsPathConnected (targetPlus rho) := by
  have hconv : Convex ℝ (targetPlus rho) := by
    rw [sc64_targetPlus_eq]
    exact (convex_ball (0 : Point2) rho).inter sc64_positive_cone_convex
  apply hconv.isPathConnected
  refine ⟨![0, rho / 2], ?_⟩
  rw [sc64_targetPlus_eq]
  refine ⟨sc64_positive_axis_ball rho hrho, ?_⟩
  change -(rho / 2) < 0 ∧ 0 < rho / 2
  constructor <;> linarith

private theorem sc64_minus_pc (rho : ℝ) (hrho : 0 < rho) :
    IsPathConnected (targetMinus rho) := by
  have hconv : Convex ℝ (targetMinus rho) := by
    rw [sc64_targetMinus_eq]
    exact (convex_ball (0 : Point2) rho).inter sc64_negative_cone_convex
  apply hconv.isPathConnected
  refine ⟨![0, -(rho / 2)], ?_⟩
  rw [sc64_targetMinus_eq]
  refine ⟨sc64_negative_axis_ball rho hrho, ?_⟩
  change -(rho / 2) < 0 ∧ 0 < -(-(rho / 2))
  constructor <;> linarith

private theorem sc64_strict_coordinate_ne_zero {rho : ℝ} {u : Point2}
    (hu : u ∈ targetStrict rho) : u 1 ≠ 0 := by
  intro heq
  have hq := hu.2
  change 0 < -(u 0)^2 + (u 1)^2 at hq
  rw [heq] at hq
  nlinarith [sq_nonneg (u 0)]

private theorem sc64_no_joined_negative_positive {rho : ℝ} {u v : Point2}
    (hun : u 1 < 0) (hvp : 0 < v 1) :
    ¬ JoinedIn (targetStrict rho) u v := by
  rintro ⟨gamma, hgamma⟩
  let f : unitInterval → ℝ := fun t => gamma t 1
  have hf : Continuous f := (continuous_apply 1).comp gamma.continuous
  have hf0 : f 0 = u 1 := by simp [f]
  have hf1 : f 1 = v 1 := by simp [f]
  have hbetween : (0 : ℝ) ∈ Icc (f 0) (f 1) := by
    rw [hf0, hf1]
    exact ⟨hun.le, hvp.le⟩
  have hrange : (0 : ℝ) ∈ Set.range f :=
    intermediate_value_univ (0 : unitInterval) (1 : unitInterval) hf hbetween
  rcases hrange with ⟨t, ht⟩
  change gamma t 1 = 0 at ht
  have hq := (hgamma t).2
  change 0 < -(gamma t 0)^2 + (gamma t 1)^2 at hq
  rw [ht] at hq
  nlinarith [sq_nonneg (gamma t 0)]

private theorem sc64_joined_iff (rho : ℝ) (hrho : 0 < rho)
    (u : Point2) (hu : u ∈ targetStrict rho)
    (v : Point2) (hv : v ∈ targetStrict rho) :
    JoinedIn (targetStrict rho) u v ↔ 0 < (u 1) * (v 1) := by
  constructor
  · intro hjoined
    rcases lt_or_gt_of_ne (sc64_strict_coordinate_ne_zero hu) with hun | hup
    · rcases lt_or_gt_of_ne (sc64_strict_coordinate_ne_zero hv) with hvn | hvp
      · exact mul_pos_of_neg_of_neg hun hvn
      · exact False.elim (sc64_no_joined_negative_positive hun hvp hjoined)
    · rcases lt_or_gt_of_ne (sc64_strict_coordinate_ne_zero hv) with hvn | hvp
      · exact False.elim (sc64_no_joined_negative_positive hvn hup hjoined.symm)
      · exact mul_pos hup hvp
  · intro hproduct
    rcases mul_pos_iff.mp hproduct with hpos | hneg
    · exact ((sc64_plus_pc rho hrho).joinedIn u ⟨hu, hpos.1⟩ v ⟨hv, hpos.2⟩).mono
        (fun _ hz => hz.1)
    · exact ((sc64_minus_pc rho hrho).joinedIn u ⟨hu, hneg.1⟩ v ⟨hv, hneg.2⟩).mono
        (fun _ hz => hz.1)

private theorem sc64_lower_pc (rho : ℝ) (hrho : 0 < rho)
    (delta : ℝ) (hdelta : 0 ≤ delta) : IsPathConnected (targetLower rho delta) := by
  have hzero : (0 : Point2) ∈ targetLower rho delta := by
    refine ⟨?_, ?_⟩
    · simpa only [Metric.mem_ball, dist_self] using hrho
    · change -delta ≤ -(0 : ℝ)^2 + (0 : ℝ)^2
      linarith
  have hstar : StarConvex ℝ (0 : Point2) (targetLower rho delta) := by
    intro u hu a b ha hb hab
    refine ⟨(convex_ball (0 : Point2) rho) hzero.1 hu.1 ha hb hab, ?_⟩
    have hb1 : b ≤ 1 := by linarith
    have hb2 : 0 ≤ b^2 := sq_nonneg b
    have hb2le : b^2 ≤ 1 := by nlinarith
    have hscale : saddleQ (a • (0 : Point2) + b • u) = b^2 * saddleQ u := by
      simp [saddleQ]
      ring
    have huq : -delta ≤ saddleQ u := hu.2
    have hnonneg1 : 0 ≤ b^2 * (saddleQ u + delta) :=
      mul_nonneg hb2 (by linarith)
    have hnonneg2 : 0 ≤ delta * (1 - b^2) :=
      mul_nonneg hdelta (by linarith)
    change -delta ≤ saddleQ (a • (0 : Point2) + b • u)
    rw [hscale]
    nlinarith
  exact hstar.isPathConnected hzero

private theorem saddleConeGeometry (rho : ℝ) (hrho : 0 < rho) : SaddleGeometry rho := by
  refine
    { plus_pc := sc64_plus_pc rho hrho
      minus_pc := sc64_minus_pc rho hrho
      disjoint := ?_
      partition := ?_
      joined_iff := sc64_joined_iff rho hrho
      lower_pc := sc64_lower_pc rho hrho }
  · apply Set.disjoint_left.mpr
    intro u hplus hminus
    exact lt_asymm (show 0 < u 1 from hplus.2) (show u 1 < 0 from hminus.2)
  · ext u
    constructor
    · intro hu
      rcases lt_or_gt_of_ne (sc64_strict_coordinate_ne_zero hu) with hneg | hpos
      · exact Or.inr ⟨hu, hneg⟩
      · exact Or.inl ⟨hu, hpos⟩
    · rintro (hu | hu)
      · exact hu.1
      · exact hu.1

private theorem collar_chart_image_preimage {L : ℝ}
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (s : Set Point2) (hs : s ⊆ phi.target) :
    phi.symm '' s = phi.source ∩ phi ⁻¹' s := by
  ext z
  constructor
  · rintro ⟨u, hu, rfl⟩
    refine ⟨phi.symm.mapsTo (hs hu), ?_⟩
    change phi (phi.symm u) ∈ s
    simpa only [phi.right_inv (hs hu)] using hu
  · rintro ⟨hz, hzs⟩
    exact ⟨phi z, hzs, phi.left_inv hz⟩

private theorem collar_pc_preimage {L : ℝ}
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (s : Set Point2) (hs : s ⊆ phi.target) (hpc : IsPathConnected s) :
    IsPathConnected (phi.source ∩ phi ⁻¹' s) := by
  have h := hpc.image' (phi.continuousOn_symm.mono hs)
  rw [collar_chart_image_preimage phi s hs] at h
  exact h

private theorem collar_joined_preimage {L : ℝ}
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (s : Set Point2) (hs : s ⊆ phi.target)
    {p r : I4Torus.SourceTorus 2 L}
    (hp : p ∈ phi.source ∩ phi ⁻¹' s) (hr : r ∈ phi.source ∩ phi ⁻¹' s) :
    JoinedIn (phi.source ∩ phi ⁻¹' s) p r ↔ JoinedIn s (phi p) (phi r) := by
  constructor
  · intro h
    exact (h.map (phi.continuousOn.mono inter_subset_left)).mono (by
      rintro _ ⟨z, hz, rfl⟩
      exact hz.2)
  · intro h
    have hi := h.map (phi.continuousOn_symm.mono hs)
    rw [collar_chart_image_preimage phi s hs] at hi
    simpa only [phi.left_inv hp.1, phi.left_inv hr.1] using hi

private theorem transportSaddleCollar {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (_hrho : 0 < rho) (hchart : ChartFacts F q O rho phi)
    (hgeometry : SaddleGeometry rho) : CollarFacts F q O rho phi := by
  let W : Set (I4Torus.SourceTorus 2 L) := phi.source ∩ {z | F q < F z}
  have hball {z : I4Torus.SourceTorus 2 L} (hz : z ∈ phi.source) :
      phi z ∈ Metric.ball (0 : Point2) rho := by
    rw [← hchart.target_eq]
    exact phi.mapsTo hz
  have hW : W = phi.source ∩ phi ⁻¹' targetStrict rho := by
    ext z
    constructor
    · rintro ⟨hz, hv⟩
      change F q < F z at hv
      refine ⟨hz, hball hz, ?_⟩
      have hid := hchart.identity z hz
      dsimp [saddleQ]
      linarith
    · rintro ⟨hz, _, hv⟩
      refine ⟨hz, ?_⟩
      change F q < F z
      have hid := hchart.identity z hz
      dsimp [saddleQ] at hv
      linarith
  have hplus : W ∩ {z | 0 < phi z 1} = phi.source ∩ phi ⁻¹' targetPlus rho := by
    rw [hW]
    ext z
    change ((z ∈ phi.source ∧ phi z ∈ targetStrict rho) ∧ 0 < phi z 1) ↔
      (z ∈ phi.source ∧ phi z ∈ targetStrict rho ∧ 0 < phi z 1)
    exact and_assoc
  have hminus : W ∩ {z | phi z 1 < 0} = phi.source ∩ phi ⁻¹' targetMinus rho := by
    rw [hW]
    ext z
    change ((z ∈ phi.source ∧ phi z ∈ targetStrict rho) ∧ phi z 1 < 0) ↔
      (z ∈ phi.source ∧ phi z ∈ targetStrict rho ∧ phi z 1 < 0)
    exact and_assoc
  have hstrictT : targetStrict rho ⊆ phi.target := by
    intro u hu
    rw [hchart.target_eq]
    exact hu.1
  have hplusT : targetPlus rho ⊆ phi.target := by
    intro u hu
    exact hstrictT hu.1
  have hminusT : targetMinus rho ⊆ phi.target := by
    intro u hu
    exact hstrictT hu.1
  refine ⟨hchart, ?_⟩
  change IsPathConnected (W ∩ {z | 0 < phi z 1}) ∧
    IsPathConnected (W ∩ {z | phi z 1 < 0}) ∧
    Disjoint (W ∩ {z | 0 < phi z 1}) (W ∩ {z | phi z 1 < 0}) ∧
    W = (W ∩ {z | 0 < phi z 1}) ∪ (W ∩ {z | phi z 1 < 0}) ∧
    (∀ p ∈ W, ∀ r ∈ W, JoinedIn W p r ↔ 0 < (phi p 1) * (phi r 1)) ∧
    (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | F q-delta ≤ F z}))
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · rw [hplus]
    exact collar_pc_preimage phi (targetPlus rho) hplusT hgeometry.plus_pc
  · rw [hminus]
    exact collar_pc_preimage phi (targetMinus rho) hminusT hgeometry.minus_pc
  · rw [hplus, hminus, Set.disjoint_left]
    intro z hzP hzM
    exact Set.disjoint_left.mp hgeometry.disjoint hzP.2 hzM.2
  · rw [hplus, hminus, hW]
    ext z
    constructor
    · rintro ⟨hz, hu⟩
      rw [hgeometry.partition] at hu
      rcases hu with hp | hm
      · exact Or.inl ⟨hz, hp⟩
      · exact Or.inr ⟨hz, hm⟩
    · rintro (⟨hz, hp⟩ | ⟨hz, hm⟩)
      · refine ⟨hz, ?_⟩
        rw [hgeometry.partition]
        exact Or.inl hp
      · refine ⟨hz, ?_⟩
        rw [hgeometry.partition]
        exact Or.inr hm
  · intro p hp r hr
    rw [hW] at hp hr ⊢
    exact (collar_joined_preimage phi (targetStrict rho) hstrictT hp hr).trans
      (hgeometry.joined_iff (phi p) hp.2 (phi r) hr.2)
  · intro delta hdelta
    have hsT : targetLower rho delta ⊆ phi.target := by
      intro u hu
      rw [hchart.target_eq]
      exact hu.1
    have hlower : phi.source ∩ {z | F q-delta ≤ F z} =
        phi.source ∩ phi ⁻¹' targetLower rho delta := by
      ext z
      constructor
      · rintro ⟨hz, hv⟩
        change F q-delta ≤ F z at hv
        refine ⟨hz, hball hz, ?_⟩
        have hid := hchart.identity z hz
        dsimp [saddleQ]
        linarith
      · rintro ⟨hz, _, hv⟩
        refine ⟨hz, ?_⟩
        change F q-delta ≤ F z
        have hid := hchart.identity z hz
        dsimp [saddleQ] at hv
        linarith
    rw [hlower]
    exact collar_pc_preimage phi (targetLower rho delta) hsT (hgeometry.lower_pc delta hdelta)

private theorem actualSaddleCollar {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O) (hXO : physicalProjection L X ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
        CollarFacts (SourceActualFoldTorus.actualTorusField hL.ne' omega)
          (physicalProjection L X) O rho phi := by
  obtain ⟨rho, hrho, phi, hchart⟩ := quotientSaddleChart hL omega X hcrit hI O hO hXO
  exact ⟨rho, hrho, phi, transportSaddleCollar _ _ O rho phi hrho hchart
    (saddleConeGeometry rho hrho)⟩

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
            (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | c-delta ≤ F z})) := by
  dsimp only
  intro O hO hXO
  obtain ⟨rho, hrho, phi, hchart, hbranches⟩ := actualSaddleCollar hL omega X hcrit hI O hO hXO
  exact ⟨rho, hrho, phi, hchart.center_mem, hchart.center_zero, hchart.source_subset,
    hchart.target_eq, hchart.identity, hbranches⟩

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
  (coordinates 2).symm ![x,y]

private def fixtureSmallOpen (X : UniversalLaw.Spec.Lifetime.E 2) :
    Set (I4Torus.SourceTorus 2 2) :=
  physicalProjection 2 '' Metric.ball X (1/8 : ℝ)

private theorem fixture_coordinateFormula (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 fixtureSample x =
      Real.cos (Real.pi * x 0) + 2 * Real.cos (Real.pi * x 1) := by
  let v := I4SourceFiniteTrig.toSource 2 fixturePolynomial
  have hsample : sampleInclusion 2 2 fixtureSample = v := by
    funext m
    simp [sampleInclusion, fixtureSample, I4SourceFinitePinKernel.finiteShiftSample_val,
      I4SourceSmoothConditional.zeroSample, v]
  change I4Source.sourceField 2 2 (sampleInclusion 2 2 fixtureSample) x = _
  rw [hsample]
  have hsum : (∑' m, I4Source.modeCoefficient 2 2 m x * v m) =
      I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x) v := by
    unfold I4SourceFinitePinKernel.finitePairing Finsupp.sum
    apply tsum_eq_sum
    intro m hm
    rw [Finsupp.notMem_support_iff.mp hm, mul_zero]
  change (∑' m, I4Source.modeCoefficient 2 2 m x * v m) = _
  rw [hsum]
  change I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x)
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial) = _
  rw [I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0)]
  norm_num [I4SourceFiniteTrig.eval, I4SourceFiniteTrig.termEval, fixturePolynomial,
    I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two, Pi.single_apply]

private theorem fixture_actualField (Y : UniversalLaw.Spec.Lifetime.E 2) :
    actualField 2 2 fixtureSample Y =
      Real.cos (Real.pi * coordinates 2 Y 0) + 2 * Real.cos (Real.pi * coordinates 2 Y 1) :=
  fixture_coordinateFormula (coordinates 2 Y)

private def fixtureCoordinate (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ).comp (coordinates 2).toContinuousLinearMap

private def fixtureDerivative (Y : UniversalLaw.Spec.Lifetime.E 2) :
    UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (-Real.pi * Real.sin (Real.pi * coordinates 2 Y 0)) • fixtureCoordinate 0 +
    (-2 * Real.pi * Real.sin (Real.pi * coordinates 2 Y 1)) • fixtureCoordinate 1

private theorem fixture_hasFDerivAt (Y : UniversalLaw.Spec.Lifetime.E 2) :
    HasFDerivAt (actualField 2 2 fixtureSample) (fixtureDerivative Y) Y := by
  have a0 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 0)
      (Real.pi • fixtureCoordinate 0) Y := (fixtureCoordinate 0).hasFDerivAt.const_mul Real.pi
  have a1 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 1)
      (Real.pi • fixtureCoordinate 1) Y := (fixtureCoordinate 1).hasFDerivAt.const_mul Real.pi
  have d := a0.cos.add (a1.cos.const_mul 2)
  rw [show actualField 2 2 fixtureSample = fun Z : UniversalLaw.Spec.Lifetime.E 2 =>
      Real.cos (Real.pi * coordinates 2 Z 0) + 2 * Real.cos (Real.pi * coordinates 2 Z 1)
    from funext fixture_actualField]
  convert d using 1
  ext v
  simp [fixtureDerivative, fixtureCoordinate]
  ring

private theorem fixture_hessian (Y u v : UniversalLaw.Spec.Lifetime.E 2) :
    hessian 2 (actualField 2 2 fixtureSample) Y u v =
      (-Real.pi^2 * Real.cos (Real.pi * coordinates 2 Y 0)) * coordinates 2 u 0 * coordinates 2 v 0 +
      (-2 * Real.pi^2 * Real.cos (Real.pi * coordinates 2 Y 1)) * coordinates 2 u 1 * coordinates 2 v 1 := by
  rw [hessian, iteratedFDeriv_two_apply]
  rw [show fderiv ℝ (actualField 2 2 fixtureSample) = fixtureDerivative
    from funext fun Z => (fixture_hasFDerivAt Z).fderiv]
  have a0 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 0)
      (Real.pi • fixtureCoordinate 0) Y := (fixtureCoordinate 0).hasFDerivAt.const_mul Real.pi
  have a1 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 1)
      (Real.pi • fixtureCoordinate 1) Y := (fixtureCoordinate 1).hasFDerivAt.const_mul Real.pi
  have d := ((a0.sin.const_mul (-Real.pi)).smul_const (fixtureCoordinate 0)).add
    ((a1.sin.const_mul (-2 * Real.pi)).smul_const (fixtureCoordinate 1))
  rw [show fderiv ℝ fixtureDerivative Y = _ from d.fderiv]
  simp [fixtureCoordinate]
  ring

private def fixtureAxis (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 :=
  (coordinates 2).symm (Pi.single i 1)

private theorem fixtureAxis_coordinates (i : Fin 2) :
    coordinates 2 (fixtureAxis i) = (Pi.single i 1 : Fin 2 → ℝ) :=
  (coordinates 2).apply_symm_apply _

private theorem fixtureAxis_ne_zero (i : Fin 2) : fixtureAxis i ≠ 0 := by
  intro h
  have hz : (Pi.single i 1 : Fin 2 → ℝ) = 0 := by
    rw [← fixtureAxis_coordinates, h, map_zero]
  have hi := congrFun hz i
  norm_num at hi

private theorem fixture_negativeFirst_inertia (Y : UniversalLaw.Spec.Lifetime.E 2)
    (a b : ℝ) (ha : a < 0) (hb : 0 < b)
    (hquadratic : ∀ v, hessian 2 (actualField 2 2 fixtureSample) Y v v =
      a * (coordinates 2 v 0)^2 + b * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 (actualField 2 2 fixtureSample) Y 1 := by
  let N := Submodule.span ℝ {fixtureAxis 0}
  let P := Submodule.span ℝ {fixtureAxis 1}
  have hN : Module.finrank ℝ N = 1 := finrank_span_singleton (fixtureAxis_ne_zero 0)
  have hP : Module.finrank ℝ P = 1 := finrank_span_singleton (fixtureAxis_ne_zero 1)
  have hd : Disjoint N P := by
    rw [Submodule.disjoint_def]
    intro v hvN hvP
    obtain ⟨s, hs⟩ := Submodule.mem_span_singleton.mp hvN
    obtain ⟨t, ht⟩ := Submodule.mem_span_singleton.mp hvP
    have he : s • (Pi.single (0 : Fin 2) 1 : Fin 2 → ℝ) =
        t • (Pi.single (1 : Fin 2) 1 : Fin 2 → ℝ) := by
      simpa only [map_smul, fixtureAxis_coordinates] using
        congrArg (coordinates 2) (hs.trans ht.symm)
    have hs0 : s = 0 := by
      have he0 := congrFun he 0
      simpa using he0
    rw [← hs, hs0, zero_smul]
  have hc : IsCompl N P := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hd
    simp [UniversalLaw.Spec.Lifetime.E, hN, hP]
  refine ⟨N, P, hc, hN, by simpa using hP, ?_, ?_⟩
  · intro v hv hv0
    obtain ⟨s, rfl⟩ := Submodule.mem_span_singleton.mp hv
    have hs : s ≠ 0 := by
      intro hs
      apply hv0
      simp [hs]
    rw [hquadratic]
    simp only [map_smul, fixtureAxis_coordinates]
    simpa using mul_neg_of_neg_of_pos ha (sq_pos_of_ne_zero hs)
  · intro v hv hv0
    obtain ⟨s, rfl⟩ := Submodule.mem_span_singleton.mp hv
    have hs : s ≠ 0 := by
      intro hs
      apply hv0
      simp [hs]
    rw [hquadratic]
    simp only [map_smul, fixtureAxis_coordinates]
    simpa using mul_pos hb (sq_pos_of_ne_zero hs)

private theorem fixture_pointCritical (x y : ℝ)
    (hx : Real.sin (Real.pi*x) = 0) (hy : Real.sin (Real.pi*y) = 0) :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint x y) := by
  change fderiv ℝ (actualField 2 2 fixtureSample) (fixturePoint x y) = 0
  rw [(fixture_hasFDerivAt _).fderiv]
  ext v
  change (-Real.pi * Real.sin (Real.pi * coordinates 2 (fixturePoint x y) 0)) *
      coordinates 2 v 0 + (-2 * Real.pi * Real.sin (Real.pi * coordinates 2 (fixturePoint x y) 1)) *
      coordinates 2 v 1 = 0
  simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
    Matrix.cons_val_zero, Matrix.cons_val_one, hx, hy, mul_zero, zero_mul, add_zero]

private theorem fixture_positiveInput :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 1 0) = 1 := by
  refine ⟨fixture_pointCritical 1 0 (by norm_num) (by norm_num), ?_, ?_⟩
  · apply I4SourceActualFoldCandidate.hessianHasInertia_one_of_diag _ _ 1
      (Real.pi^2) (-2*Real.pi^2) (by norm_num) (by positivity)
      (by nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]) 0
    intro v
    rw [fixture_hessian]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, mul_one, mul_zero, Real.cos_pi, Real.cos_zero]
    ring
  · rw [fixture_actualField]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num

private theorem fixture_negativeInput :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 0 1) = -1 := by
  refine ⟨fixture_pointCritical 0 1 (by norm_num) (by norm_num), ?_, ?_⟩
  · apply fixture_negativeFirst_inertia _ (-Real.pi^2) (2*Real.pi^2)
      (by nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]) (by positivity)
    intro v
    rw [fixture_hessian]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, mul_one, mul_zero, Real.cos_pi, Real.cos_zero]
    ring
  · rw [fixture_actualField]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num

private theorem fixture_saddleInputs :
    (IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 1 0) = 1) ∧
    (IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 0 1) = -1) :=
  ⟨fixture_positiveInput, fixture_negativeInput⟩

private theorem fixture_seamInputs :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint (-1) 0) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint (-1) 0) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint (-1) 0) = 1 ∧
      physicalProjection 2 (fixturePoint (-1) 0) = physicalProjection 2 (fixturePoint 1 0) := by
  refine ⟨fixture_pointCritical (-1) 0 (by norm_num) (by norm_num), ?_, ?_, ?_⟩
  · apply I4SourceActualFoldCandidate.hessianHasInertia_one_of_diag _ _ 1
      (Real.pi^2) (-2*Real.pi^2) (by norm_num) (by positivity)
      (by nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]) 0
    intro v
    rw [fixture_hessian]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, mul_one, mul_zero, mul_neg_one,
      Real.cos_neg, Real.cos_pi, Real.cos_zero]
    ring
  · rw [fixture_actualField]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num
  · simp only [physicalProjection, fixturePoint, ContinuousLinearEquiv.apply_symm_apply]
    funext i
    fin_cases i
    · change ((-1 : ℝ) : _root_.AddCircle (2 : ℝ)) = ((1 : ℝ) : _root_.AddCircle (2 : ℝ))
      simpa only [show (-1 : ℝ)+2 = 1 by norm_num] using
        (_root_.AddCircle.coe_add_period (2 : ℝ) (-1)).symm
    · rfl

private theorem fixture_smallOpen (X : UniversalLaw.Spec.Lifetime.E 2) :
    IsOpen (fixtureSmallOpen X) ∧ physicalProjection 2 X ∈ fixtureSmallOpen X := by
  have hopen : IsOpenMap (physicalProjection (2 : ℝ)) :=
    (SourceActualFoldTorus.torusProjection2L_open 2).comp (coordinates 2).toHomeomorph.isOpenMap
  exact ⟨hopen _ Metric.isOpen_ball, X, Metric.mem_ball_self (by norm_num), rfl⟩

private theorem fixture_saddlePositive :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
        CollarFacts fixtureTorusField (physicalProjection 2 (fixturePoint 1 0))
          (fixtureSmallOpen (fixturePoint 1 0)) rho phi := by
  exact actualSaddleCollar (by norm_num) fixtureSample (fixturePoint 1 0)
    fixture_positiveInput.1 fixture_positiveInput.2.1 _
    (fixture_smallOpen _).1 (fixture_smallOpen _).2

private theorem fixture_saddleNegative :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
        CollarFacts fixtureTorusField (physicalProjection 2 (fixturePoint 0 1))
          (fixtureSmallOpen (fixturePoint 0 1)) rho phi := by
  exact actualSaddleCollar (by norm_num) fixtureSample (fixturePoint 0 1)
    fixture_negativeInput.1 fixture_negativeInput.2.1 _
    (fixture_smallOpen _).1 (fixture_smallOpen _).2

private theorem fixture_seam :
    ∃ rho : ℝ, 0 < rho ∧
      ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
        CollarFacts fixtureTorusField (physicalProjection 2 (fixturePoint (-1) 0))
          (fixtureSmallOpen (fixturePoint (-1) 0)) rho phi := by
  exact actualSaddleCollar (by norm_num) fixtureSample (fixturePoint (-1) 0)
    fixture_seamInputs.1 fixture_seamInputs.2.1 _
    (fixture_smallOpen _).1 (fixture_smallOpen _).2

end I4SourceActualQuotientSaddleCollar
