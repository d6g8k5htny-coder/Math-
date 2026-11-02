import SourceFinitePinKernel
import SourceContactCovariance
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

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

/- Integrated once from frozen /root/conditional_remote_jet_preflight atom conversion. Section SHA256 bb748238147162c2e68e6134361c9c4ad17610a2f2adb78d2510a08c786ddff3. No helper kernel/object import. -/
open I4Source I4Weights I4Lattice I4SourceContact I4SourceFinitePinKernel

private theorem atom_amplitude_pos {L : ℝ} (hL : L ≠ 0) (m : SourceMode 2) :
    0 < sourceModeAmplitude L m := by
  unfold sourceModeAmplitude
  cases m with
  | none => exact Real.sqrt_pos.mpr (one_div_pos.mpr (sourceZ_pos 2 hL))
  | some p =>
    apply Real.sqrt_pos.mpr
    apply div_pos _ (sourceZ_pos 2 hL)
    apply mul_pos (by norm_num)
    rw [sourceWeight_eq_physical]
    exact Real.exp_pos _

private theorem atom_pairing_single (a : SourceMode 2 → ℝ)
    (m : SourceMode 2) (c : ℝ) :
    finitePairing a (Finsupp.single m c) = a m * c := by
  classical
  simp [finitePairing, Finsupp.sum_single_index]

private theorem atom_pairing_add (a : SourceMode 2 → ℝ)
    (v w : SourceMode 2 →₀ ℝ) :
    finitePairing a (v+w) = finitePairing a v + finitePairing a w := by
  classical
  exact Finsupp.sum_add_index' (fun _ => mul_zero _) (fun _ _ _ => mul_add _ _ _)

private theorem atom_pairing_pair {L : ℝ} (hL : L ≠ 0)
    (k : ↥(halfLattice 2)) (c s : ℝ) (x : Fin 2 → ℝ) :
    finitePairing (fun m => modeCoefficient 2 L m x)
      (Finsupp.single (some (k,false))
        (c / sourceModeAmplitude L (some (k,false))) +
       Finsupp.single (some (k,true))
        (s / sourceModeAmplitude L (some (k,false)))) =
      c * Real.cos (phase 2 L k x) + s * Real.sin (phase 2 L k x) := by
  rw [atom_pairing_add, atom_pairing_single, atom_pairing_single]
  have hA := (atom_amplitude_pos hL (some (k,false))).ne'
  simp only [modeCoefficient, sourceModeAmplitude, Bool.false_eq_true,
    ite_false, ite_true] at hA ⊢
  field_simp

private theorem atom_phase_neg (L : ℝ) (k : Fin 2 → ℤ) (x : Fin 2 → ℝ) :
    phase 2 L (-k) x = -phase 2 L k x := by
  simp [phase, Int.cast_neg, mul_neg, neg_mul]

private def atomSource (L : ℝ) (k : Fin 2 → ℤ) (θ : ℝ) : SourceMode 2 →₀ ℝ := by
  classical
  exact if hk0 : k = 0 then
    Finsupp.single none (Real.cos θ / sourceModeAmplitude L none)
  else if hk : k ∈ halfLattice 2 then
    let j : ↥(halfLattice 2) := ⟨k,hk⟩
    Finsupp.single (some (j,false))
      (Real.cos θ / sourceModeAmplitude L (some (j,false))) +
    Finsupp.single (some (j,true))
      (-Real.sin θ / sourceModeAmplitude L (some (j,false)))
  else
    let j : ↥(halfLattice 2) :=
      ⟨-k, (halfLattice_partition 2 hk0).1.resolve_left hk⟩
    Finsupp.single (some (j,false))
      (Real.cos θ / sourceModeAmplitude L (some (j,false))) +
    Finsupp.single (some (j,true))
      (Real.sin θ / sourceModeAmplitude L (some (j,false)))

