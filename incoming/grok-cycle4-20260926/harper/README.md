# Harper cycle-4 packet (2026-09-26)

Assigned fronts: (D) D5 transverse-cone / on-axis sigma power ledger; (E) SARD-G A1 relative-interior predicate as a standalone lemma.

Also included: exact planar Bargmann–Fock six-pin variances for `f_ts` and `f_tt`, certified by direct covariance calculus.

## Files

- `D5_OBSTRUCTION_LEDGER.md` — coordinate vs congruence isolation. No count lemma.
- `SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md` — standalone lemma an external reviewer can apply to the author source. Author source not edited.
- `CLOSED_FORMS_FTS_FTT.md` — exact identities and series.
- `test_closed_forms.py` — stdlib-only checks of the closed forms: float evaluations against the series prefixes, plus exact rational-series checks of the TS and TT coefficients, the TT denominator order (`-r^8/12`, no `r^6` term) and numerator order (`-r^{12}/72`).

Run from the repository root:

```sh
python -B -S -m unittest discover -s incoming/grok-cycle4-20260926/harper -p 'test_*.py' -v
```

## Sibling packet files (same PR, same firewall)

The change set also carries two sibling directories that were added to this branch after the Harper files. They are author-side notes with the same scientific effect (NONE) and are listed here so that the packet inventory matches the diff:

- `../benjamin/REDUCED_FRAME_4SLOT.md` — leftover 4-slot Gram at `M` after six pins; `Var(f_sss(M) | six pins) = 6` and `Var(L | six pins) = 3/2`, not the unconditional `15/4`.
- `../benjamin/ALPHA_4PIN_SERIES.md` — axial remainder series for `E[alpha_M] + 6k`.
- `../lucas/SARD_G_A1_APPLIED_TO_SUCCESSOR.md` — the RI1–RI4 predicate of `SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md` applied item by item to the written successor Section 3. The SARD-G author source is not edited.
- `../PUBLIC_READING_MAP.md` — pointer-only reading map for this packet.

## Amendments on this branch (2026-09-27)

- `CLOSED_FORMS_FTS_FTT.md`: the "Denominator check" paragraph previously stated the small-`r` denominator as `~ r^6/12`. The correct first nonzero order is `-r^8/12` (the `r^6` terms cancel); the numerator is `-r^{12}/72`, so the displayed series `r^4/6 - r^6/30 + r^8/360 - r^{10}/12600` is unchanged. Exact-series tests were added.
- `D5_OBSTRUCTION_LEDGER.md`: remainders in the on-axis Taylor expansions now retain the displacement factor (`O(r^3 |q|^3)`), the slaving statements are labeled as conditional-moment (`O_p`) scales rather than pathwise bounds, the `(beta, S)` density constant is corrected to `1`, and the Section 6 cone assembly is labeled an on-axis heuristic.
- `SARD_G_A1_RELATIVE_INTERIOR_LEMMA.md`: `partial Sigma` is defined as the endpoint set `{a, b}` (not the topological boundary in `R^2`), RI2 requires terminal-time slack `t_* < t_max`, and the RI4 inner product is delimited.
- `../benjamin/REDUCED_FRAME_4SLOT.md`: a malformed `r -> 0` limit was repaired.

## Firewall

Does not flip `STATUS`, `LANDING_CLAIMS`, `lemma_closed`, prizes, or premises.
Does not edit PR53, reviewed annulus sources, or SARD-G author source.
D5 pin-neighborhood and SARD-G A1 remain AMEND.
Same-session corroboration only.
