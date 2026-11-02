"""Exact independent and correlated binary-channel option models."""
from itertools import product
from .risk import bayes_error

MEMORY_A = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 2}
MEMORY_B = {(0, 0): 0, (0, 1): 0, (1, 0): 1, (1, 1): 2}
MEMORY_C = {(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 2}


def full_observation_floor(alpha, beta):
    return (alpha, beta / 2, beta / 2)


def specialized_risks(alpha, beta):
    """Independent-channel risks for M_A; M_B swaps the option components."""
    a0 = 0.25 * alpha + 0.5 * (1 - alpha) * beta
    a1 = 0.25 - 0.25 * alpha + 0.5 * alpha * beta
    return (alpha, a0, a1)


def robust_risks(alpha, beta):
    return (0.25 + 0.5 * alpha, 0.5 * beta, 0.5 * beta)


def visibility_premia(alpha, beta):
    distribution = 0.125 + 0.25 * beta
    realization = 0.25 - 0.25 * alpha + 0.5 * alpha * beta
    return {
        "distribution": distribution,
        "realization": realization,
        "gap": realization - distribution,
    }


def robust_expected_loss_comparison(alpha, beta):
    mixture = alpha + 0.125 + 0.25 * beta
    robust = 0.25 + 0.5 * alpha + 0.5 * beta
    return {
        "specialized_mixture": mixture,
        "robust": robust,
        "robust_minus_mixture": robust - mixture,
        "robust_preferred": 2 * alpha - beta > 0.5,
    }


def _channel_histories(alpha, beta, kappa):
    error_probs = {
        (0, 0): 1 - alpha - beta + kappa,
        (1, 0): alpha - kappa,
        (0, 1): beta - kappa,
        (1, 1): kappa,
    }
    histories, probs = [], {}
    for x, z, observed_x, observed_z in product((0, 1), repeat=4):
        history = (x, z, observed_x, observed_z)
        histories.append(history)
        probs[history] = 0.25 * error_probs[(observed_x ^ x, observed_z ^ z)]
    return histories, probs


def correlated_risks(alpha, beta, kappa, memory):
    histories, probs = _channel_histories(alpha, beta, kappa)
    mapped = {h: memory[h[2:]] for h in histories}
    task_x = {h: h[0] for h in histories}
    task_z = {h: h[1] for h in histories}
    relevant_0 = {h: int(h[0] == 0) for h in histories}
    relevant_1 = {h: int(h[0] == 1) for h in histories}
    return (
        bayes_error(histories, probs, task_x, mapped),
        bayes_error(histories, probs, task_z, mapped, relevant_0),
        bayes_error(histories, probs, task_z, mapped, relevant_1),
    )


def correlated_visibility(alpha, beta, kappa):
    a = correlated_risks(alpha, beta, kappa, MEMORY_A)
    b = correlated_risks(alpha, beta, kappa, MEMORY_B)
    distribution_0 = (a[1] + b[1]) / 2
    distribution_1 = (a[2] + b[2]) / 2
    distribution = max(distribution_0, distribution_1)
    realization = max(a[1], a[2], b[1], b[2])
    return {
        "distribution": distribution,
        "realization": realization,
        "gap": realization - distribution,
        "A": a,
        "B": b,
    }
