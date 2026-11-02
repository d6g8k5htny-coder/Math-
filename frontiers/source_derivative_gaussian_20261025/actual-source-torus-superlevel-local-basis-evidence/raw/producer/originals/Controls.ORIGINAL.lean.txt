import SourceActualTorusSuperlevelLocalBasis
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
namespace TorusSuperlevelLocalBasisControls

def fixturePolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1,Pi.single (0:Fin 2) 1,0⟩,⟨2,Pi.single (1:Fin 2) 1,0⟩]

def fixtureSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)

def fixturePoint (x y : ℝ) : UniversalLaw.Spec.Lifetime.E 2 :=
  (coordinates 2).symm ![x,y]

@[simp] theorem fixturePoint_apply (x y : ℝ) (i : Fin 2) :
    fixturePoint x y i = (![x,y] : Fin 2 → ℝ) i := by
  have hh := congrFun ((coordinates 2).apply_symm_apply (![x,y] : Fin 2 → ℝ)) i
  exact hh

def fixtureProjection (X : UniversalLaw.Spec.Lifetime.E 2) : I4Torus.SourceTorus 2 2 :=
  I4Torus.torusProjection 2 2 (coordinates 2 X)

def coordinateExpression (x : Fin 2 → ℝ) : ℝ :=
  Real.cos (Real.pi*x 0)+2*Real.cos (Real.pi*x 1)

theorem fixture_coordinateField : smoothSourceField 2 2 fixtureSample = coordinateExpression := by
  classical
  funext x
  change (∑' m, I4Source.modeCoefficient 2 2 m x *
    ((I4SourceSmoothConditional.zeroSample 2 2).val m+
      I4SourceFiniteTrig.toSource 2 fixturePolynomial m)) = _
  simp only [I4SourceSmoothConditional.zeroSample,zero_add]
  rw [tsum_eq_sum (s := (I4SourceFiniteTrig.toSource 2 fixturePolynomial).support)
    (fun m hm => by simp [Finsupp.notMem_support_iff.mp hm])]
  have he := I4SourceFiniteTrig.toSource_eval (by norm_num : (2:ℝ) ≠ 0) fixturePolynomial x
  change I4SourceFinitePinKernel.finitePairing _ _ = _
  rw [he]
  simp [fixturePolynomial,I4SourceFiniteTrig.eval,I4SourceFiniteTrig.termEval,
    I4Source.phase,I4Weights.sourceC,Fin.sum_univ_two,coordinateExpression]

theorem fixture_actualField (X : UniversalLaw.Spec.Lifetime.E 2) :
    actualField 2 2 fixtureSample X = Real.cos (Real.pi*X 0)+2*Real.cos (Real.pi*X 1) := by
  change smoothSourceField 2 2 fixtureSample (coordinates 2 X) = _
  rw [fixture_coordinateField]
  rfl

def coordinateProj (i : Fin 2) : (Fin 2 → ℝ) →L[ℝ] ℝ := ContinuousLinearMap.proj i

def coordinateDerivative (x : Fin 2 → ℝ) : (Fin 2 → ℝ) →L[ℝ] ℝ :=
  (-Real.pi*Real.sin (Real.pi*x 0)) • coordinateProj 0 +
    (-2*Real.pi*Real.sin (Real.pi*x 1)) • coordinateProj 1

theorem coordinate_hasFDerivAt (x : Fin 2 → ℝ) :
    HasFDerivAt coordinateExpression (coordinateDerivative x) x := by
  have h0 : HasFDerivAt (fun y : Fin 2 → ℝ => Real.pi*y 0)
      (Real.pi • coordinateProj 0) x := (coordinateProj 0).hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun y : Fin 2 → ℝ => Real.pi*y 1)
      (Real.pi • coordinateProj 1) x := (coordinateProj 1).hasFDerivAt.const_mul Real.pi
  have hh := h0.cos.add (h1.cos.const_mul 2)
  unfold coordinateExpression
  convert hh using 1 <;> ext v <;> simp [coordinateDerivative,coordinateProj] <;> ring

