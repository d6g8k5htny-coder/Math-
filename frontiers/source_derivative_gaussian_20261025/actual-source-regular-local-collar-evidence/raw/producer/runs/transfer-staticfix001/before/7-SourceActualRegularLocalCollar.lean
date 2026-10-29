import SourceActualFoldTorus
import SourceFiniteTrig
import SourceSmoothConditionalKernel
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Topology.OpenPartialHomeomorph.Constructions
import Mathlib.Topology.OpenPartialHomeomorph.IsImage
import Mathlib.Topology.Instances.AddCircle.Defs
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Calculus.FDeriv.Pi
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

noncomputable section
set_option autoImplicit false
open Set Filter
open scoped BigOperators
open UniversalLaw.Spec.Lifetime I4SmoothCarrier I4LifetimeField

namespace I4SourceActualRegularLocalCollar

private abbrev Point2 := Fin 2 → ℝ
private abbrev E2 := UniversalLaw.Spec.Lifetime.E 2
private abbrev Torus2 (L : ℝ) := I4Torus.SourceTorus 2 L
private def Q : E2 ≃L[ℝ] Point2 := I4LifetimeField.coordinates 2
private def cover (L : ℝ) (Y : E2) : Torus2 L :=
  I4Torus.torusProjection 2 L (Q Y)
private def actualG (L : ℝ) (ω : I4SmoothCarrier.SmoothSample 2 L) : E2 → ℝ :=
  I4LifetimeField.actualField 2 L ω
private def actualF {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L) : Torus2 L → ℝ :=
  SourceActualFoldTorus.actualTorusField hL.ne' ω
private def coordField (L : ℝ) (ω : I4SmoothCarrier.SmoothSample 2 L)
    (y : Point2) : ℝ := actualG L ω (Q.symm y)
private def physicalBasis0 : E2 := Q.symm ![1, 0]
private def physicalBasis1 : E2 := Q.symm ![0, 1]
private def smallO (L : ℝ) (X : E2) : Set (Torus2 L) :=
  cover L '' Metric.ball X (1 / 8 : ℝ)

private theorem actual_pullback {L : ℝ} (hL : 0 < L)
    (ω : SmoothSample 2 L) (Y : E2) :
    actualF hL ω (cover L Y) = actualG L ω Y := by
  exact SourceActualFoldTorus.actualTorusField_pullback hL.ne' ω (Q Y)

private theorem quotient_chart_from_physical {L : ℝ} (hL : 0 < L)
    (ω : SmoothSample 2 L) (X : E2)
    (e : OpenPartialHomeomorph E2 Point2)
    (hXe : X ∈ e.source) (heX : e X = 0)
    (hheight : ∀ Y ∈ e.source, actualG L ω Y = actualG L ω X + e Y 1)
    (O : Set (Torus2 L)) (hO : IsOpen O) (hXO : cover L X ∈ O) :
    ∃ ρ : ℝ, 0 < ρ ∧
      ∃ φ : OpenPartialHomeomorph (Torus2 L) Point2,
        cover L X ∈ φ.source ∧ φ (cover L X) = 0 ∧
        φ.source ⊆ O ∧ φ.target = Metric.ball (0 : Point2) ρ ∧
        ∀ z ∈ φ.source,
          actualF hL ω z = actualF hL ω (cover L X) + φ z 1 := by
  let : Fact (0 < L) := ⟨hL⟩
  let c : OpenPartialHomeomorph Point2 (Torus2 L) :=
    OpenPartialHomeomorph.pi (fun i : Fin 2 =>
      AddCircle.openPartialHomeomorphCoe L ((Q X) i - L / 2))
  let p : OpenPartialHomeomorph E2 (Torus2 L) :=
    Q.toHomeomorph.toOpenPartialHomeomorph.trans c
  have hp (Y : E2) : p Y = cover L Y := rfl
  have hXp : X ∈ p.source := by
    rw [OpenPartialHomeomorph.trans_source]
    refine ⟨Set.mem_univ _, ?_⟩
    change ∀ i ∈ (Set.univ : Set (Fin 2)),
      (Q X) i ∈ Set.Ioo ((Q X) i - L / 2) ((Q X) i - L / 2 + L)
    intro i _
    constructor <;> linarith
  let s : OpenPartialHomeomorph (Torus2 L) Point2 := p.symm.trans e
  have hqs : cover L X ∈ s.source := by
    rw [OpenPartialHomeomorph.trans_source]
    refine ⟨?_, ?_⟩
    · exact hp X ▸ p.map_source hXp
    · change p.symm (cover L X) ∈ e.source
      rw [← hp X, p.left_inv hXp]
      exact hXe
  have hscenter : s (cover L X) = 0 := by
    change e (p.symm (cover L X)) = 0
    rw [← hp X, p.left_inv hXp]
    exact heX
  have hsheight (z : Torus2 L) (hz : z ∈ s.source) :
      actualF hL ω z = actualF hL ω (cover L X) + s z 1 := by
    change z ∈ p.target ∧ p.symm z ∈ e.source at hz
    have hpz : cover L (p.symm z) = z := by
      rw [← hp]
      exact p.right_inv hz.1
    calc
      actualF hL ω z = actualF hL ω (cover L (p.symm z)) :=
        congrArg (actualF hL ω) hpz.symm
      _ = actualG L ω (p.symm z) := actual_pullback hL ω _
      _ = actualG L ω X + e (p.symm z) 1 := hheight _ hz.2
      _ = actualF hL ω (cover L X) + s z 1 := by
        rw [actual_pullback]
        rfl
  let r := s.restrOpen O hO
  have hqr : cover L X ∈ r.source := ⟨hqs, hXO⟩
  have hrcenter : r (cover L X) = 0 := hscenter
  have h0r : (0 : Point2) ∈ r.target := hrcenter ▸ r.map_source hqr
  rcases Metric.isOpen_iff.mp r.open_target 0 h0r with ⟨ρ, hρ, hball⟩
  let φ := (r.symm.restrOpen (Metric.ball (0 : Point2) ρ) Metric.isOpen_ball).symm
  refine ⟨ρ, hρ, φ, ?_, ?_, ?_, ?_, ?_⟩
  · change cover L X ∈ r.source ∧ r (cover L X) ∈ Metric.ball (0 : Point2) ρ
    exact ⟨hqr, hrcenter ▸ Metric.mem_ball_self hρ⟩
  · exact hrcenter
  · intro z hz
    change z ∈ r.source ∧ r z ∈ Metric.ball (0 : Point2) ρ at hz
    exact hz.1.2
  · change r.target ∩ Metric.ball (0 : Point2) ρ = Metric.ball (0 : Point2) ρ
    exact Set.inter_eq_right.mpr hball
  · intro z hz
    change z ∈ r.source ∧ r z ∈ Metric.ball (0 : Point2) ρ at hz
    exact hsheight z hz.1.1

