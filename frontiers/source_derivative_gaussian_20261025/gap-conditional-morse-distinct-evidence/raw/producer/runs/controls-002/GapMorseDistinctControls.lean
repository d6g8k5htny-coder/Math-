import SourceGapConditionalMorseDistinct
import FreeCoordinateControls
import SourceActualFoldCandidate
import Mathlib.Topology.Algebra.Module.ContinuousLinearMap.Invertible
import Mathlib.Analysis.Normed.Operator.Banach
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.FDeriv.Pi


/- Complete Controls-only text59C. One ordinary scratch integration.
No production-private calls. No independent helper execution was performed.
Positive Controls qualification, not the production kernel, covers this text. -/

noncomputable section
set_option autoImplicit false

open I4Foundation I4Weights I4Source I4SmoothCarrier I4SourceGaussian
open I4SourceDerivativeGaussian I4SourceConfluentPins I4SourceConfluentLimits
open I4SourceRawPinConditioning I4SourceSmoothConditional I4SourceFinitePinKernel
open I4SourceRawPinFreeCoordinates I4SourceCompactTargetMoments
open I4ActualSourceMorse I4SourceActualFoldCandidate I4LifetimeField
open UniversalLaw.Spec.Lifetime FreeCoordinateControls MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Topology

namespace GapMorseDistinctControls

abbrev Control59Point := Fin 2 → ℝ

def control59_a0 : ℝ := control57_AA * control57_AB / control57_DAB
def control59_a1 : ℝ := control57_AC * control57_AD / control57_DCD

theorem control59_a0_pos : 0 < control59_a0 :=
  div_pos (mul_pos (control57_amplitude_pos 0) (control57_amplitude_pos 1))
    control57_DAB_pos

theorem control59_a1_pos : 0 < control59_a1 :=
  div_pos (mul_pos (control57_amplitude_pos 2) (control57_amplitude_pos 3))
    control57_DCD_pos

def control59_omega0 : SmoothSample 2 2 :=
  finiteShiftSample control57_chi0 (zeroSample 2 2)

def control59_omegaChi1 : SmoothSample 2 2 :=
  finiteShiftSample control57_chi1 (zeroSample 2 2)

def control59_phi0 : Control59Point → ℝ := smoothSourceField 2 2 control59_omega0
def control59_phi1 : Control59Point → ℝ := smoothSourceField 2 2 control59_omegaChi1

theorem control59_omega0_rawPins : rawPins 2 0 control59_omega0 = 0 := by
  rw [control59_omega0, rawPins_finiteShiftSample (by norm_num), control57_zero_rawPins]
  ext i
  simpa [control57_chi] using control57_chi_raw_kernel i 0

theorem control59_omega0_posterior :
    rawPosteriorSample (by norm_num : (2 : ℝ) ≠ 0) 0 0 control59_omega0 =
      control59_omega0 := by
  rw [control59_omega0, rawPosteriorSample_finiteShiftSample (by norm_num) 0 0
    control57_chi0 (fun i => by simpa [control57_chi] using control57_chi_raw_kernel i 0),
    control57_zero_posterior]

theorem control59_finite_field (v : SourceMode 2 →₀ ℝ) (y : Control59Point) :
    smoothSourceField 2 2 (finiteShiftSample v (zeroSample 2 2)) y =
      finitePairing (fun m => modeCoefficient 2 2 m y) v := by
  simpa only [smoothSourceField, sourceField, scalarSeries, sampleInclusion,
    finiteShiftSample_val, zeroSample, zero_add] using
      (control57_pairing_hasSum (fun m => modeCoefficient 2 2 m y) v).tsum_eq

theorem control59_mode_spatial (s : Fin 4) (y : Control59Point) :
    modeCoefficient 2 2 (control57_mode s) y =
      control57_amplitude s * Real.cos (phase 2 2 (control57_frequency s) y) := by
  simp [control57_mode, control57_amplitude, modeCoefficient, phase]

