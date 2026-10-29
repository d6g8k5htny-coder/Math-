import SourceActualMorseLocalModel
import SourceActualFoldTorus
import SourceFiniteTrig
import SourceSmoothConditionalKernel
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Topology.Instances.AddCircle.Defs
import Mathlib.Topology.OpenPartialHomeomorph.Constructions
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Positivity
import Lean.Elab.Tactic.Omega
import Mathlib.Tactic.GCongr

noncomputable section
open Set Filter
open I4SmoothCarrier I4LifetimeField
open UniversalLaw.Spec.Lifetime
open scoped Topology BigOperators Matrix
set_option autoImplicit false
namespace I4SourceActualTorusSuperlevelLocalBasis

private def coverProjection (L : ℝ) (X : UniversalLaw.Spec.Lifetime.E 2) :
    I4Torus.SourceTorus 2 L :=
  I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)


/-
Stage61 Helper A: complete original private regular-boundary adapter.
Frozen lexical input: CONTEXT.ORIGINAL.md (shared context amendment002).
TEXT ONLY. No Lean/probe/build/kernel/control/hash/object execution by helper.
-/

private theorem regular_finTwo_functional
    (d : (Fin 2 → ℝ) →L[ℝ] ℝ) (v : Fin 2 → ℝ) :
    d v = d ![1, 0] * v 0 + d ![0, 1] * v 1 := by
  have hv : v = v 0 • ![(1 : ℝ), 0] + v 1 • ![(0 : ℝ), 1] := by
    ext i
    fin_cases i <;> simp
  calc
    d v = d (v 0 • ![(1 : ℝ), 0] + v 1 • ![(0 : ℝ), 1]) := congrArg d hv
    _ = d ![1, 0] * v 0 + d ![0, 1] * v 1 := by
      simp only [map_add, map_smul, smul_eq_mul]
      ring

private def regular_firstRowEquiv
    (d : (Fin 2 → ℝ) →L[ℝ] ℝ) (ha : d ![1, 0] ≠ 0) :
    (Fin 2 → ℝ) ≃L[ℝ] (Fin 2 → ℝ) :=
  ({ toFun := fun v => ![d v, v 1]
     invFun := fun w => ![(w 0 - d ![0, 1] * w 1) / d ![1, 0], w 1]
     left_inv := by
       intro v
       ext i
       fin_cases i
       · change (d v - d ![0, 1] * v 1) / d ![1, 0] = v 0
         rw [regular_finTwo_functional d v]
         field_simp [ha]; ring
       · rfl
     right_inv := by
       intro w
       ext i
       fin_cases i
       · change d ![(w 0 - d ![0, 1] * w 1) / d ![1, 0], w 1] = w 0
         rw [regular_finTwo_functional d]
         simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
         field_simp [ha]; ring
       · rfl
     map_add' := by
       intro u v
       ext i
       fin_cases i <;> simp
     map_smul' := by
       intro a v
       ext i
       fin_cases i <;> simp
   } : (Fin 2 → ℝ) ≃ₗ[ℝ] (Fin 2 → ℝ)).toContinuousLinearEquiv

private def regular_secondRowEquiv
    (d : (Fin 2 → ℝ) →L[ℝ] ℝ) (hb : d ![0, 1] ≠ 0) :
    (Fin 2 → ℝ) ≃L[ℝ] (Fin 2 → ℝ) :=
  ({ toFun := fun v => ![d v, v 0]
     invFun := fun w => ![w 1, (w 0 - d ![1, 0] * w 1) / d ![0, 1]]
     left_inv := by
       intro v
       ext i
       fin_cases i
       · rfl
       · change (d v - d ![1, 0] * v 0) / d ![0, 1] = v 1
         rw [regular_finTwo_functional d v]
         field_simp [hb]; ring
     right_inv := by
       intro w
       ext i
       fin_cases i
       · change d ![w 1, (w 0 - d ![1, 0] * w 1) / d ![0, 1]] = w 0
         rw [regular_finTwo_functional d]
         simp only [Matrix.cons_val_zero, Matrix.cons_val_one]
         field_simp [hb]; ring
       · rfl
     map_add' := by
       intro u v
       ext i
       fin_cases i <;> simp
     map_smul' := by
       intro a v
       ext i
       fin_cases i <;> simp
   } : (Fin 2 → ℝ) ≃ₗ[ℝ] (Fin 2 → ℝ)).toContinuousLinearEquiv

