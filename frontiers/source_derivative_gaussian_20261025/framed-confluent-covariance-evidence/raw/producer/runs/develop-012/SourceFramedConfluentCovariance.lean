import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.UniformSpace.HeineCantor
import Mathlib.Analysis.Normed.Module.Multilinear.Basic
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
  have h := congrArg (fun A => A u) (fun_iteratedFDeriv_add_apply (x:=p) hf'.contDiffAt hg'.contDiffAt)
  simpa only [Pi.add_apply, add_apply] using h

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
  have h00 := R.inner_eq_one (0:Fin 2)
  have h11 := R.inner_eq_one (1:Fin 2)
  have h01 := R.inner_eq_zero (i:=(0:Fin 2)) (j:=(1:Fin 2)) (by decide)
  simp only [EuclideanSpace.inner_eq_star_dotProduct,star_trivial,dotProduct,Fin.sum_univ_two] at h00 h11 h01
  exact ⟨by simpa only [coordinates_apply,pow_two] using h00,
    by simpa only [coordinates_apply,pow_two] using h11,
    by simpa only [coordinates_apply, mul_comm] using h01⟩

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
  · change smoothSourceField 2 L ω (coordinates 2 (z-(r/2) • e)) =
      smoothSourceField 2 L ω (coordinates 2 z-(r/2) • coordinates 2 e)
    rw [map_sub,map_smul]
  · change smoothSourceField 2 L ω (coordinates 2 (z+(r/2) • e)) =
      smoothSourceField 2 L ω (coordinates 2 z+(r/2) • coordinates 2 e)
    rw [map_add,map_smul]
  · change fderiv ℝ (actualField 2 L ω) (z-(r/2) • e) e =
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z-(r/2) • coordinates 2 e) (coordinates 2 e)
    simpa only [map_sub,map_smul] using physical_first hL ω (z-(r/2) • e) e
  · change fderiv ℝ (actualField 2 L ω) (z+(r/2) • e) e =
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z+(r/2) • coordinates 2 e) (coordinates 2 e)
    simpa only [map_add,map_smul] using physical_first hL ω (z+(r/2) • e) e
  · change fderiv ℝ (actualField 2 L ω) (z-(r/2) • e) n =
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z-(r/2) • coordinates 2 e) (coordinates 2 n)
    simpa only [map_sub,map_smul] using physical_first hL ω (z-(r/2) • e) n
  · change fderiv ℝ (actualField 2 L ω) (z+(r/2) • e) n =
      fderiv ℝ (smoothSourceField 2 L ω) (coordinates 2 z+(r/2) • coordinates 2 e) (coordinates 2 n)
    simpa only [map_add,map_smul] using physical_first hL ω (z+(r/2) • e) n

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
  have he : residualCoefficient a (framedConfluentCoefficient L z R 0)
      (0 : Matrix (Fin 7) (Fin 0) ℝ) = framedConfluentCoefficient L z R 0 := by
    funext i m
    simp only [residualCoefficient,Matrix.zero_apply,zero_mul,Finset.sum_const_zero,sub_zero]
  rw [he] at hh
  exact hh

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

-- INTEGRATED_COMPACT_BEGIN
namespace I4SourceFramedConfluentCovariance
/-
TEXT ONLY. Insert inside namespace I4SourceFramedConfluentCovariance after
pairCoefficient_bound and the shared definitions. No producer declaration
is redeclared here. The extra imports are listed in IMPORTS.txt.
-/

private theorem compact_mode_smooth (L : ℝ) (m : SourceMode 2) :
    ContDiff ℝ (⊤ : ℕ∞) (modeCoefficient 2 L m) :=
  mode_smooth L m

private theorem compact_mode_iterated_continuous (L : ℝ) (m : SourceMode 2) (k : ℕ) :
    Continuous (fun p : (Fin 2 → ℝ) × (Fin k → (Fin 2 → ℝ)) =>
      iteratedFDeriv ℝ k (modeCoefficient 2 L m) p.1 p.2) := by
  have h := (compact_mode_smooth L m).continuous_iteratedFDeriv (m := k)
    (by simp)
  exact continuous_eval.comp ((h.comp continuous_fst).prodMk continuous_snd)

