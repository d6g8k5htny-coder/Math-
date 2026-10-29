import SourceFiniteTrig
noncomputable section
set_option autoImplicit false
open I4SourceFiniteTrig

/-- Sole mutation: both product terms omit the required factor1/2. -/
private def wrongProduct (p q : TrigPoly) : TrigPoly :=
  p.flatMap (fun t => q.flatMap (fun s =>
    [⟨t.coeff*s.coeff,t.frequency-s.frequency,t.offset-s.offset⟩,
     ⟨t.coeff*s.coeff,t.frequency+s.frequency,t.offset+s.offset⟩]))

private theorem wrong_constant_eval (L : ℝ) (x : Fin 2 → ℝ) :
    eval L (wrongProduct (constant 1) (constant 1)) x = 2 := by
  norm_num [wrongProduct,constant,eval,termEval,I4Source.phase]

private theorem wrong_constant_counterexample :
    eval 1 (wrongProduct (constant 1) (constant 1)) 0 ≠
      eval 1 (constant 1) 0 * eval 1 (constant 1) 0 := by
  rw [wrong_constant_eval,eval_constant]
  norm_num

/-- False specialized consequence of the mutated product-evaluation claim. -/
theorem false_omit_product_halves :
    eval 1 (wrongProduct (constant 1) (constant 1)) 0 =
      eval 1 (constant 1) 0 * eval 1 (constant 1) 0 := by
  have hcounterexample := wrong_constant_counterexample
  rw [wrong_constant_eval,eval_constant]
  norm_num
