import SourceQuarticCaptureAlgebra

/-! New-only controls for the actual transfer additions. The unchanged Q2/Q3
counterexamples remain covered by their existing scratch receipts and are not rerun. -/

noncomputable section
open I4SmoothCarrier I4SourcePinCurvatureBounds I4SourceConditionalMajorant
open I4SourcePinPreservingQuartic I4SourceSmoothPalm I4SourceSmoothConditional
open I4QuarticCaptureAlgebra MeasureTheory
open scoped Topology
set_option autoImplicit false

namespace I4QuarticTransferControls

/-- A quarter-width value error retains the exact 11/4 drift buffer. -/
theorem quarter_error_drift_transfer (S P V : ℝ) (hS : 0 < S)
    (hP : P ≤ -3*S) (hE : |V-P| ≤ S/4) :
    V ≤ -(11/4)*S ∧ -(11/4)*S < 0 := by
  have he := (le_abs_self (V-P)).trans hE
  constructor <;> nlinarith

/-- The allowed positive error witnesses failure of the stronger unchanged bound. -/
theorem quarter_error_prevents_unchanged_drift (S : ℝ) (hS : 0 < S) :
    |(-3*S+S/4)-(-3*S)| = S/4 ∧
      -3*S+S/4 = -(11/4)*S ∧ ¬ (-3*S+S/4 ≤ -3*S) := by
  have hquarter : 0 ≤ S/4 := by positivity
  refine ⟨?_,by ring,?_⟩
  · rw [show (-3*S+S/4)-(-3*S) = S/4 by ring, abs_of_nonneg hquarter]
  · nlinarith

-- MAX-C1 controls the value component without replacing max by a sum norm.
example (v w : SourcePlane) (A : SourcePlane →L[ℝ] SourcePlane) (η : ℝ)
    (h : max ‖v-w‖ ‖A‖ ≤ η) (i : Fin 2) : |v i-w i| ≤ η :=
  euclidean_component_error_le v w η ((le_max_left _ _).trans h) i

-- Concrete Euclidean (3,4) vector: projection uses the actual L2 norm.
example (i : Fin 2) :
    |(WithLp.toLp 2 (![3,4] : Fin 2 → ℝ) : SourcePlane) i| ≤ (5 : ℝ) := by
  let v : SourcePlane := WithLp.toLp 2 ![3,4]
  have hnorm : ‖v‖ ≤ 5 := by
    have hs := euclidean_two_norm_sq v
    norm_num [v] at hs
    nlinarith [norm_nonneg v]
  have h := euclidean_component_error_le v 0 5 (by simpa using hnorm) i
  simpa [v] using h

-- The adaptive strip point is in the actual comparison ball, including its boundary.
example (r : ℝ) (U : Fin 8 → ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (X : ℝ) (hX : |X| ≤ 1/2) :
    ‖(WithLp.toLp 2 ![X,captureWidth r U] : SourcePlane)‖ ≤ 2 := by
  apply capture_strip_in_ball_two r U hr1 X _ hX
  rw [abs_of_nonneg]
  · exact le_rfl
  · exact (captureWidth_pos r U hr).le

-- These statement checks preserve the physical component and inward orientations.
example {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r) (hr1 : r ≤ 1)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar)
    (hq : sourceQ L ω ≤ -quarticKcap*r*sourceGammaRadius L ω^5) :
    ∀ X : ℝ, |X| ≤ 1/2 →
      sourceScaledGradientRaw L r ω ![X,captureWidth r (sourceRawU L ω)] 1 < 0 ∧
      0 < sourceScaledGradientRaw L r ω ![X,-captureWidth r (sourceRawU L ω)] 1 :=
  source_actual_strip_gates hL r hr hr1 ω hp hcut hq

-- The actual central theorem needs no transverse-curvature threshold.
example {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : 0 < r) (hr1 : r ≤ 1)
    (ω : SmoothSample 2 L) (hp : sourcePhysicalPins L r ω)
    (hcut : r*sourceGammaRadius L ω^5 ≤ quarticEpsilonStar) :
    ∀ X Y : ℝ, |X| ≤ 1/2-captureSigma r (sourceRawU L ω) →
      |Y| ≤ captureWidth r (sourceRawU L ω) →
      sourceScaledGradientRaw L r ω ![X,Y] 0 ≤
        -(11/4)*rawRadius (sourceRawU L ω)*captureWidth r (sourceRawU L ω) ∧
      -(11/4)*rawRadius (sourceRawU L ω)*captureWidth r (sourceRawU L ω) < 0 :=
  source_actual_central_gate hL r hr hr1 ω hp hcut

-- The new weighted source application uses the actual b=3 carrier law.
example : ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
    ∀ᵐ ω ∂sourceSmoothWeightedLaw (by norm_num : (1 : ℝ) ≠ 0) r 3,
      r*sourceGammaRadius 1 ω^5 ≤ quarticEpsilonStar →
        sourceCentralGate 1 r ω ∧
        (sourceQ 1 ω ≤ -quarticKcap*r*sourceGammaRadius 1 ω^5 → sourceStripGates 1 r ω) :=
  source_actual_weighted_gates_estimates (by norm_num) 3

end I4QuarticTransferControls
