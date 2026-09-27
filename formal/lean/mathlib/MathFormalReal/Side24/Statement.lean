import Mathlib.Analysis.SpecialFunctions.Gamma.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Complex.Exponential
import Mathlib.Analysis.Real.Sqrt
import MathFormalCore.Side24.Arithmetic

/-!
# SIDE24 coefficient — real-number statement layer of `coefficients/side24_v1/PROOF.md`

Informal object: `SIDE24-COEFFICIENT-D23-20260924-v1` (author OpenAI / ChatGPT).
Formal object: `FORMAL-SIDE24-REAL-20260927-v1` (author Cursor cloud agent,
Anthropic Claude model family; AI-authored, author-side until a distinct
reviewer accepts the alignment ledger).

This file does three things, kept visibly separate:

1. **Definitions** of the standard objects the informal note uses (reference
   coefficient `cRef`, cone moments, enclosure predicates).
2. **Specifications** (`def … : Prop`, no proof): the theorem the note claims for
   the periodic coefficient `c_{d,24}`, and the two analytic inputs it rests on.
   The periodic coefficient itself (parent main#63 Eq. 15.2, a marked Kac-Rice
   integral) is not formalized; it enters as a parameter `c24 : ℕ → ℝ`. Anything
   not in the hypotheses of a theorem below is not claimed by this file.
3. **Theorems** (kernel-checked): the logical skeleton "reference enclosure +
   periodization bound ⇒ displayed enclosure", the `e^(288/125) > 10` real
   inequality behind Section 2, and the Section 3 eigenvalue fact.

Not proved here: the Stirling/Machin/atanh interval enclosure of `cRef` (Section 5,
`coefficient.py`), the Gaussian conditioning and cone integrals (Section 1), and the
covariance comparison (3)-(4) (Sections 3-4). They are the explicit hypotheses
`ReferenceEnclosure` and `PeriodizationBound` of `side24_of_inputs`.

Scientific effect: NONE.
-/

namespace MathFormalReal.Side24

open Real MathFormalCore.Side24

/-! ## 1. Definitions -/

/-- Section 1 cone moments `D_{d-1}`: `D_1 = 4/3` (`d = 2`), `D_2 = 29/6 - √6` (`d = 3`).
Other dimensions are outside the note's scope and are assigned `0` (never used). -/
noncomputable def coneMoment : ℕ → ℝ
  | 2 => 4 / 3
  | 3 => 29 / 6 - Real.sqrt 6
  | _ => 0

/-- Section 1, display (1): the nonperiodic reference coefficient
`c_{d,ref} = Γ(7/6) (3/2)^(1/3) D_{d-1} / (2 √3 π^(d-1) √π)`. -/
noncomputable def cRef (d : ℕ) : ℝ :=
  Real.Gamma (7 / 6) * (3 / 2 : ℝ) ^ ((1 : ℝ) / 3) * coneMoment d
    / (2 * Real.sqrt 3 * Real.pi ^ (d - 1) * Real.sqrt Real.pi)

/-- Open rational enclosure of a real number. -/
def Enclosed (c : ℝ) (lo hi : ℚ) : Prop := (lo : ℝ) < c ∧ c < hi

/-- Closed rational enclosure of a real number. -/
def EnclosedClosed (c : ℝ) (lo hi : ℚ) : Prop := (lo : ℝ) ≤ c ∧ c ≤ hi

/-- Section 4, display (4): `|c/cref - 1| < 10^(-106)`. -/
def RelativeBound (c cref : ℝ) : Prop := |c / cref - 1| < (relBound : ℝ)

/-! ## 2. Specifications (no proof in this file) -/

/-- SPECIFICATION. The claim of PROOF.md for the periodic coefficient `c24 d`
(`d = 2, 3`): both displayed 20-digit enclosures. -/
def Side24Theorem (c24 : ℕ → ℝ) : Prop :=
  Enclosed (c24 2) lower2 upper2 ∧ Enclosed (c24 3) lower3 upper3

