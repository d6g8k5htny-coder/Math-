import SourceActualQuotientSaddleCollar
import SourceActualMorseLocalModel
import SourceActualFoldTorus
import SourceFiniteTrig
import SourcePinPreservingQuartic
import Mathlib.Topology.Instances.AddCircle.Real
import Mathlib.Topology.Instances.ZMultiples
import Mathlib.Topology.OpenPartialHomeomorph.Constructions
import Mathlib.Topology.OpenPartialHomeomorph.Composition
import Mathlib.Topology.OpenPartialHomeomorph.IsImage
import Mathlib.Topology.OpenPartialHomeomorph.Basic
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Convert
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Abel
import Lean.Elab.Tactic.Omega

noncomputable section
open Set Filter Topology
open UniversalLaw.Spec.Lifetime
open I4LifetimeField I4SmoothCarrier
open scoped BigOperators Topology
set_option autoImplicit false

namespace QuotientSaddleCollarControls

def physicalProjection (L : ℝ) (X : UniversalLaw.Spec.Lifetime.E 2) :
    I4Torus.SourceTorus 2 L :=
  I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)

def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, Pi.single (0 : Fin 2) 1, 0⟩,
   ⟨2, Pi.single (1 : Fin 2) 1, 0⟩]

def fixtureSample : I4SmoothCarrier.SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)

def fixtureTorusField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample

def fixturePoint (x y : ℝ) : UniversalLaw.Spec.Lifetime.E 2 :=
  (coordinates 2).symm ![x,y]

def fixtureSmallOpen (X : UniversalLaw.Spec.Lifetime.E 2) :
    Set (I4Torus.SourceTorus 2 2) :=
  physicalProjection 2 '' Metric.ball X (1/8 : ℝ)

private theorem fixture_coordinateFormula (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 fixtureSample x =
      Real.cos (Real.pi * x 0) + 2 * Real.cos (Real.pi * x 1) := by
  let v := I4SourceFiniteTrig.toSource 2 fixturePolynomial
  have hsample : sampleInclusion 2 2 fixtureSample = v := by
    funext m
    simp [sampleInclusion, fixtureSample, I4SourceFinitePinKernel.finiteShiftSample_val,
      I4SourceSmoothConditional.zeroSample, v]
  change I4Source.sourceField 2 2 (sampleInclusion 2 2 fixtureSample) x = _
  rw [hsample]
  have hsum : (∑' m, I4Source.modeCoefficient 2 2 m x * v m) =
      I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x) v := by
    unfold I4SourceFinitePinKernel.finitePairing Finsupp.sum
    apply tsum_eq_sum
    intro m hm
    rw [Finsupp.notMem_support_iff.mp hm, mul_zero]
  change (∑' m, I4Source.modeCoefficient 2 2 m x * v m) = _
  rw [hsum]
  change I4SourceFinitePinKernel.finitePairing (fun m => I4Source.modeCoefficient 2 2 m x)
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial) = _
  rw [I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0)]
  norm_num [I4SourceFiniteTrig.eval, I4SourceFiniteTrig.termEval, fixturePolynomial,
    I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two, Pi.single_apply]

theorem fixture_actualField (Y : UniversalLaw.Spec.Lifetime.E 2) :
    actualField 2 2 fixtureSample Y =
      Real.cos (Real.pi * coordinates 2 Y 0) + 2 * Real.cos (Real.pi * coordinates 2 Y 1) :=
  fixture_coordinateFormula (coordinates 2 Y)

private def fixtureCoordinate (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i : (Fin 2 → ℝ) →L[ℝ] ℝ).comp (coordinates 2).toContinuousLinearMap

private def fixtureDerivative (Y : UniversalLaw.Spec.Lifetime.E 2) :
    UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (-Real.pi * Real.sin (Real.pi * coordinates 2 Y 0)) • fixtureCoordinate 0 +
    (-2 * Real.pi * Real.sin (Real.pi * coordinates 2 Y 1)) • fixtureCoordinate 1

