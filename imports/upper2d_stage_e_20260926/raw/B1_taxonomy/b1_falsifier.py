#!/usr/bin/env python3
# b1_falsifier.py — executable falsifier for the B1 elder-rule failure taxonomy
# (U2D-UPPER work-order items 72-90, Stage B).
#
# Model: deterministic PL elder-rule persistence on a triangulated torus grid
# (6-neighbor lower-star/upper-link model). Vertex "heights" carry an exact
# lexicographic key (value, index), which is the discrete analogue of the
# a.s.-distinct-critical-values regularity event Reg: no ties exist in the
# model, exactly as on Reg in the continuous theorem.
#
# For every tested pair (Mv max, Sv PL-saddle with >=2 upper-link clusters,
# key(Sv) < key(Mv)) the script:
#   (1) computes the exact elder-rule death partner D(Mv) by union-find;
#   (2) evaluates the taxonomy categories as exact set membership:
#         A   = path form (preemption): component of Mv in {key > key(Sv)}
#               contains a vertex with key > key(Mv);
#         B1  = not A; every upper-link cluster of Sv lies in C (Mv's
#               component of {key > key(Sv)});
#         B2  = not A; C is one cluster-component and every other
#               cluster-component has birth key < key(Mv);
#         B4  = not A; no upper-link cluster of Sv lies in C;
#         success = not A; C is a cluster-component and some other
#               cluster-component has birth key > key(Mv);
#         tie B3: impossible in the model (distinct keys) -- checked.
#   (3) KILLS (exit 1) if any failure (D(Mv) != Sv) is covered by NO category,
#       or if any category fires on a success pair, or if the at-level sector
#       analysis disagrees with the exact union-find pairing, or if the path
#       form of A disagrees with the union-find death level.
#
# Fail-closed: ck() exits nonzero; no bare asserts (python -O safe).
# Deterministic: fixed seeds, sorted iteration, no floats in the digest.

import hashlib
import math
import random
import sys

N = 40  # torus grid side; vertices 0..N*N-1, vertex v = (i, j) = divmod(v, N)
V = N * N


def ck(cond, msg):
    if not cond:
        print("B1-FALSIFIER FIRED:", msg)
        raise SystemExit(1)


def ring(v):
    # the six neighbors of v in cyclic order (triangulation diagonal (i,j)-(i+1,j+1))
    i, j = divmod(v, N)
    return [
        ((i + 1) % N) * N + j,
        ((i + 1) % N) * N + ((j + 1) % N),
        i * N + ((j + 1) % N),
        ((i - 1) % N) * N + j,
        ((i - 1) % N) * N + ((j - 1) % N),
        i * N + ((j - 1) % N),
    ]


RING = [ring(v) for v in range(V)]


class Field:
    # values: list of floats; key(v) = (values[v], v) is a total order, no ties.
    def __init__(self, values, tag):
        ck(len(values) == V, "field %s: wrong size" % tag)
        self.values = values
        self.tag = tag

    def key(self, v):
        return (self.values[v], v)

    def gt(self, a, b):
        return self.key(a) > self.key(b)


def components_above(f, threshold_vertex):
    # connected components of {w : key(w) > key(threshold_vertex)} in the
    # 6-neighbor torus graph; returns comp_id list (-1 below threshold),
    # and per-component max key.
    tkey = f.key(threshold_vertex)
    comp = [-1] * V
    maxkey = []
    for s in range(V):
        if comp[s] != -1 or f.key(s) <= tkey:
            continue
        cid = len(maxkey)
        stack = [s]
        comp[s] = cid
        mk = f.key(s)
        while stack:
            x = stack.pop()
            if f.key(x) > mk:
                mk = f.key(x)
            for u in RING[x]:
                if comp[u] == -1 and f.key(u) > tkey:
                    comp[u] = cid
                    stack.append(u)
        maxkey.append(mk)
    return comp, maxkey


