import ResearchFormalCoreR1.MomentTail
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Tactic

/-!
Cap I4, author-side companion; scientific effect NONE.
Source: imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md
Git blob: dfed3b8d318a3ab1950957f393307733a4bef3f2, §§6–7.
This file does NOT construct the Gaussian matrix law or prove MatrixDepthTransport.
It preserves both soft factors, the full normalizer, and the scalar far branch.
-/

noncomputable section

namespace CapI4

open MeasureTheory ResearchFormalCoreR1
open scoped ENNReal

set_option autoImplicit false

variable {Ω Ξ : Type*} [MeasurableSpace Ω] [MeasurableSpace Ξ]

def depthEvent (k r : ℝ) (lam M3 : Ω → ℝ) : Set Ω :=
  {x | lam x ≤ (4 / (3 * k)) * r * M3 x ^ 2}

def fourthEvent (k r : ℝ) (M4 : Ω → ℝ) : Set Ω :=
  {x | 3 * k / 10 < r * M4 x}

def goodCap (k r : ℝ) (lam M3 M4 : Ω → ℝ) : Set Ω :=
  {x | (4 / (3 * k)) * r * M3 x ^ 2 < lam x ∧ r * M4 x ≤ 3 * k / 10}

/-- Exact §7 Boolean reduction, including threshold equality cases. -/
theorem cap_failure_eq_union (k r : ℝ) (lam M3 M4 : Ω → ℝ) :
    (goodCap k r lam M3 M4)ᶜ = depthEvent k r lam M3 ∪ fourthEvent k r M4 := by
  classical
  ext x
  simp only [goodCap, depthEvent, fourthEvent, Set.mem_compl_iff,
    Set.mem_setOf_eq, Set.mem_union, not_and_or, not_lt, not_le]

/-- A supplied deterministic implication transfers the same union to a target event. -/
theorem cap_failure_subset (k r : ℝ) (lam M3 M4 : Ω → ℝ) (G : Set Ω)
    (hcap : goodCap k r lam M3 M4 ⊆ G) :
    Gᶜ ⊆ depthEvent k r lam M3 ∪ fourthEvent k r M4 := by
  rw [← cap_failure_eq_union]
  exact Set.compl_subset_compl.mpr hcap

/-- A fourth-moment specialization of the EXISTING finite-measure Markov interface.
Use with the tilted law itself; its joint weighted moment is an explicit premise. -/
theorem fourth_moment_tail
    (ν : Measure Ω) [IsFiniteMeasure ν] (R : Ω → ℝ)
    (r ε M : ℝ) (hr : 0 < r) (hε : 0 < ε)
    (hi : Integrable (fun x => R x ^ 4) ν)
    (hM : (∫ x, R x ^ 4 ∂ν) ≤ M) :
    (ν {x | ε < r * R x}).toReal ≤ (M / ε ^ 4) * r ^ 4 := by
  have hsub : {x | ε < r * R x} ⊆ {x | (ε / r) ^ 4 ≤ R x ^ 4} := by
    intro x hx
    have ht : ε / r ≤ R x :=
      ((div_lt_iff₀ hr).2 (by simpa only [mul_comm] using hx)).le
    exact pow_le_pow_left₀ (div_pos hε hr).le ht 4
  have hnonneg : 0 ≤ᵐ[ν] (fun x => R x ^ 4) :=
    Filter.Eventually.of_forall (fun x => by positivity)
  have ha : 0 < (ε / r) ^ 4 := pow_pos (div_pos hε hr) 4
  calc
    _ ≤ (∫ x, R x ^ 4 ∂ν) / (ε / r) ^ 4 :=
      p02_lm009_markov_event ν (fun x => R x ^ 4) {x | ε < r * R x}
        hi hnonneg ((ε / r) ^ 4) ha hsub
    _ ≤ M / (ε / r) ^ 4 := div_le_div_of_nonneg_right hM ha.le
    _ = (M / ε ^ 4) * r ^ 4 := by
      field_simp [ne_of_gt hr, ne_of_gt hε]

