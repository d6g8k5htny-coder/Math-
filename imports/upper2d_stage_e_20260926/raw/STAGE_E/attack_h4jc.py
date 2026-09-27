#!/usr/bin/env python3
# attack_h4jc.py — STAGE-E counterexample-first attack on Theorem H4-JC
# (H4_CLOSURE.md §2.3, frozen body a67d50b9...) and on the "joint carrier
# paid once" bookkeeping consumed by D1_ASSEMBLY v2.0 (frozen body
# 86882dca...).
#
# CLAIM UNDER ATTACK (frozen, verbatim H4 §2.3):
#   "On Reg ∩ TYP, the two counted populations are disjoint at each saddle:
#    a loop witness has BOTH sector components in C; an α-qualifying witness
#    has EXACTLY one ... Hence pointwise  N_qual + N_loop ≤ N_w  a.s."
#
# Frozen literal predicates:
#   * N_loop (C2 §2.2 = H4 §1): window saddles S' (index-1, f(S') in (s,b),
#     S' != S) whose BOTH sector components AT OWN LEVEL f(S') are contained
#     in C := C_M(s)  (M's component of O^s).  NO alive/birth clause.
#   * N_qual (D2 §1.1/§1.3): window saddles y with
#     birth(C_M(v)) = b (alive), exactly one sector component = C_M(v)
#     (own-level MIX), other side elder; D2-COUNT: {N_qual=1} = A.
#
# ATTACK: on any A-field, M's death saddle S' has f(S') = u in (s,b); its
# two sector components at level u are C_M(u) and the elder Y; BELOW u they
# are one component (they merge at S'), so at level s < u both are contained
# in C_M(s).  Hence the death saddle fires BOTH N_qual (D2, own-level) and
# N_loop (C2, level-s literal): N_qual + N_loop = N_w + 1 > N_w.
#
# This program CERTIFIES the counterexample inside the campaign's own frozen
# discrete model (B1's b1_falsifier.py, hash-pinned): a hand-carved quiet
# A-field with a UNIQUE window saddle (the death saddle), plus D2's own
# synthetic T2-QUAL, plus a full-ensemble sweep showing the double count is
# generic on A-pairs, plus the demonstration that the C2/H4 mirrors'
# alpha-predicate (level-s inC reading) is structurally blind to it
# (sum(inC)==1 is impossible for 2-cluster saddles).
#
# Discipline: fail-closed (ck -> SystemExit(1)); no bare asserts; fully
# deterministic; no floats in the digest; python3 / python3 -O byte-identical.

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
B1DIR = os.path.join(ROOT, "B1_taxonomy")
sys.path.insert(0, B1DIR)

B1_FAL_SHA256 = "818df7985412071259345455c9ff6b68cad0c0fa9d636009cf8849b550154185"


def ck(cond, msg):
    if not cond:
        print("STAGE-E ATTACK SELF-CHECK FAILED:", msg)
        raise SystemExit(1)


def _sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


_p = os.path.join(B1DIR, "b1_falsifier.py")
ck(os.path.exists(_p), "b1_falsifier.py missing")
ck(_sha256(_p) == B1_FAL_SHA256, "b1_falsifier.py hash drift vs B1 FREEZE.txt")

import b1_falsifier as B1F

N, V, RING = B1F.N, B1F.V, B1F.RING

# ---------------------------------------------------------------------------
# Independent instruments (own code paths; semantics pinned to frozen text)
# ---------------------------------------------------------------------------

def window_saddles(f, Mv, Sv):
    """N_w support: w != M,S, key(S) < key(w) < key(M), >=2 upper clusters."""
    out = []
    kS, kM = f.key(Sv), f.key(Mv)
    for w in range(V):
        if w == Sv or w == Mv or not (kS < f.key(w) < kM):
            continue
        cl = B1F.upper_link_clusters(f, w)
        if len(cl) >= 2:
            out.append((w, cl))
    return out


def qual_d2(f, Mv, w, clusters):
    """D2 frozen Qual(y) (D2_BRANCH_CONTROL.md §1.1, OWN level v = key(w)):
    alive: birth(C_M(v)) = key(M); MIX: exactly one cluster's level-v
    component = C_M(v); elder: another cluster's level-v component has
    birth key > key(M)."""
    compW, maxkeyW = B1F.components_above(f, w)
    C = compW[Mv]
    if C < 0 or maxkeyW[C] != f.key(Mv):
        return False  # not alive-with-birth-b (PRE or degenerate)
    comp_ids = []
    for cl in clusters:
        ids = {compW[RING[w][k]] for k in cl}
        ck(len(ids) == 1, "cluster split across level-v components")
        comp_ids.append(ids.pop())
    inC = [c == C for c in comp_ids]
    if sum(inC) != 1:
        return False
    return any(maxkeyW[c] > f.key(Mv) for c, ic in zip(comp_ids, inC) if not ic)


