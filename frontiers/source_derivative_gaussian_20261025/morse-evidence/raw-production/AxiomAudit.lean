import SourceMorseIncidence
import Lean.Util.CollectAxioms

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let some idx := env.getModuleIdx? `SourceMorseIncidence
    | throwError "SourceMorseIncidence module is not imported"
  let names := (env.constants.toList.filter fun (n, _) => env.getModuleIdxFor? n == some idx).map Prod.fst
  let names := names.toArray.qsort Name.quickLt
  let allowed : Array Name := #[`propext, `Classical.choice, `Quot.sound]
  for n in names do
    let axs ← collectAxioms n
    for ax in axs do
      unless allowed.contains ax do
        throwError "Forbidden axiom {ax} in {n}"
    logInfo m!"AXIOMS {n}: {axs}"
  logInfo m!"COMPLETE_MODULE_AXIOM_AUDIT declarations={names.size}; allowed={allowed}"

#print I4ActualSourceMorse.smoothLaw_ae_sourceMorseCube
#print I4ActualSourceMorse.smoothLaw_ae_sourceMorse
#print I4ActualSourceMorse.smoothLaw_ae_finite_sourceCriticalCube
