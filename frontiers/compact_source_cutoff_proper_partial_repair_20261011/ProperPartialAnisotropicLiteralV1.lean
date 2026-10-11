import CompactSourceCutoffProof
import Mathlib.Topology.Order.IntermediateValue

/-!
Closed proper partial anisotropic control for the literal cutoff.  All fixture
constants are defined in this module.  This is a generic polynomial falsifier,
not an instance of the Gaussian or torus source.  Preparation is NOT_COMPILED;
only a fresh exact-source hosted run can supply elaboration/kernel evidence.
-/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open Set SourceCoordinates SourceNormalForm SourcePushedHeight SourceCompactCutoff MorseCongruence
open scoped Topology ContDiff Manifold Matrix.Norms.Frobenius
namespace ProperPartialAnisotropicLiteralV1
attribute [local instance] Classical.propDecidable

private def hk : 1 ≤ 2 := by decide
private def h1 : (0 : ℝ) < 1 := by norm_num

private def B : X 2 ≃L[ℝ] (E 1 × E 1) :=
  (EuclideanSpace.equiv (Fin 2) ℝ).symm.trans (split hk)

private def A : X 2 →L[ℝ] (E 1 × E 1) :=
  (((1 / 2 : ℝ) • ContinuousLinearMap.fst ℝ (E 1) (E 1)).prod
    ((1 / 3 : ℝ) • ContinuousLinearMap.snd ℝ (E 1) (E 1))).comp
      B.toContinuousLinearMap

private def psi : (E 1 × E 1) →L[ℝ] X 2 :=
  B.symm.toContinuousLinearMap.comp
    (((2 : ℝ) • ContinuousLinearMap.fst ℝ (E 1) (E 1)).prod
      ((3 : ℝ) • ContinuousLinearMap.snd ℝ (E 1) (E 1)))

private theorem A_apply (x : X 2) :
    A x = ((1 / 2 : ℝ) • (B x).1, (1 / 3 : ℝ) • (B x).2) := by
  simp [A]

private theorem psi_apply (z : E 1 × E 1) :
    psi z = B.symm ((2 : ℝ) • z.1, (3 : ℝ) • z.2) := by
  simp [psi]

private theorem A_psi (z : E 1 × E 1) : A (psi z) = z := by
  rw [A_apply, psi_apply, B.apply_symm_apply]
  apply Prod.ext <;> simp [smul_smul]

private theorem psi_A (x : X 2) : psi (A x) = x := by
  apply B.injective
  rw [psi_apply, B.apply_symm_apply, A_apply]
  apply Prod.ext <;> simp [smul_smul]

private def axis (a : ℝ) : E 1 :=
  a • (EuclideanSpace.single (0 : Fin 1) (1 : ℝ) : E 1)

private theorem axis_norm (a : ℝ) : ‖axis a‖ = |a| := by
  simp [axis, norm_smul, EuclideanSpace.norm_single, Real.norm_eq_abs]

private theorem smul_axis (a b : ℝ) : a • axis b = axis (a * b) := by
  simp [axis, smul_smul]

private def innerZ : E 1 × E 1 := (axis (1 / 8), 0)
private def outerZ : E 1 × E 1 := (axis 2, 0)
private def betweenZ : E 1 × E 1 := (axis (3 / 2), 0)
private def S : Set (X 2) := A ⁻¹' MorseCone.radiusBall 2
private def T : Set (E 1 × E 1) := MorseCone.radiusBall 1
private def U : Set (X 2) := A ⁻¹' T
private def outerX : X 2 := psi outerZ
private def betweenX : X 2 := psi betweenZ

