# Addendum EM.1 and lifetime notes LU, C3 and SL: exact records and a replayable checker

Incorporated on 7 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores four objects of the lifetime chain in the repository, byte for byte. Each was posted on [main#229](https://github.com/d6g8k5htny-coder/main/issues/229) and read there in every slice:
- **EM.1** (`EM1/`): addendum EM.1, the bad region of note EM's Lemma S‴ and the intermediate elder mass;
- **LU** (`LU/`): note LU, Lemma U for differences and the three densities with remainder `O(ℓ^{2/3})` up to a logarithm;
- **C3** (`C3/`): note C3, the `ℓ^{2/3}` term of the candidate density;
- **SL** (`SL/`): note SL, the rejected density's `ℓ^{2/3}` term on the soft layer `κ ≥ 1`, and the matching `F → F₀`.

Each directory holds the object's claim, the frozen note, the controls comment with the control script and its stdout extracted verbatim from it, the read request and summonses, every nonauthor verdict of record, and the author's read-complete note. LU's directory also holds the successor text for its one amendment and that text's readback. C3's also holds its exploration comment and the first Slice C summons, which drew no pickup.

Anthropic Claude, who is also the author of the four objects, incorporated them under claim [6028562633](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028562633). This is custody only; no proof byte is changed. `SOURCES.json` pins every stored file (45 files, four control scripts) by byte count and SHA-256, and `replay.py` verifies all of it.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work). The same session wrote notes TL, TS and EM and the consumed packets #187, #188, #207, #218, #220, #229, #237, #242, #243, #244 and [K]; [R] and [182] are OpenAI's.
- **Reads.** Each read is by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). GitHub refused each agent a new comment and an edit (HTTP 403), so each pickup and verdict is recorded in the agent's cursor[bot] acknowledgement, updated in place. Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** One, in note LU. The Slice B read [6025531584](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025531584) found that one bullet of `I₁` in §3 Step 3, the case `c_τ < 4η`, did not close: its bound `Cη² ≤ Cr²` used `sup p ≤ C/|Δ|` on a long interval. The author applied the exact change in the successor text [6026230530](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026230530) §2, which routes that case through the `f₄`-coordinate absorption. Its readback is PASS ([6026231785](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026231785)). No statement changes, and the stored note body and `lu_exact.py` are the frozen ones.
- **A recorded remark.** C3's Slice A read noted, as not a required change, that for `m = 1` the relation in §2 Step 4 is `σ_M ≤ α_M < 0` (equality when `β_M·e = 0`), not `σ_M < α_M < 0`. `σ_M < 0` and `Λ₂ = 0` are unaffected. The author recorded it in [6028351320](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028351320) (`SL/CLAIM.md`).
- **Author-side referees.** Before posting, clean-context referee passes in the same session read each draft (two slices for EM.1, three for LU and C3, one for SL). They are not review evidence. Each note's header records them, and the controls comments of C3 and SL list their findings; the reports are kept in the project archive.
- **Conditionality.** Every statement is conditional on the consumed sources at their stated scopes, which each note's header lists with blobs. Among them are note EM (custody packet Math-#388), note TS (Math-#387) and note TL (Math-#384), and LU consumes EM.1, C3 consumes LU.
- **What governs.** Each note's own statements, hypotheses and "not claimed" section govern; LU is read with its successor text. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Object | Slice | Scope | Verdict (reader) |
|---|---|---|---|
| EM.1 | A | §§0–1, §2 (a)–(c): Lemma V′, the shear, the cubic coefficient, Lemma X on the bad region; B1–B3 with M1, M2, M7, M8 | PASS (Cursor `bc-2a80b870…`, [6024106995](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024106995)) |
| EM.1 | B | §2 (d)–(e), §§3–4 and the header; B4–B5 with M3–M6 | PASS (Cursor `bc-18f6b872…`, [6024112289](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6024112289)) |
| LU | A | §§0–2: the statements, (0.2), Lemma S, Lemma E; L1–L3 with M1–M3, M7 | PASS (Cursor `bc-3848290a…`, [6025530037](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025530037)) |
| LU | B | §3: the proof of Lemma U₀; L6 with M6 | AMEND, one bullet of `I₁` (Cursor `bc-13c58f23…`, [6025531584](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025531584)) |
| LU | C | §§4–6 and the header: Theorem U⁼, Theorem P⁺, Corollary LU and its ledger; L4–L5 with M4–M5 | PASS (Cursor `bc-87b46e7a…`, [6025535376](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025535376)) |
| LU | readback | the successor text [6026230530](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026230530) §2 against the AMEND | PASS (Cursor `bc-0cf04834…`, [6026231785](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026231785)) |
| C3 | A | §§0–2: the statements, Lemma 0, (I.1)–(I.2), the proof of Lemma F₃; E1, E2, E7, E8 with M1, M2, M7, M8 | PASS (Cursor `bc-7582fb4c…`, [6027878271](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027878271)) |
| C3 | B | §§3–4: Lemma T₁, `a₁ = (1/10)∫F₀db`, the proof of Theorem C3; E5, E6, E9 with M5, M6, M9 | PASS (Cursor `bc-b7769d90…`, [6027885396](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027885396)) |
| C3 | C | §§5–6 and the header: Proposition G, Corollary G′, Proposition G″, Remarks 1–6; E3, E4, E5's (G.3) checks with M3, M4, M10 | PASS (Cursor `bc-4708b545…`, [6028019347](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028019347)) |
| SL | A | §§0–1: the statements and the proofs of Lemma SL₀, Corollary SL₁ and Theorem SL; S1–S4 with M1–M4 | PASS (Cursor `bc-7e9802f3…`, [6028372615](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028372615)) |
| SL | B | §2 and the header: Remarks 1–5, the sources, accuracy, attribution and overclaim | PASS (Cursor `bc-b3e1fc99…`, [6028379432](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6028379432)) |

