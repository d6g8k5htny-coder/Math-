import SourceCurvatureDecomposition

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceGaussian I4SourceCovariance
open I4SourceDerivativeGaussian I4SourceDerivativeContinuity I4SourceConfluentPins
open I4SourceConfluentLimits I4ContactCoefficientLimits I4SourceEndpointRegression
open I4SourceContact I4SourceSmoothConditional I4SourceConditionalMajorant I4ContactGram
open I4GaussianRegressionLimits I4SourceEndpointEstimates MeasureTheory ProbabilityTheory Matrix Filter
open scoped BigOperators Topology NNReal
set_option autoImplicit false
namespace I4SourceCurvatureDecomposition

def regularizedCurvatureCross (L r : ℝ) (i : Fin 6) : ℝ :=
  ∑' m, curvatureCoefficient L m * regularizedPinCoefficient L r i m

theorem regularizedCurvatureCross_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (regularizedCurvatureCross L) := by
  apply continuous_pi
  intro i
  apply continuous_tsum
  · intro m
    exact continuous_const.mul (regularizedPinCoefficient_continuous hL i m)
  · exact coefficient_product_summable (curvatureCoefficient_summable hL).norm
      (confluentModeMajorant_summable hL)
  · intro m r
    rw [norm_mul]
    exact mul_le_mul_of_nonneg_left (regularizedPinCoefficient_bound hL r i m) (norm_nonneg _)

