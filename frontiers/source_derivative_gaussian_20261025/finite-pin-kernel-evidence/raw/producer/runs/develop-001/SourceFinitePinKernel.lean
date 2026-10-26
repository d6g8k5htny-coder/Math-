import SourceRawPinConditioning
import ContactJetCovariance

/-! Finite original pin-kernel witnesses and deterministic posterior shifts.
The residual Gram theorem assumes explicit original-observation witness pairings;
no actual remote jet witness, conditional genericity or Gaussian decomposition
is asserted. Samples remain on the original smooth coefficient carrier. -/

noncomputable section
open scoped BigOperators
set_option autoImplicit false

namespace I4SourceFinitePinKernel

/-- Pair an observation row with a finite original coefficient direction,
in the fixed observation-times-direction order. -/
def finitePairing {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) : ℝ :=
  v.sum (fun m z => a m * z)

/-- Subtract an arbitrary finite correction of the original pin rows. -/
def residualCoefficient {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ) (j : Fin q) (m : ι) : ℝ :=
  b j m - ∑ i, R j i * a i m

/-- The finite pairing of a residual row retains the arbitrary correction. -/
theorem finitePairing_residualCoefficient {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ) (j : Fin q) (v : ι →₀ ℝ) :
    finitePairing (residualCoefficient a b R j) v =
      finitePairing (b j) v - ∑ i, R j i * finitePairing (a i) v := by
  classical
  simp only [finitePairing, Finsupp.sum, residualCoefficient, sub_mul,
    Finset.sum_sub_distrib, Finset.sum_mul, Finset.mul_sum]
  congr 1
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _hi
  apply Finset.sum_congr rfl
  intro m _hm
  ring

/-- Every finite corrected row is summable on the original coefficient index. -/
theorem residualCoefficient_summable {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ)
    (ha : ∀ i, Summable (a i)) (hb : ∀ j, Summable (b j)) (j : Fin q) :
    Summable (residualCoefficient a b R j) := by
  exact (hb j).sub (summable_sum (fun i _hi => (ha i).mul_left (R j i)))

private theorem finitePairing_rowCombination {ι : Type*} {q : ℕ}
    (c : Fin q → ι → ℝ) (z : Fin q → ℝ) (v : ι →₀ ℝ) :
    finitePairing (fun m => ∑ j, z j * c j m) v =
      ∑ j, z j * finitePairing (c j) v := by
  classical
  simp only [finitePairing, Finsupp.sum, Finset.sum_mul, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _hj
  apply Finset.sum_congr rfl
  intro m _hm
  ring

/-- Explicit finite pin-kernel and original-observation right-inverse identities
force positive definiteness for every correction matrix, by the accepted Gram
separation theorem. No residual rank or positivity certificate is assumed. -/
theorem coefficientGram_posDef_of_finite_kernel_rightInverse
    {ι : Type*} {p q : ℕ}
    (a : Fin p → ι → ℝ) (b : Fin q → ι → ℝ)
    (R : Matrix (Fin q) (Fin p) ℝ)
    (ha : ∀ i, Summable (a i)) (hb : ∀ j, Summable (b j))
    (v : Fin q → ι →₀ ℝ)
    (hker : ∀ i s, finitePairing (a i) (v s) = 0)
    (hright : ∀ j s, finitePairing (b j) (v s) = if j = s then 1 else 0) :
    (I4ContactGram.coefficientGram (residualCoefficient a b R)).PosDef := by
  apply I4ContactGram.coefficientGram_posDef_of_separating _
    (residualCoefficient_summable a b R ha hb)
  intro z hz
  classical
  by_contra! hzero
  apply hz
  funext s
  have hp : finitePairing (fun m => ∑ j, z j * residualCoefficient a b R j m) (v s) = 0 := by
    simp only [finitePairing, Finsupp.sum, hzero, zero_mul, Finset.sum_const_zero]
  rw [finitePairing_rowCombination] at hp
  simp_rw [finitePairing_residualCoefficient, hker, mul_zero, Finset.sum_const_zero,
    sub_zero, hright] at hp
  simpa using hp

open I4Source I4Smooth I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceEndpointRegression I4SourceSmoothConditional

/-- Add a finite original coefficient direction without changing the literal
smooth-sample carrier. This construction allows every real period. -/
def finiteShiftSample {L : ℝ} (v : SourceMode 2 →₀ ℝ)
    (ω : SmoothSample 2 L) : SmoothSample 2 L := by
  classical
  refine ⟨fun m => ω.val m + v m, ?_⟩
  apply (goodSample_finite_change_iff 2 L ω.val (fun m => ω.val m + v m)
    v.support ?_).mp ω.property
  intro m hm
  rw [Finsupp.not_mem_support_iff.mp hm, add_zero]

@[simp] theorem finiteShiftSample_val {L : ℝ} (v : SourceMode 2 →₀ ℝ)
    (ω : SmoothSample 2 L) (m : SourceMode 2) :
    (finiteShiftSample v ω).val m = ω.val m + v m := rfl

private theorem rawPinCoefficient_weighted_summable {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (ω : SmoothSample 2 L) (i : Fin 6) :
    Summable (fun m => rawPinCoefficient L r i m * ω.val m) :=
  derivativeCoefficient_weighted_summable hL ω (rawDerivativeOrder (Fin.castAdd 6 i))
    (rawDerivativePoint r (Fin.castAdd 6 i)) (rawDerivativeDirections (Fin.castAdd 6 i))

private theorem finitePairing_hasSum {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    HasSum (fun m => a m * v m) (finitePairing a v) := by
  classical
  apply hasSum_sum_of_ne_finset_zero
  intro m hm
  simp only [Finsupp.not_mem_support_iff.mp hm, mul_zero]

/-- The exact raw pin response of one finite original coefficient shift. -/
theorem rawPins_finiteShiftSample {L : ℝ} (hL : L ≠ 0) (r : ℝ)
    (v : SourceMode 2 →₀ ℝ) (ω : SmoothSample 2 L) :
    rawPins L r (finiteShiftSample v ω) = rawPins L r ω +
      fun i => finitePairing (rawPinCoefficient L r i) v := by
  rw [rawPins_series hL, rawPins_series hL]
  funext i
  have h := (rawPinCoefficient_weighted_summable hL r ω i).hasSum.add
    (finitePairing_hasSum (rawPinCoefficient L r i) v)
  change (∑' m, rawPinCoefficient L r i m * (ω.val m + v m)) =
    (∑' m, rawPinCoefficient L r i m * ω.val m) +
      finitePairing (rawPinCoefficient L r i) v
  simpa only [mul_add] using h.tsum_eq

/-- Every literal target posterior commutes with a finite pin-kernel shift.
The radius is arbitrary, including zero; no covariance invertibility or
conditional-distribution assertion is required by this deterministic equality. -/
theorem rawPosteriorSample_finiteShiftSample {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (t : Fin 6 → ℝ) (v : SourceMode 2 →₀ ℝ)
    (hker : ∀ i, finitePairing (rawPinCoefficient L r i) v = 0)
    (ω : SmoothSample 2 L) :
    rawPosteriorSample hL r t (finiteShiftSample v ω) =
      finiteShiftSample v (rawPosteriorSample hL r t ω) := by
  apply Subtype.ext
  funext m
  rw [rawPosteriorSample_val, finiteShiftSample_val, finiteShiftSample_val,
    rawPosteriorSample_val, rawPins_finiteShiftSample hL]
  have hzero : (fun i => finitePairing (rawPinCoefficient L r i) v) = 0 := funext hker
  rw [hzero, add_zero]
  ring

end I4SourceFinitePinKernel
