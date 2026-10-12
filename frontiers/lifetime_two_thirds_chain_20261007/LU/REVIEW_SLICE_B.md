**AMEND** on lifetime note LU, Slice B only (§3, the proof of Lemma U₀). GitHub refused both a new issue comment and an edit of the pickup [6025531584](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025531584) with HTTP 403, so this is the record.

Dylan Roy — delegated AI review. Actual performer: Cursor cloud agent, model Grok 4.7 (`grok-4.7-high-fast`), session `bc-13c58f23-eb0b-4a2b-bec9-7e651256c9b8`. Summoned by [6025530573](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025530573). Not the author. Scientific effect NONE. Organizational-independence credit 0. Personal reading PENDING.

Both bodies were hashed before and after the read and did not change. Note [6025486512](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025486512): 43,217 B, SHA-256 `373710a50e981e41472e51f49be4d50bcf5da70c01b518f833cb49b1e0680dac`. Controls [6025504196](https://github.com/d6g8k5htny-coder/main/issues/229#issuecomment-6025504196): 28,313 B, SHA-256 `eb6184ddcc452e6d40b1e7e19d08717e80ebbb9d30a8ea6401a77e64fffd9c85`. Sources on Math- `main` `34618d0d`: #237 blob `a97bf528`, #218 blob `70ca57ef`.

**Exact change.** Replace the bullet

> *Where `c_τ < 4η`*, both probabilities are `≤ C(c_τ + η)/|Δ|`, and with the weight `|Δ|c_τ` the term is `≤ Cη² ≤ Cr²`.

by

> *Where `c_τ < 4η`.* The symmetric difference of `{X_- < x̂ < X_+}` and `{|x̂| < c_τ}` is contained in the segments between `±c_τ` and `X_±`, hence in `{|f₄| ≥ (2/3)(|f₄^0| − E)}`, so `(1 + |f₄^0|)^N p ≤ C_N(1 + E + |m₄|)^N/|Δ|`. Its `x̂`-length is `≤ Cη`, and the term is at most `C E[c_τ η (1 + E + |m₄|)^N/(1 + |f₄^0|)^N]`. On this event `6τ|Δ| < 4η`. Substitute that bound for `τ|Δ|`. With `η ≤ C r(1 + |Δ_B| + |a₀|)(1 + |f₄^0|) + |ζ_t|` and `N ≥ 2`, each term is `O(r²)`: the powers of `(1 + |f₄^0|)` cancel, and the piece carried by `|ζ_t| = t|ξ̂|` contributes `O(t²) ≤ O(r²)`.

The comparison `≤ Cη² ≤ Cr²` does not close. `E[η² 1_{c_τ<4η}]` is not `O(r²)`, and that bound uses `sup p ≤ C/|Δ|` on a long interval, so the layer-device absorption never enters it. With the replacement, this piece is `O(r²)`, which is what `|I₁| ≤ Cr²` needs.

**Checked, and not a mismatch with §§0–2.** Steps 0–2 and the rest of Step 3 support (3.1) and (U₀). The density factor is `O(k²) ≤ O(rk)`. The gap-0 interpolation, using Step U3’s score and `(c_κ² − Y′²)_+ ≤ 36κ²Δ²`, is `O(r²κ²)`. On `𝔊`, `C₂` kills both sides and `C₁` is `G` by (1.1). In Step 2, `U_t` is #237 (2.1)’s `U`; `(κε₀ + k)(κε₀ + r) ≤ Cκ r^{3/2}`; #218 Lemma D’s first bound gives `E[𝔗^N 1_{C₃}] ≤ Cε₀` and `E[Δ² 1_{C₃}] ≤ Cε₀³`, hence both contributions are `≤ Crk`. The derivative identity, (3.2), (3.3), the `f₄`-intervals, `|e_∓| ≤ E`, the region `{|f₄| ≥ (2/3)(|f₄^0| − E)}`, and `24η/|Δ| ≤ 36τ` on `{c_τ ≥ 4η}` all match. Under (S.3) the weights and indicators used there are even, and each first-order piece is odd. The even piece `ϑ(v_± − ζ_t)` is in the Taylor remainder and is `O(κ r²)` after the layer-device absorption on `{c_τ ≥ 4η}`, not an `O(1)` or `O(κ)` leftover.

**Control L6.** Both `python3 -B -S` and `python3 -B -O -S` exit 0 with identical stdout, SHA-256 `8f47c8f039173bfd17f0bd8b4793a941127c93de7ffc413ca5fd6f64b738832e`. Mutant M6 exits 1 in both modes, empty stdout, stderr `FAILED: L6_exponents`.

**Not checked.** Proofs of §§0–2; §§4–6 and the header; controls L1–L5 and mutants M1–M5, M7. No repository edit and no pull request.



<div><a href="https://cursor.com/agents/bc-13c58f23-eb0b-4a2b-bec9-7e651256c9b8?cursor_ref=pr_footer&cursor_cta=open_in_web"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-web-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-web-light.png"><img alt="Open in Web" width="114" height="28" src="https://cursor.com/assets/images/open-in-web-dark.png"></picture></a>&nbsp;<a href="https://cursor.com/background-agent?bcId=bc-13c58f23-eb0b-4a2b-bec9-7e651256c9b8&cursor_ref=pr_footer&cursor_cta=open_in_cursor"><picture><source media="(prefers-color-scheme: dark)" srcset="https://cursor.com/assets/images/open-in-cursor-dark.png"><source media="(prefers-color-scheme: light)" srcset="https://cursor.com/assets/images/open-in-cursor-light.png"><img alt="Open in Cursor" width="131" height="28" src="https://cursor.com/assets/images/open-in-cursor-dark.png"></picture></a>&nbsp;</div>

