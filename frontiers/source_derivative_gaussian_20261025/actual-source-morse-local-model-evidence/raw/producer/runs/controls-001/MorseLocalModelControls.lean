import SourceActualMorseLocalModel
import SourceFiniteTrig
import SourceActualFoldCandidate
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic


/- Complete ordinary Controls-only text60C, independent of all production
private names/proofs. Its positive Controls compilation supplies coverage;
the production kernel does not cover this separate section. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology
open Set MeasureTheory I4Foundation I4Source I4SmoothCarrier
  I4SourceSmoothConditional I4SourceFinitePinKernel I4SourceFiniteTrig
  I4LifetimeField UniversalLaw.Spec.Lifetime

namespace I4MorseLocalModelControls

abbrev ControlPoint := Fin 2 → ℝ
abbrev ControlPhysical := UniversalLaw.Spec.Lifetime.E 2

def minimumPoly : TrigPoly :=
  scale (-1) ([⟨1,Pi.single 0 1,0⟩] ++ [⟨1,Pi.single 1 1,0⟩])

def minimumSample : SmoothSample 2 2 :=
  finiteShiftSample (toSource 2 minimumPoly) (zeroSample 2 2)

def minimumField : ControlPhysical → ℝ := actualField 2 2 minimumSample

def cosineMinimum (q : ℝ) (x : ControlPoint) : ℝ :=
  -(Real.cos (q*x 0)+Real.cos (q*x 1))

theorem minimum_coordinate_field :
    smoothSourceField 2 2 minimumSample = cosineMinimum Real.pi := by
  classical
  funext x
  have hs : HasSum (fun m => modeCoefficient 2 2 m x * toSource 2 minimumPoly m)
      (finitePairing (fun m => modeCoefficient 2 2 m x) (toSource 2 minimumPoly)) := by
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    simp only [Finsupp.notMem_support_iff.mp hm,mul_zero]
  have he : smoothSourceField 2 2 minimumSample x =
      finitePairing (fun m => modeCoefficient 2 2 m x) (toSource 2 minimumPoly) := by
    simpa [minimumSample,smoothSourceField,sourceField,scalarSeries,sampleInclusion,
      finiteShiftSample_val,zeroSample] using hs.tsum_eq
  rw [he,toSource_eval (by norm_num : (2:ℝ) ≠ 0)]
  simp [minimumPoly,eval_scale,eval_append,eval,termEval,phase,
    I4Weights.sourceC,Fin.sum_univ_two,cosineMinimum] <;> ring

def controlProj (i : Fin 2) : ControlPoint →L[ℝ] ℝ := ContinuousLinearMap.proj i

def cosineMinimumDerivative (q : ℝ) (x : ControlPoint) : ControlPoint →L[ℝ] ℝ :=
  (q*Real.sin (q*x 0)) • controlProj 0 +
    (q*Real.sin (q*x 1)) • controlProj 1

theorem cosineMinimum_hasFDerivAt (q : ℝ) (x : ControlPoint) :
    HasFDerivAt (cosineMinimum q) (cosineMinimumDerivative q x) x := by
  have hx : HasFDerivAt (fun y : ControlPoint => q*y 0) (q • controlProj 0) x :=
    (controlProj 0).hasFDerivAt.const_mul q
  have hy : HasFDerivAt (fun y : ControlPoint => q*y 1) (q • controlProj 1) x :=
    (controlProj 1).hasFDerivAt.const_mul q
  have hh := (hx.cos.add hy.cos).neg
  unfold cosineMinimum
  convert hh using 1 <;> ext v <;> simp [cosineMinimumDerivative,controlProj] <;> ring

theorem cosineMinimumDerivative_hasFDerivAt_zero (q : ℝ) :
    HasFDerivAt (cosineMinimumDerivative q)
      (((q^2) • controlProj 0).smulRight (controlProj 0) +
        ((q^2) • controlProj 1).smulRight (controlProj 1)) 0 := by
  have hx : HasFDerivAt (fun y : ControlPoint => q*y 0) (q • controlProj 0) 0 :=
    (controlProj 0).hasFDerivAt.const_mul q
  have hy : HasFDerivAt (fun y : ControlPoint => q*y 1) (q • controlProj 1) 0 :=
    (controlProj 1).hasFDerivAt.const_mul q
  have hh := ((hx.sin.const_mul q).smul_const (controlProj 0)).add
    ((hy.sin.const_mul q).smul_const (controlProj 1))
  unfold cosineMinimumDerivative
  convert hh using 1 <;> ext v w <;> simp [controlProj] <;> ring

