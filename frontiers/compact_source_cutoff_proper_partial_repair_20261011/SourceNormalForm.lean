import SourceCoordinates
import ConeFootprint
import SourceTorusC4
import Mathlib.Geometry.Manifold.ContMDiff.Atlas
import Mathlib.Topology.OpenPartialHomeomorph.Composition

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Filter Set Matrix SourceCoordinates MorseCongruence ChartedSpace IsManifold
open scoped Topology ContDiff Manifold Matrix.Norms.Frobenius
namespace SourceNormalForm
attribute [local instance] I4TorusC4.actualChartedSpace

def split {n k : ℕ} (hk : k ≤ n) : E n ≃L[ℝ] E k × E (n-k) :=
  (LinearIsometryEquiv.piLpCongrLeft 2 ℝ ℝ
    (finCongr (Nat.add_sub_of_le hk).symm)).toContinuousLinearEquiv.trans
    EuclideanSpace.finAddEquivProd

theorem split_fst {n k : ℕ} (hk : k ≤ n) (u : E n) (i : Fin k) :
    (split hk u).1 i = u (Fin.cast (Nat.add_sub_of_le hk) (Fin.castAdd (n-k) i)) := rfl

theorem split_snd {n k : ℕ} (hk : k ≤ n) (u : E n) (i : Fin (n-k)) :
    (split hk u).2 i = u (Fin.cast (Nat.add_sub_of_le hk) (Fin.natAdd k i)) := rfl

theorem split_energy {n k : ℕ} (hk : k ≤ n) (u : E n) :
    ‖u‖^2 = ‖(split hk u).1‖^2 + ‖(split hk u).2‖^2 := by
  rw [EuclideanSpace.real_norm_sq_eq, EuclideanSpace.real_norm_sq_eq,
    EuclideanSpace.real_norm_sq_eq]
  rw [← Fin.sum_congr' (fun i : Fin n => u i ^ 2) (Nat.add_sub_of_le hk)]
  exact Fin.sum_univ_add _

theorem split_quadratic {n k : ℕ} (hk : k ≤ n) (u : E n) :
    quadratic (PhysicalSpectral.signMatrix n k) u = MorseCone.quadratic (split hk u) := by
  rw [quadratic_eq_dot]
  simp only [PhysicalSpectral.signMatrix, dotProduct, Matrix.mulVec_diagonal]
  rw [← Fin.sum_congr' (fun i : Fin n => u i * ((if i.val < k then (1 : ℝ) else -1) * u i))
    (Nat.add_sub_of_le hk), Fin.sum_univ_add]
  simp only [MorseCone.quadratic, EuclideanSpace.real_norm_sq_eq, sub_eq_add_neg,
    ← Finset.sum_neg_distrib]
  congr 1
  · apply Finset.sum_congr rfl
    intro i _
    simp [split_fst, pow_two, i.isLt]
  · apply Finset.sum_congr rfl
    intro i _
    have hn : ¬ k + i.val < k := by omega
    simp [split_snd, pow_two, hn]

def physicalChart {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n)) :=
  (((Homeomorph.subRight x0).toOpenPartialHomeomorph.trans
    P.symm.toHomeomorph.toOpenPartialHomeomorph).trans e).trans
    (split hk).toHomeomorph.toOpenPartialHomeomorph

theorem physicalChart_apply {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n)) (x : X n) :
    physicalChart hk x0 P e x = split hk (e (P.symm (x-x0))) := rfl

theorem physicalChart_symm {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n)) (z : E k × E (n-k)) :
    (physicalChart hk x0 P e).symm z = x0 + P (e.symm ((split hk).symm z)) := by
  change P (e.symm ((split hk).symm z)) + x0 = _
  exact add_comm _ _

theorem physicalChart_source {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n)) (x : X n) :
    x ∈ (physicalChart hk x0 P e).source ↔ P.symm (x-x0) ∈ e.source := by
  simp [physicalChart]

theorem physicalChart_target {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n)) (z : E k × E (n-k)) :
    z ∈ (physicalChart hk x0 P e).target ↔ (split hk).symm z ∈ e.target := by
  simp [physicalChart]

