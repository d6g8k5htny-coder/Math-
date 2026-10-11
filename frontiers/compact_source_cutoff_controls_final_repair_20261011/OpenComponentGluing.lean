import ElementaryHistory
import GlobalComponentMaps
import Mathlib.Topology.Algebra.Module.LocallyConvex
import Mathlib.Topology.LocallyConstant.Basic

noncomputable section
open CategoryTheory Set GlobalComponentMaps
universe u
namespace MorseOpenGluing
variable {X : Type u} [TopologicalSpace X]

/-- The actual subtype inclusion, not a supplied component chart. -/
def inclusion (U : Set X) : TopCat.of U ⟶ TopCat.of X :=
  TopCat.ofHom ⟨Subtype.val, continuous_subtype_val⟩

def inclusionMap (U : Set X) : ZerothHomotopy U → ZerothHomotopy X :=
  componentMap (inclusion U)

/-- The image of the actual attaching intersection in actual old path components. -/
def Foot (U V : Set X) (c : ZerothHomotopy U) : Prop :=
  ∃ x : U, x.val ∈ V ∧ ZerothHomotopy.mk x = c

/-- A genuine point in the nonempty path-connected patch. -/
def patchComponent (V : Set X) (hV : IsPathConnected V) : ZerothHomotopy X :=
  ZerothHomotopy.mk (Classical.choose hV)

private def Attached (U V : Set X) : Option (ZerothHomotopy U) → Prop
  | none => True
  | some c => Foot U V c

private def attachSetoid (U V : Set X) : Setoid (Option (ZerothHomotopy U)) where
  r a b := a = b ∨ (Attached U V a ∧ Attached U V b)
  iseqv := by
    refine ⟨fun _ => Or.inl rfl, ?_, ?_⟩
    · intro a b h
      exact h.elim (fun e => Or.inl e.symm) (fun h => Or.inr ⟨h.2, h.1⟩)
    · intro a b c hab hbc
      rcases hab with rfl | ⟨ha, hb⟩
      · exact hbc
      rcases hbc with rfl | ⟨_, hc⟩
      · exact Or.inr ⟨ha, hb⟩
      · exact Or.inr ⟨ha, hc⟩

private def glueLabel (U V : Set X) (x : X) : Quotient (attachSetoid U V) := by
  classical
  exact if hx : x ∈ U then Quotient.mk _ (some (ZerothHomotopy.mk ⟨x, hx⟩))
    else Quotient.mk _ none

private theorem glueLabel_old (U V : Set X) (x : U) :
    glueLabel U V x.val = Quotient.mk _ (some (ZerothHomotopy.mk x)) := by
  classical
  simp [glueLabel, x.property]

private theorem glueLabel_patch (U V : Set X) {x : X} (hx : x ∈ V) :
    glueLabel U V x = Quotient.mk _ none := by
  classical
  by_cases hu : x ∈ U
  · simp only [glueLabel, dite_eq_left hu]
    apply Quotient.sound
    exact Or.inr ⟨⟨⟨x, hu⟩, hx, rfl⟩, trivial⟩
  · simp [glueLabel, hu]

private theorem open_cover_path_constant {Y : Type*} (U V : Set X)
    (hU : IsOpen U) (hV : IsOpen V) (hcover : U ∪ V = univ)
    (F : X → Y)
    (hFU : ∀ {x y}, JoinedIn U x y → F x = F y)
    (hFV : ∀ {x y}, JoinedIn V x y → F x = F y)
    {x y : X} (p : Path x y) : F x = F y := by
  have hloc : IsLocallyConstant (fun t : ℝ => F (p.extend t)) := by
    apply (IsLocallyConstant.iff_exists_open _).2
    intro t
    have hmem : p.extend t ∈ U ∪ V := by rw [hcover]; trivial
    rcases hmem with ht | ht
    · let S := p.extend ⁻¹' U
      have hs : IsOpen S := hU.preimage p.continuous_extend
      refine ⟨pathComponentIn S t, hs.pathComponentIn t, mem_pathComponentIn_self ht, ?_⟩
      intro s hst
      have hm : JoinedIn U (p.extend t) (p.extend s) :=
        ((show JoinedIn S t s from hst).map p.continuous_extend.continuousOn).mono
          (image_preimage_subset _ _)
      exact (hFU hm).symm
    · let S := p.extend ⁻¹' V
      have hs : IsOpen S := hV.preimage p.continuous_extend
      refine ⟨pathComponentIn S t, hs.pathComponentIn t, mem_pathComponentIn_self ht, ?_⟩
      intro s hst
      have hm : JoinedIn V (p.extend t) (p.extend s) :=
        ((show JoinedIn S t s from hst).map p.continuous_extend.continuousOn).mono
          (image_preimage_subset _ _)
      exact (hFV hm).symm
  simpa only [p.extend_zero, p.extend_one] using hloc.apply_eq_of_preconnectedSpace 0 1

