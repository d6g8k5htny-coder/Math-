import Mathlib.Analysis.SpecialFunctions.PolarCoord
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.MeasureTheory.Integral.Lebesgue.Map
import Mathlib.Tactic

/-!
Two exact linear-volume changes for Cap I4's d=3 spectral argument.
These are statements about actual Lebesgue measures, not assumed Jacobians.
The full three-entry product rearrangement and Gaussian model remain separate.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory Set
open scoped ENNReal Real
namespace CapI4Linear

/-- (a,d) to the source convention ((a+d)/2,(a-d)/2). -/
def tracePair : (ℝ × ℝ) →ₗ[ℝ] ℝ × ℝ :=
  Matrix.toLin (.finTwoProd ℝ) (.finTwoProd ℝ)
    !![(1/2 : ℝ), 1/2; 1/2, -1/2]

/-- (trace,radius) to increasingly ordered candidate eigenvalues. -/
def spectralPair : (ℝ × ℝ) →ₗ[ℝ] ℝ × ℝ :=
  Matrix.toLin (.finTwoProd ℝ) (.finTwoProd ℝ) !![(1 : ℝ), -1; 1, 1]

theorem tracePair_apply (q : ℝ × ℝ) :
    tracePair q = ((q.1 + q.2)/2, (q.1 - q.2)/2) := by
  simp only [tracePair, Matrix.toLin_finTwoProd_apply]
  ext <;> dsimp <;> ring

theorem spectralPair_apply (q : ℝ × ℝ) :
    spectralPair q = (q.1 - q.2, q.1 + q.2) := by
  simp [spectralPair, Matrix.toLin_finTwoProd_apply, sub_eq_add_neg]

theorem det_tracePair : LinearMap.det tracePair = -(1/2 : ℝ) := by
  norm_num [tracePair, LinearMap.det_toLin, Matrix.det_fin_two_of]

theorem det_spectralPair : LinearMap.det spectralPair = (2 : ℝ) := by
  norm_num [spectralPair, LinearMap.det_toLin, Matrix.det_fin_two_of]

/-- The source traceless sign is opposite to the increasing-eigenvalue radius. -/
theorem tracePair_spectralPair (q : ℝ × ℝ) :
    tracePair (spectralPair q) = (q.1, -q.2) := by
  rw [tracePair_apply, spectralPair_apply]
  ext <;> dsimp <;> ring

theorem spectralPair_tracePair (q : ℝ × ℝ) :
    spectralPair (tracePair q) = (q.2, q.1) := by
  rw [spectralPair_apply, tracePair_apply]
  ext <;> dsimp <;> ring

/-- Pushforward uses the inverse absolute determinant, hence factor TWO. -/
theorem map_tracePair :
    Measure.map tracePair (volume : Measure (ℝ × ℝ)) = (2 : ℝ≥0∞) • volume := by
  have hdet : LinearMap.det tracePair ≠ 0 := by rw [det_tracePair]; norm_num
  have h := Measure.map_linearMap_addHaar_eq_smul_addHaar
    (volume : Measure (ℝ × ℝ)) hdet
  norm_num [det_tracePair] at h
  exact h

/-- The spectral-plane pushforward has factor one half, not two. -/
theorem map_spectralPair :
    Measure.map spectralPair (volume : Measure (ℝ × ℝ)) = (1/2 : ℝ≥0∞) • volume := by
  have hdet : LinearMap.det spectralPair ≠ 0 := by rw [det_spectralPair]; norm_num
  have h := Measure.map_linearMap_addHaar_eq_smul_addHaar
    (volume : Measure (ℝ × ℝ)) hdet
  norm_num [det_spectralPair] at h
  rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 2)] at h
  norm_num at h
  exact h

theorem lintegral_tracePair (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ q : ℝ × ℝ, G (tracePair q)) = (2 : ℝ≥0∞) * ∫⁻ q : ℝ × ℝ, G q := by
  calc
    _ = ∫⁻ q : ℝ × ℝ, G q ∂Measure.map tracePair volume :=
      (lintegral_map hG tracePair.continuous_of_finiteDimensional.measurable).symm
    _ = _ := by simp only [map_tracePair, lintegral_smul_measure, smul_eq_mul]

theorem lintegral_spectralPair (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ q : ℝ × ℝ, G (spectralPair q)) = (1/2 : ℝ≥0∞) * ∫⁻ q : ℝ × ℝ, G q := by
  calc
    _ = ∫⁻ q : ℝ × ℝ, G q ∂Measure.map spectralPair volume :=
      (lintegral_map hG spectralPair.continuous_of_finiteDimensional.measurable).symm
    _ = _ := by simp only [map_spectralPair, lintegral_smul_measure, smul_eq_mul]

