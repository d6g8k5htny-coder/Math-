# Literal Lifetime endpoint lattice distance helper

26 October 2026. OpenAI/Codex `/root/candidate_distance`, delegated by `/root`, direct API coordination with `/root/actual_fold_candidate_construct`. Scratch-only ownership: `/workspace/scratch/actual-fold-candidate-distance`. Scientific effect NONE. Separate research-target credit 0; same-family/provider-distinct credit 0. No worker delegation, production/input/config/cache/manifest mutation, commit, external post, standalone kernel, audit or control campaign.

## Frozen handoff

At `2026-10-26T10:36:37.622171+00:00`, `CandidateDistance.lean` is frozen: 5,688 bytes, SHA-256 `fbb29aeb95a2f90815463cc07577aee43bf6b22579d973297e75850598ec4ab5`.

`FROZEN_SECTION.lean` is its exact full `I4SourceActualFoldCandidate` namespace body, without imports/noncomputable/open/namespace wrappers: 5,504 bytes, SHA-256 `fa9c5cedf0c740802ff211b5f232ae343f8483a5df03f7708ce3ce7f3a9e5ef3`. Integrate this exact section ONCE into the producer's common namespace. It assumes the producer has `noncomputable section` and `open UniversalLaw.Spec.Lifetime`. Source import is only `SourceActualFoldH0`; no Mathlib umbrella or new supporting dependency.

The frozen section owns `endpointLiftM` and `endpointLiftS`, exactly `(I4LifetimeField.coordinates 2).symm (I4SourceConfluentPins.endpointM r)` and the matching saddle expression. It exports:

- `coordinates_endpointLiftM`, `coordinates_endpointLiftS`: exact coordinate identities.
- `torusProjection_endpointLiftM`, `torusProjection_endpointLiftS`: exact existing product-torus projection identities, with no quotient-carrier identification.
- `endpointLiftM_apply`, `endpointLiftS_apply`: literal component facts.
- `endpoint_lifts_sub_norm {r} (hr : 0 ≤ r)`: Euclidean parent norm of the pin difference equals `r`.
- `endpoint_lifts_lattice_lower {L r} (hL : 0 < L) (hrL : r < L / 2) (n : Fin 2 → ℤ)`: every parent lattice shift has norm at least `r`.
- `endpoint_lifts_torusDist {L r} (hL : 0 < L) (hr : 0 < r) (hrL : r < L / 2)`: literal `UniversalLaw.Spec.Lifetime.torusDist 2 L (endpointLiftM r) (endpointLiftS r) = r`.
- `endpoint_lifts_torusDist_unit_zero`: `L=1,r=1` literal distance is zero, by the concrete lattice vector `![1,0]`.
- `endpoint_lifts_torusDist_unit_ne_radius`: the same distance is unequal to `1`, supporting the producer's one false mutation deleting the radius bound.

The proof unfolds the literal conditional infimum through `ciInf_le`/`le_ciInf`. Norm nonnegativity gives the required bounded-below range; zero shift gives the upper bound. For any integer lattice vector, the zeroth component equals `-r+L*n₀`. If `n₀≤0`, its absolute value is at least `r`; otherwise integer discreteness gives `n₀≥1`, and `r<L/2` gives the same lower bound. `PiLp.norm_apply_le` transfers that component bound to the actual Euclidean parent norm. The unshifted vector is explicitly `EuclideanSpace.single 0 (-r)` and uses `PiLp.norm_single`. Thus no isometry claim about `coordinates` is introduced. No actual gradient/Hessian/type/H0 API is duplicated.

## Reused evidence and scope

`/workspace/AGENTS.md` applies: completed applicable verification is reused, and unchanged material is not rechecked because this helper is a new agent or handoff. All 43 qualified modules / 32 inputs and completed actual geometry/H0/conventional mathematics remain reusable evidence. Provider-distinct review and any other pending process are separate from mathematical verification. The only new checking here was strict elaboration of the newly written helper and its changed warning fixes. Integrated producer own-module qualification covers this section; these scratch objects are not production eligible and must not be copied to a production cache.

Read authority included repository `AGENTS.md`, README, formal README/SCOPE/required-check contract, local standing owner mandate/delegation/workflow, candidate source/plan at root's precode `d7c3634` scope, and `/workspace/scratch/actual-canonical-partner-preflight/REPORT.md`. Consumed current source identities are recorded in `FROZEN_SOURCE.json`, without replaying their old verification. Canonical standing links carried for future handoff:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md

Carrying these links alone does not establish that a later agent read them. This report makes no independent/provider-distinct review claim and no scientific-status update. Native checkpoint remains 11:15 UTC and terminal 12:15 UTC; no timer reset.

## Strict elaboration raw ledger

Every invocation used the existing pinned packet environment through `/home/agent/.elan/bin/lake env lean -DwarningAsError=true -R /workspace/scratch/actual-fold-candidate-distance -o /workspace/scratch/actual-fold-candidate-distance/build/CandidateDistance.olean /workspace/scratch/actual-fold-candidate-distance/CandidateDistance.lean`, from `/workspace/Math-curvature-20261026/frontiers/source_derivative_gaussian_20261025`. Each `runs/strict-NNN/` contains exact source snapshot, START, raw output log, exit, command vector, source hash, UTC start/end and elapsed time. `run_stage.py` is the exact retaining runner. No completed upstream check was replayed.

| Run | UTC start | UTC end | Exit | Elapsed | Result |
|---|---|---|---:|---:|---|
| strict-001 | 10:35:13.253759 | 10:35:16.641398 | 1 | 3.387s | Two style warnings; zero-lattice simplification missing coordinate proof |
| strict-002 | 10:35:47.268658 | 10:35:50.757669 | 1 | 3.489s | All mathematical goals solved; two style warnings |
| strict-003 | 10:36:06.501094 | 10:36:10.149881 | 0 | 3.649s | Frozen helper strict PASS, empty output log |

All failures remain retained. The two earlier source snapshots retain their exact hashes in the corresponding receipts. There is no standalone helper kernel/inventory/negative control; producer qualification is the sole integrated campaign.