private theorem fixture_hasFDerivAt (Y : UniversalLaw.Spec.Lifetime.E 2) :
    HasFDerivAt (actualField 2 2 fixtureSample) (fixtureDerivative Y) Y := by
  have a0 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 0)
      (Real.pi • fixtureCoordinate 0) Y := (fixtureCoordinate 0).hasFDerivAt.const_mul Real.pi
  have a1 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 1)
      (Real.pi • fixtureCoordinate 1) Y := (fixtureCoordinate 1).hasFDerivAt.const_mul Real.pi
  have d := a0.cos.add (a1.cos.const_mul 2)
  rw [show actualField 2 2 fixtureSample = fun Z : UniversalLaw.Spec.Lifetime.E 2 =>
      Real.cos (Real.pi * coordinates 2 Z 0) + 2 * Real.cos (Real.pi * coordinates 2 Z 1)
    from funext fixture_actualField]
  convert d using 1
  ext v
  simp [fixtureDerivative, fixtureCoordinate]
  ring

private theorem fixture_hessian (Y u v : UniversalLaw.Spec.Lifetime.E 2) :
    hessian 2 (actualField 2 2 fixtureSample) Y u v =
      (-Real.pi^2 * Real.cos (Real.pi * coordinates 2 Y 0)) * coordinates 2 u 0 * coordinates 2 v 0 +
      (-2 * Real.pi^2 * Real.cos (Real.pi * coordinates 2 Y 1)) * coordinates 2 u 1 * coordinates 2 v 1 := by
  rw [hessian, iteratedFDeriv_two_apply]
  rw [show fderiv ℝ (actualField 2 2 fixtureSample) = fixtureDerivative
    from funext fun Z => (fixture_hasFDerivAt Z).fderiv]
  have a0 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 0)
      (Real.pi • fixtureCoordinate 0) Y := (fixtureCoordinate 0).hasFDerivAt.const_mul Real.pi
  have a1 : HasFDerivAt (fun Z : UniversalLaw.Spec.Lifetime.E 2 => Real.pi * coordinates 2 Z 1)
      (Real.pi • fixtureCoordinate 1) Y := (fixtureCoordinate 1).hasFDerivAt.const_mul Real.pi
  have d := ((a0.sin.const_mul (-Real.pi)).smul_const (fixtureCoordinate 0)).add
    ((a1.sin.const_mul (-2 * Real.pi)).smul_const (fixtureCoordinate 1))
  rw [show fderiv ℝ fixtureDerivative Y = _ from d.fderiv]
  simp [fixtureCoordinate]
  ring

