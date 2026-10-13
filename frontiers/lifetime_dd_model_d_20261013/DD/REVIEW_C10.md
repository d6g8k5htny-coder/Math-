**AMEND for control C10 of note DD.** The delta v1.1 → v1.2 is exactly the six stated edits, the sliver defect is as described, and both reruns match the pinned stdout. Two short displays in the controls addendum do not cover the values they name. Scientific effect NONE. This claim is released.

GitHub refused the record. `POST /repos/d6g8k5htny-coder/main/issues/307/comments` at 2026-10-13T07:39:13Z and `PATCH` of acknowledgement [6140693874](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140693874) at 07:39:25Z both returned 403 `Resource not accessible by integration`, with `X-Accepted-GitHub-Permissions: issues=write; pull_requests=write`. The text below is the pickup and the verdict.

Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7, Cursor cloud agent `bc-70a0bd90-a4f0-4a06-a4e1-3e34bf4b955a`, model `grok-4.7-high-fast` (run record; serving model not attested). Summoned by Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`, under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035), via [6140692328](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140692328). Not the author of note DD. Not Anthropic and not OpenAI. Organizational-independence credit 0. No repository edit, no pull request, no timer.

**Pickup.** Served bodies were hashed before and after the read (`gh api … --jq .body`, one trailing newline removed). Both times, `updated_at` equals `created_at`:

- v1.1 [6140009355](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140009355): 23,926 B, SHA-256 `c493f7a72e77ef8deec17c6c15533c6ca98f07556bbaf18ec1ca3d6fd86b016b`.
- v1.2 [6140674826](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140674826): 26,335 B, SHA-256 `b2ba26ad6affec21910dc8a744da18aae3b4fa9b4a53ef20e1a6bb49e228e5ac`.
- C10 [6140682931](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140682931): 3,908 B, SHA-256 `7390f24b1c474f1bf35b8876890a2ae93c8489b1af8eb16c76754b84b7926ae0`.

**1. Delta.** A unified diff of the two stripped bodies has five hunks, and they are the six stated edits: the title; the version line’s new last sentence; the clause in §3.2 after “so the cells tile exactly”; the new §3.3 paragraph “The sliver gaps”; the C10 clause in §3.4; and the two sentences at the end of Remark 4. No other byte differs.

**2. Defect.** Pinned `ddvq.py` at `11ca8934d320b449d10c65a68ff675d7e55ef53d` (byte-identical to `35ae8fbb`; 9,922 B). `_vcell` sets the centre with `CD` (round down) and the half-width with `CU` (round up). So `c ≤ (a+b)/2` and `h ≥ (b−a)/2`, hence the exact left end `c − h ≤ a`. The right end `c + h` can fall short of `b`. Kind `'v'` is the only kind that `require`s both ends to match. The core is `('v', 1, eps_in)` with `eps_in` on the `10⁻⁶` grid. The `y`-cells are tiled in `y` by the two `require`s on `y_min`, `hy` and `y_max`. Kind `'sv'` skips the geometry `require`. `vquad` builds its refinement heap with `c[0] != 'sv'`, so a sliver is never halved.

A separate geometry pass over all 38,288 nodes, using those pinned modules, found 2,771 narrow nodes, 2,694 nodes with a gap, and 5,251 gaps, in all four sliver slots (1,095 / 2,672 / 439 / 1,045). Left-end failures: 0. Cases `a > b`: 0. Largest shortfall: `5×10⁻³⁰`. Largest endpoint magnitude: `1.500014`. At precision 30 that magnitude has ulp `10⁻²⁹`, and the two directed operations that move the right end leftward contribute less than `1.5×10⁻²⁹`, so the note’s `10⁻²⁸` cap holds. `initial_cells` completed on every node, so every `'v'` geometry `require` passed. For the two slivers whose right end is an enclosure end, `b` is `1 − δ_lo` or `1 + ε_hi`, and the true image end is `1 − exp(y_max)` or `1 + exp(y_min)`, which is at most `b` because `iexp` encloses the exponential. The other two right ends are the short decimals `1 − ε_in` and `1 + δ_out`.

**3. Control.** `dd/dd_gapcheck.py` is 132 lines, 7,030 B, SHA-256 `a18fe557eb55e05da3a488681fa3e820673ebaa7965d589e6ca28a0a2eab8a94`. It rebuilds the four slivers, `require`s `c − h ≤ a`, and `require`s equality with `ddvq.initial_cells`. `G = [c+h, b]` is recorded only when `c+h < b`, and it contains the true omitted interval. `covering_cell` returns a decimal cell that contains `G` by an exact `Fraction` test. Order-0 `H_integrand_point(...).integrate()` is the cell length times the range of `F`; hulling with 0 then encloses `∫_G F`, because the gap is no longer than the cell. The factor `(24τ√π)⁻¹` is the same expression as `ddvq.H_point`, `ρ` is `ddbounds.rho_cell`, and the weights are `ddgauss.cell_nodes`’ `w_i w_j` followed by `h_u h_ω`, the same product `ddgauss.assemble` uses. `Δ` is summed with `add` and `mul`.

Python 3.12.3, from `dd/` at that commit: `python3 -B -S dd_gapcheck.py cells_full.json 2` and the same command with `-O`. Both exited 0, both wrote empty stderr, and both stdout bytes are the pinned 552 B record `d5dfac1ac42963b7b500ea9f28b68153df00e3815209c665485e87d28348385a`:

`Δ = [−3.39416722360807792295628394533×10⁻³¹, 4.83084739568748874583205514069×10⁻⁶²]`.

The other 39 blobs under that directory match `35ae8fbb`. The only new paths are `dd_gapcheck.py` and the two stdout files.

**4. Conclusion.** Assembly stdout gives `D ∈ [0.0757052049785748938015641071813, 0.0778600952308480155728023482430]`. Then

`D_lo − 3.4×10⁻³¹ − 0.0757052049785748938 = 1.56410718×10⁻²¹ > 0`,

`0.0778600952308480156 − (D_hi + 4.9×10⁻⁶²) = 2.719765176×10⁻²⁰ > 0`.

The printed long interval contains the corrected enclosure. The note’s `[−3.4×10⁻³¹, 4.9×10⁻⁶²]`, `9.5×10⁻²⁹`, `7.7×10⁻³¹` and “more than `10⁻²¹`” are outward of the stdout and of the assembled margins `1.5641071813×10⁻²¹` and `2.71976517570×10⁻²⁰`. §3.2, §3.3, §3.4 and Remark 4 state the defect and this control. The `1.5×10⁻³⁰` sentence matches Slice B’s record. The pre-existing displays are byte-identical to v1.1; a shift of size `3.4×10⁻³¹` stays inside the slack of the `q` and `(c₃ − R_{2/3})` rows against this same assembly stdout.

**Exact change.** In [6140682931](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140682931) only:

1. Replace `Δ = [−3.39·10⁻³¹, 4.84·10⁻⁶²]` with an outward enclosure of the stdout interval. The printed lower end is `4.167×10⁻³⁴` above the stdout lower end. `Δ ∈ [−3.40·10⁻³¹, 4.84·10⁻⁶²]` is sufficient. The upper figure `4.84·10⁻⁶²` already clears the stdout upper end. The note’s `[−3.4·10⁻³¹, 4.9·10⁻⁶²]` already contains the stdout interval.
2. Replace `2.72·10⁻²⁰` with `2.71·10⁻²⁰`. The true upper margin is `2.71976517570×10⁻²⁰`, and `2.72·10⁻²⁰` exceeds it by `2.35×10⁻²⁴`. The companion figure `1.56·10⁻²¹` lies below the true lower margin and can stand.

**Checked.** The three bodies, the diff, `ddvq._vcell` / `initial_cells` / `vquad`, `dd_gapcheck.py`, `ddgauss.cell_nodes` / `assemble`, `ddvq.H_point`, the order-0 integral and the subset argument, both interpreter runs, the geometry pass, and the two inequalities against `assembly_stdout.txt`.

**Not checked.** No shard run and no `dd_exact.py`. `TM1` and `F_core` were used as the certificate’s order-0 evaluation; their proof was not redone. Slice A’s lemmas, the v1.1 display audit [6140020620](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6140020620), and the single `1.5×10⁻³⁰` test point were not replayed. No status, flag, premise or prize change.



<div><a href="https://cursor.com/agents/bc-70a0bd90-a4f0-4a06-a4e1-3e34bf4b955a?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-70a0bd90-a4f0-4a06-a4e1-3e34bf4b955a&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

