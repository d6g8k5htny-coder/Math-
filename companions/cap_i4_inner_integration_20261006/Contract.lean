import CapI4InnerIntegration
open MeasureTheory Set
open scoped ENNReal

example (T L b : ℝ) :
    (∫⁻ x : ℝ in Ioc 0 T,
      if x ≤ L then ENNReal.ofReal (x*(x+b)*(T-x)) else 0) =
    ∫⁻ x : ℝ in Ioc 0 (min T L), ENNReal.ofReal (x*(x+b)*(T-x)) :=
  CapI4InnerIntegration.cutoff_gap_lintegral_eq T L b

example (T L b : ℝ) (hT : 0 ≤ T) (hL : 0 ≤ L) (hb : 0 ≤ b) :
    (∫⁻ x : ℝ in Ioc 0 T,
      if x ≤ L then ENNReal.ofReal (x*(x+b)*(T-x)) else 0) ≤
    ENNReal.ofReal (T*(L^3/3+b*L^2/2)) :=
  CapI4InnerIntegration.cutoff_gap_lintegral_le T L b hT hL hb

example (r K k0 j T : ℝ) (hr : 0 ≤ r) (hK : 0 ≤ K)
    (hk0 : 0 < k0) (hj : 0 ≤ j) (hT : 0 ≤ T) :
    (∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
      CapI4DepthKernel.depthKernel r K k0 (j,(x,T))) ≤
    ENNReal.ofReal ((K^2*(1+K)/4)*r^5*T^2*
      (((4*K^2/(3*k0))^3/3)*(j+T)^9+
       ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^8)) :=
  CapI4InnerIntegration.depth_slice_le r K k0 j T hr hK hk0 hj hT

example (C0 c r K k0 j T : ℝ) (hC0 : 0 ≤ C0) (hc : 0 ≤ c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0) (hj : 0 ≤ j) (hT : 0 ≤ T) :
    (∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
      (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
       CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ≤
    ENNReal.ofReal (C0*Real.exp (-c*T^2)*(K^2*(1+K)/4)*r^5*T^2*
      (((4*K^2/(3*k0))^3/3)*(j+T)^9+
       ((3*K/2)*(4*K^2/(3*k0))^2/2)*(j+T)^8)) :=
  CapI4InnerIntegration.gaussian_depth_slice_le C0 c r K k0 j T hC0 hc hr hK hk0 hj hT

example (C0 c r K k0 j T : ℝ) (hC0 : 0 ≤ C0) (hc : 0 ≤ c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0) (hj : 1 ≤ j) (hT : 0 ≤ T) :
    (∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
      (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
       CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ≤
    ENNReal.ofReal (C0*Real.exp (-c*T^2)*(K^2*(1+K)/4)*r^5*T^2*
      (((4*K^2/(3*k0))^3/3)+((3*K/2)*(4*K^2/(3*k0))^2/2))*(j+T)^9) :=
  CapI4InnerIntegration.gaussian_depth_slice_ninth_le C0 c r K k0 j T hC0 hc hr hK hk0 hj hT
