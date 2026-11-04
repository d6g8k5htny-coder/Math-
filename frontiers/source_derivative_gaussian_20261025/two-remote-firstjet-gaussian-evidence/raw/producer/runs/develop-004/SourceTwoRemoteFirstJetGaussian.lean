import SourceTwoRemoteFirstJetWitness
import SourceRemoteJetGaussian
import SourceSmoothTopology

/-! Joint ordinary first jets of two points on the same actual posterior sample.
The all-radius law retains full target mean and all cross covariance blocks. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open I4Source I4SmoothCarrier I4SourceDerivativeGaussian I4SourceConfluentPins
open I4SourceConfluentLimits I4SourceRawPinConditioning I4SourceRemoteJetWitness
open I4SourceRemoteJetGaussian I4SourceTwoRemoteFirstJetWitness I4SourceSmoothTopology
open MeasureTheory ProbabilityTheory WithLp ResearchFormalCoreR1

namespace I4SourceTwoRemoteFirstJetGaussian

/-- Literal order valueX,dxX,dyX,valueY,dxY,dyY on one original sample. -/
def twoRemoteFirstJet (L : ℝ) (x y : Fin 2 → ℝ) (ω : SmoothSample 2 L) : Fin 6 → ℝ :=
  ![remoteJet L x ω 0,remoteJet L x ω 1,remoteJet L x ω 2,
    remoteJet L y ω 0,remoteJet L y ω 1,remoteJet L y ω 2]

/-- Concatenated actual corrections, retaining the literal raw pin columns. -/
def twoRemoteRegressionMatrix (L r : ℝ) (x y : Fin 2 → ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  ![remoteRegressionMatrix L r x 0,remoteRegressionMatrix L r x 1,
    remoteRegressionMatrix L r x 2,remoteRegressionMatrix L r y 0,
    remoteRegressionMatrix L r y 1,remoteRegressionMatrix L r y 2]

/-- Full deterministic response to all six raw target coordinates. -/
def twoRemotePosteriorMean (L r : ℝ) (x y : Fin 2 → ℝ) (t : Fin 6 → ℝ) : Fin 6 → ℝ :=
  twoRemoteRegressionMatrix L r x y *ᵥ t

/-- Target-free Gram of the literal original residual coefficient rows. -/
def twoRemoteResidualCovariance (L r : ℝ) (x y : Fin 2 → ℝ) : Matrix (Fin 6) (Fin 6) ℝ :=
  I4ContactGram.coefficientGram (I4SourceFinitePinKernel.residualCoefficient
    (rawPinCoefficient L r) (twoRemoteFirstJetCoefficient L x y)
    (twoRemoteRegressionMatrix L r x y))

private def jointOrder : Fin 12 → ℕ := ![0,0,1,1,1,1,0,1,1,0,1,1]
private def jointPoint (r : ℝ) (x y : Fin 2 → ℝ) : Fin 12 → (Fin 2 → ℝ) :=
  ![endpointM r,endpointS r,endpointM r,endpointS r,endpointM r,endpointS r,x,x,x,y,y,y]
private def jointDirection : Fin 12 → (Fin 2 → ℝ) :=
  ![directionX,directionX,directionX,directionX,directionY,directionY,
    directionX,directionX,directionY,directionX,directionX,directionY]
private def jointVector (L r : ℝ) (x y : Fin 2 → ℝ) (ω : SmoothSample 2 L) : Fin 12 → ℝ :=
  fun i => iteratedFDeriv ℝ (jointOrder i) (smoothSourceField 2 L ω)
    (jointPoint r x y i) (fun _ => jointDirection i)
private def jointCoefficient (L r : ℝ) (x y : Fin 2 → ℝ) : Fin 12 → SourceMode 2 → ℝ :=
  fun i => derivativeCoefficient 2 L (jointOrder i) (jointPoint r x y i)
    (fun _ => jointDirection i)

private theorem jointVector_actual (L r : ℝ) (x y : Fin 2 → ℝ) (ω : SmoothSample 2 L) :
    jointVector L r x y ω = Fin.append (rawPins L r ω) (twoRemoteFirstJet L x y ω) := by
  funext i
  fin_cases i
  · change iteratedFDeriv ℝ 0 (smoothSourceField 2 L ω) (endpointM r) (fun _ => directionX) = smoothSourceField 2 L ω (endpointM r)
    exact iteratedFDeriv_zero_apply _
  · change iteratedFDeriv ℝ 0 (smoothSourceField 2 L ω) (endpointS r) (fun _ => directionX) = smoothSourceField 2 L ω (endpointS r)
    exact iteratedFDeriv_zero_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) (endpointM r) (fun _ => directionX) = fderiv ℝ (smoothSourceField 2 L ω) (endpointM r) directionX
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) (endpointS r) (fun _ => directionX) = fderiv ℝ (smoothSourceField 2 L ω) (endpointS r) directionX
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) (endpointM r) (fun _ => directionY) = fderiv ℝ (smoothSourceField 2 L ω) (endpointM r) directionY
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) (endpointS r) (fun _ => directionY) = fderiv ℝ (smoothSourceField 2 L ω) (endpointS r) directionY
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 0 (smoothSourceField 2 L ω) x (fun _ => directionX) = smoothSourceField 2 L ω x
    exact iteratedFDeriv_zero_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x (fun _ => directionX) = fderiv ℝ (smoothSourceField 2 L ω) x directionX
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x (fun _ => directionY) = fderiv ℝ (smoothSourceField 2 L ω) x directionY
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 0 (smoothSourceField 2 L ω) y (fun _ => directionX) = smoothSourceField 2 L ω y
    exact iteratedFDeriv_zero_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) y (fun _ => directionX) = fderiv ℝ (smoothSourceField 2 L ω) y directionX
    exact iteratedFDeriv_one_apply _
  · change iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) y (fun _ => directionY) = fderiv ℝ (smoothSourceField 2 L ω) y directionY
    exact iteratedFDeriv_one_apply _

