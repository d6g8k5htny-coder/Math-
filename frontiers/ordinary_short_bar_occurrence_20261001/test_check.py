"""Exact finite controls; none substitutes for the packet's analytic proof."""

from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

import check
import verify_sources


class CountControls(unittest.TestCase):
    def test_counts_preserve_bar_multiplicity(self):
        # Replacing K by 1{K>0} loses both the mean and the weighted multi mass.
        self.assertEqual(
            check.count_statistics({0: F(1, 2), 1: F(1, 3), 3: F(1, 6)}),
            {"mean": F(5, 6), "occurrence": F(1, 2),
             "excess": F(1, 3), "multi_mass": F(1, 2),
             "second_factorial": F(1), "conditional_multi": F(1, 3)},
        )

    def test_first_moment_alone_does_not_select_one_bar(self):
        for n in (2, 5, 16, 31):
            epsilon = F(1, n * n)
            s = check.count_statistics({0: 1 - epsilon / 2, 2: epsilon / 2})
            self.assertEqual(s["mean"], epsilon)
            self.assertEqual(s["occurrence"], epsilon / 2)
            self.assertEqual(s["multi_mass"], epsilon)
            self.assertEqual(s["conditional_multi"], 1)

    def test_small_multi_probability_does_not_bound_multi_mass(self):
        for n in (2, 5, 16, 31):
            p1, pn = F(1, n * n), F(1, n ** 3)
            s = check.count_statistics({0: 1 - p1 - pn, 1: p1, n: pn})
            self.assertEqual(pn / p1, F(1, n))
            self.assertEqual(s["multi_mass"] / p1, 1)

    def test_multi_mass_control_does_not_control_factorials(self):
        for n in (2, 5, 16, 31):
            p1, pn = F(1, n * n), F(1, n ** 4)
            s = check.count_statistics({0: 1 - p1 - pn, 1: p1, n: pn})
            self.assertEqual(s["multi_mass"] / p1, F(1, n))
            self.assertEqual(s["second_factorial"] / p1, 1 - F(1, n))

    def test_count_identities_and_singleton_tv(self):
        for n in (2, 3, 7, 15):
            s = check.count_statistics({0: F(1, 4), 1: F(1, 4), n: F(1, 2)})
            self.assertEqual(s["mean"] - s["occurrence"], s["excess"])
            self.assertLessEqual(s["excess"], s["multi_mass"])
            self.assertLessEqual(s["multi_mass"], 2 * s["excess"])
            self.assertEqual(s["conditional_multi"], F(2, 3))

    def test_zero_occurrence_does_not_invent_a_conditional_law(self):
        s = check.count_statistics({0: F(1)})
        self.assertEqual(s["mean"], 0)
        self.assertEqual(s["excess"], 0)
        self.assertIsNone(s["conditional_multi"])

    def test_invalid_count_laws_are_rejected(self):
        for law in ({-1: 1}, {True: 1}, {1.0: 1}, {0: F(1, 2)},
                    {0: 2, 1: -1}, {1: 1.0}, {1: True}, {}):
            with self.subTest(law=law), self.assertRaises(ValueError):
                check.count_statistics(law)