def upper_link_clusters(f, v):
    # clusters of strictly-higher ring neighbors, cyclic runs merged
    ks = [f.key(u) > f.key(v) for u in RING[v]]
    if not any(ks):
        return []
    if all(ks):
        return [list(range(6))]
    start = 0
    while ks[start]:
        start += 1
    clusters = []
    run = []
    for t in range(1, 7):
        idx = (start + t) % 6
        if ks[idx]:
            run.append(idx)
        elif run:
            clusters.append(run)
            run = []
    if run:
        clusters.append(run)
    return clusters


def persistence(f):
    # exact PL elder-rule pairing by descending insertion.
    # returns die_partner[max_vertex] = saddle vertex or None (essential),
    # and die_level key.
    order = sorted(range(V), key=lambda v: f.key(v), reverse=True)
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    active = [False] * V
    birth_vertex = [None] * V  # per root: the maximum vertex birthing it
    die_partner = {}
    die_level = {}
    for v in order:
        active[v] = True
        roots = sorted({find(u) for u in RING[v] if active[u]})
        if not roots:
            parent[v] = v
            birth_vertex[v] = v  # local maximum: component born
            continue
        eldest = max(roots, key=lambda r: f.key(birth_vertex[r]))
        for r in roots:
            if r != eldest:
                mv = birth_vertex[r]
                die_partner[mv] = v
                die_level[mv] = f.key(v)
                parent[r] = eldest
        parent[v] = eldest
    return die_partner, die_level


def classify_pair(f, Mv, Sv, die_partner, die_level):
    # returns (outcome, category) with outcome in {"success", "failure"};
    # category in {None, "A", "B1", "B2", "B3", "B4"}; plus consistency cks.
    ck(f.gt(Mv, Sv), "field %s: pair order violated" % f.tag)
    DM = die_partner.get(Mv)
    failure = (DM != Sv)
    comp, maxkey = components_above(f, Sv)
    C = comp[Mv]
    ck(C >= 0, "field %s: M not above S level" % f.tag)

    # --- Category A, path form (exact discrete analogue of Theorem T1(b))
    A = maxkey[C] > f.key(Mv)

    # cross-check A against union-find death level (Theorem T1(a)<->(b))
    if DM is not None:
        dies_strictly_above = die_level[Mv] > f.key(Sv)
    else:
        dies_strictly_above = False
    ck(A == dies_strictly_above,
       "field %s pair (%d,%d): path form/union-find mismatch for A"
       % (f.tag, Mv, Sv))
    if A:
        ck(failure, "field %s pair (%d,%d): A fired but D(M)==S" % (f.tag, Mv, Sv))
        return ("failure", "A")

    # --- not A: sector analysis at Sv exactly at level f(Sv)
    clusters = upper_link_clusters(f, Sv)
    ck(len(clusters) >= 2, "field %s: Sv %d not a PL saddle" % (f.tag, Sv))
    comp_ids = []
    for cl in clusters:
        ids = {comp[RING[Sv][k]] for k in cl}
        ck(len(ids) == 1, "field %s: cluster split across components" % f.tag)
        comp_ids.append(ids.pop())
    births = [maxkey[c] for c in comp_ids]

    # tie check: a foreign cluster component with birth exactly equal to
    # key(Mv) would be B3; distinct keys make it impossible unless it is C.
    for c in comp_ids:
        if c != C:
            ck(maxkey[c] != f.key(Mv),
               "field %s pair (%d,%d): tie B3 realized in a distinct-key model"
               % (f.tag, Mv, Sv))

    if C not in comp_ids:
        category = "B4"
        predicted_success = False
    elif all(c == C for c in comp_ids):
        category = "B1"
        predicted_success = False
    else:
        others = [births[k] for k in range(len(clusters)) if comp_ids[k] != C]
        if max(others) > f.key(Mv):
            category = None
            predicted_success = True
        else:
            category = "B2"
            predicted_success = False

    # the sector analysis must agree exactly with the union-find pairing
    ck(predicted_success == (not failure),
       "field %s pair (%d,%d): sector/union-find disagreement (pred=%s, D(M)=%s)"
       % (f.tag, Mv, Sv, predicted_success, DM))
    if failure:
        ck(category in ("B1", "B2", "B4"),
           "field %s pair (%d,%d): FAILURE COVERED BY NO CATEGORY"
           % (f.tag, Mv, Sv))
        return ("failure", category)
    ck(category is None,
       "field %s pair (%d,%d): category %s fired on a success pair"
       % (f.tag, Mv, Sv, category))
    return ("success", None)