private theorem regular_choose_rowEquiv
    (d : (Fin 2 → ℝ) →L[ℝ] ℝ) (hd : d ≠ 0) :
    ∃ (k : Fin 2) (A : (Fin 2 → ℝ) ≃L[ℝ] (Fin 2 → ℝ)),
      ∀ v, A v = ![d v, v k] := by
  by_cases ha : d ![1, 0] = 0
  · have hb : d ![0, 1] ≠ 0 := by
      intro hb
      apply hd
      apply ContinuousLinearMap.ext
      intro v
      change d v = 0
      rw [regular_finTwo_functional d v, ha, hb]
      ring
    exact ⟨0, regular_secondRowEquiv d hb, fun _ => rfl⟩
  · exact ⟨1, regular_firstRowEquiv d ha, fun _ => rfl⟩

private theorem regularCoverLevelBasis {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2)
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U) (hX : X ∈ U)
    (hreg : fderiv ℝ (actualField 2 L omega) X ≠ 0) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ X ∈ W ∧ W ⊆ U ∧
      IsPathConnected (W ∩ {Y | actualField 2 L omega X ≤ actualField 2 L omega Y}) := by
  let c := coordinates 2
  let g := actualField 2 L omega
  let ell : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ := fderiv ℝ g X
  let d : (Fin 2 → ℝ) →L[ℝ] ℝ := ell.comp c.symm.toContinuousLinearMap
  have hd : d ≠ 0 := by
    intro hz
    apply hreg
    apply ContinuousLinearMap.ext
    intro Y
    have h := congrArg (fun q : (Fin 2 → ℝ) →L[ℝ] ℝ => q (c Y)) hz
    change ell (c.symm (c Y)) = 0 at h
    change ell Y = 0
    simpa only [ContinuousLinearEquiv.symm_apply_apply] using h
  obtain ⟨k, A, hA⟩ := regular_choose_rowEquiv d hd
  let B : UniversalLaw.Spec.Lifetime.E 2 ≃L[ℝ] (Fin 2 → ℝ) := c.trans A
  let p : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
    (ContinuousLinearMap.proj k).comp c.toContinuousLinearMap
  let f : UniversalLaw.Spec.Lifetime.E 2 → (Fin 2 → ℝ) :=
    fun Y => ![g Y - g X, c Y k - c X k]
  have hg : ContDiff ℝ 1 g := actualField_smooth 2 hL omega 1
  have hf : ContDiff ℝ 1 f := by
    apply contDiff_pi.2
    intro i
    fin_cases i
    · change ContDiff ℝ 1 (fun Y => g Y - g X)
      exact hg.sub contDiff_const
    · change ContDiff ℝ 1 (fun Y => p Y - c X k)
      exact p.contDiff.sub contDiff_const
  have hB0 : (ContinuousLinearMap.proj (0 : Fin 2)).comp
      B.toContinuousLinearMap = ell := by
    apply ContinuousLinearMap.ext
    intro Y
    change A (c Y) 0 = ell Y
    rw [hA]
    change ell (c.symm (c Y)) = ell Y
    simp only [ContinuousLinearEquiv.symm_apply_apply]
  have hB1 : (ContinuousLinearMap.proj (1 : Fin 2)).comp
      B.toContinuousLinearMap = p := by
    apply ContinuousLinearMap.ext
    intro Y
    change A (c Y) 1 = p Y
    rw [hA]
    rfl
  have hfderiv : HasFDerivAt f B.toContinuousLinearMap X := by
    apply hasFDerivAt_pi'.2
    intro i
    fin_cases i
    · change HasFDerivAt (fun Y => g Y - g X)
        ((ContinuousLinearMap.proj (0 : Fin 2)).comp B.toContinuousLinearMap) X
      rw [hB0]
      exact (hg.differentiable (by norm_num)).differentiableAt.hasFDerivAt.sub_const (g X)
    · change HasFDerivAt (fun Y => p Y - c X k)
        ((ContinuousLinearMap.proj (1 : Fin 2)).comp B.toContinuousLinearMap) X
      rw [hB1]
      exact p.hasFDerivAt.sub_const (c X k)
  let phi : OpenPartialHomeomorph (UniversalLaw.Spec.Lifetime.E 2) (Fin 2 → ℝ) :=
    hf.contDiffAt.toOpenPartialHomeomorph f hfderiv (by norm_num)
  have hXs : X ∈ phi.source :=
    hf.contDiffAt.mem_toOpenPartialHomeomorph_source hfderiv (by norm_num)
  have hphiX : phi X = 0 := by
    change f X = 0
    ext i
    fin_cases i <;> simp [f]
  have hzeroTarget : (0 : Fin 2 → ℝ) ∈ phi.target := by
    rw [← hphiX]
    exact phi.mapsTo hXs
  have hInvZero : phi.symm 0 = X := by
    rw [← hphiX]
    exact phi.left_inv hXs
  let Q : Set (Fin 2 → ℝ) := phi.target ∩ phi.symm ⁻¹' U
  have hQ : IsOpen Q := phi.isOpen_inter_preimage_symm hU
  have hzeroQ : (0 : Fin 2 → ℝ) ∈ Q := by
    refine ⟨hzeroTarget, ?_⟩
    change phi.symm 0 ∈ U
    rw [hInvZero]
    exact hX
  obtain ⟨epsilon, hepsilon, hball⟩ := Metric.isOpen_iff.1 hQ 0 hzeroQ
  have hballTarget : Metric.ball (0 : Fin 2 → ℝ) epsilon ⊆ phi.target :=
    fun v hv => (hball hv).1
  let W : Set (UniversalLaw.Spec.Lifetime.E 2) :=
    phi.symm '' Metric.ball (0 : Fin 2 → ℝ) epsilon
  have hW : IsOpen W :=
    phi.isOpen_image_symm_of_subset_target Metric.isOpen_ball hballTarget
  have hXW : X ∈ W := by
    refine ⟨0, ?_, hInvZero⟩
    simpa only [Metric.mem_ball, dist_self] using hepsilon
  have hWU : W ⊆ U := by
    rintro Y ⟨v, hv, rfl⟩
    exact (hball hv).2
  have hheight (v : Fin 2 → ℝ) (hv : v ∈ Metric.ball 0 epsilon) :
      g (phi.symm v) - g X = v 0 := by
    have h := congrFun (phi.right_inv (hballTarget hv)) (0 : Fin 2)
    change (f (phi.symm v)) 0 = v 0 at h
    simpa only [f, Matrix.cons_val_zero] using h
  have htrace : W ∩ {Y | g X ≤ g Y} =
      phi.symm '' (Metric.ball (0 : Fin 2 → ℝ) epsilon ∩ {v | 0 ≤ v 0}) := by
    ext Y
    constructor
    · rintro ⟨⟨v, hv, rfl⟩, hlev⟩
      refine ⟨v, ⟨hv, ?_⟩, rfl⟩
      have hh := hheight v hv
      change g X ≤ g (phi.symm v) at hlev
      change 0 ≤ v 0
      linarith
    · rintro ⟨v, ⟨hv, hlev⟩, rfl⟩
      refine ⟨⟨v, hv, rfl⟩, ?_⟩
      have hh := hheight v hv
      change 0 ≤ v 0 at hlev
      change g X ≤ g (phi.symm v)
      linarith
  have hhalf : Convex ℝ {v : Fin 2 → ℝ | 0 ≤ v 0} := by
    intro u hu v hv a b ha hb _hab
    change 0 ≤ a * u 0 + b * v 0
    exact add_nonneg (mul_nonneg ha hu) (mul_nonneg hb hv)
  have hpc : IsPathConnected
      (Metric.ball (0 : Fin 2 → ℝ) epsilon ∩ {v | 0 ≤ v 0}) := by
    apply ((convex_ball (0 : Fin 2 → ℝ) epsilon).inter hhalf).isPathConnected
    refine ⟨0, ?_, ?_⟩
    · simpa only [Metric.mem_ball, dist_self] using hepsilon
    · simp
  refine ⟨W, hW, hXW, hWU, ?_⟩
  change IsPathConnected (W ∩ {Y | g X ≤ g Y})
  rw [htrace]
  exact hpc.image' (phi.symm.continuousOn.mono fun v hv => hballTarget hv.1)

