import SourceCompactTargetMoments
import SourcePinPreservingQuartic
import AdaptiveFoldTransverseRidge

/-!
# Literal normalized fold chart for the actual fixed-axis source law

The original smooth carrier and centered x/y observation are retained. The
normalization includes the genuine varying cubic-gap coefficient `6*k`.
No framed conditional law or wider-rectangle conclusion is asserted here.
-/

noncomputable section

open I4SmoothCarrier I4SourceConfluentPins I4SourceRawPinConditioning
open I4SourceCompactTargetMoments I4ConfluentIntegralIdentities
open AdaptiveFoldTransverseRidge MeasureTheory
open scoped Interval Matrix

set_option autoImplicit false

/- The following coordinate-jet section is integrated once from the frozen
scratch helper by /root/actual_fold_chart_jets (OpenAI author-side lineage).
Frozen source b40252ce1d537414657a5a952fdb97975206d83afd6bd148de35d88fd394aa3b;
section 89ced04bcf5de1eaeccf73e7fdc22b0954a3059fa044159725176db8042112fc.
Its strict compilation is reused; no separate helper kernel was run. -/
noncomputable section

open scoped ContDiff
open I4SourceConfluentPins I4SourcePinPreservingQuartic

namespace I4ActualFoldChartJets

/-- Literal coordinate inclusion from the product/max norm to the Pi/sup norm. -/
def coordMap : (ℝ × ℝ) →L[ℝ] (Fin 2 → ℝ) :=
  ContinuousLinearMap.pi ![ContinuousLinearMap.fst ℝ ℝ ℝ,
    ContinuousLinearMap.snd ℝ ℝ ℝ]

@[simp] theorem coordMap_apply (p : ℝ × ℝ) : coordMap p = ![p.1, p.2] := by
  ext i
  fin_cases i <;> rfl

def chartMap (r : ℝ) : (ℝ × ℝ) →L[ℝ] (Fin 2 → ℝ) := r • coordMap

@[simp] theorem chartMap_apply (r : ℝ) (p : ℝ × ℝ) :
    chartMap r p = r • ![p.1, p.2] := by
  simp [chartMap]

def V (f : (Fin 2 → ℝ) → ℝ) (r k : ℝ) (p : ℝ × ℝ) : ℝ :=
  f (r • ![p.1, p.2]) / (6 * k * r ^ 3)

