/-- The literal Lifetime Euclidean lift of the unchanged source maximum pin. -/
def endpointLiftM (r : ℝ) : E 2 :=
  (I4LifetimeField.coordinates 2).symm (I4SourceConfluentPins.endpointM r)

/-- The literal Lifetime Euclidean lift of the unchanged source saddle pin. -/
def endpointLiftS (r : ℝ) : E 2 :=
  (I4LifetimeField.coordinates 2).symm (I4SourceConfluentPins.endpointS r)

@[simp] theorem coordinates_endpointLiftM (r : ℝ) :
    I4LifetimeField.coordinates 2 (endpointLiftM r) =
      I4SourceConfluentPins.endpointM r := by
  simp [endpointLiftM]

@[simp] theorem coordinates_endpointLiftS (r : ℝ) :
    I4LifetimeField.coordinates 2 (endpointLiftS r) =
      I4SourceConfluentPins.endpointS r := by
  simp [endpointLiftS]

/-- The real-cover maximum lift projects to exactly the existing product-torus pin. -/
@[simp] theorem torusProjection_endpointLiftM (L r : ℝ) :
    I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 (endpointLiftM r)) =
      I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointM r) := by
  rw [coordinates_endpointLiftM]

/-- The real-cover saddle lift projects to exactly the existing product-torus pin. -/
@[simp] theorem torusProjection_endpointLiftS (L r : ℝ) :
    I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 (endpointLiftS r)) =
      I4Torus.torusProjection 2 L (I4SourceConfluentPins.endpointS r) := by
  rw [coordinates_endpointLiftS]

@[simp] theorem endpointLiftM_apply (r : ℝ) (i : Fin 2) :
    endpointLiftM r i = I4SourceConfluentPins.endpointM r i := by
  change (I4LifetimeField.coordinates 2 (endpointLiftM r)) i = _
  rw [coordinates_endpointLiftM]

@[simp] theorem endpointLiftS_apply (r : ℝ) (i : Fin 2) :
    endpointLiftS r i = I4SourceConfluentPins.endpointS r i := by
  change (I4LifetimeField.coordinates 2 (endpointLiftS r)) i = _
  rw [coordinates_endpointLiftS]

/-- Parent-norm length for the unshifted Euclidean pin difference. -/
theorem endpoint_lifts_sub_norm {r : ℝ} (hr : 0 ≤ r) :
    ‖endpointLiftM r - endpointLiftS r‖ = r := by
  have heq : endpointLiftM r - endpointLiftS r =
      EuclideanSpace.single (0 : Fin 2) (-r) := by
    ext i
    fin_cases i <;>
      simp [I4SourceConfluentPins.endpointM, I4SourceConfluentPins.endpointS]; ring
  rw [heq, PiLp.norm_single, Real.norm_eq_abs, abs_neg, abs_of_nonneg hr]

/-- Every actual parent lattice shift has length at least the pin distance.
Only the zeroth Euclidean component is needed. -/
theorem endpoint_lifts_lattice_lower {L r : ℝ} (hL : 0 < L)
    (hrL : r < L / 2) (n : Fin 2 → ℤ) :
    r ≤ ‖endpointLiftM r - endpointLiftS r + latticeVec 2 L n‖ := by
  have hcoord : (endpointLiftM r - endpointLiftS r + latticeVec 2 L n) 0 =
      -r + L * (n 0 : ℝ) := by
    have hl := congrFun (I4LifetimeField.coordinates_latticeVec 2 L n) 0
    simp only [I4LifetimeField.coordinates_apply] at hl
    simp [I4SourceConfluentPins.endpointM, I4SourceConfluentPins.endpointS, hl]
    ring
  have habs : r ≤ |-r + L * (n 0 : ℝ)| := by
    by_cases hn : n 0 ≤ 0
    · have hnR : (n 0 : ℝ) ≤ 0 := by exact_mod_cast hn
      have hm : L * (n 0 : ℝ) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hL.le hnR
      exact (le_abs).2 (Or.inr (by linarith))
    · have hn1 : 1 ≤ n 0 := by omega
      have hnR : (1 : ℝ) ≤ (n 0 : ℝ) := by exact_mod_cast hn1
      have hm : L ≤ L * (n 0 : ℝ) := by nlinarith
      exact (le_abs).2 (Or.inl (by linarith))
  calc
    r ≤ |-r + L * (n 0 : ℝ)| := habs
    _ = ‖(endpointLiftM r - endpointLiftS r + latticeVec 2 L n) 0‖ := by
      rw [hcoord, Real.norm_eq_abs]
    _ ≤ ‖endpointLiftM r - endpointLiftS r + latticeVec 2 L n‖ :=
      PiLp.norm_apply_le _ _

/-- Literal Lifetime lattice-infimum distance, without a quotient-carrier comparison. -/
theorem endpoint_lifts_torusDist {L r : ℝ} (hL : 0 < L)
    (hr : 0 < r) (hrL : r < L / 2) :
    torusDist 2 L (endpointLiftM r) (endpointLiftS r) = r := by
  apply le_antisymm
  · have hb : BddBelow (Set.range (fun n : Fin 2 → ℤ =>
        ‖endpointLiftM r - endpointLiftS r + latticeVec 2 L n‖)) :=
      ⟨0, by rintro _ ⟨n, rfl⟩; exact norm_nonneg _⟩
    have hz : latticeVec 2 L (0 : Fin 2 → ℤ) = 0 := by
      ext i
      fin_cases i <;> simp [latticeVec]
    exact (ciInf_le hb (0 : Fin 2 → ℤ)).trans (by
      rw [hz, add_zero, endpoint_lifts_sub_norm hr.le])
  · exact le_ciInf (endpoint_lifts_lattice_lower hL hrL)

/-- The endpoint separation can wrap through a full parent period. -/
theorem endpoint_lifts_torusDist_unit_zero :
    torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) = 0 := by
  apply le_antisymm
  · have hb : BddBelow (Set.range (fun n : Fin 2 → ℤ =>
        ‖endpointLiftM 1 - endpointLiftS 1 + latticeVec 2 1 n‖)) :=
      ⟨0, by rintro _ ⟨n, rfl⟩; exact norm_nonneg _⟩
    have hz : endpointLiftM 1 - endpointLiftS 1 +
        latticeVec 2 1 (![1, 0] : Fin 2 → ℤ) = 0 := by
      ext i
      fin_cases i <;>
        norm_num [I4SourceConfluentPins.endpointM, I4SourceConfluentPins.endpointS,
          latticeVec, PiLp.single_apply]
    exact (ciInf_le hb (![1, 0] : Fin 2 → ℤ)).trans (by rw [hz, norm_zero])
  · exact le_ciInf (fun _ => norm_nonneg _)

/-- Concrete witness that deleting the small-radius bound makes the distance claim false. -/
theorem endpoint_lifts_torusDist_unit_ne_radius :
    torusDist 2 1 (endpointLiftM 1) (endpointLiftS 1) ≠ 1 := by
  rw [endpoint_lifts_torusDist_unit_zero]
  norm_num
