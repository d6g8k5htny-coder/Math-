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

/- Finite Pi2 geometry for positive CLOSED saddle uppercuts.
   Common definitions and the six-field ClosedBranchFacts are producer-owned. -/

private def ug65_atHeight (u : Point2) (H : ℝ) : Point2 := ![u 0, H]

private def ug65_reflect (u : Point2) : Point2 := ![u 0, -u 1]

private theorem ug65_coord_abs_lt (rho : ℝ) (hrho : 0 < rho)
    (u : Point2) (hu : u ∈ Metric.ball (0 : Point2) rho) (i : Fin 2) :
    |u i| < rho := by
  have hn : ‖u‖ < rho := by
    simpa only [Metric.mem_ball, dist_zero_right] using hu
  simpa only [Real.norm_eq_abs] using (pi_norm_lt_iff hrho).mp hn i

private theorem ug65_point_ball (rho : ℝ) (hrho : 0 < rho) (x y : ℝ)
    (hx : |x| < rho) (hy : |y| < rho) :
    (![x, y] : Point2) ∈ Metric.ball 0 rho := by
  rw [Metric.mem_ball, dist_zero_right]
  apply (pi_norm_lt_iff hrho).2
  intro i
  fin_cases i
  · simpa [Real.norm_eq_abs] using hx
  · simpa [Real.norm_eq_abs] using hy

private theorem ug65_square_mono {x y : ℝ} (hx : 0 ≤ x) (hxy : x ≤ y) :
    x^2 ≤ y^2 := by
  have hprod : 0 ≤ (y - x) * (y + x) :=
    mul_nonneg (sub_nonneg.mpr hxy) (by linarith)
  nlinarith

private theorem ug65_square_of_abs_le {x m : ℝ} (h : |x| ≤ m) : x^2 ≤ m^2 := by
  rcases abs_le.mp h with ⟨hlo, hhi⟩
  have hprod : 0 ≤ (m - x) * (m + x) :=
    mul_nonneg (by linarith) (by linarith)
  nlinarith

private theorem ug65_vertical_join (rho eps : ℝ) (hrho : 0 < rho)
    (u : Point2) (hu : u ∈ targetUpperPos rho eps)
    (H : ℝ) (huH : u 1 ≤ H) (hHrho : H < rho) :
    JoinedIn (targetUpperPos rho eps) u (ug65_atHeight u H) := by
  have hHpos : 0 < H := lt_of_lt_of_le hu.2 huH
  have htop : ug65_atHeight u H ∈ Metric.ball (0 : Point2) rho := by
    exact ug65_point_ball rho hrho (u 0) H
      (ug65_coord_abs_lt rho hrho u hu.1.1 0)
      (by rw [abs_of_pos hHpos]; exact hHrho)
  apply JoinedIn.of_segment_subset
  rintro z ⟨a, b, ha, hb, hab, rfl⟩
  have hc0 : a * u 0 + b * u 0 = u 0 := by
    calc
      a * u 0 + b * u 0 = (a + b) * u 0 := by ring
      _ = u 0 := by rw [hab, one_mul]
  have hc1base : a * u 1 + b * u 1 = u 1 := by
    calc
      a * u 1 + b * u 1 = (a + b) * u 1 := by ring
      _ = u 1 := by rw [hab, one_mul]
  have hc1 : u 1 ≤ a * u 1 + b * H := by
    have hmul := mul_le_mul_of_nonneg_left huH hb
    linarith
  have hpos : 0 < a * u 1 + b * H := lt_of_lt_of_le hu.2 hc1
  have hsq : (u 1)^2 ≤ (a * u 1 + b * H)^2 := ug65_square_mono hu.2.le hc1
  have huq : eps ≤ -(u 0)^2 + (u 1)^2 := hu.1.2
  refine ⟨⟨(convex_ball (0 : Point2) rho) hu.1.1 htop ha hb hab, ?_⟩, ?_⟩
  · change eps ≤ -(a * u 0 + b * u 0)^2 + (a * u 1 + b * H)^2
    rw [hc0]
    linarith
  · change 0 < a * u 1 + b * H
    exact hpos

