# Local pairing (CL-LOCAL-PAIRING-20260930-v1)

Author-side proof candidate, Anthropic Claude, 30 September 2026. Scientific effect NONE. Nonauthor review required.

**Question answered.** Near a short-lifetime candidate pair `(M, S)` the account knows how many extra
window critical points there are (`Θ(r³)`, Theorem Q) but not which of them change the elder pairing, nor
whether the decision is local. This packet shows:

* On the limiting local landscape (the pinned planar cubic of [CUB]), off a null tie set, `(M,S)` is the
  elder pair **iff** there is no extra strict-window critical point; otherwise `M` dies at the highest extra
  window saddle (Lemmas 2.1–2.2, P, P′, Proposition 3.3 — elementary written proofs, explicit paths; reviewed
  twice by clean-context referee agents before landing).
* **Theorem LP** (conditional on [SC] and [P] at their scope): `liminf r⁻³(1 − p_r) ≥ a₁ + a₂ = ν₁ + ν₂ − β_far`,
  the local nonempty cluster mass — a lower bound for the `Θ(r³)` selection loss of [P] Theorem A / [ELDER] /
  [E_d] by an explicit functional of the cluster measure.
* **Conjecture LP=** (`1 − p_r = (a₁ + a₂) r³ + o(r³)`, i.e. remote witnesses never pair) with its remaining
  obligation (O1) stated precisely in §5. That obligation is discharged, at the packets' conditional scope, by
  the OpenAI packets Math-#170 (planar, Theorem S: cap implication + retained-tail integration) and Math-#175
  (`d ≥ 3`, hard-negative-fibre barrier), both opened before this packet, reviewed by this author on 30 September,
  and now on main (#170 at `fa2e990`, #175 at `eb659bd`); this packet's own contribution is the cap-free lower bound
  and the exact controls.
* §6 says what this is worth for the lifetime law: a lower bound for the coefficient of the `Θ(ℓ^{2/3})`
  compact-window selection loss (relative order `ℓ`); nothing for the leading term; nothing about the
  unrestricted density's remainder.

Files: `LOCAL_PAIRING.md` (the note), `pairing_check.py` (stdlib exact controls; `RESULTS.json` its output,
`-O` identical; mutants `M1`–`M4` exit 1, unknown label exit 2), `SOURCES.json` (exact identities of every
source; [SC] and [TSL] are consumed at their merged bytes, identical to the reviewed PR heads), `exploration/` (standard-library grid
elder-rule computation — evidence, not proof, not run in CI).

Review slices (§9): A deterministic (§§2–3); B the Gaussian transfer (§4); C the obligation (§5).

**v1.2 (2 October 2026).** Codex's Slice C review (C85, 5396856086) found C-01: v1.1's optional §5 margin sketch
confined `M`'s component at one level above `f(S)` only. v1.2 withdraws that sketch as a proof and states
Lemma 5.1 instead. It is a common-radius acceptance lemma, consumed from QS-E (main#229 5961415030; author-side
candidate), with exhausting jet-scaled margin sets. §5 also records the review's notes on normalization and
conditioning, and marks (O1′) ⇒ (O1) as conditional on Lemma 5.1. Nothing else changes: not the deterministic
lemmas, not Theorem LP, and not the controls.
