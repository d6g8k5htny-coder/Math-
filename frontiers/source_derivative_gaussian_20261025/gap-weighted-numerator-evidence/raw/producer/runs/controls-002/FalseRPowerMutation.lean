import SourceGapWeightedNumerator

/- Sole intended-negative mutation: claim r^4 <= r^5 on 0<r<=1,
then specialize r=1/2. The positive arithmetic witness refutes exactly
this step; no general asymptotic impossibility is claimed. -/
example : ((1/2:ℝ)^4 ≤ (1/2:ℝ)^5) := by
  norm_num
