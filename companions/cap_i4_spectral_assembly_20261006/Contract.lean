import CapI4SpectralAssembly
open MeasureTheory Set
open scoped ENNReal Real

example (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ e : ℝ × (ℝ × ℝ),
      if 0 < (CapI4Polar.eigenvalues e).1
      then G (CapI4Polar.eigenvalues e) else 0) =
      ENNReal.ofReal Real.pi *
        ∫⁻ q : ℝ × ℝ in {q | 0 < q.1 ∧ q.1 < q.2},
          ENNReal.ofReal (q.2 - q.1) * G q :=
  CapI4SpectralAssembly.entry_positive_spectral_lintegral G hG
