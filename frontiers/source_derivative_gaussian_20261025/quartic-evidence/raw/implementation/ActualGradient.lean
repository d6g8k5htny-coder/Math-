import SourcePinPreservingQuartic
import Mathlib.Analysis.Calculus.Gradient.Basic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourceConditionalMajorant
open I4SourcePinCurvatureBounds I4SourcePinPreservingQuartic
open Matrix WithLp InnerProductSpace
open scoped BigOperators
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

def sourceScaledPotential (L r : ℝ) (ω : SmoothSample 2 L) (p : SourcePlane) : ℝ :=
  smoothSourceField 2 L ω (r • ofLp p)/r^3

theorem sourceScaledPotential_hasGradientAt {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (p : SourcePlane) :
    HasGradientAt (sourceScaledPotential L r ω) (sourceScaledGradient L r ω p) p := by
  let f := smoothSourceField 2 L ω
  have hf : Differentiable ℝ f := (smoothSourceField_smooth 2 hL ω).differentiable (by simp)
  have hc : HasFDerivAt (fun z : SourcePlane => r • ofLp z) (r • euclideanToPi) p :=
    (r • euclideanToPi).hasFDerivAt
  have h := ((hf (r • ofLp p)).hasFDerivAt.comp p hc).const_mul ((r^3)⁻¹)
  have hm : toDual ℝ SourcePlane (sourceScaledGradient L r ω p) =
      (r^3)⁻¹ • ((fderiv ℝ f (r • ofLp p)).comp (r • euclideanToPi)) := by
    ext v
    change inner ℝ (sourceScaledGradient L r ω p) v =
      (r^3)⁻¹ * fderiv ℝ f (r • ofLp p) (r • ofLp v)
    rw [map_smul,coordinate_decomposition (ofLp v),map_add,map_smul,map_smul]
    simp [sourceScaledGradient,sourceScaledGradientRaw,PiLp.inner_apply,Fin.sum_univ_two,
      coordinateDirection_zero,coordinateDirection_one,directionX,directionY,
      smul_eq_mul,f]
    field_simp [hr]
  apply hasGradientAt_iff_hasFDerivAt.mpr
  change HasFDerivAt (fun z : SourcePlane => f (r • ofLp z)/r^3)
    (toDual ℝ SourcePlane (sourceScaledGradient L r ω p)) p
  rw [hm]
  simpa only [div_eq_mul_inv,mul_comm,Function.comp_def,f] using h

theorem sourceScaledGradient_eq_gradient {L : ℝ} (hL : L ≠ 0) (r : ℝ) (hr : r ≠ 0)
    (ω : SmoothSample 2 L) (p : SourcePlane) :
    sourceScaledGradient L r ω p = gradient (sourceScaledPotential L r ω) p :=
  (sourceScaledPotential_hasGradientAt hL r hr ω p).gradient.symm

theorem sourceScaledGradient_smooth {L : ℝ} (hL : L ≠ 0) (r : ℝ) (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (sourceScaledGradient L r ω) := by
  let f := smoothSourceField 2 L ω
  have hf := smoothSourceField_smooth 2 hL ω
  have hg : ContDiff ℝ (⊤ : ℕ∞) (gradientPi f) := by
    apply contDiff_pi.mpr
    intro i
    exact derivativeComponent_smooth f hf (coordinateDirection i)
  have he : ContDiff ℝ (⊤ : ℕ∞) (gradientEuclidean f) :=
    piToEuclidean.contDiff.comp (hg.comp euclideanToPi.contDiff)
  rw [sourceScaledGradient_eq]
  exact (he.comp (r • ContinuousLinearMap.id ℝ SourcePlane).contDiff).const_smul _

theorem pinPreservingQuartic_pins (r q : ℝ) (U : Fin 8 → ℝ) :
    pinPreservingQuartic r q U ![-1/2,0] = 0 ∧
    pinPreservingQuartic r q U ![1/2,0] = 0 := by
  constructor <;> ext i <;> fin_cases i <;> norm_num [pinPreservingQuartic]

theorem sourceScaledGradient_pins (L r : ℝ) (ω : SmoothSample 2 L)
    (hp : sourcePhysicalPins L r ω) :
    sourceScaledGradient L r ω (toLp 2 ![-1/2,0]) = 0 ∧
    sourceScaledGradient L r ω (toLp 2 ![1/2,0]) = 0 := by
  have hM : r • (![-1/2,0] : Fin 2 → ℝ) = endpointM r := by
    ext i; fin_cases i <;> simp [endpointM]; ring
  have hS : r • (![1/2,0] : Fin 2 → ℝ) = endpointS r := by
    ext i; fin_cases i <;> simp [endpointS]; ring
  constructor
  · ext i
    fin_cases i
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![-1/2,0]) directionX/r^2=0
      rw [hM]
      exact div_eq_zero_iff.mpr (Or.inl hp.1)
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![-1/2,0]) directionY/r^2=0
      rw [hM]
      exact div_eq_zero_iff.mpr (Or.inl hp.2.2.1)
  · ext i
    fin_cases i
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![1/2,0]) directionX/r^2=0
      rw [hS]
      exact div_eq_zero_iff.mpr (Or.inl hp.2.1)
    · change fderiv ℝ (smoothSourceField 2 L ω) (r • ![1/2,0]) directionY/r^2=0
      rw [hS]
      exact div_eq_zero_iff.mpr (Or.inl hp.2.2.2.1)

end I4SourcePinPreservingQuartic
