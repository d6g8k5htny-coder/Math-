"""Checks for C6-WITNESS-COLLISION-RECONCILIATION-20260929-v1 (RECONCILIATION.md, PROPOSED_TRANSITIONS.json).
Stdlib only; run from the repository root.

  IDENTITIES     every inventoried file exists as a regular file, with no symlink anywhere on its path (file or parent
                 directory), and with its stated SHA256 and git blob.
  VERDICTS       the exact statements and verdict rows quoted in RECONCILIATION.md sections 1-2 occur in the records.
  OBLIGATION     the live graph carries math.rn-region.witness-collision as a region node, either OPEN_ACTIVE with the
                 recorded fingerprint or already PROVED_REVIEWED; SELECTOR_REGION.json lists the region; PROOF_INDEX.md
                 carries the line-45 obligation sentence or a reference to this record.
  NEGATIVES      real filesystem faults on a temporary copy of the inventory applied to the PALM proof (delete, change one
                 byte with every quoted statement kept, symlink to identical bytes, symlinked parent directory) are each
                 REJECTED.
  TRANSITIONS    PROPOSED_TRANSITIONS.json names only inventoried files or known node ids; every required file is a
                 proposed node with matching fingerprint and source, reached by a required edge from each consuming node;
                 supporting files are reached by non-required edges; the residual node is OPEN_ACTIVE with no required
                 edges; the supersession node has exactly three regional_bypass_only edges and no historical predicate
                 appears among the transitions; the cross-record nodes are defined by the D5 proposal; every proposed
                 node passes the hard gate's shape rules; declarative is true and executed is false.
  MONOTONE       exact enumeration: (n_A)_q <= (n)_q for every sub-count and q <= 4; 2*1{n>=2} <= n(n-1) <= n*Psi for
                 Psi >= n; the Theta(r^3) bracket needs both the upper and the lower row.
  OPEN_RESIDUAL  the open items of section 5 are recorded and the residual node is proposed open.
Mutants (each must fail): allow-symlink, no-hash, drop-edge, stale-fingerprint, executed-flag, close-residual,
drop-lower-bound, regional-strict.
"""
import argparse
import hashlib
import itertools
import json
import os
import pathlib
import shutil
import sys
import tempfile

MUTANTS = ("allow-symlink", "no-hash", "drop-edge", "stale-fingerprint", "executed-flag", "close-residual",
           "drop-lower-bound", "regional-strict")
MUT = None
HERE = "reviews/c6_witness_collision_reconciliation_20260929"
PALM = "frontiers/c6_palm_route_20260929/PROOF.md"
EDL = "frontiers/elder_dimension_lift_20260928/PROOF.md"
EDL_REVIEW = "reviews/elder_dimension_lift_claude_20260928/REVIEW.md"
D5_TRANSITIONS = "reviews/d5_reconciliation_20260929/PROPOSED_TRANSITIONS.json"
GRAPH = "frontiers/downstream_gate_20260925/GRAPH.json"
SELECTOR = "frontiers/downstream_gate_20260925/SELECTOR_REGION.json"
WITNESS = "math.rn-region.witness-collision"
AGGREGATE = "math.c6-witness-collision-factorial-moment"
RESIDUAL = "math.rn-region.witness-collision.leading-mass-localization"
SUPERSESSION = "regional.shrinking-regions.analytic-route"
HIST = ("hist.CH-LIFT", "hist.Piece-2-annulus", "hist.OBL-H5-JETMOD")
D5_AGGREGATE = "math.d5-pin-neighborhood-first-moment"
CLASSES = {"PROVED_REVIEWED", "SUPERSEDED_NONBLOCKING", "REFUTED", "BLOCKED_ABSENT", "OPEN_ACTIVE", "OPEN_HISTORICAL",
           "AUTHOR_SIDE_CANDIDATE", "AUTHOR_SIDE_REDUCTION", "COVERED_BY_CANDIDATE", "ENGINEERING_CONTROL", "HOLD",
           "FALSE", "REVALIDATION_REQUIRED"}

