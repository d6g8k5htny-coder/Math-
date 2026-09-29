"""Finite companion for CL-C6-PALM-20260929-v1 (PROOF.md). Standard library only; exact rational arithmetic.

Groups (all exact):
  PK  slab-excluded packing of Lemma M' (b): retained radii count >= eta'/(4 delta); retained balls lie in the annulus
      {eta'/2 <= |z - c| <= 3 eta'}; every point of a retained ball is at distance >= zeta_0/2 from every point at
      distance rho_X from the centre. Grids of rho_X, both radii eta_0 = eta and eta_j = eta/8, delta = 2^(1-m).
  EX  exponent arithmetic of Lemma M' for d = 2..6 with lambda = 2^(m/(4d)): Markov term exponent -1/2, truncation
      exponent -1/(2d), final exponent -1/(2d).
  TL  moment series of Proposition 4.5: least index M_0 from which the summand ratio of
      a_m = (m+1)^(pd-1) m 2^(-m/(2d)) is at most 2^(-1/(4d)), as the exact rational inequality
      [((m+2)/(m+1))^(pd-1) (m+1)/m]^(4d) <= 2, for d = 2..6 and p = 1..4.
  PW  pathwise inequalities (3.4): N(N-1) <= N Psi and (N)_q <= N Psi^(q-1) for integers 0 <= N <= Psi - 2, q = 2..5.
  SC  Schur-complement floor (Lemma 4.2) on random rational matrices M = A A^T + c I (positivity of the Schur
      complement minus c I certified by exact LDL^T), and the residual-metric domination of Lemma 4.3.
  LG  regime ledger of section 6 for d = 2..6: radial exponents unchanged from [DL]; absorption powers of R1 region II
      (2n >= 6 + 3d) and R2a (2n/3 >= 15 + 39d) including the two mark factors.

Mutants (each must exit 1): no-slab, lambda-too-large, series-ratio, factorial-power, schur-upper, forget-mark-power.
"""
import argparse
import json
import random
import sys
from fractions import Fraction as F

MUTANTS = ['no-slab', 'lambda-too-large', 'series-ratio', 'factorial-power', 'schur-upper', 'forget-mark-power']
MUT = None
RNG = random.Random(20260929)


def require(cond, msg):
    if not cond:
        raise AssertionError(msg)


# ----------------------------------------------------------------------------------------------------------- matrices

def rand_frac(lo=-3, hi=3, den=4):
    return F(RNG.randint(lo * den, hi * den), den)


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def transpose(A):
    return [list(r) for r in zip(*A)]


def ident(n, c=F(1)):
    return [[c if i == j else F(0) for j in range(n)] for i in range(n)]


def sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def inverse(A):
    n = len(A)
    M = [list(A[i]) + [F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        M[col] = [x / p for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def is_psd(S):
    """Exact LDL^T with pivoting on the diagonal: PSD iff every pivot is >= 0 (zero pivots need a zero row)."""
    n = len(S)
    A = [list(r) for r in S]
    for k in range(n):
        if A[k][k] < 0:
            return False
        if A[k][k] == 0:
            if any(A[k][j] != 0 for j in range(k + 1, n)):
                return False
            continue
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] -= f * A[k][j]
    return True


# ------------------------------------------------------------------------------------------------------------ PK group

def check_pk(out):
    eta = F(1)
    zeta0 = eta / 64
    total_cases = 0
    for etap in (eta, eta / 8):
        require(zeta0 <= etap / 4, 'zeta_0 exceeds eta_j/4')
        for m in (8, 10, 12):
            delta = F(2) ** (1 - m)
            require(delta <= zeta0 / 2 and delta <= etap / 8, 'm_0 condition violated in the test grid')
            imax = int(etap / (2 * delta))
            radii = [etap + 2 * i * delta for i in range(imax + 1)]
            for rho_X in [F(k, 32) * etap for k in range(0, 4 * 32 + 1)]:
                if MUT == 'no-slab':
                    retained = radii
                else:
                    retained = [rho for rho in radii if abs(rho - rho_X) >= zeta0]
                require(len(retained) >= etap / (4 * delta), 'retained count below eta\'/(4 delta)')
                for rho in retained:
                    require(rho - delta >= etap / 2 and rho + delta <= 3 * etap, 'retained ball leaves the annulus')
                    # a point of the ball has | |z-c| - rho_X | >= |rho - rho_X| - delta; require >= zeta_0/2
                    require(abs(rho - rho_X) - delta >= zeta0 / 2, 'retained ball within zeta_0/2 of the witness sphere')
                for a, b in zip(retained, retained[1:]):
                    require(b - a >= 2 * delta, 'retained balls not disjoint')
                total_cases += 1
    out['pk_cases'] = total_cases
    out['pk_zeta0_over_eta'] = str(zeta0 / eta)


# ------------------------------------------------------------------------------------------------------------ EX group

def check_ex(out):
    for d in range(2, 7):
        lam_exp = F(1, 4 * d) if MUT != 'lambda-too-large' else F(1, 2 * d)     # lambda = 2^(m * lam_exp)
        markov = 2 * d * lam_exp - 1                                             # lambda^(2d) 2^(-m) = 2^(m * markov)
        trunc = -2 * lam_exp                                                     # lambda^(-2)
        require(markov < 0, 'Markov term does not decay in d=%d' % d)
        require(markov == F(-1, 2), 'Markov exponent is not -1/2 in d=%d' % d)
        require(trunc == F(-1, 2 * d), 'truncation exponent is not -1/(2d) in d=%d' % d)
        final = max(markov, trunc)
        require(final == F(-1, 2 * d), 'final exponent is not -1/(2d) in d=%d' % d)
        out['ex_markov_exponent_d%d' % d] = str(markov)
        out['ex_truncation_exponent_d%d' % d] = str(trunc)
        out['ex_final_exponent_d%d' % d] = str(final)


# ------------------------------------------------------------------------------------------------------------ TL group

def check_tl(out):
    target = F(2) if MUT != 'series-ratio' else F(1)
    for d in range(2, 7):
        for p in range(1, 5):
            e = p * d - 1
            found = None
            for m in range(1, 20001):
                ratio = (F(m + 2, m + 1) ** e) * F(m + 1, m)
                if ratio ** (4 * d) <= target:
                    # monotone: the ratio decreases in m, so all later indices satisfy it too
                    found = m
                    break
            require(found is not None, 'no index makes the series ratio fall below 2^(-1/(4d)) for d=%d p=%d' % (d, p))
            r2 = (F(found + 3, found + 2) ** e) * F(found + 2, found + 1)
            require(r2 ** (4 * d) <= target, 'ratio not monotone at the found index')
            out['tl_index_d%d_p%d' % (d, p)] = found


# ------------------------------------------------------------------------------------------------------------ PW group

def falling(n, q):
    v = 1
    for i in range(q):
        v *= (n - i)
    return v


def check_pw(out):
    cases = 0
    for psi in range(2, 13):
        for n in range(0, psi - 1):
            require(n * (n - 1) <= n * psi, 'N(N-1) <= N Psi fails')
            for q in range(2, 6):
                power = q - 1 if MUT != 'factorial-power' else q - 2
                require(falling(n, q) <= n * psi ** power, '(N)_q <= N Psi^(q-1) fails at N=%d Psi=%d q=%d' % (n, psi, q))
                cases += 1
    out['pw_cases'] = cases


# ------------------------------------------------------------------------------------------------------------ SC group

def check_sc(out):
    trials = 0
    for _ in range(12):
        n1, n2 = RNG.randint(1, 4), RNG.randint(1, 4)
        n = n1 + n2
        A = [[rand_frac() for _ in range(n + 1)] for _ in range(n)]
        c0 = F(RNG.randint(1, 8), 8)
        M = [[x + (c0 if i == j else 0) for j, x in enumerate(row)] for i, row in enumerate(matmul(A, transpose(A)))]
        require(is_psd(sub(M, ident(n, c0))), 'M - c I is not PSD by construction')
        M11 = [r[:n1] for r in M[:n1]]
        M12 = [r[n1:] for r in M[:n1]]
        M21 = [r[:n1] for r in M[n1:]]
        M22 = [r[n1:] for r in M[n1:]]
        S = sub(M11, matmul(matmul(M12, inverse(M22)), M21))
        if MUT == 'schur-upper':
            require(is_psd(sub(ident(n1, c0), S)), 'Schur complement is not bounded above by c I')
        else:
            require(is_psd(sub(S, ident(n1, c0))), 'Schur complement is not bounded below by c I')
        # residual metric domination: Gamma' = Gamma - C C^T; increments of Gamma' are at most those of Gamma
        Cm = [[rand_frac() for _ in range(3)] for _ in range(n)]
        Gp = sub(M, matmul(Cm, transpose(Cm)))
        for s in range(n):
            for t in range(n):
                inc = M[s][s] + M[t][t] - 2 * M[s][t]
                incp = Gp[s][s] + Gp[t][t] - 2 * Gp[s][t]
                diff = sum((Cm[s][k] - Cm[t][k]) ** 2 for k in range(3))
                require(inc - incp == diff and incp <= inc, 'residual increment is not dominated')
        trials += 1
    out['sc_trials'] = trials


# ------------------------------------------------------------------------------------------------------------ LG group

def check_lg(out):
    for d in range(2, 7):
        # radial ledgers inherited from [DL]: unchanged by the mark
        pin_I = -2 - (d + 1) + 6 + d
        collar = -2 - (d + 1) + 6 + d
        shell_r = -2 + 2 + 3
        shell_s = -(d + 4) + 2 + d
        require(pin_I == 3 and collar == 3 and shell_r == 3 and shell_s == -2, 'radial ledger changed in d=%d' % d)
        out['lg_pin_region_I_r_exponent_d%d' % d] = pin_I
        out['lg_shell_s_exponent_d%d' % d] = shell_s
        # R1 region II: unmarked pointwise -2-4d ([DL] (4.12)); mark factor (1+chi) <= 2/r adds -1
        mark_II = -1 if MUT != 'forget-mark-power' else 0
        pII = -2 - 4 * d + mark_II
        needII = (3 - d) - pII                       # 2n >= needII
        require(needII == 6 + 3 * d, 'R1 region II absorption power is not 6+3d in d=%d' % d)
        out['lg_R1_II_absorption_2n_at_least_d%d' % d] = needII
        # R2a: Z^-1 (-2), density (-5d), K^(6d) half-moment (-30d), mark (1+beta+Phi^(1/2)) <= C r^(-10-5d)
        mark_2a = (-10 - 5 * d) if MUT != 'forget-mark-power' else 0
        p2a = -2 - 5 * d - 30 * d + mark_2a
        need2a = (3 - d) - p2a                       # 2n/3 >= need2a
        require(need2a == 15 + 39 * d, 'R2a absorption power is not 15+39d in d=%d' % d)
        out['lg_R2a_absorption_2n_over_3_at_least_d%d' % d] = need2a
        # R2b and R3b: |v|-exponents of the marked intensity (absorbed by exp(-c/|v|^2)); recorded, finite
        out['lg_R2b_v_exponent_d%d' % d] = -(16 * d + 10)
        out['lg_R3b_v_exponent_d%d' % d] = -(22 * d + 15)


# --------------------------------------------------------------------------------------------------------------- main

def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', choices=MUTANTS)
    MUT = ap.parse_args().mutant
    out = {}
    groups = [('PK', check_pk), ('EX', check_ex), ('TL', check_tl), ('PW', check_pw), ('SC', check_sc), ('LG', check_lg)]
    checks = {}
    for name, fn in groups:
        fn(out)
        checks[name] = True
    result = {
        'object': 'CL-C6-PALM-20260929-v1',
        'checks': checks,
        'ledgers': out,
        'passed': all(checks.values()) and len(checks) == 6,
        'scientific_effect': 'NONE',
        'scope': 'exact counting, exponent, identity and finite-matrix checks only; the analytic proof is PROOF.md',
    }
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
