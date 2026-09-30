# C6 cluster law (CL-C6-CLUSTER-LAW-20260929-v1.2)

Author-side proof candidate by Anthropic Claude. **Nonauthor analytic review required.** Scientific effect: NONE.
**Stacked candidate:** consumes only merged sources at exact bytes (`SOURCE_MAP.json`): [LP], [DL], [C6], [RM], [RC],
[EDL], [LM], and, for the consumer corollary only, [RCL] (Math-#153).

## What it proves, if the arguments and the inputs hold

For the exact pinned model of `imports/lifetime_parent_20260925` with compact marks, the original endpoint weight and
the full normalizer, in every fixed `d >= 2`, with `N` the window critical-point count other than the pins:

| Result | Statement | Answers |
|---|---|---|
| Theorem N | `r^(-3) Q_r^W{N = n} -> nu(n)` with `nu(1), nu(2) > 0` explicit and `nu(n) = 0` for `n >= 3` | the "unknown conditional cluster law" of Math-#153 |
| Corollary Lambda | `r^(-3) E[(N)_q] -> Lambda_q`: `Lambda_1 = nu(1) + 2nu(2)`, `Lambda_2 = 2nu(2)`, `Lambda_q = 0` for `q >= 3` | sharpens [C6] Theorem Q to asymptotics; Palm excess converges |
| Corollary S | the limit `nu` of Math-#153's `nu_r` exists (no subsequence), `F_oo = (nu(1) delta_1 + nu(2) delta_2)/(nu(1)+nu(2))`, `CP(t nu)` explicit | uniqueness and identification of the compound-Poisson limits |
| Corollary X | the scaled positions and heights of the extra window critical points converge in law to the critical points of a planar cubic | the "positional law of the pairs" non-claim of [C6] §9 |

`nu(2) = nu_near(2)`, `nu(1) = nu_near(1) + k integral_X Lambda`, where `nu_near(n)` is a four-dimensional Gaussian
integral over the scaled soft transverse curvature `s` and the three planar cubic jets `(a_3, beta, c_3)` of the
midpoint (PROOF.md (1.3)), with the pin weight `w_0 = [-6k(s - beta/2) - a_3^2/4]_+ [a_3^2/4 - 6k(s + beta/2)]_+`, and
`Lambda` is the reviewed remote contact kernel of [RM].

**Planar case.** At `d = 2` the chart is the identity and every consumed regional bound is a reviewed planar statement,
so Theorem N at `d = 2` is conditional on this note's own steps only (PROOF.md §1.4).

## Mechanism (PROOF.md §§3–6)

1. Near the pins, one transverse curvature of order `r` (one Lebesgue direction: the factor `r`) puts the field into the
   normal form of a planar cubic `F_0` on the soft plane, with the two pins among its critical points ([EDL] (A17),
   [LM] (L6)); the stable directions are slaved (Lemma 3.1). A planar cubic has at most four critical points, so at most
   two extra ones (Lemma 3.2: the resultant is `(X^2 - 1/4) Q_2(X)` with `Q_2` quadratic, an exact identity). In the
   sheared form `C(u) + (s + Bu) Z^2/2 + (D/3) Z^3` (Lemma 3.6, exact identity) every extra window critical point is a
   nondegenerate saddle and the typed window forces `-s <= 2|B| + (32 k D^2)^(1/3)`, the integrable majorant of §6.2.
2. The pin weight on such a configuration is `r^4 (det D)^2 w_0` and the normalizer is `r^2 z_0` (Lemmas 3.4–3.5),
   giving the exponent `1 + 4 - 2 = 3`.
3. The scaled representation (4.2) in the spectral chart of §3.2, a `K_4 <= kappa` split (Lemma 4.2: the large-`K_4`
   part is `O(kappa^(-p/2)) r^3` by marked Kac–Rice) and dominated convergence on `{K_4 <= kappa}` (Lemma 4.3, with the
   full-space exclusion Lemma 3.3 for large soft curvature) give the near limits for every scaled radius `A`; the counts
   converge by `C^1` stability (Lemma 4.1).
4. The shells contribute `C r^3 (A^(-2) + rho^2)` ([DL] Theorem I_d), the remote region `k r^3 integral Lambda + O(r^4)`
   ([RC] Corollary E), a second remote point `O(r^5)` ([RC] Corollary D), and a near point together with a remote one
   `O(r^(9/2))` (Lemma 5.2: Cauchy–Schwarz inside [C6]'s marked Kac–Rice formula with a witness-conditioned remote first
   moment, Lemma 5.1). The sandwich of §6.1 then closes with `A -> oo`, `rho -> 0`.

## Run

    python -B -S cluster_law_check.py                      # rc 0, output = RESULTS.json
    python -B -O -S cluster_law_check.py                   # rc 0, byte-identical
    python -B -S cluster_law_check.py --mutant NAME        # rc 1 for each of the nine names in the docstring

Eight exact groups (`NF RS EX BD EU SH TW LG`): the pin conditions and pin Hessians of the cubic as polynomial identities; the
resultant factorization and the explicit `Q_2`; six exact configurations with `0`, `1`, `2` extra critical points in the
window and their pin weights (including the [LM] cubic with weight `45 k^4`); the block-determinant expansion in `r`
for `d = 3, 4`; the Euler identity behind the large-curvature exclusion; the shear identity (3.12); the saddle sign,
height identity and `s`-range of Lemma 3.6 on an exact rational family of critical points; the exponent ledgers (soft slice, cross term,
shell error, Hadamard row factors of (3.10), the large-`K_4` tail and the uniform-integrability tail). They verify identities,
exact configurations and exponent bookkeeping only.

## Review requests (exact interfaces)

1. Lemma 3.1: the normal form in the rotated chart and the stable slaving, in particular the bound on `|W|` for critical
   points in the physical ball and the `C^2` remainder (3.6) with its `(1 + |D^(-1)|)` growth (used only pointwise).
2. Lemma 3.3: the exclusion of near critical points for large scaled soft curvature, proved in the full transverse
   space on `{K_4 <= kappa}`; the threshold (3.8) and the pin nondegeneracy radius.
3. Lemma 4.1: the coupling of the conditional laws and the `C^1` stability count; the null sets (`E_k`, the circle, the
   atoms of `K_4`).
4. Lemma 4.2: the large-`K_4` tail through [C6] Lemma 5.1 and the regime ledgers; Lemma 4.3: the dominating function
   built from (3.8) and the Hadamard bound (3.10), with no inverse of `D`; the Weyl density (3.3).
5. Lemma 5.1: the uniform conditional covariance floor (5.3a) of the remote jets given the pins and a near witness,
   proved by whitening the joint frame against the midpoint five-jet ((5.3b), (5.3c)) with the [LP] §2 distinct-site
   floor and the [DL] frame remainders; the full normalizer `Z_r^(-1)` once in each marked display (Lemmas 4.2, 5.2); Lemma 5.2: the Cauchy–Schwarz insertion and the absorption of `(1 + beta)^(d/2)`.
6. Lemma 3.6: the sheared cubic, the saddle sign `-3k(B + 4su) < 0` and the range (3.13); the choice of `kappa` by
   Fubini on the limit law (after Lemma 4.1); §6.1: the sandwich and the order of the limits `r -> 0`, `A -> oo`, `rho -> 0`; §6.2 positivity and the explicit majorant; §6.3 uniform
   integrability from [C6] Theorem Q.
7. That every step cited from the seven consumed proof sources is used at its stated scope and exact bytes.

## What this does not do

No rate, no numerical value of `nu(1)`, `nu(2)`, `Lambda_q`, no uniformity in `k`, `L` or `d`, no elder-selection
statement about the extra points, no joint law of clusters of distinct pin pairs, no all-height near count, no register
or catalog change. The catalog entry C6 and the GRAPH node `math.rn-region.witness-collision` are not moved by this
packet.

## Provenance

Consumed sources and their exact identities on `main` `7a1cb09`: `SOURCE_MAP.json`. This packet's inventory:
`SOURCE_FILES.json`. External check: `RECONNAISSANCE.md`. Same GitHub account as every lane; zero
organizational-independence credit; [C6], [DL] and this note are Claude-authored; [EDL], [LM], [RM], [RC], [RCL] and [LP]
are OpenAI-authored.
