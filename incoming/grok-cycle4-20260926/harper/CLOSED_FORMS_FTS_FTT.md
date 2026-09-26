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

Series: `r^2/2 - r^4/12 + O(r^6)`.
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

Denominator check: `r^4 E - (E-1)^2 = 0` would require `(e^{r^2}-1)^2 = r^4 e^{r^2}`. At `r=0` both sides vanish to order `r^4` with ratio `1 != 1` after two further orders (`(r^2 + r^4/2 + ...)^2 = r^4 + r^6 + ...` versus `r^4 (1 + r^2 + ...)`), and the first differing term is `r^6`, so the small-`r` denominator is `~ r^6/12` and the variance is `~ r^4/6`.

## What these identities are not

- Not a proof of the parent mixed block on SIDE24.
- Not a replacement for File-3 / Table 4.1 (still ABSENT if still ABSENT).
- Not a D5 count lemma. They only justify the `O_p(r)` slaving of `f_ts(M)` used in the companion obstruction ledger.
