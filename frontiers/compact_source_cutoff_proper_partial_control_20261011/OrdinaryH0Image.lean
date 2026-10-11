import OrdinaryH0Elder

/-!
Actual induced-map images in ordinary singular H₀.
The strict superlevel source is explicit; no single higher closed source or barcode is assumed.
-/

noncomputable section

set_option backward.isDefEq.respectTransparency false

open CategoryTheory Set OrdinaryH0Elder

universe u

namespace OrdinaryH0Image

variable (K : Type u) [Field K]

def predicateSpace (X : TopCat.{u}) (older : X → Prop) : TopCat.{u} :=
  TopCat.of {x : X // older x}

def predicateInclusion (X : TopCat.{u}) (older : X → Prop) :
    predicateSpace X older ⟶ X :=
  TopCat.ofHom ⟨Subtype.val, continuous_subtype_val⟩

theorem pointClasses_span_top (X : TopCat.{u}) :
    Submodule.span K (Set.range (pointClass K X)) = ⊤ := by
  classical
  apply Submodule.eq_top_iff'.mpr
  intro q
  have hs : ∀ v : ZerothHomotopy X →₀ K,
      (componentEquiv K X).symm v ∈ Submodule.span K (Set.range (pointClass K X)) := by
    intro v
    induction v using Finsupp.induction_linear with
    | zero => simp
    | add a b ha hb => simpa using Submodule.add_mem _ ha hb
    | single c a =>
      obtain ⟨x, rfl⟩ := Quotient.exists_rep c
      rw [← Finsupp.smul_single_one, map_smul]
      exact Submodule.smul_mem _ a (Submodule.subset_span ⟨x, rfl⟩)
  simpa using hs ((componentEquiv K X) q)

theorem range_h0Map_eq_span_pointImages {X Y : TopCat.{u}} (g : X ⟶ Y) :
    LinearMap.range ((h0Functor K).map g).hom =
      Submodule.span K (Set.range (fun x : X => pointClass K Y (g x))) := by
  rw [LinearMap.range_eq_map, ← pointClasses_span_top K X, Submodule.map_span]
  congr 1
  ext q
  constructor
  · rintro ⟨_, ⟨x, rfl⟩, rfl⟩
    exact ⟨x, (pointClass_map K g x).symm⟩
  · rintro ⟨x, rfl⟩
    exact ⟨pointClass K X x, ⟨x, rfl⟩, pointClass_map K g x⟩

theorem olderSpan_eq_range (X : TopCat.{u}) (older : X → Prop) :
    olderSpan K X older =
      LinearMap.range ((h0Functor K).map (predicateInclusion X older)).hom := by
  rw [range_h0Map_eq_span_pointImages, olderSpan]
  congr 1
  ext q
  constructor
  · rintro ⟨x, hx, rfl⟩
    exact ⟨⟨x, hx⟩, rfl⟩
  · rintro ⟨x, rfl⟩
    exact ⟨x.1, x.2, rfl⟩

section Superlevel

variable {X : Type u} [TopologicalSpace X]

def strictSuperlevel (f : X → ℝ) (b : ℝ) : TopCat.{u} :=
  TopCat.of {x : X // b < f x}

def strictToWeak (f : X → ℝ) (b : ℝ) {h : ℝ} (hh : h ≤ b) :
    strictSuperlevel f b ⟶ superlevel f h :=
  TopCat.ofHom ⟨fun x => ⟨x.1, hh.trans (le_of_lt x.2)⟩,
    continuous_subtype_val.subtype_mk _⟩

theorem olderSpan_superlevel_eq_range (f : X → ℝ) (b : ℝ) {h : ℝ} (hh : h ≤ b) :
    olderSpan K (superlevel f h) (fun y => b < f y.1) =
      LinearMap.range ((h0Functor K).map (strictToWeak f b hh)).hom := by
  rw [range_h0Map_eq_span_pointImages, olderSpan]
  congr 1
  ext q
  constructor
  · rintro ⟨y, hy, rfl⟩
    exact ⟨⟨y.1, hy⟩, rfl⟩
  · rintro ⟨y, rfl⟩
    exact ⟨⟨y.1, hh.trans (le_of_lt y.2)⟩, y.2, rfl⟩

theorem cap_mem_range_iff {f : X → ℝ} {C : Set X} {M z : X} {b s : ℝ}
    (H : CapFirstExit.CapHyp f C M z b s) (hMb : f M = b) {h : ℝ} (hh : h ≤ b) :
    pointClass K (superlevel f h) ⟨M, by rwa [hMb]⟩ ∈
      LinearMap.range ((h0Functor K).map (strictToWeak f b hh)).hom ↔ h ≤ s := by
  rw [← olderSpan_superlevel_eq_range]
  exact cap_mem_olderSpan_iff K H hMb hh

/-- The distinguished cap point lies in this genuine closed-level image exactly at the cutoff. -/
theorem cap_mem_closedRange_iff {f : X → ℝ} {C : Set X} {M z : X} {b s : ℝ}
    (H : CapFirstExit.CapHyp f C M z b s) (hMb : f M = b) {h r : ℝ}
    (hh : h ≤ b) (hbr : b < r) (hrz : r ≤ f z) :
    pointClass K (superlevel f h) ⟨M, by rwa [hMb]⟩ ∈
      LinearMap.range ((h0Functor K).map
        (superlevelInclusion f (hh.trans (le_of_lt hbr)))).hom ↔ h ≤ s := by
  constructor
  · intro hm
    have hrange : LinearMap.range ((h0Functor K).map
        (superlevelInclusion f (hh.trans (le_of_lt hbr)))).hom ≤
        olderSpan K (superlevel f h) (fun y => b < f y.1) := by
      rw [range_h0Map_eq_span_pointImages]
      apply Submodule.span_le.mpr
      rintro _ ⟨y, rfl⟩
      exact Submodule.subset_span
        ⟨superlevelInclusion f (hh.trans (le_of_lt hbr)) y, hbr.trans_le y.2, rfl⟩
    exact (cap_mem_olderSpan_iff K H hMb hh).mp (hrange hm)
  · intro hhs
    obtain ⟨γ, hγ⟩ := H.ridge
    have hz : h ≤ f z := (hh.trans (le_of_lt hbr)).trans hrz
    have hj : JoinedIn {x | h ≤ f x} M z := ⟨γ, fun t => hhs.trans (hγ t)⟩
    have hjoin := (joinedIn_iff_joined (F := {x | h ≤ f x}) (x := M) (y := z)
      (by simpa [hMb] using hh) hz).mp hj
    have hq := (pointClass_eq_iff_joined K (superlevel f h)
      ⟨M, by rwa [hMb]⟩ ⟨z, hz⟩).mpr hjoin
    refine ⟨pointClass K (superlevel f r) ⟨z, hrz⟩, ?_⟩
    rw [pointClass_map K (superlevelInclusion f (hh.trans (le_of_lt hbr))) ⟨z, hrz⟩]
    exact hq.symm

/-- A positive separating gap forces a weak local maximum; no strictness or Morse property. -/
theorem cap_isLocalMax_of_positive_gap {f : X → ℝ} {C : Set X} {M z : X} {b s : ℝ}
    (H : CapFirstExit.CapHyp f C M z b s) (hMb : f M = b) (hsb : s < b) :
    IsLocalMax f M := by
  have hfront : M ∉ frontier C := by
    intro hm
    exact (not_le_of_gt hsb) (by simpa [hMb] using H.frontier_le M hm)
  have hinterior : M ∈ interior C := (mem_interior_iff_notMem_frontier H.mem).mpr hfront
  have hmax : IsMaxOn f C M := by
    intro x hx
    simpa [hMb] using H.ceiling x hx
  exact hmax.isLocalMax (mem_interior_iff_mem_nhds.mp hinterior)

end Superlevel
end OrdinaryH0Image
