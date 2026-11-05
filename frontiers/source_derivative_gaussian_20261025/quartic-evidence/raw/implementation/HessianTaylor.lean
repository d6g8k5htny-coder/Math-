import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds
open I4SourceConditionalMajorant I4ActualQuarticTransfer
open I4SourcePinPreservingQuartic
open scoped BigOperators Topology
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

theorem hessianEntry_eq_derivativeComponent (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (x u w : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 2 f x ![u,w] =
      fderiv ℝ (fun y => fderiv ℝ f y w) x u := by
  have h := derivativeComponent_iteratedFDeriv f hf 1 x ![u] w
  have he : Fin.snoc (![u] : Fin 1 → (Fin 2 → ℝ)) w = ![u,w] := by
    ext i; fin_cases i <;> rfl
  simpa only [iteratedFDeriv_one_apply,he,Matrix.cons_val_zero] using h.symm

theorem hessianEntry_smooth (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (u w : Fin 2 → ℝ) :
    ContDiff ℝ (⊤ : ℕ∞) (fun x => iteratedFDeriv ℝ 2 f x ![u,w]) := by
  have he : (fun x => iteratedFDeriv ℝ 2 f x ![u,w]) =
      fun x => fderiv ℝ (fun y => fderiv ℝ f y w) x u :=
    funext (fun x => hessianEntry_eq_derivativeComponent f hf x u w)
  rw [he]
  exact derivativeComponent_smooth _ (derivativeComponent_smooth f hf w) u

theorem line_hessian_iteratedDeriv (f : (Fin 2 → ℝ) → ℝ)
    (hf : ContDiff ℝ (⊤ : ℕ∞) f) (k : ℕ) (v u w : Fin 2 → ℝ) (t : ℝ) :
    iteratedDeriv k (fun s => iteratedFDeriv ℝ 2 f (s • v) ![u,w]) t =
      iteratedFDeriv ℝ (k+2) f (t • v)
        (Fin.snoc (Fin.snoc (fun _ => v) u) w) := by
  have he : (fun s : ℝ => iteratedFDeriv ℝ 2 f (s • v) ![u,w]) =
      fun s : ℝ => fderiv ℝ (fun y => fderiv ℝ f y w) (s • v) u :=
    funext (fun s => hessianEntry_eq_derivativeComponent f hf (s • v) u w)
  rw [he,line_gradient_iteratedDeriv _ (derivativeComponent_smooth f hf w)]
  exact derivativeComponent_iteratedFDeriv f hf (k+1) _ _ w

theorem source_line_hessian_taylor {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (v u w : Fin 2 → ℝ) :
    |iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) v ![u,w] -
      (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![u,w] +
        iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![v,u,w] +
        iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![v,v,u,w]/2)| ≤
      sourceDerivativeMajorant L 5 ω * ‖v‖^3 * ‖u‖*‖w‖/6 := by
  let f := smoothSourceField 2 L ω
  have hf : ContDiff ℝ (⊤ : ℕ∞) f := smoothSourceField_smooth 2 hL ω
  let g := fun s : ℝ => iteratedFDeriv ℝ 2 f (s • v) ![u,w]
  have hg : ContDiff ℝ (⊤ : ℕ∞) g :=
    (hessianEntry_smooth f hf u w).comp (lineMap v).contDiff
  have hbd (s : ℝ) : |iteratedDeriv 3 g s| ≤
      sourceDerivativeMajorant L 5 ω * ‖v‖^3*‖u‖*‖w‖ := by
    rw [show g=(fun s => iteratedFDeriv ℝ 2 f (s • v) ![u,w]) from rfl,
      line_hessian_iteratedDeriv f hf]
    have h := source_derivative_abs_le hL ω 5 (s • v)
      (Fin.snoc (Fin.snoc (fun _ : Fin 3 => v) u) w)
    have he : (fun i : Fin 5 => ‖(Fin.snoc (Fin.snoc (fun _ : Fin 3 => v) u) w :
        Fin 5 → (Fin 2 → ℝ)) i‖) =
        Fin.snoc (Fin.snoc (fun _ : Fin 3 => ‖v‖) ‖u‖) ‖w‖ := by
      ext i; fin_cases i <;> rfl
    rw [he,Fin.prod_snoc,Fin.prod_snoc] at h
    simpa only [Finset.prod_const,Finset.card_univ,Fintype.card_fin,mul_assoc] using h
  have h := scalar_taylor_two_bound g hg _ hbd 1
  have hd1 := line_hessian_iteratedDeriv f hf 1 v u w 0
  have hd2 := line_hessian_iteratedDeriv f hf 2 v u w 0
  have he1 : Fin.snoc (Fin.snoc (fun _ : Fin 1 => v) u) w = ![v,u,w] := by
    ext i; fin_cases i <;> rfl
  have he2 : Fin.snoc (Fin.snoc (fun _ : Fin 2 => v) u) w = ![v,v,u,w] := by
    ext i; fin_cases i <;> rfl
  simp only [iteratedDeriv_one,zero_smul,he1,he2] at hd1 hd2
  simp only [show g 1=iteratedFDeriv ℝ 2 f v ![u,w] by simp [g],
    show g 0=iteratedFDeriv ℝ 2 f 0 ![u,w] by simp [g],
    show deriv g 0=iteratedFDeriv ℝ 3 f 0 ![v,u,w] from hd1,
    show iteratedDeriv 2 g 0=iteratedFDeriv ℝ 4 f 0 ![v,v,u,w] from hd2,
    one_mul,one_pow,mul_one,abs_one] at h
  exact h

end I4SourcePinPreservingQuartic
