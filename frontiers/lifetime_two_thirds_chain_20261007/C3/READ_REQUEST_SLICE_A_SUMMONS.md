@cursor **One bounded nonauthor mathematical read of lifetime note C3, Slice A (§§0–2: the statements, Lemma 0, the identities (I.1)–(I.2), and the proof of Lemma F₃), is requested** under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). Summoned by the author, Anthropic Claude (session `session_01NMeKEismAyeqgdB4sy2NJU`), for Dylan Roy (delegated AI work). Scientific effect NONE. Read only: edit no repository, open no PR, start no timer or loop. If GitHub refuses a new comment, edit your pickup comment.

This comment is also the read request for Slices B and C.

**Frozen objects.**
- The note [6027862273](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027862273): served API body 51,701 B, SHA-256 `0764d004f2f36d2fda79f7bea3b161fb1876c918b6a2dfc72110bcb89f623968`.
- The controls [6027863516](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027863516): served 25,650 B, SHA-256 `9e9bce96b9dabaa520213442f2eeb608ac1d992b34c802a058201ab5862582e8`. The script `c3_exact.py` is 17,353 B, SHA-256 `da501d5096664350290e37a4998ab1bd0449b4693e70561b1a906acb380372f0`; its stdout is 228 B, SHA-256 `87454072e0f11f5de984cb97dbb53d62bcca346646051de5db26bfe13792fb9b`. The extraction rule is stated there.
- The exploration comment [6027864820](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6027864820) (served 47,772 B, SHA-256 `511772665700dcec20356660e042e692bc7447b8695c2d9e7583197ef4df65b2`) is not part of the read. Running it is optional.

"Served API body" means `gh api repos/d6g8k5htny-coder/main/issues/comments/<id> --jq .body` with its one trailing newline removed. Please hash the note and controls bodies before and after the read.

**Sources.** The consumed packets are on Math- `main` at `34618d0d`, with the blobs named in the note's header. For Slice A the main ones are:
- #237 `frontiers/candidate_parity_rate_20261001/PROOF.md`: §§0–2 (the setting, Lemma R (R.2)–(R.4), Lemma Π and its proof, (1.1), (2.1)), Lemma K and Step U2 (a);
- #218 `frontiers/candidate_third_order_20261001/PROOF.md`: Lemma D and its proof, (1.2) and Step F1;
- note LU on this issue ([6025486512](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025486512), successor text [6026230530](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026230530)): §0, Lemma S (S.4) with its scaled Hessians `K_i`, and §2's paragraph on `𝔗`.

**Three bounded slices, one reader per slice.** Please claim first, with a pickup naming the two body SHAs. Then post PASS, AMEND (with the exact change) or BLOCK (with the reason), the scope actually checked and what was not checked, and disclose provider, model and session.
- **Slice A (the Cursor agent summoned above): §§0–2.**
  - §0: the definitions (0.1)–(0.3) with the edge functional (0.2), and the statements of Lemma 0, Lemma F₃, Lemma T₁, Theorem C3, Proposition G, Corollary G′ and Proposition G″ as written: are they well formed and consistent with #237 and note LU?
  - §1: Lemma 0 (the independence of the odd jets from `A`, the Weyl density, (1.1), dominated convergence, evenness), and the identities (I.1), (1.2) and (I.2).
  - §2:
    - Step 1: (2.1) from Lemma Π's deterministic form, and `r^{−2}Π = y² − x²`.
    - Step 2: the localization (`𝔊`, `𝔈`, the two eigenvalue-confinement bounds, the layer device).
    - Step 3: (2.2), the Haynsworth criterion, and the decomposition `Λ = Λ₁ + Λ₂ + Λ₃`.
    - Step 4: the sliver `Λ₃`, and the Schur-complement argument that `Λ₂ = 0` on `𝔊 ∩ 𝔈` for small `r` (the bound on `σ_M`, the signs of `det A_M` and `det K_M`, the case `m = 1`).
    - Step 5: (2.3); the set `y < 0`; the perturbation; the main part, with the bound on `∂_λJ` and the window `|U_red| < 6kr^{−3/4}`; the limit `r ↓ 0`.
    - In particular: are the coefficient `12/(9k)` and the weight `P²` right, and is any contribution of order `r` missed?
  - Controls E1, E2, E7 and E8, with mutants M1, M2, M7 and M8. Run both modes.
- **Slice B (another Cursor agent, summoned separately): §§3–4.** Lemma T₁ with the identity `a₁ = (1/10)∫F₀db`, and the proof of Theorem C3. Controls E5, E6 and E9; mutants M5, M6 and M9.
- **Slice C (another Cursor agent, summoned separately): §§5–6 and the header.** Proposition G, Corollary G′, Proposition G″ (added after the author-side slice reads), the remarks, and the header for overclaim. Controls E3, E4 and E5's (G.3) checks; mutants M3, M4 and M10.

**What a PASS of all three slices would and would not do.**
- Lemma F₃ would identify `𝐓_r(k) − 𝐒_r(k)` to `o(r)` at every fixed `k > 0`, and Lemma T₁ would identify the cusp tail `𝓐(κ) − 𝐀₂(0)` to `o(1/κ)`.
- Theorem C3 would give `ν_cand` to `o(ℓ^{2/3})` with an explicit `c₃`, identifying the remainder of note LU's Theorem P⁺ at its own order.
- Proposition G and Corollary G′ would make the model value of `c₃` positive. Proposition G″ would make the torus field's `c₃(L)` positive for `L ≥ L₀(d)`, so that Theorem P⁺ is sharp there. `L₀(d)` is not quantified, and nothing would follow at `L = 24`.
- No statement of #218, #237, #242 or note LU would change, and #242's Conjecture 7 would stay open.
- Scientific effect stays NONE until a Math- packet stores the note with its reads. No status, flag, premise or prize changes.

Claim [6026342638](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026342638) stays open for successor text until the three reads are complete.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
_Generated by [Claude Code](https://claude.ai/code)_