/- The totalized forward value off source is deliberately small and nonzero.
The smooth potential below uses A, not this piecewise function. -/
private def phi : OpenPartialHomeomorph (X 2) (E 1 × E 1) := by
  have hR : IsOpen (MorseCone.radiusBall (E := E 1) (F := E 1) 2) :=
    isOpen_lt (by fun_prop) continuous_const
  have hS : IsOpen S := hR.preimage A.continuous
  refine {
    toFun := fun x => if x ∈ S then A x else innerZ
    invFun := psi
    source := S
    target := MorseCone.radiusBall 2
    map_source' := ?_
    map_target' := ?_
    left_inv' := ?_
    right_inv' := ?_
    continuousOn_toFun := ?_
    continuousOn_invFun := psi.continuous.continuousOn
    open_source := hS
    open_target := hR }
  · intro x hx
    change (if x ∈ S then A x else innerZ) ∈ MorseCone.radiusBall 2
    rw [if_pos hx]
    exact hx
  · intro z hz
    change A (psi z) ∈ MorseCone.radiusBall 2
    simpa only [A_psi] using hz
  · intro x hx
    change psi (if x ∈ S then A x else innerZ) = x
    rw [if_pos hx, psi_A]
  · intro z hz
    have hs : psi z ∈ S := by
      change A (psi z) ∈ MorseCone.radiusBall 2
      simpa only [A_psi] using hz
    change (if psi z ∈ S then A (psi z) else innerZ) = z
    rw [if_pos hs, A_psi]
  · exact A.continuous.continuousOn.congr
      (by intro x hx; simp [hx])

private theorem phi_source : phi.source = S := rfl
private theorem phi_target : phi.target = MorseCone.radiusBall 2 := rfl
private theorem phi_symm : (phi.symm : E 1 × E 1 → X 2) = psi := rfl

private theorem phi_on_source (x : X 2) (hx : x ∈ S) : phi x = A x := by
  change (if x ∈ S then A x else innerZ) = A x
  exact if_pos hx

private def F (x : X 2) : ℝ := MorseCone.quadratic (A x)

#eval IO.eprintln "BOUNDARY proper-partial-data"

private theorem T_open : IsOpen T :=
  isOpen_lt (by fun_prop) continuous_const

private theorem U_open : IsOpen U := T_open.preimage A.continuous

private theorem T_subset_target : T ⊆ phi.target := by
  intro z hz
  change ‖z.1‖ ^ 2 + ‖z.2‖ ^ 2 < (1 : ℝ) ^ 2 at hz
  change ‖z.1‖ ^ 2 + ‖z.2‖ ^ 2 < (2 : ℝ) ^ 2
  nlinarith

private theorem U_subset_source : U ⊆ phi.source := by
  intro x hx
  exact T_subset_target hx

private theorem inverse_target : MapsTo phi.symm T U := by
  intro z hz
  change A (psi z) ∈ T
  simpa only [A_psi] using hz

private theorem forward_target : MapsTo phi U T := by
  intro x hx
  rw [phi_on_source x (U_subset_source hx)]
  exact hx

private theorem phi_forward_C2 : ContDiffOn ℝ 2 phi phi.source := by
  apply A.contDiff.contDiffOn.congr
  intro x hx
  exact phi_on_source x hx

private theorem phi_inverse_C2 : ContDiffOn ℝ 2 phi.symm phi.target := by
  rw [phi_symm]
  exact psi.contDiff.contDiffOn

private theorem F_differentiable : Differentiable ℝ F := by
  intro x
  have hq : DifferentiableAt ℝ (MorseCone.quadratic : E 1 × E 1 → ℝ) (A x) :=
    ((hasFDerivAt_fst (p := A x)).norm_sq.sub
      (hasFDerivAt_snd (p := A x)).norm_sq).differentiableAt
  exact hq.comp x A.differentiableAt

private theorem global_height (z : E 1 × E 1) :
    F (phi.symm z) = (0 : ℝ) + MorseCone.quadratic z := by
  change MorseCone.quadratic (A (psi z)) = 0 + MorseCone.quadratic z
  rw [A_psi, zero_add]

private theorem Q0_linear (z : E 1 × E 1) :
    Q0 phi.symm z = psi (W0 z) := by
  letI : IsBoundedSMul ℝ (E 1 × E 1) := NormedSpace.toIsBoundedSMul
  letI : ContinuousSMul ℝ (E 1 × E 1) := IsBoundedSMul.continuousSMul
  change fderiv ℝ (psi : E 1 × E 1 → X 2) z (W0 z) = psi (W0 z)
  rw [ContinuousLinearMap.fderiv]

private theorem Q1_linear (z : E 1 × E 1) :
    Q1 phi.symm z = psi (W1 z) := by
  letI : IsBoundedSMul ℝ (E 1 × E 1) := NormedSpace.toIsBoundedSMul
  letI : ContinuousSMul ℝ (E 1 × E 1) := IsBoundedSMul.continuousSMul
  change fderiv ℝ (psi : E 1 × E 1 → X 2) z (W1 z) = psi (W1 z)
  rw [ContinuousLinearMap.fderiv]

