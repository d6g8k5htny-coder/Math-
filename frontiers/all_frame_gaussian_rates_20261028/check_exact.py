#!/usr/bin/env python3
"""Exact finite author controls; no continuum or scientific acceptance."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def dot(a, b):
    require(len(a) == len(b), 'matching vector lengths')
    return sum(x*y for x, y in zip(a, b))


def transpose(a):
    return list(map(list, zip(*a)))


def mm(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def identity(size):
    return [[F(i == j) for j in range(size)] for i in range(size)]


def inverse(a):
    size = len(a)
    out = [list(row)+unit for row, unit in zip(a, identity(size))]
    for col in range(size):
        candidates = [j for j in range(col, size) if out[j][col]]
        require(bool(candidates), 'nonsingular exact Gram matrix')
        pivot = candidates[0]
        out[col], out[pivot] = out[pivot], out[col]
        divisor = out[col][col]
        out[col] = [v/divisor for v in out[col]]
        for row in range(size):
            if row != col:
                factor = out[row][col]
                out[row] = [x-factor*y for x, y in zip(out[row], out[col])]
    return [row[size:] for row in out]


def rank(a):
    out = [list(row) for row in a]
    row = 0
    for col in range(len(out[0])):
        candidates = [i for i in range(row, len(out)) if out[i][col]]
        if not candidates:
            continue
        pivot = candidates[0]
        out[row], out[pivot] = out[pivot], out[row]
        divisor = out[row][col]
        out[row] = [v/divisor for v in out[row]]
        for i in range(row+1, len(out)):
            factor = out[i][col]
            out[i] = [x-factor*y for x, y in zip(out[i], out[row])]
        row += 1
        if row == len(out):
            break
    return row


def contact_matrix(frame, cube_radius):
    dimension = len(frame)
    representatives = []
    for n in product(range(-cube_radius, cube_radius+1), repeat=dimension):
        nonzero = [v for v in n if v]
        if nonzero and nonzero[0] > 0:
            representatives.append(n)
    columns = [[F(1)]+[F(0)]*(2*dimension+1)]
    for n in representatives:
        axial = dot(n, frame[0])
        transverse = [dot(n, y) for y in frame[1:]]
        cosine = [F(1), F(0), -axial**2, F(0)]
        sine = [F(0), axial, F(0), -axial**3]
        for normal in transverse:
            cosine.extend([F(0), -axial*normal])
            sine.extend([normal, F(0)])
        columns.extend([cosine, sine])
    return transpose(columns)


frames = [identity(2),
          [[F(3, 5), F(4, 5)], [F(-4, 5), F(3, 5)]],
          [[F(5, 13), F(12, 13)], [F(-12, 13), F(5, 13)]],
          identity(3),
          [[F(3, 5), F(4, 5), F(0)],
           [F(-4, 5), F(3, 5), F(0)], [F(0), F(0), F(1)]],
          [[F(7, 9), F(-4, 9), F(-4, 9)],
           [F(-4, 9), F(1, 9), F(-8, 9)],
           [F(-4, 9), F(-8, 9), F(1, 9)]]]
counts = {}
for frame in frames:
    dimension = len(frame)
    require(mm(frame, transpose(frame)) == identity(dimension), 'rational orthogonal frame')
    rows = contact_matrix(frame, 2)
    gram = mm(rows, transpose(rows))
    gram_inverse = inverse(gram)
    dual = mm(transpose(rows), gram_inverse)
    require(mm(rows, dual) == identity(2*dimension+2), 'exact contact right inverse')
counts['full_cube_contact_right_inverse_cases'] = len(frames)
for dimension in [2, 3]:
    rows = contact_matrix(identity(dimension), 1)
    require(rows[3] == [-x for x in rows[1]], 'small-cube cubic aliases gradient')
    require(rank(rows) < 2*dimension+2, 'small-cube rank obstruction')
counts['insufficient_cube_counterexamples'] = 2

# Coefficients of l^2, lr, r^2 in the global-margin identity.
left = [F(19, 10)-F(1, 14), F(-6), F(5)-F(1, 14)]
right = [F(64, 35), -2*F(64, 35)*F(105, 64),
         F(64, 35)*F(105, 64)**2+F(3, 448)]
require(left == right, 'exact global-margin completed square')
counts['global_margin_identity'] = 1

circle = [(F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)),
          (F(-3, 5), F(4, 5)), (F(-1), F(0))]
projection_cases = 0
for dimension, omega, radius in product([2, 3], [F(1), F(2, 3), F(3)],
                                       [F(1, 8), F(1, 16)]):
    entries = circle[:dimension]
    cosine, sine = [p[0] for p in entries], [p[1] for p in entries]
    require(all(c*c+s*s == 1 for c, s in entries), 'unit-circle spatial fixtures')
    q = sum(2*(1-c) for c in cosine)/omega**2
    vector = [s/omega for s in sine]
    norm = dot(vector, vector)
    require(q-norm == sum((1-c)**2 for c in cosine)/omega**2,
            'periodic q minus sine-vector norm identity')
    require(norm > 0, 'nonzero physical pin vector')
    projector = [[F(i == j)-vector[i]*vector[j]/norm
                  for j in range(dimension)] for i in range(dimension)]
    w = [radius*x/norm for x in vector]
    require(dot(w, vector) == radius, 'actual axial functional at pin')
    require([dot(row, vector) for row in projector] == [0]*dimension,
            'transverse projection kills pin')
    require(mm(projector, projector) == projector, 'orthogonal projector idempotence')
    require(projector == transpose(projector), 'orthogonal projector symmetry')
    # Gradient of ||P s(x)||^2 is 2 Ds(x)^T P^T P s(x), with omega=1 scaling.
    projected = [dot(row, vector) for row in mm(transpose(projector), projector)]
    gradient = [2*c*p for c, p in zip(cosine, projected)]
    require(gradient == [0]*dimension, 'hard term has exact zero pin gradient')
    projection_cases += 1
counts['periodic_projection_cases'] = projection_cases

# Truncated exact formal power series in r. Only coefficients through degree 5
# are inspected; degree 12 construction leaves ample guard terms after r^2
# normalization in the denominator.
ORDER = 12


def clean(a):
    return {n: F(v) for n, v in a.items() if v and 0 <= n <= ORDER}


def add(a, b):
    out = dict(a)
    for n, v in b.items():
        out[n] = out.get(n, F(0))+v
    return clean(out)


def scale(a, value):
    return clean({n: value*v for n, v in a.items()})


def mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            if i+j <= ORDER:
                out[i+j] = out.get(i+j, F(0))+x*y
    return clean(out)


def shift(a, degree):
    require(all(n+degree >= 0 for n in a), 'formal division has no pole')
    return clean({n+degree: v for n, v in a.items()})


def reciprocal_unit(a):
    require(a.get(0, 0) != 0, 'invertible formal denominator')
    out = {0: 1/a[0]}
    for n in range(1, ORDER+1):
        out[n] = -sum(a.get(j, 0)*out.get(n-j, 0) for j in range(1, n+1))/a[0]
    return clean(out)


def trig_series(coordinate, sine):
    offset = int(sine)
    return clean({2*j+offset: F((-1)**j)*coordinate**(2*j+offset)/factorial(2*j+offset)
                  for j in range((ORDER-offset)//2+1)})


series_cases = 0
wrong_gradient_cases = 0
for frame, correction_on, gamma in product(frames, [0, 1], [F(1), F(3, 2)]):
    u = frame[0]
    sine = [trig_series(v, True) for v in u]
    cosine = [trig_series(v, False) for v in u]
    q, norm = {}, {}
    for s, c in zip(sine, cosine):
        q = add(q, scale(add({0: F(1)}, scale(c, -1)), 2))
        norm = add(norm, mul(s, s))
    require(norm.get(2) == 1 and q.get(2) == 1, 'unit direction leading series')
    inverse_norm = reciprocal_unit(shift(norm, -2))
    w = [mul(shift(s, -1), inverse_norm) for s in sine]
    value_error = add({3: F(2)}, scale(shift(mul(q, q), -1), -2))
    value_error = add(value_error, scale(shift(mul(mul(q, q), q), -1),
                                       correction_on*gamma))
    require(all(value_error.get(n, 0) == 0 for n in range(5)),
            'value discrepancy starts at degree five')
    u4 = sum(v**4 for v in u)
    require(value_error.get(5, 0) == u4/3+correction_on*gamma,
            'exact leading value-discrepancy coefficient')
    wrong_leading = []
    for i, ui in enumerate(u):
        first = scale(shift(mul(w[i], cosine[i]), 2), 8)
        qsine = shift(mul(q, sine[i]), -1)
        gradient_error = add(first, scale(qsine, -8))
        gradient_error = add(gradient_error,
                             scale(shift(mul(mul(q, q), sine[i]), -1),
                                   correction_on*6*gamma))
        require(all(gradient_error.get(n, 0) == 0 for n in range(4)),
                'gradient discrepancy starts at degree four')
        require(gradient_error.get(4, 0)
                == F(10, 3)*ui*u4-4*ui**3+correction_on*6*gamma*ui,
                'exact leading gradient-discrepancy coefficient')
        wrong = add(first, scale(qsine, -4))
        require(wrong.get(2, 0) == 4*ui,
                'missing q-derivative factor gives degree-two discrepancy')
        wrong_leading.append(wrong.get(2, 0))
    require(any(wrong_leading), 'wrong gradient coefficient cannot cancel for unit direction')
    wrong_gradient_cases += 1
    series_cases += 1
counts['formal_pin_discrepancy_cases'] = series_cases
counts['wrong_gradient_factor_counterexamples'] = wrong_gradient_cases

remote_cases = 0
for qp, kmax, fraction in product([F(1, 10), F(1, 2), F(2)],
                                 [F(1), F(3)], [F(1, 4), F(1)]):
    k = kmax*fraction
    gamma = (2*kmax+1)/qp
    require(qp*qp*(gamma*qp-2*k) >= qp*qp, 'remote positive margin')
    remote_cases += 1
counts['remote_margin_cases'] = remote_cases

# Additional critical-window algebra. These finite controls do not certify
# ridge construction, global event convergence or a Gaussian probability law.
for frame in frames:
    dimension = len(frame)
    extra_columns = [[F(0)]*((dimension-1)*dimension//2+dimension)]
    for n in product(range(-2, 3), repeat=dimension):
        nonzero = [value for value in n if value]
        if not nonzero or nonzero[0] < 0:
            continue
        axial = dot(n, frame[0])
        normal = [dot(n, y) for y in frame[1:]]
        cosine, sine = [], []
        for i in range(dimension-1):
            for j in range(i, dimension-1):
                cosine.append(-normal[i]*normal[j])
                sine.append(F(0))
        cosine += [F(0)]*(dimension-1)+[axial**4]
        sine += [-axial**2*v for v in normal]+[F(0)]
        extra_columns += [cosine, sine]
    augmented = contact_matrix(frame, 2)+transpose(extra_columns)
    gram = mm(augmented, transpose(augmented))
    require(mm(gram, inverse(gram)) == identity(len(augmented)),
            'contact rank after transverse Hessian, mixed cubic and axial quartic')
counts['critical_window_augmented_contact_rank_cases'] = len(frames)


def polynomial_value(coefficients, point):
    return sum(value*point**degree for degree, value in coefficients.items())


def polynomial_derivative(coefficients):
    return {degree-1: degree*value for degree, value in coefficients.items() if degree}


scalar_cases = 0
for tau, radius, c4factor in product([F(1, 2), F(1)], [F(1, 4), F(1, 16)],
                                    [F(-36), F(0), F(24)]):
    birth, c4 = F(3, 7), c4factor*tau
    second = radius**2*(-6*tau+c4/12)
    third = radius*(12*tau-c4/2)
    polynomial = {0: birth, 2: second/2, 3: third/6, 4: c4/24}
    first = polynomial_derivative(polynomial)
    second_polynomial = polynomial_derivative(first)
    require(polynomial_value(polynomial, 0) == birth, 'critical birth pin')
    require(polynomial_value(polynomial, radius) == birth-tau*radius**4,
            'critical lower value pin')
    require(polynomial_value(first, 0) == polynomial_value(first, radius) == 0,
            'critical derivative pins')
    require(polynomial_value(second_polynomial, radius)/radius**2 == 6*tau+c4/12,
            'critical lower axial Hessian normalization')
    scalar_cases += 1
counts['critical_window_exact_scalar_pin_cases'] = scalar_cases


def small_determinant(matrix):
    if not matrix:
        return F(1)
    return sum((-1)**j*matrix[0][j]*small_determinant(
        [row[:j]+row[j+1:] for row in matrix[1:]])
        for j in range(len(matrix)))


schur_cases = 0
for block in [[[F(-2)]], [[F(-2), F(1, 3)], [F(1, 3), F(-3)]]]:
    normal_dimension = len(block)
    det_a, inverse_a = small_determinant(block), inverse(block)
    for mixed_on, tau, radius, gamma_factor in product(
            [False, True], [F(1, 2), F(1)], [F(1, 4), F(1, 16)],
            [F(-8), F(-6), F(-4), F(-2), F(0), F(2), F(4), F(6), F(8)]):
        vector = ([F(1, 3), F(-2, 5)][:normal_dimension]
                  if mixed_on else [F(0)]*normal_dimension)
        quadratic = dot(vector, [dot(row, vector) for row in inverse_a])
        gamma_target = gamma_factor*tau
        c4 = 12*gamma_target+3*quadratic
        gamma = c4/12-quadratic/4
        require(gamma == gamma_target, 'reduced quartic Schur scalar')
        adjugate = [[det_a*v for v in row] for row in inverse_a]
        cofactor_quadratic = dot(vector, [dot(row, vector) for row in adjugate])
        determinants = []
        for sign in [-1, 1]:
            axial = radius**2*(sign*6*tau+c4/12)
            cross = [sign*radius*v/2 for v in vector]
            matrix = [[axial]+cross]+[[cross[i]]+block[i]
                                          for i in range(normal_dimension)]
            normalized = small_determinant(matrix)/radius**2
            require(normalized == (sign*6*tau+c4/12)*det_a-cofactor_quadratic/4,
                    'critical adjugate determinant identity')
            require(normalized == det_a*(sign*6*tau+gamma),
                    'critical Schur determinant identity')
            determinants.append(small_determinant(matrix))
        typed = gamma-6*tau < 0 and gamma+6*tau > 0
        actual_weight = abs(determinants[0]*determinants[1])/radius**4 if typed else F(0)
        require(actual_weight == det_a**2*max(36*tau**2-gamma**2, 0),
                'critical typed weight positive-part window')
        schur_cases += 1
counts['critical_window_schur_and_type_cases'] = schur_cases

profile_cases, negative_sector_cases = 0, 0
for tau in [F(1, 2), F(1)]:
    for gamma_factor in [F(-8), F(-6), F(-4), F(-2), F(0), F(2), F(4), F(6), F(8)]:
        gamma = tau*gamma_factor
        profile = {2: -3*tau+gamma/2, 3: 2*tau-gamma, 4: gamma/2}
        at_two = polynomial_value(profile, F(2))
        require(at_two == 4*tau+2*gamma, 'critical profile at doubled separation')
        require((at_two > 0) == (gamma > -2*tau), 'critical positive-profile threshold')
        if gamma == -2*tau:
            require(profile == {2: -4*tau, 3: 4*tau, 4: -tau},
                    'critical boundary square polynomial')
        profile_cases += 1
    for rho in [F(3, 2), F(2), F(5, 2)]:
        gamma = -2*tau*rho
        profile = {2: -3*tau+gamma/2, 3: 2*tau-gamma, 4: gamma/2}
        centered_square = {0: (1+1/rho)**2, 1: -2*(1+1/rho), 2: F(1)}
        bracket = add(scale(centered_square, rho), {0: 1-1/rho})
        require(profile == scale(shift(bracket, 2), -tau),
                'negative-sector completed-square identity')
        require(1-1/rho >= F(1, 3), 'fixed positive negative-sector margin')
        require(-6*tau < gamma < -2*tau and 36*tau**2-gamma**2 > 0,
                'negative sector remains strictly inside typed window')
        negative_sector_cases += 1
counts['critical_window_profile_threshold_cases'] = profile_cases
counts['critical_window_negative_sector_margin_cases'] = negative_sector_cases

source_checks = []
for source in json.loads((HERE / 'SOURCES.json').read_text())['sources']:
    raw = (ROOT / source['path']).read_bytes()
    require(len(raw) == source['bytes'], 'source bytes: ' + source['id'])
    require(hashlib.sha256(raw).hexdigest() == source['sha256'],
            'source digest: ' + source['id'])
    require(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
            == source['git_blob'], 'source blob: ' + source['id'])
    source_checks.append(source['id'])

print(json.dumps({
    'status': 'PASS',
    'scope': 'Finite exact contact matrices, polynomial identities and formal '
             'series coefficients only; no continuum or Gaussian probability certification.',
    'counts': counts,
    'source_checks': source_checks,
    'proof_sha256': hashlib.sha256((HERE / 'PROOF.md').read_bytes()).hexdigest(),
    'critical_window_sha256': hashlib.sha256((HERE / 'CRITICAL_WINDOW.md').read_bytes()).hexdigest(),
    'sources_sha256': hashlib.sha256((HERE / 'SOURCES.json').read_bytes()).hexdigest(),
    'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}, indent=2, sort_keys=True))
