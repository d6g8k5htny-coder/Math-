import MathFormalReal
import Lean

/-!
Axiom audit for `MathFormalReal`.

Prints one line per theorem declared in the library, in sorted order, with the
sorted list of axioms its proof depends on. `formalization/formal_gate.py` compares the
output with `formalization/lean/mathlib/AXIOMS.expected` byte for byte and refuses any line
containing `sorryAx` or `Lean.ofReduceBool` (the `native_decide` axiom).

Run from `formalization/lean/mathlib`: `lake env lean scripts/Axioms.lean`
-/

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut rows : Array (String × Array String) := #[]
  for (name, info) in env.constants.map₁.toList do
    unless (`MathFormalReal).isPrefixOf name do continue
    if name.isInternal then continue
    -- Auto-generated equation lemmas (`foo.eq_1`) are elaboration artifacts, not audited statements.
    if (toString name.componentsRev.head!).startsWith "eq_" then continue
    match info with
    | .thmInfo _ =>
      let used ← collectAxioms name
      let axioms := (used.map toString).qsort (· < ·)
      rows := rows.push (toString name, axioms)
    | _ => pure ()
  let sorted := rows.qsort (fun x y => x.1 < y.1)
  for (name, axioms) in sorted do
    let joined := if axioms.isEmpty then "-" else String.intercalate "," axioms.toList
    logInfo m!"{name} {joined}"
