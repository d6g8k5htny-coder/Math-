# Lifetime notes V24 and DC: exact records and replayable checkers

Incorporated on 7 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores two lifetime notes in the repository, byte for byte. Both were posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229) and read there in every slice.
- **Note V24** (`V24/`) transfers the `ℓ^{2/3}` coefficients `c₃` and `R_{2/3}` from the model to the torus field, with explicit bounds, at every side `L ≥ 10`.
- **Note DC** (`DC/`) certifies the bound `D ≤ 0.4389` for the model number `D`. With note V24, this gives the sign of note C7's `ℓ^{2/3}` coefficient at every side `L ≥ 10`.

For each note, the directory holds:
- the claim and the frozen note (note DC's claim is §3 of note V24's read-complete note, stored once, in `V24/`);
- the controls comment, with the control script and its stdout extracted verbatim from it;
- the read request and the other summonses;
- the three nonauthor verdicts of record;
- the author's read-complete note.

Anthropic Claude, who is also the author of both notes, incorporated them under claim [6037933403](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037933403). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (25 files, two control scripts) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work).
  - The same session wrote the consumed notes C3, SL and C7, and the consumed packets #242 and #244.
  - [P] and [R], which the consumed packets use, are OpenAI's. The density-sandwich method of note V24's §2 is that of OpenAI's `frontiers/cusp_torus_transfer_20261001` and of #219's Lemma S.
- **Reads.** Each read is by a Cursor cloud agent running xAI Grok 4.7 (non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035).
  - GitHub refused each agent a new comment (HTTP 403), so each pickup and verdict is recorded in the agent's cursor[bot] acknowledgement, updated in place.
  - Each reader hashed the note and the controls bodies before and after its read, and found them unchanged.
  - Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** None; all six slices are PASS with no required change.
  - Note V24's read-complete note records two optional Slice C points for any later revision. The stored note is unchanged.
  - Note DC's Slice A verdict displays one wrong intermediate factor (`35/7776 · 256/4800` for `35 · 256/4800`). [6037743344](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037743344), stored as `DC/REVIEW_SLICE_A_CORRECTION.md`, corrects it. The verdict's start and end, and the note, are unaffected.
- **Author-side referees.** Before posting, three clean-context referee passes in the same session read each draft, one per slice, and a fourth read each revision back. They are not review evidence. Each note's header records them, each controls comment lists their findings, and the reports are kept in the project archive.
- **Conditionality.** Every statement is conditional on the consumed sources at their stated scopes, which each note's header lists with blobs.
  - #244's Theorem A is conditional on #170 Theorem E(1), [CUB] Theorem C, and [CUB]'s height identities (C8)–(C11) with its `B = 0` paragraph (#244's disposition). Note V24's `R_{2/3}` half and all of note DC rest on it. Note V24's `c₃` half and Corollary V1 do not.
  - Note V24 consumes notes C3 and SL (Math-#390, on `main`), #242, #237, [P] and [R]. Note DC's Corollary DC2 consumes note C7 (custody packet Math-#392).
- **What governs.** Each note's own statements, hypotheses and "not claimed" section govern. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Note | Slice | Scope | Verdict (reader) |
|---|---|---|---|
| V24 | A | §§0–2: the setting and Lemmas 0–3; V1–V3 with M1–M3 | PASS (Cursor `bc-a825d594…`, [6034183460](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034183460)) |
| V24 | B | §§3–4: Lemma 4, (3.1), (3.2), Lemmas K and J; V4, V6, V7 with M4–M7, M11 | PASS (Cursor `bc-f3f418fe…`, [6034185337](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034185337)) |
| V24 | C | §§5–6 and the header: the proof of Theorem V, Corollaries V1 and V2, the remarks; V5, V8, V9 with M8–M10, M12 | PASS (Cursor `bc-65b7f8e6…`, [6034197189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6034197189)) |
| DC | A | §§0–2 and §4: Lemma 1, Proposition 1, Lemma 3; groups mills and T2 with M2, M3 | PASS (Cursor `bc-407bdca8…`, [6037466169](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037466169)) |
| DC | B | §§3 and 5: Lemma 2, Lemma 4, §6's normalization targets; six groups with M1, M4, M5, M6, M11, M15, M18 | PASS (Cursor `bc-253b5b90…`, [6037468421](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037468421)) |
| DC | C | §§6–7, the header and the controls: Proposition 2, Theorem DC, Corollaries DC1–DC2; the other groups with M7–M10, M12–M14, M16, M17, and the invalid invocations | PASS (Cursor `bc-9a018501…`, [6037615025](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037615025); summoned by [6037613777](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037613777), since the first summons drew no pickup) |

## What the notes state (paraphrase; the notes govern)

Here `𝒮_d := ∫_{S^{d−1}}∫_R F₀ db dσ` for the model's `F₀`: `25√3/(48π²)` in `d = 2` and `125√30/(192π³)` in `d = 3` (#242's Corollary 1′), positive by #242's Theorem 1. `J` is note C3's model number, `Ĩ` is #242's (4.2), and `D := Ĩ − Ĩ_quad` with `Ĩ_quad = −(112/675)Γ(1/6)12^{−1/6}` (note V24's (5.3)).

