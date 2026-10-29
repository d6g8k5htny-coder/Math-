import General.Probability
import Mathlib.Order.Disjointed

namespace UniversalLaw.General
open UniversalLaw.Spec.P15
open scoped BigOperators

variable {X : Type} [Fintype X] [DecidableEq X]

/-- Source definition of a union of exactly `k` members; overlaps are permitted. -/
def unionDecomposable (D : Finset (Finset X)) (k : ℕ) (U : Finset X) : Prop :=
  ∃ parts : Fin k → Finset X, (∀ j, parts j ∈ D) ∧ Finset.univ.biUnion parts = U

/-- The historical source asks whether `U` is covered by `q` members of an arbitrary
class, which need not be decreasing. -/
def unionCoverable (A : Finset (Finset X)) (q : ℕ) (U : Finset X) : Prop :=
  ∃ parts : Fin q → Finset X, (∀ j, parts j ∈ A) ∧ U ⊆ Finset.univ.biUnion parts

/-- Disjoint partitions and the modern source's possibly overlapping unions agree for
decreasing families. The finite disjointification includes `k = 0`. -/
theorem decomposable_iff_union (D : Finset (Finset X)) (hD : decreasing D)
    (k : ℕ) (U : Finset X) : decomposable D k U ↔ unionDecomposable D k U := by
  classical
  constructor
  · rintro ⟨parts, hparts, _, hunion⟩
    exact ⟨parts, hparts, hunion⟩
  · rintro ⟨parts, hparts, hunion⟩
    obtain ⟨pieces, hle, hsup, hdisjoint⟩ := Fintype.exists_disjointed_le parts
    refine ⟨pieces, fun j => hD.2 (parts j) (hparts j) (pieces j) (hle j), hdisjoint, ?_⟩
    rw [← Finset.sup_eq_biUnion, hsup, Finset.sup_eq_biUnion, hunion]

/-- For decreasing families, covering by a union is equivalent to being a union. -/
theorem decomposable_iff_unionCoverable (D : Finset (Finset X)) (hD : decreasing D)
    (k : ℕ) (U : Finset X) : decomposable D k U ↔ unionCoverable D k U := by
  classical
  rw [decomposable_iff_union D hD]
  constructor
  · rintro ⟨parts, hparts, hunion⟩
    exact ⟨parts, hparts, by rw [hunion]⟩
  · rintro ⟨parts, hparts, hcover⟩
    refine ⟨fun j => parts j ∩ U,
      fun j => hD.2 (parts j) (hparts j) _ Finset.inter_subset_left, ?_⟩
    ext v
    constructor
    · intro hv
      obtain ⟨j, _, hj⟩ := Finset.mem_biUnion.mp hv
      exact (Finset.mem_inter.mp hj).2
    · intro hv
      obtain ⟨j, hj, hvj⟩ := Finset.mem_biUnion.mp (hcover hv)
      exact Finset.mem_biUnion.mpr ⟨j, hj, Finset.mem_inter.mpr ⟨hvj, hv⟩⟩

/-- Historical generator covers use non-coverability by arbitrary-class members. -/
def historicalGeneratorCover (A : Finset (Finset X)) (q : ℕ)
    (G : Finset (Finset X)) : Prop :=
  ∀ U : Finset X, ¬ unionCoverable A q U → ∃ g ∈ G, g ⊆ U

theorem generatorCover_iff_historical (D : Finset (Finset X)) (hD : decreasing D)
    (q : ℕ) (G : Finset (Finset X)) :
    generatorCover D q G ↔ historicalGeneratorCover D q G := by
  simp only [generatorCover, historicalGeneratorCover, decomposable_iff_unionCoverable D hD]

/-- Fixed-constant modern target, transcribed from arXiv:2608.11183v1,
Main_document.tex lines 273--303. No theorem here asserts this property universally. -/
def ThresholdStatement (k : ℕ) (L : ℝ) : Prop :=
  ∀ (Y : Type) [Fintype Y] [DecidableEq Y] (p : ℝ), 0 < p → p < 1 →
    ∀ D : Finset (Finset Y), decreasing D →
      1 - 1 / (2 * (k : ℝ)) ≤ muOf D (fun _ => p) →
      ∃ G : Finset (Finset Y), generatorCover D k G ∧
        (∑ g ∈ G, (p / L) ^ g.card) ≤ (1 : ℝ) / 2

