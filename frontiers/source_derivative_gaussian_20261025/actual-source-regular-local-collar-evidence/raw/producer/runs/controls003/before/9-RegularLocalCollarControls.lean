import SourceActualRegularLocalCollar
import SourceFiniteTrig
import SourceSmoothConditionalKernel

noncomputable section
set_option autoImplicit false
open Set
open scoped BigOperators
open UniversalLaw.Spec.Lifetime I4SmoothCarrier I4LifetimeField

namespace RegularLocalCollarControls

private abbrev P2 := Fin 2 → ℝ
private abbrev V2 := UniversalLaw.Spec.Lifetime.E 2
private abbrev T2 := I4Torus.SourceTorus 2 2
private def coords : V2 ≃L[ℝ] P2 := I4LifetimeField.coordinates 2
private def projection (X : V2) : T2 := I4Torus.torusProjection 2 2 (coords X)
private def terms : I4SourceFiniteTrig.TrigPoly :=
  [⟨1, ![(1 : ℤ), 0], 0⟩, ⟨2, ![(0 : ℤ), 1], 0⟩]
private def sample : SmoothSample 2 2 :=
  I4SourceFinitePinKernel.finiteShiftSample (I4SourceFiniteTrig.toSource 2 terms)
    (I4SourceSmoothConditional.zeroSample 2 2)
private def g : V2 → ℝ := I4LifetimeField.actualField 2 2 sample
private def F : T2 → ℝ :=
  SourceActualFoldTorus.actualTorusField (show (2 : ℝ) ≠ 0 by norm_num) sample
private def neighborhood (X : V2) : Set T2 :=
  projection '' Metric.ball X (1 / 8 : ℝ)
private def px : V2 := coords.symm ![(1 / 2 : ℝ), 0]
private def py : V2 := coords.symm ![0, (1 / 2 : ℝ)]
private def ps : V2 := coords.symm ![(-3 / 2 : ℝ), 0]
private def pm : V2 := coords.symm ![(0 : ℝ), 0]
private def b0 : V2 := coords.symm ![(1 : ℝ), 0]
private def b1 : V2 := coords.symm ![(0 : ℝ), 1]

private theorem literal_original_field (X : V2) :
    g X = Real.cos (Real.pi * (coords X) 0) +
      2 * Real.cos (Real.pi * (coords X) 1) := by
  classical
  let v := I4SourceFiniteTrig.toSource 2 terms
  have hv : sampleInclusion 2 2 sample = fun m => v m := by
    funext m
    simp [sample, I4SourceFinitePinKernel.finiteShiftSample_val,
      I4SourceSmoothConditional.zeroSample, sampleInclusion, v]
  have hs : HasSum (fun m : I4Source.SourceMode 2 =>
      I4Source.modeCoefficient 2 2 m (coords X) * v m)
      (I4SourceFiniteTrig.eval 2 terms (coords X)) := by
    rw [← I4SourceFiniteTrig.toSource_eval (show (2 : ℝ) ≠ 0 by norm_num)]
    change HasSum (fun m => I4Source.modeCoefficient 2 2 m (coords X) * v m)
      (v.sum (fun m a => I4Source.modeCoefficient 2 2 m (coords X) * a))
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    simp only [Finsupp.notMem_support_iff.mp hm, mul_zero]
  change I4Foundation.scalarSeries
    (fun m => I4Source.modeCoefficient 2 2 m (coords X)) (sampleInclusion 2 2 sample) = _
  rw [hv]
  calc
    I4Foundation.scalarSeries (fun m => I4Source.modeCoefficient 2 2 m (coords X))
      (fun m => v m) = I4SourceFiniteTrig.eval 2 terms (coords X) := hs.tsum_eq
    _ = Real.cos (Real.pi * (coords X) 0) +
      2 * Real.cos (Real.pi * (coords X) 1) := by
        simp [I4SourceFiniteTrig.eval, terms, I4SourceFiniteTrig.termEval,
          I4Source.phase, I4Weights.sourceC, Fin.sum_univ_two]

private theorem literal_pullback (X : V2) : F (projection X) = g X :=
  SourceActualFoldTorus.actualTorusField_pullback
    (show (2 : ℝ) ≠ 0 by norm_num) sample (coords X)

