import SourceNormalForm
import DeterministicSourceC4
import Mathlib.Analysis.InnerProductSpace.Calculus

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Filter Set Matrix SourceCoordinates MorseCongruence SourceNormalForm
open scoped Topology ContDiff Manifold Matrix.Norms.Frobenius RealInnerProductSpace
namespace SourcePushedHeight
attribute [local instance] I4TorusC4.actualChartedSpace

section Core
variable {A B H : Type*} [NormedAddCommGroup A] [InnerProductSpace ℝ A]
  [NormedAddCommGroup B] [InnerProductSpace ℝ B]
  [NormedAddCommGroup H] [NormedSpace ℝ H]

def W0 (z : A × B) : A × B := (0, -z.2)
def W1 (z : A × B) : A × B := (z.1, -z.2)
def Q0 (psi : A × B → H) (z : A × B) : H := fderiv ℝ psi z (W0 z)
def Q1 (psi : A × B → H) (z : A × B) : H := fderiv ℝ psi z (W1 z)

structure LocalGeometry (f : H → ℝ) (phi : OpenPartialHomeomorph H (A × B))
    (T : Set (A × B)) (U : Set H) (c : ℝ) (center : H) : Prop where
  target_open : IsOpen T
  physical_open : IsOpen U
  target_subset : T ⊆ phi.target
  inverse_target : MapsTo phi.symm T U
  forward_target : MapsTo phi U T
  forward_C2 : ContDiffOn ℝ 2 phi phi.source
  inverse_C2 : ContDiffOn ℝ 2 phi.symm phi.target
  push0_C1 : ContDiffOn ℝ 1 (Q0 phi.symm) T
  push1_C1 : ContDiffOn ℝ 1 (Q1 phi.symm) T
  physical0_C1 : ContDiffOn ℝ 1 ((Q0 phi.symm) ∘ phi) U
  physical1_C1 : ContDiffOn ℝ 1 ((Q1 phi.symm) ∘ phi) U
  height : ∀ z ∈ T, f (phi.symm z) = c + MorseCone.quadratic z
  rate0 : ∀ z ∈ T, fderiv ℝ f (phi.symm z) (Q0 phi.symm z) = 2 * ‖z.2‖^2
  rate1 : ∀ z ∈ T, fderiv ℝ f (phi.symm z) (Q1 phi.symm z) =
    2 * (‖z.1‖^2 + ‖z.2‖^2)
  center_target : (0 : A × B) ∈ T
  center_forward : phi center = 0
  center_inverse : phi.symm 0 = center
  center_push0 : Q0 phi.symm 0 = 0
  center_push1 : Q1 phi.symm 0 = 0

theorem pushed_C1 (psi : A × B → H) (T : Set (A × B))
    (hT : IsOpen T) (hpsi : ContDiffOn ℝ 2 psi T) :
    ContDiffOn ℝ 1 (Q0 psi) T ∧ ContDiffOn ℝ 1 (Q1 psi) T := by
  have hW0 : ContDiff ℝ 1 (W0 : A × B → A × B) := by
    unfold W0
    fun_prop
  have hW1 : ContDiff ℝ 1 (W1 : A × B → A × B) := by
    unfold W1
    fun_prop
  constructor
  · apply hT.contDiffOn_iff.mpr
    intro z hz
    exact ((hpsi.contDiffAt (hT.mem_nhds hz)).fderiv_right (m := 1) (by norm_num)).clm_apply
      hW0.contDiffAt
  · apply hT.contDiffOn_iff.mpr
    intro z hz
    exact ((hpsi.contDiffAt (hT.mem_nhds hz)).fderiv_right (m := 1) (by norm_num)).clm_apply
      hW1.contDiffAt

theorem rates_of_local_identity (f : H → ℝ) (psi : A × B → H)
    (T : Set (A × B)) (c : ℝ) (hT : IsOpen T)
    (hf : Differentiable ℝ f) (hpsi : ContDiffOn ℝ 2 psi T)
    (hidentity : ∀ z ∈ T, f (psi z) = c + MorseCone.quadratic z) :
    ∀ z ∈ T,
      fderiv ℝ f (psi z) (Q0 psi z) = 2 * ‖z.2‖^2 ∧
      fderiv ℝ f (psi z) (Q1 psi z) = 2 * (‖z.1‖^2 + ‖z.2‖^2) := by
  intro z hz
  have hq := ((hasFDerivAt_fst (p := z)).norm_sq.sub (hasFDerivAt_snd (p := z)).norm_sq).const_add c
  have hevent : (fun w => f (psi w)) =ᶠ[𝓝 z] (fun w => c + MorseCone.quadratic w) :=
    (hT.eventually_mem hz).mono (fun w hw => hidentity w hw)
  have hq' := hq.congr_of_eventuallyEq hevent
  have hc := (hf (psi z)).hasFDerivAt.comp z
    ((hpsi.contDiffAt (hT.mem_nhds hz)).differentiableAt (by norm_num)).hasFDerivAt
  have hder := hc.unique hq'
  constructor
  · have hv := congrArg (fun a : (A × B) →L[ℝ] ℝ => a (W0 z)) hder
    simpa [Q0, W0, ContinuousLinearMap.comp_apply, real_inner_self_eq_norm_sq] using hv
  · have hv := congrArg (fun a : (A × B) →L[ℝ] ℝ => a (W1 z)) hder
    simpa [Q1, W1, ContinuousLinearMap.comp_apply, real_inner_self_eq_norm_sq,
      mul_add, sub_eq_add_neg] using hv

