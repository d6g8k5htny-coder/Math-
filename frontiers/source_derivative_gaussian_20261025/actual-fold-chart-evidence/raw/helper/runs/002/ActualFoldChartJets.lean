import SourcePinPreservingQuartic
import AdaptiveFoldTransverseRidge

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
    chartMap r p = r • ![p.1, p.2] := rfl

def V (f : (Fin 2 → ℝ) → ℝ) (r k : ℝ) (p : ℝ × ℝ) : ℝ :=
  f (r • ![p.1, p.2]) / (6 * k * r ^ 3)

theorem V_contDiff (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k : ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (V f r k) :=
  (hf.comp (chartMap r).contDiff).div_const _

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
    (iteratedFDeriv_const_smul_apply' (a := a) hc.contDiffAt)
  have hcomp := (chartMap r).iteratedFDeriv_comp_right hf p (i := n) (by simp)
  simpa only [smul_eq_mul, hcomp, ContinuousMultilinearMap.smul_apply,
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
  field_simp
  ring

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
  field_simp
  ring

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
  field_simp
  ring

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
  field_simp
  ring

theorem curve_deriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k u : ℝ) :
    deriv (fun t => V f r k (t, 0)) u =
      AdaptiveFoldTransverseRidge.Vx (V f r k) (u, 0) := by
  have h := ((V_contDiff f hf r k).differentiable (by simp) (u, 0)).hasFDerivAt
    |>.comp_hasDerivAt u ((hasDerivAt_id u).prodMk (hasDerivAt_const u (0 : ℝ)))
  simpa [AdaptiveFoldTransverseRidge.Vx, AdaptiveFoldTransverseRidge.partialX,
    AdaptiveFoldTransverseRidge.ex] using h.deriv

theorem curve_iteratedDeriv_three (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (r k u : ℝ) :
    iteratedDeriv 3 (fun t => V f r k (t, 0)) u =
      fderiv ℝ (fderiv ℝ (AdaptiveFoldTransverseRidge.Vx (V f r k))) (u, 0)
        AdaptiveFoldTransverseRidge.ex AdaptiveFoldTransverseRidge.ex := by
  rw [show 3 = 2 + 1 from rfl, iteratedDeriv_succ']
  have hcurve : deriv (fun t => V f r k (t, 0)) =
      fun t => AdaptiveFoldTransverseRidge.Vx (V f r k) (t, 0) := by
    ext t
    exact curve_deriv f hf r k t
  rw [hcurve, iteratedDeriv_eq_iteratedFDeriv]
  let A : ℝ →L[ℝ] ℝ × ℝ :=
    (ContinuousLinearMap.id ℝ ℝ).prod (0 : ℝ →L[ℝ] ℝ)
  have hs : ContDiff ℝ (⊤ : ℕ∞) (AdaptiveFoldTransverseRidge.Vx (V f r k)) :=
    ((V_contDiff f hf r k).fderiv_right (by simp)).clm_apply contDiff_const
  have h := A.iteratedFDeriv_comp_right hs u (i := 2) (by simp)
  have hh := congrArg (fun B => B (fun _ => (1 : ℝ))) h
  simpa [A, Function.comp_def, ContinuousMultilinearMap.compContinuousLinearMap_apply,
    iteratedFDeriv_two_apply, AdaptiveFoldTransverseRidge.ex] using hh

end I4ActualFoldChartJets
