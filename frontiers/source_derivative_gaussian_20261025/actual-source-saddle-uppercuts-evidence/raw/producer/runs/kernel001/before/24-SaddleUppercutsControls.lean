import SourceActualSaddleUppercuts
import SourceActualQuotientSaddleCollar
import SourceFiniteTrig
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.PathConnected
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
namespace ActualSaddleUppercutsControls

private abbrev Point2 := Fin 2 → ℝ
private def saddleValue (u : Point2) : ℝ := -(u 0)^2 + (u 1)^2
private def targetUpper (rho eps : ℝ) : Set Point2 :=
  Metric.ball 0 rho ∩ {u | eps ≤ saddleValue u}
private def targetUpperPos (rho eps : ℝ) : Set Point2 :=
  targetUpper rho eps ∩ {u | 0 < u 1}
private def targetUpperNeg (rho eps : ℝ) : Set Point2 :=
  targetUpper rho eps ∩ {u | u 1 < 0}

private structure ClosedBranchFacts (rho eps : ℝ) : Prop where
  plus_pc : IsPathConnected (targetUpperPos rho eps)
  minus_pc : IsPathConnected (targetUpperNeg rho eps)
  disjoint : Disjoint (targetUpperPos rho eps) (targetUpperNeg rho eps)
  partition : targetUpper rho eps = targetUpperPos rho eps ∪ targetUpperNeg rho eps
  plus_witness : (![0, rho/2] : Point2) ∈ targetUpperPos rho eps
  minus_witness : (![0, -rho/2] : Point2) ∈ targetUpperNeg rho eps