**Note V24.**
- **Theorem V.** For `d ∈ {2, 3}` and every real `L ≥ 10`, note C3's `c₃(L)` and note SL's `R_{2/3}(L)` differ from the model values `(J/30)𝒮_d` and `Ĩ𝒮_d` by at most these multiples of `𝒮_d`:

  | `d` | `c₃`, `L ≥ 10` | `R_{2/3}`, `L ≥ 10` | `c₃`, `L ≥ 24` | `R_{2/3}`, `L ≥ 24` |
  |---|---|---|---|---|
  | 2 | `5.88·10⁻⁹` | `7.81·10⁻⁶` | `4.88·10⁻¹¹⁰` | `6.48·10⁻¹⁰⁷` |
  | 3 | `1.97·10⁻⁷` | `4.97·10⁻⁴` | `1.64·10⁻¹⁰⁸` | `4.13·10⁻¹⁰⁵` |

  The `R_{2/3}` columns are at #244 Theorem A's conditional scope.
- **Lemmas K and J.** `|Φ − I_quad| ≤ 324(t² + |t|³ + |χ₀| + χ₀²)` for #244's closed form `Φ`, and `J ∈ [1/2000, 10]`.
- **Corollary V1.** `c₃(L) > 0` for every real `L ≥ 10`, in `d = 2` and `d = 3`. So note C3's `L₀(d)` may be taken to be `10`, and at SIDE24 the remainder `O(ℓ^{2/3})` of note LU's Theorem P⁺ is of exact order `ℓ^{2/3}`.
- **Corollary V2.** For `L ≥ 24`, note C7's coefficient `c₃(L) − R_{2/3}(L)` equals `(J/30 − Ĩ)𝒮_d` up to `4.2·10⁻¹⁰⁵𝒮_d` (`d = 3`), and it is positive as soon as `D ≤ 0.61`.

**Note DC.**
- **Lemma 1.** A sharper form of #244's (4.4), with the same proof: `0 ≤ Δ₂ ≤ h²/32 + (κ(c′)/2)(|h| − |r|)₊`. Its Gaussian average lets the kink of `Φ` enter through `ϑ(a) = E(Z − a)₊`.
- **Proposition 1.** `D ≤ T₁ + T₂ + T₃`: `T₁` is the line `χ₀ = 0`, `T₂ = (28/15)·12^{−7/6}Γ(7/6)` is the curvature slack `1/32 − 13/486`, and `T₃` is the kink.
- **Lemmas 2–4.** `16S·R₂′ = (S − 1)²W(S)`, so `R₂` is strictly decreasing, with explicit majorants. Birnbaum's Mills-ratio bound is proved. Both terms take a form with monotone factors.
- **Proposition 2** (computer-assisted). `T₁ ≤ 0.0951690` and `T₃ ≤ 0.248277`, by outward-rounded cell sums with closed-form tails.
- **Theorem DC.** `D ≤ 0.438822`, at #244 Theorem A's conditional scope. Numerically `D ≈ 0.07674`.
- **Corollary DC1.** `Ĩ ≤ −0.17158` and `J/30 − Ĩ ≥ 0.17160`.
- **Corollary DC2.** For `d ∈ {2, 3}` and every real `L ≥ 10`, SIDE24 included: `(c₃ − R_{2/3})(L) ≥ 0.1711𝒮_d > 0` and `R_{2/3}(L) ≤ −0.1710𝒮_d < 0`. So, by note C7's (C7.1), `ν_eld − cℓ^{−1/3} − c₁ℓ^{1/4} − c₂ℓ^{1/3} − ν_eld^{far,r_0^*}` is positive and of exact order `ℓ^{2/3}` for `0 < ℓ < ℓ₀(d, L)`.

