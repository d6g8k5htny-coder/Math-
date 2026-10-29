# Sharp essential-event asymptotics

[Sharp Gaussian action](SHARP_ACTION.md) · [Vanishing critical gap](TINY_GAP.md) ·
[Exact sources](SOURCES.json) · [Verification](VERIFICATION.md)

This additive author-side continuation resolves two quantitative questions
left by PR524. It uses the original pinned Gaussian law and full typed
determinant weight, preserving every predecessor proof file.

| Question | Result | Explicit scope |
| --- | --- | --- |
| Does the fixed-gap exponential coefficient have a limit? | `r^2 log P_r(essential) -> -I(k,u)`, with an exact constrained RKHS variational formula and `I(k,u)=k^2 I(1,u)`. It is independent of birth height. | Each fixed birth, positive gap mark and direction; the predecessor's C4/cube-three spectral class. |
| How much essential mass survives as the critical ratio vanishes? | `p_E(tau) ~ C_E sqrt(tau)`, with an explicit positive finite contact-density integral for `C_E`. | First `r->0` at fixed `k=tau r`, then `tau->0`; C6 summability and positive cube-four spectrum. |

Both classes contain the original periodized Gaussian and explicitly stated
finite Fourier fields. Neither result assumes full function-space support,
inverse-matrix moments or an unproved marked law.

The sharp action proof extracts a shrinking-scale quartic constraint that a
naive global Gaussian cone would miss. Inversion symmetry and strict recovery
profiles then match the upper and lower Gaussian energies. The small-gap
proof separates a fifth-derivative window, controls soft transverse blocks
through the actual determinant weight, and proves a sextic criterion in a
fixed neighborhood before using the global gap.

The quartic cusp weight, its normalization288 and the quintic ridge formula
are existing mathematics and remain explicitly attributed. The additions
are the sharp global action and the actual global square-root essential
share. The energy minimum and density coefficient are characterized exactly;
no numerical evaluation, probability prefactor or joint `r,tau` limit is
claimed.

All four hosted checks on predecessor PR524 succeeded, and its dependency
audit found no missing hypothesis within its stated claims. Different-family
scientific review remains pending for this stack. Same-family internal
critique and exact finite controls provide error detection, not acceptance.

```sh
python -B -S frontiers/essential_sharp_asymptotics_20261028/check_exact.py
python -B -S -O frontiers/essential_sharp_asymptotics_20261028/check_exact.py
```

These standard-library controls check finite algebra and source identities.
The large-deviation, global-geometry and probability arguments are in the
two proof texts, not certified by the script.
