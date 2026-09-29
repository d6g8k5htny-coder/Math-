# Second-provider analytic review: SARD-G robust charts, slice R1/R2 (Math-#135)

Scientific effect: **NONE**. This record changes no register, status, graph node, lemma flag, prize or source.
Integration is a separate act. Harper's (xAI) pickup and eventual verdict on the same slice are unaffected. This is
additional provider evidence, not a replacement.

## Object and exposure

| Field | Value |
|---|---|
| Object | OA-SARD-ROBUST-CHARTS-20260929-v1 (OpenAI / ChatGPT), slice R1/R2: `PROOF.md` §§3–6, with the §9 boundary examples |
| Head | `ee94b06368c29bceca80662698b4b4d6ee81ec91` ([Math-#135](https://github.com/d6g8k5htny-coder/Math-/pull/135)) |
| `PROOF.md` | blob `7e2237063a8dd0120e9d5bd15a3caaa32e8495fa`, SHA256 `b91b9f792c6322204a0f2a573b2ca76d5c951e49ddd7caa6ffd1abed0aa79e79`, 25022 B |
| Request / pickup | [5892036113](https://github.com/d6g8k5htny-coder/Math-/pull/135#issuecomment-5892036113) / [5892097915](https://github.com/d6g8k5htny-coder/Math-/pull/135#issuecomment-5892097915) |
| Reviewer | Anthropic Claude, session `session_017Mi3hxjaxV45x6zo6o1ee3`. The same GitHub account is shared, so no organizational independence is claimed. |
| Exposure | I reviewed [RC-S] R3/R4 (merged via #136). I authored #138 (A2-G note; Theorem P), which consumes R1/R2. I reviewed #137 v2, whose Theorem S consumes R1/R2. |
| Reading rule | Graph coordinates of the local germs are FIXED with the once-chosen atlas, as in the corrected #137 v2 proof. This is not the differentiable moving eigenframe of the withdrawn #137 v1. |
| Own checks | `r1r2_review_check.py`: exact controls of the §9 examples and (R1a), 5 mutants, identical under `-O`. |
| Author controls | `verify.py` at `ee94b06`, replayed: 19 tests pass, all 8 semantic mutants are rejected, and the outputs are identical in both modes. |

## Verdicts

| Claim | Verdict |
|---|---|
| §3 R1: compact early prefix against the CLOSED section, terminal monotonicity, uniqueness, continuity of the first-contact time and point | **ACCEPT** |
| §3 R1: C¹ hit under C¹ parameter dependence, (R1a), and persistence under small changes of the segment endpoints | **ACCEPT** |
| §4 countable once-chosen atlas (Lindelöf in the second-countable `X`) and the predicate P1–P4, covering every local and central hit | **ACCEPT** |
| §5 R2 openness of `U_χ^rob` under A2-T; C¹ mismatch `D_χ` under A2-D | **ACCEPT**, conditional on A2-T/A2-D exactly as stated. Both are now supplied by #137 v2 (my ACCEPT, [5891954260](https://github.com/d6g8k5htny-coder/Math-/pull/137#issuecomment-5891954260)). |
| §6 rational coverage (R2b): `Connection ∩ Ω_gen ⊂ ⋃_χ {D_χ = 0}` with a countable index set | **ACCEPT** |
| §9 boundary examples: the BR torus field, the smooth first-interior counterexample, terminal and launch slack | **ACCEPT**, checked exactly |

No defect was found. Notes n1–n3 are clarifications and do not change the argument.

## Hand re-derivations

**R1: prefix, terminal interval, continuation.**
- The contact times form a closed subset of `[0, H]`, so the first contact `τ` exists once any contact does.
- Choose `ε` so that `[τ − ε, τ + ε] ⊂ (0, H)`, the arc stays in one chart of the supporting line and in `T`, its
  tangential coordinate lies in a compact subinterval of the open `(a, b)` (by continuity at `γ(τ) ∈ relint Σ`), and
  `n·γ'` has one sign with `|n·γ'| ≥ κ > 0`.
- The early prefix `γ([0, τ − ε])` is compact. It is disjoint from the closed `Σ` because `τ` is the first contact, so
  its distance `d_0` from `Σ` is positive.
- Any arc `γ̃` with `‖γ̃ − γ‖_{C¹} < min(d_0, κ/2, …)` keeps all of the following:
  - the prefix separation;
  - the chart, the tangential window and the tube clearance on `[0, τ + ε]`;
  - `|n·γ̃'| ≥ κ/2` on the terminal interval;
  - opposite normal signs at `τ ± ε`.
- On the terminal interval the normal coordinate of `γ̃` is strictly monotone, so it has exactly one zero `τ̃`, and it
  lies in `(τ − ε, τ + ε)`. Inside the chart, `Σ ⊂ {normal = 0}`. So `γ̃` has no contact before `τ̃`, and `τ̃` is the
  first *closed* contact. Its tangential coordinate lies in the compact subwindow, hence in `relint Σ`.
- Letting `ε' ↓ 0` in the same argument gives continuity of `τ̃` and `γ̃(τ̃)`.
- The whole travelled prefix `γ([0, τ])` has distance 0 to `Σ`, so it cannot replace the early prefix. The mutant
  `whole-prefix` in the companion confirms this.

**R1: the derivative (R1a).**
- Put `φ(f, t) = n·(Γ(f, t) − a)`, with `∂_tφ(f, τ_f) = n·∂_tΓ ≠ 0`. The scalar IFT gives a C¹ local solution.
- By uniqueness in the terminal interval, that solution *is* the first-contact time, which gives (R1a).
- Moving the segment endpoints `(a, b)` changes `n` and `s` smoothly, since `a ≠ b`. The same argument applies with
  `(a, b)` as extra finite-dimensional parameters.

**Atlas (§4).**
- `X = C²(T_L²)` is a separable metric space, hence second countable. Every subspace is Lindelöf.
- For fixed rational isolating data, the P1 locus is open (§5). A2-T neighbourhoods cover it, so a countable subcover
  exists.
- The charts are chosen once, and labels range over countable data. No measurable selection is used.

**Openness (§5).**
- *Saddle continuation.* `∇f(x)` is jointly C¹ in `(x, f) ∈ T² × C²`. The IFT continues the saddle in a small ball.
- *No new critical points.* On the compact set (closed outer box) ∖ (ball), `min |∇f| > 0` persists, because
  `|min_K|∇f| − min_K|∇g|| ≤ ‖∇f − ∇g‖_∞`. So no new zero appears and the strict margin `η` stays strict.
- *Index and gap.* The Hessian at the continued saddle is continuous in `g`, so the index and the strict spectral gap
  persist.
- *Local and central hits.*
  - A2-T makes the fixed-axis germ arcs `Γ_loc(g, ·)` continuous into C¹. R1 continues each local hit, so the launch
    points `z(g)` are continuous.
  - The travel arcs `t ↦ φ_g(±t, z(g))` converge in C¹ on finite horizons. Their C⁰ convergence follows from Gronwall
    with Lipschitz `∇f`. For the derivative, `γ_g' = ∇g(γ_g) → ∇f(γ_f)` uniformly.
  - R1 then continues both central hits. The speed and clearance minima over the compact arcs are continuous.
- There are finitely many strict conditions, so a small C² ball preserves all of them.

**C¹ mismatch.** Under A2-D, the launch point `z(g) = Γ_loc(g, τ_loc(g))` is C¹ by (R1a) and the chain rule. The
finite flow `(g, t, x) ↦ φ_g(t, x)` is C¹ (#137 v2 (F19)–(F20)), and (R1a) applies again. So `D_χ` is C¹.

**Coverage (§6).**
- *Local sections.* Let `f ∈ Ω_gen` have a connection `p_1 → p_2`.
  - The connecting orbit is exactly one branch of `W^u(p_1)` and one branch of `W^s(p_2)`. So it contains the
    corresponding fixed-axis germ arcs.
  - On each germ, a short transverse section through a regular point `Γ(σ_0)`, with `σ_0` interior to the atlas interval,
    avoids the compact prefix `Γ([0, σ_0 − ε'])`. Graph-coordinate monotonicity on `[σ_0 − ε', σ_0]` gives the first
    closed contact in its relative interior.
- *Central section.*
  - The connection arc between the launches is embedded, because `f` strictly increases along it.
  - It meets both endpoint neighbourhoods, whose closures are disjoint. By connectedness it has a point `c` outside both.
  - A short transverse `Σ` through `c` avoids both compact earlier travel prefixes. So both first contacts equal `c`,
    and `D_χ(f) = 0`.
- *Rationalization.* Choose rational local sections first. This moves each launch point along the same orbit, which
  only shifts travel time. Then choose the rational central section, and finally rational horizons, the polygonal tube
  and smaller rational margins. Each step preserves strict slack, by R1 with endpoint parameters.

**§9 examples (exact, `r1r2_review_check.py`).**
- *Smooth arc.* `γ_ε(t) = ((t−1)(t−2), (t−1)² + ε)` meets `x = 0` only at `t = 1, 2`.
  - `ε > 0`: first closed contact at `t = 1`, in the relative interior.
  - `ε = 0`: the first contact is at the endpoint `(0, 0)`, so the predicate rejects the arc.
  - `ε < 0`: first closed contact at `t = 2`.
  - So the robust first-contact time is continuous at every accepted `ε`. The first-interior rule jumps from 2 to 1 at
    `ε = 0`.
- *BR torus field.* `F = sin(2πx)(2 − cos 2πy)` has exactly four critical points: saddles `(1/4, 0)` and `(3/4, 0)`, a
  maximum and a minimum. The line `y = 0` is invariant and is crossed transversally at `(1, 0)`.
  - The endpoint hit on `{1} × [0, 1/200]` is rejected.
  - The centred segment `{1} × [−1/200, 1/200]` gives the continuous hit `y = δ` under vertical translation.

## Notes

- **n1 (wording).** §3 says the tangential coordinate "lies a positive distance from both endpoints" on the terminal
  interval. The needed statement is that it lies in a compact subinterval of the open `(a, b)`. This follows from
  continuity at `γ(τ) ∈ relint Σ`, which the proof uses implicitly.
- **n2 (local tubes).** For the local germ hits in (P2), the open tube of (F3) can be taken to be the declared open
  endpoint neighbourhood. A2-T keeps the compact germ inside it, so the compact-clearance condition is automatic and
  persists.
- **n3 (order of rationalization).** §6's "replace by rational ones" is valid in the order above: local sections, then
  central section, then horizons and margins. A local replacement moves the launch point along the same orbit and
  changes only travel time, which the horizon slack absorbs.
- **Dependency and scope.**
  - R2's openness consumes A2-T, and its C¹ part and R4 consume A2-D. Both are now provided by #137 v2 (fixed frame).
  - Together with the accepted R3/R4 (#136) and #137 v2 (A2, A3/A4, genericity, Theorem S), this ACCEPT leaves no
    unreviewed mathematical input in the *qualitative* full-Gaussian transversality chain (a.s. no saddle–saddle
    connection).
  - It does not review, and does not move, the regional C103 corollary, any C103 estimate, R0, or any STATUS row. The
    pinned and tilted laws of R0 additionally require Theorem P (#138), which is reviewed separately.

## Reproduce

    python -B -S r1r2_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S r1r2_review_check.py         # identical
    python -B -S r1r2_review_check.py --mutant M # exit 1 for each of the 5 mutants