theorem regularizedCurvatureCross_zero {L : ℝ} (hL : L ≠ 0) :
    regularizedCurvatureCross L 0 = sourceContactCross L := by
  funext i
  unfold regularizedCurvatureCross
  simp_rw [regularizedPinCoefficient_zero]
  change (∑' m, sourceContactCoefficient L 6 m * sourceContactCoefficient L i.castSucc m) =
    sourceContactCovariance L i.castSucc 6
  rw [sourceContactCovariance_eq_coefficientGram hL]
  change (∑' m, _) = ∑' m, _
  exact tsum_congr (fun m => mul_comm _ _)

theorem curvatureCross_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (curvatureCross L) (𝓝[>] (0 : ℝ)) (𝓝 (sourceContactCross L)) := by
  have h := (regularizedCurvatureCross_continuous hL).tendsto 0
  rw [regularizedCurvatureCross_zero hL] at h
  apply (h.mono_left nhdsWithin_le_nhds).congr'
  filter_upwards [self_mem_nhdsWithin] with r hr
  funext i
  rw [curvatureCross_coefficient hL]
  unfold regularizedCurvatureCross
  apply tsum_congr
  intro m
  rw [pinCoefficient_eq_regularized L r (ne_of_gt hr) i m]


theorem curvaturePinInverse_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (fun r => (sourcePinCovarianceAt L r)⁻¹) (𝓝[>] (0 : ℝ))
      (𝓝 (sourcePinCovariance L)⁻¹) := by
  have hunit := sourcePinCovariance_isUnit hL
  have hdet0 : (sourcePinCovariance L).det ≠ 0 :=
    ((Matrix.isUnit_iff_isUnit_det _).mp hunit).ne_zero
  have hc : ContinuousAt (Ring.inverse : ℝ → ℝ) (sourcePinCovariance L).det := by
    simpa only [Ring.inverse_eq_inv'] using (continuousAt_inv₀ hdet0)
  exact (continuousAt_matrix_inv (sourcePinCovariance L) hc).tendsto.comp
    (sourcePinCovarianceAt_tendsto hL)

theorem curvatureBeta_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (curvatureBeta L) (𝓝[>] (0 : ℝ))
      (𝓝 (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹)) := by
  have hC := curvatureCross_tendsto hL
  have hG := curvaturePinInverse_tendsto hL
  apply tendsto_pi_nhds.mpr
  intro i
  change Tendsto (fun r => ∑ j, curvatureCross L r j * (sourcePinCovarianceAt L r)⁻¹ j i)
    (𝓝[>] (0 : ℝ)) (𝓝 (∑ j, sourceContactCross L j * (sourcePinCovariance L)⁻¹ j i))
  apply tendsto_finsetSum
  intro j _
  exact (((continuous_apply j).tendsto _).comp hC).mul
    (((continuous_apply i).tendsto _).comp (((continuous_apply j).tendsto _).comp hG))

theorem curvatureVariance_tendsto {L : ℝ} (hL : L ≠ 0) :
    Tendsto (curvatureVariance L) (𝓝[>] (0 : ℝ)) (𝓝 (sourceContactSchur L)) := by
  have hb := curvatureBeta_tendsto hL
  have hC := curvatureCross_tendsto hL
  have hdot : Tendsto (fun r => curvatureBeta L r ⬝ᵥ curvatureCross L r) (𝓝[>] (0 : ℝ))
      (𝓝 ((sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ sourceContactCross L)) := by
    apply tendsto_finsetSum
    intro i _
    exact (((continuous_apply i).tendsto _).comp hb).mul
      (((continuous_apply i).tendsto _).comp hC)
  have h : Tendsto (curvatureVariance L) (𝓝[>] (0 : ℝ))
      (𝓝 (Var[sourceContactQ L; smoothLaw 2 L] -
        (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ sourceContactCross L)) :=
    tendsto_const_nhds.sub hdot
  have heq : Var[sourceContactQ L; smoothLaw 2 L] -
      (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ sourceContactCross L =
      sourceContactSchur L := by
    rw [← Matrix.dotProduct_mulVec]
    unfold sourceContactSchur
    rw [sourceContactQVariance_eq_variance hL]
    rfl
  exact heq ▸ h

theorem curvatureMean_prescribed_tendsto {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    Tendsto (fun r => curvatureMean L r (sourcePrescribedPins r b)) (𝓝[>] (0 : ℝ))
      (𝓝 ((sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) ⬝ᵥ
        ![b,0,0,0,0,2])) := by
  have hb := curvatureBeta_tendsto hL
  have hd := sourcePrescribedPins_tendsto b
  change Tendsto (fun r => ∑ i, curvatureBeta L r i * sourcePrescribedPins r b i)
    (𝓝[>] (0 : ℝ)) (𝓝 (∑ i, (sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹) i *
      (![b,0,0,0,0,2] : Fin 6 → ℝ) i))
  apply tendsto_finsetSum
  intro i _
  exact (((continuous_apply i).tendsto _).comp hb).mul
    (((continuous_apply i).tendsto _).comp hd)


theorem curvature_uniform_parameter_bounds {L : ℝ} (hL : L ≠ 0) (b : ℝ) :
    ∃ B M δ : ℝ, 0 ≤ B ∧ 0 ≤ M ∧ 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        IsUnit (sourcePinCovarianceAt L r) ∧
        sourceContactSchur L / 2 ≤ curvatureVariance L r ∧
        (∀ i, |curvatureBeta L r i| ≤ B) ∧
        |curvatureMean L r (sourcePrescribedPins r b)| ≤ M := by
  let β0 := sourceContactCross L ᵥ* (sourcePinCovariance L)⁻¹
  let m0 := β0 ⬝ᵥ (![b,0,0,0,0,2] : Fin 6 → ℝ)
  let B := ‖β0‖ + 1
  let M := |m0| + 1
  have hτ : ∀ᶠ r in 𝓝[>] (0 : ℝ), sourceContactSchur L/2 < curvatureVariance L r := by
    apply (curvatureVariance_tendsto hL).eventually
    exact lt_mem_nhds (by linarith [sourceContactSchur_pos hL])
  have hβ : ∀ᶠ r in 𝓝[>] (0 : ℝ), ‖curvatureBeta L r‖ < B :=
    (curvatureBeta_tendsto hL).norm.eventually (gt_mem_nhds (by dsimp [B]; linarith))
  have hm : ∀ᶠ r in 𝓝[>] (0 : ℝ), |curvatureMean L r (sourcePrescribedPins r b)| < M := by
    simpa only [Real.norm_eq_abs] using (curvatureMean_prescribed_tendsto hL b).norm.eventually
      (gt_mem_nhds (by dsimp [M]; linarith))
  have hu := (sourceEndpoint_parameter_limits hL b).1
  have hall : ∀ᶠ r in 𝓝[>] (0 : ℝ),
      IsUnit (sourcePinCovarianceAt L r) ∧
      sourceContactSchur L/2 < curvatureVariance L r ∧
      ‖curvatureBeta L r‖ < B ∧ |curvatureMean L r (sourcePrescribedPins r b)| < M := by
    filter_upwards [hu,hτ,hβ,hm] with r hr ht hb hm
    exact ⟨hr,ht,hb,hm⟩
  obtain ⟨δ,hδ,hbound⟩ := mem_nhdsGT_iff_exists_Ioo_subset.mp hall
  refine ⟨B,M,min δ 1,by dsimp [B]; positivity,by dsimp [M]; positivity,
    lt_min hδ (by norm_num),min_le_right _ _,?_⟩
  intro r hr hrδ
  obtain ⟨hunit,ht,hbeta,hmean⟩ := hbound ⟨hr,lt_of_lt_of_le hrδ (min_le_left _ _)⟩
  refine ⟨hunit,ht.le,?_,hmean.le⟩
  intro i
  exact (show |curvatureBeta L r i| ≤ ‖curvatureBeta L r‖ by
    simpa only [Real.norm_eq_abs] using norm_le_pi_norm (curvatureBeta L r) i).trans hbeta.le

end I4SourceCurvatureDecomposition
