# Math- PR513 source-preserving branch-sync report

Prepared by OpenAI/Codex author engineering helper on 2026-10-26. No publication, branch push, PR merge, readiness change, review disposition, permission change or scientific promotion performed.

## Exact source and topology

- PR513: https://github.com/d6g8k5htny-coder/Math-/pull/513 (open, Draft).
- Author branch: `codex/whole-field-conditioning-20261025`.
- Live remote author head: `37f8f01db8b7e30190f09bf784d1b4e3419da540`.
- PR API reported base SHA: `8b5451059903997a1956c3a9c52f02cf09928bef`.
- Actual remote `main` tip: `1cba5115253d43e1e46caa7e0381fcb3f6108cbd`.
- Common ancestor: `7a2ee81ecb088813b7c6f8cd383d66acb2c7f773`.
- `git merge-tree --write-tree` with ordered inputs author head then actual main returned success, no conflicts, predicted tree `cf3e699e9deb25a7ce1b12b92b1c2f50dd3ba82f`.
- Merge parents in order: `37f8f01db8b7e30190f09bf784d1b4e3419da540`, `1cba5115253d43e1e46caa7e0381fcb3f6108cbd`.
- Prepared candidate merge: `c0c92e7241f6ed41770b0fb6896b483d1c2ed2b0`.
- New isolated worktree: `/workspace/Math-wholefield-sync-20261026`; temporary branch `codex/wholefield-sync-20261026`.
- Normal `git merge --no-ff --no-commit` completed without conflicts, followed by an ordinary merge commit. No manual resolutions. Actual tree matches the preflight prediction. Both parents are ancestors of the candidate and the temporary worktree is clean.
- Canonical author pickup: https://github.com/d6g8k5htny-coder/Math-/pull/513#issuecomment-6408058542; root explicitly activated this helper's bounded isolated preparation. The pickup and live refs were reread immediately before mutation.

## Narrow composition delta

The incoming first-parent sync delta has 13 paths (+1142/-10):

```
.claude/skills/babysit/SKILL.md
.claude/skills/steward/SKILL.md
.github/workflows/cap-first-exit-lean.yml
.github/workflows/lean-specification-proofs.yml
.github/workflows/lean-specifications.yml
.github/workflows/lm006-sign-coefficient.yml
AGENTS.md
README.md
docs/integration/2026-10-23-postcut-proof-sources.md
tests/test_d3_l4_replay.py
tests/test_lm006_sign_coefficient_replay.py
tools/d3_l4_replay.py
tools/lm006_sign_coefficient_replay.py
```

All incoming bytes are inherited from actual main; no manual resolutions occurred. The successor diff against actual main remains 166 paths entirely inside `frontiers/source_derivative_gaussian_20261025` (+15009/-14). This is topology repair only; inherited workflow bytes are not newly authored or reviewed here.

## Source preservation and reusable verification

The complete packet `frontiers/source_derivative_gaussian_20261025` at both the reviewed source cut and predicted composition has Git tree identity `aa776f39937e40b7aff96471aa097e7a566d8a9a`. Its fixed `inputs` tree is `74938621d9444d2ce046f615b46c5bbdfa8c9c60` at both cuts. The packet-wide tree equality includes every proof, hypothesis, source contract, input, dependency pin, source manifest, receipt, raw log, failed attempt and historical evidence byte.

Unchanged packet-owned dependency selectors:

- `lakefile.toml` blob `1f6f976447ebdbbf2f3f5c97f0aab7cf47aa8b54`.
- `lake-manifest.json` blob `9fe1332352893f5f89e74b550a25ee187b871ed3`.
- `lean-toolchain` blob `ba8ebf2dbaf6a668cd2a0e086186d6d569b69ff5`.
- Mathlib rev `d13f23b723b8a846827a245b89c10fc7d3f11612`.

Owner clarification in `/workspace/AGENTS.md`: reuse completed applicable verification; do not repeat unchanged material under unchanged relevant assumptions/dependencies. The completed 18-module, 292-declaration verification is reused, including earlier baseline evidence and changed four-module compilation, kernel replay, standard-axiom audits and controls. No Lean build, kernel replay, audit, control or unchanged baseline test has been rerun for this composition.