private theorem jointCoefficient_actual (L r : ℝ) (x y : Fin 2 → ℝ) :
    jointCoefficient L r x y = Fin.append (rawPinCoefficient L r)
      (twoRemoteFirstJetCoefficient L x y) := by
  funext i m
  fin_cases i
  · rfl
  · rfl
  · rfl
  · rfl
  · rfl
  · rfl
  · change iteratedFDeriv ℝ 0 (modeCoefficient 2 L m) x (fun _ => directionX) = modeCoefficient 2 L m x
    exact iteratedFDeriv_zero_apply _
  · rfl
  · rfl
  · change iteratedFDeriv ℝ 0 (modeCoefficient 2 L m) y (fun _ => directionX) = modeCoefficient 2 L m y
    exact iteratedFDeriv_zero_apply _
  · rfl
  · rfl

private theorem joint_hasGaussianLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ) :
    HasGaussianLaw (jointVector L r x y) (smoothLaw 2 L) :=
  smoothSourceField_derivativeVector_hasGaussianLaw 2 hL 12 jointOrder
    (jointPoint r x y) (fun i _ => jointDirection i)

private def jointSplit : (Fin 12 → ℝ) →L[ℝ] ((Fin 6 → ℝ) × (Fin 6 → ℝ)) where
  toFun z := (fun i => z (Fin.castAdd 6 i),fun i => z (Fin.natAdd 6 i))
  map_add' _ _ := rfl
  map_smul' _ _ := rfl
  cont := by fun_prop

private theorem raw_remote_jointGaussian {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ) :
    HasGaussianLaw (fun ω => (rawPins L r ω,twoRemoteFirstJet L x y ω)) (smoothLaw 2 L) := by
  apply ((joint_hasGaussianLaw hL r x y).map_fun jointSplit).congr
  filter_upwards with ω
  change jointSplit (jointVector L r x y ω) = _
  rw [jointVector_actual]
  change ((fun i => Fin.append (rawPins L r ω) (twoRemoteFirstJet L x y ω) (Fin.castAdd 6 i)),
    (fun i => Fin.append (rawPins L r ω) (twoRemoteFirstJet L x y ω) (Fin.natAdd 6 i))) = _
  simp only [Fin.append_left,Fin.append_right]

