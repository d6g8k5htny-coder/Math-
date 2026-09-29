# Reconnaissance memo — literature and novelty check for the near-diagonal H0 lifetime law — 2026-09-29

**Object:** CL-LIT-RECON-LIFETIME-20260929-v1. **Author:** Anthropic Claude (claude.ai session `session_01NMeKEismAyeqgdB4sy2NJU`).
**Scientific effect:** NONE. **No priority or novelty claim follows from this memo.** It records what a documented
search did and did not find, so that any lane can extend it and so that successor attribution sections have a
verified starting list. Bibliographic details below are *as indexed by the search pass*; verify against full text
before citing in a manuscript. arXiv identifiers are the stable handles.

## 1. Object searched

The near-diagonal law for finite ordinary superlevel H0 bars of a smooth stationary Gaussian field on a fixed torus:
`ν(ℓ) ~ c ℓ^{−1/3}` (parent Theorem C at existential scope; coefficient (15.2)); its corollaries `N(0,t] ~ (3/2) c
t^{2/3}` and the inverse-lifetime integrability threshold `p < 2/3`; the `d = 3` reference constant
`c_{3,∞} = 2^{−23/6} 3^{−8/3} (29√6 − 36) Γ(1/6) π^{−5/2} ≈ 0.0417759318…` (`coefficients/side24_v1`, main#65); and the
nearest-image periodization correction `P_3(24) e^{−288}` (PR #144). Coverage target: through 29 September 2026.

## 2. Verdict under this protocol

- **Same law proved elsewhere:** none found.
- **Same law contradicted:** none found.
- **Different exponent claimed for the same object** (smooth Gaussian field, finite H0 superlevel bars, `ℓ ↓ 0`):
  none found. The explicit small-bar power laws that do exist are for **rough** processes and a different counting
  convention (number of bars of length `≥ ε`, divergent as `ε → 0`): `N^ε ~ [X]_t/(2ε²)` for continuous
  semimartingales (Perez, arXiv:2012.09459, JACT 2023), and `N^ε ~ C_H ε^{−1/H}` for Brownian, α-stable and
  fractional Brownian motion (Picard, as restated by Perez). These are neighbors, not conflicts: a `C²` path has
  finite variation and is outside their regime. Perez states in print that the smooth-field case is open.
- **Bargmann–Fock-specific persistence results beyond percolation:** none found (located: Rivera–Vanneuville
  critical threshold, arXiv:1711.05012; Gass–Stecconi finiteness of critical-point moments, arXiv:2305.17586).
- **Periodization / nearest-image corrections to local constants on tori:** none found. There is therefore **no
  external benchmark** for the `e^{−L²/2}` term or the coefficient `−620813376/35`; the benchmark is internal and
  multi-path (see §4, item C).

"None found" is a statement about this protocol (§5), not a proof of novelty. Three planned searches were not run
and the paywalled databases were not covered; §4 lists them for the next lane.

## 3. Closest neighbors (condensed; what each does / does not cover)

| arXiv / venue | Work | Covers | Does not cover |
|---|---|---|---|
| 1802.10457; SoCG 2018 / JoCG 2019 | Chazal–Divol, density of expected persistence diagrams | existence and smoothness of EPD densities; Brownian sublevels; notes accumulation near the diagonal | any exponent or constant for smooth fields |
| 2012.09459; JACT 2023 | Perez, PH of a.s. `C⁰` processes | sharp `ε → 0` bar-count asymptotics for semimartingales; exact Brownian expansion | smooth fields (stated open) |
| 2110.10982 | Perez, ζ-functions of superlevel barcodes of α-stable Lévy processes | meromorphic barcode ζ-functions; pole tied to `N^ε` | smooth; `d ≥ 2` |
| 1909.09846; JACT 2025 | Baryshnikov, Brownian motion / chirality | `PH_0` intensity and correlation functions for Brownian motion with drift | smooth; `d ≥ 2` |
| 1908.01619; JCAP 2019 | Feldbrugge–van Engelen–van de Weygaert–Pranav–Vegter | **Rice-formula pair densities `p_i(b,d,r)` for (saddle, extremum) pairs of 2-D Gaussian fields**, pushed to persistence diagrams by a fitting formula | small-`(d−b)` asymptotics, exponent, constant, rigorous elder pairing — **closest structural neighbor; cite and distinguish** |
| 1911.03455; ECP 2020 | Beliaev–Cammarota–Wigman, no repulsion (planar) | leading short-distance term of the critical-point two-point function; index dependence | value gaps; persistence |
| 1704.04943; IMRN 2019 | Beliaev–Cammarota–Wigman, random plane wave | two-point function of critical points | same |
| 1911.02300; SPA 2022 | Azaïs–Delmas, critical points of isotropic fields and GOE | attraction (`d > 2`) / neutrality (`d = 2`) / repulsion (`d = 1`), attributed to adjacent-index pairs | value-gap statistics; pairing |
| 2209.04150; SPA 2023 | Ladgham–Lachièze-Rey, local repulsion of planar critical points | second factorial moment of typed critical points in small balls | values; `d ≥ 3` |
| 2109.08721 | Pranav, topology and geometry of Gaussian fields II | simulated 3-D persistence diagrams / intensity maps | asymptotics |
| 1003.1001; 2010 | Adler–Bobrowski–Borman–Subag–Weinberger | framework and simulations for barcodes of excursion sets | short-bar law |
| J. Topol. Anal. 2012 | Bobrowski–Borman, Euler integration | expected Euler integrals ↔ persistence | near-diagonal density |
| 1808.05655 | Adler et al., planar point-process models of diagrams | qualitative repulsion of diagram points via Slepian models | exponent |
| 1706.06059; 2107.11212 | Curry; "trees to barcodes II" | elder-rule map merge tree → barcode; realization counts | random-field lifetime intensity |
| 2607.23903 (2026) | Kuriki–Matsubara–Iso, critical-point densities in any `d` | one-point height distributions by index | pair gaps |
| 2305.17586; PTRF 2024 | Gass–Stecconi | finite moments of critical-point counts incl. Bargmann–Fock | persistence |
| 2206.06347; JEMS 2026 | Buhovsky–Payette–Polterovich–Polterovich–Shelukhin–Stojisavljević | deterministic bounds on bars longer than `δ` | random `δ → 0` asymptotics |
| 2603.27903 (2026) | random-matrix persistence via Morse theory | bar lengths = eigenvalue spacings; Wigner-surmise bar laws | Gaussian fields |
| 2603.29072 (2026) | Loftus, "How much of persistent homology is topology?" | point-cloud PH of spin configurations (cond-mat) | **unrelated** to Gaussian-field lifetime densities (downgraded from an earlier "worth a read" flag) |

Forward-citation trail from Chazal–Divol (keyword-level, not an exhaustive crawl): the line quantifies near-diagonal
behavior only for Brownian-type processes and treats the near-diagonal region of smooth models as an estimation
nuisance (Maroulas–Mike–Oballe JMLR 2019; Divol–Lacombe 2105.04852; persistence-intensity estimation, PMC12083882;
2407.07326 JACT 2025; 2607.20893; 2607.27126). Nothing in it states a rate for a smooth model.

## 4. Items the other lanes can act on

**A. Attribution additions for successor packages.** The parent's §16 attribution cites Armentano–Azaïs–León,
Curry, and Beliaev–Cammarota–Wigman. A related-work section for the lifetime law should additionally distinguish:
Feldbrugge et al. 2019 (Rice-formula pair densities — closest structural neighbor); Perez 2023 and Picard
(rough-process small-bar laws, different regime); Azaïs–Delmas 2022 and Ladgham–Lachièze-Rey 2023 (spatial
critical-point correlations, no value gaps); Chazal–Divol 2018/19 (EPD density existence). No claim of the
parent's need be changed; this is scope-setting for readers.

**B. A heuristic dimension-independence cross-check reviewers may raise (heuristic; not sourced; not a proof).** If
the adjacent-index critical-pair correlation scales like `r^{2−d}` at small separation — the pattern consistent with
Azaïs–Delmas's `d = 1` repulsion / `d = 2` neutrality / `d > 2` attraction — and the fold gap scales as `r³`, then
`∫ r^{2−d} · r^{d−1} dr ∝ r²` in every dimension, giving `P(gap ≤ t) ∝ t^{2/3}` and density `∝ ℓ^{−1/3}`
independently of `d`. This matches the parent §10 ledger ("the dimension cancels") from the outside, and the factor
12 in the fold gap matches the `24^{1/3}` in (15.2). It rests on two unproved assumptions (short bars come from
fold-type adjacent pairs; the elder rule pairs them) — exactly what Theorem A + CAP supply rigorously. Useful as a
sanity narrative in a discussion section; not evidence.

**C. Periodization coefficient — the benchmark is internal.** No external work computes exponentially small
nearest-image corrections to such constants. The coefficient `P_3(24) = −620813376/35` now has independent
in-project derivations: PR #144 (first principles in the parent's (15.2) conventions, stdlib checker), the July
06B suite (SymPy, Hermite + Haar), the OKComputer 2026-08 first-variation script, and a clean-context re-check on
2026-09-29 — all exact agreement. `|P_3(24)| e^{−288} < 10^{−117}` sits inside side24_v1's reviewed `< 10^{−106}`
band. The remainder enclosure remains PR #144's flagged open item.

**D. Highest-value unexecuted search — for a lane with web access.** The classical 1-D wave literature on the
distribution of *small* crest-to-trough heights of a smooth stationary Gaussian process (Rice 1945; Longuet-Higgins;
Lindgren 1972 "Wave-length and amplitude in Gaussian noise"; Cartwright–Longuet-Higgins) is the natural `d = 1`
neighbor of the max–min small-gap law and was **not** searched. If a `t^{−1/3}` small-height density is already
explicit there, it is prior art for the `d = 1` exponent (not a conflict — the parent is `d ≥ 2` on a torus with
elder pairing) and must be cited. Also unexecuted: Divol–Polonik weight functions near the diagonal; LLN/CLT for
persistent Betti numbers of smooth Gaussian fields 2024–2026; Google-Scholar "cited by" enumeration for
1802.10457, 1911.03455, 1911.02300, 1706.06059, 1908.01619, 2012.09459, Bobrowski–Borman, Adler–Taylor.

**E. Author-side paywalled queries (verbatim, not yet run).**
MathSciNet: `Anywhere=(persistence diagram OR barcode) AND Anywhere=(Gaussian random field OR Gaussian field) AND
Anywhere=(diagonal OR short OR small lifetime)`; `MSC=(55N31 AND 60G60)`; `MSC=(60G60 AND 58K05) AND
Anywhere=(critical value* AND (gap OR pair* OR close))`; `Anywhere="Bargmann-Fock" AND Anywhere=(persistence OR
Betti OR barcode)`; `Anywhere=(crest trough OR wave height) AND Anywhere=(small OR asymptotic) AND MSC=60G15`.
zbMATH Open: `ti:(persistence OR barcode) & ab:(Gaussian field) & ab:(diagonal)`; `cc:55N31 & cc:60G60`;
`ab:"critical values" & ab:"Kac-Rice" & ab:(pair* | two-point)`; `ab:"Bargmann-Fock" & ab:(persistent | Betti |
barcode)`; `ab:(torus | periodic) & ab:"Gaussian field" & ab:(exponentially small | finite-size correction)`.

## 5. Protocol record

- **Executed 2026-09-29** in two passes: (i) a four-query web pass by this session (near-diagonal EPD density
  asymptotics; short-lifetime power law for max/saddle pairs; Bargmann–Fock persistent homology; Kac–Rice small-
  height-gap pair intensity); (ii) an extended web-research run (18 general-search queries plus a delegated
  sub-search of ~17 calls) indexing arXiv (math.PR, math.AT, math-ph, math.DG, cond-mat), Project Euclid, Springer
  (JACT, PTRF), ScienceDirect, JMLR, PMC, ORA, author pages, with keyword forward-citation checks of 1802.10457,
  1911.03455, 1911.02300, 1706.06059, 2012.09459, 1909.09846. Verbatim queries are in `PROTOCOL.json`.
- **Exclusions:** `github.com/d6g8k5htny-coder` and mirrors (self-hits). The project is now search-indexed, so any
  future novelty search must apply this exclusion.
- **Caveats:** keyword search is not a citation crawl; several items were characterized from snippets or
  summaries and must be verified against full text; the §4-B argument is an inference made for this memo.
- **Prior in-repo reconnaissance this memo extends:** parent §16 "Primary-source attribution"; side24_v1 "External
  reconnaissance, 24 September 2026" (DLMF only); OKComputer 2026-08 Part D web pass (five clusters, superseded
  packet).

## 6. Relation to open registers

This memo discharges the *web-level* part of the standing literature item that every register since July 2026 has
carried ("paywalled MathSciNet/zbMATH pass remains author-side"). It does not close that item: §4-D and §4-E remain.
It changes no claim in `claims/LANDING_CLAIMS.json`, no `PROOF_INDEX.md` row, and no status anywhere.