private theorem point_mem_ball {ρ : ℝ} (hρ : 0 < ρ)
    (u : Point2) (hu : ∀ i, |u i| < ρ) : u ∈ Metric.ball (0 : Point2) ρ := by
  rw [Metric.mem_ball, dist_zero_right]
  apply (pi_norm_lt_iff hρ).mpr
  intro i
  simpa only [Real.norm_eq_abs] using hu i

private theorem pi_closed_upper_trace_pc
    (ρ ε : ℝ) (hρ : 0 < ρ) (hε : |ε| < ρ) :
    IsPathConnected ((Metric.ball (0 : Point2) ρ) ∩ {u | ε ≤ u 1}) := by
  have hc : Convex ℝ {u : Point2 | ε ≤ u 1} := by
    intro x hx y hy a b ha hb hab
    change ε ≤ a * x 1 + b * y 1
    change ε ≤ x 1 at hx
    change ε ≤ y 1 at hy
    calc
      ε = a * ε + b * ε := by rw [← add_mul, hab, one_mul]
      _ ≤ a * x 1 + b * y 1 :=
        add_le_add (mul_le_mul_of_nonneg_left hx ha)
          (mul_le_mul_of_nonneg_left hy hb)
  apply ((convex_ball (0 : Point2) ρ).inter hc).isPathConnected
  refine ⟨![0, ε], ?_, ?_⟩
  · apply point_mem_ball hρ
    intro i
    fin_cases i
    · simpa using hρ
    · simpa using hε
  · simp

private theorem pi_level_trace_pc
    (ρ ε : ℝ) (hρ : 0 < ρ) (hε : |ε| < ρ) :
    IsPathConnected ((Metric.ball (0 : Point2) ρ) ∩ {u | u 1 = ε}) := by
  have hc : Convex ℝ {u : Point2 | u 1 = ε} := by
    intro x hx y hy a b _ _ hab
    change a * x 1 + b * y 1 = ε
    change x 1 = ε at hx
    change y 1 = ε at hy
    rw [hx, hy, ← add_mul, hab, one_mul]
  apply ((convex_ball (0 : Point2) ρ).inter hc).isPathConnected
  refine ⟨![0, ε], ?_, ?_⟩
  · apply point_mem_ball hρ
    intro i
    fin_cases i
    · simpa using hρ
    · simpa using hε
  · simp


