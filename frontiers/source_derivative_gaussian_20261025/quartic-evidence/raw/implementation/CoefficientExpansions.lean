import SourcePinPreservingQuartic

noncomputable section
open I4SmoothCarrier I4SourceConfluentPins I4SourcePinCurvatureBounds
open I4SourcePinPreservingQuartic
open scoped BigOperators
set_option autoImplicit false

namespace I4SourcePinPreservingQuartic

private theorem plane_decompose (p : Fin 2 → ℝ) :
    p = p 0 • directionX + p 1 • directionY := by
  ext i
  fin_cases i <;> simp [directionX,directionY]

private theorem cml_head {n : ℕ}
    (T : ContinuousMultilinearMap ℝ (fun _ : Fin (n+1) => Fin 2 → ℝ) ℝ)
    (p : Fin 2 → ℝ) (v : Fin n → (Fin 2 → ℝ)) :
    T (Fin.cons p v) = p 0 * T (Fin.cons directionX v) +
      p 1 * T (Fin.cons directionY v) := by
  rw [← ContinuousMultilinearMap.curryLeft_apply,plane_decompose p,map_add,map_smul,map_smul]
  simp [ContinuousMultilinearMap.curryLeft_apply,smul_eq_mul,directionX,directionY]

private theorem cml_pp {n : ℕ}
    (T : ContinuousMultilinearMap ℝ (fun _ : Fin (n+2) => Fin 2 → ℝ) ℝ)
    (p : Fin 2 → ℝ) (v : Fin n → (Fin 2 → ℝ)) :
    T (Fin.cons p (Fin.cons p v)) =
      (p 0)^2 * T (Fin.cons directionX (Fin.cons directionX v)) +
      (p 0*p 1) * T (Fin.cons directionX (Fin.cons directionY v)) +
      (p 0*p 1) * T (Fin.cons directionY (Fin.cons directionX v)) +
      (p 1)^2 * T (Fin.cons directionY (Fin.cons directionY v)) := by
  rw [cml_head T p (Fin.cons p v)]
  have hx := cml_head (T.curryLeft directionX) p v
  have hy := cml_head (T.curryLeft directionY) p v
  simp only [ContinuousMultilinearMap.curryLeft_apply] at hx hy
  rw [hx,hy]
  ring

private theorem cml_ppp {n : ℕ}
    (T : ContinuousMultilinearMap ℝ (fun _ : Fin (n+3) => Fin 2 → ℝ) ℝ)
    (p : Fin 2 → ℝ) (v : Fin n → (Fin 2 → ℝ)) :
    T (Fin.cons p (Fin.cons p (Fin.cons p v))) =
      (p 0)^3 * T (Fin.cons directionX (Fin.cons directionX (Fin.cons directionX v))) +
      (p 0)^2*p 1 * T (Fin.cons directionX (Fin.cons directionX (Fin.cons directionY v))) +
      (p 0)^2*p 1 * T (Fin.cons directionX (Fin.cons directionY (Fin.cons directionX v))) +
      p 0*(p 1)^2 * T (Fin.cons directionX (Fin.cons directionY (Fin.cons directionY v))) +
      (p 0)^2*p 1 * T (Fin.cons directionY (Fin.cons directionX (Fin.cons directionX v))) +
      p 0*(p 1)^2 * T (Fin.cons directionY (Fin.cons directionX (Fin.cons directionY v))) +
      p 0*(p 1)^2 * T (Fin.cons directionY (Fin.cons directionY (Fin.cons directionX v))) +
      (p 1)^3 * T (Fin.cons directionY (Fin.cons directionY (Fin.cons directionY v))) := by
  rw [cml_head T p (Fin.cons p (Fin.cons p v))]
  have hx := cml_pp (T.curryLeft directionX) p v
  have hy := cml_pp (T.curryLeft directionY) p v
  simp only [ContinuousMultilinearMap.curryLeft_apply] at hx hy
  rw [hx,hy]
  ring

private theorem source_word_2_xx {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX] = iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX] := by
  rfl

private theorem source_word_2_xy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] = iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] := by
  rfl

private theorem source_word_2_yx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionX] = iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY] := by
  let σ : Equiv.Perm (Fin 2) := Equiv.ofBijective (fun i => ![1,0] i) (by decide)
  have hw : (![directionX,directionY] ∘ σ) = ![directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 2 0 ![directionX,directionY] σ

private theorem source_word_2_yy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionY,directionY] = sourceQ L ω := by
  rfl

private theorem source_word_3_xxx {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX] = sourceAxialThird L ω := by
  rfl

private theorem source_word_3_xxy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY] = sourceRawU L ω 0 := by
  rfl

private theorem source_word_3_xyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX] = sourceRawU L ω 0 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![0,2,1] i) (by decide)
  have hw : (![directionX,directionX,directionY] ∘ σ) = ![directionX,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionX,directionY] σ

private theorem source_word_3_xyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY] = sourceRawU L ω 1 := by
  rfl

