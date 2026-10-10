import TaylorSymLift
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Basis.SMul

noncomputable section
open scoped ContDiff Matrix.Norms.Frobenius
open TaylorMatrix Matrix
namespace PhysicalSpectral

def hessian {n : ℕ} {L : ℝ} (omega : I4Source.SourceMode n → ℝ)
    (x0 : X n) : Matrix (Fin n) (Fin n) ℝ := fun i j =>
  iteratedFDeriv ℝ 2 (I4Source.sourceField n L omega) x0
    ![Pi.single i 1, Pi.single j 1]

theorem hessian_hermitian {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) : (hessian (L := L) omega x0).IsHermitian := by
  have hf := I4DeterministicC4.sourceField_contDiff_of_majorant n hL omega hmajor
  change (hessian (L := L) omega x0).conjTranspose = _
  ext i j
  simp only [Matrix.conjTranspose_apply, star_trivial, hessian]
  exact (hf.contDiffAt.isSymmSndFDerivAt (by norm_num)).iteratedFDeriv_cons

theorem eigenvalues_ne_zero {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (hdet : H.det ≠ 0) (i : Fin n) : hH.eigenvalues i ≠ 0 := by
  rw [hH.det_eq_prod_eigenvalues] at hdet
  exact (Finset.prod_ne_zero_iff.mp hdet) i (Finset.mem_univ i)

def scale (a : ℝ) : ℝ := Real.sqrt (2 / |a|)

theorem scale_pos {a : ℝ} (ha : a ≠ 0) : 0 < scale a := by
  exact Real.sqrt_pos.2 (div_pos (by norm_num) (abs_pos.2 ha))

theorem scale_square {a : ℝ} (ha : a ≠ 0) : scale a * scale a = 2 / |a| := by
  exact Real.mul_self_sqrt (le_of_lt (div_pos (by norm_num) (abs_pos.2 ha)))

theorem scale_normalizes {a : ℝ} (ha : a ≠ 0) :
    scale a * a * scale a = if 0 < a then 2 else -2 := by
  have hs := scale_square ha
  by_cases hp : 0 < a
  · rw [ite_eq_left hp]
    rw [abs_of_pos hp] at hs
    calc
      scale a * a * scale a = (scale a * scale a) * a := by ring
      _ = 2 := by rw [hs]; field_simp
  · rw [ite_eq_right hp]
    have hn : a < 0 := lt_of_le_of_ne (le_of_not_gt hp) ha
    rw [abs_of_neg hn] at hs
    calc
      scale a * a * scale a = (scale a * scale a) * a := by ring
      _ = -2 := by rw [hs]; field_simp

theorem bilinear_coordinates {n : ℕ} (B : X n →L[ℝ] X n →L[ℝ] ℝ) (x y : X n) :
    B x y = dotProduct x ((fun i j => B (Pi.single i 1) (Pi.single j 1)) *ᵥ y) := by
  have hx : x = ∑ i, x i • Pi.single i (1 : ℝ) := by
    ext k
    simp [Finset.sum_apply, Pi.single_apply]
  have hy : y = ∑ i, y i • Pi.single i (1 : ℝ) := by
    ext k
    simp [Finset.sum_apply, Pi.single_apply]
  conv_lhs => rw [hx, hy]
  simp only [map_sum, map_smul, _root_.sum_apply, _root_.smul_apply, smul_eq_mul,
    dotProduct, Matrix.mulVec, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

theorem source_hessian_coordinates {n : ℕ} {L : ℝ}
    (omega : I4Source.SourceMode n → ℝ) (x0 x y : X n) :
    iteratedFDeriv ℝ 2 (I4Source.sourceField n L omega) x0 ![x,y] =
      dotProduct x (hessian (L := L) omega x0 *ᵥ y) := by
  unfold hessian
  simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  exact bilinear_coordinates (fderiv ℝ (fderiv ℝ (I4Source.sourceField n L omega)) x0) x y

def frameBasis {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (hdet : H.det ≠ 0) (e : Fin n ≃ Fin n) :
    Module.Basis (Fin n) ℝ (X n) :=
  ((hH.eigenvectorBasis.reindex e).toBasis.map
    (EuclideanSpace.equiv (Fin n) ℝ).toLinearEquiv).unitsSMul
      (fun i => Units.mk0 (scale (hH.eigenvalues (e.symm i)))
        (ne_of_gt (scale_pos (eigenvalues_ne_zero hH hdet (e.symm i)))))

def frame {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (hdet : H.det ≠ 0) (e : Fin n ≃ Fin n) : E n ≃L[ℝ] X n :=
  (EuclideanSpace.equiv (Fin n) ℝ).trans (frameBasis hH hdet e).equivFunL.symm

theorem frame_single {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (hdet : H.det ≠ 0) (e : Fin n ≃ Fin n) (i : Fin n) :
    frame hH hdet e (EuclideanSpace.single i 1) =
      scale (hH.eigenvalues (e.symm i)) • ⇑(hH.eigenvectorBasis (e.symm i)) := by
  have hh : frame hH hdet e (EuclideanSpace.single i 1) = frameBasis hH hdet e i := by
    change (frameBasis hH hdet e).equivFun.symm (Pi.single i (1 : ℝ)) = _
    rw [Module.Basis.equivFun_symm_apply]
    simp [Pi.single_apply]
  rw [hh]
  simp only [frameBasis, Module.Basis.unitsSMul_apply, Units.smul_def,
    Module.Basis.map_apply, OrthonormalBasis.coe_toBasis, OrthonormalBasis.reindex_apply]
  rfl

theorem eigen_dot {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (i j : Fin n) :
    dotProduct ⇑(hH.eigenvectorBasis i) ⇑(hH.eigenvectorBasis j) =
      if i = j then 1 else 0 := by
  simpa only [EuclideanSpace.inner_eq_star_dotProduct, star_trivial, dotProduct_comm]
    using hH.eigenvectorBasis.inner_eq_ite i j

theorem frame_normalizes {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (hdet : H.det ≠ 0) (e : Fin n ≃ Fin n) (i j : Fin n) :
    dotProduct (frame hH hdet e (EuclideanSpace.single i 1))
      (H *ᵥ frame hH hdet e (EuclideanSpace.single j 1)) =
      if i = j then (if 0 < hH.eigenvalues (e.symm i) then 2 else -2) else 0 := by
  rw [frame_single, frame_single, Matrix.mulVec_smul, hH.mulVec_eigenvectorBasis]
  simp only [smul_dotProduct, dotProduct_smul, smul_eq_mul, eigen_dot]
  by_cases hij : i = j
  · subst j
    simpa [mul_assoc] using scale_normalizes (eigenvalues_ne_zero hH hdet (e.symm i))
  · have hh : e.symm i ≠ e.symm j := fun h => hij (e.symm.injective h)
    simp [hij, hh]

theorem positive_reorder {n : ℕ} (lam : Fin n → ℝ) :
    ∃ k : ℕ, k ≤ n ∧ ∃ e : Fin n ≃ Fin n, ∀ i : Fin n,
      0 < lam (e.symm i) ↔ i.val < k := by
  classical
  let Pos := {i : Fin n // 0 < lam i}
  let Neg := {i : Fin n // ¬ 0 < lam i}
  let p := Fintype.card Pos
  let q := Fintype.card Neg
  have hcard : p + q = n := by
    simpa only [Fintype.card_sum, Fintype.card_fin] using
      (Fintype.card_congr (Equiv.sumCompl (fun i : Fin n => 0 < lam i)))
  let e₀ : Fin n ≃ Fin (p + q) :=
    (Equiv.sumCompl (fun i : Fin n => 0 < lam i)).symm.trans
      (((Fintype.equivFin Pos).sumCongr (Fintype.equivFin Neg)).trans finSumFinEquiv)
  let e : Fin n ≃ Fin n := e₀.trans (finCongr hcard)
  have he (j : Fin n) : 0 < lam j ↔ (e j).val < p := by
    simp_rw [e, e₀, Equiv.trans_apply, Equiv.sumCongr_apply,
      finCongr_apply, Fin.val_cast]
    by_cases hj : 0 < lam j <;> simp [hj, p]
  refine ⟨p, by omega, e, ?_⟩
  intro i
  simpa only [Equiv.apply_symm_apply] using he (e.symm i)

theorem source_normalization {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (hessian (L := L) omega x0).det ≠ 0) :
    ∃ k : ℕ, k ≤ n ∧ ∃ P : E n ≃L[ℝ] X n, ∀ i j : Fin n,
      iteratedFDeriv ℝ 2 (I4Source.sourceField n L omega) x0
        ![P (EuclideanSpace.single i 1), P (EuclideanSpace.single j 1)] =
      if i = j then (if i.val < k then 2 else -2) else 0 := by
  have hH := hessian_hermitian hL omega hmajor x0
  obtain ⟨k, hk, e, he⟩ := positive_reorder hH.eigenvalues
  refine ⟨k, hk, frame hH hdet e, ?_⟩
  intro i j
  rw [source_hessian_coordinates, frame_normalizes]
  simp only [he]

/-- Positive coordinates precede negative coordinates; there are no zero entries. -/
def signMatrix (n k : ℕ) : MorseCongruence.Mat n :=
  Matrix.diagonal (fun i : Fin n => if i.val < k then (1 : ℝ) else -1)

theorem signMatrix_selfAdjoint (n k : ℕ) : IsSelfAdjoint (signMatrix n k) := by
  change star (signMatrix n k) = _
  ext i j
  by_cases hij : i = j
  · subst j; simp [signMatrix, Matrix.star_apply]
  · simp [signMatrix, Matrix.star_apply, hij, Ne.symm hij]

theorem signMatrix_involution (n k : ℕ) : signMatrix n k * signMatrix n k = 1 := by
  rw [signMatrix, Matrix.diagonal_mul_diagonal]
  have hd : (fun i : Fin n => (if i.val < k then (1 : ℝ) else -1) *
      (if i.val < k then (1 : ℝ) else -1)) = fun _ => 1 := by
    funext i
    split_ifs <;> norm_num
  rw [hd]
  exact Matrix.diagonal_one

def signSym (n k : ℕ) : MorseCongruence.Sym n :=
  ⟨signMatrix n k, signMatrix_selfAdjoint n k⟩

theorem matrix_normalization {n : ℕ} {H : Matrix (Fin n) (Fin n) ℝ}
    (hH : H.IsHermitian) (hdet : H.det ≠ 0) :
    ∃ k : ℕ, k ≤ n ∧ ∃ P : E n ≃L[ℝ] X n, ∀ i j : Fin n,
      dotProduct (P (EuclideanSpace.single i 1)) (H *ᵥ P (EuclideanSpace.single j 1)) =
        2 * signMatrix n k i j := by
  obtain ⟨k, hk, e, he⟩ := positive_reorder hH.eigenvalues
  refine ⟨k, hk, frame hH hdet e, ?_⟩
  intro i j
  rw [frame_normalizes]
  simp only [he, signMatrix, Matrix.diagonal_apply]
  split_ifs <;> norm_num

/-- The actual source Taylor matrix has center J, not 2J or J/2. -/
theorem source_taylor_center {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (hessian (L := L) omega x0).det ≠ 0) :
    ∃ k : ℕ, k ≤ n ∧ ∃ P : E n ≃L[ℝ] X n,
      TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap 0 = signSym n k := by
  obtain ⟨k, hk, P, hP⟩ := matrix_normalization (hessian_hermitian hL omega hmajor x0) hdet
  refine ⟨k, hk, P, ?_⟩
  apply Subtype.ext
  ext i j
  rw [TaylorSymLift.sourceSymMatrix_zero hL omega hmajor]
  rw [source_hessian_coordinates]
  change (1 / 2 : ℝ) * (dotProduct (P (EuclideanSpace.single i 1))
    (hessian (L := L) omega x0 *ᵥ P (EuclideanSpace.single j 1))) = signMatrix n k i j
  rw [hP]
  ring

/-- One and the same source, point, frame and positive-first sign matrix feed the
literal directional Hessian and the C2 symmetric Taylor matrix. No chart is assumed. -/
theorem source_normalization_bundle {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (hessian (L := L) omega x0).det ≠ 0) :
    ∃ k : ℕ, k ≤ n ∧ ∃ P : E n ≃L[ℝ] X n,
      signMatrix n k * signMatrix n k = 1 ∧
      (∀ i j : Fin n, iteratedFDeriv ℝ 2 (I4Source.sourceField n L omega) x0
        ![P (EuclideanSpace.single i 1), P (EuclideanSpace.single j 1)] =
          2 * signMatrix n k i j) ∧
      TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap 0 = signSym n k ∧
      ContDiff ℝ 2 (TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap) := by
  obtain ⟨k, hk, P, hP⟩ := matrix_normalization (hessian_hermitian hL omega hmajor x0) hdet
  refine ⟨k, hk, P, signMatrix_involution n k, ?_, ?_, ?_⟩
  · intro i j
    rw [source_hessian_coordinates]
    exact hP i j
  · apply Subtype.ext
    ext i j
    rw [TaylorSymLift.sourceSymMatrix_zero hL omega hmajor, source_hessian_coordinates]
    change (1 / 2 : ℝ) * (dotProduct (P (EuclideanSpace.single i 1))
      (hessian (L := L) omega x0 *ᵥ P (EuclideanSpace.single j 1))) = signMatrix n k i j
    rw [hP]
    ring
  · exact TaylorSymLift.sourceSymMatrix_contDiff hL omega hmajor x0 P.toContinuousLinearMap

end PhysicalSpectral
