# The remainder of Theorem R: `B_{d,L}` for candidates, `0` for elder pairs (CL-D2-REMAINDER-VANISHING-20260930-v1)

Author-side proof candidate, Anthropic Claude, 30 September 2026. Scientific effect NONE. Nonauthor review required.
Relative to merged, reviewed sources only ([R] Theorem R, [Z] Theorem Z, [C7-K], the reconciled [P] chain);
Math- #187/#188 are cited only, for a conditional rate remark.

**Statement (Theorem R+).** For the periodized Gaussian field on the fixed torus (every `d ≥ 2`, `L > 0`), as
`ℓ ↓ 0`,

    ν_cand(ℓ) = cℓ^{−1/3} + B_{d,L} + o(1),        ν_eld(ℓ) = cℓ^{−1/3} + o(1),

where `B_{d,L} = ∫∫Ψ_0` is the equal-height kernel mass of Theorem Z. Theorem R's bounded remainder is thus
identified: its constant term is the rejected mass `B_{d,L}` for candidate pairs and `0` for elder pairs, so
`ν_eld = cℓ^{−1/3}(1 + o(ℓ^{1/3}))`. Also `ν_cand^{near,r_0} − cℓ^{−1/3} → ∫_{|y|<r_0}∫Ψ_0`, which is `≤ Cr_0`.

**Mechanism.** *Even contact expansion* (Lemma E): the first-order contact error `r(k + r)H` of [R] (R11) is really
`r²H`. The endpoint curvatures are `α_M = −6k + (r/12)f_4 + …`, `α_S = +6k + (r/12)f_4 + …` with the **same**
first-order term, the transverse and mixed blocks likewise, so `det K_M = −6k det A_0 + rY + …`,
`det K_S = +6k det A_0 + rY + …` and the product has no `r`-term (the reflection symmetry of the pinned family);
on the inertia-flip layers each typed determinant is `O(r)` and their product `O(r²)`. In the separation variable
this gives an `ℓ`-uniform integrable majorant for the candidate density's deviation from the leading law — the
near-diagonal domination that [Z] §5 records as unavailable for candidates — so dominated convergence identifies
the deviation's limit as `∫∫Ψ_0 = B_{d,L}`; subtracting Theorem Z (Z4) (`ρ_rej → B_{d,L}`) leaves `o(1)` for elder
pairs.

Files: `PROOF.md`; `even_contact_check.py` (stdlib exact controls; `RESULTS.json` its output, `-O` identical;
mutants `M1`–`M3` exit 1, unknown label exit 2: the quintic pin expansions with their coefficients, the exact
reflection identity `det H_M(−r) = det H_S(r)` and the resulting parity on a general pinned quintic in two
variables, the block/Haynsworth identities with the Step 4 case split, the ledger, the layer algebra);
`SOURCES.json` (exact identities of every source; #186/#187/#188 cited as unmerged). A clean-context referee
agent read a first version before landing; its findings (a false layer inequality on the indefinite part of the
flip layer, repaired by the three-case split; the theorem's independence from #188, which the first version had
assumed; the direct identification of the constant `B_{d,L}` through Theorem Z; Proposition L being [C7-K] §4's
own proof; the norms `T` controls; controls that were symmetry-forced or tautological) were applied.

Review slices (§6): A Lemma E; B the separation-variable limit argument and the use of Theorem Z; C scope and
remarks.
