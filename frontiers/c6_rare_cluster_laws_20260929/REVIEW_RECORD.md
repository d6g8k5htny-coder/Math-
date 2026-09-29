# Scoped review and repair record

Scientific effect NONE. This records external observations, not a self-issued acceptance or a register transition.

## Mathematical review B — accepted, source-exposed

Anthropic Claude review **5358565704**, submitted 29 September 2026 at 21:15:22Z:
https://github.com/d6g8k5htny-coder/Math-/pull/153#pullrequestreview-5358565704

Binding: commit `877f8825656ec41e4fd5a955225e0bf184ff3800`; PROOF.md blob `2ab625cedfc2e47575c4a7fa4853413418c532da`.

Accepted scope: Section 1 count/source interface and Sections 2, 5, 6, 7, as elementary implications of H1/H2/Hq at fixed d,L and compact positive gap marks. The reviewer checked the Palm/positive-law distinction, set-partition moments, weighted-l1 compactness, counterexamples and independent-replica coupling. The reviewer also replayed the initial packet and recomputed its two full premise identities from Git objects.

Exposure: the reviewer authored the consumed C6 and D5 sources; this does not independently revalidate those premises. All lanes use the same GitHub login; no organizational independence. This review does NOT accept Sections 3–4 in full or the later coefficient addendum. Those remain OPEN at this record. The original PROOF.md remains byte-identical; only additive mathematics and verification/provenance successors followed.

## Codex P2 — prior-credit identity omission

Review comment **4138392498** at the initial head:
https://github.com/d6g8k5htny-coder/Math-/pull/153#discussion_r4138392498

Root cause: source_identity iterated only SOURCE_PINS.sources, omitting the separately credited prior_in_project_result. Thus a wrong prior blob still yielded source_pins_checked=true.

Reproduced before repair using a real temporary local Git repository: test_prior_wrong_blob failed because ValueError was not raised. The verifier now checks the prior commit/path/blob as well as the full size/SHA256/blob premise identities. Six tests cover a valid fixture, wrong prior blob, wrong prior path, wrong prior commit, unsafe prior path and retained premise SHA256 validation. No network, mock subprocess or fabricated source is used as evidence about the actual project sources; fixtures only test verifier behavior.

Latest local standalone suite: 40 tests per Python mode, both successful. The source hashes of the actual project must still pass hosted replay at the repair commit; older successful runs do not automatically certify a successor. Thread resolution and hosted final evidence belong in the PR discussion after that replay.
