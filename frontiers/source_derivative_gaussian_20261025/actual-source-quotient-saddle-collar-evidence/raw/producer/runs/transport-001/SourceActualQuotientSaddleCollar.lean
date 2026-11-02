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
    (hrho : 0 < rho) (hchart : ChartFacts F q O rho phi)
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
      refine ⟨hz, hball hz, ?_⟩
      have hid := hchart.identity z hz
      dsimp [saddleQ]
      linarith
    · rintro ⟨hz, _, hv⟩
      refine ⟨hz, ?_⟩
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
        refine ⟨hz, hball hz, ?_⟩
        have hid := hchart.identity z hz
        dsimp [saddleQ]
        linarith
      · rintro ⟨hz, _, hv⟩
        refine ⟨hz, ?_⟩
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

end I4SourceActualQuotientSaddleCollar
