import SourceAdaptiveFoldEstimates
import SourceLifetimeGeometry
import ElderClearance

/-! Exact real-cover strict-clearance death for the unchanged actual source.
The global real-space chart transports the retained wide box and path; absolute
raw-pin heights restore the offset absent from normalized gap data. -/

noncomputable section
open Set MeasureTheory
open I4SmoothCarrier I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4SourceAdaptiveFoldChart
open I4SourceAdaptiveFoldEstimates I4LifetimeField
open AdaptiveFoldBoundaryPath
set_option autoImplicit false

namespace I4SourceActualFoldDeath

/-- The literal pair/Pi coordinate change and nonzero physical dilation form a
homeomorphism of real spaces, with no quotient involved. -/
def physicalChart (r : ℝ) (hr : r ≠ 0) :
    (ℝ × ℝ) ≃ₜ TorusFiltration.superlevelBar_E 2 where
  toFun p := (coordinates 2).symm (r • ![p.1,p.2])
  invFun x := ((r⁻¹ • coordinates 2 x) 0, (r⁻¹ • coordinates 2 x) 1)
  left_inv p := by simp [smul_smul, hr]
  right_inv x := by
    apply (coordinates 2).injective
    ext i
    fin_cases i <;> simp [smul_smul, hr]
  continuous_toFun := (coordinates 2).symm.continuous.comp
    (continuous_const.smul (continuous_pi (by
      intro i
      fin_cases i
      · exact continuous_fst
      · exact continuous_snd)))
  continuous_invFun :=
    ((continuous_const.smul (coordinates 2).continuous).apply 0).prodMk
      ((continuous_const.smul (coordinates 2).continuous).apply 1)

@[simp] theorem physicalChart_M (r : ℝ) (hr : r ≠ 0) :
    physicalChart r hr M = (coordinates 2).symm (endpointM r) := by
  change (coordinates 2).symm (r • ![-1/2,0]) = _
  rw [chart_endpointM]

@[simp] theorem physicalChart_S (r : ℝ) (hr : r ≠ 0) :
    physicalChart r hr S = (coordinates 2).symm (endpointS r) := by
  change (coordinates 2).symm (r • ![1/2,0]) = _
  rw [chart_endpointS]

/-- The positive physical amplitude is retained without an offset subtraction. -/
theorem actualField_pullback {L r k : ℝ} (sample : SmoothSample 2 L)
    (hr : r ≠ 0) (hk : k ≠ 0) (p : ℝ × ℝ) :
    actualField 2 L sample (physicalChart r hr p) =
      (6*k*r^3) * actualFoldPotential r k sample p := by
  simp only [actualField, physicalChart, ContinuousLinearEquiv.apply_symm_apply,
    actualFoldPotential]
  field_simp

/-- Continuity for the original period, including negative nonzero periods. -/
theorem actualField_continuous {L : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) : Continuous (actualField 2 L sample) :=
  (smoothSourceField_smooth 2 hL sample).continuous.comp (coordinates 2).continuous

/-- Transport the same rectangle and retained path, then call the existing
strict-clearance/death results. The endpoints are absolute physical heights. -/
theorem scaled_rectangle_death
    (g : TorusFiltration.superlevelBar_E 2 → ℝ) (hg : Continuous g)
    (V : ℝ × ℝ → ℝ) (r a b d R c : ℝ) (z : ℝ → ℝ)
    (hr : r ≠ 0) (ha : 0 < a)
    (hpull : ∀ p, g (physicalChart r hr p) = a * V p)
    (hm : g (physicalChart r hr M) = b)
    (hs : g (physicalChart r hr S) = d)
    (h : RectangleBoundaryPathData V R c z) :
    TorusFiltration.superlevelBar_deathHeight g (physicalChart r hr M) = d ∧
      TorusFiltration.superlevelBar_clearanceSet g (physicalChart r hr M) = Iio d := by
  let A := physicalChart r hr
  let D := A '' leftBox R
  have hcompact : IsCompact D :=
    (isCompact_Icc.prod isCompact_Icc).image A.continuous
  have hfrontier : frontier D = A '' frontier (leftBox R) :=
    (A.image_frontier (leftBox R)).symm
  have hboundary : ∀ x ∈ frontier D, g x ≤ d := by
    intro x hx
    rw [hfrontier] at hx
    obtain ⟨p,hp,rfl⟩ := hx
    rw [hpull, ← hs, hpull]
    exact mul_le_mul_of_nonneg_left (h.frontier_bound p hp) ha.le
  have hM : A M ∈ D := mem_image_of_mem A h.maximum_mem
  have hheight : ∀ x ∈ D, g x ≤ g (A M) := by
    rintro x ⟨p,hp,rfl⟩
    rw [hpull, hpull]
    exact mul_le_mul_of_nonneg_left (h.ceiling p hp) ha.le
  have holder : g (A M) < g (A (olderPoint z)) := by
    rw [hpull, hpull]
    exact mul_lt_mul_of_pos_left (by linarith [h.older_gain]) ha
  obtain ⟨γ,_hgraph,hfloor,_hmid⟩ := h.path
  let η := γ.map A.continuous
  have hη : ∀ t : unitInterval, d ≤ g (η t) := by
    intro t
    change d ≤ g (A (γ t))
    rw [← hs, hpull, hpull]
    exact mul_le_mul_of_nonneg_left (hfloor t) ha.le
  have htrace := TorusFiltration.elderTrap_strictTrace_isClopen g D d
    hcompact.isClosed hboundary
  exact ⟨TorusFiltration.elderTrap_death_eq g hg D d htrace (A M) hM
      hheight (A (olderPoint z)) holder η hη,
    TorusFiltration.elderTrap_clearance_eq_Iio g D d htrace (A M) hM
      hheight (A (olderPoint z)) holder η hη⟩