theorem coordinate_second (x u v : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 coordinateExpression x ![u,v] =
      -Real.pi^2*Real.cos (Real.pi*x 0)*u 0*v 0-
        2*Real.pi^2*Real.cos (Real.pi*x 1)*u 1*v 1 := by
  rw [iteratedFDeriv_two_apply]
  have he : fderiv ℝ coordinateExpression = coordinateDerivative :=
    funext fun y => (coordinate_hasFDerivAt y).fderiv
  rw [he]
  have h0 : HasFDerivAt (fun y : Fin 2 → ℝ => Real.pi*y 0)
      (Real.pi • coordinateProj 0) x := (coordinateProj 0).hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun y : Fin 2 → ℝ => Real.pi*y 1)
      (Real.pi • coordinateProj 1) x := (coordinateProj 1).hasFDerivAt.const_mul Real.pi
  have hh := ((h0.sin.const_mul (-Real.pi)).smul_const (coordinateProj 0)).add
    ((h1.sin.const_mul (-2*Real.pi)).smul_const (coordinateProj 1))
  rw [show fderiv ℝ coordinateDerivative x = _ from hh.fderiv]
  simp [coordinateProj] <;> ring

theorem fixture_physical_fderiv (X : UniversalLaw.Spec.Lifetime.E 2) :
    fderiv ℝ (actualField 2 2 fixtureSample) X =
      (coordinateDerivative (coordinates 2 X)).comp (coordinates 2).toContinuousLinearMap := by
  have hh := (coordinate_hasFDerivAt (coordinates 2 X)).comp X (coordinates 2).hasFDerivAt
  have hf : actualField 2 2 fixtureSample = coordinateExpression ∘ coordinates 2 := by
    funext Y
    exact fixture_actualField Y
  rw [hf]
  exact hh.fderiv

theorem fixture_hessian (X u v : UniversalLaw.Spec.Lifetime.E 2) :
    hessian 2 (actualField 2 2 fixtureSample) X u v =
      -Real.pi^2*Real.cos (Real.pi*X 0)*u 0*v 0-
        2*Real.pi^2*Real.cos (Real.pi*X 1)*u 1*v 1 := by
  rw [I4SourceActualFoldCandidate.actual_hessian_coordinates (by norm_num),fixture_coordinateField]
  exact coordinate_second _ _ _

theorem fixture_critical_integral (X : UniversalLaw.Spec.Lifetime.E 2)
    (hc : IsCriticalPoint 2 (actualField 2 2 fixtureSample) X) :
    ∃ n : Fin 2 → ℤ, ∀ i, X i = (n i : ℝ) := by
  have hd : (coordinateDerivative (coordinates 2 X)).comp (coordinates 2).toContinuousLinearMap = 0 := by
    rw [← fixture_physical_fderiv]
    exact hc
  have h0 := congrArg (fun D : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ => D (fixturePoint 1 0)) hd
  have h1 := congrArg (fun D : UniversalLaw.Spec.Lifetime.E 2 →L[ℝ] ℝ => D (fixturePoint 0 1)) hd
  have hs0 : Real.sin (Real.pi*X 0) = 0 := by
    have he : (-Real.pi)*Real.sin (Real.pi*X 0) = 0 := by
      simpa [coordinateDerivative,coordinateProj,fixturePoint] using h0
    exact (mul_eq_zero.mp he).resolve_left (neg_ne_zero.mpr Real.pi_ne_zero)
  have hs1 : Real.sin (Real.pi*X 1) = 0 := by
    have he : (-2*Real.pi)*Real.sin (Real.pi*X 1) = 0 := by
      simpa [coordinateDerivative,coordinateProj,fixturePoint] using h1
    exact (mul_eq_zero.mp he).resolve_left (mul_ne_zero (by norm_num) Real.pi_ne_zero)
  obtain ⟨n0,hn0⟩ := Real.sin_eq_zero_iff.mp hs0
  obtain ⟨n1,hn1⟩ := Real.sin_eq_zero_iff.mp hs1
  refine ⟨![n0,n1],?_⟩
  intro i
  fin_cases i
  · apply mul_left_cancel₀ Real.pi_ne_zero
    nlinarith [hn0]
  · apply mul_left_cancel₀ Real.pi_ne_zero
    nlinarith [hn1]

