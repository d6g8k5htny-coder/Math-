# Finite-radius count-weighted multi-soft transfer

Author-side mathematical candidate for Dylan Roy's IBA2-012 work. The author
OpenAI / GPT-6 Astra Pro (`iba2-count-weight-transfer-r6-20261006`) wrote the
FR precursor. Scientific effect NONE; organizational independence credit0.

`PROOF.md` fills the count-insertion gap explicitly left by the landed #306
finite-radius event estimate. For the same tilted pin law, compact positive
marks and fixed d,L,R, it derives

    E[K^a N^s; E_r] <= C r^3 Pi_r^(1-s/p), p>s fixed integer,
    Pi_r = product (eta_j+r)^(j+2).

Every fixed polynomial-count contribution is o(r^3) on the specified shrinking
sectors. Positive-count intensities inherit weighted-l1 deletion control.
An explicit abstract rare-spike family proves that no-loss preservation of
Pi_r does not follow merely from all fixed moment bounds. This is NOT a
Gaussian counterexample, full cluster-law rate, all-mark theorem, or scientific
acceptance. First/second factorial normalization uses explicit lower bounds;
third and higher orders require a separate denominator lemma.

Sources are pinned at Math- commit
`2f8b6f372be383d752e9dd30d38234faa977243c`; read original DL/C6 with the additive
erratum. Source and payload hashes are in `SOURCES.json`.

```
python -B -S test_transfer.py
python -B -O -S test_transfer.py
python -B -S transfer_check.py
python -B -O -S transfer_check.py
python -B -S transfer_check.py --mutant M1  # exit1, named failed check; M1-M5
```

Twelve tests and the deterministic checker are exact finite controls, not a
continuum or Lean proof. No source files, workflow, formal manifest, status or
review record outside this additive packet are modified. Nonauthor source
review and all applicable integration checks remain separate obligations.
