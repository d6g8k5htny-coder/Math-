# Final frozen quartic controls

`quartic_control_receipt.json` records exact commands, working directory,
exit codes, timestamps, raw logs, and before/after source, `.olean` and control
hashes. All completed runs used the parent's final frozen source
`8e23717ef98518b6d701db921d1f17958c3dee2c893745cafa7aa6172f1621d9`
and `.olean`
`d4cff4ad4c99947b084df20691dfc1228e9f46710faf52d9f28f7e3d57a97f72`.

The corrected positive control file passed with exit 0 and empty raw output.
It covers the exact mixed LM001 polynomial/Jacobian, both polynomial pins,
sharp Taylor factorials and a signed argument, distinct Pi/Euclidean norms,
the attained matrix operator factor two, maximum C1 constants, and the
literal cutoff/width conventions at nonunit radii.

The sum-C1 and missing-fifth-derivative controls each ran once, exiting 1 only
at the intended unsolved `False` goal. They were not rerun. The initial
positive attempt is retained; its only defects were normalization and an
API invocation in the optional all-ones operator equality. No production
change was needed.

No actual periodic-field assumptions were fabricated: the polynomial and
scalar Taylor controls are deterministic; cutoff controls instantiate proved
generic arithmetic with their displayed hypotheses. No capture or chart
transport is claimed.

Actual author-side helper lineage is OpenAI/Codex
`/root/dm2_landed_composition/peano_strategy`. Scientific review credit is zero.
The parent owns the distinct final module kernel replay and public axiom audit.
Reuse these completed applicable controls under `/workspace/AGENTS.md`.