/-- SPECIFICATION. Section 5 input: `coefficient.py`'s outward rational enclosure of the
reference coefficient is a correct enclosure of the real number `cRef d`. -/
def ReferenceEnclosure : Prop :=
  EnclosedClosed (cRef 2) refLo2 refHi2 ∧ EnclosedClosed (cRef 3) refLo3 refHi3

/-- SPECIFICATION. Sections 2-4 input, display (4), for both dimensions. -/
def PeriodizationBound (c24 : ℕ → ℝ) : Prop :=
  RelativeBound (c24 2) (cRef 2) ∧ RelativeBound (c24 3) (cRef 3)

/-! ## 3. Kernel-checked theorems -/

/-- Transfer lemma: a positive reference value enclosed in `[lo, hi]`, together with the
relative bound `|c/cref - 1| < r` for some `r < 1`, encloses `c` in
`(lo (1 - r), hi (1 + r))`. -/
theorem enclosure_transfer {c cref lo hi r : ℝ} (hpos : 0 < cref) (hr1 : r < 1)
    (hlo : lo ≤ cref) (hhi : cref ≤ hi) (hr : |c / cref - 1| < r) :
    lo * (1 - r) < c ∧ c < hi * (1 + r) := by
  obtain ⟨h1, h2⟩ := abs_sub_lt_iff.mp hr
  have hc1 : c < cref * (1 + r) := by
    have := (div_lt_iff₀ hpos).mp (by linarith : c / cref < 1 + r)
    linarith
  have hc2 : cref * (1 - r) < c := by
    have := (lt_div_iff₀ hpos).mp (by linarith : 1 - r < c / cref)
    linarith
  have hrpos : 0 < r := lt_of_le_of_lt (abs_nonneg _) hr
  constructor
  · calc lo * (1 - r) ≤ cref * (1 - r) := mul_le_mul_of_nonneg_right hlo (by linarith)
      _ < c := hc2
  · calc c < cref * (1 + r) := hc1
      _ ≤ hi * (1 + r) := mul_le_mul_of_nonneg_right hhi (by linarith)

/-- The relative bound `10^(-106)` is below one (needed by `enclosure_transfer`). -/
theorem relBound_lt_one : (relBound : ℝ) < 1 := by
  have h : (relBound : ℚ) < 1 := by decide +kernel
  exact_mod_cast h

/-- The logical skeleton of PROOF.md: the two analytic inputs imply the displayed
enclosures. Everything analytic is in the hypotheses; the conclusion is exactly the
note's displayed theorem for the parameter `c24`. -/
theorem side24_of_inputs (c24 : ℕ → ℝ)
    (href : ReferenceEnclosure) (hper : PeriodizationBound c24) : Side24Theorem c24 := by
  obtain ⟨⟨hlo2, hhi2⟩, ⟨hlo3, hhi3⟩⟩ := href
  obtain ⟨hrel2, hrel3⟩ := hper
  have ord := refIntervals_ordered
  have t2 := transfer_d2
  have t3 := transfer_d3
  have pos2 : (0 : ℝ) < cRef 2 := lt_of_lt_of_le (by exact_mod_cast ord.1) hlo2
  have pos3 : (0 : ℝ) < cRef 3 := lt_of_lt_of_le (by exact_mod_cast ord.2.2.1) hlo3
  have e2 := enclosure_transfer pos2 relBound_lt_one hlo2 hhi2 hrel2
  have e3 := enclosure_transfer pos3 relBound_lt_one hlo3 hhi3 hrel3
  refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩⟩
  · have : ((lower2 : ℚ) : ℝ) ≤ (refLo2 : ℝ) * (1 - (relBound : ℝ)) := by
      have h := t2.1
      have h' : ((lower2 : ℚ) : ℝ) ≤ ((refLo2 * (1 - relBound) : ℚ) : ℝ) := by exact_mod_cast h
      simpa using h'
    exact lt_of_le_of_lt this e2.1
  · have : (refHi2 : ℝ) * (1 + (relBound : ℝ)) ≤ ((upper2 : ℚ) : ℝ) := by
      have h := t2.2
      have h' : ((refHi2 * (1 + relBound) : ℚ) : ℝ) ≤ ((upper2 : ℚ) : ℝ) := by exact_mod_cast h
      simpa using h'
    exact lt_of_lt_of_le e2.2 this
  · have : ((lower3 : ℚ) : ℝ) ≤ (refLo3 : ℝ) * (1 - (relBound : ℝ)) := by
      have h := t3.1
      have h' : ((lower3 : ℚ) : ℝ) ≤ ((refLo3 * (1 - relBound) : ℚ) : ℝ) := by exact_mod_cast h
      simpa using h'
    exact lt_of_le_of_lt this e3.1
  · have : (refHi3 : ℝ) * (1 + (relBound : ℝ)) ≤ ((upper3 : ℚ) : ℝ) := by
      have h := t3.2
      have h' : ((refHi3 * (1 + relBound) : ℚ) : ℝ) ≤ ((upper3 : ℚ) : ℝ) := by exact_mod_cast h
      simpa using h'
    exact lt_of_lt_of_le e3.2 this

