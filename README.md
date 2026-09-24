# Mathematics — proofs, calculations, and open reviews

[Research home](https://github.com/d6g8k5htny-coder/main) · [Topic guide](https://github.com/d6g8k5htny-coder/main/blob/main/docs/RESEARCH_INDEX.md) · [Run the checks](https://github.com/d6g8k5htny-coder/main/blob/main/docs/REPRODUCE.md) · [Work queue](https://github.com/d6g8k5htny-coder/main/issues/61)

## Read a result

| Topic | Proof or entry point | Review and scope |
|---|---|---|
| Gaussian lifetime coefficient | [SIDE24 dimensions 2 and 3](coefficients/side24_v1/PROOF.md) | [main #65](https://github.com/d6g8k5htny-coder/main/issues/65); conditional on the parent lifetime formula |
| Quantitative lifetime density | [Bounded unrestricted remainder](frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md) | [main #67](https://github.com/d6g8k5htny-coder/main/issues/67); parent interfaces remain under review |
| RN critical-point counting | [Probability-to-count interface](frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md) | Exact implications and counterexamples; the Gaussian triple integral is not evaluated |
| P15 obstruction covers | [Original-coordinate realization](frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md) | Specified family and cover; 816 versus whole-ground 818 |
| P15 failed extension | [Price-range counterexample](frontiers/three_fronts_20260924/P15_PRICE_BOUNDARY.md) | Unrestricted same-palette transformed-price extension is false |
| P15 valid price extension | [Low-probability transformed-price budget](frontiers/price_budget_20260924/PROOF.md) | New sufficient hypotheses: demand at least 2 and probabilities at most 1/4 |

All positive research claims here are author-side candidates pending nonauthor review. A merge publishes a source; a test checks its stated coverage. Neither independently accepts a theorem. The counterexample and the restricted successor concern different hypotheses.

## Run a calculation

All commands below use the Python standard library and run from this repository root.

```sh
python -B -S coefficients/side24_v1/coefficient.py
python -B -S -m unittest discover -s coefficients/side24_v1 -p 'test_*.py' -v
python -B -S -m unittest discover -s frontiers/three_fronts_20260924 -p 'test_*.py' -v
python -B -S frontiers/price_budget_20260924/price_budget.py
python -B -S -m unittest discover -s frontiers/price_budget_20260924 -p 'test_*.py' -v
```

[Full reproduction guide](https://github.com/d6g8k5htny-coder/main/blob/main/docs/REPRODUCE.md) explains normal/optimized runs, mutation controls, and pinned versus current-source replay. [Frontier directory](frontiers/README.md) groups the packages. Older dated source files are retained unchanged; use the review links for subsequent corrections.

## Where the other work lives

[main](https://github.com/d6g8k5htny-coder/main) holds the campaign, reviews and legacy research-branch links. [meta-framework](https://github.com/d6g8k5htny-coder/meta-framework) holds exact source identities; [query-](https://github.com/d6g8k5htny-coder/query-) looks them up; [trial](https://github.com/d6g8k5htny-coder/trial) checks integration; [google-drive](https://github.com/d6g8k5htny-coder/google-drive) carries selected public replicas. Private experiments are not exported through those public routes.
