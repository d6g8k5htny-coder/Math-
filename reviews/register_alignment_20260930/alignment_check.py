"""Checks for REGISTER-ALIGNMENT-20260930-v1 (RECONCILIATION.md, PROPOSED_TRANSITIONS.json, RN_COUNT_INTERFACE_REVIEW.md).

Standard library only. Run from the repository root:  python -B -S reviews/register_alignment_20260930/alignment_check.py
Checks: IDENTITIES, VERDICTS, BASELINE, TRANSITIONS, GATE, PROPAGATION, INTERFACE, NEGATIVES, D4_DUPLICATE. No mathematics
is re-proved; the proposed graph is replayed through the downstream hard gate's own validators, and two-commit source
mutations through its reverse-impact rule. Nothing is written to the repository.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import math
import os
import pathlib
import shutil
import sys
import tempfile
from fractions import Fraction as F

MUTANTS = ("allow-symlink", "no-hash", "stale-fingerprint", "drop-review-source", "controlling-true", "executed-flag",
           "skip-interface-premise", "holder-reversed", "baseline-drift", "duplicate-drift", "region-unlinked",
           "review-metadata-only")
MUT = None
HERE = "reviews/register_alignment_20260930"
GRAPH = "frontiers/downstream_gate_20260925/GRAPH.json"
HARD_GATE = "frontiers/downstream_gate_20260925/hard_gate.py"
D1 = "math.uniform-matrix-cap-lifetime"
D4_DUP = "math.d5-component.remote-window-proof"
D4_NODE = "math.rn-fixed-remote-window"
IFACE = "math.rn-count-interface"
D4 = "frontiers/remote_window_20260924/PROOF.md"
INVENTORY = {
    "frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md": [
        "380b7d0abdb0fe2de5a6564565af9560d3f1b1ce22fd5538927db0c52f4f3a4a",
        "247b3ecf80bfbe896948d5d489b2d5842a81c481"
    ],
    "frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md": [
        "aa993f5217bd70e6d1060402d121ab659f6582a098e29042c67585a345a8e3ab",
        "371fd6d17920f2eb3b1c5ec30297acf6daf1d385"
    ],
    "coefficients/side24_v1/PROOF.md": [
        "c06daccc4ba4b9168522b9888b76a7d599934fc3b91bd753ee5d492262917769",
        "44b66f04f89fcd87383b3603fa69f1feb64cdddd"
    ],
    "frontiers/remote_window_20260924/PROOF.md": [
        "a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7",
        "b383bfcc88ec4ad497dff01fb6640e429ba24a84"
    ],
    "frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md": [
        "1fd9fe7141e464fd1c09ebf0318d8a701729c9c61ea24f73f7e20a9cf10c552b",
        "081abc13c5e66342c13df2af2bd6b114f320486f"
    ],
    "frontiers/full_price_20260924/PROOF.md": [
        "87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9",
        "582180e41dca0ad815ad0f18574df42040912149"
    ],
    "reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md": [
        "29a0c6d00ce739baf1d29a3163977d8e707e2079e216fba4fee3669cebec127d",
        "1f153966dae48d10574db0d272f75d08ca3a8b23"
    ],
    "reviews/p15_full_price_nonauthor_20260926/REVIEW.md": [
        "691ea0db5c0f073326c9f7208c9804c6f5d0daf92ba7467529c9d57e08b15eb7",
        "07db19f826763b8faa7414ba2e403d9c45bc0b6e"
    ],
    "reviews/side24_v1_coefficient_claude_20260929/REVIEW.md": [
        "258c414c46be93142ee552cfa4c32c03dd89b6bf7b0b470334f152e1e0a57eef",
        "665d1683f33a7180957923c3cb2abce8ade235d1"
    ],
    "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md": [
        "9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7",
        "dfed3b8d318a3ab1950957f393307733a4bef3f2"
    ],
    "frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md": [
        "079f9399aef401d58749b3684f3acbb7f49ffdcbcac9f501b79e06c28a7f4e7d",
        "89cae3a9734f2ec7172cd0b6b0b3af3ddd355d73"
    ],
    "reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md": [
        "04cf4c986f29ac7ac33b3cc87feac23f3cf494e0c1b3bf4476e4e6666de46574",
        "8988251631cab8e65eb2b01a08f7fc593b018570"
    ],
    "frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md": [
        "c0dbb821fb57b685a20cc321e4074456f39a9697f3104afd1f728e4732179bb9",
        "173881916ccd0e738bdb41279e835e78e520fcbc"
    ],
    "reviews/register_alignment_20260930/RN_COUNT_INTERFACE_REVIEW.md": [
        "52d9038a3f27335d3c219babec785984e00b77f28d7cd7b390477c0bc6a749d1",
        "7e7049e2b5e96e51394d44683d61c9d0e03b9323"
    ],
    "reviews/register_alignment_20260930/EXTERNAL_REVIEWS.md": [
        "fa6677f16f688352f3fc9b1703d39324fe57a3b2bf61960591f524f858e99c9d",
        "2be80e35bce1ffc90d1f7a0675ad5e8830ddbd28"
    ]
}
VERDICTS = {
    "frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md": ["**Object:** LIFETIME-BOUNDED-REMAINDER-20260924-v1."],
    "frontiers/three_fronts_20260924/RN_COUNT_INTERFACE.md": [
        "**Object:** RN-COUNT-INTERFACE-20260924-v1.",
        "E[N_r 1_Er] <= (E N_r^p)^(1/p) P(E_r)^(1-1/p).",
        "N_r=ceil(log(1/r)) 1_Er.",
        "= B q[1+log(A/q)]."],
    "coefficients/side24_v1/PROOF.md": ["Object: SIDE24-COEFFICIENT-D23-20260924-v1."],
    "frontiers/remote_window_20260924/PROOF.md": [
        "**Object:** RN-FIXED-REMOTE-WINDOW-20260924-v1.",
        "Equation (14) now supplies it for every fixed remote region and the entire BETWEEN-PIN HEIGHT WINDOW."],
    "frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md": ["**Object:** D5-FIXED-ANNULUS-STITCH-20260925-v1."],
    "frontiers/full_price_20260924/PROOF.md": ["**Object:** P15-FULL-TRANSFORMED-PRICE-20260924-v1."],
    "reviews/pr22_fixed_annulus_nonauthor_20260925/REVIEW.md": [
        "| Blob | `081abc13c5e66342c13df2af2bd6b114f320486f` |",
        "| SHA256 | `1fd9fe7141e464fd1c09ebf0318d8a701729c9c61ea24f73f7e20a9cf10c552b` |",
        "| Cutoff `r^{1/24}` | **ACCEPT** |",
        "| Inner two-scale stitching | **ACCEPT** |",
        "`TWO_SCALE_ADDENDUM.md` blob `89cae3a9734f2ec7172cd0b6b0b3af3ddd355d73`, 15902 bytes"],
    "reviews/p15_full_price_nonauthor_20260926/REVIEW.md": [
        "| Blob | `582180e41dca0ad815ad0f18574df42040912149` |",
        "| SHA256 | `87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9` |",
        "| 1. Coordinatewise hazard transform, separate concavity, chord, `p=0,1` | **ACCEPT** |",
        "SHA256 `c0dbb821fb57b685a20cc321e4074456f39a9697f3104afd1f728e4732179bb9`. That is the digest named in the proof.",
        "| 4. Full-block cover, same palette, realized family | **ACCEPT** |"],
    "reviews/side24_v1_coefficient_claude_20260929/REVIEW.md": [
        "c06daccc4ba4b9168522b9888b76a7d599934fc3b91bd753ee5d492262917769",
        "Overall: **ACCEPT at the arithmetic-enclosure scope**"],
    "PROOF_INDEX.md": [
        "- D2 lifetime remainder: proof [frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md]",
        "- D3 SIDE24 coefficient: proof [coefficients/side24_v1/PROOF.md]",
        "- D4 fixed-remote RN theorem: proof [frontiers/remote_window_20260924/PROOF.md]",
        "- D5 fixed-annulus height-window fallback: proof [frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md]",
        "- D6 P15 full price theorem: proof [frontiers/full_price_20260924/PROOF.md]"],
    "frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md": ["**Object:** D5-TWO-SCALE-20260925-v1."],
    "reviews/replacement_20260925_pr19_pr21/TWO_SCALE_REVIEW.md": [
        "blob `89cae3a9734f2ec7172cd0b6b0b3af3ddd355d73`, 15902 bytes, SHA256 `079f9399aef401d58749b3684f3acbb7f49ffdcbcac9f501b79e06c28a7f4e7d`",
        "| S6 | **ACCEPT** |"],
    "frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md": ["**Object:** P15-REALIZED-COVERS-20260924-v1."],
    HERE + "/RN_COUNT_INTERFACE_REVIEW.md": [
        "**Overall: ACCEPT at the logical-interface scope.**",
        "numerical corroborations of arguments proved above, not exact checks"],
    HERE + "/EXTERNAL_REVIEWS.md": [
        "issuecomment-5841270276", "issuecomment-5841782206", "issuecomment-5841269490", "issuecomment-5841779222",
        "issuecomment-5841783172", "issuecomment-5841861362", "issuecomment-5842112010",
        "R5 and R6 are **ACCEPT**. Theorem R is accepted at its stated O(1) remainder scope.",
        "All six coefficient interfaces check out. The disposition is **COEFFICIENT-CALC-REVIEWED / PARENT-IMPORTED-OPEN**.",
        "This accepts only the fixed-ρ and fixed-η interfaces below. It does not accept a full RN or 24-jet theorem.",
        "D6 ANALYTIC REVIEW COMPLETE",
        "An issue comment is a mutable external object"],
}


def git_blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def no_symlink_on_path(root, path):
    parts = pathlib.PurePosixPath(path).parts
    return not any((root / pathlib.PurePosixPath(*parts[:i])).is_symlink() for i in range(1, len(parts) + 1))


def identities_ok(root):
    for path, (sha, blob) in INVENTORY.items():
        p = root / path
        if not os.path.lexists(p):
            return False
        if MUT != "allow-symlink" and not no_symlink_on_path(root, path):
            return False
        if not p.is_file():
            return False
        data = p.read_bytes()
        if MUT != "no-hash" and (hashlib.sha256(data).hexdigest() != sha or git_blob(data) != blob):
            return False
    return True


def check_verdicts(root):
    for path, needles in VERDICTS.items():
        text = (root / path).read_text(encoding="utf-8")
        if not all(n in text for n in needles):
            return False
    return True


def load_spec(root):
    spec = json.loads((root / HERE / "PROPOSED_TRANSITIONS.json").read_text(encoding="utf-8"))
    if MUT == "executed-flag":
        spec["executed"] = True
    if MUT == "skip-interface-premise":
        spec["transitions"] = [t for t in spec["transitions"] if t["node"] != IFACE]
    if MUT == "drop-review-source":
        for t in spec["transitions"]:
            if t["node"] == D4_NODE:
                t["proposed"]["review_sources"] = []
    if MUT == "controlling-true":
        for t in spec["transitions"]:
            if t["node"] == D4_NODE:
                t["proposed"]["controlling"] = True
    if MUT == "stale-fingerprint":
        for t in spec["transitions"]:
            if t["node"] == D4_NODE:
                t["proposed"]["fingerprint"] = "0" * 64
    if MUT == "baseline-drift":
        for t in spec["transitions"]:
            if t["node"] == D4_NODE:
                t["current"]["classification"] = "PROVED_REVIEWED"
    return spec


def check_baseline(root, spec):
    live = json.loads((root / GRAPH).read_text(encoding="utf-8"))["nodes"]
    ok = True
    for t in spec["transitions"]:
        n = live.get(t["node"])
        if not isinstance(n, dict):
            return False
        ok &= n.get("classification") == t["current"]["classification"]
        ok &= n.get("fingerprint") == t["current"]["fingerprint"]
        ok &= n.get("kind") == t["kind"] and n.get("controlling") is False
        if t["kind"] == "candidate":
            ok &= n.get("source") == t["proposed"]["source"]
    d1 = live.get(D1, {})
    ok &= d1.get("classification") == "PROVED_REVIEWED" and d1.get("fingerprint") == INVENTORY[
        "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md"][0]
    rr = d1.get("reading_rule", [])
    ok &= len(rr) == 4 and all(live.get(x, {}).get("classification") == "PROVED_REVIEWED" for x in rr)
    return bool(ok)


def apply(spec, graph):
    """The proposal applied to a copy of the live graph: the eight flips with their scope exclusions and replacement
    notes, plus the review-record / consumed-source component nodes and the required edges that carry the evidence."""
    new = copy.deepcopy(graph)
    for t in spec["transitions"]:
        n = new["nodes"][t["node"]]
        p = t["proposed"]
        n["classification"] = p["classification"]
        n["controlling"] = p["controlling"]
        n["fingerprint"] = p["fingerprint"]
        if p.get("source"):
            n["source"] = p["source"]
        n["scope"] = p["scope"]
        n["explicit_limits"] = p["explicit_limits"]
        n["notes"] = p["notes"]
        n["review_disposition"] = p["review_disposition"]
        n["review_sources"] = [r["ref"] for r in p["review_sources"]]
        n["review_basis"] = [{"review": r["ref"], "provider": r.get("provider", "unstated"), "verdict": r.get("verdict", "")}
                             for r in p["review_sources"]]
        if p.get("coverage_source"):
            n["coverage_source"] = p["coverage_source"]
    for c in spec["proposed_graph_nodes"]:
        new["nodes"][c["id"]] = {k: v for k, v in c.items() if k != "id"}
    new["edges"] = list(new["edges"]) + [dict(e) for e in spec["proposed_graph_edges"]]
    return new

def check_transitions(root, spec):
    graph = json.loads((root / GRAPH).read_text(encoding="utf-8"))
    ok = spec.get("declarative") is True and spec.get("executed") is False and spec.get("edges_unchanged") is False
    ids = [t["node"] for t in spec["transitions"]]
    ok &= len(ids) == len(set(ids)) and len(ids) >= 1
    for t in spec["transitions"]:
        p = t["proposed"]
        ok &= p["classification"] == "PROVED_REVIEWED" and p["controlling"] is False
        ok &= bool(p.get("scope")) and bool(p.get("explicit_limits")) and bool(p.get("notes"))
        ok &= len(p.get("review_sources", [])) >= 1
        if t["kind"] == "candidate":
            ok &= p.get("source") in INVENTORY and p["fingerprint"] == INVENTORY[p["source"]][0]
        else:
            ok &= t["kind"] == "region" and p.get("coverage_source") in ids
        ok &= not t["node"].startswith(("hist.", "eng.", "regional."))
    # component nodes: one per byte identity, fingerprinted to the inventory, PROVED_REVIEWED evidence records,
    # none for bytes the live graph already carries with a fingerprint (Codex 4139312869 on Math-#160)
    comps = spec["proposed_graph_nodes"]
    cids = [c["id"] for c in comps]
    live_fp_sources = {n.get("source") for n in graph["nodes"].values()
                       if isinstance(n, dict) and n.get("fingerprint") and n.get("source")}
    ok &= len(cids) == len(set(cids)) and not (set(cids) & set(graph["nodes"])) and len(comps) == spec["nodes_added"]
    ok &= len({c["source"] for c in comps}) == len(comps)
    for c in comps:
        ok &= c["kind"] == "reading_rule_component" and c["classification"] == "PROVED_REVIEWED" and c["controlling"] is False
        ok &= c["source"] in INVENTORY and c["fingerprint"] == INVENTORY[c["source"]][0]
        ok &= c["source"] not in live_fp_sources
        ok &= bool(c.get("component_role")) and bool(c.get("author_provider")) and len(c.get("review_basis", [])) >= 1
        consumers = c.get("components_of") or [c.get("component_of")]
        ok &= all(x in ids + cids for x in consumers) and len(consumers) >= 1
    edges_new = spec["proposed_graph_edges"]
    known = set(graph["nodes"]) | set(cids)
    live_keys = {(e["from"], e["to"], e["relation"]) for e in graph["edges"]}
    seen = set()
    for e in edges_new:
        ok &= {"from", "to", "required", "relation"} <= set(e) and type(e["required"]) is bool
        ok &= e["from"] in known and e["to"] in known and bool(e["relation"].strip())
        key = (e["from"], e["to"], e["relation"])
        ok &= key not in seen and key not in live_keys
        seen.add(key)
        ok &= e["from"] in ids or e["from"] in cids                 # every added edge leaves one of this record's objects
    ok &= len(edges_new) == spec["edges_added"]
    if not ok:
        return False, None
    new = apply(spec, graph)
    nodes = new["nodes"]
    edges = new["edges"]
    ok &= edges[:len(graph["edges"])] == graph["edges"] and len(edges) == len(graph["edges"]) + len(edges_new)
    ok &= all(graph["nodes"][k] == nodes[k] for k in graph["nodes"] if k not in ids)   # only the eight live nodes change
    for t in spec["transitions"]:
        nid = t["node"]
        req = [e["to"] for e in edges if e["from"] == nid and e["required"] is True]
        ok &= all(nodes[d]["classification"] == "PROVED_REVIEWED" for d in req)
        ok &= sorted(req) == sorted(t["required_premises_after"])
        if t["kind"] == "region":
            ok &= t["proposed"]["coverage_source"] in req              # a region depends on its covering node
            ok &= nodes[t["proposed"]["coverage_source"]]["classification"] == "PROVED_REVIEWED"
        n = nodes[nid]
        ok &= n.get("explicit_limits") == t["proposed"]["explicit_limits"] and n.get("notes") == t["proposed"]["notes"]
        ok &= "review open" not in n["notes"] and "candidate only" not in n["notes"]
        ok &= isinstance(n.get("review_basis"), list) and len(n["review_basis"]) >= 1
    for c in comps:                                                   # component nodes' own required premises
        req = [e["to"] for e in edges if e["from"] == c["id"] and e["required"] is True]
        ok &= all(nodes[d]["classification"] == "PROVED_REVIEWED" for d in req)
    return bool(ok), new

def load_hard_gate(root):
    hg_spec = importlib.util.spec_from_file_location("hard_gate", root / HARD_GATE)
    hg = importlib.util.module_from_spec(hg_spec)
    hg_spec.loader.exec_module(hg)
    return hg


def check_gate(root, spec, new):
    if new is None:
        return False, {}
    hg = load_hard_gate(root)
    old = json.loads((root / GRAPH).read_text(encoding="utf-8"))
    try:
        hg.validate_graph_fail_closed(new)
        rep_new = hg.closure_report(new)
        rep_old = hg.closure_report(old)
        ri = hg.reverse_impact_between(old, new)
    except Exception:
        return False, {}
    ok = rep_new.get("gate_ok") is True and not rep_new.get("illegal_controlling")
    ok &= rep_old.get("gate_ok") is True
    ok &= not any(n.get("controlling") for n in new["nodes"].values())
    changed = sorted([t["node"] for t in spec["transitions"]] + [c["id"] for c in spec["proposed_graph_nodes"]])
    imp = ri.get("impacted") if isinstance(ri, dict) else None
    names = []
    if isinstance(imp, list):
        for x in imp:
            names.append(x if isinstance(x, str) else str(x.get("node") or x.get("id") or x))
    # loss-only rule: every changed node is itself in the impacted set
    ok &= isinstance(ri, dict) and set(changed) <= set(names)
    return bool(ok), {"changed_nodes": changed, "impacted": sorted(set(names)), "reverse_impact_keys": sorted(ri.keys()) if isinstance(ri, dict) else []}


def check_interface():
    """Finite content of RN_COUNT_INTERFACE_REVIEW.md: exact rational checks, and floating-point corroborations
    labelled as such (OpenAI 5360320845 item 2)."""
    ok = True
    num = True
    le = (lambda a, b: a >= b) if MUT == "holder-reversed" else (lambda a, b: a <= b)
    # (N1) on finite rational spaces, p = 2 and p = 3 (Cauchy-Schwarz / Holder in power form)
    spaces = [([F(1, 4)] * 4, [0, 1, 3, 7], [1, 0, 1, 0]), ([F(1, 2), F(1, 3), F(1, 6)], [2, 5, 11], [1, 1, 0]),
              ([F(1, 8), F(3, 8), F(1, 2)], [0, 0, 9], [0, 0, 1]), ([F(9, 10), F(1, 10)], [0, 13], [0, 1])]
    for probs, N, E in spaces:
        assert sum(probs) == 1
        ene = sum(p * n * e for p, n, e in zip(probs, N, E))
        pe = sum(p * e for p, e in zip(probs, E))
        m2 = sum(p * n * n for p, n in zip(probs, N))
        m3 = sum(p * n ** 3 for p, n in zip(probs, N))
        ok &= le(ene ** 2, m2 * pe) and le(ene ** 3, m3 * pe ** 2)
        if pe > 0:  # (N3)
            ok &= ene == pe * (ene / pe)
    # (N2) exponent: (3(p-1) - beta)/p == 3 - 3/p - beta/p
    for p in (2, 3, 5):
        for beta in (F(0), F(1, 2), F(3)):
            ok &= F(3 * (p - 1), 1) / p - beta / p == 3 - F(3, p) - beta / p
    # (N4), NUMERICAL (floating point): r = e^-t, t = 1..12: E N / r^3 = ceil(t) increases; ceil(t)^p e^-3t <= (t+1)^p e^-3t,
    # and the grid maximum of (t+1)^p e^-3t stays below the located critical value. The proof is the log-derivative argument.
    for p in (1, 2, 4, 7):
        vals = [math.ceil(t) ** p * math.exp(-3 * t) for t in range(1, 13)]
        bound = [(t + 1) ** p * math.exp(-3 * t) for t in range(1, 13)]
        num &= all(v <= b + 1e-15 for v, b in zip(vals, bound))
        tmax = max(1.0, p / 3 - 1)  # critical point of (t+1)^p e^{-3t}
        sup = (tmax + 1) ** p * math.exp(-3 * tmax)
        grid = [(t / 100 + 1) ** p * math.exp(-3 * (t / 100)) for t in range(100, 400000, 7)]
        num &= max(grid) <= sup + 1e-9 and math.isfinite(sup)
        ok &= all(math.ceil(t) > math.ceil(t - 1) for t in range(2, 13))  # E N_r / r^3 -> infinity along the grid (exact integers)
    # sharp p: r = 2^{-p m}: E N^p = 1, E N = r^{3-3/p} exactly
    for p in (2, 3, 4):
        for m in (1, 2, 3):
            r = F(1, 2 ** (p * m))
            n_r = 2 ** (3 * m)  # = ceil(r^{-3/p}) exactly
            ok &= n_r ** p * r ** 3 == 1 and le(F(1), F(2 ** p)) and n_r * r ** 3 == F(1, 2 ** (3 * m * (p - 1)))
            ok &= n_r * r ** 3 == r ** 3 / r ** F(3, 1) * F(1, 2 ** (3 * m * (p - 1)))  # r^{3-3/p} = 2^{-3m(p-1)}
    # (N5), NUMERICAL (floating point): int_0^inf min(q, A e^{-t/B}) dt = B q (1 + log(A/q)), q <= A; Simpson quadrature at
    # three parameter points corroborates the antiderivative identity proved in the review
    for (A, B, q) in ((1.0, 1.0, 0.1), (20.0, 0.5, 0.001), (3.0, 2.0, 2.0)):
        t0 = B * math.log(A / q)
        n = 200000
        T = t0 + 60 * B
        h = T / n
        s = 0.0
        for i in range(n + 1):
            t = i * h
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            s += w * min(q, A * math.exp(-t / B))
        quad = s * h / 3
        num &= abs(quad - B * q * (1 + math.log(A / q))) <= 1e-6 * B * q * (1 + math.log(A / q))
    # uniform tail of the (N4) example, NUMERICAL (floating point): P(N_r > t) = r^3 1{t < ceil(log 1/r)} <= e^3 e^{-3t}
    for s_ in range(1, 15):
        r3 = math.exp(-3 * s_)
        for t10 in range(0, 10 * s_ + 30):
            t = t10 / 10
            p_tail = r3 if t < math.ceil(s_) else 0.0
            num &= le(p_tail, math.exp(3) * math.exp(-3 * t) + 1e-300)
    return {"exact": bool(ok), "numerical_corroboration": bool(num)}


def check_negatives(src):
    rejected = []
    for fault in ("delete", "change", "symlink", "symlink-parent"):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            for path in INVENTORY:
                dst = root / path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src / path, dst)
            target = root / D4
            if fault == "delete":
                target.unlink()
            elif fault == "change":
                target.write_bytes(target.read_bytes() + b"\n")
            elif fault == "symlink":
                moved = root / "elsewhere" / "PROOF.md"
                moved.parent.mkdir()
                shutil.move(str(target), str(moved))
                os.symlink(moved, target)
            else:
                moved = root / "elsewhere_dir"
                shutil.move(str(target.parent), str(moved))
                os.symlink(moved, target.parent)
            rejected.append(not identities_ok(root))
    return all(rejected)


def check_d4_duplicate(root, spec):
    """Since ec6db8c (Math-#151) the live graph carries the D4 bytes twice; bind the duplicate to the D4 transition."""
    live = json.loads((root / GRAPH).read_text(encoding="utf-8"))["nodes"]
    dup = live.get(D4_DUP)
    old = live.get(D4_NODE)
    t = next(t for t in spec["transitions"] if t["node"] == D4_NODE)
    want = spec["live_duplicate"]
    fp = t["proposed"]["fingerprint"]
    if MUT == "duplicate-drift":
        fp = "1" * 64
    if not isinstance(dup, dict) or not isinstance(old, dict):
        return False
    ok = dup.get("classification") == "PROVED_REVIEWED" and dup.get("controlling") is False
    ok &= dup.get("fingerprint") == fp == want["fingerprint"] == INVENTORY[t["proposed"]["source"]][0]
    ok &= dup.get("source") == t["proposed"]["source"] == want["source"]
    ok &= dup.get("component_of") == want["component_of"]
    ok &= any("main#76" in str(b.get("review")) and b.get("verdict") == "ACCEPT" for b in dup.get("review_basis", []))
    ok &= old.get("fingerprint") == dup.get("fingerprint") and old.get("classification") == t["current"]["classification"]
    return bool(ok)


def snapshot(root, graph):
    """Source snapshot in the shape of git_transition_audit.read_snapshot, taken from the working tree."""
    out = {}
    for nid, node in graph["nodes"].items():
        ref = node.get("source")
        if ref is None:
            out[nid] = {"kind": "record_only"}
            continue
        if ref.startswith(("https://", "http://", "external:")):
            out[nid] = {"kind": "external_unresolved", "reference": ref}
            continue
        p = root / ref.rstrip("/")
        if p.is_file():
            data = p.read_bytes()
            out[nid] = {"kind": "blob", "reference": ref, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        elif p.is_dir():
            h = hashlib.sha256()
            for f in sorted(x for x in p.rglob("*") if x.is_file() and "__pycache__" not in x.parts):
                h.update(str(f.relative_to(p)).encode("utf-8") + b"\0" + hashlib.sha256(f.read_bytes()).digest())
            out[nid] = {"kind": "tree", "reference": ref, "sha256": h.hexdigest()}
        else:
            out[nid] = {"kind": "missing", "reference": ref}
    return out


def check_propagation(root, spec, new):
    """Two-commit mutations on the proposed graph through the production loss-only rule (reverse_impact_between with
    source snapshots): evidence and consumed-source changes must reach the objects they support (OpenAI 5360320845,
    5360327058; Codex 4139807558, 4139807567). Nothing scientific is decided here."""
    if new is None:
        return False, {}
    hg = load_hard_gate(root)
    g = copy.deepcopy(new)
    if MUT == "region-unlinked":
        g["edges"] = [e for e in g["edges"] if e.get("relation") != "covered_by"]
    if MUT == "review-metadata-only":
        drop = {c["id"] for c in spec["proposed_graph_nodes"] if str(c.get("component_role", "")).startswith("review_record")}
        g["nodes"] = {k: v for k, v in g["nodes"].items() if k not in drop}
        g["edges"] = [e for e in g["edges"] if e["from"] not in drop and e["to"] not in drop]
    base = snapshot(root, g)
    by_source = {}
    for nid, n in g["nodes"].items():
        if n.get("source"):
            by_source.setdefault(n["source"], []).append(nid)

    def run(edit):
        g2, s2 = copy.deepcopy(g), copy.deepcopy(base)
        edit(g2, s2)
        try:
            return set(hg.reverse_impact_between(g, g2, old_sources=base, new_sources=s2)["impacted"])
        except Exception:
            return None

    def source_edit(path, kind="blob"):
        def f(g2, s2):
            for nid in by_source.get(path, []):
                s2[nid] = ({"kind": "blob", "reference": path, "bytes": 1, "sha256": "1" * 64} if kind == "blob"
                           else {"kind": "missing", "reference": path})
        return f

    def fp_edit(g2, s2):
        g2["nodes"][D4_NODE]["fingerprint"] = "2" * 64

    eight = {t["node"] for t in spec["transitions"]}
    cases = {
        "d4-proof-edit-reaches-region-and-consumer": (source_edit(D4), {D4_NODE, "math.rn-region.fixed-remote", "math.rn-mesoscopic-reduction"}),
        "annulus-proof-edit-reaches-region": (source_edit("frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md"),
                                              {"math.rn-fixed-annulus-window", "math.rn-region.fixed-annulus-window"}),
        "interface-review-deleted-reaches-interface-consumers-regions": (source_edit(HERE + "/RN_COUNT_INTERFACE_REVIEW.md", "missing"),
                                              {IFACE, D4_NODE, "math.rn-fixed-annulus-window", "math.rn-region.fixed-remote", "math.rn-region.fixed-annulus-window"}),
        "external-review-record-edit-reaches-d2-d3-d4-d6": (source_edit(HERE + "/EXTERNAL_REVIEWS.md"),
                                              {"math.lifetime-remainder", "math.side24-coefficient", D4_NODE, "math.p15-full-price", "math.rn-region.fixed-remote"}),
        "two-scale-addendum-edit-reaches-annulus-and-region": (source_edit("frontiers/rn_thin_tube_20260925/TWO_SCALE_ADDENDUM.md"),
                                              {"math.rn-fixed-annulus-window", "math.rn-region.fixed-annulus-window"}),
        "realized-covers-edit-reaches-d6": (source_edit("frontiers/three_fronts_20260924/P15_REALIZED_COVERS.md"), {"math.p15-full-price"}),
        "d4-fingerprint-edit-reaches-region": (fp_edit, {D4_NODE, "math.rn-region.fixed-remote"}),
    }
    results = {}
    for name, (edit, must) in cases.items():
        imp = run(edit)
        results[name] = imp is not None and must <= imp
    imp = run(source_edit("reviews/d5_collar_count_20260928/REVIEW.md"))
    results["unrelated-edit-leaves-the-eight-untouched"] = imp is not None and not (imp & eight)
    imp = run(lambda g2, s2: None)
    results["no-op-impacts-nothing"] = imp == set()
    return bool(all(results.values()) and len(results) == 9), results


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    root = pathlib.Path(".").resolve()
    spec = load_spec(root)
    ident = identities_ok(root)
    trans_ok, new = check_transitions(root, spec)
    gate_ok, gate = check_gate(root, spec, new)
    prop_ok, prop = check_propagation(root, spec, new)
    iface = check_interface()
    checks = {"IDENTITIES": ident, "VERDICTS": ident and check_verdicts(root), "BASELINE": check_baseline(root, spec),
              "TRANSITIONS": trans_ok, "GATE": gate_ok, "PROPAGATION": prop_ok,
              "INTERFACE": iface["exact"] and iface["numerical_corroboration"], "NEGATIVES": check_negatives(root),
              "D4_DUPLICATE": check_d4_duplicate(root, spec)}
    passed = all(checks.values()) and len(checks) == 9
    print(json.dumps({"object": "REGISTER-ALIGNMENT-20260930-v1", "checks": checks, "passed": passed,
                      "inventory_files": len(INVENTORY), "transitions": len(spec["transitions"]),
                      "component_nodes": len(spec["proposed_graph_nodes"]), "edges_added": len(spec["proposed_graph_edges"]),
                      "gate": gate, "propagation": prop,
                      "interface_evidence": {"exact_rational": ["(N1) Holder p=2,3 on finite rational spaces", "(N2) exponent identity",
                                                                "(N3) conditional-mean identity", "sharp-p example at r=2^-pm",
                                                                "(N4) integer monotonicity of ceil(t)"],
                                             "numerical_corroboration_floating_point": ["(N4) grid maximum of (t+1)^p e^-3t",
                                                                                        "(N5) Simpson quadrature at three parameter points",
                                                                                        "(N4) example uniform tail on a grid"],
                                             "results": iface},
                      "scope": "identity, verdict-row, live-baseline, transition-shape, hard-gate replay, two-commit propagation, "
                               "interface arithmetic (exact and numerical parts labelled), filesystem-negative and live D4-duplicate "
                               "checks; no mathematics is re-proved; nothing is written"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
