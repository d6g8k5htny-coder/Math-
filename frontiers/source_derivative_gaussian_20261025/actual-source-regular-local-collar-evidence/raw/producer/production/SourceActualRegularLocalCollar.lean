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

/-
Stage66 ONE private physical-adapter TEXT contribution.
Insert under the EXACT accepted common context in namespace
I4SourceActualRegularLocalCollar. No imports or namespace changes are needed.
This original has not been elaborated, executed, checked or hashed by its author.
-/

private theorem physical_adapter_linear_expansion
    (d : Point2 →L[ℝ] ℝ) (v : Point2) :
    d v = d ![1, 0] * v 0 + d ![0, 1] * v 1 := by
  have hv : v = v 0 • ![1, 0] + v 1 • ![0, 1] := by
    ext i
    fin_cases i <;> simp [smul_eq_mul]
  calc
    d v = d (v 0 • ![1, 0] + v 1 • ![0, 1]) := congrArg d hv
    _ = d ![1, 0] * v 0 + d ![0, 1] * v 1 := by
      simp only [map_add, map_smul, smul_eq_mul]
      ring

private def physical_adapter_triangularA
    (a b : ℝ) (ha : a ≠ 0) : Point2 ≃L[ℝ] Point2 where
  toFun v := ![v 1, a * v 0 + b * v 1]
  invFun w := ![(w 1 - b * w 0) / a, w 0]
  left_inv v := by
    ext i
    fin_cases i
    · change ((a * v 0 + b * v 1) - b * v 1) / a = v 0
      field_simp [ha]
      ring
    · rfl
  right_inv w := by
    ext i
    fin_cases i
    · rfl
    · change a * ((w 1 - b * w 0) / a) + b * w 0 = w 1
      field_simp [ha]
      ring
  map_add' v w := by
    ext i
    fin_cases i
    · rfl
    · change a * (v 0 + w 0) + b * (v 1 + w 1) =
        (a * v 0 + b * v 1) + (a * w 0 + b * w 1)
      ring
  map_smul' t v := by
    ext i
    fin_cases i
    · rfl
    · change a * (t * v 0) + b * (t * v 1) =
        t * (a * v 0 + b * v 1)
      ring
  continuous_toFun := by fun_prop
  continuous_invFun := by fun_prop

private def physical_adapter_triangularB
    (a b : ℝ) (hb : b ≠ 0) : Point2 ≃L[ℝ] Point2 where
  toFun v := ![v 0, a * v 0 + b * v 1]
  invFun w := ![w 0, (w 1 - a * w 0) / b]
  left_inv v := by
    ext i
    fin_cases i
    · rfl
    · change ((a * v 0 + b * v 1) - a * v 0) / b = v 1
      field_simp [hb]
      ring
  right_inv w := by
    ext i
    fin_cases i
    · rfl
    · change a * w 0 + b * ((w 1 - a * w 0) / b) = w 1
      field_simp [hb]
      ring
  map_add' v w := by
    ext i
    fin_cases i
    · rfl
    · change a * (v 0 + w 0) + b * (v 1 + w 1) =
        (a * v 0 + b * v 1) + (a * w 0 + b * w 1)
      ring
  map_smul' t v := by
    ext i
    fin_cases i
    · rfl
    · change a * (t * v 0) + b * (t * v 1) =
        t * (a * v 0 + b * v 1)
      ring
  continuous_toFun := by fun_prop
  continuous_invFun := by fun_prop

private theorem physical_adapter_choose_linear
    (d : Point2 →L[ℝ] ℝ) (hd : d ≠ 0) :
    ∃ j : Fin 2, ∃ T : Point2 ≃L[ℝ] Point2,
      (∀ v : Point2, T v 0 = v j) ∧
      (∀ v : Point2, T v 1 = d v) := by
  classical
  by_cases ha : d ![1, 0] ≠ 0
  · refine ⟨1, physical_adapter_triangularA (d ![1, 0]) (d ![0, 1]) ha,
      ?_, ?_⟩
    · intro v
      rfl
    · intro v
      change d ![1, 0] * v 0 + d ![0, 1] * v 1 = d v
      exact (physical_adapter_linear_expansion d v).symm
  · have ha0 : d ![1, 0] = 0 := not_not.mp ha
    have hb : d ![0, 1] ≠ 0 := by
      intro hb0
      apply hd
      ext v
      change d v = 0
      rw [physical_adapter_linear_expansion]
      simp [ha0, hb0]
    refine ⟨0, physical_adapter_triangularB (d ![1, 0]) (d ![0, 1]) hb,
      ?_, ?_⟩
    · intro v
      rfl
    · intro v
      change d ![1, 0] * v 0 + d ![0, 1] * v 1 = d v
      exact (physical_adapter_linear_expansion d v).symm

