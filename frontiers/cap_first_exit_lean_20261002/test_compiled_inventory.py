"""Behavioral controls for the Cap-local compiled census; fixtures are synthetic."""
import copy
import importlib.util
import inspect
import pathlib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
PACKET = HERE if (HERE / 'gate.py').is_file() else HERE.parent / 'Math-/frontiers/cap_first_exit_lean_20261002'


def enc(*parts):
    return '/'.join('n' + str(p) if type(p) is int else 's' + p.encode().hex() for p in parts)


M = enc('CapFirstExit')
T = enc('CapFirstExit', 'visible')
D = enc('CapFirstExit', 'datum')
S = enc('CapFirstExit', 'CapHyp')
P = enc('CapFirstExit', 'CapHyp', 'field')
C = enc('CapFirstExit', 'CapHyp', 'mk')
R = enc('CapFirstExit', 'CapHyp', 'rec')
A = enc('CapFirstExit', 'visible', '_proof_1')
VISIBLE = {'CapFirstExit.visible': 'theorem', 'CapFirstExit.datum': 'def', 'CapFirstExit.CapHyp': 'inductive'}
ROWS = [('theorem', 'user', M, T, 'safe'), ('def', 'user', M, D, 'safe'),
        ('inductive', 'user', M, S, 'safe'), ('def', 'user', M, P, 'safe'),
        ('ctor', 'user', M, C, 'safe'), ('rec', 'user', M, R, 'safe'),
        ('theorem', 'aux', M, A, 'safe')]
BOUND = [list(r) for r in ROWS[3:]]
RELATIONS = [('projection', P, S), ('constructor', C, S), ('recursor', R, S)]


def transcript(rows=None, relations=None, axioms=None, count=None, extra=0, module=M, module_system='false'):
    rows = ROWS if rows is None else rows
    relations = RELATIONS if relations is None else relations
    axioms = [enc('propext')] if axioms is None else axioms
    count = len(rows) if count is None else count
    lines = ['MODULE|%s|%s|%d|%d' % (module, module_system, count, extra)]
    lines += ['INV|' + '|'.join(r) for r in rows]
    lines += ['REL|%s|%s|%s' % (kind, name, parent) for kind, name, parent in relations]
    lines += ['AXIOMS|' + ','.join(axioms), 'CLOSURE|%d' % (len(rows) + len(axioms) + 10)]
    return '\n'.join(lines) + '\n'


