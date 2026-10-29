import Closure.Assembly

open Lean Elab Command

-- These adapters force the headline and supporting endpoints to have the
-- original registered proposition types, without extra bridge assumptions.
example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.FullTransformedPriceBudget F :=
  UniversalLaw.P15Closure.fullTransformedPriceBudget F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.RestrictedTransformedPriceBudget F :=
  UniversalLaw.P15Closure.restrictedTransformedPriceBudget F

example {X : Type} [Fintype X] [DecidableEq X]
    (F : UniversalLaw.Spec.P15.RealizedData X) :
    UniversalLaw.Spec.P15.RhoTestSufficient F :=
  UniversalLaw.P15Closure.rhoTestSufficient F

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
  `UniversalLaw.Proofs.P15Elementary.sharpnessOfRhoStar]

elab "#audit_p15_closure" : command => do
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
        name := Name.str `UniversalLaw.P15Closure.Rechecked name.toString
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
#audit_p15_closure