private theorem global_rates (z : E 1 × E 1) :
    fderiv ℝ F (phi.symm z) (Q0 phi.symm z) = 2 * ‖z.2‖ ^ 2 ∧
    fderiv ℝ F (phi.symm z) (Q1 phi.symm z) =
      2 * (‖z.1‖ ^ 2 + ‖z.2‖ ^ 2) := by
  have hpsi : ContDiffOn ℝ 2 phi.symm (Set.univ : Set (E 1 × E 1)) := by
    rw [phi_symm]
    exact psi.contDiff.contDiffOn
  exact rates_of_local_identity F phi.symm Set.univ 0 isOpen_univ
    F_differentiable hpsi (fun z _ => global_height z) z (Set.mem_univ _)

private theorem center_in_U : (0 : X 2) ∈ U := by
  change A (0 : X 2) ∈ T
  norm_num [T, MorseCone.radiusBall]

private theorem localGeometry : LocalGeometry F phi T U 0 0 := by
  have hpsiT : ContDiffOn ℝ 2 phi.symm T := phi_inverse_C2.mono T_subset_target
  obtain ⟨hQ0, hQ1⟩ := pushed_C1 phi.symm T T_open hpsiT
  have hphiU : ContDiffOn ℝ 1 phi U :=
    (phi_forward_C2.of_le (by norm_num)).mono U_subset_source
  refine {
    target_open := T_open
    physical_open := U_open
    target_subset := T_subset_target
    inverse_target := inverse_target
    forward_target := forward_target
    forward_C2 := phi_forward_C2
    inverse_C2 := phi_inverse_C2
    push0_C1 := hQ0
    push1_C1 := hQ1
    physical0_C1 := hQ0.comp hphiU forward_target
    physical1_C1 := hQ1.comp hphiU forward_target
    height := fun z _ => global_height z
    rate0 := fun z _ => (global_rates z).1
    rate1 := fun z _ => (global_rates z).2
    center_target := ?_
    center_forward := ?_
    center_inverse := ?_
    center_push0 := ?_
    center_push1 := ?_ }
  · norm_num [T, MorseCone.radiusBall]
  · rw [phi_on_source 0 (U_subset_source center_in_U)]
    exact map_zero A
  · change psi (0 : E 1 × E 1) = 0
    exact map_zero psi
  · rw [Q0_linear]
    simp only [W0, Prod.snd_zero, neg_zero, Prod.mk_zero_zero, map_zero]
  · rw [Q1_linear]
    simp only [W1, Prod.fst_zero, Prod.snd_zero, neg_zero, Prod.mk_zero_zero, map_zero]

private theorem compactGeometry : CompactGeometry hk 1 h1 F phi T U 0 := by
  exact compact_cutoff_of_geometry hk 1 h1 F phi T U 0 0
    localGeometry U_subset_source (by intro z hz; exact hz)

private theorem between_in_target : betweenZ ∈ phi.target := by
  change ‖betweenZ.1‖ ^ 2 + ‖betweenZ.2‖ ^ 2 < (2 : ℝ) ^ 2
  norm_num [betweenZ, axis_norm]

private theorem between_not_T : betweenZ ∉ T := by
  change ¬ (‖betweenZ.1‖ ^ 2 + ‖betweenZ.2‖ ^ 2 < (1 : ℝ) ^ 2)
  norm_num [betweenZ, axis_norm]

private theorem between_in_source : betweenX ∈ phi.source := by
  change A (psi betweenZ) ∈ MorseCone.radiusBall 2
  simpa only [A_psi, phi_target] using between_in_target

private theorem between_not_U : betweenX ∉ U := by
  change ¬ A (psi betweenZ) ∈ T
  simpa only [A_psi] using between_not_T

private theorem outer_not_target : outerZ ∉ phi.target := by
  change ¬ (‖outerZ.1‖ ^ 2 + ‖outerZ.2‖ ^ 2 < (2 : ℝ) ^ 2)
  norm_num [outerZ, axis_norm]

private theorem outer_not_source : outerX ∉ phi.source := by
  change ¬ A (psi outerZ) ∈ MorseCone.radiusBall 2
  simpa only [A_psi, phi_target] using outer_not_target

private theorem outer_not_U : outerX ∉ U :=
  fun h => outer_not_source (U_subset_source h)

private theorem proper_source : phi.source ≠ Set.univ := by
  intro h
  apply outer_not_source
  rw [h]
  exact Set.mem_univ _

