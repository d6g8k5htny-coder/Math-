"""Bounded source admission controls; never a compiled Lean inventory certificate."""
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('packet_admission_tests', ROOT / 'tools/lean_packet_admission.py')
admission = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(admission)


class CensusTests(unittest.TestCase):
    def scan(self, text):
        return admission.census(text, 'Test.Module', declarations=admission.declaration_binding(text))

    def test_opaque_declaration_headers_require_reviewed_binding(self):
        for header in ['theorem t : True := by trivial', 'def d := 0', 'abbrev A := Nat',
                       'instance named : Inhabited Nat := inferInstance', 'structure Z : Prop where']:
            trusted = header + '\n'
            binding = admission.declaration_binding(trusted)
            continuation = admission.continuation_binding(trusted)
            self.assertEqual(len(admission.census(trusted, 'M', continuation, binding)), 1)
            with self.subTest(header=header), self.assertRaisesRegex(ValueError, 'unsupported.*declaration header'):
                admission.census(trusted, 'M', continuation)
            for tail in [' register_option cbzHidden : Bool := { defValue := false, descr := "review" }',
                         ' newUnknownCommand cbz', ' (freshBinder : Nat)', ' := 37']:
                with self.subTest(header=header, tail=tail), self.assertRaisesRegex(ValueError, 'unsupported.*declaration header'):
                    admission.census(header + tail + '\n', 'M', continuation, binding)
        trusted = 'theorem t : True := by\n  trivial\n'
        with self.assertRaisesRegex(ValueError, 'unsupported.*declaration header'):
            admission.census(trusted.replace(': True', ': Bool'), 'M',
                             admission.continuation_binding(trusted.replace(': True', ': Bool')),
                             admission.declaration_binding(trusted))
        trusted = 'def s := "old"\n'
        with self.assertRaisesRegex(ValueError, 'unsupported.*declaration header'):
            admission.census(trusted.replace('old', 'new'), 'M', declarations=admission.declaration_binding(trusted))
        for malformed in [None, {}, [], {'sha256': '0' * 64, 'lines': True},
                          {'sha256': '0' * 64, 'lines': 1},
                          dict(admission.declaration_binding(trusted), extra=True)]:
            with self.subTest(binding=malformed), self.assertRaisesRegex(ValueError, 'unsupported.*declaration header'):
                admission.census(trusted, 'M', declarations=malformed)

    def test_physical_header_lines_keep_unicode_text_alignment(self):
        # Benign lexical fixtures: comments/literals never change LF row pairing.
        for separator in ['\r', '\v', '\f', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029']:
            for prefix in ['/- note' + separator + 'text' + separator + 'more\n-/\n',
                           '-- note' + separator + 'text\n',
                           'def text := "left' + separator + 'right"\n']:
                with self.subTest(separator=repr(separator), prefix=prefix):
                    text = prefix + 'def value := 0\n'
                    expected_headers = ([prefix] if prefix.startswith('def ') else []) + ['def value := 0\n']
                    expected = {'sha256': hashlib.sha256(''.join(expected_headers).encode()).hexdigest(),
                                'lines': len(expected_headers)}
                    self.assertEqual(admission.declaration_binding(text), expected)
                    changed = text.replace('def value := 0', 'def value := 1')
                    self.assertNotEqual(admission.declaration_binding(changed), expected)
                    self.assertEqual(len(admission.census(text, 'M', admission.continuation_binding(text), expected)), len(expected_headers))

    def test_physical_header_mapping_refuses_missing_lexical_lines(self):
        text = 'def value := 0\n'
        for code in ['def value := 0', 'def value := 0\n\n']:
            with self.subTest(code=code), self.assertRaisesRegex(ValueError, 'physical.line'):
                admission._declaration_binding(text, code)

    def test_indented_unknown_and_unsupported_commands_are_not_continuations(self):
        for command in ['newUnknownCommand cbz', 'register_option cbzHidden : Bool := { defValue := false, descr := "review" }']:
            for text in ['namespace A\nend A\n  ' + command + '\n',
                         'namespace A\ntheorem t : True := by trivial\n  ' + command + '\nend A\n',
                         '  ' + command + '\n']:
                with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'unsupported.*continuation'):
                    self.scan(text)

    def test_direct_placeholder_constant_is_refused_before_continuation_admission(self):
        for name in ['sorryAx', '_root_.sorryAx', 'Lean.sorryAx']:
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'forbidden token'):
                text = 'theorem t : True := by\n  have cbzUnused : False := ' + name + ' False true\n  trivial\n'
                admission.census(text, 'Test.Module', admission.continuation_binding(text), admission.declaration_binding(text))

    def test_opaque_continuations_require_exact_reviewed_binding(self):
        trusted = 'namespace A\ntheorem t : True := by\n  trivial\nend A\n'
        binding = admission.continuation_binding(trusted)
        self.assertEqual(admission.census(trusted, 'Test.Module', binding, admission.declaration_binding(trusted))[0]['name'], 'A.t')
        changed = [trusted.replace('  trivial', '  newUnknownCommand cbz'),
                   trusted.replace('end A', '  register_option cbz : Bool := { defValue := false }\nend A'),
                   trusted + '  newUnknownCommand cbz\n',
                   trusted.replace('  trivial\nend A', 'end A\n  trivial')]
        for text in changed:
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, 'unsupported.*continuation'):
                admission.census(text, 'Test.Module', binding)
        for malformed in [None, {}, [], {'sha256': '0' * 64, 'lines': True},
                          {'sha256': '0' * 64, 'lines': 1}, dict(binding, extra=True)]:
            with self.subTest(binding=malformed), self.assertRaisesRegex(ValueError, 'unsupported.*continuation'):
                admission.census(trusted, 'Test.Module', malformed)

    def test_column_zero_unknown_command_cannot_be_admitted_as_continuation(self):
        for command in [';', ')', 'newUnknownCommand cbz', 'variable {X : Type*}; newUnknownCommand cbz',
                        'variable {X : Type*} in newUnknownCommand cbz', 'open A in newUnknownCommand cbz']:
            text = 'namespace A\ntheorem t : True := by trivial\n' + command + '\nend A\n'
            with self.subTest(command=command), self.assertRaisesRegex(ValueError, 'unsupported command'):
                admission.census(text, 'Test.Module', admission.continuation_binding(text), admission.declaration_binding(text))

    def test_current_supported_declarations_and_scopes(self):
        text = ('namespace A\nsection S\nprivate theorem t : True := by trivial\n'
                'noncomputable def d : Nat := 0\nabbrev J := Nat\n'
                'instance named : Inhabited Nat := inferInstance\nend S\n'
                'namespace B\nstructure Z : Prop where\n  p : True\nend B\nend A\n')
        self.assertEqual(admission.census(text, 'Test.Module', admission.continuation_binding(text), admission.declaration_binding(text)), [
            dict(module='Test.Module', namespace=ns, name=name, kind=kind, privacy=privacy)
            for ns, name, kind, privacy in [('A', 'A.t', 'theorem', 'private'), ('A', 'A.d', 'def', 'public'),
                                          ('A', 'A.J', 'abbrev', 'public'), ('A', 'A.named', 'instance', 'public'),
                                          ('A.B', 'A.B.Z', 'structure', 'public')]])

    def test_comments_cannot_join_or_hide_commands(self):
        self.assertEqual(len(self.scan('theorem/- nested /- axiom -/ -/ t : True := by trivial\n')), 1)
        self.assertEqual(self.scan('/- theorem fake : False := by sorry -/\n-- axiom fake : False\n'), [])
        with self.assertRaisesRegex(ValueError, 'forbidden token'):
            self.scan('axiom/- comment -/ bad : False\n')

    def test_literals_do_not_fabricate_declarations_or_comments(self):
        self.assertEqual([d['name'] for d in self.scan('def x := "-- /- theorem fake axiom"\ntheorem t : True := by trivial\n')], ['x', 't'])
        self.assertEqual(len(self.scan('def x := r#"/- axiom"#\ndef y := \'x\'\n')), 2)
        self.assertEqual(len(self.scan("def x' := 1\ndef y := x'\n")), 2)
        with self.assertRaisesRegex(ValueError, 'forbidden token'):
            self.scan('def s := "--"\naxiom bad : False\n')

    def test_lean_image_notation_is_not_a_character(self):
        self.assertEqual(len(self.scan("def x := f '' A\n")), 1)

    def test_unterminated_and_interpolated_lexical_inputs_rejected(self):
        for text in ['/- open', 'def s := "open', 'def s := r#"open', "def x := 'z", 'def x := s!"{True}"', 'def x := "{x}"']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.scan(text)

    def test_forbidden_tokens_even_in_unused_or_qualified_terms(self):
        for token in ['sorry', 'admit', 'axiom', 'native_decide', 'implemented_by', 'extern', 'unsafe',
                      'Lean.ofReduceBool', 'Lean.trustCompiler', 'Lean.addDecl']:
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, 'forbidden token|unsupported'):
                self.scan('def unused := ' + token + '\n')

    def test_unsupported_declaration_and_command_forms_fail_closed(self):
        for text in ['  theorem t : True := by trivial', '@[simp] theorem t : True := by trivial',
                     '@[simp]\ntheorem t : True := by trivial', 'protected theorem t : True := by trivial',
                     'private\ntheorem t : True := by trivial', 'theorem t : True := by trivial; theorem u : True := by trivial',
                     'instance : Inhabited Nat := inferInstance', 'class C where', 'inductive I',
                     'mutual\ndef d := 0\nend', 'example : True := by trivial', 'initialize x := pure 0',
                     'open Lean in run_elab do pure ()', 'def d := by run_tac pure ()',
                     'set_option maxHeartbeats 0 in theorem x : True := by trivial',
                     'notation "foo" => True', 'attribute [simp] t', '#eval 1', 'def «quoted» := 0',
                     'namespace A; theorem t : True := by trivial', 'newUnknownCommand x',
                     'noncomputable section', '  alias x := t', 'export X (foo)', 'def d := by_elab pure ()']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.scan(text + '\n')

    def test_balanced_named_scope_and_duplicates_required(self):
        for text in ['namespace A\nend B', 'namespace A', 'section\nend', 'end A',
                     'theorem t : True := by trivial\ntheorem t : True := by trivial']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.scan(text)

    def test_census_exact_order_and_schema(self):
        actual = self.scan('theorem t : True := by trivial\ndef d := 0\n')
        admission.check_census(actual, actual)
        for bad in [None, {}, [], list(reversed(actual)), actual + actual, [dict(actual[0], extra=True)],
                    [dict(actual[0], privacy='protected')], [dict(actual[0], kind='axiom')], ['t']]:
            with self.subTest(bad=bad), self.assertRaisesRegex(ValueError, 'source declaration census'):
                admission.check_census(actual, bad)


