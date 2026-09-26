# Cross-model audit of lemma/theorem maps — 26 September 2026

Scientific effect: **NONE**. This note records independent map audits. It does not flip `lemma_closed`, prizes, or premises.

## Auditors

| Lane | Agent | Scope | Verdict |
|---|---|---|---|
| GPT | [GPT audit closed theorems](bc-9c963ad4-7ad8-5b6e-8e5a-e7bd14342d7e) | `closed-theorems/` + `open-theorems/` | **PASS_WITH_FIXES** (applied below) |
| Claude Opus | [Claude audit closed lemmas](bc-08757cc3-314a-556c-8d5c-7284be1c5bbb) | `closed-lemmas/` | pending at this note’s first write |
| Grok | [Grok audit open gaps](bc-e9a4702c-3b6d-5def-aa1c-33b962ff4f7a) | `open-lemmas/` + cross-map gaps | pending at this note’s first write |

## GPT findings applied

1. Link immutable transverse proof identity (`32b80ee…`, SHA256 `f64c…e36`); tip lacks the author path.
2. Restore d=2 / `B<∞` / fixed-`L` / mark compacta on annulus and transverse statements.
3. Correct axial density notation to `p_{grad f(X)}(0)`.
4. Refresh P15 postures from Math- [#39](https://github.com/d6g8k5htny-coder/Math-/issues/39) (P1–P5 ACCEPT; hazard still open).
5. Refresh SIDE24 postures from Math- [#40](https://github.com/d6g8k5htny-coder/Math-/issues/40) (C1–C5 VERIFIED).
6. Remove duplicate open theorem `T-PERIODIZED-SIDE24-FULL`; keep parent under `T-GLOBAL-ELDER-LIFETIME`.
7. Soften intermediate-belt as RN-complete / RN-UNIF blocker once fixed-annulus accepts are consumed; keep mesoscopic/collision holes.
8. Clarify matching lower bounds: remote already has positive expected-count asymptotic.

Local digest recompute on tip matched every primary vendored proof SHA256 cited in the maps.
