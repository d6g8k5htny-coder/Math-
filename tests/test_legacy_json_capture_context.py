"""In-memory reference-context controls; no checker, PTY, spawn or replay."""
import argparse
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'legacy_capture_context_subject', ROOT / 'tools/legacy_json_replay.py')
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class SyntheticParentTTY(io.StringIO):
    def isatty(self):
        return True


def captured_standard_diagnostic(width):
    """Independent stdlib parser in the actual captured-stream context."""
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        parser = argparse.ArgumentParser(
            prog='reference-child.py',
            formatter_class=lambda prog: argparse.HelpFormatter(prog, width=width))
        parser.add_argument('--mutant', choices=HELPER.C6_CHOICES)
        try:
            parser.parse_args(['--mutant', 'unknown'])
        except SystemExit as error:
            if error.code != 2:
                raise
        else:
            raise AssertionError('standard grammar did not reject')
    if stdout.getvalue():
        raise AssertionError('standard invalid argument emitted stdout')
    return stderr.getvalue().encode('utf-8')


class LegacyCaptureContextTests(unittest.TestCase):
    def test_constructor_parse_and_real_formatter_observe_captured_stdout(self):
        seen = {'constructor': [], 'parse': [], 'formatter': []}
        real_init = argparse.ArgumentParser.__init__
        real_parse = argparse.ArgumentParser.parse_args
        real_formatter_init = argparse.HelpFormatter.__init__

        def formatter_init(actual, *args, **kwargs):
            seen['formatter'].append(sys.stdout.isatty())
            return real_formatter_init(actual, *args, **kwargs)

        def parser_init(actual, *args, **kwargs):
            seen['constructor'].append(sys.stdout.isatty())
            return real_init(actual, *args, **kwargs)

        def parse(actual, *args, **kwargs):
            seen['parse'].append(sys.stdout.isatty())
            return real_parse(actual, *args, **kwargs)

        parent_out, parent_err = SyntheticParentTTY(), io.StringIO()
        with contextlib.redirect_stdout(parent_out), contextlib.redirect_stderr(parent_err):
            with mock.patch.object(argparse.ArgumentParser, '__init__', parser_init), \
                    mock.patch.object(argparse.ArgumentParser, 'parse_args', parse), \
                    mock.patch.object(argparse.HelpFormatter, '__init__', formatter_init):
                result = HELPER._unknown_stderr('c6-cluster', 'reference-child.py')
            self.assertIs(sys.stdout, parent_out)
            self.assertIs(sys.stderr, parent_err)
        self.assertTrue(result)
        self.assertEqual(parent_out.getvalue(), '')
        self.assertEqual(parent_err.getvalue(), '')
        for phase, observations in seen.items():
            with self.subTest(phase=phase):
                self.assertTrue(observations, 'real stdlib boundary was not observed')
                self.assertEqual(observations, [False] * len(observations),
                                 'reference inherited the parent TTY instead of child capture')

    def test_exact_bytes_match_captured_standard_parser_for_width_inputs(self):
        for columns, width in ((None, 78), ('35', 33), ('80', 78), ('220', 218),
                               (' 110 ', 108), ('', 78), ('0', 78),
                               ('-3', 78), ('not-a-number', 78)):
            with self.subTest(columns=columns), mock.patch.dict(os.environ):
                os.environ.pop('COLUMNS', None)
                if columns is not None:
                    os.environ['COLUMNS'] = columns
                expected = captured_standard_diagnostic(width)
                with contextlib.redirect_stdout(SyntheticParentTTY()):
                    actual = HELPER._unknown_stderr('c6-cluster', 'reference-child.py')
                self.assertEqual(actual, expected)

    def test_color_environment_controls_remain_unchanged(self):
        controls = ('PYTHON_COLORS', 'NO_COLOR', 'FORCE_COLOR', 'TERM')
        for values in ({'PYTHON_COLORS': '0'}, {'PYTHON_COLORS': '1'},
                       {'NO_COLOR': '1'}, {'FORCE_COLOR': '1'}, {'TERM': 'dumb'}):
            with self.subTest(values=values), mock.patch.dict(os.environ):
                for key in (*controls, 'COLUMNS'):
                    os.environ.pop(key, None)
                os.environ.update(values)
                before = dict(os.environ)
                expected = captured_standard_diagnostic(78)
                with contextlib.redirect_stdout(SyntheticParentTTY()):
                    actual = HELPER._unknown_stderr('c6-cluster', 'reference-child.py')
                self.assertEqual(actual, expected)
                self.assertEqual(dict(os.environ), before)

    def test_parent_streams_restored_after_real_formatter_boundary_error(self):
        parent_out, parent_err = SyntheticParentTTY(), io.StringIO()
        with contextlib.redirect_stdout(parent_out), contextlib.redirect_stderr(parent_err):
            with mock.patch.object(argparse, 'HelpFormatter',
                                   side_effect=RuntimeError('inert fixture refusal')):
                with self.assertRaisesRegex(RuntimeError, 'inert fixture refusal'):
                    HELPER._unknown_stderr('c6-cluster', 'reference-child.py')
            self.assertIs(sys.stdout, parent_out)
            self.assertIs(sys.stderr, parent_err)
        self.assertEqual(parent_out.getvalue(), '')
        self.assertEqual(parent_err.getvalue(), '')


if __name__ == '__main__':
    unittest.main(verbosity=2)