theorem control59_four_mode_spatial (s : Fin 4) (y : Control59Point) :
    modeCoefficient 2 2 (control57_mode s) y =
      ![control57_AA * Real.cos (Real.pi * y 0),
        control57_AB * Real.cos (2 * Real.pi * y 0),
        control57_AC * Real.cos (Real.pi * y 1),
        control57_AD * Real.cos (2 * Real.pi * y 1)] s := by
  rw [control59_mode_spatial]
  have hp : phase 2 2 (control57_frequency s) y =
      ![Real.pi * y 0,2 * Real.pi * y 0,Real.pi * y 1,2 * Real.pi * y 1] s := by
    fin_cases s <;>
      simp [control57_frequency,phase,sourceC,Fin.sum_univ_two] <;> ring_nf <;> simp
  rw [hp]
  fin_cases s <;> rfl

theorem control59_phi0_formula (y : Control59Point) :
    control59_phi0 y = control59_a0 *
      (Real.cos (Real.pi * y 0) - Real.cos (2 * Real.pi * y 0)) := by
  rw [control59_phi0, control59_omega0, control59_finite_field,
    control57_chi0, control57_pairing_add_right,
    control57_pairing_single, control57_pairing_single]
  have hA := control59_four_mode_spatial 0 y
  have hB := control59_four_mode_spatial 1 y
  norm_num only [Matrix.cons_val_zero,Matrix.cons_val_one] at hA hB
  simp only [control57_mA, control57_mB] at *
  rw [hA,hB]
  dsimp [control59_a0]
  ring

theorem control59_phi1_formula (y : Control59Point) :
    control59_phi1 y = control59_a1 *
      (Real.cos (Real.pi * y 1) - Real.cos (2 * Real.pi * y 1)) := by
  rw [control59_phi1, control59_omegaChi1, control59_finite_field,
    control57_chi1, control57_pairing_add_right,
    control57_pairing_single, control57_pairing_single]
  have hC := control59_four_mode_spatial 2 y
  have hD := control59_four_mode_spatial 3 y
  norm_num at hC hD
  simp only [control57_mC, control57_mD] at *
  rw [hC,hD]
  dsimp [control59_a1]
  ring

def control59_wave (a : ℝ) (j : Fin 2) (y : Control59Point) : ℝ :=
  a * (Real.cos (Real.pi * y j) - Real.cos (2 * Real.pi * y j))

def control59_slope (a : ℝ) (j : Fin 2) (y : Control59Point) : ℝ :=
  a * (-Real.pi * Real.sin (Real.pi * y j) +
    2 * Real.pi * Real.sin (2 * Real.pi * y j))

def control59_slopeD (a : ℝ) (j : Fin 2) (y : Control59Point) : ℝ :=
  a * (-Real.pi ^ 2 * Real.cos (Real.pi * y j) +
    4 * Real.pi ^ 2 * Real.cos (2 * Real.pi * y j))

theorem control59_wave_hasFDerivAt (a : ℝ) (j : Fin 2) (y : Control59Point) :
    HasFDerivAt (control59_wave a j)
      (control59_slope a j y • (ContinuousLinearMap.proj j : Control59Point →L[ℝ] ℝ)) y := by
  have hp : HasFDerivAt (fun x : Control59Point => x j)
      (ContinuousLinearMap.proj j) y :=
    (ContinuousLinearMap.proj j : Control59Point →L[ℝ] ℝ).hasFDerivAt
  have h := (((hp.const_mul Real.pi).cos).sub
    ((hp.const_mul (2 * Real.pi)).cos)).const_mul a
  unfold control59_wave
  convert h using 1 <;> ext v <;> simp [control59_slope] <;> ring

theorem control59_slope_hasFDerivAt (a : ℝ) (j : Fin 2) (y : Control59Point) :
    HasFDerivAt (control59_slope a j)
      (control59_slopeD a j y • (ContinuousLinearMap.proj j : Control59Point →L[ℝ] ℝ)) y := by
  have hp : HasFDerivAt (fun x : Control59Point => x j)
      (ContinuousLinearMap.proj j) y :=
    (ContinuousLinearMap.proj j : Control59Point →L[ℝ] ℝ).hasFDerivAt
  have h := ((((hp.const_mul Real.pi).sin).const_mul (-Real.pi)).add
    (((hp.const_mul (2 * Real.pi)).sin).const_mul (2 * Real.pi))).const_mul a
  unfold control59_slope
  convert h using 1 <;> ext v <;> simp [control59_slopeD] <;> ring

