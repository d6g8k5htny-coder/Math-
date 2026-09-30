"""Checks for C6-RESIDUAL-CLOSURE-20260930-v1 (RECONCILIATION.md, PROPOSED_TRANSITIONS.json, EXTERNAL_REVIEWS.md).

Standard library only. Run from the repository root:  python -B -S reviews/c6_residual_closure_20260930/residual_check.py
Checks: IDENTITIES, VERDICTS, LIVE, DEDUCTION, TRANSITIONS, GATE, NEGATIVES. No mathematics is re-proved beyond the exact
finite bookkeeping of section 3 (pair identities, tails, ledgers); the proposed graph is replayed through the downstream hard gate's own validators in
both executions. Nothing is written to the repository.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import sys
import tempfile
from fractions import Fraction as F

MUTANTS = ("allow-symlink", "no-hash", "stale-fingerprint", "drop-required-edge", "executed-flag", "controlling-true",
           "tail-reversed", "pair-identity-broken", "route-c-broken", "drop-review-needle")
MUT = None
HERE = "reviews/c6_residual_closure_20260930"
GRAPH = "frontiers/downstream_gate_20260925/GRAPH.json"
SELECTOR = "frontiers/downstream_gate_20260925/SELECTOR_REGION.json"
HARD_GATE = "frontiers/downstream_gate_20260925/hard_gate.py"
RES = "math.rn-region.witness-collision.leading-mass-localization"
WIT = "math.rn-region.witness-collision"
AGG = "math.c6-witness-collision-factorial-moment"
RECORD_NODE = "math.c6r-component.residual-closure-record"
PALM_NODE = "math.c6-component.palm-proof"
SC = "frontiers/spectral_cluster_closure_20260929/PROOF.md"
FP_RES = "leading-order r^3 mass of E N(N-1): scale-r localization; open piece = mixed local/remote pairs M(R, s_0)"
FP_WIT = "eta->0 mutual witness separation"
INVENTORY = {
    "frontiers/spectral_cluster_closure_20260929/PROOF.md": [
        "e971b2cbe50a8a06b47c1219191201e0d1037c9adac23e5e3b7d2051bb70c2eb",
        "16c56821b52fd76b0be791622b9c3809eafde75a"
    ],
    "frontiers/spectral_cluster_closure_20260929/REVIEW_RECORD.md": [
        "6031d36697789097185a8e65bfbdf80f447e229689eac5a706ee8b0558db64a5",
        "9bcae183fecdf0ffe4d612a209438a4fb1fa0edd"
    ],
    "frontiers/spectral_cluster_closure_20260929/README.md": [
        "b1e2a0722945a6189d8338c2e5b1f1a74b3b5646b8dc10fe29168c165508342c",
        "895dded8aa8e405ad8e9640d3ffebc6449a108d0"
    ],
    "frontiers/c6_cluster_law_20260929/PROOF.md": [
        "96b8e2d59defee6059bf151a896b7fc7c91fc529b385a3db8a87574901197b38",
        "ba492c8e62e58bfc055fc8254c790e893d346ba5"
    ],
    "frontiers/c6_cluster_law_20260929/README.md": [
        "e4b35f2b0e919ba57ebfb121c403896a32782d58dd99d7ec6a3d6d9e5107c6ac",
        "1166376f7b4d917b1bda3f9438adfd94d8831139"
    ],
    "frontiers/c6_cluster_law_20260929/SOURCE_MAP.json": [
        "0584c3808b633fceb3c308186b07d862eb4916053daf4e7bf1110592ec41f107",
        "ef51c582d0b1c874aabb01fce3b35c10631f7fc6"
    ],
    "frontiers/c6_palm_route_20260929/PROOF.md": [
        "aa37f16040ab9e05bb2e4e3f1d678367497e8dc2cf43eef197a4d6592c2f129b",
        "89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5"
    ],
    "reviews/c6_residual_closure_20260930/EXTERNAL_REVIEWS.md": [
        "aba67dbb8e4f8df3456652625015de4984ba3bd8afe1e4961f63dae628fde069",
        "5afe9a2090f2bbee6bd09b31b977c9451db1cea5"
    ],
    "reviews/c6_residual_closure_20260930/RECONCILIATION.md": [
        "d7420581ac771591f8449afbdd1c096450610b1158bed02a3868483efe10f546",
        "38a49460bef06548a8c4a8209c4cd11b2e0807a4"
    ],
    "frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md": [
        "e81d7fe09d25c3266eb8e62922756f54761d7f74d692fb35d9a8071fffd73769",
        "a32fd5f7d941bbe1fe943df045b1e0fbec8d691c"
    ],
    "frontiers/two_scale_cluster_geometry_20260929/REVIEW_RECORD.md": [
        "5295c373a16b6557584e1a633e28fd5962f3e96023945bcc068819e83a0d2cad",
        "9f7c7f6fc59ead440258887eb113135ab1dc3463"
    ]
}
VERDICTS = {
    "frontiers/spectral_cluster_closure_20260929/PROOF.md": [
        "sum_(n>=1) n^q |r^-3 Q_r^W(N_r=n)-nu1*1{n=1}-nu2*1{n=2}| -> 0",
        "r^-3 Q_W(N_R=j) -> a_j^R=integral 1{n_R=j}dM",
        "Dominated convergence proves a_j^R->a_j",
        "Q_W(N_R>0,N_far^rho>0)=o_(R,rho)(r^3)",
        "E (N)_2/r^3 -> 2nu2"],
    "frontiers/spectral_cluster_closure_20260929/REVIEW_RECORD.md": [
        "Git blob16c56821b52fd76b0be791622b9c3809eafde75a",
        "A — Anthropic Claude5359968447",
        "B — Anthropic Claude5359845136",
        "C — OpenAI/Codex5359879627",
        "ACCEPT Sections7-8, compact-origin-jet far conditioning, full mixed o(r^3), radius"],
    "frontiers/spectral_cluster_closure_20260929/README.md": [
        "Core conditional proof has completed scoped nonauthor A/B/C acceptance."],
    "frontiers/c6_cluster_law_20260929/PROOF.md": [
        "**Corollary Lambda (asymptotic factorial moments).**",
        "Lambda_2 = 2 nu(2)",
        "Moreover `nu_near^A(n) -> nu_near(n)` as `A -> oo`",
        "**Lemma 5.2 (no near–far cross term).**",
        "C(A, rho) r^(9/2)"],
    "frontiers/c6_cluster_law_20260929/README.md": ["# C6 cluster law (CL-C6-CLUSTER-LAW-20260929-v1.2)"],
    "frontiers/c6_cluster_law_20260929/SOURCE_MAP.json": ["nonauthor_acceptance", "review 5360192822"],
    "frontiers/c6_palm_route_20260929/PROOF.md": [
        "**Object:** CL-C6-PALM-20260929-v1.",
        "**Theorem Q (factorial moments, every fixed dimension).**"],
    HERE + "/EXTERNAL_REVIEWS.md": [
        "pullrequestreview-5360192822",
        "VERDICT: ACCEPT Theorem N, Corollaries Lambda/S",
        "A pull-request review is a mutable external object"],
    HERE + "/RECONCILIATION.md": ["**Object:** C6-RESIDUAL-CLOSURE-20260930-v1.", "(Res)", "(D1)", "(D2)"],
    "frontiers/two_scale_cluster_geometry_20260929/TWO_SCALE_LAW.md": [
        "**Theorem L (factorial localization).** For every fixed integer q>=2,",
        "r^-3 E_r[(N_r)_q-(N_in)_q] -> 0.",
        "E_r[N_R N_far^rho]=o_(R,rho)(r^3),"],
    "frontiers/two_scale_cluster_geometry_20260929/REVIEW_RECORD.md": [
        "Anthropic Claude review5360227991",
        "bloba32fd5f7d941bbe1fe943df045b1e0fbec8d691c",
        "ACCEPT of Theorem T, Theorem L, ordered-pair law L3"],
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
        if MUT == "no-hash":
            continue
        if hashlib.sha256(data).hexdigest() != sha or git_blob(data) != blob:
            return False
    return True


def check_verdicts(root):
    needles = {k: list(v) for k, v in VERDICTS.items()}
    if MUT == "drop-review-needle":
        needles[SC].append("THIS NEEDLE IS NOT IN THE SOURCE")
    for path, ns in needles.items():
        text = (root / path).read_text(encoding="utf-8")
        if not all(n in text for n in ns):
            return False
    return True


def load_spec(root):
    spec = json.loads((root / HERE / "PROPOSED_TRANSITIONS.json").read_text(encoding="utf-8"))
    if MUT == "executed-flag":
        spec["executed"] = True
    if MUT == "controlling-true":
        spec["transitions"][0]["proposed"]["controlling"] = True
    if MUT == "stale-fingerprint":
        for n in spec["proposed_graph_nodes"]:
            if n["id"] == PALM_NODE:
                n["fingerprint"] = "0" * 64
    if MUT == "drop-required-edge":
        spec["proposed_graph_edges"] = [e for e in spec["proposed_graph_edges"]
                                        if not (e["from"] == RES and e["to"] == "math.c6r-component.spectral-closure-proof")]
    return spec


def check_live(root, spec):
    graph = json.loads((root / GRAPH).read_text(encoding="utf-8"))
    nodes = graph["nodes"]
    wit = nodes.get(WIT)
    ok = isinstance(wit, dict) and wit.get("kind") == "region" and wit.get("fingerprint") == FP_WIT
    ok &= wit.get("classification") in ("OPEN_ACTIVE", "PROVED_REVIEWED")
    res = nodes.get(RES)
    if res is not None:
        ok &= res.get("kind") == "region" and res.get("fingerprint") == FP_RES
        ok &= res.get("classification") in ("OPEN_ACTIVE", "PROVED_REVIEWED")
    sel = json.loads((root / SELECTOR).read_text(encoding="utf-8"))
    ok &= "witness-collision" in sel.get("regions", [])
    # no live fingerprinted node already carries a component source, except the cross-record palm node
    comp_sources = {n["source"]: n["id"] for n in spec["proposed_graph_nodes"]}
    for nid, n in nodes.items():
        if isinstance(n, dict) and n.get("fingerprint") and n.get("source") in comp_sources:
            ok &= nid == PALM_NODE and comp_sources[n["source"]] == PALM_NODE
    return bool(ok)


def check_deduction():
    """Exact finite bookkeeping of RECONCILIATION.md section 3."""
    ok = True
    f2 = lambda n: n * (n - 1)
    f3 = lambda n: n * (n - 1) * (n - 2)
    # (D1): (N)_2 - (N_R)_2 = 2 N_R N_out + (N_out)_2 >= 2 N_R N_out >= 0
    for nr in range(13):
        for no in range(13):
            rhs = 2 * nr * no + (no * no if MUT == "pair-identity-broken" else f2(no))
            ok &= f2(nr + no) - f2(nr) == rhs and rhs >= 2 * nr * no >= 0
    # tail: for integers n > M >= 3, n(n-1) <= n(n-1)(n-2)/(M-1)
    for M in range(3, 11):
        for n in range(M + 1, 41):
            lhs, rhs = f2(n) * (M - 1), f3(n)
            ok &= (lhs >= rhs) if MUT == "tail-reversed" else (lhs <= rhs)
    # (D2), Route C: 0 <= (N)_2 - (A)_2 <= N^2 [1{B>0} + 1{A>0, C>0} + 1{C>=2}] for all counts A, B, C
    for a in range(9):
        for b in range(9):
            for c in range(9):
                n = a + b + c
                ind = (1 if b > 0 else 0) + (1 if (a > 0 and c > 0) else 0) + (0 if MUT == "route-c-broken" else (1 if c >= 2 else 0))
                ok &= 0 <= f2(n) - f2(a) <= n * n * ind
    ok &= F(3, 2) + F(9, 4) - 3 == F(3, 4) and F(3, 2) + F(5, 2) - 3 == F(1)
    # Stirling: n^4 = (n)_4 + 6 (n)_3 + 7 (n)_2 + (n)_1
    for n in range(0, 21):
        ok &= n ** 4 == n * (n - 1) * (n - 2) * (n - 3) + 6 * f3(n) + 7 * f2(n) + n
    # exponent ledgers of the two direct routes
    ok &= F(3) + F(3, 2) == F(9, 2) and F(9, 2) > 3
    ok &= F(3, 2) + F(3, 4) + F(5, 4) == F(7, 2) and F(7, 2) > 3
    # truncation error of a finite distribution against E(N)_3 / (M - 1)
    probs = [F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 32), F(1, 64), F(1, 128), F(1, 256), F(1, 256)]
    assert sum(probs) == 1
    e3 = sum(p * f3(n) for n, p in enumerate(probs))
    for M in (3, 4, 5, 6):
        tail = sum(p * f2(n) for n, p in enumerate(probs) if n > M)
        ok &= tail <= e3 / (M - 1)
    # iterated limit, exact rational instance: a_2 = 1, a_2^R = 1 - 1/R^2, limsup_r r^-3 M_R = 2 a_2 - 2 a_2^R = 2/R^2 -> 0
    vals = [2 - 2 * (1 - F(1, R * R)) for R in range(4, 40)]
    ok &= all(v == F(2, R * R) for v, R in zip(vals, range(4, 40)))
    ok &= all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)) and vals[-1] < F(1, 500)
    return bool(ok)


def build(spec, graph, stage):
    """Apply the proposal to a copy of the live graph. stage: 'interim' (before execution_order step 0: residual node
    OPEN_ACTIVE with its evidence attached), 'final' (after step 0: record node read, residual PROVED_REVIEWED),
    'final-preexisting' (Math-#160 step 1 already created the residual node OPEN_ACTIVE). Returns (old, new)."""
    old = copy.deepcopy(graph)
    if stage == "final-preexisting":
        old["nodes"][RES] = {"layer": "D5", "kind": "region", "classification": "OPEN_ACTIVE", "controlling": False,
                             "fingerprint": FP_RES, "notes": "Math-#160 execution_order step 1"}
    new = copy.deepcopy(old)
    live_by_source = {n.get("source"): nid for nid, n in graph["nodes"].items()
                      if isinstance(n, dict) and n.get("fingerprint") and n.get("source")}
    id_map = {}
    for c in spec["proposed_graph_nodes"]:
        nid = c["id"]
        if c.get("create_if_absent") and c["source"] in live_by_source:
            id_map[nid] = live_by_source[c["source"]]      # cross-record node already created by Math-#160
            continue
        node = {k: v for k, v in c.items() if k != "id"}
        new["nodes"][nid] = node
        id_map[nid] = nid
    t = spec["transitions"][0]
    p = t["proposed"]
    new["nodes"][RES] = {"layer": p["layer"], "kind": "region",
                         "classification": p["classification"] if stage.startswith("final") else "OPEN_ACTIVE",
                         "controlling": p["controlling"], "fingerprint": p["fingerprint"], "scope": p["scope"],
                         "explicit_limits": p["explicit_limits"], "review_disposition": p["review_disposition"],
                         "review_sources": [r["ref"] for r in p["review_sources"]],
                         "reading_rule": [id_map.get(x, x) for x in p["reading_rule"]], "notes": p["notes"]}
    for e in spec["proposed_graph_edges"]:
        if e.get("deferred_with"):
            continue                                        # the old-node transition presupposes Math-#160 step 3
        new["edges"].append({"from": e["from"], "to": id_map.get(e["to"], e["to"]), "required": e["required"],
                             "relation": e["relation"]})
    return old, new


def check_transitions(root, spec):
    graph = json.loads((root / GRAPH).read_text(encoding="utf-8"))
    ok = spec.get("declarative") is True and spec.get("executed") is False
    t0, t1 = spec["transitions"]
    p = t0["proposed"]
    ok &= t0["node"] == RES and t0["kind"] == "region" and p["classification"] == "PROVED_REVIEWED"
    ok &= p["controlling"] is False and p["fingerprint"] == FP_RES
    ok &= bool(p.get("scope")) and bool(p.get("explicit_limits")) and len(p.get("review_sources", [])) >= 2
    ok &= bool(p.get("notes")) and p.get("review_disposition") == "ACCEPT_AT_EXISTENTIAL_SCOPE"
    comps = spec["proposed_graph_nodes"]
    cids = [c["id"] for c in comps]
    ok &= len(cids) == len(set(cids)) and len({c["source"] for c in comps}) == len(comps)
    for c in comps:
        ok &= c["kind"] == "reading_rule_component" and c["controlling"] is False
        ok &= c["source"] in INVENTORY and c["fingerprint"] == INVENTORY[c["source"]][0]
        ok &= bool(c.get("component_role")) and bool(c.get("author_provider")) and len(c.get("review_basis", [])) >= 1
        ok &= c["component_of"] == RES
        if c["id"] == RECORD_NODE:
            ok &= c["classification"] == "AUTHOR_SIDE_CANDIDATE"       # until a non-Claude read (step 0)
        else:
            ok &= c["classification"] == "PROVED_REVIEWED"
        if c["id"] == PALM_NODE:
            ok &= c.get("create_if_absent") is True and "Math-#160" in str(c.get("cross_record"))
    req_ids = [c for c in cids if c != RECORD_NODE]
    ok &= sorted(p["reading_rule"]) == sorted(req_ids) and sorted(t0["required_premises_after"]) == sorted(req_ids)
    req = {(e["from"], e["to"]) for e in spec["proposed_graph_edges"] if e["required"] is True and not e.get("deferred_with")}
    sup = {(e["from"], e["to"]) for e in spec["proposed_graph_edges"] if e["required"] is False and not e.get("deferred_with")}
    ok &= all((RES, cid) in req for cid in req_ids) and (RES, RECORD_NODE) in sup and (RES, RECORD_NODE) not in req
    seen = set()
    for e in spec["proposed_graph_edges"]:
        key = (e["from"], e["to"], e["relation"])
        ok &= key not in seen and type(e["required"]) is bool and bool(e["relation"])
        seen.add(key)
        ok &= e["from"] in (RES, WIT)
    # the deferred old-node transition
    ok &= t1["node"] == WIT and t1.get("deferred") is True and t1["proposed"]["classification"] == "PROVED_REVIEWED"
    ok &= sorted(t1["required_premises_after"]) == sorted([RES, AGG]) and t1["proposed"]["controlling"] is False
    ok &= AGG not in graph["nodes"] or graph["nodes"][AGG].get("classification") == "PROVED_REVIEWED"
    if not ok:
        return False, None
    builds = {}
    for stage in ("interim", "final", "final-preexisting"):
        old, new = build(spec, graph, stage)
        nodes, edges = new["nodes"], new["edges"]
        ok &= all(old["nodes"][k] == nodes[k] for k in old["nodes"] if k != RES)   # no live node other than the residual changes
        ok &= edges[:len(old["edges"])] == old["edges"]
        req_after = [e["to"] for e in edges if e["from"] == RES and e["required"] is True]
        if stage.startswith("final"):
            ok &= nodes[RES]["classification"] == "PROVED_REVIEWED"
            ok &= all(nodes[d]["classification"] == "PROVED_REVIEWED" for d in req_after)
        else:
            ok &= nodes[RES]["classification"] == "OPEN_ACTIVE"
        ok &= nodes[RECORD_NODE]["classification"] == "AUTHOR_SIDE_CANDIDATE"
        ok &= len(req_after) == len(cids) - 1
        builds[stage] = (old, new)
    return bool(ok), builds


def load_hard_gate(root):
    hg_spec = importlib.util.spec_from_file_location("hard_gate", root / HARD_GATE)
    hg = importlib.util.module_from_spec(hg_spec)
    hg_spec.loader.exec_module(hg)
    return hg


def check_gate(root, spec, builds):
    if builds is None:
        return False, {}
    hg = load_hard_gate(root)
    out = {}
    ok = True
    comp_ids = {c["id"] for c in spec["proposed_graph_nodes"]}
    for stage, (old, new) in builds.items():
        try:
            hg.validate_graph_fail_closed(new)
            rep_new = hg.closure_report(new)
            rep_old = hg.closure_report(old)
            ri = hg.reverse_impact_between(old, new)
        except Exception:
            return False, {}
        ok &= rep_new.get("gate_ok") is True and not rep_new.get("illegal_controlling") and rep_old.get("gate_ok") is True
        ok &= not any(n.get("controlling") for n in new["nodes"].values())
        changed, impacted = set(ri["changed_nodes"]), set(ri["impacted"])
        ok &= RES in changed and RES in impacted
        ok &= all((cid in changed) or (cid not in new["nodes"]) for cid in comp_ids)
        ok &= WIT not in changed                                     # the deferred transition is not applied
        hold = {h["node"] for h in rep_new.get("hold_proposals", [])}
        if stage == "interim":
            ok &= RES not in hold or new["nodes"][RES]["classification"] == "OPEN_ACTIVE"
        else:
            ok &= RES not in hold                                        # every required premise PROVED_REVIEWED
        out[stage] = {"changed_nodes": sorted(changed), "impacted": sorted(impacted),
                      "residual_classification": new["nodes"][RES]["classification"],
                      "old_node_transition": "deferred: presupposes Math-#160 step 3 (aggregate node absent live)"}
    return bool(ok), out


def check_negatives(src):
    rejected = []
    for fault in ("delete", "change", "symlink", "symlink-parent"):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            for path in INVENTORY:
                dst = root / path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src / path, dst)
            target = root / SC
            if fault == "delete":
                target.unlink()
            elif fault == "change":
                data = bytearray(target.read_bytes())
                data[0] ^= 1
                target.write_bytes(bytes(data))
            elif fault == "symlink":
                real = target.with_name("real_" + target.name)
                target.rename(real)
                os.symlink(real.name, target)
            else:
                parent = target.parent
                real = parent.with_name("real_" + parent.name)
                parent.rename(real)
                os.symlink(real.name, parent)
            rejected.append(not identities_ok(root))
    return all(rejected)


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    root = pathlib.Path(".").resolve()
    spec = load_spec(root)
    ident = identities_ok(root)
    trans_ok, builds = check_transitions(root, spec)
    gate_ok, gate = check_gate(root, spec, builds)
    checks = {"IDENTITIES": ident, "VERDICTS": ident and check_verdicts(root), "LIVE": check_live(root, spec),
              "DEDUCTION": check_deduction(), "TRANSITIONS": trans_ok, "GATE": gate_ok, "NEGATIVES": check_negatives(root)}
    passed = all(checks.values()) and len(checks) == 7
    print(json.dumps({"object": "C6-RESIDUAL-CLOSURE-20260930-v1", "checks": checks, "passed": passed,
                      "inventory_files": len(INVENTORY), "component_nodes": len(spec["proposed_graph_nodes"]),
                      "gate": gate,
                      "scope": "identity, verdict-row, live-register, exact finite bookkeeping of section 3, transition-shape, "
                               "hard-gate replay in both executions, and filesystem-negative checks; the Gaussian limits are the "
                               "sources' reviewed statements and are not re-proved; nothing is written"},
                     indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
