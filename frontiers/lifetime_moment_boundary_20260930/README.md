# Which lifetime moments exist?

The answer depends on whether the maximum eventually dies. For finite deaths, the existing pinned Gaussian estimates give convergence of **every fixed positive lifetime moment**. Including the essential maximum makes every positive moment infinite, even though its probability becomes smaller than every power of the pin separation.

Let `X_r=(b-d_f(M))/(k r³)` be the actual elder lifetime divided by the prescribed pin gap, under the original weighted law `Q_r^W`. If `F_r` is pairing failure, the existing marked law has mass `a r³+o(r³)` and limiting fraction `λ∈(0,1)`. Write `m_q=∫λ^q dμ_fail`.

| Quantity, for fixed `q>0` | Result |
| --- | --- |
| Failure moment, restricted to finite deaths | `r^-3 E[X_r^q; F_r, finite] → m_q` |
| Moment conditional on failure and finite death | `E[X_r^q | F_r, finite] → m_q/a` |
| Finite lifetime tail above the nominal gap | `r^-3 E[X_r^q; finite, X_r>1] = O(r^N)` for each fixed `N>0` |
| Essential maximum | Positive probability at each fixed small `r`; `O(r^N)` for every fixed `N>0` |
| Moment including essential lifetime `∞` | Infinite at every fixed small `r` |

The key geometric step is short. A cubic matching the two values and two zero axial derivatives reaches a value above the maximum after passing the saddle. A fourth-derivative bound preserves that path. Thus a lifetime above the nominal gap requires an unusually large global derivative norm; the parent's all-order weighted bounds control its contribution.

[Read the proof](PROOF.md) · [Nonauthor analytic review](NONAUTHOR_REVIEW.md) · [Exact source identities and reading rules](SOURCES.json) · [Companion radial moment results](../../reviews/radial_moment_corollaries_20260930/README.md)

The [weighted moment and loss corollary](LOSS_COROLLARY.md), with its [separate review](LOSS_NONAUTHOR_REVIEW.md), gives a direct consequence for the full pinned law. Put `c_q=a−m_q>0`. Then the finite-death moment and the moment conditional on finite death both have expansion `1−c_q r³+o(r³)`. The bounded nonnegative loss `E[1−min(X_r,1)^q]` has expansion `c_q r³+o(r³)`. These use actual pairing success, on which `X_r=1` exactly; their finite-death convention is essential.

These are conditional mathematical consequences of the frozen parent estimates and the marked-law premises from PRs [#170](https://github.com/d6g8k5htny-coder/Math-/pull/170) and [#175](https://github.com/d6g8k5htny-coder/Math-/pull/175). Their review and acceptance obligations remain. The analysis uses actual elder pairing, the full weight and normalizer, and fixed parameters. It proves neither inverse moments nor an intensity for uniquely counted replacement bars.

## Reproduce the finite checks

From the repository root, using Python 3.11:

```sh
python3 -B -S frontiers/lifetime_moment_boundary_20260930/verify.py
```

This checks exact rational examples, negative controls, both Python optimization modes, and frozen source bytes. It does not replace the analytic proof, the separate nonauthor review, or the repository's required hosted formal gate. The proof's author-stage operational notes are preserved with its reviewed bytes; publication state belongs to the PR and delivery handoff. Scientific effect: NONE.