/-- Section 3: the smaller eigenvalue `8 - √58` of the odd block `[[1,-3],[-3,15]]`
exceeds `1/3`. -/
theorem oddBlock_minEigen_gt_third : (1 / 3 : ℝ) < 8 - Real.sqrt 58 := by
  have h : Real.sqrt 58 < 23 / 3 := by
    rw [Real.sqrt_lt' (by norm_num)]
    norm_num
  linarith

/-- Section 2: `e^(288/125) > 10`, via the degree-20 Taylor partial sum
(`Real.sum_le_exp_of_nonneg`) and exact rational evaluation. -/
theorem exp_288_125_gt_ten : (10 : ℝ) < Real.exp (288 / 125) := by
  have h := Real.sum_le_exp_of_nonneg (x := (288 / 125 : ℝ)) (by norm_num) 21
  have hsum : (10 : ℝ) < ∑ i ∈ Finset.range 21, (288 / 125 : ℝ) ^ i / (Nat.factorial i) := by
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, Nat.factorial]
    norm_num
  exact lt_of_lt_of_le hsum h

/-- Section 2: `e^(-288) < 10^(-125)`. -/
theorem exp_neg_288_lt : Real.exp (-288) < 1 / 10 ^ 125 := by
  have h1 : (10 : ℝ) ^ 125 < Real.exp 288 := by
    have : Real.exp 288 = Real.exp (288 / 125) ^ 125 := by
      rw [← Real.exp_nat_mul]; norm_num
    rw [this]
    exact pow_lt_pow_left₀ exp_288_125_gt_ten (by norm_num) (by norm_num)
  rw [Real.exp_neg]
  have hpos : (0 : ℝ) < 10 ^ 125 := by positivity
  rw [inv_eq_one_div]
  exact one_div_lt_one_div_of_lt hpos h1

/-- Section 1: the truncated cone moment `D_2 = 29/6 - √6` is strictly positive and strictly
below the untruncated value `29/6`. -/
theorem coneMoment_d3_bounds : 0 < coneMoment 3 ∧ coneMoment 3 < 29 / 6 := by
  have hs : Real.sqrt 6 < 29 / 6 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  have hp : 0 < Real.sqrt 6 := Real.sqrt_pos.mpr (by norm_num)
  simp only [coneMoment]
  constructor <;> linarith

/-- The reference coefficient is strictly positive in both dimensions of scope. -/
theorem cRef_pos (d : ℕ) (hd : d = 2 ∨ d = 3) : 0 < cRef d := by
  have hcm : 0 < coneMoment d := by
    rcases hd with rfl | rfl
    · simp [coneMoment]
    · exact coneMoment_d3_bounds.1
  unfold cRef
  have hg : 0 < Real.Gamma (7 / 6) := Real.Gamma_pos_of_pos (by norm_num)
  have hp : 0 < (3 / 2 : ℝ) ^ ((1 : ℝ) / 3) := Real.rpow_pos_of_pos (by norm_num) _
  have hpi : 0 < Real.pi := Real.pi_pos
  positivity

end MathFormalReal.Side24
