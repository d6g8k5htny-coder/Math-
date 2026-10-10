import PushedHeight
import Mathlib.Analysis.Calculus.BumpFunction.InnerProduct
import Mathlib.Topology.Algebra.Support

noncomputable section
#eval IO.eprintln "BOUNDARY imports"
set_option backward.isDefEq.respectTransparency false
open Filter Set SourceCoordinates SourceNormalForm SourcePushedHeight
open MorseCongruence
open scoped Topology ContDiff Manifold Matrix.Norms.Frobenius
namespace SourceCompactCutoff
attribute [local instance] I4TorusC4.actualChartedSpace
attribute [local instance] Classical.propDecidable

def cutoffBump {n : ℕ} (ρ : ℝ) (hρ : 0 < ρ) : ContDiffBump (0 : E n) :=
  ⟨ρ/4, ρ/2, by linarith, by linarith⟩


#eval IO.eprintln "BOUNDARY bump"
def beta {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ) (z : E k × E (n-k)) : ℝ :=
  cutoffBump (n := n) ρ hρ ((split hk).symm z)

def K {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) : Set (E k × E (n-k)) :=
  split hk '' Metric.closedBall 0 (ρ/2)

def M {n k : ℕ} (hk : k ≤ n) (ρ : ℝ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) : Set (X n) :=
  phi.symm '' K hk ρ

def extension {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n))
    (Q : (E k × E (n-k)) → X n) (x : X n) : X n :=
  if x ∈ U then beta hk ρ hρ (phi x) • Q (phi x) else 0

def V0 {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n)) : X n → X n :=
  extension hk ρ hρ phi U (Q0 phi.symm)

def V1 {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n)) : X n → X n :=
  extension hk ρ hρ phi U (Q1 phi.symm)


#eval IO.eprintln "BOUNDARY defs"
structure CompactGeometry {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (x0 : X n) : Prop where
  inner_one : ∀ z, ‖(split hk).symm z‖ ≤ ρ/4 → beta hk ρ hρ z = 1
  outer_zero : ∀ z, ρ/2 ≤ ‖(split hk).symm z‖ → beta hk ρ hρ z = 0
  beta_bounds : ∀ z, 0 ≤ beta hk ρ hρ z ∧ beta hk ρ hρ z ≤ 1
  compact_K : IsCompact (K hk ρ)
  compact_M : IsCompact (M hk ρ phi)
  K_target : K hk ρ ⊆ T
  M_physical : M hk ρ phi ⊆ U
  support0 : Function.support (V0 hk ρ hρ phi U) ⊆ M hk ρ phi
  support1 : Function.support (V1 hk ρ hρ phi U) ⊆ M hk ρ phi
  C1_0 : ContDiff ℝ 1 (V0 hk ρ hρ phi U)
  C1_1 : ContDiff ℝ 1 (V1 hk ρ hρ phi U)
  compact0 : HasCompactSupport (V0 hk ρ hρ phi U)
  compact1 : HasCompactSupport (V1 hk ρ hρ phi U)
  rate0 : ∀ x, fderiv ℝ F x (V0 hk ρ hρ phi U x) =
    if x ∈ U then beta hk ρ hρ (phi x) * (2 * ‖(phi x).2‖^2) else 0
  rate1 : ∀ x, fderiv ℝ F x (V1 hk ρ hρ phi U x) =
    if x ∈ U then beta hk ρ hρ (phi x) * (2 * (‖(phi x).1‖^2 + ‖(phi x).2‖^2)) else 0
  nonnegative0 : ∀ x, 0 ≤ fderiv ℝ F x (V0 hk ρ hρ phi U x)
  nonnegative1 : ∀ x, 0 ≤ fderiv ℝ F x (V1 hk ρ hρ phi U x)
  inner_rate0 : ∀ z, ‖(split hk).symm z‖ ≤ ρ/4 →
    fderiv ℝ F (phi.symm z) (V0 hk ρ hρ phi U (phi.symm z)) = 2 * ‖z.2‖^2
  inner_rate1 : ∀ z, ‖(split hk).symm z‖ ≤ ρ/4 →
    fderiv ℝ F (phi.symm z) (V1 hk ρ hρ phi U (phi.symm z)) =
      2 * (‖z.1‖^2 + ‖z.2‖^2)
  center0 : V0 hk ρ hρ phi U x0 = 0
  center1 : V1 hk ρ hρ phi U x0 = 0


#eval IO.eprintln "BOUNDARY structure"
private theorem compact_K_of_split {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) :
    IsCompact (K hk ρ) := by
  change IsCompact ((split hk) '' Metric.closedBall 0 (ρ / 2))
  exact (isCompact_closedBall (0 : E n) (ρ / 2)).image
    (split hk).continuous

private theorem K_subset_radiusBall {n k : ℕ} (hk : k ≤ n) (ρ : ℝ)
    (hρ : 0 < ρ) : K hk ρ ⊆ MorseCone.radiusBall ρ := by
  rintro z ⟨u, hu, rfl⟩
  have hu' : ‖u‖ ≤ ρ / 2 := by
    simpa only [Metric.mem_closedBall, dist_zero_right] using hu
  have hhalf : 0 ≤ ρ / 2 := by linarith
  have hsq : ‖u‖ ^ 2 ≤ (ρ / 2) ^ 2 :=
    (sq_le_sq₀ (norm_nonneg u) hhalf).mpr hu'
  change ‖(split hk u).1‖ ^ 2 + ‖(split hk u).2‖ ^ 2 < ρ ^ 2
  rw [← split_energy hk u]
  nlinarith

private theorem support_extension {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n))
    (Q : (E k × E (n-k)) → X n) (hsource : U ⊆ phi.source)
    (houter : ∀ z, ρ / 2 ≤ ‖(split hk).symm z‖ → beta hk ρ hρ z = 0) :
    Function.support (extension hk ρ hρ phi U Q) ⊆ M hk ρ phi := by
  intro x hx
  change extension hk ρ hρ phi U Q x ≠ 0 at hx
  have hxU : x ∈ U := by
    by_contra h
    simp [extension, h] at hx
  have hb : beta hk ρ hρ (phi x) ≠ 0 := by
    intro h
    simp [extension, hxU, h] at hx
  have hlt : ‖(split hk).symm (phi x)‖ < ρ / 2 := by
    by_contra h
    exact hb (houter _ (le_of_not_gt h))
  have hK : phi x ∈ K hk ρ := by
    refine ⟨(split hk).symm (phi x), ?_, (split hk).apply_symm_apply (phi x)⟩
    simpa only [Metric.mem_closedBall, dist_zero_right] using le_of_lt hlt
  exact ⟨phi x, hK, phi.left_inv (hsource hxU)⟩

