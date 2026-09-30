# Nonauthor review — RN count interface note (D4 premise)

**Object reviewed:** `frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md` (RN-COUNT-INTERFACE-20260924-v1), author
OpenAI / ChatGPT; on Math- `main` `aa288385af9392c509233c25a0f4012c9ba023e5`; 8938 bytes, SHA256
`aa993f5217bd70e6d1060402d121ab659f6582a098e29042c67585a345a8e3ab`, git blob `371fd6d17920f2eb3b1c5ec30297acf6daf1d385`; unchanged since its landing commit `8a13ee9`
(24 September 2026). Live graph node `math.rn-count-interface` carries this SHA256 as fingerprint.
**Revision:** v1.3 (30 September 2026) corrects the evidence labels after OpenAI review 5360320845 item 2: the checks
that use floating point are now called numerical corroborations, the rational ones exact; and names the note's consumed
premises (item 3 there; OpenAI 5360327058 item 2). Verdicts unchanged.
**Reviewer:** Anthropic Claude, Claude Code session `session_017Mi3hxjaxV45x6zo6o1ee3`. Different provider from the
author. Same GitHub account as every lane; no organizational independence is claimed.
**Exposure:** I authored none of the three-fronts notes. I authored the remote-collision packet and the C6L packet,
both downstream of the fixed-remote theorem that consumes this note; neither is an input here.
**Scope:** the logical interface only, as the note itself states: the implications (N1)–(N3), the counterexamples of
§3 with (N4)–(N5), the marked Kac–Rice expression (N6)–(N7) as a formula, and the support statement of §5. No rate,
no RN numerical certificate and no evaluation of the Gaussian triple integral are claimed by the note or accepted
here. Scientific effect: NONE.
**Promoted scope (v1.3):** (N1)–(N5) and the §3 counterexamples as self-contained probability statements; (N6)–(N7)
and §5 as formula-level implications conditional on the note's two consumed premises, the parent's regression law `Q`
with its §9 Borel-mark convention (live node `math.uniform-matrix-cap-lifetime`, read with its four reading-rule
components) and the cap support source of §5 (live node `math.d1-component.marked-cylinder-cap`, SHA256 `0bf922b9…`, the
digest the note quotes); both are required edges in `PROPOSED_TRANSITIONS.json`. Nothing quantitative.

## Verdicts