Native different-family scientific review [Claude 01Cz PASS_SCOPED 6405469445](https://github.com/d6g8k5htny-coder/Math-/pull/513#issuecomment-6405469445) binds `37f8f01db8b7e30190f09bf784d1b4e3419da540`, stacked on `7a2ee81e`, four-module scope only. Its record says proofs/statements read in full; execution reused rather than repeated. It preserves the 182 unchanged +110 new declaration split,109 direct new targets plus one disclosed transitive instance. The tree/dependency comparison provides the source-preservation basis for later carry-over assessment; this helper does not issue a scientific carry-over verdict or independent review.

Current tested integration checks, any required exact-head composition assessment, actual Ready-triggered automatic review, findings disposition and independent integration duties remain separate. No old CI is represented as current composition CI; no blanket green-CI claim is made.

## Coordination and retained incident

Fresh PR513 comments contained the scientific review pickup/release and [Cursor OBSERVE 6406512586](https://github.com/d6g8k5htny-coder/Math-/pull/513#issuecomment-6406512586), explicitly no tip-sync or Ready seat claim. Root reports a current board read with no competing PR513 sync pickup, then posted the canonical author pickup linked above. Root handles publication. The Math512/a16 keep-or-revert decision on main619 remains unresolved; governance33 process note does not waive it. This local proposal neither decides that incident nor reverts, merges, waives or changes its status.

## Onboarding and environment evidence

Read `/workspace/AGENTS.md`, `/workspace/Math-curvature-20261026/AGENTS.md`, Math README and required-check contract, current governance working contract, mandate/delegation and live workflow. Required canonical links for handoff:

- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OWNER_MANDATE_20261015.md
- https://github.com/d6g8k5htny-coder/main/blob/b665307520948308a53d190d7341bf301df3b3a2/governance/OP-AUTONOMY-20260923-v2.1.md
- Live workflow read at main-repository SHA `8fb04ee5f0488eeb4652e604d3c5b8552b931b87`, saved as `OP-WORKFLOW-live.md` beside this report.

Runtime observation current: unrestricted HTTP policy enforced; VPN configured false. Inherited proxy/credentials preserved; no secrets/environment dump. `/workspace/main/AGENTS.md` was already modified and is untouched by this helper. This helper did not write the old fixed workspace or active curvature worktree, apart from shared Git object/ref metadata from fetch. Old fixed source head remains `37f8f01db8b7e30190f09bf784d1b4e3419da540`. The active curvature head moved concurrently from initial `ecee76c` to `458058b9a004482de4e80ddae6d1a34ba31287eb`; root confirmed this is its legitimate concurrent frozen `SOURCE_COMPACT_TARGET_MOMENTS.md` contract commit, a single documentation addition, not this helper's mutation or a successor merge. An overbroad final stability assertion failed on that unrelated movement; the candidate composition checks had already passed and their applicable evidence is reused. The assertion was outside the required candidate-composition scope and prompted no reset or repeated checks. No assertion of an unchanged active-curvature head is made. Scratch refs were fetched under `refs/wholefield-sync-20261026/` and Git additionally refreshed its ordinary remote-tracking main ref; that fetch changed no checked-out branch or file.

## Live workflow treatment

The live workflow says: “A base-only or unrelated change needs a bounded comparison of that slice and fresh applicable integration checks, not a repeated mathematical argument.” It also says to reuse a review only for unchanged proof bytes, hypotheses and consumed dependencies, and to keep exact reviewed head, PR-reported base and tested composition separate. The bounded comparisons above satisfy source-preservation evidence for this local composition; later integration checks and review carry-over assessment remain required at their actual identities.

The four inherited workflow paths are already-landed base history. Their candidate blobs exactly match actual main, and the complete authored PR diff against actual main contains only the166 packet paths. No workflow code, security setting, decision authority or review rule is authored or weakened by this branch sync. No actual stop was found for the authorized isolated author-sync stage. This observation does not review those inherited workflow changes, apply the manual-review exception to a proof-carrying PR, bypass checks, or settle the retained Math512 incident.

## Non-destructive exact publication route (root only; not executed)

The update is a fast-forward from `37f8f01db8b7e30190f09bf784d1b4e3419da540` to `c0c92e7241f6ed41770b0fb6896b483d1c2ed2b0`. Root must refresh current ownership and refs; stop on a mismatch and reconcile rather than overwrite. The intended no-force command is:

```sh
git -C /workspace/Math-wholefield-sync-20261026 push --porcelain origin c0c92e7241f6ed41770b0fb6896b483d1c2ed2b0:refs/heads/codex/whole-field-conditioning-20261025
```

Immediately before it, assert `git ls-remote origin refs/heads/codex/whole-field-conditioning-20261025` still reports exactly `37f8f01db8b7e30190f09bf784d1b4e3419da540` and remote main still reports `1cba5115253d43e1e46caa7e0381fcb3f6108cbd`; assert the old head is an ancestor of the exact candidate. The command has neither a leading `+` refspec nor a force option. Git's receive-pack transaction guards against a ref changing after its advertisement, and the server independently enforces fast-forward/protection. This normal push uses the advertised-old-ref transaction guard; it is not an absolute old-SHA lease across the gap between a separate preflight read and transport advertisement. If root requires that stronger CAS, choose a supported route explicitly rather than pretending the normal command has a guarantee it lacks.

No current main or shared checked-out author branch write is required locally: publish the exact prepared commit directly to its remote author ref. Root handles current-head hosted CI and subsequent workflow duties. `COMPOSITION.json` records the local bounded evidence. Nothing was pushed or posted by this helper.