/-- Strict membership leaves an ambient ball inside the closed superlevel. -/
private theorem interiorCoverBasis {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) (X : UniversalLaw.Spec.Lifetime.E 2)
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U) (hX : X ∈ U)
    (ha : a < actualField 2 L omega X) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ X ∈ W ∧ W ⊆ U ∧
      IsPathConnected (W ∩ {Y | a ≤ actualField 2 L omega Y}) := by
  have hg : Continuous (actualField 2 L omega) :=
    (actualField_smooth 2 hL omega 1).continuous
  have hopen : IsOpen (U ∩ {Y | a < actualField 2 L omega Y}) :=
    hU.inter (hg.isOpen_preimage _ isOpen_Ioi)
  obtain ⟨epsilon, hepsilon, hball⟩ := Metric.isOpen_iff.mp hopen X ⟨hX, ha⟩
  refine ⟨Metric.ball X epsilon, Metric.isOpen_ball, Metric.mem_ball_self hepsilon,
    fun Y hY => (hball hY).1, ?_⟩
  have heq : Metric.ball X epsilon ∩ {Y | a ≤ actualField 2 L omega Y} =
      Metric.ball X epsilon := by
    apply inter_eq_left.mpr
    intro Y hY
    exact (hball hY).2.le
  rw [heq]
  exact (convex_ball X epsilon).isPathConnected ⟨X, Metric.mem_ball_self hepsilon⟩