private theorem diagonal_x_negative (g : UniversalLaw.Spec.Lifetime.E 2 → ℝ)
    (X : UniversalLaw.Spec.Lifetime.E 2) (a b : ℝ) (ha : a < 0) (hb : 0 < b)
    (hq : ∀ v, hessian 2 g X v v = a*(v 0)^2+b*(v 1)^2) :
    HessianHasInertia 2 g X 1 := by
  let n := fixturePoint 1 0
  let p := fixturePoint 0 1
  have hn : n ≠ 0 := by
    intro he
    have hh := congrArg (fun Z => coordinates 2 Z 0) he
    norm_num [n,fixturePoint] at hh
  have hp : p ≠ 0 := by
    intro he
    have hh := congrArg (fun Z => coordinates 2 Z 1) he
    norm_num [p,fixturePoint] at hh
  have hdn : Module.finrank ℝ (Submodule.span ℝ {n}) = 1 := finrank_span_singleton hn
  have hdp : Module.finrank ℝ (Submodule.span ℝ {p}) = 1 := finrank_span_singleton hp
  have hdis : Disjoint (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    rw [Submodule.disjoint_def]
    intro z hz hw
    obtain ⟨s,hs⟩ := Submodule.mem_span_singleton.mp hz
    obtain ⟨t,ht⟩ := Submodule.mem_span_singleton.mp hw
    have he := congrArg (fun Z => coordinates 2 Z 0) (hs.trans ht.symm)
    have hs0 : s=0 := by simpa [n,p,fixturePoint] using he
    simpa [hs0] using hs.symm
  have hcompl : IsCompl (Submodule.span ℝ {n}) (Submodule.span ℝ {p}) := by
    apply (Submodule.isCompl_iff_disjoint _ _ ?_).mpr hdis
    simp [UniversalLaw.Spec.Lifetime.E,hdn,hdp]
  refine ⟨Submodule.span ℝ {n},Submodule.span ℝ {p},hcompl,hdn,by simpa using hdp,?_,?_⟩
  · intro z hz hz0
    obtain ⟨s,rfl⟩ := Submodule.mem_span_singleton.mp hz
    have hs : s ≠ 0 := by intro he; apply hz0; simp [he]
    rw [hq]
    simpa [n,fixturePoint] using mul_neg_of_neg_of_pos ha (sq_pos_of_ne_zero hs)
  · intro z hz hz0
    obtain ⟨s,rfl⟩ := Submodule.mem_span_singleton.mp hz
    have hs : s ≠ 0 := by intro he; apply hz0; simp [he]
    rw [hq]
    simpa [p,fixturePoint] using mul_pos hb (sq_pos_of_ne_zero hs)

private theorem diagonal_positive (g : UniversalLaw.Spec.Lifetime.E 2 → ℝ)
    (X : UniversalLaw.Spec.Lifetime.E 2) (a b : ℝ) (ha : 0 < a) (hb : 0 < b)
    (hq : ∀ v, hessian 2 g X v v = a*(v 0)^2+b*(v 1)^2) :
    HessianHasInertia 2 g X 0 := by
  refine ⟨⊥,⊤,isCompl_bot_top,by simp,by simp [UniversalLaw.Spec.Lifetime.E],?_,?_⟩
  · intro v hv hv0
    exact (hv0 ((Submodule.mem_bot ℝ).mp hv)).elim
  · intro v _ hv
    have hn : v 0 ≠ 0 ∨ v 1 ≠ 0 := by
      by_contra! hh
      apply hv
      ext i
      fin_cases i <;> simp_all
    rw [hq]
    rcases hn with hn|hn
    · exact add_pos_of_pos_of_nonneg (mul_pos ha (sq_pos_of_ne_zero hn))
        (mul_nonneg hb.le (sq_nonneg _))
    · exact add_pos_of_nonneg_of_pos (mul_nonneg ha.le (sq_nonneg _))
        (mul_pos hb (sq_pos_of_ne_zero hn))

private theorem diagonal_inertia (g : UniversalLaw.Spec.Lifetime.E 2 → ℝ)
    (X : UniversalLaw.Spec.Lifetime.E 2) (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0)
    (hq : ∀ v, hessian 2 g X v v = a*(v 0)^2+b*(v 1)^2) :
    ∃ j : ℕ, HessianHasInertia 2 g X j := by
  rcases lt_or_gt_of_ne ha with ha|ha
  · rcases lt_or_gt_of_ne hb with hb|hb
    · refine ⟨2,I4SourceActualFoldCandidate.hessianHasInertia_two_of_diag
        g X 1 a b (by norm_num) ha hb 0 ?_⟩
      intro v
      rw [hq]
      simp <;> ring
    · exact ⟨1,diagonal_x_negative g X a b ha hb hq⟩
  · rcases lt_or_gt_of_ne hb with hb|hb
    · refine ⟨1,I4SourceActualFoldCandidate.hessianHasInertia_one_of_diag
        g X 1 a b (by norm_num) ha hb 0 ?_⟩
      intro v
      rw [hq]
      simp <;> ring
    · exact ⟨0,diagonal_positive g X a b ha hb hq⟩

private theorem same_sign_even_difference (x y : ℝ)
    (hx : Real.sin (Real.pi*x)=0) (hy : Real.sin (Real.pi*y)=0)
    (he : Real.cos (Real.pi*x)=Real.cos (Real.pi*y)) :
    ∃ k : ℤ, x-y=2*(k:ℝ) := by
  have hc : Real.cos (Real.pi*y)^2=1 := by
    rcases Real.sin_eq_zero_iff_cos_eq.mp hy with hh|hh <;> rw [hh] <;> norm_num
  have hd : Real.cos (Real.pi*(x-y))=1 := by
    rw [mul_sub,Real.cos_sub,hx,hy,he]
    nlinarith [hc]
  obtain ⟨k,hk⟩ := (Real.cos_eq_one_iff (Real.pi*(x-y))).mp hd
  refine ⟨k,?_⟩
  apply mul_left_cancel₀ Real.pi_ne_zero
  nlinarith [hk]

private theorem lattice_distance_zero (X Y : UniversalLaw.Spec.Lifetime.E 2)
    (k0 k1 : ℤ) (h0 : X 0-Y 0=2*(k0:ℝ)) (h1 : X 1-Y 1=2*(k1:ℝ)) :
    torusDist 2 2 X Y=0 := by
  let n : Fin 2 → ℤ := ![-k0,-k1]
  have hz : X-Y+latticeVec 2 2 n=0 := by
    ext i
    fin_cases i
    · simp [latticeVec,n]
      nlinarith [h0]
    · simp [latticeVec,n]
      nlinarith [h1]
  have hb : BddBelow (Set.range (fun n : Fin 2 → ℤ => ‖X-Y+latticeVec 2 2 n‖)) :=
    ⟨0,by rintro _ ⟨n,rfl⟩; exact norm_nonneg _⟩
  apply le_antisymm
  · have hh := ciInf_le hb n
    simpa [torusDist,hz] using hh
  · exact le_ciInf fun n => norm_nonneg _

theorem fixture_morseDistinct : IsMorseDistinct 2 2 (actualField 2 2 fixtureSample) := by
  constructor
  · intro X hc
    obtain ⟨n,hn⟩ := fixture_critical_integral X hc
    have hs (i : Fin 2) : Real.sin (Real.pi*X i)=0 := by
      rw [hn i,mul_comm]
      exact Real.sin_int_mul_pi _
    have ha : -Real.pi^2*Real.cos (Real.pi*X 0) ≠ 0 := by
      rcases Real.sin_eq_zero_iff_cos_eq.mp (hs 0) with he|he <;>
        rw [he] <;> positivity
    have hb : -2*Real.pi^2*Real.cos (Real.pi*X 1) ≠ 0 := by
      rcases Real.sin_eq_zero_iff_cos_eq.mp (hs 1) with he|he <;>
        rw [he] <;> positivity
    apply diagonal_inertia _ X _ _ ha hb
    intro v
    rw [fixture_hessian]
    ring
  · intro X Y hX hY hdist heq
    obtain ⟨nx,hnx⟩ := fixture_critical_integral X hX
    obtain ⟨ny,hny⟩ := fixture_critical_integral Y hY
    have hsX (i : Fin 2) : Real.sin (Real.pi*X i)=0 := by
      rw [hnx i,mul_comm]
      exact Real.sin_int_mul_pi _
    have hsY (i : Fin 2) : Real.sin (Real.pi*Y i)=0 := by
      rw [hny i,mul_comm]
      exact Real.sin_int_mul_pi _
    rw [fixture_actualField,fixture_actualField] at heq
    have hsign : Real.cos (Real.pi*X 0)=Real.cos (Real.pi*Y 0) ∧
        Real.cos (Real.pi*X 1)=Real.cos (Real.pi*Y 1) := by
      rcases Real.sin_eq_zero_iff_cos_eq.mp (hsX 0) with hx0|hx0 <;>
      rcases Real.sin_eq_zero_iff_cos_eq.mp (hsX 1) with hx1|hx1 <;>
      rcases Real.sin_eq_zero_iff_cos_eq.mp (hsY 0) with hy0|hy0 <;>
      rcases Real.sin_eq_zero_iff_cos_eq.mp (hsY 1) with hy1|hy1 <;>
      constructor <;> linarith
    obtain ⟨k0,hk0⟩ := same_sign_even_difference _ _ (hsX 0) (hsY 0) hsign.1
    obtain ⟨k1,hk1⟩ := same_sign_even_difference _ _ (hsX 1) (hsY 1) hsign.2
    have hz := lattice_distance_zero X Y k0 k1 hk0 hk1
    linarith

theorem fixture_closedBasis :
    ∀ (a : ℝ) (q : I4Torus.SourceTorus 2 2),
      a ≤ SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) fixtureSample q →
      ∀ O : Set (I4Torus.SourceTorus 2 2), IsOpen O → q ∈ O →
        ∃ V : Set (I4Torus.SourceTorus 2 2), IsOpen V ∧ q ∈ V ∧ V ⊆ O ∧
          IsPathConnected (V ∩ {z | a ≤
            SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) fixtureSample z}) :=
  I4SourceActualTorusSuperlevelLocalBasis.actualSource_torus_closedSuperlevel_localPathConnectedBasis
    (by norm_num) fixtureSample fixture_morseDistinct