def is_local_max(f, v):
    return all(f.gt(v, u) for u in RING[v])


def cheb(a, b):
    i, j = divmod(a, N)
    k, l = divmod(b, N)
    di = min((i - k) % N, (k - i) % N)
    dj = min((j - l) % N, (l - j) % N)
    return max(di, dj)


def fourier_field(seed, tag, ridge=False):
    rng = random.Random(seed)
    modes = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2), (2, 2), (3, 0), (0, 3)]
    coef = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in modes]
    vals = []
    for v in range(V):
        i, j = divmod(v, N)
        x = 2.0 * math.pi * i / N
        y = 2.0 * math.pi * j / N
        s = 0.0
        for (kx, ky), (a, b) in zip(modes, coef):
            s += a * math.cos(kx * x + ky * y) + b * math.sin(kx * x + ky * y)
        vals.append(s)
    if ridge:
        # plant a closed high ridge ring: creates preemption (A) failures
        c0, r0 = N // 2, N // 4
        for v in range(V):
            i, j = divmod(v, N)
            di = min((i - c0) % N, (c0 - i) % N)
            dj = min((j - c0) % N, (c0 - j) % N)
            d = max(di, dj)
            if d == r0:
                vals[v] += 6.0
            elif d < r0:
                vals[v] += 1.0
    return Field(vals, tag)


def base_field(tag):
    # low deterministic background with exact distinct keys
    return Field([1e-6 * v for v in range(V)], tag)


def carve(f, i, j, value):
    f.values[(i % N) * N + (j % N)] = value


def synthetic_fields():
    out = []

    # T-SUCCESS (control): M=10, saddle S=6 between M and a higher max M2=12.
    f = base_field("T-SUCCESS")
    carve(f, 10, 10, 10.0)          # Mv
    carve(f, 10, 12, 6.0)           # Sv: two upper clusters (left arm, right arm)
    carve(f, 10, 11, 8.0)           # arm from Sv to M
    carve(f, 10, 13, 9.0)           # arm from Sv to M2
    carve(f, 10, 14, 12.0)          # M2
    out.append((f, (10 * N + 10), (10 * N + 12), "success"))

    # T-A (preemption, LPW-type): M=10, S=6 adjacent, but a ridge above 6
    # joins M to a point of height 11 > b. Death must occur strictly above 6.
    f = base_field("T-A")
    carve(f, 20, 20, 10.0)          # Mv
    carve(f, 20, 22, 6.0)           # Sv
    carve(f, 20, 21, 7.0)           # arm M->S
    carve(f, 19, 22, 6.5)           # second upper neighbor of Sv (low local max)
    carve(f, 19, 20, 9.5)           # ridge start at M upward
    carve(f, 18, 20, 9.6)
    carve(f, 17, 20, 11.0)          # point above b: f > 10
    out.append((f, (20 * N + 20), (20 * N + 22), "A"))

    # T-B1 (self-attachment at S): two arms from M loop around and meet at S;
    # both upper clusters of S lie in M's own component. S creates a loop.
    f = base_field("T-B1")
    carve(f, 30, 30, 10.0)          # Mv
    carve(f, 30, 31, 9.0)           # arm 1: M -> (32,33)
    carve(f, 30, 32, 8.0)
    carve(f, 30, 33, 7.5)
    carve(f, 31, 33, 7.3)
    carve(f, 32, 33, 7.0)           # ring neighbor (idx 2) of Sv
    carve(f, 31, 30, 9.1)           # arm 2: M -> (33,32)
    carve(f, 32, 30, 8.1)
    carve(f, 33, 30, 7.6)
    carve(f, 33, 31, 7.2)
    carve(f, 33, 32, 7.1)           # ring neighbor (idx 0) of Sv
    carve(f, 32, 32, 6.0)           # Sv: both upper clusters lie in C (loop)
    out.append((f, (30 * N + 30), (32 * N + 32), "B1"))

    # T-B2 (younger other side): M=10 reaches S=6; S's other cluster leads
    # only to M2=8 < 10. M survives S.
    f = base_field("T-B2")
    carve(f, 5, 5, 10.0)            # Mv
    carve(f, 5, 7, 6.0)             # Sv
    carve(f, 5, 6, 8.5)             # arm M->S
    carve(f, 5, 8, 7.5)             # arm S->M2
    carve(f, 5, 9, 8.0)             # M2, younger than M
    out.append((f, (5 * N + 5), (5 * N + 7), "B2"))

    # T-B4 (remote saddle): M=10 isolated; Sv=6 far away between two other
    # maxima 8 and 9. Neither cluster of S touches M's component.
    f = base_field("T-B4")
    carve(f, 8, 8, 10.0)            # Mv, isolated
    carve(f, 25, 25, 8.0)           # M-left
    carve(f, 25, 27, 6.0)           # Sv
    carve(f, 25, 26, 7.0)
    carve(f, 25, 28, 7.0)
    carve(f, 25, 29, 9.0)           # M-right
    out.append((f, (8 * N + 8), (25 * N + 27), "B4"))

    return out


