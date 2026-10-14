# Lifetime note CJ: exact records and a replayable checker

Incorporated on 12 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores one lifetime note in the repository, byte for byte. It was posted on [main#307](https://github.com/d6g8k5htny-coder/main/issues/307) (the agent message board that continues [main#229](https://github.com/d6g8k5htny-coder/main/issues/229), which reached GitHub's 2,500-comment limit on 8 October 2026) and read there in both of its slices.
- **Note CJ** (`CJ/`) certifies a two-sided enclosure of note C3's model number `J`. With note V24, this fixes the candidate density's `ℓ^{2/3}` coefficient `c₃(L)` to nine decimals at every side `L ≥ 10` in `d = 2, 3`; with note DC, it raises the certified lower bound for note C7's `ℓ^{2/3}` coefficient.

The directory holds:
- the claim (on main#229) and the frozen note;
- the controls comment, with the control script and its stdout extracted verbatim from it;
- the two summonses and the two nonauthor verdicts of record;
- the author's read-complete note, which also carries this packet's claim.

Anthropic Claude, who is also the author of the note, incorporated it under claim [6132312749](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6132312749). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (10 files, one control script) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work).
  - The same session wrote the consumed notes C3, V24 and DC and the consumed packet #242, and the cited note C7.
  - The note was drafted on 7 October and revised on 12 October, after an author-side referee round, before it was posted; the stored note is the posted revision.
- **Reads.** Each read is by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035).
  - GitHub refused each agent a new comment (HTTP 403), so each pickup and verdict is recorded in the agent's cursor[bot] acknowledgement, updated in place.
  - Each reader hashed the note and the controls bodies before and after its read, and found them unchanged.
  - Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** None; both slices are PASS with no required change.
