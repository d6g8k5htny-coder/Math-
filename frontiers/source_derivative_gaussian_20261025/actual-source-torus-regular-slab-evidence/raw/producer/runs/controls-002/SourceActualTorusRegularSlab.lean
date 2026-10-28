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
open scoped Topology BigOperators Matrix NNReal
set_option autoImplicit false
namespace I4SourceActualTorusRegularSlab

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


/-! Actual-source normalized field. Private, fixed physical E2; no ODE or quotient data. -/

private theorem actualGradient_periodic {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : E2) (n : Fin 2 → ℤ) :
    gradient (actualField 2 L omega) (X + latticeVec 2 L n) =
      gradient (actualField 2 L omega) X := by
  have he : (fun Y : E2 => actualField 2 L omega (Y + latticeVec 2 L n)) =
      actualField 2 L omega :=
    funext (fun Y => actualField_periodic 2 hL omega Y n)
  have hd := congrArg (fun f : E2 → ℝ => fderiv ℝ f X) he
  rw [fderiv_comp_add_right] at hd
  exact congrArg (InnerProductSpace.toDual ℝ E2).symm hd

private theorem actualGradient_upperBounds {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) :
    ∃ A : ℝ, ∃ Kp : ℝ≥0, 0 ≤ A ∧
      (∀ X : E2, ‖gradient (actualField 2 L omega) X‖ ≤ A) ∧
      LipschitzWith Kp (gradient (actualField 2 L omega)) := by
  let q := coordinates 2
  let S := smoothSourceField 2 L omega
  let Cq : ℝ := ‖q.toContinuousLinearMap‖
  let G1 := I4SourceConditionalMajorant.sourceDerivativeMajorant L 1 omega
  let G2 := I4SourceConditionalMajorant.sourceDerivativeMajorant L 2 omega
  have hG1 : 0 ≤ G1 :=
    (norm_nonneg _).trans
      (I4SourceConditionalMajorant.smoothSourceField_global_derivative_bound hL.ne' 1 omega 0)
  have hG2 : 0 ≤ G2 :=
    (norm_nonneg _).trans
      (I4SourceConditionalMajorant.smoothSourceField_global_derivative_bound hL.ne' 2 omega 0)
  have hS : ContDiff ℝ (2 : ℕ∞) S := smoothSourceField_contDiff 2 hL.ne' omega 2
  have hSd : Differentiable ℝ S := hS.differentiable (by norm_num)
  have hSd' : Differentiable ℝ (fderiv ℝ S) :=
    (hS.fderiv_right (m := 1) (by norm_num)).differentiable (by norm_num)
  have hfirst (x : Fin 2 → ℝ) : ‖fderiv ℝ S x‖ ≤ G1 := by
    simpa only [norm_iteratedFDeriv_one] using
      I4SourceConditionalMajorant.smoothSourceField_global_derivative_bound hL.ne' 1 omega x
  have hsecond (x : Fin 2 → ℝ) : ‖fderiv ℝ (fderiv ℝ S) x‖ ≤ G2 := by
    rw [← norm_iteratedFDeriv_one (fderiv ℝ S), norm_iteratedFDeriv_fderiv]
    exact I4SourceConditionalMajorant.smoothSourceField_global_derivative_bound hL.ne' 2 omega x
  have hSLip : LipschitzWith (NNReal.mk G2 hG2) (fderiv ℝ S) := by
    apply lipschitzWith_of_nnnorm_fderiv_le hSd'
    intro x
    exact_mod_cast hsecond x
  have hchain (X : E2) : fderiv ℝ (actualField 2 L omega) X =
      (fderiv ℝ S (q X)).comp q.toContinuousLinearMap := by
    exact ((hSd (q X)).hasFDerivAt.comp X q.hasFDerivAt).fderiv
  let A : ℝ := 1 + Cq * G1
  let Kp : ℝ≥0 := NNReal.mk (Cq ^ 2 * G2) (mul_nonneg (sq_nonneg _) hG2)
  refine ⟨A, Kp, by dsimp [A, Cq]; positivity, ?_, ?_⟩
  · intro X
    calc
      ‖gradient (actualField 2 L omega) X‖ =
          ‖fderiv ℝ (actualField 2 L omega) X‖ :=
        (InnerProductSpace.toDual ℝ E2).symm.norm_map _
      _ = ‖(fderiv ℝ S (q X)).comp q.toContinuousLinearMap‖ := by rw [hchain]
      _ ≤ ‖fderiv ℝ S (q X)‖ * Cq :=
        (fderiv ℝ S (q X)).opNorm_comp_le q.toContinuousLinearMap
      _ ≤ G1 * Cq := mul_le_mul_of_nonneg_right (hfirst _) (norm_nonneg _)
      _ ≤ A := by dsimp [A]; nlinarith
  · apply LipschitzWith.of_dist_le_mul
    intro X Y
    have hR : ‖gradient (actualField 2 L omega) X -
        gradient (actualField 2 L omega) Y‖ =
        ‖fderiv ℝ (actualField 2 L omega) X -
          fderiv ℝ (actualField 2 L omega) Y‖ := by
      change ‖(InnerProductSpace.toDual ℝ E2).symm _ -
        (InnerProductSpace.toDual ℝ E2).symm _‖ = _
      rw [← map_sub, (InnerProductSpace.toDual ℝ E2).symm.norm_map]
    have he : (fderiv ℝ S (q X)).comp q.toContinuousLinearMap -
        (fderiv ℝ S (q Y)).comp q.toContinuousLinearMap =
        (fderiv ℝ S (q X) - fderiv ℝ S (q Y)).comp q.toContinuousLinearMap := by
      ext Z
      simp only [sub_apply, ContinuousLinearMap.comp_apply]
    have hq : dist (q X) (q Y) ≤ Cq * dist X Y := by
      change ‖q X - q Y‖ ≤ Cq * ‖X-Y‖
      rw [← map_sub]
      change ‖q.toContinuousLinearMap (X-Y)‖ ≤ ‖q.toContinuousLinearMap‖ * ‖X-Y‖
      exact q.toContinuousLinearMap.le_opNorm (X-Y)
    calc
      dist (gradient (actualField 2 L omega) X)
          (gradient (actualField 2 L omega) Y) =
          ‖fderiv ℝ (actualField 2 L omega) X -
            fderiv ℝ (actualField 2 L omega) Y‖ := by rw [dist_eq_norm, hR]
      _ = ‖(fderiv ℝ S (q X) - fderiv ℝ S (q Y)).comp q.toContinuousLinearMap‖ := by
        rw [hchain X, hchain Y, he]
      _ ≤ ‖fderiv ℝ S (q X) - fderiv ℝ S (q Y)‖ * Cq :=
        (fderiv ℝ S (q X) - fderiv ℝ S (q Y)).opNorm_comp_le q.toContinuousLinearMap
      _ ≤ (G2 * dist (q X) (q Y)) * Cq :=
        mul_le_mul_of_nonneg_right (by simpa only [dist_eq_norm, NNReal.coe_mk] using hSLip.dist_le_mul (q X) (q Y)) (norm_nonneg _)
      _ ≤ (G2 * (Cq * dist X Y)) * Cq :=
        mul_le_mul_of_nonneg_right (mul_le_mul_of_nonneg_left hq hG2) (norm_nonneg _)
      _ = (Kp : ℝ) * dist X Y := by simp only [Kp, NNReal.coe_mk]; ring

/-- Pointwise reduction into the CLOSED physical cell. No continuous representative is chosen. -/
private theorem physical_closedCell_representative {L : ℝ} (hL : 0 < L) (X : E2) :
    ∃ (Y : E2) (n : Fin 2 → ℤ),
      Y = X + latticeVec 2 L n ∧
      Y ∈ (coordinates 2).symm '' Set.pi Set.univ (fun _ : Fin 2 => Set.Icc (0 : ℝ) L) := by
  let n : Fin 2 → ℤ := fun i => -⌊coordinates 2 X i / L⌋
  let Y : E2 := X + latticeVec 2 L n
  refine ⟨Y, n, rfl, coordinates 2 Y, ?_, (coordinates 2).symm_apply_apply Y⟩
  intro i _
  have he : coordinates 2 Y i = L * Int.fract (coordinates 2 X i / L) := by
    change coordinates 2 (X + latticeVec 2 L n) i = L * Int.fract (coordinates 2 X i / L)
    rw [map_add, coordinates_latticeVec]
    simp only [Pi.add_apply, n, Int.cast_neg, Int.fract]
    field_simp [hL.ne']; ring
  rw [he]
  constructor
  · exact mul_nonneg hL.le (Int.fract_nonneg _)
  · calc
      L * Int.fract (coordinates 2 X i / L) ≤ L * 1 :=
        mul_le_mul_of_nonneg_left (Int.fract_lt_one _).le hL.le
      _ = L := mul_one L

private theorem actualGradient_closedBand_floor {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ)
    (hreg : ∀ X : E2, a ≤ actualField 2 L omega X →
      actualField 2 L omega X ≤ b → fderiv ℝ (actualField 2 L omega) X ≠ 0)
    (hne : ∃ X : E2, a ≤ actualField 2 L omega X ∧ actualField 2 L omega X ≤ b)
    (hpcont : Continuous (gradient (actualField 2 L omega))) :
    ∃ c : ℝ, 0 < c ∧ ∀ X : E2, a ≤ actualField 2 L omega X →
      actualField 2 L omega X ≤ b → c ≤ ‖gradient (actualField 2 L omega) X‖ ^ 2 := by
  let g := actualField 2 L omega
  let p := gradient g
  let cell : Set E2 :=
    (coordinates 2).symm '' Set.pi Set.univ (fun _ : Fin 2 => Set.Icc (0 : ℝ) L)
  let band : Set E2 := cell ∩ g ⁻¹' Set.Icc a b
  have hcell : IsCompact cell :=
    (isCompact_univ_pi (fun _ : Fin 2 => isCompact_Icc)).image (coordinates 2).symm.continuous
  have hgcont : Continuous g := (actualField_smooth 2 hL omega 0).continuous
  have hband : IsCompact band := hcell.inter_right (isClosed_Icc.preimage hgcont)
  have hbandne : band.Nonempty := by
    obtain ⟨X, ha, hb⟩ := hne
    obtain ⟨Y, n, hY, hcellY⟩ := physical_closedCell_representative hL X
    refine ⟨Y, hcellY, ?_⟩
    change a ≤ actualField 2 L omega Y ∧ actualField 2 L omega Y ≤ b
    rw [hY, actualField_periodic 2 hL omega X n]
    exact ⟨ha, hb⟩
  have hpos (X : E2) (hX : X ∈ band) : 0 < ‖p X‖ ^ 2 := by
    have hp : p X ≠ 0 := by
      intro hz
      apply hreg X hX.2.1 hX.2.2
      rw [← toDual_gradient]
      change (InnerProductSpace.toDual ℝ E2) (p X) = 0
      rw [hz, map_zero]
    exact pow_pos (norm_pos_iff.mpr hp) 2
  obtain ⟨Z, hZ, hmin⟩ := hband.exists_isMinOn hbandne
    (hpcont.norm.pow 2).continuousOn
  refine ⟨‖p Z‖ ^ 2, hpos Z hZ, ?_⟩
  intro X ha hb
  obtain ⟨Y, n, hY, hcellY⟩ := physical_closedCell_representative hL X
  have hYband : Y ∈ band := by
    refine ⟨hcellY, ?_⟩
    change a ≤ actualField 2 L omega Y ∧ actualField 2 L omega Y ≤ b
    rw [hY, actualField_periodic 2 hL omega X n]
    exact ⟨ha, hb⟩
  calc
    ‖p Z‖ ^ 2 ≤ ‖p Y‖ ^ 2 := (isMinOn_iff.mp hmin) Y hYband
    _ = ‖p X‖ ^ 2 := by
      change ‖gradient (actualField 2 L omega) Y‖ ^ 2 =
        ‖gradient (actualField 2 L omega) X‖ ^ 2
      rw [hY, actualGradient_periodic hL omega X n]

private theorem actualNormalizedVelocity_estimates {L : ℝ} (omega : SmoothSample 2 L)
    (c A : ℝ) (Kp : ℝ≥0) (hc : 0 < c) (hA : 0 ≤ A)
    (hbound : ∀ X : E2, ‖gradient (actualField 2 L omega) X‖ ≤ A)
    (hplip : LipschitzWith Kp (gradient (actualField 2 L omega))) :
    ∃ M K : ℝ≥0,
      (∀ X : E2, ‖normalizedVelocity (actualField 2 L omega) c X‖ ≤ (M : ℝ)) ∧
      LipschitzWith K (normalizedVelocity (actualField 2 L omega) c) := by
  let p := gradient (actualField 2 L omega)
  let d : E2 → ℝ := fun X => max c (‖p X‖ ^ 2)
  let D : ℝ := 2 * A * (Kp : ℝ)
  have hD : 0 ≤ D := by dsimp [D]; positivity
  have hdlower (X : E2) : c ≤ d X := le_max_left _ _
  have hdpos (X : E2) : 0 < d X := hc.trans_le (hdlower X)
  have hdinv (X : E2) : |(d X)⁻¹| ≤ 1/c := by
    rw [abs_of_pos (inv_pos.mpr (hdpos X))]
    simpa only [one_div] using one_div_le_one_div_of_le hc (hdlower X)
  have hsq : LipschitzWith (NNReal.mk D hD) (fun X : E2 => ‖p X‖ ^ 2) := by
    apply LipschitzWith.of_dist_le_mul
    intro X Y
    have hdiff : |‖p X‖ - ‖p Y‖| ≤ (Kp : ℝ) * dist X Y :=
      (abs_norm_sub_norm_le (p X) (p Y)).trans
        (by simpa only [dist_eq_norm] using hplip.dist_le_mul X Y)
    have hsum : ‖p X‖ + ‖p Y‖ ≤ 2*A := by linarith [hbound X, hbound Y]
    calc
      dist (‖p X‖ ^ 2) (‖p Y‖ ^ 2) =
          |‖p X‖ - ‖p Y‖| * (‖p X‖ + ‖p Y‖) := by
        rw [Real.dist_eq, sq_sub_sq, abs_mul,
          abs_of_nonneg (add_nonneg (norm_nonneg _) (norm_nonneg _))]; ring
      _ ≤ ((Kp : ℝ) * dist X Y) * (2*A) :=
        mul_le_mul hdiff hsum (add_nonneg (norm_nonneg _) (norm_nonneg _))
          (mul_nonneg Kp.2 dist_nonneg)
      _ = D * dist X Y := by dsimp [D]; ring
  have hdlip : LipschitzWith (NNReal.mk D hD) d := hsq.const_max c
  have hrecip (X Y : E2) : |(d X)⁻¹ - (d Y)⁻¹| ≤
      (D/(c*c)) * dist X Y := by
    have hprod : c*c ≤ d X*d Y :=
      mul_le_mul (hdlower X) (hdlower Y) hc.le (hdpos X).le
    calc
      |(d X)⁻¹ - (d Y)⁻¹| = dist (d X) (d Y) / (d X*d Y) := by
        simpa only [Real.dist_eq, Real.norm_eq_abs, abs_of_pos (hdpos X),
          abs_of_pos (hdpos Y)] using
          (dist_inv_inv₀ (hdpos X).ne' (hdpos Y).ne')
      _ ≤ dist (d X) (d Y) / (c*c) :=
        div_le_div_of_nonneg_left dist_nonneg (mul_pos hc hc) hprod
      _ ≤ (D * dist X Y) / (c*c) :=
        div_le_div_of_nonneg_right (by simpa only [NNReal.coe_mk] using hdlip.dist_le_mul X Y) (mul_nonneg hc.le hc.le)
      _ = (D/(c*c)) * dist X Y := by ring
  let M : ℝ≥0 := NNReal.mk (A/c) (div_nonneg hA hc.le)
  let K : ℝ≥0 := NNReal.mk ((Kp : ℝ)/c + (D/(c*c))*A) (by positivity)
  refine ⟨M, K, ?_, ?_⟩
  · intro X
    change ‖(d X)⁻¹ • p X‖ ≤ A/c
    rw [norm_smul, Real.norm_eq_abs]
    calc
      |(d X)⁻¹| * ‖p X‖ ≤ (1/c)*A :=
        mul_le_mul (hdinv X) (hbound X) (norm_nonneg _) (by positivity)
      _ = A/c := by ring
  · apply LipschitzWith.of_dist_le_mul
    intro X Y
    have hv : normalizedVelocity (actualField 2 L omega) c X -
        normalizedVelocity (actualField 2 L omega) c Y =
        (d X)⁻¹ • (p X-p Y) + ((d X)⁻¹-(d Y)⁻¹) • p Y := by
      change (d X)⁻¹ • p X - (d Y)⁻¹ • p Y = _
      rw [smul_sub, sub_smul]
      exact (sub_add_sub_cancel ((d X)⁻¹ • p X) ((d X)⁻¹ • p Y)
        ((d Y)⁻¹ • p Y)).symm
    calc
      dist (normalizedVelocity (actualField 2 L omega) c X)
          (normalizedVelocity (actualField 2 L omega) c Y) =
          ‖(d X)⁻¹ • (p X-p Y) + ((d X)⁻¹-(d Y)⁻¹) • p Y‖ := by
        rw [dist_eq_norm, hv]
      _ ≤ |(d X)⁻¹| * ‖p X-p Y‖ + |(d X)⁻¹-(d Y)⁻¹| * ‖p Y‖ := by
        simpa only [norm_smul, Real.norm_eq_abs] using norm_add_le
          ((d X)⁻¹ • (p X-p Y)) (((d X)⁻¹-(d Y)⁻¹) • p Y)
      _ ≤ (1/c) * ((Kp : ℝ)*dist X Y) + ((D/(c*c))*dist X Y)*A :=
        add_le_add
          (mul_le_mul (hdinv X)
            (by simpa only [dist_eq_norm] using hplip.dist_le_mul X Y)
            (norm_nonneg _) (by positivity))
          (mul_le_mul (hrecip X Y) (hbound Y) (norm_nonneg _) (by positivity))
      _ = (K : ℝ)*dist X Y := by simp only [K, NNReal.coe_mk]; ring

private theorem normalizedFieldData {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hreg : ∀ X : E2, a ≤ actualField 2 L omega X →
      actualField 2 L omega X ≤ b → fderiv ℝ (actualField 2 L omega) X ≠ 0)
    (hne : ∃ X : E2, a ≤ actualField 2 L omega X ∧ actualField 2 L omega X ≤ b) :
    ∃ c A : ℝ, ∃ Kp M K : ℝ≥0, NormalizedFieldFacts omega a b c A Kp M K := by
  have _ : a ≤ b := hab
  obtain ⟨A, Kp, hA, hpbound, hplip⟩ := actualGradient_upperBounds hL omega
  obtain ⟨c, hc, hfloor⟩ := actualGradient_closedBand_floor hL omega a b hreg hne hplip.continuous
  obtain ⟨M, K, hVbound, hVlip⟩ :=
    actualNormalizedVelocity_estimates omega c A Kp hc hA hpbound hplip
  have hspeed (X : E2) : fderiv ℝ (actualField 2 L omega) X
      (normalizedVelocity (actualField 2 L omega) c X) =
      ‖gradient (actualField 2 L omega) X‖ ^ 2 /
        max c (‖gradient (actualField 2 L omega) X‖ ^ 2) := by
    rw [normalizedVelocity, map_smul, smul_eq_mul, ← inner_gradient_left,
      real_inner_self_eq_norm_sq]
    ring
  refine ⟨c, A, Kp, M, K, ?_⟩
  change 0 < c ∧ 0 ≤ A ∧ _
  refine ⟨hc, hA, hpbound, hplip, actualGradient_periodic hL omega, hfloor,
    hVbound, hVlip, ?_, hspeed, ?_, ?_⟩
  · intro X n
    simp only [normalizedVelocity, actualGradient_periodic hL omega X n]
  · intro X
    rw [hspeed]
    have hd : 0 < max c (‖gradient (actualField 2 L omega) X‖ ^ 2) :=
      hc.trans_le (le_max_left _ _)
    exact ⟨div_nonneg (sq_nonneg _) hd.le,
      (div_le_one hd).mpr (le_max_right _ _)⟩
  · intro X ha hb
    rw [hspeed, max_eq_right (hfloor X ha hb)]
    exact div_self (ne_of_gt (hc.trans_le (hfloor X ha hb)))


/-
Stage62 Helper B. Complete original private finite-horizon construction.
Exact lexical input: CONTEXT.ORIGINAL.md, shared context001.
Unelaborated TEXT only; helper executes no Lean/probe/build/check/hash.
-/

private theorem finiteHorizon_curve_unique
    (V : E2 → E2) (K : ℝ≥0) (hlip : LipschitzWith K V)
    (D : ℝ) (hD : 0 < D) (f g : ℝ → E2)
    (hf : ∀ t ∈ Set.Icc (-D) D,
      HasDerivWithinAt f (V (f t)) (Set.Icc (-D) D) t)
    (hg : ∀ t ∈ Set.Icc (-D) D,
      HasDerivWithinAt g (V (g t)) (Set.Icc (-D) D) t)
    (heq : f 0 = g 0) : Set.EqOn f g (Set.Icc (-D) D) := by
  have hfc : ContinuousOn f (Set.Icc (-D) D) :=
    fun t ht => (hf t ht).continuousWithinAt
  have hgc : ContinuousOn g (Set.Icc (-D) D) :=
    fun t ht => (hg t ht).continuousWithinAt
  exact ODE_solution_unique_of_mem_Icc
    (v := fun _ => V) (s := fun _ => Set.univ) (K := K)
    (a := -D) (b := D) (t₀ := (0 : ℝ))
    (fun _ _ => hlip.lipschitzOnWith)
    ⟨by linarith, hD⟩
    hfc
    (fun t ht => (hf t (Set.Ioo_subset_Icc_self ht)).hasDerivAt
      (Icc_mem_nhds ht.1 ht.2))
    (fun _ _ => Set.mem_univ _)
    hgc
    (fun t ht => (hg t (Set.Ioo_subset_Icc_self ht)).hasDerivAt
      (Icc_mem_nhds ht.1 ht.2))
    (fun _ _ => Set.mem_univ _)
    heq

private theorem boundedFiniteHorizonFamily {L : ℝ} (V : E2 → E2) (M K : ℝ≥0)
    (hbound : ∀ X : E2, ‖V X‖ ≤ (M : ℝ)) (hlip : LipschitzWith K V)
    (hper : ∀ (X : E2) (n : Fin 2 → ℤ), V (X + latticeVec 2 L n) = V X)
    (T : ℝ) (hT : 0 ≤ T) :
    ∃ H : ℝ → E2 → E2, FiniteHorizonFacts L V T H := by
  classical
  let D : ℝ := T + 1
  have hD : 0 < D := by
    dsimp [D]
    linarith
  let zeroTime : Set.Icc (-D) D := ⟨0, by constructor <;> linarith⟩
  let outer : ℝ≥0 := 1 + M * NNReal.mk D (le_of_lt hD)
  have hlocal (Z : E2) :
      ∃ alpha : E2 × ℝ → E2,
        (∀ X ∈ Metric.closedBall Z (1 : ℝ), alpha (X, 0) = X ∧
          ∀ t ∈ Set.Icc (-D) D,
            HasDerivWithinAt (fun u => alpha (X, u))
              (V (alpha (X, t))) (Set.Icc (-D) D) t) ∧
        ContinuousOn alpha (Metric.closedBall Z (1 : ℝ) ×ˢ Set.Icc (-D) D) := by
    have hpic : IsPicardLindelof (fun _ => V) zeroTime Z outer 1 M K := by
      apply IsPicardLindelof.of_time_independent
      · intro X _hX
        exact hbound X
      · exact hlip.lipschitzOnWith
      · change (M : ℝ) * max (D - 0) (0 - -D) ≤ (outer : ℝ) - 1
        simp [outer]
    exact hpic.exists_forall_mem_closedBall_eq_hasDerivWithinAt_continuousOn
  let alpha : E2 → E2 × ℝ → E2 := fun Z => Classical.choose (hlocal Z)
  have halpha (Z : E2) :
      ∀ X ∈ Metric.closedBall Z (1 : ℝ), alpha Z (X, 0) = X ∧
        ∀ t ∈ Set.Icc (-D) D,
          HasDerivWithinAt (fun u => alpha Z (X, u))
            (V (alpha Z (X, t))) (Set.Icc (-D) D) t :=
    (Classical.choose_spec (hlocal Z)).1
  have halphaContinuous (Z : E2) :
      ContinuousOn (alpha Z) (Metric.closedBall Z (1 : ℝ) ×ˢ Set.Icc (-D) D) :=
    (Classical.choose_spec (hlocal Z)).2
  let H : ℝ → E2 → E2 := fun t X => alpha X (X, t)
  have hHinitial (X : E2) : H 0 X = X :=
    (halpha X X (Metric.mem_closedBall_self (by norm_num))).1
  have hHwithin (X : E2) (t : ℝ) (ht : t ∈ Set.Icc (-D) D) :
      HasDerivWithinAt (fun u => H u X) (V (H t X)) (Set.Icc (-D) D) t :=
    (halpha X X (Metric.mem_closedBall_self (by norm_num))).2 t ht
  have hcompare (Z Y : E2) (hY : Y ∈ Metric.closedBall Z (1 : ℝ)) :
      Set.EqOn (fun t => H t Y) (fun t => alpha Z (Y, t)) (Set.Icc (-D) D) := by
    apply finiteHorizon_curve_unique V K hlip D hD
      (fun t => H t Y) (fun t => alpha Z (Y, t))
    · exact hHwithin Y
    · exact (halpha Z Y hY).2
    · exact (hHinitial Y).trans (halpha Z Y hY).1.symm
  have htimeInterior (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) T) :
      t ∈ Set.Ioo (-D) D := by
    constructor <;> dsimp [D] <;> linarith [ht.1, ht.2]
  have hHjoint : ContinuousOn (fun z : E2 × ℝ => H z.2 z.1)
      (Set.univ ×ˢ Set.Icc (0 : ℝ) T) := by
    intro z hz
    have hti := htimeInterior z.2 hz.2
    have hneigh :
        Metric.closedBall z.1 (1 : ℝ) ×ˢ Set.Icc (-D) D ∈ 𝓝 z :=
      prod_mem_nhds (Metric.closedBall_mem_nhds z.1 (by norm_num))
        (Icc_mem_nhds hti.1 hti.2)
    have hzin : z ∈ Metric.closedBall z.1 (1 : ℝ) ×ˢ Set.Icc (-D) D :=
      ⟨Metric.mem_closedBall_self (by norm_num), Set.Ioo_subset_Icc_self hti⟩
    have halphaAt : ContinuousAt (alpha z.1) z :=
      ((halphaContinuous z.1).continuousWithinAt hzin).continuousAt hneigh
    have hevent : (fun w : E2 × ℝ => H w.2 w.1) =ᶠ[𝓝 z] alpha z.1 := by
      exact Filter.Eventually.mono hneigh fun w hw =>
        (hcompare z.1 w.1 hw.1) hw.2
    exact (halphaAt.congr_of_eventuallyEq hevent).continuousWithinAt
  have hHfull (X : E2) (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) T) :
      HasDerivAt (fun u => H u X) (V (H t X)) t := by
    have hti := htimeInterior t ht
    exact (hHwithin X t (Set.Ioo_subset_Icc_self hti)).hasDerivAt
      (Icc_mem_nhds hti.1 hti.2)
  have hHequiv (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) T)
      (X : E2) (n : Fin 2 → ℤ) :
      H t (X + latticeVec 2 L n) = H t X + latticeVec 2 L n := by
    let lambda : E2 := latticeVec 2 L n
    have htranslate (u : ℝ) (hu : u ∈ Set.Icc (-D) D) :
        HasDerivWithinAt (fun v => H v X + lambda)
          (V (H u X + lambda)) (Set.Icc (-D) D) u := by
      change HasDerivWithinAt (fun v => H v X + lambda)
        (V (H u X + latticeVec 2 L n)) (Set.Icc (-D) D) u
      rw [hper (H u X) n]
      exact (hHwithin X u hu).add_const lambda
    have heq : Set.EqOn (fun u => H u (X + lambda))
        (fun u => H u X + lambda) (Set.Icc (-D) D) := by
      apply finiteHorizon_curve_unique V K hlip D hD
        (fun u => H u (X + lambda)) (fun u => H u X + lambda)
      · exact hHwithin (X + lambda)
      · exact htranslate
      · rw [hHinitial, hHinitial]
    exact heq (Set.Ioo_subset_Icc_self (htimeInterior t ht))
  exact ⟨H, hHinitial, hHjoint, hHfull, hHequiv⟩


