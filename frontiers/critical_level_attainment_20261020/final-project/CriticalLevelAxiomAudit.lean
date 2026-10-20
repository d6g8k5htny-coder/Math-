import CriticalLevelAttainment
import Lean.Elab.Command
import Lean.Util.CollectAxioms

/-! Complete module-origin census for C294 and all five immutable local inputs.
Includes generated and private declarations. Only the standard axioms are allowed.
Command success is scoped execution evidence, not scientific promotion. -/

#print axioms TorusCriticalAttainment.quotient_death_attainment
#print axioms TorusCriticalAttainment.euclidean_death_attainment
#check @TorusCriticalAttainment.quotient_death_attainment
#check @TorusCriticalAttainment.euclidean_death_attainment

open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let modules : Array Name := #[`Lifetime, `TorusTopology, `SuperlevelBar,
    `ClosedSuperlevel, `MorseFiniteCritical, `CriticalLevelAttainment]
  let constants := env.constants.toList
  let mut allNames : Array Name := #[]
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing audited module: {modName}"
    let names := (constants.filterMap fun (name, _) =>
      if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt
    if names.isEmpty then throwError "empty declaration inventory: {modName}"
    liftIO <| IO.eprintln s!"ATTAINMENT_AUDIT_PROGRESS {modName} COUNT {names.size}"
    logInfo m!"ATTAINMENT_AUDIT_MODULE {modName} COUNT {names.size}"
    for name in names do
      if (env.checked.get.find? name).isNone then
        throwError "missing kernel declaration: {name}"
      let axs ← Lean.collectAxioms name
      logInfo m!"ATTAINMENT_AUDIT_DECL {name} AXIOMS {axs}"
      for ax in axs do
        unless allowed.contains ax do
          throwError "forbidden transitive axiom {ax} in {name}"
      allNames := allNames.push name
  let required : Array Name := #[
    `UniversalLaw.Spec.Lifetime.IsSmooth,
    `UniversalLaw.Spec.Lifetime.IsMorseDistinct,
    `UniversalLaw.Spec.Lifetime.IsCriticalPoint,
    `TorusFiltration.torus_proj,
    `TorusFiltration.torus_compact,
    `TorusFiltration.torus_path_lift_from,
    `TorusFiltration.superlevelBar_deathHeight,
    `TorusFiltration.superlevelBar_strict_cut,
    `TorusFiltration.superlevelBar_death_not_mem_clearance,
    `TorusMorseFinite.quotientCriticalSet_finite,
    `TorusMorseFinite.mem_quotientCriticalSet_iff,
    `TorusCriticalAttainment.quotient_death_attainment,
    `TorusCriticalAttainment.euclidean_death_attainment]
  for name in required do
    unless allNames.contains name do
      throwError "required declaration omitted from audit: {name}"
  logInfo m!"ATTAINMENT_AUDIT_STANDARD_ONLY_PASS COUNT {allNames.size}"
