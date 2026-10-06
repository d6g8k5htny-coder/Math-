"""RF-GATE-01: the environment inventory, grammar pre-check and comment stripper.

Synthetic fixtures only; nothing here compiles Lean. The authoritative inventory is produced
by `inventory_source()` inside `gate.py --execute` and audited by `audit_inventory`.
"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('inventory_gate_under_test', ROOT / 'gate.py')
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

P = gate.PACKAGE
MODULES = {P + '.Alpha', P + '.Beta'}
TARGETS = [P + '.first', P + '.second']
STD = 'Classical.choice, Quot.sound, propext'


def inv(kind, module, name):
    return 'INV|' + kind + '|' + module + '|' + name


def table(alpha=4, beta=4, root='0', is_module='false', extra='0'):
    return [
        'MODULE|' + P + '.Alpha|' + is_module + '|' + str(alpha) + '|' + extra,
        'MODULE|' + P + '.Beta|' + is_module + '|' + str(beta) + '|' + extra,
        'MODULE|' + P + '|false|' + root + '|' + root,
    ]


def clean(axioms=STD, closure='500', **kw):
    return '\n'.join(table(**kw) + [
        inv('theorem', P + '.Alpha', P + '.first'),
        inv('theorem', P + '.Beta', P + '.second'),
        inv('def', P + '.Alpha', P + '.helper'),
        inv('theorem', P + '.Alpha', P + '.first.proof_1'),
        inv('theorem', P + '.Alpha', P + '.helper._simp_1'),
        inv('inductive', P + '.Beta', P + '.Shape'),
        inv('ctor', P + '.Beta', P + '.Shape.circle'),
        inv('rec', P + '.Beta', P + '.Shape.rec'),
        'AXIOMS|[' + axioms + ']',
        'CLOSURE|' + closure,
    ])


class StripCommentsTests(unittest.TestCase):
    def test_line_comment(self):
        self.assertEqual(gate.strip_lean_comments('theorem a -- theorem hidden\n:= rfl'), 'theorem a \n:= rfl')

    def test_block_comment_nested(self):
        self.assertEqual(gate.strip_lean_comments('x /- a /- theorem b -/ sorry -/ y'), 'x  y')

    def test_doc_comment(self):
        self.assertEqual(gate.strip_lean_comments('/-- doc with sorry -/\ntheorem a : True := trivial'), '\ntheorem a : True := trivial')

    def test_line_comment_inside_block_does_not_close(self):
        self.assertEqual(gate.strip_lean_comments('/- -- still -/ z'), ' z')

    def test_newline_positions_preserved(self):
        text = 'a -- c\n/- b\n c -/ d\n/- x /- y\n -/ -/ e\n'
        stripped = gate.strip_lean_comments(text)
        self.assertEqual([i for i, ch in enumerate(text) if ch == '\n'][-1:], [len(text) - 1])
        self.assertEqual(stripped.count('\n'), text.count('\n'))
        self.assertEqual(stripped.splitlines()[2], ' d')

    def test_unterminated(self):
        with self.assertRaises(ValueError):
            gate.strip_lean_comments('/- open forever')

    def test_no_comments(self):
        text = 'theorem a : True := trivial\n'
        self.assertEqual(gate.strip_lean_comments(text), text)


class GrammarCheckTests(unittest.TestCase):
    def test_canonical_names(self):
        text = 'namespace X\ntheorem first : True := trivial\nlemma second : True := trivial\nend X\n'
        self.assertEqual(gate.grammar_check(text, 'm.lean'), ['first', 'second'])

    def test_indented_theorem_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('namespace X\n  theorem hidden : True := trivial\nend X\n', 'm.lean')

    def test_private_theorem_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('private theorem hidden : True := trivial\n', 'm.lean')

    def test_protected_theorem_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('protected theorem hidden : True := trivial\n', 'm.lean')

    def test_attribute_same_line_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('@[simp] theorem hidden : True := trivial\n', 'm.lean')

    def test_attribute_previous_line_allowed(self):
        self.assertEqual(gate.grammar_check('@[simp]\ntheorem ok : True := trivial\n', 'm.lean'), ['ok'])

    def test_keyword_inside_comment_ignored(self):
        text = '-- theorem commented : False\n/- lemma also : False -/\ntheorem ok : True := trivial\n'
        self.assertEqual(gate.grammar_check(text, 'm.lean'), ['ok'])

    def test_keyword_as_identifier_part_ignored(self):
        self.assertEqual(gate.grammar_check('def my_theorem_count : Nat := 1\ntheorem ok : True := trivial\n', 'm.lean'), ['ok'])

    def test_keyword_in_string_refused(self):
        # Conservative: the pre-check cannot parse string literals, so it refuses rather than guesses.
        with self.assertRaises(ValueError):
            gate.grammar_check('def s : String := "a theorem walks in"\n', 'm.lean')

    def test_apostrophe_and_unicode_names_refused(self):
        for name in ("foo'", '\u00abhidden\u00bb', 'foo\u2713'):
            with self.assertRaises(ValueError):
                gate.grammar_check('theorem ' + name + ' : True := trivial\n', 'm.lean')

    def test_tab_and_public_modifiers_refused(self):
        for line in ('private\ttheorem hidden : True := trivial\n', 'public theorem hidden : True := trivial\n', 'theorem\thidden : True := trivial\n'):
            with self.assertRaises(ValueError, msg=line):
                gate.grammar_check(line, 'm.lean')

    def test_refusal_names_original_line_number(self):
        text = '/- a\n b -/\n-- c\nnamespace X\n  theorem hidden : True := trivial\nend X\n'
        with self.assertRaises(ValueError) as cm:
            gate.grammar_check(text, 'm.lean')
        self.assertIn('m.lean:5', str(cm.exception))

    def test_sorry_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('theorem bad : False := by sorry\n', 'm.lean')

    def test_sorry_in_comment_allowed(self):
        self.assertEqual(gate.grammar_check('-- no sorry here\ntheorem ok : True := trivial\n', 'm.lean'), ['ok'])

    def test_axiom_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('axiom hidden : False\n', 'm.lean')

    def test_native_decide_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('theorem t : 2 + 2 = 4 := by native_decide\n', 'm.lean')

    def test_implemented_by_extern_unsafe_refused(self):
        for token in ('@[implemented_by f]', '@[extern "c"]', 'unsafe'):
            with self.assertRaises(ValueError):
                gate.grammar_check(token + ' def g : Nat := 0\n', 'm.lean')

    def test_sorryAx_identifier_not_matched_as_sorry(self):
        # `sorryAx` is a different token; the transitive audit catches it, not the grammar.
        self.assertEqual(gate.grammar_check('theorem ok : True := trivial -- sorryAx\n', 'm.lean'), ['ok'])

    def test_unterminated_comment_refused(self):
        with self.assertRaises(ValueError):
            gate.grammar_check('/- theorem a : True := trivial\n', 'm.lean')


class InventorySourceTests(unittest.TestCase):
    def test_package_import_and_module_table_enumeration(self):
        src = gate.inventory_source()
        self.assertTrue(src.startswith('import ' + P + '\nimport Lean\n'))
        self.assertIn('header.moduleData[idx]!', src)
        self.assertIn('pkg.isPrefixOf m', src)
        self.assertIn('data.constNames', src)
        self.assertIn('e.getUsedConstants.forM', src)
        for rule in ('.axiomInfo v', '.defnInfo v', '.thmInfo v', '.opaqueInfo v', '.quotInfo _', '.ctorInfo v', '.recInfo v', '.inductInfo v', '| none'):
            self.assertIn(rule, src, rule)
        self.assertIn('if includeLocal then', src)
        self.assertTrue(src.rstrip().endswith('`' + P + ' false'))

    def test_local_mode_adds_current_file_constants(self):
        src = gate.inventory_source(include_local=True)
        self.assertIn('map\u2082', src)
        self.assertIn('`_local', src)
        self.assertEqual(src.count('import Lean\n'), 1)
        self.assertTrue(src.rstrip().endswith('`' + P + ' true'))

    def test_missing_constant_is_fatal_in_lean(self):
        self.assertIn('throw (IO.userError', gate.inventory_source())


class AuditInventoryTests(unittest.TestCase):
    def test_clean_passes(self):
        report = gate.audit_inventory(clean(), TARGETS, MODULES)
        self.assertEqual(report['public_theorems'], sorted(TARGETS))
        self.assertEqual(report['declarations'], 8)
        self.assertEqual(report['axioms'], ['Classical.choice', 'Quot.sound', 'propext'])
        self.assertEqual(report['closure'], 500)
        self.assertEqual(len(report['sha256']), 64)

    def test_axiom_free_closure_passes(self):
        self.assertEqual(gate.audit_inventory(clean(axioms=''), TARGETS, MODULES)['axioms'], [])

    def test_report_is_deterministic(self):
        self.assertEqual(gate.audit_inventory(clean(), TARGETS, MODULES), gate.audit_inventory(clean(), TARGETS, MODULES))

    def test_noise_lines_ignored_but_inventory_required(self):
        gate.audit_inventory('warning: something\n' + clean() + '\ntrailing', TARGETS, MODULES)
        with self.assertRaises(ValueError):
            gate.audit_inventory('warning: only\n', TARGETS, MODULES)

    def test_hidden_sorry_anywhere_in_closure_rejected(self):
        text = clean(axioms=STD + ', sorryAx', alpha=5) + '\n' + inv('theorem', P + '.Alpha', '_private.' + P + '.Alpha.0.' + P + '.hidden')
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(text, TARGETS, MODULES)
        self.assertIn('sorryAx', str(cm.exception))

    def test_custom_axiom_in_closure_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(axioms=STD + ', Other.hidden'), TARGETS, MODULES)

    def test_extra_public_theorem_rejected(self):
        text = clean(alpha=5) + '\n' + inv('theorem', P + '.Alpha', P + '.indentedExtra')
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(text, TARGETS, MODULES)
        self.assertIn('indentedExtra', str(cm.exception))

    def test_axiom_kind_rejected_even_if_unused(self):
        text = clean(alpha=5) + '\n' + inv('axiom', P + '.Alpha', P + '.hiddenPremise')
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(text, TARGETS, MODULES)
        self.assertIn('axiom declared inside package', str(cm.exception))

    def test_unregistered_module_rejected(self):
        text = clean() + '\nMODULE|' + P + '.Gamma|false|1|0\n' + inv('def', P + '.Gamma', P + '.stray')
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(text, TARGETS, MODULES)
        self.assertIn('not registered', str(cm.exception))

    def test_declaration_outside_table_rejected(self):
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(clean() + '\n' + inv('def', P + '.Gamma', P + '.stray'), TARGETS, MODULES)
        self.assertIn('outside registered modules', str(cm.exception))

    def test_registered_module_missing_from_table_rejected(self):
        text = '\n'.join(line for line in clean().splitlines() if not line.startswith('MODULE|' + P + '.Beta|'))
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(text, TARGETS, MODULES)
        self.assertIn('module table differs', str(cm.exception))

    def test_module_system_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(is_module='true'), TARGETS, MODULES)

    def test_root_module_must_be_empty(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(root='1'), TARGETS, MODULES)

    def test_codegen_extra_constants_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(extra='1'), TARGETS, MODULES)

    def test_count_mismatch_rejected(self):
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(clean(alpha=3), TARGETS, MODULES)
        self.assertIn('count differs', str(cm.exception))

    def test_local_module_rejected_unless_allowed(self):
        text = clean() + '\n' + inv('def', '_local', '_inv.kind')
        with self.assertRaises(ValueError):
            gate.audit_inventory(text, TARGETS, MODULES)
        gate.audit_inventory(text, TARGETS, MODULES, allow_local=True)

    def test_local_public_theorem_rejected_even_when_local_allowed(self):
        text = clean() + '\n' + inv('theorem', '_local', P + '.indentedAdmission')
        with self.assertRaises(ValueError):
            gate.audit_inventory(text, TARGETS, MODULES, allow_local=True)

    def test_missing_target_rejected(self):
        text = '\n'.join(line for line in clean(beta=3).splitlines() if P + '.second' not in line)
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(text, TARGETS, MODULES)
        self.assertIn('missing', str(cm.exception))

    def test_duplicate_name_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(alpha=5) + '\n' + inv('theorem', P + '.Alpha', P + '.first'), TARGETS, MODULES)

    def test_duplicate_module_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean() + '\nMODULE|' + P + '.Alpha|false|4|0', TARGETS, MODULES)

    def test_axiom_closure_line_required_exactly_once(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean() + '\nAXIOMS|[]', TARGETS, MODULES)
        with self.assertRaises(ValueError):
            gate.audit_inventory('\n'.join(l for l in clean().splitlines() if not l.startswith('AXIOMS|')), TARGETS, MODULES)
        with self.assertRaises(ValueError):
            gate.audit_inventory('\n'.join(l for l in clean().splitlines() if not l.startswith('CLOSURE|')), TARGETS, MODULES)

    def test_closure_smaller_than_inventory_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(closure='3'), TARGETS, MODULES)

    def test_per_target_audit_cross_check(self):
        gate.audit_inventory(clean(), TARGETS, MODULES, reported_axioms={TARGETS[0]: ['propext'], TARGETS[1]: []})
        gate.audit_inventory(clean(), TARGETS, MODULES, reported_axioms={})
        with self.assertRaises(ValueError) as cm:
            gate.audit_inventory(clean(axioms='propext'), TARGETS, MODULES, reported_axioms={TARGETS[0]: ['propext', 'Quot.sound']})
        self.assertIn('closure omits', str(cm.exception))

    def test_malformed_line_rejected(self):
        for bad in ('INV|theorem|' + P + '.Alpha', 'INV|macro|' + P + '.Alpha|x', 'INV|theorem|' + P + '.Alpha|bad name', 'MODULE|' + P + '.Alpha|maybe|1|0', 'AXIOMS|propext'):
            with self.assertRaises(ValueError):
                gate.audit_inventory(clean() + '\n' + bad, TARGETS, MODULES)

    def test_empty_targets_or_modules_rejected(self):
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(), [], MODULES)
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(), TARGETS + [TARGETS[0]], MODULES)
        with self.assertRaises(ValueError):
            gate.audit_inventory(clean(), TARGETS, set())

    def test_aux_pattern_scope(self):
        for aux in (P + '.first.proof_1', P + '.first.match_2', P + '.helper._eq_1', P + '.first.eq_3', P + '._auxLemma.1', '_private.' + P + '.Alpha.0.' + P + '.hidden'):
            self.assertTrue(gate.AUX.search(aux), aux)
        for public in (P + '.first', P + '.helper.proof', P + '.proofs_of_first', P + '.matching'):
            self.assertFalse(gate.AUX.search(public), public)


class SourceCheckIntegrationTests(unittest.TestCase):
    def test_live_modules_pass_grammar_and_match_manifest(self):
        m = gate.load_json((ROOT / 'manifest.json').read_text())
        names = []
        for path in m['source_modules']:
            names.extend(P + '.' + n for n in gate.grammar_check((ROOT / path).read_text(), path))
        self.assertEqual(names, m['targets'])

    def test_required_files_bound(self):
        m = gate.load_json((ROOT / 'manifest.json').read_text())
        for name in ('tests/test_inventory_gate.py', 'GATE_HARDENING.md', 'gate.py'):
            self.assertIn(name, m['files'])


if __name__ == '__main__':
    unittest.main()
