import SourceActualLowerSeparation
import SourceFiniteTrig
import SourceFinitePinKernel
import SourceSmoothConditionalKernel
import SourceActualFoldTorus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Inverse
import Mathlib.Algebra.Ring.Int.Parity
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.QuadraticForm.Basic
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Convert
import Lean.Elab.Tactic.Omega

noncomputable section

open Set Filter Topology
open UniversalLaw.Spec.Lifetime
open I4LifetimeField I4SmoothCarrier I4Source I4SourceFiniteTrig
open I4SourceFinitePinKernel I4SourceSmoothConditional
open scoped BigOperators Topology Matrix

namespace ActualLowerSeparationControls

private def primaryPoly : TrigPoly :=
  [{ coeff := 1, frequency := ![2, 0], offset := 0 },
   { coeff := 1 / 16, frequency := ![3, 0], offset := 0 },
   { coeff := 3 / 16, frequency := ![1, 0], offset := 0 },
   { coeff := 1 / 32, frequency := ![3, 0], offset := -Real.pi / 2 },
   { coeff := 3 / 32, frequency := ![1, 0], offset := Real.pi / 2 },
   { coeff := 1 / 16, frequency := ![0, 1], offset := 0 }]

private def primarySample : SmoothSample 2 2 :=
  finiteShiftSample (toSource 2 primaryPoly) (zeroSample 2 2)

private theorem normalized_finite_source_field (p : TrigPoly) (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 (finiteShiftSample (toSource 2 p) (zeroSample 2 2)) x =
      eval 2 p x := by
  classical
  let v := toSource 2 p
  change (∑' m, modeCoefficient 2 2 m x *
    (finiteShiftSample v (zeroSample 2 2)).val m) = eval 2 p x
  simp only [finiteShiftSample_val, zeroSample, Pi.zero_apply, zero_add]
  calc
    (∑' m, modeCoefficient 2 2 m x * v m) =
        ∑ m ∈ v.support, modeCoefficient 2 2 m x * v m := by
      apply tsum_eq_sum
      intro m hm
      rw [Finsupp.notMem_support_iff.mp hm, mul_zero]
    _ = finitePairing (fun m => modeCoefficient 2 2 m x) v := rfl
    _ = eval 2 p x := toSource_eval (by norm_num) p x

private theorem primary_sample_eval (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 primarySample x = eval 2 primaryPoly x :=
  normalized_finite_source_field primaryPoly x

private def profile (theta : ℝ) : ℝ :=
  Real.cos (2 * theta) +
    (3 / 16 : ℝ) * (Real.cos (3 * theta) / 3 + Real.cos theta) +
    (3 / 32 : ℝ) * (Real.sin (3 * theta) / 3 - Real.sin theta)

private theorem primary_sample_formula (x : Fin 2 → ℝ) :
    smoothSourceField 2 2 primarySample x =
      profile (Real.pi * x 0) + (1 / 16 : ℝ) * Real.cos (Real.pi * x 1) := by
  rw [primary_sample_eval]
  have htwo : Real.pi * 2 * x 0 = 2 * (Real.pi * x 0) := by ring
  have hthree : Real.pi * 3 * x 0 = 3 * (Real.pi * x 0) := by ring
  norm_num [primaryPoly, eval, termEval, phase, sourceC, Fin.sum_univ_two,
    Real.cos_add, Real.sin_add, profile, htwo, hthree]
  <;> ring

private theorem primary_actual_formula (X : EuclideanSpace ℝ (Fin 2)) :
    actualField 2 2 primarySample X =
      profile (Real.pi * (coordinates 2 X) 0) +
        (1 / 16 : ℝ) * Real.cos (Real.pi * (coordinates 2 X) 1) :=
  primary_sample_formula (coordinates 2 X)

end ActualLowerSeparationControls
