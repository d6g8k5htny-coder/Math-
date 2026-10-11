import Mathlib.Analysis.Matrix.Normed
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.Calculus.InverseFunctionTheorem.ContDiff
import Mathlib.Topology.Algebra.Module.Star
import Mathlib.Tactic

noncomputable section
open scoped Matrix.Norms.Frobenius Topology ContDiff

namespace MorseCongruence

abbrev Mat (n : ℕ) := Matrix (Fin n) (Fin n) ℝ
abbrev Sym (n : ℕ) := selfAdjoint.submodule ℝ (Mat n)

def project (n : ℕ) : Mat n →L[ℝ] Sym n := selfAdjointPartL ℝ (Mat n)

def polynomial {n : ℕ} (J S : Sym n) : Sym n :=
  J + (2 : ℝ) • S + project n ((S : Mat n) * (J : Mat n) * (S : Mat n))

theorem polynomial_contDiff {n : ℕ} (J : Sym n) :
    ContDiff ℝ ∞ (polynomial J) := by
  let i : Sym n →L[ℝ] Mat n := (selfAdjoint.submodule ℝ (Mat n)).subtypeL
  exact (contDiff_const.add (contDiff_id.const_smul (2 : ℝ))).add
    ((project n).contDiff.comp ((i.contDiff.mul contDiff_const).mul i.contDiff))