class MarkControls(unittest.TestCase):
    def test_marked_laws_retain_two_different_samplings(self):
        s = check.mark_statistics([(F(1, 2), ()), (F(1, 3), ("red",)),
                                   (F(1, 6), ("blue", "blue", "green"))])
        self.assertEqual(s["intensity"], {"red": F(2, 5), "blue": F(2, 5), "green": F(1, 5)})
        self.assertEqual(s["field_first"], {"red": F(2, 3), "blue": F(2, 9), "green": F(1, 9)})
        self.assertEqual(s["excess_law"], {"blue": F(2, 3), "green": F(1, 3)})
        self.assertEqual(s["tv"], F(4, 15))
        self.assertEqual(s["tv_bound"], F(2, 5))

    def test_excess_mixture_identity_and_total_variation_bound(self):
        # Vary actual fields and marks, including a tuple-valued mark.
        for i in range(7):
            for j in range(7 - i):
                s = check.mark_statistics([(F(i, 6), ()),
                    (F(j, 6), ("a",)),
                    (F(6 - i - j, 6), ("b", ("c", 1), "b"))])
                if s["mean"] == 0:
                    self.assertIsNone(s["tv"])
                    continue
                p, m, e = s["occurrence"], s["mean"], s["excess"]
                for label in set(s["field_first"]) | set(s["intensity"]):
                    defect = (s["excess_law"] or {}).get(label, F(0))
                    self.assertEqual(s["intensity"].get(label, 0),
                        p / m * s["field_first"].get(label, 0) + e / m * defect)
                self.assertLessEqual(s["tv"], e / m)

    def test_no_excess_and_empty_field_cases(self):
        s = check.mark_statistics([(F(1, 2), ()), (F(1, 3), ("a",)), (F(1, 6), ("b",))])
        self.assertEqual(s["field_first"], {"a": F(2, 3), "b": F(1, 3)})
        self.assertEqual(s["field_first"], s["intensity"])
        self.assertIsNone(s["excess_law"])
        self.assertEqual(s["tv"], 0)
        z = check.mark_statistics([(F(1), ())])
        for name in ("field_first", "intensity", "excess_law", "tv", "tv_bound"):
            self.assertIsNone(z[name])

    def test_tv_uses_half_the_l1_distance(self):
        self.assertEqual(check.total_variation({"a": F(3, 4), "b": F(1, 4)},
                                              {"b": F(1, 2), "c": F(1, 2)}), F(3, 4))
        self.assertEqual(check.total_variation({"a": F(1)}, {"b": F(1)}), 1)

    def test_coalescing_equal_marks_does_not_size_bias_fields(self):
        s = check.mark_statistics([(F(1, 2), ("a",)), (F(1, 2), ("b", "b", "b"))])
        self.assertEqual(s["field_first"], {"a": F(1, 2), "b": F(1, 2)})
        self.assertEqual(s["intensity"], {"a": F(1, 4), "b": F(3, 4)})
        self.assertEqual(s["tv"], F(1, 4))

    def test_invalid_mark_laws_are_rejected(self):
        cases = [[], [(F(1, 2), ("a",))], [(-1, ()), (2, ("a",))],
                 [(1.0, ("a",))], [(True, ())], [(1, "not-a-mark-sequence")],
                 [(1, ([1],))]]
        for fields in cases:
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                check.mark_statistics(fields)
        for left in ({}, {"a": F(1, 2)}, {"a": -1, "b": 2}, {"a": 1.0}):
            with self.subTest(left=left), self.assertRaises(ValueError):
                check.total_variation(left, {"a": 1})


