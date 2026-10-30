import CriticalRidge
import Lean.Elab.Command
import Lean.Util.CollectAxioms

/-! Complete module-origin census for C299 and its exact C293 inputs.
Includes generated and private declarations. Only the standard axioms are allowed.
Command success is scoped execution evidence, not scientific promotion. -/

#print axioms TorusCriticalRidge.exists_negative_partial_gradient_ridge
#print axioms TorusCriticalRidge.negativeHessianBlock_isInvertible
#print axioms TorusCriticalRidge.negativePartialGradient_hasFDerivAt
#check @TorusCriticalRidge.exists_negative_partial_gradient_ridge

open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  let modules : Array Name := #[`Lifetime, `TorusTopology,
    `MorseFiniteCritical, `CriticalRidge]
  let constants := env.constants.toList
  let mut allNames : Array Name := #[]
  for modName in modules do
    let some idx := env.getModuleIdx? modName
      | throwError "missing audited module: {modName}"
    let names := (constants.filterMap fun (name, _) =>
      if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt
    if names.isEmpty then throwError "empty declaration inventory: {modName}"
    liftIO <| IO.eprintln s!"CRITICAL_RIDGE_AUDIT_PROGRESS {modName} COUNT {names.size}"
    logInfo m!"CRITICAL_RIDGE_AUDIT_MODULE {modName} COUNT {names.size}"
    for name in names do
      if (env.checked.get.find? name).isNone then
        throwError "missing kernel declaration: {name}"
      let axs ← Lean.collectAxioms name
      logInfo m!"CRITICAL_RIDGE_AUDIT_DECL {name} AXIOMS {axs}"
      for ax in axs do
        unless allowed.contains ax do
          throwError "forbidden transitive axiom {ax} in {name}"
      allNames := allNames.push name
  let required : Array Name := #[
    `UniversalLaw.Spec.Lifetime.IsSmooth,
    `UniversalLaw.Spec.Lifetime.IsCriticalPoint,
    `UniversalLaw.Spec.Lifetime.hessian,
    `TorusMorseFinite.literal_hessian_eq_fderiv,
    `TorusCriticalRidge.restrictCovector,
    `TorusCriticalRidge.ridgeAddition,
    `TorusCriticalRidge.negativePartialGradient,
    `TorusCriticalRidge.negativeHessianBlock,
    `TorusCriticalRidge.negativeHessianBlock_apply,
    `TorusCriticalRidge.negativeHessianBlock_isInvertible,
    `TorusCriticalRidge.negativePartialGradient_contDiff,
    `TorusCriticalRidge.negativePartialGradient_hasFDerivAt,
    `TorusCriticalRidge.exists_negative_partial_gradient_ridge]
  for name in required do
    unless allNames.contains name do
      throwError "required declaration omitted from audit: {name}"
  logInfo m!"CRITICAL_RIDGE_AUDIT_STANDARD_ONLY_PASS COUNT {allNames.size}"
