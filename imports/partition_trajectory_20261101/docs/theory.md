# Canonical theory

## 1. Possibility trajectories

A possibility trajectory is a causal information architecture through which an agent makes future tasks actionable. A finite model specifies:

- histories \(H\), optionally with probabilities;
- task suffixes \(R_t\), either required partitions or task random variables with losses;
- observations \(O_t\);
- memory states \(M_t\), with at most \(k\) states;
- available information \(A_t=(M_{t-1},O_t)\);
- causal updates \(M_t=f_t(A_t)\).

Exact actionability means that memory refines the required partition, or \(H(R_t|M_t)=0\), capacity permitting. Approximate actionability means that task–loss pairs remain below a declared Bayes-risk tolerance.

Possibility is therefore the family of task–loss structures that a causal information trajectory can keep actionable.

## 2. Causal bounds

### Refinement obstruction

A deterministic update is constant on each cell of \(A_t\). If one available cell intersects two required cells of \(R_t\), no update can refine \(R_t\). That cell is an obstruction witness.

### Entropy bound

For a deterministic update \(M_t=f(A_t)\),

\[
H(R_t|M_t)\geq H(R_t|A_t).
\]

Zero residual entropy recovers exact support, capacity permitting. Residual entropy alone does not rank approximate action success.

### Bayes-risk bound

For task loss \(L\),

\[
\rho_L(R|M_t)\geq \rho_L(R|A_t).
\]

Every decision rule measurable with respect to \(M_t\) is also measurable with respect to \(A_t\). The information-loss defect is

\[
D_L(M_t;A_t)=\rho_L(R|M_t)-\rho_L(R|A_t)\geq0.
\]

This defect is task-relative. It is not entropy and is not option value.

## 3. Partition joins and memory reuse

For static exact support of required partitions \(P_1,\ldots,P_T\), memory must refine

\[
P_*=\bigvee_{t=1}^{T}P_t.
\]

The same join governs joint options. A dynamic memory does not have to refine all required partitions simultaneously; it only has to refine the right suffix at the right time, subject to causal update feasibility.

This yields the distinction between:

- static memory, which must refine the partition join;
- dynamic memory, whose required capacity is bounded below by the largest stage partition but is not always causally attainable;
- nonmonotone information trajectories, which are not filtrations because useful forgetting can coarsen information.

## 4. Flexibility and bottlenecks

The exact flexibility sector contains future task partitions supported by memory. The risk-flexibility sector is

\[
\Phi_{\epsilon,L}(M)=\{(R,L)\in\mathfrak T:\rho_L(R|M)\leq\epsilon\}.
\]

An actionable bottleneck minimizes task risk subject to a memory bound:

\[
M^*_{\mathrm{action}}=\arg\min_{M\in\mathcal M_k}\rho_L(R|M).
\]

For multiple tasks, minimize a vector of risks rather than assuming one scalar optimum. Memories can form MI–risk or multitask Pareto frontiers. Task mutual information and Bayes risk genuinely diverge in the included three-state observation model.

## 5. Randomization and visibility

An option uncertainty premium depends on the option family, randomization, adversary visibility, and timing.

The deterministic specialized memories have minimax option risk \(0.25\). A 50/50 randomized mixture has distribution-level minimax risk \(0.125\). A realization-level adversary still obtains \(0.25\). Under expected loss, the robust memory is not automatically optimal; it becomes preferable only under specified hard constraints or noise regimes.

## 6. Independent asymmetric visibility theorem

For independent binary symmetric channels with rates \(\alpha\) on \(x\) and \(\beta\) on \(z\), the specialized option risks are

\[
A_0=0.25\alpha+0.5(1-\alpha)\beta,
\qquad
A_1=0.25-0.25\alpha+0.5\alpha\beta.
\]

The full-observation floor is \((\alpha,\beta/2,\beta/2)\). A balanced specialized mixture has distribution-level minimax risk

\[
U_{\mathrm{dist}}=0.125+0.25\beta.
\]

A realization-level adversary obtains

\[
U_{\mathrm{real}}=0.25-0.25\alpha+0.5\alpha\beta.
\]

The exact gap is

\[
U_{\mathrm{real}}-U_{\mathrm{dist}}
=0.125(1-2\alpha)(1-2\beta).
\]

It vanishes when either channel is pure noise. Under balanced option uncertainty, the robust memory is expected-loss preferable to the balanced specialized mixture when \(2\alpha-\beta>1/2\).

## 7. Correlated-noise boundary

Let \(\kappa=P(\text{both observations flip})\), with independence at \(\kappa=\alpha\beta\). Correlation changes posterior cell weights and can switch optimal decisions. The visibility gap is then piecewise rather than universally factorized.

For \(\alpha=0.2,\beta=0.3\), the independent formula predicts gap \(0.03\). The exact correlated model gives gap \(0\) at \(\kappa=0\), \(0.03\) at \(\kappa=0.06\), and \(0.05\) at \(\kappa=0.10\) and \(0.20\). The factorization is therefore independence-specific.

## 8. Interpretation and limits

Established components are partition refinement, constraint solving, information theory, Bayes decision theory, and finite games. The proposed connection is their use as a possibility semantics based on causal information trajectories.

The package is a finite model instrument. It does not establish universal laws of agency or performance of deployed systems. Losses, action sets, observation schedules, memory capacity, and adversary visibility must be declared. Exhaustive search is combinatorial, and correlated or non-Bayesian controllers may require new analysis.
