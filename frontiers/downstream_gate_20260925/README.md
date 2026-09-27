# Downstream hard gate — transition-integrity successor

**Object:** DOWNSTREAM-HARD-GATE-20260925-v1  
**Original engineering author:** Cursor. **Transition successor:** OpenAI / ChatGPT, Math- PR15.  
**Scientific effect: NONE.** Tests establish software behavior, not proof or independent review.

## Positive premise satisfaction is not terminal classification

Only `PROVED_REVIEWED` satisfies a still-required positive premise. Required `REFUTED`,
`BLOCKED_ABSENT`, author-side/open, and `SUPERSEDED_NONBLOCKING` nodes block promotion.
Supersession requires a reviewed edge replacement/removal; renaming a premise is insufficient.
The proposed result itself must also be eligible. Green tests, hashes, navigation and self-review
are non-discharge evidence. Scientific records are inputs; this package does not accept proofs.

## Loss-only transition checks

`reverse_impact_between` compares complete canonical JSON node records, outgoing edge records
(including metadata), graph context and, when supplied, paired complete source snapshots.
It includes changed nodes themselves and traverses the UNION of old and new links, so removal
cannot hide prior dependents. Input graphs are unchanged. Refuted nodes remain refuted.
Unknown classifications, malformed booleans, duplicate/contradictory edges, missing nodes,
required cycles, duplicate JSON keys and non-finite JSON values are rejected. Validation runs
at public promotion and reporting boundaries as well as transition inspection.

`git_transition_audit.py` reads graph and source objects from two immutable Git commits.
Source-only edits therefore do not depend on an author remembering to update a fingerprint.
Repository blobs/directories are byte-bound; external references are explicitly unresolved,
and absent historical carriers remain absent. Output is HOLD/REVALIDATION proposals only,
with `promotion_permission: false`. A changed controlling node, illegal controlling state,
or an unbound controlling source causes a nonzero exit. Unaffected author-side work can proceed.
This is not a complete external-source monitor or an independent-review authority.

## Run

```sh
python -B -S -m unittest discover -p 'test_*.py' -v
python -B -O -S -m unittest discover -p 'test_*.py' -v
python -B -S run_validation.py --output /tmp/downstream-gate-new-run
python -B -S git_transition_audit.py --repo /path/to/repository --base FULL_BASE_SHA --head FULL_HEAD_SHA --output /tmp/new-transition.json
```

67 distinct tests and 24 assertion-detected semantic mutants are required in both Python modes.
The source-bound CI workflow also runs 177 existing coefficient/lifetime/price/remote regressions,
for 244 distinct methods, and audits actual PR base/test-merge source objects. Workflow execution
and branch-protection enforcement are separate; no administration setting is claimed here.

The source manifest includes the nested D0 patch. All pins are checked before and after execution.
A changed source requires a deliberately regenerated manifest and result file, not a skipped check.

## Research boundaries

Fixed-remote coverage does not extend to shrinking pin/witness collisions or the full annulus.
No mathematical graph status, historical proof, normalizer, JETMOD, prize, or vault record is changed.
D0 recipe and SCOPE are preserved historical package context; current integration state comes from
live PRs and their exact commits, not from the old recipe's operational status sentences.
PR15 remains a technical candidate until distinct-lane review and the exact tested integration.