/-- Consume only the qualified public critical-neighborhood consequence of60. -/
private theorem criticalCoverLevelBasis {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (X : UniversalLaw.Spec.Lifetime.E 2) (j : ℕ)
    (hc : IsCriticalPoint 2 (actualField 2 L omega) X)
    (hi : HessianHasInertia 2 (actualField 2 L omega) X j)
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U) (hX : X ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ X ∈ W ∧ W ⊆ U ∧
      IsPathConnected (W ∩ {Y | actualField 2 L omega X ≤ actualField 2 L omega Y}) := by
  obtain ⟨_hj, phi, _hsource, _hzero, _htarget, _hphi, _hinv, _hquad, hneighborhood⟩ :=
    I4SourceActualMorseLocalModel.actualSource_c1_quadratic_localModel hL omega X j hc hi
  obtain ⟨W, hW, hXW, hWU, hpc⟩ := hneighborhood U hU hX
  exact ⟨W, hW, hXW, fun Y hY => (hWU hY).1, hpc⟩

/-- Exact quotient trace transport needs openness and continuity, not injectivity. -/
private theorem projectCoverTrace {L : ℝ} (hL : 0 < L)
    (omega : SmoothSample 2 L) (a : ℝ) (W : Set (UniversalLaw.Spec.Lifetime.E 2))
    (hW : IsOpen W) (hpc : IsPathConnected (W ∩ {Y | a ≤ actualField 2 L omega Y})) :
    IsOpen (coverProjection L '' W) ∧
      ((coverProjection L '' W) ∩
        {z | a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z} =
        coverProjection L '' (W ∩ {Y | a ≤ actualField 2 L omega Y})) ∧
      IsPathConnected ((coverProjection L '' W) ∩
        {z | a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z}) := by
  have hcont : Continuous (coverProjection L) :=
    (SourceActualFoldTorus.torusProjection2L_continuous L).comp (coordinates 2).continuous
  have hopen : IsOpenMap (coverProjection L) :=
    (SourceActualFoldTorus.torusProjection2L_open L).comp (coordinates 2).isOpenMap
  have hpull (X : UniversalLaw.Spec.Lifetime.E 2) :
      SourceActualFoldTorus.actualTorusField hL.ne' omega (coverProjection L X) =
        actualField 2 L omega X :=
    SourceActualFoldTorus.actualTorusField_pullback hL.ne' omega (coordinates 2 X)
  have heq : (coverProjection L '' W) ∩
      {z | a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z} =
      coverProjection L '' (W ∩ {Y | a ≤ actualField 2 L omega Y}) := by
    ext z
    constructor
    · rintro ⟨⟨X, hX, rfl⟩, ha⟩
      refine ⟨X, ⟨hX, ?_⟩, rfl⟩
      simpa only [mem_setOf_eq, hpull] using ha
    · rintro ⟨X, ⟨hX, ha⟩, rfl⟩
      refine ⟨⟨X, hX, rfl⟩, ?_⟩
      simpa only [mem_setOf_eq, hpull] using ha
  exact ⟨hopen W hW, heq, heq.symm ▸ hpc.image hcont⟩

/- Complete PRIVATE production fixture section61B. Insert once after the
frozen adapters, inside I4SourceActualTorusSuperlevelLocalBasis. -/

private def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1,Pi.single (0:Fin 2) 1,0⟩,⟨2,Pi.single (1:Fin 2) 1,0⟩]

private def fixtureSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)

private def fixturePoint (x y : ℝ) : UniversalLaw.Spec.Lifetime.E 2 :=
  (coordinates 2).symm ![x,y]