theorem fixture_torus_pullback (X : UniversalLaw.Spec.Lifetime.E 2) :
    SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) fixtureSample
      (fixtureProjection X) = actualField 2 2 fixtureSample X := by
  exact SourceActualFoldTorus.actualTorusField_pullback (by norm_num) fixtureSample (coordinates 2 X)

def selectedPoint : Fin 7 → UniversalLaw.Spec.Lifetime.E 2 :=
  ![fixturePoint 0 0,fixturePoint 1 0,fixturePoint 0 1,fixturePoint 1 1,
    fixturePoint (1/2) 0,fixturePoint 0 0,fixturePoint 0 0]

def selectedLevel : Fin 7 → ℝ := ![3,1,-1,-3,2,2,3]

theorem fixture_selected_closedBases (i : Fin 7)
    (O : Set (I4Torus.SourceTorus 2 2)) (hO : IsOpen O)
    (hq : fixtureProjection (selectedPoint i) ∈ O) :
    ∃ V : Set (I4Torus.SourceTorus 2 2), IsOpen V ∧
      fixtureProjection (selectedPoint i) ∈ V ∧ V ⊆ O ∧
      IsPathConnected (V ∩ {z | selectedLevel i ≤
        SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) fixtureSample z}) := by
  apply fixture_closedBasis (selectedLevel i) (fixtureProjection (selectedPoint i)) _ O hO hq
  rw [fixture_torus_pullback,fixture_actualField]
  have hp : Real.pi*(1/2:ℝ)=Real.pi/2 := by ring
  fin_cases i <;> norm_num [selectedPoint,selectedLevel,fixturePoint,hp]