/- Complete PRIVATE height/hitting section62C. Insert once inside the
frozen I4SourceActualTorusRegularSlab context. Common definitions belong
to the producer. No imports/namespace/end or helper executions. -/

private theorem height_scalar_increment_bounds
    (f v : ℝ → ℝ) (t lower upper : ℝ) (ht : 0 ≤ t)
    (hd : ∀ u ∈ Icc (0:ℝ) t, HasDerivAt f (v u) u)
    (hv : ∀ u ∈ Icc (0:ℝ) t, lower ≤ v u ∧ v u ≤ upper) :
    lower*t ≤ f t-f 0 ∧ f t-f 0 ≤ upper*t := by
  have hcont : ContinuousOn f (Icc (0:ℝ) t) := by
    intro u hu
    exact (hd u hu).continuousAt.continuousWithinAt
  have hdiff : DifferentiableOn ℝ f (interior (Icc (0:ℝ) t)) := by
    intro u hu
    exact (hd u (interior_subset hu)).differentiableAt.differentiableWithinAt
  have hlo := (convex_Icc (0 : ℝ) t).mul_sub_le_image_sub_of_le_deriv
    hcont hdiff (C:=lower) (fun u hu => by
      rw [(hd u (interior_subset hu)).deriv]
      exact (hv u (interior_subset hu)).1)
    0 ⟨le_rfl,ht⟩ t ⟨ht,le_rfl⟩ ht
  have hhi := (convex_Icc (0 : ℝ) t).image_sub_le_mul_sub_of_deriv_le
    hcont hdiff (C:=upper) (fun u hu => by
      rw [(hd u (interior_subset hu)).deriv]
      exact (hv u (interior_subset hu)).2)
    0 ⟨le_rfl,ht⟩ t ⟨ht,le_rfl⟩ ht
  exact ⟨by simpa only [sub_zero] using hlo,by simpa only [sub_zero] using hhi⟩