theorem control59_phi0_gradient (y : Control59Point) :
    coordinateGradient control59_phi0 y = ![control59_slope control59_a0 0 y,0] := by
  have hf : control59_phi0 = control59_wave control59_a0 0 :=
    funext control59_phi0_formula
  rw [hf]
  ext j
  fin_cases j <;>
    simp [coordinateGradient, (control59_wave_hasFDerivAt control59_a0 0 y).fderiv]

theorem control59_phi1_gradient (y : Control59Point) :
    coordinateGradient control59_phi1 y = ![0,control59_slope control59_a1 1 y] := by
  have hf : control59_phi1 = control59_wave control59_a1 1 :=
    funext control59_phi1_formula
  rw [hf]
  ext j
  fin_cases j <;>
    simp [coordinateGradient, (control59_wave_hasFDerivAt control59_a1 1 y).fderiv]

def control59_axisMap (j : Fin 2) : Control59Point →L[ℝ] Control59Point :=
  (ContinuousLinearMap.proj j : Control59Point →L[ℝ] ℝ).smulRight (Pi.single j 1)

def control59_B (y : Control59Point) : Control59Point →L[ℝ] Control59Point :=
  (coordinateGradient control59_phi0 y 0) • control59_axisMap 0 +
    (coordinateGradient control59_phi1 y 1) • control59_axisMap 1

def control59_g (y : Control59Point) : Control59Point := coordinateGradient control59_phi0 y

def control59_theta (y : Control59Point) : Control59Point :=
  -(control59_B y).inverse (control59_g y)

def control59_xStar : Control59Point := ![1/2,1/2]
def control59_eX : Control59Point := ![1,0]
def control59_zStar : Control59Point := ![-1,0]

theorem control59_B_columns (y v : Control59Point) :
    control59_B y v = v 0 • coordinateGradient control59_phi0 y +
      v 1 • coordinateGradient control59_phi1 y := by
  rw [control59_B, control59_phi0_gradient, control59_phi1_gradient]
  ext j
  fin_cases j <;> simp [control59_axisMap] <;> ring

theorem control59_B_apply (y v : Control59Point) :
    control59_B y v =
      ![control59_slope control59_a0 0 y * v 0,
        control59_slope control59_a1 1 y * v 1] := by
  rw [control59_B_columns, control59_phi0_gradient, control59_phi1_gradient]
  ext j
  fin_cases j <;> simp <;> ring

theorem control59_B_analytic (y : Control59Point) :
    control59_B y = control59_slope control59_a0 0 y • control59_axisMap 0 +
      control59_slope control59_a1 1 y • control59_axisMap 1 := by
  simp [control59_B,control59_phi0_gradient,control59_phi1_gradient]

theorem control59_g_analytic (y : Control59Point) :
    control59_g y = control59_slope control59_a0 0 y • (Pi.single 0 1) := by
  rw [control59_g,control59_phi0_gradient]
  ext j
  fin_cases j <;> simp

theorem control59_g_hasFDerivAt (y : Control59Point) :
    HasFDerivAt control59_g
      ((control59_slopeD control59_a0 0 y •
        (ContinuousLinearMap.proj 0 : Control59Point →L[ℝ] ℝ)).smulRight (Pi.single 0 1)) y := by
  simpa only [← control59_g_analytic] using
    (control59_slope_hasFDerivAt control59_a0 0 y).smul_const
      (Pi.single 0 1 : Control59Point)

theorem control59_B_hasFDerivAt (y : Control59Point) :
    HasFDerivAt control59_B
      (((control59_slopeD control59_a0 0 y •
          (ContinuousLinearMap.proj 0 : Control59Point →L[ℝ] ℝ)).smulRight (control59_axisMap 0)) +
        ((control59_slopeD control59_a1 1 y •
          (ContinuousLinearMap.proj 1 : Control59Point →L[ℝ] ℝ)).smulRight (control59_axisMap 1))) y := by
  have h := ((control59_slope_hasFDerivAt control59_a0 0 y).smul_const
      (control59_axisMap 0)).add
    ((control59_slope_hasFDerivAt control59_a1 1 y).smul_const (control59_axisMap 1))
  simpa only [← control59_B_analytic] using h