private def upperTrace {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (eps : ℝ) : Set (I4Torus.SourceTorus 2 L) :=
  phi.source ∩ {z | F q + eps ≤ F z}

private structure InheritedCollar {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop where
  center_mem : q ∈ phi.source
  center_eq : phi q = 0
  source_sub : phi.source ⊆ O
  target_eq : phi.target = Metric.ball 0 rho
  field_eq : ∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2
  lower_pc : ∀ delta : ℝ, 0 ≤ delta →
    IsPathConnected (phi.source ∩ {z | F q - delta ≤ F z})
  strict_test : ∀ p ∈ phi.source ∩ {z | F q < F z},
    ∀ r ∈ phi.source ∩ {z | F q < F z},
    JoinedIn (phi.source ∩ {z | F q < F z}) p r ↔ 0 < (phi p 1)*(phi r 1)

private def UpperClause {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) (eps : ℝ) : Prop :=
  let U := upperTrace F q phi eps
  let Bplus := U ∩ {z | 0 < phi z 1}
  let Bminus := U ∩ {z | phi z 1 < 0}
  IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
    U = Bplus ∪ Bminus ∧
    (∀ p ∈ U, ∀ r ∈ U, JoinedIn U p r ↔ 0 < (phi p 1)*(phi r 1))

private def UniformCutResult {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  q ∈ phi.source ∧ phi q = 0 ∧ phi.source ⊆ O ∧
  phi.target = Metric.ball 0 rho ∧
  (∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2) ∧
  (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | F q-delta ≤ F z})) ∧
  0 < rho^2/4 ∧ ∀ eps : ℝ, 0 < eps → eps < rho^2/4 → UpperClause F q phi eps

private def CutoffEquality {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (rho : ℝ)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  0 < rho^2/16 ∧ rho^2/16 < rho^2/4 ∧
  phi.symm (![0, rho/4] : Point2) ∈ upperTrace F q phi (rho^2/16) ∧
  phi.symm (![0, -rho/4] : Point2) ∈ upperTrace F q phi (rho^2/16) ∧
  F (phi.symm (![0, rho/4] : Point2)) = F q + rho^2/16 ∧
  F (phi.symm (![0, -rho/4] : Point2)) = F q + rho^2/16 ∧
  0 < phi (phi.symm (![0, rho/4] : Point2)) 1 ∧
  phi (phi.symm (![0, -rho/4] : Point2)) 1 < 0

private theorem cutoffEquality {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (hrho : 0 < rho)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (h : UniformCutResult F q O rho phi) : CutoffEquality F q rho phi := by
  have ht := h.2.2.2.1
  have hf := h.2.2.2.2.1
  have hball (s : ℝ) (hs : |s| < rho) : (![0,s] : Point2) ∈ phi.target := by
    rw [ht, Metric.mem_ball, dist_zero_right]
    apply (pi_norm_lt_iff hrho).2
    intro i
    fin_cases i
    · simpa using hrho
    · simpa using hs
  have hp : (![0,rho/4] : Point2) ∈ phi.target := hball _ (by rw [abs_of_pos (by positivity)]; linarith)
  have hm : (![0,-rho/4] : Point2) ∈ phi.target := hball _ (by rw [abs_of_neg (show -rho/4 < 0 by linarith)]; linarith)
  have hps := phi.map_target hp
  have hms := phi.map_target hm
  have hpi := phi.right_inv hp
  have hmi := phi.right_inv hm
  have hpf := hf _ hps
  have hmf := hf _ hms
  rw [hpi] at hpf
  rw [hmi] at hmf
  norm_num only [Fin.isValue, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, zero_pow] at hpf hmf
  have hpfe : F (phi.symm (![0,rho/4] : Point2)) = F q + rho^2/16 := by nlinarith [hpf]
  have hmfe : F (phi.symm (![0,-rho/4] : Point2)) = F q + rho^2/16 := by nlinarith [hmf]
  refine ⟨by positivity, by nlinarith [sq_pos_of_pos hrho], ⟨hps, hpfe.ge⟩,
    ⟨hms, hmfe.ge⟩, hpfe, hmfe, ?_, ?_⟩
  · rw [hpi]
    simpa using (show 0 < rho/4 by positivity)
  · rw [hmi]
    simpa using (show -rho/4 < 0 by linarith)

private def fixturePoly : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, Pi.single (0 : Fin 2) 1, 0⟩, ⟨2, Pi.single (1 : Fin 2) 1, 0⟩]
private def fixtureSample : I4SmoothCarrier.SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 fixturePoly)
    (I4SourceSmoothConditional.zeroSample 2 2)
private def fixturePoint (x y : ℝ) : UniversalLaw.Spec.Lifetime.E 2 :=
  (I4LifetimeField.coordinates 2).symm ![x,y]
private def fixtureCenter (x y : ℝ) : I4Torus.SourceTorus 2 2 :=
  I4Torus.torusProjection 2 2 ![x,y]
private def fixtureOpen (x y : ℝ) : Set (I4Torus.SourceTorus 2 2) :=
  I4Torus.torusProjection 2 2 '' (I4LifetimeField.coordinates 2 ''
    Metric.ball (fixturePoint x y) (1/8))
private def fixtureField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2 : ℝ) ≠ 0) fixtureSample