def channel_d2(f, Mv, w):
    """Verbatim re-implementation of d2_falsifier.channel_of (cross-check)."""
    comp, maxkey = B1F.components_above(f, w)
    C = comp[Mv]
    if C < 0:
        return "NA"
    if maxkey[C] > f.key(Mv):
        return "PRE"
    clusters = B1F.upper_link_clusters(f, w)
    comp_ids = []
    for cl in clusters:
        ids = {comp[RING[w][k]] for k in cl}
        comp_ids.append(ids.pop())
    inC = [c == C for c in comp_ids]
    if not any(inC):
        return "NA"
    if all(inC):
        return "LOOP"
    others = [maxkey[c] for c, ic in zip(comp_ids, inC) if not ic]
    if max(others) > f.key(Mv):
        return "QUAL"
    return "YNG"


def loop_c2(f, Mv, Sv, w, clusters):
    """C2 frozen N_loop predicate (C2_B_CLASSES.md §2.2 = H4 §1): EVERY
    upper-link cluster's level-key(w) component contained in C = C_M(s),
    read at LEVEL key(S) (components refine downward; exact per the C2/H4
    mirror code).  Literal: NO alive/birth clause."""
    compS, _ = B1F.components_above(f, Sv)
    C = compS[Mv]
    if C < 0:
        return False
    return all(compS[RING[w][cl[0]]] == C for cl in clusters)


def alpha_mirror(f, Mv, Sv, w, clusters):
    """The predicate the C2/H4 executable mirrors ACTUALLY check
    (c2_falsifier.alpha_qualifies / h4_falsifier.my_alpha_qual): exactly one
    cluster in C at LEVEL key(S), another elder at own level."""
    compS, _ = B1F.components_above(f, Sv)
    C = compS[Mv]
    compW, maxkeyW = B1F.components_above(f, w)
    kM = f.key(Mv)
    inC = [compS[RING[w][cl[0]]] == C for cl in clusters]
    elder = [maxkeyW[compW[RING[w][cl[0]]]] > kM for cl in clusters]
    return sum(inC) == 1 and any(elder[i] for i in range(len(clusters))
                                 if not inC[i])


def audit_pair(f, Mv, Sv):
    """Full JC audit of one pair. Returns dict with all counts."""
    die_partner, die_level = B1F.persistence(f)
    outcome, category = B1F.classify_pair(f, Mv, Sv, die_partner, die_level)
    ws = window_saddles(f, Mv, Sv)
    quals_d2 = [w for w, cl in ws if qual_d2(f, Mv, w, cl)]
    loops_c2 = [w for w, cl in ws if loop_c2(f, Mv, Sv, w, cl)]
    quals_mirror = [w for w, cl in ws if alpha_mirror(f, Mv, Sv, w, cl)]
    # cross-validate qual_d2 against D2's own channel predicate
    for w, cl in ws:
        ck((channel_d2(f, Mv, w) == "QUAL") == qual_d2(f, Mv, w, cl),
           "qual instrument mismatch vs D2 channel_of at %s w=%d" % (f.tag, w))
    doublecount = sorted(set(quals_d2) & set(loops_c2))
    return {
        "tag": f.tag, "Mv": Mv, "Sv": Sv, "outcome": outcome,
        "category": category, "DM": die_partner.get(Mv),
        "N_w": len(ws), "N_qual_d2": len(quals_d2),
        "N_loop_c2": len(loops_c2), "N_qual_mirror": len(quals_mirror),
        "doublecount": doublecount,
        "jc_lhs": len(quals_d2) + len(loops_c2), "jc_rhs": len(ws),
    }


