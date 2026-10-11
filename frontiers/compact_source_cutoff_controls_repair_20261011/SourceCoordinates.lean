import PhysicalSpectral
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Topology.OpenPartialHomeomorph.IsImage

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Filter Set Matrix
open scoped Topology ContDiff Matrix.Norms.Frobenius
namespace SourceCoordinates
abbrev E (n : ℕ) := EuclideanSpace ℝ (Fin n)
abbrev X (n : ℕ) := Fin n → ℝ
open MorseCongruence

def action (n : ℕ) : Mat n →L[ℝ] E n →L[ℝ] E n :=
  (Matrix.toEuclideanLin.trans LinearMap.toContinuousLinearMap).toLinearMap.toContinuousLinearMap

def R {n : ℕ} (J : Sym n) (s : Sym n → Sym n) (M : E n → Sym n) (u : E n) : Mat n :=
  1 + (J : Mat n) * (s (M u) : Mat n)

def theta {n : ℕ} (J : Sym n) (s : Sym n → Sym n) (M : E n → Sym n) (u : E n) : E n :=
  action n (R J s M u) u

def quadratic {n : ℕ} (A : Mat n) (u : E n) : ℝ :=
  ∑ i, ∑ j, u i * A i j * u j

theorem action_one (n : ℕ) : action n 1 = ContinuousLinearMap.id ℝ (E n) := by
  apply ContinuousLinearMap.ext
  intro u
  change Matrix.toLpLin 2 2 (1 : Mat n) u = u
  rw [Matrix.toLpLin_one]
  rfl

theorem action_apply {n : ℕ} (A : Mat n) (u : E n) :
    WithLp.ofLp (action n A u) = A *ᵥ WithLp.ofLp u := rfl

theorem quadratic_eq_dot {n : ℕ} (A : Mat n) (u : E n) :
    quadratic A u = dotProduct (WithLp.ofLp u) (A *ᵥ WithLp.ofLp u) := by
  simp [quadratic, dotProduct, Matrix.mulVec, Finset.mul_sum, mul_assoc]

theorem quadratic_congruence {n : ℕ} (J A : Mat n) (u : E n) :
    quadratic (star A * J * A) u = quadratic J (action n A u) := by
  rw [quadratic_eq_dot, quadratic_eq_dot, action_apply]
  rw [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial]
  rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec]
  rw [Matrix.dotProduct_transpose_mulVec, dotProduct_comm]

theorem apply_hasFDerivAt_zero {n : ℕ} (A : E n → E n →L[ℝ] E n)
    (hA : DifferentiableAt ℝ A 0) (hA0 : A 0 = ContinuousLinearMap.id ℝ (E n)) :
    HasFDerivAt (fun u => A u u) (ContinuousLinearMap.id ℝ (E n)) 0 := by
  simpa [hA0]
    using hA.hasFDerivAt.clm_apply (hasFDerivAt_id (0 : E n))

