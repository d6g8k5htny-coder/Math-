import Mathlib.Analysis.Calculus.ContDiff.FTaylorSeries
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.ContDiff.Basic
import SourceConfluentPins
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import SourceDerivativeContinuity
import SourceFiniteTrig
import SourceRemoteJetWitness
import SourceLifetimeGeometry
import SourceSmoothTopology
import ConfluentIntegralIdentities
import Mathlib.MeasureTheory.Integral.DominatedConvergence
import Mathlib.MeasureTheory.Integral.IntervalIntegral.DerivIntegrable
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

/-! Actual seven Peano rows in physical orthonormal frames on the unchanged
source carrier. The contact extension keeps the exact cubic factor six. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix Topology Interval
open I4Foundation I4Source I4Weights I4Smooth I4SmoothCarrier I4SourceGaussian
open I4SourceCovariance I4SourceDerivativeGaussian I4SourceDerivativeContinuity
open I4SourceFiniteTrig I4SourceFinitePinKernel I4SourceRemoteJetWitness I4SourceConfluentPins
open UniversalLaw.Spec.Lifetime I4LifetimeField
open MeasureTheory ProbabilityTheory WithLp Set

namespace I4SourceFramedConfluentCovariance

private def contactRows (f : (Fin 2 → ℝ) → ℝ) (p e n : Fin 2 → ℝ) : Fin 7 → ℝ :=
  ![f p,fderiv ℝ f p e,fderiv ℝ f p n,
    iteratedFDeriv ℝ 2 f p ![e,e],iteratedFDeriv ℝ 2 f p ![e,n],
    iteratedFDeriv ℝ 3 f p ![e,e,e],iteratedFDeriv ℝ 2 f p ![n,n] ]

private def peanoRows (f : (Fin 2 → ℝ) → ℝ) (p e n : Fin 2 → ℝ) (r : ℝ) : Fin 7 → ℝ :=
  ![(f (p-(r/2) • e)+f (p+(r/2) • e))/2,
    (fderiv ℝ f (p-(r/2) • e) e+fderiv ℝ f (p+(r/2) • e) e)/2,
    (fderiv ℝ f (p-(r/2) • e) n+fderiv ℝ f (p+(r/2) • e) n)/2,
    ∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f (p+(r*t) • e) ![e,e],
    ∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f (p+(r*t) • e) ![e,n],
    6*∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f (p+(r*t) • e) ![e,e,e],
    iteratedFDeriv ℝ 2 f p ![n,n] ]

private def pairCoefficient (L : ℝ) (z e n : E 2) (r : ℝ) : Fin 7 → SourceMode 2 → ℝ :=
  fun i m => peanoRows (modeCoefficient 2 L m) (coordinates 2 z)
    (coordinates 2 e) (coordinates 2 n) r i

/-- Actual original mode rows, including the ordinary mixed derivative and cubic factor six. -/
def framedConfluentCoefficient (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) : Fin 7 → SourceMode 2 → ℝ :=
  pairCoefficient L z (R 0) (R 1) r

/-- The literal finite series observation on the same original smooth carrier. -/
def framedConfluentVector (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (ω : SmoothSample 2 L) : Fin 7 → ℝ :=
  fun i => scalarSeries (framedConfluentCoefficient L z R r i) (sampleInclusion 2 L ω)

/-- Target-free Gram of the literal seven-row original coefficient family. -/
def framedConfluentCovariance (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) : Matrix (Fin 7) (Fin 7) ℝ :=
  I4ContactGram.coefficientGram (framedConfluentCoefficient L z R r)

private def pairCovariance (L : ℝ) (z e n : E 2) (r : ℝ) : Matrix (Fin 7) (Fin 7) ℝ :=
  I4ContactGram.coefficientGram (pairCoefficient L z e n r)

private def envelope (L : ℝ) (m : SourceMode 2) : ℝ :=
  8*∑ j : Fin 4, orderModeBound (j:ℕ) 2 L m

private theorem envelope_nonneg (L : ℝ) (m : SourceMode 2) : 0 ≤ envelope L m := by
  exact mul_nonneg (by norm_num) (Finset.sum_nonneg (fun j _ => orderModeBound_nonneg j 2 L m))

private theorem envelope_summable {L : ℝ} (hL : L ≠ 0) : Summable (envelope L) := by
  exact (summable_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 4))) =>
    orderModeBound_summable j 2 hL)).mul_left 8

private theorem envelope_weighted_summable {L : ℝ} (hL : L ≠ 0) (ell : ℕ) :
    Summable (fun m => orderModeBound ell 2 L m * envelope L m) :=
  I4ContactGram.coefficient_product_summable (orderModeBound_summable ell 2 hL)
    (envelope_summable hL)

private theorem envelope_square_summable {L : ℝ} (hL : L ≠ 0) :
    Summable (fun m => envelope L m*envelope L m) :=
  I4ContactGram.coefficient_product_summable (envelope_summable hL) (envelope_summable hL)

private theorem envelope_sample_summable {L : ℝ} (ω : SmoothSample 2 L) :
    Summable (fun m => envelope L m*|sampleInclusion 2 L ω m|) := by
  have h := (summable_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin 4))) => ω.property j)).mul_left 8
  simpa only [envelope,Finset.sum_mul,mul_assoc,sampleInclusion] using h


private def UniformContactLimit (L : ℝ) : Prop :=
  ∀ eps : ℝ, 0 < eps → ∃ delta : ℝ, 0 < delta ∧
    ∀ z : E 2, (∀ a : Fin 2, |coordinates 2 z a| ≤ |L|/2) →
      ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ,
        0 ≤ r → r ≤ delta → ∀ i j : Fin 7,
          |framedConfluentCovariance L z R r i j-framedConfluentCovariance L z R 0 i j| < eps

private def UniformCovarianceFloor (L : ℝ) : Prop :=
  ∃ gamma Lambda delta : ℝ, 0 < gamma ∧ 0 < Lambda ∧ 0 < delta ∧ delta ≤ 1 ∧ delta ≤ |L|/8 ∧
    ∀ z : E 2, (∀ a : Fin 2, |coordinates 2 z a| ≤ |L|/2) →
      ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ, 0 ≤ r → r ≤ delta →
        let G := framedConfluentCovariance L z R r
        let G6 : Matrix (Fin 6) (Fin 6) ℝ := fun i j => G (Fin.castAdd 1 i) (Fin.castAdd 1 j)
        (∀ v : Fin 7 → ℝ,
          gamma*(∑ i, (v i)^2) ≤ v ⬝ᵥ (G *ᵥ v) ∧
          v ⬝ᵥ (G *ᵥ v) ≤ Lambda*(∑ i, (v i)^2)) ∧
        G.PosDef ∧ G6.PosDef ∧ IsUnit G6 ∧
        gamma ≤ G 6 6-∑ i : Fin 6, ∑ j : Fin 6,
          G 6 (Fin.castAdd 1 i)*(G6⁻¹) i j*G (Fin.castAdd 1 j) 6

private theorem coordinates_norm_le_one (e : E 2) (he : ‖e‖ ≤ 1) :
    ‖coordinates 2 e‖ ≤ 1 := by
  apply (pi_norm_le_iff_of_nonneg (by norm_num : (0:ℝ) ≤ 1)).mpr
  intro i
  exact (PiLp.norm_apply_le e i).trans he

private theorem derivative_unit_bound {L : ℝ} (hL : L ≠ 0) (k : ℕ)
    (p : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) (hu : ∀ j, ‖u j‖ ≤ 1) (m : SourceMode 2) :
    |derivativeCoefficient 2 L k p u m| ≤ orderModeBound k 2 L m := by
  have hp : (∏ j, ‖u j‖) ≤ (1:ℝ) :=
    Finset.prod_le_one₀ (fun j _ => norm_nonneg _) (fun j _ => hu j)
  calc
    |derivativeCoefficient 2 L k p u m| ≤ derivativeMajorant 2 L k u m := by
      simpa only [Real.norm_eq_abs] using derivativeCoefficient_bound 2 hL k u m p
    _ ≤ orderModeBound k 2 L m*1 :=
      mul_le_mul_of_nonneg_left hp (orderModeBound_nonneg k 2 L m)
    _ = _ := mul_one _

private theorem average_abs_le (a b B : ℝ) (ha : |a| ≤ B) (hb : |b| ≤ B) :
    |(a+b)/2| ≤ B := by
  rw [abs_div,abs_of_pos (by norm_num : (0:ℝ)<2)]
  have hh := abs_add_le a b
  linarith

private theorem unit_interval_abs_le (g : ℝ → ℝ) (B : ℝ) (hg : ∀ t, |g t| ≤ B) :
    |∫ t in (-1/2:ℝ)..(1/2:ℝ), g t| ≤ B := by
  have h := intervalIntegral.norm_integral_le_of_norm_le_const
    (a:=(-1/2:ℝ)) (b:=(1/2:ℝ)) (C:=B) (f:=g)
    (fun t _ => by simpa only [Real.norm_eq_abs] using hg t)
  simpa only [Real.norm_eq_abs,show |(1/2:ℝ)-(-1/2)|=1 by norm_num,mul_one] using h

private theorem peano_interval_abs_le (g : ℝ → ℝ) (B : ℝ) (_hB : 0 ≤ B)
    (hg : ∀ t, |g t| ≤ B) :
    |∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*g t| ≤ B := by
  have h := intervalIntegral.norm_integral_le_of_norm_le_const
    (a:=(-1/2:ℝ)) (b:=(1/2:ℝ)) (C:=B) (f:=fun t => (1/4-t^2)*g t) (fun t ht => by
      rw [uIoc_of_le (by norm_num : (-1/2:ℝ) ≤ 1/2)] at ht
      have hprod := mul_nonneg (sub_nonneg.mpr ht.2) (sub_nonneg.mpr (le_of_lt ht.1))
      have hw0 : 0 ≤ (1/4:ℝ)-t^2 := by nlinarith
      have hw1 : (1/4:ℝ)-t^2 ≤ 1 := by nlinarith [sq_nonneg t]
      rw [Real.norm_eq_abs,abs_mul,abs_of_nonneg hw0]
      exact (mul_le_mul hw1 (hg t) (abs_nonneg _) (by norm_num : (0:ℝ)≤1)).trans_eq (one_mul B))
  simpa only [Real.norm_eq_abs,show |(1/2:ℝ)-(-1/2)|=1 by norm_num,mul_one] using h