private theorem proper_target : phi.target ≠ Set.univ := by
  intro h
  apply outer_not_target
  rw [h]
  exact Set.mem_univ _

private theorem strict_U : U ⊂ phi.source := by
  exact (Set.ssubset_iff_of_subset U_subset_source).mpr
    ⟨betweenX, between_in_source, between_not_U⟩

private theorem strict_T : T ⊂ phi.target := by
  exact (Set.ssubset_iff_of_subset T_subset_target).mpr
    ⟨betweenZ, between_in_target, between_not_T⟩

#eval IO.eprintln "BOUNDARY proper-partial-geometry"

private def rawDirection (z : E 1 × E 1) : X 2 := B.symm (W1 z)

private theorem raw_decomposition (z : E 1 × E 1) :
    rawDirection z = ((1 : ℝ) / 2) • Q1 phi.symm z -
      ((1 : ℝ) / 6) • Q0 phi.symm z := by
  rw [Q1_linear, Q0_linear]
  apply B.injective
  apply Prod.ext
  · ext i
    simp [rawDirection, psi, W0, W1, Prod.smul_def, Prod.sub_def, smul_smul] <;> ring
  · ext i
    simp [rawDirection, psi, W0, W1, Prod.smul_def, Prod.sub_def, smul_smul] <;> ring

private theorem raw_rate (z : E 1 × E 1) :
    fderiv ℝ F (phi.symm z) (rawDirection z) =
      ‖z.1‖ ^ 2 + (2 / 3 : ℝ) * ‖z.2‖ ^ 2 := by
  rw [raw_decomposition, map_sub, map_smul, map_smul,
    (global_rates z).2, (global_rates z).1]
  simp only [smul_eq_mul]
  ring

private def rayZ : E 1 × E 1 := (axis (3 / 5), axis (4 / 5))
private def rayW : E 2 := (split hk).symm rayZ

private theorem rayW_unit : ‖rayW‖ = 1 := by
  have h := split_energy hk rayW
  change ‖rayW‖ ^ 2 = ‖(split hk ((split hk).symm rayZ)).1‖ ^ 2 +
    ‖(split hk ((split hk).symm rayZ)).2‖ ^ 2 at h
  rw [(split hk).apply_symm_apply] at h
  have ha : ‖rayZ.1‖ = (3 : ℝ) / 5 := by
    change ‖axis ((3 : ℝ) / 5)‖ = (3 : ℝ) / 5
    norm_num [axis_norm]
  have hb : ‖rayZ.2‖ = (4 : ℝ) / 5 := by
    change ‖axis ((4 : ℝ) / 5)‖ = (4 : ℝ) / 5
    norm_num [axis_norm]
  rw [ha, hb] at h
  have hs : ‖rayW‖ ^ 2 = (1 : ℝ) := by
    calc
      ‖rayW‖ ^ 2 = ((3 : ℝ) / 5) ^ 2 + ((4 : ℝ) / 5) ^ 2 := h
      _ = 1 := by norm_num
  nlinarith [norm_nonneg rayW]

private theorem intermediate_beta :
    ∃ t ∈ Set.Ioo ((1 : ℝ) / 4) (1 / 2),
      beta hk 1 h1 (split hk (t • rayW)) = 1 / 2 := by
  let b := cutoffBump (n := 2) 1 h1
  let f : ℝ → ℝ := fun t => b (t • rayW)
  have hn (t : ℝ) (ht : 0 ≤ t) : ‖t • rayW‖ = t := by
    simp [norm_smul, Real.norm_eq_abs, abs_of_nonneg ht, rayW_unit]
  have ha : f (1 / 4) = 1 := by
    change b ((1 / 4 : ℝ) • rayW) = 1
    apply b.one_of_mem_closedBall
    change dist ((1 / 4 : ℝ) • rayW) 0 ≤ (1 : ℝ) / 4
    simpa only [dist_zero_right] using (hn ((1 : ℝ) / 4) (by norm_num)).le
  have hb : f (1 / 2) = 0 := by
    change b ((1 / 2 : ℝ) • rayW) = 0
    apply b.zero_of_le_dist
    change (1 : ℝ) / 2 ≤ dist ((1 / 2 : ℝ) • rayW) 0
    simpa only [dist_zero_right] using (hn ((1 : ℝ) / 2) (by norm_num)).ge
  have hf : Continuous f := by
    letI : IsBoundedSMul ℝ (E 2) := NormedSpace.toIsBoundedSMul
    letI : ContinuousSMul ℝ (E 2) := IsBoundedSMul.continuousSMul
    exact b.continuous.comp
      ((continuous_id : Continuous (fun t : ℝ => t)).smul
        (continuous_const : Continuous (fun _ : ℝ => rayW)))
  have hm : (1 / 2 : ℝ) ∈ Set.Ioo (f (1 / 2)) (f (1 / 4)) := by
    rw [hb, ha]
    norm_num
  obtain ⟨t, ht, hft⟩ := intermediate_value_Ioo'
    (by norm_num : (1 / 4 : ℝ) ≤ 1 / 2) hf.continuousOn hm
  refine ⟨t, ht, ?_⟩
  change b ((split hk).symm (split hk (t • rayW))) = 1 / 2
  simpa only [(split hk).symm_apply_apply] using hft

