import SourceFinitePinKernel
import SourceContactCovariance

noncomputable section
open scoped BigOperators
set_option autoImplicit false

namespace I4SourceFiniteTrig

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
  <;> ring

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
    simp only [atomSource, dif_pos rfl]
    rw [atom_pairing_single]
    have hA := (atom_amplitude_pos hL none).ne'
    simp only [modeCoefficient, sourceModeAmplitude] at hA ⊢
    simp only [phase, Pi.zero_apply, Int.cast_zero, mul_zero, Finset.sum_const_zero,
      zero_add]
    field_simp
  · by_cases hk : k ∈ halfLattice 2
    · simp only [atomSource, dif_neg hk0, dif_pos hk]
      rw [atom_pairing_pair hL]
      rw [Real.cos_add]
      ring
    · simp only [atomSource, dif_neg hk0, dif_neg hk]
      rw [atom_pairing_pair hL]
      change Real.cos θ * Real.cos (phase 2 L (-k) x) +
        Real.sin θ * Real.sin (phase 2 L (-k) x) = _
      rw [atom_phase_neg, Real.cos_neg, Real.sin_neg, Real.cos_add]
      ring

end I4SourceFiniteTrig