private theorem glueLabel_path (U V : Set X) (hU : IsOpen U) (hV : IsOpen V)
    (hcover : U ∪ V = univ) {x y : X} (p : Path x y) :
    glueLabel U V x = glueLabel U V y := by
  apply open_cover_path_constant U V hU hV hcover (glueLabel U V) _ _ p
  · intro a b hab
    rw [glueLabel_old U V ⟨a, hab.source_mem⟩,
      glueLabel_old U V ⟨b, hab.target_mem⟩]
    exact congrArg (fun c => Quotient.mk (attachSetoid U V) (some c))
      (ZerothHomotopy.sound hab.joined_subtype.somePath)
  · intro a b hab
    rw [glueLabel_patch U V hab.source_mem, glueLabel_patch U V hab.target_mem]

private theorem patch_eq_of_foot (U V : Set X) (hpatch : IsPathConnected V)
    {a : ZerothHomotopy U} (ha : Foot U V a) :
    patchComponent V hpatch = inclusionMap U a := by
  obtain ⟨x, hx, rfl⟩ := ha
  exact ZerothHomotopy.sound
    (hpatch.joinedIn _ (Classical.choose_spec hpatch).1 _ hx).somePath

private theorem inclusion_patch_iff (U V : Set X) (hU : IsOpen U) (hV : IsOpen V)
    (hcover : U ∪ V = univ) (hpatch : IsPathConnected V) (a : ZerothHomotopy U) :
    inclusionMap U a = patchComponent V hpatch ↔ Foot U V a := by
  constructor
  · induction a using ZerothHomotopy.rec with
    | mk x =>
      intro h
      have hp : Joined x.val (Classical.choose hpatch) := Quotient.exact h
      have hl := glueLabel_path U V hU hV hcover hp.somePath
      rw [glueLabel_old U V x,
        glueLabel_patch U V (Classical.choose_spec hpatch).1] at hl
      have hr := Quotient.exact hl
      change some (ZerothHomotopy.mk x) = none ∨
        (Foot U V (ZerothHomotopy.mk x) ∧ True) at hr
      rcases hr with hfalse | htrue
      · cases hfalse
      · exact htrue.1
  · intro ha
    exact (patch_eq_of_foot U V hpatch ha).symm


theorem inclusion_fiber (U V : Set X) (hU : IsOpen U) (hV : IsOpen V)
    (hcover : U ∪ V = univ) (hpatch : IsPathConnected V)
    (a b : ZerothHomotopy U) :
    inclusionMap U a = inclusionMap U b ↔ a = b ∨ (Foot U V a ∧ Foot U V b) := by
  constructor
  · induction a using ZerothHomotopy.rec with
    | mk x =>
      induction b using ZerothHomotopy.rec with
      | mk y =>
        intro h
        have hp : Joined x.val y.val := Quotient.exact h
        have hl := glueLabel_path U V hU hV hcover hp.somePath
        rw [glueLabel_old U V x, glueLabel_old U V y] at hl
        have hr := Quotient.exact hl
        change some (ZerothHomotopy.mk x) = some (ZerothHomotopy.mk y) ∨
          (Foot U V (ZerothHomotopy.mk x) ∧ Foot U V (ZerothHomotopy.mk y)) at hr
        exact hr.elim (fun e => Or.inl (Option.some.inj e)) Or.inr
  · rintro (rfl | ⟨ha, hb⟩)
    · rfl
    obtain ⟨x, hx, rfl⟩ := ha
    obtain ⟨y, hy, rfl⟩ := hb
    exact ZerothHomotopy.sound (hpatch.joinedIn _ hx _ hy).somePath

theorem component_coverage (U V : Set X) (hcover : U ∪ V = univ)
    (hpatch : IsPathConnected V) (c : ZerothHomotopy X) :
    c = patchComponent V hpatch ∨ ∃ a : ZerothHomotopy U, inclusionMap U a = c := by
  induction c using ZerothHomotopy.rec with
  | mk x =>
    have hx : x ∈ U ∪ V := by rw [hcover]; trivial
    rcases hx with hu | hv
    · exact Or.inr ⟨ZerothHomotopy.mk ⟨x, hu⟩, rfl⟩
    · exact Or.inl (ZerothHomotopy.sound
        (hpatch.joinedIn _ hv _ (Classical.choose_spec hpatch).1).somePath)