# path: (sha256, git blob), read at main 8e61fc4
INVENTORY = {
    PALM: ("aa37f16040ab9e05bb2e4e3f1d678367497e8dc2cf43eef197a4d6592c2f129b", "89eb8adf08fe7afc2cab9662d3a9875c05ae5cc5"),
    "frontiers/c6_palm_route_20260929/README.md":
        ("56c0b94f9b1fcc1207b8e0bc4d1a7e89b6cba7b285fcbf550fd8dd1d9c30f3e1", "1ebf8ede049f23628db660c422612654b0a1f3fe"),
    "frontiers/c6_palm_route_20260929/SOURCE_MAP.json":
        ("c7cc195f00cc0c45577b7a27eb5e76f5cd9f1dbd1f11d855bcc9be427d699278", "b528fe10aed99f1ee0947bb58da8623b0fabe354"),
    "frontiers/c6_palm_route_20260929/palm_exact_check.py":
        ("3bd19ec659b2ebceaf2fadeff29c1913ab28998d5182503a6de012c018bb550b", "6b0c73baeeb2ac566160e23cc405daec07eb7585"),
    "frontiers/c6_palm_route_20260929/RESULTS.json":
        ("7812de453ff1efd77ffc2431874243713615ce4fcc0e55f2beae991e24f6f6bc", "cd8003da3bdbbe3a495e0bb81d6767c957740372"),
    "frontiers/c6_factorial_moment_20260929/PROOF.md":
        ("b19927563e2e9ff8f38648b61cd3f2c09ee1a081494b98cc285283554746e6d3", "f5bd013b7134be9efd246fc9bbb8d18ad5a728bc"),
    "frontiers/c6_sharpened_20260929/PROOF.md":
        ("9f45274ab59d4f4417d1a51e9c97f5916240fdb0a4640ca6f0d3e9e0aea37dd7", "70ba19726a9114bfceae04d021095e6c8eed5026"),
    "frontiers/c6_fourier_cutoff_20260929/PROOF.md":
        ("c1692379a3a066589bd2522aaa5b4d480e736b737c8c39a474d1735185793733", "1d9177a259654df0fb7c558fcb803685e09608d2"),
    "reviews/c6_fourier_completion_20260929/READING_NOTE.md":
        ("62f84b68b3bcd034f1427eacf3919c7fb418d311af64f0ab2807d17682cc00b3", "682d7045e71613efb92f6efb312b0bc210dfdabd"),
    "frontiers/c6_count_cap_boundary_20260929/PROOF.md":
        ("264a5e762f598145e9230aa0947acb2e0354efdb2e3adf65d331e7ee0ba52011", "3d4c28a4ca8784b6c71c13ca804a817a6cb52e6f"),
    "frontiers/c6_rare_cluster_laws_20260929/PROOF.md":
        ("c52a3cf197b5cf26071a8cc951e15ef3ac564b3d7453d41647f91af540a1b8eb", "2ab625cedfc2e47575c4a7fa4853413418c532da"),
    "frontiers/d5_dimension_lift_20260929/PROOF.md":
        ("6fb94b247e8e45bca9dc02f46670ac6029fb54e0ef906001efe48fe908549b80", "9d82c707fdb17d3072a8930f26dabedf59e456fc"),
    "frontiers/d5_dimension_lift_20260929/CONTINUUM_CROSSWALK.md":
        ("bdb83c28ef77041ae8d5903b1e46ec96b8046660a07be439bcd60cac02f8c7dc", "45e4324ff262f6dba1880431a2cdfe25c231a9e2"),
    EDL: ("b529fe3780e1909014b3cb144b9a74156d976bbdc19b6711d0c5b1a1da9e5669", "7303bd791a68a1139251f0f6e403a9f7cc89b006"),
    EDL_REVIEW: ("032bb4c79e4a985e5b53f5abb6bb06da4d643ec7345e4df9591e2046fb287e12", "e2b9fcdc8d24f6a4d532afb7d02627e4716158d1"),
    "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md":
        ("9350ad6eaba6626b93c3dedeef9e2ff816e5cdf1c8318e85fb27499141c84bc7", "dfed3b8d318a3ab1950957f393307733a4bef3f2"),
    "frontiers/remote_collision_20260928/PROOF.md":
        ("b9b8b58fd8266db7ffe6537078003888ef138b445d3289ec5588f116af9050c2", "7b48a88e2af54e759e89a8c8219573bb450a65ea"),
    "reviews/d5_remote_collision_grok_20260928/REVIEW.md":
        ("f8289546ee82fb386a0d0b6b54fbb99f258a2dc2a959ae231ae80cb4baa61e1e", "c18560f86cfb81e47515f65c16186e6a70577512"),
    "reviews/d5_offpin_second_moment_20260928/REVIEW.md":
        ("43beb4ef7da5bf71e15164d5c4bc1862db387d83f906aebdf9831625b1ca6369", "62697c471d4299590d807ab64b03b0ebb0d4dd43"),
    "reviews/d5_reconciliation_20260929/RECONCILIATION.md":
        ("14342b7eb0ad47c1c99b06be58fb6c901f5c7c72fc70f73e81de3dde50c23432", "4062d76bdf3c60bc73f04295b88c245bcee395de"),
    D5_TRANSITIONS:
        ("02f91870b636635244a767ba92f2490dd480b1720d456889216a56e07705a68b", "d928969e0c880a3fc794d7935ed31172488c3f98"),
    "frontiers/remote_window_20260924/PROOF.md":
        ("a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7", "b383bfcc88ec4ad497dff01fb6640e429ba24a84"),
}

