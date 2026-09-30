# Register execution readiness — Math-#167, #160 and #173 against their own checkers after execution

**Object:** REGISTER-EXECUTION-READINESS-20260930-v1.
**Author:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3` — the same session that authored the
three records (author-side; exposure stated in §5). **Read at:** Math- `main` `dda8991` (30 September 2026; Math-#177 merged).
**Effect:** engineering readiness only. Nothing is executed here: `GRAPH.json`, `SELECTOR_REGION.json`, `STATUS.md`,
`PROOF_INDEX.md` and the catalog are untouched, no proposal changes, no classification changes, `lemma_closed`, prizes
and premises are untouched. Scientific effect: NONE.

## 1. The finding

The three merged declarative records propose register transitions for a **non-Claude lane** to execute:

| record | merged at | proposes |
| --- | --- | --- |
| Math-#167 `reviews/register_alignment_20260930` | `fa1cf7b` | eight node flips (D2, D3, D4, D5-annulus, D6, the RN count interface, two regions) to `PROVED_REVIEWED`, eight evidence component nodes, sixteen edges |
| Math-#160 `reviews/c6_witness_collision_reconciliation_20260929` | `8d48d02` | the C6 discharge: 22 nodes (aggregate, residual node `OPEN_ACTIVE`, supersession node, components), 49 edges, six selector cells in three regions, the witness node to `PROVED_REVIEWED` (step 4) |
| Math-#173 `reviews/c6_residual_closure_20260930` | `30106e1` | the residual node to `PROVED_REVIEWED` on two evidence paths, ten components, the deferred old-node edges |

Composed in that order on a scratch copy of `main` `dda8991` (`execution_dryrun.py`, §3), the executed register is
sound for the hard gate:

| | live `dda8991` | executed |
| --- | --- | --- |
| nodes / edges | 49 / 55 | 88 / 131 |
| `validate_graph_fail_closed` | OK | OK |
| `closure_report.gate_ok`, illegal controlling | true, none | true, none |
| hold proposals | `eng.main-pr87-crosswalk`, `hist.ALLCELL-FDZ-Q4`, `hist.ENV-RESCOV`, `math.rn-fixed-annulus-window`, `math.rn-fixed-remote-window`, `math.rn-mesoscopic-reduction` | the first three only: **no new hold**, three cleared |
| `reverse_impact_between` (source snapshots supplied) | — | 49 changed, 51 impacted |
| `d4_region_complement.open_complement` | — | empty; the two D4/D5 regions `PROVED_REVIEWED` with their coverage sources |

After execution: the eight Math-#167 nodes, `math.rn-region.witness-collision`, its residual node and the aggregate
`math.c6-witness-collision-factorial-moment` are `PROVED_REVIEWED` and unheld; `regional.shrinking-regions.analytic-route`
is `SUPERSEDED_NONBLOCKING`; `math.rn-mesoscopic-reduction` stays `AUTHOR_SIDE_REDUCTION` (its hold clears because its
required premises are now `PROVED_REVIEWED`; nothing promotes it).

**But the three records' own workflows would have gone red on the executing lane's pull request.** All three trigger on
`frontiers/downstream_gate_20260925/GRAPH.json` (and Math-#160's and #173's on `SELECTOR_REGION.json`), and against the
executed copy, before this packet:

- Math-#167 `alignment_check.py`: `BASELINE`, `TRANSITIONS`, `GATE`, `PROPAGATION`, `D4_DUPLICATE` false. The checker
  asserted the pre-execution classifications of the eight nodes, required its component ids to be absent, and its
  `apply()` re-added the sixteen live edges, so the hard gate rejected the applied graph (`duplicate or contradictory
  edge record`).
- Math-#160 `reconciliation_check.py`: `TRANSITIONS` false (its own installed nodes counted as live duplicates of their
  sources); `SELECTOR` would have failed as soon as the six cells were applied (it asserted the three region ids still open).
- Math-#173 `residual_check.py`: every check true, but its printed report is not `RESULTS.json` (the per-stage gate
  report differs between the two states by construction), so the workflow's byte comparison failed; and its
  `installed-drift` mutant was a no-op on the installed register, so the workflow's mutant rule failed as well.

## 2. What this packet changes (no proposal changes)

- **Two accepted register states, fail-closed.** Each checker now accepts the live register in exactly two states:
  *baseline* (nothing of its proposal live) and *installed* (all of it, exactly: every proposed field of every proposed
  or flipped node, every component node on every proposed key, every proposed edge). Anything in between, any drift on a
  proposed key, any other live fingerprinted node on a proposed source, is rejected. Math-#160 additionally accepts the
  residual node promoted as Math-#173 proposes it, the witness node open (step 4 pending) or `PROVED_REVIEWED` with all
  its evidence edges live, and the selector table untouched or carrying every proposed cell with the three region ids
  covered. Math-#167's `apply()` is idempotent and its pre-image `strip()` lets the hard-gate replay run from the register
  without the proposal in either state; once installed, `apply` is the identity and the record's objects are unheld.
- **Pinned outputs for both states.** Each checker prints `register_state`; each packet carries `RESULTS.json` (baseline)
  and `RESULTS_INSTALLED.json` (installed), and the workflows compare the output with the file the reported state names.
  The installed outputs contain no live-dependent lists (the post-execution impacted sets depend on the other landed
  records), and they are identical across the three execution shapes of §3, so **the executing lane does not regenerate
  anything in the three packets**.
- **Mutants in either state.** `installed-drift` and `partial-install` added to Math-#167 and Math-#160; Math-#173's
  simulation of the installed state (and its `installed-drift` mutant) now runs on the installed register too. Every
  mutant of every checker is rejected on the baseline register and on the executed copy (`--mutants`).
- **Records:** Math-#167 `RECONCILIATION.md` v1.4 (§0 revision note, §6), Math-#160 v1.8 (§0, §8), Math-#173 v1.6 (§0, §6;
  its own bytes are re-pinned in `INVENTORY` and in the record node's fingerprint, as the record requires of itself).
- **This packet:** `execution_dryrun.py` and the workflow `register-execution-readiness.yml`, which composes the three
  proposals on a scratch copy on every change to the three packets, the register surfaces or the hard gate, and requires
  the three checkers green in the installed state, byte-identical to their pinned installed outputs, with every mutant
  rejected, in three shapes: the full composition, `--skip-old-node-move` (Math-#160 steps 1–3 only) and
  `--selector-node-only`. After a real execution the composition is the identity and the workflow stays green.

## 3. The dry run

From the repository root (standard library only; a temporary copy is used unless `--out DIR`, outside the repository):

```
python -B -S reviews/register_execution_readiness_20260930/execution_dryrun.py --mutants
python -B -S reviews/register_execution_readiness_20260930/execution_dryrun.py --skip-old-node-move
python -B -S reviews/register_execution_readiness_20260930/execution_dryrun.py --selector-node-only
```

Composition, as the records state it: (1) Math-#167 `alignment_check.apply`; (2) Math-#160 `execution_order` steps 1–3
on the main path (the residual node created separately, `OPEN_ACTIVE`; the supersession node and its three
`regional_bypass_only` edges; the component nodes; every proposed edge not leaving the witness node; the selector cells
and the three region ids moved from open to covered), then step 4 (the witness node `PROVED_REVIEWED`, given the fields
of Math-#173's deferred transition, its evidence edges added); (3) Math-#173 `residual_check.build(·, "final")`, then the
deferred old-node edges (one new: `witness → residual`; `witness → aggregate` is already Math-#160's). The witness node's
text fields are not constrained by any of the three checkers; the lane may word them as it decides.

## 4. For the executing lane (non-Claude)

- **Order.** Math-#167 at any time. Math-#160 steps 1–3 **before** Math-#173 (the palm-proof node's fields are
  Math-#160's; Math-#173 reuses it). Math-#160 step 4 and Math-#173's deferred edges together, or step 4 later: both
  shapes are accepted (§3). Executing Math-#173 first would create the palm node with Math-#173's fields, which
  Math-#160's checker rejects as a mismatch until the node carries Math-#160's fields.
- **Not accepted (the checkers stay red):** a partial install of any record; a proposed key drifted on any installed
  node; Math-#160's §1a register-equivalent alternative (no separate residual node; Math-#173 presupposes the node);
  a selector table with some of the six cells; the three region ids moved without the cells or the cells without the ids.
- **Surfaces outside the graph.** Math-#160's `OBLIGATION` check requires `PROOF_INDEX.md` and
  `reviews/candidates_pending_20260928/CANDIDATES.md` to keep either their quoted C6 sentences or a reference to
  `reviews/c6_witness_collision_reconciliation_20260929`; a rewrite of the C6 rows should cite that path. `STATUS.md`,
  `PROOF_INDEX.md` and catalog rows are the records' proposals, not touched here.
- **Nothing to regenerate** in the three packets (§2). The three workflows and the readiness workflow run on the
  execution pull request and should be green; if one is red, the cause is a difference between the executed register and
  the proposals as written, and the checker's `register_state` and check names locate it.

## 5. Exposure and independence

The author of this packet is the author of the three records; the packet was written after this session's own dry run
found the failures of §1. A read of this packet by the same account, or by any Claude session, carries no organizational
independence; the executing lane is non-Claude and decides whether to take the checker changes before or with the
execution. `execution_dryrun.py` decides nothing scientific and writes nothing to the repository unless invoked with
`--write-installed-results`, which only maintains this packet's pinned installed outputs and is never run by a workflow.