private theorem source_word_3_yxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX] = sourceRawU L ω 0 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![2,0,1] i) (by decide)
  have hw : (![directionX,directionX,directionY] ∘ σ) = ![directionY,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionX,directionY] σ

private theorem source_word_3_yxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY] = sourceRawU L ω 1 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![1,0,2] i) (by decide)
  have hw : (![directionX,directionY,directionY] ∘ σ) = ![directionY,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionY,directionY] σ

private theorem source_word_3_yyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX] = sourceRawU L ω 1 := by
  change iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX] = iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 3) := Equiv.ofBijective (fun i => ![1,2,0] i) (by decide)
  have hw : (![directionX,directionY,directionY] ∘ σ) = ![directionY,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 3 0 ![directionX,directionY,directionY] σ

private theorem source_word_3_yyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY] = sourceRawU L ω 2 := by
  rfl

private theorem source_word_4_xxxx {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionX] = sourceRawU L ω 3 := by
  rfl

private theorem source_word_4_xxxy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY] = sourceRawU L ω 4 := by
  rfl

private theorem source_word_4_xxyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionX] = sourceRawU L ω 4 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,1,3,2] i) (by decide)
  have hw : (![directionX,directionX,directionX,directionY] ∘ σ) = ![directionX,directionX,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionX,directionY] σ

private theorem source_word_4_xxyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY] = sourceRawU L ω 5 := by
  rfl

private theorem source_word_4_xyxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionX] = sourceRawU L ω 4 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,3,1,2] i) (by decide)
  have hw : (![directionX,directionX,directionX,directionY] ∘ σ) = ![directionX,directionY,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionX,directionY] σ

private theorem source_word_4_xyxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionY] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionX,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,2,1,3] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionX,directionY,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_xyyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionX] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![0,2,3,1] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionX,directionY,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_xyyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY] = sourceRawU L ω 6 := by
  rfl

private theorem source_word_4_yxxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionX] = sourceRawU L ω 4 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionX,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![3,0,1,2] i) (by decide)
  have hw : (![directionX,directionX,directionX,directionY] ∘ σ) = ![directionY,directionX,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionX,directionY] σ

private theorem source_word_4_yxxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionY] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionX,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![2,0,1,3] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionY,directionX,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_yxyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionX] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![2,0,3,1] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionY,directionX,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_yxyy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionY] = sourceRawU L ω 6 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionX,directionY,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![1,0,2,3] i) (by decide)
  have hw : (![directionX,directionY,directionY,directionY] ∘ σ) = ![directionY,directionX,directionY,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionY,directionY,directionY] σ

private theorem source_word_4_yyxx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionX] = sourceRawU L ω 5 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionX,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![2,3,0,1] i) (by decide)
  have hw : (![directionX,directionX,directionY,directionY] ∘ σ) = ![directionY,directionY,directionX,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionX,directionY,directionY] σ

private theorem source_word_4_yyxy {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionY] = sourceRawU L ω 6 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionX,directionY] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![1,2,0,3] i) (by decide)
  have hw : (![directionX,directionY,directionY,directionY] ∘ σ) = ![directionY,directionY,directionX,directionY] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionY,directionY,directionY] σ

private theorem source_word_4_yyyx {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionX] = sourceRawU L ω 6 := by
  change iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionX] = iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionX,directionY,directionY,directionY]
  let σ : Equiv.Perm (Fin 4) := Equiv.ofBijective (fun i => ![1,2,3,0] i) (by decide)
  have hw : (![directionX,directionY,directionY,directionY] ∘ σ) = ![directionY,directionY,directionY,directionX] := by
    ext i; fin_cases i <;> rfl
  simpa only [hw] using source_derivative_comp_perm hL ω 4 0 ![directionX,directionY,directionY,directionY] σ

private theorem source_word_4_yyyy {L : ℝ} (_hL : L ≠ 0) (ω : SmoothSample 2 L) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![directionY,directionY,directionY,directionY] = sourceRawU L ω 7 := by
  rfl


theorem source_third_ppx_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![p,p,directionX] =
      sourceAxialThird L ω * (p 0)^2 + 2*sourceRawU L ω 0*p 0*p 1 + sourceRawU L ω 1*(p 1)^2 := by
  have h := cml_pp (iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0) p ![directionX]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_3_xxx hL ω, source_word_3_xyx hL ω, source_word_3_yxx hL ω, source_word_3_yyx hL ω]
  ring

theorem source_third_ppy_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0 ![p,p,directionY] =
      sourceRawU L ω 0*(p 0)^2 + 2*sourceRawU L ω 1*p 0*p 1 + sourceRawU L ω 2*(p 1)^2 := by
  have h := cml_pp (iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0) p ![directionY]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_3_xxy hL ω, source_word_3_xyy hL ω, source_word_3_yxy hL ω, source_word_3_yyy hL ω]
  ring

