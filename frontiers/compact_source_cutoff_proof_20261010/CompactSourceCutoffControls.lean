import CompactSourceCutoffProof
import Mathlib.Topology.Order.IntermediateValue

/-!
Static falsifying controls for the compact source cutoff.  This file has not been
elaborated.  It deliberately consumes the actual `CompactGeometry` conclusion;
the final theorem also consumes the literal actual-source theorem and retains its
original premises.  No toy quadratic is identified with the Gaussian source.
-/

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Set SourceCoordinates SourceNormalForm SourcePushedHeight SourceCompactCutoff MorseCongruence
open scoped Topology ContDiff Manifold Matrix.Norms.Frobenius
namespace CompactSourceCutoffControls
attribute [local instance] Classical.propDecidable
attribute [local instance] I4TorusC4.actualChartedSpace

theorem actual_beta_at_zero {n k : ℕ} (hk : k ≤ n)
    (ρ : ℝ) (hρ : 0 < ρ) : beta hk ρ hρ 0 = 1 := by
  change (cutoffBump ρ hρ) ((split hk).symm 0) = 1
  apply (cutoffBump ρ hρ).one_of_mem_closedBall
  simp only [map_zero, Metric.mem_closedBall, dist_self]
  linarith

/- The closed inner and outer boundaries belong to opposite plateaus. -/
theorem boundary_plateaus {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (x0 : X n)
    (g : CompactGeometry hk ρ hρ F phi T U x0) :
    beta hk ρ hρ 0 = 1 ∧
    (∀ z, ‖(split hk).symm z‖ = ρ / 4 → beta hk ρ hρ z = 1) ∧
    (∀ z, ρ / 2 ≤ ‖(split hk).symm z‖ → beta hk ρ hρ z = 0) := by
  refine ⟨?_, ?_, g.outer_zero⟩
  · apply g.inner_one
    simp only [map_zero, norm_zero]
    linarith
  · intro z hz
    exact g.inner_one z hz.le

/- The separation is stated in the actual split product with its max norm.
The two one-dimensional norms are explicit premises, so the argument also
applies to any witnessed point with those coordinates. -/
theorem euclidean_outer_product_inner {n k : ℕ} (hk : k ≤ n)
    (z : E k × E (n-k)) (hplus : ‖z.1‖ = (3 : ℝ) / 8)
    (hminus : ‖z.2‖ = (3 : ℝ) / 8) :
    ‖z‖ < (1 : ℝ) / 2 ∧
    (1 : ℝ) / 2 ≤ ‖(split hk).symm z‖ := by
  have henergy := split_energy hk ((split hk).symm z)
  rw [(split hk).apply_symm_apply] at henergy
  have hnorm : 0 ≤ ‖(split hk).symm z‖ := norm_nonneg _
  constructor
  · simpa [Prod.norm_def, hplus, hminus] using
      (show max ((3 : ℝ) / 8) (3 / 8) < 1 / 2 by norm_num)
  · rw [hplus, hminus] at henergy
    nlinarith

theorem product_max_substitution_rejected {n k : ℕ} (hk : k ≤ n)
    (z : E k × E (n-k)) (hplus : ‖z.1‖ = (3 : ℝ) / 8)
    (hminus : ‖z.2‖ = (3 : ℝ) / 8) :
    ‖z‖ < (1 : ℝ) / 2 ∧ beta hk 1 (by norm_num) z = 0 := by
  obtain ⟨hmax, houter⟩ := euclidean_outer_product_inner hk z hplus hminus
  refine ⟨hmax, ?_⟩
  change (cutoffBump 1 (by norm_num)) ((split hk).symm z) = 0
  exact (cutoffBump 1 (by norm_num)).zero_of_le_dist
    (by simpa only [cutoffBump, dist_zero_right] using houter)

private def axis (t : ℝ) : E 1 := EuclideanSpace.single (0 : Fin 1) t

private theorem axis_norm (t : ℝ) : ‖axis t‖ = |t| := by
  simp [axis, EuclideanSpace.norm_single, Real.norm_eq_abs]

private def corner : E 1 × E 1 := (axis (3/8), axis (3/8))

theorem concrete_n2_k1_product_max_rejected :
    ‖corner‖ < (1 : ℝ) / 2 ∧
    beta (by decide : 1 ≤ 2) 1 (by norm_num) corner = 0 := by
  apply product_max_substitution_rejected (by decide : 1 ≤ 2)
  · norm_num [corner, axis_norm]
  · norm_num [corner, axis_norm]

/- Uncompiled integration fragment. Place inside the controls namespace after its opens.
   `import Mathlib.Topology.Order.IntermediateValue` may be needed explicitly.
   The unit-vector argument is a real witness, not an assumed beta midpoint. -/

private theorem intermediate_beta_of_unit {n k : ℕ} (hk : k ≤ n)
    (ρ : ℝ) (hρ : 0 < ρ) (w : E n) (hw : ‖w‖ = 1) :
    ∃ t ∈ Set.Ioo (ρ / 4) (ρ / 2),
      beta hk ρ hρ (split hk (t • w)) = (1 : ℝ) / 2 := by
  let a : ℝ := ρ / 4
  let b : ℝ := ρ / 2
  let B := cutoffBump (n := n) ρ hρ
  let f : ℝ → ℝ := fun t => B (t • w)
  have ha0 : 0 ≤ a := by dsimp [a]; linarith
  have hb0 : 0 ≤ b := by dsimp [b]; linarith
  have hab : a ≤ b := by dsimp [a, b]; linarith
  have hnorm (t : ℝ) (ht : 0 ≤ t) : ‖t • w‖ = t := by
    simp [norm_smul, Real.norm_eq_abs, abs_of_nonneg ht, hw]
  have ha : f a = 1 := by
    change B (a • w) = 1
    apply B.one_of_mem_closedBall
    change dist (a • w) 0 ≤ ρ / 4
    simpa [dist_zero_right, hnorm a ha0, a]
  have hb : f b = 0 := by
    change B (b • w) = 0
    apply B.zero_of_le_dist
    change ρ / 2 ≤ dist (b • w) 0
    simpa [dist_zero_right, hnorm b hb0, b]
  have hf : Continuous f := by
    exact B.continuous.comp (continuous_id.smul continuous_const)
  have hmid : (1 / 2 : ℝ) ∈ Set.Ioo (f b) (f a) := by
    change f b < 1 / 2 ∧ 1 / 2 < f a
    rw [hb, ha]
    norm_num
  obtain ⟨t, ht, hft⟩ := intermediate_value_Ioo' hab hf.continuousOn hmid
  refine ⟨t, by simpa [a, b] using ht, ?_⟩
  change B ((split hk).symm (split hk (t • w))) = (1 : ℝ) / 2
  simpa only [(split hk).symm_apply_apply] using hft

/- Concrete n=2, k=1 instantiation; `E 2 = EuclideanSpace ℝ (Fin 2)`.
   This second theorem supplies the unit vector rather than adding it as a
   premise to the falsifying control. -/
private theorem intermediate_beta_n2_k1 :
    ∃ t ∈ Set.Ioo ((1 : ℝ) / 4) (1 / 2),
      beta (by decide : 1 ≤ 2) 1 (by norm_num)
        (split (by decide : 1 ≤ 2)
          (t • (EuclideanSpace.single (0 : Fin 2) (1 : ℝ) : E 2))) = 1 / 2 := by
  have hw : ‖(EuclideanSpace.single (0 : Fin 2) (1 : ℝ) : E 2)‖ = 1 := by
    simp [EuclideanSpace.norm_single]
  simpa using intermediate_beta_of_unit (by decide : 1 ≤ 2)
    (1 : ℝ) (by norm_num) _ hw

private def identityCone : MorseCone.NormalForm (E 1 × E 1) (E 1) (E 1) where
  f := MorseCone.quadratic
  p := 0
  c := 0
  ρ := 1
  hρ := by norm_num
  chart := (Homeomorph.refl (E 1 × E 1)).toOpenPartialHomeomorph
  center_mem := by simp
  center_eq := rfl
  ball_target := by intro z hz; simp
  equation := by intro z hz; simp

private def annulusCoordinate : E 1 × E 1 := (axis (3/4), 0)

private theorem annulus_first_norm : ‖annulusCoordinate.1‖ = (3 : ℝ) / 4 := by
  norm_num [annulusCoordinate, axis_norm]

private def annulusOldPoint : MorseCone.oldSet identityCone := by
  have hlevel : (0 : ℝ) ≤ MorseCone.quadratic annulusCoordinate := by
    norm_num [MorseCone.quadratic, annulus_first_norm, annulusCoordinate]
  have hne : annulusCoordinate ≠ (0 : E 1 × E 1) := by
    intro he
    have hn := congrArg (fun z : E 1 × E 1 => ‖z.1‖) he
    rw [annulus_first_norm] at hn
    norm_num at hn
  exact ⟨⟨annulusCoordinate, hlevel⟩, hne⟩

private theorem annulus_in_original_patch :
    annulusOldPoint.val ∈ MorseCone.patchSet identityCone := by
  constructor
  · simp [identityCone]
  · change ‖annulusCoordinate.1‖ ^ 2 + ‖annulusCoordinate.2‖ ^ 2 < (1 : ℝ) ^ 2
    norm_num [annulus_first_norm, annulusCoordinate]

theorem concrete_original_Foot_annulus_zero :
    MorseOpenGluing.Foot (MorseCone.oldSet identityCone)
      (MorseCone.patchSet identityCone) (ZerothHomotopy.mk annulusOldPoint) ∧
    beta (by decide : 1 ≤ 2) 1 (by norm_num)
      (identityCone.chart annulusOldPoint.val.val) = 0 := by
  have houter : identityCone.ρ / 2 ≤
      ‖(split (by decide : 1 ≤ 2)).symm
        (identityCone.chart annulusOldPoint.val.val)‖ := by
    have he := split_energy (by decide : 1 ≤ 2)
      ((split (by decide : 1 ≤ 2)).symm annulusCoordinate)
    rw [(split (by decide : 1 ≤ 2)).apply_symm_apply] at he
    have hn : 0 ≤ ‖(split (by decide : 1 ≤ 2)).symm annulusCoordinate‖ := norm_nonneg _
    have hsq : ‖(split (by decide : 1 ≤ 2)).symm annulusCoordinate‖ ^ 2 =
        ((3 : ℝ) / 4) ^ 2 := by
      simpa [annulusCoordinate, annulus_first_norm] using he
    have hnorm : ‖(split (by decide : 1 ≤ 2)).symm annulusCoordinate‖ = 3 / 4 := by
      nlinarith
    simpa [identityCone, annulusOldPoint, hnorm] using
      (show (1 : ℝ) / 2 ≤ 3 / 4 by norm_num)
  refine ⟨⟨annulusOldPoint, annulus_in_original_patch, rfl⟩, ?_⟩
  change (cutoffBump 1 (by norm_num))
    ((split (by decide : 1 ≤ 2)).symm
      (identityCone.chart annulusOldPoint.val.val)) = 0
  exact (cutoffBump 1 (by norm_num)).zero_of_le_dist
    (by simpa only [cutoffBump, dist_zero_right] using houter)

/- The literal oldSet/patchSet Foot witness can lie where the cutoff vanishes.
The annulus coordinate is explicit; no all-Foot coverage follows. -/
theorem literal_Foot_outer_annulus {n k : ℕ} (hk : k ≤ n)
    (D : MorseCone.NormalForm (X n) (E k) (E (n-k)))
    (a : MorseCone.oldSet D) (hpatch : a.val ∈ MorseCone.patchSet D)
    (houter : D.ρ / 2 ≤ ‖(split hk).symm (D.chart a.val.val)‖) :
    MorseOpenGluing.Foot (MorseCone.oldSet D) (MorseCone.patchSet D)
      (ZerothHomotopy.mk a) ∧
    beta hk D.ρ D.hρ (D.chart a.val.val) = 0 := by
  refine ⟨⟨a, hpatch, rfl⟩, ?_⟩
  change (cutoffBump D.ρ D.hρ) ((split hk).symm (D.chart a.val.val)) = 0
  exact (cutoffBump D.ρ D.hρ).zero_of_le_dist
    (by simpa only [cutoffBump, dist_zero_right] using houter)

/- The support boundary is admitted by the actual target inclusion, whereas
the full closed radius-ρ boundary has no such conclusion. -/
theorem closed_half_radius_in_target {n k : ℕ} (hk : k ≤ n)
    (ρ : ℝ) (hρ : 0 < ρ) (F : X n → ℝ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (x0 : X n)
    (g : CompactGeometry hk ρ hρ F phi T U x0)
    (z : E k × E (n-k)) (hz : ‖(split hk).symm z‖ = ρ / 2) : z ∈ T := by
  apply g.K_target
  refine ⟨(split hk).symm z, ?_, (split hk).apply_symm_apply z⟩
  simpa only [Metric.mem_closedBall, dist_zero_right] using hz.le

theorem full_closed_radius_rejected_by_strict_target (ρ : ℝ) (hρ : 0 < ρ) :
    ¬ Metric.closedBall (0 : ℝ) ρ ⊆ Metric.ball 0 ρ := by
  intro hsubset
  have hclosed : ρ ∈ Metric.closedBall (0 : ℝ) ρ := by
    simpa only [Metric.mem_closedBall, Real.dist_eq, sub_zero,
      abs_of_nonneg hρ.le] using (le_refl ρ)
  have hopen := hsubset hclosed
  have hbad : ρ < ρ := by
    simpa only [Metric.mem_ball, Real.dist_eq, sub_zero,
      abs_of_nonneg hρ.le] using hopen
  exact (lt_irrefl ρ) hbad

private def fullRadiusCoordinate : E 1 × E 1 := (axis 1, 0)

theorem n2_closed_rho_boundary_rejected_by_radiusBall :
    ‖(split (by decide : 1 ≤ 2)).symm fullRadiusCoordinate‖ = 1 ∧
    fullRadiusCoordinate ∉ MorseCone.radiusBall (E := E 1) (F := E 1) 1 := by
  have he := split_energy (by decide : 1 ≤ 2)
    ((split (by decide : 1 ≤ 2)).symm fullRadiusCoordinate)
  rw [(split (by decide : 1 ≤ 2)).apply_symm_apply] at he
  have hsq : ‖(split (by decide : 1 ≤ 2)).symm fullRadiusCoordinate‖ ^ 2 = 1 := by
    simpa [fullRadiusCoordinate, axis_norm] using he
  have hn : 0 ≤ ‖(split (by decide : 1 ≤ 2)).symm fullRadiusCoordinate‖ := norm_nonneg _
  have hnorm : ‖(split (by decide : 1 ≤ 2)).symm fullRadiusCoordinate‖ = 1 := by
    nlinarith
  constructor
  · exact hnorm
  · change ¬ (‖fullRadiusCoordinate.1‖ ^ 2 + ‖fullRadiusCoordinate.2‖ ^ 2 <
      (1 : ℝ) ^ 2)
    norm_num [fullRadiusCoordinate, axis_norm]

private def strictRadiusIdentityChart :
    OpenPartialHomeomorph (E 1 × E 1) (E 1 × E 1) :=
  OpenPartialHomeomorph.ofSet
    (MorseCone.radiusBall (E := E 1) (F := E 1) 1)
    (isOpen_lt (by fun_prop) continuous_const)

theorem strict_identity_target_rejects_full_closed_rho :
    fullRadiusCoordinate ∈
      (split (by decide : 1 ≤ 2)) '' Metric.closedBall (0 : E 2) 1 ∧
    fullRadiusCoordinate ∉ strictRadiusIdentityChart.target := by
  obtain ⟨hnorm, houtside⟩ := n2_closed_rho_boundary_rejected_by_radiusBall
  constructor
  · refine ⟨(split (by decide : 1 ≤ 2)).symm fullRadiusCoordinate, ?_,
      (split (by decide : 1 ≤ 2)).apply_symm_apply fullRadiusCoordinate⟩
    simpa only [Metric.mem_closedBall, dist_zero_right] using hnorm.le
  · simpa [strictRadiusIdentityChart] using houtside

theorem half_closed_K_in_strict_identity_target :
    K (by decide : 1 ≤ 2) 1 ⊆ strictRadiusIdentityChart.target := by
  rintro z ⟨u, hu, rfl⟩
  have hnorm : ‖u‖ ≤ (1 : ℝ) / 2 := by
    simpa only [Metric.mem_closedBall, dist_zero_right] using hu
  have hsq : ‖u‖ ^ 2 ≤ ((1 : ℝ) / 2) ^ 2 :=
    (sq_le_sq₀ (norm_nonneg u) (by norm_num)).mpr hnorm
  change ‖(split (by decide : 1 ≤ 2) u).1‖ ^ 2 +
    ‖(split (by decide : 1 ≤ 2) u).2‖ ^ 2 < (1 : ℝ) ^ 2
  rw [← split_energy (by decide : 1 ≤ 2) u]
  nlinarith

/- Canonical physical-to-split linear chart, with no assumed P. -/
private def partialSplit : X 2 ≃L[ℝ] (E 1 × E 1) :=
  (EuclideanSpace.equiv (Fin 2) ℝ).symm.trans (split (by decide : 1 ≤ 2))

private def partialTarget : Set (E 1 × E 1) :=
  MorseCone.radiusBall (E := E 1) (F := E 1) 1

private def partialSource : Set (X 2) := partialSplit ⁻¹' partialTarget

private def innerZ : E 1 × E 1 := (axis (1 / 8), 0)
private def outerZ : E 1 × E 1 := (axis 2, 0)
private def outerX : X 2 := partialSplit.symm outerZ

/- On the nonempty open source this is the canonical linear equivalence.
   Outside source it deliberately returns a small nonzero chart coordinate. -/
private def offSourceSmallChart : OpenPartialHomeomorph (X 2) (E 1 × E 1) := by
  have hT : IsOpen partialTarget :=
    isOpen_lt (by fun_prop) continuous_const
  have hS : IsOpen partialSource := hT.preimage partialSplit.continuous
  refine {
    toFun := fun x => if x ∈ partialSource then partialSplit x else innerZ
    invFun := partialSplit.symm
    source := partialSource
    target := partialTarget
    map_source' := ?_
    map_target' := ?_
    left_inv' := ?_
    right_inv' := ?_
    continuousOn_toFun := ?_
    continuousOn_invFun := partialSplit.symm.continuous.continuousOn
    open_source := hS
    open_target := hT
  }
  · intro x hx
    change (if x ∈ partialSource then partialSplit x else innerZ) ∈ partialTarget
    simpa [partialSource, hx] using hx
  · intro z hz
    change partialSplit.symm z ∈ partialSource
    simpa [partialSource] using hz
  · intro x hx
    change partialSplit.symm
      (if x ∈ partialSource then partialSplit x else innerZ) = x
    simp [hx]
  · intro z hz
    have hs : partialSplit.symm z ∈ partialSource := by
      simpa [partialSource] using hz
    change (if partialSplit.symm z ∈ partialSource then
      partialSplit (partialSplit.symm z) else innerZ) = z
    simp [hs]
  · exact partialSplit.continuous.continuousOn.congr
      (by intro x hx; simp [hx])

theorem off_source_small_chart_has_nonempty_source :
    (0 : X 2) ∈ offSourceSmallChart.source := by
  change (0 : X 2) ∈ partialSource
  change partialSplit (0 : X 2) ∈ partialTarget
  norm_num [partialTarget, MorseCone.radiusBall]

/- This binds the off-source behavior to the actual V1 and Q1 definitions.
   No premise asserts that beta is 1 or raw Q1 is nonzero. -/
theorem concrete_off_source_small_chart_guard :
    outerX ∉ offSourceSmallChart.source ∧
    offSourceSmallChart outerX = innerZ ∧
    beta (by decide : 1 ≤ 2) 1 (by norm_num) innerZ = 1 ∧
    Q1 offSourceSmallChart.symm innerZ ≠ 0 ∧
    V1 (by decide : 1 ≤ 2) 1 (by norm_num)
      offSourceSmallChart offSourceSmallChart.source outerX = 0 := by
  have hout : outerZ ∉ partialTarget := by
    norm_num [partialTarget, MorseCone.radiusBall, outerZ, axis_norm]
  have hx : outerX ∉ offSourceSmallChart.source := by
    change outerX ∉ partialSource
    simpa [partialSource, outerX] using hout
  have hchart : offSourceSmallChart outerX = innerZ := by
    change (if outerX ∈ partialSource then partialSplit outerX else innerZ) = innerZ
    simp [show outerX ∉ partialSource from hx]
  have he := split_energy (by decide : 1 ≤ 2)
    ((split (by decide : 1 ≤ 2)).symm innerZ)
  rw [(split (by decide : 1 ≤ 2)).apply_symm_apply] at he
  have hsq : ‖(split (by decide : 1 ≤ 2)).symm innerZ‖ ^ 2 =
      ((1 : ℝ) / 8) ^ 2 := by
    simpa [innerZ, axis_norm] using he
  have hn : 0 ≤ ‖(split (by decide : 1 ≤ 2)).symm innerZ‖ := norm_nonneg _
  have hnorm : ‖(split (by decide : 1 ≤ 2)).symm innerZ‖ = 1 / 8 := by
    nlinarith
  have hb : beta (by decide : 1 ≤ 2) 1 (by norm_num) innerZ = 1 := by
    change (cutoffBump 1 (by norm_num))
      ((split (by decide : 1 ≤ 2)).symm innerZ) = 1
    apply (cutoffBump 1 (by norm_num)).one_of_mem_closedBall
    change dist ((split (by decide : 1 ≤ 2)).symm innerZ) 0 ≤ (1 : ℝ) / 4
    simp [dist_zero_right, hnorm]
  have hW : W1 innerZ ≠ (0 : E 1 × E 1) := by
    intro heq
    have hf := congrArg (fun z : E 1 × E 1 => ‖z.1‖) heq
    norm_num [W1, innerZ, axis_norm] at hf
  have hQeq : Q1 offSourceSmallChart.symm innerZ =
      partialSplit.symm (W1 innerZ) := by
    change fderiv ℝ (partialSplit.symm : E 1 × E 1 → X 2) innerZ
      (W1 innerZ) = partialSplit.symm (W1 innerZ)
    simp [ContinuousLinearMap.fderiv]
  have hQ : Q1 offSourceSmallChart.symm innerZ ≠ 0 := by
    rw [hQeq]
    intro heq
    apply hW
    apply partialSplit.symm.injective
    simpa using heq
  refine ⟨hx, hchart, hb, hQ, ?_⟩
  simp [V1, extension, hx]

/- Membership in U is essential even when the totalized chart happens to
return an inner coordinate.  This is a direct assertion about the literal
extension and both piecewise rates, with no assumptions on phi outside U. -/
theorem off_overlap_zero_despite_small_chart {n k : ℕ} (hk : k ≤ n)
    (ρ : ℝ) (hρ : 0 < ρ) (F : X n → ℝ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (U : Set (X n)) (x : X n)
    (hx : x ∉ U) (hsmall : ‖(split hk).symm (phi x)‖ ≤ ρ / 4) :
    beta hk ρ hρ (phi x) = 1 ∧
    V0 hk ρ hρ phi U x = 0 ∧ V1 hk ρ hρ phi U x = 0 ∧
    fderiv ℝ F x (V0 hk ρ hρ phi U x) = 0 ∧
    fderiv ℝ F x (V1 hk ρ hρ phi U x) = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · change (cutoffBump ρ hρ) ((split hk).symm (phi x)) = 1
    apply (cutoffBump ρ hρ).one_of_mem_closedBall
    simpa only [cutoffBump, Metric.mem_closedBall, dist_zero_right] using hsmall
  · simp [V0, extension, hx]
  · simp [V1, extension, hx]
  · simp [V0, extension, hx]
  · simp [V1, extension, hx]

theorem smaller_overlap_rejects_coordinate_only_extension {n k : ℕ}
    (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (x : X n) (hxsource : x ∈ phi.source)
    (hsmall : ‖(split hk).symm (phi x)‖ ≤ ρ / 4)
    (Q : (E k × E (n-k)) → X n) :
    (phi.source \ {x} : Set (X n)) ⊆ phi.source ∧
    beta hk ρ hρ (phi x) = 1 ∧
    extension hk ρ hρ phi (phi.source \ {x}) Q x = 0 := by
  refine ⟨diff_subset, ?_, ?_⟩
  · change (cutoffBump ρ hρ) ((split hk).symm (phi x)) = 1
    apply (cutoffBump ρ hρ).one_of_mem_closedBall
    simpa only [cutoffBump, Metric.mem_closedBall, dist_zero_right] using hsmall
  · simp [extension]

/- These tests cover all endpoint dimensions.  They assert zero rates only
for the factor that is genuinely trivial; no positive rate is inferred. -/
theorem zero_factor_rate {n k : ℕ} (hk : k ≤ n) (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E k × E (n-k)))
    (T : Set (E k × E (n-k))) (U : Set (X n)) (x0 : X n)
    (g : CompactGeometry hk ρ hρ F phi T U x0)
    (x : X n) (hzero : (phi x).2 = 0) :
    fderiv ℝ F x (V0 hk ρ hρ phi U x) = 0 := by
  rw [g.rate0]
  by_cases hx : x ∈ U
  · simp [hx, hzero]
  · simp [hx]

theorem n0_k0_rates (ρ : ℝ) (hρ : 0 < ρ)
    (F : X 0 → ℝ) (phi : OpenPartialHomeomorph (X 0) (E 0 × E 0))
    (T : Set (E 0 × E 0)) (U : Set (X 0)) (x0 : X 0)
    (g : CompactGeometry (by decide : 0 ≤ 0) ρ hρ F phi T U x0)
    (x : X 0) :
    fderiv ℝ F x (V0 (by decide : 0 ≤ 0) ρ hρ phi U x) = 0 ∧
    fderiv ℝ F x (V1 (by decide : 0 ≤ 0) ρ hρ phi U x) = 0 := by
  have hfst : (phi x).1 = 0 := Subsingleton.elim _ _
  have hsnd : (phi x).2 = 0 := Subsingleton.elim _ _
  constructor
  · rw [g.rate0]
    simp [hsnd]
  · rw [g.rate1]
    simp [hfst, hsnd]

theorem k0_rates_agree {n : ℕ} (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E 0 × E n))
    (T : Set (E 0 × E n)) (U : Set (X n)) (x0 : X n)
    (g : CompactGeometry (Nat.zero_le n) ρ hρ F phi T U x0)
    (x : X n) :
    fderiv ℝ F x (V1 (Nat.zero_le n) ρ hρ phi U x) =
      fderiv ℝ F x (V0 (Nat.zero_le n) ρ hρ phi U x) := by
  have hfst : (phi x).1 = 0 := Subsingleton.elim _ _
  rw [g.rate0, g.rate1]
  simp [hfst]

theorem kn_rate0_zero {n : ℕ} (ρ : ℝ) (hρ : 0 < ρ)
    (F : X n → ℝ) (phi : OpenPartialHomeomorph (X n) (E n × E (n-n)))
    (T : Set (E n × E (n-n))) (U : Set (X n)) (x0 : X n)
    (g : CompactGeometry (Nat.le_refl n) ρ hρ F phi T U x0)
    (x : X n) :
    fderiv ℝ F x (V0 (Nat.le_refl n) ρ hρ phi U x) = 0 := by
  exact zero_factor_rate (Nat.le_refl n) ρ hρ F phi T U x0 g x
    (Subsingleton.elim _ _)

/- Arithmetic checkpoint for the anisotropic inverse ψ(y,z)=(2y,3z).
At (1,1), F(x)=(x₁/2)²-(x₂/3)² has gradient (1,-2/3).
Thus the pushed direction (2,-3) gives 4, the raw direction
(1,-1) gives 5/3, and the reversed negative-axis direction (0,3)
gives -2.  The following controls connect these values to actual `fderiv`; hosted
elaboration is still required. -/
theorem anisotropic_direction_arithmetic :
    (1 : ℝ) * 2 + (-(2 : ℝ) / 3) * (-3) = 4 ∧
    (1 : ℝ) * 1 + (-(2 : ℝ) / 3) * (-1) = 5 / 3 ∧
    (1 : ℝ) * 0 + (-(2 : ℝ) / 3) * 3 = -2 ∧
    (∀ b : ℝ, b * ((1 : ℝ) * 2 + (-(2 : ℝ) / 3) * (-3)) = b * 4) := by
  constructor
  · norm_num
  constructor
  · norm_num
  constructor
  · norm_num
  · intro b
    ring

private def anisotropicInverse (z : ℝ × ℝ) : ℝ × ℝ := (2 * z.1, 3 * z.2)
private def anisotropicPotential (x : ℝ × ℝ) : ℝ :=
  (x.1 / 2) ^ 2 - (x.2 / 3) ^ 2

private theorem anisotropic_actual_Q_vectors :
    Q0 anisotropicInverse ((1, 1) : ℝ × ℝ) = (0, -3) ∧
    Q1 anisotropicInverse ((1, 1) : ℝ × ℝ) = (2, -3) := by
  have hd : HasFDerivAt anisotropicInverse
      (((2 : ℝ) • (ContinuousLinearMap.fst ℝ ℝ ℝ)).prod
        ((3 : ℝ) • (ContinuousLinearMap.snd ℝ ℝ ℝ))) (1, 1) := by
    simpa only [anisotropicInverse] using
      (((hasFDerivAt_fst (p := ((1, 1) : ℝ × ℝ))).const_mul (2 : ℝ)).prodMk
        ((hasFDerivAt_snd (p := ((1, 1) : ℝ × ℝ))).const_mul (3 : ℝ)))
  constructor
  · simp [Q0, W0, hd.fderiv]
  · simp [Q1, W1, hd.fderiv]

theorem anisotropic_actual_Q_rates :
    fderiv ℝ anisotropicPotential (anisotropicInverse (1, 1))
      (Q1 anisotropicInverse (1, 1)) = 4 ∧
    fderiv ℝ anisotropicPotential (anisotropicInverse (1, 1))
      (Q0 anisotropicInverse (1, 1)) = 2 ∧
    fderiv ℝ anisotropicPotential (anisotropicInverse (1, 1))
      (-(Q0 anisotropicInverse (1, 1))) = -2 := by
  have hF : Differentiable ℝ anisotropicPotential := by
    intro x
    dsimp [anisotropicPotential]
    fun_prop
  have hpsi : ContDiffOn ℝ 2 anisotropicInverse (Set.univ : Set (ℝ × ℝ)) := by
    apply ContDiff.contDiffOn
    dsimp [anisotropicInverse]
    fun_prop
  have hidentity : ∀ z ∈ (Set.univ : Set (ℝ × ℝ)),
      anisotropicPotential (anisotropicInverse z) =
        (0 : ℝ) + MorseCone.quadratic z := by
    intro z _
    simp only [anisotropicPotential, anisotropicInverse, MorseCone.quadratic,
      Real.norm_eq_abs, sq_abs, zero_add]
    ring
  have hr := rates_of_local_identity anisotropicPotential anisotropicInverse
    (Set.univ : Set (ℝ × ℝ)) 0 isOpen_univ hF hpsi hidentity
    (1, 1) (Set.mem_univ _)
  have h0 : fderiv ℝ anisotropicPotential (anisotropicInverse (1, 1))
      (Q0 anisotropicInverse (1, 1)) = 2 := by
    simpa only [Real.norm_eq_abs, abs_one, one_pow, mul_one] using hr.1
  have h1 : fderiv ℝ anisotropicPotential (anisotropicInverse (1, 1))
      (Q1 anisotropicInverse (1, 1)) = 4 := by
    convert hr.2 using 1 <;> norm_num [Real.norm_eq_abs]
  refine ⟨h1, h0, ?_⟩
  rw [map_neg, h0]

theorem anisotropic_raw_tuple_rate :
    fderiv ℝ anisotropicPotential (anisotropicInverse ((1, 1) : ℝ × ℝ))
      ((1, -1) : ℝ × ℝ) = 5 / 3 := by
  obtain ⟨hQ0, hQ1⟩ := anisotropic_actual_Q_vectors
  obtain ⟨h1, h0, _⟩ := anisotropic_actual_Q_rates
  have hdecomp : ((1, -1) : ℝ × ℝ) =
      ((1 : ℝ) / 2) • Q1 anisotropicInverse (1, 1) -
        ((1 : ℝ) / 6) • Q0 anisotropicInverse (1, 1) := by
    rw [hQ0, hQ1]
    norm_num [Prod.smul_def]
  rw [hdecomp, map_sub, map_smul, map_smul, h1, h0]
  norm_num

theorem anisotropic_actual_scaled_Q1_rate (b : ℝ) :
    fderiv ℝ anisotropicPotential (anisotropicInverse ((1, 1) : ℝ × ℝ))
      (b • Q1 anisotropicInverse (1, 1)) = b * 4 := by
  rw [map_smul, (anisotropic_actual_Q_rates).1]

theorem anisotropic_midpoint_beta_scales_Q1_rate :
    ∃ t ∈ Set.Ioo ((1 : ℝ) / 4) (1 / 2),
      fderiv ℝ anisotropicPotential (anisotropicInverse ((1, 1) : ℝ × ℝ))
        ((beta (by decide : 1 ≤ 2) 1 (by norm_num)
          (split (by decide : 1 ≤ 2)
            (t • (EuclideanSpace.single (0 : Fin 2) (1 : ℝ) : E 2)))) •
          Q1 anisotropicInverse (1, 1)) = 2 := by
  obtain ⟨t, ht, hb⟩ := intermediate_beta_n2_k1
  refine ⟨t, ht, ?_⟩
  rw [hb, anisotropic_actual_scaled_Q1_rate]
  norm_num

theorem concrete_intermediate_beta_scales_actual_V1_rate
    (F : X 2 → ℝ) (phi : OpenPartialHomeomorph (X 2) (E 1 × E 1))
    (T : Set (E 1 × E 1)) (U : Set (X 2)) (c : ℝ) (x0 : X 2)
    (hgeo : LocalGeometry F phi T U c x0)
    (g : CompactGeometry (by decide : 1 ≤ 2) 1 (by norm_num) F phi T U x0) :
    ∃ x ∈ U,
      beta (by decide : 1 ≤ 2) 1 (by norm_num) (phi x) = 1 / 2 ∧
      fderiv ℝ F x (V1 (by decide : 1 ≤ 2) 1 (by norm_num) phi U x) =
        (1 / 2 : ℝ) * (2 * (‖(phi x).1‖ ^ 2 + ‖(phi x).2‖ ^ 2)) := by
  obtain ⟨t, ht, hbeta⟩ := intermediate_beta_n2_k1
  let hk : 1 ≤ 2 := by decide
  let w : E 2 := EuclideanSpace.single (0 : Fin 2) (1 : ℝ)
  let z : E 1 × E 1 := split hk (t • w)
  have ht0 : 0 ≤ t := by linarith [ht.1]
  have hw : ‖w‖ = 1 := by simp [w, EuclideanSpace.norm_single]
  have hnorm : ‖t • w‖ = t := by
    simp [norm_smul, Real.norm_eq_abs, abs_of_nonneg ht0, hw]
  have hzK : z ∈ K hk 1 := by
    refine ⟨t • w, ?_, rfl⟩
    simpa only [Metric.mem_closedBall, dist_zero_right, hnorm] using ht.2.le
  have hzT : z ∈ T := g.K_target hzK
  have hxU : phi.symm z ∈ U := hgeo.inverse_target hzT
  have hright : phi (phi.symm z) = z := phi.right_inv (hgeo.target_subset hzT)
  have hbetaZ : beta hk 1 (by norm_num) z = 1 / 2 := by
    simpa only [hk, z, w] using hbeta
  refine ⟨phi.symm z, hxU, ?_, ?_⟩
  · simpa only [hright] using hbetaZ
  · rw [g.rate1, if_pos hxU, hright, hbetaZ]

theorem actual_source_consumer_preserves_premises {n : ℕ} {L : ℝ}
    [Fact (0 < L)] (omega : I4Source.SourceMode n → ℝ)
    (hmajor : Summable (fun m => I4Source.modeMajorant n L m * |omega m|))
    (x0 : X n) (hdet : (PhysicalSpectral.hessian (L := L) omega x0).det ≠ 0)
    (hcrit : fderiv ℝ (I4Source.sourceField n L omega) x0 = 0) :
    ∃ (k : ℕ) (hk : k ≤ n) (P : E n ≃L[ℝ] X n) (s : Sym n → Sym n)
      (e : OpenPartialHomeomorph (E n) (E n))
      (D : MorseCone.NormalForm (I4Torus.SourceTorus n L) (E k) (E (n-k))),
      D.f = I4Torus.torusSourceField n L omega ∧
      D.p = I4Torus.torusProjection n L x0 ∧
      D.chart = (liftChart (L := L) x0).trans (physicalChart hk x0 P e) ∧
      CompactGeometry hk D.ρ D.hρ (I4Source.sourceField n L omega)
        (physicalChart hk x0 P e) D.chart.target
        ((physicalChart hk x0 P e).source ∩ (liftChart (L := L) x0).target) x0 := by
  obtain ⟨k, hk, P, s, e, D, _, _, _, _, _, _, _, _, _,
    hf, hp, _, hchart, _, _, _, _, _, hcompact⟩ :=
    actual_source_compact_cutoff omega hmajor x0 hdet hcrit
  exact ⟨k, hk, P, s, e, D, hf, hp, hchart, hcompact⟩

/- A literal signature parity check: all original conjuncts and the new geometry
are returned by the one actual-source consumer with its original inputs. -/
theorem actual_source_exact_witness_parity {n : ℕ} {L : ℝ} [Fact (0 < L)]
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
  exact actual_source_compact_cutoff omega hmajor x0 hdet hcrit

end CompactSourceCutoffControls
