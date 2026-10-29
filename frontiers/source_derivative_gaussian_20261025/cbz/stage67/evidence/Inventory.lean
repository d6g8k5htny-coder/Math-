import SourceActualLowerSeparation
import Lean.Util.CollectAxioms

open Lean Elab Command

run_cmd do
  let env ← getEnv
  let some ownIndex := env.getModuleIdx? `SourceActualLowerSeparation
    | throwError "Expected actual imported production module index"
  let owned := (env.constants.toList.filter fun entry =>
    env.getModuleIdxFor? entry.1 == some ownIndex).mergeSort
      (fun left right => Name.quickLt left.1 right.1)
  if owned.isEmpty then
    throwError "Empty actual module-index ownership inventory"
  let standard3 := [`propext, `Classical.choice, `Quot.sound]
  let mut publicEndpointCount : Nat := 0
  for (name, info) in owned do
    let kind := match info with
      | .axiomInfo _ => "axiom"
      | .defnInfo _ => "definition"
      | .thmInfo _ => "theorem"
      | .opaqueInfo _ => "opaque"
      | .quotInfo _ => "quotient"
      | .inductInfo _ => "inductive"
      | .ctorInfo _ => "constructor"
      | .recInfo _ => "recursor"
    let category :=
      if name == `I4SourceActualLowerSeparation.actualSource_closedSuperlevel_componentInclusion_locally_injective then
        "sole-public-Prop"
      else if name.toString.startsWith "_private." then
        "private-or-private-generated"
      else
        "other-owned-needs-explicit-classification"
    if category == "sole-public-Prop" then
      publicEndpointCount := publicEndpointCount + 1
    let axioms ← collectAxioms name
    IO.println s!"OWNED|{name}|{kind}|{category}|{axioms.toList}"
    for axiomName in axioms do
      if !standard3.contains axiomName then
        throwError "Nonstandard axiom {axiomName} in owned declaration {name}"
  if publicEndpointCount != 1 then
    throwError "Expected exactly one public endpoint, found {publicEndpointCount}"
  IO.println s!"PASS_ALL_OWNED_STD3|module-index={ownIndex}|count={owned.length}|public-endpoints={publicEndpointCount}"