theorem physicalChart_C2 {n k : ℕ} (hk : k ≤ n) (x0 : X n)
    (P : E n ≃L[ℝ] X n) (e : OpenPartialHomeomorph (E n) (E n))
    (he : ContDiffOn ℝ 2 e e.source) (hi : ContDiffOn ℝ 2 e.symm e.target) :
    ContDiffOn ℝ 2 (physicalChart hk x0 P e) (physicalChart hk x0 P e).source ∧
    ContDiffOn ℝ 2 (physicalChart hk x0 P e).symm (physicalChart hk x0 P e).target := by
  constructor
  · change ContDiffOn ℝ 2 (fun x => split hk (e (P.symm (x-x0)))) _
    apply (split hk).contDiff.comp_contDiffOn
    apply he.comp (P.symm.contDiff.comp (contDiff_id.sub contDiff_const)).contDiffOn
    intro x hx
    exact (physicalChart_source hk x0 P e x).mp hx
  · have h := hi.comp (split hk).symm.contDiff.contDiffOn
      (fun z hz => (physicalChart_target hk x0 P e z).mp hz)
    have h' : ContDiffOn ℝ 2 (fun z => x0 + P (e.symm ((split hk).symm z)))
        (physicalChart hk x0 P e).target := contDiffOn_const.add (P.contDiff.comp_contDiffOn h)
    have heq : ((physicalChart hk x0 P e).symm : (E k × E (n-k)) → X n) =
        (fun z => x0 + P (e.symm ((split hk).symm z))) := funext (physicalChart_symm hk x0 P e)
    rw [heq]
    exact h'

def liftChart {n : ℕ} {L : ℝ} [Fact (0 < L)] (x0 : X n) :=
  I4TorusC4.quotientChart n L (fun i => x0 i - L/2)

theorem liftChart_center {n : ℕ} {L : ℝ} [Fact (0 < L)] (x0 : X n) :
    x0 ∈ (liftChart (L := L) x0).target ∧
    I4Torus.torusProjection n L x0 ∈ (liftChart (L := L) x0).source ∧
    liftChart (L := L) x0 (I4Torus.torusProjection n L x0) = x0 := by
  have ht : x0 ∈ (liftChart (L := L) x0).target := by
    change x0 ∈ Set.pi Set.univ (fun i => Set.Ioo (x0 i - L/2) (x0 i - L/2 + L))
    intro i _
    have hL : 0 < L := Fact.out
    constructor <;> linarith
  exact ⟨ht, (liftChart (L := L) x0).map_target ht, (liftChart (L := L) x0).right_inv ht⟩

theorem liftChart_C2 {n : ℕ} {L : ℝ} [Fact (0 < L)] (x0 : X n) :
    ContMDiffOn 𝓘(ℝ, X n) 𝓘(ℝ, X n) 2 (liftChart (L := L) x0) (liftChart (L := L) x0).source ∧
    ContMDiffOn 𝓘(ℝ, X n) 𝓘(ℝ, X n) 2 (liftChart (L := L) x0).symm (liftChart (L := L) x0).target := by
  let := I4TorusC4.torus_isManifold n L
  have ha : liftChart (L := L) x0 ∈ maximalAtlas 𝓘(ℝ, X n) 2 (I4Torus.SourceTorus n L) := by
    apply IsManifold.subset_maximalAtlas
    exact ⟨(fun i => x0 i - L/2), rfl⟩
  exact ⟨contMDiffOn_of_mem_maximalAtlas ha, contMDiffOn_symm_of_mem_maximalAtlas ha⟩

theorem radiusBall_subset_ball {k m : ℕ} {ρ : ℝ} (hρ : 0 < ρ) :
    MorseCone.radiusBall (E := E k) (F := E m) ρ ⊆ Metric.ball 0 ρ := by
  intro z hz
  change ‖z.1‖^2 + ‖z.2‖^2 < ρ^2 at hz
  rw [Metric.mem_ball, dist_zero_right, Prod.norm_def, max_lt_iff]
  constructor
  · apply (sq_lt_sq₀ (norm_nonneg _) hρ.le).mp
    nlinarith [sq_nonneg ‖z.2‖]
  · apply (sq_lt_sq₀ (norm_nonneg _) hρ.le).mp
    nlinarith [sq_nonneg ‖z.1‖]

