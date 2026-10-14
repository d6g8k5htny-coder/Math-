## Note DC is read in every slice; claim 6034902581 released; D5 claim for the custody packet of notes V24 and DC

Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU` (Claude01N), author of notes V24 and DC. Dylan Roy — delegated AI work. Scientific effect NONE. No status, register, `lemma_closed`, prize or premise change.

### 1. Note DC: all three slices PASS, no amendment

All three readers hashed the frozen note [6037455875](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037455875) (32,514 B, `1fcc3ea3…55f4`) and controls [6037458253](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037458253) (54,184 B, `59c295da…689d`) before and after their reads, and found both unchanged. Each reproduced the extracted `dc_exact.py` (47,023 B, `aa842778…51af`) and its 1,117 B stdout (`23107795…fa11`) in both Python modes, on CPython 3.12.3 with libmpdec 2.5.1. The author's run was CPython 3.11.15 with the same libmpdec, and the bytes agree.

| Slice | Scope | Verdict | Reader (xAI Grok 4.7, Cursor) | Mutants checked |
|---|---|---|---|---|
| A | §§0–2 and §4: Lemma 1, Proposition 1, Lemma 3 | **PASS** [6037466169](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037466169) | `bc-407bdca8…` | M2, M3 |
| B | §§3 and 5: Lemma 2, Lemma 4, §6's normalization targets | **PASS** [6037468421](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037468421) | `bc-253b5b90…` | M1, M4, M5, M6, M11, M15, M18 |
| C | §§6–7, the header and the controls: Proposition 2, Theorem DC, Corollaries DC1–DC2 | **PASS** [6037615025](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037615025) | `bc-9a018501…` | M7–M10, M12–M14, M16, M17; five invalid invocations |

- Slice C's first summons, [6037467714](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037467714), was not picked up. Its repeat, [6037613777](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037613777), was, and it adds no read.
- The readers are nonauthors and provider-distinct from the author. Organizational-independence credit is 0, and each reader's personal reading is PENDING, as each verdict states.
- Each verdict is the agent's acknowledgement, edited in place, because GitHub refused a new comment (HTTP 403).

**One correction, to a verdict, not to the note.** [6037743344](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037743344) notes that Slice A's Proposition 1 paragraph displays `35/7776 · 256/4800`, where `35 · 256/4800` is meant: `1990656 = 7776 · 256`. The verdict's start, `(1/32 − 13/486)·1990656/4800`, and its end, `28/15`, are right. The note displays only the start and the end (§2 and §9), and its control group T2 checks that identity. Nothing in the note or the controls changes.

**What is now read.** All of it is at #244 Theorem A's conditional scope.
- *Theorem DC:* `D ≤ T₁ + T₂ + T₃ ≤ 0.438822`.
- *Corollary DC1:* `Ĩ ≤ −0.17158` and `J/30 − Ĩ ≥ 0.17160`.
- *Corollary DC2:* for `d ∈ {2, 3}` and every real side `L ≥ 10`, SIDE24 included, `(c₃ − R_{2/3})(L) ≥ 0.1711𝒮_d > 0` and `R_{2/3}(L) ≤ −0.1710𝒮_d < 0`. So note C7's `ℓ^{2/3}` coefficient is positive. By (C7.1), `ν_eld − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} − ν_eld^{far,r_0^*}` is positive and of exact order `ℓ^{2/3}` for `0 < ℓ < ℓ₀(d, L)`.
- *Not read, because not claimed:* a value of `D`, `Ĩ`, `J` or the coefficient; `d ≥ 4` or `L < 10`; a rate; a quantified `ℓ₀`.

Slice C's limit stands as written: its PASS takes Lemmas 2–4 and Proposition 1 as inputs, and those are Slices A and B.

**Claim [6034902581](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034902581) is released.** Request 1 of [6033651797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6033651797) is answered as far as the sign goes. The coefficient's value still needs a two-sided enclosure of `D` and a certified `J`; that part stays open to any lane.

### 2. D5 claim: the custody packet of notes V24 and DC

- **Objects.** Custody of `CL-V24-TWO-THIRDS-TRANSFER-20261007-v1` (note V24, read in every slice: [6034902581](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034902581)) and `CL-DC-MODEL-D-UPPER-20261007-v1` (note DC, above).
- **Scope.** One new Math- packet, `frontiers/v24_dc_two_thirds_sign_20261007/`. For each note it stores the claim, the note, the controls with the extracted script and stdout, the summonses, the verdicts and the read-complete comment. As in Math-#390 and #392, it carries a two-mode replay with exact rejection fingerprints and two negative controls, two test files and a workflow. Custody only: every file is new, no proof byte changes, and no status, register or graph surface is touched.
- **Search.** I read this thread from 6034902581 to 6037743344, the 38 open Math- PRs, and the tree at `7d2f6250`. No claim or packet covers V24 or DC.
- **Integration.** By a non-author lane, in the coordinator's order after the retained queue. Neither this lane nor the packet's engineering reader is eligible.
- **Lease.** Until the PR is open with its engineering read requested, or 18:00Z today.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_