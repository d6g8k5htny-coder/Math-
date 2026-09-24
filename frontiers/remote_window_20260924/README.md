# Fixed-remote critical points: a cubic shrinking-window estimate

[Research home](https://github.com/d6g8k5htny-coder/main) · [Topic guide](https://github.com/d6g8k5htny-coder/main/blob/main/docs/RESEARCH_INDEX.md) · [Math index](../../README.md) · [Prior RN interface](../three_fronts_20260924/RN_COUNT_INTERFACE.md)

[Read the proof](PROOF.md). For the exact periodized Gaussian field on each fixed torus and compact birth/positive-gap marks, the candidate bounds the actual expected number of remote critical points whose values lie between the two pinned heights. The spatial region stays a **fixed positive distance** from the coalescing pins.

The expected mean measure equals `k*r^3*Lambda(x) dx + O(k*r^4) dx`, with a positive contact Gaussian kernel identified in the proof. The full three-determinant numerator is O(r^5), and the full endpoint normalizer is of order r^2. Additional mutually separated m-witness counts have order r^(3m), with joint rather than factorized coefficients.

**Not supplied:** numerical constants or contact-kernel evaluation; a shrinking spatial exclusion; witness collisions; the historical full RN/24-jet certificate; a Poisson law; independent analytic acceptance. This result does not require the global elder-selection or separating-cap conclusion.

From this directory:

```sh
python -B -S remote_window.py
python -B -S -m unittest -v test_remote_window
python -B -O -S -m unittest -v test_remote_window
python -B -S run_validation.py --output /tmp/remote-window-new-run
```

Choose a new output outside this source directory. The suite contains 28 distinct finite tests and seven deliberate semantic mutations. These exercise exact conditioning, dependence, singular typed determinants, pin transforms, height integration and ordered-count exponents—not the continuum analytic proof. `RESULTS.json` states scope and exact arithmetic examples; it is not a numerical Gaussian certificate.