private theorem contDiff_extension {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k))) (U : Set (X n))
    (Q : (E k × E (n-k)) → X n) (hU : IsOpen U)
    (hphi : ContDiffOn ℝ 1 phi U) (hQ : ContDiffOn ℝ 1 (Q ∘ phi) U)
    (hM : IsCompact (M hk ρ phi)) (hMU : M hk ρ phi ⊆ U)
    (hsupport : Function.support (extension hk ρ hρ phi U Q) ⊆ M hk ρ phi) :
    ContDiff ℝ 1 (extension hk ρ hρ phi U Q) := by
  have hb : ContDiff ℝ 1 (beta hk ρ hρ) := by
    unfold beta
    exact (cutoffBump ρ hρ).contDiff.comp (split hk).symm.contDiff
  have hlocal : ContDiffOn ℝ 1 (extension hk ρ hρ phi U Q) U := by
    have hbeta : ContDiffOn ℝ 1 (fun x => beta hk ρ hρ (phi x)) U :=
      hb.comp_contDiffOn hphi
    apply (hbeta.smul hQ).congr
    intro x hx
    simp [extension, hx]
  rw [contDiff_iff_contDiffAt]
  intro x
  by_cases hx : x ∈ U
  · exact hlocal.contDiffAt (hU.mem_nhds hx)
  · have hxM : x ∉ M hk ρ phi := fun h => hx (hMU h)
    have hzero : extension hk ρ hρ phi U Q =ᶠ[𝓝 x] (fun _ => (0 : X n)) :=
      (hM.isClosed.isOpen_compl.mem_nhds hxM).mono (by
        intro y hy
        by_contra hn
        exact hy (hsupport hn))
    exact (contDiff_const : ContDiff ℝ 1 (fun _ : X n => (0 : X n))).contDiffAt.congr_of_eventuallyEq hzero