| Item | Statement | Verdict |
|---|---|---|
| (N1) | `E[N 1_E] ≤ (E N^p)^(1/p) P(E)^(1−1/p)` for `p > 1` | **ACCEPT**: Hölder with exponents `p` and `p/(p−1)` applied to `N · 1_E`. Exact rational check for `p = 2` (Cauchy–Schwarz form `(E[N1_E])² ≤ E[N²] P(E)`) and `p = 3` (`(E[N1_E])³ ≤ E[N³] P(E)²`) on finite distributions in `alignment_check.py` (`INTERFACE`). |
| (N2) | `E N^p ≤ A r^(−β)` gives `E[N 1_E] ≤ A^(1/p) C^(1−1/p) r^([3(p−1)−β]/p)` | **ACCEPT**: substitution into (N1); the exponent `3 − 3/p − β/p` is the moment convention, as the note says. |
| (N3) | `E[N 1_E] = q E[N | E]`, `q = P(E) > 0` | **ACCEPT**: definition of conditional expectation; the two remarks (sufficiency of a bounded conditional mean; equivalence only under a lower comparison `q ≥ c r³`) follow. |
| §3 (N4) | `U` uniform, `E_r = {U ≤ r³}`, `N_r = ⌈log(1/r)⌉ 1_{E_r}`: `E N_r / r³ → ∞` while `sup_r E N_r^p < ∞` for every fixed `p` | **ACCEPT**: `P(E_r) = r³`; `E N_r^p = ⌈t⌉^p e^(−3t) ≤ (t+1)^p e^(−3t)` with `t = log(1/r) ≥ 1`, whose supremum over `t ≥ 1` is finite (the logarithmic derivative `−3 + p/(t+1)` is eventually negative). The argument is the log-derivative; `INTERFACE` corroborates it numerically, in floating point, on `r = e^(−t)`, `t = 1, …, 12`, and on a grid against the located maximum (labelled `numerical_corroboration`, not exact). |
| §3 sharp `p` | `N_r = ⌈r^(−3/p)⌉ 1_{E_r}`: `E N_r^p ≤ 2^p` for `r ≤ 1`, `E N_r ≍ r^(3−3/p)` | **ACCEPT**: `r^(−3/p) ≥ 1` gives `⌈r^(−3/p)⌉ ≤ 2 r^(−3/p)`. Checked exactly at `r = 2^(−pm)`, where `r^(−3/p) = 2^(3m)` is an integer, `E N_r^p = 1` and `E N_r = r^(3−3/p)` exactly. |
| (N5) | `P(N > t) ≤ A e^(−t/B)`, `A ≥ 1`, gives `E[N 1_E] ≤ ∫ min(q, A e^(−t/B)) dt = B q [1 + log(A/q)]` | **ACCEPT**: layer cake `E[N 1_E] = ∫_0^∞ P(N > t, E) dt ≤ ∫ min(q, P(N > t)) dt`; the crossover is `t_0 = B log(A/q)` and the two pieces are `q t_0` and `A B e^(−t_0/B) = B q`. The (N4) example has the uniform tail `P(N_r > t) ≤ e³ e^(−3t)` (`A = e³`, `B = 1/3`), so the logarithmic loss in (N5) is not removable from a tail hypothesis alone, as the note says. The identity is proved by the antiderivative; `INTERFACE` corroborates it by floating-point Simpson quadrature at three parameter points and checks the tail comparison on a floating-point grid (numerical corroboration, not exact). |
| §4 (N6) | marked Kac–Rice for `E_Q^W N_B` with the endpoint weight as a field mark and the event indicator inside the conditional expectation | **ACCEPT as a formula at the note's stated level of rigour** (bounded continuous cylinder marks, extension of finite measures, truncation of `W_r`, monotone convergence; compact `B` off the pins, exhaustion), conditional on the note's consumed premise: the parent's regression law `Q` and its §9 Borel-mark convention (live node `math.uniform-matrix-cap-lifetime`, read with its four reading-rule components; a required edge in the proposal). Its fixed-remote instance is the reviewed formula (12)–(14) of the D4 proof, accepted in main#76 comment 5841783172 items 2–3. A later rigorous statement of the same identity with the kernel convention fixed is Lemma 5.1 of `frontiers/c6_palm_route_20260929/PROOF.md` (Math-#145); it is cited for the reader and is not consumed here. Nothing quantitative is asserted by (N6) and nothing quantitative is accepted here. |
| §4 (N7) | an `A r⁵` enclosure of the numerator with `Z_r ≥ z_* r²` gives `E_Q^W N_B ≤ (A/z_*) r³` | **ACCEPT**: division; the note correctly separates this from the cap probability argument (`E_Q[W_r 1_{G^c}]`). |
| §5 | support on the rare event only inside the deterministic cap cylinder; remote regions need their own support statement or the count `N 1_{G^c}` | **ACCEPT as a scope statement**; it consumes the cap source `0bf922b9…` for the containment `{M, S}` on `G_r` (the live node `math.d1-component.marked-cylinder-cap` carries exactly that SHA256; a required edge in the proposal) and adds nothing to it. |
| §6 | completion test: (N7) or a uniform conditional mean with the support relation; finite moments give (N2), tails give (N5) | **ACCEPT** as the logical summary of the above. |

**Overall: ACCEPT at the logical-interface scope.** The note proves exactly what it claims and no more: correct
inequalities and counterexamples, and the form of the full-pin Kac–Rice expression that the fixed-remote theorem later
evaluated. It is not an expected-count rate and is not treated as one. Evidence labels: the (N1)–(N3) and sharp-`p`
checks in `INTERFACE` are exact rational arithmetic; the (N4) grid, the (N5) quadrature and the tail grid are floating-point
numerical corroborations of arguments proved above, not exact checks.

## Relation to its consumers
- `math.rn-fixed-remote-window` (D4) reads the interface as the formulation it completes: PROOF §1 "identified a
  three-determinant integral whose unnormalized numerator must be O(r^5), but did not bound it. This note supplies
  that bound"; §7 "Equation (14) now supplies it for every fixed remote region and the entire BETWEEN-PIN HEIGHT WINDOW".
  The D4 review reconstructed the three determinant factors, the `O(k r⁵)` numerator and the original normalizer
  (items 2–3), i.e. the consumed content of (N6)–(N7).
- `math.rn-fixed-annulus-window` (D5 fixed annulus) uses the same normalized three-determinant intensity with the
  original normalizer (its (A8) and §5 ledger), reviewed in `reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md`.

## Not established here
No rate, no RN or 24-jet certificate, no `ENV-RESCOV` or historical carrier, no register transition. This file is a
review record; the proposal that consumes it is `RECONCILIATION.md` in this directory.
