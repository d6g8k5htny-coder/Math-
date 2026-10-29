import SourceRemoteJetGaussian
import Mathlib.Tactic.Omega

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open I4Foundation I4Source I4Weights I4Smooth I4SmoothCarrier
open I4SourceGaussian I4SourceCovariance I4SourceDerivativeGaussian
open I4SourceConfluentPins I4SourceConfluentLimits I4SourceEndpointRegression
open I4SourceSmoothConditional I4SourceRawPinConditioning I4SourceRemoteJetWitness
open I4SourceRemoteJetGaussian MeasureTheory ProbabilityTheory WithLp

namespace RemoteJetGaussianControls

/- Concrete-control text only. Required tactic import: Mathlib.Tactic.Omega
   (and the existing norm_cast/norm_num imports). No source positivity proof
   is repeated here: only the two literal quotient-separation hypotheses. -/

private theorem concrete_remote_zero_radius_separation :
    I4Torus.torusProjection 2 (-2 : ℝ) ![1,0] ≠
        I4Torus.torusProjection 2 (-2 : ℝ) (I4SourceConfluentPins.endpointM 0) ∧
    I4Torus.torusProjection 2 (-2 : ℝ) ![1,0] ≠
        I4Torus.torusProjection 2 (-2 : ℝ) (I4SourceConfluentPins.endpointS 0) := by
  have h10 : ((1 : ℝ) : AddCircle (-2 : ℝ)) ≠ 0 := by
    intro h
    obtain ⟨n, hn⟩ := (AddCircle.coe_eq_zero_iff (p := (-2 : ℝ))).mp h
    have hnR : (n : ℝ) * (-2) = 1 := by
      simpa only [zsmul_eq_mul] using hn
    have hnZ : n * (-2 : ℤ) = 1 := by
      exact_mod_cast hnR
    omega
  constructor
  · intro h
    apply h10
    have h0 := congrFun h (0 : Fin 2)
    simpa [I4Torus.torusProjection, I4SourceConfluentPins.endpointM] using h0
  · intro h
    apply h10
    have h0 := congrFun h (0 : Fin 2)
    simpa [I4Torus.torusProjection, I4SourceConfluentPins.endpointS] using h0

/-- Concrete signed-period repeated-pin actual residual Gram positivity. -/
theorem actual_signed_repeated_pin_posDef :
    (remoteResidualCovariance (-2) 0 ![1,0]).PosDef :=
  remoteResidualCovariance_posDef (by norm_num) 0 ![1,0]
    concrete_remote_zero_radius_separation.1 concrete_remote_zero_radius_separation.2


