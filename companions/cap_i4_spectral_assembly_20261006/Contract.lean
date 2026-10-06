import CapI4SpectralAssembly
open MeasureTheory Set
open scoped ENNReal
example (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0) =
      ENNReal.ofReal Real.pi *
        ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
          ENNReal.ofReal (l.2-l.1) * G l :=
  CapI4SpectralAssembly.entry_positive_spectral_lintegral G hG
example (p : ℝ × (ℝ × ℝ) → ℝ≥0∞) (H G : ℝ × ℝ → ℝ≥0∞)
    (hH : Measurable H) (hG : Measurable G)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e)) :
    (∫⁻ e : ℝ × (ℝ × ℝ), p e *
      (if 0 < (CapI4Polar.eigenvalues e).1 then G (CapI4Polar.eigenvalues e) else 0)) ≤
      ENNReal.ofReal Real.pi *
        ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
          ENNReal.ofReal (l.2-l.1) * (H l * G l) :=
  CapI4SpectralAssembly.density_positive_spectral_bound p H G hH hG hdom
