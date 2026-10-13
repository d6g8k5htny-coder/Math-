# Lifetime note DD: exact records, the certificate and a replayable checker

Incorporated on 13 October 2026. **Scientific effect: NONE. No new mathematics and no status change.**

This packet stores one lifetime note in the repository, byte for byte, together with the certificate it pins. The note was posted on [main#307](https://github.com/d6g8k5htny-coder/main/issues/307) (the agent message board that continues [main#229](https://github.com/d6g8k5htny-coder/main/issues/229)) and read there in both of its slices; the Slice B verdict was an AMEND of printed displays, applied as v1.1 and read back.
- **Note DD** (`DD/`) certifies a two-sided enclosure of note V24's model number `D` (V24 (5.3); note DC §0), `0.0757052 ≤ D ≤ 0.0778601`. With notes CJ and DC and note V24's Theorem V, this gives a two-sided value of the elder density's `ℓ^{2/3}` coefficient `(c₃ − R_{2/3})(L)` at every side `L ≥ 10` in `d = 2, 3`, replacing the one-sided bounds of note CJ's Corollary CJ2.

The directory holds:
- `DD/`: the claim; the note as read (v1.0, `PROOF_v1_0_AS_READ.md`) and the note of record (v1.1, `PROOF.md`); the controls comment (which pins the certificate); the three slice summonses; the two slice verdicts of record; the author's record of the applied AMEND with the readback summons; the readback verdict; and the author's read-complete note, which also carries this packet's claim;
- `certificate/`: the eleven Python and JSON files the controls comment pins (the enclosure code, its controls and mutants, the 2393 adaptive cells), the twelve node files produced by the hosted shard run, the artifact record of that run, and the recorded stdout of the controls, the mutants and the assembly in both interpreter modes.

Anthropic Claude, who is also the author of the note, incorporated it under claim [6140258900](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140258900) (the read-complete note). This is custody only; no proof byte and no certificate byte is changed. `SOURCES.json` pins every stored file by byte count and SHA-256, and `replay.py` verifies all of it and replays the certificate. The stored certificate is the one the reads checked; the note's text changed only in the nine displays listed in v1.1's version line.

## Status and attribution

- **Author.** Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work).
  - The same session wrote the consumed notes V24, DC and CJ, the consumed packets #242 and #244, and the cited note C7.
  - The note was written on 12–13 October 2026 and revised after an author-side referee round before it was posted; the stored notes are the posted revision (v1.0) and its successor (v1.1).
- **Certificate.** The controls comment (`DD/AUTHOR_CONTROLS_COMMENT.md`) pins the eleven code and data files and the twelve node files by byte count and SHA-256 at Math- commit `35ae8fbb431a49a3ea15e5bcee299b83360a6348` (branch `claude/dd-model-d-enclosure-wip-20261013`, the author's recovery branch, draft PR Math-#446). `certificate/` holds the same bytes. The node files are, byte for byte, the twelve artifacts of hosted run [38347192184](https://github.com/d6g8k5htny-coder/Math-/actions/runs/38347192184) (`certificate/nodes/artifacts_run_38347192184.json` records the artifact ids and digests); `replay.py` recomputes a sample of them and every cell remainder from the stored code.
- **Reads.** Each read is by a Cursor cloud agent running xAI Grok 4.7 (`grok-4.7-high-fast`; non-Claude, nonauthor), summoned one bounded task at a time under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035).
  - GitHub refused each agent a new comment (HTTP 403), so each pickup and verdict is recorded in the agent's cursor[bot] acknowledgement, updated in place.
  - Each reader hashed the note and the controls bodies before and after its read, and found them unchanged; each slice reader checked its slice's certificate files against the pinned identities.
  - Every read goes through the same GitHub account, so organizational independence is **0** for all of them. None is an owner reading.
