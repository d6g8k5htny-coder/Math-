"""C8 workflow wiring and custody of the two original diagnostic run blocks."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowControls(unittest.TestCase):
    def test_all_registered_quarantine_commands_run_before_legacy_replay(self):
        text = (ROOT / ".github/workflows/c8-elder-failure-coefficient.yml").read_text()
        self.assertIn("A3 quarantine", text)
        for command in ("python -B -S -m unittest discover -s tests -p test_c8_quarantine_mutations.py -v",
                        "python -B -O -S -m unittest discover -s tests -p test_c8_quarantine_mutations.py -v",
                        "python -B -S tools/c8_quarantine_mutations.py",
                        "python -B -S tools/check_c8_quarantine.py",
                        "--consume-output /results/k=1/J_fail"):
            self.assertIn(command, text)
            self.assertLess(text.index(command), text.index("Self-test, full replay against RESULTS.json, mutants"))
        self.assertIn("needs: quarantine-boundary", text)
        self.assertIn("if: always()", text)
        self.assertIn("include-hidden-files: true", text)

    def test_both_original_replay_blocks_are_byte_preserved(self):
        expected = set(json.loads((ROOT / "tools/c8_quarantine_registry.json").read_text())["legacy_run_block_sha256"])
        self.assertEqual(len(expected), 2)
        lines = (ROOT / ".github/workflows/c8-elder-failure-coefficient.yml").read_text().splitlines(keepends=True)
        actual = set()
        for i, line in enumerate(lines):
            if line.strip() != "run: |":continue
            indent = len(line) - len(line.lstrip());j = i + 1
            while j < len(lines) and (not lines[j].strip() or len(lines[j]) - len(lines[j].lstrip()) > indent):j += 1
            actual.add(hashlib.sha256("".join(lines[i + 1:j]).encode()).hexdigest())
        self.assertLessEqual(expected, actual)

    def test_registry_declares_nonadmission_and_bounded_source_controls(self):
        r = json.loads((ROOT / "tools/c8_quarantine_registry.json").read_text())
        self.assertEqual(r["scientific_effect"], "NONE")
        self.assertIs(r["global_isolation_established"], False)
        self.assertIs(r["cbz_certificate_admitted"], False)
        self.assertEqual((r["denied_outputs"], r["exact_rational_witnesses"]), (106, 3))
        self.assertEqual((r["core_methods_per_mode"], r["harness_methods_per_mode"], r["declared_mutants"]), (41, 22, 13))
        self.assertIn("every CLI", r["mutation_threshold"])


if __name__ == "__main__":
    unittest.main()
