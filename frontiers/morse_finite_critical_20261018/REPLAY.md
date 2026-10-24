# Replaying the finite-class unit

Use Lean 4.34.1 and a Mathlib project pinned to
`d13f23b723b8a846827a245b89c10fc7d3f11612`. The complete native dependency
manifest and artifact census are retained in the private immutable handoff.
Our run reused 83,897 prior byte hashes through unchanged size/mtime/inode and
an exact path-set check; it did not freshly rehash every dependency byte.

Use an empty output directory, place it first in `LEAN_PATH`, followed by the
compiled import roots of the pinned Mathlib project. Compile in this order:
`Lifetime`, `TorusTopology`, `MorseFiniteCritical`, `MorseFiniteControls`,
`MorseFiniteAxiomAudit`. For each module use the source in `final-project/` and
an output `.olean` in the empty output directory. Actual command shape:

```sh
lean -j2 -M4096 -DwarningAsError=true -o "$OUT/MorseFiniteCritical.olean" final-project/MorseFiniteCritical.lean
leanchecker -v MorseFiniteCritical
leanchecker -v MorseFiniteControls
leanchecker -v MorseFiniteAxiomAudit
lean -j2 -M4096 negative-project/WithoutMorse.lean
```

Warnings-as-errors applied to all three new modules; the unchanged two inputs
also built with empty stdout/stderr. Audit output must include all 169 unique
module-origin declarations and the terminal standard-only count. The last
command must reject the omitted Morse premise with a type mismatch, not an
import, syntax, timeout or tool failure. Inspect the full raw output and source
identities, not just an exit status.

The included run scripts are path-projected records of the actual local
orchestrator, not a portable one-command installer. Symbolic `$C293_ROOT`,
`$LEAN_RUNTIME`, `$PINNED_PROJECT`, `$WORK_ROOT` identify replaced local prefixes.
No hosted workflow or registered target is added by this evidence package.