private theorem actual_physical_submersion_chart
    {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L) (X : E2)
    (hreg : fderiv ℝ (I4LifetimeField.actualField 2 L ω) X ≠ 0) :
    ∃ e : OpenPartialHomeomorph E2 Point2,
      X ∈ e.source ∧ e X = 0 ∧ (0 : Point2) ∈ e.target ∧
      ∀ Y ∈ e.source,
        I4LifetimeField.actualField 2 L ω Y =
          I4LifetimeField.actualField 2 L ω X + e Y 1 := by
  classical
  let x : Point2 := Q X
  let f : Point2 → ℝ := coordField L ω
  have hg : ContDiff ℝ 1 (I4LifetimeField.actualField 2 L ω) :=
    I4LifetimeField.actualField_smooth 2 hL ω 1
  have hf : ContDiff ℝ 1 f :=
    hg.comp (Q.symm : Point2 →L[ℝ] E2).contDiff
  let d : Point2 →L[ℝ] ℝ := fderiv ℝ f x
  have hdf : HasFDerivAt f d x :=
    (hf.differentiable_one x).hasFDerivAt
  have hfun : (fun Y : E2 => f (Q Y)) =
      I4LifetimeField.actualField 2 L ω := by
    funext Y
    simp [f, coordField, actualG]
  have hphysical : HasFDerivAt (I4LifetimeField.actualField 2 L ω)
      (d.comp (Q : E2 →L[ℝ] Point2)) X := by
    have hcomp : HasFDerivAt (fun Y : E2 => f (Q Y))
        (d.comp (Q : E2 →L[ℝ] Point2)) X :=
      hdf.comp X (Q : E2 →L[ℝ] Point2).hasFDerivAt
    simpa only [hfun] using hcomp
  have hd : d ≠ 0 := by
    intro hd0
    apply hreg
    calc
      fderiv ℝ (I4LifetimeField.actualField 2 L ω) X =
          d.comp (Q : E2 →L[ℝ] Point2) := hphysical.fderiv
      _ = 0 := by simp [hd0]
  obtain ⟨j, T, hT0, hT1⟩ := physical_adapter_choose_linear d hd
  let A : Point2 → Point2 := fun y => ![y j - x j, f y - f x]
  have hA_smooth : ContDiff ℝ 1 A := by
    apply contDiff_pi.2
    intro i
    fin_cases i
    · change ContDiff ℝ 1 (fun y : Point2 => y j - x j)
      exact (contDiff_apply ℝ ℝ j).sub contDiff_const
    · change ContDiff ℝ 1 (fun y : Point2 => f y - f x)
      exact hf.sub contDiff_const
  have hD0 :
      (ContinuousLinearMap.proj (0 : Fin 2) : Point2 →L[ℝ] ℝ).comp
          (T : Point2 →L[ℝ] Point2) =
        (ContinuousLinearMap.proj j : Point2 →L[ℝ] ℝ) := by
    ext v
    exact hT0 v
  have hD1 :
      (ContinuousLinearMap.proj (1 : Fin 2) : Point2 →L[ℝ] ℝ).comp
          (T : Point2 →L[ℝ] Point2) = d := by
    ext v
    exact hT1 v
  have hA_deriv : HasFDerivAt A (T : Point2 →L[ℝ] Point2) x := by
    apply hasFDerivAt_pi'.2
    intro i
    fin_cases i
    · change HasFDerivAt (fun y : Point2 => y j - x j)
        ((ContinuousLinearMap.proj (0 : Fin 2) : Point2 →L[ℝ] ℝ).comp
          (T : Point2 →L[ℝ] Point2)) x
      rw [hD0]
      exact (hasFDerivAt_apply j x).sub_const (x j)
    · change HasFDerivAt (fun y : Point2 => f y - f x)
        ((ContinuousLinearMap.proj (1 : Fin 2) : Point2 →L[ℝ] ℝ).comp
          (T : Point2 →L[ℝ] Point2)) x
      rw [hD1]
      exact hdf.sub_const (f x)
  let P : E2 → Point2 := fun Y => A (Q Y)
  let D : E2 ≃L[ℝ] Point2 := Q.trans T
  have hP_smooth : ContDiff ℝ 1 P :=
    hA_smooth.comp (Q : E2 →L[ℝ] Point2).contDiff
  have hD : (D : E2 →L[ℝ] Point2) =
      (T : Point2 →L[ℝ] Point2).comp (Q : E2 →L[ℝ] Point2) := by
    ext Y
    rfl
  have hP_deriv : HasFDerivAt P (D : E2 →L[ℝ] Point2) X := by
    rw [hD]
    exact hA_deriv.comp X (Q : E2 →L[ℝ] Point2).hasFDerivAt
  have hn : (1 : WithTop ℕ∞) ≠ 0 := by norm_num
  let e : OpenPartialHomeomorph E2 Point2 :=
    hP_smooth.contDiffAt.toOpenPartialHomeomorph P hP_deriv hn
  have hPX : P X = 0 := by
    ext i
    fin_cases i <;> simp [P, A, x]
  refine ⟨e, ?_, ?_, ?_, ?_⟩
  · exact hP_smooth.contDiffAt.mem_toOpenPartialHomeomorph_source hP_deriv hn
  · change P X = 0
    exact hPX
  · simpa only [hPX] using
      hP_smooth.contDiffAt.image_mem_toOpenPartialHomeomorph_target hP_deriv hn
  · intro Y _hY
    change I4LifetimeField.actualField 2 L ω Y =
      I4LifetimeField.actualField 2 L ω X + (f (Q Y) - f x)
    have hfY : f (Q Y) = I4LifetimeField.actualField 2 L ω Y := by
      simp [f, coordField, actualG]
    have hfX : f x = I4LifetimeField.actualField 2 L ω X := by
      simp [f, x, coordField, actualG]
    rw [hfY, hfX]
    ring

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
      have huc : ε ≤ u 1 := hu.2
      change c + ε ≤ F (φ.symm u)
      linarith [huc]
    · intro hz
      refine ⟨φ z, ⟨?_, ?_⟩, φ.left_inv hz.1⟩
      · rw [← htarget]
        exact φ.map_source hz.1
      · change ε ≤ φ z 1
        have hh := hheight z hz.1
        have hzc : c + ε ≤ F z := hz.2
        linarith [hzc]
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
      have huc : u 1 = ε := hu.2
      change F (φ.symm u) = c + ε
      linarith [huc]
    · intro hz
      refine ⟨φ z, ⟨?_, ?_⟩, φ.left_inv hz.1⟩
      · rw [← htarget]
        exact φ.map_source hz.1
      · change φ z 1 = ε
        have hh := hheight z hz.1
        have hzc : F z = c + ε := hz.2
        linarith [hzc]
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


