"""Fail-closed C293 hosted-registration tests; no Lean execution or theorem acceptance."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / "tools/c293_hosted_verify.py"
spec = importlib.util.spec_from_file_location("c293_hosted_verify", MODULE_PATH)
c293 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c293)


class C293HostedRegistrationTests(unittest.TestCase):
    def test_actual_published_source_and_pin_crosswalk(self):
        result = c293.verify_sources()
        self.assertEqual(result["source_commit"], c293.SOURCE_COMMIT)
        self.assertEqual(len(result["module_sha256"]), 5)
        self.assertEqual(result["dependency_pins"]["mathlib"], c293.MATHLIB_PIN)

    def make_source_fixture(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        src = Path("frontiers/morse_finite_critical_20261018")
        for name in c293.SOURCES:
            p = src / "final-project" / f"{name}.lean"
            (root / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / p, root / p)
        for p in [src / "negative-project/WithoutMorse.lean",
                  Path("formal/lakefile.toml"), Path("formal/lean-toolchain"),
                  Path("formal/lake-manifest.json")]:
            (root / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / p, root / p)
        for p in c293.UPSTREAM.values():
            (root / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / p, root / p)
        return temp, root

    def test_modified_theorem_source_rejected(self):
        temp, root = self.make_source_fixture()
        with temp:
            p = root / "frontiers/morse_finite_critical_20261018/final-project/MorseFiniteCritical.lean"
            p.write_bytes(p.read_bytes() + b"\n-- mutation\n")
            with self.assertRaisesRegex(RuntimeError, "source identity mismatch"):
                c293.verify_sources(root)

    def test_modified_upstream_copy_rejected(self):
        temp, root = self.make_source_fixture()
        with temp:
            p = root / c293.UPSTREAM["TorusTopology"]
            p.write_bytes(p.read_bytes() + b"\n-- changed upstream\n")
            with self.assertRaisesRegex(RuntimeError, "upstream C293 input differs"):
                c293.verify_sources(root)

    def test_missing_premise_control_mutation_rejected(self):
        temp, root = self.make_source_fixture()
        with temp:
            p = root / "frontiers/morse_finite_critical_20261018/negative-project/WithoutMorse.lean"
            p.write_bytes(p.read_bytes() + b"\n-- mutation\n")
            with self.assertRaisesRegex(RuntimeError, "control modified"):
                c293.verify_sources(root)

    def test_changed_dependency_pin_rejected(self):
        temp, root = self.make_source_fixture()
        with temp:
            p = root / "formal/lean-toolchain"
            p.write_text("leanprover/lean4:v4.35.0\n")
            with self.assertRaisesRegex(RuntimeError, "toolchain pin changed"):
                c293.verify_sources(root)

    def test_audit_requires_169_exact_reports(self):
        preamble = "\n".join(
            f"MORSE_AUDIT_MODULE {module} COUNT {count}"
            for module, count in c293.MODULE_COUNTS.items()
        )
        preamble += ("\nMORSE_AUDIT_STANDARD_ONLY_PASS COUNT 169\n"
                     "'TorusMorseFinite.quotientCriticalSet_finite' depends on axioms:"
                     " [propext, Classical.choice, Quot.sound]\n")
        good = preamble + "MORSE_AUDIT_DECL name AXIOMS []\n" * 169
        c293.validate_audit(good)
        with self.assertRaisesRegex(RuntimeError, "169 declaration reports"):
            c293.validate_audit(preamble + "MORSE_AUDIT_DECL name AXIOMS []\n" * 168)
        with self.assertRaisesRegex(RuntimeError, "standard-only"):
            c293.validate_audit(good.replace("MORSE_AUDIT_STANDARD_ONLY_PASS", "INCOMPLETE"))

    def test_negative_requires_intended_failure_not_just_nonzero(self):
        diagnostic = ("file:10:2: error: Type mismatch\n"
                      "quotientCriticalSet_finite d L hL g hs hp\n"
                      "has type IsMorseDistinct d L g → ...\n"
                      "but is expected to have type ...")
        c293.validate_negative(1, diagnostic)
        for code, output in ((0, diagnostic), (2, diagnostic),
                             (1, "error: unknown module MorseFiniteCritical"),
                             (1, diagnostic + "\nerror: unrelated")):
            with self.subTest(code=code, output=output[:30]):
                with self.assertRaises(RuntimeError):
                    c293.validate_negative(code, output)

    def test_symlink_source_rejected(self):
        temp, root = self.make_source_fixture()
        with temp:
            p = root / "frontiers/morse_finite_critical_20261018/final-project/Lifetime.lean"
            elsewhere = root / "lifetime-copy"
            shutil.copyfile(p, elsewhere)
            p.unlink()
            p.symlink_to(elsewhere)
            with self.assertRaisesRegex(RuntimeError, "symlink"):
                c293.verify_sources(root)


if __name__ == "__main__":
    unittest.main()
