import Lake
open Lake DSL

-- Core-only package: no external dependency. Every theorem here is checked by
-- the Lean 4 kernel with `decide` / `decide +kernel` on exact Nat/Int/Rat data.
-- Scientific effect: NONE. Kernel acceptance verifies the encoded statement at
-- its trust boundary; translation fidelity is a separate alignment review lane.
-- Written as `lakefile.lean` (not TOML) because lean-action's nanoda step reads
-- the module name from a `package <Name>` declaration.

package MathFormalCore

@[default_target]
lean_lib MathFormalCore
