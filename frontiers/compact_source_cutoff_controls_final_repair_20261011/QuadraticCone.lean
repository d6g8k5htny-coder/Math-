import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Normed.Module.Connected
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Analysis.Normed.Lp.ProdLp
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Tactic

noncomputable section
open Set
open scoped Convex
namespace MorseCone
variable {E F : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F]

def quadratic (x : E × F) : ℝ := ‖x.1‖ ^ 2 - ‖x.2‖ ^ 2

def radiusBall (ρ : ℝ) : Set (E × F) := {x | ‖x.1‖ ^ 2 + ‖x.2‖ ^ 2 < ρ ^ 2}

def cone (ρ : ℝ) : Set (E × F) := {x | ‖x.2‖ ≤ ‖x.1‖ ∧ x ∈ radiusBall ρ}

def puncture (ρ : ℝ) : Set (E × F) := cone ρ \ {0}

def positiveLobe (ρ : ℝ) : Set (ℝ × F) := {x | x ∈ cone ρ ∧ 0 < x.1}

def negativeLobe (ρ : ℝ) : Set (ℝ × F) := {x | x ∈ cone ρ ∧ x.1 < 0}

private theorem radius_convex (ρ : ℝ) (hρ : 0 < ρ) :
    Convex ℝ (radiusBall (E := E) (F := F) ρ) := by
  have he : radiusBall (E := E) (F := F) ρ =
      (WithLp.linearEquiv 2 ℝ (E × F)).symm ⁻¹' Metric.ball 0 ρ := by
    ext x
    simp only [mem_preimage, Metric.mem_ball, dist_zero_right, WithLp.coe_symm_linearEquiv]
    change ‖x.1‖ ^ 2 + ‖x.2‖ ^ 2 < ρ ^ 2 ↔ ‖WithLp.toLp 2 x‖ < ρ
    have hn : ‖WithLp.toLp 2 x‖^2 = ‖x.1‖^2+‖x.2‖^2 := by
      simpa only [WithLp.toLp_fst, WithLp.toLp_snd] using WithLp.prod_norm_sq_eq_of_L2 (WithLp.toLp 2 x)
    rw [← hn]
    exact sq_lt_sq₀ (norm_nonneg _) hρ.le
  rw [he]
  exact (convex_ball (0 : WithLp 2 (E × F)) ρ).linear_preimage
    (WithLp.linearEquiv 2 ℝ (E × F)).symm.toLinearMap

private theorem zero_mem_cone (ρ : ℝ) (hρ : 0 < ρ) :
    (0 : E × F) ∈ cone ρ := by
  simp only [cone, radiusBall, mem_ofPred_eq, Prod.fst_zero, Prod.snd_zero, norm_zero,
    zero_pow (by decide : 2 ≠ 0), zero_add, le_refl, true_and]
  positivity

private theorem cone_star (ρ : ℝ) (hρ : 0 < ρ) :
    StarConvex ℝ (0 : E × F) (cone ρ) := by
  intro x hx a b ha hb hab
  constructor
  · change ‖a • (0 : F) + b • x.2‖ ≤ ‖a • (0 : E) + b • x.1‖
    simpa only [smul_zero, zero_add, norm_smul, Real.norm_eq_abs, abs_of_nonneg hb]
      using mul_le_mul_of_nonneg_left hx.1 hb
  · exact radius_convex ρ hρ (zero_mem_cone ρ hρ).2 hx.2 ha hb hab

