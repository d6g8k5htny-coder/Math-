"""Checks for D5-RECONCILIATION-20260929-v2.1 (RECONCILIATION.md, PROPOSED_TRANSITIONS.json). Stdlib only; run from the
repository root.

  IDENTITIES   every source and record named in RECONCILIATION.md section 3 exists as a regular file, with no symlink
               anywhere on its path (file or parent directory), and with its stated SHA256 and git blob. The P2 continuum record is MANDATORY (landed blob 4904e3d9...).
  VERDICTS     the exact verdict rows occur in each record, including the continuum record's (P10)-(P20) and (P2) rows.
  NEGATIVES    real filesystem negatives on a temporary copy of the complete packet: deleting the continuum record,
               changing one byte of it (all verdict rows kept), replacing it by a symlink to identical bytes, or
               replacing its parent directory by a symlink to an identical directory are each REJECTED.
  TRANSITIONS  PROPOSED_TRANSITIONS.json names only inventoried files; every transition with uses_P2 lists the P2
               continuum record, its checker and #111; every required file is a proposed graph node whose fingerprint
               equals its inventory SHA256 and source equals its path, reached by a required edge from each consuming
               node (the D5 row's node included); the witness-collision node and C6 stay open.
  TILING       pin disks, the collar C_{1/4,4}, {4r <= |X| <= s0} and {|X| >= s0} cover an exact rational grid.
  OPEN_C6      the collision item is still recorded as open.
Mutants (each must fail): optional-continuum, allow-symlink, no-hash, drop-dependency, drop-edge, stale-fingerprint,
drop-collar, close-c6.
"""
import argparse
import hashlib
import json
import os
import pathlib
import shutil
import sys
import tempfile
from fractions import Fraction as F

MUTANTS = ("optional-continuum", "allow-symlink", "no-hash", "drop-dependency", "drop-edge", "stale-fingerprint",
           "drop-collar", "close-c6")
MUT = None
HERE = "reviews/d5_reconciliation_20260929"
CONTINUUM = "reviews/d5_punctured_pin_continuum_claude_20260929/REVIEW.md"
CONTINUUM_CHECK = "reviews/d5_punctured_pin_continuum_claude_20260929/pp_continuum_check.py"
P111 = "reviews/d5_punctured_pin_nonauthor_20260928/REVIEW.md"

# path: (sha256, git blob)
INVENTORY = {
    "reviews/d5_local_collar_20260928/PUNCTURED_PIN_PROOF.md":
        ("f972e50bc07674ebce9d971d1a1bd4dba2f8036dde37ecb57d8a44a35650f76a", "d8acf0bcb9025b1562c03c077c8e0094ae282060"),
    "reviews/d5_local_collar_20260928/COLLAR_PROOF.md":
        ("794babe0fd039c3a93c401c0b8978316331af009fad45f953e63fbe7e1e31aab", "b5647907a8a589635855b59cc4246b23efce2801"),
    "frontiers/rn_annulus_bridge_20260925/PROOF.md":
        ("d55e2c03bb17e7977ff94130cc1ff21e54840cd1e20dc4e41ea9ad52228beb05", "6f317515b3d417661f86e2fed09bc7d950899c2b"),
    "frontiers/intermediate_window_20260928/PROOF.md":
        ("b3eb9456d7058b5b78149cfca4e072679beda85cd1a0293d209664a542db66cf", "f53a527ce0204fda271f24730b62b4223a5e43ec"),
    "frontiers/remote_window_20260924/PROOF.md":
        ("a332bae9bdc0106ce17047f7e0409cc3d94eb610a0c7b74ba5ba2d01a1620cb7", "b383bfcc88ec4ad497dff01fb6640e429ba24a84"),
    "frontiers/remote_collision_20260928/PROOF.md":
        ("b9b8b58fd8266db7ffe6537078003888ef138b445d3289ec5588f116af9050c2", "7b48a88e2af54e759e89a8c8219573bb450a65ea"),
    P111:
        ("668d74825f156c929177bc1a3481cf421de4dd7874e7b25b2aece6c10aa7dc0e", "c98cf3eefbf61f2ee3bbc1c8ef88f2218dd8b47a"),
    CONTINUUM:
        ("124c472cc064ba24021cb4bb8da1002836a4ce26c8df506228f5c20609f6575a", "4904e3d929d6dc7bc16b49eee85d7c3a21b6b484"),
    CONTINUUM_CHECK:
        ("57bc87d11271b47ebccec6ea73abf823fa90e3a8c3c7d7cd2165bdc6f7e4175c", "b0d6321f7e480d7ea855a2017532588d241f5d34"),
    "reviews/d5_punctured_pin_continuum_claude_20260929/RESULTS.json":
        ("599e21c525ad0aec7938d94f80f7771bd8e14aeb9ae1b0a60ba434428496c464", "b1b98cfdf15992736dd54f258afe26dde3d76baf"),
    "reviews/d5_punctured_pin_continuum_claude_20260929/SOURCE_FILES.json":
        ("6645abae056f0555cfb20128f3cbdbe9f5a72d76ab290cd2a96ae8f876f19faf", "fa36cd123bea3a48d7a84331a871c64a576ecd71"),
    "reviews/d5_collar_count_20260928/REVIEW.md":
        ("8c8c30cc3b19601a7421341d5da8cb6c982fbc1fcc5ae4791acafa11cc81ee4e", "6b1350fa88b3e217f9aac3c6bde7499639ebebe7"),
    "reviews/pr28_annulus_bridge_nonauthor_20260925/REVIEW.md":
        ("69ea7a479a9e8a5150cbe07b373772ab22413a1d81194d5a6a78adf6ada5f03f", "559d72242fdb7e4e3ac4a10d10641ae1da84f40e"),
    "reviews/d5_i5_planar_f_20260928/REVIEW.md":
        ("527d66e72b079ef7c854987f7e9d44f2252b81aa0e8d9e7ef3b45deb02388659", "031c5364d1377e0f85ed62caadd8406fbbedc0ab"),
    "reviews/d5_intermediate_window_claude_20260928/REVIEW.md":
        ("fb3207802bf2d92ad138bc338a36f39bcd3a94440669b9aba9558e566f767976", "100ce8ecc120fcf4e3e4e6b9b039c08632e2711c"),
    "reviews/d5_offpin_second_moment_20260928/REVIEW.md":
        ("43beb4ef7da5bf71e15164d5c4bc1862db387d83f906aebdf9831625b1ca6369", "62697c471d4299590d807ab64b03b0ebb0d4dd43"),
    "reviews/d5_remote_collision_grok_20260928/REVIEW.md":
        ("f8289546ee82fb386a0d0b6b54fbb99f258a2dc2a959ae231ae80cb4baa61e1e", "c18560f86cfb81e47515f65c16186e6a70577512"),
}

