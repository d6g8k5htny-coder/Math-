import Specifications.P15

namespace UniversalLaw.General

variable {X : Type} [Fintype X] [DecidableEq X]

def decreasing (D : Finset (Finset X)) : Prop :=
  ∅ ∈ D ∧ ∀ U ∈ D, ∀ V : Finset X, V ⊆ U → V ∈ D

def minimalBad (D : Finset (Finset X)) (e : Finset X) : Prop :=
  e ∉ D ∧ ∀ v ∈ e, e.erase v ∈ D

def decomposable (D : Finset (Finset X)) (K : ℕ) (U : Finset X) : Prop :=
  ∃ parts : Fin K → Finset X, (∀ j, parts j ∈ D) ∧
    (∀ j j', j ≠ j' → Disjoint (parts j) (parts j')) ∧
    (Finset.univ : Finset (Fin K)).biUnion parts = U

def generatorCover (D : Finset (Finset X)) (K : ℕ)
    (G : Finset (Finset X)) : Prop :=
  ∀ U : Finset X, ¬ decomposable D K U → ∃ g ∈ G, g ⊆ U

def block {b : ℕ} (blk : X → Fin b) (i : Fin b) : Finset X :=
  Finset.univ.filter (fun v => blk v = i)

def localFamily {b : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (i : Fin b) : Finset (Finset X) := D.filter (· ⊆ block blk i)

/-- A local obstruction lives on its block, rather than on the ambient ground.
Only subsets of that block need a local generator witness. -/
def localGeneratorCover {b : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (i : Fin b) (k : ℕ) (G : Finset (Finset X)) : Prop :=
  ∀ U : Finset X, U ⊆ block blk i →
    ¬ decomposable (localFamily D blk i) k U → ∃ g ∈ G, g ⊆ U

def colorClass {K : ℕ} (U : Finset X) (f : X → Fin K) (j : Fin K) : Finset X :=
  U.filter (fun v => f v = j)

def allowed {b K : ℕ} (blk : X → Fin b) (P : Fin b → Finset (Fin K))
    (U : Finset X) (f : X → Fin K) : Prop :=
  ∀ v ∈ U, f v ∈ P (blk v)

def locallyGood {b K : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (U : Finset X) (f : X → Fin K) : Prop :=
  ∀ j : Fin K, ∀ i : Fin b, colorClass U f j ∩ block blk i ∈ D

def paletteSeparated {b K : ℕ} (D : Finset (Finset X)) (blk : X → Fin b)
    (P : Fin b → Finset (Fin K)) : Prop :=
  ∀ e : Finset X, minimalBad D e → 1 < (e.image blk).card →
    ∀ j : Fin K, ∃ i ∈ e.image blk, j ∉ P i

noncomputable def coverCost (D : Finset (Finset X)) (K : ℕ) (c : X → ℝ) : ℝ :=
  sInf {t : ℝ | ∃ G : Finset (Finset X), generatorCover D K G ∧
    UniversalLaw.Spec.P15.famPrice c G = t}

end UniversalLaw.General