theorem control59_center_slopes :
    control59_slope control59_a0 0 control59_xStar = -Real.pi * control59_a0 ∧
    control59_slope control59_a1 1 control59_xStar = -Real.pi * control59_a1 ∧
    control59_slopeD control59_a0 0 control59_xStar = -4 * Real.pi^2 * control59_a0 ∧
    control59_slopeD control59_a1 1 control59_xStar = -4 * Real.pi^2 * control59_a1 := by
  have hp : 2 * Real.pi * (1/2 : ℝ) = Real.pi := by ring
  have hh : Real.pi * (1/2 : ℝ)=Real.pi/2 := by ring
  refine ⟨?_,?_,?_,?_⟩ <;>
    dsimp only [control59_slope,control59_slopeD,control59_xStar,
      Matrix.cons_val_zero,Matrix.cons_val_one] <;>
    rw [hp,hh] <;> norm_num <;> ring

theorem control59_B_center_diagonal (v : Control59Point) :
    control59_B control59_xStar v =
      ![(-Real.pi * control59_a0) * v 0,(-Real.pi * control59_a1) * v 1] := by
  rw [control59_B_apply,control59_center_slopes.1,control59_center_slopes.2.1]

def control59_rankSet : Set Control59Point :=
  {y | control59_slope control59_a0 0 y ≠ 0 ∧ control59_slope control59_a1 1 y ≠ 0}

theorem control59_rankSet_open : IsOpen control59_rankSet := by
  have h0 : Continuous (control59_slope control59_a0 0) :=
    continuous_iff_continuousAt.mpr fun y =>
      (control59_slope_hasFDerivAt control59_a0 0 y).continuousAt
  have h1 : Continuous (control59_slope control59_a1 1) :=
    continuous_iff_continuousAt.mpr fun y =>
      (control59_slope_hasFDerivAt control59_a1 1 y).continuousAt
  exact (isOpen_ne_fun h0 continuous_const).inter (isOpen_ne_fun h1 continuous_const)

theorem control59_center_mem_rankSet : control59_xStar ∈ control59_rankSet := by
  constructor
  · rw [control59_center_slopes.1]
    exact mul_ne_zero (neg_ne_zero.mpr Real.pi_ne_zero) control59_a0_pos.ne'
  · rw [control59_center_slopes.2.1]
    exact mul_ne_zero (neg_ne_zero.mpr Real.pi_ne_zero) control59_a1_pos.ne'

theorem control59_B_bijective (y : Control59Point) (hy : y ∈ control59_rankSet) :
    Function.Bijective (control59_B y) := by
  constructor
  · intro v w hvw
    have h0 := congrFun hvw 0
    have h1 := congrFun hvw 1
    rw [control59_B_apply,control59_B_apply] at h0 h1
    ext j
    fin_cases j
    · exact mul_left_cancel₀ hy.1 (by simpa using h0)
    · exact mul_left_cancel₀ hy.2 (by simpa using h1)
  · intro w
    refine ⟨![w 0 / control59_slope control59_a0 0 y,
      w 1 / control59_slope control59_a1 1 y], ?_⟩
    rw [control59_B_apply]
    ext j
    fin_cases j
    · change control59_slope control59_a0 0 y * (w 0 / control59_slope control59_a0 0 y)=w 0
      field_simp [hy.1]
    · change control59_slope control59_a1 1 y * (w 1 / control59_slope control59_a1 1 y)=w 1
      field_simp [hy.2]

theorem control59_B_isInvertible (y : Control59Point) (hy : y ∈ control59_rankSet) :
    (control59_B y).IsInvertible := by
  let e := (LinearEquiv.ofBijective (control59_B y).toLinearMap
    (control59_B_bijective y hy)).toContinuousLinearEquiv
  refine ⟨e,?_⟩
  ext v j
  rfl

theorem control59_theta_on_rankSet (y : Control59Point) (hy : y ∈ control59_rankSet) :
    control59_theta y = control59_zStar := by
  have hg : control59_g y = control59_B y (![1,0] : Control59Point) := by
    rw [control59_g,control59_B_columns]
    simp
  rw [control59_theta,hg,(control59_B_isInvertible y hy).inverse_apply_self]
  ext j
  fin_cases j <;> norm_num [control59_zStar]

theorem control59_actual_rank_neighborhood :
    ∃ U : Set Control59Point, IsOpen U ∧ control59_xStar ∈ U ∧
      ∀ y ∈ U, Function.Bijective (control59_B y) ∧
        control59_theta y = control59_zStar :=
  ⟨control59_rankSet,control59_rankSet_open,control59_center_mem_rankSet,
    fun y hy => ⟨control59_B_bijective y hy,control59_theta_on_rankSet y hy⟩⟩