private theorem ray_energy (t : ℝ) :
    ‖(split hk (t • rayW)).1‖ ^ 2 +
      ‖(split hk (t • rayW)).2‖ ^ 2 = t ^ 2 := by
  have h := split_energy hk (t • rayW)
  simpa [norm_smul, Real.norm_eq_abs, rayW_unit, sq_abs] using h.symm

private theorem ray_first_norm (t : ℝ) (ht : 0 ≤ t) :
    ‖(split hk (t • rayW)).1‖ = t * (3 / 5 : ℝ) := by
  have hz : split hk (t • rayW) = t • rayZ := by simp [rayW]
  have ha : ‖axis ((3 : ℝ) / 5)‖ = (3 : ℝ) / 5 := by norm_num [axis_norm]
  rw [hz]
  change ‖t • axis (3 / 5)‖ = t * (3 / 5 : ℝ)
  rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg ht, ha]

private theorem ray_second_norm (t : ℝ) (ht : 0 ≤ t) :
    ‖(split hk (t • rayW)).2‖ = t * (4 / 5 : ℝ) := by
  have hz : split hk (t • rayW) = t • rayZ := by simp [rayW]
  have ha : ‖axis ((4 : ℝ) / 5)‖ = (4 : ℝ) / 5 := by norm_num [axis_norm]
  rw [hz]
  change ‖t • axis (4 / 5)‖ = t * (4 / 5 : ℝ)
  rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg ht, ha]

private theorem inner_radial_norm : ‖(split hk).symm innerZ‖ = (1 : ℝ) / 8 := by
  have he := split_energy hk ((split hk).symm innerZ)
  rw [(split hk).apply_symm_apply] at he
  have hsq : ‖(split hk).symm innerZ‖ ^ 2 = ((1 : ℝ) / 8) ^ 2 := by
    simpa [innerZ, axis_norm] using he
  nlinarith [norm_nonneg ((split hk).symm innerZ)]

private theorem beta_inner : beta hk 1 h1 innerZ = 1 := by
  apply compactGeometry.inner_one
  rw [inner_radial_norm]
  norm_num

private theorem inner_scaling : innerZ = ((1 : ℝ) / 16) • outerZ := by
  apply Prod.ext
  · change axis (1 / 8) = ((1 : ℝ) / 16) • axis 2
    rw [smul_axis]
    norm_num
  · simp [innerZ, outerZ, Prod.smul_def]

private theorem Q1_inner_scaling :
    Q1 phi.symm innerZ = ((1 : ℝ) / 16) • Q1 phi.symm outerZ := by
  rw [Q1_linear, Q1_linear, inner_scaling]
  have hw : W1 (((1 : ℝ) / 16) • outerZ) =
      ((1 : ℝ) / 16) • W1 outerZ := by
    simp [W1, Prod.smul_def, smul_neg]
  rw [hw, map_smul]

private theorem Q1_inner_nonzero : Q1 phi.symm innerZ ≠ 0 := by
  have hW : W1 innerZ ≠ (0 : E 1 × E 1) := by
    intro heq
    have hf := congrArg (fun z : E 1 × E 1 => ‖z.1‖) heq
    norm_num [W1, innerZ, axis_norm] at hf
  rw [Q1_linear]
  intro heq
  apply hW
  have ha := congrArg (fun x : X 2 => A x) heq
  simpa only [A_psi, map_zero] using ha

