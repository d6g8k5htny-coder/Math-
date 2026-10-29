import SourceAdaptiveFoldChart

noncomputable section
open I4SourceAdaptiveFoldChart I4ActualFoldChartJets
open AdaptiveFoldTransverseRidge I4SourceCompactTargetMoments
open I4SourceConfluentPins I4SourceRawPinConditioning I4SmoothCarrier
open MeasureTheory
open scoped Matrix Interval

namespace ActualFoldChartControls

/-- Physical test field with k=r=1 and nonzero birth b=3. -/
def physicalPolynomial (x : Fin 2 → ℝ) : ℝ :=
  6 * (x 0 ^ 3 / 3 - x 0 / 4) + 5/2

/-- The normalized chart of that exact physical test field. -/
def polynomial (a c : ℝ) (p : ℝ × ℝ) : ℝ :=
  a * (p.1^3 / 3 - p.1/4) + c

theorem polynomial_smooth (a c : ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (polynomial a c) := by
  unfold polynomial
  fun_prop

theorem physicalPolynomial_chart :
    V physicalPolynomial 1 1 = polynomial 1 (5/12) := by
  ext p
  simp [V, physicalPolynomial, polynomial]
  ring

theorem physicalPolynomial_values :
    physicalPolynomial ![-1/2,0] = 3 ∧ physicalPolynomial ![1/2,0] = 2 := by
  norm_num [physicalPolynomial]

theorem polynomial_curve_deriv (a c t : ℝ) :
    deriv (fun u => polynomial a c (u,0)) t = a * (t^2-1/4) := by
  have h := (((((hasDerivAt_id t).pow 3).div_const 3).sub
    ((hasDerivAt_id t).div_const 4)).const_mul a).add_const c
  convert h.deriv using 1 <;> dsimp [polynomial] <;> ring

theorem polynomial_axial (a c t : ℝ) :
    fderiv ℝ (fderiv ℝ (Vx (polynomial a c))) (t,0) ex ex = 2*a := by
  rw [← curve_iteratedDeriv_three _ (polynomial_smooth a c) t]
  have h1 : deriv (fun u => polynomial a c (u,0)) = fun u => a*(u^2-1/4) :=
    funext (polynomial_curve_deriv a c)
  have h2 : deriv (fun u : ℝ => a*(u^2-1/4)) = fun u => 2*a*u := by
    ext u
    have h := (((hasDerivAt_id u).pow 2).sub_const (1/4 : ℝ)).const_mul a
    convert h.deriv using 1 <;> dsimp <;> ring
  have h3 : deriv (fun u : ℝ => 2*a*u) = fun _ => 2*a := by
    ext u
    simpa using ((hasDerivAt_id u).const_mul (2*a)).deriv
  simp only [iteratedDeriv_succ, iteratedDeriv_zero]
  rw [h1,h2,h3]

theorem polynomial_x_pin (a c : ℝ) :
    Vx (polynomial a c) (-1/2,0) = 0 ∧
    Vx (polynomial a c) (1/2,0) = 0 := by
  rw [← curve_deriv _ (polynomial_smooth a c) (-1/2),
    ← curve_deriv _ (polynomial_smooth a c) (1/2)]
  norm_num [polynomial_curve_deriv]

theorem polynomial_y_pin (a c : ℝ) :
    Vy (polynomial a c) (-1/2,0) = 0 ∧
    Vy (polynomial a c) (1/2,0) = 0 := by
  have he : ∀ p : ℝ × ℝ, Vy (polynomial a c) p = 0 := by
    intro p
    have hx : HasFDerivAt (fun q : ℝ × ℝ => q.1)
        (ContinuousLinearMap.fst ℝ ℝ ℝ) p := hasFDerivAt_fst
    have h := (((((hx.pow 3).div_const 3).sub (hx.div_const 4)).const_mul a).add_const c)
    change HasFDerivAt (polynomial a c) _ p at h
    rw [Vy, partialY, h.fderiv]
    simp [ey]
  exact ⟨he _,he _⟩

/-- Positive control: scale2 at genuine k=1, with physical values3 and2. -/
theorem non_specialized_positive_control :
    NormalizedFoldData (V physicalPolynomial 1 1) ∧
      (∀ u : ℝ, fderiv ℝ (fderiv ℝ (Vx (V physicalPolynomial 1 1)))
        (u,0) ex ex = 2) := by
  rw [physicalPolynomial_chart]
  obtain ⟨hxm,hxs⟩ := polynomial_x_pin 1 (5/12)
  obtain ⟨hym,hys⟩ := polynomial_y_pin 1 (5/12)
  have hg : polynomial 1 (5/12) (-1/2,0) - polynomial 1 (5/12) (1/2,0) = 1/6 := by
    norm_num [polynomial]
  constructor
  · exact ⟨(polynomial_smooth 1 (5/12)).of_le (by norm_num), hxm,hxs,hym,hys,hg,
      normalized_axial_peano _ (polynomial_smooth 1 (5/12)) hxm hxs hg⟩
  · intro u
    simpa using polynomial_axial 1 (5/12) u

/-- Actual target identity retains row5=12 at genuine k=1. -/
theorem actual_target_control {L r : ℝ} (hL : L ≠ 0) (hr : r ≠ 0) :
    sourceGapLaw hL r 3 1 = rawPinKernel hL r ![3,3-r^3,0,0,0,0] ∧
      sourceGapPins r 3 1 5 = 12 := by
  constructor
  · simpa using sourceGapLaw_eq_rawPinKernel hL r 3 1 hr
  · norm_num [sourceGapPins]

/-- Closed endpoint control: hL alone yields the common radius, before r. -/
theorem derived_interval_control {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      (∀ η : SmoothSample 2 L, NormalizedFoldData (actualFoldPotential r 1
        (rawPosteriorSample hL r ![3,3-r^3,0,0,0,0] η))) ∧
      (∀ᵐ sample ∂sourceGapLaw hL r 3 1,
        NormalizedFoldData (actualFoldPotential r 1 sample)) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_and_posterior_normalized_fold_data hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  simpa using h r hr hrδ 3 1 (by norm_num)

end ActualFoldChartControls