private theorem fixture_scalarSeries_finitePairing {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    I4Foundation.scalarSeries a v = I4SourceFinitePinKernel.finitePairing a v := by
  classical
  unfold I4Foundation.scalarSeries I4SourceFinitePinKernel.finitePairing
  exact tsum_eq_sum fun m hm => by
    rw [Finsupp.notMem_support_iff.mp hm, mul_zero]

private theorem fixture_source (u : Fin 2 → ℝ) :
    I4SmoothCarrier.smoothSourceField 2 2 fixtureSample u =
      Real.cos (Real.pi*u 0) + 2*Real.cos (Real.pi*u 1) := by
  have hv : I4SmoothCarrier.sampleInclusion 2 2 fixtureSample =
      fun m => I4SourceFiniteTrig.toSource 2 fixturePoly m := by
    funext m
    simp [fixtureSample, I4SmoothCarrier.sampleInclusion,
      I4SourceFinitePinKernel.finiteShiftSample_val, I4SourceSmoothConditional.zeroSample]
  change I4Foundation.scalarSeries (fun m => I4Source.modeCoefficient 2 2 m u)
    (I4SmoothCarrier.sampleInclusion 2 2 fixtureSample) = _
  rw [hv, fixture_scalarSeries_finitePairing,
    I4SourceFiniteTrig.toSource_eval (by norm_num : (2 : ℝ) ≠ 0)]
  norm_num [fixturePoly, I4SourceFiniteTrig.eval, I4SourceFiniteTrig.termEval,
    I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two, Pi.single_apply]

private theorem fixture_field (u : Fin 2 → ℝ) :
    fixtureField (I4Torus.torusProjection 2 2 u) =
      Real.cos (Real.pi*u 0) + 2*Real.cos (Real.pi*u 1) := by
  rw [fixtureField, SourceActualFoldTorus.actualTorusField_pullback]
  exact fixture_source u

private def coord (i : Fin 2) : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (ContinuousLinearMap.proj i).comp (I4LifetimeField.coordinates 2).toContinuousLinearMap
private def trigField (X : UniversalLaw.Spec.Lifetime.E 2) : ℝ :=
  Real.cos (Real.pi*coord 0 X) + 2*Real.cos (Real.pi*coord 1 X)
private def trigD (X : UniversalLaw.Spec.Lifetime.E 2) :
    UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ :=
  (-Real.sin (Real.pi*coord 0 X)*Real.pi) • coord 0 +
    (-2*Real.sin (Real.pi*coord 1 X)*Real.pi) • coord 1

private theorem fixture_actual : I4LifetimeField.actualField 2 2 fixtureSample = trigField := by
  funext X
  exact fixture_source (I4LifetimeField.coordinates 2 X)

private theorem trig_deriv (X : UniversalLaw.Spec.Lifetime.E 2) :
    HasFDerivAt trigField (trigD X) X := by
  have h0 := (((coord 0).hasFDerivAt (x := X)).const_mul Real.pi).cos
  have h1 := ((((coord 1).hasFDerivAt (x := X)).const_mul Real.pi).cos).const_mul 2
  convert h0.add h1 using 1 <;> ext v <;>
    simp [trigField, trigD, smul_eq_mul]; ring

private theorem trig_hessian (X v w : UniversalLaw.Spec.Lifetime.E 2) :
    hessian 2 trigField X v w =
      -Real.pi^2*Real.cos (Real.pi*coord 0 X)*(coord 0 v)*(coord 0 w) -
      2*Real.pi^2*Real.cos (Real.pi*coord 1 X)*(coord 1 v)*(coord 1 w) := by
  have hd : fderiv ℝ trigField = trigD := funext fun Y => (trig_deriv Y).fderiv
  have h0 := ((((coord 0).hasFDerivAt (x := X)).const_mul Real.pi).sin.neg.mul_const Real.pi).smul_const (coord 0)
  have h1 := (((((coord 1).hasFDerivAt (x := X)).const_mul Real.pi).sin.const_mul (-2)).mul_const Real.pi).smul_const (coord 1)
  have hh := h0.add h1
  change hessian 2 trigField X v w = _
  rw [hessian, iteratedFDeriv_succ_apply_right, iteratedFDeriv_one_apply]
  change fderiv ℝ (fderiv ℝ trigField) X v w = _
  rw [hd]
  have he := hh.fderiv
  change fderiv ℝ trigD X = _ at he
  rw [he]
  simp [ContinuousLinearMap.smulRight_apply, smul_eq_mul]
  ring

private theorem point_coords (x y : ℝ) :
    coord 0 (fixturePoint x y) = x ∧ coord 1 (fixturePoint x y) = y := by
  simp [coord, fixturePoint]

private theorem fixture_critical_of (x y : ℝ)
    (hx : Real.sin (Real.pi*x) = 0) (hy : Real.sin (Real.pi*y) = 0) :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) := by
  rw [IsCriticalPoint, fixture_actual, (trig_deriv _).fderiv]
  ext v
  simp [trigD, (point_coords x y).1, (point_coords x y).2, hx, hy]