private theorem heightHittingData {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (c A : ℝ) (Kp M K : ℝ≥0) (H : ℝ → E2 → E2)
    (hfield : NormalizedFieldFacts omega a b c A Kp M K)
    (hfamily : FiniteHorizonFacts L
      (normalizedVelocity (actualField 2 L omega) c) (b-a) H) :
    ∃ Rcover : CoverSuperlevel omega a → CoverSuperlevel omega b,
      HeightHittingFacts omega a b hab H Rcover := by
  let g : E2 → ℝ := actualField 2 L omega
  let V : E2 → E2 := normalizedVelocity g c
  dsimp only [NormalizedFieldFacts] at hfield
  rcases hfield with ⟨_hc,_hA,_hpbound,_hplip,_hpper,_hfloor,
    _hVbound,_hVlip,_hVper,_hspeedFormula,hspeed,hbandSpeed⟩
  rcases hfamily with ⟨hzero,hjoint,hODE,htranslate⟩
  have hg : Differentiable ℝ g :=
    (actualField_smooth 2 hL omega 1).differentiable (by norm_num)
  have hgcont : Continuous g := hg.continuous
  have hheight : ∀ (X : E2) (t : ℝ), t ∈ Icc (0:ℝ) (b-a) →
      HasDerivAt (fun u => g (H u X)) (fderiv ℝ g (H t X) (V (H t X))) t := by
    intro X t ht
    simpa only [Function.comp_def] using
      (hg (H t X)).hasFDerivAt.comp_hasDerivAt t (hODE X t ht)

  /- Unconditional GLOBAL barriers are proved first. No band residence or
  no-exit hypothesis enters this comparison. Full derivatives include0/T. -/
  have hbarriers : ∀ (X : E2) (t : ℝ), t ∈ Icc (0:ℝ) (b-a) →
      g X ≤ g (H t X) ∧ g (H t X) ≤ g X+t := by
    intro X t ht
    have hsub : Icc (0:ℝ) t ⊆ Icc (0:ℝ) (b-a) :=
      fun u hu => ⟨hu.1,hu.2.trans ht.2⟩
    obtain ⟨hlo,hhi⟩ := height_scalar_increment_bounds
      (fun u => g (H u X))
      (fun u => fderiv ℝ g (H u X) (V (H u X))) t 0 1 ht.1
      (fun u hu => hheight X u (hsub hu))
      (fun u _hu => hspeed (H u X))
    rw [hzero X] at hlo hhi
    constructor <;> linarith

  /- The preceding barriers place EVERY intermediate time in the CLOSED
  band before its unit speed is used. This is the noncircular arrival join. -/
  have hunit : ∀ X : E2, a ≤ g X → g X ≤ b → ∀ t : ℝ,
      0 ≤ t → t ≤ b-g X → g (H t X)=g X+t := by
    intro X hXa hXb t ht htend
    have htT : t ≤ b-a := by linarith
    have hresidence : ∀ u ∈ Icc (0:ℝ) t, a ≤ g (H u X) ∧ g (H u X) ≤ b := by
      intro u hu
      obtain ⟨hlo,hhi⟩ := hbarriers X u ⟨hu.1,hu.2.trans htT⟩
      exact ⟨hXa.trans hlo,by linarith [hu.2]⟩
    obtain ⟨hlo,hhi⟩ := height_scalar_increment_bounds
      (fun u => g (H u X))
      (fun u => fderiv ℝ g (H u X) (V (H u X))) t 1 1 ht
      (fun u hu => hheight X u ⟨hu.1,hu.2.trans htT⟩)
      (fun u hu => by
        have hstay := hresidence u hu
        have hs := hbandSpeed (H u X) hstay.1 hstay.2
        exact ⟨hs.ge,hs.le⟩)
    rw [hzero X] at hlo hhi
    linarith

  let tau : CoverSuperlevel omega a → ℝ := fun X => max 0 (b-g X.val)
  have htau : ∀ X : CoverSuperlevel omega a, tau X ∈ Icc (0:ℝ) (b-a) := by
    intro X
    refine ⟨le_max_left _ _,max_le ?_ ?_⟩
    · exact sub_nonneg.mpr hab
    · have hXa : a ≤ g X.val := X.property
      linarith
  have htau_cont : Continuous tau :=
    continuous_const.max (continuous_const.sub (hgcont.comp continuous_subtype_val))
  have heval_cont : Continuous (fun X : CoverSuperlevel omega a => H (tau X) X.val) := by
    have hh := hjoint.comp_continuous
      (continuous_subtype_val.prodMk htau_cont)
      (fun X : CoverSuperlevel omega a => ⟨Set.mem_univ _,htau X⟩)
    simpa only [Function.comp_def] using hh
  have hlands : ∀ X : CoverSuperlevel omega a, b ≤ g (H (tau X) X.val) := by
    intro X
    by_cases hupper : b ≤ g X.val
    · have ht0 : tau X=0 := max_eq_left (sub_nonpos.mpr hupper)
      rw [ht0,hzero]
      exact hupper
    · have hXb : g X.val ≤ b := (lt_of_not_ge hupper).le
      have htaueq : tau X=b-g X.val := max_eq_right (sub_nonneg.mpr hXb)
      rw [htaueq,hunit X.val X.property hXb (b-g X.val)
        (sub_nonneg.mpr hXb) le_rfl]
      linarith
  let Rcover : CoverSuperlevel omega a → CoverSuperlevel omega b :=
    fun X => ⟨H (tau X) X.val,hlands X⟩
  have hRcont : Continuous Rcover := heval_cont.subtype_mk hlands
  refine ⟨Rcover,?_⟩
  dsimp only [HeightHittingFacts]
  refine ⟨hbarriers,hunit,hRcont,?_,?_,?_,?_⟩
  · intro X
    rfl
  · intro X
    apply Subtype.ext
    change H (tau ⟨X.val,hab.trans X.property⟩) X.val=X.val
    have ht0 : tau ⟨X.val,hab.trans X.property⟩=0 :=
      max_eq_left (sub_nonpos.mpr X.property)
    rw [ht0,hzero]
  · intro X
    have htime : ∀ s ∈ Icc (0:ℝ) 1, s*tau X ∈ Icc (0:ℝ) (b-a) := by
      intro s hs
      refine ⟨mul_nonneg hs.1 (htau X).1,?_⟩
      have hh := mul_le_mul_of_nonneg_right hs.2 (htau X).1
      have hh' : s*tau X ≤ tau X := by simpa only [one_mul] using hh
      exact hh'.trans (htau X).2
    have hcurve : ContinuousOn (fun s : ℝ => H (s*tau X) X.val) (Icc (0:ℝ) 1) := by
      have hmap : Continuous (fun s : ℝ => (X.val,s*tau X)) :=
        continuous_const.prodMk (continuous_id.mul continuous_const)
      have hh := hjoint.comp
        hmap.continuousOn
        (fun s hs => ⟨Set.mem_univ _,htime s hs⟩)
      simpa only [Function.comp_def] using hh
    apply JoinedIn.ofLine hcurve
    · simpa only [zero_mul] using hzero X.val
    · simp only [one_mul]
      rfl
    · rintro Y ⟨s,hs,rfl⟩
      exact X.property.trans (hbarriers X.val (s*tau X) (htime s hs)).1
  · intro X Y n hYX
    have hperiod : g (X.val+latticeVec 2 L n)=g X.val :=
      actualField_periodic 2 hL omega X.val n
    have htXY : tau Y=tau X := by
      change max 0 (b-g Y.val)=max 0 (b-g X.val)
      rw [hYX,hperiod]
    change H (tau Y) Y.val=H (tau X) X.val+latticeVec 2 L n
    rw [htXY,hYX]
    exact htranslate (tau X) (htau X) X.val n


private theorem zeroWidth_componentBijective {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -a) (t := -a) (neg_le_neg (le_refl a))) := by
  rw [TorusFiltration.superlevel_componentInclusion_id]
  exact Function.bijective_id