private def residualMatrix (R : Matrix (Fin 6) (Fin 6) ℝ) : Matrix (Fin 6) (Fin 12) ℝ :=
  fun i => Fin.append (fun j => -R i j) (fun j => if i=j then 1 else 0)

private theorem residualMatrix_apply (R : Matrix (Fin 6) (Fin 6) ℝ) (z : Fin 12 → ℝ) :
    residualMatrix R *ᵥ z = (fun i => z (Fin.natAdd 6 i)) -
      R *ᵥ (fun i => z (Fin.castAdd 6 i)) := by
  ext i
  change (∑ a : Fin (6+6), Fin.append (fun j => -R i j) (fun j => if i=j then 1 else 0) a * z a) = _
  rw [Fin.sum_univ_add (a:=6) (b:=6)]
  simp only [Fin.append_left,Fin.append_right,neg_mul,Finset.sum_neg_distrib,
    ite_mul,one_mul,zero_mul,Fintype.sum_ite_eq]
  change - (∑ a, R i a*z (Fin.castAdd 6 a)) + z (Fin.natAdd 6 i) =
    z (Fin.natAdd 6 i) - ∑ a, R i a*z (Fin.castAdd 6 a)
  ring

private theorem posterior_actual {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ)
    (t : Fin 6 → ℝ) (ω : SmoothSample 2 L) :
    twoRemoteFirstJet L x y (rawPosteriorSample hL r t ω) =
      residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ jointVector L r x y ω +
        twoRemotePosteriorMean L r x y t := by
  rw [residualMatrix_apply,jointVector_actual]
  have hx := remoteJet_rawPosteriorSample hL r x t ω
  have hy := remoteJet_rawPosteriorSample hL r y t ω
  ext i
  fin_cases i
  all_goals first
    | exact congrFun hx 0 | exact congrFun hx 1 | exact congrFun hx 2
    | exact congrFun hy 0 | exact congrFun hy 1 | exact congrFun hy 2

