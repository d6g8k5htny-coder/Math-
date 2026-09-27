# Cross-repository coordination — formal verification lane

**Object:** MATH-FORMAL-LANE-COORDINATION-20260927-v1. **Scientific effect: NONE.**
Audience: every current and future agent working in `main`, `governance-`, `trial`, `meta-framework`, `query-`, `google-drive`, `sandbox`, and this repository, regardless of provider.

## Owner instruction (provenance)

On 27 September 2026 the owner, Dylan Roy, directed through a Cursor cloud-agent task on `Math-` that the verification stack be extended with a formal (Lean 4 + Mathlib) layer, following an external roadmap he supplied ("Keep the existing system intact … add a formal verification layer … extend the hard gate … glossary … formalization review lane … CI integration … AI-prover cross-check … external validation"). The instruction included: *"Be sure to coordinate with all other agents and future agents for all repositories so they will be aware of the changes and why, I Dylan Roy pre approve any decision, request, or action needed to achieve this goal."*

Under the [working contract](https://github.com/d6g8k5htny-coder/governance-/blob/main/README.md) this pre-approval covers the engineering and process work below. It does **not** and cannot flip a scientific register: `lemma_closed`, prizes, premises and landing dispositions move only through their existing authorities. Do not ask the owner to re-approve what is written here.

## What landed in `Math-` (this PR)

| Item | Path | Status |
|---|---|---|
| Layer 1 design and rules | [`formalization/README.md`](README.md) | live |
| Registry keyed by landing `claim_id` | [`formalization/FORMALIZATION_STATUS.json`](FORMALIZATION_STATUS.json) | live; all 10 claims covered; pilot `side24-coefficient` at `specified` |
| Fail-closed gate + 49 negative controls | [`formalization/formal_gate.py`](formal_gate.py), [`formalization/test_formal_gate.py`](test_formal_gate.py), [`formalization/FORMAL_RESULTS.json`](FORMAL_RESULTS.json) | live |
| Core-only Lean package (kernel-checked arithmetic, 36 theorems, standard axioms only) | [`formalization/lean/core`](lean/core) | live |
| Mathlib package (definitions, `Prop` specifications, 8 real-number theorems incl. the SIDE24 skeleton implication) | [`formalization/lean/mathlib`](lean/mathlib) | live |
| Glossary: project terms → standard mathematics → Lean carriers | [`formalization/GLOSSARY.md`](GLOSSARY.md) | live; extend per PR |
| Formalization (alignment) review lane template | [`formalization/ALIGNMENT_REVIEW_TEMPLATE.md`](ALIGNMENT_REVIEW_TEMPLATE.md) | live; first review open |
| CI: registry gate, kernel build + `leanchecker` + `nanoda` + axiom audit (core), Mathlib build + axiom audit | [`.github/workflows/formalization-lane.yml`](../.github/workflows/formalization-lane.yml) | live |
| Read-only index of the companion `formal/` packet (PR #92): its gate must pass, toolchain/Mathlib pins must agree | `companion_packages` in [`FORMALIZATION_STATUS.json`](FORMALIZATION_STATUS.json) | live |

Layer 0 is byte-identical: no edit to `claims/LANDING_CLAIMS.json`, `frontiers/downstream_gate_20260925/**`, any proof text, or any review record. `formal/**` (PR #92) is also byte-identical.

## Relationship to the `formal/` packet (PR #92, same day)

While this lane was being built, [PR #92](https://github.com/d6g8k5htny-coder/Math-/pull/92) (ChatGPT lineage, owner directive 2026-09-27, [main #95](https://github.com/d6g8k5htny-coder/main/issues/95)) merged a closed Lake package `ResearchFormalCoreR1` under `formal/` with its own manifest, gate, negative controls, Blueprint stub and workflow. Its 13 targets are scalar companions to GP-FOR-192 items; its gate requires every `.lean` under `formal/` to be registered in `formal/manifest.json`. This lane originally lived at `formal/` too and was relocated to `formalization/` so that neither gate has to be edited for the other to pass. Decisions, so every agent applies them the same way:

- `formal/` is owned by its manifest and gate. Do not add, move or edit files there from this lane. Do not re-pin its manifest for it.
- `formalization/FORMALIZATION_STATUS.json` indexes `formal/` under `companion_packages` **read-only**: `formal_gate.py` runs `formal/gate.py`, requires `SOURCE_IDENTITY_PASS`, requires both lanes' `lean-toolchain` and Mathlib commit to agree, scans the companion's registered modules for `sorry`/`native_decide`/`axiom`/`implemented_by`/`extern`, and refuses if the companion manifest self-declares alignment acceptance. Nothing under `formal/` counts as evidence for a landing `claim_id`.
- Toolchain or Mathlib bumps land in **both** directories in one PR, or `formalization-lane.yml` fails. That is the intended coordination point; do not silence it by removing the companion index.
- The two glossaries stay separate and complementary (GP-FOR-192 scalar vocabulary in `formal/GLOSSARY.md`; landing-claim families here). Both use the rule "a missing mapping is a formalization obligation, not evidence of novelty or ill-definition". Consolidation is a change to `formal/GLOSSARY.md` plus its manifest pin by that lane's author, with a pointer here.
- The two alignment-review mechanisms differ in form (`formal/gate.py --alignment <record>` with a lineage-independent author/reviewer pair and authenticated evidence hash; this lane's `reviews/` record checked by `_validate_alignment`) but agree in substance: kernel acceptance is not review acceptance; the reviewer must be a distinct agent; neither changes a scientific register. A future common review-record schema is a `governance-` amendment (request 2 below), not a unilateral edit in either lane.

## Why

The existing stack proves *identity* (hashes, blobs), *scope* (domains, "does not claim"), and *process* (review status, fail-closed promotion). It does not prove *logical correctness*. The Lean kernel supplies that for whatever statement is written in Lean; the alignment lane checks that the written statement is the intended one; the registry binds both to the exact informal blob so the checked artifact is provably the one advertised. The governance contract already anticipated this separation ("CAS/SMT/proof-assistant output verifies its encoded statement at its actual trust boundary; translation fidelity and imported hypotheses still require their own review"); the lane implements it.

## Requests to sibling repositories

This run's write scope is `Math-` only (Cloud Agent tokens follow the launch environment; pushes to siblings return 403). The items below are therefore **requests recorded here**, pre-approved by the owner, for the next agent with write access to each repository. Each is one bounded step; claim it in the `governance-` work-lease ledger before starting, and link back to this file by commit.

### `governance-`
1. Add a process amendment `amendments/20260927-math-formal-lane.md` summarizing: the four-value `status` vocabulary, the alignment review lane, the rule that kernel acceptance is non-discharge for the informal claim, and the pin-refresh rule for `formalization/**` (mirror of the existing "Math- exact-replay source identities" amendment).
2. In `REVIEW_TOPOLOGY.md` (next amendment), add "formalization alignment review" as a named review kind whose reviewer must be a distinct agent/session from the Lean author, with organizational independence assessed exactly as for analytic review.
3. Add the alignment review of `side24-coefficient` to the reciprocal-review pool: a nonauthor agent (not the Cursor/Anthropic session that wrote the Lean) reads [`formalization/lean/mathlib/MathFormalReal/Side24/Statement.lean`](lean/mathlib/MathFormalReal/Side24/Statement.lean) and [`Arithmetic.lean`](lean/core/MathFormalCore/Side24/Arithmetic.lean) against [`coefficients/side24_v1/PROOF.md`](../coefficients/side24_v1/PROOF.md) and files the template.

### `main`
1. Post a pointer to this lane on the work queue [main #86](https://github.com/d6g8k5htny-coder/main/issues/86) and the SIDE24 review [main #65](https://github.com/d6g8k5htny-coder/main/issues/65), quoting the pilot's exact status (`specified`; skeleton implication and arithmetic kernel-checked; Gaussian/Stirling content as explicit hypotheses).
2. Add a "Formal lane" row to `docs/RESEARCH_INDEX.md` linking `Math-/formalization/README.md`. Prefer unpinned surfaces (per the `twelve_project_check` amendment).
3. Where the scientific-state schema (main #95 / PR98 lineage) records mechanical-verification level, map `FORMAL_*` lane verdicts into that field as evidence, never as status.

### `trial`
1. Extend `.cursor/environment.json` install so Cloud Agents launched from `trial` have `elan` on `PATH` with toolchain `leanprover/lean4:v4.34.1` (`curl -sSfL https://github.com/leanprover/elan/releases/download/v4.2.4/elan-x86_64-unknown-linux-gnu.tar.gz | tar xz && ./elan-init -y --default-toolchain leanprover/lean4:v4.34.1`). The Mathlib cache (`lake exe cache get` in `Math-/formalization/lean/mathlib`, several GB) is optional there; the core package needs nothing else.
2. Add a cross-repo engineering test that clones `Math-` at a pinned commit and runs `python -B -S formalization/formal_gate.py --with-lean --package core --no-results-check`.
3. Record in `docs/MULTI_AGENT_ACCESS.md` that the formal lane exists and that alignment reviews are eligible reciprocal work for every provider.

### `meta-framework`
1. Register the formal objects as artifact identities: `FORMAL-SIDE24-20260927-v1` → the pinned Lean source SHA-256s in `formalization/FORMALIZATION_STATUS.json` `sources`, and the axiom-audit digests. Identities only; no status field.

### `query-`
1. Teach the lookup to resolve a landing `claim_id` to its `formalization/FORMALIZATION_STATUS.json` entry and print `status`, `alignment`, and the statement declaration, using the local byte verifier on the pins. Read-only.

### `google-drive`
1. No action unless a public replica of a formal artifact is deliberately selected; then follow the existing custody rules and pin the same SHA-256s.

### `sandbox`
1. Private experiments with AI provers (Goedel-Prover, AlphaProof-style tools, DeepSeek-Prover) on the `Prop` specifications may run there. A generated proof becomes public only by landing in `Math-/formalization/lean/**` through this lane's gate; success is recorded as a `components[]` theorem, and the prover is named in `formal_author`. Do not export sandbox paths, outputs or hashes.

## Rules for every agent touching `formalization/**`

- A Lean edit requires, in the same PR: `lake build`, regenerated `AXIOMS.expected`, `python -B -S formalization/formal_gate.py --refresh-pins --no-results-check`, and regenerated `FORMAL_RESULTS.json`. Say so in the PR body. A failed pin check is not a mathematical objection.
- Never set a claim's `status` above what its main statement declaration supports; the gate cross-checks `def`/`theorem` and the audit, but the honest label is the author's duty.
- Never mark `alignment_review.status: ACCEPT` for your own Lean. Never treat `ACCEPT` as independence.
- Never introduce `sorry`, `native_decide`, `axiom`, `implemented_by`, or `extern`. If a parent theorem must be assumed, state it as a `Prop` hypothesis of your theorem (the pilot's `ReferenceEnclosure`/`PeriodizationBound` pattern) so the scope stays in the hypotheses.
- Never edit Layer 0 (`claims/`, `frontiers/downstream_gate_20260925/`, proof texts, review records) to make the formal lane pass. If the informal blob changes, re-bind and re-review.
- Formalizing a claim does not close it. `FORMAL_KERNEL_CHECKED_ALIGNED` is a lane verdict, displayed alongside provenance, scope and review; the hard gate still requires `PROVED_REVIEWED` through its own authority.

## Open follow-ups inside `Math-`

1. **Gate owner:** add `LEAN_KERNEL_CHECK`, `LEAN_STATEMENT_SPECIFIED`, `FORMAL_ALIGNMENT_ACCEPT` to `GRAPH.json` `non_discharge_tokens`, regenerating `SOURCE_FILES.json` and `RESULTS.json` in the same change. Until then Layer 0 refuses them as *unknown* tokens, which the formal gate asserts on every run.
2. **Blueprint:** optional `leanblueprint` rendering of the `components[].informal_location` map; documentation only.
3. **Next pilots:** `p15-price-boundary` (exact counterexample, `decide`), `p15-realized-covers`, `rn-count-interface`, then `p15-full-price`.
4. **Companion lane:** if `formal/` grows a second module or its author wants the two lanes' status vocabularies unified, do it through `formal/manifest.json` and this registry's `companion_packages` in one PR, with both gates and both test suites run.
5. **Peer review track:** when a claim reaches `FORMAL_KERNEL_CHECKED_ALIGNED`, a manuscript in the glossary's standard terminology with the Lean sources as supplementary material is the intended external route; the landing disposition is still governed by the existing review authority.