/-- The modern conjecture; its universal constants are not supplied by this module. -/
def ModernThresholdConjecture : Prop :=
  ∃ k : ℕ, ∃ L : ℝ, 0 < k ∧ 1 ≤ L ∧ ThresholdStatement k L

/-- Fixed-constant historical Conjecture 7.1 from Talagrand's prizes/small.pdf.
This quantifies over arbitrary classes and uses coverability, as in the source. -/
def PrizeStatement (q : ℕ) : Prop :=
  ∀ (Y : Type) [Fintype Y] [DecidableEq Y] (p : ℝ), 0 < p → p < 1 →
    ∀ A : Finset (Finset Y), 1 - 1 / (q : ℝ) ≤ muOf A (fun _ => p) →
      ∃ G : Finset (Finset Y), historicalGeneratorCover A q G ∧
        (∑ g ∈ G, p ^ g.card) ≤ (1 : ℝ) / 2

/-- The historical prize target remains an unproved existential statement. -/
def HistoricalPrizeConjecture : Prop := ∃ q : ℕ, 0 < q ∧ PrizeStatement q

/-- The paper's downward-closure condition acquires empty membership at positive mass.
Thus the strengthened `decreasing` convention loses no high-mass source instances. -/
theorem decreasing_of_downwardClosed_muOf_pos (D : Finset (Finset X))
    (hclosed : ∀ U ∈ D, ∀ V : Finset X, V ⊆ U → V ∈ D)
    (p : X → ℝ) (hmu : 0 < muOf D p) : decreasing D := by
  have hne : D.Nonempty := by
    by_contra hn
    have hempty : D = ∅ := Finset.not_nonempty_iff_eq_empty.mp hn
    simp [hempty, muOf] at hmu
  obtain ⟨U, hU⟩ := hne
  exact ⟨hclosed U hU ∅ (Finset.empty_subset U), hclosed⟩

