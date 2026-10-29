#!/usr/bin/env python3
"""Bounded exact author controls for INVERSE_MOMENTS.md and LARGE_RATIO.md.

Standard-library rational arithmetic checks algebra, exponents and explicit
negative fixtures.  These finite controls do not prove Gaussian regression,
continuum estimates, large deviations, or mathematical/scientific acceptance.
Source validation means local byte identity, not verification of publication
carrier commits.  The work is authorship support, with no independent review
credit and scientific effect NONE.  Checks remain active under python -O.
"""

import ast
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
COUNTS = {}


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def counted(label, number=1):
    COUNTS[label] = COUNTS.get(label, 0) + number


def dot(left, right):
    require(len(left) == len(right), "matching vector lengths")
    return sum((x * y for x, y in zip(left, right)), F(0))


def transpose(matrix):
    return [list(column) for column in zip(*matrix)]


def mm(left, right):
    return [[dot(row, column) for column in transpose(right)] for row in left]


def identity(size):
    return [[F(i == j) for j in range(size)] for i in range(size)]


def determinant(matrix):
    work = [[F(value) for value in row] for row in matrix]
    size = len(work)
    require(all(len(row) == size for row in work), "square determinant input")
    result = F(1)
    for column in range(size):
        candidates = [row for row in range(column, size) if work[row][column]]
        if not candidates:
            return F(0)
        pivot = candidates[0]
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            result = -result
        diagonal = work[column][column]
        result *= diagonal
        for row in range(column + 1, size):
            factor = work[row][column] / diagonal
            for entry in range(column + 1, size):
                work[row][entry] -= factor * work[column][entry]
    return result


def inverse(matrix):
    size = len(matrix)
    work = [[F(value) for value in row] + unit
            for row, unit in zip(matrix, identity(size))]
    for column in range(size):
        candidates = [row for row in range(column, size) if work[row][column]]
        require(bool(candidates), "nonsingular rational inverse input")
        pivot = candidates[0]
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [value / divisor for value in work[column]]
        for row in range(size):
            if row != column:
                factor = work[row][column]
                work[row] = [x - factor * y
                             for x, y in zip(work[row], work[column])]
    return [row[size:] for row in work]


def positive_definite(matrix):
    return (matrix == transpose(matrix)
            and all(determinant([row[:size] for row in matrix[:size]]) > 0
                    for size in range(1, len(matrix) + 1)))


def scale(matrix, scalar):
    return [[scalar * value for value in row] for row in matrix]


def norm_squared(matrix):
    return sum((value * value for row in matrix for value in row), F(0))


def polynomial_value(coefficients, point, derivative=0):
    return sum((coefficient * F(factorial(degree), factorial(degree - derivative))
                * point ** (degree - derivative)
                for degree, coefficient in enumerate(coefficients)
                if degree >= derivative), F(0))


def monomial_kernel(degree, derivative, radius, kernel):
    """Integrate kernel(theta) times D^derivative(t^degree)(r theta)."""
    if degree < derivative:
        return F(0)
    coefficient = F(factorial(degree), factorial(degree - derivative))
    return coefficient * radius ** (degree - derivative) * sum(
        (value / F(degree - derivative + power + 1)
         for power, value in enumerate(kernel)), F(0))


def endpoint_rows(coefficients, radius):
    g0 = polynomial_value(coefficients, F(0))
    gr = polynomial_value(coefficients, radius)
    gp0 = polynomial_value(coefficients, F(0), 1)
    gpr = polynomial_value(coefficients, radius, 1)
    u2 = (gpr - gp0) / radius
    u3 = 6 * (gp0 + gpr - 2 * (gr - g0) / radius) / radius ** 2
    appended_a = (polynomial_value(coefficients, F(0), 2)
                  - u2 + radius * u3 / 2) / radius ** 2
    appended_v = (gp0 - (gr - g0) / radius) / radius
    return u2, u3, appended_a, appended_v


