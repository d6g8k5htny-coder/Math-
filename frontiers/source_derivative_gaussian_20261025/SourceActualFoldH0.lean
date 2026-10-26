import SourceActualFoldTorus
import ElderBridge

/-! One actual ordinary singular-H0 interval on the original-period torus.
The old typed trap, section, retraction and kernel splitting are reused literally.
The source-law endpoints derive their geometric data internally. No canonical
Morse partner, exhaustive barcode or probability bound is asserted. -/

noncomputable section
open CategoryTheory Limits Set MeasureTheory
set_option autoImplicit false

namespace SourceActualFoldH0

universe u
open SourceActualFoldTorus TorusFiltration

/-- Visible boundary and path data construct the accepted old typed trap on
exactly the same field, points, absolute levels and domain. -/
theorem toElderTrap {X : Type u} [TopologicalSpace X]
    {g : X → ℝ} {M P : X} {b d : ℝ} {D : Set X}
    (T : TorusTrapData g M P b d D) : ElderTrap g M P b d D := by
  obtain ⟨γ,hγ⟩ := T.closed_path
  exact elderTrap_of_boundary g D b d M P T.domain_closed T.frontier_bound
    T.death_lt_birth T.maximum_height T.maximum_inside T.height_ceiling
    T.older_height γ hγ

variable (K : Type u) [Field K]
variable {X : Type u} [TopologicalSpace X]
variable {g : X → ℝ} {M P : X} {b d : ℝ} {D : Set X}

/-- The actual singular-H0 point-class difference section from the old trap. -/
def h0Section (T : TorusTrapData g M P b d D) :
    elderInterval K b d ⟶ superlevel_h0Filtration g (ModuleCat.of K K) :=
  elderSection (k := K) (toElderTrap T)

/-- The accepted ordinary-H0 component projection gives the retraction. -/
def h0Retraction (T : TorusTrapData g M P b d D) :
    superlevel_h0Filtration g (ModuleCat.of K K) ⟶ elderInterval K b d :=
  elderRetraction (k := K) (toElderTrap T)

/-- These maps split the interval naturally at every increasing parameter. -/
theorem h0Section_retraction (T : TorusTrapData g M P b d D) :
    h0Section K T ≫ h0Retraction K T = 𝟙 (elderInterval K b d) :=
  elderSection_retraction (k := K) (toElderTrap T)

/-- The complement is the actual accepted retraction kernel. -/
def h0Complement (T : TorusTrapData g M P b d D) : ℝ ⥤ ModuleCat K :=
  kernel (h0Retraction K T)

/-- The old constructed natural isomorphism, with its actual kernel complement. -/
def h0DirectSummand (T : TorusTrapData g M P b d D) :
    superlevel_h0Filtration g (ModuleCat.of K K) ≅
      elderInterval K b d ⊞ h0Complement K T :=
  elderDirectSummand (k := K) (toElderTrap T)

/-- For the actual fold heights, increasing time includes birth and excludes
death, and the interval has the positive physical gap as its length. -/
theorem fold_interval_endpoints (b k r : ℝ) (hk : 0 < k) (hr : 0 < r) :
    elderActive b (b-k*r^3) (-b) ∧
      ¬ elderActive b (b-k*r^3) (-(b-k*r^3)) ∧
      -(b-k*r^3)-(-b) = k*r^3 ∧ 0 < k*r^3 := by
  have hgap : 0 < k*r^3 := mul_pos hk (pow_pos hr 3)
  exact ⟨elder_control_birth (by linarith), elder_control_death _ _, by ring, hgap⟩

open AdaptiveFoldBoundaryPath I4SmoothCarrier I4SourceConfluentPins
open I4SourceRawPinConditioning I4SourceCompactTargetMoments
open I4SourceAdaptiveFoldChart I4SourceAdaptiveFoldEstimates I4Torus

