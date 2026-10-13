"""Strict child-result contracts for the C6 residual closure workflow.

Engineering guard only. The eight named checks and expected mutant failure
sets are derived from the pinned residual_check.py branches and the original
Python 3.11.16 hosted observations; no mathematical proof is rerun here.
"""

import json

CHECK_NAMES = frozenset((
    "IDENTITIES", "VERDICTS", "LIVE", "REVIEWED", "DEDUCTION",
    "TRANSITIONS", "GATE", "NEGATIVES",
))
EXPECTED_FAILURES = {
    "partial-install": frozenset(("TRANSITIONS",)),
    "allow-symlink": frozenset(("NEGATIVES",)),
    "no-hash": frozenset(("NEGATIVES",)),
    "stale-fingerprint": frozenset(("TRANSITIONS", "GATE")),
    "drop-required-edge": frozenset(("TRANSITIONS", "GATE")),
    "executed-flag": frozenset(("TRANSITIONS", "GATE")),
    "controlling-true": frozenset(("TRANSITIONS", "GATE")),
    "tail-reversed": frozenset(("DEDUCTION",)),
    "pair-identity-broken": frozenset(("DEDUCTION",)),
    "route-c-broken": frozenset(("DEDUCTION",)),
    "drop-review-needle": frozenset(("VERDICTS",)),
    "installed-drift": frozenset(("TRANSITIONS", "GATE")),
    "snapshot-omitted": frozenset(("GATE",)),
    "record-unreviewed": frozenset(("REVIEWED", "TRANSITIONS", "GATE")),
    "reviewed-text-drift": frozenset(("REVIEWED",)),
}
REPORT_KEYS = frozenset((
    "checks", "component_nodes", "gate", "inventory_files", "live_state",
    "object", "passed", "register_state", "scope",
))


def _require(predicate, message):
    if not predicate:
        raise ValueError("C6 residual child contract: " + message)


def _loads(raw):
    _require(type(raw) is bytes, "stdout must be bytes")

    def unique(pairs):
        obj = {}
        for key, value in pairs:
            _require(key not in obj, "duplicate JSON key: " + key)
            obj[key] = value
        return obj

    def reject_constant(value):
        raise ValueError("nonfinite JSON constant: " + value)

    try:
        return json.loads(raw, object_pairs_hook=unique, parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("C6 residual child contract: invalid JSON stdout") from exc


def _check_common(report, baseline):
    _require(type(report) is dict and set(report) == REPORT_KEYS,
             "missing or extra report fields")
    _require(report["object"] == baseline["object"] == "C6-RESIDUAL-CLOSURE-20260930-v1",
             "incorrect object")
    _require(type(report["inventory_files"]) is int and report["inventory_files"] == baseline["inventory_files"],
             "inventory identity changed")
    _require(type(report["component_nodes"]) is int and report["component_nodes"] == baseline["component_nodes"],
             "component identity changed")
    _require(type(report["scope"]) is str and report["scope"] == baseline["scope"],
             "source scope changed")
    _require(report["register_state"] == baseline["register_state"] and
             report["register_state"] in ("baseline", "installed"),
             "register state changed")
    _require(type(report["live_state"]) is dict and
             report["live_state"].get("state") == report["register_state"],
             "live state does not match register state")
    _require(type(report["gate"]) is dict, "gate report must be an object")
    checks = report["checks"]
    _require(type(checks) is dict and set(checks) == CHECK_NAMES and
             all(type(v) is bool for v in checks.values()),
             "invalid or incomplete eight-check result")
    _require(type(report["passed"]) is bool, "passed must be a Boolean")
    return checks


def validate_baseline(process, pinned_bytes):
    """Bind the genuine zero-mutant result to its already-pinned source bytes."""
    _require(process.returncode == 0, "baseline exit must be zero")
    _require(process.stderr == b"", "baseline wrote unexpected stderr")
    _require(process.stdout == pinned_bytes, "baseline stdout differs from pinned result")
    report = _loads(process.stdout)
    _check_common(report, report)
    _require(report["passed"] is True and all(report["checks"].values()),
             "baseline must pass all eight checks")
    return report


def validate_mutant(mutant, process, baseline):
    """Reject crashes, silence, malformed output and failures for the wrong reason."""
    _require(mutant in EXPECTED_FAILURES, "unregistered mutant label")
    _require(process.returncode == 1, "mutant exit must be one")
    _require(process.stderr == b"", "mutant wrote unexpected stderr")
    report = _loads(process.stdout)
    checks = _check_common(report, baseline)
    failed = frozenset(name for name, value in checks.items() if value is False)
    _require(report["passed"] is False and failed == EXPECTED_FAILURES[mutant],
             "mutant failed a different check set: " + mutant)
    return report