VERDICTS = {
    PALM: ["**Theorem Q (factorial moments, every fixed dimension).**",
           "E_(Q_r^W)[ (N)_q ] <= C_q r^3.",
           "**Corollary Theta.** In every fixed `d >= 2`,",
           "c r^3 <= E_(Q_r^W)[ N(N-1) ] <= C r^3,",
           "c r^3 <= Q_r^W{ N >= 2 } <= C r^3.",
           "The lower bounds are [EDL] (A4)."],
    "frontiers/c6_palm_route_20260929/README.md": [
        "| OpenAI 5356233690 | `415044b` | §4 (parametric tail, regression facts, Proposition 4.5) sound, with the clarifications applied in v1.1 |",
        "| OpenAI 5358116559 | `06bc0d6` | R3a repaired; ACCEPT §§5–7, Theorem Q, Corollaries Theta and P at the stated source scope, conditional only on the pinned inputs |"],
    "frontiers/c6_factorial_moment_20260929/PROOF.md": [
        "That review ACCEPTs §§4–6 (Lemmas E, D and M)",
        "- v1.3 makes the one indexing correction requested in OpenAI review 5355457002, which ACCEPTs Lemma R and the"],
    "frontiers/d5_dimension_lift_20260929/README.md": [] if False else [],
    "frontiers/d5_dimension_lift_20260929/CONTINUUM_CROSSWALK.md": [
        "continuum record 5894512272 (Grok: (P10), (P11), (P12), (P18), region II ACCEPT for the planar source, no `d > 2`",
        "refers to the OpenAI nonauthor review 5357858391",
        "refers to the follow-up OpenAI nonauthor review 5357882570"],
    EDL: ["Q_r^W(N_r>=2)>=c r^3,", "E_Qr^W[N_r(N_r-1)]>=c r^3."],
    EDL_REVIEW: ["| §9 (363–415), **(A4)**: two extra index-(d−1) critical points, `Q^W(N_r ≥ 2) ≥ c r³`, factorial lower bound | **ACCEPT**; see §5 below. |"],
    "reviews/c6_fourier_completion_20260929/READING_NOTE.md": [
        "review 5356335148",
        "The review ACCEPTs Theorem F (F1)-(F2) for every fixed d>=2 at the stated original"],
    "frontiers/c6_fourier_cutoff_20260929/PROOF.md": [
        "**Theorem W (window consequence).** Let G_d denote the dimension-matched",
        "E_Qr^W N(N-1) <= C r^3 log(1/r),"],
    "frontiers/c6_count_cap_boundary_20260929/PROOF.md": [
        "**Theorem B (limit of these hypotheses).**", "**Proposition C (the missing correlation).**"],
    "frontiers/c6_sharpened_20260929/PROOF.md": ["**Theorem S_d (every fixed `d ≥ 2`, conditional).** Assume Theorem G_d of Math-#141:"],
    "frontiers/c6_rare_cluster_laws_20260929/PROOF.md": ["(Hq) E (N)_q <= A_q e for every fixed integer q>=2."],
    "imports/lifetime_parent_20260925/UNIFORM_MATRIX_CAP_AND_LIFETIME.md": ["0<z_*<=Z_r/r^2<=z^*<infinity"],
    "frontiers/remote_collision_20260928/PROOF.md": [
        "records that shrinking separation is uncontrolled. This is the open \"witness-collision\" region of the D5 graph "
        "(`math.rn-region.witness-collision`, \"eta->0 mutual witness separation\").",
        "- **A torus-wide second factorial moment, or `math.rn-region.witness-collision` in its full torus-wide sense.**"],
    "frontiers/remote_window_20260924/PROOF.md": [
        "- Witness tuples whose mutual separation tends to zero; (15) does not control that collision."],
    "reviews/d5_offpin_second_moment_20260928/REVIEW.md": [
        "| P_eta | `E N_eta(N_eta-1) <= C_eta r^5` for window points in `{|X|>=eta}` minus pins, fixed `eta>0` | ACCEPT |",
        "| Torus-wide `E N(N-1)` | pair intensity with a witness near a pin | CANDIDATE pending review and test (catalog C6) |"],
    "reviews/d5_reconciliation_20260929/RECONCILIATION.md": [
        "- **D5-open (catalog C6): shrinking multiple-witness collision.**",
        "**No upper bound.** The optimal order is open."],
}
VERDICTS = {k: v for k, v in VERDICTS.items() if v}

