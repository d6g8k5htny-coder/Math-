import MorseFiniteCritical
import Mathlib.Analysis.Calculus.ImplicitContDiff

/-!
# The actual negative partial-gradient ridge

C299 constructs a local ridge from literal smoothness, criticality and a
negative definite restriction of the literal Hessian. The parameter is ambient
`E d`; it may subsequently be restricted to the supplied positive complement.
No complement is assumed orthogonal. No ridge, inverse certificate, Morse chart,
closed-superlevel local path connectivity or finite event list is an input.

The construction follows the reviewed direct-ridge paper published at
Math-#487, issuecomment-6292079965. This module covers only its partial-gradient
implicit-function step and differentiated equation. Reduced positivity,
uniform signs, fiber concavity, tubes, paths, the quotient and full LPC remain
separate obligations.
-/

noncomputable section

open Set Topology
open UniversalLaw.Spec.Lifetime TorusMorseFinite

namespace TorusCriticalRidge

variable {d : ℕ}

/-- Restrict an ambient continuous covector to the literal subspace. -/
def restrictCovector (V : Submodule ℝ (E d)) :
    (E d →L[ℝ] ℝ) →L[ℝ] (V →L[ℝ] ℝ) where
  toFun ℓ := ℓ.comp V.subtypeL
  map_add' ℓ₁ ℓ₂ := by
    ext z
    rfl
  map_smul' c ℓ := by
    ext z
    rfl
  cont := (continuous_id : Continuous (fun ℓ : E d →L[ℝ] ℝ => ℓ)).clm_comp_const
    V.subtypeL

/-- Addition of an ambient parameter and a vector in the negative subspace. -/
def ridgeAddition (V : Submodule ℝ (E d)) :
    (E d × V) →L[ℝ] E d :=
  ContinuousLinearMap.fst ℝ (E d) V +
    V.subtypeL.comp (ContinuousLinearMap.snd ℝ (E d) V)

/-- The covector-valued partial gradient, with a fixed base point. -/
def negativePartialGradient (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d)) (q : E d × V) : V →L[ℝ] ℝ :=
  restrictCovector V (fderiv ℝ f (p + ridgeAddition V q))

/-- The actual Hessian restricted to both negative-subspace arguments. -/
def negativeHessianBlock (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d)) : V →L[ℝ] (V →L[ℝ] ℝ) :=
  (restrictCovector V).comp
    ((fderiv ℝ (fderiv ℝ f) p).comp V.subtypeL)

theorem negativeHessianBlock_apply (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d)) (v z : V) :
    negativeHessianBlock f p V v z = hessian d f p v z := by
  rw [literal_hessian_eq_fderiv]
  rfl

/-- Negative definiteness supplies the exact continuous inverse required by IFT.
This includes the zero subspace, without a unit-sphere argument. -/
theorem negativeHessianBlock_isInvertible (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d))
    (hneg : ∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0) :
    (negativeHessianBlock f p V).IsInvertible := by
  let C := negativeHessianBlock f p V
  have hz : ∀ v : V, C v = 0 → v = 0 := by
    intro v hv
    by_contra hne
    have hvne : (v : E d) ≠ 0 := by
      intro h
      apply hne
      exact Subtype.ext h
    have hn := hneg v v.property hvne
    have he : hessian d f p v v = 0 := by
      have h := congrArg (fun k : V →L[ℝ] ℝ => k v) hv
      simpa only [C, negativeHessianBlock_apply, zero_apply] using h
    linarith
  have hC : Function.Injective C := by
    intro u v huv
    apply sub_eq_zero.mp
    apply hz
    simp [map_sub, huv]
  let J : V ≃L[ℝ] (V →L[ℝ] ℝ) :=
    (InnerProductSpace.toDual ℝ V).toContinuousLinearEquiv
  let A : V →L[ℝ] V := J.symm.toContinuousLinearMap.comp C
  have hA : Function.Injective A := J.symm.injective.comp hC
  let eA : V ≃L[ℝ] V :=
    (LinearEquiv.ofInjectiveEndo A.toLinearMap hA).toContinuousLinearEquiv
  refine ⟨eA.trans J, ?_⟩
  apply ContinuousLinearMap.ext
  intro v
  change J (J.symm (C v)) = C v
  exact J.apply_symm_apply (C v)

theorem negativePartialGradient_contDiff (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d)) (hsmooth : IsSmooth d f) :
    ContDiff ℝ 2 (negativePartialGradient f p V) := by
  have hD : ContDiff ℝ 2 (fderiv ℝ f) :=
    (contDiff_succ_iff_fderiv.mp (hsmooth 3)).2.2
  change ContDiff ℝ 2 (fun q : E d × V =>
    (fderiv ℝ f (p + ridgeAddition V q)).comp V.subtypeL)
  exact (hD.comp (contDiff_const.add (ridgeAddition V).contDiff)).clm_comp
    contDiff_const