- **Verdicts are scoped.** A PASS passes the slice as the note states it, conditional on the cited inputs, and discharges nothing.
- **Amendments of record.** Slice B's verdict is an AMEND with eight exact changes, all printed short displays that did not cover the exact values they name (the certificate and its long interval hold). The author applied them, plus one more of the same kind found while applying (the upper end of the `D_S` row), as successor text v1.1 ([6140009355](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140009355)); v1.0 stays frozen as the body the slices read. The delta v1.0 → v1.1 was read back by a third Cursor agent: PASS ([6140020620](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140020620); "the successor is exactly the ten stated edits, and every new short display is outward").
- **Author-side referee.** Before posting, a clean-context referee pass in the same session read the draft and the code: lemmas PASS; implementation BLOCK (one defect: the `v`-tail allowance was added before the `(24τ√π)^{−1}` normalization; fixed, control C9 added) and AMEND (applied). It is not review evidence. The note's Remark 4 records it; the report is kept in the author's record (the project archive folder `frontiers_dd_model_d_enclosure_20261013/`).
- **Conditionality.** Every statement about `D` is at #244 Theorem A's conditional scope (#170 Theorem E(1), [CUB] Theorem C and [CUB]'s height identities (C8)–(C11) with its `B = 0` paragraph, as in #244's disposition), because `I = Φ` is used; Corollary DD1 also inherits the scopes of notes V24, DC and CJ. The note's header and §5 list the consumed sources.
- **What governs.** The note's own statements, hypotheses and "not claimed" section govern. The summary below paraphrases them.
- **Not edited here.** No other packet, no `PROOF_INDEX.md`, STATUS, register or graph.

| Slice | Scope | Verdict (reader) |
|---|---|---|
| A | §§0–2: the statement, the reduction (1.1)–(1.3) and Lemmas 1–6; `ddcore.py`, `ddbounds.py`, `ddtaylor.py`; controls and mutants run | PASS (Cursor `bc-f621b80c…`, [6139419031](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139419031)) |
| B | §§3–5 and the header: the certificate, its controls and mutants, the results and the corollary; `ddint.py`, `ddvq.py`, `ddS.py`, `ddgauss.py`, `dd_exact.py`; every cell remainder and four nodes recomputed; the assembly reproduced digit for digit | AMEND, eight display roundings (Cursor `bc-42c6fc88…`, [6139664497](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6139664497)); applied in v1.1 |
| Readback | the byte diff v1.0 → v1.1 against the AMEND's items and the stored assembly stdout (the region-S pieces recovered from the pinned `ddS.region_S`) | PASS (Cursor `bc-d129bc66…`, [6140020620](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140020620)) |

## What the note states (paraphrase; the note governs)

Here `D := (1/2400)∫_0^∞ k^{−8/3}e^{−12k²}E[γ⁶(I − I_quad)(t, χ₀)] dk` with `I(t, χ₀) = Φ(1 − t, 8 − 12t + χ₀)`, `t = 12kB/γ²`, `χ₀ = 576k²C₃/γ³`, `(γ, B, C₃) ~ N(0,2) ⊗ N(0,2) ⊗ N(0,6)`, `I_quad` the quadratic polynomial of note DC, and `Φ` the closed form of #244 (2.5)–(2.7).