theorem cosineMinimum_second_zero (q : ℝ) (u v : ControlPoint) :
    iteratedFDeriv ℝ 2 (cosineMinimum q) 0 ![u,v] =
      q^2 * (u 0*v 0+u 1*v 1) := by
  rw [iteratedFDeriv_two_apply]
  have he : fderiv ℝ (cosineMinimum q) = cosineMinimumDerivative q :=
    funext fun x => (cosineMinimum_hasFDerivAt q x).fderiv
  rw [he,(cosineMinimumDerivative_hasFDerivAt_zero q).fderiv]
  simp [controlProj] <;> ring

theorem minimum_critical : IsCriticalPoint 2 minimumField 0 := by
  have hz : fderiv ℝ (smoothSourceField 2 2 minimumSample)
      (coordinates 2 (0:ControlPhysical)) = 0 := by
    rw [map_zero,minimum_coordinate_field,(cosineMinimum_hasFDerivAt Real.pi 0).fderiv]
    simp [cosineMinimumDerivative]
  apply I4SourceActualFoldCandidate.actual_critical_of_coordinate_pins (by norm_num)
  all_goals rw [hz]; rfl

theorem minimum_hessian (u v : ControlPhysical) :
    hessian 2 minimumField 0 u v = Real.pi^2 *
      (coordinates 2 u 0*coordinates 2 v 0+coordinates 2 u 1*coordinates 2 v 1) := by
  rw [minimumField,I4SourceActualFoldCandidate.actual_hessian_coordinates (by norm_num),
    map_zero,minimum_coordinate_field]
  exact cosineMinimum_second_zero _ _ _

theorem minimum_inertia : HessianHasInertia 2 minimumField 0 0 := by
  refine ⟨⊥,⊤,isCompl_bot_top,by simp,by simp [ControlPhysical,E],?_,?_⟩
  · intro v hv hv0
    exact (hv0 ((Submodule.mem_bot ℝ).mp hv)).elim
  · intro v _ hv
    have hn : coordinates 2 v 0 ≠ 0 ∨ coordinates 2 v 1 ≠ 0 := by
      by_contra! hh
      apply hv
      apply (coordinates 2).injective
      ext i
      fin_cases i <;> simp_all
    rw [minimum_hessian]
    have hp : 0 < (coordinates 2 v 0)^2+(coordinates 2 v 1)^2 := by
      rcases hn with hn|hn
      · exact add_pos_of_pos_of_nonneg (sq_pos_of_ne_zero hn) (sq_nonneg _)
      · exact add_pos_of_nonneg_of_pos (sq_nonneg _) (sq_pos_of_ne_zero hn)
    have hpi : 0 < Real.pi^2 := sq_pos_of_ne_zero Real.pi_ne_zero
    nlinarith

def minimumScale : ℝ := Real.sqrt 2 / Real.pi

theorem minimumScale_ne_zero : minimumScale ≠ 0 :=
  div_ne_zero (Real.sqrt_pos.mpr (by norm_num)).ne' Real.pi_ne_zero

def minimumScaleEquiv : ControlPoint ≃L[ℝ] ControlPoint :=
  ({ toFun := fun y => minimumScale • y
     invFun := fun y => minimumScale⁻¹ • y
     left_inv := by intro y; simp [smul_smul,minimumScale_ne_zero]
     right_inv := by intro y; simp [smul_smul,minimumScale_ne_zero]
     map_add' := by intro y z; exact smul_add _ _ _
     map_smul' := by intro a y; simp [smul_smul,mul_comm] } :
    ControlPoint ≃ₗ[ℝ] ControlPoint).toContinuousLinearEquiv

def minimumP : ControlPoint ≃L[ℝ] ControlPhysical :=
  minimumScaleEquiv.trans (coordinates 2).symm

theorem minimumP_coordinates (y : ControlPoint) :
    coordinates 2 (minimumP y) = minimumScale • y := by
  simp [minimumP,minimumScaleEquiv]

def normalizedMinimum (y : ControlPoint) : ℝ := minimumField (minimumP y)-minimumField 0

theorem normalizedMinimum_formula (y : ControlPoint) :
    normalizedMinimum y = cosineMinimum (Real.sqrt 2) y-cosineMinimum (Real.sqrt 2) 0 := by
  have hp (a : ℝ) : Real.pi*(minimumScale*a) = Real.sqrt 2*a := by
    unfold minimumScale
    field_simp [Real.pi_ne_zero]
  simp only [normalizedMinimum,minimumField,actualField,minimum_coordinate_field,
    minimumP_coordinates,map_zero,cosineMinimum,Pi.smul_apply,smul_eq_mul,hp]
  simp

theorem normalizedMinimum_fderiv :
    fderiv ℝ normalizedMinimum = cosineMinimumDerivative (Real.sqrt 2) := by
  funext x
  have hh := (cosineMinimum_hasFDerivAt (Real.sqrt 2) x).sub_const
    (cosineMinimum (Real.sqrt 2) 0)
  have hf : normalizedMinimum = fun y =>
      cosineMinimum (Real.sqrt 2) y-cosineMinimum (Real.sqrt 2) 0 :=
    funext normalizedMinimum_formula
  rw [hf]
  exact hh.fderiv

theorem normalizedMinimum_second_zero (u v : ControlPoint) :
    iteratedFDeriv ℝ 2 normalizedMinimum 0 ![u,v] = 2*(u 0*v 0+u 1*v 1) := by
  rw [iteratedFDeriv_two_apply,normalizedMinimum_fderiv,
    (cosineMinimumDerivative_hasFDerivAt_zero (Real.sqrt 2)).fderiv]
  simp [controlProj,Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)] <;> ring

