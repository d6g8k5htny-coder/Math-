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

    def test_same_size_source_mutation_rejected(self):
        temp, root = self.make_source_fixture()
        with temp:
            p = root / "frontiers/morse_finite_critical_20261018/final-project/MorseFiniteControls.lean"
            data = bytearray(p.read_bytes())
            data[-2] ^= 0x01
            p.write_bytes(bytes(data))
            with self.assertRaisesRegex(RuntimeError, "source identity mismatch"):
                c293.verify_sources(root)

    def test_changed_lakefile_or_lock_pin_rejected(self):
        for rel, old, new, message in (
                ("formal/lakefile.toml", c293.MATHLIB_PIN, "0" * 40, "Lake mathlib pin changed"),
                ("formal/lake-manifest.json", c293.PACKAGE_PINS["batteries"], "0" * 40,
                 "dependency pins differ")):
            temp, root = self.make_source_fixture()
            with temp, self.subTest(path=rel):
                p = root / rel
                self.assertIn(old, p.read_text())
                p.write_text(p.read_text().replace(old, new))
                with self.assertRaisesRegex(RuntimeError, message):
                    c293.verify_sources(root)

    def test_out_of_tree_source_rejected(self):
        temp, root = self.make_source_fixture()
        with temp, tempfile.TemporaryDirectory() as other:
            outside = Path(other) / "Lifetime.lean"
            outside.write_text("-- outside\n")
            with self.assertRaisesRegex(RuntimeError, "outside repository"):
                c293.safe_source(outside, root)

    def audit_text(self, decls=169, counts=None, main=True):
        counts = counts or c293.MODULE_COUNTS
        text = "\n".join(f"MORSE_AUDIT_MODULE {m} COUNT {n}" for m, n in counts.items())
        text += "\nMORSE_AUDIT_STANDARD_ONLY_PASS COUNT 169\n"
        if main:
            text += ("'TorusMorseFinite.quotientCriticalSet_finite' depends on axioms:"
                     " [propext, Classical.choice, Quot.sound]\n")
        return text + "MORSE_AUDIT_DECL name AXIOMS []\n" * decls

    def test_audit_rejects_wrong_census_extra_reports_and_missing_main_report(self):
        c293.validate_audit(self.audit_text())
        wrong = dict(c293.MODULE_COUNTS, Lifetime=102)
        for text, message in ((self.audit_text(counts=wrong), "audit missing Lifetime census"),
                              (self.audit_text(decls=170), "169 declaration reports"),
                              (self.audit_text(main=False), "main theorem axiom report absent")):
            with self.subTest(message=message):
                with self.assertRaisesRegex(RuntimeError, message):
                    c293.validate_audit(text)

    def test_negative_rejects_wrong_mismatch_and_unrelated_failure(self):
        diagnostic = ("file:10:2: error: Type mismatch\n"
                      "quotientCriticalSet_finite d L hL g hs hp\n"
                      "has type IsMorseDistinct d L g → ...\n"
                      "but is expected to have type ...")
        for output in ("file:10:2: error: Type mismatch\nsomething else entirely\n",
                       diagnostic + "\nINTERNAL PANIC: lean::memory_exception"):
            with self.subTest(output=output[-40:]):
                with self.assertRaisesRegex(RuntimeError, "negative control"):
                    c293.validate_negative(1, output)

    def test_hosted_context_requires_actual_run_identity(self):
        names = ("GITHUB_SHA", "GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_REPOSITORY")
        saved = {k: c293.os.environ.get(k) for k in names}
        try:
            try:
                head = c293.git("rev-parse", "HEAD")
            except (OSError, c293.subprocess.CalledProcessError):
                self.skipTest("not a git checkout")
            good = {"GITHUB_SHA": head, "GITHUB_RUN_ID": "1", "GITHUB_RUN_ATTEMPT": "1",
                    "GITHUB_REPOSITORY": "d6g8k5htny-coder/Math-"}
            c293.os.environ.update(good)
            self.assertEqual(c293.verify_context()["github_sha"], head)
            for key, value, message in (("GITHUB_REPOSITORY", "someone/Math-", "wrong execution repository"),
                                        ("GITHUB_SHA", "0" * 40, "tested checkout mismatch"),
                                        ("GITHUB_RUN_ID", "", "actual GitHub run identity")):
                with self.subTest(key=key):
                    c293.os.environ.update(good)
                    c293.os.environ[key] = value
                    with self.assertRaisesRegex(RuntimeError, message):
                        c293.verify_context()
        finally:
            for k, v in saved.items():
                if v is None:
                    c293.os.environ.pop(k, None)
                else:
                    c293.os.environ[k] = v

    def test_unexpected_success_of_negative_phase_rejected(self):
        saved = c293.EVIDENCE
        with tempfile.TemporaryDirectory() as t:
            c293.EVIDENCE = Path(t)
            try:
                with self.assertRaisesRegex(RuntimeError, "unexpected exit: 0"):
                    c293.run_phase("negative-probe", [c293.sys.executable, "-c", "pass"], t,
                                   dict(c293.os.environ), expected_success=False)
            finally:
                c293.EVIDENCE = saved

    def test_installed_dependency_commit_and_cleanliness_checked(self):
        saved = (c293.FORMAL, c293.PACKAGE_PINS)
        with tempfile.TemporaryDirectory() as t:
            pkg = Path(t) / ".lake/packages/demo"
            pkg.mkdir(parents=True)
            run = lambda *a: c293.subprocess.run(["git", "-C", str(pkg), *a], check=True,
                                                 capture_output=True, text=True)
            run("init", "-q")
            (pkg / "f.txt").write_text("1\n")
            run("add", "f.txt")
            run("-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false",
                "commit", "-q", "-m", "x")
            head = c293.git("-C", str(pkg), "rev-parse", "HEAD")
            c293.FORMAL = Path(t)
            try:
                c293.PACKAGE_PINS = {"demo": head}
                self.assertEqual(c293.verify_packages(), {"demo": head})
                c293.PACKAGE_PINS = {"demo": "0" * 40}
                with self.assertRaisesRegex(RuntimeError, "wrong installed dependency commit"):
                    c293.verify_packages()
                c293.PACKAGE_PINS = {"demo": head}
                (pkg / "f.txt").write_text("2\n")
                with self.assertRaisesRegex(RuntimeError, "dirty installed dependency checkout"):
                    c293.verify_packages()
            finally:
                c293.FORMAL, c293.PACKAGE_PINS = saved


if __name__ == "__main__":
    unittest.main()
