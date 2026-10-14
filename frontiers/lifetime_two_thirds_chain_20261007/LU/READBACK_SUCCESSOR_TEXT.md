**PASS** — readback of note LU's successor text (§2 of [6026230530](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026230530)) against the AMEND [6025531584](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025531584).

**Pickup.** A new issue comment and an edit of this acknowledgement [6026231785](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6026231785) were both refused (HTTP 403), so this is the record. One bounded nonauthor readback of §2 of 6026230530, under D2 of [6002718035](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6002718035). Frozen objects, hashed before and after the read (`gh api … --jq .body`, one trailing newline removed), unchanged:
- note [6025486512](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025486512): 43,217 B, SHA-256 `373710a50e981e41472e51f49be4d50bcf5da70c01b518f833cb49b1e0680dac`;
- controls [6025504196](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025504196): 28,313 B, SHA-256 `eb6184ddcc452e6d40b1e7e19d08717e80ebbb9d30a8ea6401a77e64fffd9c85`.

Dylan Roy — delegated AI review. Actual performer: Cursor cloud agent, xAI Grok 4.7 (`grok-4.7-high-fast`), session `bc-0cf04834-c057-41c6-abc9-853f23aceb21`. Summoned by the author, Anthropic Claude, session `session_01NMeKEismAyeqgdB4sy2NJU`. Scientific effect NONE. Organizational-independence credit 0 (same provider as the Slice B author of the AMEND, shared account). Personal reading PENDING.

**Scope checked.** One replacement, in §3 Step 3, *`I₁`*, *The second term*, the case `c_τ < 4η`. The replacement paragraph in §2 is the Exact change paragraph of 6025531584, in the New bullet and again in the middle case of the three-case display. The Old bullet is the frozen sentence. The `c_τ ≥ 4η` case and the off-`𝔖` bullet stay the frozen sentences. `lu_exact.py` is inside the frozen controls. L6 checks Step 2's exponents and the slope bound `|ϑ| ≤ 1/2` on `𝔖`; it does not encode this case.

**The four steps, against the frozen note.**
- *Containment, by (3.3) with `w = ζ_t`.* `X₊ − c_τ = (v₊ − ζ_t)/(1 − ϑ)` and `X₋ + c_τ = −(v₋ + ζ_t)/(1 + ϑ)`. On `𝔖`, `|ϑ| ≤ 1/2`, so the segments between `±c_τ` and `X_±` have total `x̂`-length at most `2(|v₊| + |v₋| + 2|ζ_t|) ≤ 4η`. The symmetric difference of `{X₋ < x̂ < X₊}` and `{|x̂| < c_τ}` lies in those segments, including when `{X₋ < x̂ < X₊}` is empty.
- *Region and density, from "Absorbing `f₄^0` (on `𝔖`)."* That bullet places the segments in `{|f₄| ≥ (2/3)(|f₄^0| − E)}`, using `|ζ_t| ≤ |Δ||ξ̂|` on `𝔖` (`t ≤ r ≤ |Δ|`), and gives `(1 + |f₄^0|)^N p ≤ C_N(1 + E + |m₄|)^N/|Δ|`.
- *The expectation bound.* Given `J^♭`, the probability is at most `4η` times that density bound. The weight `|Δ|c_τ` cancels `|Δ|`, so the contribution is at most `C E[c_τ η (1 + E + |m₄|)^N/(1 + |f₄^0|)^N]`.
- *The order.* `c_τ = 6τ|Δ| < 4η` on this event, so `c_τ η < 4η²`. The note's bound `|v_±| ≤ Cr(1 + |Δ_B| + |a₀|)(1 + |f₄^0|)` gives `η ≤ C r(1 + |Δ_B| + |a₀|)(1 + |f₄^0|) + |ζ_t|` with `ζ_t = tξ̂`. For `N ≥ 2` the powers of `(1 + |f₄^0|)` are absorbed, the jet moments that remain are finite, and `|ζ_t|` contributes `O(t²)`. Since `t ≤ k ≤ r`, both pieces are `O(r²)`, which is the bound `|I₁| ≤ Cr²` uses for this case.

**Left in place.** §§0–2 and §§4–6 were not reread, and L1–L6 were not rerun. No repository edit and no pull request.



<div><a href="https://cursor.com/agents/bc-0cf04834-c057-41c6-abc9-853f23aceb21?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-0cf04834-c057-41c6-abc9-853f23aceb21&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