theorem actualSource_quotient_regular_local_collar
    {L : ℝ} (hL : 0 < L)
    (ω : I4SmoothCarrier.SmoothSample 2 L)
    (X : UniversalLaw.Spec.Lifetime.E 2)
    (hreg : fderiv ℝ (I4LifetimeField.actualField 2 L ω) X ≠ 0) :
    ∀ O : Set (I4Torus.SourceTorus 2 L), IsOpen O →
      I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ O →
      ∃ ρ : ℝ, 0 < ρ ∧
        ∃ φ : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) (Fin 2 → ℝ),
          I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X) ∈ φ.source ∧
          φ (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) = 0 ∧
          φ.source ⊆ O ∧ φ.target = Metric.ball (0 : Fin 2 → ℝ) ρ ∧
          (∀ z ∈ φ.source,
            SourceActualFoldTorus.actualTorusField hL.ne' ω z =
              SourceActualFoldTorus.actualTorusField hL.ne' ω
                (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) + φ z 1) ∧
          ∀ ε : ℝ, |ε| < ρ →
            IsPathConnected (φ.source ∩ {z |
              SourceActualFoldTorus.actualTorusField hL.ne' ω
                (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) + ε ≤
                  SourceActualFoldTorus.actualTorusField hL.ne' ω z}) ∧
            IsPathConnected (φ.source ∩ {z |
              SourceActualFoldTorus.actualTorusField hL.ne' ω z =
                SourceActualFoldTorus.actualTorusField hL.ne' ω
                  (I4Torus.torusProjection 2 L (I4LifetimeField.coordinates 2 X)) + ε}) := by
  intro O hO hXO
  obtain ⟨e, hXe, heX, _h0e, hheight⟩ :=
    actual_physical_submersion_chart hL ω X hreg
  obtain ⟨ρ, hρ, φ, hq, hcenter, hinside, htarget, hfield⟩ :=
    quotient_chart_from_physical hL ω X e hXe heX hheight O hO hXO
  exact ⟨ρ, hρ, φ, hq, hcenter, hinside, htarget, hfield,
    same_chart_traces_pc (actualF hL ω) (actualF hL ω (cover L X)) ρ hρ φ
      htarget hfield⟩


private theorem fixture_derivative_apply (Y V : E2) :
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) Y) V =
      -Real.pi * Real.sin (Real.pi * (Q Y) 0) * (Q V) 0 -
        2 * Real.pi * Real.sin (Real.pi * (Q Y) 1) * (Q V) 1 := by
  let d0 : E2 →L[ℝ] ℝ := (ContinuousLinearMap.proj (0 : Fin 2) : Point2 →L[ℝ] ℝ).comp (Q : E2 →L[ℝ] Point2)
  let d1 : E2 →L[ℝ] ℝ := (ContinuousLinearMap.proj (1 : Fin 2) : Point2 →L[ℝ] ℝ).comp (Q : E2 →L[ℝ] Point2)
  have h0 : HasFDerivAt (fun Z : E2 => Real.pi * (Q Z) 0) (Real.pi • d0) Y :=
    d0.hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun Z : E2 => Real.pi * (Q Z) 1) (Real.pi • d1) Y :=
    d1.hasFDerivAt.const_mul Real.pi
  have hd := h0.cos.add (h1.cos.const_mul 2)
  have heq : I4LifetimeField.actualField 2 2 fixtureSample =
      fun Z : E2 => Real.cos (Real.pi * (Q Z) 0) +
        2 * Real.cos (Real.pi * (Q Z) 1) := funext fixture_actual_formula
  have hactual : HasFDerivAt (I4LifetimeField.actualField 2 2 fixtureSample)
      (-Real.sin (Real.pi * (Q Y) 0) • Real.pi • d0 +
        (2 : ℝ) • -Real.sin (Real.pi * (Q Y) 1) • Real.pi • d1) Y := by
    rw [heq]
    exact hd
  rw [hactual.fderiv]
  change -Real.sin (Real.pi * (Q Y) 0) * (Real.pi * (Q V) 0) +
    2 * (-Real.sin (Real.pi * (Q Y) 1) * (Real.pi * (Q V) 1)) = _
  ring

