import OwnedKernelAudit.Support
open Lean
theorem OwnedKernelControl.Self : True := True.intro
#eval show CoreM Unit from do
  let pairs : List (Name × Name) := [(`OwnedKernelControl.Self, `OwnedKernelControl.Self)]

  let names := pairs.map Prod.fst
  for (name, target) in pairs do
    let ci : ConstantInfo := .thmInfo {
      name := name, levelParams := [],
      type := mkConst ``True, value := mkConst target}
    OwnedKernelAudit.checkedBody (← getEnv) ci
    let mut dependencies : NameSet := {}
    for expr in OwnedKernelAudit.expressions ci do
      for dep in expr.getUsedConstants do
        if names.contains dep then dependencies := dependencies.insert dep
    let encoded := (dependencies.toArray.map OwnedKernelAudit.enc).qsort (· < ·)
    IO.println s!"OWN_GRAPH_NODE|{OwnedKernelAudit.enc name}|{String.intercalate "," encoded.toList}"
  IO.println s!"OWN_GRAPH_COMPLETE|{pairs.length}"
