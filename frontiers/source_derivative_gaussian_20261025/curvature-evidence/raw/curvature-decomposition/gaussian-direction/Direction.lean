import SourceSmoothConditionalKernel

noncomputable section
open I4Foundation I4Source I4SmoothCarrier I4SourceGaussian I4SourceSmoothConditional
open MeasureTheory ProbabilityTheory
open scoped BigOperators
set_option autoImplicit false
namespace I4SourceCurvatureDecomposition

def unitDirection {L : ℝ} (χ : SourceMode 2 → ℝ) (ω : SmoothSample 2 L) : ℝ :=
  scalarSeries χ ω.val

def unitDirectionCoefficientResidual {L : ℝ} (χ : SourceMode 2 → ℝ)
    (ω : SmoothSample 2 L) (m : SourceMode 2) : ℝ :=
  ω.val m - χ m * unitDirection χ ω

theorem unitDirection_measurable {L : ℝ} (χ : SourceMode 2 → ℝ) :
    Measurable (unitDirection (L := L) χ) :=
  (scalarSeries_measurable χ).comp measurable_subtype_coe

theorem unitDirection_hasLaw {L : ℝ} (hL : L ≠ 0) (χ : SourceMode 2 → ℝ)
    (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1) :
    HasLaw (unitDirection (L := L) χ) (gaussianReal 0 1) (smoothLaw 2 L) where
  aemeasurable := (unitDirection_measurable χ).aemeasurable
  map_eq := by
    change (smoothLaw 2 L).map (fun ω => scalarSeries χ (sampleInclusion 2 L ω)) = _
    rw [observation_map_eq 2 hL _ (scalarSeries_measurable χ), scalarSeries_map_gaussian χ hχ, hnorm]
    norm_num

theorem unitDirection_coefficient_covariance {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (m : SourceMode 2) :
    covariance (unitDirection (L := L) χ) (fun ω : SmoothSample 2 L => ω.val m)
      (smoothLaw 2 L) = χ m := by
  change covariance (fun ω => scalarSeries χ (sampleInclusion 2 L ω))
    (fun ω => sampleInclusion 2 L ω m) (smoothLaw 2 L) = _
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable χ) (measurable_pi_apply m)]
  exact scalarSeries_coordinate_covariance χ hχ m

theorem unitDirectionCoefficientResidual_zero_covariance {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1)
    (m : SourceMode 2) :
    covariance (unitDirection (L := L) χ) (fun ω => unitDirectionCoefficientResidual χ ω m)
      (smoothLaw 2 L) = 0 := by
  have hZ := unitDirection_hasLaw hL χ hχ hnorm
  have hZG := hZ.hasGaussianLaw
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  have hvar : Var[unitDirection (L := L) χ; smoothLaw 2 L] = 1 := by
    rw [hZ.variance_eq, variance_id_gaussianReal]
    norm_num
  unfold unitDirectionCoefficientResidual
  rw [covariance_fun_sub_right hZG.memLp_two (coefficient_hasGaussianLaw hL m).memLp_two
    (hZG.memLp_two.const_mul (χ m)), covariance_const_mul_right,
    unitDirection_coefficient_covariance hL χ hχ m, covariance_self hZG.aemeasurable, hvar]
  ring

theorem unitDirection_finiteCoefficients_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      ((fun _ : Fin 1 => unitDirection χ ω), fun m : I => ω.val m)) (smoothLaw 2 L) := by
  classical
  let q : (Fin 1 ⊕ I) → SourceMode 2 → ℝ :=
    Sum.elim (fun _ => χ) (fun m => Pi.single m.val 1)
  have hq (j : Fin 1 ⊕ I) : Summable (q j) := by
    cases j with
    | inl i => exact hχ
    | inr m =>
      apply summable_of_ne_finset_zero (s := {m.val})
      intro n hn
      simp only [Finset.mem_singleton] at hn
      simp [q, hn]
  have hG := scalarSeries_finite_hasGaussianLaw q hq
  have hm : Measurable (fun η j => scalarSeries (q j) η) :=
    Measurable.of_eval (fun j => scalarSeries_measurable (q j))
  have hμ : HasGaussianLaw (fun ω : SmoothSample 2 L =>
      fun j => scalarSeries (q j) (sampleInclusion 2 L ω)) (smoothLaw 2 L) := by
    refine ⟨(hm.comp (sampleInclusion_measurable 2 L)).aemeasurable, ?_⟩
    rw [observation_map_eq 2 hL _ hm]
    exact hG.isGaussian_map
  let A : ((Fin 1 ⊕ I) → ℝ) →L[ℝ] ((Fin 1 → ℝ) × (I → ℝ)) :=
    (ContinuousLinearMap.pi (fun i => ContinuousLinearMap.proj (Sum.inl i))).prod
      (ContinuousLinearMap.pi (fun m => ContinuousLinearMap.proj (Sum.inr m)))
  apply (hμ.map_fun A).congr
  filter_upwards with ω
  apply Prod.ext
  · rfl
  · funext m
    exact scalarSeries_single m.val ω.val

