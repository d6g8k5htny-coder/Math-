# The third-order coefficient `c2` in closed form (Math-#216 / #218 / #220), Gaussian kernel

`CL-C2-EXACT-20261001-v1`. Author-side exact closed forms with certified enclosures; scientific effect NONE. See `NOTE.md`.

| `d` | `c2` | value |
|---|---|---|
| `1` | `(3/4) 12^(1/6) Gamma(5/6) / pi^(3/2)` (= Math-#214's `2 B_2`) | `0.2300445802661...` |
| `2` | `(13/18) 12^(1/6) Gamma(5/6) / pi^(3/2)` | `0.2215244106266...` |
| `3` | `(5/48)(33 - 7 sqrt6) 12^(1/6) Gamma(5/6) / pi^(5/2)` | `0.1612340491269...` |

`c2/c = kappa_d Gamma(5/6)/(12^(2/3) Gamma(1/6))`, `kappa = 54, 78, 18(141 - sqrt6)/25`.

Replay: `python3 -B -S certificate.py --check` (exact derivation, exact checks, interval evaluation; about one second).
Controls: `python3 -B -S controls.py`. Standard library only.