def saddlePoint : I4Torus.SourceTorus 2 2 := fixtureProjection (fixturePoint 1 0)
def saddleHeight : ℝ := 1
def saddleBox : Set (UniversalLaw.Spec.Lifetime.E 2) :=
  {X | (1/2:ℝ)<X 0 ∧ X 0<3/2 ∧ (-1/4:ℝ)<X 1 ∧ X 1<1/4}
def saddleOpen : Set (I4Torus.SourceTorus 2 2) := fixtureProjection '' saddleBox
def saddleTorusField : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) fixtureSample

theorem fixtureProjection_continuous : Continuous fixtureProjection :=
  (SourceActualFoldTorus.torusProjection2L_continuous 2).comp (coordinates 2).continuous

theorem saddleBox_open : IsOpen saddleBox := by
  have h0 : Continuous (fun X : UniversalLaw.Spec.Lifetime.E 2 => X 0) :=
    (continuous_apply 0).comp (coordinates 2).continuous
  have h1 : Continuous (fun X : UniversalLaw.Spec.Lifetime.E 2 => X 1) :=
    (continuous_apply 1).comp (coordinates 2).continuous
  exact (isOpen_lt continuous_const h0).inter
    ((isOpen_lt h0 continuous_const).inter
      ((isOpen_lt continuous_const h1).inter (isOpen_lt h1 continuous_const)))