private def fixtureXx : E2 := Q.symm ![(1 / 2 : ℝ), 0]
private def fixtureXy : E2 := Q.symm ![0, (1 / 2 : ℝ)]
private def fixtureXseam : E2 := Q.symm ![(-3 / 2 : ℝ), 0]
private def fixtureXmax : E2 := Q.symm ![(0 : ℝ), 0]

private theorem fixture_regularX_value :
    I4LifetimeField.actualField 2 2 fixtureSample fixtureXx = 2 := by
  rw [fixture_actual_formula]
  norm_num [fixtureXx, mul_one_div]

private theorem fixture_regularY_value :
    I4LifetimeField.actualField 2 2 fixtureSample fixtureXy = 1 := by
  rw [fixture_actual_formula]
  norm_num [fixtureXy, mul_one_div]

private theorem fixture_regularX_derivative :
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) fixtureXx) physicalBasis0 =
      -Real.pi ∧
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) fixtureXx) physicalBasis1 = 0 := by
  constructor <;> rw [fixture_derivative_apply] <;>
    norm_num [fixtureXx, physicalBasis0, physicalBasis1, mul_one_div]

private theorem fixture_regularY_derivative :
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) fixtureXy) physicalBasis0 = 0 ∧
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) fixtureXy) physicalBasis1 =
      -2 * Real.pi := by
  constructor <;> rw [fixture_derivative_apply] <;>
    norm_num [fixtureXy, physicalBasis0, physicalBasis1, mul_one_div]

private theorem fixture_seam_phase :
    Real.sin (Real.pi * (-3 / 2 : ℝ)) = 1 ∧
    Real.cos (Real.pi * (-3 / 2 : ℝ)) = 0 := by
  have heq : Real.pi * (-3 / 2 : ℝ) = Real.pi / 2 - 2 * Real.pi := by ring
  rw [heq, Real.sin_sub_two_pi, Real.cos_sub_two_pi]
  exact ⟨Real.sin_pi_div_two, Real.cos_pi_div_two⟩

