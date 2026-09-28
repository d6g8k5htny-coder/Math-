"""Independent exact checks for the nonauthor review of Math-#118 (P15 bipartite overlap and even-capacity
extension) and Math-#122 (P15 sharp even reference tail and weighted loads).

Python standard library only; exact rational arithmetic (one group uses 60-digit decimal arithmetic and says so).
Written after reading the authors' suites, but it shares no code with them. Its colouring oracle is a plain
backtracking search over colour assignments of ORIGINAL coordinates, not the authors' constructions. Groups:

  COL   (O2)/(E2)/(T5) chi_D = max ceil(|U^X_i|/a_i) against the oracle: random bipartite systems with arbitrary
        capacities, random read-two NONbipartite systems with even capacities, the E4 triangle (12 shared
        coordinates 4-colourable, all 15 need 5), and the excluded doubled triangle with capacity one (chi = 6 > 4).
  OBS   (O4)/(T6) O_K(D) = union of active full-block containments, by brute force over all subsets, with an inactive
        demand-one block; chi_D(X) = K+1; duplicate and strict-superset generator removal keeps a cover.
  HAZ   (O8)-(O9), (E3), (T11) in exponentiated exact form on random rational product measures: two-sided
        Cauchy-Schwarz, read-q product inequality for arbitrary events, integer-weighted loads; the overlap
        example 5/8 > 9/16; the max-instead-of-sum counterexample.
  TRANS (O5)/(T8) decreasing events are affine in each p_v with nonnegative coefficients; separate concavity
        chord bound checked in 60-digit decimal arithmetic (not exact).
  TAIL  (O6)-(O7), (E5), (T12)-(T16): rational e bounds, s < 1/2, Markov chains, q_5 > 25/512, the exp(7/3)
        certificate, 512/25 > (87/32)^3, the q_9 polynomial identity, both (T15) margins, rigorous enclosures of
        rho_bip and rho_9 inside (O12)/(T2), the uniform even tail with equality only at a=2, K=4, capacity one
        giving q_5 > q_9, and reviewer remark R1: every capacity a >= 2 (odd included) has tail < q_9, where
        a = 3 needs a direct tail because Markov's bound 125/8192 exceeds q_9.

Not a proof of the continuum inequalities: separate concavity, the relative-entropy chain rule and König's
theorem are argued in REVIEW.md.
"""
import argparse
import decimal
import itertools
import json
import random
import sys
from fractions import Fraction as F
from math import comb, factorial

MUTANTS = ("odd-nonbipartite", "charge-inactive", "q-one", "max-load", "interval-swap", "tail-a3",
           "drop-superset-cover")

# ----------------------------------------------------------------------------------------------------------
# Colouring
# ----------------------------------------------------------------------------------------------------------


