import SourceSmoothTopology

noncomputable section
open I4SmoothCarrier I4SourceSmoothTopology I4SourceSmoothConditional I4SourceEndpointRegression
open MeasureTheory ProbabilityTheory Filter
open scoped Topology BoundedContinuousFunction

set_option autoImplicit false

namespace I4SmoothTopologyControls

/-- The all-dimensional theorem really includes the zero-dimensional source. -/
example {L : ℝ} (hL : L ≠ 0) : StronglyMeasurable (sourceDerivativeBCF 0 hL 3) :=
  sourceDerivativeBCF_stronglyMeasurable 0 hL 3

/-- Both zeroth jet order and zero-dimensional source retain norm Borel measurability. -/
example {L : ℝ} (hL : L ≠ 0) :
    @Measurable (SmoothSample 0 L) ((j : Fin 1) → DerivativeBCF 0 j) _ (borel _)
      (sourceFiniteJet 0 hL 0) := sourceFiniteJet_borel 0 hL 0

/-- Zeroth multilinear jets recover the literal field value at the empty tuple. -/
example (d : ℕ) {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample d L) (x : Fin d → ℝ) :
    sourceDerivativeBCF d hL 0 ω x (fun a => Fin.elim0 a) = smoothSourceField d L ω x := by
  rw [sourceDerivativeBCF_apply, iteratedFDeriv_zero_apply]

/-- This type check fixes the target sigma algebra to the norm-topology Borel
structure explicitly. A product-coordinate conditional law would not suffice. -/
example {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hG : IsUnit (sourcePinCovarianceAt L r)) (K : ℕ) :
    @HasCondDistrib (SmoothSample 2 L) (Fin 6 → ℝ) ((j : Fin (K+1)) → DerivativeBCF 2 j)
      _ _ (borel _) (sourceFiniteJet 2 hL K) (sourceConfluentPinsAt L r)
      (@Kernel.map (Fin 6 → ℝ) (SmoothSample 2 L) ((j : Fin (K+1)) → DerivativeBCF 2 j)
        _ _ (borel _) (sourceSmoothKernel hL r) (sourceFiniteJet 2 hL K)) (smoothLaw 2 L) :=
  sourceFiniteJet_hasCondDistrib hL r hG K

/-- Norm functionals are covered, beyond finite point evaluations. -/
example {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hG : IsUnit (sourcePinCovarianceAt L r)) :
    HasCondDistrib (fun ω => ‖sourceFiniteJet 2 hL 3 ω‖) (sourceConfluentPinsAt L r)
      ((sourceSmoothKernel hL r).map (fun ω => ‖sourceFiniteJet 2 hL 3 ω‖)) (smoothLaw 2 L) :=
  sourceFiniteJet_functional_hasCondDistrib hL r hG 3 (fun v => ‖v‖) continuous_norm.borel_measurable

/-- A singleton compact set's function values do not determine derivative jets.
This rejects a false value-only compact field-space identification. -/
theorem singleton_values_do_not_determine_first_derivative :
    Real.sin 0 = (fun _ : ℝ => (0 : ℝ)) 0 ∧
      deriv Real.sin 0 ≠ deriv (fun _ : ℝ => (0 : ℝ)) 0 := by
  simp

/-- Actual periodicity applies at every order and every carrier sample. -/
example (d : ℕ) {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample d L)
    (n : Fin d → ℤ) (x : Fin d → ℝ) :
    sourceDerivativeBCF d hL 4 ω (x + fun a => L*(n a : ℝ)) = sourceDerivativeBCF d hL 4 ω x :=
  sourceDerivativeBCF_lattice_periodic d hL 4 ω n x

end I4SmoothTopologyControls