VERDICTS = {
    P111: ["Cauchy–Binet floor `9/131072` | **ACCEPT** |",
           "| (P2) count lemma | all-height punctured disk | **HOLD**"],
    CONTINUUM: [
        "giving `c_0 I ≤ Σ ≤ C_0 I` | **ACCEPT**. This lifts #111's HOLD on the Schur/compactness step. |",
        "| §6 (P11) density `≤ C r^{−3} Δ^{−2} e^{−cχ²}` | **ACCEPT** |",
        "| §6 (P12) `E_{Q_r}[K^6 | ∇f(X) = 0] ≤ C(1 + χ^6)` | **ACCEPT** |",
        "| §7 (P13)–(P14) `Z_r ≥ c_Z r²` | **ACCEPT** |",
        "| §9 (P18) weighted Kac–Rice at the fixed zero level | **ACCEPT** |",
        "| §10 (P19)–(P20) regions, puncture exhaustion; §10.1 reflection to `S` | **ACCEPT** |",
        "| **(P2)** `E_{Q_r^W} N_j(M + rE) ≤ C r³|E|` for Borel `E ⊂ D`, and the `S` version | **ACCEPT, existential.** "
        "No numerical `C` or `r_*`. Uniform in `b`, `k`, frame, `j` and `E`, for fixed `T` and compact marks. |"],
    "reviews/d5_collar_count_20260928/REVIEW.md": [
        "| Collar first moment | `E_{Q^W} N_j(r E) <= C r^3 |E|` on `C(eta, R)` | ACCEPT existential |",
        "| ACCEPT corollary of punctured-pin + collar |"],
    "reviews/pr28_annulus_bridge_nonauthor_20260925/REVIEW.md": [
        "| R1 finite-r subtraction and remainders (9)–(11) | **ACCEPT** |",
        "| R7 crossover, absorption, and full cover (17)–(20), (2) | **ACCEPT** |"],
    "reviews/d5_i5_planar_f_20260928/REVIEW.md": [
        "| **ACCEPT** existential |", "| **ACCEPT** as corollary of C2 + I4 + D4 A |"],
    "reviews/d5_intermediate_window_claude_20260928/REVIEW.md": [
        "| **(I3) shell** and **(I4) intermediate** | **ACCEPT** at the stated existential scope |",
        "| **(I5) global single-witness first moment** | **ACCEPT** as a composition."],
    "reviews/d5_offpin_second_moment_20260928/REVIEW.md": [
        "| ACCEPT |", "| CANDIDATE pending review and test (catalog C6) |"],
}


def git_blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def check_identities(root):
    for path, (sha, blob) in INVENTORY.items():
        p = root / path
        if MUT == "optional-continuum" and path == CONTINUUM and not os.path.lexists(p):
            continue                                            # the v1 defect: absence accepted
        if not os.path.lexists(p):
            return False
        if MUT != "allow-symlink" and any((root / pathlib.PurePosixPath(*pathlib.PurePosixPath(path).parts[:i])).is_symlink()
                                          for i in range(1, len(pathlib.PurePosixPath(path).parts) + 1)):
            return False                                        # symlinked file or parent directory
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