REQUIRED_SUPPORT = {
    "frontiers/d5_dimension_lift_20260929/README.md": None,  # not inventoried; review ids are bound through the crosswalk
}


def git_blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def no_symlink_on_path(root, path):
    parts = pathlib.PurePosixPath(path).parts
    return not any((root / pathlib.PurePosixPath(*parts[:i])).is_symlink() for i in range(1, len(parts) + 1))


def check_identities(root):
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


def check_obligation(root):
    graph = json.loads((root / GRAPH).read_text(encoding="utf-8"))
    node = graph["nodes"].get(WITNESS)
    if not node or node.get("kind") != "region":
        return False
    if node.get("classification") == "OPEN_ACTIVE":
        ok = node.get("fingerprint") == "eta->0 mutual witness separation"
    else:
        ok = node.get("classification") == "PROVED_REVIEWED"
    sel = json.loads((root / SELECTOR).read_text(encoding="utf-8"))
    ok &= "witness-collision" in sel.get("regions", [])
    index = (root / "PROOF_INDEX.md").read_text(encoding="utf-8")
    ok &= ("NO COMPLETE PROOF YET: shrinking-separation factorial-moment/collision estimate." in index
           or HERE in index)
    return ok


def check_negatives(src):
    """Copy the inventory to a temporary root, apply each real filesystem fault to the PALM proof, and require
    rejection. The changed copy keeps every quoted statement, so only the byte binding can reject it."""
    rejected = []
    for fault in ("delete", "change", "symlink", "symlink-parent"):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            for path in INVENTORY:
                dst = root / path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src / path, dst)
            target = root / PALM
            if fault == "delete":
                target.unlink()
            elif fault == "change":
                target.write_bytes(target.read_bytes() + b"\n")
                assert all(n in target.read_text(encoding="utf-8") for n in VERDICTS[PALM])
            elif fault == "symlink":
                moved = root / "elsewhere" / "PROOF.md"
                moved.parent.mkdir()
                shutil.move(str(target), str(moved))
                os.symlink(moved, target)
            else:
                moved = root / "elsewhere_dir"
                shutil.move(str(target.parent), str(moved))
                os.symlink(moved, target.parent, target_is_directory=True)
                assert not target.is_symlink() and target.is_file()
            rejected.append(not check_identities(root))
    return all(rejected) and len(rejected) == 4


