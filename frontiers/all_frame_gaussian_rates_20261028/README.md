# All directions, rare lifetimes and the critical-gap split

[Main proof](PROOF.md) · [Critical window](CRITICAL_WINDOW.md) ·
[Exact sources](SOURCES.json) · [Verification](VERIFICATION.md)

This author-side packet extends PR522/523 for the original Gaussian
regression at the two value/full-gradient pins and its full typed
determinant weight. It proves the following without a marked-law or
full-C4-support assumption.

| Regime | Result |
| --- | --- |
| Compact birth/gap ranges, gap bounded away from zero | Essential probability and finite long-lifetime probability both have matching `exp(-Theta(r^-2))` scale, uniformly over every direction. |
| `beta=k/r>=M` for a fixed sufficiently large `M` | Both probabilities have matching `exp(-Theta(beta^2))` scale. The proof retains the moment prefactors. |
| Every fixed `tau>0`, `k=tau r`, then `r->0` | Explicit contact-field formulas split essentiality from finite remote connections; each has positive limiting probability. For fixed `q>0`, `r^-3 E[X^q;finite,X>1]=Theta(r^-4q-3)`. |

The declared class is a fixed centered stationary real Gaussian field on a
fixed cubic torus in dimension `d>=2`, with even nonnegative spectrum,
strict positivity on the finite frequency cube `[-3,3]^d`, and
`sum sqrt(a_n)(1+|n|)^4<infinity`. It includes sufficiently rich band-limited
fields. Constants can depend on that fixed spectrum, dimension and torus.
Under positivity on cube four, a conditional Gaussian mesh argument also
derives Morse/distinct-critical-value genericity at each fixed pin target
and gives the conventional ordinary-H0 interpretation.

The all-direction construction uses genuine lattice Fourier modes and an
exact uniformly bounded pin right inverse. Its global maximum or separating
barrier survives a fixed zero-pin C4 ball. Gaussian translation and actual
determinant/normalizer estimates supply the lower rates. The critical-window
addition combines a fixed-neighborhood Hermite argument with off-contact
Gaussian genericity to identify the GLOBAL essential event.

The quartic cusp model, typed contact weight and local elder decision are
existing mathematics in `cusp_second_order_20261001`, and remain attributed
there. The addition is their global finite/essential split and the explicit
C4 finite-spectrum scope. Along `k=tau r`, the positive essential limit
also rules out uniform inverse-square decay, or uniform `O(r^3)` pairing
failure, across all positive gaps.

The results are conventional proof candidates with exact finite author
controls and separate same-family technical critique. Different-family
scientific review is pending. This packet supplies no status promotion,
formal-kernel result, optimal exponential coefficient or joint small-tau
asymptotic. Existing proof, workflow and status files are preserved.

Run the standard-library finite controls with:

```sh
python -B -S frontiers/all_frame_gaussian_rates_20261028/check_exact.py
python -B -S -O frontiers/all_frame_gaussian_rates_20261028/check_exact.py
```
