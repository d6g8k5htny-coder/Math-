"""Keep the factorial job finite without dropping either full regression mode.

Run 37463704292/1 completed its normal 243-test suite in 317.516 seconds,
then was cancelled during optimized discovery near its 10-minute job limit.
The 20-minute envelope is an operational budget, not a runtime guarantee or
permission to increase the unchanged 300-second numerical child limit.
These tests inspect the current restricted workflow layout, not GitHub's scheduler.
"""
from pathlib import Path
import ast
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / '.github/workflows/c6-factorial-moment.yml'
REGRESSION = 'Full repository regression suite in both Python modes'
NUMERICAL = 'Verify sources, replay both modes, reject mutants'


def named_step(text, name):
    marker = '      - name: ' + name + '\n'
    if text.count(marker) != 1:
        raise ValueError('expected one named step: ' + name)
    return text.split(marker, 1)[1].split('      - ', 1)[0]


def run_block(step):
    marker = '        run: |\n'
    if step.count(marker) != 1:
        raise ValueError('expected one literal run block')
    lines = step.split(marker, 1)[1].splitlines()
    if not lines or any(not line.startswith('          ') for line in lines):
        raise ValueError('unsupported run-block indentation')
    return '\n'.join(line[10:] for line in lines) + '\n'


class FactorialJobBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding='utf-8')

    def test_one_explicit_finite_job_budget(self):
        # Do not accidentally accept a step timeout, default 360, or expression.
        limits = re.findall(r'^\s*timeout-minutes:.*$', self.text, re.MULTILINE)
        self.assertEqual(limits, ['    timeout-minutes: 20'])
        self.assertIn('  exact-and-probe:\n    runs-on: ubuntu-latest\n'
                      '    timeout-minutes: 20\n    steps:\n', self.text)

    def test_both_complete_regression_modes_run_before_manual_packet(self):
        # C166: the PR-time run moved to full-regression-suite.yml. Here the
        # exact block stays, guarded only by the one manual-dispatch condition;
        # no other condition, bypass or always-run override is permitted.
        step = named_step(self.text, REGRESSION)
        self.assertEqual(step,
                         "        if: github.event_name == 'workflow_dispatch'\n"
                         '        run: |\n'
                         '          set -euo pipefail\n'
                         '          python -B -S -m unittest discover -s tests -v\n'
                         '          python -B -O -S -m unittest discover -s tests -v\n')
        self.assertLess(self.text.index(REGRESSION), self.text.index(NUMERICAL))
        self.assertEqual(re.findall(r'^.*\bif:.*$', self.text, re.MULTILINE),
                         ["        if: github.event_name == 'workflow_dispatch'"])
        for bypass in ('continue-on-error:', 'background:', 'always()', 'failure()', 'cancelled()'):
            self.assertNotIn(bypass, self.text)

    def test_numerical_budget_inventory_and_postflight_remain(self):
        block = run_block(named_step(self.text, NUMERICAL))
        self.assertTrue(block.startswith("set -euo pipefail\npython -B -S - <<'PY'\n"))
        self.assertTrue(block.endswith('PY\ngit diff --exit-code\n'))
        program = block.split("<<'PY'\n", 1)[1].rsplit('\nPY\n', 1)[0]
        module = ast.parse(program)
        calls = [n for n in ast.walk(module) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name) and n.func.id == 'replay']
        self.assertEqual(len(calls), 1)
        call = calls[0]
        self.assertEqual([(kw.arg, ast.literal_eval(kw.value)) for kw in call.keywords],
                         [('timeout', 300)])
        loops = [n for n in module.body if isinstance(n, ast.For)
                 and isinstance(n.target, ast.Name) and n.target.id == 'flags']
        self.assertEqual(len(loops), 1)
        self.assertEqual(ast.literal_eval(loops[0].iter), (['-B', '-S'], ['-B', '-O', '-S']))
        mutants = next(n.value for n in module.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'mutants' for t in n.targets))
        self.assertEqual(ast.literal_eval(mutants),
                         ['wrong-elimination', 'touching-balls', 'no-log', 'short-remainder'])
        for guard in ('packet tree differs from manifest:', 'flat regular source required:',
                      'source identity mismatch:', "'mathematical_acceptance': False"):
            self.assertIn(guard, program)

    def test_new_test_is_covered_and_execution_permissions_are_unchanged(self):
        # C166: tests/** coverage is central; this packet keeps its own tests.
        central = (ROOT / '.github/workflows/full-regression-suite.yml').read_text(encoding='utf-8')
        self.assertIn("      - 'tests/**'\n", central)
        self.assertNotIn("      - 'tests/**'\n", self.text)
        self.assertIn("      - 'tests/test_c6_factorial_job_budget.py'\n", self.text)
        self.assertIn("      - 'tests/test_d5_c6_workflows.py'\n", self.text)
        self.assertIn('permissions:\n  contents: read\n', self.text)
        self.assertIn('          persist-credentials: false\n          fetch-depth: 0\n', self.text)
        self.assertIn("          python-version: '3.11.16'\n", self.text)
        self.assertIn('actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1', self.text)
        self.assertIn('actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97', self.text)


if __name__ == '__main__':
    unittest.main()