-- Resolve the standard derivative uniqueness within the generic normed context;
-- this avoids repeating expensive alias-specific topological instance search.
theorem derivative_eq (psi : A × B → H) (d : (A × B) →L[ℝ] H) (z : A × B)
    (h : HasFDerivAt psi d z) : fderiv ℝ psi z = d := h.fderiv

end Core

theorem physicalChart_inverse_derivative {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n))
    (hi : ContDiffOn ℝ 2 e.symm e.target) (z : E k × E (n-k))
    (hz : z ∈ (physicalChart hk x0 P e).target) :
    fderiv ℝ (physicalChart hk x0 P e).symm z =
      P.toContinuousLinearMap.comp ((fderiv ℝ e.symm ((split hk).symm z)).comp
        (split hk).symm.toContinuousLinearMap) := by
  have hz' := (physicalChart_target hk x0 P e z).mp hz
  have hd := ((hi.contDiffAt (e.open_target.mem_nhds hz')).differentiableAt
    (by norm_num)).hasFDerivAt
  have h := ((P.hasFDerivAt.comp z (hd.comp z (split hk).symm.hasFDerivAt)).const_add x0)
  have hevent : ((physicalChart hk x0 P e).symm : (E k × E (n-k)) → X n) =ᶠ[𝓝 z]
      (fun w => x0 + P (e.symm ((split hk).symm w))) :=
    Filter.Eventually.of_forall (physicalChart_symm hk x0 P e)
  have h' : HasFDerivAt (physicalChart hk x0 P e).symm
      (P.toContinuousLinearMap.comp ((fderiv ℝ e.symm ((split hk).symm z)).comp
        (split hk).symm.toContinuousLinearMap)) z := h.congr_of_eventuallyEq hevent
  exact derivative_eq _ _ _ h'

theorem actual_source_pushed_height {n : ℕ} {L : ℝ} [Fact (0 < L)]
    (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (PhysicalSpectral.hessian (L := L) omega x0).det ≠ 0)
    (hcrit : fderiv ℝ (I4Source.sourceField n L omega) x0 = 0) :
    ∃ (k : ℕ) (hk : k ≤ n) (P : E n ≃L[ℝ] X n) (s : Sym n → Sym n)
      (e : OpenPartialHomeomorph (E n) (E n))
      (D : MorseCone.NormalForm (I4Torus.SourceTorus n L) (E k) (E (n-k))),
      let J := PhysicalSpectral.signSym n k
      let M := TaylorSymLift.sourceSymMatrix (L := L) omega x0 P.toContinuousLinearMap
      M 0 = J ∧ (∀ u, e u = theta J s M u) ∧
      e 0 = 0 ∧ e.symm 0 = 0 ∧ 0 ∈ e.source ∧ 0 ∈ e.target ∧
      HasFDerivAt e (ContinuousLinearMap.id ℝ (E n)) 0 ∧
      ContDiffOn ℝ 2 e e.source ∧ ContDiffOn ℝ 2 e.symm e.target ∧
      D.f = I4Torus.torusSourceField n L omega ∧
      D.p = I4Torus.torusProjection n L x0 ∧ D.c = I4Source.sourceField n L omega x0 ∧
      D.chart = (liftChart (L := L) x0).trans (physicalChart hk x0 P e) ∧
      (∀ q, D.chart q = split hk (e (P.symm (liftChart (L := L) x0 q - x0)))) ∧
      (∀ z, D.chart.symm z = I4Torus.torusProjection n L (x0 + P (e.symm ((split hk).symm z)))) ∧
      ContMDiffOn 𝓘(ℝ, X n) 𝓘(ℝ, E k × E (n-k)) 2 D.chart D.chart.source ∧
      ContMDiffOn 𝓘(ℝ, E k × E (n-k)) 𝓘(ℝ, X n) 2 D.chart.symm D.chart.target ∧
      LocalGeometry (I4Source.sourceField n L omega) (physicalChart hk x0 P e)
        D.chart.target ((physicalChart hk x0 P e).source ∩ (liftChart (L := L) x0).target)
        D.c x0 := by
  obtain ⟨k, hk, P, s, e, D, hM0, heq, he0, hi0, h0s, h0t, hd, heC, hiC,
    hf, hp, hc, hchart, happly, hsymm, hC, hCi⟩ :=
    actual_source_normal_form omega hmajor x0 hdet hcrit
  let phi := physicalChart hk x0 P e
  let a := liftChart (L := L) x0
  let T := D.chart.target
  let U := phi.source ∩ a.target
  have hT : IsOpen T := D.chart.open_target
  have hU : IsOpen U := phi.open_source.inter a.open_target
  have htarget : T = phi.target ∩ phi.symm ⁻¹' a.target := by
    change D.chart.target = _
    rw [hchart, OpenPartialHomeomorph.trans_target]
  have hsub : T ⊆ phi.target := by
    rw [htarget]
    exact inter_subset_left
  have hInv : MapsTo phi.symm T U := by
    intro z hz
    exact ⟨phi.map_target (hsub hz), (htarget ▸ hz).2⟩
  have hFor : MapsTo phi U T := by
    intro x hx
    rw [htarget]
    refine ⟨phi.map_source hx.1, ?_⟩
    change phi.symm (phi x) ∈ a.target
    simpa only [phi.left_inv hx.1] using hx.2
  obtain ⟨hphi, hpsi⟩ := physicalChart_C2 hk x0 P e heC hiC
  have hpsiT : ContDiffOn ℝ 2 phi.symm T := hpsi.mono hsub
  obtain ⟨hQ0, hQ1⟩ := pushed_C1 phi.symm T hT hpsiT
  have hphiU : ContDiffOn ℝ 1 phi U :=
    (hphi.of_le (by norm_num)).mono inter_subset_left
  have hPQ0 : ContDiffOn ℝ 1 ((Q0 phi.symm) ∘ phi) U := hQ0.comp hphiU hFor
  have hPQ1 : ContDiffOn ℝ 1 ((Q1 phi.symm) ∘ phi) U := hQ1.comp hphiU hFor
  have hheight : ∀ z ∈ T,
      I4Source.sourceField n L omega (phi.symm z) = D.c + MorseCone.quadratic z := by
    intro z hz
    have h := D.equation (D.chart.symm z) (D.chart.map_target hz)
    rw [D.chart.right_inv hz] at h
    have hps : D.chart.symm z = I4Torus.torusProjection n L (phi.symm z) := by
      simpa only [phi, physicalChart_symm] using hsymm z
    rw [hf, hps, I4Torus.torusSourceField_pullback] at h
    exact h
  have hF := I4DeterministicC4.sourceField_contDiff_of_majorant n
    (Fact.out : 0 < L).ne' omega hmajor
  have hrates := rates_of_local_identity (I4Source.sourceField n L omega) phi.symm T D.c hT
    (hF.differentiable (by norm_num)) hpsiT hheight
  have ht0 : (0 : E k × E (n-k)) ∈ T := by
    simpa only [D.center_eq] using D.chart.map_source D.center_mem
  have hforward0 : phi x0 = 0 := by
    simp [phi, physicalChart_apply, he0]
  have hinverse0 : phi.symm 0 = x0 := by
    simp [phi, physicalChart_symm, hi0]
  have hgeo : LocalGeometry (I4Source.sourceField n L omega) phi T U D.c x0 :=
    { target_open := hT
      physical_open := hU
      target_subset := hsub
      inverse_target := hInv
      forward_target := hFor
      forward_C2 := hphi
      inverse_C2 := hpsi
      push0_C1 := hQ0
      push1_C1 := hQ1
      physical0_C1 := hPQ0
      physical1_C1 := hPQ1
      height := hheight
      rate0 := fun z hz => (hrates z hz).1
      rate1 := fun z hz => (hrates z hz).2
      center_target := ht0
      center_forward := hforward0
      center_inverse := hinverse0
      center_push0 := by simp only [Q0, W0, Prod.snd_zero, neg_zero,
        Prod.mk_zero_zero, map_zero]
      center_push1 := by simp only [Q1, W1, Prod.fst_zero, Prod.snd_zero, neg_zero,
        Prod.mk_zero_zero, map_zero] }
  exact ⟨k, hk, P, s, e, D, hM0, heq, he0, hi0, h0s, h0t, hd, heC, hiC,
    hf, hp, hc, hchart, happly, hsymm, hC, hCi, hgeo⟩

end SourcePushedHeight
