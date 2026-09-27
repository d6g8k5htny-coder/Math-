# Formal verification lane — Layer 1

**Object:** MATH-FORMAL-LANE-20260927-v1. **Author:** Cursor cloud agent (Anthropic Claude model family), owner-directed, 27 September 2026.
**Scientific effect: NONE.** A Lean kernel check verifies the Lean statement that was written. It does not decide whether that statement is the informal theorem, and it never flips `lemma_closed`, prizes, premises, or a landing disposition.

[Registry](FORMALIZATION_STATUS.json) · [Gate](formal_gate.py) · [Pinned results](FORMAL_RESULTS.json) · [Glossary](GLOSSARY.md) · [Alignment review template](ALIGNMENT_REVIEW_TEMPLATE.md) · [Cross-repo coordination](COORDINATION.md) · [Landing claims](../claims/LANDING_CLAIMS.json) · [Downstream hard gate](../frontiers/downstream_gate_20260925/README.md)

## What this adds and what it leaves alone

Layer 0 is the existing stack: SHA-256/blob provenance, explicit domain and "does not claim" statements, nonauthor review records, the fail-closed downstream hard gate, and the landing manifest. **Nothing in Layer 0 is edited by this lane.** The hard gate's pinned sources, `GRAPH.json`, `RESULTS.json`, the landing manifest and every proof text are byte-identical to before.

Layer 1 adds, per landing `claim_id`:

| Lane field | Meaning | Who sets it |
|---|---|---|
| `status` = `none` / `specified` / `proved` / `kernel_checked` | How much of the claim's main statement exists in Lean and whether the kernel has accepted a proof of it | Formal author, checked by `formal_gate.py` against pinned sources and the pinned axiom audit |
| `components[]` | Individual Lean theorems, `Prop` specifications, and prose-only interfaces, each bound to the section/display of the informal proof it encodes | Formal author |
| `alignment_review` = `NONE` / `REVIEW_REQUIRED` / `ACCEPT` / `AMEND_REQUIRED` | Whether a distinct reviewer has checked that the Lean statement says what the informal statement says | A nonauthor reviewer, via a record under `reviews/` |
| `lane_verdict` (computed, never stored) | `FORMAL_NONE`, `FORMAL_SPECIFIED`, `FORMAL_PROVED_UNREPLAYED`, `FORMAL_KERNEL_CHECKED_AUTHOR_SIDE`, `FORMAL_KERNEL_CHECKED_ALIGNED` | `formal_gate.py` |

Only `FORMAL_KERNEL_CHECKED_ALIGNED` means "the claim is formally verified in this lane". It requires the main theorem to be kernel-checked with the three standard axioms only, replayed by CI, **and** an accepted alignment review by a distinct agent. Even then the landing disposition and the hard-gate classification are untouched: the review-topology contract says a proof assistant "verifies its encoded statement at its actual trust boundary; translation fidelity and imported hypotheses still require their own review". This lane implements exactly that separation.

## Trust boundary

- **Kernel:** Lean 4 `leanprover/lean4:v4.34.1`, pinned in both packages. Proofs use `decide`, `decide +kernel`, and Mathlib tactics whose output is kernel-checked.
- **Axioms:** only `propext`, `Classical.choice`, `Quot.sound`. `sorryAx` and `Lean.ofReduceBool` (`native_decide`) are forbidden. Each package pins a sorted axiom audit (`AXIOMS.expected`) that CI regenerates and compares byte for byte.
- **Textual guards:** the gate also rejects `sorry`, `native_decide`, `axiom`, `implemented_by`, and `extern` in pinned sources. A parent theorem may later be introduced as an explicit `axiom` only together with a registry entry that names it and its scope note; that path is deliberately closed until needed.
- **Independent re-checkers:** the core package is additionally re-checked in CI by the bundled `leanchecker` and by `nanoda` (independent Rust type checker). The Mathlib package runs the community `axiom-audit`.
- **Pins:** every Lean source, lakefile, toolchain file, axiom audit and the Mathlib `lake-manifest.json` is pinned by bytes and SHA-256 in the registry. Editing any of them without `--refresh-pins` fails closed. Refreshing pins never edits a status.
- **Informal binding:** every entry records the landing manifest's `statement_path` and Git blob of the informal proof. If the proof text changes, the blob changes, and the gate refuses with "alignment is stale" until the entry is re-bound and re-reviewed.

## Packages

| Package | Library | Dependency | What lives there |
|---|---|---|---|
| [`lean/core`](lean/core) | `MathFormalCore` | none (Lean core prelude) | Exact `Nat`/`Int`/`Rat` facts used as steps in informal proofs. Kernel-checked by `decide`. |
| [`lean/mathlib`](lean/mathlib) | `MathFormalReal` | Mathlib `v4.34.1` (`d13f23b7…`) plus `../core` | Definitions of the standard objects (`Real.Gamma`, `Real.pi`, `Real.sqrt`, `Real.exp`), `Prop` specifications of informal theorems, and real-number theorems. |

