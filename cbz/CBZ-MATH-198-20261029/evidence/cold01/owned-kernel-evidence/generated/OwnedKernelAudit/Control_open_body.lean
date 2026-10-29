import OwnedKernelAudit.Support
open Lean
#eval show CoreM Unit from do
  let ci : ConstantInfo := .thmInfo {
    name := `OwnedKernelControl.Fabricated,
    levelParams := [], type := mkConst ``False, value := Expr.bvar 0}
  OwnedKernelAudit.checkedBody (← getEnv) ci
  IO.println "OWN_CONTROL_ESCAPED|open_body"