private theorem actual_derivative (X V : V2) :
    (fderiv ℝ g X) V =
      -Real.pi * Real.sin (Real.pi * (coords X) 0) * (coords V) 0 -
      2 * Real.pi * Real.sin (Real.pi * (coords X) 1) * (coords V) 1 := by
  let d0 : V2 →L[ℝ] ℝ :=
    (ContinuousLinearMap.proj (0 : Fin 2) : P2 →L[ℝ] ℝ).comp
      (coords : V2 →L[ℝ] P2)
  let d1 : V2 →L[ℝ] ℝ :=
    (ContinuousLinearMap.proj (1 : Fin 2) : P2 →L[ℝ] ℝ).comp
      (coords : V2 →L[ℝ] P2)
  have h0 : HasFDerivAt (fun Y : V2 => Real.pi * (coords Y) 0)
      (Real.pi • d0) X := d0.hasFDerivAt.const_mul Real.pi
  have h1 : HasFDerivAt (fun Y : V2 => Real.pi * (coords Y) 1)
      (Real.pi • d1) X := d1.hasFDerivAt.const_mul Real.pi
  have hformula : g = fun Y : V2 =>
      Real.cos (Real.pi * (coords Y) 0) + 2 * Real.cos (Real.pi * (coords Y) 1) :=
    funext literal_original_field
  have hg : HasFDerivAt g
      (-Real.sin (Real.pi * (coords X) 0) • Real.pi • d0 +
        (2 : ℝ) • -Real.sin (Real.pi * (coords X) 1) • Real.pi • d1) X := by
    rw [hformula]
    exact h0.cos.add (h1.cos.const_mul 2)
  rw [hg.fderiv]
  change -Real.sin (Real.pi * (coords X) 0) * (Real.pi * (coords V) 0) +
    2 * (-Real.sin (Real.pi * (coords X) 1) * (Real.pi * (coords V) 1)) = _
  ring

private theorem regular_x_data :
    g px = 2 ∧ (fderiv ℝ g px) b0 = -Real.pi ∧ (fderiv ℝ g px) b1 = 0 := by
  constructor
  · rw [literal_original_field]
    norm_num [px, mul_one_div]
  · constructor <;> rw [actual_derivative] <;> norm_num [px, b0, b1, mul_one_div]

private theorem regular_y_data :
    g py = 1 ∧ (fderiv ℝ g py) b0 = 0 ∧ (fderiv ℝ g py) b1 = -2 * Real.pi := by
  constructor
  · rw [literal_original_field]
    norm_num [py, mul_one_div]
  · constructor <;> rw [actual_derivative] <;> norm_num [py, b0, b1, mul_one_div]

private theorem seam_trig :
    Real.sin (Real.pi * (-3 / 2 : ℝ)) = 1 ∧
    Real.cos (Real.pi * (-3 / 2 : ℝ)) = 0 := by
  rw [show Real.pi * (-3 / 2 : ℝ) = Real.pi / 2 - 2 * Real.pi by ring,
    Real.sin_sub_two_pi, Real.cos_sub_two_pi]
  exact ⟨Real.sin_pi_div_two, Real.cos_pi_div_two⟩

private theorem seam_data :
    g ps = 2 ∧ (fderiv ℝ g ps) b0 = -Real.pi ∧ (fderiv ℝ g ps) b1 = 0 := by
  constructor
  · rw [literal_original_field]
    simp [ps, seam_trig.2]
  · constructor <;> rw [actual_derivative] <;> simp [ps, b0, b1, seam_trig.1]

private theorem seam_quotient : projection ps = projection px := by
  have hp := (AddCircle.coe_add_period (2 : ℝ) (-3 / 2 : ℝ)).symm
  norm_num at hp
  have hq : ((-3 / 2 : ℝ) : AddCircle (2 : ℝ)) =
      ((1 / 2 : ℝ) : AddCircle (2 : ℝ)) := by simpa [neg_div] using hp
  ext i
  fin_cases i
  · simpa [projection, ps, px, I4Torus.torusProjection] using hq
  · simp [projection, ps, px, I4Torus.torusProjection]

private theorem neighborhood_open (X : V2) : IsOpen (neighborhood X) := by
  have hop : IsOpenMap projection :=
    (SourceActualFoldTorus.torusProjection2L_open 2).comp coords.toHomeomorph.isOpenMap
  exact hop _ Metric.isOpen_ball

private theorem neighborhood_center (X : V2) : projection X ∈ neighborhood X :=
  ⟨X, Metric.mem_ball_self (by norm_num), rfl⟩

private def InversePoint (c a ε : ℝ)
    (φ : OpenPartialHomeomorph T2 P2) : Prop :=
  let u : P2 := ![a, ε]
  let z := φ.symm u
  u ∈ φ.target ∧ z ∈ φ.source ∧ φ z = u ∧ F z = c + ε ∧
    z ∈ φ.source ∩ {p | c + ε ≤ F p} ∧ z ∈ φ.source ∩ {p | F p = c + ε}