/-- E4 uses exactly the source threshold 3k/10, not a fifth-power surrogate. -/
theorem E4_specialization
    (ν : Measure Ω) [IsFiniteMeasure ν] (M4 : Ω → ℝ)
    (k r M : ℝ) (hk : 0 < k) (hr : 0 < r)
    (hi : Integrable (fun x => M4 x ^ 4) ν)
    (hM : (∫ x, M4 x ^ 4 ∂ν) ≤ M) :
    (ν (fourthEvent k r M4)).toReal ≤ (M / (3 * k / 10) ^ 4) * r ^ 4 :=
  fourth_moment_tail ν M4 r (3 * k / 10) M hr (by positivity) hi hM

/-- The one-dimensional integral retains lambda(lambda+b), including the mixed term. -/
theorem double_soft_integral (a b : ℝ) :
    (∫ x in (0 : ℝ)..a, x * (x + b)) = a ^ 3 / 3 + b * a ^ 2 / 2 := by
  have hp : (fun x : ℝ => x * (x + b)) = (fun x => x ^ 2 + b * x) := by
    funext x
    ring
  rw [hp, intervalIntegral.integral_add
    ((continuous_id.pow 2).intervalIntegrable 0 a)
    ((continuous_const.mul continuous_id).intervalIntegrable 0 a),
    intervalIntegral.integral_const_mul, intervalIntegral.integral_pow,
    intervalIntegral.integral_id]
  norm_num
  <;> ring

/-- Exact source (7.3); U is NOT a constant independent of the remaining eigenvalues. -/
theorem matrix_soft_integral (r D E U : ℝ) :
    (∫ x in (0 : ℝ)..(D * r * U ^ 2), x * (x + E * r * U)) =
      r ^ 3 * ((D ^ 3 / 3) * U ^ 6 + (E * D ^ 2 / 2) * U ^ 5) := by
  rw [double_soft_integral]
  ring

/-- Positive polynomial majorant; no inverse eigenvalue or spectral gap is introduced. -/
def spectralEnvelope (m : ℕ) (D E P U : ℝ) : ℝ :=
  P * U ^ (2 * m) * ((D ^ 3 / 3) * U ^ 6 + (E * D ^ 2 / 2) * U ^ 5)

noncomputable def spectralKernel (m : ℕ) (r D E P U : ℝ) : ℝ :=
  r ^ 2 * P * U ^ (2 * m) *
    (∫ x in (0 : ℝ)..(D * r * U ^ 2), x * (x + E * r * U))

/-- The determinant prefactor and the double soft integration give r^5 exactly. -/
theorem spectral_kernel_eq (m : ℕ) (r D E P U : ℝ) :
    spectralKernel m r D E P U = r ^ 5 * spectralEnvelope m D E P U := by
  unfold spectralKernel spectralEnvelope
  rw [matrix_soft_integral]
  ring

/-- OPEN analytic interface, not an axiom or an asserted theorem.
For the source realization: m>=2; U=J+Lambda; P includes the nonnegative
Gaussian/Vandermonde angular majorant over ALL remaining ordered eigenvalues.
The measure nu is allowed to be coupled; no eigenvalue independence or lambda2 floor.
This is the pre-integration bound from (6.2),(7.1),(7.2), NOT the desired r^3 tail. -/
def MatrixDepthTransport
    (μ : Measure Ω) (W lam M3 : Ω → ℝ) (k r : ℝ)
    (ν : Measure Ξ) (m : ℕ) (D E : ℝ) (P U : Ξ → ℝ) : Prop :=
  (∫ x in depthEvent k r lam M3, W x ∂μ) ≤
    ∫ z, spectralKernel m r D E (P z) (U z) ∂ν

