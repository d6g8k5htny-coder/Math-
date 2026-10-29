import SourceActualTorusRegularSlab
import SourceConditionalMajorant
import SourceActualFoldTorus
import SourceFiniteTrig
import SourceSmoothConditionalKernel
import ClosedSuperlevel
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.Dual
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.ODE.PicardLindelof
import Mathlib.Analysis.ODE.ExistUnique
import Mathlib.Analysis.Normed.Field.Basic
import Mathlib.Topology.Order.Compact
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Topology.Maps.Basic
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Connected.PathConnected
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Positivity
import Lean.Elab.Tactic.Omega

noncomputable section
open Set Filter
open I4SmoothCarrier I4LifetimeField
open UniversalLaw.Spec.Lifetime
open scoped Topology BigOperators Matrix NNReal
set_option autoImplicit false
namespace TorusRegularSlabControls

abbrev Physical := UniversalLaw.Spec.Lifetime.E 2

def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1,![(2 : ℤ),0],0⟩,⟨(1/2 : ℝ),![(0 : ℤ),1],0⟩]
def fixtureSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)
def point (x y : ℝ) : Physical := (coordinates 2).symm ![x,y]
@[simp] theorem point_apply (x y : ℝ) (i : Fin 2) : point x y i = (![x,y] : Fin 2 → ℝ) i := by
  exact congrFun ((coordinates 2).apply_symm_apply (![x,y] : Fin 2 → ℝ)) i

theorem finiteField_value (p : I4SourceFiniteTrig.TrigPoly) (x : Fin 2 → ℝ) :
    smoothSourceField 2 2
      (I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 p)
        (I4SourceSmoothConditional.zeroSample 2 2)) x = I4SourceFiniteTrig.eval 2 p x := by
  classical
  change (∑' m, I4Source.modeCoefficient 2 2 m x *
    ((I4SourceSmoothConditional.zeroSample 2 2).val m+I4SourceFiniteTrig.toSource 2 p m)) = _
  simp only [I4SourceSmoothConditional.zeroSample,zero_add]
  rw [tsum_eq_sum (s := (I4SourceFiniteTrig.toSource 2 p).support)
    (fun m hm => by simp [Finsupp.notMem_support_iff.mp hm])]
  change I4SourceFinitePinKernel.finitePairing _ _ = _
  exact I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0) p x

def expression (x : Fin 2 → ℝ) : ℝ :=
  Real.cos (2*Real.pi*x 0)+(1/2 : ℝ)*Real.cos (Real.pi*x 1)

theorem coordinate_value (x : Fin 2 → ℝ) : smoothSourceField 2 2 fixtureSample x = expression x := by
  rw [fixtureSample,finiteField_value]
  have h0 : I4Source.phase 2 2 (![(2 : ℤ),0]) x = 2*Real.pi*x 0 := by
    unfold I4Source.phase I4Weights.sourceC
    rw [Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Int.cast_ofNat,Int.cast_zero]
    ring
  have h1 : I4Source.phase 2 2 (![(0 : ℤ),1]) x = Real.pi*x 1 := by
    unfold I4Source.phase I4Weights.sourceC
    rw [Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Int.cast_zero,Int.cast_one]
    ring
  simp [fixturePolynomial,I4SourceFiniteTrig.eval,I4SourceFiniteTrig.termEval,h0,h1,expression]

theorem fixture_actualField (X : Physical) : actualField 2 2 fixtureSample X =
    Real.cos (2*Real.pi*X 0)+(1/2 : ℝ)*Real.cos (Real.pi*X 1) := by
  change smoothSourceField 2 2 fixtureSample (coordinates 2 X) = _
  rw [coordinate_value]
  rfl

def projection (X : Physical) : I4Torus.SourceTorus 2 2 :=
  I4Torus.torusProjection 2 2 (coordinates 2 X)
def primaryField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample

theorem primary_pullback (X : Physical) : primaryField (projection X) = actualField 2 2 fixtureSample X :=
  SourceActualFoldTorus.actualTorusField_pullback (by norm_num) fixtureSample (coordinates 2 X)

def evalCoord (i : Fin 2) : (Fin 2 → ℝ) →L[ℝ] ℝ := ContinuousLinearMap.proj i
def derivative (x : Fin 2 → ℝ) : (Fin 2 → ℝ) →L[ℝ] ℝ :=
  (-(2*Real.pi)*Real.sin (2*Real.pi*x 0)) • evalCoord 0 +
    (-((1/2 : ℝ)*Real.pi)*Real.sin (Real.pi*x 1)) • evalCoord 1