private theorem ug65_horizontal_join (rho eps : ℝ) (hrho : 0 < rho)
    (u : Point2) (hu : u ∈ targetUpperPos rho eps)
    (v : Point2) (hv : v ∈ targetUpperPos rho eps)
    (H : ℝ) (huH : u 1 ≤ H) (hvH : v 1 ≤ H) (hHrho : H < rho) :
    JoinedIn (targetUpperPos rho eps) (ug65_atHeight u H) (ug65_atHeight v H) := by
  let m : ℝ := max |u 0| |v 0|
  have hmu : |u 0| ≤ m := le_max_left _ _
  have hmv : |v 0| ≤ m := le_max_right _ _
  have hmrho : m < rho := max_lt_iff.mpr
    ⟨ug65_coord_abs_lt rho hrho u hu.1.1 0,
      ug65_coord_abs_lt rho hrho v hv.1.1 0⟩
  have hHpos : 0 < H := lt_of_lt_of_le hu.2 huH
  have hucut : eps + (u 0)^2 ≤ H^2 := by
    have hsq := ug65_square_mono hu.2.le huH
    have hq : eps ≤ -(u 0)^2 + (u 1)^2 := hu.1.2
    linarith
  have hvcut : eps + (v 0)^2 ≤ H^2 := by
    have hsq := ug65_square_mono hv.2.le hvH
    have hq : eps ≤ -(v 0)^2 + (v 1)^2 := hv.1.2
    linarith
  have hmcut : eps + m^2 ≤ H^2 := by
    dsimp [m]
    rcases le_total |u 0| |v 0| with hle | hle
    · rw [max_eq_right hle, sq_abs]
      exact hvcut
    · rw [max_eq_left hle, sq_abs]
      exact hucut
  apply JoinedIn.of_segment_subset
  rintro z ⟨a, b, ha, hb, hab, rfl⟩
  have hmcomb : a * m + b * m = m := by
    calc
      a * m + b * m = (a + b) * m := by ring
      _ = m := by rw [hab, one_mul]
  have hncomb : a * (-m) + b * (-m) = -m := by
    calc
      a * (-m) + b * (-m) = -(a * m + b * m) := by ring
      _ = -m := by rw [hmcomb]
  have hlow : -m ≤ a * u 0 + b * v 0 := by
    calc
      -m = a * (-m) + b * (-m) := hncomb.symm
      _ ≤ a * u 0 + b * v 0 := add_le_add
        (mul_le_mul_of_nonneg_left (abs_le.mp hmu).1 ha)
        (mul_le_mul_of_nonneg_left (abs_le.mp hmv).1 hb)
  have hhigh : a * u 0 + b * v 0 ≤ m := by
    calc
      a * u 0 + b * v 0 ≤ a * m + b * m := add_le_add
        (mul_le_mul_of_nonneg_left (abs_le.mp hmu).2 ha)
        (mul_le_mul_of_nonneg_left (abs_le.mp hmv).2 hb)
      _ = m := hmcomb
  have habs : |a * u 0 + b * v 0| ≤ m := abs_le.mpr ⟨hlow, hhigh⟩
  have hHcomb : a * H + b * H = H := by
    calc
      a * H + b * H = (a + b) * H := by ring
      _ = H := by rw [hab, one_mul]
  have heq : a • ug65_atHeight u H + b • ug65_atHeight v H =
      (![a * u 0 + b * v 0, H] : Point2) := by
    ext i
    fin_cases i
    · rfl
    · change a * H + b * H = H
      exact hHcomb
  have hball : a • ug65_atHeight u H + b • ug65_atHeight v H ∈
      Metric.ball (0 : Point2) rho := by
    rw [heq]
    exact ug65_point_ball rho hrho (a * u 0 + b * v 0) H
      (habs.trans_lt hmrho) (by rw [abs_of_pos hHpos]; exact hHrho)
  have hsq : (a * u 0 + b * v 0)^2 ≤ m^2 := ug65_square_of_abs_le habs
  refine ⟨⟨hball, ?_⟩, ?_⟩
  · change eps ≤ -(a * u 0 + b * v 0)^2 + (a * H + b * H)^2
    rw [hHcomb]
    linarith
  · change 0 < a * H + b * H
    rw [hHcomb]
    exact hHpos

private theorem ug65_positive_join (rho eps : ℝ) (hrho : 0 < rho)
    (u : Point2) (hu : u ∈ targetUpperPos rho eps)
    (v : Point2) (hv : v ∈ targetUpperPos rho eps) :
    JoinedIn (targetUpperPos rho eps) u v := by
  let H : ℝ := max (u 1) (v 1)
  have huH : u 1 ≤ H := le_max_left _ _
  have hvH : v 1 ≤ H := le_max_right _ _
  have hu1rho : u 1 < rho := by
    simpa only [abs_of_pos hu.2] using ug65_coord_abs_lt rho hrho u hu.1.1 1
  have hv1rho : v 1 < rho := by
    simpa only [abs_of_pos hv.2] using ug65_coord_abs_lt rho hrho v hv.1.1 1
  have hHrho : H < rho := max_lt_iff.mpr ⟨hu1rho, hv1rho⟩
  have hfirst := ug65_vertical_join rho eps hrho u hu H huH hHrho
  have hmiddle := ug65_horizontal_join rho eps hrho u hu v hv H huH hvH hHrho
  have hlast := (ug65_vertical_join rho eps hrho v hv H hvH hHrho).symm
  exact hfirst.trans (hmiddle.trans hlast)

private theorem ug65_plus_witness (rho : ℝ) (hrho : 0 < rho)
    (eps : ℝ) (hbound : eps < rho^2/4) :
    (![0, rho/2] : Point2) ∈ targetUpperPos rho eps := by
  have hball : (![0, rho/2] : Point2) ∈ Metric.ball 0 rho :=
    ug65_point_ball rho hrho 0 (rho/2) (by simpa using hrho)
      (by rw [abs_of_pos (half_pos hrho)]; linarith)
  refine ⟨⟨hball, ?_⟩, ?_⟩
  · change eps ≤ -(0 : ℝ)^2 + (rho/2)^2
    nlinarith
  · change 0 < rho/2
    linarith

