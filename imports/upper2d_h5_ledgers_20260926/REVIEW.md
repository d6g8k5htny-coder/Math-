# Source-bound review: H5 ledger selection

Date: 2026-09-26. Review type: raw-source custody and software input semantics.
Scientific effect: NONE. Original authors' model/provider provenance: UNKNOWN.
Packet author: OpenAI Codex. Nonauthor read-only reviewer: a separate OpenAI
agent; same provider, **zero organizational-independence credit**. This is not
a qualified mathematical acceptance of the historical claims.

## Exact inputs and scope

All raw inputs are individually bound by [MANIFEST.json](MANIFEST.json) and
[MANIFEST.sha256](MANIFEST.sha256). The consuming source is Math- commit
`a2c3657c3115853a9bd8642b78c3f9ca0bbc59d1` (PR83):

| Path under `imports/upper2d_stage_e_20260926/raw/STAGE_E/` | SHA256 |
|---|---|
| `hunt_wedges.py` | `f03507da809d91eb6b358c4bf51298ba9d26bb6ab733e801cb5784394b96d48e` |
| `hunt_rim.py` | `de73e5fed00782c3709d2f9a8b1cddca23926606a8ef5ffc4cf0de8aefb66f90` |

The write scope is this additive recovery packet only. The historical scripts,
proofs, existing raw imports and scientific registers are unchanged. The four
public trees inspected before recovery contained none of these 48 Git blob IDs;
the exact refs are retained in the manifest. This is a bounded absence check,
not a claim about every branch or repository.

## Loader behavior, reproduced without numerical dependencies

`merged_constants()` sorts the nonrecursive file glob lexicographically, then
reads lines in file order. Its keys are `(scone, thS, dS)`, `(sdisk, thS)`,
`(sring, thS, dS)`, and `(mfwd/mbwd, thM, dl)`, with the last category determined
by `int(thM) < 90`. Radius is absent from every key; sdisk also omits `dS`.
Angles in this input are integers and depths are strings; the audit preserves
those types. No textual depth aliases were found in the selected keys.

Independent standard-library parsing found 48 files, 903 object rows, no blank
rows, no duplicate JSON object names and no NaN/Infinity JSON constants. Of 156
recognized probe rows, 111 survive: scone 24, mfwd 26, mbwd 26, sdisk 5, sring 30.
All 45 overwrites change the value: 34 cross radius groups and 11 stay within a
radius. Final radius counts are 17 / 24 / 17 / 24 / 29 in ascending radius order.
All four final envelope maxima are nevertheless supplied by radius 0.05 rows.
Full values and their source lines are in the regenerated selection receipt;
no extra coefficient precision is claimed as mathematical progress.

The independent selector agrees with the hash-pinned original loader function
executed in isolation with Decimal in place of `mpf`. This validates file/key
selection and exact decimal bookkeeping, not the numerical meaning of rho_hi.
No original module-level import or main routine is executed. The C1 engine,
QMC, covariance clipping, bounds and flatness assumptions remain outside scope.

## Failure rows are retained

Ten `mbackprobe_fail` rows and one `sconeprobe_fail` row are ignored by the
original loader. A failure does not erase an earlier success. Eight failed keys
eventually get successful records; three have no later success: mbwd angle 176
at depths `0.003`, `0.004248`, and `0.0084852`. These are absent probe entries,
not certified zero values. Three failures temporarily leave an earlier-radius
success selected before a later 0.05 record replaces it. Raw failures and their
origin lines remain public in the receipt and original files.

## Missing exponent in the rim literal

`hunt_rim.py` does not read JSONL files at runtime. Its `RHO_HI` dictionary claims
to reflect a last-wins merge. Last-wins `rimprobe` records at the ten dictionary
angles all come from `h5_results_r0.05_s0p1_rimprobes.jsonl`, lines 30–39.
Angles 15–170 agree after truncating each positive ledger decimal to 20 decimal
places. At angle 175, line 39 instead contains:

```text
ledger: 1.728655925369777239812566677032221782361e-35
script: 1.72865592536977723981
```

This is a source/data inconsistency of about 10^35, consistent with a dropped
exponent. Since `CFLAT` doubles the literal and the hunt divides by `CFLAT`, an
inflated literal changes the comparison threshold in the direction of hiding
exceedances. This algebraic direction does not establish an actual exceedance,
a valid replacement enclosure, or any theorem's falsity. We have not silently
repaired the historical script or accepted either value as a certified bound.

## Disposition and next obligations

The raw-input availability gap identified in Math #83 is repaired at the exact
48-file glob scope. The numerical hunt remains unverified. A subsequent repair
must specify a radius-aware input contract, retain failure/coverage semantics,
establish the intended rim bound against its underlying construction, and rerun
affected numerical work with the earlier enclosure obligations addressed.
The separate RN/24-jet/contact-asymptotic missing sources remain absent; this
packet does not supply them. Scientific status remains AUTHOR_SIDE/HOLD wherever
it already required qualified review or unresolved premises.

Falsifiers of this review: a different exact input set, a different pinned
consumer, a raw-file hash mismatch, disagreement with original loader selection,
or a source row demonstrating that the quoted angle-175 value is not its
last-wins rim record. Any such change requires a new receipt and source-bound
review, rather than inheriting this one automatically.