theorem control59_theta_center : control59_theta control59_xStar = control59_zStar :=
  control59_theta_on_rankSet _ control59_center_mem_rankSet

theorem control59_Dtheta_zero : fderiv ℝ control59_theta control59_xStar = 0 := by
  have he : control59_theta =ᶠ[nhds control59_xStar]
      (fun _ : Control59Point => control59_zStar) := by
    filter_upwards [control59_rankSet_open.mem_nhds control59_center_mem_rankSet] with y hy
    exact control59_theta_on_rankSet y hy
  rw [he.fderiv_eq]
  exact (hasFDerivAt_const (𝕜 := ℝ) _ _).fderiv

theorem control59_theta_hasFDerivAt_zero :
    HasFDerivAt control59_theta (0 : Control59Point →L[ℝ] Control59Point) control59_xStar := by
  have he : control59_theta =ᶠ[nhds control59_xStar]
      (fun _ : Control59Point => control59_zStar) := by
    filter_upwards [control59_rankSet_open.mem_nhds control59_center_mem_rankSet] with y hy
    exact control59_theta_on_rankSet y hy
  exact (hasFDerivAt_const control59_zStar control59_xStar).congr_of_eventuallyEq he

theorem control59_Dg_eX :
    fderiv ℝ control59_g control59_xStar control59_eX =
      ![-4 * Real.pi^2 * control59_a0,0] := by
  rw [(control59_g_hasFDerivAt control59_xStar).fderiv,
    control59_center_slopes.2.2.1]
  ext j
  fin_cases j <;> simp [control59_eX]

theorem control59_DB_eX_theta :
    fderiv ℝ control59_B control59_xStar control59_eX
      (control59_theta control59_xStar) = ![4 * Real.pi^2 * control59_a0,0] := by
  rw [(control59_B_hasFDerivAt control59_xStar).fderiv,control59_theta_center]
  have h := control59_center_slopes
  ext j
  fin_cases j <;>
    simp [control59_eX,control59_zStar,control59_axisMap,h.2.2.1,h.2.2.2]

theorem control59_full_normalEq_all (v : Control59Point) :
    fderiv ℝ control59_g control59_xStar v +
      fderiv ℝ control59_B control59_xStar v
        (control59_theta control59_xStar) +
      control59_B control59_xStar
        (fderiv ℝ control59_theta control59_xStar v) = 0 := by
  rw [(control59_g_hasFDerivAt control59_xStar).fderiv,
    (control59_B_hasFDerivAt control59_xStar).fderiv,
    control59_theta_center,control59_Dtheta_zero]
  ext j
  fin_cases j <;> simp [control59_axisMap,control59_zStar]

theorem control59_full_normalEq :
    fderiv ℝ control59_g control59_xStar control59_eX +
      fderiv ℝ control59_B control59_xStar control59_eX
        (control59_theta control59_xStar) +
      control59_B control59_xStar
        (fderiv ℝ control59_theta control59_xStar control59_eX) = 0 := by
  exact control59_full_normalEq_all control59_eX

theorem control59_fixed_parameter_gradient_zero (y : Control59Point) :
    control59_g y + control59_B y control59_zStar = 0 := by
  rw [control59_g,control59_B_columns]
  simp [control59_zStar]

theorem control59_fixed_parameter_Hshift_zero :
    fderiv ℝ (fun y => control59_g y + control59_B y control59_zStar)
      control59_xStar = 0 := by
  have he : (fun y => control59_g y + control59_B y control59_zStar) =
      (fun _ : Control59Point => (0 : Control59Point)) :=
    funext control59_fixed_parameter_gradient_zero
  rw [he]
  exact (hasFDerivAt_const (𝕜 := ℝ) _ _).fderiv

theorem control59_freeShift_cancel_actual :
    freeShiftSample control57_frame control59_zStar control59_omega0 = zeroSample 2 2 := by
  apply Subtype.ext
  funext m
  rw [control57_shift_val]
  simp [control59_omega0,control59_zStar,finiteShiftSample_val,zeroSample,
    Fin.sum_univ_two,control57_frame,control57_chi]