/-- The scalar probability mass threshold in the modern source. -/
theorem high_mass_pos (k : ℕ) (hk : 0 < k) (m : ℝ)
    (hm : 1 - 1 / (2 * (k : ℝ)) ≤ m) : 0 < m := by
  have hkR : (1 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have hden : (2 : ℝ) ≤ 2 * (k : ℝ) := by linarith
  have hfrac : 1 / (2 * (k : ℝ)) ≤ (1 : ℝ) / 2 :=
    one_div_le_one_div_of_le (by norm_num) hden
  linarith

/-- A high-mass source instance can use our explicit empty-admissible convention. -/
theorem decreasing_of_high_mass (D : Finset (Finset X))
    (hclosed : ∀ U ∈ D, ∀ V : Finset X, V ⊆ U → V ∈ D)
    (k : ℕ) (hk : 0 < k) (p : ℝ)
    (hmu : 1 - 1 / (2 * (k : ℝ)) ≤ muOf D (fun _ => p)) : decreasing D :=
  decreasing_of_downwardClosed_muOf_pos D hclosed _ (high_mass_pos k hk _ hmu)

/-- For `k ≥ 2`, the source's mass hypothesis makes the proved capped hazard at most
one half. This arithmetic fact supplies no local certificate or universal constants. -/
theorem cappedHazard_le_half_of_high_mass (k : ℕ) (hk : 2 ≤ k) (m : ℝ)
    (hm : 1 - 1 / (2 * (k : ℝ)) ≤ m) : cappedHazard 1 m ≤ (1 : ℝ) / 2 := by
  have hkR : (2 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
  have hden : (4 : ℝ) ≤ 2 * (k : ℝ) := by linarith
  have hfrac : 1 / (2 * (k : ℝ)) ≤ (1 : ℝ) / 4 :=
    one_div_le_one_div_of_le (by norm_num) hden
  have hmass : (3 : ℝ) / 4 ≤ m := by linarith
  have hpos : 0 < m := by linarith
  have hinv : m⁻¹ ≤ (4 : ℝ) / 3 := by
    have h := one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 3 / 4) hmass
    norm_num only [one_div, inv_div] at h
    exact h
  have hlog := Real.one_sub_inv_le_log_of_pos hpos
  have hhalf : -Real.log m ≤ (1 : ℝ) / 2 := by linarith
  rw [cappedHazard, ite_eq_left hpos, one_mul]
  exact (min_le_right _ _).trans hhalf

/-- Fully explicit finite certificate consumed by P15-B. Finding such certificates
uniformly is an additional mathematical obligation, not a conclusion of P15-B. -/
def PalettePriceCertificate (D : Finset (Finset X)) (K : ℕ)
    (p c : X → ℝ) : Prop :=
  ∃ (b : ℕ) (blk : X → Fin b) (P : Fin b → Finset (Fin K))
    (k : Fin b → ℕ) (G : Fin b → Finset (Finset X)),
    (∀ i, 0 < k i) ∧ (∀ i, k i ≤ (P i).card) ∧ paletteSeparated D blk P ∧
    (∀ i g, g ∈ G i → g ⊆ block blk i) ∧
    (∀ i, generatorCover (localFamily D blk i) (k i) (G i)) ∧
    (∀ i, famPrice c (G i) ≤ phi (1 - localMass D blk p i))

theorem famPrice_const (r : ℝ) (G : Finset (Finset X)) :
    famPrice (fun _ => r) G = ∑ g ∈ G, r ^ g.card := by
  simp only [famPrice, genPrice, Finset.prod_const]

/-- Conditional route from an ACTUAL same-price palette/local-cover certificate to
one source threshold instance. Its certificate hypothesis is not erased. -/
theorem threshold_cover_of_paletteCertificate (D : Finset (Finset X))
    (hD : decreasing D) (K : ℕ) (hK : 2 ≤ K) (L : ℝ) (hL : 1 ≤ L)
    (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1)
    (hmass : 1 - 1 / (2 * (K : ℝ)) ≤ muOf D (fun _ => p))
    (hcert : PalettePriceCertificate D K (fun _ => p) (fun _ => p / L)) :
    ∃ H : Finset (Finset X), generatorCover D K H ∧
      (∑ g ∈ H, (p / L) ^ g.card) ≤ (1 : ℝ) / 2 := by
  obtain ⟨b, blk, P, k, G, hk, hsize, hPS, hgsub, hlocal, hprice⟩ := hcert
  have hp : ∀ _ : X, 0 ≤ p ∧ p ≤ 1 := fun _ => ⟨hp0.le, hp1.le⟩
  have hc : ∀ _ : X, 0 ≤ p / L := fun _ => div_nonneg hp0.le (by linarith)
  have hbudget := paletteSeparated_budget D hD blk P k hk hsize hPS
    (fun _ => p) (fun _ => p / L) hp hc G hgsub hlocal hprice
  obtain ⟨H, hH, hcost⟩ := hbudget.2.1
  refine ⟨H, hH, ?_⟩
  rw [famPrice_const] at hcost
  exact hcost.trans (cappedHazard_le_half_of_high_mass K hK _ hmass)

/-- Precisely the missing uniform-certificate premise that would suffice for the
modern target. This theorem asserts only the implication. -/
theorem ThresholdStatement_of_certificates (K : ℕ) (hK : 2 ≤ K)
    (L : ℝ) (hL : 1 ≤ L)
    (hcert : ∀ (Y : Type) [Fintype Y] [DecidableEq Y] (p : ℝ),
      0 < p → p < 1 → ∀ D : Finset (Finset Y), decreasing D →
        1 - 1 / (2 * (K : ℝ)) ≤ muOf D (fun _ => p) →
        PalettePriceCertificate D K (fun _ => p) (fun _ => p / L)) :
    ThresholdStatement K L := by
  intro Y _ _ p hp0 hp1 D hD hmass
  exact threshold_cover_of_paletteCertificate D hD K hK L hL p hp0 hp1 hmass
    (hcert Y p hp0 hp1 D hD hmass)

end UniversalLaw.General

#print axioms UniversalLaw.General.decomposable_iff_union
#print axioms UniversalLaw.General.decomposable_iff_unionCoverable
#print axioms UniversalLaw.General.cappedHazard_le_half_of_high_mass
#print axioms UniversalLaw.General.threshold_cover_of_paletteCertificate
#print axioms UniversalLaw.General.ThresholdStatement_of_certificates