private theorem pairCoefficient_bound {L : ℝ} (hL : L ≠ 0) (z e n : E 2) (r : ℝ)
    (he : ‖e‖ ≤ 1) (hn : ‖n‖ ≤ 1) (i : Fin 7) (m : SourceMode 2) :
    |pairCoefficient L z e n r i m| ≤ envelope L m := by
  let p := coordinates 2 z
  let a := coordinates 2 e
  let b := coordinates 2 n
  let f := modeCoefficient 2 L m
  have ha : ‖a‖ ≤ 1 := coordinates_norm_le_one e he
  have hb : ‖b‖ ≤ 1 := coordinates_norm_le_one n hn
  have hsum : 0 ≤ ∑ j : Fin 4, orderModeBound (j:ℕ) 2 L m :=
    Finset.sum_nonneg (fun j _ => orderModeBound_nonneg j 2 L m)
  have hle (j : Fin 4) : orderModeBound (j:ℕ) 2 L m ≤ ∑ j : Fin 4, orderModeBound (j:ℕ) 2 L m :=
    Finset.single_le_sum (f:=fun k : Fin 4 => orderModeBound (k:ℕ) 2 L m)
      (fun k _ => orderModeBound_nonneg (k:ℕ) 2 L m) (Finset.mem_univ j)
  have h0 (q : Fin 2 → ℝ) : |f q| ≤ orderModeBound 0 2 L m := by
    simpa only [derivativeCoefficient,iteratedFDeriv_zero_apply] using
      derivative_unit_bound hL 0 q (fun j => Fin.elim0 j) (fun j => Fin.elim0 j) m
  have h1 (q v : Fin 2 → ℝ) (hv : ‖v‖ ≤ 1) : |fderiv ℝ f q v| ≤ orderModeBound 1 2 L m := by
    simpa only [derivativeCoefficient,iteratedFDeriv_one_apply] using
      derivative_unit_bound hL 1 q (fun _ => v) (fun _ => hv) m
  have h2 (q v w : Fin 2 → ℝ) (hv : ‖v‖ ≤ 1) (hw : ‖w‖ ≤ 1) :
      |iteratedFDeriv ℝ 2 f q ![v,w]| ≤ orderModeBound 2 2 L m := by
    exact derivative_unit_bound hL 2 q ![v,w] (by intro j; fin_cases j <;> assumption) m
  have h3 (q : Fin 2 → ℝ) :
      |iteratedFDeriv ℝ 3 f q ![a,a,a]| ≤ orderModeBound 3 2 L m := by
    exact derivative_unit_bound hL 3 q ![a,a,a] (by intro j; fin_cases j <;> exact ha) m
  change |peanoRows f p a b r i| ≤ envelope L m
  fin_cases i
  · exact (average_abs_le _ _ _ (h0 _) (h0 _)).trans (by dsimp [envelope]; have hh:=hle 0; norm_num at hh; linarith)
  · exact (average_abs_le _ _ _ (h1 _ _ ha) (h1 _ _ ha)).trans (by dsimp [envelope]; have hh:=hle 1; norm_num at hh; linarith)
  · exact (average_abs_le _ _ _ (h1 _ _ hb) (h1 _ _ hb)).trans (by dsimp [envelope]; have hh:=hle 1; norm_num at hh; linarith)
  · exact (unit_interval_abs_le _ _ (fun t => h2 _ _ _ ha ha)).trans (by dsimp [envelope]; have hh:=hle 2; norm_num at hh; linarith)
  · exact (unit_interval_abs_le _ _ (fun t => h2 _ _ _ ha hb)).trans (by dsimp [envelope]; have hh:=hle 2; norm_num at hh; linarith)
  · change |6*∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f (p+(r*t) • a) ![a,a,a]| ≤ _
    rw [abs_mul,abs_of_pos (by norm_num : (0:ℝ)<6)]
    have hh := peano_interval_abs_le (fun t => iteratedFDeriv ℝ 3 f (p+(r*t) • a) ![a,a,a])
      (orderModeBound 3 2 L m) (orderModeBound_nonneg 3 2 L m) (fun t => h3 (p+(r*t) • a))
    have hle3 := hle 3
    dsimp [envelope]
    norm_num at hle3
    nlinarith
  · exact (h2 _ _ _ hb hb).trans (by dsimp [envelope]; have hh:=hle 2; norm_num at hh; linarith)


private theorem coefficient_summable {L : ℝ} (hL : L ≠ 0) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (i : Fin 7) :
    Summable (framedConfluentCoefficient L z R r i) := by
  apply (envelope_summable hL).of_norm_bounded
  intro m
  simpa only [Real.norm_eq_abs,framedConfluentCoefficient] using
    pairCoefficient_bound hL z (R 0) (R 1) r (R.norm_eq_one 0).le (R.norm_eq_one 1).le i m

private theorem vector_hasGaussianLaw {L : ℝ} (hL : L ≠ 0) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) :
    HasGaussianLaw (framedConfluentVector L z R r) (smoothLaw 2 L) := by
  have hm : Measurable (fun η j => scalarSeries (framedConfluentCoefficient L z R r j) η) :=
    Measurable.of_eval (fun _ => scalarSeries_measurable _)
  refine ⟨(hm.comp (sampleInclusion_measurable 2 L)).aemeasurable,?_⟩
  change IsGaussian ((smoothLaw 2 L).map (fun ω j =>
    scalarSeries (framedConfluentCoefficient L z R r j) (sampleInclusion 2 L ω)))
  rw [observation_map_eq 2 hL _ hm]
  exact (scalarSeries_finiteVector_hasGaussianLaw 7 _ (coefficient_summable hL z R r)).isGaussian_map

private theorem vector_covariance {L : ℝ} (hL : L ≠ 0) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (i j : Fin 7) :
    cov[fun ω => framedConfluentVector L z R r ω i,
      fun ω => framedConfluentVector L z R r ω j;smoothLaw 2 L] =
      framedConfluentCovariance L z R r i j := by
  unfold framedConfluentVector
  rw [covariance_comp_inclusion 2 hL _ _ (scalarSeries_measurable _) (scalarSeries_measurable _)]
  exact I4SourceCovariance.scalarSeries_covariance _ _
    (coefficient_summable hL z R r i) (coefficient_summable hL z R r j)

private theorem peanoRows_zero (f : (Fin 2 → ℝ) → ℝ) (p e n : Fin 2 → ℝ) :
    peanoRows f p e n 0 = contactRows f p e n := by
  have hw : (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)) = (1/6:ℝ) := by
    have hc : IntervalIntegrable (fun _ : ℝ => (1/4:ℝ)) volume (-1/2) (1/2) := intervalIntegrable_const
    have hp : IntervalIntegrable (fun t : ℝ => t^2) volume (-1/2) (1/2) :=
      (continuous_id.pow 2).intervalIntegrable _ _
    calc
      (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)) =
          (∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4:ℝ))-(∫ t in (-1/2:ℝ)..(1/2:ℝ), t^2) :=
        intervalIntegral.integral_sub hc hp
      _ = _ := by norm_num
  unfold peanoRows contactRows
  simp only [zero_div,zero_mul,zero_smul,sub_zero,add_zero]
  ext i
  fin_cases i
  · change (f p+f p)/2=f p
    ring
  · change (fderiv ℝ f p e+fderiv ℝ f p e)/2=fderiv ℝ f p e
    ring
  · change (fderiv ℝ f p n+fderiv ℝ f p n)/2=fderiv ℝ f p n
    ring
  · change (∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f p ![e,e]) = _
    norm_num
  · change (∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 f p ![e,n]) = _
    norm_num
  · change 6*(∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 f p ![e,e,e]) =
      iteratedFDeriv ℝ 3 f p ![e,e,e]
    rw [intervalIntegral.integral_mul_const,hw]
    ring
  · rfl

private theorem coefficient_contact (L : ℝ) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) :
    framedConfluentCoefficient L z R 0 = fun i m => contactRows (modeCoefficient 2 L m)
      (coordinates 2 z) (coordinates 2 (R 0)) (coordinates 2 (R 1)) i := by
  funext i m
  exact congrFun (peanoRows_zero _ _ _ _) i

private theorem physical_derivative {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (z : E 2) (u : Fin k → E 2) :
    iteratedFDeriv ℝ k (actualField 2 L ω) z u =
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) (coordinates 2 z)
        (fun i => coordinates 2 (u i)) := by
  have hh := (coordinates 2).toContinuousLinearMap.iteratedFDeriv_comp_right
    (smoothSourceField_smooth 2 hL ω) z (i:=k) (by simp)
  have hu := congrArg (fun T => T u) hh
  exact hu