def peano_and_pin_controls():
    for degree, radius in product(range(11), [F(1, 32), F(1, 7), F(2, 3)]):
        coefficients = [F(0)] * degree + [F(1)]
        u2, u3, appended_a, appended_v = endpoint_rows(coefficients, radius)
        require(u2 == monomial_kernel(degree, 2, radius, [F(1)]),
                "U2 exact monomial kernel")
        require(u3 == monomial_kernel(degree, 3, radius, [F(0), F(6), F(-6)]),
                "U3 exact monomial kernel")
        require(appended_a == monomial_kernel(
            degree, 4, radius, [F(0), F(1), F(-2), F(1)]),
            "A_r exact Peano kernel")
        require(appended_v == monomial_kernel(degree, 2, radius, [F(-1), F(1)]),
                "v_r exact Peano kernel")
        counted("peano_monomial_radius_cases")
    require(sum((value / F(power + 1)
                 for power, value in enumerate([F(0), F(1), F(-2), F(1)])), F(0))
            == F(1, 12), "A contact coefficient")
    require(-1 + F(1, 2) == F(-1, 2), "v contact coefficient")
    counted("contact_kernel_coefficients", 2)

    # a*t^2*(t-r)^2 preserves both value and gradient pins exactly.
    for birth, gap, radius, quartic in product(
            [F(-2), F(0), F(3, 5)], [F(1, 2), F(2)],
            [F(1, 32), F(1, 7), F(2, 3)], [F(-3), F(0), F(5, 2)]):
        coefficients = [birth, F(0), -3 * gap * radius + quartic * radius ** 2,
                        2 * gap - 2 * quartic * radius, quartic]
        require(polynomial_value(coefficients, F(0)) == birth, "raw birth pin")
        require(polynomial_value(coefficients, radius) == birth - gap * radius ** 3,
                "raw gap pin")
        require(polynomial_value(coefficients, F(0), 1) == 0
                and polynomial_value(coefficients, radius, 1) == 0,
                "raw endpoint gradient pins")
        u2, u3, appended_a, unused_v = endpoint_rows(coefficients, radius)
        require(u2 == 0 and u3 == 12 * gap, "pinned desingularized rows")
        require(appended_a == 2 * quartic, "raw quartic appended coordinate")
        require(polynomial_value(coefficients, F(0), 2)
                == -6 * gap * radius + radius ** 2 * appended_a,
                "raw pinned H_uu identity")
        counted("raw_pinned_quartic_cases")


HARD_BLOCKS = [
    [[F(1, 3)]], [[F(2)]],
    [[F(2), F(1, 3)], [F(1, 3), F(1)]],
    [[F(1), F(-1, 2)], [F(-1, 2), F(3, 2)]],
]


def schur_controls():
    for hard, radius, gap, appended_a, v_scale in product(
            HARD_BLOCKS, [F(1, 32), F(1, 7), F(1, 3)],
            [F(1, 2), F(2)], [F(-2), F(1)], [F(-3, 2), F(0), F(2)]):
        size = len(hard)
        vector = [v_scale * F(index + 1, index + 2) for index in range(size)]
        q = 6 * gap - radius * appended_a
        require(q > 0 and positive_definite(hard), "positive Schur fixtures")
        coefficient = radius / q
        block_b = [[hard[i][j] + coefficient * vector[i] * vector[j]
                    for j in range(size)] for i in range(size)]
        hessian = [[-radius * q] + [radius * v for v in vector]]
        hessian.extend([[radius * vector[i]] + [-v for v in block_b[i]]
                        for i in range(size)])
        lower = [[F(1)] + [F(0)] * size]
        lower.extend([[-vector[i] / q] + identity(size)[i] for i in range(size)])
        diagonal = [[radius * q] + [F(0)] * size]
        diagonal.extend([[F(0)] + row for row in hard])
        require(scale(hessian, F(-1)) == mm(mm(lower, diagonal), transpose(lower)),
                "exact physical Schur congruence")
        require(positive_definite(scale(hessian, F(-1))), "typed maximum fixture")
        require(abs(determinant(hessian)) == radius * q * determinant(hard),
                "absolute determinant equals r q det C")
        cv = [dot(row, vector) for row in hard]
        difference = (2 * coefficient * dot(vector, cv)
                      + coefficient ** 2 * dot(vector, vector) ** 2)
        require(norm_squared(block_b) - norm_squared(hard) == difference,
                "exact PSD shift Frobenius identity")
        require(difference >= 0, "PSD shift preserves Gaussian envelope fixture")
        counted("schur_congruence_and_psd_shift_cases")

    # Reversing the Schur shift changes the determinant, even in one hard dimension.
    radius, q, vector, block_b = F(1, 2), F(2), F(1), F(2)
    hessian = [[-radius * q, radius * vector], [radius * vector, -block_b]]
    correct = block_b - radius * vector ** 2 / q
    wrong = block_b + radius * vector ** 2 / q
    require(abs(determinant(hessian)) == radius * q * correct
            and abs(determinant(hessian)) != radius * q * wrong,
            "wrong Schur sign counterexample detected")
    require(F(1, 2) ** 2 < F(1) ** 2,
            "negative rank-one shift invalidates claimed norm monotonicity")
    wrong_lower = [[F(1), F(0)], [vector / q, F(1)]]
    diagonal = [[radius * q, F(0)], [F(0), correct]]
    require(scale(hessian, F(-1)) != mm(mm(wrong_lower, diagonal), transpose(wrong_lower)),
            "wrong mixed congruence sign counterexample detected")
    counted("invalid_schur_sign_counterexamples", 3)