private theorem emptyBand_componentBijective {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hempty : ∀ X : E2, ¬ (a ≤ actualField 2 L omega X ∧ actualField 2 L omega X ≤ b)) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab)) := by
  let F := SourceActualFoldTorus.actualTorusField hL.ne' omega
  have hsame (q : I4Torus.SourceTorus 2 L) (ha : a ≤ F q) : b ≤ F q := by
    by_contra hb
    have hlt : F q < b := lt_of_not_ge hb
    obtain ⟨x,hx⟩ := SourceActualFoldTorus.torusProjection2L_surjective L q
    let X : E2 := (coordinates 2).symm x
    have hp : actualField 2 L omega X = F q := by
      change smoothSourceField 2 L omega (coordinates 2 ((coordinates 2).symm x)) = F q
      rw [ContinuousLinearEquiv.apply_symm_apply]
      exact (SourceActualFoldTorus.actualTorusField_pullback hL.ne' omega x).symm.trans
        (congrArg F hx)
    exact hempty X ⟨by simpa only [hp] using ha, by simpa only [hp] using hlt.le⟩
  let r : C(TorusFiltration.superlevel_set F (-a),
      TorusFiltration.superlevel_set F (-b)) :=
    ⟨fun q => ⟨q.val, by
      have hq : a ≤ F q.val := by
        simpa only [TorusFiltration.superlevel_set, Set.mem_ofPred_eq, neg_neg] using q.property
      simpa only [TorusFiltration.superlevel_set, Set.mem_ofPred_eq, neg_neg] using hsame q.val hq⟩,
      by fun_prop⟩
  let R := TorusFiltration.superlevel_componentMap r
  have hleft : Function.LeftInverse R
      (TorusFiltration.superlevel_componentInclusion F (s := -b) (t := -a) (neg_le_neg hab)) := by
    intro q
    obtain ⟨x,rfl⟩ := ZerothHomotopy.mk_surjective q
    rfl
  have hright : Function.RightInverse R
      (TorusFiltration.superlevel_componentInclusion F (s := -b) (t := -a) (neg_le_neg hab)) := by
    intro q
    obtain ⟨x,rfl⟩ := ZerothHomotopy.mk_surjective q
    rfl
  exact ⟨hleft.injective,hright.surjective⟩

private def restrictedProjection {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    CoverSuperlevel omega a → TorusSuperlevel hL omega a :=
  fun X => ⟨coverProjection L X.val, by
    change a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega
      (I4Torus.torusProjection 2 L (coordinates 2 X.val))
    rw [SourceActualFoldTorus.actualTorusField_pullback]
    exact X.property⟩

private theorem restrictedProjection_continuous {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    Continuous (restrictedProjection hL omega a) := by
  apply Continuous.subtype_mk
  exact ((SourceActualFoldTorus.torusProjection2L_continuous L).comp
    (coordinates 2).continuous).comp continuous_subtype_val

private theorem restrictedProjection_surjective {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    Function.Surjective (restrictedProjection hL omega a) := by
  intro q
  obtain ⟨x,hx⟩ := SourceActualFoldTorus.torusProjection2L_surjective L q.val
  let X : E2 := (coordinates 2).symm x
  have hproj : coverProjection L X = q.val := by
    simpa only [coverProjection,X,ContinuousLinearEquiv.apply_symm_apply] using hx
  have hmem : a ≤ actualField 2 L omega X := by
    have hp := SourceActualFoldTorus.actualTorusField_pullback hL.ne' omega (coordinates 2 X)
    change SourceActualFoldTorus.actualTorusField hL.ne' omega (coverProjection L X) = _ at hp
    rw [hproj] at hp
    have hq : a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega q.val := q.property
    simpa only [actualField,hp] using hq
  refine ⟨⟨X,hmem⟩,?_⟩
  apply Subtype.ext
  exact hproj

private theorem restrictedProjectionQuotient {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) :
    Continuous (restrictedProjection hL omega a) ∧
      IsOpenMap (restrictedProjection hL omega a) ∧
      Function.Surjective (restrictedProjection hL omega a) ∧
      Topology.IsQuotientMap (restrictedProjection hL omega a) := by
  have hopen : IsOpenMap (coverProjection L) :=
    (SourceActualFoldTorus.torusProjection2L_open L).comp (coordinates 2).isOpenMap
  have hopenRestricted : IsOpenMap (restrictedProjection hL omega a) := by
    intro S hS
    obtain ⟨U,hU,hUS⟩ := isOpen_induced_iff.mp hS
    have heq : restrictedProjection hL omega a '' S =
        Subtype.val ⁻¹' (coverProjection L '' U) := by
      ext q
      constructor
      · rintro ⟨X,hXS,rfl⟩
        refine ⟨X.val,?_,rfl⟩
        simpa only [← hUS,Set.mem_preimage] using hXS
      · rintro ⟨X,hXU,hXq⟩
        have hp : actualField 2 L omega X =
            SourceActualFoldTorus.actualTorusField hL.ne' omega q.val := by
          calc
            _ = SourceActualFoldTorus.actualTorusField hL.ne' omega (coverProjection L X) :=
              (SourceActualFoldTorus.actualTorusField_pullback hL.ne' omega (coordinates 2 X)).symm
            _ = _ := congrArg _ hXq
        have hmem : a ≤ actualField 2 L omega X := by
          rw [hp]
          exact q.property
        refine ⟨⟨X,hmem⟩,?_,?_⟩
        · simpa only [← hUS,Set.mem_preimage] using hXU
        · apply Subtype.ext
          exact hXq
    rw [heq]
    exact (hopen U hU).preimage continuous_subtype_val
  have hcont := restrictedProjection_continuous hL omega a
  have hsurj := restrictedProjection_surjective hL omega a
  exact ⟨hcont,hopenRestricted,hsurj,hopenRestricted.isQuotientMap hcont hsurj⟩


private theorem coverProjection_eq_lattice {L : ℝ} (X Y : E2)
    (h : coverProjection L X = coverProjection L Y) :
    ∃ n : Fin 2 → ℤ, Y = X + latticeVec 2 L n := by
  classical
  have hz (i : Fin 2) : ∃ n : ℤ, n • L = coordinates 2 Y i - coordinates 2 X i := by
    apply (AddCircle.coe_eq_zero_iff (p := L)).mp
    rw [AddCircle.coe_sub]
    exact sub_eq_zero.mpr (congrFun h i).symm
  choose n hn using hz
  refine ⟨n,?_⟩
  apply (coordinates 2).injective
  rw [map_add,coordinates_latticeVec]
  funext i
  have hi := hn i
  rw [zsmul_eq_mul] at hi
  change coordinates 2 Y i = coordinates 2 X i + L*(n i : ℝ)
  linarith

private theorem coverProjection_add_lattice (L : ℝ) (X : E2) (n : Fin 2 → ℤ) :
    coverProjection L (X + latticeVec 2 L n) = coverProjection L X := by
  ext i
  change ((coordinates 2 (X + latticeVec 2 L n) i : ℝ) : AddCircle L) =
    ((coordinates 2 X i : ℝ) : AddCircle L)
  rw [map_add,coordinates_latticeVec]
  change ((coordinates 2 X i + L*(n i : ℝ) : ℝ) : AddCircle L) =
    ((coordinates 2 X i : ℝ) : AddCircle L)
  rw [AddCircle.coe_add]
  have hz : ((L*(n i : ℝ) : ℝ) : AddCircle L) = 0 := by
    apply (AddCircle.coe_eq_zero_iff (p := L)).mpr
    refine ⟨n i,?_⟩
    rw [zsmul_eq_mul]
    ring
  rw [hz,add_zero]

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
        R (restrictedProjection hL omega a X) = restrictedProjection hL omega b (Rcover X)) := by
  classical
  dsimp only [HeightHittingFacts] at hcover
  rcases hcover with ⟨_hbarriers,_hunit,hRcoverCont,_hformula,hfix,hpoint,htranslate⟩
  obtain ⟨hpaCont,_hpaOpen,hpaSurj,hpaQuot⟩ := restrictedProjectionQuotient hL omega a
  obtain ⟨hpbCont,_hpbOpen,hpbSurj,_hpbQuot⟩ := restrictedProjectionQuotient hL omega b
  have hfiber (X Y : CoverSuperlevel omega a)
      (hXY : restrictedProjection hL omega a X = restrictedProjection hL omega a Y) :
      restrictedProjection hL omega b (Rcover X) = restrictedProjection hL omega b (Rcover Y) := by
    obtain ⟨n,hn⟩ := coverProjection_eq_lattice X.val Y.val (congrArg Subtype.val hXY)
    have hR := htranslate X Y n hn
    apply Subtype.ext
    change coverProjection L (Rcover X).val = coverProjection L (Rcover Y).val
    rw [hR]
    exact (coverProjection_add_lattice L (Rcover X).val n).symm
  let liftA : TorusSuperlevel hL omega a → CoverSuperlevel omega a :=
    fun q => Classical.choose (hpaSurj q)
  have hlift (q : TorusSuperlevel hL omega a) :
      restrictedProjection hL omega a (liftA q) = q := Classical.choose_spec (hpaSurj q)
  let R : TorusSuperlevel hL omega a → TorusSuperlevel hL omega b :=
    fun q => restrictedProjection hL omega b (Rcover (liftA q))
  have hcomp (X : CoverSuperlevel omega a) :
      R (restrictedProjection hL omega a X) = restrictedProjection hL omega b (Rcover X) :=
    hfiber _ X (hlift (restrictedProjection hL omega a X))
  have hRcont : Continuous R := by
    apply hpaQuot.continuous_iff.mpr
    have heq : R ∘ restrictedProjection hL omega a =
        restrictedProjection hL omega b ∘ Rcover := funext hcomp
    rw [heq]
    exact hpbCont.comp hRcoverCont
  have hRfix (q : TorusSuperlevel hL omega b) : R ⟨q.val,hab.trans q.property⟩ = q := by
    obtain ⟨X,hXq⟩ := hpbSurj q
    have hlow : restrictedProjection hL omega a ⟨X.val,hab.trans X.property⟩ =
        (⟨q.val,hab.trans q.property⟩ : TorusSuperlevel hL omega a) := by
      apply Subtype.ext
      exact congrArg (fun q : TorusSuperlevel hL omega b => q.val) hXq
    rw [← hlow,hcomp,hfix X,hXq]
  have hprojCont : Continuous (coverProjection L) :=
    (SourceActualFoldTorus.torusProjection2L_continuous L).comp (coordinates 2).continuous
  have himage : coverProjection L '' {Y : E2 | a ≤ actualField 2 L omega Y} ⊆
      {z : I4Torus.SourceTorus 2 L | a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z} := by
    rintro z ⟨Y,hY,rfl⟩
    change a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega
      (I4Torus.torusProjection 2 L (coordinates 2 Y))
    rw [SourceActualFoldTorus.actualTorusField_pullback]
    exact hY
  refine ⟨R,hRcont,hRfix,?_,hcomp⟩
  intro q
  have hp := ((hpoint (liftA q)).map hprojCont.continuousOn).mono himage
  have hleft := congrArg Subtype.val (hlift q)
  change coverProjection L (liftA q).val = q.val at hleft
  rw [hleft] at hp
  exact hp

private theorem literalComponentBijective_of_hitting {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (R : TorusSuperlevel hL omega a → TorusSuperlevel hL omega b)
    (hRcont : Continuous R)
    (hfix : ∀ q : TorusSuperlevel hL omega b, R ⟨q.val,hab.trans q.property⟩ = q)
    (hpoint : ∀ q : TorusSuperlevel hL omega a,
      JoinedIn {z : I4Torus.SourceTorus 2 L |
        a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z} q.val (R q).val) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab)) := by
  let F := SourceActualFoldTorus.actualTorusField hL.ne' omega
  let r : C(TorusFiltration.superlevel_set F (-a),TorusFiltration.superlevel_set F (-b)) :=
    ⟨fun q => ⟨(R ⟨q.val,by
      simpa only [TorusFiltration.superlevel_set,Set.mem_ofPred_eq,neg_neg] using q.property⟩).val,by
      have hp := (R ⟨q.val,by
        simpa only [TorusFiltration.superlevel_set,Set.mem_ofPred_eq,neg_neg] using q.property⟩).property
      simpa only [TorusFiltration.superlevel_set,Set.mem_ofPred_eq,neg_neg] using hp⟩,
      by fun_prop⟩
  have hleft : Function.LeftInverse (TorusFiltration.superlevel_componentMap r)
      (TorusFiltration.superlevel_componentInclusion F (s := -b) (t := -a) (neg_le_neg hab)) := by
    intro q
    obtain ⟨X,rfl⟩ := ZerothHomotopy.mk_surjective q
    change ZerothHomotopy.mk (r ((TorusFiltration.superlevel_inclusion F (neg_le_neg hab)) X)) =
      ZerothHomotopy.mk X
    congr 1
    apply Subtype.ext
    have hX : b ≤ F X.val := by
      simpa only [TorusFiltration.superlevel_set,Set.mem_ofPred_eq,neg_neg] using X.property
    exact congrArg (fun q : TorusSuperlevel hL omega b => q.val) (hfix ⟨X.val,hX⟩)
  refine ⟨hleft.injective,?_⟩
  intro q
  obtain ⟨X,rfl⟩ := ZerothHomotopy.mk_surjective q
  refine ⟨ZerothHomotopy.mk (r X),?_⟩
  apply (TorusFiltration.superlevel_component_eq_iff_joinedIn F (-a) _ _).mpr
  have hX : a ≤ F X.val := by
    simpa only [TorusFiltration.superlevel_set,Set.mem_ofPred_eq,neg_neg] using X.property
  have hp := (hpoint ⟨X.val,hX⟩).symm
  have he : ((TorusFiltration.superlevel_inclusion F (neg_le_neg hab)) (r X)).val =
      (R ⟨X.val,hX⟩).val := rfl
  rw [he]
  simpa only [TorusFiltration.superlevel_set,neg_neg,F] using hp

private theorem closedBand_componentBijective_core {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hreg : ∀ X : E2, a ≤ actualField 2 L omega X →
      actualField 2 L omega X ≤ b → fderiv ℝ (actualField 2 L omega) X ≠ 0) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab)) := by
  by_cases heq : a = b
  · subst b
    exact zeroWidth_componentBijective hL omega a
  · by_cases hne : ∃ X : E2, a ≤ actualField 2 L omega X ∧ actualField 2 L omega X ≤ b
    · obtain ⟨c,A,Kp,M,K,hfield⟩ := normalizedFieldData hL omega a b hab hreg hne
      have hf := hfield
      dsimp only [NormalizedFieldFacts] at hf
      rcases hf with ⟨_hc,_hA,_hpbound,_hplip,_hpper,_hfloor,hVbound,hVlip,hVper,
        _hspeedformula,_hspeed,_hbandspeed⟩
      obtain ⟨H,hfamily⟩ := boundedFiniteHorizonFamily
        (normalizedVelocity (actualField 2 L omega) c) M K hVbound hVlip hVper
        (b-a) (sub_nonneg.mpr hab)
      obtain ⟨Rcover,hcover⟩ := heightHittingData hL omega a b hab c A Kp M K H hfield hfamily
      obtain ⟨R,hRcont,hRfix,hRpoint,_hcomp⟩ := descendedHittingData hL omega a b hab H Rcover hcover
      exact literalComponentBijective_of_hitting hL omega a b hab R hRcont hRfix hRpoint
    · apply emptyBand_componentBijective hL omega a b hab
      intro X hX
      exact hne ⟨X,hX⟩

theorem actualSource_closedSlab_componentInclusion_bijective
    {L : ℝ} (hL : 0 < L) (omega : SmoothSample 2 L) (a b : ℝ) (hab : a ≤ b)
    (hreg : ∀ X : UniversalLaw.Spec.Lifetime.E 2,
      a ≤ I4LifetimeField.actualField 2 L omega X →
      I4LifetimeField.actualField 2 L omega X ≤ b →
      fderiv ℝ (I4LifetimeField.actualField 2 L omega) X ≠ 0) :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField hL.ne' omega)
      (s := -b) (t := -a) (neg_le_neg hab)) :=
  closedBand_componentBijective_core hL omega a b hab hreg


