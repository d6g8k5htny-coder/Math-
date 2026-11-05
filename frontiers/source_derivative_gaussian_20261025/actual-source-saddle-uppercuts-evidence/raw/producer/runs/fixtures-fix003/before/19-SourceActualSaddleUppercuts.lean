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
    simpa only [abs_of_pos (show 0 < u 1 from hu.2)] using ug65_coord_abs_lt rho hrho u hu.1.1 1
  have hv1rho : v 1 < rho := by
    simpa only [abs_of_pos (show 0 < v 1 from hv.2)] using ug65_coord_abs_lt rho hrho v hv.1.1 1
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
  · change Continuous (fun u : Point2 => -u 1)
    exact (continuous_apply (1 : Fin 2)).neg

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
    linarith [show 0 < u 1 from hu.2]
  · intro hv
    refine ⟨ug65_reflect v, ?_, ug65_reflect_involutive v⟩
    refine ⟨ug65_reflect_upper rho hrho eps v hv.1, ?_⟩
    change 0 < -(v 1)
    linarith [show v 1 < 0 from hv.2]

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
    exact lt_asymm (show 0 < u 1 from hpos.2) (show u 1 < 0 from hneg.2)
  · ext u
    constructor
    · intro hu
      rcases lt_or_gt_of_ne (ug65_upper_coordinate_ne_zero rho eps heps u hu) with hn | hp
      · exact Or.inr ⟨hu, hn⟩
      · exact Or.inl ⟨hu, hp⟩
    · rintro (hu | hu)
      · exact hu.1
      · exact hu.1