def powers_and_integrals():
    for dimension, radius in product(range(2, 10), [F(1, 32), F(1, 5), F(2, 3)]):
        mixed = dimension - 1
        transverse = mixed * (mixed + 1) // 2
        # Independent symmetric entries: A -> H_uu, v -> H_uy, B -> H_yy.
        derivatives = [radius ** 2] + [radius] * mixed + [F(-1)] * transverse
        jacobian = [[entry if i == j else F(0)
                     for j, entry in enumerate(derivatives)]
                    for i in range(len(derivatives))]
        require(abs(determinant(jacobian)) == radius ** (dimension + 1),
                "physical Hessian affine Jacobian")
        n = dimension + 3
        prior_power = n + 1 - (dimension + 1)
        require(prior_power == n - dimension == 3, "rare sector pre-epsilon power")
        require(F(prior_power) + 3 * F(2, 3) == 5,
                "retained N=d+3 gives r^5 t^(2/3)")
        require(F((dimension + 2) - dimension) + 3 * F(2, 3) != 5,
                "lower moment order does not give claimed radius power")
        counted("affine_jacobian_and_rare_exponent_cases")

    for s in [F(1, 64), F(1, 8), F(1, 2), F(1)]:
        integral = s ** 2 / 2 + s ** 3 * (1 / s - 1)
        require(integral == F(3, 2) * s ** 2 - s ** 3,
                "exact split lambda min(1,s^3/lambda^3) integral")
        require(s ** 2 / 2 <= integral <= F(3, 2) * s ** 2,
                "two-thirds spectral integral scale")
        counted("spectral_integral_cases")

    for power, radius, cube_root_t, cube_root_T, constant in product(
            [14, 16], [F(1, 32), F(1, 5)], [F(1, 8), F(1, 2), F(1)],
            [F(1), F(3, 2)], [F(2, 3), F(2)]):
        # t=s^3, T=z^3 keep the rational fractional-power endpoints exact.
        upper = constant * radius * cube_root_t * cube_root_T ** power
        integrated = radius ** 3 * upper ** 2 / 2
        require(integrated == constant ** 2 / 2 * radius ** 5 * cube_root_t ** 2
                * cube_root_T ** (2 * power),
                "exact x dx edge integral gives r^5 t^(2/3)")
        require(F(3) + 2 == 5 and F(1, 3) * 2 == F(2, 3),
                "edge exponent bookkeeping")
        counted("schur_edge_integral_cases")
    radius, s = F(1, 8), F(1, 4)
    require(radius ** 3 * (radius * s) != radius ** 3 * (radius * s) ** 2 / 2,
            "dropping determinant x changes edge integral")
    counted("missing_edge_weight_counterexamples")


def scalar_split_controls():
    for d_constant, radius, retained_t, numerator in product(
            [F(1, 2), F(1), F(3)], [F(1, 16), F(1, 4), F(1)],
            [F(1), F(2), F(5, 2)], range(1, 161)):
        x = F(numerator, 16)
        if x <= d_constant * radius * (retained_t + x) ** 2:
            near = x <= 4 * d_constant * radius * retained_t ** 2
            far = x > 1 / (4 * d_constant * radius)
            require(near or far, "scalar quadratic near/far split")
            counted("scalar_split_premise_cases")
        counted("scalar_split_grid_cases")

    # This far solution satisfies the quadratic premise and violates the near
    # conclusion.  It must be charged to the large-P sector, not omitted.
    for d_constant, radius in product([F(1, 2), F(1), F(3)], [F(1, 64), F(1, 16)]):
        retained_t = F(1)
        x = 2 / (d_constant * radius)
        require(x <= d_constant * radius * (retained_t + x) ** 2,
                "explicit far fixture satisfies original quadratic inequality")
        require(x > 4 * d_constant * radius * retained_t ** 2,
                "far fixture refutes unconditional near conclusion")
        require(x > 1 / (4 * d_constant * radius), "far fixture retained")
        c0 = 1 / (8 * d_constant)
        p_value = retained_t + x
        require(p_value >= x and c0 < 1 / (4 * d_constant)
                and p_value > c0 / radius,
                "far fixture is excluded by moderate cutoff and charged to large P")
        counted("retained_scalar_far_counterexamples")