theorem negativePartialGradient_hasFDerivAt (f : E d → ℝ) (p : E d)
    (V : Submodule ℝ (E d)) (hsmooth : IsSmooth d f) :
    HasFDerivAt (negativePartialGradient f p V)
      ((restrictCovector V).comp
        ((fderiv ℝ (fderiv ℝ f) p).comp (ridgeAddition V)))
      (0 : E d × V) := by
  have hD : ContDiff ℝ 1 (fderiv ℝ f) :=
    (contDiff_succ_iff_fderiv.mp (hsmooth 2)).2.2
  have hDp := (hD.differentiable (by norm_num) p).hasFDerivAt
  have hadd : HasFDerivAt (fun q : E d × V => p + ridgeAddition V q)
      (ridgeAddition V) 0 := by
    simpa using ((ridgeAddition V).hasFDerivAt.const_add p)
  have hDp' : HasFDerivAt (fderiv ℝ f) (fderiv ℝ (fderiv ℝ f) p)
      (p + ridgeAddition V (0 : E d × V)) := by
    simpa only [map_zero, add_zero] using hDp
  have hcomp := hDp'.comp (0 : E d × V) hadd
  change HasFDerivAt (fun q : E d × V =>
    (fderiv ℝ f (p + ridgeAddition V q)).comp V.subtypeL) _ _
  convert hcomp.clm_comp (hasFDerivAt_const V.subtypeL (0 : E d × V)) using 1
  ext q z
  simp [restrictCovector]

/-- One actual ridge and all four conclusions for the same chosen function.
The equation is in the actual ambient function and actual subspace. -/
theorem exists_negative_partial_gradient_ridge
    (f : E d → ℝ) (p : E d) (V : Submodule ℝ (E d))
    (hsmooth : IsSmooth d f) (hcritical : IsCriticalPoint d f p)
    (hneg : ∀ v ∈ V, v ≠ 0 → hessian d f p v v < 0) :
    ∃ r : E d → V,
      r 0 = 0 ∧
      ContDiffAt ℝ 2 r 0 ∧
      (∀ᶠ w in 𝓝 (0 : E d), ∀ z : V,
        fderiv ℝ f (p + w + (r w : E d)) z = 0) ∧
      (∀ (w : E d) (z : V),
        hessian d f p (w + (fderiv ℝ r 0 w : E d)) z = 0) := by
  let G := negativePartialGradient f p V
  let D := (restrictCovector V).comp
    ((fderiv ℝ (fderiv ℝ f) p).comp (ridgeAddition V))
  have hG : ContDiffAt ℝ 2 G (0 : E d × V) :=
    (negativePartialGradient_contDiff f p V hsmooth).contDiffAt
  have hDG : HasFDerivAt G D (0 : E d × V) :=
    negativePartialGradient_hasFDerivAt f p V hsmooth
  have hblock : fderiv ℝ G (0 : E d × V) ∘L
      ContinuousLinearMap.inr ℝ (E d) V = negativeHessianBlock f p V := by
    rw [hDG.fderiv]
    ext v z
    simp [D, negativeHessianBlock, ridgeAddition, restrictCovector]
  have hinv : (fderiv ℝ G (0 : E d × V) ∘L
      ContinuousLinearMap.inr ℝ (E d) V).IsInvertible := by
    rw [hblock]
    exact negativeHessianBlock_isInvertible f p V hneg
  let r : E d → V := hG.implicitFunction (by norm_num) hinv
  have hr0 : r 0 = 0 := hG.implicitFunction_apply_self (by norm_num) hinv
  have hrC : ContDiffAt ℝ 2 r 0 :=
    hG.contDiffAt_implicitFunction (by norm_num) hinv
  have hG0 : G (0 : E d × V) = 0 := by
    ext z
    simp [G, negativePartialGradient, ridgeAddition, restrictCovector,
      show fderiv ℝ f p = 0 from hcritical]
  have heq : (fun w => G (w, r w)) =ᶠ[𝓝 (0 : E d)]
      (fun _ => (0 : V →L[ℝ] ℝ)) := by
    simpa [r, hG0] using hG.eventually_apply_implicitFunction (by norm_num) hinv
  refine ⟨r, hr0, hrC, ?_, ?_⟩
  · filter_upwards [heq] with w hw
    intro z
    have hz := congrArg (fun k : V →L[ℝ] ℝ => k z) hw
    simpa [G, negativePartialGradient, ridgeAddition, restrictCovector, add_assoc] using hz
  · have hdr : HasFDerivAt r (fderiv ℝ r 0) 0 :=
      (hrC.differentiableAt (by norm_num)).hasFDerivAt
    have hgraph : HasFDerivAt (fun w : E d => (w, r w))
        ((ContinuousLinearMap.id ℝ (E d)).prod (fderiv ℝ r 0)) 0 :=
      (hasFDerivAt_id (0 : E d)).prodMk hdr
    have hzero : HasFDerivAt (fun w : E d => G (w, r w))
        (0 : E d →L[ℝ] (V →L[ℝ] ℝ)) 0 :=
      (hasFDerivAt_const (0 : V →L[ℝ] ℝ) (0 : E d)).congr_of_eventuallyEq heq
    have hchain : HasFDerivAt (fun w : E d => G (w, r w))
        (D.comp ((ContinuousLinearMap.id ℝ (E d)).prod (fderiv ℝ r 0))) 0 := by
      have hd : HasFDerivAt G D ((0 : E d), r 0) := by
        simpa only [hr0] using hDG
      exact hd.comp 0 hgraph
    have hid := hchain.unique hzero
    intro w z
    have h := congrArg (fun C : E d →L[ℝ] (V →L[ℝ] ℝ) => C w z) hid
    simpa [D, restrictCovector, ridgeAddition, literal_hessian_eq_fderiv] using h

end TorusCriticalRidge
