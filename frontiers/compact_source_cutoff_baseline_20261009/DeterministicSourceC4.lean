import SourceTorusC4

noncomputable section
open I4Foundation I4Weights I4Source I4C4 I4Torus I4TorusC4
open scoped Manifold ContDiff Topology
namespace I4DeterministicC4
attribute [local instance] actualChartedSpace

theorem sourceField_contDiff_of_majorant (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (coeff : SourceMode d → ℝ) (hcoeff : Summable (fun m => modeMajorant d L m * |coeff m|)) :
    ContDiff ℝ 4 (sourceField d L coeff) := by
  have hc (m : SourceMode d) : ContDiff ℝ 4 (modeCoefficient d L m) := by
    cases m with
    | none =>
      change ContDiff ℝ 4 (fun _ : Fin d → ℝ => Real.sqrt (1 / sourceZ d L))
      fun_prop
    | some p =>
      rcases p with ⟨k, b⟩
      change ContDiff ℝ 4 (fun x : Fin d → ℝ =>
        Real.sqrt (2 * sourceWeight d L k / sourceZ d L) *
          (if b then Real.sin (phase d L k x) else Real.cos (phase d L k x)))
      cases b <;> simp [phase] <;> fun_prop
  change ContDiff ℝ 4 (fun x => ∑' m, modeCoefficient d L m x * coeff m)
  apply contDiff_tsum (v := fun _ m => modeMajorant d L m * |coeff m|)
  · intro m
    exact (hc m).mul contDiff_const
  · intro j hj
    exact hcoeff
  · intro j m x hj
    have hj' : j ≤ 4 := by exact_mod_cast hj
    have hcj : ContDiff ℝ j (modeCoefficient d L m) :=
      (hc m).of_le (by exact_mod_cast hj')
    have heq : (fun y => modeCoefficient d L m y * coeff m) = coeff m • modeCoefficient d L m := by
      funext y
      simp [smul_eq_mul, mul_comm]
    rw [heq, iteratedFDeriv_const_smul_apply hcj.contDiffAt, norm_smul, Real.norm_eq_abs]
    simpa only [mul_comm] using mul_le_mul_of_nonneg_left
      (modeCoefficient_iteratedFDeriv_bound d hL m j hj' x) (abs_nonneg (coeff m))

theorem torusSourceField_contMDiff_of_majorant (d : ℕ) (L : ℝ) [Fact (0 < L)]
    (coeff : SourceMode d → ℝ) (hcoeff : Summable (fun m => modeMajorant d L m * |coeff m|)) :
    ContMDiff 𝓘(ℝ, Fin d → ℝ) 𝓘(ℝ) 4 (torusSourceField d L coeff) := by
  let _ := torus_isManifold d L
  have hs := sourceField_contDiff_of_majorant d (Fact.out : 0 < L).ne' coeff hcoeff
  intro q
  rw [contMDiffAt_iff_source]
  have heq : torusSourceField d L coeff ∘ (extChartAt 𝓘(ℝ, Fin d → ℝ) q).symm =
      sourceField d L coeff := by
    funext x
    change torusSourceField d L coeff ((quotientChart d L (chartCenter d L q)).symm x) = _
    rw [quotientChart_symm]
    exact torusSourceField_pullback d L coeff x
  rw [heq, contMDiffWithinAt_iff_contDiffWithinAt]
  exact hs.contDiffAt.contDiffWithinAt

end I4DeterministicC4
