# Agent entry — `Math-`

Mathematical candidates, proofs, programs, and reproducible calculations. Not a status register.

## Always

- Coordinate via [`main`](https://github.com/d6g8k5htny-coder/main) campaign work and the [`governance-`](https://github.com/d6g8k5htny-coder/governance-) working contract.
- Prefer exact source identities (commit/path/hash) over mutable labels.
- Scientific effect: **NONE**. Never flip `lemma_closed` / prizes / premises.
- Cross-repo eng tests and Path C live in [`d6g8k5htny-coder/trial`](https://github.com/d6g8k5htny-coder/trial).
- Calculations here use the Python standard library only (no extra pip env required in this repo).
- Two Lean 4 lanes exist and neither edits the other: [`formal/`](formal/README.md) (closed GP-FOR-192 companion packet, owned by `formal/manifest.json` + `formal/gate.py`) and [`formalization/`](formalization/README.md) (landing-claim-keyed registry, glossary, alignment review lane; `formalization/formal_gate.py` indexes `formal/` read-only and requires shared toolchain/Mathlib pins). Both: pinned sources, standard axioms only, no `sorry`, kernel check ≠ acceptance, alignment review by a distinct agent. Read [`formalization/COORDINATION.md`](formalization/COORDINATION.md) before touching either directory or asking a sibling repository for follow-ups.

## Never

- Duplicate scientific-status registers here.
- Publish private `sandbox` material.
- Ask Dylan for re-approval of autonomy already granted.

## Start here

1. This repository’s [README](README.md)
2. [`governance-` working contract](https://github.com/d6g8k5htny-coder/governance-)
3. [`trial` multi-agent access](https://github.com/d6g8k5htny-coder/trial/blob/main/docs/MULTI_AGENT_ACCESS.md) (Cloud Agent env deps live on trial `.cursor/environment.json`)

## Additive formal lane — owner directive 2026-09-27

Read [formal/README.md](formal/README.md), [the exact scope](formal/SCOPE.md), and [main #95](https://github.com/d6g8k5htny-coder/main/issues/95) before claiming formal verification. The isolated `formal/` package uses explicitly pinned Lean/mathlib; this owner-authorized toolchain addition does not change the standard-library Python rule elsewhere. A build alone, Blueprint link, solver output, hash or merge is not scientific acceptance. The exact source/axiom/negative-control gate and a separately authenticated, independent alignment review are distinct requirements. Preserve recovered original proof bytes and existing verdicts; document successor changes. Record actual agent pickup and actual review evidence, not presumed activity. Do not duplicate the controlling scientific-status register or broaden these scalar companions into parent theorems.