private theorem fixture_coordinateField (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 fixtureSample x = Real.cos (Real.pi*x 0)+2*Real.cos (Real.pi*x 1) := by
  classical
  have hs : HasSum (fun m => I4Source.modeCoefficient 2 2 m x *
      I4SourceFiniteTrig.toSource 2 fixturePolynomial m)
      (I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x)
        (I4SourceFiniteTrig.toSource 2 fixturePolynomial)) := by
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    simp only [Finsupp.notMem_support_iff.mp hm,mul_zero]
  have he : smoothSourceField 2 2 fixtureSample x =
      I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x)
        (I4SourceFiniteTrig.toSource 2 fixturePolynomial) := by
    simpa [fixtureSample,smoothSourceField,I4Source.sourceField,I4Foundation.scalarSeries,
      sampleInclusion,I4SourceFinitePinKernel.finiteShiftSample_val,
      I4SourceSmoothConditional.zeroSample] using hs.tsum_eq
  rw [he,I4SourceFiniteTrig.toSource_eval (by norm_num : (2:ℝ) ≠ 0)]
  simp [fixturePolynomial,I4SourceFiniteTrig.eval,I4SourceFiniteTrig.termEval,
    I4Source.phase,I4Weights.sourceC,Fin.sum_univ_two]

private theorem fixture_actualField (X : UniversalLaw.Spec.Lifetime.E 2) :
    actualField 2 2 fixtureSample X = Real.cos (Real.pi*X 0)+2*Real.cos (Real.pi*X 1) := by
  exact fixture_coordinateField (coordinates 2 X)

private def fixtureCoord (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ).comp (coordinates 2).toContinuousLinearMap

private def fixtureDerivative (X : UniversalLaw.Spec.Lifetime.E 2) :
    UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (-Real.pi*Real.sin (Real.pi*X 0)) • fixtureCoord 0 +
    (-2*Real.pi*Real.sin (Real.pi*X 1)) • fixtureCoord 1

private theorem fixture_hasFDerivAt (X : UniversalLaw.Spec.Lifetime.E 2) :
    HasFDerivAt (actualField 2 2 fixtureSample) (fixtureDerivative X) X := by
  have hx : HasFDerivAt (fun Y : UniversalLaw.Spec.Lifetime.E 2 => Real.pi*Y 0)
      (Real.pi • fixtureCoord 0) X := (fixtureCoord 0).hasFDerivAt.const_mul Real.pi
  have hy : HasFDerivAt (fun Y : UniversalLaw.Spec.Lifetime.E 2 => Real.pi*Y 1)
      (Real.pi • fixtureCoord 1) X := (fixtureCoord 1).hasFDerivAt.const_mul Real.pi
  have hh := hx.cos.add (hy.cos.const_mul 2)
  have he : actualField 2 2 fixtureSample = fun Y : UniversalLaw.Spec.Lifetime.E 2 =>
      Real.cos (Real.pi*Y 0)+2*Real.cos (Real.pi*Y 1) := funext fixture_actualField
  rw [he]
  convert hh using 1 <;> ext v <;> simp [fixtureDerivative,fixtureCoord] <;> ring

private theorem fixture_hessian (X u v : UniversalLaw.Spec.Lifetime.E 2) :
    hessian 2 (actualField 2 2 fixtureSample) X u v =
      -Real.pi^2*Real.cos (Real.pi*X 0)*u 0*v 0-
        2*Real.pi^2*Real.cos (Real.pi*X 1)*u 1*v 1 := by
  rw [hessian,iteratedFDeriv_two_apply]
  have he : fderiv ℝ (actualField 2 2 fixtureSample) = fixtureDerivative :=
    funext fun Y => (fixture_hasFDerivAt Y).fderiv
  rw [he]
  have hx : HasFDerivAt (fun Y : UniversalLaw.Spec.Lifetime.E 2 => Real.pi*Y 0)
      (Real.pi • fixtureCoord 0) X := (fixtureCoord 0).hasFDerivAt.const_mul Real.pi
  have hy : HasFDerivAt (fun Y : UniversalLaw.Spec.Lifetime.E 2 => Real.pi*Y 1)
      (Real.pi • fixtureCoord 1) X := (fixtureCoord 1).hasFDerivAt.const_mul Real.pi
  have hd := ((hx.sin.const_mul (-Real.pi)).smul_const (fixtureCoord 0)).add
    ((hy.sin.const_mul (-2*Real.pi)).smul_const (fixtureCoord 1))
  rw [show fderiv ℝ fixtureDerivative X = _ from hd.fderiv]
  simp [fixtureCoord] <;> ring

private def fixtureCriticalPoint : Fin 4 → UniversalLaw.Spec.Lifetime.E 2 :=
  ![fixturePoint 0 0,fixturePoint 1 0,fixturePoint 0 1,fixturePoint 1 1]