class CompiledInventory(unittest.TestCase):
    def setUp(self):
        path = PACKET / 'compiled_inventory.py'
        self.assertTrue(path.is_file(), 'Cap compiled admission implementation is absent')
        spec = importlib.util.spec_from_file_location('cap_compiled_inventory_under_test', path)
        self.api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.api)

    def reject(self, text, code, bound=None, visible=None, reported=None):
        with self.assertRaises(ValueError) as ctx:
            self.api.audit_inventory(text, VISIBLE if visible is None else visible,
                                     BOUND if bound is None else bound, reported_axioms=reported)
        self.assertIn(code, str(ctx.exception))

    def test_nonempty_cap_module_and_mixed_visible_kinds_pass(self):
        report = self.api.audit_inventory(transcript(), VISIBLE, BOUND)
        self.assertEqual(report['declarations'], 7)
        self.assertEqual(report['visible_declarations'], 3)
        self.assertEqual(report['axioms'], ['propext'])

    def test_lossless_unicode_private_and_numeric_names(self):
        self.assertEqual(self.api.decode('s43/sceb1/n0'), ('C', 'α', 0))
        self.assertEqual(self.api.encode(('C', 'α', 0)), 's43/sceb1/n0')
        self.assertNotEqual(self.api.decode('s412e42'), self.api.decode('s41/s42'))
        for name in (('_private', '.lake', 0, 'CapFirstExit', 'x'), ('CapFirstExit', 'swap₁₂')):
            self.assertEqual(self.api.decode(self.api.encode(name)), name)

    def test_noncanonical_or_malformed_names_refuse(self):
        for bad in ('', 's4', 'sFF', 'sff', 'n00', 'n-1', 'x12', 's41/', 's41//s42'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.api.decode(bad)

    def test_unicode_visible_target_is_not_lost(self):
        name = 'CapFirstExit.iteratedFDeriv_three_swap₁₂'
        rows = [('theorem', 'user', M, enc(*name.split('.')), 'safe')]
        report = self.api.audit_inventory(transcript(rows, [], []), {name: 'theorem'}, [])
        self.assertEqual(report['visible_declarations'], 1)

    def test_hidden_private_user_theorem_rejects_even_if_manifest_lists_it(self):
        hidden = ('theorem', 'user', M, enc('_private', 'CapFirstExit', 0, 'CapFirstExit', 'hidden'), 'safe')
        self.reject(transcript(ROWS + [hidden]), 'extra_user_theorem', BOUND + [list(hidden)])

    def test_hidden_public_user_theorem_rejects_even_if_manifest_lists_it(self):
        hidden = ('theorem', 'user', M, enc('CapFirstExit', 'hidden'), 'safe')
        self.reject(transcript(ROWS + [hidden]), 'extra_user_theorem', BOUND + [list(hidden)])

    def test_user_definition_cannot_be_laundered_as_structure_support(self):
        hidden = ('def', 'user', M, enc('CapFirstExit', 'CapHyp', 'hidden'), 'safe')
        self.reject(transcript(ROWS + [hidden]), 'extra_user_definition', BOUND + [list(hidden)])

    def test_structural_relation_requires_visible_inductive_parent(self):
        self.reject(transcript(relations=[('projection', P, T)] + RELATIONS[1:]), 'invalid_structural_relation')

    def test_missing_projection_relation_refuses_user_generated_support(self):
        self.reject(transcript(relations=RELATIONS[1:]), 'extra_user_definition')

    def test_prop_projection_theorem_uses_actual_structure_relation(self):
        rows = list(ROWS)
        rows[3] = ('theorem', 'user', M, P, 'safe')
        bound = [list(r) for r in rows[3:]]
        report = self.api.audit_inventory(transcript(rows), VISIBLE, bound)
        self.assertEqual(report['declarations'], 7)

    def test_wrong_structural_kind_refuses(self):
        self.reject(transcript(relations=[('constructor', P, S)] + RELATIONS[1:]), 'invalid_structural_relation')

    def test_generated_provenance_is_bound_exactly(self):
        rows = list(ROWS); rows[-1] = ('theorem', 'user', M, A, 'safe')
        self.reject(transcript(rows), 'extra_user_theorem')

    def test_compiler_shaped_added_theorem_is_not_automatically_admitted(self):
        hidden = ('theorem', 'aux', M, enc('CapFirstExit', 'visible', '_proof_999'), 'safe')
        self.reject(transcript(ROWS + [hidden]), 'unregistered_constant')

    def test_auxiliary_theorem_without_real_visible_parent_refuses_even_if_bound(self):
        hidden = ('theorem', 'aux', M, enc('CapFirstExit', 'absent', '_proof_1'), 'safe')
        self.reject(transcript(ROWS + [hidden]), 'unbound_auxiliary', BOUND + [list(hidden)])

    def test_missing_or_changed_support_record_refuses(self):
        self.reject(transcript(), 'unregistered_constant', BOUND[:-1])
        extra = ['def', 'aux', M, enc('CapFirstExit', 'not_present'), 'safe']
        self.reject(transcript(), 'missing_constant', BOUND + [extra])

    def test_visible_kind_change_refuses(self):
        rows = list(ROWS); rows[0] = ('def', 'user', M, T, 'safe')
        self.reject(transcript(rows), 'visible_kind')

    def test_missing_visible_definition_and_structure_refuse(self):
        self.reject(transcript([r for r in ROWS if r[3] != D]), 'missing_visible')
        self.reject(transcript([r for r in ROWS if r[3] != S]), 'missing_visible')

    def test_duplicate_names_and_module_counts_refuse(self):
        self.reject(transcript(ROWS + [ROWS[0]]), 'duplicate_name')
        self.reject(transcript(count=8), 'count_mismatch')

    def test_missing_duplicate_and_extra_module_refuse(self):
        self.reject(transcript().split('\n', 1)[1], 'missing_module')
        self.reject('MODULE|%s|false|7|0\n' % M + transcript(), 'duplicate_module')
        self.reject('MODULE|%s|false|0|0\n' % enc('CapFirstExit','Extra') + transcript(), 'unregistered_module')

    def test_module_system_and_codegen_extras_fail_closed(self):
        self.reject(transcript(module_system='true'), 'module_system')
        self.reject(transcript(extra=1), 'codegen_extra')

    def codegen_call(self, text, records):
        self.assertIn('codegen_records', inspect.signature(self.api.audit_inventory).parameters,
                      'actual IR-name admission is not implemented')
        return self.api.audit_inventory(text,VISIBLE,BOUND,codegen_records=records)

    def test_actual_abel_suffix_is_admitted_only_with_exact_binding(self):
        row=('theorem','aux',M,enc('CapFirstExit','visible','_abel_1_1'),'safe')
        try:
            report=self.api.audit_inventory(transcript(ROWS+[row]),VISIBLE,BOUND+[list(row)])
        except ValueError as error:
            self.fail('observed generated Abel support is unsupported: '+str(error))
        self.assertEqual(report['declarations'],8)
        self.reject(transcript(ROWS+[row]),'unregistered_constant')

    def test_codegen_extras_are_exactly_bound_not_ignored(self):
        name=enc('CapFirstExit','datum','_boxed')
        text=transcript(extra=1)+'EXTRA|'+M+'|'+name+'\n'
        report=self.codegen_call(text,[[M,name]])
        self.assertEqual(report['codegen_entries'],1)
        with self.assertRaisesRegex(ValueError,'codegen_binding'):
            self.codegen_call(text,[])

    def test_codegen_duplicate_or_wrong_names_refuse(self):
        name=enc('CapFirstExit','datum','_boxed')
        line='EXTRA|'+M+'|'+name+'\n'
        text=transcript(extra=2)+line+line
        with self.assertRaisesRegex(ValueError,'duplicate_codegen'):
            self.codegen_call(text,[[M,name]])
        with self.assertRaisesRegex(ValueError,'codegen_binding'):
            self.codegen_call(transcript(extra=1)+line,[[M,enc('CapFirstExit','wrong')]])

    def test_outside_module_cannot_hide_owned_constant(self):
        rows = list(ROWS); rows[-1] = ('theorem', 'aux', enc('Elsewhere'), A, 'safe')
        self.reject(transcript(rows), 'outside_module')

    def test_owned_axiom_is_forbidden_even_if_approved_name_and_bound(self):
        row = ('axiom', 'user', M, enc('propext'), 'safe')
        self.reject(transcript(ROWS + [row]), 'package_axiom', BOUND + [list(row)])

    def test_unused_sorry_and_custom_axiom_closure_refuse(self):
        for axiom in ('sorryAx', 'hiddenPremise'):
            self.reject(transcript(axioms=[enc(axiom)]), 'forbidden_axiom')

    def test_target_axiom_omission_and_duplicate_axiom_refuse(self):
        self.reject(transcript(axioms=[]), 'reported_axiom_omitted', reported={'x':['propext']})
        self.reject(transcript(axioms=[enc('propext')]*2), 'duplicate_axiom')

    def test_unsafe_or_partial_constant_refuses_even_if_bound(self):
        for safety in ('unsafe', 'partial'):
            row = ('def','aux',M,enc('CapFirstExit','unsafeHelper'),safety)
            self.reject(transcript(ROWS+[row]), 'unsafe_or_partial', BOUND+[list(row)])

    def test_owned_opaque_and_quot_never_self_admit(self):
        for kind in ('opaque','quot'):
            row = (kind,'aux',M,enc('CapFirstExit','unexpectedKind'),'safe')
            self.reject(transcript(ROWS+[row]), 'unsupported_owned_kind', BOUND+[list(row)])

    def test_private_numeric_identity_cannot_collapse(self):
        rows = [('def','aux',M,enc('_private','CapFirstExit',0,'x'),'safe')]
        bound = [['def','aux',M,enc('_private','CapFirstExit',1,'x'),'safe']]
        visible = {'CapFirstExit.visible':'theorem'}
        self.reject(transcript(ROWS[:1]+rows, [], []), 'unregistered_constant', bound, visible)

    def test_protocol_junk_missing_summary_and_malformed_record_refuse(self):
        for text in ('error: broken\n'+transcript(), transcript()+'warning: ignored\n',
                     transcript().replace('AXIOMS|'+enc('propext')+'\n',''),
                     transcript().replace('INV|theorem|user|','INV|unknown|user|',1)):
            with self.subTest(text=text), self.assertRaises(ValueError):
                self.api.audit_inventory(text, VISIBLE, BOUND)

    def test_duplicate_summary_and_impossible_closure_refuse(self):
        self.reject(transcript()+'AXIOMS|\n', 'protocol')
        self.reject(transcript().replace('CLOSURE|18','CLOSURE|1'), 'impossible_closure')

    def test_binding_duplicates_target_shadowing_and_bad_records_refuse(self):
        self.reject(transcript(), 'duplicate_binding', BOUND+[BOUND[0]])
        self.reject(transcript(), 'target_shadowing', BOUND+[list(ROWS[0])])
        self.reject(transcript(), 'binding', [['def','aux',M,'not-encoded','safe']])

    def test_generated_exporter_selects_module_tables_and_emits_protocol(self):
        text = self.api.inventory_source()
        # Behavioral compilation of this generated program is a separate actual Lean control.
        self.assertIn('import CapFirstExit\n', text)
        self.assertIn('header.moduleData[idx]!', text)
        self.assertIn('data.constNames', text)
        self.assertIn('REL|', text)


if __name__ == '__main__':
    unittest.main(verbosity=2)