def main():
    tally = {"A": 0, "B1": 0, "B2": 0, "B3": 0, "B4": 0, "success": 0}
    lines = []

    # --- synthetic non-vacuity witnesses: each category must be realizable
    for f, Mv, Sv, expect in synthetic_fields():
        die_partner, die_level = persistence(f)
        ck(is_local_max(f, Mv), "%s: carved M is not a local max" % f.tag)
        cl = upper_link_clusters(f, Sv)
        ck(len(cl) >= 2, "%s: carved S is not a PL saddle" % f.tag)
        outcome, category = classify_pair(f, Mv, Sv, die_partner, die_level)
        if expect == "success":
            ck(outcome == "success", "%s: control pair misread as failure" % f.tag)
            tally["success"] += 1
        else:
            ck(outcome == "failure" and category == expect,
               "%s: expected %s, got %s/%s" % (f.tag, expect, outcome, category))
            tally[category] += 1
        lines.append("synthetic %s -> %s/%s" % (f.tag, outcome, category))

    # --- random ensemble: every close (max, saddle) pair audited
    nfail = 0
    npair = 0
    for seed in range(40):
        f = fourier_field(1000 + seed, "ens-%d" % seed, ridge=(seed % 3 == 0))
        die_partner, die_level = persistence(f)
        maxima = [v for v in range(V) if is_local_max(f, v)]
        saddles = [v for v in range(V) if not is_local_max(f, v)
                   and len(upper_link_clusters(f, v)) >= 2]
        for Mv in sorted(maxima):
            for Sv in sorted(saddles):
                if not f.gt(Mv, Sv) or cheb(Mv, Sv) > 4:
                    continue
                npair += 1
                outcome, category = classify_pair(f, Mv, Sv, die_partner, die_level)
                if outcome == "failure":
                    nfail += 1
                    tally[category] += 1
                else:
                    tally["success"] += 1
    lines.append("ensemble pairs audited: %d; failures: %d" % (npair, nfail))
    ck(npair > 0, "ensemble produced no pairs: falsifier is vacuous")
    ck(nfail > 0, "ensemble produced no failures: falsifier is weak")
    lines.append("tally A=%d B1=%d B2=%d B4=%d success=%d"
                 % (tally["A"], tally["B1"], tally["B2"], tally["B4"],
                    tally["success"]))

    body = "\n".join(lines) + "\n"
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    print(body, end="")
    print("B1-FALSIFIER PASS digest=%s" % digest)
    raise SystemExit(0)


if __name__ == "__main__":
    main()
