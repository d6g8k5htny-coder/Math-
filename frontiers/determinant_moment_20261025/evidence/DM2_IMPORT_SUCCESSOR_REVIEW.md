# DM2 import successor: nonauthor technical review

Signed 2026-10-25: OpenAI / GPT-6-Codex family / agent
`/root/dm2_statement_review`; exact underlying model identifier unavailable.
Author: OpenAI/Codex `/root`. Separate reviewer context, same provider,
original proof visible. Organizational-independence credit 0; acceptance credit
0; scientific effect NONE. This is not provider-distinct machine alignment.

## Frozen source

Reviewed repository `d6g8k5htny-coder/Math-`, commit
`dcfc89366f590342b4cd30b141a22c9ae2a562bb`. Paths below are relative to
`frontiers/determinant_moment_20261025/`.

| File | SHA256 |
|---|---|
| manifest.json | cb2b4870debf98cdf3663663797ccfc524e23d5f41f89e1c9ecdba5b6e680811 |
| ResearchFormalCoreR1/DeterminantMoment.lean | 661b73c3f21c6d2529f5e09ce426d89c01939ab27a5cc868db3802c7e66ea82d |
| ResearchFormalCoreR1/AlgebraV2.lean | 71e4327df9f7d6979f1467f7e0d880e0ab0a70ab6d234802d8c7a1624b9ce2d9 |
| ResearchFormalCoreR1/ProbabilityCompanionsV2.lean | dbc42b17797be688fecec790f32fcfd0004d98ac776cbbe0471c62c3f506aa41 |
| SOURCE_MAP.md | 32b5e48e9d8150927542718e719a71f6d59ef7593b78dd827dd52c18c47681f6 |
| SCOPE.md | c3cb56539a6b1dcb41c6ac378c1797e95ef878ba03276456276e0bb3abfa3ddd |
| tests/test_gate.py | b5fc1b723d5137d0a41ebb67b29e25da727edfad391d62afa6d44c32b5e114c6 |

All manifest-bound files were independently hashed; no mismatches were found.
The public source identity and exposure remain those explicitly recorded in
DM2_NONAUTHOR_REVIEW.md: the preserved P02-LM-002 export at base c4eabc1a,
not inspection of the primary Drive proofs or historical independent audits.
That original review note remains unchanged and pertains to its original bytes.
This note supplies the actual new source review rather than rebinding the old one.

## Dependency and preservation findings

No substantive source-alignment regression was found. Direct Git comparison
with `deb28a751f620715ec65d3bd73690905e6fee94d` shows that the only changes
to all three Lean modules are their initial import lines. Removing lines that
begin with `import ` yields identical remaining bytes, including every
definition, theorem statement, hypothesis, proof and namespace command.
The stripped-body SHA256 values are:

| Module | Non-import body SHA256 |
|---|---|
| AlgebraV2 | 50938dbae8a0d74220d0ae1e69a6bf1be3cda47eec44970d24457c0347d75ff3 |
| ProbabilityCompanionsV2 | 432ea418452a0ea49fcbb191026edc879981be97adecee0b836a1e41ae5882fe |
| DeterminantMoment | 843c04288e7943d97e80fc9e434c7ce36d7eda85a840320604af592dc8937fec |

All new direct imports are Mathlib modules under the same pinned dependency.
Algebra imports real basics and its field/ring/numerical tactics; probability
companions import real square root and their arithmetic tactics; DM2 imports
Bochner integration, matrix determinants/topology, ordered measurable groups
and its existing proof tactics. No local extra axiom or replacement mathematical
definition is introduced. These import changes alter the dependency closure;
they still require fresh replay and transitive axiom audit.

Gate.py, toolchain, lake dependency manifest, lake configuration and both false
DM2 fixtures were byte-compared with deb28a and are unchanged. The two baseline
preservation tests now require the exact narrow import lists and retain their
comparison of the entire remaining expected source against preserved originals
plus the previously documented historical compiler repairs. This is a bounded
test adjustment, not replacement of full-body preservation with theorem-name
or partial-text matching. The reviewed fixture witnesses remain mathematically
false for the reasons in the original signed note.

The exact matrices, all nine radius coordinates, quadratic-form indicator,
pointwise hypotheses and genuine eighth-moment integrability premises are
preserved. The arbitrary-measure expectation theorem remains a sound stronger
version of the public probability-law implication. The source's uniform-family
corollary still needs one common supplied M8. Concrete Gaussian moments, Palm
identification, lower normalizer, event coverage and parent results remain open.
The documentation accurately distinguishes this successor and its changed
imports from the historical baseline bytes and review. No full thirteen-target
baseline source alignment is independently certified here.

## Evidence inspected and limitations

This reviewer ran the revised Python test suite in both normal and optimized
modes: 78 tests passed in each. No competing compiler or checker was run.

The retained RED log reports exactly two failures. A precision caveat: it tests
precursor headers Mathlib.Data.Real.Basic and Mathlib.Data.Real.Sqrt, whereas
the final tests pin Mathlib.Basic.Real.Basic and Mathlib.Analysis.Real.Sqrt.
The retained first narrow-build log records the deprecation guidance for those
precursor names and an unsuccessful DM2 build; the second log records a
successful build using the final source. Thus RED is evidence for the initial
import-preservation change, not a literal replay of the final header strings.
This does not weaken the exact current-source comparisons or the independently
rerun passing tests. Future summaries should retain this distinction.

The preserved umbrella-build log and RESULT.txt report a successful original
build followed by checker exit 137, a 17179869184-byte cgroup limit, and one
OOM kill. The original checker log is empty. These are retained author-side
execution records; this reviewer did not independently observe that past cgroup
state. The successful final narrow-build log was inspected, but compilation
alone supplies neither full replay success nor alignment acceptance.

The final gate replay was ongoing when this review was requested. This note
does not claim its outcome, a fresh leanchecker pass, transitive axiom audit,
negative-control execution success, or hosted-check success. Those require
their actual separate evidence. The unchanged validator still requires distinct
provider/family/agent identities and full target coverage. This same-provider
bounded technical review cannot provide its machine ACCEPTED alignment record.

Only this new evidence note was written by this reviewer; production sources
and the original signed review were not edited.