private theorem fixture_critical (i : Fin 4) :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixtureCriticalPoint i) := by
  rw [IsCriticalPoint,(fixture_hasFDerivAt _).fderiv]
  fin_cases i <;> simp [fixtureCriticalPoint,fixturePoint,fixtureDerivative,fixtureCoord]

private theorem fixture_heights (i : Fin 4) :
    actualField 2 2 fixtureSample (fixtureCriticalPoint i) = (![3,1,-1,-3] : Fin 4 → ℝ) i := by
  rw [fixture_actualField]
  fin_cases i <;> norm_num [fixtureCriticalPoint,fixturePoint]

private theorem fixture_axis_ne (i : Fin 2) : fixturePoint (if i=0 then 1 else 0)
    (if i=1 then 1 else 0) ≠ 0 := by
  intro h
  have he := congrArg (fun X => coordinates 2 X i) h
  fin_cases i <;> norm_num [fixturePoint] at he

private theorem fixture_saddleMinus_inertia :
    HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 := by
  let n := fixturePoint 1 0
  let p := fixturePoint 0 1
  have hn : n ≠ 0 := by simpa [n] using fixture_axis_ne 0
  have hp : p ≠ 0 := by simpa [p] using fixture_axis_ne 1
  have hdN := finrank_span_singleton hn
  have hdP := finrank_span_singleton hp
  have hd : Disjoint (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    rw [Submodule.disjoint_def]
    intro v hv hw
    obtain ⟨a,ha⟩ := Submodule.mem_span_singleton.mp hv
    obtain ⟨b,hb⟩ := Submodule.mem_span_singleton.mp hw
    have he := congrArg (fun X => coordinates 2 X 0) (ha.trans hb.symm)
    have ha0 : a=0 := by simpa [n,p,fixturePoint] using he
    simpa [ha0] using ha.symm
  have hc : IsCompl (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hd
    simp [UniversalLaw.Spec.Lifetime.E,hdN,hdP]
  refine ⟨Submodule.span ℝ {n},Submodule.span ℝ {p},hc,hdN,by simpa using hdP,?_,?_⟩
  · intro v hv hv0
    obtain ⟨a,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ha : a ≠ 0 := by intro h; apply hv0; simp [h]
    rw [fixture_hessian]
    simp [n,fixturePoint]
    nlinarith [mul_pos (sq_pos_of_ne_zero Real.pi_ne_zero) (sq_pos_of_ne_zero ha)]
  · intro v hv hv0
    obtain ⟨a,rfl⟩ := Submodule.mem_span_singleton.mp hv
    have ha : a ≠ 0 := by intro h; apply hv0; simp [h]
    rw [fixture_hessian]
    simp [p,fixturePoint]
    nlinarith [mul_pos (sq_pos_of_ne_zero Real.pi_ne_zero) (sq_pos_of_ne_zero ha)]

private theorem fixture_min_inertia :
    HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 1 1) 0 := by
  refine ⟨⊥,⊤,isCompl_bot_top,by simp,by simp [UniversalLaw.Spec.Lifetime.E],?_,?_⟩
  · intro v hv hv0
    exact (hv0 ((Submodule.mem_bot ℝ).mp hv)).elim
  · intro v _ hv
    have hn : v 0 ≠ 0 ∨ v 1 ≠ 0 := by
      by_contra! hh
      apply hv
      ext i
      fin_cases i <;> simp_all
    have hs : 0 < (v 0)^2+2*(v 1)^2 := by
      rcases hn with hn|hn
      · nlinarith [sq_pos_of_ne_zero hn,sq_nonneg (v 1)]
      · nlinarith [sq_pos_of_ne_zero hn,sq_nonneg (v 0)]
    rw [fixture_hessian]
    simp [fixturePoint]
    nlinarith [mul_pos (sq_pos_of_ne_zero Real.pi_ne_zero) hs]

private theorem fixture_max_inertia :
    HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 0 0) 2 := by
  refine I4SourceActualFoldCandidate.hessianHasInertia_two_of_diag _ _
    1 (-Real.pi^2) (-2*Real.pi^2) (by norm_num) ?_ ?_ 0 ?_
  · nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]
  · nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]
  · intro v
    rw [fixture_hessian]
    simp [fixturePoint] <;> ring

private theorem fixture_saddleOne_inertia :
    HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 := by
  refine I4SourceActualFoldCandidate.hessianHasInertia_one_of_diag _ _
    1 (Real.pi^2) (-2*Real.pi^2) (by norm_num) ?_ ?_ 0 ?_
  · exact sq_pos_of_ne_zero Real.pi_ne_zero
  · nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]
  · intro v
    rw [fixture_hessian]
    simp [fixturePoint] <;> ring

