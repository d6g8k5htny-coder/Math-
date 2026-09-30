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
  (`d ≥ 3`, hard-negative-fibre barrier), both opened before this packet and reviewed by this author on
  30 September; this packet's own contribution is the cap-free lower bound and the exact controls.
* §6 says what this is worth for the lifetime law: a lower bound for the coefficient of the `Θ(ℓ^{2/3})`
  compact-window selection loss (relative order `ℓ`); nothing for the leading term; nothing about the
  unrestricted density's remainder.

Files: `LOCAL_PAIRING.md` (the note), `pairing_check.py` (stdlib exact controls; `RESULTS.json` its output,
`-O` identical; mutants `M1`–`M4` exit 1, unknown label exit 2), `SOURCES.json` (exact identities of every
source; [SC] and [TSL] are consumed at their merged bytes, identical to the reviewed PR heads), `exploration/` (standard-library grid
elder-rule computation — evidence, not proof, not run in CI).

Review slices (§9): A deterministic (§§2–3); B the Gaussian transfer (§4); C the obligation (§5).
