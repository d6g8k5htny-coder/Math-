# Matching essential-event probability scale

[Full proof](PROOF.md) · [Exact source identities](SOURCES.json) · [Checks](VERIFICATION.md)

For the specified periodized Gaussian field, fixed `d>=2,L>0` and compact
birth/gap ranges with a positive gap floor, this candidate proves

    exp(-C/r^2) <= Q_r^W(essential) <= C' exp(-c/r^2)

when the pin direction is a coordinate axis of the torus. The upper bound
comes from [PR522's source-derived tail proof](../gaussian_lifetime_exponential_tail_20261028/PROOF.md).
The new result is the matching lower bound, improving the previous
qualitative positive-probability statement.

An exact finite-Fourier periodic template has the original pins, a unique
global maximum, the required saddle type, and RKHS norm `O(1/r)`. Its global
maximum survives a fixed C4 ball of zero-pin perturbations. Symmetric Gaussian
translation then gives the lower cost without an extra small-ball premise.

This identifies the logarithmic order `-log(probability)=Theta(r^-2)` at the
stated scope. It supplies an explicit one-sided template cost, not an optimal
rate coefficient. Arbitrary torus rotations and noncompact marks are outside
this result. Different-family scientific review remains pending; no parent
status or source bytes change.

Finite controls use Python's standard library:

```sh
python -B -S frontiers/essential_gaussian_rate_20261028/check_exact.py
python -B -S -O frontiers/essential_gaussian_rate_20261028/check_exact.py
```

They check exact pin/Fourier identities, finite rational Taylor enclosures,
norm coefficients and source identities. The global and Gaussian probability
arguments are proved in the text.