theorem expression_hasFDerivAt (x : Fin 2 → ℝ) : HasFDerivAt expression (derivative x) x := by
  have h0 : HasFDerivAt (fun y : Fin 2 → ℝ => (2*Real.pi)*y 0)
      ((2*Real.pi) • evalCoord 0) x := (evalCoord 0).hasFDerivAt.const_mul (2*Real.pi)
  have h1 : HasFDerivAt (fun y : Fin 2 → ℝ => Real.pi*y 1)
      (Real.pi • evalCoord 1) x := (evalCoord 1).hasFDerivAt.const_mul Real.pi
  unfold expression
  convert h0.cos.add (h1.cos.const_mul (1/2 : ℝ)) using 1; ext v; simp [derivative,evalCoord]; ring

theorem actual_fderiv (X : Physical) :
    fderiv ℝ (actualField 2 2 fixtureSample) X =
      (derivative (coordinates 2 X)).comp (coordinates 2).toContinuousLinearMap := by
  have he : actualField 2 2 fixtureSample = expression ∘ coordinates 2 := by
    funext Y
    exact fixture_actualField Y
  rw [he]
  exact ((expression_hasFDerivAt (coordinates 2 X)).comp X (coordinates 2).hasFDerivAt).fderiv

theorem fixture_criticalHeights (X : Physical)
    (hc : IsCriticalPoint 2 (actualField 2 2 fixtureSample) X) :
    actualField 2 2 fixtureSample X ∈ ({3/2,1/2,-1/2,-3/2} : Set ℝ) := by
  change fderiv ℝ (actualField 2 2 fixtureSample) X = 0 at hc
  rw [actual_fderiv] at hc
  have h0 := congrArg (fun D : Physical →L[ℝ] ℝ => D (point 1 0)) hc
  have h1 := congrArg (fun D : Physical →L[ℝ] ℝ => D (point 0 1)) hc
  simp [derivative,evalCoord] at h0 h1
  rcases Real.sin_eq_zero_iff_cos_eq.mp h0 with hx|hx <;>
  rcases Real.sin_eq_zero_iff_cos_eq.mp h1 with hy|hy <;>
  rw [fixture_actualField,hx,hy] <;> norm_num

theorem fixture_fieldBounds (X : Physical) :
    (-3/2 : ℝ) ≤ actualField 2 2 fixtureSample X ∧ actualField 2 2 fixtureSample X ≤ 3/2 := by
  rw [fixture_actualField]
  constructor <;> nlinarith [Real.neg_one_le_cos (2*Real.pi*X 0),Real.cos_le_one (2*Real.pi*X 0),
    Real.neg_one_le_cos (Real.pi*X 1),Real.cos_le_one (Real.pi*X 1)]

theorem closedRegular_noCritical (X : Physical) (ha : (0 : ℝ) ≤ actualField 2 2 fixtureSample X)
    (hb : actualField 2 2 fixtureSample X ≤ 1/4) : fderiv ℝ (actualField 2 2 fixtureSample) X ≠ 0 := by
  intro hc
  have hh := fixture_criticalHeights X hc
  simp only [Set.mem_insert_iff,Set.mem_singleton_iff] at hh
  rcases hh with hh|hh|hh|hh <;> linarith

theorem closedRegular_public : Function.Bijective
    (TorusFiltration.superlevel_componentInclusion primaryField
      (s := -(1/4 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (by norm_num : (0 : ℝ) ≤ 1/4))) :=
  I4SourceActualTorusRegularSlab.actualSource_closedSlab_componentInclusion_bijective
    (by norm_num) fixtureSample 0 (1/4) (by norm_num) closedRegular_noCritical

theorem zeroWidth_public : Function.Bijective
    (TorusFiltration.superlevel_componentInclusion primaryField
      (s := -(0 : ℝ)) (t := -(0 : ℝ)) (neg_le_neg (le_refl (0 : ℝ)))) := by
  apply I4SourceActualTorusRegularSlab.actualSource_closedSlab_componentInclusion_bijective
    (by norm_num) fixtureSample 0 0 (by norm_num)
  intro X ha hb
  exact closedRegular_noCritical X ha (hb.trans (by norm_num))

theorem emptyBand_public : Function.Bijective
    (TorusFiltration.superlevel_componentInclusion primaryField
      (s := -(-2 : ℝ)) (t := -(-3 : ℝ)) (neg_le_neg (by norm_num : (-3 : ℝ) ≤ -2))) := by
  apply I4SourceActualTorusRegularSlab.actualSource_closedSlab_componentInclusion_bijective
    (by norm_num) fixtureSample (-3) (-2) (by norm_num)
  intro X _ha hb
  exfalso
  linarith [(fixture_fieldBounds X).1]

theorem primary_bounds (q : I4Torus.SourceTorus 2 2) : (-3/2 : ℝ) ≤ primaryField q ∧ primaryField q ≤ 3/2 := by
  obtain ⟨x,hx⟩ := SourceActualFoldTorus.torusProjection2L_surjective 2 q
  have hh := fixture_fieldBounds ((coordinates 2).symm x)
  simpa only [actualField,ContinuousLinearEquiv.apply_symm_apply,
    ← SourceActualFoldTorus.actualTorusField_pullback (by norm_num : (2 : ℝ) ≠ 0) fixtureSample x,hx,primaryField] using hh

theorem emptyBand_whole_nonempty :
    TorusFiltration.superlevel_set primaryField (2 : ℝ) = Set.univ ∧
    TorusFiltration.superlevel_set primaryField (3 : ℝ) = Set.univ ∧
    (TorusFiltration.superlevel_set primaryField (2 : ℝ)).Nonempty := by
  have h2 : TorusFiltration.superlevel_set primaryField (2 : ℝ) = Set.univ := by
    apply Set.eq_univ_of_forall
    intro q
    change (-2 : ℝ) ≤ primaryField q
    linarith [(primary_bounds q).1]
  have h3 : TorusFiltration.superlevel_set primaryField (3 : ℝ) = Set.univ := by
    apply Set.eq_univ_of_forall
    intro q
    change (-3 : ℝ) ≤ primaryField q
    linarith [(primary_bounds q).1]
  refine ⟨h2,h3,0,?_⟩
  rw [h2]
  trivial

def separatorPolynomial : I4SourceFiniteTrig.TrigPoly := [⟨1,![(1 : ℤ),0],0⟩]
def separatorSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 separatorPolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)
def separator : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) separatorSample

