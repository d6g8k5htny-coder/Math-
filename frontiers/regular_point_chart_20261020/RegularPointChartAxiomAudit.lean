import RegularPointChart
import Lean.Elab.Command
import Lean.Util.CollectAxioms

/-! Enforce the standard-axiom policy over the complete module-origin census.
The required inventory prevents omission of any of the seven original targets.
This is an engineering audit, not independent alignment or scientific acceptance. -/

open Lean Elab Command in
run_cmd do
  let env := (← getEnv).setExporting false
  let allowed : List Name := [`propext, `Classical.choice, `Quot.sound]
  let some idx := env.getModuleIdx? `RegularPointChart
    | throwError "C296_AXIOM_MISSING_MODULE RegularPointChart"
  let constants := env.constants.toList
  let names := (constants.filterMap fun (name, _) =>
    if env.getModuleIdxFor? name == some idx then some name else none).toArray.qsort Name.lt
  let audited := names
  if audited.isEmpty then throwError "C296_AXIOM_EMPTY RegularPointChart"
  let required : Array Name := #[
    `UniversalLaw.Spec.Lifetime.regularPointDerivative_range_eq_top,
    `UniversalLaw.Spec.Lifetime.regularPointHasStrictFDerivAt,
    `UniversalLaw.Spec.Lifetime.regularPointChart,
    `UniversalLaw.Spec.Lifetime.regularPointChart_fst,
    `UniversalLaw.Spec.Lifetime.regularPointChart_self,
    `UniversalLaw.Spec.Lifetime.mem_regularPointChart_source,
    `UniversalLaw.Spec.Lifetime.mem_regularPointChart_target]
  for name in required do
    unless audited.contains name do
      throwError "C296_AXIOM_MISSING_TARGET {name}"
  for name in audited do
    if (env.checked.get.find? name).isNone then
      throwError "C296_AXIOM_MISSING_KERNEL_DECL {name}"
    let axs ← Lean.collectAxioms name
    let axiomText := String.intercalate ", " (axs.toList.map fun ax => ax.toString)
    logInfo m!"C296_AXIOM_DECL {name.toString} AXIOMS [{axiomText}]"
    for ax in axs do
      unless allowed.contains ax do
        throwError "C296_AXIOM_FORBIDDEN {ax} in {name}"
  logInfo m!"C296_AXIOM_POLICY_PASS COUNT {audited.size}"