private theorem axis0_ne : fixturePoint 1 0 ≠ 0 := by
  intro h
  have := congrArg (coord 0) h
  simp [(point_coords 1 0).1] at this
private theorem axis1_ne : fixturePoint 0 1 ≠ 0 := by
  intro h
  have := congrArg (coord 1) h
  simp [(point_coords 0 1).2] at this

private theorem axes_compl : IsCompl (ℝ ∙ fixturePoint 1 0) (ℝ ∙ fixturePoint 0 1) := by
  constructor
  · rw [Submodule.disjoint_def]
    intro v hv0 hv1
    rcases Submodule.mem_span_singleton.mp hv0 with ⟨a, rfl⟩
    rcases Submodule.mem_span_singleton.mp hv1 with ⟨b, hb⟩
    have ha := congrArg (coord 0) hb
    have ha0 : a = 0 := by simpa [(point_coords 0 1).1, (point_coords 1 0).1] using ha.symm
    simp [ha0]
  · rw [codisjoint_iff, Submodule.sup_eq_top_iff]
    intro v
    refine ⟨coord 0 v • fixturePoint 1 0, Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _),
      coord 1 v • fixturePoint 0 1, Submodule.smul_mem _ _ (Submodule.mem_span_singleton_self _), ?_⟩
    apply (I4LifetimeField.coordinates 2).injective
    have h0 : I4LifetimeField.coordinates 2 (fixturePoint 1 0) = (![1,0] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    have h1 : I4LifetimeField.coordinates 2 (fixturePoint 0 1) = (![0,1] : Point2) :=
      (I4LifetimeField.coordinates 2).apply_symm_apply _
    rw [map_add, map_smul, map_smul, h0, h1]
    ext i
    fin_cases i <;> simp [coord]

private theorem fixture_inertia_pos (x y : ℝ)
    (hx : Real.cos (Real.pi*x) = -1) (hy : Real.cos (Real.pi*y) = 1) :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) 1 := by
  rw [fixture_actual]
  refine ⟨ℝ ∙ fixturePoint 0 1, ℝ ∙ fixturePoint 1 0, axes_compl.symm,
    finrank_span_singleton axis1_ne, ?_, ?_, ?_⟩
  · simpa using finrank_span_singleton (K := ℝ) axis0_ne
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 0 1).1, (point_coords 0 1).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 1 0).1, (point_coords 1 0).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]

private theorem fixture_inertia_neg (x y : ℝ)
    (hx : Real.cos (Real.pi*x) = 1) (hy : Real.cos (Real.pi*y) = -1) :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) 1 := by
  rw [fixture_actual]
  refine ⟨ℝ ∙ fixturePoint 1 0, ℝ ∙ fixturePoint 0 1, axes_compl,
    finrank_span_singleton axis0_ne, ?_, ?_, ?_⟩
  · simpa using finrank_span_singleton (K := ℝ) axis1_ne
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 1 0).1, (point_coords 1 0).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]
  · intro v hv hne
    rcases Submodule.mem_span_singleton.mp hv with ⟨a, rfl⟩
    have ha : a ≠ 0 := fun h => hne (by simp [h])
    rw [trig_hessian]
    simp only [map_smul, smul_eq_mul, (point_coords 0 1).1, (point_coords 0 1).2,
      (point_coords x y).1, (point_coords x y).2, hx, hy]
    nlinarith only [mul_pos (sq_pos_of_pos Real.pi_pos) (sq_pos_of_ne_zero ha)]

private theorem fixture_positive_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 1 0) :=
  fixture_critical_of 1 0 (by simp) (by simp)
private theorem fixture_positive_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 1 0) 1 :=
  fixture_inertia_pos 1 0 (by simp) (by simp)
private theorem fixture_negative_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 0 1) :=
  fixture_critical_of 0 1 (by simp) (by simp)
