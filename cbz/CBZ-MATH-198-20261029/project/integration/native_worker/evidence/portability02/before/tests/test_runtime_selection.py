"""Runtime relocation and historical source boundaries; never launch Lean."""
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

import native
import runtime_support as runtime
import verify_native_saved as verifier


class RuntimeSelectionTests(unittest.TestCase):
    def environment(self, **values):
        base = {k: v for k, v in os.environ.items()
                if k not in {'UL_LEAN', 'UL_MATHLIB_ROOT'}}
        base.update(values)
        return mock.patch.dict(os.environ, base, clear=True)

    def test_defaults_remain_the_documented_pinned_installations(self):
        with self.environment():
            cfg = runtime.config('/unused/build')
        self.assertEqual(cfg.lean, runtime.LEAN)
        self.assertEqual(cfg.mathlib_root, runtime.MATHLIB)

    def test_lean_override_is_selected_without_overriding_mathlib(self):
        with self.environment(UL_LEAN='/relocated path/lean'):
            cfg = runtime.config('/unused/build')
        self.assertEqual(cfg.lean, Path('/relocated path/lean'))
        self.assertEqual(cfg.mathlib_root, runtime.MATHLIB)

    def test_mathlib_override_is_selected_without_overriding_lean(self):
        with self.environment(UL_MATHLIB_ROOT='/relocated path/mathlib'):
            cfg = runtime.config('/unused/build')
        self.assertEqual(cfg.lean, runtime.LEAN)
        self.assertEqual(cfg.mathlib_root, Path('/relocated path/mathlib'))

    def test_selection_is_per_call_and_does_not_start_a_process(self):
        with mock.patch.object(runtime.rt.subprocess, 'run') as process:
            with self.environment(UL_LEAN='/first/lean', UL_MATHLIB_ROOT='/first/mathlib'):
                first = runtime.config('/unused/first')
            with self.environment(UL_LEAN='/second/lean', UL_MATHLIB_ROOT='/second/mathlib'):
                second = runtime.config('/unused/second')
        process.assert_not_called()
        self.assertEqual((first.lean, first.mathlib_root),
                         (Path('/first/lean'), Path('/first/mathlib')))
        self.assertEqual((second.lean, second.mathlib_root),
                         (Path('/second/lean'), Path('/second/mathlib')))

    def test_relocated_invalid_binary_is_refused_before_any_compile(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lean = root / 'relocated lean'
            lean.write_bytes(b'not the pinned Lean executable')
            evidence = root / 'formal.json'
            evidence.write_text('{}')
            with self.environment(UL_LEAN=str(lean), UL_MATHLIB_ROOT=str(root / 'mathlib')):
                with mock.patch.object(native, 'dependency_bindings', return_value={}):
                    with mock.patch.object(native, 'run_recorded', return_value={'succeeded': False}) as compile_:
                        with self.assertRaisesRegex(ValueError, 'pinned Lean mismatch'):
                            native.build(root / 'build', root / 'output', root / 'cache', evidence)
            compile_.assert_not_called()

    def test_worker_command_still_requires_runtime_identity_validation(self):
        with self.environment(UL_LEAN='/relocated/lean', UL_MATHLIB_ROOT='/relocated/mathlib'):
            cfg = runtime.config('/unused/build')
        with mock.patch.object(runtime.rt.RuntimeConfig, 'identities',
                               side_effect=ValueError('identity validation required')) as identities:
            with self.assertRaisesRegex(ValueError, 'identity validation required'):
                cfg.command()
        identities.assert_called_once_with()


class HistoricalControllerBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.source = runtime.HERE / 'sources/session04_controller'
        self.campaign = runtime.HERE / 'evidence/session04'

    def test_explicit_frozen_controller_root_replays_historical_campaign(self):
        value = verifier.check(self.campaign, controller_source_root=self.source)
        self.assertEqual(value['native_endpoint_certificates'], 49)
        self.assertEqual(value['controller_source_root'], str(self.source.resolve()))
        self.assertFalse(value['kernel_executed_by_this_verifier'])

    def test_historical_campaign_does_not_silently_bind_changed_current_code(self):
        with self.assertRaisesRegex(ValueError, 'controller/transport source drift'):
            verifier.check(self.campaign)

    def test_explicit_source_boundary_still_rejects_source_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'controller'
            shutil.copytree(self.source, source)
            path = source / 'integration/native_worker/runtime_support.py'
            path.write_bytes(path.read_bytes() + b'\n# tampered historical controller\n')
            with self.assertRaisesRegex(ValueError, 'controller/transport source drift'):
                verifier.check(self.campaign, controller_source_root=source)


if __name__ == '__main__':
    unittest.main()
