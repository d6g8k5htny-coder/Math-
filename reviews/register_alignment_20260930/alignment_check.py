"""Checks for REGISTER-ALIGNMENT-20260930-v1 (RECONCILIATION.md, PROPOSED_TRANSITIONS.json, RN_COUNT_INTERFACE_REVIEW.md).

Standard library only. Run from the repository root:  python -B -S reviews/register_alignment_20260930/alignment_check.py
Checks: IDENTITIES, VERDICTS, BASELINE, TRANSITIONS, GATE, INTERFACE, NEGATIVES. No mathematics is re-proved; the
proposed graph is replayed through the downstream hard gate's own validators. Nothing is written to the repository.
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
           "skip-interface-premise", "holder-reversed", "baseline-drift", "duplicate-drift")
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
        "| Cutoff `r^{1/24}` | **ACCEPT** |"],
    "reviews/p15_full_price_nonauthor_20260926/REVIEW.md": [
        "| Blob | `582180e41dca0ad815ad0f18574df42040912149` |",
        "| SHA256 | `87521901ca8e5405b4d1e47f1deb1cd0326affbd6f5967b53c4178590da993f9` |",
        "| 1. Coordinatewise hazard transform, separate concavity, chord, `p=0,1` | **ACCEPT** |"],
    "reviews/side24_v1_coefficient_claude_20260929/REVIEW.md": [
        "c06daccc4ba4b9168522b9888b76a7d599934fc3b91bd753ee5d492262917769",
        "Overall: **ACCEPT at the arithmetic-enclosure scope**"],
    "PROOF_INDEX.md": [
        "- D2 lifetime remainder: proof [frontiers/three_fronts_20260924/LIFETIME_REMAINDER.md]",
        "- D3 SIDE24 coefficient: proof [coefficients/side24_v1/PROOF.md]",
        "- D4 fixed-remote RN theorem: proof [frontiers/remote_window_20260924/PROOF.md]",
        "- D5 fixed-annulus height-window fallback: proof [frontiers/rn_thin_tube_20260925/FIXED_ANNULUS_CANDIDATE.md]",
        "- D6 P15 full price theorem: proof [frontiers/full_price_20260924/PROOF.md]"],
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
        n["review_disposition"] = p["review_disposition"]
        n["review_sources"] = [r["ref"] for r in p["review_sources"]]
        if p.get("coverage_source"):
            n["coverage_source"] = p["coverage_source"]
    return new


def check_transitions(root, spec):
    graph = json.loads((root / GRAPH).read_text(encoding="utf-8"))
    ok = spec.get("declarative") is True and spec.get("executed") is False and spec.get("edges_unchanged") is True
    ids = [t["node"] for t in spec["transitions"]]
    ok &= len(ids) == len(set(ids)) and len(ids) >= 1
    for t in spec["transitions"]:
        p = t["proposed"]
        ok &= p["classification"] == "PROVED_REVIEWED" and p["controlling"] is False
        ok &= bool(p.get("scope")) and len(p.get("review_sources", [])) >= 1
        if t["kind"] == "candidate":
            ok &= p.get("source") in INVENTORY and p["fingerprint"] == INVENTORY[p["source"]][0]
        else:
            ok &= t["kind"] == "region" and p.get("coverage_source") in ids
        ok &= not t["node"].startswith(("hist.", "eng.", "regional."))
    if not ok:
        return False, None
    new = apply(spec, graph)
    nodes = new["nodes"]
    edges = new["edges"]
    ok &= edges == graph["edges"]
    ok &= all(graph["nodes"][k] == nodes[k] for k in graph["nodes"] if k.startswith("hist."))
    for t in spec["transitions"]:
        nid = t["node"]
        if t["kind"] == "candidate":
            req = [e["to"] for e in edges if e["from"] == nid and e["required"] is True]
            ok &= all(nodes[d]["classification"] == "PROVED_REVIEWED" for d in req)
            ok &= sorted(req) == sorted(t["required_premises_after"])
        else:
            ok &= nodes[t["proposed"]["coverage_source"]]["classification"] == "PROVED_REVIEWED"
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
    changed = sorted(t["node"] for t in spec["transitions"])
    imp = ri.get("impacted") if isinstance(ri, dict) else None
    names = []
    if isinstance(imp, list):
        for x in imp:
            names.append(x if isinstance(x, str) else str(x.get("node") or x.get("id") or x))
    # loss-only rule: every changed node is itself in the impacted set
    ok &= isinstance(ri, dict) and set(changed) <= set(names)
    return bool(ok), {"changed_nodes": changed, "impacted": sorted(set(names)), "reverse_impact_keys": sorted(ri.keys()) if isinstance(ri, dict) else []}


def check_interface():
    """Exact finite content of RN_COUNT_INTERFACE_REVIEW.md."""
    ok = True
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
    # (N4): r = e^-t, t = 1..12: E N / r^3 = ceil(t) increases; E N^p = ceil(t)^p e^-3t <= (t+1)^p e^-3t <= finite sup
    for p in (1, 2, 4, 7):
        vals = [math.ceil(t) ** p * math.exp(-3 * t) for t in range(1, 13)]
        bound = [(t + 1) ** p * math.exp(-3 * t) for t in range(1, 13)]
        ok &= all(v <= b + 1e-15 for v, b in zip(vals, bound))
        tmax = max(1.0, p / 3 - 1)  # critical point of (t+1)^p e^{-3t}
        sup = (tmax + 1) ** p * math.exp(-3 * tmax)
        grid = [(t / 100 + 1) ** p * math.exp(-3 * (t / 100)) for t in range(100, 400000, 7)]
        ok &= max(grid) <= sup + 1e-9 and math.isfinite(sup)
        ok &= all(math.ceil(t) > math.ceil(t - 1) for t in range(2, 13))  # E N_r / r^3 -> infinity along the grid
    # sharp p: r = 2^{-p m}: E N^p = 1, E N = r^{3-3/p} exactly
    for p in (2, 3, 4):
        for m in (1, 2, 3):
            r = F(1, 2 ** (p * m))
            n_r = 2 ** (3 * m)  # = ceil(r^{-3/p}) exactly
            ok &= n_r ** p * r ** 3 == 1 and le(F(1), F(2 ** p)) and n_r * r ** 3 == F(1, 2 ** (3 * m * (p - 1)))
            ok &= n_r * r ** 3 == r ** 3 / r ** F(3, 1) * F(1, 2 ** (3 * m * (p - 1)))  # r^{3-3/p} = 2^{-3m(p-1)}
    # (N5): int_0^inf min(q, A e^{-t/B}) dt = B q (1 + log(A/q)), q <= A; numeric quadrature at three points
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
        num = s * h / 3
        ok &= abs(num - B * q * (1 + math.log(A / q))) <= 1e-6 * B * q * (1 + math.log(A / q))
    # uniform tail of the (N4) example: P(N_r > t) = r^3 1{t < ceil(log 1/r)} <= e^3 e^{-3t}
    for s_ in range(1, 15):
        r3 = math.exp(-3 * s_)
        for t10 in range(0, 10 * s_ + 30):
            t = t10 / 10
            p_tail = r3 if t < math.ceil(s_) else 0.0
            ok &= le(p_tail, math.exp(3) * math.exp(-3 * t) + 1e-300)
    return bool(ok)


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
    checks = {"IDENTITIES": ident, "VERDICTS": ident and check_verdicts(root), "BASELINE": check_baseline(root, spec),
              "TRANSITIONS": trans_ok, "GATE": gate_ok, "INTERFACE": check_interface(), "NEGATIVES": check_negatives(root),
              "D4_DUPLICATE": check_d4_duplicate(root, spec)}
    passed = all(checks.values()) and len(checks) == 8
    print(json.dumps({"object": "REGISTER-ALIGNMENT-20260930-v1", "checks": checks, "passed": passed,
                      "inventory_files": len(INVENTORY), "transitions": len(spec["transitions"]), "gate": gate,
                      "scope": "identity, verdict-row, live-baseline, transition-shape, hard-gate replay, interface arithmetic, "
                               "filesystem-negative and live D4-duplicate checks; no mathematics is re-proved; nothing is written"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
