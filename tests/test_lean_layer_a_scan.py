"""Self-tests for tools/lean_layer_a_scan.py (CBZ-0 gate G0).

The scanner certifies Layer A, so it must itself be shown to catch what it claims:
planted violations in every code position are found, the same text in comments and
literals is not, malformed input is a lex error rather than a silent pass, and every
mutant of the scanner's own source is killed by this suite.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import lean_layer_a_scan as scan  # noqa: E402

SCANNER = ROOT / 'tools' / 'lean_layer_a_scan.py'


def hits(text):
    return [(f['line'], f['token']) for f in scan.findings_for_text(text)]


class CodePositionTests(unittest.TestCase):
    def test_every_forbidden_name_is_found_in_code(self):
        for token, invariant in scan.FORBIDDEN.items():
            with self.subTest(token=token):
                found = scan.findings_for_text('theorem t : True := by\n  ' + token + '\n')
                self.assertEqual([(f['line'], f['token'], f['invariant']) for f in found],
                                 [(2, token, invariant)])

    def test_forms_of_placeholders_and_escapes(self):
        cases = {
            'theorem a : 1 = 1 := sorry': [(1, 'sorry')],
            'example : P := by admit': [(1, 'admit')],
            'axiom bad : False': [(1, 'axiom')],
            'example : 2 + 2 = 4 := by native_decide': [(1, 'native_decide')],
            'def x := Lean.ofReduceBool': [(1, 'ofReduceBool')],
            'def y : Float := 1.5': [(1, 'Float')],
            'def z := Float.ofScientific 1 true 1': [(1, 'Float')],
            '@[implemented_by foo] def w := 0': [(1, 'implemented_by')],
            '@[extern "c"] opaque e : Nat': [(1, 'extern')],
            'unsafe def u := 0': [(1, 'unsafe')],
            'def q := «sorry»': [(1, 'sorry')],
            'def r := Foo.«sorryAx»': [(1, 'sorryAx')],
            'theorem s : P := (sorry)': [(1, 'sorry')],
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(hits(text), expected)

    def test_line_numbers_follow_comments_and_strings(self):
        text = '/- one\ntwo -/\ndef s := "a\nb"\n-- c\ntheorem t : P := sorry\n'
        self.assertEqual(hits(text), [(6, 'sorry')])

    def test_interpolation_holes_are_code(self):
        # Codex review 4415546474: the holes of s!/m!/f! strings are expressions.
        self.assertEqual(hits('def s := s!"{(sorry : Nat)}"'), [(1, 'sorry')])
        self.assertEqual(hits('def s := m!"x {f admit} y"'), [(1, 'admit')])
        self.assertEqual(hits('def s := s!"a\n{\n  (sorry : Nat)}"'), [(3, 'sorry')])
        self.assertEqual(hits('def s := s!"{g {h := sorry}}"'), [(1, 'sorry')])
        self.assertEqual(hits('def s := s!"literal sorry {x} admit"'), [])
        self.assertEqual(hits('def s := s!"escaped \\{sorry}"'), [])
        self.assertEqual(hits('def s := "{sorry}"'), [])

    def test_raw_strings(self):
        # Codex review 4415546483: raw strings have no escapes and may use # delimiters.
        self.assertEqual(hits('def s := r#"a "sorry" b"#'), [])
        self.assertEqual(hits('def s := r"\\"\ntheorem t : False := sorry\n-- "'), [(2, 'sorry')])
        self.assertEqual(hits('def s := r##"x "# sorry"##\ndef u := admit'), [(2, 'admit')])
        self.assertEqual(hits('def r := sorry'), [(1, 'sorry')])
        self.assertEqual(hits('def x := bar"y"'), [])

    def test_code_after_a_comment_on_the_same_line(self):
        self.assertEqual(hits('/- c -/ sorry'), [(1, 'sorry')])
        self.assertEqual(hits('def a := "x" ++ sorry'), [(1, 'sorry')])


class NonCodeTests(unittest.TestCase):
    def test_prose_and_literals_are_ignored(self):
        for text in (
            '-- these densities admit versions; no sorry here',
            '/-- docstring: uses no `sorry`, `native_decide` or Float. -/',
            '/-! module doc: axiom audit is separate -/',
            '/- outer /- nested sorry -/ still comment admit -/',
            'def s := "sorry admit axiom Float"',
            'def t := "escaped \\" quote sorry"',
            "def c := 'a'",
            "def d := '\\n'",
            'def e := "contains -- and /- not comments"',
        ):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [])

    def test_identifiers_that_merely_contain_a_name_are_not_hits(self):
        for text in ('def sorryCount := 0', 'theorem admits_bound : P := h',
                     'def axiomatic := 0', 'def Floating := 0', "def x' := sorry'"):
            with self.subTest(text=text):
                self.assertEqual(hits(text), [])

    def test_text_after_a_comment_close_is_code_again(self):
        self.assertEqual(hits('/- a /- b -/ c -/ admit'), [(1, 'admit')])


class MalformedInputTests(unittest.TestCase):
    def test_unclosed_interpolation_hole_raises(self):
        # Through the full lexer an unclosed hole also leaves its string unterminated, so
        # the helper's own refusal is pinned directly.
        for text in ('{abc', '{a {b} c', '{"}" x'):
            with self.subTest(text=text), self.assertRaises(scan.LexError):
                scan._hole_end(text, 0)
        self.assertEqual(scan._hole_end('{a {b} "}" c} d', 0), 12)

    def test_unterminated_regions_raise(self):
        for text in ('/- never closed sorry', '/- /- one level closed -/ sorry',
                     'def s := "never closed', 'def q := «never closed',
                     'def r := r#"never closed"', 'def h := s!"{unclosed"'):
            with self.subTest(text=text):
                with self.assertRaises(scan.LexError):
                    scan.findings_for_text(text)

    def test_cli_reports_lex_errors_with_exit_two_and_findings_with_exit_one(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / 'ok.lean').write_text('theorem t : True := trivial\n')
            (root / 'bad.lean').write_text('theorem t : P := sorry\n')
            (root / 'broken.lean').write_text('/- open\n')
            run = lambda *p: subprocess.run([sys.executable, '-I', str(SCANNER), '--root', td, *p],
                                            capture_output=True, text=True)
            self.assertEqual(run('ok.lean').returncode, 0)
            bad = run('ok.lean', 'bad.lean')
            self.assertEqual(bad.returncode, 1)
            self.assertIn('bad.lean:1: A1 sorry', bad.stdout)
            broken = run('ok.lean', 'bad.lean', 'broken.lean')
            self.assertEqual(broken.returncode, 2)
            self.assertIn('broken.lean: LEX ERROR unterminated block comment', broken.stdout)

    def test_default_scope_is_every_tracked_lean_file_outside_lake(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            for cmd in (['init', '-q'],):
                subprocess.run(['git', *cmd], cwd=td, check=True)
            (root / 'a').mkdir()
            (root / 'a' / 'x.lean').write_text('def x := sorry\n')
            (root / '.lake').mkdir()
            (root / '.lake' / 'y.lean').write_text('def y := sorry\n')
            (root / 'untracked.lean').write_text('def z := sorry\n')
            subprocess.run(['git', 'add', 'a/x.lean', '-f', '.lake/y.lean'], cwd=td, check=True)
            self.assertEqual(scan.tracked_lean_files(root), ['a/x.lean'])


class RepositoryScanTests(unittest.TestCase):
    """G1 on this tree: no tracked Lean file has a forbidden name in code."""

    def test_tracked_lean_files_have_no_layer_a_findings(self):
        files = scan.tracked_lean_files(ROOT)
        self.assertGreater(len(files), 0, 'no tracked Lean files found: the scan would be vacuous')
        report = scan.scan(ROOT, files)
        self.assertEqual(report['lex_errors'], [])
        self.assertEqual(report['findings'], [])


MUTANTS = [
    # (description, old, new): each must make this suite fail.
    ('drop sorry', "'sorry': 'A1', ", ''),
    ('drop admit', "'admit': 'A1', ", ''),
    ('drop axiom', "'axiom': 'A2',", ''),
    ('drop native_decide', "'native_decide': 'A2', ", ''),
    ('drop Float', "'Float': 'A3', ", ''),
    ('whole name only, no components', 'hits = [p for p in parts if p in FORBIDDEN]',
     'hits = [name] if name in FORBIDDEN else []'),
    ('block comments not nested', 'depth, i = depth + 1, i + 2', 'i = i + 2'),
    ('unterminated comment passes', "raise LexError('unterminated block comment", "return\n                    raise LexError('x"),
    ('string escapes ignored', "if text[i] == '\\\\':", "if False:"),
    ('line comments swallow the file', "i = n if j < 0 else j", "i = n"),
    ('lex errors exit 0', "return 2 if report['lex_errors'] else", "return 0 if report['lex_errors'] else"),
    ('findings exit 0', "else 1 if report['findings'] else 0", "else 0"),
    ('lake not excluded', "if p and '/.lake/' not in '/' + p", "if p"),
    ('guillemets dropped', "parts.append(text[i + 1:j])", "parts.append('')"),
    ('line count frozen', "line += 1\n            i += 1", "i += 1"),
    ('interpolation holes skipped', "elif interpolated and text[i] == '{':", "elif False:"),
    ('interpolation never detected', "interpolated = i >= 2 and", "interpolated = False and"),
    ('raw strings not recognised', "elif c == 'r' and RAW_OPEN.match(text, i)", "elif False and RAW_OPEN.match(text, i)"),
    ('raw string hashes ignored', "start, close = line, '\"' + hashes", "start, close = line, '\"'"),
    ('unclosed hole passes', "raise LexError('unterminated interpolation hole')", "return n"),
]


class ScannerMutationTests(unittest.TestCase):
    """Run this suite (minus this class) against mutated scanners; every mutant must fail."""

    def run_suite(self, scanner_source):
        here = pathlib.Path(__file__).read_text()
        with tempfile.TemporaryDirectory() as td:
            tools = pathlib.Path(td) / 'tools'
            tests = pathlib.Path(td) / 'tests'
            tools.mkdir()
            tests.mkdir()
            (tools / 'lean_layer_a_scan.py').write_text(scanner_source)
            (tests / 'test_lean_layer_a_scan.py').write_text(here)
            return subprocess.run(
                [sys.executable, '-B', '-m', 'unittest', '-q', 'test_lean_layer_a_scan.CodePositionTests',
                 'test_lean_layer_a_scan.NonCodeTests', 'test_lean_layer_a_scan.MalformedInputTests'],
                cwd=tests, capture_output=True, text=True, timeout=120)

    def test_harness_control_unmutated_scanner_passes(self):
        # Without this, an import or harness failure would make every mutant look killed.
        run = self.run_suite(SCANNER.read_text())
        self.assertEqual(run.returncode, 0, run.stderr[-2000:])

    def test_every_mutant_is_killed(self):
        source = SCANNER.read_text()
        for desc, old, new in MUTANTS:
            with self.subTest(mutant=desc):
                self.assertEqual(source.count(old), 1, 'mutation anchor missing or ambiguous: ' + desc)
                run = self.run_suite(source.replace(old, new))
                self.assertNotEqual(run.returncode, 0, 'mutant survived: ' + desc)
                self.assertIn('FAILED', run.stderr, 'mutant died without a test failure: ' + desc)


if __name__ == '__main__':
    unittest.main()
