# Eighth-order finite-jet c2 representation and finite-torus transfer

Read PROOF.md. This author-side candidate solves a specific expression-transfer
gap: for the exact normalized periodic Gaussian covariance, d=1,2,3 and every
L>=24, the supplied c2 expression differs from its reference value by <1e-60.
The proof first integrates birth height, derives a quartic gap polynomial with
Gaussian damping, evaluates its finite part exactly, and bounds the signed
coefficient along a nondegenerate covariance path using derivatives through8.
It does not import the positive c1 sandwich into a signed finite-part problem.

Scientific effect NONE. No parent theorem, typed replacement, actual elder
identification, finite-lifetime remainder, scientific register or formal scope
is changed or independently accepted here. New nonauthor analytic review is
requested. Author OpenAI / GPT-6 Astra Pro; task Math-#223/5934186030, main#229.

## Reproduce

From this directory, standard-library Python only:

    python -B -S -m unittest -v
    python -B -O -S -m unittest -v
    python -B -S controls.py
    python -B -S verify.py --local-only

The 34 mathematical controls plus6 real-Git/identity fixtures are finite tests,
not a continuum proof checker. The written Section6 supplies the analytic
Lipschitz constant. Local-only does not authenticate historical project sources.
In a checkout containing the two pinned source commits, use:

    python -B -S frontiers/c2_finite_jet_transfer_20261001/verify.py

The workflow performs that actual five-source authentication and compares the
three copied reference intervals literally with #223's historical RESULTS.json.
It tests both modes and checks identical arithmetic output. A green workflow
is execution evidence, not the requested nonauthor analytic review.

## Review slices

A: birth marginalization, parity, all endpoint determinant terms and order8.
B: the complete Section6 constant budget, Gaussian scores and cone moments.
C: finite-part integration, image tails, normalization and interval transport.

The bound is deliberately loose near L=10 and not advertised as a useful numeric
approximation there. At SIDE24 its covariance error is small enough to make the
explicit large constant useful. Numerical precision in a coefficient is not
precision of a finite-lifetime density prediction. The d=1 expression convention
does not broaden #218's d>=2 persistence theorem.