/-- Construct the primitive birth witness from empty actual intersection footprint. -/
def birthEvent (U V : Set X) (hU : IsOpen U) (hV : IsOpen V)
    (hcover : U ∪ V = univ) (hpatch : IsPathConnected V)
    (hfoot : ∀ c, ¬ Foot U V c) : ElementaryHistory.Event (inclusionMap U) := by
  refine .birth (patchComponent V hpatch) ?_ ?_ ?_
  · intro a b hab
    rcases (inclusion_fiber U V hU hV hcover hpatch a b).1 hab with he | ⟨ha, _⟩
    · exact he
    · exact False.elim (hfoot a ha)
  · rintro ⟨a, ha⟩
    exact hfoot a ((inclusion_patch_iff U V hU hV hcover hpatch a).1 ha)
  · intro c
    exact component_coverage U V hcover hpatch c

/-- A one-component attachment is a genuine nonmerge event. -/
def neutralEvent (U V : Set X) (hU : IsOpen U) (hV : IsOpen V)
    (hcover : U ∪ V = univ) (hpatch : IsPathConnected V)
    (a : ZerothHomotopy U) (hfoot : ∀ c, Foot U V c ↔ c = a) :
    ElementaryHistory.Event (inclusionMap U) := by
  refine .neutral ⟨?_, ?_⟩
  · intro x y hxy
    rcases (inclusion_fiber U V hU hV hcover hpatch x y).1 hxy with he | ⟨hx, hy⟩
    · exact he
    · exact ((hfoot x).1 hx).trans ((hfoot y).1 hy).symm
  · intro c
    rcases component_coverage U V hcover hpatch c with hc | ⟨x, hx⟩
    · refine ⟨a, ?_⟩
      exact (patch_eq_of_foot U V hpatch ((hfoot a).2 rfl)).symm.trans hc.symm
    · exact ⟨x, hx⟩

/-- Two distinct actual old components give exactly one binary merge fiber. -/
def mergeEvent (U V : Set X) (hU : IsOpen U) (hV : IsOpen V)
    (hcover : U ∪ V = univ) (hpatch : IsPathConnected V)
    (a b : ZerothHomotopy U) (hab : a ≠ b)
    (hfoot : ∀ c, Foot U V c ↔ c = a ∨ c = b) :
    ElementaryHistory.Event (inclusionMap U) := by
  refine .merge a b hab ?_ ?_
  · intro c
    rcases component_coverage U V hcover hpatch c with hc | ⟨x, hx⟩
    · refine ⟨a, ?_⟩
      exact (patch_eq_of_foot U V hpatch ((hfoot a).2 (Or.inl rfl))).symm.trans hc.symm
    · exact ⟨x, hx⟩
  · intro x y
    constructor
    · intro hxy
      rcases (inclusion_fiber U V hU hV hcover hpatch x y).1 hxy with he | ⟨hx, hy⟩
      · exact Or.inl he
      · rcases (hfoot x).1 hx with rfl | rfl <;> rcases (hfoot y).1 hy with rfl | rfl
        · exact Or.inl rfl
        · exact Or.inr (Or.inl ⟨rfl, rfl⟩)
        · exact Or.inr (Or.inr ⟨rfl, rfl⟩)
        · exact Or.inl rfl
    · rintro (he | ⟨hx, hy⟩ | ⟨hx, hy⟩)
      · exact congrArg (inclusionMap U) he
      · subst x
        subst y
        exact (inclusion_fiber U V hU hV hcover hpatch a b).2
          (Or.inr ⟨(hfoot a).2 (Or.inl rfl), (hfoot b).2 (Or.inr rfl)⟩)
      · subst x
        subst y
        exact (inclusion_fiber U V hU hV hcover hpatch b a).2
          (Or.inr ⟨(hfoot b).2 (Or.inr rfl), (hfoot a).2 (Or.inl rfl)⟩)

/-- Actual path-component maps respect composition, including inclusion chains.
This is compatibility with the existing map, not a new elder pairing theorem. -/
theorem componentMap_comp {A B C : TopCat.{u}} (g : A ⟶ B) (h : B ⟶ C)
    (c : ZerothHomotopy A) :
    componentMap h (componentMap g c) = componentMap (g ≫ h) c := by
  induction c using ZerothHomotopy.rec with
  | mk x => rfl

end MorseOpenGluing