private theorem derivative_peano_series {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (p e : Fin 2 → ℝ) (r : ℝ) (u : Fin k → (Fin 2 → ℝ))
    (w : ℝ → ℝ) (hw : Continuous w)
    (hw1 : ∀ t ∈ Ioc (-1/2:ℝ) (1/2:ℝ), |w t| ≤ 1) :
    scalarSeries (fun m => ∫ t in (-1/2:ℝ)..(1/2:ℝ),
      w t*derivativeCoefficient 2 L k (p+(r*t) • e) u m) (sampleInclusion 2 L ω) =
    ∫ t in (-1/2:ℝ)..(1/2:ℝ), w t*iteratedFDeriv ℝ k (smoothSourceField 2 L ω)
      (p+(r*t) • e) u := by
  let g : SourceMode 2 → ℝ → ℝ := fun m t =>
    w t*derivativeCoefficient 2 L k (p+(r*t) • e) u m*sampleInclusion 2 L ω m
  let C : SourceMode 2 → ℝ := fun m => derivativeMajorant 2 L k u m*|sampleInclusion 2 L ω m|
  have hC : Summable C := by
    have h := (ω.property k).mul_right (∏ j, ‖u j‖)
    convert h using 1
    funext m
    dsimp [C,derivativeMajorant,sampleInclusion]
    ring
  have hg (m : SourceMode 2) : Continuous (g m) :=
    (hw.mul ((derivativeCoefficient_continuous 2 L k u m).comp (by fun_prop))).mul continuous_const
  have hbound (m : SourceMode 2) (t : ℝ) (ht : t ∈ Ioc (-1/2:ℝ) (1/2:ℝ)) : ‖g m t‖ ≤ C m := by
    have hd : |derivativeCoefficient 2 L k (p+(r*t) • e) u m| ≤ derivativeMajorant 2 L k u m := by
      simpa only [Real.norm_eq_abs] using derivativeCoefficient_bound 2 hL k u m (p+(r*t) • e)
    dsimp [g,C]
    rw [abs_mul,abs_mul]
    have hh := mul_le_mul (hw1 t ht) hd (abs_nonneg _) (by norm_num : (0:ℝ)≤1)
    simpa only [one_mul] using mul_le_mul_of_nonneg_right hh (abs_nonneg (sampleInclusion 2 L ω m))
  have hInt (m : SourceMode 2) : Integrable (g m) (volume.restrict (Ioc (-1/2:ℝ) (1/2:ℝ))) :=
    ((hg m).intervalIntegrable (-1/2:ℝ) (1/2:ℝ)).1
  have hNorm : Summable (fun m => ∫ t, ‖g m t‖ ∂volume.restrict (Ioc (-1/2:ℝ) (1/2:ℝ))) := by
    apply hC.of_norm_bounded
    intro m
    have hh := intervalIntegral.norm_integral_le_of_norm_le_const
      (a:=(-1/2:ℝ)) (b:=(1/2:ℝ)) (C:=C m) (f:=fun t => ‖g m t‖) (fun t ht => by
        rw [uIoc_of_le (by norm_num : (-1/2:ℝ)≤1/2)] at ht
        simpa only [norm_norm] using hbound m t ht)
    rw [intervalIntegral.integral_of_le (by norm_num : (-1/2:ℝ)≤1/2)] at hh
    simpa only [show |(1/2:ℝ)-(-1/2)|=1 by norm_num,mul_one] using hh
  have hex := integral_tsum_of_summable_integral_norm hInt hNorm
  have hseries (t : ℝ) : (∑' m, g m t) =
      w t*iteratedFDeriv ℝ k (smoothSourceField 2 L ω) (p+(r*t) • e) u := by
    rw [smoothSourceField_derivative_series 2 hL ω]
    change (∑' m, w t*derivativeCoefficient 2 L k (p+(r*t) • e) u m*sampleInclusion 2 L ω m) =
      w t*(∑' m, derivativeCoefficient 2 L k (p+(r*t) • e) u m*sampleInclusion 2 L ω m)
    simp only [mul_assoc]
    exact tsum_mul_left
  calc
    scalarSeries (fun m => ∫ t in (-1/2:ℝ)..(1/2:ℝ),
        w t*derivativeCoefficient 2 L k (p+(r*t) • e) u m) (sampleInclusion 2 L ω) =
        ∑' m, ∫ t in (-1/2:ℝ)..(1/2:ℝ), g m t := by
      apply tsum_congr
      intro m
      dsimp [g]
      rw [intervalIntegral.integral_mul_const]
    _ = ∫ t in (-1/2:ℝ)..(1/2:ℝ), ∑' m, g m t := by
      simpa only [intervalIntegral.integral_of_le (by norm_num : (-1/2:ℝ)≤1/2)] using hex
    _ = _ := congrArg (fun f : ℝ → ℝ => ∫ t in (-1/2:ℝ)..(1/2:ℝ), f t) (funext hseries)


private theorem series_average (a b : SourceMode 2 → ℝ) (η : SourceMode 2 → ℝ)
    (ha : Summable (fun m => a m*η m)) (hb : Summable (fun m => b m*η m)) :
    scalarSeries (fun m => (a m+b m)/2) η = (scalarSeries a η+scalarSeries b η)/2 := by
  have hs := (ha.hasSum.add hb.hasSum).div_const 2
  have he : (fun m => (a m*η m+b m*η m)/2) = (fun m => ((a m+b m)/2)*η m) := by
    funext m
    ring
  rw [he] at hs
  exact hs.tsum_eq

private theorem series_const_mul (c : ℝ) (a : SourceMode 2 → ℝ) (η : SourceMode 2 → ℝ) :
    scalarSeries (fun m => c*a m) η = c*scalarSeries a η := by
  change (∑' m, (c*a m)*η m) = c*∑' m, a m*η m
  simp only [mul_assoc]
  exact tsum_mul_left

private theorem peano_weight_bound (t : ℝ) (ht : t ∈ Ioc (-1/2:ℝ) (1/2:ℝ)) :
    |(1/4:ℝ)-t^2| ≤ 1 := by
  have hprod := mul_nonneg (sub_nonneg.mpr ht.2) (sub_nonneg.mpr (le_of_lt ht.1))
  have hw0 : 0 ≤ (1/4:ℝ)-t^2 := by nlinarith
  rw [abs_of_nonneg hw0]
  nlinarith [sq_nonneg t]

private theorem peanoRows_series {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p e n : Fin 2 → ℝ) (r : ℝ) :
    (fun i => scalarSeries (fun m => peanoRows (modeCoefficient 2 L m) p e n r i)
      (sampleInclusion 2 L ω)) = peanoRows (smoothSourceField 2 L ω) p e n r := by
  have hs0 (q : Fin 2 → ℝ) :
      Summable (fun m => modeCoefficient 2 L m q*sampleInclusion 2 L ω m) := by
    simpa only [derivativeCoefficient,iteratedFDeriv_zero_apply] using
      I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 0 q (fun i => Fin.elim0 i)
  have hv0 (q : Fin 2 → ℝ) : scalarSeries (fun m => modeCoefficient 2 L m q)
      (sampleInclusion 2 L ω) = smoothSourceField 2 L ω q := by
    have he : derivativeCoefficient 2 L 0 q (fun i => Fin.elim0 i) =
        (fun m => modeCoefficient 2 L m q) := by
      funext m
      exact iteratedFDeriv_zero_apply _
    rw [← he]
    simpa only [iteratedFDeriv_zero_apply] using
      (smoothSourceField_derivative_series 2 hL ω 0 q (fun i => Fin.elim0 i)).symm
  have hs1 (q v : Fin 2 → ℝ) :
      Summable (fun m => fderiv ℝ (modeCoefficient 2 L m) q v*sampleInclusion 2 L ω m) := by
    simpa only [derivativeCoefficient,iteratedFDeriv_one_apply] using
      I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 1 q (fun _ => v)
  have hv1 (q v : Fin 2 → ℝ) : scalarSeries (fun m => fderiv ℝ (modeCoefficient 2 L m) q v)
      (sampleInclusion 2 L ω) = fderiv ℝ (smoothSourceField 2 L ω) q v := by
    have he : derivativeCoefficient 2 L 1 q (fun _ => v) =
        (fun m => fderiv ℝ (modeCoefficient 2 L m) q v) := by
      funext m
      exact iteratedFDeriv_one_apply _
    rw [← he]
    simpa only [iteratedFDeriv_one_apply] using
      (smoothSourceField_derivative_series 2 hL ω 1 q (fun _ => v)).symm
  ext i
  fin_cases i
  · change scalarSeries (fun m => (modeCoefficient 2 L m (p-(r/2) • e)+
      modeCoefficient 2 L m (p+(r/2) • e))/2) (sampleInclusion 2 L ω) = _
    rw [series_average _ _ _ (hs0 _) (hs0 _),hv0,hv0]
    rfl
  · change scalarSeries (fun m => (fderiv ℝ (modeCoefficient 2 L m) (p-(r/2) • e) e+
      fderiv ℝ (modeCoefficient 2 L m) (p+(r/2) • e) e)/2) (sampleInclusion 2 L ω) = _
    rw [series_average _ _ _ (hs1 _ _) (hs1 _ _),hv1,hv1]
    rfl
  · change scalarSeries (fun m => (fderiv ℝ (modeCoefficient 2 L m) (p-(r/2) • e) n+
      fderiv ℝ (modeCoefficient 2 L m) (p+(r/2) • e) n)/2) (sampleInclusion 2 L ω) = _
    rw [series_average _ _ _ (hs1 _ _) (hs1 _ _),hv1,hv1]
    rfl
  · change scalarSeries (fun m => ∫ t in (-1/2:ℝ)..(1/2:ℝ),
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p+(r*t) • e) ![e,e]) (sampleInclusion 2 L ω) =
      ∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (p+(r*t) • e) ![e,e]
    simpa only [derivativeCoefficient,one_mul] using
      derivative_peano_series hL ω 2 p e r ![e,e] (fun _ => 1) continuous_const (fun _ _ => by norm_num)
  · change scalarSeries (fun m => ∫ t in (-1/2:ℝ)..(1/2:ℝ),
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p+(r*t) • e) ![e,n]) (sampleInclusion 2 L ω) =
      ∫ t in (-1/2:ℝ)..(1/2:ℝ), iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (p+(r*t) • e) ![e,n]
    simpa only [derivativeCoefficient,one_mul] using
      derivative_peano_series hL ω 2 p e r ![e,n] (fun _ => 1) continuous_const (fun _ _ => by norm_num)
  · change scalarSeries (fun m => 6*∫ t in (-1/2:ℝ)..(1/2:ℝ),
      (1/4-t^2)*iteratedFDeriv ℝ 3 (modeCoefficient 2 L m) (p+(r*t) • e) ![e,e,e])
      (sampleInclusion 2 L ω) = _
    rw [series_const_mul]
    change 6*scalarSeries _ (sampleInclusion 2 L ω) =
      6*∫ t in (-1/2:ℝ)..(1/2:ℝ), (1/4-t^2)*iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω)
        (p+(r*t) • e) ![e,e,e]
    congr 1
    simpa only [derivativeCoefficient] using
      derivative_peano_series hL ω 3 p e r ![e,e,e] (fun t => 1/4-t^2) (by fun_prop) peano_weight_bound
  · exact (smoothSourceField_derivative_series 2 hL ω 2 p ![n,n]).symm

private theorem vector_peano {L : ℝ} (hL : L ≠ 0) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) (ω : SmoothSample 2 L) :
    framedConfluentVector L z R r ω = peanoRows (smoothSourceField 2 L ω)
      (coordinates 2 z) (coordinates 2 (R 0)) (coordinates 2 (R 1)) r :=
  peanoRows_series hL ω _ _ _ r

private theorem mode_smooth (L : ℝ) (m : SourceMode 2) :
    ContDiff ℝ (⊤ : ℕ∞) (modeCoefficient 2 L m) :=
  contDiff_infty.mpr (fun k => I4SourceSmoothTopology.modeCoefficient_contDiff 2 L m k)

end I4SourceFramedConfluentCovariance

-- INTEGRATED_CONTACT_BEGIN
/- Text-only contact7 section for the corrected producer lexical context.
   Every declaration below is private. No helper object/import is produced. -/

namespace I4SourceFramedConfluentCovariance

private theorem ct58_pair_lc (a : SourceMode 2 → ℝ) (v : SourceMode 2 →₀ ℝ) :
    finitePairing a v = Finsupp.linearCombination ℝ a v := by
  classical
  simp only [finitePairing, Finsupp.linearCombination_apply, Finsupp.sum]
  apply Finset.sum_congr rfl
  intro m _hm
  simp only [smul_eq_mul]
  ring

private theorem ct58_pair_direction_sum {q : ℕ} (a : SourceMode 2 → ℝ)
    (c : Fin q → ℝ) (v : Fin q → (SourceMode 2 →₀ ℝ)) :
    finitePairing a (∑ j, c j • v j) = ∑ j, c j * finitePairing a (v j) := by
  simp only [ct58_pair_lc, map_sum, map_smul, smul_eq_mul]

private theorem ct58_pair_direction_add_smul (a : SourceMode 2 → ℝ)
    (v w : SourceMode 2 →₀ ℝ) (c : ℝ) :
    finitePairing a (v+c • w) = finitePairing a v+c*finitePairing a w := by
  simp only [ct58_pair_lc, map_add, map_smul, smul_eq_mul]

private theorem ct58_pair_row_add (a b : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) :
    finitePairing (fun m => a m+b m) v = finitePairing a v+finitePairing b v := by
  classical
  simp only [finitePairing, Finsupp.sum, add_mul, Finset.sum_add_distrib]

private theorem ct58_pair_row_scale (c : ℝ) (a : SourceMode 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) :
    finitePairing (fun m => c*a m) v = c*finitePairing a v := by
  classical
  simp only [finitePairing, Finsupp.sum, mul_assoc, Finset.mul_sum]

private theorem ct58_ifd_scale (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (a : ℝ) (k : ℕ)
    (p : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    iteratedFDeriv ℝ k (fun x => a*f x) p u = a*iteratedFDeriv ℝ k f p u := by
  have hk : ContDiff ℝ (k : ℕ∞) f := hf.of_le (by simp)
  have h := congrArg (fun A => A u)
    (iteratedFDeriv_const_smul_apply' (a := a) (x := p) hk.contDiffAt)
  simpa only [smul_eq_mul, Pi.smul_apply, smul_apply] using h

private theorem ct58_ifd_add (f g : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (hg : ContDiff ℝ (⊤ : ℕ∞) g)
    (k : ℕ) (p : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    iteratedFDeriv ℝ k (fun x => f x+g x) p u =
      iteratedFDeriv ℝ k f p u+iteratedFDeriv ℝ k g p u := by
  have hf' : ContDiff ℝ (k : ℕ∞) f := hf.of_le (by simp)
  have hg' : ContDiff ℝ (k : ℕ∞) g := hg.of_le (by simp)
  have h := congrArg (fun A => A u) (iteratedFDeriv_add_apply (x:=p) hf'.contDiffAt hg'.contDiffAt)
  simpa only [Pi.add_apply, ContinuousMultilinearMap.add_apply] using h

private theorem ct58_jet2_scale (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (a : ℝ) (p : Fin 2 → ℝ) :
    jet2 (fun x => a*f x) p = fun j => a*jet2 f p j := by
  ext j
  fin_cases j
  · rfl
  · simpa [jet2,iteratedFDeriv_one_apply] using
      ct58_ifd_scale f hf a 1 p ![directionX]
  · simpa [jet2,iteratedFDeriv_one_apply] using
      ct58_ifd_scale f hf a 1 p ![directionY]
  · simpa [jet2] using
      ct58_ifd_scale f hf a 2 p ![directionX,directionX]
  · simpa [jet2] using
      ct58_ifd_scale f hf a 2 p ![directionX,directionY]
  · simpa [jet2] using
      ct58_ifd_scale f hf a 2 p ![directionY,directionY]

private theorem ct58_eval_smooth (L : ℝ) (P : TrigPoly) :
    ContDiff ℝ (⊤ : ℕ∞) (eval L P) := by
  induction P with
  | nil =>
      change ContDiff ℝ (⊤ : ℕ∞) (fun _ : Fin 2 → ℝ => (0:ℝ))
      exact contDiff_const
  | cons t P ih =>
      have hterm : ContDiff ℝ (⊤ : ℕ∞) (termEval L t) := by
        unfold termEval phase
        fun_prop
      have heq : eval L (t::P) = fun x => termEval L t x+eval L P x := by
        funext x
        simp only [eval, List.map_cons, List.sum_cons]
      rw [heq]
      exact hterm.add ih

private def ct58_axisCosPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L p [⟨1,Pi.single j 1,0⟩]

private def ct58_axisSinPoly (L : ℝ) (p : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  translate L p [⟨1,Pi.single j 1,-(Real.pi/2)⟩]

private theorem ct58_eval_axisCos (L : ℝ) (p y : Fin 2 → ℝ) (j : Fin 2) :
    eval L (ct58_axisCosPoly L p j) y = Real.cos (sourceC L*(y j-p j)) := by
  rw [ct58_axisCosPoly, eval_translate]
  fin_cases j <;> simp [eval, termEval, phase, Fin.sum_univ_two]

private theorem ct58_eval_axisSin (L : ℝ) (p y : Fin 2 → ℝ) (j : Fin 2) :
    eval L (ct58_axisSinPoly L p j) y = Real.sin (sourceC L*(y j-p j)) := by
  rw [ct58_axisSinPoly, eval_translate]
  fin_cases j <;>
    simp [eval, termEval, phase, Fin.sum_univ_two,
      ← sub_eq_add_neg, Real.cos_sub_pi_div_two]

private def ct58_germPoly (L : ℝ) (p : Fin 2 → ℝ) (s : Fin 6) : TrigPoly :=
  ![constant 1,
    scale (sourceC L)⁻¹ (ct58_axisSinPoly L p 0),
    scale (sourceC L)⁻¹ (ct58_axisSinPoly L p 1),
    scale ((sourceC L)^2)⁻¹
      (constant 1 ++ scale (-1) (ct58_axisCosPoly L p 0)),
    scale ((sourceC L)^2)⁻¹
      (mul (ct58_axisSinPoly L p 0) (ct58_axisSinPoly L p 1)),
    scale ((sourceC L)^2)⁻¹
      (constant 1 ++ scale (-1) (ct58_axisCosPoly L p 1))] s

private theorem ct58_germPoly_eval (L : ℝ) (p : Fin 2 → ℝ) (s : Fin 6) :
    eval L (ct58_germPoly L p s) = localGerm (sourceC L) p s := by
  funext y
  fin_cases s <;>
    simp [ct58_germPoly, localGerm, eval_constant, eval_scale, eval_append, eval_mul,
      ct58_eval_axisCos, ct58_eval_axisSin, div_eq_mul_inv] <;> ring

private theorem ct58_pair_ordinary {L : ℝ} (hL : L ≠ 0) (P : TrigPoly)
    (p : Fin 2 → ℝ) (j : Fin 6) :
    finitePairing (fun m => jet2 (modeCoefficient 2 L m) p j) (toSource L P) =
      jet2 (eval L P) p j := by
  fin_cases j
  · exact toSource_eval hL P p
  · change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 L m) p directionX) (toSource L P) =
      fderiv ℝ (eval L P) p directionX
    have he : derivativeCoefficient 2 L 1 p (fun _ => directionX) =
        (fun m => fderiv ℝ (modeCoefficient 2 L m) p directionX) := by
      funext m
      exact iteratedFDeriv_one_apply _
    rw [← he]
    simpa only [iteratedFDeriv_one_apply] using toSource_derivative hL P 1 p (fun _ => directionX)
  · change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 L m) p directionY) (toSource L P) =
      fderiv ℝ (eval L P) p directionY
    have he : derivativeCoefficient 2 L 1 p (fun _ => directionY) =
        (fun m => fderiv ℝ (modeCoefficient 2 L m) p directionY) := by
      funext m
      exact iteratedFDeriv_one_apply _
    rw [← he]
    simpa only [iteratedFDeriv_one_apply] using toSource_derivative hL P 1 p (fun _ => directionY)
  · change finitePairing (derivativeCoefficient 2 L 2 p ![directionX,directionX]) (toSource L P) =
      iteratedFDeriv ℝ 2 (eval L P) p ![directionX,directionX]
    exact toSource_derivative hL P 2 p ![directionX,directionX]
  · change finitePairing (derivativeCoefficient 2 L 2 p ![directionX,directionY]) (toSource L P) =
      iteratedFDeriv ℝ 2 (eval L P) p ![directionX,directionY]
    exact toSource_derivative hL P 2 p ![directionX,directionY]
  · change finitePairing (derivativeCoefficient 2 L 2 p ![directionY,directionY]) (toSource L P) =
      iteratedFDeriv ℝ 2 (eval L P) p ![directionY,directionY]
    exact toSource_derivative hL P 2 p ![directionY,directionY]

private theorem ct58_ordinary_finite_interpolation {L : ℝ} (hL : L ≠ 0)
    (p : Fin 2 → ℝ) (u : Fin 6 → ℝ) :
    ∃ v : SourceMode 2 →₀ ℝ,
      ∀ j, finitePairing (fun m => jet2 (modeCoefficient 2 L m) p j) v = u j := by
  have hc : sourceC L ≠ 0 := by
    unfold sourceC
    exact div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL
  let w : Fin 6 → (SourceMode 2 →₀ ℝ) := fun s => toSource L (ct58_germPoly L p s)
  have hw (j s : Fin 6) :
      finitePairing (fun m => jet2 (modeCoefficient 2 L m) p j) (w s) =
        if j=s then 1 else 0 := by
    rw [show w s = toSource L (ct58_germPoly L p s) from rfl,
      ct58_pair_ordinary hL, ct58_germPoly_eval]
    exact localGerm_jet2 (sourceC L) hc p j s
  refine ⟨∑ s, u s • w s,?_⟩
  intro j
  rw [ct58_pair_direction_sum]
  simp [hw]

private def ct58_lowerIndex : Fin 6 → Fin 7 := ![0,1,2,3,4,6]

private def ct58_lowerTransform (e n : Fin 2 → ℝ) (u : Fin 6 → ℝ) : Fin 6 → ℝ :=
  ![u 0,
    e 0*u 1+e 1*u 2,
    n 0*u 1+n 1*u 2,
    e 0^2*u 3+2*e 0*e 1*u 4+e 1^2*u 5,
    e 0*n 0*u 3+(e 0*n 1+e 1*n 0)*u 4+e 1*n 1*u 5,
    n 0^2*u 3+2*n 0*n 1*u 4+n 1^2*u 5]

private theorem ct58_linear_coordinates (A : (Fin 2 → ℝ) →L[ℝ] ℝ)
    (u : Fin 2 → ℝ) : A u = u 0*A directionX+u 1*A directionY := by
  have hu : u = u 0 • directionX+u 1 • directionY := by
    ext j
    fin_cases j <;> simp [directionX,directionY]
  calc
    A u = A (u 0 • directionX+u 1 • directionY) := congrArg A hu
    _ = _ := by simp only [map_add,map_smul,smul_eq_mul]

private theorem ct58_second_coordinates (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (p u v : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 f p ![u,v] =
      u 0*v 0*jet2 f p 3+(u 0*v 1+u 1*v 0)*jet2 f p 4+
        u 1*v 1*jet2 f p 5 := by
  let B := fderiv ℝ (fderiv ℝ f) p
  have hs : B directionY directionX = B directionX directionY :=
    (hf.contDiffAt.isSymmSndFDerivAt (by simp)).eq directionY directionX
  have hu : u = u 0 • directionX+u 1 • directionY := by
    ext j
    fin_cases j <;> simp [directionX,directionY]
  have hB : B u v = u 0*B directionX v+u 1*B directionY v := by
    calc
      B u v = B (u 0 • directionX+u 1 • directionY) v := congrArg (fun z => B z v) hu
      _ = _ := by simp only [map_add,map_smul,add_apply,smul_apply,smul_eq_mul]
  rw [iteratedFDeriv_two_apply]
  change B u v = _
  rw [hB, ct58_linear_coordinates (B directionX) v,
    ct58_linear_coordinates (B directionY) v, hs]
  simp [jet2,iteratedFDeriv_two_apply]
  dsimp only [B]
  ring

private theorem ct58_contact_lower_formula (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (p e n : Fin 2 → ℝ) (j : Fin 6) :
    contactRows f p e n (ct58_lowerIndex j) = ct58_lowerTransform e n (jet2 f p) j := by
  fin_cases j
  · rfl
  · exact ct58_linear_coordinates (fderiv ℝ f p) e
  · exact ct58_linear_coordinates (fderiv ℝ f p) n
  · change iteratedFDeriv ℝ 2 f p ![e,e] =
      e 0^2*jet2 f p 3+2*e 0*e 1*jet2 f p 4+e 1^2*jet2 f p 5
    rw [ct58_second_coordinates f hf p e e]
    ring
  · exact ct58_second_coordinates f hf p e n
  · change iteratedFDeriv ℝ 2 f p ![n,n] =
      n 0^2*jet2 f p 3+2*n 0*n 1*jet2 f p 4+n 1^2*jet2 f p 5
    rw [ct58_second_coordinates f hf p n n]
    ring

private theorem ct58_pair_lower {L : ℝ} (p e n : Fin 2 → ℝ)
    (v : SourceMode 2 →₀ ℝ) (j : Fin 6) :
    finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n (ct58_lowerIndex j)) v =
      ct58_lowerTransform e n
        (fun s => finitePairing (fun m => jet2 (modeCoefficient 2 L m) p s) v) j := by
  have heq : (fun m => contactRows (modeCoefficient 2 L m) p e n (ct58_lowerIndex j)) =
      fun m => ct58_lowerTransform e n (jet2 (modeCoefficient 2 L m) p) j := by
    funext m
    exact ct58_contact_lower_formula _ (mode_smooth L m) p e n j
  rw [heq]
  fin_cases j <;>
    simp [ct58_lowerTransform,ct58_pair_row_add,ct58_pair_row_scale]

private def ct58_inverseLower (e n : Fin 2 → ℝ) (t : Fin 6 → ℝ) : Fin 6 → ℝ :=
  ![t 0,
    e 0*t 1+n 0*t 2,
    e 1*t 1+n 1*t 2,
    e 0^2*t 3+2*e 0*n 0*t 4+n 0^2*t 5,
    e 0*e 1*t 3+(e 0*n 1+n 0*e 1)*t 4+n 0*n 1*t 5,
    e 1^2*t 3+2*e 1*n 1*t 4+n 1^2*t 5]

private theorem ct58_lower_inverse (e n : Fin 2 → ℝ)
    (he : e 0^2+e 1^2=1) (hn : n 0^2+n 1^2=1)
    (hen : e 0*n 0+e 1*n 1=0) (t : Fin 6 → ℝ) :
    ct58_lowerTransform e n (ct58_inverseLower e n t) = t := by
  ext j
  fin_cases j
  · rfl
  · change e 0*(e 0*t 1+n 0*t 2)+e 1*(e 1*t 1+n 1*t 2)=t 1
    calc
      _ = (e 0^2+e 1^2)*t 1+(e 0*n 0+e 1*n 1)*t 2 := by ring
      _ = t 1 := by rw [he,hen]; ring
  · change n 0*(e 0*t 1+n 0*t 2)+n 1*(e 1*t 1+n 1*t 2)=t 2
    calc
      _ = (e 0*n 0+e 1*n 1)*t 1+(n 0^2+n 1^2)*t 2 := by ring
      _ = t 2 := by rw [hn,hen]; ring
  · change _ = t 3
    calc
      _ = (e 0^2+e 1^2)^2*t 3+
          2*(e 0^2+e 1^2)*(e 0*n 0+e 1*n 1)*t 4+
          (e 0*n 0+e 1*n 1)^2*t 5 := by
            dsimp [ct58_lowerTransform,ct58_inverseLower]
            ring
      _ = t 3 := by rw [he,hen]; ring
  · change _ = t 4
    calc
      _ = (e 0^2+e 1^2)*(e 0*n 0+e 1*n 1)*t 3+
          ((e 0^2+e 1^2)*(n 0^2+n 1^2)+(e 0*n 0+e 1*n 1)^2)*t 4+
          (e 0*n 0+e 1*n 1)*(n 0^2+n 1^2)*t 5 := by
            dsimp [ct58_lowerTransform,ct58_inverseLower]
            ring
      _ = t 4 := by rw [he,hn,hen]; ring
  · change _ = t 5
    calc
      _ = (e 0*n 0+e 1*n 1)^2*t 3+
          2*(e 0*n 0+e 1*n 1)*(n 0^2+n 1^2)*t 4+
          (n 0^2+n 1^2)^2*t 5 := by
            dsimp [ct58_lowerTransform,ct58_inverseLower]
            ring
      _ = t 5 := by rw [hn,hen]; ring

/- The ordinary-XY Hessian block has determinant Delta^3, so the
   value/gradient/Hessian block determinant is Delta^4 in either orientation. -/
private theorem ct58_frame_block_determinants (a b c d : ℝ) :
    Matrix.det (!![a,b;c,d] : Matrix (Fin 2) (Fin 2) ℝ)=a*d-b*c ∧
    Matrix.det (!![a^2,2*a*b,b^2;a*c,a*d+b*c,b*d;c^2,2*c*d,d^2] :
      Matrix (Fin 3) (Fin 3) ℝ)=(a*d-b*c)^3 ∧
    (a*d-b*c)*(a*d-b*c)^3=(a*d-b*c)^4 := by
  constructor
  · simp [Matrix.det_fin_two]
  constructor
  · simp [Matrix.det_fin_three]
    ring
  · ring

private theorem ct58_frame_coordinates (R : OrthonormalBasis (Fin 2) ℝ (E 2)) :
    let e := coordinates 2 (R 0)
    let n := coordinates 2 (R 1)
    e 0^2+e 1^2=1 ∧ n 0^2+n 1^2=1 ∧ e 0*n 0+e 1*n 1=0 := by
  dsimp only
  constructor
  · simpa [coordinates,EuclideanSpace.inner_eq_star_dotProduct,dotProduct,
      Fin.sum_univ_two,pow_two] using R.inner_eq_ite (0 : Fin 2) (0 : Fin 2)
  constructor
  · simpa [coordinates,EuclideanSpace.inner_eq_star_dotProduct,dotProduct,
      Fin.sum_univ_two,pow_two] using R.inner_eq_ite (1 : Fin 2) (1 : Fin 2)
  · simpa [coordinates,EuclideanSpace.inner_eq_star_dotProduct,dotProduct,
      Fin.sum_univ_two,mul_comm] using R.inner_eq_ite (0 : Fin 2) (1 : Fin 2)

private theorem ct58_frame_delta_four (e n : Fin 2 → ℝ)
    (he : e 0^2+e 1^2=1) (hn : n 0^2+n 1^2=1)
    (hen : e 0*n 0+e 1*n 1=0) :
    (e 0*n 1-e 1*n 0)^4=1 := by
  have hs : (e 0*n 1-e 1*n 0)^2=
      (e 0^2+e 1^2)*(n 0^2+n 1^2)-(e 0*n 0+e 1*n 1)^2 := by ring
  rw [he,hn,hen] at hs
  calc
    _ = ((e 0*n 1-e 1*n 0)^2)^2 := by ring
    _ = 1 := by rw [hs]; norm_num

private theorem ct58_shifted_sine_third (d t : ℝ) :
    iteratedDeriv 3 (fun x : ℝ => Real.sin (x-d)) t = -Real.cos (t-d) := by
  have h1 : deriv (fun x : ℝ => Real.sin (x-d)) = fun x => Real.cos (x-d) := by
    funext x
    simp
  have h2 : deriv (fun x : ℝ => Real.cos (x-d)) = fun x => -Real.sin (x-d) := by
    funext x
    simp
  have h3 : deriv (fun x : ℝ => -Real.sin (x-d)) = fun x => -Real.cos (x-d) := by
    funext x
    simp
  simp only [iteratedDeriv_succ,iteratedDeriv_zero,h1,h2,h3]

private theorem ct58_axis_sine_third (c : ℝ) (p e : Fin 2 → ℝ) (j : Fin 2) :
    iteratedFDeriv ℝ 3 (fun y : Fin 2 → ℝ => Real.sin (c*(y j-p j))) p ![e,e,e] =
      -(c*e j)^3 := by
  let A : (Fin 2 → ℝ) →L[ℝ] ℝ := c • ContinuousLinearMap.proj j
  let g : ℝ → ℝ := fun t => Real.sin (t-c*p j)
  have hg : ContDiff ℝ (⊤ : ℕ∞) g := by dsimp [g]; fun_prop
  have heq : (fun y : Fin 2 → ℝ => Real.sin (c*(y j-p j))) = g ∘ A := by
    funext y
    simp only [Function.comp_apply,g]
    congr 1
    simp only [A,smul_apply,ContinuousLinearMap.proj_apply,smul_eq_mul]
    ring
  rw [heq]
  have h := congrArg (fun T => T ![e,e,e])
    (A.iteratedFDeriv_comp_right hg p (i := 3) (by simp))
  rw [h]
  rw [ContinuousMultilinearMap.compContinuousLinearMap_apply,
    iteratedFDeriv_apply_eq_iteratedDeriv_mul_prod]
  have hd : iteratedDeriv 3 g (A p) = -1 := by
    simpa [g,A] using ct58_shifted_sine_third (c*p j) (A p)
  rw [hd]
  simp [A,Fin.prod_univ_succ,pow_succ]
  ring

private def ct58_axisGermIndex (j : Fin 2) : Fin 6 := if j=0 then 1 else 2

private theorem ct58_axisGerm_value (c : ℝ) (p y : Fin 2 → ℝ) (j : Fin 2) :
    localGerm c p (ct58_axisGermIndex j) y = Real.sin (c*(y j-p j))/c := by
  fin_cases j <;> rfl

private def ct58_cubePoly (L : ℝ) (p e : Fin 2 → ℝ) (j : Fin 2) : TrigPoly :=
  let P := ct58_germPoly L p (ct58_axisGermIndex j)
  scale (6*(e j)^3)⁻¹ (mul (mul P P) P)

private theorem ct58_cubePoly_eval (L : ℝ) (p e y : Fin 2 → ℝ) (j : Fin 2) :
    eval L (ct58_cubePoly L p e j) y =
      (Real.sin (sourceC L*(y j-p j))/sourceC L)^3/(6*(e j)^3) := by
  simp only [ct58_cubePoly,eval_scale,eval_mul,ct58_germPoly_eval,ct58_axisGerm_value]
  ring

private theorem ct58_cube_lower_zero {L : ℝ} (hL : L ≠ 0)
    (p e : Fin 2 → ℝ) (j : Fin 2) :
    jet2 (eval L (ct58_cubePoly L p e j)) p = 0 := by
  have hc : sourceC L ≠ 0 := by
    unfold sourceC
    exact div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL
  let f := localGerm (sourceC L) p (ct58_axisGermIndex j)
  have hf : ContDiff ℝ (⊤ : ℕ∞) f := by
    rw [show f = eval L (ct58_germPoly L p (ct58_axisGermIndex j)) from
      (ct58_germPoly_eval L p (ct58_axisGermIndex j)).symm]
    exact ct58_eval_smooth L _
  have hJ : jet2 f p = fun k => if k=ct58_axisGermIndex j then 1 else 0 := by
    ext k
    exact localGerm_jet2 (sourceC L) hc p k (ct58_axisGermIndex j)
  have hcube : jet2 (fun y => (f y*f y)*f y) p = 0 := by
    rw [jet2_mul _ _ ((hf.mul hf).of_le (by norm_num)) (hf.of_le (by norm_num)),
      jet2_mul _ _ (hf.of_le (by norm_num)) (hf.of_le (by norm_num))]
    simp only [hJ]
    ext k
    fin_cases j <;> fin_cases k <;> norm_num [mulJet2,ct58_axisGermIndex]
  have heq : eval L (ct58_cubePoly L p e j) =
      fun y => (6*(e j)^3)⁻¹*((f y*f y)*f y) := by
    funext y
    simp only [ct58_cubePoly,eval_scale,eval_mul,ct58_germPoly_eval,f]
  rw [heq,ct58_jet2_scale _ ((hf.mul hf).mul hf),hcube]
  ext k
  simp

private theorem ct58_cube_third_one {L : ℝ} (hL : L ≠ 0)
    (p e : Fin 2 → ℝ) (j : Fin 2) (hej : e j ≠ 0) :
    iteratedFDeriv ℝ 3 (eval L (ct58_cubePoly L p e j)) p ![e,e,e] = 1 := by
  let c := sourceC L
  have hc : c ≠ 0 := by
    dsimp [c]
    unfold sourceC
    exact div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL
  let f : (Fin 2 → ℝ) → ℝ := fun y => Real.sin (c*(y j-p j))
  let g : (Fin 2 → ℝ) → ℝ := fun y => Real.sin ((3*c)*(y j-p j))
  have hf : ContDiff ℝ (⊤ : ℕ∞) f := by dsimp [f]; fun_prop
  have hg : ContDiff ℝ (⊤ : ℕ∞) g := by dsimp [g]; fun_prop
  have heq : eval L (ct58_cubePoly L p e j) =
      fun y => (24*c^3*(e j)^3)⁻¹*(3*f y+(-1)*g y) := by
    funext y
    rw [ct58_cubePoly_eval]
    have hs := Real.sin_three_mul (c*(y j-p j))
    change (Real.sin (c*(y j-p j))/c)^3/(6*(e j)^3)=
      (24*c^3*(e j)^3)⁻¹*(3*Real.sin (c*(y j-p j))+(-1)*Real.sin ((3*c)*(y j-p j)))
    rw [show (3*c)*(y j-p j)=3*(c*(y j-p j)) by ring]
    rw [hs]
    field_simp [hc,hej]
    ring
  have hf3 : ContDiff ℝ (⊤ : ℕ∞) (fun y => 3*f y) := contDiff_const.mul hf
  have hgm : ContDiff ℝ (⊤ : ℕ∞) (fun y => (-1:ℝ)*g y) := contDiff_const.mul hg
  rw [heq,ct58_ifd_scale _ (hf3.add hgm),
    ct58_ifd_add _ _ hf3 hgm,
    ct58_ifd_scale _ hf,ct58_ifd_scale _ hg]
  dsimp only [f,g]
  rw [ct58_axis_sine_third,ct58_axis_sine_third]
  field_simp [hc,hej]
  ring

private theorem ct58_contact_pair {L : ℝ} (hL : L ≠ 0) (P : TrigPoly)
    (p e n : Fin 2 → ℝ) (i : Fin 7) :
    finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n i) (toSource L P) =
      contactRows (eval L P) p e n i := by
  fin_cases i
  · exact toSource_eval hL P p
  · change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 L m) p e) (toSource L P) =
      fderiv ℝ (eval L P) p e
    have he : derivativeCoefficient 2 L 1 p (fun _ => e) =
        (fun m => fderiv ℝ (modeCoefficient 2 L m) p e) := by
      funext m
      exact iteratedFDeriv_one_apply _
    rw [← he]
    simpa only [iteratedFDeriv_one_apply] using toSource_derivative hL P 1 p (fun _ => e)
  · change finitePairing (fun m => fderiv ℝ (modeCoefficient 2 L m) p n) (toSource L P) =
      fderiv ℝ (eval L P) p n
    have he : derivativeCoefficient 2 L 1 p (fun _ => n) =
        (fun m => fderiv ℝ (modeCoefficient 2 L m) p n) := by
      funext m
      exact iteratedFDeriv_one_apply _
    rw [← he]
    simpa only [iteratedFDeriv_one_apply] using toSource_derivative hL P 1 p (fun _ => n)
  · change finitePairing (derivativeCoefficient 2 L 2 p ![e,e]) (toSource L P) =
      iteratedFDeriv ℝ 2 (eval L P) p ![e,e]
    exact toSource_derivative hL P 2 p ![e,e]
  · change finitePairing (derivativeCoefficient 2 L 2 p ![e,n]) (toSource L P) =
      iteratedFDeriv ℝ 2 (eval L P) p ![e,n]
    exact toSource_derivative hL P 2 p ![e,n]
  · change finitePairing (derivativeCoefficient 2 L 3 p ![e,e,e]) (toSource L P) =
      iteratedFDeriv ℝ 3 (eval L P) p ![e,e,e]
    exact toSource_derivative hL P 3 p ![e,e,e]
  · change finitePairing (derivativeCoefficient 2 L 2 p ![n,n]) (toSource L P) =
      iteratedFDeriv ℝ 2 (eval L P) p ![n,n]
    exact toSource_derivative hL P 2 p ![n,n]

private theorem ct58_contact_target {L : ℝ} (hL : L ≠ 0)
    (p e n : Fin 2 → ℝ) (he : e 0^2+e 1^2=1) (hn : n 0^2+n 1^2=1)
    (hen : e 0*n 0+e 1*n 1=0) (t : Fin 7 → ℝ) :
    ∃ v : SourceMode 2 →₀ ℝ,
      ∀ i, finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n i) v=t i := by
  let tlo : Fin 6 → ℝ := fun j => t (ct58_lowerIndex j)
  obtain ⟨w,hw⟩ := ct58_ordinary_finite_interpolation hL p (ct58_inverseLower e n tlo)
  have hwlo (j : Fin 6) :
      finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n (ct58_lowerIndex j)) w =
        t (ct58_lowerIndex j) := by
    rw [ct58_pair_lower]
    have hvec : (fun s => finitePairing (fun m => jet2 (modeCoefficient 2 L m) p s) w) =
        ct58_inverseLower e n tlo := funext hw
    rw [hvec,ct58_lower_inverse e n he hn hen]
  obtain ⟨j,hej⟩ : ∃ j : Fin 2, e j ≠ 0 := by
    by_cases h0 : e 0=0
    · refine ⟨1,?_⟩
      intro h1
      norm_num [h0,h1] at he
    · exact ⟨0,h0⟩
  let q := toSource L (ct58_cubePoly L p e j)
  have hqlo (k : Fin 6) :
      finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n (ct58_lowerIndex k)) q=0 := by
    rw [ct58_pair_lower]
    have hzero : (fun s => finitePairing (fun m => jet2 (modeCoefficient 2 L m) p s) q)=0 := by
      ext s
      rw [show q=toSource L (ct58_cubePoly L p e j) from rfl,
        ct58_pair_ordinary hL,ct58_cube_lower_zero hL]
    rw [hzero]
    fin_cases k <;> simp [ct58_lowerTransform]
  have hq5 : finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n 5) q=1 := by
    rw [show q=toSource L (ct58_cubePoly L p e j) from rfl,ct58_contact_pair hL]
    exact ct58_cube_third_one hL p e j hej
  let beta := finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n 5) w
  let v := w+(t 5-beta) • q
  have hvlo (k : Fin 6) :
      finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n (ct58_lowerIndex k)) v=
        t (ct58_lowerIndex k) := by
    rw [show v=w+(t 5-beta) • q from rfl,ct58_pair_direction_add_smul,hwlo,hqlo]
    ring
  refine ⟨v,?_⟩
  intro i
  fin_cases i
  · exact hvlo 0
  · exact hvlo 1
  · exact hvlo 2
  · exact hvlo 3
  · exact hvlo 4
  · change finitePairing (fun m => contactRows (modeCoefficient 2 L m) p e n (5:Fin 7)) v = t 5
    rw [show v=w+(t 5-beta) • q from rfl,ct58_pair_direction_add_smul,hq5]
    change beta+(t 5-beta)*1=t 5
    ring
  · exact hvlo 5