private theorem residual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ) :
    HasGaussianLaw (fun ω => residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ
      jointVector L r x y ω) (smoothLaw 2 L) := by
  let B := (Matrix.toLin' (twoRemoteRegressionMatrix L r x y)).toContinuousLinearMap
  have hg := (regression_residual_jointGaussian (raw_remote_jointGaussian hL r x y) B 0 0).snd
  apply hg.congr
  filter_upwards with ω
  rw [residualMatrix_apply,jointVector_actual]
  change twoRemoteFirstJet L x y ω - 0 -
    twoRemoteRegressionMatrix L r x y *ᵥ (rawPins L r ω - 0) = _
  simp only [sub_zero,Fin.append_left,Fin.append_right]

private theorem posterior_hasGaussianLaw {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ)
    (t : Fin 6 → ℝ) :
    HasGaussianLaw (fun ω => twoRemoteFirstJet L x y (rawPosteriorSample hL r t ω))
      (smoothLaw 2 L) := by
  have h := residual_hasGaussianLaw hL r x y
  let c := twoRemotePosteriorMean L r x y t
  have hg : HasGaussianLaw (fun ω => residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ
      jointVector L r x y ω + c) (smoothLaw 2 L) := by
    refine ⟨h.aemeasurable.add aemeasurable_const,?_⟩
    have : IsGaussian ((smoothLaw 2 L).map (fun ω =>
      residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ jointVector L r x y ω)) :=
      h.isGaussian_map
    convert (inferInstance : IsGaussian (((smoothLaw 2 L).map (fun ω =>
      residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ jointVector L r x y ω)).map
        (fun v => v+c))) using 1
    rw [AEMeasurable.map_map_of_aemeasurable (by fun_prop) h.aemeasurable]
    rfl
  exact hg.congr (Filter.Eventually.of_forall (fun ω => (posterior_actual hL r x y t ω).symm))

private theorem joint_integral_zero {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ) :
    (∫ ω, jointVector L r x y ω ∂smoothLaw 2 L) = 0 := by
  ext i
  have hi := (ContinuousLinearMap.proj i : (Fin 12 → ℝ) →L[ℝ] ℝ).integral_comp_comm
    (joint_hasGaussianLaw hL r x y).integrable
  change (∫ ω, jointVector L r x y ω i ∂smoothLaw 2 L) =
    (∫ ω, jointVector L r x y ω ∂smoothLaw 2 L) i at hi
  rw [← hi]
  exact I4SourceEndpointParameters.smoothSourceField_derivative_integral_zero 2 hL
    (jointOrder i) (jointPoint r x y i) (fun _ => jointDirection i)

private theorem posterior_integral {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ)
    (t : Fin 6 → ℝ) :
    (∫ ω, twoRemoteFirstJet L x y (rawPosteriorSample hL r t ω) ∂smoothLaw 2 L) =
      twoRemotePosteriorMean L r x y t := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  let T := (Matrix.toLin' (residualMatrix (twoRemoteRegressionMatrix L r x y))).toContinuousLinearMap
  have hi := T.integral_comp_comm (joint_hasGaussianLaw hL r x y).integrable
  change (∫ ω, residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ jointVector L r x y ω
    ∂smoothLaw 2 L) = T (∫ ω, jointVector L r x y ω ∂smoothLaw 2 L) at hi
  rw [joint_integral_zero hL,map_zero] at hi
  simp_rw [posterior_actual hL]
  rw [integral_add (residual_hasGaussianLaw hL r x y).integrable (integrable_const _),hi,
    integral_const,zero_add]
  simp

/- Uncompiled text-only fixed12-to6 covariance transport for one integration
inside I4SourceTwoRemoteFirstJetGaussian. No Gaussian/source-series argument
is repeated here. The producer qualifies the actual integrated new module. -/

private theorem fixed12_affine_covariance {Ω ι : Type*}
    [MeasurableSpace Ω] [Countable ι]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (Z : Ω → Fin 12 → ℝ) (q : Fin 12 → ι → ℝ)
    (T : Matrix (Fin 6) (Fin 12) ℝ)
    (hZ : ∀ a, MemLp (fun ω => Z ω a) 2 μ)
    (hq : ∀ a, Summable (q a))
    (hc : ∀ a b,
      cov[fun ω => Z ω a, fun ω => Z ω b; μ] = ∑' m, q a m*q b m)
    (i j : Fin 6) :
    cov[fun ω => (T *ᵥ Z ω) i, fun ω => (T *ᵥ Z ω) j; μ] =
      I4ContactGram.coefficientGram (fun k m => ∑ a : Fin 12, T k a*q a m) i j := by
  have hs : HasSum
      (fun m : ι => ∑ a : Fin 12, ∑ b : Fin 12,
        T i a * (q a m*q b m) * T j b)
      (∑ a : Fin 12, ∑ b : Fin 12,
        T i a * (∑' m : ι, q a m*q b m) * T j b) :=
    hasSum_sum (fun a _ => hasSum_sum (fun b _ =>
      (((I4ContactGram.coefficient_product_summable (hq a) (hq b)).hasSum).mul_left
        (T i a)).mul_right (T j b)))
  have hprod :
      (fun m : ι =>
        (∑ a : Fin 12, T i a*q a m) * (∑ b : Fin 12, T j b*q b m)) =
      (fun m : ι => ∑ a : Fin 12, ∑ b : Fin 12,
        T i a * (q a m*q b m) * T j b) := by
    funext m
    rw [Finset.sum_mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    apply Finset.sum_congr rfl
    intro b _
    ring
  have htsum :
      (∑' m : ι,
        (∑ a : Fin 12, T i a*q a m) * (∑ b : Fin 12, T j b*q b m)) =
      ∑ a : Fin 12, ∑ b : Fin 12,
        T i a * (∑' m : ι, q a m*q b m) * T j b := by
    rw [hprod]
    exact hs.tsum_eq
  change
    cov[fun ω => ∑ a : Fin 12, T i a*Z ω a,
      fun ω => ∑ b : Fin 12, T j b*Z ω b; μ] =
      ∑' m : ι,
        (∑ a : Fin 12, T i a*q a m) * (∑ b : Fin 12, T j b*q b m)
  rw [covariance_fun_sum_fun_sum
    (fun a => (hZ a).const_mul (T i a))
    (fun b => (hZ b).const_mul (T j b))]
  trans ∑ a : Fin 12, ∑ b : Fin 12,
    T i a * (∑' m : ι, q a m*q b m) * T j b
  · apply Finset.sum_congr rfl
    intro a _
    apply Finset.sum_congr rfl
    intro b _
    rw [covariance_const_mul_left, covariance_const_mul_right, hc a b]
    ring
  · exact htsum.symm


private theorem transformed_coefficient (L r : ℝ) (x y : Fin 2 → ℝ) :
    (fun i m => ∑ a : Fin 12, residualMatrix (twoRemoteRegressionMatrix L r x y) i a *
      jointCoefficient L r x y a m) =
    I4SourceFinitePinKernel.residualCoefficient (rawPinCoefficient L r)
      (twoRemoteFirstJetCoefficient L x y) (twoRemoteRegressionMatrix L r x y) := by
  funext i m
  change (residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ
    (fun a => jointCoefficient L r x y a m)) i = _
  rw [residualMatrix_apply,jointCoefficient_actual]
  simp only [Fin.append_left,Fin.append_right]
  rfl

private theorem posterior_covariance {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ)
    (t : Fin 6 → ℝ) (i j : Fin 6) :
    cov[fun ω => twoRemoteFirstJet L x y (rawPosteriorSample hL r t ω) i,
      fun ω => twoRemoteFirstJet L x y (rawPosteriorSample hL r t ω) j;smoothLaw 2 L] =
      twoRemoteResidualCovariance L r x y i j := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  simp_rw [posterior_actual hL]
  change cov[fun ω => (residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ
      jointVector L r x y ω) i + twoRemotePosteriorMean L r x y t i,
    fun ω => (residualMatrix (twoRemoteRegressionMatrix L r x y) *ᵥ
      jointVector L r x y ω) j + twoRemotePosteriorMean L r x y t j; smoothLaw 2 L] = _
  rw [covariance_add_const_left ((residual_hasGaussianLaw hL r x y).eval i).integrable,
    covariance_add_const_right ((residual_hasGaussianLaw hL r x y).eval j).integrable]
  have hc (a b : Fin 12) : cov[fun ω => jointVector L r x y ω a,
      fun ω => jointVector L r x y ω b;smoothLaw 2 L] =
      ∑' m, jointCoefficient L r x y a m * jointCoefficient L r x y b m :=
    smoothSourceField_derivative_covariance 2 hL _ _ _ _ _ _
  have hq (a : Fin 12) : Summable (jointCoefficient L r x y a) :=
    derivativeCoefficient_summable 2 hL _ _ _
  have hh := fixed12_affine_covariance (smoothLaw 2 L) (jointVector L r x y)
    (jointCoefficient L r x y) (residualMatrix (twoRemoteRegressionMatrix L r x y))
    (fun a => ((joint_hasGaussianLaw hL r x y).eval a).memLp_two) hq hc i j
  rw [transformed_coefficient] at hh
  exact hh

private theorem derivative_measurable {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    Measurable (fun ω : SmoothSample 2 L =>
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u) := by
  borelize (DerivativeBCF 2 k)
  have he : Continuous (fun F : DerivativeBCF 2 k => F x u) := by fun_prop
  have hh := he.measurable.comp (sourceDerivativeBCF_borel 2 hL k)
  change Measurable (fun ω => sourceDerivativeBCF 2 hL k ω x u) at hh
  simp_rw [sourceDerivativeBCF_apply] at hh
  exact hh

private theorem observation_measurable {L : ℝ} (hL : L ≠ 0) (x y : Fin 2 → ℝ) :
    Measurable (twoRemoteFirstJet L x y) := by
  apply Measurable.of_eval
  intro i
  fin_cases i
  · change Measurable (fun ω : SmoothSample 2 L => smoothSourceField 2 L ω x)
    simpa only [iteratedFDeriv_zero_apply] using derivative_measurable hL 0 x (fun i => Fin.elim0 i)
  · change Measurable (fun ω : SmoothSample 2 L => fderiv ℝ (smoothSourceField 2 L ω) x directionX)
    simpa only [iteratedFDeriv_one_apply] using derivative_measurable hL 1 x (fun _ => directionX)
  · change Measurable (fun ω : SmoothSample 2 L => fderiv ℝ (smoothSourceField 2 L ω) x directionY)
    simpa only [iteratedFDeriv_one_apply] using derivative_measurable hL 1 x (fun _ => directionY)
  · change Measurable (fun ω : SmoothSample 2 L => smoothSourceField 2 L ω y)
    simpa only [iteratedFDeriv_zero_apply] using derivative_measurable hL 0 y (fun i => Fin.elim0 i)
  · change Measurable (fun ω : SmoothSample 2 L => fderiv ℝ (smoothSourceField 2 L ω) y directionX)
    simpa only [iteratedFDeriv_one_apply] using derivative_measurable hL 1 y (fun _ => directionX)
  · change Measurable (fun ω : SmoothSample 2 L => fderiv ℝ (smoothSourceField 2 L ω) y directionY)
    simpa only [iteratedFDeriv_one_apply] using derivative_measurable hL 1 y (fun _ => directionY)

/-- Defined same-sample joint law, including collisions and singular pin radii. -/
theorem rawPinKernel_twoRemoteFirstJet_eq_multivariateGaussian {L : ℝ} (hL : L ≠ 0)
    (r : ℝ) (x y : Fin 2 → ℝ) (t : Fin 6 → ℝ) :
    (rawPinKernel hL r t).map (fun ω => toLp 2 (twoRemoteFirstJet L x y ω)) =
      multivariateGaussian (toLp 2 (twoRemotePosteriorMean L r x y t))
        (twoRemoteResidualCovariance L r x y) := by
  have hp : Measurable (rawPosteriorSample hL r t) :=
    (rawPosteriorSample_measurable hL r).comp (measurable_const.prodMk measurable_id)
  have hj : Measurable (fun ω => toLp 2 (twoRemoteFirstJet L x y ω)) :=
    (by fun_prop : Measurable (fun v : Fin 6 → ℝ => toLp 2 v)).comp (observation_measurable hL x y)
  rw [rawPinKernel_apply,Measure.map_map hj hp]
  exact (I4SourceEndpointParameters.finiteGaussian_law_parameters
    (posterior_hasGaussianLaw hL r x y t) _ (posterior_integral hL r x y t)
    _ (posterior_covariance hL r x y t)).2

/-- Qualified finite original-mode directions give positivity at the actual correction. -/
theorem twoRemoteResidualCovariance_posDef {L : ℝ} (hL : L ≠ 0) (r : ℝ) (x y : Fin 2 → ℝ)
    (hxM : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hxS : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hyM : I4Torus.torusProjection 2 L y ≠ I4Torus.torusProjection 2 L (endpointM r))
    (hyS : I4Torus.torusProjection 2 L y ≠ I4Torus.torusProjection 2 L (endpointS r))
    (hxy : I4Torus.torusProjection 2 L x ≠ I4Torus.torusProjection 2 L y) :
    (twoRemoteResidualCovariance L r x y).PosDef :=
  actual_twoRemoteFirstJet_residual_coefficientGram_posDef hL r x y hxM hxS hyM hyS hxy
    (twoRemoteRegressionMatrix L r x y)

end I4SourceTwoRemoteFirstJetGaussian
