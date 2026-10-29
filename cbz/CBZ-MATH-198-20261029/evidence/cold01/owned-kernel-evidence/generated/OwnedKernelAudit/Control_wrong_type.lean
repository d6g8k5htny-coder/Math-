import OwnedKernelAudit.Support
open Lean
#eval show CoreM Unit from do
  let ci : ConstantInfo := .thmInfo {
    name := `OwnedKernelControl.Fabricated,
    levelParams := [], type := mkConst ``False, value := mkConst ``True.intro}
  OwnedKernelAudit.checkedBody (← getEnv) ci
  IO.println "OWN_CONTROL_ESCAPED|wrong_type"
