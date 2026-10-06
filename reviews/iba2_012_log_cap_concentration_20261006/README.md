# Log-cap concentration and growing count order

Conditional author-side mathematical addendum to the existing FR/CT/LT chain.
Read NOTE.md before using a bound. No old proof, scientific status, workflow,
formal target, or parent packet is changed. The named nonauthor review and later
integration receipts are separate evidence, not implied by this README.

## Result and boundary

Let u=log(1/r), Lambda=u/log u, X=N^(1/d)/Lambda. On the specific compact-mark,
fixed-radius multi-soft sector, use the finite measure
mu=rho^(-1) E[K^a 1_E 1_X], rho=r^3 Xi. This is NOT conditioning on E.
The shifted exponential bound controls exp[(c u/8)(X-y0)_+] uniformly.
It gives simultaneous moment bounds for d*s<=(c u/8)*y0 and hence local factorial
negligibility for s=floor(theta Lambda), 0<theta<=B/d, when Xi<=C r^B.
The exact endpoint convention matters; the larger leading threshold is blocked
by the earlier LT abstract family, not by an actual Gaussian-field example.
General IBA2-012/009 and lower normalization denominators remain open.

## Finite replay

Python3.11 or newer, standard library only. From this directory:

```sh
python3 -B -S test_concentration.py
python3 -B -O -S test_concentration.py
python3 -B -S test_concentration.py --mutant M1
```

The baseline has11 methods and exits0. M1-M6 exit1 with the following exact
assertion-name sets, no unexpected test errors. Repeat each in both modes.

| Variant | Intended failing methods |
|---|---|
| M1 | test_half_tail_and_normalization |
| M2 | test_half_tail_and_normalization, test_shifted_tail |
| M3 | test_exponential_gap |
| M4 | test_uniform_order_condition |
| M5 | test_growing_threshold |
| M6 | test_no_conditional_denominator |

UNKNOWN exits2 with argparse's invalid-choice diagnostic and no JSON stdout.
Ordinary unittest output goes to stderr; it is not suppressed. These finite
Fraction/integer checks neither evaluate the Gaussian field nor prove the written
logarithmic, Tonelli or asymptotic arguments. The large dyadic strict-side tests
use integer log2 brackets, not gigantic factorial evaluations or decimal logs.
The critical endpoint is justified separately by the note's second-order proof.

No shared workflow is changed; general CI does not automatically discover this
standalone suite. Local author tests do not substitute for nonauthor mathematics
or the required current-candidate repository checks. The author will not merge.

## Offline custody

SOURCES.json records exact source/blob/SHA256/size identities. Its five inputs
include two provenance-only texts; only FR/P/SH are quantitative premises. Keep
all existing sealed deliveries unchanged. Save new output to a separate outbox,
not into a sealed kit. A Library copy or Linux replay does not prove an actual Mac
installation, disconnected local inference, or complete model/dependency caches.
