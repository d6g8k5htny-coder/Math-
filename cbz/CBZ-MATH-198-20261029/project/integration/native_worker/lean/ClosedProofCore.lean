import Lean
open Lean
namespace ClosedProof

/-- Closed, exact-target acceptance against the supplied immutable baseline. -/
def closedGate (baseline : Environment) (target proof : Expr) : CoreM (Except String (Array Name)) := do
  if target.hasFVar || target.hasMVar || target.hasLooseBVars || proof.hasFVar || proof.hasMVar || proof.hasLooseBVars then
    return .error "expression is not closed"
  let inferred ← match Kernel.check baseline {} proof with
    | .ok x => pure x
    | .error _ => return .error "kernel check failed"
  match Kernel.isDefEq baseline {} inferred target with
  | .ok true => pure ()
  | _ => return .error "target mismatch"
  let decl : Declaration := .thmDecl { name := `ClosedProof.checkedCandidate, levelParams := [], type := target, value := proof }
  let env ← match baseline.addDeclCore 0 0 decl none true with
    | .ok x => pure x
    | .error _ => return .error "declaration check failed"
  let axioms ← withEnv env <| collectAxioms `ClosedProof.checkedCandidate
  if axioms.any (fun a => a != `propext && a != `Classical.choice && a != `Quot.sound) then
    return .error "forbidden axiom"
  return .ok axioms
end ClosedProof
