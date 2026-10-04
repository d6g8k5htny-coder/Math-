"""Register execution dry run (standard library only; nothing is written to the repository unless asked).

Composes the three merged declarative proposals, in their stated order, on a scratch copy of the repository:
  1. Math-#167  reviews/register_alignment_20260930/PROPOSED_TRANSITIONS.json  (alignment_check.apply)
  2. Math-#160  reviews/c6_witness_collision_reconciliation_20260929/PROPOSED_TRANSITIONS.json  (execution_order steps 1-4,
     main path: residual node created separately; selector cells per selector_region_proposal; the old node's fields as
     Math-#173's deferred transition proposes them)
  3. Math-#173  reviews/c6_residual_closure_20260930/PROPOSED_TRANSITIONS.json  (residual_check.build 'final', then the
     deferred old-node edges once Math-#160 step 4 is applied)
then validates the executed graph with the downstream hard gate and runs the three records' checkers against the
executed copy: each must pass, report its register as 'installed' and print its packet's RESULTS_INSTALLED.json byte
for byte under both interpreter modes. With --mutants every mutant of every checker must be rejected on the executed
copy as well.

Usage, from the repository root:
  python -B -S reviews/register_execution_readiness_20260930/execution_dryrun.py [--out DIR] [--skip-old-node-move]
         [--selector-node-only] [--mutants] [--write-installed-results]
  --out DIR              keep the executed copy in DIR: a path outside the repository (not inside it, not one of its
                         parents) that does not exist or is an empty directory; nothing is ever deleted; default: a
                         temporary directory
  --skip-old-node-move   stop after Math-#160 steps 1-3: witness node left OPEN_ACTIVE, Math-#173's deferred edges not applied
  --selector-node-only   Math-#160's node-only alternative for the selector table (table unchanged)
  --mutants              also run every checker mutant on the executed copy
  --write-installed-results   maintenance of this packet only: write each checker's installed-state output into its packet
                              as RESULTS_INSTALLED.json, and only after every checker (and every mutant, if requested)
                              has passed (then the normal run compares against it)
Exit status 0 iff the executed graph validates and every checker (and mutant, if requested) behaves as required.
Scientific effect: NONE. This is not an execution: the repository's GRAPH.json and SELECTOR_REGION.json are not touched.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile

GRAPH = "frontiers/downstream_gate_20260925/GRAPH.json"
SELECTOR = "frontiers/downstream_gate_20260925/SELECTOR_REGION.json"
HARD_GATE = "frontiers/downstream_gate_20260925/hard_gate.py"
PACKETS = {
    "Math-#167": ("reviews/register_alignment_20260930", "alignment_check.py"),
    "Math-#160": ("reviews/c6_witness_collision_reconciliation_20260929", "reconciliation_check.py"),
    "Math-#173": ("reviews/c6_residual_closure_20260930", "residual_check.py"),
}
WIT = "math.rn-region.witness-collision"
RES = "math.rn-region.witness-collision.leading-mass-localization"
AGG = "math.c6-witness-collision-factorial-moment"
SUPERSESSION = "regional.shrinking-regions.analytic-route"
EIGHT_EXTRA = ("math.rn-mesoscopic-reduction",)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    argv, sys.argv = sys.argv, [str(path)]
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.argv = argv
    return mod


def edge_key(e):
    return (e["from"], e["to"], e["required"], e["relation"])


def add_edges(graph, edges):
    have = {(e["from"], e["to"], e["relation"]) for e in graph["edges"]}
    added = 0
    for e in edges:
        key = (e["from"], e["to"], e["relation"])
        if key in have:
            continue
        graph["edges"].append({"from": e["from"], "to": e["to"], "required": e["required"], "relation": e["relation"]})
        have.add(key)
        added += 1
    return added


def compose(out, skip_old_node_move, selector_node_only):
    hg = load_module("hard_gate", out / HARD_GATE)
    al = load_module("alignment_check", out / PACKETS["Math-#167"][0] / PACKETS["Math-#167"][1])
    rc = load_module("residual_check", out / PACKETS["Math-#173"][0] / PACKETS["Math-#173"][1])
    g0 = json.loads((out / GRAPH).read_text(encoding="utf-8"))
    sel0 = json.loads((out / SELECTOR).read_text(encoding="utf-8"))
    report = {"live": {"nodes": len(g0["nodes"]), "edges": len(g0["edges"])}}
    rep0 = hg.closure_report(g0)
    holds0 = {h["node"] for h in rep0["hold_proposals"]}
    report["live"]["gate_ok"] = rep0["gate_ok"]
    report["live"]["holds"] = sorted(holds0)
    # 1. Math-#167
    spec167 = al.load_spec(out)
    g1 = al.apply(spec167, g0)
    report["step_167"] = {"nodes": len(g1["nodes"]), "edges": len(g1["edges"]),
                          "flipped": sorted(t["node"] for t in spec167["transitions"])}
    # 2. Math-#160, steps 1-3 (and 4 unless skipped)
    spec160 = json.loads((out / PACKETS["Math-#160"][0] / "PROPOSED_TRANSITIONS.json").read_text(encoding="utf-8"))
    spec173 = rc.load_spec(out)
    g2 = copy.deepcopy(g1)
    kept = []
    for n in spec160["proposed_graph_nodes"]:
        if n["id"] in g2["nodes"]:
            kept.append(n["id"])
            continue
        g2["nodes"][n["id"]] = {k: v for k, v in n.items() if k != "id"}
    added = add_edges(g2, [e for e in spec160["proposed_graph_edges"] if e["from"] != WIT])
    sel = copy.deepcopy(sel0)
    srp = spec160["selector_region_proposal"]
    if not selector_node_only:
        for s, v in srp["cells"].items():
            for reg in srp["regions"]:
                sel["selectors"][s][reg] = v
        ids = ["math.rn-region." + reg for reg in srp["regions"]]
        sel["covered_region_ids"] = list(sel["covered_region_ids"]) + [i for i in ids if i not in sel["covered_region_ids"]]
        sel["open_region_ids"] = [i for i in sel["open_region_ids"] if i not in ids]
    report["step_160"] = {"nodes": len(g2["nodes"]), "edges_after_steps_1_3": len(g2["edges"]) , "nodes_already_live": kept,
                          "selector": "node-only alternative (table unchanged)" if selector_node_only else "cells and region ids per selector_region_proposal"}
    if not skip_old_node_move:
        t1 = spec173["transitions"][1]
        p = t1["proposed"]
        w = g2["nodes"][WIT]
        w.update({"classification": p["classification"], "controlling": p["controlling"], "fingerprint": p["fingerprint"],
                  "scope": p["scope"], "explicit_limits": p["explicit_limits"], "review_disposition": p["review_disposition"],
                  "review_sources": [r["ref"] for r in p["review_sources"]],
                  "review_basis": [{"review": r["ref"], "provider": r.get("provider", "unstated"), "verdict": r.get("verdict", "")}
                                   for r in p["review_sources"]]})
        if p.get("notes"):
            w["notes"] = p["notes"]
        added += add_edges(g2, [e for e in spec160["proposed_graph_edges"] if e["from"] == WIT])
        report["step_160"]["step_4"] = "witness node PROVED_REVIEWED with Math-#173's deferred-transition fields; its evidence edges added"
    else:
        report["step_160"]["step_4"] = "not applied (--skip-old-node-move): witness node left as it is"
    report["step_160"]["edges_added"] = added
    # 3. Math-#173
    _, g3 = rc.build(spec173, g2, "final")
    deferred = [e for e in spec173["proposed_graph_edges"] if e.get("deferred_with")]
    d_added = 0 if skip_old_node_move else add_edges(g3, deferred)
    report["step_173"] = {"nodes": len(g3["nodes"]), "edges": len(g3["edges"]), "deferred_edges_applied": d_added,
                          "residual": g3["nodes"][RES]["classification"]}
    # validate
    hg.validate_graph_fail_closed(g3)
    rep3 = hg.closure_report(g3)
    holds3 = {h["node"]: h.get("unsatisfied_required") for h in rep3["hold_proposals"]}
    snap_old, snap_new = rc.snapshot(out, g0), rc.snapshot(out, g3)
    ri = hg.reverse_impact_between(g0, g3, old_sources=snap_old, new_sources=snap_new)
    watch = [WIT, RES, AGG, SUPERSESSION, *EIGHT_EXTRA, *(t["node"] for t in spec167["transitions"])]
    report["executed"] = {
        "nodes": len(g3["nodes"]), "edges": len(g3["edges"]), "validate_graph_fail_closed": "OK",
        "gate_ok": rep3["gate_ok"], "illegal_controlling": rep3.get("illegal_controlling"),
        "holds_new": {k: v for k, v in holds3.items() if k not in holds0}, "holds_cleared": sorted(holds0 - set(holds3)),
        "classifications": {nid: g3["nodes"].get(nid, {}).get("classification") for nid in watch},
        "held": sorted(nid for nid in watch if nid in holds3),
        "reverse_impact": {"changed_nodes": len(ri["changed_nodes"]), "impacted": len(ri["impacted"]),
                           "source_snapshots_supplied": ri["source_snapshots_supplied"]},
        "d4_region_complement": hg.d4_region_complement(g3) if hasattr(hg, "d4_region_complement") else None,
    }
    (out / GRAPH).write_text(json.dumps(g3, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / SELECTOR).write_text(json.dumps(sel, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def write_installed_outputs(root, outputs):
    """Prepare all pins before replacing any; roll back recoverable install failures.

    This maintenance operation requires an exclusively owned checkout. It is not
    a cross-file atomic transaction against process termination or another writer.
    Symlink paths are rejected; replacing a regular hardlinked pin preserves its
    other names. A failed rollback retains its backup and reports its location.
    """
    root = root.resolve()
    originals, modes = {}, {}
    for name, (folder, _) in PACKETS.items():
        target = root / folder / "RESULTS_INSTALLED.json"
        relative = target.relative_to(root)
        for i in range(1, len(relative.parts) + 1):
            part = root.joinpath(*relative.parts[:i])
            if part.is_symlink():
                raise ValueError("symlink output path rejected: " + str(part))
        if not target.parent.is_dir():
            raise ValueError("output parent directory missing: " + str(target.parent))
        if target.exists() and not stat.S_ISREG(target.stat().st_mode):
            raise ValueError("regular output file required: " + str(target))
        originals[target] = target.read_bytes() if target.exists() else None
        modes[target] = stat.S_IMODE(target.stat().st_mode) if target.exists() else 0o644

    temporary, retained, staged, backups, installed = [], set(), {}, {}, []

    def stage(target, data):
        fd, name = tempfile.mkstemp(prefix=".installed-result-", dir=target.parent)
        path = pathlib.Path(name)
        temporary.append(path)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        path.chmod(modes[target])
        return path

    primary_error = None
    try:
        for name, (folder, _) in PACKETS.items():
            target = root / folder / "RESULTS_INSTALLED.json"
            staged[target] = stage(target, outputs[name])
            backups[target] = stage(target, originals[target]) if originals[target] is not None else None
        try:
            for target, replacement in staged.items():
                os.replace(replacement, target)
                installed.append(target)
        except BaseException as error:
            failures = []
            for target in reversed(installed):
                try:
                    if backups[target] is None:
                        target.unlink()
                    else:
                        os.replace(backups[target], target)
                except OSError as rollback_error:
                    if backups[target] is not None:
                        retained.add(backups[target])
                    failures.append(str(target) + ": " + str(rollback_error)
                                    + "; backup=" + str(backups[target]))
            if failures:
                raise RuntimeError("output rollback incomplete: " + "; ".join(failures)) from error
            raise
    except BaseException as error:
        primary_error = error
        raise
    finally:
        cleanup_errors = []
        for path in temporary:
            if path not in retained:
                try:
                    path.unlink(missing_ok=True)
                except OSError as error:
                    cleanup_errors.append(str(path) + ": " + str(error))
        if cleanup_errors:
            prior = (str(primary_error) if primary_error is not None
                     else "output installation completed")
            raise RuntimeError(prior + "; temporary cleanup incomplete: "
                               + "; ".join(cleanup_errors)) from primary_error


def run_checkers(root, out, mutants, write_installed):
    """Run every checker (both interpreter modes, and every mutant if asked) on the executed copy; then, only if all of
    that passed, write the pinned installed outputs if asked; then compare with the pinned files."""
    results, outputs = {}, {}
    valid = True
    for name, (pdir, script) in PACKETS.items():
        entry = {}
        outs = {}
        for flags in (("-B", "-S"), ("-B", "-O", "-S")):
            r = subprocess.run([sys.executable, *flags, str(out / pdir / script)], cwd=out, capture_output=True, timeout=900)
            outs[flags] = r.stdout
            try:
                payload = json.loads(r.stdout)
            except Exception:
                payload = {}
            entry[" ".join(flags)] = {"rc": r.returncode, "checks": payload.get("checks"), "passed": payload.get("passed"),
                                      "register_state": payload.get("register_state")}
            valid &= r.returncode == 0 and payload.get("passed") is True and payload.get("register_state") == "installed"
        entry["modes_identical"] = outs[("-B", "-S")] == outs[("-B", "-O", "-S")]
        valid &= entry["modes_identical"]
        if mutants:
            src = (out / pdir / script).read_text(encoding="utf-8")
            names = re.findall(r'"([a-z0-9-]+)"', re.search(r"MUTANTS = \((.*?)\)\n", src, re.S).group(1))
            rejected, not_rejected = [], []
            for m in names:
                r = subprocess.run([sys.executable, "-B", "-S", str(out / pdir / script), "--mutant", m], cwd=out,
                                   capture_output=True, timeout=900)
                (rejected if r.returncode == 1 else not_rejected).append(m)
            entry["mutants_rejected"] = len(rejected)
            entry["mutants_not_rejected"] = not_rejected
            valid &= not not_rejected and len(rejected) == len(names)
        results[name] = entry
        outputs[name] = outs[("-B", "-S")]
    if write_installed and valid:
        try:
            write_installed_outputs(root, outputs)
        except (OSError, ValueError, RuntimeError) as error:
            for entry in results.values():
                entry.update(written=None, write_error=str(error), matches_RESULTS_INSTALLED=None)
            return False, results
    ok = valid
    for name, (pdir, script) in PACKETS.items():
        entry = results[name]
        pinned = root / pdir / "RESULTS_INSTALLED.json"
        if write_installed and valid:                       # never on a failed run (Codex 4143661525)
            entry["written"] = str(pinned.relative_to(root))
        elif write_installed:
            entry["written"] = None
        if pinned.exists():
            entry["matches_RESULTS_INSTALLED"] = pinned.read_bytes() == outputs[name]
            entry["RESULTS_INSTALLED_sha256"] = hashlib.sha256(pinned.read_bytes()).hexdigest()
            ok &= entry["matches_RESULTS_INSTALLED"]
        else:
            entry["matches_RESULTS_INSTALLED"] = None
            ok = False
    return ok, results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--skip-old-node-move", action="store_true")
    ap.add_argument("--selector-node-only", action="store_true")
    ap.add_argument("--mutants", action="store_true")
    ap.add_argument("--write-installed-results", action="store_true")
    args = ap.parse_args()
    root = pathlib.Path(".").resolve()
    for rel in (GRAPH, SELECTOR, HARD_GATE, *(p + "/" + s for p, s in PACKETS.values())):
        if not (root / rel).is_file():
            print(json.dumps({"error": "run from the repository root; missing " + rel}))
            return 2
    tmp = None
    if args.out:
        out = pathlib.Path(args.out).resolve()
        if root == out or root in out.parents or out in root.parents:
            print(json.dumps({"error": "--out must lie outside the repository (neither inside it nor one of its parents)"}))
            return 2
        if out.exists() and (not out.is_dir() or any(out.iterdir())):   # nothing is ever deleted (Codex 4143661496)
            print(json.dumps({"error": "--out must not exist or must be an empty directory; nothing is deleted"}))
            return 2
    else:
        tmp = tempfile.mkdtemp(prefix="register-dryrun-")
        out = pathlib.Path(tmp)
    shutil.copytree(root, out, symlinks=False, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
    for p in out.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    scenario = {"old_node_move": not args.skip_old_node_move, "selector": "node-only" if args.selector_node_only else "cells"}
    try:
        try:
            report = compose(out, args.skip_old_node_move, args.selector_node_only)
            composed = True
        except Exception as ex:
            report, composed = {"composition_error": repr(ex)[:500]}, False
        ok, checkers = (run_checkers(root, out, args.mutants, args.write_installed_results) if composed else (False, {}))
        for p in out.rglob("__pycache__"):
            shutil.rmtree(p, ignore_errors=True)
    finally:
        if tmp is not None:
            shutil.rmtree(tmp, ignore_errors=True)
    payload = {"object": "REGISTER-EXECUTION-DRYRUN-20260930-v1", "scenario": scenario, "composition": report,
               "checkers": checkers, "mutants_run": args.mutants, "passed": bool(composed and ok),
               "scientific_effect": "NONE", "repository_write_requested": bool(args.write_installed_results),
               "repository_written": (None if any("write_error" in entry for entry in checkers.values())
                                      else any(entry.get("written") for entry in checkers.values())),
               "meaning": "composition of three declarative proposals on a scratch copy; validation by the hard gate; the "
                          "records' own checkers in their installed state; not an execution, not acceptance"}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
