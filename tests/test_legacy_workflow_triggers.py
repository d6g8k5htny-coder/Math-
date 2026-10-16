"""Named legacy import-resolution triggers; real imports, not a GitHub scheduler.

The loader below intentionally accepts only these workflows' simple, positive,
single-quoted path lists and literal/prefix/** patterns. Unsupported syntax fails
rather than pretending to implement the general GitHub glob/YAML language.
Synthetic helper bodies demonstrate resolution only, not numerical correctness.
"""
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tests/test_legacy_workflow_triggers.py'
FAMILIES = {
    'local-pairing.yml': 'frontiers/local_pairing_20260930',
    'far-elder-rate.yml': 'frontiers/far_elder_rate_20260930',
    'c6-cluster-law.yml': 'frontiers/c6_cluster_law_20260929',
}
STEP = (
    '      - name: Check legacy import-resolution trigger coverage\n'
    '        run: |\n'
    '          python -B -S ' + SELF + '\n'
    '          python -B -O -S ' + SELF + '\n'
)


def workflow_text(name):
    return (ROOT / '.github' / 'workflows' / name).read_text(encoding='utf-8')


def trigger_paths(text):
    start = "'on':\n  pull_request:\n    paths:\n"
    if text.count(start) != 1:
        raise ValueError('expected one plain pull-request path list')
    rows = text.split(start, 1)[1].split('  workflow_dispatch:\n', 1)
    if len(rows) != 2:
        raise ValueError('expected workflow-dispatch after path list')
    found = []
    for line in rows[0].splitlines():
        match = re.fullmatch(r"      - '([^']+)'", line)
        if not match or match[1].startswith('!'):
            raise ValueError('unsupported path-list syntax')
        pattern = match[1]
        plain = pattern[:-3] if pattern.endswith('/**') else pattern
        if any(c in plain for c in '*?[]{}!'):
            raise ValueError('unsupported path pattern')
        found.append(pattern)
    if not found or len(found) != len(set(found)):
        raise ValueError('empty or duplicate path list')
    return found


def covered(patterns, path):
    # Only literal names or whole subtrees, as validated by trigger_paths.
    return any(path.startswith(p[:-2]) if p.endswith('/**') else path == p
               for p in patterns)


class LegacyTriggerTests(unittest.TestCase):
    def test_package_and_root_module_changes_are_covered(self):
        for name in FAMILIES:
            paths = trigger_paths(workflow_text(name))
            for path in ('tools/__init__.py', 'tools.py', 'tools/nested/input.py'):
                with self.subTest(workflow=name, path=path):
                    self.assertTrue(covered(paths, path), 'resolver change lacks replay trigger')

    def test_original_paths_and_new_regression_remain_covered(self):
        for name, packet in FAMILIES.items():
            paths = trigger_paths(workflow_text(name))
            for path in (packet + '/checker.py', '.github/workflows/' + name,
                         'tools/legacy_json_replay.py', 'tools/legacy_json_contracts.json',
                         'tests/test_legacy_json_workflows.py', SELF):
                with self.subTest(workflow=name, path=path):
                    self.assertTrue(covered(paths, path), 'consumed or regression path is uncovered')
            for path in ('README.md', 'unrelated/tools.py', 'tools_extra/file.py'):
                with self.subTest(workflow=name, unrelated=path):
                    self.assertFalse(covered(paths, path), 'unexpected unrelated trigger')

    def test_new_checks_run_in_both_modes_before_existing_replay(self):
        for name in FAMILIES:
            text = workflow_text(name)
            with self.subTest(workflow=name):
                self.assertEqual(text.count(STEP), 1, 'missing exact two-mode trigger-test step')
                self.assertLess(text.index(STEP), text.index(
                    '      - name: Exercise the complete shell rejection contract in both modes\n'))

    def test_original_import_actually_uses_both_resolver_inputs(self):
        for name in FAMILIES:
            lines = [s.strip() for s in workflow_text(name).splitlines()
                     if s.strip().startswith('from tools.')]
            self.assertEqual(lines, ['from tools.legacy_json_replay import replay'])
            program = lines[0] + "\nprint(replay())\n"
            for flags in (['-B', '-S'], ['-B', '-O', '-S']):
                for variant in ('namespace', 'initializer', 'root-module'):
                    with self.subTest(workflow=name, flags=flags, variant=variant), \
                            tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        (root / 'tools').mkdir()
                        (root / 'tools/legacy_json_replay.py').write_text(
                            "def replay(): return 'SYNTHETIC_HELPER'\n", encoding='utf-8')
                        if variant != 'namespace':
                            target = ('tools/__init__.py' if variant == 'initializer'
                                      else 'tools.py')
                            (root / target).write_text(
                                "from pathlib import Path\n"
                                "Path('resolver.marker').write_text('executed')\n",
                                encoding='utf-8')
                        # Private process environment; do not alter caller configuration.
                        env = {k: v for k, v in os.environ.items() if not k.startswith('PYTHON')}
                        child = subprocess.run([sys.executable, *flags, '-'], input=program.encode(),
                                               cwd=root, env=env, capture_output=True, timeout=10)
                        marker = root / 'resolver.marker'
                        self.assertEqual(marker.exists(), variant != 'namespace')
                        if marker.exists():
                            self.assertEqual(marker.read_text(), 'executed')
                        if variant == 'root-module':
                            self.assertEqual(child.returncode, 1)
                            self.assertEqual(child.stdout, b'')
                            self.assertIn(b'ModuleNotFoundError', child.stderr)
                            self.assertIn(b"'tools' is not a package", child.stderr)
                        else:
                            self.assertEqual((child.returncode, child.stdout, child.stderr),
                                             (0, b'SYNTHETIC_HELPER\n', b''))

    def test_limited_path_reader_rejects_unsupported_syntax(self):
        template = "'on':\n  pull_request:\n    paths:\n%s  workflow_dispatch:\n"
        for rows in ("      - '!tools.py'\n", "      - tools.py\n",
                     "      - 'tools.*'\n", "      - 'tools.py'\n      - 'tools.py'\n", ''):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                trigger_paths(template % rows)


if __name__ == '__main__':
    unittest.main()