private theorem fixture_negative_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint 0 1) 1 :=
  fixture_inertia_neg 0 1 (by simp) (by simp)
private theorem fixture_seam_critical :
    IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint (-1) 0) :=
  fixture_critical_of (-1) 0 (by simp) (by simp)
private theorem fixture_seam_inertia :
    HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint (-1) 0) 1 :=
  fixture_inertia_pos (-1) 0 (by simp) (by simp)

private theorem fixture_heights : fixtureField (fixtureCenter 1 0) = 1 ∧
    fixtureField (fixtureCenter 0 1) = -1 ∧ fixtureField (fixtureCenter (-1) 0) = 1 := by
  norm_num [fixtureCenter, fixture_field]

private theorem fixture_open (x y : ℝ) : IsOpen (fixtureOpen x y) ∧
    fixtureCenter x y ∈ fixtureOpen x y := by
  refine ⟨?_, ?_⟩
  · exact (SourceActualFoldTorus.torusProjection2L_open 2)
      _ ((I4LifetimeField.coordinates 2).isOpenMap _ Metric.isOpen_ball)
  · refine ⟨![x,y], ?_, rfl⟩
    exact ⟨fixturePoint x y, Metric.mem_ball_self (by norm_num), by simp [fixturePoint]⟩

private theorem fixture_seam : fixtureCenter (-1) 0 = fixtureCenter 1 0 := by
  funext i
  fin_cases i
  · change ((-1 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ))
    have h : (((-1 : ℝ)+2 : ℝ) : AddCircle (2 : ℝ)) = ((1 : ℝ) : AddCircle (2 : ℝ)) :=
      congrArg (fun t : ℝ => (t : AddCircle (2 : ℝ))) (by norm_num)
    exact (AddCircle.coe_add_period (2 : ℝ) (-1 : ℝ)).symm.trans h
  · rfl

private theorem fixture_consumer (x y : ℝ)
    (hc : IsCriticalPoint 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y))
    (hi : HessianHasInertia 2 (I4LifetimeField.actualField 2 2 fixtureSample) (fixturePoint x y) 1) :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter x y) (fixtureOpen x y) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter x y) rho phi := by
  have hh := I4SourceActualSaddleUppercuts.actualSource_quotient_saddle_uniform_closed_uppercuts (by norm_num : (0 : ℝ) < 2)
    fixtureSample (fixturePoint x y) hc hi (fixtureOpen x y) (fixture_open x y).1
  have hq : I4Torus.torusProjection 2 2 (I4LifetimeField.coordinates 2 (fixturePoint x y)) ∈ fixtureOpen x y := by
    simpa [fixturePoint, fixtureCenter] using (fixture_open x y).2
  obtain ⟨rho, hrho, phi, h⟩ := hh hq
  have hu : UniformCutResult fixtureField (fixtureCenter x y) (fixtureOpen x y) rho phi := by
    simpa [UniformCutResult, UpperClause, upperTrace, fixtureField, fixtureCenter, fixturePoint] using h
  exact ⟨rho, hrho, phi, hu, cutoffEquality _ _ _ _ hrho _ hu⟩

private theorem ordinary_positive_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 1 0) (fixtureOpen 1 0) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter 1 0) rho phi :=
  fixture_consumer 1 0 fixture_positive_critical fixture_positive_inertia
private theorem ordinary_negative_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 0 1) (fixtureOpen 0 1) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter 0 1) rho phi :=
  fixture_consumer 0 1 fixture_negative_critical fixture_negative_inertia
private theorem ordinary_seam_consumer :
    ∃ rho : ℝ, 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter (-1) 0) (fixtureOpen (-1) 0) rho phi ∧
      CutoffEquality fixtureField (fixtureCenter (-1) 0) rho phi :=
  fixture_consumer (-1) 0 fixture_seam_critical fixture_seam_inertia

