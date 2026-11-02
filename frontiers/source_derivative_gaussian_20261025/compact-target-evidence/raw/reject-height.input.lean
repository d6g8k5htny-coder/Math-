import SourceCompactTargetMoments
open I4SourceCompactTargetMoments
open scoped Matrix
-- Deliberately false: the new target cannot discard its height component.
example : sourceGapPins (1/2) 3 1 = (![-(1:ℝ)*(1/2)^3/2,0,0,0,0,12] : Fin 6 → ℝ) := by
  norm_num [sourceGapPins, funext_iff, Fin.forall_fin_succ]
