# When one very short bar occurs

For the fixed planar periodized Gaussian field, the candidate theorem shows that a field containing a sufficiently short ordinary finite superlevel H0 bar asymptotically contains only one such bar. Its occurrence probability has the same leading coefficient as its expected count.

[Theorem and proof](PROOF.md) · [New fold isolation lemma](FOLD_ISOLATION.md) · [Exact sources](SOURCES.json)

The new step controls the expected count on fields containing multiple short bars. It also removes the bias introduced by sampling bars across fields: conditioning a field on occurrence and choosing its bar uniformly has the same limiting mark law as the intensity calculation.

This is a conditional mathematical candidate. It retains the imported global elder-pairing, Kac–Rice and Gaussian bounds. It supplies no factorial-moment or Poisson theorem, quantitative convergence rate, increasing-volume limit, higher-dimensional extension or whole-program closure. Scientific-status effect NONE; C8 remains OPEN.

Run the exact finite controls from the repository root:

```sh
python3 -B -S frontiers/ordinary_short_bar_occurrence_20261001/test_check.py -v
python3 -B -O -S frontiers/ordinary_short_bar_occurrence_20261001/test_check.py -v
python3 -B -S frontiers/ordinary_short_bar_occurrence_20261001/test_check.py --mutants
```

These standard-library controls verify source identities, rational counting and sampling identities, cubic-scale Jacobians, and counterexamples to invalid inferences. Implementation mutations must be rejected in both modes. They do not prove the continuum analysis. Fresh mathematical review and engineering review are recorded separately on the source-bound pull request.

Actual authoring: OpenAI/Codex root and named coauthors in the delivery. Dylan Roy — delegated AI work; personal reading PENDING. Same-provider technical review carries zero organizational-independence credit.
