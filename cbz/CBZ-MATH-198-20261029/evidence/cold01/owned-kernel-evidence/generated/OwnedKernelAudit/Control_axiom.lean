import OwnedKernelAudit.Support
open Lean

axiom OwnedKernelControl.Bad : False
#eval show CoreM Unit from do
  let ci : ConstantInfo := .thmInfo {
    name := `OwnedKernelControl.Fabricated,
    levelParams := [], type := mkConst ``False, value := mkConst ``OwnedKernelControl.Bad}
  let (_, closure) ← (OwnedKernelAudit.collectEntry (← getEnv) ci).run {}
  OwnedKernelAudit.permitted closure
  IO.println "OWN_CONTROL_ESCAPED|axiom"
