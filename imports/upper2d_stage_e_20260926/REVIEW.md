# Source-bound nonauthor review

Review date: 2026-09-26. Reviewer: OpenAI/Codex subagent, separate from the packet author in the same session and provider. **Organizational independence credit: 0. Scientific effect: NONE.** This is a bounded source and custody review; it grants no theorem acceptance, premise promotion, prize, or `lemma_closed` change.

The reviewer read the recovered sources and packet metadata without modifying any original source. The only authored file is this review. No numerical search or complete numerical-certificate script was run by the reviewer. A small isolated probe of the original `Isserlis` class and the standard-library custody verifier were run as described below. No posts or commits were made by this reviewer.

## Exact reviewed source identities

Paths are relative to this packet. SHA-256 values cover the complete file bytes.

| Path | SHA-256 |
|---|---|
| `raw/STAGE_E/attack_h4jc.py` | `4ae404d70659333d50d3dfee6c11df6b082b9797d893db1eef8a575128d64f5e` |
| `raw/STAGE_E/certify_axis_break.py` | `f9e0efefe442bc474201f7cf1951a526b09b344657ef3b1cbd300e7a143aeda8` |
| `raw/STAGE_E/isserlis_break.py` | `098adfe093f5bcd9a0ea463b77a6c3b4d1b234df028439174c9e82de9772e8d7` |
| `raw/STAGE_E/hunt_wedges.py` | `f03507da809d91eb6b358c4bf51298ba9d26bb6ab733e801cb5784394b96d48e` |
| `raw/STAGE_E/hunt_rim.py` | `de73e5fed00782c3709d2f9a8b1cddca23926606a8ef5ffc4cf0de8aefb66f90` |
| `raw/STAGE_E/t_attack_normal.txt` | `bc9bcca0297cf03169f28d251c42a0211b8c50685b36824aaef2cd52defe1dd6` |
| `raw/STAGE_E/t_attack_O.txt` | `bc9bcca0297cf03169f28d251c42a0211b8c50685b36824aaef2cd52defe1dd6` |
| `raw/B1_taxonomy/b1_falsifier.py` | `818df7985412071259345455c9ff6b68cad0c0fa9d636009cf8849b550154185` |
| `raw/C1_alpha_intensity/c1_grid.py` | `2ebe6eb47ee3554b3257342b726d9990009793a66994c9e53fffdc13f70705e0` |
| `raw/H2_foundations/cov_exact.py` | `f08c1c5f653f2ffd2e85d39e1112f80d15db04d15f932e5ee42db2ca3553e783` |
| `raw/H2_foundations/pin_transform.py` | `c6988ac7fcfa32dcc03c1374e13fb4c26af1c12c25cb824a315e6dce8991fd41` |

All 11 packet files, totaling 109,342 bytes, were compared byte for byte with the recovery workspace and matched. The B1 and covariance hashes match the hardcoded pins in the Stage E scripts. Remote source IDs and Dropbox paths are the packet author's recovery metadata; this reviewer did not independently query Dropbox.

## Execution and dependency scope

The reviewed originals contain no visible network calls, subprocess launches, deletion operations, or explicit file writes. This is a source inspection, not an audit of installed third-party packages. Imports change `sys.path`, numerical precision, caches, and in the hunt scripts `c1_grid.chol_np`. All five Stage E scripts execute work on import; the hunt scripts can allocate large arrays and run lengthy searches. Normal Python imports can write bytecode caches unless disabled.

The discrete attack uses Python's standard library and the pinned B1 file. The four numerical scripts use `C1_alpha_intensity/c1_grid.py`, which imports both `H2_foundations/cov_exact.py` and `H2_foundations/pin_transform.py`. Their third-party dependency set is NumPy, SciPy, mpmath, and SymPy. Package versions are not locked in this packet. `hunt_wedges.py` additionally reads `H5_closure/h5_results_*.jsonl`; those ledgers are absent. `hunt_rim.py` and the numerical certificate scripts embed H5 constants whose supporting ledgers/certificates are not supplied here.

## Discrete witness and replay

The executable model is a 40-by-40, six-neighbor triangulated torus with lexicographic `(binary-floating-point height, vertex index)` keys. Its quiet witness has one window saddle counted by both implemented predicates, producing `N_qual + N_loop = 2 > N_w = 1`. The quiet and T2 witnesses use the same construction. The ensemble uses fixed uniform-coefficient Fourier fields and planted ridges; it is not the side-24 Gaussian continuum ensemble used by the numerical library.

The packet author's fresh CPython 3.12.14 normal and optimized runs are recorded in `REPLAY.json` with zero exit codes and the same 1,025-byte stdout as both historical transcripts. This reviewer inspected that receipt and the historical bytes, without independently rerunning the complete attack. The transcript reports 427 audited pairs, 175 A-pairs, 132 inequality violations, and 1,612 two-cluster checks. Its printed internal digest is `51b2bd7c078aef92d1992d43b04c10454f23af0c760716e0674bbc4274987dbf`; this is distinct from the full-transcript SHA-256 above.