private theorem fixture_critical_max
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U)
    (hX : fixturePoint 0 0 ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ fixturePoint 0 0 ∈ W ∧
      W ⊆ U ∧ IsPathConnected (W ∩ {Y |
        actualField 2 2 fixtureSample (fixturePoint 0 0) ≤ actualField 2 2 fixtureSample Y}) := by
  exact criticalCoverLevelBasis (by norm_num) fixtureSample (fixturePoint 0 0) 2
    (fixture_critical 0) fixture_max_inertia U hU hX

private theorem fixture_critical_saddleOne
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U)
    (hX : fixturePoint 1 0 ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ fixturePoint 1 0 ∈ W ∧
      W ⊆ U ∧ IsPathConnected (W ∩ {Y |
        actualField 2 2 fixtureSample (fixturePoint 1 0) ≤ actualField 2 2 fixtureSample Y}) := by
  exact criticalCoverLevelBasis (by norm_num) fixtureSample (fixturePoint 1 0) 1
    (fixture_critical 1) fixture_saddleOne_inertia U hU hX

private theorem fixture_critical_saddleMinusOne
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U)
    (hX : fixturePoint 0 1 ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ fixturePoint 0 1 ∈ W ∧
      W ⊆ U ∧ IsPathConnected (W ∩ {Y |
        actualField 2 2 fixtureSample (fixturePoint 0 1) ≤ actualField 2 2 fixtureSample Y}) := by
  exact criticalCoverLevelBasis (by norm_num) fixtureSample (fixturePoint 0 1) 1
    (fixture_critical 2) fixture_saddleMinus_inertia U hU hX

private theorem fixture_critical_min
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U)
    (hX : fixturePoint 1 1 ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ fixturePoint 1 1 ∈ W ∧
      W ⊆ U ∧ IsPathConnected (W ∩ {Y |
        actualField 2 2 fixtureSample (fixturePoint 1 1) ≤ actualField 2 2 fixtureSample Y}) := by
  exact criticalCoverLevelBasis (by norm_num) fixtureSample (fixturePoint 1 1) 0
    (fixture_critical 3) fixture_min_inertia U hU hX

private theorem fixture_regular
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U)
    (hX : fixturePoint (1/2) 0 ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ fixturePoint (1/2) 0 ∈ W ∧
      W ⊆ U ∧ IsPathConnected (W ∩ {Y |
        actualField 2 2 fixtureSample (fixturePoint (1/2) 0) ≤ actualField 2 2 fixtureSample Y}) := by
  apply regularCoverLevelBasis (by norm_num) fixtureSample _ U hU hX
  intro he
  have hp : Real.pi*(1/2:ℝ) = Real.pi/2 := by ring
  have hv : fderiv ℝ (actualField 2 2 fixtureSample) (fixturePoint (1/2) 0)
      (fixturePoint 1 0) = -Real.pi := by
    rw [(fixture_hasFDerivAt _).fderiv]
    norm_num [fixtureDerivative,fixturePoint,fixtureCoord,hp]
  apply (neg_ne_zero.mpr Real.pi_ne_zero)
  calc
    -Real.pi = fderiv ℝ (actualField 2 2 fixtureSample) (fixturePoint (1/2) 0)
        (fixturePoint 1 0) := hv.symm
    _ = 0 := by rw [he]; rfl

private theorem fixture_interior
    (U : Set (UniversalLaw.Spec.Lifetime.E 2)) (hU : IsOpen U)
    (hX : fixturePoint 0 0 ∈ U) :
    ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2), IsOpen W ∧ fixturePoint 0 0 ∈ W ∧
      W ⊆ U ∧ IsPathConnected (W ∩ {Y | (2:ℝ) ≤ actualField 2 2 fixtureSample Y}) := by
  apply interiorCoverBasis (by norm_num) fixtureSample 2 _ U hU hX
  norm_num [fixture_actualField,fixturePoint]

