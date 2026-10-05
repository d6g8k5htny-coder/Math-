# Erratum DL-AXIS-K-01: the axis-safe endpoint display in §6.4 omits the Lipschitz factor

Scientific effect: **NONE**. Dylan Roy, delegated AI work. Author: Anthropic /
Claude, Claude Code session `session_015wNj8LPTKXsaT68G3DgPPh`, the author of
`frontiers/d5_dimension_lift_20260929/PROOF.md` ([DL], [D5]).

This file is additive and lives outside the packet directory on purpose: the
packet's workflow (`.github/workflows/d5-dimension-lift.yml`) pins the exact
file set of `frontiers/d5_dimension_lift_20260929/` to `SOURCE_FILES.json`, so
nothing is added there. `PROOF.md` stays byte-identical (Git blob
`9d82c707fdb17d3072a8930f26dabedf59e456fc`, the bytes reviewed on Math-#141
and consumed by [CP] and [SC]). No theorem, constant, exponent, status, index
or review changes. The finding is OpenAI / GPT-6 Astra Pro's DL-AXIS-K-01,
main#259 comment 6004712957, raised during the IBA2-010 interface audit
(checks 3 and 4, main#259 comment 6004871493); it was verified against the
source before being written here.

## The display (`frontiers/d5_dimension_lift_20260929/PROOF.md` §6.4, "Axis-safe bound", line 524)

The source says that the two endpoint short columns `H_M e_x`, `H_S e_x` have
size at most `L r/2` "by [LP] (5.3)", and then concludes from Lemma D2 that

    |det H_M|, |det H_S| <= C r K^(d-1).

**(b) Citation.** The column bound `||H_i e_x|| <= L r/2` is the critical-segment
identity `||H_U e|| <= L |V - U| / 2` for `e = (V - U)/|V - U|` ([PP] (P15)),
which `PROOF.md` §4.6 (line 284) states and §5 (line 405) and §6.4 (line 516)
reuse as "the segment `MS` gives `||H_M e_x|| <= Lr/2`". [LP] (5.3) is the block
determinant identity `det H_i / r = alpha_i det A_i - r beta_i^T adj(A_i) beta_i`
and does not state a column bound; the "(5.3)" at line 524 is a mis-citation.
The bound itself is correct and is the one used below.

Lemma D2 (line 116) is `|det H| <= ||H e|| K^(d-1)`. With `||H_i e_x|| <= L r/2`
it gives

    |det H_i| <= (L r / 2) K^(d-1) <= (r / 2) K^d,          i in {M, S},

using `L <= K` from §1.1 (line 28), where `L` is the Hessian Lipschitz
constant on the chart and `K` dominates `1 + ||f||_(C^6)`. `L` is not a fixed
constant and cannot be absorbed into `C`: for `0 < r <= 1` and `L = K = A`,
the matrix `H = diag(r A/2, A, ..., A)` has operator norm `A` and exactly the
permitted short column, but `|det H| / (r K^(d-1)) = A/2` is unbounded in `A`.
The display as printed therefore omits the factor `L` (equivalently, after
`L <= K`, one power of `K`): the discrepancy is unbounded, not a constant. The
corrected display is the one above.

## Why nothing downstream changes

The very next clause of the same paragraph uses

    W_r |det H_X| <= C r^2 K^(3d),

which is what the corrected endpoint bounds give: `W_r = F_d(H_M) F_(d-1)(H_S)
<= |det H_M| |det H_S| <= (r^2/4) K^(2d)` (with equality on the typed support
and `W_r = 0` off it) and `|det H_X| <= K^d`. The faulty intermediate display
would have given the *smaller* power `K^(3d-2)`, which the source never used.
After the single division by [LP] (5.5), `Z_r >= z_* r^2`, the paragraph's
conclusion `W_r |det H_X| / Z_r <= C K^(3d)` on the whole strip `|v| <= s^(1/8)`
stands as written, and §6.5 (line 528) consumes exactly that `K^(3d)` bound.

Consequently Theorem I_d (1.5)–(1.6), Theorem G_d (1.7), the `r/s` powers, the
shell ledger of §6.7 and every statement in §1.2 are unchanged. The two
consumers, pinned at Math- `main` `c08e83597f94f923b8411dc13cdf28be3f214b37`:
- the C6 Palm route, `frontiers/c6_palm_route_20260929/PROOF.md`, blob
  `89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5` (called [CP] in the IBA2-010
  ledger; note that `PROOF.md`'s own `[CP]` tag denotes the planar collar
  template `reviews/d5_local_collar_20260928/COLLAR_PROOF.md`, a different
  file), whose §6.2 row R3a writes the endpoint product as `C r^2 K^(2d)` and
  the final bound as `C K^(3d)` directly, so it never relied on the misprinted
  display;
- the spectral cluster closure, `frontiers/spectral_cluster_closure_20260929/PROOF.md`,
  blob `16c56821b52fd76b0be791622b9c3809eafde75a` ([SC]), which consumes only
  Theorem I_d (1.6) and Theorem G_d (1.7) (its §1, display (1)), both unchanged.

## Scope check

The other two places where a short column or an axial displacement enters a
determinant bound already carry the Lipschitz factor through `K`: line 210
(`O(r |p| K)`) and line 506 (`A_i = S_0 + O(rK)`), and lines 405 and 516 cite the
segment identity correctly. **Within `PROOF.md`**, both slips, (a) the omitted
factor and (b) the "(5.3)" citation, are confined to the single display at
line 524.

**Consumer occurrence (AUD-308-CONSUMER-CITE-01).** The C6 Palm route,
`frontiers/c6_palm_route_20260929/PROOF.md` (blob `89eb8adf…`), §6.2 row R3a,
line 602, repeats the same citation: "short columns `H_M e_x`, `H_S e_x`, of
size at most `Lr/2` by [LP] (5.3)". There too the correct source is the
critical-segment identity, [DL] §4.6 / [PP] (P15). Its determinant powers are
already the correct `C r^2 K^(2d)` and `C K^(3d)`, so this is citation-only and
changes none of the consumed estimates. A repository-wide search (`git grep`
at Math- `main` `c08e8359…` over `frontiers/`, `reviews/`, `imports/`) finds
exactly these two occurrences of the "`Lr/2` by [LP] (5.3)" pointer: [DL] line
524 and [CP] line 602. Slip (a) occurs only in [DL].

## Record

- Finding: DL-AXIS-K-01, Astra, main#259 6004712957 (2026-10-05 22:45Z).
- Author readback: main#259, posted with this erratum.
- Codex review of Math-#308 (review 5422003010): four wording/pinning
  corrections to this file, applied in its second commit; (b) was raised there.
- Nonauthor read of Math-#308 (OpenAI / GPT-6 Astra Pro, comment 6005725870):
  PASS_SCOPED on the correction; AMEND_SCOPED AUD-308-CONSUMER-CITE-01 (the
  consumer occurrence above), applied in the third commit.
- Correction: this file. `PROOF.md` unchanged. Any future revision of
  `PROOF.md` should replace the display with the corrected one, cite [PP]
  (P15) for the column bound, and cite this erratum; any future revision of the
  C6 Palm route should likewise repoint line 602's citation.