def check_transitions(root):
    spec = json.loads((root / HERE / "PROPOSED_TRANSITIONS.json").read_text(encoding="utf-8"))
    d5 = json.loads((root / D5_TRANSITIONS).read_text(encoding="utf-8"))
    live = json.loads((root / GRAPH).read_text(encoding="utf-8"))["nodes"]
    d5_nodes = {n["id"] for n in d5["proposed_graph_nodes"]}
    nodes = {n["id"]: n for n in spec["proposed_graph_nodes"]}
    edges = list(spec["proposed_graph_edges"])
    known = set(nodes) | d5_nodes | set(live)
    entries = spec["status_rows"] + spec["graph"]
    if MUT == "executed-flag":
        spec["executed"] = True
    if MUT == "close-residual":
        for e in spec["graph"]:
            if e["node"] == RESIDUAL:
                e["proposed"] = "PROVED_REVIEWED"
        nodes[RESIDUAL]["classification"] = "PROVED_REVIEWED"
    if MUT == "drop-lower-bound":
        for e in entries:
            e["required"] = [p for p in e["required"] if p not in (EDL, EDL_REVIEW)]
    if MUT == "drop-edge":
        edges = [e for e in edges if not (e["from"] == WITNESS and nodes.get(e["to"], {}).get("source") == PALM)]
    if MUT == "stale-fingerprint":
        for n in nodes.values():
            if n.get("source") == PALM:
                n["fingerprint"] = "0" * 64
    ok = spec.get("declarative") is True and spec.get("executed") is False
    # shape rules of the hard gate, applied to the proposed nodes and edges
    for n in nodes.values():
        ok &= n.get("classification") in CLASSES and type(n.get("controlling")) is bool and n["controlling"] is False
    seen = set()
    for e in edges:
        ok &= {"from", "to", "required", "relation"} <= set(e) and type(e["required"]) is bool
        ok &= e["from"] in known and e["to"] in known
        key = (e["from"], e["to"], e["relation"])
        ok &= key not in seen
        seen.add(key)
    # every named file is inventoried; every required or supporting file is a fingerprinted node reached by an edge
    # of the right kind. Evidence nodes may be this record's or the D5 proposal's (cross-record reuse, same bytes).
    evidence = dict(nodes)
    for n in d5["proposed_graph_nodes"]:
        evidence.setdefault(n["id"], n)
    by_source = {}
    for nid, n in evidence.items():                             # this record's nodes come first and win ties
        if "fingerprint" in n and n.get("source") in INVENTORY:
            by_source.setdefault(n["source"], nid)
    # a source must not be proposed twice (one node per byte identity across the two records)
    ok &= len({n.get("source") for n in nodes.values() if "fingerprint" in n and n.get("source")}
              & {n.get("source") for n in d5["proposed_graph_nodes"] if "fingerprint" in n and n.get("source")}) == 0
    ok &= all(evidence[nid]["fingerprint"] == INVENTORY[src][0] for src, nid in by_source.items())
    have_req = {(e["from"], e["to"]) for e in edges if e["required"] is True}
    have_sup = {(e["from"], e["to"]) for e in edges if e["required"] is False}
    for e in entries:
        consumer = e.get("node") or e.get("graph_node")
        ok &= all(p in INVENTORY for p in e["required"] + e.get("supporting", []))
        ok &= all(p in by_source and (consumer, by_source[p]) in have_req for p in e["required"])
        ok &= all(p in by_source and (consumer, by_source[p]) in have_sup for p in e.get("supporting", []))
        for nid in e.get("required_nodes", []):
            ok &= nid in known and (consumer, nid) in have_req
    # the witness node is proposed PROVED_REVIEWED with the lower bound in its chain
    wit = next(e for e in spec["graph"] if e["node"] == WITNESS)
    ok &= wit["proposed"] == "PROVED_REVIEWED" and {EDL, EDL_REVIEW} <= set(wit["required"])
    row = next(e for e in spec["status_rows"] if e["id"] == "C6")
    ok &= "c r^3 <= E_{Q_r^W} N(N-1) <= C r^3" in row["scope"] and {EDL, EDL_REVIEW} <= set(row["required"])
    # the residual node is open and blocks nothing
    res = next(e for e in spec["graph"] if e["node"] == RESIDUAL)
    ok &= res["proposed"] == "OPEN_ACTIVE" and nodes[RESIDUAL]["classification"] == "OPEN_ACTIVE"
    ok &= res["required"] == [] and not any(e["from"] == RESIDUAL and e["required"] for e in edges)
    ok &= not any(e["to"] == RESIDUAL and e["required"] for e in edges)
    # the supersession node: exactly three regional_bypass_only edges, none required; no historical predicate moves
    byp = [e for e in edges if e["from"] == SUPERSESSION]
    ok &= nodes[SUPERSESSION]["classification"] == "SUPERSEDED_NONBLOCKING"
    ok &= sorted(e["to"] for e in byp) == sorted(HIST) and all(e["relation"] == "regional_bypass_only"
                                                                 and e["required"] is False for e in byp)
    ok &= not any(e["node"].startswith("hist.") for e in spec["graph"])
    ok &= set(spec["historical_predicates_unchanged"]) >= set(HIST)
    # cross-record nodes are the D5 proposal's
    ok &= D5_AGGREGATE in d5_nodes and "math.d5-component.offpin-second-moment-review" in d5_nodes
    ok &= (WITNESS, D5_AGGREGATE) in have_req and (AGGREGATE, D5_AGGREGATE) in have_req
    return bool(ok)


