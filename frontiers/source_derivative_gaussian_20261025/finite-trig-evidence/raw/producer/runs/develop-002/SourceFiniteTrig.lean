import SourceFinitePinKernel
import SourceContactCovariance

/-! Finite shifted-cosine lists in the unchanged original source coefficients.
The finite algebra allows every real period. Source conversion correctness uses
only the original nonzero-period hypothesis. No remote jet rank is asserted. -/

noncomputable section
set_option autoImplicit false
open scoped BigOperators
open I4Source I4SourceFinitePinKernel

namespace I4SourceFiniteTrig

/-- A shifted real cosine with its literal integer spatial frequency. -/
structure TrigTerm where
  coeff : ℝ
  frequency : Fin 2 → ℤ
  offset : ℝ

abbrev TrigPoly := List TrigTerm

def termEval (L : ℝ) (t : TrigTerm) (x : Fin 2 → ℝ) : ℝ :=
  t.coeff * Real.cos (phase 2 L t.frequency x + t.offset)

def eval (L : ℝ) (p : TrigPoly) (x : Fin 2 → ℝ) : ℝ :=
  (p.map (fun t => termEval L t x)).sum

def constant (a : ℝ) : TrigPoly := [⟨a,0,0⟩]

def scale (a : ℝ) (p : TrigPoly) : TrigPoly :=
  p.map (fun t => { t with coeff := a*t.coeff })

/-- Translation means x ↦ f(x−z). -/
def translate (L : ℝ) (z : Fin 2 → ℝ) (p : TrigPoly) : TrigPoly :=
  p.map (fun t => { t with offset := t.offset - phase 2 L t.frequency z })

private def termProduct (t s : TrigTerm) : TrigPoly :=
  [⟨t.coeff*s.coeff/2,t.frequency-s.frequency,t.offset-s.offset⟩,
   ⟨t.coeff*s.coeff/2,t.frequency+s.frequency,t.offset+s.offset⟩]

def mul (p q : TrigPoly) : TrigPoly :=
  p.flatMap (fun t => q.flatMap (termProduct t))

private theorem phase_spatial_sub (L : ℝ) (k : Fin 2 → ℤ) (x z : Fin 2 → ℝ) :
    phase 2 L k (x-z) = phase 2 L k x - phase 2 L k z := by
  simp only [phase,Pi.sub_apply,mul_sub,Finset.sum_sub_distrib]

private theorem phase_frequency_sub (L : ℝ) (k l : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    phase 2 L (k-l) x = phase 2 L k x - phase 2 L l x := by
  simp only [phase,Pi.sub_apply,Int.cast_sub,mul_sub,sub_mul,Finset.sum_sub_distrib]

private theorem phase_frequency_add (L : ℝ) (k l : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    phase 2 L (k+l) x = phase 2 L k x + phase 2 L l x := by
  simp only [phase,Pi.add_apply,Int.cast_add,mul_add,add_mul,Finset.sum_add_distrib]

private theorem eval_cons (L : ℝ) (t : TrigTerm) (p : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (t::p) x = termEval L t x + eval L p x := by
  simp [eval]

/-- Constants include the true zero frequency. -/
theorem eval_constant (L a : ℝ) (x : Fin 2 → ℝ) : eval L (constant a) x = a := by
  simp [eval,constant,termEval,phase]

/-- List append is finite polynomial addition, with duplicates permitted. -/
theorem eval_append (L : ℝ) (p q : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (p++q) x = eval L p x + eval L q x := by
  simp [eval,List.map_append,List.sum_append]

/-- Coefficient scaling gives exact pointwise scalar multiplication. -/
theorem eval_scale (L a : ℝ) (p : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (scale a p) x = a * eval L p x := by
  induction p with
  | nil => simp [scale,eval]
  | cons t p ih =>
    change termEval L { t with coeff := a*t.coeff } x + eval L (scale a p) x =
      a * (termEval L t x + eval L p x)
    rw [ih]
    simp only [termEval]
    ring

/-- The offset convention transports evaluation by exactly x−z. -/
theorem eval_translate (L : ℝ) (z : Fin 2 → ℝ) (p : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (translate L z p) x = eval L p (x-z) := by
  induction p with
  | nil => simp [translate,eval]
  | cons t p ih =>
    change termEval L { t with offset := t.offset-phase 2 L t.frequency z } x +
        eval L (translate L z p) x = termEval L t (x-z) + eval L p (x-z)
    rw [ih]
    congr 1
    simp only [termEval,phase_spatial_sub]
    congr 2
    ring

private theorem eval_termProduct (L : ℝ) (t s : TrigTerm) (x : Fin 2 → ℝ) :
    eval L (termProduct t s) x = termEval L t x * termEval L s x := by
  simp only [termProduct,eval,List.map_cons,List.map_nil,List.sum_cons,List.sum_nil,
    add_zero,termEval,phase_frequency_sub,phase_frequency_add]
  have h := Real.two_mul_cos_mul_cos (phase 2 L t.frequency x+t.offset)
    (phase 2 L s.frequency x+s.offset)
  rw [show phase 2 L t.frequency x - phase 2 L s.frequency x + (t.offset-s.offset) =
      (phase 2 L t.frequency x+t.offset) - (phase 2 L s.frequency x+s.offset) by ring,
    show phase 2 L t.frequency x + phase 2 L s.frequency x + (t.offset+s.offset) =
      (phase 2 L t.frequency x+t.offset) + (phase 2 L s.frequency x+s.offset) by ring]
  rw [← mul_add,← h]
  ring

private theorem eval_termProducts (L : ℝ) (t : TrigTerm) (q : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (q.flatMap (termProduct t)) x = termEval L t x * eval L q x := by
  induction q with
  | nil => simp [eval]
  | cons s q ih =>
    rw [List.flatMap_cons,eval_append,eval_termProduct,ih,eval_cons]
    ring

/-- The two half-weighted cosine products preserve multiplication exactly. -/
theorem eval_mul (L : ℝ) (p q : TrigPoly) (x : Fin 2 → ℝ) :
    eval L (mul p q) x = eval L p x * eval L q x := by
  induction p with
  | nil => simp [mul,eval]
  | cons t p ih =>
    change eval L ((q.flatMap (termProduct t)) ++ mul p q) x = _
    rw [eval_append,eval_termProducts,ih,eval_cons]
    ring

end I4SourceFiniteTrig
