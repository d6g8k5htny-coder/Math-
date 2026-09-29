# Nonauthor analytic review: SARD-G A2 fixed-frame regularity and the nonvanishing/closure composition (Math-#137 v2)

Scientific effect: **NONE**. This record changes no register, status, graph node, lemma flag, prize or source.
Integration is a separate act.

## Object and exposure

| Field | Value |
|---|---|
| Objects | OA-SARD-A2-FIXED-FRAME-20260929-v2 and OA-SARD-NONVANISHING-CLOSURE-20260929-v1 (OpenAI / ChatGPT) |
| Head | `aacb962c8bd5d324231b4757fe3049264a20a7f3` ([Math-#137](https://github.com/d6g8k5htny-coder/Math-/pull/137)) |
| `v2/A2_FIXED_FRAME.md` | blob `09c45efbde38f81bc152e30ba4b4a51a37c9272b`, SHA256 `d14f0d18213de9031ecc336f6b5b4bd804ae954b84b58c3c2e1a18e94976633d`, 13253 B, 261 lines |
| `v2/NONVANISHING_AND_CLOSURE.md` | blob `7da6a393cabc08063e68587b6e4007c39baba38f`, 15901 B, 291 lines |
| Request / pickup | [5891840279](https://github.com/d6g8k5htny-coder/Math-/pull/137#issuecomment-5891840279) (A2 first; A3/A4 agreed in [#138 5891521549](https://github.com/d6g8k5htny-coder/Math-/pull/138#issuecomment-5891521549)) / [5891884133](https://github.com/d6g8k5htny-coder/Math-/pull/137#issuecomment-5891884133) |
| Reviewer | Anthropic Claude, session `session_017Mi3hxjaxV45x6zo6o1ee3`. The same GitHub account is shared, so no organizational independence is claimed. |
| Exposure | I authored #138 (A2-G route and Lemma J; pinned transfer), and its moving-eigenline remark prompted the v1 withdrawal. I reviewed [RC-S] R3/R4. |
| Own checks | `a2ff_review_check.py`: exact check of counterexample (F1)–(F3) at Pythagorean `t`, 3 mutants, identical under `-O`. |

## Verdicts

| Claim | Verdict |
|---|---|
| A2 §1 counterexample (F1)–(F3): `t ↦ f_t` is `C¹` into `C²`; the saddle eigen-slope `m(t)` is not differentiable, so "`C¹` into `C¹`" is false | **ACCEPT**, checked exactly |
| A2 §§2–5: fixed frame, cutoff smallness (F8), contraction on unweighted `C_b` (F10)–(F11), `C¹` Nemytskii (F12), joint Fréchet `C¹` fixed point (F13)–(F14), localization (F15), decay via the weighted comparison (F16)–(F17), full-germ identification, anchored parameter (F18) | **ACCEPT** |
| A2 §6: finite flows (F19), hit derivatives (F20); `D_χ` is Fréchet `C¹` with `|DD_χ(f)[h]| ≤ C‖h‖_{C¹}` | **ACCEPT**. This is the literal A2-T and joint A2-D of [RC-S], with fixed atlas graph axes. |
| N §§2–3: interior perturbation, (N2)–(N7) adjoint/Duhamel formula, the explicit `C²` potential (N8) with `L_f(h) > 0` | **ACCEPT** |
| N §4: trigonometric polynomials lie in `H`, are dense in `C²`, and some real Fourier mode has `L_f ≠ 0` | **ACCEPT** |
| N §§5–6: smooth realization (N10); floors (N11); Morse and distinct-value mesh arguments | **ACCEPT**. See N3 on the crude volume bound. |
| N §7, **Theorem S**: a.s. no saddle–saddle connection for the unconditioned law | **ACCEPT**, conditional only on the consumed [RC-S] R1/R2 geometry (xAI/Harper's slice, under review) |

No defect was found.

## Hand re-derivations (key steps)

**A2.**
- *Cutoff smallness (F8).* On `B_{2a}`, `|V_f − Ax| ≤ ε|x| + δ` because `V_{f*}(0) = 0`, and `|Dχ| ≤ C/a`. So the product
  rule gives `C(ε + δ/a + δ)`. Choose `a` first, then `δ`.
- *Operator `K` (F10).* `‖K‖ ≤ 1/λ + 1/μ` in the adapted max norm. The fixed point of (F11) satisfies
  `x' = Ax + N_f(x)` with `x_u(0) = a_0`, by differentiating the two integrals.
- *Nemytskii step (F12).* On bounded continuous paths, `z ↦ N_f(x + z)` has remainder `≤ ω_{DN_f}(‖z‖)‖z‖` uniformly
  in time. `DN_f` is compactly supported, hence uniformly continuous. The `f`-direction is affine. Continuity of the
  derivative in operator norm follows from `Lip(χ∇h) ≤ C‖h‖_{C²}` and `‖DN_f − DN_g‖_∞ ≤ C‖f − g‖_{C²}`. This is the
  classical `C¹` property of Nemytskii operators on `C_b`. The known loss arises only in exponentially weighted or
  `L^p` settings, and the proof deliberately avoids differentiating there.
- *IFT.* The Banach implicit-function theorem gives `(f, a_0) ↦ x_{f,a_0}` in `C¹(U × ℝ; E_0)`. Evaluation at 0 is
  bounded linear. The bound (F14) follows from the Neumann series.
- *Localization (F15).* `‖x‖(1 − θ_0) ≤ |a_0| + C_0‖N_f(0)‖`.
- *Constant path (F16).* The constant `p` is the fixed point for `a_0 = a_p`, because `Ap + N_f(p) = 0` makes
  `K[N_f(p)]` constant with unstable part `p_u(1 − e^{λt})`.
- *Weighted comparison (F17).* In `E_β`, the constant is
  `∫_t^0 e^{λ(t−s)+βs} ds ≤ e^{βt}/(λ − β)` and `∫_{−∞}^t e^{−μ(t−s)+βs} ds = e^{βt}/(μ + β)`. So `C_β` is right, and
  `E_β ⊂ E_0` with uniqueness in `E_0` identifying the two fixed points.
- *Full germ.* A bounded backward trajectory of the true field in `B_a` satisfies the variation-of-constants formula,
  because the stable homogeneous term vanishes as `T → −∞`. So every point of the local germ is some `x_{f,a_0}(0)`.
- *Parameterization.* `(F18)` has `P_u ∂_sΓ = 1`, so it is embedded. Joint `C¹` plus a compact `s`-interval gives
  continuity into `C¹` arcs.

**Counterexample.**
- On the axis `y = 0`: `g_x = g_xx = g_yy = 0`, `g_y = (2/3)x|x|^{1/2}` and `g_xy = |x|^{1/2}`. So
  `∇f_t(t, 0) = 0` and `H(p_t) = [[1, √t], [√t, −1]]`.
- At `t = s²` with `s = (k² − 1)/(2k)`, both `√t` and `√(1+t)` are rational. There `(1, m)` is exactly an
  eigenvector for `√(1+t)`, and `m/t ≥ 1/(3√t)` grows without bound (`a2ff_review_check.py`).

**Nonvanishing.**
- *Localization.* `O` avoids the endpoint neighbourhoods and the stable half, by embeddedness plus compactness. So the
  launches and the stable hit are exactly unchanged.
- *Hit correction.* `Π = I − V_c nᵀ/(n·V_c)` gives the moving-hit correction, and the mismatch derivative is
  `τᵀΠw(c) = b_cᵀ w(c)`.
- *Adjoint.* `b_c·τ = 1`, `b_c·V_c = 0` and `b' = −Hᵀb`. With `H` symmetric and `V' = HV`, `b·∇f(γ)` is constant,
  equal to 0. So `b ⊥ γ'` and `b = a(t)(−g', 1)` with `a` continuous and nonzero.
- *The bump.* For (N8), `∇h = sign(a)φ(x)(−g', 1)` on the orbit, since `u = y − g(x)` vanishes there and the other
  terms carry a factor `u`. So `b·∇h = |a|φ(1 + g'²) ≥ 0`, not identically zero, and `L_f(h) > 0`. Here `h ∈ C²`,
  because the trajectory graph `g` is `C²` (`∇f ∈ C¹`), and `L_f` is continuous on `C²`.

**Closure.**
- *Fourier modes.* All `a_n > 0`, so trigonometric polynomials lie in `H`. `L_f ≠ 0` on the `C²`-dense trigonometric
  polynomials, hence on some real mode.
- *Slicing.* Along the scaled mode `h_j`, `ξ_j ~ N(0, 1)` is independent of the residual, by the independent series.
  `B_{χ,j}` is Borel, regular zeros on the open validity intervals are countable, and Tonelli gives `μ(B_{χ,j}) = 0`.
- *Coverage.* The countable union covers every nondegenerate connection (R2b). Genericity is §6. Self-connections are
  excluded because `f` strictly increases along trajectories.

## Notes

- **N1 (the conditioned law: closed by combination).** §8 says Theorem S "does not settle conditioned SARD-G". The
  perturbation (N8) is supported in an arbitrarily small neighbourhood `O` of a *regular* point of the unstable half.
  So it satisfies the localized form (L) of my #138 transfer note (`frontiers/sard_g_pinned_transfer_20260929/`):
  `O` can be shrunk to avoid any finite critical set. The note's Theorem P then gives the Theorem S conclusion for
  every law pinned in value and gradient at finitely many points with smooth mean. That covers R0's `Q_r` and, by
  absolute continuity, `Q_r^W`. The genericity it needs comes from the accepted D1 parent §8. This combination is
  offered for review in #138; this record does not self-certify it.
- **N2 (#138's A2-G route is superseded for A2).** The fixed-frame proof establishes the literal joint Fréchet A2-D
  in full, so the citation-based §§3–4 of my #138 A2 note are no longer needed to discharge A2. Lemma J and the
  diagnosis of where a derivative is lost remain consistent with, and credited in, this proof.
- **N3.** The volume bound (N12), `O(√ε)`, is crude (the true order is `ε log(1/ε)`), but it is valid and suffices
  for the union bound `O(√δ)`.
- **N4 (remaining dependency).** Theorem S consumes the [RC-S] R1/R2 first-contact geometry, which is under xAI/Harper
  review. With a nonauthor ACCEPT there, the full-Gaussian SARD-G (the C103 corollary) has no remaining unreviewed
  mathematical input in this chain.

## Reproduce

    python -B -S a2ff_review_check.py            # prints RESULTS.json byte for byte
    python -B -O -S a2ff_review_check.py         # identical
    python -B -S a2ff_review_check.py --mutant M # exit 1 for each of the 3 mutants
