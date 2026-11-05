import GeometrySupport

noncomputable section
open I4SourcePinPreservingQuartic
set_option autoImplicit false

namespace I4QuarticCaptureAlgebra

/-- Vanishing raw coefficients and q=0 give no upper-strip inward drift,
even at every radius satisfying REG. -/
theorem zero_coefficients_transverse_failure (r : ℝ) :
    pinPreservingQuartic r 0 (fun _ => 0) ![0,captureWidth r (fun _ => 0)] 1 = 0 ∧
    ¬ pinPreservingQuartic r 0 (fun _ => 0) ![0,captureWidth r (fun _ => 0)] 1 ≤ -1 := by
  norm_num [pinPreservingQuartic]

/-- This positive-radius witness satisfies REG exactly; the omitted scalar
curvature threshold still prevents the strip conclusion. -/
theorem scalar_threshold_essential_witness :
    let r : ℝ := 1 / (1024 * quarticK0)
    0 < r ∧ r ≤ 1 ∧ regular r (fun _ => 0) ∧
      pinPreservingQuartic r 0 (fun _ => 0) ![0,captureWidth r (fun _ => 0)] 1 = 0 ∧
      ¬ pinPreservingQuartic r 0 (fun _ => 0) ![0,captureWidth r (fun _ => 0)] 1 ≤ -1 := by
  dsimp
  refine ⟨by norm_num [quarticK0], by norm_num [quarticK0], ?_,
    (zero_coefficients_transverse_failure _).1, (zero_coefficients_transverse_failure _).2⟩
  norm_num [regular,rawRadius]

def regularityCounterexampleU : Fin 8 → ℝ := ![0,0,0,64,0,0,0,0]

theorem regularity_counterexample_radius : rawRadius regularityCounterexampleU = 65 := by
  norm_num [rawRadius,regularityCounterexampleU,Fin.sum_univ_succ]

/-- Without REG the central X-component has the wrong sign at an actual
central-strip point, independently of the scalar q parameter. -/
theorem regularity_essential_central_witness (q : ℝ) :
    ¬ regular 1 regularityCounterexampleU ∧
    |(-(1 : ℝ)/4)| ≤ 1/2-captureSigma 1 regularityCounterexampleU ∧
    |(0 : ℝ)| ≤ captureWidth 1 regularityCounterexampleU ∧
    pinPreservingQuartic 1 q regularityCounterexampleU ![-1/4,0] 0 = 5/16 ∧
    0 < pinPreservingQuartic 1 q regularityCounterexampleU ![-1/4,0] 0 := by
  have hσ := captureSigma_le 1 regularityCounterexampleU (by norm_num)
  have hW := captureWidth_pos 1 regularityCounterexampleU (by norm_num)
  have hP : pinPreservingQuartic 1 q regularityCounterexampleU ![-1/4,0] 0 = 5/16 := by
    norm_num [pinPreservingQuartic,regularityCounterexampleU]
  refine ⟨?_,?_,?_,hP,?_⟩
  · norm_num [regular,regularity_counterexample_radius,quarticK0]
  · norm_num only
    linarith
  · simpa using hW.le
  · rw [hP]
    norm_num

end I4QuarticCaptureAlgebra
