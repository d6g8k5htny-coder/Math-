import AdaptiveFoldTransverseRidge
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Calculus.Deriv.Pow

open Set
open scoped ContDiff

namespace AdaptiveFoldBoundaryPath

open AdaptiveFoldTransverseRidge

/-- A scalar second-derivative upper bound gives the precise quadratic loss
from a zero of the first derivative. The jets are full derivatives, including
at the endpoints of the closed interval. -/
theorem quadratic_loss_of_second_derivative
    {f f₁ f₂ : ℝ → ℝ} {a b c z y : ℝ}
    (hf : ∀ t ∈ Icc a b, HasDerivAt f (f₁ t) t)
    (hf₁ : ∀ t ∈ Icc a b, HasDerivAt f₁ (f₂ t) t)
    (hneg : ∀ t ∈ Icc a b, f₂ t ≤ -c)
    (hz : z ∈ Icc a b) (hroot : f₁ z = 0) (hy : y ∈ Icc a b) :
    f y ≤ f z - (c / 2) * (y - z) ^ 2 := by
  let g : ℝ → ℝ := fun t => f t + (c / 2) * (t - z) ^ 2
  let g₁ : ℝ → ℝ := fun t => f₁ t + c * (t - z)
  let g₂ : ℝ → ℝ := fun t => f₂ t + c
  have hg : ∀ t ∈ Icc a b, HasDerivAt g (g₁ t) t := by
    intro t ht
    have hq : HasDerivAt (fun t : ℝ => (c / 2) * (t - z) ^ 2)
        (c * (t - z)) t := by
      convert (((hasDerivAt_id t).sub_const z).pow 2).const_mul (c / 2) using 1 <;>
        dsimp <;> ring
    exact (hf t ht).add hq
  have hg₁ : ∀ t ∈ Icc a b, HasDerivAt g₁ (g₂ t) t := by
    intro t ht
    have hlin : HasDerivAt (fun t : ℝ => c * (t - z)) c t := by
      simpa only [id_eq, mul_one] using ((hasDerivAt_id t).sub_const z).const_mul c
    exact (hf₁ t ht).add hlin
  have hconc : ConcaveOn ℝ (Icc a b) g := by
    apply concaveOn_of_hasDerivWithinAt2_nonpos (convex_Icc a b)
      (f' := g₁) (f'' := g₂)
    · intro t ht
      exact (hg t ht).continuousAt.continuousWithinAt
    · intro t ht
      exact (hg t (interior_subset ht)).hasDerivWithinAt
    · intro t ht
      exact (hg₁ t (interior_subset ht)).hasDerivWithinAt
    · intro t ht
      dsimp [g₂]
      linarith [hneg t (interior_subset ht)]
  have hgz : HasDerivAt g 0 z := by
    simpa [g₁, hroot] using hg z hz
  have hmax : g y ≤ g z := by
    rcases lt_trichotomy y z with hlt | heq | hgt
    · have hs := hconc.le_slope_of_hasDerivAt hy hz hlt hgz
      rw [slope_def_field] at hs
      have hsub : 0 ≤ g z - g y := by
        simpa only [zero_mul] using (le_div_iff₀ (sub_pos.mpr hlt)).mp hs
      linarith
    · exact heq ▸ le_rfl
    · have hs := hconc.slope_le_of_hasDerivAt hz hy hgt hgz
      rw [slope_def_field] at hs
      have hsub : g y - g z ≤ 0 := by
        simpa only [zero_mul] using (div_le_iff₀ (sub_pos.mpr hgt)).mp hs
      linarith
  dsimp [g] at hmax
  nlinarith

/-- The scalar loss lemma applied to the literal potential and its actual
coordinate partials. No norm convention or mixed-partial symmetry is used. -/
theorem vertical_quadratic_loss
    {V : ℝ × ℝ → ℝ} {O : Set (ℝ × ℝ)} {R c x z y : ℝ}
    (hO : IsOpen O) (hV : ContDiffOn ℝ 4 V O)
    (hstrip : ∀ t ∈ Icc (-R) R, (x, t) ∈ O)
    (hneg : ∀ t ∈ Icc (-R) R, partialY (Vy V) (x, t) ≤ -c)
    (hz : z ∈ Icc (-R) R) (hroot : Vy V (x, z) = 0)
    (hy : y ∈ Icc (-R) R) :
    V (x, y) ≤ V (x, z) - (c / 2) * (y - z) ^ 2 := by
  have hG : ContDiffOn ℝ 2 (Vy V) O := contDiffOn_partialY hO hV (by norm_num)
  apply quadratic_loss_of_second_derivative
    (f := fun t => V (x, t)) (f₁ := fun t => Vy V (x, t))
    (f₂ := fun t => partialY (Vy V) (x, t)) _ _ hneg hz hroot hy
  · intro t ht
    exact hasDerivAt_slice ((hV.contDiffAt (hO.mem_nhds (hstrip t ht))).differentiableAt
      (by norm_num))
  · intro t ht
    exact hasDerivAt_slice ((hG.contDiffAt (hO.mem_nhds (hstrip t ht))).differentiableAt
      (by norm_num))

end AdaptiveFoldBoundaryPath
