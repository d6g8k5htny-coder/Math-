# d=3, L=4 anisotropic coefficient certificate

**Result:** `0.040415041992 < c_3,4 < 0.040481934343` for the coefficient expression in the pinned parent's equation (15.2).

**Disposition:** author-side rigorous numerical enclosure and proof; independent mathematical review pending. Scientific effect NONE. No parent lifetime theorem is promoted.

Read `PROOF.md` for the derivation, normalization dependency, explicit image/cone/angular error ledger and limitations. `RESULTS.json` contains full outward endpoints. `CROSSCHECKS.json` separates interval computations from floating diagnostics.

## Replay

Python standard library only; tested with CPython 3.13.5 and libmpdec 2.5.1. In the packet directory:

```sh
set -eu
python -B -S -m unittest test_certificate -v
python -B -O -S -m unittest test_certificate -v
python -B -S certificate.py --n 128 > replay.json
cmp replay.json RESULTS.json
python -B -O -S certificate.py --n 128 > replay_optimized.json
cmp replay.json replay_optimized.json
python -B -S certificate.py --reference --n 4 > reference_replay.json
cmp reference_replay.json REFERENCE.json
```

For crosschecks against the exact #297 source, supply its path:

```sh
python -B -S source_crosscheck.py --source ../sources/periodic_jet_check.py > crosschecks_replay.json
cmp crosschecks_replay.json CROSSCHECKS.json
```

In a Math- checkout, use instead:

```sh
python -B -S source_crosscheck.py \
  --source ../../reviews/iba1_periodic_jet_claude_20261005/periodic_jet_check.py
```

The source must have SHA-256 `59b53e5c2e8fdcacc9983f705b9d301fcfcf9242ac6c4d8b7bfbcf0ada7caf9f`; otherwise the crosscheck exits with an error before executing it. The downloadable bundle includes this exact unmodified source under `sources/` and its exact full replay output in `UPSTREAM_REPLAY.json`. It comes from Math- commit `2f8d721e300850e36ab17464dc541c977b3ffcbf`.

The main checker does not need the upstream Python module to run: it implements the same moment law with new outward arithmetic. Its reference normalization consumes the existing certified SIDE24 endpoints and uniform periodization bound, explicitly pinned in `PROOF.md` and the delivery manifest.

## Contents and trust boundaries

`certificate.py` is the certificate calculation; `test_certificate.py` is its focused test suite. `source_crosscheck.py` is a separate falsification harness whose floating disk integral and 270-digit gamma evaluation are **not** certificate error bounds. `RESULTS.json`, `REFERENCE.json`, and `CROSSCHECKS.json` are frozen replay outputs. `PROOF.md` supplies all estimates used to widen the numerical quadrature.

`VALIDATION.json` records the local execution scope and hashes. Nonauthor review, full-repository tests, hosted CI, Lean verification, merge and scientific acceptance are not represented as completed by this delivery.