theorem control59_actual_shifted_field_zero :
    smoothSourceField 2 2
      (freeShiftSample control57_frame control59_zStar control59_omega0) =
        (fun _ : Control59Point => 0) := by
  rw [control59_freeShift_cancel_actual]
  funext y
  simp [smoothSourceField,sourceField,scalarSeries,sampleInclusion,zeroSample]

theorem control59_actual_shifted_Hessian_zero :
    fderiv ℝ (coordinateGradient (smoothSourceField 2 2
      (freeShiftSample control57_frame control59_zStar control59_omega0)))
        control59_xStar = 0 := by
  rw [control59_actual_shifted_field_zero]
  have hc : coordinateGradient (fun _ : Control59Point => (0 : ℝ)) =
      (fun _ : Control59Point => (0 : Control59Point)) := by
    funext y j
    change (fderiv ℝ (fun _ : Control59Point => (0 : ℝ)) y) (Pi.single j 1)=0
    rw [(hasFDerivAt_const (𝕜 := ℝ) (0 : ℝ) y).fderiv]
    rfl
  rw [hc]
  exact (hasFDerivAt_const (𝕜 := ℝ) (0 : Control59Point) control59_xStar).fderiv

theorem dropped_DBtheta_actual_counterexample :
    (control59_B control59_xStar
      (fderiv ℝ control59_theta control59_xStar control59_eX)) 0 ≠
      (-(fderiv ℝ control59_g control59_xStar control59_eX)) 0 := by
  rw [control59_Dtheta_zero,control59_Dg_eX]
  simp only [zero_apply,map_zero,Pi.zero_apply,Pi.neg_apply,
    Matrix.cons_val_zero,neg_mul,neg_neg]
  have hp : 0 < 4 * Real.pi^2 * control59_a0 := by
    have ha := control59_a0_pos
    positivity
  linarith

theorem dropped_DBtheta_eq_iff_false :
    ((control59_B control59_xStar
      (fderiv ℝ control59_theta control59_xStar control59_eX)) 0 =
      (-(fderiv ℝ control59_g control59_xStar control59_eX)) 0) ↔ False := by
  exact iff_false_intro dropped_DBtheta_actual_counterexample

/- New finite arithmetic control. These are the qualified actual finite
directions, with a nonorthogonal presentation, rather than abstract vectors. -/

def control59_nonorthogonal : Fin 2 → (SourceMode 2 →₀ ℝ) :=
  ![(2 : ℝ) • control57_chi0,control57_chi0 + (3 : ℝ) • control57_chi1]

theorem control59_pair_combo (a b c d : ℝ) :
    finitePairing (fun m => (a • control57_chi0 + b • control57_chi1) m)
      (c • control57_chi0 + d • control57_chi1) = a*c+b*d := by
  have h00 := control57_chi_gram 0 0
  have h01 := control57_chi_gram 0 1
  have h10 := control57_chi_gram 1 0
  have h11 := control57_chi_gram 1 1
  norm_num [control57_chi] at h00 h01 h10 h11
  simp only [control57_pairing_add_right,control57_pairing_smul_right,
    Finsupp.add_apply,Finsupp.smul_apply,smul_eq_mul,
    control57_pairing_add_left,control57_pairing_mul_left,h00,h01,h10,h11]
  ring

theorem control59_nonorthogonal_gram (i j : Fin 2) :
    finitePairing (fun m => control59_nonorthogonal i m)
      (control59_nonorthogonal j) = ![![4,2],![2,10]] i j := by
  fin_cases i <;> fin_cases j
  · convert control59_pair_combo 2 0 2 0 using 1 <;> norm_num [control59_nonorthogonal]
  · convert control59_pair_combo 2 0 1 3 using 1 <;> norm_num [control59_nonorthogonal]
  · convert control59_pair_combo 1 3 2 0 using 1 <;> norm_num [control59_nonorthogonal]
  · convert control59_pair_combo 1 3 1 3 using 1 <;> norm_num [control59_nonorthogonal]

theorem control59_nonorthogonal_raw_kernel (i : Fin 6) (j : Fin 2) :
    finitePairing (rawPinCoefficient 2 0 i) (control59_nonorthogonal j) = 0 := by
  have h0 : finitePairing (rawPinCoefficient 2 0 i) control57_chi0 = 0 := by
    simpa [control57_chi] using control57_chi_raw_kernel i 0
  have h1 : finitePairing (rawPinCoefficient 2 0 i) control57_chi1 = 0 := by
    simpa [control57_chi] using control57_chi_raw_kernel i 1
  fin_cases j <;>
    simp [control59_nonorthogonal,control57_pairing_add_right,
      control57_pairing_smul_right,h0,h1]

