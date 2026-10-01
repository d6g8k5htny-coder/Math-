# C8: the radial ledger on the torus with a vanishing remainder (Theorem L′)

**Object:** CL-C8-TORUS-VANISHING-REMAINDER-20261001-v1.
**Author:** Anthropic Claude (Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`), 1 October 2026.
**Disposition:** author-side theorem with certified constants; no review yet. It extends Math-#215 (Theorem L) and closes
the item that #215 lists as not given ("a vanishing-remainder rate"), which Math-#193 (comment 5932553031) records among the
open C8 items as "a vanishing torus remainder".
**Scientific effect:** NONE. No `STATUS`, `PROOF_INDEX`, `GRAPH`, claim, catalog, prize or source-body change. Same GitHub
account as every lane; zero organizational-independence credit. Nothing in Math-#215, #206 or #212 is touched.
**Delivered under:** Dylan Roy's explicit instructions in this session, given after the 2026-09-27 owner stop (quoted in
`SOURCE_MAP.json`, `delivered_under`). `OWNER_STOP.md` addresses Cursor agents and automations and is untouched.

## 0. Statement

Notation as in Math-#215 ([B]) and [LP]: `A_r(b, k, u) = 12 pi_r(R; v_r) Z_r / r^2` is the radial ledger of [LP] (10.2) for
the field with kernel `K`, the band is `B x K = [0, 1] x [1/2, 2]`, and `A_0 = lim_{r -> 0} A_r` is the contact integrand
**of the same kernel**. For the Gaussian kernel `A_0 = A_0^ref` (closed form, [B] §1); for the torus kernel `K_L` it is
its own `A_0^(L)`, which [B] only locates within `eps_d` of `A_0^ref`.

**Theorem L′.** For `d = 2, 3`, every torus side `L >= 10`, every frame, every `b in B`, `k in K`, every `R` in the
table and every `0 < r <= R`,

    -(a_dn(R) r^2 + beta_dn r)  <=  A_r(b, k, u) / A_0(b, k, u) - 1  <=  a_up(R) r^2 + beta_up r.

The constants are exact rationals in `RESULTS.json` (key `rate_torus`), shown rounded up:

| `R` | `a_up`, `d = 2` | `a_dn`, `d = 2` | `a_up`, `d = 3` | `a_dn`, `d = 3` |
|---|---|---|---|---|
| `1/4096` | `13.822900` | `3.637234` | `25.666574` | `25.516405` |
| `1/2048` | `13.825546` | `3.643346` | `26.256538` | `26.108063` |
| `1/1024` | `13.830904` | `3.655573` | `27.446809` | `27.301701` |
| `1/512` | `13.841883` | `3.680046` | `29.869058` | `29.730582` |
| `1/256` | `13.864900` | `3.729062` | `34.883096` | `34.757367` |
| `1/128` | `13.915213` | `3.827402` | `45.611669` | `45.508415` |
| `1/64` | `14.033374` | `4.025510` | `70.060722` | `69.981331` |

with first-order coefficients

    beta_2 <= 1.036 x 10^-9,        beta_3 <= 1.914 x 10^-7        (every R in the table).

**For the Gaussian kernel the first-order coefficients vanish identically** (`rate_reference_kernel`: `beta = 0` exactly),
and the `a` columns are the same: `|A_r / A_0^ref - 1| <= a(R) r^2`, with no additive remainder.

What changes against [B]:
- **The remainder vanishes.** [B] proves `|A_r / A_0^ref - 1| <= a r^2 + eps_d`, with `eps_2 <= 3.96 x 10^-10` and
  `eps_3 <= 1.79 x 10^-8` independent of `r`. Theorem L′ compares `A_r` with the limit of the same kernel, and every
  remainder carries a factor `r` or `r^2`. In particular `A_r^(L) = A_0^(L) (1 + O(r))` on the torus with explicit
  constants, and `A_r = A_0^ref (1 + O(r^2))` for the Gaussian kernel with no remainder at all.
- **The second-order coefficients are [B]'s.**
  - `a(R)` is never below [B]'s Theorem L value.
  - It equals [B]'s to the displayed digits for `R <= 1/2048`.
  - It exceeds [B]'s by at most `1.1 x 10^-5` for `R <= 1/512` and by at most `7.4 x 10^-4` at `R = 1/64`. The excess comes
    from the cross terms and the `r^9` remainders, §§2, 5.
- **The first-order coefficient is a torus artefact.** `beta` is a bound on the torus part of the `r^1` coefficients
  (§2, Lemma V2). It is not sharp: the actual torus corrections are of order `e^-50`, while `beta` comes from Cauchy
  estimates at `M_1(10) < 4.46 x 10^-15`.

**Corollary L′1 (the densities with a vanishing remainder).** Let `nu_cand`, `nu_eld` be the compact-window densities of [LP]
Theorem B in the versions (11.2), for the torus kernel or the Gaussian kernel, and
`c_{B,K} = int_{B x K x S^(d-1)} A_0(b, k, u)/(3 k^(2/3)) db dk dsigma(u)` the leading constant **of the same kernel**. The
angular integral uses ordinary surface measure `dsigma`, as in [LP] (11.2)–(11.3). The torus is not assumed isotropic. For `0 < ell < R^3 / 2`:

    -(c2_dn ell^(2/3) + c1_dn ell^(1/3))  <=  ell^(1/3) nu_cand(ell) - c_{B,K}  <=  c2_up ell^(2/3) + c1_up ell^(1/3),
    ell^(1/3) nu_cand(ell) - C_{B,K}(R) ell  <=  ell^(1/3) nu_eld(ell)  <=  ell^(1/3) nu_cand(ell),

with `C_{B,K}(R)` of [B] Corollary L1, and (`corollary_torus`; ratios to `c_{B,K}`, rounded up):

| `R` | `c2_up/c`, `d = 2` | `c2_dn/c`, `d = 2` | `c2_up/c`, `d = 3` | `c2_dn/c`, `d = 3` |
|---|---|---|---|---|
| `1/4096` | `6.282558` | `4.464593` | `23.153357` | `22.427357` |
| `1/512` | `6.322008` | `4.505526` | `27.377121` | `26.661848` |
| `1/64` | `6.643378` | `4.836304` | `67.060479` | `66.396981` |

and `c1/c <= 1.531 x 10^-10` (`d = 2`), `<= 3.985 x 10^-8` (`d = 3`). For the Gaussian kernel `c1 = 0`
(`corollary_reference_kernel`).

So, on the torus, both densities are `c_{B,K} ell^(-1/3) + O(1) + O(ell^(1/3))` about the **torus** constant, with explicit
constants and a vanishing remainder. [B] gave the same expansion only about `c^ref_{B,K}`, up to `eps'_d ell^(-1/3)`.

## 1. Where [B]'s remainder came from

[B]'s `eps_d` collects five things, each `r`-independent:
1. the Taylor-model remainder `e` (rounding, truncated powers `r^j`, `j > 8`, the covariance tail beyond `g_x = 60`);
2. the torus part of each covariance, as one constant `M_1`-bound;
3. the kernel normalization `Theta` in the pin density (`n theta_1 / 2`);
4. in `d = 3`, the Loewner coupling's truncation at radius 12 (`out_D2`, `tail_c`), present even for the Gaussian kernel;
5. the far set `G_0^c`, bounded at its worst radius `R`.

Theorem L′ removes all five:
1. Every rounding goes into a coefficient radius and every truncation into a remainder proportional to `r^9` (§2).
2. The torus part is split coefficientwise (Lemma V2). Its constant term cancels against `A_0^(L)`, and its higher terms
   carry powers of `r`.
3. `Theta` multiplies only increments (Lemma V3).
4. The main normalizer term is compared at `r` and at `0` directly, without truncation (Lemmas V4, V5).
5. The far set is bounded by Markov's inequality at order 64, which gives `O(r^2)` (Lemma V6).

## 2. Interval-coefficient Taylor models (Lemmas V1, V2)

**Lemma V1 (the class `TV`).** A `TV` on `[0, R_0]`, `R_0 = 1/64`, is a list of centers `C_j`, radii `D_j` (`j <= 8`) and a
remainder coefficient `E`. It encloses a function `f` if there are **fixed** numbers `c_j in [C_j - D_j, C_j + D_j]` and a
function `rho` with `|rho(r)| <= E r^9` such that `f(r) = sum c_j r^j + rho(r)` for every `r in [0, R_0]`. Then `f(0) = c_0`.
Sums, products, scalar multiples and reciprocals of enclosed functions are enclosed by the operations of `theorem_v.py`:
- **Products.** The coefficient `sum_{i+j=k} a_i b_j` lies in the interval product. For `k <= 8` its center is rounded
  with the error added to the radius. For `k > 8` the term is at most `(|S_k| + Rd_k) R_0^(k-9) r^9`. The cross terms
  `rho_a g_b`, `rho_b g_a`, `rho_a rho_b` are at most `(E_a |g_b| + E_b |g_a| + E_a E_b R_0^9) r^9`, where `|g| <= sum (|C_j| + D_j) R_0^j`.
- **Reciprocals.** Write `f = c_0 + h`, with `h(0) = 0` and `u = 1/c_0` in an interval. The interval is centered at
  `1/C_0`, so that centers stay the reference values. Then `g = h u` has `|g(r)| <= G_1 r`, and
  `1/f = u sum_{n <= 8} (-g)^n + u theta (G_1 r)^9/(1 - G_1 R_0)`. The certificate requires `G_1 R_0 < 1/2` and `g(0) = 0`.

Nothing is assumed about the coefficients beyond their intervals. In particular the same unknown number appears
consistently wherever an enclosed function is reused, because each operation is sound for every admissible choice.

**Readers.** For `0 < r <= R`, with `H = sum_{j >= 3} (|C_j| + D_j) R^(j-2) + E R^7`:

    f(r) - f(0)  in  [c_1^lo r + (c_2^lo - H) r^2,  c_1^hi r + (c_2^hi + H) r^2].

**Lemma V2 (the torus part, coefficientwise).** For the covariance of two preconditioned functionals with weight `w`:
- [E] §2(c) writes the torus part as `sum_{g_x >= w} partial^gamma rho(0) pi_gamma r^(g_x - w)`, with
  `|partial^gamma rho(0)| <= g_x! g_y! M_1` (Cauchy estimates on the unit polydisc).
- `|pi_gamma| <= sum |c c'| |d|^m/m!`, with `m = g_x - A`, `|d| <= 1`.
- `g_x!/(g_x - A)! <= w^A e^(g_x - w)`, because `A log x <= w(x - 1)` for `x = g_x/w >= 1`.

So the coefficient of `r^p` in the torus part is at most `T_0 e^p`, with `T_0 = sum |c c'| g_y! max(w, 1)^A M_1`, the
quantity [E] uses at `p`-sum level. The certificate adds:
- radii `T_0 e^p` to the coefficients `p = 0, ..., 8`;
- `T_0 e^9 / (1 - e R_0) r^9` to the remainder.

The reference series gives the centers exactly. The truncation tail beyond `g_x = 60` is at most
`2 |c c'| |h(g_y)| 61^A r^(61 - w)` for `r <= 1/64` ([E] §2(b)), so it goes into the `r^9` remainder (`61 - w >= 9` is
checked). `M_1(10) < 4.46 x 10^-15` (`d = 2`) and `< 1.94 x 10^-13` (`d = 3`) decrease in `L`, so the models hold for every
`L >= 10` and every frame; with `M_1 = 0` they are the Gaussian kernel's.

The six pins, the targets of [B] §2 and Gaussian elimination without pivoting give `TV`s for `det S_r`, the energies `e_bb`,
`e_bk`, `e_kk`, the regression coefficients `alpha`, `beta` of the transverse Hessian and of `Omega'`, their covariances, and in
`d = 3` the regression of `Omega'` on `B = -A`. The certificate checks that the centers are [B]'s reference laws. In
particular the law of the transverse Hessian is flat in `r` ([B] Lemma 1): every center of `alpha_A + 1`, `beta_A` and
`Cov(A) - Cov(GOE)` vanishes to `10^-60`, so on the torus only radii survive.

## 3. The pin density (Lemma V3)

With `S_r` the unnormalized pin covariance and `Theta in [1, 1 + theta_1]` the normalization, `pi_r ∝ det(S_r/Theta)^(-1/2)
exp(-Theta E_r/2)`. So

    log(pi_r / pi_0) = -(1/2) log(det S_r / det S_0) - Theta (E_r - E_0)/2.

`Theta^(n/2)` cancels and `Theta` multiplies only the increment `E_r - E_0`. With `x = (det S_r - det S_0)/det S_0` and
`|x| <= x_m < 1/2`:
- `-(1/2) log(1 + x) <= max(0, -x)/(2(1 - x_m))`;
- `(1/2) log(1 + x) <= max(0, x)/2`.

The increments of `det S` and of the energies are read off the `TV`s as above. On a box with `b, k >= 0` the energy weights
`b^2`, `2bk`, `k^2` are nonnegative and the bounds are taken coefficientwise. There is no constant term:
`log(pi_r/pi_0) in [-(dn_a r^2 + dn_b r), up_a r^2 + up_b r]`.

## 4. The normalizer (Lemmas V4–V6)

As in [B] §4 (exact expansion of `W_r = r^2 P1 P2` on the typed set, the three first-order cancellations, Hölder for the
second-order terms):

    Z_r / (36 k^2 r^2) = m_r + (first-order term) + (second-order terms),

where `m_r = E_r[lambda_+^2]` (`d = 2`) or `E_r[det(B)^2 1{B > 0}]` (`d = 3`), under the law at `r`, and `m_0` is the same
under the law at `0`. Then `A_r / A_0 = (pi_r/pi_0) (Z_r / (36 k^2 r^2 m_0))`, and every term below is divided by `m_0`.

**Lemma V4 (`d = 2`, main term).** `lambda ~ N(mu, sigma^2)` with `mu = -(b alpha_w + k beta_w)`, `sigma^2 = C_ww / Theta`, and
`F(mu, sigma) = E[(mu + sigma z)_+^2]`. Then `dF/dmu = 2 E[lambda_+]` and `dF/d(sigma^2) = Phi(mu/sigma) <= 1`. Along the
segment from `(mu_0, sigma_0^2)` to `(mu_r, sigma_r^2)`, which stays in the band's range,

    |m_r - m_0| <= 2 F_1,max |mu_r - mu_0| + |C_ww(r) - C_ww(0)|,      m_0 >= F_min.

Both increments are `TV` increments. For the Gaussian kernel they vanish ([B] Lemma 1).

**Lemma V5 (`d = 3`, main term).** In natural coordinates `(B_11, B_22, sqrt2 B_12)` the Frobenius norm is Euclidean. Couple
`B_r = mu_r + C_r^(1/2) Z` and `B_0 = mu_0 + C_0^(1/2) Z`.
- `g(B) = det(B)^2 1{B > 0}` is continuous, since `det B = 0` on the boundary of the cone.
- `g` is piecewise smooth along segments, with `|grad g| = 2 |det B| ||adj B||_F <= ||B||_F^3` (`2 x 2`:
  `|det B| <= ||B||_F^2/2`, `||adj B||_F = ||B||_F`).

Hence

    |m_r - m_0| <= E[max(||B_r||, ||B_0||)^3 ||B_r - B_0||] <= sqrt2 ||B||_8^3 (||mu_r - mu_0|| + ||C_r^(1/2) - C_0^(1/2)||_F).

Square roots satisfy `||C_r^(1/2) - C_0^(1/2)||_F <= ||C_r - C_0||_F / (2 sqrt(lambda_min))`. Proof:
- `X = C_r^(1/2) - C_0^(1/2)` solves `C_r^(1/2) X + X C_0^(1/2) = C_r - C_0`.
- In the eigenbases, `|X_ij| (s_i + t_j) = |(C_r - C_0)_ij|`.
- Here `lambda_min` is the Gershgorin floor over the band.

`||B||_8` is the band's Frobenius moment bound, and `m_0 >= m_3(b) rho_lo`, with `rho_lo` from [B]'s Loewner coupling over
`[0, R]` (which contains `r = 0`). For the Gaussian kernel the increments vanish.

**First-order terms.** For `d = 2`, the term is `-36 k^2 r E[lambda_+ om]`. For `d = 3`, it is `-36 k^2 r E[D tr(A* Omega') 1]`.
- [B] writes each through the regression, with coefficients `mu_om`, `bw_om` (`d = 2`) and `beta(r)`, `mu_Omega`, `DG`
  (`d = 3`).
- Each `TV` coefficient satisfies `|t(r)| <= c_0 + s r`.
- The explicit factor `r` turns `c_0` (a torus radius; `0` for the Gaussian kernel) into a contribution to `beta`. It turns
  `s` into a contribution to `a`.
- In `d = 3`, `r beta(r) - r^2/2 = c_0 r + (c_1 - 1/2) r^2 + ...`, with `c_1` centered at `1/2`.

**Second-order terms.** These are [B]'s, with its interval band laws, divided by `m_0` instead of the reference moment:
- in `d = 2`: the signed `kappa` term, `T_4`, `T_5`, `T_6` and the thin set;
- in `d = 3`: `U_2`, ..., `U_10` and the thin set.

**Lemma V6 (the far set).** `G_0^c = {|T| > 3k/(2r)} u {|tau| > 3k/(2r^2)}` enters through
`E[W_r 1_(G_0^c)]/r^2 <= P1n P2n P(G_0^c)^(1/2)` ([B] §5). By Markov's inequality at order `p = 64`:

    P(G_0^c) <= (2 ||T||_64/(3 k_0))^64 R^60 r^4 + (2 ||tau||_64/(3 k_0))^64 R^124 r^4,

so this term is `O(r^2)`.

## 5. Assembly

`(1 + p)(1 + z) - 1 <= p + z + p z(R)` and `1 - (1 - p)(1 - z) <= p + z`, with `exp(x) - 1 <= x exp(x(R))` for the pin factor.
This gives Theorem L′ on each of the 96 boxes `[i/8, (i+1)/8] x [1/2 + j/8, 1/2 + (j+1)/8]` (as in [B]) and each `R`.

**Corollary L′1.** As in [B] Corollary L1:
- `ell^(1/3) nu_cand(ell) = int_{B x K x S^(d-1)} A_r(b, k, u) / (3 k^(2/3)) db dk dsigma(u)`, with `r = (ell/k)^(1/3) <= R`
  ([LP] (11.2)).
- Theorem L′ holds uniformly in the direction `u`. Integrate it box by box, over each box and all of `S^(d-1)`:
  `a r^2` gives the weight `int_{box x S^(d-1)} A_0 / (3 k^(4/3))`, and `beta r` gives `int_{box x S^(d-1)} A_0 / (3 k)`.
  No isotropy is used. The reference weights of the pinned `theorem_b.py` are these full angular integrals for `A_0^ref`
  (its `K_const` includes `|S^(d-1)|`), so the program needs no extra sphere factor (OA-227-C-01, review 5384474393).
- The weights of the torus `A_0^(L)` are at most `(1 + eps_0)` times the reference weights. Here `eps_0` is [B]'s
  `|A_0/A_0^ref - 1|` bound, recomputed by the pinned `theorem_b.py` at `R = 1/4096`:
  `eps_0 <= 3.95 x 10^-10` (`d = 2`), `1.78 x 10^-8` (`d = 3`).
- The elder line is [B]'s.

## 6. Verification

- `python3 -B -S theorem_v.py --check` recomputes everything and compares it with `RESULTS.json` exactly:
  - the `TV` laws of both kernels;
  - the 2 x 7 x 96 box bounds per kernel;
  - the reference integrals and the `r^1` weights;
  - `eps_0`;
  - the corollaries.

  It takes about 3.5 minutes on one core and passes under `-B -S` and `-B -O -S`.
- Five mutants, each of which must exit 1:
  - `torus-const-only`: the torus part only in the constant coefficient;
  - `exp-radius`: `e^p` replaced by `1` in the torus radii;
  - `no-lin`: drop the `r^1` coefficients;
  - `no-om-term`: drop the first-order terms;
  - `coupling-half`: halve Lemma V5's constant.
- The workflow `.github/workflows/c8-torus-vanishing-remainder.yml` checks:
  - the manifest;
  - the main-resident pin [LP];
  - the packet copies [B], [E], [E3], byte for byte;
  - both modes;
  - the mutants;
  - a clean tree.

**Consistency with [B].** With `beta` set aside, `a(R)` reproduces [B]'s Theorem L table, as in §0. The `c2/c` ratios
reproduce [B]'s Corollary L1 to within `5 x 10^-4`. Both come from an independent assembly, using increments rather than
deviations from `A_0^ref`.

## 7. What this does not do

- **Still the compact window `B x K`, `L >= 10`, `d = 2, 3`, `R <= 1/64`.** These are [B]'s ranges.
- **`beta` is not the true first-order coefficient.** It bounds the torus part of the `r^1` coefficients through
  `M_1`. Whether the torus `A_r` has a nonzero `r^1` term at all (of order `e^-50`) is not decided.
- **Consumed, not reviewed:**
  - [LP]'s sections 8–12, as in [B];
  - [B]'s §§2–5 algebra (exact expansions, first-order cancellations, Hölder bounds, Loewner coupling for the moment
    bounds);
  - the interval band laws and transcendentals of [E], [E3].

  [B] is author-side with an OpenAI amendment ACCEPT (5378815703). [E] and [E3] are author-side and unmerged.
- No `C`, `r_*`, `z_*` beyond [B], #206, #212 and #195. No new count, moment or elder statement beyond Corollary L′1.
- Same GitHub account as every lane; zero organizational-independence credit. **I will not merge.**

## 8. Provenance

- **Sources** (`SOURCE_MAP.json`):
  - [LP] `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` (on `main`, verified by the workflow);
  - [B] Math-#215 `theorem_b.py` at `d77cabf` (packet copy `theorem_b.py`) and its `NOTE.md` and `RESULTS.json` (provenance);
  - [E] Math-#206 `theorem_a.py` (packet copy `engine_e2.py`);
  - [E3] Math-#212 `theorem_a3.py` (packet copy `engine_e3.py`).
- **Files:**
  - `NOTE.md`, `README.md`;
  - `theorem_v.py` (new);
  - the copies `theorem_b.py`, `engine_e2.py`, `engine_e3.py`;
  - `RESULTS.json`, `SOURCE_MAP.json`, `SOURCE_FILES.json`.