These results support reproducibility of the historical discrete predicates and witness. They do not establish a Gaussian continuum counterexample, Gaussian failure probability, Palm rate, or result about a repaired successor. Full H4/C2/D2 target texts are not included, so this review does not independently establish that the code's quoted/reimplemented predicates faithfully reproduce every hypothesis of those texts. Finite sample checks alone also do not certify the script's universal or continuum comments.

## Established execution defect

`isserlis_break.py` constructs `S_iv` as a list of lists at line 158 and passes it to `Isserlis` at line 159. `Isserlis.__init__` indexes `Sigma[i, j]` at line 85. Python lists reject that tuple index.

The reviewer parsed the original file, extracted only its `Isserlis` class with the standard-library AST module, executed that class definition in isolation, and called `Isserlis([0], [[0]])`. It raised:

```text
TypeError: list indices must be integers or slices, not tuple
```

This is a reproduced interface defect in the original class and the original call site. The complete script was not run; it might encounter an earlier dependency or numerical failure. If execution reaches the displayed call, this defect prevents completion and the printed certification verdict.

The packet author separately reported the same exception from the exact AST-extracted class with a nine-component zero mean and a nested-list 9-by-9 identity covariance. That probe also avoided all top-level script execution.

## Numerical certification concerns requiring further work

The following source findings block adoption of the numerical certification labels. They do not quantify the actual numerical error or settle the truth of the intended H5 envelope claim.

- `c1_grid.py` explicitly describes a diagnostic display. Its covariance assembly uses the `spectral`, `mpf` path (line 73), takes midpoints of pin-inverse intervals (lines 61-64), and performs subsequent conditioning in ordinary multiprecision arithmetic. `cov_exact.py` itself describes its `mpf` path alone as diagnostic grade. The numerical wrappers do not propagate complete interval uncertainty through this chain. Repeated precision calculations and heuristic safety factors do not supply a demonstrated end-to-end enclosure.
- `certify_axis_break.py` constructs determinant-box endpoints through `float` conversion (lines 145-146). Its nominal station quantities and margins lack enclosing intervals; rounding to a shorter decimal string also enters tail bounds. Its header describes a different safety scale from the code. The extra `s_t_lo` in `I_lo` (line 186) is inconsistent with the standardized-normal integration used by `c1_grid.rho_station` (lines 163-173). Whether this extra factor is conservative at the chosen point requires a separate justified calculation.
- `isserlis_break.py` likewise uses rounded float endpoints and treats approximate station means/covariances as point inputs. Its degree-six polynomial mean-shift correction sums only degrees 1, 2, and 3 (lines 173-194). The source supplies no cancellation proof or explicit bound for degrees 4, 5, and 6; a factor-four allowance alone does not establish one. This is an unresolved bound obligation, not a demonstrated numerical counterexample to the intended bound.
- The `isserlis_break.py` precision comparison constructs base objects at 120 and 160 digits, then resets the active precision to 120 before both station calculations (lines 231-252). It compares only `pgrad`, `mu_t`, and `s_t2`. This does not demonstrate two fully independent precision evaluations of every quantity consumed by the certificate.
- Both hunt scripts replace failed Cholesky factorization with eigenvalue clipping at a floor proportional to `1e-13`, changing the covariance used for sampling. Their deterministic QMC and finite quadrature outputs are exploratory estimates, not rigorous envelope certificates.

Accordingly, original `CERTIFIED`, `PASS`, and theorem-falsification labels are preserved only as historical text. No fresh numerical-certificate replay is claimed.

## Packet review and disposition

The README correctly limits the import to historical recovery, identifies absent H5 ledgers and unlocked numerical dependencies, states the finite replay scope, and records zero organizational-independence credit. Its corrected CPython version, 3.12.14, matches `REPLAY.json`.

The reviewer ran this packet's `verify.py` with `python -B -S`, using the absolute script path. It exited zero with:

```text
CUSTODY VERIFIED: 11 raw files; scientific effect NONE; no numerical certification
```

The verifier is standard-library-only, checks the exact raw inventory, rejects unsafe paths and symlink components, and recomputes byte counts, ordinary SHA-256, Dropbox content hashes, and Git blob SHA-1 identities. It does not import the mathematics. It establishes local consistency with the manifest; it does not independently authenticate remote provenance, replay the attack, validate narrative claims, or endorse historical labels. The four-tree/source-manifest absence statement remains the packet author's explicitly bounded comparison, not a search independently repeated by this reviewer.

The packet author additionally reported verifier success in optimized mode and rejection of a mutated raw attack file in a temporary packet copy. Those two checks were not independently repeated by this reviewer.

Reviewed supporting-file SHA-256 values:

| File | SHA-256 |
|---|---|
| `MANIFEST.json` | `0d167bdc2e6fa02e49aaeafe0d4ea06f21608d717030f80315aa042d14849a16` |
| `REPLAY.json` | `1348652593a79f5f7afa45da241ee0e6d503d7fd22082b4ed4b7acb6ed7897c6` |
| `verify.py` | `81846a8f4d383746002971970dbbbe8b77c4568ef5a80858b0ff1ce67ca12fa6` |

Disposition: suitable for an explicitly qualified historical source-custody import with scientific effect NONE. Numerical certification remains unaccepted, and organizational independence credit remains zero.
