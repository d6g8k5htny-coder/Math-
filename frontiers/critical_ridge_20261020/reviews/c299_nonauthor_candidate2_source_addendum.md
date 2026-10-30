# C299 nonauthor review — candidate 2 source addendum

Actual reviewer: OpenAI Codex `/root/c299_nonauthor_review`, delegated by root chat `01a0bbb5-2fcb-77f0-b78b-4d220ddd7ab2` for Dylan Roy. This is an additive source review, not an edit of the historical candidate 1 review.

**Source disposition: ACCEPT_SCOPED_SOURCE, with formal execution still UNCONFIRMED.** Candidate 2 addresses both source-derived elaboration concerns in the preliminary review without changing any public statement or assumption. No blocking mathematical source issue remains identified at this finite endpoint. Compilation, complete local-origin declaration/axiom census, named-module kernel checks, negative controls and exact hosted artifact verification remain separate gates.

## Exact successor and unchanged scope

Candidate 2 is `project/CriticalRidge.lean`, 8149 bytes, SHA-256 `b3c22e590f761953ba322ad2903978e3982179204ad5c4a166dffc5fa1558322`. I freshly hashed the working source and its same-hash snapshot under `execution/author/source-attempts`; both match. Its predecessor is candidate 1, 7922 bytes, SHA-256 `729b57030c9d595b6ee9061b7cc6c730a6de713044ab0f7509637ed029771375`.

I read the author freeze and diff, and independently compared the two frozen source snapshots. The observed difference consists of exactly two proof-body changes. The stored `execution/author/CANDIDATE2.diff` freshly hashes to `ae861fed21ed6ad6a8f24daf974971cbe200173663e880a1d5f8c5d13273fe40`. The comparison command's exit status 1 denotes observed file differences, not a failed mathematical check.

The four definitions, five theorem statements, public hypotheses and all four conclusions for the same selected ridge are unchanged. The detailed proof reconstruction, local-versus-global scope analysis, independent adversarial examples, source reuse and paper-byte qualifications in `c299_nonauthor_preliminary_candidate1.md` therefore continue to apply. That historical report is 16507 bytes, SHA-256 `3d95edee47d2349fa1aa4c2dff6be5ad798dbc0dd40a0eabc60f2250b7489701`.

## Assessment of the two changes

1. The first change introduces a derivative assertion at the actual inner-map value `p + ridgeAddition V 0`, obtained from the derivative at `p` by `map_zero` and `add_zero`, and uses it in the chain rule. This resolves the base-point mismatch identified as F1. The derivative map and mathematical argument are unchanged.
2. The second change replaces the restricted-block proof's `rfl` with simplification after extensionality, explicitly unfolding the structural maps. This accounts for the `0 + v = v` identity identified as F2. It proves the same block identity and introduces no additional assumption.

These source changes address the identified concerns in the expected mathematical way. I have not executed their Lean elaboration and do not claim that every remaining typeclass or tactic obligation has compiled. The initial findings were predictions from source, and candidate 1's actual execution produced no diagnostic confirming them.

## Historical execution evidence

I fully read candidate 1's terminal receipt and freshly hashed it: `execution/author/runs/20261020T134843Z-89c13163/RECEIPT.json`, SHA-256 `6db1db80b14045d5b964658b76aa620fa512a960aab1e767e853cb7a97e92c45`. It records:

- Start: `2026-10-20T13:48:43.888892+00:00`.
- End: `2026-10-20T13:58:43.933989+00:00`.
- Elapsed seconds: `600.041933625`.
- `returncode: -15`, `timed_out: true`, and `source_unchanged: true`.
- Both stream hashes equal the empty-file SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; I independently rehashed both files and confirmed that equality.

This is an inconclusive bounded compile attempt. It is neither a proof result nor a refutation, and the empty streams do not locate the precise point of the stall. The author freeze separately records no resulting object; the terminal receipt itself does not contain an object-inventory field. No native retry or candidate 2 execution was performed by this reviewer. The author freeze declares that candidate 2 had not been executed when frozen.

## Attribution and limits

I remain the nonauthor reviewer. I inspected frozen source, reported defects and evaluated the author's subsequent changes; I did not edit the implementation or supply a replacement proof. Review adds mathematical reconstruction and adversarial analysis. Source exposed, same provider, organizational independence credit 0, blind review 0, human review 0, scientific effect NONE. No review by Dylan is implied.

This source acceptance covers only the negative partial-gradient ridge and its differentiated equation. Reduced positivity, uniform signs, fiber concavity, tubes, paths, critical neighborhood basis, Euclidean full LPC, quotient transport, C294 premise discharge, full ordinary bars and scientific obligations remain OPEN. The broader goal remains ACTIVE_UNMET.