private theorem positive_convex (ρ : ℝ) (hρ : 0 < ρ) :
    Convex ℝ (positiveLobe (F := F) ρ) := by
  intro x hx y hy a b ha hb hab
  have hp : 0 < a * x.1 + b * y.1 := by
    by_cases hz : a = 0
    · have hb1 : b = 1 := by linarith
      simpa [hz, hb1] using hy.2
    · exact add_pos_of_pos_of_nonneg (mul_pos (lt_of_le_of_ne ha (Ne.symm hz)) hx.2)
        (mul_nonneg hb hy.2.le)
  refine ⟨⟨?_, radius_convex ρ hρ hx.1.2 hy.1.2 ha hb hab⟩, hp⟩
  change ‖a • x.2 + b • y.2‖ ≤ ‖a * x.1 + b * y.1‖
  rw [Real.norm_eq_abs, abs_of_pos hp]
  calc
    _ ≤ ‖a • x.2‖ + ‖b • y.2‖ := norm_add_le _ _
    _ = a * ‖x.2‖ + b * ‖y.2‖ := by simp [norm_smul, abs_of_nonneg ha, abs_of_nonneg hb]
    _ ≤ a * x.1 + b * y.1 := by
      have hx' : ‖x.2‖ ≤ x.1 := by simpa [Real.norm_eq_abs, abs_of_pos hx.2] using hx.1.1
      have hy' : ‖y.2‖ ≤ y.1 := by simpa [Real.norm_eq_abs, abs_of_pos hy.2] using hy.1.1
      exact add_le_add (mul_le_mul_of_nonneg_left hx' ha) (mul_le_mul_of_nonneg_left hy' hb)

theorem cone_pathConnected (ρ : ℝ) (hρ : 0 < ρ) :
    IsPathConnected (cone (E := E) (F := F) ρ) := by
  exact (cone_star ρ hρ).isPathConnected (zero_mem_cone ρ hρ)

theorem cone_zero_positive (ρ : ℝ) (hρ : 0 < ρ) :
    cone (E := EuclideanSpace ℝ (Fin 0)) (F := F) ρ = {0} := by
  ext x
  constructor
  · intro hx
    have he : x.1 = 0 := Subsingleton.elim _ _
    have hf : x.2 = 0 := norm_eq_zero.mp (le_antisymm (by simpa [he] using hx.1) (norm_nonneg _))
    exact mem_singleton_iff.mpr (Prod.ext he hf)
  · rintro rfl
    exact zero_mem_cone ρ hρ

theorem one_positive_lobe (ρ : ℝ) (hρ : 0 < ρ) :
    IsPathConnected (positiveLobe (F := F) ρ) := by
  apply (positive_convex ρ hρ).isPathConnected
  refine ⟨(ρ / 2, 0), ?_⟩
  change (‖(0 : F)‖ ≤ ‖ρ / 2‖ ∧ ‖ρ / 2‖ ^ 2 + ‖(0 : F)‖ ^ 2 < ρ ^ 2) ∧ 0 < ρ / 2
  simp only [norm_zero, Real.norm_eq_abs, abs_of_pos (by positivity : 0 < ρ / 2), zero_pow (by decide : 2 ≠ 0), add_zero]
  constructor
  · constructor <;> nlinarith
  · positivity

theorem one_negative_lobe (ρ : ℝ) (hρ : 0 < ρ) :
    IsPathConnected (negativeLobe (F := F) ρ) := by
  have he : negativeLobe (F := F) ρ = (fun x : ℝ × F => (-x.1, x.2)) '' positiveLobe ρ := by
    ext x
    constructor
    · intro hx
      refine ⟨(-x.1, x.2), ?_, by simp⟩
      simpa [positiveLobe, negativeLobe, cone, radiusBall, norm_neg] using hx
    · rintro ⟨y, hy, rfl⟩
      simpa [positiveLobe, negativeLobe, cone, radiusBall, norm_neg] using hy
  rw [he]
  exact (one_positive_lobe ρ hρ).image (by fun_prop)

theorem one_puncture_partition (ρ : ℝ) :
    puncture (E := ℝ) (F := F) ρ = positiveLobe ρ ∪ negativeLobe ρ := by
  ext x
  constructor
  · intro hx
    have hne : x.1 ≠ 0 := by
      intro hzero
      have hz : x.2 = 0 := norm_eq_zero.mp (le_antisymm (by simpa [hzero] using hx.1.1) (norm_nonneg _))
      exact hx.2 (mem_singleton_iff.mpr (Prod.ext hzero hz))
    rcases lt_or_gt_of_ne hne with hn | hp
    · exact Or.inr ⟨hx.1, hn⟩
    · exact Or.inl ⟨hx.1, hp⟩
  · rintro (hx | hx)
    · refine ⟨hx.1, ?_⟩
      intro he
      have : x = 0 := mem_singleton_iff.mp he
      simpa [this] using hx.2
    · refine ⟨hx.1, ?_⟩
      intro he
      have : x = 0 := mem_singleton_iff.mp he
      simpa [this] using hx.2

