# Recovered H5 ledgers and STAGE_E input-selection audit

Recovered on 2026-09-26: **48 original JSONL files, 98,773 bytes**, from Dylan's
authorized UPPER2D Dropbox folder. Every raw file retains its original bytes,
including failed outcomes. These are raw files, not native-document exports or
reading copies. Publication and integrity checks adopt no historical proof labels.
**Scientific effect: NONE.**

These files supply the direct `H5_closure/h5_results_*.jsonl` input glob missing
from [the earlier STAGE_E recovery](../upper2d_stage_e_20260926/README.md).
The scope is exactly that nonrecursive glob: five radius groups, with 7, 7, 10,
10 and 14 files for 0.0125, 0.0177, 0.025, 0.035355 and 0.05 respectively.
The archive and STAGE_E snapshot/mutation directories are separate source sets
and are not flattened into this one. This packet does not claim the entire
research corpus has been recovered.

## Read and reproduce

- [Raw ledgers](raw/H5_closure) preserve full records, not summaries.
- [Manifest](MANIFEST.json) records source IDs/paths, sizes, SHA256, Git blob SHA1,
  Dropbox content hashes, inspected public refs, and exact consuming scripts.
- [SHA256 list](MANIFEST.sha256) supports ordinary file checks.
- [Review](REVIEW.md) describes the loader and the missing exponent finding.
- [Selection audit](SELECTION_AUDIT.json) records every selected source line,
  all overwrite history, ignored failure rows and rim-literal comparisons.
- [Radius-scoped rim successor](../../repairs/h5_rim_contract_20260926/REPAIR.md)
  removes manual literal transcription at the data-interface level and records
  the exact angle-175 impact; it does not rerun or certify the numerical hunt.

From the Math- repository root, with Python's standard library only:

```sh
python -B -S imports/upper2d_h5_ledgers_20260926/verify.py
python -B -O -S imports/upper2d_h5_ledgers_20260926/verify.py
python -B -S imports/upper2d_h5_ledgers_20260926/verify.py --emit
```

The verifier checks all 48 identities and regenerates the selection receipt.
It runs only the inspected, hash-pinned `merged_constants` function with Decimal
substituted for `mpf`, and independently compares a second selector. It does not
import the numerical modules, execute the hunt, or validate numerical bounds.
Decimal arithmetic here records source values and their multiplication by two;
it is not a reproduction of mpmath, interval arithmetic or QMC.

For a numerical reproduction environment, copy the earlier packet's `raw/`
tree to a temporary directory and overlay this packet's `raw/H5_closure/` there.
Keep the original imports unchanged. That assembles the missing data layout;
it does **not** resolve the earlier review's dependency, execution, covariance,
enclosure or proof obligations. The numerical hunt has not been rerun here.

## Material findings

The wedge loader reads 903 rows, recognizes 156 probe rows, and retains 111 site
keys after 45 value-changing overwrites. It does not put the radius in the key or
filter by radius. Thirty-four overwrites cross radius groups; 82 final site
records are from radii below 0.05. Nevertheless, all four resulting maxima come
from 0.05 records. This audit therefore does not claim that mixed radii alter
those four final constants for this exact file set.

The rim script uses a literal dictionary instead of reading these ledgers. At
angle 175 its literal is `1.72865592536977723981`; the final ledger row is
`1.728655925369777239812566677032221782361e-35`. The exponent is absent from the
literal, yielding a discrepancy of about 10^35. The nine other literals truncate
the corresponding ledger decimals. Neither the script nor the raw ledgers were
silently corrected. A successor must review the intended bound, restore explicit
input/radius identities, and rerun the affected computation before relying on it.

Eleven failure rows remain visible and are ignored by the original successful
probe selector. They do not certify zero intensity or complete coverage.
No theorem, flatness hypothesis, Palm transfer, continuum enclosure, scientific
status, or independent acceptance is established by this recovery.
