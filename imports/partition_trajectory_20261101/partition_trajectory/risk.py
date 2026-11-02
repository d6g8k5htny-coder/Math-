"""Decision-theoretic risk, entropy, and information-loss measures."""
import math


def binary_entropy(p):
    if p <= 0 or p >= 1:
        return 0.0
    return -(p * math.log2(p) + (1 - p) * math.log2(1 - p))


def posterior_groups(histories, probs, task, memory):
    groups = {}
    for history in histories:
        groups.setdefault(memory[history], []).append(history)
    result = []
    for cell in groups.values():
        weight = sum(probs[h] for h in cell)
        posterior = sum(probs[h] * task[h] for h in cell) / weight
        result.append((weight, posterior, cell))
    return result


def bayes_error(histories, probs, task, memory, relevant=None):
    """Bayes-optimal zero-one error, optionally restricted to relevant histories.

    `task[h]` is either the binary label or P(R=1|h) when histories are posterior
    cells. Relevance weights allow conditional options such as predicting z only
    when x=0.
    """
    relevant = relevant or {h: 1 for h in histories}
    error = 0.0
    for _, _, cell in posterior_groups(histories, probs, task, memory):
        relevant_cell = [h for h in cell if relevant[h]]
        relevant_weight = sum(probs[h] for h in relevant_cell)
        if relevant_weight:
            posterior = sum(probs[h] * task[h] for h in relevant_cell) / relevant_weight
            error += relevant_weight * min(posterior, 1 - posterior)
    return error


def mutual_information(histories, probs, task, memory):
    """Mutual information I(M;R) in bits for binary or deterministic task states."""
    memory_marginal, task_marginal, joint = {}, {}, {}
    for history in histories:
        memory_marginal[memory[history]] = memory_marginal.get(memory[history], 0.0) + probs[history]
        task_marginal[task[history]] = task_marginal.get(task[history], 0.0) + probs[history]
        key = (memory[history], task[history])
        joint[key] = joint.get(key, 0.0) + probs[history]
    result = 0.0
    for (memory_value, task_value), probability in joint.items():
        if probability > 0:
            result += probability * math.log2(
                probability / (memory_marginal[memory_value] * task_marginal[task_value])
            )
    return result


def conditional_entropy(histories, probs, task, memory):
    """Residual task entropy H(R|M) for discrete task variables."""
    result = 0.0
    for weight, _, cell in posterior_groups(histories, probs, task, memory):
        counts = {}
        for history in cell:
            counts[task[history]] = counts.get(task[history], 0.0) + probs[history]
        entropy = 0.0
        for probability in counts.values():
            conditional = probability / weight
            entropy -= conditional * math.log2(conditional)
        result += weight * entropy
    return result


def information_loss_defect(histories, probs, task, memory, available, relevant=None):
    """Risk under memory minus risk under available information."""
    return (
        bayes_error(histories, probs, task, memory, relevant)
        - bayes_error(histories, probs, task, available, relevant)
    )
