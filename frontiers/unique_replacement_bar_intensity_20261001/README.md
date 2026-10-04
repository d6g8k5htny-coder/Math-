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
- [Historical-source regressions](test_sources.py): real temporary Git repositories test commit/path binding, missing history, replacement objects and Git environment isolation.

From the repository root, with Python3.11 and Git supporting
`--no-lazy-fetch` available:

```sh
python3.11 -B -S frontiers/unique_replacement_bar_intensity_20261001/check_exact.py
python3.11 -B -O -S frontiers/unique_replacement_bar_intensity_20261001/check_exact.py
python3.11 -B -S frontiers/unique_replacement_bar_intensity_20261001/test_sources.py
python3.11 -B -O -S frontiers/unique_replacement_bar_intensity_20261001/test_sources.py
```

The verifier requires the pinned commit
`044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43` and its source objects in this
repository. It checks that the object is a commit, each historical path is a
regular blob, and that its blob identity and bytes match the manifest and
working file. Replacement objects and inherited Git repository/configuration
environment overrides are disabled. Missing history fails closed; the checker
does not fetch. For a shallow checkout, explicitly fetch only the pinned commit
before running the checks:

```sh
git fetch --no-tags --depth=1 origin 044d42d5bd7f31df6f7e6b9034d6711e8fb7ee43
```

The packet workflow performs this bounded fetch only when needed; it does not
require full repository history. This source-binding repair changes neither
PROOF.md, ROOTS.md nor SOURCES.json, and does not re-vote their mathematical review.

Authors: OpenAI/Codex root and the named contributors in ROOTS.md, under Dylan Roy's delegation. Source-bound review is recorded in the associated PR. Scientific effect NONE; no imported theorem, independence requirement, formal alignment or controlling scientific status is promoted by these files or green checks.
