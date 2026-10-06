import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Tactic

/-!
Transport existing support and finite ninth-moment information to the actual
residual marginal. No source-field support or moment estimate is constructed.
-/
noncomputable section
set_option autoImplicit false
open MeasureTheory
namespace CapI4ResidualLaw

/-- Source almost-everywhere support is carried to the measurable marginal. -/
theorem support_transfer {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J) (hs : ∀ᵐ ω ∂Q, 1 ≤ J ω) :
    ∀ᵐ j ∂Q.map J, 1 ≤ j := by
  exact (ae_map_iff hJ.aemeasurable
    (measurableSet_le measurable_const measurable_id)).2 hs

/-- Integrability is transported, not inferred from a totalized real integral. -/
theorem ninth_integrable_iff {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J) :
    Integrable (fun j : ℝ => |j|^9) (Q.map J) ↔
      Integrable (fun ω => |J ω|^9) Q := by
  have hphi : AEStronglyMeasurable (fun j : ℝ => |j|^9) (Q.map J) := by
    fun_prop
  simpa only [Function.comp_def] using
    (integrable_map_measure hphi hJ.aemeasurable)

/-- The actual finite absolute ninth moments agree without normalization. -/
theorem ninth_integral_eq {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J)
    (h9 : Integrable (fun ω => |J ω|^9) Q) :
    (∫ j : ℝ, |j|^9 ∂Q.map J) = ∫ ω, |J ω|^9 ∂Q := by
  exact integral_map hJ.aemeasurable
    ((ninth_integrable_iff Q J hJ).2 h9).aestronglyMeasurable

/-- The source support and bound M give precisely the marginal outer inputs. -/
theorem outer_inputs {Ω : Type*} [MeasurableSpace Ω] (Q : Measure Ω)
    (J : Ω → ℝ) (hJ : Measurable J) (hs : ∀ᵐ ω ∂Q, 1 ≤ J ω)
    (h9 : Integrable (fun ω => |J ω|^9) Q) (M : ℝ)
    (hM : (∫ ω, |J ω|^9 ∂Q) ≤ M) :
    (∀ᵐ j ∂Q.map J, 1 ≤ j) ∧
      Integrable (fun j : ℝ => |j|^9) (Q.map J) ∧
      (∫ j : ℝ, |j|^9 ∂Q.map J) ≤ M := by
  refine ⟨support_transfer Q J hJ hs,
    (ninth_integrable_iff Q J hJ).2 h9, ?_⟩
  rw [ninth_integral_eq Q J hJ h9]
  exact hM

end CapI4ResidualLaw