def inverse_moment_controls():
    alpha = F(2, 3)
    for p, delta_root in product([F(1, 6), F(1, 3), F(1, 2), F(3, 5)],
                                 [F(1, 2), F(2, 3), F(1)]):
        exponent = alpha - p
        coefficient = 1 + p / exponent
        require(coefficient == alpha / (alpha - p), "inverse UI coefficient")
        exponent_times_thirty = 30 * exponent
        require(exponent_times_thirty.denominator == 1 and exponent > 0,
                "subcritical positive truncation exponent")
        boundary = delta_root ** exponent_times_thirty.numerator
        integral_term = p / exponent * boundary
        require(boundary + integral_term == alpha / (alpha - p) * boundary,
                "exact UI boundary plus integral terms")
        require(coefficient != p / exponent,
                "omitting truncation boundary produces wrong coefficient")
        counted("inverse_ui_coefficient_cases")
    require(alpha - F(2, 3) == 0 and alpha - F(1) < 0,
            "critical and supercritical powers do not have positive UI exponent")
    # Model H(t)=t^(2/3): t=y^3 has density 2y.  At p=2/3,
    # each dyadic interval has the rational lower bound one for 2/y.
    for block in range(12):
        lower, upper = F(2) ** (-block - 1), F(2) ** (-block)
        critical_lower_bound = 2 * (upper - lower) / upper
        supercritical_integral = 2 * (1 / lower - 1 / upper)
        subcritical_integral = 2 * (upper - lower)  # p=1/3.
        require(critical_lower_bound == 1, "critical dyadic mass does not decay")
        require(supercritical_integral == F(2) ** (block + 1),
                "supercritical exact dyadic growth")
        require(subcritical_integral == F(2) ** (-block),
                "subcritical exact geometric decay")
        counted("inverse_moment_boundary_blocks")
    counted("critical_ui_denominator_counterexamples")


def contact_weight(matrix_a, vector_b, fourth, tau):
    delta = determinant(matrix_a)
    matrix_inverse = inverse(matrix_a)
    quadratic = dot(vector_b, [dot(row, vector_b) for row in matrix_inverse])
    gamma = fourth / 12 - quadratic / 4
    # Y is evaluated with the adjugate, with no inverse in its definition.
    adjugate = [[delta * entry for entry in row] for row in matrix_inverse]
    polynomial_y = (fourth * delta / 12
                    - dot(vector_b, [dot(row, vector_b) for row in adjugate]) / 4)
    negative = positive_definite(scale(matrix_a, F(-1)))
    weight = max(36 * tau ** 2 * delta ** 2 - polynomial_y ** 2, F(0)) if negative else F(0)
    return delta, polynomial_y, gamma, weight, negative


