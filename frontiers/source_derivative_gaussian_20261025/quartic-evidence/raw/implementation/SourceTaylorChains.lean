import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds
open I4SourceConditionalMajorant I4SourceDerivativeGaussian I4Source I4Weights I4Foundation
open I4ActualQuarticTransfer I4SourcePinPreservingQuartic
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

def lineMap (v : Fin 2 → ℝ) : ℝ →L[ℝ] (Fin 2 → ℝ) :=
  (ContinuousLinearMap.id ℝ ℝ).smulRight v

theorem line_iteratedDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (v : Fin 2 → ℝ) (t : ℝ) :
    iteratedDeriv k (fun s => f (s • v)) t =
      iteratedFDeriv ℝ k f (t • v) (fun _ => v) := by
  rw [iteratedDeriv_eq_iteratedFDeriv]
  have h := (lineMap v).iteratedFDeriv_comp_right hf t (i := k) (by simp)
  have hh := congrArg (fun A => A (fun _ => (1 : ℝ))) h
  simpa [Function.comp_def,lineMap,ContinuousMultilinearMap.compContinuousLinearMap_apply] using hh

theorem derivativeComponent_smooth (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (u : Fin 2 → ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => fderiv ℝ f x u) :=
  (hf.fderiv_right (by simp)).clm_apply contDiff_const

theorem derivativeComponent_iteratedFDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (x : Fin 2 → ℝ)
    (v : Fin k → (Fin 2 → ℝ)) (u : Fin 2 → ℝ) :
    iteratedFDeriv ℝ k (fun y => fderiv ℝ f y u) x v =
      iteratedFDeriv ℝ (k+1) f x (Fin.snoc v u) := by
  have hdf : ContDiff ℝ (⊤ : ℕ∞) (fderiv ℝ f) := hf.fderiv_right (by simp)
  calc
    _ = iteratedFDeriv ℝ k (fderiv ℝ f) x v u :=
      iteratedFDeriv_clm_apply_const_apply hdf (by simp)
    _ = _ := by rw [iteratedFDeriv_succ_apply_right,Fin.init_snoc,Fin.snoc_last]

theorem line_gradient_iteratedDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (v u : Fin 2 → ℝ) (t : ℝ) :
    iteratedDeriv k (fun s => fderiv ℝ f (s • v) u) t =
      iteratedFDeriv ℝ (k+1) f (t • v) (Fin.snoc (fun _ => v) u) := by
  rw [line_iteratedDeriv _ (derivativeComponent_smooth f hf u)]
  exact derivativeComponent_iteratedFDeriv f hf k _ _ u

theorem source_derivative_abs_le {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) :
    |iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u| ≤
      sourceDerivativeMajorant L k ω * ∏ i, ‖u i‖ := by
  exact (ContinuousMultilinearMap.le_opNorm _ _).trans
    (mul_le_mul_of_nonneg_right (smoothSourceField_global_derivative_bound hL k ω x)
      (Finset.prod_nonneg (fun _ _ => norm_nonneg _)))

theorem source_line_gradient_taylor {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (v u : Fin 2 → ℝ) :
    |fderiv ℝ (smoothSourceField 2 L ω) v u -
      (fderiv ℝ (smoothSourceField 2 L ω) 0 u +
        iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![v,u] +
        iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![v,v,u]/2 +
        iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![v,v,v,u]/6)| ≤
      sourceDerivativeMajorant L 5 ω * ‖v‖^4 * ‖u‖/24 := by
  let f := smoothSourceField 2 L ω
  have hf : ContDiff ℝ (⊤ : ℕ∞) f := smoothSourceField_smooth 2 hL ω
  let g := fun s : ℝ => fderiv ℝ f (s • v) u
  have hg : ContDiff ℝ (⊤ : ℕ∞) g :=
    (derivativeComponent_smooth f hf u).comp (lineMap v).contDiff
  have hbd (s : ℝ) : |iteratedDeriv 4 g s| ≤ sourceDerivativeMajorant L 5 ω * ‖v‖^4*‖u‖ := by
    rw [show g=(fun s => fderiv ℝ f (s • v) u) from rfl,line_gradient_iteratedDeriv f hf]
    have h := source_derivative_abs_le hL ω 5 (s • v) (Fin.snoc (fun _ : Fin 4 => v) u)
    have he : (fun i : Fin 5 => ‖(Fin.snoc (fun _ : Fin 4 => v) u : Fin 5 → (Fin 2 → ℝ)) i‖) =
        Fin.snoc (fun _ : Fin 4 => ‖v‖) ‖u‖ := by ext i; fin_cases i <;> rfl
    rw [he,Fin.prod_snoc] at h
    simpa only [Finset.prod_const,Finset.card_univ,Fintype.card_fin,mul_assoc] using h
  have h := scalar_taylor_three_bound g hg _ hbd 1
  have hd1 := line_gradient_iteratedDeriv f hf 1 v u 0
  have hd2 := line_gradient_iteratedDeriv f hf 2 v u 0
  have hd3 := line_gradient_iteratedDeriv f hf 3 v u 0
  have h1 : Fin.snoc (fun _ : Fin 1 => v) u = ![v,u] := by ext i; fin_cases i <;> rfl
  have h2 : Fin.snoc (fun _ : Fin 2 => v) u = ![v,v,u] := by ext i; fin_cases i <;> rfl
  have h3 : Fin.snoc (fun _ : Fin 3 => v) u = ![v,v,v,u] := by ext i; fin_cases i <;> rfl
  simp only [iteratedDeriv_one,zero_smul,h1,h2,h3] at hd1 hd2 hd3
  simp only [show g 1=fderiv ℝ f v u by simp [g],show g 0=fderiv ℝ f 0 u by simp [g],
    show deriv g 0=iteratedFDeriv ℝ 2 f 0 ![v,u] from hd1,
    show iteratedDeriv 2 g 0=iteratedFDeriv ℝ 3 f 0 ![v,v,u] from hd2,
    show iteratedDeriv 3 g 0=iteratedFDeriv ℝ 4 f 0 ![v,v,v,u] from hd3,
    one_mul,one_pow,mul_one] at h
  exact h

theorem modeCoefficient_analytic_order (L : ℝ) (m : SourceMode 2) :
    ContDiff ℝ (⊤ : WithTop ℕ∞) (modeCoefficient 2 L m) := by
  cases m with
  | none =>
    change ContDiff ℝ (⊤ : WithTop ℕ∞) (fun _ : Fin 2 → ℝ => Real.sqrt (1/sourceZ 2 L))
    fun_prop
  | some p =>
    rcases p with ⟨k,b⟩
    change ContDiff ℝ (⊤ : WithTop ℕ∞) (fun x : Fin 2 → ℝ => Real.sqrt (2*sourceWeight 2 L k/sourceZ 2 L)*
      if b then Real.sin (phase 2 L k x) else Real.cos (phase 2 L k x))
    cases b <;> simp only [Bool.false_eq_true,ite_false,ite_true] <;> unfold phase <;> fun_prop

/-- Symmetry is proved mode by mode; analyticity of the whole random field
is not asserted or needed. -/
theorem source_derivative_comp_perm {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (k : ℕ) (x : Fin 2 → ℝ) (u : Fin k → (Fin 2 → ℝ)) (σ : Equiv.Perm (Fin k)) :
    iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x (u ∘ σ) =
      iteratedFDeriv ℝ k (smoothSourceField 2 L ω) x u := by
  rw [smoothSourceField_derivative_series 2 hL,smoothSourceField_derivative_series 2 hL]
  unfold scalarSeries
  apply tsum_congr
  intro m
  congr 1
  exact (modeCoefficient_analytic_order L m).contDiffAt.iteratedFDeriv_comp_perm u σ

end I4SourcePinPreservingQuartic