/-- Six literal first-jet entries are recovered on the actual posterior sample. -/
theorem literal_raw_order {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (t : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    let η := rawPosteriorSample hL r t ω
    remoteJet L (endpointM r) η 0 = t 0 ∧ remoteJet L (endpointS r) η 0 = t 1 ∧
    remoteJet L (endpointM r) η 1 = t 2 ∧ remoteJet L (endpointS r) η 1 = t 3 ∧
    remoteJet L (endpointM r) η 2 = t 4 ∧ remoteJet L (endpointS r) η 2 = t 5 := by
  have h := rawPosteriorSample_rawPins hL r hr hG t ω
  exact ⟨congrFun h 0, congrFun h 1, congrFun h 2, congrFun h 3,
    congrFun h 4, congrFun h 5⟩

/-- Multiple nonzero literal target entries detect any lost or permuted mean components. -/
theorem six_nonzero_targets {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (hG : IsUnit (sourcePinCovarianceAt L r)) (ω : SmoothSample 2 L) :
    let η := rawPosteriorSample hL r ![1,2,3,4,5,6] ω
    remoteJet L (endpointM r) η 0 = 1 ∧ remoteJet L (endpointS r) η 0 = 2 ∧
    remoteJet L (endpointM r) η 1 = 3 ∧ remoteJet L (endpointS r) η 1 = 4 ∧
    remoteJet L (endpointM r) η 2 = 5 ∧ remoteJet L (endpointS r) η 2 = 6 :=
  literal_raw_order hL r hr hG ![1,2,3,4,5,6] ω

/-- Signed original period, repeated pins, arbitrary target: a defined sampling identity. -/
theorem negative_period_zero_radius_sample (ω : SmoothSample 2 (-2)) :
    remoteJet (-2) ![1,0] (rawPosteriorSample (by norm_num) 0 ![1,2,3,4,5,6] ω) =
      remoteJet (-2) ![1,0] ω - remoteRegressionMatrix (-2) 0 ![1,0] *ᵥ rawPins (-2) 0 ω +
        remotePosteriorMean (-2) 0 ![1,0] ![1,2,3,4,5,6] :=
  remoteJet_rawPosteriorSample (by norm_num) 0 ![1,0] ![1,2,3,4,5,6] ω

/-- The finite Gaussian presentation remains valid at a singular sampling radius. -/
theorem negative_period_zero_radius_law :
    (rawPinKernel (L := -2) (by norm_num) 0 ![1,2,3,4,5,6]).map
      (fun ω => toLp 2 (remoteJet (-2) ![1,0] ω)) =
    multivariateGaussian (toLp 2 (remotePosteriorMean (-2) 0 ![1,0] ![1,2,3,4,5,6]))
      (remoteResidualCovariance (-2) 0 ![1,0]) :=
  rawPinKernel_remoteJet_eq_multivariateGaussian (by norm_num) 0 ![1,0] ![1,2,3,4,5,6]

/-- At a pin the sampling statement allows a singular covariance. -/
theorem pin_sampling_law {L : ℝ} (hL : L ≠ 0) (r : ℝ) (t : Fin 6 → ℝ) :
    (rawPinKernel hL r t).map (fun ω => toLp 2 (remoteJet L (endpointM r) ω)) =
      multivariateGaussian (toLp 2 (remotePosteriorMean L r (endpointM r) t))
        (remoteResidualCovariance L r (endpointM r)) :=
  rawPinKernel_remoteJet_eq_multivariateGaussian hL r (endpointM r) t

/-- All six target components enter the same matrix, with target-independent S. -/
theorem mean_difference (L r : ℝ) (x : Fin 2 → ℝ) (t₁ t₂ : Fin 6 → ℝ) :
    remotePosteriorMean L r x t₁ - remotePosteriorMean L r x t₂ =
      remoteRegressionMatrix L r x *ᵥ (t₁-t₂) := by
  exact (Matrix.mulVec_sub _ _ _).symm

/-- Two nonzero targets share the literal residual Gram covariance. -/
theorem same_covariance_two_targets {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x : Fin 2 → ℝ) :
    (rawPinKernel hL r ![1,2,3,4,5,6]).map (fun ω => toLp 2 (remoteJet L x ω)) =
      multivariateGaussian (toLp 2 (remotePosteriorMean L r x ![1,2,3,4,5,6]))
        (remoteResidualCovariance L r x) ∧
    (rawPinKernel hL r ![6,5,4,3,2,1]).map (fun ω => toLp 2 (remoteJet L x ω)) =
      multivariateGaussian (toLp 2 (remotePosteriorMean L r x ![6,5,4,3,2,1]))
        (remoteResidualCovariance L r x) ∧
    remotePosteriorMean L r x ![1,2,3,4,5,6] - remotePosteriorMean L r x ![6,5,4,3,2,1] =
      remoteRegressionMatrix L r x *ᵥ (![1,2,3,4,5,6]-![6,5,4,3,2,1]) :=
  ⟨rawPinKernel_remoteJet_eq_multivariateGaussian hL r x _,
    rawPinKernel_remoteJet_eq_multivariateGaussian hL r x _, mean_difference L r x _ _⟩

/-- Delta is chosen before both x and the arbitrary literal raw target. -/
theorem uniform_RCD_and_fibers {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ x : Fin 2 → ℝ,
      I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r) →
      I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r) →
      HasCondDistrib (remoteJet L x) (rawPins L r)
        ((rawPinKernel hL r).map (remoteJet L x)) (smoothLaw 2 L) ∧
      ∀ t : Fin 6 → ℝ, rawPinKernel hL r t {ω | rawPins L r ω = t} = 1 := by
  obtain ⟨δ,hδ,hδ1,h⟩ := rawPinKernel_remoteJet_conditional_uniform hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ x hxM hxS
  exact ⟨(h r hr hrδ x hxM hxS).1,fun t => ((h r hr hrδ x hxM hxS).2.2 t).2⟩

/-- The same valid interval recovers all six nonzero pin targets on every sample. -/
theorem uniform_literal_targets {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧ ∀ r : ℝ, 0 < r → r < δ → ∀ ω : SmoothSample 2 L,
      let η := rawPosteriorSample hL r ![1,2,3,4,5,6] ω
      remoteJet L (endpointM r) η 0 = 1 ∧ remoteJet L (endpointS r) η 0 = 2 ∧
      remoteJet L (endpointM r) η 1 = 3 ∧ remoteJet L (endpointS r) η 1 = 4 ∧
      remoteJet L (endpointM r) η 2 = 5 ∧ remoteJet L (endpointS r) η 2 = 6 := by
  obtain ⟨K,δ,_hK,hδ,hδ1,h⟩ :=
    I4SourceCompactTargetMoments.sourceInverse_target_uniform_bounds hL
  exact ⟨δ,hδ,hδ1,fun r hr hrδ ω => six_nonzero_targets hL r hr.ne' (h r hr hrδ).1 ω⟩

/-- Finite scalar counterexample: preserving the deterministic affine mean is necessary. -/
theorem finite_affine_scalar_law :
    (Measure.dirac (0:ℝ)).map (fun z : ℝ => (0:ℝ)*z+1) = Measure.dirac 1 := by
  simp

/-- Singleton {1} separates the correct affine law from the omitted-mean law. -/
theorem finite_mean_omission_counterexample :
    (Measure.dirac (0:ℝ)).map (fun z : ℝ => (0:ℝ)*z+1) ≠
      (Measure.dirac (0:ℝ)).map (fun z : ℝ => (0:ℝ)*z+0) := by
  have h1 : (Measure.dirac (1:ℝ)) {1} = 1 := by simp
  have h0 : (Measure.dirac (0:ℝ)) {1} = 0 := by simp
  simpa using (show (Measure.dirac (1:ℝ)) ≠ Measure.dirac (0:ℝ) from by
    intro h
    have hh := congrArg (fun μ : Measure ℝ => μ {1}) h
    rw [h1,h0] at hh
    exact one_ne_zero hh)

end RemoteJetGaussianControls
