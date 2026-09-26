#!/usr/bin/env python3
import importlib.util
from decimal import Decimal
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / 'rim_contract.py'
LEDGER = (HERE.parents[1] / 'imports/upper2d_h5_ledgers_20260926/raw/H5_closure'
          / 'h5_results_r0.05_s0p1_rimprobes.jsonl')
HISTORICAL_HUNT = (HERE.parents[1] / 'imports/upper2d_stage_e_20260926/raw/STAGE_E'
                   / 'hunt_rim.py')
VERIFY_PATH = HERE / 'verify.py'


class RimContractTests(unittest.TestCase):
    def load_module(self):
        self.assertTrue(MODULE_PATH.is_file(), 'rim_contract.py successor is missing')
        spec = importlib.util.spec_from_file_location('rim_contract', MODULE_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def mutated_ledger(self, extra_row):
        lines = LEDGER.read_text().splitlines()
        last_marker = max(i for i, line in enumerate(lines)
                          if json.loads(line).get('part') == 'rimprobes_done')
        lines.insert(last_marker, extra_row)
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / LEDGER.name
        path.write_text('\n'.join(lines) + '\n')
        return directory, path

    def copied_ledger(self, lines, name=None):
        directory = tempfile.TemporaryDirectory()
        path = Path(directory.name) / (name or LEDGER.name)
        path.write_text('\n'.join(lines) + '\n')
        return directory, path

    def test_loads_exact_final_completed_radius_005_constants(self):
        module = self.load_module()

        values = module.load_rim_constants(LEDGER, expected_radius=Decimal('0.05'))

        self.assertEqual(tuple(values), (15, 45, 75, 105, 135, 150, 160, 165, 170, 175))
        self.assertEqual(
            values[175],
            Decimal('1.728655925369777239812566677032221782361e-35'),
        )
        self.assertEqual(
            module.flat_envelope(values)[175],
            Decimal('3.457311850739554479625133354064443564722e-35'),
        )

    def test_rejects_duplicate_angle_in_completed_block(self):
        module = self.load_module()
        directory, path = self.mutated_ledger(
            '{"part":"rimprobe","th":175,"rho_hi":"1e-35"}'
        )
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'duplicate rim angle'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_duplicate_json_object_name(self):
        module = self.load_module()
        directory, path = self.mutated_ledger('{"part":"note","part":"other"}')
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'duplicate JSON object name'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_explicit_rimprobe_failure_in_completed_block(self):
        module = self.load_module()
        directory, path = self.mutated_ledger('{"part":"rimprobe_fail","th":175}')
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'rimprobe failure row'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_trailing_rimprobe_failure_after_last_marker(self):
        module = self.load_module()
        lines = LEDGER.read_text().splitlines()
        lines.append('{"part":"rimprobe_fail","th":175}')
        directory, path = self.copied_ledger(lines)
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'unterminated failed rimprobe block'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_numeric_rho_hi_instead_of_decimal_string(self):
        module = self.load_module()
        lines = LEDGER.read_text().splitlines()
        last_marker = max(i for i, line in enumerate(lines)
                          if json.loads(line).get('part') == 'rimprobes_done')
        selected_175 = max(i for i in range(last_marker)
                           if json.loads(lines[i]).get('part') == 'rimprobe'
                           and json.loads(lines[i])['th'] == 175)
        lines[selected_175] = '{"part":"rimprobe","th":175,"rho_hi":1e-35}'
        directory, path = self.copied_ledger(lines)
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'rho_hi must be a decimal string'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_noninteger_angle_encoding(self):
        module = self.load_module()
        lines = LEDGER.read_text().splitlines()
        last_marker = max(i for i, line in enumerate(lines)
                          if json.loads(line).get('part') == 'rimprobes_done')
        selected_175 = max(i for i in range(last_marker)
                           if json.loads(lines[i]).get('part') == 'rimprobe'
                           and json.loads(lines[i])['th'] == 175)
        row = json.loads(lines[selected_175])
        row['th'] = 175.0
        lines[selected_175] = json.dumps(row, separators=(',', ':'))
        directory, path = self.copied_ledger(lines)
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'rim angle must be an integer'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_angle_order_does_not_change_the_completed_block(self):
        module = self.load_module()
        lines = LEDGER.read_text().splitlines()
        last_marker = max(i for i, line in enumerate(lines)
                          if json.loads(line).get('part') == 'rimprobes_done')
        selected = [i for i in range(last_marker)
                    if json.loads(lines[i]).get('part') == 'rimprobe'][-10:]
        lines[selected[-2]], lines[selected[-1]] = lines[selected[-1]], lines[selected[-2]]
        directory, path = self.copied_ledger(lines)
        self.addCleanup(directory.cleanup)

        values = module.load_rim_constants(path, expected_radius=Decimal('0.05'))

        self.assertEqual(tuple(values), module.ANGLES)

    def test_rejects_wrong_filename_radius(self):
        module = self.load_module()
        directory, path = self.copied_ledger(
            LEDGER.read_text().splitlines(),
            name='h5_results_r0.025_s0p1_rimprobes.jsonl',
        )
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'filename radius'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_missing_angle_in_selected_block(self):
        module = self.load_module()
        lines = LEDGER.read_text().splitlines()
        last_marker = max(i for i, line in enumerate(lines)
                          if json.loads(line).get('part') == 'rimprobes_done')
        selected_175 = max(i for i in range(last_marker)
                           if json.loads(lines[i]).get('part') == 'rimprobe'
                           and json.loads(lines[i])['th'] == 175)
        del lines[selected_175]
        directory, path = self.copied_ledger(lines)
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'coverage'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_rejects_unterminated_final_block(self):
        module = self.load_module()
        lines = LEDGER.read_text().splitlines()
        last_marker = max(i for i, line in enumerate(lines)
                          if json.loads(line).get('part') == 'rimprobes_done')
        del lines[last_marker]
        directory, path = self.copied_ledger(lines)
        self.addCleanup(directory.cleanup)
        with self.assertRaisesRegex(ValueError, 'unterminated'):
            module.load_rim_constants(path, expected_radius=Decimal('0.05'))

    def test_reproduces_only_the_angle_175_historical_transcription_defect(self):
        module = self.load_module()
        values = module.load_rim_constants(LEDGER, expected_radius=Decimal('0.05'))

        comparison = module.compare_historical_literal(HISTORICAL_HUNT, values)

        self.assertEqual(comparison['matching_truncated_angles'], list(module.ANGLES[:-1]))
        self.assertEqual(comparison['mismatching_angles'], [175])
        self.assertGreater(comparison['angle_175_inflation_factor'], Decimal('1e34'))
        self.assertLess(comparison['angle_175_inflation_factor'], Decimal('1e35'))

    def test_report_binds_sources_and_keeps_scientific_effect_none(self):
        module = self.load_module()

        report = module.reproduction_report(HISTORICAL_HUNT, LEDGER)

        self.assertEqual(report['scientific_effect'], 'NONE')
        self.assertEqual(
            report['historical_hunt_sha256'],
            'de73e5fed00782c3709d2f9a8b1cddca23926606a8ef5ffc4cf0de8aefb66f90',
        )
        self.assertEqual(
            report['ledger_sha256'],
            '22c7107e93ba9c02bea1f6f34085044ab535f29c067ce79c0cd7d8b1911ecc63',
        )
        self.assertEqual(report['mismatching_angles'], [175])
        self.assertEqual(
            report['corrected_cflat_175'],
            '3.457311850739554479625133354064443564722E-35',
        )
        self.assertFalse(report['numerical_hunt_replayed'])
        self.assertFalse(report['bound_certified'])

    def test_verify_cli_emits_the_bound_report(self):
        self.assertTrue(VERIFY_PATH.is_file(), 'verify.py reproduction entry point is missing')
        run = subprocess.run(
            [sys.executable, '-B', '-S', str(VERIFY_PATH), '--emit'],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(run.returncode, 0, run.stderr)
        report = json.loads(run.stdout)
        self.assertEqual(report['mismatching_angles'], [175])
        self.assertEqual(report['scientific_effect'], 'NONE')


if __name__ == '__main__':
    unittest.main()