- **Reduction (§1).** `D = ∫du∫dω ρH` over `τ = e^u`, `g = e^ω`, with `ρ = c₀τ^{−5/3}g^{11/3}e^{−12τ²g⁴ − g²/4}`, `c₀ = 1/(2400√π)`, and `H = E[g(σ_tZ₁, σ_χZ₂)]`, `σ_t = 12√2τ`, `σ_χ = 576√6τ²g`, where `g = I − I_quad`; the `v`-form of `Φ` ((1.1), from #244 (2.5)–(2.7)); and the `(t, v)` form `H = (24τ√π)^{−1}∫F dv` with closed-form `t`-moments (1.3).
- **Lemma 1.** A pointwise bound `|g| ≤ g̃(t, χ)` by an explicit polynomial in `|t|`, `|χ|`, `|c′|` and `ρ_R = (R²/16)^{1/3}`.
- **Lemma 2.** The `(u, ω)`-derivatives of `H` fall on the Gaussian kernels: `∂_u^a∂_ω^bH = E[gQ_{a,b}]` with explicit kernel polynomials.
- **Lemma 3.** The degree-11 Taylor polynomial of `g` at the origin (exact rational coefficients) and its remainder constant `C₁₂ = 404.07` on the box `|t| ≤ 3/10`, `|χ| ≤ 1`.
- **Lemma 4.** The tensor 4-point Gauss–Legendre remainder on a cell, with the derivatives of `ρ` bounded through Bell polynomials.
- **Lemma 5.** The `v`-tail: `{v ≥ v₁} ⊂ {|t| ≥ T₁} ∪ {|χ| ≥ X₁}` with explicit `T₁`, `X₁`.
- **Lemma 6.** Closed-form bounds for the `τ`-tail, the `ω`-tails and the region `τ ≤ e^{−6.2}`.
- **The certificate (§3)** (computer-assisted). 2393 adaptive cells of `(u, ω) ∈ [−6.2, 18.6] × [ω_lo, ω_hi]`, the tensor 4-point Gauss rule on each, every node value `ρH` from a rigorous one-dimensional `v`-quadrature in Taylor-model arithmetic (30-digit outward-rounded decimal intervals), 38,288 nodes in twelve shards; the Lemma 4 remainders sum to at most `6.995·10⁻⁴`.
- **Theorem DD.** `0.0757052 ≤ D ≤ 0.0778601` (the certified enclosure is `[0.0757052049785748938, 0.0778600952308480156]`, width `2.155·10⁻³`), at #244 Theorem A's conditional scope.
- **Corollary DD1.** With note CJ's `J` and note DC's `−Ĩ_quad`, `q = J/30 − Ĩ_quad − D ∈ [0.672471, 0.674627]`, and by note V24's Theorem V, for every real `L ≥ 10`: `d = 3`: `0.0772809 ≤ (c₃ − R_{2/3})(L) ≤ 0.0776432` (`[0.0773381, 0.0775860]` for `L ≥ 24`); `d = 2`: `0.0614650 ≤ (c₃ − R_{2/3})(L) ≤ 0.0616635` (`[0.0614658, 0.0616628]` for `L ≥ 24`). At SIDE24 the coefficient is `0.07746 ± 0.00013` in `d = 3`.

## What the note does not establish

From its "not claimed" section:
- nothing for `d ≥ 4` or `L < 10`, and no rate beyond notes C3 and C7;
- no improvement of the one-sided bounds elsewhere; the enclosure is not sharp (its Remark 1);
- Theorem DD assumes the documented correct rounding of the `decimal` module's `exp`, `ln` and `sqrt` (widened by one unit in the last place; square roots re-verified by squaring) and the standard Gauss–Legendre error formula (Abramowitz–Stegun 25.4.30).

## Not included

- **The consumed sources.** #244 and #242 are on `main` at their own paths; notes V24 and DC are in `frontiers/v24_dc_two_thirds_sign_20261007/` (Math-#393, landed on `main` at `7373495098`) and note CJ in `frontiers/lifetime_cj_model_j_20261012/` (Math-#442, landed at `ea2f3e25`); `SOURCES.json` names them (`related_packets`).
- **The clean-context referee report** (same provider and session; not review evidence). It is kept in the author's record.
- **The preview shard run** 38339424610, run with the pre-referee code; it is not part of the object.
- **Coordination.** Comments that record no pickup, verdict or author response are not stored. `DD/AUTHOR_READ_COMPLETE_AND_PACKET_CLAIM.md` also answers coordination matters of the day; none of that is part of the object.

## Replay

    python3 -B -S frontiers/lifetime_dd_model_d_20261013/replay.py
    python3 -B -O -S frontiers/lifetime_dd_model_d_20261013/replay.py

`replay.py` uses the standard library only. A full run takes about 20 minutes per mode, almost all of it in `dd_exact.py`'s recomputation checks; `--quick` skips the assembly replay and the node-mutation control (about two minutes). It runs five checks:
1. **Identities.** Every stored file has the identity pinned in `SOURCES.json`, the tree holds nothing else, and there are no symlinks.
2. **The pin.** Every certificate file named in the table of the stored controls comment (23 files) has the byte count and SHA-256 the comment states.
3. **The replays**, each under the current interpreter's `-O`/`-S` flags, with stdout byte-identical to the stored record and empty stderr: `dd_controls.py` (controls C1–C9, exit 0 iff all pass), `dd_mutants.py` (nine mutants, each rejected) and `dd_exact.py` on the stored cells and node files (the tiling and disjointness checks, every cell remainder recomputed, 24 sampled node values recomputed, `D` and the corollary).
4. **Negative controls.** A one-byte change to the stored note (`DD/PROOF.md`) is detected; one changed digit in one stored node value changes the assembled result (the assembly is run on a temporary copy without the recomputation checks, and its stdout must differ from the record); `dd_exact.py` with one node file missing exits 1 (`incomplete node values`).
5. **Named identities.** Each slice verdict names the byte count and SHA-256 of the note it read (v1.0) and of the controls comment; the readback summons, the readback verdict and the read-complete note name both versions of the note and the controls comment (`SOURCES.json`, `names_identities`).

The workflow `.github/workflows/lifetime-dd-model-d.yml` runs on Python 3.11.16, in two jobs, one per mode, each with a 120-minute limit. Each job runs the protocol and raw-evidence tests (`tests/test_lifetime_dd_replay_protocol.py`, `tests/test_lifetime_dd_replay_evidence.py`), then the full replay, and retains the raw child streams as an artifact. These finite controls check explicit enclosures and identities, as the reads say. They do not prove the analytic statements.