private def fixtureAxis (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 :=
  (coordinates 2).symm (Pi.single i 1)

private theorem fixtureAxis_coordinates (i : Fin 2) :
    coordinates 2 (fixtureAxis i) = (Pi.single i 1 : Fin 2 → ℝ) :=
  (coordinates 2).apply_symm_apply _

private theorem fixtureAxis_ne_zero (i : Fin 2) : fixtureAxis i ≠ 0 := by
  intro h
  have hz : (Pi.single i 1 : Fin 2 → ℝ) = 0 := by
    rw [← fixtureAxis_coordinates, h, map_zero]
  have hi := congrFun hz i
  norm_num at hi

private theorem fixture_negativeFirst_inertia (Y : UniversalLaw.Spec.Lifetime.E 2)
    (a b : ℝ) (ha : a < 0) (hb : 0 < b)
    (hquadratic : ∀ v, hessian 2 (actualField 2 2 fixtureSample) Y v v =
      a * (coordinates 2 v 0)^2 + b * (coordinates 2 v 1)^2) :
    HessianHasInertia 2 (actualField 2 2 fixtureSample) Y 1 := by
  let N := Submodule.span ℝ {fixtureAxis 0}
  let P := Submodule.span ℝ {fixtureAxis 1}
  have hN : Module.finrank ℝ N = 1 := finrank_span_singleton (fixtureAxis_ne_zero 0)
  have hP : Module.finrank ℝ P = 1 := finrank_span_singleton (fixtureAxis_ne_zero 1)
  have hd : Disjoint N P := by
    rw [Submodule.disjoint_def]
    intro v hvN hvP
    obtain ⟨s, hs⟩ := Submodule.mem_span_singleton.mp hvN
    obtain ⟨t, ht⟩ := Submodule.mem_span_singleton.mp hvP
    have he : s • (Pi.single (0 : Fin 2) 1 : Fin 2 → ℝ) =
        t • (Pi.single (1 : Fin 2) 1 : Fin 2 → ℝ) := by
      simpa only [map_smul, fixtureAxis_coordinates] using
        congrArg (coordinates 2) (hs.trans ht.symm)
    have hs0 : s = 0 := by
      have he0 := congrFun he 0
      simpa using he0
    rw [← hs, hs0, zero_smul]
  have hc : IsCompl N P := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hd
    simp [UniversalLaw.Spec.Lifetime.E, hN, hP]
  refine ⟨N, P, hc, hN, by simpa using hP, ?_, ?_⟩
  · intro v hv hv0
    obtain ⟨s, rfl⟩ := Submodule.mem_span_singleton.mp hv
    have hs : s ≠ 0 := by
      intro hs
      apply hv0
      simp [hs]
    rw [hquadratic]
    simp only [map_smul, fixtureAxis_coordinates]
    simpa using mul_neg_of_neg_of_pos ha (sq_pos_of_ne_zero hs)
  · intro v hv hv0
    obtain ⟨s, rfl⟩ := Submodule.mem_span_singleton.mp hv
    have hs : s ≠ 0 := by
      intro hs
      apply hv0
      simp [hs]
    rw [hquadratic]
    simp only [map_smul, fixtureAxis_coordinates]
    simpa using mul_pos hb (sq_pos_of_ne_zero hs)

private theorem fixture_pointCritical (x y : ℝ)
    (hx : Real.sin (Real.pi*x) = 0) (hy : Real.sin (Real.pi*y) = 0) :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint x y) := by
  change fderiv ℝ (actualField 2 2 fixtureSample) (fixturePoint x y) = 0
  rw [(fixture_hasFDerivAt _).fderiv]
  ext v
  change (-Real.pi * Real.sin (Real.pi * coordinates 2 (fixturePoint x y) 0)) *
      coordinates 2 v 0 + (-2 * Real.pi * Real.sin (Real.pi * coordinates 2 (fixturePoint x y) 1)) *
      coordinates 2 v 1 = 0
  simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
    Matrix.cons_val_zero, Matrix.cons_val_one, hx, hy, mul_zero, zero_mul, add_zero]

private theorem fixture_positiveInput :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 1 0) = 1 := by
  refine ⟨fixture_pointCritical 1 0 (by norm_num) (by norm_num), ?_, ?_⟩
  · apply I4SourceActualFoldCandidate.hessianHasInertia_one_of_diag _ _ 1
      (Real.pi^2) (-2*Real.pi^2) (by norm_num) (by positivity)
      (by nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]) 0
    intro v
    rw [fixture_hessian]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, mul_one, mul_zero, Real.cos_pi, Real.cos_zero]
    ring
  · rw [fixture_actualField]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num

private theorem fixture_negativeInput :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 0 1) = -1 := by
  refine ⟨fixture_pointCritical 0 1 (by norm_num) (by norm_num), ?_, ?_⟩
  · apply fixture_negativeFirst_inertia _ (-Real.pi^2) (2*Real.pi^2)
      (by nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]) (by positivity)
    intro v
    rw [fixture_hessian]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, mul_one, mul_zero, Real.cos_pi, Real.cos_zero]
    ring
  · rw [fixture_actualField]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num

theorem saddleInputs :
    (IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 1 0) = 1) ∧
    (IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint 0 1) = -1) :=
  ⟨fixture_positiveInput, fixture_negativeInput⟩