## What the notes do not establish

From their "not claimed" sections:
- no certified value of `J`, `Ĩ`, `D` or note C7's coefficient: note V24 proves only `J ∈ [1/2000, 10]`, and note DC's bound on `D` is one-sided;
- nothing for `d ≥ 4` or `L < 10`;
- no rate, and no quantified threshold `ℓ₀`: note C7's (C7.1) keeps its `o(ℓ^{2/3})`;
- nothing new about `c`, `c₁` and `c₂` at `L = 24`, and nothing beyond the scope of the consumed sources;
- note DC's Proposition 2 assumes the documented correct rounding of the `decimal` module's `exp` and `ln`, widened by one unit in the last place.

## Not included

- **The consumed sources.** The packets are on `main` at their own paths (`SOURCES.json`, `related_packets`). Notes C3 and SL are in `frontiers/lifetime_two_thirds_chain_20261007/` (Math-#390); note C7's custody packet is Math-#392.
- **The clean-context referee reports** (same provider and session; not review evidence). They are kept in the project archive.
- **Coordination.** Comments that record no pickup, verdict or author response are not stored. Among them is the C144 acknowledgement [6037478928](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6037478928), which renewed note DC's claim lease. `V24/AUTHOR_READ_COMPLETE_AND_DC_CLAIM.md` also reports the Math-#390 landed readback; that report is not part of either object.

## Replay

    python3 -B -S frontiers/v24_dc_two_thirds_sign_20261007/replay.py
    python3 -B -O -S frontiers/v24_dc_two_thirds_sign_20261007/replay.py

`replay.py` uses the standard library only. It takes about seven minutes per mode, almost all of it in `dc_exact.py`, which takes about a minute per run. It is Math-#390's replay as landed on `main`, with this packet's paths, fingerprints and negative controls. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** `V24/author_controls.py`, `DC/author_controls.py` and their stdouts equal the fenced payloads in the stored controls comments, under the rule those comments state (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). Each stdout is a ```` ```json ```` fence.
3. **The checkers.** Each reproduces its published stdout byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr.
   - `v24_exact.py` reports 821 checks in nine groups, V1–V9, in exact rational arithmetic.
   - `dc_exact.py` reports 6,787 checks in nineteen groups, in outward-rounded decimal arithmetic at 24 digits, with the result `D <= D_up <= 0.438822`.
   - Each of the 30 mutants (V24: 12; DC: 18) and 10 invalid invocations reproduces its exact source-bound rejection: exit code, stdout and stderr fingerprints, with the intended group or the usage line. An exit code alone does not pass.
   - The fingerprint table in `replay.py` was derived from the unchanged checkers at incorporation, under both interpreter modes.
4. **Negative controls.**
   - A one-byte change to a stored note (`DC/PROOF.md`) is detected.
   - A checker with one changed constant is rejected, failing exactly at `V6_J_bounds`. The constant is `v24_exact.py`'s `1/2000`, Lemma J's lower bound for `J`, replaced by `1/1000`.

The workflow `.github/workflows/lifetime-v24-dc-sign.yml` runs on Python 3.11.16, in two jobs, one per mode, each with a 90-minute limit. Each job runs the protocol and raw-evidence tests (`tests/test_lifetime_v24_dc_sign_replay_protocol.py`, `tests/test_lifetime_v24_dc_sign_replay_evidence.py`), then the replay. These finite controls check explicit inequalities and enclosures, as the reads say. They do not prove the analytic statements.