private theorem outer_forward : phi outerX = innerZ := by
  change (if outerX ∈ S then A outerX else innerZ) = innerZ
  exact if_neg outer_not_source

private theorem off_source_actual_unguarded_rate :
    fderiv ℝ F outerX (beta hk 1 h1 (phi outerX) •
      Q1 phi.symm (phi outerX)) = (1 : ℝ) / 2 := by
  have hrate : fderiv ℝ F outerX (Q1 phi.symm outerZ) = 8 := by
    have h := (global_rates outerZ).2
    change fderiv ℝ F (psi outerZ) (Q1 phi.symm outerZ) =
      2 * (‖outerZ.1‖ ^ 2 + ‖outerZ.2‖ ^ 2) at h
    have hn : 2 * (‖outerZ.1‖ ^ 2 + ‖outerZ.2‖ ^ 2) = (8 : ℝ) := by
      norm_num [outerZ, axis_norm]
    rw [hn] at h
    simpa only [outerX] using h
  rw [outer_forward, beta_inner, one_smul, Q1_inner_scaling, map_smul, hrate]
  norm_num

#eval IO.eprintln "BOUNDARY proper-partial-rate-lemmas"

private theorem domains_and_geometry :
    phi.source ≠ Set.univ ∧ phi.target ≠ Set.univ ∧
    U ⊂ phi.source ∧ T ⊂ phi.target ∧
    U ⊆ phi.source ∧ MorseCone.radiusBall (E := E 1) (F := E 1) 1 ⊆ T ∧
    LocalGeometry F phi T U 0 0 ∧ CompactGeometry hk 1 h1 F phi T U 0 := by
  exact ⟨proper_source, proper_target, strict_U, strict_T, U_subset_source,
    (by intro z hz; exact hz), localGeometry, compactGeometry⟩

