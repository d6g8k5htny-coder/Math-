# Glossary

**Possibility trajectory** — A time-indexed sequence of available information, memory states, and causal updates through which task suffixes become actionable.

**Task suffix** — The distinctions or random variables required to act successfully for the remainder of a task.

**Available information** — The joint information \((M_{t-1},O_t)\) consisting of previous memory and the current observation.

**Causal memory update** — A memory update \(M_t=f_t(M_{t-1},O_t)\) determined entirely by previously available information.

**Exact actionability** — Memory refines the required task partition, or residual task entropy is zero, subject to capacity.

**Approximate actionability** — A task–loss pair remains within a declared Bayes-risk tolerance.

**Obstruction cell** — An available-information cell whose histories cannot be distinguished by an update even though the task requires differentiating them.

**Partition refinement** — Partition \(P\) refines \(Q\) when every cell of \(P\) is contained in a cell of \(Q\).

**Partition join** — The coarsest partition that refines every member of a family. Static exact support requires refinement of the join.

**Nonmonotone information trajectory** — An information sequence that can refine or coarsen over time. It need not be a filtration because useful forgetting is allowed.

**Memory-reuse gain** — The static-minus-dynamic capacity advantage when a causal memory schedule reuses states for different distinctions.

**Flexibility sector** — The future task partitions a memory can support exactly.

**Risk-flexibility sector** — The task–loss pairs whose Bayes risk under memory is below a stated tolerance.

**Information-loss defect** — Bayes risk under memory minus Bayes risk under available information.

**Actionable bottleneck** — A memory selected to minimize task-relative Bayes risk under a memory bound, rather than to maximize stored information alone.

**MI–risk Pareto frontier** — The nondominated memories when task mutual information is maximized and Bayes risk is minimized simultaneously.

**Specialized memory** — A memory that preserves the current task and one option while sacrificing another.

**Robust memory** — A memory that preserves every declared option, potentially at a cost to current-task performance.

**Option uncertainty premium** — The additional risk caused by not knowing the future option when memory is selected. Its value depends on randomization, adversary visibility, and timing.

**Distribution-level adversary** — An adversary that chooses an option knowing the encoding distribution but not the realized memory.

**Realization-level adversary** — An adversary that chooses an option after seeing the realized memory.

**Full-observation floor** — The Bayes risk achievable with all declared observations before memory compression.

**Section-or-obstruction solver** — A finite solver that returns either a causal memory trajectory or a localized witness showing why the required refinement cannot be produced.

All terms are provisional labels for the implemented finite-model framework, not claims of standardized terminology.
