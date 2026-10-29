import Closure.Assembly
import Completion.Structural
import Completion.PaletteFormula
import Completion.Benchmark
import Completion.BenchmarkPrices
import Completion.BenchmarkUnion
import Completion.Numerics

open Lean Elab Command

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.PaletteNumberAttained F :=
  UniversalLaw.P15Closure.paletteNumberAttained F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.MinimalForbiddenCharacterisation F :=
  UniversalLaw.P15Completion.minimalForbiddenCharacterisation F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.LocalRestriction F :=
  UniversalLaw.P15Closure.localRestriction F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.LocalDecomposability F :=
  UniversalLaw.P15Completion.localDecomposability F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.LocalObstructionIsFullBlock F :=
  UniversalLaw.P15Completion.localObstructionIsFullBlock F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.LocalPriceChain F :=
  UniversalLaw.P15Closure.localPriceChain F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.IndependentBlockHazard F :=
  UniversalLaw.P15Closure.independentBlockHazard F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.FullBlockCoverIff F :=
  UniversalLaw.P15Closure.fullBlockCoverIff F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.CoverCostHazardBound F :=
  UniversalLaw.P15Closure.coverCostHazardBound F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.WholeGroundChromaticNumber F :=
  UniversalLaw.P15Completion.wholeGroundChromaticNumber F

example : UniversalLaw.Spec.P15.ElementaryPaletteFormula :=
  UniversalLaw.P15Completion.elementaryPaletteFormula

example : UniversalLaw.Spec.P15.TriangleNeedsThree :=
  UniversalLaw.Proofs.P15Elementary.triangleNeedsThree

example : UniversalLaw.Spec.P15.Benchmark816IsRealized :=
  UniversalLaw.P15Completion.benchmark816IsRealized

example : UniversalLaw.Spec.P15.Benchmark816Palette :=
  UniversalLaw.P15Completion.benchmark816Palette

example : UniversalLaw.Spec.P15.Benchmark816Cover :=
  UniversalLaw.P15Completion.benchmark816Cover

example : UniversalLaw.Spec.P15.Benchmark816WholeGround :=
  UniversalLaw.P15Completion.benchmark816WholeGround

example : UniversalLaw.Spec.P15.Benchmark816MinimalForbiddenCounts :=
  UniversalLaw.P15Completion.benchmark816MinimalForbiddenCounts

example : UniversalLaw.Spec.P15.Benchmark816Price :=
  UniversalLaw.P15Completion.benchmark816Price

example : UniversalLaw.Spec.P15.Benchmark816UnionBound :=
  UniversalLaw.P15Completion.benchmark816UnionBound

example : UniversalLaw.Spec.P15.TwoCoordGeneratorPrices :=
  UniversalLaw.Proofs.P15Elementary.twoCoordGeneratorPrices

example : UniversalLaw.Spec.P15.DemandOneRefutation :=
  UniversalLaw.Proofs.P15Elementary.demandOneRefutation

example : UniversalLaw.Spec.P15.LogOnePlusBelowIdentity :=
  UniversalLaw.Proofs.P15Elementary.logOnePlusBelowIdentity

example : UniversalLaw.Spec.P15.LogRatioBound :=
  UniversalLaw.Proofs.P15Elementary.logRatioBound

example : UniversalLaw.Spec.P15.RatioExponentBound :=
  UniversalLaw.Proofs.P15Elementary.ratioExponentBound

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.RestrictedLocalBudget F :=
  UniversalLaw.P15Closure.restrictedLocalBudget F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.RestrictedTransformedPriceBudget F :=
  UniversalLaw.P15Closure.restrictedTransformedPriceBudget F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.RhoTestSufficient F :=
  UniversalLaw.P15Closure.rhoTestSufficient F

example : UniversalLaw.Spec.P15.CapTestAtTwoThirds :=
  UniversalLaw.Proofs.P15Elementary.capTestAtTwoThirds

example : UniversalLaw.Spec.P15.Benchmark816TransformedRange :=
  UniversalLaw.P15Completion.benchmark816TransformedRange

example : UniversalLaw.Spec.P15.Benchmark816RationalPrice :=
  UniversalLaw.P15Completion.benchmark816RationalPrice

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.FullTransformedPriceBudget F :=
  UniversalLaw.P15Closure.fullTransformedPriceBudget F

