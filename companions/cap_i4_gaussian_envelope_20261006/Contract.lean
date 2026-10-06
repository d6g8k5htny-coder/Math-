import CapI4GaussianEnvelope
open MeasureTheory Set
open scoped ENNReal

example (c : ℝ) (hc : 0 < c) (n : ℕ) :
    Integrable (fun t : ℝ => |t|^n * Real.exp (-c*t^2)) :=
  CapI4GaussianEnvelope.gaussian_abs_moment_integrable c hc n

example (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) :
    (x+y)^9 ≤ 256*(x^9+y^9) :=
  CapI4GaussianEnvelope.ninth_power_le x y hx hy

example (c j t : ℝ) :
    (|j|+|t|)^9*t^2*Real.exp (-c*t^2) ≤
      256*(|j|^9*(t^2*Real.exp (-c*t^2)) + 1*(|t|^11*Real.exp (-c*t^2))) :=
  CapI4GaussianEnvelope.mixed_envelope_pointwise_le c j t

example (ν : Measure ℝ) [IsFiniteMeasure ν]
    (c : ℝ) (hc : 0 < c) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    Integrable (fun z : ℝ × ℝ => (|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2))
      (ν.prod (volume.restrict (Ioi 0))) :=
  CapI4GaussianEnvelope.mixed_envelope_integrable ν c hc h9

example (ν : Measure ℝ) [IsFiniteMeasure ν]
    (c : ℝ) (hc : 0 < c) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫ z : ℝ × ℝ, (|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2)
      ∂ν.prod (volume.restrict (Ioi 0))) ≤
      256*((∫ j : ℝ, |j|^9 ∂ν)*(∫ t : ℝ in Ioi 0, t^2*Real.exp (-c*t^2)) +
        ν.real univ*(∫ t : ℝ in Ioi 0, |t|^11*Real.exp (-c*t^2))) :=
  CapI4GaussianEnvelope.mixed_envelope_integral_le ν c hc h9

example (ν : Measure ℝ) [IsFiniteMeasure ν]
    (c : ℝ) (hc : 0 < c) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫⁻ z : ℝ × ℝ, ENNReal.ofReal ((|z.1|+|z.2|)^9*z.2^2*Real.exp (-c*z.2^2))
      ∂ν.prod (volume.restrict (Ioi 0))) ≤
      ENNReal.ofReal (256*((∫ j : ℝ, |j|^9 ∂ν)*(∫ t : ℝ in Ioi 0, t^2*Real.exp (-c*t^2)) +
        ν.real univ*(∫ t : ℝ in Ioi 0, |t|^11*Real.exp (-c*t^2)))) :=
  CapI4GaussianEnvelope.mixed_envelope_lintegral_le ν c hc h9