theorem saddleOpen_open : IsOpen saddleOpen := by
  apply ((SourceActualFoldTorus.torusProjection2L_open 2).comp
    (coordinates 2).toHomeomorph.isOpenMap) _ saddleBox_open

theorem saddlePoint_mem : saddlePoint ∈ saddleOpen := by
  refine ⟨fixturePoint 1 0,?_,rfl⟩
  norm_num [saddleBox,fixturePoint]

theorem saddle_closedMembership : (1:ℝ) ≤ saddleTorusField saddlePoint := by
  rw [saddleTorusField,saddlePoint,fixture_torus_pullback,fixture_actualField]
  norm_num [fixturePoint]

theorem saddle_closedBasis :
    ∃ V : Set (I4Torus.SourceTorus 2 2), IsOpen V ∧ saddlePoint ∈ V ∧ V ⊆ saddleOpen ∧
      IsPathConnected (V ∩ {z | (1:ℝ) ≤ saddleTorusField z}) :=
  fixture_closedBasis 1 saddlePoint saddle_closedMembership saddleOpen saddleOpen_open saddlePoint_mem

def strictBasisAtSaddle : Prop :=
  ∃ V : Set (I4Torus.SourceTorus 2 2), IsOpen V ∧ saddlePoint ∈ V ∧ V ⊆ saddleOpen ∧
    IsPathConnected (V ∩ {z | (1:ℝ) < saddleTorusField z})

/- Root CONTROL_PLAN_AMENDMENT_001 was personally read and ACKed before
this dependent proof text. The auxiliary observable is a scalar separator;
the sample defining saddleTorusField and the sole mutation are unchanged. -/
def separatorPolynomial : I4SourceFiniteTrig.TrigPoly :=
  [⟨1,Pi.single (0:Fin 2) 1,-Real.pi/2⟩]

def separatorSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 separatorPolynomial)
    (I4SourceSmoothConditional.zeroSample 2 2)

def separator : I4Torus.SourceTorus 2 2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (by norm_num : (2:ℝ) ≠ 0) separatorSample

theorem separator_continuous : Continuous separator :=
  SourceActualFoldTorus.actualTorusField_continuous (by norm_num) separatorSample

theorem separator_pullback (X : UniversalLaw.Spec.Lifetime.E 2) :
    separator (fixtureProjection X) = Real.sin (Real.pi*X 0) := by
  classical
  rw [separator,fixtureProjection,SourceActualFoldTorus.actualTorusField_pullback]
  have hs : HasSum (fun m => I4Source.modeCoefficient 2 2 m (coordinates 2 X) *
      I4SourceFiniteTrig.toSource 2 separatorPolynomial m)
      (I4SourceFinitePinKernel.finitePairing
        (fun m => I4Source.modeCoefficient 2 2 m (coordinates 2 X))
        (I4SourceFiniteTrig.toSource 2 separatorPolynomial)) := by
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    simp only [Finsupp.notMem_support_iff.mp hm,mul_zero]
  have he : smoothSourceField 2 2 separatorSample (coordinates 2 X) =
      I4SourceFinitePinKernel.finitePairing
        (fun m => I4Source.modeCoefficient 2 2 m (coordinates 2 X))
        (I4SourceFiniteTrig.toSource 2 separatorPolynomial) := by
    simpa [separatorSample,smoothSourceField,I4Source.sourceField,I4Foundation.scalarSeries,
      sampleInclusion,I4SourceFinitePinKernel.finiteShiftSample_val,
      I4SourceSmoothConditional.zeroSample] using hs.tsum_eq
  rw [he,I4SourceFiniteTrig.toSource_eval (by norm_num : (2:ℝ) ≠ 0)]
  have hp : I4Source.phase 2 2 (Pi.single (0:Fin 2) 1) (coordinates 2 X) = Real.pi*X 0 := by
    simp [I4Source.phase,I4Weights.sourceC,Fin.sum_univ_two]
  simp only [separatorPolynomial,I4SourceFiniteTrig.eval,List.map_cons,List.map_nil,
    List.sum_cons,List.sum_nil,I4SourceFiniteTrig.termEval,one_mul,add_zero,hp]
  rw [show Real.pi*X 0 + -Real.pi/2 = Real.pi*X 0-Real.pi/2 by ring,Real.cos_sub]
  simp