private def ordinaryChosen :
    {rho : ℝ // 0 < rho ∧ ∃ phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2,
      UniformCutResult fixtureField (fixtureCenter 1 0) (fixtureOpen 1 0) rho phi} := by
  let rho := Classical.choose ordinary_positive_consumer
  have h := Classical.choose_spec ordinary_positive_consumer
  exact ⟨rho, h.1, Classical.choose h.2, (Classical.choose_spec h.2).1⟩
private def chosenRho : ℝ := ordinaryChosen.val
private def chosenPhi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 2) Point2 :=
  Classical.choose ordinaryChosen.property.2
private def chosenCenter : I4Torus.SourceTorus 2 2 := fixtureCenter 1 0
private def chosenBound : ℝ := chosenRho^2/4
private def chosenTrace (eps : ℝ) : Set (I4Torus.SourceTorus 2 2) :=
  upperTrace fixtureField chosenCenter chosenPhi eps
private def plusPoint : I4Torus.SourceTorus 2 2 := chosenPhi.symm (![0,chosenRho/2] : Point2)
private def minusPoint : I4Torus.SourceTorus 2 2 := chosenPhi.symm (![0,-chosenRho/2] : Point2)
private def boundaryTargetPoint (t : unitInterval) : Point2 :=
  ![0, (1-2*(t : ℝ))*chosenRho/2]
def nonnegativeUpperMutation : Prop :=
  ∀ eps : ℝ, 0 ≤ eps → eps < chosenBound → UpperClause fixtureField chosenCenter chosenPhi eps

private theorem chosen_positive : 0 < chosenRho := ordinaryChosen.property.1
private theorem chosen_uniform :
    UniformCutResult fixtureField chosenCenter (fixtureOpen 1 0) chosenRho chosenPhi :=
  Classical.choose_spec ordinaryChosen.property.2
private theorem chosen_structural : chosenCenter ∈ chosenPhi.source ∧
    chosenPhi chosenCenter = 0 ∧ chosenPhi.source ⊆ fixtureOpen 1 0 ∧
    chosenPhi.target = Metric.ball 0 chosenRho ∧
    ∀ z ∈ chosenPhi.source, fixtureField z = fixtureField chosenCenter -
      (chosenPhi z 0)^2 + (chosenPhi z 1)^2 :=
  ⟨chosen_uniform.1, chosen_uniform.2.1, chosen_uniform.2.2.1,
    chosen_uniform.2.2.2.1, chosen_uniform.2.2.2.2.1⟩

private theorem boundaryTargetPoint_mem (t : unitInterval) :
    boundaryTargetPoint t ∈ chosenPhi.target := by
  rw [chosen_structural.2.2.2.1, Metric.mem_ball, dist_zero_right]
  apply (pi_norm_lt_iff chosen_positive).2
  intro i
  fin_cases i
  · change |(0 : ℝ)| < chosenRho
    simpa using chosen_positive
  · change |(1-2*(t : ℝ))*chosenRho/2| < chosenRho
    have h0 := mul_nonneg t.property.1 chosen_positive.le
    have h1 := mul_le_mul_of_nonneg_right t.property.2 chosen_positive.le
    apply lt_of_le_of_lt (abs_le.mpr ?_) (show chosenRho/2 < chosenRho by linarith [chosen_positive])
    constructor <;> nlinarith

private def boundaryPath : Path plusPoint minusPoint where
  toFun := fun t => chosenPhi.symm (boundaryTargetPoint t)
  continuous_toFun := by
    apply chosenPhi.symm.continuousOn.comp_continuous
    · unfold boundaryTargetPoint
      fun_prop
    · intro t
      exact boundaryTargetPoint_mem t
  source' := by simp [boundaryTargetPoint, plusPoint]
  target' := by
    change chosenPhi.symm (![0,(1-2*(1 : ℝ))*chosenRho/2] : Point2) = minusPoint
    congr 1
    ext i
    fin_cases i <;> simp [minusPoint] <;> ring