class ScalingControls(unittest.TestCase):
    def test_radial_and_pin_jacobians_give_twelve_over_three(self):
        self.assertEqual(check.radial_pushforward(12, 1), (F(4), F(-2, 3), F(-1, 3)))
        self.assertEqual(check.radial_pushforward(7, 5), (F(7, 3), F(-2), F(1)))
        self.assertEqual(check.radial_pushforward(6, 0, 2), (F(3), F(-1, 2), F(-1, 2)))

    def test_cumulative_integral_agrees_with_density(self):
        self.assertEqual(check.radial_cumulative(12, 1), (F(6), F(-2, 3), F(2, 3)))
        for power in (0, 1, 3, 5):
            density = check.radial_pushforward(F(7, 2), power)
            cumulative = check.radial_cumulative(F(7, 2), power)
            self.assertEqual(cumulative[0] * cumulative[2], density[0])
            self.assertEqual(cumulative[1], density[1])
            self.assertEqual(cumulative[2] - 1, density[2])

    def test_density_evaluation_uses_gap_derivative(self):
        self.assertEqual(check.radial_density_at_r(12, 1, 2, F(1, 4)), 8)
        self.assertEqual(check.radial_density_at_r(2, 5, 3, F(1, 2)), F(1, 36))
        self.assertEqual(check.radial_density_at_r(5, 0, 3, F(1, 2), 2), F(5, 3))

    def test_error_orders_include_the_jacobian(self):
        # A radial density r^a dr becomes ell^((a-2)/3), not ell^(a/3).
        table = {1: F(-1, 3), 2: F(0), 4: F(2, 3), 5: F(1)}
        for power, expected in table.items():
            self.assertEqual(check.radial_pushforward(1, power)[2], expected)

    def test_invalid_scaling_inputs_are_rejected(self):
        for args in ((1, 1, 0), (1.0, 1, 3), (1, True, 3), (1, 1, True)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                check.radial_pushforward(*args)
        with self.assertRaises(ValueError):
            check.radial_cumulative(1, -1)
        for k, r in ((0, 1), (1, 0), (-1, 1), (1, -1)):
            with self.subTest(k=k, r=r), self.assertRaises(ValueError):
                check.radial_density_at_r(1, 1, k, r)


class FoldControls(unittest.TestCase):
    def test_endpoint_jet_and_third_derivative(self):
        self.assertEqual(check.fold_jet(12, F(1, 2), F(-1, 4)),
                         (F(1, 8), F(0), F(-6), F(24)))
        self.assertEqual(check.fold_jet(12, F(1, 2), F(1, 4)),
                         (F(-1, 8), F(0), F(6), F(24)))
        self.assertEqual(check.fold_jet(12, F(1, 2), 0),
                         (F(0), F(-3, 4), F(0), F(24)))

    def test_fold_gap_matches_kappa_r_cubed(self):
        for a, r in ((F(3), F(1, 5)), (F(7, 3), F(2, 7)), (F(12), F(1, 2))):
            left, right = check.fold_jet(a, r, -r / 2), check.fold_jet(a, r, r / 2)
            self.assertEqual(left[1], 0)
            self.assertEqual(right[1], 0)
            self.assertLess(left[2], 0)
            self.assertGreater(right[2], 0)
            self.assertEqual(left[0] - right[0], a * r ** 3 / 6)
            self.assertEqual(left[3], 2 * a)

    def test_derivative_is_strictly_convex_and_two_root_model_is_oriented(self):
        r, a = F(2, 3), F(9, 2)
        values = [check.fold_jet(a, r, x)[1] for x in (-r, -r / 2, 0, r / 2, r)]
        self.assertEqual(values, [F(3, 2), F(0), F(-1, 2), F(0), F(3, 2)])
        for x, y in ((F(-2), F(1)), (F(-1, 3), F(2, 5))):
            slope = (check.fold_jet(a, r, y)[2] - check.fold_jet(a, r, x)[2]) / (y - x)
            self.assertEqual(slope, 9)
            self.assertEqual(check.fold_jet(a, r, (x + y) / 2)[3], slope)

    def test_degenerate_or_inexact_fold_inputs_are_rejected(self):
        for a, r, x in ((0, 1, 0), (-1, 1, 0), (1, 0, 0), (1, -1, 0),
                        (1.0, 1, 0), (1, 1, 0.1), (True, 1, 0)):
            with self.subTest(a=a, r=r, x=x), self.assertRaises(ValueError):
                check.fold_jet(a, r, x)

    def test_curved_ridge_third_derivative_is_not_raw_partial(self):
        # f=b-kr^3/2+2kx^3-3kr^2*x/2-(z-q(x^2-r^2/4))^2/2.
        # Raw f_xxx vanishes at x=1/4 here; reduced g''' remains 12.
        self.assertEqual(check.curved_ridge_third(1, F(1, 2), 2, F(1, 4)), (F(0), F(12)))
        self.assertEqual(check.curved_ridge_third(1, F(1, 2), 2, F(1, 8)), (F(6), F(12)))
        self.assertEqual(check.curved_ridge_third(F(1, 2), F(1, 3), 1, F(-1, 4)), (F(9), F(6)))
        self.assertEqual(check.curved_ridge_third(2, F(1, 2), 0, 3), (F(24), F(24)))
        for args in ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0.5, 1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                check.curved_ridge_third(*args)


class SourceControls(unittest.TestCase):
    def test_seven_exact_imported_source_identities(self):
        self.assertEqual(verify_sources.verify_sources(), 7)

    @staticmethod
    def entry(path, data):
        return {"local_path": path, "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}

    def test_source_byte_and_metadata_tampering_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = b"exact source\n"
            (root / "source").write_bytes(data)
            entry = self.entry("source", data)
            verify_sources.verify_entry(root, entry)
            for key, value in (("bytes", len(data) + 1), ("sha256", "0" * 64), ("blob", "0" * 40)):
                with self.subTest(key=key), self.assertRaises(ValueError):
                    verify_sources.verify_entry(root, dict(entry, **{key: value}))
            (root / "source").write_bytes(b"wrong source\n")
            with self.assertRaises(ValueError):
                verify_sources.verify_entry(root, entry)

    def test_source_path_escape_and_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = b"source"
            (root / "real").write_bytes(data)
            (root / "alias").symlink_to(root / "real")
            for path in ("../real", str(root / "real"), "./real", "alias"):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    verify_sources.verify_entry(root, self.entry(path, data))

    def test_manifest_whitespace_tampering_is_rejected(self):
        packet = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "SOURCES.json"
            manifest.write_bytes((packet / "SOURCES.json").read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "manifest digest"):
                verify_sources.verify_sources(packet.parents[1], manifest)


MUTATIONS = (
    ("mean-loses-multiplicity", "p * k for k, p in weights.items()), Fraction(0))", "p * (k > 0) for k, p in weights.items()), Fraction(0))"),
    ("occurrence-size-biased", "p for k, p in weights.items() if k > 0", "p * k for k, p in weights.items() if k > 0"),
    ("excess-drops-minus-one", "p * max(k - 1, 0)", "p * k"),
    ("multi-loses-count-weight", "p * k for k, p in weights.items() if k >= 2", "p for k, p in weights.items() if k >= 2"),
    ("factorial-becomes-excess", "p * k * (k - 1)", "p * max(k - 1, 0)"),
    ("conditional-multi-wrong-divisor", "multi_probability / occurrence", "multi_probability / mean"),
    ("accept-bool-probability", "isinstance(value, bool) or not isinstance(value, (int, Fraction))", "not isinstance(value, (int, Fraction))"),
    ("negative-probability", "any(p < 0 for p in weights.values()) or sum(weights.values()) != 1", "sum(weights.values()) != 1"),
    ("tv-misses-half", "Fraction(0)) / 2", "Fraction(0))"),
    ("intensity-loses-size-bias", "intensity[label] += probability", "intensity[label] += probability / k"),
    ("field-sampling-size-biased", "field[label] += probability / k", "field[label] += probability"),
    ("excess-mark-misses-minus-one", "probability * (k - 1) / k", "probability"),
    ("tv-bound-wrong-normalizer", "tv_bound=e / m", "tv_bound=e / p"),
    ("pushforward-misses-cubic-divisor", "return amplitude / q, -order, order - 1", "return amplitude, -order, order - 1"),
    ("pushforward-wrong-kappa-power", "return amplitude / q, -order, order - 1", "return amplitude / q, order, order - 1"),
    ("pushforward-misses-jacobian-power", "return amplitude / q, -order, order - 1", "return amplitude / q, -order, Fraction(a, q)"),
    ("cumulative-misses-integration", "return amplitude / (a + 1), -order, order", "return amplitude, -order, order"),
    ("density-wrong-gap-derivative", "q * kappa * r ** (q - 1)", "kappa * r ** q"),
    ("fold-gap-wrong-sign", "x ** 3 / 3 - r ** 2 * x / 4", "x ** 3 / 3 + r ** 2 * x / 4"),
    ("fold-critical-pins-shift", "a * (x ** 2 - r ** 2 / 4)", "a * (x ** 2 - r ** 2)"),
    ("fold-third-derivative-dropped", "2 * a * x, 2 * a)", "2 * a * x, Fraction(0))"),
    ("curved-ridge-tangent-sign", "v = -derivative(1, 1) / derivative(0, 2)", "v = derivative(1, 1) / derivative(0, 2)"),
    ("curved-ridge-raw-for-reduced", "return raw, reduced", "return raw, raw"),
)


def run_mutations():
    """Change executable behavior in scratch trees; reject each in both modes."""
    packet = Path(__file__).resolve().parent
    source = (packet / "check.py").read_text()
    manifest = json.loads((packet / "SOURCES.json").read_text())
    results = []
    with tempfile.TemporaryDirectory(prefix="c52-finite-mutants-") as directory:
        root = Path(directory)
        target = root / "frontiers" / packet.name
        target.mkdir(parents=True)
        for name in ("test_check.py", "verify_sources.py", "SOURCES.json"):
            shutil.copyfile(packet / name, target / name)
        for entry in manifest["sources"]:
            destination = root / entry["local_path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(packet.parents[1] / entry["local_path"], destination)
        for name, old, new in (("baseline", "", ""),) + MUTATIONS:
            if name != "baseline" and source.count(old) != 1:
                raise RuntimeError("mutation anchor is not unique: " + name)
            mutated = source if name == "baseline" else source.replace(old, new, 1)
            (target / "check.py").write_text(mutated)
            for optimized in (False, True):
                command = [sys.executable, "-B"] + (["-O"] if optimized else []) + ["-S", str(target / "test_check.py")]
                run = subprocess.run(command, capture_output=True, text=True, timeout=30)
                output = run.stdout + run.stderr
                if name == "baseline":
                    good = run.returncode == 0 and "\nOK\n" in output
                else:
                    good = run.returncode != 0 and "Ran " in output and "FAILED (" in output
                row = {"mutation": name, "mode": "optimized" if optimized else "normal",
                       "returncode": run.returncode, "expected_outcome": good}
                results.append(row)
                if not good:
                    print(output)
                    print(json.dumps(results, indent=2))
                    raise RuntimeError("unexpected mutation outcome: " + name)
    print(json.dumps({"mutations_per_mode": len(MUTATIONS), "baseline_modes": 2,
                      "results": results, "scope": "Finite implementation controls only"}, indent=2))


if __name__ == "__main__":
    if sys.argv[1:] == ["--mutants"]:
        run_mutations()
    else:
        unittest.main()
