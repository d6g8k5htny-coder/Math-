import Lean
open Lean

/- Load the compiled worker and its trusted task environment once. The bootstrap
   frontend imports Lean only, avoiding a second simultaneous Mathlib frontend. -/
unsafe def main (args : List String) : IO UInt32 := do
  if args.isEmpty then throw <| IO.userError "missing session"
  enableInitializersExecution
  let env ← importModules (loadExts := true) #[{ module := `ClosedProofWorker }] {}
  let run ← IO.ofExcept <| env.evalConst (Environment → List String → IO UInt32)
    {} `ClosedProof.Worker.runWithEnvironment (checkMeta := false)
  run env args
