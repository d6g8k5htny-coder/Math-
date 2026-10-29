import Specifications.Lifetime

/-!
Conditional countermodel to universal use of the literal upper predicate.
The field, elder interface and frame remain explicit supplied parameters.
No intended geometric law or interface inhabitance is constructed.
-/

namespace CBZ.LifetimeZeroLawCountermodel
open UniversalLaw.Spec.Lifetime

def zeroLaw (L : ℝ) (G : GaussianFieldInterface 2 L)
    (I : SuperlevelBarInterface 2 L) : PairLawInterface 2 L G I where
  p := fun _ _ _ _ => 0
  p_nonneg := by intros; norm_num
  p_le_one := by intros; norm_num

theorem zeroLaw_refutes_upper (L : ℝ) (G : GaussianFieldInterface 2 L)
    (I : SuperlevelBarInterface 2 L) (hL : 0 < L)
    (R : OrthonormalBasis (Fin 2) ℝ (E 2)) :
    ¬ ParentUniformSelectionA 2 L G I (zeroLaw L G I) 0 0 1 1 := by
  intro hypothetical
  obtain ⟨rStar, hStar, C, bound⟩ :=
    hypothetical (by norm_num) hL (by norm_num) (by norm_num) (by norm_num)
  let r : ℝ := min (rStar / 2) (min 1 (1 / (2 * (|C| + 1))))
  have hr : 0 < r := by
    dsimp [r]
    exact lt_min (by linarith) (lt_min (by norm_num) (by positivity))
  have hrStar : r ≤ rStar := by
    dsimp [r]
    have hm := min_le_left (rStar / 2) (min (1 : ℝ) (1 / (2 * (|C| + 1))))
    linarith
  have hrOne : r ≤ 1 := by
    dsimp [r]
    exact le_trans (min_le_right _ _) (min_le_left _ _)
  have hrBound : r ≤ 1 / (2 * (|C| + 1)) := by
    dsimp [r]
    exact le_trans (min_le_right _ _) (min_le_right _ _)
  have hLower : 1 ≤ C * r ^ 3 := by
    simpa [zeroLaw] using (bound r hr hrStar 0 (by simp) 1 (by simp) R).2
  have hSquare : r ^ 2 ≤ 1 := by nlinarith
  have hCube : r ^ 3 ≤ r := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hSquare) (le_of_lt hr)]
  have hCompare : C * r ^ 3 ≤ |C| * r ^ 3 :=
    mul_le_mul_of_nonneg_right (le_abs_self C) (by positivity)
  have hScale : |C| * r ^ 3 ≤ |C| * r :=
    mul_le_mul_of_nonneg_left hCube (abs_nonneg C)
  have hDen : 0 < 2 * (|C| + 1) := by positivity
  have hProduct : r * (2 * (|C| + 1)) ≤ 1 := (le_div_iff₀ hDen).mp hrBound
  have hStrict : |C| * r < 1 := by nlinarith [abs_nonneg C]
  linarith

#print axioms zeroLaw_refutes_upper

end CBZ.LifetimeZeroLawCountermodel
