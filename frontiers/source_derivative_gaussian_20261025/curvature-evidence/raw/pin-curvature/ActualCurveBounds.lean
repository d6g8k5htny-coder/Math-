import SourceConditionalMajorant
import Mathlib.Analysis.Calculus.MeanValue

noncomputable section

open I4SmoothCarrier I4SourceConfluentPins I4SourceConditionalMajorant I4ModeCurveChains
open MeasureTheory Set
open scoped BigOperators

namespace I4SourcePinCurvatureBounds

def sourceF (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  smoothSourceField 2 L ω ![t,0]

def sourceH (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  fderiv ℝ (smoothSourceField 2 L ω) ![t,0] directionY

def sourceQCurve (L : ℝ) (ω : SmoothSample 2 L) (t : ℝ) : ℝ :=
  iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) ![t,0] ![directionY,directionY]

theorem directionX_norm_le_one : ‖directionX‖ ≤ (1 : ℝ) := by
  apply (pi_norm_le_iff_of_nonneg zero_le_one).mpr
  intro i
  fin_cases i <;> norm_num [directionX]

theorem directionY_norm_le_one : ‖directionY‖ ≤ (1 : ℝ) := by
  apply (pi_norm_le_iff_of_nonneg zero_le_one).mpr
  intro i
  fin_cases i <;> norm_num [directionY]

theorem axis_point_sub_norm_le (s t : ℝ) :
    ‖(![s,0] : Fin 2 → ℝ) - ![t,0]‖ ≤ |s-t| := by
  apply (pi_norm_le_iff_of_nonneg (abs_nonneg _)).mpr
  intro i
  fin_cases i <;> simp [Real.norm_eq_abs]

/-- A bound on the next operator derivative gives a Lipschitz bound for
every fixed unit-bounded derivative tuple along the actual x axis. -/
theorem axis_derivative_lipschitz
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (k : ℕ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ i, ‖u i‖ ≤ 1)
    (C : ℝ) (hbound : ∀ x, ‖iteratedFDeriv ℝ (k+1) f x‖ ≤ C)
    (s t : ℝ) :
    |iteratedFDeriv ℝ k f ![s,0] u - iteratedFDeriv ℝ k f ![t,0] u| ≤ C * |s-t| := by
  have hfk : ContDiff ℝ (k+1 : ℕ) f :=
    hf.of_le (by exact_mod_cast (show (k+1 : ℕ∞) ≤ ⊤ from le_top))
  have hdiff : Differentiable ℝ (iteratedFDeriv ℝ k f) :=
    hfk.differentiable_iteratedFDeriv (by exact_mod_cast Nat.lt_succ_self k)
  have hC : 0 ≤ C := (norm_nonneg _).trans (hbound 0)
  have hD : ‖iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]‖ ≤
      C * ‖(![s,0] : Fin 2 → ℝ)-![t,0]‖ := by
    apply Convex.norm_image_sub_le_of_norm_fderiv_le
      (fun x _ => hdiff x) (fun x _ => ?_) convex_univ (mem_univ _) (mem_univ _)
    rw [norm_fderiv_iteratedFDeriv]
    exact hbound x
  have hprod : ∏ i, ‖u i‖ ≤ (1 : ℝ) :=
    Finset.prod_le_one₀ (fun _ _ => norm_nonneg _) (fun i _ => hu i)
  calc
    _ = ‖(iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]) u‖ := by
      rfl
    _ ≤ ‖iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]‖ * ∏ i, ‖u i‖ :=
      ContinuousMultilinearMap.le_opNorm _ _
    _ ≤ ‖iteratedFDeriv ℝ k f ![s,0] - iteratedFDeriv ℝ k f ![t,0]‖ :=
      mul_le_of_le_one_right (norm_nonneg _) hprod
    _ ≤ C * |s-t| := hD.trans (mul_le_mul_of_nonneg_left (axis_point_sub_norm_le s t) hC)