theorem V_contDiff (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (V f r k) := by
  change ContDiff ℝ (⊤ : ℕ∞) (fun p : ℝ × ℝ => f (r • ![p.1, p.2]) / (6 * k * r ^ 3))
  convert (hf.comp (chartMap r).contDiff).div_const (6 * k * r ^ 3) using 1
  ext p
  rw [Function.comp_apply, chartMap_apply]

/-- Every input is transported by the literal coordinate map; no norm conversion is used. -/
theorem pullback_jet (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (n : ℕ) (a r : ℝ)
    (p : ℝ × ℝ) (v : Fin n → ℝ × ℝ) :
    iteratedFDeriv ℝ n (fun q => a * f (r • ![q.1, q.2])) p v =
      a * r ^ n * iteratedFDeriv ℝ n f (r • ![p.1, p.2])
        (fun i => ![(v i).1, (v i).2]) := by
  have hc : ContDiff ℝ (n : ℕ∞) (f ∘ chartMap r) :=
    (hf.of_le (by simp)).comp (chartMap r).contDiff
  have h := congrArg (fun A => A v)
    (iteratedFDeriv_const_smul_apply' (a := a) (x := p) hc.contDiffAt)
  have hcomp := (chartMap r).iteratedFDeriv_comp_right hf p (i := n) (by simp)
  rw [hcomp] at h
  simpa only [smul_eq_mul, smul_apply,
    ContinuousMultilinearMap.compContinuousLinearMap_apply, Function.comp_def,
    chartMap_apply, ContinuousMultilinearMap.map_smul_univ, Finset.prod_const,
    Finset.card_univ, Fintype.card_fin, mul_assoc] using h

theorem Vx_eq (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0) (p : ℝ × ℝ) :
    AdaptiveFoldTransverseRidge.Vx (V f r k) p =
      fderiv ℝ f (r • ![p.1, p.2]) directionX / (6 * k * r ^ 2) := by
  have h := pullback_jet f hf 1 ((6 * k * r ^ 3)⁻¹) r p
    (fun _ => AdaptiveFoldTransverseRidge.ex)
  simp only [iteratedFDeriv_one_apply, pow_one] at h
  change fderiv ℝ (V f r k) p AdaptiveFoldTransverseRidge.ex = _
  have hV : V f r k = fun q => (6 * k * r ^ 3)⁻¹ * f (r • ![q.1, q.2]) := by
    ext q
    simp [V, div_eq_mul_inv, mul_comm]
  rw [hV, h]
  simp only [AdaptiveFoldTransverseRidge.ex, directionX]
  field_simp [hr]

theorem Vy_eq (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0) (p : ℝ × ℝ) :
    AdaptiveFoldTransverseRidge.Vy (V f r k) p =
      fderiv ℝ f (r • ![p.1, p.2]) directionY / (6 * k * r ^ 2) := by
  have h := pullback_jet f hf 1 ((6 * k * r ^ 3)⁻¹) r p
    (fun _ => AdaptiveFoldTransverseRidge.ey)
  simp only [iteratedFDeriv_one_apply, pow_one] at h
  change fderiv ℝ (V f r k) p AdaptiveFoldTransverseRidge.ey = _
  have hV : V f r k = fun q => (6 * k * r ^ 3)⁻¹ * f (r • ![q.1, q.2]) := by
    ext q
    simp [V, div_eq_mul_inv, mul_comm]
  rw [hV, h]
  simp only [AdaptiveFoldTransverseRidge.ey, directionY]
  field_simp [hr]

theorem axial_third_eq (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0) (p : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (AdaptiveFoldTransverseRidge.Vx (V f r k))) p
        AdaptiveFoldTransverseRidge.ex AdaptiveFoldTransverseRidge.ex =
      iteratedFDeriv ℝ 3 f (r • ![p.1, p.2])
        ![directionX, directionX, directionX] / (6 * k) := by
  have hX : AdaptiveFoldTransverseRidge.Vx (V f r k) =
      fun q => (6 * k * r ^ 2)⁻¹ * fderiv ℝ f (r • ![q.1, q.2]) directionX := by
    ext q
    rw [Vx_eq f hf r k hr q]
    exact div_eq_inv_mul _ _
  have h := pullback_jet _ (derivativeComponent_smooth f hf directionX) 2
    ((6 * k * r ^ 2)⁻¹) r p (fun _ => AdaptiveFoldTransverseRidge.ex)
  rw [derivativeComponent_iteratedFDeriv f hf] at h
  have hdirs : Fin.snoc (fun _ : Fin 2 => ![(AdaptiveFoldTransverseRidge.ex).1,
      (AdaptiveFoldTransverseRidge.ex).2]) directionX =
      ![directionX, directionX, directionX] := by
    ext i
    fin_cases i <;> rfl
  rw [hdirs] at h
  rw [hX, ← iteratedFDeriv_two_apply (𝕜 := ℝ) _ p
    (fun _ => AdaptiveFoldTransverseRidge.ex), h]
  field_simp [hr]

theorem transverse_center_eq (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) (hr : r ≠ 0) :
    fderiv ℝ (AdaptiveFoldTransverseRidge.Vy (V f r k)) (0, 0)
        AdaptiveFoldTransverseRidge.ey =
      iteratedFDeriv ℝ 2 f 0 ![directionY, directionY] / (6 * k * r) := by
  have hY : AdaptiveFoldTransverseRidge.Vy (V f r k) =
      fun q => (6 * k * r ^ 2)⁻¹ * fderiv ℝ f (r • ![q.1, q.2]) directionY := by
    ext q
    rw [Vy_eq f hf r k hr q]
    exact div_eq_inv_mul _ _
  have h := pullback_jet _ (derivativeComponent_smooth f hf directionY) 1
    ((6 * k * r ^ 2)⁻¹) r (0, 0) (fun _ => AdaptiveFoldTransverseRidge.ey)
  rw [derivativeComponent_iteratedFDeriv f hf] at h
  have hdirs : Fin.snoc (fun _ : Fin 1 => ![(AdaptiveFoldTransverseRidge.ey).1,
      (AdaptiveFoldTransverseRidge.ey).2]) directionY = ![directionY, directionY] := by
    ext i
    fin_cases i <;> rfl
  rw [hdirs] at h
  simp only [iteratedFDeriv_one_apply, pow_one] at h
  rw [hY, h]
  have hzero : r • (![0, 0] : Fin 2 → ℝ) = 0 := by
    ext i
    fin_cases i <;> simp
  rw [hzero]
  field_simp [hr]

theorem curve_deriv (G : ℝ × ℝ → ℝ)
    (hG : ContDiff ℝ (⊤ : ℕ∞) G) (u : ℝ) :
    deriv (fun t => G (t, 0)) u =
      AdaptiveFoldTransverseRidge.Vx G (u, 0) := by
  have h := (hG.differentiable (by simp) (u, 0)).hasFDerivAt
    |>.comp_hasDerivAt u ((hasDerivAt_id u).prodMk (hasDerivAt_const u (0 : ℝ)))
  simpa [Function.comp_def, AdaptiveFoldTransverseRidge.Vx,
    AdaptiveFoldTransverseRidge.partialX, AdaptiveFoldTransverseRidge.ex] using h.deriv

theorem curve_iteratedDeriv_three (G : ℝ × ℝ → ℝ)
    (hG : ContDiff ℝ (⊤ : ℕ∞) G) (u : ℝ) :
    iteratedDeriv 3 (fun t => G (t, 0)) u =
      fderiv ℝ (fderiv ℝ (AdaptiveFoldTransverseRidge.Vx G)) (u, 0)
        AdaptiveFoldTransverseRidge.ex AdaptiveFoldTransverseRidge.ex := by
  rw [show 3 = 2 + 1 from rfl, iteratedDeriv_succ']
  have hcurve : deriv (fun t => G (t, 0)) =
      fun t => AdaptiveFoldTransverseRidge.Vx G (t, 0) := by
    ext t
    exact curve_deriv G hG t
  rw [hcurve, iteratedDeriv_eq_iteratedFDeriv]
  let A : ℝ →L[ℝ] ℝ × ℝ :=
    (ContinuousLinearMap.id ℝ ℝ).prod (0 : ℝ →L[ℝ] ℝ)
  have hs : ContDiff ℝ (⊤ : ℕ∞) (AdaptiveFoldTransverseRidge.Vx G) :=
    (hG.fderiv_right (by simp)).clm_apply contDiff_const
  have h := A.iteratedFDeriv_comp_right hs u (i := 2) (by simp)
  have hh := congrArg (fun B => B (fun _ => (1 : ℝ))) h
  simpa [A, Function.comp_def, ContinuousMultilinearMap.compContinuousLinearMap_apply,
    iteratedFDeriv_two_apply, AdaptiveFoldTransverseRidge.ex] using hh

end I4ActualFoldChartJets

namespace I4SourceAdaptiveFoldChart

/-- Literal fixed-axis potential on the product/max-norm coordinate domain. -/
def actualFoldPotential {L : ℝ} (r k : ℝ) (ω : SmoothSample 2 L)
    (p : ℝ × ℝ) : ℝ :=
  smoothSourceField 2 L ω (r • ![p.1, p.2]) / (6*k*r^3)

/-- The exact deterministic data exported at every actual conditioned sample. -/
def NormalizedFoldData (V : ℝ × ℝ → ℝ) : Prop :=
  ContDiff ℝ 4 V ∧
  Vx V (-1/2, 0) = 0 ∧ Vx V (1/2, 0) = 0 ∧
  Vy V (-1/2, 0) = 0 ∧ Vy V (1/2, 0) = 0 ∧
  V (-1/2, 0) - V (1/2, 0) = 1/6 ∧
  (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), (3/2-6*u^2) *
    (fderiv ℝ (fderiv ℝ (Vx V)) (u, 0) ex ex)) = 2

/-- The product chart sends the literal left normalized endpoint to the raw one. -/
theorem chart_endpointM (r : ℝ) :
    r • (![-1/2, 0] : Fin 2 → ℝ) = endpointM r := by
  ext i
  fin_cases i <;> simp [endpointM]; ring

/-- The product chart sends the literal right normalized endpoint to the raw one. -/
theorem chart_endpointS (r : ℝ) :
    r • (![1/2, 0] : Fin 2 → ℝ) = endpointS r := by
  ext i
  fin_cases i <;> simp [endpointS]; ring

/-- The actual raw values give the exact normalized height difference. -/
theorem actualFoldPotential_gap {L r k b : ℝ} (ω : SmoothSample 2 L)
    (hr : 0 < r) (hk : 0 < k)
    (hp : rawPins L r ω = ![b,b-k*r^3,0,0,0,0]) :
    actualFoldPotential r k ω (-1/2,0) -
      actualFoldPotential r k ω (1/2,0) = 1/6 := by
  have hm := congrFun hp (0 : Fin 6)
  have hs := congrFun hp (1 : Fin 6)
  simp only [rawPins, Matrix.cons_val_zero, Matrix.cons_val_one] at hm hs
  simp only [actualFoldPotential, chart_endpointM, chart_endpointS, hm, hs]
  field_simp [hr.ne', hk.ne']
  ring

/-- The scalar Peano theorem at radius one gives the normalized actual axial jet. -/
theorem normalized_axial_peano (V : ℝ × ℝ → ℝ)
    (hV : ContDiff ℝ (⊤ : ℕ∞) V)
    (hxm : Vx V (-1/2,0) = 0) (hxs : Vx V (1/2,0) = 0)
    (hgap : V (-1/2,0) - V (1/2,0) = 1/6) :
    (∫ u in (-1/2 : ℝ)..(1/2 : ℝ), (3/2-6*u^2) *
      (fderiv ℝ (fderiv ℝ (Vx V)) (u,0) ex ex)) = 2 := by
  let f : ℝ → ℝ := fun u => V (u,0)
  have hfs : ContDiff ℝ (⊤ : ℕ∞) f :=
    hV.comp (contDiff_id.prodMk contDiff_const)
  have hp5 : pin5 f 1 = 2 := by
    simp only [pin5, f, I4ActualFoldChartJets.curve_deriv V hV,
      hxm, hxs]
    norm_num
    linarith
  have hi := pin5_integral f (hfs.of_le (by norm_num)) 1 one_ne_zero
  rw [hp5] at hi
  simp only [one_mul] at hi
  calc
    _ = ∫ u in (-1/2 : ℝ)..(1/2 : ℝ),
        6 * ((1/4-u^2) * iteratedDeriv 3 f u) := by
      apply intervalIntegral.integral_congr
      intro u _hu
      rw [show iteratedDeriv 3 f u = _ from
        I4ActualFoldChartJets.curve_iteratedDeriv_three V hV u]
      ring
    _ = 6 * ∫ u in (-1/2 : ℝ)..(1/2 : ℝ),
        (1/4-u^2) * iteratedDeriv 3 f u := by
      rw [intervalIntegral.integral_const_mul]
    _ = 2 := hi.symm

/-- Actual field smoothness, with the literal product/Pi pullback. -/
theorem actualFoldPotential_smooth {L : ℝ} (hL : L ≠ 0) (r k : ℝ)
    (ω : SmoothSample 2 L) :
    ContDiff ℝ (⊤ : ℕ∞) (actualFoldPotential r k ω) := by
  exact I4ActualFoldChartJets.V_contDiff (smoothSourceField 2 L ω)
    (smoothSourceField_smooth 2 hL ω) r k

/-- The literal actual potential is C4 on the full real-cover chart. -/
theorem actualFoldPotential_C4 {L : ℝ} (hL : L ≠ 0) (r k : ℝ)
    (ω : SmoothSample 2 L) : ContDiff ℝ 4 (actualFoldPotential r k ω) :=
  (actualFoldPotential_smooth hL r k ω).of_le (by norm_num)

/-- The first x derivative includes the exact r² and 6k normalization. -/
theorem actualFoldPotential_Vx {L r k : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (hr : r ≠ 0) (p : ℝ × ℝ) :
    Vx (actualFoldPotential r k ω) p =
      fderiv ℝ (smoothSourceField 2 L ω) (r • ![p.1,p.2]) directionX /
        (6*k*r^2) := by
  exact I4ActualFoldChartJets.Vx_eq (smoothSourceField 2 L ω)
    (smoothSourceField_smooth 2 hL ω) r k hr p

/-- The first y derivative includes the exact r² and 6k normalization. -/
theorem actualFoldPotential_Vy {L r k : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (hr : r ≠ 0) (p : ℝ × ℝ) :
    Vy (actualFoldPotential r k ω) p =
      fderiv ℝ (smoothSourceField 2 L ω) (r • ![p.1,p.2]) directionY /
        (6*k*r^2) := by
  exact I4ActualFoldChartJets.Vy_eq (smoothSourceField 2 L ω)
    (smoothSourceField_smooth 2 hL ω) r k hr p

/-- Ordered axial third jet, with the differentiated x direction last. -/
theorem actualFoldPotential_axial_third {L r k : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (hr : r ≠ 0) (p : ℝ × ℝ) :
    fderiv ℝ (fderiv ℝ (Vx (actualFoldPotential r k ω))) p ex ex =
      iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) (r • ![p.1,p.2])
        ![directionX,directionX,directionX] / (6*k) := by
  exact I4ActualFoldChartJets.axial_third_eq (smoothSourceField 2 L ω)
    (smoothSourceField_smooth 2 hL ω) r k hr p

/-- Actual center transverse curvature retains the physical radius denominator. -/
theorem actualFoldPotential_transverse_center {L r k : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (hr : r ≠ 0) :
    fderiv ℝ (Vy (actualFoldPotential r k ω)) (0,0) ey =
      iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0
        ![directionY,directionY] / (6*k*r) := by
  exact I4ActualFoldChartJets.transverse_center_eq (smoothSourceField 2 L ω)
    (smoothSourceField_smooth 2 hL ω) r k hr

/-- Literal raw pins imply all four normalized actual gradient pins. -/
theorem actualFoldPotential_gradient_pins {L r k b : ℝ} (hL : L ≠ 0)
    (ω : SmoothSample 2 L) (hr : 0 < r)
    (hp : rawPins L r ω = ![b,b-k*r^3,0,0,0,0]) :
    Vx (actualFoldPotential r k ω) (-1/2,0) = 0 ∧
    Vx (actualFoldPotential r k ω) (1/2,0) = 0 ∧
    Vy (actualFoldPotential r k ω) (-1/2,0) = 0 ∧
    Vy (actualFoldPotential r k ω) (1/2,0) = 0 := by
  have h2 := congrFun hp (2 : Fin 6)
  have h3 := congrFun hp (3 : Fin 6)
  have h4 := congrFun hp (4 : Fin 6)
  have h5 := congrFun hp (5 : Fin 6)
  simp [rawPins] at h2 h3 h4 h5
  simp only [actualFoldPotential_Vx hL ω hr.ne',
    actualFoldPotential_Vy hL ω hr.ne', chart_endpointM, chart_endpointS,
    h2, h3, h4, h5, zero_div, and_self]

/-- Internal deterministic adapter: no desired normalized pin or integral input. -/
theorem actualFoldPotential_normalized_data_of_rawPins {L r k b : ℝ}
    (hL : L ≠ 0) (ω : SmoothSample 2 L) (hr : 0 < r) (hk : 0 < k)
    (hp : rawPins L r ω = ![b,b-k*r^3,0,0,0,0]) :
    NormalizedFoldData (actualFoldPotential r k ω) := by
  obtain ⟨hxm,hxs,hym,hys⟩ := actualFoldPotential_gradient_pins hL ω hr hp
  have hg := actualFoldPotential_gap ω hr hk hp
  exact ⟨actualFoldPotential_C4 hL r k ω, hxm, hxs, hym, hys, hg,
    normalized_axial_peano _ (actualFoldPotential_smooth hL r k ω) hxm hxs hg⟩

/-- One interval, chosen before height and gap, works both pointwise on every
original posterior sample and almost surely under the actual gap law. -/
theorem sourceGapLaw_and_posterior_normalized_fold_data {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, 0 < k →
        (∀ η : SmoothSample 2 L,
          NormalizedFoldData (actualFoldPotential r k
            (rawPosteriorSample hL r ![b,b-k*r^3,0,0,0,0] η))) ∧
        (∀ᵐ ω ∂sourceGapLaw hL r b k,
          NormalizedFoldData (actualFoldPotential r k ω)) := by
  obtain ⟨_K,δ,_hK,hδ,hδ1,hbounds⟩ := sourceInverse_target_uniform_bounds hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro r hr hrδ b k hk
  have hG := (hbounds r hr hrδ).1
  constructor
  · intro η
    exact actualFoldPotential_normalized_data_of_rawPins hL _ hr hk
      (rawPosteriorSample_rawPins hL r hr.ne' hG _ η)
  · rw [sourceGapLaw_eq_rawPinKernel hL r b k hr.ne']
    have hm : MeasurableSet {ω : SmoothSample 2 L |
        rawPins L r ω = ![b,b-k*r^3,0,0,0,0]} :=
      measurableSet_eq_fun (rawPins_measurable hL r) measurable_const
    have hp : ∀ᵐ ω ∂rawPinKernel hL r ![b,b-k*r^3,0,0,0,0],
        rawPins L r ω = ![b,b-k*r^3,0,0,0,0] := by
      apply (ae_iff_measure_eq hm.nullMeasurableSet).mpr
      simpa using rawPinKernel_pin_fiber hL r hr.ne' hG ![b,b-k*r^3,0,0,0,0]
    filter_upwards [hp] with ω hω
    exact actualFoldPotential_normalized_data_of_rawPins hL ω hr hk hω

/-- Closed actual-law endpoint; no final invertibility, pin or integral premise. -/
theorem sourceGapLaw_normalized_fold_data {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, 0 < k →
        ∀ᵐ ω ∂sourceGapLaw hL r b k,
          NormalizedFoldData (actualFoldPotential r k ω) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_and_posterior_normalized_fold_data hL
  exact ⟨δ,hδ,hδ1,fun r hr hrδ b k hk => (h r hr hrδ b k hk).2⟩

/-- Every original prior sample has the same normalized data on the common interval. -/
theorem rawPosteriorSample_normalized_fold_data {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ r : ℝ, 0 < r → r < δ → ∀ b k : ℝ, 0 < k →
        ∀ η : SmoothSample 2 L,
          NormalizedFoldData (actualFoldPotential r k
            (rawPosteriorSample hL r ![b,b-k*r^3,0,0,0,0] η)) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_and_posterior_normalized_fold_data hL
  exact ⟨δ,hδ,hδ1,fun r hr hrδ b k hk => (h r hr hrδ b k hk).1⟩

end I4SourceAdaptiveFoldChart