private def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1,![(2 : ℤ),0],0⟩,⟨(1/2 : ℝ),![(0 : ℤ),1],0⟩]
private def fixtureSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)
private def fixturePoint (x y : ℝ) : E2 := (coordinates 2).symm ![x,y]
@[simp] private theorem fixturePoint_apply (x y : ℝ) (i : Fin 2) :
    fixturePoint x y i = (![x,y] : Fin 2 → ℝ) i := by
  change (coordinates 2 ((coordinates 2).symm ![x,y])) i = _
  rw [ContinuousLinearEquiv.apply_symm_apply]

private theorem finiteSourceField (p : I4SourceFiniteTrig.TrigPoly) (x : Fin 2 → ℝ) :
    smoothSourceField 2 2
      (I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 p)
        (I4SourceSmoothConditional.zeroSample 2 2)) x = I4SourceFiniteTrig.eval 2 p x := by
  classical
  have hs : HasSum (fun m => I4Source.modeCoefficient 2 2 m x *
      I4SourceFiniteTrig.toSource 2 p m)
      (I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x)
        (I4SourceFiniteTrig.toSource 2 p)) := by
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    simp only [Finsupp.notMem_support_iff.mp hm,mul_zero]
  have hf : smoothSourceField 2 2
      (I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 p)
        (I4SourceSmoothConditional.zeroSample 2 2)) x =
      I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x)
        (I4SourceFiniteTrig.toSource 2 p) := by
    simpa [smoothSourceField,I4Source.sourceField,I4Foundation.scalarSeries,sampleInclusion,
      I4SourceFinitePinKernel.finiteShiftSample_val,I4SourceSmoothConditional.zeroSample] using hs.tsum_eq
  exact hf.trans (I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0) p x)

