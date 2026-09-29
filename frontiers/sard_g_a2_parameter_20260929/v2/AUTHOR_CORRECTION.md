# Author correction to Math-#137 v1

The original PROOF.md at e944ba0b595d790d27d1466cc4f576467890bc3a is NOT an accepted
proof of A2.2 or Section 3. Its claim that a moving Hessian/eigenframe and a
recentered C1 graph transform are C1 in a C2 field parameter is invalid without
additional arguments/regularity. Claude's #138 correctly identified this issue.
The preceding assistant explanation repeated that unsupported claim; it is
withdrawn here, not merely relabelled as needing a routine check.

The explicit C2 gradient counterexample (F1)-(F3) in A2_FIXED_FRAME.md disproves
the C1-into-C1 strengthening. The tracked-saddle and finite-flow formulas remain
valid. The old four finite illustrations never verified the invalid analytic step.

This additive v2 preserves all original files in Git history and as predecessor
files in the branch. Its claims are different and narrower: joint C1 evaluation,
not C1 dependence into C1 arcs; continuous C1 arc dependence is proved separately.
The actual fixed-point map on bounded C0 trajectories is displayed and its
Nemytskii differentiability justified. Only a decay comparison uses weighted
spaces; no weighted differentiability is assumed.

The extension to A3/A4 and genericity is new author-side work. It must receive
its own source-bound analytic review; the merged R3/R4 review cannot discharge
its newly supplied premises retroactively. No original proof or review verdict,
scientific register, lemma flag, prize, RN/JETMOD or C103 status is altered here.