/-- What remains after supplying the source's matrix-to-eigenvalue domination.
Integrability is retained so the Bochner integral cannot silently totalize divergence. -/
theorem depth_numerator_r5
    (μ : Measure Ω) (W lam M3 : Ω → ℝ) (k r : ℝ)
    (ν : Measure Ξ) (m : ℕ) (D E : ℝ) (P U : Ξ → ℝ) (M : ℝ)
    (ht : MatrixDepthTransport μ W lam M3 k r ν m D E P U)
    (hi : Integrable (fun z => spectralEnvelope m D E (P z) (U z)) ν)
    (hM : (∫ z, spectralEnvelope m D E (P z) (U z) ∂ν) ≤ M)
    (hr : 0 ≤ r) :
    (∫ x in depthEvent k r lam M3, W x ∂μ) ≤ M * r ^ 5 := by
  have hki : Integrable (fun z => spectralKernel m r D E (P z) (U z)) ν := by
    simpa only [spectral_kernel_eq] using hi.const_mul (r ^ 5)
  calc
    _ ≤ ∫ z, spectralKernel m r D E (P z) (U z) ∂ν := ht
    _ ≤ ∫ z, r ^ 5 * spectralEnvelope m D E (P z) (U z) ∂ν :=
      integral_mono hki (hi.const_mul _) (fun z => le_of_eq (spectral_kernel_eq _ _ _ _ _ _))
    _ = r ^ 5 * ∫ z, spectralEnvelope m D E (P z) (U z) ∂ν := integral_const_mul _ _
    _ ≤ r ^ 5 * M := mul_le_mul_of_nonneg_left hM (pow_nonneg hr 5)
    _ = M * r ^ 5 := mul_comm _ _

/-- Existing same-law normalization, NOT a Cauchy--Schwarz transfer. -/
theorem weighted_depth_r3
    (μ : Measure Ω) (W lam M3 : Ω → ℝ) (k r : ℝ)
    (ν : Measure Ξ) (m : ℕ) (D E : ℝ) (P U : Ξ → ℝ) (M cZ : ℝ)
    (hW : Integrable W μ) (hW0 : 0 ≤ᵐ[μ] W)
    (hA : MeasurableSet (depthEvent k r lam M3))
    (hr : 0 < r) (hcZ : 0 < cZ) (hM0 : 0 ≤ M)
    (hz : cZ * r ^ 2 ≤ ∫ x, W x ∂μ)
    (ht : MatrixDepthTransport μ W lam M3 k r ν m D E P U)
    (hi : Integrable (fun z => spectralEnvelope m D E (P z) (U z)) ν)
    (hM : (∫ z, spectralEnvelope m D E (P z) (U z) ∂ν) ≤ M) :
    IsProbabilityMeasure (weightedLaw μ W) ∧
      (weightedLaw μ W (depthEvent k r lam M3)).toReal ≤ (M / cZ) * r ^ 3 := by
  have hp : 0 < ∫ x, W x ∂μ :=
    lt_of_lt_of_le (mul_pos hcZ (sq_pos_of_pos hr)) hz
  refine ⟨weightedLaw_isProbabilityMeasure μ W hW hW0 hp, ?_⟩
  rw [weightedLaw_event_real μ W (depthEvent k r lam M3) hW hW0 hA hp]
  calc
    _ ≤ (M * r ^ 5) / (∫ x, W x ∂μ) :=
      div_le_div_of_nonneg_right
        (depth_numerator_r5 μ W lam M3 k r ν m D E P U M ht hi hM hr.le) hp.le
    _ ≤ (M * r ^ 5) / (cZ * r ^ 2) :=
      div_le_div_of_nonneg_left (by positivity) (mul_pos hcZ (sq_pos_of_pos hr)) hz
    _ = (M / cZ) * r ^ 3 := by
      field_simp [ne_of_gt hr, ne_of_gt hcZ]
      <;> ring

/-- Source (7.5): retaining the strict far branch is essential in m=1. -/
theorem scalar_near_or_far (lam J D r : ℝ)
    (hD : 0 < D) (hr : 0 < r) (hlam : 0 < lam)
    (hdepth : lam ≤ 2 * D * r * J ^ 2 + 2 * D * r * lam ^ 2) :
    lam ≤ 4 * D * r * J ^ 2 ∨ 1 / (4 * D * r) < lam := by
  by_cases hn : lam ≤ 4 * D * r * J ^ 2
  · exact Or.inl hn
  · right
    apply (div_lt_iff₀ (by positivity : 0 < 4 * D * r)).2
    have hn' : 4 * D * r * J ^ 2 < lam := lt_of_not_ge hn
    have hp : 0 < lam * (4 * D * r * lam - 1) := by
      nlinarith
    nlinarith

