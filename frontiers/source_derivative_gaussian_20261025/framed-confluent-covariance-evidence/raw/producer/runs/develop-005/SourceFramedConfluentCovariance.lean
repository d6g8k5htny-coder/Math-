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
open I4SourceFiniteTrig I4SourceFinitePinKernel I4SourceRemoteJetWitness
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
  have ht : HasSum (fun m => ((a m+b m)/2)*η m) ((scalarSeries a η+scalarSeries b η)/2) :=
    hs.congr (fun m => by ring)
  exact ht.tsum_eq

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
    simpa only [derivativeCoefficient,iteratedFDeriv_zero_apply] using
      (smoothSourceField_derivative_series 2 hL ω 0 q (fun i => Fin.elim0 i)).symm
  have hs1 (q v : Fin 2 → ℝ) :
      Summable (fun m => fderiv ℝ (modeCoefficient 2 L m) q v*sampleInclusion 2 L ω m) := by
    simpa only [derivativeCoefficient,iteratedFDeriv_one_apply] using
      I4SourceSmoothConditional.derivativeCoefficient_weighted_summable hL ω 1 q (fun _ => v)
  have hv1 (q v : Fin 2 → ℝ) : scalarSeries (fun m => fderiv ℝ (modeCoefficient 2 L m) q v)
      (sampleInclusion 2 L ω) = fderiv ℝ (smoothSourceField 2 L ω) q v := by
    simpa only [derivativeCoefficient,iteratedFDeriv_one_apply] using
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
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p+(r*t) • e) ![e,e]) (sampleInclusion 2 L ω) = _
    simpa only [derivativeCoefficient,one_mul] using
      derivative_peano_series hL ω 2 p e r ![e,e] (fun _ => 1) continuous_const (fun _ _ => by norm_num)
  · change scalarSeries (fun m => ∫ t in (-1/2:ℝ)..(1/2:ℝ),
      iteratedFDeriv ℝ 2 (modeCoefficient 2 L m) (p+(r*t) • e) ![e,n]) (sampleInclusion 2 L ω) = _
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

end I4SourceFramedConfluentCovariance