private theorem fixture_coordinateField (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 fixtureSample x =
      Real.cos (2*Real.pi*x 0)+(1/2 : ℝ)*Real.cos (Real.pi*x 1) := by
  rw [fixtureSample,finiteSourceField]
  have h0 : I4Source.phase 2 2 (![(2 : ℤ),0]) x = 2*Real.pi*x 0 := by
    unfold I4Source.phase I4Weights.sourceC
    rw [Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Int.cast_ofNat,Int.cast_zero]
    ring
  have h1 : I4Source.phase 2 2 (![(0 : ℤ),1]) x = Real.pi*x 1 := by
    unfold I4Source.phase I4Weights.sourceC
    rw [Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Int.cast_zero,Int.cast_one]
    ring
  simp [fixturePolynomial,I4SourceFiniteTrig.eval,I4SourceFiniteTrig.termEval,h0,h1]

private theorem fixture_actualField (X : E2) :
    actualField 2 2 fixtureSample X =
      Real.cos (2*Real.pi*X 0)+(1/2 : ℝ)*Real.cos (Real.pi*X 1) :=
  fixture_coordinateField (coordinates 2 X)

private def fixtureCoord (i : Fin 2) : E2 →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i).comp (coordinates 2).toContinuousLinearMap
private def fixtureDerivative (X : E2) : E2 →L[ℝ] ℝ :=
  (-(2*Real.pi)*Real.sin (2*Real.pi*X 0)) • fixtureCoord 0 +
    (-((1/2 : ℝ)*Real.pi)*Real.sin (Real.pi*X 1)) • fixtureCoord 1
