import CapI4OuterComposition
import Mathlib.Tactic

/-!
Exact positive-chamber rearrangement connecting the upstream spectral plane to
R20's iterated finite bound. No field model or normalization is instantiated.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4ChamberBridge

/-- The measurable positive chamber is decomposed in reverse integration order, without swapping the test. -/
theorem positive_chamber_lintegral (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2}, G l) =
      ∫⁻ T : ℝ in Ioi 0, ∫⁻ x : ℝ in Ioo 0 T, G (x,T) := by
  have hs : MeasurableSet {l : ℝ × ℝ | 0 < l.1 ∧ l.1 < l.2} :=
    (isOpen_lt continuous_const continuous_fst).measurableSet.inter
      (isOpen_lt continuous_fst continuous_snd).measurableSet
  rw [← lintegral_indicator hs]
  calc
    _ = ∫⁻ T : ℝ, ∫⁻ x : ℝ,
        {l : ℝ × ℝ | 0 < l.1 ∧ l.1 < l.2}.indicator G (x,T) :=
      lintegral_prod_symm _ (hG.indicator hs).aemeasurable
    _ = _ := by
      rw [← lintegral_indicator measurableSet_Ioi]
      apply lintegral_congr
      intro T
      by_cases hT : 0 < T
      · rw [Set.indicator_of_mem (show T ∈ Ioi (0 : ℝ) from hT)]
        rw [← lintegral_indicator measurableSet_Ioo]
        rfl
      · rw [Set.indicator_of_notMem (show T ∉ Ioi (0 : ℝ) from hT)]
        have hz (x : ℝ) :
            {l : ℝ × ℝ | 0 < l.1 ∧ l.1 < l.2}.indicator G (x,T) = 0 := by
          have hx : (x,T) ∉ {l : ℝ × ℝ | 0 < l.1 ∧ l.1 < l.2} := by
            intro h
            exact hT (lt_trans h.1 h.2)
          exact Set.indicator_of_notMem hx G
        simp only [hz, lintegral_zero]

/-- The actual kernel plane integral equals the iterated expression, with arbitrary residual measure. -/
theorem gaussian_depth_plane_eq (ν : Measure ℝ) (C0 c r K k0 : ℝ) :
    (∫⁻ j, (ENNReal.ofReal Real.pi *
      ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
        ENNReal.ofReal (l.2-l.1) *
          (ENNReal.ofReal (C0*Real.exp (-c*(l.1^2+l.2^2))) *
            CapI4DepthKernel.depthKernel r K k0 (j,l))) ∂ν) =
    ENNReal.ofReal Real.pi * (∫⁻ j, (∫⁻ T : ℝ in Ioi 0,
      ∫⁻ x : ℝ in Ioo 0 T, ENNReal.ofReal (T-x) *
        (ENNReal.ofReal (C0*Real.exp (-c*(x^2+T^2))) *
          CapI4DepthKernel.depthKernel r K k0 (j,(x,T)))) ∂ν) := by
  let F : ℝ × (ℝ × ℝ) → ℝ≥0∞ := fun z =>
    ENNReal.ofReal (z.2.2-z.2.1) *
      (ENNReal.ofReal (C0*Real.exp (-c*(z.2.1^2+z.2.2^2))) *
        CapI4DepthKernel.depthKernel r K k0 z)
  have hk := CapI4DepthKernel.measurable_depthKernel r K k0
  have hF : Measurable F := by dsimp [F]; fun_prop
  have hslice : Measurable (fun j : ℝ =>
      ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2}, F (j,l)) :=
    hF.lintegral_prod_right'
  calc
    _ = ENNReal.ofReal Real.pi * (∫⁻ j,
        (∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2}, F (j,l)) ∂ν) :=
      lintegral_const_mul _ hslice
    _ = _ := by
      congr 1
      apply lintegral_congr
      intro j
      exact positive_chamber_lintegral (fun l => F (j,l))
        (hF.comp (measurable_const.prodMk measurable_id))

/-- Transfer the existing finite outer estimate to the spectral-plane side used by the weight bound. -/
theorem gaussian_depth_plane_le (ν : Measure ℝ) [IsFiniteMeasure ν]
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
        ν.real univ*(∫ T : ℝ in Ioi 0, |T|^11*Real.exp (-c*T^2)))) := by
  rw [gaussian_depth_plane_eq]
  exact CapI4OuterComposition.gaussian_depth_outer_le
    ν C0 c r K k0 hC0 hc hr hK hk0 hsupp h9

/-- Finiteness of that plane expression; no matrix model or probability normalization is asserted. -/
theorem gaussian_depth_plane_lt_top (ν : Measure ℝ) [IsFiniteMeasure ν]
    (C0 c r K k0 : ℝ) (hC0 : 0 ≤ C0) (hc : 0 < c)
    (hr : 0 ≤ r) (hK : 0 ≤ K) (hk0 : 0 < k0)
    (hsupp : ∀ᵐ j ∂ν, 1 ≤ j) (h9 : Integrable (fun j : ℝ => |j|^9) ν) :
    (∫⁻ j, (ENNReal.ofReal Real.pi *
      ∫⁻ l : ℝ × ℝ in {l | 0 < l.1 ∧ l.1 < l.2},
        ENNReal.ofReal (l.2-l.1) *
          (ENNReal.ofReal (C0*Real.exp (-c*(l.1^2+l.2^2))) *
            CapI4DepthKernel.depthKernel r K k0 (j,l))) ∂ν) < ∞ := by
  rw [gaussian_depth_plane_eq]
  exact CapI4OuterComposition.gaussian_depth_outer_lt_top
    ν C0 c r K k0 hC0 hc hr hK hk0 hsupp h9

end CapI4ChamberBridge