def e0 : ControlPoint := Pi.single 0 1

/- Only the factor (1-t) differs. The actual field, P, normalized h,
point, directions, interval and measure are identical. -/
def correctTaylorEntry : ℝ := ∫ t : ℝ in (0:ℝ)..1,
  (1-t) * iteratedFDeriv ℝ 2 normalizedMinimum (t • (0:ControlPoint)) ![e0,e0]

def omittedTaylorEntry : ℝ := ∫ t : ℝ in (0:ℝ)..1,
  iteratedFDeriv ℝ 2 normalizedMinimum (t • (0:ControlPoint)) ![e0,e0]

theorem actual_normalized_entry_two (t : ℝ) :
    iteratedFDeriv ℝ 2 normalizedMinimum (t • (0:ControlPoint)) ![e0,e0] = 2 := by
  rw [smul_zero,normalizedMinimum_second_zero]
  norm_num [e0]

theorem correctTaylorEntry_eq_one : correctTaylorEntry = 1 := by
  unfold correctTaylorEntry
  simp_rw [actual_normalized_entry_two]
  have he : (fun t : ℝ => (1-t)*2) = fun t => 2-2*t := by
    funext t; ring
  rw [he,intervalIntegral.integral_sub
    (intervalIntegrable_const : IntervalIntegrable (fun _ : ℝ => (2:ℝ)) volume 0 1)
    (intervalIntegrable_id.const_mul 2),intervalIntegral.integral_const_mul]
  norm_num [integral_id]

theorem omittedTaylorEntry_eq_two : omittedTaylorEntry = 2 := by
  unfold omittedTaylorEntry
  simp_rw [actual_normalized_entry_two]
  norm_num

theorem omittedTaylorEntry_ne_one : omittedTaylorEntry ≠ 1 := by
  rw [omittedTaylorEntry_eq_two]
  norm_num

theorem actualMinimum_public_specialization :
    ∃ phi : OpenPartialHomeomorph ControlPhysical ControlPoint,
      (0:ControlPhysical) ∈ phi.source ∧ phi 0 = 0 ∧ (0:ControlPoint) ∈ phi.target ∧
      ContDiffOn ℝ 1 phi phi.source ∧ ContDiffOn ℝ 1 phi.symm phi.target ∧
      (∀ x ∈ phi.source, minimumField x = minimumField 0 +
        ∑ i : Fin 2, (phi x i)^2) ∧
      ∀ O : Set ControlPhysical, IsOpen O → (0:ControlPhysical) ∈ O →
        ∃ V : Set ControlPhysical, IsOpen V ∧ (0:ControlPhysical) ∈ V ∧
          V ⊆ O ∩ phi.source ∧ IsPathConnected (V ∩ {x | minimumField 0 ≤ minimumField x}) := by
  obtain ⟨_hj,phi,hphi⟩ :=
    I4SourceActualMorseLocalModel.actualSource_c1_quadratic_localModel
      (by norm_num : (0:ℝ)<2) minimumSample (0:ControlPhysical) 0
      minimum_critical minimum_inertia
  refine ⟨phi,?_⟩
  simpa only [Nat.not_lt_zero,if_false,one_mul] using hphi

end I4MorseLocalModelControls
