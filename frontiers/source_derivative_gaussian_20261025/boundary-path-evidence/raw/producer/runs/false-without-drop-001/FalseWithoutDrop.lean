import AdaptiveFoldBoundaryPath

open Set AdaptiveFoldBoundaryPath
namespace BoundaryPathOmittedDropMutation

def lowdrop (p : ℝ × ℝ) : ℝ := p.1^3/3-p.1/4-p.2^2/100

-- The complete structural and analytic qualification for this exact polynomial
-- is the passing controls-004 receipt; that unchanged result is reused here.
-- This literal point lies on the top side. The putative universal frontier
-- conclusion with only the drop budget deleted would require the final example.
theorem point_on_frontier : (-(1/2:ℝ),1) ∈ frontier (leftBox 1) := by
  rw [leftBox, frontier_prod_eq, closure_Icc, closure_Icc,
    frontier_Icc (by norm_num : -(1:ℝ) ≤ 1),
    frontier_Icc (by norm_num : -(3/2:ℝ) ≤ 1/2)]
  simp only [mem_union, mem_prod, mem_Icc, mem_insert_iff, mem_singleton_iff]
  norm_num

theorem actual_rational_violation :
    lowdrop (-(1/2:ℝ),1) = 11/150 ∧ lowdrop S = -1/12 ∧
    lowdrop (-(1/2:ℝ),1) - lowdrop S = 47/300 := by norm_num [lowdrop,S]

-- EXPECTED MATHEMATICAL REJECTION: normalization reduces this actual false
-- frontier-bound instance to the residual goal False.
example : lowdrop (-(1/2:ℝ),1) ≤ lowdrop S := by
  norm_num [lowdrop,S]

end BoundaryPathOmittedDropMutation
