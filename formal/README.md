# Formal verification lane

**Source-bound Lean evidence; no scientific promotion.** This is an additive implementation of main issue 95's existing L5 lane, not a replacement for custody, analytic review or the scientific-status authority.

## Run

```sh
python -m unittest discover -s formal/tests -v
python -O -m unittest discover -s formal/tests -v
python formal/gate.py
cd formal
lake exe cache get
cd ..
python formal/gate.py --execute
```

The source-only command does not run Lean. The execute command fails unless the pinned project builds, `leanchecker` rechecks the package, all 13 declarations have transitive axiom reports restricted to propext/Classical.choice/Quot.sound, and five executable negative controls are rejected. It writes logs and a receipt in `.lake/formal-evidence/`; the workflow uploads them even on failure. A receipt from arbitrary input is not trusted evidence: use the successful read-only workflow and checked Git commit.

Sources: [scope](SCOPE.md), [glossary](GLOSSARY.md), [manifest](manifest.json), [blueprint source](blueprint/src/content.tex). The original GP-FOR-192 bytes are preserved under originals/*.lean.txt; separately named V2 companions carry the documented compiler-only repairs in [COMPATIBILITY.md](COMPATIBILITY.md). No historical Status.lean or claimed status is imported. [Alignment contract](SCOPE.md#review-contract) remains distinct from kernel evidence.

## Formal progress versus scientific status

`none`: no formal source; `specified`: statement only; `proved`: proof text supplied but no successful trusted run yet; `kernel-checked`: successful exact-commit build, recheck, axiom audit and negative controls. Alignment is separately pending/accepted/stale. The pilot's manifest records `proved` as source progress; the actual run receipt reports kernel evidence. No workflow edits a scientific register or retroactively changes old ACCEPT/AMEND dispositions. This workflow is not claimed to be a globally required branch-protection check.

## Next agents

Read main #95 and the exact PR head first. A non-OpenAI alignment reviewer should inspect all assumptions, the source correspondence and the explicit nonclaims. An independent engineering reviewer should attack omitted targets, imports carrying custom axioms, stale scope/hash/review records and altered toolchains. A probability formalizer should next establish an actual measure-theoretic Cauchy–Schwarz interface and its lower-normalizer dependency, without importing GP214's upper bound as the lower bound. Coordinate before editing; a review request is not a claim that a reviewer is active.

Blueprint declaration links are checked against the target inventory and compiled declarations, not by semantic equivalence. The full plasTeX/LaTeX website is not installed in this pilot. Optional independent checkers or AI proof generators may be added with pinned versions/budgets; their availability and execution must be separately recorded. Never treat AlphaProof as an assumed publicly callable CI service or a generator's success as an independent alignment review.