def large_ratio_controls():
    for hard, vector_scale, fourth, tau in product(
            HARD_BLOCKS, [F(0), F(1, 2), F(-2)],
            [F(-96), F(-48), F(-36), F(-24), F(0), F(24)],
            [F(1, 2), F(1), F(5, 3), F(3)]):
        matrix_a = scale(hard, F(-1))
        vector_b = [vector_scale * F(index + 1) for index in range(len(hard))]
        delta, polynomial_y, gamma, weight, negative = contact_weight(
            matrix_a, vector_b, fourth, tau)
        require(negative and polynomial_y == delta * gamma,
                "inverse-free Y equals Delta gamma on A<0")
        require(36 * delta ** 2 - weight / tau ** 2
                == min(36 * delta ** 2, polynomial_y ** 2 / tau ** 2),
                "literal contact weight normalizer min identity")
        require(0 <= weight / tau ** 2 <= 36 * delta ** 2,
                "full weight polynomial envelope")
        require(gamma >= fourth / 12, "gamma lower bound on A<0")
        if gamma < -2 * tau:
            require(fourth < -24 * tau, "negative sector implies quartic action constraint")
        dimension = len(hard) + 1
        unit_weight = contact_weight(matrix_a, vector_b, fourth, F(1))[3]
        scaled_weight = contact_weight(scale(matrix_a, tau),
                                       [tau * value for value in vector_b],
                                       tau * fourth, tau)[3]
        require(scaled_weight == tau ** (2 * dimension) * unit_weight,
                "full determinant weight homogeneity tau^(2d)")
        counted("large_ratio_weight_cases")

    positive_a = [[F(1)]]
    delta, polynomial_y, gamma, weight, negative = contact_weight(
        positive_a, [F(2)], F(-36), F(1))
    require(not negative and weight == 0 and gamma < F(-36, 12),
            "gamma bound requires the negative hard block sign")
    unit_weight = contact_weight([[F(-1)]], [F(0)], F(-36), F(1))[3]
    scaled_weight = contact_weight([[F(-2)]], [F(0)], F(-72), F(2))[3]
    require(unit_weight > 0 and scaled_weight == 2 ** 4 * unit_weight
            and scaled_weight != 2 ** 2 * unit_weight,
            "full-weight degree is distinct from normalizer tau squared")
    counted("large_ratio_sign_and_degree_counterexamples", 2)

    kernel_integral = sum((F((-1) ** power * factorial(3),
                             factorial(power) * factorial(3 - power)) / F(power + 1)
                           for power in range(4)), F(0))
    require(kernel_integral / 6 == F(1, 24), "one-contact Taylor coefficient")
    for degree, x in product(range(4, 11), [F(-2, 3), F(-1, 32), F(1, 32), F(2, 3)]):
        integral = monomial_kernel(degree, 4, x,
                                   [F(1), F(-3), F(3), F(-1)])
        require(x ** 4 * integral / 6 == x ** degree,
                "one-node Taylor integral valid on both axial signs")
        counted("one_contact_taylor_monomial_cases")
    require(kernel_integral != F(1, 24), "missing Taylor factorial counterexample")
    counted("taylor_factor_counterexamples")


def digest_metadata(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode("ascii")
                                     + b"\0" + data).hexdigest()}


def source_identity_controls():
    source_bytes = (HERE / "SOURCES.json").read_bytes()
    manifest = json.loads(source_bytes)
    require(isinstance(manifest, dict), "source manifest object")
    entries = manifest.get("sources")
    require(isinstance(entries, list) and bool(entries), "nonempty source identity list")
    identifiers = set()
    for entry in entries:
        require(isinstance(entry, dict), "source identity object")
        for key in ("path", "bytes", "sha256", "git_blob"):
            require(key in entry, "source identity requires " + key)
        relative_path = entry.get("local_path", entry["path"])
        require(isinstance(relative_path, str) and not Path(relative_path).is_absolute(),
                "repository-relative local source path")
        target = (ROOT / relative_path).resolve()
        require(target.is_relative_to(ROOT), "source path stays in repository")
        require(target.is_file(), "source path is a local file: " + relative_path)
        require(type(entry["bytes"]) is int and entry["bytes"] >= 0,
                "source byte count is a nonnegative integer")
        actual = digest_metadata(target.read_bytes())
        for key, expected in actual.items():
            require(entry[key] == expected, "source " + key + " mismatch: " + relative_path)
        if "id" in entry:
            require(isinstance(entry["id"], str) and entry["id"] not in identifiers,
                    "distinct string source identifiers")
            identifiers.add(entry["id"])
        counted("source_entries_verified")
    # Both authored proofs are mandatory even if their identities are not
    # entries in the transitive source manifest.
    proof_metadata = {}
    for name in ("INVERSE_MOMENTS.md", "LARGE_RATIO.md"):
        data = (HERE / name).read_bytes()
        require(bool(data) and bool(data.decode("utf-8").strip()), "mandatory proof bytes")
        proof_metadata[name] = digest_metadata(data)
    counted("mandatory_proofs_hashed", len(proof_metadata))
    return proof_metadata, digest_metadata(source_bytes)


def main():
    self_bytes = Path(__file__).read_bytes()
    tree = ast.parse(self_bytes.decode("utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "all checks remain active under optimization")
    require(not any(isinstance(node, ast.Constant) and isinstance(node.value, float)
                    for node in ast.walk(tree)), "no floating point literals")
    peano_and_pin_controls()
    schur_controls()
    powers_and_integrals()
    scalar_split_controls()
    inverse_moment_controls()
    large_ratio_controls()
    proofs, sources = source_identity_controls()
    print(json.dumps({
        "result": "PASS",
        "scope": "bounded exact author controls; no continuum proof or independent review",
        "scientific_effect": "NONE",
        "proofs": proofs,
        "sources_manifest": sources,
        "checker": digest_metadata(self_bytes),
        "counts": COUNTS,
        "total_control_cases": sum(COUNTS.values()),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