/-- Literal actual derivative values inherit the globally proved Fourier majorant. -/
theorem source_axis_derivative_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ i, ‖u i‖ ≤ 1) (t : ℝ) :
    |iteratedFDeriv ℝ k (smoothSourceField 2 L ω) ![t,0] u| ≤
      sourceDerivativeMajorant L k ω := by
  have hprod : ∏ i, ‖u i‖ ≤ (1 : ℝ) :=
    Finset.prod_le_one₀ (fun _ _ => norm_nonneg _) (fun i _ => hu i)
  calc
    _ ≤ ‖iteratedFDeriv ℝ k (smoothSourceField 2 L ω) ![t,0]‖ * ∏ i, ‖u i‖ :=
      ContinuousMultilinearMap.le_opNorm _ _
    _ ≤ ‖iteratedFDeriv ℝ k (smoothSourceField 2 L ω) ![t,0]‖ :=
      mul_le_of_le_one_right (norm_nonneg _) hprod
    _ ≤ _ := smoothSourceField_global_derivative_bound hL k ω ![t,0]

theorem sourceF_third_continuous {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    Continuous (iteratedDeriv 3 (sourceF L ω)) := by
  have hF : ContDiff ℝ (⊤ : ℕ∞) (sourceF L ω) :=
    (smoothSourceField_smooth 2 hL ω).comp axisMap.contDiff
  exact hF.continuous_iteratedDeriv 3 (by simp)

theorem sourceH_second_continuous {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    Continuous (iteratedDeriv 2 (sourceH L ω)) := by
  have hH : ContDiff ℝ (⊤ : ℕ∞) (sourceH L ω) :=
    axis_transverse_smooth _ (smoothSourceField_smooth 2 hL ω)
  exact hH.continuous_iteratedDeriv 2 (by simp)

theorem sourceF_third_lipschitz {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (s t : ℝ) :
    |iteratedDeriv 3 (sourceF L ω) s - iteratedDeriv 3 (sourceF L ω) t| ≤
      sourceDerivativeMajorant L 4 ω * |s-t| := by
  unfold sourceF
  rw [axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 s,
    axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 t]
  exact axis_derivative_lipschitz _ (smoothSourceField_smooth 2 hL ω) 3
    (fun _ => directionX) (fun _ => directionX_norm_le_one) _
    (smoothSourceField_global_derivative_bound hL 4 ω) s t

theorem sourceH_second_lipschitz {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (s t : ℝ) :
    |iteratedDeriv 2 (sourceH L ω) s - iteratedDeriv 2 (sourceH L ω) t| ≤
      sourceDerivativeMajorant L 4 ω * |s-t| := by
  unfold sourceH
  rw [axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 s,
    axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 t]
  apply axis_derivative_lipschitz _ (smoothSourceField_smooth 2 hL ω) 3 _ ?_ _
    (smoothSourceField_global_derivative_bound hL 4 ω) s t
  intro i
  fin_cases i
  · exact directionX_norm_le_one
  · change ‖directionX‖ ≤ (1 : ℝ)
    exact directionX_norm_le_one
  · change ‖directionY‖ ≤ (1 : ℝ)
    exact directionY_norm_le_one

theorem sourceQCurve_lipschitz {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (s t : ℝ) :
    |sourceQCurve L ω s - sourceQCurve L ω t| ≤
      sourceDerivativeMajorant L 3 ω * |s-t| := by
  apply axis_derivative_lipschitz _ (smoothSourceField_smooth 2 hL ω) 2 _ ?_ _
    (smoothSourceField_global_derivative_bound hL 3 ω) s t
  intro i
  fin_cases i <;> exact directionY_norm_le_one

theorem sourceF_third_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    |iteratedDeriv 3 (sourceF L ω) t| ≤ sourceDerivativeMajorant L 3 ω := by
  unfold sourceF
  rw [axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 3 t]
  exact source_axis_derivative_abs_le hL ω 3 (fun _ => directionX)
    (fun _ => directionX_norm_le_one) t

theorem sourceH_second_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    |iteratedDeriv 2 (sourceH L ω) t| ≤ sourceDerivativeMajorant L 3 ω := by
  unfold sourceH
  rw [axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) 2 t]
  apply source_axis_derivative_abs_le hL ω 3 _ ?_ t
  intro i
  fin_cases i
  · exact directionX_norm_le_one
  · change ‖directionX‖ ≤ (1 : ℝ)
    exact directionX_norm_le_one
  · change ‖directionY‖ ≤ (1 : ℝ)
    exact directionY_norm_le_one

theorem sourceQCurve_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (t : ℝ) :
    |sourceQCurve L ω t| ≤ sourceDerivativeMajorant L 2 ω := by
  apply source_axis_derivative_abs_le hL ω 2 _ ?_ t
  intro i
  fin_cases i <;> exact directionY_norm_le_one

end I4SourcePinCurvatureBounds
