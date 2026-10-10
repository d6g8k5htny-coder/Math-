# Compact source cutoff portable baseline

This source package preserves the 27-module compact-cutoff input graph and provides a separately named diagnostic fixture for hosted reproduction. The default target is `PushedHeight`: its predecessor graph contains 26 original modules and 504,047 source bytes. The registered original `CompactSourceCutoff` target is outside the default build.

The 27 inherited source files total 509,962 bytes and are copied unchanged from the registered `SOURCE_INPUTS.json` inventory (13,221 bytes; SHA-256 `c7febb8e99ee17481b72678ab03fe839ef50773fb96529c404cced3eb9ba0fb1`). `SOURCE_MANIFEST.json` binds every module, byte length, digest and import without publishing private source paths. `SOURCE_SHA256SUMS` binds all 35 other package files.

`CompactSourceCutoff.lean` is preserved at 5,915 bytes with SHA-256 `a8abb169acb74c7ac11396b956bb5e055fd30f98af4ca0c0fb1f91ea06375f86`. `CompactSourceCutoffTargetRed.lean` is a separate 5,936-byte diagnostic with SHA-256 `6d85955aab50429251c441358a26f4cb6e670ea8f6560b5caaf026d697ede0cd`: it inserts exactly `open MorseCongruence` plus LF after original line 8. Removing candidate line 9 restores the original bytes. The fixture imports the same predecessors, does not import the original target, and retains both empty proofs and all original witnesses, premises and mathematical statements. It supplies no proof implementation. See `TARGET_TRANSFORMATION.json`.

Lean is pinned to `leanprover/lean4:v4.34.1`. The parent nine-record project dependency manifest is preserved with only its root name changed from `ordinary_h0_elder` to `compact_source_cutoff_baseline`. The exact revisions are:

- `plausible`: `118aa17ee84656b8bd727fef7c458ee8c833385c`
- `LeanSearchClient`: `ddf04cf3949fa556442341e87d47f9f6e6074707`
- `importGraph`: `e928b72544873815af278d38681b31c0293588e3`
- `proofwidgets`: `106ff4fafc74ef4ac99d81dbf3ab399118f497a5`
- `aesop`: `355695d523e41d0554926416cba2a2b3544fbbc9`
- `Qq`: `6a489d9af5d0c47e5b259e2e8bcdfc1811b5a259`
- `batteries`: `f2effa3d803fda822b1f97b806c47cf2adfbcbc2`
- `Cli`: `e92c9f15fdfacc8536f31cfb3b7ad26c3c8cd204`
- `mathlib`: `d13f23b723b8a846827a245b89c10fc7d3f11612`

The following commands are intended for an authorized hosted runner, from this package directory, and were NOT_RUN during assembly:

```sh
sha256sum -c SOURCE_SHA256SUMS
lake exe cache get
lake build PushedHeight
lake env lean CompactSourceCutoff.lean
lake env lean CompactSourceCutoffTargetRed.lean
```

The hosted workflow must record the original target diagnostic's actual exit status and retain its output. The namespace diagnostic fixture's actual nonzero status must fail CI. A green setup or predecessor step supplies no proof of either compact-cutoff target. These are prospective workflow requirements; no target exit status has been observed in this assembly.

NONCLAIMS: package assembly establishes static source custody and reversible transformation only. All compiler, Lake, dependency retrieval, project tests and hosted execution are NOT_RUN here. The original and diagnostic targets retain unresolved empty proofs. A future successful predecessor build would establish build evidence for that exact graph and revision only; it would not establish the original formal lane's full kernel/checker, transitive axiom audit, negative controls, receipt binding or alignment acceptance. This package makes no scientific promotion, theorem completion, human-review, blind-review or organizational-independence claim.
