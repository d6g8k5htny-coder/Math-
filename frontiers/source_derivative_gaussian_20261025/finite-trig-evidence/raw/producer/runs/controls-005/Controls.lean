import SourceFiniteTrig

noncomputable section
set_option autoImplicit false
open scoped BigOperators Matrix
open I4SourceFiniteTrig I4SourceFinitePinKernel I4Source I4SourceContact
open I4SmoothCarrier I4SourceSmoothConditional I4SourceDerivativeGaussian I4Lattice

open Lean in
macro "trigPrivate%" n:ident : term => do
  let pref := Lean.Name.str (Lean.Name.num `_private.SourceFiniteTrig 0) "I4SourceFiniteTrig"
  return Lean.mkIdent (pref ++ n.getId)

open Lean in
macro "unfold_trig_private " n:ident : tactic => do
  let pref := Lean.Name.str (Lean.Name.num `_private.SourceFiniteTrig 0) "I4SourceFiniteTrig"
  let id := Lean.mkIdent (pref ++ n.getId)
  `(tactic| unfold $id)

namespace FiniteTrigControls

private def axial : ↥(halfLattice 2) :=
  ⟨![1,0],⟨0,by decide,by intro j hj; omega⟩⟩

private theorem axial_ne_zero : (axial : Fin 2 → ℤ) ≠ 0 :=
  halfLattice_ne_zero 2 axial.property

/-- Empty and true constants work at zero and negative period as well. -/
theorem empty_constants (x : Fin 2 → ℝ) :
    eval 0 [] x = 0 ∧ eval 0 (constant 3) x = 3 ∧ eval (-2) (constant (-4)) x = -4 := by
  exact ⟨by simp [eval],eval_constant _ _ _,eval_constant _ _ _⟩

/-- Append and negative coefficient scaling retain their literal arithmetic. -/
theorem append_scale (L : ℝ) (p : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (constant 3 ++ scale (-2) p) x = 3-2*eval L p x := by
  rw [eval_append,eval_constant,eval_scale]
  ring

/-- Nonzero spatial shift uses x−z with no hidden sign change. -/
theorem nonzero_translation (p : TrigPoly) (x : Fin 2 → ℝ) :
    eval 2 (translate 2 ![1/3,-2/5] p) x = eval 2 p (x-![1/3,-2/5]) :=
  eval_translate _ _ _ _

/-- Both product coefficients are exactly one half for constant-one inputs. -/
theorem constant_product_coefficients :
    mul (constant 1) (constant 1) =
      [⟨1/2,0,0⟩,⟨1/2,0,0⟩] := by
  simp only [mul,constant,List.flatMap_cons,List.flatMap_nil,List.nil_append,List.append_nil]
  unfold_trig_private termProduct
  simp

/-- The full product normalization evaluates to one for every real period. -/
theorem constant_product (L : ℝ) (x : Fin 2 → ℝ) :
    eval L (mul (constant 1) (constant 1)) x = 1 := by
  rw [eval_mul,eval_constant]
  norm_num

/-- Sine is the same shifted-cosine representation at offset−π/2. -/
theorem sine_offset (L : ℝ) (k : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    eval L [⟨1,k,-Real.pi/2⟩] x = Real.sin (phase 2 L k x) := by
  simpa [eval,termEval,sub_eq_add_neg,neg_div] using
    Real.cos_sub_pi_div_two (phase 2 L k x)

/-- Canonical positive-frequency coefficients preserve arbitrary offsets and the
negative sine-channel coefficient. The map itself is total in L. -/
theorem positive_frequency_coefficients (L θ : ℝ) :
    toSource L [⟨1,axial,θ⟩] (some (axial,false)) =
      Real.cos θ / sourceModeAmplitude L (some (axial,false)) ∧
    toSource L [⟨1,axial,θ⟩] (some (axial,true)) =
      -Real.sin θ / sourceModeAmplitude L (some (axial,false)) := by
  classical
  constructor <;> simp only [toSource,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,add_zero,one_smul]
  all_goals
    unfold_trig_private atomSource
    simp [axial_ne_zero,axial.property]

/-- Negative frequencies use the positive representative and the positive
sine-channel coefficient; this separately checks the crucial sign. -/
theorem negative_frequency_coefficients (L θ : ℝ) :
    toSource L [⟨1,-(axial : Fin 2 → ℤ),θ⟩] (some (axial,false)) =
      Real.cos θ / sourceModeAmplitude L (some (axial,false)) ∧
    toSource L [⟨1,-(axial : Fin 2 → ℤ),θ⟩] (some (axial,true)) =
      Real.sin θ / sourceModeAmplitude L (some (axial,false)) := by
  classical
  have hn0 : -(axial : Fin 2 → ℤ) ≠ 0 := neg_ne_zero.mpr axial_ne_zero
  have hn : -(axial : Fin 2 → ℤ) ∉ halfLattice 2 := by
    intro hh
    exact (halfLattice_partition 2 axial_ne_zero).2 ⟨axial.property,hh⟩
  constructor <;> simp only [toSource,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,add_zero,one_smul]
  all_goals
    unfold_trig_private atomSource
    simp [hn0,hn]

/-- Zero frequency uses exactly the true none coefficient, including its offset. -/
theorem zero_frequency_none (L θ : ℝ) :
    toSource L [⟨2,0,θ⟩] none = 2*(Real.cos θ/sourceModeAmplitude L none) ∧
    toSource L [⟨2,0,θ⟩] (some (axial,false)) = 0 := by
  classical
  constructor <;> simp only [toSource,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,add_zero]
  all_goals
    unfold_trig_private atomSource
    simp

/-- The actual finite source field on the unchanged original carrier equals
finite evaluation globally, without a new source or amplitude definition. -/
theorem actual_field_equality {L : ℝ} (hL : L ≠ 0) (p : TrigPoly) :
    smoothSourceField 2 L (finiteShiftSample (toSource L p) (zeroSample 2 L)) = eval L p :=
  (trigPrivate% representedSample_field) hL p

/-- Arbitrary-order derivative pairing also composes with the actual finite product. -/
theorem arbitrary_order_product {L : ℝ} (hL : L ≠ 0) (p q : TrigPoly)
    (n : ℕ) (x : Fin 2 → ℝ) (u : Fin n → (Fin 2 → ℝ)) :
    finitePairing (derivativeCoefficient 2 L n x u) (toSource L (mul p q)) =
      iteratedFDeriv ℝ n (fun y => eval L p y * eval L q y) x u := by
  have he : eval L (mul p q) = fun y => eval L p y * eval L q y := funext (eval_mul L p q)
  simpa only [he] using toSource_derivative hL (mul p q) n x u

/-- Explicit order zero retains the literal finite evaluation. -/
theorem derivative_zero {L : ℝ} (hL : L ≠ 0) (p : TrigPoly) (x : Fin 2 → ℝ)
    (u : Fin 0 → (Fin 2 → ℝ)) :
    finitePairing (derivativeCoefficient 2 L 0 x u) (toSource L p) = eval L p x := by
  simpa only [iteratedFDeriv_zero_apply] using toSource_derivative hL p 0 x u

/-- Explicit first-order pairing is the full directional Frechet derivative. -/
theorem derivative_first {L : ℝ} (hL : L ≠ 0) (p : TrigPoly) (x v : Fin 2 → ℝ) :
    finitePairing (derivativeCoefficient 2 L 1 x ![v]) (toSource L p) =
      fderiv ℝ (eval L p) x v := by
  simpa only [iteratedFDeriv_one_apply,Matrix.cons_val_zero] using
    toSource_derivative hL p 1 x ![v]

/-- Explicit second-order pairing preserves both ordered directions. -/
theorem derivative_second {L : ℝ} (hL : L ≠ 0) (p : TrigPoly) (x v w : Fin 2 → ℝ) :
    finitePairing (derivativeCoefficient 2 L 2 x ![v,w]) (toSource L p) =
      fderiv ℝ (fderiv ℝ (eval L p)) x v w := by
  simpa only [iteratedFDeriv_two_apply,Matrix.cons_val_zero,Matrix.cons_val_one] using
    toSource_derivative hL p 2 x ![v,w]

private def oneMinusCos (k : Fin 2 → ℤ) : TrigPoly :=
  constant 1 ++ scale (-1) [⟨1,k,0⟩]

/-- A finite product used in later annihilator algebra, with no jet/rank claim. -/
theorem future_annihilator_product {L : ℝ} (hL : L ≠ 0) (x : Fin 2 → ℝ) :
    finitePairing (fun m => modeCoefficient 2 L m x)
      (toSource L (mul (oneMinusCos ![1,0]) (oneMinusCos ![0,1]))) =
      (1-Real.cos (phase 2 L ![1,0] x))*(1-Real.cos (phase 2 L ![0,1] x)) := by
  rw [toSource_eval hL,eval_mul]
  simp only [oneMinusCos,eval_append,eval_constant,eval_scale]
  simp [eval,termEval]
  ring

end FiniteTrigControls