theorem source_fourth_pppx_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![p,p,p,directionX] =
      sourceRawU L ω 3*(p 0)^3 + 3*sourceRawU L ω 4*(p 0)^2*p 1 + 3*sourceRawU L ω 5*p 0*(p 1)^2 + sourceRawU L ω 6*(p 1)^3 := by
  have h := cml_ppp (iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0) p ![directionX]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_4_xxxx hL ω, source_word_4_xxyx hL ω, source_word_4_xyxx hL ω, source_word_4_xyyx hL ω, source_word_4_yxxx hL ω, source_word_4_yxyx hL ω, source_word_4_yyxx hL ω, source_word_4_yyyx hL ω]
  ring

theorem source_fourth_pppy_expansion {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L) (p : Fin 2 → ℝ) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0 ![p,p,p,directionY] =
      sourceRawU L ω 4*(p 0)^3 + 3*sourceRawU L ω 5*(p 0)^2*p 1 + 3*sourceRawU L ω 6*p 0*(p 1)^2 + sourceRawU L ω 7*(p 1)^3 := by
  have h := cml_ppp (iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0) p ![directionY]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  simp only [source_word_4_xxxy hL ω, source_word_4_xxyy hL ω, source_word_4_xyxy hL ω, source_word_4_xyyy hL ω, source_word_4_yxxy hL ω, source_word_4_yxyy hL ω, source_word_4_yyxy hL ω, source_word_4_yyyy hL ω]
  ring

theorem source_second_p_basis {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i : Fin 2) :
    iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![p,![directionX,directionY] i] =
      ![iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionX]*p 0 +
          iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]*p 1,
        iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0 ![directionX,directionY]*p 0 +
          sourceQ L ω*p 1] i := by
  have h := cml_head (iteratedFDeriv ℝ 2 (smoothSourceField 2 L ω) 0) p ![![directionX,directionY] i]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  fin_cases i <;> simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Fin.reduceFinMk,
    source_word_2_yx hL ω,source_word_2_yy hL ω] <;> ring

theorem source_third_p_basis_basis {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i j : Fin 2) :
    iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0
        ![p,![directionX,directionY] i,![directionX,directionY] j] =
      !![sourceAxialThird L ω*p 0+sourceRawU L ω 0*p 1,
          sourceRawU L ω 0*p 0+sourceRawU L ω 1*p 1;
          sourceRawU L ω 0*p 0+sourceRawU L ω 1*p 1,
          sourceRawU L ω 1*p 0+sourceRawU L ω 2*p 1] i j := by
  have h := cml_head (iteratedFDeriv ℝ 3 (smoothSourceField 2 L ω) 0) p
    ![![directionX,directionY] i,![directionX,directionY] j]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  fin_cases i <;> fin_cases j <;>
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.of_apply,Fin.reduceFinMk,
      source_word_3_xxx hL ω, source_word_3_xxy hL ω, source_word_3_xyx hL ω, source_word_3_xyy hL ω, source_word_3_yxx hL ω, source_word_3_yxy hL ω, source_word_3_yyx hL ω, source_word_3_yyy hL ω] <;> ring

theorem source_fourth_pp_basis_basis {L : ℝ} (hL : L ≠ 0) (ω : SmoothSample 2 L)
    (p : Fin 2 → ℝ) (i j : Fin 2) :
    iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0
        ![p,p,![directionX,directionY] i,![directionX,directionY] j] =
      !![sourceRawU L ω 3*(p 0)^2+2*sourceRawU L ω 4*p 0*p 1+sourceRawU L ω 5*(p 1)^2,
          sourceRawU L ω 4*(p 0)^2+2*sourceRawU L ω 5*p 0*p 1+sourceRawU L ω 6*(p 1)^2;
          sourceRawU L ω 4*(p 0)^2+2*sourceRawU L ω 5*p 0*p 1+sourceRawU L ω 6*(p 1)^2,
          sourceRawU L ω 5*(p 0)^2+2*sourceRawU L ω 6*p 0*p 1+sourceRawU L ω 7*(p 1)^2] i j := by
  have h := cml_pp (iteratedFDeriv ℝ 4 (smoothSourceField 2 L ω) 0) p
    ![![directionX,directionY] i,![directionX,directionY] j]
  simp only [Matrix.Fin.cons_vecCons] at h
  rw [h]
  fin_cases i <;> fin_cases j <;>
    simp only [Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.of_apply,Fin.reduceFinMk,
      source_word_4_xxxx hL ω, source_word_4_xxxy hL ω, source_word_4_xxyx hL ω, source_word_4_xxyy hL ω, source_word_4_xyxx hL ω, source_word_4_xyxy hL ω, source_word_4_xyyx hL ω, source_word_4_xyyy hL ω, source_word_4_yxxx hL ω, source_word_4_yxxy hL ω, source_word_4_yxyx hL ω, source_word_4_yxyy hL ω, source_word_4_yyxx hL ω, source_word_4_yyxy hL ω, source_word_4_yyyx hL ω, source_word_4_yyyy hL ω] <;> ring

end I4SourcePinPreservingQuartic