/-- The exact positive chamber, with no lower cutoff on either eigenvalue. -/
theorem positive_chamber_change (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ q : ℝ × ℝ in {q | 0 < q.2 ∧ q.2 < q.1}, G (q.1-q.2, q.1+q.2)) =
      (1/2 : ℝ≥0∞) * ∫⁻ e : ℝ × ℝ in {e | 0 < e.1 ∧ e.1 < e.2}, G e := by
  have hs : MeasurableSet {e : ℝ × ℝ | 0 < e.1 ∧ e.1 < e.2} := by
    exact (isOpen_lt continuous_const continuous_fst).measurableSet.inter
      (isOpen_lt continuous_fst continuous_snd).measurableSet
  have he : spectralPair ⁻¹' {e : ℝ × ℝ | 0 < e.1 ∧ e.1 < e.2} =
      {q : ℝ × ℝ | 0 < q.2 ∧ q.2 < q.1} := by
    ext q
    simp only [mem_preimage, mem_ofPred_eq, spectralPair_apply]
    constructor <;> intro h <;> constructor <;> linarith [h.1,h.2]
  calc
    _ = ∫⁻ q : ℝ × ℝ in spectralPair ⁻¹' {e : ℝ × ℝ | 0 < e.1 ∧ e.1 < e.2},
        G (spectralPair q) := by simp only [he, spectralPair_apply]
    _ = ∫⁻ e : ℝ × ℝ in {e | 0 < e.1 ∧ e.1 < e.2},
        G e ∂Measure.map spectralPair volume :=
      (setLIntegral_map hs hG spectralPair.continuous_of_finiteDimensional.measurable).symm
    _ = _ := by simp only [map_spectralPair, Measure.restrict_smul, lintegral_smul_measure, smul_eq_mul]

/-- Both the spectral-plane Jacobian and rho=(Lambda-lambda)/2 are retained. -/
theorem weighted_positive_chamber_change (G : ℝ × ℝ → ℝ≥0∞) (hG : Measurable G) :
    (∫⁻ q : ℝ × ℝ in {q | 0 < q.2 ∧ q.2 < q.1},
      ENNReal.ofReal q.2 * G (q.1-q.2, q.1+q.2)) =
      (1/4 : ℝ≥0∞) * ∫⁻ e : ℝ × ℝ in {e | 0 < e.1 ∧ e.1 < e.2},
        ENNReal.ofReal (e.2-e.1) * G e := by
  have hH : Measurable (fun e : ℝ × ℝ => ENNReal.ofReal ((e.2-e.1)/2) * G e) := by
    fun_prop
  have hweight (e : ℝ × ℝ) : ENNReal.ofReal ((e.2-e.1)/2) =
      (1/2 : ℝ≥0∞) * ENNReal.ofReal (e.2-e.1) := by
    rw [show (e.2-e.1)/2 = (1/2 : ℝ)*(e.2-e.1) by ring,
      ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 1/2)]
    rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 2)]
    norm_num
  calc
    _ = ∫⁻ q : ℝ × ℝ in {q | 0 < q.2 ∧ q.2 < q.1},
        ENNReal.ofReal (((q.1+q.2)-(q.1-q.2))/2) * G (q.1-q.2, q.1+q.2) := by
      apply lintegral_congr
      intro q
      rw [show ((q.1+q.2)-(q.1-q.2))/2 = q.2 by ring]
    _ = (1/2 : ℝ≥0∞) * ∫⁻ e : ℝ × ℝ in {e | 0 < e.1 ∧ e.1 < e.2},
        ENNReal.ofReal ((e.2-e.1)/2) * G e :=
      positive_chamber_change _ hH
    _ = (1/2 : ℝ≥0∞) * ((1/2 : ℝ≥0∞) *
        ∫⁻ e : ℝ × ℝ in {e | 0 < e.1 ∧ e.1 < e.2},
          ENNReal.ofReal (e.2-e.1) * G e) := by
      simp_rw [hweight, mul_assoc]
      rw [lintegral_const_mul _ (by fun_prop)]
    _ = _ := by
      have hhalf : ENNReal.ofReal (1/2 : ℝ) = (1/2 : ℝ≥0∞) := by
        rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 2)]
        norm_num
      have hquarter : ENNReal.ofReal (1/4 : ℝ) = (1/4 : ℝ≥0∞) := by
        rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 4)]
        norm_num
      rw [← mul_assoc, ← hhalf, ← hquarter,
        ← ENNReal.ofReal_mul (by norm_num : (0 : ℝ) ≤ 1/2)]
      norm_num

end CapI4Linear
