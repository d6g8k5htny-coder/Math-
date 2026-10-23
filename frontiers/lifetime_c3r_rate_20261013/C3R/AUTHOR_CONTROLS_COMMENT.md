**Controls of note C3-R v1.0** ([6145991558](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6145991558); served body 28,268 B, SHA-256 `5d465e1be578de19f18439116299771c8aa64f5bc4030eba5187a2a3002f2c2e`), under claim [6145251763](https://github.com/d6g8k5htny-coder/main/issues/307#issuecomment-6145251763).

Dylan Roy — delegated AI work. Actual performer: Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU` (serving model changed to Claude Opus 5.5 at about 12:30Z at the owner's instruction; session, claim and custody unchanged). Scientific effect NONE. (A first attempt at this comment, 6146000791, was posted with its shell-quoted fields empty and deleted within a minute; this is the comment of record.)

**Pinned bytes** — Math- commit `9232eff05a5753f41c9ea5528f797b7bf1df1967`, branch `claude/dd-model-d-enclosure-wip-20261013`, directory `frontiers/dd_model_d_enclosure_20261013/wip_20261013T0245Z/c3r/`:

| File | Bytes | SHA-256 | Git blob |
|---|---:|---|---|
| `c3r_exact.py` | 11,625 | `6d911f0a6c1b0cda5ddd579b26aeaab2c3cc557f6b95c0970a944de25380a335` | `10e3512354a29580b39a4e650edb863be61ae6f9` |
| `c3r_mutants.py` | 2,027 | `6afab0e79659ff0e5064a7ca4144aef485150b521c55e611e651b1d687c6c8f3` | `d826fe8709884c2c8704d5e8e7dcc4d5be62ba2a` |
| `c3r_stdout.txt` | 2,152 | `684d06a01eefb160188e7769099cd42e8c7ccf5b3803edd3010a646e4513791d` | `9a6e593e0ef654e911f2107c33553583b9c08d2b` |
| `c3r_mutants_stdout.txt` | 421 | `25a233227ef286319aa312fd07e4cd508176ca2eb656dcf4d3f4fdfffca6c215` | `89040c56d9d2828f09d1be5b6b579ee223d6d2f6` |

The same directory holds the draft as posted (`NOTE_C3R_draft.md`, the posted bytes without the served footer) and the plan `C3R_PLAN_20261013.md`.

**Replay** (Python standard library, exact rationals; about a second each):
- `python3 -B -S c3r_exact.py` and `python3 -B -O -S c3r_exact.py`: exit 0, stdout byte-identical to each other and to `c3r_stdout.txt`.
- `python3 -B -S c3r_mutants.py` (and with `-O`): exit 0, every mutant rejected; stdout = `c3r_mutants_stdout.txt`.

What the controls check (note §6): **E1** the exponents of (4.1) and (1.3) at every stated `δ(d)`, `d = 2, …, 6`, the caps `σ ≤ v(α)`, `σ ≤ 1/12`, the closed-form optimum for `m = 2` (`α* = 23/60`, `σ* = 23/1149`), and the grid optima for `d = 3, …, 6` as lower bounds; **E2** `0 < v(α) < 1/12` on `0 < α < α_max` (exact endpoints, monotonicity, the form `n/(3(n + 3))`); **E3** the six exponents re-derived from the substitution `r = ℓ^{1/3}s`, `k = s^{−3}`, `κ = ℓ^{−1/3}s^{−4}` term by term (with `a_eff = min(α, 2α/(m − 1))` derived independently) agree with the table at 56 points. They check arithmetic only: which error terms appear in (4.1), and the analytic lemmas, are the reads' business.

`c3r_exact.py` stdout:
```
d = 2 (m = 1): delta = 1/30 (sigma = 1/30; validity cap v_1 = 31/381)
d = 3 (m = 2): delta >= 437/22047 = 0.01982 at a = 437/1152 (0.3793), a' = 15/32 (0.4688), sigma = 437/22047 (0.01982); a_max = 23/48, a'_max = 1/2, v(a) = 115/5529 (0.02080), theta = 1/48
d = 4 (m = 3): delta >= 1159/58773 = 0.01972 at a = 1159/3072 (0.3773), a' = 15/32 (0.4688), sigma = 1159/58773 (0.01972); a_max = 61/128, a'_max = 1/2, v(a) = 305/14739 (0.02069), theta = 1/64
d = 5 (m = 4): delta >= 779/54177 = 0.01438 at a = 779/1920 (0.4057), a' = 91/288 (0.3160), sigma = 779/54177 (0.01438); a_max = 19/40, a'_max = 1/3, v(a) = 133/9039 (0.01471), theta = 1/80
d = 6 (m = 5): delta >= 7735/686757 = 0.01126 at a = 7735/18432 (0.4197), a' = 91/384 (0.2370), sigma = 7735/686757 (0.01126); a_max = 91/192, a'_max = 1/4, v(a) = 1001/85947 (0.01165), theta = 1/96
d = 3 closed form: a* = 23/60, sigma* = 23/1149 = 0.02002 >= 1/50: True (grid optimum 437/22047 is a lower bound)
d = 3 stated delta = 1/50 admissible at (a, a', sigma) = (23/60, 499/1000, 1/50): terms of (4.1) = [1/50, 181/9000, 1981/75000, 41/150, 23/150, 44/75]
d = 4 stated delta = 1/51 admissible at (a, a', sigma) = (3/8, 499/1000, 1/51): terms of (4.1) = [1/51, 1/51, 1487/51000, 14/51, 8/51, 10/17]
d = 5 stated delta = 1/70 admissible at (a, a', sigma) = (779/1920, 91/288, 779/54177): terms of (4.1) = [779/54177, 779/54177, 79351/5200992, 15722/54177, 11048/54177, 33002/54177]
d = 6 stated delta = 1/89 admissible at (a, a', sigma) = (7735/18432, 91/384, 7735/686757): terms of (4.1) = [7735/686757, 7735/686757, 1054963/87904896, 205714/686757, 159304/686757, 426898/686757]
E2 m = 2: 0 < v(a) <= v(0) = 23/285 < 1/12 < 1/3 on 0 < a < a_max = 23/48, v(a_max) = 0
E2 m = 3: 0 < v(a) <= v(0) = 61/759 < 1/12 < 1/3 on 0 < a < a_max = 61/128, v(a_max) = 0
E2 m = 4: 0 < v(a) <= v(0) = 19/237 < 1/12 < 1/3 on 0 < a < a_max = 19/40, v(a_max) = 0
E2 m = 5: 0 < v(a) <= v(0) = 91/1137 < 1/12 < 1/3 on 0 < a < a_max = 91/192, v(a_max) = 0
E2 m = 1: v_1 = 31/381
E3: the exponents of (4.1) derived from r = l^{1/3} s, k = s^{-3}, kappa = l^{-1/3} s^{-4} agree with the table at 56 points
controls: ALL PASS
```

`c3r_mutants.py` stdout:
```
M1 T1-R term 4a' -> 2a': REJECTED (exit 1) AssertionError: E3 m = 2: derived exponents = table
M2 v(a) without m theta: REJECTED (exit 1) AssertionError: m = 2: the crossing a/(3(a+6)) = v(a) is at a* = (6 - 12 theta)/15
M3 m = 1 rate 1/30 -> 1/29: REJECTED (exit 1) AssertionError: d = 2: delta = 1/30
M4 a_eff = a for every m: REJECTED (exit 1) AssertionError: E3 m = 4: derived exponents = table
mutants: ALL REJECTED
```

**Author-side referee round (not review evidence).** Two clean-context same-session Anthropic subagents read §§0–2 and §§3–6 against C3 and LU before posting; both AMEND, no blocking finding; all changes applied before posting and listed in the note's Remark 5. No stated `δ(d)` changed.

Two bounded reads (Slice A: §§0–2; Slice B: §§3–6 and these controls) are summoned next.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
_Generated by [Claude Code](https://claude.ai/code)_