private theorem fixture_seam_value :
    I4LifetimeField.actualField 2 2 fixtureSample fixtureXseam = 2 := by
  rw [fixture_actual_formula]
  simp [fixtureXseam, fixture_seam_phase.2]

private theorem fixture_seam_derivative :
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) fixtureXseam) physicalBasis0 =
      -Real.pi ∧
    (fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) fixtureXseam) physicalBasis1 = 0 := by
  constructor <;> rw [fixture_derivative_apply] <;>
    simp [fixtureXseam, physicalBasis0, physicalBasis1, fixture_seam_phase.1]

private theorem fixture_seam_quotient : cover 2 fixtureXseam = cover 2 fixtureXx := by
  have hq : ((-3 / 2 : ℝ) : AddCircle (2 : ℝ)) =
      ((1 / 2 : ℝ) : AddCircle (2 : ℝ)) := by
    have hp := (AddCircle.coe_add_period (2 : ℝ) (-3 / 2 : ℝ)).symm
    norm_num at hp
    simpa [neg_div] using hp
  ext i
  fin_cases i
  · simpa [cover, fixtureXseam, fixtureXx, I4Torus.torusProjection] using hq
  · simp [cover, fixtureXseam, fixtureXx, I4Torus.torusProjection]

private theorem smallO_isOpen (L : ℝ) (X : E2) : IsOpen (smallO L X) := by
  have hp : IsOpenMap (cover L) :=
    (SourceActualFoldTorus.torusProjection2L_open L).comp Q.toHomeomorph.isOpenMap
  exact hp _ Metric.isOpen_ball

private theorem center_mem_smallO (L : ℝ) (X : E2) : cover L X ∈ smallO L X :=
  ⟨X, Metric.mem_ball_self (by norm_num), rfl⟩

private def FixedCutChecks {L : ℝ} (F : Torus2 L → ℝ) (c ρ : ℝ)
    (φ : OpenPartialHomeomorph (Torus2 L) Point2) : Prop :=
  ∀ ε : ℝ, (ε = 0 ∨ ε = ρ / 2 ∨ ε = -ρ / 2) →
    let z := φ.symm ![0, ε]
    let zm := φ.symm ![-ρ / 2, ε]
    let zp := φ.symm ![ρ / 2, ε]
    z ∈ φ.source ∧ zm ∈ φ.source ∧ zp ∈ φ.source ∧
    φ z = ![0, ε] ∧ φ zm = ![-ρ / 2, ε] ∧ φ zp = ![ρ / 2, ε] ∧
    F z = c + ε ∧ F zm = c + ε ∧ F zp = c + ε ∧
    z ∈ φ.source ∩ {p | c + ε ≤ F p} ∧
    z ∈ φ.source ∩ {p | F p = c + ε} ∧
    zm ∈ φ.source ∩ {p | F p = c + ε} ∧
    zp ∈ φ.source ∩ {p | F p = c + ε} ∧
    zm ≠ zp ∧ JoinedIn (φ.source ∩ {p | F p = c + ε}) zm zp