# ---------------------------------------------------------------------------
# Part 1: the certified quiet counterexample (UNIQUE window saddle)
# ---------------------------------------------------------------------------
def quiet_field():
    f = B1F.base_field("STAGE-E-QUIET")
    c = B1F.carve
    c(f, 10, 10, 10.0)    # Mv
    c(f, 8, 10, 6.0)      # Sv (pair saddle; two low upper clusters)
    c(f, 9, 10, 6.5)      # Sv upper cluster 1
    c(f, 8, 11, 6.6)      # Sv upper cluster 2
    c(f, 14, 14, 8.5)     # y = the ONLY window saddle = M's death saddle
    # arm A: y -> M, all keys > key(y)
    for (i, j), val in [((14, 15), 9.2), ((13, 15), 9.25), ((12, 14), 9.3),
                        ((11, 13), 9.35), ((10, 12), 9.4), ((10, 11), 9.45)]:
        c(f, i, j, val)
    # arm B: y -> elder maximum 11.5 > b = key(M)
    for (i, j), val in [((15, 14), 9.15), ((16, 14), 9.3), ((16, 13), 9.5)]:
        c(f, i, j, val)
    c(f, 16, 12, 11.5)    # elder terminal
    return f, 10 * N + 10, 8 * N + 10


fQ, MQ, SQ = quiet_field()
r = audit_pair(fQ, MQ, SQ)
print("== Part 1: certified quiet counterexample ==")
print("   pair classification:", r["outcome"], r["category"],
      " D(M) =", r["DM"], "(y = %d)" % (14 * N + 14))
print("   N_w =", r["N_w"], " N_qual(D2,frozen,own-level) =", r["N_qual_d2"],
      " N_loop(C2,frozen,level-s) =", r["N_loop_c2"])
print("   double-counted saddles (qual AND loop):", r["doublecount"])
print("   H4-JC: N_qual + N_loop =", r["jc_lhs"], " > N_w =", r["jc_rhs"],
      " -> INEQUALITY VIOLATED:", r["jc_lhs"] > r["jc_rhs"])
ck(r["outcome"] == "failure" and r["category"] == "A", "quiet field not A")
ck(r["DM"] == 14 * N + 14, "quiet field: death partner is not y")
ck(r["N_w"] == 1, "quiet field: expected a unique window saddle")
ck(r["N_qual_d2"] == 1, "quiet field: D2 N_qual != 1 (D2-COUNT vs A)")
ck(r["N_loop_c2"] == 1, "quiet field: literal N_loop does not count death saddle")
ck(r["jc_lhs"] == 2 and r["jc_rhs"] == 1,
   "quiet field: JC violation not exhibited")
ck(r["N_qual_mirror"] == 0,
   "quiet field: the C2/H4 mirror alpha-predicate unexpectedly fired")

# ---------------------------------------------------------------------------
# Part 2: D2's own synthetic T2-QUAL is also a counterexample
# ---------------------------------------------------------------------------
def t2_qual():
    f = B1F.base_field("STAGE-E-T2QUAL")
    c = B1F.carve
    c(f, 10, 10, 10.0); c(f, 8, 10, 6.0); c(f, 9, 10, 6.5); c(f, 8, 11, 6.6)
    c(f, 14, 14, 8.5)
    for (i, j), val in [((14, 15), 9.2), ((13, 15), 9.25), ((12, 14), 9.3),
                        ((11, 13), 9.35), ((10, 12), 9.4), ((10, 11), 9.45)]:
        c(f, i, j, val)
    for (i, j), val in [((15, 14), 9.15), ((16, 14), 9.3), ((16, 13), 9.5)]:
        c(f, i, j, val)
    c(f, 16, 12, 11.5)
    return f, 10 * N + 10, 8 * N + 10, 14 * N + 14


fT, MT, ST, yT = t2_qual()
ck(channel_d2(fT, MT, yT) == "QUAL", "T2-QUAL replica: y not QUAL (D2 channel)")
rT = audit_pair(fT, MT, ST)
print("== Part 2: D2's own T2-QUAL synthetic ==")
print("   classification:", rT["outcome"], rT["category"], " D(M) =", rT["DM"])
print("   N_w =", rT["N_w"], " N_qual(D2) =", rT["N_qual_d2"],
      " N_loop(C2) =", rT["N_loop_c2"], " double:", rT["doublecount"],
      " JC violated:", rT["jc_lhs"] > rT["jc_rhs"])
ck(rT["category"] == "A" and rT["jc_lhs"] > rT["jc_rhs"],
   "T2-QUAL replica: JC violation not exhibited")

