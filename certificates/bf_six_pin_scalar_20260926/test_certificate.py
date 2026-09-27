"""Arithmetic and refusal controls; these do not kernel-check PROOF.md."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "certificate.py"

class ScalarCertificateTests(unittest.TestCase):
    def load(self):
        self.assertTrue(SCRIPT.is_file(), "certificate implementation is absent")
        spec = importlib.util.spec_from_file_location("scalar_certificate", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_cli_emits_expected_uniform_interval(self):
        p = subprocess.run([sys.executable, "-B", "-S", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        data = json.loads(p.stdout)
        self.assertEqual(data["normalized_variance"], {"lower": "1599/3200", "upper": "1/2"})
        self.assertEqual(data["radius"], {"lower": "0", "lower_open": True, "upper": "1/40"})
        self.assertEqual(data["scientific_effect"], "NONE")
        self.assertFalse(data["formal_kernel_checked"])

    def test_exact_generation_and_validation(self):
        m = self.load()
        self.assertEqual(m.validate(m.certificate()), m.certificate())

    def test_true_but_looser_enclosure_is_allowed(self):
        m = self.load(); c = m.certificate()
        c["normalized_variance"] = {"lower": "49/100", "upper": "51/100"}
        self.assertEqual(m.validate(c), c)

    def test_false_lower_half_is_refused(self):
        m = self.load(); c = m.certificate()
        c["normalized_variance"]["lower"] = "1/2"
        with self.assertRaisesRegex(ValueError, "lower"): m.validate(c)

    def test_false_upper_is_refused(self):
        m = self.load(); c = m.certificate()
        c["normalized_variance"]["upper"] = "499/1000"
        with self.assertRaisesRegex(ValueError, "upper"): m.validate(c)

    def test_radius_widening_without_lower_update_is_refused(self):
        m = self.load(); c = m.certificate(); c["radius"]["upper"] = "1/20"
        with self.assertRaisesRegex(ValueError, "lower"): m.validate(c)

    def test_bad_radius_domains_are_refused(self):
        m = self.load()
        for value in ("0", "-1/40", "1", "2"):
            with self.subTest(value=value), self.assertRaises(ValueError): m.certificate(value)

    def test_float_boolean_and_decimal_inputs_are_refused(self):
        m = self.load()
        for value in (0.025, True, 1, "0.025", " 1/40", "2/80", "1/0"):
            with self.subTest(value=value), self.assertRaises((ValueError, TypeError)): m.certificate(value)

    def test_zero_radius_cannot_be_closed(self):
        m = self.load(); c = m.certificate(); c["radius"]["lower_open"] = False
        with self.assertRaises(ValueError): m.validate(c)

    def test_changed_field_or_law_is_refused(self):
        m = self.load()
        for key,value in (("model", "periodized SIDE24"), ("conditioning", "determinant-weighted Palm"), ("dimension", 3)):
            c = m.certificate(); c[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): m.validate(c)

    def test_status_and_formalization_claims_are_refused(self):
        m = self.load()
        for key,value in (("scientific_effect", "CLOSE_D5"), ("formal_kernel_checked", True), ("review", "ACCEPT")):
            c = m.certificate(); c[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): m.validate(c)
        c = m.certificate(); c["lemma_closed"] = True
        with self.assertRaises(ValueError): m.validate(c)

    def test_missing_and_unknown_fields_are_refused(self):
        m = self.load(); c = m.certificate(); del c["analytic_dependency"]
        with self.assertRaises(ValueError): m.validate(c)
        c = m.certificate(); c["radius"]["grid_points"] = 40
        with self.assertRaises(ValueError): m.validate(c)

    def test_cli_rejects_bad_certificate_and_duplicate_keys(self):
        m = self.load()
        with tempfile.TemporaryDirectory() as t:
            path = Path(t)/"input.json"; c = m.certificate(); c["normalized_variance"]["lower"] = "1/2"
            for text in (json.dumps(c), '{"schema":1,"schema":2}', '{"schema": NaN}'):
                path.write_text(text)
                p = subprocess.run([sys.executable,"-B","-S",str(SCRIPT),"--check",str(path)],capture_output=True,text=True)
                self.assertNotEqual(p.returncode,0)
                self.assertIn("REFUSED",p.stderr)

    def test_all_order_coefficient_identity_finite_checks(self):
        m = self.load()
        from fractions import Fraction as F
        from math import factorial
        for n in range(3,65):
            actual = F(1,2*factorial(n-1))-F(1,factorial(n))
            self.assertEqual(actual,m.upper_slack_coefficient(n))
            self.assertGreater(actual,0)

    def test_schur_polynomial_identity(self):
        m = self.load()
        self.assertTrue(m.schur_identity())

    def test_normal_and_optimized_outputs_match(self):
        self.load()
        cmds = [[sys.executable,"-B","-S",str(SCRIPT)], [sys.executable,"-O","-B","-S",str(SCRIPT)]]
        outputs = [subprocess.run(c,capture_output=True,check=True).stdout for c in cmds]
        self.assertEqual(*outputs)

if __name__ == "__main__": unittest.main()
