# IBA2-010 interface ledger: regional imports behind [CP] and [SC]

Scientific effect: **NONE**. Dylan Roy, delegated AI work. Author: Anthropic /
Claude, Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh` (claim main#259
comment 6001134368).

**This is an author-side map, not an audit.** It makes no acceptance, closes no
IBA2 item, and changes no status. The ledger author also wrote [CP]
(`c6_palm_route`) and [DL]/[D5] (`d5_dimension_lift`). The IBA2-010 audit itself
needs a **non-Claude** owner. Everything below was checked mechanically against
Math- `main` at `dcd2a886e322738324a745adcad12fd3735bd2c5`:
- pins: `git rev-parse main:<path>` compared with each consumer's recorded blob;
- review IDs: read from the GitHub API.

Equation and section references are reproduced **as the consumer cites them**.
Checking that each cited statement matches its use, hypothesis by hypothesis, is
the auditor's job (§3).

## IBA2-010 as stated (main#259 audit II)

> Sharp factorial moments and the support-{1,2} cluster law. Conditional
> deductions survive; complete upstream verification remains open in this audit.
> Reconstruct named regional covariance/collision interfaces before declaring
> full closure.

The audit's bound sources, at Math- `b55b8f34`:
- [CP] `frontiers/c6_palm_route_20260929/PROOF.md`, blob `89eb8adf`;
- [SC] `frontiers/spectral_cluster_closure_20260929/PROOF.md`, blob `16c56821`;
- [CL] `frontiers/c6_factorial_moment_20260929/PROOF.md`, blob `f5bd013b`.

All three blobs are unchanged on current `main`.

## 1. [SC] (OpenAI / GPT-6 Astra Pro), named imports (SC §1, `SOURCES.json`)

| Id | Statement consumed by [SC] | Source, current-`main` blob = pin | Author | Nonauthor review on file |
|---|---|---|---|---|
| [P] | Sections 2–5: positive spectrum, contact frame `U_r`, regression, `C^q` moments, `Z_r/r² → z0 > 0`; `W_r/r² ≤ C K^{2d}` | `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md` `dfed3b8d` ✓ | OpenAI | Math-#106 OpenAI reviews 5341593068, 5341686506 and xAI 5341712731 (as cited by [D5]/[CP] for (5.5)) |
| [D5] | (1): `E_W N_r ≤ C r³`; `E_W N({Rr<|x|<ρ}) ≤ C r³(R⁻²+ρ²)`, R ≥ 4 | `frontiers/d5_dimension_lift_20260929/PROOF.md` `9d82c707` ✓ | Anthropic Claude | Math-#141 OpenAI 5357858391 (continuum A+B) and 5357882570 (C, G_d); planar bases: xAI 5894512272, `reviews/d5_collar_count_20260928/`, `reviews/d5_i5_planar_f_20260928/` |
| [RM] | (2) first part: `E_W N(D_ρ) = k r³ ∫_{D_ρ} Λ + O_ρ(r⁴)`, continuous positive normalized kernel | `frontiers/remote_window_20260924/PROOF.md` `b383bfcc` ✓ | OpenAI | main#76 (Theorem A, every d; as cited by [CP], [D5]) |
| [RC] | (2) second part: `E_W (N(D_ρ))₂ = O_ρ(r⁵)`, all-index (Corollary D) | `frontiers/remote_collision_20260928/PROOF.md` `7b48a88e` ✓ | Anthropic Claude | Math-#110: OpenAI 5342280263 and v4 re-review 5343164624; xAI/Harper scoped 5342481786; ledger and Bonferroni record Math-#113 |
| [C6] | `E_W (N_r)_q ≤ C_q r³`, every fixed q ≥ 2 (used only for uniform integrability) | `frontiers/c6_palm_route_20260929/PROOF.md` `89eb8adf` ✓ | Anthropic Claude (this author) | Math-#145 OpenAI 5356233690 (§4), 5357899713 (§§5–7, AMEND R3a), 5358116559 (successor ACCEPT) |
| [CUB] | #158 Theorem C deterministic classifier, algebraic scope only | `frontiers/planar_cubic_cluster_20260929/PROOF.md` `bb446d08` ✓ | OpenAI | Math-#158: xAI 5359488967 (Slice A, C2–C14 ACCEPT); OpenAI/Codex Slice D 5359601495 and Slice B 5359738045; Claude Slice C 5359814083 |
| [RCL] | Generic Poisson / compound-Poisson consequences | `frontiers/c6_rare_cluster_laws_20260929/PROOF.md` `2ab625ce` ✓ | OpenAI | Math-#153: Claude 5358565704 (§1 interface, §§2,5–7); xAI/Harper 5358623521 (§§3–4) |
| [RCL-A] | Sharp Poisson coefficient | `.../SHARP_POISSON_COEFFICIENT.md` `9f96f7d6` ✓ | OpenAI | Math-#153 (as above) |
| [LM], [DEEP] | Prior credit only, not consumed | `b5c18aac` ✓, `309a38ca` ✓ | OpenAI | n/a |
| AUDITED-159 | Audited, **not** consumed | `frontiers/c6_cluster_law_20260929/PROOF.md`: pin `1ce3769e`, `main` `ba492c8e` (**differs**) | Anthropic Claude | Not a premise of [SC]. The drift is informational only. |

[SC]'s own reviews on Math-#162, all at stated scope and conditional on the
pinned imports:
- Claude Slice B 5359845136 (§§4–6);
- Claude Slice A 5359968447 (§§2–3);
- OpenAI/Codex Slice A 5360029463;
- OpenAI/Codex Slice C 5359879627 (§§7–8);
- Claude Slice D 5360082678 (`GLOBAL_DERIVATIVE_WEIGHTED.md`).

## 2. [CP] (Anthropic Claude, this author), regional rows of §6 and inputs (`SOURCE_MAP.json`)

All 8 `SOURCE_MAP.json` inputs are unchanged on `main`: [C6L] `f5bd013b`,
[DL] `9d82c707`, [LP] `dfed3b8d`, [PP] `d8acf0bc`, [CP-collar] `b5647907`,
[IW] `f53a527c`, [RM] `b383bfcc`, [EDL] `7303bd79`.

| [CP] §6 row | Frame / interface consumed | Source statement | Nonauthor review on file |
|---|---|---|---|
| R1, pin balls | `Y` of [DL] §4, (4.2)–(4.12) | [DL] Theorem P_d; planar (P10)–(P12), (P18)–(P20) | Math-#141 5357858391; planar xAI 5894512272 and Math-#111 |
| R2a–R2c, collar | raw `∇f` [DL] §5.4; `Gc` [DL] (5.2)–(5.3); fixed floor [DL] §5.6 | [DL] Theorem C_d; planar (C4)–(C19); floors `c r¹⁰`, `c|v|⁴`, `c` | Math-#141 5357858391; `reviews/d5_collar_count_20260928/` |
| R3a–R3b, shells | raw `(∇f, f)` [DL] §6.5; `Z` [DL] (6.4), (6.11) | [DL] Theorem I_d; planar (I9)–(I33); floors `c s¹⁰`, `c|v|⁶` | Math-#141 5357882570; `reviews/d5_i5_planar_f_20260928/`; Math-#107 Claude analytic review via Math-#109 |
| R4, remote | `Y_x = (∇f(x), f(x))`, [RM] §§2–3, (10), (14) | [RM] Theorem A, uniform remote nondegeneracy, coupling (5) | main#76 |
| normalizer | `Z_r ≥ z_* r²` | [LP] (5.5) | Math-#106 |
| Lemma D / R / §8 | [C6L] §§2–5, Lemma R, §8 assembly | [C6L] | Math-#140 OpenAI 5355120953, 5355457002, 5355682335; xAI 5894209739 (Lemma R and §8) |
| Corollary Θ (lower bound only) | `Q^W(N_r ≥ 2) ≥ c r³` | [EDL] (A4) | Integrated by Math-#129. Not needed for the IBA2-010 **upper** bounds. Review status not re-traced here. |

## 3. What the IBA2-010 auditor still has to check

Only an independent check can supply these. The ledger supplies the map, not
the verification.

1. **(2) for [SC].** [RC] Corollary D's all-index scope and fixed-ρ uniformity
   must cover [SC]'s use with Λ as the **sum** of the index-specific kernels.
   [RM]'s `O_ρ(r⁴)` remainder must hold at the same marks and window.
2. **(1) for [SC].** The shell estimate's uniformity in `R ≥ 4` and ρ must match
   [SC] §7's choice `R_r = ρ'/r` with ρ' fixed. [SC] states this is permitted;
   the auditor confirms it against [D5].
3. **[CP] §6 joint-floor rows.** Each floor exponent and each Gaussian tail
   factor in the R1–R4 table must be the one the cited [DL] equation proves, for
   the conditioned measure `Q_r` with the extra witness conditioning. [CP] §6
   reads them from [DL] and [RM] §3.
4. **Gap at `d ≥ 3`.** For `d ≥ 3`, both [CP] and [SC] consume [DL]'s continuum
   rows. Their acceptance is OpenAI's source-exposed review (Math-#141); the
   planar rows have xAI and Claude records. Whether that suffices for "full
   closure" is the auditor's call.
5. **[EDL].** Out of scope for the upper bounds. If the audit also covers the
   matching lower bound (Corollary Θ), trace [EDL]'s review separately.