private theorem inverse_point (c ρ a ε : ℝ) (hρ : 0 < ρ)
    (ha : |a| < ρ) (hε : |ε| < ρ)
    (φ : OpenPartialHomeomorph T2 P2)
    (htarget : φ.target = Metric.ball (0 : P2) ρ)
    (hheight : ∀ z ∈ φ.source, F z = c + φ z 1) :
    InversePoint c a ε φ := by
  have ht : (![a, ε] : P2) ∈ φ.target := by
    rw [htarget, Metric.mem_ball, dist_zero_right]
    apply (pi_norm_lt_iff hρ).mpr
    intro i
    fin_cases i
    · simpa using ha
    · simpa using hε
  have hz := φ.map_target ht
  have hi := φ.right_inv ht
  have hv : F (φ.symm ![a, ε]) = c + ε := by
    rw [hheight _ hz, hi]
    rfl
  exact ⟨ht, hz, hi, hv, ⟨hz, hv.ge⟩, ⟨hz, hv⟩⟩

private def FixedCases (c ρ : ℝ) (φ : OpenPartialHomeomorph T2 P2) : Prop :=
  ∀ ε : ℝ, (ε = 0 ∨ ε = ρ / 2 ∨ ε = -ρ / 2) →
    InversePoint c 0 ε φ ∧ InversePoint c (-ρ / 2) ε φ ∧
      InversePoint c (ρ / 2) ε φ ∧
      φ.symm ![-ρ / 2, ε] ≠ φ.symm ![ρ / 2, ε] ∧
      JoinedIn (φ.source ∩ {z | F z = c + ε})
        (φ.symm ![-ρ / 2, ε]) (φ.symm ![ρ / 2, ε])

private theorem fixed_cases (c ρ : ℝ) (hρ : 0 < ρ)
    (φ : OpenPartialHomeomorph T2 P2)
    (htarget : φ.target = Metric.ball (0 : P2) ρ)
    (hheight : ∀ z ∈ φ.source, F z = c + φ z 1)
    (hall : ∀ ε : ℝ, |ε| < ρ →
      IsPathConnected (φ.source ∩ {z | c + ε ≤ F z}) ∧
      IsPathConnected (φ.source ∩ {z | F z = c + ε})) :
    FixedCases c ρ φ := by
  intro ε he
  have hh : |ρ / 2| < ρ := by
    rw [abs_of_pos (by positivity : 0 < ρ / 2)]
    linarith
  have heps : |ε| < ρ := by
    rcases he with rfl | rfl | rfl
    · simpa using hρ
    · exact hh
    · simpa only [neg_div, abs_neg] using hh
  have hneg : |-ρ / 2| < ρ := by simpa only [neg_div, abs_neg] using hh
  have hzero : |(0 : ℝ)| < ρ := by simpa using hρ
  have h0 := inverse_point c ρ 0 ε hρ hzero heps φ htarget hheight
  have hm := inverse_point c ρ (-ρ / 2) ε hρ hneg heps φ htarget hheight
  have hp := inverse_point c ρ (ρ / 2) ε hρ hh heps φ htarget hheight
  have hneq : φ.symm ![-ρ / 2, ε] ≠ φ.symm ![ρ / 2, ε] := by
    intro heq
    have he0 := congrArg (fun z => φ z 0) heq
    rw [hm.2.2.1, hp.2.2.1] at he0
    change -ρ / 2 = ρ / 2 at he0
    linarith
  exact ⟨h0, hm, hp, hneq, (hall ε heps).2.joinedIn
    _ hm.2.2.2.2.2 _ hp.2.2.2.2.2⟩

private def PositiveAt (X : V2) : Prop :=
  ∃ ρ : ℝ, 0 < ρ ∧ ∃ φ : OpenPartialHomeomorph T2 P2,
    projection X ∈ φ.source ∧ φ (projection X) = 0 ∧
    φ.source ⊆ neighborhood X ∧ φ.target = Metric.ball (0 : P2) ρ ∧
    (∀ z ∈ φ.source, F z = F (projection X) + φ z 1) ∧
    (∀ ε : ℝ, |ε| < ρ →
      IsPathConnected (φ.source ∩ {z | F (projection X) + ε ≤ F z}) ∧
      IsPathConnected (φ.source ∩ {z | F z = F (projection X) + ε})) ∧
    FixedCases (F (projection X)) ρ φ