private theorem extension_rate {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n))
    (Q : (E k × E (n-k)) → X n) (R : (E k × E (n-k)) → ℝ)
    (hsource : U ⊆ phi.source) (hforward : MapsTo phi U T)
    (hrate : ∀ z ∈ T, fderiv ℝ F (phi.symm z) (Q z) = R z) :
    ∀ x, fderiv ℝ F x (extension hk ρ hρ phi U Q x) =
      if x ∈ U then beta hk ρ hρ (phi x) * R (phi x) else 0 := by
  intro x
  by_cases hx : x ∈ U
  · have hr := hrate (phi x) (hforward hx)
    rw [phi.left_inv (hsource hx)] at hr
    simp only [extension, if_pos hx, map_smul, smul_eq_mul]
    rw [hr]
  · simp [extension, hx]

theorem compact_cutoff_of_geometry {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (c : ℝ) (x0 : X n)
    (hgeo : LocalGeometry F phi T U c x0) (hsource : U ⊆ phi.source)
    (hrad : MorseCone.radiusBall ρ ⊆ T) : CompactGeometry hk ρ hρ F phi T U x0 := by
  have hK : IsCompact (K hk ρ) := compact_K_of_split hk ρ
  have hKT : K hk ρ ⊆ T := (K_subset_radiusBall hk ρ hρ).trans hrad
  have hM : IsCompact (M hk ρ phi) :=
    hK.image_of_continuousOn (phi.continuousOn_symm.mono (hKT.trans hgeo.target_subset))
  have hMU : M hk ρ phi ⊆ U := by
    rintro x ⟨z, hz, rfl⟩
    exact hgeo.inverse_target (hKT hz)
  have hinner : ∀ z, ‖(split hk).symm z‖ ≤ ρ / 4 → beta hk ρ hρ z = 1 := by
    intro z hz
    change (cutoffBump ρ hρ) ((split hk).symm z) = 1
    apply (cutoffBump ρ hρ).one_of_mem_closedBall
    simpa only [cutoffBump, Metric.mem_closedBall, dist_zero_right] using hz
  have houter : ∀ z, ρ / 2 ≤ ‖(split hk).symm z‖ → beta hk ρ hρ z = 0 := by
    intro z hz
    change (cutoffBump ρ hρ) ((split hk).symm z) = 0
    apply (cutoffBump ρ hρ).zero_of_le_dist
    simpa only [cutoffBump, dist_zero_right] using hz
  have hs0 : Function.support (V0 hk ρ hρ phi U) ⊆ M hk ρ phi :=
    support_extension hk ρ hρ phi U (Q0 phi.symm) hsource houter
  have hs1 : Function.support (V1 hk ρ hρ phi U) ⊆ M hk ρ phi :=
    support_extension hk ρ hρ phi U (Q1 phi.symm) hsource houter
  have hphi : ContDiffOn ℝ 1 phi U :=
    (hgeo.forward_C2.of_le (by norm_num)).mono hsource
  have hC0 : ContDiff ℝ 1 (V0 hk ρ hρ phi U) :=
    contDiff_extension hk ρ hρ phi U (Q0 phi.symm) hgeo.physical_open
      hphi hgeo.physical0_C1 hM hMU hs0
  have hC1 : ContDiff ℝ 1 (V1 hk ρ hρ phi U) :=
    contDiff_extension hk ρ hρ phi U (Q1 phi.symm) hgeo.physical_open
      hphi hgeo.physical1_C1 hM hMU hs1
  have hr0 : ∀ x, fderiv ℝ F x (V0 hk ρ hρ phi U x) =
      if x ∈ U then beta hk ρ hρ (phi x) * (2 * ‖(phi x).2‖ ^ 2) else 0 :=
    extension_rate hk ρ hρ F phi T U (Q0 phi.symm)
      (fun z => 2 * ‖z.2‖ ^ 2) hsource hgeo.forward_target hgeo.rate0
  have hr1 : ∀ x, fderiv ℝ F x (V1 hk ρ hρ phi U x) =
      if x ∈ U then beta hk ρ hρ (phi x) *
        (2 * (‖(phi x).1‖ ^ 2 + ‖(phi x).2‖ ^ 2)) else 0 :=
    extension_rate hk ρ hρ F phi T U (Q1 phi.symm)
      (fun z => 2 * (‖z.1‖ ^ 2 + ‖z.2‖ ^ 2)) hsource hgeo.forward_target hgeo.rate1
  have hcenter : x0 ∈ U := by
    simpa only [hgeo.center_inverse] using hgeo.inverse_target hgeo.center_target
  have hinnerT : ∀ z, ‖(split hk).symm z‖ ≤ ρ / 4 → z ∈ T := by
    intro z hz
    have hle : ‖(split hk).symm z‖ ≤ ρ / 2 := by linarith
    have hzK : z ∈ K hk ρ := by
      refine ⟨(split hk).symm z, ?_, (split hk).apply_symm_apply z⟩
      simpa only [Metric.mem_closedBall, dist_zero_right] using hle
    exact hKT hzK
  have hinnerU : ∀ z, ‖(split hk).symm z‖ ≤ ρ / 4 → phi.symm z ∈ U :=
    fun z hz => hgeo.inverse_target (hinnerT z hz)
  refine {
    inner_one := hinner
    outer_zero := houter
    beta_bounds := fun z =>
      ⟨(cutoffBump ρ hρ).nonneg' ((split hk).symm z),
        (cutoffBump ρ hρ).le_one (x := (split hk).symm z)⟩
    compact_K := hK
    compact_M := hM
    K_target := hKT
    M_physical := hMU
    support0 := hs0
    support1 := hs1
    C1_0 := hC0
    C1_1 := hC1
    compact0 := hM.closure_of_subset hs0
    compact1 := hM.closure_of_subset hs1
    rate0 := hr0
    rate1 := hr1
    nonnegative0 := by
      intro x
      rw [hr0]
      split_ifs with hx
      · exact mul_nonneg ((cutoffBump ρ hρ).nonneg' ((split hk).symm (phi x)))
          (by positivity)
      · exact le_refl 0
    nonnegative1 := by
      intro x
      rw [hr1]
      split_ifs with hx
      · exact mul_nonneg ((cutoffBump ρ hρ).nonneg' ((split hk).symm (phi x)))
          (by positivity)
      · exact le_refl 0
    inner_rate0 := by
      intro z hz
      have hxU := hinnerU z hz
      rw [hr0, if_pos hxU, phi.right_inv (hgeo.target_subset (hinnerT z hz)),
        hinner z hz]
      ring
    inner_rate1 := by
      intro z hz
      have hxU := hinnerU z hz
      rw [hr1, if_pos hxU,
        phi.right_inv (hgeo.target_subset (hinnerT z hz)), hinner z hz]
      ring
    center0 := by
      simp [V0, extension, hcenter, hgeo.center_forward, hgeo.center_push0]
    center1 := by
      simp [V1, extension, hcenter, hgeo.center_forward, hgeo.center_push1] }


#eval IO.eprintln "BOUNDARY generic-target"
theorem actual_source_compact_cutoff {n : ℕ} {L : ℝ} [Fact (0 < L)]
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
        D.c x0 ∧
      CompactGeometry hk D.ρ D.hρ (I4Source.sourceField n L omega)
        (physicalChart hk x0 P e) D.chart.target
        ((physicalChart hk x0 P e).source ∩ (liftChart (L := L) x0).target) x0 := by
  obtain ⟨k, hk, P, s, e, D, hM0, heq, he0, hi0, h0s, h0t, hd, heC, hiC,
    hf, hp, hc, hchart, happly, hsymm, hC, hCi, hgeo⟩ :=
    actual_source_pushed_height omega hmajor x0 hdet hcrit
  refine ⟨k, hk, P, s, e, D, hM0, heq, he0, hi0, h0s, h0t, hd, heC, hiC,
    hf, hp, hc, hchart, happly, hsymm, hC, hCi, hgeo, ?_⟩
  exact compact_cutoff_of_geometry hk D.ρ D.hρ (I4Source.sourceField n L omega)
    (physicalChart hk x0 P e) D.chart.target
    ((physicalChart hk x0 P e).source ∩ (liftChart (L := L) x0).target)
    D.c x0 hgeo inter_subset_left D.ball_target


#eval IO.eprintln "BOUNDARY actual-target"
end SourceCompactCutoff
