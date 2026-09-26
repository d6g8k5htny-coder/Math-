# H5 rim input contract and angle-175 falsifier repair

Date: 2026-09-26. Disposition: **AUTHOR-SIDE SOFTWARE REPAIR / FALSIFIER**.
Scientific effect: **NONE**. Author: OpenAI Codex. This document does not accept
the H5-RIM flatness lemma, certify a numerical enclosure, or change a theorem or
premise status. The preserved historical source remains unchanged.

## Exact reviewed inputs

| Object | Immutable identity | Role |
|---|---|---|
| `imports/upper2d_stage_e_20260926/raw/STAGE_E/hunt_rim.py` | Math- `a2c3657c3115853a9bd8642b78c3f9ca0bbc59d1`; SHA-256 `de73e5fed00782c3709d2f9a8b1cddca23926606a8ef5ffc4cf0de8aefb66f90` | historical consumer |
| `imports/upper2d_h5_ledgers_20260926/raw/H5_closure/h5_results_r0.05_s0p1_rimprobes.jsonl` | Math- `f6a63031547c2433267b05a676d74fd54fb4412d`; SHA-256 `22c7107e93ba9c02bea1f6f34085044ab535f29c067ce79c0cd7d8b1911ecc63`; Dropbox source ID `id:PdRszXtmKE0AAAAAAAAAAQ` | exact radius-0.05 ledger |
| [H5 totals erratum](https://github.com/d6g8k5htny-coder/main/blob/7caac254cbba5f513b2dc0afb56b78a598bc0c93/drive/mirrors/2026-09-16%20%E2%80%94%20PEER_REVIEW_SUBMISSION_PACKAGES/PKG-01%20%E2%80%94%20U2D_CONDITIONAL_UPPER_D1_v2_2/07e_H5_TOTALS_ERRATA_2026-09-15.md) | main `7caac254cbba5f513b2dc0afb56b78a598bc0c93`; blob `91b5a9550da4b08a2f214c727f232ceeeec5c6f8`; SHA-256 `a7ce5299bdaab5a1a79da50af7b8e32f1b7d193d175d4dff46a224a0b12eb4f2` | prior rung-scoping correction |
| [H5 state](https://github.com/d6g8k5htny-coder/main/blob/7caac254cbba5f513b2dc0afb56b78a598bc0c93/drive/mirrors/2026-09-16%20%E2%80%94%20PEER_REVIEW_SUBMISSION_PACKAGES/PKG-01%20%E2%80%94%20U2D_CONDITIONAL_UPPER_D1_v2_2/07_H5_STATE.md) | main `7caac254cbba5f513b2dc0afb56b78a598bc0c93`; blob `1be02f986fb054594960826103998949cf0e75d6`; SHA-256 `42899319071f0e4db77c20c0d52e2f46e56b8aaa99dedddfa2d626543fc96d27` | frozen version discipline |

The public [H5 ledger recovery review](../../imports/upper2d_h5_ledgers_20260926/REVIEW.md)
already establishes custody and original loader semantics. This successor adds a
radius-scoped rim interface; it does not inherit a numerical-certification label.

## Reproduced defect

The historical consumer embeds ten decimal strings in `RHO_HI`. For angles
15 through 170, each string is exactly the corresponding final radius-0.05
ledger decimal truncated toward zero at 20 places after the decimal point. The
sole exception is angle 175:

```text
historical literal: 1.72865592536977723981
ledger rho_hi:      1.728655925369777239812566677032221782361e-35
```

Thus the literal is larger than the ledger value by a factor strictly between
`1e34` and `1e35`. This source pattern supports the narrow diagnosis “exponent
dropped during manual transcription.” It does **not** prove that the ledger row
is a valid bound; that requires the underlying numerical/enclosure argument.

The script defines `CFLAT = 2 * RHO_HI`. Under the explicit ledger contract,

```text
C_flat(175) = 3.457311850739554479625133354064443564722e-35
```

The hunt compares `rho / C_flat`. Inflating `C_flat` suppresses that ratio by
the reciprocal factor. Therefore any historical “no exceedance” result in the
175-degree column cannot exclude an exceedance against the ledger-derived
threshold. No actual exceedance is asserted here because the QMC hunt was not
rerun and the ledger bound itself was not re-certified.

## Successor contract

[`rim_contract.py`](rim_contract.py) makes the consumed data boundary explicit:

1. The requested radius must equal the radius encoded in the filename; this
   repair consumes only `r = 0.05`.
2. A completed rim block is terminated by a `rimprobes_done` row. The last
   completed block in the exact ledger is selected. In the bound source it is
   lines 30–39, terminated by line 58; preliminary lines 1–10 are not selected.
3. The completed block must contain exactly angles
   `15,45,75,105,135,150,160,165,170,175`, once each. Missing, duplicate,
   nonpositive, nonfinite, unterminated, malformed or explicitly failed rim
   coverage is rejected.
4. Decimal strings are retained as `Decimal`; `C_flat = 2*rho_hi` is computed
   with enough decimal precision to avoid the ambient 28-digit rounding that
   would otherwise alter the printed exact product.
5. The historical module is parsed with `ast`; it is never imported, so its QMC
   work and module-level `main()` do not execute.

This is a successor interface. It does not rewrite the original Dropbox bytes,
the raw GitHub import, or any frozen H5 document.

## Relation to the September totals erratum

The public totals erratum identifies a different defect: the old
`h5_results_*.jsonl` glob mixed radius-0.025 patch rows into radius-0.05
`patches_lo`, contaminating `I_lo`. It states that the fixed merger is
rung-scoped and that the frozen v2 `I_hi` was independently clean. This repair
follows the same radius-scoping principle, but its object is the standalone
`hunt_rim.py` literal, not `h5_totals_v2` or `I_hi`. Consequently:

- the totals erratum does not repair or validate the angle-175 literal;
- the angle-175 finding does not refute the erratum's clean-`I_hi` statement;
- neither artifact supplies the missing H5-RIM analytic flatness proof.

## Reproduction and falsifiers

From the Math- repository root, using only Python's standard library:

```sh
python -B -S repairs/h5_rim_contract_20260926/verify.py
python -B -O -S repairs/h5_rim_contract_20260926/verify.py
python -B -S repairs/h5_rim_contract_20260926/verify.py --emit
python -B -S -m unittest discover -s repairs/h5_rim_contract_20260926 -p 'test_*.py' -v
python -B -O -S -m unittest discover -s repairs/h5_rim_contract_20260926 -p 'test_*.py' -v
```

Falsifiers: a hash mismatch in either bound input; an alternative exact
radius-0.05 completed block; evidence that the literal was intended to use a
different construction rather than the cited ledger; a second mismatch outside
angle 175; or a valid enclosure showing that the selected decimal is not the
intended `rho_hi`. Any such evidence requires a successor review and rerun.

## Remaining obligations

- establish the H5-RIM flatness/continuum enclosure underlying the selected
  `rho_hi` values;
- recreate the numerical environment and rerun the affected hunt against this
  explicit contract, retaining QMC uncertainty and covariance-clipping limits;
- give the immutable repair head a nonauthor technical review; same-provider
  review earns zero organizational-independence credit;
- keep broader H5, RN/24-jet and contact-asymptotic obligations unchanged.
