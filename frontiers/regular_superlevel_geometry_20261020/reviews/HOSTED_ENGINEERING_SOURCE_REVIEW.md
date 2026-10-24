# C297 hosted engineering source review

**`PASS_SCOPED_ENGINEERING_SOURCE` — no unresolved publication-blocking finding in the final reviewed bytes.** This approves the verifier's source design for the stated scope; it does not claim hosted execution or formal acceptance.

Actual reviewer: OpenAI Codex `/root/c292_geometry_review`, delegated work for Dylan Roy. This is same-provider, source-exposed nonauthor engineering review, with organizational independence 0 and human review 0. Prior exposure includes C292–C295 reviews, C294 proof-shape advice, C297 topology/control advice, and the C297 proof-source reviews. The reviewer did not author the hosted verifier, its test module, or its workflow. The reviewer identified the multiline audit-output issue below and reviewed the author's correction.

The relative links in the following table address the published packet layout. These exact files were reviewed in the working directory's `hosted/` staging area and rehashed at the end of the review.

| Reviewed artifact | Bytes | SHA-256 |
|---|---:|---|
| [c297_hosted_verify.py](../c297_hosted_verify.py) | 25,481 | `fefd7500e698d75c60cc907c3b679a498e598a4c235f3b3e7fe2e1102502e217` |
| [test_c297_hosted_verify.py](../test_c297_hosted_verify.py) | 10,784 | `8510b0fca398f75dc28dd35bae5ab7c6f6d2735c74b453d2c93c0606b4c3df28` |
| `c297-regular-superlevel.yml` (published at `.github/workflows/c297-regular-superlevel.yml`) | 3,129 | `03b3d8fb4ca95316247b93ad3937ea2d56f0509040c819534873be1bb341eab3` |

The concrete blocker found during review is **closed**: the original physical-line audit parser rejected valid wrapped axiom arrays emitted by pinned Lean. I checked actual retained C294 examples, read the failing regression, reviewed the logical-record replacement, and read the subsequent normal and optimized nine-test results. The replacement preserves rejection of interrupted/truncated records, malformed records, duplicate declarations, forbidden axioms, and missing required targets.

The final implementation matches the requested execution contract:

- **Five fresh builds:** an initially absent local object directory, ordered builds of Lifetime, peer chart, topology, literal consumer, and audit.
- **Four standard kernel replays:** peer chart, topology, literal consumer, and audit; no claim of fresh import-closure replay.
- **Complete four-module census:** all declaration records are parsed, module counts and total must agree, all 17 required targets must occur, and axioms are restricted to the three standard names.
- **Two negatives:** exact omitted-premise invocation and diagnostic checks, not merely exit-code checks. Overall success requires semantic validation of both.
- **Source/object stability:** hashes are checked before and after verification; existing local objects cannot change, builds may add only their own permitted outputs, and replay/control phases cannot alter the inventory.
- **Failure evidence:** handled process failures and timeouts retain binary streams and receipts. Completed object/control metadata is saved consistently in phase and aggregate records. Timeout handling tolerates the process-exit/kill race.
- **Workflow:** commit-pinned actions, `contents: read`, checkout credentials disabled, bounded timeouts, and an always-run artifact upload. Tested commit/tree, PR head/base context, run/attempt, actual runtime binaries, and dependency pins are recorded.

I independently matched the workflow's manifest digest, **`c339a9d1ca5b9ef70f8d581ea0760f11922aba2cd16cbeeb7aba02092b476e94`**, to the 1,539-byte local [manifest](../HOSTED_SOURCE_MANIFEST.json) and verified all seven file bindings against the reviewed sources.

For interpreting future evidence, a phase-level `PASS` initially records the expected process/object outcome. Negative acceptance additionally requires `intended_missing_premise_rejection: true` and the aggregate final success status. Remote source-origin equality and full dependency-artifact custody remain separately scoped owner checks, as the verifier states.

The retained engineering records read during review include `TEST_WRAPPED_RED.*`, `TEST_WRAPPED_GREEN.*`, and `TEST_WRAPPED_OPTIMIZED.*`, plus `C294_WRAPPED_OUTPUT_CHARACTERIZATION.json`. The latter records a marker-prefix-only projection of the retained C294 audit stdout, SHA-256 `062a8168ad5b05f1238ea8fd516d7fc5a806941cf77480b6de6837921c294386`, and an author-performed parser check covering its 235 declarations. This is reuse of existing output to characterize the engineering parser, not a new Lean run or a C297 census result.

## C296-N1 dependency boundary

A later coordination update supplied by the root reports a separate native review, ID `5584579361`, and [Math488 comment `6290185439`](https://github.com/d6g8k5htny-coder/Math-/pull/488#issuecomment-6290185439), with disposition `AMEND_SCOPED` for C296-N1 at peer head `72edcf5b93be45c29f2d10a26f7d8e861a48f528`. The reported finding concerns the peer workflow's negative classifier accepting some token-containing syntax, setup, or resource failures. The update reports that the actual hosted negative was the intended type mismatch and that the mathematical/interface source was clean.

This paragraph attributes that coordination update; this reviewer did not independently reread or reproduce the separate native finding and does not supply the peer's approval or fix. It does not convert the C296 peer PR into a blanket accepted dependency.

C297 consumes the exact `RegularPointChart.lean` proof source, 2,767 bytes, SHA-256 `5568c8d6e03f7064cd5924ebe2814ae746100505ae31789d5c975902528f9fa2`. It does not consume the peer workflow or negative classifier. The C297 verifier's own two controls use the stricter invocation and diagnostic checks reviewed above, and the C297 execution contract rebuilds and replays the chart module. C296-N1 remains with its existing reviewer and source owner; no takeover or duplicate repair is implied.

## Reviewer actions and limits

Same-provider, source-exposed nonauthor engineering review, **org0/human0**. I read retained test records but ran no tests, Lean, hosted execution, or remote action, and edited no implementation files. The only subsequent reviewer write was this authorized review record, preserving the substantive engineering verdict and adding the explicitly attributed dependency caveat.

This is source-bound engineering review. Actual hosted outcomes, downloaded artifact equality, final formal acceptance, source custody, and scientific acceptance remain separate gates.
