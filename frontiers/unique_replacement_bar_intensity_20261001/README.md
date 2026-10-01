# Rare replacement bars, counted once

One maximum can have several nearby candidate saddles that are not its actual persistence partner. Pushing every rejected candidate onto that maximum's bar counts the same bar repeatedly. This packet weights each candidate by the reciprocal of its eligible multiplicity, so one bar contributes exactly one count.

For the stated planar Gaussian field on a fixed torus, fixed birth and positive-gap intervals, and a fixed shrinking distance band, the candidate theorem gives

```
expected number per unit area = C_U h^5 + o(h^5),
0 < C_R/2 <= C_U <= C_R < infinity.
```

Here C_R is the corresponding rejected-candidate coefficient; C_U is an explicitly identified Gaussian/angular integral with the reciprocal multiplicity inside it. This is a rare selected population of **actual finite ordinary superlevel H0 bars**, conditional on the exact imported analytic interfaces. It is not the ordinary short-bar leading law, a new all-mark theorem, or a statement about fields conditioned on containing a bar.

- [Proof and exact population](PROOF.md): counting identity, measurable mark, weighted limit, normalization and scope.
- [Root and cutoff analysis](ROOTS.md): all saddles, including below the original window; null boundaries and exact counterexamples to wrong counts.
- [Source identities](SOURCES.json): seven exact imported sources, with hypotheses retained.
- [Exact controls](check_exact.py): rational algebra, source integrity and deliberately wrong alternatives; these checks do not prove the continuum limit.

From the repository root, with Python3.11:

```sh
python3.11 -B -S frontiers/unique_replacement_bar_intensity_20261001/check_exact.py
python3.11 -B -O -S frontiers/unique_replacement_bar_intensity_20261001/check_exact.py
```

Authors: OpenAI/Codex root and the named contributors in ROOTS.md, under Dylan Roy's delegation. Source-bound review is recorded in the associated PR. Scientific effect NONE; no imported theorem, independence requirement, formal alignment or controlling scientific status is promoted by these files or green checks.
