import CapI4Angular

noncomputable section
open MeasureTheory Set
open scoped ENNReal Real

example (g : ℝ → ℝ≥0∞) (hg : Measurable g) :
    (∫⁻ q : ℝ × ℝ in polarCoord.target, g q.1) =
      ENNReal.ofReal (2 * Real.pi) * ∫⁻ r : ℝ in Ioi 0, g r :=
  CapI4Angular.angle_lintegral g hg

example (t : ℝ) (F : ℝ × ℝ → ℝ≥0∞) (hF : Measurable F) :
    (∫⁻ z : ℝ × ℝ, F (CapI4Polar.spectrum t z)) =
      ENNReal.ofReal (2 * Real.pi) *
        ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal r * F (t - r, t + r) :=
  CapI4Angular.polar_spectral_radial t F hF

example (t : ℝ) (p w F : ℝ × ℝ → ℝ≥0∞)
    (hw : Measurable w) (hF : Measurable F)
    (hdom : ∀ z, p z ≤ w (CapI4Polar.spectrum t z)) :
    (∫⁻ z : ℝ × ℝ, p z * F (CapI4Polar.spectrum t z)) ≤
      ENNReal.ofReal (2 * Real.pi) *
        ∫⁻ r : ℝ in Ioi 0, ENNReal.ofReal r *
          (w (t - r, t + r) * F (t - r, t + r)) :=
  CapI4Angular.density_radial_bound t p w F hw hF hdom
