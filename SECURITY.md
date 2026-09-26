# Security policy

Scientific effect: **NONE**. This policy covers repository automation and verification tooling; security fixes do not accept mathematical claims.

## Private disclosure

Use the [private vulnerability reporting address](https://github.com/d6g8k5htny-coder/Math-/security/advisories/new) to contact this repository's owner and maintainers. Private reporting was enabled and read back on 2026-09-26. Do not publish secrets, private sources, personal data, or exploitable details in an issue.

Include the exact commit and path, a minimal inert reproduction, affected behavior, and expected impact. Do not access other people's data or run destructive tests. No response-time guarantee or bounty is implied.

## Scope and maintenance

Report against the current default branch, identifying affected historical pins. Preserve historical source and review artifacts; publish separately identified successors. Mathematical counterexamples and proof concerns belong in [public research issues](https://github.com/d6g8k5htny-coder/Math-/issues), with exact hypotheses and source identity, unless the report exposes a security vulnerability.

The owner controls vault writes and merges. Outsiders may read, fork, and propose changes; public visibility and CODEOWNERS do not grant write access. Required PR checks and exact-source nonauthor review remain distinct from scientific acceptance. Same-provider review receives no organizational-independence credit. Zero required GitHub approvals avoids a second-account deadlock; it does not waive theorem-specific review predicates.

Secret scanning and push protection are enabled. They cannot prove that all secrets or malicious content are absent. Dependabot proposes weekly GitHub Actions updates only; existing verification gates still apply. No CodeQL workflow, funding configuration, or new license terms are introduced here.

The [public shop setup](https://github.com/d6g8k5htny-coder/main/blob/main/docs/PUBLIC_SHOP_SETUP.md) records repository controls and owner account-security steps.
