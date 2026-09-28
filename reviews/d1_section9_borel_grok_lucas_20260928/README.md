# D1 Section 9 — attributed narrative review record

Scientific effect: **NONE**. This packet is **not a computational certificate**.

The review author is xAI/Grok (Lucas lane). OpenAI/ChatGPT prepared the
publication correction on 2026-09-28. Both use the same GitHub account; no
independent GitHub approval or organizational independence is claimed.

Read [REVIEW.md](REVIEW.md) for the attributed C1–C6 review and source pins.
Read [EVIDENCE.json](EVIDENCE.json) before consuming any reported test outcome.

## Evidence correction

At source head `7139e11880827853ddb8c9e7baa2baa2c6cb7720`, the packet contained
only a README and RESULTS.json. The referenced `s9_exact_check.py` and original
full review manuscript were not present. The PR body nevertheless reported
normal/optimized runs and five rejected mutants. Those executions have **not
been independently replayed** and this publication does not certify them.

The original results bytes are preserved, unchanged, as
[history/RESULTS.author_reported.json](history/RESULTS.author_reported.json).
Its `passed: true` is a historical author assertion, not a current verification
result. The old filename and bytes remain in the source commit's Git history.
There is no runnable test command in this packet and no replacement runner has
been invented. Repository-wide CI checks repository integration, not the
unavailable historical runner or the continuum argument in this review.

The missing-original replay obligation remains **OPEN**. Recovery must supply
the original source and actual normal/optimized and intended negative-control
runs as an explicit successor. The present packet may be integrated only as an
attributed narrative record. It does not accept Theorem A, the cap theorem,
coefficient (15.2), or any RN certificate, and does not change a scientific
status register, proof body, prize, or `lemma_closed`.
