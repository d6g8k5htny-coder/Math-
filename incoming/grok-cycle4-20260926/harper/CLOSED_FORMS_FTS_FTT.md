# Closed pin-conditional variances on planar Bargmann–Fock

Date: 2026-09-26
Scientific effect: NONE. Exact identities on the planar BF six-pin algebra. Not a parent mixed-block statement and not a SIDE24 landing.

Field: stationary centered Gaussian on `R^2` with
`E[f(x)f(y)] = exp(-|x-y|^2 / 2)`.
Pins at `M = (0,0)` and `S = (r, 0)` in orthonormal coordinates `(t,s)`:
`{f, f_t, f_s}` at each endpoint (six pins).

Unconditional moments used below:
`Var(f) = Var(f_t) = Var(f_s) = Var(f_ts) = 1`, `Var(f_tt) = Var(f_ss) = 3`.

## Identity TS (mixed slaving)

```
Var(f_ts(M) | six pins) = (e^{r^2} - 1 - r^2) / (e^{r^2} - 1).
```

Crosses, computed from the covariance kernel:

```
Cov(f_ts(M), f(M))   = 0
Cov(f_ts(M), f_t(M)) = 0
Cov(f_ts(M), f_s(M)) = 0
Cov(f_ts(M), f(S))   = 0
Cov(f_ts(M), f_t(S)) = 0
Cov(f_ts(M), f_s(S)) = r e^{-r^2/2}
Cov(f_s(M),  f_s(S)) = e^{-r^2/2}
```

Only the pair `(f_s(M), f_s(S))` contributes to the Schur complement. With `c = r e^{-r^2/2}` and `det K = 1 - e^{-r^2}`,

```
1 - c^2 / det K = 1 - r^2 / (e^{r^2} - 1) = (e^{r^2} - 1 - r^2) / (e^{r^2} - 1).
```

Series: `r^2/2 - r^4/12 + r^8/720 + O(r^{12})`; the `r^6` and `r^{10}` coefficients are exactly zero.
Set `beta_M := f_ts(M)/r`. Then

```
Var(beta_M | pins) = (e^{r^2} - 1 - r^2) / (r^2 (e^{r^2} - 1)) -> 1/2.
```

## Identity TT (axial second derivative)

`f_tt(M)` is orthogonal to both transverse pins by `s`-parity:
`Cov(f_tt(M), f_s(M)) = Cov(f_tt(M), f_s(S)) = 0`.
So the six-pin conditional variance equals the four-pin variance on `{f, f_t}` at both ends.

Four-pin Gram `G` (rows/cols: `f(M), f_t(M), f(S), f_t(S)`) has

```
det G = (1 - e^{-r^2})^2 - r^4 e^{-r^2}
      = e^{-2 r^2} ( (e^{r^2} - 1)^2 - r^4 e^{r^2} ).
```

The Schur complement against the cross vector

```
(-1,  0,  (r^2-1) e^{-r^2/2},  r(3-r^2) e^{-r^2/2})
```

yields, with `E := e^{r^2}`,

```
Var(f_tt(M) | pins)
  = ( r^6 E - r^4 E - r^4 + 4 r^2 E - 4 r^2 - 2 E^2 + 4 E - 2 )
    / ( r^4 E - (E - 1)^2 ).
```

Exact series of this rational function:

```
r^4/6 - r^6/30 + r^8/360 - r^{10}/12600 + O(r^{12}).
```

The coefficient `1/360` of `r^8` is therefore an identity coefficient of the closed form, not a truncated numerical inversion of a large Gram. A finite-order Gram inversion that fails to stabilize at `r^8` does not refute the coefficient.

Denominator check (amended 2026-09-27; the first version of this paragraph stated `~ r^6/12`, which was wrong). With `x = r^2`,

```
(e^x - 1)^2 = x^2 + x^3 + (7/12) x^4 + (1/4) x^5 + ...
x^2 e^x     = x^2 + x^3 + (1/2) x^4  + (1/6) x^5 + ...
```

so the `x^2` and `x^3` terms cancel and

```
r^4 E - (E-1)^2 = -(1/12) x^4 - (1/12) x^5 - (2/45) x^6 + ...
                = -r^8/12 - r^{10}/12 - (2/45) r^{12} + O(r^{14}).
```

The first nonzero order of the denominator is `r^8`, with coefficient `-1/12`; there is no `r^6` term. The numerator vanishes to the matching order `r^{12}`:

```
r^6 E - r^4 E - r^4 + 4 r^2 E - 4 r^2 - 2 E^2 + 4 E - 2 = -r^{12}/72 - r^{14}/90 - (7/1440) r^{16} + O(r^{18}),
```

so the ratio is `(-1/72)/(-1/12) r^4 = r^4/6` at leading order, both signs cancel, and the series displayed above follows by exact division of the two expansions. `test_closed_forms.py` asserts the denominator order and leading coefficient, the numerator order, and the quotient coefficients through `r^{10}` with exact rational arithmetic. For `r <~ 0.05` the float64 evaluation of the rational closed form suffers catastrophic cancellation (both numerator and denominator are `O(r^8)` differences of `O(1)` quantities); use the series there.

## What these identities are not

- Not a proof of the parent mixed block on SIDE24.
- Not a replacement for File-3 / Table 4.1 (still ABSENT if still ABSENT).
- Not a D5 count lemma. They only justify the `O_p(r)` slaving of `f_ts(M)` used in the companion obstruction ledger.
