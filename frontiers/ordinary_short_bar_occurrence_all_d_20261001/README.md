# Ordinary short-bar occurrence in every dimension

This packet extends OpenAI/Codex's planar C52 theorem (Math-#235) to the periodized Gaussian field on `T_L^d` for every
`d >= 2`. A field that contains a sufficiently short ordinary finite superlevel H0 bar asymptotically contains only one
such bar. The probability that one occurs has the same leading coefficient, `L^d (3/2) c_{d,L} tau^(2/3)`, as the
expected count. Sampling a bar after conditioning the field on occurrence has the same limiting mark law as the
intensity calculation.

[Theorem and proof](NOTE.md) · [Exact sources](SOURCES.json)

**What is new.** The only new step is ordinary-fold isolation in dimension `d` (NOTE §2):
- the transverse ridge on a ball;
- the identities `g''' = D³F[v,v,v]` and `g'' = Schur complement`;
- Haynsworth inertia for the pin types;
- the `{lambda_max(A) = 0}` null boundary;
- the general-`d` mesh counts.

The consumer (NOTE §§3–4) is C52's, written out with `L^d`, `S^(d-1)` and `c_{d,L}`. For `d = 2` it is C52's Theorem O.

**Conditional.** The theorem retains the imported elder-pairing, Kac–Rice and Gaussian interfaces of the seven pinned
sources, all of which are stated for every `d >= 2`.

**Not supplied:**
- a rate;
- factorial moments or a Poisson law;
- an increasing-volume limit;
- uniformity in `d`.

Scientific effect NONE; C8 OPEN.

Run from the repository root:

```sh
python3 -B -S frontiers/ordinary_short_bar_occurrence_all_d_20261001/verify_sources.py
python3 -B -S frontiers/ordinary_short_bar_occurrence_all_d_20261001/check.py
python3 -B -S frontiers/ordinary_short_bar_occurrence_all_d_20261001/test_check.py -v
python3 -B -O -S frontiers/ordinary_short_bar_occurrence_all_d_20261001/test_check.py -v
python3 -B -S frontiers/ordinary_short_bar_occurrence_all_d_20261001/test_check.py --mutants
```

The exact rational controls check the finite identities for `d = 2..6`. They do not prove the continuum analysis.

Author lane: Anthropic / Claude, under Dylan Roy's delegation; personal reading PENDING. Every lane uses the same
account, so organizational-independence credit is 0.