private theorem same_point_control :
    (∃ t ∈ Set.Ioo ((1 : ℝ) / 4) (1 / 2),
      let z := split hk (t • rayW)
      let x := psi z
      x ∈ U ∧ phi x = z ∧
      (phi x).1 ≠ 0 ∧ (phi x).2 ≠ 0 ∧
      (1 : ℝ) / 4 < ‖(split hk).symm (phi x)‖ ∧
      beta hk 1 h1 (phi x) = 1 / 2 ∧
      fderiv ℝ F x (V1 hk 1 h1 phi U x) = t ^ 2 ∧
      fderiv ℝ F x (Q1 phi.symm (phi x)) = 2 * t ^ 2 ∧
      fderiv ℝ F x (rawDirection (phi x)) = (59 / 75 : ℝ) * t ^ 2 ∧
      fderiv ℝ F x (beta hk 1 h1 (phi x) • rawDirection (phi x)) =
        (59 / 150 : ℝ) * t ^ 2 ∧
      fderiv ℝ F x (-(V1 hk 1 h1 phi U x)) = -(t ^ 2) ∧
      fderiv ℝ F x (rawDirection (phi x)) <
        fderiv ℝ F x (V1 hk 1 h1 phi U x) ∧
      fderiv ℝ F x (beta hk 1 h1 (phi x) • rawDirection (phi x)) <
        fderiv ℝ F x (V1 hk 1 h1 phi U x) ∧
      fderiv ℝ F x (V1 hk 1 h1 phi U x) <
        fderiv ℝ F x (Q1 phi.symm (phi x)) ∧
      fderiv ℝ F x (-(V1 hk 1 h1 phi U x)) < 0) := by
  obtain ⟨t, ht, hb⟩ := intermediate_beta
  let z := split hk (t • rayW)
  let x := psi z
  have htpos : 0 < t := by linarith [ht.1]
  have henergy : ‖z.1‖ ^ 2 + ‖z.2‖ ^ 2 = t ^ 2 := ray_energy t
  have hzK : z ∈ K hk 1 := by
    refine ⟨t • rayW, ?_, rfl⟩
    have hn : ‖t • rayW‖ = t := by
      simp [norm_smul, Real.norm_eq_abs, abs_of_nonneg htpos.le, rayW_unit]
    simpa only [Metric.mem_closedBall, dist_zero_right, hn] using ht.2.le
  have hzT : z ∈ T := compactGeometry.K_target hzK
  have hxU : x ∈ U := inverse_target hzT
  have hchart : phi x = z := phi.right_inv (T_subset_target hzT)
  have hbeta : beta hk 1 h1 (phi x) = 1 / 2 := by
    simpa only [hchart, z] using hb
  have hfirst : ‖z.1‖ = t * (3 / 5 : ℝ) := ray_first_norm t htpos.le
  have hsecond : ‖z.2‖ = t * (4 / 5 : ℝ) := ray_second_norm t htpos.le
  have hfirst_ne : (phi x).1 ≠ 0 := by
    rw [hchart]
    intro h
    have hn : ‖z.1‖ = 0 := by rw [h]; exact norm_zero
    rw [hfirst] at hn
    nlinarith
  have hsecond_ne : (phi x).2 ≠ 0 := by
    rw [hchart]
    intro h
    have hn : ‖z.2‖ = 0 := by rw [h]; exact norm_zero
    rw [hsecond] at hn
    nlinarith
  have haway : (1 : ℝ) / 4 < ‖(split hk).symm (phi x)‖ := by
    rw [hchart]
    change (1 : ℝ) / 4 < ‖(split hk).symm (split hk (t • rayW))‖
    rw [(split hk).symm_apply_apply]
    simpa [norm_smul, Real.norm_eq_abs, abs_of_nonneg htpos.le, rayW_unit] using ht.1
  have hQ : fderiv ℝ F x (Q1 phi.symm (phi x)) = 2 * t ^ 2 := by
    rw [hchart]
    simpa only [x, phi_symm, henergy] using (global_rates z).2
  have hV : fderiv ℝ F x (V1 hk 1 h1 phi U x) = t ^ 2 := by
    rw [compactGeometry.rate1, if_pos hxU, hbeta, hchart, henergy]
    ring
  have hraw : fderiv ℝ F x (rawDirection (phi x)) = (59 / 75 : ℝ) * t ^ 2 := by
    rw [hchart]
    change fderiv ℝ F (phi.symm z) (rawDirection z) = (59 / 75 : ℝ) * t ^ 2
    rw [raw_rate, hfirst, hsecond]
    ring
  have hbraw : fderiv ℝ F x
      (beta hk 1 h1 (phi x) • rawDirection (phi x)) =
        (59 / 150 : ℝ) * t ^ 2 := by
    rw [map_smul, hbeta, hraw, smul_eq_mul]
    ring
  have hrev : fderiv ℝ F x (-(V1 hk 1 h1 phi U x)) = -(t ^ 2) := by
    rw [map_neg, hV]
  have ht2 : 0 < t ^ 2 := sq_pos_of_pos htpos
  refine ⟨t, ht, hxU, hchart, hfirst_ne, hsecond_ne, haway, hbeta,
    hV, hQ, hraw, hbraw, hrev, ?_, ?_, ?_, ?_⟩
  · rw [hraw, hV]
    nlinarith
  · rw [hbraw, hV]
    nlinarith
  · rw [hV, hQ]
    nlinarith
  · rw [hrev]
    linarith

private theorem off_source_control :
    outerX ∉ phi.source ∧ outerX ∉ U ∧ phi outerX = innerZ ∧
    beta hk 1 h1 (phi outerX) = 1 ∧ Q1 phi.symm (phi outerX) ≠ 0 ∧
    V1 hk 1 h1 phi U outerX = 0 ∧
    fderiv ℝ F outerX (V1 hk 1 h1 phi U outerX) = 0 ∧
    fderiv ℝ F outerX (beta hk 1 h1 (phi outerX) •
      Q1 phi.symm (phi outerX)) = 1 / 2 ∧
    beta hk 1 h1 (phi outerX) *
      (2 * (‖(phi outerX).1‖ ^ 2 + ‖(phi outerX).2‖ ^ 2)) = 1 / 32 ∧
    fderiv ℝ F outerX (beta hk 1 h1 (phi outerX) •
      Q1 phi.symm (phi outerX)) ≠
      beta hk 1 h1 (phi outerX) *
        (2 * (‖(phi outerX).1‖ ^ 2 + ‖(phi outerX).2‖ ^ 2)) := by
  have hbeta : beta hk 1 h1 (phi outerX) = 1 := by
    rw [outer_forward, beta_inner]
  have hQ : Q1 phi.symm (phi outerX) ≠ 0 := by
    rw [outer_forward]
    exact Q1_inner_nonzero
  have hV : V1 hk 1 h1 phi U outerX = 0 := by
    simp [V1, extension, outer_not_U]
  have hrate : fderiv ℝ F outerX (V1 hk 1 h1 phi U outerX) = 0 := by
    rw [hV, map_zero]
  have hfake : beta hk 1 h1 (phi outerX) *
      (2 * (‖(phi outerX).1‖ ^ 2 + ‖(phi outerX).2‖ ^ 2)) = (1 : ℝ) / 32 := by
    rw [outer_forward, beta_inner]
    norm_num [innerZ, axis_norm]
  refine ⟨outer_not_source, outer_not_U, outer_forward, hbeta, hQ, hV,
    hrate, off_source_actual_unguarded_rate, hfake, ?_⟩
  rw [off_source_actual_unguarded_rate, hfake]
  norm_num

