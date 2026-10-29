import Specifications.P15

namespace UniversalLaw.P15Completion
open UniversalLaw.Spec.P15

/-- Every label may occur in at most `s` rows for the complete `(s+1)`-clutter. -/
theorem completeClutter_condition_iff {b s K : ℕ} (P : Fin b → Finset (Fin K)) :
    (∀ e ∈ completeClutter b s, ∀ l : Fin K, ∃ i ∈ e, l ∉ P i) ↔
      ∀ l : Fin K, (Finset.univ.filter (fun i => l ∈ P i)).card ≤ s := by
  classical
  constructor
  · intro h l
    by_contra hn
    have hs : s + 1 ≤ (Finset.univ.filter (fun i => l ∈ P i)).card := by omega
    obtain ⟨e, he, hc⟩ := Finset.exists_subset_card_eq hs
    have hem : e ∈ completeClutter b s := by
      simp only [completeClutter, Finset.mem_powersetCard]
      exact ⟨Finset.subset_univ _, hc⟩
    obtain ⟨i, hi, hli⟩ := h e hem l
    exact hli (Finset.mem_filter.mp (he hi)).2
  · intro h e he l
    have hc : e.card = s + 1 := (Finset.mem_powersetCard.mp he).2
    by_contra hn
    push Not at hn
    have hsub : e ⊆ Finset.univ.filter (fun i => l ∈ P i) := by
      intro i hi
      exact Finset.mem_filter.mpr ⟨Finset.mem_univ _, hn i hi⟩
    have := (Finset.card_le_card hsub).trans (h l)
    omega

/-- Necessary row and total-capacity bounds, without positivity assumptions. -/
theorem completeClutter_palette_necessary {b s K : ℕ} {d : Fin b → ℕ}
    (h : IsPaletteFeasible b (completeClutter b s) d K) :
    (∀ i, d i ≤ K) ∧ (∑ i, d i) ≤ s * K := by
  classical
  obtain ⟨P, hd, he⟩ := h
  have hcap := (completeClutter_condition_iff P).mp he
  constructor
  · intro i
    exact (hd i).trans (by simpa using Finset.card_le_card (Finset.subset_univ (P i)))
  · calc
      (∑ i, d i) ≤ ∑ i, (P i).card := Finset.sum_le_sum (fun i _ => hd i)
      _ = ∑ l : Fin K, (Finset.univ.filter (fun i => l ∈ P i)).card := by
        simpa [Finset.bipartiteAbove, Finset.bipartiteBelow] using
          (Finset.sum_card_bipartiteAbove_eq_sum_card_bipartiteBelow
            (s := Finset.univ) (t := Finset.univ) (fun i l => l ∈ P i))
      _ ≤ ∑ _l : Fin K, s := Finset.sum_le_sum (fun l _ => hcap l)
      _ = s * K := by simp [Nat.mul_comm]

private def demandPrefix {b : ℕ} (d : Fin b → ℕ) (i : Fin b) : ℕ :=
  ∑ j ∈ Finset.univ.filter (fun j => j < i), d j

private theorem demandPrefix_add_le_of_lt {b : ℕ} (d : Fin b → ℕ)
    {i j : Fin b} (hij : i < j) : demandPrefix d i + d i ≤ demandPrefix d j := by
  classical
  have hnot : i ∉ Finset.univ.filter (fun j => j < i) := by simp
  have hsub : insert i (Finset.univ.filter (fun j => j < i)) ⊆
      Finset.univ.filter (fun k => k < j) := by
    intro k hk
    rcases Finset.mem_insert.mp hk with rfl | hk
    · simp [hij]
    · exact Finset.mem_filter.mpr ⟨Finset.mem_univ _,
        lt_trans (Finset.mem_filter.mp hk).2 hij⟩
  have h := Finset.sum_le_sum_of_subset (f := d) hsub
  simpa only [Finset.sum_insert hnot, demandPrefix, Nat.add_comm] using h

private theorem demandPrefix_add_le_total {b : ℕ} (d : Fin b → ℕ) (i : Fin b) :
    demandPrefix d i + d i ≤ ∑ j, d j := by
  classical
  have hnot : i ∉ Finset.univ.filter (fun j => j < i) := by simp
  have h := Finset.sum_le_sum_of_subset (f := d)
    (Finset.subset_univ (insert i (Finset.univ.filter (fun j => j < i))))
  simpa only [Finset.sum_insert hnot, demandPrefix, Nat.add_comm] using h

private theorem demandCode_injective {b : ℕ} (d : Fin b → ℕ) :
    Function.Injective (fun x : Sigma (fun i => Fin (d i)) => demandPrefix d x.1 + x.2.val) := by
  intro x y hxy
  rcases x with ⟨i,u⟩
  rcases y with ⟨j,v⟩
  have hij : i = j := by
    rcases lt_trichotomy i j with hij | hij | hij
    · have hle := demandPrefix_add_le_of_lt d hij
      have hu := u.isLt
      have hv := v.isLt
      simp only at hxy
      omega
    · exact hij
    · have hle := demandPrefix_add_le_of_lt d hij
      have hu := u.isLt
      have hv := v.isLt
      simp only at hxy
      omega
  subst j
  have huv : u = v := Fin.ext (by simpa using hxy)
  subst v
  rfl