set_option backward.isDefEq.respectTransparency false in
theorem polynomial_hasFDerivAt_zero {n : ℕ} (J : Sym n) :
    HasFDerivAt (polynomial J)
      ((2 : ℝ) • ContinuousLinearMap.id ℝ (Sym n)) 0 := by
  let i : Sym n →L[ℝ] Mat n := (selfAdjoint.submodule ℝ (Mat n)).subtypeL
  have hq : HasFDerivAt (fun S : Sym n => (S : Mat n) * (J : Mat n) * (S : Mat n))
      (0 : Sym n →L[ℝ] Mat n) 0 := by
    convert! ((i.hasFDerivAt (x := (0 : Sym n))).mul_const' (𝕜 := ℝ) (J : Mat n)).mul' (𝕜 := ℝ)
      (i.hasFDerivAt (x := (0 : Sym n))) using 1
    ext S
    simp [i]
  have hp : HasFDerivAt (fun S : Sym n =>
      project n ((S : Mat n) * (J : Mat n) * (S : Mat n)))
      (0 : Sym n →L[ℝ] Sym n) 0 := by
    convert! (project n).hasFDerivAt.comp (0 : Sym n) hq using 1
    ext S
    simp
  convert! ((hasFDerivAt_const J (0 : Sym n)).add
    ((hasFDerivAt_id (0 : Sym n)).const_smul (2 : ℝ))).add hp using 1
  ext S
  simp

theorem polynomial_congruence {n : ℕ} (J S : Sym n)
    (hJ : (J : Mat n) * (J : Mat n) = 1) :
    (polynomial J S : Mat n) =
      star (1 + (J : Mat n) * (S : Mat n)) * (J : Mat n) *
        (1 + (J : Mat n) * (S : Mat n)) := by
  have hs : IsSelfAdjoint ((S : Mat n) * (J : Mat n) * (S : Mat n)) := by
    change star ((S : Mat n) * (J : Mat n) * (S : Mat n)) = _
    simp only [star_mul, S.2.star_eq, J.2.star_eq, mul_assoc]
  have hp : (project n ((S : Mat n) * (J : Mat n) * (S : Mat n)) : Mat n) =
      (S : Mat n) * (J : Mat n) * (S : Mat n) :=
    hs.coe_selfAdjointPart_apply ℝ
  change (J : Mat n) + (2 : ℝ) • (S : Mat n) +
    (project n ((S : Mat n) * (J : Mat n) * (S : Mat n)) : Mat n) = _
  rw [hp]
  simp only [star_add, star_one, star_mul, S.2.star_eq, J.2.star_eq]
  calc
    (J : Mat n) + (2 : ℝ) • (S : Mat n) + (S : Mat n) * (J : Mat n) * (S : Mat n) =
        (J : Mat n) + (S : Mat n) + (S : Mat n) + (S : Mat n) * (J : Mat n) * (S : Mat n) := by
      simp [two_smul, add_assoc]
    _ = (1 + (S : Mat n) * (J : Mat n)) * (J : Mat n) *
          (1 + (J : Mat n) * (S : Mat n)) := by
      symm
      calc
        (1 + (S : Mat n) * (J : Mat n)) * (J : Mat n) * (1 + (J : Mat n) * (S : Mat n)) =
            (J : Mat n) + (S : Mat n) * ((J : Mat n) * (J : Mat n)) +
            ((J : Mat n) * (J : Mat n)) * (S : Mat n) +
            (S : Mat n) * ((J : Mat n) * (J : Mat n)) * (J : Mat n) * (S : Mat n) := by
          noncomm_ring
        _ = _ := by simp [hJ, add_assoc]

def doubleEquiv (n : ℕ) : Sym n ≃L[ℝ] Sym n where
  toFun S := (2 : ℝ) • S
  invFun S := (1 / 2 : ℝ) • S
  left_inv S := by simp [smul_smul]
  right_inv S := by simp [smul_smul]
  map_add' S T := smul_add _ _ _
  map_smul' a S := by simp [smul_smul, mul_comm]
  continuous_toFun := continuous_const_smul _
  continuous_invFun := continuous_const_smul _

theorem doubleEquiv_coe (n : ℕ) :
    (doubleEquiv n : Sym n →L[ℝ] Sym n) =
      (2 : ℝ) • ContinuousLinearMap.id ℝ (Sym n) := rfl

theorem exists_congruence_branch {n : ℕ} (J : Sym n)
    (hJ : (J : Mat n) * (J : Mat n) = 1) :
    ∃ (V : Set (Sym n)) (s : Sym n → Sym n),
      IsOpen V ∧ J ∈ V ∧ s J = 0 ∧ ContDiffOn ℝ 2 s V ∧
      ∀ M ∈ V, (M : Mat n) =
        star (1 + (J : Mat n) * (s M : Mat n)) * (J : Mat n) *
          (1 + (J : Mat n) * (s M : Mat n)) := by
  have hz : polynomial J 0 = J := by simp [polynomial]
  have hf : ContDiffAt ℝ 2 (polynomial J) 0 :=
    (polynomial_contDiff J).of_le (by simp) |>.contDiffAt
  have hd : HasFDerivAt (polynomial J) (doubleEquiv n : Sym n →L[ℝ] Sym n) 0 :=
    polynomial_hasFDerivAt_zero J
  let e := hf.toOpenPartialHomeomorph (polynomial J) hd (by norm_num)
  let s := hf.localInverse hd (by norm_num)
  have hc : s J = 0 := by simpa [s, hz] using hf.localInverse_apply_image hd (by norm_num)
  have hsm : ContDiffAt ℝ 2 s J := by simpa [s, hz] using hf.to_localInverse hd (by norm_num)
  obtain ⟨U, hU, hUs⟩ := hsm.contDiffOn le_rfl (by simp)
  obtain ⟨W, hWU, hWo, hJW⟩ := mem_nhds_iff.mp hU
  have hJe : J ∈ e.target := by
    simpa [e, hz] using hf.image_mem_toOpenPartialHomeomorph_target hd (by norm_num)
  refine ⟨W ∩ e.target, s, hWo.inter e.open_target, ⟨hJW, hJe⟩, hc,
    hUs.mono (fun M hM => hWU hM.1), ?_⟩
  intro M hM
  have he : polynomial J (s M) = M := e.right_inv hM.2
  exact (congrArg (fun T : Sym n => (T : Mat n)) he).symm.trans
    (polynomial_congruence J (s M) hJ)

end MorseCongruence