theorem seamInputs :
    IsCriticalPoint 2 (actualField 2 2 fixtureSample) (fixturePoint (-1) 0) ∧
      HessianHasInertia 2 (actualField 2 2 fixtureSample) (fixturePoint (-1) 0) 1 ∧
      actualField 2 2 fixtureSample (fixturePoint (-1) 0) = 1 ∧
      physicalProjection 2 (fixturePoint (-1) 0) = physicalProjection 2 (fixturePoint 1 0) := by
  refine ⟨fixture_pointCritical (-1) 0 (by norm_num) (by norm_num), ?_, ?_, ?_⟩
  · apply I4SourceActualFoldCandidate.hessianHasInertia_one_of_diag _ _ 1
      (Real.pi^2) (-2*Real.pi^2) (by norm_num) (by positivity)
      (by nlinarith [sq_pos_of_ne_zero Real.pi_ne_zero]) 0
    intro v
    rw [fixture_hessian]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one, mul_one, mul_zero, mul_neg_one,
      Real.cos_neg, Real.cos_pi, Real.cos_zero]
    ring
  · rw [fixture_actualField]
    simp only [fixturePoint, ContinuousLinearEquiv.apply_symm_apply,
      Matrix.cons_val_zero, Matrix.cons_val_one]
    norm_num
  · simp only [physicalProjection, fixturePoint, ContinuousLinearEquiv.apply_symm_apply]
    funext i
    fin_cases i
    · change ((-1 : ℝ) : _root_.AddCircle (2 : ℝ)) = ((1 : ℝ) : _root_.AddCircle (2 : ℝ))
      simpa only [show (-1 : ℝ)+2 = 1 by norm_num] using
        (_root_.AddCircle.coe_add_period (2 : ℝ) (-1)).symm
    · rfl

theorem smallOpen (X : UniversalLaw.Spec.Lifetime.E 2) :
    IsOpen (fixtureSmallOpen X) ∧ physicalProjection 2 X ∈ fixtureSmallOpen X := by
  have hopen : IsOpenMap (physicalProjection (2 : ℝ)) :=
    (SourceActualFoldTorus.torusProjection2L_open 2).comp (coordinates 2).toHomeomorph.isOpenMap
  exact ⟨hopen _ Metric.isOpen_ball, X, Metric.mem_ball_self (by norm_num), rfl⟩

def OrdinaryCollar (X : UniversalLaw.Spec.Lifetime.E 2) : Prop :=
  let q := physicalProjection 2 X
  let c := fixtureTorusField q
  ∃ rho : ℝ, 0 < rho ∧
    ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) (Fin 2 → ℝ),
      q ∈ phi.source ∧ phi q = 0 ∧ phi.source ⊆ fixtureSmallOpen X ∧
      phi.target = Metric.ball (0 : Fin 2 → ℝ) rho ∧
      (∀ z ∈ phi.source, fixtureTorusField z = c-(phi z 0)^2+(phi z 1)^2) ∧
      let W := phi.source ∩ {z | c < fixtureTorusField z}
      let Bplus := W ∩ {z | 0 < phi z 1}
      let Bminus := W ∩ {z | phi z 1 < 0}
      IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
        W = Bplus ∪ Bminus ∧
        (∀ p ∈ W, ∀ r ∈ W, JoinedIn W p r ↔ 0 < (phi p 1)*(phi r 1)) ∧
        (∀ delta : ℝ, 0 ≤ delta →
          IsPathConnected (phi.source ∩ {z | c-delta ≤ fixtureTorusField z}))


theorem positiveSaddle : OrdinaryCollar (fixturePoint 1 0) := by
  unfold OrdinaryCollar
  exact I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar
    (by norm_num) fixtureSample (fixturePoint 1 0) saddleInputs.1.1 saddleInputs.1.2.1
    (fixtureSmallOpen (fixturePoint 1 0)) (smallOpen _).1 (smallOpen _).2

theorem negativeSaddle : OrdinaryCollar (fixturePoint 0 1) := by
  unfold OrdinaryCollar
  exact I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar
    (by norm_num) fixtureSample (fixturePoint 0 1) saddleInputs.2.1 saddleInputs.2.2.1
    (fixtureSmallOpen (fixturePoint 0 1)) (smallOpen _).1 (smallOpen _).2