example : UniversalLaw.Spec.P15.RhoStarEnclosure :=
  UniversalLaw.P15Completion.rhoStarEnclosure

example : UniversalLaw.Spec.P15.RhoStarBelowSixSevenths :=
  UniversalLaw.Proofs.P15Elementary.rhoStarBelowSixSevenths

example : UniversalLaw.Spec.P15.HazardStarPositive :=
  UniversalLaw.Proofs.P15Elementary.hazardStarPositive

example : UniversalLaw.Spec.P15.CoordinatewiseConcavity :=
  UniversalLaw.P15Closure.coordinatewiseConcavity

example : UniversalLaw.Spec.P15.HazardProductBound :=
  UniversalLaw.P15Closure.hazardProductBound

example : UniversalLaw.Spec.P15.HazardPhiBound :=
  UniversalLaw.P15Closure.hazardPhiBound

example : UniversalLaw.Spec.P15.FullGroundPriceBound :=
  UniversalLaw.P15Closure.fullGroundPriceBound

example : UniversalLaw.Spec.P15.PhiAtPStar :=
  UniversalLaw.Proofs.P15Elementary.phiAtPStar

example : UniversalLaw.Spec.P15.FullGroundBudgetIff :=
  UniversalLaw.P15Closure.fullGroundBudgetIff

example : UniversalLaw.Spec.P15.CapacityHazardIsBinomial :=
  UniversalLaw.Proofs.P15Elementary.capacityHazardIsBinomial

example : UniversalLaw.Spec.P15.OddMajorityIdentity :=
  UniversalLaw.Proofs.P15Elementary.oddMajorityIdentity

example : UniversalLaw.Spec.P15.CapacityWorstCase :=
  UniversalLaw.Proofs.P15Elementary.capacityWorstCase

example : UniversalLaw.Spec.P15.HStarExceedsOne :=
  UniversalLaw.Proofs.P15Elementary.hStarExceedsOne

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.LocalPriceBoundFull F :=
  UniversalLaw.P15Closure.localPriceBoundFull F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.GlobalAssemblyHazard F :=
  UniversalLaw.P15Closure.globalAssemblyHazard F

example : UniversalLaw.Spec.P15.SharpnessOfRhoStar :=
  UniversalLaw.Proofs.P15Elementary.sharpnessOfRhoStar

example : UniversalLaw.Spec.P15.DemandOneBoundary :=
  UniversalLaw.Proofs.P15Elementary.demandOneBoundary

example : UniversalLaw.Spec.P15.SixSeventhsCertificate :=
  UniversalLaw.Proofs.P15Elementary.sixSeventhsCertificate

