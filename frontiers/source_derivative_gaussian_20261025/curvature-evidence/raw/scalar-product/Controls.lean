import ScalarProductCurvatureBound
import Mathlib.MeasureTheory.Measure.Lebesgue.Basic
import Mathlib.Tactic.NormNum

noncomputable section
open I4ScalarProductCurvature MeasureTheory Set
open scoped ENNReal

private def scalar : Measure ℝ := volume.restrict (Icc (-1/2 : ℝ) (1/2 : ℝ))
private instance scalar_probability : IsProbabilityMeasure scalar := by
  constructor
  norm_num [scalar, Measure.restrict_apply_univ, Real.volume_Icc]

private lemma scalar_density (a : ℝ) (ha : 0 ≤ a) :
    scalar.real (Icc (-a) a) ≤ 2 * 1 * a := by
  have hm : scalar (Icc (-a) a) ≤ volume (Icc (-a) a) :=
    Measure.restrict_apply_le _ _
  have hfin : volume (Icc (-a) a) ≠ ∞ := by rw [Real.volume_Icc]; finiteness
  have hb := ENNReal.toReal_mono hfin hm
  simpa [Measure.real, Real.volume_Icc, sub_neg_eq_add, two_mul, ha, show 0 ≤ a+a by positivity] using hb

-- A literal uniform scalar law and a residual radius 2: powers 12+5 give 17.
example (r : ℝ) (hr : 0 ≤ r) :
    (∫ _p in {p : ℝ × Unit | |p.1| ≤ r * 2^5},
      r^4 * 2^12 ∂scalar.prod (Measure.dirac ())) ≤ 2 * r^5 * 2^17 := by
  have he : MeasurableSet {p : ℝ × Unit | |p.1| ≤ r * 2^5} := by
    exact measurableSet_le (by fun_prop) measurable_const
  have hb := scalar_product_tube_integral_bound scalar (Measure.dirac ())
    (fun _ : Unit => (2 : ℝ)) (fun _ => by norm_num) (integrable_const _)
    {p : ℝ × Unit | |p.1| ≤ r * 2^5} he
    (fun _ => r^4 * 2^12) (integrable_const _) r 1 1 1 hr (by norm_num)
    (by norm_num) (by norm_num) scalar_density
    (fun p hp => by simpa using hp)
    (fun p hp => by simp)
  simpa using hb

-- Zero-radius regular cutoff arithmetic, and nonzero q permitted when its slab allows it.
example : (1 : ℝ) ≤ (1*(1+1*1))*1 ∧
    |(0 : ℝ)| ≤ 1*(1*(1+1*1))^5*0*1^5 ∧
    2*(0 : ℝ)^2*1^2*0^2+8*0^4*1^4 ≤
      (2*1^2*(1*(1+1*1))^12+8*(1*(1+1*1))^4)*0^4*1^12 := by
  exact regular_bounds (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num)