private theorem ug65_minus_witness (rho : ℝ) (hrho : 0 < rho)
    (eps : ℝ) (hbound : eps < rho^2/4) :
    (![0, -rho/2] : Point2) ∈ targetUpperNeg rho eps := by
  have hball : (![0, -rho/2] : Point2) ∈ Metric.ball 0 rho := by
    apply ug65_point_ball rho hrho 0 (-rho/2) (by simpa using hrho)
    have hneg : -rho/2 = -(rho/2) := by ring
    rw [hneg, abs_neg, abs_of_pos (half_pos hrho)]
    linarith
  refine ⟨⟨hball, ?_⟩, ?_⟩
  · change eps ≤ -(0 : ℝ)^2 + (-rho/2)^2
    nlinarith
  · change -rho/2 < 0
    linarith

private theorem ug65_plus_pc (rho : ℝ) (hrho : 0 < rho)
    (eps : ℝ) (hbound : eps < rho^2/4) : IsPathConnected (targetUpperPos rho eps) := by
  have hw := ug65_plus_witness rho hrho eps hbound
  refine ⟨![0, rho/2], hw, ?_⟩
  intro v hv
  exact ug65_positive_join rho eps hrho ![0, rho/2] hw v hv

private theorem ug65_reflect_continuous : Continuous ug65_reflect := by
  apply continuous_pi
  intro i
  fin_cases i
  · simpa [ug65_reflect] using
      (continuous_apply (0 : Fin 2) : Continuous (fun u : Point2 => u 0))
  · simpa [ug65_reflect] using
      (continuous_apply (1 : Fin 2) : Continuous (fun u : Point2 => u 1)).neg

private theorem ug65_reflect_involutive (u : Point2) : ug65_reflect (ug65_reflect u) = u := by
  ext i
  fin_cases i <;> simp [ug65_reflect]

private theorem ug65_reflect_upper (rho : ℝ) (hrho : 0 < rho) (eps : ℝ)
    (u : Point2) (hu : u ∈ targetUpper rho eps) :
    ug65_reflect u ∈ targetUpper rho eps := by
  refine ⟨?_, ?_⟩
  · exact ug65_point_ball rho hrho (u 0) (-u 1)
      (ug65_coord_abs_lt rho hrho u hu.1 0)
      (by simpa only [abs_neg] using ug65_coord_abs_lt rho hrho u hu.1 1)
  · simpa [ug65_reflect, saddleValue] using hu.2

private theorem ug65_reflect_image (rho : ℝ) (hrho : 0 < rho) (eps : ℝ) :
    ug65_reflect '' targetUpperPos rho eps = targetUpperNeg rho eps := by
  ext v
  constructor
  · rintro ⟨u, hu, rfl⟩
    refine ⟨ug65_reflect_upper rho hrho eps u hu.1, ?_⟩
    change -(u 1) < 0
    linarith [hu.2]
  · intro hv
    refine ⟨ug65_reflect v, ?_, ug65_reflect_involutive v⟩
    refine ⟨ug65_reflect_upper rho hrho eps v hv.1, ?_⟩
    change 0 < -(v 1)
    linarith [hv.2]

private theorem ug65_minus_pc (rho : ℝ) (hrho : 0 < rho)
    (eps : ℝ) (hbound : eps < rho^2/4) : IsPathConnected (targetUpperNeg rho eps) := by
  rw [← ug65_reflect_image rho hrho eps]
  exact (ug65_plus_pc rho hrho eps hbound).image ug65_reflect_continuous

private theorem ug65_upper_coordinate_ne_zero (rho eps : ℝ) (heps : 0 < eps)
    (u : Point2) (hu : u ∈ targetUpper rho eps) : u 1 ≠ 0 := by
  intro hzero
  have hq := hu.2
  change eps ≤ -(u 0)^2 + (u 1)^2 at hq
  rw [hzero] at hq
  nlinarith [sq_nonneg (u 0)]

private theorem closedSaddleBranchGeometry (rho : ℝ) (hrho : 0 < rho)
    (eps : ℝ) (heps : 0 < eps) (hbound : eps < rho^2/4) :
    ClosedBranchFacts rho eps := by
  refine
    { plus_pc := ug65_plus_pc rho hrho eps hbound
      minus_pc := ug65_minus_pc rho hrho eps hbound
      disjoint := ?_
      partition := ?_
      plus_witness := ug65_plus_witness rho hrho eps hbound
      minus_witness := ug65_minus_witness rho hrho eps hbound }
  · apply Set.disjoint_left.mpr
    intro u hpos hneg
    exact lt_asymm hpos.2 hneg.2
  · ext u
    constructor
    · intro hu
      rcases lt_or_gt_of_ne (ug65_upper_coordinate_ne_zero rho eps heps u hu) with hn | hp
      · exact Or.inr ⟨hu, hn⟩
      · exact Or.inl ⟨hu, hp⟩
    · rintro (hu | hu)
      · exact hu.1
      · exact hu.1

end I4SourceActualSaddleUppercuts