private theorem actualInheritedCollar {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O)
    (hqO : I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
      InheritedCollar (SourceActualFoldTorus.actualTorusField hL.ne' omega)
        (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) O rho phi := by
  rcases I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar
    hL omega X hcrit hI O hO hqO with
    ⟨rho, hrho, phi, hq, hzero, hsub, htarget, hfield, _, _, _, _, htest, hlower⟩
  exact ⟨rho, hrho, phi, ⟨hq, hzero, hsub, htarget, hfield, hlower, htest⟩⟩

private theorem transportedUpperSign {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (h : InheritedCollar F q O rho phi) (eps : ℝ) (sign : ℝ → Prop) :
    phi.symm '' (targetUpper rho eps ∩ {u | sign (u 1)}) =
      upperTrace F q phi eps ∩ {z | sign (phi z 1)} := by
  ext z
  constructor
  · rintro ⟨u, ⟨⟨hub, huq⟩, hus⟩, rfl⟩
    have hut : u ∈ phi.target := by rwa [h.target_eq]
    have hzs := phi.map_target hut
    have hinv := phi.right_inv hut
    refine ⟨⟨hzs, ?_⟩, ?_⟩
    · have hf := h.field_eq _ hzs
      rw [hinv] at hf
      dsimp [saddleValue] at huq
      change F q + eps ≤ F (phi.symm u)
      linarith
    · change sign (phi (phi.symm u) 1)
      rw [hinv]
      exact hus
  · rintro ⟨⟨hzs, hzq⟩, hzs'⟩
    refine ⟨phi z, ⟨⟨?_, ?_⟩, hzs'⟩, phi.left_inv hzs⟩
    · rw [← h.target_eq]
      exact phi.map_source hzs
    · have hf := h.field_eq z hzs
      change eps ≤ -(phi z 0)^2 + (phi z 1)^2
      change F q + eps ≤ F z at hzq
      linarith

private theorem transportClosedUpper {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (h : InheritedCollar F q O rho phi) (eps : ℝ) (heps : 0 < eps)
    (hg : ClosedBranchFacts rho eps) : UpperClause F q phi eps := by
  have hpimage := transportedUpperSign F q O rho phi h eps (fun t => 0 < t)
  have hmimage := transportedUpperSign F q O rho phi h eps (fun t => t < 0)
  have hpcont : ContinuousOn phi.symm (targetUpperPos rho eps) :=
    phi.symm.continuousOn.mono fun u hu => by
      change u ∈ phi.target
      rw [h.target_eq]
      exact hu.1.1
  have hmcont : ContinuousOn phi.symm (targetUpperNeg rho eps) :=
    phi.symm.continuousOn.mono fun u hu => by
      change u ∈ phi.target
      rw [h.target_eq]
      exact hu.1.1
  have hppc : IsPathConnected (upperTrace F q phi eps ∩ {z | 0 < phi z 1}) := by
    rw [← hpimage]
    exact hg.plus_pc.image' hpcont
  have hmpc : IsPathConnected (upperTrace F q phi eps ∩ {z | phi z 1 < 0}) := by
    rw [← hmimage]
    exact hg.minus_pc.image' hmcont
  have hstrict : upperTrace F q phi eps ⊆ phi.source ∩ {z | F q < F z} := by
    intro z hz
    exact ⟨hz.1, lt_of_lt_of_le (lt_add_of_pos_right _ heps) hz.2⟩
  refine ⟨hppc, hmpc, ?_, ?_, ?_⟩
  · exact Set.disjoint_left.mpr fun z hz hp => lt_asymm (show 0 < phi z 1 from hz.2) (show phi z 1 < 0 from hp.2)
  · ext z
    constructor
    · intro hz
      have hf := h.field_eq z hz.1
      have hnonzero : phi z 1 ≠ 0 := by
        intro hzero
        rw [hzero] at hf
        have hsq := sq_nonneg (phi z 0)
        have hh := hz.2
        change F q + eps ≤ F z at hh
        nlinarith
      rcases lt_or_gt_of_ne hnonzero with hm | hp
      · exact Or.inr ⟨hz, hm⟩
      · exact Or.inl ⟨hz, hp⟩
    · rintro (hz | hz) <;> exact hz.1
  · intro p hp r hr
    constructor
    · intro hjoin
      exact (h.strict_test p (hstrict hp) r (hstrict hr)).mp (hjoin.mono hstrict)
    · intro hprod
      rcases mul_pos_iff.mp hprod with hpos | hneg
      · exact (hppc.joinedIn p ⟨hp, hpos.1⟩ r ⟨hr, hpos.2⟩).mono fun _ hz => hz.1
      · exact (hmpc.joinedIn p ⟨hp, hneg.1⟩ r ⟨hr, hneg.2⟩).mono fun _ hz => hz.1

private theorem actualUniformSaddleCuts {L : ℝ} (hL : 0 < L)
    (omega : I4SmoothCarrier.SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (hcrit : UniversalLaw.Spec.Lifetime.IsCriticalPoint 2 (I4LifetimeField.actualField 2 L omega) X)
    (hI : UniversalLaw.Spec.Lifetime.HessianHasInertia 2 (I4LifetimeField.actualField 2 L omega) X 1)
    (O : Set (I4Torus.SourceTorus 2 L)) (hO : IsOpen O)
    (hqO : I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ O) :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2,
      UniformCutResult (SourceActualFoldTorus.actualTorusField hL.ne' omega)
        (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) O rho phi := by
  obtain ⟨rho, hrho, phi, h⟩ := actualInheritedCollar hL omega X hcrit hI O hO hqO
  refine ⟨rho, hrho, phi, h.center_mem, h.center_eq, h.source_sub, h.target_eq,
    h.field_eq, h.lower_pc, div_pos (sq_pos_of_pos hrho) (by norm_num), ?_⟩
  intro eps heps hbound
  exact transportClosedUpper _ _ O rho phi h eps heps
    (closedSaddleBranchGeometry rho hrho eps heps hbound)

private theorem cutoffEquality {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (hrho : 0 < rho)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (h : UniformCutResult F q O rho phi) : CutoffEquality F q rho phi := by
  have ht := h.2.2.2.1
  have hf := h.2.2.2.2.1
  have hball (s : ℝ) (hs : |s| < rho) : (![0,s] : Point2) ∈ phi.target := by
    rw [ht, Metric.mem_ball, dist_zero_right]
    apply (pi_norm_lt_iff hrho).2
    intro i
    fin_cases i
    · simpa using hrho
    · simpa using hs
  have hp : (![0,rho/4] : Point2) ∈ phi.target := hball _ (by rw [abs_of_pos (by positivity)]; linarith)
  have hm : (![0,-rho/4] : Point2) ∈ phi.target := hball _ (by rw [abs_of_neg (show -rho/4 < 0 by linarith)]; linarith)
  have hps := phi.map_target hp
  have hms := phi.map_target hm
  have hpi := phi.right_inv hp
  have hmi := phi.right_inv hm
  have hpf := hf _ hps
  have hmf := hf _ hms
  rw [hpi] at hpf
  rw [hmi] at hmf
  norm_num only [Fin.isValue, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, zero_pow] at hpf hmf
  have hpfe : F (phi.symm (![0,rho/4] : Point2)) = F q + rho^2/16 := by nlinarith [hpf]
  have hmfe : F (phi.symm (![0,-rho/4] : Point2)) = F q + rho^2/16 := by nlinarith [hmf]
  refine ⟨by positivity, by nlinarith [sq_pos_of_pos hrho], ⟨hps, hpfe.ge⟩,
    ⟨hms, hmfe.ge⟩, hpfe, hmfe, ?_, ?_⟩
  · rw [hpi]
    simpa using (show 0 < rho/4 by positivity)
  · rw [hmi]
    simpa using (show -rho/4 < 0 by linarith)

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
              (∀ p ∈ U, ∀ r ∈ U, JoinedIn U p r ↔ 0 < (phi p 1)*(phi r 1))) := by
  dsimp only
  intro O hO hqO
  exact actualUniformSaddleCuts hL omega X hcrit hI O hO hqO


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

private theorem fixture_scalarSeries_finitePairing {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    I4Foundation.scalarSeries a v = I4SourceFinitePinKernel.finitePairing a v := by
  classical
  unfold I4Foundation.scalarSeries I4SourceFinitePinKernel.finitePairing
  exact tsum_eq_sum fun m hm => by
    rw [Finsupp.notMem_support_iff.mp hm, mul_zero]

private theorem fixture_source (u : Fin 2 → ℝ) :
    I4SmoothCarrier.smoothSourceField 2 2 fixtureSample u =
      Real.cos (Real.pi*u 0) + 2*Real.cos (Real.pi*u 1) := by
  have hv : I4SmoothCarrier.sampleInclusion 2 2 fixtureSample =
      fun m => I4SourceFiniteTrig.toSource 2 fixturePoly m := by
    funext m
    simp [fixtureSample, I4SmoothCarrier.sampleInclusion,
      I4SourceFinitePinKernel.finiteShiftSample_val, I4SourceSmoothConditional.zeroSample]
  change I4Foundation.scalarSeries (fun m => I4Source.modeCoefficient 2 2 m u)
    (I4SmoothCarrier.sampleInclusion 2 2 fixtureSample) = _
  rw [hv, fixture_scalarSeries_finitePairing,
    I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0)]
  norm_num [fixturePoly, I4SourceFiniteTrig.eval, I4SourceFiniteTrig.termEval,
    I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two, Pi.single_apply]

private theorem fixture_field (u : Fin 2 → ℝ) :
    fixtureField (I4Torus.torusProjection 2 2 u) =
      Real.cos (Real.pi*u 0) + 2*Real.cos (Real.pi*u 1) := by
  rw [fixtureField, SourceActualFoldTorus.actualTorusField_pullback]
  exact fixture_source u

private def coord (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i).comp (I4LifetimeField.coordinates 2).toContinuousLinearMap
private def trigField (X : UniversalLaw.Spec.Lifetime.E 2) : ℝ :=
  Real.cos (Real.pi*coord 0 X) + 2*Real.cos (Real.pi*coord 1 X)
private def trigD (X : UniversalLaw.Spec.Lifetime.E 2) :
    UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (-Real.sin (Real.pi*coord 0 X)*Real.pi) • coord 0 +
    (-2*Real.sin (Real.pi*coord 1 X)*Real.pi) • coord 1

private theorem fixture_actual : I4LifetimeField.actualField 2 2 fixtureSample = trigField := by
  funext X
  exact fixture_source (I4LifetimeField.coordinates 2 X)

private theorem trig_deriv (X : UniversalLaw.Spec.Lifetime.E 2) :
    HasFDerivAt trigField (trigD X) X := by
  have h0 := (((coord 0).hasFDerivAt (x := X)).const_mul Real.pi).cos
  have h1 := ((((coord 1).hasFDerivAt (x := X)).const_mul Real.pi).cos).const_mul 2
  convert h0.add h1 using 1 <;> ext v <;>
    simp [trigField, trigD, smul_eq_mul] <;> ring

private theorem trig_hessian (X v w : UniversalLaw.Spec.Lifetime.E 2) :
    hessian 2 trigField X v w =
      -Real.pi^2*Real.cos (Real.pi*coord 0 X)*(coord 0 v)*(coord 0 w) -
      2*Real.pi^2*Real.cos (Real.pi*coord 1 X)*(coord 1 v)*(coord 1 w) := by
  have hd : fderiv ℝ trigField = trigD := funext fun Y => (trig_deriv Y).fderiv
  have h0 := ((((coord 0).hasFDerivAt (x := X)).const_mul Real.pi).sin.neg.mul_const Real.pi).smul_const (coord 0)
  have h1 := (((((coord 1).hasFDerivAt (x := X)).const_mul Real.pi).sin.const_mul (-2)).mul_const Real.pi).smul_const (coord 1)
  have hh := h0.add h1
  change hessian 2 trigField X v w = _
  rw [hessian, iteratedFDeriv_succ_apply_right, iteratedFDeriv_one_apply]
  change fderiv ℝ (fderiv ℝ trigField) X v w = _
  rw [hd]
  have he := hh.fderiv
  change fderiv ℝ trigD X = _ at he
  rw [he]
  simp [ContinuousLinearMap.smulRight_apply, ContinuousLinearMap.smul_apply,
    smul_eq_mul]
  ring

private theorem point_coords (x y : ℝ) :
    coord 0 (fixturePoint x y) = x ∧ coord 1 (fixturePoint x y) = y := by
  simp [coord, fixturePoint]

private theorem fixture_critical_of (x y : ℝ)
    (hx : Real.sin (Real.pi*x) = 0) (hy : Real.sin (Real.pi*y) = 0) :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) := by
  rw [IsCriticalPoint, fixture_actual, (trig_deriv _).fderiv]
  ext v
  simp [trigD, (point_coords x y).1, (point_coords x y).2, hx, hy]

private theorem axis0_ne : fixturePoint 1 0 ≠ 0 := by
  intro h
  have := congrArg (coord 0) h
  simp [(point_coords 1 0).1] at this
private theorem axis1_ne : fixturePoint 0 1 ≠ 0 := by
  intro h
  have := congrArg (coord 1) h
  simp [(point_coords 0 1).2] at this

private theorem axes_compl : IsCompl (ℝ ∙ fixturePoint 1 0) (ℝ ∙ fixturePoint 0 1) := by
  constructor
  · rw [Submodule.disjoint_def]
    intro v hv0 hv1
    rcases Submodule.mem_span_singleton.mp hv0 with ⟨a, rfl⟩
    rcases Submodule.mem_span_singleton.mp hv1 with ⟨b, hb⟩
    have ha := congrArg (coord 0) hb
    have ha0 : a = 0 := by simpa [(point_coords 0 1).1, (point_coords 1 0).1] using ha.symm
    simp [ha0]
  · rw [codisjoint_iff, Submodule.sup_eq_top_iff]
    intro v
    refine ⟨coord 0 v • fixturePoint 1 0, Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _),
      coord 1 v • fixturePoint 0 1, Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _), ?_⟩
    apply (I4LifetimeField.coordinates 2).injective
    have h0 : I4LifetimeField.coordinates 2 (fixturePoint 1 0) = (![1,0] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    have h1 : I4LifetimeField.coordinates 2 (fixturePoint 0 1) = (![0,1] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    rw [map_add, map_smul, map_smul, h0, h1]
    ext i
    fin_cases i <;> simp [coord]

private theorem fixture_inertia_pos (x y : ℝ)
    (hx : Real.cos (Real.pi*x) = -1) (hy : Real.cos (Real.pi*y) = 1) :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) 1 := by
  rw [fixture_actual]
  refine ⟨ℝ ∙ fixturePoint 0 1, ℝ ∙ fixturePoint 1 0, axes_compl.symm,
    finrank_span_singleton axis1_ne, ?_, ?_, ?_⟩
  · simpa using finrank_span_singleton (K := ℝ) axis0_ne
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 0 1).1, (point_coords 0 1).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 1 0).1, (point_coords 1 0).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]

private theorem fixture_inertia_neg (x y : ℝ)
    (hx : Real.cos (Real.pi*x) = 1) (hy : Real.cos (Real.pi*y) = -1) :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) 1 := by
  rw [fixture_actual]
  refine ⟨ℝ ∙ fixturePoint 1 0, ℝ ∙ fixturePoint 0 1, axes_compl,
    finrank_span_singleton axis0_ne, ?_, ?_, ?_⟩
  · simpa using finrank_span_singleton (K := ℝ) axis1_ne
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 1 0).1, (point_coords 1 0).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 0 1).1, (point_coords 0 1).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]