theorem seamSaddle : OrdinaryCollar (fixturePoint (-1) 0) := by
  unfold OrdinaryCollar
  exact I4SourceActualQuotientSaddleCollar.actualSource_quotient_saddle_local_collar
    (by norm_num) fixtureSample (fixturePoint (-1) 0) seamInputs.1 seamInputs.2.1
    (fixtureSmallOpen (fixturePoint (-1) 0)) (smallOpen _).1 (smallOpen _).2

def chosenRadius : ℝ := Classical.choose positiveSaddle

def chosenChart : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) (Fin 2 → ℝ) :=
  Classical.choose (Classical.choose_spec positiveSaddle).2

def chosenCenter : I4Torus.SourceTorus 2 2 := physicalProjection 2 (fixturePoint 1 0)
def chosenHeight : ℝ := fixtureTorusField chosenCenter
def chosenSource : Set (I4Torus.SourceTorus 2 2) := chosenChart.source

def chosenStrictTrace : Set (I4Torus.SourceTorus 2 2) :=
  chosenSource ∩ {z | chosenHeight < fixtureTorusField z}

theorem chosenChart_structure :
    0 < chosenRadius ∧ chosenCenter ∈ chosenChart.source ∧ chosenChart chosenCenter = 0 ∧
      chosenChart.source ⊆ fixtureSmallOpen (fixturePoint 1 0) ∧
      chosenChart.target = Metric.ball (0 : Fin 2 → ℝ) chosenRadius ∧
      (∀ z ∈ chosenChart.source,
        fixtureTorusField z = chosenHeight-(chosenChart z 0)^2+(chosenChart z 1)^2) := by
  have hr := (Classical.choose_spec positiveSaddle).1
  have hp := Classical.choose_spec (Classical.choose_spec positiveSaddle).2
  exact ⟨hr, hp.1, hp.2.1, hp.2.2.1, hp.2.2.2.1, hp.2.2.2.2.1⟩

theorem chosen_lowerTrace (delta : ℝ) (hdelta : 0 ≤ delta) :
    IsPathConnected (chosenSource ∩ {z | chosenHeight-delta ≤ fixtureTorusField z}) := by
  have hp := Classical.choose_spec (Classical.choose_spec positiveSaddle).2
  rcases hp with ⟨_, _, _, _, _, hbranches⟩
  rcases hbranches with ⟨_, _, _, _, _, hlower⟩
  exact hlower delta hdelta

private theorem ordinary_axisBall (rho : ℝ) (hrho : 0 < rho) :
    (![0,rho/2] : Fin 2 → ℝ) ∈ Metric.ball 0 rho ∧
      (![0,-rho/2] : Fin 2 → ℝ) ∈ Metric.ball 0 rho := by
  constructor
  · rw [Metric.mem_ball, dist_zero_right]
    apply (pi_norm_lt_iff hrho).2
    intro i
    fin_cases i
    · simpa using hrho
    · change ‖rho/2‖ < rho
      rw [Real.norm_eq_abs, abs_of_pos (half_pos hrho)]
      linarith
  · rw [Metric.mem_ball, dist_zero_right]
    apply (pi_norm_lt_iff hrho).2
    intro i
    fin_cases i
    · simpa using hrho
    · change ‖-rho/2‖ < rho
      rw [neg_div, norm_neg, Real.norm_eq_abs, abs_of_pos (half_pos hrho)]
      linarith

private theorem strictPlus_target :
    (![0,chosenRadius/2] : Fin 2 → ℝ) ∈ chosenChart.target := by
  rw [chosenChart_structure.2.2.2.2.1]
  exact (ordinary_axisBall chosenRadius chosenChart_structure.1).1

private theorem strictMinus_target :
    (![0,-chosenRadius/2] : Fin 2 → ℝ) ∈ chosenChart.target := by
  rw [chosenChart_structure.2.2.2.2.1]
  exact (ordinary_axisBall chosenRadius chosenChart_structure.1).2

def strictPointPlus : I4Torus.SourceTorus 2 2 := chosenChart.symm ![0,chosenRadius/2]
def strictPointMinus : I4Torus.SourceTorus 2 2 := chosenChart.symm ![0,-chosenRadius/2]

private theorem strictPlus_coordinates : chosenChart strictPointPlus = ![0,chosenRadius/2] :=
  chosenChart.right_inv strictPlus_target

