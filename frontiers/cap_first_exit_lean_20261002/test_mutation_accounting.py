"""The kill classifier must distinguish intended assertions from failed execution."""
import pathlib
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
import run_cbz_mutations as runner


def result(method='expected', count='1 test', status=1, extra=''):
    text=('FAIL: '+method+' (controls.Case)\nAssertionError: ValueError not raised\n'+extra
          +'Ran '+count+' in 0.001s\nFAILED (failures=1)\n')
    return types.SimpleNamespace(returncode=status,stderr=text.encode())


class MutationAccounting(unittest.TestCase):
    def test_intended_assertion_is_counted(self):
        self.assertTrue(runner.intended_failure(result(),'expected'))

    def test_foreign_assertion_is_not_a_kill(self):
        self.assertFalse(runner.intended_failure(result(method='unrelated'),'expected'))

    def test_zero_and_multiple_collections_are_not_single_control_kills(self):
        for count in ('0 tests','10 tests','11 tests'):
            with self.subTest(count=count):
                self.assertFalse(runner.intended_failure(result(count=count),'expected'))

    def test_process_error_or_success_is_not_a_kill(self):
        for status in (0,2,-9):
            self.assertFalse(runner.intended_failure(result(status=status),'expected'))

    def test_import_or_test_error_is_not_a_kill(self):
        self.assertFalse(runner.intended_failure(result(extra='ERROR: unrelated import failure\n'),'expected'))

    def test_actual_exporter_kill_requires_its_safety_assertion_marker(self):
        self.assertFalse(runner.intended_failure(result(),'expected',b'ACTUAL_UNSAFE_OPAQUE_EXPORT_MISMATCH'))

    def test_same_method_wrong_cause_is_not_a_kill(self):
        here = pathlib.Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as temporary:
            copied = pathlib.Path(temporary)
            for name in ('compiled_inventory.py', 'test_compiled_inventory.py', 'gate.py'):
                shutil.copy2(here / name, copied / name)
            path = copied / 'compiled_inventory.py'
            original = path.read_text()
            anchor = "        if kind == 'axiom':\n            flag('package_axiom', name)"
            self.assertEqual(original.count(anchor), 1)
            path.write_text(original.replace(anchor,
                "        if kind == 'axiom':\n            raise ValueError('FOREIGN_PROTOCOL_FAILURE_BEFORE_EXPECTED_REJECTION')", 1))
            method = 'test_owned_axiom_is_forbidden_even_if_approved_name_and_bound'
            process = subprocess.run([sys.executable, '-B', '-S', '-m', 'unittest', '-v',
                'test_compiled_inventory.CompiledInventory.' + method], cwd=copied,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            self.assertEqual(process.returncode, 1)
            self.assertIn(b"'package_axiom' not found in 'FOREIGN_PROTOCOL_FAILURE", process.stderr)
            self.assertFalse(runner.intended_failure(process, method),
                             'wrong-cause rejection was counted as a guard-bypass kill')

    def test_same_method_foreign_assertion_without_guard_bypass_is_not_a_kill(self):
        process = result()
        process.stderr = process.stderr.replace(b'ValueError not raised', b'foreign assertion')
        self.assertFalse(runner.intended_failure(process, 'expected'))


if __name__=='__main__':unittest.main()
