# Nonauthor review — OA-PIN-MICRO-COV-20260926-v1 (pin microdisk covariance lemma)

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, `STATUS`,
`PROOF_INDEX`, D5 or global RN. It does not edit the author source.

## Claim

| Field | Value |
|---|---|
| Object | `reviews/pin_micro_covariance_20260926/NOTE.md` (OA-PIN-MICRO-COV-20260926-v1) |
| Commit reviewed | `582c05b4c5a28dca164605313a0ac8bad81206d5` (Math- `main`) |
| Blob / size / SHA256 | `36cc6cfcc0ab776bc22e5f1f480d4d264b1294a6` / 5273 B / `0351da0680e81c2b001338ede50770b9e00fa5cb09aab438940a9b81d56fd866` |
| Author of the object | OpenAI / ChatGPT |
| Scope | Items 1–5 of the note's §6 review request, at fixed d=2, fixed L, compact b, `0<k_-<=k<=k_+` |
| Write scope | `reviews/pin_micro_covariance_nonauthor_20260928/` only |

## Reviewer provenance

| Field | Value |
|---|---|
| Provider / tool | Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` |
| Relation to author | Different provider and different session. Same GitHub account as every lane, so no organizational independence is claimed. |
| Exposure | Author note, `d5_pin_microdisk_20260927/NOTE.md`, `d5_short_edge_20260928/NOTE.md`, the PR28 nonauthor review, and `frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md` (A5) were read. The derivations below were redone independently. |

## Verdicts

| Item | Verdict |
|---|---|
| 1. Degree-four pin solution and `B_r` | **CONFIRMED (exact).** |
| 2. Minors and Cauchy–Binet `h`-scale bound | **CONFIRMED (exact constants).** |
| 3. Uniform residual Schur covariance | **CONFIRMED** by the reviewed lattice-positivity argument, extended to all jets of order ≤ 4. |
| 4. Taylor remainder o(h), uniform across Q=0 and P=0 | **CONFIRMED with an explicit rate O(r h).** |
| 5. Mean/density coercivity (4.1), (4.2) | **CONFIRMED.** |
| Extension | (3.1)–(4.2) hold on the **whole pin chart**: the square `|rP|,|rQ|<=1/4`, which contains the disk `|X-M|<=r/4`, not only on bounded (P,Q). |

### 1. Pin solution and B_r

`cov_exact_check.py` builds the degree-four Taylor polynomial at M with `f(M)=b` and `grad f(M)=0`, and
all nine free jets `(S0,T,R4,C,D,E1,E2,E3,F4) = (f_zz,f_xxz,f_xxxx,f_xzz,f_zzz,f_xxxz,f_xxzz,f_xzzz,f_zzzz)`.
It verifies the following as exact polynomial identities:

- `f_xx=-6kr+r^2R4/12`, `f_xxx=12k-rR4/2` and `f_xz=-rT/2-r^2E1/6` satisfy the three pins at S.
- The `(S0,T,R4)` coefficients of `G_r=(f_x(X)/r^3, f_z(X)/r^2)` equal the note's `B_r` entry by entry.

The note's `f_xz=-(r/2)T+O(r^2)` has exact degree-four form `-(r/2)T-(r^2/6)f_xxxz`.

### 2. Minors and constants

- The three minors `m_ST`, `m_SR`, `m_TR` are exact identities.
- For `|rP|<=1/4`: `|m_ST|>=Q^2/4`, `|m_TR|>=(3/256)r^2P^2`, and
  `det(B_rB_r^T) >= (9/131072) h^4`.
- `tr(B_rB_r^T) <= (25/16) h^2`. The trace bound needs only `|rP|<=1/4`, with no bound on Q.
- Hence `sigma_min(B_r)^2 >= (9/204800) h^2`.

### 3. Residual Schur floor

**Jet positivity.** The PR28 nonauthor review (blob `559d7224…`, R-section on the nine-jet covariance) and
FIXED_ANNULUS_CANDIDATE (A5) use this fact: every Fourier weight of the periodized Gaussian kernel is
positive on the full rotated lattice, and a polynomial vanishing on `Z^2` is zero. So any finite family
of distinct one-point derivative monomials has positive-definite covariance, uniformly over the compact
frame set. Applied to all 15 monomials of order ≤ 4, the Schur complement of the nine free jets `J` given
the contact frame `U_0=(f,f_x,f_z,f_xx,f_xz,f_xxx)(M)` is positive definite.

**Convergence.** The six pins are an invertible Hermite transform of a desingularized vector
`U_r = U_0 + O_{L^2}(r)`, so `Cov(J|pins) -> Cov(J|U_0)` and a uniform floor `lambda_*` holds for
`r<=r_*`.

**Conclusion.** Writing `G_r = B_full J + mean + remainder`, where `B_full` contains the `B_r` columns,
`B_full Cov(J|pins) B_full^T >= lambda_* B_r B_r^T >= lambda_* (9/204800) h^2 I`.

### 4. Remainder

**Key inequality.** For `r<=1`, `h^2 = Q^2+r^2P^2 >= r^2 rho^2` with `rho^2=P^2+Q^2`.

**The omitted terms are:**

- degree-≥5 Taylor terms of f: `O(r^5 rho^4)` in `G_r1` and `O(r^6 rho^4)` in `G_r2`;
- degree-≥5 corrections to the pin solve (`f_xx`, `f_xxx`, `f_xz` shifted by `O(r^3)`, `O(r^2)`, `O(r^3)`
  times fifth-order jets): contributions `O(r^2 P)`, `O(r^3P^2)`, `O(r^2 Q)`, `O(r^3P)`.

**Bounds.** With `r rho <= 1/(2 sqrt 2)` on the chart, each term is `<= C r h`. For example,
`r^5 rho^4 <= (r rho)^3 r h` and `r^2|P| <= r h`. The coefficients are fifth-order sups of the regressed
field. Under `Q_r` they have uniformly bounded moments by (A5): the conditional variance is at most the
unconditional one, and the conditional mean is bounded for compact (b,k). All terms vanish at (P,Q)=0.

**Conclusion.** The remainder is `O_{L^2}(r h)` uniformly, which is stronger than the note's o(h). Then
`c h^2 I <= Cov(G_r|pins) <= C h^2 I` for `r<=r_*`.

### 5. Mean and density

**Mean.** The exact degree-four mean is `(6kP(rP-1), 0)`. Every random column is `O(h)` (checked exactly
below), and conditional jet means are bounded, so `E[G_r|pins] = (6kP(rP-1),0) + O(h)`, with
`|6kP(rP-1)| >= (9/2)k_-|P|` for `|rP|<=1/4`.

**Density (4.1).** The Gaussian density at 0 is at most `(2 pi c h^2)^-1 exp(-|mu|^2/(2Ch^2))`.

- If `|P|>=A h` with A large, then `|mu|>=(9/4)k_-|P|`.
- If `|P|<A h`, the factor `exp(-cP^2/h^2)` is at least `exp(-cA^2)`.

Either way (4.1) follows.

**Physical density (4.2).** The physical gradient is `(r^3G_r1, r^2G_r2)`, which gives the Jacobian factor
`r^-5` in (4.2).

### Extension to the whole pin chart (checked exactly)

The note restricts to `|P|,|Q|<=K`. Rewrite each random column as a polynomial in `(r, s=rP, Q)`.

- `cov_exact_check.py` confirms, for all 18 columns, that every monomial `r^a s^b Q^c` has `a>=0`,
  `b+c>=1` and `a>=c-1`.
- Consequently every column is `O(|s|+|Q|)=O(h)` uniformly for `|s|,|rQ|<=1/4`, even though Q is then
  unbounded.
- Items 2–5 above used only `|rP|<=1/4` and `r rho <= 1/(2 sqrt 2)`.

Hence (3.1), (4.1) and (4.2) hold on the whole pin chart, the square `|p|,|q|<=1/4`. That square contains
the disk `p^2+q^2<=1/16` (`|X-M|<=r/4`), which is what the pin-disk note uses. In physical dimensionless coordinates
`p=rP`, `q=rQ` this reads:

```
p_{grad f(X)|pins}(0) <= C r^-3 (q^2+r^2p^2)^-1 exp(-c p^2/(q^2+r^2p^2)),   |p|,|q|<=1/4.
```

On the transverse cone `|p|<=|q|` this is the premise `C_p/(r^3q^2)` assumed in
`d5_short_edge_20260928/NOTE.md` §5.

## Checks run

```
python -B -S cov_exact_check.py        # rc 0
python -B -O -S cov_exact_check.py     # rc 0, byte-identical output = RESULTS.json
python -B -S cov_exact_check.py --mutant pin-sign        # rc 1
python -B -S cov_exact_check.py --mutant B-entry         # rc 1
python -B -S cov_exact_check.py --mutant column-r-power  # rc 1
python -B -S cov_exact_check.py --mutant trace-constant  # rc 1
```

The trace bound `tr(B_rB_r^T) <= (25/16)h^2` is proved by the script, not only its constant. It checks an
exact trace identity `tr = Q^2 f1(rP) + (rP)^2 f2(rP)`, then bounds `f1` and `f2` on `|rP|<=1/4` by
convexity and monotonicity checks.

These are exact polynomial identities, not a continuum or Gaussian proof. Items 3–5 rest on the written
argument above.

## Not established here

- Kac–Rice validity.
- The determinant-weighted expectation (the note's §5): see `reviews/d5_pin_disk_all_directions_20260928/`
  for a separate author-side proposal.
- The collar to the reviewed annulus, and multiple-witness collisions.

D5 stays open.
