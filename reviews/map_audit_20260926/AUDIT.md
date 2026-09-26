# Cross-model audit of lemma/theorem maps — 26 September 2026

Scientific effect: **NONE**. This note records independent map audits. It does not flip `lemma_closed`, prizes, or premises.

## Auditors

| Lane | Agent | Scope | Verdict |
|---|---|---|---|
| GPT | [GPT audit closed theorems](bc-9c963ad4-7ad8-5b6e-8e5a-e7bd14342d7e) | `closed-theorems/` + `open-theorems/` | **PASS_WITH_FIXES** (applied) |
| Claude Opus | [Claude audit closed lemmas](bc-08757cc3-314a-556c-8d5c-7284be1c5bbb) | `closed-lemmas/` | **PASS_WITH_FIXES** (applied) |
| Grok | [Grok audit open gaps](bc-e9a4702c-3b6d-5def-aa1c-33b962ff4f7a) | `open-lemmas/` + cross-map gaps | pending at this note’s last update |

## GPT findings applied

1. Link immutable transverse proof identity (`32b80ee…`, SHA256 `f64c…e36`); tip lacks the author path.
2. Restore d=2 / `B<∞` / fixed-`L` / mark compacta on annulus and transverse statements.
3. Correct axial density notation to `p_{grad f(X)}(0)`.
4. Refresh P15 postures from Math- [#39](https://github.com/d6g8k5htny-coder/Math-/issues/39) (P1–P5 ACCEPT; hazard still open).
5. Refresh SIDE24 postures from Math- [#40](https://github.com/d6g8k5htny-coder/Math-/issues/40) (C1–C5 VERIFIED).
6. Remove duplicate open theorem `T-PERIODIZED-SIDE24-FULL`; keep parent under `T-GLOBAL-ELDER-LIFETIME`.
7. Soften intermediate-belt as RN-complete / RN-UNIF blocker once fixed-annulus accepts are consumed; keep mesoscopic/collision holes.
8. Clarify matching lower bounds: remote already has positive expected-count asymptotic.

## Claude findings applied

1. Vendor `reviews/collision_mechanism_20260925/` from `origin/main` so contact / D1 / D2 proofs exist on this branch (`NOTE.md` `530dd3ef…`, companion `83f65339…`).
2. Relabel SIDE24 as C1–C5 closed with parent still open (not a lifetime closure).
3. Clarify two-scale chart (`δ≤δ₀`, not fixed `ε`) and three-Hessian PR16 vs PR28 forms.
4. Fix contact-kernel scope to Sections B–C; cross-link typed-cubic; add missing `L-D1-DENSITY`.
5. Point D2 closed lemma at the companion correction; narrow open bookkeeping to optional in-place `NOTE.md` merge.

Local digest recompute on tip matched every primary vendored proof SHA256 cited in the maps.
