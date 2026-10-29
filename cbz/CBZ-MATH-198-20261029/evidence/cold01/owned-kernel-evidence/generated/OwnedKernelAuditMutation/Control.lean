import OwnedKernelAuditMutation.Support
open Lean

#eval show CoreM Unit from do
  let u := Level.param `unlistedUniverse
  let type := Expr.forallE `α (.sort u) (.forallE `x (.bvar 0) (.bvar 1) .default) .default
  let value := Expr.lam `α (.sort u) (.lam `x (.bvar 0) (.bvar 0) .default) .default
  let ci : ConstantInfo := .defnInfo {
    name := `OwnedKernelControl.BadUniverse,
    levelParams := [], type := type, value := value, hints := .opaque, safety := .safe}
  OwnedKernelAuditMutation.checkedBody (← getEnv) ci
  IO.println "OWN_CONTROL_ESCAPED|universe"