private theorem contact_finite_directions {L : ℝ} (hL : L ≠ 0)
    (z : E 2) (R : OrthonormalBasis (Fin 2) ℝ (E 2)) :
    ∃ v : Fin 7 → (SourceMode 2 →₀ ℝ), ∀ i s,
      finitePairing (fun m => contactRows (modeCoefficient 2 L m) (coordinates 2 z)
        (coordinates 2 (R 0)) (coordinates 2 (R 1)) i) (v s)=if i=s then 1 else 0 := by
  obtain ⟨he,hn,hen⟩ := ct58_frame_coordinates R
  have ht (s : Fin 7) := ct58_contact_target hL (coordinates 2 z)
    (coordinates 2 (R 0)) (coordinates 2 (R 1)) he hn hen (fun i => if i=s then 1 else 0)
  classical
  choose v hv using ht
  exact ⟨v,fun i s => hv s i⟩

end I4SourceFramedConfluentCovariance

-- INTEGRATED_CONTACT_END

-- INTEGRATED_PEANO_BEGIN
namespace I4SourceFramedConfluentCovariance
/- UNCOMPILED TEXT ONLY. Insert once inside namespace
   I4SourceFramedConfluentCovariance, after the corrected shared peanoRows
   definition. No physical-coordinate or series/Gram adapter is included. -/

