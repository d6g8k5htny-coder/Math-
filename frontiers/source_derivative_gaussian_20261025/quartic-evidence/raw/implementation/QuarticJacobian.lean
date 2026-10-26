import SourcePinPreservingQuartic

noncomputable section

open Matrix WithLp

namespace I4SourcePinPreservingQuartic

-- Uses the actual production Jacobian definition from stage07.

theorem hasFDerivAt_pinPreservingQuartic (r q : ℝ) (U : Fin 8 → ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) :
    HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) => toLp 2 (pinPreservingQuartic r q U (ofLp z)))
      (matrixLinearEuclidean (pinPreservingJacobian r q U (ofLp z))) z := by
  let X : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ := EuclideanSpace.proj (𝕜 := ℝ) 0
  let Y : EuclideanSpace ℝ (Fin 2) →L[ℝ] ℝ := EuclideanSpace.proj (𝕜 := ℝ) 1
  let M := matrixLinearEuclidean (pinPreservingJacobian r q U (ofLp z))
  have hX := X.hasFDerivAt (x := z)
  have hY := Y.hasFDerivAt (x := z)
  have h0 := (((((hX.pow 2).sub_const (1/4 : ℝ)).add
      ((hX.const_mul (U 0)).mul hY)).add ((hY.pow 2).const_mul (U 1/2))).add
      ((((((hX.const_mul (U 3/6)).mul ((hX.pow 2).sub_const (1/4 : ℝ))).add
        ((((hX.pow 2).const_mul 3).sub_const (1/4 : ℝ)).const_mul (U 4/6) |>.mul hY)).add
        ((hX.const_mul (U 5/2)).mul (hY.pow 2))).add
        ((hY.pow 3).const_mul (U 6/6))).const_mul r))
  have h1 := (((((hY.const_mul (q/r)).add
      (((hX.pow 2).sub_const (1/4 : ℝ)).const_mul (U 0/2))).add
      ((hX.const_mul (U 1)).mul hY)).add ((hY.pow 2).const_mul (U 2/2))).add
      ((((((hX.const_mul (U 4/6)).mul ((hX.pow 2).sub_const (1/4 : ℝ))).add
        (((hX.pow 2).const_mul (U 5/2)).mul hY)).add
        ((hX.const_mul (U 6/2)).mul (hY.pow 2))).add
        ((hY.pow 3).const_mul (U 7/6))).const_mul r))
  have hp0 : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) =>
      pinPreservingQuartic r q U (ofLp z) 0) (X.comp M) z := by
    apply h0.congr_fderiv
    ext v
    simp [X,Y,M,pinPreservingJacobian,matrixLinearEuclidean,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two]
    ring
  have hp1 : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) =>
      pinPreservingQuartic r q U (ofLp z) 1) (Y.comp M) z := by
    apply h1.congr_fderiv
    ext v
    simp [X,Y,M,pinPreservingJacobian,matrixLinearEuclidean,
      Matrix.mulVec,dotProduct,Fin.sum_univ_two]
    ring
  have hraw : HasFDerivAt (fun z : EuclideanSpace ℝ (Fin 2) =>
      pinPreservingQuartic r q U (ofLp z))
      (ContinuousLinearMap.pi (fun i : Fin 2 => (EuclideanSpace.proj (𝕜 := ℝ) i).comp M)) z := by
    apply hasFDerivAt_pi.mpr
    intro i
    fin_cases i
    · exact hp0
    · exact hp1
  have hE := piToEuclidean.hasFDerivAt.comp z hraw
  have hmap : M = piToEuclidean.comp (ContinuousLinearMap.pi
      (fun i : Fin 2 => (EuclideanSpace.proj (𝕜 := ℝ) i).comp M)) := by
    ext v i
    rfl
  change HasFDerivAt _ M z
  rw [hmap]
  exact hE

theorem fderiv_pinPreservingQuartic (r q : ℝ) (U : Fin 8 → ℝ)
    (z : EuclideanSpace ℝ (Fin 2)) :
    fderiv ℝ (fun z : EuclideanSpace ℝ (Fin 2) => toLp 2 (pinPreservingQuartic r q U (ofLp z))) z =
      matrixLinearEuclidean (pinPreservingJacobian r q U (ofLp z)) :=
  (hasFDerivAt_pinPreservingQuartic r q U z).fderiv

end I4SourcePinPreservingQuartic