def formula(U, blocks, caps):
    return max([0] + [-(-len(U & B) // a) for B, a in zip(blocks, caps)])


def chi_oracle(U, blocks, caps):
    """Least k such that U splits into k sets each meeting every block X_i in <= a_i coordinates."""
    U = sorted(U)
    if not U:
        return 0
    memb = {v: [i for i, B in enumerate(blocks) if v in B] for v in U}
    U.sort(key=lambda v: -len(memb[v]))
    lower = max(-(-sum(1 for v in U if i in memb[v]) // a) for i, a in enumerate(caps))  # counting bound
    for k in range(max(1, lower), len(U) + 1):
        load = [[0] * len(blocks) for _ in range(k)]

        def bt(idx, used):
            if idx == len(U):
                return True
            v = U[idx]
            for c in range(min(used + 1, k)):
                if all(load[c][i] < caps[i] for i in memb[v]):
                    for i in memb[v]:
                        load[c][i] += 1
                    if bt(idx + 1, max(used, c + 1)):
                        return True
                    for i in memb[v]:
                        load[c][i] -= 1
            return False

        if bt(0, 0):
            return k
    raise AssertionError("unreachable")


def random_bipartite(rng):
    n = rng.randrange(5, 10)
    nl, nr = rng.randrange(1, 4), rng.randrange(1, 4)
    L = [set() for _ in range(nl)]
    R = [set() for _ in range(nr)]
    for v in range(n):
        side = rng.randrange(3)
        if side in (0, 2):
            L[rng.randrange(nl)].add(v)
        if side in (1, 2):
            R[rng.randrange(nr)].add(v)
    blocks = [B for B in L + R if B]
    caps = [rng.randrange(1, 4) for _ in blocks]
    return n, blocks, caps


def random_read_two(rng, cyc):
    """Blocks are the vertices of an odd cycle; coordinates are cycle edges (shared) or private."""
    blocks = [set() for _ in range(cyc)]
    v = 0
    for i in range(cyc):
        for _ in range(rng.randrange(1, 3)):
            blocks[i].add(v)
            blocks[(i + 1) % cyc].add(v)
            v += 1
        for _ in range(rng.randrange(0, 2)):
            blocks[i].add(v)
            v += 1
    return v, blocks


def check_col(mut):
    rng = random.Random(118)
    out = {}
    ok_bip, ok_even = True, True
    for _ in range(120):
        n, blocks, caps = random_bipartite(rng)
        for _ in range(6):
            U = {x for x in range(n) if rng.random() < 0.7}
            ok_bip &= chi_oracle(U, blocks, caps) == formula(U, blocks, caps)
    for _ in range(80):
        n, blocks = random_read_two(rng, rng.choice((3, 5)))
        caps = [1 if mut == "odd-nonbipartite" else rng.choice((2, 4)) for _ in blocks]
        for _ in range(4):
            U = {x for x in range(n) if rng.random() < 0.8}
            ok_even &= chi_oracle(U, blocks, caps) == formula(U, blocks, caps)
    out["bipartite_arbitrary_capacity_formula_equals_oracle"] = ok_bip
    out["read_two_nonbipartite_even_capacity_formula_equals_oracle"] = ok_even
    # E4 triangle: capacity 2, four shared coordinates per side, one private per block.
    blocks = [set(), set(), set()]
    v = 0
    for i in range(3):
        for _ in range(4):
            blocks[i].add(v)
            blocks[(i + 1) % 3].add(v)
            v += 1
    shared = set(range(v))
    for i in range(3):
        blocks[i].add(v)
        v += 1
    full = set(range(v))
    caps = [2, 2, 2]
    out["E4_triangle_shared_4_full_5"] = (all(len(B) == 9 for B in blocks) and chi_oracle(shared, blocks, caps) == 4
                                          and chi_oracle(full, blocks, caps) == 5)
    # Excluded doubled triangle, capacity one (PROOF.md section 8).
    blocks = [{0, 1, 4, 5, 6}, {0, 1, 2, 3, 7}, {2, 3, 4, 5, 8}]
    U = {0, 1, 2, 3, 4, 5}
    out["doubled_triangle_capacity_one_chi_6_formula_4"] = (chi_oracle(U, blocks, [1, 1, 1]) == 6
                                                           and formula(U, blocks, [1, 1, 1]) == 4
                                                           and not any(B <= U for B in blocks))
    return out


def check_obs(mut):
    out = {}
    # Bipartite: X0 (a=1, d=4, active), X1={4,5} (a=1, d=1, inactive, overlaps both), X2 (a=1, d=4, active).
    blocks = [set(range(0, 5)), {4, 5}, set(range(5, 10))]
    caps, d = [1, 1, 1], [4, 1, 4]
    K = max(d)
    X = set(range(10))
    active = [B for B, di in zip(blocks, d) if di == K]
    charged = blocks if mut == "charge-inactive" else active
    ok = all(len(B) == a * di + 1 for B, a, di in zip(blocks, caps, d))
    for bits in range(1 << 10):
        U = {v for v in range(10) if bits >> v & 1}
        obstruct = chi_oracle(U, blocks, caps) > K
        ok &= obstruct == any(B <= U for B in active)
        if mut == "charge-inactive":
            ok &= obstruct == any(B <= U for B in charged)
    out["O4_exact_obstruction_equals_active_full_blocks"] = ok
    out["chi_whole_ground_K_plus_1"] = chi_oracle(X, blocks, caps) == K + 1
    out["inactive_full_block_not_obstruction"] = chi_oracle(blocks[1], blocks, caps) == 2 <= K
    # Duplicate removal (X0 = X1, read-two, bipartite) and strict-superset removal (X0 inside X1, a = 1 and 2).
    ok = True
    for blocks, caps, keep, drop in (([set(range(5)), set(range(5)), set(range(5, 10))], [1, 1, 1], [0, 2], [1, 2]),
                                     ([set(range(5)), set(range(9))], [1, 2], [0], [1])):
        ok &= all(len(B) == a * 4 + 1 for B, a in zip(blocks, caps))
        n = len(set().union(*blocks))
        retained = [blocks[i] for i in (drop if mut == "drop-superset-cover" and len(blocks) == 2 else keep)]
        for bits in range(1 << n):
            U = {v for v in range(n) if bits >> v & 1}
            ok &= (chi_oracle(U, blocks, caps) > 4) == any(B <= U for B in retained)
    out["duplicate_and_superset_removal_keeps_cover"] = ok
    return out


# ----------------------------------------------------------------------------------------------------------
# Product-measure hazards
# ----------------------------------------------------------------------------------------------------------


def configs(n):
    return [tuple(bits >> v & 1 for v in range(n)) for bits in range(1 << n)]


def measure(p, event, n):
    tot = F(0)
    for x in configs(n):
        if event(x):
            w = F(1)
            for v in range(n):
                w *= p[v] if x[v] else 1 - p[v]
            tot += w
    return tot


def check_haz(mut):
    rng = random.Random(1181)
    out = {}
    # Overlap destroys independence; Cauchy-Schwarz survives.
    p = [F(1, 2)] * 3
    a1 = measure(p, lambda x: x[0] + x[1] <= 1, 3)
    a2 = measure(p, lambda x: x[1] + x[2] <= 1, 3)
    dd = measure(p, lambda x: x[0] + x[1] <= 1 and x[1] + x[2] <= 1, 3)
    out["overlap_5_8_exceeds_9_16_and_CS"] = a1 == a2 == F(3, 4) and dd == F(5, 8) > a1 * a2 and dd ** 2 <= a1 * a2
    ok_cs, ok_rq, ok_w = True, True, True
    for trial in range(150):
        n = rng.randrange(4, 7)
        p = [F(rng.randrange(0, 11), 10) for _ in range(n)]
        # Bipartite capacity system: two disjoint left blocks, two disjoint right blocks.
        perm = list(range(n))
        rng.shuffle(perm)
        cut = rng.randrange(1, n)
        L = [set(perm[:cut]), set(perm[cut:])]
        rng.shuffle(perm)
        cut = rng.randrange(1, n)
        R = [set(perm[:cut]), set(perm[cut:])]
        blocks = L + R
        caps = [rng.randrange(0, 3) for _ in blocks]
        ev = [lambda x, B=B, a=a: sum(x[v] for v in B) <= a for B, a in zip(blocks, caps)]
        mus = [measure(p, e, n) for e in ev]
        muL = measure(p, lambda x: ev[0](x) and ev[1](x), n)
        muR = measure(p, lambda x: ev[2](x) and ev[3](x), n)
        muD = measure(p, lambda x: all(e(x) for e in ev), n)
        ok_cs &= muL == mus[0] * mus[1] and muR == mus[2] * mus[3] and muD ** 2 <= muL * muR
        ok_cs &= muD ** 2 <= mus[0] * mus[1] * mus[2] * mus[3]
        # Read-q with ARBITRARY events on triangle incidence (q = 2): Prod mu(A_i) >= mu(D)^q.
        S = [(0, 1), (1, 2), (2, 0)] + ([(3, 0)] if n > 3 else [])
        q = max(sum(1 for s in S if v in s) for v in range(n))
        tables = [{xy: rng.random() < 0.75 for xy in itertools.product((0, 1), repeat=2)} for _ in S]
        evs = [lambda x, s=s, t=t: t[(x[s[0]], x[s[1]])] for s, t in zip(S, tables)]
        muA = [measure(p, e, n) for e in evs]
        muD = measure(p, lambda x: all(e(x) for e in evs), n)
        qq = 1 if mut == "q-one" else q
        prod = F(1)
        for m in muA:
            prod *= m
        ok_rq &= prod >= muD ** qq
        # Integer-weighted loads (T11): Prod mu(A_i)^{n_i} >= mu(D)^{max_v sum_{i ni v} n_i}.
        wts = [rng.randrange(0, 4) for _ in S]
        if mut == "max-load":
            load = max(max([w for s, w in zip(S, wts) if v in s], default=0) for v in range(n))
        else:
            load = max(sum(w for s, w in zip(S, wts) if v in s) for v in range(n))
        prod = F(1)
        for m, w in zip(muA, wts):
            prod *= m ** w
        ok_w &= prod >= muD ** load
    # Max-instead-of-sum counterexample: two identical events on one fair coordinate.
    mA = measure([F(1, 2)], lambda x: x[0] == 0, 1)
    load = 1 if mut == "max-load" else 2
    ok_w &= mA * mA >= mA ** load
    out["two_sided_cauchy_schwarz_bipartite"] = ok_cs
    out["read_q_product_inequality_arbitrary_events"] = ok_rq
    out["weighted_load_sum_not_max"] = ok_w
    return out


def check_trans(mut):
    rng = random.Random(1182)
    out = {}
    ok_aff = True
    for _ in range(120):
        n = rng.randrange(2, 6)
        gens = [frozenset(v for v in range(n) if rng.random() < 0.5) for _ in range(3)]
        # decreasing event: the configuration contains no nonempty generator
        down = lambda x, gens=gens: not any(g and all(x[v] for v in g) for g in gens)
        p = [F(rng.randrange(0, 11), 10) for _ in range(n)]
        j = rng.randrange(n)
        vals = []
        for pj in (F(0), F(1, 3), F(1)):
            pp = list(p)
            pp[j] = pj
            vals.append(measure(pp, down, n))
        P0, P1 = vals[0], vals[2]  # coordinate j forced absent / present
        ok_aff &= P0 >= P1 >= 0 and vals[1] == P1 + (P0 - P1) * (1 - F(1, 3))
    out["decreasing_event_affine_nonneg_coefficients"] = ok_aff
    # Separate-concavity chord bound F(t) >= H prod t, 60-digit decimal (numerical, not exact).
    ctx = decimal.Context(prec=60)
    D = decimal.Decimal
    ok = True
    for _ in range(60):
        n = rng.randrange(2, 5)
        a = rng.randrange(0, n)
        t = [D(rng.randrange(1, 101)) / D(100) for _ in range(n)]
        pt = [1 - ctx.exp(-x) for x in t]
        p1 = 1 - ctx.exp(D(-1))

        def mu(pv):
            tot = D(0)
            for x in configs(n):
                if sum(x) <= a:
                    w = D(1)
                    for v in range(n):
                        w *= pv[v] if x[v] else 1 - pv[v]
                    tot += w
            return tot

        Ft = -ctx.ln(mu(pt))
        H = -ctx.ln(mu([p1] * n))
        prod = D(1)
        for x in t:
            prod *= x
        ok &= Ft >= H * prod - D(10) ** -50
    out["separate_concavity_chord_decimal60"] = ok
    return out


# ----------------------------------------------------------------------------------------------------------
# Reference tails and certificates
# ----------------------------------------------------------------------------------------------------------


def e_bounds(N):
    s = sum(F(1, factorial(j)) for j in range(N + 1))
    return s, s + F(1, factorial(N) * N)


def round_out(x, down):
    den = 10 ** 45
    num = (x.numerator * den) // x.denominator
    return F(num if down else num + 1, den)


def log_enclosure(x, m=60):
    """Rigorous [lo, hi] for log x, rational x >= 1, via x = 2^j y and the atanh series with remainder."""
    assert x >= 1
    j = 0
    while x >= 2:
        x /= 2
        j += 1

    def atanh2(y):
        t = (y - 1) / (y + 1)
        s = 2 * sum(t ** (2 * k + 1) / (2 * k + 1) for k in range(m))
        return s, s + 2 * t ** (2 * m + 1) / ((2 * m + 1) * (1 - t * t))

    l2lo, l2hi = atanh2(F(2))
    ylo, yhi = atanh2(x)
    return j * l2lo + ylo, j * l2hi + yhi


def binom_le(n, p, a):
    return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(a + 1))


def check_tail(mut):
    out = {}
    l, u = F(1957, 720), F(87, 32)
    eu6 = l + F(1, factorial(7)) * F(8, 7)
    out["e_bounds_series"] = (l == sum(F(1, factorial(j)) for j in range(7)) and eu6 == F(31967, 11760)
                              and F(8, 3) < l < eu6 < u < F(11, 4))
    el, eh = e_bounds(40)
    out["e_bounds_consistent_with_tight"] = l < el < eh < F(31967, 11760)
    s_at = lambda e: (e + 4) / (5 * e)
    out["s_below_half_from_e_above_8_3"] = s_at(F(8, 3)) == F(1, 2) and s_at(eh) < F(1, 2)
    out["markov_chain_a_ge_2_and_a_ge_4"] = (all(F(1, 2) * F(5, 16) ** a <= F(25, 512) for a in range(2, 60))
                                             and all(F(1, 2) * F(5, 16) ** a <= F(625, 131072)
                                                     for a in range(4, 60, 2))
                                             and all(5 ** a * F(1, 2) ** (4 * a + 1) == F(1, 2) * F(5, 16) ** a
                                                     for a in range(1, 30)))
    q5lo = F(28, 3) * F(4, 11) ** 5
    out["q5_above_25_512_margin"] = q5lo - F(25, 512) == F(2601239, 247374336) > 0
    out["exp_7_3_certificate"] = (sum(F(7, 3) ** j / factorial(j) for j in range(7)) - F(307, 32)
                                  == F(129055, 209952) and 5 * u - 4 == F(307, 32))
    out["512_25_exceeds_87_32_cubed"] = F(512, 25) - u ** 3 == F(314641, 819200)
    # q_9 identity as a polynomial identity in e (y = 1/e): Bin(9, 1-y) <= 2.
    ok = True
    for e in (F(5, 2), F(11, 4), F(271, 100), F(3)):
        y = 1 / e
        lhs = binom_le(9, 1 - y, 2)
        ok &= lhs == (36 * e * e - 63 * e + 28) / e ** 9 == y ** 9 * (1 + 9 * (e - 1) + 36 * (e - 1) ** 2)
    out["q9_polynomial_identity"] = ok
    Pz = lambda z: 36 * z * z - 63 * z + 28
    lo9, hi9 = Pz(l) / u ** 9, Pz(u) / l ** 9
    if mut == "interval-swap":
        hi9 = Pz(l) / u ** 9
    tlo, thi = Pz(el) / eh ** 9, Pz(eh) / el ** 9
    out["T15_margins_exact"] = (lo9 - F(625, 131072) == F(87187623163627321174969, 8421039761612032386662400)
                                and F(1, 64) - Pz(u) / l ** 9
                                == F(12311490319341451572976881157, 26946192308072632700222520394048))
    out["T15_interval_directions"] = (72 * l - 63 > 0 and lo9 <= tlo and thi <= hi9 and lo9 < hi9
                                      and F(625, 131072) < lo9 and hi9 < F(1, 64))
    out["log2_above_2_3"] = F(11, 4) ** 2 < 8
    # Rigorous enclosures of rho_bip and rho_9 lie inside the published ones.
    x_lo, x_hi = round_out(5 * el - 4, True), round_out(5 * eh - 4, False)
    lg_lo, _ = log_enclosure(x_lo)
    _, lg_hi = log_enclosure(x_hi)
    rb = (2 / (5 - lg_lo), 2 / (5 - lg_hi))
    P_lo, P_hi = round_out(Pz(el), True), round_out(Pz(eh), False)
    lq_lo, _ = log_enclosure(P_lo)
    _, lq_hi = log_enclosure(P_hi)
    r9 = (2 / (9 - lq_lo), 2 / (9 - lq_hi))
    out["rho_bip_inside_O12"] = (F("0.73015826409534942932") < rb[0] <= rb[1] < F("0.73015826409534942934")
                                 and rb[1] < F(3, 4))
    out["rho_9_inside_T2"] = (F("0.47734798895766998533") < r9[0] <= r9[1] < F("0.47734798895766998534")
                              and r9[1] < F(1, 2))
    # Uniform even tail (T13): rigorous upper bound on P(Bin(aK+1, p*) <= a) via p* > 1 - 1/el.
    p_lo, p_hi = 1 - 1 / el, 1 - 1 / eh
    q9_lo = binom_le(9, p_hi, 2)
    ok_even = True
    for a in range(2, 11, 2):
        for K in range(4, 9):
            if (a, K) == (2, 4):
                continue
            ok_even &= binom_le(a * K + 1, p_lo, a) < q9_lo
    # Capacity one is NOT covered by q_9 (it gives q_5), which is why rho_9 excludes it.
    q5_lo = binom_le(5, p_hi, 1)
    q9_hi = binom_le(9, p_lo, 2)
    out["uniform_even_tail_max_only_at_a2_K4"] = ok_even
    out["capacity_one_tail_q5_exceeds_q9"] = q5_lo > q9_hi
    # Reviewer remark R1: every capacity a >= 2, odd included, has reference tail < q_9 for K >= 4. For a = 3
    # Markov's bound (1/2)(5/16)^3 = 125/8192 EXCEEDS q_9, so a direct tail (monotone in n, n >= 13) is needed.
    markov_a3 = F(1, 2) * F(5, 16) ** 3
    direct_a3 = markov_a3 if mut == "tail-a3" else binom_le(13, p_lo, 3)
    out["R1_a3_markov_insufficient_direct_tail_below_q9"] = markov_a3 > q9_hi and direct_a3 < q9_lo
    out["R1_a3_monotone_in_trials"] = all(binom_le(n + 1, p_lo, 3) <= binom_le(n, p_lo, 3) for n in range(13, 40))
    out["R1_odd_a_ge_5_markov_below_q9"] = all(F(1, 2) * F(5, 16) ** a < q9_lo for a in range(5, 61, 2))
    # Five-trial reference: q_5 = e^-5 (5e-4) as a polynomial identity.
    ok = True
    for e in (F(5, 2), F(11, 4), F(3)):
        ok &= binom_le(5, 1 - 1 / e, 1) == (5 * e - 4) / e ** 5
    out["q5_polynomial_identity"] = ok
    # a = 1 branch: monotone in n.
    out["a1_monotone_in_trials"] = all(binom_le(n + 1, p_lo, 1) <= binom_le(n, p_lo, 1) for n in range(5, 30))
    return out


def flatten(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from flatten(v)
        else:
            yield v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    mut = ap.parse_args().mutant
    checks = {"COL_colouring": check_col(mut), "OBS_obstruction_cover": check_obs(mut),
              "HAZ_product_hazards": check_haz(mut), "TRANS_local_transfer": check_trans(mut),
              "TAIL_reference_tails": check_tail(mut)}
    passed = all(flatten(checks))
    print(json.dumps({"checks": checks, "passed": passed, "scientific_effect": "NONE",
                      "scope": "exact identities, brute-force colouring oracle and exact product-measure "
                               "inequalities on finite instances; one 60-digit decimal check; the continuum "
                               "arguments are in REVIEW.md"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