private theorem fixture_seam
    (O : Set (I4Torus.SourceTorus 2 2)) (hO : IsOpen O)
    (hq : coverProjection 2 (fixturePoint 0 0) ∈ O) :
    ∃ V : Set (I4Torus.SourceTorus 2 2), IsOpen V ∧
      coverProjection 2 (fixturePoint 0 0) ∈ V ∧ V ⊆ O ∧
      IsPathConnected (V ∩ {z | (3:ℝ) ≤
        SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) fixtureSample z}) := by
  have hp : Continuous (coverProjection 2) :=
    (SourceActualFoldTorus.torusProjection2L_continuous 2).comp (coordinates 2).continuous
  obtain ⟨W,hW,hXW,hWU,hpc⟩ := fixture_critical_max
    ((coverProjection 2) ⁻¹' O) (hO.preimage hp) hq
  have hpc3 : IsPathConnected (W ∩ {Y | (3:ℝ) ≤ actualField 2 2 fixtureSample Y}) := by
    simpa only [show actualField 2 2 fixtureSample (fixturePoint 0 0) = 3 from fixture_heights 0] using hpc
  obtain ⟨hopen,_himage,htrace⟩ := projectCoverTrace (by norm_num) fixtureSample 3 W hW hpc3
  refine ⟨coverProjection 2 '' W,hopen,⟨fixturePoint 0 0,hXW,rfl⟩,?_,htrace⟩
  rintro q ⟨X,hX,rfl⟩
  exact hWU hX

/-- Every closed-superlevel member has arbitrarily small path-connected traces
in ambient-open neighborhoods of the same actual product AddCircle torus. -/
theorem actualSource_torus_closedSuperlevel_localPathConnectedBasis
    {L : ℝ} (hL : 0 < L) (omega : SmoothSample 2 L)
    (hm : IsMorseDistinct 2 L (actualField 2 L omega)) :
    ∀ (a : ℝ) (q : I4Torus.SourceTorus 2 L),
      a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega q →
      ∀ O : Set (I4Torus.SourceTorus 2 L), IsOpen O → q ∈ O →
        ∃ V : Set (I4Torus.SourceTorus 2 L), IsOpen V ∧ q ∈ V ∧ V ⊆ O ∧
          IsPathConnected (V ∩
            {z | a ≤ SourceActualFoldTorus.actualTorusField hL.ne' omega z}) := by
  intro a q haq O hO hq
  obtain ⟨x, hx⟩ := SourceActualFoldTorus.torusProjection2L_surjective L q
  let X : UniversalLaw.Spec.Lifetime.E 2 := (coordinates 2).symm x
  have hqX : coverProjection L X = q := by
    simpa only [coverProjection, X, ContinuousLinearEquiv.apply_symm_apply] using hx
  have hcont : Continuous (coverProjection L) :=
    (SourceActualFoldTorus.torusProjection2L_continuous L).comp (coordinates 2).continuous
  let U : Set (UniversalLaw.Spec.Lifetime.E 2) := coverProjection L ⁻¹' O
  have hU : IsOpen U := hO.preimage hcont
  have hXU : X ∈ U := by simpa only [U, mem_preimage, hqX] using hq
  have hpull : SourceActualFoldTorus.actualTorusField hL.ne' omega (coverProjection L X) =
      actualField 2 L omega X :=
    SourceActualFoldTorus.actualTorusField_pullback hL.ne' omega (coordinates 2 X)
  have haX : a ≤ actualField 2 L omega X := by
    rw [← hqX, hpull] at haq
    exact haq
  have hlocal : ∃ W : Set (UniversalLaw.Spec.Lifetime.E 2),
      IsOpen W ∧ X ∈ W ∧ W ⊆ U ∧
        IsPathConnected (W ∩ {Y | a ≤ actualField 2 L omega Y}) := by
    rcases lt_or_eq_of_le haX with ha | ha
    · exact interiorCoverBasis hL omega a X U hU hXU ha
    · by_cases hc : fderiv ℝ (actualField 2 L omega) X = 0
      · obtain ⟨j, hj⟩ := hm.1 X hc
        obtain ⟨W, hW, hXW, hWU, hpc⟩ :=
          criticalCoverLevelBasis hL omega X j hc hj U hU hXU
        exact ⟨W, hW, hXW, hWU, by simpa only [ha] using hpc⟩
      · obtain ⟨W, hW, hXW, hWU, hpc⟩ :=
          regularCoverLevelBasis hL omega X U hU hXU hc
        exact ⟨W, hW, hXW, hWU, by simpa only [ha] using hpc⟩
  obtain ⟨W, hW, hXW, hWU, hpc⟩ := hlocal
  obtain ⟨hV, _heq, hVpc⟩ := projectCoverTrace hL omega a W hW hpc
  refine ⟨coverProjection L '' W, hV, ⟨X, hXW, hqX⟩, ?_, hVpc⟩
  rintro z ⟨Y, hY, rfl⟩
  exact hWU hY

end I4SourceActualTorusSuperlevelLocalBasis