Splitting keeps the always-on lane cheap (the core package builds in under a second with no downloads) while still exposing the real-analysis statement layer.

## Pilot: SIDE24 coefficient

Claim `side24-coefficient` ([PROOF.md](../coefficients/side24_v1/PROOF.md), blob `44b66f04…`). Lane status **`specified`**, alignment **`REVIEW_REQUIRED`**.

- `MathFormalReal.Side24.Side24Theorem c24` is the displayed enclosure as a `Prop`, with the periodic coefficient `c24 : ℕ → ℝ` a parameter (parent main#63 Eq. 15.2 is a marked Kac-Rice integral and is not formalized).
- `ReferenceEnclosure` (Section 5: the Stirling/Machin/atanh interval computation) and `PeriodizationBound` (Sections 2–4, display (4)) are `Prop` specifications. **They are the hypotheses. Anything not in them is not claimed by the Lean file.**
- `side24_of_inputs : ReferenceEnclosure → PeriodizationBound c24 → Side24Theorem c24` is **kernel-checked**. So are the exact transfer steps `transfer_d2`/`transfer_d3` on the 80-digit endpoints `coefficient.py` produced, `exp_288_125_gt_ten`, `exp_neg_288_lt`, the odd-block eigenvalue bound, the cone-moment bounds, and thirty-odd arithmetic identities of Sections 1–5. See `components[]` in the registry for the section-by-section map.
- Not formalized: Gaussian conditioning, the cone integrals, the PSD covariance comparison, and the Gamma(7/6) remainder. They are listed as prose-only `interface` components with status `none`.

The claim therefore remains **author-side and conditional** exactly as the landing manifest says (`HOLD_WITH_DOMAIN`); the lane has made its logical skeleton and its arithmetic machine-checked and has made its remaining analytic content explicit as hypotheses.

## Run

From the repository root. Python is standard library only.

```sh
python -B -S -m unittest discover -s formal -p 'test_*.py' -v     # 40 negative controls
python -B -S formalization/formal_gate.py                                 # registry, pins, Layer 0 composition; compares FORMAL_RESULTS.json
python -B -S formalization/formal_gate.py --with-lean                     # + lake build and axiom audit replay (needs elan)
python -B -S formalization/formal_gate.py --refresh-pins --no-results-check   # deliberate pin regeneration after editing Lean sources
```

Installing the toolchain: `curl -sSfL https://github.com/leanprover/elan/releases/download/v4.2.4/elan-x86_64-unknown-linux-gnu.tar.gz | tar xz && ./elan-init -y --default-toolchain none`, then `cd formalization/lean/core && lake build`. The Mathlib package needs `lake exe cache get` once (several GB); CI does this with `leanprover/lean-action`.

When Lean sources change: rebuild, regenerate `AXIOMS.expected` with `lake env lean scripts/Axioms.lean > AXIOMS.expected` in the package directory, run `--refresh-pins`, then regenerate `FORMAL_RESULTS.json` with `python -B -S formalization/formal_gate.py --no-results-check > formalization/FORMAL_RESULTS.json`. Do this deliberately and say so in the PR; a failed pin check is not a mathematical objection.

## How it composes with the downstream hard gate

`formal_gate.py` imports `frontiers/downstream_gate_20260925/hard_gate.py` read-only and, for every claim with a graph node, asserts:

1. `promotion_allowed` is unchanged before and after the formal lane reads the graph;
2. each formal token (`LEAN_KERNEL_CHECK`, `LEAN_STATEMENT_SPECIFIED`, `FORMAL_ALIGNMENT_ACCEPT`) offered **alone** to `refuse_non_discharge_promotion` is refused;
3. no node is `controlling`.

Kernel acceptance is therefore non-discharge evidence for the informal claim, in the sense of main #90. Adding the formal tokens to `GRAPH.json`'s `non_discharge_tokens` list would make that explicit in Layer 0 as well; it requires regenerating the hard gate's `SOURCE_FILES.json` and `RESULTS.json` in the same change and is left to the gate owner (see [COORDINATION.md](COORDINATION.md)).

## Blueprint-style alignment

The registry's `components[].informal_location` fields and the doc strings on every Lean declaration form the informal↔formal correspondence that Lean Blueprint would render. Adopting `leanblueprint` (LaTeX + plasTeX) is a documentation follow-up; it does not change what the gate checks, and it must not be mistaken for the alignment review, which is a human/agent judgement recorded under `reviews/`.

## Next formalization targets

In order of expected effort: `p15-price-boundary` (exact finite counterexample; `decide`), `p15-realized-covers` (finite combinatorics), `rn-count-interface` (abstract event/count implications), `p15-full-price` (Theorem F with the sharp constant `1/[3 - log(3e-2)]`), then the Gaussian/Kac-Rice claims once the glossary's probabilistic objects have Mathlib carriers. Reuse `MathFormalCore`/`MathFormalReal`; add one module per claim.
