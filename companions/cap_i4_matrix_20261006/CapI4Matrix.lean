import CapI4Polar
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.LinearAlgebra.Matrix.Charpoly.Eigs

/-!
Deterministic 2x2 matrix-cone identification for the Cap I4 polar coordinates.
No matrix-volume change or concrete random-field law is supplied here.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped Matrix
namespace CapI4Matrix

/-- The same independent-entry convention as the parent: e = (a,(b,d)). -/
def entryMatrix (e : ℝ × (ℝ × ℝ)) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![e.1, e.2.1; e.2.1, e.2.2]

theorem entryMatrix_isHermitian (e : ℝ × (ℝ × ℝ)) :
    (entryMatrix e).IsHermitian := by
  apply Matrix.IsHermitian.ext
  intro i j
  fin_cases i <;> fin_cases j <;> simp [entryMatrix]

theorem entryMatrix_det (e : ℝ × (ℝ × ℝ)) :
    (entryMatrix e).det = e.1 * e.2.2 - e.2.1 ^ 2 := by
  simp [entryMatrix, Matrix.det_fin_two, pow_two]

theorem entryMatrix_trace (e : ℝ × (ℝ × ℝ)) :
    (entryMatrix e).trace = e.1 + e.2.2 := by
  simp [entryMatrix, Matrix.trace, Fin.sum_univ_two]

theorem entryMatrix_quadratic (e : ℝ × (ℝ × ℝ)) (v : Fin 2 → ℝ) :
    star v ⬝ᵥ (entryMatrix e *ᵥ v) =
      e.1 * v 0 ^ 2 + 2 * e.2.1 * v 0 * v 1 + e.2.2 * v 1 ^ 2 := by
  simp [entryMatrix, Matrix.mulVec, dotProduct, Fin.sum_univ_two]
  ring

/-- Strict Sylvester criterion, proved by a multiplied quadratic completion. -/
theorem entryMatrix_posDef_iff (e : ℝ × (ℝ × ℝ)) :
    (entryMatrix e).PosDef ↔
      0 < e.1 ∧ 0 < e.1 * e.2.2 - e.2.1 ^ 2 := by
  constructor
  · intro hM
    have hu : (![(1 : ℝ), 0] : Fin 2 → ℝ) ≠ 0 := by
      intro h
      have h0 := congrFun h 0
      norm_num at h0
    have ha : 0 < e.1 := by
      simpa [entryMatrix_quadratic] using hM.dotProduct_mulVec_pos hu
    have hw : (![-e.2.1, e.1] : Fin 2 → ℝ) ≠ 0 := by
      intro h
      have h1 := congrFun h 1
      have : e.1 = 0 := by simpa using h1
      linarith
    have hq := hM.dotProduct_mulVec_pos hw
    rw [entryMatrix_quadratic] at hq
    change 0 < e.1 * (-e.2.1) ^ 2 + 2 * e.2.1 * (-e.2.1) * e.1 + e.2.2 * e.1 ^ 2 at hq
    have hid :
        e.1 * (-e.2.1) ^ 2 + 2 * e.2.1 * (-e.2.1) * e.1 + e.2.2 * e.1 ^ 2 =
          e.1 * (e.1 * e.2.2 - e.2.1 ^ 2) := by ring
    rw [hid] at hq
    exact ⟨ha, (mul_pos_iff_of_pos_left ha).mp hq⟩
  · rintro ⟨ha, hd⟩
    apply Matrix.PosDef.of_dotProduct_mulVec_pos (entryMatrix_isHermitian e)
    intro v hv
    rw [entryMatrix_quadratic]
    by_cases hy : v 1 = 0
    · have hx : v 0 ≠ 0 := by
        intro hx
        apply hv
        funext i
        fin_cases i <;> simp_all
      have hpos := mul_pos ha (sq_pos_of_ne_zero hx)
      simpa [hy] using hpos
    · have hpos := mul_pos hd (sq_pos_of_ne_zero hy)
      have hsq := sq_nonneg (e.1 * v 0 + e.2.1 * v 1)
      have hid :
          e.1 * (e.1 * v 0 ^ 2 + 2 * e.2.1 * v 0 * v 1 + e.2.2 * v 1 ^ 2) =
            (e.1 * v 0 + e.2.1 * v 1) ^ 2 +
              (e.1 * e.2.2 - e.2.1 ^ 2) * v 1 ^ 2 := by ring
      have hmul :
          0 < e.1 * (e.1 * v 0 ^ 2 + 2 * e.2.1 * v 0 * v 1 + e.2.2 * v 1 ^ 2) := by
        rw [hid]
        exact add_pos_of_nonneg_of_pos hsq hpos
      exact (mul_pos_iff_of_pos_left ha).mp hmul

