import Completion.UnionBound
import Completion.Benchmark

namespace UniversalLaw.P15Completion
open UniversalLaw.Spec.P15
open scoped BigOperators

/-- Constant-coordinate prices are determined by the two geometric witness strata.
No members of the huge family are enumerated. -/
theorem benchmark_minimal_constant_price
    (hcounts : Benchmark816MinimalForbiddenCounts)
    (hsupport : ∀ U, IsMinimalForbidden benchmark816 U →
      (supp benchmark816 U).card = 1 ∨ (supp benchmark816 U).card = 4)
    (hcard_one : ∀ U, IsMinimalForbidden benchmark816 U →
      (supp benchmark816 U).card = 1 → U.card = 2)
    (hcard_four : ∀ U, IsMinimalForbidden benchmark816 U →
      (supp benchmark816 U).card = 4 → U.card = 4) (p : ℝ) :
    famPrice (fun _ => p) (minimalForbiddenFamily benchmark816) =
      500616 * p ^ 2 + (15 * 409 ^ 4) * p ^ 4 := by
  classical
  let G := minimalForbiddenFamily benchmark816
  let A := G.filter (fun U => (supp benchmark816 U).card = 1)
  let B := G.filter (fun U => (supp benchmark816 U).card = 4)
  have hG (U : Finset (Fin 6 × Fin 409)) : U ∈ G ↔ IsMinimalForbidden benchmark816 U := by
    simp only [G,minimalForbiddenFamily,Finset.mem_filter,Finset.mem_univ,true_and]
  have hAset : (A : Set (Finset (Fin 6 × Fin 409))) =
      {U | IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 1} := by
    ext U
    simp only [A,Finset.mem_coe,Finset.mem_filter,hG,Set.mem_ofPred_eq]
  have hBset : (B : Set (Finset (Fin 6 × Fin 409))) =
      {U | IsMinimalForbidden benchmark816 U ∧ (supp benchmark816 U).card = 4} := by
    ext U
    simp only [B,Finset.mem_coe,Finset.mem_filter,hG,Set.mem_ofPred_eq]
  have hAcard : A.card = 500616 := by
    rw [← Set.ncard_coe_finset, hAset,hcounts.1,Nat.choose_two_right]
  have hBcard : B.card = 15 * 409 ^ 4 := by
    rw [← Set.ncard_coe_finset,hBset,hcounts.2.1]
  have hsplit : A ∪ B = G := by
    ext U
    simp only [A,B,Finset.mem_union,Finset.mem_filter]
    constructor
    · rintro (h | h)
      · exact h.1
      · exact h.1
    · intro hu
      rcases hsupport U ((hG U).mp hu) with h1 | h4
      · exact Or.inl ⟨hu,h1⟩
      · exact Or.inr ⟨hu,h4⟩
  have hdisj : Disjoint A B := by
    apply Finset.disjoint_left.mpr
    intro U hUa hUb
    have h1 := (Finset.mem_filter.mp hUa).2
    have h4 := (Finset.mem_filter.mp hUb).2
    omega
  have hsumA : (∑ U ∈ A, genPrice (fun _ => p) U) = 500616 * p ^ 2 := by
    calc
      _ = ∑ _U ∈ A, p ^ 2 := by
        apply Finset.sum_congr rfl
        intro U hU
        have hU' := Finset.mem_filter.mp hU
        simp [genPrice,hcard_one U ((hG U).mp hU'.1) hU'.2]
      _ = _ := by simp [hAcard]
  have hsumB : (∑ U ∈ B, genPrice (fun _ => p) U) = (15 * 409 ^ 4) * p ^ 4 := by
    calc
      _ = ∑ _U ∈ B, p ^ 4 := by
        apply Finset.sum_congr rfl
        intro U hU
        have hU' := Finset.mem_filter.mp hU
        simp [genPrice,hcard_four U ((hG U).mp hU'.1) hU'.2]
      _ = _ := by
        simp only [Finset.sum_const,nsmul_eq_mul,hBcard,Nat.cast_mul,Nat.cast_ofNat,Nat.cast_pow]
  change (∑ U ∈ G, genPrice (fun _ => p) U) = _
  rw [← hsplit,Finset.sum_union hdisj,hsumA,hsumB]

theorem benchmark816UnionBound_of_counts
    (hcounts : Benchmark816MinimalForbiddenCounts)
    (hsupport : ∀ U, IsMinimalForbidden benchmark816 U →
      (supp benchmark816 U).card = 1 ∨ (supp benchmark816 U).card = 4)
    (hcard_one : ∀ U, IsMinimalForbidden benchmark816 U →
      (supp benchmark816 U).card = 1 → U.card = 2)
    (hcard_four : ∀ U, IsMinimalForbidden benchmark816 U →
      (supp benchmark816 U).card = 4 → U.card = 4) : Benchmark816UnionBound := by
  have hp : ∀ _v : Fin 6 × Fin 409, 0 ≤ (1 : ℝ) / 40900 ∧ (1 : ℝ) / 40900 ≤ 1 := by
    intro v
    norm_num
  have hu := minimalForbidden_union_bound benchmark816 (fun _ => (1 : ℝ) / 40900) hp
  rw [benchmark_minimal_constant_price hcounts hsupport hcard_one hcard_four] at hu
  have heq : (500616 * ((1 : ℝ) / 40900) ^ 2 +
      (15 * 409 ^ 4) * ((1 : ℝ) / 40900) ^ 4) = 500616 / 40900 ^ 2 + 15 / 100 ^ 4 := by
    norm_num
  rw [heq] at hu
  have harith : (500616 / 40900 ^ 2 + 15 / 100 ^ 4 : ℝ) = 2449227 / 8180000000 := by
    norm_num
  have hlt : (2449227 / 8180000000 : ℝ) < 3 / 10000 := by norm_num
  refine ⟨hu,harith,hlt,?_⟩
  rw [harith] at hu
  linarith

/-- The exact benchmark probability display, proved from the complete geometric
witness count and the finite probability union bound. -/
theorem benchmark816UnionBound : Benchmark816UnionBound :=
  benchmark816UnionBound_of_counts benchmark816MinimalForbiddenCounts
    benchmark_minimal_support benchmark_minimal_card_one benchmark_minimal_card_four

#check benchmark816UnionBound
#print axioms benchmark816UnionBound

end UniversalLaw.P15Completion