/-- A radius from the original nonzero period alone works for every coefficient
field and all later targets. On the same actual-law event, the same U,z, image
box, older point and closed path supply the literal old trap and actual ordinary
singular-H0 interval with the old retraction kernel as complement. -/
theorem sourceGapLaw_actual_torus_trap_h0 {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ (K : Type) [Field K],
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          let R := 4/Real.sqrt κ
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            ∃ (U : Set ℝ) (z : ℝ → ℝ),
              RidgeScalarData (actualFoldPotential r k sample)
                univ R (κ/2) T (3*T) T U z ∧
              ∃ ET : ElderTrap (actualTorusField hL sample)
                  (torusProjection 2 L (endpointM r)) (torusPhysicalMap L r (olderPoint z))
                  b (b-k*r^3) (torusPhysicalMap L r '' leftBox R),
                b + (3/2)*k*r^3 ≤
                  actualTorusField hL sample (torusPhysicalMap L r (olderPoint z)) ∧
                (∃ η : Path (torusProjection 2 L (endpointM r))
                    (torusPhysicalMap L r (olderPoint z)),
                  (∀ t : unitInterval, b-k*r^3 ≤ actualTorusField hL sample (η t)) ∧
                    η pathMidpoint = torusProjection 2 L (endpointS r)) ∧
                strictClearanceSet (actualTorusField hL sample)
                    (torusProjection 2 L (endpointM r)) = Iio (b-k*r^3) ∧
                strictClearanceDeath (actualTorusField hL sample)
                    (torusProjection 2 L (endpointM r)) = b-k*r^3 ∧
                Nonempty (superlevel_h0Filtration (actualTorusField hL sample)
                    (ModuleCat.of K K) ≅ elderInterval K b (b-k*r^3) ⊞
                    kernel (elderRetraction (k := K) ET)) := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_torus_trap_clearance hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K instK k₀ hk₀ r hr hrδ b k hk
  filter_upwards [h k₀ hk₀ r hr hrδ b k hk] with sample hs
  dsimp only at hs ⊢
  intro hrT hκ
  obtain ⟨U,z,hz,ht,hgain,hpath,hclear,hdeath⟩ := hs hrT hκ
  exact ⟨U,z,hz,toElderTrap ht,hgain,hpath,hclear,hdeath,
    ⟨elderDirectSummand (k := K) (toElderTrap ht)⟩⟩

/-- Closed actual-law endpoint for one ordinary singular-H0 interval and a
complement. Its only sample premises are the established numeric cutoffs;
strict clearance and its real supremum retain their exact torus meanings. -/
theorem sourceGapLaw_actual_torus_h0 {L : ℝ} (hL : L ≠ 0) :
    ∃ δ : ℝ, 0 < δ ∧ δ ≤ 1 ∧
      ∀ (K : Type) [Field K],
      ∀ k₀ : ℝ, 0 < k₀ → ∀ r : ℝ, 0 < r → r < δ →
        ∀ b k : ℝ, k₀ ≤ k → ∀ᵐ sample ∂sourceGapLaw hL r b k,
          let T := sourceT k₀ sample
          let κ := sourceKappa r k sample
          r*T^5 ≤ 1/100 → 1024*T^5 ≤ κ →
            ∃ C : ℝ ⥤ ModuleCat K,
              Nonempty (superlevel_h0Filtration (actualTorusField hL sample)
                (ModuleCat.of K K) ≅ elderInterval K b (b-k*r^3) ⊞ C) ∧
              strictClearanceSet (actualTorusField hL sample)
                  (torusProjection 2 L (endpointM r)) = Iio (b-k*r^3) ∧
              strictClearanceDeath (actualTorusField hL sample)
                  (torusProjection 2 L (endpointM r)) = b-k*r^3 := by
  obtain ⟨δ,hδ,hδ1,h⟩ := sourceGapLaw_actual_torus_trap_h0 hL
  refine ⟨δ,hδ,hδ1,?_⟩
  intro K instK k₀ hk₀ r hr hrδ b k hk
  filter_upwards [h K k₀ hk₀ r hr hrδ b k hk] with sample hs
  dsimp only at hs ⊢
  intro hrT hκ
  obtain ⟨U,z,_hz,ET,_hgain,_hpath,hclear,hdeath,hiso⟩ := hs hrT hκ
  exact ⟨kernel (elderRetraction (k := K) ET),hiso,hclear,hdeath⟩

end SourceActualFoldH0
