"""External controls for C6 residual child output admissibility (no proof edits)."""
import copy
import json
import pathlib
import sys
import unittest
from subprocess import CompletedProcess

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'tools'))
from c6_residual_child_contract import (CHECK_NAMES, EXPECTED_FAILURES,
                                        validate_baseline, validate_mutant)


def packet(state='baseline'):
    return dict(object='C6-RESIDUAL-CLOSURE-20260930-v1',
                checks={name: True for name in CHECK_NAMES}, passed=True,
                inventory_files=13, component_nodes=10, scope='pinned mathematical scope',
                register_state=state, live_state={'state': state}, gate={})


def output(payload, *, returncode=1, stderr=b''):
    return CompletedProcess(['residual_check.py'], returncode,
                            stdout=json.dumps(payload, sort_keys=True).encode(), stderr=stderr)


class ChildContracts(unittest.TestCase):
    def test_baseline_in_both_register_states(self):
        for state in ('baseline', 'installed'):
            original = packet(state)
            out = output(original, returncode=0)
            with self.subTest(state=state):
                self.assertEqual(validate_baseline(out, out.stdout), original)
                with self.assertRaises(ValueError):
                    validate_baseline(output(original, returncode=0, stderr=b'warning'), out.stdout)
                with self.assertRaises(ValueError):
                    validate_baseline(output(original, returncode=0), b'changed')

    def test_all_fifteen_frozen_mutant_failure_sets_in_both_states(self):
        for state in ('baseline', 'installed'):
            baseline = packet(state)
            for mutant, expected_failed in EXPECTED_FAILURES.items():
                result = copy.deepcopy(baseline)
                result['passed'] = False
                for name in expected_failed:
                    result['checks'][name] = False
                with self.subTest(state=state, mutant=mutant):
                    self.assertEqual(validate_mutant(mutant, output(result), baseline), result)
                    bad = copy.deepcopy(result)
                    bad['checks'] = dict.fromkeys(CHECK_NAMES, True)
                    bad['checks']['IDENTITIES'] = False
                    if expected_failed != frozenset(('IDENTITIES',)):
                        with self.assertRaises(ValueError):
                            validate_mutant(mutant, output(bad), baseline)

    def test_crash_silence_wrong_exit_and_extra_stderr_are_refused(self):
        baseline = packet()
        example = copy.deepcopy(baseline)
        example['passed'] = False
        example['checks']['DEDUCTION'] = False
        for child in [CompletedProcess([], 1, b'', b''),
                      CompletedProcess([], 1, b'', b'Traceback: unrelated crash'),
                      output(example, returncode=0),
                      output(example, stderr=b'warning'),
                      CompletedProcess([], 1, b'not-json', b'')]:
            with self.subTest(child=child):
                with self.assertRaises(ValueError):
                    validate_mutant('tail-reversed', child, baseline)

    def test_structural_invalidity_and_type_confusion(self):
        baseline = packet()
        good = copy.deepcopy(baseline)
        good['passed'] = False
        good['checks']['DEDUCTION'] = False
        mutations = []
        for key, value in [('object','DIFFERENT'), ('passed',0), ('register_state','fake'),
                           ('scope','changed'), ('inventory_files',True),
                           ('component_nodes','10'), ('gate',None)]:
            changed = copy.deepcopy(good)
            changed[key] = value
            mutations.append(changed)
        changed = copy.deepcopy(good)
        changed['checks']['DEDUCTION'] = 0
        mutations.append(changed)
        changed = copy.deepcopy(good)
        del changed['checks']['DEDUCTION']
        mutations.append(changed)
        changed = copy.deepcopy(good)
        changed['checks']['OTHER'] = False
        mutations.append(changed)
        changed = copy.deepcopy(good)
        changed['extra'] = 'field'
        mutations.append(changed)
        changed = copy.deepcopy(good)
        changed['live_state']['state'] = 'installed'
        mutations.append(changed)
        for changed in mutations:
            with self.subTest(changed=changed):
                with self.assertRaises(ValueError):
                    validate_mutant('tail-reversed', output(changed), baseline)

    def test_duplicate_fields_nonfinite_and_extra_json(self):
        baseline = packet()
        for data in (b'{"passed":false,"passed":false}', b'{"x":NaN}',
                     b'{"x":Infinity}', b'{}{}'):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    validate_mutant('tail-reversed', CompletedProcess([],1,data,b''), baseline)

if __name__ == '__main__':
    unittest.main()
