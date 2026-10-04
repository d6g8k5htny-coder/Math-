# C8: the radial ledger on the torus with a vanishing remainder

Theorem L′ (`NOTE.md`): for the torus kernel (every side `L >= 10`, every frame) and the Gaussian kernel, `d = 2, 3`, on the
band `b in [0, 1]`, `k in [1/2, 2]`,

    -(a_dn r^2 + beta_dn r)  <=  A_r / A_0 - 1  <=  a_up r^2 + beta_up r        (0 < r <= R <= 1/64),

with `A_0` the contact integrand of the same kernel. The `a(R)` are Math-#215's Theorem L constants (13.82 / 3.64 in the
plane, 25.67 / 25.52 in `d = 3` at `R = 1/4096`); `beta_2 <= 1.04e-9`, `beta_3 <= 1.92e-7` on the torus and `beta = 0` for
the Gaussian kernel. This removes the `r`-independent `eps_d` of Math-#215. Corollary L′1 gives `ell^(1/3) nu(ell)` about
the torus's own `c_{B,K}` with remainder `c1 ell^(1/3) + c2 ell^(2/3)`.

Replay (standard library, about 3.5 minutes):

    python3 -B -S theorem_v.py --check
    python3 -B -S theorem_v.py --mutant torus-const-only     # must exit 1 (also exp-radius, no-lin, no-om-term, coupling-half)

`theorem_b.py`, `engine_e2.py` and `engine_e3.py` are byte-identical copies of Math-#215's files (and of the engines of
Math-#206, #212), pinned in `SOURCE_MAP.json`. Scientific effect NONE; author-side; not merged by its author.
