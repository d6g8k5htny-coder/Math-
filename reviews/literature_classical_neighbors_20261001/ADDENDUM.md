# Literature addendum — the classical 1-D neighbours read in full; forward citations — 2026-10-01

**Object:** CL-LIT-CLASSICAL-NEIGHBORS-20261001-v1.1 (v1 → v1.1 after Codex review of v1, comments 4151188790–4151188834: hypotheses for the `d = 1` law; the `[P]` source identified; the machine-readable verdict qualified; the provenance made exact; the NumPy simulation replaced by a deterministic standard-library Rice check, `d1_rice_check.py`). **Author:** Anthropic Claude (claude.ai session
`session_01NMeKEismAyeqgdB4sy2NJU`; the searches and full-text reads were run by a clean-context Claude subagent of that
session, the d = 1 computation and its deterministic check by the session). **Scientific effect:** NONE. **No priority or novelty claim
follows from this memo.** It extends CL-LIT-RECON-LIFETIME-20260929-v1.1
(`reviews/literature_lifetime_law_recon_20260929/RECONNAISSANCE.md`, blob `003b9879`, Math- #147), executing the items its
§4-D left open: full-text reads of Rice 1944/1945 and Cartwright–Longuet-Higgins 1956, a partial read of
Longuet-Higgins 1957, the later 1-D wave-characteristic literature, and a forward-citation enumeration. Quotations are
as extracted (OCR or PDF text); verify against the printed pages before citing.

## 1. Verdict under this protocol

- **Same law stated elsewhere:** not found. No source located, in any year or field, states `f(h) ~ C h^{−1/3}` or
  `F(h) ~ C h^{2/3}` for the gap between a maximum and the adjacent minimum of a smooth stationary Gaussian process
  (`d = 1`), or for the gap between a maximum and a neighbouring saddle (`d ≥ 2`).
- **Next-order (cusp-scale, `ℓ^{1/4}`) correction:** not found anywhere.
- **Closest source:** Lindgren (2019), which prints the exact joint law of (maximum, following minimum, half-period) of a
  stationary Gaussian process (eq. (18)) and evaluates it numerically. The small-amplitude law is implicit in that
  formula (a small-period expansion), but the paper does not carry the expansion out (§3).
- The verdict of the 2026-09-29 memo stands and is now stronger for `d = 1`: Lindgren 1972 and Lindgren 2019 are prior art
  for the **object** (the maximum-to-following-minimum amplitude), not, on the evidence read, for the **exponent**.

"Not found" is a statement about this protocol (§5), not a proof of novelty.

## 2. Sources read in full (`d = 1`)

| Source | Access | Relevant content | Prior art for the exponent? |
|---|---|---|---|
| S. O. Rice, *Mathematical analysis of random noise*, Bell Syst. Tech. J. 23(3) 282–332 (1944), doi:10.1002/j.1538-7305.1944.tb00874.x; 24(1) 46–156 (1945), doi:10.1002/j.1538-7305.1945.tb00453.x | full (archive.org OCR, items `bstj23-3-282`, `bstj24-1-46`) | §3.6 (pp. 71–75) gives only the height density of a single maximum: "the probability that a maximum selected at random from the universe of maxima will lie in I, I+dI" (3.6-9). The string "minim" does not occur in either OCR text. §3.4 (pp. 57–58): "The problem of determining the distribution function for the distance between two successive zeros seems to be quite difficult and apparently nobody has as yet given a satisfactory solution" — small-spacing results there concern zeros and separations, not heights. | no |
| D. E. Cartwright, M. S. Longuet-Higgins, *The statistical distribution of the maxima of a random function*, Proc. R. Soc. Lond. A 237, 212–232 (1956), doi:10.1098/rspa.1956.0173 | full (IFREMER copy) | §8 "Crest-to-trough wave heights" (pp. 229–231): "The statistical distribution of an is more difficult to obtain theoretically than that of Xn for general values of ε." "From figure 8 it will be seen that the records with the two broad spectra deviate especially from the Rayleigh distribution for low values of the wave amplitude, having relatively more waves in that range." §9: "The theoretical distribution of crest-to-trough heights is known only for a narrow spectrum (ε = 0), when it is a Rayleigh distribution." The excess of small waves is reported from data, with no exponent. | no |
| G. Lindgren, *Gaussian integrals and Rice series in crossing distributions — to compute the distribution of maxima and other features of Gaussian processes*, Statist. Sci. 34(1) 100–128 (2019), doi:10.1214/18-STS662 | full (Project Euclid PDF) | Eq. (18): "f_T(t) × P(X^max ≤ x1, X^min ≤ x2 \| T = t) = (1/ν^max) E[1(t,x1,x2) X''(0)^− X''(t)^+ \| X'(0) = X'(t) = 0] f_{X'(0),X'(t)}(0,0)", with "1(t,x1,x2) = 1(X'(s) < 0, 0 < s < t, and X(0) ≤ x1 and X(t) ≤ x2)"; "Integrating over x1 − x2 = h one then obtains the joint amplitude, X^max − X^min = H, and period, T, distribution." Evaluated numerically (WAFO) only. | not stated (implicit, §3) |
| I. Rychlik, P. Johannesson, M. R. Leadbetter, *Modelling and statistical analysis of ocean-wave data using transformed Gaussian processes*, Marine Structures 10, 13–47 (1997), doi:10.1016/S0951-8339(96)00017-2 | full | "This departure is due to the joint density of T, H having a peak for short waves with small amplitudes (see Fig. 13b) and hence, the numerical integration can have low accuracy for small amplitudes." Qualitative only. | no |
| G. Lindgren, I. Rychlik, DTIC Technical Report 282 (1990; Int. Stat. Rev. 59, 1991) | read through text extraction, possibly truncated | "higher order approximations are smoother, in particular at the left, smaller end of the distribution." No power law. | no, as far as read |

**Not accessible / abstracts only (not determinable):** G. Lindgren, I. Rychlik, Ocean Eng. 9(5) 411–432 (1982),
doi:10.1016/0029-8018(82)90034-8 (abstract: "…no closed form expressions are known at present"); M. S. Longuet-Higgins,
Proc. R. Soc. Lond. A 389, 241–258 (1983), doi:10.1098/rspa.1983.0107 (a narrow-band joint density, per Lindgren 2019
§5.1); I. Rychlik, Adv. Appl. Prob. 19, 396–430 (1987), doi:10.2307/1427425; I. Rychlik, SPA 34, 313–339 (1990),
doi:10.1016/0304-4149(90)90021-J; G. Lindgren, K. B. Broberg, Extremes 7, 69–89 (2004), doi:10.1007/s10687-004-4729-3;
L. D. Lutes, Prob. Eng. Mech. 23, 254–266 (2008), doi:10.1016/j.probengmech.2007.12.008. None of these abstracts mentions
small amplitudes. OpenCitations lists 37, 65, 23, 10 and 3 citing works for Lindgren 1972, Lindgren–Rychlik 1982,
Rychlik 1987, Lindgren–Broberg 2004 and Lutes 2008; no title suggests a small-amplitude asymptotic.

## 3. The `d = 1` analogue, made explicit (a remark for the attribution wording; not a theorem of this repository)

**Source.** The contact computation of the parent `[P]` = `imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md`
(blob `dfed3b8d`), (15.2), uses `d ≥ 2` only through the transverse block. That block is empty in `d = 1` (cone moment
`D_0 = 1`).

**Hypotheses.** A stationary Gaussian process with `C⁴` paths whose jets `(X', X'', X''')` at a point are jointly
nondegenerate. In particular `τ² := λ₆ − λ₄²/λ₂ > 0`; this excludes spectral measures carried by at most two points such as
`A cos t + B sin t`, for which `H = 2√(A² + B²)` has no `h^{−1/3}` law. Carried out under these hypotheses, the computation
gives, for the crest-to-trough amplitude `H` (a maximum to the following minimum) under the Palm distribution of maxima,

    f_H(h) ~ C h^{−1/3},     P(H ≤ h) ~ (3/2) C h^{2/3}     (h ↓ 0),
    C = Γ(7/6) · 72^{−1/6} (2π)^{−1/2} · (λ₆ − λ₄²/λ₂)^{2/3} / λ₄,

i.e. `C = 0.199718…` for the covariance `e^{−t²/2}` (`λ₂ = 1`, `λ₄ = 3`, `λ₆ = 15`).

**Derivation.** In the separation variable,
`c_d = Γ(7/6)72^{−1/6}(2π)^{−1/2}∫_{S^{d−1}} p_G(0)p_{V_u}(0)τ_u^{4/3}D_u dσ(u)`, with `G = f'`, `V_u = f''` and
`τ² = Var(f''' | f' = 0)`. Here `S⁰` has two points, one for each orientation, and "following minimum" keeps one of them.
Dividing by the intensity of maxima, `(2π)^{−1}(λ₄/λ₂)^{1/2}`, gives `C`. The formula is invariant under time rescaling
and scales as `σ^{−2/3}` under `f ↦ σf`. In `d = 1` a fold pair sits on a monotone slope, so the neighbour beyond the
minimum is higher than the small maximum. To leading order the pair is an elder pair, and the same constant should
govern the elder (persistence) lifetimes in `d = 1` (not proved here).

**Deterministic check (standard library; `d1_rice_check.py`, output `D1_RICE.json`).** For `e^{−t²/2}`, the two-point
Rice density of (maximum at `0`, minimum at `t`) with `X(0) − X(t) = h` is evaluated exactly in distribution:
- no sampling;
- rescaled rows, Decimal arithmetic for the covariance algebra;
- one-dimensional quadratures.

It is then integrated over separations `t ≤ 1.5`. `h^{1/3}f(h)/(Cν_max)` equals `1.0048, 0.9971, 0.9984, 0.99941, 0.99982,
0.999951, 0.999989, 0.9999983, 1.0000003` at `h = 10⁻², …, 10⁻¹⁰`. The deviation shrinks by a factor of about `3.3–4.4`
per decade, i.e. roughly as `h^{0.57}`, consistent with a relative correction of order `h^{7/12}` (the cusp scale).
This checks the constant's arithmetic through the exact two-point Rice formula. It is not an independent proof of the
law, since intermediate extrema are not excluded, which affects only the regular part.

So the exponent is implicit in exact classical formulas (Lindgren 2019, (18)), but on the evidence read it is not stated
in print. **Suggested manuscript wording:** *"In dimension one the same contact computation gives the small-amplitude
law of crest-to-trough heights, `f_H(h) ~ Ch^{−1/3}` with an explicit `C`; the exact joint law of adjacent extremes
(Lindgren 2019, (18)) contains it implicitly, but we have not found it stated."*

## 4. `d ≥ 2` and next-order terms

- M. S. Longuet-Higgins, *The statistical analysis of a random, moving surface*, Phil. Trans. R. Soc. Lond. A 249, 321–387
  (1957), doi:10.1098/rsta.1957.0002 — **partial** (the extraction stopped inside §2.4, about p. 348; §2.9 "The heights of
  maxima" was not read). §2.4: "On a statistically uniform surface the average density of maxima per unit area plus the
  average density of minima is equal to the average density of saddle-points". Nothing about height differences between
  neighbouring critical points in the part read; the abstract's item (8) concerns narrow spectra ("when the spectrum is
  narrow, the probability distribution of the heights of maxima and minima…"). Not determinable for §2.9.
- Cadiou et al., arXiv:2003.04413 — "critical events" (pairs whose persistence vanishes as the smoothing scale changes):
  a different object (a one-parameter family, not gaps in a fixed field). Sousbie, arXiv:1009.4015, and Pranav,
  arXiv:2109.08721 — numerical persistence statistics. Ladgham–Lachièze-Rey arXiv:2209.04150, Beliaev–Cammarota–Wigman,
  Azaïs–Delmas — short-distance correlations of critical-point **positions**, no height-gap law (abstracts).
- **Cusp-scale correction:** not found. "Cusp" occurs only for unrelated objects (cusp caustics, arXiv:2405.20475; cusps
  of Gaussian maps to the plane, arXiv:2202.08242). Feng–Götze–Yao, arXiv:2607.19660 (smallest gaps between zeros), never
  mentions critical points or heights.

## 5. Forward citations (cited-by enumeration of the 2026-09-29 neighbours)

Semantic Scholar and OpenAlex were rate-limited (HTTP 429 throughout, 01:34–01:52 UTC); zbMATH `ci:` queries returned no
citing documents. OpenCitations v2 (DOI-indexed, so it misses most arXiv-only papers) and INSPIRE (for 1908.01619) gave:
1802.10457 — 17; 1911.03455 — 5; 1911.02300 — 7; 1908.01619 — 52 (OpenCitations) / 50 (INSPIRE); 2012.09459 — 2;
1706.06059 — 34 citing records (some preprint/journal duplicates). No title concerns short-bar or near-diagonal
asymptotics for smooth Gaussian fields. Nearest: Baryshnikov, arXiv:1909.09846 (JACT 2025; Brownian motion with drift,
not smooth: "near the diagonal the density explodes as 1/m(d−b)^3"); arXiv:2407.07326 (LLN/CLT for discrete-time
sequences); arXiv:2601.06009 (`ε^{−2}` excursion law for semimartingales); arXiv:2507.06255 (Betti-number and
Euler-characteristic statistics); arXiv:2009.04819 (numerical).

## 6. Status of the 2026-09-29 memo's open items

- §4-D: Rice and Cartwright–Longuet-Higgins **done** (no); Longuet-Higgins 1957 **partial** (§2.9 unread); Lindgren–Rychlik
  1982 and Longuet-Higgins 1983 **inaccessible here** (paywalled; author-side). Divol–Polonik and the 2024–2026 LLN/CLT
  line: only 2407.07326 surfaced, no near-diagonal rate.
- Cited-by: **executed through OpenCitations/INSPIRE** (§5); a Google-Scholar-level enumeration remains author-side.
- §4-E (MathSciNet/zbMATH paywalled queries): **not run** (zbMATH Open `ci:` only, empty). Unchanged.

## 7. Protocol

Queries (WebSearch, verbatim) and Consensus searches are listed in `PROTOCOL.json`, with the APIs used and the
exclusions (`github.com/d6g8k5htny-coder` and mirrors: the project is search-indexed). Caveats: keyword search is not a
citation crawl; quotations are from OCR/PDF text extraction; the `d = 1` constant of §3 is a computation recorded for
the attribution wording, not a reviewed theorem, checked deterministically by `d1_rice_check.py`.