def saddleCurve (t : ℝ) : I4Torus.SourceTorus 2 2 := fixtureProjection (fixturePoint (1+t) 0)

theorem saddleCurve_continuous : Continuous saddleCurve := by
  apply fixtureProjection_continuous.comp
  apply (coordinates 2).symm.continuous.comp
  apply continuous_pi
  intro i
  fin_cases i <;> fun_prop

theorem saddleCurve_height (t : ℝ) : saddleTorusField (saddleCurve t) = 2-Real.cos (Real.pi*t) := by
  change saddleTorusField (fixtureProjection (fixturePoint (1+t) 0)) = _
  rw [saddleTorusField,fixture_torus_pullback,fixture_actualField]
  have hp : Real.pi*(1+t)=Real.pi+Real.pi*t := by ring
  simp [fixturePoint,hp,Real.cos_add] <;> ring

theorem saddleCurve_separator (t : ℝ) : separator (saddleCurve t) = -Real.sin (Real.pi*t) := by
  rw [saddleCurve,separator_pullback]
  have hp : Real.pi*(1+t)=Real.pi+Real.pi*t := by ring
  simp [fixturePoint,hp,Real.sin_add]

theorem saddleCurve_side_facts {delta : ℝ} (hdelta : 0 < delta) (hsmall : delta < 1/2) :
    (1:ℝ) < saddleTorusField (saddleCurve (-delta)) ∧
    (1:ℝ) < saddleTorusField (saddleCurve delta) ∧
    0 < separator (saddleCurve (-delta)) ∧ separator (saddleCurve delta) < 0 := by
  have hangle : 0 < Real.pi*delta := mul_pos Real.pi_pos hdelta
  have hanglepi : Real.pi*delta < Real.pi := by
    have hd1 : delta < 1 := by linarith
    simpa using mul_lt_mul_of_pos_left hd1 Real.pi_pos
  have hsin := Real.sin_pos_of_pos_of_lt_pi hangle hanglepi
  have hcos : Real.cos (Real.pi*delta) < 1 := by
    have hh := Real.cos_lt_cos_of_nonneg_of_le_pi (x:=(0:ℝ)) (y:=Real.pi*delta)
      (by norm_num) hanglepi.le hangle
    simpa using hh
  rw [saddleCurve_height,saddleCurve_height,saddleCurve_separator,saddleCurve_separator]
  simp only [mul_neg,Real.cos_neg,Real.sin_neg,neg_neg]
  exact ⟨by linarith,by linarith,hsin,neg_neg_of_pos hsin⟩

theorem strictTrace_twoSides :
    fixtureProjection (fixturePoint (3/4) 0) ∈ saddleOpen ∩ {z | (1:ℝ)<saddleTorusField z} ∧
    fixtureProjection (fixturePoint (5/4) 0) ∈ saddleOpen ∩ {z | (1:ℝ)<saddleTorusField z} := by
  have hh := saddleCurve_side_facts (delta:=(1/4:ℝ)) (by norm_num) (by norm_num)
  have hm : saddleCurve (-(1/4:ℝ)) = fixtureProjection (fixturePoint (3/4) 0) := by
    norm_num [saddleCurve]
  have hp : saddleCurve (1/4:ℝ) = fixtureProjection (fixturePoint (5/4) 0) := by
    norm_num [saddleCurve]
  constructor
  · refine ⟨⟨fixturePoint (3/4) 0,?_,rfl⟩,?_⟩
    · norm_num [saddleBox,fixturePoint]
    · simpa only [hm] using hh.1
  · refine ⟨⟨fixturePoint (5/4) 0,?_,rfl⟩,?_⟩
    · norm_num [saddleBox,fixturePoint]
    · simpa only [hp] using hh.2.1