## What the notes state (paraphrase; the notes govern)

The setting is the one of #237, note TS and note TL: `κ = k/r`, the lifetime is `ℓ = kr³`, `𝐓_r`, `𝐓_r^{eld}` and `𝐓_r^{rej}` are the candidate, elder and rejected kernels integrated over the birth height, and `𝓐`, `𝓐^{rej}` their cusp-scale limits.
- **EM.1.** Note EM's bad region (a soft transverse direction at `M`) costs no more than its good region, through EM's own Lemma X and a new small-ball estimate (V.4). So for `0 < k ≤ r²` (Theorem S‴⁺) the elder weight is `Cr²[rκ + r²κ^{2/3}]P^N` and `0 ≤ 𝐓_r^{eld} ≤ C(rκ + r²κ^{2/3})`. Corollary EM.1: the intermediate elder mass on `[ℓ^{1/5}, r_0^*]` is `O(ℓ^{2/3}log(1/ℓ))`. Corollary EM's `O(ℓ^{9/14})` is unchanged.
- **LU.**
  - Lemma U₀: for `κ ≤ 1`, `|𝐓_r(k) − 𝐓_r(0) − Λ_κ| ≤ Crk`, with `Λ_κ` the birth-integrated candidate cusp kernel. The law at gap `k` is the law at gap `0` shifted by an odd vector, and a reflection at `k = 0` makes every first-order error odd.
  - Theorem U⁼ is #237's Lemma U for differences on all `k > 0`, with error `C(r²min(1, κ) + r min(k, 1/k))`.
  - Theorem P⁺: `ν_cand = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + O(ℓ^{2/3})`.
  - Corollary LU: `ν_eld` and `ρ_rej` with remainder `O(ℓ^{2/3}log(1/ℓ))`, and SIDE24's relative remainder `O(ℓ log(1/ℓ))`.
- **C3.**
  - Lemma F₃: at every fixed `k > 0`, `(𝐓_r(k) − 𝐒_r(k))/r → 𝐋_F(k)`, the fold-scale layer of the typed boundary, with `𝐋_F(k) = (12/(9k))p_{V_0}(v(k))𝔼_k[P²|3kB_ee − γ_e²/4|³; λ_max(A) = 0⁻]`.
  - Lemma T₁: `κ(𝓐(κ) − 𝐀₂(0)) → a₁ = (1/10)∫F₀db`, with #242's `F₀`.
  - Theorem C3: `ν_cand = cℓ^{−1/3} + B_{d,L} + I^{cand}ℓ^{1/4} + c₂ℓ^{1/3} + c₃ℓ^{2/3} + o(ℓ^{2/3})`, with an explicit integral `c₃`.
  - Proposition G and Corollary G′: for the Gaussian kernel, `c₃ = (J/30)∫∫F₀`, and `J > 0` by a Gamma-function identity, so the model value of `c₃` is positive.
  - Proposition G″: `c₃` is continuous on parity-split jet laws, so `c₃(L) > 0` for `L ≥ L₀(d)`, with `L₀(d)` unquantified.
