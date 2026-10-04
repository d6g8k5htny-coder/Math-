"""Output-maintenance regressions: real files and bounded checker subprocesses."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("dryrun", Path(__file__).with_name("execution_dryrun.py"))
dryrun = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dryrun)


class OutputMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve() / "repo"
        self.out = Path(self.tmp.name).resolve() / "executed"
        self.pins = []
        self.old = []
        self.payload = b'{"passed": true, "register_state": "installed"}\n'
        for i, (folder, script) in enumerate(dryrun.PACKETS.values()):
            pin = self.root / folder / "RESULTS_INSTALLED.json"
            pin.parent.mkdir(parents=True)
            data = ("old pin %d\n" % i).encode()
            pin.write_bytes(data)
            self.pins.append(pin)
            self.old.append(data)
            entry = self.out / folder / script
            entry.parent.mkdir(parents=True)
            entry.write_text('import sys\nMUTANTS = ("reject",)\n'
                             'if "--mutant" in sys.argv: sys.exit(1)\n'
                             'print(\'{"passed": true, "register_state": "installed"}\')\n')

    def run_write(self):
        return dryrun.run_checkers(self.root, self.out, True, True)

    def assert_old(self):
        self.assertEqual([p.read_bytes() for p in self.pins], self.old)

    def test_success_updates_all_outputs(self):
        ok, report = self.run_write()
        self.assertTrue(ok)
        self.assertEqual([p.read_bytes() for p in self.pins], [self.payload] * 3)
        self.assertTrue(all(v["written"] for v in report.values()))

    def test_late_checker_failure_preserves_every_pin(self):
        folder, script = list(dryrun.PACKETS.values())[-1]
        (self.out / folder / script).write_text('import sys\nMUTANTS = ("reject",)\nsys.exit(1)\n')
        ok, report = self.run_write()
        self.assertFalse(ok)
        self.assert_old()
        self.assertTrue(all(v["written"] is None for v in report.values()))

    def test_invalid_second_destination_does_not_write_first(self):
        self.pins[1].unlink()
        self.pins[1].mkdir()
        try:
            ok, _ = self.run_write()
        except OSError:
            ok = False
        self.assertFalse(ok)
        self.assertEqual(self.pins[0].read_bytes(), self.old[0])
        self.assertEqual(self.pins[2].read_bytes(), self.old[2])
        self.assertTrue(self.pins[1].is_dir())

    def test_leaf_symlink_never_overwrites_external_target(self):
        outside = Path(self.tmp.name) / "outside"
        outside.write_bytes(b"outside sentinel\n")
        self.pins[0].unlink()
        self.pins[0].symlink_to(outside)
        ok, _ = self.run_write()
        self.assertFalse(ok)
        self.assertEqual(outside.read_bytes(), b"outside sentinel\n")
        self.assertEqual(self.pins[1].read_bytes(), self.old[1])
        self.assertTrue(self.pins[0].is_symlink())

    def test_parent_symlink_never_overwrites_external_target(self):
        parent = self.pins[0].parent
        outside = Path(self.tmp.name) / "outside-directory"
        parent.rename(outside)
        parent.symlink_to(outside, target_is_directory=True)
        ok, _ = self.run_write()
        self.assertFalse(ok)
        self.assertEqual((outside / self.pins[0].name).read_bytes(), self.old[0])
        self.assertEqual(self.pins[1].read_bytes(), self.old[1])

    def test_hardlinked_old_pin_does_not_modify_other_name(self):
        outside = Path(self.tmp.name) / "hardlinked-old-pin"
        os.link(self.pins[0], outside)
        ok, _ = self.run_write()
        self.assertTrue(ok)
        self.assertEqual(outside.read_bytes(), self.old[0])
        self.assertEqual(self.pins[0].read_bytes(), self.payload)

    def test_second_replacement_failure_restores_all_old_outputs(self):
        real_replace = os.replace
        failed = False

        def fail_once(source, destination, *args, **kwargs):
            nonlocal failed
            if Path(destination) == self.pins[1] and not failed:
                failed = True
                raise OSError("injected second-destination failure")
            return real_replace(source, destination, *args, **kwargs)

        with patch.object(os, "replace", side_effect=fail_once):
            ok, _ = self.run_write()
        self.assertFalse(ok)
        self.assert_old()

    def test_missing_pins_can_be_created_after_validation(self):
        for pin in self.pins:
            pin.unlink()
        ok, _ = self.run_write()
        self.assertTrue(ok)
        self.assertEqual([p.read_bytes() for p in self.pins], [self.payload] * 3)

    def test_staging_failure_preserves_all_outputs(self):
        real_mkstemp = tempfile.mkstemp
        calls = 0

        def fail_third(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError("injected staging failure")
            return real_mkstemp(*args, **kwargs)

        with patch.object(tempfile, "mkstemp", side_effect=fail_third):
            ok, _ = self.run_write()
        self.assertFalse(ok)
        self.assert_old()
        self.assertEqual(list(self.root.rglob(".installed-result-*")), [])

    def test_rollback_failure_is_explicit_and_retains_recovery_bytes(self):
        real_replace = os.replace
        calls = 0

        def fail_install_and_rollback(source, destination):
            nonlocal calls
            calls += 1
            if calls in (2, 3):
                raise OSError("injected install/rollback failure")
            return real_replace(source, destination)

        with patch.object(os, "replace", side_effect=fail_install_and_rollback):
            ok, report = self.run_write()
        self.assertFalse(ok)
        self.assertTrue(all("rollback incomplete" in v["write_error"] for v in report.values()))
        backups = list(self.root.rglob(".installed-result-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), self.old[0])
        self.assertEqual(self.pins[0].read_bytes(), self.payload)
        self.assertEqual(self.pins[1].read_bytes(), self.old[1])

    def test_failure_removes_new_pin_when_original_was_absent(self):
        for pin in self.pins:
            pin.unlink()
        real_replace = os.replace

        def fail_second(source, destination):
            if Path(destination) == self.pins[1]:
                raise OSError("injected second install failure")
            return real_replace(source, destination)

        with patch.object(os, "replace", side_effect=fail_second):
            ok, _ = self.run_write()
        self.assertFalse(ok)
        self.assertTrue(all(not pin.exists() for pin in self.pins))

    def test_existing_file_permissions_are_preserved(self):
        self.pins[0].chmod(0o640)
        ok, _ = self.run_write()
        self.assertTrue(ok)
        self.assertEqual(self.pins[0].stat().st_mode & 0o777, 0o640)

    def test_cleanup_failure_keeps_rollback_recovery_path_in_report(self):
        real_replace, real_unlink = os.replace, Path.unlink
        calls = 0

        def fail_install_and_rollback(source, destination):
            nonlocal calls
            calls += 1
            if calls in (2, 3):
                raise OSError("injected install/rollback failure")
            return real_replace(source, destination)

        def fail_cleanup(path, *args, **kwargs):
            if path.name.startswith(".installed-result-"):
                raise OSError("injected cleanup failure")
            return real_unlink(path, *args, **kwargs)

        with patch.object(os, "replace", side_effect=fail_install_and_rollback), \
                patch.object(Path, "unlink", fail_cleanup):
            ok, report = self.run_write()
        self.assertFalse(ok)
        error = next(iter(report.values()))["write_error"]
        self.assertIn("rollback incomplete", error)
        backups = [p for p in self.root.rglob(".installed-result-*") if p.read_bytes() == self.old[0]]
        self.assertEqual(len(backups), 1)
        self.assertIn(str(backups[0]), error)

    def test_cleanup_stat_failure_cannot_hide_recovery_location(self):
        real_replace, real_exists = os.replace, Path.exists
        calls = 0

        def fail_install_and_rollback(source, destination):
            nonlocal calls
            calls += 1
            if calls in (2, 3):
                raise OSError("injected install/rollback failure")
            return real_replace(source, destination)

        def fail_cleanup_stat(path):
            if calls >= 3 and path.name.startswith(".installed-result-"):
                raise PermissionError("injected cleanup stat failure")
            return real_exists(path)

        with patch.object(os, "replace", side_effect=fail_install_and_rollback), \
                patch.object(Path, "exists", fail_cleanup_stat):
            ok, report = self.run_write()
        self.assertFalse(ok)
        error = next(iter(report.values()))["write_error"]
        self.assertIn("rollback incomplete", error)
        backups = [p for p in self.root.rglob(".installed-result-*") if p.read_bytes() == self.old[0]]
        self.assertEqual(len(backups), 1)
        self.assertIn(str(backups[0]), error)


if __name__ == "__main__":
    unittest.main()