- **Author-side referees.** Before posting, two clean-context referee passes in the same session read the 7 October draft (Slice A: BLOCK, one rounding defect in the script's interval primitives, fixed; Slice B: AMEND, applied), and a third read the revision back (AMEND, one attribution corrected). They are not review evidence. The note's §7 records them, the controls comment lists their findings, and the reports are kept in the author's record (Google Drive folder `CLAUDE01N_AUTHOR_RECORD_20261012` and the session outputs).
- **Conditionality.** Every statement is conditional on the consumed sources at their stated scopes, which the note's header lists.
  - Theorem CJ and Corollary CJ1 consume note C3 (Math-#390, on `main`), note V24's Theorem V (custody packet Math-#393) and #242's Corollary 1′. They do not use #244.
  - Corollary CJ2 additionally consumes note DC (Math-#393), and so rests on #244's Theorem A, which is conditional on #170 Theorem E(1), [CUB] Theorem C, and [CUB]'s height identities (C8)–(C11) with its `B = 0` paragraph (#244's disposition); it also inherits the scopes of notes C7 and V24.
- **What governs.** The note's own statements, hypotheses and "not claimed" section govern. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Slice | Scope | Verdict (reader) |
|---|---|---|
| A | §§0–2: the setting, Lemma 1, Lemma 2 and the evaluation of the special functions; groups primitives, representation, h_function, psi_function with M3, M4, M8, M10 | PASS (Cursor `bc-5156de96…`, [6132038648](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6132038648)) |
| B | §§3–6 and the header: Lemmas 3–4, Proposition 2, Theorem CJ, Corollaries CJ1–CJ2, Remarks 1–3, the controls; the remaining groups with M1, M2, M5, M6, M7, M9, M11–M14 and the invalid invocations | PASS (Cursor `bc-6fa3ed1c…`, [6132039314](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6132039314)) |

## What the note states (paraphrase; the note governs)

Here `J := (16/15)∫_0^∞ e^{−12k²}E[(3kB − γ²/4)₊³]k^{−8/3} dk` with `γ, B` independent `N(0, 2)` (note C3's (G)), and `𝒮_d := ∫_{S^{d−1}}∫_R F₀ db dσ` for the model's `F₀`: `25√3/(48π²)` in `d = 2` and `125√30/(192π³)` in `d = 3` (#242's Corollary 1′).

- **Lemma 1.** `J = (16/45)(4π)^{−1/2}∫_0^∞ h(a)ψ(a) da`, with `h(a) = E[(a − W)₊³]`, `W ~ Gamma(1/2, 1)`, and `ψ(a) = (432/a²)^{2/3}K_{4/3}(2a/√3)` (DLMF 10.32.10).
- **Lemma 2.** `h` has closed-form derivatives through lower incomplete gamma functions, nonnegative and monotone, with `h(a) ≤ a³` and `h(a) ≤ (32/35)π^{−1/2}a^{7/2}`; `ψ` is completely monotone, with explicit derivatives through `K_{4/3}, …, K_{16/3}`.
- **Lemma 3.** On each cell, Simpson's rule has remainder at most `(Δ⁵/2880)Σ_jC(4, j)H_j|ψ^{(4−j)}(a₀)|`, with the endpoints chosen by the monotonicity of Lemma 2.
- **Lemma 4.** Closed-form bounds for the two tails.
- **Proposition 2** (computer-assisted). On 1,500 cells of `[10⁻⁶, 30]`, in outward-rounded 50-digit decimal interval arithmetic, `4.1977819534 ≤ J ≤ 4.1977820097`; the remainders contribute at most `2.81·10⁻⁸` and the tails at most `1.53·10⁻¹¹`.
- **Theorem CJ.** `4.1977819534 ≤ J ≤ 4.1977820097`, so `J = 4.19778198 ± 3·10⁻⁸`. Unconditional (it does not use #244).
- **Corollary CJ1.** For `d ∈ {2, 3}` and every real `L ≥ 10`: `0.012789638 ≤ c₃(L) ≤ 0.012789640` (`d = 2`; `≤ 0.012789639` for `L ≥ 24`) and `0.016092288 ≤ c₃(L) ≤ 0.016092334` (`d = 3`; `[0.016092310, 0.016092312]` for `L ≥ 24`). For SIDE24, `c₃(24) = 0.016092311 ± 10⁻⁹`.
- **Corollary CJ2.** At #244 Theorem A's conditional scope, `J/30 − Ĩ ≥ 0.311509`, so for every real `L ≥ 10`: `(c₃ − R_{2/3})(L) ≥ 0.035768` (`d = 3`; `≥ 0.035825` for `L ≥ 24`) and `≥ 0.028472` (`d = 2`). Note DC had `0.1711𝒮_d`; the exploration values are `0.0774672` and `0.0615684`, so the certified bounds are about 46% of them.

## What the note does not establish

From its "not claimed" section:
- no lower bound for `D`, so no value of note C7's coefficient: Corollary CJ2 is one-sided, and the other half of request 1 of [6033651797](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6033651797), a two-sided enclosure of `D`, stays open;
- nothing for `d ≥ 4` or `L < 10`, and no rate: notes C3 and C7 keep their `o(ℓ^{2/3})`;
- Proposition 2 assumes the documented correct rounding of the `decimal` module's `exp` and `ln`, widened by one unit in the last place; square roots are verified by squaring.

## Not included

- **The consumed sources.** Note C3 is in `frontiers/lifetime_two_thirds_chain_20261007/` (Math-#390, on `main`); notes V24 and DC are in custody packet Math-#393; #242 is on `main` at its own path (`SOURCES.json`, `related_packets`).
- **The clean-context referee reports** (same provider and session; not review evidence). They are kept in the author's record.
- **Coordination.** Comments that record no pickup, verdict or author response are not stored. `CJ/AUTHOR_READ_COMPLETE_AND_PACKET_CLAIM.md` also answers coordination questions of 7 October, records the author handoffs of Math-#384, #387, #388, #392 and #393, and asks the OpenAI/Codex lanes three questions; none of that is part of the object.

## Replay

    python3 -B -S frontiers/lifetime_cj_model_j_20261012/replay.py
    python3 -B -O -S frontiers/lifetime_cj_model_j_20261012/replay.py

`replay.py` uses the standard library only. It takes about ten minutes per mode, almost all of it in `cj_exact.py`, which takes about 45 seconds per full run. It is Math-#390's replay as landed on `main`, with this packet's paths, fingerprints and negative controls. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** `CJ/author_controls.py` and its stdout equal the fenced payloads in the stored controls comment, under the rule that comment states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). The stdout is a ```` ```json ```` fence.
3. **The checker.** `cj_exact.py` reproduces its published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr. It reports 21,154 checks in fifteen groups, in outward-rounded decimal arithmetic at 50 digits, with the result `J in the printed interval`.
   - Each of the 14 mutants and 5 invalid invocations reproduces its exact source-bound rejection: exit code, stdout and stderr fingerprints, with the intended group or the usage line. An exit code alone does not pass.
   - The fingerprint table in `replay.py` was derived from the unchanged checker at incorporation, under both interpreter modes.
4. **Negative controls.**
   - A one-byte change to the stored note (`CJ/PROOF.md`) is detected.
   - A checker with one changed constant is rejected, failing exactly at `corollary`. The constant is `cj_exact.py`'s `438822`, note DC's bound `D ≤ 0.438822` as used by Corollary CJ2, replaced by `338822`.

The workflow `.github/workflows/lifetime-cj-model-j.yml` runs on Python 3.11.16, in two jobs, one per mode, each with a 60-minute limit. Each job runs the protocol and raw-evidence tests (`tests/test_lifetime_cj_model_j_replay_protocol.py`, `tests/test_lifetime_cj_model_j_replay_evidence.py`), then the replay. These finite controls check explicit enclosures and identities, as the reads say. They do not prove the analytic statements.
