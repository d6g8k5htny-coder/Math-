"""Source-bound publication controls, not a Lean or field acceptance gate."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "reviews/d2_sharp_scalar_floor_20261006"
BASE = {"counts": {"direction_inequalities": 5508, "dominance_checks": 324,
    "endpoint_minimum_checks": 324, "equal_endpoint_cases": 6,
    "example_checks": 1, "native_formula_equalities": 5508,
    "outside_direction_counterexamples": 2, "polynomial_identities": 10,
    "rational_difference_equalities": 2304}, "errors": [],
    "example_floor": "153/86", "example_gain": "68/43", "failures": [],
    "mutant": None, "ok": True,
    "scope": "exact algebra and finite controls for comment6008747995 Part B; not a Lean or field verdict"}
FAILURES = {
    "flip_difference_sign": ["symbolic:F0_x_difference"],
    "omit_F1_factor_four": ["symbolic:endpoint1"],
    "max_for_min": ["direction_floor"],
    "square_input_missing": ["direction_floor", "dominance"],
    "reverse_monotone_direction": ["monotonicity"],
    "example_wrong_denominator": ["example"],
}
CHECKER_SHA256 = "64047e54a8525cd890fcc0f400cd529a357537a901a5de792b49afb71cd669da"


def encoded(report):
    return (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class SharpScalarPublicationTests(unittest.TestCase):
    def run_checker(self, *arguments):
        source = PACKET / "check_partb.py"
        self.assertTrue(source.is_file(), "published checker missing")
        self.assertFalse(source.is_symlink(), "checker must be a regular stored file")
        before = source.read_bytes()
        self.assertEqual(hashlib.sha256(before).hexdigest(), CHECKER_SHA256)
        flags = ["-B"] + (["-O"] if sys.flags.optimize else []) + ["-S"]
        env = dict(os.environ, COLUMNS="80", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, *flags, str(source), *arguments],
                                cwd=ROOT, env=env, capture_output=True, timeout=30)
        self.assertEqual(source.read_bytes(), before)
        return result

    def test_exact_source_inventory(self):
        manifest = PACKET / "SOURCES.json"
        self.assertTrue(manifest.is_file(), "publication manifest missing")
        self.assertFalse(manifest.is_symlink())
        data = json.loads(manifest.read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertEqual(data["scientific_effect"], "NONE")
        self.assertEqual(data["publication_review_status"], "PENDING_SOURCE_BOUND_REVIEW")
        expected = {
            "reviews/d2_sharp_scalar_floor_20261006/NOTE.md",
            "reviews/d2_sharp_scalar_floor_20261006/check_partb.py",
            "tests/test_d2_sharp_scalar_floor.py",
        }
        self.assertEqual({item["path"] for item in data["files"]}, expected)
        self.assertEqual(len(data["files"]), len(expected))
        self.assertEqual({p.name for p in PACKET.iterdir()},
                         {"NOTE.md", "check_partb.py", "SOURCES.json"})
        for item in data["files"]:
            with self.subTest(path=item["path"]):
                path = ROOT / item["path"]
                self.assertTrue(path.is_file())
                self.assertFalse(path.is_symlink())
                raw = path.read_bytes()
                self.assertEqual(len(raw), item["bytes"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), item["sha256"])
                self.assertEqual(git_blob(raw), item["git_blob"])
        self.assertEqual(data["comment_mathematical_review"]["comment_id"], 6016072968)
        self.assertEqual(data["comment_mathematical_review"]["scope"], "comment Part B only; not this publication code")

    def test_baseline_exact_report(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, encoded(BASE))
        self.assertEqual(result.stderr, b"")

    def test_all_six_named_rejection_reports(self):
        for name, failures in FAILURES.items():
            with self.subTest(mutant=name):
                expected = dict(BASE, mutant=name, failures=failures, ok=False)
                result = self.run_checker("--mutant", name)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(result.stdout, encoded(expected))
                self.assertEqual(result.stderr, b"")

    def test_unknown_mutant_is_usage_error_not_mathematical_rejection(self):
        result = self.run_checker("--mutant", "UNKNOWN")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        # Explicit presentation alternatives; the wrong label and all choices stay exact.
        endings = tuple(
            ("check_partb.py: error: argument --mutant: invalid choice: 'UNKNOWN' "
             "(choose from " + ", ".join(render(name) for name in FAILURES) + ")\n").encode()
            for render in (str, repr)
        )
        self.assertTrue(result.stderr.startswith(b"usage: check_partb.py "))
        self.assertTrue(result.stderr.endswith(endings), result.stderr)
        self.assertNotIn(b"Traceback", result.stderr)

    def test_extra_argument_is_usage_error_not_success(self):
        result = self.run_checker("--unexpected")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr.startswith(b"usage: check_partb.py "))
        self.assertTrue(result.stderr.endswith(b"check_partb.py: error: unrecognized arguments: --unexpected\n"))
        self.assertNotIn(b"Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
