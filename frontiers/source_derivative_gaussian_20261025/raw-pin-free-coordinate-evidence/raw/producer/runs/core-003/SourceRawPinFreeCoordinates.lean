import SourceFinitePinKernel
import SourceCurvatureDecomposition
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-! Finite raw-pin-free coordinates on the original smooth coefficient carrier.
Only the deterministic directions have finite support. -/

noncomputable section
open scoped BigOperators
set_option autoImplicit false

open MeasureTheory ProbabilityTheory I4Foundation I4Source I4Smooth I4SmoothCarrier
open I4SourceGaussian I4SourceCovariance I4SourceSmoothConditional
open I4SourceCurvatureDecomposition I4SourceFinitePinKernel I4SourceRawPinConditioning

namespace I4SourceRawPinFreeCoordinates

/-- A finite orthonormal family in the literal six-row raw pin kernel. -/
structure RawPinFreeFrame (L r : ℝ) (n : ℕ) where
  chi : Fin n → (SourceMode 2 →₀ ℝ)
  gram : ∀ j k : Fin n,
    finitePairing (fun m => chi j m) (chi k) = if j = k then 1 else 0
  raw_kernel : ∀ (i : Fin 6) (j : Fin n),
    finitePairing (rawPinCoefficient L r i) (chi j) = 0

private def freeLift {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) : SourceMode 2 →₀ ℝ := ∑ j, z j • F.chi j

/-- All finite original-coefficient coordinates of the supplied frame. -/
def freeCoordinate {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (ω : SmoothSample 2 L) : Fin n → ℝ := fun j => finitePairing ω.val (F.chi j)

/-- Add the entire finite frame lift to the literal smooth sample. -/
def freeShiftSample {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  finiteShiftSample (freeLift F z) ω

/-- Subtract the full finite orthogonal projection, on the original carrier. -/
def freeResidualSample {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  freeShiftSample F (-freeCoordinate F ω) ω

private theorem freeLift_apply {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (z : Fin n → ℝ) (m : SourceMode 2) :
    freeLift F z m = ∑ j, z j * F.chi j m := by
  classical
  simp [freeLift]

private theorem freeShiftSample_val {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (ω : SmoothSample 2 L)
    (m : SourceMode 2) :
    (freeShiftSample F z ω).val m = ω.val m + ∑ j, z j * F.chi j m := by
  rw [freeShiftSample, finiteShiftSample_val, freeLift_apply]

private theorem freeResidualSample_val {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (freeResidualSample F ω).val m =
      ω.val m - ∑ j, F.chi j m * freeCoordinate F ω j := by
  simp only [freeResidualSample, freeShiftSample_val, Pi.neg_apply, neg_mul,
    Finset.sum_neg_distrib, mul_comm]
  rfl

private theorem finitePairing_eq_tsum {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing a v = ∑' m, a m * v m := by
  classical
  symm
  apply HasSum.tsum_eq
  apply hasSum_sum_of_ne_finset_zero
  intro m hm
  simp [Finsupp.notMem_support_iff.mp hm]

private theorem chi_summable {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n)
    (j : Fin n) : Summable (fun m => F.chi j m) := by
  classical
  apply summable_of_ne_finset_zero (s := (F.chi j).support)
  intro m hm
  exact Finsupp.notMem_support_iff.mp hm

private theorem chi_normSquared {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (j : Fin n) : ∑' m, (F.chi j m) ^ 2 = 1 := by
  have h := F.gram j j
  rw [finitePairing_eq_tsum] at h
  simpa [pow_two] using h

private theorem freeCoordinate_eq_unitDirection {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (j : Fin n) :
    (fun ω => freeCoordinate F ω j) = unitDirection (fun m => F.chi j m) := by
  funext ω
  simp only [freeCoordinate, finitePairing_eq_tsum, unitDirection, scalarSeries, mul_comm]

/-- The coordinate vector, joint finite shift, and full residual are measurable. -/
set_option maxHeartbeats 1000000 in
theorem freeMaps_measurable {L r : ℝ} {n : ℕ} (F : RawPinFreeFrame L r n) :
    Measurable (freeCoordinate F) ∧
    Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L => freeShiftSample F p.1 p.2) ∧
    Measurable (freeResidualSample F) := by
  have hZ : Measurable (freeCoordinate F) := by
    apply Measurable.of_eval
    intro j
    rw [freeCoordinate_eq_unitDirection]
    exact unitDirection_measurable _
  have hS : Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L =>
      freeShiftSample F p.1 p.2) := by
    apply Measurable.subtype_mk
    apply Measurable.of_eval
    intro m
    change Measurable (fun p : (Fin n → ℝ) × SmoothSample 2 L =>
      p.2.val m + freeLift F p.1 m)
    simp_rw [freeLift_apply]
    exact ((measurable_pi_apply m).comp (measurable_subtype_coe.comp measurable_snd)).add
      (Finset.measurable_sum _ (fun j _ =>
        ((measurable_pi_apply j).comp measurable_fst).mul_const _))
  exact ⟨hZ, hS, hS.comp (hZ.neg.prodMk measurable_id)⟩

private theorem finitePairing_eq_linearCombination {ι : Type*}
    (a : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing a v = Finsupp.linearCombination ℝ a v := by
  simp only [finitePairing, Finsupp.linearCombination_apply, smul_eq_mul, mul_comm]

private theorem freeLift_raw_kernel {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (z : Fin n → ℝ) (i : Fin 6) :
    finitePairing (rawPinCoefficient L r i) (freeLift F z) = 0 := by
  classical
  simp only [finitePairing_eq_linearCombination, freeLift, map_sum, map_smul]
  simp_rw [← finitePairing_eq_linearCombination, F.raw_kernel]
  simp

private theorem free_reconstruction {L r : ℝ} {n : ℕ}
    (F : RawPinFreeFrame L r n) (ω : SmoothSample 2 L) :
    freeShiftSample F (freeCoordinate F ω) (freeResidualSample F ω) = ω := by
  apply Subtype.ext
  funext m
  rw [freeShiftSample_val, freeResidualSample_val]
  simp only [mul_comm (freeCoordinate F ω _)]
  ring

/-- Every full raw target posterior retains the complete finite free lift,
including at singular radii. -/
theorem rawPosteriorSample_free_reconstruction {L r : ℝ} {n : ℕ}
    (hL : L ≠ 0) (F : RawPinFreeFrame L r n) (t : Fin 6 → ℝ)
    (ω : SmoothSample 2 L) :
    rawPosteriorSample hL r t ω = freeShiftSample F (freeCoordinate F ω)
      (rawPosteriorSample hL r t (freeResidualSample F ω)) := by
  conv_lhs => rw [← free_reconstruction F ω]
  exact rawPosteriorSample_finiteShiftSample hL r t (freeLift F (freeCoordinate F ω))
    (freeLift_raw_kernel F _) (freeResidualSample F ω)

end I4SourceRawPinFreeCoordinates