theorem one_lobes_separated (ρ : ℝ) {x y : ℝ × F}
    (hx : x ∈ positiveLobe ρ) (hy : y ∈ negativeLobe ρ) :
    ¬ JoinedIn (puncture ρ) x y := by
  intro h
  have hi := isPreconnected_Icc.intermediate_value
    (show (1 : ℝ) ∈ Icc 0 1 by simp) (show (0 : ℝ) ∈ Icc 0 1 by simp)
    (h.somePath.continuous_extend.fst.continuousOn)
  have hm : (0 : ℝ) ∈ Icc (h.somePath.extend 1).1 (h.somePath.extend 0).1 := by
    simpa using And.intro hy.2.le hx.2.le
  obtain ⟨t, ht, he⟩ := hi hm
  have hv : h.somePath.extend t ∈ puncture ρ := by
    rw [h.somePath.extend_apply ht]
    exact h.somePath_mem ⟨t, ht⟩
  have hz : (h.somePath.extend t).2 = 0 := norm_eq_zero.mp
    (le_antisymm (by simpa [he] using hv.1.1) (norm_nonneg _))
  exact hv.2 (mem_singleton_iff.mpr (Prod.ext he hz))

private theorem puncture_positive {ρ : ℝ} {x : E × F} (hx : x ∈ puncture ρ) :
    0 < ‖x.1‖ := by
  apply lt_of_le_of_ne (norm_nonneg _)
  intro he
  have hy : x.1 = 0 := norm_eq_zero.mp he.symm
  have hz : x.2 = 0 := norm_eq_zero.mp (le_antisymm (by simpa [hy] using hx.1.1) (norm_nonneg _))
  exact hx.2 (mem_singleton_iff.mpr (Prod.ext hy hz))

private theorem joined_axis {ρ : ℝ} {x : E × F} (hx : x ∈ puncture ρ) :
    JoinedIn (puncture ρ) x (x.1, 0) := by
  refine JoinedIn.ofLine (f := fun t : ℝ => (x.1, (1-t) • x.2)) (by fun_prop)
    (by simp) (by simp) ?_
  rintro q ⟨t, ht, rfl⟩
  have hb : 0 ≤ 1-t := by linarith [ht.2]
  have hb1 : 1-t ≤ 1 := by linarith [ht.1]
  have hn : ‖(1-t) • x.2‖ ≤ ‖x.2‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg hb]
    nlinarith [norm_nonneg x.2]
  refine ⟨⟨hn.trans hx.1.1, ?_⟩, ?_⟩
  · change ‖x.1‖^2+‖(1-t) • x.2‖^2<ρ^2
    have hs := sq_le_sq₀ (norm_nonneg ((1-t) • x.2)) (norm_nonneg x.2)
    have hbound : ‖x.1‖^2+‖x.2‖^2<ρ^2 := hx.1.2
    nlinarith [hbound, (hs.mpr hn)]
  · intro hzero
    have hf := congrArg Prod.fst (mem_singleton_iff.mp hzero)
    exact (norm_pos_iff.mp (puncture_positive hx)) hf