private theorem boundaryPath_formula (t : unitInterval) :
    boundaryPath t = chosenPhi.symm (boundaryTargetPoint t) := rfl
private theorem boundaryPath_source (t : unitInterval) : boundaryPath t ∈ chosenPhi.source :=
  chosenPhi.map_target (boundaryTargetPoint_mem t)
private theorem boundaryPath_coordinates (t : unitInterval) :
    chosenPhi (boundaryPath t) = boundaryTargetPoint t :=
  chosenPhi.right_inv (boundaryTargetPoint_mem t)
private theorem boundaryPath_zero_cut (t : unitInterval) : boundaryPath t ∈ chosenTrace 0 := by
  refine ⟨boundaryPath_source t, ?_⟩
  have hf := chosen_structural.2.2.2.2 _ (boundaryPath_source t)
  rw [boundaryPath_coordinates] at hf
  change fixtureField chosenCenter + 0 ≤ fixtureField (boundaryPath t)
  change fixtureField (boundaryPath t) = fixtureField chosenCenter - 0^2 +
    ((1-2*(t : ℝ))*chosenRho/2)^2 at hf
  nlinarith [sq_nonneg ((1-2*(t : ℝ))*chosenRho/2)]
private theorem boundaryPath_midpoint :
    boundaryPath ⟨(1/2 : ℝ), by constructor <;> norm_num⟩ = chosenCenter := by
  rw [boundaryPath_formula]
  have he : boundaryTargetPoint ⟨(1/2 : ℝ), by constructor <;> norm_num⟩ = 0 := by
    ext i
    fin_cases i <;> norm_num [boundaryTargetPoint]
  rw [he, ← chosen_structural.2.1]
  exact chosenPhi.left_inv chosen_structural.1
private theorem boundary_joined : JoinedIn (chosenTrace 0) plusPoint minusPoint :=
  ⟨boundaryPath, boundaryPath_zero_cut⟩
private theorem boundary_endpoint_product :
    (chosenPhi plusPoint 1)*(chosenPhi minusPoint 1) = -chosenRho^2/4 := by
  have hp : (![0,chosenRho/2] : Point2) ∈ chosenPhi.target := by
    simpa [boundaryTargetPoint] using boundaryTargetPoint_mem (0 : unitInterval)
  have hm : (![0,-chosenRho/2] : Point2) ∈ chosenPhi.target := by
    convert boundaryTargetPoint_mem (1 : unitInterval) using 1 <;>
      congr 1 <;> ext i <;> fin_cases i <;> simp [boundaryTargetPoint] <;> ring
  change (chosenPhi (chosenPhi.symm (![0,chosenRho/2] : Point2)) 1)*
    (chosenPhi (chosenPhi.symm (![0,-chosenRho/2] : Point2)) 1) = _
  rw [chosenPhi.right_inv hp, chosenPhi.right_inv hm]
  simp only [Fin.isValue, Matrix.cons_val_one]
  ring
private theorem ordinary_cutoff_equality : CutoffEquality fixtureField chosenCenter chosenRho chosenPhi :=
  cutoffEquality _ _ (fixtureOpen 1 0) chosenRho chosen_positive chosenPhi chosen_uniform

theorem nonnegativeUpperMutation_false : ¬ nonnegativeUpperMutation := by
  intro hmut
  have hzero := hmut 0 (le_refl 0) (by exact div_pos (sq_pos_of_pos chosen_positive) (by norm_num))
  have hp : plusPoint ∈ chosenTrace 0 := by
    simpa using boundaryPath_zero_cut (0 : unitInterval)
  have hm : minusPoint ∈ chosenTrace 0 := by
    simpa using boundaryPath_zero_cut (1 : unitInterval)
  have hpositive := (hzero.2.2.2.2 plusPoint hp minusPoint hm).mp boundary_joined
  rw [boundary_endpoint_product] at hpositive
  have hs := sq_pos_of_pos chosen_positive
  linarith

end ActualSaddleUppercutsControls
