import SourceFiniteTrig
import Lean.Util.CollectAxioms
open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mod := `SourceFiniteTrig
  let some idx := env.getModuleIdx? mod | throwError "Missing target module"
  let names := ((env.constants.toList.filter fun (n, _) =>
    env.getModuleIdxFor? n == some idx).map Prod.fst).toArray.qsort Name.quickLt
  for n in names do
    let some ci := env.find? n | throwError "Missing constant {n}"
    let kind := match ci with
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | .axiomInfo _ => "axiom"
      | .opaqueInfo _ => "opaque"
      | .inductInfo _ => "inductive"
      | .ctorInfo _ => "constructor"
      | .recInfo _ => "recursor"
      | .quotInfo _ => "quotient"
    logInfo m!"INVENTORY|{kind}|{n}"
    let axs ← collectAxioms n
    for ax in axs do
      unless #[`propext, `Classical.choice, `Quot.sound].contains ax do
        throwError "Forbidden axiom {ax} in {n}"
    logInfo m!"AXIOMS|{n}|{axs}"
  logInfo m!"COMPLETE_NEW_MODULE_INVENTORY|{mod}|{names.size}"
