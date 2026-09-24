# Math — research candidates and reproducible calculations

This repository now hosts mathematical deliverables for Dylan Roy's research workspace. The prior README-only shell is superseded by the owner's 24 September 2026 instruction to use the expanded repository set to advance the project.

## Current deliverable

[The SIDE24 coefficient in dimensions two and three](coefficients/side24_v1/PROOF.md) evaluates the expression in [main issue63](https://github.com/d6g8k5htny-coder/main/issues/63), with exact reference cone moments, a uniform bound for all periodic images, and outward rational numerical bounds. The parent's global lifetime theorem remains an author-side candidate awaiting nonauthor review.

```sh
cd coefficients/side24_v1
python -B -S coefficient.py
python -B -S -m unittest -v test_coefficient
python -B -O -S -m unittest -v test_coefficient
```

No third-party dependency is needed. [ENCLOSURE.json](coefficients/side24_v1/ENCLOSURE.json) is an output to reproduce, not a mathematical acceptance record.

## Repository boundaries

`main` retains the research campaign, source-linked claim discussion and integration decisions. This repository owns its candidate proofs/code; it does not duplicate the scientific-status registers. `google-drive` carries selected byte-identified public evidence replicas; `meta-framework` carries routing metadata; `query-` provides read-only source lookup; `trial` tests integration; private experiments stay in `sandbox`. `governance-` describes the working contract.

Use exact parent identities, state the scope of each result, preserve failed evidence and coordinate overlapping paths. A merge publishes a candidate; a passing test verifies only its stated test scope. Neither constitutes independent analytic acceptance. Older blanket never-main and empty-by-design language is not a veto on the owner's current instruction. Repository visibility and source privacy are not changed by this update.
