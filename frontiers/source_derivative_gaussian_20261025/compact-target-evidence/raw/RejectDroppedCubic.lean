import SourceCompactTargetMoments
open I4SourceCompactTargetMoments I4SourceConfluentPins
open scoped Matrix
-- Deliberately false: raw drop k cannot replace the actual drop k*r^3.
example : confluentTransform (1/2) (![3,3-(1:ℝ),0,0,0,0] : Fin 6 → ℝ) =
    sourceGapPins (1/2) 3 1 := by
  norm_num [confluentTransform, sourceGapPins, funext_iff, Fin.forall_fin_succ]
