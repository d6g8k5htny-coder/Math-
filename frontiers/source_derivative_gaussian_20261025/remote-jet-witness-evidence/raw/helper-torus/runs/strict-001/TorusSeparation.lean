import SourceTorus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

noncomputable section
namespace I4SourceRemoteJetWitness

-- BEGIN NEEDED SECTION
open I4Weights I4Torus

private theorem sourceC_ne_zero {L : ℝ} (hL : L ≠ 0) : sourceC L ≠ 0 := by
  exact div_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hL

private theorem cosine_sourceC_eq_one_iff {L : ℝ} (hL : L ≠ 0) (a b : ℝ) :
    Real.cos (sourceC L * (a - b)) = 1 ↔
      (a : AddCircle L) = (b : AddCircle L) := by
  constructor
  · intro hc
    obtain ⟨n, hn⟩ := (Real.cos_eq_one_iff _).mp hc
    have ht : 2 * Real.pi ≠ 0 := mul_ne_zero (by norm_num) Real.pi_ne_zero
    have hdiv : (n : ℝ) = (a - b) / L := by
      apply mul_left_cancel₀ ht
      calc
        (2 * Real.pi) * (n : ℝ) = (n : ℝ) * (2 * Real.pi) := by ring
        _ = sourceC L * (a - b) := hn
        _ = (2 * Real.pi) * ((a - b) / L) := by unfold sourceC; ring
    have hperiod : n • L = a - b := by
      simpa only [zsmul_eq_mul] using (eq_div_iff hL).mp hdiv
    have hz : ((a - b : ℝ) : AddCircle L) = 0 :=
      (AddCircle.coe_eq_zero_iff (p := L)).mpr ⟨n, hperiod⟩
    rw [AddCircle.coe_sub] at hz
    exact sub_eq_zero.mp hz
  · intro hab
    have hz : ((a - b : ℝ) : AddCircle L) = 0 := by
      rw [AddCircle.coe_sub]
      exact sub_eq_zero.mpr hab
    obtain ⟨n, hn⟩ := (AddCircle.coe_eq_zero_iff (p := L)).mp hz
    have hn' : (n : ℝ) * L = a - b := by
      simpa only [zsmul_eq_mul] using hn
    have hdiv : (n : ℝ) = (a - b) / L := (eq_div_iff hL).mpr hn'
    apply (Real.cos_eq_one_iff _).mpr
    refine ⟨n, ?_⟩
    calc
      (n : ℝ) * (2 * Real.pi) = (2 * Real.pi) * ((a - b) / L) := by
        rw [hdiv]
        ring
      _ = sourceC L * (a - b) := by unfold sourceC; ring

private theorem remote_positive_coordinate {L : ℝ} (hL : L ≠ 0)
    (x p : Fin 2 → ℝ)
    (hx : torusProjection 2 L x ≠ torusProjection 2 L p) :
    ∃ j : Fin 2, 0 < 1 - Real.cos (sourceC L * (x j - p j)) := by
  classical
  have hex : ∃ j : Fin 2, (x j : AddCircle L) ≠ (p j : AddCircle L) := by
    by_contra h
    push_neg at h
    apply hx
    funext j
    exact h j
  obtain ⟨j, hj⟩ := hex
  refine ⟨j, sub_pos.mpr ?_⟩
  apply lt_of_le_of_ne (Real.cos_le_one _)
  intro hc
  exact hj ((cosine_sourceC_eq_one_iff hL (x j) (p j)).mp hc)
-- END NEEDED SECTION

end I4SourceRemoteJetWitness
