# C296 hosted results

## Source identities

- base and PR target: Math- PR #487 head
  `7af365e8c8db1ae0275d4efe08a70a678f153ca2`;
- implementation GREEN head: `4aaddf42c474eee783f08b0350e705cea2cff181`;
- production Git blob: `77a75a4611040973ad355aff40555a808f1816e7`;
- positive-interface blob: `4885f7a0e8fdb7f1d3ab308991b043c438dbb8ef`;
- negative-control blob: `dd97a6073da0ea9bf87a19cb910daea2b46ca365`;
- axiom-audit blob: `2d77d76781209655c1a02478f5dccc827d573a78`;
- exact external C294 `Lifetime.lean` blob:
  `f2508f7f2e3fd42f22f5aa52bc5ead5ff9e73b9a`;
- Lean `v4.34.1`, commit `5045d0056413266e57c625dcd7c365b10e377c52`;
- Mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612`;
- workflow action `leanprover/lean-action@f061402b660e0c34644504b324e830f2991d4865`.

`SOURCE_SHA256SUMS` binds the complete implementation, interface/control,
toolchain/dependency, workflow, and consumed C294 source bytes.

## Verified execution

GitHub Actions run
[39415169578](https://github.com/d6g8k5htny-coder/Math-/actions/runs/39415169578),
job `118602321184`, succeeded at the implementation GREEN head.

- `Lifetime`, `RegularPointChart`, and `RegularPointChartInterface` built;
- production and interface passed Lean `-E warning` rechecks;
- standalone `leanchecker` passed for both named new modules;
- all seven audited declarations reported only `propext`,
  `Classical.choice`, and `Quot.sound`;
- the omitted-noncriticality fixture exited nonzero with the intended type
  mismatch: `regularPointChart hg` still required
  `¬ IsCriticalPoint d g ...`;
- the exact GREEN-head repository downstream hard gate passed in run
  [39415169606](https://github.com/d6g8k5htny-coder/Math-/actions/runs/39415169606).

Earlier runs preserve setup and harness failures rather than suppressing them:
`39412669016`, `39413381712`, `39413746410`, `39414329053`, and
`39414753347`.  The valid RED is run `39412930269`, job `118594890340`, which
built the exact consumed source and rejected the missing chart declarations.

## Limits

Local Lean execution was unavailable because the downloaded Lean 4.34.1 runtime
could not read `/proc/<pid>/exe` in this environment.  No runtime patch or bypass
was attempted.  Hosted checks are execution evidence, not scientific acceptance,
external independent replay, correspondence review, or authorization to merge.
Scientific effect remains **NONE**.