/-- Absolute raw pins and the same qualified rectangle suffice pointwise. -/
theorem actual_rectangle_death {L r k b R c : ℝ} (hL : L ≠ 0)
    (sample : SmoothSample 2 L) (z : ℝ → ℝ) (hr : 0 < r) (hk : 0 < k)
    (hp : rawPins L r sample = ![b,b-k*r^3,0,0,0,0])
    (h : RectangleBoundaryPathData (actualFoldPotential r k sample) R c z) :
    TorusFiltration.superlevelBar_deathHeight (actualField 2 L sample)
        ((coordinates 2).symm (endpointM r)) = b-k*r^3 ∧
      TorusFiltration.superlevelBar_clearanceSet (actualField 2 L sample)
        ((coordinates 2).symm (endpointM r)) = Iio (b-k*r^3) := by
  have hm := congrFun hp (0 : Fin 6)
  have hs := congrFun hp (1 : Fin 6)
  simp only [rawPins, Matrix.cons_val_zero, Matrix.cons_val_one] at hm hs
  have hM : actualField 2 L sample (physicalChart r hr.ne' M) = b := by
    simpa [actualField] using hm
  have hS : actualField 2 L sample (physicalChart r hr.ne' S) = b-k*r^3 := by
    simpa [actualField] using hs
  have hresult := scaled_rectangle_death (actualField 2 L sample)
    (actualField_continuous hL sample) (actualFoldPotential r k sample)
    r (6*k*r^3) b (b-k*r^3) R c z hr.ne' (by positivity)
    (actualField_pullback sample hr.ne' hk.ne') hM hS h
  simpa only [physicalChart_M] using hresult

/-- One radius from hL alone precedes every scale and target. Under the same
actual sample cutoffs, literal physical death and strict clearance are closed
conclusions with no pin, invertibility or desired-trap premise. -/
theorem sourceGapLaw_actual_death_clearance {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            TorusFiltration.superlevelBar_deathHeight (actualField 2 L sample)
                ((coordinates 2).symm (endpointM r)) = b-k*r^3 ∧
              TorusFiltration.superlevelBar_clearanceSet (actualField 2 L sample)
                ((coordinates 2).symm (endpointM r)) = Iio (b-k*r^3) := by
  obtain ⟨δ₁,hδ₁,hδ₁1,hwide⟩ := sourceGapLaw_actual_rectangle_boundary_path hL
  obtain ⟨_K,δ₂,_hK,hδ₂,_hδ₂1,hbounds⟩ := sourceInverse_target_uniform_bounds hL
  refine ⟨min δ₁ δ₂, lt_min hδ₁ hδ₂, (min_le_left _ _).trans hδ₁1, ?_⟩
  intro k₀ hk₀ r hr hrδ b k hk
  have hr₁ : r < δ₁ := hrδ.trans_le (min_le_left _ _)
  have hr₂ : r < δ₂ := hrδ.trans_le (min_le_right _ _)
  have hG := (hbounds r hr hr₂).1
  have hpins : ∀ᵐ sample ∂sourceGapLaw hL r b k,
      rawPins L r sample = ![b,b-k*r^3,0,0,0,0] := by
    rw [sourceGapLaw_eq_rawPinKernel hL r b k hr.ne']
    have hm : MeasurableSet {sample : SmoothSample 2 L |
        rawPins L r sample = ![b,b-k*r^3,0,0,0,0]} :=
      measurableSet_eq_fun (rawPins_measurable hL r) measurable_const
    apply (ae_iff_measure_eq hm.nullMeasurableSet).mpr
    simpa using rawPinKernel_pin_fiber hL r hr.ne' hG ![b,b-k*r^3,0,0,0,0]
  filter_upwards [hwide k₀ hk₀ r hr hr₁ b k hk, hpins] with sample hw hp
  dsimp only at hw ⊢
  intro hrT hκ
  obtain ⟨U,z,_hz,hbox⟩ := hw hrT hκ
  exact actual_rectangle_death hL sample z hr (hk₀.trans_le hk) hp hbox

end I4SourceActualFoldDeath
