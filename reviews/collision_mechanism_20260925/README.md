# Critical-point geometry and collision transfer

[Read the research note](NOTE.md). This is a new OpenAI-authored candidate package, not a status register and not an accepted global persistence theorem.

New derivations: quantitative critical-simplex Hessian bound; sharpness and flattening counterexamples; exact intermediate-saddle determinant identity for the six-pin cubic; a proposed positive saddle contact kernel with vanishing leading extrema kernel on fixed transverse charts; a marked lifetime-transfer theorem with explicit derivative and negative-moment hypotheses; countermodels giving log corrections and changed exponents.

Run from repository root:

```sh
python -B -S reviews/collision_mechanism_20260925/exact_checks.py
python -B -O -S reviews/collision_mechanism_20260925/exact_checks.py
```

There are24 distinct test methods using exact rational/Laurent-polynomial and Gaussian Schur-complement arithmetic. Some methods check explicit false-variant/counterexample cases. This is not a separate mutation-runner count, a continuum Gaussian proof checker, independent analytic acceptance or a novelty certificate.

Review requested: geometry/shape hypotheses; the determinant sum-of-squares identity derived from the complete cubic; conditioned field convergence and full normalizer in the positive contact-kernel theorem; the marked transfer/density assumptions and small-mark failure regimes. The author will not self-award PROVED_REVIEWED. Earlier PR9/PR16/PR22 bodies and all canonical status files remain unchanged.
