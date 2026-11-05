import SourceActualFoldDeath

noncomputable section
open Set MeasureTheory
open I4SmoothCarrier I4LifetimeField I4SourceConfluentPins I4SourcePinPreservingQuartic
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates
open I4SourceActualFoldDeath AdaptiveFoldBoundaryPath
open TorusFiltration
set_option autoImplicit false

namespace ActualDeathControls

/-- The scale is physical 6, not the normalized unit scale. -/
theorem actual_scale_control {L : ℝ} (sample : SmoothSample 2 L) (p : ℝ × ℝ) :
    actualField 2 L sample (physicalChart 1 (by norm_num) p) =
      6 * actualFoldPotential 1 1 sample p := by
  simpa using actualField_pullback sample (by norm_num : (1:ℝ) ≠ 0)
    (by norm_num : (1:ℝ) ≠ 0) p

/-- A negative original period, nonzero absolute target and non-unit normalized
amplitude use the same closed actual-law interface. -/
theorem negative_period_actual_law :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ →
      ∀ᵐ sample ∂sourceGapLaw (by norm_num : (-1:ℝ) ≠ 0) r 3 1,
        r*(sourceT 1 sample)^5 ≤ 1/100 →
          1024*(sourceT 1 sample)^5 ≤ sourceKappa r 1 sample →
            superlevelBar_deathHeight (actualField 2 (-1) sample)
                ((coordinates 2).symm (endpointM r)) = 3-r^3 ∧
              superlevelBar_clearanceSet (actualField 2 (-1) sample)
                ((coordinates 2).symm (endpointM r)) = Iio (3-r^3) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_death_clearance
    (by norm_num : (-1:ℝ) ≠ 0)
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ
  simpa using h 1 (by norm_num) r hr hrδ 3 1 le_rfl

/-- A shifted cubic with a genuine transverse drop. -/
def V (p : ℝ × ℝ) : ℝ := p.1^3/3-p.1/4+5/12-p.2^2

def G (x : superlevelBar_E 2) : ℝ := 6 * V ((coordinates 2 x) 0, (coordinates 2 x) 1)

def Mphys : superlevelBar_E 2 := physicalChart 1 (by norm_num) M

theorem polynomial_ceiling (x : ℝ) (hx : x ≤ (1/2:ℝ)) :
    x^3/3-x/4+5/12 ≤ 1/2 := by
  have hh := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg (x+1/2))
    (show x-1 ≤ 0 by linarith)
  nlinarith

theorem polynomial_floor (x : ℝ) (hx : -(1/2:ℝ) ≤ x) :
    1/3 ≤ x^3/3-x/4+5/12 := by
  have hh := mul_nonneg (sq_nonneg (x-1/2)) (show 0 ≤ x+1 by linarith)
  nlinarith

theorem polynomial_rectangle : RectangleBoundaryPathData V 1 2 (fun _ => 0) := by
  refine ⟨?_, isClosed_Icc.prod isClosed_Icc, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro x _hx y _hy
    dsimp [V, AdaptiveFoldTransverseRidge.profile]
    nlinarith
  · norm_num [M, leftBox]
  · norm_num [V, M, S]
  · intro p hp
    have hc := polynomial_ceiling p.1 hp.1.2
    dsimp [V, M]
    nlinarith [sq_nonneg p.2]
  · intro p hp
    obtain ⟨hpD,hside⟩ := frontier_leftBox_sides hp
    have hc := polynomial_ceiling p.1 hpD.1.2
    rcases hside with hleft | hright | hbottom | htop
    · dsimp [V, S]
      rw [hleft]
      nlinarith [sq_nonneg p.2]
    · dsimp [V, S]
      rw [hright]
      nlinarith [sq_nonneg p.2]
    · dsimp [V, S]
      rw [hbottom]
      nlinarith
    · dsimp [V, S]
      rw [htop]
      nlinarith
  · norm_num [V, M, olderPoint]
  · let γ := ridgePath (z := fun _ : ℝ => (0:ℝ)) (U := univ)
      isOpen_univ (subset_univ _) contDiffOn_const rfl
    refine ⟨γ, fun _ => rfl, ?_, ?_⟩
    · intro t
      change V S ≤ V (pathX t,0)
      have hf := polynomial_floor (pathX t) (pathX_mem t).1
      norm_num [V, S] at *
      exact hf
    · change (pathX pathMidpoint, (0:ℝ)) = S
      norm_num [pathX, pathMidpoint, S]

/-- Literal old C263 death and clearance of the physical cubic, not a supplied
certificate renamed as the result. -/
theorem polynomial_physical_death :
    superlevelBar_deathHeight G Mphys = 2 ∧
      superlevelBar_clearanceSet G Mphys = Iio 2 := by
  have hpull : ∀ p, G (physicalChart 1 (by norm_num) p) = 6 * V p := by
    intro p
    unfold G
    rw [physicalChart_apply, ContinuousLinearEquiv.apply_symm_apply]
    simp
  apply scaled_rectangle_death G (by unfold G V; fun_prop) V
    1 6 3 2 1 2 (fun _ => 0) (by norm_num) (by norm_num) hpull
  · rw [hpull]
    norm_num [V, M]
  · rw [hpull]
    norm_num [V, S]
  · exact polynomial_rectangle

theorem clearance_below_two : (1:ℝ) ∈ superlevelBar_clearanceSet G Mphys := by
  rw [polynomial_physical_death.2]
  norm_num

theorem clearance_at_two_excluded : (2:ℝ) ∉ superlevelBar_clearanceSet G Mphys := by
  rw [polynomial_physical_death.2]
  simp

/-- Proven scale counterexample for both the normalized saddle and gap-only
value: absolute physical death is 2, with b=3,k=r=1. -/
theorem dropped_scale_counterexample :
    superlevelBar_deathHeight G Mphys ≠ -(1/12:ℝ) ∧
      superlevelBar_deathHeight G Mphys ≠ -(1/6:ℝ) := by
  rw [polynomial_physical_death.1]
  norm_num

end ActualDeathControls
