# Source-derived Gaussian lifetime tails

[Full proof](PROOF.md) · [Exact sources](SOURCES.json) · [Verification](VERIFICATION.md)

For the specified periodized Gaussian field in every fixed `d>=2`, on fixed
compact birth/gap ranges with the gap bounded away from zero, this candidate
derives the actual determinant-weighted estimate

    E exp(lambda (1+||f||_C4)^2) <= C.

It reconstructs the positive full-normalizer floor rather than assuming one.
Together with the [sharp axial lemma](../sharp_axial_escape_20261026/PROOF.md),
this gives `C exp(-c/r^2)` upper bounds for the essential event and, for each
fixed `q>0`, the normalized finite-lifetime q-moment above the prescribed gap.
No failure-mark convergence or selection-probability estimate is needed for
these upper bounds. Constants are not numerically evaluated.

This is an additive author-side proof. It reuses existing Gaussian-majorant
ideas and preserves posterior drift, correlations, the typed weight and the
full normalizer. Different-family scientific review remains pending. It does
not establish the broader marked-law limit or an unconditional parent theorem.

Finite algebra controls, using only Python's standard library:

```sh
python -B -S frontiers/gaussian_lifetime_exponential_tail_20261028/check_exact.py
python -B -S -O frontiers/gaussian_lifetime_exponential_tail_20261028/check_exact.py
```

These verify exact finite identities and counterexamples. The continuum
Gaussian and path-functional arguments are supplied by the proof text.