private theorem fixture_hasFDerivAt (X : E2) :
    HasFDerivAt (actualField 2 2 fixtureSample) (fixtureDerivative X) X := by
  have h0 : HasFDerivAt (fun Y : E2 => (2*Real.pi)*Y 0)
      ((2*Real.pi) • fixtureCoord 0) X := (fixtureCoord 0).hasFDerivAt.const_mul (2*Real.pi)
  have h1 : HasFDerivAt (fun Y : E2 => Real.pi*Y 1)
      (Real.pi • fixtureCoord 1) X := (fixtureCoord 1).hasFDerivAt.const_mul Real.pi
  have hh := h0.cos.add (h1.cos.const_mul (1/2 : ℝ))
  have he : actualField 2 2 fixtureSample = fun Y : E2 =>
      Real.cos (2*Real.pi*Y 0)+(1/2 : ℝ)*Real.cos (Real.pi*Y 1) := funext fixture_actualField
  rw [he]
  convert hh using 1; ext v; simp [fixtureDerivative,fixtureCoord]; ring

private theorem fixture_criticalHeights (X : E2)
    (hc : IsCriticalPoint 2 (actualField 2 2 fixtureSample) X) :
    actualField 2 2 fixtureSample X ∈ ({3/2,1/2,-1/2,-3/2} : Set ℝ) := by
  change fderiv ℝ (actualField 2 2 fixtureSample) X = 0 at hc
  rw [(fixture_hasFDerivAt X).fderiv] at hc
  have h0 := congrArg (fun D : E2 →L[ℝ] ℝ => D (fixturePoint 1 0)) hc
  have h1 := congrArg (fun D : E2 →L[ℝ] ℝ => D (fixturePoint 0 1)) hc
  simp [fixtureDerivative,fixtureCoord] at h0 h1
  have hs0 : Real.sin (2*Real.pi*X 0) = 0 := by
    exact h0
  have hs1 : Real.sin (Real.pi*X 1) = 0 := by
    exact h1
  rcases Real.sin_eq_zero_iff_cos_eq.mp hs0 with hx|hx <;>
  rcases Real.sin_eq_zero_iff_cos_eq.mp hs1 with hy|hy <;>
  rw [fixture_actualField,hx,hy] <;> norm_num