private theorem compact_peano_continuous (L : ℝ) (m : SourceMode 2) (i : Fin 7) :
    Continuous (fun p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ =>
      peanoRows (modeCoefficient 2 L m) p.1.1 p.1.2.1 p.1.2.2 p.2 i) := by
  have hf := (compact_mode_smooth L m).continuous
  have hd := (compact_mode_smooth L m).continuous_fderiv
    (by simp)
  have h2 := compact_mode_iterated_continuous L m 2
  have h3 := compact_mode_iterated_continuous L m 3
  have h22 : Continuous (fun p :
      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m)
        (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1)
        ![p.1.1.2.1, p.1.1.2.1]) := by
    exact h2.comp (show Continuous (fun p :
      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
      (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1, ![p.1.1.2.1, p.1.1.2.1])) by fun_prop)
  have h2n : Continuous (fun p :
      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m)
        (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1)
        ![p.1.1.2.1, p.1.1.2.2]) := by
    exact h2.comp (show Continuous (fun p :
      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
      (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1, ![p.1.1.2.1, p.1.1.2.2])) by fun_prop)
  have h33 : Continuous (fun p :
      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
      (1 / 4 - p.2 ^ 2) * iteratedFDeriv ℝ 3 (modeCoefficient 2 L m)
        (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1)
        ![p.1.1.2.1, p.1.1.2.1, p.1.1.2.1]) := by
    have hh : Continuous (fun p :
        (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
        iteratedFDeriv ℝ 3 (modeCoefficient 2 L m)
          (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1)
          ![p.1.1.2.1, p.1.1.2.1, p.1.1.2.1]) := by
      exact h3.comp (show Continuous (fun p :
        (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
        (p.1.1.1 + (p.1.2 * p.2) • p.1.1.2.1,
          ![p.1.1.2.1, p.1.1.2.1, p.1.1.2.1])) by fun_prop)
    exact (show Continuous (fun p :
      (((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) × ℝ =>
      (1 / 4 : ℝ) - p.2 ^ 2) by fun_prop).mul hh
  have hi22 := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous' (μ := volume)
    (f := fun (p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) t =>
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p.1.1 + (p.2*t) • p.1.2.1)
        ![p.1.2.1,p.1.2.1]) h22 (-1 / 2 : ℝ) (1 / 2 : ℝ)
  have hi2n := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous' (μ := volume)
    (f := fun (p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) t =>
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p.1.1 + (p.2*t) • p.1.2.1)
        ![p.1.2.1,p.1.2.2]) h2n (-1 / 2 : ℝ) (1 / 2 : ℝ)
  have hi33 := intervalIntegral.continuous_parametric_intervalIntegral_of_continuous' (μ := volume)
    (f := fun (p : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ) t =>
      (1/4-t^2)*iteratedFDeriv ℝ 3 (modeCoefficient 2 L m) (p.1.1 + (p.2*t) • p.1.2.1)
        ![p.1.2.1,p.1.2.1,p.1.2.1]) h33 (-1 / 2 : ℝ) (1 / 2 : ℝ)
  fin_cases i <;> simp only [peanoRows] <;>
    first | exact hi22 | exact hi2n | exact continuous_const.mul hi33 |
      fun_prop

private abbrev CompactFrame := {u : Fin 2 → E 2 // Orthonormal ℝ u}

private theorem compact_frames_isCompact :
    IsCompact {u : Fin 2 → E 2 | Orthonormal ℝ u} := by
  have hc : IsClosed {u : Fin 2 → E 2 | Orthonormal ℝ u} := by
    simp only [orthonormal_iff_ite, Set.ofPred_forall]
    change IsClosed (⋂ i : Fin 2, ⋂ j : Fin 2,
      {u : Fin 2 → E 2 | inner ℝ (u i) (u j) = if i = j then 1 else 0})
    exact isClosed_iInter (fun i => isClosed_iInter (fun j =>
      isClosed_eq (by fun_prop) continuous_const))
  apply (isCompact_closedBall (0 : Fin 2 → E 2) 1).of_isClosed_subset hc
  intro u hu
  rw [Metric.mem_closedBall, dist_zero_right]
  exact (pi_norm_le_iff_of_nonneg (by norm_num)).2
    (fun i => (hu.norm_eq_one i).le)

private instance compactFrame_compactSpace : CompactSpace CompactFrame :=
  isCompact_iff_compactSpace.mp compact_frames_isCompact

private def compact_frame_basis (u : CompactFrame) :
    OrthonormalBasis (Fin 2) ℝ (E 2) :=
  OrthonormalBasis.mk u.property
    ((u.property.linearIndependent.span_eq_top_of_card_eq_finrank'
      (by simp [E])).ge)

private theorem compact_frame_basis_apply (u : CompactFrame) (i : Fin 2) :
    compact_frame_basis u i = u.val i := by
  simp [compact_frame_basis]

private def compact_midpoints (L : ℝ) : Set (E 2) :=
  {z | ∀ a : Fin 2, |coordinates 2 z a| ≤ |L| / 2}

private theorem compact_midpoints_isCompact (L : ℝ) :
    IsCompact (compact_midpoints L) := by
  have hh := (isCompact_Icc : IsCompact
    (Set.Icc (fun _ : Fin 2 => -(|L| / 2)) (fun _ : Fin 2 => |L| / 2))).image
      (coordinates 2).symm.continuous
  convert hh using 1
  ext z
  constructor
  · intro hz
    refine ⟨coordinates 2 z, ?_, by simp⟩
    exact ⟨fun a => (abs_le.mp (hz a)).1, fun a => (abs_le.mp (hz a)).2⟩
  · rintro ⟨x, hx, rfl⟩ a
    change |coordinates 2 ((coordinates 2).symm x) a| ≤ |L|/2
    rw [(coordinates 2).apply_symm_apply x]
    exact abs_le.mpr ⟨hx.1 a, hx.2 a⟩

private def compact_parameters (L : ℝ) : Set ((E 2 × CompactFrame) × ℝ) :=
  (compact_midpoints L ×ˢ Set.univ) ×ˢ Set.Icc 0 1

private theorem compact_parameters_isCompact (L : ℝ) :
    IsCompact (compact_parameters L) :=
  ((compact_midpoints_isCompact L).prod isCompact_univ).prod isCompact_Icc

private def compact_gram (L : ℝ) (p : (E 2 × CompactFrame) × ℝ) :
    Matrix (Fin 7) (Fin 7) ℝ :=
  pairCovariance L p.1.1 (p.1.2.val 0) (p.1.2.val 1) p.2

private theorem compact_coefficient_continuous (L : ℝ) (i : Fin 7) (m : SourceMode 2) :
    Continuous (fun p : (E 2 × CompactFrame) × ℝ =>
      pairCoefficient L p.1.1 (p.1.2.val 0) (p.1.2.val 1) p.2 i m) := by
  change Continuous (fun p : (E 2 × CompactFrame) × ℝ =>
    peanoRows (modeCoefficient 2 L m) (coordinates 2 p.1.1)
      (coordinates 2 (p.1.2.val 0)) (coordinates 2 (p.1.2.val 1)) p.2 i)
  have hz : Continuous (fun p : (E 2 × CompactFrame) × ℝ => coordinates 2 p.1.1) :=
    (coordinates 2).continuous.comp (continuous_fst.comp continuous_fst)
  have hu : Continuous (fun p : (E 2 × CompactFrame) × ℝ => p.1.2.val) :=
    continuous_subtype_val.comp (continuous_snd.comp continuous_fst)
  have he : Continuous (fun p : (E 2 × CompactFrame) × ℝ => coordinates 2 (p.1.2.val 0)) :=
    (coordinates 2).continuous.comp ((continuous_apply (0 : Fin 2)).comp hu)
  have hn : Continuous (fun p : (E 2 × CompactFrame) × ℝ => coordinates 2 (p.1.2.val 1)) :=
    (coordinates 2).continuous.comp ((continuous_apply (1 : Fin 2)).comp hu)
  have hg : Continuous (fun p : (E 2 × CompactFrame) × ℝ =>
      ((coordinates 2 p.1.1, coordinates 2 (p.1.2.val 0),
        coordinates 2 (p.1.2.val 1)),p.2)) :=
    (hz.prodMk (he.prodMk hn)).prodMk continuous_snd
  have h := Continuous.comp
    (f := fun q : ((Fin 2 → ℝ) × (Fin 2 → ℝ) × (Fin 2 → ℝ)) × ℝ =>
      peanoRows (modeCoefficient 2 L m) q.1.1 q.1.2.1 q.1.2.2 q.2 i)
    (g := fun p : (E 2 × CompactFrame) × ℝ =>
      ((coordinates 2 p.1.1, coordinates 2 (p.1.2.val 0),
        coordinates 2 (p.1.2.val 1)),p.2))
    (compact_peano_continuous L m i) hg
  simpa only [Function.comp_def] using h

private theorem compact_gram_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (compact_gram L) := by
  apply continuous_pi
  intro i
  apply continuous_pi
  intro j
  change Continuous (fun p : (E 2 × CompactFrame) × ℝ =>
    ∑' m, pairCoefficient L p.1.1 (p.1.2.val 0) (p.1.2.val 1) p.2 i m *
      pairCoefficient L p.1.1 (p.1.2.val 0) (p.1.2.val 1) p.2 j m)
  apply continuous_tsum
  · intro m
    exact (compact_coefficient_continuous L i m).mul
      (compact_coefficient_continuous L j m)
  · exact envelope_square_summable hL
  · intro m p
    rw [Real.norm_eq_abs, abs_mul]
    exact mul_le_mul
      (pairCoefficient_bound hL _ _ _ _
        ((p.1.2.property.norm_eq_one 0).le)
        ((p.1.2.property.norm_eq_one 1).le) i m)
      (pairCoefficient_bound hL _ _ _ _
        ((p.1.2.property.norm_eq_one 0).le)
        ((p.1.2.property.norm_eq_one 1).le) j m)
      (abs_nonneg _) (envelope_nonneg L m)

private theorem compact_gram_hermitian (L : ℝ) (p : (E 2 × CompactFrame) × ℝ) :
    (compact_gram L p).IsHermitian := by
  ext i j
  simp only [Matrix.conjTranspose_apply, star_trivial]
  change (∑' m, _ * _) = ∑' m, _ * _
  apply tsum_congr
  intro m
  ring

private theorem compact_uniform_contact {L : ℝ} (hL : L ≠ 0) :
    UniformContactLimit L := by
  intro eps heps
  let f : ((E 2 × CompactFrame) × ℝ) → (Fin 7 × Fin 7 → ℝ) :=
    fun p ij => compact_gram L p ij.1 ij.2
  have hf : Continuous f := by
    apply continuous_pi
    intro ij
    exact (continuous_apply ij.2).comp ((continuous_apply ij.1).comp
      (compact_gram_continuous hL))
  have hu := (compact_parameters_isCompact L).uniformContinuousOn_of_continuous hf.continuousOn
  obtain ⟨d, hd, hdist⟩ := Metric.uniformContinuousOn_iff.mp hu eps heps
  refine ⟨min (d / 2) 1, lt_min (half_pos hd) zero_lt_one, ?_⟩
  intro z hz R r hr hrδ i j
  let u : CompactFrame := ⟨fun a => R a, R.orthonormal⟩
  have hr1 : r ≤ 1 := hrδ.trans (min_le_right _ _)
  have hrd : r < d := lt_of_le_of_lt
    (hrδ.trans (min_le_left _ _)) (half_lt_self hd)
  have hp : ((z, u), r) ∈ compact_parameters L := ⟨⟨hz, mem_univ _⟩, hr, hr1⟩
  have h0 : ((z, u), 0) ∈ compact_parameters L :=
    ⟨⟨hz, mem_univ _⟩, le_rfl, zero_le_one⟩
  have he := hdist ((z, u), r) hp ((z, u), 0) h0 (by
    simpa [Prod.dist_eq, Real.dist_eq, abs_of_nonneg hr] using And.intro hd hrd)
  have hij : dist (f ((z,u),r) (i,j)) (f ((z,u),0) (i,j)) < eps :=
    lt_of_le_of_lt (dist_le_pi_dist (f ((z,u),r)) (f ((z,u),0)) (i,j)) he
  change |compact_gram L ((z,u),r) i j - compact_gram L ((z,u),0) i j| < eps
  simpa only [Real.dist_eq, f] using hij

private def compact_square (v : Fin 7 → ℝ) : ℝ := ∑ i, (v i) ^ 2

private def compact_quad (G : Matrix (Fin 7) (Fin 7) ℝ) (v : Fin 7 → ℝ) : ℝ :=
  ∑ i, ∑ j, v i * G i j * v j

private theorem compact_quad_dot (G : Matrix (Fin 7) (Fin 7) ℝ) (v : Fin 7 → ℝ) :
    compact_quad G v = v ⬝ᵥ (G *ᵥ v) := by
  simp [compact_quad, dotProduct, Matrix.mulVec, Finset.mul_sum, mul_assoc]

private theorem compact_quad_smul (G : Matrix (Fin 7) (Fin 7) ℝ)
    (a : ℝ) (v : Fin 7 → ℝ) :
    compact_quad G (a • v) = a ^ 2 * compact_quad G v := by
  simp only [compact_quad, Pi.smul_apply, smul_eq_mul]
  simp_rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

private theorem compact_square_nonneg (v : Fin 7 → ℝ) : 0 ≤ compact_square v :=
  Finset.sum_nonneg (fun _ _ => sq_nonneg _)

private theorem compact_square_eq_zero {v : Fin 7 → ℝ} :
    compact_square v = 0 ↔ v = 0 := by
  constructor
  · intro hv
    funext i
    have hi : (v i) ^ 2 ≤ compact_square v :=
      Finset.single_le_sum (fun j _ => sq_nonneg (v j)) (Finset.mem_univ i)
    have : (v i) ^ 2 = 0 := le_antisymm (hv ▸ hi) (sq_nonneg _)
    exact sq_eq_zero_iff.mp this
  · rintro rfl
    simp [compact_square]

private def compact_unit : Set (Fin 7 → ℝ) := {v | compact_square v = 1}

private theorem compact_unit_isCompact : IsCompact compact_unit := by
  have hc : IsClosed compact_unit := isClosed_eq (by
    unfold compact_square
    fun_prop) continuous_const
  apply (isCompact_closedBall (0 : Fin 7 → ℝ) 1).of_isClosed_subset hc
  intro v hv
  rw [Metric.mem_closedBall, dist_zero_right]
  apply (pi_norm_le_iff_of_nonneg (by norm_num)).2
  intro i
  have hi : (v i) ^ 2 ≤ (1 : ℝ) := by
    calc
      (v i) ^ 2 ≤ compact_square v :=
        Finset.single_le_sum (fun j _ => sq_nonneg (v j)) (Finset.mem_univ i)
      _ = 1 := hv
  rw [Real.norm_eq_abs]
  nlinarith [sq_abs (v i), abs_nonneg (v i)]

private theorem compact_normalize_bounds (G : Matrix (Fin 7) (Fin 7) ℝ)
    (a b : ℝ)
    (hb : ∀ w ∈ compact_unit, a ≤ compact_quad G w ∧ compact_quad G w ≤ b)
    (v : Fin 7 → ℝ) :
    a * compact_square v ≤ compact_quad G v ∧
      compact_quad G v ≤ b * compact_square v := by
  by_cases hv : v = 0
  · subst v
    simp [compact_quad, compact_square]
  have hs : 0 < compact_square v :=
    lt_of_le_of_ne (compact_square_nonneg v)
      (Ne.symm (fun h => hv (compact_square_eq_zero.mp h)))
  let c : ℝ := (Real.sqrt (compact_square v))⁻¹
  let w : Fin 7 → ℝ := c • v
  have hsq : (Real.sqrt (compact_square v)) ^ 2 = compact_square v :=
    Real.sq_sqrt hs.le
  have hc : c ^ 2 * compact_square v = 1 := by
    dsimp [c]
    rw [inv_pow, hsq, inv_mul_cancel₀ hs.ne']
  have hw : w ∈ compact_unit := by
    change (∑ i, (c * v i) ^ 2) = 1
    simp_rw [mul_pow, ← Finset.mul_sum]
    exact hc
  have hq : compact_quad G v = compact_square v * compact_quad G w := by
    dsimp [w]
    rw [compact_quad_smul]
    calc
      compact_quad G v = (c ^ 2 * compact_square v) * compact_quad G v := by rw [hc, one_mul]
      _ = compact_square v * (c ^ 2 * compact_quad G v) := by ring
  rw [hq]
  constructor
  · simpa [mul_comm] using mul_le_mul_of_nonneg_left (hb w hw).1 hs.le
  · simpa [mul_comm] using mul_le_mul_of_nonneg_left (hb w hw).2 hs.le

private theorem compact_quad_continuous {L : ℝ} (hL : L ≠ 0) :
    Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) =>
      compact_quad (compact_gram L p.1) p.2) := by
  unfold compact_quad
  apply continuous_finsetSum
  intro i hi
  apply continuous_finsetSum
  intro j hj
  have hg : Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) =>
      compact_gram L p.1 i j) :=
    (continuous_apply j).comp ((continuous_apply i).comp
      ((compact_gram_continuous hL).comp continuous_fst))
  have hvi : Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) => p.2 i) :=
    (continuous_apply i).comp continuous_snd
  have hvj : Continuous (fun p : ((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ) => p.2 j) :=
    (continuous_apply j).comp continuous_snd
  exact (hvi.mul hg).mul hvj

private theorem compact_entry_perturb (A B : Matrix (Fin 7) (Fin 7) ℝ)
    (eta : ℝ) (heta : 0 ≤ eta) (hAB : ∀ i j, |A i j - B i j| ≤ eta)
    (v : Fin 7 → ℝ) :
    |compact_quad A v - compact_quad B v| ≤ 7 * eta * compact_square v := by
  have hh : compact_quad A v - compact_quad B v =
      ∑ i, ∑ j, v i * (A i j - B i j) * v j := by
    simp only [compact_quad, mul_sub, sub_mul, Finset.sum_sub_distrib]
  rw [hh]
  calc
    |∑ i, ∑ j, v i * (A i j - B i j) * v j|
      ≤ ∑ i, ∑ j, |v i * (A i j - B i j) * v j| := by
        exact (Finset.abs_sum_le_sum_abs _ _).trans
          (Finset.sum_le_sum (fun i _ => Finset.abs_sum_le_sum_abs _ _))
    _ ≤ ∑ i, ∑ j, eta * ((v i) ^ 2 + (v j) ^ 2) / 2 := by
      apply Finset.sum_le_sum
      intro i hi
      apply Finset.sum_le_sum
      intro j hj
      rw [abs_mul, abs_mul]
      have h : 2 * |v i| * |v j| ≤ (v i) ^ 2 + (v j) ^ 2 := by
        nlinarith [sq_nonneg (|v i| - |v j|), sq_abs (v i), sq_abs (v j)]
      have he := mul_le_mul_of_nonneg_left (hAB i j)
        (mul_nonneg (abs_nonneg (v i)) (abs_nonneg (v j)))
      have heta' := mul_le_mul_of_nonneg_left h heta
      nlinarith [he, heta']
    _ = 7 * eta * compact_square v := by
      simp only [mul_add, add_div, Finset.sum_add_distrib]
      simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
      simp only [← Finset.sum_div, ← Finset.mul_sum, compact_square]
      ring

private theorem compact_principal_schur (G : Matrix (Fin 7) (Fin 7) ℝ)
    (gamma : ℝ) (hgamma : 0 < gamma) (hH : G.IsHermitian)
    (hlower : ∀ v : Fin 7 → ℝ,
      gamma * compact_square v ≤ v ⬝ᵥ (G *ᵥ v)) :
    let A : Matrix (Fin 6) (Fin 6) ℝ :=
      fun i j => G (Fin.castAdd 1 i) (Fin.castAdd 1 j)
    G.PosDef ∧ A.PosDef ∧ IsUnit A ∧
      gamma ≤ G 6 6 - ∑ i : Fin 6, ∑ j : Fin 6,
        G 6 (Fin.castAdd 1 i) * (A⁻¹) i j * G (Fin.castAdd 1 j) 6 := by
  let A : Matrix (Fin 6) (Fin 6) ℝ :=
    fun i j => G (Fin.castAdd 1 i) (Fin.castAdd 1 j)
  have hG : G.PosDef := Matrix.PosDef.of_dotProduct_mulVec_pos hH (by
    intro v hv
    have hs : 0 < compact_square v :=
      lt_of_le_of_ne (compact_square_nonneg v)
        (Ne.symm (fun h => hv (compact_square_eq_zero.mp h)))
    simpa only [star_trivial] using
      lt_of_lt_of_le (mul_pos hgamma hs) (hlower v))
  have hA : A.PosDef := by
    exact hG.submatrix (e := Fin.castAdd 1) (by
      intro i j h
      exact Fin.ext (congrArg (fun t : Fin 7 => t.val) h))
  let : Invertible A := hA.isUnit.invertible
  let b : Fin 6 → ℝ := fun i => G (Fin.castAdd 1 i) 6
  let x : Fin 6 → ℝ := -(A⁻¹ *ᵥ b)
  let w : Fin 7 → ℝ := Fin.snoc x 1
  have hAx : A *ᵥ x = -b := by
    dsimp [x]
    rw [Matrix.mulVec_neg, Matrix.mulVec_mulVec, Matrix.mul_inv_of_invertible,
      Matrix.one_mulVec]
  have hcast (i : Fin 6) : Fin.castAdd 1 i = i.castSucc := rfl
  have hrow (i : Fin 6) : (G *ᵥ w) i.castSucc = 0 := by
    have hi : (A *ᵥ x) i + b i = 0 := by rw [hAx]; simp
    change (∑ j : Fin 7, G i.castSucc j * w j) = 0
    rw [Fin.sum_univ_castSucc]
    change (∑ j : Fin 6, G i.castSucc j.castSucc * x j) + G i.castSucc (Fin.last 6) * 1 = 0
    rw [show (Fin.last 6 : Fin 7) = 6 from rfl, mul_one]
    simpa only [Matrix.mulVec, dotProduct, A, b, hcast] using hi
  have hqw : compact_quad G w =
      G 6 6 - ∑ i : Fin 6, ∑ j : Fin 6,
        G 6 (Fin.castAdd 1 i) * (A⁻¹) i j * G (Fin.castAdd 1 j) 6 := by
    rw [compact_quad_dot]
    change (∑ i : Fin 7, w i * (G *ᵥ w) i) = _
    rw [Fin.sum_univ_castSucc]
    simp only [w, Fin.snoc_castSucc, Fin.snoc_last, hrow, mul_zero,
      Finset.sum_const_zero, one_mul, zero_add]
    change (∑ j : Fin 7, G 6 j * w j) = _
    rw [Fin.sum_univ_castSucc]
    simp only [w, Fin.snoc_castSucc, Fin.snoc_last, mul_one]
    calc
      (∑ i : Fin 6, G 6 i.castSucc * x i) + G 6 6 =
          G 6 6 - ∑ i : Fin 6, ∑ j : Fin 6,
            G 6 i.castSucc * ((A⁻¹) i j * b j) := by
        simp only [x, Pi.neg_apply, Matrix.mulVec, dotProduct,
          Finset.mul_sum, mul_neg, Finset.sum_neg_distrib]
        ring
      _ = G 6 6 - ∑ i : Fin 6, ∑ j : Fin 6,
          G 6 (Fin.castAdd 1 i) * (A⁻¹) i j * G (Fin.castAdd 1 j) 6 := by
        congr 1
        apply Finset.sum_congr rfl
        intro i hi
        apply Finset.sum_congr rfl
        intro j hj
        simp only [b, hcast]
        ring
  have hsw : 1 ≤ compact_square w := by
    unfold compact_square
    rw [Fin.sum_univ_castSucc]
    simp only [w,
      Fin.snoc_castSucc, Fin.snoc_last, one_pow]
    exact le_add_of_nonneg_left (Finset.sum_nonneg (fun _ _ => sq_nonneg _))
  refine ⟨hG, hA, hA.isUnit, ?_⟩
  rw [← hqw]
  calc
    gamma ≤ gamma * compact_square w := by nlinarith
    _ ≤ compact_quad G w := by simpa [compact_quad_dot] using hlower w

/- The only rank input below is PRIVATE. Production discharges it from the
   actual finite original-source contact witnesses before invoking this theorem. -/
private theorem compact_contact_bounds {L : ℝ} (hL : L ≠ 0)
    (hcontact : ∀ z : E 2, ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2),
      (framedConfluentCovariance L z R 0).PosDef) :
    UniformContactLimit L ∧ UniformCovarianceFloor L := by
  have hlimit : UniformContactLimit L := compact_uniform_contact hL
  refine ⟨hlimit, ?_⟩
  let K : Set ((E 2 × CompactFrame) × (Fin 7 → ℝ)) :=
    (compact_midpoints L ×ˢ Set.univ) ×ˢ compact_unit
  have hK : IsCompact K :=
    ((compact_midpoints_isCompact L).prod isCompact_univ).prod compact_unit_isCompact
  let Q0 : ((E 2 × CompactFrame) × (Fin 7 → ℝ)) → ℝ :=
    fun p => compact_quad (compact_gram L (p.1, 0)) p.2
  have hQ0 : Continuous Q0 := by
    exact (compact_quad_continuous hL).comp
      (show Continuous (fun p : (E 2 × CompactFrame) × (Fin 7 → ℝ) =>
        ((p.1,(0:ℝ)),p.2)) by fun_prop)
  have hpositive : ∀ p ∈ K, 0 < Q0 p := by
    intro p hp
    have hv : p.2 ≠ 0 := by
      intro hv
      have hh : compact_square p.2 = 1 := hp.2
      simp [hv, compact_square] at hh
    have hg := (hcontact p.1.1 (compact_frame_basis p.1.2)).dotProduct_mulVec_pos hv
    simpa only [Q0, compact_quad_dot, compact_gram, pairCovariance,
      framedConfluentCovariance, framedConfluentCoefficient,
      compact_frame_basis_apply, star_trivial] using hg
  obtain ⟨m, hm, hmle⟩ := hK.exists_forall_le' hQ0.continuousOn hpositive
  let KT : Set (((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ)) :=
    compact_parameters L ×ˢ compact_unit
  have hKT : IsCompact KT :=
    (compact_parameters_isCompact L).prod compact_unit_isCompact
  let QT : (((E 2 × CompactFrame) × ℝ) × (Fin 7 → ℝ)) → ℝ :=
    fun p => compact_quad (compact_gram L p.1) p.2
  obtain ⟨M, hM⟩ := hKT.bddAbove_image (compact_quad_continuous hL).continuousOn
  have heps : 0 < m / 14 := div_pos hm (by norm_num)
  obtain ⟨d, hd, hdlim⟩ := hlimit (m / 14) heps
  let gamma : ℝ := m / 2
  let Lambda : ℝ := max M 1
  let delta : ℝ := min d (min 1 (|L| / 8))
  have hgamma : 0 < gamma := half_pos hm
  have hLambda : 0 < Lambda := lt_of_lt_of_le zero_lt_one (le_max_right _ _)
  have hdelta : 0 < delta := by
    exact lt_min hd (lt_min zero_lt_one (div_pos (abs_pos.mpr hL) (by norm_num)))
  have hdelta1 : delta ≤ 1 :=
    (min_le_right _ _).trans (min_le_left _ _)
  have hdeltaL : delta ≤ |L| / 8 :=
    (min_le_right _ _).trans (min_le_right _ _)
  refine ⟨gamma, Lambda, delta, hgamma, hLambda, hdelta, hdelta1, hdeltaL, ?_⟩
  intro z hz R r hr hrδ
  let u : CompactFrame := ⟨fun a => R a, R.orthonormal⟩
  let p : (E 2 × CompactFrame) × ℝ := ((z, u), r)
  let G : Matrix (Fin 7) (Fin 7) ℝ := compact_gram L p
  have hp : p ∈ compact_parameters L :=
    ⟨⟨hz, mem_univ _⟩, hr, hrδ.trans hdelta1⟩
  have hrd : r ≤ d := hrδ.trans (min_le_left _ _)
  have hentry : ∀ i j : Fin 7,
      |G i j - compact_gram L ((z, u), 0) i j| ≤ m / 14 := by
    intro i j
    exact (hdlim z hz R r hr hrd i j).le
  have hunit : ∀ w ∈ compact_unit,
      gamma ≤ compact_quad G w ∧ compact_quad G w ≤ Lambda := by
    intro w hw
    have hcontactmin : m ≤ compact_quad (compact_gram L ((z, u), 0)) w :=
      hmle ((z, u), w) ⟨⟨hz, mem_univ _⟩, hw⟩
    have hpert := compact_entry_perturb G (compact_gram L ((z, u), 0))
      (m / 14) heps.le hentry w
    have hws : compact_square w = 1 := hw
    have hupp : compact_quad G w ≤ M := by
      change QT (p,w) ≤ M
      exact hM (a := QT (p,w)) ⟨(p,w),⟨hp,hw⟩,rfl⟩
    refine ⟨?_, hupp.trans (le_max_left _ _)⟩
    rw [hws] at hpert
    have hminus := (abs_le.mp hpert).1
    dsimp [gamma]
    nlinarith
  have hquad : ∀ v : Fin 7 → ℝ,
      gamma * compact_square v ≤ v ⬝ᵥ (G *ᵥ v) ∧
        v ⬝ᵥ (G *ᵥ v) ≤ Lambda * compact_square v := by
    intro v
    simpa only [compact_quad_dot] using compact_normalize_bounds G gamma Lambda hunit v
  have hschur := compact_principal_schur G gamma hgamma
    (compact_gram_hermitian L p) (fun v => (hquad v).1)
  exact ⟨hquad, hschur.1, hschur.2.1, hschur.2.2.1, hschur.2.2.2⟩

end I4SourceFramedConfluentCovariance
-- INTEGRATED_COMPACT_END

namespace I4SourceFramedConfluentCovariance

/-- One explicit every-order envelope and a contact limit uniform in midpoint and both frame orientations. -/
theorem framedConfluent_family_bounds {L : ℝ} (hL : L ≠ 0) :
    let A : SourceMode 2 → ℝ := fun m => 8*∑ j : Fin 4, orderModeBound (j:ℕ) 2 L m
    (∀ m, 0 ≤ A m) ∧
    (∀ ell : ℕ, Summable (fun m => orderModeBound ell 2 L m*A m)) ∧
    (∀ z : E 2, ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ, ∀ i : Fin 7, ∀ m,
      |framedConfluentCoefficient L z R r i m| ≤ A m) ∧
    (∀ eps : ℝ, 0 < eps → ∃ delta : ℝ, 0 < delta ∧
      ∀ z : E 2, (∀ a : Fin 2, |coordinates 2 z a| ≤ |L|/2) →
        ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ,
          0 ≤ r → r ≤ delta → ∀ i j : Fin 7,
            |framedConfluentCovariance L z R r i j-framedConfluentCovariance L z R 0 i j| < eps) := by
  change (∀ m, 0 ≤ envelope L m) ∧
    (∀ ell : ℕ, Summable (fun m => orderModeBound ell 2 L m*envelope L m)) ∧
    (∀ z : E 2, ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ, ∀ i : Fin 7, ∀ m,
      |framedConfluentCoefficient L z R r i m| ≤ envelope L m) ∧ UniformContactLimit L
  refine ⟨envelope_nonneg L,envelope_weighted_summable hL,?_,
    (compact_contact_bounds hL (contact_posDef hL)).1⟩
  intro z R r i m
  exact pairCoefficient_bound hL z (R 0) (R 1) r (R.norm_eq_one 0).le (R.norm_eq_one 1).le i m

/-- Derived compact-uniform seven-row floor, principal invertibility and the same quantitative Schur floor. -/
theorem framedConfluent_covariance_uniform_floor {L : ℝ} (hL : L ≠ 0) :
    ∃ gamma Lambda delta : ℝ, 0 < gamma ∧ 0 < Lambda ∧ 0 < delta ∧ delta ≤ 1 ∧ delta ≤ |L|/8 ∧
      ∀ z : E 2, (∀ a : Fin 2, |coordinates 2 z a| ≤ |L|/2) →
        ∀ R : OrthonormalBasis (Fin 2) ℝ (E 2), ∀ r : ℝ, 0 ≤ r → r ≤ delta →
          let G := framedConfluentCovariance L z R r
          let G6 : Matrix (Fin 6) (Fin 6) ℝ := fun i j => G (Fin.castAdd 1 i) (Fin.castAdd 1 j)
          (∀ v : Fin 7 → ℝ, gamma*(∑ i, (v i)^2) ≤ v ⬝ᵥ (G *ᵥ v) ∧
            v ⬝ᵥ (G *ᵥ v) ≤ Lambda*(∑ i, (v i)^2)) ∧
          G.PosDef ∧ G6.PosDef ∧ IsUnit G6 ∧
          gamma ≤ G 6 6-∑ i : Fin 6, ∑ j : Fin 6,
            G 6 (Fin.castAdd 1 i)*(G6⁻¹) i j*G (Fin.castAdd 1 j) 6 :=
  (compact_contact_bounds hL (contact_posDef hL)).2

end I4SourceFramedConfluentCovariance