/- The endpoint is closed: it takes no parameters or geometry/beta hypotheses.
Its positive comparisons share one physical x.  Its separate off-source witness
uses the SAME fixed proper chart and the actual global-potential derivative. -/
theorem closed_proper_partial_anisotropic_literal_V1_control :
    (phi.source ≠ Set.univ ∧ phi.target ≠ Set.univ ∧
    U ⊂ phi.source ∧ T ⊂ phi.target ∧
    U ⊆ phi.source ∧ MorseCone.radiusBall (E := E 1) (F := E 1) 1 ⊆ T ∧
    LocalGeometry F phi T U 0 0 ∧ CompactGeometry hk 1 h1 F phi T U 0) ∧
    (∃ t ∈ Set.Ioo ((1 : ℝ) / 4) (1 / 2),
      let z := split hk (t • rayW)
      let x := psi z
      x ∈ U ∧ phi x = z ∧
      (phi x).1 ≠ 0 ∧ (phi x).2 ≠ 0 ∧
      (1 : ℝ) / 4 < ‖(split hk).symm (phi x)‖ ∧
      beta hk 1 h1 (phi x) = 1 / 2 ∧
      fderiv ℝ F x (V1 hk 1 h1 phi U x) = t ^ 2 ∧
      fderiv ℝ F x (Q1 phi.symm (phi x)) = 2 * t ^ 2 ∧
      fderiv ℝ F x (rawDirection (phi x)) = (59 / 75 : ℝ) * t ^ 2 ∧
      fderiv ℝ F x (beta hk 1 h1 (phi x) • rawDirection (phi x)) =
        (59 / 150 : ℝ) * t ^ 2 ∧
      fderiv ℝ F x (-(V1 hk 1 h1 phi U x)) = -(t ^ 2) ∧
      fderiv ℝ F x (rawDirection (phi x)) <
        fderiv ℝ F x (V1 hk 1 h1 phi U x) ∧
      fderiv ℝ F x (beta hk 1 h1 (phi x) • rawDirection (phi x)) <
        fderiv ℝ F x (V1 hk 1 h1 phi U x) ∧
      fderiv ℝ F x (V1 hk 1 h1 phi U x) <
        fderiv ℝ F x (Q1 phi.symm (phi x)) ∧
      fderiv ℝ F x (-(V1 hk 1 h1 phi U x)) < 0) ∧
    (outerX ∉ phi.source ∧ outerX ∉ U ∧ phi outerX = innerZ ∧
    beta hk 1 h1 (phi outerX) = 1 ∧ Q1 phi.symm (phi outerX) ≠ 0 ∧
    V1 hk 1 h1 phi U outerX = 0 ∧
    fderiv ℝ F outerX (V1 hk 1 h1 phi U outerX) = 0 ∧
    fderiv ℝ F outerX (beta hk 1 h1 (phi outerX) •
      Q1 phi.symm (phi outerX)) = 1 / 2 ∧
    beta hk 1 h1 (phi outerX) *
      (2 * (‖(phi outerX).1‖ ^ 2 + ‖(phi outerX).2‖ ^ 2)) = 1 / 32 ∧
    fderiv ℝ F outerX (beta hk 1 h1 (phi outerX) •
      Q1 phi.symm (phi outerX)) ≠
      beta hk 1 h1 (phi outerX) *
        (2 * (‖(phi outerX).1‖ ^ 2 + ‖(phi outerX).2‖ ^ 2))) := by
  exact ⟨domains_and_geometry, same_point_control, off_source_control⟩

#eval IO.eprintln "BOUNDARY proper-partial-closed-endpoint"
end ProperPartialAnisotropicLiteralV1
