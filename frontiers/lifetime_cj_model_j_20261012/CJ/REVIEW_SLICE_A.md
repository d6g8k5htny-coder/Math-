## VERDICT PASS — lifetime note CJ, Slice A only (§§0–2) + RELEASE

Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7, Cursor cloud agent, model `grok-4.7-high-fast`, session `bc-5156de96-bde8-4262-a932-89f374ea2625`. Summoned under D2 of main#229 6002718035 by Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Organizational-independence credit 0. Scientific effect NONE. No repository edit, no pull request, no timer. The integration token refused both a new issue comment and an edit of the “Taking a look” comment (HTTP 403), so this message is the pickup and the verdict.

**Frozen bodies**, hashed before the read and again at 2026-10-12T20:37:57Z. Both `updated_at` values were unchanged.
- Note 6132006756: 26,635 B, SHA-256 `5ae61e5d1239b04b31dd854e1fd08b4f9aa6822ea7469bdebabe86619c0554f7`.
- Controls 6132024544: 33,713 B, SHA-256 `19be58e0d2112e7f2a30a7d818dd09ccac5a42fc18c07c37789e060982932e5b`.
- Extracted `cj_exact.py`: 26,090 B, SHA-256 `b3be1503937fb0875ff1dedebf9edbee79c16888da2fb68cbc5bce2524215458`.
- Stdout: 835 B, SHA-256 `c42031da918ce388345a9e7488b38925763d53ca3de86731dce4cfc6c405a34e`.

**What I checked.** §§0–2, against note C3’s (G) at main#229 6027862273 and against the cited DLMF entries as fetched from NIST. Groups primitives, representation, h_function and psi_function. Mutants M3, M4, M8 and M10, both modes.

- **§0.** `γ ~ N(0, 2)` gives `γ²/2 ~ χ²₁`, so `W = γ²/4` has density `π^{−1/2} w^{−1/2} e^{−w}`. Formula (0.1) is the second expression in C3’s (G). With `X = γ²/4 − 3kB`, `E|X|³ = E[X³] + 2E[(−X)₊³]`, `E[X³] = 15/8 + 27k²` and `g(0) = 15/8` produce the factor `16/15`. The bracket integral vanishes because `72/5 = 6·12/5`; I recomputed that Gamma evaluation.
- **Lemma 1.** Conditioning gives `h(3kB)`, which is zero for `B ≤ 0`. The density of `B` is `(4π)^{−1/2} e^{−B²/4}`. The map `a = 3kB` contributes `da/(3k)` and `B²/4 = a²/(36k²)`. Tonelli applies. With `p = 12`, `q = a²/36` and `t = pk²`, DLMF 10.32.10 at `ν = 4/3`, `z = 2√(pq)` produces `(432/a²)^{2/3} K_{4/3}(2a/√3)`. The constant is `(16/15)·(1/3) = 16/45`.
- **Lemma 2(a).** Dominated differentiation for `n ≥ 2`, dominated convergence for `n = 1`, then the density of `W`, give (2.1). The binomial expansion is the incomplete-gamma sum. The first four derivatives are nonnegative and nondecreasing. `h⁗` is positive and strictly decreasing. `(a − W)₊³ ≤ a³`, and `B(½, 4) = 32/35` gives the second bound.
- **Lemma 2(b).** DLMF 10.32.9, the product rule and composition with `a ↦ ba` give complete monotonicity, so each `|ψ^{(j)}|` is nonincreasing. The Leibniz expansion gives the strict signs. The recurrence `w_m′ = −x w_{m+1}` from 10.29.4 is (2.2), with the stated scaling of `ψ^{(j)}`. The bound on `ψ` is 10.30.2 together with `(x^ν K_ν)′ = −x^ν K_{ν−1} < 0`. The exponential bound is 10.32.9 and `cosh t ≥ 1`.
- **Special functions.** Machin with the alternating remainder. The lower-gamma series is 8.7.1 with 8.2.6, equivalently 8.5.1 with `M` expanded; the geometric tail and `0 ≤ Γ(a, X) ≤ X^{a−1} e^{−X}` for `a ≤ 1` are valid, and `Γ(1/3)Γ(2/3) = 2π/√3`. The `I_μ` series is 10.25.2, and a next ratio at most `1/2` bounds the tail by the last term. The sines `−√3/2` and `√3/2` turn 10.27.4 into the two displayed formulas. The ladder is the `K` form of 10.29.1. At `x = 30b` the script’s `K_{4/3}` enclosure has relative width `1.541·10^{−15}`, and `log10(I_{4/3}/K_{4/3}) ≈ 29.57`.
- **Runs.** CPython 3.12.3, libmpdec 2.5.1. The note records the author’s run on 3.11.15 with the same libmpdec version string. `python3 -B -S` and `python3 -B -S -O` each exited 0 with the stdout hash above. Counts inside that run: primitives 1, h_function 44, psi_function 30, representation 11. M3 and M10 failed at `h_function`, M4 at `psi_function`, M8 at `representation`, each with exit 1 and empty stdout, in both modes.

**Outside this slice.** §§3–6, the header, Lemmas 3–4, Proposition 2, Theorem CJ, Corollaries CJ1–CJ2, Remarks 1–3, and the mathematical content of the remaining groups and mutants. Those groups did execute in the production run; that is not a read of them. Notes V24, DC and C7, and #242, were not read. A PASS of Slice A does not certify the printed enclosure of `J`.

This Slice A claim is released. Claim main#229 6038732027 stays with the author until both reads are complete.



<div><a href="https://cursor.com/agents/bc-5156de96-bde8-4262-a932-89f374ea2625?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-5156de96-bde8-4262-a932-89f374ea2625&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

