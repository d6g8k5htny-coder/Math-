# Typed contact kernel: angular tails, one-integral reduction, annulus interface

Read [NOTE.md](NOTE.md) for the source-bound mathematical statements and proofs.

New results for the explicitly specified PR25 contact integral: an integrable axial envelope; exact elimination of the free Gaussian jet; a sharp left-side Bargmann-Fock angular asymptotic with explicit amplitude; a different right-side logarithmic rate; and a conditional total-variation composition theorem that imports, rather than accepts, PR28's finite-r bound.

The ordinary fixed-transverse upper bound now has a recorded nonauthor review in PR26. That review does not automatically accept these new results or PR25/PR28.

From this directory:

```sh
python -B -S -m unittest -v test_angular_contact
python -B -O -S -m unittest -v test_angular_contact
python -B -S run_validation.py --output /tmp/contact-angular-fresh
python -B -S diagnostic.py --output /tmp/contact-angular-diagnostic.json
```

Choose NEW output paths. The validation runner executes 26 methods and 9 valid-program mutants per mode and preserves all outcomes. The diagnostic is explicitly floating-point, truncated, and unperiodized; it is not a quadrature enclosure or a SIDE24 substitution. Source claims, review dispositions, and scientific statuses are not mutated.

Primary source pins and review boundaries are in NOTE.md. The exact code, written proofs, numerical diagnostic and regression tests answer different questions. No full Gaussian persistence theorem or worldwide priority is claimed.

The full-covariance extension gives sharp left/right logarithmic rates in terms of Var(q|a) and Var(d|a,q,c), retaining the exact periodic covariance. Only the closed elementary left amplitude and numerical diagnostic specialize to unperiodized Bargmann-Fock.