private theorem atomSource_pairing {L : ℝ} (hL : L ≠ 0)
    (k : Fin 2 → ℤ) (θ : ℝ) (x : Fin 2 → ℝ) :
    finitePairing (fun m => modeCoefficient 2 L m x) (atomSource L k θ) =
      Real.cos (phase 2 L k x + θ) := by
  classical
  by_cases hk0 : k = 0
  · subst k
    simp only [atomSource, dite_true]
    rw [atom_pairing_single]
    have hA := (atom_amplitude_pos hL none).ne'
    simp only [modeCoefficient, sourceModeAmplitude] at hA ⊢
    simp only [phase, Pi.zero_apply, Int.cast_zero, mul_zero, zero_mul, Finset.sum_const_zero,
      zero_add]
    field_simp
  · by_cases hk : k ∈ halfLattice 2
    · simp only [atomSource, dite_eq_right hk0, dite_eq_left hk]
      rw [atom_pairing_pair hL]
      rw [Real.cos_add]
      ring
    · simp only [atomSource, dite_eq_right hk0, dite_eq_right hk]
      rw [atom_pairing_pair hL]
      change Real.cos θ * Real.cos (phase 2 L (-k) x) +
        Real.sin θ * Real.sin (phase 2 L (-k) x) = _
      rw [atom_phase_neg, Real.cos_neg, Real.sin_neg, Real.cos_add]
      ring

private theorem pairing_eq_linearCombination {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    finitePairing a v = Finsupp.linearCombination ℝ a v := by
  classical
  simp only [finitePairing,Finsupp.linearCombination_apply,Finsupp.sum]
  apply Finset.sum_congr rfl
  intro m _hm
  simp only [smul_eq_mul]
  ring

/-- A total finite direction in the ORIGINAL source coefficient modes. -/
def toSource (L : ℝ) (p : TrigPoly) : SourceMode 2 →₀ ℝ :=
  (p.map (fun t => t.coeff • atomSource L t.frequency t.offset)).sum

/-- The exact finite coefficient pairing represents every shifted-cosine list,
including zero frequency, negative frequencies and arbitrary offsets. -/
theorem toSource_eval {L : ℝ} (hL : L ≠ 0) (p : TrigPoly) (x : Fin 2 → ℝ) :
    finitePairing (fun m => modeCoefficient 2 L m x) (toSource L p) = eval L p x := by
  induction p with
  | nil => simp [toSource,eval,finitePairing]
  | cons t p ih =>
    change finitePairing (fun m => modeCoefficient 2 L m x)
      (t.coeff • atomSource L t.frequency t.offset + toSource L p) =
        termEval L t x + eval L p x
    rw [pairing_eq_linearCombination,map_add,map_smul,
      ← pairing_eq_linearCombination,← pairing_eq_linearCombination,
      atomSource_pairing hL,ih]
    rfl

open I4Foundation I4SmoothCarrier I4SourceSmoothConditional I4SourceDerivativeGaussian

private theorem scalarSeries_finitePairing {ι : Type*} (a : ι → ℝ) (v : ι →₀ ℝ) :
    scalarSeries a v = finitePairing a v := by
  classical
  have h : HasSum (fun m => a m * v m) (finitePairing a v) := by
    apply hasSum_sum_of_ne_finset_zero
    intro m hm
    simp only [Finsupp.notMem_support_iff.mp hm,mul_zero]
  exact h.tsum_eq

private def representedSample (L : ℝ) (p : TrigPoly) : SmoothSample 2 L :=
  finiteShiftSample (toSource L p) (zeroSample 2 L)

private theorem representedSample_val (L : ℝ) (p : TrigPoly) (m : SourceMode 2) :
    (representedSample L p).val m = toSource L p m := by
  simp [representedSample,finiteShiftSample_val,zeroSample]

private theorem representedSample_field {L : ℝ} (hL : L ≠ 0) (p : TrigPoly) :
    smoothSourceField 2 L (representedSample L p) = eval L p := by
  funext x
  change scalarSeries (fun m => modeCoefficient 2 L m x)
      (sampleInclusion 2 L (representedSample L p)) = _
  have hval : sampleInclusion 2 L (representedSample L p) =
      fun m => toSource L p m := by
    funext m
    exact representedSample_val L p m
  rw [hval,scalarSeries_finitePairing,toSource_eval hL]

/-- All derivative orders and direction arrays are paired against the same
finite original direction, by the accepted literal source derivative series. -/
theorem toSource_derivative {L : ℝ} (hL : L ≠ 0) (p : TrigPoly)
    (n : ℕ) (x : Fin 2 → ℝ) (u : Fin n → (Fin 2 → ℝ)) :
    finitePairing (derivativeCoefficient 2 L n x u) (toSource L p) =
      iteratedFDeriv ℝ n (eval L p) x u := by
  have h := smoothSourceField_derivative_series 2 hL (representedSample L p) n x u
  rw [representedSample_field hL] at h
  have hval : sampleInclusion 2 L (representedSample L p) =
      fun m => toSource L p m := by
    funext m
    exact representedSample_val L p m
  rw [hval,scalarSeries_finitePairing] at h
  exact h.symm

end I4SourceFiniteTrig
