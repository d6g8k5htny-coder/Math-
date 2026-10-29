# Frozen same-period torus separation helper

Root-dispatched48 helper, 26 October2026. PRECODE `b43c1c023574a19fda86bc82108c5cd0f9999f78`; native pickup6415454977, checkpoint12:45/terminal13:45UTC unchanged. Producer explicitly confirmed its `CONTROL_CONTRACT.md` frozen before helper source began. Own scratch only: `/workspace/scratch/remote-jet-torus-separation`.

`NEEDED_SECTION.lean.txt` is the single frozen integration section, to paste **inside** namespace `I4SourceRemoteJetWitness` once. It contains three **private** theorems with the producer-agreed names/order:

- `sourceC_ne_zero {L} (hL : L ≠ 0)`.
- `cosine_sourceC_eq_one_iff {L} (hL) (a b : ℝ)`: literal `cos (sourceC L * (a-b)) = 1 ↔ (a : AddCircle L) = (b : AddCircle L)`.
- `remote_positive_coordinate {L} (hL) (x p : Fin 2 → ℝ) (hx : torusProjection 2 L x ≠ torusProjection 2 L p)`: some coordinate has `0 < 1 - cos (sourceC L * (x j-p j))`.

Only hL is required. Negative periods remain literal; no representatives, positive-period instance, absolute-value replacement, phase range, radius or pin inverse. The scalar proof uses the unrestricted integer cosine period characterization, nonzero2π cancellation and `AddCircle.coe_eq_zero_iff`. Function extensionality extracts a quotient-separating coordinate, and `cos_le_one` gives strict positivity.

Strict Werror development **strict003 PASS** at12:03:27.937548UTC, 2.678742208seconds, empty stdout/stderr. It elaborated only this new scratch source against the qualified dependencies. Retained actual failures: strict001 was rejected because scratch source lay outside the default package root; strict002 then reached source and rejected deprecated `push_neg` under Werror. Explicit `--root` corrected the harness; `push Not` corrected the source. No failed evidence or original snapshots were overwritten. `runs/*` retain exact source snapshots, full separate streams, commands, exits and measured times; `RAW_LEDGER.jsonl` indexes all three attempts.

Exact source/section bounds/hashes and helper object custody are in `FROZEN_SECTION.json`. The helper object is **excluded** from production import/cache. No standalone kernel, axiom audit, control campaign or target credit; producer integrates this exact source section before its sole final module kernel. The integrated producer remains responsible for actual interpolation/collision controls and full actual-module inventory, including these private constants. This helper makes no jet-rank, global Morse, actual conditional-law or canonical-label claim.

Qualified47/1096/32 at `c0398e27fe8da6363a9a1f6d50c206918778491e` and all applicable prior mathematical evidence are reused without replay. Owner rule: unchanged completed evidence does not expire on a new agent/session/freeze or pending process; provider-distinct obligations remain separate. No upstream source, cache, config, manifest, git or external post changed. Scientific effect **NONE**; provider-distinct credit **0**.

Canonical onboarding links carried forward (not proof of another recipient's reading):

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