private theorem fixed_cut_checks {L : ℝ} (F : Torus2 L → ℝ) (c ρ : ℝ)
    (hρ : 0 < ρ) (φ : OpenPartialHomeomorph (Torus2 L) Point2)
    (htarget : φ.target = Metric.ball (0 : Point2) ρ)
    (hheight : ∀ z ∈ φ.source, F z = c + φ z 1)
    (hpc : ∀ ε : ℝ, |ε| < ρ →
      IsPathConnected (φ.source ∩ {z | c + ε ≤ F z}) ∧
      IsPathConnected (φ.source ∩ {z | F z = c + ε})) :
    FixedCutChecks F c ρ φ := by
  intro ε he
  have hhalf : |ρ / 2| < ρ := by
    rw [abs_of_pos (by positivity : 0 < ρ / 2)]
    linarith
  have hε : |ε| < ρ := by
    rcases he with rfl | rfl | rfl
    · simpa using hρ
    · exact hhalf
    · simpa only [neg_div, abs_neg] using hhalf
  have ht0 : (![0, ε] : Point2) ∈ φ.target := by
    rw [htarget]
    apply point_mem_ball hρ
    intro i
    fin_cases i
    · simpa using hρ
    · simpa using hε
  have htm : (![-ρ / 2, ε] : Point2) ∈ φ.target := by
    rw [htarget]
    apply point_mem_ball hρ
    intro i
    fin_cases i
    · simpa [neg_div, abs_neg] using hhalf
    · simpa using hε
  have htp : (![ρ / 2, ε] : Point2) ∈ φ.target := by
    rw [htarget]
    apply point_mem_ball hρ
    intro i
    fin_cases i
    · simpa using hhalf
    · simpa using hε
  have hs0 := φ.map_target ht0
  have hsm := φ.map_target htm
  have hsp := φ.map_target htp
  have hi0 := φ.right_inv ht0
  have him := φ.right_inv htm
  have hip := φ.right_inv htp
  have hv0 : F (φ.symm ![0, ε]) = c + ε := by
    rw [hheight _ hs0, hi0]
    rfl
  have hvm : F (φ.symm ![-ρ / 2, ε]) = c + ε := by
    rw [hheight _ hsm, him]
    rfl
  have hvp : F (φ.symm ![ρ / 2, ε]) = c + ε := by
    rw [hheight _ hsp, hip]
    rfl
  have hneq : φ.symm ![-ρ / 2, ε] ≠ φ.symm ![ρ / 2, ε] := by
    intro heq
    have he0 := congrArg (fun z => φ z 0) heq
    rw [him, hip] at he0
    change -ρ / 2 = ρ / 2 at he0
    linarith
  have hm : φ.symm ![-ρ / 2, ε] ∈ φ.source ∩ {p | F p = c + ε} :=
    ⟨hsm, hvm⟩
  have hp : φ.symm ![ρ / 2, ε] ∈ φ.source ∩ {p | F p = c + ε} :=
    ⟨hsp, hvp⟩
  exact ⟨hs0, hsm, hsp, hi0, him, hip, hv0, hvm, hvp,
    ⟨hs0, hv0.ge⟩, ⟨hs0, hv0⟩, hm, hp, hneq, (hpc ε hε).2.joinedIn _ hm _ hp⟩

private def FixtureOutput (X : E2) : Prop :=
  ∃ ρ : ℝ, 0 < ρ ∧ ∃ φ : OpenPartialHomeomorph (Torus2 2) Point2,
    cover 2 X ∈ φ.source ∧ φ (cover 2 X) = 0 ∧
    φ.source ⊆ smallO 2 X ∧ φ.target = Metric.ball (0 : Point2) ρ ∧
    (∀ z ∈ φ.source,
      actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample z =
        actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample (cover 2 X) + φ z 1) ∧
    (∀ ε : ℝ, |ε| < ρ →
      IsPathConnected (φ.source ∩ {z |
        actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample (cover 2 X) + ε ≤
          actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample z}) ∧
      IsPathConnected (φ.source ∩ {z |
        actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample z =
          actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample (cover 2 X) + ε})) ∧
    FixedCutChecks (actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample)
      (actualF (show (0 : ℝ) < 2 by norm_num) fixtureSample (cover 2 X)) ρ φ

private theorem fixture_output (X : E2)
    (hreg : fderiv ℝ (I4LifetimeField.actualField 2 2 fixtureSample) X ≠ 0) :
    FixtureOutput X := by
  obtain ⟨ρ, hρ, φ, hq, hc, hO, ht, hh, hp⟩ :=
    actualSource_quotient_regular_local_collar (show (0 : ℝ) < 2 by norm_num)
      fixtureSample X hreg (smallO 2 X) (smallO_isOpen 2 X) (center_mem_smallO 2 X)
  exact ⟨ρ, hρ, φ, hq, hc, hO, ht, hh, hp,
    fixed_cut_checks _ _ ρ hρ φ ht hh hp⟩

private theorem fixture_regularX_consumer : FixtureOutput fixtureXx := by
  apply fixture_output
  intro hz
  have he := fixture_regularX_derivative.1
  rw [hz] at he
  simp only [zero_apply] at he
  linarith [Real.pi_pos]

private theorem fixture_regularY_consumer : FixtureOutput fixtureXy := by
  apply fixture_output
  intro hz
  have he := fixture_regularY_derivative.2
  rw [hz] at he
  simp only [zero_apply] at he
  linarith [Real.pi_pos]

private theorem fixture_seam_consumer : FixtureOutput fixtureXseam := by
  apply fixture_output
  intro hz
  have he := fixture_seam_derivative.1
  rw [hz] at he
  simp only [zero_apply] at he
  linarith [Real.pi_pos]

end I4SourceActualRegularLocalCollar
