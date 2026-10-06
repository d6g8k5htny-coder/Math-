import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Tactic

/-!
Clipped soft-eigenvalue integration for Cap I4. The signed gap is retained only
on its original chamber. This is finite integral algebra, not a Gaussian model.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal
namespace CapI4ClippedIntegral

/-- Exact signed polynomial integral, valid also for negative oriented endpoints. -/
theorem gap_integral_exact (a b T : ℝ) :
    (∫ x in (0 : ℝ)..a, x*(x+b)*(T-x)) =
      T*a^3/3 + T*b*a^2/2 - a^4/4 - b*a^3/3 := by
  have hp : (fun x : ℝ => x*(x+b)*(T-x)) =
      (fun x => (T*x^2+(T*b)*x-x^3)-b*x^2) := by
    funext x
    ring
  have hT2 : IntervalIntegrable (fun x : ℝ => T*x^2) volume 0 a :=
    (by fun_prop : Continuous (fun x : ℝ => T*x^2)).intervalIntegrable 0 a
  have hTb : IntervalIntegrable (fun x : ℝ => (T*b)*x) volume 0 a :=
    (by fun_prop : Continuous (fun x : ℝ => (T*b)*x)).intervalIntegrable 0 a
  have h3 : IntervalIntegrable (fun x : ℝ => x^3) volume 0 a :=
    (by fun_prop : Continuous (fun x : ℝ => x^3)).intervalIntegrable 0 a
  have hb2 : IntervalIntegrable (fun x : ℝ => b*x^2) volume 0 a :=
    (by fun_prop : Continuous (fun x : ℝ => b*x^2)).intervalIntegrable 0 a
  rw [hp, intervalIntegral.integral_sub ((hT2.add hTb).sub h3) hb2,
    intervalIntegral.integral_sub (hT2.add hTb) h3,
    intervalIntegral.integral_add hT2 hTb]
  simp only [intervalIntegral.integral_const_mul, _root_.integral_pow, _root_.integral_id]
  norm_num <;> ring

/-- Nonnegativity uses a <= T, and does not hold on an arbitrarily enlarged interval. -/
theorem clipped_integral_nonneg (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    0 ≤ ∫ x in (0 : ℝ)..min T L, x*(x+b)*(T-x) := by
  have ha : 0 ≤ min T L := le_min hT hL
  have hgap : 0 ≤ T-min T L := sub_nonneg.mpr (min_le_left T L)
  rw [gap_integral_exact]
  calc
    0 ≤ (min T L)^2 * ((T-min T L)*(min T L/3+b/2) +
        (min T L)^2/12+b*(min T L)/6) := by positivity
    _ = _ := by ring

/-- Bound the gap on the original clipped interval before enlarging the soft primitive. -/
theorem clipped_integral_le (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    (∫ x in (0 : ℝ)..min T L, x*(x+b)*(T-x)) ≤
      T*(L^3/3+b*L^2/2) := by
  have ha : 0 ≤ min T L := le_min hT hL
  rw [gap_integral_exact]
  calc
    _ ≤ T*((min T L)^3/3+b*(min T L)^2/2) := by
      have h4 : 0 ≤ (min T L)^4/4 := by positivity
      have h3 : 0 ≤ b*(min T L)^3/3 := by positivity
      nlinarith
    _ ≤ _ := by gcongr <;> exact min_le_right T L

/-- The saturated chamber value, with the gap still present. -/
theorem full_chamber_integral (T b : ℝ) :
    (∫ x in (0 : ℝ)..T, x*(x+b)*(T-x)) = T^4/12+b*T^3/6 := by
  rw [gap_integral_exact]
  ring

/-- The determinant prefactor and clipped soft integral supply the exact r^5 ledger. -/
theorem moving_prefactor_le (A T r D E U : ℝ) (hA : 0 ≤ A) (hT : 0 ≤ T)
    (hr : 0 ≤ r) (hD : 0 ≤ D) (hE : 0 ≤ E) (hU : 0 ≤ U) :
    A*r^2*T*U^3*(∫ x in (0 : ℝ)..min T (D*r*U^2),
      x*(x+E*r*U)*(T-x)) ≤
      A*r^5*T^2*((D^3/3)*U^9+(E*D^2/2)*U^8) := by
  have hbound := clipped_integral_le T (D*r*U^2) (E*r*U) hT
    (by positivity) (by positivity)
  calc
    _ ≤ A*r^2*T*U^3*(T*((D*r*U^2)^3/3+(E*r*U)*(D*r*U^2)^2/2)) :=
      mul_le_mul_of_nonneg_left hbound (by positivity)
    _ = _ := by ring

/-- Explicit finite-integrability bridge to the nonnegative measure integral. -/
theorem clipped_lintegral_eq (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    (∫⁻ x : ℝ in Ioc 0 (min T L), ENNReal.ofReal (x*(x+b)*(T-x))) =
      ENNReal.ofReal (T*(min T L)^3/3+T*b*(min T L)^2/2-
        (min T L)^4/4-b*(min T L)^3/3) := by
  have ha : 0 ≤ min T L := le_min hT hL
  have hi : IntervalIntegrable (fun x : ℝ => x*(x+b)*(T-x)) volume 0 (min T L) :=
    (by fun_prop : Continuous (fun x : ℝ => x*(x+b)*(T-x))).intervalIntegrable _ _
  have hn : 0 ≤ᵐ[volume.restrict (Ioc 0 (min T L))]
      (fun x : ℝ => x*(x+b)*(T-x)) := by
    filter_upwards [ae_restrict_mem measurableSet_Ioc] with x hx
    exact mul_nonneg (mul_nonneg hx.1.le (add_nonneg hx.1.le hb))
      (sub_nonneg.mpr (hx.2.trans (min_le_left T L)))
  rw [← ofReal_integral_eq_lintegral_ofReal hi.1 hn,
    ← intervalIntegral.integral_of_le ha, gap_integral_exact]

end CapI4ClippedIntegral
