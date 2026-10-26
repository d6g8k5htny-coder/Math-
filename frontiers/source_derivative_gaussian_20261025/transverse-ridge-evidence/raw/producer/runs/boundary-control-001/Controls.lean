import AdaptiveFoldTransverseRidge

open Set
open scoped Topology ContDiff
namespace AdaptiveFoldTransverseRidgeControls
open AdaptiveFoldTransverseRidge

/-- A nonconstant horizontal root from an actual polynomial potential. -/
noncomputable def positiveV (p : ℝ × ℝ) : ℝ := p.1 * p.2 - p.2 * p.2 * (1 / 2)

theorem positiveV_c4 : ContDiff ℝ 4 positiveV := by unfold positiveV; fun_prop

theorem positiveV_Vy (p : ℝ × ℝ) : Vy positiveV p = p.1 - p.2 := by
  have hx : HasFDerivAt (fun q : ℝ × ℝ => q.1) (ContinuousLinearMap.fst ℝ ℝ ℝ) p := hasFDerivAt_fst
  have hy : HasFDerivAt (fun q : ℝ × ℝ => q.2) (ContinuousLinearMap.snd ℝ ℝ ℝ) p := hasFDerivAt_snd
  have h := (hx.mul hy).sub ((hy.mul hy).mul_const (1 / 2 : ℝ))
  change HasFDerivAt positiveV _ p at h
  unfold Vy partialY
  rw [h.fderiv]
  simp [ey]
  ring

theorem positiveV_Gderiv (p : ℝ × ℝ) :
    fderiv ℝ (Vy positiveV) p = ContinuousLinearMap.fst ℝ ℝ ℝ - ContinuousLinearMap.snd ℝ ℝ ℝ := by
  have hfun : Vy positiveV = fun q : ℝ × ℝ => q.1 - q.2 := funext positiveV_Vy
  rw [hfun]
  have h := (hasFDerivAt_fst (𝕜 := ℝ) (p := p)).sub (hasFDerivAt_snd (𝕜 := ℝ) (p := p))
  change HasFDerivAt (fun q : ℝ × ℝ => q.1 - q.2) _ p at h
  exact h.fderiv

theorem positiveV_Gx (p : ℝ × ℝ) : partialX (Vy positiveV) p = 1 := by
  rw [partialX, positiveV_Gderiv]
  simp [ex]

theorem positiveV_Gy (p : ℝ × ℝ) : partialY (Vy positiveV) p = -1 := by
  rw [partialY, positiveV_Gderiv]
  simp [ey]

theorem positiveV_Gsecond (p : ℝ × ℝ) : fderiv ℝ (fderiv ℝ (Vy positiveV)) p = 0 := by
  have hfun : fderiv ℝ (Vy positiveV) = fun _ =>
      ContinuousLinearMap.fst ℝ ℝ ℝ - ContinuousLinearMap.snd ℝ ℝ ℝ := funext positiveV_Gderiv
  rw [hfun]
  simp