theorem separator_actualField (X : Physical) : actualField 2 2 separatorSample X = Real.cos (Real.pi*X 0) := by
  change smoothSourceField 2 2 separatorSample (coordinates 2 X) = _
  rw [separatorSample,finiteField_value]
  have hp : I4Source.phase 2 2 (![(1 : ℤ),0]) (coordinates 2 X) = Real.pi*X 0 := by
    unfold I4Source.phase I4Weights.sourceC
    rw [Fin.sum_univ_two]
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Int.cast_zero,Int.cast_one,coordinates_apply]
    ring
  simp [separatorPolynomial,I4SourceFiniteTrig.eval,I4SourceFiniteTrig.termEval,hp]

theorem separator_continuous : Continuous separator :=
  SourceActualFoldTorus.actualTorusField_continuous (by norm_num) separatorSample

theorem separator_pullback (X : Physical) : separator (projection X) = Real.cos (Real.pi*X 0) := by
  rw [separator,projection,SourceActualFoldTorus.actualTorusField_pullback]
  exact separator_actualField X

theorem projection_surjective : Function.Surjective projection := by
  intro q
  obtain ⟨x,hx⟩ := SourceActualFoldTorus.torusProjection2L_surjective 2 q
  exact ⟨(coordinates 2).symm x,by
    simpa only [projection,ContinuousLinearEquiv.apply_symm_apply] using hx⟩

theorem primary_le_separator (q : I4Torus.SourceTorus 2 2) : primaryField q ≤ 2*(separator q)^2-1/2 := by
  obtain ⟨X,rfl⟩ := projection_surjective q
  rw [primary_pullback,fixture_actualField,separator_pullback]
  have ha : 2*Real.pi*X 0 = Real.pi*X 0+Real.pi*X 0 := by ring
  rw [ha,Real.cos_add]
  nlinarith [Real.sin_sq_add_cos_sq (Real.pi*X 0),Real.cos_le_one (Real.pi*X 1)]

def mutant_a : ℝ := -1/2
def mutant_b : ℝ := 0

theorem openBand_noCritical (X : Physical) (ha : mutant_a < actualField 2 2 fixtureSample X)
    (hb : actualField 2 2 fixtureSample X < mutant_b) : fderiv ℝ (actualField 2 2 fixtureSample) X ≠ 0 := by
  intro hc
  have hh := fixture_criticalHeights X hc
  simp only [Set.mem_insert_iff,Set.mem_singleton_iff] at hh
  dsimp [mutant_a,mutant_b] at ha hb
  rcases hh with hh|hh|hh|hh <;> linarith

def upperPoint0 : TorusFiltration.superlevel_set primaryField (-mutant_b) :=
  ⟨projection (point 0 0),by
    change -(-mutant_b) ≤ primaryField (projection (point 0 0))
    rw [primary_pullback,fixture_actualField]
    norm_num [mutant_b]⟩
def upperPoint1 : TorusFiltration.superlevel_set primaryField (-mutant_b) :=
  ⟨projection (point 1 0),by
    change -(-mutant_b) ≤ primaryField (projection (point 1 0))
    rw [primary_pullback,fixture_actualField]
    norm_num [mutant_b]⟩