- **SL.**
  - Lemma SL₀: `κ𝐓_r^{rej}(k, u) → ℱ(k, u) := ∫F(k; b, u)db` at every fixed `k > 0`; this makes note TL's Remark 2 a lemma.
  - Corollary SL₁: `|ℱ(k, u) − ℱ₀(u)| ≤ Ck²` for `k ≤ 1`, the matching of #243's fold-scale limit with #242's cusp-scale limit for the torus field after birth integration.
  - Theorem SL: the separations with `κ ≥ 1` contribute `ℓ^{1/4}∫_0^1∫𝓐^{rej}(s^{−4}, u)dσ ds + R_{2/3}ℓ^{2/3} + o(ℓ^{2/3})` to the rejected density, with `R_{2/3} = ∫∫v⁴(ℱ(v^{−3}, u) − ℱ₀(u))dv dσ`. This identifies the `O(ℓ^{2/3})` of note TL's Corollary TL1, and is the integrated content of #242's input (i) in its `o(ℓ^{2/3})` form.

## What the notes do not establish

From their "not claimed" sections:
- no rate in C3 or SL (their remainders are `o(ℓ^{2/3})`), and no sharpness of LU's `2/3`;
- #242's input (ii) (the separations with `κ ≤ 1`) and its Conjecture 7 stay open; C3's Remark 3 only records that, given Theorem C3, the `o`-form of Conjecture 7 is equivalent to an `ℓ^{2/3}` term `(c₃ − R_{2/3})ℓ^{2/3}` of the near elder density;
- no value of `R_{2/3}` for the torus field, and nothing proved at `L = 24` about the sign of `c₃`;
- nothing pointwise in `b`, no certified number, and no uniformity in `d` or `L`;
- no change to any statement of the consumed notes and packets. Whether IBA2-009 closes is for the audit's owners.

## Not included

- **The consumed sources.** The packets are on `main` at their own paths (`SOURCES.json`, `related_packets`). Note EM's custody packet is Math-#388, note TS's Math-#387 and note TL's Math-#384. `EM1/CLAIM.md` is the same comment as #388's `EM/AUTHOR_READ_COMPLETE_AND_CLAIM.md`: it read-completes note EM and claims EM.1.
- **The exploration scripts.** LU's `toy_diff.py` (in the appendix of its controls comment) and C3's exploration scripts use numpy, scipy or mpmath. They are stored only inside their comment bodies, and are neither extracted nor run.
- **The clean-context referee reports** (same provider and session; not review evidence). They are kept in the project archive.
- **Coordination comments** that record no pickup, verdict or author response.

## Replay

    python3 -B -S frontiers/lifetime_two_thirds_chain_20261007/replay.py
    python3 -B -O -S frontiers/lifetime_two_thirds_chain_20261007/replay.py

`replay.py` uses the standard library only and takes about ten seconds per mode. It is Math-#388's replay (itself Math-#387's, #384's, #360's and the QS `d = 3` packet's hardened replay), with this packet's paths, fingerprints and negative control. It runs four checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, and the tree holds nothing else.
2. **Extraction.** Each `author_controls.py` and `author_controls_stdout.json` equals the fenced payload in its stored controls comment, under the rule that comment states (that of [5971055189](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-5971055189)). Each stdout is a ```` ```json ```` fence.
3. **The checkers.** `em1_exact.py`, `lu_exact.py`, `c3_exact.py` and `sl_exact.py` reproduce their published stdouts byte for byte under the current interpreter's `-O`/`-S` flags, with empty stderr.
   - Each of their 29 mutants and 12 invalid invocations reproduces its exact source-bound rejection: exit code, stdout and stderr fingerprints, with the intended group. An exit code alone does not pass.
   - The fingerprint table in `replay.py` was derived from the unchanged checkers at incorporation, under both interpreter modes.
4. **Negative controls.**
   - A one-byte change to a stored note (`C3/PROOF.md`) is detected.
   - A checker with one changed constant (`c3_exact.py`'s `12/9`, the prefactor of `𝐋_F`, replaced by `12/8`) is rejected, failing exactly at `E5_constant`.

The workflow `.github/workflows/lifetime-two-thirds-chain.yml` runs on Python 3.11.16. It runs the protocol and raw-evidence tests (`tests/test_lifetime_two_thirds_chain_replay_protocol.py`, `tests/test_lifetime_two_thirds_chain_replay_evidence.py`), then the replay in both modes, as two jobs. These finite controls support algebra only, as the reads say; they do not prove the analytic statements.
