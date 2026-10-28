import SourceActualQuotientSaddleCollar
import SourceFiniteTrig
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.Convex.PathConnected
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Convert
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Abel
import Lean.Elab.Tactic.Omega

noncomputable section
open Set Filter Topology
open UniversalLaw.Spec.Lifetime
open I4LifetimeField I4SmoothCarrier
open scoped BigOperators Topology
set_option autoImplicit false
namespace I4SourceActualSaddleUppercuts

private abbrev Point2 := Fin 2 → ℝ
private def saddleValue (u : Point2) : ℝ := -(u 0)^2 + (u 1)^2
private def targetUpper (rho eps : ℝ) : Set Point2 :=
  Metric.ball 0 rho ∩ {u | eps ≤ saddleValue u}
private def targetUpperPos (rho eps : ℝ) : Set Point2 :=
  targetUpper rho eps ∩ {u | 0 < u 1}
private def targetUpperNeg (rho eps : ℝ) : Set Point2 :=
  targetUpper rho eps ∩ {u | u 1 < 0}

private structure ClosedBranchFacts (rho eps : ℝ) : Prop where
  plus_pc : IsPathConnected (targetUpperPos rho eps)
  minus_pc : IsPathConnected (targetUpperNeg rho eps)
  disjoint : Disjoint (targetUpperPos rho eps) (targetUpperNeg rho eps)
  partition : targetUpper rho eps = targetUpperPos rho eps ∪ targetUpperNeg rho eps
  plus_witness : (![0, rho/2] : Point2) ∈ targetUpperPos rho eps
  minus_witness : (![0, -rho/2] : Point2) ∈ targetUpperNeg rho eps

private def upperTrace {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2)
    (eps : ℝ) : Set (I4Torus.SourceTorus 2 L) :=
  phi.source ∩ {z | F q + eps ≤ F z}

private structure InheritedCollar {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop where
  center_mem : q ∈ phi.source
  center_eq : phi q = 0
  source_sub : phi.source ⊆ O
  target_eq : phi.target = Metric.ball 0 rho
  field_eq : ∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2
  lower_pc : ∀ delta : ℝ, 0 ≤ delta →
    IsPathConnected (phi.source ∩ {z | F q - delta ≤ F z})
  strict_test : ∀ p ∈ phi.source ∩ {z | F q < F z},
    ∀ r ∈ phi.source ∩ {z | F q < F z},
    JoinedIn (phi.source ∩ {z | F q < F z}) p r ↔ 0 < (phi p 1)*(phi r 1)

private def UpperClause {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) (eps : ℝ) : Prop :=
  let U := upperTrace F q phi eps
  let Bplus := U ∩ {z | 0 < phi z 1}
  let Bminus := U ∩ {z | phi z 1 < 0}
  IsPathConnected Bplus ∧ IsPathConnected Bminus ∧ Disjoint Bplus Bminus ∧
    U = Bplus ∪ Bminus ∧
    (∀ p ∈ U, ∀ r ∈ U, JoinedIn U p r ↔ 0 < (phi p 1)*(phi r 1))

private def UniformCutResult {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (O : Set (I4Torus.SourceTorus 2 L))
    (rho : ℝ) (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  q ∈ phi.source ∧ phi q = 0 ∧ phi.source ⊆ O ∧
  phi.target = Metric.ball 0 rho ∧
  (∀ z ∈ phi.source, F z = F q - (phi z 0)^2 + (phi z 1)^2) ∧
  (∀ delta : ℝ, 0 ≤ delta → IsPathConnected (phi.source ∩ {z | F q-delta ≤ F z})) ∧
  0 < rho^2/4 ∧ ∀ eps : ℝ, 0 < eps → eps < rho^2/4 → UpperClause F q phi eps

private def CutoffEquality {L : ℝ} (F : I4Torus.SourceTorus 2 L → ℝ)
    (q : I4Torus.SourceTorus 2 L) (rho : ℝ)
    (phi : OpenPartialHomeomorph (I4Torus.SourceTorus 2 L) Point2) : Prop :=
  0 < rho^2/16 ∧ rho^2/16 < rho^2/4 ∧
  phi.symm (![0, rho/4] : Point2) ∈ upperTrace F q phi (rho^2/16) ∧
  phi.symm (![0, -rho/4] : Point2) ∈ upperTrace F q phi (rho^2/16) ∧
  F (phi.symm (![0, rho/4] : Point2)) = F q + rho^2/16 ∧
  F (phi.symm (![0, -rho/4] : Point2)) = F q + rho^2/16 ∧
  0 < phi (phi.symm (![0, rho/4] : Point2)) 1 ∧
  phi (phi.symm (![0, -rho/4] : Point2)) 1 < 0

end I4SourceActualSaddleUppercuts