/-- Consecutive cyclic intervals realize all row sizes if their total fits the columns. -/
theorem completeClutter_palette_sufficient {b s K : ℕ} {d : Fin b → ℕ}
    (hK : 0 < K) (hd : ∀ i, d i ≤ K) (htotal : (∑ i, d i) ≤ s * K) :
    IsPaletteFeasible b (completeClutter b s) d K := by
  classical
  let color (i : Fin b) (t : Fin (d i)) : Fin K :=
    ⟨(demandPrefix d i + t.val) % K, Nat.mod_lt _ hK⟩
  let P : Fin b → Finset (Fin K) := fun i => Finset.univ.image (color i)
  have hcolor_inj (i : Fin b) : Function.Injective (color i) := by
    intro t u htu
    apply Fin.ext
    have hmod : Nat.ModEq K (demandPrefix d i + t.val) (demandPrefix d i + u.val) :=
      congrArg Fin.val htu
    have htu' := Nat.ModEq.add_left_cancel' (demandPrefix d i) hmod
    exact htu'.eq_of_lt_of_lt (t.isLt.trans_le (hd i)) (u.isLt.trans_le (hd i))
  refine ⟨P, ?_, (completeClutter_condition_iff P).mpr ?_⟩
  · intro i
    simp only [P, Finset.card_image_of_injective _ (hcolor_inj i), Finset.card_univ,
      Fintype.card_fin, le_refl]
  · intro l
    let R : Finset (Fin b) := Finset.univ.filter (fun i => l ∈ P i)
    have hrep : ∀ i : R, ∃ t : Fin (d i.val), color i.val t = l := by
      intro i
      obtain ⟨t, ht, htl⟩ := Finset.mem_image.mp (Finset.mem_filter.mp i.property).2
      exact ⟨t, htl⟩
    choose t ht using hrep
    let quotient (i : R) : Fin s :=
      ⟨(demandPrefix d i.val + (t i).val) / K, by
        apply (Nat.div_lt_iff_lt_mul hK).mpr
        exact (Nat.add_lt_add_left (t i).isLt _).trans_le
          ((demandPrefix_add_le_total d i.val).trans htotal)⟩
    have hquot : Function.Injective quotient := by
      intro i j hij
      have hq : (demandPrefix d i.val + (t i).val) / K =
          (demandPrefix d j.val + (t j).val) / K := congrArg Fin.val hij
      have hmod : (demandPrefix d i.val + (t i).val) % K =
          (demandPrefix d j.val + (t j).val) % K := by
        exact (congrArg Fin.val (ht i)).trans (congrArg Fin.val (ht j)).symm
      have hcode : demandPrefix d i.val + (t i).val =
          demandPrefix d j.val + (t j).val := by
        have hi := Nat.mod_add_div (demandPrefix d i.val + (t i).val) K
        have hj := Nat.mod_add_div (demandPrefix d j.val + (t j).val) K
        rw [hq, hmod] at hi
        exact hi.symm.trans hj
      have hsigma : (⟨i.val, t i⟩ : Sigma (fun i => Fin (d i))) = ⟨j.val, t j⟩ :=
        demandCode_injective d hcode
      exact Subtype.ext (congrArg Sigma.fst hsigma)
    have hcard := Fintype.card_le_of_injective quotient hquot
    simpa only [Fintype.card_coe, Fintype.card_fin] using hcard

/-- The complete-clutter allocation problem is exactly its row and total bounds. -/
theorem completeClutter_palette_feasible_iff {b s K : ℕ} {d : Fin b → ℕ} :
    IsPaletteFeasible b (completeClutter b s) d K ↔
      (∀ i, d i ≤ K) ∧ (∑ i, d i) ≤ s * K := by
  constructor
  · exact completeClutter_palette_necessary
  · rintro ⟨hd, ht⟩
    rcases Nat.eq_zero_or_pos K with rfl | hK
    · refine ⟨fun _ => ∅, ?_, ?_⟩
      · intro i
        simpa using hd i
      · intro e he l
        exact Fin.elim0 l
    · exact completeClutter_palette_sufficient hK hd ht

private theorem ceil_div_le_iff {n s K : ℕ} (hs : 0 < s) :
    ⌈(n : ℚ) / (s : ℚ)⌉₊ ≤ K ↔ n ≤ s * K := by
  have hsQ : (0 : ℚ) < s := by exact_mod_cast hs
  rw [Nat.ceil_le, div_le_iff₀ hsQ]
  constructor
  · intro h
    have h' : n ≤ K * s := by exact_mod_cast h
    simpa [Nat.mul_comm] using h'
  · intro h
    have h' : n ≤ K * s := by simpa [Nat.mul_comm] using h
    exact_mod_cast h'

/-- Exact elementary palette formula, including nonuniform demands and the empty clutter. -/
theorem elementaryPaletteFormula : ElementaryPaletteFormula := by
  classical
  intro b s d hs hsb hd
  let M := max (Finset.univ.sup d) ⌈((∑ i, d i : ℕ) : ℚ) / (s : ℚ)⌉₊
  have hM : IsPaletteFeasible b (completeClutter b s) d M := by
    apply completeClutter_palette_feasible_iff.mpr
    constructor
    · intro i
      exact (Finset.le_sup (Finset.mem_univ i)).trans (le_max_left _ _)
    · exact (ceil_div_le_iff (by omega)).mp (le_max_right _ _)
  apply le_antisymm
  · exact Nat.sInf_le hM
  · have hatt : IsPaletteFeasible b (completeClutter b s) d
        (paletteNumber b (completeClutter b s) d) := by
      exact Nat.sInf_mem (show {K : ℕ | IsPaletteFeasible b (completeClutter b s) d K}.Nonempty
        from ⟨M, hM⟩)
    obtain ⟨hrows, htotal⟩ := completeClutter_palette_feasible_iff.mp hatt
    apply max_le
    · exact Finset.sup_le (fun i hi => hrows i)
    · exact (ceil_div_le_iff (by omega)).mpr htotal

#check completeClutter_palette_feasible_iff
#print axioms completeClutter_palette_feasible_iff
#check elementaryPaletteFormula
#print axioms elementaryPaletteFormula
end UniversalLaw.P15Completion