private theorem positive_at (X : V2) (hregular : fderiv ℝ g X ≠ 0) : PositiveAt X := by
  obtain ⟨ρ, hρ, φ, hq, hc, hinside, ht, hh, hall⟩ :=
    I4SourceActualRegularLocalCollar.actualSource_quotient_regular_local_collar
      (show (0 : ℝ) < 2 by norm_num) sample X hregular
      (neighborhood X) (neighborhood_open X) (neighborhood_center X)
  exact ⟨ρ, hρ, φ, hq, hc, hinside, ht, hh, hall, fixed_cases _ ρ hρ φ ht hh hall⟩

private theorem regular_x_positive : PositiveAt px := by
  apply positive_at
  intro hz
  have he := regular_x_data.2.1
  rw [hz] at he
  simp only [zero_apply] at he
  linarith [Real.pi_pos]

private theorem regular_y_positive : PositiveAt py := by
  apply positive_at
  intro hz
  have he := regular_y_data.2.2
  rw [hz] at he
  simp only [zero_apply] at he
  linarith [Real.pi_pos]

private theorem seam_positive : PositiveAt ps := by
  apply positive_at
  intro hz
  have he := seam_data.2.1
  rw [hz] at he
  simp only [zero_apply] at he
  linarith [Real.pi_pos]

private theorem actual_maximum_value : g pm = 3 := by
  rw [literal_original_field]
  norm_num [pm]

private theorem actual_maximum_derivative : fderiv ℝ g pm = 0 := by
  ext V
  rw [actual_derivative]
  simp [pm]

private theorem actual_global_bound (z : T2) : F z ≤ 3 := by
  obtain ⟨u, hu⟩ := SourceActualFoldTorus.torusProjection2L_surjective 2 z
  have hz : projection (coords.symm u) = z := by simpa [projection] using hu
  rw [← hz, literal_pullback, literal_original_field]
  nlinarith [Real.cos_le_one (Real.pi * (coords (coords.symm u)) 0),
    Real.cos_le_one (Real.pi * (coords (coords.symm u)) 1)]

private theorem no_linear_chart_at_maximum (ρ : ℝ) (hρ : 0 < ρ)
    (φ : OpenPartialHomeomorph T2 P2)
    (_hsource : projection pm ∈ φ.source) (_hcenter : φ (projection pm) = 0)
    (_hinside : φ.source ⊆ neighborhood pm)
    (htarget : φ.target = Metric.ball (0 : P2) ρ)
    (hheight : ∀ z ∈ φ.source, F z = F (projection pm) + φ z 1) : False := by
  have hu : (![0, ρ / 2] : P2) ∈ φ.target := by
    rw [htarget, Metric.mem_ball, dist_zero_right]
    apply (pi_norm_lt_iff hρ).mpr
    intro i
    fin_cases i
    · simpa using hρ
    · have hh : |ρ / 2| < ρ := by
        rw [abs_of_pos (by positivity : 0 < ρ / 2)]
        linarith
      simpa using hh
  have hz := φ.map_target hu
  have hi := φ.right_inv hu
  have hv := hheight (φ.symm ![0, ρ / 2]) hz
  rw [literal_pullback, actual_maximum_value, hi] at hv
  change F (φ.symm ![0, ρ / 2]) = 3 + ρ / 2 at hv
  have hbound := actual_global_bound (φ.symm ![0, ρ / 2])
  linarith

def omittedNonzeroDerivativeMutation : Prop :=
  ∃ ρ : ℝ, 0 < ρ ∧ ∃ φ : OpenPartialHomeomorph T2 P2,
    projection pm ∈ φ.source ∧ φ (projection pm) = 0 ∧
    φ.source ⊆ neighborhood pm ∧ φ.target = Metric.ball (0 : P2) ρ ∧
    (∀ z ∈ φ.source, F z = F (projection pm) + φ z 1) ∧
    ∀ ε : ℝ, |ε| < ρ →
      IsPathConnected (φ.source ∩ {z | F (projection pm) + ε ≤ F z}) ∧
      IsPathConnected (φ.source ∩ {z | F z = F (projection pm) + ε})

theorem not_omittedNonzeroDerivativeMutation : ¬ omittedNonzeroDerivativeMutation := by
  rintro ⟨ρ, hρ, φ, hq, hc, hinside, ht, hh, _hall⟩
  exact no_linear_chart_at_maximum ρ hρ φ hq hc hinside ht hh

end RegularLocalCollarControls
