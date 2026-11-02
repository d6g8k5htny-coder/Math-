import SourcePinCurvatureBounds

noncomputable section
open I4SmoothCarrier I4SourceConditionalMajorant I4SourceConfluentPins
open I4SourcePinCurvatureBounds I4ModeCurveChains
set_option autoImplicit false

namespace I4ActualQuarticTransfer

theorem smooth_iteratedDeriv (g : ℝ → ℝ) (hg : ContDiff ℝ (⊤ : ℕ∞) g) (k : ℕ) :
    ContDiff ℝ (⊤ : ℕ∞) (iteratedDeriv k g) := by
  induction k with
  | zero => simpa using hg
  | succ k hk =>
    rw [iteratedDeriv_succ]
    have hm : ContDiff ℝ ((⊤ : ℕ∞)+1) (iteratedDeriv k g) := by simpa using hk
    exact hm.deriv'

theorem iteratedDeriv_iteratedDeriv (g : ℝ → ℝ) (n k : ℕ) :
    iteratedDeriv n (iteratedDeriv k g) = iteratedDeriv (n+k) g := by
  simp only [iteratedDeriv_eq_iterate, Function.iterate_add_apply]

theorem sourceF_smooth {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (sourceF L ω) :=
  (smoothSourceField_smooth 2 hL ω).comp axisMap.contDiff

theorem sourceH_smooth {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (sourceH L ω) :=
  axis_transverse_smooth _ (smoothSourceField_smooth 2 hL ω)

theorem sourceF_iteratedDeriv_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (t : ℝ) :
    |iteratedDeriv k (sourceF L ω) t| ≤ sourceDerivativeMajorant L k ω := by
  unfold sourceF
  rw [axis_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) k t]
  exact source_axis_derivative_abs_le hL ω k (fun _ => directionX)
    (fun _ => directionX_norm_le_one) t

theorem sourceH_iteratedDeriv_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (t : ℝ) :
    |iteratedDeriv k (sourceH L ω) t| ≤ sourceDerivativeMajorant L (k+1) ω := by
  unfold sourceH
  rw [axis_transverse_iteratedDeriv _ (smoothSourceField_smooth 2 hL ω) k t]
  apply source_axis_derivative_abs_le hL ω (k+1) _ ?_ t
  intro i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simpa only [Fin.snoc_last] using directionY_norm_le_one
  · simpa only [Fin.snoc_castSucc] using directionX_norm_le_one

end I4ActualQuarticTransfer