theorem control59_nonorthogonal_normalization :
    (1/2 : ℝ) • control59_nonorthogonal 0 = control57_chi0 ∧
      control59_nonorthogonal 1 - (1/2 : ℝ) • control59_nonorthogonal 0 =
        (3 : ℝ) • control57_chi1 ∧
      (1/3 : ℝ) • (control59_nonorthogonal 1 -
        (1/2 : ℝ) • control59_nonorthogonal 0) = control57_chi1 := by
  constructor
  · ext m
    simp [control59_nonorthogonal]
  constructor
  · ext m
    simp [control59_nonorthogonal]
  · ext m
    simp [control59_nonorthogonal]

/- Public59 positive specialization. The interval precedes the prescribed
radius; no target-dependent exceptional-law selection is introduced. -/

theorem control59_public_global_specialization :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ →
        ∀ᵐ ω ∂sourceGapLaw (by norm_num : (2 : ℝ) ≠ 0) r 3 1,
          IsMorseDistinct 2 2 (actualField 2 2 ω) := by
  obtain ⟨δ,hδ,hδ1,_hδL,hglobal⟩ :=
    I4SourceGapConditionalMorseDistinct.sourceGapLaw_ae_isMorseDistinct
      (by norm_num : (0 : ℝ) < 2)
  exact ⟨δ,hδ,hδ1,fun r hr hrδ => hglobal r hr hrδ 3 1 (by norm_num)⟩

/- Positive LIMIT control at zero gap. This theorem proves the actual
failure of the distinct-value clause on the literal two pinned points.
It is not a mutation and asserts no positive Gaussian mass for a sample. -/

theorem control59_equal_height_forced_pin_tie_limit :
    ∃ ε : ℝ, 0 < ε ∧ ε ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < ε → ∀ b : ℝ,
        ∀ᵐ ω ∂sourceGapLaw (by norm_num : (2 : ℝ) ≠ 0) r b 0,
          ¬ IsMorseDistinct 2 2 (actualField 2 2 ω) := by
  obtain ⟨K,ε,_hK,hε,hε1,hbound⟩ :=
    sourceInverse_target_uniform_bounds (by norm_num : (2 : ℝ) ≠ 0)
  refine ⟨ε,hε,hε1,?_⟩
  intro r hr hrε b
  have hG := (hbound r hr hrε).1
  have hpins : ∀ᵐ ω ∂sourceGapLaw (by norm_num : (2 : ℝ) ≠ 0) r b 0,
      rawPins 2 r ω = ![b,b-0*r^3,0,0,0,0] := by
    rw [sourceGapLaw_eq_rawPinKernel (by norm_num) r b 0 hr.ne']
    have hm : MeasurableSet {ω : SmoothSample 2 2 |
        rawPins 2 r ω = ![b,b-0*r^3,0,0,0,0]} :=
      measurableSet_eq_fun (rawPins_measurable (by norm_num) r) measurable_const
    apply (mem_ae_iff_prob_eq_one hm).2
    exact rawPinKernel_pin_fiber (by norm_num : (2 : ℝ) ≠ 0) r hr.ne'
      hG (![b,b-0*r^3,0,0,0,0] : Fin 6 → ℝ)
  filter_upwards [hpins] with ω hp
  intro hmd
  obtain ⟨hM,hS⟩ := actual_rawPins_critical (by norm_num : (0 : ℝ) < 2) ω hp
  obtain ⟨hvalM,hvalS,_⟩ := actual_rawPins_heights ω hp
  have hrL : r < (2 : ℝ)/2 := by linarith
  have hdist : 0 < torusDist 2 2 (endpointLiftM r) (endpointLiftS r) := by
    rw [endpoint_lifts_torusDist (by norm_num : (0 : ℝ) < 2) hr hrL]
    exact hr
  have hne := hmd.2 (endpointLiftM r) (endpointLiftS r) hM hS hdist
  apply hne
  change actualField 2 2 ω ((coordinates 2).symm (endpointM r))=
    actualField 2 2 ω ((coordinates 2).symm (endpointS r))
  rw [hvalM,hvalS]
  ring

end GapMorseDistinctControls
