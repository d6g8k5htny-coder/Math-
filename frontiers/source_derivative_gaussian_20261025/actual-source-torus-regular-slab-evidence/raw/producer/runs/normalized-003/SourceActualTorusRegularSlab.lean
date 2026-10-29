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
          abs_of_nonneg (add_nonneg (norm_nonneg _) (norm_nonneg _))] <;> ring
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

end I4SourceActualTorusRegularSlab