# ---------------------------------------------------------------------------
# Part 3: ensemble sweep — the double count is generic on A-pairs, and the
# mirrors' alpha-predicate is structurally blind on 2-cluster saddles
# ---------------------------------------------------------------------------
print("== Part 3: full-ensemble sweep (B1's frozen 40-field ensemble) ==")
n_pairs = nA = nA_viol = 0
n_mirror_qual_pairs = 0
n_mirror_qual_2cluster = 0
n_death_in_loop = 0
for seed in range(40):
    f = B1F.fourier_field(1000 + seed, "ens-%d" % seed, ridge=(seed % 3 == 0))
    maxima = [v for v in range(V) if B1F.is_local_max(f, v)]
    saddles = [v for v in range(V) if not B1F.is_local_max(f, v)
               and len(B1F.upper_link_clusters(f, v)) >= 2]
    for Mv in sorted(maxima):
        for Sv in sorted(saddles):
            if not f.gt(Mv, Sv) or B1F.cheb(Mv, Sv) > 4:
                continue
            rr = audit_pair(f, Mv, Sv)
            n_pairs += 1
            if rr["category"] == "A":
                nA += 1
                if rr["jc_lhs"] > rr["jc_rhs"]:
                    nA_viol += 1
                if rr["DM"] is not None:
                    ws = dict(window_saddles(f, Mv, Sv))
                    if rr["DM"] in ws and loop_c2(f, Mv, Sv, rr["DM"],
                                                  ws[rr["DM"]]):
                        n_death_in_loop += 1
            if rr["N_qual_mirror"] > 0:
                n_mirror_qual_pairs += 1
                for w, cl in window_saddles(f, Mv, Sv):
                    if len(cl) == 2 and alpha_mirror(f, Mv, Sv, w, cl):
                        n_mirror_qual_2cluster += 1
print("   pairs audited:", n_pairs, " A-pairs:", nA)
print("   A-pairs with N_qual(D2)+N_loop(C2) > N_w:", nA_viol)
print("   A-pairs whose death saddle fires literal N_loop:", n_death_in_loop)
print("   pairs where the C2/H4 mirror alpha fired at all:",
      n_mirror_qual_pairs)
print("   ... of those, mirror-alpha firings at 2-cluster (Morse) saddles:",
      n_mirror_qual_2cluster)
ck(n_pairs > 400, "ensemble too thin")
ck(nA_viol > 0, "JC inequality never violated on the ensemble (expected "
               "positive-probability failure)")
ck(nA == n_death_in_loop, "some death saddle escaped literal N_loop")
ck(n_mirror_qual_2cluster == 0,
   "mirror alpha fired at a 2-cluster saddle (structural lemma broken)")

# ---------------------------------------------------------------------------
# Part 4: structural lemma (discrete): for ANY 2-cluster window saddle,
# both upper-link clusters lie in the SAME level-key(S) component.
# (The mirror alpha's sum(inC)==1 is therefore impossible for Morse saddles:
# in the continuum the mirrored alpha population is EMPTY.)
# ---------------------------------------------------------------------------
n2 = 0
for seed in range(40):
    f = B1F.fourier_field(1000 + seed, "ens-%d" % seed, ridge=(seed % 3 == 0))
    maxima = [v for v in range(V) if B1F.is_local_max(f, v)]
    saddles = [v for v in range(V) if not B1F.is_local_max(f, v)
               and len(B1F.upper_link_clusters(f, v)) >= 2]
    for Mv in sorted(maxima):
        for Sv in sorted(saddles):
            if not f.gt(Mv, Sv) or B1F.cheb(Mv, Sv) > 4:
                continue
            compS, _ = B1F.components_above(f, Sv)
            for w, cl in window_saddles(f, Mv, Sv):
                if len(cl) != 2:
                    continue
                n2 += 1
                c0 = compS[RING[w][cl[0][0]]]
                c1 = compS[RING[w][cl[1][0]]]
                ck(c0 == c1,
                   "structural lemma fails at %s w=%d" % (f.tag, w))
print("== Part 4: structural lemma ==")
print("   2-cluster window saddles checked:", n2,
      "— both clusters ALWAYS share their level-s component")
ck(n2 > 500, "2-cluster sample too thin")

DIG = hashlib.sha256()
for line in [
    "quiet: A, D(M)=y, N_w=1, N_qual_d2=1, N_loop_c2=1, JC 2>1",
    "t2qual: JC violated",
    "ensemble: pairs=%d A=%d viol=%d deathinloop=%d mirrorpairs=%d mirror2cl=%d"
    % (n_pairs, nA, nA_viol, n_death_in_loop, n_mirror_qual_pairs,
       n_mirror_qual_2cluster),
    "structural: n2=%d all-shared" % n2,
]:
    DIG.update(line.encode())
print("STAGE-E H4-JC COUNTEREXAMPLE CERTIFIED digest=%s" % DIG.hexdigest())