open I4ConfluentIntegralIdentities
open scoped Interval

private theorem peanoCurve_iteratedDeriv
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (p e : Fin 2 → ℝ) (k : ℕ) (t : ℝ) :
    iteratedDeriv k (fun s : ℝ => f (p+s • e)) t =
      iteratedFDeriv ℝ k f (p+t • e) (fun _ => e) := by
  let ell : ℝ →L[ℝ] (Fin 2 → ℝ) :=
    (ContinuousLinearMap.id ℝ ℝ).smulRight e
  have hshift : ContDiff ℝ (⊤ : ℕ∞) (fun y : Fin 2 → ℝ => f (p+y)) :=
    hf.comp (contDiff_const.add contDiff_id)
  rw [iteratedDeriv_eq_iteratedFDeriv]
  have h := ell.iteratedFDeriv_comp_right hshift t (i := k) (by simp)
  have hh := congrArg (fun A => A (fun _ : Fin k => (1 : ℝ))) h
  simpa only [Function.comp_def,ContinuousMultilinearMap.compContinuousLinearMap_apply,
    iteratedFDeriv_comp_add_left,ell,ContinuousLinearMap.smulRight_apply,
    ContinuousLinearMap.id_apply,one_smul] using hh

private theorem peanoCurve_deriv
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (p e : Fin 2 → ℝ) (t : ℝ) :
    deriv (fun s : ℝ => f (p+s • e)) t = fderiv ℝ f (p+t • e) e := by
  simpa only [iteratedDeriv_one,iteratedFDeriv_one_apply] using
    peanoCurve_iteratedDeriv f hf p e 1 t