private theorem joined_normalized (ρ : ℝ) (hρ : 0 < ρ) {y : E}
    (hy : 0 < ‖y‖) (hyρ : ‖y‖ < ρ) :
    JoinedIn (puncture (F := F) ρ) (y, 0) (((ρ/2)/‖y‖) • y, 0) := by
  let fac : ℝ := (ρ/2)/‖y‖
  have hl : 0 < fac := by dsimp [fac]; positivity
  have hn : ‖fac • y‖ = ρ/2 := by
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos hl]
    dsimp [fac]
    field_simp
  have hball : [y -[ℝ] fac • y] ⊆ Metric.ball 0 ρ :=
    (convex_ball (0:E) ρ).segment_subset
      (by simpa using hyρ) (by simpa [hn] using (show ρ/2<ρ by linarith))
  refine JoinedIn.of_segment_subset ?_
  rintro q ⟨a,b,ha,hb,hab,rfl⟩
  have ht : 0 < a+b*fac := by
    by_cases ha0 : a=0
    · have hb1 : b=1 := by linarith
      simpa [ha0,hb1] using hl
    · exact add_pos_of_pos_of_nonneg (lt_of_le_of_ne ha (Ne.symm ha0)) (mul_nonneg hb hl.le)
  have hs : a • y + b • (fac • y) = (a+b*fac) • y := by rw [add_smul,mul_smul]
  have hbnd : ‖(a+b*fac) • y‖ < ρ := by
    simpa [hs] using hball ⟨a,b,ha,hb,hab,rfl⟩
  simp only [Prod.smul_mk, Prod.mk_add_mk, smul_zero, add_zero]
  change ((a • y + b • (fac • y), (0 : F)) ∈ puncture ρ)
  rw [hs]
  refine ⟨⟨by simp, ?_⟩, ?_⟩
  · change ‖(a+b*fac) • y‖^2 + ‖(0:F)‖^2 < ρ^2
    simpa using (sq_lt_sq₀ (norm_nonneg _) hρ.le).2 hbnd
  · intro he
    have he' : (a+b*fac) • y = 0 := congrArg Prod.fst (mem_singleton_iff.mp he)
    exact (smul_ne_zero (ne_of_gt ht) (norm_pos_iff.mp hy)) he'

theorem higher_puncture_pathConnected (ρ : ℝ) (hρ : 0 < ρ)
    (hE : 1 < Module.rank ℝ E) : IsPathConnected (puncture (E := E) (F := F) ρ) := by
  have hs := isPathConnected_sphere hE (0 : E) (r := ρ/2) (by positivity)
  obtain ⟨y,hy,hjoin⟩ := hs
  have hyn : ‖y‖ = ρ/2 := by simpa using hy
  refine ⟨(y,0), ⟨⟨by simp, ?_⟩, ?_⟩, ?_⟩
  · change ‖y‖^2+‖(0:F)‖^2<ρ^2
    simp only [norm_zero,zero_pow (by decide : 2≠0),add_zero,hyn]
    nlinarith
  · intro he
    have he' : y=0 := congrArg Prod.fst (mem_singleton_iff.mp he)
    have : ρ/2=0 := by simpa [he'] using hyn.symm
    linarith
  · intro x hx
    have hp := puncture_positive hx
    have hxρ : ‖x.1‖ < ρ := by
      have hh : ‖x.1‖^2 < ρ^2 := lt_of_le_of_lt (le_add_of_nonneg_right (sq_nonneg ‖x.2‖)) hx.1.2
      exact (sq_lt_sq₀ (norm_nonneg _) hρ.le).1 hh
    let v := ((ρ/2)/‖x.1‖) • x.1
    have hvn : ‖v‖=ρ/2 := by
      dsimp [v]
      rw [norm_smul, Real.norm_eq_abs, abs_of_pos (by positivity)]
      field_simp
    have hv : v ∈ Metric.sphere 0 (ρ/2) := by simpa using hvn
    have hmap := (hjoin hv).map (f := fun z : E => (z,(0:F))) (by fun_prop)
    have hmap' : JoinedIn (puncture (F := F) ρ) (y,(0:F)) (v,(0:F)) := hmap.mono (by
      rintro q ⟨z,hz,rfl⟩
      have hn : ‖z‖=ρ/2 := by simpa using hz
      refine ⟨⟨by simp, ?_⟩, ?_⟩
      · change ‖z‖^2+‖(0:F)‖^2<ρ^2
        simp only [norm_zero,zero_pow (by decide : 2≠0),add_zero,hn]
        nlinarith
      · intro he
        have he' : z=0 := congrArg Prod.fst (mem_singleton_iff.mp he)
        have : ρ/2=0 := by simpa [he'] using hn.symm
        linarith)
    exact hmap'.trans ((joined_axis hx).trans (joined_normalized ρ hρ hp hxρ)).symm

end MorseCone
