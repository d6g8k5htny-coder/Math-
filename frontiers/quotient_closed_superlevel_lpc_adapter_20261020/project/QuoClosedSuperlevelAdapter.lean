import CriticalLevelAttainment

/-!
# Private conditional quotient closed-superlevel adapter R3

STATUS: R3 SOURCE ONLY, UNCOMPILED. No Lean process, import elaboration, kernel
audit, project test, CI run, or mathematical source program has been executed
for these R3 bytes. The R2 predecessor failed in run 39854925919 at its subtype
LPC proof transfer and proof-valued letI linter; that failure is preserved.
R3 uses an explicit equal-set homeomorphism before restricted quotient descent.
Project source: Math- PR487, 7af365e8c8db1ae0275d4efe08a70a678f153ca2.
Mathlib source: d13f23b723b8a846827a245b89c10fc7d3f11612.

This is nonexclusive private assistance, not a formal-source ownership claim.
It only transports explicit Euclidean closed-superlevel local path connectivity
to the actual torus quotient. It does not derive that Euclidean premise from
Morse data, provide a Morse chart or ridge, prove strict death drop, identify an
elder saddle, or establish an exhaustive barcode. org=0; human=0; science=NONE.
-/

noncomputable section

open Set Topology
open UniversalLaw.Spec.Lifetime TorusFiltration TorusMorseFinite

namespace TorusCriticalAttainment.QuotientSuperlevelAdapter

/-- The actual period-lattice projection is a surjective continuous open map. -/
theorem torus_proj_isOpenQuotientMap (d : ℕ) (L : ℝ) (hL : 0 < L) :
    IsOpenQuotientMap (torus_proj d L hL) where
  surjective := torus_proj_surjective d L hL
  continuous := torus_proj_continuous d L hL
  isOpenMap := (torus_proj_isCoveringMap d L hL).isOpenMap

/-- Exact preimage identity for the literal descended height, at any real level. -/
theorem closedSuperlevel_preimage (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hperiodic : IsLPeriodic d L g) (a : ℝ) :
    (torus_proj d L hL) ⁻¹'
        {q : torus_quotient d L hL | a ≤ descendedHeight d L hL g hperiodic q} =
      {x : E d | a ≤ g x} := by
  ext x
  change (a ≤ descendedHeight d L hL g hperiodic (torus_proj d L hL x)) ↔ a ≤ g x
  rw [descendedHeight_proj]

/-- Conditional transport only: Euclidean closed-superlevel LPC is an input. -/
theorem quotient_closedSuperlevel_lpc_of_euclidean
    (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hperiodic : IsLPeriodic d L g) (a : ℝ)
    (hEuclideanLPC : LocallyPathConnectedSpace {x : E d // a ≤ g x}) :
    LocallyPathConnectedSpace
      {q : torus_quotient d L hL // a ≤ descendedHeight d L hL g hperiodic q} := by
  let S : Set (torus_quotient d L hL) :=
    {q | a ≤ descendedHeight d L hL g hperiodic q}
  let : LocallyPathConnectedSpace {x : E d // a ≤ g x} := hEuclideanLPC
  let e : ((torus_proj d L hL) ⁻¹' S) ≃ₜ
      {x : E d // a ≤ g x} :=
    Homeomorph.setCongr
      (closedSuperlevel_preimage d L hL g hperiodic a)
  have hcomposed : IsOpenQuotientMap
      (S.restrictPreimage (torus_proj d L hL) ∘ e.symm) :=
    ((torus_proj_isOpenQuotientMap d L hL).restrictPreimage S).comp
      e.symm.isOpenQuotientMap
  exact hcomposed.isQuotientMap.locallyPathConnectedSpace

/-- The original quotient attainment conclusion, with its quotient LPC premise
supplied from explicit Euclidean LPC at the exact, unchanged C263 death height. -/
theorem quotient_death_attainment_of_euclidean_closedLPC
    (d : ℕ) (L : ℝ) (hL : 0 < L)
    (g : E d → ℝ) (hsmooth : IsSmooth d g) (hperiodic : IsLPeriodic d L g)
    (hmorse : IsMorseDistinct d L g) (M : E d)
    (hnonessential : ¬ superlevelBar_isEssential g M)
    (hEuclideanLPC : LocallyPathConnectedSpace
      {x : E d // superlevelBar_deathHeight g M ≤ g x}) :
    ∃ Q ∈ quotientCriticalSet d L hL g,
      g M < descendedHeight d L hL g hperiodic Q ∧
      ∃ γ : Path (torus_proj d L hL M) Q,
        (∀ t : unitInterval,
          superlevelBar_deathHeight g M ≤ descendedHeight d L hL g hperiodic (γ t)) ∧
        ∃ t : unitInterval,
          descendedHeight d L hL g hperiodic (γ t) = superlevelBar_deathHeight g M := by
  exact TorusCriticalAttainment.quotient_death_attainment
    d L hL g hsmooth hperiodic hmorse M hnonessential
    (quotient_closedSuperlevel_lpc_of_euclidean d L hL g hperiodic
      (superlevelBar_deathHeight g M) hEuclideanLPC)

end TorusCriticalAttainment.QuotientSuperlevelAdapter