private theorem fixture_fieldBounds (X : E2) :
    (-3/2 : ℝ) ≤ actualField 2 2 fixtureSample X ∧ actualField 2 2 fixtureSample X ≤ 3/2 := by
  rw [fixture_actualField]
  constructor <;> nlinarith [Real.neg_one_le_cos (2*Real.pi*X 0),Real.cos_le_one (2*Real.pi*X 0),
    Real.neg_one_le_cos (Real.pi*X 1),Real.cos_le_one (Real.pi*X 1)]

private theorem fixture_closedRegular_noCritical (X : E2)
    (ha : (0 : ℝ) ≤ actualField 2 2 fixtureSample X)
    (hb : actualField 2 2 fixtureSample X ≤ 1/4) :
    fderiv ℝ (actualField 2 2 fixtureSample) X ≠ 0 := by
  intro hc
  have hh := fixture_criticalHeights X hc
  simp only [Set.mem_insert_iff,Set.mem_singleton_iff] at hh
  rcases hh with hh|hh|hh|hh <;> linarith

private theorem fixture_band_nonempty :
    ∃ X : E2, (0 : ℝ) ≤ actualField 2 2 fixtureSample X ∧ actualField 2 2 fixtureSample X ≤ 1/4 := by
  refine ⟨fixturePoint (1/4) (1/2),?_⟩
  have h0 : 2*Real.pi*(1/4 : ℝ) = Real.pi/2 := by ring
  have h1 : Real.pi*(1/2 : ℝ) = Real.pi/2 := by ring
  norm_num [fixture_actualField,h0,h1]

private theorem fixture_regularObjects :
    ∃ c A : ℝ, ∃ Kp M K : ℝ≥0, ∃ H : ℝ → E2 → E2,
      NormalizedFieldFacts fixtureSample 0 (1/4) c A Kp M K ∧
      FiniteHorizonFacts 2 (normalizedVelocity (actualField 2 2 fixtureSample) c) (1/4) H ∧
      Function.Bijective (TorusFiltration.superlevel_componentInclusion
        (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
        (s := -(1/4 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (by norm_num : (0 : ℝ) ≤ 1/4))) := by
  obtain ⟨c,A,Kp,M,K,hfield⟩ := normalizedFieldData (by norm_num) fixtureSample 0 (1/4)
    (by norm_num) fixture_closedRegular_noCritical fixture_band_nonempty
  have hf := hfield
  dsimp only [NormalizedFieldFacts] at hf
  rcases hf with ⟨_hc,_hA,_hpb,_hpl,_hpp,_hfloor,hVb,hVl,hVp,_hform,_hsp,_hunit⟩
  obtain ⟨H,hfamily⟩ := boundedFiniteHorizonFamily
    (normalizedVelocity (actualField 2 2 fixtureSample) c) M K hVb hVl hVp (1/4) (by norm_num)
  exact ⟨c,A,Kp,M,K,H,hfield,hfamily,
    closedBand_componentBijective_core (by norm_num) fixtureSample 0 (1/4) (by norm_num)
      fixture_closedRegular_noCritical⟩

private theorem fixture_closedRegular :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
      (s := -(1/4 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (by norm_num : (0 : ℝ) ≤ 1/4))) := by
  obtain ⟨_c,_A,_Kp,_M,_K,_H,_hfield,_hfamily,hbij⟩ := fixture_regularObjects
  exact hbij

private theorem fixture_zeroWidth :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
      (s := -(0 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (le_refl (0 : ℝ)))) :=
  zeroWidth_componentBijective (by norm_num) fixtureSample 0

private theorem fixture_emptyBand :
    Function.Bijective (TorusFiltration.superlevel_componentInclusion
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample)
      (s := -(-2 : ℝ)) (t := -(-3 : ℝ)) (neg_le_neg (by norm_num : (-3 : ℝ) ≤ -2))) := by
  apply emptyBand_componentBijective (by norm_num) fixtureSample (-3) (-2) (by norm_num)
  intro X hX
  have hlow := (fixture_fieldBounds X).1
  linarith [hX.2]

private theorem fixture_torusBounds (q : I4Torus.SourceTorus 2 2) :
    (-3/2 : ℝ) ≤ SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample q ∧
      SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample q ≤ 3/2 := by
  obtain ⟨x,hx⟩ := SourceActualFoldTorus.torusProjection2L_surjective 2 q
  have hh := fixture_fieldBounds ((coordinates 2).symm x)
  simpa only [actualField,ContinuousLinearEquiv.apply_symm_apply,
    ← SourceActualFoldTorus.actualTorusField_pullback (by norm_num : (2 : ℝ) ≠ 0) fixtureSample x,hx] using hh

private theorem fixture_emptyBand_whole_nonempty :
    TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (2 : ℝ) = Set.univ ∧
    TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (3 : ℝ) = Set.univ ∧
    (TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (2 : ℝ)).Nonempty := by
  have h2 : TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (2 : ℝ) = Set.univ := by
    apply Set.eq_univ_of_forall
    intro q
    change (-2 : ℝ) ≤ SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample q
    linarith [(fixture_torusBounds q).1]
  have h3 : TorusFiltration.superlevel_set
      (SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample) (3 : ℝ) = Set.univ := by
    apply Set.eq_univ_of_forall
    intro q
    change (-3 : ℝ) ≤ SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample q
    linarith [(fixture_torusBounds q).1]
  refine ⟨h2,h3,0,?_⟩
  rw [h2]
  trivial

end I4SourceActualTorusRegularSlab
