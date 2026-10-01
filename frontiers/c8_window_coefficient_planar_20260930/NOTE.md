# The compact-window coefficient `c_{B,K}` in the plane: exact factorization, closed forms and certified values on the C8 band

**Object:** `CL-C8-WINDOW-COEFFICIENT-PLANAR-20260930-v1`. **Author lane:** Anthropic / Claude (Claude Code
`session_017Mi3hxjaxV45x6zo6o1ee3`). **Kind:** certified numerical constant with its exact reduction: interval arithmetic over
`decimal` (60 digits, directed rounding), fractional powers by exact integer roots, every series with an explicit remainder
or a bracket by consecutive partial sums. **Scientific effect:** NONE. No register, catalog, GRAPH or STATUS change; catalog
entry C8 (`reviews/candidates_pending_20260928/CANDIDATES.md`) stays OPEN: this note supplies a second of its listed
constants, `c_{B,K}`, in `d = 2`, on the band declared by Math-#195 and on a few other windows, and none of `C`, `r_*`,
`c_{d,L}` (Math-#195 supplies `z_*`). Scope claimed on Math-#195 (comment 5915784573).

## 0. Statement

Let `f` be the unit-variance stationary Gaussian field on the torus `R^2 / (L Z^2)` with the parent kernel
`K_L(z) = sum_n exp(-|z + Ln|^2/2) / sum_n exp(-|Ln|^2/2)` ([LP] section 1), `B = [b_-, b_+]` a birth window and
`K = [k_-, k_+]` a gap window, `0 < k_-`. [LP] Theorem B gives `nu_cand(ell) ~ c_{B,K} ell^(-1/3)` and
`nu_eld(ell) ~ c_{B,K} ell^(-1/3)` for the pairs with birth in `B` and scaled gap in `K`, with `c_{B,K}` the Gaussian integral
(11.3). Everything below is about that integral; the theorem is consumed at its stated scope and not revalidated.

**Theorem W (exact factorization, reference kernel).** For the Euclidean kernel `exp(-|z|^2/2)` in `d = 2`,

    c_{B,K} = c_{2,ref} F_B G_K,          c_{2,ref} = 2 Gamma(7/6) (3/2)^(1/3) / (3 sqrt3 pi^(3/2)),

    G_K = P(7/6, 12 k_+^2) - P(7/6, 12 k_-^2)                      (P the regularized lower incomplete gamma function),

    F_B = Psi(b_+ sqrt(3/2)) - Psi(b_- sqrt(3/2)),
    Psi(x) = Phi(x) - 2 T(x, 1/sqrt3) - (1/2) x phi(x) Phi(x/sqrt3) - (sqrt3 / (4 pi)) exp(-2x^2/3),

`T` Owen's T-function, `Psi(-inf) = 0`, `Psi(+inf) = 1`. In particular

    F_{[-beta, beta]} = erf(beta sqrt3/2) - beta sqrt3 exp(-3 beta^2/4) / (4 sqrt pi),      F_{[0, inf)} = 2/3 + sqrt3/(4 pi),

and the gap-mark density is `k^(4/3) exp(-12 k^2)`, normalized, with mode `k = sqrt2/6`.

**Certified values.** `c_{2,ref} = 0.07340691930603427103013596295777405001766424468433...` (enclosure width below `1e-55`;
it lies inside SIDE24's `[0.07340691930603427103, 0.07340691930603427104]` for `c_{2,24}`, rule SIDE24_CONSISTENT), and on
the C8 band of Math-#195, `B = [0, 1]`, `K = [1/2, 2]`:

    F_B = 0.48264345641927413020434204645556992729...,   G_K = 0.06737173342564166734884441847440277343...,
    c_{B,K} (reference)  = 0.0023869380211529483091019117...,             c_{B,K} / c_{2,ref} = 0.0325165262...,
    c_{B,K} (torus, every L >= 10, every frame) in [0.00238693802093000833, 0.00238693802137588829],
    c_{B,K} (torus, L = 24) = 0.0023869380211529483091019117...  (agrees with the reference to the printed digits).

So the C8 band carries `48.26 %` of the birth mass and `6.74 %` of the gap mass of the leading coefficient, `3.25 %` in all.
Section 6 tabulates five windows and the two factors separately; section 4 gives the `d = 3` reference closed form.

## 1. The object

Write, in an orthonormal frame `(u, w)`, `G = grad f`, `V = (f_uu, f_uw)`, `A = f_ww`, `t = f_uuu`. [LP] (11.3) with the
section 15 factorization `pi_0 = p_{(f,V)}(b, 0) p_G(0) phi_tau(12k)`, `z_0 = 36 k^2 E[A^2 1{A<0} | f = b, V = 0]`,
`tau^2 = Var(t | G = 0)`, reads

    c_{B,K} = 144 int_{S^1} p_G(0) p_V(0) I_B(u) J_K(u) dsigma(u),
    I_B(u) = int_B p_{f|V=0}(b) E[A^2 1{A<0} | f = b, V = 0] db,        J_K(u) = int_K k^(4/3) phi_tau(12 k) dk,          (1.1)

where `p_{(f,V)}(b, 0) = p_V(0) p_{f|V=0}(b)` is the ordinary disintegration of a centred Gaussian vector. Odd and even
derivatives are independent for any even kernel, so `(G, t)` is independent of `(f, V, A)` and (1.1) is exactly [LP]'s
integral restricted to `B x K`; with `B = R`, `K = (0, inf)` it is `c_{2,L}` of (15.2). Section 15 evaluates the full gap
integral (`144 int_0^inf k^(4/3) phi_tau(12k) dk = Gamma(7/6) tau^(4/3) / (24^(1/3) sqrt pi)`) and the full birth integral
(`p_V(0) D_u`); the window keeps both integrals finite and this note evaluates them.

## 2. Reference kernel: conditional laws and closed forms

**Covariances.** For `K(z) = exp(-|z|^2/2)`, `Cov(d^a f, d^b f) = (-1)^|a| d^(a+b) K(0)`, and the even derivatives of the
Gaussian at zero are `(-1)^n (2n-1)!!` per axis: `Var f = 1`, `Cov(G) = I`, `Var t = 15`, `Cov(t, f_u) = -3`,
`Cov(f, f_uu) = Cov(f, f_ww) = -1`, `Var f_uu = Var f_ww = 3`, `Cov(f_uu, f_ww) = 1`, `Var f_uw = 1`, all other entries of
the 3-jet zero (SIDE24 section 1). Hence `p_G(0) = 1/(2 pi)`, `tau^2 = 15 - 9 = 6`, `Cov(V) = diag(3, 1)`,
`p_V(0) = 1/(2 pi sqrt3)`.

**Conditioning on `V = 0`.** `(f, A)` given `V = 0` is centred with covariance
`[[1, -1], [-1, 3]] - [[-1, 0], [1, 0]] diag(1/3, 1) [[-1, 1], [0, 0]] = [[2/3, -2/3], [-2/3, 8/3]]`: `f | V = 0 ~ N(0, 2/3)`
and `A | V = 0 ~ N(0, 8/3)` (SIDE24's `A = Q + sqrt(2/3) Z`, `Q ~ N(0, 2)`). **Conditioning further on `f = b`:**
`A | f = b, V = 0 ~ N(alpha b, s^2)` with `alpha = (-2/3)/(2/3) = -1`, `s^2 = 8/3 - (2/3)^2/(2/3) = 2`. This is the
contact law `A_0 ~ N(-b, 2)` of [LP] (5.4) as quoted in Math-#195 section 1; `E[A^2 1{A<0} | V = 0] = (8/3)/2 = 4/3 = D_1`.

**The birth integrand.** With `X` standard normal and `t = b/sqrt2`,
`E[A^2 1{A<0} | f = b, V = 0] = 2 E[(X - t)^2 1{X < t}] = 2[(1 + t^2) Phi(t) + t phi(t)]`, i.e.
`m_{2,b} = (b^2 + 2) Phi(b/sqrt2) + sqrt2 b phi(b/sqrt2)` (Math-#178 section 1 in the same words). Substituting
`b = sigma x`, `sigma = sqrt(2/3)`, and `Phi(b/sqrt2) = Phi(x/sqrt3)`:

    I_B = 2 int_{x_-}^{x_+} phi(x) [ (1 + x^2/3) Phi(x/sqrt3) + (x/sqrt3) phi(x/sqrt3) ] dx,      x_+- = b_+- sqrt(3/2).      (2.1)

**Three Gaussian primitives.** For `0 < a <= 1`, `rho^2 = 1 + a^2`, with `T` Owen's function
`T(h, a) = (1/2 pi) int_0^a exp(-h^2 (1+x^2)/2) / (1+x^2) dx` (so that `int_{-inf}^h phi(x) Phi(ax) dx = Phi(h)/2 - T(h, a)`,
Owen 1956; `T(0, a) = arctan(a)/(2 pi)`, `T(+-inf, a) = 0`, `T` even in `h`):

    G_0(x) := int_{-inf}^x phi Phi(a .) = Phi(x)/2 - T(x, a),
    G_1(x) := int_{-inf}^x t phi Phi(a t) dt = -phi(x) Phi(ax) + (a / (rho sqrt(2 pi))) Phi(rho x),
    G_2(x) := int_{-inf}^x t^2 phi Phi(a t) dt = G_0(x) - x phi(x) Phi(ax) - (a / (2 pi rho^2)) exp(-rho^2 x^2/2),
    G_3(x) = -x^2 phi(x) Phi(ax) + (a/2 pi) [ -(x/rho^2) exp(-rho^2 x^2/2) + (sqrt(2 pi)/rho^3) Phi(rho x) ] + 2 G_1(x),
    G_4(x) = -x^3 phi(x) Phi(ax) - (a/2 pi) (x^2/rho^2 + 2/rho^4) exp(-rho^2 x^2/2) + 3 G_2(x),

by `t^n phi = -(t^(n-1) phi)' + (n-1) t^(n-2) phi`, integration by parts and `phi(t) phi(at) = exp(-rho^2 t^2/2)/(2 pi)`;
the limits at `+inf` are `1/2, a/(rho sqrt(2 pi)), 1/2, a/(rho^3 sqrt(2 pi)) + 2a/(rho sqrt(2 pi)), 3/2` (Stein's identity
checks `G_3(inf)`). Since `int a x phi(x) phi(ax) dx = -(a / (2 pi rho^2)) exp(-rho^2 x^2/2)`, (2.1) gives, with `a = 1/sqrt3`,
`rho^2 = 4/3`,

    I_B = 2 [ Psi_a(x_+) - Psi_a(x_-) ],     Psi_a(x) = G_0(x) + a^2 G_2(x) - (a / (2 pi rho^2)) exp(-rho^2 x^2/2),
    Psi_a(x) = rho^2 [Phi(x)/2 - T(x, a)] - a^2 x phi(x) Phi(ax) - (a/2 pi) exp(-rho^2 x^2/2),

and `F_B := I_B / D_1 = (3/2) [Psi_a(x_+) - Psi_a(x_-)]` is the `Psi` of Theorem W:
`(3/2)(4/3)[Phi/2 - T] = Phi - 2T`, `(3/2)(1/3) x phi Phi = x phi Phi/2`, `(3/2)(1/(2 pi sqrt3)) = sqrt3/(4 pi)`.
`Psi(+inf) - Psi(-inf) = 1` recovers `D_1 = 4/3` (rule D1_EXACT). For a symmetric window the `T` terms cancel (`T` is
even), `Phi(y) + Phi(-y) = 1` collapses the `x phi Phi` terms to `-(1/2) beta' phi(beta')`, `beta' = beta sqrt(3/2)`, and the
exponential terms cancel: `F_{[-beta,beta]} = erf(beta sqrt3/2) - beta sqrt3 exp(-3 beta^2/4)/(4 sqrt pi)` (rule
SYMMETRIC_CLOSED_FORM). At `x = 0`, `T(0, 1/sqrt3) = (pi/6)/(2 pi) = 1/12`, so `Psi(0) = 1/3 - sqrt3/(4 pi)` and
`F_{[0, inf)} = 2/3 + sqrt3/(4 pi) = 0.80449889...` (rule HALF_LINE_EXACT): births above the mean carry four fifths of the
coefficient, because `m_{2,b}` increases in `b`.

**The gap integral.** With `s = 72 k^2/tau^2` (`= 12 k^2` at `tau^2 = 6`),

    J_K = tau^(4/3) 72^(-7/6) [ gamma(7/6, s_+) - gamma(7/6, s_-) ] / (2 sqrt(2 pi)),                              (2.2)

`gamma` the lower incomplete gamma function; `144 J_(0,inf) = Gamma(7/6) tau^(4/3)/(24^(1/3) sqrt pi)` is [LP]'s
evaluation, and `G_K := J_K / J_(0,inf) = P(7/6, s_+) - P(7/6, s_-)`. The gap density `k^(4/3) exp(-12 k^2)` has its mode
at `24 k^2 = 4/3`, `k = sqrt2/6 = 0.2357`, and `P(7/6, 3) = 0.9326...`: at a fixed lifetime, `93 %` of the leading
coefficient comes from scaled gaps `k < 1/2`, that is from pairs at radius `r = (ell/k)^(1/3) > (2 ell)^(1/3)`.

**Assembly.** `144 . 2 pi . (1/2 pi) (1/(2 pi sqrt3)) . (4/3) F_B . 6^(2/3) 72^(-7/6) Gamma(7/6) G_K / (2 sqrt(2 pi))`
`= [2 Gamma(7/6) (3/2)^(1/3) / (3 sqrt3 pi^(3/2))] F_B G_K`, using `144 . 72^(-7/6) 6^(2/3) / (2 sqrt(2 pi)) = 6^(2/3) / (24^(1/3) sqrt pi)`
and `6^(2/3)/24^(1/3) = (3/2)^(1/3)`; the bracket is SIDE24 (1) at `d = 2`, `D_1 = 4/3`. The script evaluates both sides
independently (the closed form of Theorem W, and the pipeline (1.1) from the covariance entries) and requires them to
intersect on every window (rule FACTORIZATION_AND_TRANSFER).

## 3. Torus kernel: one enclosure for every `L >= 10` and every frame

**Image bound.** For a unit-direction contraction of order `q <= 6` of `phi(x) = exp(-|x|^2/2)`, the product rule gives
`|D^q phi(x)| <= phi(x) sum_j q! |x|^(q-2j) / (2^j j! (q-2j)!) <= 76 |x|^6 phi(x)` for `|x| >= 1` (`1 + 15 + 45 + 15 = 76`
at `q = 6` dominates the lower orders) and `|D^q phi(0)| <= 15` (SIDE24 section 2). In `d = 2` the shell `|n|_inf = j`
holds `8 j` lattice points with `j^2 <= |n|^2 <= 2 j^2`, so `sum_{n != 0} |n|^6 exp(-L^2 |n|^2/2) <= 64 sum_j j^7 exp(-L^2 j^2/2)
<= 128 exp(-L^2/2)`, successive shell terms having ratio at most `2^7 exp(-3L^2/2) < 1/2` for `L >= 10`. Writing
`K_L = [phi + sum_{n != 0} phi(. + Ln)] / S`, `S = 1 + sum_{n != 0} exp(-L^2|n|^2/2) >= 1`, every unit-direction contraction
satisfies

    |D^q K_L(0) - D^q phi(0)| <= E_L := 128 (76 L^6 + 15) exp(-L^2/2),      E_10 ≈ 1.876e-12,   E_24 ≈ 1.558e-113.      (3.1)

`E_L` decreases in `L`, so the box "each entry within `E_10` of its reference value" contains the 3-jet covariance of `K_L`
for every `L >= 10` and every frame `(u, w)` (the entries `Cov(d^a f, d^b f) = (-1)^|a| d^(a+b) K_L(0)` are exactly such
contractions; `Var f = 1` is exact by the normalization).

**Interval evaluation.** The class `Planar(E)` in the script takes the fifteen entries as intervals `[v - E, v + E]`,
forms `p_G(0) = (2 pi)^-1 det(Cov G)^(-1/2)`, `tau^2 = Var t - c^T Cov(G)^-1 c`, `p_V(0)`, the Schur complement of `V` in
`(f, A)`, `alpha`, `s^2`, `sigma^2 = Var(f | V = 0)`, then `I_B` through the primitives of section 2 with the interval slope
`a = -alpha sigma / s` (Owen's series and `arctan` take interval arguments) and `J_K` through (2.2) with the interval
`tau^2`. Every quantity is a function of `u` through the entries only, so the interval computed for one box bounds the
integrand for every `u`; with `|S^1| = 2 pi` this encloses `c_{B,K}` of (1.1) for every `L >= 10` (`E = E_10`) and, more
sharply, for `L = 24` (`E = E_24`). At `E = 0` the same code reproduces the reference (rule FACTORIZATION_AND_TRANSFER:
the `L >= 10` enclosure contains the reference one and is at least ten times wider; the `L = 24` enclosure intersects it).
The `L >= 10` relative half-width is `2.7e-11` (about fourteen times `E_10`, the condition of the conditional-covariance
formulas); the `L = 24` enclosure is arithmetic-limited (`1e-55`).

**Relation to the SIDE24 records.** On the full window the `L = 24` enclosure lies inside SIDE24's interval for `c_{2,24}`
(rule SIDE24_CONSISTENT); SIDE24 (4) bounds `|c_{2,24}/c_{2,ref} - 1| < 1e-106` and the remainder record's Theorem R
(candidate) identifies the correction as `P_2(24) e^-288 = -6.5e-119`; the transfer here (`E_24 = 1.6e-113` per entry) is
consistent with both and weaker than the second. Its point is the window: it applies to `c_{B,K}`, where the scaling
argument of SIDE24 section 4 does not (the birth window breaks the homogeneity of the cone moment).

## 4. The `d = 3` reference expression

For the Euclidean kernel in `d = 3`, `A | f = b, V = 0 = -b I + Q` with `Q` the `2 x 2` matrix of SIDE24 section 1
(independent diagonal entries of variance `2`, off-diagonal of variance `1`; same computation as section 2, the
conditioning on `f = b` removing exactly the shared `sqrt(2/3) Z` shift). Write `Q = [[s + x, y], [y, s - x]]`,
`s, x, y ~ N(0, 1)` independent, `R^2 = x^2 + y^2 ~ Exp(1/2)`: `det A = (s - b)^2 - R^2`, and `A < 0` iff `s - b < -R`.
SIDE24's Rayleigh integral `int_0^w (w - z)^2 e^(-z/2) dz/2 = w^2 - 4w + 8 - 8 e^(-w/2) =: g(w)` gives
`m_{3,b} := E[det(A)^2 1{A<0}] = int_{-inf}^b g((s-b)^2) phi(s) ds = int_0^inf g(v^2) phi(v - b) dv`, and with the
truncated moments `int_0^inf v^n phi(v - b) dv` (`n <= 4`) and `int_0^inf exp(-v^2/2) phi(v - b) dv = exp(-b^2/4) Phi(b/sqrt2)/sqrt2`,

    m_{3,b} = (b^3 + b) phi(b) + (b^4 + 2 b^2 + 7) Phi(b) - 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2).                       (4.1)

Its mean over `b ~ N(0, 2/3)` is `(1/2)(3 . 4/9 + 2 . 2/3 + 7) - 2 sqrt2 (1 + 1/3)^(-1/2) = 29/6 - sqrt6 = D_2`, SIDE24's
cone moment, so the window factor `F^(3)_B = int_B phi_{2/3}(b) m_{3,b} db / D_2` integrates to one (rule D2_EXACT; the
script also checks (4.1) against the direct double integral in floating point). The three pieces of `int_B phi_{2/3} m_{3,b}`
are elementary through the primitives of section 2: `int phi_{2/3}(b) (b^3 + b) phi(b) db = -(2 b^2/5 + 18/25) exp(-5 b^2/4) / (2 pi sigma)`;
`int phi_{2/3}(b) (b^4 + 2 b^2 + 7) Phi(b) db = sigma^4 G_4 + 2 sigma^2 G_2 + 7 G_0` at `x = b/sigma` with slope `a = sigma`;
`int phi_{2/3}(b) 4 sqrt2 exp(-b^2/4) Phi(b/sqrt2) db = (4/sigma) G_0(sqrt2 b; 1/2)`. The gap factor is the same `G_K`
(`tau^2 = 6` in every dimension for the reference kernel), and `c^(3)_{B,K} = c_{3,ref} F^(3)_B G_K` with `c_{3,ref}` SIDE24
(1) at `d = 3`. **No torus transfer is made in `d = 3`:** under the perturbed entries the conditional mean of `A` is no
longer a multiple of the identity and the truncated cone moment has no closed form; a Lipschitz bound in the mean and the
density sandwich of SIDE24 section 4 would give one and are left for a later record.

## 5. Exhaustion: what a window leaves out

`1 - G_K = P(7/6, 12 k_-^2) + Q(7/6, 12 k_+^2)`, `Q = 1 - P`, with the elementary two-sided bounds (`s > 0`)

    e^-s s^(7/6) / Gamma(13/6) <= P(7/6, s) <= s^(7/6) / Gamma(13/6),
    s^(1/6) e^-s / Gamma(7/6) <= Q(7/6, s) <= s^(1/6) e^-s / (Gamma(7/6) (1 - 1/(6s))),

from `e^-s <= e^-t <= 1` on `[0, s]` and `t^(1/6) <= s^(1/6) exp((t - s)/(6s))` on `[s, inf)`. So the small-gap cut costs
`12^(7/6) k_-^(7/3) / Gamma(13/6) (1 + O(k_-^2))`, the large-gap cut `(12 k_+^2)^(1/6) e^(-12 k_+^2)/Gamma(7/6)`.
For the birth window, `m_{2,b} <= b^2 + 2` for every `b` (Mills' ratio for `b > 0`) and `(Q - b)^2 <= Q^2` on `{Q < b <= 0}`
give

    1 - Psi(x) <= 2 Phi_bar(x) + x phi(x)/2   (x > 0),          Psi(x) <= (3/2) Phi(x)   (x <= 0),      x = b sqrt(3/2),

Gaussian rates `exp(-3 b^2/4)` on both sides; the symmetric closed form gives the exact loss
`erfc(beta sqrt3/2) + beta sqrt3 exp(-3 beta^2/4)/(4 sqrt pi)`. Rule EXHAUSTION_BOUNDS checks the certified values against
each bound with margin. These are the rates at which `c_{B,K}` increases to `c_{2,L}` along exhausting windows ([LP]
section 13).

## 6. Values (`RESULTS.json`)

Birth factor `F_B` (`d = 2`) and `F^(3)_B` (`d = 3`, reference), gap factor `G_K` (both dimensions):

| `B` | `F_B` (`d = 2`) | `F^(3)_B` (`d = 3`, ref.) | `K` | `G_K` |
|---|---|---|---|---|
| `[0, 1]` (C8 band) | `0.482643456419274130...` | `0.346198792034071727...` | `[1/2, 2]` (C8 band) | `0.067371733425641667...` |
| `[-1/2, 1/2]` | `0.358442197996678535...` | `0.156521520040231396...` | `[1, 3/2]` | `0.0000101517691908456...` |
| `[-1, 1]` | `0.663928895976061762...` | `0.391483956900814659...` | `[1/4, 4]` | `0.549058584986557263...` |
| `[-2, 2]` | `0.961368034899749630...` | `0.866952146414130272...` | `[1/10, 10]` | `0.926964889761576745...` |
| `[-3, 3]` | `0.998903294460189530...` | `0.993299304898946068...` | `[1/2, inf)` | `0.067371733425641667...` |
| `[0, inf)` | `0.804498890522114679...` | `0.953797733717050929...` | `[1, inf)` | `0.0000101517727209572...` |
| `(-inf, 0]` | `0.195501109477885320...` | `0.046202266282949070...` | `(0, inf)` | `1` |

All enclosure widths are below `1e-50`. Coefficients (reference closed form; torus `L >= 10` enclosure; `d = 3` reference):

| window | `c_{B,K}` reference (`d = 2`) | fraction of `c_{2,ref}` | torus `L >= 10`, every frame | `c^(3)_{B,K}` reference |
|---|---|---|---|---|
| W1 `B=[0,1] K=[1/2,2]` | `0.00238693802115294830910...` | `0.0325165` | `[0.00238693802093000833, 0.00238693802137588829]` | `0.000974382366024250...` |
| W2 `B=[-1,1] K=[1/2,2]` | `0.00328349448038652830503...` | `0.0447300` | `[0.00328349448011528868, 0.00328349448065776793]` | `0.00110183822983417...` |
| W3 `B=[-2,2] K=[1/4,4]` | `0.03874764950788533309909...` | `0.5278474` | `[0.03874764950590828641, 0.03874764950986237979]` | `0.0198856576593802...` |
| W4 `B=[-3,3] K=[1/10,10]` | `0.06797101083534825121205...` | `0.9259483` | `[0.06797101083232680835, 0.06797101083836969407]` | `0.0384653388278856...` |
| W5 `B=[-1/2,1/2] K=[1,3/2]` | `2.6711474686063351637e-7` | `3.63882e-6` | `[2.67114746807e-7, 2.67114746914e-7]` | `6.6380716823e-8` |
| full | `0.07340691930603427103013...` | `1` | `[0.07340691930405245284, 0.07340691930801608922]` | `0.0417759318405983433...` |

The `L = 24` enclosures agree with the reference column to every printed digit (`RESULTS.json`, `c_torus_L_24`); the `d = 3`
fractions are `0.0233`, `0.0264`, `0.4760`, `0.9208`, `1.59e-6`, `1`. `Gamma(7/6) = 0.92771933363003920070834948253462...`,
`c_{3,ref} = 0.04177593184059834334293666542857...` (SIDE24's `d = 3` interval contains it).

## 7. Rules, mutants, verification

`python3 -B -S window_coefficient.py` (also `-B -O -S`; eleven seconds) prints `RESULTS.json` and exits `0` only if all
fourteen rules hold: FLOAT_INSIDE (independent floating quadratures of the birth and gap factors, `m_{3,b}` by the direct
double integral, Owen's `T` by its defining integral, `math.gamma(7/6)`, all within `1e-9` of the enclosures); WIDTHS
(`1e-40` for the reference, `d = 3` and `L = 24` enclosures, `1e-10` for `L >= 10`); D1_EXACT (`4/3`, and both factors
equal to one on the full window); D2_EXACT (`29/6 - sqrt6`); HALF_LINE_EXACT (`2/3 + sqrt3/(4 pi)`);
SYMMETRIC_CLOSED_FORM; FACTORIZATION_AND_TRANSFER (closed form against pipeline on every window, `L >= 10` contains
the reference and is wider, `L = 24` intersects it); SIDE24_CONSISTENT; IMAGE_BOUND (`E_10 in (1.8e-12, 1.95e-12)`,
`0 < E_24 < 1e-112`); MONOTONE (nested windows, positive half-lines); EXHAUSTION_BOUNDS; TRUNCATION_NESTING (Owen's
series with half the terms, `erf` and `gamma(7/6, .)` stopped at the first admissible tail bound, `Gamma(7/6)` split at
`X = 90` instead of `120`: every coarse enclosure intersects the fine one and is wider); LIBRARY_EXACT (the decimal
module's `exp` and `sqrt`, and the interval negation, against exact rational brackets at six arguments: `e^-q` as
`(e^(-q/64))^64` from the rational series, `sqrt q` from an integer root); PINNED (fifty leading digits of `pi`,
`Gamma(7/6)`, `c_{2,ref}`, `F_{[0,1]}`, `G_{[1/2,2]}`). Mutants (`--mutant`, each must exit `1`): `no-owen` (`T := 0`),
`mean-sign` (`alpha -> -alpha` in the pipeline), `slope` (`a` scaled by `11/10`), `gamma-shape` (`P(4/3, .)` for the window),
`image-dropped` (`E_L := 0`), `shell-count` (`64` for `128`), `tail-dropped` (series stopped early with no tail),
`prefactor` (`72` for `144`), `d3-cross` (the `exp(-b^2/4) Phi(b/sqrt2)` term halved), `window-swap` (endpoints
exchanged). The workflow `c8-window-coefficient-planar.yml` replays the manifest, the three main-resident pins, checks that
the SIDE24 interval quoted in the script is the one in `ENCLOSURE.json`, runs both interpreter modes byte for byte against
`RESULTS.json` and the ten mutants in each, on a clean tree. Timing goes to `stderr`; the floating controls enter the pinned
output rounded to ten significant digits.

Rule LIBRARY_EXACT exists because this packet's first draft negated interval endpoints with the Decimal unary minus, which
rounds to the thread's default 28-digit context; `exp(-x)` at a 60-digit `x` was then wrong beyond the 28th digit while every
other rule passed. Negation is now the exact `copy_negate`, every arithmetic step names its context, and the rule detects
the old behaviour at `1e-28`. The interval class is the one of Math-#190, where the operation is never applied to a long
endpoint (its outputs are byte-identical under the repaired class); Math-#190 v1.3 carries the same repair, rule and a
mutant reinstating the old negation.

## 8. What this does not do

Not a proof or review of [LP] Theorem B or C: the identity of (1.1) with the leading coefficient of the compact-window
lifetime density is [LP]'s, consumed at its scope, and its D1 dependencies (Math-#194, Math-#196) are untouched. Not a value
of `C`, `r_*`, `c_{d,L}` for `d >= 3`, or of any finite-radius quantity; not an enclosure of the torus coefficient in
`d = 3`; nothing about `p_r`, the elder selection or the boundary layer. The windows are declared, not optimized. No
register, catalog, GRAPH or STATUS change; C8 stays OPEN. Same GitHub account as every lane; zero
organizational-independence credit. Claude reads of this packet count for nothing; the author will not merge.

## 9. Provenance

Pins on `main 3e0a91b` ([LP] `dfed3b8d`, SIDE24 `PROOF.md` `44b66f04`, `ENCLOSURE.json` `57af39a0`) verified by the
workflow; read, not pinned: the SIDE24 remainder record (`0bcf0a6f`) and the C8 catalog entry (`02455f05`); unmerged
companion Math-#195 at `16da75f` (`NOTE.md` `a8b1f71d`) for the band and the quoted (5.4). `SOURCE_FILES.json` fingerprints
the packet. Owen's series for `T(h, a)`, `T = (1/2 pi)[arctan a - sum_j (-1)^j a^(2j+1)/(2j+1) . P(Poisson(h^2/2) > j)]`
(Owen 1956, equation 2.3), is used with the bracket by consecutive partial sums (the terms alternate and decrease for each
fixed `(h, a)`, `a <= 1`). No external numerical library is used.

## 10. Revisions

- **v1.1 (reporting only; the pattern of finding C41-205-C-01 on Math-#205, found here by the author's containment audit).** The upper
  endpoints of the `L >= 10` torus intervals in section 0 and in the section 6 coefficient table had been truncated instead of
  rounded up. The displayed intervals therefore did not contain the certified intervals of `RESULTS.json`.
  - Every displayed interval is now rounded outward: lower endpoints down, upper endpoints up, at the displayed precision.
  - An exact containment audit against `RESULTS.json` passes for every bracketed interval in this note, and every `...`-terminated
    digit string is a common prefix of a certified interval's endpoints.
  - The image-bound values of section 3 are stated as approximations.

  `window_coefficient.py` (blob `43b4f51b`, pinned by Math-#205 and reviewed by C41 in review 5373681556), `RESULTS.json`, every
  certified value, the rules and the mutants are unchanged.