/-- Scalar near branch: upper endpoint 4DrJ^2, mixed shift ErJ^2, prefactor r^2 J^4.
This is the source J^10 moment, not the invalid m>=2 calculation holding Lambda fixed. -/
theorem scalar_soft_integral (r D E J : ℝ) :
    r ^ 2 * J ^ 4 *
      (∫ x in (0 : ℝ)..(4 * D * r * J ^ 2), x * (x + E * r * J ^ 2)) =
        r ^ 5 * (64 * D ^ 3 / 3 + 8 * E * D ^ 2) * J ^ 10 := by
  rw [double_soft_integral]
  ring

/-- Scalar far branch on any finite (including weighted) measure: source (7.6).
Use nu with density W/r^2 for its unnormalized r^4 bound; joint moment is a premise. -/
theorem scalar_far_fourth_moment
    (ν : Measure Ω) [IsFiniteMeasure ν] (lam : Ω → ℝ)
    (D r M : ℝ) (hD : 0 < D) (hr : 0 < r)
    (hi : Integrable (fun x => lam x ^ 4) ν)
    (hM : (∫ x, lam x ^ 4 ∂ν) ≤ M) :
    (ν {x | 1 / (4 * D * r) < lam x}).toReal ≤ (M / (1 / (4 * D)) ^ 4) * r ^ 4 := by
  have he : {x | 1 / (4 * D * r) < lam x} = {x | 1 / (4 * D) < r * lam x} := by
    ext x
    simp only [Set.mem_setOf_eq]
    rw [div_lt_iff₀ (by positivity : 0 < 4 * D * r),
      div_lt_iff₀ (by positivity : 0 < 4 * D)]
    congr 1 <;> ring
  rw [he]
  exact fourth_moment_tail ν lam r (1 / (4 * D)) M hr (by positivity) hi hM

/-- Union assembly for the actual good-cap event on a finite measure. -/
theorem cap_union_mass
    (ν : Measure Ω) [IsFiniteMeasure ν] (k r : ℝ) (lam M3 M4 : Ω → ℝ) :
    (ν (goodCap k r lam M3 M4)ᶜ).toReal ≤
      (ν (depthEvent k r lam M3)).toReal + (ν (fourthEvent k r M4)).toReal := by
  rw [cap_failure_eq_union]
  calc
    _ ≤ (ν (depthEvent k r lam M3) + ν (fourthEvent k r M4)).toReal :=
      ENNReal.toReal_mono (by finiteness) (measure_union_le _ _)
    _ = _ := ENNReal.toReal_add (by finiteness) (by finiteness)

/-- Conditional final power ledger: no model bound or matrix transport is manufactured. -/
theorem cap_cubic_of_tails
    (ν : Measure Ω) [IsFiniteMeasure ν] (k r C3 C4 : ℝ) (lam M3 M4 : Ω → ℝ)
    (hr : 0 ≤ r) (hr1 : r ≤ 1) (hC4 : 0 ≤ C4)
    (hdepth : (ν (depthEvent k r lam M3)).toReal ≤ C3 * r ^ 3)
    (hfourth : (ν (fourthEvent k r M4)).toReal ≤ C4 * r ^ 4) :
    (ν (goodCap k r lam M3 M4)ᶜ).toReal ≤ (C3 + C4) * r ^ 3 := by
  have hp : r ^ 4 ≤ r ^ 3 := by
    calc
      r ^ 4 = r ^ 3 * r := by ring
      _ ≤ r ^ 3 * 1 := mul_le_mul_of_nonneg_left hr1 (pow_nonneg hr 3)
      _ = r ^ 3 := mul_one _
  calc
    _ ≤ (ν (depthEvent k r lam M3)).toReal + (ν (fourthEvent k r M4)).toReal :=
      cap_union_mass ν k r lam M3 M4
    _ ≤ C3 * r ^ 3 + C4 * r ^ 4 := add_le_add hdepth hfourth
    _ ≤ C3 * r ^ 3 + C4 * r ^ 3 := add_le_add_left (mul_le_mul_of_nonneg_left hp hC4) _
    _ = (C3 + C4) * r ^ 3 := by ring

end CapI4
