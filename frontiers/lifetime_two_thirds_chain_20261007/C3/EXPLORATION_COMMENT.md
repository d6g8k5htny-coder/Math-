## Lifetime note C3: exploration scripts and outputs (not controls; not part of the proof)

This publishes the exploration behind note C3's §5 *Values* and Remarks 2, 3 and 6 (note [6027862273](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027862273), controls [6027863516](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027863516)). It uses mpmath, numpy and scipy, so it lies outside the standard-library rule for controls and outside the repository. Nothing here is certified, and nothing here is review evidence.

Dylan Roy — delegated AI work. Actual performers, all Anthropic Claude in session `session_01NMeKEismAyeqgdB4sy2NJU`: the author wrote `c3_values.py` and `mc_summary.py`; two clean-context author-side referees of this session wrote the rest (Slice A: `engine.py`, `lf_indep.py`, `mc_layer.py`, `run_grid.sh`; Slice B: `t1_vec_check.py`). Scientific effect: NONE.

**Extraction rule.** Each file is the exact text between the first fence after its `###` heading (```` ```python ````, ```` ```bash ```` or ```` ```text ````) and the next ```` ``` ```` line, plus a final newline.

**Versions.** Python 3.11.15, mpmath 1.3.0, numpy 2.4.4, scipy 1.17.1. The Monte Carlo streams are fixed by the seeds for these versions; other versions may differ in the last digits.

**Runs.**
- `python3 c3_values.py > c3_values_out.txt` (mpmath only; about 50 s). The numbers of §5 *Values* and Remarks 2–3. The inputs it quotes from sources are listed in its docstring.
- Remark 6, Lemma F₃ (the Slice A referee's Monte Carlo; `engine.py` must sit next to the other two scripts):
  - `python3 lf_indep.py 0.2 0.4 0.6 0.8 > lf_indep.out`, which also writes `lf_indep.json`. It computes `𝐋_F(k)` from the engine's `r = 0` laws without assuming (G.1), and checks the odd jets' law for several `e`.
  - `bash run_grid.sh 2 24 > mc_d2.out` and `bash run_grid.sh 3 16 > mc_d3.out`: `500000 × 24` samples per entry in `d = 2` and `500000 × 16` in `d = 3`, window constant `8`, seed `1000d` (plus `10⁶r + 10³k` inside `mc_layer.py`). The raw JSON lines are not reproduced here.
  - `python3 mc_summary.py mc_d2.out mc_d3.out lf_indep.json > mc_summary.txt`. The output below is byte-identical to the referee's own summary.
- Remark 6, Lemma T₁ (the Slice B referee's quadrature): `python3 t1_vec_check.py 2 5 10 30 100 300 1000 10000 100000 > t1_d2.txt`, then `python3 t1_vec_check.py 3 10 30 100 > t1_d3_a.txt 2>&1` and `python3 t1_vec_check.py 3 300 1000 3000 10000 > t1_d3_b.txt`. The first `d = 3` run printed a numpy `RuntimeWarning`, kept in its output; it comes from a guarded division in the Newton step. In `d = 2` the `κ = 10⁵` row lost precision in double arithmetic and is not used in the note.

**Identities** (bytes, SHA-256):

- `c3_values.py`: 4,200 B, `0836247f355fd4e264f0209516f3fc1c4b56c4f8ee83c40987a930973d7606fd`
- `c3_values_out.txt`: 1,002 B, `c8eead9d80b975b9d60034facebae8c612a78015a067a2e6ae395c13cb88fefa`
- `engine.py`: 3,421 B, `ab03229bf483e4a93289371d4b71c60eb0dcbc873b0f88c146605ba933b7d3cd`
- `lf_indep.py`: 5,763 B, `e95cc3cf036f02eaacf9929260b02ec6012629863df1b840a2ddb478a5a76f29`
- `lf_indep.out`: 2,688 B, `1da2256a69cf2cd99d6708a2a4c45af39f6b69c78abb83c9ec669e861b2ee2f5`
- `mc_layer.py`: 7,975 B, `92a27f3784ff615b4e2321b98f15193705328bf87ddf6bc94b29cbbb32d6f746`
- `run_grid.sh`: 160 B, `a60f56be8a10d09dbfe5398bc50be6700c3621ecc4399abdb3c079f195375f37`
- `mc_summary.py`: 1,574 B, `e05b6efa412fb6b834a0b7bd9e188c839c66dc3a79dfd7d4d21dff4fe3d31dd4`
- `mc_summary.txt`: 8,451 B, `c330400649e0cd39f2049b017a198685ca4af77fd7ce278f3a940cae9b0186e6`
- `t1_vec_check.py`: 5,703 B, `c94f0b92ca873acf6002061e8dafc8d8af7860890e420ff8b66d070314e0a18f`
- `t1_d2.txt`: 1,062 B, `db24ca0f0a8756557d5ffb4e1f2f6cc2093290b9158a2ab8dc1e8c0c0bc9f72c`
- `t1_d3_a.txt`: 650 B, `675ce04dfa0a9f41004b3eb69775692bbdec77f2f7c98055445b856e08e0b6e0`
- `t1_d3_b.txt`: 572 B, `66386af38210e52a54a01c6416756b0ff489a1ea5437985f5fedcf44a28bbf16`

### c3_values.py

```python
"""Exploration (not proof, not a control): the numbers quoted in note C3's section 5 and Remarks 2-3, Gaussian kernel.

mpmath only.  gamma, B independent N(0, 2); X := gamma^2/4 - 3kB; g(k) = E|X|^3 = 15/8 + 27k^2 + 2h(k),
h(k) := E[(3kB - gamma^2/4)_+^3] (the positive representation; with gamma = sqrt2 t, B = sqrt2 z, t, z iid N(0, 1)).
R(k) := e^{-12k^2} g(k)/g(0), so E(k) = (a1/k)(R(k) - 1) (G.2) and J = int_0^inf (R(k) - 1) k^{-8/3} dk (G).
Inputs quoted from the sources: c_{d,inf} (#216, #223), c1 (#207 section 8), c2 (#223's closed forms),
int int F0 (#242 Corollary 1'), R_{2/3} (#244, numerically), #216's elder-density range [1e-4, 1e-2].
"""
import mpmath as mp

mp.mp.dps = 20
S32 = 3 * mp.sqrt(2)


def h(k):
    """E[(3kB - gamma^2/4)_+^3] = 2 int_0^inf phi(t) (ck)^3 E[(z - t^2/(2ck))_+^3] dt, c = 3 sqrt2."""
    k = mp.mpf(k)
    if k == 0:
        return mp.mpf(0)
    s = S32 * k

    def inner(t):
        a = t * t / (2 * s)                     # E[(z - a)_+^3] = (a^2 + 2) phi(a) - a(a^2 + 3)(1 - Phi(a))
        return s ** 3 * ((a * a + 2) * mp.npdf(a) - a * (a * a + 3) * (1 - mp.ncdf(a)))
    return 2 * mp.quad(lambda t: inner(t) * mp.npdf(t), [0, mp.sqrt(s), 1, 3, 8])


def g(k):
    return mp.mpf(15) / 8 + 27 * mp.mpf(k) ** 2 + 2 * h(k)


def R(k):
    k = mp.mpf(k)
    return mp.e ** (-12 * k * k) * g(k) / (mp.mpf(15) / 8)


# the Gamma identity at (a, b) = (12, 72/5): the bracket integrates to 0
br = mp.quad(lambda k: (mp.expm1(-12 * k * k) + mp.e ** (-12 * k * k) * mp.mpf(72) / 5 * k * k) * k ** (-mp.mpf(8) / 3),
             [0, 0.001, 0.01, 0.05, 0.3, 1, 3, mp.inf])
print('Gamma identity at (12, 72/5): int = %s' % mp.nstr(br, 3))
J = mp.mpf(16) / 15 * mp.quad(lambda k: mp.e ** (-12 * k * k) * h(k) * k ** (-mp.mpf(8) / 3), [0, 0.05, 0.2, 0.5, 1, 2, mp.inf])
print('J = %s' % mp.nstr(J, 12))

# the k^{7/2} coefficient of R(k) - 1: (16/15) h(k) ~ (16/15)(32/(35 sqrt pi)) (3k)^{7/2} E[B_+^{7/2}]
c72 = 256 * mp.mpf(6) ** mp.mpf(3.5) * mp.gamma(mp.mpf(9) / 4) / (525 * mp.pi)
print('c_{7/2} = 256 6^{7/2} Gamma(9/4)/(525 pi) = %s' % mp.nstr(c72, 8))
for k in ('0.001', '0.003', '0.01'):
    k = mp.mpf(k)
    print('  k=%s  (R - 1 - (12/5)k^2)/k^{7/2} = %s' % (k, mp.nstr((R(k) - 1 - mp.mpf(12) / 5 * k * k) / k ** mp.mpf(3.5), 8)))

FF = {2: 25 * mp.sqrt(3) / (48 * mp.pi ** 2), 3: 125 * mp.sqrt(30) / (192 * mp.pi ** 3)}      # int int F0 (#242 Cor. 1')
SPH = {2: 2 * mp.pi, 3: 4 * mp.pi}
CINF = {2: mp.mpf('0.0734069193'), 3: mp.mpf('0.0417759318')}                                 # #216, #223
a1 = {d: FF[d] / 10 / SPH[d] for d in (2, 3)}
print('a1 per direction: d=2 %s  d=3 %s;  (12/5) a1 (d=2) = %s' % (mp.nstr(a1[2], 10), mp.nstr(a1[3], 10),
                                                                  mp.nstr(mp.mpf(12) / 5 * a1[2], 8)))
for k in ('0.05', '0.1', '0.2', '0.4', '0.8'):
    r = R(k)
    print('  k=%-4s R(k) = %s   a1 (R - 1)/k^2 (d=2) = %s' % (k, mp.nstr(r, 10), mp.nstr(a1[2] * (r - 1) / mp.mpf(k) ** 2, 6)))
print('E(k) changes sign at k = %s' % mp.nstr(mp.findroot(lambda k: R(k) - 1, mp.mpf('0.37')), 6))
print('1/R(0.8) = %s' % mp.nstr(1 / R('0.8'), 5))

R23 = {2: mp.mpf('-0.048779'), 3: mp.mpf('-0.061375')}                                        # #244 (numerically)
C1 = {2: mp.mpf('-0.26939883'), 3: mp.mpf('-0.21184835')}                                     # #207 section 8
C2 = {2: mp.mpf(13) / 18 * mp.mpf(12) ** (mp.mpf(1) / 6) * mp.gamma(mp.mpf(5) / 6) / mp.pi ** mp.mpf(1.5),
      3: mp.mpf(5) / 48 * (33 - 7 * mp.sqrt(6)) * mp.mpf(12) ** (mp.mpf(1) / 6) * mp.gamma(mp.mpf(5) / 6) / mp.pi ** mp.mpf(2.5)}
for d in (2, 3):
    c3 = J / 30 * FF[d]
    t = c3 - R23[d]
    law = lambda l: CINF[d] * l ** (-mp.mpf(1) / 3) + C1[d] * l ** (mp.mpf(1) / 4) + C2[d] * l ** (mp.mpf(1) / 3)
    lo, hi = mp.mpf('1e-4'), mp.mpf('1e-2')
    base = mp.quad(law, [lo, hi])
    extra = t * (hi ** (mp.mpf(5) / 3) - lo ** (mp.mpf(5) / 3)) * mp.mpf(3) / 5
    print('d=%d  c3 = %s  c3/c = %s  c2 = %s  c3 - R23 = %s = %s c  count ratio on [1e-4, 1e-2] = %s'
          % (d, mp.nstr(c3, 9), mp.nstr(c3 / CINF[d], 7), mp.nstr(C2[d], 9), mp.nstr(t, 7), mp.nstr(t / CINF[d], 6),
             mp.nstr(1 + extra / base, 6)))
```

### c3_values_out.txt

```text
Gamma identity at (12, 72/5): int = -5.66e-9
J = 4.19778198158
c_{7/2} = 256 6^{7/2} Gamma(9/4)/(525 pi) = 93.044619
  k=0.001  (R - 1 - (12/5)k^2)/k^{7/2} = 89.768011
  k=0.003  (R - 1 - (12/5)k^2)/k^{7/2} = 87.250785
  k=0.01  (R - 1 - (12/5)k^2)/k^{7/2} = 81.992282
a1 per direction: d=2 0.001454721257  d=3 0.0009151871836;  (12/5) a1 (d=2) = 0.003491331
  k=0.05 R(k) = 1.007793223   a1 (R - 1)/k^2 (d=2) = 0.00453479
  k=0.1  R(k) = 1.038545938   a1 (R - 1)/k^2 (d=2) = 0.00560736
  k=0.2  R(k) = 1.15017612   a1 (R - 1)/k^2 (d=2) = 0.00546161
  k=0.4  R(k) = 0.8981079013   a1 (R - 1)/k^2 (d=2) = -0.000926404
  k=0.8  R(k) = 0.01696391483   a1 (R - 1)/k^2 (d=2) = -0.00223444
E(k) changes sign at k = 0.369153
1/R(0.8) = 58.949
d=2  c3 = 0.0127896387  c3/c = 0.1742293  c2 = 0.221524411  c3 - R23 = 0.06156864 = 0.838731 c  count ratio on [1e-4, 1e-2] = 1.00377
d=3  c3 = 0.016092311  c3/c = 0.3852053  c2 = 0.161234049  c3 - R23 = 0.07746731 = 1.85435 c  count ratio on [1e-4, 1e-2] = 1.00863
```

### engine.py

```python
"""Referee A: independent Gaussian-kernel engine (C(z) = exp(-|z|^2/2) on R^d).

Written from scratch for the referee pass (does not import or copy the author's exploration code).
Cov(d^a f(x), d^b f(y)) = (-1)^{|b|} (d^{a+b} C)(x - y),  d_x^n e^{-x^2/2} = (-1)^n He_n(x) e^{-x^2/2}.
Rows V_r of #237 (1.1): avg gradient, gradient difference / r, T_r; target v(k) = (0_d, 0_d, 12k).
"""
import mpmath as mp

mp.mp.dps = 60


def He(n, x):
    a, b = mp.mpf(1), x
    if n == 0:
        return a
    for j in range(1, n):
        a, b = b, x * b - j * a
    return b


def dC(gam, z):
    v = mp.mpf(1)
    for g, zz in zip(gam, z):
        v *= (-1) ** g * He(g, zz)
    return v * mp.exp(-sum(zz * zz for zz in z) / 2)


def cov(L1, L2):
    """L = list of (coef, point, multiindex)."""
    s = mp.mpf(0)
    for c1, x, a in L1:
        for c2, y, b in L2:
            z = [xi - yi for xi, yi in zip(x, y)]
            s += c1 * c2 * (-1) ** sum(b) * dC([ai + bi for ai, bi in zip(a, b)], z)
    return s


def ei(d, *idx):
    v = [0] * d
    for i in idx:
        v[i] += 1
    return tuple(v)


def rows(d, r):
    """#237 (1.1) rows; u = e_0, Theta = e_1..e_{d-1}."""
    r = mp.mpf(r)
    M = [-r / 2] + [mp.mpf(0)] * (d - 1)
    S = [r / 2] + [mp.mpf(0)] * (d - 1)
    R = []
    for j in range(d):
        R.append([(mp.mpf(1) / 2, M, ei(d, j)), (mp.mpf(1) / 2, S, ei(d, j))])
    for j in range(d):
        R.append([(1 / r, S, ei(d, j)), (-1 / r, M, ei(d, j))])
    R.append([(6 / r ** 2, M, ei(d, 0)), (6 / r ** 2, S, ei(d, 0)), (-12 / r ** 3, S, ei(d)), (12 / r ** 3, M, ei(d))])
    return R, M, S


def rows0(d):
    """the r = 0 limit V_0 = (grad f(0), d_u grad f(0), d_u^3 f(0))."""
    O = [mp.mpf(0)] * d
    R = [[(mp.mpf(1), O, ei(d, j))] for j in range(d)]
    R += [[(mp.mpf(1), O, ei(d, 0, j))] for j in range(d)]
    R.append([(mp.mpf(1), O, ei(d, 0, 0, 0))])
    return R, O


def target(d, k):
    return [mp.mpf(0)] * (2 * d) + [12 * mp.mpf(k)]


def gauss_density(Sig, v):
    n = Sig.rows
    vv = mp.matrix(v)
    q = (vv.T * (Sig ** -1) * vv)[0, 0]
    return mp.exp(-q / 2) / mp.sqrt((2 * mp.pi) ** n * mp.det(Sig))


def condition(X, V, v):
    """conditional mean/cov of functionals X given V = v; returns (mu, Sc, pV)."""
    SVV = mp.matrix([[cov(a, b) for b in V] for a in V])
    SXV = mp.matrix([[cov(a, b) for b in V] for a in X])
    SXX = mp.matrix([[cov(a, b) for b in X] for a in X])
    K = SXV * SVV ** -1
    mu = K * mp.matrix(v)
    Sc = SXX - K * SXV.T
    return mu, Sc, gauss_density(SVV, v)


def hess_functionals(d, r):
    """scaled endpoint Hessian entries and A(0):
    at P in {M, S}: alpha = f_uu/r, beta_j = f_{u theta_j}/r, A_P[i][j] = f_{theta_i theta_j} (i<=j);
    at 0: A0[i][j] (i<=j). Returns (list of functionals, index map)."""
    R, M, S = rows(d, r)
    r = mp.mpf(r)
    O = [mp.mpf(0)] * d
    X, names = [], []
    for nm, P in (('M', M), ('S', S)):
        X.append([(1 / r, P, ei(d, 0, 0))]); names.append((nm, 'alpha'))
        for j in range(1, d):
            X.append([(1 / r, P, ei(d, 0, j))]); names.append((nm, 'beta', j))
        for i in range(1, d):
            for j in range(i, d):
                X.append([(mp.mpf(1), P, ei(d, i, j))]); names.append((nm, 'A', i, j))
    for i in range(1, d):
        for j in range(i, d):
            X.append([(mp.mpf(1), O, ei(d, i, j))]); names.append(('0', 'A', i, j))
    return X, names, R
```

### lf_indep.py

```python
"""Referee A: independent evaluation of L_F(k) = (12/(9k)) p_{V_0}(v(k)) Lfrak(k), Gaussian kernel, d = 2, 3.

Lfrak(k) = E_k[P^2 |U_red|^3 ; lambda_m = 0-]  (C3 (0.2)-(0.3)), computed from this engine's own r = 0 conditional
laws given V_0 = v(k) -- (G.1) is NOT assumed: the law of (B_ee, gamma_e) is computed for each e, and the edge
density of A is integrated with its general covariance in coordinates A = t I + [[p, c], [c, -p]] (d = 3).
Also prints alternative coefficients (|P|, |P|^3 in place of P^2) so the d = 3 Monte Carlo can discriminate.
"""
import sys
import json
import mpmath as mp
import numpy as np
from engine import rows0, target, condition, ei, cov

mp.mp.dps = 20


def E_abs3(mu, sig):
    """E|mu + sig Z|^3 (closed form; checked against quadrature in selftest)."""
    if sig == 0:
        return abs(mu) ** 3
    m = mu / sig
    return sig ** 3 * ((m ** 3 + 3 * m) * (1 - 2 * mp.ncdf(-m)) + 2 * (m ** 2 + 2) * mp.npdf(m))


def selftest():
    for mu, sig in ((0.3, 1.1), (-2.0, 0.7), (0.0, 2.0)):
        q = mp.quad(lambda z: abs(mu + sig * z) ** 3 * mp.npdf(z), [-mp.inf, -mu / sig, mp.inf])
        assert abs(q - E_abs3(mp.mpf(mu), mp.mpf(sig))) < 1e-15, (mu, sig)


def odd_law(d, k, e):
    """law of (B_ee, gamma_e) given V_0 = v(k): B_ee = sum e_i e_j f_{u ij}, gamma_e = sum e_i f_{uu i}."""
    O = [mp.mpf(0)] * d
    th = range(1, d)
    Bee = [(e[i - 1] * e[j - 1], O, ei(d, 0, i, j)) for i in th for j in th]
    ge = [(e[i - 1], O, ei(d, 0, 0, i)) for i in th]
    V, _ = rows0(d)
    mu, Sc, pV = condition([Bee, ge], V, target(d, k))
    return mu, Sc, pV


def h_k(d, k, e):
    """E|3k B_ee - gamma_e^2/4|^3: integrate gamma_e, closed form in B_ee | gamma_e."""
    mu, Sc, _ = odd_law(d, k, e)
    mB, mg = mu[0], mu[1]
    sBB, sBg, sgg = Sc[0, 0], Sc[0, 1], Sc[1, 1]
    cB = sBg / sgg
    sBc = mp.sqrt(sBB - sBg ** 2 / sgg)
    k = mp.mpf(k)

    def f(g):
        mean = 3 * k * (mB + cB * (g - mg)) - g * g / 4
        return E_abs3(mean, 3 * k * sBc) * mp.npdf(g, mg, mp.sqrt(sgg))
    sg = mp.sqrt(sgg)
    return mp.quad(f, [mg - 14 * sg, mg - 4 * sg, mg, mg + 4 * sg, mg + 14 * sg])


def A_law(d, k):
    O = [mp.mpf(0)] * d
    th = range(1, d)
    X = [[(mp.mpf(1), O, ei(d, i, j))] for i in th for j in th if i <= j]
    V, _ = rows0(d)
    mu, Sc, pV = condition(X, V, target(d, k))
    return mu, Sc, pV


def Lfrak(d, k, power=2):
    """edge expectation E[|P|^power h_k(e); lambda_max(A) = 0-]."""
    muA, SA, pV = A_law(d, k)
    if d == 2:
        # m = 1: P = 1, e = (1); density of A at 0
        assert abs(muA[0]) < 1e-30
        dens0 = mp.npdf(0, 0, mp.sqrt(SA[0, 0]))
        return dens0 * h_k(2, k, [mp.mpf(1)]), pV, {'pA0': dens0, 'varA': SA[0, 0]}
    # d = 3: A = [[a, c], [c, b]]  ->  (t, p, c), t = (a+b)/2, p = (a-b)/2
    T = mp.matrix([[0.5, 0, 0.5], [0.5, 0, -0.5], [0, 1, 0]])   # (a, c, b) -> (t, p, c); engine order is (11, 12, 22)
    S = T * SA * T.T
    Si = S ** -1
    detS = mp.det(S)
    norm = 1 / mp.sqrt((2 * mp.pi) ** 3 * detS)

    def ptpc(t, p, c):
        v = mp.matrix([t, p, c])
        return norm * mp.exp(-(v.T * Si * v)[0, 0] / 2)
    # h_k(e) as a function of the eigenvector angle; e = (cos(psi/2), sin(psi/2)), (p, c) = rho (cos psi, sin psi)
    hcache = {}

    def h_of_psi(psi):
        key = mp.nstr(psi, 25)
        if key not in hcache:
            hcache[key] = h_k(3, k, [mp.cos(psi / 2), mp.sin(psi / 2)])
        return hcache[key]
    # edge: t = -rho, lambda_min = -2 rho, |P| = 2 rho. dp dc = rho drho dpsi.
    def inner(psi):
        hv = h_of_psi(psi)
        return hv * mp.quad(lambda rho: (2 * rho) ** power * ptpc(-rho, rho * mp.cos(psi), rho * mp.sin(psi)) * rho,
                            [0, 1, 3, 8, 20])
    npsi = 12                                    # periodic trapezoid rule (spectrally accurate in psi)
    val = sum(inner(2 * mp.pi * j / npsi) for j in range(npsi)) * 2 * mp.pi / npsi
    return val, pV, {'cov_tpc': [[float(S[i, j]) for j in range(3)] for i in range(3)],
                     'h_spread': [float(min(hcache.values())), float(max(hcache.values()))]}


if __name__ == '__main__':
    selftest()
    ks = [float(x) for x in sys.argv[1:]] or [0.2, 0.4, 0.8]
    out = {}
    for d in (2, 3):
        for k in [0.0] + ks:
            L2, pV, info = Lfrak(d, k, 2)
            rec = {'Lfrak': float(L2), 'pV0': float(pV)}
            if k > 0:
                rec['LF'] = float(12 / (9 * mp.mpf(k)) * pV * L2)
            if d == 3:
                rec['Lfrak_P1'] = float(Lfrak(d, k, 1)[0])
                rec['Lfrak_P3'] = float(Lfrak(d, k, 3)[0])
                rec['h_spread'] = info['h_spread']
                if k == 0.0:
                    rec['cov_tpc'] = info['cov_tpc']
            else:
                rec.update({'pA0': float(info['pA0']), 'varA': float(info['varA'])})
            out['d=%d,k=%g' % (d, k)] = rec
            print(d, k, rec, flush=True)
        # a1 and checks of (G.1) as a by-product: odd law for several e, two k
        a1 = 12 / mp.mpf(9) * out['d=%d,k=0' % d]['pV0'] * out['d=%d,k=0' % d]['Lfrak']
        out['d=%d,a1' % d] = float(a1)
        print('d=%d a1=%s' % (d, mp.nstr(a1, 12)))
    for d, es in ((2, [[1]]), (3, [[1, 0], [0.6, 0.8], [mp.cos(1.1), mp.sin(1.1)]])):
        for k in (0.0, 0.7):
            for e in es:
                mu, Sc, pV = odd_law(d, k, [mp.mpf(x) for x in e])
                print('odd law d=%d k=%g e=%s: mean=(%s,%s) cov=[[%s,%s],[%s,%s]] pV0=%s' % (
                    d, k, [float(x) for x in e], mp.nstr(mu[0], 8), mp.nstr(mu[1], 8), mp.nstr(Sc[0, 0], 10),
                    mp.nstr(Sc[0, 1], 6), mp.nstr(Sc[1, 0], 6), mp.nstr(Sc[1, 1], 10), mp.nstr(pV, 12)))
    json.dump(out, open('lf_indep.json', 'w'), indent=1)
```

### lf_indep.out

```text
2 0.0 {'Lfrak': 0.4580648549089874, 'pV0': 0.002381848183489012, 'pA0': 0.24430125595145996, 'varA': 2.6666666666666665}
2 0.2 {'Lfrak': 0.8514372954441976, 'pV0': 0.001473848097746626, 'LF': 0.00836592825493975, 'pA0': 0.24430125595145996, 'varA': 2.6666666666666665}
2 0.4 {'Lfrak': 2.806085464843272, 'pV0': 0.00034919552643701676, 'LF': 0.003266241637077357, 'pA0': 0.24430125595145996, 'varA': 2.6666666666666665}
2 0.6 {'Lfrak': 7.660822341782289, 'pV0': 3.167830345618511e-05, 'LF': 0.0005392930108153378, 'pA0': 0.24430125595145996, 'varA': 2.6666666666666665}
2 0.8 {'Lfrak': 16.820336350620362, 'pV0': 1.100354073480595e-06, 'LF': 3.084720936786474e-05, 'pA0': 0.24430125595145996, 'varA': 2.6666666666666665}
d=2 a1=0.00145472125678
3 0.0 {'Lfrak': 1.8106603219837012, 'pV0': 0.00037908291209672794, 'Lfrak_P1': 0.7176239480810092, 'Lfrak_P3': 5.382179610607569, 'h_spread': [1.875, 1.875], 'cov_tpc': [[1.6666666666666667, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]}
3 0.2 {'Lfrak': 3.3656014230217126, 'pV0': 0.00023457021012296246, 'LF': 0.005263132219922297, 'Lfrak_P1': 1.333897999272359, 'Lfrak_P3': 10.004234994542692, 'h_spread': [3.4851940982790897, 3.4851940982790897]}
3 0.4 {'Lfrak': 11.092026722496351, 'pV0': 5.5576194138027836e-05, 'LF': 0.002054842101712166, 'Lfrak_P1': 4.396133229504512, 'Lfrak_P3': 32.97099922128384, 'h_spread': [11.486168803818229, 11.486168803818229]}
3 0.6 {'Lfrak': 30.28205918742118, 'pV0': 5.041758583816933e-06, 'LF': 0.000339277404097407, 'Lfrak_P1': 12.001771180522725, 'Lfrak_P3': 90.01328385392044, 'h_spread': [31.358096428715914, 31.358096428715914]}
3 0.8 {'Lfrak': 66.48821734760612, 'pV0': 1.7512678994573932e-07, 'LF': 1.9406446788834798e-05, 'Lfrak_P1': 26.351456678292887, 'Lfrak_P3': 197.63592508719665, 'h_spread': [68.85079769693196, 68.85079769693196]}
d=3 a1=0.000915187183567
odd law d=2 k=0 e=[1.0]: mean=(0.0,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=0.00238184818349
odd law d=2 k=0.7 e=[1.0]: mean=(1.7370793e-24,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=6.65675423059e-6
odd law d=3 k=0 e=[1.0, 0.0]: mean=(0.0,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=0.000379082912097
odd law d=3 k=0 e=[0.6, 0.8]: mean=(0.0,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=0.000379082912097
odd law d=3 k=0 e=[0.4535961214255773, 0.8912073600614354]: mean=(0.0,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=0.000379082912097
odd law d=3 k=0.7 e=[1.0, 0.0]: mean=(1.7370793e-24,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=1.05945534075e-6
odd law d=3 k=0.7 e=[0.6, 0.8]: mean=(4.7451216e-21,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=1.05945534075e-6
odd law d=3 k=0.7 e=[0.4535961214255773, 0.8912073600614354]: mean=(1.7370793e-24,0.0) cov=[[2.0,0.0],[0.0,2.0]] pV0=1.05945534075e-6
```

### mc_layer.py

```python
"""Referee A: independent Monte Carlo of (T_r(k) - S_r(k))/r for the Gaussian kernel, d = 2 and d = 3.

T_r - S_r = 12 p_{V_r}(v(k)) E[Lam],  Lam = r^{-2} Pi (1_typed - 1{A<0}),  r^{-2} Pi = -m_M m_S,  m_i = det K_i / r,
K_i = [[alpha_i, sqrt(r) beta_i^T], [sqrt(r) beta_i, A_i]],  alpha_i = f_uu(i)/r, beta_i = f_{u Theta}(i)/r.
typed: K_M negative definite and K_S of index d-1, decided by EIGENVALUES (not by Haynsworth), so the note's
typedness criterion (Step 3) is tested, not assumed.  Exact Gaussian conditioning on #237's rows V_r (60 digits).
Importance sampling: lambda_max(A) is drawn from a defensive mixture (1/2 a window around 0, 1/2 the exact law),
the remaining jets exactly given A; the estimator is unbiased for any window.
Also records the decomposition Lam1 + Lam2 + Lam3 of Step 3 and checks the criterion
  typed <=> (lambda_max(A_M) < 0 and |x| < y)   whenever A_M, A_S have at most one nonnegative eigenvalue.
"""
import sys
import json
import time
import numpy as np
import mpmath as mp
from engine import hess_functionals, condition, target

mp.mp.dps = 60


def setup(d, r, k):
    X, names, V = hess_functionals(d, r)
    mu, Sc, pV = condition(X, V, target(d, k))
    n = len(X)
    nA = (d - 1) * d // 2
    iY = list(range(n - nA))
    iA = list(range(n - nA, n))
    # transform A-block to the sampling coordinates: d=2: a; d=3: (t, p, c) from (a11, a12, a22)
    if d == 2:
        T = mp.matrix([[1]])
    else:
        T = mp.matrix([[0.5, 0, 0.5], [0.5, 0, -0.5], [0, 1, 0]])
    SAA = mp.matrix([[Sc[i, j] for j in iA] for i in iA])
    SYA = mp.matrix([[Sc[i, j] for j in iA] for i in iY])
    SYY = mp.matrix([[Sc[i, j] for j in iY] for i in iY])
    muA = mp.matrix([mu[i] for i in iA])
    muY = mp.matrix([mu[i] for i in iY])
    Sz = T * SAA * T.T                       # cov of z = T a
    Ti = T ** -1
    # Y | a: mean muY + SYA SAA^{-1}(a - muA), cov SYY - SYA SAA^{-1} SAY ; in terms of z: a = Ti z
    G = SYA * SAA ** -1
    CY = SYY - G * SYA.T
    LY = mp.cholesky(CY)
    f = lambda Mx: np.array([[float(Mx[i, j]) for j in range(Mx.cols)] for i in range(Mx.rows)])
    return dict(d=d, r=r, k=k, pV=float(pV), muA=f(muA)[:, 0], muY=f(muY)[:, 0], Sz=f(Sz), Ti=f(Ti), G=f(G),
                LY=f(LY), names=names, nY=len(iY))


def sample(par, N, rng, Wc):
    d, r, k = par['d'], par['r'], par['k']
    Sz = par['Sz']
    if d == 2:
        sA = np.sqrt(Sz[0, 0])
        Ws = [Wc * r * (1 + 1 / k) * f for f in (0.0625, 0.25, 1.0)]
        comp = rng.integers(0, 4, N)
        lam = rng.normal(0, sA, N)
        for j, W in enumerate(Ws):
            lam = np.where(comp == j + 1, rng.uniform(-W, W, N), lam)
        pex = np.exp(-lam ** 2 / (2 * sA ** 2)) / (np.sqrt(2 * np.pi) * sA)
        q = 0.25 * pex + sum(0.25 * (np.abs(lam) <= W) / (2 * W) for W in Ws)
        w = pex / q
        a = (par['Ti'] @ lam[None, :]).T              # (N, 1)
        lmax = lam
    else:
        # z = (t, p, c); (p, c) from marginal, t | (p, c) from mixture around -rho
        Spc = Sz[1:, 1:]
        Lpc = np.linalg.cholesky(Spc)
        pc = rng.standard_normal((N, 2)) @ Lpc.T
        b = Sz[0, 1:] @ np.linalg.inv(Spc)              # regression of t on (p, c)
        st = np.sqrt(Sz[0, 0] - b @ Sz[1:, 0])
        mt = pc @ b
        rho = np.sqrt(pc[:, 0] ** 2 + pc[:, 1] ** 2)
        Wb = Wc * r * (1 + 1 / k) * (1 + 1 / (2 * rho + np.sqrt(r)))
        Ws = [Wb * f for f in (0.0625, 0.25, 1.0)]
        comp = rng.integers(0, 4, N)
        t = mt + st * rng.standard_normal(N)
        for j, W in enumerate(Ws):
            t = np.where(comp == j + 1, -rho + rng.uniform(-1, 1, N) * W, t)
        pex = np.exp(-(t - mt) ** 2 / (2 * st ** 2)) / (np.sqrt(2 * np.pi) * st)
        q = 0.25 * pex + sum(0.25 * (np.abs(t + rho) <= W) / (2 * W) for W in Ws)
        w = pex / q
        z = np.stack([t, pc[:, 0], pc[:, 1]], axis=1)
        a = z @ par['Ti'].T                            # (a11, a12, a22)
        lmax = t + rho
    Y = par['muY'][None, :] + (a - par['muA'][None, :]) @ par['G'].T + rng.standard_normal((N, par['nY'])) @ par['LY'].T
    return a, Y, w, lmax


def evaluate(par, a, Y, lmax):
    d, r = par['d'], par['r']
    m = d - 1
    s = (-1) ** m
    nP = 1 + (d - 1) + (d - 1) * d // 2

    def block(off):
        al = Y[:, off]
        be = Y[:, off + 1: off + d]
        Avals = Y[:, off + d: off + nP]
        N = Y.shape[0]
        K = np.zeros((N, d, d))
        K[:, 0, 0] = al
        K[:, 0, 1:] = np.sqrt(r) * be
        K[:, 1:, 0] = np.sqrt(r) * be
        Am = np.zeros((N, m, m))
        t = 0
        for i in range(m):
            for j in range(i, m):
                Am[:, i, j] = Avals[:, t]
                Am[:, j, i] = Avals[:, t]
                t += 1
        K[:, 1:, 1:] = Am
        # m_i = det K / r = alpha det A / r - beta^T adj(A) beta  (exact algebra, avoids dividing a float det by r)
        if m == 1:
            detA = Am[:, 0, 0]
            badjb = be[:, 0] ** 2
        else:
            detA = Am[:, 0, 0] * Am[:, 1, 1] - Am[:, 0, 1] ** 2
            badjb = Am[:, 1, 1] * be[:, 0] ** 2 - 2 * Am[:, 0, 1] * be[:, 0] * be[:, 1] + Am[:, 0, 0] * be[:, 1] ** 2
        mi = al * detA / r - badjb
        ev = np.linalg.eigvalsh(K)
        evA = np.linalg.eigvalsh(Am)
        return mi, ev, evA
    mM, evM, evAM = block(0)
    mS, evS, evAS = block(nP)
    typed = (evM < 0).all(axis=1) & ((evS < 0).sum(axis=1) == d - 1)
    neg = lmax < 0
    Lam = -mM * mS * (typed.astype(float) - neg.astype(float))
    x = s * (mM + mS) / 2
    y = s * (mS - mM) / 2
    lamM = evAM[:, -1]
    L1 = (x * x - y * y) * (neg & (np.abs(x) >= y))
    L2 = -(y * y - x * x) * (neg & (np.abs(x) < y) & (lamM >= 0))
    L3 = (y * y - x * x) * ((~neg) & (lamM < 0) & (np.abs(x) < y))
    # criterion check where A_M and A_S have at most one nonnegative eigenvalue
    ok_dom = (evAM[:, 0] < 0) & (evAS[:, 0] < 0) if m >= 2 else np.ones(len(x), bool)
    crit = (lamM < 0) & (np.abs(x) < y)
    mism = ok_dom & (crit != typed)
    hits = np.array([int((neg & (lamM >= 0)).sum()), int((L2 != 0).sum()), int((L3 != 0).sum()),
                     int(((~neg) & (lamM < 0)).sum())])
    return Lam, L1, L2, L3, mism, ok_dom, hits


def run(d, r, k, N, chunks, Wc, seed):
    par = setup(d, r, k)
    rng = np.random.default_rng(seed)
    S = np.zeros(4)
    S2 = np.zeros(4)
    mism = 0
    ndom = 0
    nn = 0
    resid = 0.0
    hits = np.zeros(4, int)
    for _ in range(chunks):
        a, Y, w, lmax = sample(par, N, rng, Wc)
        Lam, L1, L2, L3, mm, od, hh = evaluate(par, a, Y, lmax)
        hits += hh
        vals = np.stack([Lam, L1, L2, L3]) * w[None, :]
        S += vals.sum(axis=1)
        S2 += (vals ** 2).sum(axis=1)
        mism += int(mm.sum())
        ndom += int(od.sum())
        resid = max(resid, float(np.max(np.abs(Lam - (L1 + L2 + L3))[od])) if od.any() else 0.0)
        nn += N
    mean = S / nn
    se = np.sqrt((S2 / nn - mean ** 2) / nn)
    fac = 12 * par['pV'] / r
    return dict(d=d, r=r, k=k, n=nn, Wc=Wc, pV=par['pV'], D_over_r=float(mean[0] * fac), se=float(se[0] * fac),
                L1=float(mean[1] * fac), L1se=float(se[1] * fac), L2=float(mean[2] * fac), L2se=float(se[2] * fac),
                L3=float(mean[3] * fac), L3se=float(se[3] * fac), criterion_mismatches=mism, criterion_domain=ndom,
                max_decomp_residual=resid, hits_strip_L2_L3_Mstrip=[int(h) for h in hits])


if __name__ == '__main__':
    d = int(sys.argv[1])
    k = float(sys.argv[2])
    rs = [float(x) for x in sys.argv[3].split(',')]
    N = int(sys.argv[4])
    chunks = int(sys.argv[5])
    Wc = float(sys.argv[6]) if len(sys.argv) > 6 else 8.0
    seed = int(sys.argv[7]) if len(sys.argv) > 7 else 7
    res = []
    for r in rs:
        t0 = time.time()
        out = run(d, r, k, N, chunks, Wc, seed + int(1e6 * r) + int(1e3 * k))
        out['sec'] = round(time.time() - t0, 1)
        print(json.dumps(out), flush=True)
        res.append(out)
```

### run_grid.sh

```bash
#!/bin/bash
# d k rlist N chunks Wc seed
d=$1
for k in 0.2 0.4 0.6 0.8; do
  python3 mc_layer.py $d $k 0.0025,0.005,0.01,0.02,0.04 500000 $2 8 $((1000*d))
done
```

### mc_summary.py

```python
"""Summarize mc_layer.py output against lf_indep.py's L_F (author's summarizer for the Slice A referee's runs).

Usage: python3 mc_summary.py mc_d2.out mc_d3.out lf_indep.json > mc_summary.txt
"""
import json
import sys

lf = json.load(open(sys.argv[3]))
zs = []
for path in sys.argv[1:3]:
    rows = [json.loads(line) for line in open(path) if line.startswith('{')]
    d = rows[0]['d']
    print('d=%d   ratio (T_r-S_r)/(r L_F)   [L_F from lf_indep.py; MC from mc_layer.py]' % d)
    a1 = lf['d=%d,a1' % d]
    for x in rows:
        rec = lf['d=%d,k=%g' % (d, x['k'])]
        LF = rec['LF']
        ratio, se = x['D_over_r'] / LF, x['se'] / LF
        z = (ratio - 1) / se
        zs.append(z)
        h = x['hits_strip_L2_L3_Mstrip']
        line = ('  k=%g r=%.4f n=%.1e  (T-S)/r=%.6e+-%.1e  L_F=%.6e  ratio=%.4f+-%.4f (z=%+.2f)  vs a1/k: %.4f  L2/r=%.1e '
                'L3/r=%.1e strip=%d L2hits=%d crit_mism=%d'
                % (x['k'], x['r'], x['n'], x['D_over_r'], x['se'], LF, ratio, se, z, x['D_over_r'] / (a1 / x['k']),
                   x['L2'], x['L3'], h[0], h[1], x['criterion_mismatches']))
        if d == 3:
            line += ' | ratio if |P|: %.3f, if |P|^3: %.3f' % (ratio * rec['Lfrak'] / rec['Lfrak_P1'],
                                                                ratio * rec['Lfrak'] / rec['Lfrak_P3'])
        print(line)
n = len(zs)
print('all %d points: mean z = %.3f, rms z = %.3f, max |z| = %.2f, chi2/dof = %.3f'
      % (n, sum(zs) / n, (sum(z * z for z in zs) / n) ** 0.5, max(abs(z) for z in zs), sum(z * z for z in zs) / n))
```

### mc_summary.txt

```text
d=2   ratio (T_r-S_r)/(r L_F)   [L_F from lf_indep.py; MC from mc_layer.py]
  k=0.2 r=0.0025 n=1.2e+07  (T-S)/r=8.335476e-03+-2.8e-05  L_F=8.365928e-03  ratio=0.9964+-0.0034 (z=-1.08)  vs a1/k: 1.1460  L2/r=0.0e+00 L3/r=0.0e+00 strip=185456 L2hits=0 crit_mism=0
  k=0.2 r=0.0050 n=1.2e+07  (T-S)/r=8.385765e-03+-2.8e-05  L_F=8.365928e-03  ratio=1.0024+-0.0033 (z=+0.72)  vs a1/k: 1.1529  L2/r=0.0e+00 L3/r=1.4e-14 strip=186136 L2hits=0 crit_mism=0
  k=0.2 r=0.0100 n=1.2e+07  (T-S)/r=8.387002e-03+-2.8e-05  L_F=8.365928e-03  ratio=1.0025+-0.0033 (z=+0.76)  vs a1/k: 1.1531  L2/r=0.0e+00 L3/r=1.1e-14 strip=187422 L2hits=0 crit_mism=0
  k=0.2 r=0.0200 n=1.2e+07  (T-S)/r=8.364431e-03+-2.7e-05  L_F=8.365928e-03  ratio=0.9998+-0.0032 (z=-0.06)  vs a1/k: 1.1500  L2/r=0.0e+00 L3/r=7.5e-12 strip=189574 L2hits=0 crit_mism=0
  k=0.2 r=0.0400 n=1.2e+07  (T-S)/r=8.377875e-03+-2.7e-05  L_F=8.365928e-03  ratio=1.0014+-0.0032 (z=+0.44)  vs a1/k: 1.1518  L2/r=0.0e+00 L3/r=5.9e-11 strip=194158 L2hits=0 crit_mism=0
  k=0.4 r=0.0025 n=1.2e+07  (T-S)/r=3.265358e-03+-7.0e-06  L_F=3.266242e-03  ratio=0.9997+-0.0021 (z=-0.13)  vs a1/k: 0.8979  L2/r=0.0e+00 L3/r=0.0e+00 strip=316867 L2hits=0 crit_mism=0
  k=0.4 r=0.0050 n=1.2e+07  (T-S)/r=3.261602e-03+-6.9e-06  L_F=3.266242e-03  ratio=0.9986+-0.0021 (z=-0.67)  vs a1/k: 0.8968  L2/r=0.0e+00 L3/r=2.7e-15 strip=317274 L2hits=0 crit_mism=0
  k=0.4 r=0.0100 n=1.2e+07  (T-S)/r=3.261799e-03+-7.0e-06  L_F=3.266242e-03  ratio=0.9986+-0.0021 (z=-0.64)  vs a1/k: 0.8969  L2/r=0.0e+00 L3/r=5.0e-14 strip=318430 L2hits=0 crit_mism=0
  k=0.4 r=0.0200 n=1.2e+07  (T-S)/r=3.276237e-03+-6.9e-06  L_F=3.266242e-03  ratio=1.0031+-0.0021 (z=+1.44)  vs a1/k: 0.9009  L2/r=0.0e+00 L3/r=1.9e-12 strip=320472 L2hits=0 crit_mism=0
  k=0.4 r=0.0400 n=1.2e+07  (T-S)/r=3.275210e-03+-6.9e-06  L_F=3.266242e-03  ratio=1.0027+-0.0021 (z=+1.31)  vs a1/k: 0.9006  L2/r=0.0e+00 L3/r=1.2e-11 strip=324488 L2hits=0 crit_mism=0
  k=0.6 r=0.0025 n=1.2e+07  (T-S)/r=5.373995e-04+-9.8e-07  L_F=5.392930e-04  ratio=0.9965+-0.0018 (z=-1.93)  vs a1/k: 0.2217  L2/r=0.0e+00 L3/r=0.0e+00 strip=407032 L2hits=0 crit_mism=0
  k=0.6 r=0.0050 n=1.2e+07  (T-S)/r=5.416492e-04+-9.9e-07  L_F=5.392930e-04  ratio=1.0044+-0.0018 (z=+2.38)  vs a1/k: 0.2234  L2/r=0.0e+00 L3/r=0.0e+00 strip=408842 L2hits=0 crit_mism=0
  k=0.6 r=0.0100 n=1.2e+07  (T-S)/r=5.411256e-04+-9.9e-07  L_F=5.392930e-04  ratio=1.0034+-0.0018 (z=+1.86)  vs a1/k: 0.2232  L2/r=0.0e+00 L3/r=0.0e+00 strip=410164 L2hits=0 crit_mism=0
  k=0.6 r=0.0200 n=1.2e+07  (T-S)/r=5.389907e-04+-9.8e-07  L_F=5.392930e-04  ratio=0.9994+-0.0018 (z=-0.31)  vs a1/k: 0.2223  L2/r=0.0e+00 L3/r=6.0e-13 strip=410725 L2hits=0 crit_mism=0
  k=0.6 r=0.0400 n=1.2e+07  (T-S)/r=5.401148e-04+-9.8e-07  L_F=5.392930e-04  ratio=1.0015+-0.0018 (z=+0.84)  vs a1/k: 0.2228  L2/r=0.0e+00 L3/r=8.5e-12 strip=415400 L2hits=0 crit_mism=0
  k=0.8 r=0.0025 n=1.2e+07  (T-S)/r=3.073381e-05+-5.4e-08  L_F=3.084721e-05  ratio=0.9963+-0.0017 (z=-2.10)  vs a1/k: 0.0169  L2/r=0.0e+00 L3/r=5.8e-17 strip=471098 L2hits=0 crit_mism=0
  k=0.8 r=0.0050 n=1.2e+07  (T-S)/r=3.083023e-05+-5.4e-08  L_F=3.084721e-05  ratio=0.9994+-0.0017 (z=-0.32)  vs a1/k: 0.0170  L2/r=0.0e+00 L3/r=2.8e-17 strip=471863 L2hits=0 crit_mism=0
  k=0.8 r=0.0100 n=1.2e+07  (T-S)/r=3.089922e-05+-5.4e-08  L_F=3.084721e-05  ratio=1.0017+-0.0018 (z=+0.96)  vs a1/k: 0.0170  L2/r=0.0e+00 L3/r=1.5e-15 strip=474511 L2hits=0 crit_mism=0
  k=0.8 r=0.0200 n=1.2e+07  (T-S)/r=3.092277e-05+-5.4e-08  L_F=3.084721e-05  ratio=1.0024+-0.0017 (z=+1.40)  vs a1/k: 0.0170  L2/r=0.0e+00 L3/r=1.4e-14 strip=475033 L2hits=0 crit_mism=0
  k=0.8 r=0.0400 n=1.2e+07  (T-S)/r=3.086701e-05+-5.3e-08  L_F=3.084721e-05  ratio=1.0006+-0.0017 (z=+0.37)  vs a1/k: 0.0170  L2/r=0.0e+00 L3/r=2.4e-13 strip=477891 L2hits=0 crit_mism=0
d=3   ratio (T_r-S_r)/(r L_F)   [L_F from lf_indep.py; MC from mc_layer.py]
  k=0.2 r=0.0025 n=8.0e+06  (T-S)/r=5.254105e-03+-2.5e-05  L_F=5.263132e-03  ratio=0.9983+-0.0048 (z=-0.36)  vs a1/k: 1.1482  L2/r=0.0e+00 L3/r=0.0e+00 strip=83502 L2hits=0 crit_mism=0 | ratio if |P|: 2.519, if |P|^3: 0.336
  k=0.2 r=0.0050 n=8.0e+06  (T-S)/r=5.234466e-03+-2.5e-05  L_F=5.263132e-03  ratio=0.9946+-0.0048 (z=-1.13)  vs a1/k: 1.1439  L2/r=0.0e+00 L3/r=0.0e+00 strip=84219 L2hits=0 crit_mism=0 | ratio if |P|: 2.509, if |P|^3: 0.335
  k=0.2 r=0.0100 n=8.0e+06  (T-S)/r=5.254087e-03+-2.6e-05  L_F=5.263132e-03  ratio=0.9983+-0.0049 (z=-0.35)  vs a1/k: 1.1482  L2/r=0.0e+00 L3/r=9.5e-15 strip=85026 L2hits=0 crit_mism=0 | ratio if |P|: 2.519, if |P|^3: 0.336
  k=0.2 r=0.0200 n=8.0e+06  (T-S)/r=5.214700e-03+-2.5e-05  L_F=5.263132e-03  ratio=0.9908+-0.0047 (z=-1.96)  vs a1/k: 1.1396  L2/r=-3.2e-11 L3/r=1.1e-13 strip=86578 L2hits=1 crit_mism=0 | ratio if |P|: 2.500, if |P|^3: 0.333
  k=0.2 r=0.0400 n=8.0e+06  (T-S)/r=5.225051e-03+-2.4e-05  L_F=5.263132e-03  ratio=0.9928+-0.0046 (z=-1.57)  vs a1/k: 1.1419  L2/r=-1.6e-10 L3/r=1.9e-10 strip=89920 L2hits=3 crit_mism=0 | ratio if |P|: 2.505, if |P|^3: 0.334
  k=0.4 r=0.0025 n=8.0e+06  (T-S)/r=2.053533e-03+-6.6e-06  L_F=2.054842e-03  ratio=0.9994+-0.0032 (z=-0.20)  vs a1/k: 0.8975  L2/r=0.0e+00 L3/r=0.0e+00 strip=143214 L2hits=0 crit_mism=0 | ratio if |P|: 2.522, if |P|^3: 0.336
  k=0.4 r=0.0050 n=8.0e+06  (T-S)/r=2.051214e-03+-6.5e-06  L_F=2.054842e-03  ratio=0.9982+-0.0031 (z=-0.56)  vs a1/k: 0.8965  L2/r=0.0e+00 L3/r=0.0e+00 strip=143964 L2hits=0 crit_mism=0 | ratio if |P|: 2.519, if |P|^3: 0.336
  k=0.4 r=0.0100 n=8.0e+06  (T-S)/r=2.048956e-03+-6.5e-06  L_F=2.054842e-03  ratio=0.9971+-0.0032 (z=-0.91)  vs a1/k: 0.8955  L2/r=0.0e+00 L3/r=6.3e-14 strip=144985 L2hits=0 crit_mism=0 | ratio if |P|: 2.516, if |P|^3: 0.335
  k=0.4 r=0.0200 n=8.0e+06  (T-S)/r=2.049210e-03+-6.5e-06  L_F=2.054842e-03  ratio=0.9973+-0.0031 (z=-0.87)  vs a1/k: 0.8956  L2/r=0.0e+00 L3/r=4.7e-13 strip=146907 L2hits=0 crit_mism=0 | ratio if |P|: 2.516, if |P|^3: 0.335
  k=0.4 r=0.0400 n=8.0e+06  (T-S)/r=2.043951e-03+-6.4e-06  L_F=2.054842e-03  ratio=0.9947+-0.0031 (z=-1.70)  vs a1/k: 0.8933  L2/r=0.0e+00 L3/r=3.1e-11 strip=150659 L2hits=0 crit_mism=0 | ratio if |P|: 2.510, if |P|^3: 0.335
  k=0.6 r=0.0025 n=8.0e+06  (T-S)/r=3.399424e-04+-9.2e-07  L_F=3.392774e-04  ratio=1.0020+-0.0027 (z=+0.72)  vs a1/k: 0.2229  L2/r=0.0e+00 L3/r=0.0e+00 strip=187230 L2hits=0 crit_mism=0 | ratio if |P|: 2.528, if |P|^3: 0.337
  k=0.6 r=0.0050 n=8.0e+06  (T-S)/r=3.396007e-04+-9.2e-07  L_F=3.392774e-04  ratio=1.0010+-0.0027 (z=+0.35)  vs a1/k: 0.2226  L2/r=0.0e+00 L3/r=6.6e-15 strip=188653 L2hits=0 crit_mism=0 | ratio if |P|: 2.526, if |P|^3: 0.337
  k=0.6 r=0.0100 n=8.0e+06  (T-S)/r=3.388321e-04+-9.1e-07  L_F=3.392774e-04  ratio=0.9987+-0.0027 (z=-0.49)  vs a1/k: 0.2221  L2/r=0.0e+00 L3/r=7.6e-15 strip=189588 L2hits=0 crit_mism=0 | ratio if |P|: 2.520, if |P|^3: 0.336
  k=0.6 r=0.0200 n=8.0e+06  (T-S)/r=3.389526e-04+-9.1e-07  L_F=3.392774e-04  ratio=0.9990+-0.0027 (z=-0.36)  vs a1/k: 0.2222  L2/r=0.0e+00 L3/r=8.3e-14 strip=190967 L2hits=0 crit_mism=0 | ratio if |P|: 2.521, if |P|^3: 0.336
  k=0.6 r=0.0400 n=8.0e+06  (T-S)/r=3.373920e-04+-8.9e-07  L_F=3.392774e-04  ratio=0.9944+-0.0026 (z=-2.12)  vs a1/k: 0.2212  L2/r=-3.6e-12 L3/r=4.8e-12 strip=196328 L2hits=1 crit_mism=0 | ratio if |P|: 2.509, if |P|^3: 0.335
  k=0.8 r=0.0025 n=8.0e+06  (T-S)/r=1.950774e-05+-4.9e-08  L_F=1.940645e-05  ratio=1.0052+-0.0025 (z=+2.07)  vs a1/k: 0.0171  L2/r=0.0e+00 L3/r=0.0e+00 strip=221461 L2hits=0 crit_mism=0 | ratio if |P|: 2.536, if |P|^3: 0.338
  k=0.8 r=0.0050 n=8.0e+06  (T-S)/r=1.946598e-05+-4.9e-08  L_F=1.940645e-05  ratio=1.0031+-0.0025 (z=+1.21)  vs a1/k: 0.0170  L2/r=0.0e+00 L3/r=2.4e-17 strip=221533 L2hits=0 crit_mism=0 | ratio if |P|: 2.531, if |P|^3: 0.337
  k=0.8 r=0.0100 n=8.0e+06  (T-S)/r=1.943223e-05+-4.9e-08  L_F=1.940645e-05  ratio=1.0013+-0.0025 (z=+0.53)  vs a1/k: 0.0170  L2/r=0.0e+00 L3/r=2.4e-16 strip=222458 L2hits=0 crit_mism=0 | ratio if |P|: 2.526, if |P|^3: 0.337
  k=0.8 r=0.0200 n=8.0e+06  (T-S)/r=1.937124e-05+-4.8e-08  L_F=1.940645e-05  ratio=0.9982+-0.0025 (z=-0.73)  vs a1/k: 0.0169  L2/r=0.0e+00 L3/r=1.5e-14 strip=225581 L2hits=0 crit_mism=0 | ratio if |P|: 2.519, if |P|^3: 0.336
  k=0.8 r=0.0400 n=8.0e+06  (T-S)/r=1.935512e-05+-4.8e-08  L_F=1.940645e-05  ratio=0.9974+-0.0025 (z=-1.06)  vs a1/k: 0.0169  L2/r=-1.4e-14 L3/r=1.5e-13 strip=230153 L2hits=1 crit_mism=0 | ratio if |P|: 2.516, if |P|^3: 0.336
all 40 points: mean z = -0.106, rms z = 1.164, max |z| = 2.38, chi2/dof = 1.354
```

### t1_vec_check.py

```python
"""Referee B: vectorized independent check of Lemma T1 (the cusp tail) for the Gaussian kernel, d = 2 and d = 3.

G(kappa) := kappa (scrA(kappa) - A2(0)) = kappa * 12 p0 E_{Qbar_{0,0}}[(Y'^2 - 36 kappa^2 Delta^2)_+ 1{A<0}]   ((3.1)),
claimed limit a1 = (1/10) int F0 db (per direction), with #242 Cor. 1':
  d = 2: int int F0 db dsigma = 25 sqrt(3)/(48 pi^2),   |S^1| = 2 pi
  d = 3: int int F0 db dsigma = 125 sqrt(30)/(192 pi^3), |S^2| = 4 pi

Jet laws under Qbar_{0,0} (derived independently by the referee from the derivative moments of exp(-|z|^2/2)):
  d = 2: (A, f4) ~ N(0, [[8/3, 2], [2, 30]]), gamma ~ N(0, 2) independent; p0 = (2pi)^{-5/2} 18^{-1/2}.
  d = 3: A = t I + traceless, t ~ N(0, 5/3), traceless coordinates iid N(0,1) (eigenvalues t +- rho, rho ~ Rayleigh(1),
         uniform frame), f4 | t ~ N(6t/5, 138/5) (independent of the traceless part), gamma ~ N(0, 2 I_2) independent;
         p0 = (2pi)^{-7/2} 18^{-1/2}.  In the eigenframe, adj A = P e e^T + lambda e1 e1^T, with lambda = t + rho (top),
         P = t - rho; gamma^T adj(A) gamma = P ge^2 + lambda gp^2, ge, gp iid N(0, 2) whatever the frame.
f4 is integrated in closed form (Y' is affine in f4). The A-variable at the edge is lambda = -s/kappa, and
kappa * int d(lambda) = int ds. The s-integral uses Gauss-Legendre panels around the kink of the sigma = 0 integrand.
"""
import sys
import numpy as np
from numpy.polynomial.hermite_e import hermegauss
from numpy.polynomial.legendre import leggauss
from scipy.special import ndtr

SQ2PI = np.sqrt(2 * np.pi)


def npdf(z):
    return np.exp(-0.5 * z * z) / SQ2PI


def e_plus(mu, s, c):
    """E[(Y^2 - c^2)_+] for Y ~ N(mu, s^2), s > 0."""
    z0 = (c - mu) / s
    z1 = (-c - mu) / s
    q = ndtr(-z0) + ndtr(z1)
    return (mu * mu + s * s - c * c) * q + s * ((mu + c) * npdf(z0) + (c - mu) * npdf(z1))


def panels(lo_kink, kink, width, n):
    """Gauss-Legendre nodes/weights on [0, kink-width], [kink-width, kink-width/10], ..., [kink+width/10, kink+width]."""
    x, w = leggauss(n)
    a0 = np.maximum(kink - width, 0.5 * kink)
    edges = [np.zeros_like(kink), a0, kink - (kink - a0) / 10, kink, kink + width / 10, kink + width]
    S, W = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        h = (b - a) / 2
        S.append(a[..., None] + h[..., None] * (x + 1))
        W.append(h[..., None] * w)
    return np.concatenate(S, axis=-1), np.concatenate(W, axis=-1)


def G_d2(kappa, ng=120, n=60):
    VA, VF, CAF = 8 / 3, 30.0, 2.0
    SF = np.sqrt(VF - CAF ** 2 / VA)
    p0 = (2 * np.pi) ** (-2.5) / np.sqrt(18)
    xg, wg = hermegauss(ng)
    g = np.sqrt(2) * xg
    wg = wg / SQ2PI
    ts = 8 * kappa ** 2 * (np.sqrt(36 + g * g / (16 * kappa ** 2)) - 6)
    ts = np.maximum(ts, 1e-300)
    width = ts * 40 * SF / (72 * kappa)
    T, WT = panels(None, ts, width, n)
    A = -T / kappa
    mu = A * A / 16 - (g * g / 4)[:, None]
    s = T * SF / (12 * kappa)
    val = npdf(A / np.sqrt(VA)) / np.sqrt(VA) * e_plus(mu, s, 6 * T)
    inner = np.sum(val * WT, axis=1)
    return 12 * p0 * np.sum(wg * inner)


def G_d3(kappa, nge=64, ngp=24, nrho=64, n=40, rho_max=9.0):
    p0 = (2 * np.pi) ** (-3.5) / np.sqrt(18)
    vt = 5 / 3
    sf4 = np.sqrt(138 / 5)
    xe, we = hermegauss(nge)
    xp, wp = hermegauss(ngp)
    ge_all, we = np.sqrt(2) * xe, we / SQ2PI
    gp, wp = np.sqrt(2) * xp, wp / SQ2PI
    xr, wr = leggauss(nrho)
    rho = rho_max / 2 * (xr + 1)
    wr = rho_max / 2 * wr * rho * np.exp(-rho * rho / 2)          # Rayleigh(1) weight folded in
    total = 0.0
    for ge, wge in zip(ge_all, we):
        R, GP = np.meshgrid(rho, gp, indexing="ij")              # (nrho, ngp)
        Wgrid = np.outer(wr, wp)

        def parts(sv):
            lam = -sv / kappa
            P = lam - 2 * R[..., None] if sv.ndim == 3 else lam - 2 * R
            t = lam - (R[..., None] if sv.ndim == 3 else R)
            Dl = lam * P
            gpp = GP[..., None] if sv.ndim == 3 else GP
            mu = t * Dl / 10 - (P * ge * ge + lam * gpp * gpp) / 4
            sig = np.abs(Dl) * sf4 / 12
            c = 6 * sv * np.abs(P)
            return mu, sig, c, t
        # kink: |mu(s)| = c(s); Newton from s = ge^2/24 (vectorized, with a safeguard)
        sk = np.full(R.shape, ge * ge / 24 + 1e-300)
        for _ in range(30):
            h = 1e-7 * np.maximum(sk, 1e-12)
            m1, _, c1, _ = parts(sk)
            m2, _, c2, _ = parts(sk + h)
            f1 = np.abs(m1) - c1
            f2 = np.abs(m2) - c2
            d = (f2 - f1) / h
            step = np.where(d != 0, f1 / d, 0.0)
            sk = np.clip(sk - step, 0.5 * sk, 2 * sk + 1e-300)
        width = sk * 40 * sf4 / (72 * kappa) + 1e-300
        S, WS = panels(None, sk, width, n)                      # (nrho, ngp, npts)
        mu, sig, c, t = parts(S)
        dens = np.exp(-t * t / (2 * vt)) / np.sqrt(2 * np.pi * vt)
        val = dens * e_plus(mu, np.maximum(sig, 1e-300), c)
        inner = np.sum(val * WS, axis=-1)
        total += wge * np.sum(Wgrid * inner)
    return 12 * p0 * total


A1 = {2: 25 * np.sqrt(3) / (48 * np.pi ** 2) / 10 / (2 * np.pi),
      3: 125 * np.sqrt(30) / (192 * np.pi ** 3) / 10 / (4 * np.pi)}

if __name__ == "__main__":
    d = int(sys.argv[1])
    ks = [float(x) for x in sys.argv[2:]]
    print("d=%d  a1 = (1/10) int F0 db per direction = %.13g" % (d, A1[d]))
    for k in ks:
        if d == 2:
            g1, g2 = G_d2(k), G_d2(k, ng=160, n=90)
        else:
            g1, g2 = G_d3(k), G_d3(k, nge=80, ngp=32, nrho=80, n=56)
        print("kappa=%-8g G=%.13g (refined %.13g, diff %.1e)  G/a1-1=%.6e  kappa*(G/a1-1)=%.6f"
              % (k, g1, g2, g2 - g1, g2 / A1[d] - 1, k * (g2 / A1[d] - 1)))
        sys.stdout.flush()
```

### t1_d2.txt

```text
d=2  a1 = (1/10) int F0 db per direction = 0.00145472125678
kappa=5        G=0.001454053684475 (refined 0.001454053684475, diff -1.1e-18)  G/a1-1=-4.589005e-04  kappa*(G/a1-1)=-0.002295
kappa=10       G=0.001454554202787 (refined 0.001454554202787, diff -4.3e-19)  G/a1-1=-1.148357e-04  kappa*(G/a1-1)=-0.001148
kappa=30       G=0.001454702689918 (refined 0.001454702689918, diff 1.5e-18)  G/a1-1=-1.276318e-05  kappa*(G/a1-1)=-0.000383
kappa=100      G=0.001454719585708 (refined 0.001454719585708, diff 2.6e-18)  G/a1-1=-1.148723e-06  kappa*(G/a1-1)=-0.000115
kappa=300      G=0.001454721071105 (refined 0.001454721071105, diff 2.6e-18)  G/a1-1=-1.276363e-07  kappa*(G/a1-1)=-0.000038
kappa=1000     G=0.001454721240069 (refined 0.001454721240069, diff 3.0e-18)  G/a1-1=-1.148727e-08  kappa*(G/a1-1)=-0.000011
kappa=10000    G=0.001454721256613 (refined 0.001454721256613, diff 2.8e-18)  G/a1-1=-1.148710e-10  kappa*(G/a1-1)=-0.000001
kappa=100000   G=0.001454721249799 (refined 0.001454721252212, diff 2.4e-12)  G/a1-1=-3.140325e-09  kappa*(G/a1-1)=-0.000314
```

### t1_d3_a.txt

```text
/tmp/claude-0/-home-claude/b41b316f-232c-5cf7-a0ee-80f0de603a6f/scratchpad/c3/referee/refB/t1_vec_check.py:105: RuntimeWarning: divide by zero encountered in divide
  step = np.where(d != 0, f1 / d, 0.0)
d=3  a1 = (1/10) int F0 db per direction = 0.0009151871835674
kappa=10       G=0.0009142088797984 (refined 0.0009142088772423, diff -2.6e-12)  G/a1-1=-1.068969e-03  kappa*(G/a1-1)=-0.010690
kappa=30       G=0.0009148895688792 (refined 0.0009148895687917, diff -8.8e-14)  G/a1-1=-3.251955e-04  kappa*(G/a1-1)=-0.009756
kappa=100      G=0.0009151008897126 (refined 0.0009151008897112, diff -1.4e-15)  G/a1-1=-9.429094e-05  kappa*(G/a1-1)=-0.009429
```

### t1_d3_b.txt

```text
d=3  a1 = (1/10) int F0 db per direction = 0.0009151871835674
kappa=300      G=0.0009151587037651 (refined 0.0009151587037651, diff -1.7e-17)  G/a1-1=-3.111910e-05  kappa*(G/a1-1)=-0.009336
kappa=1000     G=0.0009151786695326 (refined 0.0009151786695326, diff -1.1e-18)  G/a1-1=-9.303053e-06  kappa*(G/a1-1)=-0.009303
kappa=3000     G=0.000915184348404 (refined 0.000915184348404, diff -8.7e-19)  G/a1-1=-3.097906e-06  kappa*(G/a1-1)=-0.009294
kappa=10000    G=0.0009151863333175 (refined 0.0009151863333175, diff -1.5e-18)  G/a1-1=-9.290449e-07  kappa*(G/a1-1)=-0.009290
```

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_