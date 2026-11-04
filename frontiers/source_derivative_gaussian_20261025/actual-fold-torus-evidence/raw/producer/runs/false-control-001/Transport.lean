import SourceActualFoldDeath
import ReusedCompactFrontier

noncomputable section
open Set MeasureTheory
set_option autoImplicit false
namespace SourceActualFoldTorus

/-- Strict clearance through an actual path to a strictly higher endpoint. -/
def strictClearanceSet {X : Type*} [TopologicalSpace X] (g : X → ℝ) (M : X) : Set ℝ :=
  {h | ∃ P, g M < g P ∧ ∃ γ : Path M P, ∀ t : unitInterval, h < g (γ t)}

/-- The real supremum of the explicit strict-clearance set. -/
def strictClearanceDeath {X : Type*} [TopologicalSpace X] (g : X → ℝ) (M : X) : ℝ :=
  sSup (strictClearanceSet g M)

/-- On the old Euclidean carrier the new predicate is literally C263. -/
theorem strictClearanceSet_eq_C263 {n : ℕ}
    (g : TorusFiltration.superlevelBar_E n → ℝ) (M : TorusFiltration.superlevelBar_E n) :
    strictClearanceSet g M = TorusFiltration.superlevelBar_clearanceSet g M := rfl

/-- Visible geometric trap data, with separation derived at the strict level.
No clearance equation, selected partner or homology conclusion is a field. -/
structure TorusTrapData {X : Type*} [TopologicalSpace X]
    (g : X → ℝ) (M P : X) (b d : ℝ) (D : Set X) : Prop where
  death_lt_birth : d < b
  maximum_height : g M = b
  older_height : b < g P
  domain_closed : IsClosed D
  maximum_inside : M ∈ D
  older_outside : P ∉ D
  height_ceiling : ∀ x ∈ D, g x ≤ b
  frontier_bound : ∀ x ∈ frontier D, g x ≤ d
  strict_trace : IsClopen (TorusFiltration.elderTrap_strictTrace g D d)
  closed_path : ∃ γ : Path M P, ∀ t : unitInterval, d ≤ g (γ t)

/-- The accepted arbitrary-space threshold theorem supplies the upper cut;
the retained closed-level path supplies every strictly lower level. -/
theorem TorusTrapData.strictClearanceSet_eq_Iio {X : Type*} [TopologicalSpace X]
    {g : X → ℝ} {M P : X} {b d : ℝ} {D : Set X}
    (T : TorusTrapData g M P b d D) : strictClearanceSet g M = Iio d := by
  ext h
  constructor
  · rintro ⟨y,hy,γ,hγ⟩
    obtain ⟨t,ht⟩ := TorusFiltration.elderTrap_higher_path_meets_threshold g D d
      T.strict_trace M T.maximum_inside
      (fun x hx => (T.height_ceiling x hx).trans_eq T.maximum_height.symm) hy γ
    exact (hγ t).trans_le ht
  · intro hh
    obtain ⟨γ,hγ⟩ := T.closed_path
    exact ⟨P, T.maximum_height.trans_lt T.older_height, γ,
      fun t => hh.trans_le (hγ t)⟩

/-- The explicit clearance interval has supremum exactly d. -/
theorem TorusTrapData.strictClearanceDeath_eq {X : Type*} [TopologicalSpace X]
    {g : X → ℝ} {M P : X} {b d : ℝ} {D : Set X}
    (T : TorusTrapData g M P b d D) : strictClearanceDeath g M = d := by
  rw [strictClearanceDeath, T.strictClearanceSet_eq_Iio, csSup_Iio]



open AdaptiveFoldBoundaryPath

/-- A continuous open physical map transports the compact box and its actual
path. Frontier inclusion is enough; no injectivity premise occurs. -/
theorem scaled_rectangle_trap {X : Type*} [TopologicalSpace X] [T2Space X]
    (e : ℝ × ℝ → X) (he : Continuous e) (heo : IsOpenMap e)
    (g : X → ℝ) (V : ℝ × ℝ → ℝ) (a b d R c : ℝ) (z : ℝ → ℝ)
    (ha : 0 < a) (hpull : ∀ p, g (e p) = a * V p)
    (hm : g (e M) = b) (hs : g (e S) = d)
    (h : RectangleBoundaryPathData V R c z) :
    TorusTrapData g (e M) (e (olderPoint z)) b d (e '' leftBox R) ∧
      b + a/4 ≤ g (e (olderPoint z)) ∧
      ∃ η : Path (e M) (e (olderPoint z)),
        (∀ t : unitInterval, d ≤ g (η t)) ∧ η pathMidpoint = e S := by
  let D := e '' leftBox R
  have hcompact : IsCompact D := (isCompact_Icc.prod isCompact_Icc).image he
  have hboundary : ∀ x ∈ frontier D, g x ≤ d := by
    intro x hx
    obtain ⟨p,hp,rfl⟩ := CapFirstExit.frontier_image_subset he heo
      (isCompact_Icc.prod isCompact_Icc) hx
    rw [hpull, ← hs, hpull]
    exact mul_le_mul_of_nonneg_left (h.frontier_bound p hp) ha.le
  have hheight : ∀ x ∈ D, g x ≤ b := by
    rintro x ⟨p,hp,rfl⟩
    rw [← hm, hpull, hpull]
    exact mul_le_mul_of_nonneg_left (h.ceiling p hp) ha.le
  have hgain : b + a/4 ≤ g (e (olderPoint z)) := by
    rw [← hm, hpull, hpull]
    have hh := mul_le_mul_of_nonneg_left h.older_gain ha.le
    nlinarith only [hh]
  have holder : b < g (e (olderPoint z)) := by linarith
  obtain ⟨γ,_hgraph,hfloor,hmid⟩ := h.path
  let η := γ.map he
  have hη : ∀ t : unitInterval, d ≤ g (η t) := by
    intro t
    change d ≤ g (e (γ t))
    rw [← hs, hpull, hpull]
    exact mul_le_mul_of_nonneg_left (hfloor t) ha.le
  have htrap : TorusTrapData g (e M) (e (olderPoint z)) b d D := {
    death_lt_birth := by
      rw [← hs, ← hm, hpull, hpull]
      exact mul_lt_mul_of_pos_left h.death_lt_maximum ha
    maximum_height := hm
    older_height := holder
    domain_closed := hcompact.isClosed
    maximum_inside := mem_image_of_mem e h.maximum_mem
    older_outside := fun hP => (not_lt_of_ge (hheight _ hP)) holder
    height_ceiling := hheight
    frontier_bound := hboundary
    strict_trace := TorusFiltration.elderTrap_strictTrace_isClopen g D d
      hcompact.isClosed hboundary
    closed_path := ⟨η,hη⟩ }
  exact ⟨htrap,hgain,η,hη,congrArg e hmid⟩

end SourceActualFoldTorus
