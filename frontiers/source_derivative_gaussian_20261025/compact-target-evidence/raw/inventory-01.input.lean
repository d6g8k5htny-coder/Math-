import SourceCompactTargetMoments
import Lean.Util.CollectAxioms

open Lean in
run_cmd do
  let env ← getEnv
  let names := env.constants.toList.filterMap fun (name, ci) =>
    if name.toString.startsWith "I4SourceCompactTargetMoments." then some (name, ci) else none
  for (name, ci) in names.toArray.qsort (fun x y => x.1.toString < y.1.toString) do
    let kind := match ci with
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | .axiomInfo _ => "axiom"
      | .opaqueInfo _ => "opaque"
      | _ => "other"
    logInfo m!"INVENTORY|{kind}|{name}"
    let axioms ← collectAxioms name
    logInfo m!"AXIOMS|{name}|{axioms}"