private theorem fixture_positive_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 1 0) :=
  fixture_critical_of 1 0 (by simp) (by simp)
private theorem fixture_positive_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 :=
  fixture_inertia_pos 1 0 (by simp) (by simp)
private theorem fixture_negative_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 0 1) :=
  fixture_critical_of 0 1 (by simp) (by simp)
private theorem fixture_negative_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 :=
  fixture_inertia_neg 0 1 (by simp) (by simp)
private theorem fixture_seam_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint (-1) 0) :=
  fixture_critical_of (-1) 0 (by simp) (by simp)
private theorem fixture_seam_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint (-1) 0) 1 :=
  fixture_inertia_pos (-1) 0 (by simp) (by simp)

private theorem fixture_heights : fixtureField (fixtureCenter 1 0) = 1 ∧
    fixtureField (fixtureCenter 0 1) = -1 ∧ fixtureField (fixtureCenter (-1) 0) = 1 := by
  norm_num [fixtureCenter, fixture_field]

private theorem fixture_open (x y : ℝ) : IsOpen (fixtureOpen x y) ∧
    fixtureCenter x y ∈ fixtureOpen x y := by
  refine ⟨?_, ?_⟩
  · exact (SourceActualFoldTorus.torusProjection2L_open 2)
      _ ((I4LifetimeField.coordinates 2).isOpenMap _ Metric.isOpen_ball)
  · refine ⟨![x,y], ?_, rfl⟩
    exact ⟨fixturePoint x y, Metric.mem_ball_self (by norm_num), by simp [fixturePoint]⟩