def check_negatives(src):
    """Copy the inventory to a temporary root, apply each real filesystem fault to the continuum record, and require
    rejection. The changed copy keeps every verdict substring, so only the byte binding can reject it."""
    rejected = []
    for fault in ("delete", "change", "symlink", "symlink-parent"):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            for path in INVENTORY:
                dst = root / path
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src / path, dst)
            target = root / CONTINUUM
            if fault == "delete":
                target.unlink()
            elif fault == "change":
                target.write_bytes(target.read_bytes() + b"\n")
                assert all(n in target.read_text(encoding="utf-8") for n in VERDICTS[CONTINUUM])
            elif fault == "symlink":
                moved = root / "elsewhere" / "REVIEW.md"
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
    entries = spec["status_rows"] + spec["graph"]
    if MUT == "drop-dependency":
        for e in entries:
            if e.get("node") == "math.rn-region.pin-collision":
                e["required"] = [p for p in e["required"] if p != CONTINUUM]
    ok = all(p in INVENTORY for e in entries for p in e["required"])
    ok &= all({CONTINUUM, CONTINUUM_CHECK, P111} <= set(e["required"]) for e in entries if e["uses_P2"])
    ok &= any(e.get("node") == "math.rn-region.witness-collision" and e["proposed"] == "OPEN_ACTIVE"
              for e in spec["graph"])
    ok &= any(e["id"].startswith("D5-collision") and e["proposed"] == "OPEN" for e in spec["status_rows"])
    nodes = {n["id"]: n for n in spec["proposed_graph_nodes"]}
    edges = spec["proposed_graph_edges"]
    if MUT == "drop-edge":
        edges = [e for e in edges if not (e["from"] == "math.rn-region.pin-collision"
                                          and nodes.get(e["to"], {}).get("source") == CONTINUUM)]
    if MUT == "stale-fingerprint":
        for n in nodes.values():
            if n.get("source") == CONTINUUM:
                n["fingerprint"] = "0" * 64
    by_source = {n["source"]: nid for nid, n in nodes.items() if "fingerprint" in n}
    ok &= all(n["fingerprint"] == INVENTORY[n["source"]][0] for n in nodes.values() if "fingerprint" in n)
    have = {(e["from"], e["to"]) for e in edges if e["required"] is True}
    for e in entries:
        src_node = e.get("node") or e.get("graph_node")
        if src_node is None:
            continue
        ok &= all(p in by_source and (src_node, by_source[p]) in have for p in e["required"])
    ok &= "math.d5-pin-neighborhood-first-moment" in nodes
    return ok


def check_tiling():
    """Exact grid check in physical coordinates from the midpoint; torus side 1, s0 = 1/5, r = 1/20."""
    L, s0, r = F(1), F(1, 5), F(1, 20)
    M, S = (-r / 2, F(0)), (r / 2, F(0))

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def covered(X):
        if X in (M, S):
            return True
        n2 = X[0] ** 2 + X[1] ** 2
        pin = d2(X, M) <= (r / 4) ** 2 or d2(X, S) <= (r / 4) ** 2
        collar = n2 <= (4 * r) ** 2 and not pin and MUT != "drop-collar"
        return pin or collar or (4 * r) ** 2 <= n2 <= s0 ** 2 or n2 >= s0 ** 2

    n = 80
    pts = [(L * F(i, n) - L / 2, L * F(j, n) - L / 2) for i in range(n) for j in range(n)]
    fine = [(F(i, 400), F(j, 400)) for i in range(-30, 31) for j in range(-30, 31)]
    return all(covered(X) for X in pts + fine + [M, S])


def check_open(root):
    text = (root / "reviews/d5_offpin_second_moment_20260928/REVIEW.md").read_text(encoding="utf-8")
    return "CANDIDATE pending review and test (catalog C6)" in text and MUT != "close-c6"


def main():
    global MUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutant", choices=MUTANTS)
    MUT = ap.parse_args().mutant
    root = pathlib.Path(".").resolve()
    ident = check_identities(root)
    checks = {"IDENTITIES": ident, "VERDICTS": ident and check_verdicts(root), "NEGATIVES": check_negatives(root),
              "TRANSITIONS": check_transitions(root), "TILING": check_tiling(), "OPEN_C6": check_open(root)}
    passed = all(checks.values()) and len(checks) == 6
    print(json.dumps({"object": "D5-RECONCILIATION-20260929-v2.1", "checks": checks, "passed": passed,
                      "inventory_files": len(INVENTORY),
                      "scope": "identity, verdict-row, filesystem-negative, transition-chain, tiling and open-item "
                               "checks; no mathematics is re-proved"}, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