private theorem peanoCurve_transverse_iteratedDeriv
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (p e n : Fin 2 → ℝ) (k : ℕ) (t : ℝ) :
    iteratedDeriv k (fun s : ℝ => fderiv ℝ f (p+s • e) n) t =
      iteratedFDeriv ℝ (k+1) f (p+t • e) (Fin.snoc (fun _ => e) n) := by
  have hdf : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ f) := hf.fderiv_right (by simp)
  have hfun : ContDiff ℝ (⊤ : ℕ∞) (fun y : Fin 2 → ℝ => fderiv ℝ f y n) :=
    hdf.clm_apply contDiff_const
  calc
    _ = iteratedFDeriv ℝ k (fun y : Fin 2 → ℝ => fderiv ℝ f y n)
        (p+t • e) (fun _ => e) :=
      peanoCurve_iteratedDeriv _ hfun p e k t
    _ = iteratedFDeriv ℝ k (fderiv ℝ f) (p+t • e) (fun _ => e) n :=
      iteratedFDeriv_clm_apply_const_apply hdf (by simp)
    _ = _ := by
      rw [iteratedFDeriv_succ_apply_right,Fin.init_snoc,Fin.snoc_last]

private theorem peanoRows_confluent
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f)
    (p e n : Fin 2 → ℝ) (r : ℝ) (hr : r ≠ 0) :
    (fun i : Fin 6 => peanoRows f p e n r (Fin.castAdd 1 i)) =
      I4SourceConfluentPins.confluentTransform r
        ![f (p-(r/2) • e),f (p+(r/2) • e),
          fderiv ℝ f (p-(r/2) • e) e,fderiv ℝ f (p+(r/2) • e) e,
          fderiv ℝ f (p-(r/2) • e) n,fderiv ℝ f (p+(r/2) • e) n] := by
  let F : ℝ → ℝ := fun s => f (p+s • e)
  let H : ℝ → ℝ := fun s => fderiv ℝ f (p+s • e) n
  have hcurve : ContDiff ℝ (⊤ : ℕ∞) (fun s : ℝ => p+s • e) :=
    contDiff_const.add (contDiff_id.smul contDiff_const)
  have hF : ContDiff ℝ 3 F := (hf.comp hcurve).of_le (by simp)
  have hdf : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ f) := hf.fderiv_right (by simp)
  have hH : ContDiff ℝ 2 H :=
    ((hdf.clm_apply contDiff_const).comp hcurve).of_le (by simp)
  have hF1 (s : ℝ) : deriv F s = fderiv ℝ f (p+s • e) e :=
    peanoCurve_deriv f hf p e s
  have he2 : (fun _ : Fin 2 => e) = ![e,e] := by
    funext i
    fin_cases i <;> rfl
  have he3 : (fun _ : Fin 3 => e) = ![e,e,e] := by
    funext i
    fin_cases i <;> rfl
  have hF2 (s : ℝ) :
      iteratedDeriv 2 F s = iteratedFDeriv ℝ 2 f (p+s • e) ![e,e] := by
    simpa only [he2] using peanoCurve_iteratedDeriv f hf p e 2 s
  have hF3 (s : ℝ) :
      iteratedDeriv 3 F s = iteratedFDeriv ℝ 3 f (p+s • e) ![e,e,e] := by
    simpa only [he3] using peanoCurve_iteratedDeriv f hf p e 3 s
  have hen : Fin.snoc (fun _ : Fin 1 => e) n = ![e,n] := by
    funext i
    fin_cases i <;> rfl
  have hH1 (s : ℝ) :
      deriv H s = iteratedFDeriv ℝ 2 f (p+s • e) ![e,n] := by
    simpa only [iteratedDeriv_one,hen] using
      peanoCurve_transverse_iteratedDeriv f hf p e n 1 s
  have hneg : p+(-r/2) • e = p-(r/2) • e := by
    simp only [neg_div,neg_smul,sub_eq_add_neg]
  have h3 := pin3_integral F hF r hr
  simp only [pin3,hF1,hF2,hneg] at h3
  have h4 := pin4_integral H hH r hr
  simp only [pin4,hH1] at h4
  simp only [H,hneg] at h4
  have h5 := pin5_integral F hF r hr
  simp only [pin5,hF1,hF3] at h5
  simp only [F,hneg] at h5
  rw [add_comm (fderiv ℝ f (p+(r/2) • e) e)
    (fderiv ℝ f (p-(r/2) • e) e)] at h5
  funext i
  fin_cases i
  · rfl
  · rfl
  · rfl
  · exact h3.symm
  · exact h4.symm
  · exact h5.symm

