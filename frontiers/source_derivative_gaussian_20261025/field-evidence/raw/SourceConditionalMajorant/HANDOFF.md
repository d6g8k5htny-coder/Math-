# Actual conditional Fourier majorants: completed local proof

Sole new production source in the new worktree:
`/workspace/Math-wholefield-20261025/frontiers/source_derivative_gaussian_20261025/SourceConditionalMajorant.lean`.

Source SHA256:
`07ae7796e461a2ee59a757b37a3e64f7ed31c76d26a3b40825f23170fcb4e691`.

Frozen contract read in full: `9c7984e`, `SOURCE_CONDITIONAL_MAJORANT.md`.
The old `/workspace/Math-` delivery, 14 baseline modules and 23 bound inputs
were preserved and their completed verification reused.

## Proved results

Namespace `I4SourceConditionalMajorant` has 20 public theorems, listed exactly
in `targets.json` and `qualification_receipt.json`.

- `sampleMajorant` is the literal sum of nonnegative weights times absolute
  actual noise coefficients. `sourceDerivativeMajorant L k` uses the actual
  `orderModeBound k 2 L` weights.
- Every-sample confluent-weighted summability is proved from the actual
  all-order smooth carrier. Actual pins are bounded by its Gamma_A.
- `posterior_sampleMajorant_le` proves the literal
  `Gamma_w(post d ω) ≤ Gamma_w(ω)+36 K B_w(D+Gamma_A(ω))`, carrying the general
  weight's sample/product summability explicitly and deriving posterior
  weighted summability. No real-tsum equality substitutes for convergence.
- `sourceInverse_prescribed_uniform_bounds` derives K,D and `0<δ≤1` from the
  actual inverse/prescribed-pin limits. The chosen interval also intersects
  actual current pin-covariance invertibility.
- `smoothSourceField_global_derivative_bound hL k ω x` proves the actual global
  operatornorm bound `norm(D^k field(ω)(x)) ≤ Gamma_k(ω)` at every point.
- `sourceDerivativeMajorant_uniform_domination hL b k` derives a fixed positive
  summable weight w and nonnegative drift a with
  `Gamma_k(posterior d_r ω) ≤ a+Gamma_w(ω)` uniformly for small positive r.
- `sourceConditionalDerivative_moments hL b k` proves every natural moment
  under the actual specified whole-carrier kernel, on one radius interval
  uniform in the moment order, with no moment premise.
- `sourceConditionalDerivative_cutoff_tail hL b k n` proves the measurable
  `{r⁻¹ < Gamma_k}` cutoff has bound `M*r^n` for each natural requested order.
- `sourceConditionalDerivative_gaussian_upper_tail hL b k` proves constants
  `a≥0,s>0,0<δ≤1` and the genuine bound
  `Q_r{a+R≤Gamma_k} ≤ 2 exp(-R²/(2s²))` for `R≥0` and small positive r.
  This uses the separately proved folded-Gaussian exponential estimate via
  Jensen/Fatou; it is not inferred from bare all-fixed-moment boundedness.
- `sourceWeightedDerivative_cutoff_tail hL b k n` proves probability status
  and the same requested polynomial cutoff rate for the actual constructed
  whole-carrier endpoint-weighted law. It uses conditional order 2n and the
  proved square-root transfer to obtain weighted order n.

The final source-model inputs are only fixed `L≠0`, arbitrary fixed b and the
natural indices. Current inverse bounds, pin bounds, Gaussian noise laws,
posterior realization, moments and tails are derived, not desired conclusions
added as hypotheses. The posterior drift remains present.

The measurable Gamma event certifies a global derivative bound. No
measurability of an arbitrary uncountable derivative supremum is assumed.
Natural orders give every fixed polynomial decay rate by choosing a larger
integer when needed; the directly exported polynomial theorems use `n : Nat`.

## Verification evidence

`qualification_receipt.json` records exact commands, working directory, exits,
raw-log paths and hashes, unchanged source SHA, targets and axiom reports.

- Final new-module compile with `-DwarningAsError=true`: exit 0, empty output,
  `.olean` generated. That completed compile was reused for qualification.
- Named `leanchecker SourceConditionalMajorant`: run once, exit 0, empty output.
- All 20 public transitive axiom reports: only `propext`, `Classical.choice`,
  `Quot.sound`.
- Actual final elaborated types: exit 0.
- Positive controls with warnings as errors: exit 0. A weight two on a negative
  coefficient minus three gives Gamma six. A separate actual-model proof
  derives a small-radius posterior of zero noise with Gamma_A at least two,
  from the literal prescribed cubic pin, demonstrating that drift cannot be
  silently discarded.
- False omitted-absolute-value and false weight-scaling controls: each exit 1
  at an intended unsolved `False` proof goal.

The positive-control helper is scratch-only. Its first attempt was rejected
because emitting an olean for an external scratch file requires an explicit
Lean root. The next attempt exposed only hidden set-membership syntax in the
new drift-control proof; adding `change 0<δ at hδ` corrected it. These records
remain as `positive-attempt1/2`; only that affected control was rechecked.
Completed kernel, axiom and source checks were not repeated.

## Lineage and remaining original-goal work

Actual OpenAI/Codex `/root/dm2_landed_composition` is the sole implementer.
Earlier read-only Lp API research for the proposal came from actual OpenAI/Codex
`/root/dm2_landed_composition/peano_strategy`; the later attempted implementation
helper was not created because the thread limit was reached. Qualified
GaussianWeightedMajorants, SourceSmoothConditionalKernel and SourceSmoothPalm
results are consumed as dependencies with their own actual owner records.
None of this is an independent scientific review.

The original research goal remains active. Remaining joins include literal
historical nine-jet normalization/event identification, any specifically
requested chart-supremum measurable representation, geometric Kac-Rice/Palm
identification of the constructed weighted carrier law, and later geometric
or parent theorems. Historical LM007/LM009 scientific reviews do not transfer
to this new source. Scientific effect NONE.

No commits, external posts, Lakefile changes or completed-source edits were
made. Root owns integration and scientific-review routing. Per
`/workspace/AGENTS.md`, reuse the completed applicable verification here; a
handoff or pending process requirement alone does not justify repeating it.