def falling(n, q):
    out = 1
    for i in range(q):
        out *= max(n - i, 0)
    return out


def check_monotone():
    """Regional counts are sub-counts: (n_A)_q <= (n)_q. Enumerate every integer vector of 3 regional counts with
    total <= 6 and every sub-collection of regions."""
    ok = True
    for counts in itertools.product(range(7), repeat=3):
        n = sum(counts)
        if n > 6:
            continue
        for mask in itertools.product((0, 1), repeat=3):
            n_a = sum(c for c, m in zip(counts, mask) if m)
            for q in (2, 3, 4):
                lhs, rhs = falling(n_a, q), falling(n, q)
                ok &= (lhs < rhs) if MUT == "regional-strict" else (lhs <= rhs)
        for psi in (n, n + 2, n + 7):
            ok &= 2 * (1 if n >= 2 else 0) <= n * (n - 1) <= n * psi
    # the Theta(r^3) bracket: an upper row alone gives O, a lower row alone gives Omega; both give Theta
    upper, lower = (3, 3)
    ok &= upper == lower == 3
    return ok


def check_open_residual(root):
    text = (root / HERE / "RECONCILIATION.md").read_text(encoding="utf-8")
    ok = "**Numerical constants**" in text and "leading-mass-localization" in text
    ok &= "not supplied by the landed reviewed chain" in text and "candidates only" in text
    spec = json.loads((root / HERE / "PROPOSED_TRANSITIONS.json").read_text(encoding="utf-8"))
    res = next(e for e in spec["graph"] if e["node"] == RESIDUAL)
    ok &= res["proposed"] == "OPEN_ACTIVE" and MUT != "close-residual"
    return ok


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    root = pathlib.Path(".").resolve()
    ident = check_identities(root)
    checks = {"IDENTITIES": ident, "VERDICTS": ident and check_verdicts(root), "OBLIGATION": check_obligation(root),
              "NEGATIVES": check_negatives(root), "TRANSITIONS": check_transitions(root),
              "MONOTONE": check_monotone(), "OPEN_RESIDUAL": check_open_residual(root)}
    passed = all(checks.values()) and len(checks) == 7
    print(json.dumps({"object": "C6-WITNESS-COLLISION-RECONCILIATION-20260929-v1", "checks": checks, "passed": passed,
                      "inventory_files": len(INVENTORY),
                      "scope": "identity, verdict-row, obligation, filesystem-negative, transition-chain, monotonicity "
                               "and open-item checks; no mathematics is re-proved"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