end I4SourceFramedConfluentCovariance
-- INTEGRATED_PEANO_END

namespace I4SourceFramedConfluentCovariance

private theorem physical_first {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (z e : E 2) :
    fderiv ℝ (actualField 2 L ω) z e =
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z) (coordinates 2 e) := by
  simpa only [iteratedFDeriv_one_apply] using physical_derivative hL ω 1 z (fun _ => e)

private theorem physical_second {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (z e n : E 2) :
    iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![e,n] =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (coordinates 2 z) ![coordinates 2 e,coordinates 2 n] := by
  have h := physical_derivative hL ω 2 z ![e,n]
  have he : (fun i : Fin 2 => coordinates 2 (![e,n] i)) = ![coordinates 2 e,coordinates 2 n] := by
    funext i
    fin_cases i <;> rfl
  rw [he] at h
  exact h

private theorem physical_third {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (z e : E 2) :
    iteratedFDeriv ℝ 3 (actualField 2 L ω) z ![e,e,e] =
      iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) (coordinates 2 z)
        ![coordinates 2 e,coordinates 2 e,coordinates 2 e] := by
  have h := physical_derivative hL ω 3 z ![e,e,e]
  have he : (fun i : Fin 3 => coordinates 2 (![e,e,e] i)) =
      ![coordinates 2 e,coordinates 2 e,coordinates 2 e] := by
    funext i
    fin_cases i <;> rfl
  rw [he] at h
  exact h

private theorem physical_contactRows {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (z e n : E 2) :
    contactRows (smoothSourceField 2 L ω) (coordinates 2 z) (coordinates 2 e) (coordinates 2 n) =
      ![actualField 2 L ω z,fderiv ℝ (actualField 2 L ω) z e,fderiv ℝ (actualField 2 L ω) z n,
        iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![e,e],
        iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![e,n],
        iteratedFDeriv ℝ 3 (actualField 2 L ω) z ![e,e,e],
        iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![n,n] ] := by
  ext i
  fin_cases i
  · rfl
  · exact (physical_first hL ω z e).symm
  · exact (physical_first hL ω z n).symm
  · exact (physical_second hL ω z e e).symm
  · exact (physical_second hL ω z e n).symm
  · exact (physical_third hL ω z e).symm
  · exact (physical_second hL ω z n n).symm

private theorem raw_physical_coordinates {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (z e n : E 2) (r : ℝ) :
    ![actualField 2 L ω (z-(r/2) • e),actualField 2 L ω (z+(r/2) • e),
      fderiv ℝ (actualField 2 L ω) (z-(r/2) • e) e,
      fderiv ℝ (actualField 2 L ω) (z+(r/2) • e) e,
      fderiv ℝ (actualField 2 L ω) (z-(r/2) • e) n,
      fderiv ℝ (actualField 2 L ω) (z+(r/2) • e) n] =
    ![smoothSourceField 2 L ω (coordinates 2 z-(r/2) • coordinates 2 e),
      smoothSourceField 2 L ω (coordinates 2 z+(r/2) • coordinates 2 e),
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z-(r/2) • coordinates 2 e) (coordinates 2 e),
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z+(r/2) • coordinates 2 e) (coordinates 2 e),
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z-(r/2) • coordinates 2 e) (coordinates 2 n),
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z+(r/2) • coordinates 2 e) (coordinates 2 n)] := by
  ext i
  fin_cases i
  · change smoothSourceField 2 L ω (coordinates 2 (z-(r/2) • e)) = _
    rw [map_sub,map_smul]
  · change smoothSourceField 2 L ω (coordinates 2 (z+(r/2) • e)) = _
    rw [map_add,map_smul]
  · simpa only [map_sub,map_smul] using physical_first hL ω (z-(r/2) • e) e
  · simpa only [map_add,map_smul] using physical_first hL ω (z+(r/2) • e) e
  · simpa only [map_sub,map_smul] using physical_first hL ω (z-(r/2) • e) n
  · simpa only [map_add,map_smul] using physical_first hL ω (z+(r/2) • e) n

