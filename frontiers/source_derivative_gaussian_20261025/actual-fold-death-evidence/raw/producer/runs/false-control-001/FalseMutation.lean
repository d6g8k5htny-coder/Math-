import Controls

open TorusFiltration ActualDeathControls

/-- Deliberately drop the physical amplitude and absolute target in the cubic
control, replacing its literal physical death 2 by normalized saddle -1/12. -/
theorem false_dropped_physical_scale : False := by
  have wrong : superlevelBar_deathHeight G Mphys = -(1/12:ℝ) := by
    exact polynomial_physical_death.1
  exact dropped_scale_counterexample.1 wrong
