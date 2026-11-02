# Input provenance and package mapping

The 13 source modules are exact byte copies of the source package at repository `d6g8k5htny-coder/Math-`, commit `57ddbd6ba39340049afe0ecca99808c934e10584`, path `frontiers/source_smooth_realization_20261011/` (Math PR 468 source identity). The original `lakefile.toml`, `lake-manifest.json`, and `lean-toolchain` are preserved here with `source-` filenames. Their expected Git blobs and SHA-256 digests are recorded in `FILE_IDENTITIES.json`.

The unchanged `Lifetime.lean` target snapshot is identified by commit `dc7aca2f9adaf6d6d986b0e34b7b39c8fc3cf417`, blob `f2508f7f2e3fd42f22f5aa52bc5ead5ff9e73b9a`, and SHA-256 `90f4892608e953ecc696bb32ea159d1c178ceb8a1c6edfd11acfceb14af462c6`. Its original repository path is `specifications/lean_statements_20261010/Specifications/Lifetime.lean`; the current default-tree preflight retains the same blob. The proof imports the local module named `Lifetime`.

The original source metadata files named `SOURCE_MANIFEST.json` and `SOURCE_SHA256SUMS` are not used as current build receipts. Earlier recovered metadata differed from the later source publication metadata while every included Lean source and build-configuration blob matched. This package records exact included-file identities directly, without importing historical status claims.

The active package name is `source_lifetime_realization`; the original name was `source_smooth_realization`. Only that top-level field is adapted in the active dependency manifest. No dependency pin, URL, inherited flag, or other package entry is changed.

The `C291Inputs` library maps all original module names and `Lifetime` to `inputs/`. `srcDir` and explicit `roots` are supported by the pinned Lean 4.34.1 Lake sources. Relative to the Lake source root these are `Lake/Config/LeanLibConfig.lean` (fields), `Lake/Config/LeanLib.lean` (directory resolution), and `Lake/Load/Toml.lean` (library configuration decoder), with corresponding `lean_lib` documentation in `README.md`. This layout needs no `C291Inputs.lean` root file because the roots are explicitly supplied. Static inspection of those sources supports the mapping; it is separate from executing Lake on the package.

The five new proof, control, and audit files are copied from the exact source bytes associated with their successful development receipts. The public receipt summary omits machine paths and process identifiers, names the original run IDs, and hashes the original receipt files; it is a derived summary, not a byte-identical original receipt. No compiled object is included.
