# Contribution replay and process supervision

Owner: `none — self-contained`. This finish-only tool runs an explicit local
contribution campaign. It never declares federation CBZ-0, global Git/PR hygiene,
RL effectiveness or an unrestricted theorem. A passing local result is exactly
`LOCAL_CONTRIBUTION_PASS` with `cbz_zero:false`.

## Reproduction

From the envelope containing `tools/`, `tests/` and its canonical or source-identified
projected `QUARANTINE.json`, use fresh external build and evidence destinations:

```sh
python -B tools/contribution_gate.py --source /ABS/IMMUTABLE_PROJECT \
  --lean /ABS/PINNED_LEAN/bin/lean --mathlib-root /ABS/PINNED_MATHLIB \
  --build-dir /ABS/NEW_BUILD --output /ABS/NEW_EVIDENCE
```

The executable/Mathlib pins are checked by the fresh proof and native builders.
`UL_LEAN` and `UL_MATHLIB_ROOT` propagate the selected paths to the native adapter.
Only the documented external compiler/shared-library/dependency cache trust is
used; no prior project proof cache is accepted as the fresh compilation cache.
The generated formal scanner inventory covers all regular files in `formal/`,
with explicit local modules and exact Lean/Mathlib external import names. Original
quarantine prefixes relocate to the chosen source; source hashes do not change.

The full immutable project, tool and test directories, quarantine index and
prepared scanner inputs are frozen by exact file-name set and SHA256 before
launch. Only four explicit paths inside the project are excluded: `build/`,
`integration/native_worker/build/`, `.native.lock` and `.git`. Arbitrary nested
folders named `evidence`, `sources`, or `build` do not inherit those exclusions.
Unreadable traversals and symlinks reject. Before each child, after each child,
and at the final observation, both names and bytes must still match. A child
cannot repair drift that existed before its launch and receive success.

The complete literal-argv job plan is validated before any job executes. Empty or
duplicate plans, malformed argv/cwd and nonfinite or invalid resource bounds
reject. No shell interprets command arguments. Actual children, exit codes,
streams and terminal receipts are retained on failure; no failure becomes a pass
because a later job succeeds. The final contrary source observation overrides a
previous local passing result.

Normal and optimized Python auditor/regression controls precede the source scan.
The fresh proof job supplies the immediately following all-owned-kernel job's
cache and result. The latter's `--parent-lock-held` is verified against the actual
OS lock holder through the process-supervisor ancestor chain; it is not an
untrusted environment assertion. Native build, fresh-worker sessions and saved
wire/source bindings follow. Each logical gate keeps its own exact coverage;
the orchestration does not turn scoped checks into federation-wide acceptance.

## Linux supervision boundary

`recorded_process.py` invokes an isolated standard-library supervisor per job.
`process_supervisor.py` uses Linux subreaper and parent-death controls to retain
ownership of ordinary child/setsid/double-fork descendants. Timeout, output-limit
trigger or recorder death requests bounded cleanup; only unreaped direct children
are signaled, preventing PID-reuse races against unrelated processes. Orphaned
ordinary descendants reparent into the supervisor and are killed/reaped in later
cleanup iterations. Unexpected descendants after leader exit prevent success.
Streams are hashed only after the terminal tree receipt; incomplete or missing
cleanup evidence prevents success. Native proof validity remains separate.

This is not an OS sandbox, a hard wall-time bound for the entire caller, or
protection against hostile same-UID tampering, unkillable kernel tasks, or
filesystem changes made and restored between observations. Cleanup and stream
hashing may follow the child timeout. Output-limit polling can overshoot the
trigger threshold before a fast child exits. Receipts state these operational
facts without claiming mathematical certification from timings or memory.
`wait4` covers the supervisor and its reaped subtree; nested receipts must not
be summed again as independent cost.

## Observed self-verification

The current source-bound observation is
`evidence/replay_finish_20261029T180528Z/results.json`:

| Component | Normal | Optimized | Source stability |
| --- | --- | --- | --- |
| Replay, source inventory and process supervision | 25 tests, PASS, no skips | 25 tests, PASS, no skips | Exact source/test hashes unchanged |
| Federation snapshot controls | 25 tests, PASS, no skips | 25 tests, PASS, no skips | Exact source/test hashes unchanged |

Exact executable component commands:

```sh
python -B -m unittest discover -s tests -p 'test_contribution_gate*.py' -v
python -B -O -m unittest discover -s tests -p 'test_contribution_gate*.py' -v
python -B -m unittest discover -s tests -p 'test_federation*.py' -v
python -B -O -m unittest discover -s tests -p 'test_federation*.py' -v
```

An additional read-only reviewer independently ran the replay25-test suite in
both modes, with unchanged implementation/test hashes and no unresolved important
finding within this scope: `evidence/replay_final_review/review.md` and its pinned
`verification.json`. This is technical review and finite adverse testing, not a
formal proof of Python correctness or independent mathematical acceptance.

Earlier RED logs and source snapshots remain preserved. Correcting the earlier
nested-reaping test requires the deep child to be confirmed dead/observed and
cleanup complete; it does not falsely require that the outer supervisor itself
reaped a child legitimately reaped by its inner supervisor. The implementation
must still report actual reaping ownership and cannot claim the dead child as a
survivor-free live process without evidence.

Current implementation identities:

- `contribution_gate.py`: `cace0daa785c8344cf5cde923b1a143d9d164bcabdcec472956eba8d474b2481`
- `recorded_process.py`: `ef2eb81b3ffbe0accb8e9cc83f709462896e7f779e50af05ae58448046dc312d`
- `process_supervisor.py`: `43e3c749d6945ea64a2c6ceaec13094553fc018af644ebf5d93b799d9ab18c5a`

## Canonical registry entries

| Tool | Purpose | Self-verification | Owner | Criteria served |
| --- | --- | --- | --- | --- |
| `tools/contribution_gate.py` | Explicit local gate plan, full immutable-input freeze, truthful scoped result | Source-bound25 normal/25 optimized controls plus independent same-scope read-only review | none — self-contained | 5,9,11 |
| `tools/recorded_process.py`, `tools/process_supervisor.py` | Linux owned-subtree lifecycle, literal argv, streams and truthful terminal cost/cleanup receipts | Nested-session, double-fork, parent-death, unrelated-sibling, output-limit and malformed-bound controls in the25-test suite | none — self-contained | 5,9 |

No heavy Lean process or fresh native proof campaign was launched by this
verification task. The final source-commit clone campaign remains a separate
parent-owned execution obligation.