def finiteDirectionLift (χ : SourceMode 2 → ℝ) (I : Finset (SourceMode 2)) :
    (Fin 1 → ℝ) →L[ℝ] (I → ℝ) :=
  ContinuousLinearMap.pi (fun m => χ m.val • ContinuousLinearMap.proj 0)

lemma finiteDirectionLift_apply (χ : SourceMode 2 → ℝ) (I : Finset (SourceMode 2))
    (z : Fin 1 → ℝ) (m : I) : finiteDirectionLift χ I z m = χ m.val * z 0 := rfl

theorem unitDirection_finiteResidual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      ((fun _ : Fin 1 => unitDirection χ ω), fun m : I => unitDirectionCoefficientResidual χ ω m.val))
      (smoothLaw 2 L) := by
  let A : ((Fin 1 → ℝ) × (I → ℝ)) →L[ℝ] ((Fin 1 → ℝ) × (I → ℝ)) :=
    (ContinuousLinearMap.fst ℝ (Fin 1 → ℝ) (I → ℝ)).prod
      (ContinuousLinearMap.snd ℝ (Fin 1 → ℝ) (I → ℝ) -
        (finiteDirectionLift χ I).comp (ContinuousLinearMap.fst ℝ (Fin 1 → ℝ) (I → ℝ)))
  apply ((unitDirection_finiteCoefficients_hasGaussianLaw hL χ hχ I).map_fun A).congr
  filter_upwards with ω
  apply Prod.ext
  · rfl
  · rfl

theorem unitDirection_scalar_finiteResidual_hasGaussianLaw {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (I : Finset (SourceMode 2)) :
    HasGaussianLaw (fun ω : SmoothSample 2 L =>
      (unitDirection χ ω, fun m : I => unitDirectionCoefficientResidual χ ω m.val))
      (smoothLaw 2 L) := by
  let A : ((Fin 1 → ℝ) × (I → ℝ)) →L[ℝ] (ℝ × (I → ℝ)) :=
    ((ContinuousLinearMap.proj 0).comp (ContinuousLinearMap.fst ℝ (Fin 1 → ℝ) (I → ℝ))).prod
      (ContinuousLinearMap.snd ℝ (Fin 1 → ℝ) (I → ℝ))
  apply ((unitDirection_finiteResidual_hasGaussianLaw hL χ hχ I).map_fun A).congr
  filter_upwards with ω
  rfl

theorem unitDirectionCoefficientResidual_finite_indepFun {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1)
    (I : Finset (SourceMode 2)) :
    IndepFun (unitDirection (L := L) χ)
      (fun (ω : SmoothSample 2 L) (m : I) => unitDirectionCoefficientResidual χ ω m.val) (smoothLaw 2 L) := by
  have h := (unitDirection_finiteResidual_hasGaussianLaw hL χ hχ I).indepFun_of_covariance_eval
    (fun _ m => unitDirectionCoefficientResidual_zero_covariance hL χ hχ hnorm m.val)
  exact h.comp (show Measurable (fun z : Fin 1 → ℝ => z 0) by fun_prop) measurable_id

theorem unitDirectionCoefficientResidual_indepFun {L : ℝ} (hL : L ≠ 0)
    (χ : SourceMode 2 → ℝ) (hχ : Summable χ) (hnorm : (∑' m, χ m ^ 2) = 1) :
    IndepFun (unitDirection (L := L) χ) (fun ω m => unitDirectionCoefficientResidual χ ω m)
      (smoothLaw 2 L) := by
  have : IsProbabilityMeasure (smoothLaw 2 L) := smoothLaw_isProbabilityMeasure 2 hL
  apply IndepFun.indepFun_process (unitDirection_measurable χ)
  · intro m
    exact ((measurable_pi_apply m).comp measurable_subtype_coe).sub
      (measurable_const.mul (unitDirection_measurable χ))
  · exact unitDirectionCoefficientResidual_finite_indepFun hL χ hχ hnorm
end I4SourceCurvatureDecomposition