private theorem fixture_seam : fixtureCenter (-1) 0 = fixtureCenter 1 0 := by
  funext i
  fin_cases i
  · change ((-1 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ))
    have h : (((-1 : ℝ)+2 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ)) :=
      congrArg (fun t : ℝ => (t : AddCircle (2 : ℝ))) (by norm_num)
    exact (AddCircle.coe_add_period (2 : ℝ) (-1 : ℝ)).symm.trans h
  · rfl

private theorem fixture_consumer (x y : ℝ)
    (hc : IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y))
    (hi : HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) 1) :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter x y) (fixtureOpen x y) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter x y) rho phi := by
  have hh := actualSource_quotient_saddle_uniform_closed_uppercuts (by norm_num : (0 : ℝ) < 2)
    fixtureSample (fixturePoint x y) hc hi (fixtureOpen x y) (fixture_open x y).1
  have hq : I4Torus.torusProjection 2 2 (I4LifetimeField.coordinates 2 (fixturePoint x y)) ∈ fixtureOpen x y := by
    simpa [fixturePoint, fixtureCenter] using (fixture_open x y).2
  obtain ⟨rho, hrho, phi, h⟩ := hh hq
  have hu : UniformCutResult fixtureField (fixtureCenter x y) (fixtureOpen x y) rho phi := by
    simpa [UniformCutResult, UpperClause, upperTrace, fixtureField, fixtureCenter, fixturePoint] using h
  exact ⟨rho, hrho, phi, hu, cutoffEquality _ _ _ _ hrho _ hu⟩

private theorem fixture_positive_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 1 0) (fixtureOpen 1 0) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter 1 0) rho phi :=
  fixture_consumer 1 0 fixture_positive_critical fixture_positive_inertia
private theorem fixture_negative_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 0 1) (fixtureOpen 0 1) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter 0 1) rho phi :=
  fixture_consumer 0 1 fixture_negative_critical fixture_negative_inertia
private theorem fixture_seam_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter (-1) 0) (fixtureOpen (-1) 0) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter (-1) 0) rho phi :=
  fixture_consumer (-1) 0 fixture_seam_critical fixture_seam_inertia

end I4SourceActualSaddleUppercuts