theorem strictTrace_everyNeighborhood
    (V : Set (I4Torus.SourceTorus 2 2)) (hV : IsOpen V) (hq : saddlePoint ∈ V) :
    ∃ delta : ℝ, 0 < delta ∧ delta < 1/2 ∧
      saddleCurve (-delta) ∈ V ∧ saddleCurve delta ∈ V ∧
      (1:ℝ)<saddleTorusField (saddleCurve (-delta)) ∧
      (1:ℝ)<saddleTorusField (saddleCurve delta) ∧
      0<separator (saddleCurve (-delta)) ∧ separator (saddleCurve delta)<0 := by
  have hpre : IsOpen (saddleCurve ⁻¹' V) := hV.preimage saddleCurve_continuous
  have hzero : (0:ℝ) ∈ saddleCurve ⁻¹' V := by simpa [saddleCurve,saddlePoint] using hq
  obtain ⟨epsilon,hepsilon,hball⟩ := Metric.isOpen_iff.mp hpre 0 hzero
  let delta : ℝ := min (epsilon/2) (1/4)
  have hd : 0<delta := lt_min (by linarith) (by norm_num)
  have hde : delta<epsilon := lt_of_le_of_lt (min_le_left _ _) (by linarith)
  have hds : delta<(1/2:ℝ) := lt_of_le_of_lt (min_le_right _ _) (by norm_num)
  have hm : saddleCurve (-delta) ∈ V := by
    apply hball
    simpa [Real.dist_eq,abs_of_pos hd] using hde
  have hp : saddleCurve delta ∈ V := by
    apply hball
    simpa [Real.dist_eq,abs_of_pos hd] using hde
  obtain ⟨hmf,hpf,hmh,hph⟩ := saddleCurve_side_facts hd hds
  exact ⟨delta,hd,hds,hm,hp,hmf,hpf,hmh,hph⟩

theorem separator_zero_box (X : UniversalLaw.Spec.Lifetime.E 2) (hX : X ∈ saddleBox)
    (hzero : separator (fixtureProjection X)=0) : X 0=1 := by
  rw [separator_pullback] at hzero
  obtain ⟨n,hn⟩ := Real.sin_eq_zero_iff.mp hzero
  have hcoord : X 0=(n:ℝ) := by
    apply mul_left_cancel₀ Real.pi_ne_zero
    nlinarith [hn]
  have hn0 : (0:ℤ)<n := by
    exact_mod_cast (show (0:ℝ)<(n:ℝ) by rw [← hcoord]; linarith [hX.1])
  have hn2 : n<(2:ℤ) := by
    exact_mod_cast (show (n:ℝ)<(2:ℝ) by rw [← hcoord]; linarith [hX.2.1])
  have hn1 : n=1 := by omega
  simpa only [hn1,Int.cast_one] using hcoord

theorem not_strictBasisAtSaddle : ¬ strictBasisAtSaddle := by
  rintro ⟨V,hV,hq,hVO,hpc⟩
  obtain ⟨delta,_hd,_hds,hmV,hpV,hmF,hpF,hmH,hpH⟩ := strictTrace_everyNeighborhood V hV hq
  have hpre : IsPreconnected (V ∩ {z | (1:ℝ)<saddleTorusField z}) :=
    hpc.isConnected.isPreconnected
  have hinterval : (0:ℝ) ∈ Icc (separator (saddleCurve delta))
      (separator (saddleCurve (-delta))) := ⟨hpH.le,hmH.le⟩
  obtain ⟨z,hz,hzero⟩ := hpre.intermediate_value
    (a:=saddleCurve delta) (b:=saddleCurve (-delta)) ⟨hpV,hpF⟩ ⟨hmV,hmF⟩
    separator_continuous.continuousOn hinterval
  obtain ⟨X,hXB,hXz⟩ := hVO hz.1
  have hxzero : separator (fixtureProjection X)=0 := by rw [hXz]; exact hzero
  have hxone := separator_zero_box X hXB hxzero
  have hbound : saddleTorusField z ≤ 1 := by
    rw [← hXz,saddleTorusField,fixture_torus_pullback,fixture_actualField,hxone]
    have hh := Real.cos_le_one (Real.pi*X 1)
    norm_num only [mul_one,Real.cos_pi] at *
    linarith
  exact (not_lt_of_ge hbound) hz.2

end TorusSuperlevelLocalBasisControls
