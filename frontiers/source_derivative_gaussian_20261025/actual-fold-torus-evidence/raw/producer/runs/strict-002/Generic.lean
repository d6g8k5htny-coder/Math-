import SourceActualFoldDeath

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

end SourceActualFoldTorus
