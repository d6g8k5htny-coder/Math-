import CapI4DepthKernel
open MeasureTheory ProbabilityTheory Set
open scoped ENNReal

example (r K k0 j lam top : ℝ) :
    CapI4DepthKernel.depthKernel r K k0 (j,(lam,top)) =
      if lam ≤ (4*K^2/(3*k0))*r*(j+top)^2 then
        ENNReal.ofReal ((K^2*(1+K)/4)*r^2*top*(j+top)^3*lam*
          (lam+(3*K/2)*r*(j+top))) else 0 := rfl

example (r K k0 : ℝ) : Measurable (CapI4DepthKernel.depthKernel r K k0) :=
  CapI4DepthKernel.measurable_depthKernel r K k0

example (r K j lam top h : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (hK : 0 ≤ K) (hj : 0 ≤ j) (hlam : 0 ≤ lam) (htop : 0 ≤ top)
    (hh : 0 ≤ h) (hhU : h ≤ K*(j+top)) :
    (r^2*h^2/4)*lam*(lam+(3/2)*r*h)*top*(top+r*h) ≤
      (K^2*(1+K)/4)*r^2*top*(j+top)^3*lam*(lam+(3*K/2)*r*(j+top)) :=
  CapI4DepthKernel.double_soft_majorant r K j lam top h hr hr1 hK hj hlam htop hh hhU

example (r K k0 k j lam top h : ℝ) (hr : 0 ≤ r) (hK : 0 ≤ K)
    (hk0 : 0 < k0) (hk : k0 ≤ k) (hj : 0 ≤ j) (htop : 0 ≤ top)
    (hh : 0 ≤ h) (hhU : h ≤ K*(j+top))
    (hfail : lam ≤ (4/(3*k))*r*h^2) :
    lam ≤ (4*K^2/(3*k0))*r*(j+top)^2 :=
  CapI4DepthKernel.depth_cutoff r K k0 k j lam top h hr hK hk0 hk hj htop hh hhU hfail

example (r K k0 k j lam top h w : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1)
    (hK : 0 ≤ K) (hk0 : 0 < k0) (hk : k0 ≤ k)
    (hs : 0 < w → 0 < lam ∧ lam ≤ top ∧ 0 ≤ j ∧ 0 ≤ h ∧
      h ≤ K*(j+top) ∧ w ≤ (r^2*h^2/4)*lam*(lam+(3/2)*r*h)*top*(top+r*h)) :
    ENNReal.ofReal (if lam ≤ (4/(3*k))*r*h^2 then w else 0) ≤
      if 0 < lam then CapI4DepthKernel.depthKernel r K k0 (j,(lam,top)) else 0 :=
  CapI4DepthKernel.typed_depth_weight_le r K k0 k j lam top h w hr hr1 hK hk0 hk hs

example {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω) [IsProbabilityMeasure Q]
    (J : Ω → ℝ) (B : Ω → ℝ × (ℝ × ℝ)) (hJ : Measurable J) (hB : Measurable B)
    (hI : IndepFun J B Q) (p : ℝ × (ℝ × ℝ) → ℝ≥0∞)
    (hB_law : Measure.map B Q = (volume : Measure (ℝ × (ℝ × ℝ))).withDensity p)
    (H : ℝ × ℝ → ℝ≥0∞) (hp : Measurable p) (hH : Measurable H)
    (hdom : ∀ e, p e ≤ H (CapI4Polar.eigenvalues e))
    (r K k0 k : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1) (hK : 0 ≤ K)
    (hk0 : 0 < k0) (hk : k0 ≤ k) (h w : Ω → ℝ)
    (hdata : ∀ᵐ ω ∂Q, 0 < w ω →
      0 < (CapI4Polar.eigenvalues (B ω)).1 ∧
      (CapI4Polar.eigenvalues (B ω)).1 ≤ (CapI4Polar.eigenvalues (B ω)).2 ∧
      0 ≤ J ω ∧ 0 ≤ h ω ∧ h ω ≤ K*(J ω+(CapI4Polar.eigenvalues (B ω)).2) ∧
      w ω ≤ (r^2*(h ω)^2/4)*(CapI4Polar.eigenvalues (B ω)).1*
        ((CapI4Polar.eigenvalues (B ω)).1+(3/2)*r*h ω)*
        (CapI4Polar.eigenvalues (B ω)).2*((CapI4Polar.eigenvalues (B ω)).2+r*h ω)) :
    (∫⁻ ω, ENNReal.ofReal (if (CapI4Polar.eigenvalues (B ω)).1 ≤
      (4/(3*k))*r*(h ω)^2 then w ω else 0) ∂Q) ≤
    ∫⁻ j, (ENNReal.ofReal Real.pi * ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
      ENNReal.ofReal (l.2-l.1)*(H l*CapI4DepthKernel.depthKernel r K k0 (j,l))) ∂Measure.map J Q :=
  CapI4DepthKernel.independent_depth_bound_ae Q J B hJ hB hI p hB_law H hp hH hdom
    r K k0 k hr hr1 hK hk0 hk h w hdata