private def p15AuditNames : List Name := [
  `UniversalLaw.P15Closure.paletteNumberAttained,
  `UniversalLaw.P15Closure.localRestriction,
  `UniversalLaw.P15Closure.localPriceChain,
  `UniversalLaw.P15Closure.independentBlockHazard,
  `UniversalLaw.P15Closure.fullBlockCoverIff,
  `UniversalLaw.P15Closure.coverCostHazardBound,
  `UniversalLaw.P15Closure.restrictedLocalBudget,
  `UniversalLaw.P15Closure.restrictedTransformedPriceBudget,
  `UniversalLaw.P15Closure.rhoTestSufficient,
  `UniversalLaw.P15Closure.fullTransformedPriceBudget,
  `UniversalLaw.P15Closure.coordinatewiseConcavity,
  `UniversalLaw.P15Closure.hazardProductBound,
  `UniversalLaw.P15Closure.hazardPhiBound,
  `UniversalLaw.P15Closure.fullGroundPriceBound,
  `UniversalLaw.P15Closure.fullGroundBudgetIff,
  `UniversalLaw.P15Closure.localPriceBoundFull,
  `UniversalLaw.P15Closure.globalAssemblyHazard,
  `UniversalLaw.P15Closure.fullTransformedPriceBudget_sixSevenths,
  `UniversalLaw.Proofs.P15Elementary.twoCoordGeneratorPrices,
  `UniversalLaw.Proofs.P15Elementary.logOnePlusBelowIdentity,
  `UniversalLaw.Proofs.P15Elementary.demandOneRefutation,
  `UniversalLaw.Proofs.P15Elementary.logRatioBound,
  `UniversalLaw.Proofs.P15Elementary.capTestAtTwoThirds,
  `UniversalLaw.Proofs.P15Elementary.ratioExponentBound,
  `UniversalLaw.Proofs.P15Elementary.rhoStarBelowSixSevenths,
  `UniversalLaw.Proofs.P15Elementary.sixSeventhsCertificate,
  `UniversalLaw.Proofs.P15Elementary.hStarExceedsOne,
  `UniversalLaw.Proofs.P15Elementary.phiAtPStar,
  `UniversalLaw.Proofs.P15Elementary.hazardStarPositive,
  `UniversalLaw.Proofs.P15Elementary.oddMajorityIdentity,
  `UniversalLaw.Proofs.P15Elementary.capacityWorstCase,
  `UniversalLaw.Proofs.P15Elementary.demandOneBoundary,
  `UniversalLaw.Proofs.P15Elementary.triangleNeedsThree,
  `UniversalLaw.Proofs.P15Elementary.capacityHazardIsBinomial,
  `UniversalLaw.Proofs.P15Elementary.sharpnessOfRhoStar,
  `UniversalLaw.P15Completion.minimalForbiddenCharacterisation,
  `UniversalLaw.P15Completion.localDecomposability,
  `UniversalLaw.P15Completion.localObstructionIsFullBlock,
  `UniversalLaw.P15Completion.wholeGroundChromaticNumber,
  `UniversalLaw.P15Completion.elementaryPaletteFormula,
  `UniversalLaw.P15Completion.benchmark816IsRealized,
  `UniversalLaw.P15Completion.benchmark816Palette,
  `UniversalLaw.P15Completion.benchmark816Cover,
  `UniversalLaw.P15Completion.benchmark816WholeGround,
  `UniversalLaw.P15Completion.benchmark816MinimalForbiddenCounts,
  `UniversalLaw.P15Completion.benchmark816Price,
  `UniversalLaw.P15Completion.benchmark816UnionBound,
  `UniversalLaw.P15Completion.benchmark816TransformedRange,
  `UniversalLaw.P15Completion.benchmark816RationalPrice,
  `UniversalLaw.P15Completion.rhoStarEnclosure,
  `UniversalLaw.P15Completion.badWitness_union_bound,
  `UniversalLaw.P15Completion.exists_minimalForbidden_subset,
  `UniversalLaw.P15Completion.minimalForbidden_union_bound]

elab "#audit_p15_completion" : command => do
  liftCoreM do
    let env ← getEnv
    for name in p15AuditNames do
      let some (.thmInfo info) := env.find? name
        | throwError "Missing theorem: {name}"
      if info.type.hasFVar || info.type.hasMVar || info.type.hasLooseBVars ||
          info.value.hasFVar || info.value.hasMVar || info.value.hasLooseBVars then
        throwError "Open theorem expression: {name}"
      let inferred ← match Kernel.check env {} info.value with
        | .ok t => pure t
        | .error _ => throwError "Kernel recheck failed: {name}"
      match Kernel.isDefEq env {} inferred info.type with
      | .ok true => pure ()
      | _ => throwError "Inferred type mismatch: {name}"
      let declaration : Declaration := .thmDecl {
        name := Name.str `UniversalLaw.P15Completion.Rechecked name.toString
        levelParams := info.levelParams, type := info.type, value := info.value }
      match env.addDeclCore 0 0 declaration none true with
      | .ok _ => pure ()
      | .error _ => throwError "Checked declaration insertion failed: {name}"
      let axioms ← collectAxioms name
      if axioms.any (fun a => a != `propext && a != `Classical.choice && a != `Quot.sound) then
        throwError "Forbidden transitive axiom: {name}"
      let names := String.intercalate "," (axioms.toList.map Name.toString)
      liftM <| IO.println s!"P15_AUDIT|{name}|closed|kernel|declaration|{names}"
    liftM <| IO.println s!"P15_AUDIT_COMPLETE|{p15AuditNames.length}"

#check UniversalLaw.P15Closure.fullTransformedPriceBudget
#audit_p15_completion
