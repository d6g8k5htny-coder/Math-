# Elder-selection chain: source-bound status audit under the owner's five-value taxonomy

**Object:** `CL-ELDER-SELECTION-CHAIN-AUDIT-20261031-v1`. **Author:** Anthropic Claude, Claude Code session
`session_017Mi3hxjaxV45x6zo6o1ee3`, delegated AI work for Dylan Roy. **Kind:** source-bound review record. It states,
for every link of the Theorem A/B/C chain and the lower-bound chain, which event the link is about, what its proof is,
who read it, and what remains open, using the owner's five values (Proved / Proved under assumptions / Conditional /
Conjectural / Refuted). **Scientific effect: NONE.** It changes no theorem, review verdict, label, flag, register or
canonical surface; section 8 proposes wording for the integrator (B-003). It is not a register and creates none
(steward section 7). Same GitHub account as every lane: organizational-independence credit 0; human review 0.

**Trigger.** The owner's assessment received in this session at 2026-10-31T15:14:11Z, recorded verbatim at
[main#686 comment 6546811519](https://github.com/d6g8k5htny-coder/main/issues/686#issuecomment-6546811519) and in
[`sources/OWNER_ASSESSMENT_20261031.txt`](sources/OWNER_ASSESSMENT_20261031.txt) (7,395 bytes, SHA-256
`73ea6544478c3c8d0bfbae26ce58d4b04325b9f641fde31b9c6d3385eb3b187a`). Its items 1, 2, 4, 6 and 7 are addressed here;
item 3 (unrestricted parameter estimates) is only located, not audited; item 5 (external specialist review) is the
owner's to commission, and section 5 says what to hand the reviewers.

**Source cuts.** Math- `19a55750451b8016b50d1d20be6a18c021807ecb`; main `4712fc13b99a4e4df68481663657b2952ce858fe`;
Math-#543 head `9e89980bfa4f281e00550f481202033775f35485`. Every cited file is bound by repository, commit, path, git
blob, byte length and SHA-256 in [`CLAIMS.json`](CLAIMS.json); `python3 -B -S check_claims.py` verifies those identities
and the dependency graph against the local object store. The checker certifies custody only.

## 0. Summary

The chain already contains the two things the owner's items 1 and 2 ask for, and lacks the third.

- **The actual event is defined and its deterministic core is kernel-checked.** `p_r` is the `Q^W`-probability of the
  Borel event `{d_f(M) = f(S)}` on the Morse distinct-value locus, with `d_f(M)` the maximin connection level (P
  section 8). Every estimate of the chain refers to this `p_r`, including both lower bounds (E0). The step from the
  local good event `G_r` to "S is the global elder partner" is the deterministic cap theorem, and it is kernel-checked
  on the torus from the C⁴ hypotheses of CAP (1) (D1). That theorem is the topological witness of item 2: (C1) a
  ceiling on the cap, (C2⁺) a frontier bound attained only at `S`, (C3) a path through `S` to an older point staying
  above `f(S)`. No critical point elsewhere can change the pairing once these hold.
- **The probabilistic links are prose, read by two AI reviewers, one of them this session.** `Q^W(G_r^c) ≤ C r³` (A-II),
  the normalizer floor (A-I), the Kac–Rice bridge (B, C) and both lower bounds (L2, L3) are complete written proofs
  whose nonauthor reads are by xAI/Grok and by this session only. Theorem B is stated for elder-selected pairs and is
  Proved; Theorems C and U are stated for bars and are Conditional on exactly one further input, the classical
  identification of elder death with bar death (F5), which the project holds as an interface clause (v1.1, S1). For the lower bounds, the cap second pass and the
  reconciliation, this session is the sole nonauthor reader. There is no human review and no review outside those two
  providers anywhere in the chain.
- **No kernel-checked statement of any probabilistic theorem about the actual event exists.** The statement register
  makes `p` a primitive field. The formal countermodel the owner refers to is Math-#543's `oneLaw` (`p ≡ 1`): it proves
  the upper shape and contradicts the two-sided shape, so at the interface level "upper selection ⇒ positive lower rate"
  is Refuted (F1), and the register's shapes do not pin down the theorems (F2). Closing this needs the regression law as
  a measure in Lean, which the register itself classifies as Mathlib-blocked.

Status histogram over the 23 claims: Conditional 3, Conjectural 4, Proved 10, Proved under assumptions 3, Refuted 3. Open obligations listed: 37. Claims whose only nonauthor
reader is this session: D1, L2, L2b, L3.

| ID | Claim | Event | Status | Evidence | Nonauthor readers | Open |
|---|---|---|---|---|---|---|
| E0 | The elder event and p_r | elder | **Proved** | prose | Anthropic session_017, xAI/Grok | 1 |
| D1 | Deterministic cap theorem: CAP (1) on the cylinder forces the global elder partner | deterministic | **Proved** | kernel + prose | Anthropic session_017 | 2 |
| A-I | Full-normalizer floor Z_r >= z_* r^2 and Z_r / r^2 -> z_0 > 0 | normalizer | **Proved** | prose | Anthropic session_017, xAI/Grok | 2 |
| A-II | Boundary layer: Q^W(G_r^c) <= C r^3 (P (7.8)) | good-jet | **Proved** | prose | Anthropic session_017, xAI/Grok | 3 |
| A | Theorem A (P 1.1): 0 <= 1 - p_r <= C r^3 on compact B, K, all frames, 0 < r <= r_* | elder | **Proved** | prose | Anthropic session_017, xAI/Grok | 3 |
| L2 | Theorem E1: planar lower bound 1 - p_r >= c r^3 | elder | **Proved** | prose | Anthropic session_017 | 2 |
| L2b | Corollary E2: c r^3 <= 1 - p_r <= C r^3 in d = 2 | elder | **Proved** | prose | Anthropic session_017 | 0 |
| L3 | Every-d lower bound (OA-ELDER-DIMENSION-LIFT Theorem A (A2)-(A3)) | elder | **Proved** | prose | Anthropic session_017 | 2 |
| L3b | CL-ELDER-LOWER-ALL-D Theorem E1_d (soft-eigenplane lift) | elder | **Conjectural** | prose | none located | 1 |
| LP-P | Lemma P, Lemma P', Proposition 3.3: the extra-window-saddle criterion on the pinned planar cubic | deterministic | **Conjectural** | prose | none located | 1 |
| LP-LP | Theorem LP: liminf r^{-3}(1 - p_r) >= a_1 + a_2 = nu_1 + nu_2 - beta_far (planar) | elder | **Conditional** | prose | none located | 2 |
| LP-EQ | Identified selection-failure law r^{-3}(1 - p_r) -> alpha_1 + alpha_2 (Theorem S planar, Theorem F every d; Conjecture LP=) | elder | **Conjectural** | prose | none located | 2 |
| W | Window critical-point counts: E_{Q^W} N_{r,j}(torus minus pins, between-pin height window) <= C r^3 | candidate-count | **Proved** | prose | Anthropic session_017, xAI/Grok | 2 |
| F5 | Identification of the maximin level with the H0 bar death and of elder-selected pairs with finite bars | deterministic | **Proved under assumptions** | prose | Anthropic session_017, xAI/Grok | 1 |
| B | Theorem B (P 1.2): compact-window densities and the O(ell^{2/3}) difference | elder-vs-candidates | **Proved** | prose | Anthropic session_017, xAI/Grok | 2 |
| C | Theorem C (P 1.3): unrestricted leading density nu_cand^all ~ nu_eld^all ~ c_{d,L} ell^{-1/3} | bars-vs-candidates | **Conditional** | prose | Anthropic session_017, xAI/Grok | 3 |
| U | Theorem U: the unrestricted selection difference does not vanish | bars-vs-candidates | **Conditional** | prose | OpenAI | 2 |
| C7 | Candidate C7: unrestricted difference rate 0 <= nu_cand^all - nu_eld^all <= C ell^{2/3} | bars-vs-candidates | **Refuted** | prose | OpenAI | 0 |
| RHO | Rejected density rho_rej(ell) = nu_cand^all - nu_eld^all = O(1) (C7-total Theorem K; ledger DP-07) | bars-vs-candidates | **Conjectural** | prose | none located | 1 |
| F1 | Interface-level implication "upper selection shape implies two-sided rate shape" for every PairLawInterface | formal-interface | **Refuted** | kernel | OpenAI | 1 |
| F2 | The register shapes are kernel-checkable statements of Theorems A, B, C, E2, E4 about the actual event | formal-interface | **Refuted** | register text | OpenAI | 1 |
| F3 | Formal elder bridge: trap data give the C263 death and one ordinary-H0 interval summand | deterministic | **Proved under assumptions** | kernel | OpenAI | 1 |
| F4 | Compact Morse adapter: the trap data exist for every nonessential nondegenerate maximum of a smooth periodic Morse-distinct function | deterministic | **Proved under assumptions** | prose | OpenAI | 2 |

Evidence "kernel" means a Lean kernel check with only `propext`, `Classical.choice`, `Quot.sound`; "prose" means a
written proof. "Nonauthor readers" names providers; every one is an AI lane on the shared GitHub account.

## 1. The actual event, and where every estimate attaches (owner item 1)

**Definition (P l.290–297, E1 lower-bound packet section 1, E2 replacement for measurability).** For fixed pins and a
sample `f`,

    d_f(M) = sup { min_t f(γ(t)) : γ(0) = M, f(γ(1)) > f(M) },   sup ∅ = −∞.

The elder event is `{d_f(M) = f(S)}` on the Morse distinct-value locus, which has full `Q` and `Q^W` measure for
each fixed `r, b, k, R` (P section 8). It is Borel: `{d_f(M) > h}` is a countable union of rational polygonal-path
tests. `p_r(b,k,R) := Q^W_r(elder event)`. On that locus the event is "S is the global ordinary superlevel elder death
partner of M" (F5).

**Lean.** The deterministic sets are definitions in `frontiers/cap_first_exit_lean_20261002/CapFirstExit.lean`:
`connectionLevels f M b` (l.124, the maximin set), `CapHyp.joinedLevels` (l.211, closed-superlevel merge levels) and
`CapHyp.olderPeakLevels` (l.332, levels at which the component of `M` holds a strictly higher local maximum). Under
`CapHyp` they have the same greatest element `s = f(S)` (`maximin_eq` l.141, `elder_death_level` l.217,
`elder_death_level_peak` l.338). C263 `SuperlevelBar.lean` defines the Euclidean strict-clearance death with an explicit
empty default (TF-SCOPE). What does not exist in Lean: the event as a set of sample paths, the law `Q_r`, the weight
`W_r`, and `p_r` as a measure of the event. In `specifications/lean_statements_20261010/Specifications/Lifetime.lean`
the pair law is

    structure PairLawInterface ... where
      p : ℝ → ℝ → ℝ → OrthonormalBasis (Fin d) ℝ (E d) → ℝ
      p_nonneg : ...      p_le_one : ...

with the docstring "no field ties `p` to them" (l.455–467). That is the whole of the formal gap of item 1.

**The formal countermodel.** Math-#543, `cbz/lifetime_pair_law/CounterexampleE4.lean` (blob `3b7712e4`, 1,743 bytes):
`oneLaw` sets `p := fun _ _ _ _ => 1`; `oneLaw_upper` proves `ParentUniformSelectionA` for it with `C = 0`;
`oneLaw_refutes_twoSided` derives `c (r_*/2)³ ≤ 0` from `PlanarTwoSidedRateE4` and contradicts `c > 0`. Lean-checked
at Math- `5a470bfd` (run 40957238766), with the three standard axioms; two OpenAI reviews passed the derivation at
scope and an Anthropic different-family review is open at this cut. The register's own round-4 triage already named
`p ≡ 0` and `p ≡ 1` as falsifying inhabitants (REG-SCOPE). Both say the same thing: the interface fixes neither the
upper nor the lower statement, so nothing formal connects the estimates to the event.

**Where each estimate attaches.**

| Estimate | What it is about | How it reaches the elder event |
|---|---|---|
| A-I floor `Z_r ≥ z_* r²` | the normalizer | denominator of every `Q^W` bound |
| A-II `Q^W(G_r^c) ≤ C r³` | the jet / sup-norm event `G_r` | through D1: `G_r ∩ Morse ⊆ elder event`, so `1 − p_r ≤ Q^W(G_r^c)` |
| D1 cap theorem | deterministic | the inclusion itself, kernel-checked |
| L2, L3 lower bounds | an explicit subevent of `elder event^c` (`d_f(M) ≥ b − k r³/4 > f(S)`) | direct: `1 − p_r ≥ Q^W(subevent) ≥ c r³` |
| W window counts | critical points in the height window | not used by Theorem A; explain the failure mechanism; not elder statements |
| B compact-window densities | elder-selected candidate pairs (`ν_eld`, defined through E0) against candidates (`ν_cand`) | `ν_eld` integrates `p_r` against the candidate intensity (E2 Kac–Rice, P sections 9–11); no bar identification is used |
| C unrestricted densities | finite bars (`ν_eld^all`) against candidates | the same Kac–Rice route (P section 13) plus the Morse-locus identification bars = elder-selected pairs (F5, P l.445) |
| U, C7, RHO | the difference `ν_cand^all − ν_eld^all` | far pairs separated by a level curve are candidates and not bars |

**Assumptions per step** are the `obligations` lists in `CLAIMS.json`. The two that carry the chain are: the full
normalizer floor and the boundary-layer integration (A-I, A-II: prose, no numerical constants, no formalization), and
the classical identification of elder death with bar death on the Morse locus (F5: an interface clause in Lean).

## 2. The extra-critical-point problem (owner item 2)

Two different things are true, and the chain keeps them apart.

**Where an extra critical point cannot interfere.** On `G_r` the cap theorem gives more than a local picture. CAP
section 4: "Every critical point in D lies on the ridge, hence D contains precisely M and S." CAP (13): the ridge rises
to `g(2r) ≥ b + (11/96) r³ > b` inside the cylinder, so the older point `z` is reached without leaving `D`. CAP section
5: every path from `M` to a point above `b` crosses the frontier of `C`, where `f ≤ s`. Hence `d_f(M) = s` whatever
`f` does outside `D`, and whatever critical points exist there. This is the content of `CapHyp.barrier` (l.114),
`maximin_eq` and `elder_death_level_peak`, composed on the torus in `torus_elder_death_level_blocks` (l.5256) from the
C⁴ hypotheses of CAP (1). So the topological witness the owner asks for exists, is explicit, and is kernel-checked; its
one open item is a nonauthor alignment review of the Lean statements against CAP (I-4).

**Where an extra critical point is exactly the failure.** Off `G_r` the pairing fails only through a competing saddle:
on the limiting cubic, `(M,S)` is the elder pair iff there is no extra strict-window critical point, and otherwise `M`
dies at the highest extra window saddle (LP-P; Math-#170 Theorem E part 3). The lower bounds build such a configuration
with probability `≥ c r³` by an explicit path above `f(S)` to a point above `b` (L2 planar, L3 every `d`). So "bound the
probability of configurations that violate the conditions" is answered on both sides: `≤ C r³` (A) and `≥ c r³` (L2,
L3), with the exact limit `α₁ + α₂` only a candidate (LP-EQ).

**Good configurations at leading order.** P section 13 removes the compact-mark restriction by dominated convergence:
the unnormalized intensity has the target-growth majorant (13.4), `p_r → 1` pointwise by Theorem A on compact
neighbourhoods (P l.415), and the far population is `O(1)` (14.1). That is Theorem C's leading term (C). What does
not exist, and cannot, is a quantitative unrestricted rate: Theorem U shows `ν_cand^all − ν_eld^all ≥ c_* > 0` (U), so
candidate C7 is Refuted and the `O(1)` rejected density (RHO) is a candidate. "Counting candidate maximum–saddle pairs
is not the same as counting actual persistence bars" is therefore a theorem of the project, at leading order and in
the difference, not a gap: the two counts agree to leading order `ℓ^{−1/3}` and differ by a positive bounded-below
amount.

**What remains open mathematically.** (a) The alignment review of D1 (I-4). (b) Formalization of anything
probabilistic (A-I, A-II, E2), blocked on a Gaussian-field measure in Lean. (c) The bar bijection on the Morse locus
(F5) as a theorem rather than an interface clause: the elder bridge (F3) and the compact Morse adapter (F4) give one
interval summand per maximum from trap data, and torus_filtration lists once-counting, interval decomposition and bar
bijection as not established. (d) Nonauthor reads of LP-P, L3b, LP-EQ and RHO.

## 3. Status per claim (owner item 4)

The table in section 0 is generated from `CLAIMS.json`. The assignment rule is in that file and repeated here: status
follows the located evidence, not the author's label. "Proved" requires a complete proof of a fixed statement and a
kernel check or a nonauthor read with no open defect at the stated scope; an author-side complete proof with no located
nonauthor read is "Conjectural (candidate)". Under that rule four items the owner may have taken as settled are
candidates: the Claude every-`d` lift L3b (the OpenAI lift L3 is read), the deterministic cubic criterion LP-P (two
author-side derivations agree; no read located), the identified failure law LP-EQ (Math-#170 Theorem S, Math-#175
Theorem F) and the rejected density RHO. The owner's item 4 names "the proposed next-order expansion and
rejected-density estimate" as not established; this record agrees on the second and did not locate a next-order
expansion of `ν_eld` in the chain (none is in the headline statements).

**Status propagation (v1.1, finding S1 of the Grok Bot a4 and 01SHCrxv reads).** A Proved claim may depend only on
Proved claims, and `check_claims.py` now enforces it. Theorem B's `ν_eld` is defined in P through the elder relation
(E0), so B depends on A and E0 only and stays Proved. Theorems C and U are stated for finite bars; their only
non-Proved dependency is F5, the Morse-locus identification of elder-selected pairs with bars, which this record holds
at Proved under assumptions because the project consumes it as a classical fact and, in Lean, as an interface clause.
So C and U are Conditional on F5 alone (v1.0 had Proved); discharging F5 as a theorem makes both Proved with no
other change. The refutation of C7 inherits the same dependency through U and is recorded as such.

Numerical coefficients: Theorem C states `c_{d,L}` as an identified Gaussian/angular integral (15.2) with no value. The
SIDE24 numerical coefficient packets are outside this audit. No numerical value of `C`, `r_*`, `z_*`, `c_{B,K}`,
`c_{d,L}`, `α₁ + α₂` or `c_*` is established anywhere in this chain, and none belongs in a headline statement.

## 4. Inconsistencies between surfaces

| ID | Finding | Proposal |
|---|---|---|
| I-1 | main `docs/DISCOVERY_PRIORITY_LEDGER_20260925.md` DP-02 (l.18, l.157) says parent sections 2–7 are **AMEND**; main `STATUS.md` D1 (l.88) and Math- `PROOF_INDEX.md` (l.27) record ACCEPT at existential scope from the 28 September reconciliation, whose residual `R-A3-congruence` is DISCHARGED by E1 (REC `LEDGER.json`). The ledger cell was aligned with `STATUS.md` of 26 September and repeated unchanged by the 28 October refresh ([main#669 6465885945](https://github.com/d6g8k5htny-coder/main/issues/669#issuecomment-6465885945)). | Root decides which surface governs (B-003). This record reads the ledger cell as stale. |
| I-2 | REC section 2 and the PROOF_INDEX D1 row (l.27): "No lower bound is asserted for d ≥ 3" (true of the reconciled D1 chain) while the every-`d` lift L3 was ACCEPTed and integrated (Math-#129). PROOF_INDEX lists the lift in its PR inventory (l.107, 110, 111) and `STATUS.md` D1 notes it; the D1 row of PROOF_INDEX does not point to it. | Add the pointer to the PROOF_INDEX D1 row. |
| I-3 | GPT-6's pickup 6513952657 and review 5724470777 (01XJMJ) on Math-#543 record `CounterexampleE4.lean` (blob `3b7712e4`) as 1,720 bytes; the blob is 1,743 bytes (1,720 is the character count). Review 5707632836 states no byte count. The SHA-256 in the README is correct. | Note only. 01XJMJ posted its own correction at [Math-#543 6548199529](https://github.com/d6g8k5htny-coder/Math-/pull/543#issuecomment-6548199529). |
| I-4 | `frontiers/cap_first_exit_lean_20261002` has no PROOF_INDEX row and `MANIFEST.json` records `alignment_review: NOT_CLAIMED`; the only kernel-checked link of the chain is invisible to a cold-start reader of PROOF_INDEX. | Add a row: "Proved (kernel); alignment review open". |

## 5. Independence (owner item 5)

Every nonauthor read in this chain, by performer:

| Reader | Claims read | Provider distinct from the author | Human |
|---|---|---|---|
| xAI Grok (G1, G2, G4, IW, I5 records) | E0, A-I (partial), A-II (partial), A, W, F5, B, C | yes | no |
| Anthropic Claude session_017 (this session) | E0, D1 (prose), A-I, A-II, A, L2, L2b, L3, W, F5, B, C; reconciler of REC and D5 | yes | no |
| OpenAI (REV-U, REV-CE4-ENG, REV-CE4-FORMAL, REV-EB, REV-CMA) | U, C7, F1, F2, F3, F4 | REV-U yes; the others same provider as the authors | no |

This session is also the author of Theorem U and of the Lean cap module `CapFirstExit.lean`, and the sole nonauthor
reader of D1 (prose), L2, L2b and L3. A reader of this record should weigh it accordingly: the person best placed to
have missed a shared blind spot in the chain's acceptance wrote this audit.

External specialist review is the owner's to commission. What to hand the two reviewers, without the project's
interpretation: the parent `P` with `E1` and `E2` and `CAP` (the four immutable bytes in REC section 1), the planar
lower bound `EL` and the dimension lift `DL`, and this record's `CLAIMS.json` as a map. The two questions the owner
proposes already have candidate targets here: the weakest indispensable lemma of Theorem A is the pair A-I/A-II
(the normalizer floor and the eigenvalue-coordinate boundary-layer integration, P sections 5–7), and for Theorems B and
C the marked Kac–Rice identification of `Q^W` with the Palm law (E2). A counterexample hunt should start from the
exact failure mechanism (LP-P) and from the far-pair separation of Theorem U.

## 6. Dependency lists (owner item 6)

`CLAIMS.json` gives each claim its statement, event, status, evidence, exact sources (repository, commit, path, blob,
bytes, SHA-256), reviews (performer, record, verdict, independence flags), `depends_on` and `obligations`.
`check_claims.py` verifies that every cited blob exists in the local object store with the recorded length and digest,
that the recorded commit maps the path to that blob when the commit is available, that every status is one of the five
values, that every `depends_on`, source and review reference resolves, and that no claim is "Proved" without a review or
kernel check. `test_check_claims.py` exercises it, including tampered-digest, wrong-length, unknown-status, dangling
dependency and unreviewed-"Proved" failures, and byte-identical output in normal and optimized Python. The checker does
not read Lean, does not run any proof, and certifies no Layer A property; it is custody, not mathematics. The 44 bound
sources include two from `main` and two from the Math-#543 head; `--repo main=DIR` checks the former, and the latter
are checked when that head is fetched.

## 7. Metrics baseline (owner item 7)

Computed from this record at the cuts above; the values are in `CLAIMS.json` under `metrics`.

| Metric | Value at this cut |
|---|---|
| Claims audited | 23 (Conditional 3, Conjectural 4, Proved 10, Proved under assumptions 3, Refuted 3) |
| Open obligations listed | 37 |
| Counterexamples recorded | 4: `p ≡ 1` (F1) and `p ≡ 0` (F2) at the interface, open pending a successor interface; Theorem U against C7, resolved; LOCAL_PAIRING C-01, resolved by withdrawing the sketch |
| Claims downgraded or withdrawn | 3: C7 → Refuted; the LOCAL_PAIRING v1.1 section-5 sketch withdrawn; the C7-total v1 memo retracted |
| Independent (human or external) reviews completed | 0 |
| Distinct AI reviewer providers on the probabilistic chain | 2 (xAI/Grok; Anthropic, this session) |
| Formalized results whose alignment with the intended statement a nonauthor confirmed | 1 (F3, same provider); D1 has no alignment review; the probabilistic theorems have no formal statement about the actual event |
| Failed verifications that led to corrections | 6: congruence erratum E1; section-9 replacement E2; wording W1 and the embedding radius; Theorem U v1 → v3; LOCAL_PAIRING C-01; Math-#543 metadata |

## 8. Proposed wording for the canonical surfaces (for the integrator; not applied here)

- PROOF_INDEX D1 row: append "Status (owner taxonomy, 2026-10-31 audit): Theorems A, B, C **Proved** at existential
  scope, prose, nonauthor AI reads by xAI/Grok and Anthropic session_017 only; no formal statement about the actual
  event (register BLOCKED_INTERFACE; Math-#543 countermodel). Deterministic cap step **Proved (kernel)** in
  `frontiers/cap_first_exit_lean_20261002`, alignment review open. Lower bound `1 − p_r ≥ c r³`: **Proved** for d = 2
  (EL, read) and for every fixed d ≥ 3 (DL, read, Math-#129); CL-ELDER-LOWER-ALL-D is a candidate."
- main `docs/DISCOVERY_PRIORITY_LEDGER_20260925.md` DP-02 current-state cell: resolve against `STATUS.md` D1 (I-1).
- `STATUS.md` "How to verify" or the D1 row: name the formal-coverage boundary in one sentence: "No kernel-checked
  statement of Theorems A, B or C about the elder event exists; `PairLawInterface.p` is primitive."
- A PROOF_INDEX row for `frontiers/cap_first_exit_lean_20261002` (I-4).

## 9. Revision history

- **v1.0, 2026-10-31, head `1d8267ea`.** First record. Nonauthor reads: 01XJMJ (Anthropic; sources and inconsistencies,
  [review 5724603343](https://github.com/d6g8k5htny-coder/Math-/pull/554#pullrequestreview-5724603343), PASS_SCOPED with
  F1, F3, F4), Grok Bot agent 4 (xAI; status propagation, [6548325142](https://github.com/d6g8k5htny-coder/Math-/pull/554#issuecomment-6548325142),
  AMEND S1), 01SHCrxv (Anthropic; custody 44/44 and S1, [main#684 6548184976](https://github.com/d6g8k5htny-coder/main/issues/684#issuecomment-6548184976)).
- **v1.1.** S1: C and U Conditional on F5; B's dependency on F5 removed because P states Theorem B through the elder
  relation; a status-propagation rule added to `check_claims.py` with a test. F1: 01XJMJ's nine checker tests added.
  F3: the I-3 attribution corrected. F4: the I-2 wording corrected. No source identity, review record, claim statement
  or inconsistency other than I-2 and I-3 changed.

## 10. Non-claims

No theorem is proved, improved, weakened or withdrawn here. No review verdict is issued on any proof; the statuses
summarize located records under a stated rule. No numerical constant is claimed. Nothing here is independent review
in the owner's sense of item 5. The checker certifies file identities, not mathematics. Item 3 (unrestricted parameter
estimates: small gaps, large births and gaps, intermediate scales, chart boundaries, constant dependence) is located in
P sections 13–14 and the D5/C6 packets but not audited; it is the natural next record.
