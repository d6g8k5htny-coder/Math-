"""Finite process-contract regressions, not mathematical certification."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / 'frontiers/lifetime_dd_model_d_20261013/replay.py'
EXPECTED = (ROOT / 'tests/fixtures/lifetime_dd_changed_node_stdout.txt').read_bytes()
MISSING_TEMPLATE = (ROOT / 'tests/fixtures/lifetime_dd_missing_node_stderr.txt').read_bytes()
MISSING = MISSING_TEMPLATE.replace(b'<CERTIFICATE_V2>', str(WRAPPER.parent / 'certificate_v2').encode())


def load():
    spec = importlib.util.spec_from_file_location('dd_oracle_subject', WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NodeOracleTests(unittest.TestCase):
    def outcome(self, missing, changed=None):
        m = load()
        manifest = json.loads((WRAPPER.parent / 'SOURCES.json').read_text())
        outputs = [missing] if changed is None else [missing, changed]
        capture = io.StringIO()
        with mock.patch.object(m, 'run', side_effect=outputs):
            with contextlib.redirect_stdout(capture):
                failures = m.negative_failures(WRAPPER.parent, manifest, quick=changed is None)
        return failures, capture.getvalue()

    def test_changed_rejects_unrelated_results(self):
        cases = [(1,b'',b'Traceback: crash\n'), (17,b'failed',b'oom'), (-9,b'',b''),
                 (0,b'',b''), (0,b'unrelated',b''), (1,EXPECTED,b''),
                 (17,EXPECTED,b''), (-9,EXPECTED,b''), (0,EXPECTED,b'warning'),
                 (0,EXPECTED[:-1],b''), (0,EXPECTED+b'noise',b''),
                 (0,EXPECTED+b'\n',b''), (0,b'noise'+EXPECTED,b''),
                 (0,EXPECTED+EXPECTED,b''),
                 (0,EXPECTED.replace(b'0.075705195564',b'0.075705195565'),b'')]
        for case in cases:
            with self.subTest(case=case):
                failures,_ = self.outcome((1,b'',MISSING),case)
                self.assertTrue(any('negative control (b)' in f for f in failures),failures)

    def test_changed_accepts_exact_sensitivity(self):
        failures, output = self.outcome((1,b'',MISSING),(0,EXPECTED,b''))
        self.assertEqual(failures,[])
        records=[json.loads(line) for line in output.splitlines()]
        records=[r for r in records if r.get('output_sensitivity_verified') is True]
        self.assertEqual(len(records),1)
        self.assertNotIn('rejected',records[0])

    def test_changed_fixture_identity(self):
        self.assertEqual(len(EXPECTED),989)
        self.assertEqual(hashlib.sha256(EXPECTED).hexdigest(),
                         '1e547fee84313e3fd62d822c97f9c76b08335112bcd71337e00bc06ea4a31bf8')
        stored=(WRAPPER.parent/'certificate_v2/results/assembly_stdout.txt').read_bytes()
        self.assertNotEqual(EXPECTED,b'\n'.join(x for x in stored.split(b'\n') if not x.startswith(b'C9')))

    def test_missing_rejects_inexact_results(self):
        cases=[(1,b'noise',MISSING),(1,b'',b'error incomplete node values\n'),
               (1,b'',MISSING.replace(b'2194 of 2393',b'0 of 1')),
               (1,b'',MISSING.replace(b'AssertionError:',b'RuntimeError:')),
               (1,b'',MISSING.replace(b'ddcore.py',b'other.py')),
               (1,b'',MISSING.replace(b'line 23,',b'line 24,')),
               (1,b'',MISSING[:-1]),(1,b'',MISSING+b'\n'),
               (1,b'',MISSING+b'noise'),(1,b'',b'noise'+MISSING),
               (1,b'',MISSING+MISSING),
               (1,b'',MISSING.replace(str(WRAPPER.parent).encode(),b'/wrong')),
               (1,b'',b''),(0,b'',MISSING),(17,b'',MISSING),(-9,b'',MISSING)]
        for case in cases:
            with self.subTest(case=case):
                failures,_=self.outcome(case)
                self.assertTrue(any('negative control (c)' in f for f in failures),failures)

    def test_missing_accepts_exact_completeness_rejection(self):
        failures,output=self.outcome((1,b'',MISSING))
        self.assertEqual(failures,[])
        self.assertIn('"input_completeness_rejection_verified": true',output)

    def test_missing_fixture_identity(self):
        self.assertEqual(hashlib.sha256(MISSING_TEMPLATE).hexdigest(),
                         '74c9a35ac855ac1abba7c48a3eb1f25333b277738fd75da47fa8c73fe402833b')

    def test_real_bounded_specimens(self):
        m=load()
        capture=io.StringIO()
        with contextlib.redirect_stdout(capture):
            failures=m.negative_failures(WRAPPER.parent,json.loads((WRAPPER.parent/'SOURCES.json').read_text()),False)
        self.assertEqual(failures,[])
        self.assertIn('"output_sensitivity_verified": true',capture.getvalue())
        self.assertIn('"input_completeness_rejection_verified": true',capture.getvalue())

    def test_workflow_binding(self):
        text=(ROOT/'.github/workflows/lifetime-dd-model-d.yml').read_text()
        for name in ('tests/test_lifetime_dd_node_oracle.py',
                     'tests/fixtures/lifetime_dd_changed_node_stdout.txt',
                     'tests/fixtures/lifetime_dd_missing_node_stderr.txt'):
            self.assertIn("      - '"+name+"'",text)
            self.assertIn('cp '+name,text)
        self.assertIn('-p test_lifetime_dd_node_oracle.py -v',text)

    def mutations(self, needle, variants, methods):
        source=WRAPPER.read_text()
        self.assertEqual(source.count(needle),1)
        for name,replacement in variants.items():
            with self.subTest(mutation=name):
                subject=types.ModuleType('mutated_dd_oracle')
                subject.__file__=str(WRAPPER)
                exec(compile(source.replace(needle,replacement),str(WRAPPER),'exec'),subject.__dict__)
                suite=unittest.TestSuite(NodeOracleTests(method) for method in methods)
                capture=io.StringIO()
                with mock.patch.object(sys.modules[__name__],'load',return_value=subject):
                    with contextlib.redirect_stdout(capture):
                        result=unittest.TextTestRunner(stream=capture).run(suite)
                self.assertEqual(result.testsRun,2)
                self.assertEqual(result.errors,[],capture.getvalue())
                self.assertGreater(len(result.failures),0,capture.getvalue())

    def test_changed_mutations(self):
        self.mutations("if (code, out, err) != (0, CHANGED_NODE_STDOUT, b''):",{
            'generic_difference':"if code == 0 and out == b'unchanged baseline':",
            'ignore_exit':"if (out, err) != (CHANGED_NODE_STDOUT, b''):",
            'ignore_stderr':"if (code, out) != (0, CHANGED_NODE_STDOUT):",
            'ignore_stdout':"if (code, err) != (0, b''):",
            'strip':"if (code, out.strip(), err) != (0, CHANGED_NODE_STDOUT.strip(), b''):",
            'prefix':"if code != 0 or err or not out.startswith(CHANGED_NODE_STDOUT):",
            'accept':'if False:', 'reject':'if True:'},
            ('test_changed_rejects_unrelated_results','test_changed_accepts_exact_sensitivity'))

    def test_missing_mutations(self):
        self.mutations("if (code, out, err) != (1, b'', expected_missing):",{
            'substring':"if code != 1 or b'incomplete node values' not in err:",
            'ignore_exit':"if (out, err) != (b'', expected_missing):",
            'ignore_stdout':"if (code, err) != (1, expected_missing):",
            'ignore_stderr':"if (code, out) != (1, b''):",
            'strip':"if (code, out, err.strip()) != (1, b'', expected_missing.strip()):",
            'prefix':"if code != 1 or out or not err.startswith(expected_missing):",
            'accept':'if False:', 'reject':'if True:'},
            ('test_missing_rejects_inexact_results','test_missing_accepts_exact_completeness_rejection'))


if __name__ == '__main__':
    unittest.main()
