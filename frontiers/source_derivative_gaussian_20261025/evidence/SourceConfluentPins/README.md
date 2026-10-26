# New-module qualification only

The completed SourceConfluentPins compilation was reused. This run covers the
previously uncovered named kernel replay, eight public target axiom audit and
new meaningful controls. Existing inputs and previously qualified modules were
not separately rechecked.

`qualification_receipt.json` records exact subprocess commands, working
directories, exit codes, raw-log paths and digests, and the unchanged source
SHA256. Every subprocess's untouched combined stdout/stderr is retained in
its `.log`; metadata is retained in its `.json`.

Results:

- `lake env leanchecker SourceConfluentPins`: exit 0, empty raw output.
- Eight public-target transitive axiom reports: only `propext`,
  `Classical.choice`, `Quot.sound`.
- Positive controls: exit 0. Height seven/radius two gives the literal target
  `(19/3,0,0,0,0,2)`; radius minus two gives `(23/3,0,0,0,0,2)`.
  Zero-radius controls prove the noninverse collapse to `(1,1,0,0,0,0)` and
  zero cubic coordinate.
- The false zero-radius inverse and false cubic-coordinate-two controls each
  exit 1 at an unsolved `False` proof goal, with no import or syntax failure.

Source SHA256 throughout:
`41e1ea1ef4f9960307552a8271a5c04d2b72d94736b98eb601b51669ed603c3f`.

A preliminary CLI discovery call `lake env leanchecker --help` returned exit 1
with `uncaught exception: Could not find any oleans for: Source_smooth_realization`.
That output is reconstructed here from the actual tool response; it was not
redirected. It did not replay any old module. The actual requested named
`SourceConfluentPins` replay was then run exactly once, with its raw log retained.

Actual author-side lineage is OpenAI/Codex `/root/dm2_landed_composition`.
No helper was created. Qualification is local mathematical evidence, separate
from independent scientific review. Actual-source covariance limits,
conditioning/regression joins and overall campaign completion remain open.

Per `/workspace/AGENTS.md`, reuse these completed applicable checks; a later
handoff or process obligation does not invalidate the mathematics checked here.
