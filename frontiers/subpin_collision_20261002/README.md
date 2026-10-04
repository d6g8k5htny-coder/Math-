# Witness collisions below the pin scale

Pairs of additional critical points can occur with probability of order r^3
when their separation is comparable to the pin distance r. This conditional
corollary shows that pairs separated by o(r) carry only o(r^3) weighted mass.
On compact positive gap marks, their collision-marked lifetime density is
o(ell^(2/3)). The original determinant weight and full normalizer are retained.

Read [the proof and boundaries](PROOF.md), [the exact source map](SOURCES.json),
and [finite negative controls](controls.py). This is a new deduction from the
reviewed two-scale pair law, not a new Gaussian collision calculation or a
whole-project completion certificate. No convergence rate is claimed.

From the repository root, run:

```sh
python3 -B -S frontiers/subpin_collision_20261002/controls.py
python3 -B -O -S frontiers/subpin_collision_20261002/controls.py
```

The output should match [RESULTS.json](RESULTS.json). The script checks exact
algebra and logical counterexamples; the proof's analytic imports require their
own source-bound reviews. Hosted downstream/formal checks have a different scope.

Author-side OpenAI/Codex work, with root and named analytical subagents.
Dylan Roy delegated the work; personal reading remains PENDING.
Organizational independence 0; scientific effect NONE.

[Public mathematical reading map](../../PUBLIC_READING_MAP.md)
· [Two-scale configuration source](../two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md)