theorem separator_upper0 : separator upperPoint0.val = 1 := by
  change separator (projection (point 0 0)) = 1
  rw [separator_pullback]
  norm_num

theorem separator_upper1 : separator upperPoint1.val = -1 := by
  change separator (projection (point 1 0)) = -1
  rw [separator_pullback]
  norm_num

theorem upperClasses_ne : ZerothHomotopy.mk upperPoint0 ≠ ZerothHomotopy.mk upperPoint1 := by
  intro heq
  obtain ⟨p,hp⟩ := (TorusFiltration.superlevel_component_eq_iff_joinedIn
    primaryField (-mutant_b) upperPoint0 upperPoint1).mp heq
  have hcont : Continuous (fun t : unitInterval => separator (p t)) :=
    separator_continuous.comp p.continuous
  have h0 : separator (p (0 : unitInterval)) = 1 := by
    simpa only [Path.source] using separator_upper0
  have h1 : separator (p (1 : unitInterval)) = -1 := by
    simpa only [Path.target] using separator_upper1
  have hinter : (0 : ℝ) ∈ Icc (separator (p (1 : unitInterval))) (separator (p (0 : unitInterval))) := by
    rw [h0,h1]
    norm_num
  obtain ⟨t,_ht,htzero⟩ := isPreconnected_univ.intermediate_value
    (a := (1 : unitInterval)) (b := (0 : unitInterval)) (Set.mem_univ _) (Set.mem_univ _)
    hcont.continuousOn hinter
  have hupper : (0 : ℝ) ≤ primaryField (p t) := by
    simpa only [TorusFiltration.superlevel_set,Set.mem_ofPred_eq,mutant_b,neg_zero] using hp t
  have hbound := primary_le_separator (p t)
  rw [htzero] at hbound
  nlinarith

def lowerCurve (s : ℝ) : I4Torus.SourceTorus 2 2 := projection (point s 0)

theorem lowerCurve_continuous : Continuous lowerCurve := by
  change Continuous (fun s : ℝ => I4Torus.torusProjection 2 2
    (coordinates 2 ((coordinates 2).symm ![s,0])))
  simp only [ContinuousLinearEquiv.apply_symm_apply]
  apply (SourceActualFoldTorus.torusProjection2L_continuous 2).comp
  apply continuous_pi
  intro i
  fin_cases i <;> fun_prop

theorem lowerJoined : JoinedIn (TorusFiltration.superlevel_set primaryField (-mutant_a))
    upperPoint0.val upperPoint1.val := by
  apply JoinedIn.ofLine lowerCurve_continuous.continuousOn
  · rfl
  · rfl
  · rintro Y ⟨s,_hs,rfl⟩
    change (-1/2 : ℝ) ≤ primaryField (projection (point s 0))
    rw [primary_pullback,fixture_actualField]
    simp only [point_apply,Matrix.cons_val_zero,Matrix.cons_val_one,mul_zero,Real.cos_zero,mul_one]
    linarith [Real.neg_one_le_cos (2*Real.pi*s)]

def fixedInclusion :
    ZerothHomotopy (TorusFiltration.superlevel_set primaryField (-mutant_b)) →
      ZerothHomotopy (TorusFiltration.superlevel_set primaryField (-mutant_a)) :=
  TorusFiltration.superlevel_componentInclusion primaryField (s := -mutant_b) (t := -mutant_a)
    (neg_le_neg (by norm_num [mutant_a,mutant_b] : mutant_a ≤ mutant_b))

theorem lowerImages_eq : fixedInclusion (ZerothHomotopy.mk upperPoint0) =
    fixedInclusion (ZerothHomotopy.mk upperPoint1) := by
  apply (TorusFiltration.superlevel_component_eq_iff_joinedIn primaryField (-mutant_a) _ _).mpr
  exact lowerJoined

theorem not_injective_componentInclusion : ¬ Function.Injective fixedInclusion := by
  intro h
  exact upperClasses_ne (h lowerImages_eq)

theorem not_bijective_componentInclusion : ¬ Function.Bijective fixedInclusion := by
  intro h
  exact not_injective_componentInclusion h.1

def openBandVariantAtFixture : Prop :=
  (∀ X : Physical, mutant_a < actualField 2 2 fixtureSample X →
    actualField 2 2 fixtureSample X < mutant_b → fderiv ℝ (actualField 2 2 fixtureSample) X ≠ 0) →
  Function.Bijective fixedInclusion

theorem not_openBandVariantAtFixture : ¬ openBandVariantAtFixture := by
  intro h
  exact not_bijective_componentInclusion (h openBand_noCritical)

end TorusRegularSlabControls