/-- Instantiate the complete construction, including both endpoint full jets,
root bound, derivative formulas, and the literal profile interface. -/
theorem positive_constructed_ridge :
    ∃ (U : Set ℝ) (z : ℝ → ℝ), IsOpen U ∧ Icc (-(1 / 2 : ℝ)) (1 / 2) ⊆ U ∧
      ContDiffOn ℝ 2 z U ∧ (∀ x ∈ U, z x = x) ∧
      HasDerivAt z 1 (-(1 / 2 : ℝ)) ∧ HasDerivAt z 1 (1 / 2 : ℝ) ∧
      deriv (deriv z) 0 = 0 ∧
      (∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), |z x| ≤ (1 / 2 : ℝ)) := by
  have hrect : Icc (-(1 / 2 : ℝ)) (1 / 2) ×ˢ Icc (-(1 : ℝ)) 1 ⊆ (univ : Set (ℝ × ℝ)) :=
    subset_univ _
  have hn : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), ∀ y ∈ Icc (-(1 : ℝ)) 1,
      partialY (Vy positiveV) (x, y) ≤ -(1 : ℝ) := by
    intros; rw [positiveV_Gy]
  have hl : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), 0 < Vy positiveV (x, -(1 : ℝ)) := by
    intro x hx; rw [positiveV_Vy]; dsimp; linarith [hx.1]
  have hu : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), Vy positiveV (x, (1 : ℝ)) < 0 := by
    intro x hx; rw [positiveV_Vy]; dsimp; linarith [hx.2]
  have hc : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), |Vy positiveV (x, 0)| ≤ (1 / 2 : ℝ) := by
    intro x hx; rw [positiveV_Vy]; dsimp; rw [sub_zero]; exact abs_le.mpr hx
  have hf : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), ∀ y ∈ Icc (-(1 : ℝ)) 1,
      |partialX (Vy positiveV) (x, y)| ≤ (1 : ℝ) := by
    intros; rw [positiveV_Gx]; norm_num
  have h2 : ∀ x ∈ Icc (-(1 / 2 : ℝ)) (1 / 2), ∀ y ∈ Icc (-(1 : ℝ)) 1,
      ∀ a b : ℝ × ℝ, |fderiv ℝ (fderiv ℝ (Vy positiveV)) (x, y) a b| ≤ (0 : ℝ) := by
    intros; rw [positiveV_Gsecond]; simp
  obtain ⟨U, z, hU, hJU, hz, hroot, _, _, hj, hb, _⟩ :=
    exists_unique_c2_transverse_ridge_with_jets (by norm_num : (0 : ℝ) < 1)
      (by norm_num : (0 : ℝ) < 1) isOpen_univ positiveV_c4.contDiffOn hrect hn hl hu
      (by norm_num : (0 : ℝ) ≤ 1) (by norm_num : (0 : ℝ) ≤ 0) hc hf
      (fun x hx y hy => h2 x hx y hy ex ex) (fun x hx y hy => h2 x hx y hy ex ey)
      (fun x hx y hy => h2 x hx y hy ey ex) (fun x hx y hy => h2 x hx y hy ey ey)
  have heq : ∀ x ∈ U, z x = x := by
    intro x hx
    have h := (hroot x hx).2.2
    rw [positiveV_Vy] at h
    dsimp at h
    linarith
  have hj1 (x : ℝ) (hx : x ∈ U) : HasDerivAt z 1 x := by
    have h := (hj x hx).2.2.2.1
    rw [positiveV_Gx, positiveV_Gy] at h
    norm_num at h
    simpa only [h] using (hj x hx).1
  refine ⟨U, z, hU, hJU, hz, heq, hj1 _ (hJU (by norm_num)), hj1 _ (hJU (by norm_num)), ?_, ?_⟩
  · have h := (hj 0 (hJU (by norm_num))).2.2.2.2
    rw [positiveV_Gsecond] at h
    simpa using h
  · intro x hx
    simpa using (hb x hx).1

/-- A genuine negative vertical derivative alone does not force a strip root. -/
noncomputable def negativeV (p : ℝ × ℝ) : ℝ := 3 * p.2 - p.2 * p.2 * (1 / 2)

theorem negativeV_Vy (p : ℝ × ℝ) : Vy negativeV p = 3 - p.2 := by
  have hy : HasFDerivAt (fun q : ℝ × ℝ => q.2) (ContinuousLinearMap.snd ℝ ℝ ℝ) p := hasFDerivAt_snd
  have h := (hy.const_mul 3).sub ((hy.mul hy).mul_const (1 / 2 : ℝ))
  change HasFDerivAt negativeV _ p at h
  unfold Vy partialY
  rw [h.fderiv]
  simp [ey]
  ring

theorem negativeV_strict_vertical (p : ℝ × ℝ) : partialY (Vy negativeV) p = -1 := by
  have hfun : Vy negativeV = fun q : ℝ × ℝ => 3 - q.2 := funext negativeV_Vy
  rw [partialY, hfun]
  have h := (hasFDerivAt_const (3 : ℝ) p).sub (hasFDerivAt_snd (𝕜 := ℝ) (p := p))
  change HasFDerivAt (fun q : ℝ × ℝ => 3 - q.2) _ p at h
  rw [h.fderiv]
  simp [ey]

theorem negativeV_no_root (x : ℝ) : ¬ ∃ y ∈ Icc (-(1 : ℝ)) 1, Vy negativeV (x, y) = 0 := by
  rintro ⟨y, hy, hz⟩
  rw [negativeV_Vy] at hz
  dsimp at hz
  linarith [hy.2]

end AdaptiveFoldTransverseRidgeControls