private theorem contact_posDef {L : ℝ} (hL : L ≠ 0) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) : (framedConfluentCovariance L z R 0).PosDef := by
  obtain ⟨v,hv⟩ := contact_finite_directions hL z R
  have hright (i s : Fin 7) : finitePairing (framedConfluentCoefficient L z R 0 i) (v s) =
      if i=s then 1 else 0 := by
    rw [coefficient_contact]
    exact hv i s
  let a : Fin 0 → SourceMode 2 → ℝ := fun i => Fin.elim0 i
  have hh := coefficientGram_posDef_of_finite_kernel_rightInverse a
    (framedConfluentCoefficient L z R 0) (0 : Matrix (Fin 7) (Fin 0) ℝ)
    (fun i => Fin.elim0 i) (coefficient_summable hL z R 0) v (fun i => Fin.elim0 i) hright
  change (I4ContactGram.coefficientGram (framedConfluentCoefficient L z R 0)).PosDef
  simpa only [residualCoefficient,Matrix.zero_apply,zero_mul,Finset.sum_const_zero,sub_zero] using hh

/-- Literal same-source seven-row prior law, Gram and physical Peano identities. -/
theorem framedConfluentVector_actual {L : ℝ} (hL : L ≠ 0) (z : E 2)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) (r : ℝ) :
    HasGaussianLaw (framedConfluentVector L z R r) (smoothLaw 2 L) ∧
    (∀ i j : Fin 7, cov[fun ω => framedConfluentVector L z R r ω i,
      fun ω => framedConfluentVector L z R r ω j;smoothLaw 2 L] = framedConfluentCovariance L z R r i j) ∧
    (∀ ω : SmoothSample 2 L, framedConfluentVector L z R r ω 6 =
      iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![R 1,R 1]) ∧
    (∀ ω : SmoothSample 2 L, framedConfluentVector L z R 0 ω =
      ![actualField 2 L ω z,fderiv ℝ (actualField 2 L ω) z (R 0),fderiv ℝ (actualField 2 L ω) z (R 1),
        iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![R 0,R 0],
        iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![R 0,R 1],
        iteratedFDeriv ℝ 3 (actualField 2 L ω) z ![R 0,R 0,R 0],
        iteratedFDeriv ℝ 2 (actualField 2 L ω) z ![R 1,R 1] ]) ∧
    (r ≠ 0 → ∀ ω : SmoothSample 2 L,
      (fun i : Fin 6 => framedConfluentVector L z R r ω (Fin.castAdd 1 i)) =
      I4SourceConfluentPins.confluentTransform r
        ![actualField 2 L ω (z-(r/2) • R 0),actualField 2 L ω (z+(r/2) • R 0),
          fderiv ℝ (actualField 2 L ω) (z-(r/2) • R 0) (R 0),
          fderiv ℝ (actualField 2 L ω) (z+(r/2) • R 0) (R 0),
          fderiv ℝ (actualField 2 L ω) (z-(r/2) • R 0) (R 1),
          fderiv ℝ (actualField 2 L ω) (z+(r/2) • R 0) (R 1)]) := by
  refine ⟨vector_hasGaussianLaw hL z R r,vector_covariance hL z R r,?_,?_,?_⟩
  · intro ω
    have h := congrFun (vector_peano hL z R r ω) (6:Fin 7)
    change framedConfluentVector L z R r ω 6 =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) (coordinates 2 z)
        ![coordinates 2 (R 1),coordinates 2 (R 1)] at h
    exact h.trans (physical_second hL ω z (R 1) (R 1)).symm
  · intro ω
    rw [vector_peano hL,peanoRows_zero]
    exact physical_contactRows hL ω z (R 0) (R 1)
  · intro hr ω
    have hv := congrArg (fun v : Fin 7 → ℝ => fun i : Fin 6 => v (Fin.castAdd 1 i))
      (vector_peano hL z R r ω)
    have hp := peanoRows_confluent (smoothSourceField 2 L ω) (smoothSourceField_smooth 2 hL ω)
      (coordinates 2 z) (coordinates 2 (R 0)) (coordinates 2 (R 1)) r hr
    exact hv.trans (hp.trans (congrArg (I4SourceConfluentPins.confluentTransform r)
      (raw_physical_coordinates hL ω z (R 0) (R 1) r).symm))

end I4SourceFramedConfluentCovariance