/-- The source lower root is positive exactly on the actual matrix positive cone. -/
theorem entryMatrix_posDef_iff_first_pos (e : ℝ × (ℝ × ℝ)) :
    (entryMatrix e).PosDef ↔ 0 < (CapI4Polar.eigenvalues e).1 := by
  rw [entryMatrix_posDef_iff]
  have hs := CapI4Polar.eigenvalues_sum e
  have hp := CapI4Polar.eigenvalues_product e
  have ho : (CapI4Polar.eigenvalues e).1 ≤ (CapI4Polar.eigenvalues e).2 :=
    CapI4Polar.spectrum_ordered (CapI4Polar.traceCoordinates e).1
      (CapI4Polar.traceCoordinates e).2
  constructor
  · rintro ⟨ha, hd⟩
    have hdpos : 0 < e.2.2 := by
      by_contra h
      have hprod := mul_nonpos_of_nonneg_of_nonpos ha.le (le_of_not_gt h)
      nlinarith [sq_nonneg e.2.1]
    have hsum : 0 < (CapI4Polar.eigenvalues e).1 + (CapI4Polar.eigenvalues e).2 := by
      rw [hs]
      exact add_pos ha hdpos
    by_contra h
    have hlo := le_of_not_gt h
    have hhi : 0 < (CapI4Polar.eigenvalues e).2 := by linarith
    have hprod := mul_nonpos_of_nonpos_of_nonneg hlo hhi.le
    linarith
  · intro hlo
    have hhi : 0 < (CapI4Polar.eigenvalues e).2 := lt_of_lt_of_le hlo ho
    have hprod := mul_pos hlo hhi
    have hsum : 0 < e.1 + e.2.2 := by linarith
    have hd : 0 < e.1 * e.2.2 - e.2.1 ^ 2 := by linarith
    have ha : 0 < e.1 := by
      by_contra h
      have hmul := mul_nonpos_of_nonpos_of_nonneg (le_of_not_gt h) hsum.le
      nlinarith [sq_nonneg e.1, sq_nonneg e.2.1]
    exact ⟨ha, hd⟩

theorem entryMatrix_posDef_measurableSet :
    MeasurableSet {e : ℝ × (ℝ × ℝ) | (entryMatrix e).PosDef} := by
  have heq :
      {e : ℝ × (ℝ × ℝ) | (entryMatrix e).PosDef} =
        {e : ℝ × (ℝ × ℝ) | 0 < (CapI4Polar.eigenvalues e).1} := by
    ext e
    exact entryMatrix_posDef_iff_first_pos e
  rw [heq]
  exact (isOpen_lt continuous_const
    (continuous_fst.comp CapI4Polar.continuous_eigenvalues)).measurableSet

theorem entryMatrix_char_det (e : ℝ × (ℝ × ℝ)) (s : ℝ) :
    (algebraMap ℝ (Matrix (Fin 2) (Fin 2) ℝ) s - entryMatrix e).det =
      (s - (CapI4Polar.eigenvalues e).1) * (s - (CapI4Polar.eigenvalues e).2) := by
  have hs := CapI4Polar.eigenvalues_sum e
  have hp := CapI4Polar.eigenvalues_product e
  have hdet :
      (algebraMap ℝ (Matrix (Fin 2) (Fin 2) ℝ) s - entryMatrix e).det =
        (s - e.1) * (s - e.2.2) - e.2.1 ^ 2 := by
    simp [Matrix.det_fin_two, Matrix.algebraMap_eq_diagonal, Pi.algebraMap_def,
      entryMatrix, pow_two]
  rw [hdet]
  calc
    _ = s ^ 2 - s * (e.1 + e.2.2) + (e.1 * e.2.2 - e.2.1 ^ 2) := by ring
    _ = s ^ 2 - s * ((CapI4Polar.eigenvalues e).1 + (CapI4Polar.eigenvalues e).2) +
        (CapI4Polar.eigenvalues e).1 * (CapI4Polar.eigenvalues e).2 := by rw [hs, hp]
    _ = _ := by ring

theorem entryMatrix_mem_spectrum_iff (e : ℝ × (ℝ × ℝ)) (s : ℝ) :
    s ∈ spectrum ℝ (entryMatrix e) ↔
      s = (CapI4Polar.eigenvalues e).1 ∨ s = (CapI4Polar.eigenvalues e).2 := by
  simp [spectrum.mem_iff, Matrix.isUnit_iff_isUnit_det, entryMatrix_char_det,
    mul_eq_zero, sub_eq_zero]

theorem entryMatrix_spectrum (e : ℝ × (ℝ × ℝ)) :
    spectrum ℝ (entryMatrix e) =
      {(CapI4Polar.eigenvalues e).1, (CapI4Polar.eigenvalues e).2} := by
  ext s
  simpa using entryMatrix_mem_spectrum_iff e s

theorem entryMatrix_eigenvalues_sq_sum (e : ℝ × (ℝ × ℝ)) :
    (CapI4Polar.eigenvalues e).1 ^ 2 + (CapI4Polar.eigenvalues e).2 ^ 2 =
      e.1 ^ 2 + 2 * e.2.1 ^ 2 + e.2.2 ^ 2 := by
  have hs := CapI4Polar.eigenvalues_sum e
  have hp := CapI4Polar.eigenvalues_product e
  calc
    _ = ((CapI4Polar.eigenvalues e).1 + (CapI4Polar.eigenvalues e).2) ^ 2 -
        2 * ((CapI4Polar.eigenvalues e).1 * (CapI4Polar.eigenvalues e).2) := by ring
    _ = _ := by rw [hs, hp]; ring

end CapI4Matrix
