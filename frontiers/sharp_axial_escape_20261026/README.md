# Sharp axial escape: fewer assumptions for one lifetime moment

[Proof](PROOF.md) · [Source identities](SOURCES.json) · [Verification](VERIFICATION.md)

This additive author-side candidate establishes two bounded improvements:

- With the two exact value pins and zero derivative pins, `rH<24k` guarantees
  an axial path ending above the birth height with minimum at the lower pin.
  The old sufficient condition was `rH<=3k`. The constant 24 is sharp, and
  the strict inequality is essential.
- For a fixed lifetime power `q>0`, one uniform weighted C4-norm moment at
  an order `s>4q+3` suffices for the finite-death tail step. All-order moments
  are unnecessary for this step at a single q. An abstract counterexample
  shows why the equality case does not suffice from these bounds alone.

The deterministic result has no stochastic conjecture as a premise. Its
Gaussian application retains the actual source moment and marked-law inputs.
This does not make the parent theorem unconditional or supply independent
scientific review. No scientific status changes.

From the repository root, using only the Python standard library:

```sh
python -B -S frontiers/sharp_axial_escape_20261026/check_exact.py
python -B -S -O frontiers/sharp_axial_escape_20261026/check_exact.py
```

The outputs should be identical. Finite controls are supplemental exact
algebra checks; the continuum theorem is proved in the text.
