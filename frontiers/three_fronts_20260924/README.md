# Three mathematical fronts — 24 September 2026

This directory contains new author-side research, not another routing database.
Main campaign61 is the collaboration entry. Parent lifetime/coefficient discussions
are main63/main65; the P15 source interface is P15-B and main59. Nonauthor review
remains open. The published parent objects and coefficient_v1 are unchanged.

| Proof | New result | Boundary |
|---|---|---|
| [LIFETIME_REMAINDER.md](LIFETIME_REMAINDER.md) | Candidate and finite-bar densities equal c*ell^(-1/3)+O(1); nonselected density O(1), for all marks and separations on each fixed torus | Uses parent's exact marked Kac-Rice and deterministic cap interfaces; no numerical remainder constant or convergence radius |
| [RN_COUNT_INTERFACE.md](RN_COUNT_INTERFACE.md) | Sharp probability-to-count estimates/counterexamples and exact pinned triple-determinant Kac-Rice interface | Does not evaluate the RN integral or discharge the original RN/24-jet certificates |
| [P15_REALIZED_COVERS.md](P15_REALIZED_COVERS.md) | Complete original-coordinate family with actual restrictions, nonempty covers and exact palette optimum for that cover | Prices c<=p; explicit family, not arbitrary downsets or full transformed-price range |

`frontier_math.py` implements exact finite controls and prints `RESULTS.json`.
`test_frontiers.py` contains54 distinct tests. Matrix determinants and inertia use
rational arithmetic. The P15 tests enumerate real small original-coordinate sets,
not only abstract palettes. The large816 construction uses proved counting
formulas, not enumeration of its419743994415 crossing witnesses.

```sh
python -B -S -m unittest -v test_frontiers
python -B -O -S -m unittest -v test_frontiers
python -B -S frontier_math.py
python -B -S run_validation.py --output /absolute/new/directory/outside/this/directory
```

The last command retains normal/optimized logs and ten deliberately incorrect
program variants, all checked for actual assertion failures. Results are finite
implementation/algebra evidence, not verification of continuum Gaussian estimates.
Use the accompanying actual run report rather than treating this README as an
execution receipt. No third-party dependency is required.

`SOURCES.json` identifies the exact consumed project objects. The external
reconnaissance note separates primary-source background from new arguments.
Existing source bytes, failed evidence, other agents' branches, private sandbox
contents and scientific acceptance flags are not altered by this package.
