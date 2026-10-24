import TaylorMatrix

noncomputable section
open scoped ContDiff Matrix.Norms.Frobenius
open TaylorMatrix

namespace TaylorSymLift

def sourceSymMatrix {n : ℕ} {L : ℝ} (omega : I4Source.SourceMode n → ℝ)
    (x0 : X n) (P : E n →L[ℝ] X n) (u : E n) : MorseCongruence.Sym n :=
  MorseCongruence.project n (matrix (I4Source.sourceField n L omega) x0 P u)

theorem sourceSymMatrix_coe {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n) (u : E n) :
    (sourceSymMatrix (L := L) omega x0 P u : MorseCongruence.Mat n) =
      matrix (I4Source.sourceField n L omega) x0 P u := by
  exact (source_matrix_selfAdjoint hL omega hmajor x0 P u).coe_selfAdjointPart_apply ℝ

theorem sourceSymMatrix_contDiff {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n) :
    ContDiff ℝ 2 (sourceSymMatrix (L := L) omega x0 P) := by
  exact (MorseCongruence.project n).contDiff.comp
    (source_matrix_contDiff hL omega hmajor x0 P)

theorem sourceSymMatrix_zero {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n) (i j : Fin n) :
    (sourceSymMatrix (L := L) omega x0 P 0 : MorseCongruence.Mat n) i j =
      (1/2 : ℝ) * iteratedFDeriv ℝ 2 (I4Source.sourceField n L omega) x0
        ![P (EuclideanSpace.single i 1), P (EuclideanSpace.single j 1)] := by
  rw [sourceSymMatrix_coe hL omega hmajor x0 P 0]
  exact source_matrix_zero hL omega hmajor x0 P i j

theorem sourceSymMatrix_quadratic {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (P : E n →L[ℝ] X n)
    (hcrit : fderiv ℝ (I4Source.sourceField n L omega) x0 = 0) (u : E n) :
    I4Source.sourceField n L omega (x0+P u) = I4Source.sourceField n L omega x0 +
      ∑ i, ∑ j, u i * (sourceSymMatrix (L := L) omega x0 P u : MorseCongruence.Mat n) i j * u j := by
  rw [sourceSymMatrix_coe hL omega hmajor x0 P u]
  exact source_matrix_quadratic hL omega hmajor x0 P hcrit u

end TaylorSymLift