private theorem same_chart_traces_pc {L : ℝ}
    (F : Torus2 L → ℝ) (c ρ : ℝ) (hρ : 0 < ρ)
    (φ : OpenPartialHomeomorph (Torus2 L) Point2)
    (htarget : φ.target = Metric.ball (0 : Point2) ρ)
    (hheight : ∀ z ∈ φ.source, F z = c + φ z 1) :
    ∀ ε : ℝ, |ε| < ρ →
      IsPathConnected (φ.source ∩ {z | c + ε ≤ F z}) ∧
      IsPathConnected (φ.source ∩ {z | F z = c + ε}) := by
  intro ε hε
  have hupper_image :
      φ.symm '' (Metric.ball (0 : Point2) ρ ∩ {u | ε ≤ u 1}) =
        φ.source ∩ {z | c + ε ≤ F z} := by
    ext z
    constructor
    · rintro ⟨u, hu, rfl⟩
      have hut : u ∈ φ.target := htarget ▸ hu.1
      refine ⟨φ.map_target hut, ?_⟩
      have hh := hheight (φ.symm u) (φ.map_target hut)
      rw [φ.right_inv hut] at hh
      change ε ≤ u 1 at hu
      linarith [hu.2]
    · intro hz
      refine ⟨φ z, ⟨?_, ?_⟩, φ.left_inv hz.1⟩
      · rw [← htarget]
        exact φ.map_source hz.1
      · change ε ≤ φ z 1
        have hh := hheight z hz.1
        change c + ε ≤ F z at hz
        linarith [hz.2]
  have hlevel_image :
      φ.symm '' (Metric.ball (0 : Point2) ρ ∩ {u | u 1 = ε}) =
        φ.source ∩ {z | F z = c + ε} := by
    ext z
    constructor
    · rintro ⟨u, hu, rfl⟩
      have hut : u ∈ φ.target := htarget ▸ hu.1
      refine ⟨φ.map_target hut, ?_⟩
      have hh := hheight (φ.symm u) (φ.map_target hut)
      rw [φ.right_inv hut] at hh
      change u 1 = ε at hu
      linarith [hu.2]
    · intro hz
      refine ⟨φ z, ⟨?_, ?_⟩, φ.left_inv hz.1⟩
      · rw [← htarget]
        exact φ.map_source hz.1
      · change φ z 1 = ε
        have hh := hheight z hz.1
        change F z = c + ε at hz
        linarith [hz.2]
  have hcupper : ContinuousOn φ.symm
      (Metric.ball (0 : Point2) ρ ∩ {u | ε ≤ u 1}) :=
    φ.continuousOn_symm.mono (fun _ hu => htarget ▸ hu.1)
  have hclevel : ContinuousOn φ.symm
      (Metric.ball (0 : Point2) ρ ∩ {u | u 1 = ε}) :=
    φ.continuousOn_symm.mono (fun _ hu => htarget ▸ hu.1)
  constructor
  · rw [← hupper_image]
    exact (pi_closed_upper_trace_pc ρ ε hρ hε).image' hcupper
  · rw [← hlevel_image]
    exact (pi_level_trace_pc ρ ε hρ hε).image' hclevel

private def fixturePoly : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, ![(1 : ℤ), 0], 0⟩, ⟨2, ![(0 : ℤ), 1], 0⟩]

private def fixtureSample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample
    (I4SourceFiniteTrig.toSource 2 fixturePoly)
    (I4SourceSmoothConditional.zeroSample 2 2)

private theorem fixture_actual_formula (Y : E2) :
    I4LifetimeField.actualField 2 2 fixtureSample Y =
      Real.cos (Real.pi * (Q Y) 0) + 2 * Real.cos (Real.pi * (Q Y) 1) := by
  classical
  let v := I4SourceFiniteTrig.toSource 2 fixturePoly
  have hcoeff (m : I4Source.SourceMode 2) :
      I4SmoothCarrier.sampleInclusion 2 2 fixtureSample m = v m := by
    simp [fixtureSample, I4SourceFinitePinKernel.finiteShiftSample_val,
      I4SourceSmoothConditional.zeroSample, I4SmoothCarrier.sampleInclusion, v]
  have hs : HasSum (fun m : I4Source.SourceMode 2 =>
      I4Source.modeCoefficient 2 2 m (Q Y) * v m)
      (I4SourceFiniteTrig.eval 2 fixturePoly (Q Y)) := by
    rw [← I4SourceFiniteTrig.toSource_eval (show (2 : ℝ) ≠ 0 by norm_num)]
    change HasSum (fun m => I4Source.modeCoefficient 2 2 m (Q Y) * v m)
      (v.sum (fun m z => I4Source.modeCoefficient 2 2 m (Q Y) * z))
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    rw [Finsupp.notMem_support_iff.mp hm, mul_zero]
  change I4Foundation.scalarSeries
    (fun m => I4Source.modeCoefficient 2 2 m (Q Y))
    (I4SmoothCarrier.sampleInclusion 2 2 fixtureSample) = _
  have heq : I4SmoothCarrier.sampleInclusion 2 2 fixtureSample = fun m => v m :=
    funext hcoeff
  rw [heq]
  calc
    I4Foundation.scalarSeries (fun m => I4Source.modeCoefficient 2 2 m (Q Y))
        (fun m => v m) = I4SourceFiniteTrig.eval 2 fixturePoly (Q Y) := hs.tsum_eq
    _ = Real.cos (Real.pi * (Q Y) 0) + 2 * Real.cos (Real.pi * (Q Y) 1) := by
      simp [I4SourceFiniteTrig.eval, fixturePoly, I4SourceFiniteTrig.termEval,
        I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two]

end I4SourceActualRegularLocalCollar
