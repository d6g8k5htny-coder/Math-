# Nonauthor re-review — main PR124 C1/C2 repair only

Scientific effect: **NONE**. This file does not change `lemma_closed`, prizes, premises, claim graphs, or any scientific-status register. It does not accept a cubic envelope, a numerical `C`, an unconditional limit for `q_MS`, or a full-Gaussian corollary. C3–C8 are not re-reviewed.

## Binding

| Field | Value |
|---|---|
| Object | [main pull request 124](https://github.com/d6g8k5htny-coder/main/pull/124), head `cursor/q0-c103-c1-c2-repair-31c5` |
| Exact tip | `a380dcfb8f4a13e13ae8e13deb5d870dd8b75b25` |
| Repair parent | `a14aa4f2d90ebc7650fd2b9209d681e64dbd983c` |
| Successor path | `research/q0/Q0_C103_SOURCE_BOUND_CUBIC_RATE.md` |
| Successor blob | `85e00f317b01fd04ab51df9a9f7c6fead28e87a2` |
| Successor size / SHA256 | 11330 bytes / `da6a24fdddcea27621a121450e05c4e9d38db704d3a6a492311a0677aee0997b` |
| Source map path | `research/q0/Q0_C103_SOURCE_MAP.json` |
| Source map blob | `6b1f97ad67518cd105274fd9e1e269a4e46ccf2e` |
| Source map size / SHA256 | 4558 bytes / `ea81ae44d8007516184c9a8005fc3c65929f1a17c1cb58eb0f4bcf2fcb0cee04` |
| Prior C1–C8 review | main pull request 121 comment `5841690735` |
| Lane | C1 and C2 only. The release spelling PREMISS-Z-LOWER is the successor’s `PREMISE-Z-LOWER` |

The tip was read after `gh pr view 124` returned head `a380dcfb8f4a13e13ae8e13deb5d870dd8b75b25`. No later commit was on the branch.

## Reviewer provenance

| Field | Value |
|---|---|
| Provider | xAI |
| Model | Grok 4.7 (`grok-4.7-high-fast`) |
| Agent | Cursor cloud run `bc-532d8628-0226-4e51-b1d5-f629285e0f36` |
| Run URL | https://cursor.com/agents/bc-532d8628-0226-4e51-b1d5-f629285e0f36 |
| Account wrapper | Cursor application, owning user Electric_Universe_Theory |

Organizational independence is **not awarded**. The repair commit on PR124 is also a Cursor cloud session (`bc-01a0d95b-e593-75f4-a1b1-d440961231c5`). This is a later session, not that authoring session. A second Cursor session is not organizational independence.

No child agent was spawned. The author proof was not edited. C3–C8 regional arithmetic was not re-decided.

## Verdicts

| Slice | Verdict | What this tip actually does |
|---|---|---|
| C1 Branch-attached inclusion | **AMEND** | The false unconditional inclusion is withdrawn, and `H_branch` matches the C102 theorem setup. The displayed cubic inequality still uses `1 - q_MS` and concludes `q_MS → 1` on the `H_branch`-conditioned law. That conditional probability does not follow from the event inclusion. |
| C2 `PREMISE-Z-LOWER` | **ACCEPT** | `Z_r ≥ c r^2` on `0 < r ≤ 0.025` is named, unresolved, and required wherever a regional estimate divides by `Z_r`. It is not given a proof in this tip. |

C3–C8 have no verdict in this record. SARD-G stays where the successor left it (`HOLD-WITH-DOMAIN`); that gate was not re-opened.

## C1 — AMEND

### What is removed

C102, blob `25917befb388211e3848b00c5ba90670e9b716b0`, opens by assuming a Morse function with distinct critical values and a Morse–Smale gradient, and then:

> Let `M` be a local maximum and `S` an index-one saddle such that one ascending branch of `S` terminates at `M`.

Only after that attachment does the boxed theorem give `{D(M) ≠ S} ⊂ Π ∪ Γ`. The same file’s “Exact relation to the C101 decomposition” restates the inclusion under Morse–Smale and distinct critical values alone. That restatement drops the attachment. It is the false transfer cited in comment `5841690735`.

The successor does not adopt that restatement. Section 1.1, Section 3, the C1 paragraph, and the source map all consume the inclusion only with `H_branch` plus Morse, distinct critical values, and Morse–Smale. `H_branch` is the C102 sentence above: one ascending branch of `S` terminates at `M`. The map records `controlling_alias_to_historical_q: false`. `B_miss` is defined as neither ascending branch terminating at `M`, and the tip gives it no `O(r^3)` envelope. Section 3 says the inclusion is not claimed for the unconditioned typed pair-Palm law. Those sentences do withdraw the false unconditional inclusion.

The successor writes `subseteq` where C102 proves `subset`. The subset relation implies the subseteq relation used for an upper bound. That widening is not the defect.

### What does not follow

Section 1 defines

```text
q_MS(r,b) := P_MS(r,b){ D(M) = S }
```

on the typed pair-Palm law, before any branch conditioning. On that law,

```text
1 - q_MS = P((D(M) ≠ S) ∩ H_branch) + P(B_miss).
```

C102’s theorem gives the joint inclusion

```text
(D(M) ≠ S) ∩ H_branch  ⊆  Π ∪ Γ,
```

and therefore

```text
P((D(M) ≠ S) ∩ H_branch) ≤ P(Π) + P(Γ).
```

The conditional probability is a different quotient:

```text
P(D(M) ≠ S | H_branch) = P((D(M) ≠ S) ∩ H_branch) / P(H_branch)
                        ≤ (P(Π) + P(Γ)) / P(H_branch).
```

Section 2 displays `0 ≤ 1 - q_MS(r,6/5) ≤ C r^3` “on the `H_branch`-conditioned typed pair-Palm law” and concludes `q_MS(r,6/5) → 1`. Section 3 displays `1 - q_MS ≤ P_MS(Π) + P_MS(Γ)` “on the `H_branch` event”. Section 7 repeats the conditional limit. None of these displays is the joint inequality above.

`P(H_branch) ≥ c > 0` is not in the tip. It would be an upper bound `P(B_miss) ≤ 1 - c`. The same tip says `B_miss` has no source-bound cubic envelope and that the squeeze does not bound `B_miss`. Without a positive lower bound on `P(H_branch)`, an `O(r^3)` bound on `P(Π)` and `P(Γ)` does not bound the conditional defect probability. A schematic measure with `P(H_branch) = r^6`, `P((D(M) ≠ S) ∩ H_branch) = r^6`, and `P(Π ∪ Γ) = r^3` obeys the joint inclusion and still has conditional defect probability `1`.

Reading the left-hand side as the Section 1 symbol instead, unconditioned `1 - q_MS` still contains `P(B_miss)`, which the tip refuses to bound. The surrounding sentence does not change that symbol.

### Required amendment

Keep the withdrawal of the unconditional inclusion. Replace the displayed cubic lines in Sections 2, 3, and 7 with the joint bound

```text
P_MS( (D(M) ≠ S) ∩ H_branch ) ≤ P_MS(Π ∪ Γ) ≤ P_MS(Π) + P_MS(Γ)
```

on the typed pair-Palm law of Section 1. Do not conclude `q_MS → 1`, on the conditioned law or off it, in this tip. A conditional limit needs a separately named premise `P_MS(H_branch) ≥ c > 0`, and that premise must not be marked proved. This amendment does not ask for a new `Π` or `Γ` estimate and does not reopen C3–C8.

## C2 — ACCEPT

`PREMISE-Z-LOWER` is the statement: there exists `c > 0` such that `Z_r ≥ c r^2` for every `0 < r ≤ 0.025`, at mark `b = 6/5` under the six-pin typed law. The successor isolates it at every load-bearing use:

| Place | Status in this tip |
|---|---|
| Section 2, hypothesis 4 | Explicit hypothesis of the conditional theorem |
| Section 2, closing sentence | Without it, the tip does not assert the cubic envelope |
| Section 4, C2 paragraph | “unresolved in this tip”; “No source-bound proof”; every division by `Z_r` is conditional on it |
| Section 4, singular ledger | “assuming PREMISE-Z-LOWER”; “premise, not proved here”; without it the division is not discharged |
| Section 4, collar paragraph | The inherited `r^2` normalizer step is “read under PREMISE-Z-LOWER” |
| Section 5 | Conditional theorem assumes it |
| Section 7 | The squeeze does not discharge it |
| Section 8 | Named unresolved premise “rather than treating it as proved” |
| Source map `gates.PREMISE_Z_LOWER` | `UNRESOLVED` |
| Source map note on C101 | The source assertion “is PREMISE-Z-LOWER here, not discharged” |

The numerator bound is not used as a substitute. Section 4 records `det H_M, det H_S = O(r)`, hence `W_MS = O(r^2)`. That is an upper bound on the weight. It matches C098’s pair-weight scaling and does not lower-bound `Z_r = E[W_MS | J_6]`.

The sources that mention a floor do not become proofs by being mapped:

- C098, blob `3e3037b6dbe57d98b7b5932fb1db62b8e8c29ea6`, calls positivity of the limiting `z_0` “the load-bearing mathematical input” and marks the `3.230979` three-row table diagnostic. The successor repeats that distinction and says this input is not a proved uniform floor.
- C098’s later line `inf z_r > 0` and C100’s line `Z_r = r^2 z_r` with `inf_{0<r≤0.025} z_r > 0` (blob `04d6e1c5a012d1a0e87abe8c9c2e3f7e921478a8`) are assertions in those files. C100 Section 4 states the floor and then uses it; it does not derive it there.
- C101 Section 6, blob `1daec2574e2505ab8162c9a36d8beead34360dd0`, states `Z_r ≥ c r^2` and multiplies. No derivation of that inequality appears before that sentence.

The successor cites those blobs and labels the floor unresolved. The diagnostic limit `z_0 > 0` is not promoted to `inf_{r≤0.025} Z_r / r^2 > 0`. C5’s exterior division is not rewritten; the C2 paragraph already makes every regional division conditional on the premise, and C5 is marked review-pending. That is isolation, not a discharge, and it is not a C5 verdict.

## Out of scope

C3 through C8, the singular exponent arithmetic, the chart atlas, finite-jet nondegeneracy, and Clarifications A and C were not re-audited. No claim status moves. `q_MS` remains unbound from historical adjacency `q`.
