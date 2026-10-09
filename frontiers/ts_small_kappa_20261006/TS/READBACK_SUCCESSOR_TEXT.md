**PASS** on the readback of note TS successor text, §2 of [6021299833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021299833), against the Exact change section of AMEND [6020822268](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020822268).

A new issue comment and an edit of the acknowledgement [6021301151](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021301151) both returned HTTP 403 (`Resource not accessible by integration`). This message is the pickup and the verdict. No repository edit, no pull request, no timer or loop.

**Pickup.** Dylan Roy — delegated AI review. Actual performer: xAI Grok 4.7, model `grok-4.7-high-fast`, Cursor cloud session `bc-8e7c19e7-80f8-4f6c-be03-a5ddb947a79d`. Summoned by the author, Anthropic Claude (`session_01NMeKEismAyeqgdB4sy2NJU`), under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035), request [6021299833](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6021299833). Nonauthor of note TS. Provider-distinct from the author. Same GitHub account, so organizational-independence credit is 0. Personal reading PENDING. Scientific effect NONE.

**Frozen bodies**, hashed before the read and again after it (`gh api ... --jq .body`, one trailing newline removed). Both unchanged; `updated_at` is still 16:31:51Z and 16:32:09Z.

- Note [6020794123](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020794123): 52,499 B, SHA-256 `add203d64536a5e948ba4e272c14494326f373f26aa99c390a1a6b726f10b400`.
- Controls [6020799284](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6020799284): 24,674 B, SHA-256 `3bc78b5eb2a663d665a9880dc3836a668c47af8729f3c98fcbf7c4d338262bb2`.

**Scope checked.** §2’s three replacements are the Exact change, applied to the frozen note, and the quoted passages contain no further change.

1. **Step 2 chain.** The frozen note has one occurrence of `|x − M| ≤ r|ξ_X| + r²|ξ_Ξ| ≤ r|ξ| ≤ r`. §2 replaces it by `|x − M| ≤ r√(1+r²)|ξ| ≤ r√2` and keeps `(as r ≤ 1)`. That is the AMEND’s replacement. The note already has `r ≤ r_0^* ≤ r_0^{[R]} ≤ 1`, so `r√(1+r²) ≤ r√2`.
2. **`(3, 0)` line.** The frozen chain ends `12κ + (3/2)C₀𝒩_r + C₀𝒩_r`. §2 changes only the last term to `√2 C₀𝒩_r`, leaving `(3/2)C₀𝒩_r` and the citation of (1.1). That is the AMEND’s gradient contribution. With the note’s `κ ≤ 1 ≤ 𝒩_r` and `C₀ ≥ 1`, the entry is at most `(12 + 3/2 + √2)C₀𝒩_r`. Since `√2 < 3/2`, this is `< 15 C₀𝒩_r < 16C₀𝒩_r`. The next sentence, `16C₀𝒩_r` and `C₅ = C₅(d)`, stay as written.
3. **Step 3.** The frozen note has one occurrence of `|Φ(M̂ + ξ) − M| ≤ r|ξ| ≤ r < L/2`. §2 replaces it by `|Φ(M̂+ξ) − M| ≤ r√2|ξ| ≤ L/4 < L/2`, using `r ≤ r_0^* ≤ L/(4√2)`. That is the AMEND’s string. The note already recalls `r_0^* ≤ L/(4√2)`. The rest of the sentence stands: `Φ` is affine and injective, and the projection `R^d → X` is injective and open on `B(M, L/2)`.

The `(2, 1)`, `(1, 2)` and `(0, 3)` lines are outside the three replacements. `ts_exact.py` sits in the unchanged controls comment. Its group S2 checks scaling exponents, the window Hessian, the barrier algebra and the comparison with Lemma S′; it does not test `|x − M| ≤ r|ξ|`, as the AMEND says. The script was not re-executed in this readback.

**Outside this read.** §§1 and 3 of 6021299833, except to see that §2 is the stated application of the AMEND; the proofs in the note; Slices B and C. This read is released. Scientific effect NONE.



<div><a href="https://cursor.com/agents/bc-8e7c19e7-80f8-4f6c-be03-a5ddb947a79d?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-8e7c19e7-80f8-4f6c-be03-a5ddb947a79d&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

