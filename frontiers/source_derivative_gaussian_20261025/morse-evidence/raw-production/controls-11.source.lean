import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Topology.DiscreteSubset
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.MeasureTheory.Function.Jacobian
import Mathlib.Analysis.Normed.Operator.Prod
import Mathlib.Topology.Algebra.Module.Determinant
import Mathlib.LinearAlgebra.FiniteDimensional.Basic
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Analysis.Calculus.FDeriv.Linear
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.MeasureTheory.Constructions.Pi
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import SourceSmoothConditionalKernel
import SourceSmoothCarrier
import Mathlib.Tactic.FinCases
import Mathlib.MeasureTheory.Constructions.BorelSpace.Order
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.Bases
import Mathlib.Algebra.Order.Archimedean.Basic
import SourceDerivativeGaussian
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Tactic.Linarith
import SourceContactCovariance

/-! Actual source Morse incidence: the equal-dimensional Sard argument is joined
to the literal four original Fourier coefficients and the unchanged smooth law.
Helper lineage and all earlier verification remain attributed to their authors. -/

/-! Preserved author-side helper: lean-sard-route/TrigonometricMorseSard.lean -/

set_option autoImplicit false

set_option autoImplicit false

noncomputable section

namespace I4ActualSourceMorse

/-- The normal equations force a singular incidence differential whenever the
spatial Hessian is singular. No finite-dimensional hypothesis is needed for
the noninjectivity conclusion. -/
theorem incidence_noninjective_of_normal_equations
    {E Z : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup Z] [NormedSpace ℝ Z]
    (D : (E × Z) →L[ℝ] (E × Z)) (B H : E →L[ℝ] E)
    (hB : Function.Injective B) (hH : ¬ Function.Injective H)
    (hDz : ∀ v : E, (D (v,0)).2 = 0)
    (hDx : ∀ v : E, B ((D (v,0)).1) = -H v) :
    ¬ Function.Injective D := by
  intro hD
  apply hH
  intro v w hvw
  have heq : D (v,0) = D (w,0) := by
    apply Prod.ext
    · apply hB
      rw [hDx, hDx, hvw]
    · rw [hDz, hDz]
  exact congrArg Prod.fst (hD heq)

/-- Finite-dimensional determinant form of the incidence normal-equation
criterion, in the exact continuous-linear-map API used by the equal-dimension
Sard theorem. -/
theorem incidence_det_eq_zero_of_normal_equations
    {E Z : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [NormedAddCommGroup Z] [NormedSpace ℝ Z]
    [FiniteDimensional ℝ E] [FiniteDimensional ℝ Z]
    (D : (E × Z) →L[ℝ] (E × Z)) (B H : E →L[ℝ] E)
    (hB : Function.Injective B) (hH : ¬ Function.Injective H)
    (hDz : ∀ v : E, (D (v,0)).2 = 0)
    (hDx : ∀ v : E, B ((D (v,0)).1) = -H v) :
    D.det = 0 := by
  apply LinearMap.det_eq_zero_iff_ker_ne_bot.mpr
  intro hker
  exact incidence_noninjective_of_normal_equations D B H hB hH hDz hDx
    (LinearMap.ker_eq_bot.mp hker)

end I4ActualSourceMorse


noncomputable section

namespace I4ActualSourceMorse

abbrev ChannelSpace (n : ℕ) := Fin n → ℝ

def twoChannelIncidence {n : ℕ} (g b c : ChannelSpace n → ChannelSpace n)
    (p : ChannelSpace n × ChannelSpace n) : ChannelSpace n × ChannelSpace n :=
  ((fun i => -(g p.1 i + c p.1 i * p.2 i) / b p.1 i), p.2)

def twoChannelGradientFamily {n : ℕ} (g b c : ChannelSpace n → ChannelSpace n)
    (x : ChannelSpace n) (a : ChannelSpace n × ChannelSpace n) : ChannelSpace n :=
  fun i => g x i + b x i * a.1 i + c x i * a.2 i

private theorem scalar_quotient_hasFDerivAt
    {X : Type*} [NormedAddCommGroup X] [NormedSpace ℝ X]
    {f b : X → ℝ} {f' b' : X →L[ℝ] ℝ} {x : X}
    (hf : HasFDerivAt f f' x) (hb : HasFDerivAt b b' x) (hb0 : b x ≠ 0) :
    HasFDerivAt (fun y => f y / b y)
      ((b x ^ 2)⁻¹ • (b x • f' - f x • b')) x := by
  convert hf.mul ((hasDerivAt_inv hb0).comp_hasFDerivAt x hb) using 1
  · rfl
  · ext v
    simp
    field_simp
    ring

def channelDerivative {n : ℕ} (f : ChannelSpace n → ChannelSpace n)
    (x : ChannelSpace n) (i : Fin n) : ChannelSpace n →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i).comp (fderiv ℝ f x)

def channelLiftDerivative {n : ℕ} (f : ChannelSpace n → ChannelSpace n)
    (x : ChannelSpace n) (i : Fin n) :
    (ChannelSpace n × ChannelSpace n) →L[ℝ] ℝ :=
  (channelDerivative f x i).comp (ContinuousLinearMap.fst ℝ _ _)

def twoChannelNumeratorDerivative {n : ℕ}
    (g c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n)
    (i : Fin n) : (ChannelSpace n × ChannelSpace n) →L[ℝ] ℝ :=
  -(channelLiftDerivative g p.1 i +
    (c p.1 i) • (ContinuousLinearMap.proj i).comp (ContinuousLinearMap.snd ℝ _ _) +
    (p.2 i) • channelLiftDerivative c p.1 i)

def twoChannelIncidenceDerivative {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n) :
    (ChannelSpace n × ChannelSpace n) →L[ℝ] (ChannelSpace n × ChannelSpace n) :=
  (ContinuousLinearMap.pi fun i =>
    (b p.1 i ^ 2)⁻¹ •
      (b p.1 i • twoChannelNumeratorDerivative g c p i -
        (-(g p.1 i + c p.1 i * p.2 i)) • channelLiftDerivative b p.1 i)).prod
    (ContinuousLinearMap.snd ℝ _ _)

