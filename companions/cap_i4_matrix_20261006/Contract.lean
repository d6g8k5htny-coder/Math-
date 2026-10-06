import CapI4Matrix
open scoped Matrix
open MeasureTheory Set
example (e : ℝ × (ℝ × ℝ)) :
    (CapI4Matrix.entryMatrix e).IsHermitian :=
  CapI4Matrix.entryMatrix_isHermitian e
example (e : ℝ × (ℝ × ℝ)) :
    (CapI4Matrix.entryMatrix e).det = e.1 * e.2.2 - e.2.1 ^ 2 :=
  CapI4Matrix.entryMatrix_det e
example (e : ℝ × (ℝ × ℝ)) :
    (CapI4Matrix.entryMatrix e).trace = e.1 + e.2.2 :=
  CapI4Matrix.entryMatrix_trace e
example (e : ℝ × (ℝ × ℝ)) (v : Fin 2 → ℝ) :
    star v ⬝ᵥ (CapI4Matrix.entryMatrix e *ᵥ v) =
      e.1 * v 0 ^ 2 + 2 * e.2.1 * v 0 * v 1 + e.2.2 * v 1 ^ 2 :=
  CapI4Matrix.entryMatrix_quadratic e v
example (e : ℝ × (ℝ × ℝ)) :
    (CapI4Matrix.entryMatrix e).PosDef ↔
      0 < e.1 ∧ 0 < e.1 * e.2.2 - e.2.1 ^ 2 :=
  CapI4Matrix.entryMatrix_posDef_iff e
example (e : ℝ × (ℝ × ℝ)) :
    (CapI4Matrix.entryMatrix e).PosDef ↔
      0 < (CapI4Polar.eigenvalues e).1 :=
  CapI4Matrix.entryMatrix_posDef_iff_first_pos e
example : MeasurableSet {e : ℝ × (ℝ × ℝ) | (CapI4Matrix.entryMatrix e).PosDef} :=
  CapI4Matrix.entryMatrix_posDef_measurableSet
example (e : ℝ × (ℝ × ℝ)) (s : ℝ) :
    (algebraMap ℝ (Matrix (Fin 2) (Fin 2) ℝ) s - CapI4Matrix.entryMatrix e).det =
      (s - (CapI4Polar.eigenvalues e).1) * (s - (CapI4Polar.eigenvalues e).2) :=
  CapI4Matrix.entryMatrix_char_det e s
example (e : ℝ × (ℝ × ℝ)) (s : ℝ) :
    s ∈ spectrum ℝ (CapI4Matrix.entryMatrix e) ↔
      s = (CapI4Polar.eigenvalues e).1 ∨ s = (CapI4Polar.eigenvalues e).2 :=
  CapI4Matrix.entryMatrix_mem_spectrum_iff e s
example (e : ℝ × (ℝ × ℝ)) :
    spectrum ℝ (CapI4Matrix.entryMatrix e) =
      {(CapI4Polar.eigenvalues e).1, (CapI4Polar.eigenvalues e).2} :=
  CapI4Matrix.entryMatrix_spectrum e
example (e : ℝ × (ℝ × ℝ)) :
    (CapI4Polar.eigenvalues e).1 ^ 2 + (CapI4Polar.eigenvalues e).2 ^ 2 =
      e.1 ^ 2 + 2 * e.2.1 ^ 2 + e.2.2 ^ 2 :=
  CapI4Matrix.entryMatrix_eigenvalues_sq_sum e

example : (CapI4Matrix.entryMatrix (2, (1, 2))).PosDef := by
  rw [CapI4Matrix.entryMatrix_posDef_iff]
  norm_num
example : ¬ (CapI4Matrix.entryMatrix (0, (0, 1))).PosDef := by
  rw [CapI4Matrix.entryMatrix_posDef_iff]
  norm_num
example : ¬ (CapI4Matrix.entryMatrix (-1, (0, -1))).PosDef := by
  rw [CapI4Matrix.entryMatrix_posDef_iff]
  norm_num
example : spectrum ℝ (CapI4Matrix.entryMatrix (1, (0, 1))) = {1} := by
  rw [CapI4Matrix.entryMatrix_spectrum]
  norm_num [CapI4Polar.eigenvalues, CapI4Polar.traceCoordinates,
    CapI4Polar.spectrum, CapI4Polar.radius]