theorem exists_coordinates {n : ℕ} (J : Sym n) (hJ : (J : Mat n) * (J : Mat n) = 1)
    (M : E n → Sym n) (hM : ContDiff ℝ 2 M) (hM0 : M 0 = J) :
    ∃ (V : Set (Sym n)) (s : Sym n → Sym n) (e : OpenPartialHomeomorph (E n) (E n)),
      IsOpen V ∧ J ∈ V ∧ s J = 0 ∧ ContDiffOn ℝ 2 s V ∧
      (∀ u, e u = theta J s M u) ∧ e 0 = 0 ∧ e.symm 0 = 0 ∧
      0 ∈ e.source ∧ 0 ∈ e.target ∧
      HasFDerivAt e (ContinuousLinearMap.id ℝ (E n)) 0 ∧
      ContDiffOn ℝ 2 e e.source ∧ ContDiffOn ℝ 2 e.symm e.target ∧
      (∀ u ∈ e.source, M u ∈ V ∧ quadratic (M u : Mat n) u = quadratic (J : Mat n) (e u)) := by
  obtain ⟨V, s, hV, hJV, hs0, hs, hcong⟩ := exists_congruence_branch J hJ
  let U : Set (E n) := M ⁻¹' V
  have hU : IsOpen U := hV.preimage hM.continuous
  have h0U : (0 : E n) ∈ U := by simpa [U, hM0] using hJV
  let inc : Sym n →L[ℝ] Mat n := (selfAdjoint.submodule ℝ (Mat n)).subtypeL
  have hSM : ContDiffOn ℝ 2 (fun u => s (M u)) U :=
    hs.comp hM.contDiffOn (fun u hu => hu)
  have hR : ContDiffOn ℝ 2 (R J s M) U := by
    exact contDiffOn_const.add (contDiffOn_const.mul (inc.contDiff.comp_contDiffOn hSM))
  let A : E n → E n →L[ℝ] E n := fun u => action n (R J s M u)
  have hA : ContDiffOn ℝ 2 A U := (action n).contDiff.comp_contDiffOn hR
  have htheta : ContDiffOn ℝ 2 (theta J s M) U := hA.clm_apply contDiffOn_id
  have hR0 : R J s M 0 = 1 := by simp [R, hM0, hs0]
  have hA0 : A 0 = ContinuousLinearMap.id ℝ (E n) := by
    simp only [A, hR0, action_one]
  have htheta0 : theta J s M 0 = 0 := by simp [theta]
  have hthetaAt : ContDiffAt ℝ 2 (theta J s M) 0 := htheta.contDiffAt (hU.mem_nhds h0U)
  have hd : HasFDerivAt (theta J s M) (ContinuousLinearMap.id ℝ (E n)) 0 :=
    apply_hasFDerivAt_zero A ((hA.contDiffAt (hU.mem_nhds h0U)).differentiableAt (by norm_num)) hA0
  let e0 := hthetaAt.toOpenPartialHomeomorph (theta J s M)
    (f' := ContinuousLinearEquiv.refl ℝ (E n)) hd (by norm_num)
  have h0e : (0 : E n) ∈ e0.source :=
    hthetaAt.mem_toOpenPartialHomeomorph_source (f' := ContinuousLinearEquiv.refl ℝ (E n)) hd (by norm_num)
  have h0t : (0 : E n) ∈ e0.target := by
    simpa [e0, htheta0] using hthetaAt.image_mem_toOpenPartialHomeomorph_target (f' := ContinuousLinearEquiv.refl ℝ (E n)) hd (by norm_num)
  have hinv0 : e0.symm 0 = 0 := by
    have h := e0.left_inv h0e
    change e0.symm (theta J s M 0) = 0 at h
    simpa [htheta0] using h
  have hinvAt : ContDiffAt ℝ 2 e0.symm 0 := by
    apply e0.contDiffAt_symm (f₀' := ContinuousLinearEquiv.refl ℝ (E n)) h0t
    · change HasFDerivAt (theta J s M) _ (e0.symm 0)
      rw [hinv0]
      exact hd
    · change ContDiffAt ℝ 2 (theta J s M) (e0.symm 0)
      rw [hinv0]
      exact hthetaAt
  obtain ⟨T, hT, hTinverse⟩ := hinvAt.contDiffOn le_rfl (by simp)
  obtain ⟨W, hWT, hW, h0W⟩ := mem_nhds_iff.mp hT
  let e1 := e0.restrOpen U hU
  let e := (e1.symm.restrOpen W hW).symm
  have hes : e.source ⊆ U := by
    intro u hu
    exact hu.1.2
  have het : e.target ⊆ W := by
    intro u hu
    exact hu.2
  have h0e1t : (0 : E n) ∈ e1.target := by
    exact ⟨h0t, by simpa [hinv0] using h0U⟩
  have h0es : (0 : E n) ∈ e.source := by
    exact ⟨⟨h0e, h0U⟩, by simpa [e1, e0, htheta0] using h0W⟩
  have h0et : (0 : E n) ∈ e.target := ⟨h0e1t, h0W⟩
  refine ⟨V, s, e, hV, hJV, hs0, hs, (fun _ => rfl), htheta0, hinv0,
    h0es, h0et, hd, htheta.mono hes, (hTinverse.mono (fun v hv => hWT (het hv))), ?_⟩
  intro u hu
  have hMu : M u ∈ V := hes hu
  refine ⟨hMu, ?_⟩
  rw [hcong (M u) hMu]
  exact quadratic_congruence (J : Mat n) (R J s M u) u

theorem source_coordinates {n : ℕ} {L : ℝ} (hL : L ≠ 0)
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (PhysicalSpectral.hessian (L := L) omega x0).det ≠ 0)
    (hcrit : fderiv ℝ (I4Source.sourceField n L omega) x0 = 0) :
    ∃ k : ℕ, k ≤ n ∧ ∃ (P : E n ≃L[ℝ] X n)
      (V : Set (Sym n)) (s : Sym n → Sym n) (e : OpenPartialHomeomorph (E n) (E n)),
      let J := PhysicalSpectral.signSym n k
      let M := TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap
      M 0 = J ∧ IsOpen V ∧ J ∈ V ∧ s J = 0 ∧ ContDiffOn ℝ 2 s V ∧
      (∀ u, e u = theta J s M u) ∧ e 0 = 0 ∧ e.symm 0 = 0 ∧
      0 ∈ e.source ∧ 0 ∈ e.target ∧
      HasFDerivAt e (ContinuousLinearMap.id ℝ (E n)) 0 ∧
      ContDiffOn ℝ 2 e e.source ∧ ContDiffOn ℝ 2 e.symm e.target ∧
      (∀ u ∈ e.source, M u ∈ V ∧ I4Source.sourceField n L omega (x0 + P u) =
        I4Source.sourceField n L omega x0 + quadratic (J : Mat n) (e u)) ∧
      (∀ v ∈ e.target, I4Source.sourceField n L omega (x0 + P (e.symm v)) =
        I4Source.sourceField n L omega x0 + quadratic (J : Mat n) v) := by
  obtain ⟨k, hk, P, hJ, hH, hM0, hM⟩ :=
    PhysicalSpectral.source_normalization_bundle hL omega hmajor x0 hdet
  obtain ⟨V, s, e, hV, hJV, hs0, hs, heq, he0, hi0, h0s, h0t, hd, heC, hiC, hq⟩ :=
    exists_coordinates (PhysicalSpectral.signSym n k) hJ
      (TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap) hM hM0
  refine ⟨k, hk, P, V, s, e, hM0, hV, hJV, hs0, hs, heq, he0, hi0,
    h0s, h0t, hd, heC, hiC, ?_, ?_⟩
  · intro u hu
    refine ⟨(hq u hu).1, ?_⟩
    have he := TaylorSymLift.sourceSymMatrix_quadratic hL omega hmajor x0 P.toContinuousLinearMap hcrit u
    exact he.trans (congrArg (fun q => I4Source.sourceField n L omega x0 + q) (hq u hu).2)
  · intro v hv
    have hu := e.map_target hv
    have he := TaylorSymLift.sourceSymMatrix_quadratic hL omega hmajor x0
      P.toContinuousLinearMap hcrit (e.symm v)
    change I4Source.sourceField n L omega (x0 + P (e.symm v)) =
      I4Source.sourceField n L omega x0 + quadratic _ _ at he
    rw [(hq (e.symm v) hu).2, e.right_inv hv] at he
    exact he

end SourceCoordinates