theorem actual_source_normal_form {n : ℕ} {L : ℝ} [Fact (0 < L)]
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
      ContMDiffOn 𝓘(ℝ, E k × E (n-k)) 𝓘(ℝ, X n) 2 D.chart.symm D.chart.target := by
  obtain ⟨k, hk, P, V, s, e, hM0, hV, hJV, hs0, hs, heq, he0, hi0, h0s, h0t,
    hd, heC, hiC, hf, hi⟩ := source_coordinates (Fact.out : 0 < L).ne' omega hmajor x0 hdet hcrit
  let a := liftChart (L := L) x0
  let b := physicalChart hk x0 P e
  let c := a.trans b
  obtain ⟨hat, has, hac⟩ := liftChart_center (L := L) x0
  have hbs : x0 ∈ b.source := by
    apply (physicalChart_source hk x0 P e x0).mpr
    simpa using h0s
  have hb0 : b x0 = 0 := by
    simp [b, physicalChart_apply, he0]
  have hcs : I4Torus.torusProjection n L x0 ∈ c.source := by
    refine ⟨has, ?_⟩
    change a (I4Torus.torusProjection n L x0) ∈ b.source
    simpa only [a, hac] using hbs
  have hc0 : c (I4Torus.torusProjection n L x0) = 0 := by
    change b (a (I4Torus.torusProjection n L x0)) = 0
    simpa only [a, hac] using hb0
  have hct : (0 : E k × E (n-k)) ∈ c.target := by
    simpa only [hc0] using c.map_source hcs
  obtain ⟨ρ, hρ, hr⟩ := Metric.mem_nhds_iff.mp (c.open_target.mem_nhds hct)
  have energy : ∀ q ∈ c.source, I4Torus.torusSourceField n L omega q =
      I4Source.sourceField n L omega x0 + MorseCone.quadratic (c q) := by
    intro q hq
    have hq' : a q ∈ b.source := hq.2
    have hu := (physicalChart_source hk x0 P e (a q)).mp hq'
    have he := (hf (P.symm (a q - x0)) hu).2
    have hxx : x0 + P (P.symm (a q - x0)) = a q := by simp
    rw [hxx] at he
    have ht : I4Torus.torusSourceField n L omega q = I4Source.sourceField n L omega (a q) := by
      rw [← I4Torus.torusSourceField_pullback n L omega (a q)]
      congr 1
      exact (a.left_inv hq.1).symm
    rw [ht, he]
    exact congrArg (fun v => I4Source.sourceField n L omega x0 + v)
      (split_quadratic hk (e (P.symm (a q - x0))))
  let D : MorseCone.NormalForm (I4Torus.SourceTorus n L) (E k) (E (n-k)) :=
    { f := I4Torus.torusSourceField n L omega
      p := I4Torus.torusProjection n L x0
      c := I4Source.sourceField n L omega x0
      ρ := ρ
      hρ := hρ
      chart := c
      center_mem := hcs
      center_eq := hc0
      ball_target := (radiusBall_subset_ball hρ).trans hr
      equation := energy }
  obtain ⟨haC, haiC⟩ := liftChart_C2 (L := L) x0
  obtain ⟨hbC, hbiC⟩ := physicalChart_C2 hk x0 P e heC hiC
  have hcC : ContMDiffOn 𝓘(ℝ, X n) 𝓘(ℝ, E k × E (n-k)) 2 c c.source :=
    hbC.contMDiffOn.comp' haC
  have hciC : ContMDiffOn 𝓘(ℝ, E k × E (n-k)) 𝓘(ℝ, X n) 2 c.symm c.target :=
    haiC.comp' hbiC.contMDiffOn
  refine ⟨k, hk, P, s, e, D, hM0, heq, he0, hi0, h0s, h0t, hd, heC, hiC,
    rfl, rfl, rfl, rfl, (fun _ => rfl), ?_, hcC, hciC⟩
  intro z
  change I4Torus.torusProjection n L (b.symm z) = _
  rw [physicalChart_symm]

end SourceNormalForm