theorem twoChannelIncidence_hasFDerivAt {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n)
    (hg : DifferentiableAt ℝ g p.1) (hb : DifferentiableAt ℝ b p.1)
    (hc : DifferentiableAt ℝ c p.1) (hb0 : ∀ i, b p.1 i ≠ 0) :
    HasFDerivAt (twoChannelIncidence g b c) (twoChannelIncidenceDerivative g b c p) p := by
  apply HasFDerivAt.prodMk _ hasFDerivAt_snd
  apply hasFDerivAt_pi.mpr
  intro i
  have hgi := (hasFDerivAt_pi'.mp hg.hasFDerivAt i).comp p hasFDerivAt_fst
  have hbi := (hasFDerivAt_pi'.mp hb.hasFDerivAt i).comp p hasFDerivAt_fst
  have hci := (hasFDerivAt_pi'.mp hc.hasFDerivAt i).comp p hasFDerivAt_fst
  have hzi := (hasFDerivAt_apply (𝕜 := ℝ) i p.2).comp p hasFDerivAt_snd
  have hn := (hgi.add (hci.mul hzi)).neg
  have hq := scalar_quotient_hasFDerivAt hn hbi (hb0 i)
  simpa [twoChannelNumeratorDerivative, channelLiftDerivative, channelDerivative,
    add_assoc] using hq

theorem twoChannelIncidence_differentiableAt {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n)
    (hg : DifferentiableAt ℝ g p.1) (hb : DifferentiableAt ℝ b p.1)
    (hc : DifferentiableAt ℝ c p.1) (hb0 : ∀ i, b p.1 i ≠ 0) :
    DifferentiableAt ℝ (twoChannelIncidence g b c) p :=
  (twoChannelIncidence_hasFDerivAt g b c p hg hb hc hb0).differentiableAt

theorem twoChannelIncidence_critical_identity {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n)
    (hb0 : ∀ i, b p.1 i ≠ 0) :
    twoChannelGradientFamily g b c p.1 (twoChannelIncidence g b c p) = 0 := by
  funext i
  dsimp [twoChannelGradientFamily, twoChannelIncidence]
  field_simp [hb0 i]
  ring

def channelDiagonal {n : ℕ} (b : ChannelSpace n) : ChannelSpace n →L[ℝ] ChannelSpace n :=
  ContinuousLinearMap.pi fun i => b i • ContinuousLinearMap.proj i

theorem channelDiagonal_injective {n : ℕ} (b : ChannelSpace n) (hb : ∀ i, b i ≠ 0) :
    Function.Injective (channelDiagonal b) := by
  intro v w hvw
  funext i
  exact mul_left_cancel₀ (hb i) (congrFun hvw i)

theorem twoChannelGradientFamily_hasFDerivAt {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (x : ChannelSpace n)
    (a : ChannelSpace n × ChannelSpace n)
    (hg : DifferentiableAt ℝ g x) (hb : DifferentiableAt ℝ b x)
    (hc : DifferentiableAt ℝ c x) :
    HasFDerivAt (fun y => twoChannelGradientFamily g b c y a)
      (ContinuousLinearMap.pi fun i => channelDerivative g x i +
        a.1 i • channelDerivative b x i + a.2 i • channelDerivative c x i) x := by
  apply hasFDerivAt_pi.mpr
  intro i
  exact ((hasFDerivAt_pi'.mp hg.hasFDerivAt i).add
    ((hasFDerivAt_pi'.mp hb.hasFDerivAt i).mul_const (a.1 i))).add
    ((hasFDerivAt_pi'.mp hc.hasFDerivAt i).mul_const (a.2 i))

theorem twoChannelIncidence_spatial_snd_eq_zero {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n)
    (hg : DifferentiableAt ℝ g p.1) (hb : DifferentiableAt ℝ b p.1)
    (hc : DifferentiableAt ℝ c p.1) (hb0 : ∀ i, b p.1 i ≠ 0)
    (v : ChannelSpace n) :
    ((fderiv ℝ (twoChannelIncidence g b c) p) (v,0)).2 = 0 := by
  rw [(twoChannelIncidence_hasFDerivAt g b c p hg hb hc hb0).fderiv]
  rfl

theorem twoChannelIncidence_spatial_normal_equation {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (p : ChannelSpace n × ChannelSpace n)
    (hg : DifferentiableAt ℝ g p.1) (hb : DifferentiableAt ℝ b p.1)
    (hc : DifferentiableAt ℝ c p.1) (hb0 : ∀ i, b p.1 i ≠ 0)
    (v : ChannelSpace n) :
    channelDiagonal (b p.1) (((fderiv ℝ (twoChannelIncidence g b c) p) (v,0)).1) =
      -((fderiv ℝ (fun x => twoChannelGradientFamily g b c x
          (twoChannelIncidence g b c p)) p.1) v) := by
  rw [(twoChannelIncidence_hasFDerivAt g b c p hg hb hc hb0).fderiv,
    (twoChannelGradientFamily_hasFDerivAt g b c p.1
      (twoChannelIncidence g b c p) hg hb hc).fderiv]
  funext i
  simp [channelDiagonal, twoChannelIncidenceDerivative, twoChannelNumeratorDerivative,
    channelLiftDerivative, channelDerivative, twoChannelIncidence]
  field_simp [hb0 i]
  ring

end I4ActualSourceMorse
open MeasureTheory MeasureTheory.Measure Set

namespace I4ActualSourceMorse

theorem twoChannelIncidence_eq_of_critical {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) (x : ChannelSpace n)
    (a : ChannelSpace n × ChannelSpace n)
    (hb0 : ∀ i, b x i ≠ 0) (hcrit : twoChannelGradientFamily g b c x a = 0) :
    twoChannelIncidence g b c (x,a.2) = a := by
  apply Prod.ext
  · funext i
    have hi := congrFun hcrit i
    dsimp [twoChannelGradientFamily] at hi
    dsimp [twoChannelIncidence]
    apply (div_eq_iff (hb0 i)).mpr
    linear_combination -hi
  · rfl

def twoChannelDegenerateIncidenceSet {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) :
    Set (ChannelSpace n × ChannelSpace n) :=
  {p | (∀ i, b p.1 i ≠ 0) ∧
    ¬ Function.Injective (fderiv ℝ (fun x => twoChannelGradientFamily g b c x
      (twoChannelIncidence g b c p)) p.1)}

def twoChannelDegenerateCriticalParameters {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) :
    Set (ChannelSpace n × ChannelSpace n) :=
  {a | ∃ x, (∀ i, b x i ≠ 0) ∧ twoChannelGradientFamily g b c x a = 0 ∧
    ¬ Function.Injective (fderiv ℝ (fun y => twoChannelGradientFamily g b c y a) x)}

theorem twoChannelDegenerateCriticalParameters_subset_image {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n) :
    twoChannelDegenerateCriticalParameters g b c ⊆
      twoChannelIncidence g b c '' twoChannelDegenerateIncidenceSet g b c := by
  rintro a ⟨x, hb0, hcrit, hH⟩
  have heq := twoChannelIncidence_eq_of_critical g b c x a hb0 hcrit
  refine ⟨(x,a.2), ⟨hb0, ?_⟩, heq⟩
  simpa only [heq] using hH

theorem twoChannelIncidence_det_eq_zero_on_degenerate {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n)
    (hg : Differentiable ℝ g) (hb : Differentiable ℝ b) (hc : Differentiable ℝ c)
    (p : ChannelSpace n × ChannelSpace n)
    (hp : p ∈ twoChannelDegenerateIncidenceSet g b c) :
    (fderiv ℝ (twoChannelIncidence g b c) p).det = 0 := by
  apply incidence_det_eq_zero_of_normal_equations
    (fderiv ℝ (twoChannelIncidence g b c) p) (channelDiagonal (b p.1))
    (fderiv ℝ (fun x => twoChannelGradientFamily g b c x
      (twoChannelIncidence g b c p)) p.1)
    (channelDiagonal_injective (b p.1) hp.1) hp.2
  · exact twoChannelIncidence_spatial_snd_eq_zero g b c p (hg p.1) (hb p.1) (hc p.1) hp.1
  · exact twoChannelIncidence_spatial_normal_equation g b c p (hg p.1) (hb p.1) (hc p.1) hp.1

/-- The incidence image of the degenerate locus is Haar null by mathlib's
equal-dimensional Sard theorem. Only ordinary differentiability is used. -/
theorem twoChannelDegenerateIncidence_image_haar_null {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n)
    (hg : Differentiable ℝ g) (hb : Differentiable ℝ b) (hc : Differentiable ℝ c)
    (μ : Measure (ChannelSpace n × ChannelSpace n)) [IsAddHaarMeasure μ] :
    μ (twoChannelIncidence g b c '' twoChannelDegenerateIncidenceSet g b c) = 0 := by
  apply addHaar_image_eq_zero_of_det_fderivWithin_eq_zero μ
    (f' := fderiv ℝ (twoChannelIncidence g b c))
  · intro p hp
    exact (twoChannelIncidence_differentiableAt g b c p (hg p.1) (hb p.1) (hc p.1)
      hp.1).hasFDerivAt.hasFDerivWithinAt
  · exact twoChannelIncidence_det_eq_zero_on_degenerate g b c hg hb hc

/-- In one nonvanishing channel patch, all parameters admitting a degenerate
critical point form a Haar-null set. The hypotheses are source independent
and do not assume either critical-value nullity or a Morse conclusion. -/
theorem twoChannelDegenerateCriticalParameters_haar_null {n : ℕ}
    (g b c : ChannelSpace n → ChannelSpace n)
    (hg : Differentiable ℝ g) (hb : Differentiable ℝ b) (hc : Differentiable ℝ c)
    (μ : Measure (ChannelSpace n × ChannelSpace n)) [IsAddHaarMeasure μ] :
    μ (twoChannelDegenerateCriticalParameters g b c) = 0 := by
  apply le_antisymm _ bot_le
  calc
    μ (twoChannelDegenerateCriticalParameters g b c) ≤
        μ (twoChannelIncidence g b c '' twoChannelDegenerateIncidenceSet g b c) :=
      measure_mono (twoChannelDegenerateCriticalParameters_subset_image g b c)
    _ = 0 := twoChannelDegenerateIncidence_image_haar_null g b c hg hb hc μ

end I4ActualSourceMorse


noncomputable section

open MeasureTheory MeasureTheory.Measure

namespace I4ActualSourceMorse

/-- In each spatial coordinate, exchange the selected and unused coefficients
when the sine channel is selected. -/
def channelSwap {n : ℕ} (σ : Fin n → Bool) :
    ((Fin n → ℝ) × (Fin n → ℝ)) →L[ℝ] ((Fin n → ℝ) × (Fin n → ℝ)) :=
  (ContinuousLinearMap.pi fun i =>
    if σ i then (ContinuousLinearMap.proj i : (Fin n → ℝ) →L[ℝ] ℝ).comp
      (ContinuousLinearMap.snd ℝ (Fin n → ℝ) (Fin n → ℝ))
    else (ContinuousLinearMap.proj i : (Fin n → ℝ) →L[ℝ] ℝ).comp
      (ContinuousLinearMap.fst ℝ (Fin n → ℝ) (Fin n → ℝ))).prod
  (ContinuousLinearMap.pi fun i =>
    if σ i then (ContinuousLinearMap.proj i : (Fin n → ℝ) →L[ℝ] ℝ).comp
      (ContinuousLinearMap.fst ℝ (Fin n → ℝ) (Fin n → ℝ))
    else (ContinuousLinearMap.proj i : (Fin n → ℝ) →L[ℝ] ℝ).comp
      (ContinuousLinearMap.snd ℝ (Fin n → ℝ) (Fin n → ℝ)))

theorem channelSwap_involutive {n : ℕ} (σ : Fin n → Bool) :
    Function.Involutive (channelSwap σ) := by
  intro p
  apply Prod.ext <;> funext i <;> cases h : σ i <;> simp [channelSwap, h]

/-- The selected/unused convention changes only the ordering of the original
four coefficients; it preserves the literal affine gradient. -/
theorem channelSwap_gradient_identity {n : ℕ} (σ : Fin n → Bool)
    (g b c : Fin n → ℝ) (a : (Fin n → ℝ) × (Fin n → ℝ)) (i : Fin n) :
    g i + (if σ i then c i else b i) * (channelSwap σ a).1 i +
      (if σ i then b i else c i) * (channelSwap σ a).2 i =
        g i + b i * a.1 i + c i * a.2 i := by
  cases h : σ i <;> simp [channelSwap, h]
  ring

/-- Returning a null set of selected/unused parameters to the original
coefficient order preserves Haar nullity. No Gaussian permutation law is
needed for this step. -/
theorem channelSwap_image_null {n : ℕ}
    (μ : Measure ((Fin n → ℝ) × (Fin n → ℝ))) [IsAddHaarMeasure μ]
    (σ : Fin n → Bool) (s : Set ((Fin n → ℝ) × (Fin n → ℝ)))
    (hs : μ s = 0) : μ (channelSwap σ '' s) = 0 :=
  addHaar_image_eq_zero_of_differentiableOn_of_addHaar_eq_zero μ
    (channelSwap σ).differentiable.differentiableOn hs

end I4ActualSourceMorse

noncomputable section

open MeasureTheory MeasureTheory.Measure ProbabilityTheory
open scoped NNReal

namespace I4ActualSourceMorse

/-- The original independent two-coordinate Gaussian law has a density for
arbitrary means and strictly positive variances. -/
theorem gaussian_two_absolutelyContinuous (m : Fin 2 → ℝ)
    (v : Fin 2 → ℝ≥0) (hv : ∀ i, v i ≠ 0) :
    (Measure.pi fun i : Fin 2 => gaussianReal (m i) (v i)) ≪ volume := by
  let e := MeasurableEquiv.piFinTwo (fun _ : Fin 2 => ℝ)
  have hp := measurePreserving_piFinTwo (fun i : Fin 2 => gaussianReal (m i) (v i))
  have hvol := volume_preserving_piFinTwo (fun _ : Fin 2 => ℝ)
  have hprod := (gaussianReal_absolutelyContinuous (m 0) (hv 0)).prod
    (gaussianReal_absolutelyContinuous (m 1) (hv 1))
  have hmap := e.symm.measurableEmbedding.absolutelyContinuous_map hprod
  rw [(hp.symm e).map_eq] at hmap
  change (Measure.pi fun i : Fin 2 => gaussianReal (m i) (v i)) ≪
    (volume : Measure (ℝ × ℝ)).map e.symm at hmap
  rwa [(hvol.symm e).map_eq] at hmap

/-- The selected/unused grouping of four standard Gaussian coefficients is
absolutely continuous with four-dimensional Haar measure. -/
theorem gaussian_four_grouped_absolutelyContinuous :
    (Measure.pi (fun _ : Fin 2 => gaussianReal 0 1)).prod
      (Measure.pi (fun _ : Fin 2 => gaussianReal 0 1)) ≪
        (volume : Measure ((Fin 2 → ℝ) × (Fin 2 → ℝ))) := by
  exact (gaussian_two_absolutelyContinuous (fun _ => 0) (fun _ => 1)
    (fun _ => one_ne_zero)).prod
      (gaussian_two_absolutelyContinuous (fun _ => 0) (fun _ => 1)
        (fun _ => one_ne_zero))

def selectedTrigonometricChannel (A : Fin 2 → ℝ) (c : ℝ)
    (σ : Fin 2 → Bool) (x : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  if σ i then A i * c * Real.cos (c * x i)
  else -A i * c * Real.sin (c * x i)

/-- Four choices of the two selected sin/cos channels cover the spatial
domain. The signed frequency need only be nonzero. -/
theorem four_trigonometric_patches_cover (A : Fin 2 → ℝ) (c : ℝ)
    (hA : ∀ i, A i ≠ 0) (hc : c ≠ 0) (x : Fin 2 → ℝ) :
    ∃ σ : Fin 2 → Bool, ∀ i,
      selectedTrigonometricChannel A c σ x i ≠ 0 := by
  classical
  let σ : Fin 2 → Bool := fun i => decide (Real.cos (c * x i) ≠ 0)
  refine ⟨σ, fun i => ?_⟩
  by_cases hcos : Real.cos (c * x i) ≠ 0
  · simp only [selectedTrigonometricChannel, σ, decide_eq_true hcos,
      ↓reduceIte]
    exact mul_ne_zero (mul_ne_zero (hA i) hc) hcos
  · have hsin : Real.sin (c * x i) ≠ 0 := by
      intro hs
      have hh := Real.sin_sq_add_cos_sq (c * x i)
      rw [hs, not_ne_iff.mp hcos] at hh
      norm_num at hh
    simp only [selectedTrigonometricChannel, σ, decide_eq_false_iff_not.mpr hcos,
      Bool.false_eq_true, ↓reduceIte]
    exact mul_ne_zero (mul_ne_zero (neg_ne_zero.mpr (hA i)) hc) hsin

end I4ActualSourceMorse


namespace I4ActualSourceMorse

def cosineGradientChannel (A : Fin 2 → ℝ) (c : ℝ)
    (x : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  -A i * c * Real.sin (c * x i)

def sineGradientChannel (A : Fin 2 → ℝ) (c : ℝ)
    (x : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  A i * c * Real.cos (c * x i)

def unusedTrigonometricChannel (A : Fin 2 → ℝ) (c : ℝ)
    (σ : Fin 2 → Bool) (x : Fin 2 → ℝ) (i : Fin 2) : ℝ :=
  if σ i then cosineGradientChannel A c x i else sineGradientChannel A c x i

theorem cosineGradientChannel_differentiable (A : Fin 2 → ℝ) (c : ℝ) :
    Differentiable ℝ (cosineGradientChannel A c) := by
  intro x
  apply differentiableAt_pi.mpr
  intro i
  dsimp [cosineGradientChannel]
  fun_prop

theorem sineGradientChannel_differentiable (A : Fin 2 → ℝ) (c : ℝ) :
    Differentiable ℝ (sineGradientChannel A c) := by
  intro x
  apply differentiableAt_pi.mpr
  intro i
  dsimp [sineGradientChannel]
  fun_prop

theorem selectedTrigonometricChannel_differentiable (A : Fin 2 → ℝ) (c : ℝ)
    (σ : Fin 2 → Bool) : Differentiable ℝ (selectedTrigonometricChannel A c σ) := by
  intro x
  apply differentiableAt_pi.mpr
  intro i
  cases h : σ i <;> simp only [selectedTrigonometricChannel, h,
    Bool.false_eq_true, ↓reduceIte] <;> fun_prop

theorem unusedTrigonometricChannel_differentiable (A : Fin 2 → ℝ) (c : ℝ)
    (σ : Fin 2 → Bool) : Differentiable ℝ (unusedTrigonometricChannel A c σ) := by
  intro x
  apply differentiableAt_pi.mpr
  intro i
  cases h : σ i <;> simp only [unusedTrigonometricChannel, h,
    Bool.false_eq_true, ↓reduceIte, cosineGradientChannel, sineGradientChannel] <;> fun_prop

/-- The entire spatial gradient function, and hence its actual Fréchet
derivative, is unchanged by selecting and swapping the two channels. -/
theorem trigonometricChannelSwap_gradient_function_identity
    (g : (Fin 2 → ℝ) → (Fin 2 → ℝ)) (A : Fin 2 → ℝ) (c : ℝ)
    (σ : Fin 2 → Bool) (a : (Fin 2 → ℝ) × (Fin 2 → ℝ)) :
    (fun x => twoChannelGradientFamily g (selectedTrigonometricChannel A c σ)
      (unusedTrigonometricChannel A c σ) x (channelSwap σ a)) =
      (fun x => twoChannelGradientFamily g (cosineGradientChannel A c)
        (sineGradientChannel A c) x a) := by
  funext x i
  exact channelSwap_gradient_identity σ (g x) (cosineGradientChannel A c x)
    (sineGradientChannel A c x) a i

def trigonometricDegenerateCriticalParameters
    (g : (Fin 2 → ℝ) → (Fin 2 → ℝ)) (A : Fin 2 → ℝ) (c : ℝ) :
    Set ((Fin 2 → ℝ) × (Fin 2 → ℝ)) :=
  {a | ∃ x,
    twoChannelGradientFamily g (cosineGradientChannel A c) (sineGradientChannel A c) x a = 0 ∧
    ¬ Function.Injective (fderiv ℝ (fun y =>
      twoChannelGradientFamily g (cosineGradientChannel A c) (sineGradientChannel A c) y a) x)}

theorem trigonometricDegenerateCriticalParameters_subset_patch_union
    (g : (Fin 2 → ℝ) → (Fin 2 → ℝ)) (A : Fin 2 → ℝ) (c : ℝ)
    (hA : ∀ i, A i ≠ 0) (hc : c ≠ 0) :
    trigonometricDegenerateCriticalParameters g A c ⊆
      ⋃ σ : Fin 2 → Bool, channelSwap σ '' twoChannelDegenerateCriticalParameters g
        (selectedTrigonometricChannel A c σ) (unusedTrigonometricChannel A c σ) := by
  rintro a ⟨x, hcrit, hH⟩
  obtain ⟨σ, hσ⟩ := four_trigonometric_patches_cover A c hA hc x
  apply Set.mem_iUnion.mpr
  refine ⟨σ, channelSwap σ a, ?_, channelSwap_involutive σ a⟩
  have heq := trigonometricChannelSwap_gradient_function_identity g A c σ a
  refine ⟨x, hσ, ?_, ?_⟩
  · exact (congrFun heq x).trans hcrit
  · simpa only [heq] using hH

/-- Every parameter admitting a degenerate critical point is Haar exceptional.
The four sine/cosine channel patches cover every spatial point, and the
one-patch equal-dimensional Sard theorem proves the nullity in each patch. -/
theorem trigonometricDegenerateCriticalParameters_haar_null
    (g : (Fin 2 → ℝ) → (Fin 2 → ℝ)) (A : Fin 2 → ℝ) (c : ℝ)
    (hg : Differentiable ℝ g) (hA : ∀ i, A i ≠ 0) (hc : c ≠ 0)
    (μ : Measure ((Fin 2 → ℝ) × (Fin 2 → ℝ))) [IsAddHaarMeasure μ] :
    μ (trigonometricDegenerateCriticalParameters g A c) = 0 := by
  have hnull (σ : Fin 2 → Bool) :
      μ (channelSwap σ '' twoChannelDegenerateCriticalParameters g
        (selectedTrigonometricChannel A c σ) (unusedTrigonometricChannel A c σ)) = 0 :=
    channelSwap_image_null μ σ _
      (twoChannelDegenerateCriticalParameters_haar_null g
        (selectedTrigonometricChannel A c σ) (unusedTrigonometricChannel A c σ) hg
        (selectedTrigonometricChannel_differentiable A c σ)
        (unusedTrigonometricChannel_differentiable A c σ) μ)
  apply le_antisymm _ bot_le
  calc
    μ (trigonometricDegenerateCriticalParameters g A c) ≤
        μ (⋃ σ : Fin 2 → Bool, channelSwap σ '' twoChannelDegenerateCriticalParameters g
          (selectedTrigonometricChannel A c σ) (unusedTrigonometricChannel A c σ)) :=
      measure_mono (trigonometricDegenerateCriticalParameters_subset_patch_union g A c hA hc)
    _ ≤ ∑' σ : Fin 2 → Bool, μ (channelSwap σ '' twoChannelDegenerateCriticalParameters g
        (selectedTrigonometricChannel A c σ) (unusedTrigonometricChannel A c σ)) :=
      measure_iUnion_le _
    _ = 0 := by simp only [hnull, tsum_zero]

/-- The four original independent standard Gaussian coefficients avoid the
degenerate-critical parameter set. This is an immediate density transport of
the proved Haar-nullity result. -/
theorem trigonometricDegenerateCriticalParameters_gaussian_null
    (g : (Fin 2 → ℝ) → (Fin 2 → ℝ)) (A : Fin 2 → ℝ) (c : ℝ)
    (hg : Differentiable ℝ g) (hA : ∀ i, A i ≠ 0) (hc : c ≠ 0) :
    ((Measure.pi (fun _ : Fin 2 => gaussianReal 0 1)).prod
      (Measure.pi (fun _ : Fin 2 => gaussianReal 0 1)))
      (trigonometricDegenerateCriticalParameters g A c) = 0 := by
  have : IsAddHaarMeasure (volume : Measure (Fin 2 → ℝ)) :=
    isAddHaarMeasure_volume_pi (Fin 2)
  have : IsAddHaarMeasure
      ((volume : Measure (Fin 2 → ℝ)).prod (volume : Measure (Fin 2 → ℝ))) :=
    inferInstance
  exact gaussian_four_grouped_absolutelyContinuous
    (trigonometricDegenerateCriticalParameters_haar_null g A c hg hA hc volume)

end I4ActualSourceMorse

/-! Preserved author-side helper: lean-sard-route/FiniteMorseTransfer.lean -/

set_option autoImplicit false

/-! Actual finite coefficient erasure, carrier preservation and source splitting.
These new application lemmas reuse the established product Gaussian and smooth
carrier theorems. They do not assert a formal Sard/Morse theorem. -/

noncomputable section
open I4Foundation I4Source I4Smooth I4SmoothCarrier I4SourceDerivativeGaussian
open I4SourceSmoothConditional MeasureTheory ProbabilityTheory
open scoped BigOperators
set_option autoImplicit false

namespace I4ActualSourceMorse

def eraseCoefficients {I : Type*} [DecidableEq I] (B : Finset I) (η : I → ℝ) : I → ℝ :=
  fun m => if m ∈ B then 0 else η m

theorem eraseCoefficients_measurable {I : Type*} [DecidableEq I] (B : Finset I) :
    Measurable (eraseCoefficients B) := by
  apply Measurable.of_eval
  intro m
  by_cases hm : m ∈ B
  · simpa only [eraseCoefficients,hm,ite_true] using
      (measurable_const : Measurable (fun _ : I → ℝ => (0 : ℝ)))
  · simpa only [eraseCoefficients,hm,ite_false] using (measurable_pi_apply m)

def eraseSample (d : ℕ) (L : ℝ) (B : Finset (SourceMode d))
    (ω : SmoothSample d L) : SmoothSample d L :=
  ⟨eraseCoefficients B ω.val,
    (goodSample_finite_change_iff d L ω.val (eraseCoefficients B ω.val) B
      (fun m hm => by simp only [eraseCoefficients,hm,ite_false])).mp ω.property⟩

theorem eraseSample_measurable (d : ℕ) (L : ℝ) (B : Finset (SourceMode d)) :
    Measurable (eraseSample d L B) := by
  unfold eraseSample
  exact Measurable.subtype_mk ((eraseCoefficients_measurable B).comp measurable_subtype_coe)

/-- Removing any finite original coefficient block leaves the same every-order
smooth carrier, and the literal derivative splits into tail plus finite block. -/
theorem actual_derivative_finite_split {L : ℝ} (hL : L ≠ 0)
    (B : Finset (SourceMode 2)) (ω : SmoothSample 2 L)
    (k : ℕ) (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u =
      iteratedFDeriv ℝ k (smoothSourceField 2 L (eraseSample 2 L B ω)) x u +
        ∑ m ∈ B, derivativeCoefficient 2 L k x u m * ω.val m := by
  classical
  rw [smoothSourceField_derivative_series 2 hL ω,
    smoothSourceField_derivative_series 2 hL (eraseSample 2 L B ω)]
  let a := fun m => derivativeCoefficient 2 L k x u m * ω.val m
  have ha : Summable a := derivativeCoefficient_weighted_summable hL ω k x u
  have hb : Summable (fun m => if m ∈ B then a m else 0) := by
    apply summable_of_ne_finset_zero (s := B)
    intro m hm
    simp only [hm,ite_false]
  have hbsum : (∑' m, if m ∈ B then a m else 0) = ∑ m ∈ B, a m := by
    calc
      _ = ∑ m ∈ B, (if m ∈ B then a m else 0) := by
        apply tsum_eq_sum
        intro m hm
        simp only [hm,ite_false]
      _ = _ := Finset.sum_congr rfl (fun m hm => ite_eq_left hm)
  have heq : (fun m => derivativeCoefficient 2 L k x u m *
      sampleInclusion 2 L (eraseSample 2 L B ω) m) =
      (fun m => a m - (if m ∈ B then a m else 0)) := by
    funext m
    by_cases hm : m ∈ B <;> simp [eraseSample,eraseCoefficients,sampleInclusion,hm,a]
  change (∑' m, a m) = (∑' m, derivativeCoefficient 2 L k x u m *
    sampleInclusion 2 L (eraseSample 2 L B ω) m) + ∑ m ∈ B, a m
  rw [heq,ha.tsum_sub hb,hbsum]
  ring

/-- Original finite coordinates are independent of the full erased coefficient
process. This asserts no independence among derivatives or posterior coordinates. -/
theorem finite_block_indep_erased {I : Type*} [DecidableEq I] (B : Finset I) :
    IndepFun (fun η : I → ℝ => fun m : B => η m.val) (eraseCoefficients B)
      (coefficientLaw I) := by
  classical
  have hX : Measurable (fun η : I → ℝ => fun m : B => η m.val) :=
    Measurable.of_eval (fun m => measurable_pi_apply m.val)
  apply IndepFun.indepFun_process hX (fun m =>
    (measurable_pi_apply m).comp (eraseCoefficients_measurable B))
  intro T
  have hd : Disjoint B (T \ B) := Finset.disjoint_left.mpr (fun m hm hT =>
    (Finset.mem_sdiff.mp hT).2 hm)
  have hi := (coordinates_independent I).indepFun_finset B (T \ B) hd
    (fun m => measurable_pi_apply m)
  let reconstruct : (↥(T \ B) → ℝ) → T → ℝ := fun y m =>
    if hm : m.val ∈ B then 0 else y ⟨m.val,Finset.mem_sdiff.mpr ⟨m.property,hm⟩⟩
  have hm : Measurable reconstruct := by
    apply Measurable.of_eval
    intro m
    by_cases hmb : m.val ∈ B
    · simp [reconstruct,hmb]
    · simpa [reconstruct,hmb] using
        (measurable_pi_apply (⟨m.val,Finset.mem_sdiff.mpr ⟨m.property,hmb⟩⟩ : ↥(T \ B)))
  have heq : reconstruct ∘ (fun η : I → ℝ => fun m : ↥(T \ B) => η m.val) =
      (fun η => fun m : T => eraseCoefficients B η m.val) := by
    funext η m
    by_cases hmb : m.val ∈ B <;> simp [reconstruct,eraseCoefficients,hmb]
  simpa only [Function.id_comp,heq,Function.comp_def,id_eq] using hi.comp measurable_id hm

theorem finite_block_law {I : Type*} [DecidableEq I] (B : Finset I) :
    (coefficientLaw I).map (fun η : I → ℝ => fun m : B => η m.val) =
      Measure.pi (fun _ : B => gaussianReal 0 1) := by
  have hi := (coordinates_independent I).precomp (g := fun m : B => m.val) Subtype.val_injective
  have hm := hi.map_fun_eq_pi_map (fun m => (measurable_pi_apply m.val).aemeasurable)
  simpa only [I4Foundation.coordinate_marginal] using hm

theorem actual_finite_block_law (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (B : Finset (SourceMode d)) :
    (smoothLaw d L).map (fun ω : SmoothSample d L => fun m : B => ω.val m.val) =
      Measure.pi (fun _ : B => gaussianReal 0 1) := by
  change (smoothLaw d L).map (fun ω => (fun η => fun m : B => η m.val)
    (sampleInclusion d L ω)) = _
  rw [observation_map_eq d hL (fun η => fun m : B => η m.val)
    (Measurable.of_eval (fun m => measurable_pi_apply m.val))]
  exact finite_block_law B

/-- The independent tail is the literal erased smooth sample, not only an
ambient coefficient process or a different Gaussian field with matching covariance. -/
theorem actual_finite_block_indep_erased (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (B : Finset (SourceMode d)) :
    IndepFun (fun ω : SmoothSample d L => fun m : B => ω.val m.val)
      (eraseSample d L B) (smoothLaw d L) := by
  have : IsProbabilityMeasure (smoothLaw d L) := smoothLaw_isProbabilityMeasure d hL
  let X : (SourceMode d → ℝ) → B → ℝ := fun η m => η m.val
  let T := eraseCoefficients B
  have hX : Measurable X := Measurable.of_eval (fun m => measurable_pi_apply m.val)
  have hT : Measurable T := eraseCoefficients_measurable B
  have hinc := sampleInclusion_measurable d L
  have hi : IndepFun (X ∘ sampleInclusion d L) (T ∘ sampleInclusion d L) (smoothLaw d L) := by
    apply (indepFun_iff_map_prod_eq_prod_map_map (hX.comp hinc).aemeasurable
      (hT.comp hinc).aemeasurable).mpr
    change (smoothLaw d L).map (fun ω => (X (sampleInclusion d L ω),T (sampleInclusion d L ω))) =
      ((smoothLaw d L).map (fun ω => X (sampleInclusion d L ω))).prod
        ((smoothLaw d L).map (fun ω => T (sampleInclusion d L ω)))
    rw [observation_map_eq d hL _ (hX.prodMk hT),
      observation_map_eq d hL X hX,observation_map_eq d hL T hT]
    exact (finite_block_indep_erased B).map_prod_eq_prod_map_map hX.aemeasurable hT.aemeasurable
  obtain ⟨q,hq,hret⟩ := exists_measurable_sampleProjection d L
  have heq : q ∘ (T ∘ sampleInclusion d L) = eraseSample d L B := by
    funext ω
    change q (sampleInclusion d L (eraseSample d L B ω)) = eraseSample d L B ω
    exact hret _
  have hf := hi.comp measurable_id hq
  rw [heq] at hf
  simpa only [Function.comp_def,id_eq,X,sampleInclusion] using hf

end I4ActualSourceMorse

noncomputable section

open MeasureTheory I4Source I4Smooth I4SmoothCarrier

namespace I4ActualSourceMorse

/-- Replace a finite original Fourier block by literal real coefficients. -/
def replaceCoefficients {I : Type*} [DecidableEq I] (B : Finset I)
    (a : B → ℝ) (η : I → ℝ) : I → ℝ :=
  fun m => if hm : m ∈ B then a ⟨m,hm⟩ else η m

/-- Finite replacement preserves every-order smoothness of the actual carrier. -/
def replaceSample (d : ℕ) (L : ℝ) (B : Finset (SourceMode d))
    (a : B → ℝ) (ω : SmoothSample d L) : SmoothSample d L :=
  ⟨replaceCoefficients B a ω.val,
    (goodSample_finite_change_iff d L ω.val (replaceCoefficients B a ω.val) B
      (fun m hm => by simp only [replaceCoefficients, hm, dite_false])).mp ω.property⟩

theorem replaceSample_measurable (d : ℕ) (L : ℝ) (B : Finset (SourceMode d)) :
    Measurable (fun p : (B → ℝ) × SmoothSample d L =>
      replaceSample d L B p.1 p.2) := by
  apply Measurable.subtype_mk
  apply Measurable.of_eval
  intro m
  by_cases hm : m ∈ B
  · simpa only [replaceSample, replaceCoefficients, hm, dite_true, Function.comp_def] using
      (measurable_pi_apply (⟨m,hm⟩ : B)).comp measurable_fst
  · simpa only [replaceSample, replaceCoefficients, hm, dite_false, Function.comp_def,
      sampleInclusion] using
      (measurable_pi_apply m).comp ((sampleInclusion_measurable d L).comp measurable_snd)

theorem replaceSample_compose (d : ℕ) (L : ℝ) (B : Finset (SourceMode d))
    (a b : B → ℝ) (ω : SmoothSample d L) :
    replaceSample d L B a (replaceSample d L B b ω) = replaceSample d L B a ω := by
  apply Subtype.ext
  funext m
  by_cases hm : m ∈ B <;> simp [replaceSample, replaceCoefficients, hm]

theorem replaceSample_read_self (d : ℕ) (L : ℝ) (B : Finset (SourceMode d))
    (ω : SmoothSample d L) :
    replaceSample d L B (fun m => ω.val m.val) ω = ω := by
  apply Subtype.ext
  funext m
  by_cases hm : m ∈ B <;> simp [replaceSample, replaceCoefficients, hm]

/-- Reconstruct the literal sample from its finite original coordinates and
the carrier obtained by setting that same block to zero. -/
theorem replaceSample_reconstruct (d : ℕ) (L : ℝ) (B : Finset (SourceMode d))
    (ω : SmoothSample d L) :
    replaceSample d L B (fun m => ω.val m.val)
      (replaceSample d L B 0 ω) = ω := by
  rw [replaceSample_compose, replaceSample_read_self]

/-- In particular, a Borel geometric event on the smooth carrier pulls back
to a Borel event on residual sample times finite coefficient block. -/
theorem replaceSample_event_measurable (d : ℕ) (L : ℝ)
    (B : Finset (SourceMode d)) (s : Set (SmoothSample d L)) (hs : MeasurableSet s) :
    MeasurableSet {p : (B → ℝ) × SmoothSample d L |
      replaceSample d L B p.1 p.2 ∈ s} :=
  hs.preimage (replaceSample_measurable d L B)

end I4ActualSourceMorse
namespace I4ActualSourceMorse

theorem eraseSample_eq_replaceSample_zero (d : ℕ) (L : ℝ)
    (B : Finset (SourceMode d)) (ω : SmoothSample d L) :
    eraseSample d L B ω = replaceSample d L B 0 ω := by
  apply Subtype.ext
  funext m
  by_cases hm : m ∈ B <;>
    simp [eraseSample, eraseCoefficients, replaceSample, replaceCoefficients, hm]

theorem replaceSample_read_erased (d : ℕ) (L : ℝ)
    (B : Finset (SourceMode d)) (ω : SmoothSample d L) :
    replaceSample d L B (fun m => ω.val m.val) (eraseSample d L B ω) = ω := by
  rw [eraseSample_eq_replaceSample_zero]
  exact replaceSample_reconstruct d L B ω

/-- The exact residual-first joint law needed for coefficient-section Fubini.
This reuses independence of the actual original block and actual erased
smooth sample, together with their already established marginals. -/
theorem actual_erased_block_joint_map (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (B : Finset (SourceMode d)) :
    (smoothLaw d L).map (fun ω : SmoothSample d L =>
      (eraseSample d L B ω, fun m : B => ω.val m.val)) =
      ((smoothLaw d L).map (eraseSample d L B)).prod
        (Measure.pi fun _ : B => gaussianReal 0 1) := by
  have : IsProbabilityMeasure (smoothLaw d L) := smoothLaw_isProbabilityMeasure d hL
  have hread : Measurable (fun ω : SmoothSample d L => fun m : B => ω.val m.val) :=
    Measurable.of_eval fun m =>
      (measurable_pi_apply m.val).comp measurable_subtype_coe
  have heq := (actual_finite_block_indep_erased d hL B).symm.map_prod_eq_prod_map_map
    (eraseSample_measurable d L B).aemeasurable hread.aemeasurable
  rw [actual_finite_block_law d hL B] at heq
  exact heq

/-- Measurable sectionwise full measure for finite replacement gives full
measure under the unchanged actual smooth source law. No independence of
geometric derivatives or target almost-sure conclusion is assumed. -/
theorem actual_finite_replacement_ae (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (B : Finset (SourceMode d)) (s : Set (SmoothSample d L)) (hs : MeasurableSet s)
    (hsections : ∀ ρ : SmoothSample d L,
      (Measure.pi fun _ : B => gaussianReal 0 1)
        {a | replaceSample d L B a ρ ∉ s} = 0) :
    ∀ᵐ ω ∂smoothLaw d L, ω ∈ s := by
  let bad : Set (SmoothSample d L × (B → ℝ)) :=
    {p | replaceSample d L B p.2 p.1 ∉ s}
  have hbad : MeasurableSet bad :=
    hs.compl.preimage ((replaceSample_measurable d L B).comp measurable_swap)
  have hnull : (((smoothLaw d L).map (eraseSample d L B)).prod
      (Measure.pi fun _ : B => gaussianReal 0 1)) bad = 0 := by
    apply Measure.measure_prod_null_of_ae_null hbad
    exact Filter.Eventually.of_forall hsections
  rw [← actual_erased_block_joint_map d hL B] at hnull
  have hread : Measurable (fun ω : SmoothSample d L => fun m : B => ω.val m.val) :=
    Measurable.of_eval fun m =>
      (measurable_pi_apply m.val).comp measurable_subtype_coe
  rw [Measure.map_apply ((eraseSample_measurable d L B).prodMk hread) hbad] at hnull
  have heq : (fun ω : SmoothSample d L =>
      (eraseSample d L B ω, fun m : B => ω.val m.val)) ⁻¹' bad = sᶜ := by
    ext ω
    simp only [Set.mem_preimage, bad, Set.mem_ofPred_eq, replaceSample_read_erased,
      Set.mem_compl_iff]
  rw [heq] at hnull
  exact (ae_iff.mpr hnull)

end I4ActualSourceMorse

/-! Preserved author-side helper: lean-sard-route/GroupFourCoefficients.lean -/

noncomputable section

set_option autoImplicit false

open I4Foundation I4Source I4SmoothCarrier
open MeasureTheory ProbabilityTheory

namespace I4ActualSourceMorse

def interleavedFour : (Fin 2 ⊕ Fin 2) ≃ Fin 4 where
  toFun := Sum.elim ![0,2] ![1,3]
  invFun := ![Sum.inl 0, Sum.inr 0, Sum.inl 1, Sum.inr 1]
  left_inv := by
    intro j
    cases j with
    | inl i => fin_cases i <;> rfl
    | inr i => fin_cases i <;> rfl
  right_inv := by
    intro i
    fin_cases i <;> rfl

def groupFour (a : Fin 4 → ℝ) : (Fin 2 → ℝ) × (Fin 2 → ℝ) :=
  (![a 0,a 2], ![a 1,a 3])

theorem groupFour_measurable : Measurable groupFour := by
  unfold groupFour
  fun_prop

/-- Interleaving four independent scalar coordinates into their cosine/sine
groups preserves the product measure. This is a reindexing identity for any
sigma-finite common scalar law. -/
theorem groupFour_measurePreserving (ν : Measure ℝ) [SigmaFinite ν] :
    MeasurePreserving groupFour (Measure.pi fun _ : Fin 4 => ν)
      ((Measure.pi fun _ : Fin 2 => ν).prod (Measure.pi fun _ : Fin 2 => ν)) := by
  have hp := measurePreserving_piCongrLeft
    (fun _ : Fin 2 ⊕ Fin 2 => ν) interleavedFour.symm
  have hs := measurePreserving_sumPiEquivProdPi (fun _ : Fin 2 ⊕ Fin 2 => ν)
  have hh := hs.comp hp
  have heq : (MeasurableEquiv.sumPiEquivProdPi (fun _ : Fin 2 ⊕ Fin 2 => ℝ)) ∘
      (MeasurableEquiv.piCongrLeft (fun _ : Fin 2 ⊕ Fin 2 => ℝ) interleavedFour.symm) =
      groupFour := by
    funext a
    apply Prod.ext <;> funext i <;> fin_cases i <;> rfl
  simpa only [heq] using hh

theorem groupFour_gaussian_measurePreserving :
    MeasurePreserving groupFour (Measure.pi fun _ : Fin 4 => gaussianReal 0 1)
      ((Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
        (Measure.pi fun _ : Fin 2 => gaussianReal 0 1)) :=
  groupFour_measurePreserving (gaussianReal 0 1)

/-- Four distinct original source coordinates retain their actual independent
standard Gaussian law on the existing smooth sample carrier. -/
theorem actual_four_coordinate_law (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (m : Fin 4 → SourceMode d) (hm : Function.Injective m) :
    (smoothLaw d L).map (fun ω : SmoothSample d L =>
      fun j => sampleInclusion d L ω (m j)) =
      Measure.pi (fun _ : Fin 4 => gaussianReal 0 1) := by
  rw [finiteCoordinate_map_eq d hL 4 m]
  have hi := (coordinates_independent (SourceMode d)).precomp (g := m) hm
  have hmap := hi.map_fun_eq_pi_map (fun j => (measurable_pi_apply (m j)).aemeasurable)
  simpa only [I4Foundation.coordinate_marginal] using hmap

def actualGroupedFour (d : ℕ) (L : ℝ) (m : Fin 4 → SourceMode d)
    (ω : SmoothSample d L) : (Fin 2 → ℝ) × (Fin 2 → ℝ) :=
  groupFour (fun j => sampleInclusion d L ω (m j))

theorem actualGroupedFour_measurable (d : ℕ) (L : ℝ) (m : Fin 4 → SourceMode d) :
    Measurable (actualGroupedFour d L m) :=
  groupFour_measurable.comp (Measurable.of_eval fun j =>
    (measurable_pi_apply (m j)).comp (sampleInclusion_measurable d L))

/-- The actual four source coordinates in grouped order have exactly the
grouped product Gaussian law used by the trigonometric Morse Sard adapter. -/
theorem actualGroupedFour_map_eq (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (m : Fin 4 → SourceMode d) (hm : Function.Injective m) :
    (smoothLaw d L).map (actualGroupedFour d L m) =
      (Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
        (Measure.pi fun _ : Fin 2 => gaussianReal 0 1) := by
  change (smoothLaw d L).map
    (groupFour ∘ (fun ω : SmoothSample d L => fun j => sampleInclusion d L ω (m j))) = _
  have hcoords : Measurable (fun ω : SmoothSample d L =>
      fun j => sampleInclusion d L ω (m j)) :=
    Measurable.of_eval fun j =>
      (measurable_pi_apply (m j)).comp (sampleInclusion_measurable d L)
  rw [← Measure.map_map groupFour_measurable hcoords,
    actual_four_coordinate_law d hL m hm]
  exact groupFour_gaussian_measurePreserving.map_eq

theorem actualGroupedFour_measurePreserving (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (m : Fin 4 → SourceMode d) (hm : Function.Injective m) :
    MeasurePreserving (actualGroupedFour d L m) (smoothLaw d L)
      ((Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
        (Measure.pi fun _ : Fin 2 => gaussianReal 0 1)) :=
  ⟨actualGroupedFour_measurable d L m, actualGroupedFour_map_eq d hL m hm⟩

end I4ActualSourceMorse

/-! Preserved author-side helper: measurable/ActualMorseEvent.lean -/

open MeasureTheory Set TopologicalSpace

namespace I4ActualSourceMorse

/-- On a compact space, strict positivity of a continuous real function is
equivalent to a uniform reciprocal-natural floor on any dense subset. Empty
compact spaces are included. -/
theorem compact_positive_iff_dense_nat_floor
    {K : Type*} [TopologicalSpace K] [CompactSpace K]
    {D : Set K} (hD : Dense D) {f : K → ℝ} (hf : Continuous f) :
    (∀ x, 0 < f x) ↔
      ∃ n : ℕ, ∀ x ∈ D, 1 / ((n : ℝ) + 1) ≤ f x := by
  constructor
  · intro hpos
    obtain ⟨c, hc, hcf⟩ := isCompact_univ.exists_forall_le' hf.continuousOn
      (fun x _ => hpos x)
    obtain ⟨n, hn⟩ := exists_nat_one_div_lt hc
    exact ⟨n, fun x _ => hn.le.trans (hcf x (mem_univ x))⟩
  · rintro ⟨n, hn⟩ x
    have hx : 1 / ((n : ℝ) + 1) ≤ f x :=
      hD.induction hn (isClosed_le continuous_const hf) x
    exact (one_div_pos.mpr (by positivity)).trans_le hx

/-- Separate measurability in the random variable and continuous spatial
paths suffice for the event of strict positivity everywhere on a compact
separable space to be measurable. No measurable function-space carrier is
required. -/
theorem measurableSet_forall_pos_of_compact
    {Ω K : Type*} [MeasurableSpace Ω] [TopologicalSpace K]
    [CompactSpace K] [SeparableSpace K]
    (H : Ω → K → ℝ) (hcont : ∀ ω, Continuous (H ω))
    (hmeas : ∀ x, Measurable (fun ω => H ω x)) :
    MeasurableSet {ω | ∀ x, 0 < H ω x} := by
  obtain ⟨D, hDc, hDd⟩ := exists_countable_dense K
  have heq : {ω | ∀ x, 0 < H ω x} =
      ⋃ n : ℕ, ⋂ x ∈ D, {ω | 1 / ((n : ℝ) + 1) ≤ H ω x} := by
    ext ω
    simp only [mem_ofPred_eq, mem_iUnion, mem_iInter]
    exact compact_positive_iff_dense_nat_floor hDd (hcont ω)
  rw [heq]
  exact MeasurableSet.iUnion fun n =>
    MeasurableSet.biInter hDc fun x _ => measurableSet_le measurable_const (hmeas x)

/-- The compact-subset version, stated without replacing the spatial ambient
space by the compact subtype in the hypotheses or conclusion. -/
theorem measurableSet_forall_mem_pos_of_isCompact
    {Ω X : Type*} [MeasurableSpace Ω] [TopologicalSpace X]
    {s : Set X} (hs : IsCompact s) [SeparableSpace s]
    (H : Ω → X → ℝ) (hcont : ∀ ω, ContinuousOn (H ω) s)
    (hmeas : ∀ x ∈ s, Measurable (fun ω => H ω x)) :
    MeasurableSet {ω | ∀ x ∈ s, 0 < H ω x} := by
  let : CompactSpace s := isCompact_iff_compactSpace.mp hs
  have hc (ω : Ω) : Continuous (fun x : s => H ω x) :=
    (hcont ω).domRestrict
  convert measurableSet_forall_pos_of_compact
    (fun (ω : Ω) (x : s) => H ω x) hc (fun x => hmeas x x.property) using 1
  ext ω
  simp

end I4ActualSourceMorse

noncomputable section

open I4Foundation I4Source I4SmoothCarrier I4SourceDerivativeGaussian

namespace I4ActualSourceMorse

def morseDirectionX : Fin 2 → ℝ := ![1,0]
def morseDirectionY : Fin 2 → ℝ := ![0,1]

/-- The actual five derivative observations used in the coordinate Morse
discriminant, taken on the unchanged literal smooth source carrier. -/
def sourceMorseDiscriminant (L : ℝ) (ω : SmoothSample 2 L) (x : Fin 2 → ℝ) : ℝ :=
  (iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x ![morseDirectionX]) ^ 2 +
  (iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x ![morseDirectionY]) ^ 2 +
  ((iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![morseDirectionX,morseDirectionX]) *
    (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![morseDirectionY,morseDirectionY]) -
    (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![morseDirectionX,morseDirectionY]) ^ 2) ^ 2

theorem sourceDerivative_eval_measurable (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (x : Fin d → ℝ) (u : Fin k → (Fin d → ℝ)) :
    Measurable (fun ω : SmoothSample d L =>
      iteratedFDeriv ℝ k (smoothSourceField d L ω) x u) := by
  simp_rw [smoothSourceField_derivative_series d hL]
  exact (scalarSeries_measurable _).comp (sampleInclusion_measurable d L)

theorem sourceDerivative_spatial_continuous (d : ℕ) {L : ℝ} (hL : L ≠ 0)
    (k : ℕ) (u : Fin k → (Fin d → ℝ)) (ω : SmoothSample d L) :
    Continuous (fun x => iteratedFDeriv ℝ k (smoothSourceField d L ω) x u) :=
  (continuous_eval_const u).comp
    ((smoothSourceField_contDiff d hL ω k).continuous_iteratedFDeriv le_rfl)

theorem sourceMorseDiscriminant_eval_measurable {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) :
    Measurable (fun ω : SmoothSample 2 L => sourceMorseDiscriminant L ω x) := by
  exact (((sourceDerivative_eval_measurable 2 hL 1 x ![morseDirectionX]).pow_const 2).add
    ((sourceDerivative_eval_measurable 2 hL 1 x ![morseDirectionY]).pow_const 2)).add
    ((((sourceDerivative_eval_measurable 2 hL 2 x ![morseDirectionX,morseDirectionX]).mul
      (sourceDerivative_eval_measurable 2 hL 2 x ![morseDirectionY,morseDirectionY])).sub
      ((sourceDerivative_eval_measurable 2 hL 2 x ![morseDirectionX,morseDirectionY]).pow_const 2)).pow_const 2)

theorem sourceMorseDiscriminant_spatial_continuous {L : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) : Continuous (sourceMorseDiscriminant L ω) := by
  exact (((sourceDerivative_spatial_continuous 2 hL 1 ![morseDirectionX] ω).pow 2).add
    ((sourceDerivative_spatial_continuous 2 hL 1 ![morseDirectionY] ω).pow 2)).add
    ((((sourceDerivative_spatial_continuous 2 hL 2 ![morseDirectionX,morseDirectionX] ω).mul
      (sourceDerivative_spatial_continuous 2 hL 2 ![morseDirectionY,morseDirectionY] ω)).sub
      ((sourceDerivative_spatial_continuous 2 hL 2 ![morseDirectionX,morseDirectionY] ω).pow 2)).pow 2)

def sourceMorseCube (L : ℝ) : Set (Fin 2 → ℝ) :=
  Icc 0 (fun _ => |L|)

theorem sourceMorseCube_isCompact (L : ℝ) : IsCompact (sourceMorseCube L) :=
  isCompact_Icc

/-- The literal compact-cube coordinate Morse event is measurable directly
on SmoothSample; no random smooth-function-space realization is required. -/
theorem sourceMorseCube_event_measurable {L : ℝ} (hL : L ≠ 0) :
    MeasurableSet {ω : SmoothSample 2 L |
      ∀ x ∈ sourceMorseCube L, 0 < sourceMorseDiscriminant L ω x} :=
  measurableSet_forall_mem_pos_of_isCompact (sourceMorseCube_isCompact L)
    (sourceMorseDiscriminant L)
    (fun ω => (sourceMorseDiscriminant_spatial_continuous hL ω).continuousOn)
    (fun x _ => sourceMorseDiscriminant_eval_measurable hL x)

end I4ActualSourceMorse

/-! Preserved author-side helper: lean-sard-route/CoordinateMorse.lean -/

set_option autoImplicit false

noncomputable section

namespace I4ActualSourceMorse

def coordinateGradient (f : (Fin 2 → ℝ) → ℝ) (x : Fin 2 → ℝ) : Fin 2 → ℝ :=
  fun i => fderiv ℝ f x (Pi.single i 1)

theorem coordinateGradient_differentiable (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) : Differentiable ℝ (coordinateGradient f) := by
  apply differentiable_pi.mpr
  intro i
  have hdf : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ f) := hf.fderiv_right (by simp)
  exact (hdf.differentiable (by simp)).clm_apply
    (show Differentiable ℝ (fun _ : Fin 2 → ℝ => (Pi.single i 1 : Fin 2 → ℝ)) from
      differentiable_const _)

theorem coordinateGradient_fderiv_apply (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (x v : Fin 2 → ℝ) (i : Fin 2) :
    (fderiv ℝ (coordinateGradient f) x v) i =
      fderiv ℝ (fderiv ℝ f) x v (Pi.single i 1) := by
  have hdf_smooth : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ f) := hf.fderiv_right (by simp)
  have hdf := hdf_smooth.differentiable (by simp) x
  change ((ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ).comp
    (fderiv ℝ (coordinateGradient f) x)) v = _
  rw [← fderiv_apply (coordinateGradient_differentiable f hf x)]
  change fderiv ℝ (fun y => fderiv ℝ f y (Pi.single i 1)) x v = _
  rw [fderiv_clm_apply hdf
    (differentiableAt_const (Pi.single i 1 : Fin 2 → ℝ))]
  simp

/-- In two dimensions the literal symmetric Hessian discriminant detects
noninjectivity of the derivative of the coordinate gradient. -/
theorem coordinateGradient_singular_of_hessian_discriminant_zero
    (f : (Fin 2 → ℝ) → ℝ) (hf : ContDiff ℝ (⊤ : ℕ∞) f) (x : Fin 2 → ℝ)
    (hdet :
      (iteratedFDeriv ℝ 2 f x ![Pi.single 0 1, Pi.single 0 1]) *
        (iteratedFDeriv ℝ 2 f x ![Pi.single 1 1, Pi.single 1 1]) -
      (iteratedFDeriv ℝ 2 f x ![Pi.single 0 1, Pi.single 1 1]) ^ 2 = 0) :
    ¬ Function.Injective (fderiv ℝ (coordinateGradient f) x) := by
  let e0 : Fin 2 → ℝ := Pi.single 0 1
  let e1 : Fin 2 → ℝ := Pi.single 1 1
  let D := fderiv ℝ (fderiv ℝ f) x
  let a := D e0 e0
  let b := D e0 e1
  let c := D e1 e1
  have hsym : D e1 e0 = b := (hf.contDiffAt.isSymmSndFDerivAt (by simp)) e1 e0
  have hac : a * c - b ^ 2 = 0 := by
    simpa only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
      e0, e1, a, b, c, D] using hdet
  intro hinj
  by_cases ha : a = 0
  · have hb : b = 0 := by
      rw [ha, zero_mul, zero_sub] at hac
      exact sq_eq_zero_iff.mp (neg_eq_zero.mp hac)
    have he : fderiv ℝ (coordinateGradient f) x e0 =
        fderiv ℝ (coordinateGradient f) x 0 := by
      rw [map_zero]
      funext i
      rw [coordinateGradient_fderiv_apply f hf]
      fin_cases i
      · exact ha
      · exact hb
    have hz := congrFun (hinj he) 0
    norm_num [e0] at hz
  · let v : Fin 2 → ℝ := b • e0 - a • e1
    have hv : fderiv ℝ (coordinateGradient f) x v =
        fderiv ℝ (coordinateGradient f) x 0 := by
      rw [map_zero]
      funext i
      rw [coordinateGradient_fderiv_apply f hf]
      change (D v) (Pi.single i 1) = 0
      dsimp [v]
      simp only [map_sub, map_smul, _root_.sub_apply, _root_.smul_apply, smul_eq_mul]
      fin_cases i
      · change b * a - a * (D e1 e0) = 0
        rw [hsym]
        ring
      · change b * b - a * c = 0
        nlinarith [hac]
    have hz := congrFun (hinj hv) 1
    have : a = 0 := by simpa [v, e0, e1] using hz
    exact ha this

end I4ActualSourceMorse

/-! Preserved author-side helper: lean-sard-route/ActualFourModeShift.lean -/

noncomputable section

open I4Source I4Weights I4SourceContact
open Matrix
open scoped BigOperators

namespace I4ActualSourceMorse

def fourFrequency10 : ↥(halfLattice 2) := ⟨![1,0], by
  refine ⟨0, by norm_num, ?_⟩
  intro j hj
  fin_cases j <;> norm_num at hj⟩

def fourFrequency01 : ↥(halfLattice 2) := ⟨![0,1], by
  refine ⟨1, by norm_num, ?_⟩
  intro j hj
  fin_cases j <;> norm_num at *⟩

def fourModeIndex : Fin 4 → Fin 7 := ![1,4,2,6]

def fourMode : Fin 4 → SourceMode 2 := fun j => sourceContactMode (fourModeIndex j)

theorem fourMode_eq : fourMode =
    ![some (fourFrequency10,false), some (fourFrequency10,true),
      some (fourFrequency01,false), some (fourFrequency01,true)] := by
  funext j
  fin_cases j <;> rfl

theorem sourceContactAmplitude_four_pairs (L : ℝ) :
    sourceContactAmplitude L 4 = sourceContactAmplitude L 1 ∧
      sourceContactAmplitude L 6 = sourceContactAmplitude L 2 := by
  constructor <;> rfl

theorem fourModeCoefficient_eq (L : ℝ) (x : Fin 2 → ℝ) :
    (fun j => modeCoefficient 2 L (fourMode j) x) =
      ![sourceContactAmplitude L 1 * Real.cos (sourceC L * x 0),
        sourceContactAmplitude L 1 * Real.sin (sourceC L * x 0),
        sourceContactAmplitude L 2 * Real.cos (sourceC L * x 1),
        sourceContactAmplitude L 2 * Real.sin (sourceC L * x 1)] := by
  rw [fourMode_eq]
  funext j
  fin_cases j <;>
    simp [modeCoefficient, phase, fourFrequency10, fourFrequency01,
      sourceContactAmplitude, sourceModeAmplitude, sourceContactMode,
      Fin.sum_univ_two]
  all_goals left; rfl

theorem coordinate_cos_hasFDerivAt (A c : ℝ) (i : Fin 2) (x : Fin 2 → ℝ) :
    HasFDerivAt (fun y : Fin 2 → ℝ => A * Real.cos (c * y i))
      ((-A * c * Real.sin (c * x i)) •
        (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ)) x := by
  convert (((hasFDerivAt_apply i x).const_mul c).cos.const_mul A) using 1
  ext y
  simp
  ring

theorem coordinate_sin_hasFDerivAt (A c : ℝ) (i : Fin 2) (x : Fin 2 → ℝ) :
    HasFDerivAt (fun y : Fin 2 → ℝ => A * Real.sin (c * y i))
      ((A * c * Real.cos (c * x i)) •
        (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ)) x := by
  convert (((hasFDerivAt_apply i x).const_mul c).sin.const_mul A) using 1
  ext y
  simp
  ring

def fourGradientMatrix (L : ℝ) (x : Fin 2 → ℝ) : Matrix (Fin 2) (Fin 4) ℝ :=
  ![![-sourceContactAmplitude L 1 * sourceC L * Real.sin (sourceC L * x 0),
      sourceContactAmplitude L 1 * sourceC L * Real.cos (sourceC L * x 0),0,0],
    ![0,0,-sourceContactAmplitude L 2 * sourceC L * Real.sin (sourceC L * x 1),
      sourceContactAmplitude L 2 * sourceC L * Real.cos (sourceC L * x 1)]]

theorem fourMode_hasFDerivAt (L : ℝ) (x : Fin 2 → ℝ) (j : Fin 4) :
    HasFDerivAt (modeCoefficient 2 L (fourMode j))
      (∑ i : Fin 2, fourGradientMatrix L x i j •
        (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ)) x := by
  have hf (j : Fin 4) : modeCoefficient 2 L (fourMode j) =
      (fun x =>
        ![sourceContactAmplitude L 1 * Real.cos (sourceC L * x 0),
          sourceContactAmplitude L 1 * Real.sin (sourceC L * x 0),
          sourceContactAmplitude L 2 * Real.cos (sourceC L * x 1),
          sourceContactAmplitude L 2 * Real.sin (sourceC L * x 1)] j) := by
    funext x
    exact congrFun (fourModeCoefficient_eq L x) j
  rw [hf j]
  fin_cases j
  · simpa [fourGradientMatrix, Fin.sum_univ_two] using
      coordinate_cos_hasFDerivAt (sourceContactAmplitude L 1) (sourceC L) 0 x
  · simpa [fourGradientMatrix, Fin.sum_univ_two] using
      coordinate_sin_hasFDerivAt (sourceContactAmplitude L 1) (sourceC L) 0 x
  · simpa [fourGradientMatrix, Fin.sum_univ_two] using
      coordinate_cos_hasFDerivAt (sourceContactAmplitude L 2) (sourceC L) 1 x
  · simpa [fourGradientMatrix, Fin.sum_univ_two] using
      coordinate_sin_hasFDerivAt (sourceContactAmplitude L 2) (sourceC L) 1 x

def fourGradientRightInverse (L : ℝ) (x : Fin 2 → ℝ) (v : Fin 2 → ℝ) : Fin 4 → ℝ :=
  ![-Real.sin (sourceC L * x 0) * v 0 / (sourceContactAmplitude L 1 * sourceC L),
    Real.cos (sourceC L * x 0) * v 0 / (sourceContactAmplitude L 1 * sourceC L),
    -Real.sin (sourceC L * x 1) * v 1 / (sourceContactAmplitude L 2 * sourceC L),
    Real.cos (sourceC L * x 1) * v 1 / (sourceContactAmplitude L 2 * sourceC L)]

theorem fourGradient_rightInverse {L : ℝ} (hL : L ≠ 0)
    (x v : Fin 2 → ℝ) :
    fourGradientMatrix L x *ᵥ fourGradientRightInverse L x v = v := by
  have hc : sourceC L ≠ 0 := div_ne_zero
    (mul_ne_zero (by norm_num) (ne_of_gt Real.pi_pos)) hL
  have hAx : sourceContactAmplitude L 1 ≠ 0 := (sourceContactAmplitude_pos hL 1).ne'
  have hAy : sourceContactAmplitude L 2 ≠ 0 := (sourceContactAmplitude_pos hL 2).ne'
  funext i
  fin_cases i <;>
    simp [Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
      fourGradientMatrix, fourGradientRightInverse]
  · field_simp
    linear_combination v 0 * (Real.sin_sq_add_cos_sq (sourceC L * x 0))
  · field_simp
    linear_combination v 1 * (Real.sin_sq_add_cos_sq (sourceC L * x 1))

theorem fourGradient_surjective {L : ℝ} (hL : L ≠ 0) (x : Fin 2 → ℝ) :
    Function.Surjective (fun a : Fin 4 → ℝ => fourGradientMatrix L x *ᵥ a) := by
  intro v
  exact ⟨fourGradientRightInverse L x v, fourGradient_rightInverse hL x v⟩

theorem fourMode_fderiv (L : ℝ) (x : Fin 2 → ℝ) (j : Fin 4) (i : Fin 2) :
    fderiv ℝ (modeCoefficient 2 L (fourMode j)) x (Pi.single i 1) =
      fourGradientMatrix L x i j := by
  rw [(fourMode_hasFDerivAt L x j).fderiv]
  fin_cases i <;> simp [Fin.sum_univ_two]

def fourModePerturbation (L : ℝ) (a : Fin 4 → ℝ) (x : Fin 2 → ℝ) : ℝ :=
  ∑ j, a j * modeCoefficient 2 L (fourMode j) x

theorem fourModePerturbation_hasFDerivAt (L : ℝ) (a : Fin 4 → ℝ) (x : Fin 2 → ℝ) :
    HasFDerivAt (fourModePerturbation L a)
      (∑ j : Fin 4, a j • ∑ i : Fin 2, fourGradientMatrix L x i j •
        (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ)) x := by
  exact HasFDerivAt.fun_sum fun j _ => (fourMode_hasFDerivAt L x j).const_mul (a j)

theorem fourModePerturbation_gradient (L : ℝ) (a : Fin 4 → ℝ) (x : Fin 2 → ℝ) :
    (fun i => fderiv ℝ (fourModePerturbation L a) x (Pi.single i 1)) =
      fourGradientMatrix L x *ᵥ a := by
  rw [(fourModePerturbation_hasFDerivAt L a x).fderiv]
  funext i
  fin_cases i <;>
    simp [Fin.sum_univ_two, Matrix.mulVec, dotProduct, mul_comm]

theorem fourModePerturbation_gradient_surjective {L : ℝ} (hL : L ≠ 0)
    (x : Fin 2 → ℝ) :
    Function.Surjective (fun a : Fin 4 → ℝ =>
      fun i => fderiv ℝ (fourModePerturbation L a) x (Pi.single i 1)) := by
  intro v
  refine ⟨fourGradientRightInverse L x v, ?_⟩
  exact (fourModePerturbation_gradient L (fourGradientRightInverse L x v) x).trans
    (fourGradient_rightInverse hL x v)

end I4ActualSourceMorse


namespace I4ActualSourceMorse

open I4Foundation I4Smooth I4SmoothCarrier I4SourceDerivativeGaussian I4SourceSmoothConditional

theorem fourMode_injective : Function.Injective fourMode := by
  intro i j hij
  fin_cases i <;> fin_cases j <;>
    simp_all [fourMode_eq, fourFrequency10, fourFrequency01]
  all_goals have h := congrFun (congrArg Subtype.val hij) 0; norm_num at h

def fourModeSet : Finset (SourceMode 2) := Finset.univ.image fourMode

def fourCoefficientLift (a : Fin 4 → ℝ) (m : SourceMode 2) : ℝ :=
  ∑ j : Fin 4, if m = fourMode j then a j else 0

def fourAddSample (L : ℝ) (a : Fin 4 → ℝ) (ω : SmoothSample 2 L) : SmoothSample 2 L :=
  ⟨fun m => ω.val m + fourCoefficientLift a m,
    (goodSample_finite_change_iff 2 L ω.val _ fourModeSet (by
      intro m hm
      have hne : ∀ j, m ≠ fourMode j := by
        intro j h
        apply hm
        exact Finset.mem_image.mpr ⟨j, Finset.mem_univ j, h.symm⟩
      simp [fourCoefficientLift, hne])).mp ω.property⟩

theorem fourAddSample_measurable (L : ℝ) :
    Measurable (fun p : (Fin 4 → ℝ) × SmoothSample 2 L => fourAddSample L p.1 p.2) := by
  apply Measurable.subtype_mk
  apply Measurable.of_eval
  intro m
  change Measurable (fun p : (Fin 4 → ℝ) × SmoothSample 2 L =>
    p.2.val m + ∑ j : Fin 4, if m = fourMode j then p.1 j else 0)
  apply Measurable.add
  · exact (measurable_pi_apply m).comp ((sampleInclusion_measurable 2 L).comp measurable_snd)
  · exact Finset.measurable_sum _ (fun j _ => by
      by_cases h : m = fourMode j
      · simpa only [h, ite_true, Function.comp_def] using
          (measurable_pi_apply j).comp measurable_fst
      · simpa only [h, ite_false] using
          (measurable_const : Measurable (fun _ : (Fin 4 → ℝ) × SmoothSample 2 L => (0 : ℝ))))

theorem actual_derivative_fourAdd {L : ℝ} (hL : L ≠ 0)
    (a : Fin 4 → ℝ) (ω : SmoothSample 2 L) (k : ℕ) (x : Fin 2 → ℝ)
    (u : Fin k → (Fin 2 → ℝ)) :
    iteratedFDeriv ℝ k (smoothSourceField 2 L (fourAddSample L a ω)) x u =
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u +
        ∑ j : Fin 4, derivativeCoefficient 2 L k x u (fourMode j) * a j := by
  classical
  let δ : Fin 4 → SourceMode 2 → ℝ := fun j m => if m = fourMode j then 1 else 0
  have hδ : ∀ j, Summable (δ j) := by
    intro j
    apply summable_of_ne_finset_zero (s := {fourMode j})
    intro m hm
    simp only [Finset.mem_singleton] at hm
    simp [δ, hm]
  have hs := scalarSeries_add_finiteShift
    (derivativeCoefficient 2 L k x u) δ ω.val a
    (derivativeCoefficient_summable 2 hL k x u) hδ
    (derivativeCoefficient_weighted_summable hL ω k x u)
  rw [smoothSourceField_derivative_series 2 hL (fourAddSample L a ω),
    smoothSourceField_derivative_series 2 hL ω]
  change scalarSeries _ (fun m => ω.val m + fourCoefficientLift a m) =
    scalarSeries _ ω.val + _
  convert hs using 1
  · congr 1
    funext m
    congr 1
    apply Finset.sum_congr rfl
    intro j hj
    by_cases h : m = fourMode j <;> simp [δ, h]
  · congr 1
    apply Finset.sum_congr rfl
    intro j hj
    congr 1
    simp [δ, mul_ite]

theorem actual_coordinateGradient_fourAdd {L : ℝ} (hL : L ≠ 0)
    (a : Fin 4 → ℝ) (ω : SmoothSample 2 L) (x : Fin 2 → ℝ) :
    (fun i : Fin 2 => fderiv ℝ (smoothSourceField 2 L (fourAddSample L a ω)) x
      (Pi.single i 1)) =
    (fun i : Fin 2 => fderiv ℝ (smoothSourceField 2 L ω) x (Pi.single i 1)) +
      fourGradientMatrix L x *ᵥ a := by
  funext i
  have hs := actual_derivative_fourAdd hL a ω 1 x ![Pi.single i 1]
  simpa only [iteratedFDeriv_one_apply, Matrix.cons_val_zero, derivativeCoefficient,
    fourMode_fderiv, Pi.add_apply, Matrix.mulVec, dotProduct, mul_comm] using hs

end I4ActualSourceMorse


namespace I4ActualSourceMorse

/-- The four-mode range is identified with the four original scalar coordinates. -/
def fourModeEquiv : Fin 4 ≃ fourModeSet :=
  Equiv.ofBijective (fun j => ⟨fourMode j, Finset.mem_image.mpr ⟨j, Finset.mem_univ j, rfl⟩⟩)
    ⟨fun i j h => fourMode_injective (congrArg Subtype.val h), by
      rintro ⟨m, hm⟩
      obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hm
      exact ⟨j, rfl⟩⟩

def fourReindex (a : fourModeSet → ℝ) : Fin 4 → ℝ := fun j => a (fourModeEquiv j)

theorem fourReindex_measurePreserving :
    MeasurePreserving fourReindex (Measure.pi fun _ : fourModeSet => gaussianReal 0 1)
      (Measure.pi fun _ : Fin 4 => gaussianReal 0 1) := by
  convert measurePreserving_piCongrLeft
    (fun _ : Fin 4 => gaussianReal 0 1) fourModeEquiv.symm using 1
  funext a j
  simpa only [fourReindex, Equiv.symm_apply_apply] using
    (MeasurableEquiv.piCongrLeft_apply_apply (β := fun _ : Fin 4 => ℝ)
      fourModeEquiv.symm a (fourModeEquiv j)).symm

theorem fourCoefficientLift_at (a : Fin 4 → ℝ) (j : Fin 4) :
    fourCoefficientLift a (fourMode j) = a j := by
  simp [fourCoefficientLift, fourMode_injective.eq_iff]

theorem replaceSample_fourModeSet (L : ℝ) (a : fourModeSet → ℝ)
    (ρ : SmoothSample 2 L) :
    replaceSample 2 L fourModeSet a ρ =
      fourAddSample L (fourReindex a) (eraseSample 2 L fourModeSet ρ) := by
  apply Subtype.ext
  funext m
  by_cases hm : m ∈ fourModeSet
  · obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hm
    simp [replaceSample, replaceCoefficients, fourAddSample, eraseSample,
      eraseCoefficients, fourCoefficientLift_at, fourReindex, fourModeEquiv,
      fourModeSet]
    rfl
  · have hne : ∀ j, m ≠ fourMode j := by
      intro j hj
      exact hm (Finset.mem_image.mpr ⟨j, Finset.mem_univ j, hj.symm⟩)
    simp [replaceSample, replaceCoefficients, fourAddSample, eraseSample,
      eraseCoefficients, fourCoefficientLift, hm, hne]

def sourceMorseAmplitude (L : ℝ) : Fin 2 → ℝ :=
  ![sourceContactAmplitude L 1, sourceContactAmplitude L 2]

theorem sourceMorseAmplitude_ne_zero {L : ℝ} (hL : L ≠ 0) :
    ∀ i, sourceMorseAmplitude L i ≠ 0 := by
  intro i
  fin_cases i
  · exact (sourceContactAmplitude_pos hL 1).ne'
  · exact (sourceContactAmplitude_pos hL 2).ne'

theorem sourceC_ne_zero {L : ℝ} (hL : L ≠ 0) : sourceC L ≠ 0 :=
  div_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt Real.pi_pos)) hL

/-- Literal coordinate gradient of replacement of the four original modes.
The residual is the entire erased smooth sample, rather than a finite jet. -/
theorem actual_coordinateGradient_replace {L : ℝ} (hL : L ≠ 0)
    (a : fourModeSet → ℝ) (ρ : SmoothSample 2 L) (x : Fin 2 → ℝ) :
    coordinateGradient (smoothSourceField 2 L (replaceSample 2 L fourModeSet a ρ)) x =
      twoChannelGradientFamily
        (coordinateGradient (smoothSourceField 2 L (eraseSample 2 L fourModeSet ρ)))
        (cosineGradientChannel (sourceMorseAmplitude L) (sourceC L))
        (sineGradientChannel (sourceMorseAmplitude L) (sourceC L)) x
        (groupFour (fourReindex a)) := by
  rw [replaceSample_fourModeSet]
  change (fun i => fderiv ℝ _ x (Pi.single i 1)) = _
  rw [actual_coordinateGradient_fourAdd hL]
  funext i
  fin_cases i <;>
    simp [twoChannelGradientFamily, coordinateGradient, fourGradientMatrix,
      Matrix.mulVec, dotProduct, Fin.sum_univ_succ, cosineGradientChannel,
      sineGradientChannel, sourceMorseAmplitude, groupFour] <;> ring

theorem morseDirectionX_eq : morseDirectionX = Pi.single 0 1 := by
  ext i
  fin_cases i <;> simp [morseDirectionX]

theorem morseDirectionY_eq : morseDirectionY = Pi.single 1 1 := by
  ext i
  fin_cases i <;> simp [morseDirectionY]

/-- The actual nonpositive five-observation discriminant supplies both the
critical equation and singular derivative used by the incidence theorem. -/
theorem sourceMorseDiscriminant_nonpos {L : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (x : Fin 2 → ℝ)
    (h : sourceMorseDiscriminant L ω x ≤ 0) :
    coordinateGradient (smoothSourceField 2 L ω) x = 0 ∧
      ¬ Function.Injective (fderiv ℝ
        (coordinateGradient (smoothSourceField 2 L ω)) x) := by
  let p := iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x ![morseDirectionX]
  let q := iteratedFDeriv ℝ 1 (smoothSourceField 2 L ω) x ![morseDirectionY]
  let d :=
    (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![morseDirectionX,morseDirectionX]) *
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![morseDirectionY,morseDirectionY]) -
    (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) x ![morseDirectionX,morseDirectionY]) ^ 2
  change p ^ 2 + q ^ 2 + d ^ 2 ≤ 0 at h
  have hp : p = 0 := by nlinarith [sq_nonneg q, sq_nonneg d]
  have hq : q = 0 := by nlinarith [sq_nonneg p, sq_nonneg d]
  have hd : d = 0 := by nlinarith [sq_nonneg p, sq_nonneg q]
  constructor
  · funext i
    fin_cases i
    · have hp' : fderiv ℝ (smoothSourceField 2 L ω) x morseDirectionX = 0 := by
        simpa only [p, iteratedFDeriv_one_apply, Matrix.cons_val_zero] using hp
      change fderiv ℝ (smoothSourceField 2 L ω) x _ = 0
      calc
        _ = fderiv ℝ (smoothSourceField 2 L ω) x morseDirectionX := by
          congr 1
          ext j
          fin_cases j <;> simp [Pi.single, morseDirectionX]
        _ = 0 := hp'
    · have hq' : fderiv ℝ (smoothSourceField 2 L ω) x morseDirectionY = 0 := by
        simpa only [q, iteratedFDeriv_one_apply, Matrix.cons_val_zero] using hq
      change fderiv ℝ (smoothSourceField 2 L ω) x _ = 0
      calc
        _ = fderiv ℝ (smoothSourceField 2 L ω) x morseDirectionY := by
          congr 1
          ext j
          fin_cases j <;> simp [Pi.single, morseDirectionY]
        _ = 0 := hq'
  · apply coordinateGradient_singular_of_hessian_discriminant_zero
      (smoothSourceField 2 L ω) (smoothSourceField_smooth 2 hL ω) x
    simpa only [d, morseDirectionX_eq, morseDirectionY_eq] using hd

/-- Every residual sample has Gaussian-null bad sections for the literal
replacement family, by the proved four-channel incidence Sard theorem. -/
theorem actual_four_replacement_bad_null {L : ℝ} (hL : L ≠ 0)
    (ρ : SmoothSample 2 L) (K : Set (Fin 2 → ℝ)) :
    (Measure.pi fun _ : fourModeSet => gaussianReal 0 1)
      {a | ¬ ∀ x ∈ K, 0 < sourceMorseDiscriminant L
        (replaceSample 2 L fourModeSet a ρ) x} = 0 := by
  let g := coordinateGradient (smoothSourceField 2 L (eraseSample 2 L fourModeSet ρ))
  let D := trigonometricDegenerateCriticalParameters g (sourceMorseAmplitude L) (sourceC L)
  have hD : ((Measure.pi fun _ : Fin 2 => gaussianReal 0 1).prod
      (Measure.pi fun _ : Fin 2 => gaussianReal 0 1)) D = 0 :=
    trigonometricDegenerateCriticalParameters_gaussian_null g
      (sourceMorseAmplitude L) (sourceC L)
      (coordinateGradient_differentiable _ (smoothSourceField_smooth 2 hL _))
      (sourceMorseAmplitude_ne_zero hL) (sourceC_ne_zero hL)
  have hmp := groupFour_gaussian_measurePreserving.comp fourReindex_measurePreserving
  have hpre : (Measure.pi fun _ : fourModeSet => gaussianReal 0 1)
      ((groupFour ∘ fourReindex) ⁻¹' D) = 0 := by
    apply Measure.preimage_null_of_map_null hmp.measurable.aemeasurable
    rw [hmp.map_eq]
    exact hD
  apply measure_mono_null _ hpre
  intro a ha
  push Not at ha
  obtain ⟨x, _, hx⟩ := ha
  obtain ⟨hcrit, hsing⟩ := sourceMorseDiscriminant_nonpos hL _ x hx
  have heq : coordinateGradient (smoothSourceField 2 L
      (replaceSample 2 L fourModeSet a ρ)) =
      (fun y => twoChannelGradientFamily g
        (cosineGradientChannel (sourceMorseAmplitude L) (sourceC L))
        (sineGradientChannel (sourceMorseAmplitude L) (sourceC L)) y
        (groupFour (fourReindex a))) := by
    funext y
    exact actual_coordinateGradient_replace hL a ρ y
  change groupFour (fourReindex a) ∈ D
  refine ⟨x, ?_, ?_⟩
  · exact (congrFun heq x).symm.trans hcrit
  · simpa only [heq] using hsing

/-- The unchanged actual smooth source is Morse on its fundamental cube.
The sole premise is the nonzero signed side length. -/
theorem smoothLaw_ae_sourceMorseCube {L : ℝ} (hL : L ≠ 0) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ x ∈ sourceMorseCube L,
      0 < sourceMorseDiscriminant L ω x := by
  exact actual_finite_replacement_ae 2 hL fourModeSet
    {ω | ∀ x ∈ sourceMorseCube L, 0 < sourceMorseDiscriminant L ω x}
    (sourceMorseCube_event_measurable hL)
    (fun ρ => actual_four_replacement_bad_null hL ρ (sourceMorseCube L))

end I4ActualSourceMorse

namespace I4ActualSourceMorse

/-- The same source argument applies on every specified compact subset of the
real cover; compactness is used only to make the event measurable. -/
theorem smoothLaw_ae_sourceMorseCompact {L : ℝ} (hL : L ≠ 0)
    (K : Set (Fin 2 → ℝ)) (hK : IsCompact K) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ x ∈ K, 0 < sourceMorseDiscriminant L ω x := by
  exact actual_finite_replacement_ae 2 hL fourModeSet
    {ω | ∀ x ∈ K, 0 < sourceMorseDiscriminant L ω x}
    (measurableSet_forall_mem_pos_of_isCompact hK (sourceMorseDiscriminant L)
      (fun ω => (sourceMorseDiscriminant_spatial_continuous hL ω).continuousOn)
      (fun x _ => sourceMorseDiscriminant_eval_measurable hL x))
    (fun ρ => actual_four_replacement_bad_null hL ρ K)

/-- Countable compact exhaustion gives the actual source Morse statement
simultaneously at every point of the real cover. -/
theorem smoothLaw_ae_sourceMorse {L : ℝ} (hL : L ≠ 0) :
    ∀ᵐ ω ∂smoothLaw 2 L, ∀ x, 0 < sourceMorseDiscriminant L ω x := by
  have hballs (n : ℕ) : ∀ᵐ ω ∂smoothLaw 2 L,
      ∀ x ∈ Metric.closedBall (0 : Fin 2 → ℝ) (n : ℝ),
        0 < sourceMorseDiscriminant L ω x :=
    smoothLaw_ae_sourceMorseCompact hL _ (isCompact_closedBall _ _)
  filter_upwards [ae_all_iff.mpr hballs] with ω hω
  intro x
  obtain ⟨n, hn⟩ := exists_nat_gt ‖x‖
  exact hω n x (by simpa only [Metric.mem_closedBall, dist_zero_right] using hn.le)

/-- The coordinate-gradient determinant is exactly the literal symmetric
Hessian determinant, without a norm or quotient coordinate change. -/
theorem coordinateGradient_det_eq (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (x : Fin 2 → ℝ) :
    (fderiv ℝ (coordinateGradient f) x).det =
      (iteratedFDeriv ℝ 2 f x ![Pi.single 0 1, Pi.single 0 1]) *
        (iteratedFDeriv ℝ 2 f x ![Pi.single 1 1, Pi.single 1 1]) -
      (iteratedFDeriv ℝ 2 f x ![Pi.single 0 1, Pi.single 1 1]) ^ 2 := by
  change LinearMap.det (fderiv ℝ (coordinateGradient f) x).toLinearMap = _
  rw [← LinearMap.det_toMatrix', Matrix.det_fin_two]
  simp only [LinearMap.toMatrix'_apply, ContinuousLinearMap.coe_coe,
    coordinateGradient_fderiv_apply f hf, iteratedFDeriv_two_apply,
    Matrix.cons_val_zero, Matrix.cons_val_one]
  rw [(hf.contDiffAt.isSymmSndFDerivAt (by simp)) (Pi.single 1 1) (Pi.single 0 1)]
  ring

theorem sourceMorseDiscriminant_eq (L : ℝ) (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (x : Fin 2 → ℝ) :
    sourceMorseDiscriminant L ω x =
      (coordinateGradient (smoothSourceField 2 L ω) x 0) ^ 2 +
      (coordinateGradient (smoothSourceField 2 L ω) x 1) ^ 2 +
      (fderiv ℝ (coordinateGradient (smoothSourceField 2 L ω)) x).det ^ 2 := by
  rw [coordinateGradient_det_eq _ (smoothSourceField_smooth 2 hL ω)]
  simp only [sourceMorseDiscriminant, morseDirectionX_eq, morseDirectionY_eq,
    iteratedFDeriv_one_apply, Matrix.cons_val_zero, coordinateGradient]

end I4ActualSourceMorse

namespace I4ActualSourceMorse

theorem coordinateGradient_contDiff (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) : ContDiff ℝ (⊤ : ℕ∞) (coordinateGradient f) := by
  apply contDiff_pi.mpr
  intro i
  exact (hf.fderiv_right (by simp)).clm_apply contDiff_const

/-- Positivity at a critical point forces the actual derivative of its
coordinate gradient to be injective. -/
theorem sourceMorse_regular {L : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (x : Fin 2 → ℝ)
    (hpos : 0 < sourceMorseDiscriminant L ω x)
    (hcrit : coordinateGradient (smoothSourceField 2 L ω) x = 0) :
    Function.Injective (fderiv ℝ (coordinateGradient (smoothSourceField 2 L ω)) x) := by
  rw [sourceMorseDiscriminant_eq L hL, hcrit] at hpos
  have hdet : (fderiv ℝ (coordinateGradient (smoothSourceField 2 L ω)) x).det ≠ 0 := by
    intro hz
    simp [hz] at hpos
  apply LinearMap.ker_eq_bot.mp
  by_contra hker
  exact hdet (LinearMap.det_eq_zero_iff_ker_ne_bot.mpr hker)

/-- The existing smooth inverse-function theorem isolates any zero with
injective derivative in this finite-dimensional coordinate space. -/
theorem regular_zero_isolated (g : (Fin 2 → ℝ) → (Fin 2 → ℝ))
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (x : Fin 2 → ℝ) (hx : g x = 0)
    (hreg : Function.Injective (fderiv ℝ g x)) :
    ∃ U : Set (Fin 2 → ℝ), IsOpen U ∧ x ∈ U ∧ ∀ y ∈ U, g y = 0 → y = x := by
  let D := fderiv ℝ g x
  let e : (Fin 2 → ℝ) ≃L[ℝ] (Fin 2 → ℝ) :=
    (LinearEquiv.ofInjectiveEndo D.toLinearMap hreg).toContinuousLinearEquiv
  have he : (e : (Fin 2 → ℝ) →L[ℝ] (Fin 2 → ℝ)) = D := by
    ext v i
    rfl
  have hd : HasFDerivAt g (e : (Fin 2 → ℝ) →L[ℝ] (Fin 2 → ℝ)) x := by
    rw [he]
    exact (hg.differentiable (by simp) x).hasFDerivAt
  let p := hg.contDiffAt.toOpenPartialHomeomorph g hd (by simp)
  have hxp : x ∈ p.source :=
    hg.contDiffAt.mem_toOpenPartialHomeomorph_source hd (by simp)
  refine ⟨p.source, p.open_source, hxp, ?_⟩
  intro y hy hzero
  apply p.injOn hy hxp
  change g y = g x
  exact hzero.trans hx.symm

/-- Closed regular zeros in a compact set form a finite set. This uses the
proved inverse-function and compact-discrete theorems, with no finiteness premise. -/
theorem finite_regular_zeros_on_compact (g : (Fin 2 → ℝ) → (Fin 2 → ℝ))
    (hg : ContDiff ℝ (⊤ : ℕ∞) g) (K : Set (Fin 2 → ℝ)) (hK : IsCompact K)
    (hreg : ∀ x ∈ K, g x = 0 → Function.Injective (fderiv ℝ g x)) :
    {x | x ∈ K ∧ g x = 0}.Finite := by
  have hc : IsCompact {x | x ∈ K ∧ g x = 0} :=
    hK.inter_right (isClosed_eq hg.continuous continuous_const)
  apply hc.finite
  rw [isDiscrete_iff_forall_mem_exists_isOpen]
  rintro x ⟨hxK, hx⟩
  obtain ⟨U, hU, hxU, hiso⟩ := regular_zero_isolated g hg x hx (hreg x hxK hx)
  refine ⟨U, hU, ?_⟩
  ext y
  constructor
  · rintro ⟨hyU, _, hyzero⟩
    exact Set.mem_singleton_iff.mpr (hiso y hyU hyzero)
  · intro hy
    have hyx := Set.mem_singleton_iff.mp hy
    subst y
    exact ⟨hxU, hxK, hx⟩

/-- The actual critical points in the fundamental cube are almost surely
finite, derived from the source Morse theorem and compactness/IFT. -/
theorem smoothLaw_ae_finite_sourceCriticalCube {L : ℝ} (hL : L ≠ 0) :
    ∀ᵐ ω ∂smoothLaw 2 L,
      {x | x ∈ sourceMorseCube L ∧
        coordinateGradient (smoothSourceField 2 L ω) x = 0}.Finite := by
  filter_upwards [smoothLaw_ae_sourceMorseCube hL] with ω hω
  exact finite_regular_zeros_on_compact _
    (coordinateGradient_contDiff _ (smoothSourceField_smooth 2 hL ω)) _
    (sourceMorseCube_isCompact L) (fun x hx hcrit => sourceMorse_regular hL ω x (hω x hx) hcrit)

end I4ActualSourceMorse
