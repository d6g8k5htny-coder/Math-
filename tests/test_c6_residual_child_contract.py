"""External controls for C6 residual child output admissibility (no proof edits)."""
import copy
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from subprocess import CompletedProcess

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'tools'))
from c6_residual_child_contract import (CHECK_NAMES, EXPECTED_FAILURES_BY_STATE,
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
            for mutant, expected_failed in EXPECTED_FAILURES_BY_STATE[state].items():
                result = copy.deepcopy(baseline)
                result['passed'] = False
                for name in expected_failed:
                    result['checks'][name] = False
                if 'LIVE' in expected_failed:
                    result['register_state'] = 'partial'
                    result['live_state']['state'] = 'partial'
                with self.subTest(state=state, mutant=mutant):
                    self.assertEqual(validate_mutant(mutant, output(result), baseline), result)
                    bad = copy.deepcopy(result)
                    bad['checks'] = dict.fromkeys(CHECK_NAMES, True)
                    bad['checks']['IDENTITIES'] = False
                    if expected_failed != frozenset(('IDENTITIES',)):
                        with self.assertRaises(ValueError):
                            validate_mutant(mutant, output(bad), baseline)
                    if 'LIVE' not in expected_failed:
                        bad_state = copy.deepcopy(result)
                        bad_state['register_state'] = 'partial'
                        bad_state['live_state']['state'] = 'partial'
                        with self.assertRaises(ValueError):
                            validate_mutant(mutant, output(bad_state), baseline)

    def test_three_state_dependent_mutants_against_checker_installed_graph(self):
        repo = pathlib.Path(__file__).resolve().parents[1]
        checker_path = (repo / 'reviews/c6_residual_closure_20260930' /
                        'residual_check.py')
        module_spec = importlib.util.spec_from_file_location('c6_residual_checker',
                                                             checker_path)
        checker = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(checker)

        source_graph = json.loads(
            (repo / 'frontiers/downstream_gate_20260925/GRAPH.json').read_text())
        proposal = json.loads(
            (repo / 'reviews/c6_residual_closure_20260930' /
             'PROPOSED_TRANSITIONS.json').read_text())
        installed = checker.build(proposal, source_graph, 'final')[1]

        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            shutil.copytree(repo / 'frontiers', root / 'frontiers')
            shutil.copytree(repo / 'reviews', root / 'reviews')
            graph_path = root / 'frontiers/downstream_gate_20260925/GRAPH.json'
            graph_path.write_text(json.dumps(installed, indent=2, sort_keys=True) + '\n')
            script = root / 'reviews/c6_residual_closure_20260930/residual_check.py'
            pinned = (root / 'reviews/c6_residual_closure_20260930' /
                      'RESULTS_INSTALLED.json').read_bytes()

            for flags in (('-B', '-S'), ('-B', '-O', '-S')):
                base_proc = subprocess.run(
                    [sys.executable, *flags, str(script)],
                    cwd=root, capture_output=True, timeout=300)
                baseline = validate_baseline(base_proc, pinned)
                self.assertEqual(baseline['register_state'], 'installed')
                for mutant in ('stale-fingerprint', 'record-unreviewed',
                               'installed-drift'):
                    proc = subprocess.run(
                        [sys.executable, *flags, str(script), '--mutant', mutant],
                        cwd=root, capture_output=True, timeout=300)
                    with self.subTest(flags=flags, mutant=mutant):
                        validate_mutant(mutant, proc, baseline)

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

    def test_workflow_wires_strict_child_validation(self):
        workflow = (pathlib.Path(__file__).resolve().parents[1] /
                    '.github/workflows/c6-residual-closure.yml').read_text()
        self.assertIn('from c6_residual_child_contract import validate_baseline, validate_mutant', workflow)
        self.assertIn('validate_baseline(base_proc, expected)', workflow)
        self.assertIn('validate_mutant(m, proc, baseline)', workflow)

    def test_duplicate_fields_nonfinite_and_extra_json(self):
        baseline = packet()
        for data in (b'{"passed":false,"passed":false}', b'{"x":NaN}',
                     b'{"x":Infinity}', b'{}{}'):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    validate_mutant('tail-reversed', CompletedProcess([],1,data,b''), baseline)

if __name__ == '__main__':
    unittest.main()