private theorem strictMinus_coordinates : chosenChart strictPointMinus = ![0,-chosenRadius/2] :=
  chosenChart.right_inv strictMinus_target

theorem strictPoints_mem :
    strictPointPlus ∈ chosenStrictTrace ∧ strictPointMinus ∈ chosenStrictTrace := by
  have hplus : strictPointPlus ∈ chosenChart.source := chosenChart.symm.mapsTo strictPlus_target
  have hminus : strictPointMinus ∈ chosenChart.source := chosenChart.symm.mapsTo strictMinus_target
  have hr : 0 < chosenRadius/2 := half_pos chosenChart_structure.1
  constructor
  · refine ⟨hplus, ?_⟩
    change chosenHeight < fixtureTorusField strictPointPlus
    have hid := chosenChart_structure.2.2.2.2.2 strictPointPlus hplus
    rw [strictPlus_coordinates] at hid
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one, zero_pow, sub_zero] at hid
    nlinarith [sq_pos_of_pos hr]
  · refine ⟨hminus, ?_⟩
    change chosenHeight < fixtureTorusField strictPointMinus
    have hid := chosenChart_structure.2.2.2.2.2 strictPointMinus hminus
    rw [strictMinus_coordinates] at hid
    simp only [Matrix.cons_val_zero, Matrix.cons_val_one, zero_pow, sub_zero] at hid
    nlinarith [sq_pos_of_pos hr]

private theorem strictPlus_coordinate1 : chosenChart strictPointPlus 1 = chosenRadius/2 := by
  simpa only [Matrix.cons_val_one] using congrFun strictPlus_coordinates 1

private theorem strictMinus_coordinate1 : chosenChart strictPointMinus 1 = -chosenRadius/2 := by
  simpa only [Matrix.cons_val_one] using congrFun strictMinus_coordinates 1

theorem not_pathConnected_chosenStrictTrace : ¬ IsPathConnected chosenStrictTrace := by
  intro hpc
  have hj := hpc.joinedIn strictPointMinus strictPoints_mem.2 strictPointPlus strictPoints_mem.1
  have hcoordinate : ContinuousOn (fun z : I4Torus.SourceTorus 2 2 => chosenChart z 1)
      chosenStrictTrace :=
    (continuous_apply (1 : Fin 2)).continuousOn.comp
      (chosenChart.continuousOn.mono inter_subset_left) (by intro z hz; trivial)
  have hjReal := hj.map hcoordinate
  let gamma := hjReal.somePath
  have hg0 : gamma (0 : unitInterval) = -chosenRadius/2 := by
    calc
      gamma 0 = chosenChart strictPointMinus 1 := gamma.source
      _ = -chosenRadius/2 := strictMinus_coordinate1
  have hg1 : gamma (1 : unitInterval) = chosenRadius/2 := by
    calc
      gamma 1 = chosenChart strictPointPlus 1 := gamma.target
      _ = chosenRadius/2 := strictPlus_coordinate1
  have hbetween : (0 : ℝ) ∈ Icc (gamma 0) (gamma 1) := by
    rw [hg0, hg1]
    constructor <;> linarith [chosenChart_structure.1]
  obtain ⟨t, ht⟩ := intermediate_value_univ (0 : unitInterval) (1 : unitInterval)
    gamma.continuous hbetween
  have himage := hjReal.somePath_mem t
  rcases himage with ⟨z, hz, hzcoord⟩
  have hzero : chosenChart z 1 = 0 := by
    change chosenChart z 1 = gamma t at hzcoord
    exact hzcoord.trans ht
  have hzstrict : chosenHeight < fixtureTorusField z := hz.2
  have hid := chosenChart_structure.2.2.2.2.2 z hz.1
  rw [hzero] at hid
  nlinarith [sq_nonneg (chosenChart z 0)]

def strictPCMutation : Prop := IsPathConnected chosenStrictTrace

theorem not_strictPCMutation : ¬ strictPCMutation := not_pathConnected_chosenStrictTrace

end QuotientSaddleCollarControls
