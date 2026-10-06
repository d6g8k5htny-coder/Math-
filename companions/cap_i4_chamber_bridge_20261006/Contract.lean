import CapI4ChamberBridge
open MeasureTheory Set
open scoped ENNReal Real

example (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2}, G l) =
      ∫⁻ T : ℝ in Ioi 0, ∫⁻ x : ℝ in Ioo 0 T, G (x,T) :=
  CapI4ChamberBridge.positive_chamber_lintegral G hG

example (ν : Measure ℝ) (C0 c r K k0 : ℝ) :
    (∫⁻ j, (ENNReal.ofReal Real.pi *
      ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
        ENNReal.ofReal (l.2-l.1) *
          (ENNReal.ofReal (C0*Real.exp (-c*(l.1^2+l.2^2))) *
            CapI4DepthKernel.depthKernel r K k0 (j,l))) ∂ν) =
    ENNReal.ofReal Real.pi * (∫⁻ j, (∫⁻ T : ℝ in Ioi 0,
      ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
        (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
          CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ∂ν) :=
  CapI4ChamberBridge.gaussian_depth_plane_eq ν C0 c r K k0

example (ν : Measure ℝ) [IsFiniteMeasure ν]
    (C0 c r K k0 : ℝ) (hC0 : 0 ≤ C0) (hc : 0 < c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0)
    (hsupp : ∀ᵐ j ∂ν, 1 ≤ j) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫⁻ j, (ENNReal.ofReal Real.pi *
      ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
        ENNReal.ofReal (l.2-l.1) *
          (ENNReal.ofReal (C0*Real.exp (-c*(l.1^2+l.2^2))) *
            CapI4DepthKernel.depthKernel r K k0 (j,l))) ∂ν) ≤
    ENNReal.ofReal (256*Real.pi*C0*(K^2*(1+K)/4)*
      (((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*r^5*
      ((∫ j : ℝ, |j|^9 ∂ν)*(∫ T : ℝ in Ioi 0, T^2*Real.exp (-c*T^2)) +
        ν.real univ*(∫ T : ℝ in Ioi 0, |T|^11*Real.exp (-c*T^2)))) :=
  CapI4ChamberBridge.gaussian_depth_plane_le ν C0 c r K k0 hC0 hc hr hK hk0 hsupp h9

example (ν : Measure ℝ) [IsFiniteMeasure ν]
    (C0 c r K k0 : ℝ) (hC0 : 0 ≤ C0) (hc : 0 < c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0)
    (hsupp : ∀ᵐ j ∂ν, 1 ≤ j) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫⁻ j, (ENNReal.ofReal Real.pi *
      ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
        ENNReal.ofReal (l.2-l.1) *
          (ENNReal.ofReal (C0*Real.exp (-c*(l.1^2+l.2^2))) *
            CapI4DepthKernel.depthKernel r K k0 (j,l))) ∂ν) < ∞ :=
  CapI4ChamberBridge.gaussian_depth_plane_lt_top ν C0 c r K k0 hC0 hc hr hK hk0 hsupp h9