class HelperIntegrityTests(unittest.TestCase):
    def gates(self):
        for packet in ['determinant_moment_20261025', 'cap_first_exit_lean_20261002']:
            spec = importlib.util.spec_from_file_location('integrity_' + packet, ROOT / 'frontiers' / packet / 'gate.py')
            gate = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gate)
            yield packet, gate

    def test_verified_fixed_helper_can_be_loaded(self):
        data = (ROOT / 'tools/lean_packet_admission.py').read_bytes()
        for packet, gate in self.gates():
            with self.subTest(packet=packet):
                helper = gate.load_admission(ROOT, {'helper_sha256': hashlib.sha256(data).hexdigest(), 'census': [], 'continuations': {}, 'declarations': {}})
                self.assertEqual(helper['census']('def d := 0\n', 'M', declarations=helper['declaration_binding']('def d := 0\n'))[0]['name'], 'd')

    def test_substitution_is_rejected_before_helper_execution(self):
        for packet, gate in self.gates():
            with self.subTest(packet=packet), tempfile.TemporaryDirectory() as d:
                repo = Path(d)
                (repo / 'tools').mkdir()
                marker = repo / 'executed'
                payload = ('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("executed")\n')
                (repo / 'tools/lean_packet_admission.py').write_text(payload)
                with self.assertRaisesRegex(ValueError, 'admission helper hash mismatch'):
                    gate.load_admission(repo, {'helper_sha256': '0' * 64, 'census': [], 'continuations': {}, 'declarations': {}})
                self.assertFalse(marker.exists(), 'unverified helper executed')

    def test_helper_and_parent_symlinks_rejected_even_with_matching_digest(self):
        data = (ROOT / 'tools/lean_packet_admission.py').read_bytes()
        metadata = {'helper_sha256': hashlib.sha256(data).hexdigest(), 'census': [], 'continuations': {}, 'declarations': {}}
        for packet, gate in self.gates():
            for target in ['file', 'tools', 'repo', 'ancestor']:
                with self.subTest(packet=packet, target=target), tempfile.TemporaryDirectory() as d:
                    root = Path(d)
                    repo = root / 'repo'
                    (repo / 'tools').mkdir(parents=True)
                    (repo / 'tools/lean_packet_admission.py').write_bytes(data)
                    if target == 'file':
                        helper = repo / 'tools/lean_packet_admission.py'
                        helper.unlink()
                        helper.symlink_to(ROOT / 'tools/lean_packet_admission.py')
                    elif target == 'tools':
                        (repo / 'tools/lean_packet_admission.py').unlink()
                        (repo / 'tools').rmdir()
                        (repo / 'tools').symlink_to(ROOT / 'tools', target_is_directory=True)
                    elif target == 'ancestor':
                        alias = root / 'alias'
                        alias.symlink_to(root, target_is_directory=True)
                        repo = alias / 'repo'
                    else:
                        alias = root / 'alias'
                        alias.symlink_to(repo, target_is_directory=True)
                        repo = alias
                    with self.assertRaisesRegex(ValueError, 'symlink admission helper'):
                        gate.load_admission(repo, metadata)

    def test_metadata_cannot_redirect_helper_or_omit_digest(self):
        for packet, gate in self.gates():
            for metadata in [None, {}, {'helper_sha256': '0' * 64, 'census': [], 'continuations': {}, 'path': '/tmp/evil.py'},
                             {'helper_sha256': True, 'census': [], 'continuations': {}, 'declarations': {}}]:
                with self.subTest(packet=packet, metadata=metadata), self.assertRaises(ValueError):
                    gate.load_admission(ROOT, metadata)


if __name__ == '__main__':
    unittest.main()
